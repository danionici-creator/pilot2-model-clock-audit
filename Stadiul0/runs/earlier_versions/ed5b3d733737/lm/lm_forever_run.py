"""Pilot 2, LM arm, technical run: the FOREVER clock in the FOREVER schedule (6 Nov 2026).

    D:\\Time\\_venv_cuda\\Scripts\\python.exe -I lm_forever_run.py --seed 7101 --out ..\\runs\\lmtech1\\s7101 [--tasks 10]

Copies the training schedule of FOREVER (arXiv:2601.03938; code github.com/WoodScene/FOREVER, commit bbeb549,
src/finetune_cl_our_qwen.py) on Qwen3-0.6B, with synthetic facts instead of SuperNI:
  * LoRA r=8, alpha=16 (scale 2), dropout 0.05, on q_proj and v_proj only; PEFT-style init (A ~ U(+-1/sqrt(in)), B = 0);
    base weights fp16, LoRA factors fp32, fp16 autocast with a GradScaler (init 65536), as Trainer(fp16=True).
  * Every phase is a new Trainer: AdamW (0.9, 0.999, eps 1e-8, weight decay 0), clip 1.0, lr 3e-4, HF linear schedule
    with warmup (first step at lr 0), a fresh optimizer, a fresh scheduler and a fresh GradScaler.
  * Per task: tau starts at 0. Calibration phase = first 24 steps (warmup 10, max_steps 24); model_day = tau after it;
    thresholds d*model_day, d in {1,2,4,7,15,30,60,90,120}. Current phase: warmup 10, max_steps = remaining task steps,
    stopped as soon as tau >= next threshold. Replay phase (tasks >= 1): warmup 5, 2 epochs over the memory buffer,
    loss + 0.001*beta_t*sum((theta - theta_star)^2), theta_star = factors at task start, beta_t = clip(mu/mu0, 0.5, 3),
    mu = EMA(0.05) of Delta_t, mu0 = tau_calib/24. Replay steps are not counted in tau; the reference point moves after a
    replay. A final replay at the end of every task >= 1. Task 0: 60 epochs, no replay; tasks >= 1: 10 epochs.
Declared deviations: one batch of 32 instead of 4 x 8 accumulation; loss on the single answer token; the memory buffer is
16 fixed facts per previous task (the meaning of memory_data_ratio=2 is not checkable: utils/load_data.py is missing at
that commit); replay steps per epoch = ceil(M/32); the task's batches form one stream across its phases (a new
Trainer would restart its dataloader at every phase).

Telemetry per optimizer step (all phases): phase kind, step in phase, lr, loss, grad norm before / after clipping, GradScaler
skip, |m_hat|, sqrt(Tr v_hat), Delta_t on the factors (tau increment), Delta_t on dW = scale*B*A (Gram identity, exact),
mu, beta. Probe outputs (128 never-trained prompts, log-softmax over the 32 answer words) every 8 counted steps, for a
functional distance. Accuracy on the tasks seen so far at every task end goes to evals.npz (not read by the G2 analysis).
Deterministic: CUBLAS_WORKSPACE_CONFIG, torch.use_deterministic_algorithms(True), seeded generators. Keeps Windows awake
while it runs (SetThreadExecutionState), without changing any power setting.
"""
import os
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
import argparse, ctypes, hashlib, json, math, platform, sys, time
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

MODEL_DIR = r"D:\Time\_modele\Qwen_Qwen3-0.6B"
MODEL_SHA256 = "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"   # modele_provenienta.md
WORDS = ["apple", "river", "stone", "cloud", "tiger", "piano", "candle", "forest", "silver", "rocket", "garden",
         "mirror", "pepper", "violet", "harbor", "lemon", "castle", "dragon", "falcon", "marble", "orange", "pencil",
         "rabbit", "saddle", "tunnel", "velvet", "window", "anchor", "basket", "copper", "desert", "engine"]
LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"
KINDS = ["calib", "current", "replay", "final_replay"]
AMP = torch.float16                      # --precision bf16 (sensitivity, not FOREVER): bf16 weights and autocast, no GradScaler

def keep_awake(on=True):
    if platform.system() == "Windows":
        ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | (ES_SYSTEM_REQUIRED if on else 0))

class LoRA(nn.Module):
    def __init__(self, base, r, alpha, dropout, gen):
        super().__init__()
        self.base, self.scale = base, alpha / r
        dev = base.weight.device
        bound = 1.0 / math.sqrt(base.in_features)
        self.A = nn.Parameter((torch.rand(r, base.in_features, generator=gen) * 2 - 1).mul_(bound).to(dev))
        self.B = nn.Parameter(torch.zeros(base.out_features, r, device=dev))
        self.drop = nn.Dropout(dropout)
    def forward(self, x):
        return self.base(x) + F.linear(F.linear(self.drop(x), self.A), self.B) * self.scale

def build_model(seed, args):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, local_files_only=True, dtype=AMP,
                                                 attn_implementation=args.attn).to("cuda")
    for p in model.parameters():
        p.requires_grad_(False)
    gen = torch.Generator().manual_seed(seed * 10 + 1)
    loras = []
    for layer in model.model.layers:
        for nm in ["q_proj", "v_proj"]:
            m = LoRA(getattr(layer.self_attn, nm), args.r, args.alpha, args.dropout, gen)
            setattr(layer.self_attn, nm, m); loras.append(m)
    return tok, model, loras

def make_world(tok, seed, n_tasks, per_task, n_probe):
    words = [w for w in WORDS if len(tok(" " + w, add_special_tokens=False).input_ids) == 1]
    wid = torch.tensor([tok(" " + w, add_special_tokens=False).input_ids[0] for w in words])
    g = torch.Generator().manual_seed(seed * 10 + 2)
    codes, seen = [], set()
    while len(codes) < n_tasks * per_task + n_probe:
        c = "".join(LETTERS[j] for j in torch.randint(len(LETTERS), (6,), generator=g).tolist())
        if c not in seen:
            seen.add(c); codes.append(c[:3] + "-" + c[3:])
    ans = torch.randint(len(words), (len(codes),), generator=g)
    ids = [tok(f"code {c} is", add_special_tokens=False).input_ids for c in codes]
    L = max(map(len, ids)); pad = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    x = torch.full((len(ids), L), pad); att = torch.zeros((len(ids), L), dtype=torch.long)
    for i, s in enumerate(ids):                      # left padding, as FOREVER (padding_side = "left")
        x[i, L - len(s):] = torch.tensor(s); att[i, L - len(s):] = 1
    pos = (att.cumsum(1) - 1).clamp(min=0)
    tasks = [torch.arange(t * per_task, (t + 1) * per_task) for t in range(n_tasks)]
    probe = torch.arange(n_tasks * per_task, n_tasks * per_task + n_probe)
    return dict(x=x.cuda(), att=att.cuda(), pos=pos.cuda(), y=wid[ans].cuda(), ans=ans.cuda(), wid=wid.cuda(),
                tasks=tasks, probe=probe, words=words, codes=codes)

def logits_at_answer(model, W, idx):
    out = model(input_ids=W["x"][idx], attention_mask=W["att"][idx], position_ids=W["pos"][idx], logits_to_keep=1)
    return out.logits[:, -1, :]

class Run:
    def __init__(self, args):
        self.a = args
        torch.manual_seed(args.seed); np.random.seed(args.seed)
        self.tok, self.model, self.loras = build_model(args.seed, args)
        self.W = make_world(self.tok, args.seed, args.tasks, args.per_task, args.n_probe)
        self.params = [p for m in self.loras for p in (m.A, m.B)]
        self.data_gen = torch.Generator().manual_seed(args.seed * 10 + 3)
        self.mem_gen = torch.Generator().manual_seed(args.seed * 10 + 4)
        self.rows, self.probe_rows, self.evals, self.phases = [], [], [], []
        self.pre_final = []                                   # (task, accuracy before the final replay), diagnostic
        self.gstep = 0
        self.prev = self.flat().clone()                       # reference point for Delta_t
        self.prevAB = [(m.A.detach().clone(), m.B.detach().clone()) for m in self.loras]
        self.memory = torch.empty(0, dtype=torch.long)

    def flat(self):
        return torch.cat([p.detach().reshape(-1) for p in self.params])

    def dW_delta(self):
        s2 = []
        for m, (A0, B0) in zip(self.loras, self.prevAB):   # |B A - B0 A0|_F^2 = sum((Bc^T Bc) * (Ac Ac^T)), rank 2r
            Bc = torch.cat([m.B.detach(), -B0], 1); Ac = torch.cat([m.A.detach(), A0], 0)
            s2.append(((Bc.t() @ Bc) * (Ac @ Ac.t())).sum())
        return self.loras[0].scale * math.sqrt(max(float(torch.stack(s2).sum()), 0.0))

    def move_reference(self):
        self.prev = self.flat().clone()
        self.prevAB = [(m.A.detach().clone(), m.B.detach().clone()) for m in self.loras]

    def batches(self, idx, epochs):
        for _ in range(epochs):
            perm = idx[torch.randperm(len(idx), generator=self.data_gen)]
            for i in range(0, len(perm), self.a.batch):
                yield perm[i:i + self.a.batch]

    def probe(self, task, tau):
        self.model.eval()
        with torch.no_grad(), torch.autocast("cuda", dtype=AMP):
            lg = logits_at_answer(self.model, self.W, self.W["probe"].cuda()).float()
        self.model.train()
        lp = torch.log_softmax(lg[:, self.W["wid"]], -1)
        self.probe_rows.append((self.gstep, task, tau, lp.cpu().numpy().astype(np.float32)))

    def evaluate(self, task):
        self.model.eval(); acc = []
        with torch.no_grad(), torch.autocast("cuda", dtype=AMP):
            for t in range(task + 1):
                idx = self.W["tasks"][t].cuda(); hit = 0
                for i in range(0, len(idx), 128):
                    hit += int((logits_at_answer(self.model, self.W, idx[i:i+128]).argmax(-1) == self.W["y"][idx[i:i+128]]).sum())
                acc.append(hit / len(idx))
        self.model.train()
        self.evals.append((task, self.gstep, acc))
        return acc

    def acc_current(self, task):
        """Diagnostic only (--diag_pre_final): accuracy on the current task, logged nowhere else; no RNG, no grad."""
        self.model.eval(); idx = self.W["tasks"][task].cuda(); hit = 0
        with torch.no_grad(), torch.autocast("cuda", dtype=AMP):
            for i in range(0, len(idx), 128):
                hit += int((logits_at_answer(self.model, self.W, idx[i:i+128]).argmax(-1) == self.W["y"][idx[i:i+128]]).sum())
        self.model.train()
        return hit / len(idx)

    def phase(self, kind, task, data, max_steps, warmup, stop_tau=None, beta=None, theta_star=None, counted=True):
        a = self.a
        opt = torch.optim.AdamW(self.params, lr=a.lr, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0)
        lam = lambda s: s / max(1, warmup) if s < warmup else max(0.0, (max_steps - s) / max(1.0, max_steps - warmup))
        sched = torch.optim.lr_scheduler.LambdaLR(opt, lam)
        scaler = torch.amp.GradScaler("cuda", init_scale=65536.0, enabled=(AMP == torch.float16))
        start, n = self.gstep, 0
        while n < max_steps:
            idx = next(data).cuda(); lr = opt.param_groups[0]["lr"]
            with torch.autocast("cuda", dtype=AMP):
                loss = F.cross_entropy(logits_at_answer(self.model, self.W, idx).float(), self.W["y"][idx])
            total = loss
            if theta_star is not None:
                reg = sum(((p - q) ** 2).sum() for p, q in zip(self.params, theta_star))
                total = loss + 0.001 * beta * reg
            scaler.scale(total).backward()
            scaler.unscale_(opt)
            gn = float(torch.nn.utils.clip_grad_norm_(self.params, 1.0))
            gn_after = float(torch.sqrt(sum((p.grad.float() ** 2).sum() for p in self.params)))
            s0 = scaler.get_scale(); scaler.step(opt); scaler.update(); skipped = scaler.get_scale() < s0
            if not skipped:
                sched.step()
            opt.zero_grad(set_to_none=True)
            st = [opt.state[p] for p in self.params if p in opt.state and "exp_avg" in opt.state[p]]
            if st:
                k = float(st[0]["step"])                         # same step count for every parameter
                mv = torch.stack([torch.stack([(s_["exp_avg"] ** 2).sum(), s_["exp_avg_sq"].sum()]) for s_ in st]).sum(0)
                m2, v1 = (mv / torch.tensor([(1 - 0.9 ** k) ** 2, 1 - 0.999 ** k], device=mv.device)).tolist()
            else:
                m2 = v1 = 0.0
            cur = self.flat(); d = float(torch.linalg.vector_norm(cur - self.prev)); dw = self.dW_delta()
            self.prev = cur.clone(); self.prevAB = [(m.A.detach().clone(), m.B.detach().clone()) for m in self.loras]
            if counted:
                self.tau += d
                if self.mu0 is not None:
                    self.mu = (1 - 0.05) * self.mu + 0.05 * d
            self.gstep += 1; n += 1
            self.rows.append((self.gstep, task, KINDS.index(kind), len(self.phases), n, lr, float(loss.detach()), gn, gn_after,
                              int(skipped), math.sqrt(m2), math.sqrt(v1), d, dw, int(counted), self.tau,
                              self.mu if self.mu is not None else np.nan, beta if beta is not None else np.nan))
            if not math.isfinite(float(loss)):
                raise RuntimeError(f"non-finite loss at step {self.gstep}")
            if counted:
                self.counted += 1
                if self.counted % a.probe_every == 0:
                    self.probe(task, self.tau)
                if stop_tau is not None and self.tau >= stop_tau:
                    break
        self.phases.append((task, KINDS.index(kind), start, self.gstep, max_steps, warmup))
        return n

    def replay_phase(self, kind, task, theta_star):
        ratio = self.mu / (self.mu0 + 1e-12)
        beta = min(3.0, max(0.5, 1.0 + (ratio - 1.0)))
        M = len(self.memory); steps = 2 * max(1, math.ceil(M / self.a.batch))
        self.phase(kind, task, self.batches(self.memory, 2), steps, 5, beta=beta, theta_star=theta_star, counted=False)
        self.move_reference()

    def task(self, t):
        a = self.a
        epochs = a.first_epochs if t == 0 else a.epochs
        idx = self.W["tasks"][t]
        total = math.ceil(len(idx) / a.batch * epochs)
        data = self.batches(idx, epochs)
        self.tau, self.mu, self.mu0, self.counted = 0.0, None, None, 0
        theta_star = [p.detach().clone() for p in self.params]
        have_mem = len(self.memory) > 0
        self.probe(t, 0.0)                                  # functional reference at task start
        done = self.phase("calib", t, data, min(24, total), 10)
        model_day = max(self.tau, 1e-8); thr = [d * model_day for d in (1, 2, 4, 7, 15, 30, 60, 90, 120)]; nxt = 0
        self.mu0 = self.tau / done; self.mu = self.mu0
        while done < total:
            if have_mem and nxt < len(thr) and self.tau >= thr[nxt]:
                self.replay_phase("replay", t, theta_star); nxt += 1
                continue
            stop = thr[nxt] if (have_mem and nxt < len(thr)) else None
            done += self.phase("current", t, data, total - done, 10, stop_tau=stop)
        if have_mem:
            if a.diag_pre_final:
                self.pre_final.append((t, self.acc_current(t)))
            self.replay_phase("final_replay", t, theta_star)
        acc = self.evaluate(t)
        keep = idx[torch.randperm(len(idx), generator=self.mem_gen)[:a.mem_per_task]]
        self.memory = torch.cat([self.memory, keep])
        return total, model_day, acc

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--tasks", type=int, default=10); ap.add_argument("--per_task", type=int, default=512)
    ap.add_argument("--epochs", type=int, default=10); ap.add_argument("--first_epochs", type=int, default=60)
    ap.add_argument("--batch", type=int, default=32); ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--r", type=int, default=8); ap.add_argument("--alpha", type=float, default=16.0)
    ap.add_argument("--dropout", type=float, default=0.05); ap.add_argument("--mem_per_task", type=int, default=16)
    ap.add_argument("--n_probe", type=int, default=128); ap.add_argument("--probe_every", type=int, default=8)
    ap.add_argument("--attn", default="sdpa")
    ap.add_argument("--precision", default="fp16", choices=["fp16", "bf16"])
    ap.add_argument("--diag_pre_final", action="store_true",
                    help="diagnostic: current-task accuracy just before the final replay (training unchanged)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if os.path.exists(os.path.join(a.out, "meta.json")):
        print("complete run found, skipping:", a.out); return
    global AMP
    AMP = torch.float16 if a.precision == "fp16" else torch.bfloat16
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False
    torch.backends.cuda.matmul.allow_tf32 = False
    keep_awake(True)
    t0 = time.time()
    run = Run(a)
    cfg = vars(a).copy(); cfg.pop("out")
    log = open(os.path.join(a.out, "run.log"), "a", encoding="utf-8")
    def say(s):
        print(s, flush=True); log.write(s + "\n"); log.flush()
    say(f"seed {a.seed}; trainable {sum(p.numel() for p in run.params)}; words {len(run.W['words'])}; config {json.dumps(cfg)}")
    for t in range(a.tasks):
        tt = time.time()
        total, day, acc = run.task(t)
        nph = sum(1 for p in run.phases if p[0] == t)
        say(f"task {t}: {total} steps, model_day {day:.4f}, tau {run.tau:.3f}, phases {nph}, step {run.gstep}, "
            f"acc_new {acc[-1]:.3f}, {time.time() - tt:.0f}s, max VRAM {torch.cuda.max_memory_allocated() / 2**20:.0f} MiB")
    cols = ["gstep", "task", "kind", "phase", "step_in_phase", "lr", "loss", "gnorm", "gnorm_clipped", "skipped",
            "m_hat_norm", "sqrt_trv", "delta", "delta_dW", "counted", "tau", "mu", "beta"]
    steps = np.array(run.rows, dtype=np.float64)
    np.savez_compressed(os.path.join(a.out, "steps.npz"), cols=np.array(cols), data=steps,
                        phases=np.array(run.phases, dtype=np.int64))
    np.savez_compressed(os.path.join(a.out, "probes.npz"), gstep=np.array([r[0] for r in run.probe_rows]),
                        task=np.array([r[1] for r in run.probe_rows]), tau=np.array([r[2] for r in run.probe_rows]),
                        logp=np.stack([r[3] for r in run.probe_rows]))
    np.savez_compressed(os.path.join(a.out, "evals.npz"), task=np.array([e[0] for e in run.evals]),
                        gstep=np.array([e[1] for e in run.evals]),
                        acc=np.array([e[2] + [np.nan] * (a.tasks - len(e[2])) for e in run.evals]))
    final = run.flat().cpu().numpy().astype(np.float32)
    np.save(os.path.join(a.out, "final_factors.npy"), final)
    h = lambda f: hashlib.sha256(open(os.path.join(a.out, f), "rb").read()).hexdigest()
    meta = dict(config=cfg, config_sha256=hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest(),
                model_dir=MODEL_DIR, model_sha256=MODEL_SHA256, torch=torch.__version__, cuda=torch.version.cuda,
                device=torch.cuda.get_device_name(0), python=sys.version.split()[0],
                transformers=__import__("transformers").__version__, wall_s=time.time() - t0, steps=run.gstep,
                sha256_steps_data=hashlib.sha256(steps.tobytes()).hexdigest(),
                sha256_final_factors=hashlib.sha256(final.tobytes()).hexdigest(),
                files={f: h(f) for f in ["steps.npz", "probes.npz", "evals.npz", "final_factors.npy"]},
                script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
                diag_pre_final=[[t, acc] for t, acc in run.pre_final])
    json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1)
    say(f"done: {run.gstep} steps, {time.time() - t0:.0f}s; steps sha256 {meta['sha256_steps_data'][:16]}; "
        f"factors sha256 {meta['sha256_final_factors'][:16]}")
    keep_awake(False)

if __name__ == "__main__":
    main()
