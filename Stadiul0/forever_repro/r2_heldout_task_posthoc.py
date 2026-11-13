# POST HOC, 12 Nov 2026, after the independent audit of the archive (Recenzii/Audit_Codex_2026-11-10/, finding B02/C02).
# Not preregistered. r2_reconstruction.py and r2_reconstruction_arm.py fit the OLS (intercept + slope) and score it on the
# same 8-step windows, so their R² are in-sample (with one predictor, the squared correlation). This script reports, for
# the same windows and the same definitions, the R² of each task when the line is fitted on the OTHER tasks of the run
# (leave one task out), next to the in-sample value.
# Windows: consecutive, non-overlapping blocks of 8 rows of drift_log.csv within each task, the incomplete last block
# dropped; y = sum of delta_t (||dtheta|| of the step) in the block; x = increase of the eta*|m_hat| clock (column tau).
# Arms: eta_m (R2 of the reproduction), tasks 0-3 as the headline of r2_reconstruction.py, and tasks 1-3 for comparison
# with eta_m_A1, whose task-0 drift_log is copied from the tau run (see r2_reconstruction_arm.py).
# Usage, from Stadiul0/forever_repro: python -I r2_heldout_task_posthoc.py   (prints only; the stored output is
# runs/forever_r2_heldout_task_posthoc.log)
import csv, sys
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
MODEL = "Qwen_Qwen3-0.6Blora_cl_dataset_id_4"


def windows(p):
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    d = np.array([float(r["delta_t"]) for r in rows])
    tau = np.array([float(r["tau"]) for r in rows])
    inc = np.diff(np.concatenate([[0.0], tau]))
    nb = len(d) // 8
    return inc[: nb * 8].reshape(nb, 8).sum(1), d[: nb * 8].reshape(nb, 8).sum(1)


def fit(x, y):
    return np.linalg.lstsq(np.column_stack([np.ones_like(x), x]), y, rcond=None)[0]


def r2(y, p):
    return float(1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum())


print("R² of the rate of ||dtheta|| from the eta*|m_hat| clock, 8-step windows: in-sample (fitted on the task itself, as")
print("r2_reconstruction*.py) and leave one task out (fitted on the other tasks of the same run). Post hoc, 12 Nov 2026.")
for arm, tasks in [("eta_m", ["0-dbpedia", "1-amazon", "2-yahoo", "3-agnews"]),
                   ("eta_m", ["1-amazon", "2-yahoo", "3-agnews"]),
                   ("eta_m_A1", ["1-amazon", "2-yahoo", "3-agnews"])]:
    W = {t: windows(HERE / f"ckpt_{arm}" / MODEL / t / "drift_log.csv") for t in tasks}
    print(f"\n{arm}, tasks {tasks[0][0]}-{tasks[-1][0]}:")
    for t in tasks:
        x, y = W[t]
        b_in = fit(x, y)
        xo = np.concatenate([W[u][0] for u in tasks if u != t])
        yo = np.concatenate([W[u][1] for u in tasks if u != t])
        b_out = fit(xo, yo)
        print(f"  {t:10s} windows {len(x):3d}  in-sample R² {r2(y, b_in[0] + b_in[1] * x):.3f}  "
              f"leave-task-out R² {r2(y, b_out[0] + b_out[1] * x):.3f}  slope in/out {b_in[1]:.1f} / {b_out[1]:.1f}")
