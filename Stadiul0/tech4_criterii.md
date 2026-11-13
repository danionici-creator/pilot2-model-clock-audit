# Runda tehnică tech4: F1–F6 pe codul corectat după Deep Review (criterii fixate ÎNAINTE de rulare, 6 nov. 2026)

**Ce e:** pasul 2 din `02_Pilot2\Recenzii\Pilot2_v0.4_verificare_recenzie_DeepReview.md` §4 („rundă tehnică nouă, c_e-orbă”). Nepreînregistrată, ca tech1–tech3. **Orb față de relația c_e–T1:** nu se calculează nicio valoare incrementală a lui c_e și nicio relație între c_e și uitare.

**Codul:** corecturile Deep Review aplicate pe 6 nov. (`Stadiul0_note_lucru.md` §14): `max_ctx` 4; embedding-urile scoase din weight decay (`wd_embeddings: false`, **provizoriu**, decizia (c) a autorului e deschisă; varianta recomandată); suprapunerea q_hist la începutul segmentului; L̄_A,clip și L̄_B,clip în evaluări; C10c și L_R(t₀); C0 ca ticuri de pauză; blocul D2 la 16 pași. Verificări: 27/27 (`runs\checks_latest.log`). Copiile codului de dinainte: `_work\_copii_siguranta\stadiul0_inainte_corecturi_DR_2026-11-06\`.

**Rulările:** F1–F6, sămânța 9005, rata 3e-4 (din configurație), 4 procese (referința de debit), mod ASUS Turbo, la priză, cu paznicul hardware pornit (`hw_watchdog.py`).

**Ce se măsoară (descriptiv, fără porți):**
1. copilăria după scoaterea embedding-urilor din weight decay: acuratețea de referință ≥ 0,95 în toate cele 6 (poarta existentă);
2. viteza uitării în F5 și F6 (cerută de recenzie): F_A și T1-acc pe ΔN, la intervale < 1.280, < 2.048 și fără plafon, și pe F^clip;
3. **debitul real în Turbo:** rulări pe oră la 4 procese, timpul pe componente (copilărie, antrenare, evaluări, fragmente), memoria maximă pe proces (blocul D2 la 16 adaugă ~70 MB);
4. temperaturile și limitarea de frecvență din jurnalul paznicului, pe toată durata.

**Validitate:** fiecare rulare se termină cu `meta.json` și amprentele; nicio oprire a paznicului.

**Estimarea de timp:** 6 rulări pe 4 procese = un val de 4 (~20–25 min; tech3 dădea 25 min înainte de Turbo, iar copilăria e acum de ~2 ori mai rapidă) și un val de 2 (~15–20 min, mai puțină concurență pe memorie). În total **~40–45 min**.
