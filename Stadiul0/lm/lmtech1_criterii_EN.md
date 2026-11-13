> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `lmtech1_criterii.md`, whose hash was recorded before the
> runs in `runs/lmtech1_criterii_sha256.txt`. File names, paths, code identifiers and quoted words are left as in the
> original.

# Technical round lmtech1: the FOREVER clock in the FOREVER schedule, on Qwen3-0.6B (criteria fixed BEFORE running, 6 Nov 2026)

**What it is:** a technical round, not preregistered, like tech1–tech3. The LM arm of Pilot 2, step 2 of `02_Pilot2\Literatura\Literatura_marime_actualizari_AdamW.md` §6. **Blind to T1:** the G2 analysis does not read `evals.npz` (the accuracy on the old tasks, i.e. forgetting).

**The run:** `lm_forever_run.py` (the complete description of the set-up and of the deviations is in the script's header), 3 seeds: 7101, 7102, 7103. 10 tasks × 512 synthetic facts; task 0: 60 epochs, the others: 10 (as in the FOREVER script). Qwen3-0.6B (SHA-256 in `..\modele_provenienta.md`), LoRA r = 8, α = 16, q_proj and v_proj; fp16 with GradScaler; AdamW without weight decay; rate 3e-4; linear schedule with warmup, restarted at every phase; calibration on 24 steps; thresholds d·τ_day; replays not counted in τ. RTX 3050 Laptop, ASUS Turbo mode, on mains power.

**Determinism (checked beforehand):** two identical runs (2 short tasks) give bit-identical arrays (the telemetry, the probes, the evaluations, the final factors). It is repeated at the end on one run of the round (G7-GPU).

**The analysis** (`lm_forever_g2.py`, fixed now): windows of 8 counted steps; out-of-run R² (one seed left out) for the rate of τ (factors; secondarily ΔW) and for D3 (the change on 128 untrained probes), with the ladder: Ση → Ση‖g̃‖ → Ση‖m̂‖ → the mean field Ση‖m̂‖·√d/√Tr v̂ → Ση + Ση‖m̂‖ → GBDT on all the telemetry; the residual of "y ~ Ση" by window within the phase; τ at the level of the phase from Ση and Ση‖m̂‖.

**The prediction written before any LM data** (the literature document, 4 Nov 2026, §1 point 3 and §5 point 3): in the FOREVER set-up, Ση (the schedule of the rate, known for free from the scheduler) explains most of τ. Operationalisation: out-of-run R² of the rate of τ from Ση ≥ 0.80 → "the clock is dominated by the schedule of the rate". It is not a gate; it is reported whatever the outcome. **Note of honesty:** the code test on two short and identical runs (4 epochs, 15 windows) has already given R² 0.40 for Ση and 0.97 for Ση‖m̂‖; it is a code test, not a measurement, but it shows that the prediction can fail.

**Validity criteria per run** (fixed after the learning check with 2 tasks, `runs\lm_smoke\full2`, before lmtech1):
- no non-finite loss (the script stops);
- steps skipped by the GradScaler ≤ 2% of the counted steps;
- the accuracy on the current task at the end of each task ≥ 0.95 (only the diagonal of `evals.npz`, read from `run.log`; check full2: 1.000 and 1.000).

The full2 check (seed 2, 2 complete tasks, 6 Nov, 16:29–16:35): task 0, 960 steps in 311 s (0.32 s/step), accuracy 1.000; task 1, 160 counted steps, 8 phases (calibration, 3 replays, 3 current phases, the final replay), 56 s, accuracy 1.000; skipped steps 1.16%; maximum VRAM 1.7 GB. **Note:** the check also displayed the accuracy on task 0 after task 1 (0.514). It is T1-type information from a check, not from the round; it enters no analysis. In lmtech1 only the diagonal is read.
- the run ends with `meta.json` and the SHA-256 hashes.

**What is not decided from this round:** nothing about H1 (forgetting) and nothing about protocol v0.5. The result goes into the Stage 0 notes and into the decision about the form of the LM arm.
