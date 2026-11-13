import json, re, math, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(r"D:\Time\02_Pilot2\Stadiul0")
# A02: malformed lines in hash lists
for L in sorted((S/"runs").glob("*_sha256.txt")):
    bad = [l for l in L.read_text(encoding="utf-8").splitlines() if l.strip() and not re.match(r"([0-9a-f]{64}) \*(.+)$", l.strip())]
    print(L.name, "non-matching lines:", len(bad), [b[:70] for b in bad][:5])
# A01: NaN / inf / empty containers in stored JSONs compared by reproduce_analyses
J = ["runs/ta_verdict.json","runs/tb_part1_verdict.json","runs/sni_verdict.json","runs/forever_repro_r2_reconstruction.json",
     "runs/forever_repetari_r2_eta_m.json","runs/forever_repetari_r2_eta_m_A1.json","runs/forever_d_same_trajectory.json",
     "runs/forever_repetari_verdict.json","runs/forever_eval_noise_posthoc.json","runs/ta_memory_posthoc.json"]
def walk(x, p=""):
    if isinstance(x, dict):
        if not x: yield p, "EMPTY{}"
        for k,v in x.items(): yield from walk(v, f"{p}/{k}")
    elif isinstance(x, list):
        if not x: yield p, "EMPTY[]"
        for i,v in enumerate(x): yield from walk(v, f"{p}[{i}]")
    elif isinstance(x, float) and not math.isfinite(x):
        yield p, repr(x)
for j in J:
    d = json.loads((S/j).read_text(encoding="utf-8"))
    odd = list(walk(d))
    print(j, "nonfinite/empty:", len(odd), odd[:6])
