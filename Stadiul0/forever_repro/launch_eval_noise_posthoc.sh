#!/usr/bin/env bash
# POST HOC test (a), 9 Nov 2026: evaluation noise of the four final adapters of stage 1 (eval_noise_posthoc.py).
# Order: seed 1 for the four cells, then greedy for the four, then seed 2 for the four (12 evaluations), so that a
# stop leaves complete rounds. Each evaluation is scored with the authors' unchanged eval_avgPerf_longsequence.py
# (exact match), as in eval_repro.sh. Checks runs/_HW_STOP before each evaluation. Then eval_noise_summary.py (CPU).
# Usage: bash launch_eval_noise_posthoc.sh
cd "$(dirname "$0")"
export PYTHONPATH=. FOREVER_CACHE=D:/Time/_date/hf_cache HF_HUB_OFFLINE=1 PYTHONIOENCODING=utf-8 FOREVER_DATA=data_longsequence
V=/d/Time/_venv_forever/Scripts/python.exe
N=Qwen_Qwen3-0.6Blora_cl_dataset_id_4
LOG=../runs/forever_eval_noise_posthoc.log
mkdir -p logs
echo "EVAL NOISE (post hoc) start $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
for mode in seed1 greedy seed2; do
  for arm in tau eta_m eta_m_A1 tau_B1; do
    [ -e ../runs/_HW_STOP ] && { echo "oprit de paznic $(date '+%H:%M:%S')" >> $LOG; exit 0; }
    echo "$arm $mode gen start $(date '+%H:%M:%S')" >> $LOG
    $V eval_noise_posthoc.py $arm $mode > logs/eval_noise_${arm}_${mode}.log 2>&1
    rc=$?; echo "$arm $mode gen rc=$rc $(date '+%H:%M:%S')" >> $LOG
    [ $rc -eq 3 ] && { echo "oprit de paznic $(date '+%H:%M:%S')" >> $LOG; exit 0; }
    [ $rc -ne 0 ] && { echo "OPRIT: generarea $arm $mode a esuat" >> $LOG; exit 1; }
    ( cd src && PYTHONPATH="..;." $V eval_avgPerf_longsequence.py --dataset_id 4 \
        --test_data_name _eval_noise_posthoc/${arm}_${mode}/${N}_avgPerf | grep -vE '^[0-9]+$' ) \
        > ../runs/forever_eval_noise_posthoc_${arm}_${mode}.log 2>&1
    rc=$?; echo "$arm $mode score rc=$rc $(date '+%H:%M:%S')" >> $LOG
  done
done
python -I eval_noise_summary.py > ../runs/forever_eval_noise_posthoc_summary.log 2>&1
echo "summary rc=$? $(date '+%H:%M:%S')" >> $LOG
echo "EVAL NOISE (post hoc) TERMINAT $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
