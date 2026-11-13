# Evaluarea direcției de cercetare Pilot 2 (v0.4) de către Mistral Large 4

Model: `mistral-large-4` prin API; temperature 0.3, max_tokens 32000, reasoning_effort low; finish_reason: stop; usage: {'prompt_tokens': 2166, 'total_tokens': 5605, 'completion_tokens': 3439, 'prompt_tokens_details': {'cached_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 1723}, 'service_tier': 'standard'}. Trimis: rezumatul studiului și 6 întrebări de direcție, `02_Pilot2/Recenzii/Mistral_detalii/mistral_msg_directie_v04.txt`. Data: 2026-11-04 19:05.

---

**Q1. Relevance.** Verdict: it matters only in one of two framings — a sharp redundancy result with tight bounds, or a scheduler result — and is otherwise an incremental ablation.

FOREVER's only ablation of its time signal is against step counts (arXiv:2601.03938), so "does cumulative update norm carry information beyond ordinary training telemetry" is a genuine, unanswered gap, and the forgetting-prediction literature (Toneva et al., arXiv:1812.05159; Jin & Ren, arXiv:2402.01865) has likewise not asked it. The reader is the continual-learning community at NeurIPS/ICLR workshops and whoever cites FOREVER. What makes it cited rather than ignored: (i) a pre-specified equivalence margin tight enough that "equivalent" is a finding, not a shrug; (ii) at least one condition run in a FOREVER-like setting (small pretrained LM + LoRA); (iii) code and preregistration that let others reuse the harness. Without those, a toy-world R² comparison will be ignored.

Concrete change: add a direct reconstruction analysis — regress c_e itself on B_strong and report that R². That single number tells the reader whether the question is already closed before any forgetting prediction is run.

**Q2. The likely "equivalent" outcome.** Verdict: as specified, "equivalent" is close to foreordained, not merely predictable — and that is a design fact, not bad luck.

If S(t) is the parameter vector and D is a parameter-space distance, then D(S(t), S(t+1)) is the AdamW update, which is a deterministic function of the learning rate, momentum, and second-moment norms — all of which are in B_strong. Stage A then reduces to "does a nonlinear model (GBT) recover a known function of the features better than the raw features," which it will, trivially, to a degree set by model capacity. The informative version of an equivalence result needs: (a) a tight pre-specified margin on the incremental R², not just three outcome labels; (b) the reconstruction R² from Q1; (c) a cost/benefit statement — c_e as FOREVER uses it requires retaining or snapshotting full state per step, while telemetry is O(1) per step, so "equivalent" plus "cheaper" is a real recommendation; (d) a direct comparison inside the FOREVER setting, since that is where the claim is actually deployed.

Concrete change: reframe the primary estimand as "upper bound on the incremental predictive value of c_e given B_strong, with a margin small enough to matter for scheduling," and report the telemetry→c_e reconstruction R² alongside.

**Q3. Narrow world.** Verdict: the toy world can support a claim about mechanisms, not about LLMs — and a null result there is nearly unpublishable.

Memorised key–value facts in a 0.93 M model with forgetting saturated by 1,280 steps is a regime where interference is dominated by output-bias drift (your own Stage 0 finding), which is not how LLM continual learning fails. The honest statement is: the study tests whether accumulated self-change carries information beyond telemetry *in this regime*. Weighing power against external validity: on one CPU, Pythia-160m/410m with LoRA admits perhaps tens of runs, which is enough for a scheduler comparison with a large effect but not for an R² increment. My weighing: external validity wins, because the toy-world result has no reader if null and little novelty if positive; a small pretrained-model condition is what makes any outcome citable. Keep the toy world only as a fast sanity harness, not as the reported result.

Concrete change: make the reported Stage A a small pretrained LM + LoRA forgetting-prediction audit (fewer runs, larger effect expected), with the synthetic world demoted to pilot data.

**Q4. Scope of the preregistration.** Verdict: sound, and standard practice for conditional designs.

Deferring Stage B to a later protocol written after Stage A is defensible precisely because Stage B is expensive (600–1,000 runs) and only runs on a supported Stage A. The risk is motivated re-specification of B after seeing A; the mitigation is to commit now, in the Stage A preregistration, to the exact decision rule and to the skeleton of B's comparison set, so the later protocol can refine but not reverse.

Concrete change: in the Stage A preregistration, include a one-page frozen appendix stating the Stage B decision rule and scheduler set.

**Q5. Over-engineering.** Verdict: yes, the protocol is disproportionate; the complexity is in the wrong places.

Cut or merge: (i) six stream families → keep two: one "natural" stream and the adversarial/decoupling stream, which is the only one where c_e and telemetry can diverge in the direction that matters; (ii) merge calibration and validation into one pilot phase; (iii) drop the exploratory order-effects module from the preregistration entirely; (iv) drop placebo gates that do not enter the primary inference — keep one positive control and one placebo; (v) collapse the 21 sections; a 32-page protocol with revision logs is a signal that each review added process, not inference. Must stay: the pre-specified smallest effect of interest with a tight equivalence margin, held-out within-run R², locked hyperparameters with equal tuning budgets, the adversarial stream, and bit-identical reruns.

Concrete change: rewrite as a ≤8-page protocol with one primary estimand, one adversarial stream, one positive control, one placebo.

**Q6. A better study.** Verdict: yes — collapse the audit and the scheduler question into one smaller study in a FOREVER-like setting.

Concretely: Pythia-160m (or 410m if CPU allows) with LoRA, ~8–12 synthetic or curated fact streams, budget-matched replay schedulers — (a) step-count, (b) c_e = cumulative LoRA update norm (FOREVER's clock), (c) a GBM on cheap telemetry — with final retention as the outcome, plus the telemetry→c_e reconstruction R² as a secondary estimand. This answers "does the model-centric clock earn its keep" directly, which is the question FOREVER actually raises, with ~30–60 runs instead of 315+. The current design's Stage A (predicting forgetting from telemetry) is a detour: even a supported Stage A does not show the clock is useful, and an equivalent Stage A does not show it is useless, until Stage B runs.

**Final recommendation: C — a redesigned, smaller study (essentially B's staging with Q6's design).**

Three deciding reasons: (1) the practically relevant question is the scheduler comparison, and the current Stage A is a near-foreordained redundancy check because c_e in parameter space is a deterministic function of telemetry already in B_strong — so run the decisive comparison directly, in a small pretrained-LM + LoRA setting, with fewer runs; (2) Stage B should not be locked into a preregistration before Stage A's outcome exists, so keep the conditional structure but shrink the whole programme; (3) external validity is what makes any outcome citable, and one laptop cannot buy both 315 toy runs and LLM validity — buy the latter.

Main risk of this recommendation: with tens of runs on a pretrained model, the equivalence/scheduler comparison may be underpowered, and an inconclusive result on a laptop is hard to publish. What would change my mind: if the telemetry→c_e reconstruction R² in a pilot exceeds ~0.99, the question is closed by construction and I would move to D (stop); if a small pilot on Pythia-LoRA shows a large scheduler effect, I would commit to the full pretrained-model study rather than the toy world.