"""One Pilot 2 run for Stage 0 (protocol v0.3): childhood, life, evaluations, distances and logs.

Usage (from the Stadiul0 folder):
    python -m p2.run --family F1 --seed 1 [--out runs/F1_s1] [--set run.life_steps_per_task=512 ...]

The run writes per-step logs (section 3), per-chunk distances (section 5.1), probe evaluations
(sections 4.2, 4.3), per-episode displacements and drift (sections 5.2, 6) and the online
covariates that cannot be recomputed afterwards (section 7). Triplets, competitors and models are
built offline from these files.
"""
import os

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse
import copy
import ctypes
import hashlib
import json
import platform
import sys
import time
from collections import deque
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
import yaml

from .agent import FlatAgent, STEP_FIELDS
from .metrics import cka_distance, sqrt_js, sqrt_js_np
from .streams import EXPOSURE_KINDS, build_schedule
from .world import VOCAB, World

HERE = Path(__file__).resolve().parent.parent
EVAL_KINDS = ["life_start", "grid", "seg_end", "seg_end+grid", "idle_grid", "idle_end"]
SEG_KINDS = ["new", "reexp", "reh", "distractor", "idle"]
DISP_FIELDS = ["D1", "D1_rel", "D2", "D3", "D4", "T2"]
LN64 = float(np.log(64.0))                                 # clip level of F^clip (64 value tokens: chance loss)


def _peak_rss_mb():
    if platform.system() != "Windows":
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    class PMC(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong),
                    ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
    c = PMC()
    c.cb = ctypes.sizeof(PMC)
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.GetCurrentProcess.restype = ctypes.c_void_p
    k32.K32GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(PMC), ctypes.c_ulong]
    k32.K32GetProcessMemoryInfo.restype = ctypes.c_int
    if not k32.K32GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(c), c.cb):
        return float("nan")
    return c.PeakWorkingSetSize / 2 ** 20


def _set_path(cfg, dotted, value):
    keys = dotted.split(".")
    d = cfg
    for k in keys[:-1]:
        d = d[k]
    d[keys[-1]] = value


def load_config(path, overrides=()):
    raw = Path(path).read_bytes()
    cfg = yaml.safe_load(raw.decode("utf-8"))
    for item in overrides:
        k, v = item.split("=", 1)
        _set_path(cfg, k, yaml.safe_load(v))
    return cfg, hashlib.sha256(raw).hexdigest()


def array_hashes(arrays):
    return {k: hashlib.sha256(np.ascontiguousarray(arrays[k]).tobytes()).hexdigest() for k in sorted(arrays)}


class Timer:
    def __init__(self):
        self.t = {}

    def add(self, key, dt):
        self.t[key] = self.t.get(key, 0.0) + dt


class StrideState:
    """Chunked distances at one stride m over [start, end] in life steps (section 5.1)."""

    def __init__(self, m, start, end, P, chunked_param):
        self.m, self.start, self.end = m, start, end
        self.prev = None
        self.rows = []
        self.chunked_param = chunked_param
        if chunked_param:
            self.acc_pre = torch.zeros(P)
            self.acc_full = torch.zeros(P)
            self.lay_theta0 = None
            self.vlag0 = None

    def due(self, N):
        return self.start <= N <= self.end and (N - self.start) % self.m == 0


class Runner:
    def __init__(self, cfg, family, seed, out_dir, cfg_sha=""):
        torch.set_num_threads(1)
        try:
            torch.set_num_interop_threads(1)
        except RuntimeError:
            pass                                     # already set in this process
        torch.use_deterministic_algorithms(True)
        self.cfg, self.family, self.seed = cfg, family, seed
        self.cfg_sha = cfg_sha
        self.out = Path(out_dir)
        self.fam = fam = cfg["families"][family]
        r = cfg["run"]
        self.q0, self.grid = r["q0"], r["eval_grid"]
        ss = np.random.SeedSequence([int(seed), int(family[1:])])
        s_world, s_stream, s_init, s_batch = ss.spawn(4)
        self.world = World(cfg["world"], np.random.default_rng(s_world), fam["rule_frac"], fam["pi_overlap"])
        n_t = cfg["world"]["n_target"]
        self.segs, self.lr_life, self.restarts = build_schedule(
            fam, n_t, r["life_steps_per_task"], self.q0, cfg["optim"]["lr"],
            np.random.default_rng(s_stream), cfg["world"]["n_distractor"])
        self.life_steps = len(self.lr_life)
        torch.manual_seed(int(s_init.generate_state(1)[0]))
        self.agent = FlatAgent(cfg["agent"], cfg["optim"])
        self.rng = np.random.default_rng(s_batch)
        self.timer = Timer()

        # probe tensors, [n_target, 256, 4]
        W = self.world
        self.probe_x = torch.from_numpy(np.stack([t.probe_x for t in W.targets]))
        self.probe_y = torch.from_numpy(np.stack([t.probe_y for t in W.targets]))
        maskA = np.zeros((n_t, cfg["world"]["items_per_task"]), dtype=bool)
        for i, t in enumerate(W.targets):
            maskA[i, t.half_a] = True
        self.maskA = torch.from_numpy(maskA)
        self.R_x, self.R_y = torch.from_numpy(W.R_x), torch.from_numpy(W.R_y)
        self.B_x, self.B_y = torch.from_numpy(W.B_x), torch.from_numpy(W.B_y)
        self.value_tokens = W.vocab.value
        # q_k of every target task (section 7, input overlap), as sparse (ids, probabilities)
        self.qk = []
        for t in W.targets:
            ids, cnt = np.unique(t.train_pairs(), return_counts=True)
            self.qk.append((ids, cnt / cnt.sum()))
        self.pair_counter = np.zeros(VOCAB * VOCAB, dtype=np.int64)

        # D2 lag (section 5.1)
        self.L = r["d2_lag"]
        self.lag_mode = r["d2_lag_mode"]
        self.d2_block = int(r.get("d2_block", self.q0))   # Deep Review D9: 16 -> lag in [L, L + 15]
        self.vring = {}
        self.vexact = deque(maxlen=self.L + 1) if self.lag_mode == "both" else None

        self.strides = [StrideState(int(m), int(a), int(self.life_steps if b is None else b),
                                    self.agent.P, r["chunked_param_D"]) for m, a, b in r["d3_strides"]]
        self.snapD = set(r["snapshot_D"])
        self.dbuf = torch.zeros(self.agent.P)          # work buffers for displacements
        self.dbuf2 = torch.zeros(self.agent.P)

        # logs
        self.N, self.ca = 0, 0
        self.learned = set()
        self.active = {}                 # task -> episode id with an open snapshot
        self.episodes = []               # dicts
        self.snap = {}                   # episode id -> snapshot tensors
        self.step_stats, self.step_aux, self.step_d2exact = [], [], []
        self.ev = {k: [] for k in ["N", "ca", "kind", "seg", "theta_norm", "sqrt_trv", "L_R"]}
        self.probe_rows = []             # (e, k, LA, LB, AA, AB)
        self.disp_rows = []              # (ep, e, D1, D1_rel, D2, D3, D4, T2)
        self.last = None
        self.childhood = {}

    # ------------------------------------------------------------------ forward passes
    @torch.no_grad()
    def forward_items(self, X, Y, probs=False, reps=False, chunk=None):
        chunk = chunk or self.cfg["run"]["probe_chunk"]
        ce, cor, P, H = [], [], [], []
        for i in range(0, len(X), chunk):
            logits, h = self.agent.model(X[i: i + chunk], reps=True)
            y = Y[i: i + chunk]
            ce.append(F.cross_entropy(logits, y, reduction="none"))
            cor.append(logits.argmax(-1) == y)
            if probs:
                P.append(logits.softmax(-1))
            if reps:
                H.append(h)
        out = {"ce": torch.cat(ce), "correct": torch.cat(cor)}
        if probs:
            out["probs"] = torch.cat(P)
        if reps:
            out["reps"] = torch.cat(H)
        return out

    # ------------------------------------------------------------------ batches
    def batches(self, X, Y, steps, B, label_noise=0.0):
        n = len(X)
        assert (steps * B) % n == 0, "segment must end at the end of an epoch"
        per_epoch = n // B
        counts = np.zeros(n, dtype=np.int64)
        for s in range(steps):
            if s % per_epoch == 0:
                perm = self.rng.permutation(n)
            idx = perm[(s % per_epoch) * B: (s % per_epoch + 1) * B]
            counts[idx] += 1
            y = Y[idx].copy()
            if label_noise > 0:
                flip = self.rng.random(B) < label_noise
                y[flip] = self.value_tokens[self.rng.integers(0, 64, size=int(flip.sum()))]
            yield X[idx], y
        assert np.all(counts == counts[0]), "unbalanced exposure"

    # ------------------------------------------------------------------ v_hat lag
    def vhat_lag(self):
        if self.lag_mode == "none":
            return None
        blk = self.d2_block
        ref = blk * ((self.agent.t - self.L) // blk)
        return self.vring.get(ref) if ref > 0 else None

    def after_step_vring(self):
        t = self.agent.t
        blk = self.d2_block
        if t % blk == 0:
            self.vring[t] = self.agent.vhat().clone()
            for key in [k for k in self.vring if k < t - self.L - blk]:
                del self.vring[key]
        if self.vexact is not None:
            self.vexact.append(self.agent.vhat().clone())

    # ------------------------------------------------------------------ childhood
    def childhood_phase(self):
        r = self.cfg["run"]
        X, Y = self.world.childhood_x, self.world.childhood_y
        losses = []
        t0 = time.perf_counter()
        lr = self.cfg["optim"]["lr"]
        for x, y in self.batches(X, Y, r["childhood_steps"], r["childhood_batch"]):
            stats, _, _ = self.agent.step(torch.from_numpy(x), torch.from_numpy(y), lr, None)
            losses.append(float(stats[0]))
            self.after_step_vring()
        self.timer.add("childhood", time.perf_counter() - t0)
        ref_all = self.forward_items(torch.from_numpy(X), torch.from_numpy(Y))
        accR = self.forward_items(self.R_x, self.R_y)["correct"].double().mean().item()
        accB = self.forward_items(self.B_x, self.B_y)["correct"].double().mean().item()
        acc = ref_all["correct"].double().mean().item()
        kinds = np.array([t.kind for t in self.world.refs for _ in range(len(t.train_x))])
        cor = ref_all["correct"].numpy()
        self.childhood = {
            "steps": r["childhood_steps"], "acc_reference": acc, "acc_R": accR, "acc_B_beh": accB,
            "acc_reference_fact": float(cor[kinds == "fact"].mean()) if (kinds == "fact").any() else None,
            "acc_reference_rule": float(cor[kinds == "rule"].mean()) if (kinds == "rule").any() else None,
            "gate_passed": bool(acc >= r["childhood_gate"]), "final_loss": float(np.mean(losses[-64:])),
        }
        self.childhood_loss = np.array(losses)

    # ------------------------------------------------------------------ chunked distances
    def chunk_tick(self, dpre=None, full=None):
        N = self.N
        if dpre is not None:
            for s in self.strides:
                if s.chunked_param and s.start < N <= s.end:
                    s.acc_pre.add_(dpre)
                    s.acc_full.add_(full)
        due = [s for s in self.strides if s.due(N)]
        if not due:
            return
        t0 = time.perf_counter()
        o = self.forward_items(self.R_x, self.R_y, probs=True, reps=True)
        ceR = o["ce"].double()
        LR = ceR.mean().item()
        for s in due:
            if s.prev is not None and N > s.start:
                # C10b: |change of the mean loss on R|; C10c (Deep Review D5): mean over items of |change of the
                # per-item loss on R|, from the same forward pass as D3
                row = [N, sqrt_js(s.prev["probs"], o["probs"]).mean().item(),
                       cka_distance(s.prev["reps"], o["reps"]), abs(LR - s.prev["L"]),
                       (ceR - s.prev["ce"]).abs().mean().item()]
                if s.chunked_param:
                    a = self.agent
                    d1c = s.acc_full.double().norm().item()
                    d1r = torch.sqrt((a.layer_sq(s.acc_pre) / (s.lay_theta0 + 1e-12)).sum()).item()
                    d2c = (torch.sqrt((s.vlag0.double() * s.acc_pre.double().pow(2)).sum()).item()
                           if s.vlag0 is not None else float("nan"))
                    row += [d1c, d1r, d2c]
                s.rows.append(row)
            s.prev = {"probs": o["probs"], "reps": o["reps"], "L": LR, "ce": ceR}
            if s.chunked_param:
                s.acc_pre.zero_()
                s.acc_full.zero_()
                s.lay_theta0 = self.agent.layer_sq(self.agent.flat)
                s.vlag0 = self.vhat_lag()
        self.timer.add("chunks", time.perf_counter() - t0)

    # ------------------------------------------------------------------ evaluations
    def eval_point(self, kind, seg_index=-1, reuse=False):
        t0 = time.perf_counter()
        if not reuse:
            learned = sorted(self.learned)
            res = {"learned": learned}
            if learned:
                idx = torch.tensor(learned)
                X = self.probe_x[idx].reshape(-1, 4)
                Y = self.probe_y[idx].reshape(-1)
                o = self.forward_items(X, Y)
                ce = o["ce"].view(len(learned), -1).double()
                cor = o["correct"].view(len(learned), -1).double()
                mA = self.maskA[idx].double()
                mB = 1.0 - mA
                res["LA"] = ((ce * mA).sum(1) / mA.sum(1)).numpy()
                res["LB"] = ((ce * mB).sum(1) / mB.sum(1)).numpy()
                res["AA"] = ((cor * mA).sum(1) / mA.sum(1)).numpy()
                res["AB"] = ((cor * mB).sum(1) / mB.sum(1)).numpy()
                cec = ce.clamp(max=LN64)                       # Deep Review A3: loss clipped at ln 64, online
                res["LAc"] = ((cec * mA).sum(1) / mA.sum(1)).numpy()
                res["LBc"] = ((cec * mB).sum(1) / mB.sum(1)).numpy()
            oR = self.forward_items(self.R_x, self.R_y, probs=True, reps=True)
            oB = self.forward_items(self.B_x, self.B_y, probs=True)
            res["R_probs"], res["R_reps"] = oR["probs"], oR["reps"]
            res["L_R"] = oR["ce"].double().mean().item()
            res["B_probs"] = oB["probs"]
            fl = self.agent.flat
            res["theta_norm"] = float(torch.dot(fl, fl).double().sqrt())
            res["sqrt_trv"] = self.agent.trace_vhat() ** 0.5
            self.last = res
        res = self.last
        e = len(self.ev["N"])
        for key, val in [("N", self.N), ("ca", self.ca), ("kind", EVAL_KINDS.index(kind)), ("seg", seg_index),
                         ("theta_norm", res["theta_norm"]), ("sqrt_trv", res["sqrt_trv"]), ("L_R", res["L_R"])]:
            self.ev[key].append(val)
        for j, k in enumerate(res["learned"]):
            self.probe_rows.append((e, k, res["LA"][j], res["LB"][j], res["AA"][j], res["AB"][j],
                                    res["LAc"][j], res["LBc"][j]))
        self.timer.add("eval", time.perf_counter() - t0)
        t1 = time.perf_counter()
        for k, ep in self.active.items():
            self.disp_rows.append([ep, e] + self.displacement(self.snap[ep], res))
        self.timer.add("disp", time.perf_counter() - t1)
        return e

    @torch.no_grad()
    def displacement(self, s, res):
        a = self.agent
        out = []
        diff = None
        if "theta" in s:                       # float32 difference into a persistent buffer; dots in float32
            diff = torch.sub(a.flat, s["theta"], out=self.dbuf)
        out.append(float(torch.dot(diff, diff).double().sqrt()) if diff is not None and "D1" in self.snapD
                   else float("nan"))
        if diff is not None and "D1_rel" in self.snapD:
            out.append(torch.sqrt((a.layer_sq(diff) / (s["lay_theta"] + 1e-12)).sum()).item())
        else:
            out.append(float("nan"))
        if diff is not None and "vhat" in s:
            torch.mul(diff, diff, out=self.dbuf2)
            out.append(float(torch.dot(s["vhat"], self.dbuf2).double().sqrt()))
        else:
            out.append(float("nan"))
        out.append(sqrt_js(s["R_probs"], res["R_probs"]).mean().item() if "R_probs" in s else float("nan"))
        out.append(cka_distance(s["R_reps"], res["R_reps"]) if "R_reps" in s else float("nan"))
        out.append(sqrt_js(s["B_probs"], res["B_probs"]).mean().item() if "B_probs" in s else float("nan"))
        return out

    def eval_task_B(self, k):
        t = self.world.targets[k]
        X = torch.from_numpy(t.probe_x[t.half_b])
        Y = torch.from_numpy(t.probe_y[t.half_b])
        o = self.forward_items(X, Y)
        return o["ce"].double().mean().item(), o["correct"].double().mean().item()

    def overlap(self, k):
        tot = self.pair_counter.sum()
        if tot == 0:
            return float("nan")
        ids, p = self.qk[k]
        support = np.union1d(ids, np.flatnonzero(self.pair_counter))
        qh = self.pair_counter[support] / tot
        pk = np.zeros(len(support))
        pk[np.searchsorted(support, ids)] = p
        return 1.0 - sqrt_js_np(pk, qh)

    def open_episode(self, k, seg_index, seg_kind, prior, e, overlap):
        # overlap = 1 - sqrt(JS)(q_k, q_hist) with q_hist taken at the START of segment s0, before its own
        # steps are counted (Deep Review D4: it used to include the segment itself)
        ep = len(self.episodes)
        self.episodes.append({"task": k, "seg": seg_index, "kind": SEG_KINDS.index(seg_kind), "s0": self.N,
                              "t0": e, "prior_LB": prior[0], "prior_AB": prior[1], "overlap": overlap})
        a, res, s = self.agent, self.last, {}
        if self.snapD & {"D1", "D1_rel", "D2"}:
            s["theta"] = a.flat.clone()
            s["lay_theta"] = a.layer_sq(a.flat)
        if "D2" in self.snapD:
            s["vhat"] = a.vhat().clone()
        if "D3" in self.snapD:
            s["R_probs"] = res["R_probs"]
        if "D4" in self.snapD:
            s["R_reps"] = res["R_reps"]
        if "T2" in self.snapD:
            s["B_probs"] = res["B_probs"]
        self.snap[ep] = s
        self.active[k] = ep

    def close_episode(self, k):
        ep = self.active.pop(k, None)
        if ep is not None:
            del self.snap[ep]

    # ------------------------------------------------------------------ life
    def idle(self, seg, si):
        start, end = self.ca, self.ca + seg.ticks
        c = (start // self.grid + 1) * self.grid
        while c < end:
            self.ca = c
            self.eval_point("idle_grid", si, reuse=True)
            c += self.grid
        self.ca = end
        self.eval_point("idle_end", si, reuse=True)

    def life_phase(self):
        W = self.world
        self.eval_point("life_start")
        self.chunk_tick()
        prev_key = None
        for si, seg in enumerate(self.segs):
            if seg.kind == "idle":
                self.idle(seg, si)
                continue
            task = W.distractors[seg.task] if seg.kind == "distractor" else W.targets[seg.task]
            key = (task.token, seg.batch)
            boundary = key != prev_key
            prev_key = key
            exposure = seg.kind in EXPOSURE_KINDS
            prior, ov = None, None
            if exposure:
                self.close_episode(seg.task)
                t0 = time.perf_counter()
                prior = self.eval_task_B(seg.task)
                ov = self.overlap(seg.task)                    # q_hist before the segment
                self.timer.add("eval", time.perf_counter() - t0)
            for j, (x, y) in enumerate(self.batches(task.train_x, task.train_y, seg.steps, seg.batch,
                                                    seg.label_noise)):
                t0 = time.perf_counter()
                vlag = self.vhat_lag()
                lr = float(self.lr_life[self.N])
                stats, dpre, decay = self.agent.step(torch.from_numpy(x), torch.from_numpy(y), lr, vlag)
                self.step_stats.append(stats)
                self.step_aux.append((lr, seg.batch, seg.batch * 5, int(boundary and j == 0), si))
                if self.vexact is not None:
                    vx = self.vexact[0] if len(self.vexact) == self.L + 1 else None
                    self.step_d2exact.append(torch.sqrt((vx.double() * dpre.double().pow(2)).sum()).item()
                                             if vx is not None else float("nan"))
                np.add.at(self.pair_counter, x[:, 1] * VOCAB + x[:, 2], 1)
                self.N += 1
                self.ca += 1
                self.after_step_vring()
                self.timer.add("train", time.perf_counter() - t0)
                full = None
                if any(s.chunked_param for s in self.strides):
                    full = dpre.clone()
                    full[: self.agent.Pd] -= decay
                self.chunk_tick(dpre, full)
                if self.N % self.grid == 0 and j < seg.steps - 1:
                    self.eval_point("grid", si)
            if exposure:
                self.learned.add(seg.task)
            e = self.eval_point("seg_end+grid" if self.N % self.grid == 0 else "seg_end", si)
            if exposure:
                self.open_episode(seg.task, si, seg.kind, prior, e, ov)
        assert self.N == self.life_steps

    # ------------------------------------------------------------------ output
    def save(self, wall):
        out = self.out
        out.mkdir(parents=True, exist_ok=True)
        st = torch.stack(self.step_stats).numpy()
        steps = {f: st[:, i] for i, f in enumerate(STEP_FIELDS)}
        aux = np.array(self.step_aux, dtype=np.float64)
        for i, f in enumerate(["lr", "batch", "tokens", "boundary", "seg"]):
            steps[f] = aux[:, i]
        if self.step_d2exact:
            steps["D2_exact"] = np.array(self.step_d2exact)
        steps["childhood_loss"] = self.childhood_loss
        n_e, n_t = len(self.ev["N"]), self.cfg["world"]["n_target"]
        evals = {k: np.array(v, dtype=np.float64) for k, v in self.ev.items()}
        for name in ["LA", "LB", "AA", "AB", "LAc", "LBc"]:
            evals[name] = np.full((n_e, n_t), np.nan)
        for e, k, la, lb, aa, ab, lac, lbc in self.probe_rows:
            evals["LA"][e, k], evals["LB"][e, k], evals["AA"][e, k], evals["AB"][e, k] = la, lb, aa, ab
            evals["LAc"][e, k], evals["LBc"][e, k] = lac, lbc
        episodes = {k: np.array([ep[k] for ep in self.episodes], dtype=np.float64) for k in self.episodes[0]}
        disp = np.array(self.disp_rows, dtype=np.float64).reshape(-1, 2 + len(DISP_FIELDS))
        disp = {"ep": disp[:, 0], "e": disp[:, 1], **{f: disp[:, 2 + i] for i, f in enumerate(DISP_FIELDS)}}
        chunks = {}
        for s in self.strides:
            rows = np.array(s.rows, dtype=np.float64)
            names = ["N", "D3", "D4", "C10b", "C10c"] + (["D1c", "D1_relc", "D2c"] if s.chunked_param else [])
            for i, f in enumerate(names):
                chunks[f"m{s.m}_s{s.start}_{f}"] = rows[:, i] if len(rows) else np.empty(0)
        W = self.world
        world = {"kinds": np.array([t.kind == "rule" for t in W.targets], dtype=np.int8),
                 "n_values": np.array([t.n_values for t in W.targets]),
                 "moduli": np.array([t.modulus for t in W.targets]),
                 "train_pairs": np.stack([t.train_pairs() for t in W.targets]),
                 "key_overlap": W.key_overlap()}
        files = {"steps": steps, "evals": evals, "episodes": episodes, "disp": disp, "chunks": chunks,
                 "world": world}
        hashes = {}
        for name, arrays in files.items():
            np.savez_compressed(out / f"{name}.npz", **arrays)
            hashes[name] = array_hashes(arrays)
        (out / "schedule.json").write_text(json.dumps(
            {"segments": [s.as_dict() for s in self.segs], "restarts": self.restarts}, indent=0), encoding="utf-8")
        meta = {
            "family": self.family, "seed": self.seed, "config": self.cfg, "config_sha256": self.cfg_sha,
            "config_resolved_sha256": hashlib.sha256(json.dumps({k: v for k, v in self.cfg.items() if k not in ("analysis", "meta")},
                                                                sort_keys=True).encode("utf-8")).hexdigest(),
            "protocol": self.cfg["meta"]["protocol"],
            "versions": {"python": sys.version.split()[0], "torch": torch.__version__, "numpy": np.__version__,
                         "platform": platform.platform()},
            "n_params": self.agent.P, "n_params_decayed": self.agent.Pd,
            "layers": [[n, b - a] for n, a, b in self.agent.layers],
            "childhood": self.childhood, "life_steps": self.life_steps, "ticks_total": self.ca,
            "n_evals": n_e, "n_episodes": len(self.episodes), "n_segments": len(self.segs),
            "eval_kinds": EVAL_KINDS, "seg_kinds": SEG_KINDS, "disp_fields": DISP_FIELDS,
            "timing_s": {**{k: round(v, 2) for k, v in self.timer.t.items()}, "wall": round(wall, 2)},
            "peak_rss_mb": round(_peak_rss_mb(), 1), "sha256_arrays": hashes,
        }
        (out / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
        return meta

    def run(self):
        t0 = time.perf_counter()
        self.childhood_phase()
        self.life_phase()
        return self.save(time.perf_counter() - t0)


def run_one(config_path, family, seed, out_dir, overrides=()):
    cfg, sha = load_config(config_path, overrides)
    return Runner(cfg, family, seed, out_dir, sha).run()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--family", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--config", default=str(HERE / "config_stage0.yaml"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--set", action="append", default=[], help="override, e.g. run.childhood_steps=256")
    a = ap.parse_args(argv)
    out = a.out or str(HERE / "runs" / f"{a.family}_s{a.seed}")
    meta = run_one(a.config, a.family, a.seed, out, a.set)
    print(json.dumps({k: meta[k] for k in ["family", "seed", "n_params", "childhood", "n_evals", "n_episodes",
                                           "timing_s", "peak_rss_mb"]}, indent=1))


if __name__ == "__main__":
    main()
