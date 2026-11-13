# About this folder: AI evaluations of the Pilot 2 protocol drafts (27 October – 4 November 2026)

*Informative annex. A Romanian version follows the English text.*

## What these documents are

This folder keeps the evaluations of the Pilot 2 protocol drafts (v0.1–v0.4) requested from AI systems before any
experiment was run, the prompts that were sent, and the author's claim-by-claim verification of each evaluation.
Read in order, they allow the path of the study to be reconstructed: the successive versions of the plan, the
dilemmas met along the way, the obstacles (design errors, unidentifiable hypotheses, costs that did not fit a laptop)
and how each was resolved, kept, or set aside.

They are an annex for readers who want that history, **for information and documentation only.** They are not results
of the study and they support none of its conclusions; the results, with their limits, are in the closure report
(https://doi.org/10.5281/zenodo.24188374).

## How to read them

- **Status of the texts.** The evaluations are texts produced by AI systems, reproduced as received, without
  correction. They are not the author's views. Model names and settings are those shown by each provider on the date
  of use.
- **They contain errors.** Each evaluation was checked point by point against the protocol text, the code and the
  cited sources. The verification documents (in Romanian, `Pilot2_v0.*_verificare_*.md`) say which points were
  accepted, which were rejected and why. A point should not be quoted from an evaluation without its verification.
- **They concern superseded drafts.** The drafts are in `../Versiuni_anterioare/` and `../Pilot2_Protocol_EN_draft.md`
  (v0.4, never frozen). Each draft from v0.2 on has a revision log (§19, §20, §21) listing every change with its source.
- **Decisions.** These evaluations informed the revisions of the protocol. The later direction decisions (6 and
  8 November) were taken differently: through colloquia under decision rules fixed in advance; see `../Colocviu/`.
- `Mistral_detalii/` holds, for the Mistral API calls, the exact message sent, the raw API response (identifier,
  model, token counts, time) and the intermediate reasoning text returned by the model, kept for completeness.

## Index, in order

| Date (2026) | Draft | Prompt sent | Evaluation (system, settings) | Verification | What followed |
|---|---|---|---|---|---|
| 27 Oct | v0.1 | `Prompturi/Pilot2_Prompt_Argon.txt` | `Recenzie_Argon_Pilot2_v01.md` (Argon, Deep Review platform, Extra High depth; **partial**: the run stopped when the API credit ran out, and the text ends at question 12, item 8) | in the v0.2 revision log (§19 of v0.2) | v0.2 |
| 27 Oct | v0.1 | `Prompturi/Pilot2_Prompt_Argon_continuare.txt` | none: prepared to continue the interrupted run; the run was not resumed | — | — |
| 3 Nov | v0.2 | `Prompturi/Pilot2_Prompt_Argon_v02.txt` | `Recenzie_Argon_Pilot2_v02.md` (Argon 4, Deep Review, Medium depth) | `Pilot2_v0.3_verificare_recenzie_v02.md` (8 points marked fatal; 2 confirmed) | v0.3 (§20) |
| 3–4 Nov | v0.3 | `Mistral_detalii/mistral_msg_v03.txt` | `Recenzie_Mistral_Large4_v03.md` (Mistral Large 4, API) | applied as 5 clarifications to v0.3 (§20) | v0.3 clarified |
| 4 Nov | v0.4 | `Prompturi/Pilot2_Prompt_evaluare_v04.txt` | `Recenzie_DeepReview_Pilot2_v04.md` (Argon 4, Deep Review, Extra High depth, High thinking) | `Pilot2_v0.4_verificare_recenzie_DeepReview.md` (six points judged fatal after verification: B1, B5, C1, C4, E1, F1) | calibration not started on v0.4 |
| 4 Nov | v0.4, direction | `Mistral_detalii/mistral_msg_directie_v04.txt` | `Recenzie_Mistral_Large4_directie_v04.md` (low reasoning), `…_medium.md` (medium reasoning) | `Pilot2_v0.4_verificare_directie_Mistral.md` | synthesis below |
| 4 Nov | v0.4, direction | `Prompturi/Pilot2_Prompt_directie_v04_chat.txt` | `Recenzie_Copilot_directie_v04.md` (Copilot, Think Deeper), `Recenzie_Gemini_directie_v04.md` (Gemini 3.1 Pro, High), `Recenzie_ChatGPT_directie_v04.md` (ChatGPT, GPT-6, High) | `Sinteza_directie_5_opinii.md` (references checked; points of agreement and of error) | technical checks, then the colloquium of 6 Nov |
| 4 Nov | — | `Prompturi/Pilot2_Prompt_literatura_AdamW.txt` | none: **prepared, never sent** (the literature check was done directly; `../Literatura/`) | — | — |

## The final review round of the closure documents (9 November 2026)

`Runda_finala_2026-11-09/` holds a later and different round: automated evaluations of the closure report and of the
draft of Perspective version 1.4, requested after the study had ended and before publication. The adoption rule was
fixed and hashed before anything was sent (`Regula_de_adoptare_2026-11-09.md`, `SHA256SUMS_2026-11-09.txt`): a verified
factual error is corrected; an objection of interpretation is adopted if at least 2 of the 8 evaluators raise it and
verification confirms it; a confirmed fatal point blocks publication until corrected.
- Phase 1: CMU Paper Reviewer and Stanford Agentic Reviewer (`Trimiteri_faza1.md`, `Adaptari_conditii_2026-11-09.md`).
  Phase 2: DeepSeek, GLM, Le Chat (Mistral), ChatGPT, Gemini and Deep Review, all sent before any answer was read
  (`Trimiteri_faza2.md`). The documents sent are kept (`*_review_draft.*`, `Dosar_combinat_DeepReview.pdf`) with the
  prompts (`Prompt_analiza_EN*.txt`); the answers are in `Raspunsuri/`, as received.
- `Verificare_runda_finala.md` checks every claim (in Romanian); `Corecturi_propuse_faza2.md` lists the corrections
  (R1–R17 for the report, P1–P11 for Perspective), all approved by the author and applied on 9 November.
  `Verificari_faza2/skip_check.py` is the check of skipped steps made for the round; its archived copy is
  `../Stadiul0/forever_repro/skip_check_posthoc.py`.
- `Raspunsuri/Extra_Copilot_Perspective_v13_v14.txt` is a supplementary evaluation received after the round (Copilot,
  on the two Perspective PDFs only); it is not counted under the rule, and its verification is at the end of
  `Verificare_runda_finala.md`.
- Access keys and tokens of the evaluation services are kept outside the archive. In this public copy, the links to
  the author's private conversations in the headers of three answers (`Faza2_Gemini.txt`, `Faza2_GLM.md`,
  `Faza2_DeepReview.md`) are replaced by "[private link, omitted]" (the files are in no hash list; nothing else in them
  is changed).

## The independent audit of the archive (10–12 November 2026)

`Audit_Codex_2026-11-10/` holds an independent audit of this archive and a scientific review of Perspective v1.4, made
in OpenAI Codex (model GPT-6 Astra, highest effort) on a private copy of the release, without access to the author's
other files and without network, except for a sample of references in the second task. The adoption rule and the two
briefs were fixed and hashed before sending (`Regula_de_adoptare_audit_Codex.md`, `AUDIT_BRIEF.md`,
`PERSPECTIVE_REVIEW_BRIEF.md`, `SHA256SUMS_audit_2026-11-10.txt`): a verified error of code or fact is corrected, and a
code correction becomes a new version declared post hoc; a confirmed fatal error stops publication; a point of
interpretation is adopted only if the files confirm it, and a change of framework is noted for a later version.
- `raspuns/` holds the two answers as received (`AUDIT_REPORT.md`, `PERSPECTIVE_REVIEW.md`), with the auditor's
  intermediate reports, scripts and logs. Its large working copy is not kept.
- `Verificare_audit_Codex.md` verifies every finding in the files (in Romanian), with the assistant's own read-only
  checks in `verificare_asistent/`. No fatal finding was confirmed. The corrections it confirmed were applied on
  12 November, after the author's approval: wording in the closure report and in Perspective v1.4, stricter archive
  tools (`Stadiul0/reproduce_analyses.py`, `Stadiul0/verify_hash_lists.py`) and one post hoc analysis
  (`Stadiul0/forever_repro/r2_heldout_task_posthoc.py`). Points of framework are noted for a later version.

---

# Despre acest folder: evaluările AI ale ciornelor de protocol Pilot 2 (27 octombrie – 4 noiembrie 2026)

*Anexă informativă.*

Folderul păstrează evaluările ciornelor de protocol Pilot 2 (v0.1–v0.4) cerute unor sisteme AI înainte de orice
experiment, prompturile trimise și verificarea punct cu punct a fiecărei evaluări, făcută de autor. Citite în ordine,
ele permit reconstituirea drumului parcurs: versiunile succesive ale planului, dilemele întâlnite, obstacolele (erori
de design, ipoteze neidentificabile, costuri care nu încăpeau pe un laptop) și felul în care fiecare a fost rezolvat,
păstrat sau lăsat deoparte.

Sunt o anexă pentru cei interesați de acest istoric, **doar în scop informativ și de documentare**. Nu sunt rezultate
ale studiului și nu susțin niciuna dintre concluziile lui; rezultatele, cu limitele lor, sunt în raportul de închidere
(https://doi.org/10.5281/zenodo.24188374).

Cum se citesc: evaluările sunt texte produse de sisteme AI, păstrate așa cum au venit, fără corecturi, și nu exprimă
opiniile autorului. Conțin erori: documentele de verificare (`Pilot2_v0.*_verificare_*.md`) spun ce s-a acceptat, ce
s-a respins și de ce, așa că un punct dintr-o evaluare nu trebuie citat fără verificarea lui. Ciornele evaluate sunt
depășite; fiecare, de la v0.2 încolo, are un jurnal al schimbărilor cu sursa fiecăreia. Deciziile de direcție de după
4 noiembrie s-au luat altfel, prin colocvii cu reguli de decizie fixate dinainte (`../Colocviu/`). Indexul de mai sus
dă ordinea documentelor.

**Runda finală (9 noiembrie 2026).** `Runda_finala_2026-11-09/` conține evaluările automate ale raportului de închidere
și ale ciornei Perspective 1.4, cerute după încheierea studiului, sub o regulă de adoptare fixată și amprentată înainte
de trimitere (`Regula_de_adoptare_2026-11-09.md`): eroarea de fapt verificată se corectează; obiecția ridicată de cel
puțin 2 din 8 evaluatori și confirmată se adoptă; punctul fatal confirmat blochează publicarea. Răspunsurile sunt în
`Raspunsuri/`, așa cum au venit; verificarea, în `Verificare_runda_finala.md`; corecturile (R1–R17, P1–P11), aprobate
de autor și aplicate pe 9 noiembrie, în `Corecturi_propuse_faza2.md`. Cheile de acces la evaluări nu sunt în arhivă; în copia publică, linkurile către conversațiile private ale autorului
din antetele a trei răspunsuri sunt înlocuite cu „[private link, omitted]”.

**Auditul independent (10–12 noiembrie 2026).** `Audit_Codex_2026-11-10/` conține un audit independent al acestei arhive
și o recenzie științifică a Perspective v1.4, făcute în OpenAI Codex (modelul GPT-6 Astra, efort maxim) pe o copie
privată a pachetului, sub o regulă de adoptare și cu instrucțiuni fixate și amprentate înainte de trimitere. Răspunsurile
sunt în `raspuns/`, așa cum au venit; verificarea punct cu punct, în `Verificare_audit_Codex.md` (cu verificările proprii
în `verificare_asistent/`). Niciun punct fatal confirmat; corecturile confirmate au fost aplicate pe 12 noiembrie, cu
acordul autorului; punctele de cadru sunt notate pentru o versiune ulterioară.
