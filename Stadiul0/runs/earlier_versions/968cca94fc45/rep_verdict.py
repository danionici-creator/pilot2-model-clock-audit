# Preregistered analysis of the repeated runs (preinregistrare_FOREVER_repetari_2026-11-08.md, version 2),
# fixed BEFORE any of them ran. Reads runs/forever_repro_eval_<arm>.log (written by eval_repro.sh) and
# logs/<arm>_train_t<k>.log (trigger table, descriptive). Exit 10 = preregistered early stop after stage 1.
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "runs"
ARMS = {("tau", "A", 1): "tau", ("eta", "B", 1): "eta_m", ("eta", "A", 1): "eta_m_A1", ("tau", "B", 1): "tau_B1",
        ("tau", "A", 2): "tau_A2", ("eta", "A", 2): "eta_m_A2"}
PAIRS = [("A", 1), ("B", 1), ("A", 2)]
MARGIN = 2.0  # points
NOT_ATTR = "NU SE POATE ATRIBUI CEASULUI (datele nu sustin o atribuire stabila a diferentei catre ceas; nu inseamna ca ceasul nu are efect)"


def parse(arm):
    p = RUNS / f"forever_repro_eval_{arm}.log"
    if not p.exists():
        return None
    s = p.read_text(encoding="utf-8")
    acc = {k: 100 * float(v) for k, v in re.findall(r"任务 (\w+) 的 accuracy：([0-9.]+)", s)}
    op = re.search(r"average Performance \(mean accuracy\) is ([0-9.]+)", s)
    bwt = re.search(r"^BWT is (-?[0-9.]+)", s, re.M)
    dl = re.search(r"BWT diff list: \[([^\]]+)\]", s)
    if len(acc) != 4 or not op or not bwt or not dl:
        sys.exit(f"eval log incomplete: {p}")
    return {"dbpedia": acc["dbpedia"], "OP": 100 * float(op.group(1)), "BWT": 100 * float(bwt.group(1)),
            "dbpedia_forgetting": 100 * float(dl.group(1).split(",")[0]), "per_task": acc}


def triggers(arm):
    """Per task: list of clock-triggered replays (step, threshold, clock value), from the training logs."""
    res = {}
    for t in (1, 2, 3):
        p = HERE / "logs" / f"{arm}_train_t{t}.log"
        if not p.exists():
            continue
        lines = p.read_text(encoding="utf-8", errors="replace").replace("\r", "\n").split("\n")
        total = None
        for l in lines:
            m = re.search(r"steps_done\(before\)=\d+/(\d+)", l)
            if m:
                total = int(m.group(1)); break
        trig, pending = [], None
        for l in lines:
            m = re.search(r"MEMORY REPLAY \(immediate\), trigger_threshold=([0-9.eE+-]+), tau=([0-9.eE+-]+)", l)
            if m:
                if pending is not None:
                    trig.append(pending)
                pending = {"threshold": float(m.group(1)), "clock": float(m.group(2)), "step": None}
                continue
            m = re.search(r"CONTINUE CURRENT, remaining_steps=(\d+)", l)
            if m and pending is not None and total is not None:
                pending["step"] = total - int(m.group(1)); trig.append(pending); pending = None
        if pending is not None:
            pending["step"] = total; trig.append(pending)
        res[t] = trig
    return res


R = {k: parse(a) for k, a in ARMS.items()}
T = {a: triggers(a) for a in ARMS.values()}


def diff(metric, a, r):
    t, e = R[("tau", a, r)], R[("eta", a, r)]
    return None if t is None or e is None else t[metric] - e[metric]


out = {"arms": {ARMS[k]: v for k, v in R.items() if v is not None}}
D = {f"{a}{r}": diff("dbpedia", a, r) for a, r in PAIRS}
out["D_dbpedia_tau_minus_eta"] = D
for m in ("OP", "BWT", "dbpedia_forgetting"):
    out[f"paired_{m}_tau_minus_eta"] = {f"{a}{r}": diff(m, a, r) for a, r in PAIRS}
out["triggers"] = {a: v for a, v in T.items() if v}
out["trigger_step_diff_eta_minus_tau"] = {}
for a, r in PAIRS:
    ta, ea = T[ARMS[("tau", a, r)]], T[ARMS[("eta", a, r)]]
    if ta and ea:
        out["trigger_step_diff_eta_minus_tau"][f"{a}{r}"] = {
            t: [e["step"] - x["step"] for x, e in zip(ta.get(t, []), ea.get(t, []))] for t in (1, 2, 3)}
if R[("tau", "B", 1)] and R[("eta", "A", 1)]:
    out["adapter_effect_A_minus_B"] = {"tau": R[("tau", "A", 1)]["dbpedia"] - R[("tau", "B", 1)]["dbpedia"],
                                       "eta": R[("eta", "A", 1)]["dbpedia"] - R[("eta", "B", 1)]["dbpedia"]}
for c in ("tau", "eta"):
    x1, x2 = R[(c, "A", 1)], R[(c, "A", 2)]
    if x1 and x2:
        out[f"N_{c}"] = abs(x1["dbpedia"] - x2["dbpedia"])
code = 0
if D["A1"] is None or D["B1"] is None:
    verdict = "etapa 1 incompleta: fara verdict"
elif D["A1"] * D["B1"] < 0:
    # preregistered early stop; the verdict stays this one even if stage 2 is later run descriptively
    verdict = NOT_ATTR + " [semne opuse dupa etapa 1; oprire timpurie]"
    code = 10 if D["A2"] is None else 0
elif D["A2"] is None:
    verdict = "etapa 1: semne la fel, continua cu etapa 2"
else:
    Dv = [D["A1"], D["B1"], D["A2"]]
    mean = sum(Dv) / 3
    N = max(out["N_tau"], out["N_eta"])
    out.update({"mean_D": mean, "min_D": min(Dv), "max_D": max(Dv), "noise_N": N})
    if all(d > MARGIN for d in Dv) and mean > N:
        verdict = "EFECT AL CEASULUI: tau mai bun pe dbpedia"
    elif all(d < -MARGIN for d in Dv) and -mean > N:
        verdict = "EFECT AL CEASULUI: eta_m mai bun pe dbpedia"
    elif not (all(d > 0 for d in Dv) or all(d < 0 for d in Dv)) or abs(mean) <= MARGIN or abs(mean) <= N:
        verdict = NOT_ATTR
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
