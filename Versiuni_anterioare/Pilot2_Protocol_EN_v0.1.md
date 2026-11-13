# Pilot 2 — Technical Protocol (Draft for External Review)

**Working title:** *Does an Agent's Own Change Keep Time? Testing an Experiential Index of Adaptation Against Clocks, Counts, and Logged Update Summaries*

**Author:** Ioan Daniel Ionici (Independent Researcher, Oradea, Romania; ORCID 0009-0009-8183-3656)
**Status:** draft protocol v0.1, 27 October 2026. Not frozen. To be frozen, hashed (SHA-256), and deposited on Zenodo before any main run.
**Builds on:** Ionici (2026), *A Time of Their Own* v1.1, §4 and Level 2 of Table 2, https://doi.org/10.5281/zenodo.23687300; method of Ionici (2026), *Does Explicit Episode–Trace Binding Help?* v1.2, https://doi.org/10.5281/zenodo.23666336; code base https://doi.org/10.5281/zenodo.23667154.

---

## 0. Position within the research programme (context for the reviewer)

This protocol is the empirical continuation of two published works by the same author. Neither is under review here. They are summarised so that every design decision below can be traced to its source.

### 0.1 The Perspective: what is to be tested

*A Time of Their Own* (v1.1) argues the following:
- **The problem.** A persistent artificial agent whose complete state can be saved and restored holds no evidence about elapsed time or about its own change that it could not have been given, reset, or forged together with that state.
- **The classification.** It classifies the temporal evidence available to an agent (order, duration, sequential computation, continuity, and its own change) by who can write, reset, forge, or copy it, and by whether the agent's self-model can read it.
- **Two roles that must be kept apart:**
  1. A **continuity anchor**: a non-restorable time reference c_a and a state-bound operation counter N, read through a trusted path. It detects and distinguishes suspension and restoration (Level 4 of its programme).
  2. A **dual clock**: an **experiential index** c_e(t) = Σ_{τ<t} D(S(τ), S(τ+1)), accumulated change of the agent's persistent state S, read against c_a. It serves the agent's model of its own adaptation (Level 2). The index is non-decreasing, costs one stored number, and is distinct from the net displacement D(S(t₀), S(t₁)). The choice of D is declared an open problem.
- **Admissibility of D.** A candidate D is admissible only if it:
  - (a) beats decoders restricted to within-episode (local) update statistics;
  - (b) survives the reset criterion and randomisation of episode order, where it is meant to reflect history;
  - (c) predicts a later functional consequence better than event counts and logged update summaries;
  - (d) is used by the agent rather than merely decodable from it.
- **Test programme.** Six levels (time reference, experiential index, history, discontinuity, closed-loop use, temporal self), each paired with the conventional competitor that can close it. A level is **closed** if its competitor matches it at equal declared cost. The primary metric of Level 2 is **predictive validity per unit of storage**.
- **Stance on outcomes.** Equivalence with the competitor is a legitimate negative result, and *functional separation* (the platform suffices, and agent-held evidence is unnecessary) is a possible outcome of the programme. The Perspective offered its tests to others and stated that its author did not plan to pursue them. This study is a declared change of that plan.

**This protocol tests Level 2 only:** whether c_e, under some admissible D, is worth holding.

### 0.2 The closed study: how it is to be tested

*Does Explicit Episode–Trace Binding Help?* (v1.2, closed) asked whether binding an episode record to a summary of the internal change it produced (arm D) helps a model attribute the episode's source (own, imported, or inferred), compared with an information-matched control that receives the same streams without the binding (arm F). The model was a small Transformer self-model reading the traces of a plastic agent. Over five exploratory iterations:
- **The apparent advantage was a control failure.** Generic controls failed to use the trace, which produced a large but uninformative advantage for D (+0.38 Brier skill score). When the control was made competent (87% of a decoding ceiling), D − F was +0.002 BSS, with descriptive equivalence under a ±0.05 BSS margin.
- **The signal was local, not historical.** Decoder diagnostics showed that the source was carried by **local update statistics**, and that resetting the state before each episode did not reduce decodability. The benchmark therefore did not test attribution from path-dependent history.
- **A shortcut caused the apparent reversal.** With 32 episodes per window, an apparent reversal between objectives was traced to a shortcut in how one objective was applied, and removing it repaired the reversal.

**What carries over is the method,** not a result: an information-matched control, a competence audit of the control, a decoding ceiling, a reset criterion, equivalence tests (TOST) with a prespecified margin, the distinction between onset (whether learning starts) and skill (performance once learned), reliance versus necessity, frozen and hashed configurations, and a per-run inventory.

**What carries over as a warning:** local update statistics can impersonate accumulated history. This is why competitor C6 is mandatory here.

### 0.3 Why Level 2, and why not the continuity anchor

An earlier internal draft of Pilot 2 tested the continuity anchor (Level 4) in simulation. It was abandoned. With a simulated anchor that is deterministic by construction, classifying suspension against restoration reduces to comparing two counters. A raw anchor can then beat an information-matched adjudicated flag only where the flag is absent, which is an argument about availability, not an empirical finding.

Level 2 is different: whether c_e predicts the agent's own forgetting depends on the actual learning dynamics of the network, so the outcome is not fixed by the design. It is also the element of the Perspective that is furthest from existing work: forgetting prediction exists (§7), but not as a single agent-held running index evaluated against competence-audited conventional competitors.

### 0.4 Traceability of design decisions

| Design decision | Source |
|---|---|
| Definition of c_e; distinction from displacement; D as open problem | Perspective §4 |
| Q1–Q4 and the mapping to criteria (a)–(d) | Perspective §4 (admissibility) |
| Baseline B_cheap = union of all cheap competitors | Perspective §5 (a level closes if the competitor matches); closed study (control competence) |
| Competitor C6 (local update statistics) | Closed study: main diagnostic finding |
| Primary metric: validity per unit of storage (H2) | Perspective §5, Level 2 |
| Three-way outcomes (supported, equivalent, inconclusive) and TOST | Perspective (equivalence as a legitimate result); closed study (equivalence margins) |
| Ceiling G1, competence G3, onset versus skill G6, reliance G8 | Closed study, method; Perspective §6 |
| Frozen configurations, hashes, inventory, bit-identical reruns G7 | Closed study and its code archive |
| Competitors C1, C8, C8b, C9 | External literature on forgetting (§7) |
| Stage C on pretrained language models | Perspective (claims concern persistent agents, not toy worlds) |

### 0.5 What the reviewer is asked to evaluate

Only this protocol: whether its design can deliver an interpretable answer to Q1–Q4 at the stated scale, and whether it transfers unchanged to Stage C. The claims of the Perspective and the results of the closed study are published and are not under review.

### 0.6 Glossary

| Term | Meaning |
|---|---|
| S, θ | Persistent state of the agent; its parameters |
| c_a | Elapsed time in ticks (§4.5) |
| N | Number of committed optimizer steps |
| c_e^D | Experiential index: accumulated D-change of S |
| ρ | Rate dc_e/dN; the only source of information in c_e beyond counts (§2) |
| Disp^D | Net displacement D(S(t₀), S(t₁)) |
| √JS | Jensen–Shannon distance (a metric) |
| B_cheap | Confirmatory baseline: covariates plus all cheap competitors C0–C7 |
| SESOI | Smallest effect size of interest |
| TOST | Two one-sided tests (equivalence) |
| MET | Minimal-effect test: lower confidence bound above the SESOI |
| BSS | Brier skill score (used in the closed study) |
| Gate | A prespecified validity check; failing it changes how a result may be reported |

---

## 1. Research question

Let a Transformer learn continually from a non-stationary stream of tasks. Let

  c_e(t) = Σ_{τ<t} D(S(τ), S(τ+1))

be its *experiential index*: the accumulated change of its persistent state S under a distance D. This is a non-decreasing scalar held by the agent. It costs one stored number.

**Q1 (predictive validity).** Does Δc_e over an interval (t₀, t₁] predict the agent's forgetting of a task last trained at t₀ better than the following?
- elapsed time;
- step, token, and event counts;
- cumulative learning rate and loss;
- logged gradient summaries;
- local (within-window) update statistics.

**Q2 (storage efficiency).** How much of the predictive value of the full net displacement D(S(t₀), S(t₁)), which requires storing S(t₀), does the scalar c_e retain?

**Q3 (path dependence).** Do order-induced differences in forgetting, under a fixed multiset of experiences, track order-induced differences in Δc_e?

**Q4 (use).** Does a rehearsal scheduler that uses c_e outperform budget-matched schedulers that use the competitors, and does its advantage depend on the actual c_e stream rather than on a yoked one?

The admissibility criteria for D stated in *A Time of Their Own* §4 map onto these questions:

| Criterion | Question |
|---|---|
| (a) beats decoders restricted to local update statistics | Q1, competitor C6 |
| (b) order and reset sensitivity where history matters | Q3 |
| (c) predicts a functional consequence better than counts and logged summaries | Q1 |
| (d) used by the agent rather than merely decodable | Q4, gate G8 |

The reset criterion (b) is **not applicable** here. Δc_e is used as an interval index, not as a summary of the whole life history, so only order sensitivity is tested. This scope restriction is declared in advance.

## 2. Identification note (read first)

Within a run, at a fixed evaluation time t₁, the ranking of tasks by Δc_e = c_e(t₁) − c_e(t₀,k) is identical to their ranking by t₀,k, the time since the last exposure. The reason is that c_e is non-decreasing. A global scalar index therefore carries **no task-specific information at a fixed time**.

All information that c_e carries beyond counts lies in the **temporal variation of its rate**, ρ(t) = dc_e/dN: some intervals of equal length contain more change than others. Two consequences follow:
1. Q1 is identifiable only to the extent that ρ varies across intervals. Gate G2 checks this.
2. A scheduler that *selects which task to rehearse* by ranking tasks on Δc_e since their last exposure is equivalent to least-recently-rehearsed. Q4 must therefore test *when*, and *how much*, to rehearse (allocation over time), or use c_e together with task covariates inside a learned predictor (§9).

## 3. Agent

| Component | Specification |
|---|---|
| Architecture | Decoder-only Transformer, 4 layers, d_model = 128, 4 heads, d_ff = 512, pre-LN, GELU, learned positional embeddings, context 64, vocabulary ≈ 512 tokens, ≈ 0.8 M parameters |
| Optimizer (primary) | AdamW, β = (0.9, 0.999), ε = 1e-8, weight decay 0.01, gradient clipping at norm 1.0 |
| Optimizer (robustness arm) | SGD with momentum 0.9 (under SGD, ‖Δθ‖ and ‖g‖ are near-collinear; under Adam they are not) |
| Persistent state S | Parameters θ and optimizer moments (m, v); D is computed on θ, and v is used as a diagonal Fisher proxy |
| Precision, device | float32 on CPU; deterministic algorithms enabled; fixed seeds for data, initialisation, and dropout (dropout = 0 in the primary arm) |
| Software | Python 3.14, PyTorch 2.13, NumPy 2.5, scikit-learn (version pinned at freeze); `environment.txt` recorded |

## 4. World and streams

### 4.1 Task types

- **Fact tasks.** Task k is a set of 128 key→value pairs. The input is `[TASK_k] [KEY] →`, and the target is a single `[VALUE]` token. Keys are drawn from a shared pool of P keys, and the overlap between tasks is controlled by a pool-sharing parameter π_overlap. Values are drawn uniformly from V value tokens.
- **Rule tasks.** Task k is an algorithmic map, for example y = (a_k·x + b_k) mod m_k on tokenised integers. Inputs are drawn fresh, and probe inputs are held out from training.
- **Reference tasks.** A fixed set of fact and rule tasks, trained only during an initial *childhood* phase. They are never targets. They supply the reference battery R (§5).

### 4.2 Probes

Each target task has a probe set: its 128 facts (fact tasks) or 256 held-out inputs (rule tasks). The probe set is split **once, at task creation**, into disjoint halves A (used for the target) and B (used for reliability, and by Stage B). No probe item belongs to R or to the behavioural battery B_beh.

### 4.3 Run structure

| Phase | Steps (indicative) | Content |
|---|---|---|
| Childhood | 3,000 | Reference tasks to criterion |
| Life | ≈ 20,000 | ≈ 40 target tasks, presented according to the stream family; rehearsal segments, re-exposure segments, and idle intervals according to the family |
| Evaluation | — | Probes of every learned task are evaluated at the end of every exposure segment and on a grid every 200 steps |

### 4.4 Stream families

| Family | Generator | Intended decoupling |
|---|---|---|
| **F1, natural** | New task every fixed number of steps, fixed segment length, round-robin rehearsal, constant LR, fixed batch | None (positive control: counts are expected to suffice) |
| **F2, variable novelty** | New tasks interleaved with re-exposure to already-mastered data in random amounts; batch size ∈ {16, 32, 64} per segment | Steps and tokens decouple from change |
| **F3, LR schedule** | Cosine annealing with warm restarts at random times | Steps decouple from change; cumulative LR is a strong competitor |
| **F4, idle** | Random idle intervals with no updates; c_a advances, θ is frozen | Elapsed time decouples trivially (sanity, not a finding) |
| **F5, held-out** | Mixture of the F2–F4 generators with a different proportion of rule tasks and a different π_overlap | Never used for fitting or selection; test only |
| **O, order blocks** | Designed blocks (§10, H3): task k learned, then segments X (high key overlap with k) and Y (low overlap) in orders XY and YX, with the same seed and the same multiset | Path dependence |

Generator parameters for each family are frozen with the protocol.

### 4.5 Time

c_a counts *ticks*. Each optimizer step adds 1 tick; each idle interval adds its length in ticks; evaluations add 0 ticks. In F1–F3, c_a equals N, the number of optimizer steps. They differ only in F4 and F5.

## 5. Distances D and the index c_e

| D | Definition | Evaluated | Storage per t₀ |
|---|---|---|---|
| **D1** | ‖θ(τ+1) − θ(τ)‖₂ | Every step | 1 scalar |
| **D2** | ( Σ_i v_i (Δθ_i)² )^{1/2}, with v the Adam second moment at τ | Every step | 1 scalar |
| **D3** | Mean over x ∈ R of √JS( p_{S(τ)}(·\|x), p_{S(τ+k)}(·\|x) ), with \|R\| = 256 | Every k = 10 steps (chunked) | 1 scalar |
| **D4** (secondary) | 1 − linear CKA of final-layer representations on R, between S(τ) and S(τ+k) | Every k = 10 steps | 1 scalar |

- c_e^{D}(t) = Σ over steps (D1, D2) or over chunks (D3, D4) up to t.
- √JS is a metric, so by the triangle inequality the chunked sum is a lower bound on the per-step sum. The value of k is a frozen parameter, and a sensitivity arm uses k ∈ {1, 10, 50} on calibration runs.
- **Net displacement:** Disp^{D}(t₀, t₁) = D(S(t₀), S(t₁)). It requires storing S(t₀), that is ≈ 0.8 M numbers per t₀.
- **D\*** is the single D used in the confirmatory tests H1 and H4. It is chosen among D1–D3 on calibration runs as the one with the largest incremental validity over the baseline B_cheap (§7), and is frozen before any test run.

## 6. Targets

**T1 (primary): forgetting.** For each target task k and each exposure segment of k ending at step s₀, let t₀ be the evaluation immediately after s₀. For every evaluation time t₁ > t₀ before the next exposure of k:

  F_k(t₀, t₁) = L̄_A,k(t₁) − L̄_A,k(t₀),

where L̄_A,k is the mean cross-entropy on probe half A of task k.
- **Inclusion:** a pair is included only if the probe-A accuracy of task k at t₀ is ≥ 0.90 (task learned). Excluded pairs are counted and reported.
- **Unit of observation:** the triplet (k, t₀, t₁). **Unit of inference:** the run.

**T2 (secondary): behavioural drift.** The √JS distance between the outputs of S(t₀) and S(t₁) on a battery B_beh disjoint from R and from all probes. It is reported descriptively. T2 is structurally favourable to Disp^{D3}, so it is not used for confirmatory claims.

**T3 (Stage B): retention.** The time-averaged probe-B accuracy over all learned tasks during the life phase, at a fixed rehearsal budget.

## 7. Predictor sets and competitors

**Covariates X_cov, given to every model:**
- task type;
- π_overlap of task k with the pool;
- task age at t₀;
- number of prior exposures of k;
- L̄_A,k(t₀);
- probe-A accuracy at t₀.

**Cheap competitors (≤ 32 stored numbers per t₀):**

| Code | Predictor over (t₀, t₁] | Source |
|---|---|---|
| C0 | Δc_a, elapsed ticks | wall clock |
| C1 | ΔN, optimizer steps, with transform log(ΔN + b) | the shifted power law of Kalajdzievski (2024), arXiv:2401.05605 |
| C2 | Δ tokens | data volume |
| C3 | Σ η_t | cumulative learning rate |
| C4 | Σ L_t | cumulative training loss |
| C5 | Σ ‖g_t‖₂ | logged gradient norm |
| C6 | mean and SD of ‖Δθ‖ over the last W = 200 steps before t₁ and the first W steps after t₀ | local update statistics (Pilot 1 shortcut; criterion (a)) |
| C7 | number of new tasks, re-exposure segments, and rehearsals in the interval | semantic event counts |

**B_cheap** = X_cov ∪ {C0, …, C7}. This is the confirmatory baseline: the union of all cheap competitors, not a single selected one.

**Reference predictors** (not agent-available, or of high storage; used to bound, not to compete):

| Code | Predictor | Storage |
|---|---|---|
| C8 | Σ over intervening tasks j of key overlap(k, j) × steps on j | world metadata (Lee, Goldt and Saxe 2021, arXiv:2107.04384) |
| C8b | Disp^{D2}(t₀, t₁), Fisher-weighted displacement (EWC: Kirkpatrick et al. 2017, doi:10.1073/pnas.1611835114) | ≈ 0.8 M per t₀ |
| C9 | First-order response: ⟨∇_θ L_k(S(t₀)), θ(t₁) − θ(t₀)⟩ (cf. Su and Zhang 2026, arXiv:2609.32818; Jin and Ren 2024, arXiv:2402.01865) | ≈ 0.8 M per task |
| Ceiling | Split-half reliability of T1 (A vs B), corrected with Spearman–Brown | — |

## 8. Prediction models and competence audit

- **Primary model family:** gradient-boosted regression trees (scikit-learn `HistGradientBoostingRegressor`), with monotone-increasing constraints on all interval predictors (C0–C5, C7, Δc_e, Disp).
- **Secondary model family:** ridge regression on predefined transforms (log1p of every interval predictor, plus interactions with task type), with λ chosen by cross-validation.
- **Equal tuning budget:** every predictor set receives the same random search, 50 configurations, on validation runs, with the same seeds for the search.
- **Fitting:** models are fitted on pooled pairs from the training runs and evaluated on test runs. No test-run information is used in fitting, selection, or transformation.
- **Skill per test run r:** R²_r = 1 − SSE_r / SST_r, with SST_r computed around the mean of run r. This is the within-run variance explained. Spearman ρ_r and MAE_r are reported alongside.

## 9. Stage B: use by the agent

- **Budget.** The rehearsal budget is fixed per run: a total of Q rehearsal steps over the life phase. Rehearsal segments last r = 50 steps.
- **Schedulers.** By the identification note (§2), schedulers differ in **when** they spend the budget (allocation over time), and in which task, only through a learned predictor that includes covariates.

| Scheduler | Rule |
|---|---|
| S-uniform | Rehearsal every Q-th fraction of N; task chosen least recently rehearsed |
| S-c_e | Rehearsal triggered when Δc_e^{D\*} since the last rehearsal ≥ θ_e; task chosen least recently rehearsed; θ_e set so that the budget is spent |
| S-C3, S-C4, S-C7 | As S-c_e, with the trigger on cumulative LR, cumulative loss, or event counts |
| S-pred(B_cheap) | A learned forgetting predictor (Stage A model, B_cheap) scores every task; rehearse argmax when the predicted max ≥ threshold |
| S-pred(B_cheap + c_e) | Same, with Δc_e^{D\*} added (information-matched pair) |
| S-oracle | Rehearse the task with the largest true current forgetting (requires evaluating all probes; upper bound) |
| S-random | Random times and tasks, same budget |

- **Calibration:** all thresholds are calibrated on validation runs to spend exactly Q.
- **Reliance test (G8):** S-c_e and S-pred(+c_e) are rerun with the c_e stream replaced by that of a yoked run (same family, different seed).

## 10. Hypotheses (confirmatory)

**SESOI:**
- Stage A: δ = 0.05 absolute ΔR².
- Stage B: δ_B = 2 percentage points of T3 at equal budget.

For each hypothesis, the outcome is decided with the 95% bootstrap confidence interval (BCa, 10,000 resamples over test runs):
- **supported** if the lower bound is > δ (a minimal-effect test);
- **equivalent** if the 90% interval lies within (−δ, δ) (TOST);
- **inconclusive** otherwise.

| | Statement | Statistic |
|---|---|---|
| **H1** | Adding Δc_e^{D\*} to B_cheap increases held-out skill on T1 | Mean over test runs of R²_r(B_cheap + c_e) − R²_r(B_cheap); test runs from F1–F5; F5 also reported alone |
| **H2** | The scalar index retains at least 80% of the displacement's incremental value | Ratio [R²(B_cheap + c_e) − R²(B_cheap)] / [R²(B_cheap + Disp^{D\*}) − R²(B_cheap)], with a bootstrap CI; supported if the lower bound is ≥ 0.80 |
| **H3** | In order blocks, order-induced differences in forgetting track order-induced differences in Δc_e | Across matched pairs (same seed, task k, multiset; orders XY vs YX), Spearman between ΔF and Δ(Δc_e); supported if the lower bound is > 0.10 |
| **H4** | S-pred(B_cheap + c_e) exceeds S-pred(B_cheap) on T3, and S-c_e exceeds the best of S-C3, S-C4 and S-C7 | Paired differences per test run; both comparisons reported; Holm-adjusted |

- **Multiplicity:** Holm across H1–H4, with family-wise α = 0.05.
- **Exploratory, labelled as such:** D1–D4 comparisons beyond D\*; the SGD arm; T2; C8, C8b and C9 bounds; single-competitor comparisons.

## 11. Gates

| Gate | Check | Criterion | Consequence of failure |
|---|---|---|---|
| G1, ceiling | Spearman–Brown split-half reliability of T1 on calibration runs | ≥ 0.70 | Increase probe-set size before freeze; report all skills also as a fraction of the ceiling |
| G2, identifiability | Correlation of Δc_e^{D\*} with its best linear prediction from B_cheap on test pairs | R² < 0.90 | H1 is reported as *not identifiable*, never as equivalence |
| G3, competence | In F1, B_cheap beats X_cov alone | ΔR² ≥ 0.10 on validation | Redesign the target or the stream before freeze (checked on calibration) |
| G4, leakage and placebo | R ∩ probes = ∅ (asserted in code); incremental value of a yoked-run c_e over B_cheap | Placebo ΔR² 90% CI within ±0.01 | Stop; leakage or a design artefact |
| G5, local statistics | B_cheap contains C6; additionally, c_e versus C6 + X_cov alone is reported | — (reported) | — |
| G6, onset versus skill | H1 conclusion stable when the number of training runs is halved and doubled; Stage B learned predictors stable when their training budget is doubled | Same three-way outcome | Report as onset-dependent |
| G7, reproducibility | Bit-identical reruns of a random 5% of runs; config hashes verified before analysis | 100% | No analysis until fixed |
| G8, reliance | Yoked c_e stream in Stage B | Advantage falls to within ±δ_B/2 of the baseline | c_e is decodable but not used |
| G9, H3 identifiability | Order effect on F exceeds noise: split-half reliability of ΔF across matched pairs | ≥ 0.50 | H3 is reported as *not identifiable* |

## 12. Data splits and sample size

- **Calibration runs:** used only for G1, G3, the choice of D\*, the chunk size k, the variance of ΔR², and threshold design. They are discarded afterwards and never enter test statistics.
- **Training runs:** F1–F4. **Validation runs:** F1–F4, new seeds. **Test runs:** F1–F4, new seeds, plus all of F5 and the O blocks.
- **Sample size:** the SD σ of per-run ΔR² is estimated on calibration runs. The number of test runs n is the larger of two powers of 0.80 at α = 0.05: TOST at true ΔR² = 0, and the minimal-effect test at true ΔR² = 2δ.
- **Budget cap:** 200 test runs. If n exceeds the cap, the scope is reduced (fewer families, declared before freeze). The SESOI is not relaxed.

## 13. Stage C: scaling

- **Protocol:** identical, with only the configuration file changed.
- **Agent:** publicly available pretrained causal LMs (the Pythia family, from 70M on CPU as a feasibility check up to ≥ 1.4B on GPU).
- **Stream:** a fixed sequence of public text or instruction domains, frozen at Stage C freeze.
- **T1:** loss on held-out samples of earlier domains.
- **R:** a fixed generic-text battery.
- **Competitors:** C0–C7 computed identically.
- **Optimizer arms:** full fine-tuning and LoRA. Under LoRA, D is computed on the adapter parameters.

The Stage A conclusions are claimed to generalise only if Stage C reproduces the three-way outcome of H1.

## 14. Compute estimate (to be replaced by measured values in Stage 0)

| Item | Estimate |
|---|---|
| Training step (batch 32 × 64 tokens, CPU, 8 cores) | 10–20 ms |
| D3 every 10 steps | +30% |
| One run (≈ 23,000 steps + ≈ 120 evaluations) | 8–12 min |
| Stage A (≈ 150–200 test runs + training, validation and calibration runs) | 40–60 CPU-hours |
| Stage B | ≈ 20 CPU-hours |
| Stage C-mini (Pythia-70M, CPU) | hours per run; feasibility only |

## 15. Interpretation table (frozen with the protocol)

| Outcome | Interpretation |
|---|---|
| H1 supported, including on F5 alone | Accumulated own change predicts own forgetting beyond clocks, counts, and logged summaries: first empirical support for the experiential index (Level 2) |
| H1 equivalent | Counts and logged summaries suffice; Level 2 is closed for this regime |
| H1 supported on F2–F4 only, equivalent or inconclusive on F1 and F5 | The advantage is confined to designed decoupling; it is reported as a construction effect, not a general result |
| G2 fails | Not identifiable in this design |
| H2 supported | The scalar index captures most of what full displacement captures, at a fraction of the storage of order 10⁻⁶ |
| H2 not supported | Displacement carries information that the path index does not; the claim of a one-number index is weakened |
| H3 supported (G9 passed) | The index tracks path dependence invisible to order-invariant counts |
| H4 supported and G8 passed | The agent uses the index in a decision about itself |
| Stage C reproduces H1 | The result is not an artefact of the synthetic world |

## 16. Threats to validity and mitigations

| Threat | Mitigation |
|---|---|
| Designer degrees of freedom in the stream families | F1 natural; F5 held out; families frozen; Stage C on real data |
| Shared noise between predictor and target | R disjoint from probes; placebo G4; T2 not confirmatory |
| Local-statistics shortcut (Pilot 1) | C6 inside B_cheap; G5 |
| Dependence of pairs within a run | Run-level inference; within-run R² |
| Selection of D after seeing results | D\* chosen on calibration and frozen |
| Optimizer specificity | SGD arm (exploratory) |
| Scale | Stage C; restrained claims |

## 17. Deliverables

- Code (MIT), data and reports (CC BY 4.0), frozen configurations with SHA-256, a run inventory, automated audit checks, and scripts that regenerate every reported table.
- A Zenodo preregistration (with DOI) before main runs.
- A preprint with *References* links to the Perspective and the closed study, and *Is supplemented by* to the code archive.

## 18. References

- Ionici, I. D. (2026). *A Time of Their Own: Agent-Held Temporal Evidence for Persistent AI Agents* (Version 1.1). Zenodo. https://doi.org/10.5281/zenodo.23687300
- Ionici, I. D. (2026). *Does Explicit Episode–Trace Binding Help? An Exploratory Study with Information-Matched, Competence-Audited Controls* (Version 1.2). Zenodo. https://doi.org/10.5281/zenodo.23666336
- Ionici, I. D. (2026). *Episode–Trace Binding Pilot: Code, Frozen Configurations, and Per-Run Results* (Version 1.2) [Software]. Zenodo. https://doi.org/10.5281/zenodo.23667154
- Jin, X., & Ren, X. (2024). What will my model forget? Forecasting forgotten examples in language model refinement. arXiv:2402.01865.
- Kalajdzievski, D. (2024). Scaling laws for forgetting when fine-tuning large language models. arXiv:2401.05605.
- Kirkpatrick, J., Pascanu, R., Rabinowitz, N., et al. (2017). Overcoming catastrophic forgetting in neural networks. *Proceedings of the National Academy of Sciences, 114*(13), 3521–3526. https://doi.org/10.1073/pnas.1611835114
- Lakens, D., Scheel, A. M., & Isager, P. M. (2018). Equivalence testing for psychological research: A tutorial. *Advances in Methods and Practices in Psychological Science, 1*(2), 259–269. https://doi.org/10.1177/2515245918770963
- Lee, S., Goldt, S., & Saxe, A. (2021). Continual learning in the teacher-student setup: Impact of task similarity. In *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139, 6109–6119. arXiv:2107.04384.
- Mirzadeh, S. I., Farajtabar, M., Pascanu, R., & Ghasemzadeh, H. (2020). Understanding the role of training regimes in continual learning. arXiv:2006.06958.
- Roseboom, W., Fountas, Z., Nikiforou, K., Bhowmik, D., Shanahan, M., & Seth, A. K. (2019). Activity in perceptual classification networks as a basis for human subjective time perception. *Nature Communications, 10*, 267. https://doi.org/10.1038/s41467-018-08194-7
- Su, J., & Zhang, W. (2026). When can first-order models of fine-tuning bound forgetting? arXiv:2609.32818.
- Toneva, M., Sordoni, A., Tachet des Combes, R., Trischler, A., Bengio, Y., & Gordon, G. J. (2019). An empirical study of example forgetting during deep neural network learning. arXiv:1812.05159.

---

## Appendix — Questions for the external reviewer

Please address each question explicitly. Where you recommend a change, state the concrete replacement value or design.

1. **SESOI.** Is δ = 0.05 absolute ΔR² (within-run R²) a defensible smallest effect of interest for forgetting prediction? Would a relative criterion, a fraction of the explainable variance under the G1 ceiling, be better?
2. **Chunked D3.** Is computing √JS over chunks of k = 10 steps (a lower bound on the per-step path length) an acceptable approximation, or does it bias the comparison between D3 and the per-step D1 and D2? Is the sensitivity arm k ∈ {1, 10, 50} sufficient?
3. **Inference structure.** Pairs (k, t₀, t₁) are nested in tasks, which are nested in runs. Is run-level inference on within-run R² adequate, or is a hierarchical model required? Does the pairing of overlapping intervals for the same task inflate the effective sample size even within a run?
4. **Baseline strength.** Is B_cheap (the union of C0–C7 plus covariates, with monotone gradient boosting and an equal tuning budget) a sufficiently competent baseline? Which cheap, agent-available competitor is missing?
5. **Stream families.** Do F2–F4 favour c_e by construction beyond what F1 and F5 control for? Propose a family that would favour the competitors against c_e as an adversarial check.
6. **Identification.** Given §2 (no task-specific information at a fixed time), is H1 well posed, or should the target be restricted to variation across t₁ within a task?
7. **H2.** Is the 80% retention ratio a meaningful threshold, and is the ratio estimator stable when the denominator is small? Propose an alternative if not.
8. **H3.** Is the XY versus YX order-block design identifiable, given that a global index may not encode similarity-specific interference? Is a lower bound of 0.10 on the Spearman correlation reasonable?
9. **Stage B.** Given that a ranking over tasks by a global monotone index reduces to least-recently-rehearsed, is the allocation-over-time design (S-c_e versus S-C3, S-C4, S-C7) a valid test of use? Is the information-matched pair S-pred(B_cheap) versus S-pred(B_cheap + c_e) the right test of criterion (d)?
10. **Placebo.** Is a yoked-run c_e (same family, different seed) an adequate placebo, or can it carry family-level information that B_cheap does not already contain?
11. **Power.** Is the sample-size rule (§12) correct for a minimal-effect test combined with TOST on bootstrap intervals?
12. **Scaling.** Which elements of the protocol are least likely to transfer to Stage C (pretrained LMs, LoRA), and what should be changed now to make the transfer clean?
13. **Anything else.** Identify any flaw that would make a positive H1 uninterpretable.
