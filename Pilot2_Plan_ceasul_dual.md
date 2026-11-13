# Pilot 2 — Plan de cercetare: ceasul propriei schimbări

**Titlu de lucru:** *Does an Agent's Own Change Keep Time? Testing an Experiential Index of Adaptation Against Clocks, Counts, and Logged Update Summaries*

**Autor:** Ioan Daniel Ionici · **Stadiu:** plan teoretic, versiunea 0.1 (27 octombrie 2026), înainte de înghețarea protocolului
**Pornește din:** *A Time of Their Own*, v1.1, §4 și Level 2 din Table 2 (https://doi.org/10.5281/zenodo.23687300); metoda studiului închis (https://doi.org/10.5281/zenodo.23666336) și codul lui (https://doi.org/10.5281/zenodo.23667154)
**Notă de transparență:** Perspective v1.1 spune că autorul nu plănuia să urmeze testele. Studiul acesta este o schimbare a acelui plan și o va declara explicit.

---

## 0. Întrebarea, într-o frază

Când o rețea Transformer învață continuu, **schimbarea acumulată a propriei stări**, c_e, prezice ce și cât va uita mai bine decât timpul scurs, numărul de pași și rezumatele de actualizare pe care platforma le înregistrează oricum? Poate agentul să folosească acest indice ca să decidă singur ce să repete?

## 1. Ce testăm din Perspective și ce nu

Perspective (§4) definește indicele experiențial

  c_e(t) = Σ_{τ<t} D(S(τ), S(τ+1)),

o sumă nedescrescătoare care costă un singur număr stocat, distinctă de deplasarea netă D(S(t₀), S(t₁)). Perspective numește alegerea lui D „o problemă deschisă” și fixează **patru criterii de admisibilitate**. Planul le preia exact:

| # | Criteriul din Perspective | Unde îl testăm |
|---|---|---|
| (a) | bate decodorii restrânși la statisticile locale ale actualizărilor | H1, competitorul C6 |
| (b) | supraviețuiește criteriului de reset și randomizării ordinii, acolo unde trebuie să reflecte istoria | H3, permutarea ordinii |
| (c) | prezice o consecință funcțională ulterioară mai bine decât numărarea evenimentelor și rezumatele de actualizare | H1, competitorii C1–C7 |
| (d) | e *folosit* de agent, nu doar decodabil din el | H4, Stadiul B, testul de dependență |

**Metrica principală a Level 2**, tot din Perspective: *validitatea predictivă pe unitatea de stocare* (H2).

**Ce nu testăm:** sursa de timp nerestaurabilă (Level 1), istoria și atribuirea (Level 3), detecția restaurării (Level 4), deciziile în buclă închisă în lumea externă (Level 5), nefalsificabilitatea dovezilor și agenții LLM în producție.

## 2. Poziționarea față de literatură

Prezicerea uitării nu e un teren gol. Planul trebuie să bată sau să egaleze onest ce există deja.

| Lucrare | Ce arată | Rolul ei în Pilot 2 |
|---|---|---|
| Kalajdzievski (2024), arXiv:2401.05605 | Uitarea la fine-tuning crește ca lege de putere decalată în numărul de pași | **Competitorul C1**, ajustat exact în forma aceasta |
| Jin și Ren (2024), arXiv:2402.01865 și arXiv:2406.14026 | Prezic exemplele uitate din asocieri între exemple și din reprezentări | Referință de stocare mare: nu e un singur număr |
| Su și Zhang (2026), arXiv:2609.32818 | Sondele de ordinul întâi prezic marginile, dar nu uitarea; limitele lor conțin un termen care măsoară cât se schimbă coeficienții pe parcursul rulării | Aliat apropiat: un termen de tip „drum parcurs” apare chiar în limitele lor |
| He, Bai și Yang (2026), arXiv:2602.20796 | Uitarea ca degradare indusă de deriva în spațiul parametrilor | Justifică D1 și D2 |
| Kirkpatrick et al. (2017), PNAS, 10.1073/pnas.1611835114 (EWC) | Deplasarea ponderată Fisher protejează sarcinile vechi | **D2** și deplasarea ponderată Fisher (C8b) |
| Mirzadeh et al. (2020), arXiv:2006.06958 | Uitarea depinde de deplasare și de curbura minimului | Justifică D2 |
| Lee, Goldt și Saxe (2021), ICML, arXiv:2107.04384 | Uitarea depinde de similaritatea dintre sarcini | **Competitorul C8**, metadate de similaritate |
| Toneva et al. (2019), arXiv:1812.05159 | Evenimente de uitare la nivel de exemplu | Definiția țintei la nivel de item |
| Si și Qin (2026), arXiv:2608.16141; van der Veldt et al. (2025), arXiv:2512.22045 | Deriva reprezentărilor crește cu sarcinile intermediare | Justifică D4 |
| Roseboom et al. (2019), *Nature Communications* | Durata estimată din schimbarea acumulată a activității unei rețele | Strămoșul conceptual al lui c_e, acolo pentru durată, aici pentru propria adaptare |

**Ce e nou, spus cinstit:** nimeni nu testează dacă **un singur indice, acumulat de agent, al propriei schimbări** prezice propria uitare mai bine decât ceasurile, numărarea pașilor și rezumatele logate. Și nimeni nu face asta cu competitori auditați pentru competență, cu randomizarea ordinii, cu excluderea statisticilor locale și cu utilizarea în buclă închisă. Contribuția posibilă e modestă, dar curată. Un rezultat negativ e la fel de publicabil, pentru că închide Level 2.

## 3. Sistemul

### 3.1 Agentul

- **Transformer decoder-only**, mic, pe CPU: 4 straturi, d_model 128, 4 capete, context 64, vocabular de aproximativ 512 simboluri, în jur de 0,8 milioane de parametri.
- **Optimizator:** AdamW. Ca test de robustețe, o variantă SGD cu momentum, unde ‖Δθ‖ și ‖g‖ se despart altfel.
- **Starea persistentă S:** parametrii θ, plus momentele optimizatorului (m, v), care se salvează în checkpoint. D se calculează pe θ, iar v se folosește ca estimare gratuită a lui Fisher (D2).
- **Diferența față de Pilot 1:** acolo agentul era un sistem plastic cu regulă delta, iar Transformer-ul era self-model-ul. Aici **agentul însuși e Transformer-ul**, iar self-model-ul (Stadiul B) e un mecanism separat care citește indicii.

### 3.2 Lumea: un flux de sarcini

Sunt două tipuri de sarcini, ca uitarea să nu depindă de un singur mecanism:
- **Fapte (cheie → valoare):** fiecare sarcină k are 128 de perechi. Cheile vin dintr-un fond comun, iar suprapunerea cheilor dintre sarcini controlează interferența. Intrarea are forma `[task_k] [cheie] → [valoare]`.
- **Reguli:** transformări algoritmice proprii sarcinii (de exemplu, adunare modulară cu modul și decalaj specifice), evaluate pe intrări ținute deoparte.

Fiecare rulare are o fază inițială de „copilărie”. În ea se învață și **sarcinile de referință**, care nu vor fi niciodată ținte. Pe ele se calculează D3 și D4.

### 3.3 Fluxurile (familiile de streamuri)

Fiecare rulare are în jur de 40 de sarcini și 20.000 de pași. Familiile sunt alese ca să **decupleze** timpul, pașii și schimbarea, dar includ și o familie naturală, unde decuplarea nu e forțată.

| Familie | Ce variază | Pe cine favorizează intenționat |
|---|---|---|
| **F1, naturală** | Sarcini noi la intervale egale, repetiție prin rotație fixă, LR constant | Numărarea pașilor (control pozitiv pentru C1) |
| **F2, noutate variabilă** | Sarcini noi intercalate cu re-expunere la date deja stăpânite, în cantități aleatoare | Nimic explicit. Aici pașii „ieftini” se despart de pașii care schimbă mult |
| **F3, programul LR** | Cosinus cu reporniri la momente aleatoare | Rata de învățare cumulată (C3) |
| **F4, pauze** | Intervale aleatoare fără nicio actualizare | Nimic. Timpul pierde trivial, iar asta se raportează doar ca verificare |
| **F5, test ținut deoparte** | Combinație de F2–F4, cu altă proporție de sarcini-regulă | Familie folosită doar la testare, niciodată la ajustare |

**Permutarea ordinii (criteriul b):** pentru o parte din semințe, același multiset de expuneri e rulat în 4 ordini diferite.

### 3.4 Gradul de libertate al proiectantului, recunoscut explicit

Alegerea familiilor influențează rezultatul. Am patru protecții:
1. F1 (naturală) e inclusă și raportată separat.
2. F5 e o familie nefolosită la ajustare.
3. Familiile și ponderile lor se îngheață înainte de rulările principale.
4. Stadiul C repetă testul pe un flux real (fine-tuning continuu al unui model de limbaj preantrenat), unde nimic nu e construit de noi.

## 4. Indicele c_e și distanțele D

| D | Definiție | Cost | Observații |
|---|---|---|---|
| **D1** | ‖θ(τ+1) − θ(τ)‖₂ | neglijabil, la fiecare pas | „O distanță între ponderi nu e o diferență de funcție” (Perspective); e candidatul ieftin și slab |
| **D2** | √(Σᵢ vᵢ·Δθᵢ²), cu v = al doilea moment Adam | neglijabil | Ponderare de tip Fisher fără stocare suplimentară |
| **D3** | distanța Jensen–Shannon (√JS) între distribuțiile de ieșire înainte și după, pe bateria de referință R (256 de intrări) | 2 treceri forward pe R, la fiecare k = 10 pași | √JS e o metrică, deci suma pe bucăți e o limită inferioară a sumei pas cu pas; k e fixat în configurație |
| **D4** (secundar) | 1 − CKA liniar al ultimului strat ascuns, pe R | ca D3 | Distanță reprezentațională |

- **Deplasarea netă** Disp^D(t₀, t₁) = D(S(t₀), S(t₁)) cere stocarea întregii stări S(t₀), adică aproximativ 0,8 milioane de numere pentru fiecare t₀.
- **c_e** cere un singur număr pentru fiecare t₀.
- **Exact asta compară H2:** validitatea predictivă pe unitatea de stocare.

**D\*** e singura distanță folosită în H1 și H4. Se alege dintre D1–D3 pe rulările de calibrare și validare și se îngheață înainte de test, ca să nu existe alegere după rezultat.

## 5. Ținta: consecința funcțională

- **T1 (principală): uitarea sarcinii k în intervalul (t₀, t₁].** t₀ e sfârșitul ultimei expuneri a sarcinii k (antrenare sau repetiție), iar t₁ e un punct de evaluare ulterior.
  - F_k(t₀, t₁) = pierderea medie la t₁ minus pierderea medie la t₀, pe itemii sondă ai sarcinii k.
  - Itemii sondă sunt împărțiți în **două jumătăți disjuncte, A și B**. Ținta se calculează pe A, iar B servește la estimarea fidelității (plafonul).
- **T2 (secundară): deriva comportamentală** pe o baterie B_beh, disjunctă de R și de sarcinile-țintă.
- **T3 (Stadiul B): retenția** sub un program de repetiție cu buget fix.

**Unitatea de date:** perechea (sarcina k, t₀, t₁), pe o grilă de evaluare la fiecare 200 de pași. **Unitatea de inferență:** rularea, pentru că perechile din aceeași rulare nu sunt independente.

## 6. Competitorii

Fiecare competitor costă cel mult câteva numere stocate. Excepție fac referințele de stocare mare, marcate separat.

| Cod | Predictor pe (t₀, t₁] | Ce reprezintă |
|---|---|---|
| C0 | Δc_a, timpul simulat scurs (inclusiv pauzele) | Ceasul de pe perete |
| C1 | ΔN, numărul de pași, ajustat ca a·(ΔN + b)^c | Legea lui Kalajdzievski |
| C2 | numărul de tokeni sau exemple văzute | Volumul de date |
| C3 | Σ η_t, rata de învățare cumulată | Pași ponderați cu programul LR |
| C4 | Σ L_t, pierderea de antrenare cumulată | „Surpriza” |
| C5 | Σ ‖g_t‖, norma cumulată a gradientului brut | Rezumat de actualizare logat; sub Adam diferă de D1 |
| C6 | media și abaterea lui ‖Δθ‖ în ultimele W pași înainte de t₁ și în primii W pași după t₀ | **Statisticile locale**: scurtătura din Pilot 1, criteriul (a) |
| C7 | numărul de sarcini noi și de repetiții din interval | Numărarea evenimentelor cu semantică |
| C8 | Σ suprapunerea cheilor dintre sarcina k și sarcinile intermediare | Metadate de similaritate ale lumii. Agentul nu le are, deci e o referință, nu un rival |
| C8b | Disp^{D2} față de S(t₀) | Deplasarea ponderată Fisher (EWC). Stocare mare |
| C9 | răspunsul de ordinul întâi: produsul scalar dintre gradientul sarcinii k la t₀ și actualizarea cumulată | În spiritul Su–Zhang și Jin–Ren. Stocare mare |

**Covariatele comune** sunt date tuturor modelelor: tipul sarcinii, vârsta ei, numărul de repetiții anterioare și pierderea la t₀.

**Auditul competenței** (lecția centrală din Pilot 1): fiecare set de predictori primește aceeași familie de modele și același buget de ajustare. Familiile sunt (i) un model monoton pe log-predictori (GAM sau izotonic) și (ii) arbori boosting mici. „Cel mai bun competitor” se alege pe validare, nu după test.

## 7. Ipotezele, fixate dinainte

**SESOI** (cea mai mică diferență de interes): ΔR² = 0,05 absolut în Stadiul A. În Stadiul B: +2 puncte procentuale de retenție la buget egal, sau 10% mai puține repetiții la retenție egală.

| | Ipoteza | Test de superioritate | Pereche de echivalență (TOST, ±SESOI) |
|---|---|---|---|
| **H1** (principală) | Adăugarea lui Δc_e^{D\*} la modelul celui mai bun competitor crește R² pe date ținute deoparte pentru T1 | ΔR² ≥ SESOI, unilateral, pe toate rulările ținute deoparte (F1–F5); F5 se raportează separat | Dacă ΔR² e în ±0,05, **Level 2 se închide** pentru acest regim |
| **H2** | Validitatea pe unitatea de stocare: c_e (1 număr) atinge cel puțin 80% din câștigul incremental al lui Disp^{D\*} (aproximativ 0,8 milioane de numere) | raportul și intervalul lui de încredere | — |
| **H3** | Sensibilitatea la ordine: la același multiset de expuneri, diferențele de uitare induse de ordine sunt prezise de diferențele lui Δc_e | Spearman > 0, cu intervalul de încredere peste 0; competitorii invarianți la ordine au varianță nulă aici | Dacă uitarea nu diferă cu ordinea peste zgomot, H3 e **neidentificabilă** și se raportează ca atare |
| **H4** (Stadiul B) | Un program de repetiție declanșat de Δc_e de la ultima repetiție bate cel mai bun program declanșat de un competitor (C1, C3, C4, C7), fiecare ajustat pe validare | ≥ SESOI la buget egal | Dacă diferența e în ±SESOI, echivalență |

**Multiplicitatea:** Holm pe H1–H4, α = 0,05 pentru întreaga familie de teste.

## 8. Gate-urile (metoda din Perspective §6 și din Pilot 1)

| Gate | Ce verifică | Criteriu | Dacă eșuează |
|---|---|---|---|
| **G1, plafonul** | Fidelitatea țintei: corelația dintre jumătățile A și B, corectată Spearman–Brown | ≥ 0,70 pe calibrare | Mai mulți itemi sondă. Orice R² se raportează și ca fracție din plafon |
| **G2, identificabilitate** | Decuplarea dintre Δc_e și cel mai bun competitor | \|r\| < 0,95 (VIF < 10) pe datele ținute deoparte | H1 se raportează „neidentificabilă”, nu „echivalentă” |
| **G3, competență** | Competitorii sunt competenți | În F1, cel mai bun competitor bate covariatele singure cu ΔR² ≥ 0,10 | Comparația e invalidă până la reparare |
| **G4, scurgeri** | R e disjunctă de itemii-țintă; **placebo**: c_e luat dintr-o rulare-pereche (aceeași familie, altă sămânță) | Placebo: câștig incremental în ±0,01 | Bug de scurgere; se oprește analiza |
| **G5, statistici locale** | Criteriul (a): c_e bate C6 | Inclus în H1, raportat explicit | c_e nu e admisibil |
| **G6, debut vs. abilitate** | Concluzia nu depinde de volumul de antrenare al predictorilor (dublarea numărului de rulări de antrenare); în Stadiul B, de bugetul de antrenare al self-model-ului | Concluzia rămâne aceeași | Se raportează ca „debut”, nu ca „abilitate” |
| **G7, reproductibilitate** | Configurații înghețate cu SHA-256; reluările pe CPU identice bit cu bit, cu semințe fixe | 100% identice pe un eșantion | Nicio rulare principală nu pornește |
| **G8, folosit, nu decodabil** | Criteriul (d): la evaluare, c_e e înlocuit cu valoarea dintr-o rulare-pereche | Performanța scade până la nivelul competitorului | c_e e doar decodabil, nu folosit |

## 9. Analiza

- **Împărțirea datelor:** rulări de calibrare (doar pentru dimensionare și pentru alegerea lui D\*, apoi aruncate), rulări de antrenare (F1–F4), rulări de validare (F1–F4, alte semințe) și rulări de test (semințe noi pe F1–F4, plus toată F5).
- **Metricile:** R² în afara eșantionului, Spearman ρ și eroarea absolută medie, calculate pe fiecare rulare de test.
- **Inferența:** diferența pereche ΔR² pe fiecare rulare, cu interval de încredere bootstrap pe rulări (95%), test unilateral față de SESOI și TOST ±SESOI.
- **Dimensionarea:** varianța lui ΔR² între rulări se măsoară pe calibrare, iar numărul de rulări de test se alege pentru puterea de 80% la SESOI. Plafonul de buget e de aproximativ 200 de rulări. Dacă puterea nu se poate atinge în buget, se **reduce aria** (mai puține familii), nu standardul.
- **Ce se raportează întotdeauna:** fiecare familie separat, plafonul G1, toate gate-urile (inclusiv cele trecute) și toate rulările din inventar.

## 10. Stadiile de execuție

### Stadiul 0: construcție și calibrare (laptop)
1. Implementarea agentului, a lumii și a familiilor F1–F5, a indicilor D1–D4, a competitorilor C0–C9 și a țintelor T1 și T2.
2. **Teste unitare:** c_e e nedescrescător; √JS e o metrică; suma pe bucăți e cel mult egală cu suma pas cu pas; R e disjunctă de sonde; F4 nu modifică θ în pauze; determinismul.
3. Măsurarea timpului real pe laptop (vezi §11).
4. Calibrarea: G1 (numărul de sonde), varianța lui ΔR² (numărul de rulări), alegerea lui D\*. Pe rulări separate, care nu intră în test.
5. **Înghețarea:** protocolul în engleză, configurațiile cu SHA-256 și planul de analiză. Le depunem pe **Zenodo, cu DOI, înainte de rulările principale** (preînregistrare cu dată certă).
6. ▶ **Punctul tău de decizie:** mergem sau nu mai departe, pe baza calibrării.

### Stadiul A: validitatea predictivă (laptop)
Rulările principale, apoi H1–H3 și gate-urile G1–G7, apoi raportul. ▶ **Punctul tău de decizie:** dacă H1 e echivalentă, Level 2 e închis. Stadiul B devine atunci opțional și se raportează ca atare.

### Stadiul B: folosit de agent (laptop)
- **Sarcina:** repetiția cu buget fix. La fiecare decizie, agentul alege ce sarcină veche să repete.
- **Programele concurente:** un prag pe Δc_e de la ultima repetiție, față de praguri pe ΔN, Σ η, Σ L și C7. Fiecare prag e ajustat pe validare.
- **Varianta cu self-model învățat:** un model mic primește istoricul indicilor și prezice uitarea pe sarcină, cu și fără c_e, ca control cu informație echivalentă.
- **Analiza:** H4 și G8. Referința de plafon e un oracol care repetă sarcina cu uitarea reală maximă, ceea ce cere evaluarea tuturor sarcinilor.

### Stadiul C: scalare (pentru cine are GPU; varianta mini pe laptop)
- **Fluxul:** fine-tuning continuu al unui model preantrenat public (familia Pythia, de la 70M la 1,4B parametri) pe o secvență de domenii sau de sarcini.
- **Ținta:** pierderea sau marginile pe fapte și exemple din etapele anterioare.
- **D3** se calculează pe o baterie de text generic.
- **Aceiași competitori, aceleași gate-uri, același plan de analiză.** Se schimbă doar fișierul de configurație.
- Un rezultat care se păstrează aici nu mai poate fi atribuit construcției lumii sintetice.

## 11. Bugetul de calcul (de verificat în Stadiul 0)

- **Un pas** (batch 32 × 64 tokeni, aproximativ 0,8 milioane de parametri, CPU cu 8 nuclee): estimat la 10–20 ms. D3 la fiecare 10 pași adaugă în jur de 30%.
- **O rulare** (20.000 de pași plus 100 de evaluări): estimat la 8–12 minute.
- **Stadiul A:** 150–200 de rulări, deci 25–40 de ore CPU, adică câteva nopți.
- **Stadiul B:** încă aproximativ 20 de ore. **Stadiul C-mini** (Pythia-70M pe CPU): ore pentru fiecare rulare, cu un număr mic de rulări, doar ca test de fezabilitate.

Cifrele sunt estimări. Stadiul 0 le înlocuiește cu valori măsurate, înainte de înghețare.

## 12. Ce poate ieși și ce înseamnă

| Rezultat | Interpretare | Ce înseamnă pentru Perspective |
|---|---|---|
| H1 confirmată, inclusiv pe F5 | Propria schimbare acumulată prezice propria uitare dincolo de ceasuri, pași și rezumate | Level 2: primul suport empiric pentru ceasul dual |
| H1 echivalentă (TOST) | Numărarea pașilor sau rezumatele logate ajung | **Level 2 închis** în acest regim. Un rezultat negativ valid, pe care Perspective îl anticipează explicit |
| H1 confirmată doar pe F2–F4, nu pe F1 și F5 | Avantajul există doar unde l-am construit noi | Un avantaj de construcție, nu un rezultat general. Se raportează ca atare |
| G2 eșuează | Indicii nu se pot separa | Neidentificabil: nici confirmare, nici închidere |
| H2: c_e ≈ deplasarea, cu stocare de un milion de ori mai mică | Indicele ieftin conține informația deplasării | Confirmă afirmația „costă un singur număr” |
| H2: deplasarea e mult mai bună | Drumul nu ține locul destinației | Perspective trebuie să admită că c_e nu ține locul lui Disp |
| H3 confirmată | c_e reflectă dependența de drum, pe care numărarea nu o poate vedea | Criteriul (b) e satisfăcut |
| H4 confirmată, cu G8 trecut | Agentul folosește indicele pentru o decizie despre sine | Criteriul (d) e satisfăcut: puntea spre Level 5 |
| Stadiul C reproduce Stadiul A | Rezultatul nu e un artefact al lumii sintetice | Generalitatea minimă necesară |

**Niciun rezultat nu se reinterpretează după ce e văzut.** Interpretările din acest tabel se îngheață odată cu protocolul.

## 13. Amenințări la validitate

1. **Gradul de libertate în construirea fluxurilor:** tratat în §3.4 și prin Stadiul C.
2. **Zgomotul comun:** ținta și predictorii pot avea zgomot în comun, de exemplu dacă D3 și ținta folosesc aceleași intrări. Răspunsul: R disjunctă, placebo G4 și T2 doar secundară.
3. **Scurtătura statisticilor locale**, cea care a explicat rezultatul din Pilot 1: C6 e competitor explicit.
4. **Specificul optimizatorului:** varianta SGD.
5. **Scara:** un model mic. Stadiul C și formularea prudentă a concluziilor.
6. **Dependența perechilor din aceeași rulare:** inferența se face pe rulări.
7. **Alegerea lui D după rezultat:** D\* se îngheață după calibrare.

## 14. Ce livrăm

- **Codul** (MIT) și **datele și rapoartele** (CC BY 4.0), în același format ca la Pilot 1: configurații înghețate, inventarul rulărilor, verificări automate, scripturi care regenerează fiecare tabel.
- **Preînregistrarea** pe Zenodo, cu DOI, la sfârșitul Stadiului 0.
- **Lucrarea** (preprint pe Zenodo), cu legături „References” spre Perspective și studiul închis, și „Is supplemented by” spre arhiva de cod.
- **Declarația despre AI**, ca la lucrările anterioare. Niciun sistem AI nu apare ca autor.

## 15. Ce e „incontestabil” și ce nu

Niciun experiment nu e incontestabil ca existența Soarelui. Ce putem obține e altceva, și e suficient:
- **Întrebarea și criteriile au dată certă**, prin preînregistrare, deci nu pot fi ajustate după rezultat.
- **Oricine poate reface totul identic**, bit cu bit, pe un laptop.
- **Oricine poate schimba o singură alegere** (D, familia de fluxuri, modelul) și poate vedea unde se schimbă rezultatul.

Dacă alții obțin altceva, diferența va arăta exact ipoteza ascunsă care a decis. Și din asta se învață.
