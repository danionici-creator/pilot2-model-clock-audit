> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `preinregistrare_SuperNI_2026-11-07.md`, whose hash was
> recorded before the runs in `runs/preinregistrare_SuperNI_sha256.txt`. File names, paths, code identifiers and quoted
> words are left as in the original.

# Preregistration of the SuperNI check (S1, S2), 7 Nov 2026, BEFORE running

**Why:** the missing control named by Gemini (G2 on natural, non-stationary data) and the test proposed by Deep Review (5 heterogeneous SuperNI tasks). The conclusion of the tests of the night of 6–7 Nov (`02_Pilot2/Rezultate_teste_decisive_2026-11-07.md`) is limited to synthetic facts; this checks whether it extends to natural tasks. Starting it was requested by the user ("SuperNI check first"), and the data download approved ("Yes, download").

**The data:** `D:\Time\_date\FOREVER_bbeb549\data_superni` (from the FOREVER repository, commit `bbeb549a21e5…`, checked with the git hashes; `SHA256SUMS.txt`). The first 5 tasks of FOREVER's order 7: task1572, task363, task1290, task181, task002 (generation and classification; 160–1,000 examples; median between 106 and 512 tokens).

**Configuration:** `lm/lm_superni_run.py` (hash in `runs/preinregistrare_SuperNI_sha256.txt`). The FOREVER schedule as in `lm_forever_run.py`, with the settings of their script for Qwen (`scripts/run_train_cl_ours_qwen.sh`): micro-batch 4 × 8 = 32, at most 512 tokens, the loss on the answer only, 2 epochs over the memory, a model day of 24 steps, memory of 2% per previous task. Declared deviations (in the script's header): bf16; 3 / 10 epochs on the first task (theirs: 10 / 60), for the laptop's time; no group_by_length; the memory rule corrected for the generation tasks (it would take ~the whole task); gradient checkpointing (does not change the mathematics). **New seeds: 7401, 7402, 7403.**

## S1 (primary): reconstruction of τ on heterogeneous natural data
The runs with `--clock tau`. Windows of 8 counted steps within the phases (as `lm_forever_g2.py`); target: the rate of τ (mean Δ_t). Predictors: Ση, Ση‖m̂‖, Ση + Ση‖m̂‖ (OLS), GBDT on the telemetry (η, ‖g‖, ‖g̃‖, ‖m̂‖, √Tr v̂, loss, step within the phase, phase type, task, answer tokens in the step).
Two out-of-sample schemes: (a) **one seed left out**; (b) **one task left out** (all seeds; the heterogeneity test).
- **The reconstruction extends to SuperNI** if OLS on Ση + Ση‖m̂‖ has mean R² ≥ 0.90 in **both** schemes.
- **It does not extend** if the mean R² < 0.90 in either scheme: the conclusion "the FOREVER clock = the optimizer's telemetry" remains limited to the synthetic facts, with the failure regime reported (per task).
- Also reported: Ση‖m̂‖ alone, GBDT and the minimum over folds.

## S2 (secondary): the scheduler on SuperNI
The runs with `--clock eta_m` on the same seeds, paired with τ. Outcome: **E1 = the mean loss on the answer on the test sets of the 5 tasks, after the last final replay** (lower is better); secondary: the loss on the old tasks just before each final replay (`evals_pre.npz`) and the separation of the triggers (median |Δ step|).
- **Practical equivalence** if the paired 95% t interval of the relative difference (E1(τ) − E1(eta_m)) / E1(τ) lies within (−5%; +5%).
- **τ superior** if the relative difference is ≤ −5% and the interval does not contain 0.
- **Otherwise: inconclusive.** With 3 seeds the power is low; a wide interval gives "inconclusive".

**Order of the runs:** first the 3 τ runs (S1), then the 3 eta_m runs (S2). The user may stop after S1.
**Estimated duration:** ~65–70 min per run: S1 ≈ 3.5 h, S2 another ≈ 3.5 h.
