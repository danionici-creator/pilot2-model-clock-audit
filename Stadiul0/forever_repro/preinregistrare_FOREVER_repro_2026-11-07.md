# Preînregistrarea reproducerii FOREVER cu codul lor (7 nov. 2026, ÎNAINTE de rulare)

**De ce:** limita principală rămasă după testele decisive și după SuperNI: comparațiile cu FOREVER (arXiv:2601.03938) au fost făcute cu portul nostru, nu cu codul lor. Cerută de utilizator („Reproduce with their code”, „Full fidelity, ~17 h”).

**Codul și mediul:** copia de lucru `Stadiul0/forever_repro/` a depozitului lor (github.com/WoodScene/FOREVER, commit `bbeb549a21e5…`; originalele în `D:\Time\_date\FOREVER_bbeb549\`, verificate cu amprentele git). Mediul separat `D:\Time\_venv_forever` cu versiunile din `requirements.txt` al lor: torch 2.8.0+cu128, transformers 4.57.0, peft 0.17.1, accelerate 1.10.1, datasets 4.1.1, numpy 1.26.4 etc. (`pip_freeze_venv_forever.txt`); Python 3.12.

**Adaptările (singurele schimbări față de codul lor):**
1. `TRANSFORMERS_CACHE` / `AutoConfig.default_cache_dir`: o cale locală în loc de `/workspace/...`;
2. în `generate_avgPerf.py` și `generate_bwt.py`: calea fișierelor de test vine din `FOREVER_DATA` (`data_longsequence`); originalul are fixat `../data_superni`, deci nu ar putea evalua benchmark-ul „long sequence”;
3. rularea cu `python` în loc de `torchrun --nproc_per_node=1` (un GPU); `PYTHONIOENCODING=utf-8` (consola Windows); `HF_HUB_OFFLINE=1`; numele fișierului: scriptul lor de lansare cheamă `finetune_cl_ours_qwen.py`, care nu există în depozit; rulăm `finetune_cl_our_qwen.py`;
4. torch 2.8 pe Windows, laptop RTX 3050 4 GB (al lor: Linux, alt GPU). Codul lor nu e determinist (fp16, fără algoritmi deterministici), deci o repetare dă rezultate ușor diferite.

**Rulările:** ordinea 4 („Standard CL”: dbpedia → amazon → yahoo → agnews), argumentele exacte din `scripts/run_train_cl_ours_qwen.sh`: `--num_epochs 10 --first_task_epochs 60 --group_by_length --lora_target_modules ["q_proj","v_proj"] --micro_batch_size 4 --batch_size 32 --max_input_length 512 --memory_epochs 2 --steps_per_day 24 --memory_data_ratio 2`. După fiecare sarcină 0–2: `generate_bwt.py` pe sarcina proprie; după ultima: `generate_avgPerf.py` pe toate 4. Evaluarea cu `eval_avgPerf_longsequence.py` și `eval_bwt_longsequence.py` ale lor.
- **R1, reproducerea:** codul lor neschimbat (ceasul τ).
- **R2, înlocuirea ceasului:** `finetune_cl_our_qwen_clock.py`, generat de `make_clock_variant.py`; singura schimbare: contorul care conduce repetițiile (`DriftRecorderCallback.tau`) avansează cu η·‖m̂‖ (primul moment AdamW corectat de bias), în loc de ‖Δθ‖. Norma reală e păstrată în `tau_true`, iar intensitatea μ (deci β) rămâne calculată din ‖Δθ‖, ca în original.

**Criteriile (fixate acum):**
- **R1 reproduce FOREVER** dacă OP pe ordinea 4 (scriptul lor `eval_avgPerf_longsequence.py`, potrivire exactă) e în **±5 puncte** față de **72,9** (tabelul 1 al articolului, media pe 3 ordini). Se raportează și BWT (articolul: −4,7) și OP calculat cu extragerea de etichetă din scriptul lor de BWT (mai tolerantă).
- **R2 față de R1** (o singură pereche, descriptiv, fără interval): **echivalență** dacă |OP(τ) − OP(η‖m̂‖)| ≤ 2 puncte; **τ mai bun** dacă diferența e > 2; **η‖m̂‖ mai bun** dacă e < −2. Același raport pentru BWT.
- **Secundar, reconstrucția în codul lor:** în rularea R2, R² (OLS) al ratei lui ‖Δθ‖ pe ferestre de 8 pași, din creșterea ceasului η‖m̂‖ în aceeași fereastră; se raportează (reperul nostru: ≥ 0,90).
- **Dacă R1 nu reproduce** (OP în afara ±5): R2 se raportează doar descriptiv, iar concluziile despre FOREVER rămân limitate la portul nostru.

**Durata estimată** (viteze măsurate cu codul lor: ~5,5–7 s pe pas, ~0,35 s pe exemplu generat): pe variantă ~5 h antrenare + ~1,4 h generare BWT + ~1,6 h generare OP ≈ **8 h**; total **~16–17 h**.
