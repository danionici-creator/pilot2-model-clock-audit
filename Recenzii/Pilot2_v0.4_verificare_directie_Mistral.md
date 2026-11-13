# Verificarea evaluării de direcție (Mistral Large 4) pentru Pilot 2

Răspunsul: `Recenzie_Mistral_Large4_directie_v04.md` (4 nov. 2026, 19:05; 2.166 tokeni de intrare, 3.439 de ieșire, din care 1.723 de gândire; finish_reason: stop; cost de ordinul centimilor). Mesajul trimis: `Mistral_detalii/mistral_msg_directie_v04.txt`. Verificat pe 4 nov. 2026.

## 1. Referințe

Răspunsul citează doar lucrări din rezumatul trimis (FOREVER, arXiv:2601.03938; Toneva et al., arXiv:1812.05159; Jin & Ren, arXiv:2402.01865), toate verificate deja. **Nicio referință nouă, nicio referință inventată.**

## 2. Afirmațiile, una câte una

| # | Afirmația | Verdict | Motiv |
|---|---|---|---|
| 1 | Întrebarea e o lacună reală: FOREVER compară ceasul doar cu numărul de pași | Corect | Verificat la 3 nov. pe arXiv și în ACL Anthology |
| 2 | Rezultatul contează doar dacă „echivalent” are o marjă strânsă, dacă există și o condiție de tip FOREVER (LM mic + LoRA) și dacă instrumentul e reutilizabil | Întemeiat ca judecată | Marja există deja (SESOI); a doua condiție e Stadiul C, care e scos din preînregistrare |
| 3 | Să raportăm cât de bine se reconstruiește c_e din telemetrie (un R²) | Întemeiat ca accent, deja în design | E poarta G2 (rata ρ̄ prezisă din B_strong). Propunerea utilă: G2 să fie un rezultat de prim rang, nu doar o poartă |
| 4 | **„D este actualizarea AdamW, deci o funcție deterministă de rata de învățare, normele momentelor și ale lui v, toate în B_strong; echivalența e aproape predeterminată”** | **Greșit ca afirmație generală** | Norma actualizării ‖η m̂ / (√v̂ + ε)‖ depinde de raporturile pe fiecare parametru, nu doar de normele globale ‖m̂‖ și Tr v̂. Afirmația e aproape adevărată doar pentru D2 în același pas (≈ η‖m̂‖, adică C5d), exact cazul pe care protocolul îl tratează în §5.1. Pentru D1, D1_rel și D3 nu există o identitate. Partea corectă: colinearitatea poate fi mare, iar „echivalent” e rezultatul cel mai probabil, cum spune și rezumatul |
| 5 | „c_e cere păstrarea sau salvarea întregii stări la fiecare pas, telemetria e O(1)” | **Greșit** | c_e^{D1} e un scalar care se acumulează; norma actualizării se calculează în același pas, ca și norma gradientului. Salvări de stare cere deplasarea netă (Disp), nu c_e. Argumentul „echivalent, dar mai ieftin” nu se susține în această formă |
| 6 | Lumea de jucărie poate susține o afirmație despre mecanisme, nu despre LLM; un rezultat nul acolo e greu de publicat | Parțial | Limitarea de domeniu e reală și a fost cerută și de Deep Review. „Greu de publicat” e o estimare, nu un fapt; pentru o preînregistrare și un preprint pe Zenodo, un nul bine controlat rămâne publicabil |
| 7 | Pe un singur CPU, Pythia-160m/410m cu LoRA permite „câteva zeci de rulări” | Neverificat | Fezabilitatea pe acest laptop nu e măsurată. `transformers` e instalat, `peft` nu, iar modelele Pythia nu sunt descărcate. E nevoie de o măsurătoare de timp (descărcarea cere acordul utilizatorului) |
| 8 | Preînregistrarea doar a Stadiului A e corectă, cu o anexă fixă despre regula de decizie a Stadiului B | Întemeiat | Coincide cu propunerea făcută utilizatorului; anexa e o precauție bună împotriva respecificării după rezultat |
| 9 | Protocolul e disproporționat: de păstrat doar o familie naturală și una adversarială | Parțial | Diagnosticul (complexitate adăugată ca proces, nu ca inferență) e corect. Remediul e greșit: familiile F2–F3 sunt chiar domeniul în care numărul de pași se decuplează de schimbare, deci singurul în care c_e poate aduce informație; fără ele, testul își pierde obiectul. De acceptat: H3 scos din preînregistrare; un singur control pozitiv și un singur placebo pe inferența principală; detaliile tehnice mutate în anexă |
| 10 | Un protocol de cel mult 8 pagini | Parțial | Ca țintă pentru textul principal, da; specificațiile (generatorii, porțile) trebuie să rămână undeva, ca anexă |
| 11 | Studiul mai bun: direct comparația planificatoarelor de repetiție (după pași, după c_e ca în FOREVER, după un GBM pe telemetrie) pe Pythia + LoRA, 30–60 de rulări | Întemeiat ca direcție, riscant ca plan | E întrebarea practică pe care o ridică FOREVER, iar comparația cu un GBM pe telemetrie ar fi nouă. Dar Mistral recunoaște singur riscul: cu zeci de rulări, rezultatul poate fi neconcludent. Fezabilitatea nu e măsurată |
| 12 | „Stadiul A e un ocoliș” | Parțial | Față de întrebarea practică a lui FOREVER, da. Față de programul din Perspective, nu: criteriul (c) (validitate predictivă) și criteriul (d) (folosire) sunt distincte, iar Stadiul A testează (c) |
| 13 | Recomandarea: C (un studiu reproiectat, mai mic, pe LM + LoRA). M-ar face să mă opresc un R² de reconstrucție > 0,99 într-un pilot | Discutabil, dar criteriul de oprire e util | Criteriul se poate verifica **acum**, ieftin, pe rulările tehnice: G2 nu folosește ținta T1, deci intră în faza 0a și nu încalcă regula despre valoarea incrementală a lui c_e |

## 3. Calitatea răspunsului

Scurt (1.723 de tokeni de gândire). Judecăți strategice rezonabile și sincere, dar cu două erori tehnice de fond (punctele 4 și 5), care chiar susțin argumentul „echivalența e predeterminată”. Recomandarea finală se sprijină parțial pe ele. Concluziile se folosesc ca opinie, nu ca verdict.

## 4. Ce rămâne după verificare

- **Convergent cu Deep Review și cu propria analiză:** domeniul trebuie declarat îngust; protocolul e prea complex; Stadiul B iese din preînregistrare; G2 (reconstrucția) trebuie pus în prim-plan.
- **Nou și util:** criteriul „dacă rata lui c_e se reconstruiește din telemetrie cu R² > 0,99, întrebarea e închisă prin construcție”. Testul e ieftin și orb față de țintă.
- **Deschis:** dacă studiul raportat trebuie mutat pe un model de limbaj mic. Asta depinde de o măsurătoare de fezabilitate care încă nu există.

## 5. Doi pași mici, ambii fără a atinge relația c_e–T1

1. **G2 pe rulările tehnice tech3** (F2, F3, 3e-4, fără reguli): R²-ul ratei ρ̄ pentru fiecare D (D1, D1_rel, D2, D3), prezis din B_strong, în afara rulării. Minute de calcul. Dacă e ≥ 0,99 pentru toți candidații, întrebarea e practic închisă și se raportează ca atare. Dacă e mic, auditul are obiect.
2. **Măsurătoarea de timp pentru Pythia-70m/160m cu LoRA pe CPU** (secunde pe pas, memorie), după acordul pentru descărcare (~170–330 MB de pe Hugging Face). Ea decide dacă varianta C e fezabilă pe laptop.

Abia după acești doi pași se alege între B (Stadiul A simplificat, lumea sintetică) și C (studiu mic pe LM + LoRA), eventual cu lumea sintetică drept pilot.

## 6. A doua opinie: aceeași întrebare la raționament „medium”

Răspunsul: `Recenzie_Mistral_Large4_directie_v04_medium.md` (19:14; 5.445 de tokeni de ieșire, din care 3.704 de gândire, adică de peste două ori mai mult decât prima; max_tokens 64.000; finish_reason: stop). Aceleași referințe (FOREVER, Toneva, Jin & Ren, plus Kalajdzievski, arXiv:2401.05605, din rezumat); nicio referință nouă.

### Comparația

| Tema | Prima opinie (low) | A doua (medium) | Verdict |
|---|---|---|---|
| Recomandarea finală | **C**: studiu reproiectat pe LM + LoRA, lumea sintetică doar pilot | **B**: doar Stadiul A preînregistrat, protocol mai scurt, **plus un braț Pythia + LoRA** (20–30 de rulări), raportat separat | Converg pe fond: un braț pe LM mic e ce face rezultatul citabil. Diferă doar dacă lumea sintetică rămâne rezultatul principal |
| Reconstruirea lui c_e din telemetrie | „funcție deterministă de normele din B_strong” (greșit) | „funcție deterministă de gradient și de momentele a doua, deci în mare reconstructibilă” | Formulare mai prudentă, dar încă exagerată: B_strong conține normele, nu vectorii. Direcția (colinearitate mare) e plauzibilă și se poate măsura cu G2 |
| Costul lui c_e | „cere salvarea stării la fiecare pas” (greșit) | „cere salvări de stare **sau** o distanță pe toți parametrii la fiecare pas” | A doua jumătate e corectă (O(P) calcul pe pas, cât norma gradientului), prima rămâne greșită. Comparația de cost e corectă de făcut, dar va arăta costuri apropiate pentru D1 |
| Familiile de fluxuri | doar „naturală” + adversarială (greșit) | **păstrează explicit familiile care decuplează pașii de schimbare** („fără ele întrebarea e vidă”); reduce de la 6 la 3 | A doua corectează eroarea primei |
| Simplificări | sub 8 pagini; un control pozitiv și un placebo | ~10 pagini; o singură împărțire pilot + test; GBDT cu o configurație blocată fără căutare, sau un model mixt; controlul pozitiv „numărul de pași prezice uitarea” | **Respins** renunțarea la căutarea de hiperparametri: un baseline neacordat fabrică avantaje (lecția studiului închis; Mukhoti et al. 2018). **Respins** înlocuirea lui G4b cu „pașii prezic uitarea”: nu testează sensibilitatea conductei la un efect de mărimea căutată. **Acceptabil** de discutat: mai puține familii și mai puține împărțiri |
| Marja de echivalență | — | „din mărimile efectelor din FOREVER” | **Parțial**: FOREVER raportează câștiguri de acuratețe ale planificării, nu ΔR² ale predicției uitării; marja se poate lega de FOREVER doar într-un braț de planificare, nu în Stadiul A |
| Studiul mai bun | comparația directă a planificatoarelor pe Pythia + LoRA, 30–60 de rulări | (1) ablația lui FOREVER pe Pythia-70M + LoRA, 20–40 de rulări; (2) o sondă cauzală 2×2 în lumea sintetică: flux adversarial × pauze | (1) converge cu prima opinie. (2) **Slab**: în pauze θ e înghețat, deci se opresc și c_e, și toată telemetria, iar uitarea e zero; pauza nu deosebește c_e de telemetrie (protocolul o folosește deja doar ca verificare de bun-simț, F4) |
| Fezabilitatea pe laptop | Pythia-160m/410m „câteva zeci de rulări” | Pythia-70M „lent, dar plauzibil”; 160M „probabil nu” | A doua e mai prudentă; ambele sunt estimări nemăsurate |
| Stadiul B | anexă fixă cu regula de decizie | protocolul Stadiului B depus public, cu dată, înainte de orice rulare B | Ambele întemeiate; compatibile |

### Ce rămâne după ambele opinii

1. **Convergent și întemeiat:** doar Stadiul A preînregistrat; protocol mult mai scurt, cu detaliile în anexă; titlul și rezumatul formulate în jurul întrebării „e timpul centrat pe model redundant față de telemetria optimizatorului?”; un **braț pe un LM mic cu LoRA** ca ancoră de validitate externă, raportat separat.
2. **Divergent:** dacă lumea sintetică rămâne rezultatul principal (B) sau doar pilot (C). Decide fezabilitatea brațului LoRA.
3. **Respins în ambele:** afirmațiile de identitate și de cost luate ca atare; renunțarea la acordarea baseline-ului; sonda cu pauze.
4. **Pașii următori neschimbați:** G2 pe tech3 (orb față de T1) și măsurătoarea de timp Pythia-70M + LoRA (cere acordul pentru descărcare). După ele se fixează forma v0.5.
