# Colocviul de direcție Pilot 2: regula de decizie (fixată pe 6 nov. 2026, ÎNAINTE de orice răspuns)

**Principiul (cerut de utilizator, 6 nov.):** deciziile mari de direcție nu vin de la utilizator, un nespecialist, ci dintr-un colocviu al celor mai puternice modele AI disponibile, cu o regulă fixată dinainte. Ținta: o descoperire documentată sau închiderea definitivă, prin teste incontestabile, a ce se sprijină pe presupuneri, la noi sau la alții.

**Participanții** (fiecare primește același dosar și același prompt, fără să vadă răspunsurile celorlalți):
1. Deep Review (Gemini Argon, plătit, cu acordul utilizatorului din 6 nov.): PDF-ul dosarului + promptul în „Add custom context”;
2. ChatGPT, cel mai puternic model disponibil în contul utilizatorului, raționament maxim;
3. Gemini 3.1 Pro (High), în Gemini;
4. Copilot (Think Deeper);
5. Mistral Large 4 (raționament maxim disponibil).

Claude (autorul analizelor) **nu votează**: verifică doar faptele din răspunsuri și aplică regula.

**Pașii:**
1. Fiecare răspuns se salvează integral, nemodificat (`02_Pilot2\Colocviu\Raspunsuri\`).
2. **Verificarea punct cu punct:** fiecare cifră comparată cu dosarul și cu jurnalele; fiecare afirmație despre cod comparată cu codul; fiecare referință verificată (arXiv, Crossref, DataCite). Rezultatul: un tabel cu verdicte (întemeiat / parțial / fals / neverificabil).
3. **O recomandare se elimină** dacă argumentul ei principal se sprijină pe o afirmație falsă.
4. **Direcția** (întrebarea Q7, opțiunile A–D din prompt) = opțiunea cu cele mai multe recomandări rămase după verificare, câte un vot de participant. La egalitate: opțiunea mai ușor de infirmat și mai ieftină pe acest laptop. Dacă nicio opțiune nu are cel puțin 2 voturi rămase, se repetă colocviul doar pe întrebarea de direcție, cu argumentele rămase.
5. **Deciziile 1–8 din dosar** (§7): aceeași regulă, decizie cu decizie.
6. **Testele decisive:** cele propuse de cel puțin 2 participanți (după verificare) se preînregistrează primele, cu criteriile scrise înainte de rulare; celelalte se listează.
7. **Rolul utilizatorului:** dreptul de a opri sau de a amâna, nu de a alege între opțiuni.

**Integritate:** amprenta SHA-256 a acestui fișier, a dosarului și a promptului se notează în `Predare_fir.md` înainte de prima trimitere; orice schimbare ulterioară a regulii se notează explicit, cu motivul.
