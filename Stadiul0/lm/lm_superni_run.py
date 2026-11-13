"""Pilot 2, SuperNI check (7 Nov 2026, colloquium missing control): the FOREVER schedule on natural SuperNI tasks.

    D:\\Time\\_venv_cuda\\Scripts\\python.exe -I lm_superni_run.py --seed 7401 --clock tau --out ..\\runs\\sni\\tau\\s7401

Same schedule as lm_forever_run.py (FOREVER, github.com/WoodScene/FOREVER, commit bbeb549, src/finetune_cl_our_qwen.py and
scripts/run_train_cl_ours_qwen.sh, read 7 Nov 2026): per task a calibration phase of 24 steps (model day), replay thresholds
d * day, d in {1,2,4,7,15,30,60,90,120}, replay = 2 epochs over the memory buffer with loss + 0.001*beta*|theta-theta*|^2,
beta = clip(mu/mu0, 0.5, 3), a final replay at every task end, every phase a fresh AdamW (wd 0) + linear schedule with
warmup (10; 5 for replay); LoRA r 8, alpha 16, dropout 0.05 on q_proj, v_proj; effective batch 32 = micro-batch 4 x 8
accumulation (as their script); max length 512 tokens; loss on the response tokens only (train_on_inputs False), averaged
over the response tokens of the 32 examples; alpaca prompt template (templates/alpaca.json).
Data: D:\\Time\\_date\\FOREVER_bbeb549\\data_superni (order 7 of utils/dataset_order.py), first --tasks tasks.
Declared deviations: bf16 without GradScaler (colloquium decision 6; theirs fp16); epochs --epochs/--first_epochs
(theirs 10/60; reduced for laptop time); no group_by_length; memory = int(2% of the task's training set) per previous task,
class-stratified as their load_memory_buffer when the number of distinct outputs is at most that size, otherwise a random
sample of that size (their code would take one example per distinct output, i.e. almost the whole task for generation
tasks); the task's batches form one stream across its phases; the input text is truncated so that the template and the
response fit in 512 tokens. No probe set (D3 is not computed here). Evaluation (evals.npz): mean response-token loss on
the test set of every seen task at every task end (and, with --diag_pre_final_all, just before each final replay).
"""
import os
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
import argparse, ctypes, hashlib, json, math, platform, sys, time
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

MODEL_DIR = r"D:\Time\_modele\Qwen_Qwen3-0.6B"
MODEL_SHA256 = "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"
DATA = r"D:\Time\_date\FOREVER_bbeb549\data_superni"
ORDER7 = ["task1572", "task363", "task1290", "task181", "task002", "task1510", "task639", "task1729", "task073",
          "task1590", "task748", "task511", "task591", "task1687", "task875"]
HEAD_IN = ("Below is an instruction that describes a task, paired with an input that provides further context. Write a "
           "response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Input:\n")
TAIL = "\n\n### Response:\n"
KINDS = ["calib", "current", "replay", "final_replay"]
AMP = torch.bfloat16

def keep_awake(on=True):
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | (0x00000001 if on else 0))

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
    if args.grad_ckpt:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    return tok, model, loras

def load_tasks(tok, n_tasks, cutoff):
    enc = lambda s: tok(s, add_special_tokens=False).input_ids
    tail = enc(TAIL); eos = tok.eos_token_id
    tasks = []
    for name in ORDER7[:n_tasks]:
        task = {"name": name}
        for sp in ["train", "test"]:
            rows = json.load(open(os.path.join(DATA, sp, name + ".json"), encoding="utf-8"))
            ex = []
            for r in rows:
                h = enc(HEAD_IN.format(instruction=r["instruction"])); i = enc(r["input"])
                o = (enc(str(r["output"])) + [eos])[: cutoff // 2]
                budget = cutoff - len(h) - len(tail) - len(o)
                if budget < 0:
                    h = h[: max(1, len(h) + budget)]; budget = 0
                ex.append((h + i[:budget] + tail, o, str(r["output"])))
            task[sp] = ex
        tasks.append(task)
    return tasks

class Run:
    def __init__(self, args):
        self.a = args
        torch.manual_seed(args.seed); np.random.seed(args.seed)
        self.tok, self.model, self.loras = build_model(args.seed, args)
        self.model.train()                                   # LoRA dropout and gradient checkpointing are active in train mode
        self.pad =self.tok.pad_token_id if self.tok.pad_token_id is not None else self.tok.eos_token_id
        self.T = load_tasks(self.tok, args.tasks, args.cutoff)
        self.params = [p for m in self.loras for p in (m.A, m.B)]
        self.data_gen = torch.Generator().manual_seed(args.seed * 10 + 3)
        self.mem_gen = torch.Generator().manual_seed(args.seed * 10 + 4)
        self.rows, self.evals, self.phases, self.pre_final_all = [], [], [], []
        self.gstep = 0; self.clk = 0.0
        self.prev = self.flat().clone()
        self.memory = []                                     # (task, index in its train set)

    def flat(self):
        return torch.cat([p.detach().reshape(-1) for p in self.params])

    def batches(self, items, epochs):
        for _ in range(epochs):
            perm = torch.randperm(len(items), generator=self.data_gen).tolist()
            for i in range(0, len(perm), self.a.batch):
                yield [items[j] for j in perm[i:i + self.a.batch]]

    def ex(self, it):
        t, j = it
        return self.T[t]["train"][j]

    def loss_sum(self, exs):
        """Sum of the response-token cross-entropies of a micro-batch, and the number of those tokens."""
        L = max(len(p) + len(o) for p, o, _ in exs)
        ids = torch.full((len(exs), L), self.pad, dtype=torch.long); att = torch.zeros((len(exs), L), dtype=torch.long)
        rows, cols, tgt = [], [], []
        for b, (p, o, _) in enumerate(exs):
            seq = p + o; ids[b, :len(seq)] = torch.tensor(seq); att[b, :len(seq)] = 1
            for k in range(len(o)):
                rows.append(b); cols.append(len(p) - 1 + k); tgt.append(o[k])
        with torch.autocast("cuda", dtype=AMP):
            h = self.model.model(input_ids=ids.cuda(), attention_mask=att.cuda()).last_hidden_state
            logits = self.model.lm_head(h[torch.tensor(rows, device="cuda"), torch.tensor(cols, device="cuda")])
        return F.cross_entropy(logits.float(), torch.tensor(tgt, device="cuda"), reduction="sum"), len(tgt)

    def clock_inc(self, d, lr, m2):
        c = self.a.clock
        return d if c == "tau" else lr * math.sqrt(m2) if c == "eta_m" else lr if c == "eta" else 1.0

    def phase(self, kind, task, data, max_steps, warmup, stop_clk=None, beta=None, theta_star=None, counted=True):
        a = self.a
        opt = torch.optim.AdamW(self.params, lr=a.lr, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0)
        lam = lambda s: s / max(1, warmup) if s < warmup else max(0.0, (max_steps - s) / max(1.0, max_steps - warmup))
        sched = torch.optim.lr_scheduler.LambdaLR(opt, lam)
        start, n = self.gstep, 0
        while n < max_steps:
            batch = next(data); lr = opt.param_groups[0]["lr"]
            exs = [self.ex(it) for it in batch]; ntok = sum(len(o) for _, o, _ in exs); lsum = 0.0
            for i in range(0, len(exs), a.micro):
                s, _ = self.loss_sum(exs[i:i + a.micro])
                (s / ntok).backward(); lsum += float(s.detach())
            if theta_star is not None:
                reg = sum(((p - q) ** 2).sum() for p, q in zip(self.params, theta_star))
                (0.001 * beta * reg).backward()
            loss = lsum / ntok
            gn = float(torch.nn.utils.clip_grad_norm_(self.params, 1.0))
            gn_after = float(torch.sqrt(sum((p.grad.float() ** 2).sum() for p in self.params)))
            opt.step(); sched.step(); opt.zero_grad(set_to_none=True)
            st = [opt.state[p] for p in self.params if p in opt.state and "exp_avg" in opt.state[p]]
            k = float(st[0]["step"])
            mv = torch.stack([torch.stack([(s_["exp_avg"] ** 2).sum(), s_["exp_avg_sq"].sum()]) for s_ in st]).sum(0)
            m2, v1 = (mv / torch.tensor([(1 - 0.9 ** k) ** 2, 1 - 0.999 ** k], device=mv.device)).tolist()
            cur = self.flat(); d = float(torch.linalg.vector_norm(cur - self.prev)); self.prev = cur.clone()
            if counted:
                self.tau += d; self.clk += self.clock_inc(d, lr, m2)
                if self.mu0 is not None:
                    self.mu = 0.95 * self.mu + 0.05 * d
            self.gstep += 1; n += 1
            self.rows.append((self.gstep, task, KINDS.index(kind), len(self.phases), n, lr, loss, gn, gn_after, 0,
                              math.sqrt(m2), math.sqrt(v1), d, ntok, int(counted), self.tau,
                              self.mu if self.mu is not None else np.nan, beta if beta is not None else np.nan, self.clk))
            if not math.isfinite(loss):
                raise RuntimeError(f"non-finite loss at step {self.gstep}")
            if counted and stop_clk is not None and self.clk >= stop_clk:
                break
        self.phases.append((task, KINDS.index(kind), start, self.gstep, max_steps, warmup))
        return n

    def replay_phase(self, kind, task, theta_star):
        beta = min(3.0, max(0.5, self.mu / (self.mu0 + 1e-12)))
        M = len(self.memory); steps = 2 * max(1, math.ceil(M / self.a.batch))
        self.phase(kind, task, self.batches(self.memory, 2), steps, 5, beta=beta, theta_star=theta_star, counted=False)
        self.prev = self.flat().clone()

    @torch.no_grad()
    def test_losses(self, upto):
        self.model.eval(); out = []
        for t in range(upto + 1):
            exs = self.T[t]["test"]; s = n = 0.0
            for i in range(0, len(exs), 8):
                ls, k = self.loss_sum(exs[i:i + 8]); s += float(ls); n += k
            out.append(s / n)
        self.model.train()
        return out

    def memory_for(self, t):
        tr = self.T[t]["train"]; n = len(tr); num = max(1, int(n * self.a.mem_ratio / 100))
        labels = [e[2] for e in tr]; classes = sorted(set(labels))
        perm = torch.randperm(n, generator=self.mem_gen).tolist()
        if len(classes) <= num:                               # their class-stratified rule
            per = max(1, num // len(classes)); picked = []
            for c in classes:
                picked += [i for i in perm if labels[i] == c][:per]
            chosen = set(picked); picked += [i for i in perm if i not in chosen][:max(0, num - len(picked))]
        else:                                                 # declared deviation (see docstring)
            picked = perm[:num]
        return [(t, j) for j in picked]

    def task(self, t):
        a = self.a
        epochs = a.first_epochs if t == 0 else a.epochs
        items = [(t, j) for j in range(len(self.T[t]["train"]))]
        total = math.ceil(len(items) / a.batch * epochs)
        data = self.batches(items, epochs)
        self.tau, self.mu, self.mu0, self.clk = 0.0, None, None, 0.0
        theta_star = [p.detach().clone() for p in self.params]
        have_mem = len(self.memory) > 0
        done = self.phase("calib", t, data, min(24, total), 10)
        model_day = max(self.clk, 1e-8); thr = [d * model_day for d in (1, 2, 4, 7, 15, 30, 60, 90, 120)]; nxt = 0
        self.mu0 = self.tau / done; self.mu = self.mu0
        while done < total:
            if have_mem and nxt < len(thr) and self.clk >= thr[nxt]:
                self.replay_phase("replay", t, theta_star); nxt += 1
                continue
            stop = thr[nxt] if (have_mem and nxt < len(thr)) else None
            done += self.phase("current", t, data, total - done, 10, stop_clk=stop)
        if have_mem:
            if a.diag_pre_final_all:
                self.pre_final_all.append((t, self.gstep, self.test_losses(t)))
            self.replay_phase("final_replay", t, theta_star)
        res = self.test_losses(t); self.evals.append((t, self.gstep, res))
        self.memory += self.memory_for(t)
        return total, model_day, res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--tasks", type=int, default=5); ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--first_epochs", type=int, default=10); ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--micro", type=int, default=4); ap.add_argument("--cutoff", type=int, default=512)
    ap.add_argument("--lr", type=float, default=3e-4); ap.add_argument("--r", type=int, default=8)
    ap.add_argument("--alpha", type=float, default=16.0); ap.add_argument("--dropout", type=float, default=0.05)
    ap.add_argument("--mem_ratio", type=float, default=2.0); ap.add_argument("--attn", default="sdpa")
    ap.add_argument("--grad_ckpt", action="store_true"); ap.add_argument("--diag_pre_final_all", action="store_true")
    ap.add_argument("--clock", default="tau", choices=["tau", "eta_m", "eta", "steps"])
    ap.add_argument("--max_tasks_steps", type=int, default=0, help="speed probe only: stop after this many optimizer steps")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if os.path.exists(os.path.join(a.out, "meta.json")):
        print("complete run found, skipping:", a.out); return
    torch.use_deterministic_algorithms(True); torch.backends.cudnn.benchmark = False
    torch.backends.cuda.matmul.allow_tf32 = False
    keep_awake(True); t0 = time.time()
    run = Run(a)
    cfg = vars(a).copy(); cfg.pop("out")
    log = open(os.path.join(a.out, "run.log"), "a", encoding="utf-8")
    def say(s):
        print(s, flush=True); log.write(s + "\n"); log.flush()
    lens = {T["name"]: (len(T["train"]), int(np.median([len(p) + len(o) for p, o, _ in T["train"]]))) for T in run.T}
    say(f"seed {a.seed}; trainable {sum(p.numel() for p in run.params)}; tasks (train n, median tokens) {lens}; config {json.dumps(cfg)}")
    if a.max_tasks_steps:
        items = [(0, j) for j in range(len(run.T[0]["train"]))]; run.tau, run.mu, run.mu0 = 0.0, None, None
        tt = time.time(); run.phase("calib", 0, run.batches(items, 100), a.max_tasks_steps, 10)
        say(f"speed probe: {a.max_tasks_steps} steps in {time.time() - tt:.1f}s; max VRAM {torch.cuda.max_memory_allocated() / 2**20:.0f} MiB")
        return
    for t in range(a.tasks):
        tt = time.time()
        total, day, res = run.task(t)
        say(f"task {t} ({run.T[t]['name']}): {total} steps, model_day {day:.4f}, tau {run.tau:.3f}, step {run.gstep}, "
            f"test losses {[round(x, 3) for x in res]}, {time.time() - tt:.0f}s, max VRAM {torch.cuda.max_memory_allocated() / 2**20:.0f} MiB")
    cols = ["gstep", "task", "kind", "phase", "step_in_phase", "lr", "loss", "gnorm", "gnorm_clipped", "skipped",
            "m_hat_norm", "sqrt_trv", "delta", "ntok", "counted", "tau", "mu", "beta", "clk"]
    steps = np.array(run.rows, dtype=np.float64)
    np.savez_compressed(os.path.join(a.out, "steps.npz"), cols=np.array(cols), data=steps, phases=np.array(run.phases, dtype=np.int64))
    pad = lambda r: r + [np.nan] * (a.tasks - len(r))
    np.savez_compressed(os.path.join(a.out, "evals.npz"), task=np.array([e[0] for e in run.evals]),
                        gstep=np.array([e[1] for e in run.evals]), loss=np.array([pad(e[2]) for e in run.evals]))
    if run.pre_final_all:
        np.savez_compressed(os.path.join(a.out, "evals_pre.npz"), task=np.array([e[0] for e in run.pre_final_all]),
                            gstep=np.array([e[1] for e in run.pre_final_all]), loss=np.array([pad(e[2]) for e in run.pre_final_all]))
    final = run.flat().cpu().numpy().astype(np.float32); np.save(os.path.join(a.out, "final_factors.npy"), final)
    h = lambda f: hashlib.sha256(open(os.path.join(a.out, f), "rb").read()).hexdigest()
    meta = dict(config=cfg, model_sha256=MODEL_SHA256, torch=torch.__version__, cuda=torch.version.cuda,
                device=torch.cuda.get_device_name(0), transformers=__import__("transformers").__version__,
                wall_s=time.time() - t0, steps=run.gstep, memory_size=len(run.memory),
                sha256_steps_data=hashlib.sha256(steps.tobytes()).hexdigest(),
                sha256_final_factors=hashlib.sha256(final.tobytes()).hexdigest(),
                files={f: h(f) for f in ["steps.npz", "evals.npz", "final_factors.npy", "evals_pre.npz"] if os.path.exists(os.path.join(a.out, f))},
                script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest())
    json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1)
    say(f"done: {run.gstep} steps, {time.time() - t0:.0f}s; steps sha256 {meta['sha256_steps_data'][:16]}; "
        f"factors sha256 {meta['sha256_final_factors'][:16]}")
    keep_awake(False)

if __name__ == "__main__":
    main()
