# Runda finală de evaluare externă (9 nov. 2026): ordinea și regula de adoptare

**Fixată și amprentată înainte de orice trimitere și înainte de citirea oricărui răspuns.** Runda evaluează
corectitudinea rezultatelor Pilot 2 și integrarea lor în Perspective v1.4. Nu e un colocviu de direcție și nu se
votează.

## Ce primesc evaluatorii

- `Pilot2_closure_report_review_draft.pdf`: raportul de închidere, ciornă pentru evaluare. Diferă de sursă doar prin
  antet (locurile pentru DOI și linkul GitHub privat sunt înlocuite).
- `Perspective_v1.4_review_draft.pdf`: Perspective v1.4, ciornă pentru evaluare. Construită dintr-o copie a surselor,
  cu toate punctele M1–M17 din `D:\Time\Perspective_v1.4_propunere.md`, inclusiv cele opționale.
- Pentru modelele din faza 2: `Prompt_analiza_EN.txt`, identic pentru toate.

## Ordinea

**Faza 1, evaluatori automați de articole, fără întrebările noastre.** Fiecare evaluează fiecare document separat, așa
cum l-ar citi un cititor neutru.

1. CMU Paper Reviewer: întâi raportul, apoi ciorna v1.4. (A evaluat și v1.3, deci se poate vedea dacă punctele lui
   de atunci sunt rezolvate.)
2. Stanford Agentic Reviewer: întâi raportul, apoi ciorna v1.4.

După faza 1 se verifică fiecare punct. Se corectează **doar erorile de fapt verificate și punctele fatale
confirmate**. Fiecare corectură se notează, iar PDF-urile se reconstruiesc.

**Faza 2, modele de vârf din trei familii, cu promptul comun și ambele PDF-uri.** Fiecare primește cel mai bun model
disponibil în cont, cu setarea maximă de raționament afișată în interfață în ziua folosirii. Toate cinci primesc
același mesaj înainte să se citească vreun răspuns din faza 2.

- chinezești: DeepSeek (gândire profundă, cu căutare); Z.AI (GLM, cel mai bun mod de gândire disponibil);
- european: Mistral (Le Chat, modul Think, sau Mistral Large 4 prin API, dacă limitele permit documentele întregi);
- americane: ChatGPT (cel mai bun model, efort maxim); Gemini (cel mai bun model, gândire maximă).

**Excluși din numărătoare:**
- Claude: e asistentul care a lucrat la studiu, deci nu e independent;
- Copilot: a văzut deja ciorna raportului (opinia din `Raport_inchidere/Opinii/`). Poate participa doar ca martor
  fără vot, dacă autorul hotărăște.

## Regula de adoptare

1. **Fiecare afirmație a unui evaluator se verifică la sursă:** datele, jurnalele, codul, articolele citate. O
   recomandare care se sprijină pe o afirmație falsă se elimină.
2. **O eroare de fapt verificată se corectează,** indiferent câți evaluatori au semnalat-o.
3. **O obiecție de interpretare, de domeniu sau de formulare se adoptă dacă e ridicată de cel puțin doi evaluatori**
   din cei șapte care se numără (CMU, Stanford, DeepSeek, GLM, Mistral, ChatGPT, Gemini) și dacă verificarea o confirmă.
   O obiecție ridicată de un singur evaluator se poate adopta doar prin decizia explicită a autorului, notată ca atare.
4. **Un punct marcat FATAL și confirmat la verificare oprește publicarea** tuturor celor trei intrări Zenodo până la
   rezolvare.
5. **Opțiunile deschise** (lungimea rezumatului Perspective, amendamentul din §5, precedentul SI/Benzing și direcția
   agenților cu memorie) se numără ca opinii. Decizia rămâne a autorului (D1, D3, D6 din propunere).
6. **Totul se documentează:** răspunsurile se păstrează exact cum au venit, iar verificarea punct cu punct se scrie în
   `Verificare_runda_finala.md`. Ambele merg în arhivă, în `Recenzii/`.

## Condiții de lucru

- **Fiecare trimitere se face doar cu acordul autorului.** Trimite asistentul, prin conturile autorului, în browserul
  lui, ca la colocvii; sau trimite autorul.
- **Datele personale cerute de formulare** (de exemplu adresa de email pentru primirea evaluării) le introduce
  autorul, nu asistentul.
- **Numai servicii gratuite sau incluse în abonamentele existente.** Orice cost suplimentar cere un acord separat și un
  plafon fix.
- Răspunsurile nu se discută cu evaluatorii înainte de verificare.

## Addendum (9 nov. 2026, ~13:25, înainte de trimiterea fazei 2)

La cererea autorului („încearcă și Deep Review varianta gratuită cu setare de efort medium”), faza 2 include și **Deep
Review** (Google; Argon 4, adâncime și raționament „Medium”, cota gratuită). Deep Review primește un singur document:
`Dosar_combinat_DeepReview.pdf`, adică raportul (paginile 1–12) urmat de ciorna v1.4 (paginile 13–32). Contextul e
`Prompt_analiza_EN_DeepReview.txt`, identic cu promptul comun, cu excepția primei fraze, care descrie fișierul unic.
Deep Review se numără ca evaluator. Pragul pentru obiecțiile de fond rămâne **cel puțin doi evaluatori**, acum din
opt. Fără cheie API și fără costuri: dacă interfața ar folosi o cheie plătită, trimiterea se oprește.
