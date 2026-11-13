# Faza 2: trimiterile (9 nov. 2026)

**Ce s-a trimis:**
- Celor cinci modele: același mesaj, adică `Prompt_analiza_EN.txt` (SHA-256 `5c5d7d46…`, verificat în câmpul de mesaj
  înainte de trimitere, acolo unde câmpul permitea), plus cele două PDF-uri din faza 1, neschimbate (amprentele fixate
  la 11:53).
- La Deep Review: `Dosar_combinat_DeepReview.pdf`, cu contextul `Prompt_analiza_EN_DeepReview.txt` (vezi addendumul
  din `Regula_de_adoptare_2026-11-09.md`).

Niciun răspuns din faza 2 nu a fost citit înainte de ultima trimitere. Linkurile conversațiilor sunt păstrate local, în
afara arhivei: sunt conversații private.

| Evaluator | Familia | Model și setări, cum le arăta interfața | Ora (aprox.) | Note |
|---|---|---|---|---|
| Deep Review | americană (Google) | Argon 4, adâncime și raționament „Medium” (cota gratuită) | ~13:30 | un singur PDF combinat; contextul identic cu promptul, cu excepția primei fraze; identitatea textului verificată prin SHA-256, după normalizarea capetelor de linie |
| DeepSeek | chineză | „Gândire profundă” și „Căutare inteligentă” activate | ~13:40 | SHA-256 al textului din câmp = `5c5d7d46…` |
| Mistral (Le Chat, „Vibe Work”) | europeană | modul „Think” (alternativa era „Fast”) | ~13:45 | Le Chat a transformat textul lipit într-un bloc de text atașat; conversația îl afișează întreg. API-ul Mistral Large 4 nu s-a folosit: dosarul are aproximativ 35.000 de tokeni, peste limita de 20.000 de tokeni pe minut |
| GLM (Z.AI) | chineză | GLM-5.3 (alternativele: 5.3-Flash, 5.2); efort „Max” | ~13:50 | autentificarea a făcut-o autorul; SHA-256 = `5c5d7d46…` |
| ChatGPT | americană | contul Plus, efort de gândire „High” (maximul cursorului) | ~13:55 | textul din editor e identic cu promptul, cu spațiile normalizate |
| Gemini | americană | 3.1 Pro (4 Argon e blocat în cont), nivel de gândire „High” | ~14:00 | textul din editor e identic cu promptul, cu spațiile normalizate |

**Excluși:** Claude (asistentul care a lucrat la studiu) și Copilot (a văzut deja raportul; poate fi doar martor, dacă
hotărăște autorul).

**Incidente:**
- **Le Chat** a răspuns de două ori „This model is at full capacity”. După două „Retry” (același mesaj), a răspuns în modul Think.
- **Gemini:** prima conversație s-a pierdut („Couldn't load this chat. It doesn't exist or was deleted”), fără niciun răspuns. Mesajul a fost retrimis identic (aceleași PDF-uri, 3.1 Pro, gândire High) la ~15:10.
- Înainte de retrimitere, la verificarea stării, au fost văzute doar ultimele rânduri ale unor răspunsuri din faza 2 (DeepSeek, GLM, Le Chat, ChatGPT). Mesajul retrimis e fix și identic, deci asta nu-l putea influența.
