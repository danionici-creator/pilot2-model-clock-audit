# Stadiul 0: note de lucru (4 noiembrie 2026)

Note interne, în română, pentru raportul Stadiului 0 (care se va scrie în engleză, cu protocolul). Nimic nu e înghețat. Protocolul de referință e v0.3 (`../Pilot2_Protocol_EN_draft.md`).

## 1. Ce e construit

- Codul în `p2\` (lume, fluxuri F1–F6, agent, rulare, tripleți), configurația provizorie `config_stage0.yaml`, verificările `checks_stage0.py`, lansatorul `launch.py`, sondele de calibrare `calib_probe.py`, rezumatul `stage0_summary.py`.
- Agentul are **925.952 de parametri** (protocolul: ≈ 0,93 M).
- AdamW explicit, **bit-identic** cu `torch.optim.AdamW` pe 30 de pași (după alinierea tăierii gradientului la ordinea modulului și a primului moment la `lerp_`).
- Rulări repetate cu aceeași sămânță: **bit-identice** (G7, verificat pe F4 și F6 scurte).

## 2. Abateri de implementare de declarat

1. **Decalajul lui D2.** Un decalaj exact de 256 de pași cere 256 de copii ale lui v̂ (≈ 1 GB pe proces). Implementat: decalaj în blocuri, v̂ la 64·⌊(τ − 256)/64⌋, adică decalaj între 256 și 319 pași. Față de decalajul exact (măsurat pe rulări scurte): diferență relativă mediană 0,6–0,9%, maximă 11–19%.
2. **Lungimea exemplelor.** Toate exemplele au 5 tokeni; nu apare umplere (padding).
3. **Evaluările în pauză** refolosesc rezultatul ultimei evaluări (θ e înghețat), cu c_a nou. E exact.
4. **Numărul de valori distincte** pentru reguli e numărat pe setul de antrenare (protocolul: m_k; diferă doar dacă nu apar toate valorile).

## 3. Rulările tehnice tech1 (rata 1e-3, 6 procese în paralel, semințele 9001)

| Familie | Acuratețe copilărie | Episoade valide / total | Fapte competente | Reguli competente | r_AB | F_A medie (nați) | ΔAcc_A medie | ms/pas |
|---|---|---|---|---|---|---|---|---|
| F1 | 0,52 | 61 / 116 | 60 / 60 | 1 / 56 | 0,991 | 5,92 | 0,76 | 88,6 |
| F2 | 0,59 | 46 / 121 | 44 / 47 | 2 / 74 | 0,985 | 7,09 | 0,88 | 92,0 |
| F3 | 0,84 | 68 / 116 | 59 / 60 | 9 / 56 | 0,993 | 5,17 | 0,68 | 90,5 |
| F4 | 0,55 | 57 / 117 | 57 / 57 | 0 / 60 | 0,991 | 4,67 | 0,64 | 87,6 |
| F5 | 0,44 | 68 / 126 | 68 / 84 | 0 / 42 | 0,992 | 6,04 | 0,78 | 94,6 |
| F6 | 0,56 | 39 / 79 | 39 / 39 | 0 / 40 | 0,988 | 5,84 | 0,85 | 87,9 |

Durata unei rulări: 44–48 de minute cu 6 procese în paralel.

## 4. Probleme găsite

### 4.1 Copilăria nu trece poarta (≥ 0,95) la rata 1e-3
Pierderea stă pe un platou (~3,4 nați) până la ~1.000 de pași și încă scade la 3.072. Ratele mai mari sunt mai rele (2e-3, 3e-3, 5e-3: acuratețe 0,13–0,16). Ratele mai mici trec:

| Rata | Sămânța | Acuratețe | Fapte | Reguli |
|---|---|---|---|---|
| 1e-3 | 9101 | 0,650 | 0,917 | 0,383 |
| 5e-4 | 9101 | 0,917 | 0,986 | 0,848 |
| 4e-4 | 9101 / 9102 | 0,956 / 0,911 | 0,992 / 0,991 | 0,920 / 0,830 |
| 3e-4 | 9101 | 0,979 | 0,995 | 0,962 |
| 2e-4 | 9101 | 0,973 | 0,999 | 0,946 |

La 4e-4, o sarcină nouă de fapte e învățată complet în 128 de pași (batch 32 și 16). Candidat provizoriu: **3e-4**, de verificat pe mai multe semințe.

### 4.2 Regulile din protocol (§4.1) nu generalizează
O sarcină de reguli y = (a·x + b) mod m, antrenată singură 2.048 de pași: acuratețe pe antrenare 1,0 după 128–256 de pași, dar pe sondele neantrenate 0,02–0,05 (m = 36) și 0,30 (m = 24); pierderea pe sonde **crește** (supraînvățare). În rulările complete, 0–9 din 40–74 de episoade de reguli trec includerea. Deci aproape jumătate din sarcini nu produc tripleți, iar stratul „reguli” al H1 nu există.

Variantă testată (nu e în protocol): reguli **unare**, y = (a·d1 + b) mod m, cu d2 irelevant. Generalizează perfect în 128 de pași, iar copilăria ajunge la 0,99. E însă o generalizare slabă (doar peste o cifră irelevantă).

Variante posibile (decizia autorului, la nivel de protocol):
- A. fără sarcini de reguli (doar fapte; se pierde stratul de generalizare);
- B. reguli unare (generalizare peste combinații nevăzute; slabă, dar măsurabilă);
- C. reguli cu dificultate intermediară (de exemplu, două tabele selectate de un bit al lui d2), de testat;
- D. sondele de reguli devin itemi antrenați (retenție, nu generalizare).

### 4.3 Uitarea e catastrofală și saturată (la rata 1e-3)
O sarcină de fapte învățată perfect scade de la 1,0 la ~0,05 în ~2.000 de pași, iar pierderea urcă la 6–8 nați, peste nivelul șansei (ln 64 ≈ 4,2): modelul devine sigur pe răspunsuri greșite. r_AB ≈ 0,99 e mare tocmai pentru că variația dintre episoade e uriașă, deci poarta G1 trece fără să spună mult. Riscul: ținta e dominată de saturare și de lungimea intervalului, iar spațiul de câștig (G3) poate fi mic. De verificat la rata 3e-4 (rulările tech2).

### 4.4 Costul: limita e lățimea de bandă a memoriei
Un pas: ~19 ms singur. În paralel (același pas, măsurat):

| Procese | ms/pas | Pași/s în total |
|---|---|---|
| 1 | 19–20 | ≈ 51 |
| 2 | 27 | ≈ 74 |
| 4 | 42–49 | ≈ 85–95 |
| 8 | 95–101 | ≈ 80–84 |

Operațiile pe vectori de mărimea modelului încetinesc de 8× la 4 procese și de 22× la 8 (lățimea totală ≈ 15–20 GB/s); calculul pur (matmul în cache) doar de ~2×. Bufferele prealocate n-au schimbat esențial scalarea (101 → 95 ms la 8 procese).

Consecință: criteriul din §12a „≤ 25 min pe rulare, cu opt procese în paralel” **nu se poate atinge** pe acest laptop (o rulare cu 6–8 procese: 44–48 min). Debitul total e maxim la ~4 procese: o rulare ≈ 20 min, Stadiul A (≈ 315 rulări) ≈ 105 ore-CPU ≈ 26 de ore de ceas; Stadiul B (≈ 590 de rulări) ≈ 200 de ore-CPU ≈ 50 de ore de ceas. Criteriul ar trebui formulat ca debit (rulări pe oră) și ore-CPU, nu ca durată la 8 procese.

## 5. Rulările tehnice tech2 (rata 3e-4, 3 procese în paralel, semințele 9002, cod cu buffere)

| Familie | Acuratețe copilărie | Episoade valide / total | Fapte competente | Reguli competente | r_AB | F_A medie | ΔAcc_A medie | ms/pas | Durată | Memorie maximă |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 | 0,954 | 60 / 116 | 58 / 58 | 2 / 58 | 0,994 | 3,37 | 0,52 | 56,7 | 30,0 min | 821 MB |
| F2 | 0,948 | 68 / 132 | 68 / 68 | 0 / 64 | 0,989 | 4,89 | 0,73 | 55,1 | 31,1 min | 819 MB |
| F3 | 0,971 | 60 / 116 | 58 / 58 | 2 / 58 | 0,996 | 3,77 | 0,53 | 56,6 | 30,1 min | 814 MB |

Debit observat: tech1 6 rulări în 48 min (≈ 7,5 rulări/oră), tech2 3 rulări în 31 min (≈ 5,8 rulări/oră).

**Copilăria la 2e-4, pe cele șase lumi ale rulărilor tehnice:** 0,975; 0,948; 0,966; 0,958; 0,974; 0,982 (5 din 6 trec). Faptele stau mereu la 0,996–0,999; singura rulare care pică o face din cauza regulilor (0,897). **Poarta copilăriei depinde deci de decizia despre reguli** (cu reguli unare: 0,99).

**Forma uitării** (tech2, tripleți incluși, după ΔN):

| ΔN | n | F_A medie (nați) | ΔAcc_A medie |
|---|---|---|---|
| 64–127 | 39 | 0,77 | 0,19 |
| 128–255 | 135 | 1,22 | 0,23 |
| 256–511 | 264 | 1,74 | 0,37 |
| 512–1.023 | 447 | 4,26 | 0,71 |
| 1.024–2.047 | 597 | 5,95 | 0,87 |
| 2.048–4.095 | 809 | 7,59 | 0,95 |
| ≥ 4.096 | 1.695 | 9,06 | 0,98 |

Uitarea funcțională e aproape completă după ~2.000 de pași, dar pierderea continuă să urce (7,6 → 9,1 nați, mult peste șansă). **La intervale lungi, T1 măsoară mai ales creșterea scării logiților**, nu uitare suplimentară. 2.504 din 3.986 de tripleți au ΔN ≥ 2.048.

**Marja de câștig, estimare brută (G3, fără c_e):** GBDT neacordat, câte o rulare lăsată deoparte (antrenare pe celelalte familii), R² ponderat în rulare. c_e nu a fost folosit: valoarea lui incrementală e statistica lui H1 și nu se calculează înainte de înghețare.

| Rulare test | r_AB | doar ΔN | ΔN + X_cov | B_standard + X_cov | B_strong | r_AB − B_strong |
|---|---|---|---|---|---|---|
| F1 (3e-4) | 0,994 | 0,843 | 0,885 | 0,917 | 0,899 | 0,094 |
| F2 (3e-4) | 0,989 | 0,664 | 0,496 | 0,701 | 0,717 | 0,272 |
| F3 (3e-4) | 0,996 | 0,679 | 0,730 | 0,712 | 0,859 | 0,137 |
| F1–F6 (1e-3) | 0,985–0,993 | 0,45–0,90 | | | 0,70–0,93 | 0,06–0,29 |

Marja nu e neglijabilă (cu ea, δ = 0,02 și G3 ar trece), dar estimarea e pesimistă pentru B_strong (neacordat, antrenat pe alte familii, câte o rulare); marja reală va fi mai mică.

## 5b. Analiză aprofundată (4 nov. 2026, fir nou; fără c_e incremental)

Doar episoade de fapte (varianta A; prima versiune a acestei analize includea și cele 2 episoade de reguli din F1 și F3), ponderi §6 recalculate după filtru. Scripturile (`t1_deep.py`, `mech.py`, `headroom_cap.py`) sunt în scratchpad-ul sesiunii; se pot reface din descrierile de mai jos. Nicio coloană `ce_*` sau `Disp_*` nu intră în modele; singura mărime c_e citită e rata pe sferturi a lui D3, D1, D1_rel și D2, cerută de verificarea de staționaritate din §5.1 (descriptivă, nu valoare incrementală).

### 5b.1 Saturarea lui T1

| Rulare | Pondere w cu ΔN ≥ 2.048 | Parte din SST(F_A) | SD ΔAcc_A acolo | r_AB fără plafon / ≤ 2.048 | Tripleți fără plafon / ≤ 2.048 | Episoade păstrate |
|---|---|---|---|---|---|---|
| F1, 3e-4 | 0,18 | 0,64 | 0,04 | 0,993 / 0,985 | 947 / 298 | 58 / 58 |
| F2, 3e-4 | 0,23 | 0,32 | 0,02 | 0,989 / 0,987 | 1.774 / 897 | 68 / 68 |
| F3, 3e-4 | 0,21 | 0,52 | 0,04 | 0,996 / 0,992 | 1.156 / 303 | 58 / 58 |
| F1–F6, 1e-3 | 0,20–0,38 | 0,28–0,53 | | 0,985–0,993 / 0,982–0,991 | | toate |

Pragul de saturare depinde de rată: ΔAcc_A mediu ajunge la ≈ 0,90 pe la ΔN ≈ 1.024 la 1e-3 și pe la ΔN ≈ 2.048 la 3e-4 (curbele pe benzi de ΔN, F1–F3).

**Mecanismul.** Bateria R (nereantrenată după copilărie) e uitată aproape imediat: L_R trece de nivelul șansei (ln 64 ≈ 4,2) după ~400–800 de pași din viață la 3e-4 și ajunge la 7–8 nați după ~2.000. După uitare, pierderea pe sarcinile uitate (Acc_A ≤ 0,05) are același nivel ca L_R și se mișcă împreună cu el de la o evaluare la alta (corelație peste evaluări 0,48–0,76 la 3e-4; 0,61–0,91 la 1e-3). Pe tripleții saturați, corr(F_A, C10) = 0,29–0,44 la 3e-4 și 0,54–0,73 la 1e-3. Deci, după saturare, F_A măsoară mai ales **un nivel comun al pierderii pe intrări străine în momentul t₁** (cât de sigur greșește modelul pe orice intrare care nu e antrenată acum), nu uitarea sarcinii k.

**Marja de tip G3, cu și fără plafon** (tech2, GBDT neacordat, câte o rulare lăsată deoparte, antrenare pe celelalte două familii):

| Plafon ΔN | R² doar ΔN | R² B_strong | r_AB − B_strong |
|---|---|---|---|
| fără | 0,63–0,89 | 0,71–0,93 | 0,06–0,28 |
| ≤ 4.096 | 0,60–0,84 | 0,69–0,91 | 0,08–0,30 |
| ≤ 2.048 | 0,36–0,68 | 0,66–0,85 | 0,14–0,33 |
| ≤ 1.024 | 0,22–0,38 | 0,38–0,74 | 0,24–0,61 |

Fără plafon, o parte din R²-ul numărătorilor vine din regiunea saturată. Estimarea rămâne brută (3 rulări, neacordat, transfer între familii), iar plafonul reduce numărul de tripleți cu 50–70%, deci varianța lui ΔR²_r între rulări poate crește (n_H1 mai mare); asta nu se poate măsura fără c_e.

**Atenție:** lumile tech2 aveau ~jumătate sarcini de reguli. Cu varianta A, toate cele 40 de sarcini sunt de fapte, deci interferența fapte–fapte crește și saturarea poate începe mai devreme. Pragul măsurat la 3e-4 nu e încă pragul lumii fără reguli.

### 5b.2 Staționaritatea lui R (§5.1): verificarea va pica și nu măsoară ce trebuie

Rata pe sferturi de viață, Q4/Q1 (criteriu: ±20%):

| Rulare | D3 | C10b | D1 | D1_rel | D2 | D3 / D1_rel |
|---|---|---|---|---|---|---|
| F1, 3e-4 | 0,62 | 0,44 | 0,80 | 0,52 | 0,56 | 1,19 |
| F2, 3e-4 | 0,70 | 0,93 | 0,88 | 0,54 | 0,69 | 1,30 |
| F3, 3e-4 | 0,58 | 0,64 | 0,73 | 0,45 | 0,61 | 1,29 |
| F1, 1e-3 | 0,74 | 1,16 | 0,82 | 0,50 | 0,71 | 1,48 |

D3 scade cu 30–42%, dar distanțele în spațiul parametrilor scad la fel sau mai mult (D1_rel cu 46–55%): scăderea pare o încetinire reală a schimbării (‖θ‖ crește de la ~50 la ~80–85), nu o pierdere de sensibilitate a lui R. Mai mult, R e uitată în primul sfert (Q1 = primii 5.120 de pași), deci comparația Q1–Q4 nu poate detecta efectul uitării lui R. Remediul din protocol (R_maint, un batch la 512 pași) nu poate păstra itemi de fapte: o sarcină de fapte se uită în ~1.000–2.000 de pași, iar R_eval ar fi uitată oricum. **De decis** (amendament în v0.4).

### 5b.3 Rata: competența nu discriminează

Sonde `calib_probe.py task --kind fact --steps 512 --seed 9201`: copilăria 0,995 (2e-4) și 0,989 (3e-4); o sarcină nouă de fapte are Acc_B = 1,0 după 128 de pași la ambele rate, și la batch 16, și la 64 (L_B 0,035–0,041 la batch 16, 0,003–0,007 la 64). În tech2 (3e-4) toate episoadele de fapte au Acc_B(t₀) ≥ 0,992. La 1e-3, F5 avea 16 episoade sub 0,90. Între 2e-4 și 3e-4 rămâne de comparat doar forma uitării (pragul de saturare), care se vede numai în rulări complete.

### 5b.4 Costul, recalculat din jurnalele rulărilor

- Debit măsurat: tech2, 3 procese: 3 rulări în 1.875 s (5,8 pe oră; 0,52 ore-nucleu pe rulare). tech1, 6 procese: 6 rulări în 2.897 s (7,5 pe oră; 0,73–0,80 ore-nucleu pe rulare). Dintr-o rulare tech2 (1.868 s): antrenarea vieții 1.128 s, copilăria 243 s, evaluările 241 s, D3/D4/C10b 187 s, instantaneele 65 s.
- Stadiul A, ≈ 315 rulări: 160 de ore-nucleu (3 procese) sau ≈ 240 (6 procese). **Criteriul „≤ 150 de ore-CPU” pică în ambele configurații**, nu doar criteriul de 25 de minute. *Corectură după tech3:* cu 4 procese (25 min pe rulare) Stadiul A ar avea ≈ 130 de ore-nucleu, deci sub 150, dar fără ajustarea modelelor; concluzia „ora-nucleu nu măsoară costul” rămâne. Un singur proces (~0,2 ore-nucleu pe rulare) l-ar trece, dar cu ~65 de ore de ceas. Ora-nucleu nu e o măsură a costului când limita e memoria.
- Estimarea din §4.4 („≈ 26 de ore de ceas”) e prea optimistă: debitul măsurat dă 42–54 de ore pentru Stadiul A și 80–100 pentru Stadiul B (≈ 590 de rulări). Ajustarea modelelor (250 de replici bootstrap, căutări de 50–100 de configurații, G3b, G4, G4b, G6) nu e măsurată și e inclusă de §12a în buget.
- Hardware: i5-12500H (4 nuclee P + 8 E), 16 GB într-un **singur modul DDR4-3200 (canalul A; al doilea slot e gol)**, deci memorie pe un singur canal (≈ 25,6 GB/s teoretic; măsurat 15–20 GB/s). Un al doilea modul ar dubla lățimea de bandă teoretică; câștigul de debit nu e măsurat.
- Reluarea din puncte de salvare (cerută de §12a) **nu e implementată**: `run.py` nu salvează stare, iar `launch.py` nu sare peste rulările terminate și rescrie `run.log`. Cum rulările sunt deterministe bit cu bit, o rulare întreruptă poate fi refăcută de la zero cu rezultat identic; e nevoie doar ca lansatorul să sară peste rulările complete (verificând `meta.json` și hash-urile).
- `config_stage0.yaml` are încă `optim.lr: 1.0e-3`; tech2 a rulat cu suprascrierea `optim.lr=3.0e-4`.

## 5c. Runda tech3 (fără reguli): criterii fixate ÎNAINTE de rulare (4 nov. 2026)

Rulări: F2 și F3, sămânța 9004, la `optim.lr` = 2e-4 și 3e-4 (4 rulări, câte 2 procese pe rată, în paralel); configurația curentă (varianta A). Tag-uri `tech3_lr2e-4`, `tech3_lr3e-4`. Nicio mărime c_e nu intră în criterii.

1. **Validitate:** copilăria ≥ 0,95 și cel puțin 20 de episoade valide în fiecare rulare; altfel rata respectivă e exclusă.
2. **Pragul de saturare la fiecare rată:** cel mai mic multiplu de 256, ΔN*, la care ΔAcc_A mediu ponderat (ponderi §6), pe tripleții cu ΔN în [ΔN*, ΔN* + 256), atinge 0,90, pe F2 și F3 reunite.
3. **Alegerea ratei:** rata cu mai mulți tripleți incluși cu ΔN < ΔN* (însumați pe F2 și F3). Dacă diferența e sub 10%, se alege 3e-4 (singura măsurată deja în viață).
4. **Plafonul propus pentru T1:** ΔN* al ratei alese (rezultatul fără plafon rămâne analiză de sensibilitate). Propunerea merge la autor; nu se aplică automat.

**Rezultate tech3** (4 nov. 2026; `tech3_criteria.py`; rulările în `runs/tech3_lr2e-4`, `runs/tech3_lr3e-4`):

| Rată | Familie | Copilărie | Episoade valide / total | Tripleți incluși | r_AB | ms/pas | Durată |
|---|---|---|---|---|---|---|---|
| 2e-4 | F2 | 0,991 | 132 / 132 | 3.616 | 0,990 | 46,6 | 25,2 min |
| 2e-4 | F3 | 0,994 | 116 / 116 | 2.340 | 0,994 | 45,9 | 23,6 min |
| 3e-4 | F2 | 0,988 | 132 / 132 | 3.616 | 0,989 | 46,6 | 25,2 min |
| 3e-4 | F3 | 0,982 | 116 / 116 | 2.340 | 0,994 | 46,0 | 23,6 min |

1. Validitate: trec toate (copilăria ≥ 0,98; toate episoadele valide, fiindcă toate sarcinile sunt de fapte).
2. **ΔN* = 1.280 la ambele rate** (fără reguli, saturarea începe mai devreme decât în tech2: acolo ≈ 2.048). Curbele uitării pe benzi de ΔN sunt practic identice la 2e-4 și 3e-4 (ΔAcc_A: 0,21 / 0,24 / 0,38 / 0,70 / 0,88 / 0,96 / 0,98 / 0,98 la ambele; F_A diferă cu ≤ 0,12 nați).
3. Tripleți sub ΔN*: 1.585 la ambele rate (programul e același, fiind aceeași sămânță) → diferență 0% < 10% → **regula alege 3e-4**.
4. **Plafon propus: ΔN < 1.280.** Păstrează toate episoadele (132 / 116), r_AB 0,981–0,988, SD ΔAcc_A 0,27–0,31 (fără plafon: 0,29–0,36); rămân 31% (F2) și 19% (F3) din tripleți; regiunea tăiată are 25–39% din pondere.

Observații (descriptive, o singură sămânță): uitarea pe pas nu depinde de rată între 2e-4 și 3e-4, deși mărimea pașilor diferă de 1,5×. Debit la 4 procese: 4 rulări în 25,2 min ≈ **9,5 rulări pe oră** (mai bun decât 7,5 la 6 procese și 5,8 la 3). Lansatorul sare acum peste rulările complete (`launch.py`), iar `meta.json` primește `config_resolved_sha256` (hash-ul configurației cu suprascrieri; `config_sha256` acoperă doar fișierul). Verificările: 19/19 după modificare.

## 6. Decizii

**Luată (4 nov. 2026): varianta A, fără sarcini de reguli**, nici țintă, nici de referință. Aplicat în `config_stage0.yaml` (`rule_frac: 0.0` în toate familiile; `n_ref_fact: 8`, `n_ref_rule: 0`). Codul pentru reguli rămâne, neutilizat. Copilăria doar cu fapte trece poarta în toate cele șase lumi verificate:

| Rata | F1, 9001 | F2, 9002 | F5, 9003 |
|---|---|---|---|
| 2e-4 | 0,993 | 0,993 | 0,990 |
| 3e-4 | 0,977 | 0,986 | 0,981 |

**Amendamente de protocol implicate** (de scris în v0.4, cu jurnal §21):
- §4.1: fără sarcini de reguli; cele 32 de tokeni-cifră devin rezervă; R și B_beh: câte 256 de itemi de fapte (32 din fiecare dintre cele 8 sarcini de referință de fapte).
- §4.2 și §6: sondele sunt doar itemi antrenați, deci T1 măsoară **retenția asociativă în eșantion**; stratul „după tipul sarcinii” dispare (rămâne stratul după terțila lui ΔN).
- §7: covariatele „tipul sarcinii” și „log numărul de valori distincte” devin constante și se scot din X_cov.
- §4.4: F5 nu mai diferă prin proporția regulilor; rămâne diferit prin π_overlap, pauze și restarturile ratei de învățare (amestecul generatorilor F2–F3).
- §1, §16: limitare declarată: studiul nu testează uitarea unei generalizări.
- Plus constatările deja notate: decalajul D2 în blocuri (§5.1), criteriul de cost (§12a), rata provizorie.

**De decis în continuare:**

1. **Rata de învățare provizorie:** 2e-4 sau 3e-4 (doar cu fapte, ambele trec poarta; 2e-4 cu marjă mai mare; efectul asupra uitării în viață e măsurat doar la 3e-4 și 1e-3).
2. **Ținta T1 la intervale lungi:** creșterea scării logiților după uitarea completă. Variante: (i) plafon pentru ΔN în definiția tripleților; (ii) T1-acc devine ținta principală sau co-primară; (iii) repetiții mai dese, ca mai puține intervale să fie saturate; (iv) se lasă așa, cu raportarea stratificată după ΔN (deja în §6).
3. **Criteriul de cost din §12a:** de reformulat ca debit (rulări pe oră) și ore-CPU; observat ≈ 6–7,5 rulări pe oră, deci Stadiul A (≈ 315 rulări) ≈ 42–54 de ore de ceas, iar Stadiul B (≈ 590) ≈ 80–100 de ore.

## 7. Aplicat (4 nov. 2026, după confirmarea autorului: „merg exclusiv pe propunerile tale”)

- `config_stage0.yaml`: `optim.lr: 3.0e-4`; secțiune nouă `analysis: t1_max_dN: 1280` (citită doar de `p2/triplets.py`). Copia dinainte: `_work\_copii_siguranta\config_stage0.yaml.bak_4nov_lr1e-3`.
- `p2/triplets.py`: plafonul intră în includere (`excl_reason` = `dN>=1280`); se păstrează `incl_nocap` și `w_nocap` pentru analiza de sensibilitate; coloana `t1_max_dN`. Verificat pe tech3 (3e-4): 1.135 / 450 tripleți, toate episoadele, ponderile însumează 1.
- `p2/run.py`: `config_resolved_sha256` exclude secțiunile `analysis` și `meta` (nu influențează rularea). `launch.py` compară la fel. Rulările `tech3_lr3e-4` sunt recunoscute drept rulări complete ale configurației noi.
- Protocolul **v0.4** (`../Pilot2_Protocol_EN_draft.md` și `.pdf`, 32 de pagini, 26 de tabele): generat de `_work\make_pilot2_v04.py` din textul exact al v0.3 (30 de înlocuiri, fiecare verificată că apare o singură dată) plus jurnalul §21; v0.3 păstrat în `Versiuni_anterioare\Pilot2_Protocol_EN_v0.3.md/.pdf`. PDF: `_workuild_pilot2_pdf.py` (marked 15.0.12 → HTML → Edge headless, căi absolute).

## 8. Fezabilitatea unui braț Pythia + LoRA (4 nov. 2026, orb față de c_e)

Modele descărcate (doar safetensors, config, tokenizer; încărcate cu `local_files_only`, fără cod la distanță): `D:\Time\_modele\EleutherAI_pythia-70m` (168 MB) și `..._pythia-31m` (63 MB). **Nu intră în nicio arhivă publică.** Modelele din LM Studio (`D:\.lmstudio\models\`: RoMistral 7B, Qwen2.5-Coder 7B, DeepSeek-R1-Distill 8B, toate GGUF cuantizate) servesc doar la inferență și nu pot fi antrenate cu LoRA în PyTorch; la precizie completă un model de 7B ar cere ~28 GB.

Scriptul: `_work\bench_pythia_lora.py` (LoRA de rang 8, alpha 16, pe toate stratele liniare din atenție și MLP; AdamW; fapte sintetice „code XXX-YYY is WORD”, 256 pe sarcină, 31 de cuvinte-răspuns de un token, secvență de 10 tokeni, batch 32; capul de ieșire de 50k aplicat doar la poziția răspunsului).

| Model | Parametri (antrenați LoRA) | ms/pas, 1 fir | ms/pas, 4 fire | Evaluarea a 256 de itemi, 4 fire |
|---|---|---|---|---|
| Pythia-31m | 30,7 M (0,197 M) | 139 | 68 | 244 ms |
| Pythia-70m | 70,8 M (0,393 M) | 414 | 180 | 694 ms |

(Prima variantă, cu logiții pe toate pozițiile: 309 / 761 ms pe pas la 1 fir.)

Învățare și uitare (o singură sămânță; sarcina 1, apoi sarcina 2 pe același șablon, fără token de sarcină):
- **Pythia-31m, lr 1e-3:** sarcina 1 învățată în 128–192 de pași (acuratețe 0,97 → 1,0); după 64 de pași pe sarcina 2, acuratețea pe sarcina 1 scade la 0,08 (șansa: 1/31 ≈ 0,03), iar pierderea urcă la 9,5 nați, **același tipar de saturare ca în lumea sintetică** (răspunsuri greșite tot mai sigure).
- **Pythia-70m, lr 3e-4:** învățată în ~192 de pași; după 64 de pași pe sarcina 2, acuratețea scade la 0,13–0,22 și rămâne pe un platou de ~0,20; pierderea ajunge la 5,4.

Concluzii provizorii:
1. **Fezabil pe laptop.** O viață de 10 sarcini × 512 pași cu evaluări la 256 de pași: ~18 min (70m) sau ~7 min (31m) la 4 fire; 20–30 de rulări ≈ 6–9 h (70m) sau 2,5–3,5 h (31m), fără D3 și telemetrie (estimat +20–30%). Rularea în paralel pe un fir nu e măsurată.
2. **Modelul preantrenat chiar învață și uită** fapte arbitrare cu LoRA, condiția cerută de ChatGPT pentru un braț util.
3. **Uitarea e mult mai rapidă decât în lumea sintetică** (completă în ~64 de pași, față de ~1.280): grila de evaluare ar trebui să fie mult mai fină (8–16 pași), rata mai mică sau sarcinile intercalate. De rezolvat la proiectare.
4. Tiparul de saturare a pierderii apare și aici: obiecția „artefact al unui model mic de jucărie” (Gemini) e slăbită pentru acest tip de țintă.

## 9. G2 pe rulările tehnice: rata lui c_e e aproape complet reconstructibilă din telemetrie (4 nov. 2026)

Orb față de T1: modelele prezic doar rata ρ̄ = Δc_e / max(ΔN, 1) din B_strong; coloanele F_A, F_B, ΔAcc_A nu sunt citite. Scriptul: `g2_preview.py`. Date: 5 rulări cu 3e-4 (tech3 F2 și F3, fără reguli; tech2 F1–F3, doar tripleții de fapte), ΔN ∈ [64, 1.280), 2.639 de tripleți, 58 de variabile; test pe fiecare rulare tech3, antrenare pe celelalte patru; modele neacordate.

| D | R² OLS (F2 / F3) | R² GBDT (F2 / F3) | CV al ratei | R² doar din ΔN |
|---|---|---|---|---|
| D1 | 0,984 / 0,992 | 0,981 / 0,991 | 0,37 / 0,66 | 0,33 / −0,06 |
| D1_rel | 0,956 / 0,981 | 0,974 / 0,972 | 0,44 / 0,73 | 0,30 / −0,11 |
| D2 | 0,987 / 0,993 | 0,989 / 0,989 | 0,40 / 0,73 | 0,27 / −0,06 |
| D3 | 0,919 / 0,960 | 0,907 / 0,950 | 0,40 / 0,63 | 0,22 / −0,13 |

Rata variază mult (CV 0,37–0,73) și ΔN singur nu o explică, deci familiile decuplează bine pașii de schimbare. Dar **telemetria o reconstruiește aproape complet**: poarta G2 din v0.4 (ambele R² < 0,90) **pică pentru toți cei patru candidați**, chiar dacă la limită pentru D3.

**Scara de telemetrie minimă** (OLS, media celor două rulări test): ΔN + rata Ση‖m̂‖ (C5d, un singur scalar ieftin) dă R² = 0,935 (D1), 0,919 (D1_rel), 0,987 (D2), 0,846 (D3); ΔN + rata Ση‖g̃‖ (C5b) dă 0,892 / 0,898 / 0,964 / 0,824. ΔN + Ση singur: 0,30–0,47; ΔN + pierderea pe R (C10b): 0,47–0,63.

Interpretare provizorie (estimare brută: rulări tehnice, neacordat, o sămânță pe familie):
1. Ceasul de tip FOREVER (D1) e, în acest regim, practic **momentul ponderat cu rata de învățare, Ση‖m̂‖**, plus durata. Un singur scalar ieftin îl înlocuiește în proporție de ~94%.
2. Pentru D1, D1_rel și D2, un rezultat H1 „susținut” e foarte puțin probabil, iar un „echivalent” ar fi aproape predeterminat. Concluzia lui Mistral („echivalență predeterminată”) se confirmă empiric, deși argumentul lui algebric era greșit.
3. D3 (schimbarea ieșirilor pe R) e candidatul cel mai puțin reconstructibil (R² 0,91–0,96; din C5d doar 0,85): singurul cu loc pentru informație proprie.
4. Rezultatul e deja o constatare în sine, de tipul cerut de Copilot, Gemini și ChatGPT („cel mai mic substitut suficient”), și se obține fără a atinge ținta. Trebuie confirmat pe rulări noi (calibrarea) și pe brațul Pythia + LoRA, unde FOREVER își face afirmația.

## 10. Placa RTX 3050 Laptop (4 GB) existentă: braț LM fezabil, inclusiv Qwen3-0.6B (4 nov. 2026)

Mediu separat `D:\Time\_venv_cuda` (torch 2.13.0+cu130, transformers 5.13.1; 3,1 GB); mediul CPU al Stadiului 0 a rămas neschimbat. Modele noi în `D:\Time\_modele\`: Pythia-410m (913 MB), Qwen3-0.6B (1.519 MB). Script: `_work\bench_lm_lora.py` (LoRA r = 8 pe toate stratele liniare din blocuri; batch 32; fapte ca în §8).

| Model (LoRA antrenat) | fp32: ms/pas, VRAM | bf16: ms/pas, VRAM | Evaluarea a 256 de itemi (bf16) |
|---|---|---|---|
| Pythia-70m (0,39 M) | 71 ms, 434 MiB | 83 ms, 261 MiB | 37 ms |
| Pythia-410m | 268 ms, 2.251 MiB | 288 ms, 1.209 MiB | 259 ms |
| **Qwen3-0.6B** (5,05 M) | 548 ms, 3.331 MiB | **259 ms, 2.065 MiB** | 473 ms |

(Pythia-70m pe CPU, 4 fire: 180 ms/pas; la modele mici GPU-ul câștigă puțin, fiindcă timpul se duce pe lansarea operațiilor.)

Qwen3-0.6B, bf16, lr 3e-4: sarcina 1 învățată în 64 de pași (0,96 → 1,0 la 128); după 64 de pași pe sarcina 2, acuratețea pe sarcina 1 scade la 0,18 și rămâne acolo (pierderea ~4,3 nați).

Concluzii: **modelul cel mai mic din FOREVER (Qwen3-0.6B) rulează pe placa existentă**, cu ~2 GB VRAM din 4. O viață de 10 sarcini × 512 pași ≈ 24 min; 20–30 de rulări ≈ 8–12 h. **eGPU-ul nu e necesar pentru brațul LM la această scară.** Neverificat: rulări bit-identice pe GPU (va trebui `torch.use_deterministic_algorithms` și CUBLAS_WORKSPACE_CONFIG, plus o verificare G7 separată) și rularea în paralel cu campania CPU.

## 11. Al doilea modul de memorie: identitate, canal dublu, G7, debit (5 nov. 2026)

**Modulele** (WMI `Win32_PhysicalMemory`): ambele Samsung M471A2K43EB1-CWE, 16 GB, DDR4-3200 SO-DIMM, 1,2 V, două ranguri, fără ECC; seriile 37AF60BF și 34FD16A0. Unul pe Controller0-ChannelA-DIMM0, celălalt pe Controller1-ChannelA-DIMM0 (la i5-12500H cu DDR4, câte un canal pe controler), poziții de intercalare 1 și 2, ambele la 3200 MT/s. Windows vede 31,6 GB.

**Canal dublu, confirmat empiric** (`membw.py`, torch 2.13 CPU, tablouri de 256 MB): copiere 21,7 / 25,1 / **37,6** / 34,4 / 31,2 GB/s la 1 / 2 / 4 / 8 / 12 fire; triad la 4 fire 37,4 GB/s; 4 procese cu câte un fir, simultan: 34,8 GB/s în total. Peste maximul teoretic al unui canal DDR4-3200 (25,6 GB/s). Înainte (un modul) estimasem 15–20 GB/s, fără o măsurătoare de tip STREAM.

**Erori:** Windows Memory Diagnostic (pornit de autor, 19:20–19:54): fără erori. Jurnalele: nicio eroare de memorie WHEA (memoria fără ECC nu le-ar putea raporta oricum). Cele două opriri neașteptate din 5 nov. sunt explicate: prima pornire cu memoria nouă (pornirea rapidă eșuată, 0xC00000D4, firmware 17 s din antrenarea memoriei; înregistrată cu ora greșită, 08:22, fiindcă ceasul intern s-a resetat la deconectarea bateriei) și o oprire făcută de autor la ~19:07 (confirmat). Fără evenimente de limitare a frecvenței de către firmware (Kernel-Processor-Power 37). `checks_stage0.py`: 19/19.

**G7 după montare: TRECE.** Cele 4 rulări tech3 (F2 și F3, sămânța 9004, la 3e-4 și 2e-4) refăcute cu 4 procese, ca înainte (`runs/g7_ram_lr3e-4`, `runs/g7_ram_lr2e-4`): toate cele 24 de fișiere de tablouri (steps, evals, episodes, disp, chunks, world) sunt **identice bit cu bit** cu rulările făcute cu un singur modul, atât după hash-urile din `meta.json`, cât și recalculate din fișiere (`g7_ram_compare.py`).

**Debitul: practic neschimbat** pe acest lot. 4 rulări în 25,1 min (înainte 25,2 min); rularea cea mai lungă (F2) 1.497–1.505 s față de 1.509 s, F3 1.242 s față de 1.414–1.418 s (−12%). Pe componente: antrenarea vieții e mai rapidă (F2 955 → 854–860 s, −10%; F3 940 → 726 s, −23%), dar copilăria e mai lentă (149 → 193 s, +30%, la toate patru) și evaluările F2 la fel (211 → 235 s). Cauza încetinirii copilăriei nu e stabilită (profil de alimentare ASUS după resetarea controlerului la deconectarea bateriei? activitate în fundal la pornirea lotului?). Concluzie: dublarea lățimii de bandă nu dublează debitul; ipoteza din §4.4 („limita e lățimea de bandă”) e doar parțial adevărată. Criteriul de cost (≥ 6 rulări pe oră) rămâne îndeplinit (≈ 9,5 pe oră). O nouă măsurătoare, cu modul de operare ASUS cunoscut, e opțională.

**Modul ASUS Turbo (5 nov. 2026, ales de autor în Armoury Crate):** registrul `ThrottlePlugin\ROG ATKStatus\ThrottleModeOnAC` a trecut din 0 în 3 (`External\SelectedMode` din 1 în 8); semnificația exactă a valorilor nu e documentată. Test: copilăria (`calib_probe.py childhood`, aceeași funcție ca în `p2/run.py`) pentru F2 și F3, sămânța 9004, la 3e-4 și 2e-4, **4 procese simultan: 100,6–101,3 s**, față de 193 s în G7 (modul de dinainte, din aceeași seară) și 149 s în tech3 (4 nov.). Acuratețea de referință e identică cu cea din rulările complete (0,9878 / 0,9819 / 0,9907 / 0,9941). Performanța procesorului ≈ 121–125% din frecvența nominală (typeperf). Deci încetinirea din G7 venea din modul de operare, nu din memorie. Rezervă: testul durează ~100 s, iar regimul termic stabil pe 25 de minute nu e măsurat; debitul real în Turbo se măsoară în runda tehnică următoare (F1–F6). Temperatura nu se poate citi fără drepturi de administrator. **Regulă: toate campaniile de acum înainte rulează în Turbo, la priză;** modul se notează în raport. Tot pe 5 nov. seara, autorul a curățat ventilatoarele și a schimbat pasta termică pe procesor și pe componenta alăturată. Comparațiile de debit cu 4 nov. amestecă deci patru schimbări (memoria, pasta, curățarea, modul); referința nouă e cea în Turbo.

**MemTest86 Free 11.7: TRECE** (5 nov. 22:28 → 6 nov., 3 h 12 min; originalele copiate de pe stick în `hardware/`: raportul `MemTest86-Report-20261105-222858_038611.html`, SHA-256 `d5d57133…7df5e89`, și jurnalul `MemTest86-20261105-222808_938424.log`; transcrierea făcută înainte, când stick-ul nu era conectat, e păstrată ca `_transcriere_MemTest86-Report.html.bak`). Jurnalul: 4 treceri, fiecare cu „Cumulative error count: 0”, „Test result: PASS (Errors: 0)” la 01:41; controlerul de memorie raportează „Ch mode: 2”, fără ECC (așa cum e modulul); singurele avertismente sunt despre fonturi (glife lipsă). 48 din 48 de teste (testele 0–10 și 13 „Hammer”, câte 4 treceri), **0 erori**, toate procesoarele în paralel, intervalul 0x0–8B0800000. Configurația văzută de MemTest86: **DDR4 3192 MT/s, x2 Channel**, 22-22-22-52, 1,2 V, două SPD-uri identice (Samsung M471A2K43EB1-CWE, 2Rx8, serii 37AF60BF și 34FD16A0). Temperatura procesorului: min / max / medie **58 / 83 / 69 °C** (după schimbarea pastei). Raportul conține seriile laptopului și ale plăcii de bază: **nu intră în nicio arhivă publică.**

**Stare hardware: verificat complet** (identitate, canal dublu de două ori, Windows Memory Diagnostic, MemTest86, 19/19 verificări, G7 identic bit cu bit, Turbo). Calibrarea rămâne blocată doar de protocol (corecturile Deep Review, v0.5), nu de hardware.

## 12. Două verificări pe CPU înainte de brațul LM (6 nov. 2026; `g2_cpu_checks.py`, jurnalul în `runs/g2_cpu_checks_2026-11-06.log`; orb față de T1)

**(a) G2 cu familia F3 lăsată complet deoparte** (F3 e singura familie de test cu reporniri ale ratei; antrenare pe tech3_F2, tech2_F1, tech2_F2; test pe tech3_F3 și tech2_F3). R² în afara familiei:

| D | OLS pe B_strong | GBDT pe B_strong | ΔN | ΔN + Ση (C3) | **ΔN + Ση‖m̂‖ (C5d)** | ΔN + C3 + C5d + C5e |
|---|---|---|---|---|---|---|
| D1 | −9,6 / −15,1 | 0,94 / 0,92 | −0,10 / −0,02 | la fel ca ΔN | **0,96 / 0,95** | 0,62 / 0,65 |
| D1_rel | −19,1 / −14,4 | 0,85 / 0,85 | −0,18 / −0,04 | la fel | **0,95 / 0,83** | 0,68 / 0,64 |
| D2 | −1,5 / −1,5 | 0,93 / 0,85 | −0,09 / −0,02 | la fel | **0,99 / 0,98** | 0,66 / 0,67 |
| D3 | −41 / −52 | 0,79 / 0,68 | −0,31 / −0,26 | la fel | **0,87 / 0,31** | 0,63 / 0,28 |

(prima valoare: tech3_F3, fără reguli; a doua: tech2_F3, cu reguli.) Citire: **scalarul cu sens fizic, Ση‖m̂‖, extrapolează la repornirile ratei** (D1, D2 ≥ 0,95), pe când modelele flexibile extrapolează prost (OLS pe cele 58 de trăsături: catastrofal; combinațiile coliniare C5d/C5e se despart arbitrar când η e constant la antrenare). Ση singur nu poate fi învățat din familii cu rată constantă (coeficient nedeterminat). D3 rămâne cel mai puțin reconstructibil, mai ales cu reguli (0,31). Consecință pentru G2: poarta trebuie definită pe scară (competitori minimi), nu pe „B_strong cu orice model”; un GBDT pe tot setul nu e o limită superioară sigură în afara distribuției.

**(b) Unde cedează „ΔN + rata C5d”** (OLS, o rulare lăsată deoparte; R² global D1 0,93, D3 0,80). Fiecare interval începe la un început de segment (N0 pe o graniță în 100% din cazuri), deci tranzitoriul de după graniță apare ca intervale scurte. Eroarea absolută relativă la rata medie, D1: 0,23 (ΔN 64–127), 0,14 (128–255), 0,085 (256–511), 0,084 (512–1.279), fără deplasare sistematică (−0,04 … 0); D3: 0,22 / 0,21 / 0,16 / 0,14. Cu o repornire a ratei în interval (6,7% din pondere): deplasare −0,05 la D1 și **−0,21 la D3** (predicția supraestimează rata după repornire). Deci aproximarea cedează exact unde prezicea documentul de literatură (după granițe și reporniri), mai mult pentru D3. În setarea FOREVER (optimizator și program reluate la fiecare fază) asta e regula, nu excepția: motivul pentru care brațul LM e informativ.

## 13. Brațul LM în programul FOREVER: pregătire și determinism pe GPU (6 nov. 2026)

Scripturi noi în `lm/`: `lm_forever_run.py` (programul FOREVER copiat din codul lor, commit `bbeb549`: calibrare pe 24 de pași, praguri d·τ_zi, faze curente oprite la prag, repetiții ne-contorizate cu regularizare spre θ*, repetiție finală, optimizator, program de rată și GradScaler noi la fiecare fază; abaterile declarate în antet), `lm_forever_g2.py` (analiza, orbă față de `evals.npz`), `lmtech1_criterii.md` (criteriile, fixate înainte), `launch_lmtech1.sh`. Telemetria pe pas: η, pierderea, ‖g‖ înainte și după tăiere, pașii săriți de GradScaler, ‖m̂‖, √Tr v̂, Δ_t pe factori (τ) și pe ΔW = 2·B·A (exact, prin identitatea Gram de rang 2r), μ, β; sonde (128 de prompturi neantrenate, log-probabilitățile celor 31 de cuvinte-răspuns) la fiecare 8 pași contorizați.

**Determinism pe GPU: TRECE pe proba scurtă.** Două rulări identice (2 sarcini × 4 epoci, 134 de pași, SDPA, `torch.use_deterministic_algorithms(True)`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`) dau `steps.npz`, `probes.npz`, `evals.npz` și factorii finali identici bit cu bit (`runs/lm_smoke/a`, `b`). Proba confirmă și structura fazelor (sarcina 1: calibrare, repetiție, curentă, repetiție, curentă, repetiție finală), primul pas al fiecărei faze la rata 0 (ca în HF) și 3 pași săriți de GradScaler din 134. VRAM maxim 1,7 GB. Pe GPU, în Turbo: ~70 °C, 62–73 W din 95 W, 1.965–1.980 MHz.

**lmtech1: rezultate (6 nov., 16:36–17:37, 61 min față de ~1 h estimat; `runs/lmtech1_g2.log`, `runs/lmtech1_posthoc.log`).** 3 rulări × 10 sarcini × 512 fapte, ~15 min pe rulare (858–922 s). **G7-GPU pe rularea completă: TRECE** (repetarea lui 7101: toate fișierele identice bit cu bit). **Validitate: două criterii fixate dinainte PICATE:** acuratețea pe sarcina curentă < 0,95 la ultimele sarcini în 2 din 3 rulări (7101: 0,920 la sarcina 9; 7102: 0,941 la sarcina 8) și pașii săriți de GradScaler 4,1% (> 2%). Rezultatele sunt deci **descriptive**.
- Analiza fixată (869 de ferestre de 8 pași, R² în afara rulării, mediu): rata lui τ din **Ση 0,67**, Ση‖g̃‖ 0,86, **Ση‖m̂‖ 0,94**, câmpul mediu 0,94, Ση + Ση‖m̂‖ 0,96, GBDT pe toată telemetria 0,986. Pe ΔW: 0,65 / 0,86 / 0,89 / 0,89 / 0,91 / 0,994. **D3:** 0,49 / 0,69 / 0,64 / 0,64 / 0,66 / 0,94.
- **Predicția scrisă pe 4 nov. („Ση explică cea mai mare parte din τ”, R² ≥ 0,80) PICĂ** la nivel de fereastră (0,67). Reziduul lui „y ~ Ση”: subestimare de 48–85% în primele ferestre ale fiecărei faze (pasul Adam după resetarea momentelor e mai mare pe unitatea de η), supraestimare de ~22% mai târziu în fazele curente.
- **Post hoc (explorare):** (1) Ση doar pe pașii aplicați nu ajută (0,655); (2) la nivel de fază, R² 0,99 al lui τ din Ση e un artefact al duratei: pașii singuri dau 0,987, iar rata pe fază (τ/n) din Ση/n are R² doar 0,18; (3) în 160 de pași pe sarcină se ating doar pragurile d = 1, 2, 4 (nu 7): un ceas doar din program ar declanșa repetiția de la d = 2 practic în același pas (mediana −1 pas) și pe cea de la d = 4 cu ~9 pași mai devreme (din ~85).
- Citire provizorie: în setarea FOREVER, τ nu e redus la programul ratei, dar e reconstruit aproape complet de telemetria optimizatorului (Ση‖m̂‖ 0,94; totul 0,986), ca în lumea sintetică. Funcțional (D3) rămâne cel mai puțin reconstructibil din scalari ieftini.

## 14. Corecturile de cod din recenzia Deep Review (6 nov. 2026, seara; pasul 1 din §4 al verificării recenziei)

Copii vechi: `_work\_copii_siguranta\stadiul0_inainte_corecturi_DR_2026-11-06\` (cu `SHA256SUMS.txt`). Aplicate:
- **D2:** `max_ctx: 4` (intrările au 4 tokeni).
- **D3:** `optim.wd_embeddings: false`: embedding-ul de intrare și cel pozițional scoase din weight decay; stratele liniare și capul rămân. **Provizoriu: decizia (c) a autorului e deschisă** (varianta recomandată). Aranjamentul bufferului: matricele cu decay, apoi cele fără, apoi biasurile și LayerNorm; `layers` (pentru D1_rel) conține toate matricele, ca înainte; `theta_dec_norm` rămâne norma matricelor cu decay. Cu `wd_embeddings: true` aritmetica e identică cu cea veche.
- **D4:** suprapunerea q_hist calculată la începutul segmentului s₀ (prima expunere: NaN, fără istoric).
- **A3:** L̄_A,clip și L̄_B,clip (pierderea tăiată la ln 64) în `evals` (`LAc`, `LBc`); în tripleți `F_A_clip`, `F_B_clip`.
- **D5:** C10c (media pe itemi a lui |Δℓ| pe R, din aceeași trecere ca D3) în fragmente și tripleți; `x_LR0` = L_R(t₀) în X_cov.
- **D1:** C0 = ticuri de pauză (Δc_a − ΔN), zero pe F1–F3. Atenție: tripleții vechi (parquet) au încă C0 = Δc_a; nu se regenerează retroactiv.
- **D9:** blocul D2 la 16 pași (`run.d2_block: 16`), decalaj în [256, 271].
- `launch.py`: nu mai pornește rulări noi dacă există `runs/_HW_STOP` (paznicul hardware).
- `checks_stage0.py`: **27/27** (6 verificări noi: context = lățimea intrării; rândurile de embedding nefolosite rămân neschimbate; C10c ≥ C10b; L_clip ≤ L și ≤ ln 64; prima suprapunere NaN; plus AdamW bit-identic cu grupurile noi).

**Paznicul hardware** (`hw_watchdog.py`, pornit 6 nov. 17:21 până luni 9 nov. 08:00): la 30 s jurnalizează GPU (temperatură, putere, frecvență, încetinire termică), zona termică ACPI (`\_TZ.THRM`, în kelvini; sub sarcină GPU 77–93 °C), limita pasivă (100% = fără limitare de firmware), performanța procesorului, priza și discul, în `runs/_hw/`. Oprește rulările și scrie `runs/_HW_STOP` la GPU ≥ 87 °C (90 s), încetinire termică GPU (90 s), zona termică ≥ 97 °C (90 s), limită pasivă < 100% (3 min), baterie (60 s) sau disc < 10 GB. Ține Windows treaz cât rulează (fără să schimbe setări). Windows Update e pe pauză până pe 15 nov. (făcut de utilizator).

## 15. lmtech2 și tech4 (6 nov. 2026, seara)

**lmtech2** (GPU, 17:38–18:00, 22 min față de 25–30 estimat; 256 de fapte pe sarcină; `runs/lmtech2_g2.log`, `runs/lmtech2_posthoc.log`). ~7,4 min pe rulare. **Criteriul de învățare pică din nou, mai tare:** 0,852 (7201, sarcina 8), 0,848 (7202, sarcina 8), 0,934 (7203, sarcina 9); scăderea crește cu indicele sarcinii, deci nu vine din numărul de fapte. Ipoteza de lucru: repetiția finală (pe 16·t fapte vechi, 2 epoci) chiar înainte de evaluare, tot mai lungă la sarcinile târzii. De verificat cu diagnosticul `lm/launch_lmdiag.sh` (acuratețea înainte de repetiția finală, cu antrenare identică bit cu bit). Pași săriți: 5,9%. **G2 reproduce lmtech1:** rata lui τ din Ση 0,58, Ση‖g̃‖ 0,84, Ση‖m̂‖ 0,95, Ση + Ση‖m̂‖ 0,97, GBDT 0,976; D3: 0,36 / 0,64 / 0,53 / 0,55 / 0,93. Post hoc: rata pe fază din Ση/n, R² 0,09; repetiția de la d = 2 declanșată de un ceas doar din program în același pas (mediana −1); d = 4 nu se atinge în 80 de pași.

**tech4** (CPU, 4 procese, 18:01–18:30, **29,3 min față de 40–45 estimat**; `runs/tech4_analysis.log`, `tech4_analysis.py`). Toate cele 6 rulări valide.
- **Copilăria după scoaterea embedding-urilor din weight decay: trece în 6 din 6** (0,982–0,985).
- **Debit în Turbo: 6 rulări în 29,3 min = 12,3 rulări pe oră** (tech3: ~9,5). Valul de 4: 982–1.084 s pe rulare (copilăria 88–90 s, antrenarea 625–665 s, evaluările 112–166 s, fragmentele 115–119 s); valul de 2: 762–764 s. Memoria maximă ~864–884 MB pe proces; parametri 925.440 (max_ctx 4), din care 851.968 cu weight decay.
- **Temperaturi (paznicul):** zona termică mediană 91 °C, maxim 95 °C; limita pasivă 100% (fără limitare); performanța procesorului ~126%. Pragul paznicului rămâne 97 °C (confirmat de utilizator).
- **Viteza uitării, fără plafon** (medii pe episod): T1-acc (dAcc_A) la ΔN 64–255 / 256–639 / 640–1.279 / 1.280–2.047 / ≥ 4.096: F1 0,11 / 0,40 / 0,67 / 0,83 / 0,98; F6 0,29 / 0,64 / 0,79 / 0,87 / 0,98; F5 0,27 / 0,60 / 0,84 / 0,94 / 0,98. **F6 uită mai repede la intervale scurte** (zgomotul etichetelor din distractori), dar mai încet pe scara pierderii la intervale lungi (F_A 6,8 față de 9,2 nați la ≥ 4.096). F^clip se saturează la ~3,9–4,0 nați (ln 64 = 4,16). Plafonul ΔN < 1.280 păstrează regiunea în care uitarea nu e completă.
- **G2 pe tech4** (o familie lăsată deoparte, antrenare pe celelalte 5): Ση‖m̂‖ reconstruiește D1 0,86–0,95, D2 0,98–0,99, D1_rel 0,67–0,87; **noul competitor C10c reconstruiește D3 aproape complet în F2, F3, F5 (0,95–0,99)**, dar nu în F6 (0,59; C5d 0,18; GBDT 0,81). Citire: pe fapte, distanța funcțională D3 (JS pe R) și C10c (|Δℓ| pe itemii din R, aceleași treceri) poartă practic aceeași informație; D3 nu mai e „singurul candidat cu informație proprie” față de un competitor de același cost. **F6 rămâne cazul în care niciun scalar nu ajunge.** Consecință pentru v0.5: C10c e obligatoriu în scara de competitori a lui D3, iar contrastul F6 e locul unde se poate vedea ceva nou.

**Lanțul 2, primele rezultate (6 nov., 18:56–19:13).** (1) **Fixarea pe nuclee (Deep Review B7, `pin_test.py`, `runs/pin_test_2026-11-06.json`):** 4 copilării în paralel: libere 94–95 s fiecare; fixate pe nucleele P (logice 0, 2, 4, 6) 77–82 s (**−15%**); pe nucleele E (8–11) 150–152 s (+60%); acuratețea identică în toate cele trei condiții (determinism independent de nucleu). `launch.py` are acum opțiunea `--pin-pcores` (cel mult 4 procese). (2) **G7 pe o rulare completă cu codul corectat:** tech4 F6_s9005 refăcută singură în 638 s (față de 762 s în valul de 2): **toate tablourile identice bit cu bit**.

**Lanțul 2, sensibilitățile LM (6 nov., 19:13–20:41; lanțul întreg 18:56–20:41, 1 h 45 min față de ~1 h 50 estimat; `runs/lmsens_bf16_g2.log`, `runs/lmsens_a32_g2.log`).** Semințele lmtech1 (7101–7103), 512 fapte pe sarcină, analiza fixată `lm/lm_forever_g2.py` (aceeași amprentă ca la lmtech1, `546311e6…`), câte o singură schimbare: (3) **bf16 fără GradScaler** (abatere de la FOREVER), 871–885 s pe rulare; (4) **α = 32** (valoarea din articol), 886–888 s pe rulare. R² în afara rulării pentru rata lui τ (lmtech1 / bf16 / α 32): Ση 0,669 / 0,648 / 0,686; Ση‖g̃‖ 0,858 / 0,848 / 0,879; **Ση‖m̂‖ 0,944 / 0,958 / 0,941**; Ση + Ση‖m̂‖ 0,960 / 0,969 / 0,956; GBDT 0,986 / 0,986 / 0,988. Pe ΔW: Ση‖m̂‖ 0,887 / 0,900 / 0,922, GBDT 0,994 / 0,995 / 0,992. D3: Ση 0,490 / 0,475 / 0,460; Ση‖g̃‖ 0,693 / 0,635 / 0,672; Ση‖m̂‖ 0,639 / 0,605 / 0,661; GBDT 0,941 / 0,937 / 0,941. La nivel de fază, Ση 0,991 în toate trei (artefactul duratei). **Validitate:** înainte de repetiția finală, acuratețea pe sarcina curentă ≥ 0,998 la toate sarcinile, în toate cele 6 rulări (criteriul fixat: TRECE); după repetiția finală, minimul 0,957 (bf16) și 0,973 (α 32), deci ≥ 0,95 chiar și după repetiție în toate cele 6 (la lmtech1, pe aceleași semințe: 0,920 și 0,941). Pași săriți: 0 cu bf16; cu α 32, 304 din 6.984 de pași în ferestre (4,4%; lmtech1 4,1%). **Citire:** rezultatul reconstrucției nu depinde de pașii săriți din fp16 și nici de α; predicția „Ση explică cea mai mare parte din τ” pică în toate trei configurațiile (0,65–0,69 < 0,80). Cu 3 semințe pe configurație, diferența acurateței de după repetiție nu se atribuie unei cauze. **Lipsă observată la redactarea dosarului colocviului:** pe brațul LM nu s-a calculat analogul lui C10c (|Δ pierdere pe item| pe aceleași sonde), deși `probes.npz` îl permite (fiecare sondă are un cuvânt-răspuns aleator, neantrenat); în dosar e trecut la „ce nu spun rezultatele”, nu s-a rulat.
