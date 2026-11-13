#!/bin/bash
# lmtech2: lmtech1 with 256 facts per task (learning criterion), seeds 7201-7203, in sequence on the GPU.
# Stops before a run if runs/_HW_STOP exists (hardware watchdog). Run from Stadiul0/lm:  bash launch_lmtech2.sh
PY=/d/Time/_venv_cuda/Scripts/python.exe
OUT=../runs/lmtech2
mkdir -p "$OUT"
for s in 7201 7202 7203; do
  if [ -f ../runs/_HW_STOP ]; then echo "OPRIT de paznic: $(cat ../runs/_HW_STOP)"; exit 3; fi
  "$PY" -I lm_forever_run.py --seed $s --per_task 256 --out "$OUT/s$s" 2>&1 | grep -E --line-buffered "^(seed|task|done|complete)|Error|error|Traceback"
done
echo "lmtech2 TERMINAT"
