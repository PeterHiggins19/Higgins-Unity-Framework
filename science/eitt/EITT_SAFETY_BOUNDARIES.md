# EITT Safety Boundaries — When Not to Use It

**Status:** Living document. Updated whenever a new failure mode is observed in validation work or reported from external use. Read this before applying EITT to any consequential analysis.

**Date:** 2026-04-15 (Phase 2 start)
**Companion to:** `EITT_HESSIAN_BOUND.md` (the rigorous second-order theorem) and `EITT_WHY_IT_WORKS.md` (the conceptual framework, including the shape/magnitude decomposition in §7)

---

## Why this document exists

EITT is a powerful tool when applied inside its domain of validity. Outside that domain it can produce results that look statistically clean but are scientifically misleading — an invariance claim where no real invariance holds, or a drift flag where no real drift exists. In high-stakes settings (clinical trials, environmental regulation, financial risk) a misleading result can cause harm that is hard to reverse.

This document is the safety fence. It lists the assumptions EITT requires, the failure modes that occur when each assumption is violated, the sample-size requirements for a reliable answer, the domain-specific red flags, and the sanity checks a practitioner should run before trusting an EITT result.

## The three core assumptions

From `EITT_HESSIAN_BOUND.md`, the second-order theorem requires:

**(A1) Interior bound.** Every component of every observation is bounded away from zero: `x_i(t) ≥ δ > 0` for all `i, t`. This is the boundary-avoidance condition.

**(A2) Finite second moment.** The Aitchison covariance `Σ = Cov(clr(x(t)))` has finite trace `σ_A² = tr(Σ)`.

**(A3) Sufficient mixing.** The process is stationary and autocorrelation decays fast enough that the CLT applies to block averages: `Cov(x̄_M) ≈ Σ/M + o(1/M)`.

Each assumption has a characteristic failure mode when violated. Knowing the signatures protects against silent misinterpretation.

## Failure modes by assumption

### (A1) violated — boundary-close compositions

**What it looks like.** One or more carriers have proportions close to zero in a significant fraction of observations. Rare species in ecology. Trace-level chemical components. Marginal treatment arms. Pathway-specific gene expression at detection limit.

**Why it breaks EITT.** The Hessian of Shannon entropy has diagonal entries `1/x_i`. When `x_i → 0`, these entries blow up, and the second-order Taylor correction becomes enormous. The `1/δ` factor in the bound `(D−1)σ_A²/(2δM)` drives the predicted residual to arbitrarily large values.

**Observed signatures.** The Jensen correction in Chemistry Findings showed a 476% overcorrection at ionic-liquid boundaries — `claim_5_jensen_overcorrection` in `science/eitt/INDEX.json`. This is the canonical example.

**What to do.** Either drop the near-zero carriers (amalgamation), or use a bounded-curvature entropy lens (Aitchison norm, Rényi q=2 collision entropy) that does not have the `1/x_i` singularity. The repo's four-lens analysis in CheMixHub demonstrates the Aitchison rescue.

**Hard red flag.** Do not apply EITT with Shannon entropy to compositions where `min(x_i) < 0.01` in any significant fraction of the data.

### (A2) violated — infinite or near-infinite variance

**What it looks like.** Compositions with extremely heavy tails. Financial markets during crashes. Species abundances dominated by one massive outlier observation. Data with severe measurement-outlier contamination.

**Why it breaks EITT.** The second-order Taylor term is a variance-weighted trace. Undefined variance means undefined bound.

**Observed signatures.** Rare in real compositional data because the unit-sum constraint bounds everything. More common as a symptom of measurement errors or preprocessing bugs than of genuine distributional pathology.

**What to do.** Identify and handle outliers before applying EITT. Compositional boxplots (Aitchison-geometry versions) help. Winsorization in clr space is one option; removal is another.

**Red flag.** Trimmed-mean Aitchison variance differs from raw Aitchison variance by more than a factor of two. You have outlier contamination and should clean before proceeding.

### (A3) violated — insufficient autocorrelation

**What it looks like.** Sequences that are not stationary, or that have autocorrelation so weak that the CLT doesn't apply. Dirichlet random noise. Step-function regime changes. Oscillating extremes. Strong drift over the observation window.

**Why it breaks EITT.** The bound assumes block covariance scales as `Σ/M`. Under insufficient mixing, block covariance scales more slowly or not at all, and the predicted residual underestimates what actually occurs.

**Observed signatures.** This is the entire `EITT_Adversarial_001.json` suite. Seven synthetic failures including Dirichlet noise, step functions, oscillating extremes, monotonic linear drift. These are not pathological inventions — each matches a real-world pattern that can occur in applied settings.

**What to do.** Before applying EITT, check the integrated autocorrelation time `τ_int`. If `τ_int < 2` (essentially white noise) the CLT still applies but the data is structurally uninformative. If `τ_int` approaches the series length, the effective sample size is one and EITT gives a vacuous result. If there is obvious regime change within the window, segment the data and analyze each regime separately.

**Red flag.** Observed EITT residual exceeds theoretical bound by more than 2×. Either (A3) is violated or the data contains a regime change that should be flagged and excluded from the stationary analysis.

## Sample-size requirements

The second-order Hessian bound shows the predicted residual scaling as:

    |δ_M| ≤ (D−1) σ_A² / (2δ M H̄)

For the bound to be tight enough to be useful — say, below 5% — you need:

    M · δ · H̄ > (D−1) σ_A² / 0.1

Rough rules of thumb for typical compositional data:

- **D ≤ 4** (small number of carriers): reliable with `M ≥ 10` blocks if `δ ≥ 0.05`
- **D = 5–10** (medium): reliable with `M ≥ 30` blocks if `δ ≥ 0.02`
- **D > 10** (many carriers): reliable only with `M ≥ 100` blocks and careful `δ` management

These are minimum compression ratios. They assume `σ_A²` is typical for the domain. Short time series with many carriers are fundamentally hostile to EITT — no amount of cleverness rescues a 12-point series on 20 carriers.

## Domain-specific red flags

### Clinical and biomedical

This is where the danger is highest, because clinical compositional data (cell type fractions, microbiome abundances, gene expression ratios, immune cell subsets) often combines small cohorts, short time series, boundary-close compositions, strong treatment effects that confound stationarity, and high-stakes downstream decisions.

**Specific red flags:**

- **Cohort size < 20** combined with longitudinal compositional data: EITT lacks statistical power regardless of the bound's nominal value. Absence of detected drift is not evidence of absence of drift.
- **Time series with < 5 measurement points**: second-order CLT approximation is not justified. Use different methods.
- **Rare cell populations or microbial taxa with abundances < 1%**: (A1) violated. Either amalgamate rare categories or use the Aitchison-norm lens, not Shannon.
- **Treatment change within observation window**: stationarity violated by design. Apply EITT separately to pre-treatment and post-treatment segments, not across the transition.
- **Multiple primary endpoints**: if you are testing EITT invariance across many patients, many time windows, or many analytes, correct for multiple testing. Bonferroni is conservative but safe.
- **Effect size interpretation**: "EITT invariant" does not mean "no biological effect occurred." It means the compositional structure, summed over the carriers you chose, stayed within a specific bound. The inverse does not hold.
- **Comparison against external threshold**: EITT's bound is an internal consistency check, not a clinical effect size. Do not report EITT residuals as clinical effect sizes.

**The canonical misuse example.** A breast cancer microbiome study with 15 patients, three measurement points per patient (pre-treatment, mid-treatment, post-treatment), 50 taxa many of which are near-zero, tries to use EITT to test whether the treatment is "composition-stable" and concludes that it is. The conclusion is almost certainly a power problem, not a biological finding. EITT should not have been used here.

### Environmental monitoring and hydrology

- **Seasonal transitions**: stationarity violated. Apply within season, not across.
- **Rare flow components (snowmelt, event water)**: δ → 0 during their off-seasons. Handle by segmentation or Aitchison-norm lens.
- **Extreme events (floods, droughts)**: regime changes by definition. Flag and exclude from stationary analysis, or study transition itself as the object of interest.
- **Sensor drift**: technical non-stationarity can masquerade as (A3) violation. Investigate before interpreting.

### Financial and economic

- **Regime shifts (pre/post crisis, pre/post regulatory change)**: obvious stationarity violations. Segment.
- **Market microstructure effects at high frequency**: autocorrelation structure is dominated by effects below the window of interest. EITT needs careful window choice.
- **Missing data and asynchronous observations**: compositional methods assume all carriers measured at each time. Complicated missing-data patterns break the setup.

### Physical and chemical systems

This is where EITT is best-behaved. Stationary interior regimes dominate and the assumptions are typically met. Even here:

- **Near phase boundaries or mixing gaps**: δ drops and the bound loses tightness. Proof 4 (CheMixHub) documents this regime.
- **Reactive systems**: non-conservative dynamics can violate the compositional framework entirely.

## Sanity-check checklist

Before trusting any EITT result in a consequential setting, run through these five checks. If any fails, investigate before proceeding.

1. **Proportion floor check.** Is `min_t min_i x_i(t) ≥ 0.01`? If no, either amalgamate or use Aitchison-norm lens.
2. **Autocorrelation check.** Compute `τ_int` for each clr coordinate. Is it between 2 and 0.1 × series length? If outside this range, EITT is either uninformative (too little autocorrelation) or vacuous (too much).
3. **Sample-size check.** Does `M · δ · H̄ > (D−1) σ_A² / 0.1` for your target tightness? If no, EITT lacks power.
4. **Regime-change check.** Apply EITT to overlapping sub-windows. Does the residual jump anywhere? If yes, segment around the jump rather than analyzing the full series.
5. **Bound-consistency check.** Is the observed residual within 2× of the theoretical bound? If no, one of (A1), (A2), (A3) is violated and the result is not reliable.

## Responsible-use examples

**Appropriate.** Monthly energy-generation mix of a mature power grid over 10+ years, tracking compositional stability of the fossil/renewable/nuclear mix, with drift flags expected around policy changes and major infrastructure events. Assumptions (A1-A3) typically hold; sample size is adequate; domain is well-understood; red flags are visible when present.

**Appropriate.** Long-term ecological community composition at a stable habitat with well-designed sampling protocol, tracking compositional stability across seasonal cycles, with residuals interpreted relative to season and with rare-species boundary handled by amalgamation or lens choice.

**Appropriate but requires care.** Manufacturing quality control where compositional output of a production process is monitored for drift. EITT can work here if the process is normally stationary and the sample size is adequate, but treatment changes (new feedstock, process adjustment) must be treated as segment boundaries and not smoothed through.

## Inappropriate-use examples

**Inappropriate.** Clinical trial with 15 patients and three longitudinal measurements each. Sample size inadequate; cohort effects confound temporal structure; EITT produces a number but it does not support any clinical claim.

**Inappropriate.** Comparison of two populations via EITT residual magnitude. EITT is not a two-sample test; it is a within-series consistency check. Use appropriate comparative compositional statistics.

**Inappropriate.** Applying EITT to a series of ten measurements covering a known treatment transition. The series is non-stationary by design; EITT will either miss the transition (if the bound is loose) or flag it correctly but without the granular resolution a proper change-point method would provide.

**Inappropriate.** Reporting EITT-stable as "the biological system did not change" to a non-compositional audience. The result is about the compositional structure under specific assumptions, not about the underlying biology.

## When things go wrong

If you apply EITT and the result looks anomalous, work through the diagnosis in this order:

1. Check the five sanity-check items above. Most anomalies trace to one of them.
2. Inspect the data for outliers, missing values, sensor drift, or preprocessing bugs.
3. Segment the data by time or by experimental condition and reapply.
4. Try an alternative entropy lens (Rényi q=2, Aitchison norm, Jensen-corrected Shannon).
5. If the anomaly persists after all of the above, you may have discovered a genuine regime change or a violation that EITT is correctly flagging. This is the useful case — take it seriously.
6. Report unresolved anomalies back to the repository so the safety document can be updated. Every documented failure mode saves future users from the same trap.

## Update history

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-15 | Initial version at Phase 2 start. Covers assumptions, failure modes, sample-size rules, domain red flags, sanity checklist, responsible-use and inappropriate-use examples. |

This document is expected to grow. If you use EITT and hit a failure mode that is not documented here, the failure mode belongs here.
