# Re-runs the analyses of Pilot 2 from the stored results and compares what they print and write with the stored logs and
# JSON files. Written for the archive on 9 Nov 2026, after the study; it changes nothing in the analyses themselves.
#   Usage, from the repository root, after unpacking the Zenodo data part into it:  python -I Stadiul0/reproduce_analyses.py
#   Optional: names of checks to run (e.g. T-A T-B); default: all.
# Every stored JSON file that an analysis rewrites is restored byte for byte afterwards, so SHA256SUMS.txt still verifies.
# Four scripts contain the author's absolute path to Stadiul0/runs; they run from a temporary copy in their own folder with
# that path replaced, and the copy is removed afterwards. CPU only; about 3 minutes on the author's laptop.
# Library versions of the original runs: Python 3.14.6, numpy 2.5.1, pandas 3.0.3, scikit-learn 1.9.0, scipy 1.18.0,
# torch 2.13.0+cpu. With these, every stored log was reproduced line for line on 9 Nov 2026; three JSON files differ only in
# the last digits of regression coefficients (relative difference below 1e-15), which the comparison below tolerates.
# Corrected on 12 Nov 2026 after the independent audit of the archive (Recenzii/Audit_Codex_2026-11-10/): the JSON
# comparison is now strict about structure (empty containers included), types and non-finite values (finding A01: a
# finite value turned into NaN used to pass); the exit code is 1 if any check differs, fails or is unknown (A03); one
# post hoc check added (B02). The tech-G2 check has no stored output and is only executed and printed; its numbers are
# compared by hand with table 1 of the report.
import json, math, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent  # Stadiul0
# the author's absolute path, as written in four scripts: r"D:\Time\02_Pilot2\Stadiul0\runs..."
ABS_RE = re.compile(r'r"D:\\Time\\02_Pilot2\\Stadiul0((?:\\[^"\\]+)*)"')
TOL = 1e-9

L, F = "lm", "forever_repro"
# name, folder (relative to Stadiul0), arguments, stored log (relative to Stadiul0) or None, JSON files the script writes
CHECKS = [
    ("T-A", ".", ["ta_analysis.py"], "runs/ta_analysis.log", ["runs/ta_verdict.json"]),
    ("T-B", ".", ["tb_part1_g2.py"], "runs/tb_part1_g2.log", ["runs/tb_part1_verdict.json"]),
    ("T-D", ".", ["td_audit.py"], "runs/td_audit.log", []),
    ("T-C", L, ["lm_d3_competitors.py", "../runs/lmtech1", "../runs/lmtech2", "../runs/lmsens_bf16", "../runs/lmsens_a32"],
     "runs/tc_lm_d3_competitors.log", []),
    ("SuperNI", ".", ["sni_analysis.py"], "runs/sni_analysis_final.log", ["runs/sni_verdict.json"]),
    ("SuperNI-S2-secondary", ".", ["sni_s2_secondary.py"], "runs/sni_S2_secundar.log", []),  # script written 9 Nov
    ("LM-tau-lmtech1", L, ["lm_forever_g2.py", "../runs/lmtech1"], "runs/lmtech1_g2.log", []),
    ("LM-tau-lmtech2", L, ["lm_forever_g2.py", "../runs/lmtech2"], "runs/lmtech2_g2.log", []),
    ("LM-tau-bf16", L, ["lm_forever_g2.py", "../runs/lmsens_bf16"], "runs/lmsens_bf16_g2.log", []),
    ("LM-tau-a32", L, ["lm_forever_g2.py", "../runs/lmsens_a32"], "runs/lmsens_a32_g2.log", []),
    ("tech-G2", ".", ["g2_preview.py"], None, []),  # no output was stored when it ran; its numbers are report §5.1, table 1
    ("G2-CPU-checks", ".", ["g2_cpu_checks.py"], "runs/g2_cpu_checks_2026-11-06.log", []),
    ("tech4", ".", ["tech4_analysis.py"], "runs/tech4_analysis.log", []),
    ("FOREVER-R2-reconstruction", F, ["r2_reconstruction.py"], "runs/forever_repro_r2_reconstruction.log",
     ["runs/forever_repro_r2_reconstruction.json"]),
    ("FOREVER-R2-arm-eta_m", F, ["r2_reconstruction_arm.py", "eta_m"], None, ["runs/forever_repetari_r2_eta_m.json"]),
    ("FOREVER-R2-arm-eta_m_A1", F, ["r2_reconstruction_arm.py", "eta_m_A1"], "runs/forever_repetari_r2.log",
     ["runs/forever_repetari_r2_eta_m_A1.json"]),
    ("FOREVER-d", F, ["d_same_trajectory.py"], None, ["runs/forever_d_same_trajectory.json"]),
    ("FOREVER-stage1", F, ["rep_verdict.py"], None, ["runs/forever_repetari_verdict.json"]),
    ("FOREVER-drift-ratio", F, ["drift_ratio_posthoc.py"], "runs/forever_drift_ratio_posthoc.log", []),  # post hoc, 9 Nov
    # post hoc, after the final review round of 9 Nov (Recenzii/Runda_finala_2026-11-09): (a), (b), (c)
    ("POSTHOC-a-eval-noise", F, ["eval_noise_summary.py"], "runs/forever_eval_noise_posthoc_summary.log",
     ["runs/forever_eval_noise_posthoc.json"]),
    ("POSTHOC-b-TA-memory", ".", ["ta_memory_posthoc.py"], "runs/ta_memory_posthoc.log", ["runs/ta_memory_posthoc.json"]),
    ("POSTHOC-c-skipped-steps", F, ["skip_check_posthoc.py"], "runs/forever_skip_check_posthoc.log", []),
    # post hoc, 12 Nov 2026, after the independent audit (finding B02/C02): in-sample versus leave-one-task-out R²
    ("POSTHOC-B02-heldout-task", F, ["r2_heldout_task_posthoc.py"], "runs/forever_r2_heldout_task_posthoc.log", []),
]


def clean(text):
    """Lines of a log without Python warnings (they carry local paths) and the source line printed under each."""
    out, skip = [], False
    for line in text.replace("\r\n", "\n").split("\n"):
        if re.search(r"(Warning|warn)\b.*:", line) and ("\\" in line or "/" in line):
            skip = True
            continue
        if skip and line.startswith("  "):
            skip = False
            continue
        skip = False
        out.append(line.rstrip())
    while out and not out[-1]:
        out.pop()
    return out


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def diff_json(a, b, p, worst):
    """First difference between stored a and new b (None if equal); worst[0] keeps the largest relative difference."""
    if isinstance(a, dict) or isinstance(b, dict):
        if not (isinstance(a, dict) and isinstance(b, dict)):
            return f"{p}: {type(a).__name__} vs {type(b).__name__}"
        if set(a) != set(b):
            return f"{p}: keys {sorted(set(a) ^ set(b))[:5]}"
        for k in a:
            d = diff_json(a[k], b[k], f"{p}/{k}", worst)
            if d:
                return d
        return None
    if isinstance(a, list) or isinstance(b, list):
        if not (isinstance(a, list) and isinstance(b, list)):
            return f"{p}: {type(a).__name__} vs {type(b).__name__}"
        if len(a) != len(b):
            return f"{p}: length {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = diff_json(x, y, f"{p}[{i}]", worst)
            if d:
                return d
        return None
    if is_num(a) and is_num(b):
        fa, fb = math.isfinite(a), math.isfinite(b)
        if not (fa and fb):  # NaN only matches NaN, an infinity only the same infinity
            same = (math.isnan(a) and math.isnan(b)) if (math.isnan(a) or math.isnan(b)) else a == b
            return None if same else f"{p}: {a!r} vs {b!r}"
        d = abs(a - b) / max(1.0, abs(a))
        if d > TOL:
            return f"{p}: {a!r} vs {b!r}"
        worst[0] = max(worst[0], d)
        return None
    if type(a) is not type(b) or a != b:
        return f"{p}: {a!r} vs {b!r}"
    return None


def same_json(a, b):
    worst = [0.0]
    d = diff_json(a, b, "", worst)
    if d:
        return False, d
    return True, ("identical" if worst[0] == 0 else f"equal within {worst[0]:.1e}")


def run(name, folder, args):
    cwd = S / folder
    script = cwd / args[0]
    src = script.read_text(encoding="utf-8")
    tmp = None
    new, n = ABS_RE.subn(lambda m: repr(str(S.joinpath(*[q for q in m.group(1).split("\\") if q]))), src)
    if n:
        tmp = cwd / f"_repro_tmp_{script.stem}.py"
        tmp.write_text(new, encoding="utf-8")
        args = [tmp.name] + args[1:]
    try:
        cmd = [sys.executable, "-I", "-X", "utf8"] + args
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if p.returncode != 0 and "ModuleNotFoundError" in p.stderr:
            p = subprocess.run(cmd[:1] + cmd[2:], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()
    return p


def main():
    import numpy, pandas, sklearn, scipy
    try:
        import torch
        tv = torch.__version__
    except ImportError:
        tv = "not installed (needed by T-C)"
    print(f"Python {sys.version.split()[0]}, numpy {numpy.__version__}, pandas {pandas.__version__}, "
          f"scikit-learn {sklearn.__version__}, scipy {scipy.__version__}, torch {tv}\n")
    want = set(sys.argv[1:])
    unknown = want - {c[0] for c in CHECKS}
    if unknown:
        print(f"Unknown check name(s): {', '.join(sorted(unknown))}. Known: {', '.join(c[0] for c in CHECKS)}")
        sys.exit(1)
    n_ok = n_all = 0
    for name, folder, args, log, jsons in CHECKS:
        if want and name not in want:
            continue
        n_all += 1
        saved = {j: (S / j).read_bytes() for j in jsons}
        t0 = time.time()
        try:
            p = run(name, folder, args)
            msgs, ok = [f"rc {p.returncode}, {time.time() - t0:.0f} s"], p.returncode == 0
            if log:
                a, b = clean((S / log).read_text(encoding="utf-8", errors="replace")), clean(p.stdout)
                if a == b:
                    msgs.append(f"output = {log} ({len(a)} lines)")
                else:
                    ok = False
                    d = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
                    first = d[0] if d else min(len(a), len(b))
                    msgs.append(f"output differs from {log} (stored {len(a)} lines, new {len(b)}; first at line {first + 1})")
            elif not jsons:
                msgs.append("no stored output; printed below")
            for j in jsons:
                good, why = same_json(json.loads(saved[j]), json.loads((S / j).read_text(encoding="utf-8")))
                ok &= good
                msgs.append(f"{Path(j).name}: {why}")
        finally:
            for j, data in saved.items():  # restore the stored files exactly
                (S / j).write_bytes(data)
        n_ok += ok
        print(f"[{'OK' if ok else 'DIFFERS'}] {name}: " + "; ".join(msgs), flush=True)
        if (not log and not jsons) or p.returncode != 0:
            print("    " + "\n    ".join((p.stdout + p.stderr).strip().splitlines()[:40]))
    print(f"\n{n_ok} of {n_all} checks reproduce the stored results.")
    sys.exit(0 if n_all and n_ok == n_all else 1)


if __name__ == "__main__":
    main()
