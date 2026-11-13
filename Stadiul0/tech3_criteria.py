"""Criteria of the tech3 round (Stadiul0_note_lucru.md, section 5c), fixed before the runs. No c_e quantity is read.

    python tech3_criteria.py runs/tech3_lr2e-4 runs/tech3_lr3e-4
"""
import sys
import numpy as np
import pandas as pd
from pathlib import Path


def reweight(d):
    d = d.copy(); E = d.ep.nunique(); M = d.groupby("ep").ep.transform("size"); d["w"] = 1.0 / (E * M); return d


def wavg(x, w):
    return float((w * x).sum() / w.sum())


for tag in map(Path, sys.argv[1:]):
    runs = []
    for rd in sorted(p for p in tag.iterdir() if (p / "triplets.parquet").exists()):
        df = pd.read_parquet(rd / "triplets.parquet", columns=["ep", "dN", "F_A", "F_B", "dAcc_A", "incl", "family"])
        df = df[df.incl]
        runs.append(reweight(df))
    pooled = pd.concat(runs, ignore_index=True)
    dNstar = None
    for lo in range(256, 20480, 256):
        b = pooled[(pooled.dN >= lo) & (pooled.dN < lo + 256)]
        if len(b) >= 10 and wavg(b.dAcc_A.values, b.w.values) >= 0.90:
            dNstar = lo; break
    print(f"== {tag.name}: dN* = {dNstar}")
    tot = 0
    for d in runs:
        n_un = int((d.dN < dNstar).sum()) if dNstar else len(d); tot += n_un
        print(f"   {d.family.iloc[0]}: episoade valide {d.ep.nunique()}, tripleti {len(d)}, sub dN* {n_un}")
    print(f"   total tripleti sub dN*: {tot}")
    bins = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 1e9]
    pooled["b"] = pd.cut(pooled.dN, bins, right=False)
    print(pooled.groupby("b", observed=True).apply(lambda g: pd.Series({"n": len(g), "F_A": wavg(g.F_A.values, g.w.values),
          "dAcc": wavg(g.dAcc_A.values, g.w.values)}), include_groups=False).round(2).T.to_string())
