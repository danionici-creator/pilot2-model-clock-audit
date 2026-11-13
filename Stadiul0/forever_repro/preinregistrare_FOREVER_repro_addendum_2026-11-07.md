# Addendum la preînregistrarea reproducerii FOREVER (7 nov. 2026, ~18:25, ÎNAINTE de orice rezultat de evaluare)

**Ce s-a întâmplat.** R1 (τ), sarcina 1 (amazon): antrenarea curentă s-a terminat (313/313 pași), dar repetiția finală din memorie a căzut la 18:12 cu `torch.AcceleratorError: CUDA error: out of memory` (jurnalul: `_work\_copii_siguranta\forever_repro_t1_oom_2026-11-07\logs\tau_train_t1.log`). Pe Windows (WDDM), când cei 4 GB de VRAM se umplu, driverul pune alocările în memoria partajată din RAM. Alocatorul PyTorch cu cache le păstrează, deci memoria procesului a crescut (măsurat la 16:20: 3,9 GB dedicat + 9,7 GB partajat), pașii au încetinit de la ~7 s la ~30–40 s, iar la final s-a atins limita. Vârful real al unui lot lung depășește 4 GB: alocatorul `cudaMallocAsync`, care nu folosește memoria partajată, cade imediat (verificat). Lansatorul original ar fi continuat cu un adaptor fără repetiția finală; paznicul de eșec l-a oprit. Generarea BWT pornită pe acel adaptor a fost oprită manual, înainte de orice evaluare.

**Ce s-a mutat (nimic șters):** `ckpt_tau/.../1-amazon`, `logs/tau_train_t1.log`, `logs/tau_bwt_t1.log` și rezultatul parțial `1-amazon_result.txt` sunt în `_work\_copii_siguranta\forever_repro_t1_oom_2026-11-07\`. Mutarea e necesară: codul lor reia contorul de pași din `drift_log.csv`, dacă fișierul există. Sarcina 0 (adaptorul `0-dbpedia` și generarea BWT pe dbpedia) rămâne neatinsă.

**Adaptarea 5 (nouă, doar de execuție):** antrenarea sarcinilor 1–3 (cele cu repetiții din memorie) rulează cu variabila de mediu `PYTORCH_NO_CUDA_MEMORY_CACHING=1`, **pentru ambele variante**. Fiecare tensor e eliberat imediat, deci blocurile ajunse în memoria partajată nu se mai acumulează. Sarcina 0 și toate generările rămân cu alocatorul implicit, ca în R1 sarcina 0. Codul, argumentele și calculele nu se schimbă (alocatorul decide doar unde stă memoria, nu ce se calculează); costul e doar timpul (măsurat: ~18,5 s pe pas față de ~7,5 s pe pas fără umplerea VRAM-ului).

**Variante respinse:**
- `micro_batch_size` 2 în loc de 4: în codul lor, termenul de regularizare din `ReplayTrainer` se adună la fiecare micro-lot fără împărțire la numărul de pași de acumulare, deci forța lui s-ar dubla. Asta e o schimbare de algoritm.
- `garbage_collection_threshold`: fără efect fără `set_per_process_memory_fraction`, care cere schimbare de cod (verificat).
- `cudaMallocAsync`: cade imediat.

**Lansatorul de reluare:** `launch_repro_resume.sh` (aceleași comenzi; începe cu τ de la sarcina 1, apoi η‖m̂‖ de la sarcina 0; se oprește la prima etapă eșuată).

**Criteriile din preînregistrare rămân neschimbate.** Singura informație de rezultat cunoscută acum: verificarea de funcționare a generării pe dbpedia după sarcina 0 (98,5% potriviri exacte pe primele 2.654 de exemple), care nu e criteriul.
