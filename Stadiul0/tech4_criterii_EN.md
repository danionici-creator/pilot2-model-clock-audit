> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `tech4_criterii.md`, whose hash was recorded before the
> runs in `runs/tech4_criterii_sha256.txt`. File names, paths, code identifiers and quoted words are left as in the
> original.

# Technical round tech4: F1–F6 on the code corrected after Deep Review (criteria fixed BEFORE running, 6 Nov 2026)

**What it is:** step 2 of `02_Pilot2\Recenzii\Pilot2_v0.4_verificare_recenzie_DeepReview.md` §4 ("a new technical round, blind to c_e"). Not preregistered, like tech1–tech3. **Blind to the c_e–T1 relation:** no incremental value of c_e and no relation between c_e and forgetting is computed.

**The code:** the Deep Review corrections applied on 6 Nov (`Stadiul0_note_lucru.md` §14): `max_ctx` 4; the embeddings taken out of weight decay (`wd_embeddings: false`, **provisional**, the author's decision (c) is open; the recommended variant); the q_hist overlap at the start of the segment; L̄_A,clip and L̄_B,clip in the evaluations; C10c and L_R(t₀); C0 as pause ticks; the D2 block at 16 steps. Checks: 27/27 (`runs\checks_latest.log`). Copies of the earlier code: `_work\_copii_siguranta\stadiul0_inainte_corecturi_DR_2026-11-06\`.

**The runs:** F1–F6, seed 9005, rate 3e-4 (from the configuration), 4 processes (the throughput reference), ASUS Turbo mode, on mains power, with the hardware watchdog on (`hw_watchdog.py`).

**What is measured (descriptive, no gates):**
1. childhood after taking the embeddings out of weight decay: the reference accuracy ≥ 0.95 in all 6 (the existing gate);
2. the speed of forgetting in F5 and F6 (requested by the review): F_A and T1-acc over ΔN, at intervals < 1,280, < 2,048 and with no cap, and on F^clip;
3. **the actual throughput in Turbo:** runs per hour at 4 processes, the time per component (childhood, training, evaluations, chunks), the maximum memory per process (the D2 block at 16 adds ~70 MB);
4. the temperatures and the frequency throttling from the watchdog's log, over the whole duration.

**Validity:** each run ends with `meta.json` and the hashes; no stop by the watchdog.

**Time estimate:** 6 runs on 4 processes = a wave of 4 (~20–25 min; tech3 took 25 min before Turbo, and childhood is now ~2 times faster) and a wave of 2 (~15–20 min, less contention for memory). In all **~40–45 min**.
