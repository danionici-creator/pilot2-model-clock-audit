# Preînregistrarea testelor decisive T-A și T-B (colocviul Pilot 2, 6 nov. 2026)

**Scrisă și amprentată ÎNAINTE de orice rulare a acestor teste** (6 nov. 2026, ~23:05). Testele vin din colocviu (`02_Pilot2/Colocviu/Verificare_raspunsuri_2026-11-06.md` §10): T-A propus de toți cei 5 participanți, T-B de 4 din 5. Pornirea lor e aprobată de utilizator („Yes, start”, 6 nov.). Deciziile colocviului aplicate: Stadiul 0 împărțit (0a orb față de T1, singura fază în care se poate schimba designul; 0b automat după blocare), bf16 pe brațul LM, C10c obligatoriu, criteriul de învățare LM citit înainte de repetiția finală, embedding-urile complet fără weight decay (cum e deja în cod).

**Reguli comune.** Nimic din această fișă nu se schimbă după ce se văd datele. Orice abatere se notează explicit, cu motivul, în `Predare_fir.md`. Scriptul de analiză al părții H1 (T-B, partea 2) se scrie după această fișă, dar **înainte de deschiderea coloanelor T1**, și se amprentează în `Predare_fir.md` înainte de rulare. Paznicul hardware rămâne pornit; o rulare oprită de el se reface identic (rulările sunt deterministe), fără nicio altă schimbare.

---

## T-A. Planificatorul FOREVER condus de ceasuri diferite (brațul LM, GPU)

**Întrebarea:** declanșarea repetițiilor după τ (timpul centrat pe model, FOREVER) reduce uitarea mai mult decât declanșarea după un ceas ieftin?

**Configurația:** `lm/lm_forever_run.py` (amprenta în `runs/preinregistrare_sha256.txt`), Qwen3-0.6B + LoRA r = 8, α = 16 (valoarea din codul FOREVER), **bf16**, 10 sarcini × 512 fapte, 60 de epoci pe sarcina 0 și 10 pe celelalte, batch 32, η 3·10⁻⁴, memorie 16 fapte pe sarcină; `--diag_pre_final --diag_pre_final_all`. Patru ceasuri (`--clock`), aceeași calibrare pe primii 24 de pași și aceleași praguri d × zi: **tau** (FOREVER), **eta_m** = Ση‖m̂‖, **eta** = Ση aplicat (doar programul), **steps** = pași contorizați. Ponderea β a repetiției rămâne calculată din τ în toate brațele (doar *când* se repetă diferă). Varianta tau e identică bit cu bit cu scriptul dinainte (proba `runs/ta_smoke2`). **Semințe noi: 7301–7305** (5 perechi). 20 de rulări, în ordinea sămânță cu sămânță (toate cele 4 ceasuri pe o sămânță, apoi următoarea).

**Rezultatele fixate:**
- **E1 (primar):** acuratețea medie finală pe cele 10 sarcini, după ultima repetiție finală (ultimul rând din `evals.npz`).
- E2: BWT = media pe t < 9 a (acc_final[t] − acc la sfârșitul sarcinii t[t]).
- E3: acuratețea medie pe sarcinile vechi chiar înainte de fiecare repetiție finală (`evals_pre.npz`), mediată pe sarcinile 1–9.
- E4: numărul de repetiții și diferența pașilor de declanșare față de τ (mediana |Δ| pentru fiecare d atins).

**Criteriile** (marja δ = 0,02, adică 2 puncte procentuale; comparații pereche pe sămânță: τ față de fiecare alt ceas, pe E1):
- **Separarea** (precondiția ChatGPT): dacă mediana |Δ pas de declanșare| ≤ 2 pentru toate pragurile atinse, cele două ceasuri sunt **echivalente ca planificare** în acest cadru. Asta e un rezultat în sine (redundanța lui τ ca planificator), oricum ar ieși E1.
- **τ superior** lui X: media diferențelor E1(τ) − E1(X) ≥ 0,02 și intervalul t pereche 95% nu conține 0.
- **Echivalență practică:** intervalul t pereche 95% al diferenței e cuprins în (−0,02; +0,02).
- **Altfel: neconcludent** (nu dovadă de egalitate).

Citirea pentru nota FOREVER: dacă τ e echivalent cu eta_m (și cu eta), valoarea lui de planificator e reprodusă de un ceas gratuit în acest cadru. Dacă τ e superior, are valoare de planificator dincolo de telemetrie în acest cadru. E2–E4 se raportează. **Limite declarate:** fapte sintetice, un singur model mic, abaterile de la FOREVER din dosar, 5 semințe (putere mică; un interval lat dă „neconcludent”).

**Durata estimată:** 20 × ~15 min ≈ **5 h** pe GPU.

---

## T-B. D3 sub zgomot dozat, pe semințe noi, contra concurenților de același cost (lumea sintetică, CPU)

**Întrebarea:** schimbarea funcțională D3 conține, în regimul cu distractori zgomotoși (F6), informație pe care nici telemetria, nici concurenții de același cost nu o au, și prezice ea uitarea dincolo de aceștia?

**Configurația:** `p2/run.py`, `p2/triplets.py` (amprentele în `runs/preinregistrare_sha256.txt`), `config_stage0.yaml` neschimbat. Noii concurenți de același cost, din aceeași trecere ca D3: **C10p** = media |Δ p(țintă)| și **C10h** = media |Δ entropia ieșirii| pe bateria R, acumulați pe aceleași blocuri de 8 pași ca D3 și C10c (antrenarea rămâne identică bit cu bit: controlul `runs/tech4_g7_TB`). Condiții: **F6 cu zgomotul etichetelor 0 / 0,1 / 0,3 / 0,5** (`--set families.F6.label_noise=x`) și **F1** drept control fără zgomot (a doua familie slabă la scalarul ieftin, corectura E4). **Semințe noi: 9101–9108** (8 pe condiție), deci 40 de rulări, 4 procese fixate pe nucleele P.

### Partea 1: Stadiul 0a, G2 (orb față de T1; F_A, F_B, dAcc_A nu se citesc)
Ținta: rata lui D3 pe tripleți (ΔN ∈ [64; 1.280), includerea din protocol). Modele, cu o sămânță lăsată deoparte **în interiorul fiecărei condiții**: (i) ΔN + C10c; (ii) ΔN + C10c + C10p + C10h; (iii) **GBDT pe B⁺** = ratele telemetriei (fără C6) + X_cov + termenii în ΔN + C10c + C10p + C10h (hiperparametrii din `tech4_analysis.py`).
- **G2-F6 trece** (D3 nu e reconstruit) dacă, la zgomot 0,3, R² al lui (iii) e < 0,90 pentru **cel puțin 6 din 8** semințe testate.
- **Doza–răspuns** (Mistral T2): u(z) = 1 − R² mediu al lui (iii) la zgomotul z; trece dacă u crește strict cu z pe cele 4 niveluri (Spearman = 1) și u(0,3) ≥ 2 · u(0).
- Se raportează: aceleași modele pentru D1_rel (excepția E2) și pentru F1.
- **Dacă G2-F6 nu trece:** D3 e reconstruit de concurenții de același cost și în F6, H1 nu e identificabil (regula protocolului), **D3 se închide** ca indice experiențial în acest cadru, iar partea 2 nu se rulează.

### Partea 2: Stadiul 0b, H1 (automat, doar dacă partea 1 trece)
Ținta **T1 = F_A** (creșterea pierderii pe jumătatea A); ținta secundară T1_acc = dAcc_A. Pe fiecare rulare F6 la 0,3, validare încrucișată în 5 pliuri pe **sarcini** (toți tripleții unei sarcini în același pliu). Model de bază: GBDT pe B⁺; model extins: B⁺ + rata lui D3 + ΔD3 cumulat. **ΔR²** = R²(extins) − R²(bază), în afara pliului, pe rulare.
- **H1-F6 susținut** dacă media ΔR² pe cele 8 semințe e ≥ 0,02, **și** ΔR² > 0 în cel puțin 6 din 8 semințe, **și** marginea de jos a intervalului bootstrap 95% pe semințe (10.000 de reeșantionări) e > 0, **și** semnul e același pe T1_acc.
- **Altfel: H1-F6 nesusținut, D3 se închide.**
- Replicarea la 0,1 sau 0,5 (Copilot) se raportează ca secundară, nu e condiție.

**Durata estimată:** 40 de rulări în 5 loturi de câte 8 (4 procese, 2 valuri de ~17 min pe lot) ≈ **2 h 50 min** pe CPU, în paralel cu T-A.

---

**Ce NU se testează aici** (propus de un singur participant, doar listat): reziduul pe pas al lui D1 (Mistral), datele naturale SuperNI (Gemini, Deep Review), controlul distanță netă / D3_shuffled (Deep Review; DeepSeek ca martor), F2 cu zgomot (ChatGPT).
