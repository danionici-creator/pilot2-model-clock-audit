# Preînregistrarea rulărilor repetate R1/R2 (8 nov. 2026, ÎNAINTE de rulare; versiunea 2)

Versiunea 1 (13:43) e păstrată în `_work\_copii_siguranta\forever_repetari_v1_2026-11-08\`, cu amprenta în `runs/forever_repro_sha256.txt`. Versiunea 2 (13:58) integrează observațiile Copilot verificate; lista schimbărilor e la sfârșit. Nicio rulare nouă nu a pornit între versiuni.

**De ce:** după R2 (`Rezultate_teste_decisive_2026-11-07.md`, secțiunea din 8 nov., ~13:45) a rămas o întrebare deschisă. Verdictul agregat e echivalență (ΔOP +0,84, ΔBWT +0,69), dar pe dbpedia (prima sarcină) τ dă 93,21, iar η‖m̂‖ 87,89 (**+5,33 puncte**). O singură pereche nu separă efectul ceasului de nedeterminism. Cerută de utilizator („Plan repeated runs”). Verdictul R2 rămâne cel înregistrat; rulările de aici îl completează și nu îl înlocuiesc.

**Fapte pe care se sprijină proiectul (verificate în cod și în fișiere):**
1. Codul lor fixează sămânța: `set_seed(42)` (`src/finetune_cl_our_qwen.py`, linia 31); amestecările (`shuffle()` fără sămânță) și eșantionarea memoriei derivă din ea. Deci R1 și R2 diferă **doar** prin ceas și prin nedeterminismul GPU (fp16, fără algoritmi deterministici).
2. Nedeterminismul e real: adaptoarele de după sarcina 0 diferă între R1 și R2 (`adapter_model.safetensors`: `636589d5…` în `ckpt_tau`, `66dc0d26…` în `ckpt_eta_m`); dbpedia imediat după sarcina 0: 98,04 față de 97,86.
3. Pe sarcina 0 nu există repetiții (2 faze în ambele rulări), deci ceasul nu influențează adaptorul sarcinii 0. Ambele adaptoare sunt puncte de plecare valide pentru oricare ceas.
4. Fiecare sarcină își calibrează ziua-model din propriii 24 de pași (`Phase 1: CALIBRATION CURRENT`), iar `DriftRecorderCallback` citește doar `drift_log.csv` din dosarul sarcinii curente. Copierea dosarului `0-dbpedia` nu transmite nimic din ceasul sarcinii 0 către sarcinile 1–3.
5. **Ce trece de la o sarcină la alta în codul lor: numai ponderile adaptorului.** Sarcina t > 0 încarcă `PeftModel.from_pretrained(model, <dosarul sarcinii t−1>)` (linia 330); `resume_from_checkpoint` nu e folosit de lansator. Fiecare fază construiește un Trainer nou (liniile 433, 553, 646, 719), deci optimizatorul AdamW (inclusiv m, v și contorul de pași), planificatorul ratei de învățare și scalerul fp16 pornesc de la zero la fiecare fază, în toate rulările. Generatoarele aleatoare se reinițializează cu 42 la import (linia 31) și în constructorul fiecărui Trainer (`set_seed(self.args.seed)`, transformers 4.57.0, `trainer.py` linia 452); fiecare sarcină e un proces nou. Memoria de repetiție se construiește din date (`load_memory_buffer`), nu din punctul de control. **Deci copierea dosarului `0-dbpedia` reproduce exact granița dintre sarcini din conducta lor**, iar η‖m̂‖ pornește de la un optimizator nou în ambele ceasuri, ca în R1 și R2.
6. **Punctul de plecare** (dbpedia imediat după sarcina 0, scriptul lor de BWT, extragere tolerantă): A 98,04, B 97,86. În fiecare pereche, ambele brațe pornesc din același adaptor, deci diferența de start se anulează în D.

**Proiectul: 2 × 2 încrucișat (ceas × adaptorul sarcinii 0), plus o repetare.** A = adaptorul sarcinii 0 din R1 (`ckpt_tau`), B = cel din R2 (`ckpt_eta_m`).

| Braț | Ceas | Sarcina 0 | Stare |
|---|---|---|---|
| `tau` (R1) | τ | A | existent |
| `eta_m` (R2) | η‖m̂‖ | B | existent |
| `eta_m_A1` | η‖m̂‖ | A (copiat) | **etapa 1** |
| `tau_B1` | τ | B (copiat) | **etapa 1** |
| `tau_A2` | τ | A (copiat) | **etapa 2** |
| `eta_m_A2` | η‖m̂‖ | A (copiat) | **etapa 2** |

Fiecare braț nou: dosarul `0-dbpedia` și `0-dbpedia_result.txt` (partea BWT a sarcinii 0) se **copiază** (nu se mută) din brațul sursă; apoi sarcinile 1–3, generările BWT pentru 1 și 2 și generarea OP, cu **aceleași comenzi și argumente** ca `launch_repro_resume.sh`, același cod (amprentele din `runs/forever_repro_sha256.txt`), sămânța lor (42), sarcinile 1–3 fără cache-ul alocatorului (adaptarea 5). Evaluarea: `eval_repro.sh <braț>` neschimbat. Lansator: `launch_repetari.sh`; analiza: `rep_verdict.py`; reconstrucția: `r2_reconstruction_arm.py`.

**Mărimea principală (singura pe care se dă verdictul):** d = acuratețea finală pe dbpedia (scriptul lor `eval_avgPerf_longsequence.py`, potrivire exactă), în puncte. **Cele trei perechi, fixate acum** (același adaptor, aceeași repetare), cu diferența τ − η‖m̂‖: D_A1 = d(`tau`) − d(`eta_m_A1`); D_B1 = d(`tau_B1`) − d(`eta_m`); D_A2 = d(`tau_A2`) − d(`eta_m_A2`). Celelalte comparații posibile pe A (de exemplu `tau` cu `eta_m_A2`) sunt doar descriptive. **Zgomotul** aceluiași ceas pe același adaptor (nedeterminismul GPU): N_τ = |d(`tau`) − d(`tau_A2`)|, N_η = |d(`eta_m_A1`) − d(`eta_m_A2`)|; **N = max(N_τ, N_η)** (maximul, prudent). Media: D̄ = (D_A1 + D_B1 + D_A2) / 3.

**Regula de decizie (fixată acum, aplicată mecanic de `rep_verdict.py`).** Este un criteriu prudent de consecvență practică, nu un test statistic: cu 3 perechi și 2 repetări pe ceas nu se poate estima o distribuție.
- **Oprire după etapa 1:** dacă D_A1 și D_B1 au semne opuse, verdictul este **NU SE POATE ATRIBUI CEASULUI**: criteriul strict de atribuire nu e îndeplinit (nicio valoare a lui D_A2 nu mai poate da trei semne la fel). Formularea este „datele nu susțin o atribuire stabilă a diferenței către ceas”, **nu** „ceasul nu are efect”: semnele opuse pot veni din zgomot sau dintr-o interacțiune între ceas și punctul de plecare, pe care o celulă cu o singură rulare nu le poate separa. Etapa 2 nu mai e necesară pentru verdict. Rularea ei rămâne posibilă, ca măsurare descriptivă a zgomotului GPU, la decizia utilizatorului (timp de laptop); **verdictul rămâne cel de după etapa 1**.
- **După etapa 2:**
  - **EFECT AL CEASULUI, τ mai bun pe dbpedia:** toate trei D > +2 și D̄ > N;
  - **EFECT AL CEASULUI, η‖m̂‖ mai bun pe dbpedia:** toate trei D < −2 și |D̄| > N;
  - **NU SE POATE ATRIBUI CEASULUI** (aceeași formulare ca mai sus): semne amestecate, sau |D̄| ≤ 2, sau |D̄| ≤ N;
  - **NEDECIS:** orice altă situație (de exemplu toate D de același semn, |D̄| > 2 și > N, dar un D sub 2 în valoare absolută).
- **Validitatea:** un braț cu o etapă eșuată (rc ≠ 0) sau oprit de paznic se mută deoparte (nu se șterge) și se reia o dată din sarcina 0 copiată; dacă eșuează din nou, verdictul e **NEDECIS**.

**Raportate, fără verdict nou (nu schimbă verdictul de pe dbpedia):** cele trei D, D̄, minimul și maximul lor, N_τ, N_η; uitarea pe dbpedia (componenta dbpedia a BWT din scriptul lor) pe fiecare braț; media diferențelor perechi pe OP și pe BWT (cu mențiunea dacă |media| ≤ 2) și scorurile pe sarcini; efectul adaptorului (d(`tau`) − d(`tau_B1`), d(`eta_m_A1`) − d(`eta_m`)), descriptiv; **declanșările**, din jurnalele de antrenare: pentru fiecare braț, sarcină și declanșare, pasul, pragul și valoarea ceasului, plus diferența de pași față de brațul pereche; R² al reconstrucției (aceeași analiză ca `r2_reconstruction.py`) pentru brațele η‖m̂‖, **doar pe sarcinile 1–3**: în brațele A, `drift_log.csv` al sarcinii 0 vine din rularea τ și nu măsoară ceasul η‖m̂‖. Pentru comparație se calculează aceeași valoare (sarcinile 1–3) și pentru R2; întrebarea e dacă R² slab pe agnews (0,578 în R2) se repetă.

**Limite fixate dinainte:** toate rulările au sămânța 42, deci repetările măsoară nedeterminismul GPU, nu variația între semințe; aceasta este exact sursa de variație dintre R1 și R2, dar nu acoperă alte semințe. O singură ordine (4), un model mic, n mic (3 perechi).

**Timpul:** măsurat în R1 și în R2 (de la sarcina 1 la sfârșitul generării OP): 7 h 24 min pe braț, în ambele. Etapa 1 ≈ 15 h, etapa 2 ≈ 15 h, total ≈ 30 h de GPU ocupat. Paznicul hardware se repornește cu un termen care acoperă rularea.

**Mediul:** RTX 3050 Laptop 4 GB, driver 592.00; torch 2.8.0+cu128 (CUDA 12.8), transformers 4.57.0, peft 0.17.1 (`pip_freeze_venv_forever.txt`); AMP fp16, fără algoritmi deterministici (ca în codul lor); Windows 11, mod Turbo. Codul: commit `bbeb549a21e5…`, amprentele scripturilor în `runs/forever_repro_sha256.txt`. Adaptoarele A și B au câte 4.602.248 de octeți. R1 și R2 nu se suprascriu: lansatorul doar citește din `ckpt_tau`, `ckpt_eta_m`, `output/tau`, `output/eta_m` și refuză un braț al cărui dosar există deja.

**Pornire:** numai cu acordul explicit al utilizatorului (autorizarea de weekend expiră după 8 nov. 2026).

**Schimbările din versiunea 2 (observațiile Copilot, verificate punct cu punct):**
- *Acceptate:* faptul 5 (starea care trece între sarcini, verificată în cod) și faptul 6 (punctul de plecare); perechile și formula lui N scrise explicit, cu restul comparațiilor marcate descriptive (perechile și N existau deja în v1; acum sunt numite „fixate”); formularea verdictului de oprire timpurie și posibilitatea unei interacțiuni; etapa 2 permisă și după oprire, doar descriptiv; regula numită criteriu de consecvență, nu test statistic; raportarea D, D̄, minim, maxim, N_τ, N_η; regula de validitate; tabelul declanșărilor; uitarea pe dbpedia raportată secundar; mediul.
- *Respinse, cu motiv:* (1) restaurarea completă a optimizatorului, a planificatorului, a scalerului și a stărilor aleatoare: în codul lor nimic din acestea nu trece între sarcini (faptul 5), deci restaurarea ar abate rularea de la conducta lor; (2) scorul dbpedia înainte și după fiecare repetiție: codul lor suprascrie adaptorul în același dosar la fiecare fază, deci ar cere schimbarea codului; (3) R² „în apropierea pragurilor”: nedefinit și cu prea puține ferestre (~4 declanșări pe sarcină); întrebarea mecanismului e măsurată direct de pașii declanșărilor; (4) condițiile vagi pentru NEDECIS („interacțiune complicată”, „prea aproape de limita regulii”): ar reintroduce judecata de după rezultat; (5) uitarea ca mărime principală: în fiecare pereche punctul de plecare e comun, deci D pe scorul final și D pe uitare diferă doar prin metrica de extragere; rămâne principal scorul cu potrivire exactă, ca în R1 și R2.
