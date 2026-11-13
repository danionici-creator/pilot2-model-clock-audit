# Pilot 2 — Technical Protocol (Draft for External Review)

**Working title:** *Does an Agent's Own Change Keep Time? Testing an Experiential Index of Adaptation Against Clocks, Counts, and Logged Update Summaries*

**Author:** Ioan Daniel Ionici (Independent Researcher, Oradea, Romania; ORCID 0009-0009-8183-3656)  
**Status:** draft protocol **v0.2**, 27 October 2026 (citations updated 1 November 2026; no change of design). Not frozen. To be frozen, hashed (SHA-256), and deposited on Zenodo before any main run. v0.2 revises v0.1 after an AI review (Google Argon) and an AI analysis of that review (Copilot); every change and every rejected suggestion is listed in §19.  
**Builds on:** Ionici (2026), *A Time of Their Own* v1.3, §4 and Level 2 of Table 2, https://doi.org/10.5281/zenodo.23847648; method of Ionici (2026), *Does Explicit Episode–Trace Binding Help?* v1.3, https://doi.org/10.5281/zenodo.23847602; code base https://doi.org/10.5281/zenodo.23847723.

---

## 0. Position within the research programme (context for the reviewer)

This protocol is the empirical continuation of two published works by the same author. Neither is under review here. They are summarised so that every design decision below can be traced to its source.

### 0.1 The Perspective: what is to be tested

*A Time of Their Own* (v1.3) argues the following:
- **The problem.** A persistent artificial agent whose complete state can be saved and restored holds no evidence about elapsed time or about its own change that it could not have been given, reset, or forged together with that state.
- **The classification.** It classifies the temporal evidence available to an agent (order, duration, sequential computation, continuity, and its own change) by who can write, reset, forge, or copy it, and by whether the agent's self-model can read it.
- **Two roles that must be kept apart:**
  1. A **continuity anchor**: a non-restorable time reference c_a and a state-bound operation counter N, read through a trusted path. It detects and distinguishes suspension and restoration (Level 4 of its programme).
  2. A **dual clock**: an **experiential index** c_e(t) = Σ_{τ<t} D(S(τ), S(τ+1)), accumulated change of the agent's persistent state S, read against c_a. It serves the agent's model of its own adaptation (Level 2). The index is non-decreasing, is updated online at constant cost, and is distinct from the net displacement D(S(t₀), S(t₁)). The choice of D is declared an open problem.
- **Admissibility of D.** A candidate D is admissible only if it:
  - (a) beats decoders restricted to within-episode (local) update statistics;
  - (b) survives the reset criterion and randomisation of episode order, where it is meant to reflect history;
  - (c) predicts a later functional consequence better than event counts and logged update summaries;
  - (d) is used by the agent rather than merely decodable from it.
- **Test programme.** Six levels (time reference, experiential index, history, discontinuity, closed-loop use, temporal self), each paired with the conventional competitor that can close it. A level is **closed** if its competitor is non-inferior on the level's primary metric within a margin fixed in advance and no worse on any declared cost dimension; a mixed trade-off is reported as unresolved, neither closing the level nor supporting the hypothesis. The Perspective states that each level needs its own evaluation contract; this protocol is that contract for Level 2. The primary metric of Level 2 is **predictive validity per unit of storage**.
- **Stance on outcomes.** Equivalence with the competitor is a legitimate negative result, and *functional separation* (the platform suffices, and agent-held evidence is unnecessary) is a possible outcome of the programme. The Perspective offers its tests to others; versions 1.0–1.2 also stated that its author did not plan to pursue them. This study is a declared change of that plan.

**This protocol tests Level 2 only:** whether c_e, under some admissible D, is worth holding.

### 0.2 The closed study: how it is to be tested

*Does Explicit Episode–Trace Binding Help?* (v1.3, closed) asked whether binding an episode record to a summary of the internal change it produced (arm D) helps a model attribute the episode's source (own, imported, or inferred), compared with an information-matched control that receives the same streams without the binding (arm F). The model was a small Transformer self-model reading the traces of a plastic agent. Over five exploratory iterations:
- **The apparent advantage was a control failure.** Generic controls failed to use the trace, which produced a large but uninformative advantage for D (+0.38 Brier skill score). When the control was made competent (87% of a decoding ceiling), D − F was +0.002 BSS, with descriptive equivalence under a ±0.05 BSS margin.
- **The signal was local, not historical.** Decoder diagnostics showed that the source was carried by **local update statistics**, and that resetting the state before each episode did not reduce decodability. The benchmark therefore did not test attribution from path-dependent history.
- **A shortcut caused the apparent reversal.** With 32 episodes per window, an apparent reversal between objectives was traced to a shortcut in how one objective was applied, and removing it repaired the reversal.

**What carries over is the method,** not a result: an information-matched control, a competence audit of the control, a decoding ceiling, a reset criterion, equivalence tests (TOST) with a prespecified margin, the distinction between onset (whether learning starts) and skill (performance once learned), reliance versus necessity, frozen and hashed configurations, and a per-run inventory.

**What carries over as a warning:** local update statistics can impersonate accumulated history, and an under-specified control can manufacture an advantage. This is why competitor C6 is mandatory and why the baseline is deliberately strong (§7).

### 0.3 Why Level 2, and why not the continuity anchor

An earlier internal draft of Pilot 2 tested the continuity anchor (Level 4) in simulation. It was abandoned. With a simulated anchor that is deterministic by construction, classifying suspension against restoration reduces to comparing two counters. A raw anchor can then beat an information-matched adjudicated flag only where the flag is absent, which is an argument about availability, not an empirical finding.

Level 2 is different: whether c_e predicts the agent's own forgetting depends on the actual learning dynamics of the network, so the outcome is not fixed by the design.

**Prior work with the same index.** Feng et al. (2026, FOREVER, ACL 2026, arXiv:2601.03938) define a "model-centric time" as the cumulative L2 norm of parameter updates, τ_t = Σ_{i≤t} ‖Θ_i − Θ_{i−1}‖₂ on LoRA weights. This is c_e^{D1} (their τ is reset at each new task). They use it to schedule replay at forgetting-curve intervals, with models from 0.6B to 13B parameters. Their only ablation of the time signal is against step counts; learning-rate-based and gradient-norm-based signals are not tested. Priority for the use of accumulated update magnitude as a model clock for replay therefore belongs to FOREVER, and this study claims no novelty for the index itself.

**What this study adds** is an audit of identification: whether such an index carries information beyond the union of cheap online competitors that could reconstruct it (§7), under a placebo that destroys its temporal alignment (G4) and under an adversarial stream with much change and little interference (F6). If the answer is equivalence, the benefit attributed to a model-centric clock is reproducible from elementary optimizer statistics; if it is superiority, the clock carries information of its own. Both outcomes bear directly on that line of work. Forgetting prediction more generally also exists (§18).

### 0.4 Content, not provenance

In the Perspective, the difference between agent-held evidence and logged update summaries is partly one of **provenance**: who writes, holds, and can reset or forge the evidence. In a simulation every quantity is computed by the same code, so provenance cannot differ between predictors. **Stage A therefore tests content only**: whether the number c_e carries predictive information that the other cheap numbers do not. For parameter-space distances (D1, D1_rel, D2), c_e is itself a cumulative update summary; H1 then asks whether *this* summary beats the strongest set of *other* cheap summaries. Claims about provenance are outside the scope of this study.

### 0.5 Traceability of design decisions

| Design decision | Source |
|---|---|
| Definition of c_e; distinction from displacement; D as open problem | Perspective §4 |
| Q1–Q4 and the mapping to criteria (a)–(d) | Perspective §4 (admissibility) |
| Confirmatory baseline B_strong; descriptive B_standard | Perspective §5 (a level closes if the competitor matches); closed study (control competence); review v0.1 (§19) |
| Competitor C6 (local update statistics) | Closed study: main diagnostic finding |
| Primary metric: validity per unit of storage (H2) | Perspective §5, Level 2 |
| Three-way outcomes (supported, equivalent, inconclusive) and TOST | Perspective (equivalence as a legitimate result); closed study (equivalence margins) |
| Ceiling G1, competence G3, onset versus skill G6, reliance G8 | Closed study, method; Perspective §6 |
| Frozen configurations, hashes, inventory, bit-identical reruns G7 | Closed study and its code archive |
| Competitors C1, C5b–C5d, C8, C8b, C9 | External literature on forgetting and consolidation (§18) |
| Stage C on pretrained language models | Perspective (claims concern persistent agents, not toy worlds) |

### 0.6 What the reviewer is asked to evaluate

Only this protocol: whether its design can deliver an interpretable answer to Q1–Q4 at the stated scale. The claims of the Perspective and the results of the closed study are published and are not under review.

### 0.7 Glossary

| Term | Meaning |
|---|---|
| S, θ | Persistent state of the agent; its parameters |
| m, v; m̂, v̂ | Adam first and second moments; bias-corrected values |
| c_a | Elapsed time in ticks (§4.5) |
| N, N(t) | Committed optimizer steps; their count at time t |
| c_e^D | Experiential index: accumulated D-change of S |
| ρ̄ | Mean interval rate Δc_e / ΔN; the only information in c_e beyond counts (§2) |
| Disp^D | Net displacement D(S(t₀), S(t₁)) |
| √JS | Jensen–Shannon distance, base-2 logarithm, in [0, 1] (a metric) |
| m_ch | Chunk stride, in optimizer steps, for chunked distances (§5) |
| L_reh | Length of one rehearsal segment (§9) |
| B_standard | Descriptive baseline: standard telemetry (§7) |
| B_strong | Confirmatory baseline: all cheap competitors (§7) |
| SESOI | Smallest effect size of interest |
| TOST | Two one-sided tests (equivalence) |
| MET | Minimal-effect test: lower confidence bound above the SESOI |
| BSS | Brier skill score (used in the closed study) |
| Gate | A prespecified validity check; failing it changes how a result may be reported |

---

## 1. Research question

Let a Transformer learn continually from a non-stationary stream of tasks. Let

  c_e(t) = Σ_{τ<t} D(S(τ), S(τ+1))

be its *experiential index*: the accumulated change of its persistent state S under a distance D. It is a non-decreasing scalar held by the agent.

**Storage.** Maintaining c_e costs **one running scalar**. Answering a query about task k needs the snapshot c_e(t₀,k) taken at its last exposure: **one scalar per tracked task exposure**, at most K + 1 scalars for K active tasks (here K ≤ 40). This is O(1) per update and O(K) for queries, against a full snapshot per task for displacement (§5.2).

**Q1 (predictive validity).** Does Δc_e over an interval (t₀, t₁] predict the agent's forgetting of a task last trained at t₀ better than a strong set of cheap online competitors: elapsed time; step, token, and event counts; cumulative learning rate and loss; logged gradient summaries, including learning-rate-weighted ones; optimizer and parameter-state norms; local (within-window) update statistics; and the loss change on a fixed reference battery?

**Q2 (storage efficiency).** How much of the predictive value of the full net displacement D(S(t₀), S(t₁)), which requires storing a snapshot at t₀, does the scalar c_e retain?

**Q3 (path dependence; secondary).** Under a fixed multiset of experiences, do order-induced differences in forgetting track order-induced differences in Δc_e?

**Q4 (use).** Does a rehearsal scheduler that uses c_e outperform budget-matched schedulers that use the competitors, and does its advantage depend on the actual c_e stream rather than on a placebo stream?

The admissibility criteria for D stated in *A Time of Their Own* §4 map onto these questions:

| Criterion | Question |
|---|---|
| (a) beats decoders restricted to local update statistics | Q1, competitor C6, gate G5 |
| (b) order sensitivity where history matters | Q3 (secondary, §10.3) |
| (c) predicts a functional consequence better than counts and logged summaries | Q1 |
| (d) used by the agent rather than merely decodable | Q4, gate G8 |

**Scope restriction on criterion (b).** The reset criterion is **not applicable** to the target used here: resetting S(t₀) would erase the task whose forgetting is measured. Only order sensitivity is examined, and only as a secondary hypothesis. The rate of change ρ(τ) still depends on the whole prior history through S(t₀); this is why absolute run progress N(t₀) and state norms at t₀ are covariates (§7).

## 2. Identification note (read first)

Within a run, at a fixed evaluation time t₁, the ranking of tasks by Δc_e = c_e(t₁) − c_e(t₀,k) is identical to their ranking by t₁ − t₀,k, the time elapsed since their last exposure (ties occur where D = 0, for example during idle intervals). The reason is that c_e is non-decreasing. A global scalar index therefore carries **no task-specific ordinal information at a fixed time**.

It does carry **cardinal** information: the spacing between two tasks' values, c_e(t₀,k) − c_e(t₀,j), equals the change accumulated between their exposures, which varies with the rate ρ(τ) = dc_e/dN. All information that c_e carries beyond counts lies in this **temporal variation of its rate**: some intervals of equal length contain more change than others. Three consequences follow:
1. Q1 is identifiable only to the extent that the interval rate ρ̄ = Δc_e / ΔN varies across intervals and is not reconstructible from the baseline. Gate G2 checks this on the rate, not on the raw increment, because the raw increment is dominated by interval length.
2. A scheduler that *selects which task to rehearse* by ranking tasks on Δc_e since their last exposure is equivalent to least-recently-rehearsed. Q4 must therefore test *when*, and *how much*, to rehearse (allocation over time), or use c_e together with task covariates inside a learned predictor (§9).
3. c_e is not task-specific memory. It cannot by itself encode which tasks a stretch of change interfered with (§10.3).

## 3. Agent

| Component | Specification |
|---|---|
| Architecture | Decoder-only Transformer, 4 layers, d_model = 128, 4 heads, d_ff = 512, pre-LN, GELU, learned positional embeddings, maximum context 64, vocabulary 512 tokens. Input embedding and output head **untied**; biases in all linear layers and LayerNorms. ≈ 0.93 M parameters (exact count recorded at Stage 0) |
| Sequences | One example per sequence, no packing; sequence length equals example length (4–6 tokens); padding to the batch maximum with masked loss |
| Optimizer (primary) | AdamW, β = (0.9, 0.999), ε = 1e-8, weight decay λ = 0.01, global gradient clipping at norm 1.0 applied immediately before `optimizer.step()`. m and v see the clipped gradient g̃ |
| Optimizer (robustness arm) | SGD with momentum 0.9, same clipping, learning rate and weight decay frozen at Stage 0. A passive EMA v_τ = 0.999 v_{τ−1} + 0.001 g̃_τ² is maintained so that D2 is defined; it does not affect the update |
| Persistent state S | Parameters θ and optimizer moments (m, v); distances are computed on θ |
| Logged per step | ‖g_τ‖₂ (raw) and ‖g̃_τ‖₂ (clipped); η_τ; batch size B_τ; training loss L_τ; ‖Δθ_τ‖₂ before and after the decoupled weight-decay term; ‖m̂_τ‖₂ |
| Precision, device, determinism | float32 on CPU; `torch.use_deterministic_algorithms(True)`; fixed seeds for data, initialisation, and dropout (dropout = 0 in the primary arm). Each run is a **single-threaded worker** (`torch.set_num_threads(1)`, `torch.set_num_interop_threads(1)`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`); eight workers run in parallel |
| Software | Python 3.14.6, PyTorch 2.13.0 (CPU build), NumPy 2.5.1, scikit-learn 1.9.0, as installed at drafting; exact versions are re-recorded in `environment.txt` at freeze |

## 4. World and streams

### 4.1 Task types and vocabulary

- **Fact tasks.** Task k is a set of 256 key→value pairs. The input is `[TASK_k] [KEY] →`, and the target is a single `[VALUE]` token. Keys are drawn from a target key pool P_target, and the overlap between tasks is controlled by a pool-sharing parameter π_overlap. Values are drawn uniformly from V value tokens. Fact probes are **trained items**: they measure in-sample associative retention.
- **Rule tasks.** Task k is an algorithmic map y = (a_k·x + b_k) mod m_k, with m_k ≤ 64 so that y is a single value token. The input is `[TASK_k] [D1] [D2] →`, where x ∈ [0, 1023] is written as two base-32 digit tokens. Probe inputs are held out from training: rule probes measure held-out algorithmic generalisation.
- **Reference tasks.** A fixed set of fact and rule tasks, trained only during the childhood phase. They are never targets. They supply the reference battery R (§5) and the behavioural battery B_beh. Their keys come from a pool P_ref disjoint from P_target, and their rule moduli are not used by any target task.
- **Vocabulary partition** (frozen at Stage 0; indicative): 64 task tokens, P_target and P_ref key tokens (with multi-token keys if more keys are needed), 64 value tokens, 32 digit tokens, and special tokens, in total ≤ 512.
- **Exposure.** Every training, re-exposure, and rehearsal segment iterates over balanced permutations of the task's items (full epochs), so that every item of halves A and B has the same exposure count and comparable recency at the end of a segment.

### 4.2 Probes

Each target task has a probe set: its 256 facts (fact tasks) or 256 held-out inputs (rule tasks). The probe set is split **once, at task creation**, into disjoint halves A and B of 128 items each.
- **Half A** supplies the confirmatory target T1.
- **Half B** supplies the competence covariates at t₀, the inclusion criterion, the reliability ceiling (with A), and the Stage B retention target T3.

No probe item belongs to R or to B_beh. All probe losses and probabilities are read at the single answer position after `→`; cross-entropy is in nats.

### 4.3 Run structure

| Phase | Steps | Content |
|---|---|---|
| Childhood | exactly 3,000 | Reference tasks. Gate: reference accuracy ≥ 0.95 at the end; a run that fails is replaced and counted |
| Life | ≈ 20,000 | ≈ 40 target tasks, presented according to the stream family; rehearsal segments, re-exposure segments, and idle intervals according to the family |
| Evaluation | — | Probes of every learned task are evaluated at the end of every segment and on a grid every 200 optimizer steps |

All segment lengths and the evaluation grid are integer multiples of 50 optimizer steps, so that chunk boundaries (§5) never fall inside a segment.

### 4.4 Stream families

| Family | Generator | Intended decoupling | Role |
|---|---|---|---|
| **F1, natural** | New task every fixed number of steps, fixed segment length, round-robin rehearsal, constant LR, fixed batch | None | Positive control: counts are expected to suffice |
| **F2, variable novelty** | New tasks interleaved with re-exposure to already-mastered data in random amounts; batch size ∈ {16, 32, 64} per segment | Steps and tokens decouple from change | Pooled |
| **F3, LR schedule** | Cosine annealing with warm restarts at random times | Steps decouple from change; LR-weighted summaries are strong competitors | Pooled |
| **F4, idle** | Random idle intervals with no updates; c_a advances, θ is frozen | Only elapsed time decouples (C1–C7 stop with c_e) | Sanity check only; **not pooled** into H1 |
| **F5, held-out** | Mixture of the F2–F3 generators with a different proportion of rule tasks, a different π_overlap, and idle intervals | Generalisation across generator parameters | Never used for fitting or selection; test only; reported alone |
| **F6, adversarial** | Target exposures at a regular rate, interleaved with variable-length distractor segments on a disjoint distractor pool (P_distractor ∩ P_target = ∅) with label noise 0.3 and batch size 16, under the same optimizer configuration | High parameter change with little interference: favours the competitors | Never used for fitting or selection; test only; reported alone |
| **O, order blocks** | Designed blocks (§10.3) forked from one saved state | Path dependence | H3 only; **not pooled** into H1, H2, H4 |

F5 is built from the F2–F3 generators, so it tests generalisation across generator parameters, not freedom from designed decoupling. F6 tests the converse regime that F2–F5 lack: much movement, little forgetting. Scale-drift interventions (weight-decay pulses, rescaling of pre-LN weights) are exploratory robustness checks only, because they have no counterpart in ordinary training. Generator parameters for each family are frozen with the protocol.

### 4.5 Time

c_a counts *ticks*. Each optimizer step adds 1 tick; each idle interval adds its length in ticks; evaluations add 0 ticks. Without idle intervals c_a equals N. All interval sums in §7 run over committed optimizer steps τ ∈ (N(t₀), N(t₁)], so idle ticks contribute nothing to them.

## 5. Distances D and the index c_e

### 5.1 Candidate distances

| D | Definition | Evaluated |
|---|---|---|
| **D1** | ‖θ(τ+1) − θ(τ)‖₂ | Every step |
| **D1_rel** | ( Σ_ℓ ‖Δθ^(ℓ)(τ)‖₂² / (‖θ^(ℓ)(τ)‖₂² + 10⁻¹²) )^{1/2}, layer-wise, with Δθ taken **before** the decoupled weight-decay term | Every step |
| **D2** | ( Σ_i v̂_i(s) (Δθ_i(τ))² )^{1/2}, with v̂(s) the bias-corrected second moment **frozen at the start s of the current segment** | Every step |
| **D3** | Mean over x ∈ R of √JS( p_{S(τ)}(·\|x), p_{S(τ+m_ch)}(·\|x) ) at the answer position, \|R\| = 256 | Every m_ch steps (chunked) |
| **D4** (secondary) | √(1 − linear CKA) of final-layer answer-position representations on R (Kornblith et al. 2019) | Every m_ch steps (chunked) |

**Why D2 uses a lagged curvature.** Under Adam, Δθ_i ≈ −η m̂_i / √v̂_i. Weighting by the *current* v̂ therefore cancels the preconditioner: Σ_i v̂_i(τ) Δθ_i(τ)² ≈ η_τ² ‖m̂_τ‖₂², so a same-step D2 would be the learning-rate-weighted momentum norm, a logged optimizer summary. The segment-lagged weighting avoids exact cancellation; whatever remains of the relation is controlled by competitor C5d (§7).

**Why D1_rel.** In a pre-LN Transformer, some weight rescalings change ‖θ‖ without changing the function, and AdamW shrinks θ at every step independently of the data. D1_rel removes both scale effects; raw D1 is kept for comparison.

- c_e^D(t) = sum over steps (D1, D1_rel, D2) or over chunks (D3, D4) up to t. Chunks are indexed by committed optimizer steps.
- √JS is a metric, so the chunked D3 sum is a lower bound on the per-step sum. √(1 − CKA) is the chordal distance between centred Gram matrices and also satisfies the triangle inequality.
- **Chunking control.** On calibration runs, chunked versions of D1, D1_rel and D2 at the same stride m_ch are computed alongside the per-step versions, so that a difference between D3 and D1/D2 cannot be produced by temporal smoothing alone. Sensitivity: m_ch ∈ {1, 5, 10, 20, 50} on 5 calibration runs (m_ch = 1 over a 2,000-step window). m_ch = 10 is adopted if, for D3, the within-run Spearman correlation between Δc_e at m_ch = 1 and m_ch = 10 across intervals is ≥ 0.98 and their ΔR² differ by ≤ 0.01; otherwise m_ch = 5 (with \|R\| reduced to 128 if needed for cost).
- **Stationarity check of R.** Because R is never retrained after childhood, the sensitivity of D3 may decay as R is forgotten. On F1 calibration runs, the mean D3 rate in the fourth quartile of the life phase must be within ±20% of the first quartile. If not, a fixed maintenance rehearsal of R (one batch every 500 steps, in all families) is added before freeze.
- **D\*** is the single D used in the confirmatory tests. It is chosen among D1, D1_rel, D2 and D3 on calibration runs as the one with the largest incremental validity over B_strong (§7), and is frozen before any test run.

### 5.2 Net displacement and its storage

Disp^D(t₀, t₁) = D(S(t₀), S(t₁)), evaluated at grid points. The cached object per active task exposure is:

| D | Cached at t₀ | Numbers per t₀ |
|---|---|---|
| D1, D1_rel | θ(t₀) (and layer norms) | ≈ 0.93 M |
| D2 | θ(t₀) and v̂(t₀) (Fisher weight anchored at t₀, as in EWC) | ≈ 1.9 M |
| D3 | answer-position output distributions on R | 256 × 512 ≈ 0.13 M |
| D4 | final-layer answer-position representations on R | 256 × 128 ≈ 0.03 M |

A snapshot of task k is overwritten at its next exposure, so at most K ≤ 40 snapshots are active. Storage ratios in H2 are reported per D (of order 10⁻⁵ to 10⁻⁶ in Stage A).

## 6. Targets

**T1 (primary): forgetting.** For each target task k and each exposure segment of k (training, re-exposure, or rehearsal) ending at step s₀, let t₀ be the evaluation immediately after s₀. For every evaluation time t₁ > t₀ strictly before the first step of the next segment that trains k:

  F_k(t₀, t₁) = L̄_A,k(t₁) − L̄_A,k(t₀),

where L̄_A,k is the mean cross-entropy on probe half A of task k.
- **Inclusion:** a triplet is included only if the probe-**B** accuracy of task k at t₀ is ≥ 0.90, and ΔN = N(t₁) − N(t₀) ≥ 50 (or Δc_a ≥ 50 ticks where no step is taken). Excluded triplets are counted and reported by reason.
- **Unit of observation:** the triplet (k, t₀, t₁). **Unit of inference:** the run.
- **Weighting:** each exposure episode (k, t₀) carries equal total weight within its run: w = 1 / (E_r · M_{r,k,t₀}), where E_r is the number of valid episodes in run r and M_{r,k,t₀} the number of evaluation times of that episode. The same weights are used in model fitting (`sample_weight`) and in R²_r.

**T1-acc (secondary): bounded forgetting.** ΔAcc_A,k = Acc_A,k(t₀) − Acc_A,k(t₁) on the same triplets. It checks that an effect on T1 reflects functional forgetting rather than logit-scale drift. The H1 statistic is reported for T1-acc descriptively.

**T2 (secondary): behavioural drift.** The √JS distance between the outputs of S(t₀) and S(t₁) on B_beh. It is reported descriptively. T2 is structurally favourable to Disp^{D3}, so it is not used for confirmatory claims.

**T3 (Stage B): retention.** The time-averaged probe-B accuracy over all learned tasks during the life phase, at a fixed rehearsal budget.

## 7. Predictor sets and competitors

All interval quantities are sums over τ ∈ (N(t₀), N(t₁)]. Every competitor is agent-available online and costs ≤ 2 stored scalars per t₀.

**Covariates X_cov, given to every model** (agent-observable only):
- task type (fact or rule);
- L̄_B,k(t₀) and Acc_B,k(t₀) (competence at t₀, from half B);
- L̄_B,k at the start of the exposure segment ending at s₀ (prior mastery, a proxy for novelty);
- input-token overlap of task k with the agent's history: 1 − √JS(q_k, q_hist(t₀)), where q_k is the task's input-token unigram distribution and q_hist(t₀) the cumulative input-token histogram up to t₀ (one 512-length counter);
- N(t₀), absolute run progress; N(t₀) − N(t_first,k), task tenure; number of prior exposures of k; number of active learned tasks K_active(t₀);
- ‖θ(t₀)‖₂ and √Tr v̂(t₀).

The generator parameter π_overlap is **not** a covariate: it is world metadata (see C8).

**B_standard** (standard telemetry; descriptive only):

| Code | Predictor over (t₀, t₁] | Source |
|---|---|---|
| C0 | Δc_a, elapsed ticks | wall clock |
| C1 | ΔN, with the fixed basis {ΔN, log(ΔN + 1), log(ΔN + 10), log(ΔN + 100)} | shifted power law of Kalajdzievski (2024), arXiv:2401.05605 |
| C2 | Δ tokens | data volume |
| C3 | Σ η_τ | cumulative learning rate |
| C4 | Σ L_τ | cumulative training loss |
| C5 | Σ ‖g_τ‖₂ (raw) | logged gradient norm |
| C7a | number of segment boundaries and of agent-triggered rehearsals | agent-observable event counts |

**B_strong** (confirmatory baseline) = X_cov ∪ B_standard ∪:

| Code | Predictor over (t₀, t₁] | Source |
|---|---|---|
| C5a | Σ ‖g̃_τ‖₂ (clipped) | gradient actually used by the optimizer |
| C5b | Σ η_τ ‖g_τ‖₂, Σ η_τ ‖g̃_τ‖₂, Σ η_τ L_τ | within-step products that interval sums cannot recover |
| C5c | Σ η_τ² ‖g̃_τ‖₂², Σ \|⟨g̃_τ, Δθ_τ⟩\| | squared-gradient accumulator; path-integral work of Synaptic Intelligence (Zenke et al. 2017) |
| C5d | Σ η_τ ‖m̂_τ‖₂ | learning-rate-weighted momentum norm (the same-step D2 identity, §5.1) |
| C2b | Σ η_τ / B_τ | noise-scale-weighted steps |
| C6 | mean and SD of ‖Δθ_τ‖₂ over the first W_eff and the last W_eff steps of (t₀, t₁], with W_eff = min(20, ⌊ΔN/4⌋), windows clamped inside the interval | local update statistics (closed study; criterion (a)) |
| C6b | Δ‖θ‖₂ and Δ√Tr v̂ over the interval | state-scale drift |
| C10 | L_R(t₁) − L_R(t₀): change of the mean loss on the reference battery R | canary loss; 1 stored scalar per t₀ |
| rates | ΔN-normalised versions of C2–C5d and C10 (Z / max(ΔN, 1)) | computed, not stored |

**Why two baselines.** B_strong is deliberately close to a reconstruction of c_e from cheap telemetry, so that a positive H1 cannot be explained by an omitted product of learning rate and gradient, by momentum, by weight decay, by norm drift, or by local statistics. Claimed advantages over under-trained baselines often vanish when the baseline is trained properly (Mukhoti et al. 2018); the closed study documented the same failure for an information-matched control. B_standard is reported so that readers can see how much of any gap is closed by the specialised competitors. If c_e beats B_standard but not B_strong, the result is reported as *reconstructible from cheap telemetry*, not as support.

**Reference predictors** (not agent-available, or of high storage; used to bound, not to compete; exploratory):

| Code | Predictor | Storage |
|---|---|---|
| C7b | separate counts of new-task and re-exposure segments (oracle labels) | world metadata |
| C8 | Σ over intervening tasks j of key overlap(k, j) × steps on j; for rule tasks, overlap is the Jaccard overlap of input-token sets | world metadata (Lee, Goldt and Saxe 2021, arXiv:2107.04384) |
| C8b | Disp^{D2}(t₀, t₁) with v̂(t₀), Fisher-weighted displacement (EWC: Kirkpatrick et al. 2017) | ≈ 1.9 M per t₀ |
| C9 | First-order response ⟨∇_θ L_train,k(S(t₀)), θ(t₁) − θ(t₀)⟩, with the gradient computed on task k's **training items only**, never on probe half A (cf. Su and Zhang 2026; Jin and Ren 2024) | ≈ 1.9 M per task |
| Ceiling | Reliability of the half-A target: within-run correlation r_AB between F_A and F_B on the same triplets, **uncorrected** (the target uses one half) | — |

## 8. Prediction models and competence audit

- **Primary model family:** gradient-boosted regression trees (scikit-learn `HistGradientBoostingRegressor`), `max_features = 1.0`, `max_bins = 255`. Monotone constraints (`monotonic_cst`): +1 for C0, C1 (raw ΔN only), C2, C2b, C3, C4, C5, C5a–C5d, Δc_e, Disp, C8, C8b; 0 for C7a, C6, C6b, C10, all rates, all of X_cov, and the log terms of C1.
- **Secondary model family:** ridge regression on the predictors with log1p applied to raw (non-log) positive interval sums, sign(x)·log(1 + \|x\|) for signed predictors (C6b, C10, C9), interactions with all of X_cov, a `StandardScaler` fitted on training runs, and λ chosen by cross-validation over training runs.
- **Equal tuning budget:** every predictor set receives the same random search, 50 configurations, on validation runs, with the same seeds. The best configuration of B_strong is always included as a candidate for B_strong + c_e. The **locked-hyperparameter** ΔR² (both sets fitted with the B_strong configuration) is the confirmatory statistic; the re-tuned ΔR² is reported alongside.
- **Fitting:** models are fitted on pooled, weighted triplets from the training runs and evaluated on test runs. No test-run information is used in fitting, selection, or transformation. Training-split variability is assessed by 5-fold cross-fitting over training runs (the five fitted models are averaged); a full two-sample bootstrap (resampling training and test runs, with refitting) is run for the ridge model as a sensitivity analysis.
- **Skill per test run r:** weighted R²_r = 1 − SSE_r / SST_r, with SST_r around the weighted mean of run r. Weighted Spearman ρ_S,r and MAE_r are reported alongside.
- **Decomposition (reported, not confirmatory):** within-episode skill, with SST computed around the mean of each episode (k, t₀) across its t₁; and partial skill [SSE_r(B_strong) − SSE_r(B_strong + c_e)] / SSE_r(X_cov).

## 9. Stage B: use by the agent

Stage B is run only if H1 is supported (§10.1).

- **Budget.** The rehearsal budget is fixed per run: K_reh = Q / L_reh rehearsal segments of L_reh = 50 steps over the life phase. The budget is a **hard cap**, and every scheduler spends exactly Q on every run (asserted per run; gate G7).
- **Pacing.** Threshold schedulers use an online pacing rule: θ_eff(N) = θ_cal · [(K_reh − k_spent(N)) / K_reh] / max(ε, (N_life − N) / N_life), with θ_cal calibrated on validation runs. When the remaining life steps fall to the remaining budget, all remaining rehearsals are executed (terminal flush). The same pacing rule is applied to every threshold scheduler.
- **Schedulers.** By the identification note (§2), schedulers differ in **when** they spend the budget, and in which task only through a learned predictor that includes covariates.

| Scheduler | Rule |
|---|---|
| S-uniform | One rehearsal segment every ⌊N_life / K_reh⌋ optimizer steps; task chosen least recently rehearsed |
| S-c_e | Rehearsal triggered when Δc_e^{D\*} since the last rehearsal ≥ θ_eff; task least recently rehearsed |
| S-C2, S-C3, S-C4, S-C5, S-C5b, S-C7a | As S-c_e, with the trigger on tokens, cumulative LR, cumulative loss, gradient norm, LR-weighted clipped gradient norm, or event counts |
| S-pred(B_strong) | A learned forgetting predictor (Stage A model on B_strong) scores every task; rehearse the argmax when the predicted maximum ≥ θ_eff |
| S-pred(B_strong + c_e) | Same, with Δc_e^{D\*} added (information-matched pair) |
| S-oracle | Rehearse the task with the largest true current forgetting on half B (upper bound) |
| S-random | Random times and tasks, same budget |

- **Relation to FOREVER.** With D\* = D1, S-c_e is a trigger on the clock of Feng et al. (2026). An exploratory arm S-FOREVER applies their schedule (replay when c_e^{D1} since the end of a task's training reaches d · τ_day, with τ_day the change over the first 24 steps and d ∈ {1, 2, 4, 7, 15, 30, …}), under the same budget cap and pacing.
- **Comparator selection.** The single best trigger competitor S-C\* is chosen among S-uniform, S-C2, S-C3, S-C4, S-C5, S-C5b and S-C7a on **validation runs**, frozen, and evaluated once on test runs.
- **Online covariates.** In Stage B, competence covariates at t₀ are computed from the loss and accuracy on the last training mini-batches of the segment, not from probes. T3 uses half B only, and no scheduler except S-oracle reads any probe.
- **Placebo for reliance (G8).** Information that is decodable need not be used (Elazar et al. 2021); reliance is therefore tested by intervention. S-c_e and S-pred(B_strong + c_e) are rerun with the c_e stream replaced by a within-run block-permuted stream (§11, G4); a cross-seed yoked stream from the same family, aligned by N, is run as a robustness check.
- **Logged:** realised rehearsal steps per run; Wasserstein distance between the trigger times of S-c_e and of S-C\* (when); task agreement at matched times (which).

## 10. Hypotheses

### 10.1 Decision rules

- **One-sided level:** α = 0.025 per side for every test. Each hypothesis is decided from a single two-sided (1 − 2α_adj) BCa bootstrap confidence interval (10,000 resamples over the resampling unit), where α_adj is the level assigned to it by the procedure below:
  - **supported** if the lower bound is > δ (minimal-effect test);
  - **equivalent** if the whole interval lies within (−δ, δ) (TOST, each side at α_adj; Lakens et al. 2018; for stochastic machine-learning experiments, Knopov and Shvai 2026);
  - **inconclusive** otherwise.
- **Multiplicity (fixed sequence, then Holm).** H1 is tested first at α = 0.025. Only if H1 is supported are H2, H4a and H4b tested, as a Holm family at α = 0.025: ranked by their one-sided bootstrap p-values, the j-th is tested at α_adj = 0.025 / (3 − j + 1). This controls the family-wise error rate. If H1 is equivalent or inconclusive, H2–H4 are not tested confirmatorily and Stage B is not run.
- **SESOI (rule frozen now, value computed on calibration runs and frozen before test):** δ = max(0.02, min(0.05, 0.15 × [ceiling − R̄²_cal(B_strong)])), where the ceiling is r̄_AB from G1. Raw ΔR² and ΔR² as a fraction of the headroom are both reported. Stage B: δ_B = 2 percentage points of T3.

### 10.2 Confirmatory hypotheses

| | Statement | Statistic | Resampling unit |
|---|---|---|---|
| **H1** | Adding Δc_e^{D\*} to B_strong increases held-out skill on T1 | Mean over test runs of the locked-hyperparameter ΔR²_r = R²_r(B_strong + Δc_e^{D\*}) − R²_r(B_strong); test runs from F1, F2, F3, F5, F6. F1, F5 and F6 are also reported alone | test run |
| **H2** | The scalar index retains at least 80% of the displacement's incremental value | Z̄ = mean over test runs of Z_r = ΔR²_r(c_e) − 0.80 · ΔR²_r(Disp^{D\*}). Supported if the lower bound of Z̄ is ≥ 0; equivalent (retention indistinguishable from 80%) if the interval lies within ±0.01. Tested only if G2b passes. The ratio of means and its Fieller interval are reported descriptively | test run |
| **H4a** | c_e helps a covariate-aware rehearsal predictor | Mean paired difference in T3, S-pred(B_strong + c_e) − S-pred(B_strong); SESOI δ_B | Stage B test run |
| **H4b** | c_e suffices as a standalone rehearsal trigger | Mean paired difference in T3, S-c_e − S-C\*; SESOI δ_B | Stage B test run |

### 10.3 Optional exploratory module H3 (path dependence)

H3 is **not** part of the confirmatory study. Its design is preregistered here so that it cannot be tuned after the fact, but it is run only if H1 is supported and the compute budget of §12a remains after Stages A and B (it needs about 120 runs, comparable to the whole Stage A test set). If run, it is reported as exploratory.

The v0.1 design (segments X and Y with high and low key overlap with k) is withdrawn: a global index cannot encode *which* task a stretch of change interfered with, and recency can reverse the sign of the order effect. The redesign varies a **global** property:
- **Blocks.** From one saved state S(t₀) after task k is learned (θ, m, v, data-generator state), two branches are forked. Segment A trains a new task with the same input-token overlap with k as segment B; segment B re-exposes already-mastered data. A two-stage learning-rate schedule (η_high, then η_low) is fixed. Branch 1: A at η_high, then B at η_low. Branch 2: B at η_high, then A at η_low. Steps, tokens, batches, the multiset of examples, Σ η, and C7a are identical across branches.
- **Statement.** Across matched pairs, the order-induced difference in forgetting of k, ΔF, has a positive Spearman correlation with the order-induced difference Δ(Δc_e^{D\*}).
- **Decision (descriptive labels).** Supported if the lower bound of the 95% bootstrap interval (resampling unit: the matched pair) is > 0.20; equivalent if the interval lies within (−0.20, 0.20); not part of the confirmatory family.
- **Comparator.** The same correlation is reported for C5b (Σ η‖g̃‖), which is also order-sensitive. H3 shows that c_e tracks a path effect invisible to order-invariant counts; it does not, by itself, show an advantage over order-sensitive telemetry.

### 10.4 Exploratory, labelled as such

D comparisons beyond D\*; the SGD arm; T1-acc and T2; C7b, C8, C8b and C9 bounds; single-competitor comparisons; B_standard comparisons; scale-drift robustness checks; per-family results other than those named above.

## 11. Gates

| Gate | Check | Criterion | Consequence of failure |
|---|---|---|---|
| G1, ceiling | Within-run correlation r_AB between F_A and F_B on calibration runs, uncorrected | r̄_AB ≥ 0.70 | Increase probe-set size before freeze; report all skills also as a fraction of r̄_AB |
| G2, identifiability | Out-of-sample R² for predicting the interval rate ρ̄ = Δc_e^{D\*} / max(ΔN, 1) from B_strong, with OLS and with GBDT (fitted on training runs, evaluated on test triplets of F2, F3, F5, F6 and of F5 alone) | Both R² < 0.90 | H1 is reported as *not identifiable*, never as equivalence |
| G2b, H2 denominator | Mean ΔR² of Disp^{D\*} over B_strong | Lower bound of its 95% interval > 0.02 | H2 is reported as *not identifiable* |
| G3, competence and headroom | On calibration runs (verified on validation runs): B_strong beats X_cov alone in F1; headroom = r̄_AB − R̄²(B_strong) on F2–F3 | ΔR² ≥ 0.10; headroom ≥ 2.5 δ | Redesign the target or the stream before freeze |
| G3b, baseline saturation | On calibration runs: B_strong re-tuned with a doubled search (100 configurations instead of 50), same seeds for the first 50 | Change in mean R²(B_strong) ≤ 0.01 | The baseline is under-tuned: increase the search budget for every predictor set before freeze; if not achievable, H1 may not be reported as supported |
| G4b, positive control (sensitivity) | On calibration runs only: a synthetic predictor Z carrying known incremental information about T1 is added to B_strong. Z is the out-of-fold residual of T1 given B_strong, mixed with independent noise so that its true ΔR² is 2δ. The full pipeline (weighting, locked hyperparameters, GBDT, bootstrap, decision rule) is applied | Estimated ΔR² within ±0.01 of 2δ, and outcome *supported* | The pipeline cannot detect an effect of the size sought: fix the pipeline before freeze. If it still fails, an *equivalent* outcome of H1 may not be reported as closing Level 2 |
| G4, leakage and placebo | R ∩ probes = ∅ and P_ref ∩ P_target = ∅ (asserted in code); incremental value over B_strong, with locked hyperparameters, of a **within-run block-permuted** c_e: the run's per-step increments are cut into 200-step blocks (idle zeros kept in place), the blocks are permuted within the run, and the index is re-accumulated. Evaluated within each family | Point estimate ≤ 0.005 and upper bound of the one-sided 95% interval < 0.015 | Stop; leakage or a design artefact |
| G5, local statistics | R̄²(X_cov + c_e) versus R̄²(X_cov + C6) on test runs | c_e must exceed C6 | Otherwise c_e is reported as failing admissibility criterion (a), whatever H1 shows |
| G6, onset versus skill | H1 statistic with the number of training runs halved and doubled; Stage B predictors with their training budget doubled | No flip between *supported* and *equivalent*, and \|change in mean ΔR²\| ≤ 0.01 | Report as onset-dependent |
| G7, reproducibility and budget | Bit-identical reruns of a random 5% of runs; configuration hashes verified before analysis; realised rehearsal steps = Q on every Stage B run | 100% | No analysis until fixed |
| G8, reliance | Placebo c_e stream in Stage B (§9) | Upper bound of the one-sided 95% interval of the placebo scheduler's advantage over its comparator < δ_B / 2 | c_e is decodable but not used |
| G9, H3 identifiability | Split-half reliability (A vs B) of ΔF across matched pairs; cross-seed reliability of Δ(Δc_e^{D\*}); its coefficient of variation SD / mean Δc_e^{D\*} | ≥ 0.50; ≥ 0.50; ≥ 0.05 | H3 is reported as *not identifiable* |

## 12. Data splits and sample size

- **Calibration runs:** used only for G1, G3, the SESOI value, the choice of D\*, m_ch, the stationarity check of R, the variance of the test statistics, and threshold design. They are discarded afterwards and never enter test statistics.
- **Training runs:** F1–F3. **Validation runs:** F1–F3, new seeds. **Test runs:** F1–F3, new seeds, plus F4 (sanity), F5, F6, and the O blocks. O blocks are used only for H3 and G9.
- **Fixed sizes (indicative; frozen after the power simulation):** calibration 24 runs (8 per F1–F3); training 30 base (15 and 60 for G6); validation 15; O-block pairs 60; Stage B 40 paired seeds per scheduler.
- **Sample size for H1.** Let σ̂_up be the upper 80% chi-square confidence bound of the SD of per-run ΔR² on calibration runs. For TOST at a true ΔR² of 0 and for the MET at a true ΔR² of 2δ, each at power 0.80 and one-sided α = 0.025:
  - n_TOST = ⌈(z_0.975 + z_0.90)² (σ̂_up/δ)²⌉ = ⌈10.51 (σ̂_up/δ)²⌉;
  - n_MET = ⌈(z_0.975 + z_0.80)² (σ̂_up/δ)²⌉ = ⌈7.85 (σ̂_up/δ)²⌉;
  - n = max(n_TOST, n_MET), with at least ⌈7.85 (σ̂_up/δ)²⌉ runs each in F5 and in F6 so that their standalone reports have power 0.80 for the MET.
- **Sample size for H2, H4a, H4b** uses the first Holm level, one-sided α = 0.025/3 (z = 2.394): n = ⌈(2.394 + z_0.90)² (σ̂_up/δ)²⌉ = ⌈13.5 (σ̂_up/δ)²⌉, with δ_B and the Stage B variance for H4.
- **Power simulation.** Before freeze, these closed-form sizes are checked by simulation on calibration data, with the weighted R², the final bootstrap, the fixed-sequence and Holm procedure, and the separate F5 and F6 reports.
- **Budget cap:** 200 test runs in Stage A. If n exceeds the cap, the scope is reduced (fewer families, declared before freeze). The SESOI rule is not relaxed.

## 12a. Stage 0: calibration and go/no-go decision

Stage 0 uses 8–12 technical runs, followed by the calibration runs of §12. It measures and decides; it tests no hypothesis. The author decides after Stage 0 whether to continue. Continuation requires all of the following; otherwise the design is simplified again or the study stops, and the decision is reported.

| Criterion | Requirement |
|---|---|
| Target measurable | G1 passed (r̄_AB ≥ 0.70); at least 20 valid exposure episodes per run; forgetting with non-negligible variance |
| Index not reconstructible | G2 passed on calibration runs (interval rate, OLS and GBDT). The raw increment Δc_e is not used for this check, because it is dominated by interval length |
| Headroom | G3 passed (headroom ≥ 2.5 δ) |
| Baseline and pipeline | G3b passed (baseline saturated); G4b passed (positive control detected) |
| Cost | Measured time per full run (training, probes, D3, snapshots) ≤ 40 min single-threaded; projected Stage A ≤ 150 CPU-hours; runs resumable from checkpoints; parallel runs bit-identical (G7) |
| Sample size | Projected n for H1 ≤ 150 test runs |

The feasibility of the full design is not assumed: the step times in §14 cover training only, and probe evaluation and D3 are measured in Stage 0.

## 13. Stage C: transfer to pretrained language models

Stage C keeps the **question and the inferential logic** (B_strong versus B_strong + c_e, three-way outcomes, gates). It does **not** keep every operational definition, and it is **not part of this preregistration**. A separate Stage C adaptation document will be frozen and deposited with its own DOI before any Stage C run. Its cost is not included in §14. Changes already known:
- **Agent.** Publicly available pretrained causal LMs (the Pythia family); a CPU feasibility check on the smallest model; the confirmatory model size and optimizer arm are named in the adaptation document before any Stage C run.
- **No childhood phase.** Pretraining replaces it; R is a fixed generic-text battery evaluated, not trained.
- **Targets.** T1 is the loss on held-out samples of earlier domains, read at fixed target positions. The accuracy-based inclusion criterion is replaced by a loss-based learned criterion defined in the adaptation document.
- **Covariates.** Task type is replaced by domain identity; competence uses a held-out half of each domain's samples; C7a only (no oracle labels).
- **LoRA.** D is computed on the effective weight update ΔW_eff = (α/r)(B_{τ+1}A_{τ+1} − B_τ A_τ), not on the concatenated adapter matrices.
- **D3.** Restricted to a small number of target positions and to top-K or sketched distributions; the vocabulary of ≈ 50,000 tokens makes full distributions infeasible.
- **Displacement and C8b, C9.** Evaluated only for the smallest model, for LoRA, or for a subset of tasks, as offline references.

The Stage A conclusions are claimed to generalise only if Stage C reproduces the three-way outcome of H1.

## 14. Compute estimate

Measured at drafting on the author's laptop (16 logical CPUs), with the §3 agent (0.93 M parameters, untied embeddings, AdamW, clipping):

| Setting | ms per training step |
|---|---|
| batch 32 × 4 tokens, 1 thread | 19.9 |
| batch 32 × 4 tokens, 8 threads | 17.3 |
| batch 32 × 64 tokens, 1 thread | 206.5 |
| batch 32 × 64 tokens, 8 threads | 87.5 |

Because examples are 4–6 tokens long and unpacked (§3), the relevant figure is ≈ 20 ms per step on one thread, and eight single-threaded runs proceed in parallel with almost no loss.

| Item | Estimate (to be replaced by Stage 0 measurements) |
|---|---|
| Training, ≈ 23,000 steps | ≈ 8 min per run |
| Probe evaluation (≈ 120 evaluations × up to 40 tasks × 256 items, forward only) | ≈ 1–2 min per run |
| D3 every 10 steps (2,300 forward passes on 256 items) | ≈ 1–2 min per run |
| One run | ≈ 10–12 min single-threaded |
| Stage A (≤ 200 test runs + ≈ 70 calibration, training and validation runs) | ≈ 50 CPU-hours, ≈ 7 wall-clock hours on 8 workers |
| Stage B | ≈ 20–30 CPU-hours |
| Stage C-mini (smallest Pythia model, CPU) | hours per run; feasibility only |

## 15. Interpretation table (frozen with the protocol)

| Outcome | Interpretation |
|---|---|
| H1 supported, G2 and G5 passed, and F5 supported alone | Accumulated own change predicts own forgetting beyond clocks, counts, and a strong set of logged summaries, and the result generalises across generator parameters: first empirical support for the experiential index (Level 2) |
| H1 supported, but F5 not supported alone | The advantage does not generalise beyond the training generators; reported as a construction effect, not a general result |
| H1 supported, and F6 alone shows c_e worse than B_strong (upper bound < 0) | The index is useful where change and interference coincide, and misleading where they do not; reported as a conditional result |
| H1 equivalent, and G3b and G4b passed | Counts and logged summaries suffice; Level 2 is closed for this regime |
| H1 equivalent, but G4b failed | Not interpretable as closure: the pipeline could not detect an effect of the size sought |
| c_e beats B_standard but H1 is equivalent | The information in c_e is reconstructible from cheap telemetry |
| G2 fails | Not identifiable in this design |
| G5 fails | c_e fails admissibility criterion (a), whatever H1 shows |
| F1 alone | Equivalence on F1 is the expected result of the positive control and does not weaken H1 |
| H2 supported | The scalar index captures at least 80% of what full displacement captures, at the storage ratio reported for D\* |
| H2 not supported, or G2b fails | Displacement carries information that the path index does not, or neither adds enough to compare; the claim of a compact index is weakened |
| H3 supported (G9 passed; optional module) | The index tracks a global path effect invisible to order-invariant counts (exploratory) |
| H4a supported and G8 passed | The agent uses the index inside a covariate-aware predictor to improve a decision about itself |
| H4b supported and G8 passed | The index alone suffices as a rehearsal trigger, beyond the best cheap trigger chosen on validation |
| Stage C reproduces H1 | The result is not an artefact of the synthetic world |

## 16. Threats to validity and mitigations

| Threat | Mitigation |
|---|---|
| Designer degrees of freedom in the stream families | F1 natural; F5 and F6 held out; F6 adversarial; families frozen; Stage C on real data |
| Omitted cheap competitor reconstructs c_e | B_strong with LR-weighted, momentum, work, norm, local and canary summaries; G2 on the rate; B_standard reported |
| Shared noise between predictors, inclusion, and target | Half B for covariates and inclusion, half A for the target; R and P_ref disjoint from probes and P_target; block-permuted placebo G4; T2 not confirmatory |
| Scale and weight-decay drift | D1_rel; C6b; N(t₀) and state norms in X_cov; T1-acc |
| Local-statistics shortcut (closed study) | C6 with short clamped windows inside B_strong; G5 |
| Over-weighting of early tasks | Equal weight per exposure episode |
| Dependence of triplets within a run | Run-level inference; within-run weighted R² |
| Selection of D, k or comparators after seeing results | D\*, m_ch and S-C\* chosen on calibration or validation and frozen |
| Unequal rehearsal budgets | Hard cap, pacing, terminal flush; G7 |
| Under-tuned baseline produces a spurious advantage | Equal tuning budget; locked hyperparameters; saturation gate G3b |
| A null result produced by an insensitive pipeline | Positive control G4b |
| Optimizer specificity | SGD arm (exploratory) |
| Scale | Stage C; restrained claims |

## 17. Deliverables

- Code (MIT), data and reports (CC BY 4.0), frozen configurations with SHA-256, a run inventory, automated audit checks, and scripts that regenerate every reported table.
- A Zenodo preregistration (with DOI) before main runs, stating explicitly that the study is a change of the plan announced in the Perspective (versions 1.0–1.2).
- A preprint with *References* links to the Perspective and the closed study, and *Is supplemented by* to the code archive.

## 18. References

- Biderman, S., Schoelkopf, H., Anthony, Q., et al. (2023). Pythia: A suite for analyzing large language models across training and scaling. arXiv:2304.01373.
- Elazar, Y., Ravfogel, S., Jacovi, A., & Goldberg, Y. (2021). Amnesic probing: Behavioral explanation with amnesic counterfactuals. *Transactions of the Association for Computational Linguistics, 9*, 160–175. https://doi.org/10.1162/tacl_a_00359
- Feng, Y., Wang, H., Li, J., Chu, X., Kang, Z., Liu, Y., Wang, Y., Yu, P. S., & Wu, X.-M. (2026). FOREVER: Forgetting curve-inspired memory replay for language model continual learning. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 24945–24965. https://doi.org/10.18653/v1/2026.acl-long.1144 (arXiv:2601.03938)
- Hu, E. J., Shen, Y., Wallis, P., et al. (2022). LoRA: Low-rank adaptation of large language models. arXiv:2106.09685.
- Ionici, I. D. (2026). *A Time of Their Own: Agent-Held Temporal Evidence for Persistent AI Agents* (Version 1.3). Zenodo. https://doi.org/10.5281/zenodo.23847648
- Ionici, I. D. (2026). *Does Explicit Episode–Trace Binding Help? An Exploratory Study with Information-Matched, Competence-Audited Controls* (Version 1.3). Zenodo. https://doi.org/10.5281/zenodo.23847602
- Ionici, I. D. (2026). *Episode–Trace Binding Pilot: Code, Frozen Configurations, and Per-Run Results* (Version 1.2) [Software]. Zenodo. https://doi.org/10.5281/zenodo.23667154
- Jin, X., & Ren, X. (2024). What will my model forget? Forecasting forgotten examples in language model refinement. arXiv:2402.01865.
- Kalajdzievski, D. (2024). Scaling laws for forgetting when fine-tuning large language models. arXiv:2401.05605.
- Kirkpatrick, J., Pascanu, R., Rabinowitz, N., et al. (2017). Overcoming catastrophic forgetting in neural networks. *Proceedings of the National Academy of Sciences, 114*(13), 3521–3526. https://doi.org/10.1073/pnas.1611835114
- Knopov, D., & Shvai, N. (2026). Equivalence testing and run-count design for stochastic machine-learning experiments. arXiv:2610.23700.
- Kornblith, S., Norouzi, M., Lee, H., & Hinton, G. (2019). Similarity of neural network representations revisited. arXiv:1905.00414.
- Lakens, D., Scheel, A. M., & Isager, P. M. (2018). Equivalence testing for psychological research: A tutorial. *Advances in Methods and Practices in Psychological Science, 1*(2), 259–269. https://doi.org/10.1177/2515245918770963
- Lee, S., Goldt, S., & Saxe, A. (2021). Continual learning in the teacher-student setup: Impact of task similarity. In *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139, 6109–6119. arXiv:2107.04384.
- Loshchilov, I., & Hutter, F. (2019). Decoupled weight decay regularization. arXiv:1711.05101.
- Mirzadeh, S. I., Farajtabar, M., Pascanu, R., & Ghasemzadeh, H. (2020). Understanding the role of training regimes in continual learning. arXiv:2006.06958.
- Mukhoti, J., Stenetorp, P., & Gal, Y. (2018). On the importance of strong baselines in Bayesian deep learning. NeurIPS 2018 Bayesian Deep Learning Workshop. arXiv:1811.09385.
- Roseboom, W., Fountas, Z., Nikiforou, K., Bhowmik, D., Shanahan, M., & Seth, A. K. (2019). Activity in perceptual classification networks as a basis for human subjective time perception. *Nature Communications, 10*, 267. https://doi.org/10.1038/s41467-018-08194-7
- Su, J., & Zhang, W. (2026). When can first-order models of fine-tuning bound forgetting? arXiv:2609.32818.
- Toneva, M., Sordoni, A., Tachet des Combes, R., Trischler, A., Bengio, Y., & Gordon, G. J. (2019). An empirical study of example forgetting during deep neural network learning. arXiv:1812.05159.
- Zenke, F., Poole, B., & Ganguli, S. (2017). Continual learning through synaptic intelligence. arXiv:1703.04200.

*References added in v0.2 (Biderman et al., Hu et al., Kornblith et al., Loshchilov and Hutter, Zenke et al.) are to be verified against arXiv before freeze, as are all others.*

## 19. Revision log v0.1 → v0.2

Sources: **A** = Google Argon review of v0.1 (truncated in Q12; a continuation was requested); **C** = Copilot analysis of that review; **O** = the author's own pre-review. Every accepted item was checked before adoption.

**Accepted**

| Change | Sections | Source |
|---|---|---|
| Half B for covariates and inclusion; half A for the target; fact tasks enlarged to 256 items; balanced exposure | §4.1, §4.2, §6, §7 | A, O |
| G1 ceiling uses the uncorrected r_AB (the target uses one half) | §7, §11 | A, O |
| Same-step D2 cancels the Adam preconditioner (verified algebraically); D2 uses a segment-lagged v̂; C5d added; Disp^{D2} anchored at v̂(t₀) | §5, §7 | A, O |
| D1_rel against scale and weight-decay drift; Δθ logged before and after decay | §3, §5 | A |
| D2 defined in the SGD arm by a passive EMA | §3 | A, O |
| Clipped and raw gradient norms both logged and used | §3, §7 | A |
| B_strong with LR-weighted gradient and loss, squared gradient, SI work, momentum norm, noise scale, state norms, N(t₀); B_standard kept descriptively | §7 | A (two-tier design: C) |
| Canary loss C10 on R | §7 | O |
| C6 windows shortened to W_eff = min(20, ⌊ΔN/4⌋) and clamped; minimum interval of 50 steps | §6, §7 | A |
| π_overlap removed from X_cov; C7 split into agent-observable C7a and oracle C7b; agent-observable novelty and overlap covariates | §7 | A |
| R and B_beh on a disjoint key pool; stationarity check of D3 | §4.1, §5 | A |
| Storage accounting: one running scalar plus one snapshot per task; snapshot objects per D; C9 storage and training-items gradient | §1, §5.2, §7 | A |
| T1-acc secondary target | §6 | A |
| Operational specifications: answer-position reading, base-2 JS, vocabulary partition, rule-task template, no packing, fixed childhood with gate, O blocks forked from one state, fixed C1 basis, end of interval before the next exposure | §3–§7 | A |
| Monotone constraints specified per feature; locked-hyperparameter ΔR²; ridge transforms and scaling | §8 | A |
| Equal weight per exposure episode | §6, §8 | A |
| Cross-fitting over training runs; two-sample bootstrap for ridge only | §8 | A (scope: C) |
| H2 as the linear contrast Z_r with denominator gate G2b and an equivalence bound | §10, §11 | A, O |
| H3 redesigned around a global property and moved outside the confirmatory family; G9 expanded; threshold 0.20 | §10.3, §11 | A (secondary status: C) |
| Stage B: hard budget cap, pacing, terminal flush; comparator chosen on validation; S-uniform, S-C2, S-C5, S-C5b added; H4 split into H4a and H4b; online covariates from training batches | §9, §10 | A, O |
| Within-run block-permuted placebo; G4 one-sided, locked hyperparameters, per family; cross-seed yoked stream kept as a robustness check | §9, §11 | A (both kept: C) |
| Single α = 0.025 per side for MET and TOST; fixed sequence H1, then Holm over H2, H4a, H4b; Stage B only after H1 is supported | §9, §10 | A, C, O |
| Power formulas with z_{1−β/2} for TOST, the Holm level, an upper bound on σ, and F5/F6 allocation; checked by simulation | §12 | A, C |
| Headroom-based SESOI rule, frozen before test, with raw and relative gains both reported | §10.1 | A (caution: C) |
| G2 on the interval rate with OLS and GBDT; G3 on calibration with a headroom check; G5 and G6 made quantitative; G8 one-sided | §11 | A, O |
| F4 not pooled; adversarial F6 added; F5 described as generalisation across generator parameters; F1 row added to the interpretation table | §4.4, §15 | A, O (F6 design: C) |
| Stage C rewritten as a transfer protocol with a separate adaptation document; LoRA on ΔW_eff; no childhood | §13 | A, C, O |
| Compute estimate replaced by measured step times; single-threaded workers for determinism and throughput | §3, §14 | O, A |
| Notation: ρ̄ for the rate, m_ch for the chunk stride, L_reh for the rehearsal length; §2 wording on elapsed time; consistent scheduler names | throughout | A |
| Content versus provenance note | §0.4 | O |
| Prior work FOREVER (Feng et al. 2026) cited, with priority for the index acknowledged; contribution restated as an identification audit; exploratory S-FOREVER arm. Verified on arXiv and in the ACL Anthology: τ_t = Σ‖Θ_i − Θ_{i−1}‖₂ on LoRA weights; only step counts tested as an alternative clock | §0.3, §9, §18 | A (named), C (positioning), O (verification) |
| H3 made an optional exploratory module, run only if H1 is supported and budget remains | §10.3, §15 | C |
| Stage 0 go/no-go criteria (cost, sample size, episodes per run) | §12a | C |
| Stage C declared outside this preregistration | §13 | C |
| Positive control G4b (sensitivity of the pipeline to an effect of 2δ) and baseline-saturation gate G3b (doubled tuning budget); interpretation table and Stage 0 criteria updated. Motivated by the second priority-search round on the closed study (positive-control validation; Mukhoti et al. 2018) | §11, §12a, §15 | C, O |
| Mukhoti et al. 2018 (strong baselines), Knopov and Shvai 2026 (TOST and run counts for stochastic ML), Elazar et al. 2021 (decodability is not use) cited; all verified on arXiv or Crossref | §7, §9, §10.1, §18 | C (priority search on the closed study) |

**Rejected or modified**

| Suggestion | Decision |
|---|---|
| "PyTorch 2.13 and NumPy 2.5 do not exist" (A) | Rejected: both are installed and were used for the measurements (PyTorch 2.13.0, NumPy 2.5.1) |
| Per-step D2 weighted by the running maximum of v̂ (A) | Modified: segment-lagged v̂ is used, because a running maximum never decreases and would track history age |
| Weight-decay pulses and pre-LN rescaling as part of F6 (A) | Moved to exploratory robustness checks: no counterpart in ordinary training (C) |
| H3 option B (midpoint evaluation or a recency-weighted index) (A) | Rejected: it introduces a second index and complicates interpretation (C) |
| Packed 64-token sequences with block-diagonal masks (A) | Rejected: examples are unpacked, which is simpler and, as measured, ≈ 4× cheaper per step |
| Argon's split sizes adopted as final (A) | Modified: indicative only, to be fixed by the power simulation (C) |
| Two-sample bootstrap with refitting for all models (A) | Modified: ridge only; cross-fitting for GBDT (C) |
| Go/no-go on R²(Δc_e \| B_strong) < 0.90 for the raw increment as well as the rate (C) | Rate only: the raw increment is dominated by interval length and would fail the check trivially |
| Full-run time of 45–120 min (C) | Not adopted as an estimate: it assumed long sequences; examples are unpacked. Replaced by a measured go/no-go limit of 40 min per run (§12a) |

**Pending.** The truncated part of the Argon review (end of Q12, Q13, compute check (g), §15–§17, and its five priority changes) has been requested. Any further change will be logged in v0.3.

**Update of 1 November 2026 (no change of design).** The Perspective (v1.3, 10.5281/zenodo.23847648), the study (v1.3, 10.5281/zenodo.23847602), and the code archive (v1.3, 10.5281/zenodo.23847723) were revised after an automated review by the CMU Paper Reviewer. Citations and the closure rule in §0 now follow v1.3: non-inferiority within a prespecified margin and no worse declared cost, with mixed trade-offs reported as unresolved.
