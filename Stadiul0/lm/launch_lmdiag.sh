#!/bin/bash
# Diagnostic (6 Nov 2026): current-task accuracy just before the final replay, on two runs already done (training must be
# bit-identical: steps sha256 compared with lmtech2/s7201 and lmtech1/s7101). Stops if runs/_HW_STOP exists.
PY=/d/Time/_venv_cuda/Scripts/python.exe
for spec in "7201 256 ../runs/lmtech2/s7201" "7101 512 ../runs/lmtech1/s7101"; do
  set -- $spec
  if [ -f ../runs/_HW_STOP ]; then echo "OPRIT de paznic: $(cat ../runs/_HW_STOP)"; exit 3; fi
  "$PY" -I lm_forever_run.py --seed $1 --per_task $2 --diag_pre_final --out ../runs/lmdiag/s$1_$2 2>&1 | grep -E --line-buffered "^(task|done)|Error|Traceback"
  "$PY" -I -c "
import json
a = json.load(open('$3/meta.json')); b = json.load(open('../runs/lmdiag/s$1_$2/meta.json'))
print('antrenare identica:', a['sha256_steps_data'] == b['sha256_steps_data'], '| factori identici:', a['sha256_final_factors'] == b['sha256_final_factors'])
print('acuratete inainte de repetitia finala:', [round(x[1], 3) for x in b['diag_pre_final']])
"
done
echo "LMDIAG TERMINAT"
