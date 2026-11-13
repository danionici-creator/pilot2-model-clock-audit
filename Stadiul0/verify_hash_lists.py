# Checks every entry of the hash lists recorded before the runs (Stadiul0/runs/*_sha256.txt) against the files of this
# archive. Written on 9 Nov 2026 for the archive; it reads only. Usage, from the repository root:
#     python -I Stadiul0/verify_hash_lists.py
# Each entry gets one status:
#   ok           the file at its path has the recorded SHA-256
#   earlier      the file was changed after the list was written; the recorded version is in runs/earlier_versions/
#   authors      a file of the FOREVER authors (no licence, not redistributed): rebuild the working copy with
#                Stadiul0/forever_repro/prepare_forever_copy.py, which checks these hashes itself
#   external     an absolute path outside the study (the hash list of the authors' downloaded data)
#   lost         the recorded version was not kept (explained in runs/earlier_versions/README.md)
#   MISMATCH     none of the above: an error
# Only "ok" and "earlier" entries have their bytes checked here; "authors" entries are checked by prepare_forever_copy.py,
# while "external" and "lost" entries cannot be checked.
# Exit code 0 when no entry is MISMATCH, no line is malformed and every expected list is present with its entries.
# Corrected on 12 Nov 2026 after the independent audit of the archive (Recenzii/Audit_Codex_2026-11-10/, finding A02):
# a line that contains a SHA-256 but not in the expected form is now an error (it used to be skipped), the nine lists and
# their entry counts are checked against the inventory below, and the summary separates what was verified from what was
# only classified.
import hashlib, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent  # Stadiul0
RUNS = S / "runs"
EARLIER = RUNS / "earlier_versions"
BASE = {"forever_repro_sha256.txt": S / "forever_repro", "lmtech1_criterii_sha256.txt": S / "lm",
        "lmtech2_criterii_sha256.txt": S / "lm", "tc_criterii_sha256.txt": S / "lm"}  # all other lists: Stadiul0
AUTHORS = ("src/", "utils/", "templates/")
LOST = {
    "2d3f61013b9d": ("lm_forever_run.py of the runs lmtech1 and lmtech2", ["lmtech1", "lmtech2"]),
    "61d740185b23": ("td_audit.py v1 (unscaled OLS), replaced one minute later; output: runs/td_audit_v1_eroare_scalare.log", []),
}
# the hash lists written before the runs, with their number of entries (87 in all)
EXPECTED = {"forever_repro_sha256.txt": 39, "lant2_criterii_sha256.txt": 4, "lmtech1_criterii_sha256.txt": 4,
            "lmtech2_criterii_sha256.txt": 4, "preinregistrare_sha256.txt": 15, "preinregistrare_SuperNI_sha256.txt": 5,
            "tc_criterii_sha256.txt": 2, "td_criterii_sha256.txt": 3, "tech4_criterii_sha256.txt": 11}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    total, bad = {}, 0
    found = {L.name: L for L in sorted(RUNS.glob("*_sha256.txt"))}
    for name in sorted(set(EXPECTED) - set(found)):
        bad += 1
        print(f"  {name}: MISSING (expected {EXPECTED[name]} entries)")
    for name in sorted(set(found) - set(EXPECTED)):
        print(f"  {name}: not in the inventory of this script (checked anyway)")
    for L in found.values():
        base = BASE.get(L.name, S)
        counts = {}
        for line in L.read_text(encoding="utf-8").splitlines():
            m = re.match(r"([0-9a-f]{64}) \*(.+)$", line.strip())
            if not m:
                if re.search(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{64}(?![0-9A-Fa-f])", line):
                    st = "INVALID"
                    bad += 1
                    print(f"  {L.name}: malformed line with a SHA-256: {line.strip()[:100]}")
                    counts[st] = counts.get(st, 0) + 1
                    total[st] = total.get(st, 0) + 1
                continue  # timestamps and comments
            digest, rel = m.groups()
            p = base / rel
            if rel.startswith("/") or re.match(r"[A-Za-z]:", rel):
                st = "external"
            elif rel.startswith(AUTHORS) and base == S / "forever_repro":
                st = "authors"
            elif p.is_file() and sha(p) == digest:
                st = "ok"
            elif (EARLIER / digest[:12] / rel).is_file() and sha(EARLIER / digest[:12] / rel) == digest:
                st = "earlier"
            elif digest[:12] in LOST:
                what, run_dirs = LOST[digest[:12]]
                metas = [q for d in run_dirs for q in sorted((RUNS / d).glob("*/meta.json"))]
                same = [q for q in metas if json.loads(q.read_text(encoding="utf-8")).get("script_sha256") == digest]
                st = "lost"
                note = f"{what}" + (f"; SHA-256 also in script_sha256 of {len(same)} of {len(metas)} run meta.json files"
                                    if metas else "")
                print(f"  {L.name}: {rel} {digest[:12]} lost: {note}")
            else:
                st = "MISMATCH"
                bad += 1
                print(f"  {L.name}: {rel} {digest[:12]} MISMATCH")
            counts[st] = counts.get(st, 0) + 1
            total[st] = total.get(st, 0) + 1
        n = sum(v for k, v in counts.items() if k != "INVALID")
        if L.name in EXPECTED and n != EXPECTED[L.name]:
            bad += 1
            print(f"  {L.name}: {n} entries, expected {EXPECTED[L.name]}")
        print(f"{L.name}: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    print("\nall lists: " + ", ".join(f"{k} {v}" for k, v in sorted(total.items())))
    print(f"bytes verified here: {total.get('ok', 0) + total.get('earlier', 0)} (ok + earlier); authors' files: checked by "
          f"prepare_forever_copy.py ({total.get('authors', 0)}); not checkable: external {total.get('external', 0)}, "
          f"lost {total.get('lost', 0)}")
    print("no mismatch" if not bad else f"{bad} ERROR(S): MISMATCH, MISSING, INVALID or wrong count")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
