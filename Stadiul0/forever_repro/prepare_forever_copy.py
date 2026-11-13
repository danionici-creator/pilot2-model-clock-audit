# Rebuilds, byte for byte, the FOREVER working copy used in Pilot 2 (runs R1, R2 and the repeated runs).
#
# The FOREVER repository (https://github.com/WoodScene/FOREVER) has no licence, so none of its files are
# redistributed in this archive. Get them yourself:
#     git clone https://github.com/WoodScene/FOREVER
#     cd FOREVER && git checkout bbeb549a21e59d9490f20a2b02099ee766a67f48
# then, from this folder (Stadiul0/forever_repro):
#     python -I prepare_forever_copy.py <path-to-FOREVER-checkout>
#
# What it does:
#  1. checks the 15 source files it needs against the SHA-256 of commit bbeb549 (recorded on 7 Nov 2026);
#  2. copies 8 of them unchanged (utils/, templates/, the two evaluation scripts) and the data_longsequence/ split;
#  3. applies the three documented adaptations (preregistration of 7 Nov 2026, adaptations 1-2): the local model
#     cache path in finetune_cl_our_qwen.py and the test-data path in the two generators (the originals hard-code
#     ../data_superni). On the laptop these files were saved with CRLF line endings; the script writes them the same way;
#  4. builds the clock-swap variant src/finetune_cl_our_qwen_clock.py with make_clock_variant.py (unchanged);
#  5. checks every resulting file against the SHA-256 recorded BEFORE the runs (../runs/forever_repro_sha256.txt).
# It never overwrites an existing file: run it in a folder without src/, utils/, templates/, data_longsequence/.
import hashlib, runpy, shutil, sys
from pathlib import Path

COMMIT = "bbeb549a21e59d9490f20a2b02099ee766a67f48"
ORIGINAL = {  # sha256 of the authors' files at COMMIT
    "src/eval_avgPerf_longsequence.py": "688feacb548b1ac8b7f016d3c751faa940851a6aaf372b40988004b317e40383",
    "src/eval_bwt_longsequence.py": "ba87a2d9137b685d9c16f166baf427ec58b9b5b41820b8a57a00d94c66c2e86c",
    "src/finetune_cl_our_qwen.py": "908f32db42264b3911d3a913a58c2807eba2f87e07a3848973e78422139b3e88",
    "src/generate_avgPerf.py": "4a850b554dea6ffa6f60eb8e48a8f50d9fc9693e5e3b47290e9aeb283b3f4d45",
    "src/generate_bwt.py": "a30729581d5bb8a3deab481d0a3acc30d9321165fb4a027a25189e4a05904a79",
    "templates/alpaca.json": "75d04fb221d211d76cfed5040eeaac510d9ab60d013cbe90242106e3aa56dced",
    "utils/callbacks.py": "c7e5451b99f7d1da8cb4127787345632f8aa22d87e9a081e92d674cf1765df11",
    "utils/dataset_order.py": "b9a5ec55c7195b846a9b67bdbd4724ab6a53cca85a81cbde2c3439dc636d21d4",
    "utils/load_data.py": "df244882f4c71455fb448adec4fdb1569028530b8bf7a09a4581c43902b0e042",
    "utils/prompter.py": "47c07c99da5d220eac398ed03f4c6e785a77dfa814fd1cc2a5d143111eeb3447",
    "data_longsequence/dev/agnews.json": "9df54874d051c0802544c900b4276af541226e1e028bc2d21a57d7912e1212d2",
    "data_longsequence/dev/amazon.json": "f143517eb4037812c2ff38504252f9882d9e5d9a6bb502c04db329e34db61248",
    "data_longsequence/dev/dbpedia.json": "8691eaae453a9056ec535a6ab09cdf409da2563ee031c03db601670df5223996",
    "data_longsequence/dev/yahoo.json": "e81fa6cc35080f79aa7e1c5e94f4a87a3380fc08d249d398f73b6cdfdfdd35fd",
    "data_longsequence/test/agnews.json": "61a0dd7c61e8a5d7e80f6def6f476500eb3fc8ddbaf32e2d329f6ba1902e6257",
    "data_longsequence/test/amazon.json": "f2034a068f52269d5538e95a8872aa3dde1c8526bb25a88efc97f43ed0c003c8",
    "data_longsequence/test/dbpedia.json": "c50bf6abc18f2d67cfd21c6df5fa1e28d04422676591960f2f452139eb38c7fa",
    "data_longsequence/test/yahoo.json": "a5ec02d8ba65198a76f7d37d8cd02a7ff5d9b403592595bfb4cdd649d25e7898",
    "data_longsequence/train/agnews.json": "207e04812008d287d2e818cb7e0873710b39d9d7acc3e0b32567b0146c301c9d",
    "data_longsequence/train/amazon.json": "c51b01bf775609d3947282dc94c3c83c5e28149acb3509d9c535bf511b130947",
    "data_longsequence/train/dbpedia.json": "c3e8a5a52e1748c8f1041ad69e93d723ccd29c77b2c206761306560a116756f1",
    "data_longsequence/train/yahoo.json": "74c38780a0b39dc80cc12f2eb9c5eab64ea9b932461d486798968a6747e8d040",
}
RECORDED = {  # sha256 of the working copy, recorded before the runs (../runs/forever_repro_sha256.txt)
    "src/eval_avgPerf_longsequence.py": "688feacb548b1ac8b7f016d3c751faa940851a6aaf372b40988004b317e40383",
    "src/eval_bwt_longsequence.py": "ba87a2d9137b685d9c16f166baf427ec58b9b5b41820b8a57a00d94c66c2e86c",
    "src/finetune_cl_our_qwen.py": "4590692c921e800ddd2401e5298235b3576655f2cb7d8a3917aa7eaf675a3918",
    "src/finetune_cl_our_qwen_clock.py": "86c3313197a7658bcc341979ac3bb9f422df2f9fbc4eb9a4a990a8a3fd487161",
    "src/generate_avgPerf.py": "f4bbbab0a8965df25cec80df3812ba0c6a5d8e8a6ea3fce7c617092c35fffe0d",
    "src/generate_bwt.py": "311f12514e64ef4877bf82b7b24462b203e2e656a33d0f9a6dce62828babbac3",
    "utils/callbacks.py": "c7e5451b99f7d1da8cb4127787345632f8aa22d87e9a081e92d674cf1765df11",
    "utils/dataset_order.py": "b9a5ec55c7195b846a9b67bdbd4724ab6a53cca85a81cbde2c3439dc636d21d4",
    "utils/load_data.py": "df244882f4c71455fb448adec4fdb1569028530b8bf7a09a4581c43902b0e042",
    "utils/prompter.py": "47c07c99da5d220eac398ed03f4c6e785a77dfa814fd1cc2a5d143111eeb3447",
    "templates/alpaca.json": "75d04fb221d211d76cfed5040eeaac510d9ab60d013cbe90242106e3aa56dced",
}
ADAPT = {  # file -> [(original line, adapted line)]; each original line must occur exactly once
    "src/finetune_cl_our_qwen.py": [
        ("os.environ['TRANSFORMERS_CACHE'] = '/workspace/CL_Memory/cache'",
         "os.environ['TRANSFORMERS_CACHE'] = os.environ.get('FOREVER_CACHE', 'D:/Time/_date/hf_cache')  # adaptation: local cache (Windows)"),
        ("AutoConfig.default_cache_dir = '/workspace/CL_Memory/cache'",
         "AutoConfig.default_cache_dir = os.environ.get('FOREVER_CACHE', 'D:/Time/_date/hf_cache')  # adaptation"),
    ],
    "src/generate_avgPerf.py": [
        ('        testfile_name = "../data_superni/test/" + dataset_order[service_id] + ".json"',
         '        testfile_name = os.path.join(os.environ.get("FOREVER_DATA", "../data_superni"), "test", dataset_order[service_id] + ".json")  # adaptation: the original hard-codes data_superni'),
    ],
    "src/generate_bwt.py": [
        ('    testfile_name = "../data_superni/test/" + dataset_order[service_id] + ".json"',
         '    testfile_name = os.path.join(os.environ.get("FOREVER_DATA", "../data_superni"), "test", dataset_order[service_id] + ".json")  # adaptation: the original hard-codes data_superni'),
    ],
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__ or "usage: python -I prepare_forever_copy.py <path-to-FOREVER-checkout>")
    src_root = Path(sys.argv[1]).resolve()
    here = Path(__file__).resolve().parent
    bad = [f for f, h in ORIGINAL.items() if not (src_root / f).is_file() or sha(src_root / f) != h]
    if bad:
        sys.exit(f"not the files of commit {COMMIT}: " + ", ".join(bad))
    out = [here / f for f in list(RECORDED) + [f for f in ORIGINAL if f.startswith("data_")]]
    clash = [str(p) for p in out if p.exists()]
    if clash:
        sys.exit("refusing to overwrite existing files: " + ", ".join(clash[:5]))
    for f in ORIGINAL:
        if f not in ADAPT:
            (here / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src_root / f, here / f)
    for f, pairs in ADAPT.items():
        s = (src_root / f).read_bytes().decode("utf-8")
        for old, new in pairs:
            assert s.count(old) == 1, (f, old)
            s = s.replace(old, new)
        (here / f).parent.mkdir(parents=True, exist_ok=True)
        (here / f).write_bytes(s.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8"))
    # clock-swap variant, built by the unchanged script that built it on 7 Nov 2026 (it reads and writes in text mode,
    # which on Windows gives CRLF; normalise so the result is the same on any system)
    import os
    cwd = os.getcwd()
    os.chdir(here)
    try:
        runpy.run_path(str(here / "make_clock_variant.py"), run_name="__main__")
    finally:
        os.chdir(cwd)
    clock = here / "src/finetune_cl_our_qwen_clock.py"
    clock.write_bytes(clock.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    wrong = [f for f, h in RECORDED.items() if sha(here / f) != h]
    if wrong:
        sys.exit("MISMATCH with the hashes recorded before the runs: " + ", ".join(wrong))
    print(f"ok: {len(RECORDED)} code files identical to the recorded working copy; "
          f"{sum(f.startswith('data_') for f in ORIGINAL)} data files copied unchanged")


if __name__ == "__main__":
    main()
