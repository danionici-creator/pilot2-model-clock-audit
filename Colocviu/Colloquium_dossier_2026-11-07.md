# Colloquium dossier: Pilot 2 after the technical rounds of 4–6 November 2026

**Purpose.** This dossier asks several AI systems, independently and with the same questions, to analyse the results so far and to set the direction of the study: continue in a revised form, close a line of work with a decisive test, or take another direction. The author is an independent researcher and a non-specialist in machine learning; the direction will be set by a decision rule fixed before any answer is read (summarised in §8), not by the author's preference. **Your mandate is adversarial:** find what is wrong, trivial or unsupported, and name the test that would settle it.

**Status of every number below.** All results come from *technical rounds*: not preregistered, few runs (one seed per family on the synthetic world, three seeds per configuration on the language model). Each result is marked **[pre-fixed]** (analysis and criterion written before the run) or **[post hoc]** (added after seeing the data). The relation between any clock and forgetting has deliberately **never been analysed**, to keep a later confirmatory test clean.

---

## 1. Background

- **Perspective paper** (author, Zenodo 2026, v1.3, "A Time of Their Own"): a persistent AI agent whose state can be saved and restored holds no unforgeable evidence of elapsed time or of its own change. Its "Level 2" proposes an **experiential index** c_e(t) = Σ_steps D(S(t), S(t+1)), the accumulated change of the agent's own state under a distance D, read against an external clock. It says the question whether this index "carries information beyond logged optimizer statistics … remains open", and lists candidates "from cheap and weak to costly and valid".
- **Pilot 1** (closed, Zenodo): an apparent advantage of binding an episode to a summary of internal change disappeared once the control model was made competent; the signal was carried by local update statistics.
- **Pilot 2 protocol v0.4** (draft, not frozen). Confirmatory hypothesis H1: over an interval (t0, t1], Δc_e predicts the forgetting of a task last trained at t0 (target T1 = increase in loss on half A of the task's probe items) better than **B_strong**, the union of cheap online telemetry (elapsed steps ΔN, tokens, Σ learning rate, Σ loss, gradient norms, Adam moment norms, weight-decay path, parameter and second-moment norms, local update statistics, loss changes on a fixed reference battery R). Statistic: held-out increase in within-run R² when c_e is added. **Gate G2 (identifiability):** if the rate of Δc_e is reconstructible from B_strong (held-out R² ≥ 0.90), H1 is not identifiable as a test.
- **Candidates for D:** D1 = Euclidean norm of the full parameter update (the FOREVER clock); D1_rel = per-layer relative update; D2 = update weighted by a lagged second moment (Fisher-like); D3 = functional change, mean √JS divergence of the outputs on the reference battery R, accumulated over 8-step chunks; D4 = CKA on representations (secondary).
- **FOREVER** (Feng et al., ACL 2026, arXiv:2601.03938; code github.com/WoodScene/FOREVER, commit bbeb549, read by the author's assistant): "model-centric time" τ = Σ_t ‖θ_t − θ_{t−1}‖₂ over the LoRA factors, reset per task; a "model day" = τ after the first 24 steps of a task; replay is triggered when τ crosses d × day, d ∈ {1, 2, 4, 7, 15, 30, 60, 90, 120}. In the code, every phase (calibration, current-task phase, replay) is a new `transformers.Trainer`: a fresh AdamW (weight decay 0) and a fresh linear learning-rate schedule with warmup (10 steps; 5 for replay), fp16 with a fresh GradScaler; replay steps are not counted in τ and the reference point moves after replay; a replay at the end of each task; LoRA r = 8, α = 16 in the code (32 in the paper), q_proj and v_proj, batch 32 (8 in the paper). The paper's only ablation of the time signal is against step counts (+1.2% overall performance, one benchmark).

**Known theory** (from a literature check, 4 Nov 2026; IDs verified on arXiv): the RMS of an Adam step depends on the gradient signal-to-noise ratio (Kosson, Messmer & Jaggi, arXiv:2305.17212; Liu et al., arXiv:2502.16982: "AdamW's update RMS is usually around 0.2 to 0.4"). Hence ‖Δθ‖ ≈ η‖m̂‖/√v̄ is expected as a mechanism. No published audit of the FOREVER clock was found (13 citing papers in Semantic Scholar; none examines the clock). A workshop poster uses the path length of parameters as an "intrinsic clock" for weight averaging (Dao & Block, ICML 2026 workshop; text not read).

## 2. Set-ups

**Synthetic world (CPU).** Agent: pre-LN decoder-only Transformer, 4 layers, d = 128, 4 heads, d_ff = 512, vocabulary 512, context 4 tokens, 925,440 parameters, explicit AdamW (β 0.9/0.999, weight decay 0.01, clip 1.0, η 3 × 10⁻⁴; bit-identical to `torch.optim.AdamW`). World: 40 target tasks of 256 arbitrary facts each (key → value, 64 value tokens), 8 reference fact tasks (battery R, 256 items). "Childhood" of 3,072 steps on the reference tasks, then a "life" of 20,480 steps (512 per task) under one of six schedule families:
- F1: new task, then round-robin rehearsal of earlier tasks; constant η;
- F2: new tasks interleaved with re-exposures of random length; batch sizes 16/32/64; constant η;
- F3: as F1 with cosine learning-rate restarts (0.05× to 2× η, periods 512–4,096);
- F4: as F1 with idle pauses (no training, the external clock runs);
- F5: as F2 with more input overlap, pauses and learning-rate restarts;
- F6: regular target exposures plus distractor segments of variable length with 30% label noise.

**Language-model arm (GPU, RTX 3050 Laptop, 4 GB).** Qwen3-0.6B (the smallest model of FOREVER; weights SHA-256 verified against Hugging Face), the FOREVER schedule copied from their code as listed in §1. Data: synthetic facts "code ABC-DEF is WORD" (31 single-token answer words), 10 tasks per run, 512 (lmtech1) or 256 (lmtech2) facts per task, 60 epochs on task 0, 10 on the others, a memory buffer of 16 facts per previous task. Declared deviations: one batch of 32 instead of 4 × 8 accumulation; loss on the answer token; the meaning of FOREVER's `memory_data_ratio = 2` could not be checked (file missing at that commit); the task's batches form one stream across its phases. Telemetry per step: η, loss, gradient norm before and after clipping, GradScaler skips, ‖m̂‖, √Tr v̂, Δ_t on the factors (the τ increment) and on ΔW = 2BA. Functional distance D3 on 128 never-trained prompts (log-probabilities of the 31 answer words), every 8 counted steps.

**Determinism.** Repeated runs are bit-identical on the CPU (all checks, and a full corrected-code run: G7) and on the GPU (a full 10-task run repeated; all arrays identical).

## 3. Results on the synthetic world

**R1. G2 preview, tech2/tech3** (4 Nov; [pre-fixed as "blind to T1"], analysis written before running it, models untuned). Held-out R² of the rate ρ = Δc_e/ΔN predicted from B_strong; test on each tech3 run, training on the other four runs; ΔN ∈ [64, 1,280):

| D | B_strong, OLS | B_strong, GBDT | ΔN only | ΔN + Ση‖m̂‖ (one scalar) |
|---|---|---|---|---|
| D1 | 0.98–0.99 | 0.98–0.99 | −0.06–0.33 | 0.94 |
| D1_rel | 0.96–0.98 | 0.97 | −0.11–0.30 | 0.92 |
| D2 | 0.99 | 0.99 | −0.06–0.27 | 0.99 |
| D3 | 0.92–0.96 | 0.91–0.95 | −0.13–0.22 | 0.85 |

The rate varies substantially (coefficient of variation 0.37–0.73), so the families do decouple steps from change. **Under the protocol's own rule, G2 fails for all four candidates.**

**R2. Family F3 left out entirely** (6 Nov; [post hoc check, planned on 4 Nov]): training on runs without learning-rate restarts, test on the two F3 runs. ΔN + Ση‖m̂‖: D1 0.95–0.96, D1_rel 0.83–0.95, D2 0.98–0.99, D3 0.87 / 0.31 (the second with rule tasks, later removed). Flexible models extrapolate badly: OLS on all 58 B_strong features gives R² from −1.5 to −52; GBDT 0.68–0.94. Residuals of the one-scalar model: relative error 23% for intervals of 64–127 steps against 8% for long ones; after a learning-rate restart inside the interval, bias −5% (D1) and −21% (D3).

**R3. tech4, on code corrected after an external review** (6 Nov; [pre-fixed descriptive measures]; one seed per family F1–F6). Corrections: context 4 (was 8; positions 4–7 got no gradient), embeddings out of weight decay, input-overlap covariate taken before the segment, clipped loss, a new competitor C10c = mean over items of |change of the per-item loss| on R (same forward passes as D3), pause ticks as their own competitor. Childhood gate (reference accuracy ≥ 0.95) passed in 6 of 6 (0.982–0.985). G2 with one family left out (training on the other five):

| D | test | ΔN | ΔN + Ση | ΔN + Ση‖m̂‖ | ΔN + C10c | GBDT, all |
|---|---|---|---|---|---|---|
| D1 | F2 / F3 / F5 / F6 | 0.37 / −0.13 / 0.06 / 0.01 | 0.39 / 0.58 / 0.67 / 0.02 | **0.86 / 0.94 / 0.92 / 0.95** | 0.88 / 0.93 / 0.90 / −0.40 | 0.96 / 0.99 / 0.98 / 0.95 |
| D1_rel | same | 0.25 / −0.15 / 0.09 / −0.09 | 0.27 / 0.49 / 0.62 / −0.08 | 0.67 / 0.87 / 0.79 / 0.82 | 0.73 / 0.79 / 0.75 / −0.26 | 0.94 / 0.99 / 0.95 / 0.79 |
| D2 | same | 0.41 / −0.14 / −0.02 / −0.39 | 0.41 / 0.50 / 0.56 / −0.37 | **0.98 / 0.98 / 0.99 / 0.98** | 0.35 / 0.92 / 0.78 / −0.95 | 0.98 / 0.99 / 0.94 / 0.99 |
| D3 | same | 0.15 / −0.21 / 0.09 / 0.34 | 0.17 / 0.46 / 0.58 / 0.33 | 0.64 / 0.93 / 0.91 / **0.18** | **0.98 / 0.95 / 0.99 / 0.59** | 0.99 / 0.99 / 0.99 / **0.81** |

**F6 is the only family where no cheap scalar reconstructs the functional clock D3.**

**R4. Forgetting dynamics, tech4** (descriptive; no relation to any clock). Episode-weighted mean loss of accuracy on half A, by ΔN band 64–255 / 256–639 / 640–1,279 / 1,280–2,047 / ≥ 4,096: F1 0.11 / 0.40 / 0.67 / 0.83 / 0.98; F5 0.27 / 0.60 / 0.84 / 0.94 / 0.98; F6 0.29 / 0.64 / 0.79 / 0.87 / 0.98. Functional forgetting is nearly complete beyond ~1,280 steps, while the loss keeps rising (to 6.8–9.2 nats at ΔN ≥ 4,096); hence the protocol's cap ΔN < 1,280. F6 forgets faster at short intervals but more slowly on the loss scale at long ones.

## 4. Results on the language-model arm (FOREVER schedule)

**R5. lmtech1** (3 runs × 10 tasks × 512 facts; [pre-fixed analysis and prediction]). The prediction written on 4 Nov, before any LM data: "in the FOREVER setting the learning-rate schedule Ση explains most of τ" (operationalised as held-out R² ≥ 0.80 for the rate of τ in 8-step windows). Held-out R² (leave one seed out), 869 windows:

| Predictor of the τ rate | factors (τ) | ΔW = 2BA | D3 (functional) |
|---|---|---|---|
| Ση (schedule only) | **0.67** | 0.65 | 0.49 |
| Ση‖g̃‖ | 0.86 | 0.86 | 0.69 |
| Ση‖m̂‖ | **0.94** | 0.89 | 0.64 |
| mean-field Ση‖m̂‖·√d/√Tr v̂ | 0.94 | 0.89 | 0.64 |
| Ση + Ση‖m̂‖ | 0.96 | 0.91 | 0.66 |
| GBDT, all telemetry | **0.986** | 0.994 | 0.94 |

**The pre-fixed prediction fails** (0.67 < 0.80). Residuals of "rate ~ Ση": underestimation by 48–85% in the first windows of each phase (Adam steps are larger per unit η after the moment reset), overestimation by ~22% later in current phases.

**R6. lmtech2** (3 runs, 256 facts per task; same pre-fixed analysis): Ση 0.58, Ση‖g̃‖ 0.84, Ση‖m̂‖ 0.95, Ση + Ση‖m̂‖ 0.97, GBDT 0.976; D3: 0.36 / 0.64 / 0.53 / 0.55 / 0.93. **Replicates R5.**

**R7. [post hoc] Phase level and replay triggers** (lmtech1, lmtech2). τ per phase from Ση per phase: R² 0.975–0.991, but steps alone give practically the same (0.975–0.987): a duration artefact; with duration removed (rate per phase), Ση explains 0.09–0.18. Only the thresholds d = 1 and 2 are reached in the 80 counted steps of a task in lmtech2, and d = 1, 2, 4 in the 160 steps of lmtech1. A clock built only from the schedule (cumulative applied η, normalised by its own value after calibration) would trigger the d = 2 replay at the same step as τ (median difference −1 step) and the d = 4 replay about 9 steps earlier (median, out of ~85).

**R8. Validity failures and their diagnosis.** Two pre-fixed criteria failed in lmtech1 and again in lmtech2: (a) accuracy on the current task at the end of the task ≥ 0.95 failed in late tasks (0.85–0.94); (b) GradScaler skipped steps ≤ 2% failed (4.1% and 5.9%; a property of fp16 with a fresh GradScaler per phase). A diagnostic run, bit-identical in training, showed that the current task is learned perfectly (accuracy 1.000 at every task) **just before** FOREVER's end-of-task replay; the drop is caused by that replay on old facts. Results R5–R7 are therefore labelled descriptive.

**R9. Sensitivities** (6 Nov; the lmtech1 seeds 7101–7103 and 512 facts per task; [pre-fixed]: the same fixed analysis as R5, criteria written before the runs, including the decision to read the learning criterion **before** FOREVER's final replay and to report the value after it). Two changes, one at a time: bf16 without GradScaler (a deviation from FOREVER, which uses fp16), and α = 32 (the paper's value; their code has 16). Held-out R² (leave one seed out); 869, 869 and 873 windows:

| Predictor | τ rate: lmtech1 (fp16, α 16) | bf16 | α 32 | D3: lmtech1 | bf16 | α 32 |
|---|---|---|---|---|---|---|
| Ση (schedule only) | 0.669 | 0.648 | 0.686 | 0.490 | 0.475 | 0.460 |
| Ση‖g̃‖ | 0.858 | 0.848 | 0.879 | 0.693 | 0.635 | 0.672 |
| Ση‖m̂‖ | 0.944 | 0.958 | 0.941 | 0.639 | 0.605 | 0.661 |
| Ση + Ση‖m̂‖ | 0.960 | 0.969 | 0.956 | 0.657 | 0.621 | 0.666 |
| GBDT, all telemetry | 0.986 | 0.986 | 0.988 | 0.941 | 0.937 | 0.941 |

On ΔW = 2BA, Ση‖m̂‖ gives 0.887 / 0.900 / 0.922 and GBDT 0.994 / 0.995 / 0.992. At phase level, Ση gives R² 0.991 in all three (the duration artefact of R7). Validity: before the final replay, accuracy on the current task is ≥ 0.998 at every task in all six runs; after it, the minimum is 0.957 (bf16) and 0.973 (α 32), so the ≥ 0.95 criterion holds in all six runs even after the replay, unlike lmtech1 on the same seeds (0.920 and 0.941). Skipped steps: none with bf16; with α 32, 304 of 6,984 steps in windows (4.4%), as in lmtech1 (283 of 6,952, 4.1%). **Reading:** neither the fp16 skipped steps nor α changes the reconstruction result: Ση‖m̂‖ gives 0.94–0.96 for the τ rate, and the schedule-only prediction fails in all three configurations (0.65–0.69 < 0.80). With three seeds per configuration, the difference in post-replay accuracy is not attributed to a cause.

## 5. Infrastructure facts

Throughput on the laptop (ASUS Turbo mode, mains power): 12.3 synthetic-world runs per hour with 4 parallel processes; pinning the 4 processes to the 4 performance cores shortens childhood by ~15% (E-cores: +60%), with identical results; ~15 min per 10-task LM run on the GPU. Temperatures stay below the processor limit without firmware throttling.

## 6. What the results do not say

- Nothing about whether any clock predicts forgetting better than telemetry (H1): never analysed.
- Nothing about FOREVER's benchmark gains: their data (SuperNI), models above 0.6B and their evaluation were not reproduced; the LM arm uses synthetic facts.
- Small samples; several analyses are post hoc; the synthetic world has fact tasks only (in-sample retention).
- On the language-model arm, no same-cost competitor of D3 (the analogue of C10c: mean change of the per-item loss on the same probes) has been computed, although the stored probe outputs allow it (each probe prompt has a random answer word that is never trained); the D3 columns of R5, R6 and R9 compare D3 with optimizer telemetry only.

## 7. Open decisions (the options as currently framed)

1. **Form of the confirmatory Stage A:** (B) the synthetic world as the main study plus a descriptive LM module; (C) only a small LM study; (R) restructured: four families (F1, F2, F3, F6), reconstruction (G2) promoted to a primary result for every candidate, the ladder of competitors including C10c, a confirmatory H1 only where room remains (D3 against C10c; the F6 contrast), the LM module descriptive.
2. **Stage 0 split into 0a (blind to the c_e–T1 relation, the only phase allowed to change the design) and 0b (automatic after the design is locked).**
3. **Stage B** (using the clock to schedule rehearsal, budget Q): now or postponed.
4. **Embeddings out of weight decay:** fully (applied provisionally) / unused rows only / not at all.
5. **LM learning criterion:** before or after FOREVER's final replay.
6. **LM precision:** fp16 with GradScaler (as FOREVER) or bf16.
7. **C10c mandatory in the ladder of D3.**
8. **A short, separate, descriptive note on the FOREVER clock** before Stage A, or not.

## 8. How your answer will be used

Your answer will be verified claim by claim (numbers against this dossier and the logs, statements about code against the code, every reference against arXiv, Crossref or DataCite). Recommendations resting on a false claim are struck out. The direction is the option recommended by most participants whose recommendation survives verification; ties go to the option that is more falsifiable and cheaper on this laptop. Tests proposed by at least two participants are preregistered first. Please therefore end with the fixed answer block requested in the prompt.
