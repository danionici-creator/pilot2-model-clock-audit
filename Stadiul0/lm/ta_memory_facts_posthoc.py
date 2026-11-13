"""POST HOC test (b), 9 Nov 2026, after the final review round: T-A retention on the facts held in memory. CPU only.

T-A stored only the per-task accuracy (evals.npz), not which facts were recalled. Each run also stored its final LoRA
factors (final_factors.npy, hash in meta.json), and the world and the memory buffer are fixed by the seed
(lm_forever_run.py: make_world with generator seed*10+2; memory = 16 facts per task from randperm with generator
seed*10+4). This script rebuilds both on the CPU, loads the final factors into Qwen3-0.6B (bf16 weights, fp32 LoRA,
bf16 autocast, as the T-A runs on the GPU), and records for every fact whether the final model recalls it
(argmax over the vocabulary = answer word, as lm_forever_run.evaluate). Validation: the per-task accuracies recomputed
here are compared with the stored final row of evals.npz (the GPU and the CPU kernels differ, so a few borderline facts
may flip; the number is reported).
Output: runs/ta_memory_facts_posthoc.npz (correct[clock, seed, fact], memory[seed, fact], stored and recomputed
per-task accuracies). Read by Stadiul0/ta_memory_posthoc.py.
    python -I lm/ta_memory_facts_posthoc.py [clock seed]   (from Stadiul0; default: all 4 clocks x 5 seeds)
"""
import hashlib, json, math, sys, time
from pathlib import Path
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent.parent
TA = S / "runs" / "ta"
MODEL_DIR = r"D:\Time\_modele\Qwen_Qwen3-0.6B"
CLOCKS = ["tau", "eta_m", "eta", "steps"]
SEEDS = [7301, 7302, 7303, 7304, 7305]
sys.path.insert(0, str(S / "lm"))
import lm_forever_run as L                                  # WORDS, LETTERS, the LoRA module (unchanged)


def world(tok, seed, n_tasks, per_task, n_probe):
    """lm_forever_run.make_world without the .cuda() calls."""
    words = [w for w in L.WORDS if len(tok(" " + w, add_special_tokens=False).input_ids) == 1]
    wid = torch.tensor([tok(" " + w, add_special_tokens=False).input_ids[0] for w in words])
    g = torch.Generator().manual_seed(seed * 10 + 2)
    codes, seen = [], set()
    while len(codes) < n_tasks * per_task + n_probe:
        c = "".join(L.LETTERS[j] for j in torch.randint(len(L.LETTERS), (6,), generator=g).tolist())
        if c not in seen:
            seen.add(c); codes.append(c[:3] + "-" + c[3:])
    ans = torch.randint(len(words), (len(codes),), generator=g)
    ids = [tok(f"code {c} is", add_special_tokens=False).input_ids for c in codes]
    Lm = max(map(len, ids)); pad = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    x = torch.full((len(ids), Lm), pad); att = torch.zeros((len(ids), Lm), dtype=torch.long)
    for i, s in enumerate(ids):
        x[i, Lm - len(s):] = torch.tensor(s); att[i, Lm - len(s):] = 1
    pos = (att.cumsum(1) - 1).clamp(min=0)
    return x, att, pos, wid[ans]


def memory(seed, n_tasks, per_task, mem):
    g = torch.Generator().manual_seed(seed * 10 + 4); m = np.zeros(n_tasks * per_task, bool)
    for t in range(n_tasks):                                 # one randperm per task end, as Run.task
        keep = torch.arange(t * per_task, (t + 1) * per_task)[torch.randperm(per_task, generator=g)[:mem]]
        if t < n_tasks - 1:                                  # the last task's draw is never replayed
            m[keep.numpy()] = True
    return m


def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.manual_seed(0)
    todo = [(sys.argv[1], int(sys.argv[2]))] if len(sys.argv) == 3 else [(c, s) for c in CLOCKS for s in SEEDS]
    tok = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, local_files_only=True, dtype=torch.bfloat16)
    for p in model.parameters():
        p.requires_grad_(False)
    gen = torch.Generator().manual_seed(0)
    loras = []
    for layer in model.model.layers:
        for nm in ["q_proj", "v_proj"]:
            m = L.LoRA(getattr(layer.self_attn, nm), 8, 16.0, 0.05, gen)
            setattr(layer.self_attn, nm, m); loras.append(m)
    model.eval()
    out = S / "runs" / "ta_memory_facts_posthoc.npz"
    prev = dict(np.load(out, allow_pickle=False)) if out.exists() else {}
    correct = np.full((len(CLOCKS), len(SEEDS), 5120), -1, np.int8)
    mem = np.zeros((len(SEEDS), 5120), bool); acc_st = np.full((len(CLOCKS), len(SEEDS), 10), np.nan)
    acc_cpu = acc_st.copy()
    if prev:
        correct, mem, acc_st, acc_cpu = prev["correct"], prev["memory"], prev["acc_stored"], prev["acc_cpu"]
    for clock, seed in todo:
        if prev and len(todo) > 1 and (correct[CLOCKS.index(clock), SEEDS.index(seed)] >= 0).any():
            continue                                         # already computed
        t0 = time.time(); rd = TA / clock / f"s{seed}"
        meta = json.load(open(rd / "meta.json")); cfg = meta["config"]
        assert cfg["precision"] == "bf16" and cfg["clock"] == clock and cfg["per_task"] == 512 and cfg["mem_per_task"] == 16
        f = np.load(rd / "final_factors.npy")
        assert hashlib.sha256(f.tobytes()).hexdigest() == meta["sha256_final_factors"]
        o = 0
        for lo in loras:                                     # Run.flat(): A then B for each module, layer order
            for p in (lo.A, lo.B):
                n = p.numel(); p.data.copy_(torch.from_numpy(f[o:o + n]).view_as(p)); o += n
        assert o == f.size
        x, att, pos, y = world(tok, seed, 10, 512, 128)
        ci, si = CLOCKS.index(clock), SEEDS.index(seed)
        mem[si] = memory(seed, 10, 512, 16)
        full = (clock, seed) == ("tau", 7301)                # the validation run: all 5120 facts; the others: memory only
        idx = np.arange(5120) if full else np.flatnonzero(mem[si])
        hit = np.full(5120, -1, np.int8)
        with torch.no_grad(), torch.autocast("cpu", dtype=torch.bfloat16):
            for i in range(0, len(idx), 128):
                j = torch.from_numpy(idx[i:i+128])
                lg = model(input_ids=x[j], attention_mask=att[j], position_ids=pos[j], logits_to_keep=1).logits[:, -1, :]
                hit[idx[i:i+128]] = (lg.argmax(-1) == y[j]).numpy()
        correct[ci, si] = hit
        acc_st[ci, si] = np.load(rd / "evals.npz")["acc"][-1]
        msg = ""
        if full:
            acc_cpu[ci, si] = hit.reshape(10, 512).mean(1)
            flips = np.abs(acc_cpu[ci, si] - acc_st[ci, si]) * 512
            msg = (f"; validation, |recomputed - stored| correct facts per task: {flips.round().astype(int).tolist()}; "
                   f"other facts of tasks 0-8 {hit[:4608][~mem[si][:4608]].mean():.3f}")
        print(f"{clock:6s} s{seed}: {time.time() - t0:.0f} s; memory facts recalled {hit[mem[si]].mean():.3f}{msg}", flush=True)
        np.savez_compressed(out, correct=correct, memory=mem, acc_stored=acc_st, acc_cpu=acc_cpu,
                            clocks=np.array(CLOCKS), seeds=np.array(SEEDS))


if __name__ == "__main__":
    main()
