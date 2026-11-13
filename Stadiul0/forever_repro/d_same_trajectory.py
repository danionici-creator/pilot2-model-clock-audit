# Option (d) of the 8 Nov 2026 colloquium (Colocviu/Verificare_raspunsuri_2026-11-08.md): zero-GPU, POST HOC analysis of
# R2's drift logs, outputs fixed in preinregistrare_FOREVER_repetari_2026-11-08.md (version 3) BEFORE this script ran.
# On R2's trajectory both clocks are logged: tau = the eta*|m_hat| clock that drove the replays, tau_true = sum |dtheta|.
#  (1) validation: thresholds mult*day on the eta clock (day = clock at step 24) must reproduce R2's actual trigger steps;
#  (2) counterfactual: where tau_true (calibrated the same way) would cross its thresholds on the SAME trajectory;
#      only up to and including the first trigger index where the two differ is the comparison clean;
#  (3) ratio |dtheta| / eta-increment by position since the last phase start (phase starts: step 1, step 25, and the
#      step after every actual trigger), normalised by the task median, to see whether divergence sits after restarts;
#  (4) per-task R^2 (8-step windows, same as r2_reconstruction.py) with and without the windows that contain a phase start.
# Usage: python -I d_same_trajectory.py ; writes runs/forever_d_same_trajectory.json
import csv, json, sys
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROOT = HERE / "ckpt_eta_m" / "Qwen_Qwen3-0.6Blora_cl_dataset_id_4"
MULTS = [1, 2, 4, 7, 15, 30, 60, 90, 120]
ACTUAL = {"1-amazon": [24, 50, 104, 192], "2-yahoo": [24, 48, 96, 178], "3-agnews": [24, 47, 96, 193]}  # R2 logs
R1_TAU = {"1-amazon": [24, 48, 100, 185], "2-yahoo": [24, 46, 87, 160], "3-agnews": [24, 47, 93, 160]}  # R1 logs


def crossings(cum, steps, day):
    out = []
    for m in MULTS:
        idx = np.where(cum >= m * day - 1e-15)[0]
        if len(idx) == 0:
            break
        out.append(int(steps[idx[0]]))
    return out


def r2(x, y):
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    return float(1 - (res ** 2).sum() / ((y - y.mean()) ** 2).sum())


out = {}
for t, act in ACTUAL.items():
    rows = list(csv.DictReader(open(ROOT / t / "drift_log.csv", encoding="utf-8")))
    steps = np.array([int(r["step"]) for r in rows])
    d = np.array([float(r["delta_t"]) for r in rows])
    eta = np.array([float(r["tau"]) for r in rows])
    true = np.array([float(r["tau_true"]) for r in rows])
    i24 = int(np.where(steps == 24)[0][0])
    eta_tr = [s for s in crossings(eta, steps, eta[i24]) if s <= 313][: len(act)]
    tau_tr = [s for s in crossings(true, steps, true[i24]) if s <= 313][: len(act)]
    first_diff = next((k for k in range(min(len(eta_tr), len(tau_tr))) if eta_tr[k] != tau_tr[k]), None)
    clean = tau_tr[: first_diff + 1] if first_diff is not None else tau_tr
    # (3) ratio by position since the last phase start
    inc = np.diff(np.concatenate([[0.0], eta]))
    starts = sorted({1, 25} | {s + 1 for s in act[1:]})
    pos = np.array([s - max(p for p in starts if p <= s) for s in steps])
    ok = inc > 0
    ratio = np.where(ok, d / np.where(ok, inc, 1), np.nan)
    med = np.nanmedian(ratio)
    bins = {"0": pos == 0, "1": pos == 1, "2": pos == 2, "3-4": (pos >= 3) & (pos <= 4), "5-9": (pos >= 5) & (pos <= 9),
            "10+": pos >= 10}
    by_pos = {k: (float(np.nanmedian(ratio[m]) / med) if np.any(m & ok) else None) for k, m in bins.items()}
    n_by_pos = {k: int(np.sum(m & ok)) for k, m in bins.items()}
    # (4) R^2 with / without windows containing a phase start
    nb = len(d) // 8
    y = d[: nb * 8].reshape(nb, 8).sum(1); x = inc[: nb * 8].reshape(nb, 8).sum(1)
    has_start = np.array([any(s in starts for s in steps[k * 8:(k + 1) * 8]) for k in range(nb)])
    out[t] = {"validation_eta_triggers_recomputed": eta_tr, "eta_triggers_actual_R2": act,
              "validation_ok": eta_tr == act, "counterfactual_tau_triggers_same_trajectory": tau_tr,
              "first_differing_index": first_diff, "clean_part": clean, "R1_tau_triggers_other_trajectory": R1_TAU[t],
              "ratio_dtheta_over_eta_inc_by_position_rel_median": by_pos, "n_by_position": n_by_pos,
              "R2_all_windows": r2(x, y), "R2_without_phase_start_windows": r2(x[~has_start], y[~has_start]),
              "windows_with_start": int(has_start.sum()), "windows_total": int(nb)}
    o = out[t]
    print(f"{t}: eta recomputed {eta_tr} (actual {act}, ok={o['validation_ok']}); tau on same trajectory {tau_tr}; "
          f"R1 tau {R1_TAU[t]}; first differing index {first_diff}")
    print(f"   ratio |dtheta|/eta-inc by position (rel. to median): "
          + ", ".join(f"{k}: {v:.2f} (n={n_by_pos[k]})" if v is not None else f"{k}: -" for k, v in by_pos.items()))
    print(f"   R2 all windows {o['R2_all_windows']:.3f}; without {o['windows_with_start']} phase-start windows "
          f"{o['R2_without_phase_start_windows']:.3f}")
json.dump(out, open(HERE.parent / "runs" / "forever_d_same_trajectory.json", "w"), indent=1)
