# Secondary analysis of the preregistration (preinregistrare_FOREVER_repro_2026-11-07.md), fixed 8 Nov 2026 ~02:00,
# BEFORE the R2 drift logs exist beyond its first steps:
#   "in R2, R^2 (OLS) of the rate of ||dtheta|| over 8-step windows, from the increase of the eta*|m_hat| clock
#    in the same window; reported (our benchmark: >= 0.90)".
# Data: ckpt_eta_m/<model>/<k>-<task>/drift_log.csv, columns step, delta_t (=||dtheta|| of the step, their code),
#   tau (= the eta*|m_hat| clock, cumulative), tau_true (= cumulative ||dtheta||).
# Windows: consecutive, non-overlapping blocks of 8 rows within each task; the incomplete last block is dropped.
#   y = sum of delta_t in the block; x = increase of tau over the block (tau[last] - tau[before first]).
# OLS with intercept; R^2 = 1 - SSres/SStot. HEADLINE: pooled over the 4 tasks; per-task R^2 reported as detail.
import csv, json, sys
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
root = Path(__file__).resolve().parent / "ckpt_eta_m" / "Qwen_Qwen3-0.6Blora_cl_dataset_id_4"
tasks = ["0-dbpedia", "1-amazon", "2-yahoo", "3-agnews"]


def r2(x, y):
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    sst = ((y - y.mean()) ** 2).sum()
    return float(1 - (res ** 2).sum() / sst), beta.tolist()


out, X_all, Y_all = {}, [], []
for t in tasks:
    p = root / t / "drift_log.csv"
    if not p.exists():
        print(f"{t}: drift_log missing"); continue
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    d = np.array([float(r["delta_t"]) for r in rows])
    tau = np.array([float(r["tau"]) for r in rows])
    inc = np.diff(np.concatenate([[0.0], tau]))
    nb = len(d) // 8
    y = d[: nb * 8].reshape(nb, 8).sum(1)
    x = inc[: nb * 8].reshape(nb, 8).sum(1)
    R2, beta = r2(x, y)
    out[t] = {"rows": len(rows), "windows": nb, "R2": R2, "intercept_slope": beta}
    print(f"{t}: rows {len(rows)}, windows {nb}, R2 = {R2:.4f}")
    X_all.append(x); Y_all.append(y)

if X_all:
    R2p, betap = r2(np.concatenate(X_all), np.concatenate(Y_all))
    out["pooled"] = {"windows": int(sum(len(x) for x in X_all)), "R2": R2p, "intercept_slope": betap}
    print(f"POOLED (headline): windows {out['pooled']['windows']}, R2 = {R2p:.4f}  (benchmark >= 0.90)")
json.dump(out, open(Path(__file__).resolve().parent.parent / "runs" / "forever_repro_r2_reconstruction.json", "w"), indent=1)
