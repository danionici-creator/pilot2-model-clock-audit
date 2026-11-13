# Does a model-centred clock carry information beyond optimizer telemetry? Closure report of Pilot 2

Ioan Daniel Ionici, independent researcher, Oradea, Romania. ORCID 0009-0009-8183-3656.

Draft for review, 9 November 2026 (not for citation). Code, preregistrations and logs: an archive to be published with this report (DOI to be assigned).

## Abstract

The Perspective paper *A Time of Their Own* (v1.3) left open whether an agent's accumulated internal change, an "experiential index" c_e, carries information beyond the statistics an optimizer logs anyway. Pilot 2 set out to test this on a synthetic continual-learning world and on a small language model trained with the schedule of FOREVER, a recent method that triggers replay with a "model-centric" clock τ = Σ‖Δθ‖. The confirmatory test was never reached: in our implementations, every candidate clock (three parameter-space distances, a functional distance, and τ itself) was reconstructed from cheap telemetry or from same-cost competitors with held-out R² ≥ 0.90 (exceptions only under extrapolation to a schedule family left out of training), which makes the planned hypothesis unidentifiable under the protocol's own rule. Driving FOREVER's replay with the free clock Ση‖m̂‖ (learning rate times the norm of Adam's first moment) instead of τ left retention within the preregistered margins in our port (synthetic facts, 5 seeds; SuperNI, 3 seeds) and, in aggregate, with the authors' own code (three pairs of runs, seed 42, after reproducing their reported score within 0.53 points). In the authors' fp16 code, Ση‖m̂‖ triggers replay systematically later than τ (by 0–36 of 313 steps). In the first pair one task differed by 5.3 points; repeated from common starting points in a preregistered 2 × 2 design (clock × task-0 adapter), the difference did not recur consistently (−0.5 and +3.3 points), so it cannot be attributed to the clock. The line "own time as accumulated internal change" is closed in this framework as a documented negative result.

## 1. The question and the outcome in brief

**Question.** Perspective v1.3 (Ionici 2026c, Level 2) defines an experiential index c_e(t) = Σ_{τ<t} D(S(τ), S(τ+1)), the accumulated change of an agent's own state under a distance D, read against an external clock, and states that whether it "carries information beyond logged optimizer statistics … remains open". Candidates range "from cheap and weak to costly and valid". Version 1.2 had said of the proposed tests that "the author does not plan to pursue them"; Pilot 2 was undertaken afterwards as a change of plan (version 1.3 says only that "the tests are offered to others"), and this report closes it.

**Outcome.**
1. *Reconstruction (identifiability).* In every setting of our own implementations (synthetic world, LM port, SuperNI port), the rate of each candidate clock is predicted out of sample from cheap online telemetry, or from a competitor computed from the same forward passes, with R² ≥ 0.90 (§5.1; the exceptions, all under extrapolation to a schedule family left out of training, are named there). Under the protocol's gate G2 this makes the confirmatory hypothesis H1 (c_e predicts forgetting beyond telemetry) not identifiable, so H1 was never run and the forgetting targets were never opened.
2. *Scheduling.* Triggering FOREVER's replay with Ση‖m̂‖, with the learning-rate schedule alone, or with the step count gave retention within the preregistered margins of the τ-driven schedule in our port, and in aggregate with the authors' code (§5.2).
3. *The exception, and what remains of it.* With the authors' code the two clocks schedule replay differently: Ση‖m̂‖ triggers later than τ, systematically (in 16 of 17 comparable triggers of two pairs, once at the same step, never earlier; up to 36 of 313 steps). In the first pair of runs the first task differed by 5.3 points. Repeated from common starting points (preregistered 2 × 2 design, clock × task-0 adapter), the difference had opposite signs in the two pairs (−0.51 and +3.29 points); under the rule fixed beforehand it is **not reproduced robustly** and cannot be attributed to the clock. The reconstruction R² on tasks with replay, 0.75 in the first pair (post hoc), was 0.97 in the repeated run (§5.1, §5.2).

What is closed is the empirical line "own time = accumulated internal change" as a source of information beyond telemetry, *in this framework*: small models (a 0.93 M-parameter Transformer; Qwen3-0.6B with LoRA), synthetic facts, five SuperNI tasks and four classification tasks. Nothing here concerns large models, full fine-tuning or subjective experience.

## 2. Background

**FOREVER** (Feng et al. 2026, ACL 2026, arXiv:2601.03938; code github.com/WoodScene/FOREVER, commit bbeb549) defines model-centric time τ = Σ_t ‖θ_t − θ_{t−1}‖₂ over the LoRA factors, reset per task. A "model day" is the value of τ after the first 24 steps of a task; replay from a small memory buffer is triggered when τ crosses d × day, d ∈ {1, 2, 4, 7, 15, 30, 60, 90, 120} (the paper writes {1, 2, 4, 7, 15, 30, …}; the full list is in the code), and the replay strength β is set from the same update norms. The paper's only ablation of the time signal is against a step-based calibration (+1.2 points of overall performance and +1.1 BWT; Table 2, one benchmark: SuperNI, task order 7), and it reports that τ_day does not correlate with final forgetting across tasks (r = 0.2182, p = 0.4536; Appendix C).

**Known mechanism.** For Adam-type optimizers the size of a step is set by the learning rate and by the ratio of the first moment to the root of the second, so that ‖Δθ‖ ≈ η‖m̂‖/√v̄ (Kosson, Messmer & Jaggi 2024; Liu et al. 2025, who report that AdamW's update RMS "is usually around 0.2 to 0.4"; see also Wang & Aitchison 2025). A close relation between τ and the free quantity Ση‖m̂‖ is therefore expected; the question was whether the remainder carries information that matters. No published audit of the FOREVER clock was found: Semantic Scholar listed 13 citing papers on 4 Nov 2026 and 13 on 9 Nov, and none examines the clock (checked on 4 Nov, and again on 9 Nov from the abstracts of the seven most recent).

**Other uses of accumulated change.** FOREVER is the method tested here, but the question concerns a class of methods that read the accumulated change of a model as a clock, a control signal or a measure of importance.
- Path-based learning-rate schedules compare the cumulative path of the parameters with that of a random walk, also for Adam (Atamna et al. 2025).
- Synaptic Intelligence accumulates, for each parameter, the contribution of its updates along the trajectory (Zenke, Poole & Ganguli 2017). Benzing (2022) showed that this importance, like that of MAS, approximates the square root of the Fisher information, a statistic of the gradients, and that for SI the relation, "and in fact its performance", is due to a previously unknown bias. This is the same pattern as here, at the level of single parameters.
- Work on the magnitude of updates as a cause of forgetting studies a quantity that, under Adam, the optimizer sets (He, Bai & Yang 2026).
- Schedulers of repetition decide when to review training items from estimated forgetting delays (Amiri, Miller & Savova 2017), or which stored samples to replay from the interference of the next update (Aljundi et al. 2019).

The results of §5 bear on these classes to different degrees. On path-based clocks they bear most directly, since under Adam the path length is to first order a sum the optimizer already keeps. On per-parameter importance they extend a published pattern without testing it. On schedulers of repetition they suggest including the schedule-only clock and the step count as baselines, and no more: those methods also choose what to repeat, and the regimes tested here were narrow. Costlier quantities integrated along the trajectory, such as the influence of training examples traced through training (Pruthi et al. 2020), lie outside what was tested.

**Pilot 1** (Ionici 2026a, b) found that an apparent advantage of binding episodes to a summary of internal change disappeared once the control model was made competent; the signal was carried by local update statistics. Pilot 2 asked the same question of the clock itself.

## 3. How the plan changed (an honest timeline)

The study did not follow one frozen protocol. The order of events matters for reading the results.

| Date (2026) | Step | Record |
|---|---|---|
| 27 Oct – 4 Nov | Protocol drafts v0.1–v0.4: confirmatory H1 with gate G2; Stage A (prediction of forgetting), Stage B (scheduling) | `Versiuni_anterioare/`, `Pilot2_Protocol_EN_draft.md` (v0.4) |
| 27 Oct – 4 Nov | AI evaluations of drafts v0.1–v0.4, each verified point by point (for v0.4, six points judged fatal after verification); direction opinions from five AI systems on 4 Nov | `Recenzii/` (informative annex; see its README) |
| 4 Nov | Stage 0 technical rounds: **G2 preview fails for all candidates** (R² 0.91–0.99) | `Stadiul0/Stadiul0_note_lucru.md` §9 |
| 4–6 Nov | LM arm (Qwen3-0.6B + LoRA, FOREVER schedule ported): τ rate reconstructed (0.94–0.96) | dossier of 7 Nov, R5–R9 |
| 6 Nov | Colloquium of five AI systems under a decision rule fixed in advance: **direction C** (close the parameter-clock line; one decisive test per open exception), 4 votes to 1 | `Colocviu/Regula_de_decizie.md`, `Verificare_raspunsuri_2026-11-06.md` |
| 6–7 Nov | Decisive tests T-A, T-B (preregistered), T-C, T-D (criteria fixed before computing) | `Stadiul0/preinregistrare_TA_TB_2026-11-06.md`, `lm/tc_criterii.md`, `td_criterii.md` |
| 7 Nov | SuperNI check S1, S2 (preregistered) | `Stadiul0/preinregistrare_SuperNI_2026-11-07.md` |
| 7–8 Nov | Reproduction with the authors' code, R1 (τ) and R2 (η‖m̂‖) (preregistered + one addendum) | `Stadiul0/forever_repro/preinregistrare_FOREVER_repro_2026-11-07.md` |
| 8 Nov | Short colloquium on the R2 per-task difference: analysis (d) + stage 1 of repeated runs, 3 votes of 3 | `Colocviu/Regula_de_decizie_2026-11-08.md`, `Verificare_raspunsuri_2026-11-08.md` |
| 8–9 Nov | Stage 1 of repeated runs (preregistered, v3): not reproduced robustly (D_A1 −0.51, D_B1 +3.29); stage 2 not needed for the verdict, not run | `Stadiul0/forever_repro/preinregistrare_FOREVER_repetari_2026-11-08.md`, `runs/forever_repetari_verdict.json` |

Two consequences. First, **the confirmatory study was never run**: the closure rests on identifiability (G2) and on scheduling comparisons, not on H1. The forgetting columns of the synthetic world (T1) were never opened. Second, **preregistration here means local**: each preregistration, with the code and analysis scripts it names, was hashed (SHA-256) before the runs it governs, and the hash lists are in the archive; but none was deposited publicly before running, so the timing is attested only by the author's own records (§7).

## 4. Set-ups

**Synthetic world (CPU).** Pre-LN decoder-only Transformer, 4 layers, d = 128, 4 heads, vocabulary 512, context 4 tokens, 925,440 parameters; explicit AdamW (β 0.9/0.999, weight decay 0.01, clip 1.0, η 3 × 10⁻⁴), bit-identical to `torch.optim.AdamW`. Forty target tasks of 256 arbitrary key → value facts and a reference battery R of 256 items; a "childhood" of 3,072 steps, then a "life" of 20,480 steps under one of six schedule families (F1 round-robin rehearsal; F2 interleaved re-exposures with varying batch sizes; F3 cosine learning-rate restarts; F4 idle pauses; F5 a mixture; F6 distractor segments with label noise). Candidates for D: D1, the Euclidean norm of the parameter update; D1_rel, the per-layer relative update; D2, the update weighted by a lagged second moment; D3, the functional change (mean √JS divergence of outputs on R, over 8-step chunks). Telemetry ("B_strong"): steps, tokens, Ση, Σ loss, gradient and Adam-moment norms, weight-decay path, parameter norms, local update statistics, loss changes on R. Same-cost competitors of D3 from the same forward passes: C10c (mean |change of the per-item loss| on R), C10p (mean |Δ p(target)|), C10h (mean |Δ output entropy|). Runs are bit-identical on repetition.

**Language-model arm, port (GPU, RTX 3050 Laptop, 4 GB).** Qwen3-0.6B (Yang et al. 2025) with LoRA (Hu et al. 2021; r 8, α 16, q_proj and v_proj; 1,146,880 trainable parameters), the FOREVER schedule re-implemented from their code; synthetic facts "code ABC-DEF is WORD" (31 answer words), 10 tasks, 60 epochs on task 0 and 10 on the others, memory of 16 facts per earlier task; per-step telemetry (η, loss, gradient norms, GradScaler skips, ‖m̂‖, √Tr v̂, the τ increment). Declared deviations from FOREVER: one batch of 32 instead of 4 × 8 accumulation, loss on the answer token, one data stream across a task's phases, bf16 in T-A. Runs are bit-identical on repetition on the GPU.

**SuperNI (port).** The first five tasks of FOREVER's order 7 of Super-NaturalInstructions (Wang et al. 2022): task1572, task363, task1290, task181, task002; with their Qwen script settings (micro-batch 4 × 8, up to 512 tokens, 2 memory epochs, 2% memory per earlier task) and declared deviations (bf16; 3 / 10 epochs instead of 10 / 60; no length grouping; memory rule corrected for generation tasks).

**Authors' code.** FOREVER at commit bbeb549 with their library versions (torch 2.8.0+cu128, transformers 4.57.0) in a separate environment, on the same laptop GPU (RTX 3050 Laptop, 4 GB, Windows 11). The authors ran their experiments on 8 NVIDIA H20 GPUs (Appendix H). Their scripts assign one GPU to each job (`CUDA_VISIBLE_DEVICES`, `torchrun --nproc_per_node=1`), so a single run does not depend on several GPUs. The code itself names no hardware. We used their arguments for Qwen3-0.6B, the "Standard CL" sequence dbpedia → amazon → yahoo → agnews (classification datasets of Zhang, Zhao & LeCun 2015; `dataset_id` 4 in their repository = order 1 of the paper, Appendix G, Table 14), seed 42 as fixed in their code, their evaluation scripts unchanged. The adaptations, all documented and hashed: local model-cache path; test-data path in the two generators (hard-coded to the SuperNI folder); `python` instead of `torchrun` on one GPU, with a UTF-8 console and Hugging Face offline mode; the training script's actual file name (§8, note 3); and, for tasks 1–3, the PyTorch allocator without caching (`PYTORCH_NO_CUDA_MEMORY_CACHING=1`; the 4 GB card ran out of memory otherwise; arithmetic unchanged). The clock-swap variant changes only the counter that triggers replay; β is still computed from ‖Δθ‖.

## 5. Results

### 5.1 Reconstruction of the clocks (gate G2)

**Synthetic world, technical rounds** (pre-fixed as blind to forgetting; models untuned). Held-out R² of the rate of each candidate, test on each tech3 run, training on the other runs:

| D | B_strong, OLS | B_strong, GBDT | ΔN only | ΔN + Ση‖m̂‖ |
|---|---|---|---|---|
| D1 | 0.98–0.99 | 0.98–0.99 | −0.06–0.33 | 0.94 |
| D1_rel | 0.96–0.98 | 0.97 | −0.11–0.30 | 0.92 |
| D2 | 0.99 | 0.99 | −0.06–0.27 | 0.99 |
| D3 | 0.92–0.96 | 0.91–0.95 | −0.13–0.22 | 0.85 |

Source: `Stadiul0/g2_preview.py`; `Stadiul0_note_lucru.md` §9. The rate varies substantially (coefficient of variation 0.37–0.73), so the schedule families do decouple steps from change; steps alone explain little. These rounds (4 Nov) ran with an earlier configuration and code than the one described in §4, before the corrections of 6 Nov. Among the differences: a context of 8 tokens instead of 4, and in tech2 also rule tasks and a different reference battery. The resolved configuration of each run is in its `meta.json`; the code of that day was not kept (§7). The tech4 round and T-B, run with the corrected code, give the same picture (below).

**T-D, audit of the reconstruction** (criteria fixed before computing). (1) Without the features that contain D1's own statistics (C6), the result is unchanged (e.g. D1 0.983–0.994 OLS). (2) With the mechanism of the test family left out of training, the one-scalar model ΔN + Ση‖m̂‖ reconstructs D2 everywhere (0.977–0.983) and D1 in F2, F3 and F6 (0.90–0.95) but **not in F1 and F4** (0.41 and 0.35), where flexible models on all telemetry still give 0.97 and 0.96. D1_rel and D3, reported but outside the fixed reading, stay below 0.90 in some families even with GBDT on all telemetry (D1_rel 0.74 in F3 and 0.82 in F6; D3 0.80 in F6). (3) By interval length, the one-scalar reconstruction of D1 is weakest for the shortest intervals (R² 0.78 at 64–127 steps). (4) On the LM arm, a linear model on Ση + Ση‖m̂‖ trained on one configuration transfers to the other three at 0.956–0.971. Source: `runs/td_audit.log`. Reading under the fixed rule: robust, with a limited exception (D1 with a single scalar in F1/F4).

**T-B, the functional clock D3 under dosed label noise** (preregistered; 40 new runs, seeds 9101–9108). D3 and D1_rel were the candidates with an apparent exception (F6 left out of training, one seed: GBDT R² 0.81 and 0.79; `runs/tech4_analysis.log`); D3 was the one preregistered for T-B. On 8 new seeds per condition, leaving one seed out within the condition, GBDT on telemetry plus the same-cost competitors reconstructs D3 at R² 0.991 at noise 0.3 (minimum 0.968; 0 of 8 seeds below 0.90; ΔN + C10c alone 0.958), and at ≥ 0.990 at noise 0, 0.1, 0.5 and in F1. D1_rel, reported from the same runs, is reconstructed by the same GBDT at 0.993–0.994 in every condition. The dose–response criterion passes formally (unexplained share 0.003 / 0.004 / 0.009 / 0.010, monotone) but the unexplained variance stays ≤ 1%. **G2 fails for D3; by the preregistered rule H1 was not run.** Source: `runs/tb_part1_g2.log`, `runs/tb_part1_verdict.json`. The earlier exception was an artefact of extrapolating across families with one seed.

**T-C, D3 on the language model** (criteria fixed before computing). The same-cost competitor C10c_LM (the change of loss on each probe's never-trained random answer word) reconstructs D3 at mean R² 0.979–0.988 alone and 0.980–0.989 with two further competitors, in all four LM configurations (minimum over seeds 0.979). Verdict: reconstructed. Source: `runs/tc_lm_d3_competitors.log`.

**The τ clock on the LM arm (port).** Held-out R² (leave one seed out) of the rate of τ in 8-step windows: Ση alone 0.58–0.69 (a pre-fixed prediction that the schedule would explain ≥ 0.80 failed); Ση‖m̂‖ 0.94–0.96; Ση + Ση‖m̂‖ 0.96–0.97; GBDT on all telemetry 0.976–0.988, in four configurations (fp16/bf16, α 16/32). Source: `runs/lmtech1_g2.log`, `lmtech2_g2.log`, `lmsens_bf16_g2.log`, `lmsens_a32_g2.log` (colloquium dossier of 7 Nov, R5, R6, R9).

**SuperNI, S1** (preregistered; 3 runs, 128 windows). OLS on Ση + Ση‖m̂‖ reconstructs the rate of τ at R² 0.986 with one seed left out (minimum 0.985) and **0.980 with a whole task left out** (minimum 0.969 over five heterogeneous tasks). Ση‖m̂‖ alone: 0.963 / 0.956; Ση alone: 0.51 / 0.44; GBDT: 0.94 / 0.72 (it extrapolates poorly to unseen tasks). Verdict: the reconstruction extends to natural tasks. Source: `runs/sni_S1_analysis.log`, `runs/sni_verdict.json`.

**Authors' code** (secondary, preregistered script). On R2's run, Σ‖Δθ‖ from the increments of Ση‖m̂‖ in 8-step windows: pooled R² 0.922 (351 windows), but by task 0.937 (dbpedia, no replay), 0.986, 0.934 and **0.578 (agnews)**. Post hoc, on the tasks with replay only: **0.749** (117 windows). Source: `runs/forever_repro_r2_reconstruction.log`, `runs/forever_repetari_r2_eta_m.json`. Analysis (d), fixed before running and without new training: on the same trajectory, the ratio Σ‖Δθ‖ / Ση‖m̂‖ drifts within a task (the ratio in the calibration window divided by the ratio over the rest of the task: 0.967, 0.861, 0.705 on amazon, yahoo, agnews; post hoc), so the 24-step calibration freezes a factor that later changes. This is a hypothesis about the mechanism, not a finding. In the repeated Ση‖m̂‖ arm of stage 1 (`eta_m_A1`, task-0 adapter of R1), the same computation on tasks 1–3, preregistered for this arm, gives **0.969** (amazon 0.986, yahoo 0.975, agnews 0.963; `runs/forever_repetari_r2_eta_m_A1.json`): the weak value of R2 did not recur. The calibration-to-rest ratio of that arm, computed post hoc in the same way, drifts in the same direction but less (0.966, 0.903, 0.810; both arms: `Stadiul0/forever_repro/drift_ratio_posthoc.py`, `runs/forever_drift_ratio_posthoc.log`; the τ runs do not log the Ση‖m̂‖ clock, so the ratio cannot be computed there). The drift hypothesis therefore remains compatible with two runs, while the weak R² on agnews belongs to one run.

### 5.2 Scheduling: does the τ clock schedule replay better than a free clock?

**T-A, port, synthetic facts** (preregistered; 4 clocks × seeds 7301–7305, bf16; margin ±2 points on final mean accuracy).

| τ versus | mean difference in final accuracy | paired 95% CI | verdict | triggers |
|---|---|---|---|---|
| Ση‖m̂‖ | −0.0037 | [−0.0147; +0.0074] | practical equivalence | practically identical (median \|Δ\| 0 / 0 / 1 step) |
| Ση (schedule only) | +0.0023 | [−0.0041; +0.0086] | practical equivalence | differ (9 steps at d = 4; 36 vs 27 replays) |
| steps | −0.0018 | [−0.0106; +0.0070] | practical equivalence | — |

Mean final accuracy 0.240–0.246 in all arms; BWT ≈ −0.83. Source: `runs/ta_analysis.log`, `runs/ta_verdict.json`. Retention is low in this regime (memory of 16 facts out of 512 per task), so equivalence is shown under strong forgetting only.

**SuperNI, S2** (preregistered; 3 seeds; margin ±5% on test loss). Relative difference τ − Ση‖m̂‖: −0.6%, 95% CI [−1.9%; +0.7%]: practical equivalence. Replay triggers coincided (median difference in trigger step 0 in each seed; 7 replays in both arms). Source: `runs/sni_analysis_final.log`, `runs/sni_verdict.json`, `runs/sni_S2_secundar.log` (recomputed byte for byte by `Stadiul0/sni_s2_secondary.py`).

**Authors' code, R1: reproduction** (criterion: overall performance OP within ±5 points of the paper's 72.9). OP 72.37 (dbpedia 93.2, amazon 47.5, yahoo 60.3, agnews 88.4); BWT −5.78 (paper −4.7). **FOREVER reproduced** (difference −0.53). The paper's figure is a mean over three orders; this is one run on one order. Source: `runs/forever_repro_eval_tau.log`.

**Authors' code, R2: τ replaced by Ση‖m̂‖** (criterion: |ΔOP| ≤ 2, descriptive; not a statistical equivalence test).

| | τ (R1) | Ση‖m̂‖ (R2) | τ − Ση‖m̂‖ |
|---|---|---|---|
| OP (exact match) | 72.37 | 71.53 | +0.84 |
| dbpedia | 93.21 | 87.89 | +5.33 |
| amazon | 47.52 | 48.92 | −1.40 |
| yahoo | 60.34 | 61.66 | −1.32 |
| agnews | 88.40 | 87.65 | +0.75 |
| BWT | −5.78 | −6.47 | +0.69 |

Source: `runs/forever_repro_eval_tau.log`, `runs/forever_repro_eval_eta_m.log`. Both aggregate differences are inside the preregistered margin. Ση‖m̂‖ triggered the same number of replays, at the same step or later (up to 33 of 313 steps). The aggregate hides a 5.33-point difference on dbpedia in τ's favour (its forgetting −9.9 against −4.8), partly offset on amazon and yahoo. With one pair of runs, the clock cannot be separated from run-to-run non-determinism (fp16; stochastic decoding at evaluation).

**Repeated runs, stage 1** (preregistered v3; 2 × 2 crossed design, clock × task-0 adapter, the adapters of R1 and R2 reused so that the pairs share a starting point; margin 2 points on dbpedia). A = task-0 adapter of R1, B = that of R2; the two differ only by GPU non-determinism in task 0 (dbpedia right after it: 98.04 and 97.86). Each new arm copies the task-0 folder and runs tasks 1–3 with the authors' commands.

| Arm | Clock | Task 0 | dbpedia | amazon | yahoo | agnews | OP | BWT |
|---|---|---|---|---|---|---|---|---|
| R1 (`tau`) | τ | A | 93.21 | 47.52 | 60.34 | 88.40 | 72.37 | −5.78 |
| `eta_m_A1` | Ση‖m̂‖ | A | 93.73 | 49.36 | 61.86 | 87.20 | 73.04 | −4.79 |
| `tau_B1` | τ | B | 91.17 | 49.84 | 61.76 | 87.45 | 72.56 | −4.69 |
| R2 (`eta_m`) | Ση‖m̂‖ | B | 87.89 | 48.92 | 61.66 | 87.65 | 71.53 | −6.47 |

Pairs sharing a task-0 adapter, τ − Ση‖m̂‖: on dbpedia (the quantity of the verdict) D_A1 = −0.51 and D_B1 = +3.29; OP −0.67 and +1.03; BWT −0.99 and +1.78. **Verdict under the rule fixed beforehand: not reproduced robustly.** The signs are opposite, so the data do not support a stable attribution of the dbpedia difference to the clock. This does not mean that the clock has no effect: with one run per cell, run-to-run noise and an interaction between clock and starting point cannot be separated. Stage 2 is not needed for the verdict and was not run. In all three pairs (R1–R2, A1, B1) the differences in OP and BWT stay within ±2 points. Descriptively, changing the task-0 adapter from A to B moved final dbpedia by 2.04 points under τ and by 5.84 under Ση‖m̂‖. Across the four cells, final dbpedia spans 5.84 points and OP 1.51.

Replay triggers (step at which the clock crossed each threshold; the first is at step 24 by construction):

| Task | τ, R1 (A) | Ση‖m̂‖, A1 | τ, B1 | Ση‖m̂‖, R2 (B) |
|---|---|---|---|---|
| amazon | 24, 48, 100, 185 | 24, 50, 105, 196 | 24, 48, 100, 183 | 24, 50, 104, 192 |
| yahoo | 24, 46, 87, 160 | 24, 47, 90, 165 | 24, 46, 90, 164 | 24, 48, 96, 178 |
| agnews | 24, 47, 93, 160 | 24, 50, 105, — | 24, 47, 90, 157 | 24, 47, 96, 193 |

Within each pair, Ση‖m̂‖ triggered later than τ in 16 of the 17 comparable triggers, once at the same step and never earlier (0–36 steps). The two τ runs, which start from different adapters, differ by at most 4 steps. On agnews with adapter A, Ση‖m̂‖ did not reach the fourth threshold before the end of the task, so it made one clock-triggered replay fewer. The delay is systematic, as analysis (d) found on a single trajectory; in these two pairs it did not translate into a consistent difference in retention. Integrity checks: the copied task-0 adapters carry the hashes of their sources, the files of R1 and R2 were not modified, every stage returned 0. Source: `runs/forever_repetari_verdict.json`, `runs/forever_repro_eval_*.log`, `Stadiul0/forever_repro/logs/*_train_t*.log`.

### 5.3 What each clock costs

The four clocks compared as replay triggers differ in what they compute at every training step. Listed from the code (`Stadiul0/lm/lm_forever_run.py`; the clock-swap variant of FOREVER's script); the run time of each was not measured separately.

| Clock | Computed at each step | Extra memory | Reads the model's parameters? |
|---|---|---|---|
| Steps | a counter | none | no |
| Ση (applied learning rate) | the scheduler's current rate, added to a sum | none | no |
| Ση‖m̂‖ | the norm of Adam's first moment, already kept by the optimizer, with its bias correction, times the rate | none beyond the optimizer's own state | no |
| τ = Σ‖Δθ‖ (FOREVER) | the difference between the trainable parameters and their copy from the previous step, and its norm | one copy of all trainable parameters | yes |

For the LoRA set-up of FOREVER on Qwen3-0.6B (r 8 on q_proj and v_proj), the trainable parameters number 1,146,880, so τ's copy takes about 4.6 MB in fp32, which is small. Under full fine-tuning, which FOREVER also reports, the copy would be the size of the whole set of trained weights. The practical advantage of Ση‖m̂‖ is therefore modest but definite: it uses only what the optimizer already holds.

## 6. What this closes, and what it does not

**Closed, in this framework.** In our implementations, every candidate for c_e tested here (D1, D1_rel, D2, D3 and FOREVER's τ) is reconstructed out of sample from cheap telemetry or same-cost competitors (R² ≥ 0.90; the exceptions named in §5.1 all come from extrapolation to a schedule family left out of training, and those of D3 and D1_rel in F6 did not recur in T-B, where F6 itself was sampled with new seeds and one seed was left out), so the hypothesis that c_e predicts forgetting beyond telemetry is not identifiable here. Used as a replay scheduler, τ gave no measurable advantage over free clocks in our port, on synthetic facts and on SuperNI. With the authors' code, in three pairs of runs, OP and BWT stayed within ±2 points, and the 5.3-point difference on the first task did not recur consistently from common starting points (§5.2). Perspective's Level 2 is revised accordingly (Ionici 2026c, v1.4): c_e remains a definition; the open question is answered negatively for the candidates tested.

**A reading of the scheduling results.** In the regimes tested, the exact moment of replay, within the range produced by the clocks compared, did not change retention measurably. In T-A the schedule-only clock and the step count triggered replay up to 9 and 13 steps away from τ (median differences), and the schedule-only clock made 36 replays per run on average against 27 for τ (`runs/ta_analysis.log`), yet every paired 95% interval of the difference in final accuracy stayed within ±0.015. With the authors' code, Ση‖m̂‖ triggered later than τ in both pairs of stage 1 (up to 36 steps) and, on one task, made one replay fewer, yet the dbpedia difference had opposite signs in the two pairs (−0.51 and +3.29 points) and OP stayed within ±2. This is an observation about these regimes, not evidence for a class of clocks defined by general conditions: no such conditions were fixed in advance; the step count, which tracks no change in the model at all, did as well as τ in T-A; T-A had strong forgetting (final accuracy about 0.24) and a small memory; and on the authors' benchmark the paper reports +1.2 points of overall performance (+1.1 BWT) for τ over a step-based calibration (Table 2, one benchmark), a comparison not repeated here with their code.

**Not closed.** (i) Whether the systematic delay of Ση‖m̂‖ in the authors' fp16 code has an effect on retention smaller than the run-to-run variation seen here (several points on one task): settling that would need many runs per cell, other seeds and other orders. (ii) Larger models, full fine-tuning, other optimizers, longer task sequences. (iii) Forgetting regimes with good retention for the synthetic-fact comparison (T-A had strong forgetting). (iv) Candidates outside this list (for example representation-similarity measures, listed as secondary and never tested).

**What would overturn or bound these conclusions.** Each item is a test that someone else can run with the archived code and rules. Inside this framework, a positive outcome would overturn the corresponding verdict; in another setting it would mark a limit of it.
1. *Identifiability.* A setting in which a candidate's rate is not reconstructed out of sample, with R² < 0.90 for both the linear and the flexible model on the same telemetry and same-cost competitors (gate G2), and without extrapolation to a schedule family left out of training. G2 would then pass, and H1 could be tested.
2. *Scheduling.* A preregistered comparison with a margin of 2 points in which τ beats Ση‖m̂‖, or the schedule-only clock, with a mean difference of at least 2 points and a paired 95% interval above zero (the criterion of T-A).
3. *The authors' code.* A difference on one task that keeps its sign and size across many runs per cell, over other seeds and task orders. This is the test that stage 1 could not settle with one run per cell.

**On generality.** Two predictions follow; neither was tested here.
- *Same configuration, other hardware.* The numbers will differ; the verdicts should not. Most of them lie well clear of their thresholds; for τ on the LM arm and on SuperNI, the reconstruction R² is 0.94–0.99, against 0.90. Two lie closest. D3 in the technical rounds had R² 0.91–0.96 (§5.1, first table) and was re-tested in T-B at 0.99. Among the scheduling verdicts, T-A has a widest interval bound of −0.0147, against a margin of ±0.02.
- *Larger models with Adam-type optimizers.* τ should remain reconstructible from the optimizer's own state, since each step is set by the moments the optimizer keeps (§2). Whether one cheap scalar still suffices is open: under full fine-tuning, τ runs over all weights and the second moments are more heterogeneous.

The equivalence of the clocks as replay schedulers has no such mechanistic basis and should not be extrapolated beyond the regimes tested.

## 7. Limitations

- **Local preregistration.** Hashes were recorded before each run, but not deposited publicly; an outside reader must trust the records. Every preregistration, hash list and log is in the archive with its timestamps. Some files named in the hash lists were changed afterwards for a later test; the earlier versions are archived (11 of 13; four of them reconstructed and identified by their recorded hash), and `Stadiul0/verify_hash_lists.py` checks every entry.
- **Two code versions not preserved.** The synthetic-world code of the technical rounds of 4 Nov (before the corrections of 6 Nov) and the LM training script of the runs lmtech1 and lmtech2 were not kept. Their stored results, resolved configurations and (for the LM runs) the script's hash are archived, and the analyses reproduce from them; the runs themselves cannot be repeated with exactly that code.
- **Small samples.** T-A 5 seeds per clock; SuperNI 3 seeds; the authors' code one pair (R1, R2) plus two crossed runs from shared task-0 adapters (stage 1), one run per cell; seed 42 throughout, as fixed in their code; one task order (order 1 of the paper).
- **Scope.** Models of 0.93 M and 0.6 B parameters; LoRA on q_proj and v_proj only; synthetic facts, five SuperNI tasks, four classification tasks.
- **Several analyses are post hoc** and labelled as such (the R² 0.749 on replay tasks, the drift ratios of (d) and of stage 1, residual analyses).
- **Many comparisons** without correction; verdicts follow the fixed rules, and secondary numbers are descriptive.
- **Equivalence margins are descriptive** (±2 points; ±5% on loss); only T-A and S2 use paired confidence intervals, and those with few seeds.
- **Evaluation noise** in the authors' code: decoding is stochastic (`do_sample=True`, temperature 0.02, no seed).
- **Hardware.** One laptop GPU with 4 GB, against the 8 NVIDIA H20 data-centre GPUs of the authors (Appendix H); the allocator change for tasks 1–3 of the authors' code; GPU non-determinism in fp16. Runs of their fp16 code are not expected to be bit-identical across such different hardware, so the reproduction (OP within 0.53 points) and the run-to-run differences are read against margins, not as exact replications.
- **Our code on one machine only.** The synthetic world and the LM arm ran only on the author's laptop, where they are bit-identical on repetition. On other hardware, agreement is expected at the level of the verdicts, not of the numbers (§6), but this was not tested.
- **Direction decisions** were taken through colloquia of AI systems under rules fixed before reading their answers, with every claim verified; the author is not a machine-learning specialist (§9).

## 8. Notes on FOREVER (for its authors and users)

Neutral observations made while reproducing the method; none changes the reproduced score.
1. Every phase (calibration, current-task training, replay) builds a new `transformers.Trainer`, so AdamW, the learning-rate schedule with warmup and the fp16 GradScaler restart at each phase, and the data loader starts again from the beginning; τ therefore contains the schedule directly. In the drift logs the first step of every phase (step 1, step 25 and the step after each trigger) has Δθ = 0, as do a few other steps (probably steps skipped by the GradScaler; not verified).
2. The code uses LoRA α = 16 and batch 32 (4 × 8); the paper states α = 32 and batch 8 (Appendix H).
3. The launch script calls `finetune_cl_ours_qwen.py`, which is not in the repository; `finetune_cl_our_qwen.py` is.
4. The generators hard-code the SuperNI test folder, so the "long sequence" benchmark cannot be evaluated without a change.
5. Memory sampling takes at least one example per distinct answer; on generation tasks with mostly distinct answers this approaches the whole task rather than 2% (observation from the code; not tested at scale).
6. Overall performance is computed by exact match and BWT with tolerant label extraction; decoding is stochastic without a seed.
7. In our re-implementation (bf16 without GradScaler, one data stream across a task's phases) the free clock Ση‖m̂‖ triggered replay at practically the same steps as τ (median difference ≤ 1 step); in the original code it triggered at the same step or later, in all three pairs of runs (up to 36 of 313 steps; in two pairs from shared starting points, 16 of 17 comparable triggers later and none earlier), and on the same trajectory the ratio between the two clocks drifts within a task. Which difference between the two implementations causes this was not established.
8. The paper's ablation of the time signal is against step counts only; the learning-rate schedule and Ση‖m̂‖ are free competitors that the reproduction suggests including.
9. At the scale of the paper, the decisive check of the clock costs almost nothing. Log Ση‖m̂‖ next to τ: it is the learning rate times the norm of Adam's bias-corrected first moment, which the optimizer already holds. Then compute the R² of the rate of τ from it in 8-step windows (`Stadiul0/forever_repro/r2_reconstruction.py` does this for one run). The same quantity can also enter the ablation as a replay clock: `Stadiul0/forever_repro/make_clock_variant.py` builds that variant from their script and also logs τ. The fp16 code is not deterministic, so comparing clocks needs several runs per configuration.

## 9. How the work was done

The research question and the framework it tests are the author's (Ionici 2026c). The author also set how the study was governed: decision rules fixed in advance, colloquia with claim-by-claim verification, and consent for each action. The author provided and maintained the hardware, and paid for the external evaluations that were not free. The author approved the tests proposed by the colloquia and each decision rule, which was written and hashed before any answer was read, and kept the right to stop or postpone at every step. Runs were approved one campaign at a time, except for the technical rounds of 6–8 November, which ran under a standing authorisation limited to that weekend and to a hardware watchdog. Direction calls were settled by the rules applied to the verified answers, not by the author's preference.

An AI assistant, Claude Opus 5.5 (Anthropic; model identifier claude-opus-5-5), used through Claude Code in the Claude desktop application in October and November 2026, worked under the author's direction. It wrote and ran the code that produced all the data, ran the analyses, monitored the hardware, and checked every number and reference against the logs and the sources. It also built the archive and its reproduction checks, and drafted this text. The author reviewed the results, the decision documents and the text; the code was not reviewed line by line by the author, and its correctness rests on the automated checks, the preregistered analyses and the reproduction from the archive (§10). The author is responsible for all of it.

Direction calls were put to colloquia of AI systems (6 November: five participants and one non-voting witness; 8 November: three participants and one witness, named in `Colocviu/README.md`). Each system received the same dossier, sent by the assistant through the author's own accounts after the author approved each sending. Every factual claim and reference in the answers was checked, and recommendations resting on a false claim were struck out. The colloquia contributed substantively. The four decisive tests were proposed in their answers: T-A by all five participants of 6 November, T-B by four, and T-C and T-D by three each. Three errors or omissions of the dossier were found through them (`Colocviu/Verificare_raspunsuri_2026-11-06.md`). Dossiers, rules, answers and verification documents are in the archive (`Colocviu/`). The earlier AI evaluations of the protocol drafts (v0.1–v0.4), the prompts sent and their verification are kept in `Recenzii/` as an informative annex. They document the path of the study (its dilemmas, obstacles and how they were resolved) but support none of its conclusions. No AI system is listed as an author, because none can take responsibility for the work.

## 10. Data and code availability

Code, preregistrations, hash lists, logs and results: the archive published with this report (DOI to be assigned) (code under MIT, data and documents under CC BY 4.0). Large run arrays and the LoRA adapters: the archive (DOI to be assigned), data part. Not redistributed: FOREVER's code and data (no licence; `Stadiul0/forever_repro/prepare_forever_copy.py` rebuilds the exact working copy from the authors' commit and checks it against the hashes recorded before the runs), model weights (Hugging Face; hashes in `Stadiul0/modele_provenienta.md`), hardware reports. The archive opens with `INDEX.md`, which sorts every file into essential and non-essential for repeating the test and maps each test to its rules, launcher, code, stored results and analysis. The 19 analyses behind the verdicts, tables and quoted numbers of this report run again from the archive with `Stadiul0/reproduce_analyses.py` (CPU, about 3 minutes). On 9 Nov 2026, from a fresh copy of the archive with the data part unpacked, all 19 reproduced the stored outputs: every log line for line, and the JSON files identical or with relative differences below 1e-15.

## References

- Aljundi, R., Caccia, L., Belilovsky, E., et al. (2019). Online Continual Learning with Maximally Interfered Retrieval. NeurIPS 2019. arXiv:1908.04742.
- Amiri, H., Miller, T., & Savova, G. (2017). Repeat before Forgetting: Spaced Repetition for Efficient and Effective Training of Neural Networks. EMNLP 2017, 2401–2410. https://doi.org/10.18653/v1/D17-1255
- Atamna, A., Maus, T., Kievelitz, F., & Glasmachers, T. (2025). Cumulative Learning Rate Adaptation: Revisiting Path-Based Schedules for SGD and Adam. arXiv:2508.05408.
- Benzing, F. (2022). Unifying Importance Based Regularisation Methods for Continual Learning. AISTATS 2022, PMLR 151, 2372–2396. arXiv:2006.06357.
- Feng, Y., Wang, H., Li, J., Chu, X., Kang, Z., Liu, Y., Wang, Y., Yu, P. S., & Wu, X.-M. (2026). FOREVER: Forgetting Curve-Inspired Memory Replay for Language Model Continual Learning. ACL 2026. arXiv:2601.03938 (v2).
- He, J., Bai, L., & Yang, X. (2026). Exploring the Impact of Parameter Update Magnitude on Forgetting and Generalization of Continual Learning. arXiv:2602.20796.
- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., & Chen, W. (2021). LoRA: Low-Rank Adaptation of Large Language Models. arXiv:2106.09685.
- Ionici, I. D. (2026a). *Does Explicit Episode–Trace Binding Help? An Exploratory Study with Information-Matched, Competence-Audited Controls* (Version 1.3). Zenodo. https://doi.org/10.5281/zenodo.23847602
- Ionici, I. D. (2026b). *Episode–Trace Binding Pilot: Code, Frozen Configurations, and Per-Run Results* (Version 1.3) [Software]. Zenodo. https://doi.org/10.5281/zenodo.23847723
- Ionici, I. D. (2026c). *A Time of Their Own: Agent-Held Temporal Evidence for Persistent AI Agents* (Version 1.3). Zenodo. https://doi.org/10.5281/zenodo.23847648
- Kosson, A., Messmer, B., & Jaggi, M. (2024). Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks. ICML 2024. arXiv:2305.17212.
- Liu, J., Su, J., Yao, X., et al. (2025). Muon is Scalable for LLM Training. arXiv:2502.16982.
- Pruthi, G., Liu, F., Sundararajan, M., & Kale, S. (2020). Estimating Training Data Influence by Tracing Gradient Descent. NeurIPS 2020. arXiv:2002.08484.
- Wang, X., & Aitchison, L. (2025). How to set AdamW's weight decay as you scale model and dataset size. ICML 2025. arXiv:2405.13698.
- Wang, Y., Mishra, S., Alipoormolabashi, P., et al. (2022). Super-NaturalInstructions: Generalization via Declarative Instructions on 1600+ NLP Tasks. EMNLP 2022. arXiv:2204.07705.
- Yang, A., Li, A., Yang, B., et al. (2025). Qwen3 Technical Report. arXiv:2505.09388.
- Zenke, F., Poole, B., & Ganguli, S. (2017). Continual Learning Through Synaptic Intelligence. ICML 2017. arXiv:1703.04200.
- Zhang, X., Zhao, J., & LeCun, Y. (2015). Character-level Convolutional Networks for Text Classification. NIPS 2015. arXiv:1509.01626.
