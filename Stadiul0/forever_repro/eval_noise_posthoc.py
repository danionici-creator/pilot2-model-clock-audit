"""POST HOC test (a), 9 Nov 2026, after the final review round (Recenzii/Runda_finala_2026-11-09): evaluation noise.

Regenerates the OP outputs of the FINAL adapter (task 3, agnews) of one cell of stage 1 with the authors' own
src/generate_avgPerf.py, imported and called unchanged, in one of two modes:
  seed<N>  their decoding settings (do_sample=True, temperature 0.02, top_p 0, top_k 1), with every RNG seeded to N;
  greedy   the same call with do_sample=False (temperature, top_p and top_k dropped; nothing else changed).
Outputs go to output/_eval_noise_posthoc/<arm>_<mode>/; the original outputs (output/<arm>/) are never touched.
A partial output folder from an interrupted attempt is renamed (kept), never deleted, and the evaluation restarts.
Every 100 generations it checks runs/_HW_STOP (hardware watchdog) and exits with code 3 if the file exists.

Run from forever_repro/ in the authors' environment (see launch_eval_noise_posthoc.sh):
    PYTHONPATH=. FOREVER_DATA=data_longsequence HF_HUB_OFFLINE=1 <_venv_forever python> eval_noise_posthoc.py <arm> <mode>
<arm> in {tau, eta_m, eta_m_A1, tau_B1}: the four cells of stage 1 (R1, R2, A1, B1).
"""
import datetime as dt, os, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STOP = HERE.parent / "runs" / "_HW_STOP"
ARMS = ("tau", "eta_m", "eta_m_A1", "tau_B1")
BM = "D:/Time/_modele/Qwen_Qwen3-0.6B"
N = "Qwen_Qwen3-0.6Blora_cl_dataset_id_4"
TASKS = ("0-dbpedia", "1-amazon", "2-yahoo", "3-agnews")


def main():
    arm, mode = sys.argv[1], sys.argv[2]
    assert arm in ARMS, arm
    assert mode == "greedy" or (mode.startswith("seed") and mode[4:].isdigit()), mode
    os.chdir(HERE)
    root = Path("output") / "_eval_noise_posthoc" / f"{arm}_{mode}"
    res = root / f"{N}_avgPerf"
    test = {t: len(__import__("json").load(open(f"data_longsequence/test/{t.split('-')[1]}.json", encoding="utf-8")))
            for t in TASKS}
    done = res.exists() and all((res / f"{t}_result.txt").exists() and
                                sum(1 for _ in open(res / f"{t}_result.txt", encoding="utf-8")) == test[t] for t in TASKS)
    if done:
        print(f"complete, skipping: {res}"); return 0
    if root.exists():                                   # interrupted attempt: keep it, start again
        keep = root.with_name(root.name + f"_incomplete_{dt.datetime.now():%Y%m%d_%H%M%S}")
        root.rename(keep); print(f"partial output kept as {keep}")

    import numpy as np, torch, transformers
    orig = transformers.GenerationMixin.generate
    calls = [0]

    def generate(self, *a, **k):
        calls[0] += 1
        if calls[0] % 100 == 0 and STOP.exists():
            print(f"_HW_STOP found after {calls[0]} generations; exiting", flush=True); sys.exit(3)
        if mode == "greedy":
            k["do_sample"] = False
            for x in ("temperature", "top_p", "top_k"):
                k.pop(x, None)
        return orig(self, *a, **k)

    transformers.GenerationMixin.generate = generate
    if mode != "greedy":
        s = int(mode[4:])
        random.seed(s); np.random.seed(s); torch.manual_seed(s); torch.cuda.manual_seed_all(s)
    print(f"eval_noise_posthoc {arm} {mode} start {dt.datetime.now():%Y-%m-%d %H:%M:%S}; torch {torch.__version__}, "
          f"transformers {transformers.__version__}", flush=True)
    sys.path.insert(0, str(HERE / "src"))
    import generate_avgPerf                               # the authors' script, unchanged
    generate_avgPerf.main(base_model=BM, dataset_id=4, method_name="cl", max_task_id=3,
                          output_root=str(root), lora_checkpoint_path=f"ckpt_{arm}")
    print(f"eval_noise_posthoc {arm} {mode} end {dt.datetime.now():%Y-%m-%d %H:%M:%S}; generations {calls[0]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
