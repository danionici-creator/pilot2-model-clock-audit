> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `lmtech2_criterii.md`, whose hash was recorded before the
> runs in `runs/lmtech2_criterii_sha256.txt`. File names, paths and code identifiers are left as in the original.

# Technical round lmtech2 (criteria fixed BEFORE running, 6 Nov 2026, after the results of lmtech1)

**Why:** lmtech1 broke two validity criteria fixed in advance: the accuracy on the current task < 0.95 on the last tasks in 2 of 3 runs (7101: 0.920 on task 9; 7102: 0.941 on task 8) and the steps skipped by the GradScaler 4.1% (> 2%). The results of lmtech1 remain descriptive and are reported as such.

**The single change:** 256 facts per task instead of 512 (the same 10 exposures per fact; the FOREVER schedule unchanged: 10 epochs, 60 on the first task). Seeds 7201, 7202, 7203. The same script (`lm_forever_run.py`, SHA-256 unchanged), the same fixed analysis (`lm_forever_g2.py`); the post hoc analyses of lmtech1 (`lm_forever_posthoc.py`) are run here too, also as exploration.

**Validity criteria:**
- the accuracy on the current task at the end of each task ≥ 0.95 (only the diagonal);
- the steps skipped by the GradScaler: **reported, with no threshold**. Reason: they are a property of the FOREVER set-up (fp16, a new GradScaler at every phase, initial scale 65,536); the 2% threshold had been fixed on a check with 2 tasks. The ladder analysis includes the number of skipped steps anyway (lmtech1: the correction does not change the result, 0.655 against 0.669);
- no non-finite loss; `meta.json` with the hashes.

**Time estimate:** ~8–9 min per run (task 0: 480 steps × 0.32 s; tasks 1–9: 80 steps each plus replays), ~25–30 min in all.
