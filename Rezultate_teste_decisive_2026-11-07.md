# Testele decisive ale colocviului Pilot 2: rezultate (noaptea 6–7 nov. 2026)

Testele vin din colocviul din 6 nov. (`Colocviu/Verificare_raspunsuri_2026-11-06.md` §10). Criteriile și scripturile de analiză au fost fixate și amprentate **înainte** de rulări (`Stadiul0/preinregistrare_TA_TB_2026-11-06.md`; `Stadiul0/runs/preinregistrare_sha256.txt`; `tc_criterii.md`, `td_criterii.md`). Coloanele de uitare din lumea sintetică (T1) au rămas **nedeschise**.

## Verdictele, după criteriile fixate

| Test | Întrebarea | Verdict | Cifrele cheie |
|---|---|---|---|
| **T-C** (brațul LM, offline) | D3 pe LM conține ceva în plus față de concurentul de același cost? | **NU: reconstruit** | C10c_LM (schimbarea pierderii pe cuvântul-țintă al sondei) reconstruiește D3 la R² 0,979–0,989 în toate cele 4 configurații |
| **T-D** (reconstrucția, offline) | Reconstrucția ceasurilor din parametri e un artefact? | **NU, în afară de un caz limitat** | fără trăsăturile circulare C6: neschimbat; D2 robust peste tot (0,98); transfer LM între configurații 0,96–0,97; D1 nu e reconstruit de **scalarul unic** în F1/F4 (0,40/0,35), dar e reconstruit de toată telemetria (0,96–0,99) |
| **T-B** (lumea sintetică, 40 de rulări noi) | D3 scapă reconstrucției în F6, cu zgomot dozat, pe semințe noi? | **NU: G2 pică, D3 se închide**; H1 nu se rulează | F6 la zgomot 0,3: R² 0,991 (min 0,968), 0/8 semințe sub 0,90; C10c singur 0,958; la toate nivelurile de zgomot ≥ 0,990; D1_rel ≥ 0,993 |
| **T-A** (brațul LM, 20 de rulări noi) | Repetiția condusă de τ (FOREVER) reduce uitarea mai mult decât una condusă de un ceas ieftin? | **NU: echivalență practică cu toate trei** (±2 pp) | acuratețea finală 0,240–0,246 la toate ceasurile; τ față de Ση‖m̂‖: −0,004 [−0,015; +0,007], cu declanșări identice (≤ 1 pas); față de programul ratei: +0,002 [−0,004; +0,009]; față de pași: −0,002 [−0,011; +0,007] |

## Ce se poate afirma acum (în limitele cadrului: modele mici, fapte sintetice, Qwen3-0.6B + LoRA)

1. **Niciun candidat la indicele experiențial c_e nu conține informație dincolo de telemetria ieftină și de concurenții de același cost:** nici distanțele în parametri (D1, D1_rel, D2), nici ceasul FOREVER τ, nici schimbarea funcțională D3, pe niciun braț. Excepțiile din rundele tehnice (D3/F6, D1_rel/F6, D3 pe LM) au dispărut pe semințe noi sau la comparația cu concurentul de același cost. D2 se reduce chiar algebric la Ση‖m̂‖ (Deep Review, confirmat în cod).
2. **Ceasul FOREVER nu aduce un avantaj de planificare măsurabil:** declanșată după Ση‖m̂‖ (gratuit, din optimizator), după programul ratei sau după simplul număr de pași, repetiția dă aceeași retenție în limita a ±2 puncte procentuale. Ση‖m̂‖ reproduce chiar momentele declanșării. Rezultatul e compatibil cu ce raportează chiar autorii FOREVER: τ_day nu se corelează cu uitarea finală (r = 0,22, p = 0,45; arXiv:2601.03938v2).
3. **Linia de cercetare „timpul propriu ca acumulare de schimbare internă” e închisă empiric în acest cadru.** E un rezultat negativ documentat (scenariul de eșec A), cu teste preînregistrate, nu o presupunere.

## Limitele (de spus explicit în orice raport)

- T-A: retenția e mică în toate brațele (acuratețea finală ~0,24, BWT ~ −0,83; memoria are 16 fapte din 512 pe sarcină). Echivalența e demonstrată în acest regim de uitare puternică; în regimuri cu retenție mai bună (de exemplu SuperNI) nu e testată. 5 semințe pe ceas.
- T-B: G2 e evaluat în interiorul fiecărei condiții (o sămânță lăsată deoparte), ceea ce e relevant pentru H1 (care e definit în interiorul rulării). Varianta cu o familie întreagă lăsată deoparte (cerută și de Deep Review) nu a fost preînregistrată.
- Totul e pe modele mici și date sintetice; nimic despre modele mari, date naturale sau experiență subiectivă.

## Ce urmează (decizii pentru utilizator / colocviu)

- **Raportul de închidere** (reconstrucția ca rezultat principal, plus T-A, T-B, T-C, T-D) și **nota FOREVER** (decizia 8: „acum”), cu limitele de mai sus.
- **Revizuirea nivelului 2 din lucrarea Perspective:** retragerea ceasurilor din parametri și a lui D3 drept candidați cu informație proprie; c_e rămâne o definiție, dar întrebarea deschisă se închide negativ pentru candidații testați.
- Opțional, înainte de publicare: verificarea pe date naturale (SuperNI, propusă de Gemini și Deep Review), dacă se vrea extinderea concluziei dincolo de faptele sintetice.

## Adăugat 7 nov., 08:52: verificarea pe SuperNI, S1 (preînregistrată: `Stadiul0/preinregistrare_SuperNI_2026-11-07.md`)

Programul FOREVER pe 5 sarcini SuperNI naturale și eterogene (ordinea 7 a FOREVER: task1572, task363, task1290, task181, task002; generare și clasificare, prompturi cu mediana între 106 și 512 tokeni), 3 semințe. **Reconstrucția se extinde la date naturale:** Ση + Ση‖m̂‖ reconstruiește rata lui τ la R² **0,986** (o sămânță lăsată deoparte) și **0,980** (o sarcină întreagă lăsată deoparte; cea mai slabă sarcină 0,969). Programul ratei singur: 0,44–0,51. Limitele scrise la punctul 1 (doar fapte sintetice) se reduc deci pentru reconstrucție. Planificatorul pe SuperNI (S2) rulează.

## Adăugat 7 nov., 11:00: SuperNI, S2 (planificatorul)

Aceleași 3 semințe, repetiția declanșată de Ση‖m̂‖ în loc de τ. Pierderea pe test după ultima repetiție finală: diferența relativă τ − Ση‖m̂‖ = **−0,6%, IC 95% [−1,9%; +0,7%] → echivalență practică** (marja fixată ±5%). Ση‖m̂‖ declanșează repetițiile chiar în aceiași pași ca τ (mediana diferenței 0 pași, 7 repetiții în ambele brațe).

**Limita principală care rămâne:** toate comparațiile cu FOREVER sunt făcute cu portul nostru al programului lor, nu cu codul lor original, și nu le-am reprodus cifrele de bază. Pasul care ar închide-o: rularea codului lor (`finetune_cl_our_qwen.py`, cu versiunile lor de biblioteci) pe benchmark-ul lor, pe un subset fezabil pe laptop, întâi ca reproducere, apoi cu τ înlocuit de Ση‖m̂‖.

## Adăugat 8 nov., 01:55: reproducerea FOREVER cu codul lor, R1 (preînregistrată: `Stadiul0/forever_repro/preinregistrare_FOREVER_repro_2026-11-07.md` + addendum)

Codul lor neschimbat (commit `bbeb549a21e5…`, versiunile lor de biblioteci, torch 2.8), ordinea 4 („Standard CL”: dbpedia → amazon → yahoo → agnews), argumentele exacte din scriptul lor; evaluarea cu scripturile lor neschimbate (`runs/forever_repro_eval_tau.log`).

| | R1 (noi, o rulare, ordinea 4) | Articolul (Qwen3-0.6B, media pe 3 ordini) |
|---|---|---|
| **OP** (potrivire exactă) | **72,37** (dbpedia 93,2 · amazon 47,5 · yahoo 60,3 · agnews 88,4) | 72,9 |
| BWT (extragerea tolerantă a etichetei) | −5,78 (dbpedia −4,8 · amazon −8,5 · yahoo −4,0) | −4,7 |
| OP cu extragerea tolerantă | 72,39 | — |

**Verdict după criteriul fixat (OP în ±5 puncte de 72,9): R1 REPRODUCE FOREVER** (diferența −0,53 puncte). BWT e cu ~1,1 puncte mai slab, dar BWT nu era criteriu.

**Limite:** o singură rulare, pe o singură ordine; reperul articolului e media pe 3 ordini. Codul lor nu e determinist (fp16). Antrenarea sarcinilor 1–3 a rulat fără cache-ul alocatorului PyTorch (adaptarea 5, din cauza memoriei de 4 GB; nu schimbă calculele). **Consecința pentru limita de mai sus:** cifra de bază a FOREVER e reprodusă cu codul lor, deci comparația τ față de η‖m̂‖ din R2 (în curs, gata ~12:00–13:30) se va face pe codul lor, nu pe portul nostru.

## Adăugat 8 nov., ~13:45: reproducerea FOREVER cu codul lor, R2 (ceasul η‖m̂‖ în locul lui τ)

Aceeași rulare ca R1, cu o singură schimbare: contorul care declanșează repetițiile avansează cu η·‖m̂‖ în loc de ‖Δθ‖ (intensitatea repetițiilor rămâne calculată din ‖Δθ‖, ca în original). Pornită automat la 01:48, terminată la 13:35:01, toate etapele cu rc 0. Evaluarea cu scripturile lor neschimbate, amprentele verificate înainte de rulare (`runs/forever_repro_eval_eta_m.log`).

| | τ (R1) | η‖m̂‖ (R2) | τ − η‖m̂‖ |
|---|---|---|---|
| **OP** (potrivire exactă) | **72,37** | **71,53** | **+0,84** |
| dbpedia (prima sarcină) | 93,21 | 87,89 | +5,33 |
| amazon | 47,52 | 48,92 | −1,40 |
| yahoo | 60,34 | 61,66 | −1,32 |
| agnews | 88,40 | 87,65 | +0,75 |
| **BWT** | **−5,78** | **−6,47** | **+0,69** |
| BWT pe sarcini (dbpedia · amazon · yahoo) | −4,8 · −8,5 · −4,0 | −9,9 · −5,8 · −3,7 | |
| OP cu extragerea tolerantă | 72,39 | 71,57 | +0,82 |

**Verdict după criteriul fixat (|ΔOP| ≤ 2 puncte; același raport pentru BWT): ECHIVALENȚĂ** pe OP (0,84) și pe BWT (0,69).

**Declanșările repetițiilor** (descriptiv): același număr în fiecare sarcină (4 declanșate de ceas plus repetiția finală, toate trecute). η‖m̂‖ declanșează la același pas sau mai târziu: sarcina 1 cu +2 / +4 / +7 pași, sarcina 2 cu +2 / +9 / +18, sarcina 3 cu 0 / +3 / +33 (din 313; prima repetiție vine în ambele imediat după calibrare).

**Secundar (preînregistrat, `r2_reconstruction.py` amprentat înainte de date; `runs/forever_repro_r2_reconstruction.log` și `.json`):** R² al lui Σ‖Δθ‖ pe ferestre de 8 pași, din creșterea ceasului η‖m̂‖: **comun 0,922 (351 de ferestre; reperul ≥ 0,90 atins)**; pe sarcini: dbpedia 0,937 (234 de ferestre), amazon 0,986, yahoo 0,934, **agnews 0,578** (39 de ferestre fiecare). Verificare exploratorie (nepreînregistrată): la agnews corelația e 0,76, iar împrăștierea lui y nu e mică (CV 0,49), deci potrivirea slabă e reală; cauza nu a fost cercetată. Valoarea comună e dominată de dbpedia (2/3 din ferestre).

**Citire:**
1. **În codul lor, înlocuirea ceasului τ cu η‖m̂‖ lasă rezultatul agregat în marja preînregistrată**, la fel ca în portul nostru (SuperNI S2: −0,6%). Limita principală de până acum („comparațiile au folosit portul nostru, nu codul lor”) e ridicată pentru această ordine și această pereche de rulări.
2. **Agregatul ascunde o diferență mare pe dbpedia:** 5,3 puncte în favoarea lui τ (uitare −9,9 față de −4,8), compensată parțial de +1,3–1,4 puncte pe amazon și yahoo în favoarea lui η‖m̂‖. Cu o singură pereche nu se poate separa efectul ceasului de nedeterminism. Zgomotul măsurat pe sarcina 0 (~0,2 puncte, unde ceasul nu joacă niciun rol) e zgomotul imediat după antrenare, nu cel acumulat după încă 3 sarcini, deci nu o explică și nici nu o exclude. Verdictul rămâne cel dat de regula fixată; diferența pe dbpedia e o întrebare deschisă, nu un rezultat.
3. **Reconstrucția ține în codul lor în agregat (0,92), dar nu uniform:** pe agnews (0,58) η‖m̂‖ urmărește slab mișcarea reală a parametrilor.

**Limite:** o singură pereche de rulări, o singură ordine, un model mic (0,6B), sarcini de clasificare; nedeterminismul fp16 al codului lor. **Ce ar lămuri punctul 2:** mai multe rulări pe fiecare ceas. Sarcina 0 nu depinde de ceas, deci perechile pot porni din același adaptor după sarcina 0, cu ~7,5 h pe rulare (sarcinile 1–3 plus generările) în loc de ~12 h. Nedecis; decizia de direcție aparține colocviului sau utilizatorului.

**Completare exploratorie (calculată după rezultate, nepreînregistrată; `r2_reconstruction_arm.py eta_m`, `runs/forever_repetari_r2_eta_m.json`):** pe sarcinile cu repetiții (1–3), R² comun al reconstrucției în R2 e **0,749** (117 ferestre), sub reperul de 0,90. Valoarea preînregistrată de 0,922 se datorează în mare parte lui dbpedia, unde nu există repetiții. Citire prudentă: în codul lor, η‖m̂‖ urmărește bine mișcarea parametrilor în antrenarea simplă, dar mai slab când apar repetițiile.

## Adăugat 8 nov., după-amiaza: colocviul scurt despre continuare și analiza (d)

**Colocviul** (`Colocviu/Regula_de_decizie_2026-11-08.md`, `Verificare_raspunsuri_2026-11-08.md`). ChatGPT GPT-6 High, Gemini 3.1 Pro High și Mistral Vibe Think au primit același dosar. Toți trei au recomandat **(d) + (a) etapa 1**; argumentele de bază trec verificarea. Ce se schimbă după verificare:
- **Formularea R2 corectată** (critică comună, verificată): „cu codul autorilor (o singură pereche, o singură ordine, sămânța 42), înlocuirea **ceasului care declanșează repetițiile** τ = Σ‖Δθ‖ cu Ση‖m̂‖ (intensitatea β rămâne calculată din ‖Δθ‖) a lăsat OP (72,37 față de 71,53) și BWT (−5,78 față de −6,47) **în marja descriptivă preînregistrată de ±2 puncte; nu e un test statistic de echivalență**. Pe dbpedia, diferența e de 5,33 puncte (5,26 cu extragere tolerantă) și nu e atribuită. Reconstrucția pe sarcinile cu repetiții: R² **0,749**; valoarea comună de 0,922 e diluată de dbpedia, unde nu există repetiții.” Prima declanșare (pasul 24) coincide prin construcție.
- **Nomenclatura:** „ordinea 4” din documentele noastre e `dataset_id` 4 din depozitul lor, adică **ordinea 1 din articol** (anexa G, tabelul 14). Verificat.
- **Limită nouă:** generatoarele lor decodează stocastic (`do_sample=True`, `temperature=0.02`, fără sămânță), deci evaluarea are un mic zgomot propriu.

**Analiza (d)**, fixată și amprentată înainte de rulare, fără GPU:
- Pe aceeași traiectorie, τ ar fi declanșat mai devreme decât η‖m̂‖ (48/50, 46/48, 89/96 la prima declanșare diferită). **Ceasurile diferă intrinsec în codul lor**, deci întârzierea nu e zgomotul rulării.
- Divergența **nu** stă în tranzițiile de după repornirea optimizatorului.
- Post hoc: raportul Σ‖Δθ‖ / Ση‖m̂‖ derivă în timpul sarcinii (fereastra de calibrare / restul: 0,97, 0,86, 0,70), în aceeași ordine cu întârzierile și cu R² slab pe agnews. **Ipoteză:** calibrarea pe 24 de pași îngheață un factor care apoi derivă.

**Consecința pentru afirmația „Ση‖m̂‖ reconstruiește și poate înlocui ceasul FOREVER”:** în codul lor, „reconstruiește” se restrânge la o corelație puternică, dar cu un factor care derivă. „Poate înlocui” rămâne valabil doar la nivelul rezultatului agregat, într-o pereche. Coincidența planificărilor din portul nostru **nu se transferă** la codul lor. Etapa 1 a lui (a) decide dacă deficitul de pe dbpedia se reproduce din puncte de start comune.

## Adăugat 9 nov., ~05:50: rulările repetate, etapa 1 (preînregistrare v3: `Stadiul0/forever_repro/preinregistrare_FOREVER_repetari_2026-11-08.md`)

**Verdictul (regula v3, aplicată mecanic de `rep_verdict.py`; cifrele verificate separat din `runs/forever_repro_eval_*.log`): NU SE REPRODUCE ROBUST.** D_A1 = −0,51 și D_B1 = +3,29 au semne opuse. Datele nu susțin o atribuire stabilă către ceas a diferenței de 5,33 puncte pe dbpedia din R2. Formularea nu este „ceasul nu are efect”: cu o singură rulare pe celulă, zgomotul rulării și o eventuală interacțiune ceas × punct de plecare nu se pot separa. Etapa 2 nu pornește (regula v3). Fișiere: `runs/forever_repetari.log`, `runs/forever_repetari_verdict.json`.

| Braț | Ceas | Sarcina 0 | dbpedia | amazon | yahoo | agnews | OP | BWT |
|---|---|---|---|---|---|---|---|---|
| `tau` (R1) | τ | A | 93,21 | 47,52 | 60,34 | 88,40 | 72,37 | −5,78 |
| `eta_m` (R2) | η‖m̂‖ | B | 87,89 | 48,92 | 61,66 | 87,65 | 71,53 | −6,47 |
| `eta_m_A1` | η‖m̂‖ | A | 93,73 | 49,36 | 61,86 | 87,20 | 73,04 | −4,79 |
| `tau_B1` | τ | B | 91,17 | 49,84 | 61,76 | 87,45 | 72,56 | −4,69 |

**Raportate secundar, fără verdict (preînregistrate):**
- Perechile τ − η‖m̂‖ (A1 / B1): OP −0,67 / +1,03; BWT −0,99 / +1,78; uitarea pe dbpedia −0,50 / +3,21. Toate diferențele de OP și BWT stau în marja descriptivă de ±2 puncte, ca în R2.
- Efectul adaptorului sarcinii 0 (A − B, descriptiv): τ +2,04; η‖m̂‖ +5,84. Adaptoarele A și B diferă doar prin nedeterminismul GPU al sarcinii 0 (dbpedia după sarcina 0: 98,04 față de 97,86). Pe cele patru celule, dbpedia final variază între 87,89 și 93,73, iar OP între 71,53 și 73,04.
- Verificări de integritate: adaptoarele sarcinii 0 copiate au amprentele sursei (`636589d5…` în `eta_m_A1`, `66dc0d26…` în `tau_B1`). Fișierele R1 și R2 nu au fost modificate (date din 8 nov., 00:58 și 12:45). Toate etapele au rc = 0. În brațul 2: GPU maxim 67 °C, la priză tot timpul, fără încetinire termică; zona termică ACPI a atins maxim 94,9 °C, sub pragul paznicului de 97 °C, la fel ca în nopțile anterioare.
- **Declanșările** (pasul la care trece pragul; diferența η‖m̂‖ − τ în fiecare pereche, fără prima declanșare, care e la pasul 24 prin construcție):
  - A1: amazon +2, +5, +11; yahoo +1, +3, +5; agnews +3, +12, iar al patrulea prag nu e atins în η‖m̂‖ (o repetiție declanșată de ceas mai puțin).
  - B1: amazon +2, +4, +9; yahoo +2, +6, +14; agnews 0, +6, +36.
  - În 16 din 17 declanșări comparabile, η‖m̂‖ declanșează mai târziu, într-una la același pas, niciodată mai devreme.
  - Pentru comparație, între cele două rulări τ (R1 și `tau_B1`, adaptoare diferite) declanșările diferă cu cel mult 4 pași.
  - Întârzierea e deci sistematică și confirmă rezultatul analizei (d): ceasurile diferă intrinsec în codul lor. În aceste două perechi, întârzierea nu s-a tradus într-o diferență consecventă de retenție.
- R² al reconstrucției, sarcinile 1–3, brațul `eta_m_A1`: **0,9695** (amazon 0,986, yahoo 0,975, agnews 0,963), față de 0,749 în R2 (agnews 0,578). **Valoarea slabă din R2 nu se repetă.** Citirea de la completarea din 8 nov. („mai slab când apar repetițiile”) nu se generalizează: brațul 1 are aceleași repetiții și R² ridicat.

**Completare exploratorie (calculată după rezultate, nepreînregistrată, aceeași definiție ca în analiza (d)):** raportul Σ‖Δθ‖ / Ση‖m̂‖ în fereastra de calibrare (pașii 1–24), împărțit la același raport pe restul sarcinii:
- R2: amazon 0,967, yahoo 0,861, agnews 0,705 (valorile din analiza (d), refăcute);
- `eta_m_A1`: 0,966, 0,903, 0,810.

(Adăugat 9 nov., ~09:10: calculul e fixat în `Stadiul0/forever_repro/drift_ratio_posthoc.py`, scris după verdict, cu ieșirea în `runs/forever_drift_ratio_posthoc.log`; dă aceleași valori.)

Deriva are același sens în ambele rulări: raportul crește după calibrare, deci η‖m̂‖ rămâne în urmă. Ordinea pe sarcini e aceeași, iar mărimea e mai mică pe agnews în brațul 1. Ipoteza „calibrarea pe 24 de pași îngheață un factor care apoi derivă” rămâne compatibilă cu două rulări, post hoc. Jurnalele brațelor τ nu înregistrează ceasul η‖m̂‖, deci acolo raportul nu se poate calcula.

**Ce se închide:** cu codul autorilor, sămânța 42, ordinea 1 din articol, deficitul pe dbpedia din R2 nu se poate atribui ceasului, iar rezultatul agregat (OP, BWT) rămâne în marja de ±2 puncte în toate trei perechile. Rămâne stabilit că η‖m̂‖ declanșează sistematic mai târziu decât τ în codul lor, cu 0–36 de pași.

**Limite:** o rulare pe celulă; o singură sămânță, deci repetările măsoară doar nedeterminismul GPU; o ordine; un model mic; decodarea stocastică a generatoarelor lor (`do_sample=True`, `temperature=0.02`).
