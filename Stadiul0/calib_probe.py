"""Stage 0 calibration probes (short experiments, not runs of the study).

    python calib_probe.py childhood --lr 2e-3 --seed 9101
        childhood only (3,072 steps): reference accuracy (fact, rule) at the end.
    python calib_probe.py task --lr 1e-3 --kind rule --steps 2048 --seed 9101
        childhood, then one target task of the given kind trained alone for --steps steps;
        probe-B accuracy and loss every 128 steps (learnability of the task type).
"""
import os

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse
import json
import time
from pathlib import Path

import torch

from p2.run import Runner, load_config

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["childhood", "task"])
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--life_lr", type=float, default=None)
    ap.add_argument("--seed", type=int, default=9101)
    ap.add_argument("--family", default="F1")
    ap.add_argument("--kind", default="rule")
    ap.add_argument("--steps", type=int, default=2048)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--set", action="append", default=[])
    a = ap.parse_args()
    cfg, sha = load_config(HERE / "config_stage0.yaml", [f"optim.lr={a.lr}"] + a.set)
    R = Runner(cfg, a.family, a.seed, HERE / "runs" / "_calib_unused", sha)
    t0 = time.perf_counter()
    R.childhood_phase()
    out = {"mode": a.mode, "lr": a.lr, "seed": a.seed, "childhood": R.childhood,
           "childhood_loss_curve": [round(float(R.childhood_loss[max(0, i - 32): i + 32].mean()), 3)
                                    for i in range(256, len(R.childhood_loss) + 1, 256)]}
    if a.mode == "task":
        k = next(i for i, t in enumerate(R.world.targets) if t.kind == a.kind)
        t = R.world.targets[k]
        lr = a.life_lr if a.life_lr is not None else a.lr
        curve = []
        for j, (x, y) in enumerate(R.batches(t.train_x, t.train_y, a.steps, a.batch)):
            R.agent.step(torch.from_numpy(x), torch.from_numpy(y), lr, None)
            if (j + 1) % 128 == 0:
                LB, AB = R.eval_task_B(k)
                tr = R.forward_items(torch.from_numpy(t.train_x), torch.from_numpy(t.train_y))
                curve.append((j + 1, round(AB, 3), round(LB, 3), round(tr["correct"].double().mean().item(), 3)))
        out.update({"task": k, "kind": a.kind, "modulus": t.modulus, "life_lr": lr,
                    "curve_step_accB_lossB_acctrain": curve})
    out["wall_s"] = round(time.perf_counter() - t0, 1)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
