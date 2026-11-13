# OP over all 4 tasks with the lenient label extraction of THEIR eval_bwt_longsequence.py (imported unchanged).
# Run from src/ with PYTHONPATH="..;." (see eval_repro.sh). Argument: <variant>/<model>_avgPerf.
import sys
sys.stdout.reconfigure(encoding="utf-8")
from utils.dataset_order import get_dataset_order
import eval_bwt_longsequence as E

order = get_dataset_order(4)
d = E.resolve_output_dir(sys.argv[1])
acc = E.get_acc_scores_for_dir(d, order, list(range(len(order))))
print("lenient per-task acc:", [round(a, 4) for a in acc])
print("lenient OP:", sum(acc) / len(acc))
