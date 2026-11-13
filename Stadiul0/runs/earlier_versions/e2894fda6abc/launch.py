"""Run several Stage 0 runs as parallel single-threaded workers (protocol v0.3, sections 3 and 12a).

    python launch.py --runs F1:9001 F2:9001 ... [--workers 8] [--tag tech] [--set key=value ...]

Each run is a separate process with OMP_NUM_THREADS = MKL_NUM_THREADS = 1 and writes to
runs/<tag>/<family>_s<seed>/ (stdout and stderr in run.log). A summary with wall times is written to
runs/<tag>/launch_summary.json.

A run whose folder already holds a complete result (meta.json, written last, with every array file present
and the same resolved configuration) is skipped, so an interrupted campaign is resumed by repeating the
same command; runs are bit-identical, so a run cut off midway is simply redone from the start. An earlier
run.log of an incomplete run is kept as run.log.prevN (nothing is deleted). A completed run with a
different resolved configuration stops the launcher.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from p2.run import load_config, array_hashes

HERE = Path(__file__).resolve().parent
ARRAYS = ["steps", "evals", "episodes", "disp", "chunks", "world"]


def completed(out, cfg, verify):
    """True if out holds a complete run with configuration cfg; raises on a configuration mismatch."""
    m = out / "meta.json"
    if not m.exists() or not all((out / f"{n}.npz").exists() for n in ARRAYS):
        return False
    meta = json.loads(m.read_text(encoding="utf-8"))
    run_part = lambda c: {k: v for k, v in c.items() if k not in ("analysis", "meta")}
    if run_part(meta["config"]) != run_part(cfg):
        raise SystemExit(f"{out}: completed run with a different resolved configuration; use another --tag")
    if verify:
        for n in ARRAYS:
            with np.load(out / f"{n}.npz") as z:
                if array_hashes({k: z[k] for k in z.files}) != meta["sha256_arrays"][n]:
                    raise SystemExit(f"{out}: array hashes of {n}.npz do not match meta.json")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True, help="FAMILY:SEED items")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--tag", default="tech")
    ap.add_argument("--set", action="append", default=[])
    ap.add_argument("--verify-skipped", action="store_true", help="re-hash the arrays of skipped runs")
    a = ap.parse_args()
    cfg, _ = load_config(HERE / "config_stage0.yaml", a.set)
    env = dict(os.environ, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONUNBUFFERED="1")
    base = HERE / "runs" / a.tag
    base.mkdir(parents=True, exist_ok=True)
    queue = [tuple(item.split(":")) for item in a.runs]
    running, done = [], []
    t0 = time.time()
    while queue or running:
        while queue and len(running) < a.workers:
            if (HERE / "runs" / "_HW_STOP").exists():          # hardware watchdog (hw_watchdog.py): start nothing new
                print(json.dumps({"stopped_by_watchdog": (HERE / "runs" / "_HW_STOP").read_text(encoding="utf-8").strip(),
                                  "not_started": [f"{f}:{s}" for f, s in queue]}), flush=True)
                queue.clear()
                break
            fam, seed = queue.pop(0)
            out = base / f"{fam}_s{seed}"
            if completed(out, cfg, a.verify_skipped):
                done.append({"family": fam, "seed": int(seed), "returncode": 0, "skipped": True})
                print(json.dumps(done[-1]), flush=True)
                continue
            out.mkdir(parents=True, exist_ok=True)
            if (out / "run.log").exists():
                i = 1
                while (out / f"run.log.prev{i}").exists():
                    i += 1
                (out / "run.log").rename(out / f"run.log.prev{i}")
            cmd = [sys.executable, "-m", "p2.run", "--family", fam, "--seed", seed, "--out", str(out)]
            for s in a.set:
                cmd += ["--set", s]
            log = open(out / "run.log", "w", encoding="utf-8")
            p = subprocess.Popen(cmd, cwd=HERE, env=env, stdout=log, stderr=subprocess.STDOUT)
            running.append((p, fam, seed, time.time(), log))
        time.sleep(2)
        for item in list(running):
            p, fam, seed, ts, log = item
            if p.poll() is not None:
                log.close()
                running.remove(item)
                done.append({"family": fam, "seed": int(seed), "returncode": p.returncode,
                             "wall_s": round(time.time() - ts, 1)})
                print(json.dumps(done[-1]), flush=True)
    if (base / "launch_summary.json").exists():
        i = 1
        while (base / f"launch_summary.prev{i}.json").exists():
            i += 1
        (base / "launch_summary.json").rename(base / f"launch_summary.prev{i}.json")
    summary = {"workers": a.workers, "overrides": a.set, "total_wall_s": round(time.time() - t0, 1), "runs": done}
    (base / "launch_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    return 0 if all(d["returncode"] == 0 for d in done) else 1


if __name__ == "__main__":
    raise SystemExit(main())
