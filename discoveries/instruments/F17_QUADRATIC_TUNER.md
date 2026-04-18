# F17 Quadratic Tuner

## An Early Warning System for When to Distrust the Geometric Mean

**Status:** L2 Process Control Candidate. Validated on 10 US states (R^2 > 0.96 in all). Requires wider cross-domain calibration.

---

## Statement

The gap between geometric and arithmetic EITT deviations, fitted as a quadratic in compression ratio M:

    gap(M) = a*M^2 + b*M + c

provides a contamination signal that measures near-vertex stress. The quadratic coefficient 'a' is always negative (sub-linear growth). The linear coefficient 'b' dominates.

F17 does **NOT** modify the EITT reading. It tells you when to distrust it.

## The Pennsylvania Crossover

Pennsylvania is the canonical bridge state: at M=12, geometric EITT fails (1.09%) but arithmetic EITT passes (0.87%). The geometric mean amplifies near-zero monthly carriers through log-space averaging. F17 detects this stress before the threshold is crossed.

**Early warning rule:** If the gap exceeds 2% at M=6, the geometric EITT will likely fail at M=12.

## Results

All 10 US states show R^2 > 0.96 for the quadratic fit:
- Coefficient 'a' always negative (sub-linear growth)
- Coefficient 'b' always positive (linear dominant)
- Interior states: small gap, low stress
- Boundary states: large gap, high stress

## Design Principle

F17 is separate from the core EITT observable by design. The constraint: **the tuner does NOT modify the EITT reading.** It is a process-control instrument — a gauge on the dashboard, not a hand on the steering wheel.

## Evidence

| Document | Location |
|----------|----------|
| F17 tuner data | DATA/Energy/EXP02_quadratic_tuner.json |
| EXP-02 Sealed | codawork2026/experiments/EXP-02_US_Monthly/EXP02_SEALED_CONCLUSION.json |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> f17_quadratic_tuner (L2) |

---

*The gap is the canary. The tuner reads the canary. The EITT reading stands on its own.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T2, L2, canonical values).*

### Formal Definition

Let delta_G(M) be the geometric EITT residual and delta_A(M) the arithmetic EITT residual at compression ratio M. The F17 gap function is:

    gap(M) = delta_A(M) - delta_G(M)

Fitted as a quadratic:

    gap(M) = a*M^2 + b*M + c

The coefficients carry physical meaning:

| Coefficient | Sign | Meaning |
|-------------|------|---------|
| a | Always negative | Sub-linear growth (gap saturates) |
| b | Always positive | Linear dominant (gap grows with compression) |
| c | Small | Intercept (gap at M=1 should be zero) |

### Why the Gap Exists

By T2 (CLR Linearity), the geometric mean computes the exact arithmetic mean in CLR space. The arithmetic mean does NOT satisfy this identity. The gap measures the discrepancy between:

1. Exact CLR averaging (geometric mean) — preserves compositional structure
2. Naive averaging (arithmetic mean) — distorts CLR coordinates

By L2 (entropy concavity), both means create an upward entropy bias, but the arithmetic mean's bias grows faster with compositional variance.

### Operating Envelope Thresholds

| Threshold | Value | Action |
|-----------|-------|--------|
| F17 R^2 minimum | > 0.96 | All 10 US states exceed this |
| Early warning trigger | gap > 2% at M=6 | Geometric EITT will likely fail at M=12 |
| Pennsylvania crossover | geometric 1.09%, arithmetic 0.87% | Bridge state: geometric amplifies near-zero carriers |

### Design Constraint

F17 is a gauge, not a hand on the wheel. It operates in the process-control layer (Pass 2 of the Two-Pass Instrument). It does NOT modify the EITT reading. This separation is mandated by the Governed Breakpoint Principle: the instrument reads, never actuates.
