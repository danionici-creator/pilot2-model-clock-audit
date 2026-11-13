# Pilot 2: sinteza celor cinci opinii despre direcția de cercetare (4 nov. 2026)

**Subiect deschis.** Documentul ține starea discuției, ca să poată fi reluată oricând: ce s-a întrebat, ce au răspuns cele cinci sisteme, ce s-a verificat, ce rămâne de decis.

## 1. Ce s-a întrebat

Același rezumat al studiului și aceleași 6 întrebări de direcție (relevanța față de FOREVER, valoarea rezultatului „echivalent”, lumea sintetică îngustă față de un LM mic cu LoRA, preînregistrarea doar a Stadiului A, supra-proiectarea, un studiu mai bun), plus o recomandare finală A/B/C/D. Mesajul: `Mistral_detalii/mistral_msg_directie_v04.txt`; varianta pentru chat, cu rolul inclus: `Prompturi/Pilot2_Prompt_directie_v04_chat.txt`. Recenziile anterioare (Argon, Mistral pe v0.3, Deep Review pe v0.4) evaluaseră doar metodologia.

| Sistem | Mod | Fișier |
|---|---|---|
| Mistral Large 4 | API, reasoning low | `Recenzie_Mistral_Large4_directie_v04.md` |
| Mistral Large 4 | API, reasoning medium | `Recenzie_Mistral_Large4_directie_v04_medium.md` |
| Microsoft Copilot | Think Deeper | `Recenzie_Copilot_directie_v04.md` |
| Gemini 3.1 Pro | High | `Recenzie_Gemini_directie_v04.md` |
| ChatGPT (GPT-6) | efort High | `Recenzie_ChatGPT_directie_v04.md` |

Verificarea detaliată a celor două opinii Mistral: `Pilot2_v0.4_verificare_directie_Mistral.md`.

## 2. Referințele: toate verificate (4 nov. 2026)

Toate există (arXiv API, Crossref, Hugging Face) și descrierile lor sunt corecte:

| Referință | Citată de | Verificat |
|---|---|---|
| FOREVER, Feng et al. 2026, arXiv:2601.03938, doi:10.18653/v1/2026.acl-long.1144 | toate | ✓. Detalii confirmate în textul articolului (arXiv HTML v2): ablația „model time” față de calibrarea pe pași (+STC) aduce **+1,2% OP și +1,1% BWT**, pe un singur benchmark (SuperNI, ordinea de sarcini 7; Tabelul 2: 42,5 / −2,8 față de 41,3 / −3,9); Δ_t se obține din actualizările aplicate de optimizator, „without requiring additional forward or backward passes”; anexa B.1 extinde metoda la **fine-tuning cu toți parametrii** |
| Kalajdzievski 2024, arXiv:2401.05605 | Copilot, Mistral | ✓ uitarea crește ca lege de putere deplasată în numărul de parametri antrenați și de pași; LoRA nu o elimină |
| Jin & Ren 2024, arXiv:2402.01865 | Copilot, ChatGPT, Mistral | ✓ modelul parțial interpretabil „merge decent pe BART, dar eșuează pe T5”; reluarea exemplelor prezise reduce uitarea |
| Su & Zhang 2026, arXiv:2609.32818 | ChatGPT | ✓ modelul de ordinul întâi prezice schimbările marginilor cu r = 0,974–0,998, dar predicțiile de uitare eșuează (schimbările ies din regiunea validată) |
| **Wang et al. 2026, „Geometry Conflict”, arXiv:2605.09608** | ChatGPT | ✓ **nouă pentru proiect**: uitarea în post-antrenarea continuă a LLM explicată prin geometria (covarianța) actualizărilor, nu prin mărimea lor |
| **Farajtabar et al. 2019, OGD, arXiv:1910.07104** | ChatGPT | ✓ **nouă pentru proiect**: direcția gradientului, nu mărimea, decide interferența |
| Pythia, Biderman et al. 2023, arXiv:2304.01373 | Gemini, ChatGPT | ✓ articolul descrie 70M–12B; **pythia-14m (14,1 M parametri) și pythia-31m (30,5 M) există pe Hugging Face** (EleutherAI), adăugate ulterior; pythia-70m are 95,6 M parametri în total, cu embedding-urile |
| EWC (doi:10.1073/pnas.1611835114), SI (arXiv:1703.04200), Toneva (arXiv:1812.05159) | Copilot, Mistral | ✓ deja verificate în protocol |

Nicio referință inventată în niciuna dintre cele cinci opinii.

## 3. Comparația

| Tema | Mistral low | Mistral medium | Copilot | Gemini | ChatGPT |
|---|---|---|---|---|---|
| **Recomandarea** | C | B + braț LoRA | C | C (radical) | C |
| Doar Stadiul A preînregistrat | da | da | da („cartă” scurtă pentru B) | da | da |
| Protocolul e supra-proiectat | da | da | da | da | da |
| Articolul formulat ca audit al „ceasului centrat pe model”, separat de Perspective | da | da | **da, explicit** | da | **da, explicit** |
| Lumea sintetică rămâne | doar pilot | da, principală | da (A1, 80–120 de rulări, toate familiile) | **nu** | da, principală (3–4 regimuri, 80–120) |
| Braț pe LM preantrenat cu LoRA | da (Pythia-160m/410m) | da (Pythia-70M, 20–30) | da (12–24, model blocat) | da, ca studiu principal (~30) | da (Pythia-70M, rezervă 31M; coroborare, nu replicare) |
| Familiile de fluxuri | 2 | 3, păstrează decuplarea | toate, 2–3 contraste confirmatorii | 2 | 3–4 |
| „Scara” de competitori (cel mai mic set suficient) | — | — | **da** | da (importanța variabilelor) | **da** |
| R² de reconstrucție a lui c_e din telemetrie | da | — | — | — | da, separat |
| Contrastul „același c_e, interferență diferită” | — | (sondă cu pauze: slabă) | da (perechi; competitor direcțional) | — | **da** (Experimentul 2; OGD, Geometry Conflict) |
| Erori găsite la verificare | 2 (identitate, cost) | 1,5 (identitate atenuată, cost pe jumătate) | 1 discutabilă (scoaterea metricilor „derivate”) | 3 (identitate, 2 familii, fără GBDT) | **niciuna** |

**Calitate.** ChatGPT e cel mai solid: toate referințele și cifrele sunt exacte, face distincțiile logice corecte („echivalent” nu înseamnă „reconstructibil”; c_e e ieftin, deci un rezultat negativ nu aduce automat o economie) și propune două contraste care testează limitele ceasului, nu doar îl clasează. Copilot e pe locul doi (scara de competitori, intervențiile pereche, competitorul direcțional). Gemini e cel mai radical și repetă eroarea despre identitate; recomandările lui de a scoate arborii și de a păstra două familii contrazic lecția studiului închis și pe celelalte opinii.

## 4. Ce rezultă

**Consens (5 din 5):**
1. Preînregistrare doar pentru Stadiul A. Stadiul B primește un protocol separat, cu semințe noi, depus înainte de orice rulare B.
2. Protocol mult mai scurt (~5 secțiuni substanțiale sau ~10 pagini), cu detaliile tehnice și jurnalele în anexă.
3. Formularea: un audit empiric al „ceasului centrat pe model” (FOREVER), ținut separat de Perspective. Un rezultat negativ nu infirmă Perspective, iar unul pozitiv nu validează „timpul experiențial”.
4. O componentă mică pe un LM preantrenat cu LoRA, cu buget fixat după o măsurătoare de timp. Se raportează ca verificare de transport sau coroborare, nu ca replicare cu putere completă.

**Majoritate (3–4 din 5):**
5. Lumea sintetică rămâne testul principal controlat (Mistral medium, Copilot, ChatGPT), cu 3–4 familii, nu 6.
6. **Scara de competitori**: c_e adăugat peste fiecare treaptă (pași; + Σ η; + pierdere; set minim al optimizatorului; B_strong); întrebarea centrală devine „care e cel mai mic set ieftin care îl înlocuiește?” (Copilot, Gemini, ChatGPT).
7. **Contrastul de interferență**: același c_e, uitare diferită (Copilot, ChatGPT). Fluxul F6 („multă schimbare, puțină interferență”) e deja acest contrast; trebuie urcat de la „verificare” la contrast principal.

**Respinse după verificare:** abandonarea lumii sintetice (Gemini; 1 din 5 explicit); doar două familii (Gemini, Mistral low); scoaterea arborilor sau a acordării hiperparametrilor (Gemini, Mistral medium: un baseline neacordat fabrică avantaje, lecția studiului închis); sonda cu pauze (Mistral medium).

## 5. Recomandarea mea (de discutat)

Un **Stadiu A restructurat**, mai mic și mai discriminant:
- **Lumea sintetică**, 4 familii: F1 (control natural), F2 și F3 (decuplarea pașilor de schimbare), F6 (interferență mică la schimbare mare); numărul de rulări din analiza de putere (probabil 100–150, nu 315).
- **Trei mărimi principale:** (a) cât de bine se reconstruiește rata lui c_e din telemetrie (G2 urcat la rezultat); (b) scara de competitori, cu două trepte confirmatorii fixate dinainte (setul minim și B_strong), restul descriptiv; (c) contrastul de interferență pe F6.
- **Modul de transport:** Pythia-70M (sau 31M) cu LoRA, câteva regimuri, model blocat, descriptiv; doar dacă măsurătoarea de timp îl face fezabil și dacă modelul chiar învață și uită faptele.
- **Stadiul B:** doar o „cartă” de o pagină.
- **Corecturile verificate din Deep Review** rămân valabile (cod: context 4, embedding-uri fără weight decay, q_hist înainte de segment, L_clip, C0 ca ticuri de pauză, C10c; text: 0a/0b, G5 cu C1, G4b reparat, σ²_train, §15).

## 6. Pașii următori (neschimbați, ambii orbi față de relația c_e–T1)

1. **G2 pe tech3:** R² al ratei lui c_e prezise din telemetrie, pentru D1, D1_rel, D2, D3. Câteva minute. Dacă e ≥ 0,99, întrebarea e practic închisă (criteriul Mistral).
2. **Măsurătoarea de timp Pythia-70M / 31M cu LoRA pe CPU.** Cere acordul pentru descărcare (~60–200 MB); `transformers` e instalat, iar LoRA se poate scrie fără `peft`.
3. După ele: decizia de formă, apoi v0.5 (jurnal §22), codul, runda tehnică F1–F6 și memoria. Calibrarea vine la urmă.

**Decizii deschise ale autorului:** forma Stadiului A (§5); 0a/0b; bugetul Q (relevant doar dacă Stadiul B revine); embedding-urile fără weight decay.
