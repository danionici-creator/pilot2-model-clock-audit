# POST HOC, not preregistered. Written on 9 Nov 2026, after the stage 1 verdict, so that the drift ratios quoted in the
# closure report (section 5.1) and in Rezultate_teste_decisive_2026-11-07.md can be recomputed from the archive. The same
# numbers had been computed by hand on 8-9 Nov; this script only fixes the computation in a file. It reads the drift logs
# of the two runs in which the eta*|m_hat| clock drove replay (R2 = ckpt_eta_m, task-0 adapter B; eta_m_A1, adapter A);
# the tau runs do not log the eta clock, so the ratio cannot be computed there.
# For each task with replay (1-3): r = (sum |dtheta| / sum eta-increment over the calibration window, steps 1-24)
#                                    / (the same ratio over the rest of the task, steps 25-313).
# r < 1 means that after calibration |dtheta| grows relative to the eta clock, so the eta clock lags behind tau.
# Usage: python -I drift_ratio_posthoc.py   (prints only; writes nothing)
import csv, sys
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ARMS = {"eta_m (R2, adapter B)": "ckpt_eta_m", "eta_m_A1 (adapter A)": "ckpt_eta_m_A1"}
TASKS = ["1-amazon", "2-yahoo", "3-agnews"]

print("calibration-to-rest ratio of sum|dtheta| / sum eta-increment (post hoc)")
for label, folder in ARMS.items():
    vals = []
    for t in TASKS:
        rows = list(csv.DictReader(open(HERE / folder / "Qwen_Qwen3-0.6Blora_cl_dataset_id_4" / t / "drift_log.csv",
                                        encoding="utf-8")))
        steps = np.array([int(r["step"]) for r in rows])
        d = np.array([float(r["delta_t"]) for r in rows])
        inc = np.diff(np.concatenate([[0.0], np.array([float(r["tau"]) for r in rows])]))
        cal = steps <= 24
        vals.append((d[cal].sum() / inc[cal].sum()) / (d[~cal].sum() / inc[~cal].sum()))
    print(f"  {label:22s} " + "  ".join(f"{t[2:]} {v:.3f}" for t, v in zip(TASKS, vals)))
