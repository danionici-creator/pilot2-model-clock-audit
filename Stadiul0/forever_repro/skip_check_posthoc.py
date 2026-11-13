# POST HOC check (c), archived 9 Nov 2026: copy of Recenzii/Runda_finala_2026-11-09/Verificari_faza2/skip_check.py
# (sha256 d360afe8...cb44), written for the final review round. Only change: the folder argument defaults to this
# script's folder. Run from anywhere: python -I Stadiul0/forever_repro/skip_check_posthoc.py; output stored in
# Stadiul0/runs/forever_skip_check_posthoc.log (= Verificari_faza2/skip_check_output.txt).
# Verification aid (not an archive analysis): on steps with |dtheta| = 0, does the eta_m clock still advance?
import csv, sys
from pathlib import Path
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
for folder in ["ckpt_eta_m", "ckpt_eta_m_A1"]:
    for t in ["1-amazon", "2-yahoo", "3-agnews"]:
        rows = list(csv.DictReader(open(BASE / folder / "Qwen_Qwen3-0.6Blora_cl_dataset_id_4" / t / "drift_log.csv", encoding="utf-8")))
        steps = np.array([int(r["step"]) for r in rows])
        d = np.array([float(r["delta_t"]) for r in rows])
        clk = np.array([float(r["tau"]) for r in rows])
        inc = np.diff(np.concatenate([[0.0], clk]))
        z = d == 0
        cal = steps <= 24
        neg = (inc < 0).sum()
        print(f"{folder:14s} {t:9s} rows {len(rows):3d} steps {steps.min()}-{steps.max()} | dtheta=0 at steps {list(steps[z])}"
              f" | clock inc on those: {[f'{x:.2e}' for x in inc[z]]} | share of clock from dtheta=0 steps: cal {inc[z&cal].sum()/inc[cal].sum():.3f}, rest {inc[z&~cal].sum()/inc[~cal].sum():.3f} | negative incs {neg}")
