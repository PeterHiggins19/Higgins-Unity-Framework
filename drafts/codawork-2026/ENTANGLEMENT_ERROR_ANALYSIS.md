# HUF–CoDa Entanglement Error Analysis

## Where the instruments degrade — alone and together

*Peter Higgins · April 2026 · CoDaWork 2026 preparation*

The question: when HUF adopts CoDa's mathematical machinery, what error sources does it inherit? When CoDa adopts HUF's continuous monitoring application, what error sources does *it* inherit? And what new errors emerge only at the union — things neither system produces alone?

This is a diagnostic tool for the diagnostic tool.

---

## Table 1 — Error Sources by Origin

| # | Error Source | HUF Alone | CoDa Alone | HUF–CoDa Union | Detectable? | Governable? |
|---|-------------|-----------|------------|-----------------|-------------|-------------|
| **E-01** | **Wrong geometry on the simplex** | YES — TV distance treats simplex as flat Euclidean. Compositions near boundary are distorted. Spurious drift signals near dominant carriers. | NO — CoDa uses Aitchison geometry natively. | REDUCED — Aitchison distance corrects this. Dual-metric engine (TV + Aitchison) makes residual distortion visible where metrics disagree. | Yes: compare TV vs Aitchison on same data. Divergence = geometry artifact. | Yes: flag divergence zones, trust Aitchison in boundary regions. |
| **E-02** | **Closure bias (false correlation)** | PARTIAL — HUF normalizes to proportions but doesn't take log-ratios, so spurious correlations from constant-sum constraint are present but not amplified. | YES — closure is CoDa's first axiom. Well-understood. Addressed by working in log-ratio coordinates (CLR/ILR). | INHERITED — HUF inherits closure when adopting CoDa transforms. Properly handled if all analysis uses log-ratio space. Risk: mixing raw proportions with log-ratio results in same pipeline. | Yes: Aitchison (1986) subcomposition tests. | Yes: enforce log-ratio space throughout. Never mix raw proportions with CLR/ILR outputs. |
| **E-03** | **Zero replacement artifact (zeros tension)** | NO — HUF works with raw proportions, zeros are valid (carrier absent = 0). A carrier reaching exactly zero is the strongest possible structural signal: a fuel type retiring, a species disappearing, a market segment vanishing. HUF treats zero as a domain event first. | YES — log(0) is undefined. Every CoDa pipeline must replace zeros before log-ratio transforms. Replacement method (multiplicative, Bayesian, count-zero) affects results. Classical imputation inserts phantom presence. | NEW AT UNION — HUF previously tolerated zeros naturally. CoDa integration forces zero replacement, inserting instrument-generated values into the data. **Event-first protocol:** treat zero first as a domain event (flag it, attribute the carrier, record the TV velocity spike), then apply CoDa zero-handling protocols only if further geometric analysis is required. Greenacre's chiPower power-transform provides an elegant post-event correction layer that preserves subcompositional coherence while accepting genuine zeros (see E-17). | Yes: vary replacement method (multiplicative vs Bayesian vs count-zero vs chiPower). If signal changes, the replacement is the source. Compare TV spike before/after correction. | Yes: prioritize event flag. Report sensitivity to replacement method. Flag any drift signal that depends on zero-replacement choice. Apply chiPower as optional post-event layer for downstream geometry. |
| **E-04** | **Partition choice bias (SBP/ILR)** | NO — HUF has no partition structure. All carriers are peers. | YES — ILR balances require choosing a Sequential Binary Partition. Different partitions emphasize different contrasts. The choice is supposed to reflect domain knowledge but often reflects analyst convenience. | NEW AT UNION — HUF's coherence chain (1→2→4) provides a natural partition from system structure: reference vs stereo vs drivers, or fossil vs non-fossil vs subtypes. This is better than arbitrary SBP — but if the governance hierarchy doesn't match the system's actual structure, every balance carries that structural error. | Yes: compute balances under multiple SBPs. Signal robust to partition = real. Signal that vanishes under alternative partition = partition artifact. | Yes: derive SBP from system structure (governance hierarchy, physical grouping), not convenience. Test alternatives. |
| **E-05** | **Geometric mean flattening** | NO — HUF uses arithmetic operations on proportions. | YES — CLR divides by geometric mean of all components. Every carrier contributes equally to the mean regardless of dominance or governance relevance. A 0.1% trace carrier has the same geometric influence as a 60% dominant carrier. | INHERITED — when HUF computes CLR, governance-irrelevant carriers pollute the reference point. A noise carrier entering or leaving the composition shifts every CLR value. | Yes: compare CLR with ALR (asymmetric log-ratio using a specific reference carrier). If results differ meaningfully, geometric mean is the source. | Partially: use ALR with the governance reference carrier (the "1" in the 1→2→4 chain) as denominator. Or use ILR which avoids the geometric mean issue. |
| **E-06** | **Stale reference / anchor drift** | YES — HUF's "declared composition" (the authorized ratio state) is set by governance. If governance doesn't update the reference when the system legitimately changes, every subsequent reading shows phantom drift. | NO — CoDa is typically applied to static datasets, not continuous monitoring. No persistent reference. | AMPLIFIED AT UNION — Aitchison distance from a stale reference is geometrically correct but governancially wrong. The math says "big drift" when reality says "authorized transition." CoDa's precision makes a governance failure look like a system failure. | Yes: log governance decisions alongside readings. Undocumented drift = real alarm. Documented policy change + drift = reference update needed. | Yes: governance protocol (LOOP-001). Every authorized change updates the reference composition. |
| **E-07** | **Temporal aliasing** | YES — HUF samples at discrete intervals. If composition oscillates faster than sampling rate, drift appears smooth when it's actually volatile. Nyquist for compositional data. | NO — CoDa typically analyzes complete datasets, not time series. | AMPLIFIED AT UNION — perturbation velocity v(t) = d_A(x(t), x(t−1)) is only meaningful if sampling rate captures the dynamics. Annual EMBER data misses seasonal oscillations. Monthly data misses weekly dispatch cycles. The Aitchison distance between two points says nothing about the path between them. | Yes: compare velocity at different sampling rates. If halving the interval doubles detected events, you're aliased. | Yes: match sampling rate to system dynamics. Document the Nyquist boundary. Flag velocity measurements near it. |
| **E-08** | **Carrier admission error** | YES — KILL-1.1. If a carrier is admitted without domain justification, the instrument reads noise as structure. Adding a 7th carrier changes the simplex dimension and redefines all distances. | PARTIAL — CoDa assumes the analyst has already defined the composition correctly. Subcomposition coherence (Aitchison's principle) means you can analyze subsets, but the choice of what's in the full composition still matters. | AMPLIFIED AT UNION — Aitchison distance, CLR, ILR all change dimensionality when a carrier is added or removed. A spurious carrier doesn't just add noise — it restructures the entire geometry. In HUF-alone with TV distance, a noise carrier adds a small linear term. In HUF-CoDa, it changes the manifold. | Partially: domain expert review. No mathematical test distinguishes a legitimate 0.5% carrier from a noise carrier at 0.5%. | Yes: governance (KILL-001). Every carrier must have domain justification. Sensitivity test: remove carrier, recompute all metrics. If conclusions change, the carrier matters and needs justification. |
| **E-09** | **Subcomposition incoherence** | YES — HUF can analyze a subset of carriers without checking whether the analysis is consistent with the full composition. Simplex logic is violated. | NO — CoDa's subcompositional coherence principle (Aitchison 1986) guarantees that analysis of a subcomposition is consistent with the full composition when using log-ratio methods. | CORRECTED AT UNION — CoDa fixes a pre-existing HUF weakness. Subcomposition analysis in the Aitchison framework is automatically coherent. This is a genuine improvement, not an error source. | N/A — the error existed in HUF-alone and is resolved by the union. | Yes: use CoDa methods (CLR/ILR) for any subcomposition analysis. |
| **E-10** | **Instrument memory (stored energy)** | NO — by design. Open-loop doctrine (LOOP-001). The instrument has no state, no feedback, no accumulation. Each reading is independent. | NO — CoDa methods are stateless transformations. CLR of today's data doesn't depend on yesterday's CLR. | RISK AT UNION — if the monitoring system caches previous readings for velocity calculation, trend smoothing, or anomaly baselines, the instrument acquires memory. A rolling Aitchison distance baseline is stored energy. An exponential moving average on perturbation velocity is a feedback loop. The instrument starts influencing its own future readings. | Yes: verify that every metric is computable from current observation + declared reference only. Any metric requiring historical buffer = stored energy. | Yes: strict separation. Raw metrics use only current data + reference. Trend analysis is a separate governance layer, clearly labeled as derived, not observed. |
| **E-11** | **Dimensionality mismatch over time** | PARTIAL — if carriers enter or leave the system (new energy source appears, old one decommissioned), HUF on raw proportions simply gains or loses a dimension. Awkward but survivable. | YES — CoDa's log-ratio transforms require consistent dimensionality. You cannot compute Aitchison distance between a point in S³ and a point in S⁴. The compositions must have the same parts. | CRITICAL AT UNION — real systems change dimensionality. Solar didn't exist in 1980 electricity data. Adding it changes the simplex. CoDa has no native mechanism for comparing compositions of different dimension. HUF needs to monitor across structural transitions. | Partially: flag dimensionality changes as structural events. Split analysis at transition points. | Partially: project both compositions into a common subcomposition for comparison, OR treat the transition itself as the event of interest (a carrier admission event, KILL-1.1 in reverse). |
| **E-12** | **Outlier masking in Aitchison space** | NO — HUF with TV distance treats outliers linearly. A huge spike in one carrier shows up proportionally. | YES — log-ratio transforms compress extreme values. A carrier going from 1% to 0.01% is a 2-unit change in log space. A carrier going from 50% to 5% is a 2.3-unit change. The log compresses the dominant carrier's movement and amplifies the small carrier's. | INHERITED — Aitchison distance may understate dramatic changes in dominant carriers while overstating changes in trace carriers. TV distance has the opposite bias. | Yes: dual-metric engine. Where TV shows a large event but Aitchison shows small = dominant carrier movement. Where Aitchison shows large but TV shows small = trace carrier movement. | Yes: report both metrics. Use divergence between them as a diagnostic signal, not a problem. |

---

## Table 2 — Summary Scorecard

| Category | HUF Alone | CoDa Alone | HUF–CoDa Union |
|----------|-----------|------------|-----------------|
| **Errors present** | E-01, E-02 (partial), E-06, E-07, E-08, E-11 (partial) | E-02, E-03, E-04, E-05, E-08 (partial), E-11, E-12 | All 17 error sources are relevant |
| **Errors corrected by union** | E-01 (geometry), E-09 (subcomposition) | E-06 (stale reference — HUF governance fixes this) | — |
| **Errors inherited at union** | — | E-02, E-03, E-05, E-12 → enter HUF pipeline | E-06, E-07, E-08 → affect CoDa metrics |
| **Errors NEW at union only** | — | — | E-04 (partition choice matters more in continuous monitoring), E-10 (stored energy from temporal caching), E-11 amplified (dimensionality change breaks log-ratio time series) |
| **Net instrument quality** | Reads continuously but with wrong geometry and no subcomposition coherence | Mathematically rigorous but static, no governance, no temporal framework | Strongest instrument — but needs explicit governance of 17 error sources, not 6 |

---

## Table 3 — The Diagnostic Protocol

For each error source, the test to detect it and the governance action to contain it:

| Error | Detection Test | Governance Action |
|-------|---------------|-------------------|
| E-01 Wrong geometry | Compute TV and Aitchison on same transition. Report both. | Trust Aitchison near boundary. Flag divergence. |
| E-02 Closure bias | Check: are any analyses mixing raw proportions with log-ratio outputs? | Enforce: all analysis in log-ratio space OR raw space, never mixed. |
| E-03 Zero replacement | Recompute with 3 different replacement methods. Signal stable? | Report replacement method. Flag any result sensitive to method choice. |
| E-04 Partition bias | Compute ILR balances under 2+ alternative SBPs. Signal robust? | Derive SBP from system structure. Document rationale. Test alternatives. |
| E-05 Geometric mean | Compare CLR vs ALR (using governance reference carrier). Divergence? | Use ILR for final analysis. Use CLR for visualization only. |
| E-06 Stale reference | Compare declared reference date vs last governance decision. Gap? | Governance log. Every authorized change updates reference. |
| E-07 Temporal aliasing | Halve sampling interval. New events appear? | Document Nyquist boundary. Flag near-boundary measurements. |
| E-08 Carrier admission | Remove each carrier, recompute. Conclusions change? | KILL-001 review. Domain justification required for every carrier. |
| E-09 Subcomposition | Use CoDa methods for any subcomposition analysis. | Resolved by union. No further action. |
| E-10 Stored energy | Audit: does any metric require historical buffer? | Separate raw observation from derived trend. Label clearly. |
| E-11 Dimensionality | Flag any carrier entry/exit event. | Split time series at transitions. Common subcomposition for cross-epoch comparison. |
| E-12 Outlier masking | Report TV and Aitchison side by side. Divergence = scale artifact. | Dual-metric engine. Divergence is diagnostic information. |

---

## Table 4 — Extended Error Sources (E-13 through E-17)

*Discovered during CoDa literature cross-reference and Grok collective review, April 2–3, 2026.*

| # | Error Source | Origin | Description | Detection Test | Governance Action |
|---|-------------|--------|-------------|----------------|-------------------|
| **E-13** | **Quasi-coherence challenge** | Literature (Greenacre vs Egozcue debate) | Greenacre argues exact subcompositional coherence is overly restrictive; quasi-coherence suffices. HUF requires exact coherence for its hierarchical analysis to be consistent. HUF is independent engineering evidence for Egozcue's position. | Test: does HUF analysis break under quasi-coherence? If yes, exact coherence is required. | Lock to exact coherence in the pipeline. Document as design constraint. |
| **E-14** | **MEWMA stored energy as governance parameter** | MEWMA-CoDa convergence | The MEWMA smoothing constant λ is treated as a statistical tuning parameter. In the union, λ is a governance decision — it controls how much memory the instrument retains. Different domains need different λ for different reasons (cost of false alarm vs cost of missed event). | Audit: who set λ, when, and why? Is it documented? | Governance log for λ. Treat λ changes as reference updates. |
| **E-15** | **Compositional Nyquist** | HUF continuous monitoring | Temporal aliasing specific to compositions: if the simplex trajectory oscillates between sampling points, the measured perturbation underestimates true compositional volatility. No CoDa formalization exists. | Halve the sampling interval. If new compositional events appear (new perturbation spikes), you're aliased. | Document Nyquist boundary per domain. Flag near-boundary measurements. |
| **E-16** | **Dual-metric diagnostic tension** | HUF-CoDa union | TV distance and Aitchison distance disagree by design — their disagreement IS the diagnostic signal (dominant vs trace carrier movement). But operationalizing the disagreement requires a protocol: how much divergence is informative vs how much is noise? | Calibrate divergence on known ground truth (EMBER data with documented events). Establish baseline divergence profile. | Dual-metric protocol: report both, flag divergence exceeding baseline, diagnose via coherence chain which carrier group drives the disagreement. |
| **E-17** | **chiPower-HUF calibration tension** | Grok collective review (Greenacre entanglement) | Greenacre's chiPower power-transform (Box-Cox style θ parameter) provides zero-handling that preserves subcompositional coherence without imputation. When entangled with HUF's E-03 event-first doctrine, the union gains a calibrated zero-handling protocol — but introduces a new tuning parameter (θ) that must be governed. As θ→0, chiPower converges to Aitchison geometry; for θ>0, it down-weights extreme zeros while retaining the event signal. The choice of θ is a governance decision analogous to λ in E-14. | Vary θ. If conclusions change, θ is the source. Compare TV spike (event signal) before/after chiPower correction. | Governance log for θ. Event-first ordering: flag zero as domain event before any chiPower correction. θ choice must be documented and domain-justified. |

---

## Updated Summary

The error catalogue now contains **17 active error sources** (E-01 through E-17), each with a detection test and governance action. Two additional error sources (E-18: signed compositions, E-19: complex CoDa extensions) are catalogued as **HUF-EXT future research** — outside the current simplex pipeline, gated behind the open-loop breaker.

---

## What This Means for CoDaWork

This table is the conversation Peter brings to Coimbra. Not "HUF uses CoDa" and not "CoDa should adopt HUF." Instead:

**"Here are 17 ways our instruments degrade. Here's which ones I brought to you, which ones you'd bring to me, and which ones only appear when we work together. Here's how to test for each one. Here's how to govern each one. The entanglement makes us stronger — but only if we're honest about what it costs."**

That's not a sales pitch. That's a calibration study. Engineers and mathematicians both respect calibration studies.

---

---

## HUF-EXT — Future Research (Rough Diamonds)

*These error sources lie outside the current simplex pipeline. They cannot be added without violating Rule 1 (simplex carrier constraint). Filed here as future congress calibration topics for potential CoDa collaboration. Gated behind the open-loop breaker.*

| # | Error Source | Description | Status |
|---|-------------|-------------|--------|
| **E-18** | **Signed compositions** | Relaxing the simplex to allow negative contributions (ρᵢ ∈ [-1,1], Σρᵢ = 1). Relevant for net-flow domains: carbon budgets (source vs sink), financial net positions, spectral contrasts. Class B amplifier analogy: complementary devices handling positive/negative half-cycles. CoDa literature has emerging work on signed measures. | HUF-EXT future. Requires separate carrier space. |
| **E-19** | **Complex CoDa extensions** | Carriers as complex-valued (ρᵢ ∈ ℂ) with complex sum constraint. Separates magnitude and phase in the ratio state. Relevant for frequency-domain spectra, quantum probability amplitudes, cyclical flows. | HUF-EXT future. Requires complex Aitchison-style geometry. |

*Both extensions could use HUF's governance layer (event-first flagging, dual-metric diagnostics, calibrated error catalogue) while CoDa supplies the extended geometric transforms. Neither alters the current pipeline.*

---

*Cross-references: [BATTLE_CARD.md](BATTLE_CARD.md) (gap #6 — concentration measure), [FORMULA_REFERENCE.md](FORMULA_REFERENCE.md) (all CoDa formulas), [THE_CORE.md](THE_CORE.md) (coherence chain), [KILL-001](../../huf-gov/governance/KILL-001-kill-test.json) (failure modes), [LOOP-001](../../huf-gov/governance/LOOP-001-open-loop-doctrine.json) (open-loop doctrine)*
