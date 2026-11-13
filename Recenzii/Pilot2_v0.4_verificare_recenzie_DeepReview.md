# Verificarea recenziei Deep Review pe protocolul Pilot 2 v0.4

Recenzia: `Recenzie_DeepReview_Pilot2_v04.md` (Google Deep Review, Argon 4, adâncime Extra High, gândire High, 4 nov. 2026; 177 KB). Verificare făcută pe 4 nov. 2026, pe textul v0.4 (`../Pilot2_Protocol_EN_draft.md`) și pe codul Stadiului 0 (`../Stadiul0/p2/`). Fiecare punct are un verdict: **Întemeiat**, **Parțial** (problema e reală, dar remediul sau gravitatea nu se susțin întru totul) sau **Respins**. Etichetele FATAL/MAJOR sunt ale recenziei; gravitatea reală e în coloana „Gravitate verificată”.

## 1. Concluzie

- Recenzia e cea mai temeinică de până acum. Aproape toate punctele de fond sunt întemeiate, iar câteva sunt **confirmate în cod**: suprapunerea de intrări a sarcinii cu propriul segment (`run.py`, `open_episode` după segment), pozițiile 4–7 neutilizate (intrarea are 4 tokeni, `max_ctx: 8`), weight decay pe rândurile de embedding nefolosite (toate matricele 2D sunt „decayed”, `agent.py`).
- Nu sunt erori care să invalideze rezultatele de până acum: nicio mărime c_e incrementală nu a fost calculată, iar rulările tehnice rămân valabile ca rulări tehnice.
- **Calibrarea nu poate porni pe v0.4.** E nevoie de v0.5 (text) și de câteva modificări de cod, urmate de verificări și de o rundă tehnică nouă (F1–F6, c_e-orb).
- Recenzia răspunde și la întrebarea deschisă despre regula „valoarea incrementală a lui c_e nu se calculează înainte de înghețare” (punctul 5 din prompt): aruncarea rulărilor de calibrare nu ajunge; trebuie împărțit Stadiul 0 în 0a (orb față de c_e, singura fază în care designul se mai poate schimba) și 0b (automat, după blocarea designului). Recomand adoptarea (§3, B1).

## 2. Numere verificate (corecte în recenzie)

- 291 din 512 rânduri ale embedding-ului de intrare nu primesc gradient în viață în F1–F5 (64 valori + 32 cifre + 8 task de rezervă + ~3 speciali + 84 V_ref + 8 task de referință + 84 V_distractor + 8 task distractor); scad deterministic cu 1 − (1 − 3·10⁻⁶)^20480 ≈ 6%.
- G4b: σ²_ξ,r = s²[(1 − R²_r)/(2δ) − 1] e negativ când 1 − R²_r < 2δ (algebră directă).
- n = 16 rulări F2–F3: puterea 0,80 la efectul 2δ cere σ/δ ≤ √(16/7,85) = 1,43.
- H2: plafonul de jos 0,01 pentru δ_H2 subestimează n_H2 de (0,01/0,006)² = 2,78 ori la ΔR²(Disp) = 0,03.
- Stadiul B: 590 = 10 × 15 + 11 × 40 (§14) — corect, dar fără S-FOREVER pe validare, calibrarea θ_cal în buclă închisă, G6 în Stadiul B și reluările G7.
- Recenzia confirmă ea însăși ca exacte: multiplicatorii 10,51 / 7,85 / 10,47 / 13,51, formula G4b în cazul liniar ideal, plafonul r_AB (nu r²_AB), pragul de pacing, identitatea de urmă LoRA.

## 3. Punctele de fond

### A. Ținta T1 și plafonul

| # | Punct | Verdict | Gravitate verificată | Ce se face |
|---|---|---|---|---|
| A1 | Modelul de desfășurare al Stadiului B e antrenat „without the inclusion filter” (§8): fie preia regiunea saturată de după plafon, fie extrapolează în afara suportului | Întemeiat (ambiguitate reală în text) | MAJOR (Stadiul B) | §6: includerea separată în (a) filtrul de competență și (b) domeniul intervalului. §8: modelul de desfășurare e antrenat pe ΔN ≥ 64, fără filtrul de competență, pe ținta mărginită F^clip (vezi A3) |
| A2 | Plafonul cenzurează F6 (distractori: multă schimbare, uitare lentă), exact regimul pe care F6 trebuie să-l testeze | Întemeiat | MAJOR | Verificarea F6 raportată și la ΔN < 2.048 și fără plafon, pe ținte mărginite (F^clip, T1-acc); viteza uitării în F6 se măsoară în runda tehnică nouă |
| A3 | Pierderea tăiată la ln 64 (F^clip) poate fi calculată online, fără stocare per item: motivul de respingere din §21 („nu e stocată”) nu se susține | Întemeiat | MAJOR | Cod: `evals` primește L̄_A,clip și L̄_B,clip (un scalar în plus pe evaluare). Text: F^clip ca analiză de sensibilitate și țintă a modelului din Stadiul B; T1 rămâne ținta confirmatorie |
| A4 | T1-acc nu mai e la podea sub plafon, deci al doilea motiv de respingere nu mai ține | Întemeiat | MINOR | §21: motivul corectat. §15: condiție de interpretare: dacă H1 e susținută pe T1, dar ΔR² pe T1-acc ≤ 0, rezultatul se raportează ca efect pe scara pierderii, nu ca uitare funcțională (fără test nou în familia Holm) |
| A5 | Plafoane de încadrare: ΔN < 640 și < 2.048, ca sensibilitate | Întemeiat (ieftin) | MINOR | Raportate descriptiv |
| A6 | Plafonul favorizează c_e (direcția efectului) | Parțial: mecanismele sunt plauzibile, nu demonstrate | — | Analiza fără plafon și plafoanele de încadrare răspund la întrebare |
| A7 | Ponderea episoadelor: plafon de jos max(M, 3) | Respins | — | Ponderea egală pe episod e intenționată; se precizează că un episod valid are ≥ 1 triplet inclus (codul face deja așa) |
| A8 | C6 acoperă 25–50% din intervalele scurte; ferestre micșorate la min(8, ⌊ΔN/8⌋) | Respins ca remediu | — | Problema e reală (W_eff e mereu 16, se notează), dar micșorarea ar slăbi competitorul și ar favoriza c_e; C6 rămâne cum e |
| A9 | Bazele lui C1 ({1, 10, 100}) aproape colineare în [64, 1.280) | Parțial | MINOR | Contează doar pentru ridge (arborii sunt invarianți la transformări monotone): noduri {64, 256} în baza ridge |

### B. Stadiul 0 și calibrarea (răspunsul la întrebarea despre c_e)

| # | Punct | Verdict | Gravitate verificată | Ce se face |
|---|---|---|---|---|
| B1 | Deblocarea în Stadiul 0: după ce se vede ΔR²(c_e) pe calibrare, autorul poate „simplifica designul” sau opri; semințele se fixează abia după | Întemeiat | **FATAL** (pentru validitatea preînregistrării) | Stadiul 0 împărțit: **0a** (orb față de relația c_e–T1: copilărie, numărători, G1, G2, G3, G3b, G4b, δ, m_ch, ratele D3/D1_rel, debit) — singura fază în care designul se mai poate schimba; **0b** (automat, după blocarea designului: D\*, G4, G5, G2b, σ̂_up, σ̂_up(Z), δ_H2, N_test; dacă 0b pică, studiul se oprește cu raport). Listele de semințe pentru toate etapele, disjuncte, generate și hash-uite înainte de calibrare |
| B2 | D\* ales prin argmax fără filtrul porților | Întemeiat | MAJOR | D\* ales doar dintre candidații care trec G2, G4 și G5 (cu C1, vezi C1) pe F2–F3, cu hiperparametrii B_strong blocați; ordine fixă la egalitate |
| B3 | Domeniul de agregare nespecificat (F2–F3 sau toate cele 24) pentru D\*, G3b, G4b, G5, G2b, δ_H2 | Întemeiat | MAJOR | Toate pe cele 16 rulări F2–F3, cu excepția G3 pe F1 |
| B4 | Lipsește un prag de jos pentru variația ratei, CV(ρ̄) | Întemeiat | MAJOR | Criteriu în 0a: CV mediu în rulare al lui ρ̄ ≥ 0,10; plus praguri numerice pentru „varianța nenegligabilă” a țintei și minimum de tripleți sub plafon pe rulare |
| B5 | G4b: varianță negativă, atenuare prin pante diferite între rulări, putere mică la n = 16 | Întemeiat | **FATAL** (poarta poate pica fals) | Z = a_r·ẽ + ξ cu Var(ξ) = a_r(1 − a_r)s²: panta e 1 în fiecare rulare, varianța e pozitivă (verificat algebric: Cov(ẽ, Z) = Var(Z) = a_r s²). Cerința „supported” evaluată prin simulare la n_H1, nu pe 16 rulări. Obiecția de „scurgere” din rularea de evaluare se respinge: G4b construiește Z din țintă prin definiție |
| B6 | Controlul de fragmentare (m_ch = 1 doar pe o fereastră de 2.048 de pași) nu permite ΔR² în afara pliului | Întemeiat | MINOR | Criteriul: Spearman ≥ 0,98 pe Δc_e și pe rata ρ̄ în fereastră; comparația ΔR² între m_ch = 8 și 4 pe toate rulările |
| B7 | Montarea memoriei înainte de calibrare; fixarea proceselor pe nucleele P | Întemeiat (memoria); plauzibil (nucleele P) | MAJOR (cost) | Memoria se montează înainte de calibrare (planul existent). Efectul fixării pe nucleele P se măsoară, nu se presupune |

### C. Porți și inferență

| # | Punct | Verdict | Gravitate verificată | Ce se face |
|---|---|---|---|---|
| C1 | G5 compară X_cov + c_e cu X_cov + C6, dar perechea {Δc_e, ρ̄} dă exact ΔN, iar X_cov și C6 nu conțin durata | Întemeiat | **FATAL** (G5 ar trece banal) | G5: X_cov + C1 + c_e față de X_cov + C1 + C6 |
| C2 | G2 în Stadiul A amestecă familii, include intervale ΔN = 0 și folosește constrângeri monotone | Întemeiat | MAJOR | G2 doar pe ΔN ≥ 64, GBDT fără constrângeri, R² mediu în rulare; separat pe F2+F3 (poarta), F5, F6 |
| C3 | G4 pe familie, cu n = 5–8, oprește fals studiul cu probabilitate mare | Întemeiat | MAJOR | Oprirea fermă pe domeniul H1 (F2+F3), medie peste 20 de permutări fixe; celelalte familii descriptiv; blocuri în pași N, nu în ticuri |
| C4 | Varianța replicilor de antrenare (σ²_train) lipsește din formula mărimii eșantionului | Întemeiat | **FATAL** (putere supraestimată; la σ_train ≥ 0,31δ, nicio mărime nu ajunge) | σ²_train estimat la Stadiul 0 (bootstrap pe rulările de antrenare din pliu) și inclus în formule; simularea de putere decide; dacă σ²_train e mare, antrenare pe 60 de rulări |
| C5 | Deplasarea z₀ din BCa (replici cu ~19 rulări unice din 30) | Parțial (plauzibil, mărimea necunoscută) | MINOR | Replicile centrate pe modelul complet m₀; aceeași listă de rulări pentru toate seturile comparate |
| C6 | H2: contrastul Z_r neplafonat, dar marja δ_H2 plafonată la 0,01 | Întemeiat | MAJOR | Plafonul 0,01 eliminat din δ_H2 |
| C7 | Holm: nespecificat ce p-valoare ordonează ipotezele și regula de oprire | Întemeiat | MINOR (claritate) | Procedura scrisă pas cu pas prin intervalele BCa la nivelurile ajustate |
| C8 | F6: „limita superioară ≥ 0” trece și la estimări negative cu interval larg (sarcina dovezii inversată) | Întemeiat | MAJOR | Trei rezultate: trecut (limita inferioară > −δ), înșelător (limita superioară < 0), neconcludent |
| C9 | Regula de divergență: re-tunare nepereche; „echivalent” blocat și „neconcludent” re-tunat cu diferență ≤ 0,01 închide Level 2 | Întemeiat | MAJOR | ΔR² re-tunat ca contrast pereche cu aceeași configurație; închiderea Level 2 cere ca și varianta re-tunată să fie „echivalent” |
| C10 | Niveluri α inconsecvente (G4, G5, G8 „one-sided 95%”) | Întemeiat | MINOR | Aliniat la α = 0,025 sau declarat explicit ca nivel al porților |

### D. Competitori, distanțe și agent

| # | Punct | Verdict | Gravitate verificată | Ce se face |
|---|---|---|---|---|
| D1 | C0 (Δc_a) ≡ ΔN pe toate rulările F1–F3 (fără pauze): modelele împart greutatea pe C0 și greșesc pe F4/F5 | Întemeiat | MAJOR (F5, F4; nu H1, care e pe F2+F3) | C0 redefinit ca ticuri de pauză Δc_a − ΔN (același spațiu liniar, zero pe F1–F3) |
| D2 | Context maxim 8 cu intrări de 4 tokeni: pozițiile 4–7 nu primesc gradient și doar scad | Întemeiat (**confirmat în cod**: `train_x` are 4 coloane, `max_ctx: 8`) | MAJOR | `max_ctx: 4` |
| D3 | Weight decay pe rândurile de embedding fără gradient (inclusiv V_ref după copilărie): semnal Σ η determinist în D1, ‖θ‖, C5f, C6b și numitorul D1_rel | Întemeiat (**confirmat în cod**: toate matricele 2D sunt „decayed”) | MAJOR | Embedding-ul de intrare și cel pozițional scoase din weight decay (stratele liniare și capul de ieșire rămân); copilăria se reverifică |
| D4 | Suprapunerea de intrări q_hist(t₀) include propriul segment s₀ (prima sarcină: suprapunere 1,0 cu istoric gol) | Întemeiat (**confirmat în cod**: `overlap` calculat în `open_episode`, după segment) | MAJOR (covariabilă coruptă) | q_hist luat la începutul segmentului s₀ |
| D5 | L_R(t₀) lipsește din X_cov; C10b se anulează între itemi când masa se mută între tokenii-valoare | Întemeiat (mecanism plauzibil) | MAJOR (competitor slab tocmai față de D3) | L_R(t₀) în X_cov (0 stocare în plus); competitor nou **C10c** = Σ pe fragmente a mediei per item a lui \|Δℓ\| pe R, din aceleași treceri ca D3. Entropia: nu se adaugă |
| D6 | Poarta de eligibilitate pentru D3 (raporturi Q2–Q4 în [0,5; 2], Spearman ≥ 0,5, diversitate ≥ 0,15) | Respins (praguri arbitrare) | — | Rămâne raportarea descriptivă |
| D7 | C9 „never on probe half A”: la fapte, itemii de antrenare sunt A ∪ B, deci gradientul ar folosi jumătatea A | Întemeiat | MAJOR (C9 e de referință, exploratoriu; nu e încă în cod) | Gradientul lui C9 doar pe jumătatea B |
| D8 | Disp^{D1_rel} nu e invariant la scară (folosește diferența după weight decay) | Întemeiat | MINOR (după D3 scade mult) | Se declară; se raportează și forma cordală propusă, ca sensibilitate, dacă D\* = D1_rel |
| D9 | D2: v̂ = 0 pentru rândurile tokenilor noi în primii 256–319 pași; „dinte de fierăstrău” la fiecare 64 de pași | Parțial | MINOR | v̂ = 0 e o proprietate de tip Fisher (curbură necunoscută = pondere zero), nu o eroare: se declară. Pasul blocului coborât la 16 (lag 256–271; ~20 de copii ≈ 74 MB pe proces) |
| D10 | Ridge: log1p pe sume mici e practic liniar; coloana log(ΔN + 1) dublată | Întemeiat | MINOR (ridge e secundar) | Sume pozitive scalate cu incrementul mediu pe pas, aceeași bază pentru toate; coloana dublă eliminată |
| D11 | F6: zgomotul etichetelor (0,3) umflă C4 și C5b | Parțial (plauzibil) | MINOR | Pe F6 se raportează și R²(X_cov + c_e) singur și eroarea medie cu semn |
| D12 | GBDT cu ratele constrânse monoton, ca sensibilitate | Respins | — | Fitul complet neconstrâns e deja sensibilitatea prevăzută |
| D13 | „Parametrii generatorilor nu sunt în protocol” | Întemeiat | MINOR | Tabel cu valorile înghețate F1–F6 (din `config_stage0.yaml`) și regula pentru brațul SGD |

### E. Stadiul B

| # | Punct | Verdict | Gravitate verificată | Ce se face |
|---|---|---|---|---|
| E1 | Bugetul Q (K_reh) nu are valoare numerică nicăieri | Întemeiat (verificat: nu apare) | **FATAL** pentru preînregistrarea Stadiului B | Q, familiile Stadiului B (F2 și F3), declanșarea S-oracle, grila lui T3 (doar grila fixă de 256 de pași) |
| E2 | Declanșatorul S-pred: salturi negative la reexpunerile externe; scara crește cu K_active | Întemeiat | MAJOR | Statistica: suma incrementelor pozitive pe 64 de pași, medie pe sarcinile active neantrenate; acumulatoarele repornesc la sfârșitul repetiției |
| E3 | Placebo-ul G8 pentru S-pred (rezidualul pe interval) nu e bine definit în buclă închisă | Întemeiat | MAJOR | Placebo la nivel de pas: reziduurile pe pas ale lui δc_e față de un predictor din telemetria pe pas, permutate în blocuri de 256 de pași, cu c_e ≥ 0 |
| E4 | n_B și costul Stadiului B nu pot fi calculate la Stadiul 0 | Întemeiat | MAJOR | La Stadiul 0 se îngheață formula și plafonul n_B,max; σ̂ al diferențelor se estimează pe cele 15 semințe de validare ale Stadiului B, înainte de orice test |
| E5 | Verificarea selecției sarcinii comparată cu LRR, nu cu S-pred(B_strong) | Întemeiat | MAJOR | Criteriu: cele două modele S-pred aleg sarcini diferite în ≥ 10% din repetiții, în aceleași stări |
| E6 | Numărul de rulări al Stadiului B subestimat (590 față de 719–989) | Întemeiat | MAJOR (cost) | Recalculat; θ_cal inițializat analitic din urmele Stadiului A, plus o singură trecere de verificare; G6 offline |

### F. Interpretare, domeniu, stocare, cost

| # | Punct | Verdict | Gravitate verificată | Ce se face |
|---|---|---|---|---|
| F1 | §15: rândul „H1 equivalent” nu cere G2, G4 și absența divergenței; rânduri suprapuse; lipsesc rândurile pentru H4 echivalent sau neconcludent, F5/F6 eliminate, Stadiul C nereprodus | Întemeiat (verificat pe text) | **FATAL** (tabelul e contractul înghețat) | §15 refăcut: porțile de bază și divergența au precedență; rânduri exclusive; rândurile lipsă adăugate |
| F2 | G2 picat înseamnă reconstructibilitate, nu doar neidentificare | Parțial | MAJOR | G2 picat: „rata lui c_e e reconstructibilă din telemetrie; H1 nu e identificabilă ca echivalență”. G2 nu anulează un H1 susținut, dar se raportează alături |
| F3 | Domeniul (fapte, ΔN < 1.280, parametri compleți) nu e trecut în §0.3 și §15 | Întemeiat | MAJOR | Formulările din §0.3 și §15 restrânse la retenția asociativă în eșantion; §21, rândul 1, completat cu §15 |
| F4 | Stocarea: „un scalar” e adevărat doar pentru D1 și D1_rel; D2 cere copii de v̂, D3 cere ieșirile anterioare pe R | Întemeiat | MAJOR (H2, metrica Level 2) | §1 și H2: stocare marginală pe sarcină și memorie de lucru globală, raportate separat, pe fiecare D |
| F5 | Costul conductei de analiză nemăsurat; „câteva minute-CPU” din §20 e optimist | Întemeiat | MAJOR | Măsurat în 0a (CV imbricat și un bootstrap de probă cu 25 de replici); criteriul de cost include timpul de ajustare |
| F6 | H3: „bugetul din §12a” nedefinit după noul criteriu; costul supraestimat (ramurile sunt scurte) | Întemeiat | MINOR | Condiție în ore de ceas |

### G. Corecturi mici (toate acceptate, cu o excepție)

§0 „main run” definit; §0.5 lista competitorilor; §0.7 q₀ („multipli”, iar pașii fragmentelor îl divid); §3 numărul exact de parametri și §4.3 viața de 20.480 de pași; §4.1 „4 tokeni speciali”; §5.1 W_out inclus explicit în ℓ, paranteze, L_τ; §5.2 „la toate punctele de evaluare”, nu doar pe grilă (așa face codul); §6 claritatea r_AB; §7 „≤ 2 scalari” → „≤ 4”; W_eff mereu 16; B_strong⁺ definit; §8 replicile bootstrap cu rânduri duplicate; §9 S-FOREVER pe grila de 64; §10.3 parametrii blocurilor H3; §11 G6 și numărul rulărilor; §12 13,51 și n_H4; §12a rândul Headroom complet și lista în afara pliului; §13 notația; §14 rulările de diagnostic; §16 formularea „Over-weighting”; §17 lista valorilor înghețate; §18 referințele necitate (Loshchilov, Mirzadeh, Roseboom, Toneva) se citează sau se scot, iar Pythia și LoRA primesc autorii; §20 nota „înlocuit în v0.4”.
**Respins:** în §21, rândul 1, „§13 nu a fost afectat” — §13 a fost modificat în v0.4 (covariabila „tipul sarcinii”); se adaugă doar §15. Respins și plafonul Δc_a < 1.280 pentru intervalele de pauză: uitarea cere pași, iar ΔN = 0 nu produce uitare.

## 4. Ce urmează (ordinea propusă)

1. **Cod** (copii vechi păstrate): `max_ctx: 4`; embedding-urile scoase din weight decay; q_hist la începutul segmentului; L̄_clip în evaluări; C10c și L_R(t₀); C0 ca ticuri de pauză; pasul blocului D2 la 16; verificările `checks_stage0.py` actualizate și rulate.
2. **Rundă tehnică nouă, c_e-orbă**: F1–F6, rata 3e-4, pe configurația nouă (copilăria reverificată după schimbarea weight decay; viteza uitării în F6 și F5). Patru procese, ~50 de minute; se poate face înainte de memorie.
3. **v0.5** prin script, cu jurnalul §22 (fiecare punct de mai sus cu sursa R4 = această recenzie).
4. **Semințele** pentru toate etapele, generate și hash-uite; scriptul fazei 0b scris înainte de calibrare.
5. Montarea memoriei, testul, reluarea cu comparare de hash-uri; apoi calibrarea (0a → 0b).

**De decis de autor:** (a) adoptarea împărțirii Stadiului 0 în 0a/0b în locul regulii actuale despre c_e (recomandat); (b) valoarea bugetului Q al Stadiului B (propunere: K_reh = 32 de repetiții de 64 de pași, ≈ 10% din viață; de verificat față de regimul de uitare); (c) dacă embedding-urile se scot complet din weight decay (recomandat, mai simplu) sau doar rândurile nefolosite.
