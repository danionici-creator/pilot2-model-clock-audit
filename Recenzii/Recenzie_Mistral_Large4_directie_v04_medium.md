# Evaluarea direcției de cercetare Pilot 2 (v0.4) de către Mistral Large 4

Model: `mistral-large-4` prin API; temperature 0.3, max_tokens 64000, reasoning_effort medium; finish_reason: stop; usage: {'prompt_tokens': 2166, 'total_tokens': 7611, 'completion_tokens': 5445, 'prompt_tokens_details': {'cached_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 3704}, 'service_tier': 'standard'}. Trimis: rezumatul studiului și 6 întrebări de direcție, `02_Pilot2/Recenzii/Mistral_detalii/mistral_msg_directie_v04.txt`. Data: 2026-11-04 19:14.

---

**Q1. Relevance.** Verdict: relevant only if framed as a direct test of FOREVER's model-centric-time claim; as a standalone toy audit it will be ignored.

The question — does accumulated self-change carry predictive information about forgetting beyond what a training loop already logs — is exactly the ablation FOREVER lacks (its only time-signal control is step count; arXiv:2601.03938). That matters to the continual-learning community (CoLLAs, NeurIPS/ICML continual-learning workshops) and to anyone building rehearsal schedulers on forgetting curves (Toneva et al., arXiv:1812.05159; Jin & Ren, arXiv:2402.01865; Kalajdzievski, arXiv:2401.05605). But a 0.93M dense transformer memorizing 256 key–value pairs is a mechanism probe, not evidence about LLMs; readers will file it as a toy unless it is tied to the setting where the claim is made. To be cited rather than ignored, the headline must be about model-centric time's redundancy, and there must be at least one arm in the FOREVER regime (small pretrained LM + LoRA).

Concrete change: retitle and re-abstract around "is model-centric time redundant with optimizer telemetry?", and add a small Pythia-LoRA arm (even 10–20 runs) as the external-validity anchor.

**Q2. The likely "equivalent" outcome.** Verdict: "equivalent" is a real contribution only if equivalence is tightly bounded and costed; otherwise it is a predictable confirmation.

In an AdamW-trained network the update norm is a deterministic function of the gradient and the second-moment estimates, so c_e is largely reconstructible from telemetry — the author's prior is almost certainly correct. The informative version of the null is: "c_e adds no predictive value beyond O(1)-per-step telemetry, at zero extra memory and compute, in the setting where FOREVER claims it matters." That requires equivalence bounds tied to FOREVER's reported scheduling gains, not bounds chosen for statistical convenience, plus an explicit cost accounting: c_e requires either storing full parameter snapshots or computing a full-parameter distance every step, while B_strong is scalar telemetry any loop already has. Without the FOREVER setting and the cost framing, equivalence in a toy is unsurprising and will not be cited.

Concrete change: prespecify the equivalence margin from FOREVER's effect sizes (arXiv:2601.03938) and add a short compute/memory cost comparison of c_e versus B_strong.

**Q3. Narrow world.** Verdict: the toy world supports mechanism claims only; run the audit in the LoRA setting or add a LoRA arm, accepting fewer runs.

Forgetting in a 0.93M model over ≤1,280 steps is a different regime from LLM continual fine-tuning: LoRA updates live in a low-rank subspace, and the interference structure that drives forgetting differs. On the power/validity trade-off: 315 toy runs give a precise estimate of a toy quantity; 20–50 LoRA runs give a noisy estimate of the quantity that matters. Given the author's prior is "equivalent," precision matters less than validity — a noisy but valid equivalence in the FOREVER regime is more citable than a precise toy equivalence. On the stated hardware, Pythia-70M with LoRA for a few thousand steps is slow but plausible; Pythia-160M is likely not. If even 70M is infeasible in reasonable wall-clock time, keep the toy model but scope the title and claims explicitly to "small dense transformers."

Concrete change: add a Stage A′ arm — smallest feasible Pythia + LoRA, ~20–30 runs, same decoupling streams, same analysis — reported separately from the toy arm.

**Q4. Scope of the preregistration.** Verdict: sound; preregister Stage A only, with the Stage B decision rule fixed now and the Stage B protocol timestamped before any Stage B data.

Conditional multi-stage preregistrations are standard when the gating condition is prespecified. The risk is reputational rather than methodological: a Stage B protocol written after seeing Stage A could look motivated. That is mitigated by committing now to deposit a dated Stage B protocol (design, analysis, gates) before the first Stage B run.

Concrete change: add to the Stage A preregistration a commitment that the Stage B protocol will be publicly deposited, with a timestamp, before any Stage B data collection.

**Q5. Over-engineering.** Verdict: over-engineered; cut the run-split machinery and exploratory modules, keep the decoupling streams, the telemetry battery, and the equivalence bounds.

What must stay: (i) the stream families that decouple steps from parameter change (idle intervals, cosine warm restarts, variable re-exposure/batch size) — without these, c_e and step count are collinear and the question is vacuous; (ii) B_strong as the competitor set; (iii) unit of inference = run, with held-out evaluation; (iv) prespecified SESOI/equivalence bounds; (v) bit-identical reruns. What to cut or merge: collapse the calibration/training/validation/test split of runs into a single pilot plus one held-out test set; reduce six stream families to three; defer or drop the order/path-effects module; replace the gradient-boosted trees with a single prespecified mixed-effects model (or keep GBTs with one locked configuration and no tuning budget); reduce the gates to one positive control (step count predicts forgetting) and one placebo (time-permuted c_e adds nothing).

Concrete change: rewrite the protocol to roughly ten pages containing only the items in the "must stay" list plus the cut list above.

**Q6. A better study.** Verdict: the decisive smaller study is a direct ablation of FOREVER plus a causal probe using the adversarial stream.

Two designs answer the underlying question more decisively than a 315-run predictive audit. (1) Direct ablation: replicate FOREVER at the smallest feasible scale — Pythia-70M + LoRA, replay scheduled on forgetting-curve intervals in c_e-time versus step-time versus telemetry-time, matched compute, 20–40 runs. This tests the published claim directly and is citable whatever the outcome. (2) Causal probe in the toy model: use the adversarial stream (large parameter change, little interference) and the idle stream (time passing, little change) as a 2×2 manipulation; if forgetting tracks interference/telemetry rather than c_e, the model-centric clock is not the driver. That is a handful of runs and decisive about mechanism.

Concrete change: if compute forces a choice, run design (2) in the toy model plus 10–20 runs of design (1), and drop the large GBT audit.

**Final. Recommendation: B — preregister Stage A only, defer Stage B — with two modifications: add the LoRA arm and cut the protocol as in Q5.**

Deciding reasons: (1) the question is worth asking and the decoupling-stream design is the right way to ask it, so stopping (D) wastes a sound core; (2) Stage-A-only preregistration avoids overcommitting to a Stage B that runs only on a supported outcome; (3) the LoRA arm plus a lean protocol is what makes the result citable rather than a toy null.

Main risk: the toy-model "equivalent" result is ignored because it does not speak to LLMs; the LoRA arm mitigates this but may be underpowered on one CPU, in which case the equivalence claim must be scoped down explicitly.

What would change my mind: if the LoRA arm proves computationally infeasible on the stated hardware, I would switch to option C — the adversarial-stream causal probe (Q6, design 2) as the primary study, since it is decisive about mechanism at toy scale; and if Stage A unexpectedly returns "supported" with a large effect, Stage B becomes the priority and the toy result gains value as mechanism evidence.