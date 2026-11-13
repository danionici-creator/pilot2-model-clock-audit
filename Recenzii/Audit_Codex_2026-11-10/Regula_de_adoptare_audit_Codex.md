# Regula de adoptare pentru auditul independent Codex (fixată pe 10 nov. 2026, ÎNAINTE de trimitere)

**Ce e:** un audit independent al pachetului Pilot 2 (cod, rezultate, interpretare, Perspective v1.4), făcut de OpenAI
Codex, la efort maxim, pe copia `D:\Pilot2_audit\` (depozitul public cu partea de date dezarhivată, raportul,
Perspective v1.4). Instrucțiunile trimise: `AUDIT_BRIEF.md` (copie în acest folder, amprentată). Codex lucrează doar în
`_audit\`, fără acces la `D:\Time`, fără rețea (în afară de pachetele Python listate), fără git. Proiectul îl deschide
autorul, din contul lui.

**Regula (aplicată de asistent, cu verificare punct cu punct în fișiere, înainte de orice schimbare):**
1. **Eroare de cod sau de fapt, verificată:** se corectează. Dacă atinge o analiză, analiza se reface, iar
   rezultatul nou se raportează alături de cel vechi (nimic șters; versiunea veche în `_work\_copii_siguranta\` sau în
   `runs/earlier_versions/`). Fișierele amprentate dinainte de rulări nu se modifică niciodată: o corectură de cod
   devine o versiune nouă, declarată ca post hoc.
2. **Eroare care schimbă un verdict sau o afirmație principală (fatală, confirmată):** publicarea pe Zenodo se
   oprește până la lămurire; schimbarea se discută cu autorul, iar o eventuală schimbare de direcție merge la colocviu.
3. **Observație de interpretare sau de formulare:** se verifică; se adoptă doar dacă e confirmată de fișiere sau de
   sursă. Un singur evaluator nu poate impune o schimbare de cadru (de exemplu redenumiri ale conceptelor); acestea se
   notează pentru o versiune ulterioară.
4. **Afirmație falsă a evaluatorului:** se notează ca atare, cu dovada, și nu se aplică.
5. Răspunsul se păstrează exact cum a venit (`_audit\AUDIT_REPORT.md` și scripturile lui, copiate în acest folder),
   împreună cu verificarea (`Verificare_audit_Codex.md`).

Publicarea pe Zenodo așteaptă rezultatul auditului și verificarea lui.
