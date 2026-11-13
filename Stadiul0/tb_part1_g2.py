# T-B, part 1 (Stage 0a, blind to T1): G2 for D3 within each condition, as fixed in preinregistrare_TA_TB_2026-11-06.md.
# Run from Stadiul0 after the night: python -I tb_part1_g2.py
# Builds triplets.parquet for each T-B run (p2.triplets.build; prints nothing about T1), then drops F_A, F_B, dAcc_A,
# F_A_clip, F_B_clip before any analysis. Writes the verdict to runs/tb_part1_verdict.json (read by part 2).
import json, sys, numpy as np, pandas as pd
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from scipy.stats import spearmanr
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
from p2.triplets import build
sys.stdout.reconfigure(encoding="utf-8")
R = HERE / "runs"
COND = {"F6_z0.0": "tb_F6_n00", "F6_z0.1": "tb_F6_n01", "F6_z0.3": "tb_F6_n03", "F6_z0.5": "tb_F6_n05", "F1": "tb_F1"}
FORBID = {"F_A", "F_B", "dAcc_A", "F_A_clip", "F_B_clip"}
xcov4 = ["x_LB0", "x_AB0", "x_prior_LB", "x_overlap", "x_N0", "x_tenure", "x_prior_exposures", "x_K_active",
         "x_theta_norm0", "x_sqrt_trv0", "x_LR0"]
dN4 = ["C1_a", "C1_b", "C1_c", "C1_d"]
def r2w(y, p, w):
    m = (w * y).sum() / w.sum(); return 1 - (w * (y - p) ** 2).sum() / (w * (y - m) ** 2).sum()
def ols():
    return make_pipeline(StandardScaler(), LinearRegression())
def gbdt():
    return HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20, random_state=0)

def load(tag):
    out = []
    for rd in sorted(p for p in (R / tag).iterdir() if (p / "meta.json").exists()):
        f = rd / "triplets.parquet"
        if not f.exists():
            df, _ = build(rd); df.to_parquet(f)
        d = pd.read_parquet(f)
        d = d.drop(columns=[c for c in FORBID if c in d])
        d = d[d.incl & (d.dN >= 64) & (d.dN < 1280)].copy(); d["run"] = rd.name; out.append(d)
    D = pd.concat(out, ignore_index=True)
    D["C1_a"] = D.dN; D["C1_b"] = np.log(D.dN + 1); D["C1_c"] = np.log(D.dN + 10); D["C1_d"] = np.log(D.dN + 100)
    return D

models = {"(i) dN + C10c": lambda D: dN4 + ["rate_C10c"],
          "(ii) dN + C10c + C10p + C10h": lambda D: dN4 + ["rate_C10c", "rate_C10p", "rate_C10h"],
          "(iii) GBDT pe B+": lambda D: xcov4 + dN4 + ["C0"] + [c for c in D.columns if c.startswith("rate_")
                                                             and not c.startswith(("rate_ce_", "rate_Disp_"))]}
res, per_seed = {}, {}
for cond, tag in COND.items():
    D = load(tag)
    assert not (set(D.columns) & FORBID)
    for clock in ["D3", "D1_rel"]:
        y = np.nan_to_num(D[f"rate_ce_{clock}"].to_numpy())
        for nm, colf in models.items():
            cols = colf(D); D[cols] = D[cols].fillna(0.0); rr = []
            for test in sorted(D.run.unique()):
                tr, te = (D.run != test).to_numpy(), (D.run == test).to_numpy()
                mdl = gbdt() if nm.startswith("(iii)") else ols()
                rr.append(r2w(y[te], mdl.fit(D.loc[tr, cols], y[tr]).predict(D.loc[te, cols]), D.w.to_numpy()[te]))
            res[(cond, clock, nm)] = (float(np.mean(rr)), float(np.min(rr)), float(np.max(rr)))
            per_seed[(cond, clock, nm)] = rr
    print(f"{cond}: {D.run.nunique()} rulări, {len(D)} tripleți")
print("\nR² în afara sămânței (o sămânță lăsată deoparte, în interiorul condiției): medie / min / max")
for k, v in res.items():
    print(f"  {k[0]:8s} {k[1]:7s} {k[2]:32s} {v[0]:.3f} / {v[1]:.3f} / {v[2]:.3f}")
k3 = ("F6_z0.3", "D3", "(iii) GBDT pe B+")
n_below = int(sum(r < 0.90 for r in per_seed[k3]))
g2_pass = n_below >= 6
u = {z: 1 - res[(f"F6_z{z}", "D3", "(iii) GBDT pe B+")][0] for z in ["0.0", "0.1", "0.3", "0.5"]}
zs = [0.0, 0.1, 0.3, 0.5]; us = [u["0.0"], u["0.1"], u["0.3"], u["0.5"]]
mono = all(us[i] < us[i + 1] for i in range(3)); rho = float(spearmanr(zs, us).correlation)
dose_pass = mono and u["0.3"] >= 2 * u["0.0"]
verdict = {"G2_F6_pass": g2_pass, "seeds_below_0.90_at_z0.3": n_below, "per_seed_R2_GBDT_z0.3": per_seed[k3],
           "u": u, "spearman": rho, "monotone": mono, "dose_response_pass": dose_pass,
           "part2_allowed": g2_pass}
(R / "tb_part1_verdict.json").write_text(json.dumps(verdict, indent=1), encoding="utf-8")
print(f"\nG2-F6 (z = 0,3, GBDT pe B+ < 0,90 în ≥ 6/8 semințe): {'TRECE' if g2_pass else 'PICĂ'} ({n_below}/8)")
print(f"Doza–răspuns: u = {dict((k, round(v, 3)) for k, v in u.items())}; monoton {mono}; Spearman {rho:.2f}; "
      f"u(0,3) ≥ 2·u(0): {u['0.3'] >= 2 * u['0.0']} -> {'TRECE' if dose_pass else 'PICĂ'}")
print("Partea 2 (H1):", "PERMISĂ" if g2_pass else "NU SE RULEAZĂ (D3 se închide ca indice experiențial în acest cadru)")
