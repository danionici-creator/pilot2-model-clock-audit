# Pilot 2: deciziile deschise, cu datele din 6 noiembrie (pregătit pentru utilizator)

Fiecare decizie are opțiunile, recomandarea mea și dovezile. Nimic din ce urmează nu e aplicat definitiv; ce e aplicat provizoriu e spus explicit. Detaliile tehnice: `Stadiul0\Stadiul0_note_lucru.md` §12–§15.

## Ce s-a aflat pe 6 nov. (pe scurt)

1. **Ceasul pe distanța parametrilor e reconstructibil din telemetria optimizatorului, peste tot unde l-am măsurat.** Un singur scalar, Ση‖m̂‖, reconstruiește rata lui D1 cu R² 0,86–0,96 și pe cea a lui D2 cu 0,98–0,99, chiar pe o familie nevăzută la antrenare. Același lucru e valabil pe Qwen3-0.6B în programul FOREVER: 0,94–0,95, iar cu toată telemetria 0,976–0,986.
2. **Predicția din 4 nov. („în setarea FOREVER, programul ratei Ση explică cea mai mare parte din τ”) a picat:** R² 0,58–0,67. Nu programul ratei, ci momentul optimizatorului face treaba. La nivel de fază, R² aparent de 0,99 e un artefact al duratei (pașii singuri dau la fel).
3. **D3 (distanța funcțională) nu mai e „singurul candidat cu informație proprie”:** noul competitor C10c, de același cost, îl reconstruiește cu 0,95–0,99 în F2, F3, F5. **Excepția e F6** (distractori cu zgomot): acolo niciun scalar nu ajunge (C10c 0,59, Ση‖m̂‖ 0,18).
4. **Brațul LM funcționează:** determinist bit cu bit, ~15 min pe rulare de 10 sarcini. „Eșecul de învățare” de la ultimele sarcini vine din repetiția finală FOREVER: înainte de ea, acuratețea e 1,000 la toate sarcinile.
5. **Debitul real în Turbo:** 12,3 rulări pe oră pe CPU (4 procese), față de 9,5 măsurat înainte.

## Deciziile

| # | Decizia | Opțiuni | Recomandarea mea | De ce |
|---|---|---|---|---|
| 1 | **Forma Stadiului A** | (B) lumea sintetică principală + modul LM descriptiv; (C) doar un studiu mic pe LM; (R) Stadiul A restructurat | **R:** 4 familii (F1, F2, F3, F6); rezultatul principal = reconstrucția (G2 urcat la rezultat) pentru toți candidații D, cu scara de competitori care include C10c; H1 confirmatorie doar unde mai e loc (D3 față de C10c, contrastul F6); modulul LM descriptiv | Pentru D1, D1_rel și D2 răspunsul e practic cunoscut („echivalent”/„reconstructibil”); a-l preînregistra ca test H1 cheltuie timp pe o întrebare închisă. Locul unde se poate vedea ceva nou e F6. |
| 2 | **Stadiul 0 împărțit în 0a/0b** (Deep Review B1) | da / regula veche despre c_e | **da** | Singura soluție curată la conflictul cu §12a; 0a e orbă față de relația c_e–T1. |
| 3 | **Bugetul Q și Stadiul B** | K_reh = 32 acum / Stadiul B amânat | **Stadiul B amânat** (doar o „cartă” de o pagină) | Cu D1/D2 reconstructibili, un declanșator de repetiții pe c_e nu poate bate un declanșator pe Ση‖m̂‖; Q nu mai trebuie fixat acum. |
| 4 | **Embedding-urile fără weight decay** (Deep Review D3) | complet / doar rândurile nefolosite / deloc | **complet** (aplicat deja provizoriu în cod) | Copilăria trece în 6 din 6 (0,982–0,985); codul e mai simplu; verificat că rândurile nefolosite nu se mai mișcă. |
| 5 | **Criteriul de învățare al brațului LM** (nou) | după repetiția finală (cum era) / înainte de ea | **înainte**; valoarea de după se raportează | Diagnosticul arată că repetiția finală e cea care scade acuratețea; e o proprietate a programului FOREVER, nu o învățare slabă. |
| 6 | **Precizia brațului LM** (nou) | fp16 cu GradScaler (ca FOREVER; 4–6% pași săriți) / bf16 | **fp16** ca setare principală, bf16 ca sensibilitate | Auditul e „în setarea lor”; rezultatul bf16 vine diseară (lanțul 2). |
| 7 | **C10c în scara lui D3** (nou) | obligatoriu / opțional | **obligatoriu** | Fără el, D3 ar părea că are informație proprie doar fiindcă îi lipsește competitorul de același cost. |
| 8 | **O notă scurtă despre ceasul FOREVER** (nou, opțional) | acum / după Pilot 2 / deloc | **de discutat** | Rezultatele brațului LM sunt aproape complete și descriptive; o notă tehnică separată (fără pretenție confirmatorie) ar ieși repede. Riscul: e o comunicare înainte de preînregistrarea Stadiului A, deci trebuie spus clar că e exploratorie. |

## Estimările de timp, cu debitul măsurat

| Etapa | Calcul | Muncă |
|---|---|---|
| v0.5 (după deciziile 1–4 și 7) | — | 5–7 h (mai scurt dacă forma R se adoptă) |
| Semințele hash-uite, scriptul 0b | — | ~1 h |
| Calibrarea 0a → 0b (24 de rulări) | **~2 h** CPU (12,3 rulări pe oră) | ~1 h |
| Raportul Stadiului 0, înghețarea, preînregistrarea | — | 4–6 h |
| Stadiul A, 100–150 de rulări | **~8–12 h** CPU (o noapte) | supraveghere |
| Modulul LM, 20–30 de rulări | **~5–7,5 h** GPU (poate rula în paralel cu CPU, de verificat) | ~2 h |
| Analiza și scrierea | ~1 h | 4–6 zile |

**Ce fac în lipsa deciziilor:** doar runde tehnice (lanțul 2 diseară), fără calibrare, fără Stadiul A, fără publicări.
