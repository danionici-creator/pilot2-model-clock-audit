#!/usr/bin/env bash
# Repeated runs for the open dbpedia question of R2 (preinregistrare_FOREVER_repetari_2026-11-08.md).
# Each new arm = tasks 1-3 + generations, starting from an EXISTING task-0 adapter, which is COPIED (never moved):
#   A = R1's task 0 (ckpt_tau), B = R2's task 0 (ckpt_eta_m). Commands and arguments as in launch_repro_resume.sh.
# Stage 1: eta_m_A1, tau_B1, then rep_verdict.py (exit 10 = preregistered early stop). Stage 2: tau_A2, eta_m_A2.
# Usage: bash launch_repetari.sh [1|2|all]   (default: all). Stops at the first failed stage.
cd "$(dirname "$0")"
export PYTHONPATH=. FOREVER_CACHE=D:/Time/_date/hf_cache HF_HUB_OFFLINE=1 PYTHONIOENCODING=utf-8 FOREVER_DATA=data_longsequence
V=/d/Time/_venv_forever/Scripts/python.exe
BM=D:/Time/_modele/Qwen_Qwen3-0.6B
M=Qwen_Qwen3-0.6Blora_cl_dataset_id_4
LOG=../runs/forever_repetari.log
STAGE=${1:-all}
mkdir -p logs

run_arm() {  # $1 arm name, $2 clock (tau|eta_m), $3 source arm whose task 0 is reused (tau|eta_m)
  local arm=$1 clock=$2 src=$3 t rc
  local CK=ckpt_$arm OUT=output/$arm
  if [ -e $CK ] || [ -e $OUT ]; then echo "OPRIT: $CK sau $OUT exista deja $(date +%H:%M:%S)" >> $LOG; return 1; fi
  mkdir -p $CK/$M $OUT/${M}_bwt
  cp -r ckpt_$src/$M/0-dbpedia $CK/$M/ && cp output/$src/${M}_bwt/0-dbpedia_result.txt $OUT/${M}_bwt/ \
    || { echo "OPRIT: copierea sarcinii 0 pentru $arm a esuat $(date +%H:%M:%S)" >> $LOG; return 1; }
  echo "$arm: sarcina 0 copiata din $src ($(sha256sum $CK/$M/0-dbpedia/adapter_model.safetensors | cut -c1-8)) $(date +%H:%M:%S)" >> $LOG
  local SCRIPT=src/finetune_cl_our_qwen.py; [ $clock != tau ] && SCRIPT=src/finetune_cl_our_qwen_clock.py
  export FOREVER_CLOCK=$clock
  for t in 1 2 3; do
    [ -e ../runs/_HW_STOP ] && { echo "oprit de paznic $(date +%H:%M)" >> $LOG; return 2; }
    echo "$arm train task $t start $(date +%H:%M:%S) (no_cache=1)" >> $LOG
    env PYTORCH_NO_CUDA_MEMORY_CACHING=1 $V $SCRIPT --base_model $BM --num_epochs 10 --first_task_epochs 60 --group_by_length \
      --lora_target_modules '["q_proj","v_proj"]' --micro_batch_size 4 --batch_size 32 --max_input_length 512 \
      --dataset_id 4 --task_id $t --output_path $CK --memory_epochs 2 --steps_per_day 24 --memory_data_ratio 2 \
      --data_dir data_longsequence --cache_dir D:/Time/_date/hf_cache > logs/${arm}_train_t$t.log 2>&1
    rc=$?; echo "$arm train task $t rc=$rc $(date +%H:%M:%S)" >> $LOG
    [ $rc -ne 0 ] && { echo "OPRIT: antrenarea $arm/$t a esuat $(date +%H:%M:%S)" >> $LOG; return 1; }
    if [ $t -lt 3 ]; then
      $V src/generate_bwt.py --base_model $BM --dataset_id 4 --service_begin_id $t --method_name cl \
        --output_root $OUT --lora_checkpoint_path $CK > logs/${arm}_bwt_t$t.log 2>&1
      rc=$?; echo "$arm bwt-gen task $t rc=$rc $(date +%H:%M:%S)" >> $LOG
      [ $rc -ne 0 ] && { echo "OPRIT: generarea BWT $arm/$t a esuat $(date +%H:%M:%S)" >> $LOG; return 1; }
    fi
  done
  $V src/generate_avgPerf.py --base_model $BM --dataset_id 4 --method_name cl --max_task_id 3 \
    --output_root $OUT --lora_checkpoint_path $CK > logs/${arm}_avgPerf.log 2>&1
  rc=$?; echo "$arm avgPerf-gen rc=$rc $(date +%H:%M:%S)" >> $LOG
  [ $rc -ne 0 ] && { echo "OPRIT: generarea OP $arm a esuat $(date +%H:%M:%S)" >> $LOG; return 1; }
  bash eval_repro.sh $arm >> $LOG 2>&1 || { echo "OPRIT: evaluarea $arm a esuat" >> $LOG; return 1; }
  if [ $clock = eta_m ]; then $V -I r2_reconstruction_arm.py $arm >> ../runs/forever_repetari_r2.log 2>&1; fi
  return 0
}

arm_or_exit() { run_arm "$@"; local rc=$?; [ $rc -eq 2 ] && exit 0; [ $rc -ne 0 ] && exit 1; }

echo "REPETARI start (etapa $STAGE) $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
if [ "$STAGE" = 1 ] || [ "$STAGE" = all ]; then
  arm_or_exit eta_m_A1 eta_m tau
  arm_or_exit tau_B1 tau eta_m
  $V -I rep_verdict.py >> $LOG 2>&1; rc=$?
  [ $rc -eq 10 ] && { echo "OPRIRE TIMPURIE dupa etapa 1 (regula preinregistrata) $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG; exit 0; }
  [ $rc -ne 0 ] && { echo "OPRIT: rep_verdict.py rc=$rc" >> $LOG; exit 1; }
fi
if [ "$STAGE" = 2 ] || [ "$STAGE" = all ]; then
  arm_or_exit tau_A2 tau tau
  arm_or_exit eta_m_A2 eta_m tau
  $V -I rep_verdict.py >> $LOG 2>&1
fi
echo "REPETARI TERMINAT $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
