"""POST HOC diagnostic, 10 Nov 2026: why greedy decoding differs from the authors' decoding on a few items (test (a)).

For every item whose greedy answer (output/_eval_noise_posthoc/<arm>_greedy) differs from the original answer
(output/<arm>), the item is generated again with the final adapter, in the authors' way (prompt from their Prompter,
fp16 PeftModel, do_sample=True, temperature 0.02, top_p 0, top_k 1) and greedily, with output_scores. At the first
token where the two generations differ, it records the two highest raw logits of the greedy pass (the forward passes are
identical up to that token) and the raw logit of the token the authors' decoding chose. A tie means equal raw logits.
Writes runs/forever_eval_tie_diagnostic_posthoc.json and prints a summary.
    cd forever_repro; PYTHONPATH=. HF_HUB_OFFLINE=1 <_venv_forever python> eval_tie_diagnostic_posthoc.py
"""
import json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
os.chdir(HERE)
sys.path.insert(0, str(HERE / "src"))
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils.prompter import Prompter
from utils.dataset_order import get_dataset_order

BM = "D:/Time/_modele/Qwen_Qwen3-0.6B"
N = "Qwen_Qwen3-0.6Blora_cl_dataset_id_4"
ARMS = ["tau", "eta_m", "eta_m_A1", "tau_B1"]
order = get_dataset_order(4)
prompter = Prompter("")
tok = AutoTokenizer.from_pretrained(BM)
if tok.pad_token_id is None:
    tok.pad_token_id = tok.eos_token_id
tok.padding_side = "left"
res = []
for arm in ARMS:
    base = AutoModelForCausalLM.from_pretrained(BM, dtype=torch.float16, device_map="auto", trust_remote_code=True)
    model = PeftModel.from_pretrained(base, f"ckpt_{arm}/{N}/3-agnews", dtype=torch.float16)
    model.config.pad_token_id = tok.pad_token_id
    model.eval()
    for i, task in enumerate(order):
        a = open(f"output/{arm}/{N}_avgPerf/{i}-{task}_result.txt", encoding="utf-8").read().split("\n")
        g = open(f"output/_eval_noise_posthoc/{arm}_greedy/{N}_avgPerf/{i}-{task}_result.txt", encoding="utf-8").read().split("\n")
        data = json.load(open(f"data_longsequence/test/{task}.json", encoding="utf-8"))
        for k, (x, y) in enumerate(zip(a, g)):
            if x == y:
                continue
            s = data[k]
            ids = tok(prompter.generate_prompt(s["instruction"], s["input"]), return_tensors="pt").to("cuda")
            with torch.no_grad():
                o1 = model.generate(**ids, do_sample=True, temperature=0.02, top_p=0, top_k=1, num_beams=1,
                                    max_new_tokens=128, return_dict_in_generate=True)
                o2 = model.generate(**ids, do_sample=False, num_beams=1, max_new_tokens=128,
                                    return_dict_in_generate=True, output_scores=True)
            L = ids["input_ids"].shape[1]
            t1, t2 = o1.sequences[0, L:].tolist(), o2.sequences[0, L:].tolist()
            j = next((n for n, (p, q) in enumerate(zip(t1, t2)) if p != q), None)
            r = {"arm": arm, "task": task, "item": k, "reproduced": tok.decode(t1, skip_special_tokens=True) != tok.decode(t2, skip_special_tokens=True)}
            if j is not None and j < len(o2.scores):
                sc = o2.scores[j][0].float()
                top = torch.topk(sc, 2)
                r.update(step=j, top1=float(top.values[0]), top2=float(top.values[1]), greedy_token=t2[j],
                         authors_token=t1[j], authors_token_logit=float(sc[t1[j]]),
                         tie=float(sc[t1[j]]) == float(top.values[0]))
            res.append(r)
    del model, base
    torch.cuda.empty_cache()
out = HERE.parent / "runs" / "forever_eval_tie_diagnostic_posthoc.json"
out.write_text(json.dumps(res, indent=1), encoding="utf-8")
n = len(res); rep = sum(r["reproduced"] for r in res); ties = sum(r.get("tie", False) for r in res)
print(f"items whose greedy answer differs from the original: {n}; difference reproduced now: {rep}; "
      f"first differing token is a tie of raw logits: {ties} of {sum('tie' in r for r in res)}")
for r in res:
    print(r)
