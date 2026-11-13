# Runda tehnică lmtech1: ceasul FOREVER în programul FOREVER, pe Qwen3-0.6B (criterii fixate ÎNAINTE de rulare, 6 nov. 2026)

**Ce e:** o rundă tehnică, nepreînregistrată, ca tech1–tech3. Brațul LM al Pilot 2, pasul 2 din `02_Pilot2\Literatura\Literatura_marime_actualizari_AdamW.md` §6. **Orb față de T1:** analiza G2 nu citește `evals.npz` (acuratețea pe sarcinile vechi, adică uitarea).

**Rularea:** `lm_forever_run.py` (descrierea completă a setării și a abaterilor în antetul scriptului), 3 semințe: 7101, 7102, 7103. 10 sarcini × 512 fapte sintetice; sarcina 0: 60 de epoci, celelalte: 10 (ca în scriptul FOREVER). Qwen3-0.6B (SHA-256 în `..\modele_provenienta.md`), LoRA r = 8, α = 16, q_proj și v_proj; fp16 cu GradScaler; AdamW fără weight decay; rata 3e-4; program liniar cu warmup, reluat la fiecare fază; calibrare pe 24 de pași; praguri d·τ_zi; repetiții ne-contorizate în τ. RTX 3050 Laptop, mod ASUS Turbo, la priză.

**Determinism (verificat înainte):** două rulări identice (2 sarcini scurte) dau tablouri identice bit cu bit (telemetria, sondele, evaluările, factorii finali). Se repetă la final pe o rulare din rundă (G7-GPU).

**Analiza** (`lm_forever_g2.py`, fixată acum): ferestre de 8 pași contorizați; R² în afara rulării (o sămânță lăsată deoparte) pentru rata lui τ (factori; secundar ΔW) și pentru D3 (schimbarea pe 128 de sonde neantrenate), cu scara: Ση → Ση‖g̃‖ → Ση‖m̂‖ → câmpul mediu Ση‖m̂‖·√d/√Tr v̂ → Ση + Ση‖m̂‖ → GBDT pe toată telemetria; reziduul lui „y ~ Ση” după fereastra din fază; τ la nivel de fază din Ση și Ση‖m̂‖.

**Predicția scrisă înainte de orice date LM** (documentul de literatură, 4 nov. 2026, §1 punctul 3 și §5 punctul 3): în setarea FOREVER, Ση (programul ratei, cunoscut gratuit din planificator) explică cea mai mare parte din τ. Operaționalizare: R² în afara rulării al ratei lui τ din Ση ≥ 0,80 → „ceasul e dominat de programul ratei”. Nu e o poartă; se raportează oricum ar ieși. **Notă de onestitate:** testul de cod pe două rulări scurte și identice (4 epoci, 15 ferestre) a dat deja R² 0,40 pentru Ση și 0,97 pentru Ση‖m̂‖; e un test de cod, nu o măsurătoare, dar arată că predicția poate pica.

**Criterii de validitate pe rulare** (fixate după proba de învățare cu 2 sarcini, `runs\lm_smoke\full2`, înainte de lmtech1):
- nicio pierdere nefinită (scriptul se oprește);
- pași săriți de GradScaler ≤ 2% din pașii contorizați;
- acuratețea pe sarcina curentă la sfârșitul fiecărei sarcini ≥ 0,95 (doar diagonala din `evals.npz`, citită de `run.log`; proba full2: 1,000 și 1,000).

Proba full2 (sămânța 2, 2 sarcini complete, 6 nov., 16:29–16:35): sarcina 0, 960 de pași în 311 s (0,32 s/pas), acuratețe 1,000; sarcina 1, 160 de pași contorizați, 8 faze (calibrare, 3 repetiții, 3 faze curente, repetiția finală), 56 s, acuratețe 1,000; pași săriți 1,16%; VRAM maxim 1,7 GB. **Notă:** verificarea a afișat și acuratețea pe sarcina 0 după sarcina 1 (0,514). E o informație de tip T1 dintr-o probă, nu din rundă; nu intră în nicio analiză. În lmtech1 se citește doar diagonala.
- rularea se termină cu `meta.json` și amprentele SHA-256.

**Ce nu se decide din această rundă:** nimic despre H1 (uitarea) și nimic despre protocolul v0.5. Rezultatul intră în notele Stadiului 0 și în decizia despre forma brațului LM.
