# Testul T-C (colocviul din 6 nov. 2026): concurenții de același cost ai lui D3 pe brațul LM. Criterii fixate ÎNAINTE de calcul (6 nov., ~22:45)

Propus de Mistral (T3), ChatGPT (testul 3) și Deep Review (testul 1a); vezi `02_Pilot2/Colocviu/Verificare_raspunsuri_2026-11-06.md` §10. Descriptiv și orb față de T1: se citesc doar `probes.npz` și `steps.npz`; `evals.npz` nu se deschide.

**Date:** rulările existente `lmtech1`, `lmtech2`, `lmsens_bf16`, `lmsens_a32` (câte 3 semințe). **Intervalele lui D3**, exact ca în `lm_forever_g2.py`: perechi de sonde consecutive ale aceleiași sarcini, fără pas de repetiție în interval; y = schimbarea RMS a log-probabilităților (128 de sonde × 31 de cuvinte) / pașii contorizați.

**Concurenții** (din aceleași treceri, ca rate pe pas contorizat, pe același interval; a_i = cuvântul-răspuns aleator, neantrenat, al sondei i, regenerat din sămânța lumii):
- C10c_LM = mean_i |Δ(−log p_i(a_i))| (analogul direct al lui C10c);
- P_LM = mean_i |Δ p_i(a_i)| (mărginit);
- H_LM = mean_i |ΔH(p_i)| (schimbarea entropiei pe cele 31 de cuvinte);
- raportat, dar **nefolosit la verdict** (aproape-duplicat al lui D3, aceeași diferență în altă normă): L1_LM = mean_{i,w} |Δ log p_i(w)|.

**Modele** (R² în afara rulării, o sămânță lăsată deoparte, în fiecare configurație): (a) OLS pe C10c_LM; (b) OLS pe C10c_LM + P_LM + H_LM; (c) OLS pe Ση‖m̂‖ + C10c_LM + P_LM + H_LM; (d) GBDT pe telemetria completă din `lm_forever_g2.py` + cei trei concurenți.

**Verdictul (fixat):** dacă media R² a modelului (b) e ≥ 0,90 în toate cele 4 configurații, **D3 pe brațul LM e reconstruit de concurenții de același cost**, iar pretinsul lui rest informațional se închide pe acest braț. Dacă e < 0,90 în toate 4: **D3 e distinct** de concurenții de același cost pe acest braț. Altfel: **mixt**. Se raportează și (a), (c), (d) și minimul pe semințe.
