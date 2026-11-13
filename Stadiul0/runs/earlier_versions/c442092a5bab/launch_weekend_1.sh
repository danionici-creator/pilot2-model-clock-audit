#!/bin/bash
# Weekend chain 1 (6 Nov 2026, evening): lmtech2 on the GPU, then tech4 (F1-F6, seed 9005) on the CPU with 4 workers.
# Sequential, so the throughput of each round is measured alone. Stops if runs/_HW_STOP exists.
cd /d/Time/02_Pilot2/Stadiul0/lm && bash launch_lmtech2.sh || exit $?
cd /d/Time/02_Pilot2/Stadiul0
if [ -f runs/_HW_STOP ]; then echo "OPRIT de paznic înainte de tech4: $(cat runs/_HW_STOP)"; exit 3; fi
date "+tech4 start %Y-%m-%d %H:%M:%S"
python -I launch.py --runs F1:9005 F2:9005 F3:9005 F4:9005 F5:9005 F6:9005 --workers 4 --tag tech4 2>&1 | grep -E --line-buffered "returncode|stopped_by_watchdog|total_wall_s|Error|Traceback"
date "+tech4 end %Y-%m-%d %H:%M:%S"
echo "LANT 1 TERMINAT"
