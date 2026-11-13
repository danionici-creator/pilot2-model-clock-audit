# T-D (colloquium 6 Nov 2026): offline audit of the parameter-clock reconstruction. Criteria fixed before: td_criterii.md
# Run from Stadiul0: python -I td_audit.py. v2 (6 Nov, 23:0x): parts (2)-(3) use the scaled OLS of tech4_analysis.py
# (v1 used unscaled OLS: ill-conditioned with dN ~1e3 and rates ~1e-7; log kept as runs/td_audit_v1_eroare_scalare.log). Blind to T1 (F_A, F_B, dAcc_A are dropped on load).
import sys, numpy as np, pandas as pd
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
sys.stdout.reconfigure(encoding="utf-8")
R = Path(r"D:\Time\02_Pilot2\Stadiul0\runs")
FORBID = {"F_A", "F_B", "dAcc_A", "F_A_clip", "F_B_clip"}
CL = ["D1", "D1_rel", "D2", "D3"]
def r2w(y, p, w):
    m = (w * y).sum() / w.sum(); return 1 - (w * (y - p) ** 2).sum() / (w * (y - m) ** 2).sum()
def gbdt():
    return HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, random_state=0)
def ols():
    return make_pipeline(StandardScaler(), LinearRegression())
xcov = ["x_LB0", "x_AB0", "x_prior_LB", "x_overlap", "x_N0", "x_tenure", "x_prior_exposures", "x_K_active",
        "x_theta_norm0", "x_sqrt_trv0"]
xcov4 = xcov + ["x_LR0"]                                # tech4 has L_R(t0) in X_cov, as tech4_analysis.py

# ---------- (1) R1 data without the circular C6 features
runs = {"tech3_F2": R / "tech3_lr3e-4/F2_s9004", "tech3_F3": R / "tech3_lr3e-4/F3_s9004",
        "tech2_F1": R / "tech2_lr3e-4/F1_s9002", "tech2_F2": R / "tech2_lr3e-4/F2_s9002", "tech2_F3": R / "tech2_lr3e-4/F3_s9002"}
dfs = []
for name, rd in runs.items():
    d = pd.read_parquet(rd / "triplets.parquet")
    d = d[d["incl_nocap"] if "incl_nocap" in d else d["incl"]]
    d = d[(d.x_rule == 0) & (d.dN < 1280) & (d.dN >= 64)].copy()
    E = d.ep.nunique(); d["w"] = 1.0 / (E * d.groupby("ep").ep.transform("size")); d["run"] = name
    dfs.append(d.drop(columns=[c for c in FORBID if c in d]))
df = pd.concat(dfs, ignore_index=True)
df["C1_a"] = df.dN; df["C1_b"] = np.log(df.dN + 1); df["C1_c"] = np.log(df.dN + 10); df["C1_d"] = np.log(df.dN + 100)
c6 = [c for c in df.columns if c.startswith("C6_")]
base = xcov + ["C0", "C1_a", "C1_b", "C1_c", "C1_d", "C2", "C3", "C4", "C5", "C7a", "C5a", "C5b_g", "C5b_gt", "C5b_L",
               "C5c_sq", "C5c_work", "C5d", "C5e", "C5f", "C2b", "C6b_theta", "C6b_v", "C10", "C10b"] + \
       [f"rate_{z}" for z in ["C2", "C2b", "C3", "C4", "C5", "C5a", "C5b_g", "C5b_gt", "C5b_L", "C5c_sq", "C5c_work",
                              "C5d", "C5e", "C5f", "C10", "C10b"]]
sets = {"B_strong complet": base + c6, "B_strong fără C6": base}
for s in sets.values():
    df[s] = df[s].fillna(0.0)
print(f"(1) R1 (tech2/tech3): {len(df)} tripleți; C6 = {len(c6)} trăsături; test pe fiecare rulare tech3, antrenare pe celelalte 4")
out = []
for D in CL:
    y = np.nan_to_num(df[f"rate_ce_{D}"].to_numpy(), nan=0.0)
    for test in ["tech3_F2", "tech3_F3"]:
        tr, te = (df.run != test).to_numpy(), (df.run == test).to_numpy(); w = df.w.to_numpy()[te]
        row = {"D": D, "test": test}
        for nm, cols in sets.items():
            row[f"OLS, {nm}"] = r2w(y[te], ols().fit(df.loc[tr, cols], y[tr]).predict(df.loc[te, cols]), w)
            row[f"GBDT, {nm}"] = r2w(y[te], gbdt().fit(df.loc[tr, cols], y[tr]).predict(df.loc[te, cols]), w)
        out.append(row)
print(pd.DataFrame(out).round(3).to_string(index=False))

# ---------- (2)-(3) tech4: leave one mechanism out; dN bands
T4 = R / "tech4"; D4 = []
for f in ["F1", "F2", "F3", "F4", "F5", "F6"]:
    d = pd.read_parquet(T4 / f"{f}_s9005" / "triplets.parquet")
    d = d[d.incl].drop(columns=[c for c in FORBID if c in d]).copy(); d["run"] = f; D4.append(d)
D4 = pd.concat(D4, ignore_index=True)
D4 = D4[(D4.dN >= 64) & (D4.dN < 1280)].copy()
D4["C1_a"] = D4.dN; D4["C1_b"] = np.log(D4.dN + 1); D4["C1_c"] = np.log(D4.dN + 10); D4["C1_d"] = np.log(D4.dN + 100)
dN4 = ["C1_a", "C1_b", "C1_c", "C1_d"]
rates = [c for c in D4.columns if c.startswith("rate_") and not c.startswith(("rate_ce_", "rate_Disp_"))]
full = xcov4 + dN4 + ["C0"] + rates
D4[full] = D4[full].fillna(0.0)
ladder = {"dN + C5d (Ση‖m̂‖)": dN4 + ["rate_C5d"], "dN + C10c": dN4 + ["rate_C10c"], "GBDT tot": full}
excl = {"F1": [], "F2": ["F5"], "F3": ["F5"], "F4": ["F5"], "F6": []}
print("\n(2) tech4, mecanismul lăsat deoparte (pentru F2, F3, F4 antrenarea exclude și F5); R² ponderat")
out = []
for Dn in CL:
    y = np.nan_to_num(D4[f"rate_ce_{Dn}"].to_numpy())
    for test, ex in excl.items():
        te = (D4.run == test).to_numpy(); tr = (~D4.run.isin([test] + ex)).to_numpy(); w = D4.w.to_numpy()[te]
        row = {"D": Dn, "test": test, "exclus": "+".join(ex) or "-"}
        for nm, cols in ladder.items():
            mdl = gbdt() if nm.startswith("GBDT") else ols()
            row[nm] = r2w(y[te], mdl.fit(D4.loc[tr, cols], y[tr]).predict(D4.loc[te, cols]), w)
        out.append(row)
print(pd.DataFrame(out).round(3).to_string(index=False))

print("\n(3) tech4, o familie lăsată deoparte, dN + C5d: R² și eroarea relativă medie pe benzi de dN")
bands = [(64, 128), (128, 256), (256, 640), (640, 1280)]
out = []
for Dn in ["D1", "D2", "D3"]:
    y = np.nan_to_num(D4[f"rate_ce_{Dn}"].to_numpy()); pred = np.zeros_like(y)
    for test in D4.run.unique():
        te = (D4.run == test).to_numpy()
        pred[te] = ols().fit(D4.loc[~te, ladder["dN + C5d (Ση‖m̂‖)"]], y[~te]).predict(D4.loc[te, ladder["dN + C5d (Ση‖m̂‖)"]])
    for lo, hi in bands:
        m = ((D4.dN >= lo) & (D4.dN < hi)).to_numpy(); w = D4.w.to_numpy()[m]
        out.append(dict(D=Dn, banda=f"{lo}-{hi - 1}", n=int(m.sum()), R2=r2w(y[m], pred[m], w),
                        eroare_rel=float((w * np.abs(y[m] - pred[m])).sum() / (w * np.abs(y[m])).sum())))
print(pd.DataFrame(out).round(3).to_string(index=False))

# ---------- (4) LM arm: transfer across configurations (tau rate, 8-step windows, as lm_forever_g2.py)
def lm_windows(root, W=8):
    rows = []
    for rd in sorted(p for p in root.iterdir() if (p / "meta.json").exists()):
        z = np.load(rd / "steps.npz"); S = pd.DataFrame(z["data"], columns=list(z["cols"]))
        S["eta_m"] = S.lr * S.m_hat_norm
        for (task, ph), g in S[S.counted == 1].groupby(["task", "phase"]):
            g = g.sort_values("gstep")
            for j in range(len(g) // W):
                w = g.iloc[j * W:(j + 1) * W]
                rows.append(dict(run=rd.name, y=w.delta.mean(), S_eta=w.lr.sum(), S_eta_m=w.eta_m.sum(), lr=w.lr.mean(),
                                 g=w.gnorm.mean(), gc=w.gnorm_clipped.mean(), m=w.m_hat_norm.mean(), v=w.sqrt_trv.mean(),
                                 loss=w.loss.mean(), sip=w.step_in_phase.mean(), kind=int(w.kind.iloc[0]), task=task,
                                 skipped=w.skipped.sum()))
    return pd.DataFrame(rows)
print("\n(4) brațul LM, rata lui τ (ferestre de 8 pași): antrenare pe lmtech1, test pe celelalte configurații")
L = {n: lm_windows(R / n) for n in ["lmtech1", "lmtech2", "lmsens_bf16", "lmsens_a32"]}
lin = ["S_eta", "S_eta_m"]; fullL = ["lr", "g", "gc", "m", "v", "loss", "sip", "kind", "task", "skipped"]
A = L["lmtech1"]
m_lin = LinearRegression().fit(A[lin], A.y); m_gb = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05,
          max_leaf_nodes=31, min_samples_leaf=20, random_state=0).fit(A[fullL], A.y)
def r2(y, p):
    return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()
out = []
for n in ["lmtech2", "lmsens_bf16", "lmsens_a32"]:
    B = L[n]
    out.append(dict(test=n, ferestre=len(B), **{"OLS Ση + Ση‖m̂‖": r2(B.y.to_numpy(), m_lin.predict(B[lin])),
                                                 "GBDT telemetrie": r2(B.y.to_numpy(), m_gb.predict(B[fullL]))}))
print(pd.DataFrame(out).round(3).to_string(index=False))
rr = []
for test in A.run.unique():
    tr, te = A.run != test, A.run == test
    rr.append(r2(A.y[te].to_numpy(), LinearRegression().fit(A.loc[tr, lin], A.y[tr]).predict(A.loc[te, lin])))
print("lmtech1, o sămânță lăsată deoparte, OLS Ση + Ση‖m̂‖ pe semințe:", np.round(rr, 3))
