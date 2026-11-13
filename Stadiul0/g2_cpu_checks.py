# Stage 0, two CPU checks on the technical runs before the LM arm (6 Nov 2026). Run from Stadiul0:
#   python g2_cpu_checks.py
# Blind to T1: F_A, F_B, dAcc_A are dropped on load; no model predicts forgetting.
# (a) G2 with family F3 left out entirely (F3 is the only test family with learning-rate restarts):
#     train on tech3_F2, tech2_F1, tech2_F2; test on tech3_F3 and tech2_F3.
# (b) Where does the cheap reconstruction "dN + rate of sum eta*|m_hat| (C5d)" fail? Residuals of a leave-one-run-out
#     OLS, binned by interval length, by segment boundaries and by learning-rate restarts inside the interval.
import json, numpy as np, pandas as pd
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

R = Path(r"D:\Time\02_Pilot2\Stadiul0\runs")
runs = {"tech3_F2": R/"tech3_lr3e-4/F2_s9004", "tech3_F3": R/"tech3_lr3e-4/F3_s9004",
        "tech2_F1": R/"tech2_lr3e-4/F1_s9002", "tech2_F2": R/"tech2_lr3e-4/F2_s9002", "tech2_F3": R/"tech2_lr3e-4/F3_s9002"}
FORBID = {"F_A", "F_B", "dAcc_A"}

def boundaries(rd):
    s = json.load(open(rd/"schedule.json"))
    b = np.cumsum([seg["steps"] for seg in s["segments"]])
    return np.unique(np.concatenate([[0], b])), np.asarray(s["restarts"], dtype=float)

dfs = []
for name, rd in runs.items():
    d = pd.read_parquet(rd/"triplets.parquet")
    d = d.drop(columns=[c for c in FORBID if c in d])
    d = d[d["incl_nocap"] if "incl_nocap" in d else d["incl"]]
    d = d[(d.x_rule == 0) & (d.dN < 1280) & (d.dN >= 64)].copy()
    E = d.ep.nunique(); d["w"] = 1.0/(E*d.groupby("ep").ep.transform("size")); d["run"] = name
    bnd, rst = boundaries(rd)
    n0, n1 = d.N0.to_numpy(float), d.N1.to_numpy(float)
    last = bnd[np.searchsorted(bnd, n0, side="right") - 1]
    d["since_bnd0"] = n0 - last
    d["n_bnd"] = np.searchsorted(bnd, n1, side="left") - np.searchsorted(bnd, n0, side="right")
    d["n_rst"] = (np.searchsorted(rst, n1, side="right") - np.searchsorted(rst, n0, side="right")) if len(rst) else 0
    dfs.append(d)
df = pd.concat(dfs, ignore_index=True)
assert not (set(df.columns) & FORBID)
df["C1_a"] = df.dN; df["C1_b"] = np.log(df.dN+1); df["C1_c"] = np.log(df.dN+10); df["C1_d"] = np.log(df.dN+100)
xcov = ["x_LB0","x_AB0","x_prior_LB","x_overlap","x_N0","x_tenure","x_prior_exposures","x_K_active","x_theta_norm0","x_sqrt_trv0"]
c6 = [c for c in df.columns if c.startswith("C6_")]
bstrong = xcov + ["C0","C1_a","C1_b","C1_c","C1_d","C2","C3","C4","C5","C7a","C5a","C5b_g","C5b_gt","C5b_L","C5c_sq","C5c_work",
          "C5d","C5e","C5f","C2b","C6b_theta","C6b_v","C10","C10b"] + c6 + \
          [f"rate_{z}" for z in ["C2","C2b","C3","C4","C5","C5a","C5b_g","C5b_gt","C5b_L","C5c_sq","C5c_work","C5d","C5e","C5f","C10","C10b"]]
assert not any(c.startswith("ce_") or "Disp" in c for c in bstrong)
df[bstrong] = df[bstrong].fillna(0.0)
dN4 = ["C1_a","C1_b","C1_c","C1_d"]
ladder = {"dN": dN4, "dN+C3": dN4+["rate_C3"], "dN+C5d": dN4+["rate_C5d"], "dN+C3+C5d+C5e": dN4+["rate_C3","rate_C5d","rate_C5e"]}

def r2w(y, p, w):
    m = (w*y).sum()/w.sum(); return 1 - (w*(y-p)**2).sum()/(w*(y-m)**2).sum()
def ols(): return make_pipeline(StandardScaler(), LinearRegression())
def gbdt(): return HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20, random_state=0)

print(f"triplets: {len(df)}; runs: {df.run.nunique()}; B_strong features: {len(bstrong)}")
print("\n(a) G2 with F3 left out of training entirely (train: tech3_F2, tech2_F1, tech2_F2)")
train = ~df.run.str.endswith("F3")
rows = []
for D in ["D1", "D1_rel", "D2", "D3"]:
    y = np.nan_to_num(df[f"rate_ce_{D}"].to_numpy(), nan=0.0)
    for test in ["tech3_F3", "tech2_F3"]:
        te = (df.run == test).to_numpy(); w = df.w.to_numpy()[te]; out = {"D": D, "test": test}
        for nm, mk in [("OLS_Bstrong", ols), ("GBDT_Bstrong", gbdt)]:
            out[nm] = r2w(y[te], mk().fit(df.loc[train, bstrong], y[train]).predict(df.loc[te, bstrong]), w)
        for nm, cols in ladder.items():
            out[nm] = r2w(y[te], ols().fit(df.loc[train, cols], y[train]).predict(df.loc[te, cols]), w)
        rows.append(out)
print(pd.DataFrame(rows).round(3).to_string(index=False))

print("\n(b) residual of OLS 'dN + rate C5d', leave-one-run-out; relative error |y-p|/mean(y) and bias (y-p)/mean(y)")
for D in ["D1", "D3"]:
    y = np.nan_to_num(df[f"rate_ce_{D}"].to_numpy(), nan=0.0); p = np.zeros_like(y)
    for r in df.run.unique():
        te = (df.run == r).to_numpy()
        p[te] = ols().fit(df.loc[~te, ladder["dN+C5d"]], y[~te]).predict(df.loc[te, ladder["dN+C5d"]])
    t = df[["run", "w", "since_bnd0", "n_bnd", "n_rst"]].copy(); t["y"] = y; t["res"] = y - p
    t["dN"] = df.dN.to_numpy()   # every interval starts at a segment start (N0 on a boundary), so the transient after a
    t["bin_dN"] = pd.cut(t.dN, [63, 127, 255, 511, 1279], labels=["64-127", "128-255", "256-511", "512-1279"])  # boundary = short dN
    t["bin_bnd"] = pd.cut(t.n_bnd, [-1, 0, 2, 5, 1e9], labels=["0", "1-2", "3-5", ">=6"])
    t["rst"] = np.where(t.n_rst > 0, "restart inside", "no restart")
    mu = (t.w*t.y).sum()/t.w.sum()
    def summ(g):
        ww = g.w.sum()
        return pd.Series({"n": len(g), "weight_%": 100*ww/t.w.sum(), "abs_err_rel": (g.w*g.res.abs()).sum()/ww/mu,
                          "bias_rel": (g.w*g.res).sum()/ww/mu})
    print(f"\n  {D}: overall R2 = {r2w(y, p, t.w.to_numpy()):.3f}")
    print(f"  N0 on a segment boundary in {100*(t.since_bnd0 == 0).mean():.0f}% of intervals")
    print("  by interval length dN (short = dominated by the transient after the boundary):")
    print(t.groupby("bin_dN", observed=True).apply(summ, include_groups=False).round(3).to_string())
    print("  by number of further segment boundaries inside the interval:")
    print(t.groupby("bin_bnd", observed=True).apply(summ, include_groups=False).round(3).to_string())
    print("  by learning-rate restart inside the interval (F3 only has restarts):")
    print(t.groupby("rst").apply(summ, include_groups=False).round(3).to_string())
