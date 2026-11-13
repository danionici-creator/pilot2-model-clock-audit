# Adversarial research assessment — Pilot 2

Recommendation: B — Continue with a narrower, falsification-first Stage A

Overall judgment: The parameter-distance clocks have not been shown to be informationally redundant in general, but the evidence is strong enough to end their broad development as candidate experiential indices. The remaining scientific opportunity is narrower: determine whether functional change contains a reproducible, outcome-relevant residual beyond equally costly functional measurements and optimizer telemetry.

The strongest unresolved case is D3 under noisy distractors. It is also the case most vulnerable to a synthetic-design explanation. I would retain one parameter-clock exception, D1_rel in F6, as a bounded reconstruction check—not as an invitation to reopen the entire search.

Confidence: medium. My judgment is based on the technical results reported in the attached dossier, not independently rerun logs. I checked the primary FOREVER paper, arXiv:2601.03938v2. I could inspect the public repository's landing page, but not independently verify the specified code commit `bbeb549`; commit-specific implementation details therefore remain dossier-reported, not independently confirmed.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://arxiv.org\&sz=32)

arxiv.org

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

WoodScene/FOREVER: ACL 2026 · GitHub



## Q1. What does reconstruction actually establish?

### The defensible conclusion

R1 and R3 show that D1 and D2 are highly reconstructible from the tested telemetry in the observed synthetic regimes. R5, R6 and R9 show a similarly strong reconstruction of FOREVER's factor-space \\(\tau\\) on the Qwen3-0.6B arm.

They do not show that these clocks carry no information beyond telemetry in a general statistical or scientific sense.

The distinction is essential. A clock can have held-out reconstruction \\(R^2=0.99\\) while its remaining one percent of variance contains information about forgetting. Reconstruction establishes predictability of one variable from another; it does not establish conditional irrelevance to a third variable.

G2 is therefore a sensible protocol-level stopping rule, but the dossier's use of “not identifiable” must not be interpreted as a mathematical theorem.

The results also contain a meaningful exception that should not be hidden.

| Candidate          | Strongest evidence for reconstruction                                                                                            | Important limitation                                                      |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| D1                 | Synthetic GBDT \\(R^2=0.95–0.99\\) in reported R3 held-out families; LM \\(\tau\\) results separately support the same mechanism | Short windows and restart boundaries show larger errors                   |
| D1_rel             | R3 GBDT \\(R^2=0.94–0.99\\) in F2/F3/F5                                                                                          | F6 falls to \\(0.79\\); no universal closure                              |
| D2                 | R3 GBDT \\(R^2=0.94–0.99\\); simple moment-based scalar \\(0.98–0.99\\)                                                          | Strongly optimizer-linked, but this is not an H1 result                   |
| FOREVER \\(\tau\\) | LM GBDT \\(R^2=0.976–0.994\\) across R5–R6; R9 remains about \\(0.986–0.988\\)                                                   | Limited seeds, synthetic language tasks, and no causal replay replacement |

These are dossier results, not independent replications.

### Plausible artefacts and their terminating checks

1\. A near-duplicate predictor is included in B_strong.

The dossier lists “local update statistics” among the 58 baseline features without giving their complete provenance in this document. This matters because D1 is itself a norm of an applied update.

AdamW's applied update depends on learning rate, momentum, second-moment scaling and weight decay. A baseline containing closely derived update magnitudes could reconstruct D1 almost by construction.

The check is a feature-provenance audit:

- Identify every feature calculated directly from \\(\Delta\theta\\), D1, D1_rel or their components.
- Report reconstruction twice: with the complete operational baseline and with these direct clock proxies excluded.
- Preserve legitimate pre-existing optimizer telemetry, including moment norms; excluding every mechanically related variable would create an artificially weak competitor.

If the reconstruction remains above 0.90 with a genuinely independent, cheap feature set, the substantive claim survives. If it collapses, the original result is partly circular.

2\. Leakage or dependence between observations.

R1's held-out-run design and R3's leave-family-out design reduce ordinary row leakage. They do not eliminate dependence among overlapping intervals, shared tasks or phase templates. In the LM arm, 869 windows are not 869 independent experiments.

The check is prediction on entirely new seeds and task instances, with all windows from one run confined to one split. Report uncertainty across runs, not window rows.

3\. Window length and rate normalization hide failures.

R2 already identifies relevant failures: short-window relative error reaches 23%, compared with 8% for longer intervals; restarts produce systematic bias. R5 shows even larger schedule-only errors immediately after optimizer resets.

The check is to preregister reconstruction of both interval totals \\(\Delta c_e\\) and rates \\(\rho\\), conditioning on \\(\Delta N\\), and report performance separately for 64–127, 128–255, 256–639 and 640–1,279 steps. The LM audit should isolate the first eight steps after each phase reset.

4\. Learning-rate changes are mistaken for genuine experiential change.

R2 demonstrates that learning-rate restarts damage extrapolation for flexible models, while simple moment-based predictors remain comparatively stable for D1 and D2.

The check is a held-out restart distribution: train on one set of restart periods and amplitudes, test on disjoint settings. Predefine acceptable reconstruction error and bias at the transition, not merely aggregate \\(R^2\\).

5\. The synthetic world is too restricted.

The 4-token context and arbitrary facts are useful for controlled interference, but they do not establish relevance to linguistic or semantic continual learning. R4 also shows that accuracy saturates near complete forgetting after relatively short intervals.

The check is limited transfer, not a new benchmark programme: use the existing Qwen arm and one new synthetic family with a different interference mechanism. The objective is to test whether the same reconstruction relationship survives—not to claim coverage of realistic continual learning.

My assessment: D2 is the clearest candidate for operational closure. D1 and \\(\tau\\) are also near closure in the studied regimes. D1_rel/F6 must be resolved before claiming blanket reconstruction.

## Q2. Should confirmatory H1 proceed despite G2 failure?

No, not for D1, D2 or FOREVER's \\(\tau\\) as currently tested.

H1 has deliberately remained unanalysed. That is valuable because the investigators can still preserve a clean test for a defensible candidate. It would be poor research practice to override the protocol's own gate after observing reconstruction results.

The scientifically useful content remaining is:

1. A documented empirical result that optimizer telemetry reconstructs several parameter-distance clocks under specified conditions.
2. A demonstration that step counts or learning-rate schedules alone can be inadequate, even when richer optimizer telemetry succeeds.
3. An analysis of where reconstruction fails: short windows, optimizer resets, distribution shifts and F6.
4. A methodological distinction between measuring parameter movement and measuring information relevant to forgetting.

I would report R1–R3 and R5–R9 as exploratory or technical-stage evidence, keeping pre-fixed and post hoc analyses visibly separated. No p-value or uncertainty interval should suggest preregistered confirmation where there was none.

The closure report should say “highly reconstructible in the evaluated regimes,” not “contains no information.” It should not claim that the H1 null hypothesis was tested or accepted.

For D1_rel/F6, the appropriate next action is a prospective reconstruction audit. Only a reproducible residual below the G2 threshold would justify considering H1 on fresh data.

## Q3. Is D3/F6 real science or a synthetic artefact?

At present, it is an unresolved diagnostic anomaly, not an established scientific effect.

R3 reports that D3's held-out reconstruction in F6 is \\(R^2=0.18\\) using \\(\Delta N+\sum\eta\\|\hat m\\|\\), \\(0.59\\) using \\(\Delta N+C10c\\), and \\(0.81\\) using all telemetry. The corresponding GBDT reconstruction is approximately \\(0.99\\) in F2, F3 and F5.

That contrast is substantial. But it comes from a single corrected-code seed per family and a deliberately distinctive schedule containing variable distractors and 30% label noise.

The simpler explanation is that F6 changes the relationship between reference-probe output distributions and the optimizer measurements. D3 may merely detect that distribution shift.

There is an additional competitor problem. C10c measures absolute change in the loss assigned to the correct label. D3 measures changes in an entire predictive distribution. Even with identical forward-pass costs, C10c discards information D3 retains. Beating C10c alone would not establish a distinctive “functional clock.”

### Decisive experiment

I recommend a preregistered, seed-matched four-condition experiment:

| Condition                                               | Purpose                                                 |
| ------------------------------------------------------- | ------------------------------------------------------- |
| F6, 0% noise                                            | Distinguish distractor scheduling from label corruption |
| F6, 30% noise                                           | Direct replication of the anomaly                       |
| F6, 30% noise, altered distractor-duration distribution | Test robustness beyond the original schedule            |
| F2-style schedule with 30% noise                        | Test whether the effect transfers beyond F6             |

Use 20 fresh seeds per condition: eight for fitting predefined reconstruction and forgetting models, twelve held out for final evaluation. Match task generation and schedules where the paired comparison permits it. Keep the original T1 endpoint and \\(\Delta N<1,280\\) eligibility rule.

Competitors must include B_strong, C10c, and at least two non-identical, same-forward-pass functional summaries such as predictive-entropy change and mean total-variation distance. The latter is intentionally a strong functional rival, though it is closely related to D3; report it separately so a near-duplicate cannot silently determine the conclusion.

Preregistered success criterion: In both F6 noisy variants, D3's held-out reconstruction must remain below 0.90 under the strongest eligible competitor set. It must then improve held-out within-run forgetting \\(R^2\\) by at least 0.02 over that set, with a seed-clustered confidence interval excluding zero. The F2 noisy condition must show a positive improvement; otherwise the claim remains explicitly F6-specific. The clean F6 arm diagnoses noise dependence, rather than serving as an automatic failure condition.

All models and contrasts must be fixed before the twelve test seeds are generated. No selection of favourable window bands after inspection.

At 12.3 runs per hour, 80 runs require approximately 6.5 CPU wall-clock hours, plus an estimated two hours for validation and analysis. If the result fails, close D3 as an experiential-index candidate in this setting. If it passes, the defensible new result is residual predictive value of a functional-change summary under noisy interference, not experiential time.

## Q4. What can fairly be claimed about FOREVER?

The original FOREVER paper defines model-centric time as accumulated trainable-parameter update norm, resetting it per task. Its method uses this clock for replay scheduling and also uses update intensity to adjust replay regularisation. Those are distinct mechanisms. The paper reports a SuperNI time-calibration ablation against fixed-step calibration: an improvement of 1.2 percentage points in overall performance and 1.1 points in backward transfer, for the reported task order. It does not compare \\(\tau\\) with a moment-derived clock or a schedule-only cumulative-learning-rate clock. (Feng et al., arXiv:2601.03938v2.)&#x20;

[image](https://www.google.com/s2/favicons?domain=https://arxiv.org\&sz=32)

arxiv.org



A detail worth adding to the dossier: FOREVER's own Appendix C reports no statistically significant correlation between calibrated model-day length and final backward transfer (\\(r=0.2182,\ p=0.4536\\)). This is not a refutation of their scheduler, but it limits an intuitive interpretation that the calibrated clock directly tracks eventual forgetting.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://arxiv.org\&sz=32)

arxiv.org



### Supported by the author's technical results

- The pre-fixed prediction that schedule-only \\(\sum\eta\\) would reconstruct \\(\tau\\) with \\(R^2\geq0.80\\) failed: R5 gives 0.67 and R6 gives 0.58.
- Adding moment information produces much stronger reconstruction: \\(\sum\eta\\|\hat m\\|\\) reaches 0.94–0.95, and rich telemetry reaches 0.976–0.986 in R5–R6.
- R7's impressive phase-total reconstruction is largely a duration effect; the rate-normalised phase-level \\(R^2\\) of 0.09–0.18 is much less impressive.
- The schedule-only surrogate is close to \\(\tau\\) for the \\(d=2\\) trigger, but differs more at \\(d=4\\). Similar trigger timing is not evidence of equal forgetting outcomes.
- R8's validity failures prevent strong claims about performance. R9, however, shows that reconstruction is robust to the tested bf16 and LoRA-\\(\alpha\\) changes; bf16 also eliminates GradScaler skips.

Fair one-sentence claim: On this small synthetic-fact LoRA setup, FOREVER's parameter-distance clock is much better reconstructed from optimizer moments than from learning-rate schedules alone, and the result survives the tested precision and LoRA-scaling sensitivities.

That is a useful technical observation. It is not a refutation of FOREVER's published benchmark results.

### The experiment that would settle practical scheduler value

Run three versions of the same replay algorithm:

1. The original \\(\tau\\)-driven trigger.
2. A trigger driven by calibrated cumulative \\(\sum\eta\\|\hat m\\|\\).
3. A trigger driven by calibrated cumulative applied learning rate.

Hold constant the task stream, memory contents, replay regularisation rule and total replay budget. The regulariser should retain its original update-intensity calculation in all three arms so that only when to replay changes. Compare end-of-task and final old-task retention across paired seeds.

Use bf16, documenting it as a departure from the original fp16 implementation. Use the 512-fact setup because it reaches the \\(d=4\\) trigger. Before interpreting performance, require enough actual trigger separation—e.g. at least 20% of tasks differing by eight or more counted steps between relevant arms. Otherwise the experiment cannot distinguish the schedulers.

For a practically meaningful benefit, preregister a two-percentage-point minimum difference in old-task retention. A positive superiority conclusion needs both the observed improvement and a seed-clustered interval excluding zero. Practical equivalence requires an appropriately narrow interval within ±2 points. Anything between is inconclusive, not proof of equality.

Twelve seeds per arm cost approximately 9 GPU hours, plus analysis. This would be decisive for the local setup, not incontestable across FOREVER's original benchmarks. Those benchmark claims require their data and evaluation, which this laptop experiment has not reproduced.

### Should a descriptive note appear now?

Not yet, in my judgment. It would be permissible to publish a plainly labelled exploratory note before preregistration, provided all timestamps, deviations, code and negative results were disclosed. But its present contribution is narrowly reconstructive, the LM functional same-cost control is missing, and its likely readership could mistake it for a causal audit of FOREVER.

Compute the LM analogue of C10c from stored probe outputs now, without retraining. Then complete Stage A and decide whether the FOREVER material merits a separate note, preferably with the scheduler comparison. Do not call a post hoc descriptive result confirmatory merely because the later main study is preregistered.

## Q5. Consequences for the Perspective paper's Level 2

The results weaken the empirical motivation for the currently tested parameter metrics, but they do not disprove the abstract possibility of an index of accumulated internal change.

Level 2 defines

\\[ c_e(t)=\sum_k D(S_k,S\_{k+1}). \\]

As mathematics, that is an accumulated path length under a chosen distance. Its interpretation depends entirely on what constitutes the persistent state and why the chosen distance measures meaningful change.

A deeper limitation should be made explicit: parameter-space distances are not generally invariant to function-preserving reparameterisations. For LoRA factors, transformations of the form \\(B\mapsto cB\\) and \\(A\mapsto A/c\\), for nonzero \\(c\\), leave \\(BA\\) unchanged but can alter distances measured on the factors. Thus factor-space \\(\tau\\) is not an intrinsic property of the represented function. This is an algebraic point, not an empirical claim requiring a citation.

I would revise Level 2 in four ways:

1. Withdraw any wording implying that accumulated parameter movement is an intrinsic, representation-independent experiential time. It is coordinate- and metric-dependent.
2. Define \\(c_e\\) as a family of candidate change indices, not a single validated construct. State explicitly that monotonic accumulation does not imply learning, retention, meaning or subjective experience.
3. Distinguish three properties: reconstructibility from cheap observables, incremental prediction of a specified outcome, and usefulness for an intervention. Success on one does not establish the others.
4. Identify the tested parameter-distance candidates as empirically weak for the incremental-information objective, with D1_rel/F6 unresolved. Leave D3 provisional until its same-cost and noise controls are completed.

The phrase “from cheap and weak to costly and valid” should change. Cost does not confer validity. A costly metric can be irrelevant, and a cheap statistic can be sufficient.

The Perspective's core argument about saveable, restorable agents and the absence of unforgeable internal evidence of elapsed external time is logically separate. These experiments neither validate nor refute that argument. They concern a proposed proxy for state change and forgetting, not the metaphysics of experienced time.

## Q6. Strongest red-team case and the missing control

The strongest hostile interpretation is that the project has mostly measured consequences of its own optimizer and simulator.

For D1, D2 and \\(\tau\\), the clocks are deterministic summaries of applied parameter updates. Their relationship to optimizer moments is expected, even if reconstructing them from a few scalar summaries is not an exact algebraic identity. High \\(R^2\\) may therefore be a successful engineering approximation rather than a discovery about learning.

For D3, the observation of output changes is also unsurprising. The reference probes already expose model behaviour. With label-noisy distractors, distributional drift could make D3 look exceptional merely because it measures more of the predictive distribution than C10c.

The test data are highly structured, the number of independent runs is small, and no clock–forgetting association has been tested. The LM results have not demonstrated a replay benefit for any clock.

The single most important missing control for the remaining positive hypothesis is a new-seed, schedule-matched clean-versus-noisy distractor experiment, evaluated against a complete same-cost functional baseline. Without it, the D3/F6 exception cannot be separated from the simulator's distinctive noise mechanism.

The feature-provenance audit is equally necessary for interpreting the reconstruction report, but it addresses a different risk: possible circularity in the negative results.

## Q7. Direction — B, with a precise modification

I reject A because unrestricted confirmation across the four families spends effort on candidates already highly reconstructible. I reject C because R3 leaves a genuine D1_rel/F6 reconstruction exception, and the D3/F6 effect has not survived a matched design. D would be justified only if that targeted test revealed a new mechanism requiring a different research question.

Choose B: modify restructured Stage A into one bounded, preregistered falsification study. Make reconstruction and same-cost functional competition primary; retain H1 only conditionally for D3, with D1_rel/F6 as a secondary anomaly audit. Add the four-condition matched-noise comparison above, explicit feature provenance, and independent seed-level splits. Do not expand the candidate list or begin Stage B. Treat the LM arm as descriptive, use bf16 for reliable applied updates, and defer publication of the FOREVER note until Stage A is concluded.

The result will matter only if a functional clock demonstrates reproducible incremental prediction against strong same-cost rivals, preferably beyond one noise schedule. Otherwise the line should close with a transparent negative report. That outcome is scientifically usable; it is not a reason to invent another clock.

DIRECTION: B - Continue a narrowed Stage A with matched-noise falsification; retain D1_rel/F6 only as a bounded secondary reconstruction check.

DECISIONS: 1: R; 2: yes; 3: postpone; 4: fully; 5: before; 6: bf16; 7: yes; 8: after Stage A

DECISIVE TESTS:

1\. Baseline-provenance and reconstruction audit.\
Hypothesis: D1, D2 and \\(\tau\\) remain reconstructible without direct clock-derived features, across short windows and optimizer resets.\
Pass/fail: Pass if held-out reconstruction \\(R^2\geq0.90\\) for the eligible baseline on fresh splits in the declared primary window range, with transition-stratified errors reported. Fail if the result depends materially on prohibited direct proxies or cannot generalise to held-out runs.\
Cost: Approximately 1–2 CPU hours of analysis; no new training, assuming stored per-step logs suffice.

2\. Matched-noise D3/F6 confirmation.\
Hypothesis: D3 contains outcome-relevant information beyond B_strong and same-cost functional competitors under noisy interference.\
Pass/fail: Pass if reconstruction remains below \\(R^2=0.90\\) and incremental forgetting prediction reaches \\(\Delta R^2\geq0.02\\) with seed-clustered uncertainty excluding zero in both noisy F6 variants, plus a positive transfer result in noisy F2. Otherwise fail the stated generalisable claim. Evaluate D1_rel reconstruction secondarily on the same fresh runs; do not reopen parameter-clock H1 without a separate locked protocol.\
Cost: 80 runs / 12.3 per hour ≈ 6.5 CPU hours, plus approximately 2 hours of analysis.

3\. Language-model same-cost functional audit.\
Hypothesis: D3's apparent residual is not simply a consequence of comparing a full-output metric with weak scalar telemetry.\
Pass/fail: Pass as evidence of distinct information only if D3's held-out reconstruction remains below 0.90 against C10c and the preregistered same-pass functional summaries; otherwise close that LM residual claim. No H1 inference from this descriptive reanalysis.\
Cost: Approximately 0.5–1 CPU hour using stored probe outputs; no GPU training.

4\. FOREVER scheduler counterfactual.\
Hypothesis: \\(\tau\\)-driven replay achieves materially better old-task retention than moment-driven and schedule-only clocks under a matched replay budget.\
Pass/fail: Require meaningful trigger separation first. Superiority passes if the gain is at least two percentage points with a paired interval excluding zero; practical equivalence passes only if the relevant interval lies within ±2 points. Otherwise report inconclusive, not equivalence.\
Cost: 36 paired-arm runs × 15 minutes ≈ 9 GPU hours, plus approximately 1 hour of analysis; defer until after Stage A.

MISSING CONTROL: Fresh-seed, schedule-matched clean/noisy distractors with a full same-cost functional competitor set, including C10c.

CONFIDENCE: medium - The high reconstruction results are credible within the tested regimes, but the F6 exception rests on too few independent runs, and no clock has yet demonstrated incremental prediction of forgetting.