"""Summary of a set of Stage 0 runs: measurability (section 12a, first row), timing and memory.

    python stage0_summary.py runs/tech1        (writes runs/tech1/summary.json and summary.md)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from p2.triplets import build, run_summary      # noqa: E402


def main(tag_dir):
    base = Path(tag_dir)
    rows = []
    for d in sorted(p for p in base.iterdir() if (p / "meta.json").exists()):
        df, meta = build(d)
        df.to_parquet(d / "triplets.parquet")
        s = run_summary(df, meta)
        s["life_steps"] = meta["life_steps"]
        s["ms_per_train_step"] = round(1000 * s["timing_s"]["train"] / (meta["life_steps"]), 1)
        s["n_evals"] = meta["n_evals"]
        rows.append(s)
    (base / "summary.json").write_text(json.dumps(rows, indent=1, default=float), encoding="utf-8")
    cols = ["family", "childhood_acc", "childhood_acc_rule", "episodes", "valid_episodes", "episodes_competent_fact",
            "episodes_fact", "episodes_competent_rule", "episodes_rule", "included", "r_AB", "F_A_mean", "F_A_sd",
            "dAcc_A_mean", "rate_D1_cv", "n_evals", "ms_per_train_step"]
    lines = ["| " + " | ".join(cols) + " | wall min | peak MB |", "|" + "---|" * (len(cols) + 2)]
    for s in rows:
        lines.append("| " + " | ".join(str(s.get(c, "")) for c in cols)
                     + f" | {s['timing_s']['wall'] / 60:.1f} | {s['peak_rss_mb']} |")
    (base / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1])
