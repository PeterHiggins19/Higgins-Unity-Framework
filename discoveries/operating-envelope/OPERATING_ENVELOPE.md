# The Operating Envelope

## Where the Method Works, Where It Breaks, and Why

**Status:** L4 Canonical Method Component. Established by EXP-02, refined by EXP-03.

---

## Statement

EITT is reliable when:
- Shannon entropy H > 1.0 (sufficient compositional diversity)
- Zero rate < 15% (sparse zeros manageable by multiplicative replacement)
- The ordering parameter represents a true parametric walk (each step is a physical transformation)

EITT correctly fails when:
- Zero rate > 35% (multiplicative replacement introduces artifacts)
- Shannon entropy H < 0.7 (monolithic composition — one carrier dominates)
- The data is an ordered survey, not a parametric walk (non-stationarity across regimes)

## The Evidence

### EXP-02: Interior vs Boundary States

| State | Band | H_bar | Zero rate | Max EITT | Verdict |
|-------|------|-------|-----------|----------|---------|
| California | interior | 1.485 | 1.6% | 0.83% | PASS |
| Minnesota | interior | 1.364 | 6.1% | 0.49% | PASS |
| Texas | interior | 1.219 | 5.7% | 0.21% | PASS |
| Wisconsin | interior | 1.181 | 5.9% | 0.13% | PASS |
| Pennsylvania | bridge | 1.124 | 9.6% | 1.09% | FAIL (geometric) / PASS (arithmetic) |
| North Carolina | bridge | 1.222 | 12.4% | 0.21% | PASS |
| Rhode Island | boundary | 0.278 | 47.5% | 8.78% | FAIL |
| West Virginia | boundary | 0.289 | 36.9% | 5.28% | FAIL |
| Wyoming | boundary | 0.511 | 40.1% | 2.82% | FAIL |
| Delaware | boundary | 0.695 | 47.2% | 6.44% | FAIL |

The 1% threshold separates cleanly. The boundary states fail by factors of 3-9x.

### EXP-03: Walk vs Survey

Decay chains (true parametric walks): **0.003-0.12% deviation. All PASS.**

SEMF valley (ordered survey): **1.16% at M=12. FAILS at high compression.**

The distinction: each step in a decay chain IS a physical transformation with similar-magnitude perturbation. The valley of stability is a survey where Z=2 (Helium) and Z=92 (Uranium) are qualitatively different physics.

### PLL Operating Envelope

The parabola requires **two competing compositional forces** creating a balance point:
- Gold vs Silver monetary demand: parabola with R^2 = 0.90
- Fossil vs renewable energy: parabola in 8/10 states
- Decay chains: hill-shaped relaxation (one force dominates — relaxation, not competition)
- SEMF valley: L-shaped (Volume binding dominates at all Z) — R^2 = 0.20, parabola fails

## Safety Fences

1. **Do not apply EITT to compositions where >35% of observations are zero** without switching to arithmetic decimation or pre-filtering zero carriers.
2. **Do not apply the PLL parabola to systems without two-force competition.** The parabola model is inappropriate when one force dominates. The slope diagnostic still works.
3. **Distinguish parametric walks from ordered surveys.** EITT requires approximate stationarity along the ordering parameter.
4. **Use F17 as an early warning.** If the geometric-arithmetic gap exceeds 2% at M=6, the geometric EITT will likely fail at M=12.

## Evidence

| Document | Location |
|----------|----------|
| EXP-02 Sealed | codawork2026/experiments/EXP-02_US_Monthly/EXP02_SEALED_CONCLUSION.json |
| EXP-03 Sealed | codawork2026/experiments/EXP-03_Uranium/EXP03_SEALED_CONCLUSION.json |
| Safety boundaries | science/eitt/EITT_SAFETY_BOUNDARIES.md |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> operating_envelope (L4) |

---

*The envelope is the honesty. It tells you where the instrument should not be trusted. Every high-power system must contain intentional, predictable failure points.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T3, L2, canonical values).*

### Formal Threshold Derivation

The operating envelope thresholds derive from the interaction of entropy concavity (L2) and the Hessian Bound (T3):

**Entropy minimum (H > 1.0):** When Shannon entropy H is low, the composition is near a vertex of the simplex (one component dominates). The Hessian of H has eigenvalues proportional to -1/x_i. Near a vertex, min(x_i) -> 0, making the Hessian eigenvalues diverge. The second-order bound in T3 breaks down because sigma_A^2 is no longer small relative to delta*min(x_bar_i).

**Zero rate (< 15%):** Multiplicative zero replacement maps structural zeros to small positive values. For zero rates below 15%, the replacement has negligible effect on CLR coordinates (the replaced values are far from any compositional force). Above 35%, the replacement dominates the CLR structure and creates artificial entropy.

**Parametric walk requirement:** The Hessian Bound (T3) assumes A1 (stationarity) and A3 (mixing). Ordered surveys (e.g., the SEMF valley by atomic number) violate both: Z=2 and Z=92 represent qualitatively different physics, and there is no ergodic mixing across the ordering parameter.

### Boundary Regime Classification

| Regime | H_bar | Zero rate | sigma_A^2 | EITT behaviour |
|--------|-------|-----------|-----------|----------------|
| Interior | > 1.0 | < 15% | moderate | Hessian Bound applies, delta_M < 1% |
| Bridge | 0.7-1.0 | 10-20% | elevated | F17 early warning triggers |
| Boundary | < 0.7 | > 35% | extreme | Hessian Bound breaks, delta_M > 2% |

### The EITT Pass Threshold — Why 1%

The 1% threshold is the empirical boundary between interior-regime compositions (where the Hessian Bound predicts small delta_M) and boundary-regime compositions (where the bound diverges). It is calibrated against:

- 8+ passing domains (all < 1% at moderate compression)
- 4+ failing boundary states (all > 2.8%)
- The Pennsylvania bridge case (1.09% geometric, 0.87% arithmetic)

### Canonical Threshold Values

| Parameter | Value | Source |
|-----------|-------|--------|
| EITT pass | < 1% | Empirical calibration, 30+ domains |
| Entropy minimum | H > 1.0 | Hessian eigenvalue divergence |
| Zero rate maximum | < 15% | Multiplicative replacement stability |
| Zero rate hard fail | > 35% | Structural artifact dominance |
| F17 R^2 threshold | > 0.96 | All 10 US states |
| F17 early warning | gap > 2% at M=6 | Pennsylvania crossover prediction |
