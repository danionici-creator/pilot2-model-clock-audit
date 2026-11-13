# Independent audit of the Pilot 2 package: brief for the auditor

You are asked for an independent, adversarial audit of a research package before its public release. Be as demanding
as a strict reviewer of a reproducibility study: look for errors, not for reassurance. Report what you find, with
evidence; do not fix anything in place.

## What the package is

Pilot 2 tested whether the "model-centric clock" of FOREVER (Feng et al., ACL 2026, arXiv:2601.03938), τ = Σ‖Δθ‖, and
related indices of accumulated parameter change carry information beyond cheap optimizer telemetry. Main claims: every
candidate was reconstructed out of sample from cheap telemetry or same-cost competitors (R² ≥ 0.90), so the planned
hypothesis H1 was not identifiable and was never run; as a replay clock, τ did no better than the free clock Ση‖m̂‖ in
the regimes tested.

Layout of this folder:
- `repository/`: the public archive (code, preregistrations, hash lists, logs, results), with the large data part
  already unpacked. Start with `repository/README.md` and `repository/INDEX.md` (test map, file groups).
- `documents/`: the closure report (`Pilot2_closure_report_draft_v0.1.md` / `.pdf`) and the Perspective paper
  (`Ionici_2026_A_Time_of_Their_Own_Perspective_v1.4.pdf` / `.docx`), a conceptual proposal that cites the report.
- `_audit/`: the only place where you may write.

Some documents are in Romanian. The eleven files of rules fixed before the runs have English translations next to them
(`*_EN.md`); the Romanian originals are the binding, hashed versions.

## Rules for the audit

1. **Do not modify, move or delete any existing file.** The preregistrations, scripts and results are hashed; any change
   breaks the verification. Write only inside `_audit/` (notes, your own check scripts, your report).
2. No network access except, if needed, installing Python packages listed in
   `repository/Stadiul0/requirements_cpu_2026-11-09.txt`. Do not download anything else. The FOREVER authors' code is
   not included (it has no licence and is not redistributed); do not download it. The model weights are not included.
3. No git operations, no accounts, no uploads.
4. For independence: form and write down your own findings **before** reading `repository/Recenzii/` and the
   verification documents in `repository/Colocviu/` (earlier AI reviews and their verification). You may read them
   afterwards and say where you agree or disagree.

## What to check

**A. Reproduction.** Run `python -I Stadiul0/reproduce_analyses.py` from `repository/` (CPU; about 3–4 minutes) and
`python -I Stadiul0/verify_hash_lists.py`. Then check that the scripts do what their names and the documents claim:
does `reproduce_analyses.py` really compare against the stored outputs; does `verify_hash_lists.py` really check
every entry?

**B. Code correctness (most important).** Read the code, not only the outputs. In particular:
- **Leakage in the out-of-sample R²** of the reconstruction analyses (`Stadiul0/g2_preview.py`, `td_audit.py`,
  `tech4_analysis.py`, `tb_part1_g2.py`, `lm/lm_forever_g2.py`, `lm/lm_d3_competitors.py`, `sni_analysis.py`,
  `forever_repro/r2_reconstruction*.py`): are training and test truly separated (by run, seed, task or family as
  claimed)? Is any scaling, feature selection or tuning fitted on the test part?
- **Target leakage in the features:** does any predictor (telemetry "B_strong", competitors C10c/C10p/C10h, the LM
  telemetry) contain the target itself or a near-copy of it?
- **Decision rules versus preregistrations:** do `ta_analysis.py`, `tb_part1_g2.py`, `sni_analysis.py`,
  `forever_repro/rep_verdict.py` apply exactly the thresholds, intervals and pairings written in the preregistrations
  and criteria files (`Stadiul0/preinregistrare_*.md`, `*_criterii.md`, `forever_repro/preinregistrare_*.md`)?
- **Fidelity of the port** (`Stadiul0/lm/lm_forever_run.py`, `lm_superni_run.py`) to the FOREVER schedule as described
  in its header and in the report (§4): calibration on 24 steps, thresholds d × day, replay phases, β, what is counted
  in τ, the declared deviations. And of the clock-swap variant (`forever_repro/make_clock_variant.py`): does it change
  only the counter that triggers replay?
- **The synthetic world** (`Stadiul0/p2/`): anything that would make the candidates trivially reconstructible by
  construction, or bias the comparison.
- **The post hoc checks** (a)–(c) and the tie diagnostic (`forever_repro/eval_noise_*.py`,
  `eval_tie_diagnostic_posthoc.py`, `lm/ta_memory_facts_posthoc.py`, `ta_memory_posthoc.py`,
  `forever_repro/skip_check_posthoc.py`).

**C. Results and interpretation.** For the report (`documents/Pilot2_closure_report_draft_v0.1.md`):
- does every number follow from the stored logs and JSON files it cites?
- does any sentence claim more than the data show (identifiability versus equivalence versus refutation; aggregate
  versus per task; port versus the authors' code)?
- is any limitation missing that a reviewer would expect?
- is the mathematical claim of §5.3 (τ is determined by the AdamW state) correct as stated?

**D. The Perspective paper** (`documents/…v1.4.pdf`): internal consistency, logical gaps (in particular the continuity
anchor of §4 and the closure rule of §5), claims not supported, and consistency with the report.

## What to deliver

Write `_audit/AUDIT_REPORT.md` with:
1. a summary verdict (is the package fit for release; what, if anything, blocks it);
2. a table of findings, one per row: **ID, part (A–D), file and line, what is wrong, evidence (how you checked),
   severity, suggested fix**. Severities: **fatal** (changes a verdict or a main claim), **major** (wrong number,
   wrong method detail, unsupported claim, missing important limitation), **minor** (wording, inconsistency without
   effect on conclusions);
3. what you checked and found correct (so that the absence of findings is informative);
4. what you could not check, and why.

Keep your own scripts in `_audit/` so that every finding can be re-run.
