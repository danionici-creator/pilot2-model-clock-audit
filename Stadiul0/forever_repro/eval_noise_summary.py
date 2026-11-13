# POST HOC test (a), 9 Nov 2026: summary of the evaluation-noise re-evaluations (eval_noise_posthoc.py). CPU only.
# Reads the authors' exact-match scores (their eval_avgPerf_longsequence.py output) of the original evaluation
# (runs/forever_repro_eval_<arm>.log) and of each re-evaluation (runs/forever_eval_noise_posthoc_<arm>_<mode>.log), and
# compares the generated answers line by line with the original outputs. Per task and cell: the standard deviation over
# the sampled evaluations (the original, unseeded, and the seeded ones), the greedy value, and the number of answers that
# differ from the original. Then the evaluation SD of a paired difference on dbpedia, against D_A1 and D_B1 of stage 1.
# Writes runs/forever_eval_noise_posthoc.json. Run from forever_repro/: python -I eval_noise_summary.py
import json, math, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "runs"
N = "Qwen_Qwen3-0.6Blora_cl_dataset_id_4"
ARMS = ["tau", "eta_m", "eta_m_A1", "tau_B1"]
TASKS = ["dbpedia", "amazon", "yahoo", "agnews"]
PAIRS = {"A1": ("tau", "eta_m_A1"), "B1": ("tau_B1", "eta_m")}   # tau - eta_m, sharing a task-0 adapter (stage 1)


def scores(log):
    if not log.exists():
        return None
    acc = {k: 100 * float(v) for k, v in re.findall(r"任务 (\w+) 的 accuracy：([0-9.]+)", log.read_text(encoding="utf-8"))}
    return acc if len(acc) == 4 else None


def answers(folder, i, t):
    p = folder / f"{N}_avgPerf" / f"{i}-{t}_result.txt"
    return [l.rstrip("\n").split("|||")[-1] for l in open(p, encoding="utf-8")] if p.exists() else None


def sd(xs):
    if len(xs) < 2:
        return float("nan")
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


modes = sorted({p.name.rsplit("_", 1)[1] for p in (HERE / "output" / "_eval_noise_posthoc").glob("*_*")
                if p.is_dir() and "_incomplete_" not in p.name and p.name.rsplit("_", 1)[0] in ARMS},
               key=lambda m: (m == "greedy", m))
print(f"re-evaluation modes found: {modes}")
res = {"modes": modes, "cells": {}}
for arm in ARMS:
    orig = scores(RUNS / f"forever_repro_eval_{arm}.log")
    cell = {"original": orig}
    for m in modes:
        s = scores(RUNS / f"forever_eval_noise_posthoc_{arm}_{m}.log")
        if s is None:
            continue
        diff = {}
        for i, t in enumerate(TASKS):
            a, b = answers(HERE / "output" / arm, i, t), answers(HERE / "output" / "_eval_noise_posthoc" / f"{arm}_{m}", i, t)
            diff[t] = None if a is None or b is None or len(a) != len(b) else sum(x != y for x, y in zip(a, b))
        cell[m] = {"acc": s, "answers_differing_from_original": diff}
    sampled = [orig] + [cell[m]["acc"] for m in modes if m != "greedy" and m in cell]
    cell["sd_sampled"] = {t: sd([x[t] for x in sampled]) for t in TASKS}
    cell["n_sampled"] = len(sampled)
    res["cells"][arm] = cell
    print(f"\n{arm}: {len(sampled)} sampled evaluations (original + seeded)" + (", greedy" if "greedy" in cell else ""))
    for t in TASKS:
        line = f"  {t:8s} original {orig[t]:6.2f}"
        for m in modes:
            if m in cell:
                line += f" | {m} {cell[m]['acc'][t]:6.2f} ({cell[m]['answers_differing_from_original'][t]} answers differ)"
        print(line + f" | SD sampled {cell['sd_sampled'][t]:.3f}")

pooled = {t: math.sqrt(sum(res["cells"][a]["sd_sampled"][t] ** 2 for a in ARMS) / len(ARMS)) for t in TASKS}
res["pooled_sd_sampled"] = pooled
print("\npooled within-cell SD of the sampled evaluations (points): " + ", ".join(f"{t} {pooled[t]:.3f}" for t in TASKS))
res["dbpedia_pairs"] = {}
for k, (x, y) in PAIRS.items():
    cx, cy = res["cells"][x], res["cells"][y]
    D = cx["original"]["dbpedia"] - cy["original"]["dbpedia"]
    sdd = math.sqrt(cx["sd_sampled"]["dbpedia"] ** 2 + cy["sd_sampled"]["dbpedia"] ** 2)
    per_mode = {m: cx[m]["acc"]["dbpedia"] - cy[m]["acc"]["dbpedia"] for m in modes if m in cx and m in cy}
    res["dbpedia_pairs"][k] = {"D_original": D, "sd_of_difference": sdd, "D_by_mode": per_mode,
                               "exceeds_eval_sd": abs(D) > sdd}
    print(f"D_{k} = {D:+.3f} (tau - eta_m on dbpedia); evaluation SD of the difference {sdd:.3f}; "
          f"|D| exceeds it: {abs(D) > sdd}; by mode: " + ", ".join(f"{m} {v:+.3f}" for m, v in per_mode.items()))
(RUNS / "forever_eval_noise_posthoc.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
