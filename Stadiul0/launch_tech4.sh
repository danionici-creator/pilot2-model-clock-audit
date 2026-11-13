#!/bin/bash
# tech4 alone (the first attempt in launch_weekend_1.sh failed at import: python -I drops the script folder from sys.path).
cd /d/Time/02_Pilot2/Stadiul0
if [ -f runs/_HW_STOP ]; then echo "OPRIT de paznic: $(cat runs/_HW_STOP)"; exit 3; fi
date "+tech4 start %Y-%m-%d %H:%M:%S"
python launch.py --runs F1:9005 F2:9005 F3:9005 F4:9005 F5:9005 F6:9005 --workers 4 --tag tech4 2>&1 | grep -E --line-buffered "returncode|stopped_by_watchdog|total_wall_s|Error|Traceback"
date "+tech4 end %Y-%m-%d %H:%M:%S"
echo "TECH4 TERMINAT"
