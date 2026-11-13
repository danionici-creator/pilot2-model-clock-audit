> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `lant2_criterii.md`, whose hash was recorded before the
> runs in `runs/lant2_criterii_sha256.txt`. File names, paths and code identifiers are left as in the original.

# Chain 2 (6 Nov 2026, evening): criteria fixed BEFORE running

All are technical, descriptive, non-preregistered measurements; none links c_e to forgetting.

1. **Pinning to cores (Deep Review B7)**, `pin_test.py`: 4 childhoods in parallel (3,072 steps, as in a run), in three conditions: free, pinned to the 4 P-cores (logical processors 0, 2, 4, 6), pinned to 4 E-cores (8–11). The time is reported; the accuracy must be identical in all conditions (determinism). **~5 min.**
2. **G7 on a complete run with the corrected code:** tech4 F6_s9005 redone alone (`runs/tech4_g7`), its arrays compared with tech4 through the hashes in `meta.json`. **~10–13 min.**
3. **LM arm, sensitivity to precision:** lmtech1 with `--precision bf16` (no GradScaler, hence no skipped steps; a deviation from FOREVER), seeds 7101–7103, 512 facts. **~45 min.**
4. **LM arm, sensitivity to α:** lmtech1 with `--alpha 32` (the value in the FOREVER paper; their code has 16). **~45 min.**

For 3 and 4: the fixed analysis `lm/lm_forever_g2.py`, compared with lmtech1 (the same seeds); `--diag_pre_final` on; **the learning criterion is read before the final replay** (≥ 0.95; the diagnostic of 6 Nov showed that the drop afterwards comes from the final replay), and the value after the replay is reported. Skipped steps are reported.

**Total estimated duration: ~1 h 50 min** (start ~19:00, end ~20:50). The hardware watchdog stays on; each stage checks `runs/_HW_STOP`.
