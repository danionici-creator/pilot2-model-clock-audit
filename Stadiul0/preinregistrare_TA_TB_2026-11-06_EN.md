> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `preinregistrare_TA_TB_2026-11-06.md`, whose hash was
> recorded before the runs in `runs/preinregistrare_sha256.txt`. File names, paths, code identifiers and quoted words
> are left as in the original; explanatory additions are in [square brackets].

# Preregistration of the decisive tests T-A and T-B (Pilot 2 colloquium, 6 Nov 2026)

**Written and hashed BEFORE any run of these tests** (6 Nov 2026, ~23:05). The tests come from the colloquium (`02_Pilot2/Colocviu/Verificare_raspunsuri_2026-11-06.md` §10): T-A proposed by all 5 participants, T-B by 4 of 5. Starting them was approved by the user ("Yes, start", 6 Nov). Decisions of the colloquium applied: Stage 0 split (0a blind to T1, the only phase in which the design may change; 0b automatic after the lock), bf16 on the LM arm, C10c mandatory, the LM learning criterion read before the final replay, embeddings entirely without weight decay (as already in the code).

**Common rules.** Nothing in this sheet changes after the data are seen. Any deviation is recorded explicitly, with its reason, in `Predare_fir.md`. The analysis script of the H1 part (T-B, part 2) is written after this sheet, but **before the T1 columns are opened**, and is hashed in `Predare_fir.md` before it runs. The hardware watchdog stays on; a run stopped by it is redone identically (the runs are deterministic), with no other change.

---

## T-A. The FOREVER scheduler driven by different clocks (LM arm, GPU)

**The question:** does triggering replay by τ (model-centred time, FOREVER) reduce forgetting more than triggering by a cheap clock?

**Configuration:** `lm/lm_forever_run.py` (hash in `runs/preinregistrare_sha256.txt`), Qwen3-0.6B + LoRA r = 8, α = 16 (the value in the FOREVER code), **bf16**, 10 tasks × 512 facts, 60 epochs on task 0 and 10 on the others, batch 32, η 3·10⁻⁴, memory of 16 facts per task; `--diag_pre_final --diag_pre_final_all`. Four clocks (`--clock`), the same calibration on the first 24 steps and the same thresholds d × day: **tau** (FOREVER), **eta_m** = Ση‖m̂‖, **eta** = applied Ση (the schedule only), **steps** = counted steps. The replay weight β is still computed from τ in every arm (only *when* replay happens differs). The tau variant is bit-identical to the earlier script (check `runs/ta_smoke2`). **New seeds: 7301–7305** (5 pairs). 20 runs, seed by seed (all 4 clocks on one seed, then the next).

**Fixed outcomes:**
- **E1 (primary):** mean final accuracy over the 10 tasks, after the last final replay (last row of `evals.npz`).
- E2: BWT = mean over t < 9 of (acc_final[t] − acc at the end of task t[t]).
- E3: mean accuracy on the old tasks just before each final replay (`evals_pre.npz`), averaged over tasks 1–9.
- E4: the number of replays and the difference of the trigger steps from τ (median |Δ| for each d reached).

**Criteria** (margin δ = 0.02, i.e. 2 percentage points; paired comparisons by seed: τ against each other clock, on E1):
- **Separation** (ChatGPT's precondition): if the median |Δ trigger step| ≤ 2 for all thresholds reached, the two clocks are **equivalent as schedulers** in this framework. This is a result in itself (the redundancy of τ as a scheduler), whatever E1 shows.
- **τ superior** to X: the mean of the differences E1(τ) − E1(X) ≥ 0.02 and the paired 95% t interval does not contain 0.
- **Practical equivalence:** the paired 95% t interval of the difference lies within (−0.02; +0.02).
- **Otherwise: inconclusive** (not evidence of equality).

Reading for the FOREVER note: if τ is equivalent to eta_m (and to eta), its value as a scheduler is reproduced by a free clock in this framework. If τ is superior, it has value as a scheduler beyond telemetry in this framework. E2–E4 are reported. **Declared limits:** synthetic facts, a single small model, the deviations from FOREVER listed in the dossier, 5 seeds (low power; a wide interval gives "inconclusive").

**Estimated duration:** 20 × ~15 min ≈ **5 h** on the GPU.

---

## T-B. D3 under dosed noise, on new seeds, against same-cost competitors (synthetic world, CPU)

**The question:** does the functional change D3 contain, in the regime with noisy distractors (F6), information that neither the telemetry nor the same-cost competitors have, and does it predict forgetting beyond them?

**Configuration:** `p2/run.py`, `p2/triplets.py` (hashes in `runs/preinregistrare_sha256.txt`), `config_stage0.yaml` unchanged. The new same-cost competitors, from the same pass as D3: **C10p** = mean |Δ p(target)| and **C10h** = mean |Δ output entropy| on battery R, accumulated over the same 8-step blocks as D3 and C10c (training stays bit-identical: control `runs/tech4_g7_TB`). Conditions: **F6 with label noise 0 / 0.1 / 0.3 / 0.5** (`--set families.F6.label_noise=x`) and **F1** as a control without noise (the second family weak for the cheap scalar, correction E4). **New seeds: 9101–9108** (8 per condition), hence 40 runs, 4 processes pinned to the P-cores.

### Part 1: Stage 0a, G2 (blind to T1; F_A, F_B, dAcc_A are not read)
Target: the rate of D3 on triplets (ΔN ∈ [64; 1,280), the inclusion rule of the protocol). Models, with one seed left out **within each condition**: (i) ΔN + C10c; (ii) ΔN + C10c + C10p + C10h; (iii) **GBDT on B⁺** = the telemetry rates (without C6) + X_cov + the terms in ΔN + C10c + C10p + C10h (hyperparameters from `tech4_analysis.py`).
- **G2-F6 passes** (D3 is not reconstructed) if, at noise 0.3, the R² of (iii) is < 0.90 for **at least 6 of the 8** seeds tested.
- **Dose–response** (Mistral T2): u(z) = 1 − mean R² of (iii) at noise z; it passes if u increases strictly with z over the 4 levels (Spearman = 1) and u(0.3) ≥ 2 · u(0).
- Reported: the same models for D1_rel (exception E2) and for F1.
- **If G2-F6 does not pass:** D3 is reconstructed by the same-cost competitors in F6 too, H1 is not identifiable (the protocol's rule), **D3 is closed** as an experiential index in this framework, and part 2 is not run. [Wording of the original, fixed before the runs; the closure report describes this outcome as "not identifiable".]

### Part 2: Stage 0b, H1 (automatic, only if part 1 passes)
Target **T1 = F_A** (the increase of the loss on half A); secondary target T1_acc = dAcc_A. On each F6 run at 0.3, 5-fold cross-validation over **tasks** (all triplets of a task in the same fold). Base model: GBDT on B⁺; extended model: B⁺ + the rate of D3 + cumulative ΔD3. **ΔR²** = R²(extended) − R²(base), out of fold, per run.
- **H1-F6 supported** if the mean ΔR² over the 8 seeds is ≥ 0.02, **and** ΔR² > 0 in at least 6 of 8 seeds, **and** the lower bound of the 95% bootstrap interval over seeds (10,000 resamples) is > 0, **and** the sign is the same on T1_acc.
- **Otherwise: H1-F6 not supported, D3 is closed.**
- The replication at 0.1 or 0.5 (Copilot) is reported as secondary; it is not a condition.

**Estimated duration:** 40 runs in 5 batches of 8 (4 processes, 2 waves of ~17 min per batch) ≈ **2 h 50 min** on the CPU, in parallel with T-A.

---

**What is NOT tested here** (proposed by a single participant, only listed): the per-step residual of D1 (Mistral), the natural SuperNI data (Gemini, Deep Review), the net-distance control / D3_shuffled (Deep Review; DeepSeek as witness), F2 with noise (ChatGPT).
