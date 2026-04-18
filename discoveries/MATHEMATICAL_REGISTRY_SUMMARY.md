# HUF Mathematical Registry — Executive Summary Addendum

*Created 2026-04-18. Companion to HUF_Executive_Summary_2026-04-18_v2.docx.*
*Full machine-readable registry: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json*

---

## Theorems and Proofs

| ID | Name | Status | Statement (compact) |
|----|------|--------|-------------------|
| T1 | Vertex Theorem | PROVED (exact) | d(sigma_A^2)/dt = (2/D) sum clr_i * clr_i' = 0 implies clr(t*) perpendicular to clr'(t*) |
| T2 | CLR Linearity | PROVED (exact) | clr(x_bar_G) = (1/M) sum clr(x(t)). No approximation. |
| T3 | Hessian Bound | Proof sketch | |E[delta_M]| <= (D-1)*sigma_A^2 / (2*delta*M*H_bar) + O(M^{-3/2}) |

## Lemmas

| ID | Name | Status | Statement (compact) |
|----|------|--------|-------------------|
| L1 | Balance Mean Preservation | Proved | ILR coordinates preserved exactly under decimation. SBP choice irrelevant. |
| L2 | Entropy Concavity | Known result | H(x_bar_G) >= (1/M) sum H(x(t)). Jensen gap is the upward bias. |

## Corollaries

| ID | Parent | Name | Key result |
|----|--------|------|-----------|
| C1.1 | T1 | PLL Error Signal | epsilon(t) = 2a(t - t_0), factor of 2 from chain rule |
| C1.2 | T1 | Bowl vs Hill | a > 0: lock (stable); a < 0: anti-lock (relaxation) |
| C1.3 | T1 | Vertex as Transition Date | t_0 marks dynamic equilibrium |
| C-L1 | L1 | SBP Independence | Any ILR basis gives same balance-mean values |

## Fixed-Point and Banach Results

| ID | Name | Status | Key fact |
|----|------|--------|---------|
| FP1 | ADAC Convergence | Claimed (numerical: L ~ 0.4) | Banach contraction on (S^D, d_A). Formal L derivation missing. |
| FP2 | EITT as RG Fixed Point | Analogy only | dH/dM = 0 analogous to RG fixed point. NOT a contraction. |
| FP3 | H1 Operator Fixed Point | Claimed (external paper) | Lyapunov V = 1 - mu, V_dot = -gamma(1-mu)^2 <= 0 |
| FP4 | Refresh Chain v3.2 | Administrative | Document consistency marker, not mathematical fixed point |

## Open Problems

| ID | Statement | If solved |
|----|-----------|-----------|
| O-1 | General EITT invariance theorem with concentration inequality | EITT promoted from empirical to mathematical theorem |
| O-2 | Prove sigma_A^2 generically parabolic under mild regularity | PLL universality L1 -> L2 |
| O-3 | Prove lock noise + anti-lock noise = 0 | Noise squeeze L0 -> L1 |
| O-4 | Derive ADAC contraction constant L analytically | Boundary species convergence formalised |
| O-5 | Renyi entropy invariance under geometric-mean decimation | EITT generalised beyond Shannon |
| O-6 | Shape functional invariance in interior regime | Unifying theorem for all scale-free functionals |
| O-7 | Concentration inequality for |delta_M - E[delta_M]| | Tail bound for EITT |
| O-8 | Non-stationary EITT extension with drift velocity | Applicability to trending systems |

## Notation Table (14 Symbols)

| Symbol | Definition |
|--------|-----------|
| S^D | D-part simplex: {x in R^D : x_i > 0, sum x_i = 1} |
| C | Closure operator: C(x) = x / sum x_i |
| clr | Centred log-ratio: clr(x)_i = ln(x_i) - (1/D) sum ln(x_j) |
| ilr | Isometric log-ratio: ilr(x) = Psi^T * clr(x) |
| d_A | Aitchison distance: ||clr(x) - clr(y)||_2 |
| <x,y>_A | Aitchison inner product: (1/D) sum clr(x)_i * clr(y)_i |
| sigma_A^2 | Aitchison variance: (1/D) sum clr_i^2 |
| H | Shannon entropy: -sum x_i ln(x_i) |
| D_M | Block decimation operator (geometric mean blocks) |
| delta_M | EITT residual: percentage entropy deviation |
| x perturb y | Perturbation: C(x_1*y_1, ..., x_D*y_D) |
| alpha odot x | Powering: C(x_1^alpha, ..., x_D^alpha) |
| N_eff | Effective diversity: exp(H(x)) |
| Delta(t) | Perturbation difference between consecutive time steps |

## Canonical Values Registry

### EITT Benchmarks
European prices 341:1: 0.18% | EMBER monthly: 1.02% | NGFS geometric 5yr: 1.8% | NGFS arithmetic 5yr: 14.2% (7.9x worse) | EXP-01 Gold/Silver: 0.60% | EXP-03 QGP: 0.27% | Geochemistry: 37/39 TAS types pass

### PLL Benchmarks
30 domains tested | Confidence threshold: 3^3 = 27 (exceeded by 30) | Highest R^2: 0.998 (room acoustics) | EXP-01 R^2: 0.9007, vertex 1751, Q = 22.18

### Nuclear Constants
Li-7 C/S: 2.525 | sigma_A^2 light: 16.77 | sigma_A^2 iron peak: 2.49 | sigma_A^2 heavy: 1.50 | sigma_A^2 actinide: 1.15 | Coulomb cliff: Z ~ 419 | Absolute instability: Z ~ 363

### Operating Envelope
EITT pass: < 1% | H minimum: > 1.0 | Zero rate max: < 15% | Zero rate hard fail: > 35% | F17 R^2: > 0.96

---

## Claim Classification Summary (22 Claims)

| Level | Count | Key claims |
|-------|-------|-----------|
| L5 Core Science | 3 | EITT entropy invariance, geometric mean superiority, simplex geometry |
| L4 Canonical Method | 5 | Vertex theorem, operating envelope, contamination doctrine, HIVIP, Hessian bound |
| L3 Validated Companion | 2 | MC-4, geochemistry validation |
| L2 Process Control | 3 | F17 tuner, two-pass instrument, energy transition dating |
| L1 Candidate Overlay | 3 | PLL universality, Bell test analogy, nuclear corridor |
| L0 Exploratory | 6 | Noise squeeze, boundary species, H1 operator, quantum isomorphisms, PLL correspondence, stability island |

---

*This document serves as the mathematical content appendix to the HUF Executive Summary. For the full machine-readable registry with all proofs, LaTeX notation, and cross-references, see: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json*

*P. Higgins, 2026. Higgins Unity Framework. Independent Researcher, Markham, Ontario, Canada.*
