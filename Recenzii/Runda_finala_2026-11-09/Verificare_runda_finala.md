# Runda finală: verificarea punct cu punct

Regula aplicată: `Regula_de_adoptare_2026-11-09.md`. Răspunsurile, exact cum au venit, sunt în `Raspunsuri/`: CMU în
Markdown, luate de la serverul serviciului; Stanford în text, copiat din pagina de evaluare; faza 2 în fișierele
`Faza2_*`, cu antetul care spune cum a fost luat fiecare. Fiecare afirmație e verificată în PDF-urile trimise, în sursele
raportului și ale Perspective, în jurnale sau la sursa citată.

**Prescurtări:** R = raportul de închidere; P = ciorna Perspective v1.4. CMU1/CMU2 și S1/S2 sunt cele patru evaluări din
faza 1.

## Faza 1 (CMU Paper Reviewer, Stanford Agentic Reviewer), 9 nov. 2026

### Afirmații de fapt despre documentele noastre

| Punct | Afirmația | Verificarea | Verdict |
|---|---|---|---|
| CMU2-4 | În P, §4, definiția indicelui ar fi „c_a(t) = Σ_{τ=t} …”, iar ρ = Δc_s/Δc_s ar fi identic cu 1 | Textul extras din PDF (pypdf): „ce(t) = Σ τ<t D(S(τ), S(τ+1))” și „ρ = Δ ce/Δca”; sursa (`persp_content.js`): `{i|c}_{e}({i|t}) = Σ_{τ<t}` și `Δ{i|c}_{e}/Δ{i|c}_{a}`. Evaluatorul a citit greșit indicii, prin OCR | **Fals**, eliminat. Nicio corectură |
| CMU1-4 | Pachetul trimis reproduce doar 6 din 19 analize; lipsesc fișierele `.npz` și `.parquet` | Adevărat pentru pachetul primit: zip-ul de cod nu conține partea de date (665 MB, peste limita serviciului), iar R spune explicit că reproducerea cere partea de date dezarhivată | **Adevărat, dar nu e o eroare a lui R**. O îmbunătățire utilă e notată la O4 |
| S1 | „no formal TOST equivalence tests are reported” | La T-A și S2, echivalența se declară când intervalul de încredere pereche de 95% e cuprins în marjă. Asta echivalează formal cu un TOST la α = 0,025 pe fiecare parte (mai strict decât TOST-ul uzual la 0,05, care corespunde intervalului de 90%). R nu folosește denumirea „TOST” | **Parțial fals.** Se poate preciza în R (O3) |
| S2 | Lipsesc lucrări înrudite (8 identificatori arXiv) | Toate 8 există (API-ul arXiv). Cinci sunt deja citate în P: 2608.29381 (`wu2026resume`), 2511.13641 (`burke2026`), 2609.00546 (`zhao2026enoch`), 2607.17328 (`sayadi2026ptlp`), 2606.30306 (sondajul Ding et al.). Necitate: CRISP (2408.06822), atacurile prin clonare pe SGX (2601.09273), repararea prin rollback ghidată de dependențe (2608.10502). S2 a analizat doar primele 15 pagini, fără bibliografie | **Parțial fals** (5 din 8 sunt citate). Trei adăugiri posibile, discutate la O11 |
| CMU1, CMU2: referințele citate | Lakens 2017; Dodge et al. 2020 (2002.06305); Bouthillier et al. 2021 (2103.03098); Bell & Lawrence 2022 (2205.13323); Pineau et al. 2021 (JMLR); Lakens, Scheel & Isager 2018; Matetic et al. 2017 (ROTE); Geirhos et al. 2020; Kingma & Ba (1412.6980); Pruthi et al. 2020 | Identificatorii arXiv există, cu titlurile și autorii indicați. ROTE și Geirhos sunt deja citate în P | **Corecte** |
| TracIn (R, referințe) | CMU2 dă ordinea autorilor „Pruthi, Liu, Kale, Sundararajan” (NeurIPS); arXiv dă „Pruthi, Liu, Sundararajan, Kale” | R folosește ordinea de pe arXiv și eticheta NeurIPS 2020. Proceedings-ul NeurIPS și dblp nu au răspuns azi | **De verificat la publicare** (Crossref). Nu e o eroare confirmată |

**Rezultatul fazei 1 pentru corecturile dintre faze:** nicio eroare de fapt confirmată în R sau în P și niciun punct
fatal (evaluatorii nu au marcat niciunul, iar verificarea nu a găsit vreunul). Documentele trimise în faza 2 rămân deci
cele din faza 1, cu amprentele fixate la 11:53.

### Obiecții de interpretare și de domeniu (se adoptă după faza 2, după regulă: cel puțin 2 din 7 evaluatori, după verificare)

| Cod | Obiecția | Cine o ridică | Verificarea | Stare după faza 1 |
|---|---|---|---|---|
| O1 | Concluzia negativă e formulată mai tare decât s-a testat. H1 nu a fost rulat, deci „neidentificabil” nu înseamnă „răspuns negativ”; limbajul „closed” depășește domeniul testat | CMU1-1, CMU1-5, CMU2-2, CMU2-3 (S1 notează aceeași limită, fără să ceară o schimbare) | **Adevărat**. R §6: „the open question is answered negatively for the candidates tested”. R, rezumat: „is closed in this framework as a documented negative result”. P, M6: „the open question is answered negatively”. Asta contrazice principiul 2 din propunerea v1.4 („neidentificabil”, nu „închis”) | **2 evaluatori: prag atins.** Propunere: „answered negatively” devine „not identifiable / found no basis to proceed”; ultima frază a rezumatului din R se restrânge (textul sugerat de CMU1-5 e un punct de plecare) |
| O2 | Comparațiile de planificare au putere mică și sunt confundate cu alți factori: codul autorilor cu o singură rulare pe celulă, o singură ordine, decodare stocastică | CMU1-2, CMU2-3, S1 | **Adevărat**, iar R declară toate limitele. Problema e tăria formulării „no measurable advantage” și „in aggregate” pentru codul autorilor | **3 evaluatori.** Propunere: pentru codul autorilor, „inconclusive beyond the observed runs; no consistent difference”, în loc de orice sugestie de echivalență |
| O3 | Marjele (±2 puncte, ±5%) nu sunt justificate ca cel mai mic efect relevant (SESOI) și lipsește o analiză a puterii | CMU1-3, CMU2-3, S1 | **Adevărat**: preînregistrările fixează marjele fără justificare explicită | **3 evaluatori.** Propunere: o propoziție de justificare (sau declarația că marjele sunt convenții), precizarea că testul prin interval de 95% e un TOST la 0,025 și un calcul simplu de sensibilitate (lățimea intervalelor observate) |
| O4 | Reproductibilitatea nu se poate verifica din materialele primite; preînregistrarea e locală; două versiuni de cod nu s-au păstrat; DOI-ul încă nu există | CMU1-4, CMU2-2, S1 | **Adevărat** pentru stadiul de dinaintea publicării; toate sunt declarate în R | **3 evaluatori.** Propunere: `reproduce_analyses.py` să verifice întâi fișierele necesare și să le listeze pe cele lipsă; P să citeze [24] doar cu DOI (deja în plan); limita preînregistrării locale rămâne declarată |
| O5 | O analiză exploratorie a reziduului: ajută reziduul ceasului după reconstrucție la prezicerea uitării? | CMU1-1 (acțiunea propusă) | Fezabilă: țintele de uitare T1 există, dar n-au fost deschise niciodată, conform preînregistrării. Deschiderea lor ar fi o analiză post hoc, nouă | 1 evaluator. **Decizia autorului** |
| O6 | Ambele ceasuri înregistrate în aceleași rulări τ ale codului autorilor, pentru mecanismul întârzierii | S1 | Adevărat: rulările τ nu înregistrează ceasul η‖m̂‖ (R §5.1) | 1 evaluator. Ar cere rulări noi pe GPU |
| O7 | Alți optimizatori (SGD, Adafactor); rezultatul e specific lui Adam | S1, CMU2-2 | Adevărat. R, „Not closed” (ii) spune deja „other optimizers” | 2 evaluatori, dar R o spune deja. Eventual o precizare în rezumat |
| O8 | Partea despre proces (colocviile AI) distrage de la miezul științific | S1 | Opinie | 1 evaluator. Decizia autorului |
| O9 | P: lipsesc contractele de evaluare și un prototip pentru nivelul 4, deci partea distinctivă nu e testată | CMU2-1, S2 | **Adevărat**: P spune „No such contract is provided here”, iar M12 spune că testele ancorei sunt oferite altora | **2 evaluatori.** Propunere: o propoziție care numește explicit un contract minim pentru nivelul 4 drept următorul pas |
| O10 | P: afirmația că perechea (c_a, N) e „necessary and sufficient” e prea largă (furcarea înainte de concurența pe contor, agenți cu mai multe procese, consistența la prăbușire) | CMU2-5, S2 | **Adevărat ca formulare.** P recunoaște mai jos furcarea și clonarea. Contraexemplul CMU2 („restaurare fără niciun pas ulterior = suspendare”) nu e o eroare: P definește restaurarea prin funcționarea de după salvare | **2 evaluatori.** Propunere: „sufficient under the stated assumptions for the freshness of one lineage”, cu limitele scrise lângă, nu mai jos (textul sugerat de CMU2-5 e un punct de plecare) |
| O11 | P: alte lucrări înrudite | S2 | 3 din 8 lipsesc (vezi mai sus). Furcarea (2601.09273) se leagă de O10 | 1 evaluator. Decizia autorului; 2601.09273 se potrivește cu O10 |
| O12 | P: separarea istoriei acumulate de telemetrie cere un exemplu pozitiv | CMU2-6 | E chiar concluzia lui P (nivelul 2 rămâne o definiție) | 1 evaluator. Fără schimbare |

### Opțiunile deschise (D1, D3, D6)

Evaluatorii automați nu au primit întrebările noastre. Singurul semnal: S2 numește ieșirea prin neidentificabilitate „a
principled ‘not identifiable’ exit” (pentru D3: păstrarea amendamentului). Niciun evaluator nu comentează lungimea
rezumatului P (D1) și nici M16/M17 (D6).

### Ce urmează

Faza 2: aceleași PDF-uri și același prompt (`Prompt_analiza_EN.txt`) la DeepSeek, GLM, Mistral, ChatGPT și Gemini,
trimise toate înainte să citesc vreun răspuns. După faza 2: numărătoarea finală pentru O1–O12, apoi corecturile, cu
acordul autorului.

## Faza 2 (DeepSeek, GLM, Mistral, ChatGPT, Gemini, Deep Review), 9 nov. 2026

Răspunsurile: `Raspunsuri/Faza2_DeepSeek.txt`, `Faza2_GLM.md`, `Faza2_Mistral_LeChat.txt`, `Faza2_ChatGPT.txt`,
`Faza2_Gemini.txt`, `Faza2_DeepReview.md`. Toate șase au fost trimise înainte să fie citit vreun răspuns din faza 2
(`Trimiteri_faza2.md`). Niciun document nu a fost schimbat între faze.

**Prescurtări.** DS = DeepSeek, GLM = Z.AI GLM-5.3, MI = Mistral Le Chat, GPT = ChatGPT, GEM = Gemini, DR = Deep Review.
Un punct e numit după numărul lui din răspuns (GPT-1 = constatarea 1 a ChatGPT; DS-A1 = răspunsul lui DeepSeek la A1).
La Deep Review, care își împarte raportul pe segmente: DR-A = raportul §1–4, DR-B = raportul §5–10, DR-C = Perspective
§1–3, DR-D = Perspective §4–6, DR-E = Perspective §7–8. Evaluatorii care se numără sunt opt: CMU, Stanford (S) și cei șase
de mai sus.

### Afirmații de fapt despre documentele noastre

| Punct | Afirmația | Verificarea | Verdict |
|---|---|---|---|
| GPT-1 | R §5.2 (R2): uitarea pe dbpedia e atribuită invers | `runs/forever_repetari_verdict.json`: `dbpedia_forgetting` −4,81 pentru τ, −9,89 pentru Ση‖m̂‖. R scrie „in τ's favour (its forgetting −9.9 against −4.8)” | **Adevărat: eroare de fapt.** Se corectează |
| MI-2, MI-3, GPT-2, GLM-11, DR-D4 (și slăbiciunea 2 din rezumatul DR) | P spune că toți candidații au fost reconstruiți „from free optimizer telemetry”. D3 a fost reconstruit din concurenți de același cost (C10c, pe aceleași treceri înainte), nu din telemetria optimizatorului | Formularea apare în rândul „Changes”, în rezumat, în caseta „What this perspective offers” și, ca „from free telemetry”, în a doua precauție din §6. Concluzia spune „the statistics the optimizer already keeps”. P §4 și R spun corect „cheap telemetry or same-cost competitors” | **Adevărat** (4 evaluatori). Se corectează în toate locurile |
| MI-12, GLM-16, DR-D4 | Tabelul 2, nivelul 2: poarta „from the optimizer's state” nu acoperă concurenții de același cost; §5 spune corect „the competitor's own inputs” | Adevărat | **Adevărat.** Se aliniază la §5 |
| DR-B6 | R §6 citează „(Ionici 2026c, v1.4)”, dar lista de referințe are doar v1.3 | Adevărat | **Eroare de fapt** (minoră). Se adaugă intrarea v1.4 |
| GLM-13 | Fraza din P §4 („In a synthetic … world and in a 0.6-billion-parameter language model …, three parameter-space distances, a functional distance …, and the update-norm clock itself were each reconstructed”) sugerează că toți cinci au fost testați în ambele cadre | R §5.1: D1, D1_rel și D2 doar în lumea sintetică; pe modelul de limbaj τ (portul, SuperNI, codul autorilor) și D3 (T-C) | **Adevărat**: o formulare care sugerează un fapt fals. Se reformulează |
| GLM-14 | Nota de sub Tabelul 2, „tested … since version 1.2”, e confuză | Pilot 2 a început pe 27 oct., când v1.2 era curentă; v1.3 a apărut pe 1 nov. (`Lucrari_publicate.md`). Nu e falsă, dar se citește ca și cum testarea ar fi avut loc în v1.2 | **Adevărat ca formulare.** Se scoate trimiterea la versiune |
| DR-E (corecturi minore) | P: referința [3] (Benzing) nu are identificatorul arXiv; [72] (Zenke) nu are paginile | Propunerea, M16: `benzing2022` fără arXiv:2006.06357; `zenke2017` fără pagini. Paginile sunt PMLR 70:3987–3995 (verificat azi pe proceedings.mlr.press) | **Adevărat.** Se completează |
| GPT-5 (FATAL), CMU2-5, S2 (O10), DR-D3 | P §4, ancora de continuitate: cele trei cazuri și „necessary and sufficient” | Textul (din v1.3, neschimbat în v1.4) spune: „If N exceeds N(t0) … has been restored; if N equals N(t0) while c_a has advanced …, it has been suspended; if both have advanced together, it has operated without interruption.” Primul și al treilea caz se suprapun, pentru că N > N(t0) apare în ambele. Textul amestecă două comparații: valorile sigilate din starea încărcată cu valorile vii (schița de protocol face corect asta) și valorile de la t0 cu cele de acum, de-a lungul aceleiași linii. Un agent pornit care nu consemnează niciun pas arată la fel ca unul suspendat. Caracterul „necessary” nu e argumentat. Punctul 1 al DR-D3 (căderea între incrementarea contorului și salvare) e deja tratat în același paragraf („commits must be crash-consistent …”) | **Adevărat: defect logic într-o afirmație centrală, prezent deja în v1.3.** Corectura e locală. Marcat FATAL de ChatGPT și confirmat, deci, după regula 4, nicio intrare Zenodo nu se publică înainte de corectură |
| MI-4 | „16 of 17 comparable triggers” nu ar rezulta din tabel | Perechea A are 8 declanșări comparabile (Ση‖m̂‖ nu atinge al patrulea prag pe agnews), toate mai târziu. Perechea B are 9: 8 mai târziu, una la același pas (agnews, pasul 47). Total 17, din care 16 mai târziu. DR face corect același calcul | **Fals.** E utilă doar precizarea regulii de numărare (N9) |
| MI-7 | FOREVER: câștigul în BWT al ablației ar fi 0,9, nu 1,1 | Articolul, în arXiv v2 și în PDF-ul ACL, §3.2.2: „average improvement of 1.2% in OP and 1.1% in BWT”; Tabelul 2: −2,8 față de −3,9. Cifra 0,9 e din §3.2.1 și compară FOREVER cu VBM, nu cu calibrarea pe pași. GLM a verificat tabelul la fel | **Fals:** evaluatorul a confundat două comparații |
| MI-10, GLM-6, DR-B (corecturi minore, 3) | Diferențele −0,51, +3,29 și +5,33 nu se obțin din cifrele tabelului | În JSON: D_A1 = −0,514, D_B1 = +3,286, dbpedia R1 − R2 = 5,329. Textul e corect; tabelul arată valori rotunjite | **Nu e eroare.** Se adaugă precizarea că diferențele sunt calculate din valorile nerotunjite (3 evaluatori) |
| MI-11 | Notația m̄ / m̃; „Stadiu10” | Sursa folosește doar m̂ (29 de apariții, niciun m̄ sau m̃), iar „Stadiul0” e scris corect | **Fals** (OCR). Sunt adevărate doar două mărunțișuri: „313 steps” nu e explicat (fiecare sarcină 1–3 are 313 pași în jurnale), iar tech2–tech4 apar înainte să fie definite |
| MI-13 | ρ = Δc_a/Δc_a | Ca la CMU2-4 din faza 1 | **Fals** (OCR) |
| DS-A1 | Valorile D1_rel 0,74 (F3) și 0,82 (F6) și D3 0,80 (F6) nu ar fi excepții de extrapolare | R §5.1, T-D (2): „With the mechanism of the test family left out of training”. Sunt chiar excepții de extrapolare | **Fals.** Întrebarea legată de el (de ce nu deschid H1) e utilă (N8) |
| DS-A3 | Reconstrucția ar fi parțial tautologică, pentru că fiecare candidat e o funcție de telemetrie | τ nu e o funcție algebrică de scalarii jurnalizați, fiindcă depinde de v̂ pe fiecare coordonată. T-D (1): fără statisticile proprii ale lui D1 (C6), rezultatul nu se schimbă. D3 se compară cu concurenți de același cost | **În mare parte fals** |
| DR-D2 (B2) | Poarta de reconstrucție ar fi existat deja în Tabelul 2 | În v1.3 (`persp_content.js`), Tabelul 2 are la nivelul 2 „Must beat decoders restricted to within-episode update statistics …”. Poarta de reconstrucție intră în P abia în v1.4. Proveniența corectă e protocolul Pilot 2 v0.4, scris înainte de rulări: el fixează G2 și rezultatul „H1 is reported as *not identifiable*, never as equivalence” (`Pilot2_Protocol_EN_draft.md`, tabelul porților) | **Fals pentru P.** Fraza propusă de DR nu se preia; se folosește proveniența din protocol (N14) |
| DR-B (corecturi minore, 4) | Cele 2 fișiere din 13 ar fi cele două versiuni de cod nepăstrate | `verify_hash_lists.py`, lista LOST: `lm_forever_run.py` al rulărilor lmtech1 și lmtech2 (una dintre cele două versiuni nepăstrate) și `td_audit.py` v1 (OLS nescalat, înlocuit după un minut; ieșirea lui e arhivată). Codul rundelor tehnice din 4 nov. nu figurează în listele de amprente | **Parțial fals.** Cele două fișiere se numesc în R (N11) |
| DR, verificarea citărilor | Referința [24] (raportul Pilot 2) ar fi „likely hallucinated” | Raportul e o ciornă nepublicată, iar DOI-ul se rezervă la publicare | **Fals pe fond.** Rezultatul era de așteptat înainte de publicare |
| MI-16, GLM (nota de verificare) | Citatul din Liu et al., „usually around 0.2 to 0.4”, nu a putut fi găsit | arXiv:2502.16982, §2.2: „From empirical observations, AdamW's update RMS is usually around 0.2 to 0.4.” | **Citatul e corect** |
| DR-A2 | Portul ar păstra o singură stare AdamW și o singură planificare a ratei pe toată sarcina, fără repornirile din codul autorilor | `lm/lm_forever_run.py`, funcția `phase` (rândurile 168–173): la fiecare fază se creează un AdamW nou, o planificare nouă cu încălzire și un GradScaler nou (în configurațiile fp16), exact ca în codul autorilor. Continuu rămâne doar fluxul de date. R §4 nu spune explicit acest lucru | **Fals.** E utilă precizarea în R §4 (N7) |
| GPT-10 | R ar confunda reconstrucția din starea completă a optimizatorului cu cea dintr-un singur scalar | R §6: „Whether one cheap scalar still suffices is open” | **Parțial fals.** Rămâne adevărat că §2 comprimă formula (N5) |

### Mecanismul întârzierii: verificarea în jurnale (MI-9, GPT-9, DS-A2, GLM-A2, DR-B2)

Cinci evaluatori au propus aceeași explicație: întârzierea lui Ση‖m̂‖ în codul autorilor ar putea fi un artefact al
pașilor săriți de GradScaler, pe care Δθ = 0 dar ceasul liber avansează. Am verificat-o.

**Ce face codul.** `make_clock_variant.py` adună la sfârșitul fiecărui pas rata × ‖m̂‖, citite din starea AdamW. Pe un pas
sărit, starea nu se schimbă, deci ceasul ar adăuga momentul pasului anterior. La primul pas al unei faze, starea e goală
și ceasul adaugă 0.

**Ce arată jurnalele.** Am verificat jurnalele de derivă ale celor două rulări η‖m̂‖ (`Verificari_faza2/skip_check.py`,
ieșirea în `skip_check_output.txt`; amprentele sunt mai jos).
- Δθ = 0 apare la primul pas al fiecărei faze (pasul 1, pasul 25 și pasul de după fiecare declanșare). Acolo ceasul
  adaugă 0.
- Mai apare la încă 3 pași din 6 × 313. Acolo ceasul avansează, dar contribuția lor e de cel mult 0,3% din ceasul de după
  calibrare și de 1,9% dintr-o singură fereastră de calibrare (A1, agnews).
- Întârzierile observate ajung la 36 de pași la al patrulea prag, adică aproximativ 19%.

**Concluzie.** Pașii săriți nu explică întârzierea. Nici repornirea AdamW, a planificării ratei și a GradScaler la fiecare
fază nu o poate explica singură: portul nostru repornește și el toate trei la fiecare fază (rândul DR-A2 de mai sus), iar
acolo declanșările au coincis.

**Ce rămâne neverificat.** Diferențele care rămân între cele două implementări:
- încărcătorul de date pornit de la început la fiecare fază, față de un flux continuu;
- fp16 cu GradScaler, față de bf16 în T-A și S2;
- acumularea 4 × 8, față de un lot de 32;
- pierderea pe toată secvența, față de pierderea pe tokenul răspunsului;
- detaliile clasei Trainer.

Toate au fost schimbate împreună, deci nu se pot separa. Asta e în acord cu nota 7 din R, care spune deja că originea nu a
fost stabilită.

Aceasta e o verificare făcută pentru rundă, post hoc. Nu face parte din cele 19 analize. Amprente:
`skip_check.py` d360afe8…cb44, `skip_check_output.txt` 0259ef88…178f.

### Obiecții de interpretare, de domeniu și de formulare: numărătoarea finală

Prag: cel puțin 2 din 8 evaluatori, după verificare.

| Cod | Obiecția | Cine o ridică | Câți | Decizia după regulă |
|---|---|---|---|---|
| O1 | „Closed … as a documented negative result” (R) și „answered negatively” (P) spun mai mult decât s-a testat: H1 nu a fost rulat, deci rezultatul e „not identifiable”, nu negativ | CMU, DS, GLM, MI, GPT-4 (FATAL), GEM-1 (FATAL), DR | 7 | **Se adoptă.** Cele două marcaje FATAL sunt confirmate ca formulare excesivă: publicarea așteaptă corectura (regula 4) |
| O1b | P, concluzia: „proved sufficient” | DS, GLM, MI, GPT, GEM, DR | 6 | **Se adoptă** |
| O1c | Trebuie despărțite H1 (neidentificabil) și planificarea replay-ului, care a fost testată direct | GPT-4, DR-D1, MI-B2 | 3 | **Se adoptă** |
| O2 | Codul autorilor: rezultatele de planificare sunt neconcludente la nivel de sarcină, iar marja e descriptivă; „in aggregate” trebuie să apară și în rezumatul P | CMU, S, GPT-8, GLM (A3, B4), DR-B3, MI-B4 | 6 | **Se adoptă** |
| O3 | Marjele nu sunt justificate (SESOI); testul prin interval de 95% e un TOST la 0,025 | CMU, S, GPT-8 | 3 | **Se adoptă** (cum s-a propus după faza 1) |
| O4 | Preregistrarea e locală, iar testele formează o succesiune adaptivă; arhiva trebuie publicată odată cu raportul | CMU, S, GPT-14, MI-15, DR-A3, GLM-B2 | 6 | **Se adoptă:** „preregistered locally (hashed, not deposited)”; T-C și T-D numite drept criterii fixate înainte de calcul pe rulări existente; schimbările din v1–v3 ale preînregistrării etapei 1, într-o frază |
| O5 + rezidual | G2 e un prag operațional, nu o dovadă că restul de varianță (până la 10%, ≤ 1% în T-B) nu spune nimic despre uitare | CMU (O5), MI-6, GPT-6, GEM-2, GLM-5, DR-B5 | 6 | **Se adoptă formularea.** Analiza reziduului (deschiderea țintelor T1) rămâne **decizia autorului** |
| O6 + N7 | Mecanismul întârzierii: candidați necontrolați (repornirile pe faze, GradScaler, abaterile portului) | S, MI-9, GPT-9, DS-A2, GLM-A2, DR-A2, DR-B2 | 7 | **Se adoptă formularea:** cauzele candidate care rămân sunt numite în nota 7; se adaugă rezultatul verificării pașilor săriți și precizarea că portul repornește și el optimizatorul la fiecare fază. Rulările noi pe GPU (ambele ceasuri în aceleași rulări) rămân **decizia autorului** |
| O7 | Rezultatul e specific lui Adam | S, CMU, GPT-B3 | 3 | **Se adoptă minimal:** „with Adam” în rezumatul R |
| O8 | Partea despre proces distrage | S | 1 | Fără schimbare |
| O9 | Nivelul 4: lipsesc contractul minim și motivul pentru care un canal ar ceda | CMU, S, GPT-12 | 3 | **Se adoptă:** o frază care numește contractul minim drept pasul următor. Detaliul canalelor (GPT-12) rămâne decizia autorului |
| O10 | Ancora de continuitate: „necessary and sufficient” și cazurile care se suprapun | CMU, S, GPT-5, DR-D3 | 4 | **Se adoptă**, împreună cu corectura de fapt de mai sus |
| O11 | Alte lucrări înrudite | S | 1 | Decizia autorului |
| O12 | Lipsește un exemplu pozitiv | CMU | 1 | Fără schimbare |
| N1 | T-A e la podea (memorie de 16 fapte din 512), iar în port declanșările τ și Ση‖m̂‖ coincid, deci comparația lor testează puțin | MI-8, GEM-3, GLM-2, DR-B4, GPT-A2 | 5 | **Se adoptă:** precizarea intră în rezumatul R, în §6 și în P. Analiza retenției pe faptele din memorie (DR) rămâne **decizia autorului** |
| N2 | Zgomotul evaluării nu e cuantificat, dar verdictele se citesc față de el | MI-5, GLM-3, DR-B3, GPT-9 | 4 | **Se adoptă formularea.** Reevaluarea adaptoarelor salvate (GPU, doar inferență) rămâne **decizia autorului** |
| N3 | Reconstrucția cere date din același regim; transferul între familii e limitat; „artefact” e prea tare | GPT-7, MI-6, DS-A2, DR-B5 | 4 | **Se adoptă** |
| N4 | β se calculează tot din ‖Δθ‖, deci schimbarea ceasului nu elimină copia parametrilor din FOREVER | DR-B1, GPT-A3 | 2 | **Verificat în cod.** În port: „beta stays tau-based in every arm” (`lm_forever_run.py`). În varianta codului autorilor: „mu still uses delta_t”. **Se adoptă** (R §4 și §5.3) |
| N5 | §2 comprimă formula lui Adam (precondiționarea pe coordonate; v̄ nedefinit) | DR-A1, GPT-10, GLM-8 | 3 | **Se adoptă** |
| N6 | Reproducerea, în rezumat: o rulare pe o ordine, față de media pe trei ordini din articol | GPT-3, GLM-7 | 2 | **Se adoptă** |
| N8 | Trebuie spus de ce valorile obținute cu familia lăsată afară nu deschid H1: G2 e definit prin validare încrucișată pe rulările de calibrare, în aceleași familii | DS (prioritatea 3), DR-B5 | 2 | **Se adoptă:** o frază, cu trimitere la protocolul v0.4 |
| N9 | Regula de numărare pentru „16 of 17”; 33 față de 36 de pași | MI-4, DR-B (corecturi minore 1–2) | 2 | **Se adoptă** (precizare) |
| N10 | Diferențele sunt calculate din valori nerotunjite | MI, GLM, DR | 3 | **Se adoptă** (o notă) |
| N11 | Cele 2 fișiere din 13 trebuie numite | DR, MI-15 | 2 | **Se adoptă** |
| N12 | P §4 e încărcat cu detaliu empiric | DS, MI, GPT-15, GEM, GLM, DR | 6 | **Se adoptă:** §4 se comprimă; cifrele rămân în §6 sau în [24] |
| N13 | Direcția agenților cu memorie: concurenți mai tari (versiuni, proveniență, revocări) și poarta formulată și pentru telemetria scrierilor | GPT-13, DR-D4, GLM-B3 | 3 | **Se adoptă** |
| N14 | Amendamentul din §5: proveniența și o frază de gardă („not closure, not support”) | GPT-11, DR-D2, GLM-B2, MI-B2, DS-B2 | 5 | **Se adoptă**, cu proveniența corectă: protocolul Pilot 2 (vezi DR-D2 mai sus) |

**Puncte ridicate de un singur evaluator; decizia autorului:**
- GLM-4: tensiunea cu ablația proprie a lui FOREVER pe pași.
- GLM-B4: întârzierea sistematică lipsește din P.
- GEM-5: poarta de identificabilitate să fie despărțită formal de regula de închidere.
- DS-A2: familii de planificare de altă formă.
- DR-A4: definirea lui ΔN și C6; 512 fapte pe sarcină în port.
- DR-B5: regula T-B scrisă ca o conjuncție.
- DR-C1: propoziția fixează intrările externe.
- DR-C2: tabelul 1, VDF cu provocare proaspătă.
- DR-D3 (punctele 2–4): recalcularea H(S); suspendarea cu alimentare; sesiunea TEE.
- DR-E1: accesul epistemic față de virtualizare.
- DR, corecturi minore: punctuația din rândul „Changes”; spațiul din „( ca, N)”; trimiterea la [62, 71]. Acestea se verifică la construirea PDF-ului.

### Opțiunile deschise (D1, D3, D6), numărate ca opinii

| Opțiunea | Faza 2 | Faza 1 |
|---|---|---|
| D1: scurtarea rezumatului P (aprox. 420 de cuvinte) | 6 din 6 spun să se scurteze: DS 200–250 de cuvinte, MI aprox. 250, GPT 200–250, GLM aprox. 250, DR 250–300, GEM fără cifră | niciun comentariu |
| D3: păstrarea amendamentului din §5 | 6 din 6 spun să se păstreze, cu condiții: proveniența și caracterul prospectiv (GPT, DR, GLM), fraza de gardă (MI), justificarea logică (DS), reclasificarea ca condiție prealabilă (GEM) | S2: „a principled ‘not identifiable’ exit” |
| D6: păstrarea precedentului SI/Benzing și a direcției agenților cu memorie | 6 din 6 spun să se păstreze ambele (GPT: cu afirmații mai înguste; MI: eventual scurtată direcția) | niciun comentariu |

Decizia rămâne a autorului.

### Rezultatul fazei 2

- **Erori de fapt confirmate (se corectează):**
  - în R: uitarea pe dbpedia atribuită invers; referința la v1.4 lipsește din listă;
  - în P: „free optimizer telemetry” în patru locuri, plus poarta din Tabelul 2; fraza din §4 despre ambele cadre; nota
    „since version 1.2”; referințele [3] și [72]; cazurile ancorei de continuitate.
- **Puncte FATAL:** trei, toate confirmate ca defecte de formulare sau de logică în text: GPT-4 și GEM-1 (O1), GPT-5
  (O10). Toate trei se rezolvă prin text, fără rulări noi. Până la corectură nu se publică nimic pe Zenodo.
- **Obiecții care trec pragul:** O1–O4, O5 (formularea), O6/N7 (formularea), O7, O9, O10 și N1–N14.
- **Analize sau rulări posibile, la decizia autorului:**
  - analiza reziduului (O5);
  - rulări care înregistrează ambele ceasuri (O6);
  - reevaluarea adaptoarelor salvate (N2);
  - retenția pe faptele din memorie în T-A (N1).
- **Textele propuse** pentru corecturi sunt în `Corecturi_propuse_faza2.md`. Se aplică numai cu acordul autorului.

## Evaluare suplimentară (Copilot), 9 nov. 2026, seara

`Raspunsuri/Extra_Copilot_Perspective_v13_v14.txt`: Copilot (Think Deeper), doar pe PDF-urile Perspective v1.3 și v1.4
(construcția de seară, după corecturi), fără cod și fără celelalte documente. **Nu se numără** după regulă: Copilot nu e
unul dintre cei 8 evaluatori (în rundă a fost doar martor). Se verifică doar ca eventuală eroare de fapt.

- **Erori de fapt sau puncte fatale:** niciuna. Cifrele citate (R² 0,94–0,96 și 0,96–0,97; reconstrucția distanței
  funcționale din schimbarea pierderii pe aceleași sonde) corespund textului.
- **Confirmă corecturile:** citește ancora ca în M18 (suspendare sau execuție fără pas confirmat; suficientă pentru o
  singură linie, fără furcare și clonare) și nivelul 2 ca „neidentificabil”: nici echivalență, nici sprijin, nici
  închidere.
- **Deja în text:** separarea ipotezei pe ramuri (§5: „each level can be closed independently”; H-CONT, H-DEC și H-ADAPT
  corespund nivelurilor 4, 5 și 2/6); forma îngustă a nivelului 4 (Tabelul 2: „flag delayed, incomplete, or absent”;
  „graded evidence”; sarcina (iv), „Continuity under a delayed flag”); citirea care schimbă comportamentul și
  virtualizarea (paragraful despre separarea privilegiilor).
- **Planificat:** locurile goale `[DATA PUBLICĂRII]`, `[DOI-REPORT]`, `[DOI-PERSPECTIVE-1.4]` se completează la publicare.
  Codul, commit-ul, semințele și jurnalele sunt în arhivă și în raport ([24]), pe care evaluatorul nu le-a primit.
- **Propunere reținută pentru o versiune ulterioară, nu pentru v1.4:** „dual clock” retrogradat terminologic
  („continuity anchor plus trajectory measure”). Argumentul e real (rolurile nu mai sunt simetrice după Pilot 2), dar e
  o schimbare de cadru (titlul §4, caseta de contribuții, concluzia), nu o corectură; niciun evaluator din rundă n-a
  ridicat-o.
- **Formula de încheiere** („un candidat la ceas intern trebuie să demonstreze mai întâi că nu e o transformare
  reconstructibilă a contabilității deja existente a sistemului”) e deja în v1.4 (§6, al doilea avertisment; criteriul
  de admisibilitate din §4); poate fi folosită în descrierea Zenodo.

**Decizie (asistentul, cu libertatea dată de autor):** evaluarea se arhivează, nimic nu se schimbă în v1.4.

### A doua analiză Copilot (convergența cu FOREVER; replicarea pe 8 GPU), 9 nov., seara

Primită de la autor în sesiune, împreună cu promptul dat lui Copilot (după prima analiză, în aceeași conversație, cu
Perspective v1.3 și v1.4 ca singure documente). Textul nu se arhivează: e un răspuns la o întrebare a autorului, nu o
evaluare a documentelor. Nu se numără. Două premise greșite vin din prompt, nu de la Copilot (primele două puncte).
Verificarea:
- **Fals (premisa din prompt):** FOREVER ar fi testat Pythia-31M/70M/410M. Articolul (arXiv v2, §3): Qwen3-0.6B,
  Qwen3-4B, LLaMA3.1-8B, LLaMA2-13B; rezultatele principale (Tabelul 1) doar pe Qwen3-0.6B. Modelele Pythia din
  `D:\Time\_modele\` au fost descărcate pe 4 nov. pentru testul nostru de fezabilitate al unui braț Pythia + LoRA
  (`_workench_pythia_lora.py`; `Stadiul0/modele_provenienta.md`), nu pentru FOREVER.
- **Fals ca ordine (sugerat de prompt):** „abia după reproducere a fost rulată adaptarea proprie”. Portul (T-A, S1, S2, 6–7 nov.) a rulat
  înaintea reproducerii cu codul autorilor (R1, 7–8 nov.); doar varianta cu ceasul schimbat în codul lor (R2, etapa 1)
  a urmat reproducerii.
- **Supra-interpretare:** „ambele studii confirmă utilitatea unui semnal de progres al actualizării”. În T-A numărul
  de pași, care nu urmărește nicio schimbare a modelului, a dat aceeași retenție ca τ; s-a reprodus scorul FOREVER, nu
  avantajul ceasului lor (+1,2 OP față de calibrarea pe pași, nerepetat cu codul lor).
- **Inferență falsă din omisiunea din P:** „trigger-ele coincid” și „aproape integral reconstructibil” în orice
  replicare. În codul autorilor (fp16) Ση‖m̂‖ declanșează sistematic mai târziu (0–36 din 313 pași), iar R² a fost
  0,922 global, 0,749 pe sarcinile cu replay în R2 (post hoc) și 0,969 în A1. Confirmă punctul GLM-B4 (întârzierea lipsește
  din P).
- **Omisiune:** eliminarea copiei parametrilor cere și înlocuirea lui β, care folosește ‖Δθ‖ (R §5.3, R13).
- **Premisa multi-GPU:** scripturile FOREVER rulează fiecare job pe un singur GPU (`torchrun --nproc_per_node=1`);
  cele 8 H20 înseamnă rulări în paralel, nu antrenare distribuită (fără DDP, NCCL sau FSDP). Utilitatea unei asemenea
  mașini: multe rulări pe celulă, alte semințe și ordini (testul 3 din R §6), cu ambele ceasuri înregistrate.
- **Corect sau deja în arhivă:** intervenția „înlocuiește ceasul cu proxy-ul Adam, același buget de replay” e chiar R2 și
  etapa 1 (agregat în ±2, pe sarcină neconcludent); criteriul „aceeași decizie, nu aceleași zecimale” e R §6 („On
  generality”); majoritatea elementelor din lista pentru arhivă există (commit, scriptul variantei, mediile, hash-urile,
  semințele, lansatoarele, jurnalele, reproducerea automată). Lipsesc: intervale de încredere pentru R² și costul în timp
  al ceasurilor (R §5.3 spune că nu a fost măsurat).
