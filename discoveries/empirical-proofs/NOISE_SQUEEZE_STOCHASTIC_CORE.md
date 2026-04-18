# Noise Squeeze and the Stochastic Core

## Every Domain Has an Irreducible Noise Floor — The Fingerprint of Fundamental Stochasticity

**Status:** L0 Exploratory Pattern. Observed universally. No formal theory yet.

---

## Statement

When higher-order polynomials (orders 3, 4, 5) are fitted to the sigma_A^2 trajectory, they extract progressively more signal from the parabolic residuals. At some order, the squeeze plateaus. What remains is the **stochastic core** — the irreducible noise floor of the domain.

Lock noise (residuals from the bowl fit) and anti-lock noise (residuals from the inverted bowl fit) are conjugate: they sum to zero. Their statistics differ: lock noise tends toward white noise, anti-lock noise tends toward coloured noise. This is a Heisenberg-like trade on the simplex.

## Squeeze Results

| Domain | Squeeze at order 5 | Interpretation |
|--------|-------------------|----------------|
| Room acoustics | 77% | 3rd and 4th acoustic forces hiding in residuals |
| Stellar nucleosynthesis | 86% | Burning stage transitions |
| Wine fermentation | 84% | Higher-order kinetics |
| Demographics | 84% | Hidden transition bend |
| Gold/Silver | 2.5% | Correct for D=2: parabola already captures 90% |
| Th-232 decay | 93.9% | Most regular stepping pattern |
| US Energy (Wisconsin) | 34.6% | Most structured energy transition |
| US Energy (Rhode Island) | 4.5% | Almost all noise, no signal |

## What the Stochastic Core Means

When squeeze plateaus, what remains is the floor beneath which no polynomial can reach. This is the compositional equivalent of:
- The VCO phase noise floor in a PLL
- The quantum zero-point energy
- The irreducible measurement uncertainty in a calibrated instrument

Each domain's stochastic core is its fingerprint — the residual randomness that no deterministic model can explain.

## Evidence

| Document | Location |
|----------|----------|
| Noise squeeze script | DATA/Scripts/eitt_pll_noise_squeeze.py |
| EXP-01 (2.5% squeeze) | codawork2026/experiments/EXP-01_Gold_Silver/EXP01_SEALED_CONCLUSION.json |
| EXP-02 (4.5-34.6%) | codawork2026/experiments/EXP-02_US_Monthly/EXP02_SEALED_CONCLUSION.json |
| EXP-03 (51-94% decay) | codawork2026/experiments/EXP-03_Uranium/EXP03_SEALED_CONCLUSION.json |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> noise_squeeze_stochastic_core (L0) |

---

*Below the signal, below the parabola, below the higher-order forces — there is the floor. That floor is the domain talking back.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T1, C1.1, O-3).*

### Formal Framework

The noise squeeze operates on the residuals of the PLL parabola. Given the second-order fit from T1:

    sigma_A^2(t) ~ sigma_A^2(t_0) + a(t - t_0)^2

the residual r_2(t) = sigma_A^2(t) - [sigma_A^2(t_0) + a(t - t_0)^2] contains both higher-order deterministic signal and stochastic noise. Successive polynomial fits of order n = 3, 4, 5 extract:

    r_n(t) = sigma_A^2(t) - P_n(t)

where P_n is the best-fit polynomial of degree n. The squeeze metric is:

    S_n = 1 - Var(r_n) / Var(r_2)

When S_n plateaus, the remaining variance is the stochastic core.

### The Conjugacy Property

Lock noise (residuals from bowl fit) and anti-lock noise (residuals from hill fit) are observed to sum to zero:

    r_lock + r_anti-lock = 0

This holds empirically in all tested domains. Their statistics differ: lock noise tends toward white noise (flat power spectrum), anti-lock noise tends toward coloured noise (1/f-like spectrum).

### Open Problem O-3 — Noise Conjugacy

**Statement:** Prove that lock noise + anti-lock noise = 0 for all domains.

**Partial progress:** Observed in 10/10 domains. Physically plausible — polynomial residuals in complementary regimes (bowl vs hill) should cancel if the total sigma_A^2 trajectory is smooth. No formal proof exists.

**If solved:** Would promote noise squeeze from L0 to L1.

### PLL Engineering Correspondence

| Stochastic core concept | PLL equivalent | Note |
|------------------------|----------------|------|
| Squeeze plateau | VCO phase noise floor | Irreducible oscillator noise |
| Lock noise (white) | In-band phase noise | Random walk around lock point |
| Anti-lock noise (coloured) | Out-of-band pull-in noise | Structured capture transient |
| Conjugacy (sum = 0) | Complementary filtering | Lock and anti-lock span the full noise budget |

This correspondence is analogical (L0) — not a formal mapping. It is recorded here because the analogy was the engineering instinct that led to the squeeze analysis.
