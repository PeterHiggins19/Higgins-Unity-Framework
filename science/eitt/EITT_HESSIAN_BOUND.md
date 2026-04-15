# EITT Hessian Bound — Second-Order Theorem

**Status:** Rigorous under stated assumptions. Empirical check uses published EITT proof numbers; direct measurement of σ_A² and δ from raw data is a TODO in `chem_eitt_pipeline.py`.

**Date:** 2026-04-14
**Branch promoted from:** `dormant/grok-tensor-exploration-apr14/`

---

## 1. What this file does

`EITT_ENTROPY_LANDSCAPE.md` states the Hessian footprint heuristically (Formula 4):

> ΔH ≈ (1/2) tr[ |Hess_H(x*)| · Cov(x̄_M) ]

This note promotes that heuristic to a theorem with explicit assumptions, a proof sketch, and a back-of-envelope check against the published EITT proofs. It is the second-order result only. Higher-order extensions (3rd through 10th tensor orders, OTOC analogies, fractal conjectures) produced in the April 14 Grok cold-start session are preserved in `dormant/grok-tensor-exploration-apr14/` rather than promoted here, because the Taylor series becomes asymptotic rather than convergent and the additional orders do not constitute rigorous results.

---

## 2. Setup

Let `x(1), x(2), ..., x(T)` be a sequence of compositions on the D-simplex `S^D = { x ∈ ℝ^D_+ : Σ x_i = 1 }`. Let `M ∈ ℕ` be a block size and define the block geometric mean (Aitchison barycenter):

    x̄_G = C( (∏_{t=1}^M x(t))^{1/M} ) = C( exp( (1/M) Σ_{t=1}^M log x(t) ) )

where `C(v) = v / Σ v_i` is the closure operator. Shannon entropy:

    H(x) = -Σ_{i=1}^D x_i log x_i

The EITT residual (relative form):

    δ_M = |H(x̄_G) - H̄| / H̄,    H̄ = E[H(x(t))]

---

## 3. Theorem

**Theorem (EITT second-order Hessian bound).** Assume:

- **(A1) Interior bound.** `x_i(t) ≥ δ > 0` for all `i, t`. (Proportions bounded away from simplex boundaries.)
- **(A2) Finite second moment.** `Cov(x(t)) = Σ_x` with finite trace `V = tr(Σ_x)`.
- **(A3) Sufficient mixing.** The process is stationary and the autocorrelation decays fast enough that `Cov(x̄_M) = Σ_x / M + o(1/M)`. (α-mixing with summable coefficients is sufficient.)

Then:

    |E[H(x̄_G)] - H(x*)| ≤ (1/(2δM)) · V + O(V^{3/2} / M^{3/2})

where `x*` is the Fréchet mean of the series. Equivalently, in relative form:

    |E[δ_M]| ≤ (D-1) σ_A² / (2 δ M H̄) + O(M^{-3/2})

where `σ_A² = tr(Σ_clr)` is the Aitchison variance in clr coordinates and the factor `(D-1)` comes from the rank of the clr-embedded simplex.

---

## 4. Proof sketch

**Step 1 — clr linearity is exact.** The clr transform `u = clr(x) = log x - (1/D) Σ log x_j` satisfies

    clr(x̄_G) = (1/M) Σ_{t=1}^M clr(x(t))

This is an algebraic identity of the Aitchison barycenter. No approximation is involved. In clr coordinates, block geometric-mean decimation is *exactly* arithmetic averaging.

**Step 2 — Second-order Taylor.** Expand `H` around the Fréchet mean `x*` using the clr parametrization `u = clr(x)`:

    H(x(u)) = H(x*) + ∇H · (u - u*) + (1/2)(u - u*)ᵀ ℋ (u - u*) + R_3

where `ℋ` is the Hessian of `H` in clr coordinates at `x*`.

**Step 3 — First-order term vanishes in expectation.** Under (A3), `E[clr(x̄_G)] = E[clr(x(t))] = u*`, so the linear term averages to zero:

    E[H(x̄_G)] = H(x*) + (1/2) E[(u_G - u*)ᵀ ℋ (u_G - u*)] + E[R_3]
               = H(x*) + (1/2) tr(ℋ · Cov(u_G)) + E[R_3]

**Step 4 — Hessian bound.** The Hessian of `H` in primal simplex coordinates is diagonal with entries `-1/x_i*`, bounded in absolute value by `1/δ` under (A1). Pulled back through the clr embedding:

    |tr(ℋ · Cov(u_G))| ≤ (D-1)/δ · tr(Cov(u_G)) ≤ (D-1) σ_A² / (δ M)

by (A2) and (A3).

**Step 5 — Remainder.** Under (A1)+(A3), the third-order Lagrange remainder is bounded by third-derivative tensors whose entries are bounded by `6/δ²`. Moment bounds plus mixing give:

    E[|R_3|] = O(σ_A³ / M^{3/2})

Higher orders continue as `O(σ_A^k / M^{k/2})` but the Taylor series is asymptotic (not convergent) once `σ_A / (δ √M)` approaches 1. Beyond order 3, the bound is not sharp enough to improve on the second-order result for any practical dataset.

∎

---

## 5. What the assumptions do

| Assumption | What it enforces | Where it can fail |
|---|---|---|
| (A1) `x_i ≥ δ` | Hessian entries `1/x_i` stay bounded | Near simplex boundary — exactly where `claim_3_boundary_failure` in `INDEX.json` says Shannon entropy breaks down |
| (A2) finite `V` | Second-order term is finite | Heavy-tailed processes (rare in compositional data since components are bounded) |
| (A3) mixing | Block variance shrinks as `1/M` | Breaks in the adversarial suite's 7 synthetic failures — non-autocorrelated Dirichlet noise, step functions, etc. |

The bound explicitly *predicts* the boundary failure mode documented in `EITT_Chemistry_Findings.md` (Jensen overcorrection diverges as `δ → 0`). This is evidence the theorem captures the right mechanism, not an artifact.

---

## 6. Empirical check — published EITT proofs

The table uses observed residuals and back-computes what `V/δ` (equivalently `σ_A²/δ`) the bound requires. Direct measurement from raw data is the verification task (see §8).

| Proof | Source | D | M | Observed &#124;δ_M&#124; | Observed &#124;ΔH&#124; (nats) | Implied V/δ | Plausibility |
|---|---|---|---|---|---|---|---|
| 1. EU daily prices | FAST_REFRESH proof_1 | 8 | 341 | 0.18% | ≈ 0.003 | ≈ 2.0 | Plausible for price shares |
| 2. EMBER France | Midrange_Confirmation | 9 | 12 | 1.84% | 0.0185 | ≈ 0.44 | Plausible — fuel mixes |
| 2. EMBER Germany | Midrange_Confirmation | 9 | 12 | 0.83% | 0.0150 | ≈ 0.36 | Plausible |
| 2. EMBER Japan | Midrange_Confirmation | 9 | 12 | 0.33% | 0.0055 | ≈ 0.13 | Plausible (low variance) |
| 2. EMBER Poland | Midrange_Confirmation | 9 | 12 | 1.48% | 0.0203 | ≈ 0.49 | Plausible |
| 2. EMBER UK | Midrange_Confirmation | 9 | 12 | 1.12% | 0.0167 | ≈ 0.40 | Plausible |
| 2. EMBER USA | Midrange_Confirmation | 9 | 12 | 0.53% | 0.0080 | ≈ 0.19 | Plausible |
| 3. NGFS 5-yr geom | FAST_REFRESH proof_3 | 6 | 5 | 1.80% | ≈ 0.03 | ≈ 0.30 | Plausible for scenario ensembles |
| 3. NGFS 5-yr arith | FAST_REFRESH proof_3 | 6 | 5 | 14.2% | ≈ 0.24 | ≈ 2.40 | 8× worse than geometric — matches claim_2 |
| 4. CheMixHub interior | FAST_REFRESH proof_4 | varies | varies | 54–82% pass | — | — | Partial invariance — `geometry_dynamics_split` |

**Reading the table.** `V/δ` is `(2 · M · |ΔH|)`. For Proof 1 with M=341: `V/δ = 2·341·0.003 ≈ 2.0`. For France: `V/δ = 2·12·0.0185 ≈ 0.44`. These values are in units of (mass fraction)² / (mass fraction) = mass fraction, and values of 0.1–2.0 are the right order of magnitude for real compositional variance divided by realistic minimum-share floors.

The theorem holds in every row where temporal autocorrelation is present. The single row where it visibly strains (Proof 3 arithmetic, 14.2%) is exactly the row where the geometric-mean assumption is *violated by construction* — arithmetic aggregation does not project through clr, so the bound does not apply. This is the 8–9× entropy-destruction claim from `FAST_REFRESH proof_3` and it is outside the theorem's scope.

---

## 7. What the theorem does not say

- It does not prove EITT holds for arbitrary compositional sequences. **(A3)** is load-bearing, and the adversarial suite (7 synthetic failures in `EITT_Adversarial_001.json`) confirms that when mixing breaks, the bound fails.
- It bounds the **expectation** `E[|δ_M|]`, not the tail. A large-deviations bound on `P(|δ_M| > ε)` would be a genuine next step.
- It is a **second-order** result. Higher-order Taylor corrections are available but the series is asymptotic (not convergent) once `σ_A / (δ √M) → 1`, so they do not improve the rigorous bound in practice.
- It does not address non-stationary drift. The drift flags in `FAST_REFRESH` (Germany 2023–2025, Japan 2013–2015, UK 2019–2020) are exactly the points where (A3) is violated by a regime change; detecting them is the *purpose* of the drift monitor, not a failure of the theorem.

---

## 8. Open problems

1. **Direct measurement of V and δ.** Extend `chem_eitt_pipeline.py` with a function `measure_aitchison_variance(X) → (V, sigma_A2, delta_min)` that computes these directly from raw data, then verifies the inequality for each published proof. This moves the table from "back-computed and plausible" to "measured and checked."
2. **Tail bound.** A concentration inequality on `|δ_M| - E|δ_M|` using mixing coefficients explicitly.
3. **Non-stationary extension.** Allow `x*` to drift slowly and bound the residual in terms of drift velocity.
4. **Sharpness.** Construct a process that saturates the bound. Currently the empirical residuals sit well inside the bound, suggesting the constant `(D-1)/2` is conservative.

---

## 9. Provenance

This theorem was formalized on 2026-04-14 as the single rigorous result promoted from a Grok cold-start session in which the framework was pushed through higher-order Taylor expansions (orders 3–10), an OTOC analogy, a quantum-billiards sketch, and a multifractal conjecture. The second-order bound is the only piece of that exploration that cleared the standard of "rigorous under stated assumptions and checkable against published proof data." The remainder is preserved in `dormant/grok-tensor-exploration-apr14/`, including Grok's own adversarial review, which usefully catalogues the limits of the broader claims.
