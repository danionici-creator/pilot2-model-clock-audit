#!/usr/bin/env bash
# Preregistered evaluation of one variant with THEIR unchanged scripts (preinregistrare_FOREVER_repro_2026-11-07.md).
# Usage: bash eval_repro.sh <tau|eta_m>. Their scripts read ../output/<name> and ../data_longsequence/test, so they run from src/.
# Lines that are only a sample index (their script prints one per example) are filtered out of the log.
cd "$(dirname "$0")/src"
V=/d/Time/_venv_forever/Scripts/python.exe
v=$1; N=Qwen_Qwen3-0.6Blora_cl_dataset_id_4
OUT=../../runs/forever_repro_eval_$v.log
export PYTHONPATH="..;." PYTHONIOENCODING=utf-8
{
  echo "=== eval $v $(date '+%Y-%m-%d %H:%M:%S')"
  echo "--- OP (eval_avgPerf_longsequence.py, exact match)"
  $V eval_avgPerf_longsequence.py --dataset_id 4 --test_data_name $v/${N}_avgPerf | grep -vE '^[0-9]+$'
  echo "--- BWT (eval_bwt_longsequence.py, lenient label extraction)"
  $V eval_bwt_longsequence.py --dataset_id 4 --test_data_name $v/${N}_bwt --test_data_name2 $v/${N}_avgPerf
  echo "--- OP with the lenient extraction of their BWT script (all 4 tasks)"
  $V ../lenient_op.py $v/${N}_avgPerf
} > $OUT 2>&1
echo "eval $v done: $OUT"
