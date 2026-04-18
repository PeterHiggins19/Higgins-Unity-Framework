# MC-4: The Fourth Monitoring Category

## Composition Monitoring — What Percentage-Based Monitoring Misses

**Status:** L3 Validated Companion. CoDaWork 2026 falsifiable claim. 5-AI literature verification found no prior art.

---

## Statement

Existing monitoring frameworks operate in three categories:
- MC-1: Magnitude (how much?)
- MC-2: Identity (what is it?)
- MC-3: Trend (where is it going?)

None of them answer: **when did the composition change, which carrier moved, and was it real or noise?**

MC-4 (Composition Monitoring) fills this gap using Aitchison geometry: compositional change is measured as perturbation on the simplex, drift is detected via self-calibrated thresholds on Aitchison distance, and individual carrier contributions are identified through CLR decomposition.

## The Falsifiable Claim

No existing monitoring framework performs compositional change detection at the carrier level with formal perturbation-based drift measurement.

Four defeats required — any ONE would falsify the claim:
1. Published system using Aitchison metric on energy-mix compositions to detect drift
2. Published system measuring change as perturbation rather than arithmetic difference
3. Published system at individual carrier level within the simplex
4. Theoretical proof that CoDa adds no information beyond percentage-based monitoring

Five-AI literature verification (Claude, ChatGPT, Grok, Gemini, Copilot): **no prior art found.**

## What MC-4 Detects

| Country | Event | MC-4 Detection |
|---------|-------|----------------|
| Germany | Nuclear shutdown Apr 2023 | d_A = 9.07, sigma = 3.68 |
| Japan | Fukushima full shutdown 2013-14 | d_A = 9.05, sigma = 3.52 |
| UK | Coal collapse acceleration 2017-18 | d_A = 3.23, sigma = 2.48 |
| UK | COVID + coal near-zero 2019-20 | d_A = 3.26, sigma = 2.51 |

All detected without being told they happened. Self-calibrated per country.

## The Three-Diagnostic Protocol

TV (Total Variation) + Aitchison distance + coherence residual. Metric agreement = robustness. Metric disagreement = diagnostic information about the TYPE of compositional change.

Inherited from the paired-measurement doctrine in acoustic engineering: a flat frequency response can hide directional redistribution. One curve lies. Two curves diagnose.

## Evidence

| Document | Location |
|----------|----------|
| EMBER protocol | data/ember/codawork_ember_protocol.py |
| EMBER results | data/ember/codawork2026_results.json |
| CoDaWork abstract | codawork2026/presentation/abstract_v3_submitted.md |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> mc4_fourth_monitoring_category (L3) |

---

*The percentages can lie. The simplex cannot. MC-4 reads the simplex.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (notation table, T2).*

### Formal Definitions

**Compositional change detection** uses the perturbation difference:

    Delta(t) = C(x_1(t+1)/x_1(t), ..., x_D(t+1)/x_D(t))

This measures compositional change between consecutive time steps as a perturbation on the simplex.

**Drift detection** uses the Aitchison distance:

    d_A(x(t), x(t+1)) = ||clr(x(t)) - clr(x(t+1))||_2

Self-calibrated thresholds: the drift alarm triggers when d_A exceeds a country-specific baseline derived from the historical distribution of d_A values.

**Carrier-level decomposition** uses CLR components:

    clr_i(x(t+1)) - clr_i(x(t))

The carrier with the largest absolute change is the driver of the compositional shift.

### The Three-Diagnostic Protocol

| Diagnostic | Formula | What it measures |
|-----------|---------|-----------------|
| Total Variation (TV) | sum |x_i(t+1) - x_i(t)| | Raw percentage change |
| Aitchison distance d_A | ||clr(x(t+1)) - clr(x(t))||_2 | Compositional distance |
| Coherence residual | d_A - k*TV | Discrepancy between percentage and compositional views |

Metric agreement = robustness. Metric disagreement = diagnostic information about the TYPE of change.

### Why Aitchison Distance, Not Euclidean

Euclidean distance on raw percentages is not subcompositionally coherent: adding or removing a carrier changes all pairwise distances. Aitchison distance is:

1. **Subcompositionally coherent** — distances between subcompositions are consistent with the full composition
2. **Permutation invariant** — the ordering of carriers does not affect the distance
3. **Scale invariant** — multiplying all carriers by a constant does not change d_A

These properties are inherited from the Aitchison inner product on S^D (see notation table).

### Canonical Detection Values

| Country | Event | d_A | sigma | Detection confidence |
|---------|-------|-----|-------|---------------------|
| Germany | Nuclear shutdown 2023 | 9.07 | 3.68 | > 2 sigma |
| Japan | Fukushima 2013-14 | 9.05 | 3.52 | > 2 sigma |
| UK | Coal collapse 2017-18 | 3.23 | 2.48 | > 1 sigma |
| UK | COVID + coal 2019-20 | 3.26 | 2.51 | > 1 sigma |
