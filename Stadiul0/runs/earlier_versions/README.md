# Earlier versions of files named in the hash lists

Written on 9 Nov 2026, for the archive. Each hash list in `Stadiul0/runs/*_sha256.txt` records the SHA-256 of files as
they were before the runs it governs. Some of these files were changed afterwards, for a later test, and the archive
keeps their current version at the original path. This folder holds the earlier versions: one subfolder per SHA-256
(its first 12 hex digits), with the file under the path written in the list. To check every entry of every list, run
from the repository root:

```
python -I Stadiul0/verify_hash_lists.py
```

Every file below has exactly the SHA-256 recorded in the list. "Safety copy" means a copy the author kept on the laptop
before the change. "Reconstructed" means the file was rebuilt on 9 Nov 2026 by undoing the documented change in the
current version. Its identity with the original is proved by the recorded SHA-256, not assumed.

## Versions used by runs (5)

| SHA-256 (12) | File | Hash list (runs it governs) | Why it changed afterwards | Source |
|---|---|---|---|---|
| `2317e3d4a22b` | `p2/run.py` | `tech4_criterii` (tech4 round, 6 Nov, 17:38) | before T-B: the same-cost competitors C10p and C10h were added; training is unchanged bit for bit (`runs/tech4_g7_TB`) | safety copy |
| `2b51243ebf11` | `p2/triplets.py` | `tech4_criterii` | the same change | safety copy |
| `e2894fda6abc` | `launch.py` | `tech4_criterii` | the option `--pin-pcores` was added later on 6 Nov (results are bit-identical with or without it: `pin_test.py`) | reconstructed (option removed) |
| `c442092a5bab` | `launch_weekend_1.sh` | `tech4_criterii` | with the flag `-I`, `p2` could not be imported and tech4 did not start (`runs/lant1_launch.log`, 18:00:30); at 18:01 the flag was removed here, and tech4 was started with `launch_tech4.sh`, the same command without `-I` (that script has no entry in the list; `runs/tech4_launch.log`, 18:01:07) | reconstructed (flag restored) |
| `ed5b3d733737` | `lm/lm_forever_run.py` | `lant2_criterii` (runs `lmsens_bf16`, `lmsens_a32`) | before T-A: the option `--clock` was added; the τ variant is identical bit for bit with this version (`runs/ta_smoke2`) | safety copy |

## Versions superseded before any run (6)

| SHA-256 (12) | File | Hash list | What replaced it | Source |
|---|---|---|---|---|
| `986859770f78` | `preinregistrare_FOREVER_repetari_2026-11-08.md` (v1) | `forever_repro_sha256` | v2, with the verified observations of one AI reviewer | safety copy |
| `48cda21caa55` | the same file (v2) | `forever_repro_sha256` | v2 with the two times in its heading corrected (~14:30 → 13:43, ~15:15 → 13:58) | reconstructed |
| `ffb115c2a00a` | the same file (v2, times corrected) | `forever_repro_sha256` | v3, after the short colloquium of 8 Nov (the version that governs stage 1) | safety copy |
| `4471989f5a61` | `rep_verdict.py` (v1) | `forever_repro_sha256` | v2 | safety copy |
| `968cca94fc45` | `rep_verdict.py` (v2) | `forever_repro_sha256` | v3 (the version that ran) | safety copy |
| `76266d79022f` | `preinregistrare_FOREVER_repro_addendum_2026-11-07.md` | `forever_repro_sha256` | the same text, with the time in its heading corrected (~18:35 → ~18:25) seven seconds later | reconstructed |

## Not preserved (2)

- `2d3f61013b9d`, `lm/lm_forever_run.py`: the version used by the runs `lmtech1` and `lmtech2` (6 Nov), named in
  `lmtech1_criterii_sha256.txt` and `lmtech2_criterii_sha256.txt`. The next version (`ed5b3d733737`, above) adds the
  options `--precision` and `--diag_pre_final`, as the configurations stored in the runs' `meta.json` show. The file
  itself was not kept. Its SHA-256 is also stored as `script_sha256` in the `meta.json` of each of the six runs, and
  `verify_hash_lists.py` checks this. The analyses of these runs use only their stored results, and they reproduce.
- `61d740185b23`, `td_audit.py` v1: it used unscaled OLS, which was ill-conditioned. It was replaced one minute later by v2,
  the current file, before the T-D reading. The output of v1 is kept as `runs/td_audit_v1_eroare_scalare.log`.
