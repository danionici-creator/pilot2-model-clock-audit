# C02: in-sample per-task R2 (as r2_reconstruction*.py) vs leave-one-task-out R2 (fit intercept+slope on the other tasks)
import csv, sys, numpy as np
from pathlib import Path
R = Path(r"D:\Time\02_Pilot2\Stadiul0\forever_repro")
def win(p):
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    d = np.array([float(r["delta_t"]) for r in rows]); tau = np.array([float(r["tau"]) for r in rows])
    inc = np.diff(np.concatenate([[0.0], tau])); nb = len(d)//8
    return inc[:nb*8].reshape(nb, 8).sum(1), d[:nb*8].reshape(nb, 8).sum(1)
def fit(x, y): return np.linalg.lstsq(np.column_stack([np.ones_like(x), x]), y, rcond=None)[0]
def r2(y, p): return 1 - ((y-p)**2).sum()/((y-y.mean())**2).sum()
for arm, tasks in [("eta_m", ["0-dbpedia","1-amazon","2-yahoo","3-agnews"]), ("eta_m", ["1-amazon","2-yahoo","3-agnews"]), ("eta_m_A1", ["1-amazon","2-yahoo","3-agnews"])]:
    W = {t: win(R/f"ckpt_{arm}"/"Qwen_Qwen3-0.6Blora_cl_dataset_id_4"/t/"drift_log.csv") for t in tasks}
    out = []
    for t in tasks:
        x, y = W[t]; b_in = fit(x, y); ins = r2(y, b_in[0] + b_in[1]*x)
        xo = np.concatenate([W[u][0] for u in tasks if u != t]); yo = np.concatenate([W[u][1] for u in tasks if u != t])
        b = fit(xo, yo); ho = r2(y, b[0] + b[1]*x)
        out.append(f"{t}: in-sample {ins:.3f}, held-out-task {ho:.3f}, slope in/out {b_in[1]:.3f}/{b[1]:.3f}")
    print(arm, f"({len(tasks)} tasks)"); print("  " + "\n  ".join(out))
