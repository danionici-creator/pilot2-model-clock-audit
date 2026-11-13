"""G2 on the LM arm (technical round lmtech1): how much of the FOREVER clock is reconstructible from free telemetry?

    python -I lm_forever_g2.py ..\\runs\\lmtech1      (CPU environment of Stage 0: numpy, pandas, sklearn)

Blind to T1: reads steps.npz, probes.npz and the phase table only; evals.npz (accuracy, forgetting) is never opened.
Choices fixed before the round (lmtech1_criterii.md):
  * unit: non-overlapping windows of 8 counted steps (calibration and current phases), aligned to the phase start;
    a trailing partial window is dropped; y = mean Delta_t in the window (rate of tau, factors; also dW);
  * D3 (functional): RMS change of the probe log-probabilities (32 answer words) between consecutive probes of the same
    task, intervals that contain a replay step are dropped; y = increment / counted steps;
  * competitors, as window sums: S_eta = sum eta (C3, from the scheduler); S_eta_m = sum eta*|m_hat| (C5d);
    S_eta_g = sum eta*|g_clipped| (C5b); mean-field null S_eta_m*sqrt(d)/sqrt(Tr v_hat) (C5d/sqrt(v_bar));
    full telemetry (GBDT): eta, |g|, |g_clipped|, |m_hat|, sqrt(Tr v_hat), loss, step in phase, phase kind, task index,
    skipped steps;
  * out-of-run R^2: leave one seed out, every window weighted equally; OLS with intercept for single scalars.
"""
import sys, numpy as np, pandas as pd
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression

sys.stdout.reconfigure(encoding="utf-8")
root = Path(sys.argv[1]); W = 8
runs = sorted(p for p in root.iterdir() if (p/"meta.json").exists())
win_rows, d3_rows, phase_rows = [], [], []
for rd in runs:
    z = np.load(rd/"steps.npz"); cols = list(z["cols"]); S = pd.DataFrame(z["data"], columns=cols)
    S["eta_m"] = S.lr * S.m_hat_norm; S["eta_g"] = S.lr * S.gnorm_clipped
    C = S[S.counted == 1].copy()
    for (task, ph), g in C.groupby(["task", "phase"]):
        g = g.sort_values("gstep"); k = len(g) // W
        phase_rows.append(dict(run=rd.name, task=task, phase=ph, kind=int(g.kind.iloc[0]), n=len(g),
                               tau=g.delta.sum(), S_eta=g.lr.sum(), S_eta_m=g.eta_m.sum()))
        for j in range(k):
            w = g.iloc[j*W:(j+1)*W]
            win_rows.append(dict(run=rd.name, task=task, phase=ph, kind=int(w.kind.iloc[0]), win=j,
                                 y=w.delta.mean(), y_dW=w.delta_dW.mean(), S_eta=w.lr.sum(), S_eta_m=w.eta_m.sum(),
                                 S_eta_g=w.eta_g.sum(), mf=(w.eta_m * np.sqrt(1146880) / w.sqrt_trv.clip(lower=1e-12)).sum(),
                                 lr=w.lr.mean(), g=w.gnorm.mean(), gc=w.gnorm_clipped.mean(), m=w.m_hat_norm.mean(),
                                 v=w.sqrt_trv.mean(), loss=w.loss.mean(), sip=w.step_in_phase.mean(), skipped=w.skipped.sum()))
    P = np.load(rd/"probes.npz"); gs, tk, lp = P["gstep"], P["task"], P["logp"]
    rep = set(S.gstep[S.counted == 0].astype(int))
    for i in range(1, len(gs)):
        if tk[i] != tk[i-1]:
            continue
        span = C[(C.gstep > gs[i-1]) & (C.gstep <= gs[i])]
        if len(span) == 0 or any(gs[i-1] < s <= gs[i] for s in rep):
            continue
        inc = float(np.sqrt(((lp[i] - lp[i-1]) ** 2).mean(axis=1).mean()))
        d3_rows.append(dict(run=rd.name, task=int(tk[i]), y=inc/len(span), S_eta=span.lr.sum(), S_eta_m=span.eta_m.sum(),
                            S_eta_g=span.eta_g.sum(), tau=span.delta.sum(), lr=span.lr.mean(), g=span.gnorm.mean(),
                            gc=span.gnorm_clipped.mean(), m=span.m_hat_norm.mean(), v=span.sqrt_trv.mean(),
                            loss=span.loss.mean(), sip=span.step_in_phase.mean(), kind=int(span.kind.iloc[0]),
                            skipped=span.skipped.sum(), mf=(span.eta_m*np.sqrt(1146880)/span.sqrt_trv.clip(lower=1e-12)).sum()))
Wd, D3, Ph = pd.DataFrame(win_rows), pd.DataFrame(d3_rows), pd.DataFrame(phase_rows)
print(f"runs: {[r.name for r in runs]}; windows: {len(Wd)}; D3 intervals: {len(D3)}; phases: {len(Ph)}")

def r2(y, p):
    return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()
full = ["lr", "g", "gc", "m", "v", "loss", "sip", "kind", "task", "skipped"]
ladder = {"Ση (C3)": ["S_eta"], "Ση‖g̃‖ (C5b)": ["S_eta_g"], "Ση‖m̂‖ (C5d)": ["S_eta_m"],
          "câmp mediu C5d/√v̄": ["mf"], "Ση + Ση‖m̂‖": ["S_eta", "S_eta_m"]}
def ladder_table(df, ycol):
    out = {}
    for nm, cols in list(ladder.items()) + [("GBDT telemetrie completă", full)]:
        r = []
        for test in df.run.unique():
            tr, te = df.run != test, df.run == test
            mdl = (HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20,
                                                 random_state=0) if nm.startswith("GBDT") else LinearRegression())
            mdl.fit(df.loc[tr, cols], df.loc[tr, ycol]); r.append(r2(df.loc[te, ycol].to_numpy(), mdl.predict(df.loc[te, cols])))
        out[nm] = (np.mean(r), np.min(r))
    return pd.DataFrame(out, index=["R2 mediu", "R2 minim"]).T

if Wd.run.nunique() >= 2:
    print("\nRata lui τ pe ferestre de 8 pași (factori), R² în afara rulării:")
    print(ladder_table(Wd, "y").round(3).to_string())
    print("\nRata lui τ pe ΔW = 2·B·A (secundar):")
    print(ladder_table(Wd, "y_dW").round(3).to_string())
    if len(D3) > 50:
        print("\nD3 (schimbarea funcțională pe sonde), R² în afara rulării:")
        print(ladder_table(D3, "y").round(3).to_string())
    # where does the cheapest scalar fail? residual of OLS y ~ S_eta (leave one run out), by window after phase start
    Wd["res"] = np.nan
    for test in Wd.run.unique():
        tr, te = Wd.run != test, Wd.run == test
        m = LinearRegression().fit(Wd.loc[tr, ["S_eta"]], Wd.loc[tr, "y"]); Wd.loc[te, "res"] = Wd.loc[te, "y"] - m.predict(Wd.loc[te, ["S_eta"]])
    mu = Wd.y.mean()
    Wd["fereastra"] = pd.cut(Wd.win, [-1, 0, 1, 3, 1e9], labels=["1 (pașii 1-8)", "2", "3-4", ">=5"])
    Wd["faza"] = np.where(Wd.kind == 0, "calibrare", "curentă")
    print("\nReziduul lui 'y ~ Ση' (relativ la rata medie), după fereastra din fază și tipul fazei:")
    print(Wd.groupby(["faza", "fereastra"], observed=True).agg(n=("y", "size"), eroare_abs=("res", lambda r: r.abs().mean()/mu),
                                                             bias=("res", lambda r: r.mean()/mu)).round(3).to_string())
    # phase level: how much of tau per phase is the integral of the schedule?
    print("\nLa nivel de fază: R² (în afara rulării) al lui τ_fază din Ση_fază și din Ση‖m̂‖_fază:")
    for c in ["S_eta", "S_eta_m"]:
        r = [r2(Ph.loc[Ph.run == t, "tau"].to_numpy(), LinearRegression().fit(Ph.loc[Ph.run != t, [c]], Ph.loc[Ph.run != t, "tau"]).predict(Ph.loc[Ph.run == t, [c]]))
             for t in Ph.run.unique()]
        print(f"  {c}: mediu {np.mean(r):.3f}, minim {np.min(r):.3f}")
    print(f"\nPași săriți de GradScaler: {int(Wd.skipped.sum())} din {8*len(Wd)} pași în ferestre")
