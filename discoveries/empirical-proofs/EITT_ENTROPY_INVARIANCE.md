# EITT: Entropy Invariance Under Geometric-Mean Decimation

## The Core Scientific Claim

**Status:** L5 Core Science. Validated across 8+ domains, 2 sealed experiments.

---

## Statement

Shannon entropy of legitimate compositional time series is near-invariant under geometric-mean block decimation across temporal resolutions.

In plain language: you can compress a compositional time series by factors of 2, 3, 5, 10, 50, even 341 — and the entropy changes by less than 1%. The compositional information is scale-free. Whether you look at daily data, monthly averages, annual summaries, or decade blocks, the structure tells the same story.

This holds for geometric-mean decimation. Arithmetic-mean decimation destroys it.

## Cross-Domain Evidence

| Domain | Source | Compression | Deviation | Verdict |
|--------|--------|-------------|-----------|---------|
| European prices | 8 countries, daily | 341:1 | 0.18% | PASS |
| EMBER energy | 6 countries, monthly | 12:1 | 1.02% mean | PASS |
| NGFS scenarios | 35 scenarios | 5yr, 10yr | 1.8%, 2.3% geom | PASS |
| Gold/Silver | 338 years, annual | 50:1 | 0.60% | PASS (sealed EXP-01) |
| US Energy | 10 states, monthly | 12:1 | 0.13-0.83% interior | PASS (sealed EXP-02) |
| QGP freeze-out | 8 collision energies | various | 0.27% | PASS |
| Geochemistry | 40,666 real rocks | various | 37/39 TAS types | PASS |
| Nuclear decay | 3 chains, AME2020 | 2:1 to 5:1 | 0.003-0.12% | PASS (sealed EXP-03) |

## Where It Correctly Fails

| Domain | Deviation | Why |
|--------|-----------|-----|
| US boundary states (WV, WY, RI, DE) | 2.8-8.8% | Monolithic compositions, >35% zeros |
| Neutron star EOS | 6.7% | Phase transition at muon threshold |
| Nuclear SEMF valley at M=12 | 1.16% | Non-stationary survey, extreme dynamic range |
| Random Dirichlet walks | 6.65% | No temporal autocorrelation |
| Shuffled/fabricated data | various | Correctly rejected as synthetic |

The failures are as informative as the passes. The method comes with built-in honesty.

## What It Means

EITT gives the first measurable consequence of the Aitchison geometry. The simplex has its own structure, and that structure is preserved under the geometric mean — the mean that Aitchison's geometry demands. The information is scale-free because the geometry is scale-free.

## Evidence

| Document | Location |
|----------|----------|
| EXP-01 Sealed | codawork2026/experiments/EXP-01_Gold_Silver/EXP01_SEALED_CONCLUSION.json |
| EXP-02 Sealed | codawork2026/experiments/EXP-02_US_Monthly/EXP02_SEALED_CONCLUSION.json |
| EXP-03 Sealed | codawork2026/experiments/EXP-03_Uranium/EXP03_SEALED_CONCLUSION.json |
| Adversarial tests | science/eitt/EITT_Adversarial_001.json |
| Hessian bound | science/eitt/EITT_HESSIAN_BOUND.md |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> EITT_entropy_invariance (L5) |

---

*The structure was always there. The geometric mean was always the right operation. EITT makes both visible.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T2, T3, L1, L2, FP2).*

### Formal Definition of the EITT Residual

The block decimation operator D_M maps a time series {x(t)}_{t=1}^{T} to {x_bar_G^{(b)}}_{b=1}^{floor(T/M)} where:

    x_bar_G^{(b)} = C(prod_{t in B_b} x(t)^{1/M})

The EITT residual is:

    delta_M = |H(D_M(series)) - H(series)| / H(series) * 100%

### Why It Works — The Three-Step Argument

**Step 1 (T2, exact):** CLR linearity ensures clr(x_bar_G) = (1/M) sum clr(x(t)). The geometric mean computes the arithmetic mean in CLR space.

**Step 2 (L2, Jensen gap):** Entropy is concave, so H(x_bar_G) >= (1/M) sum H(x(t)). The bias is upward but controlled.

**Step 3 (T3, Hessian bound):** The expected bias is bounded:

    |E[delta_M]| <= (D-1) * sigma_A^2 / (2*delta*M*H_bar) + O(M^{-3/2})

Under assumptions A1 (stationarity), A2 (interior regime: sigma_A^2 < delta*min(x_bar_i)), and A3 (mixing: autocovariance decays).

### The Hessian Bound — Proof Sketch

1. Taylor expand H(x) around x_bar to second order on the simplex.
2. First-order term vanishes by stationarity (E[deviation] = 0).
3. Hessian of H has eigenvalues bounded by -1/min(x_i). Trace contributes the leading term.
4. Under mixing (A3), the O(M^{-3/2}) remainder is controlled by the mixing rate.

### Structural Analogy: EITT as RG Fixed Point (FP2)

The invariance condition dH/dM = 0 is structurally analogous to a renormalization group fixed point: decimation by M is the "blocking" step, and entropy invariance is the fixed-point condition. **Important:** this is a framing device, not a theorem. Decimation is NOT a contraction mapping on (S^D, d_A) — Aitchison distances EXPAND under decimation.

### Open Problems

**O-1 (Central problem):** Prove a general theorem: under conditions C, |delta_M| < f(D, sigma_A^2, rho_1, M) for all legitimate compositional time series. The Hessian Bound provides an expected-value bound; what remains is a concentration inequality (tail bound).

**O-5:** Prove that geometric-mean decimation preserves the Renyi entropy family for q in (0, infinity). Empirically confirmed for q in [0.1, 5.0] across 3 domains.

**O-6:** Prove that any shape functional (function of ratios only, invariant to scaling) is EITT-invariant in the interior regime.

**O-7:** Derive a concentration inequality for |delta_M - E[delta_M]| using explicit mixing coefficients.

**O-8:** Extend EITT bounds to slowly-drifting (non-stationary) processes with drift velocity as a parameter.
