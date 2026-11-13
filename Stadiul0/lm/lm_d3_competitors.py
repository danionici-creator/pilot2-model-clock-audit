"""T-C (colloquium 6 Nov 2026): same-cost competitors of D3 on the LM arm, from the stored probe outputs.

    python -I lm_d3_competitors.py ..\\runs\\lmtech1 ..\\runs\\lmtech2 ..\\runs\\lmsens_bf16 ..\\runs\\lmsens_a32

Criteria fixed before running: tc_criterii.md. Blind to T1: reads probes.npz, steps.npz and meta.json only.
D3 intervals exactly as lm_forever_g2.py (consecutive probes of one task, no replay step inside, y = RMS change of
the 128 x 31 log-probabilities per counted step). The probe answer words are regenerated from the world seed with
the same generator calls as lm_forever_run.make_world (no tokenizer needed: 31 single-token words, as logged).
"""
import json, sys
import numpy as np, pandas as pd, torch
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression

sys.stdout.reconfigure(encoding="utf-8")
LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"        # as lm_forever_run.py
N_WORDS = 31


def probe_answers(seed, n_tasks, per_task, n_probe):
    g = torch.Generator().manual_seed(seed * 10 + 2)
    codes, seen = [], set()
    while len(codes) < n_tasks * per_task + n_probe:
        c = "".join(LETTERS[j] for j in torch.randint(len(LETTERS), (6,), generator=g).tolist())
        if c not in seen:
            seen.add(c); codes.append(c)
    ans = torch.randint(N_WORDS, (len(codes),), generator=g)
    return ans[n_tasks * per_task: n_tasks * per_task + n_probe].numpy()


def rows_of(rd):
    meta = json.loads((rd / "meta.json").read_text(encoding="utf-8")); cfg = meta["config"]
    z = np.load(rd / "steps.npz"); S = pd.DataFrame(z["data"], columns=list(z["cols"]))
    S["eta_m"] = S.lr * S.m_hat_norm; S["eta_g"] = S.lr * S.gnorm_clipped
    C = S[S.counted == 1]
    P = np.load(rd / "probes.npz"); gs, tk, lp = P["gstep"], P["task"], P["logp"].astype(np.float64)
    a = probe_answers(cfg["seed"], cfg["tasks"], cfg["per_task"], cfg["n_probe"])
    pr = np.exp(lp); ii = np.arange(lp.shape[1])
    tgt_lp = lp[:, ii, a]; tgt_p = pr[:, ii, a]; H = -(pr * lp).sum(-1)
    rep = set(S.gstep[S.counted == 0].astype(int))
    out = []
    for i in range(1, len(gs)):
        if tk[i] != tk[i - 1]:
            continue
        span = C[(C.gstep > gs[i - 1]) & (C.gstep <= gs[i])]
        if len(span) == 0 or any(gs[i - 1] < s <= gs[i] for s in rep):
            continue
        n = len(span); d = lp[i] - lp[i - 1]
        out.append(dict(run=rd.name, y=float(np.sqrt((d ** 2).mean(axis=1).mean())) / n,
                        c10c=float(np.abs(tgt_lp[i] - tgt_lp[i - 1]).mean()) / n,
                        p=float(np.abs(tgt_p[i] - tgt_p[i - 1]).mean()) / n,
                        h=float(np.abs(H[i] - H[i - 1]).mean()) / n,
                        l1=float(np.abs(d).mean()) / n,
                        S_eta_m=span.eta_m.sum(), lr=span.lr.mean(), g=span.gnorm.mean(), gc=span.gnorm_clipped.mean(),
                        m=span.m_hat_norm.mean(), v=span.sqrt_trv.mean(), loss=span.loss.mean(),
                        sip=span.step_in_phase.mean(), kind=int(span.kind.iloc[0]), task=int(tk[i]),
                        skipped=span.skipped.sum()))
    return out


def r2(y, p):
    return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()


full = ["lr", "g", "gc", "m", "v", "loss", "sip", "kind", "task", "skipped"]
models = {"(a) C10c_LM": ["c10c"], "(b) C10c_LM + P_LM + H_LM": ["c10c", "p", "h"],
          "(c) Ση‖m̂‖ + C10c_LM + P_LM + H_LM": ["S_eta_m", "c10c", "p", "h"],
          "L1_LM (aproape-duplicat, nefolosit la verdict)": ["l1"],
          "(d) GBDT telemetrie + cei trei": full + ["c10c", "p", "h"]}
verdict_b = []
for arg in sys.argv[1:]:
    root = Path(arg); runs = sorted(p for p in root.iterdir() if (p / "meta.json").exists())
    D = pd.DataFrame([r for rd in runs for r in rows_of(rd)])
    print(f"\n== {root.name}: runs {[r.name for r in runs]}; D3 intervals {len(D)}")
    for nm, cols in models.items():
        rr = []
        for test in D.run.unique():
            tr, te = D.run != test, D.run == test
            mdl = (HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=20,
                                                 random_state=0) if nm.startswith("(d)") else LinearRegression())
            mdl.fit(D.loc[tr, cols], D.loc[tr, "y"]); rr.append(r2(D.loc[te, "y"].to_numpy(), mdl.predict(D.loc[te, cols])))
        print(f"  {nm:48s} R2 mediu {np.mean(rr):.3f}  minim {np.min(rr):.3f}")
        if nm.startswith("(b)"):
            verdict_b.append(np.mean(rr))
v = np.array(verdict_b)
print("\nVerdict (criteriul fixat, modelul b):",
      "RECONSTRUIT de concurenții de același cost" if (v >= 0.90).all() else
      "DISTINCT de concurenții de același cost" if (v < 0.90).all() else "MIXT", "| R2 (b) pe configurații:", np.round(v, 3))
