# Preregistered analysis of the repeated runs (preinregistrare_FOREVER_repetari_2026-11-08.md), fixed BEFORE any of them ran.
# Reads runs/forever_repro_eval_<arm>.log (written by eval_repro.sh). Exit 10 = preregistered early stop after stage 1.
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RUNS = Path(__file__).resolve().parent.parent / "runs"
ARMS = {("tau", "A", 1): "tau", ("eta", "B", 1): "eta_m", ("eta", "A", 1): "eta_m_A1", ("tau", "B", 1): "tau_B1",
        ("tau", "A", 2): "tau_A2", ("eta", "A", 2): "eta_m_A2"}
MARGIN = 2.0  # points


def parse(arm):
    p = RUNS / f"forever_repro_eval_{arm}.log"
    if not p.exists():
        return None
    s = p.read_text(encoding="utf-8")
    acc = {k: 100 * float(v) for k, v in re.findall(r"任务 (\w+) 的 accuracy：([0-9.]+)", s)}
    op = re.search(r"average Performance \(mean accuracy\) is ([0-9.]+)", s)
    bwt = re.search(r"^BWT is (-?[0-9.]+)", s, re.M)
    if len(acc) != 4 or not op or not bwt:
        sys.exit(f"eval log incomplete: {p}")
    return {"dbpedia": acc["dbpedia"], "OP": 100 * float(op.group(1)), "BWT": 100 * float(bwt.group(1)), "per_task": acc}


R = {k: parse(a) for k, a in ARMS.items()}


def diff(metric, a, r):
    t, e = R[("tau", a, r)], R[("eta", a, r)]
    return None if t is None or e is None else t[metric] - e[metric]


out = {"arms": {ARMS[k]: v for k, v in R.items() if v is not None}}
D = {f"{a}{r}": diff("dbpedia", a, r) for a, r in [("A", 1), ("B", 1), ("A", 2)]}
out["D_dbpedia_tau_minus_eta"] = D
for m in ("OP", "BWT"):
    out[f"paired_{m}_tau_minus_eta"] = {f"{a}{r}": diff(m, a, r) for a, r in [("A", 1), ("B", 1), ("A", 2)]}
if R[("tau", "B", 1)] and R[("eta", "A", 1)]:
    out["adapter_effect_A_minus_B"] = {"tau": R[("tau", "A", 1)]["dbpedia"] - R[("tau", "B", 1)]["dbpedia"],
                                       "eta": R[("eta", "A", 1)]["dbpedia"] - R[("eta", "B", 1)]["dbpedia"]}
code = 0
if D["A1"] is None or D["B1"] is None:
    verdict = "etapa 1 incompleta: fara verdict"
elif D["A2"] is None:
    if D["A1"] * D["B1"] < 0:
        verdict = "NU SE POATE ATRIBUI CEASULUI (semne opuse dupa etapa 1; oprire timpurie)"
        code = 10
    else:
        verdict = "etapa 1: semne la fel, continua cu etapa 2"
else:
    Dv = [D["A1"], D["B1"], D["A2"]]
    mean = sum(Dv) / 3
    N = max(abs(R[("tau", "A", 1)]["dbpedia"] - R[("tau", "A", 2)]["dbpedia"]),
            abs(R[("eta", "A", 1)]["dbpedia"] - R[("eta", "A", 2)]["dbpedia"]))
    out["mean_D"], out["noise_N"] = mean, N
    if all(d > MARGIN for d in Dv) and mean > N:
        verdict = "EFECT AL CEASULUI: tau mai bun pe dbpedia"
    elif all(d < -MARGIN for d in Dv) and -mean > N:
        verdict = "EFECT AL CEASULUI: eta_m mai bun pe dbpedia"
    elif not (all(d > 0 for d in Dv) or all(d < 0 for d in Dv)) or abs(mean) <= MARGIN or abs(mean) <= N:
        verdict = "NU SE POATE ATRIBUI CEASULUI"
    else:
        verdict = "NEDECIS"
    for m in ("OP", "BWT"):
        vals = list(out[f"paired_{m}_tau_minus_eta"].values())
        mm = sum(vals) / len(vals)
        out[f"mean_paired_{m}"] = mm
        out[f"mean_paired_{m}_within_2"] = abs(mm) <= MARGIN
out["verdict"] = verdict
print(json.dumps(out, indent=1, ensure_ascii=False))
json.dump(out, open(RUNS / "forever_repetari_verdict.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
sys.exit(code)
