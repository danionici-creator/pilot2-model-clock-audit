#!/usr/bin/env bash
# FOREVER reproduction with their code, order 4, full fidelity (preinregistrare_FOREVER_repro_2026-11-07.md).
cd "$(dirname "$0")"
export PYTHONPATH=. FOREVER_CACHE=D:/Time/_date/hf_cache HF_HUB_OFFLINE=1 PYTHONIOENCODING=utf-8 FOREVER_DATA=data_longsequence
V=/d/Time/_venv_forever/Scripts/python.exe
BM=D:/Time/_modele/Qwen_Qwen3-0.6B
LOG=../runs/forever_repro.log
mkdir -p logs
echo "REPRO start $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
for variant in tau eta_m; do
  SCRIPT=src/finetune_cl_our_qwen.py; [ "$variant" != tau ] && SCRIPT=src/finetune_cl_our_qwen_clock.py
  export FOREVER_CLOCK=$variant
  CK=ckpt_$variant; OUT=output/$variant
  for t in 0 1 2 3; do
    [ -e ../runs/_HW_STOP ] && { echo "oprit de paznic $(date +%H:%M)" >> $LOG; exit 0; }
    echo "$variant train task $t start $(date +%H:%M:%S)" >> $LOG
    $V $SCRIPT --base_model $BM --num_epochs 10 --first_task_epochs 60 --group_by_length \
      --lora_target_modules '["q_proj","v_proj"]' --micro_batch_size 4 --batch_size 32 --max_input_length 512 \
      --dataset_id 4 --task_id $t --output_path $CK --memory_epochs 2 --steps_per_day 24 --memory_data_ratio 2 \
      --data_dir data_longsequence --cache_dir D:/Time/_date/hf_cache > logs/${variant}_train_t$t.log 2>&1
    echo "$variant train task $t rc=$? $(date +%H:%M:%S)" >> $LOG
    if [ $t -lt 3 ]; then
      $V src/generate_bwt.py --base_model $BM --dataset_id 4 --service_begin_id $t --method_name cl \
        --output_root $OUT --lora_checkpoint_path $CK > logs/${variant}_bwt_t$t.log 2>&1
      echo "$variant bwt-gen task $t rc=$? $(date +%H:%M:%S)" >> $LOG
    fi
  done
  $V src/generate_avgPerf.py --base_model $BM --dataset_id 4 --method_name cl --max_task_id 3 \
    --output_root $OUT --lora_checkpoint_path $CK > logs/${variant}_avgPerf.log 2>&1
  echo "$variant avgPerf-gen rc=$? $(date +%H:%M:%S)" >> $LOG
done
echo "REPRO TERMINAT $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG
