# About this folder: the direction colloquia of Pilot 2 (6 and 8 November 2026)

*Part of the decision record. A Romanian version follows the English text.*

## What these documents are

This folder records how the two major direction decisions of Pilot 2 were taken. Unlike the evaluations of the
protocol drafts in `../Recenzii/`, which are an informative annex, the answers kept here were **inputs to decisions**:
the direction of the study was set by applying a rule, fixed in advance, to these answers after each had been checked.
For each colloquium the folder holds the dossier and the prompt that were sent, the decision rule, the hash lists
recorded before the first answer was read, the answers as received, the claim-by-claim verification, and the outcome.

## How the decisions were taken

- **Why.** The author is not a specialist in machine learning and chose not to take the major direction decisions
  alone. For each one, a dossier and a decision rule were written, and their SHA-256 hashes recorded, before any answer
  was read.
- **Independence.** Each participating AI system received the same dossier and the same prompt, separately, without
  seeing the other answers. The prompt asked for an adversarial reading: what is wrong, trivial or unsupported, and
  which test would settle it.
- **Verification.** Every number was checked against the dossier and the logs, every statement about code against the
  code, every reference against arXiv, Crossref or DataCite. A recommendation whose main argument rested on a false
  claim was struck out.
- **Rule.** The direction was the option with the most recommendations left after verification; ties went to the
  option cheaper on the laptop and easier to falsify. Tests proposed by at least two participants were preregistered
  first.
- **Roles.** The author kept the right to stop or to postpone, not to choose between options. The AI assistant that
  wrote the analyses and prepared the dossiers (Claude, Anthropic, in Claude Code) did not vote: it checked the answers
  and applied the rule.
- **Witness.** In each colloquium a further system (DeepSeek) answered the same dossier as a non-voting witness, added
  after the rule was fixed, to see whether a different family of models would agree. Its answer does not count.
- **A limit of the method.** The dossiers were prepared, and the answers verified, by the same assistant that carried
  out the analyses. Errors in the dossiers were mostly brought to light by the participants: three on 6 November (E1–E3),
  with a fourth (E4) found later during test T-D; on 8 November, an omission (the re-implementation also restarts AdamW
  in every phase) that misled all participants into the same wrong explanation. They are listed in the verification
  documents.

## How to read the answers

They are texts produced by AI systems, kept exactly as received (hashes in `Raspunsuri/SHA256SUMS.txt` for
6 November), and are not the author's views. They contain errors, which the verification documents mark; a point
should not be quoted without its verification. The conclusions of the study rest on the preregistered tests that the
colloquia chose, reported in the closure report (https://doi.org/10.5281/zenodo.24188374), not on the answers themselves. Model names and
settings are those shown by each provider on the date of use. `Raspunsuri/_proveniență.md` (Romanian) records how
each answer of 6 November was obtained; in this public copy, two links to the author's private conversations are
replaced by "[link privat, omis]" (the file is in no hash list; nothing else in it is changed).

## Index

| | Colloquium of 6 November | Colloquium of 8 November |
|---|---|---|
| Question | Direction of Pilot 2 after the technical rounds, and eight open design decisions (dossier §7) | What to do after reproducing FOREVER with the authors' code (R1, R2): options (a)–(e) |
| Dossier, prompt | `Colloquium_dossier_2026-11-07.md` (+ `.pdf`), `Colloquium_prompt_EN.txt` | `Dosar_continuare_FOREVER_2026-11-08.md`, `Prompt_continuare_EN_2026-11-08.txt` |
| Rule, hashes | `Regula_de_decizie.md`, `SHA256SUMS_2026-11-06.txt` | `Regula_de_decizie_2026-11-08.md`, `SHA256SUMS_2026-11-08.txt` |
| Participants | Deep Review (Argon 4, Extra High depth, High thinking); ChatGPT (GPT-6, High effort); Gemini (3.1 Pro, High thinking); Copilot (Think Deeper); Mistral Large 4 (API, reasoning effort high, temperature 0.3) | ChatGPT (GPT-6, High effort); Gemini (3.1 Pro, High thinking); Mistral Le Chat (Think mode; the exact model is not shown in a free account). Copilot did not take part: it had already seen the plan under discussion |
| Witness (no vote) | DeepSeek (deep thinking) | DeepSeek (deep thinking, with web search) |
| Answers | `Raspunsuri/` | `Raspunsuri/2026-11-08_continuare/` |
| Verification | `Verificare_raspunsuri_2026-11-06.md` | `Verificare_raspunsuri_2026-11-08.md` |
| Checking the hashes | `sha256sum -c SHA256SUMS_2026-11-06.txt` here, and `sha256sum -c SHA256SUMS.txt` in `Raspunsuri/`: all OK | `SHA256SUMS_2026-11-08.txt` was written as the colloquium went, with paths relative to more than one folder. The answers are in `Raspunsuri/2026-11-08_continuare/`. `mesaj_concatenat(prompt+dosar)` is the hash of the message sent (prompt followed by dossier), not a file. The first two entries for `Verificare_raspunsuri_2026-11-08.md` are earlier drafts of that document; its last entry matches the archived file |
| Outcome | **Direction C**: close the line of parameter clocks, write a closure report and a note on FOREVER, and run one decisive test for each remaining exception (4 votes left after verification, against 1 for B; the witness also chose C). Tests proposed by at least two participants, preregistered and run: T-A, T-B, T-C, T-D | **Analysis (d) and stage 1 of (a)** (3 votes of 3; the witness agreed): a zero-GPU analysis on the same trajectory, then repeated runs from common starting points under a rule fixed beforehand (preregistration v3) |

---

# Despre acest folder: colocviile de direcție ale Pilot 2 (6 și 8 noiembrie 2026)

*Parte din registrul deciziilor.*

Folderul arată cum s-au luat cele două decizii mari de direcție ale Pilot 2. Spre deosebire de evaluările ciornelor de
protocol din `../Recenzii/`, care sunt o anexă informativă, răspunsurile de aici **au stat la baza deciziilor**:
direcția a fost stabilită aplicând o regulă fixată dinainte răspunsurilor verificate. Pentru fiecare colocviu, folderul
păstrează dosarul și promptul trimise, regula de decizie, amprentele notate înainte de citirea primului răspuns,
răspunsurile așa cum au venit, verificarea punct cu punct și rezultatul.

Cum s-a lucrat: autorul, care nu e specialist în învățare automată, a ales să nu ia singur deciziile mari de direcție.
Pentru fiecare, dosarul și regula au fost scrise și amprentate înainte de orice răspuns. Fiecare sistem AI a primit,
separat, același dosar și același prompt, fără să vadă celelalte răspunsuri. Fiecare cifră, afirmație despre cod și
referință a fost verificată; o recomandare sprijinită pe o afirmație falsă a fost eliminată. Direcția a fost opțiunea
cu cele mai multe recomandări rămase. Autorul a păstrat dreptul de a opri sau de a amâna, nu de a alege între opțiuni.
Asistentul AI care a scris analizele și a pregătit dosarele (Claude, Anthropic, în Claude Code) nu a votat: a verificat
răspunsurile și a aplicat regula. Un martor fără vot (DeepSeek), adăugat după fixarea regulii, a răspuns la același
dosar. O limită a metodei: dosarele au fost pregătite, iar răspunsurile verificate, de același asistent care a făcut
analizele; erorile din dosare au fost scoase la iveală în mare parte de participanți (o omisiune din dosarul din
8 noiembrie i-a dus pe toți la aceeași explicație greșită) și sunt listate în documentele de verificare.

Răspunsurile sunt texte produse de sisteme AI, păstrate exact cum au venit, și nu exprimă opiniile autorului. Conțin
erori, marcate în verificări. Concluziile studiului se sprijină pe testele preînregistrate alese de colocvii, raportate
în raportul de închidere, nu pe răspunsurile în sine. Indexul de mai sus dă fișierele fiecărui colocviu. În copia
publică a fișierului `Raspunsuri/_proveniență.md`, două linkuri către conversațiile private ale autorului sunt înlocuite
cu „[link privat, omis]”; restul fișierului e neschimbat.
