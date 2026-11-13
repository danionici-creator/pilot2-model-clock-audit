# Read-only count for Codex B04: responses capped at cutoff//2 = 256 tokens in lm_superni_run.load_tasks
import json, os, sys
from transformers import AutoTokenizer
sys.stdout.reconfigure(encoding="utf-8")
MODEL_DIR = r"D:\Time\_modele\Qwen_Qwen3-0.6B"
DATA = r"D:\Time\_date\FOREVER_bbeb549\data_superni"
ORDER = ["task1572", "task363", "task1290", "task181", "task002"]
HEAD_IN = ("Below is an instruction that describes a task, paired with an input that provides further context. Write a "
           "response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Input:\n")
TAIL = "\n\n### Response:\n"
cutoff = 512
tok = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
enc = lambda s: tok(s, add_special_tokens=False).input_ids
tail = enc(TAIL); eos = tok.eos_token_id
for name in ORDER:
    for sp in ["train", "test"]:
        rows = json.load(open(os.path.join(DATA, sp, name + ".json"), encoding="utf-8"))
        n = len(rows); cut_resp = 0; cut_head = 0; cut_input = 0; lost_tok = 0; tot_tok = 0; maxlen = 0
        for r in rows:
            h = enc(HEAD_IN.format(instruction=r["instruction"])); i = enc(r["input"])
            full = enc(str(r["output"])) + [eos]
            o = full[: cutoff // 2]
            tot_tok += len(full); lost_tok += len(full) - len(o); maxlen = max(maxlen, len(full))
            if len(full) > len(o): cut_resp += 1
            budget = cutoff - len(h) - len(tail) - len(o)
            if budget < 0: cut_head += 1; budget = 0
            if len(i) > budget: cut_input += 1
        print(f"{name} {sp}: n={n}, response cut={cut_resp} ({100*cut_resp/n:.1f}%), resp tokens lost={lost_tok}/{tot_tok} ({100*lost_tok/max(tot_tok,1):.2f}%), max resp+eos={maxlen}, input cut={cut_input}, instruction head cut={cut_head}")
