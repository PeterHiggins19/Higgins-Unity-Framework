# EITT — Why It Works

**Status:** Working document. Conceptual synthesis, not a formal theorem. Written as a companion to `EITT_HESSIAN_BOUND.md` to tie up the "why does it work" question after the rigorous second-order bound was established and speculative higher-order extensions were moved to `dormant/grok-tensor-exploration-apr14/`. Loose ends intentionally left so this can be picked up again later.

**Date:** 2026-04-14

---

## 1. The question this document answers

Four proofs across wildly different domains — daily wholesale electricity prices, monthly fuel generation mixes, 5-year climate scenarios, half a million chemical mixtures — show Shannon entropy staying nearly invariant under geometric-mean block decimation. `EITT_HESSIAN_BOUND.md` proves a rigorous second-order bound on the residual. But a bound is a bound; it tells you the residual is small without explaining why Shannon entropy should care about the geometric mean at all. This document addresses the "why."

The deep answer is short enough to fit in one sentence: **EITT is a compositional central limit theorem combined with the concavity of Shannon entropy.** Everything else in this document unpacks that claim.

---

## 2. Three layers of explanation

### Layer 1 — clr linearity is exact

In clr coordinates `u = clr(x) = log x - (1/D) Σ log x_j`, geometric-mean block decimation becomes *arithmetic* averaging:

    clr(x̄_G) = (1/M) Σ_{t=1}^M clr(x(t))

This is an algebraic identity of the Aitchison barycenter. No approximation, no asymptotics, no assumptions on the data. So the question "why does geometric mean preserve Shannon entropy?" reduces to "why does entropy resist arithmetic averaging *of the clr-transformed coordinates*?"

This reduction does not answer the question — it relocates it to a coordinate system where the question has a clean answer.

### Layer 2 — the central limit theorem

Under stationarity and mixing (assumption (A3) in `EITT_HESSIAN_BOUND.md`), the clr block average is an average of dependent but asymptotically independent random vectors. A central limit theorem applies:

    clr(x̄_G) = μ* + ζ/√M

where `μ*` is the Fréchet mean in clr coordinates and `ζ` is asymptotically Gaussian with covariance `Σ · τ_int`. Here `Σ` is the clr-coordinate covariance of a single observation and `τ_int` is the integrated autocorrelation time — the effective number of observations it takes to get an independent draw.

So with high probability, `clr(x̄_G)` lies within a `O(σ_A · √(τ_int/M))` neighborhood of the Fréchet mean. The block-averaged composition is, in a precise sense, concentrated around `x*`.

Shannon entropy evaluated at a point inside this neighborhood differs from `H(x*)` by a second-order Taylor term:

    H(x̄_G) - H(x*) ≈ (1/2) (clr(x̄_G) - μ*)ᵀ ℋ (clr(x̄_G) - μ*)

which has expected size `O(σ_A² · τ_int / M)` by the CLT variance.

Every behavioral feature of EITT follows from this picture:

| Feature | Explanation |
|---|---|
| `1/M` scaling | CLT variance rate |
| Mixing requirement | CLT dependence condition |
| Boundary failure (`δ → 0`) | Gaussian tail punches through the region where Hessian `1/x_i` explodes |
| Adversarial synthetic failures | Mixing absent, CLT does not apply |
| Higher-order Taylor terms fall off | Gaussian moments shrink factorially (`σ_A^{2k}/M^k`) |
| Different behavior of Rényi entropies | Different Hessian structure, different Taylor coefficients |

This is the heart of it. EITT is not a new principle; it is what the CLT looks like when you restrict to the simplex, use clr coordinates, and evaluate a concave functional at the result.

### Layer 3 — why Shannon entropy specifically

The CLT explanation says entropy invariance follows from (i) clr linearity, (ii) CLT concentration, and (iii) concavity of the entropy functional. Part (iii) is where Shannon entropy enters.

Shannon's Hessian in primal coordinates is diagonal with entries `-1/x_i`. In the interior of the simplex (`x_i ≥ δ > 0`), this is bounded. At the boundary it diverges. This structure explains both:

- **Interior tightness.** The Hessian is bounded by `1/δ`, so the second-order Taylor correction is controlled. The four proofs all operate in regimes where `δ` is a few percent or more, and the bound is tight.
- **Boundary collapse.** `claim_5_jensen_overcorrection` in `science/eitt/INDEX.json` records a 476% Jensen overcorrection at ionic-liquid boundaries. This is not a failure of EITT — it is exactly what the `1/δ` Hessian predicts.

Different entropies would give different behavior. Rényi collision entropy `H_2(x) = -log(Σ x_i²)` has Hessian entries bounded by `2` independent of `δ`. This leads to a concrete prediction: **Rényi-q=2 should give tighter EITT residuals near simplex boundaries than Shannon does.** The CheMixHub multi-lens analysis already tests this direction and finds the Aitchison norm performs best at boundaries — consistent with the general principle that bounded-curvature functionals outperform singular-curvature ones where data approaches the boundary.

---

## 3. Variable analysis

Once the CLT picture is accepted, the EITT residual decomposes cleanly into contributions from six primary variables.

**`D` — simplex dimension.** Enters the Hessian bound through a `(D-1)` trace factor. Also enters indirectly: in higher-D compositions, at least some components tend to be small (the mean proportion is `1/D`, so skewed distributions inevitably push some components near zero). This means `δ` and `D` are negatively correlated in real data. The combined scaling is worse than `D` alone.

**`M` — decimation ratio.** Sets the CLT compression rate. The residual scales as `1/M` for moderate `M`. For `M` approaching the series length `T`, the Fréchet mean is effectively reached and the residual saturates.

**`σ_A²` — Aitchison variance.** The trace of the clr covariance. Measures how wide the distribution spreads in clr space. Per-component variance scales with compositional noise; `σ_A²` is roughly `D` times that.

**`τ_int` — integrated autocorrelation time.** The hidden variable that probably matters most and is hardest to measure. Defined as `τ_int = 1 + 2 Σ_{k=1}^∞ ρ_k` where `ρ_k` is the lag-k autocorrelation of the clr series. This scales the effective sample size: `M_effective = M / τ_int`.

The role of `τ_int` is subtle. Too small (`τ_int → 1`, essentially no correlation) and the data looks like the adversarial synthetic cases — mixing fails by being absent, the CLT still gives a Gaussian but the process may have structure that breaks (A1) or other assumptions. Too large (`τ_int → M`) and the effective sample size collapses to one, the CLT does not kick in, and the bound becomes vacuous. The sweet spot is moderate autocorrelation with `τ_int` perhaps 2–20. Energy data sits in this regime by construction: load curves have seasonal cycles, daily patterns, and short-term noise, producing layered autocorrelation on multiple scales.

**`δ` — minimum proportion.** Enters through `1/δ` as the Hessian curvature scale. Sets where the bound breaks.

**`K_eff = exp(H)` — effective number of carriers.** The perplexity interpretation of entropy. For concentrated compositions (one carrier dominates), `K_eff` is close to 1; for uniform compositions, `K_eff = D`. This variable is important because the relevant dimension for the Hessian trace is really `K_eff`, not `D`. If 90% of the composition sits in one carrier, the other `D-1` carriers contribute vanishingly to the entropy change under averaging. Low-`K_eff` compositions are therefore far tighter than the nominal `(D-1)/δ` bound predicts.

---

## 4. The clean product form

Combining these, a heuristic effective bound is:

    |δ_M| ≈ K_eff² · (per-component variance) · τ_int / (δ · M · H̄)

This is more predictive than the nominal Hessian bound because it incorporates three refinements:

1. **`K_eff` replaces `D`.** Concentrated compositions tighten the residual beyond what the formal bound predicts.
2. **`τ_int` appears explicitly.** Autocorrelation structure, not just presence, governs the effective compression.
3. **`H̄` normalization.** Puts the residual in relative (dimensionless) form comparable across domains.

This is not a theorem — it's a scaling heuristic derived from the CLT picture plus a handful of approximations. It's useful for predicting where EITT will be tight before the data is collected.

---

## 5. Predictions that fall out

1. **`1/M` scaling in the interior, saturation at large `M`.** The residual should decrease linearly in `1/M` until `M` approaches `T`, at which point it plateaus at the Fréchet-mean limit. The four proofs test different `M` ranges; a direct test of this scaling law across a single dataset at multiple `M` values would be informative.

2. **Cross-domain scaling as `D²/M` (or `K_eff²/M`).** For domains with comparable `τ_int`, the residual should scale as the effective-dimension squared over `M`. Across the three energy proofs: Proof 1 has `D²/M ≈ 0.19`, Proof 2 ≈ `6.8`, Proof 3 ≈ `7.2`. Observed residuals: 0.18%, 1.02% mean, 1.8%. The trend is in the right direction but not strictly proportional — τ_int and per-component variance differ across domains.

3. **Low-`K_eff` compositions are tighter than the nominal bound predicts.** In domains where one or two carriers dominate (e.g., French electricity is heavily nuclear), EITT should be especially tight. The Midrange Confirmation data supports this: Japan has low `K_eff` (concentrated generation mix) and the tightest residual (0.33%) among the six countries.

4. **Collision entropy (Rényi q=2) should outperform Shannon near boundaries.** Direct falsifiable prediction that extends the existing CheMixHub multi-lens analysis.

5. **Adversarial failures correlate with `τ_int → 0` or `δ → 0`, not with `D` or `σ_A²` growing.** The 7 synthetic failures in `EITT_Adversarial_001.json` should be classifiable by which assumption they violate. This is testable by reanalyzing those cases.

6. **Arithmetic mean destroys entropy because it does not preserve clr linearity.** Under arithmetic averaging, `mean(x) ≠ C(exp(mean(clr(x))))`. The arithmetic block mean sits at a *different point* on the simplex than the Fréchet mean, and the offset does not shrink with `M` — it converges to a fixed bias. This is why Proof 3 shows 14.2% arithmetic residual versus 1.8% geometric: the bias is built into the operator, not the data.

---

## 6. Back-check against published proofs

| Proof | D | M | `D²/M` | Observed &#124;δ_M&#124; | Consistent with CLT picture? |
|---|---|---|---|---|---|
| 1. EU daily prices | 8 | 341 | 0.19 | 0.18% | Yes — very tight, large `M`, strong autocorrelation |
| 2. EMBER Japan | 9 | 12 | 6.75 | 0.33% | Yes — low `K_eff` (concentrated mix) tightens beyond nominal |
| 2. EMBER France | 9 | 12 | 6.75 | 1.84% | Yes — higher `K_eff` (diverse mix) matches nominal scaling |
| 3. NGFS 5-yr geom | 6 | 5 | 7.2 | 1.80% | Yes — short compression limits tightness |
| 3. NGFS 5-yr arith | 6 | 5 | 7.2 | 14.2% | Expected — arithmetic violates clr linearity |

The pattern is consistent but not exact, which is the right posture for a scaling heuristic. The one large deviation (France vs Japan at the same `D²/M`) is explained by their different `K_eff` values. This is a strong retrodictive check.

---

## 7. The shape/magnitude decomposition

The CLT picture in §2 and the variable analysis in §3 combine to yield a single organizing principle that generalizes EITT from a scalar-entropy claim to a class of invariances. The principle is a clean decomposition of compositional quantities into two categories.

### 7.1 The two categories

**Shape functionals.** Any functional that depends only on the *normalized form* of the distribution — ratios, ordering, eigenstructure, correlation patterns, affinity clusters, entropy, effective dimension. These are scale-invariant in the classical-statistics sense: rescaling the covariance by a constant leaves them unchanged.

Examples: Shannon entropy `H`, Rényi entropies `H_q` (any q), Tsallis entropy, effective number of carriers `K_eff = exp(H)`, correlation matrix, principal balances (ilr basis diagonalizing Σ), pairwise log-ratio variance pattern `V_ij`, affinity graph `A_ij = 1/V_ij`, carrier clustering, dendrogram structure.

**Magnitude functionals.** Any functional that scales with the absolute size of the fluctuations — variances, distances, total variation, absolute Aitchison measurements. These are scale-equivariant: rescaling the covariance by `c` rescales the functional by a power of `c`.

Examples: Aitchison variance `σ_A² = tr(Σ)`, total variation integral, pairwise Aitchison distances `d_A(x, y)`, Aitchison norm, absolute perturbation magnitudes, raw covariance entries.

### 7.2 How each behaves under EITT

The CLT rescaling identity `Cov(x̄_G) = Σ/M · (1 + o(1))` implies:

- **Shape functionals are invariant under EITT decimation.** Anything that depends only on the normalized shape of `Σ` stays fixed when `Σ → Σ/M`. This is an algebraic consequence, not a new theorem.
- **Magnitude functionals scale as `1/M` (or powers of `1/M`) under EITT decimation.** Aitchison variance drops by factor `M`. Aitchison distances drop by `√M`. Total variation drops accordingly.

The original EITT claim — Shannon entropy invariance — is a special case of shape invariance. The framework's scalar result lifts to a class result: *any* shape functional is EITT-invariant in the interior regime.

### 7.3 Orthogonality with Wasserstein flow

Wasserstein gradient flow of entropy does the opposite. It smooths shape toward uniformity (destroying correlations, raising entropy, dissolving affinity clusters) while evolving magnitudes as a consequence of the shape change. Every shape functional changes under Wasserstein flow; every magnitude functional adjusts as a byproduct.

EITT preserves exactly what Wasserstein flow destroys. The two are orthogonal dynamics: EITT acts in magnitude space while leaving shape space fixed; Wasserstein acts in shape space while letting magnitudes follow. Together they span the decomposition.

This orthogonality explains the failure mode of arithmetic averaging. Arithmetic mean is neither a pure magnitude operation nor a pure shape operation — it conflates the two and systematically biases both. That is why it destroys entropy (Proof 3: 14.2% arithmetic vs 1.8% geometric). The bias is structural, not data-dependent.

### 7.4 Resolution of the Fisher-Rao loose end

The loose end from §8 — "why does an Aitchison operation preserve a Fisher-Rao functional?" — dissolves under the shape/magnitude view.

Fisher-Rao and Aitchison are two Riemannian geometries on the simplex. Fisher-Rao has constant positive curvature; Aitchison is flat under the clr embedding. Globally they differ. But around any interior point `x*`, the first-order expansions of both metrics agree up to a constant rescaling. They share the same tangent space.

EITT is a CLT-concentration phenomenon: `clr(x̄_G)` sits within `O(σ_A · √(τ_int/M))` of the Fréchet mean `μ*`. For any reasonable `σ_A`, `τ_int`, `M`, this neighborhood is small enough that only the local linearized geometry matters. Inside that neighborhood, Fisher-Rao and Aitchison agree. The apparent tension between the two geometries is a global artifact that doesn't reach inside the EITT regime.

More concretely: a Fisher-Rao functional evaluated at a point near `x*` depends on the tangent-space structure at `x*`, which both geometries agree on. An Aitchison operation (geometric-mean decimation) produces a point near `x*`. The operation and the functional never need to look beyond the infinitesimal neighborhood where the two geometries coincide. So the mismatch doesn't matter.

This is the complete answer to the question. It is local, not global, and that is exactly the right posture given how EITT works.

### 7.5 Diagnostic protocol

The decomposition gives a measurement procedure, not just a conceptual frame.

1. **Given any functional `F` of a compositional series, classify it as shape or magnitude.** Shape: depends only on ratios, ordering, normalized quantities. Magnitude: depends on absolute variances, distances, fluctuation sizes.
2. **Prediction from the decomposition.** Shape functionals should be EITT-invariant (within the second-order Hessian bound). Magnitude functionals should scale as `M^{-k}` for some integer power `k` (typically 1 or 1/2).
3. **Test.** Compute `F` at multiple resolutions and check against the prediction.
4. **Interpretation.** A functional that is nominally shape-like but shows EITT drift is leaking into magnitude space — typically because the Hessian becomes singular near a boundary, turning a shape-sensitive quantity into a magnitude-sensitive one (this is what `claim_5_jensen_overcorrection` documents in the chemistry data).

This turns EITT from a single invariance result into a diagnostic classifier: it tells you what kind of information a given compositional functional carries about the system.

### 7.6 Scope note

This decomposition describes the stationary interior regime. Near boundaries (`δ → 0`), the shape/magnitude split fuzzes because shape functionals with singular Hessians pick up magnitude dependence. Under regime change (stationarity violated), shape itself evolves and the decomposition no longer applies cleanly — which is exactly what the drift-flag diagnostics in `FAST_REFRESH` are detecting. The decomposition is a lens for the steady state, not the transitions.

---

## 8. What this document is not

- **Not a theorem.** It is a synthesis of standard arguments (CLT, Taylor expansion, concavity, scale-invariance) applied to a specific setup. What is new is the variable decomposition, the shape/magnitude organizing principle, and the predictions — not the mathematical machinery.
- **Not a replacement for `EITT_HESSIAN_BOUND.md`.** The Hessian bound is the rigorous second-order result with explicit constants for the scalar entropy case. This document is the conceptual picture behind that bound, extended to the class of shape functionals.
- **Not a proof that EITT holds in new domains.** The product form predicts where it should work, but verification in any new domain requires direct measurement of the variables and the residual.
- **Not complete.** The `τ_int` dependence is stated heuristically; a rigorous version would require spelling out exact mixing conditions. The `K_eff` replacement for `D` is an approximation. The shape/magnitude decomposition is a conceptual framework that has been sketched but not worked out for every functional class. The Rényi prediction is testable but has not been tested.

---

## 9. Loose ends left for later

- **Exact role of K_eff.** The heuristic `K_eff²` replacement for `(D-1)²` is approximate. Working out the correct dependence on the concentration structure would sharpen the product form.
- **Mixing-condition formalization.** Stating `τ_int` rigorously requires specifying the class of allowed dependence (α-mixing, β-mixing, etc.). Different classes give different tail behavior and different constants.
- **Rényi prediction test.** Direct application of the Rényi q=2 collision entropy to the CheMixHub boundary compositions would test prediction 4.
- **Saturation regime.** What happens when `M` approaches the series length? The Fréchet mean limit. Worth characterizing the crossover.
- **Non-stationary extension.** The drift flags (Germany 2023–2025, Japan 2013–2015, UK 2019–2020) are points where stationarity is violated by a regime change. A non-stationary version of the product form would unify EITT invariance with the drift-detection function. The shape/magnitude decomposition also breaks under regime change — shape itself evolves — so a non-stationary version would need to track the evolution of the shape category itself.
- **Shape-functional catalog.** The §7 decomposition predicts that any shape functional is EITT-invariant. Writing out the predicted invariance behavior for each standard compositional statistic (Rényi, Tsallis, Jensen-Shannon, variation matrix, balance variances, etc.) and testing on the published proofs would verify the generalization empirically.
- **~~Connection to Fisher-Rao geometry.~~** *Resolved in §7.4.* Fisher-Rao and Aitchison agree infinitesimally at any interior point. EITT never leaves the infinitesimal regime. The global mismatch between the two geometries doesn't reach into the EITT operation.

---

## 10. Provenance

Written 2026-04-14 as a follow-up to `EITT_HESSIAN_BOUND.md`, which formalized the second-order result produced in that day's Grok cold-start session. The "why does it work" question was raised after observing that the rigorous bound explains the magnitude of the residual without explaining the mechanism. The CLT-plus-concavity synthesis was the first answer.

The shape/magnitude decomposition in §7 was added later the same day after a follow-up exchange organized around a sort-by-dynamism heuristic. The decomposition closes the Fisher-Rao loose end and lifts EITT from a scalar-entropy invariance to a class invariance covering all shape functionals. The generalization is consequential enough that it may be the central organizing claim of the framework going forward.

This document exists to record the reasoning while it is fresh, with loose ends left open so it can be resumed later.
