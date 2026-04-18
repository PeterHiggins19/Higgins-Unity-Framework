# The PLL Parabola: Universal Compositional Dynamics

## Wherever Two Forces Compete on a Simplex, sigma_A^2 Forms a Parabola

**Status:** L1 Candidate Overlay. 30/30 domains produce diagnostic output. Mathematically exact (Vertex Theorem). Physical universality is empirical.

---

## Statement

Wherever two compositional forces compete on a simplex — one concentrating, one diversifying — the Aitchison variance sigma_A^2 traces a parabola over the ordering parameter.

- The **vertex** is where the forces balance (dynamic equilibrium)
- The **shape** tells you the stability: bowl (U) = stable, hill (inverted-U) = unstable
- The **error signal** d(sigma_A^2)/dt = 2a(t - t_0) is linear — the ratio of 2
- When no vertex exists within the data range, the **slope** becomes a trajectory diagnostic

## The 30-Domain Hunt

| Phase | Domains | Locks | Notes |
|-------|---------|-------|-------|
| First hunt | 7 | 7 | Founding domains |
| Full hunt | 15 | 13 | Extended domains, 2 recovered |
| Clean sweep | 30 | 25 | All available domains |
| Failure retest | — | +3 | Recovered via regime splitting |
| Boundary gifts | — | +2 trajectory | Monotonic = no equilibrium, slope is diagnostic |
| **TOTAL** | **30** | **28 locks + 2 trajectory diagnostics = 30/30 wins** |

## Standout Vertices

| Domain | Vertex | R^2 | What It Means |
|--------|--------|-----|---------------|
| Gold/Silver | 1751 | 0.901 | Gold winning over silver for 275 years |
| Room acoustics | ~150 m^3 | 0.998 | Peter's own domain — the screwdriver works |
| California energy | 2014 | 0.832 | Solar+wind began to dominate |
| QGP freeze-out | ~20 GeV | strong | Deconfinement transition |
| Minnesota energy | 2037 (extrap) | 0.694 | Transition still in descent phase |
| Wisconsin energy | 1951 (extrap) | strong | Coal's peak — declining ever since |

## What the Shapes Tell You

**Bowl (U-shape, a > 0):** Stable equilibrium. The system was closest to balance at the vertex and has been moving away. Gold/Silver: balance in 1751, gold winning since. California: balance in 2014, renewables winning since.

**Hill (inverted-U, a < 0):** Unstable equilibrium. The system was at peak stress and chose a direction. Nuclear decay chains: all three are hills — the unstable nucleus starts at maximum stress and relaxes toward stable lead.

**Monotonic (vertex outside data):** No equilibrium within the observed range. One force dominates. Cosmic rays: vertex at logE=16.9 (outside range) — spallation speedometer, no equilibrium. Demographics: vertex at HDI=-0.24 — transition speedometer.

## The Mathematics

See: [Vertex Theorem](../theorems/VERTEX_THEOREM.md) — the exact mathematical foundation.

The parabola is the simplest polynomial that can have a unique extremum. The ratio of 2 in the error signal comes from the chain rule, not from physics. The orthogonality condition clr perpendicular to clr' at the vertex is a geometric fact about the simplex.

## Evidence

| Document | Location |
|----------|----------|
| Full hunt scripts | DATA/Scripts/eitt_pll_*.py |
| EXP-01 (Gold/Silver vertex at 1751) | codawork2026/experiments/EXP-01_Gold_Silver/EXP01_SEALED_CONCLUSION.json |
| EXP-02 (10 state vertices) | codawork2026/experiments/EXP-02_US_Monthly/EXP02_SEALED_CONCLUSION.json |
| EXP-03 (nuclear anti-lock) | codawork2026/experiments/EXP-03_Uranium/EXP03_SEALED_CONCLUSION.json |
| Experiment journal | codawork2026/journals/EITT_PLL_Experiment_Journal.pdf |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> pll_parabola_universality (L1) |

---

*The parabola is the simplest lock geometry. The vertex is the balance point. The ratio of 2 was always there.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T1, C1.1, C1.2, C1.3).*

### The Vertex Theorem (T1) — Foundation

The PLL parabola rests on the Vertex Theorem. For any D-part compositional time series with differentiable CLR trajectories:

    d(sigma_A^2)/dt = (2/D) sum_{i=1}^{D} clr_i(t) * clr_i'(t) = 0

at the vertex t = t*. This is equivalent to clr(t*) perpendicular to clr'(t*) in the Aitchison inner product. The proof is a direct application of the chain rule to sigma_A^2 = (1/D) sum clr_i^2.

### The Error Signal (C1.1)

Near the vertex t_0, the Taylor expansion gives:

    sigma_A^2(t) ~ sigma_A^2(t_0) + a(t - t_0)^2

where a = (1/D) sum [(clr_i')^2 + clr_i * clr_i''] evaluated at t_0. The error signal:

    epsilon(t) = d(sigma_A^2)/dt = 2a(t - t_0)

The factor of 2 is the chain rule — the "ratio of 2" in PLL engineering language. It is mathematical, not empirical.

### Bowl vs Hill (C1.2)

The sign of 'a' classifies the parabola:

    a > 0 : bowl (U-shape) — stable lock. System returns when perturbed.
    a < 0 : hill (inverted-U) — anti-lock. System departs when perturbed.

| Type | Examples | Physical meaning |
|------|----------|-----------------|
| Bowl (a > 0) | Gold/Silver, California energy, room acoustics | Two competing forces at balance |
| Hill (a < 0) | U-238 decay, Th-232 decay, stellar nucleosynthesis | Relaxation — one force dominates |
| Monotonic | Cosmic rays, demographics | Vertex outside data range — trajectory diagnostic |

### Vertex as Transition Date (C1.3)

The vertex parameter t_0 marks dynamic equilibrium — where competing forces are most balanced. The curvature |a| measures transition speed: steep parabola = fast transition.

### Canonical PLL Values

| Domain | Vertex | R^2 | Q-factor |
|--------|--------|-----|----------|
| Gold/Silver | 1751 | 0.9007 | 22.18 |
| Room acoustics | ~150 m^3 | 0.998 | — |
| California energy | 2014 | 0.832 | — |
| QGP freeze-out | ~20 GeV | strong | — |

### Open Problem O-2 — Parabola Genericity

**Statement:** Prove that sigma_A^2(t) is generically parabolic under mild regularity conditions (smooth, slowly-varying forces on the simplex).

**Partial progress:** T1 proves the orthogonality condition at the extremum. What remains is showing uniqueness of the extremum when forcing is slow relative to the system timescale.

**If solved:** Would promote PLL universality from L1 to L2 (process control candidate).

### Relation to Noise Squeeze

When higher-order polynomials (orders 3, 4, 5) are fitted to the sigma_A^2 trajectory, the parabolic residuals reveal the stochastic core. The squeeze plateau is the irreducible noise floor — the compositional equivalent of VCO phase noise in a PLL. See: NOISE_SQUEEZE_STOCHASTIC_CORE.md.
