"""Automated checks for the Stage 0 code (run from the Stadiul0 folder: python checks_stage0.py).

1. World: vocabulary partition, disjointness of R, B_beh and probes, probe halves (gate G4, structural).
2. Schedules: every family sums to the life length, segments on the 64-step quantum.
3. Optimizer: the explicit AdamW step equals torch.optim.AdamW (with clipping and parameter groups).
3b. Deep Review corrections (6 Nov 2026): max_ctx = input width; embeddings out of weight decay; C10c, L_clip, q_hist.
4. Identity: a same-step D2 equals lr * ||m_hat|| up to epsilon (section 5.1).
5. Determinism: two short runs with the same seed give bit-identical arrays (gate G7).
"""
import os

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import copy
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from p2.agent import FlatAgent                      # noqa: E402
from p2.run import load_config, run_one              # noqa: E402
from p2.streams import build_schedule                # noqa: E402
from p2.world import World                           # noqa: E402

CFG_PATH = HERE / "config_stage0.yaml"
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{(': ' + detail) if detail else ''}")


def main():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    cfg, _ = load_config(CFG_PATH)

    # 1. world
    for fam in ["F1", "F5"]:
        f = cfg["families"][fam]
        w = World(cfg["world"], np.random.default_rng(7), f["rule_frac"], f["pi_overlap"])   # asserts inside
        n_rule = sum(t.kind == "rule" for t in w.targets)
        check(f"world {fam}: partition and disjointness", True,
              f"{len(w.targets)} target tasks ({n_rule} rule), |R| = {len(w.R_x)}, |B_beh| = {len(w.B_x)}")
        ov = w.key_overlap()
        facts = [i for i, t in enumerate(w.targets) if t.kind == "fact"]
        mean_ov = ov[np.ix_(facts, facts)][~np.eye(len(facts), dtype=bool)].mean()
        check(f"world {fam}: fact-task pair overlap is positive", mean_ov > 0, f"mean pairwise {mean_ov:.4f}")

    # 2. schedules
    r = cfg["run"]
    for fam_name, fam in cfg["families"].items():
        segs, lr, restarts = build_schedule(fam, cfg["world"]["n_target"], r["life_steps_per_task"], r["q0"],
                                            cfg["optim"]["lr"], np.random.default_rng(3))
        kinds = {k: sum(s.kind == k for s in segs) for k in ["new", "reexp", "reh", "distractor", "idle"]}
        ok = (len(lr) == cfg["world"]["n_target"] * r["life_steps_per_task"]
              and all(s.steps % 64 == 0 and s.ticks % 64 == 0 for s in segs)
              and kinds["new"] == cfg["world"]["n_target"])
        check(f"schedule {fam_name}", ok, f"{len(lr)} steps, {kinds}, lr [{lr.min():.2e}, {lr.max():.2e}], "
                                          f"{len(restarts)} restart(s)")

    # 3. explicit AdamW == torch.optim.AdamW
    torch.manual_seed(0)
    a = FlatAgent(cfg["agent"], cfg["optim"])
    ref = copy.deepcopy(a.model)
    o = cfg["optim"]
    dec = set(a.decayed_names)                     # matrices under weight decay (embeddings out if wd_embeddings false)
    groups = [{"params": [p for n, p in ref.named_parameters() if n in dec], "weight_decay": o["weight_decay"]},
              {"params": [p for n, p in ref.named_parameters() if n not in dec], "weight_decay": 0.0}]
    opt = torch.optim.AdamW(groups, lr=o["lr"], betas=tuple(o["betas"]), eps=o["eps"], foreach=False)
    g = torch.Generator().manual_seed(1)
    max_dev = 0.0
    for s in range(30):
        x = torch.randint(0, 512, (32, 4), generator=g)
        y = torch.randint(0, 512, (32,), generator=g)
        a.step(x, y, o["lr"])
        opt.zero_grad()
        torch.nn.functional.cross_entropy(ref(x), y).backward()
        torch.nn.utils.clip_grad_norm_(ref.parameters(), o["clip"])
        opt.step()
        mine = torch.cat([p.detach().reshape(-1) for _, p in a.order])
        theirs = torch.cat([dict(ref.named_parameters())[n].detach().reshape(-1) for n, _ in a.order])
        max_dev = max(max_dev, (mine - theirs).abs().max().item())
    check("explicit AdamW is bit-identical to torch.optim.AdamW (30 steps)", max_dev == 0.0,
          f"max |diff| = {max_dev:.2e}")

    # 3b. Deep Review corrections (6 Nov 2026): context = input width; embeddings out of weight decay
    w0 = World(cfg["world"], np.random.default_rng(7), 0.0, 0.25)
    width = w0.targets[0].train_x.shape[1]
    check("max_ctx equals the input width (Deep Review D2)", cfg["agent"]["max_ctx"] == width,
          f"max_ctx {cfg['agent']['max_ctx']}, input width {width}")
    torch.manual_seed(5)
    b = FlatAgent(cfg["agent"], cfg["optim"])
    rows0 = b.model.tok.weight[256:].detach().clone()
    g2 = torch.Generator().manual_seed(2)
    for _ in range(20):
        b.step(torch.randint(0, 256, (32, 4), generator=g2), torch.randint(0, 256, (32,), generator=g2), o["lr"])
    unchanged = torch.equal(b.model.tok.weight[256:], rows0)
    want = not o.get("wd_embeddings", True)
    check("unused embedding rows: unchanged iff embeddings are out of weight decay (Deep Review D3)",
          unchanged == want, f"wd_embeddings={o.get('wd_embeddings', True)}, rows unchanged={unchanged}, "
                             f"decayed matrices {len(b.decayed_names)} of {len(b.layers)}")

    # 4. same-step D2 identity: (sum v_hat dpre^2)^(1/2) ~= lr ||m_hat|| (with eps)
    x = torch.randint(0, 512, (32, 4), generator=g)
    y = torch.randint(0, 512, (32,), generator=g)
    m_prev, v_prev, t_prev = a.m.clone(), a.v.clone(), a.t
    flat_prev = a.flat.clone()
    stats, dpre, _ = a.step(x, y, o["lr"], None)
    vh = a.vhat()
    same = torch.sqrt((vh.double() * dpre.double() ** 2).sum()).item()
    lrm = o["lr"] * a.mhat().double().norm().item()
    check("same-step D2 identity (section 5.1)", abs(same - lrm) / lrm < 1e-3, f"{same:.6e} vs {lrm:.6e}")
    del m_prev, v_prev, t_prev, flat_prev

    # 5. determinism (G7): two tiny runs with the same seed
    tiny = ["world.n_target=4", "run.childhood_steps=128", "run.life_steps_per_task=512",
            "run.d3_strides=[[8,0,null],[1,64,192]]", "run.chunked_param_D=true", "run.d2_lag_mode=both"]
    tmp = Path(tempfile.mkdtemp(prefix="p2chk_", dir=str(HERE)))
    try:
        hashes = []
        for fam in ["F4", "F6"]:
            m1 = run_one(CFG_PATH, fam, 11, tmp / f"{fam}_a", tiny)
            m2 = run_one(CFG_PATH, fam, 11, tmp / f"{fam}_b", tiny)
            same = m1["sha256_arrays"] == m2["sha256_arrays"]
            check(f"determinism {fam}: bit-identical reruns", same,
                  f"{m1['n_evals']} evals, {m1['n_episodes']} episodes, wall {m1['timing_s']['wall']} s")
            hashes.append(m1["sha256_arrays"])
            st = np.load(tmp / f"{fam}_a" / "steps.npz")
            ok = np.isfinite(st["D2_exact"][300:]).all() and np.isfinite(st["D2"][300:]).all()
            rel = np.abs(st["D2"] - st["D2_exact"]) / st["D2_exact"]
            check(f"D2 blocked vs exact lag {fam}", ok, f"median rel. diff {np.nanmedian(rel):.2e}, "
                                                       f"max {np.nanmax(rel):.2e}")
            ch = np.load(tmp / f"{fam}_a" / "chunks.npz")
            ev = np.load(tmp / f"{fam}_a" / "evals.npz"); eps = np.load(tmp / f"{fam}_a" / "episodes.npz")
            c10c = ch["m8_s0_C10c"]
            check(f"C10c present, finite and >= C10b {fam} (Deep Review D5)",
                  len(c10c) > 0 and np.isfinite(c10c).all() and np.all(c10c >= ch["m8_s0_C10b"] - 1e-12),
                  f"{len(c10c)} chunks, median C10c / C10b {np.median(c10c / np.maximum(ch['m8_s0_C10b'], 1e-12)):.1f}")
            okc = np.nanmax(ev["LAc"] - ev["LA"]) <= 1e-12 and np.nanmax(ev["LAc"]) <= np.log(64) + 1e-9
            check(f"clipped losses L_A,clip <= L_A and <= ln 64 {fam} (Deep Review A3)", okc,
                  f"max L_A,clip {np.nanmax(ev['LAc']):.3f}")
            ov = eps["overlap"]
            check(f"q_hist before the segment: first exposure has no history {fam} (Deep Review D4)",
                  np.isnan(ov[0]) and np.all((ov[1:] >= 0) & (ov[1:] <= 1)), f"overlap[0] = {ov[0]}, then {np.round(ov[1:4], 3)}")
            d1c, d1 = ch["m1_s64_D1c"], st["D1"][64:192]
            check(f"chunked D1 at m_ch = 1 equals per-step D1 {fam}",
                  np.allclose(d1c, d1, rtol=1e-5), f"max rel {np.max(np.abs(d1c - d1) / d1):.1e}")
        check("different families give different runs", hashes[0] != hashes[1])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    n_fail = sum(not ok for _, ok in results)
    print(f"\n{len(results) - n_fail}/{len(results)} checks passed")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
