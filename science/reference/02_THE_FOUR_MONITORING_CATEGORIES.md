# The Four Monitoring Categories

**DocCode:** REF-002 (derived from MONITOR-001)  
**Source:** `huf-gov/science/MONITOR-001.json`  
**Status:** State of record  

---

## The Gap

No unified taxonomy of monitoring categories exists. The first three — Magnitude, Identity, Trend — are ubiquitous but never unified into a formal framework. The fourth — Composition — has a 40-year mathematical foundation (Aitchison 1982, Compositional Data Analysis) but was never framed as a monitoring category.

HUF's contribution is applying existing mathematics as a monitoring observable, not inventing new mathematics.

---

## The Four Categories

| Category | Question | What It Reveals | What It Misses | Status |
|----------|----------|-----------------|----------------|--------|
| **MC-1: Magnitude** | How much? What is the scalar quantity? | Scale, size, total volume | Internal structure (deceptive drift) | Universally deployed |
| **MC-2: Identity** | Who or what? What are the named constituents? | The names on the axes; who the players are | Internal dynamics; balance of power shifting | Universally deployed |
| **MC-3: Trend** | Which direction? How is magnitude changing over time? | Direction and speed of aggregate change | Internal rotation (object rotates without translating; shadow unchanged) | Universally deployed |
| **MC-4: Composition** | What is the internal balance? How are parts arranged? | Structural dynamics; zero-sum trade-offs; concentration; deceptive drift | Absolute scale (deliberately removed by normalisation) | Mathematically established; diagnostically absent |

---

## Operational Examples

**MC-1 (Magnitude):** Total GDP, total hectares, total energy generation, total case counts.

**MC-2 (Identity):** Country name, sector label, species ID, demographic category.

**MC-3 (Trend):** GDP growth rate, energy change year-over-year, population growth, revenue trajectory.

**MC-4 (Composition):** Energy mix (coal, gas, nuclear, renewables; sum = 1). GDP composition (agriculture, industry, services; sum = 1). Ecosystem balance (water, marsh, forest, grassland; sum = 1).

---

## Mathematical Home

MC-1 through MC-3 operate on Stevens' measurement scales (1946): ratio scale (true zero), nominal scale (categorical), and interval/ratio scale (time-indexed).

MC-4 operates on the Aitchison simplex: a bounded space where all components sum to a constant (typically 1), and the natural operations are perturbation (multiplicative change) and powering (scalar scaling). The geometry is Riemannian. Distances are measured by the Aitchison metric. Coordinates are log-ratios.

---

## Why MC-4 Was Invisible

**The closure problem was treated as nuisance, not signal.** When statisticians encountered unit-sum data, they treated the constraint as a technical annoyance requiring correction (spurious correlations, singular covariance matrices). Aitchison showed it was geometry — but the monitoring community never adopted the result.

**Magnitude dominance.** Institutional culture rewards growth. Monitoring systems are built to answer "how much?" because funding, policy, and careers are denominated in magnitude. Composition is not rewarded in the same way.

**The primer gap.** The mathematics community (CoDa) had the structure. The monitoring community (WHO, OECD, UN) had the context. Neither read the other. HUF sits at the boundary where these two communities meet.

---

## Using Existing Methods to Define MC-4

**UN Results-Based Management:** Indicator definition: Structural Concentration Index (K_eff) — dimensionless scalar on [0,1]. Deliberately marked with NO target, because MC-4 is diagnostic, not prescriptive. The instrument reads. The human decides.

**OECD extension:** Seventh evaluation criterion: Structural Integrity — "did the intervention maintain or improve internal proportional balance, or introduce structural concentration?"

**WHO extension:** Composition-Based Surveillance (CBS) — monitors proportional distribution across subpopulations; detects hollowing before magnitude triggers.

**ISO standard:** Future ISO standard for composition monitoring instruments. Precedent: ISO 7240 (fire systems), ISO 10816 (vibration), ISO 14644 (cleanrooms).

---

## Academic Lineage

Stevens (1946) → Shannon (1948) → Aitchison (1982) → Pawlowsky-Glahn & Egozcue (2001) → WHO/OECD/UN frameworks → Higgins (2025–2026) HUF

---

## Open Questions

- **MONITOR-Q1:** Is the four-category taxonomy complete, or are there additional monitoring intents?
- **MONITOR-Q2:** Can MC-1, MC-2, MC-3 be formally derived as projections from MC-4?

---

*Definitive source: `huf-gov/science/MONITOR-001.json`*  
*Peter Higgins | Rogue Wave Audio | PeterHiggins@RogueWaveAudio.com*
