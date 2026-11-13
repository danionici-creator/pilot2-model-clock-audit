> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `tc_criterii.md`, whose hash was recorded before computing
> in `runs/tc_criterii_sha256.txt` (and in `runs/preinregistrare_sha256.txt`). File names, paths and code identifiers are
> left as in the original; explanatory additions are in [square brackets].

# Test T-C (colloquium of 6 Nov 2026): the same-cost competitors of D3 on the LM arm. Criteria fixed BEFORE computing (6 Nov, ~22:45)

Proposed by Mistral (T3), ChatGPT (test 3) and Deep Review (test 1a); see `02_Pilot2/Colocviu/Verificare_raspunsuri_2026-11-06.md` §10. Descriptive and blind to T1: only `probes.npz` and `steps.npz` are read; `evals.npz` is not opened.

**Data:** the existing runs `lmtech1`, `lmtech2`, `lmsens_bf16`, `lmsens_a32` (3 seeds each). **The intervals of D3**, exactly as in `lm_forever_g2.py`: pairs of consecutive probes of the same task, with no replay step in the interval; y = the RMS change of the log-probabilities (128 probes × 31 words) / the counted steps.

**The competitors** (from the same passes, as rates per counted step, over the same interval; a_i = the random, untrained answer word of probe i, regenerated from the world's seed):
- C10c_LM = mean_i |Δ(−log p_i(a_i))| (the direct analogue of C10c);
- P_LM = mean_i |Δ p_i(a_i)| (bounded);
- H_LM = mean_i |ΔH(p_i)| (the change of the entropy over the 31 words);
- reported, but **not used for the verdict** (a near-duplicate of D3, the same difference in another norm): L1_LM = mean_{i,w} |Δ log p_i(w)|.

**Models** (out-of-run R², one seed left out, in each configuration): (a) OLS on C10c_LM; (b) OLS on C10c_LM + P_LM + H_LM; (c) OLS on Ση‖m̂‖ + C10c_LM + P_LM + H_LM; (d) GBDT on the complete telemetry of `lm_forever_g2.py` + the three competitors.

**The verdict (fixed):** if the mean R² of model (b) is ≥ 0.90 in all 4 configurations, **D3 on the LM arm is reconstructed by the same-cost competitors**, and its alleged informational remainder is closed on this arm [wording of the original, fixed before computing; the closure report describes this outcome as "reconstructed", hence not identifiable]. If it is < 0.90 in all 4: **D3 is distinct** from the same-cost competitors on this arm. Otherwise: **mixed**. Also reported: (a), (c), (d) and the minimum over seeds.
