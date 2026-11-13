# The quantities are preregistered secondaries; only this script is later. Written on 9 Nov 2026 so that the S2 numbers quoted in the closure report
# (section 5.2: replay triggers and old-task loss) can be recomputed from the archive. On 7 Nov the same numbers were
# printed by a command typed by hand and saved as runs/sni_S2_secundar.log; this script reproduces that file byte for byte.
# The secondary quantities are those listed in preinregistrare_SuperNI_2026-11-07.md, with the definitions of ta_analysis.py:
#   old-task loss before the final replay: mean over tasks 1-4 of the mean test loss on the earlier tasks (evals_pre.npz);
#   |difference of the trigger step|: counted steps of a task before each mid-task replay, tau versus eta_m, median per seed;
#   replays: number of mid-task replays (phase kind 2) per run.
# Usage, from Stadiul0:  python -I sni_s2_secondary.py   (prints only; writes nothing)
import sys
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
R = Path(__file__).resolve().parent / "runs" / "sni"


def info(rd):
    p = np.load(rd / "evals_pre.npz")
    old = float(np.mean([np.nanmean(p["loss"][i, :int(t)]) for i, t in enumerate(p["task"])]))
    z = np.load(rd / "steps.npz"); cols = list(z["cols"]); D = z["data"]; ph = z["phases"]
    task, gstep, counted = D[:, cols.index("task")], D[:, cols.index("gstep")], D[:, cols.index("counted")]
    trig = {}
    for t_, kind, start, *_ in ph:
        if kind == 2:  # mid-task replay
            trig.setdefault(int(t_), []).append(int(((task == t_) & (counted == 1) & (gstep <= start)).sum()))
    return old, trig


for s in ["s7401", "s7402", "s7403"]:
    a, ta = info(R / "tau" / s); b, tb = info(R / "eta_m" / s)
    diffs = [abs(x - y) for t in ta if t in tb for x, y in zip(ta[t], tb[t])]
    print(f"{s} | pierderea pe sarcinile vechi înainte de repetiția finală: τ {a:.4f} eta_m {b:.4f} | "
          f"|Δ pas declanșare| mediana {np.median(diffs):.1f} | repetiții τ / eta_m {sum(map(len, ta.values()))} / "
          f"{sum(map(len, tb.values()))}")
