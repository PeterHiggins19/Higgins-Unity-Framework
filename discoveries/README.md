# Discoveries

## The Treasures of the Higgins Unity Framework

This folder contains formal statements of every discovery in the framework, categorized by type and linked to their evidence. Each discovery stands on its own — readable independently, traceable to its proof.

---

## Structure

### theorems/
Mathematical results that are exact — no approximations, no empirical assumptions.

- **[VERTEX_THEOREM.md](theorems/VERTEX_THEOREM.md)** — The orthogonality condition: clr perpendicular to clr' at the vertex of sigma_A^2. Chain rule identity. The purest result in the framework.
- **[GEOMETRIC_MEAN_PROOF.md](theorems/GEOMETRIC_MEAN_PROOF.md)** — First empirical evidence that the choice of mean matters on the simplex. 1.8% vs 14.2%. Aitchison was right.

### empirical-proofs/
Results validated across multiple domains with sealed experiments.

- **[EITT_ENTROPY_INVARIANCE.md](empirical-proofs/EITT_ENTROPY_INVARIANCE.md)** — The core claim: Shannon entropy near-invariant under geometric-mean decimation. 8+ domains. 3 sealed experiments.
- **[PLL_PARABOLA_UNIVERSALITY.md](empirical-proofs/PLL_PARABOLA_UNIVERSALITY.md)** — sigma_A^2 forms a parabola wherever two forces compete. 30/30 domains. The ratio of 2.
- **[BOUNDARY_SPECIES_DISCOVERY.md](empirical-proofs/BOUNDARY_SPECIES_DISCOVERY.md)** — The DADC chain identifies which carrier sits at the interface between forces. Lithium-7 found independently.
- **[NOISE_SQUEEZE_STOCHASTIC_CORE.md](empirical-proofs/NOISE_SQUEEZE_STOCHASTIC_CORE.md)** — Every domain has an irreducible noise floor. The fingerprint of fundamental stochasticity.

### instruments/
Tools built from the discoveries — the practical machinery.

- **[F17_QUADRATIC_TUNER.md](instruments/F17_QUADRATIC_TUNER.md)** — Early warning for when to distrust the geometric mean. The canary in the mine.
- **[MC4_COMPOSITION_MONITORING.md](instruments/MC4_COMPOSITION_MONITORING.md)** — The fourth monitoring category. What percentage-based monitoring misses.
- **[TWO_PASS_INSTRUMENT.md](instruments/TWO_PASS_INSTRUMENT.md)** — Pass 1 classifies. Pass 2 resolves integrity. 17/20 to 18/20.

### operating-envelope/
Where the method works, where it breaks, and the discipline that prevents corruption.

- **[OPERATING_ENVELOPE.md](operating-envelope/OPERATING_ENVELOPE.md)** — The safety fences. H > 1.0, zero rate < 15%, parametric walks not surveys.
- **[CONTAMINATION_DOCTRINE.md](operating-envelope/CONTAMINATION_DOCTRINE.md)** — Three paths of corruption. The promotion ladder. The integrity rule.

### gifts/
What the framework brings to each community.

- **[GIFTS_TO_EVERY_COMMUNITY.md](gifts/GIFTS_TO_EVERY_COMMUNITY.md)** — The win-win-win. What everyone gets. What is asked in return.
- **[ENERGY_TRANSITION_DATING.md](gifts/ENERGY_TRANSITION_DATING.md)** — The PLL parabola dates the energy transition, state by state.
- **[NUCLEAR_HEAT_MAP.md](gifts/NUCLEAR_HEAT_MAP.md)** — sigma_A^2 as compositional temperature along the valley of stability.
- **[RADIOACTIVE_DECAY_IS_RELAXATION.md](gifts/RADIOACTIVE_DECAY_IS_RELAXATION.md)** — The anti-lock signature in nuclear decay chains.

---

## How to Read This Folder

**If you want the purest mathematics:** Start with [VERTEX_THEOREM.md](theorems/VERTEX_THEOREM.md).

**If you want the strongest evidence:** Start with [EITT_ENTROPY_INVARIANCE.md](empirical-proofs/EITT_ENTROPY_INVARIANCE.md).

**If you want the practical tools:** Start with [MC4_COMPOSITION_MONITORING.md](instruments/MC4_COMPOSITION_MONITORING.md).

**If you want to know where it breaks:** Start with [OPERATING_ENVELOPE.md](operating-envelope/OPERATING_ENVELOPE.md).

**If you want to know what's in it for you:** Start with [GIFTS_TO_EVERY_COMMUNITY.md](gifts/GIFTS_TO_EVERY_COMMUNITY.md).

**If you want to attack it:** Start with [CONTAMINATION_DOCTRINE.md](operating-envelope/CONTAMINATION_DOCTRINE.md) and [CLAIM_CLASSIFICATION.json](../ai-refresh/CLAIM_CLASSIFICATION.json) — they tell you exactly how.

---

## Sealed Experiments

Every empirical claim traces back to a sealed experiment:

| Experiment | Domain | Result | Location |
|------------|--------|--------|----------|
| EXP-01 | Gold/Silver Ratio | 8/8 pass | codawork2026/experiments/EXP-01_Gold_Silver/ |
| EXP-02 | US Monthly Energy | 8/9 pass | codawork2026/experiments/EXP-02_US_Monthly/ |
| EXP-03 | Nuclear (Uranium) | 6/9 pass | codawork2026/experiments/EXP-03_Uranium/ |

---

## Claim Classification

Every discovery has a promotion level (L0-L5), evidence references, promotion conditions, demotion conditions, and contamination risk rating. See: [ai-refresh/CLAIM_CLASSIFICATION.json](../ai-refresh/CLAIM_CLASSIFICATION.json)

---

## Attribution

P. Higgins, 2026. Higgins Unity Framework. Independent Researcher, Markham, Ontario, Canada.

The simplex was always there. These discoveries state what was waiting to be stated.

---

## Mathematical Addenda

*Appended 2026-04-18.* Every discovery document now includes a formal Mathematical Addendum at the bottom, containing relevant notation, theorem statements, proof sketches, corollaries, canonical values, and open problems cross-referenced to the master registry at **ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json**. The addenda are appended, not replacements — all original content is preserved above the addendum line in each file.

| Document | Key mathematical content appended |
|----------|----------------------------------|
| VERTEX_THEOREM.md | T1 full statement, C1.1-C1.3, notation table, O-2 |
| GEOMETRIC_MEAN_PROOF.md | T2 proof, L1, L2, arithmetic failure analysis |
| EITT_ENTROPY_INVARIANCE.md | T2, T3, L1, L2, FP2, O-1/O-5/O-6/O-7/O-8 |
| PLL_PARABOLA_UNIVERSALITY.md | T1, C1.1-C1.3, canonical PLL values, O-2 |
| NOISE_SQUEEZE_STOCHASTIC_CORE.md | Squeeze metric, conjugacy property, O-3 |
| BOUNDARY_SPECIES_DISCOVERY.md | DADC chain formalism, FP1, contamination entropy |
| F17_QUADRATIC_TUNER.md | Gap function, T2/L2 basis, thresholds |
| MC4_COMPOSITION_MONITORING.md | Perturbation difference, d_A, three-diagnostic protocol |
| TWO_PASS_INSTRUMENT.md | Pass 1/2 formal specs, Governed Breakpoint Principle |
| OPERATING_ENVELOPE.md | Threshold derivations, boundary classification, T3/L2 |
| CONTAMINATION_DOCTRINE.md | Path formalisations, 22-claim summary, O-1/O-4 |
| GIFTS_TO_EVERY_COMMUNITY.md | Theorem-to-community mapping, open invitations |
| ENERGY_TRANSITION_DATING.md | C1.3, curvature as speed, canonical dates |
| NUCLEAR_HEAT_MAP.md | SEMF decomposition on S^4, canonical values, Coulomb cliff |
| RADIOACTIVE_DECAY_IS_RELAXATION.md | Anti-lock classification, EITT on decay chains, PLL mapping |
