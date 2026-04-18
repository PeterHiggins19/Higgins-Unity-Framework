# Energy Transition Dating

## The PLL Parabola Dates the Transition, State by State

**Status:** L1 Candidate Overlay. Demonstrated in EXP-02 across 10 US states.

---

## Statement

The PLL parabola vertex dates the energy transition — the moment when the competing forces (fossil dominance vs renewable growth) are most balanced. Before the vertex, fossil wins. After the vertex, renewables win.

## The Dates

| State | Vertex Year | R^2 | Shape | Interpretation |
|-------|------------|------|-------|----------------|
| California | 2014 | 0.832 | bowl | Solar+wind began to dominate |
| Minnesota | 2037 (extrapolated) | 0.694 | bowl | Still in descent — transition incomplete |
| Texas | within range | 0.571 | bowl | Wind emerging as major force |
| Wisconsin | 1951 (extrapolated) | strong | hill | Coal's peak — declining ever since |
| Pennsylvania | within range | varies | varies | Bridge state — at the crossover |
| West Virginia | flat | 0.008 | none | No transition. Coal won. |
| Wyoming | flat | 0.091 | none | No transition. Coal won. |

## What It Means for Policy

The vertex year is not a prediction — it is a measurement of where the forces balanced. But the curvature tells you the speed: a steep parabola means a fast transition. A shallow one means a slow transition. Minnesota's 2037 vertex means its transition is slower than California's.

States with no parabola (West Virginia, Wyoming) have no energy transition to detect. The method correctly identifies them as compositionally static.

## Evidence

| Document | Location |
|----------|----------|
| EXP-02 Sealed | codawork2026/experiments/EXP-02_US_Monthly/EXP02_SEALED_CONCLUSION.json |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> energy_transition_parabola_dating (L1) |

---

*The transition has a date. The parabola finds it.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T1, C1.3).*

### Formal Basis: Corollary C1.3

The vertex of the PLL parabola sigma_A^2(t) = sigma_A^2(t_0) + a(t - t_0)^2 locates the transition date t_0 where competing compositional forces are most balanced.

For energy mixes on S^D (D = number of energy carriers), the two forces are:

    F_fossil : concentration toward fossil carriers (clr_fossil increasing)
    F_clean  : diversification toward renewable carriers (clr_clean increasing)

At t = t_0, these forces balance: clr(t_0) perpendicular to clr'(t_0) by T1.

### Curvature as Transition Speed

The curvature coefficient 'a' measures transition speed:

    |a| large : fast transition (steep parabola)
    |a| small : slow transition (shallow parabola)
    a not defined : no transition (flat or no parabola)

### Extrapolation Caveat

When the vertex t_0 falls outside the observed data range, it is an extrapolated estimate, not a measurement. The extrapolation assumes the parabolic form continues — which requires the two-force competition to persist. Policy changes, technological disruptions, or new energy sources would alter the trajectory.

### Canonical Energy Transition Dates

| State | t_0 | |a| (curvature) | Status |
|-------|-----|----------------|--------|
| California | 2014 | high | Measured — within data range |
| Minnesota | 2037 | moderate | Extrapolated — transition incomplete |
| Wisconsin | 1951 | moderate | Extrapolated — coal's peak, now declining |
| West Virginia | N/A | 0 | No transition — coal dominates |
| Wyoming | N/A | 0 | No transition — coal dominates |
