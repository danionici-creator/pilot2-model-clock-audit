# Pilot 2, pasul 1: literatura despre mărimea actualizărilor în Adam/AdamW și ceasul FOREVER (4 nov. 2026)

**Întrebarea.** E deja cunoscută constatarea din `Stadiul0_note_lucru.md` §9: sub AdamW, „timpul centrat pe model” (τ = Σ‖Δθ_t‖, ceasul FOREVER, la noi D1) e practic suma Ση‖m̂‖ (plus durata), cu R² ≈ 0,94 pe rulările tehnice? Dacă da, merită continuat Pilot 2?

**Metoda.** Căutare web (≈ 15 interogări), citirea articolului FOREVER (arXiv HTML v2) și a **codului lor** (GitHub), lista citărilor FOREVER din Semantic Scholar și verificarea tuturor ID-urilor prin API-ul arXiv (4 nov. 2026). La fiecare lucrare e notat ce s-a citit efectiv: textul, rezumatul sau doar metadatele. Căutarea nu e exhaustivă. Pentru o verificare independentă e pregătit promptul `..\Recenzii\Prompturi\Pilot2_Prompt_literatura_AdamW.txt`.

## 1. Concluzia pe scurt

1. **Ca mecanism, constatarea e de așteptat.** Rezultă în câțiva pași din rezultate publicate. Pasul Adam e η·m̂/(√v̂+ε). RMS-ul lui depinde doar de raportul semnal/zgomot al gradientului: e constant în regimul dominat de zgomot (Kosson et al. 2024) și crește spre 1 când domină semnalul (Su 2025, formula de câmp mediu; Liu et al. 2025: 0,2–0,4 empiric). Câtă vreme energia gradientului (≈ v̂) variază lent, ‖m̂‖ poartă aceeași informație despre raportul semnal/zgomot, deci D1 ≈ Ση‖m̂‖ / √v̄. Un recenzent care cunoaște optimizatorii va spune că rezultatul era de așteptat (nu banal, dar așteptat). **Nu se poate prezenta ca descoperire.**
2. **Ca audit al ceasului FOREVER, n-am găsit nimic.** Semantic Scholar listează 13 citări ale FOREVER; niciuna nu examinează ceasul. O singură lucrare înrudită folosește tot drumul parcurs ca ceas intrinsec (Pathwise EMA, poster de workshop ICML 2026), fără o comparație cunoscută cu statistici ieftine.
3. **Constatare nouă, din codul FOREVER** (§2): τ se calculează pe factorii LoRA. Fiecare fază de antrenare (calibrare, faza curentă, repetiție) e un `Trainer` nou: optimizatorul e recreat (m̂ și v̂ pornesc de la zero), iar programul ratei (warmup de 10 pași, apoi scădere liniară la 0) repornește. Weight decay e 0. Deci τ conține direct programul ratei, iar ablația lor compară τ doar cu numărul de pași. **Competitorul gratuit Ση_t (rata aplicată, cunoscută din planificator) lipsește.** E o predicție verificabilă, nu un rezultat: cât din τ explică Ση în setarea lor exactă se măsoară la pasul 2.
4. **Pentru decizie:** constatarea „τ ≈ Ση‖m̂‖” nu poate fi miezul unei lucrări. Un audit mic al ceasului FOREVER rămâne posibil și nepublicat de altcineva (după cât am găsit), cu trei componente: (a) τ față de competitori gratuiți, în setarea lor exactă; (b) unde cedează aproximarea (granițele de sarcină, resetarea optimizatorului, factorii față de B·A); (c) D3 (distanța funcțională) față de D1. Nivelul rămâne cel estimat: o notă empirică mică.

## 2. Ce face FOREVER exact (articolul și codul)

Articolul: arXiv:2601.03938 v2 (ACL 2026 camera-ready), citit în HTML. Codul: https://github.com/WoodScene/FOREVER, ultimul commit `bbeb549` (20 apr. 2026), fișierele `src/finetune_cl_our_qwen.py` și `scripts/run_train_cl_ours_qwen.sh`, citite pe 4 nov. 2026 (copie temporară în scratchpad, nu în proiect). `requirements.txt`: transformers 4.57.0, peft 0.17.1, torch 2.8.0.

| Element | Articolul | Codul (Qwen) |
|---|---|---|
| Δ_t | ‖Θ_t − Θ_{t−1}‖₂ (§2.1, ec. 2), „computed over trainable parameters only (i.e., the LoRA weights)” | `DriftRecorderCallback`: concatenarea tuturor parametrilor cu `requires_grad` (factorii A și B), în float32, la fiecare pas (rândurile 62–93) |
| τ | Σ Δ_i (ec. 3), resetat la începutul fiecărei sarcini | la fel; fazele de repetiție nu se contorizează („Silent Update after Replay”: punctul de referință se mută) |
| Optimizator | **nenumit** în text | `optim="adamw_torch"`; `weight_decay` nesetat → **0,0** (implicit în transformers), deci practic Adam |
| Rata | 3e-4 (anexa H); programul nu e menționat | `learning_rate=3e-4`, `warmup_steps=10` (5 la repetiție); `lr_scheduler_type` nesetat → **„linear”** (scădere la 0 până la `max_steps`) |
| Faze | calibrare pe primii 24 de pași = o „zi”; praguri d·τ_day, d ∈ {1, 2, 4, 7, 15, 30, 60, 90, 120} | fiecare fază = un `transformers.Trainer` nou → **optimizator nou și program de rată nou** la fiecare fază |
| LoRA | r = 8, α = 32, dropout 0,05, q_proj și v_proj | r = 8, **α = 16** (implicit, nesuprascris de script), dropout 0,05, q_proj și v_proj |
| Batch | 8 | 32 (4 × 8 acumulări) |
| Precizie, tăiere | — | `fp16=True`; `max_grad_norm` implicit 1,0 |
| Sensibilitate | Δ_t „substantially less sensitive to optimization hyperparameters”, fără analiză | — |

Valorile implicite sunt verificate local în transformers 5.13.1 (`dataclasses.fields(TrainingArguments)`: linear, 0,0, β 0,9 / 0,999, ε 1e-8, tăiere 1,0); în 4.57.0 sunt aceleași (nu am verificat direct versiunea lor). `MyTrainer` suprascrie doar `compute_loss`.

**Consecințe pentru audit:**
1. În fiecare fază, η urcă de la 0 la 3e-4 în 10 pași și apoi scade liniar. Δ_t e proporțional cu η_t în primul ordin, deci τ e în mare parte integrala programului de rată, iar programul depinde la rândul lui de τ (fazele se încheie când τ atinge pragul). Ablația „+STC” (pași în loc de τ) nu separă programul ratei de „timpul modelului”.
2. Resetarea momentelor la fiecare fază: în primii pași după resetare, m̂/√v̂ ≈ semnul gradientului (RMS ≈ 1), dar η e aproape 0 din cauza warmup-ului. E locul în care Ση‖m̂‖ ≈ D1 poate ceda local.
3. Cu weight decay 0, echilibrul rotațional (Kosson et al. 2024) și imaginea „ponderile = medie mobilă a actualizărilor” (Wang & Aitchison 2025) nu se aplică în setarea FOREVER. Se aplică doar partea despre RMS-ul pasului în funcție de semnal/zgomot.
4. **Corectură la predare:** c_e primar pe brațul LM trebuie să fie τ **pe factori**, exact ca la ei; ΔW = B·A (cu scara α/r) e varianta secundară. Predarea spunea invers.
5. **Pentru v0.5 (neaplicat):** în §0.3, §9 și §13, „LoRA and AdamW (the regime of FOREVER)” se înlocuiește cu descrierea exactă de mai sus, cu diferențele articol/cod (α 32/16, batch 8/32) și cu sursa (commit `bbeb549`).

## 3. Literatura despre mărimea pasului Adam (ce e cunoscut)

Toate ID-urile sunt verificate prin API-ul arXiv pe 4 nov. 2026 (titlu, autori, dată, comentariu).

| Lucrare | Ce s-a citit | Ce spune | Relevanța |
|---|---|---|---|
| Balles & Hennig 2018, „Dissecting Adam: The Sign, Magnitude and Variance of Stochastic Gradients”, ICML 2018, arXiv:1705.07774 | rezumatul | Adam = direcția semnului × o adaptare a mărimii după varianța relativă a gradientului | baza conceptuală: mărimea pasului pe coordonată e stabilită de raportul semnal/zgomot |
| Kosson, Messmer & Jaggi 2024, „Rotational Equilibrium: How Weight Decay Balances Learning Across Neural Networks”, ICML 2024, arXiv:2305.17212 | textul HTML, prima jumătate | în regimul dominat de zgomot, RMS-ul pasului AdamW e η√(C(1−β₁)/(1+β₁)), constant; norma și unghiul ajung la echilibru sub weight decay, cu constanta de timp ≈ 1/(2ηλ) (calculul meu din relația lor de convergență) | prezice D1 ∝ Ση **în echilibru**. Datele noastre îl contrazic în învățarea continuă: în F2 (rată constantă) rata lui D1 variază (CV 0,37), deși Ση nu aduce nimic peste ΔN. La noi ηλ = 3·10⁻⁶ → 1/(2ηλ) ≈ 167.000 de pași, mult peste viața de 20.480: echilibrul nu se atinge. În FOREVER (λ = 0) nici nu există |
| Kosson, Messmer & Jaggi 2024, „Analyzing & Reducing the Need for Learning Rate Warmup in GPT Training”, NeurIPS 2024, arXiv:2410.23922 | rezumatul | warmup-ul compensează actualizări inițiale mari (unghiulare); compară mai multe măsuri ale mărimii pasului și normalizează actualizările | mărimea pasului variază sistematic cu faza antrenării: fapt cunoscut |
| Wang & Aitchison 2025, „How to set AdamW's weight decay as you scale model and dataset size”, ICML 2025, arXiv:2405.13698 | rezumatul | ponderile AdamW ca medie mobilă exponențială a actualizărilor, cu scara de timp 1/(ηλ) | slabă: în FOREVER λ = 0, iar la noi scara depășește viața |
| Liu et al. 2025, „Muon is Scalable for LLM Training”, arXiv:2502.16982 | §2.2 | „AdamW's update RMS is usually around 0.2 to 0.4” (observație empirică, preantrenare LLM) | în preantrenare (zgomot dominant) RMS-ul e aproape constant, deci acolo τ ≈ Ση. Învățarea continuă, cu schimbări de sarcină, e regimul în care variază |
| Su 2025, „Why is Adam's Update RMS 0.2?”, blog *Scientific Spaces*, kexue.fm/archives/11267, 2 sept. 2025 | traducerea în engleză (originalul răspunde 403 roboților); **nerecenzat** | aproximare de câmp mediu: RMS ≈ √((r + (1−β₁)/(1+β₁)) / (r + 1)), cu r = ‖μ‖²/‖σ‖²; nu depinde de β₂ | cea mai directă formulare a mecanismului. Cu ea, rata lui D1 ≈ η√d·f(r), iar ‖m̂‖² ≈ ‖μ‖² + ((1−β₁)/(1+β₁))‖σ‖² poartă aceeași informație câtă vreme ‖μ‖² + ‖σ‖² variază lent. Într-un articol: derivarea proprie + Kosson pentru limită; blogul doar ca mențiune |
| Kunstner et al. 2023, „Noise Is Not the Main Factor Behind the Gap Between SGD and Adam on Transformers, but Sign Descent Might Be”, arXiv:2304.13960 | doar metadatele | — | secundară; de citit doar dacă se discută regimul „semn” |
| van Laarhoven 2017, „L2 Regularization versus Batch and Weight Normalization”, arXiv:1706.05350 | doar metadatele | (rata efectivă sub normalizare, cunoscut) | fundal pentru D1_rel și unghiuri |
| Atamna et al. 2025, „Cumulative Learning Rate Adaptation: Revisiting Path-Based Schedules for SGD and Adam”, arXiv:2508.05408 | rezumatul (prin căutare) | adaptează rata comparând drumul cumulat observat cu cel al unei plimbări aleatoare, extins la Adam | statisticile de drum ale lui Adam sunt deja folosite ca semnal de control; raportul ‖Σu‖ / Σ‖u‖ (coerența) e un posibil competitor ieftin |
| Guille-Escuret et al. 2023, „No Wrong Turns: The Simple Geometry Of Neural Networks Optimization Paths”, arXiv:2306.11922 | doar rezumatul căutării | Adam parcurge o distanță mai mare, într-un ritm mai regulat (ResNet-18, CIFAR-10) | slabă |

## 4. Ceasuri pe drumul parcurs și schimbarea parametrilor în învățarea continuă

| Lucrare | Ce s-a citit | Ce spune | Relevanța |
|---|---|---|---|
| Dao & Block 2026, „Pathwise EMA: An Intrinsic Clock for Weight Averaging”, poster, workshop ICML 2026 „High Dimensional Learning Dynamics” (icml.cc/virtual/2026/72447; OpenReview `458LCpzUwu`) | rezumatul de pe pagina ICML. OpenReview cere o verificare anti-robot, neocolită. Niciun arXiv (căutarea pe titlu: 0 rezultate) | decăderea EMA a ponderilor legată de **lungimea normalizată a drumului** parcurs de parametri, „intrinsic clock”; SFT pe SmolLM2, Qwen, Gemma | al doilea utilizator din 2026 al ceasului pe drumul parcurs, deci auditul contează pentru mai mult decât FOREVER. **Necitabil** până nu se citește textul |
| He, Bai & Yang 2026, „Exploring the Impact of Parameter Update Magnitude on Forgetting and Generalization of Continual Learning”, arXiv:2602.20796 | rezumatul | teorie: o mărime optimă a actualizării care minimizează uitarea; strategie hibridă după direcția gradientului | mărimea ca factor al uitării, nu ca ceas; nu menționează FOREVER |
| Wang et al. 2026, „Geometry Conflict”, arXiv:2605.09608 | deja verificată (sinteza §2) | geometria actualizărilor, nu mărimea lor, explică uitarea; FOREVER apare ca baseline | susține D3 și contrastul F6 |
| Kang & Lee 2024, „Continual Learning of Numerous Tasks from Long-tail Distributions”, arXiv:2404.02754 | rezumatul (prin căutare) | v̂ al parametrilor inactivi în sarcina curentă scade exponențial; propune un v̂ ponderat pe sarcini | locul în care D1 ≈ Ση‖m̂‖ poate ceda: v̂ nestaționar între sarcini |
| Sahu et al. 2026, „Adapt or Forget: Provable Tradeoffs Between Adam and SGD in Nonstationary Optimization”, arXiv:2605.04269 | rezumatul | sub derivă, primul moment învechit și perturbarea precondiționatorului slăbesc garanțiile lui Adam | teoria aceleiași cedări |
| Biderman et al. 2024, „LoRA Learns Less and Forgets Less”, TMLR, arXiv:2405.09673 | rezumatul (prin căutare) | LoRA uită mai puțin; perturbările complete au rang de 10–100 de ori mai mare | context pentru brațul LM |
| Mirzadeh et al. 2020, „Understanding the Role of Training Regimes in Continual Learning”, NeurIPS 2020, arXiv:2006.06958 | rezumatul (deja în protocol) | geometria minimelor (lățimea) influențează uitarea | dacă se citează pentru legătura uitare–‖Δw‖ prin curbură, **de verificat în text**: nu am confirmat-o acum |
| de Haan et al. 2026, „Continual Learning through Control Minimization”, arXiv:2602.04542 | doar rezumatul căutării | uitarea ca creștere a pierderii vechi sub o aproximare pătratică | fundal |

**Citările FOREVER** (Semantic Scholar, 4 nov. 2026): 13 lucrări, toate din 2026; niciuna nu examinează timpul centrat pe model (doar ca baseline sau în treacăt). Indexul Semantic Scholar nu e complet.

## 5. Verdictul, cu critică

1. **„τ ≈ Ση‖m̂‖” nu e o contribuție.** Poate apărea într-un articol doar ca verificare, cu derivarea în trei rânduri (pasul Adam + RMS în funcție de semnal/zgomot). R²-ul de 0,94 confirmă o aproximare cunoscută, nu una nouă. Formularea din predare („ce poate fi nou: (2) constatarea că… e practic suma Ση‖m̂‖”) e prea tare și trebuie retrasă.
2. **Ce n-am găsit și ar fi un pas mic, real:**
   - (a) un audit empiric al ceasului FOREVER față de competitori gratuiți (Ση din planificator, Ση‖m̂‖), **în setarea lor exactă** (program liniar reluat pe fază, momente resetate, LoRA pe q/v);
   - (b) „cel mai mic substitut suficient” și locul în care aproximarea cedează (granițele de sarcină, resetarea optimizatorului, factorii față de B·A);
   - (c) D3 față de D1: un ceas funcțional față de unul în spațiul parametrilor.
3. **Predicția testabilă de la (a):** dacă Ση explică cea mai mare parte din τ în setarea FOREVER, câștigul lor față de pași (+1,2% OP, un singur benchmark) poate veni din programul ratei, nu din „timpul modelului”. E o ipoteză; dacă iese, e cea mai clară constatare a studiului. **Limitare de declarat:** nu putem reproduce benchmark-ul lor (SuperNI, Qwen3 pe GPU mare); măsurăm reconstrucția ceasului pe faptele sintetice ale brațului LM, nu performanța lor.
4. **Riscul „era evident”** rămâne pentru (b). Pentru (a) e mai mic: e o constatare despre o metodă publicată, într-un detaliu de implementare pe care articolul nu îl descrie.
5. **Incertitudine:** căutarea nu e exhaustivă (fără Google Scholar, fără citările OpenReview). Conform regulii de lucru, înainte de a investi în scrierea articolului se cere o căutare independentă (promptul din `Prompturi\`).

## 6. Ce schimbă pentru pasul 2 (G2 pe LM)

- **Setarea FOREVER copiată:** Qwen3-0.6B, LoRA r = 8 pe q_proj și v_proj, α = 16 (codul; α = 32 ca variantă, după articol), dropout 0,05, AdamW cu weight decay 0, tăiere 1,0, η = 3e-4, warmup de 10 pași + scădere liniară **reluate la fiecare fază**, **optimizator recreat la fiecare fază**. Precizia: fp16 ca la ei, dacă merge pe RTX 3050; altfel bf16, declarat.
- **c_e:** τ pe factori (ca `DriftRecorderCallback`), primar; τ pe ΔW = (α/r)·B·A, secundar.
- **Telemetria pe pas:** η_t, ‖g‖, ‖g̃‖ (după tăiere), ‖m̂‖, Tr v̂, plus resetările și granițele de sarcină.
- **Scara de competitori pentru rata lui τ** (orb față de T1, ca în `g2_preview.py`): ΔN → + Ση → + Ση‖m̂‖ → + restul telemetriei.
- **Modelul nul teoretic:** predicția de câmp mediu η_t·√d·f(r̂_t), cu r̂ estimat din m̂ și v̂. Dacă explică τ la fel de bine ca C5d, rezultatul e „explicat de teoria cunoscută” și se scrie așa.
- **Reziduul** în funcție de timpul de la ultima resetare sau graniță de sarcină.
- **Înainte, pe CPU (minute):** G2 cu o familie întreagă lăsată deoparte (F3, singura de test cu reporniri ale ratei) și reziduul lui C5d lângă granițele de sarcină, pe tech2/tech3.
