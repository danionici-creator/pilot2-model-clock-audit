> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `preinregistrare_FOREVER_repetari_2026-11-08.md`
> (version 3), whose hash was recorded before stage 1 in `runs/forever_repro_sha256.txt` (versions 1 and 2 are in
> `runs/earlier_versions/`). File names, paths, code identifiers, verdict labels and quoted words are left as in the
> original, with an English rendering in [square brackets] where useful.

# Preregistration of the repeated runs R1/R2 (8 Nov 2026, BEFORE running; version 3)

> **Version 3 (after the short colloquium of 8 Nov, `02_Pilot2/Colocviu/Verificare_raspunsuri_2026-11-08.md`).** The direction adopted under the rule, with 3 votes of 3: **(d) now, then (a) stage 1 only.** The section "Version 3" at the end **replaces** the decision rule below for stage 1. The rest remains valid. Version 2 is kept in `_work\_copii_siguranta\forever_repetari_v2_2026-11-08\`.

Version 1 (13:43) is kept in `_work\_copii_siguranta\forever_repetari_v1_2026-11-08\`, with its hash in `runs/forever_repro_sha256.txt`. Version 2 (13:58) integrates Copilot's verified remarks; the list of changes is at the end. No new run started between versions.

**Why:** after R2 (`Rezultate_teste_decisive_2026-11-07.md`, the section of 8 Nov, ~13:45) one question remained open. The aggregate verdict is equivalence (ΔOP +0.84, ΔBWT +0.69), but on dbpedia (the first task) τ gives 93.21 and η‖m̂‖ 87.89 (**+5.33 points**). A single pair does not separate the effect of the clock from non-determinism. Requested by the user ("Plan repeated runs"). The R2 verdict remains the one recorded; the runs here complement it and do not replace it.

**Facts the design rests on (checked in the code and in the files):**
1. Their code fixes the seed: `set_seed(42)` (`src/finetune_cl_our_qwen.py`, line 31); the shuffles (`shuffle()` without a seed) and the memory sampling derive from it. So R1 and R2 differ **only** by the clock and by GPU non-determinism (fp16, no deterministic algorithms).
2. The non-determinism is real: the adapters after task 0 differ between R1 and R2 (`adapter_model.safetensors`: `636589d5…` in `ckpt_tau`, `66dc0d26…` in `ckpt_eta_m`); dbpedia right after task 0: 98.04 against 97.86.
3. There are no replays on task 0 (2 phases in both runs), so the clock does not influence the task-0 adapter. Both adapters are valid starting points for either clock.
4. Each task calibrates its model day from its own 24 steps (`Phase 1: CALIBRATION CURRENT`), and `DriftRecorderCallback` reads only the `drift_log.csv` of the current task's folder. Copying the `0-dbpedia` folder carries nothing of the task-0 clock into tasks 1–3.
5. **What passes from one task to the next in their code: only the adapter weights.** Task t > 0 loads `PeftModel.from_pretrained(model, <the folder of task t−1>)` (line 330); `resume_from_checkpoint` is not used by the launcher. Each phase builds a new Trainer (lines 433, 553, 646, 719), so the AdamW optimizer (including m, v and the step counter), the learning-rate scheduler and the fp16 scaler start from zero at every phase, in all runs. The random generators are re-initialised with 42 at import (line 31) and in the constructor of every Trainer (`set_seed(self.args.seed)`, transformers 4.57.0, `trainer.py` line 452); each task is a new process. The replay memory is built from the data (`load_memory_buffer`), not from the checkpoint. **So copying the `0-dbpedia` folder reproduces exactly the boundary between tasks of their pipeline**, and η‖m̂‖ starts from a new optimizer under both clocks, as in R1 and R2.
6. **The starting point** (dbpedia right after task 0, their BWT script, lenient extraction): A 98.04, B 97.86. In each pair both arms start from the same adapter, so the difference at the start cancels in D.

**The design: 2 × 2 crossed (clock × task-0 adapter), plus a repetition.** A = the task-0 adapter of R1 (`ckpt_tau`), B = that of R2 (`ckpt_eta_m`).

| Arm | Clock | Task 0 | Status |
|---|---|---|---|
| `tau` (R1) | τ | A | existing |
| `eta_m` (R2) | η‖m̂‖ | B | existing |
| `eta_m_A1` | η‖m̂‖ | A (copied) | **stage 1** |
| `tau_B1` | τ | B (copied) | **stage 1** |
| `tau_A2` | τ | A (copied) | **stage 2** |
| `eta_m_A2` | η‖m̂‖ | A (copied) | **stage 2** |

Each new arm: the `0-dbpedia` folder and `0-dbpedia_result.txt` (the BWT part of task 0) are **copied** (not moved) from the source arm; then tasks 1–3, the BWT generations for 1 and 2 and the OP generation, with **the same commands and arguments** as `launch_repro_resume.sh`, the same code (the hashes in `runs/forever_repro_sha256.txt`), their seed (42), tasks 1–3 without the allocator cache (adaptation 5). Evaluation: `eval_repro.sh <arm>` unchanged. Launcher: `launch_repetari.sh`; analysis: `rep_verdict.py`; reconstruction: `r2_reconstruction_arm.py`.

**The main quantity (the only one the verdict is given on):** d = the final accuracy on dbpedia (their script `eval_avgPerf_longsequence.py`, exact match), in points. **The three pairs, fixed now** (the same adapter, the same repetition), with the difference τ − η‖m̂‖: D_A1 = d(`tau`) − d(`eta_m_A1`); D_B1 = d(`tau_B1`) − d(`eta_m`); D_A2 = d(`tau_A2`) − d(`eta_m_A2`). The other possible comparisons on A (for example `tau` with `eta_m_A2`) are descriptive only. **The noise** of the same clock on the same adapter (GPU non-determinism): N_τ = |d(`tau`) − d(`tau_A2`)|, N_η = |d(`eta_m_A1`) − d(`eta_m_A2`)|; **N = max(N_τ, N_η)** (the maximum, to be prudent). The mean: D̄ = (D_A1 + D_B1 + D_A2) / 3.

**The decision rule (fixed now, applied mechanically by `rep_verdict.py`).** It is a prudent criterion of practical consistency, not a statistical test: with 3 pairs and 2 repetitions per clock a distribution cannot be estimated.
- **Stop after stage 1:** if D_A1 and D_B1 have opposite signs, the verdict is **NU SE POATE ATRIBUI CEASULUI** [cannot be attributed to the clock]: the strict attribution criterion is not met (no value of D_A2 can then give three equal signs). The wording is "the data do not support a stable attribution of the difference to the clock", **not** "the clock has no effect": opposite signs may come from noise or from an interaction between the clock and the starting point, which a cell with a single run cannot separate. Stage 2 is then not needed for the verdict. Running it remains possible, as a descriptive measurement of the GPU noise, at the user's decision (laptop time); **the verdict remains the one after stage 1**.
- **After stage 2:**
  - **EFECT AL CEASULUI, τ mai bun pe dbpedia** [effect of the clock, τ better on dbpedia]: all three D > +2 and D̄ > N;
  - **EFECT AL CEASULUI, η‖m̂‖ mai bun pe dbpedia** [effect of the clock, η‖m̂‖ better on dbpedia]: all three D < −2 and |D̄| > N;
  - **NU SE POATE ATRIBUI CEASULUI** (the same wording as above): mixed signs, or |D̄| ≤ 2, or |D̄| ≤ N;
  - **NEDECIS** [undecided]: any other situation (for example all D of the same sign, |D̄| > 2 and > N, but one D below 2 in absolute value).
- **Validity:** an arm with a failed stage (rc ≠ 0) or stopped by the watchdog is moved aside (not deleted) and rerun once from the copied task 0; if it fails again, the verdict is **NEDECIS**.

**Reported, with no new verdict (they do not change the verdict on dbpedia):** the three D, D̄, their minimum and maximum, N_τ, N_η; the forgetting on dbpedia (the dbpedia component of BWT from their script) in each arm; the mean of the paired differences on OP and on BWT (stating whether |mean| ≤ 2) and the per-task scores; the effect of the adapter (d(`tau`) − d(`tau_B1`), d(`eta_m_A1`) − d(`eta_m`)), descriptive; **the triggers**, from the training logs: for each arm, task and trigger, the step, the threshold and the value of the clock, plus the difference in steps from the paired arm; the R² of the reconstruction (the same analysis as `r2_reconstruction.py`) for the η‖m̂‖ arms, **on tasks 1–3 only**: in the A arms, the `drift_log.csv` of task 0 comes from the τ run and does not measure the η‖m̂‖ clock. For comparison the same value (tasks 1–3) is also computed for R2; the question is whether the weak R² on agnews (0.578 in R2) recurs.

**Limits fixed in advance:** all runs have seed 42, so the repetitions measure GPU non-determinism, not variation between seeds; that is exactly the source of variation between R1 and R2, but it does not cover other seeds. A single order (4), a small model, small n (3 pairs).

**Time:** measured in R1 and in R2 (from task 1 to the end of the OP generation): 7 h 24 min per arm, in both. Stage 1 ≈ 15 h, stage 2 ≈ 15 h, in total ≈ 30 h of busy GPU. The hardware watchdog is restarted with a deadline that covers the run.

**The environment:** RTX 3050 Laptop 4 GB, driver 592.00; torch 2.8.0+cu128 (CUDA 12.8), transformers 4.57.0, peft 0.17.1 (`pip_freeze_venv_forever.txt`); AMP fp16, no deterministic algorithms (as in their code); Windows 11, Turbo mode. The code: commit `bbeb549a21e5…`, the hashes of the scripts in `runs/forever_repro_sha256.txt`. Adapters A and B have 4,602,248 bytes each. R1 and R2 are not overwritten: the launcher only reads from `ckpt_tau`, `ckpt_eta_m`, `output/tau`, `output/eta_m` and refuses an arm whose folder already exists.

**Start:** only with the user's explicit agreement (the weekend authorisation expires after 8 Nov 2026).

**The changes of version 2 (Copilot's remarks, checked point by point):**
- *Accepted:* fact 5 (the state that passes between tasks, checked in the code) and fact 6 (the starting point); the pairs and the formula of N written explicitly, with the other comparisons marked descriptive (the pairs and N already existed in v1; now they are called "fixed"); the wording of the early-stop verdict and the possibility of an interaction; stage 2 allowed after the stop too, descriptively only; the rule called a consistency criterion, not a statistical test; reporting D, D̄, minimum, maximum, N_τ, N_η; the validity rule; the table of triggers; the forgetting on dbpedia reported as secondary; the environment.
- *Rejected, with the reason:* (1) the complete restoration of the optimizer, the scheduler, the scaler and the random states: in their code none of these passes between tasks (fact 5), so restoring them would take the run away from their pipeline; (2) the dbpedia score before and after each replay: their code overwrites the adapter in the same folder at every phase, so it would require changing the code; (3) R² "near the thresholds": undefined and with too few windows (~4 triggers per task); the question of the mechanism is measured directly by the trigger steps; (4) the vague conditions for NEDECIS ("complicated interaction", "too close to the limit of the rule"): they would reintroduce judgement after the result; (5) forgetting as the main quantity: in each pair the starting point is common, so D on the final score and D on forgetting differ only by the extraction metric; the main quantity remains the exact-match score, as in R1 and R2.

## Version 3 (8 Nov 2026, after the short colloquium, BEFORE stage 1 and before running analysis (d))

**Nomenclature (a correction checked in the paper, Appendix G, Table 14):** what we call "order 4" (`dataset_id` 4 in their repository) is **order 1 of the paper** (Standard CL: dbpedia → amazon → yahoo → ag). Option (b), "order 5", is order 2 of the paper. In the repository, `dataset_id` 1–3 are the long sequences of 15 tasks.

**The decision rule of stage 1** (replaces the rule above; applied mechanically by `rep_verdict.py` v3). D_A1 = d(`tau`) − d(`eta_m_A1`), D_B1 = d(`tau_B1`) − d(`eta_m`), where d is the final accuracy on dbpedia, by exact match.
- D_A1 > +2 and D_B1 > +2: **DEFICIT CONSECVENT PE DBPEDIA SUB η‖m̂‖** [consistent deficit on dbpedia under η‖m̂‖] on both starting adapters. It is associated with the clock, not causal evidence; the scope: seed 42, order 1 of the paper.
- D_A1 < −2 and D_B1 < −2: **AVANTAJ CONSECVENT PE DBPEDIA SUB η‖m̂‖** [consistent advantage on dbpedia under η‖m̂‖], with the same reservations.
- Opposite signs: **NU SE REPRODUCE ROBUST** [not reproduced robustly]. The data do not support a stable attribution to the clock; the wording is not "the clock has no effect".
- Both |D| ≤ 2: **DEFICITUL DE 5,3 NU SE REPRODUCE** [the 5.3 deficit does not recur] from common starting points.
- Otherwise (the same sign, only one above 2): **NECONCLUDENT** [inconclusive].
- **Stage 2 no longer starts automatically.** It is not needed for the verdict (2 of 3 participants). For NECONCLUDENT, the three proposed different continuations, and the colloquium's rule then requires the cheaper option, hence a stop. If stage 2 is ever run, it is a separate decision, with a descriptive role: N is only a lower bound of the noise, and the labels remain the prudent ones above.
- Validity (a failed arm is rerun once, then NEDECIS) remains.
- Launch: `bash launch_repetari.sh 1` (the launcher is unchanged; with the argument 1 it stops after stage 1).

**Reported as secondary, with no verdict:** the forgetting on dbpedia (the BWT component) for each pair; OP, BWT and the per-task scores; the table of triggers; the lenient score on dbpedia. For all results the limit of stochastic decoding is noted: their generators use `do_sample=True`, `temperature=0.02`, no seed. [Post hoc test (a) of 9–10 Nov later showed that this decoding, with top_k 1 and top_p 0, is deterministic in practice; closure report §5.2.]

**Analysis (d), fixed before running** (`d_same_trajectory.py`; post hoc with respect to the R2 data, but with its outputs fixed here). On the R2 trajectory both clocks are recorded: `tau` (η‖m̂‖, the one that triggered) and `tau_true` (Σ‖Δθ‖).
1. **Validation of the method:** the thresholds mult × day (day = the value of the clock at step 24, mult ∈ {1, 2, 4, 7, …}) applied to the η clock must reproduce exactly the actual triggers of R2.
2. **The counterfactual:** where τ = Σ‖Δθ‖ would have crossed its thresholds on the **same** trajectory. The comparison is clean only up to the first trigger that differs, inclusive.
3. **The ratio** ‖Δθ‖ / η increment, by position since the last start of a phase (step 1, step 25 and the step after each actual trigger), relative to the task's median.
4. **R²** over 8-step windows, with and without the windows that contain the start of a phase.

**How it is read (fixed now):**
- If the counterfactual τ triggers coincide with the η ones on the same trajectory, the delay of 0–33 steps between R1 and R2 comes from different trajectories (the noise of the run). If τ triggers earlier on the same trajectory, the clocks differ intrinsically in their code.
- If the ratio at positions 0–2 departs from 1 by more than a factor of 2, and R² without the start windows rises by at least 0.10, the divergence lies in the transitions after a restart. The restart is common to our port, so it does not by itself explain the port–code difference; the remaining candidates are fp16 with GradScaler, the data restarted at every phase and the number of epochs.
