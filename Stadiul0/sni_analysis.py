# SuperNI check analysis (S1, S2), as fixed in preinregistrare_SuperNI_2026-11-07.md. Run from Stadiul0: python -I sni_analysis.py
import sys, json, numpy as np, pandas as pd
from pathlib import Path
from scipy import stats
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
sys.stdout.reconfigure(encoding="utf-8")
R = Path(__file__).resolve().parent / "runs" / "sni"
W = 8

def windows(rd):
    z = np.load(rd / "steps.npz"); S = pd.DataFrame(z["data"], columns=list(z["cols"]))
    S["eta_m"] = S.lr * S.m_hat_norm; rows = []
    for (task, ph), g in S[S.counted == 1].groupby(["task", "phase"]):
        g = g.sort_values("gstep")
        for j in range(len(g) // W):
            w = g.iloc[j * W:(j + 1) * W]
            rows.append(dict(run=rd.name, task=int(task), y=w.delta.mean(), S_eta=w.lr.sum(), S_eta_m=w.eta_m.sum(),
                             lr=w.lr.mean(), g=w.gnorm.mean(), gc=w.gnorm_clipped.mean(), m=w.m_hat_norm.mean(),
                             v=w.sqrt_trv.mean(), loss=w.loss.mean(), sip=w.step_in_phase.mean(), kind=int(w.kind.iloc[0]),
                             ntok=w.ntok.mean()))
    return rows

def r2(y, p):
    return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()

tau_runs = sorted(p for p in (R / "tau").glob("s*") if (p / "meta.json").exists())
D = pd.DataFrame([r for rd in tau_runs for r in windows(rd)])
print(f"S1: rulări τ {[p.name for p in tau_runs]}; ferestre {len(D)}; pe sarcini {D.groupby('task').size().to_dict()}")
full = ["lr", "g", "gc", "m", "v", "loss", "sip", "kind", "task", "ntok"]
models = {"Ση": ["S_eta"], "Ση‖m̂‖": ["S_eta_m"], "Ση + Ση‖m̂‖": ["S_eta", "S_eta_m"], "GBDT telemetrie": full}
res = {}
for scheme, key in [("o sămânță lăsată deoparte", "run"), ("o sarcină lăsată deoparte", "task")]:
    print(f"\n  {scheme}:")
    for nm, cols in models.items():
        rr = []
        for test in sorted(D[key].unique()):
            tr, te = D[key] != test, D[key] == test
            mdl = (HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20,
                                                 random_state=0) if nm.startswith("GBDT") else LinearRegression())
            if te.sum() < 3:
                continue
            rr.append(r2(D.loc[te, "y"].to_numpy(), mdl.fit(D.loc[tr, cols], D.loc[tr, "y"]).predict(D.loc[te, cols])))
        res[(scheme, nm)] = (float(np.mean(rr)), float(np.min(rr)), [round(x, 3) for x in rr])
        print(f"    {nm:18s} R² mediu {np.mean(rr):.3f}  minim {np.min(rr):.3f}  pe pliuri {res[(scheme, nm)][2]}")
s1 = all(res[(s, "Ση + Ση‖m̂‖")][0] >= 0.90 for s in ["o sămânță lăsată deoparte", "o sarcină lăsată deoparte"])
print("\nS1:", "RECONSTRUCȚIA SE EXTINDE la SuperNI" if s1 else "NU se extinde (concluzia rămâne limitată la faptele sintetice)")
out = {"S1_extends": s1, "results": {f"{k[0]} | {k[1]}": v for k, v in res.items()}}

eta_runs = sorted(p for p in (R / "eta_m").glob("s*") if (p / "meta.json").exists())
seeds = [p.name for p in eta_runs if (R / "tau" / p.name / "meta.json").exists()]
if seeds:
    E = lambda rd: float(np.nanmean(np.load(rd / "evals.npz")["loss"][-1]))
    d = np.array([(E(R / "tau" / s) - E(R / "eta_m" / s)) / E(R / "tau" / s) for s in seeds]); n = len(d)
    half = stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n) if n > 1 else np.inf
    lo, hi = d.mean() - half, d.mean() + half
    v = ("τ SUPERIOR" if d.mean() <= -0.05 and hi < 0 else "ECHIVALENȚĂ PRACTICĂ" if (lo > -0.05 and hi < 0.05) else "NECONCLUDENT")
    print(f"\nS2 ({n} semințe): diferența relativă E1(τ) − E1(eta_m) = {d.mean():+.4f}, IC 95% [{lo:+.4f}; {hi:+.4f}] -> {v}")
    for s in seeds:
        print(f"  {s}: E1 τ {E(R / 'tau' / s):.4f}, eta_m {E(R / 'eta_m' / s):.4f}")
    out["S2"] = dict(seeds=seeds, rel_diff=float(d.mean()), ci=[float(lo), float(hi)], verdict=v)
(R.parent / "sni_verdict.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
