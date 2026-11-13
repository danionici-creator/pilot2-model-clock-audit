#!/bin/bash
# lmtech1: 3 seeds in sequence on the GPU, then a full repeat of the first seed (G7-GPU). Rerunning the script skips
# complete runs (meta.json present). Run from Stadiul0/lm:  bash launch_lmtech1.sh
PY=/d/Time/_venv_cuda/Scripts/python.exe
OUT=../runs/lmtech1
mkdir -p "$OUT"
for s in 7101 7102 7103; do
  "$PY" -I lm_forever_run.py --seed $s --out "$OUT/s$s" 2>&1 | grep -E --line-buffered "^(seed|task|done|complete)|Error|error|Traceback"
done
"$PY" -I lm_forever_run.py --seed 7101 --out ../runs/lmtech1_g7/s7101 2>&1 | grep -E --line-buffered "^(seed|task|done|complete)|Error|error|Traceback"
"$PY" -I -c "
import json
a = json.load(open('$OUT/s7101/meta.json')); b = json.load(open('../runs/lmtech1_g7/s7101/meta.json'))
same = a['sha256_steps_data'] == b['sha256_steps_data'] and a['files'] == b['files']
print('G7-GPU', 'TRECE: identic bit cu bit' if same else 'PICĂ: diferențe', {k: a['files'][k] == b['files'][k] for k in a['files']})
"
echo "lmtech1 TERMINAT"
