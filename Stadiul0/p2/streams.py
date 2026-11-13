"""Stream families F1-F6 (protocol v0.3, sections 4.3-4.5).

A schedule is a list of segments plus a learning rate for every life step. Training segments are
multiples of the step quantum q0 = 64; idle intervals are multiples of 64 ticks and sit between
segments. All generator parameters come from the family block of the configuration.
"""
from dataclasses import dataclass, asdict

import numpy as np

TRAIN_KINDS = ("new", "reexp", "reh", "distractor")
EXPOSURE_KINDS = ("new", "reexp", "reh")        # segments that train a target task


@dataclass
class Segment:
    kind: str            # new | reexp | reh | distractor | idle
    task: int            # target index (new, reexp, reh), distractor index, or -1 (idle)
    steps: int = 0       # optimizer steps (training segments)
    ticks: int = 0       # idle ticks (idle intervals)
    batch: int = 0
    label_noise: float = 0.0

    def as_dict(self):
        return asdict(self)


def _split_units(rng, total, lengths):
    """Split `total` units into a random sequence of segment lengths drawn from `lengths`."""
    out = []
    while total > 0:
        ok = [L for L in lengths if L <= total]
        L = int(rng.choice(ok))
        out.append(L)
        total -= L
    return out


def _batch(rng, fam):
    return int(rng.choice(fam["batch"]))


def _cycle(fam, n_tasks, per_task, q0, rng):
    """F1, F3, F4: new task, then round-robin rehearsal of the tasks learned before it."""
    segs, rr = [], 0
    assert fam["new_steps"] + fam["reh_per_cycle"] * fam["reh_steps"] == per_task
    for i in range(n_tasks):
        segs.append(Segment("new", i, steps=fam["new_steps"], batch=_batch(rng, fam)))
        for _ in range(fam["reh_per_cycle"]):
            if i == 0:
                k = 0
            else:
                k = rr % i
                rr += 1
            segs.append(Segment("reh", k, steps=fam["reh_steps"], batch=_batch(rng, fam)))
    return segs


def _novelty(fam, n_tasks, per_task, q0, rng):
    """F2, F5: new tasks interleaved with re-exposure to learned tasks in random amounts."""
    units_total = n_tasks * (per_task - fam["new_steps"]) // q0
    gaps = rng.multinomial(units_total, np.full(n_tasks, 1.0 / n_tasks))
    segs = []
    for i in range(n_tasks):
        segs.append(Segment("new", i, steps=fam["new_steps"], batch=_batch(rng, fam)))
        for L in _split_units(rng, int(gaps[i]), fam["reexp_units"]):
            k = int(rng.integers(0, i + 1))
            segs.append(Segment("reexp", k, steps=L * q0, batch=_batch(rng, fam)))
    return segs


def _distractor(fam, n_tasks, per_task, q0, rng, n_distractor):
    """F6: regular target exposures, interleaved with variable-length distractor segments."""
    target_steps = fam["new_steps"] + fam["reh_per_cycle"] * fam["reh_steps"]
    units_total = n_tasks * (per_task - target_steps) // q0
    gaps = rng.multinomial(units_total, np.full(n_tasks, 1.0 / n_tasks))
    segs, rr = [], 0
    for i in range(n_tasks):
        segs.append(Segment("new", i, steps=fam["new_steps"], batch=_batch(rng, fam)))
        for L in _split_units(rng, int(gaps[i]), fam["distractor_units"]):
            d = int(rng.integers(0, n_distractor))
            segs.append(Segment("distractor", d, steps=L * q0, batch=_batch(rng, fam),
                                label_noise=fam["label_noise"]))
        for _ in range(fam["reh_per_cycle"]):
            k = 0 if i == 0 else rr % i
            rr += i > 0
            segs.append(Segment("reh", k, steps=fam["reh_steps"], batch=_batch(rng, fam)))
    return segs


def _insert_idle(segs, idle, q0, rng):
    out = []
    for s in segs:
        out.append(s)
        if rng.random() < idle["p"]:
            lo, hi = idle["units"]
            out.append(Segment("idle", -1, ticks=int(rng.integers(lo, hi + 1)) * q0))
    return out


def _lr_schedule(fam, base_lr, life_steps, q0, rng):
    spec = fam["lr"]
    if spec["kind"] == "constant":
        return np.full(life_steps, base_lr), [0]
    assert spec["kind"] == "cosine_restarts"
    hi, lo = base_lr * spec["max_mult"], base_lr * spec["min_mult"]
    p_lo, p_hi = spec["period"]
    lr = np.empty(life_steps)
    restarts, start = [], 0
    while start < life_steps:
        T = int(rng.integers(p_lo // q0, p_hi // q0 + 1)) * q0
        restarts.append(start)
        n = np.arange(min(T, life_steps - start))
        lr[start: start + len(n)] = lo + 0.5 * (hi - lo) * (1 + np.cos(np.pi * n / T))
        start += T
    return lr, restarts


def build_schedule(fam, n_tasks, per_task, q0, base_lr, rng, n_distractor=8):
    structure = fam["structure"]
    if structure == "cycle":
        segs = _cycle(fam, n_tasks, per_task, q0, rng)
    elif structure == "novelty":
        segs = _novelty(fam, n_tasks, per_task, q0, rng)
    elif structure == "distractor":
        segs = _distractor(fam, n_tasks, per_task, q0, rng, n_distractor)
    else:
        raise ValueError(structure)
    if "idle" in fam:
        segs = _insert_idle(segs, fam["idle"], q0, rng)
    life_steps = sum(s.steps for s in segs)
    assert life_steps == n_tasks * per_task, (life_steps, n_tasks * per_task)
    for s in segs:
        assert s.steps % q0 == 0 and s.ticks % q0 == 0
        assert (s.kind == "idle") == (s.steps == 0)
    lr, restarts = _lr_schedule(fam, base_lr, life_steps, q0, rng)
    return segs, lr, restarts
