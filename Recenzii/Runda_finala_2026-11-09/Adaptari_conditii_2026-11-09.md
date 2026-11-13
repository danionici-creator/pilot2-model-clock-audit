# Runda finală: condițiile serviciilor și configurația trimiterilor (addendum, 9 nov. 2026)

Scris după verificarea paginilor serviciilor (Claude in Chrome, ~11:55–12:00) și **înainte de orice trimitere**.
Regula de adoptare (`Regula_de_adoptare_2026-11-09.md`) nu se schimbă. Addendumul fixează doar logistica.

## CMU Paper Reviewer (https://prometheus-eval.github.io/cmu-paper-reviewer/)

**Condiții afișate pe pagină:**
- 3 evaluări gratuite pe zi;
- adresa de email e obligatorie (evaluarea vine în 10–15 minute);
- manuscrisul: cel mult 100 de pagini; un PDF suplimentar: cel mult 50 de pagini; 50 MB pe PDF;
- cod: un zip de cel mult 50 MB, extras în spațiul de lucru al agentului evaluator, care poate genera cod de verificare;
- setări: criterii „Nature”, „NeurIPS” sau „Custom”; numărul de puncte critice, între 1 și 10 (implicit 5); „cunoștințe
  recente” și „poate critica și punctele din secțiunea de limite”, ambele bifate implicit;
- câmp opțional pentru o anumită secțiune sau temă;
- folosirea datelor: manuscrisele, evaluările și reacțiile pot fi colectate și folosite în scop de cercetare, nu
  comercial; studiul e aprobat de comisia de etică (IRB) a CMU.

**Trimiterile (2 din cele 3 permise azi; a treia rămâne în rezervă):**
1. **Raportul:** `Pilot2_closure_report_review_draft.pdf` (12 pagini), cu codul ca zip
   `_work\zenodo_pilot2\pilot2_code_for_review_2026-11-09.zip`. Zip-ul conține copia publică a depozitului: 631 de
   fișiere, 4,5 MB, SHA-256 `e5fee11a8c6639c64c2bcdccb84d6c602e7891c85254e06c0f252a62f2e83624`, fără partea de date
   (665 MB, peste limită). Criterii: NeurIPS; 10 puncte; setările implicite bifate; câmpul de temă gol.
2. **Ciorna Perspective v1.4:** `Perspective_v1.4_review_draft.pdf` (20 de pagini), cu raportul ca PDF suplimentar,
   ca să se poată verifica integrarea. Criterii: Nature (e o lucrare conceptuală, nu un articol de conferință);
   10 puncte; setările implicite; câmpul de temă gol.

## Stanford Agentic Reviewer (https://paperreview.ai)

**Condiții afișate pe pagină:**
- gratuit;
- un PDF de cel mult 10 MB, din care se analizează doar primele 15 pagini;
- adresa de email e obligatorie;
- revista sau conferința țintă e opțională (o listă, plus „Other”).

Pe site (prima pagină și pagina tehnică) nu am găsit o declarație despre folosirea datelor trimise.

**Trimiterile:**
1. **Raportul:** 12 pagini, deci analizat integral. Ținta: NeurIPS.
2. **Ciorna Perspective v1.4:** 20 de pagini. Primele 15 cuprind tot textul până la concluzie inclusiv (pagina 15).
   Declarația despre AI (pagina 16) și referințele (paginile 17–20) nu se analizează; limita se notează la verificare.
   Ținta: „Other”.

## Alternative căutate

Am căutat alte servicii gratuite de evaluare automată a articolelor, cu o calitate verificabilă. N-am găsit unul mai
bun decât cele două. Studiul CMU din mai 2026 (arXiv:2605.20668) compară CMU Paper Reviewer cu Stanford Agentic
Reviewer și cu OpenAIReview. OpenAIReview cere o cheie API proprie, deci are costuri. Celelalte servicii găsite apar
doar în pagini de marketing ale propriilor furnizori. Faza 2 rămâne neschimbată.

## Datele personale

Ambele servicii cer adresa de email a autorului. O introduce autorul sau, cu acordul lui explicit, asistentul.
