# POST HOC test (b), 9 Nov 2026, after the final review round: T-A retention on the 16 facts per task held in memory.
# Reads runs/ta_memory_facts_posthoc.npz (written by lm/ta_memory_facts_posthoc.py from the stored final LoRA factors).
# Per clock: final recall of the memory facts of tasks 0-8 and of the other facts of those tasks (the latter from the
# stored per-task accuracy minus the memory facts recalled); per task, the memory recall averaged over seeds; paired by
# seed, tau minus each other clock on memory recall, with a t interval of 95% (descriptive; no margin was fixed for it).
# Writes runs/ta_memory_posthoc.json. Run from Stadiul0: python -I ta_memory_posthoc.py
import json, sys
from pathlib import Path
import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
z = np.load(S / "runs" / "ta_memory_facts_posthoc.npz")
C, M, A, clocks, seeds = z["correct"], z["memory"], z["acc_stored"], list(z["clocks"]), list(z["seeds"])
for ci in range(len(clocks)):
    for si in range(len(seeds)):
        assert (C[ci, si][M[si]] >= 0).all(), f"missing: {clocks[ci]} {seeds[si]}"
v = np.isfinite(z["acc_cpu"][:, :, 0])
for ci, si in zip(*v.nonzero()):
    d = np.round(np.abs(z["acc_cpu"][ci, si] - A[ci, si]) * 512).astype(int)
    print(f"validation run {clocks[ci]} s{seeds[si]}: all 5120 facts recomputed on the CPU; "
          f"|recomputed - stored| correct facts per task: {d.tolist()}")
mem_t = np.zeros((len(clocks), len(seeds), 9)); oth_t = mem_t.copy()
for ci in range(len(clocks)):
    for si in range(len(seeds)):
        for t in range(9):
            m = M[si, t * 512:(t + 1) * 512]; c = C[ci, si, t * 512:(t + 1) * 512]
            k = int((c[m] == 1).sum()); n = int(m.sum())
            mem_t[ci, si, t] = k / n
            oth_t[ci, si, t] = (round(A[ci, si, t] * 512) - k) / (512 - n)
mem, oth = mem_t.mean(2), oth_t.mean(2)
out = {"seeds": [int(s) for s in seeds], "per_clock": {}, "tau_minus": {}}
print(f"\nmemory: {int(M[0, :4608].sum() // 9)} facts per task, tasks 0-8; seeds {[int(s) for s in seeds]}")
for ci, c in enumerate(clocks):
    out["per_clock"][c] = {"memory_recall": float(mem[ci].mean()), "other_recall": float(oth[ci].mean()),
                           "memory_recall_by_task": [round(float(x), 4) for x in mem_t[ci].mean(0)]}
    print(f"  {c:6s} final recall: memory facts {mem[ci].mean():.4f}, other facts of tasks 0-8 {oth[ci].mean():.4f}; "
          f"memory recall by task 0-8: {[round(float(x), 3) for x in mem_t[ci].mean(0)]}")
for ci, c in enumerate(clocks[1:], 1):
    d = mem[0] - mem[ci]; n = len(d)
    h = stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n)
    out["tau_minus"][c] = {"mean": float(d.mean()), "ci95": [float(d.mean() - h), float(d.mean() + h)]}
    print(f"tau - {c}: memory recall {d.mean():+.4f}, paired 95% CI [{d.mean() - h:+.4f}; {d.mean() + h:+.4f}]")
(S / "runs" / "ta_memory_posthoc.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
