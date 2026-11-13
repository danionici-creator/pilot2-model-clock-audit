# Testul T-D (colocviul din 6 nov. 2026): auditul reconstrucției pe jurnalele existente. Criterii fixate ÎNAINTE de calcul (6 nov., ~22:55)

Propus de Copilot (testul 3), ChatGPT (testul 1) și Deep Review (artefactele 1–4); `02_Pilot2/Colocviu/Verificare_raspunsuri_2026-11-06.md` §10. Orb față de T1 (F_A, F_B, dAcc_A nu se citesc). Partea cu semințe noi și analiză înghețată vine din T-B; aici doar jurnalele existente.

1. **Fără trăsături circulare** (eroarea E1): pe datele R1 (tech2/tech3, `g2_preview.py`), OLS și GBDT pe B_strong **fără C6_*** (statisticile lui D1 însuși și ale pasului Adam la capetele intervalului), față de B_strong complet.
2. **Mecanismul lăsat deoparte** (Deep Review): pe tech4, scara de scalari ieftini (ΔN, ΔN + Ση‖m̂‖, ΔN + C10c) și GBDT; teste pe F1, F2, F3, F4, F6; pentru F2, F3, F4 antrenarea **exclude și F5** (familia compusă).
3. **Benzi de ΔN** (Copilot, ChatGPT, Deep Review): pe tech4, o familie lăsată deoparte, R² și eroarea relativă a lui ΔN + Ση‖m̂‖, separat pe 64–127 / 128–255 / 256–639 / 640–1.279.
4. **Transfer între configurații pe brațul LM** (Deep Review): rata lui τ pe ferestre de 8 pași; OLS pe Ση + Ση‖m̂‖ și GBDT antrenate pe lmtech1, testate pe lmtech2, lmsens_bf16, lmsens_a32; plus minimul pe semințe în lmtech1.

**Citirea fixată:** reconstrucția ceasurilor din parametri e **robustă** dacă R² ≥ 0,90 se păstrează pentru D1 și D2 în (1) fără C6, (2) cu scalarul ΔN + Ση‖m̂‖ și mecanismul lăsat deoparte, (4) cu modelul liniar transferat, pentru τ. Unde pică, se redeschide doar scara sau regimul acela (regula lui Copilot), nu toată linia. D1_rel și D3 se raportează, dar nu intră în citire (au deja excepția F6).
