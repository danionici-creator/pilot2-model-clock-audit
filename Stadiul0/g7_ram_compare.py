# G7 after the RAM upgrade: are the reruns bit-identical to the tech3 runs made with one module?
# Compares (1) the array hashes stored in meta.json, (2) hashes recomputed now from the .npz files of both runs,
# (3) wall time and ms per step. Run from the Stadiul0 folder: python <this file>
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path.cwd()))
from p2.run import array_hashes

ARRAYS = ["steps", "evals", "episodes", "disp", "chunks", "world"]
R = Path("runs")
pairs = [("tech3_lr3e-4", "g7_ram_lr3e-4"), ("tech3_lr2e-4", "g7_ram_lr2e-4")]
ok_all = True
for old, new in pairs:
    for run in ["F2_s9004", "F3_s9004"]:
        a, b = R / old / run, R / new / run
        ma = json.loads((a / "meta.json").read_text(encoding="utf-8"))
        mb = json.loads((b / "meta.json").read_text(encoding="utf-8"))
        same_cfg = {k: v for k, v in ma["config"].items() if k not in ("analysis", "meta")} == \
                   {k: v for k, v in mb["config"].items() if k not in ("analysis", "meta")}
        res = []
        for n in ARRAYS:
            stored = ma["sha256_arrays"][n] == mb["sha256_arrays"][n]
            with np.load(a / f"{n}.npz") as za, np.load(b / f"{n}.npz") as zb:
                ha = array_hashes({k: za[k] for k in za.files}); hb = array_hashes({k: zb[k] for k in zb.files})
            res.append((n, stored, ha == hb, ha == ma["sha256_arrays"][n], hb == mb["sha256_arrays"][n]))
        ok = same_cfg and all(all(r[1:]) for r in res)
        ok_all &= ok
        ta, tb = ma["timing_s"], mb["timing_s"]
        print(f"{old} -> {new} {run}: config equal={same_cfg}; " +
              "; ".join(f"{n}: {'=' if s and r else 'DIFF'}" for n, s, r, _, _ in res) + f"  => {'PASS' if ok else 'FAIL'}")
        print(f"    timing old: {ta}\n    timing new: {tb}\n    peak RSS MB old/new: {ma.get('peak_rss_mb')} / {mb.get('peak_rss_mb')}")
for old, new in pairs:
    la = json.loads((R / old / "launch_summary.json").read_text(encoding="utf-8"))
    lb = json.loads((R / new / "launch_summary.json").read_text(encoding="utf-8"))
    print(f"wall {old}: {la['total_wall_s']} s ({[r.get('wall_s') for r in la['runs']]}); {new}: {lb['total_wall_s']} s ({[r.get('wall_s') for r in lb['runs']]})")
print("G7 after RAM upgrade:", "PASS (all arrays bit-identical)" if ok_all else "FAIL")
