# Stage 0 preview of gate G2 on technical runs (4 Nov 2026). Run from Stadiul0: python g2_preview.py
# G2 (identifiability) on technical runs: out-of-sample R^2 of the interval rate rho = dce/max(dN,1) predicted from
# B_strong. Blind to T1: F_A, F_B, dAcc_A are never read; no model predicts forgetting.
import sys, numpy as np, pandas as pd
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
R = Path(r"D:\Time\02_Pilot2\Stadiul0\runs")
runs = {"tech3_F2": R/"tech3_lr3e-4/F2_s9004", "tech3_F3": R/"tech3_lr3e-4/F3_s9004",
        "tech2_F1": R/"tech2_lr3e-4/F1_s9002", "tech2_F2": R/"tech2_lr3e-4/F2_s9002", "tech2_F3": R/"tech2_lr3e-4/F3_s9002"}
FORBID = {"F_A", "F_B", "dAcc_A"}
dfs = []
for name, rd in runs.items():
    d = pd.read_parquet(rd/"triplets.parquet")
    d = d[d["incl_nocap"] if "incl_nocap" in d else d["incl"]]
    d = d[(d.x_rule == 0) & (d.dN < 1280) & (d.dN >= 64)].copy()
    E = d.ep.nunique(); d["w"] = 1.0/(E*d.groupby("ep").ep.transform("size")); d["run"] = name
    dfs.append(d.drop(columns=[c for c in FORBID if c in d]))
df = pd.concat(dfs, ignore_index=True)
df["C1_a"] = df.dN; df["C1_b"] = np.log(df.dN+1); df["C1_c"] = np.log(df.dN+10); df["C1_d"] = np.log(df.dN+100)
xcov = ["x_LB0","x_AB0","x_prior_LB","x_overlap","x_N0","x_tenure","x_prior_exposures","x_K_active","x_theta_norm0","x_sqrt_trv0"]
c6 = [c for c in df.columns if c.startswith("C6_")]
bstrong = xcov + ["C0","C1_a","C1_b","C1_c","C1_d","C2","C3","C4","C5","C7a","C5a","C5b_g","C5b_gt","C5b_L","C5c_sq","C5c_work",
          "C5d","C5e","C5f","C2b","C6b_theta","C6b_v","C10","C10b"] + c6 + \
          [f"rate_{z}" for z in ["C2","C2b","C3","C4","C5","C5a","C5b_g","C5b_gt","C5b_L","C5c_sq","C5c_work","C5d","C5e","C5f","C10","C10b"]]
assert not any(c.startswith("ce_") or "Disp" in c or c in FORBID for c in bstrong)
df[bstrong] = df[bstrong].fillna(0.0)
def r2w(y, p, w):
    m = (w*y).sum()/w.sum(); return 1 - (w*(y-p)**2).sum()/(w*(y-m)**2).sum()
print(f"triplets: {len(df)}; runs: {df.run.nunique()}; features: {len(bstrong)}")
rows = []
for D in ["D1", "D1_rel", "D2", "D3"]:
    y = np.nan_to_num(df[f"rate_ce_{D}"].to_numpy(), nan=0.0)
    for test in ["tech3_F2", "tech3_F3"]:
        tr, te = (df.run != test).to_numpy(), (df.run == test).to_numpy()
        out = {"D": D, "test": test}
        for name, mdl in [("OLS", make_pipeline(StandardScaler(), LinearRegression())),
                          ("GBDT", HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20, random_state=0))]:
            mdl.fit(df.loc[tr, bstrong], y[tr], **({"histgradientboostingregressor__sample_weight": None} if False else {}))
            p = mdl.predict(df.loc[te, bstrong]); w = df.w.to_numpy()[te]
            out[f"R2_{name}"] = r2w(y[te], p, w)
        # how variable is the rate within the test run (CV), and how much does dN alone explain it
        yt = y[te]; w = df.w.to_numpy()[te]; mu = (w*yt).sum()/w.sum()
        out["CV_rate"] = np.sqrt((w*(yt-mu)**2).sum()/w.sum())/mu
        g = HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, random_state=0).fit(df.loc[tr, ["C1_a","C1_b","C1_c","C1_d"]], y[tr])
        out["R2_dN_only"] = r2w(yt, g.predict(df.loc[te, ["C1_a","C1_b","C1_c","C1_d"]]), w)
        rows.append(out)
print(pd.DataFrame(rows).round(3).to_string(index=False))

print("\n--- scara: R2 (OLS) al ratei din seturi minime de telemetrie, medie pe cele doua rulari test ---")
sets = {"ΔN": ["C1_a","C1_b","C1_c","C1_d"],
        "ΔN + rata Ση (C3)": ["C1_a","C1_b","C1_c","C1_d","rate_C3"],
        "ΔN + rata Σ‖g̃‖ (C5a)": ["C1_a","C1_b","C1_c","C1_d","rate_C5a"],
        "ΔN + rata Ση‖g̃‖ (C5b)": ["C1_a","C1_b","C1_c","C1_d","rate_C5b_gt"],
        "ΔN + rata Ση‖m̂‖ (C5d)": ["C1_a","C1_b","C1_c","C1_d","rate_C5d"],
        "ΔN + rata Σ‖m̂‖ (C5e)": ["C1_a","C1_b","C1_c","C1_d","rate_C5e"],
        "ΔN + C3 + C5d + C5e (rate)": ["C1_a","C1_b","C1_c","C1_d","rate_C3","rate_C5d","rate_C5e"],
        "ΔN + rata pierderii pe R (C10b)": ["C1_a","C1_b","C1_c","C1_d","rate_C10b"]}
res = []
for D in ["D1","D1_rel","D2","D3"]:
    y = np.nan_to_num(df[f"rate_ce_{D}"].to_numpy(), nan=0.0)
    row = {"D": D}
    for nm, cols in sets.items():
        r = []
        for test in ["tech3_F2","tech3_F3"]:
            tr, te = (df.run != test).to_numpy(), (df.run == test).to_numpy()
            m = make_pipeline(StandardScaler(), LinearRegression()).fit(df.loc[tr, cols], y[tr])
            r.append(r2w(y[te], m.predict(df.loc[te, cols]), df.w.to_numpy()[te]))
        row[nm] = np.mean(r)
    res.append(row)
print(pd.DataFrame(res).set_index("D").T.round(3).to_string())
