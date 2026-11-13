# Pilot 2, Stage 0: code and calibration

Code for Stage 0 of the Pilot 2 technical protocol v0.3 (`../Pilot2_Protocol_EN_draft.md`, section 12a):
construction and calibration on the author's laptop, before any freeze. Nothing in this folder is frozen.
The values in `config_stage0.yaml` marked *provisional* are generator and optimizer parameters that
the protocol leaves to Stage 0.

| File | Content | Protocol |
|---|---|---|
| `config_stage0.yaml` | Agent, optimizer, world, run structure, stream families F1–F6 | §3, §4 |
| `p2/world.py` | Vocabulary partition, fact, rule, reference and distractor tasks, probe halves A and B, batteries R and B_beh, disjointness assertions | §4.1, §4.2, G4 |
| `p2/streams.py` | Schedules of the stream families (segments on the 64-step quantum, idle intervals, cosine warm restarts) | §4.3–§4.5 |
| `p2/agent.py` | Pre-LN Transformer (≈ 0.93 M parameters) on one flat parameter buffer; explicit AdamW step, bit-identical to `torch.optim.AdamW`; per-step logged quantities, D1, D1_rel, D2 | §3, §5.1 |
| `p2/metrics.py` | Jensen–Shannon distance (base 2), centred linear CKA | §5.1 |
| `p2/run.py` | One run: childhood, life, evaluations, chunked D3, D4, C10b, displacement snapshots, drift T2, online covariates | §4–§7 |
| `p2/triplets.py` | Offline triplets (k, t₀, t₁): T1, T1-acc, inclusion, weights, competitors C0–C10b, rates, X_cov, Δc_e | §6, §7 |
| `launch.py` | Parallel single-threaded workers; skips completed runs (same resolved configuration), so a campaign resumes by repeating the command; `--verify-skipped` re-hashes their arrays | §3, §12a, G7 |
| `checks_stage0.py` | Automated checks: world, schedules, optimizer equivalence, D2 identity, determinism | G4, G7 |
| `calib_probe.py` | Short calibration probes: childhood at a given learning rate; learnability of one task type | §4.3, §12a |
| `stage0_summary.py`, `preview_headroom.py` | Measurability summary of a set of runs; crude headroom preview without c_e | §12a, G1, G3 |

## Commands (from this folder)

```
python checks_stage0.py
python launch.py --runs F1:9001 F2:9001 --workers 8 --tag tech1
python -m p2.run --family F2 --seed 9001 --out runs/test/F2_s9001
python -m p2.triplets runs/tech1/F2_s9001
```

## Implementation choices to be declared in the Stage 0 report

- **D2 lag.** The protocol's lag of exactly 256 steps needs 256 stored copies of v̂ (≈ 1 GB per worker).
  The code uses a blocked lag: v̂ at step 64·⌊(τ − 256)/64⌋, so the lag lies in [256, 319] steps and
  6 copies are kept. `run.d2_lag_mode: both` also computes the exact lag, for comparison.
- **Example length.** Every example is `[TASK] a b →` plus one answer token (5 tokens); training loss
  and probes are read at the answer position only. No padding occurs.
- **Idle evaluations.** During idle intervals θ is frozen, so the probe results of the last evaluation
  are reused, with the new c_a; this is exact.
- **Reference batteries.** R and B_beh are drawn from the reference tasks' trained items (32 per reference task each).
- **Seeds.** A run is (family, seed); the world, schedule, initialisation and batch order are drawn
  from independent streams of `numpy.random.SeedSequence([seed, family number])`. Technical runs use
  seeds 9001 and above.

Run outputs (`runs/`) are not part of any archive until Stage 0 is closed.
