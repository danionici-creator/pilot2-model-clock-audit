#!/usr/bin/env bash
# Night of 6-7 Nov 2026: decisive tests T-A (GPU) and T-B (CPU) in parallel; preregistration: preinregistrare_TA_TB_2026-11-06.md
# Run from Stadiul0. Each part stops starting new runs if runs/_HW_STOP exists (hardware watchdog).
cd "$(dirname "$0")"
LOG=runs/noapte_TA_TB.log
PY=/d/Time/_venv_cuda/Scripts/python.exe
export CUBLAS_WORKSPACE_CONFIG=:4096:8

part_TA() {
  for seed in 7301 7302 7303 7304 7305; do
    for clk in tau eta_m eta steps; do
      [ -e runs/_HW_STOP ] && { echo "TA oprit de paznic $(date +%H:%M)" >> $LOG; return; }
      echo "TA start seed $seed clock $clk $(date +%H:%M:%S)" >> $LOG
      (cd lm && $PY lm_forever_run.py --seed $seed --clock $clk --precision bf16 --diag_pre_final --diag_pre_final_all \
          --out ../runs/ta/$clk/s$seed) 2>&1 | tail -1 >> $LOG
    done
  done
  echo "TA TERMINAT $(date +%H:%M:%S)" >> $LOG
}

part_TB() {
  for spec in "F6:0.3:tb_F6_n03" "F6:0.0:tb_F6_n00" "F6:0.5:tb_F6_n05" "F6:0.1:tb_F6_n01" "F1:none:tb_F1"; do
    IFS=: read fam noise tag <<< "$spec"
    [ -e runs/_HW_STOP ] && { echo "TB oprit de paznic $(date +%H:%M)" >> $LOG; return; }
    RUNS=""; for s in 9101 9102 9103 9104 9105 9106 9107 9108; do RUNS="$RUNS $fam:$s"; done
    SET=""; [ "$noise" != "none" ] && SET="--set families.F6.label_noise=$noise"
    echo "TB start $tag $(date +%H:%M:%S)" >> $LOG
    python launch.py --runs $RUNS --tag $tag --workers 4 --pin-pcores $SET > runs/${tag}_launch.log 2>&1
    echo "TB end $tag rc=$? $(date +%H:%M:%S)" >> $LOG
  done
  echo "TB TERMINAT $(date +%H:%M:%S)" >> $LOG
}

echo "NOAPTE start $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
part_TA &
part_TB &
wait
echo "NOAPTE TERMINAT $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
