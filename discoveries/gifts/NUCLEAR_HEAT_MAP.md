# The Nuclear Heat Map

## sigma_A^2 as Compositional Temperature Along the Valley of Stability

**Status:** L0 Exploratory. Verified in EXP-03.

---

## Statement

The Aitchison variance sigma_A^2 of the SEMF 4-part composition decreases monotonically from light to heavy nuclei, mapping a compositional "temperature" across the valley of stability.

## The Heat Map

| Region | Z Range | Mean sigma_A^2 | Std | Description |
|--------|---------|---------------|-----|-------------|
| Light | 1-20 | 16.77 | 30.12 | HOT — shell effects, magic numbers, He-4 anomaly |
| Medium (Iron peak) | 21-28 | 2.49 | 0.43 | WARM — most tightly bound nuclei |
| Heavy | 29-82 | 1.50 | 0.40 | COOL — smooth Coulomb growth |
| Actinide | 83+ | 1.15 | 0.08 | COLD — SEMF composition barely changes |

## What It Means

Light nuclei are compositionally volatile — their SEMF composition (Volume, Surface, Coulomb, Asymmetry fractions) changes dramatically from one Z to the next due to shell closures and magic numbers. Heavy and actinide nuclei are compositionally calm — the SEMF terms scale smoothly with A and Z.

The actinide region (sigma_A^2 ~ 1.1) is where the stability island programme operates. The "cold" compositional landscape at high Z is consistent with the broad stability corridor prediction (Z ~ 114-126, N ~ 184).

## Evidence

| Document | Location |
|----------|----------|
| EXP-03 Sealed | codawork2026/experiments/EXP-03_Uranium/EXP03_SEALED_CONCLUSION.json |
| Nuclear staircase analysis | ai-refresh/HUF_FAST_REFRESH.json -> nuclear_programme |

---

*The valley has a temperature. The instrument reads it.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (SEMF formulas, canonical values).*

### SEMF Compositional Decomposition

Each nucleus (Z, A) is decomposed into a 4-part composition on S^4:

    x(Z, A) = C(E_V, E_S, E_C, E_A)

where:

    E_V = a_V * A                          (Volume: 15.56 MeV)
    E_S = a_S * A^{2/3}                    (Surface: 17.23 MeV)
    E_C = a_C * Z(Z-1) / A^{1/3}           (Coulomb: 0.7 MeV)
    E_A = a_A * (A-2Z)^2 / A               (Asymmetry: 23.285 MeV)

The closure operator C normalises to sum = 1.

### sigma_A^2 as Compositional Temperature

    sigma_A^2(Z) = (1/4) sum_{i=1}^{4} [clr_i(x(Z))]^2

This measures how balanced the four SEMF terms are. Light nuclei have extreme imbalances (shell effects, He-4 anomaly), producing high sigma_A^2. Heavy nuclei have smooth scaling, producing low sigma_A^2.

### Canonical Values

| Region | Z range | Mean sigma_A^2 | Std | Physical regime |
|--------|---------|---------------|-----|----------------|
| Light | 1-20 | 16.77 | 30.12 | Shell closures, magic numbers |
| Iron peak | 21-28 | 2.49 | 0.43 | Maximum binding per nucleon |
| Heavy | 29-82 | 1.50 | 0.40 | Smooth Coulomb growth |
| Actinide | 83+ | 1.15 | 0.08 | Near-constant SEMF composition |

### The Coulomb Cliff

Beyond the actinide region, SEMF extrapolation predicts:

    Z ~ 363 : B/A becomes negative (absolute instability)
    Z ~ 419 : Coulomb term dominates all others (Coulomb cliff)

These are SEMF extrapolations beyond the validated regime and carry no shell-correction or relativistic corrections. They are corridor-level estimates (L0).

### Connection to Decay Chain Relaxation

The nuclear heat map (sigma_A^2 vs Z) is the static view. The decay chain PLL (sigma_A^2 along a decay chain) is the dynamic view. Both use the same SEMF decomposition on S^4. The heat map shows WHERE the valley is cold; the decay chain shows HOW the system reaches cold from hot. See: RADIOACTIVE_DECAY_IS_RELAXATION.md.
