# Same analysis as r2_reconstruction.py (hashed 8 Nov ~01:50), for one eta_m arm of the repeated runs
# (preinregistrare_FOREVER_repetari_2026-11-08.md). TASKS 1-3 ONLY: in the A arms the task-0 drift_log is copied
# from the tau run and does not measure the eta*|m_hat| clock. Run it on "eta_m" too, for the comparable R2 value.
# Usage: python -I r2_reconstruction_arm.py <arm>; writes runs/forever_repetari_r2_<arm>.json
import csv, json, sys
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
arm = sys.argv[1]
here = Path(__file__).resolve().parent
root = here / f"ckpt_{arm}" / "Qwen_Qwen3-0.6Blora_cl_dataset_id_4"
tasks = ["1-amazon", "2-yahoo", "3-agnews"]


def r2(x, y):
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    sst = ((y - y.mean()) ** 2).sum()
    return float(1 - (res ** 2).sum() / sst), beta.tolist()


out, X_all, Y_all = {"arm": arm}, [], []
for t in tasks:
    rows = list(csv.DictReader(open(root / t / "drift_log.csv", encoding="utf-8")))
    d = np.array([float(r["delta_t"]) for r in rows])
    tau = np.array([float(r["tau"]) for r in rows])
    inc = np.diff(np.concatenate([[0.0], tau]))
    nb = len(d) // 8
    y = d[: nb * 8].reshape(nb, 8).sum(1)
    x = inc[: nb * 8].reshape(nb, 8).sum(1)
    R2, beta = r2(x, y)
    out[t] = {"rows": len(rows), "windows": nb, "R2": R2, "intercept_slope": beta}
    print(f"{arm} {t}: rows {len(rows)}, windows {nb}, R2 = {R2:.4f}")
    X_all.append(x); Y_all.append(y)
R2p, betap = r2(np.concatenate(X_all), np.concatenate(Y_all))
out["pooled_tasks_1_3"] = {"windows": int(sum(len(x) for x in X_all)), "R2": R2p, "intercept_slope": betap}
print(f"{arm} POOLED tasks 1-3: windows {out['pooled_tasks_1_3']['windows']}, R2 = {R2p:.4f}")
json.dump(out, open(here.parent / "runs" / f"forever_repetari_r2_{arm}.json", "w"), indent=1)
