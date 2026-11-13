# Usage (from Stadiul0): python preview_headroom.py runs/tech2_lr3e-4  (needs triplets.parquet from stage0_summary.py)
"""Headroom preview (G3-type quantity) on technical runs: R^2 of Delta N alone and of B_strong (no c_e).
Leave-one-run-out, untuned GBDT, episode weights, weighted within-run R^2. c_e is deliberately NOT used."""
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor

tag = Path(sys.argv[1])
dfs = [pd.read_parquet(p) for p in sorted(tag.glob("*/triplets.parquet"))]
df = pd.concat([d[d["incl"]] for d in dfs], ignore_index=True)
df["run"] = df["family"] + "_" + df["seed"].astype(str)
df["C1_a"] = df["dN"]; df["C1_b"] = np.log(df["dN"] + 1); df["C1_c"] = np.log(df["dN"] + 10); df["C1_d"] = np.log(df["dN"] + 100)

xcov = ["x_rule", "x_log_nvalues", "x_LB0", "x_AB0", "x_prior_LB", "x_overlap", "x_N0", "x_tenure",
        "x_prior_exposures", "x_K_active", "x_theta_norm0", "x_sqrt_trv0"]
counts = ["C0", "C1_a", "C1_b", "C1_c", "C1_d"]
bstd = counts + ["C2", "C3", "C4", "C5", "C7a"]
c6 = [c for c in df.columns if c.startswith("C6_")]
bstrong = xcov + bstd + ["C5a", "C5b_g", "C5b_gt", "C5b_L", "C5c_sq", "C5c_work", "C5d", "C5e", "C5f", "C2b",
                         "C6b_theta", "C6b_v", "C10", "C10b"] + c6 + \
          [f"rate_{z}" for z in ["C2", "C2b", "C3", "C4", "C5", "C5a", "C5b_g", "C5b_gt", "C5b_L", "C5c_sq",
                                 "C5c_work", "C5d", "C5e", "C5f", "C10", "C10b"]]
assert not any(c.startswith("ce_") or c.startswith("Disp") for c in bstrong)


def r2w(y, p, w):
    m = (w * y).sum() / w.sum()
    return 1 - (w * (y - p) ** 2).sum() / (w * (y - m) ** 2).sum()


def wcorr(x, y, w):
    w = w / w.sum(); mx, my = (w * x).sum(), (w * y).sum()
    return (w * (x - mx) * (y - my)).sum() / np.sqrt((w * (x - mx) ** 2).sum() * (w * (y - my) ** 2).sum())


rows = []
for r in sorted(df["run"].unique()):
    tr, te = df[df["run"] != r], df[df["run"] == r]
    out = {"test_run": r, "n": len(te), "r_AB": wcorr(te["F_A"].values, te["F_B"].values, te["w"].values)}
    for name, cols in [("dN_only", ["C1_a", "C1_b", "C1_c", "C1_d"]), ("dN+X_cov", counts[1:] + xcov),
                       ("B_standard+X_cov", bstd + xcov), ("B_strong", bstrong)]:
        m = HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20,
                                          random_state=0)
        m.fit(tr[cols], tr["F_A"], sample_weight=tr["w"])
        out[name] = r2w(te["F_A"].values, m.predict(te[cols]), te["w"].values)
    rows.append(out)
res = pd.DataFrame(rows)
res["headroom_vs_B_strong"] = res["r_AB"] - res["B_strong"]
pd.set_option("display.width", 200)
print(res.round(3).to_string(index=False))
# shape of forgetting vs Delta N (pooled)
bins = [64, 128, 256, 512, 1024, 2048, 4096, 1e9]
df["dN_bin"] = pd.cut(df["dN"], bins, right=False)
g = df.groupby("dN_bin", observed=True).apply(lambda d: pd.Series({"n": len(d), "F_A_mean": np.average(d["F_A"], weights=d["w"]),
                                                    "F_A_sd": d["F_A"].std(), "dAcc_mean": np.average(d["dAcc_A"], weights=d["w"])}))
print(g.round(3).to_string())
