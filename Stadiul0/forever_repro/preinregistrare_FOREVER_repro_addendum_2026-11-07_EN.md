> **English translation, made on 10 Nov 2026, after the study, for readers who do not read Romanian.** It is not hashed
> and not binding. The binding text is the Romanian original, `preinregistrare_FOREVER_repro_addendum_2026-11-07.md`,
> whose hash was recorded in `runs/forever_repro_sha256.txt` before any evaluation result. File names, paths, code
> identifiers and quoted words are left as in the original.

# Addendum to the preregistration of the FOREVER reproduction (7 Nov 2026, ~18:25, BEFORE any evaluation result)

**What happened.** R1 (τ), task 1 (amazon): the current-task training finished (313/313 steps), but the final replay from memory failed at 18:12 with `torch.AcceleratorError: CUDA error: out of memory` (the log: `_work\_copii_siguranta\forever_repro_t1_oom_2026-11-07\logs\tau_train_t1.log`). On Windows (WDDM), when the 4 GB of VRAM fill up, the driver places allocations in shared memory in RAM. The caching PyTorch allocator keeps them, so the memory of the process grew (measured at 16:20: 3.9 GB dedicated + 9.7 GB shared), the steps slowed from ~7 s to ~30–40 s, and at the end the limit was reached. The real peak of a long batch exceeds 4 GB: the `cudaMallocAsync` allocator, which does not use shared memory, fails immediately (checked). The original launcher would have continued with an adapter without the final replay; the failure watcher stopped it. The BWT generation started on that adapter was stopped by hand, before any evaluation.

**What was moved (nothing deleted):** `ckpt_tau/.../1-amazon`, `logs/tau_train_t1.log`, `logs/tau_bwt_t1.log` and the partial result `1-amazon_result.txt` are in `_work\_copii_siguranta\forever_repro_t1_oom_2026-11-07\`. The move is necessary: their code resumes the step counter from `drift_log.csv` if the file exists. Task 0 (the adapter `0-dbpedia` and the BWT generation on dbpedia) is left untouched.

**Adaptation 5 (new, execution only):** the training of tasks 1–3 (those with replays from memory) runs with the environment variable `PYTORCH_NO_CUDA_MEMORY_CACHING=1`, **for both variants**. Every tensor is freed immediately, so the blocks that reached shared memory no longer accumulate. Task 0 and all generations keep the default allocator, as in task 0 of R1. The code, the arguments and the computations do not change (the allocator decides only where memory lives, not what is computed); the cost is only time (measured: ~18.5 s per step against ~7.5 s per step without the VRAM filling up).

**Rejected alternatives:**
- `micro_batch_size` 2 instead of 4: in their code, the regularisation term of `ReplayTrainer` is added at every micro-batch without division by the number of accumulation steps, so its strength would double. That is a change of algorithm.
- `garbage_collection_threshold`: no effect without `set_per_process_memory_fraction`, which requires a code change (checked).
- `cudaMallocAsync`: fails immediately.

**The resume launcher:** `launch_repro_resume.sh` (the same commands; it starts with τ from task 1, then η‖m̂‖ from task 0; it stops at the first failed stage).

**The criteria of the preregistration remain unchanged.** The only result information known now: the functioning check of the generation on dbpedia after task 0 (98.5% exact matches on the first 2,654 examples), which is not the criterion.
