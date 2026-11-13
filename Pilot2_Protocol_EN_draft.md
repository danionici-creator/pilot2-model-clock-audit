# Pilot 2 — Technical Protocol (Draft for External Review)

**Working title:** *Does an Agent's Own Change Keep Time? Testing an Experiential Index of Adaptation Against Clocks, Counts, and Logged Update Summaries*

**Author:** Ioan Daniel Ionici (Independent Researcher, Oradea, Romania; ORCID 0009-0009-8183-3656)  
**Status:** draft protocol **v0.4**, 4 November 2026. Not frozen. To be frozen, hashed (SHA-256), and deposited on Zenodo before any main run. v0.2 revised v0.1 after an AI review (Google Argon) and an AI analysis of that review (Copilot); v0.3 revises v0.2 after an AI review of v0.2 (Google Deep Review, Argon), with clarifications after an AI review of v0.3 (Mistral Large 4); v0.4 revises v0.3 after the Stage 0 technical runs (rule tasks withdrawn, learning rate, a cap on the target interval, the reference battery, the cost criterion). Every change and every rejected suggestion is listed in §19–§21.  
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
| Competitors C1, C5b–C5f, C8, C8b, C9 | External literature on forgetting and consolidation (§18) |
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
| ρ̄ | Mean interval rate Δc_e / max(ΔN, 1); the only information in c_e beyond counts (§2) |
| Disp^D | Net displacement D(S(t₀), S(t₁)) |
| √JS | Jensen–Shannon distance, base-2 logarithm, in [0, 1] (a metric) |
| m_ch | Chunk stride, in optimizer steps, for chunked distances (§5) |
| L_reh | Length of one rehearsal segment, 64 steps (§9) |
| η₀ | Base learning rate, 3 × 10⁻⁴ (frozen at Stage 0; §3) |
| ΔN_max | Cap on the interval of a T1 triplet: ΔN < 1,280 (frozen at Stage 0; §6) |
| q₀ | Step quantum: 64 optimizer steps; segment lengths, idle intervals, the evaluation grid and the chunk strides are aligned to it (§4.3) |
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

**Storage.** Maintaining c_e costs **one running scalar**. Answering a query about task k needs the snapshot c_e(t_{0,k}) taken at its last exposure. The marginal storage of adding c_e to any predictor set, and the total storage of the standalone trigger S-c_e, is therefore one running scalar plus **one scalar per tracked task exposure**: at most K + 1 scalars for K active tasks (here K ≤ 40). The rate ρ̄ (§2) needs nothing more, because N(t_{0,k}) is already stored for the baseline. For comparison, B_strong caches about 20 scalars per task exposure plus one global input counter (§7), and net displacement needs 0.03 M to 1.9 M numbers per task exposure (§5.2).

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

**Scope restriction on the task type.** Since v0.4 the world contains fact tasks only (§4.1): T1 is the forgetting of trained associations (in-sample retention). The study does not test the forgetting of a generalisation.

## 2. Identification note (read first)

Within a run, at a fixed evaluation time t₁, the ranking of tasks by Δc_e = c_e(t₁) − c_e(t_{0,k}) induces the same weak ordering as the committed steps ΔN_k = N(t₁) − N(t_{0,k}) since their last exposure, with ties wherever the intervening steps produce no change (D = 0). Elapsed ticks Δc_a can differ where steps do not, for example across idle intervals. The reason is that c_e is non-decreasing. A global scalar index therefore carries **no task-specific ordinal information at a fixed time**.

It does carry **cardinal** information: the spacing between two tasks' values, c_e(t_{0,k}) − c_e(t_{0,j}), equals the change accumulated between their exposures, which varies with the rate ρ(τ) = dc_e/dN. All information that c_e carries beyond counts lies in this **temporal variation of its rate**: some intervals of equal length contain more change than others. Three consequences follow:
1. Q1 is identifiable only to the extent that the interval rate ρ̄ = Δc_e / max(ΔN, 1) varies across intervals and is not reconstructible from the baseline. Gate G2 checks this on the rate, not on the raw increment, because the raw increment is dominated by interval length. For the same reason c_e enters every predictor set as the pair {Δc_e, ρ̄} (§8), as the competitors do.
2. A scheduler that *selects which task to rehearse* by ranking tasks on Δc_e since their last exposure is equivalent to least-recently-rehearsed. Q4 must therefore test *when*, and *how much*, to rehearse (allocation over time), or use c_e together with task covariates inside a learned predictor (§9). Inside such a predictor the *conditional* ranking can differ from least-recently-rehearsed, because the spacing c_e(t_{0,k}) − c_e(t_{0,j}) is traded off against covariates at t₀; whether it does is checked on validation runs before H4a is interpreted (§9).
3. c_e is not task-specific memory. It cannot by itself encode which tasks a stretch of change interfered with (§10.3).

## 3. Agent

| Component | Specification |
|---|---|
| Architecture | Decoder-only Transformer, 4 layers, d_model = 128, 4 heads, d_ff = 512, pre-LN, GELU, learned positional embeddings, maximum context 8 (every example has 5 tokens; a longer context would leave positional embeddings that never receive a gradient and only decay), vocabulary 512 tokens. Input embedding and output head **untied**; biases in all linear layers and LayerNorms. ≈ 0.93 M parameters (exact count recorded at Stage 0) |
| Sequences | One example per sequence, no packing; every example is `[TASK] [K1] [K2] →` plus the answer token (5 tokens), so no padding occurs; loss and probes are read at the answer position only |
| Optimizer (primary) | AdamW, base learning rate η₀ = 3 × 10⁻⁴ (childhood and constant-rate families; the F3 and F5 schedules multiply it), β = (0.9, 0.999), ε = 1e-8, weight decay λ = 0.01, global gradient clipping at norm 1.0 applied immediately before `optimizer.step()`. m and v see the clipped gradient g̃. Weight decay applies to weight and embedding matrices, not to biases or LayerNorm parameters. m and v are initialised to 0 at the first childhood step, persist without reset through life, segment boundaries and warm restarts, and are bias-corrected with the global count of committed steps |
| Optimizer (robustness arm) | SGD with momentum 0.9, same clipping, learning rate and weight decay frozen at Stage 0. A passive EMA v_τ = 0.999 v_{τ−1} + 0.001 g̃_τ² is maintained so that D2 is defined; it does not affect the update. Without preconditioning, D2 then scales with the square of the gradient magnitude (§5.1); the arm is exploratory |
| Persistent state S | Parameters θ and optimizer moments (m, v); distances are computed on θ |
| Logged per step | ‖g_τ‖₂ (raw) and ‖g̃_τ‖₂ (clipped); η_τ; batch size B_τ; training loss L_τ; ‖Δθ_τ‖₂ before and after the decoupled weight-decay term; ‖m̂_τ‖₂; \|⟨g̃_τ, Δθ^pre_τ⟩\|; ‖θ_τ‖₂ and the norm of the decayed parameters; Tr v̂_τ |
| Precision, device, determinism | float32 on CPU; `torch.use_deterministic_algorithms(True)`; fixed seeds for data, initialisation, and dropout (dropout = 0 in the primary arm). Each run is a **single-threaded worker** (`torch.set_num_threads(1)`, `torch.set_num_interop_threads(1)`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`); workers run in parallel, as many as maximise throughput on the declared machine (four at Stage 0; §14) |
| Software | Python 3.14.6, PyTorch 2.13.0 (CPU build), NumPy 2.5.1, scikit-learn 1.9.0, as installed at drafting; exact versions are re-recorded in `environment.txt` at freeze |

## 4. World and streams

### 4.1 Task types and vocabulary

- **Fact tasks.** Task k is a set of 256 key→value pairs. A key is an ordered pair of key tokens, so the input is `[TASK_k] [K1] [K2] →` and the target is a single `[VALUE]` token. Keys are drawn from the target key vocabulary V_target, and the overlap between tasks is controlled by a pool-sharing parameter π_overlap. Values are drawn uniformly from 64 value tokens. Fact probes are **trained items**: they measure in-sample associative retention.
- **Rule tasks: withdrawn at Stage 0.** v0.3 also had algorithmic rule tasks, y = (a_k·x + b_k) mod m_k on two base-32 digit tokens, with held-out probe inputs. At Stage 0 a rule task trained alone reached training accuracy 1.0 within 128–256 steps but held-out accuracy 0.02–0.30 after 2,048 steps, with the held-out loss rising (overfitting); in full runs 0–9 of 40–74 rule episodes per run passed inclusion. They would have produced almost no triplets, so v0.4 has fact tasks only (§21). The world therefore tests in-sample retention, not generalisation (§1, §16).
- **Reference tasks.** A fixed set of 8 fact tasks, trained only during the childhood phase. They are never targets. They supply the reference battery R (256 items, 32 per reference task) and the behavioural battery B_beh (256 items, 32 per reference task, disjoint from R), both drawn from their trained items. Their keys use the key vocabulary V_ref. R is forgotten early in life (§5.1).
- **Distractor tasks (F6).** Fact tasks on the distractor key vocabulary V_distractor, with their own task tokens.
- **Vocabulary partition** (frozen at Stage 0): 64 task tokens (40 target, 8 reference, 8 distractor, 8 spare); key tokens in three **token-disjoint** vocabularies, V_target (180 tokens), V_ref (84) and V_distractor (84); 64 value tokens; 32 digit tokens (unused since v0.4, kept so that the partition is unchanged); at most 4 special tokens (`→`, padding, spares); 512 in total. Disjointness holds for single tokens, not only for key pairs.
- **Exposure.** Every training, re-exposure, and rehearsal segment iterates over balanced permutations of the task's items (full epochs). With 256 items and batch sizes 16, 32 or 64, an epoch takes 16, 8 or 4 steps; every segment length is a multiple of 64 steps (§4.3), so every segment ends at the end of an epoch and every item of halves A and B has the same exposure count.

### 4.2 Probes

Each target task has a probe set: its 256 facts, which are trained items, so T1 measures in-sample associative retention. The probe set is split **once, at task creation**, into disjoint halves A and B of 128 items each.
- **Half A** supplies the confirmatory target T1.
- **Half B** supplies the competence covariates at t₀, the inclusion criterion, the reliability ceiling (with A), and the Stage B retention target T3.

No probe item belongs to R or to B_beh. All probe losses and probabilities are read at the single answer position after `→`; cross-entropy is in nats.

### 4.3 Run structure

| Phase | Steps | Content |
|---|---|---|
| Childhood | exactly 3,072 (48 × 64) | Reference tasks. Gate: reference accuracy ≥ 0.95 at the end; a run that fails is replaced and counted |
| Life | ≈ 20,000 (a multiple of 64) | ≈ 40 target tasks, presented according to the stream family; rehearsal segments, re-exposure segments, and idle intervals according to the family |
| Evaluation | — | Probes of every learned task are evaluated at the end of every segment, at the end of every idle interval, and on a grid every 256 optimizer steps (during idle intervals, every 256 ticks) |

**Step quantum.** All segment lengths, idle intervals, warm-restart times and the evaluation grid are integer multiples of q₀ = 64 optimizer steps (ticks, for idle intervals). Every chunk stride m_ch considered in §5.1 divides 64, so segment boundaries and evaluation points always coincide with chunk boundaries. Chunks are indexed by committed optimizer steps from the first step of life.

**Segment boundaries.** A segment boundary is an agent-observable event: a change of the task token in the training inputs, the start or end of an agent-triggered rehearsal, or a change of batch size. Warm restarts in F3 change only the learning rate and are not segment boundaries. No generator metadata defines a boundary.

### 4.4 Stream families

| Family | Generator | Intended decoupling | Role |
|---|---|---|---|
| **F1, natural** | New task every fixed number of steps, fixed segment length, round-robin rehearsal, constant LR, fixed batch | None | Positive control, reported alone: counts are expected to suffice; **not pooled** into H1 |
| **F2, variable novelty** | New tasks interleaved with re-exposure to already-mastered data in random amounts; batch size ∈ {16, 32, 64} per segment | Steps and tokens decouple from change | **H1 confirmatory domain** (pooled with F3) |
| **F3, LR schedule** | Cosine annealing with warm restarts at random times (multiples of 64 steps) | Steps decouple from change; LR-weighted summaries are strong competitors | **H1 confirmatory domain** (pooled with F2) |
| **F4, idle** | Random idle intervals with no updates; c_a advances, θ is frozen | Only elapsed time decouples (C1–C7 stop with c_e) | Sanity check only; **not pooled** into H1 |
| **F5, held-out** | Mixture of the F2–F3 generators (re-exposure in random amounts, variable batch size, cosine warm restarts) with a different π_overlap and idle intervals | Generalisation across generator parameters | Never used for fitting or selection; test only; replication check reported alone (§10.2) |
| **F6, adversarial** | Target exposures at a regular rate, interleaved with variable-length distractor segments on V_distractor with their own task tokens, label noise 0.3, and batch size ∈ {16, 32, 64} per segment as in F2, under the same optimizer configuration | High parameter change with little interference: favours the competitors | Never used for fitting or selection; test only; adversarial check reported alone (§10.2) |
| **O, order blocks** | Designed blocks (§10.3) forked from one saved state | Path dependence | H3 only; **not pooled** into H1, H2, H4 |

F5 is built from the F2–F3 generators, so it tests generalisation across generator parameters, not freedom from designed decoupling. F6 tests the converse regime that F2–F5 lack: much movement, little forgetting. Scale-drift interventions (weight-decay pulses, rescaling of pre-LN weights) are exploratory robustness checks only, because they have no counterpart in ordinary training. Generator parameters for each family are frozen with the protocol.

### 4.5 Time

c_a counts *ticks*. Each optimizer step adds 1 tick; each idle interval adds its length in ticks; evaluations add 0 ticks. Idle intervals are inserted only between segments, in multiples of 64 ticks. Without idle intervals c_a equals N. All interval sums in §7 run over committed optimizer steps τ ∈ (N(t₀), N(t₁)], so idle ticks contribute nothing to them.

## 5. Distances D and the index c_e

### 5.1 Candidate distances

Δθ^pre(τ) denotes the update of step τ before the decoupled weight-decay term.

| D | Definition | Evaluated |
|---|---|---|
| **D1** | ‖θ(τ+1) − θ(τ)‖₂, the full update including weight decay | Every step |
| **D1_rel** | ( Σ_ℓ ‖Δθ^pre_ℓ(τ)‖₂² / (‖θ_ℓ(τ)‖₂² + 10⁻¹²) )^{1/2}, where ℓ runs over the weight matrices and embedding matrices (biases and LayerNorm vectors excluded) | Every step |
| **D2** | ( Σ_i v̂_i(τ − L_τ) (Δθ^pre_i(τ))² )^{1/2}, with v̂ the bias-corrected second moment at step 64·⌊(τ − 256)/64⌋, i.e. lagged by L_τ ∈ [256, 319] steps (a blocked lag: an exact lag of 256 steps would need 256 stored copies of v̂, ≈ 1 GB per worker; at Stage 0 the blocked and exact versions differed by a median of < 1% per step, at most 11–19%) | Every step |
| **D3** | Mean over x ∈ R of √JS( p_{S(τ)}(·\|x), p_{S(τ+m_ch)}(·\|x) ) at the answer position, \|R\| = 256 | Every m_ch steps (chunked) |
| **D4** (exploratory) | √(1 − CKA), with standard (biased) centred linear CKA of the final-layer answer-position representations on R, taken after the final LayerNorm (Kornblith et al. 2019) | Every m_ch steps (chunked) |

**Why D2 uses a lagged curvature.** Under Adam, Δθ^pre_i ≈ −η m̂_i / (√v̂_i + ε). Weighting by the *current* v̂ therefore cancels the preconditioner: (Σ_i v̂_i(τ) Δθ^pre_i(τ)²)^{1/2} ≈ η_τ ‖m̂_τ‖₂, so a same-step D2 would be the learning-rate-weighted momentum norm, a logged optimizer summary (C5d, §7). A fixed lag avoids exact cancellation without using segment boundaries, which an agent in an unsegmented stream would not have. With β₂ = 0.999 the lagged and current moments stay close over 256 steps, so D2 may remain nearly collinear with C5d; gate G2 detects this, and C5d stays in the baseline. Under SGD (robustness arm) the update is not preconditioned, so D2 scales with the square of the gradient magnitude; the difference is reported, not interpreted.

**Why D1_rel.** In a pre-LN Transformer, some weight rescalings change ‖θ‖ without changing the function, and AdamW shrinks θ at every step independently of the data. D1_rel removes both scale effects. Raw D1 includes the weight-decay step and is kept for comparison; the corresponding weight-decay path is a competitor (C5f, §7).

- c_e^D(t) = sum over steps (D1, D1_rel, D2) or over chunks (D3, D4) up to t.
- √JS is a metric, so the chunked D3 sum is a lower bound on the per-step sum. √(1 − CKA) is the chordal distance between centred Gram matrices normalised to unit Frobenius norm and also satisfies the triangle inequality.
- **Chunking control.** On calibration runs, chunked versions of D1, D1_rel and D2 at the same stride m_ch are computed alongside the per-step versions, so that a difference between D3 and D1/D2 cannot be produced by temporal smoothing alone. A chunked distance over [τ, τ + m_ch) uses the vector sum of the updates in the chunk (pre-decay for D1_rel and D2), weighted with the layer norms at τ (D1_rel) or with v̂(τ − L) (D2). Sensitivity: m_ch ∈ {1, 4, 8, 16, 32, 64} on 5 calibration runs (m_ch = 1 over a 2,048-step window). m_ch = 8 is adopted if, for D3, the within-run Spearman correlation between Δc_e at m_ch = 1 and m_ch = 8 across intervals is ≥ 0.98 and their ΔR² differ by ≤ 0.01; otherwise m_ch = 4 (with \|R\| reduced to 128 if needed for cost).
- **R is a battery of forgotten inputs.** R is never retrained after childhood. At Stage 0 its mean loss passed the chance level (ln 64 ≈ 4.2 nats) after 400–800 life steps and reached 7–8 nats after ≈ 2,000 steps, in every family. Throughout almost all of life, D3 and D4 therefore measure the change of the outputs, and C10 and C10b the change of the loss, on inputs that are not being trained, which is the regime of the forgotten target tasks themselves. The v0.3 stationarity check (mean D3 rate in the fourth quartile of life within ±20% of the first) is **withdrawn**: R is forgotten within the first quartile, so the check cannot detect the loss of sensitivity it was meant to detect; at Stage 0 the D3 rate fell by 30–42% from the first to the fourth quartile while D1_rel fell by 46–55%, which indicates a slowing of change, not an insensitive battery. The v0.3 remedy (R_maint rehearsed with one batch every 512 steps, R_eval never trained) is **withdrawn**: one batch every 512 steps cannot maintain fact items that are forgotten within 1,000–2,000 steps, and R_eval would be forgotten in any case. The quartile rates of D3 and of D1_rel, and their ratio, are reported descriptively.
- **Moment-reset diagnostic (calibration only).** On 4 calibration runs, a forked copy resets the optimizer moments at every segment boundary; the change in the per-step rate of each candidate D is reported, to show how much of ρ is carried by optimizer state rather than by the parameters.
- **D\*** is the single D used in the confirmatory tests. It is chosen among D1, D1_rel, D2 and D3 on calibration runs, out of fold (§12a), as the one with the largest incremental validity over B_strong (§7), and is frozen before any test run.

### 5.2 Net displacement and its storage

Disp^D(t₀, t₁) = D(S(t₀), S(t₁)), evaluated at grid points: ‖θ(t₁) − θ(t₀)‖₂ for D1; the layer-wise relative form with the layer norms at t₀ for D1_rel; (Σ_i v̂_i(t₀)(θ_i(t₁) − θ_i(t₀))²)^{1/2} for D2; and the D3 and D4 distances between the cached outputs at t₀ and the outputs at t₁. The cached object per active task exposure is:

| D | Cached at t₀ | Numbers per t₀ |
|---|---|---|
| D1, D1_rel | θ(t₀) (and layer norms) | ≈ 0.93 M |
| D2 | θ(t₀) and v̂(t₀) (Fisher weight anchored at t₀, as in EWC) | ≈ 1.9 M |
| D3 | answer-position output distributions on R | 256 × 512 ≈ 0.13 M |
| D4 | final-layer answer-position representations on R | 256 × 128 ≈ 0.03 M |

A snapshot of task k is overwritten at its next exposure, so at most K ≤ 40 snapshots are active. Storage ratios in H2 are reported per D (of order 10⁻⁵ to 10⁻⁶ in Stage A). The path metric of D2 is lagged while its displacement is anchored at v̂(t₀); if D\* = D2, the metric-free Disp^{D1} is reported alongside, so that a difference between path and displacement is not confused with the choice of curvature anchor. On test runs, snapshots are kept only for D\*; C8b and C9 are evaluated on a subsample of 30 test runs (§14).

## 6. Targets

**T1 (primary): forgetting.** For each target task k and each exposure segment of k (training, re-exposure, or rehearsal) ending at step s₀, let t₀ be the evaluation immediately after s₀. For every evaluation time t₁ > t₀ strictly before the first step of the next segment that trains k:

  F_k(t₀, t₁) = L̄_A,k(t₁) − L̄_A,k(t₀),

where L̄_A,k is the mean cross-entropy on probe half A of task k.
- **Inclusion:** a triplet is included only if the probe-**B** accuracy of task k at t₀ is ≥ 0.90; either ΔN = N(t₁) − N(t₀) ≥ 64, or ΔN = 0 and Δc_a ≥ 64 ticks (idle intervals); and ΔN < ΔN_max = 1,280. Excluded triplets are counted and reported by reason.
- **Cap on ΔN.** At Stage 0 (fact tasks only, η₀ = 3 × 10⁻⁴), functional forgetting was nearly complete at ΔN ≈ 1,280: the episode-weighted mean of ΔAcc_A reached 0.90 in the band [1,280, 1,536) and 0.96–0.98 beyond 2,048. Beyond that point F_A kept rising, to ≈ 9 nats, far above chance, but it moved with the loss on the forgotten battery R at t₁, a level shared by all inputs that are not being trained, rather than with the forgetting of task k; in v0.3 runs these intervals carried ≈ 20% of the weight but 32–64% of the within-run variance of F_A. The cap was set by a rule written down before the runs that determined it (the smallest multiple of 256 at which the band mean of ΔAcc_A reaches 0.90, on F2 and F3 technical runs that are not calibration runs) and is frozen as a number. On those runs it kept every exposure episode (r_AB ≥ 0.98). The H1 statistic without the cap (all evaluation times before the next exposure, with their own weights) is reported as a sensitivity analysis.
- **Unit of observation:** the triplet (k, t₀, t₁). **Unit of inference:** the run.
- **Weighting:** each exposure episode (k, t₀) carries equal total weight within its run: w = 1 / (E_r · M_{r,k,t₀}), where E_r is the number of valid episodes in run r and M_{r,k,t₀} the number of evaluation times of that episode. The same weights are used in model fitting (`sample_weight`) and in R²_r.
- **Strata (descriptive).** The H1 statistic is also reported by tercile of ΔN (below the cap).

**T1-acc (secondary): bounded forgetting.** ΔAcc_A,k = Acc_A,k(t₀) − Acc_A,k(t₁) on the same triplets. It checks that an effect on T1 reflects functional forgetting rather than logit-scale drift. The H1 statistic is reported for T1-acc descriptively.

**T2 (secondary): behavioural drift.** The √JS distance between the outputs of S(t₀) and S(t₁) on B_beh. It is reported descriptively. T2 is structurally favourable to Disp^{D3}, so it is not used for confirmatory claims.

**T3 (Stage B): retention.** The time-averaged probe-B accuracy over all learned tasks during the life phase, at a fixed rehearsal budget.

## 7. Predictor sets and competitors

All interval quantities are sums over τ ∈ (N(t₀), N(t₁)]. Every competitor is agent-available online and costs ≤ 2 stored scalars per t₀. Δθ_τ means the update before the decoupled weight-decay term (Δθ^pre_τ) unless stated otherwise.

**Covariates X_cov, given to every model** (agent-observable only):
- L̄_B,k(t₀) and Acc_B,k(t₀) (competence at t₀, from half B);
- L̄_B,k at the start of the exposure segment ending at s₀ (prior mastery, a proxy for novelty);
- input overlap of task k with the agent's history: 1 − √JS(q_k, q_hist(t₀)), where q_k is the distribution of the task's input **pairs** (key pairs; task tokens and `→` excluded) and q_hist(t₀) the cumulative distribution of input pairs from the first step of life up to t₀ (one counter over input pairs);
- N(t₀), absolute run progress; task tenure N(t₀) − N(t_first,k), with t_first,k the evaluation after task k's first training segment; number of prior exposures of k; number of active learned tasks K_active(t₀);
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
| C7a | number of segment boundaries (§4.3) and of agent-triggered rehearsals | agent-observable event counts |

**B_strong** (confirmatory baseline) = X_cov ∪ B_standard ∪:

| Code | Predictor over (t₀, t₁] | Source |
|---|---|---|
| C5a | Σ ‖g̃_τ‖₂ (clipped) | gradient actually used by the optimizer |
| C5b | Σ η_τ ‖g_τ‖₂, Σ η_τ ‖g̃_τ‖₂, Σ η_τ L_τ | within-step products that interval sums cannot recover |
| C5c | Σ η_τ² ‖g̃_τ‖₂², Σ \|⟨g̃_τ, Δθ_τ⟩\| | squared-gradient accumulator; path-integral work of Synaptic Intelligence (Zenke et al. 2017) |
| C5d | Σ η_τ ‖m̂_τ‖₂ | learning-rate-weighted momentum norm (the same-step D2 identity, §5.1) |
| C5e | Σ ‖m̂_τ‖₂ | unweighted momentum norm |
| C5f | Σ η_τ λ ‖θ^dec_τ‖₂, with θ^dec the decayed parameters | path length of the decoupled weight-decay term |
| C2b | Σ η_τ / B_τ | noise-scale-weighted steps |
| C6 | mean and SD (population, ddof = 0) of ‖Δθ_τ‖₂ over the first W_eff and the last W_eff steps of (t₀, t₁], with W_eff = min(16, ⌊ΔN/4⌋), windows clamped inside the interval; computed for the pre-decay and for the post-decay update; all set to 0 when ΔN = 0 | local update statistics (closed study; criterion (a)) |
| C6b | ‖θ(t₁)‖₂ − ‖θ(t₀)‖₂ and √Tr v̂(t₁) − √Tr v̂(t₀) | state-scale drift (signed) |
| C10 | L_R(t₁) − L_R(t₀): change of the mean loss on the reference battery R | canary loss (signed); 1 stored scalar per t₀ |
| C10b | Σ over chunks of \|L_R(τ + m_ch) − L_R(τ)\|, from the same forward passes as D3 | accumulated unsigned canary change: path accumulation on R without the √JS distance |
| rates | Z / max(ΔN, 1) for Z ∈ {C2, C2b, C3, C4, C5, C5a, C5b, C5c, C5d, C5e, C5f, C10, C10b} (the rate of C10 is signed) | computed, not stored |

**Why two baselines.** B_strong is deliberately close to a reconstruction of c_e from cheap telemetry, so that a positive H1 cannot be explained by an omitted product of learning rate and gradient, by momentum, by weight decay, by norm drift, by local statistics, or, for D3, by path accumulation of a cheap loss on R. Claimed advantages over under-trained baselines often vanish when the baseline is trained properly (Mukhoti et al. 2018); the closed study documented the same failure for an information-matched control. B_standard is reported so that readers can see how much of any gap is closed by the specialised competitors. If c_e beats B_standard but not B_strong, the result is reported as *reconstructible from cheap telemetry*, not as support.

**B_strong⁺ (exploratory sensitivity).** Further norm- and preconditioner-scaled accumulators (Σ η‖m̂‖ / ‖θ‖, Σ η‖m̂‖ / √(Tr v̂ / P), and the ratio of lagged to current Tr v̂) are reported as a sensitivity baseline, not in the confirmatory comparison.

**Reference predictors** (not agent-available, or of high storage; used to bound, not to compete; exploratory):

| Code | Predictor | Storage |
|---|---|---|
| C7b | separate counts of new-task and re-exposure segments (oracle labels) | world metadata |
| C8 | Σ over intervening tasks j of key overlap(k, j) × steps on j | world metadata (Lee, Goldt and Saxe 2021, arXiv:2107.04384) |
| C8b | Disp^{D2}(t₀, t₁) with v̂(t₀), Fisher-weighted displacement (EWC: Kirkpatrick et al. 2017) | ≈ 1.9 M per t₀ |
| C9 | First-order response ⟨∇_θ L_train,k(S(t₀)), θ(t₁) − θ(t₀)⟩, with the gradient computed on task k's **training items only**, never on probe half A (cf. Su and Zhang 2026; Jin and Ren 2024) | ≈ 1.9 M per task |
| C8b + C9 | Second-order Taylor reference, from the same cached objects; reported alongside each alone | ≈ 2.8 M per task |
| Ceiling | Reliability of the half-A target: within-run, episode-weighted correlation r_AB between F_A and F_B on the same triplets (weights of §6), **uncorrected** (the target uses one half) | — |

## 8. Prediction models and competence audit

- **Primary model family:** gradient-boosted regression trees (scikit-learn `HistGradientBoostingRegressor`), `max_features = 1.0`, `max_bins = 255`. Monotone constraints (`monotonic_cst`, applied to every column of a multi-column code): +1 for C0, all four terms of C1, C2, C2b, C3, C4, C5, C5a–C5f, C10b, Δc_e, Disp, and, in exploratory reference models, C8 and C8b; 0 for C7a, C6, C6b, C10, all rates (including ρ̄ and the rate of Disp), all of X_cov, and, in exploratory models, C7b and C9. An unconstrained fit (`monotonic_cst = None`) is reported as a sensitivity check.
- **How c_e and Disp enter.** Adding c_e to a predictor set adds the pair {Δc_e^{D\*}, ρ̄^{D\*} = Δc_e^{D\*} / max(ΔN, 1)}, at no extra storage; Disp^{D\*} enters the same way. c_e thus has the same representation as every competitor in B_strong, and H1 tests the quantity that G2 audits. Because ΔN is in B_strong, ρ̄ is a deterministic function of Δc_e and ΔN, so the pair adds one degree of freedom; the rate is given explicitly because trees cannot form ratios, and G2 audits exactly that degree of freedom.
- **Search space** (the same for every predictor set): `learning_rate` ~ LogUniform[0.01, 0.2]; `max_iter` ∈ {100, 200, 400}; `max_leaf_nodes` ∈ {15, 31, 63}; `min_samples_leaf` ∈ {20, 50, 100}; `l2_regularization` ~ LogUniform[10⁻⁴, 10].
- **Secondary model family:** ridge regression with log1p applied to raw positive interval sums (including ΔN and Δc_e), the same shifted-log basis for Δc_e as for ΔN (knots scaled by the mean training-run increment per step), the rates as linear terms, sign(x)·log(1 + \|x\|) for signed predictors (C6b, C10, C9), pairwise interactions between each interval predictor and each variable of X_cov, a `StandardScaler` fitted on training runs, and λ chosen by cross-validation grouped by run.
- **Equal tuning budget:** every predictor set receives the same random search, 50 configurations, on validation runs, with the same seeds. The best configuration of B_strong is always included as a candidate for B_strong + c_e. The **locked-hyperparameter** ΔR² (both sets fitted with the B_strong configuration) is the confirmatory statistic; the re-tuned ΔR² is reported alongside. **Divergence rule:** if the locked and the re-tuned ΔR² lead to different outcomes and differ by more than 0.01, H1 is reported as *inconclusive (sensitive to hyperparameters)*, never as closing Level 2.
- **Fitting:** models are fitted on pooled, weighted triplets from the training runs and evaluated on test runs. No test-run information is used in fitting, selection, or transformation. **Training-sample variance:** for both model families, 250 bootstrap resamples of the training runs (with replacement; refitted with locked hyperparameters; any cross-validation grouped by original run) are evaluated on the test runs, and the confirmatory interval resamples training replicates and test runs jointly (§10.1). Quantities on calibration runs are computed out of fold (§12a).
- **Skill per test run r:** weighted R²_r = 1 − SSE_r / SST_r, with SST_r around the weighted mean of run r. Weighted Spearman ρ_S,r and MAE_r are reported alongside.
- **Decomposition (reported, not confirmatory):** within-episode skill, with SST computed around the mean of each episode (k, t₀) across its t₁; and partial skill [SSE_r(B_strong) − SSE_r(B_strong + c_e)] / SSE_r(X_cov).
- **Stage B deployment model.** The predictors used by S-pred in Stage B are fitted separately on the same Stage A training runs, with the competence covariates computed as Stage B computes them online (loss and accuracy over the last epoch of the segment, and over its first epoch for prior mastery), and without the inclusion filter. Their in-loop calibration (MAE and ρ_S against half-A probes) is logged during Stage B.

## 9. Stage B: use by the agent

Stage B is run only if H1 is supported (§10.1).

- **Budget.** The rehearsal budget is fixed per run: K_reh = Q / L_reh rehearsal segments of L_reh = 64 steps over the life phase. The budget is a **hard cap**, and every scheduler spends exactly Q on every run (asserted per run; gate G7).
- **Decision grid.** Every scheduler, including S-pred and S-oracle, decides only on the 64-step grid; S-pred scores all active tasks in one batched call per decision.
- **Pacing.** A threshold scheduler triggers a rehearsal when its statistic since the last rehearsal reaches θ_eff(N) = θ_cal · [(N_life − N) / N_life] / max(ε, (K_reh − k_spent(N)) / K_reh), with ε = 1 / (2 K_reh). Spending ahead of schedule raises the threshold; falling behind lowers it. When the remaining life steps fall to the remaining budget, all remaining rehearsals are executed (terminal flush). θ_cal is calibrated separately for each threshold scheduler on validation runs, to minimise the mean absolute deviation between cumulative spending k_spent(N)/K_reh and uniform spending N/N_life; the terminal flush must average ≤ 5% of K_reh on validation runs, and its size is logged per run (G7).
- **Schedulers.** By the identification note (§2), schedulers differ in **when** they spend the budget, and in which task only through a learned predictor that includes covariates.

| Scheduler | Rule |
|---|---|
| S-uniform | One rehearsal segment every ⌊N_life / K_reh⌋ optimizer steps (rounded to the grid); task chosen least recently rehearsed |
| S-c_e | Rehearsal triggered when Δc_e^{D\*} since the last rehearsal ≥ θ_eff; task least recently rehearsed |
| S-C2, S-C3, S-C4, S-C5, S-C5b, S-C7a | As S-c_e, with the trigger on tokens, cumulative LR, cumulative loss, gradient norm, LR-weighted clipped gradient norm, or event counts |
| S-pred(B_strong) | The Stage B deployment model on B_strong (§8) scores every task; a rehearsal is triggered when the increase in total predicted forgetting over active tasks since the last rehearsal reaches θ_eff, and the task with the largest predicted forgetting among tasks with ΔN ≥ 64 is rehearsed |
| S-pred(B_strong + c_e) | Same, with {Δc_e^{D\*}, ρ̄^{D\*}} added (information-matched pair) |
| S-oracle | Rehearse the task with the largest true current forgetting on half B, evaluated on the decision grid (upper bound) |
| S-random | Random times and tasks, same budget |

- **Relation to FOREVER.** With D\* = D1, S-c_e is a trigger on the clock of Feng et al. (2026). An exploratory arm S-FOREVER applies their schedule (replay when c_e^{D1} since the end of a task's training reaches d · τ_day, with τ_day the change over the first 24 steps and d ∈ {1, 2, 4, 7, 15, 30, …}), under the same budget cap and pacing.
- **Comparator selection.** The single best trigger competitor S-C\* is chosen among S-uniform, S-C2, S-C3, S-C4, S-C5, S-C5b and S-C7a on **validation runs**, frozen, and evaluated once on test runs.
- **Task-selection check.** On validation runs, S-pred(B_strong) and S-pred(B_strong + c_e) must select a task other than the least recently rehearsed one on at least 10% of rehearsals. Otherwise H4a is reported as a duplicate of the timing test H4b, not as a test of task selection.
- **Online covariates.** In Stage B, competence covariates at t₀ are computed online from the training batches, as in the deployment model (§8). T3 uses half B only, and no scheduler except S-oracle reads any probe.
- **Placebo for reliance (G8).** Information that is decodable need not be used (Elazar et al. 2021); reliance is therefore tested by intervention. For each Stage B test seed, the live run of S-c_e (or of S-pred(B_strong + c_e)) is executed first. Its realised per-step c_e increments, cut into 256-step blocks with idle zeros kept in place, are permuted with a fixed seed and fed online, step by step, to a placebo twin with the same seed. For S-pred, the permuted quantity is the out-of-fold residual of Δc_e given B_strong, so that the feature pairs stay within the range seen in training. A cross-seed yoked stream from the same family, aligned by N, is run as a robustness check.
- **Logged:** realised rehearsal steps and terminal-flush size per run; Wasserstein distance between the trigger times of S-c_e and of S-C\* (when); task agreement at matched times (which); in-loop calibration of S-pred.

## 10. Hypotheses

### 10.1 Decision rules

- **One-sided level:** α = 0.025 per side for every test. Each hypothesis is decided from a single two-sided (1 − 2α_adj) BCa bootstrap confidence interval (10,000 resamples over the resampling unit; for Stage A statistics, each draw resamples the test runs within family strata and pairs them with one of the 250 training-run replicates of §8, drawn uniformly; the BCa acceleration is estimated by the jackknife over test runs), where α_adj is the level assigned to it by the procedure below:
  - **supported** if the lower bound is > δ (minimal-effect test);
  - **equivalent** if the whole interval lies within (−δ, δ) (TOST, each side at α_adj; Lakens et al. 2018; for stochastic machine-learning experiments, Knopov and Shvai 2026);
  - **inconclusive** otherwise.
  H2 uses the non-inferiority rule of §10.2, because its margin is built into its contrast.
- **Multiplicity (fixed sequence, then Holm).** H1 is tested first at α = 0.025. Only if H1 is supported are H2, H4a and H4b tested, as a Holm family at α = 0.025: ranked by their one-sided bootstrap p-values, the j-th is tested at α_adj = 0.025 / (3 − j + 1). This controls the family-wise error rate. If H1 is equivalent or inconclusive, H2–H4 are not tested confirmatorily and Stage B is not run. The family checks of §10.2 (F1, F5, F6) are interpretation conditions, not members of the Holm family; each uses one-sided α = 0.025.
- **SESOI (rule frozen now, value computed on calibration runs and frozen before test):** δ = max(0.02, min(0.05, 0.15 × [ceiling − R̄²_cal(B_strong)])), where the ceiling r̄_AB (G1) and R̄²_cal(B_strong) are averaged over the F2–F3 calibration runs, out of fold (§12a). Raw ΔR² and ΔR² as a fraction of the headroom are both reported. Stage B: δ_B = 2 percentage points of T3.

### 10.2 Confirmatory hypotheses and family checks

| | Statement | Statistic | Resampling unit |
|---|---|---|---|
| **H1** | Adding c_e to B_strong increases held-out skill on T1 | Mean over the H1 test runs (**F2 and F3**, pooled) of the locked-hyperparameter ΔR²_r = R²_r(B_strong + c_e) − R²_r(B_strong), where "+ c_e" adds {Δc_e^{D\*}, ρ̄^{D\*}} | test run, stratified by family |
| F5 replication | The H1 effect generalises across generator parameters | The same statistic on F5 test runs; **passed** if the lower bound is > 0 | F5 test run |
| F6 adversarial check | c_e is not misleading under change without interference | The same statistic on F6 test runs; c_e is **misleading under drift** if the upper bound is < 0 | F6 test run |
| F1 positive control | Counts suffice in the natural stream | The same statistic on F1 test runs, reported alone; equivalence is the expected result | F1 test run |
| **H2** | The scalar index retains at least 80% of the displacement's incremental value | Z̄ = mean over the H1 test runs of Z_r = ΔR²_r(c_e) − 0.80 · ΔR²_r(Disp^{D\*}). **Supported** (retains ≥ 80%) if the lower bound of Z̄ is ≥ 0; **refuted** (retains < 80%) if the upper bound is < 0; inconclusive otherwise. Tested only if G2b passes. The ratio of means and its Fieller interval are reported descriptively | test run, stratified by family |
| **H4a** | c_e helps a covariate-aware rehearsal predictor | Mean paired difference in T3, S-pred(B_strong + c_e) − S-pred(B_strong); SESOI δ_B | matched Stage B seed pair |
| **H4b** | c_e suffices as a standalone rehearsal trigger | Mean paired difference in T3, S-c_e − S-C\*; SESOI δ_B | matched Stage B seed pair |

### 10.3 Optional exploratory module H3 (path dependence)

H3 is **not** part of the confirmatory study. Its design is preregistered here so that it cannot be tuned after the fact, but it is run only if H1 is supported and the compute budget of §12a remains after Stages A and B (it needs about 120 runs, comparable to the whole Stage A test set). If run, it is reported as exploratory.

The v0.1 design (segments X and Y with high and low key overlap with k) is withdrawn: a global index cannot encode *which* task a stretch of change interfered with, and recency can reverse the sign of the order effect. The redesign varies a **global** property:
- **Blocks.** From one saved state S(t₀) after task k is learned (θ, m, v, data-generator state), two branches are forked. There are 30 saved states, each forked under 2 independent mini-batch permutation seeds (60 matched pairs). Segment A trains a new task with the same input-token overlap with k as segment B; segment B re-exposes already-mastered data. A two-stage learning-rate schedule (η_high, then η_low) is fixed. Branch 1: A at η_high, then B at η_low. Branch 2: B at η_high, then A at η_low. Steps, tokens, batches, the multiset of examples, Σ η, and C7a are identical across branches.
- **Statement.** Across matched pairs, the order-induced difference in forgetting of k, ΔF, has a positive Spearman correlation with the order-induced difference Δ(Δc_e^{D\*}).
- **Decision (descriptive labels).** Supported if the lower bound of the 95% bootstrap interval (resampling unit: the matched pair) is > 0.20; equivalent if the interval lies within (−0.20, 0.20); not part of the confirmatory family.
- **Comparator.** The same correlation is reported for C5b (Σ η‖g̃‖), which is also order-sensitive. H3 shows that c_e tracks a path effect invisible to order-invariant counts; it does not, by itself, show an advantage over order-sensitive telemetry.

### 10.4 Exploratory, labelled as such

D comparisons beyond D\*; the SGD arm; T1-acc and T2; C7b, C8, C8b and C9 bounds; single-competitor comparisons; B_standard comparisons; scale-drift robustness checks; per-family results other than those named above.

## 11. Gates

| Gate | Check | Criterion | Consequence of failure |
|---|---|---|---|
| G1, ceiling | Within-run, episode-weighted correlation r_AB between F_A and F_B (weights of §6), uncorrected, on calibration runs | r̄_AB ≥ 0.70 on F2–F3 | Increase probe-set size before freeze; report all skills also as a fraction of r̄_AB |
| G2, identifiability | Out-of-sample R² for predicting the interval rate ρ̄ = Δc_e^{D\*} / max(ΔN, 1) from B_strong, with OLS and with GBDT: at Stage 0 by cross-fitting on the F2–F3 calibration runs (§12a); at Stage A fitted on training runs and evaluated on test triplets of F2, F3, F5, F6 and of F5 alone | Both R² < 0.90 | H1 is reported as *not identifiable*, never as equivalence |
| G2b, H2 denominator | Mean ΔR² of Disp^{D\*} over B_strong on the H1 test runs (F2 and F3) | Lower bound of the two-sided 95% BCa interval > 0.02 | H2 is reported as *not identifiable* |
| G3, competence and headroom | On calibration runs, out of fold (§12a), verified on validation runs: B_strong beats X_cov alone in F1; headroom = r̄_AB − R̄²(B_strong) on F2–F3 | ΔR² ≥ 0.10; headroom ≥ 2.5 δ | Redesign the target or the stream before freeze |
| G3b, baseline saturation | On calibration runs, out of fold: B_strong re-tuned with a doubled search (100 configurations instead of 50), same seeds for the first 50 | Change in mean R²(B_strong) ≤ 0.01 | The baseline is under-tuned: increase the search budget for every predictor set before freeze; if not achievable, H1 may not be reported as supported |
| G4, leakage and placebo | R ∩ probes = ∅, and V_target, V_ref and V_distractor pairwise disjoint (asserted in code); incremental value over B_strong of a **block-permuted** c_e: per-step increments are cut into 256-step blocks (idle zeros kept in place), the blocks are permuted **across the runs of the same family**, so that no run keeps its own mean rate, the index is re-accumulated per run, and the model is **refitted** on training runs with locked hyperparameters and evaluated on test runs. Checked at Stage 0 (out of fold) and at Stage A, within each family | Point estimate ≤ 0.005 and upper bound of the one-sided 95% interval < 0.015 | Stop; leakage or a design artefact |
| G4b, positive control (sensitivity) | On calibration runs only, out of fold: a synthetic predictor Z = e + ξ is added to B_strong, with e the out-of-fold residual of T1 given B_strong and ξ independent Gaussian noise of per-run variance σ²_ξ,r = s²_e,r [(1 − R²_r(B_strong)) / (2δ) − 1], s²_e,r the episode-weighted residual variance, so that the expected within-run ΔR² is 2δ. Z has monotonic_cst = +1. The full pipeline (weighting, locked hyperparameters, GBDT, bootstrap, decision rule) is applied | Estimated ΔR² in [1.25δ, 2.5δ], and outcome *supported* | The pipeline cannot detect an effect of the size sought: fix the pipeline before freeze. If it still fails, an *equivalent* outcome of H1 may not be reported as closing Level 2 |
| G5, local statistics | R̄²(X_cov + c_e) versus R̄²(X_cov + C6) on the H1 test runs, both models tuned with the same 50-configuration search | Lower bound of the one-sided 95% interval of the difference > 0 | c_e is reported as failing admissibility criterion (a), whatever H1 shows |
| G6, onset versus skill | H1 statistic with the number of training runs halved and doubled; Stage B deployment models fitted on the doubled Stage A training set (60 runs) | No flip between *supported* and *equivalent*, and \|change in mean ΔR²\| ≤ 0.01 | Report as onset-dependent |
| G7, reproducibility and budget | Bit-identical reruns of a random 5% of runs; configuration hashes verified before analysis, both of the configuration file and of the resolved configuration with its overrides (`config_resolved_sha256`); after any change of hardware, a bit-identical rerun of at least one completed run before further runs; realised rehearsal steps = Q on every Stage B run, with the terminal flush logged | 100% | No analysis until fixed |
| G8, reliance | For S-c_e and S-pred(B_strong + c_e): paired difference T3(live) − T3(placebo twin) over Stage B seeds (§9) | Lower bound of the one-sided 95% interval > 0, and point estimate ≥ δ_B / 2 | c_e is decodable but not used |
| G9, H3 identifiability | Split-half reliability (A vs B) of ΔF across matched pairs; cross-seed reliability of Δ(Δc_e^{D\*}) between the two seeds of each saved state; variation SD(Δ(Δc_e^{D\*})) / mean of the branch-average Δc_e^{D\*} | ≥ 0.50; ≥ 0.50; ≥ 0.05 | H3 is reported as *not identifiable* |

## 12. Data splits and sample size

- **Calibration runs:** 24 (8 per F1–F3), used only in Stage 0 (§12a): G1, G2, G3, G3b, G4, G4b, the SESOI value, D\*, m_ch, the quartile rates of D3 and D1_rel (descriptive, §5.1), the moment-reset diagnostic, the variance of the test statistics, and threshold design. All model-based quantities on them are out of fold (§12a). They are discarded afterwards and never enter test statistics.
- **Training runs:** F1–F3, 30 base. For G6 the models are refitted on 15 of them and on 60 (the 30 base runs plus 30 additional runs), so there are 60 training runs in total. **Validation runs:** F1–F3, 15. **Test runs:** new seeds of F1, F2, F3, F4 (sanity), F5 and F6. O blocks are used only for H3 and G9 (30 saved states × 2 seeds).
- **Sample size for H1** (F2 and F3). Let σ̂_up be the upper 80% chi-square confidence bound of the SD of per-run ΔR² on the F2–F3 calibration runs (out of fold). For TOST at a true ΔR² of 0 and for the MET at a true ΔR² of 2δ (an effective shift of δ from the boundary δ), each at power 0.80 and one-sided α = 0.025 (for TOST the type II error is split between the two sides, hence z_0.90):
  - n_TOST = ⌈(z_0.975 + z_0.90)² (σ̂_up/δ)²⌉ = ⌈10.51 (σ̂_up/δ)²⌉;
  - n_MET = ⌈(z_0.975 + z_0.80)² (σ̂_up/δ)²⌉ = ⌈7.85 (σ̂_up/δ)²⌉;
  - n_H1 = max(n_TOST, n_MET), split equally between F2 and F3.
- **Family checks.** n_F5 = n_F6 = n_MET, which gives the F5 replication test (lower bound > 0) and the F6 check (upper bound < 0) power 0.80 at a true effect of ±δ. n_F1 = 10 and n_F4 = 5, reported descriptively.
- **Total.** N_test = n_H1 + n_F5 + n_F6 + n_F1 + n_F4 ≤ 200 (budget cap). If the cap is exceeded, the scope is reduced before freeze, first by dropping F6, then F5 (whose replication check is then reported as underpowered), and the reduction is declared in the Stage 0 report. If n_H1 alone exceeds 200 − n_F1 − n_F4, H1 cannot be run at the prespecified SESOI: the study stops at Stage 0 and the reason is reported (§12a). The SESOI rule is not relaxed.
- **Sample size for H2.** With σ̂_up(Z), the upper bound of the SD of Z_r on calibration runs, and the margin δ_H2 = max(0.01, 0.20 · ΔR̄²_cal(Disp^{D\*})): n_H2 = ⌈(2.394 + z_0.80)² (σ̂_up(Z)/δ_H2)²⌉ = ⌈10.47 (σ̂_up(Z)/δ_H2)²⌉ (non-inferiority at the first Holm level, one-sided α = 0.025/3, true Z = δ_H2). If n_H2 > n_H1, H2 is reported as underpowered.
- **Sample size for H4a, H4b.** With δ_B and the upper bound of the SD of paired Stage B differences, the larger of TOST and MET at the first Holm level: n = ⌈(2.394 + z_0.90)² (σ̂_up/δ_B)²⌉ = ⌈13.5 (σ̂_up/δ_B)²⌉ (the MET alone would need 10.47). Stage B uses n_B = max(40, n) paired seeds per scheduler, frozen after the power simulation; if the compute budget cannot accommodate n, H4a and H4b are reported as underpowered.
- **Power simulation.** Before freeze, these closed-form sizes are checked by simulation on calibration data, with the weighted R², the stratified bootstrap with training-run replicates, the fixed-sequence and Holm procedure, and the separate family checks.
- **Fixed sizes (indicative; frozen after the power simulation):** calibration 24 runs (8 per F1–F3); training 60 (30 base and 30 more for G6); validation 15; O blocks 30 saved states × 2 seeds; Stage B max(40, n_H4) paired seeds per scheduler.

## 12a. Stage 0: calibration and go/no-go decision

Stage 0 uses technical runs (13 by v0.4: the withdrawal of the rule tasks required a further round; §21), followed by the 24 calibration runs of §12. It measures and decides; it tests no hypothesis. The author decides after Stage 0 whether to continue. Continuation requires all of the following; otherwise the design is simplified again or the study stops, and the decision is reported.

**Out-of-fold scheme.** All model-based quantities on calibration runs (G2, G3, G3b, G4, G4b, the SESOI value, σ̂_up, σ̂_up(Z), and the choice of D\*) are computed by 4-fold cross-fitting at the run level, stratified by family (18 runs for fitting and 6 for evaluation in each fold), with hyperparameters chosen by an inner 3-fold cross-validation on the fitting runs.

| Criterion | Requirement |
|---|---|
| Target measurable | G1 passed (r̄_AB ≥ 0.70 on F2–F3); at least 20 valid exposure episodes per run; forgetting with non-negligible variance |
| Index not reconstructible | G2 passed on the F2–F3 calibration runs (interval rate, OLS and GBDT) |
| Headroom | G3 passed (headroom ≥ 2.5 δ) |
| Baseline and pipeline | G3b passed (baseline saturated); G4 passed (no leakage; placebo null); G4b passed (positive control detected) |
| Index and battery | D\* and m_ch selected and frozen; quartile rates of D3 and D1_rel recorded (§5.1); G5 and G2b recorded for D\* |
| Cost | Measured on the calibration campaign, on the declared machine (§14), with the number of workers that maximises throughput: throughput ≥ 6 full runs per wall-clock hour; projected wall-clock time ≤ 72 h for Stage A (calibration, training, validation, test and G7 runs, plus model fitting) and ≤ 120 h for Stage B; an interrupted campaign is resumed by repeating its command (completed runs are verified and skipped; a run cut off is redone from its start, bit-identically); parallel runs bit-identical (G7). Core-hours are reported but are not a criterion: under a memory-bandwidth limit they fall with fewer workers while wall-clock time rises (§14, §21) |
| Sample size | N_test (§12) ≤ 200 for the declared set of families |

The feasibility of the full design is not assumed: full runs were measured on technical runs (§14), and the cost criterion is checked again on the calibration campaign.

**Stage 0 report.** The values frozen at Stage 0 (η₀, ΔN_max, δ, D\*, m_ch, σ̂_up, the sample size per family), the measured cost and all gate results are written to a report that is deposited with the preregistration (§17).

## 13. Stage C: transfer to pretrained language models

Stage C keeps the **question and the inferential logic** (B_strong versus B_strong + c_e, three-way outcomes, gates). It does **not** keep every operational definition, and it is **not part of this preregistration**. A separate Stage C adaptation document will be frozen and deposited with its own DOI before any Stage C run. Its cost is not included in §14. Changes already known:
- **Agent.** Publicly available pretrained causal LMs (the Pythia family); a CPU feasibility check on the smallest model; the confirmatory model size and optimizer arm are named in the adaptation document before any Stage C run.
- **No childhood phase.** Pretraining replaces it; R is a fixed generic-text battery evaluated, not trained.
- **Targets.** T1 is the loss on held-out samples of earlier domains, read at fixed target positions. The accuracy-based inclusion criterion is replaced by a loss-based learned criterion defined in the adaptation document.
- **Covariates.** Domain identity is added; competence uses a held-out half of each domain's samples; C7a only (no oracle labels).
- **LoRA.** D is computed on the effective weight update ΔW_eff = (α/r)(B_{τ+1}A_{τ+1} − B_τ A_τ), not on the concatenated adapter matrices.
- **D3.** Restricted to a small number of target positions and to top-K or sketched distributions; the vocabulary of ≈ 50,000 tokens makes full distributions infeasible.
- **Displacement and C8b, C9.** Evaluated only for the smallest model, for LoRA, or for a subset of tasks, as offline references.
- **Task identity.** Stage A marks each task with a task token (task-incremental learning). Text domains in Stage C carry no such token (domain-incremental learning), and part of the measured forgetting can then be a misalignment of the output layer rather than a loss of knowledge (spurious forgetting; Zheng et al. 2025). The adaptation document states whether a domain token is given and reports a readout-realignment check.

**The adaptation document must fix, before any Stage C run:**
1. **Decision unit.** One primary confirmatory arm: a single named Pythia checkpoint, chosen by a timing check before any forgetting outcome is seen, adapted with LoRA and AdamW (the regime of FOREVER). Full fine-tuning of the smallest feasible model is secondary. If both are run and their three-way outcomes differ, Stage C is reported as regime-conditional, not as reproduction.
2. **Resampling unit.** A Stage C run is an independent seed controlling the draw and order of domain segments from a pool of at least 15 domains, disjoint document subsamples for training and for probe halves A and B, the stream schedule, and the initialisation of the adapters.
3. **LoRA distances.** D1 and D1_rel on ΔW_eff, computed through the rank-2r factorisation ‖ΔW_eff‖_F² = (α/r)² Tr(B̃ᵀB̃ ÃÃᵀ), with B̃ = [B_{τ+1}, −B_τ] and Ã = [A_{τ+1}; A_τ], without forming dense matrices; D2 and C5d in the adapter coordinates, where the optimizer moments exist.
4. **Top-K D3.** √JS on the union of the top-K tokens (K = 128) at both times plus one tail bucket, so that both distributions share a support and √JS remains a metric.
5. **Inclusion and covariates.** A loss-based inclusion criterion: a relative reduction of half-B loss over the exposure segment of at least γ_inc, calibrated so that r̄_AB ≥ 0.70; input overlap over a fixed histogram of the 4,096 most frequent tokens plus a tail bin.

The Stage A conclusions are claimed to generalise only if the primary Stage C arm reproduces the three-way outcome of H1.

## 14. Compute estimate

Measured at Stage 0 on the author's laptop: Intel Core i5-12500H (4 performance and 8 efficiency cores, 16 logical CPUs), 16 GB DDR4-3200 in a single module (single-channel memory), Windows 11; agent of §3 (925,952 parameters), single-threaded workers. A second memory module (dual channel) is planned before Stage A. Results do not depend on the memory configuration, only time does; after the change, throughput is measured again and a bit-identical rerun of completed runs is checked (G7).

| Workers in parallel | ms per training step (same step) | Training steps per second, all workers |
|---|---|---|
| 1 | 19–20 | ≈ 51 |
| 2 | 27 | ≈ 74 |
| 4 | 42–49 | ≈ 85–95 |
| 8 | 95–101 | ≈ 80–84 |

The limit is memory bandwidth (≈ 15–20 GB/s in total): operations on model-size vectors slow down ≈ 8× with 4 workers and ≈ 22× with 8, pure compute only ≈ 2×. Throughput is highest at about four workers.

| Item | Measured (technical runs) |
|---|---|
| One full run (childhood 3,072 steps, life 20,480 steps, all evaluations, D3, D4 and C10b every 8 steps, snapshots for every D), 4 workers | 23.6–25.2 min; 46 ms per training step; peak memory ≈ 0.82 GB per worker |
| Throughput | 9.5 runs per hour with 4 workers; 7.5 with 6 workers; 5.8 with 3 workers (the spread between rounds is not fully explained; the calibration campaign gives the reference measurement) |
| Split of one run (3 workers, 31 min) | life training 1,128 s; childhood 243 s; probe evaluations 241 s; D3, D4 and C10b 187 s; snapshots 65 s |
| Stage A (24 calibration + 60 training + 15 validation + ≤ 200 test + ≈ 16 G7 reruns ≈ 315 runs) | ≈ 33 wall-clock hours at 9.5 runs per hour (≈ 55 at 5.8), plus model fitting (measured with the analysis pipeline); ≈ 130 core-hours with 4 workers |
| Stage B (≈ 590 runs) | ≈ 62 wall-clock hours at 9.5 runs per hour (≈ 100 at 5.8) |
| C8b and C9 (exploratory) | on a subsample of 30 test runs |
| Stage C-mini (smallest Pythia model, CPU) | hours per run; feasibility only |

The v0.3 estimate (12–15 min per run, 9–11 wall-clock hours for Stage A on eight workers) assumed that eight workers scale; they do not (§21).

## 15. Interpretation table (frozen with the protocol)

"Gates passed" means G2, G3b, G4 and G5 passed. Rows on H1 are mutually exclusive.

| Outcome | Interpretation |
|---|---|
| H1 supported, gates passed, F5 replication passed, F6 upper bound ≥ 0 | Accumulated own change predicts own forgetting beyond clocks, counts, and a strong set of logged summaries; the result generalises across generator parameters and is not misleading under change without interference: first empirical support for the experiential index (Level 2) |
| H1 supported, gates passed, F5 replication passed, F6 upper bound < 0 | The index generalises across generator parameters and is useful where change and interference coincide, but misleading where they decouple; reported as a conditional result |
| H1 supported, gates passed, F5 replication not passed | The advantage does not generalise beyond the training generators; reported as a construction effect, not a general result |
| H1 lower bound > δ, but G3b failed | Not interpretable as support: the baseline was not saturated |
| H1 lower bound > δ, but locked and re-tuned outcomes diverge (§8) | Inconclusive: sensitive to hyperparameters |
| H1 equivalent, and G3b and G4b passed | Counts and logged summaries suffice; Level 2 is closed for this regime |
| H1 equivalent, but G4b failed | Not interpretable as closure: the pipeline could not detect an effect of the size sought |
| H1 inconclusive | Level 2 is unresolved at the prespecified sample size and SESOI; neither support nor closure is claimed, and Stage B is not run |
| c_e beats B_standard but H1 is equivalent | The information in c_e is reconstructible from cheap telemetry |
| G2 fails | Not identifiable in this design |
| G4 fails | Stop: leakage or a design artefact; no result is reported as a finding |
| G5 fails | c_e fails admissibility criterion (a), whatever H1 shows |
| G6 fails | The result is reported as onset-dependent |
| F1 alone | Equivalence on F1 is the expected result of the positive control and does not weaken H1 |
| H2 supported | The scalar index captures at least 80% of what full displacement captures, at the storage ratio reported for D\* |
| H2 refuted | Displacement carries information that the path index does not; the claim of a compact index is weakened |
| H2 inconclusive, or G2b fails | Neither a retention claim nor its rejection is supported |
| H3 supported (G9 passed; optional module) | The index tracks a global path effect invisible to order-invariant counts (exploratory) |
| H4a supported, G8 passed, task-selection check passed | The agent uses the index inside a covariate-aware predictor to improve a decision about itself |
| H4a supported, task-selection check failed | Reported as a duplicate of the timing test, not as evidence about task selection |
| H4b supported and G8 passed | The index alone suffices as a rehearsal trigger, beyond the best cheap trigger chosen on validation |
| H4a or H4b supported, but G8 failed | The gain does not depend on the temporal alignment of c_e: c_e is decodable but not used, and criterion (d) is not met |
| The primary Stage C arm reproduces H1 | The result is not an artefact of the synthetic world |

## 16. Threats to validity and mitigations

| Threat | Mitigation |
|---|---|
| Designer degrees of freedom in the stream families | F1 natural; F5 and F6 held out; F6 adversarial; families frozen; Stage C on real data |
| The mixture of families decides H1 | H1 confirmatory on F2 and F3 only; F1, F5 and F6 reported alone with prespecified checks (§10.2) |
| Omitted cheap competitor reconstructs c_e | B_strong with LR-weighted, momentum (weighted and unweighted), work, weight-decay path, norm, local and canary summaries (signed and accumulated); c_e and competitors on the same footing (raw and rate); G2 on the rate; B_standard reported; B_strong⁺ as sensitivity |
| Shared noise between predictors, inclusion, and target | Half B for covariates and inclusion, half A for the target; R and the three key vocabularies disjoint from probes and from each other; block-permuted placebo G4; T2 not confirmatory |
| Scale and weight-decay drift | D1_rel; C5f; C6b; N(t₀) and state norms in X_cov; T1-acc |
| The loss target keeps rising after functional forgetting is complete (a level shared by all untrained inputs, not forgetting of the task) | Cap ΔN < 1,280 (§6), set by a prior rule on technical runs; uncapped H1 statistic reported as sensitivity; T1-acc |
| The reference battery is forgotten early, so D3, D4, C10 and C10b read untrained inputs | Declared (§5.1); quartile rates of D3 reported next to D1_rel |
| Fact tasks only: the forgetting of a generalisation is not tested | Declared scope (§1, §4.1); Stage C on text domains |
| A change of hardware between stages | Results are bit-identical by construction; a rerun of completed runs is checked after the change (G7); throughput re-measured (§14) |
| Deterministic drift of unused parameters | Maximum context 8; no weight decay on biases and LayerNorm parameters |
| Local-statistics shortcut (closed study) | C6 with short clamped windows inside B_strong; G5 |
| Over-weighting of early tasks | Equal weight per exposure episode |
| Dependence of triplets within a run | Run-level inference; within-run weighted R² |
| Training-sample variance ignored | 250 training-run bootstrap replicates for both model families (§8) |
| Selection of D, m_ch or comparators after seeing results | D\*, m_ch and S-C\* chosen on calibration or validation and frozen |
| Hyperparameter locking hides an interaction | Divergence rule (§8); unconstrained sensitivity fit |
| Unequal rehearsal budgets and pacing artefacts | Hard cap; corrected pacing rule; θ_cal calibrated for uniform spending; terminal flush ≤ 5% and logged; G7 |
| Train–deployment shift for S-pred (probe covariates offline, online covariates and closed-loop intervals in Stage B) | Separate Stage B deployment model on online covariates (§8); in-loop calibration logged; task-selection check (§9) |
| Under-tuned baseline produces a spurious advantage | Equal tuning budget; locked hyperparameters; saturation gate G3b |
| A null result produced by an insensitive pipeline | Positive control G4b |
| Optimizer specificity | SGD arm (exploratory) |
| Scale | Stage C; restrained claims |

## 17. Deliverables

- Code (MIT), data and reports (CC BY 4.0), frozen configurations with SHA-256, a run inventory, automated audit checks, and scripts that regenerate every reported table.
- A Zenodo preregistration (with DOI), deposited after Stage 0 and before any Stage A or B training, validation, or test run. It states explicitly that the study is a change of the plan announced in the Perspective (versions 1.0–1.2) and contains the frozen protocol, the Stage 0 report (§12a), the SHA-256 hashes of the locked values (D\*, m_ch, δ, σ̂_up, sample sizes per family) and the test-run seed lists, or a stopping report if Stage 0 halts the study.
- A preprint with *References* links to the Perspective and the closed study, and *Is supplemented by* to the code archive.

## 18. References

- Biderman, S., Schoelkopf, H., Anthony, Q., et al. (2023). Pythia: A suite for analyzing large language models across training and scaling. arXiv:2304.01373.
- Elazar, Y., Ravfogel, S., Jacovi, A., & Goldberg, Y. (2021). Amnesic probing: Behavioral explanation with amnesic counterfactuals. *Transactions of the Association for Computational Linguistics, 9*, 160–175. https://doi.org/10.1162/tacl_a_00359
- Feng, Y., Wang, H., Li, J., Chu, X., Kang, Z., Liu, Y., Wang, Y., Yu, P. S., & Wu, X.-M. (2026). FOREVER: Forgetting curve-inspired memory replay for language model continual learning. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 24945–24965. https://doi.org/10.18653/v1/2026.acl-long.1144 (arXiv:2601.03938)
- Hu, E. J., Shen, Y., Wallis, P., et al. (2022). LoRA: Low-rank adaptation of large language models. arXiv:2106.09685.
- Ionici, I. D. (2026). *A Time of Their Own: Agent-Held Temporal Evidence for Persistent AI Agents* (Version 1.3). Zenodo. https://doi.org/10.5281/zenodo.23847648
- Ionici, I. D. (2026). *Does Explicit Episode–Trace Binding Help? An Exploratory Study with Information-Matched, Competence-Audited Controls* (Version 1.3). Zenodo. https://doi.org/10.5281/zenodo.23847602
- Ionici, I. D. (2026). *Episode–Trace Binding Pilot: Code, Frozen Configurations, and Per-Run Results* (Version 1.3) [Software]. Zenodo. https://doi.org/10.5281/zenodo.23847723
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
- Zheng, J., Cai, X., Qiu, S., & Ma, Q. (2025). Spurious forgetting in continual learning of language models. arXiv:2501.13453.

*All references were checked against arXiv, Crossref or the publisher; those added in v0.2 and v0.3 on 3 November 2026.*

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

**Closed.** The truncated part of the review of v0.1 was not continued; v0.2 was reviewed in full instead (§20).

**Update of 1 November 2026 (no change of design).** The Perspective (v1.3, 10.5281/zenodo.23847648), the study (v1.3, 10.5281/zenodo.23847602), and the code archive (v1.3, 10.5281/zenodo.23847723) were revised after an automated review by the CMU Paper Reviewer. Citations and the closure rule in §0 now follow v1.3: non-inferiority within a prespecified margin and no worse declared cost, with mixed trade-offs reported as unresolved.


## 20. Revision log v0.2 → v0.3

Sources: **R2** = Google Deep Review (Argon, Medium) of v0.2, 3 November 2026, each point checked against the text before adoption; **O** = the author's own check, including four points of the v0.1 review that v0.2 neither adopted nor rejected; **M** = Mistral Large 4 review of v0.3 (API, reasoning effort "low"), 4 November 2026, each point checked against the text (its check of this log found every accepted change implemented).

**Accepted**

| Change | Sections | Source |
|---|---|---|
| H1 confirmatory on F2 and F3 only; F1, F5 and F6 reported alone with prespecified checks; total test runs as a sum of family allocations; σ̂_up on F2–F3; bootstrap stratified by family | §4.4, §10.2, §12 | R2 |
| Pacing rule corrected (it lowered the threshold when spending ran ahead, a runaway loop); ε fixed; θ_cal calibrated for uniform spending; terminal flush bounded and logged; decisions on the 64-step grid; S-pred triggered by the increase in predicted forgetting since the last rehearsal | §9, §11 | R2 |
| c_e and Disp enter as {raw increment, rate}, as the competitors do; +1 on all four terms of C1; matched ridge basis; constraints per column; unconstrained sensitivity fit | §2, §8 | R2 |
| Separate Stage B deployment model fitted on the online covariates; in-loop calibration; task-selection check (≥ 10% non-least-recently-rehearsed choices) | §8, §9, §15, §16 | R2 |
| G4: model refitted; blocks permuted across the runs of a family; checked at Stage 0 and Stage A | §11 | R2 |
| Stage B placebo made causal (the live twin's realised blocks, permuted and fed online; residual for S-pred); G8 as the live-versus-placebo contrast | §9, §11 | R2 |
| Interpretation table rebuilt: mutually exclusive rows on H1; rows for H1 inconclusive, G3b, G4, G6 and G8 failures, divergent hyperparameter outcomes, H2 refuted, and the task-selection check | §15 | R2 |
| Stage 0: out-of-fold 4-fold cross-fitting on the calibration runs; G4, stationarity of R, m_ch, G5 and G2b added; cost limit of 25 min per run under eight concurrent workers; sample-size criterion aligned with the 200-run cap; Stage 0 report | §12a, §17 | R2 |
| Step quantum of 64 steps, so that 256-item epochs at batch sizes 16, 32 and 64 end exactly at segment ends: childhood 3,072 steps, evaluation grid 256, L_reh = 64, minimum interval 64, m_ch ∈ {1, 4, 8, 16, 32, 64} (default 8), placebo blocks of 256 steps | §0.7, §4.1, §4.3, §5.1, §6, §9, §11 | R2 (quantum: O) |
| Maximum context 8 and no weight decay on biases and LayerNorm parameters: unused positional embeddings would otherwise decay deterministically and inject a Σ η signal into D1 and ‖θ‖ | §3, §16 | R2 |
| Pre-decay update for D1_rel, D2, C5c and C6; ℓ defined (weight and embedding matrices); D2 with a fixed lag of 256 steps instead of segment starts; C5e (Σ ‖m̂‖) and C5f (weight-decay path) added; logged quantities completed | §3, §5.1, §7 | R2 |
| Segment boundaries defined by agent-observable events | §4.3, §7 | R2 |
| C6 window W_eff = min(16, ⌊ΔN/4⌋), zeros when ΔN = 0, population SD, pre- and post-decay; inclusion rule for idle intervals; idle intervals in multiples of 64 ticks, evaluated at their end and every 256 ticks | §4.3, §4.5, §6, §7 | R2 |
| Vocabulary: two-token keys; token-disjoint key vocabularies V_target, V_ref, V_distractor; task tokens allocated, including distractor tokens; F6 batch sizes as in F2; fixed training set of 256 inputs per rule task; \|R\| = \|B_beh\| = 256 (128 fact, 128 rule); overlap over input pairs; log number of distinct target values as a covariate | §4.1, §4.4, §7 | R2 |
| Chunked distances written out; D4 exploratory, after the final LayerNorm, standard CKA; square root restored in the same-step identity | §5.1 | R2 |
| Displacement formulas written out; metric-free Disp^{D1} alongside if D\* = D2; snapshots on test runs only for D\*; C8b and C9 on 30 test runs; C8b + C9 as a joint reference | §5.2, §7, §14 | R2 |
| R split into R_maint and R_eval if maintenance is needed; accumulated unsigned canary change C10b in B_strong | §5.1, §7 | R2 |
| G1 on the episode-weighted r_AB; SESOI from F2–F3 calibration runs, out of fold | §7, §10.1, §11 | R2 |
| G4b: per-run noise scaling, +1 constraint on Z, tolerance [1.25δ, 2.5δ] | §11 | R2 |
| Divergence rule between locked and re-tuned ΔR² | §8, §15 | R2 |
| H2 as a non-inferiority test (supported, refuted, inconclusive); its sample size with σ̂_up(Z) and a scaled margin δ_H2 | §10.2, §12 | R2 |
| Search space stated; cross-validation grouped by run; 250 training-run bootstrap replicates for both model families (the v0.2 restriction to ridge is withdrawn: the cost is a few CPU-minutes) | §8, §10.1 | R2 |
| G2 at Stage 0 and Stage A; G2b on the two-sided 95% interval on F2 and F3; G5 as a one-sided lower bound > 0 with both models tuned; G6 wording; G7 terminal flush; G9 pairing (30 states × 2 seeds) and its denominator | §10.3, §11 | R2 |
| Compute estimate recounted: ≈ 315 Stage A runs, ≈ 590 Stage B runs, 12–15 min per run, batched probes | §14 | R2 |
| Stage C adaptation document: decision unit, resampling unit, LoRA distance algebra, top-K D3 with a tail bucket, loss-based inclusion, overlap histogram; task identity and spurious forgetting (Zheng et al. 2025, verified on arXiv) | §13, §18 | R2, O |
| Optimizer moments: initialisation, persistence, bias correction; SGD scaling of D2 | §3, §5.1 | R2 |
| Storage wording; weak ordering in the identification note; ρ̄ with max(ΔN, 1); conditional ranking inside a learned predictor | §0.7, §1, §2 | R2 |
| H1 reported by task type and by tercile of ΔN (descriptive) | §6 | O (v0.1 review) |
| Calibration diagnostic: optimizer moments reset at segment boundaries in a forked copy | §5.1 | O (v0.1 review) |
| References: code archive v1.3; five references of v0.2 verified on arXiv; Zheng et al. 2025 added; placeholder note removed | §18 | R2, O |
| Bootstrap mechanics: each draw pairs the resampled test runs with one training-run replicate; jackknife acceleration | §10.1 | M |
| The pair {Δc_e, ρ̄} adds one degree of freedom, stated | §8 | M |
| G6 training-run accounting: 60 training runs in total | §12 | M |
| Stop rule if n_H1 alone exceeds the cap; Stage B size n_B = max(40, n_H4) | §12 | M |
| TOST power wording: type II error split between the two sides (z_0.90 for power 0.80) | §12 | M (a misreading showed that the wording was unclear) |

**Rejected or modified**

| Suggestion | Decision |
|---|---|
| Further norm- and preconditioner-scaled accumulators in the confirmatory baseline (R2) | Modified: reported as the sensitivity baseline B_strong⁺. The confirmatory baseline already holds C5d, C5e, C5f, state norms and the normalisation of D1_rel; ratios of the candidate's own ingredients would make G2 fail by construction |
| F5 replication as "lower bound > 0 and point estimate ≥ δ" (R2) | Modified: lower bound > 0 only. Requiring the point estimate to reach δ halves the power when the true effect is δ |
| Step quantum of 48 steps, or tasks of 200 items with batch sizes {20, 40, 100} (R2) | Modified: a quantum of 64 steps keeps 256 items and the batch sizes |
| Lower bound of G2b raised to 0.05 (R2) | Not adopted: the H2 margin is scaled instead (δ_H2 = max(0.01, 0.20 · ΔR̄²_cal(Disp))) |
| D2 anchored at the curvature at the end of childhood (R2, alternative) | Not adopted: a fixed lag of 256 steps keeps the curvature current |
| Publication venues added to the arXiv references (R2) | Deferred: each venue is added only after it is checked at the publisher |
| G4b noise formula "does not give 2δ" (M) | Rejected: with Z = e + ξ, the expected within-run ΔR² is (1 − R²)·s²/(s² + σ²), which equals 2δ for the stated σ² (checked numerically: R² = 0.5, δ = 0.05 give ΔR² = 0.10). The review assumed that adding Z removes σ² from the residual linearly |
| n_TOST "uses power 0.90" (M) | Rejected: for TOST at a true difference of 0 the type II error is split between the two sides, so z_0.90 gives power 0.80; the wording was clarified |
| Ceiling should be r̄_AB² (M) | Rejected: for parallel halves, the largest fraction of the variance of F_A that any predictor of the true score can explain is the reliability r_AB itself; r²_AB would understate the ceiling |


## 21. Revision log v0.3 → v0.4

Sources: **S0** = Stage 0 measurements, 4 November 2026: technical runs tech1 (F1–F6, learning rate 1 × 10⁻³, with rule tasks), tech2 (F1–F3, 3 × 10⁻⁴, with rule tasks), tech3 (F2 and F3, 2 × 10⁻⁴ and 3 × 10⁻⁴, without rule tasks), and short calibration probes; tables in the Stage 0 working notes, to be reported in the Stage 0 report. **O** = the author's decision on that evidence. No incremental value of c_e over any predictor set was computed on technical runs; the only c_e quantities read were the per-quartile rates required by the v0.3 stationarity check and the coefficient of variation of the D1 rate in the run summaries.

**Accepted**

| Change | Sections | Source |
|---|---|---|
| Rule tasks withdrawn: held-out accuracy 0.02–0.30 with overfitting; 0–9 of 40–74 rule episodes valid per run. Fact tasks only; R and B_beh from 8 fact reference tasks; task-type and log-number-of-values covariates removed (constant); F5 differs by π_overlap, idle intervals and the F2–F3 generator mixture; declared scope: in-sample retention, no generalisation | §1, §4.1, §4.2, §4.4, §6, §7, §13, §16 | S0, O |
| Base learning rate η₀ = 3 × 10⁻⁴. At 1 × 10⁻³ the childhood gate failed (0.44–0.84). Without rule tasks, 2 × 10⁻⁴ and 3 × 10⁻⁴ both pass (0.982–0.994), a new fact task reaches probe accuracy 1.0 within 128 steps at batch 16 and 64, and the forgetting curves of the two rates coincide (same seed); a rule written before the tech3 runs chose the rate with more unsaturated triplets and, at a difference below 10%, 3 × 10⁻⁴ | §3, §0.7 | S0, O |
| T1 cap ΔN < 1,280, set by a rule written before the tech3 runs; uncapped statistic as sensitivity; strata by tercile of ΔN below the cap | §0.7, §6, §16 | S0, O |
| R declared a battery of forgotten inputs; stationarity check and the R_maint / R_eval remedy withdrawn; quartile rates of D3 and D1_rel reported | §4.1, §5.1, §12, §12a, §16 | S0, O |
| D2 with a blocked lag of 256–319 steps (implementation; exact lag needs ≈ 1 GB per worker) | §5.1 | S0 |
| Examples of 5 tokens, no padding | §3 | S0 |
| Workers: as many as maximise throughput, not eight | §3, §14 | S0 |
| Cost criterion in wall-clock hours and throughput on the declared machine; resumption at the run level; core-hours reported only | §12a, §14 | S0, O |
| Compute estimate replaced by full-run measurements; machine declared, including its memory configuration | §14 | S0 |
| G7: hash of the resolved configuration (overrides included); rerun check after a change of hardware | §11, §16 | O (the v0.3 configuration hash covered the file only and did not distinguish runs with overridden values) |
| Stage 0 report lists η₀, ΔN_max and the measured cost | §12a | O |

**Criteria of v0.3 that failed at Stage 0** (reported, not hidden)

| v0.3 criterion or assumption | Measured | Consequence in v0.4 |
|---|---|---|
| Childhood gate ≥ 0.95 at the provisional learning rate 1 × 10⁻³ | 0.44–0.84 | η₀ = 3 × 10⁻⁴ |
| Rule tasks measure held-out generalisation | 0.02–0.30 held-out accuracy | Rule tasks withdrawn |
| Stationarity of R within ±20% | D3 rate, fourth / first quartile: 0.58–0.70 at 3 × 10⁻⁴, 0.74–0.96 at 1 × 10⁻³ (F1–F3) | Check withdrawn as uninformative; R redefined |
| ≤ 25 min per run with eight concurrent workers | 44–48 min with six workers; 95–101 ms per step with eight | Criterion rewritten (wall-clock hours, throughput) |
| ≤ 150 CPU-hours for Stage A | ≈ 130 core-hours with four workers, ≈ 160 with three, ≈ 240 with six, model fitting not included | Not a measure of cost under a memory-bandwidth limit; reported only |
| Runs resumable from checkpoints | Not implemented | Resumption at the run level: runs are bit-identical, so an interrupted run is redone from its start and completed runs are skipped |
| D2 lag of exactly 256 steps | Not implemented (memory) | Blocked lag of 256–319 steps |
| ≈ 12–15 min per run, 9–11 wall-clock hours for Stage A | 24–25 min per run with four workers; ≈ 33 h for Stage A at the best measured throughput | §14 replaced |

**Rejected or not adopted**

| Alternative | Decision |
|---|---|
| Unary rule tasks y = (a·d₁ + b) mod m (generalise perfectly within 128 steps) | Not adopted: generalisation over an irrelevant digit only, too weak to stand for a generalisation stratum |
| Rule tasks of intermediate difficulty, or rule probes turned into trained items | Not adopted: the first is untested, the second would duplicate fact tasks |
| T1-acc as a co-primary target | Rejected: a second confirmatory test, and T1-acc is at its floor in the saturated intervals (SD 0.02–0.04) |
| More frequent rehearsal, so that fewer intervals saturate | Rejected: it changes the world to suit the measurement and only moves the threshold |
| Stratified reporting only, without a cap | Rejected: the saturated intervals would stay in the confirmatory statistic |
| Excluding triplets in which task k is already forgotten at t₁ | Rejected: selection on the outcome |
| Per-item cross-entropy clipped at ln 64 | Not adopted: it changes the definition of T1, and per-item losses are not stored |
| Maintaining R by rehearsal in every family | Rejected: it adds a training component that interferes with the target tasks, and a cheap schedule cannot keep fact items |
