> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `td_criterii.md`, whose hash was recorded before computing
> in `runs/td_criterii_sha256.txt` (and in `runs/preinregistrare_sha256.txt`). File names, paths and code identifiers are
> left as in the original.

# Test T-D (colloquium of 6 Nov 2026): audit of the reconstruction on the existing logs. Criteria fixed BEFORE computing (6 Nov, ~22:55)

Proposed by Copilot (test 3), ChatGPT (test 1) and Deep Review (artefacts 1–4); `02_Pilot2/Colocviu/Verificare_raspunsuri_2026-11-06.md` §10. Blind to T1 (F_A, F_B, dAcc_A are not read). The part with new seeds and a frozen analysis comes from T-B; here only the existing logs.

1. **Without circular features** (error E1): on the R1 data (tech2/tech3, `g2_preview.py`), OLS and GBDT on B_strong **without C6_*** (the statistics of D1 itself and of the Adam step at the ends of the interval), against the complete B_strong.
2. **The mechanism left out** (Deep Review): on tech4, the ladder of cheap scalars (ΔN, ΔN + Ση‖m̂‖, ΔN + C10c) and GBDT; tests on F1, F2, F3, F4, F6; for F2, F3, F4 the training **also excludes F5** (the composite family).
3. **Bands of ΔN** (Copilot, ChatGPT, Deep Review): on tech4, one family left out, the R² and the relative error of ΔN + Ση‖m̂‖, separately for 64–127 / 128–255 / 256–639 / 640–1,279.
4. **Transfer between configurations on the LM arm** (Deep Review): the rate of τ over 8-step windows; OLS on Ση + Ση‖m̂‖ and GBDT trained on lmtech1, tested on lmtech2, lmsens_bf16, lmsens_a32; plus the minimum over seeds in lmtech1.

**The fixed reading:** the reconstruction of the clocks from the parameters is **robust** if R² ≥ 0.90 holds for D1 and D2 in (1) without C6, (2) with the scalar ΔN + Ση‖m̂‖ and the mechanism left out, (4) with the transferred linear model, for τ. Where it fails, only that ladder or regime is reopened (Copilot's rule), not the whole line. D1_rel and D3 are reported, but do not enter the reading (they already have the F6 exception).
