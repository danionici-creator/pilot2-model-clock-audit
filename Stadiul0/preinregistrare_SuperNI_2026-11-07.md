# Preînregistrarea verificării pe SuperNI (S1, S2), 7 nov. 2026, ÎNAINTE de rulare

**De ce:** controlul lipsă numit de Gemini (G2 pe date naturale, nestaționare) și testul propus de Deep Review (5 sarcini SuperNI eterogene). Concluzia testelor din noaptea 6–7 nov. (`02_Pilot2/Rezultate_teste_decisive_2026-11-07.md`) e limitată la fapte sintetice; aici se verifică dacă ea se extinde la sarcini naturale. Pornirea a fost cerută de utilizator („SuperNI check first”), iar descărcarea datelor aprobată („Yes, download”).

**Datele:** `D:\Time\_date\FOREVER_bbeb549\data_superni` (din depozitul FOREVER, commit `bbeb549a21e5…`, verificate cu amprentele git; `SHA256SUMS.txt`). Primele 5 sarcini din ordinea 7 a FOREVER: task1572, task363, task1290, task181, task002 (generare și clasificare; 160–1.000 de exemple; mediana între 106 și 512 tokeni).

**Configurația:** `lm/lm_superni_run.py` (amprenta în `runs/preinregistrare_SuperNI_sha256.txt`). Programul FOREVER ca în `lm_forever_run.py`, cu setările scriptului lor pentru Qwen (`scripts/run_train_cl_ours_qwen.sh`): micro-batch 4 × 8 = 32, maxim 512 tokeni, pierderea doar pe răspuns, 2 epoci pe memorie, ziua-model de 24 de pași, memoria 2% pe sarcină anterioară. Abateri declarate (în antetul scriptului): bf16; epoci 3 / 10 pe prima sarcină (ale lor: 10 / 60), pentru timpul laptopului; fără group_by_length; regula memoriei corectată la sarcinile de generare (ar lua ~toată sarcina); gradient checkpointing (nu schimbă matematica). **Semințe noi: 7401, 7402, 7403.**

## S1 (primar): reconstrucția lui τ pe date naturale eterogene
Rulările cu `--clock tau`. Ferestre de 8 pași contorizați în interiorul fazelor (ca `lm_forever_g2.py`); ținta: rata lui τ (media Δ_t). Predictori: Ση, Ση‖m̂‖, Ση + Ση‖m̂‖ (OLS), GBDT pe telemetrie (η, ‖g‖, ‖g̃‖, ‖m̂‖, √Tr v̂, pierdere, pasul în fază, tipul fazei, sarcina, tokenii de răspuns din pas).
Două scheme în afara eșantionului: (a) **o sămânță lăsată deoparte**; (b) **o sarcină lăsată deoparte** (toate semințele; testul de eterogenitate).
- **Reconstrucția se extinde la SuperNI** dacă OLS pe Ση + Ση‖m̂‖ are R² mediu ≥ 0,90 în **ambele** scheme.
- **Nu se extinde** dacă R² mediu < 0,90 în oricare schemă: concluzia „ceasul FOREVER = telemetria optimizatorului” rămâne limitată la faptele sintetice, cu regimul de eșec raportat (pe sarcină).
- Se raportează și Ση‖m̂‖ singur, GBDT și minimul pe pliuri.

## S2 (secundar): planificatorul pe SuperNI
Rulările cu `--clock eta_m` pe aceleași semințe, comparate pereche cu τ. Rezultatul: **E1 = media pierderii pe răspuns pe seturile de test ale celor 5 sarcini, după ultima repetiție finală** (mai mic e mai bine); secundar: pierderea pe sarcinile vechi chiar înainte de fiecare repetiție finală (`evals_pre.npz`) și separarea declanșărilor (mediana |Δ pas|).
- **Echivalență practică** dacă intervalul t pereche 95% al diferenței relative (E1(τ) − E1(eta_m)) / E1(τ) e cuprins în (−5%; +5%).
- **τ superior** dacă diferența relativă e ≤ −5% și intervalul nu conține 0.
- **Altfel: neconcludent.** Cu 3 semințe, puterea e mică; un interval lat dă „neconcludent”.

**Ordinea rulărilor:** întâi cele 3 rulări τ (S1), apoi cele 3 eta_m (S2). Utilizatorul poate opri după S1.
**Durata estimată:** ~65–70 min pe rulare: S1 ≈ 3,5 h, S2 încă ≈ 3,5 h.
