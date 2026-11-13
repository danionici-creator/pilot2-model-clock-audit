# Colocviul Pilot 2: verificarea punct cu punct a răspunsurilor (6 nov. 2026, seara)

Pasul 2 din `Regula_de_decizie.md`. Verificat de Claude (autorul analizelor, fără vot): cifrele cu dosarul și jurnalele (`runs/*.log`), afirmațiile despre cod cu codul (`p2/`, `lm/`), referințele prin arXiv API (6 nov., 21:46) și, pentru FOREVER, în textul HTML arXiv v2. Verdicte: **întemeiat / parțial / fals / neverificabil / opinie**.

**Martor fără vot (hotărât înainte de trimitere, 6 nov., ~22:05):** DeepSeek primește același PDF și prompt; se verifică la fel, dar nu intră în nicio numărătoare (direcție, decizii 1–8, testele „propuse de ≥ 2”).

**Stare:** toate 5 răspunsurile verificate (plus martorul DeepSeek). Rezultatul final: §10.

## 0. Erori și omisiuni ale DOSARULUI, scoase la iveală de răspunsuri (le notez aici; dosarul trimis rămâne neschimbat, cu amprenta din `SHA256SUMS_2026-11-06.txt`)

| # | Ce | Verificare | Efect |
|---|---|---|---|
| E1 | B_strong din R1 (tech2/tech3, `g2_preview.py`) și R2 (`g2_cpu_checks.py`) conține statisticile C6: media și abaterea **chiar a lui D1 pe pas** (`C6_post_*`, din `st["D1"]`) și a normei pasului Adam (`C6_pre_*`, `dpre_norm`) pe primii și ultimii 16 pași ai intervalului. Dosarul (§1) spunea doar „local update statistics”. | cod: `p2/triplets.py` r. 106–109; `g2_preview.py` r. 24–26 | Coloanele „B_strong, OLS/GBDT” din R1 și „OLS/GBDT pe B_strong” din R2 sunt **parțial circulare** pentru D1 (și aproape-duplicat pentru D1_rel, D2). **Nu sunt afectate:** coloanele cu un singur scalar (ΔN + Ση‖m̂‖), R3 (`tech4_analysis.py`: „GBDT, all” folosește doar ratele C2–C10c, fără C6) și brațul LM (GBDT pe η, ‖g‖, ‖m̂‖, √Tr v̂, pierdere etc., fără Δθ). Semnalat de ChatGPT (auditul de proveniență); Gemini și Mistral, pe altă cale (identitatea Adam). |
| E2 | Fraza din R3 „F6 is the only family where no cheap scalar reconstructs the functional clock D3” e corectă pentru D3, dar dosarul și promptul (Q1) tratează D1_rel ca reconstruit. În tech4, **niciun scalar ieftin nu reconstruiește D1_rel peste 0,90 în nicio familie** (ΔN + Ση‖m̂‖: 0,67 / 0,87 / 0,79 / 0,82 în F2 / F3 / F5 / F6; ΔN + C10c: 0,73 / 0,79 / 0,75 / −0,26); doar GBDT trece de 0,90 în F2 / F3 / F5 (0,94 / 0,99 / 0,95), dar **nu în F6 (0,79)**. | `runs/tech4_analysis.log` | D1_rel/F6 e o a doua excepție, nu doar D3/F6. Semnalat de ChatGPT (și de Copilot: încredere „medium for D1_rel”). |
| E3 | Lipsea din dosar: articolul FOREVER raportează el însuși **nicio corelație semnificativă** între τ_day și uitarea finală BWT pe sarcini (r = 0,2182, p = 0,4536; în aceeași anexă: τ_day stabil între ordinile de sarcini, r = 0,7379). | arXiv:2601.03938v2, HTML, citit 6 nov. | Relevant pentru Q4 și pentru nota FOREVER. Semnalat de ChatGPT. |

## 1. Referințe (toate cele citate în cele 4 răspunsuri)

| ID | Titlul (arXiv API) | Citat de | Verdict |
|---|---|---|---|
| arXiv:2601.03938 | FOREVER: Forgetting Curve-Inspired Memory Replay for Language Model Continual Learning (Feng, Wang, Li, …) | toți | întemeiat |
| arXiv:2305.17212 | Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks (Kosson, Messmer, Jaggi) | Gemini, Copilot, Mistral (din dosar) | întemeiat |
| arXiv:2502.16982 | Muon is Scalable for LLM Training (Liu, Su, Yao, …) | Gemini, Copilot, Mistral (din dosar) | întemeiat |
| arXiv:1412.6980 | Adam: A Method for Stochastic Optimization (Kingma, Ba) | Mistral | întemeiat |

Nicio referință inventată. ChatGPT a citit FOREVER v2 și pagina depozitului (spune singur că nu a putut verifica commit-ul `bbeb549`).

## 2. Gemini 3.1 Pro (High): direcția C

| Afirmație | Verdict | Sursa |
|---|---|---|
| ΔN + Ση‖m̂‖ reconstruiește D1 la 0,94 | întemeiat | R1 |
| Pasul AdamW ≈ η‖m̂‖/√v (mecanism) | parțial: elementwise, plus weight decay și tăiere; nu e „strict” | cod `p2/agent.py` |
| „rata e practic constantă în fazele staționare; o țintă aproape constantă dă trivial R² mare” | **fals**: CV al ratei 0,37–0,73 (R1); ΔN singur dă R² ≈ 0; R² măsoară varianța explicată, o țintă constantă nu dă R² mare | R1 |
| C10c e media *algebrică* a schimbărilor de pierdere, deci se anulează sub zgomot; testul propus „C10c_abs” | **fals**: C10c este deja media valorilor **absolute** (dosarul R3: „mean over items of \|change of the per-item loss\|”; codul: `(ceR - prev).abs().mean()`) | `p2/run.py` r. 283–287 |
| „C10c eșuează sever (R² −0,95 față de GBDT 0,99)” în F6 pentru D3 | **fals**: −0,95 și 0,99 sunt valorile lui **D2** în F6; pentru D3 în F6: C10c 0,59, GBDT 0,81 | R3 |
| La nivel de fază, Ση explică τ la 0,975–0,991, deci τ e dictat de programul ratei | **parțial / înșelător**: cifra e corectă, dar dosarul spune explicit că e un artefact al duratei (pașii singuri dau la fel; rata pe fază: 0,09–0,18); predicția „Ση explică τ” a picat (0,67) | R5, R7 |
| τ e „un numărător de pași ponderat cu rata, ascuns” | **fals** în forma asta: Ση explică doar 0,58–0,69; e nevoie de ‖m̂‖ (0,94–0,96) | R5, R6, R9 |
| Perspective „presupune că agentul deține dovezi nefalsificabile ale propriei schimbări” | **fals** (inversat): dosarul §1: agentul „holds **no** unforgeable evidence” | dosar §1 |
| „R² 0,94–0,99 pentru D1, D1_rel, D2” | parțial: D1_rel doar cu GBDT; scalarul ieftin 0,67–0,87 | R3 |
| Testul 2: „4,5 h (3 rulări × 1,5 h)” | **fals**: ~15 min pe rulare LM | dosar §5 |
| Lipsa de control: G2 pe date naturale (SuperNI) | opinie, fezabilă parțial pe laptop | — |

**Recomandarea de direcție C:** argumentul principal (ceasurile din parametri pică G2; coliniaritate cu telemetria) e **întemeiat** pentru D1, D2, τ. **Rămâne.** **Se elimină:** testul decisiv 1 (C10c_abs: premisă falsă) și concluziile Q3 și Q5 bazate pe afirmațiile false. Testul 2 (planificatorul FOREVER) rămâne, cu costul corectat.

## 3. Copilot (Raționament profund): direcția C

| Afirmație | Verdict | Sursa |
|---|---|---|
| R1: B_strong reconstruiește toate cele patru rate, R² 0,91–0,99; scalarul: D1 0,94, D1_rel 0,92, D2 0,99 | întemeiat (cu E1: B_strong din R1 e parțial circular) | R1 |
| R3: D2 0,98 în F6; D1 0,92–0,95 în F3, F5, F6 și 0,86 în F2; D1_rel cu GBDT 0,94–0,99, F6 0,79; D3: C10c aproape perfect în F2, F3, F5, F6 0,59, GBDT 0,81 | întemeiat | R3 |
| LM: τ 0,94 / 0,95; cu Ση 0,96–0,97; robust la bf16 și α | întemeiat | R5, R6, R9 |
| R2: eroarea 23% / 8%; D3 −21% după reporniri; faza 0,975–0,991 față de rata 0,09–0,18 | întemeiat | R2, R7 |
| C10c = schimbări absolute ale pierderii pe item; D3 = JS pe toată distribuția | întemeiat | cod |
| G2 pică ⇒ H1 neidentificabil (după regula protocolului) | întemeiat ca regulă; „nu e o teoremă” e spus corect de ChatGPT și Mistral | protocol v0.4 |
| Costuri: 32 de rulări ≈ 2,6 h; 32 de rulări LM ≈ 8 h | întemeiat (12,3 rulări/h; 15 min/rulare) | dosar §5 |
| Lipsa de control: un set de audit nou, generat după înghețarea întregii analize | opinie, întemeiată metodologic | — |

Nicio afirmație falsă găsită. Interfața a afișat „A raționat timp de 1 s” (neconcludent despre efort; răspunsul are 17 KB și blocul final complet). **Recomandarea C rămâne.**

## 4. Mistral Large 4 (high): direcția C

| Afirmație | Verdict | Sursa |
|---|---|---|
| Δθ = −η m̂/(√v̂+ε), deci ‖Δθ‖ e o funcție deterministă de (η, m̂, v̂), „toate în B_strong” | **parțial**: B_strong conține **normele** ‖m̂‖ și √Tr v̂, nu vectorii; plus weight decay decuplat și tăiere în lumea sintetică. Mecanismul de ordinul întâi e corect; „funcție deterministă de B_strong” e fals (aceeași greșeală ca pe 4 nov.) | cod |
| R² 0,86–0,99 lasă 1–14% din varianță; „nicio informație” nu e stabilit | întemeiat | R1, R3 |
| C10c reconstruiește D1 la 0,88–0,93 în F2, F3, F5 | întemeiat | R3 |
| R2: 23% / 8%; ferestrele LM de 8 pași față de intervalele sintetice de 64–1.280 | întemeiat | R2, R5 |
| „La pragul 0,95, D1_rel (0,96–0,98) și D2 trec” | **fals** (inversat): R² ≥ prag înseamnă că G2 pică; la 0,95, D1_rel și D2 tot pică; doar D3 ar trece parțial | R1 |
| Logica lui G2: reconstrucția nu implică neidentificabilitatea lui H1 (reziduul poate prezice T1) | întemeiat ca observație metodologică (și ChatGPT, și Copilot o spun) | — |
| C10c și D3 „se corelează 0,98–0,99” în familiile curate | parțial: sunt R² 0,95–0,99, nu corelații | R3 |
| F6: GBDT 0,81, C10c 0,59; o singură sămânță pe familie | întemeiat | R3 |
| T3: analogul C10c din `probes.npz` (cuvânt-răspuns aleator, neantrenat) | întemeiat | cod `lm_forever_run.py` r. 85, 93 |
| R7: echivalența declanșărilor e calculată pe aceleași rulări (aritmetic), nu pe rulări independente ale planificatorului | întemeiat | `lm_forever_posthoc.py` |
| τ „pe fază” | **fals**: τ se resetează pe sarcină, se acumulează peste faze (repetițiile excluse) | `lm_forever_run.py` r. 230 |
| Costuri: 16 rulări ≈ 1,5 h CPU; 20 × 15 min = 5 h GPU; 48 de rulări ≈ 4 h | întemeiat | dosar §5 |
| „Conform departajării fixate, C domină R și B” | parțial: departajarea se aplică doar la egalitate | regula |

**Recomandarea C:** argumentul principal (mecanism + reconstrucție pe date reținute, pe două brațe și trei configurații LM) e întemeiat empiric; partea „funcție deterministă de B_strong” e falsă, dar nu e argumentul principal. **Rămâne.**

## 5. ChatGPT GPT-6 (High): direcția B

| Afirmație | Verdict | Sursa |
|---|---|---|
| Reconstrucția nu arată irelevanța condiționată față de uitare; G2 e o regulă de oprire, nu o teoremă | întemeiat | — |
| Tabelul: D1 GBDT 0,95–0,99 (R3); D1_rel 0,94–0,99 (F2, F3, F5), F6 0,79; D2 0,94–0,99, scalar 0,98–0,99; τ GBDT 0,976–0,994 (R5–R6), R9 0,986–0,988 | întemeiat (0,994 e pe ΔW, nu pe factori; minor) | R3, R5, R6, R9 |
| B_strong poate conține derivate directe ale actualizării (auditul de proveniență) | **întemeiat, confirmat în cod** (E1) | `p2/triplets.py` |
| **D1_rel/F6 e o excepție reală de reconstrucție** | **întemeiat** (E2) | R3 |
| D3/F6: 0,18 / 0,59 / 0,81; GBDT ≈ 0,99 în F2, F3, F5 | întemeiat | R3 |
| C10c = schimbarea absolută a pierderii pe eticheta corectă; D3 = toată distribuția | întemeiat | cod |
| FOREVER: ablația față de pași +1,2 OP, +1,1 BWT; fără comparație cu un ceas din momente sau din program | întemeiat (verificat și pe 4 nov.) | arXiv:2601.03938v2 |
| **FOREVER: τ_day nu se corelează cu BWT (r = 0,2182, p = 0,4536)** | **întemeiat** (E3) | arXiv:2601.03938v2 |
| Factorii LoRA: B→cB, A→A/c lasă BA neschimbat, dar schimbă distanțele pe factori; τ pe factori nu e intrinsec funcției | întemeiat (algebric; brațul LM măsoară și ΔW = 2BA) | — |
| Costuri: 80 de rulări ≈ 6,5 h CPU; 36 × 15 min ≈ 9 h GPU | întemeiat | dosar §5 |
| Nota FOREVER: nu acum | opinie | — |
| A folosit „Personal Context” (memoria contului) | notă de independență, nu afirmație falsă | interfața |

Nicio afirmație falsă găsită. **Recomandarea B rămâne.** Cele două argumente principale (excepția D1_rel/F6 și faptul că D3/F6 nu a trecut un design potrivit) sunt întemeiate.

## 6. Numărătoarea provizorie (4 din 5; Deep Review lipsește)

**Direcția (Q7):** C: Gemini, Copilot, Mistral (3 voturi rămase); B: ChatGPT (1 vot). Cu Deep Review, C are majoritatea indiferent de votul acestuia (3 din 5). **Direcția C e deja decisă**, cu condiția ca niciunul dintre cele trei voturi C să nu cadă la o verificare ulterioară.

**Deciziile 1–8:**

| # | Gemini | Copilot | Mistral | ChatGPT | Provizoriu |
|---|---|---|---|---|---|
| 1 Forma Stadiului A | C | C | altul: fără Stadiul A, doar pachetul D3/F6 + T4 | R | C: 2 strict (Gemini, Copilot); Mistral „altul”, echivalent ca fond cu C; R: 1 |
| 2 Stadiul 0a/0b | da | da | da | da | **da** |
| 3 Stadiul B | amânat | amânat | amânat | amânat | **amânat** |
| 4 Embedding-uri fără wd | complet | complet | complet | complet | **complet** |
| 5 Criteriul LM | înainte | înainte | înainte | înainte | **înainte de repetiția finală** |
| 6 Precizia LM | bf16 | bf16 | bf16 | bf16 | **bf16** |
| 7 C10c obligatoriu | da | da | da | da | **da** |
| 8 Nota FOREVER | acum | acum | acum | după Stadiul A | acum (3) |

**Testele propuse de cel puțin 2 participanți (se preînregistrează primele, după sosirea Deep Review):**

| Test | Propus de | Esența comună |
|---|---|---|
| T-A: planificatorul FOREVER contrafactual (τ, Ση‖m̂‖, doar programul [, pași/fix]) cu uitarea ca rezultat | toți patru (Gemini t2, Copilot t2, Mistral T4, ChatGPT t4) | aceleași semințe și memorie; Copilot și ChatGPT cer bugetul de repetiție egal; ChatGPT cere întâi o separare suficientă a declanșărilor; Mistral: întâi o simulare din tablourile existente |
| T-B: F6 cu zgomotul etichetelor manipulat, semințe noi, D3 contra B_strong + C10c (+ alte rezumate funcționale), apoi creșterea predicției uitării | Copilot t1, Mistral T1+T2, ChatGPT t2 | doze de zgomot 0 / 0,1 / 0,3 / 0,5 (Copilot, Mistral) sau 0 / 0,3 + variante (ChatGPT); prag ΔR² ≥ 0,02 cu interval pe rulări (Copilot, ChatGPT) sau ≥ 0,05 cu permutări (Mistral) |
| T-C: analogul C10c pe brațul LM, din sondele salvate | Mistral T3, ChatGPT t3 | prag 0,90 la ambii; ~0,5 h, fără GPU |
| T-D: auditul reconstrucției pe semințe noi, cu analiza înghețată înainte, pe mai multe scări de fereastră și fără trăsături derivate din Δθ | Copilot t3, ChatGPT t1 (Mistral: lungimea ferestrei, scurgerea între lumi) | prag 0,90 pe fiecare scară relevantă pentru H1 |

**Controlul lipsă cel mai des numit:** semințe noi (Mistral: ≥ 3 pe familie, mai ales F6; ChatGPT: semințe noi cu zgomot potrivit; Copilot: un set de audit nou, după înghețarea analizei).

## 7. Criteriul de valoare pentru Deep Review (fixat ÎNAINTE de citirea raportului, 6 nov., ~22:25)

Costul rulării: ~27,7 $ raportați la 99% (≈ 3,3 × estimarea tipică de 8,43 $). Deep Review își justifică costul dacă aduce **cel puțin o constatare verificată, relevantă pentru decizie, pe care niciun alt participant nu a găsit-o** (o eroare în cod, analiză sau dosar; sau un test decisiv nou, bine definit). Dacă da: îl păstrăm la setările maxime doar la deciziile mari, cu bugetul de ~3 × estimarea. Dacă nu: la colocviile următoare folosim varianta gratuită (Argon 4 Medium, 2 pe săptămână) sau High în loc de Extra High.

## 8. Martor fără vot: DeepSeek (DeepThink + căutare web): direcția C

Răspunsul are textul principal în chineză și blocul final în engleză (8.997 de caractere, sub lungimea cerută). Fișier: `Raspunsuri/Martor_DeepSeek_DeepThink.md` (nemodificat). A deschis 79 de pagini web; nu citează ID-uri noi în afara celor din dosar.

| Afirmație | Verdict | Sursa |
|---|---|---|
| AdamW update RMS 0,2–0,4 (Liu et al.); R3: D1 0,86–0,95 | întemeiat | dosar |
| R1 nu spune că împărțirea e pe rulări; posibilă scurgere între ferestre vecine | **fals**: R1 spune explicit „test on each tech3 run, training on the other four runs” (împărțire pe rulări) | dosar R1 |
| D1 și τ sunt „prin definiție” acumulări ale lui Ση‖m̂‖ / Ση‖ĝ‖, deci G2 nu poate decât să pice | **parțial / exagerat**: Δθ depinde de vectorii m̂, v̂ elementwise, nu de norme; datele arată că nu e o identitate (D1 în F2: 0,86; D1_rel: 0,67–0,87). Pentru R1/R2 există însă o circularitate reală, pe altă cale (E1) | cod, R3 |
| „R² ≥ 0,86 cu un singur termen” pentru D1, D1_rel, D2, τ | **fals** pentru D1_rel (0,67–0,87 în tech4) | R3 |
| Q3: în F6, C10c e calculat pe etichete zgomotoase, iar D3 pe 128 de prompturi neantrenate | **fals**: amestecă brațele. În lumea sintetică, D3 și C10c folosesc aceeași baterie R (sarcini de referință, etichete corecte); zgomotul e doar în segmentele distractoare de antrenare. Cele 128 de prompturi neantrenate sunt ale brațului LM | dosar §1–§2, cod |
| Costul T3 (FOREVER): „3 semințe × 10 sarcini × 15 min ≈ 7,5 h pe planificator, 22,5 h în total” | **fals** (de 10 ori): 15 min sunt pentru o rulare întreagă de 10 sarcini, deci ~2,25 h pentru 3 × 3 rulări | dosar §5 |
| Idee nouă: controlul **D3_shuffled** (aceleași sonde și același cost, dar perechile de blocuri de 8 pași amestecate), ca să separe „măsurarea funcției” de „timpul acumulat” | opinie, **nouă** (niciun alt participant); înrudită cu întrebarea „lungimea drumului vs. distanța netă între capete”; de discutat la preînregistrare, nu adoptată (martor) | — |
| Deciziile 2–8: da / amânat / complet / înainte / bf16 / da / acum | identice cu majoritatea | — |

**Ca martor:** confirmă direcția C dintr-o familie de modele diferită, dar cu mai multe erori de fapt decât Copilot, ChatGPT sau Mistral (asemănător cu Gemini). Aduce o idee nouă (D3_shuffled). Nu intră în nicio numărătoare.


## 9. Deep Review (gemini-4-argon, Extra High / High): direcția C

Fișier: `Raspunsuri/Raspuns_DeepReview_Argon4_ExtraHigh.md` (134.558 de caractere, prin „Copy Report”, nemodificat). Costul raportat: ~27,7 $.

**Referințe** (toate verificate: arXiv API, Crossref): 1412.6980 (Adam); 1711.05101 (Decoupled Weight Decay, Loshchilov & Hutter); 1905.12558 (Limitations of the Empirical Fisher, Kunstner, Balles, Hennig); 1908.03265 (RAdam, Liu et al.); 1805.08289 (Measuring and regularizing networks in function space, Benjamin, Rolnick, Kording); 2204.07705 (Super-NaturalInstructions); 1908.04742 (MIR, Aljundi et al.); 1706.05394 (A Closer Look at Memorization, Arpit et al.); 1710.03740 (Mixed Precision Training); 2501.13453 (Spurious Forgetting, Zheng et al.); 2509.17348 (AIMMerging, Feng et al.); 2306.17833 (Resetting the Optimizer in Deep RL, Asadi et al.); DOI 10.1109/TIT.2003.813506 (Endres & Schindelin, „A new metric for probability distributions”, 2003). **Niciuna inventată.**

| Afirmație | Verdict | Sursa |
|---|---|---|
| **D2 se reduce algebric la η‖m̂‖:** D2 = √Σ v̂_lag·Δθ², iar Δθ ≈ η m̂/√v̂, deci v̂ se anulează (β₂ = 0,999, lag 16) | **întemeiat, confirmat în cod**; nou și precis (ceilalți vorbesc doar general de „identitatea Adam”). Explică R² 0,98–0,99 pentru D2: **D2 e aproape o tautologie** | `p2/agent.py` r. 204–206 |
| În R3, familia compusă F5 (= F2 + suprapunere + pauze + reporniri) rămâne în antrenare când se testează F2, F3 sau F4, deci „o familie lăsată deoparte” nu e „un mecanism lăsat deoparte”; doar F6 are un mecanism absent din rest | **întemeiat**, nou; R2 (F3 complet scoasă) e testul curat de mecanism | dosar §2, `tech4_analysis.py` |
| R3 nu raportează testele pe F1 și F4; R4 nu raportează F2, F3, F4 | întemeiat (prezentare; jurnalul le are pe toate) | `tech4_analysis.log` |
| D1_rel nu e reconstruit peste 0,90 de niciun scalar ieftin în nicio familie, nici de GBDT în F6 | întemeiat (= E2) | R3 |
| Brațul LM: cele 3 semințe au același program de faze, deci GBDT poate învăța poziția în fază; test propus: antrenare pe lmtech1, test pe lmtech2 | plauzibil, nou; afectează doar GBDT, nu scalarul liniar; verificarea e ieftină | — |
| Sondele LM sunt prompturi neantrenate cu răspuns aleator, deci D3 pe LM măsoară deriva priorului, nu retenția; propune ancorarea pe itemi din sarcina 0 | întemeiat ca observație conceptuală (cod: `make_world`) | `lm_forever_run.py` |
| τ pe factori e invariant la α (Adam anulează o scalare constantă a gradientului) | întemeiat (mecanism standard; R9: 0,944 față de 0,941) | R9 |
| Eticheta „C” e folosită și pentru Direcția C, și pentru varianta C a deciziei 1 („doar un studiu LM mic”) | **întemeiat**, și confirmat de răspunsuri: Gemini și Copilot scriu „1: C”, dar conținutul lor nu e „doar LM” (vezi §10) | dosar §7, prompt |
| În dosar, §6 omite „absolut” la C10c | întemeiat (minor) | dosar §6 |
| Numărul de parametri 925.440 implică un tabel de poziții de 8 rânduri, încă alocat | **fals**: tabelul are 4 rânduri (`max_ctx: 4`); Deep Review a omis bias-ul stratului de ieșire (512): 793.088 + 256 + 65.536 + 512 + 65.536 + 512 = 925.440 | `p2/agent.py` r. 41–45, config |
| „Dacă C10c e diferența între capetele intervalului, oscilațiile se anulează”, cu propunerea C10c_chunk | **fals** ca premisă: C10c e deja acumulat pe aceleași blocuri de 8 pași ca D3 (Σ_k mean_i \|Δℓ_i\|); C10c_chunk = C10c | `p2/run.py` r. 283–296, `triplets.py` |
| Concurenți noi de același cost (schimbarea mărginită a probabilității țintă, schimbarea entropiei), „calculabili offline pe jurnalele tech4 în < 0,1 h” | ideea: întemeiată (o propun și ChatGPT, Mistral); **costul: fals**, pentru că `chunks.npz` păstrează doar scalarii pe bloc, nu distribuțiile; cer rerularea (6 rulări ≈ 30 min) | `p2/run.py` |
| Controlul „distanța netă între capete” față de lungimea drumului pentru D3 | opinie, nouă (înrudită cu D3_shuffled de la DeepSeek, martor) | — |
| Sarcinile de reguli au fost scoase post hoc, iar R² 0,31 arată că D3 se decuplează la generalizare | **parțial**: scoaterea e documentată (note §4.2: regulile nu generalizau, sondele 0,02–0,30, 0–9 episoade valide), deci nu e post hoc arbitrară; inferența despre generalizare nu e susținută. Corect că dosarul nu explica | `Stadiul0_note_lucru.md` §4.2 |
| R1/R3 regresează rata pe ΔN plus sume cumulative (specificare greșită) | **fals** pentru scara de scalari: codul folosește rate (`rate_C5d`) plus termeni în ΔN; corect doar că antetul din dosar era ambiguu | `g2_preview.py` r. 53–60, `tech4_analysis.py` |
| Rezumatul: „toate ceasurile din parametri au R² ∈ [0,94; 0,99]” | parțial (D1_rel 0,67–0,87 cu scalari, 0,79 în F6; Deep Review dă chiar el 0,79 în detaliu) | R3 |
| Ipoteze despre căderea de după repetiția finală (pași săriți fp16 în încălzirea repetiției; marje mai mari la α 32) | plauzibile, verificabile din jurnale; neverificate încă | — |

**Recomandarea C:** argumentul principal (G2 pică pentru ceasurile din parametri, mecanismul Adam, D2 exact) e **întemeiat**. **Rămâne.**

**Criteriul de valoare (§7):** **îndeplinit.** Constatări verificate, relevante pentru decizie, găsite doar de Deep Review: (1) anularea exactă din D2; (2) F5 compromite separarea pe mecanisme din R3; (3) ambiguitatea etichetei „C” din decizia 1, confirmată de răspunsurile celorlalți. Are și 3 afirmații false de fapt (numărul de parametri, C10c_chunk, costul offline).

## 10. Rezultatul colocviului, după regula fixată (verificarea completă a celor 5)

**Direcția (Q7): C**, cu 4 voturi rămase după verificare (Gemini, Copilot, Mistral, Deep Review), față de B cu 1 (ChatGPT). Martorul DeepSeek (fără vot): tot C.

**Deciziile 1–8** (5 participanți):

| # | Gemini | Copilot | Mistral | ChatGPT | Deep Review | Rezultat |
|---|---|---|---|---|---|---|
| 1 | „C” | „C” | altul: fără Stadiul A, doar D3/F6 + T4 | R | R „restrâns sub Direcția C” | **ambiguu din vina dosarului** (vezi mai jos) |
| 2 | da | da | da | da | da | **da** (5/5) |
| 3 | amânat | amânat | amânat | amânat | amânat | **amânat** (5/5) |
| 4 | complet | complet | complet | complet | complet | **complet** (5/5) |
| 5 | înainte | înainte | înainte | înainte | înainte | **înainte de repetiția finală** (5/5) |
| 6 | bf16 | bf16 | bf16 | bf16 | bf16 | **bf16** (5/5) |
| 7 | da | da | da | da | da | **da** (5/5) |
| 8 | acum | acum | acum | după Stadiul A | acum | **acum** (4/5) |

**Decizia 1, notă de onestitate:** în dosar (§7), varianta „(C)” a deciziei 1 însemna „doar un studiu LM mic”, iar „C” era și numele Direcției C. Gemini și Copilot au scris „1: C”, dar conținutul răspunsurilor lor nu e „doar LM”: păstrează testul D3/F6 pe lumea sintetică, închid ceasurile din parametri și fac nota FOREVER, deci conținutul Direcției C. Pe conținut, toți cinci cer același lucru: **reconstrucția (G2) ca rezultat principal pentru ceasurile din parametri; un singur test confirmator, D3 contra scării C10c în F6, pe semințe noi; brațul LM descriptiv, plus testul intervențional al planificatorului FOREVER.** Asta e varianta R în forma ei cea mai restrânsă, adică conținutul Direcției C. **Interpretarea e a mea; utilizatorul poate opri sau amâna.**

**Testele decisive propuse de cel puțin 2 participanți (se preînregistrează primele):**

| Test | Propus de | Cost estimat pe laptop |
|---|---|---|
| T-A: planificatorul FOREVER intervențional: repetiția condusă de τ, de Ση‖m̂‖, doar de program (și de pași), bf16, uitarea și retenția ca rezultat | toți 5 | 4 ceasuri × 3–5 semințe × 15 min ≈ 3–5 h GPU |
| T-B: F6 pe semințe noi, cu doze de zgomot (0 / 0,1 / 0,3 / 0,5) și familii de control; D3 contra B_strong + C10c + concurenți funcționali noi (probabilitate mărginită, entropie); întâi G2 (orb), apoi H1 (ΔR² ≥ 0,02, interval pe rulări) | Copilot, Mistral, ChatGPT, Deep Review | ~32–40 de rulări ≈ 2,6–3,3 h CPU + analiză |
| T-C: analogul C10c pe brațul LM (și variantele pe 31 de cuvinte, entropie), din sondele salvate | Mistral, ChatGPT, Deep Review | < 0,5 h CPU, fără GPU |
| T-D: auditul reconstrucției: fără trăsături derivate din Δθ (C6), pe benzi de ΔN, cu mecanismul lăsat deoparte (fără F5), transfer lmtech1 → lmtech2, apoi pe semințe noi cu analiza înghețată | Copilot, ChatGPT, Deep Review (Mistral: ferestre) | ~1 h CPU pe jurnalele existente; semințele noi vin din T-B |

Listate, nepreînregistrate primele (un singur participant): reziduul pe pas al lui D1 (Mistral T5), datele naturale SuperNI (Gemini; Deep Review ca subset), controlul distanță netă / D3_shuffled (Deep Review; DeepSeek ca martor).
