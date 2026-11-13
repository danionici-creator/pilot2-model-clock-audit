# Colloquium dossier: FOREVER with the authors' own code, what next? (8 November 2026)

Author of all analyses: Claude (AI assistant). The project owner is a non-specialist. Claude does not vote; it verifies the answers and applies a decision rule fixed before sending (section 7). Everything below is either **verified** (checked against code, logs or files) or explicitly marked **post hoc** (computed after the results were known) or **hypothesis**.

## 1. Background (short)

The study asked whether an "experiential index" (accumulated internal change of a network, one candidate being FOREVER's model-centric clock τ, arXiv:2601.03938) carries information beyond cheap optimizer telemetry. Earlier preregistered tests closed this line negatively in our setting. The clock τ = Σ‖Δθ‖ (sum of parameter-update norms) was reconstructed by Ση‖m̂‖ (learning rate × norm of AdamW's bias-corrected first moment), and a replay scheduler driven by Ση‖m̂‖ instead of τ gave the same retention:
- **T-A**, synthetic facts, Qwen3-0.6B + LoRA, 5 seeds per clock: retention within ±2 pp; Ση‖m̂‖ triggered replays at the same steps as τ (≤ 1 step).
- **SuperNI S1**, natural tasks, 3 seeds: Ση‖m̂‖ alone reconstructs the rate of τ over 8-step windows at R² 0.963 (one seed held out) and 0.956 (one task held out).
- **SuperNI S2**: test loss with Ση‖m̂‖ − τ = −0.6%, 95% CI [−1.9%; +0.7%], inside a ±5% margin; triggers at the same steps (median difference 0).

**Limit:** all of these used **our port** of FOREVER's schedule, not their code. Declared port deviations: bf16 without GradScaler (theirs: fp16 AMP with GradScaler); fewer epochs; the task's batches form one data stream across phases (in their code every phase builds a new Trainer and restarts the data); memory sampling differs for generation tasks.

## 2. What we ran this weekend (their code, preregistered)

- **Code:** github.com/WoodScene/FOREVER, commit bbeb549, `src/finetune_cl_our_qwen.py`, unchanged, with their library versions (torch 2.8.0+cu128, transformers 4.57.0, peft 0.17.1).
- **Benchmark:** "Standard CL" order 4 (dbpedia → amazon → yahoo → agnews), with their arguments: Qwen3-0.6B fp16 + LoRA on q_proj and v_proj, micro-batch 4 × 8 accumulation, 10 epochs (60 on the first task), 2 memory epochs, model day 24 steps, memory 2% per previous task.
- **Evaluation:** their own scripts. OP = mean final accuracy, exact match; BWT uses their lenient label extraction.
- **Hardware:** RTX 3050 Laptop, 4 GB.
- **Necessary adaptations:** a cache path; the test-data path, because their generators hard-code SuperNI; `python` instead of `torchrun`. Tasks 1–3 were trained with `PYTORCH_NO_CUDA_MEMORY_CACHING=1` after a CUDA OOM under Windows. That allocator setting changes speed and memory, not the arithmetic, and was applied to both runs. Everything was preregistered and hashed before the runs.

**R1**: their code with clock τ. **R2**: one change only: the counter that triggers replays advances by η‖m̂‖ instead of ‖Δθ‖. The replay intensity β is still computed from ‖Δθ‖ as in the original.

| | Paper (Qwen3-0.6B, Table 1, mean of 3 orders) | R1 τ | R2 η‖m̂‖ | R1 − R2 |
|---|---|---|---|---|
| **OP** (exact match) | 72.9 | **72.37** | **71.53** | **+0.84** |
| dbpedia (first task) | – | 93.21 | 87.89 | **+5.33** |
| amazon | – | 47.52 | 48.92 | −1.40 |
| yahoo | – | 60.34 | 61.66 | −1.32 |
| agnews | – | 88.40 | 87.65 | +0.75 |
| **BWT** | −4.7 | **−5.78** | **−6.47** | +0.69 |
| BWT per task (dbpedia, amazon, yahoo) | – | −4.81, −8.48, −4.04 | −9.89, −5.84, −3.68 | |
| OP with lenient extraction | – | 72.39 | 71.57 | +0.82 |

**Preregistered verdicts:**
- R1 reproduces FOREVER: OP within ±5 of 72.9.
- R2 vs R1 is **equivalence**: |ΔOP| ≤ 2 points (one pair, descriptive), and the same for BWT.

**Replay triggers** (step within the 313 steps of each task; thresholds are 1, 2, 4, 7 × the model day, calibrated per task on its own first 24 steps; plus one final replay per task in both runs):

| Task | R1 τ | R2 η‖m̂‖ |
|---|---|---|
| 1 amazon | 24, 48, 100, 185 | 24, 50, 104, 192 |
| 2 yahoo | 24, 46, 87, 160 | 24, 48, 96, 178 |
| 3 agnews | 24, 47, 93, 160 | 24, 47, 96, 193 |

η‖m̂‖ triggers at the same step or later, by up to 33 steps. In our port the triggers coincided.

**Secondary analysis**, preregistered: OLS R² of Σ‖Δθ‖ over non-overlapping 8-step windows, from the increase of the η‖m̂‖ clock in the same window, within R2. The benchmark is ≥ 0.90.
- Pooled over the 4 tasks: **0.922** (351 windows). Per task: dbpedia 0.937 (234 windows), amazon 0.986, yahoo 0.934, **agnews 0.578** (39 windows each).
- **Post hoc:** pooled over tasks 1–3 only, the tasks with replay: **0.749** (117 windows).
- **Post hoc:** for agnews, correlation 0.76, with a coefficient of variation of y of 0.49, so the weak fit is not caused by a small spread.

## 3. Verified facts about their code that matter for interpretation

1. **The seed is fixed:** `set_seed(42)` at import (line 31), and `Trainer.__init__` calls `set_seed(args.seed)` again (transformers 4.57.0, trainer.py line 452). Shuffles and memory sampling derive from it. R1 and R2 therefore differ **only** by the clock and by GPU non-determinism: fp16, with no deterministic algorithms.
2. **GPU non-determinism is real.** The task-0 adapters of R1 and R2 have different hashes. dbpedia accuracy right after task 0 is 98.04 (R1) vs 97.86 (R2), with the lenient script. Task 0 has no replay in either run, so the clock played no role there.
3. **Only the LoRA weights pass between tasks:** `PeftModel.from_pretrained(<previous task dir>)`, line 330. Each phase (calibration, current, replay, final replay) builds a new Trainer (lines 433, 553, 646, 719), so AdamW's m, v and step count, the LR scheduler and the GradScaler restart in every phase, in both runs.
4. **The drift log covers the 313 current-task steps.** Δθ = 0 at the first step of every current-task phase in both runs (for example steps 0, 24, 48, 100 and 185 in R1, task 1), plus 1–2 isolated steps on agnews and yahoo. **Hypothesis:** these are fp16 GradScaler skips at the initial loss scale of each new Trainer. In R2, the η‖m̂‖ increment at those steps is about 0 as well.
5. **Each task calibrates its own model day.** The drift recorder reads only the current task's `drift_log.csv`.

## 4. Open questions after R2

- **The dbpedia gap of 5.3 points** (forgetting −9.9 vs −4.8) is offset by about 1.4 points in η‖m̂‖'s favour on amazon and yahoo. One pair cannot separate a clock effect from GPU non-determinism amplified over three tasks. The 0.2-point task-0 difference measures noise right after training, not accumulated noise.
- **Port vs. code discrepancy.** In our port, η‖m̂‖ and τ triggered at the same steps, and reconstruction was ≈ 0.96. In their code, triggers come up to 33 steps later, and reconstruction on the replay tasks is 0.75. Candidate explanations, not tested:
  - fp16 + GradScaler vs. bf16;
  - the data restarting at each phase;
  - the different number of epochs;
  - chance.

## 5. Options for the next GPU budget (~15–30 h on the laptop; one arm = tasks 1–3 + generations = 7 h 24 min, measured in both R1 and R2)

**(a) Repeated runs on order 4** (preregistration v2 ready, hashed, verdict script tested). It is a 2 × 2 crossed design: clock × task-0 adapter, where A is R1's adapter and B is R2's, copied (a valid start for either clock, by facts 2–3).
- **Stage 1** (~15 h): η‖m̂‖ from A, τ from B.
- **Stage 2** (~15 h): τ from A again, η‖m̂‖ from A again.
- **Primary measure:** final dbpedia accuracy (exact match). Paired differences D = τ − η‖m̂‖ for (A,1), (B,1), (A,2). Noise N = max over clocks of |rep1 − rep2| on A.
- **Rule:**
  - "clock effect" if all three D > 2 and mean(D) > N;
  - "not attributable to the clock" if the signs are mixed, |mean(D)| ≤ 2, or |mean(D)| ≤ N;
  - otherwise "undecided".
  - Early stop after stage 1 if D(A,1) and D(B,1) have opposite signs.
- **It answers:** was the dbpedia gap clock or GPU noise, at seed 42? **It does not answer:** generalisation across orders or seeds.

**(b) Order 5** (dbpedia → amazon → agnews → yahoo; same 4 datasets, already local), both clocks, both starting from adapter A. Order 5's task 0 is the same training as order 4's task 0: same data, same seed.
- **Cost:** 2 arms, ~15 h (estimate; this order has not been timed).
- **It answers:** does equivalence hold on a second order, and does the first task (dbpedia) again lose more under η‖m̂‖? **Limit:** again one pair, so the same noise ambiguity. Order 6 (yahoo first, 60 epochs on the longest texts) is likely > 10 h for task 0 alone.

**(c) Stop GPU work** and write the closure report and the FOREVER note with the limits stated.

**(d) Zero-GPU analysis** of existing logs, post hoc, about 1 h. R2's drift log records both the η‖m̂‖ clock and Σ‖Δθ‖ along the same trajectory, so we can compute where τ's thresholds (calibrated the same way) would have been crossed on that trajectory. Only the first divergent trigger per task is clean, because the trajectory changes after a replay.
- **It answers:** do the clocks schedule differently on the same trajectory, free of non-determinism? **It does not answer:** whether that changes accuracy. It can be combined with (a) or (b).

**(e) Something else**, with a concrete design within the budget. Running other seeds would require editing `set_seed(42)` in their code.

## 6. What depends on it

The closure report and a short note on FOREVER will state, in their current draft:
- "with the authors' code (one order, one pair), replacing τ by η‖m̂‖ keeps OP and BWT within ±2 points";
- "dbpedia is 5.3 points lower under η‖m̂‖, unresolved";
- "η‖m̂‖ tracks Σ‖Δθ‖ at R² 0.92 overall, but 0.75 on tasks with replay";
- "in our port the schedules coincided".

The next step should make one of these statements stronger, weaker or more precise.

## 7. Decision rule (fixed before sending; full text in `Regula_de_decizie_2026-11-08.md`)

Three participants (ChatGPT, Gemini, Mistral), each with the same dossier and prompt and without seeing the others. Each answer is verified point by point against code, logs and references; a recommendation whose main argument rests on a false claim is dropped. The direction is the option with the most remaining votes. A tie goes to the cheaper, more falsifiable option. If no option keeps at least 2 votes, the default is (a) stage 1 only. Criticisms that survive verification and come from at least 2 participants are integrated into the plan or report; the others are listed. The owner may stop or postpone.
