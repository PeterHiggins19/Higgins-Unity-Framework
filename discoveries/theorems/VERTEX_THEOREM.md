# The Vertex Theorem

## A Pure Geometric Fact About Compositional Time Series

**Status:** Exact mathematical identity. No approximations. Anyone can verify.

---

## Statement

For a D-part compositional time series x(t) on the simplex S^D, define the Aitchison variance as:

    sigma_A^2(t) = (1/D) * sum_i [ clr_i(t) ]^2

where clr_i(t) = ln(x_i(t)) - (1/D) * sum_j ln(x_j(t)) is the centered log-ratio transform.

**The vertex of sigma_A^2(t) occurs where:**

    d(sigma_A^2)/dt = (2/D) * sum_i [ clr_i(t) * clr_i'(t) ] = 0

**This is equivalent to:**

    clr(t*) is perpendicular to clr'(t*)

That is: at the vertex, the composition vector in Aitchison space is orthogonal to its own rate of change.

## Proof

By the chain rule:

    d/dt [ (1/D) * sum_i clr_i^2 ] = (1/D) * sum_i [ 2 * clr_i * clr_i' ] = (2/D) * <clr, clr'>

Setting this equal to zero gives <clr, clr'> = 0, which is the orthogonality condition.

This is the standard derivative of a sum of squares. No approximations, no assumptions beyond differentiability of the composition trajectory.

## Physical Meaning

At the vertex, the composition restructures (species fractions change, so clr' is nonzero) but compositional stress is momentarily stationary (d(sigma_A^2)/dt = 0). The forces that drive compositional change are acting, but they are balanced in a way that produces no net change in overall stress.

This is **dynamic equilibrium on the simplex**: the system moves, but its distance from the barycenter is momentarily constant.

## The Error Signal

The derivative of sigma_A^2 near the vertex is:

    epsilon(t) = d(sigma_A^2)/dt = 2a(t - t_0)

where a is the curvature of the parabolic fit and t_0 is the vertex time. This is **linear** in (t - t_0), and the coefficient is always **2a** — the ratio of 2 appears from the chain rule, not from any physical model.

The discriminator 2a determines the stability:
- 2a > 0: stable equilibrium (bowl / U-shape) — the system returns when perturbed
- 2a < 0: unstable equilibrium (hill / inverted-U) — the system departs when perturbed

## What the Theorem Does Not Require

This result does not require:
- Any specific physical model
- Temporal ordering (works for any smoothly parameterized simplex walk)
- EITT or entropy invariance
- PLL language or engineering analogies
- Any minimum number of observations
- Any specific number of components D

It is a property of the Aitchison geometry of the simplex. It was always there.

## Verification

Confirmed across 30 independent domains spanning 338 years of commodity prices, 25 years of energy transitions, 3.5 billion years of nuclear decay, stellar nucleosynthesis, room acoustics, wine fermentation, soil ecology, Big Bang nucleosynthesis, and particle physics.

Every domain where two compositional forces compete produces a parabolic sigma_A^2 trajectory. Every parabola's vertex satisfies the orthogonality condition. Every error signal is linear with coefficient 2a.

## Evidence

| Document | Location |
|----------|----------|
| EXP-01 Sealed Conclusion | codawork2026/experiments/EXP-01_Gold_Silver/EXP01_SEALED_CONCLUSION.json |
| EXP-02 Sealed Conclusion | codawork2026/experiments/EXP-02_US_Monthly/EXP02_SEALED_CONCLUSION.json |
| EXP-03 Sealed Conclusion | codawork2026/experiments/EXP-03_Uranium/EXP03_SEALED_CONCLUSION.json |
| 30-domain hunt | Documented in ai-refresh/HUF_FAST_REFRESH.json -> pll_parabola_discovery |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> vertex_theorem (L4) |

## Attribution

P. Higgins, 2026. Discovered during the PLL-EITT investigation, April 2026. The vertex theorem is the mathematical core beneath the PLL parabola discovery — it stands independently of any physical interpretation.

---

*The simplex was always there. The orthogonality was always there. The theorem states what was waiting to be stated.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T1, C1.1, C1.2, C1.3).*

### Formal Notation

| Symbol | LaTeX | Definition |
|--------|-------|------------|
| S^D | \mathcal{S}^D | D-part simplex: S^D = {x in R^D : x_i > 0, sum x_i = 1} |
| clr | \mathrm{clr} | Centred log-ratio: clr(x)_i = ln(x_i) - (1/D) sum_j ln(x_j) |
| sigma_A^2 | \sigma_A^2 | Aitchison variance: sigma_A^2 = (1/D) sum clr_i^2 |
| d_A | d_A | Aitchison distance: d_A(x,y) = ||clr(x) - clr(y)||_2 |
| <x,y>_A | \langle x,y \rangle_A | Aitchison inner product: (1/D) sum clr(x)_i * clr(y)_i |

### Theorem T1 — Full Statement

Let {x(t)} be a D-part compositional time series on S^D with differentiable CLR trajectories. Then:

    sigma_A^2(t) = (1/D) sum_{i=1}^{D} [clr_i(t)]^2

The vertex (extremum) of sigma_A^2 occurs at t = t* where:

    d(sigma_A^2)/dt = (2/D) sum_{i=1}^{D} clr_i(t) * clr_i'(t) = 0

This is equivalent to clr(t*) perpendicular to clr'(t*) in the Aitchison inner product. QED.

### Corollary C1.1 — PLL Error Signal

Near the vertex t_0, sigma_A^2(t) approximates sigma_A^2(t_0) + a(t - t_0)^2 where:

    a = (1/D) sum [(clr_i')^2 + clr_i * clr_i'']    (evaluated at t_0)

The error signal epsilon(t) = d(sigma_A^2)/dt = 2a(t - t_0) is linear near the lock point. The coefficient 2 arises from the chain rule, not from any physical model.

### Corollary C1.2 — Bowl vs Hill Classification

If a > 0 (second derivative positive), sigma_A^2 has a bowl (minimum) — the system is locked (stable equilibrium). If a < 0, sigma_A^2 has a hill (maximum) — the system is relaxing (anti-lock, unstable equilibrium).

### Corollary C1.3 — Vertex Location as Transition Date

When sigma_A^2(t) is parabolic with vertex at t_0, the parameter value t_0 marks the moment of dynamic equilibrium — where competing compositional forces are most balanced. Examples: California energy (2014), Gold/Silver (1751), Wisconsin (1951).

### Relation to Other Theorems

T1 depends only on the chain rule and the definition of sigma_A^2. It does not require T2 (CLR Linearity) or T3 (Hessian Bound). However, when combined with T2, the vertex theorem extends to decimated series: the vertex of sigma_A^2 computed from geometric-mean-averaged blocks satisfies the same orthogonality condition.

### Open Problem O-2

Prove that sigma_A^2(t) is generically parabolic under mild regularity conditions (smooth, slowly-varying forces on the simplex). The vertex theorem proves the orthogonality condition at the extremum; what remains is showing that sigma_A^2 has exactly one extremum when forcing is slow relative to the system timescale. If solved, this would promote PLL universality from L1 to L2.
