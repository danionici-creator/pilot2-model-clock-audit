# Evaluarea direcției de cercetare Pilot 2 (v0.4): Microsoft Copilot

Mod: „Think Deeper” (setat de utilizator). Prompt: `Prompturi/Pilot2_Prompt_directie_v04_chat.txt`. Lipit de utilizator în conversație, 4 nov. 2026. Textul e redat exact; linkurile [[arxiv.org]] sunt ale interfeței Copilot, iar câteva subiecte de propoziție (de exemplu „FOREVER” la începutul Q1 și Q3) s-au pierdut la copiere, probabil pentru că erau linkuri.

---

I treat this as a programme-level decision: whether the experiment can produce a result that changes beliefs or practice, not whether its preregistered estimators are technically defensible. My judgement below separates established points from estimates based on the brief.

Q1. Relevance
Verdict: The audit is relevant, but the present synthetic-only study would probably be read as a careful diagnostic note, not as a consequential continual-learning result.
Argument
already establishes both the operational index and its use in replay scheduling: accumulated optimizer-update magnitude as “model-centric time,” evaluated on continual-learning benchmarks and models from 0.6B to 13B (arXiv:2601.03938). Its reported comparison with step-based scheduling leaves a genuine unresolved question: whether update magnitude contains information unavailable from other cheap training telemetry. [[arxiv.org]](https://arxiv.org/abs/2601.03938), [[arxiv.org]](https://arxiv.org/pdf/2601.03938)
That question matters to three groups:

1. Continual-learning and replay researchers. They need to know whether update-norm clocks are a distinct control variable or merely a convenient compression of optimizer activity.
2. LLM fine-tuning researchers. Forgetting under LoRA is real, and it depends on update steps and the number of trainable parameters, so identifying which online signals improve prediction has operational value (arXiv:2401.05605). [[arxiv.org]](https://arxiv.org/abs/2401.05605)
3. Training-systems practitioners. They care whether a scheduling signal justifies extra parameter-difference accumulation, storage reads, synchronization or instrumentation.

It does not yet matter directly to persistent-agent research. Your experiment concerns optimizer-induced loss of memorised associations. It does not test self-knowledge, restoration, temporal evidence or agent identity. The connection to A Time of Their Own is conceptual, not an empirical conclusion supported by this design.
What would make the work cited is not the number of controls. It is one reusable conclusion of the following form:
Across deliberately decoupled training regimes, accumulated update norm adds no practically meaningful predictive information beyond a specified minimal telemetry set, or adds information only under identifiable conditions X and Y.
The publishable object should therefore be an audit of model-centric training clocks, not a validation of the broader experiential-time programme.
Concrete change
Frame the paper around three claims only:

1. incremental predictive value;
2. minimal sufficient telemetry;
3. transport to one pretrained-LoRA setting.

Use “experiential index” only in the motivation or discussion. Put “optimizer clock” or “model-centric training clock” in the title.

Q2. The likely “equivalent” outcome
Verdict: Equivalence to the full B_strong union is predictable and insufficient by itself; equivalence to a small, portable baseline would be informative.
Argument
Your current baseline contains losses, gradients, learning rates, moments, parameter norms, local update statistics and reference-battery loss changes. With enough nonlinear modelling, this is close to asking whether the norm of the realised update can be reconstructed from quantities that generate or closely track that update. A negative incremental result against this union would not be surprising.
The scientifically useful question is not:
Can a very rich telemetry set reconstruct cec_e?
It is:
What is the cheapest sufficient substitute, and in which regimes does substitution fail?
The distinction matters because cec_e could be redundant against 20 signals but still be the best single operational scalar. Conversely, it could add predictive value while being too costly, unstable or architecture-specific to justify using.
A comparable precedent is forgetting forecasting that connects prediction to targeted replay rather than stopping at predictive fit. Jin and Ren show that forecasts can support selective replay, while also reporting that one proposed mechanism worked on BART but failed on T5 (arXiv:2402.01865). That kind of cross-setting failure analysis matters more than a single aggregate R2R^2. [[arxiv.org]](https://arxiv.org/abs/2402.01865), [[ar5iv.labs.arxiv.org]](https://ar5iv.labs.arxiv.org/html/2402.01865)
Concrete change
Predefine a baseline ladder, not only B_strong:

1. steps or tokens;
2. steps + learning-rate integral;
3. steps + learning-rate integral + training loss;
4. a minimal optimizer set, probably gradient/update proxy plus learning-rate information;
5. B_strong;
6. each level plus cec_e.

Report:

* incremental predictive value;
* telemetry collection cost;
* storage and compute overhead;
* sensitivity to optimizer and clipping;
* the smallest subset matching cec_e.

Do not add more candidate metrics. Add ablation toward minimal sufficiency. A useful equivalent result would be: “Three scalars recover at least 95% of the predictive performance of update-norm time across all six stream families,” with the threshold preregistered.

Q3. Narrow world
Verdict: The synthetic model is suitable for mechanism isolation, but insufficient for claims about LLM continual learning; one small pretrained-LoRA transport test is necessary.
Argument
The synthetic setting gives you high run count, controlled stream interventions and repeated lives. That is valuable for distinguishing steps from parameter movement. A CPU-constrained pretrained model would sharply reduce replication and make flexible predictive comparisons unstable.
But the present world has three severe transport limitations:

* the target is retention of trained key-value associations, not preservation of broad pretrained capability;
* forgetting is nearly complete within about 1,280 steps;
* later loss growth reflects a shared output-distribution shift rather than additional item-specific forgetting.

Therefore, Stage A can support a statement about short-horizon associative retention in a small Transformer. It cannot establish that the same telemetry sufficiency relation holds in pretrained representations, LoRA subspaces or realistic continual fine-tuning. LoRA does not eliminate forgetting, and existing work examines much larger pretrained models (arXiv:2401.05605). likewise evaluates models beginning at 0.6B parameters, far outside your mechanistic system. [[arxiv.org]](https://arxiv.org/abs/2401.05605) [[arxiv.org]](https://arxiv.org/abs/2601.03938)
This is not resolved by replacing 200 synthetic runs with perhaps 10 expensive LoRA runs. That would trade a well-powered narrow result for an underpowered, noisy approximation of FOREVER.
Concrete change
Use a two-level Stage A:

* A1: Mechanistic audit, approximately 80 to 120 synthetic runs, preserving all six stream families and the designed decouplings.
* A2: Transport check, approximately 12 to 24 independent LoRA runs on one small pretrained model, with fewer predictors and a locked model.

Use the smallest pretrained model that gives nontrivial baseline competence and whose CPU runtime you measure before preregistration. Pythia-70M or Pythia-160M are reasonable candidates to benchmark, but I cannot infer feasibility from the brief. Missing information: measured CPU time per LoRA update, sequence length, rank and evaluation-battery cost.
A2 should test only the direction and practical magnitude of the main A1 contrast. Do not fit a large gradient-boosted predictor bank on 12 runs. Aggregate within-run evidence using a locked low-dimensional model.

Q4. Scope of the preregistration
Verdict: Preregister Stage A only; writing Stage B after observing Stage A is sound if Stage B is explicitly labelled a new confirmatory study.
Argument
Stage B is not merely another endpoint. It changes the research question from predictive information to closed-loop decision utility. Scheduler construction, budget matching and replay effects require different calibration and failure controls.
Because Stage B occurs only after a supported Stage A, fully specifying it now creates two problems:

* substantial work is spent designing a branch that probably never runs;
* Stage A may reveal the conditions under which cec_e is informative, making the present scheduler specification inappropriate.

The danger is not deferral. The danger is presenting a post-Stage-A scheduler as though it were part of the original confirmatory test.
Concrete change
Preregister Stage A and include only a short Stage B decision charter:

* the exact Stage A criterion that permits Stage B;
* what data from Stage A may be used to design it;
* a commitment to a new timestamped preregistration;
* fresh random seeds or streams not used in Stage A;
* no closed-loop efficacy claim unless Stage B is completed.

Call Stage B “confirmation of utility,” not “Stage A follow-up analysis.”

Q5. Over-engineering
Verdict: Yes; 315 runs, 32 pages and a 600 to 1,000-run conditional stage are disproportionate to the present scientific claim.
Argument
Repeated AI review has apparently expanded the protocol by accumulating safeguards. That can reduce procedural ambiguity while making the actual hypothesis difficult to see. More gates do not compensate for weak external validity.
Concrete change
Cut or merge:

* Merge placebo and positive-control logic into one compact validation section.
* Reduce the baseline family to the baseline ladder above. Remove metrics that are deterministic transformations or near-duplicates of realised updates.
* Use one principal forgetting outcome. Keep accuracy and alternative loss transformations as descriptive or sensitivity results.
* Reduce stream-family interaction claims. Retain all families for stress testing, but designate only two or three contrasts as confirmatory.
* Remove the optional path-order module from this protocol.
* Remove Stage B implementation details.
* Cut the 200-run test maximum unless calibration demonstrates that it is required to resolve the smallest effect of interest.
* Replace extensive adaptive calibration with a fixed pilot-to-lock transition and one auditable revision boundary.
* Do not treat the forgotten reference battery as a core candidate distance unless refreshed or independently held fixed. As described, it confounds the clock with degradation of its measuring instrument.

Must stay:

* run as the inference unit;
* held-out runs and locked models;
* deliberate decoupling of steps from parameter change;
* competence and signal-detection controls;
* time-permuted or otherwise structure-destroying placebo;
* prespecified practical-equivalence region;
* family-wise reporting, not only pooled performance;
* a hard rule excluding the post-saturation region from the forgetting interpretation.

Q6. A better study
Verdict: Use a paired intervention audit that asks when equal cheap telemetry produces unequal forgetting, rather than predicting forgetting from a large observational telemetry vector.
Argument
Prediction against B_strong encourages the learner to reconstruct cec_e from correlated variables. A more decisive design actively matches competing clocks and varies accumulated update distance.
Concrete study
Construct paired training intervals starting from the same checkpoint and protected task:

1. Step-matched pairs: equal steps and tokens, different accumulated update norm through learning-rate schedule, gradient clipping or batch construction.
2. Loss-matched pairs: approximately equal cumulative training loss, different update norm.
3. Update-matched pairs: approximately equal cec_e, different steps or token counts.
4. Silent controls: equal elapsed wall time with no updates.

For each pair, measure forgetting of the same protected items at the same endpoints. The primary estimand is the paired difference in forgetting.
The decisive pattern is:

* if forgetting follows cec_e under step- and loss-matched interventions, and remains similar under update-matched interventions, cec_e has mechanistic utility;
* if forgetting instead follows task-gradient alignment or reference-item loss change, scalar path length is inadequate;
* if all differences vanish after matching elementary update proxies, cec_e is a convenient summary, not an independent signal.

Run approximately 20 to 30 seeds per principal pair in the synthetic model, giving roughly 80 to 120 runs. Then repeat only the strongest two contrasts with LoRA on a small pretrained model.
Add one direction-sensitive competitor. A scalar path length cannot distinguish two equally large updates, one aligned with protected-task gradients and one orthogonal or antagonistic to them. EWC and Synaptic Intelligence already motivate parameter-importance and path-sensitive accounts rather than undifferentiated distance (DOI:10.1073/pnas.1611835114; arXiv:1703.04200). If a cheap directional statistic dominates cec_e, that is a more informative conclusion than “B_strong wins.”
This design is smaller, more interpretable and closer to a causal stress test. Its limitation is that exact matching may be difficult. Use tolerance bands established in pilot runs, not post hoc pair selection.

Final recommendation
Recommend C: replace the current protocol with a smaller Stage-A-only paired intervention audit, plus a limited pretrained-LoRA transport check. Do not preregister Stage B now.
Deciding reasons

1. The main likely result is currently too easy to explain away. B_strong contains enough optimizer-derived information that equivalence is expected, while a positive result could depend on synthetic stream peculiarities.
2. The main scientific uncertainty is transport, not another methodological gate. A modest LoRA check contributes more than hundreds of additional synthetic runs.
3. Interventional matching answers the underlying question more directly. It tests whether self-change tracks forgetting when cheap clocks are held approximately constant, rather than whether a flexible predictor can extract one correlated scalar from another.

Main risk
The smaller design may show that no scalar clock, including cec_e, works once update direction and task interference are considered. That would weaken the experiential-index narrative, but it would be the scientifically stronger outcome: accumulated change magnitude is not sufficient to represent consequential internal history.
What would change my recommendation
I would return to B, Stage A only in approximately its present predictive form, if pilot evidence showed both of the following:

* paired intervention matching cannot be achieved without destabilising training or changing task difficulty; and
* cec_e displays a sizeable, consistent incremental effect over a minimal telemetry baseline across several stream families, not merely over steps.

I would recommend D, stop, if a locked pilot on unseen runs shows that the apparent remaining headroom is almost entirely measurement noise or shared output-distribution drift, or if forgetting has too little unsaturated variation inside the 1,280-step window to distinguish the clocks reliably.
