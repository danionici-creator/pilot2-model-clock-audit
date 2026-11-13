#!/bin/bash
# Chain 2 (6 Nov 2026): pin test, G7 on tech4 F6, LM bf16 and alpha=32 sensitivities. See lant2_criterii.md.
cd /d/Time/02_Pilot2/Stadiul0
stop() { if [ -f runs/_HW_STOP ]; then echo "OPRIT de paznic: $(cat runs/_HW_STOP)"; exit 3; fi; }
stop; date "+pin start %H:%M:%S"; python pin_test.py; date "+pin end %H:%M:%S"
stop; date "+g7 start %H:%M:%S"
python launch.py --runs F6:9005 --workers 1 --tag tech4_g7 2>&1 | grep -E --line-buffered "returncode|total_wall_s|Error|Traceback"
python -I -c "
import json
a = json.load(open('runs/tech4/F6_s9005/meta.json'))['sha256_arrays']; b = json.load(open('runs/tech4_g7/F6_s9005/meta.json'))['sha256_arrays']
print('G7 tech4 F6:', 'TRECE: identic bit cu bit' if a == b else 'PICA', {k: a[k] == b[k] for k in a})"
date "+g7 end %H:%M:%S"
PY=/d/Time/_venv_cuda/Scripts/python.exe
cd lm
for v in "bf16 --precision bf16" "a32 --alpha 32"; do
  set -- $v; tag=$1; shift
  for s in 7101 7102 7103; do
    cd ..; stop; cd lm
    "$PY" -I lm_forever_run.py --seed $s --diag_pre_final "$@" --out ../runs/lmsens_$tag/s$s 2>&1 | grep -E --line-buffered "^(seed|done)|Error|Traceback"
  done
  date "+lmsens_$tag end %H:%M:%S"
done
echo "LANT 2 TERMINAT"
