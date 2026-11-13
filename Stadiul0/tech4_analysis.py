# tech4 (6 Nov 2026), the descriptive measures fixed in tech4_criterii.md. Run from Stadiul0: python -I tech4_analysis.py
# c_e-blind with respect to T1: no model relates c_e to forgetting. (1) forgetting speed by dN, per family, uncapped,
# on T1 (F_A), T1-acc (dAcc_A) and F^clip; (2) the G2 ladder (rate of c_e from telemetry), leave one run out, which
# never reads F_A, F_B, dAcc_A.
import sys, numpy as np, pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
sys.stdout.reconfigure(encoding="utf-8")
R = Path(r"D:\Time\02_Pilot2\Stadiul0\runs\tech4")
dfs = {f: pd.read_parquet(R / f"{f}_s9005" / "triplets.parquet") for f in ["F1", "F2", "F3", "F4", "F5", "F6"]}

print("(1) Viteza uitării, fără plafon (tripleți cu competență AB0 >= 0,90 și dN >= 64), medii ponderate pe episod")
bins = [63, 255, 639, 1279, 2047, 4095, 1e9]; labels = ["64-255", "256-639", "640-1279", "1280-2047", "2048-4095", ">=4096"]
rows = []
for f, d in dfs.items():
    d = d[d.incl_nocap].copy(); d["bin"] = pd.cut(d.dN, bins, labels=labels)
    for b, g in d.groupby("bin", observed=True):
        w = g.w_nocap
        rows.append(dict(fam=f, dN=b, n=len(g), F_A=(w*g.F_A).sum()/w.sum(), dAcc_A=(w*g.dAcc_A).sum()/w.sum(),
                         F_A_clip=(w*g.F_A_clip).sum()/w.sum() if "F_A_clip" in g else np.nan))
T = pd.DataFrame(rows)
for col in ["F_A", "dAcc_A", "F_A_clip"]:
    print(f"\n  {col} (nați pentru F, fracție pentru dAcc):")
    print(T.pivot(index="fam", columns="dN", values=col).round(3).to_string())
print("\n  numărul de tripleți:"); print(T.pivot(index="fam", columns="dN", values="n").fillna(0).astype(int).to_string())

print("\n(2) G2 pe tech4: R² al ratei lui c_e, o familie lăsată deoparte (antrenare pe celelalte 5; dN in [64, 1280))")
FORBID = {"F_A", "F_B", "dAcc_A", "F_A_clip", "F_B_clip"}
D = []
for f, d in dfs.items():
    d = d[d.incl].drop(columns=[c for c in FORBID if c in d]).copy(); d["run"] = f; D.append(d)
D = pd.concat(D, ignore_index=True)
D["C1_a"] = D.dN; D["C1_b"] = np.log(D.dN + 1); D["C1_c"] = np.log(D.dN + 10); D["C1_d"] = np.log(D.dN + 100)
dN4 = ["C1_a", "C1_b", "C1_c", "C1_d"]
xcov = ["x_LB0", "x_AB0", "x_prior_LB", "x_overlap", "x_N0", "x_tenure", "x_prior_exposures", "x_K_active",
        "x_theta_norm0", "x_sqrt_trv0", "x_LR0"]
rates = [c for c in D.columns if c.startswith("rate_") and not c.startswith(("rate_ce_", "rate_Disp_"))]
full = xcov + dN4 + ["C0"] + rates
D[full] = D[full].fillna(0.0)
def r2w(y, p, w):
    m = (w*y).sum()/w.sum(); return 1 - (w*(y-p)**2).sum()/(w*(y-m)**2).sum()
ladder = {"dN": dN4, "dN + C3 (Ση)": dN4 + ["rate_C3"], "dN + C5d (Ση‖m̂‖)": dN4 + ["rate_C5d"],
          "dN + C10c": dN4 + ["rate_C10c"]}
out = []
for Dn in ["D1", "D1_rel", "D2", "D3"]:
    y = np.nan_to_num(D[f"rate_ce_{Dn}"].to_numpy())
    for test in ["F2", "F3", "F5", "F6"]:
        tr, te = (D.run != test).to_numpy(), (D.run == test).to_numpy(); w = D.w.to_numpy()[te]
        row = {"D": Dn, "test": test}
        for nm, cols in ladder.items():
            row[nm] = r2w(y[te], make_pipeline(StandardScaler(), LinearRegression()).fit(D.loc[tr, cols], y[tr]).predict(D.loc[te, cols]), w)
        g = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20, random_state=0)
        row["GBDT tot"] = r2w(y[te], g.fit(D.loc[tr, full], y[tr]).predict(D.loc[te, full]), w)
        out.append(row)
print(pd.DataFrame(out).round(3).to_string(index=False))
