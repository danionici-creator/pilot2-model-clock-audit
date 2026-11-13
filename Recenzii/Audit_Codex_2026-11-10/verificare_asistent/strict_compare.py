# Strict JSON comparison (A01): same structure (incl. empty containers), same types, finite<->finite, NaN only vs NaN.
import json, math, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SC = Path(sys.argv[1]); ORIG = Path(r"D:\Time\02_Pilot2\Stadiul0")
def cmp(a, b, p=""):
    if type(a) is not type(b):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
            pass
        else:
            return [f"{p}: type {type(a).__name__} vs {type(b).__name__}"]
    if isinstance(a, dict):
        if a.keys() != b.keys(): return [f"{p}: keys differ {sorted(set(a)^set(b))[:5]}"]
        return [e for k in a for e in cmp(a[k], b[k], f"{p}/{k}")]
    if isinstance(a, list):
        if len(a) != len(b): return [f"{p}: length {len(a)} vs {len(b)}"]
        return [e for i in range(len(a)) for e in cmp(a[i], b[i], f"{p}[{i}]")]
    if isinstance(a, float) or isinstance(b, float):
        fa, fb = math.isfinite(a), math.isfinite(b)
        if fa != fb or (not fa and not (math.isnan(a) and math.isnan(b)) and a != b): return [f"{p}: {a!r} vs {b!r}"]
        if fa and abs(a - b) / max(1.0, abs(a)) > 1e-9: return [f"{p}: {a!r} vs {b!r}"]
        return []
    return [] if a == b else [f"{p}: {a!r} vs {b!r}"]
jobs = [(["r2_reconstruction.py"], "runs/forever_repro_r2_reconstruction.json"),
        (["r2_reconstruction_arm.py", "eta_m"], "runs/forever_repetari_r2_eta_m.json"),
        (["r2_reconstruction_arm.py", "eta_m_A1"], "runs/forever_repetari_r2_eta_m_A1.json"),
        (["d_same_trajectory.py"], "runs/forever_d_same_trajectory.json"),
        (["rep_verdict.py"], "runs/forever_repetari_verdict.json"),
        (["eval_noise_summary.py"], "runs/forever_eval_noise_posthoc.json")]
for args, j in jobs:
    p = subprocess.run([sys.executable, "-I", "-X", "utf8"] + args, cwd=SC / "forever_repro", capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print(f"[RC {p.returncode}] {args}: {p.stderr.strip().splitlines()[-1:]}"); continue
    errs = cmp(json.loads((ORIG / j).read_text(encoding="utf-8")), json.loads((SC / j).read_text(encoding="utf-8")))
    print(f"[{'STRICT OK' if not errs else 'DIFF'}] {' '.join(args)} -> {j}" + ("" if not errs else f": {len(errs)} {errs[:3]}"))
