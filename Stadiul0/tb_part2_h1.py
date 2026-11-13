# T-B, part 2 (Stage 0b, automatic): H1 for D3 in F6, as fixed in preinregistrare_TA_TB_2026-11-06.md.
# Runs ONLY if runs/tb_part1_verdict.json says part2_allowed. Run from Stadiul0: python -I tb_part2_h1.py
# Per run: 5-fold cross-validation grouped by task; baseline GBDT on B+ (telemetry rates without C6, X_cov, dN terms,
# pause ticks, C10c, C10p, C10h); augmented = B+ plus rate_ce_D3 and ce_D3. Out-of-fold predictions pooled per run,
# R² weighted by the triplet weights w (as every G2 analysis); models fitted unweighted. dR² = R²(aug) - R²(base).
import json, sys, numpy as np, pandas as pd
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold
HERE = Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding="utf-8")
R = HERE / "runs"
v = json.loads((R / "tb_part1_verdict.json").read_text(encoding="utf-8"))
if not v["part2_allowed"]:
    raise SystemExit("Part 1 did not pass: H1 is not identifiable, part 2 is not run (preregistration).")
xcov4 = ["x_LB0", "x_AB0", "x_prior_LB", "x_overlap", "x_N0", "x_tenure", "x_prior_exposures", "x_K_active",
         "x_theta_norm0", "x_sqrt_trv0", "x_LR0"]
dN4 = ["C1_a", "C1_b", "C1_c", "C1_d"]
def r2w(y, p, w):
    m = (w * y).sum() / w.sum(); return 1 - (w * (y - p) ** 2).sum() / (w * (y - m) ** 2).sum()
def gbdt():
    return HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20, random_state=0)

def run_dr2(tag):
    out = []
    for rd in sorted(p for p in (R / tag).iterdir() if (p / "triplets.parquet").exists()):
        d = pd.read_parquet(rd / "triplets.parquet")
        d = d[d.incl & (d.dN >= 64) & (d.dN < 1280)].reset_index(drop=True)
        d["C1_a"] = d.dN; d["C1_b"] = np.log(d.dN + 1); d["C1_c"] = np.log(d.dN + 10); d["C1_d"] = np.log(d.dN + 100)
        base = xcov4 + dN4 + ["C0"] + [c for c in d.columns if c.startswith("rate_") and not c.startswith(("rate_ce_", "rate_Disp_"))]
        aug = base + ["rate_ce_D3", "ce_D3"]
        d[aug] = d[aug].fillna(0.0)
        row = {"run": rd.name, "n": len(d), "tasks": d.task.nunique()}
        for tgt in ["F_A", "dAcc_A"]:
            y = d[tgt].to_numpy(); pb, pa = np.zeros(len(d)), np.zeros(len(d))
            for tr, te in GroupKFold(n_splits=5).split(d, y, groups=d.task):
                pb[te] = gbdt().fit(d.loc[tr, base], y[tr]).predict(d.loc[te, base])
                pa[te] = gbdt().fit(d.loc[tr, aug], y[tr]).predict(d.loc[te, aug])
            w = d.w.to_numpy()
            row[f"R2_base_{tgt}"] = r2w(y, pb, w); row[f"R2_aug_{tgt}"] = r2w(y, pa, w)
            row[f"dR2_{tgt}"] = row[f"R2_aug_{tgt}"] - row[f"R2_base_{tgt}"]
        out.append(row)
    return pd.DataFrame(out)

def verdict(T, label):
    dr = T.dR2_F_A.to_numpy(); rng = np.random.default_rng(20261107)
    boot = np.array([rng.choice(dr, len(dr), replace=True).mean() for _ in range(10000)])
    lo = float(np.percentile(boot, 2.5)); pos = int((dr > 0).sum()); same_sign = bool(T.dR2_dAcc_A.mean() > 0)
    ok = dr.mean() >= 0.02 and pos >= 6 and lo > 0 and same_sign
    print(f"\n{label}: dR² pe T1 (F_A): medie {dr.mean():.4f}, > 0 în {pos}/{len(dr)} semințe, IC 95% bootstrap inferior {lo:.4f}; "
          f"dR² pe T1_acc: medie {T.dR2_dAcc_A.mean():.4f}")
    print(f"  H1 {label}: {'SUSȚINUT' if ok else 'NESUSȚINUT (D3 se închide)'}")
    return ok, lo

T = run_dr2("tb_F6_n03"); print(T.round(4).to_string(index=False))
ok, lo = verdict(T, "F6, zgomot 0,3 (primar)")
for tag, lab in [("tb_F6_n01", "F6, zgomot 0,1 (secundar)"), ("tb_F6_n05", "F6, zgomot 0,5 (secundar)")]:
    verdict(run_dr2(tag), lab)
(R / "tb_part2_verdict.json").write_text(json.dumps({"H1_F6_supported": bool(ok), "boot_lo": lo,
                                                     "per_run": T.to_dict(orient="records")}, indent=1), encoding="utf-8")
