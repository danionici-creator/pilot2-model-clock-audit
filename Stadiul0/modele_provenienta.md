# Proveniența modelelor preantrenate pentru brațul LM (verificată 6 nov. 2026)

Modelele stau în `D:\Time\_modele\` și **nu intră în nicio arhivă publică**. Au fost descărcate doar fișierele `model.safetensors`, config, tokenizer (și, la Qwen, `generation_config.json`, `merges.txt`, `vocab.json`). Nu există niciun fișier pickle (`.bin`, `.pt`, `.pth`, `.pkl`, `.ckpt`), niciun fișier `.py` și niciun `auto_map` în `config.json`. Scripturile (`_work\bench_pythia_lora.py`, `_work\bench_lm_lora.py`) încarcă modelele cu `local_files_only=True`, fără `trust_remote_code`, și nu folosesc șabloanele de chat.

SHA-256 local al greutăților = SHA-256 înregistrat la descărcare (`.cache/huggingface/download/model.safetensors.metadata`) = OID-ul LFS publicat de Hugging Face pentru același commit (API `/api/models/<repo>/tree/<commit>`, interogat pe 6 nov. 2026):

| Model | Repo, commit | `model.safetensors` SHA-256 | Mărime |
|---|---|---|---|
| Pythia-31m | EleutherAI/pythia-31m @ `e556ace21b489575e94e9d50b6dad2fcc7419679` | `02ddadd516061264cd44b47c84ae49c6641f869e6d3f06c7d0e4855f31e34059` | 58,2 MB |
| Pythia-70m | EleutherAI/pythia-70m @ `a39f36b100fe8a5377810d56c3f4789b9c53ac42` | `ebfa4e2f18696ebd83716a0d39fe2c025f2ff8483f72a83ca59c475692fc9d15` | 158,3 MB |
| Pythia-410m | EleutherAI/pythia-410m @ `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` | `3e09001631bb18ec8a6f4522f8e6ab26a53099e69228f9822adc91bfbe27511b` | 869,2 MB |
| Qwen3-0.6B | Qwen/Qwen3-0.6B @ `c1899de289a04d12100db370d81485cdf75e47ca` | `f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b` | 1.433,7 MB |

Depozitele Pythia conțin și greutăți pickle (`pytorch_model.bin`, la 31m și `mp_rank_00_model_states.pt`); ele **nu** au fost descărcate. În raportul Stadiului 0 și în orice articol se citează repo-ul, commit-ul și hash-ul din acest tabel.
