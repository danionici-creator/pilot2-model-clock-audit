# T-A analysis, as fixed in preinregistrare_TA_TB_2026-11-06.md. Run from Stadiul0: python -I ta_analysis.py
# E1 final average accuracy (last row of evals.npz); E2 BWT; E3 mean old-task accuracy just before each final replay
# (evals_pre.npz, tasks 1-9); E4 replay counts and |difference of the trigger step| vs tau (counted steps of the task
# before the j-th replay; median over tasks, per threshold index). Paired by seed: tau vs eta_m, eta, steps.
import json, sys, numpy as np
from pathlib import Path
from scipy import stats
sys.stdout.reconfigure(encoding="utf-8")
R = Path(__file__).resolve().parent / "runs" / "ta"
CLOCKS = ["tau", "eta_m", "eta", "steps"]; DELTA = 0.02
seeds = sorted({p.name for c in CLOCKS for p in (R / c).glob("s*") if (p / "meta.json").exists()})
seeds = [s for s in seeds if all((R / c / s / "meta.json").exists() for c in CLOCKS)]   # complete seed sets only

def endpoints(rd):
    e = np.load(rd / "evals.npz"); acc = e["acc"]; n = acc.shape[1]
    E1 = float(np.nanmean(acc[-1])); E2 = float(np.mean([acc[-1, t] - acc[t, t] for t in range(n - 1)]))
    p = np.load(rd / "evals_pre.npz"); E3 = float(np.mean([np.nanmean(p["acc"][i, :int(t)]) for i, t in enumerate(p["task"])]))
    z = np.load(rd / "steps.npz"); cols = list(z["cols"]); D = z["data"]; ph = z["phases"]
    task, gstep, counted = D[:, cols.index("task")], D[:, cols.index("gstep")], D[:, cols.index("counted")]
    trig = {}
    for t_, kind, start, *_ in ph:
        if kind == 2:                                     # mid-task replay
            trig.setdefault(int(t_), []).append(int(((task == t_) & (counted == 1) & (gstep <= start)).sum()))
    return dict(E1=E1, E2=E2, E3=E3, trig=trig, n_replay=sum(len(v) for v in trig.values()))

V = {c: {s: endpoints(R / c / s) for s in seeds} for c in CLOCKS}
print(f"semințe complete: {seeds}")
for c in CLOCKS:
    a = V[c]
    print(f"  {c:6s} E1 {np.mean([a[s]['E1'] for s in seeds]):.4f}  E2 {np.mean([a[s]['E2'] for s in seeds]):+.4f}  "
          f"E3 {np.mean([a[s]['E3'] for s in seeds]):.4f}  repetiții medii {np.mean([a[s]['n_replay'] for s in seeds]):.1f}")
out = {}
for c in CLOCKS[1:]:
    d = np.array([V["tau"][s]["E1"] - V[c][s]["E1"] for s in seeds]); n = len(d)
    half = stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n) if n > 1 else np.inf
    lo, hi = d.mean() - half, d.mean() + half
    sep = {}
    for j in range(3):
        diffs = [abs(V["tau"][s]["trig"][t][j] - V[c][s]["trig"][t][j]) for s in seeds for t in V["tau"][s]["trig"]
                 if t in V[c][s]["trig"] and len(V["tau"][s]["trig"][t]) > j and len(V[c][s]["trig"][t]) > j]
        if diffs:
            sep[f"d_index_{j}"] = float(np.median(diffs))
    equiv_sched = bool(sep) and all(v <= 2 for v in sep.values())
    verdict = ("τ SUPERIOR" if d.mean() >= DELTA and lo > 0 else
               "ECHIVALENȚĂ PRACTICĂ" if (lo > -DELTA and hi < DELTA) else "NECONCLUDENT")
    out[c] = dict(mean_diff=float(d.mean()), ci=[float(lo), float(hi)], separation=sep, schedule_equivalent=equiv_sched,
                  verdict=verdict, dE2=float(np.mean([V["tau"][s]["E2"] - V[c][s]["E2"] for s in seeds])),
                  dE3=float(np.mean([V["tau"][s]["E3"] - V[c][s]["E3"] for s in seeds])))
    print(f"\nτ față de {c}: E1(τ) − E1({c}) = {d.mean():+.4f}, IC 95% [{lo:+.4f}; {hi:+.4f}] -> {verdict}")
    print(f"  separarea declanșărilor (mediana |Δ pas|, pe indicele pragului): {sep} -> "
          f"{'ECHIVALENTE ca planificare (≤ 2 pași)' if equiv_sched else 'separate'}")
    print(f"  ΔE2 (BWT) {out[c]['dE2']:+.4f}; ΔE3 (vechi, înainte de repetiția finală) {out[c]['dE3']:+.4f}")
(Path(__file__).resolve().parent / "runs" / "ta_verdict.json").write_text(json.dumps({"seeds": seeds, **out}, indent=1), encoding="utf-8")
