# Recenzia Mistral Large 4 pe protocolul Pilot 2 v0.3

Model: `mistral-large-4` prin API; temperature 0.3, max_tokens 32000, reasoning_effort low; finish_reason: stop; usage: {'prompt_tokens': 17847, 'total_tokens': 40244, 'completion_tokens': 22397, 'prompt_tokens_details': {'cached_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 20348}, 'service_tier': 'standard'}. Trimis: extrasul protocolului (glosar, §1–§12a, §15, §20), `_work/mistral_msg_v03.txt`. Data: 2026-11-04 00:04.

---

## Problems found

**1. MAJOR — §11 (G4b): the noise-scaling formula does not produce the claimed expected ΔR² = 2δ.**
The gate sets σ²_ξ,r = s²_e,r·[(1 − R²_r(B_strong))/(2δ) − 1], with s²_e,r the episode-weighted residual variance. Under §8's definition (R²_r = 1 − SSE_r/SST_r, so ΔR² is measured against SST), adding Z = e + ξ to B_strong gives expected ΔR²_r = (s²_e,r − σ²_ξ,r)/s²_total,r = (1 − R²_r)(1 − σ²_ξ,r/s²_e,r). Setting this to 2δ requires σ²_ξ,r = s²_e,r·[1 − 2δ/(1 − R²_r)]. The protocol's formula puts 2δ in the denominator and multiplies by (1 − R²_r); under every standard reading (ΔR² vs. SST, vs. residual SSE, or vs. headroom) it yields an expected ΔR² far from 2δ (typically negative or enormous for small δ). Why it matters: G4b is the gate that decides whether an *equivalent* H1 may be reported as closing Level 2 (§15); a mis-scaled synthetic effect makes the pipeline-sensitivity check pass or fail for the wrong reason. Fix: σ²_ξ,r = s²_e,r·max(0, 1 − 2δ/(1 − R²_r(B_strong))) (ΔR² vs. SST), or state explicitly that ΔR² is a fraction of residual variance and use σ²_ξ,r = s²_e,r(1 − 2δ).

**2. MAJOR — §12: no decision rule if n_H1 alone exceeds the 200-run cap.**
The cap-reduction rule only drops F6, then F5. If n_H1 = max(n_TOST, n_MET) itself exceeds 200 − n_F1 − n_F4 (plausible when σ̂_up/δ is large, since δ has a floor of 0.02), the protocol has no fallback, yet "the SESOI rule is not relaxed." Why it matters: the confirmatory test could be infeasible at freeze with no prespecified action, inviting post-hoc scope or SESOI changes. Fix: add "if n_H1 > 200 − n_F1 − n_F4, the study stops at Stage 0 (reported), or H1 is declared underpowered at the achievable n with the SESOI unchanged."

**3. MINOR — §12: power statement contradicts the TOST formula.**
Text: "each at power 0.80 and one-sided α = 0.025." But n_TOST = ⌈(z_0.975 + z_0.90)²(σ̂_up/δ)²⌉ uses z_0.90, i.e., power 0.90 (10.51), while n_MET uses z_0.80 (7.85). The same convention appears in the H4 sizing (TOST at z_0.90 → 13.5). Why it matters: decision-rule internal consistency; a reviewer cannot tell which power the equivalence branch is sized for. Fix: change the sentence to "TOST at power 0.90, MET at power 0.80" (or change n_TOST to z_0.80).

**4. MINOR — §12: Stage B size is fixed at 40 paired seeds but n_H4 is computed separately, with no reconciliation rule.**
If n_H4 = ⌈13.5(σ̂_up/δ_B)²⌉ > 40, the protocol does not say whether Stage B is enlarged, or H4a/H4b are declared underpowered. "Frozen after the power simulation" partially covers this, but the fixed-size line and the formula line are not linked. Fix: "Stage B uses n_StageB = max(40, n_H4) paired seeds per scheduler, frozen after the power simulation; if n_H4 > 40 and the budget cannot accommodate it, H4a/H4b are reported as underpowered."

**5. MINOR — §8/§10.1: the joint bootstrap mechanics are underspecified.**
"10,000 resamples… test runs are resampled within family strata, jointly with the 250 training-run replicates." It is not stated how the 250 refitted training replicates enter each of the 10,000 BCa draws (one randomly drawn per draw? averaged? nested?). Why it matters: the confirmatory interval's level depends on this; two analysts would implement different intervals. Fix: "each BCa draw pairs the resampled test runs with one training replicate drawn uniformly from the 250 (or with the replicate-averaged prediction); state which."

**6. MINOR — §12: G6 training-run accounting is ambiguous.**
"Training runs: F1–F3, 30 base (15 and 60 for G6)" does not say whether 15 and 60 are additional runs (105 total) or replacements. §10.1/G6 references "the doubled Stage A training set (60 runs)," implying 30→60, but the parenthetical reads as extra arms. Fix: "30 base training runs; for G6, refit on 15 and on 60 runs (the 60-run set is 30 base + 30 additional), total 105 training runs."

**7. MINOR — §10.1/§11 (G1, G3): the ceiling mixes a correlation with an R².**
δ and the headroom use ceiling = r̄_AB (a correlation, uncorrected) minus R̄²_cal(B_strong) (a squared-error ratio). An R² is not bounded by r_AB in the same units; the reliability-consistent ceiling for R² would be r̄_AB² (or a disattenuated quantity). Why it matters: δ and the G3 headroom check (≥ 2.5δ) inherit this unit mismatch; with r̄_AB = 0.70 the implied ceiling is generous. Fix: define ceiling = r̄_AB², or state explicitly that r̄_AB is used as a linear ceiling and justify.

**8. MINOR — §2/§8: ρ̄ is a deterministic function of features already in the model.**
ρ̄ = Δc_e/max(ΔN,1), and ΔN (four-term basis) is in B_strong, so the pair {Δc_e, ρ̄} contributes exactly one new degree of freedom; G2 audits ρ̄ while H1's increment can only come through Δc_e's deviation from a function of ΔN. This is consistent with the identification note, but the protocol should state that the pair is effectively one feature so that G2's audit is understood as the operative identifiability check. Fix: one sentence in §8; no numeric change.

## §20 implementation check

All accepted changes I could verify against the shown sections are implemented as described (F2/F3-only H1 with family-stratified bootstrap; corrected pacing direction with ε = 1/(2K_reh); {increment, rate} entry with per-column constraints; deployment model and ≥10% task-selection check; refitted cross-run block-permuted G4; causal live-vs-placebo G8; 4-fold out-of-fold Stage 0 with 18/6 splits; q₀ = 64 throughout; context 8 and bias/LN weight-decay exclusion; pre-decay updates and L = 256 lag; agent-observable boundaries; C6 window rule; vocabulary partition; chunked distances; displacement formulas and D2 anchor caveat; R_maint/R_eval split and C10b; episode-weighted G1; G4b structure; divergence rule; H2 non-inferiority with δ_H2; search space and 250 replicates; G2/G2b/G5/G6/G7/G9 wording; moment persistence; storage and weak-ordering wording; strata; moment-reset diagnostic). No new contradictions introduced by §20 were found beyond items 3–6 above.

## Decision-rule consistency (§10, §11, §12, §12a)

Levels, Holm α_adj = 0.025/(3−j+1), z-quantities (2.394 = z_{1−0.025/3}; 10.51, 7.85, 10.47, 13.5 all recompute correctly), family-check sizing n_F5 = n_F6 = n_MET, the 200-run cap, and the 18/6 cross-fitting split are internally consistent, subject to items 2–4.

## Five changes to make first

1. Correct the G4b noise-scaling formula (§11) so the synthetic predictor's expected ΔR² is actually 2δ under §8's R² definition.
2. Add the missing fallback for n_H1 exceeding the 200-run cap (§12).
3. Reconcile the TOST power statement with the z_0.90 used in n_TOST and n_H4 (§12).
4. Specify how the 250 training-run replicates enter the 10,000 BCa draws (§8/§10.1).
5. Link Stage B's seed count to n_H4 and disambiguate the G6 training-run totals (§12).