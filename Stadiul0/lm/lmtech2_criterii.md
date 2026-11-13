# Runda tehnică lmtech2 (criterii fixate ÎNAINTE de rulare, 6 nov. 2026, după rezultatele lmtech1)

**De ce:** lmtech1 a încălcat două criterii de validitate fixate dinainte: acuratețea pe sarcina curentă < 0,95 la ultimele sarcini în 2 din 3 rulări (7101: 0,920 la sarcina 9; 7102: 0,941 la sarcina 8) și pașii săriți de GradScaler 4,1% (> 2%). Rezultatele lmtech1 rămân descriptive și se raportează așa.

**Schimbarea unică:** 256 de fapte pe sarcină în loc de 512 (aceleași 10 expuneri pe fapt; programul FOREVER neschimbat: 10 epoci, 60 la prima sarcină). Semințele 7201, 7202, 7203. Același script (`lm_forever_run.py`, SHA-256 neschimbat), aceeași analiză fixată (`lm_forever_g2.py`); analizele post hoc din lmtech1 (`lm_forever_posthoc.py`) se rulează și aici, tot ca explorare.

**Criterii de validitate:**
- acuratețea pe sarcina curentă la sfârșitul fiecărei sarcini ≥ 0,95 (doar diagonala);
- pașii săriți de GradScaler: **raportați, fără prag**. Motiv: sunt o proprietate a setării FOREVER (fp16, un GradScaler nou la fiecare fază, scara inițială 65.536); pragul de 2% fusese fixat pe o probă de 2 sarcini. Analiza scării include oricum numărul pașilor săriți (lmtech1: corecția nu schimbă rezultatul, 0,655 față de 0,669);
- nicio pierdere nefinită; `meta.json` cu amprentele.

**Estimarea de timp:** ~8–9 min pe rulare (sarcina 0: 480 de pași × 0,32 s; sarcinile 1–9: câte 80 de pași plus repetiții), ~25–30 min în total.
