# Pilot 2: An Audit of a Model-Centred Clock Against Optimizer Telemetry

Code, preregistrations, hash lists, logs and results of Pilot 2, described in

> Ionici, I. D. (2026). *Does a model-centred clock carry information beyond optimizer telemetry? Closure report of
> Pilot 2* (Version 1.0). Zenodo. https://doi.org/10.5281/zenodo.24188374

The archived, citable release is on Zenodo: https://doi.org/10.5281/zenodo.24188372. This repository holds the code and the small result files.
The large run arrays (`*.npz`, `*.npy`, `*.parquet`) and the final LoRA adapters are only in the Zenodo data part.

**Related records.**
- Closure report, version 1.0: https://doi.org/10.5281/zenodo.24188374
- This archive, version 1.0 (repository and data part): https://doi.org/10.5281/zenodo.24188372
- *A Time of Their Own*, the Perspective whose Level 2 Pilot 2 tested: version 1.3,
  https://doi.org/10.5281/zenodo.23847648; version 1.4, which reports the outcome, https://doi.org/10.5281/zenodo.24188352
- Code repository: https://github.com/danionici-creator/pilot2-model-clock-audit

**Status: closed.** Pilot 2 asked whether an agent's accumulated internal change carries information beyond the
statistics an optimizer logs anyway. This change is the "experiential index" c<sub>e</sub> of *A Time of Their Own*,
Level 2 (https://doi.org/10.5281/zenodo.23671714).

- In our implementations every candidate clock was reconstructed from cheap telemetry or from a competitor of the same
  cost (held-out R² ≥ 0.90; the exceptions arise only when a schedule family is left out of training). So the
  confirmatory hypothesis was never run.
- Used to schedule replay in FOREVER, the clock gave no measurable advantage over free clocks in our port. With the
  authors' code, over three comparisons among four runs, it gave none in aggregate either.
- With the authors' code the free clock triggers replay systematically later. A 5.3-point difference on one task in the
  first pair did not recur consistently from common starting points (preregistered 2 × 2 repetition), so it is not
  attributed to the clock.

The report gives the results, the exceptions and the limits.

## Start here

1. **[`INDEX.md`](INDEX.md)** sorts every file into two categories: *essential for repeating the test* and *not needed
   to repeat the test*. It gives the path through the archive and a test map, one row per test: rules → launcher →
   code → stored results → analysis → stored output. [`FILES.tsv`](FILES.tsv) lists every file with its category,
   group and part (repository or Zenodo data part).
2. **Check integrity:** `sha256sum -c SHA256SUMS.txt`, then `python -I Stadiul0/verify_hash_lists.py`, which
   classifies every entry of the hash lists written before the runs and verifies the bytes of those kept here.
3. **Re-run the analyses** (CPU, about 3 minutes): unpack the Zenodo data part into the repository root, then run
   `python -I Stadiul0/reproduce_analyses.py`.

The folders keep the layout of the study's working folder, so every path in the preregistrations, hash lists and logs
resolves as written. Working notes, preregistrations and colloquium documents are partly in Romanian; the report, this
README, the index and the archive scripts are in English. The eleven files of rules fixed before the runs (the
preregistrations and the criteria files) have English translations next to them (`*_EN.md`, made on 10 Nov 2026,
after the study); the translations are not hashed, and the hashed Romanian originals are the binding versions.

## Not included

- **FOREVER's code and data** (https://github.com/WoodScene/FOREVER; no licence). Rebuild the exact working copy:
  ```
  git clone https://github.com/WoodScene/FOREVER
  git -C FOREVER checkout bbeb549a21e59d9490f20a2b02099ee766a67f48
  cd Stadiul0/forever_repro
  python -I prepare_forever_copy.py ../../FOREVER
  ```
  It checks the authors' files against the hashes of that commit, applies the documented adaptations, builds the
  clock-swap variant, and checks every result against the hashes recorded before the runs.
- **Model weights** (Qwen3-0.6B; Pythia, used only in a speed benchmark described in the working notes): from Hugging
  Face. The files used and their hashes are in `Stadiul0/modele_provenienta.md`.
- **SuperNI task files**: from the FOREVER repository at the same commit (`data_superni/`).
- **Hardware reports** (they contain the laptop's serial numbers), temporary check folders, caches, and the intermediate
  checkpoints of the authors' code.
- **Two code versions that were not preserved.** The first is the synthetic-world code of the technical rounds of
  4 Nov (`tech1`–`tech3`), which ran before the corrections of 6 Nov. The second is the LM training script of the runs
  `lmtech1` and `lmtech2`. Their stored results are here, and the analyses reproduce from them. Each run's `meta.json`
  holds its resolved configuration, and for the LM runs also the SHA-256 of the script.

## Reproduction

1. **Integrity.** `sha256sum -c SHA256SUMS.txt` checks every file of this release.
   `python -I Stadiul0/verify_hash_lists.py` classifies the 87 entries of the nine hash lists in `Stadiul0/runs/`,
   written before the runs they govern, and verifies the bytes of the 66 kept in this release. 55 entries match the
   current file and 11 match an earlier version kept in `Stadiul0/runs/earlier_versions/` (the file was changed later
   for another test). 17 are files of the FOREVER authors, checked by `prepare_forever_copy.py`, and 1 is an external
   path. The remaining 3 name 2 versions that were not preserved, explained in
   `Stadiul0/runs/earlier_versions/README.md`.
2. **Analyses from the stored results** (CPU, about 3 minutes). This needs the Zenodo data part unpacked into the
   repository root, where its paths start with `Stadiul0/`:
   ```
   python -I Stadiul0/reproduce_analyses.py
   ```
   It re-runs the 23 analyses behind the verdicts, tables and quoted numbers of the report:
   - T-A, T-B, T-C and T-D;
   - SuperNI S1 and S2, with the S2 secondary quantities;
   - the τ reconstruction on the four LM configurations;
   - the technical rounds, the CPU checks and tech4;
   - the six analyses of the runs with the authors' code, one of them the post hoc drift ratio;
   - the three post hoc checks made after the final review round of the report: (a) the evaluation noise of the
     authors' evaluation scripts, (b) the T-A retention of the facts held in memory, (c) the skipped steps;
   - the leave-one-task-out R² of the authors' code, added after the independent audit of the archive (12 Nov 2026,
     `Recenzii/Audit_Codex_2026-11-10/`; `Stadiul0/forever_repro/r2_heldout_task_posthoc.py`).

   It compares their output with the stored logs and JSON files, and restores every file it rewrites, so that
   `SHA256SUMS.txt` still verifies. On 12 Nov 2026, from a fresh copy of this release, all 23 reproduced, under the
   strict comparison introduced after the independent audit (exit code 0). Every stored log matched line for line. The
   JSON files were identical, or differed only in the last digits of regression coefficients (relative differences
   below 1e-15).

   Two of these scripts were written on 9 Nov, after the study: `Stadiul0/sni_s2_secondary.py` and
   `Stadiul0/forever_repro/drift_ratio_posthoc.py`. On 7–9 Nov the same numbers had been computed by commands typed by
   hand. The first script reproduces byte for byte the log saved on 7 Nov. The second gives the values recorded by
   hand in `Rezultate_teste_decisive_2026-11-07.md`. One analysis (`Stadiul0/g2_preview.py`) stored no output when it
   ran; its numbers are the first table of the report. The runner only executes and prints it (on 12 Nov its output
   was checked by hand against that table); run alone on a Windows console, it needs `python -I -X utf8`. The scripts
   of the post hoc checks (a)–(c) were written on 9–10 Nov, after the final review round, and produced the stored
   outputs themselves: (a) re-evaluated the four final adapters of stage 1 on the GPU
   (`Stadiul0/forever_repro/launch_eval_noise_posthoc.sh`, about 10.5 hours) and (b) re-scored the stored final LoRA
   factors of T-A on the CPU (`Stadiul0/lm/ta_memory_facts_posthoc.py`); the archive check re-runs only their
   summaries, from the stored outputs. A short GPU diagnostic of (a),
   `Stadiul0/forever_repro/eval_tie_diagnostic_posthoc.py` (10 Nov), shows that the few answers where greedy decoding
   differs from the authors' decoding are exact ties of the two highest fp16 logits; it needs the GPU and is not
   re-run.
   The environment is in `Stadiul0/requirements_cpu_2026-11-09.txt` (Python 3.14.6, numpy 2.5.1, pandas 3.0.3,
   scikit-learn 1.9.0, scipy 1.18.0, torch 2.13.0+cpu).
3. **Runs.**
   - The synthetic world runs on CPU (`Stadiul0/launch.py`) and is bit-identical on repetition on the same machine.
   - The LM arm needs a CUDA GPU with 4 GB or more (`Stadiul0/lm/`; environment in
     `Stadiul0/lm/pip_freeze_venv_cuda_2026-11-09.txt`).
   - The authors' code needs their library versions (`Stadiul0/forever_repro/pip_freeze_venv_forever.txt`); rebuild it
     first, as described under "Not included" above.
   - The test map in `INDEX.md` gives the launcher, the code and the output of each test.
   - **Time on the author's laptop** (RTX 3050 Laptop GPU, 4 GB; wall-clock times from the launch logs in
     `Stadiul0/runs/`):

     | Test | Hardware | Duration |
     |---|---|---|
     | T-A (20 LM runs) and T-B (40 synthetic-world runs), in parallel | GPU + CPU | 6 h 40 min (T-B alone 3 h 47 min) |
     | SuperNI S1/S2 (6 runs) | GPU | 4 h 20 min |
     | R1, the authors' code, one full run (4 tasks, generation, evaluation) | GPU | 13 h 54 min, including a 12-min restart after the 4 GB card ran out of memory |
     | R2, the same with the free clock | GPU | 11 h 47 min |
     | Stage 1, two arms (tasks 1–3 from a copied task-0 adapter) | GPU | 14 h 28 min (about 7 h 15 min per arm) |
     | Post hoc (a), 12 re-evaluations | GPU | 10 h 30 min (48–62 min each) |
     | The 23 analyses, from the stored results | CPU | about 3.5 min |

     In all, the GPU was busy 63.5 hours in three sessions (6–8, 8–9 and 9–10 Nov 2026), under the hardware watchdog,
     which never stopped a run. Tasks 1–3 of the authors' code needed the PyTorch allocator without caching on the 4 GB
     card (`PYTORCH_NO_CUDA_MEMORY_CACHING=1`).

**Absolute paths.** Scripts are archived exactly as they ran, so that their hashes match the records. 23 of them contain
absolute paths of the author's laptop:

- `D:/Time/_modele/…` for the model;
- `D:/Time/_date/…` for the data and the model cache;
- `/d/Time/_venv_*/…` for the Python environments;
- `D:\Time\02_Pilot2\Stadiul0\runs` for outputs.

These 23 are the 11 launchers and the evaluation wrapper of the authors' code (`.sh`), the two LM training scripts,
the hardware watchdog, the launcher and the generator of post hoc check (a) (`launch_eval_noise_posthoc.sh`,
`eval_noise_posthoc.py`), the generator of post hoc check (b) (`lm/ta_memory_facts_posthoc.py`), the tie diagnostic of (a)
(`eval_tie_diagnostic_posthoc.py`), and four analyses (`g2_preview.py`, `g2_cpu_checks.py`, `td_audit.py`, `tech4_analysis.py`).
`reproduce_analyses.py` runs the four analyses from a temporary copy with the path replaced; adjust the other scripts
before re-running them.

Two other scripts mention such a path without depending on it:

- `prepare_forever_copy.py` writes the authors' cache path as it was in the working copy (`D:/Time/_date/hf_cache`). It
  is used only when the environment variable `FOREVER_CACHE` is not set.
- `reproduce_analyses.py` contains the pattern that it replaces.

The earlier versions in `Stadiul0/runs/earlier_versions/` keep their paths too.

One change in this public copy: in two stored logs, `Stadiul0/runs/lmsens_a32_g2.log` and
`Stadiul0/runs/lmtech1_g2.log`, the Python warnings named the local Python installation, with the author's user name;
that prefix is shortened to `<Python 3.14>`. Nothing else in them changes. Neither log is in a hash list, and
`reproduce_analyses.py` ignores warning lines when it compares.

## How to challenge these results

The closure report (§6) states what would overturn its conclusions. Each item can be tested with this archive:

1. **Identifiability.** Find a setting where a candidate clock's rate is *not* reconstructed out of sample: R² < 0.90
   for both the linear and the flexible model (gate G2), without extrapolation to a schedule family left out of
   training.
2. **Scheduling.** Find a preregistered comparison where τ beats the free clock Ση‖m̂‖ by at least 2 points, with a
   paired 95% interval above zero.
3. **The authors' code.** Find a difference on one task that keeps its sign and size over many runs per cell, other
   seeds and task orders.

Running one configuration of the test map in `INDEX.md` on other hardware is also useful. The prediction is that the
numbers change and the verdicts do not; this was not tested. Please compare and report verdicts, not only numbers.

## Licence and citation

Code: MIT ([`LICENSE`](LICENSE)). Data, logs and documents: CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)).
How to cite: [`CITATION.cff`](CITATION.cff). Please cite the closure report, and this archive when you use its code or
data.
