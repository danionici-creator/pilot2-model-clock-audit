# Corecturi propuse după runda finală (9 nov. 2026)

**Stare: propuneri. Nimic nu e aplicat.** Fiecare punct trimite la `Verificare_runda_finala.md`, unde sunt verificarea și
evaluatorii care l-au ridicat. Se aplică doar punctele aprobate de autor; înainte de aplicare se fac copii de siguranță în
`_work\_copii_siguranta\`.

**Tipuri:**
- **F**: eroare de fapt confirmată (se corectează oricum, după regula 2);
- **O/N**: obiecție care a trecut pragul de 2 din 8 (după regula 3);
- **A**: decizia autorului (un singur evaluator sau o opțiune deschisă).

Prescurtări: R = raportul de închidere (`Raport_inchidere/Pilot2_closure_report_draft_v0.1.md`), P = Perspective v1.4
(textele propuse în `D:\Time\Perspective_v1.4_propunere.md`, M1–M17).

**Blocaj:** după regula 4, nicio intrare Zenodo nu se publică până nu sunt aplicate R3–R5 și P3, P6, P8 (O1), precum și
P9 (ancora), adică punctele marcate FATAL și confirmate.

---

## A. Raportul de închidere

**R1 (F, GPT-1). §5.2, paragraful de după tabelul R2.**
Acum: `The aggregate hides a 5.33-point difference on dbpedia in τ's favour (its forgetting −9.9 against −4.8), partly offset on amazon and yahoo.`
Propus:
```
The aggregate hides a 5.33-point difference on dbpedia in τ's favour (forgetting −4.8 under τ against −9.9 under Ση‖m̂‖), partly offset on amazon and yahoo.
```
Sursa: `runs/forever_repetari_verdict.json`, `dbpedia_forgetting` −4,81 și −9,89.

**R2 (F, DR-B6). §6 și referințele.** În text, „(Ionici 2026c, v1.4)” devine „(Ionici 2026d)”. În listă se adaugă:
```
- Ionici, I. D. (2026d). *A Time of Their Own: Agent-Held Temporal Evidence for Persistent AI Agents* (Version 1.4). Zenodo. [DOI-PERSPECTIVE-1.4]
```
DOI-ul v1.4 trebuie rezervat înaintea publicării raportului (în plan: ambele DOI-uri se rezervă înainte de orice
publicare).

**R3 (O1, O1c, O2, O4, O7, N1, N6; FATAL GPT-4, GEM-1). Rezumatul** (era „to be written last”). Propun textul final, de
aproximativ 260 de cuvinte:
```
The Perspective paper A Time of Their Own (v1.3) left open whether an agent's accumulated internal change, an "experiential index" c_e, carries information beyond the statistics an optimizer logs anyway. Pilot 2 set out to test this, under rules preregistered locally (hashed before each run, not deposited), on a synthetic continual-learning world and on a small language model trained with Adam and the replay schedule of FOREVER, a recent method that triggers replay with a "model-centric" clock τ = Σ‖Δθ‖. The confirmatory test was never reached. In our implementations, every candidate tested (three parameter-space distances, a functional distance, and τ itself) was reconstructed from cheap telemetry or from same-cost competitors with held-out R² ≥ 0.90 (exceptions only when a schedule family was left out of training), which makes the planned hypothesis unidentifiable under the protocol's own gate. Driving FOREVER's replay with the free clock Ση‖m̂‖ (learning rate times the norm of Adam's first moment) instead of τ left retention within the preregistered margins in our port, where the two clocks triggered replay at practically the same steps, and in aggregate with the authors' own code (three pairs of runs, after reproducing their reported score within 0.53 points in one run on one task order). There, Ση‖m̂‖ triggers replay systematically later (by 0–36 of 313 steps); a 5.3-point difference on one task did not recur consistently from common starting points (−0.5 and +3.3 points). The line "own time as accumulated internal change" therefore ends here without having been tested: its cheap candidates are not identifiable, and τ showed no scheduling advantage in the regimes tested. This is not evidence that they carry no information about forgetting.
```

**R4 (O1). §1, paragraful de după „Outcome”.**
Acum: `What is closed is the empirical line "own time = accumulated internal change" as a source of information beyond telemetry, *in this framework*: …`
Propus:
```
What ends here, *in this framework*, is the empirical line "own time = accumulated internal change" as a source of information beyond telemetry: its cheap candidates cannot be separated from telemetry, so the line has no testable candidate left in these regimes. This is not a refutation of H1, which was never run. The framework: …
```
(Restul frazei, de la „small models (a 0.93 M-parameter Transformer; …”, rămâne neschimbat.)

**R5 (O1, O5, N3). §6.**
- Titlul secțiunii: `What this closes, and what it does not` devine `What this settles, and what it does not`.
- Primul paragraf: `**Closed, in this framework.**` devine `**Not identifiable, in this framework.**`
- În paranteză, după „… and one seed was left out)”, se inserează:
```
; reconstruction thus has to be learned within the regime, and transfer to a family left out of training remains limited
```
- Ultima frază a paragrafului:
  Acum: `Perspective's Level 2 is revised accordingly (Ionici 2026c, v1.4): c_e remains a definition; the open question is answered negatively for the candidates tested.`
  Propus:
```
Perspective's Level 2 is revised accordingly (Ionici 2026d): c_e remains a definition, and its cheap candidates are not identifiable in the regimes tested. G2 is an operational threshold fixed in advance, not a proof: whether the remainder (up to 10% of the variance of the rate; at most 1% for D3 in T-B) predicts forgetting was not tested, because the forgetting targets were never opened.
```
- Paragraful „Not closed” devine `**Not settled.**`

**R6 (N3). §5.1, T-B, ultima frază.**
Acum: `The earlier exception was an artefact of extrapolating across families with one seed.`
Propus:
```
The earlier exception thus arises only when F6 is absent from training; once F6 is sampled, D3 is reconstructed. Transfer to a schedule family left out of training remains limited (T-D).
```

**R7 (N8). §5.1, T-D, după „… (D1_rel 0.74 in F3 and 0.82 in F6; D3 0.80 in F6).”** Se inserează:
```
They lie outside the fixed reading because G2, as defined in protocol v0.4, is computed by cross-fitting on calibration runs of the same schedule families (F2–F3), not with a family left out; values obtained with a family left out describe transfer and cannot open H1.
```

**R8 (N2, O2). §5.2, etapa 1, după „… cannot be separated.”** Se inserează:
```
The variance of the evaluation itself (stochastic decoding without a seed) was not measured, so part of these differences may be evaluation noise; the saved adapters would allow measuring it by inference alone.
```
În §7, punctul „Evaluation noise”, se adaugă la sfârșit: `; its size was not measured.`

**R9 (O2). §1, Outcome 2.**
Acum: `… gave retention within the preregistered margins of the τ-driven schedule in our port, and in aggregate with the authors' code (§5.2).`
Propus:
```
… gave retention within the preregistered margins of the τ-driven schedule in our port; with the authors' code the aggregate differences stayed within a descriptive ±2-point margin, and the comparison of single tasks is inconclusive (§5.2).
```

**R10 (O3). §7, punctul despre marje.**
Acum: `**Equivalence margins are descriptive** (±2 points; ±5% on loss); only T-A and S2 use paired confidence intervals, and those with few seeds.`
Propus:
```
**Equivalence margins are conventions** (±2 points; ±5% on loss), not derived from a smallest effect of interest, and no power analysis was made. Only T-A and S2 use paired 95% confidence intervals, with few seeds; inclusion of such an interval in the margin amounts to two one-sided tests at α = 0.025 each. Their widest bounds (−0.0147 on accuracy; −1.9% on loss) indicate the size of effect the data can exclude.
```

**R11 (O4). §3, după „Two consequences. … (§7).”** Se adaugă:
```
The tests after 4 Nov form an adaptive sequence: each was designed after the previous results, and its rules were fixed and hashed before its own runs (T-C and T-D: before computing, on runs that already existed). The preregistration of stage 1 went through three versions on 8 Nov (13:43; 13:58, after verified remarks of one AI reviewer; and a third after the short colloquium, which replaced the decision rule), all before any run of stage 1.
```

**R12 (N1). §5.2.**
- T-A, după „… so equivalence is shown under strong forgetting only.”:
```
With 16 of 512 facts per task in memory, most of each task cannot be replayed at all, which limits how much the timing of replay can matter. Between τ and Ση‖m̂‖ the triggers practically coincided, so their equivalence says little; the informative contrasts are the schedule-only clock and the step count, which triggered differently.
```
- S2, după „… 7 replays in both arms).”: `S2 therefore does not test a difference in timing.`

**R13 (N4).**
- §4, la sfârșitul paragrafului „Language-model arm, port”:
```
In every arm the replay strength β is computed from ‖Δθ‖, as in FOREVER; only the clock that triggers replay changes. Each phase starts a new AdamW, learning-rate schedule and (in fp16) GradScaler, as in the authors' code.
```
- §5.3, după „… it uses only what the optimizer already holds.”:
```
This holds for the clock. In our variants FOREVER's replay strength β still uses ‖Δθ‖, so removing the copy altogether would also require replacing β, for instance by η‖m̂‖, which was not tested.
```

**R14 (N5; și DS-A4, DR-A1 despre Atamna). §2.**
- „Known mechanism”, prima frază.
  Acum: `For Adam-type optimizers the size of a step is set by the learning rate and by the ratio of the first moment to the root of the second, so that ‖Δθ‖ ≈ η‖m̂‖/√v̄ (Kosson, Messmer & Jaggi 2024; …`
  Propus:
```
For Adam-type optimizers each coordinate moves by η m̂_i/(√v̂_i + ε), plus the decoupled weight decay where it is used (none in our language-model port). Hence ‖Δθ‖ ≈ η‖m̂‖/√v̄, where √v̄ stands for a typical value of √v̂_i; the approximation holds when v̂ varies little across coordinates and over time, and the per-coordinate preconditioning is what can break it (Kosson, Messmer & Jaggi 2024; …
```
- „Other uses”, primul punct.
  Acum: `Path-based learning-rate schedules compare the cumulative path of the parameters with that of a random walk, also for Adam (Atamna et al. 2025).`
  Propus:
```
Path-based learning-rate schedules compare the cumulative path of the parameters with that of a random walk; for Adam, the authors find that the optimizer's internal preconditioning makes this comparison inconsistent unless it is corrected (Atamna et al. 2025).
```

**R15 (N7). §8, notele 1 și 7.**
- Nota 1. Acum: `… (probably steps skipped by the GradScaler; not verified).` Propus:
```
… (consistent with steps skipped by the GradScaler, which the code does not log; at the first step of a phase the new optimizer holds no moments yet). The free clock adds nothing at those first steps, and at the three other such steps of the two η‖m̂‖ runs it adds at most 0.3% of the clock after calibration and 1.9% of one calibration window (`Recenzii/Runda_finala_2026-11-09/Verificari_faza2/skip_check.py`), so skipped steps do not explain note 7.
```
- Nota 7. Acum: `Which difference between the two implementations causes this was not established.` Propus:
```
Which difference causes this was not established. Our re-implementation also restarts AdamW, the schedule and the GradScaler at every phase, so these restarts alone do not explain it. The remaining differences changed together: the data loader restarting at every phase against one stream; fp16 with GradScaler against bf16; accumulation of 4 × 8 against one batch of 32; the loss over the sequence against the loss on the answer token; and the Trainer's own settings.
```
Dacă R15 e aprobat, scriptul `skip_check.py` intră în arhivă cu ieșirea lui (e deja în `Recenzii/Runda_finala_2026-11-09/`).

**R16 (N9, N10, N11, mărunțișuri).**
- §5.2, sub tabelul declanșărilor, după „… (0–36 steps)”: `, counting the thresholds after the first (at step 24 by construction) that both clocks reached: 8 in pair A and 9 in pair B. Each of tasks 1–3 has 313 steps.`
- §5.2, în paragraful R2, după „(up to 33 of 313 steps)”: `; the 36 of stage 1 compares runs from the same task-0 adapter`.
- §5.2, sub tabelul etapei 1: `Differences are computed from unrounded values.`
- §7, după „… (11 of 13; four of them reconstructed and identified by their recorded hash)”: `; the two not recovered are the LM training script of lmtech1 and lmtech2 (below) and a first version of td_audit.py, replaced one minute later, whose output is archived`.
- §5.1, la prima apariție a lui tech3: `(technical rounds of the synthetic world: tech2 and tech3 on 4 Nov; tech4 on 6 Nov, with the corrected code)`.

**R17 (A, opțional: DR-A4).** În §4 se definesc ΔN (numărul de pași din fereastră) și C6 (statisticile proprii ale lui D1 din
B_strong), iar în portul LM se spune „512 synthetic facts per task”. Precizări ieftine; le recomand.

---

## B. Perspective v1.4 (modificări ale textelor propuse în M1–M17, plus M18 nou)

**P1 (F). M2, rândul „Changes”.**
Acum: `… and found them reconstructed from free optimizer telemetry [@ionici2026p2]; …`
Propus:
```
… and found them not identifiable, each reconstructed from free optimizer telemetry or from a competitor of the same cost [@ionici2026p2]; …
```

**P2 (F, O2). M4, rezumatul.**
Acum: `… in small models trained with Adam, each was reconstructed from free optimizer telemetry, and as a replay clock the update-norm index did no better than a free one.`
Propus:
```
… in small models trained with Adam, each was reconstructed from free optimizer telemetry or from a competitor of the same cost, and as a replay clock the update-norm index did no better than a free one in the regimes tested.
```
Scurtarea rezumatului (D1) e separată; vezi C.

**P3 (F GLM-13, O1, N1, N12). M6, paragraful despre al doilea studiu**, comprimat. Textul propus în M6, de la „A second
study asked …” până la „… and other optimizers.”, devine:
```
A second study asked whether such an index carries information beyond logged optimizer statistics [@ionici2026p2]. Three parameter-space distances, in a synthetic continual-learning world, and the update-norm clock, in a 0.6-billion-parameter language model trained with LoRA and Adam, were reconstructed out of sample chiefly from the learning rate times the norm of Adam’s first moment, which the optimizer already holds; a functional distance on probes, in both settings, was reconstructed from the change of loss on the same probes, a competitor of the same cost (R² ≥ 0.90, except when a schedule family was left out of training). Under Adam the size of a step is set by moments the optimizer keeps, so this was expected for the parameter-space quantities. Used as a replay clock, the update-norm index did no better than that free quantity in the regimes tested: in a re-implementation, where the two clocks triggered replay at practically the same steps, and in aggregate with the original code. For these candidates, in these regimes, the index is therefore not identifiable: the study found no basis to test whether it predicts adaptation, and it does not show that it cannot. What remains open are the costly candidates — change in measured competences and counterfactual influence — and larger models, full fine-tuning, and other optimizers.
```
Pentru criteriul de admisibilitate din același paragraf:
Acum: `A candidate is admissible only if it is not reconstructed out of sample from the optimizer’s own state — learning rate, moment norms, and schedule — and beats …`
Propus:
```
A candidate is admissible only if it is not reconstructed out of sample from its competitor’s inputs — the optimizer’s own state (learning rate, moment norms, schedule) or a measure of the same cost — and beats …
```

**P4 (N13). M17a, ultima frază.**
Acum: `… is untested; its natural competitor is the count and size of the writes.`
Propus:
```
… is untested; its natural competitors are what a memory system already records — the count and size of writes, versions, provenance, and revocations — and the same reconstruction may recur there.
```
În M17c, `; for state that changes without gradient updates, the count and size of writes` devine `; for state that changes without gradient updates, the memory system’s own records of writes, versions, provenance, and revocations`.

**P5 (F). M7, Tabelul 2, poarta nivelului 2.**
Acum: `'Must not be reconstructed out of sample from the optimizer’s state, and must beat …`
Propus:
```
'Must not be reconstructed out of sample from the competitor’s own inputs (the optimizer’s state, or a measure of the same cost), and must beat …
```
Nota de sub tabel (F, GLM-14). Acum: `Level 2 has been tested for its cheapest candidates since version 1.2: they are not identifiable in the regimes tested [@ionici2026p2] (§4).` Propus:
```
Level 2 has now been tested for its cheapest candidates: they are not identifiable in the regimes tested, which neither closes the level nor supports it [@ionici2026p2] (§4, §5).
```

**P6 (N14, O1c, O5). M8, amendamentul din §5.**
Acum: `… If a candidate is reconstructed out of sample from the competitor’s own inputs, above a threshold fixed in advance, it carries no testable information beyond them. The hypothesis is then reported as not identifiable for that candidate and regime, never as equivalence and never as support. This exit was added in version 1.4, after the second study met it [@ionici2026p2].`
Propus:
```
… If a candidate is reconstructed out of sample from the competitor’s own inputs, above a threshold fixed in advance, it carries no information beyond them that the test could detect. The hypothesis is then reported as not identifiable for that candidate and regime: never as equivalence, never as support, and not as closure of the level. The candidate is set aside, and costlier candidates remain open. The exit concerns only the comparison that could not be run; a secondary comparison that was run, such as the use of a candidate as a replay clock, is reported by the rule above. This exit was added in version 1.4, after the second study met it [@ionici2026p2], and applies to later tests; that study had fixed the same gate and the same outcome in its own protocol before its runs.
```

**P7 (F, N3). M10, cele două precauții noi.**
- Prima, ultima frază. Acum: `Any candidate index must be reconstructed from free telemetry before its predictive value is tested: if it is reconstructed, its value cannot be identified.` Propus:
```
Before its predictive value is tested, any candidate index must be checked for reconstruction from its competitors’ inputs — free telemetry, or measures of the same cost: if it is reconstructed above a threshold fixed in advance, its value cannot be identified. The threshold is operational; the remainder it leaves untested could still matter.
```
- A doua. Acum: `{b|An exception found by extrapolation must be re-tested inside its regime.} … it was reconstructed at 0.99. An exception counts as evidence only once it recurs where it was found.` Propus:
```
{b|An exception found by extrapolation is a limit on transfer, not yet evidence of information.} A functional distance seemed to escape reconstruction in one schedule family, with that family left out of training and one seed (R² 0.81); with the family sampled, on eight new seeds and leaving one seed out, it was reconstructed at 0.99. The reconstruction has to be learned within the regime; an exception counts as evidence only if it persists there.
```

**P8 (O1b, F). M12, concluzia.**
Acum: `One level has since been tested for its cheapest candidates, and the statistics the optimizer already keeps proved sufficient [@ionici2026p2]; …`
Propus:
```
One level has since been tested for its cheapest candidates, which proved not identifiable: free optimizer telemetry, or a measure of the same cost, reconstructed each of them [@ionici2026p2]; …
```

**P9 (F, O10; FATAL GPT-5). M18 nou: §4, ancora de continuitate (`persp_content.js`, rândul 75; textul din v1.3).**
Acum:
```
If {i|N} exceeds {i|N}({i|t}_{0}), the agent has operated since that state was saved and has been restored; if {i|N} equals {i|N}({i|t}_{0}) while {i|c}_{a} has advanced beyond its calibration error, it has been suspended; if both have advanced together, it has operated without interruption. The pair ({i|c}_{a}, {i|N}) is necessary and sufficient for this distinction, and it is what state-continuity protocols already maintain for data [...]
```
Propus:
```
When a state is loaded, the live values are compared with the sealed copies it carries. If the live {i|N} exceeds {i|N}({i|t}_{0}), the agent has committed steps since that state was saved, so the loaded state is not its latest: it has been restored. If {i|N} equals {i|N}({i|t}_{0}) while {i|c}_{a} has advanced beyond its calibration error, no step has been committed since the save: the agent was suspended, or ran without committing a step. While the agent runs, each commit renews the sealed copies, so both values advance together. Under the assumptions stated below — one lineage, a counter the host cannot reset and a key it cannot read, and crash-consistent commits — the pair ({i|c}_{a}, {i|N}) suffices for this distinction; forking and cloning, discussed below, lie outside it. The pair is what state-continuity protocols already maintain for data [...]
```
În schița de protocol, pasul (3), opțional: `an equal counter with the time reference advanced beyond calibration error is a suspension` devine `… is a suspension, or an interval without committed steps`. Rândul „Changes” (M2) primește o propoziție: `It corrects the description of the continuity anchor (§4).`

**P10 (O9). §5, după „No such contract is provided here.”** (`persp_content.js`, rândul 85). Se inserează:
```
The first to write is the contract for Level 4: detection of suspension and restoration against the flag of a trusted monitor, with the margin, the sample of events, and the decision rule fixed in advance.
```

**P11 (F, DR-E). Referințele M16.**
- `benzing2022`: la sfârșit se adaugă `. arXiv:2006.06357`.
- `zenke2017`: `(PMLR 70)` devine `(PMLR 70, pp. 3987–3995)`, păstrând `arXiv:1703.04200`.

---

## C. Decizii ale autorului

- **D1, rezumatul P.** Toți cei șase evaluatori din faza 2 recomandă scurtarea la aproximativ 250–300 de cuvinte. Pot redacta
  o variantă scurtă, după ce hotărăști.
- **D3, amendamentul.** Toți șase recomandă păstrarea, cu proveniență și gardă: P6 le include.
- **D6, SI/Benzing și direcția agenților cu memorie.** Toți șase recomandă păstrarea: P4 îngustează afirmația.
- **Analize sau rulări posibile** (niciuna nu e cerută de regulă; fiecare ar fi post hoc și ar intra în raport ca atare):
  - (a) reevaluarea adaptoarelor finale ale celor patru celule din etapa 1, de câteva ori fiecare, pentru zgomotul
    evaluării (GPU, doar inferență; durata o estimez înainte de pornire);
  - (b) retenția T-A pe cele 16 fapte din memorie, din rezultatele existente, dacă jurnalele o permit (CPU);
  - (c) analiza reziduului față de uitare, adică deschiderea țintelor T1 (schimbă statutul „never opened” din raport);
  - (d) rulări care înregistrează ambele ceasuri (GPU, câteva ore).
- **Puncte ridicate de un singur evaluator:** lista e în `Verificare_runda_finala.md`. Nu propun schimbări pentru ele, în
  afară de R17.

---

**Notă de aplicare (10 nov. 2026).** Toate punctele R1–R17 și P1–P11 au fost aplicate cu acordul autorului (9 nov.). R8 a
fost înlocuit după testul post hoc (a): decodarea autorilor (`top_k=1`, `top_p=0`) păstrează doar tokenul cel mai probabil,
iar două reevaluări cu semințe fixe au reprodus toate răspunsurile, deci „stochastic decoding … was not measured” devenise
inexact; raportul spune acum rezultatul măsurat (§5.2, §7, §8 nota 6). În Perspective s-au adăugat la aplicare M20 (rândul
DOI; „Level 2” în „Changes”) și M21 (întârzierea în codul autorilor; numărul de pași în port), descrise în propunere.
