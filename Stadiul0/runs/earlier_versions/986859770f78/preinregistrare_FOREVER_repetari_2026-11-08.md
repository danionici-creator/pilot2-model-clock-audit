# Preînregistrarea rulărilor repetate R1/R2 (8 nov. 2026, ÎNAINTE de rulare)

**De ce:** după R2 (`Rezultate_teste_decisive_2026-11-07.md`, secțiunea din 8 nov., ~13:45) a rămas o întrebare deschisă. Verdictul agregat e echivalență (ΔOP +0,84, ΔBWT +0,69), dar pe dbpedia (prima sarcină) τ dă 93,21, iar η‖m̂‖ 87,89 (**+5,33 puncte**). O singură pereche nu separă efectul ceasului de nedeterminism. Cerută de utilizator („Plan repeated runs”). Verdictul R2 rămâne cel înregistrat; rulările de aici îl completează și nu îl înlocuiesc.

**Fapte pe care se sprijină proiectul (verificate în cod și în fișiere):**
1. Codul lor fixează sămânța: `set_seed(42)` (`src/finetune_cl_our_qwen.py`, linia 31); amestecările (`shuffle()` fără sămânță) și eșantionarea memoriei derivă din ea. Deci R1 și R2 diferă **doar** prin ceas și prin nedeterminismul GPU (fp16, fără algoritmi deterministici).
2. Nedeterminismul e real: adaptoarele de după sarcina 0 diferă între R1 și R2 (`adapter_model.safetensors`: `636589d5…` în `ckpt_tau`, `66dc0d26…` în `ckpt_eta_m`); dbpedia imediat după sarcina 0: 98,04 față de 97,86.
3. Pe sarcina 0 nu există repetiții (2 faze în ambele rulări), deci ceasul nu influențează adaptorul sarcinii 0. Ambele adaptoare sunt puncte de plecare valide pentru oricare ceas.
4. Fiecare sarcină își calibrează ziua-model din propriii 24 de pași (`Phase 1: CALIBRATION CURRENT`), iar `DriftRecorderCallback` citește doar `drift_log.csv` din dosarul sarcinii curente. Copierea dosarului `0-dbpedia` nu transmite nimic din ceasul sarcinii 0 către sarcinile 1–3.

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

**Mărimea principală:** d = acuratețea finală pe dbpedia (scriptul lor `eval_avgPerf_longsequence.py`, potrivire exactă), în puncte. Diferențele perechi (același adaptor, aceeași repetare), τ − η‖m̂‖: D_A1 = d(`tau`) − d(`eta_m_A1`); D_B1 = d(`tau_B1`) − d(`eta_m`); D_A2 = d(`tau_A2`) − d(`eta_m_A2`). Zgomotul aceluiași ceas pe același adaptor: N_τ = |d(`tau`) − d(`tau_A2`)|, N_η = |d(`eta_m_A1`) − d(`eta_m_A2`)|; N = max(N_τ, N_η).

**Regula de decizie (fixată acum, aplicată mecanic de `rep_verdict.py`):**
- **Oprire după etapa 1:** dacă D_A1 și D_B1 au semne opuse, verdictul este **NU SE POATE ATRIBUI CEASULUI** și etapa 2 nu mai rulează (nicio valoare a lui D_A2 nu mai poate da trei semne la fel).
- **După etapa 2:**
  - **EFECT AL CEASULUI, τ mai bun pe dbpedia:** toate trei D > +2 și media D > N;
  - **EFECT AL CEASULUI, η‖m̂‖ mai bun pe dbpedia:** toate trei D < −2 și |media D| > N;
  - **NU SE POATE ATRIBUI CEASULUI:** semne amestecate, sau |media D| ≤ 2, sau |media D| ≤ N;
  - **NEDECIS:** orice altă situație.

**Raportate, fără verdict nou:** media diferențelor perechi pe OP și pe BWT (cu mențiunea dacă |media| ≤ 2); efectul adaptorului (d(`tau`) − d(`tau_B1`), d(`eta_m_A1`) − d(`eta_m`)), descriptiv; R² al reconstrucției (aceeași analiză ca `r2_reconstruction.py`) pentru brațele η‖m̂‖, **doar pe sarcinile 1–3**: în brațele A, `drift_log.csv` al sarcinii 0 vine din rularea τ și nu măsoară ceasul η‖m̂‖. Pentru comparație se calculează aceeași valoare (sarcinile 1–3) și pentru R2; întrebarea e dacă R² slab pe agnews (0,578 în R2) se repetă.

**Limite fixate dinainte:** toate rulările au sămânța 42, deci repetările măsoară nedeterminismul GPU, nu variația între semințe; aceasta este exact sursa de variație dintre R1 și R2, dar nu acoperă alte semințe. O singură ordine (4), un model mic, n mic (3 perechi).

**Timpul:** măsurat în R1 și în R2 (de la sarcina 1 la sfârșitul generării OP): 7 h 24 min pe braț, în ambele. Etapa 1 ≈ 15 h, etapa 2 ≈ 15 h, total ≈ 30 h de GPU ocupat. Paznicul hardware se repornește cu un termen care acoperă rularea.

**Pornire:** numai cu acordul explicit al utilizatorului (autorizarea de weekend expiră după 8 nov. 2026).
