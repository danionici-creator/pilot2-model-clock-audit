# Index of the Pilot 2 archive

<!-- Written on 9 Nov 2026. The counts and the group tables are generated from the classification rules that also write
FILES.tsv (author's build script); the rest is written by hand. -->

This archive holds <!-- COUNTS -->1528 files: 1113 essential, 415 non-essential<!-- /COUNTS -->, in two categories:

- **Essential for repeating the test.** Everything needed to repeat Pilot 2, either by re-running the analyses on the
  stored results or by re-running the experiments. It also includes what you need to check that the repeated test is
  the one fixed before the runs: the rules, code, launchers, stored results and hash lists.
- **Not needed to repeat the test.** The record of how the study got there: the plan, the colloquia, the AI
  evaluations of the protocol and of the closure documents, the independent audit, the literature note, earlier
  drafts, working notes, technical rounds, controls and hardware logs. It helps explain the decisions, but no result
  depends on it.

`FILES.tsv` lists every file with its category, its group and its part: the repository, or the Zenodo data part for the
large arrays and the LoRA adapters. `SHA256SUMS.txt` gives the SHA-256 of every repository file.

The folders keep the layout of the study's working folder; they are not regrouped by category. The preregistrations,
hash lists, logs and scripts name files by these paths, so moving a file would break the checks that show what was fixed
when. The categories are therefore given here and in `FILES.tsv`, not by folders.

## The path through the archive

1. **Read** the closure report (https://doi.org/10.5281/zenodo.24188374). It gives the question, the results and the limits, and names the files
   behind each number. Then read this index.
2. **Check integrity** (a few seconds):
   ```
   sha256sum -c SHA256SUMS.txt
   python -I Stadiul0/verify_hash_lists.py
   ```
   The first command checks every file of this release. The second classifies every entry of the hash lists written
   before the runs and verifies the bytes of those kept in this release. Each entry is either the current file, an
   earlier version kept in `Stadiul0/runs/earlier_versions/`, a file of the FOREVER authors (not redistributed), an
   external file, or a version that was not preserved (explained in `Stadiul0/runs/earlier_versions/README.md`).
3. **Re-run the analyses** (CPU, about 3 minutes; first unpack the Zenodo data part into the repository root):
   ```
   python -I Stadiul0/reproduce_analyses.py
   ```
   This runs the 23 analyses behind the verdicts, tables and quoted numbers of the report and compares their output with
   the stored logs and JSON files. The environment is listed in `Stadiul0/requirements_cpu_2026-11-09.txt`.
4. **Repeat a test.** Take its row in the test map below and read the rules. Then run the launcher, after adjusting the
   absolute paths of the author's laptop (see `README.md`), run the analysis, and compare with the stored output. On the
   author's laptop, the synthetic world (CPU) and the LM arm (GPU) were bit-identical on repetition. The authors' fp16
   code is not deterministic, even there. On other hardware, identical bits are not to be expected: compare the
   verdicts, within the margins fixed in the rules.

## Test map

Paths are relative to `Stadiul0/` unless they start with a top-level folder. "§" refers to the closure report.

| Test (report) | Rules fixed before | Launcher | Code | Stored results | Analysis → stored output |
|---|---|---|---|---|---|
| Technical rounds, G2 preview (§5.1, first table) | `Pilot2_Protocol_EN_draft.md` (gate G2) | `launch.py` (runs and overrides in each folder's `launch_summary.json`) | `p2/` as of 4 Nov: **not preserved**; the resolved configuration of each run is in its `meta.json` | `runs/tech2_lr3e-4/`, `runs/tech3_lr3e-4/` | `g2_preview.py` (prints; numbers in the report), `g2_cpu_checks.py` → `runs/g2_cpu_checks_2026-11-06.log` |
| tech4, family left out (§5.1, T-B) | `tech4_criterii.md` | `launch_tech4.sh` (first attempt: `launch_weekend_1.sh`) | `p2/`, `launch.py`: the versions of that day are in `runs/earlier_versions/` | `runs/tech4/` | `tech4_analysis.py` → `runs/tech4_analysis.log` |
| T-D, audit of the reconstruction (§5.1) | `td_criterii.md` | no new runs | | tech2, tech3, tech4 and the four LM configurations | `td_audit.py` → `runs/td_audit.log` |
| T-B, D3 under dosed label noise (§5.1) | `preinregistrare_TA_TB_2026-11-06.md` | `launch_noapte_TA_TB.sh` | `p2/`, `config_stage0.yaml` | `runs/tb_F1/`, `runs/tb_F6_n00/`, `runs/tb_F6_n01/`, `runs/tb_F6_n03/`, `runs/tb_F6_n05/` | `tb_part1_g2.py` → `runs/tb_part1_g2.log`, `runs/tb_part1_verdict.json` (`tb_part2_h1.py`: H1, not run because G2 failed) |
| τ on the LM arm (§5.1) | `lm/lmtech1_criterii.md`, `lm/lmtech2_criterii.md`, `lant2_criterii.md` | `lm/launch_lmtech1.sh`; `launch_weekend_1.sh` → `lm/launch_lmtech2.sh`; `launch_lant2.sh` | `lm/lm_forever_run.py`: the version of lmtech1/lmtech2 is **not preserved** (its SHA-256 is in their `meta.json`); the version of lant2 is in `runs/earlier_versions/` | `runs/lmtech1/`, `runs/lmtech2/`, `runs/lmsens_bf16/`, `runs/lmsens_a32/` | `lm/lm_forever_g2.py` → `runs/lmtech1_g2.log`, `runs/lmtech2_g2.log`, `runs/lmsens_bf16_g2.log`, `runs/lmsens_a32_g2.log` |
| T-C, D3 on the LM arm (§5.1) | `lm/tc_criterii.md` | no new runs | | the four LM configurations | `lm/lm_d3_competitors.py` → `runs/tc_lm_d3_competitors.log` |
| T-A, replay clocks in the port (§5.2) | `preinregistrare_TA_TB_2026-11-06.md` | `launch_noapte_TA_TB.sh` | `lm/lm_forever_run.py` | `runs/ta/` | `ta_analysis.py` → `runs/ta_analysis.log`, `runs/ta_verdict.json` |
| SuperNI S1 and S2 (§5.1, §5.2) | `preinregistrare_SuperNI_2026-11-07.md` | `launch_SuperNI.sh` | `lm/lm_superni_run.py`; task files from the FOREVER repository | `runs/sni/` | `sni_analysis.py` → `runs/sni_S1_analysis.log`, `runs/sni_analysis_final.log`, `runs/sni_verdict.json`; `sni_s2_secondary.py` → `runs/sni_S2_secundar.log` |
| FOREVER R1 (τ) and R2 (Ση‖m̂‖) with the authors' code (§5.1, §5.2) | `forever_repro/preinregistrare_FOREVER_repro_2026-11-07.md` and its addendum | `forever_repro/launch_repro.sh`, `forever_repro/launch_repro_resume.sh`, `forever_repro/eval_repro.sh` | the authors' code, rebuilt by `forever_repro/prepare_forever_copy.py` (with `forever_repro/make_clock_variant.py`) | `forever_repro/ckpt_tau/`, `forever_repro/ckpt_eta_m/`, `forever_repro/logs/`, `forever_repro/output/` | the authors' evaluation → `runs/forever_repro_eval_tau.log`, `runs/forever_repro_eval_eta_m.log`; `forever_repro/r2_reconstruction.py` → `runs/forever_repro_r2_reconstruction.log` |
| Analysis (d), same trajectory (§5.1) | `forever_repro/preinregistrare_FOREVER_repetari_2026-11-08.md` (v3) | no new runs | | `forever_repro/ckpt_eta_m/` (drift logs) | `forever_repro/d_same_trajectory.py` → `runs/forever_d_same_trajectory.json` |
| Stage 1, 2 × 2 repeated runs (§5.2) | `forever_repro/preinregistrare_FOREVER_repetari_2026-11-08.md` (v3) | `forever_repro/launch_repetari.sh`, `forever_repro/eval_repro.sh` | as for R1 and R2 | `forever_repro/ckpt_eta_m_A1/`, `forever_repro/ckpt_tau_B1/`, `forever_repro/logs/`, `forever_repro/output/` | `forever_repro/rep_verdict.py` → `runs/forever_repetari_verdict.json`; `forever_repro/r2_reconstruction_arm.py` → `runs/forever_repetari_r2.log` |
| Drift ratio, post hoc (§5.1) | none (post hoc) | no new runs | | `forever_repro/ckpt_eta_m/`, `forever_repro/ckpt_eta_m_A1/` | `forever_repro/drift_ratio_posthoc.py` → `runs/forever_drift_ratio_posthoc.log` |
| Leave-one-task-out R² of the authors' code, post hoc (§5.1) | none (post hoc, after the independent audit of 12 Nov; `Recenzii/Audit_Codex_2026-11-10/`) | no new runs | | `forever_repro/ckpt_eta_m/`, `forever_repro/ckpt_eta_m_A1/` | `forever_repro/r2_heldout_task_posthoc.py` → `runs/forever_r2_heldout_task_posthoc.log` |
| Post hoc checks after the final review round (§5.2, §7, §8) | none (post hoc; `Recenzii/Runda_finala_2026-11-09/`) | (a) `forever_repro/launch_eval_noise_posthoc.sh`; (b) no new runs; (c) no new runs | (a) `forever_repro/eval_noise_posthoc.py` with the authors' scripts; (b) `lm/ta_memory_facts_posthoc.py` | (a) `forever_repro/output/_eval_noise_posthoc/`, `runs/forever_eval_noise_posthoc_*.log`; (b) `runs/ta_memory_facts_posthoc.npz`; (c) `forever_repro/ckpt_eta_m*/…/drift_log.csv` | (a) `forever_repro/eval_noise_summary.py` → `runs/forever_eval_noise_posthoc_summary.log`; (b) `ta_memory_posthoc.py` → `runs/ta_memory_posthoc.log`; (c) `forever_repro/skip_check_posthoc.py` → `runs/forever_skip_check_posthoc.log` |

## Groups

<!-- GROUPS -->
### Essential for repeating the test

| Group | Content | Files | Where |
|---|---|---|---|
| **E1. Start and integrity** | What to read first; hash lists recorded before the runs, earlier versions of the files they name, and the scripts that check them. Main files: `README.md`, `INDEX.md`, `FILES.tsv`, `SHA256SUMS.txt`, `CITATION.cff`, `Stadiul0/verify_hash_lists.py`, `Stadiul0/runs/*_sha256.txt`, `Stadiul0/runs/earlier_versions/`. | 30 (0.1 MB) | repository |
| **E2. Rules fixed before the runs** | The protocol draft that defines gate G2 and hypothesis H1; preregistrations and criteria, each hashed before the runs it governs, with English translations made after the study (`*_EN.md`, not hashed; the Romanian originals are binding). Main files: `Pilot2_Protocol_EN_draft.md`, `Stadiul0/preinregistrare_TA_TB_2026-11-06.md`, `Stadiul0/preinregistrare_SuperNI_2026-11-07.md`, `Stadiul0/forever_repro/preinregistrare_*.md`, `Stadiul0/*_criterii.md`, `Stadiul0/lm/*_criterii.md`. | 24 (1.0 MB) | repository |
| **E3. Code: synthetic world (CPU)** | Agent, world, schedules, triplets, configuration, launcher, automated checks, environment. Main files: `Stadiul0/README.md`, `Stadiul0/p2/`, `Stadiul0/config_stage0.yaml`, `Stadiul0/launch.py`, `Stadiul0/checks_stage0.py`. | 12 (0.1 MB) | repository |
| **E4. Code: language-model arm (GPU)** | The FOREVER schedule ported to Qwen3-0.6B + LoRA, on synthetic facts and on SuperNI; model provenance; environment. Main files: `Stadiul0/lm/lm_forever_run.py`, `Stadiul0/lm/lm_superni_run.py`, `Stadiul0/modele_provenienta.md`. | 4 (0.0 MB) | repository |
| **E5. Code: runs with the authors' FOREVER code** | Rebuilds the authors' working copy (their code is not redistributed), the clock-swap variant, evaluation helper, their environment. Main files: `Stadiul0/forever_repro/prepare_forever_copy.py`, `Stadiul0/forever_repro/make_clock_variant.py`. | 4 (0.0 MB) | repository |
| **E6. Launchers of the decisive runs** | The exact commands, seeds and output folders; also the generators of the post hoc checks (a) and (b) of the final review round. Main files: `Stadiul0/launch_*.sh`, `Stadiul0/lm/launch_lmtech*.sh`, `Stadiul0/forever_repro/*.sh`. | 15 (0.0 MB) | repository |
| **E7. Analyses** | The scripts behind every verdict, table and quoted number (including the post hoc checks (a)-(c) of the final review round and the leave-one-task-out R² added after the independent audit), and the script that re-runs them all. Main files: `Stadiul0/reproduce_analyses.py` and the scripts it runs (test map above). | 21 (0.1 MB) | repository |
| **E8. Stored results read by the analyses** | Run folders (arrays, per-run logs, meta.json), launch logs, analysis logs and verdict files; the large arrays and the LoRA adapters are in the Zenodo data part. Main files: `Stadiul0/runs/` (run folders, logs, verdict files), `Stadiul0/forever_repro/ckpt_*/`, `Stadiul0/forever_repro/logs/`, `Stadiul0/forever_repro/output/`. | 1003 (609.8 MB) | repository (441) + data part (562) |

### Not needed to repeat the test

| Group | Content | Files | Where |
|---|---|---|---|
| **N1. Decision path** | The research plan, the open decisions after the technical rounds, and the AI colloquia (dossiers, decision rules fixed in advance, answers as received, claim-by-claim verification). Main files: `Pilot2_Plan_ceasul_dual.md`, `Decizii_deschise_Pilot2_2026-11-07.md`, `Colocviu/` (start with its `README.md`). | 30 (0.8 MB) | repository |
| **N2. AI evaluations and the independent audit** | An informative annex: evaluations as received, with their verification: the protocol drafts, the final review round of the closure documents and the independent audit of this archive (see its README). Main files: `Recenzii/` (start with its `README.md`). | 93 (4.0 MB) | repository |
| **N3. Literature note** | What is known about the size of Adam/AdamW updates, and what was read of each source. Main files: `Literatura/Literatura_marime_actualizari_AdamW.md`. | 1 (0.0 MB) | repository |
| **N4. Earlier protocol drafts** | Protocol drafts v0.1, v0.2 and v0.3 (v0.3 also as it stood before the clarifications prompted by one AI evaluation), superseded by the v0.4 draft in E2. Main files: `Versiuni_anterioare/`. | 7 (2.0 MB) | repository |
| **N5. Working notes and running summary** | The Stage 0 notebook and the running summary of the decisive tests, written as the work went. Main files: `Stadiul0/Stadiul0_note_lucru.md`, `Rezultate_teste_decisive_2026-11-07.md`. | 2 (0.1 MB) | repository |
| **N6. Technical rounds, controls and diagnostics** | Configuration-choice rounds, determinism and bit-identity controls, smoke tests, diagnostics, and the small tools used for them. Main files: `Stadiul0/runs/` folders tech1, tech3_lr2e-4, g7_ram_*, lm_smoke, lmdiag, lmtech1_g7, sni_g7, ta_smoke, ta_smoke2, tech4_g7, tech4_g7_TB; check and diagnostic logs; small tools. | 276 (137.6 MB) | repository (108) + data part (168) |
| **N7. Hardware safety** | The watchdog that stopped runs on overheating or battery, and its logs (temperatures, power; no serial numbers). Main files: `Stadiul0/hw_watchdog.py`, `Stadiul0/runs/_hw/`. | 6 (0.7 MB) | repository |
<!-- /GROUPS -->

## Not in the archive

- **FOREVER's code and data** (https://github.com/WoodScene/FOREVER, commit `bbeb549`; no licence): rebuilt by
  `Stadiul0/forever_repro/prepare_forever_copy.py`, which checks them against the hashes recorded before the runs. The
  SuperNI task files come from the same repository (`data_superni/`).
- **Model weights** (Qwen3-0.6B from Hugging Face): the files used and their hashes are in `Stadiul0/modele_provenienta.md`.
- **Hardware reports** (they contain the laptop's serial numbers), temporary check folders, caches, and the intermediate
  checkpoints of the authors' code (optimizer states, tokenizer copies). The final LoRA adapter of every task is in the
  data part.
- **Two code versions that were not preserved:** the synthetic-world code of the technical rounds of 4 Nov (tech1–tech3),
  run before the corrections of 6 Nov; and the LM training script of the runs lmtech1 and lmtech2. Their stored results
  are in the archive, and the analyses reproduce from them. The configuration of each of these runs is in its `meta.json`,
  and for the LM runs so is the SHA-256 of the script.
- **The closure report** is a separate Zenodo record (https://doi.org/10.5281/zenodo.24188374).
