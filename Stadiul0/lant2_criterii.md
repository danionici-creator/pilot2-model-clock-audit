# Lanțul 2 (6 nov. 2026, seara): criterii fixate ÎNAINTE de rulare

Toate sunt măsurători tehnice, descriptive, nepreînregistrate; niciuna nu leagă c_e de uitare.

1. **Fixarea pe nuclee (Deep Review B7)**, `pin_test.py`: 4 copilării în paralel (3.072 de pași, ca într-o rulare), în trei condiții: libere, fixate pe cele 4 nuclee P (procesoarele logice 0, 2, 4, 6), fixate pe 4 nuclee E (8–11). Se raportează timpul; acuratețea trebuie să fie identică în toate condițiile (determinism). **~5 min.**
2. **G7 pe o rulare completă cu codul corectat:** tech4 F6_s9005 refăcută singură (`runs/tech4_g7`), tablourile comparate cu tech4 prin amprentele din `meta.json`. **~10–13 min.**
3. **Brațul LM, sensibilitatea la precizie:** lmtech1 cu `--precision bf16` (fără GradScaler, deci fără pași săriți; abatere de la FOREVER), semințele 7101–7103, 512 fapte. **~45 min.**
4. **Brațul LM, sensibilitatea la α:** lmtech1 cu `--alpha 32` (valoarea din articolul FOREVER; codul lor are 16). **~45 min.**

La 3 și 4: analiza fixată `lm/lm_forever_g2.py`, comparată cu lmtech1 (aceleași semințe); `--diag_pre_final` pornit; **criteriul de învățare se citește înainte de repetiția finală** (≥ 0,95; diagnosticul din 6 nov. a arătat că scăderea de după vine din repetiția finală), iar valoarea de după repetiție se raportează. Pașii săriți se raportează.

**Durata totală estimată: ~1 h 50 min** (start ~19:00, sfârșit ~20:50). Paznicul hardware rămâne pornit; fiecare etapă verifică `runs/_HW_STOP`.
