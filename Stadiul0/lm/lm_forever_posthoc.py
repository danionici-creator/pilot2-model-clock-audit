"""lmtech1, analyses ADDED AFTER seeing the pre-fixed G2 output (6 Nov 2026) - exploratory, labelled as such.
    python -I lm_forever_posthoc.py ..\\runs\\lmtech1
Blind to T1 (evals.npz never opened).
(1) Sum eta over APPLIED steps only (GradScaler skips change nothing but still carry an eta in the log).
(2) Phase level, with duration controlled: tau_phase from steps alone, from sum eta, from sum eta applied.
(3) The FOREVER trigger: within each task (tasks >= 1), the counted step at which tau crosses d * model_day, versus the
    step at which a schedule-only clock (cumulative applied eta, normalised by its own calibration value) crosses d.
"""
import sys, numpy as np, pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
sys.stdout.reconfigure(encoding="utf-8")
root = Path(sys.argv[1]); W = 8
def r2(y, p): return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()
def loro(df, cols, y):
    out = []
    for t in df.run.unique():
        tr, te = df.run != t, df.run == t
        out.append(r2(df.loc[te, y].to_numpy(), LinearRegression().fit(df.loc[tr, cols], df.loc[tr, y]).predict(df.loc[te, cols])))
    return np.mean(out), np.min(out)
win, ph, trig = [], [], []
for rd in sorted(p for p in root.iterdir() if (p/"meta.json").exists()):
    z = np.load(rd/"steps.npz"); S = pd.DataFrame(z["data"], columns=list(z["cols"]))
    S["eta_app"] = S.lr * (1 - S.skipped); S["eta_m"] = S.lr * S.m_hat_norm
    C = S[S.counted == 1]
    for (task, p), g in C.groupby(["task", "phase"]):
        g = g.sort_values("gstep")
        ph.append(dict(run=rd.name, kind=int(g.kind.iloc[0]), n=len(g), tau=g.delta.sum(), S_eta=g.lr.sum(), S_eta_app=g.eta_app.sum()))
        for j in range(len(g) // W):
            w = g.iloc[j*W:(j+1)*W]
            win.append(dict(run=rd.name, y=w.delta.mean(), S_eta=w.lr.sum(), S_eta_app=w.eta_app.sum(), S_eta_m=w.eta_m.sum(),
                            skipped=w.skipped.sum()))
    for task, g in C.groupby("task"):
        if task == 0:
            continue
        g = g.sort_values("gstep"); tau = g.delta.cumsum().to_numpy(); eta = g.eta_app.cumsum().to_numpy()
        calib = g.kind.to_numpy() == 0; day_tau, day_eta = tau[calib][-1], eta[calib][-1]
        for d in (2, 4, 7, 15, 30, 60, 90, 120):
            i_tau = np.argmax(tau >= d * day_tau) if (tau >= d * day_tau).any() else None
            i_eta = np.argmax(eta >= d * day_eta) if (eta >= d * day_eta).any() else None
            trig.append(dict(run=rd.name, task=task, d=d, step_tau=i_tau, step_eta=i_eta, n=len(g)))
Wd, Ph, Tr = pd.DataFrame(win), pd.DataFrame(ph), pd.DataFrame(trig)
print("(1) Ferestre de 8 pași, R² în afara rulării (mediu, minim):")
for nm, cols in [("Ση (toți pașii)", ["S_eta"]), ("Ση aplicat (fără pașii săriți)", ["S_eta_app"]),
                 ("Ση aplicat + nr. pași săriți", ["S_eta_app", "skipped"]), ("Ση‖m̂‖", ["S_eta_m"])]:
    m, lo = loro(Wd, cols, "y"); print(f"  {nm:32s} {m:.3f}  {lo:.3f}")
print(f"  ferestre cu cel puțin un pas sărit: {100*(Wd.skipped > 0).mean():.1f}%")
print("\n(2) La nivel de fază (fazele curente și de calibrare), R² în afara rulării:")
for nm, cols in [("pași (n)", ["n"]), ("Ση", ["S_eta"]), ("Ση aplicat", ["S_eta_app"]), ("n + Ση aplicat", ["n", "S_eta_app"])]:
    m, lo = loro(Ph, cols, "tau"); print(f"  {nm:16s} {m:.3f}  {lo:.3f}")
Ph["tau_per_step"] = Ph.tau / Ph.n; Ph["eta_per_step"] = Ph.S_eta_app / Ph.n
m, lo = loro(Ph, ["eta_per_step"], "tau_per_step"); print(f"  rata pe fază (τ/n) din (Ση aplicat/n): {m:.3f}  {lo:.3f}   <- durata scoasă")
print("\n(3) Declanșarea repetițiilor (sarcinile 1-9): pasul la care τ atinge d·zi față de pasul ceasului doar din program")
T = Tr.dropna(subset=["step_tau"]).copy()
T["ambele"] = T.step_eta.notna()
T["dif"] = np.where(T.ambele, T.step_eta.astype(float) - T.step_tau.astype(float), np.nan)
g = T.groupby("d").agg(praguri_tau=("step_tau", "size"), atinse_si_de_program=("ambele", "sum"),
                       pas_tau_median=("step_tau", "median"), dif_mediana=("dif", "median"),
                       dif_abs_medie=("dif", lambda x: np.nanmean(np.abs(x))))
print(g.round(1).to_string())
