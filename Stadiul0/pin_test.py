# Deep Review B7 (6 Nov 2026): does pinning the 4 workers to the P-cores change throughput? Run from Stadiul0:
#   python pin_test.py
# Three conditions in sequence, each = 4 childhood probes (3,072 steps, the same work as in a run) in parallel:
#   free (Windows scheduler), P-cores (logical 0, 2, 4, 6: one thread per physical P-core), E-cores (logical 8-11).
# Assumes the usual Alder Lake numbering (P-core threads first); the result itself shows whether it holds.
import ctypes, json, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
COND = {"liber": None, "nuclee_P": [1 << 0, 1 << 2, 1 << 4, 1 << 6], "nuclee_E": [1 << 8, 1 << 9, 1 << 10, 1 << 11]}
res = {}
for name, masks in COND.items():
    if (HERE / "runs" / "_HW_STOP").exists():
        print("OPRIT de paznic"); sys.exit(3)
    ps, t0 = [], time.time()
    for i in range(4):
        p = subprocess.Popen([sys.executable, "calib_probe.py", "childhood", "--lr", "3e-4", "--seed", str(9200 + i),
                              "--family", "F2"], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if masks:
            ctypes.windll.kernel32.SetProcessAffinityMask(ctypes.c_void_p(int(p._handle)), ctypes.c_size_t(masks[i]))
        ps.append(p)
    outs = [json.loads(p.communicate()[0].strip().splitlines()[-1]) for p in ps]
    res[name] = {"wall_total_s": round(time.time() - t0, 1), "wall_each_s": [o["wall_s"] for o in outs],
                 "acc_reference": [round(o["childhood"]["acc_reference"], 4) for o in outs]}
    print(name, json.dumps(res[name]), flush=True)
(HERE / "runs" / "pin_test_2026-11-06.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
same = all(res[k]["acc_reference"] == res["liber"]["acc_reference"] for k in res)
print("acuratetea identica in toate conditiile (determinism, independent de nuclee):", same)
