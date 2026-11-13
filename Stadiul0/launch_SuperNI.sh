#!/usr/bin/env bash
# SuperNI check (7 Nov 2026), preregistration: preinregistrare_SuperNI_2026-11-07.md. Order: S1 (tau, 3 seeds), then S2 (eta_m).
cd "$(dirname "$0")"
LOG=runs/sni_launch.log
PY=/d/Time/_venv_cuda/Scripts/python.exe
export CUBLAS_WORKSPACE_CONFIG=:4096:8
echo "SNI start $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
for clk in tau eta_m; do
  for seed in 7401 7402 7403; do
    [ -e runs/_HW_STOP ] && { echo "oprit de paznic $(date +%H:%M)" >> $LOG; exit 0; }
    echo "start $clk $seed $(date +%H:%M:%S)" >> $LOG
    (cd lm && $PY lm_superni_run.py --seed $seed --clock $clk --grad_ckpt --diag_pre_final_all --out ../runs/sni/$clk/s$seed) 2>&1 | grep -E "^task|^done" >> $LOG
  done
  echo "gata $clk $(date +%H:%M:%S)" >> $LOG
done
echo "SNI TERMINAT $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
