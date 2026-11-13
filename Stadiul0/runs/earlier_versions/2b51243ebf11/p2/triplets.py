"""Offline construction of triplets (k, t0, t1), targets, competitors and c_e (protocol v0.3, sections 6-7).

Interval convention: an interval (t0, t1] covers the committed steps tau in (N(t0), N(t1)]. The per-step
arrays are indexed by life step i, where step i moves the state from N = i to N = i + 1, so the
interval sum is cs[N1] - cs[N0] with cs the cumulative sum starting at 0.

Usage: python -m p2.triplets RUN_DIR [RUN_DIR ...]   (writes triplets.parquet into each run folder)
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

CONFIG = Path(__file__).resolve().parent.parent / "config_stage0.yaml"


def default_max_dN():
    """T1 cap on dN from the analysis section of the configuration (None = no cap)."""
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    return (cfg.get("analysis") or {}).get("t1_max_dN")


def _cs(x):
    return np.concatenate([[0.0], np.cumsum(np.asarray(x, dtype=np.float64))])


def load_run(run_dir):
    d = Path(run_dir)
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    load = lambda name: dict(np.load(d / f"{name}.npz"))
    sched = json.loads((d / "schedule.json").read_text(encoding="utf-8"))
    return meta, load("steps"), load("evals"), load("episodes"), load("disp"), load("chunks"), load("world"), sched


def c6_stats(x, N0, N1):
    """C6: mean and population SD of x over the first and last W_eff steps of (N0, N1] (section 7)."""
    dN = N1 - N0
    W = min(16, dN // 4)
    if dN == 0 or W == 0:
        return 0.0, 0.0, 0.0, 0.0
    first = x[N0: N0 + W]
    last = x[N1 - W: N1]
    return first.mean(), first.std(ddof=0), last.mean(), last.std(ddof=0)


def build(run_dir, stride_key=None, max_dN="config"):
    """Triplets of one run. max_dN: cap on dN for inclusion ('config' = analysis.t1_max_dN; None = no cap).
    The uncapped inclusion and weights are kept as incl_nocap and w_nocap (sensitivity analysis)."""
    if max_dN == "config":
        max_dN = default_max_dN()
    meta, st, ev, eps, disp, ch, world, sched = load_run(run_dir)
    lam = meta["config"]["optim"]["weight_decay"]
    lr, B = st["lr"], st["batch"]
    cs = {
        "C2": _cs(st["tokens"]), "C3": _cs(lr), "C4": _cs(st["loss"]), "C5": _cs(st["gnorm_raw"]),
        "C5a": _cs(st["gnorm_clip"]), "C5b_g": _cs(lr * st["gnorm_raw"]), "C5b_gt": _cs(lr * st["gnorm_clip"]),
        "C5b_L": _cs(lr * st["loss"]), "C5c_sq": _cs(lr ** 2 * st["gnorm_clip"] ** 2), "C5c_work": _cs(st["gdot"]),
        "C5d": _cs(lr * st["mhat_norm"]), "C5e": _cs(st["mhat_norm"]), "C5f": _cs(lr * lam * st["theta_dec_norm"]),
        "C2b": _cs(lr / B), "C7a": _cs(st["boundary"]),
        "ce_D1": _cs(st["D1"]), "ce_D1_rel": _cs(st["D1_rel"]), "ce_D2": _cs(np.nan_to_num(st["D2"])),
    }
    if stride_key is None:
        keys = sorted({k.rsplit("_", 1)[0] for k in ch if k.endswith("_N")})
        stride_key = next(k for k in keys if k.endswith("_s0"))
    cN = ch[f"{stride_key}_N"].astype(np.int64)
    life = int(meta["life_steps"])
    chunk_arr = {}
    chunk_names = ["D3", "D4", "C10b"] + (["C10c"] if f"{stride_key}_C10c" in ch else [])   # C10c: runs after 6 Nov 2026
    for f in chunk_names:
        a = np.zeros(life + 1)
        a[cN] = ch[f"{stride_key}_{f}"]
        chunk_arr[f] = np.cumsum(a)                       # value at N = sum of chunks ending at or before N
    evN, evca = ev["N"].astype(np.int64), ev["ca"]
    LA, LB, AA, AB = ev["LA"], ev["LB"], ev["AA"], ev["AB"]
    kinds = world["kinds"]
    n_values = world["n_values"]
    ep_task = eps["task"].astype(int)
    ep_t0 = eps["t0"].astype(int)
    # first-exposure evaluation of each task and exposure counts, for tenure and prior exposures
    first_t0 = {}
    for i in np.argsort(ep_t0, kind="stable"):
        first_t0.setdefault(ep_task[i], ep_t0[i])
    rows = []
    disp_ep, disp_e = disp["ep"].astype(int), disp["e"].astype(int)
    dfields = [f for f in meta["disp_fields"]]
    for r in range(len(disp_ep)):
        ep, e1 = disp_ep[r], disp_e[r]
        k, e0 = ep_task[ep], ep_t0[ep]
        N0, N1 = int(evN[e0]), int(evN[e1])
        dN = N1 - N0
        row = {"ep": ep, "task": k, "e0": e0, "e1": e1, "N0": N0, "N1": N1, "dN": dN,
               "C0": evca[e1] - evca[e0] - dN,            # pause ticks (Deep Review D1: was dc_a, identical to dN without pauses)
               "F_A": LA[e1, k] - LA[e0, k], "F_B": LB[e1, k] - LB[e0, k],
               "dAcc_A": AA[e0, k] - AA[e1, k], "AB0": AB[e0, k]}
        for name, c in cs.items():
            row[name] = c[N1] - c[N0]
        for name in chunk_names:
            key = f"ce_{name}" if name not in ("C10b", "C10c") else name
            row[key] = chunk_arr[name][N1] - chunk_arr[name][N0]
        row["C10"] = ev["L_R"][e1] - ev["L_R"][e0]
        row["C6b_theta"] = ev["theta_norm"][e1] - ev["theta_norm"][e0]
        row["C6b_v"] = ev["sqrt_trv"][e1] - ev["sqrt_trv"][e0]
        for tag, x in [("pre", st["dpre_norm"]), ("post", st["D1"])]:
            m1, s1, m2, s2 = c6_stats(x, N0, N1)
            row.update({f"C6_{tag}_m_first": m1, f"C6_{tag}_sd_first": s1,
                        f"C6_{tag}_m_last": m2, f"C6_{tag}_sd_last": s2})
        for i, f in enumerate(dfields):
            row[f"Disp_{f}" if f != "T2" else "T2"] = disp[f][r]
        # covariates X_cov (section 7)
        row.update({
            "x_rule": int(kinds[k]), "x_log_nvalues": np.log(n_values[k]),
            "x_LB0": LB[e0, k], "x_AB0": AB[e0, k], "x_prior_LB": eps["prior_LB"][ep],
            "x_overlap": eps["overlap"][ep], "x_N0": N0, "x_tenure": N0 - int(evN[first_t0[k]]),
            "x_prior_exposures": int(np.sum((ep_task == k) & (ep_t0 < e0))),
            "x_K_active": int(np.sum(~np.isnan(LA[e0]))),
            "x_theta_norm0": ev["theta_norm"][e0], "x_sqrt_trv0": ev["sqrt_trv"][e0],
            "x_LR0": ev["L_R"][e0],                       # Deep Review D5: L_R(t0) in X_cov
        })
        if "LAc" in ev:                                   # F^clip (Deep Review A3), sensitivity target
            row["F_A_clip"] = ev["LAc"][e1, k] - ev["LAc"][e0, k]
            row["F_B_clip"] = ev["LBc"][e1, k] - ev["LBc"][e0, k]
        rows.append(row)
    df = pd.DataFrame(rows)
    # rates (section 7): Z / max(dN, 1)
    den = np.maximum(df["dN"].to_numpy(), 1)
    for z in ["C2", "C2b", "C3", "C4", "C5", "C5a", "C5b_g", "C5b_gt", "C5b_L", "C5c_sq", "C5c_work", "C5d",
              "C5e", "C5f", "C10", "C10b"] + (["C10c"] if "C10c" in df else []) + \
             [c for c in df.columns if c.startswith("ce_") or c.startswith("Disp_")]:
        df[f"rate_{z}"] = df[z] / den
    # inclusion (section 6)
    comp = df["AB0"] >= 0.90
    gap = (df["dN"] >= 64) | ((df["dN"] == 0) & (df["C0"] >= 64))
    cap = np.ones(len(df), bool) if max_dN is None else (df["dN"] < max_dN).to_numpy()
    df["incl_nocap"] = comp & gap
    df["incl"] = comp & gap & cap
    df["excl_reason"] = np.where(~comp, "competence<0.90", np.where(~gap, "interval<64",
                                 np.where(~cap, f"dN>={max_dN}", "")))
    # weights: equal total weight per valid episode (for the capped and for the uncapped inclusion)
    for flag, wcol in [("incl", "w"), ("incl_nocap", "w_nocap")]:
        inc = df[df[flag]]
        E = inc["ep"].nunique()
        M = inc.groupby("ep")["ep"].transform("size")
        df[wcol] = 0.0
        df.loc[inc.index, wcol] = 1.0 / (E * M)
    df["t1_max_dN"] = -1 if max_dN is None else int(max_dN)
    df["family"], df["seed"] = meta["family"], meta["seed"]
    return df, meta


def weighted_corr(x, y, w):
    w = w / w.sum()
    mx, my = (w * x).sum(), (w * y).sum()
    cov = (w * (x - mx) * (y - my)).sum()
    return cov / np.sqrt((w * (x - mx) ** 2).sum() * (w * (y - my) ** 2).sum())


def run_summary(df, meta):
    inc = df[df["incl"]]
    ex = df.loc[~df["incl"], "excl_reason"].value_counts().to_dict()
    eps = df.groupby("ep").agg(task=("task", "first"), AB0=("AB0", "first"))
    kinds = np.array([df.loc[df["task"] == t, "x_rule"].iloc[0] for t in eps["task"]])
    out = {
        "family": meta["family"], "seed": meta["seed"],
        "childhood_gate": meta["childhood"]["gate_passed"], "childhood_acc": round(meta["childhood"]["acc_reference"], 4),
        "childhood_acc_rule": (round(meta["childhood"]["acc_reference_rule"], 4)
                               if meta["childhood"]["acc_reference_rule"] is not None else None),
        "episodes": int(len(eps)), "valid_episodes": int(inc["ep"].nunique()),
        "episodes_competent_fact": int(((eps["AB0"] >= 0.9) & (kinds == 0)).sum()),
        "episodes_competent_rule": int(((eps["AB0"] >= 0.9) & (kinds == 1)).sum()),
        "episodes_fact": int((kinds == 0).sum()), "episodes_rule": int((kinds == 1).sum()),
        "triplets": int(len(df)), "included": int(len(inc)), "excluded": ex,
    }
    if len(inc) > 2:
        w = inc["w"].to_numpy()
        out["r_AB"] = round(float(weighted_corr(inc["F_A"].to_numpy(), inc["F_B"].to_numpy(), w)), 4)
        out["F_A_mean"] = round(float((w * inc["F_A"]).sum() / w.sum()), 4)
        out["F_A_sd"] = round(float(np.sqrt((w * (inc["F_A"] - (w * inc["F_A"]).sum() / w.sum()) ** 2).sum() / w.sum())), 4)
        out["dAcc_A_mean"] = round(float((w * inc["dAcc_A"]).sum() / w.sum()), 4)
        rho = inc["rate_ce_D1"].to_numpy()
        out["rate_D1_cv"] = round(float(rho.std() / rho.mean()), 4) if rho.mean() > 0 else None
    t = meta["timing_s"]
    out["timing_s"] = t
    out["peak_rss_mb"] = meta["peak_rss_mb"]
    return out


def main(argv):
    for d in argv:
        df, meta = build(d)
        df.to_parquet(Path(d) / "triplets.parquet")
        print(json.dumps(run_summary(df, meta), indent=1, default=float))


if __name__ == "__main__":
    main(sys.argv[1:])
