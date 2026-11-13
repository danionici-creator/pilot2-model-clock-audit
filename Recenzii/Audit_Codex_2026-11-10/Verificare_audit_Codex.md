# Verificarea auditului independent Codex (12 nov. 2026)

**Ce se verifică:** cele două răspunsuri ale auditului independent făcut în OpenAI Codex (modelul **GPT-6 Astra, efort Extra High**, după precizarea autorului din 12 nov.), copiate exact în `raspuns\`:
1. auditul pachetului Pilot 2, `raspuns\AUDIT_REPORT.md` (B01–B04, A01–A03, C01–C05, D01–D04), cu scripturile și jurnalele lui;
2. recenzia Perspective v1.4, `raspuns\PERSPECTIVE_REVIEW.md` (P01–P23, recomandarea „major revision”).

**Regula aplicată:** `Regula_de_adoptare_audit_Codex.md`, fixată înainte de trimitere. Amprentele au fost reverificate azi și corespund (`085efea6…` regula, `7e5889fe…` AUDIT_BRIEF, `0921854f…` PERSPECTIVE_REVIEW_BRIEF).

**Stare: verificare încheiată, NICIO CORECTURĂ APLICATĂ.** Corecturile propuse (§3) așteaptă acordul autorului.

**Verdicte folosite:** *adevărată* (confirmată în fișiere), *parțial adevărată* (miezul e corect, dar formularea sau gravitatea e exagerată ori o parte e deja tratată), *falsă* (contrazisă de fișiere), *deja tratată* (problema e reală, dar textul sau o analiză o rezolvă deja). Propunerile: **A** = de adoptat acum (corectură locală, confirmată); **A?** = adoptabilă, dar e decizia autorului; **N** = de notat pentru o versiune ulterioară (schimbare de cadru, de structură sau de contract; un singur evaluator nu o poate impune, regula 3); **—** = nu se aplică.

## 0. Cum s-a verificat

- **Identitatea fișierelor.** Copia auditată `D:\Pilot2_audit\` are aceleași fișiere ca sursele din `D:\Time`. Am comparat SHA-256 pentru 11 fișiere-cheie (g2_preview, triplets, td_audit, r2_reconstruction*, lm_superni_run, lm_forever_run, reproduce_analyses, verify_hash_lists, tech4_analysis, raportul MD): toate identice. PDF-ul Perspective v1.4 are aceeași amprentă (`dd09e7a3…`) în `_work\_persp_v14_final\`, în `D:\Pilot2_audit\documents\` și în `D:\Pilot 2\`.
- **Verificări proprii, care doar citesc**, cu scripturile și ieșirile lor în `verificare_asistent\`:
  - `a_checks.py`: liniile din listele de amprente și valorile ne-finite sau containerele goale din JSON-urile stocate;
  - `strict_compare.py`: rerularea celor 6 analize FOREVER care scriu JSON, pe o copie temporară, cu un comparator strict;
  - `c02_heldout.py`: R² în eșantion față de R² cu sarcina lăsată deoparte;
  - `b04_count.py`: răspunsurile și intrările SuperNI tăiate, numărate cu tokenizerul Qwen3-0.6B pe datele reale.
- **Alte verificări:**
  - rularea `g2_preview.py` (doar tipărește) și compararea cu tabelul 1 din raport;
  - citirea filtrelor top-k și top-p din `transformers` 4.57 (`_venv_forever`);
  - textul Perspective v1.3 față de v1.4, pentru a vedea care formulări sunt noi;
  - versiunile protocolului din `Versiuni_anterioare\`;
  - referințele [5], [20], [21] și [54], verificate azi la Crossref, arXiv și DataCite.
- **Fișierele sursă nu au fost atinse.** Analizele rerulate au scris doar în copia temporară.

## 1. Auditul pachetului (AUDIT_REPORT.md)

Verdictul Codex: „revise before public release; no fatal finding”. **Confirmat: nicio eroare fatală.** Niciun verdict preînregistrat și niciun număr pe care se sprijină un verdict nu se schimbă.

### B: corectitudinea codului

**B01: C6 în B_strong din `g2_preview.py`.**
*Verdict: adevărată, deja tratată (T-D (1)).* Gravitatea reală: minoră (Codex: major).

- `g2_preview.py:24–27` pune `C6_*` în B_strong.
- `p2/triplets.py:107–110` construiește C6_pre și C6_post din `st["dpre_norm"]` și `st["D1"]`: media și abaterea standard pe primii și ultimii W = min(16, ΔN//4) pași ai intervalului (`triplets.py:38–46`). Sunt deci statistici parțiale ale țintei D1 însăși.
- Problema e cunoscută din 6 nov. ca „eroarea E1” (`td_criterii.md:5`). A fost testată în T-D (1), cu criteriile fixate înainte: fără C6, R² nu se schimbă. În `runs/td_audit.log`, D1 dă 0,983 și 0,994 fără C6, față de 0,984 și 0,992 cu C6. D3 dă 0,916/0,961 față de 0,919/0,960.
- Chiar `check_b.log` al Codex arată corelații între C6_post și rata lui D1 de doar −0,04…0,24.
- Raportul numește C6 în §4 (r. 71) și dă T-D (1) în §5.1 (r. 94). Lipsește doar ca sursa tabelului 1 (r. 92) să spună că coloanele B_strong conțin C6.

*Propunere: A.* O propoziție la r. 92: „The B_strong columns include the C6 features, which contain D1's own statistics; T-D (1) below removes them, with unchanged results.” Nicio reanaliză.

**B02: R² din codul autorilor, calculat în eșantion.**
*Verdict: adevărată.* Gravitatea reală: moderată (nu atinge niciun verdict).

- `r2_reconstruction.py:19–24, 39, 45` și `r2_reconstruction_arm.py:16–21` potrivesc OLS (intercept + pantă) și îl evaluează pe aceleași ferestre. Cu un singur predictor, R² în eșantion e pătratul corelației: măsoară asocierea liniară, nu reconstrucția în afara eșantionului.
- Raportul dă aceste valori fără eticheta „in-sample”: §5.1 (r. 104: 0,922; 0,937/0,986/0,934/0,578; 0,749; 0,969) și §1 punctul 3 (r. 29: 0,75 și 0,97). În restul §5.1 și în rezumat, R² e „held-out”.
- Am recalculat independent (`c02_heldout.log`), cu modelul potrivit pe celelalte sarcini și aplicat sarcinii lăsate deoparte:

  | Rularea | dbpedia | amazon | yahoo | agnews |
  |---|---|---|---|---|
  | R2 | 0,724 | 0,950 | 0,892 | 0,373 |
  | A1 | — | 0,981 | 0,966 | 0,955 |

  Valorile sunt identice cu `check_b.log` al Codex.
- Lectura nu se schimbă. În A1, raportul dintre ceasuri e stabil și între sarcini (≥ 0,955). În R2 derivă (agnews), compatibil cu analiza (d). Poarta pentru τ se sprijină pe port și pe SuperNI, ambele held-out.

*Propunere: A.* Eticheta „in-sample (OLS with one predictor, fitted and scored on the same windows)” la r. 104 și r. 29, plus valorile cu sarcina lăsată deoparte, marcate post hoc. *Varianta recomandată:* un script nou, arhivat și declarat post hoc (`forever_repro/r2_heldout_task_posthoc.py` + jurnal), adăugat în `reproduce_analyses.py`, care trece astfel la 23 de analize. *Varianta minimă:* doar eticheta și citarea numerelor.

**B03: bugetul de pași pe epocă în SuperNI.**
*Verdict: adevărată (fapt de cod).* Gravitatea reală: minoră; verdictul S2 neatins.

- `lm_superni_run.py:211` calculează `total = ceil(n/32 · epochs)`, dar generatorul (`:110–114`) dă epochs · ceil(n/32) loturi, cu un ultim lot parțial în fiecare epocă.
- Din `runs/sni/tau/s7401/run.log`:
  - task363, task1290 și task002 (n = 1.000, 3 epoci): 94 de pași din 96 de loturi;
  - task181 (n = 338): 32 din 33;
  - task1572 (n = 160, 10 epoci): 50 din 50.
- Așadar ultimele 30–40 de exemple ale epocii a treia nu au fost văzute a treia oară (2,96 epoci; 98,7% și 98,2% din prezentări).
- Regula e aceeași în ambele brațe și în toate cele trei semințe, iar S2 e o comparație pereche. Brațul LM (512 fapte, lot 32) nu e atins.
- Scriptul e amprentat înainte de rulări (`runs/preinregistrare_SuperNI_sha256.txt:4`), deci nu se modifică.

*Propunere: A.* Declararea în raport §4 (SuperNI): „the step budget is ceil(3n/32): 94 of 96 batches on the three tasks of 1,000 examples and 32 of 33 on task181, i.e. 2.96 epochs”. Nicio rerulare.

**B04: răspunsurile tăiate la 256 de tokeni.**
*Verdict: parțial adevărată.* Plafonul există în cod, dar nu a tăiat niciun exemplu.

- `lm_superni_run.py:82` taie răspunsul la cutoff//2 = 256 de tokeni. Antetul (`:17`) declară doar tăierea intrării.
- Am numărat cu tokenizerul Qwen3-0.6B pe cele 5 sarcini (`b04_count.log`). Cel mai lung răspuns, cu EOS, are 73 de tokeni (task1572). **0 răspunsuri tăiate**, în train și în test. Pierderea a fost deci peste tot cea pe răspunsul întreg, iar abaterea declarată descrie exact ce s-a întâmplat.
- Observație proprie, nesemnalată de Codex: intrarea a fost tăiată la 426 din 1.000 de exemple de antrenare în task1290, la 595 din 1.000 în task002 și la 5 din 160 în task1572. În test: 40/100, 58/100 și 1/20. Instrucțiunea nu a fost tăiată niciodată. Tăierea intrării e declarată, dar proporția nu e dată.

*Propunere: A.* O propoziție în raport §4: plafonul de 256 există în cod și nu a tăiat niciun răspuns (maximum 73 de tokeni); intrarea a fost tăiată la 43% și 60% din exemplele de antrenare ale task1290 și task002.

### A: reproducerea și integritatea

**A01: comparatorul JSON din `reproduce_analyses.py`.**
*Verdict: adevărată (defect al instrumentului), fără efect asupra rezultatelor raportate.*

- `same_json` (`:81–97`) acceptă NaN în locul unei valori finite: diferența e NaN, iar `NaN > TOL` e fals. Containerele goale dispar la aplatizare.
- JSON-urile stocate nu conțin nicio valoare ne-finită și niciun container gol (`a_checks.log`).
- Am rerulat pe o copie cele 6 analize FOREVER care scriu JSON, inclusiv cele trei fără jurnal (FOREVER-R2-arm-eta_m, FOREVER-d, FOREVER-stage1). Le-am comparat strict (structura, tipurile, valorile finite, toleranța 1e-9): **toate 6 corespund** (`strict_compare.log`).
- Celelalte 4 JSON-uri (T-A, T-B, SuperNI, post hoc (b)) au și jurnale comparate rând cu rând.
- `reproduce_analyses.py` e un instrument de arhivă scris pe 9 nov., după studiu, și nu e în listele de amprente dinainte de rulări. Se poate deci corecta pe loc, cu copia veche păstrată.

*Propunere: A.* Comparator strict (structură, tipuri, valori finite) și rerularea tuturor analizelor pe o copie proaspătă.

**A02: `verify_hash_lists.py` sare liniile malformate.**
*Verdict: adevărată (robustețe), fără efect prezent.*

- La `:40`, `if not m: continue` sare orice linie care nu se potrivește.
- În cele 9 liste există 87 de linii cu amprentă de 64 de caractere hex, adică exact cele 87 de intrări recunoscute. Cele 21 de linii nepotrivite sunt toate ore sau comentarii, fără nicio amprentă (`a_checks.log`). Deci nu s-a sărit nimic.
- O listă lipsă nu ar fi detectată, dar listele sunt acoperite de `SHA256SUMS.txt`.
- Intrările „authors” (17) sunt doar clasificate; octeții lor îi verifică `prepare_forever_copy.py` (refăcut identic pe 10 nov.). Intrarea „external” (1) și cele 3 „lost” nu pot fi verificate. Antetul scriptului spune asta, dar raportul §7 (r. 196) și README/INDEX („checks every entry”) spun mai mult decât face scriptul.

*Propunere: A.*
- În script: eroare pentru orice linie cu amprentă hex care nu se potrivește; inventarul așteptat al celor 9 liste; numărători separate.
- În texte: „classifies every entry and verifies the bytes of 66 (55 current, 11 earlier versions); the authors' 17 are checked by `prepare_forever_copy.py`; 1 external and 3 lost cannot be checked”.

**A03: codul de ieșire.**
*Verdict: adevărată, minoră.* `main()` se termină fără `sys.exit`. Un nume de verificare necunoscut dă „0 of 0”.

*Propunere: A.* Ieșire 1 la orice eșec sau nume necunoscut.

**Nota Codex despre tech-G2** (în text, fără ID): „22 reproduse” include `g2_preview.py`, fără comparație automată.
*Verdict: deja tratată.* README (r. 95–96) spune că analiza nu a stocat ieșire. Am rulat-o azi: toate celulele tabelului 1 din raport corespund:
- D1: 0,984/0,992 OLS și 0,981/0,991 GBDT;
- ΔN singur: −0,06…0,33;
- ΔN + Ση‖m̂‖: 0,935 / 0,919 / 0,987 / 0,846;
- CV: 0,37–0,73.

Observație proprie: în consola Windows (cp1252), `python -I g2_preview.py` cade la al doilea tabel (`UnicodeEncodeError`, „Δ”). Prin `reproduce_analyses.py`, care rulează cu `-X utf8`, merge.

*Propunere: A.* În README, „21 compared automatically; tech-G2 printed and checked by hand against table 1 of the report (12 Nov)” și comanda cu `-X utf8`. Scriptul nu se modifică.

### C: rezultatele și interpretarea

**C01: „forgetting targets were never opened”.**
*Verdict: adevărată.* Gravitatea: moderată; nefatală.

- `tech4_analysis.py:2–3, 15–26` citește F_A, dAcc_A și F_A_clip și tipărește viteza uitării pe ΔN, pe familie (`runs/tech4_analysis.log:1–20`). Măsurătoarea e permisă de `tech4_criterii.md` (măsura 2), care interzice doar relația c_e–T1.
- Raportul spune fals, în trei locuri: r. 27 („the forgetting targets were never opened”), r. 67 („The forgetting columns … (T1) were never opened”) și r. 177 („because the forgetting targets were never opened”).
- Afirmația adevărată e mai îngustă: nicio relație între un candidat și uitare nu a fost calculată niciodată, H1 nu a rulat, iar analizele G2 elimină F_A, F_B și dAcc_A la încărcare.
- Perspective nu are această afirmație.

*Propunere: A.* Reformulare în cele trei locuri, de exemplu: „no relation between any candidate and forgetting was ever computed (the forgetting columns were read only descriptively, for the speed of forgetting in tech4, as its criteria allowed)”.

**C02** = B02, partea din raport. Aceeași propunere.

**C03: „compute τ exactly”.**
*Verdict: parțial adevărată.* Identitatea e corectă (o confirmă și Codex; verificată pe 10 nov. în `torch/optim/adam.py`). Formularea are însă două probleme:
- „exactly” se bate cap în cap cu „up to floating-point rounding”, din aceeași frază (r. 173);
- „τ determined by the state” trebuie condiționat de pașii executați: la un pas sărit de GradScaler, formula aplicată momentelor vechi nu dă zero, deci trebuie știut că pasul a fost sărit.

*Propunere: A.* „The copy is not needed to compute τ either” și „for every step the optimizer actually executes (a step skipped by the GradScaler changes neither the parameters nor the state and counts as zero, as the GradScaler records)”.

**C04: „three pairs of runs”.**
*Verdict: parțial adevărată (formulare).*

- Sunt patru rulări și trei comparații: R1–R2, A1 și B1. Fiecare rulare intră în două comparații (`rep_verdict.py`; tabelul de la r. 139–144). Corpul raportului explică designul.
- Formularea poate sugera trei replicări independente: rezumat (r. 20), r. 177, nota 7 (r. 217) și README (r. 20).

*Propunere: A.* „three comparisons among four runs (one original pair and two from shared starting points)” în rezumat și README; „in all three comparisons” la r. 177 și r. 217.

**C05: zgomotul de evaluare zero, fără configurație.**
*Verdict: parțial adevărată.*

- Măsurat (`forever_eval_noise_posthoc.json`): originalul și cele două evaluări cu sămânță sunt identice.
- Mecanismul l-am verificat în `transformers` 4.57 (`generation/logits_process.py`). TopK, cu top_k = 1, păstrează toate tokenurile egale cu maximul. TopP, cu top_p = 0, păstrează exact unul (`min_tokens_to_keep = 1`). Eșantionarea are deci un singur candidat, iar sămânța nu contează. „Needs no seed” e corect pentru această implementare.
- Care dintre două logituri exact egale câștigă depinde de implementarea sortării; acestea sunt cele 46 de egalități.
- Lipsește calificarea configurației, la r. 148, 203 și 216.

*Propunere: A.* La r. 203 și 216: „with these library versions (transformers 4.57, torch 2.8) on this GPU; which of two exactly equal logits is kept depends on the implementation”.

### D: Perspective (din auditul pachetului)

**D01: „no information … that the test could detect”.**
*Verdict: adevărată.* Gravitatea: majoră ca formulare; **nefatală**.

- Perspective §5, p. 11 (`persp_content.js:84`) spune: „it carries no information beyond them that the test could detect”.
- Contraexemplul Codex e corect (`check_d.py`): y = x + 0,1z are R² = 0,990 față de x, dar restul determină complet ținta z. Am verificat aritmetica.
- Fraza contrazice raportul §6 (r. 177: „G2 is an operational threshold … not a proof”) și chiar Perspective §6, p. 14 („the remainder it leaves untested could still matter”).
- Formularea e nouă în v1.4; lipsește din v1.3.
- Nu se schimbă niciun număr, niciun verdict și nici eticheta „not identifiable”, doar justificarea.

*Propunere: A.* Înlocuire cu: „the test then stops before the comparison, by that rule: the remainder is not tested, and could still carry information.”

**D02: atomicitatea contorului.**
*Verdict: parțial adevărată; în mare parte deja tratată.*

- Paragraful dinaintea schiței (p. 8) cere deja: „commits must be crash-consistent, so that a crash between incrementing the counter and saving the state is not mistaken for a restoration [61]”. Lista de presupuneri include „crash-consistent commits”.
- Lipsește doar ca pasul (2) al schiței să includă incrementul contorului; acum numește doar „the state and its seal”.

*Propunere: A.* Pasul (2): „The counter increment, the state and its seal form one crash-consistent commit [47, 61], so that a crash leaves either the old values or the new ones.” Plus „a forgery” → „a forgery or a corruption” (vezi P04).

**D03: steagul și dovezile brute pe aceeași cale.**
*Verdict: parțial adevărată.*

- P. 12: monitorul local „shares the root of trust and the readout path of raw agent-bound evidence”. Apoi se cer regimuri cu steagul „delayed, incomplete, or absent, as on a disconnected device or under an orchestrator that withholds it”.
- Pentru un monitor local pe aceeași cale, deconectarea nu elimină steagul, iar un orchestrator care l-ar putea reține ar avea acces la aceeași cale. Regimurile cer deci o arhitectură în care steagul trece pe altă cale (platformă, verificator la distanță, livrare prin orchestrator). Textul nu o spune: inconsecvență locală.
- Partea a doua (un steag binar pierde informație; competitorul ar trebui să fie un rezumat autentificat bogat) e parțial tratată. §1 spune că (b) e cel mai puternic competitor al lui (c). Nivelul 5 are deja ca competitori „freshness metadata” și „authenticated agent telemetry [20]”. Totuși, la p. 12 întrebarea rămasă e pusă doar față de „a binary flag”.

*Propunere: A.* (1) O propoziție: regimurile acestea privesc un steag livrat prin platformă sau calculat la distanță; unde steagul și citirile brute împart calea monitorului, aceeași defecțiune se aplică ambelor. (2) „beyond a binary flag” → „beyond a binary flag or an authenticated summary of the same readings”. Contractul complet al Nivelului 4: **N**.

**D04: locurile goale (DOI, data).**
*Verdict: deja tratată (cunoscută).* Planificate pentru publicare (predarea din 10 nov., „Rămân pentru publicare”). Nicio acțiune acum.

## 2. Recenzia Perspective v1.4 (PERSPECTIVE_REVIEW.md)

Recomandarea Codex: „major revision”, fără nicio obiecție fatală. **Confirmat: nicio eroare fatală.**

Din cele 23 de constatări:
- **8 corecturi locale de logică sau de fapt sunt confirmate**: P07, P08, P09, P12, P13, P14, P18 și precizările din P04/P05;
- **mai multe sunt parțial adevărate** sau tratate deja în corpul textului;
- **P02 nu se susține**;
- **P10 (parțial), P11, P21, P22 și P23 țin de cadru, de contract sau de editare** și merg la v1.5.

Multe formulări criticate există deja în v1.3 (publicată) și au trecut de rundele anterioare: „costly and valid”, „Restoring behaviour therefore requires”, „only if the restored state carries”, „a forgery”, „Today a self-model reads”, „beyond a binary flag”, „as on a disconnected device”, „decoding ceiling”. Noi în v1.4 sunt doar D01/P09 și P20.

| ID | Verdict | Dovada | Propunere |
|---|---|---|---|
| **P01** raw față de adjudecat, fără avantaj demonstrat | *parțial adevărată* | Lucrarea nu pretinde un avantaj demonstrat: e o ipoteză condiționată. §1 spune că „(b) is also the strongest competitor of (c)”, iar §2 numește separarea funcțională drept rezultat posibil. Miezul valid e cel din D03: la p. 12, întrebarea e pusă doar față de un steag binar. | **A** prin D03 (2). Reîncadrarea noutății ca „comparison of evidence representations”: **N** |
| **P02** „needs … a time of its own … irreversible” | *falsă ca obiecție, deja tratată* | P. 4 o prezintă explicit ca „the motivating intuition”, urmată de „the hypothesis of §2 is the testable form of the intuition”. §3 o califică („true but proves too much”), iar p. 7 definește ireversibilitatea relativ la checkpoint și la modelul de amenințare. | — |
| **P03** „only if” din propoziție | *parțial adevărată* | Contraexemplul Codex (o notificare a monitorului despre o restaurare) e acoperit de a doua ramură: un monitor nu poate raporta o restaurare la o stare *anterioară* decât dacă ține evidența celei mai recente („or the source holds one to the latest state”). Însă cerințele de autentificare și încredere din „only if” nu decurg din egalitatea stărilor: sub A (erori accidentale), o înregistrare neautentificată în afara checkpoint-ului ajunge. Formularea e din v1.3. | **A?** (atinge propoziția centrală): „and, against an adversary who controls the state and its inputs (threat model B), only if …” |
| **P04** atomicitatea; „forgery” | *parțial adevărată* | = D02. Sub A, o nepotrivire a sigiliului poate fi și o corupere. | **A** (ca la D02) |
| **P05** rezumatele promit mai mult decât cazurile observabile | *parțial adevărată* | Corpul e corect (p. 8: „suspended, or ran without committing a step”; bifurcările doar la contenția pe contor; clonele nedetectabile de original). Rezumatul („distinguishes suspension from restoration”) și lista de la p. 2 comprimă. „Once one branch commits, the other finds N ahead” presupune o verificare a predecesorului la commit, pe care pasul (1) nu o spune: fără ea, a doua ramură ar putea face commit la N+1. | **A**: rezumatul și lista: „distinguishes restoration from an interval without committed steps, such as a suspension”; pasul (1): „the monitor accepts a commit only from the state that carries the latest seal” |
| **P06** indexul la restaurare | *parțial adevărată (lacună de definiție)* | P. 9: „maintained as one running number”, fără să spună unde e ținut. P. 10 îl presupune restaurabil („a restored agent fed synthetic experience … can show normal change while only the anchor reveals the restoration”). | **A?** (alegere de definiție a autorului): „The index is kept in the agent's restorable state and restored with it; it is defined along one lineage, and a rate is read only over intervals that the anchor shows to contain no restoration.” Altfel **N** |
| **P07** „costly and valid”; raportul deplasare/drum | *adevărată, minoră* | Costul nu e validitate; textul spune chiar că „costly candidates” rămân deschise (p. 9). Raportul ≤ 1 cere ca D să fie metrică (inegalitatea triunghiului). Formularea e din v1.3. | **A**: „from cheap and weak to costly and more direct, none yet validated”; „(for a metric D)” |
| **P08** VDF ca competitor pentru timp scurs | *adevărată (inconsecvență internă)* | Tabelul 2, Nivelul 1, are „a verifiable delay function where it does not”, deși Tabelul 1 și p. 10 spun că VDF certifică lucru secvențial, nu timp scurs. | **A**: „…, which bounds elapsed time from below only while it runs and only under an assumed maximum evaluation speed” |
| **P09** R² mare ⇒ „no detectable information” | *adevărată* | = D01. Contraexemplul cu rată pozitivă (R² 0,95; restul prezice ținta exact) e corect. | **A** (ca la D01) |
| **P10** lacune de contract (N2, N3, N4, N6) | *parțial adevărată* | Lucrarea spune explicit că nu dă contracte (p. 11: „No such contract is provided here”). N4: = D03. N2: „predictive validity per unit of storage” e nedefinit la stocare suplimentară zero. N3: „recomputation” nu cere calitate egală. N6: competitorul nu primește aceeași telemetrie și proveniență. | N4: **A** (D03). N2: **A?** („predictive validity, with storage among the declared costs”). N3 și N6: **N** (contracte) |
| **P11** „decoding ceiling”, „one half” | *parțial adevărată, în esență tratată* | Textul spune „it estimates what the evidence supports” și nu pretinde o limită superioară, deși numele sugerează una. Termenul vine din studiul publicat [25]. „One half” e dat ca „prespecified fraction — one half in the accompanying study”. | **N** (termenul, ratele necondiționate de pornire) |
| **P12** rutarea epistemică nu restaurează comportamentul | *parțial adevărată* | P. 15 spune deja „Privilege separation does not, however, make behaviour restorable by itself”. Fraza următoare cere însă ca dovada să intre „only epistemic functions … or virtualise”. Rutarea epistemică nu restaurează comportamentul exact: invalidarea cache-ului și re-verificarea sunt acțiuni (exemplul Nivelului 5). Formularea e din v1.3. | **A**: „Routing it only into epistemic functions … limits its effect on behaviour but does not remove it, since re-verifying a fact is itself an action; restoring behaviour exactly requires that the platform virtualise …” |
| **P13** index cumulat față de rată | *adevărată, minoră* | P. 14: „the accumulated norm of parameter change was reconstructed … R² 0.94–0.96”. Ținta e rata lui τ în ferestre de 8 pași (raportul, r. 100; `lm_forever_g2.py`). Mediile recalculate de Codex (0,944–0,958; 0,956–0,971) corespund. | **A**: „the rate of the accumulated norm …, in 8-step windows, … the norm of the bias-corrected first moment” |
| **P14** „did no better” | *parțial adevărată* | În port: echivalență preînregistrată (IC pereche în margini). În codul autorilor: marjă descriptivă ±2, o rulare pe celulă, OP τ − Ση‖m̂‖ = +0,84 / −0,67 / +1,03 (τ înainte în 2 din 3). „Did no better” e puțin prea tare. P. 11: comparația secundară „is reported by the rule above”, dar regula completă (non-inferioritate și costuri declarate) nu a fost aplicată; timpul de rulare nu a fost măsurat (raportul §5.3). | **A**: rezumatul: „showed no demonstrated advantage over a free one”; §4: „and in aggregate, within a descriptive two-point margin, with the original code (one run per cell; the effect on single tasks unresolved)”; §5: „is reported under the margins fixed for it” |
| **P15** „before its runs” fără „local” | *parțial adevărată* | Faptul e corect: G2 și „not identifiable” apar deja în protocolul v0.1 (27 oct., `Versiuni_anterioare\`: 3 apariții fiecare) și în v0.4 (§11, r. 401; §15, r. 509), înainte de primele rulări (4 nov.). Lipsește „local” (amprente, fără depozit public; raportul §3 și §7). | **A**: „…in its own protocol, recorded locally before its runs” |
| **P16** „free” | *parțial adevărată* | Momentul e ținut de optimizator; norma lui cere o trecere peste tensor (`make_clock_variant.py:19–23`). Memorie în plus: niciuna (raportul §5.3). Calcul: nenul, nemăsurat. Auditul vocabularului din 10 nov. a păstrat „free optimizer telemetry”. | **A?**: o definiție, o singură dată, în §4: „free here meaning that it needs no state beyond the optimizer's own; computing its norm still takes one pass over that state” |
| **P17** excepția prin extrapolare | *parțial adevărată* | Corect sub G2 așa cum e definită (cross-fitting în familie). Utilitatea unui index calculat direct la transfer e o altă întrebare, netestată. | **A?**: „…only if it persists there; whether a directly computed index serves better than its learned substitute under such a shift is a separate question, not tested” |
| **P18** „The pair is what state-continuity protocols already maintain” | *adevărată* | ROTE [36], NARRATOR [40], Memoir [47] și Ariadne [61] păstrează prospețimea prin contoare monotone și versiuni de stare. Niciunul nu ține o referință de timp scurs c_a. Formularea e din v1.3. | **A**: „The counter is what state-continuity protocols already maintain for data [36, 40, 47, 61]; binding it to a time reference is the arrangement considered here.” |
| **P19** „today” fără sondaj | *parțial adevărată* | „Read by the self-model today” (Tabelul 1), „Today a self-model reads…” (p. 6), „not the agent's model of itself” (p. 15): plauzibile pentru designurile obișnuite, dar nesusținute de un sondaj. | **N** (eventual „in conventional designs” la p. 6) |
| **P20** „had pointed the same way” | *parțial adevărată* | Formularea e nouă în v1.4. Are o bază: în Pilot 1, semnalul era purtat de statistici locale ale actualizărilor (raportul §2, r. 47; Perspective §6). „The same way” e însă vag. | **A**: „had found a related pattern: its signal was carried by local update statistics” |
| **P21** istoricul versiunilor, rezumatul lung | *judecată editorială* | Istoricul e o alegere deliberată de transparență; depinde de revistă. | **N** |
| **P22** „dual clock”, „continuity”, „gate” | *schimbare de cadru* | Redenumirea „dual clock” e deja notată pentru v1.5 (Copilot, 9 nov.). | **N** |
| **P23** așezarea tabelelor, ultima pagină | *editorială* | Fără tăieri de conținut; fără defect științific. | **N** |

**Referințe** (Codex, punctul 4):
- [5] TriHaRd e acum publicată: Crossref, verificat azi, IEEE INFOCOM 2026, pp. 1–10, DOI 10.1109/INFOCOM59046.2026.11571700, 18 mai 2026. *Propunere: A*, referința actualizată.
- [20] (arXiv:2608.16178) și [21] (arXiv:2610.00132): verificate azi pe arXiv, titlurile corespund.
- [54] (DataCite, v2.0.0): corespunde.
- Codex nu le-a putut accesa; nu e niciun semn de eroare.

**Fără ID:**
- „The hypothesis is unchanged” (caseta Changes): caseta enumeră deja schimbările. **N**.
- Contractul complet propus de Codex pentru Nivelul 5: **N**, ca material pentru primul contract.

## 3. Lista corecturilor propuse (așteaptă acordul)

**Erori fatale confirmate: niciuna.** Publicarea nu e oprită de o eroare fatală; după regulă, ea așteaptă totuși aplicarea corecturilor adoptate.

**Raportul de închidere** (`Pilot2_closure_report_draft_v0.1.md`):
- R-a (C01): „never opened” → reformulat la r. 27, 67 și 177.
- R-b (B02/C02): eticheta „in-sample” la r. 29 și r. 104, plus valorile cu sarcina lăsată deoparte (post hoc).
- R-c (B01): sursa tabelului 1 (r. 92) spune că B_strong conține C6, înlăturate în T-D (1).
- R-d (B03, B04): în §4, la SuperNI, bugetul real de pași (2,96 epoci), plafonul de 256 de tokeni care nu a tăiat nimic și proporțiile intrărilor tăiate.
- R-e (C03): fraza „exactly” din §5.3.
- R-f (C04): „three pairs of runs” → „three comparisons among four runs” (rezumat, r. 177, nota 7).
- R-g (C05): calificarea configurației la r. 203 și r. 216.
- R-h (A02): §7, r. 196: ce verifică efectiv `verify_hash_lists.py`.
- R-i: §10: numărul analizelor (22 sau 23) și data reproducerii, după rerulare.

**README și INDEX:** C04 (r. 20), A02 („checks every entry”), A01–A03 (instrumentele corectate după audit), nota despre tech-G2 (`-X utf8`), plus analiza post hoc nouă, dacă e aleasă.

**Scripturi** (niciunul dintre ele nu e amprentat înainte de rulări; copiile vechi merg în `_work\_copii_siguranta\`):
- `reproduce_analyses.py`: comparator strict (A01) și cod de ieșire (A03);
- `verify_hash_lists.py`: sintaxă, inventar și numărători separate (A02);
- nou, recomandat (B02): `forever_repro/r2_heldout_task_posthoc.py` + `runs/forever_r2_heldout_task_posthoc.log`, declarat post hoc, adăugat în verificarea de reproducere.

Scripturile amprentate (`lm_superni_run.py`, `g2_preview.py` și celelalte) **nu se ating**.

**Perspective v1.4** (`_work\persp_content.js`, `refs_persp.js`):
- *de adoptat:* D01/P09, D02/P04, D03 (+P01, P10 N4), P05, P07, P08, P12, P13, P14, P15, P18, P20, referința [5];
- *la alegerea autorului:* P03, P06, P10 (N2), P16, P17.

**Pentru v1.5 (N):** P10 (N3, N6), P11, P19, P21, P22, P23, contractul Nivelului 4/5 și reîncadrarea noutății (P01).

**Arhiva:** folderul `Recenzii\Audit_Codex_2026-11-10\` (răspunsurile, regula și această verificare) intră la reconstrucție în anexa `Recenzii/`, ca runda finală. Recomand să rămână, cu o secțiune în `Recenzii\README.md`. Scanarea de confidențialitate: nicio cale cu numele de utilizator; apare doar `D:\Pilot2_audit`.

**După acord (ordinea):**
1. corecturile;
2. scriptul post hoc nou, dacă e ales;
3. reproducerea completă pe o copie proaspătă, cu comparatorul strict;
4. indexul, copia publică, SHA256SUMS și `verify_hash_lists`;
5. PDF-urile raportului și Perspective;
6. depozitul local, fără commit;
7. `D:\Pilot 2`;
8. auditul final al vocabularului.

Fără Zenodo, fără commit, fără push.

## 4. Aplicare (12 nov. 2026, după acordul autorului)

**Acordul:** „doar cele validate de tine în urma verificării auditului”. Am aplicat deci doar punctele marcate **A**. Pentru B02 am ales varianta recomandată (scriptul post hoc). Punctele **A?** (P03, P06, P10 N2, P16, P17) și **N** nu sunt aplicate.

**Copii de siguranță:** `_work\_copii_siguranta\inainte_audit_Codex_2026-11-12\`, cu cele 16 fișiere modificate și amprentele celor 9 liste de dinainte de rulări (neatinse). Construcția publică înlocuită e în `_work\_copii_siguranta\pilot2_repo_build_inlocuit_audit_Codex_2026-11-12\`. Scripturile de aplicare sunt în `_work\audit_codex_2026-11-12\`; fiecare text vechi a trebuit să apară exact o dată.

**Ce s-a schimbat:**
- **Raportul** (20 de înlocuiri, `apply_report.py`): C01 (3 locuri), B02/C02 (eticheta „in-sample” și valorile cu sarcina lăsată deoparte), B01, B03/B04, C03, C04 (4 locuri), C05 (2 locuri), A02 și §7 (lista post hoc). În plus: un rând nou în tabelul din §3 (auditul, 10–12 nov.) și o notă în antetul-comentariu.
- **README și INDEX** (`apply_readme_index.py`): C04, A02, numărul analizelor (23), analiza nouă, nota despre tech-G2 (`-X utf8`) și un rând nou în harta testelor.
- **`Recenzii\README.md`:** secțiunea despre audit, în engleză și română.
- **Scripturi de arhivă**, neamprentate înainte de rulări:
  - `reproduce_analyses.py`: comparator strict (A01), cod de ieșire 1 la orice eșec sau nume necunoscut (A03) și verificarea nouă. Testat pe cazurile din A01: NaN, containere goale, tipuri, lungimi.
  - `verify_hash_lists.py`: liniile malformate cu amprentă sunt eroare, inventarul de 9 liste și 87 de intrări e verificat, iar rezumatul arată „verified 66 / authors 17 / external 1 / lost 3” (A02). Pe o fixtură cu o listă lipsă și o linie malformată dă codul 1.
- **Analiza post hoc nouă:** `Stadiul0/forever_repro/r2_heldout_task_posthoc.py` → `runs/forever_r2_heldout_task_posthoc.log`, adăugată în reproducere (23 de analize). Valorile sunt identice cu verificarea din §1.
- **Indexul:** reguli noi în `_work\build_pilot2_index.py` (E7 scriptul, E8 jurnalul).
- **Perspective v1.4** (22 de înlocuiri în `persp_content.js`, 1 în `refs_persp.js`, `apply_perspective.py`): D01/P09, D02/P04, D03 (+ P01, P10 N4), P05 (rezumatul, lista de la p. 2, pasul (1)), P07, P08, P12, P13, P14 (rezumatul, §4, §5), P15, P18, P20 și referința [5] (TriHaRd publicată).
  - Pe lângă listă, în declarația AI (regula permanentă: evaluatorii AI se numesc), am adăugat: „its final text was revised after AI reviews of its draft and after an independent audit in OpenAI Codex (GPT-6 Astra), documented in the archive of that study”.
  - DOCX și PDF reconstruite: 75 de referințe, toate citate. Toate formulările noi sunt prezente în textul PDF, iar cele vechi lipsesc. Paginile 8 și 12 au fost verificate vizual; Tabelul 2 încape acum întreg pe p. 12.
  - PDF-ul are 21 de pagini (înainte 20). Ultimele 6 rânduri ale declarațiilor trec pe p. 17, pentru că bibliografia începe pe pagină nouă.

**Neschimbate:** fișierele amprentate dinainte de rulări (cele 9 liste au aceleași amprente), toate rezultatele stocate și partea de date (`pilot2_data_2026-11-10.zip`: 730 de intrări cu aceleași CRC și dimensiuni ca o construcție nouă).

**Reproducerea pe o copie proaspătă** (`_work\zenodo_pilot2\repro_check_v7_2026-11-12.txt`; copia `_work\_test_arhiva_pilot2_v7_2026-11-12`):
- `SHA256SUMS` OK înainte și după;
- `prepare_forever_copy` refăcut identic: 11 fișiere de cod și 12 de date;
- `verify_hash_lists` fără nepotrivire: 55 ok, 11 earlier, 17 authors, 1 external, 3 lost; 66 verificate, cod de ieșire 0;
- **23 din 23 de analize reproduc**, cu comparatorul strict, cod de ieșire 0, în 3 min 27 s.

După rulare s-au schimbat doar propoziția despre reproducere (README, raportul §10) și acest document. Copia publică a fost reconstruită; față de copia testată diferă doar în fișiere care nu sunt analize.

**Auditul vocabularului** (`vocab_audit.py`), în raport (R) și Perspective (P):
- 0 apariții în ambele pentru formulările interzise pe 10 nov. și pentru cele corectate acum: „never opened”, „three pairs”, „did no better”, „that the test could detect”, „pointed the same way”, „compute τ exactly”, „The pair is what”, „deterministic in practice”.
- „costly and valid”: 0 în P; 1 în R, unde e un citat explicit din v1.3 (§1, între ghilimele).
- „free optimizer telemetry”: 0 în R; 3 în P, toate cu „or … of the same cost” (neschimbat, P16 neaplicat).
- „artefact”: 0 în R; 1 în P (avertismentul despre Pilot 1).
- „not identifiable / unidentifiable”: 6 în R, același număr ca înainte de corecturi.
- „closed / closure” în R: doar titlul și „the closure rests on identifiability”.

**Observație proprie, aplicată separat** (acordul autorului din 12 nov.: „Da, redactează”):
- `Stadiul0/runs/lmsens_a32_g2.log` (12 apariții) și `lmtech1_g2.log` (11) conțineau, în avertismentele Python stocate, calea locală cu numele de utilizator. Erau și în copia publică din 10 nov.; Codex nu le-a semnalat, iar scanarea de confidențialitate nu căuta astfel de căi.
- Sunt singurele fișiere din `02_Pilot2` cu această cale; partea de date nu are niciuna.
- Nu sunt în listele de amprente. În copia publică, prefixul devine `<Python 3.14>`; originalele rămân neschimbate (regula REDACT din `_work\build_pilot2_archive.py`, cu numărul exact de apariții).
- Scanarea de confidențialitate caută acum și dosarele de utilizator din căi.
- Redactarea e declarată în README. `reproduce_analyses.py` ignoră liniile de avertisment, deci comparația nu e afectată.
- Reverificat pe o copie proaspătă v8 (`_work\zenodo_pilot2\repro_check_v8_2026-11-12.txt`): SHA256SUMS OK înainte și după, codul autorilor identic, `verify_hash_lists` fără nepotrivire, **23 din 23 reproduc** (inclusiv LM-tau-lmtech1 și LM-tau-a32, pe jurnalele redactate), cod de ieșire 0. După rulare s-a schimbat doar acest document.
