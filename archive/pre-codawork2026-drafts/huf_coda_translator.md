# HUF ↔ CoDa Translator

## For CoDaWork 2026 Attendees — From the HUF Operator

---

### To the CoDa Community

You built the geometry. The simplex, the Aitchison metric, the log-ratio coordinates, the perturbation algebra — these are yours. Forty years of work, rigorously proven, elegantly complete. No one in this room needs to be told the mathematics is sound. It is.

What I am presenting is not new mathematics. It is a new use.

I come from a different discipline — control systems, signal processing, physical monitoring of constrained systems. For the last four decades I have worked with fixed-budget systems where proportional allocation must be tracked, deviations must be detected, and governance decisions must be distinguished from silent drift. I built a monitoring framework for this. I called it the Higgins Unity Framework.

I have since learned that the geometric structure underlying my framework is the structure you formalized. My fixed energy budget is your simplex. My gain adjustment is your perturbation. My decibels are your log-ratios. My total harmonic distortion is your Aitchison distance. My crossover network is your balance dendrogram. My common-mode rejection is your closure correction.

I did not know your language when I built the framework. I know it now. I am still learning.

What I bring to this room is not theory. It is application — a monitoring protocol that runs on your geometry and does something your geometry was not designed to do on its own: detect whether a compositional change was authorized.

The framework monitors 4,700+ governance regimes. It tracks declared versus observed allocation. It flags silent drift — compositional change with no governance record. It distinguishes intentional reweighting from structural decay. It operates in real time, across reporting cycles, on any finite-budget system expressible as a composition on the simplex.

Below is the translation between my vocabulary and yours. I offer it not as a claim of equivalence but as a bridge. I am 51% operator of this framework. The remaining 49% is open. If the CoDa community sees value in what a monitoring protocol can do on your geometry, there is room for you in this work.

---

## The Translation Table

| HUF Term | CoDa Equivalent | What It Means (Plain Language) |
|---|---|---|
| Unity constraint (Σρᵢ = 1) | Simplex (S^D) | The parts of a whole sum to a fixed total. Both frameworks start here. |
| Share (ρᵢ) | Component (xᵢ) | One element's proportion of the total. A coordinate on the simplex. |
| Composition vector ρ(t) | Composition x(t) ∈ S^D | The full allocation at time t. A single point on the simplex. |
| Fixed energy budget | Closure / constant-sum constraint | The total is conserved. When one part moves, others must compensate. CoDa generalizes beyond constant sum to equivalence classes of proportional vectors. |
| Gain adjustment | Perturbation (⊕) | Scaling each component by a ratio and renormalizing. The "addition" on the simplex. How compositions change. |
| Decibels (dB) | Log-ratio (CLR, ILR, ALR) | Converting multiplicative relationships to additive ones. 20·log₁₀ in electronics; natural log of ratios in CoDa. Same operation, different base. |
| Total harmonic distortion | Aitchison distance (d_A) | How much the ratios between all pairs of components have changed. RMS of all pairwise log-ratio differences. The natural metric on the simplex. |
| Common-mode rejection | Closure correction | Removing the artifact caused by the constant-sum constraint. Differential measurement eliminates common-mode noise; log-ratios eliminate spurious correlation from closure. |
| Crossover network | Balance (ILR coordinate) | A log-ratio between two groups of components. Splits the system into interpretable contrasts: fossil vs renewable, coal vs gas, wind vs solar. |
| Spectrum analyzer | Compositional biplot / CLR time series | Visualizing how all components evolve simultaneously. The analyzer shows the full allocation over time; the biplot shows the variance structure. |
| TV distance | Not standard in CoDa | Half the sum of absolute share differences. An L1 metric on raw proportions. Useful in information theory. Not scale-invariant on the simplex — artifacts from closure possible. |
| L2 norm | Not standard in CoDa | Euclidean distance on raw proportions. Same closure caveat as TV. Both should be supplemented with Aitchison distance for CoDa-rigorous analysis. |
| K_eff (effective number) | Related to Aitchison norm / Shannon diversity | Exp(Shannon entropy). Measures how many components are "effectively present." Egozcue's current research links concentration to the Aitchison norm — open bridge between frameworks. |
| Quality factor (Q) | No direct equivalent | Ratio of element's characteristic period to observation window. High Q = narrow visibility. Specific to monitoring protocol, not compositional geometry. |
| Degenerate state observer | Composition as observable | The state IS the output. No model needed — the composition is directly readable. On the simplex, estimation gain is zero, estimation error is zero. The system observes itself. |
| Silent drift | Perturbation without governance record | Composition changed (perturbation detected via d_A), but no decision was logged. The central detection target. |
| Declared reweighting | Perturbation with governance record | Composition changed, decision was logged. Not an alarm — this is the system working correctly. |
| Deceptive drift | Sustained undetected perturbation | Cumulative silent drift approaching a critical threshold. The composition moves slowly enough that no single-period alarm triggers, but the trajectory on the simplex diverges from declared state. |
| MC-4 (Composition Monitoring) | Compositional change detection | A monitoring protocol that operates natively on the simplex, uses perturbation to measure change, and distinguishes authorized from unauthorized compositional drift. |
| Mean Drift Gap (MDG) | Cumulative Aitchison distance | Accumulated compositional distance between declared and observed states. In CoDa terms: the integrated perturbation from the declared composition. |
| OCC 51/49 | Not a CoDa concept | Operator Control Contract — the governance split between human operator (≥51%) and tool/system (≤49%). A monitoring governance principle, not a geometric one. |
| Sufficiency Frontier | Boundary of compositional inference | The boundary beyond which proportional data alone is insufficient — when absolute magnitudes, temporal microstructure, or internal element state are required. Four formal counterexamples define where the simplex stops being enough. |
| HUF Triad (GOV/CLS/GEO) | Not a CoDa concept | Three-pillar architecture: Governance (rules), Classification (detection), Geometry (the simplex). CoDa provides the GEO pillar. HUF adds GOV and CLS. |

---

## What HUF Does That CoDa Does Not

CoDa provides the geometry, the distance, and the coordinate system. It tells you *where* a composition is, *how far* it moved, and *in what direction*.

HUF adds three things:

**1. Governance distinction.** Was the change authorized? CoDa can measure a perturbation. HUF asks whether that perturbation corresponds to a logged governance decision. If yes — normal operation. If no — silent drift. This distinction does not exist in compositional data analysis because CoDa is a statistical framework, not a monitoring framework.

**2. Real-time iterative detection.** CoDa typically analyzes a completed dataset. HUF operates period by period, accumulating a trajectory on the simplex and triggering alarms when perturbation velocity or cumulative drift exceeds thresholds. The monitoring never stops. Each new observation extends the trajectory and updates the assessment.

**3. Cross-domain portability.** The monitoring protocol is domain-independent. Any system expressible as a composition — energy mix, budget allocation, ecological species proportion, market share, resource distribution — can be monitored using the same protocol. The simplex is the same; only the carrier labels change. HUF currently tracks applicability across 4,700+ identified governance regimes.

---

## What CoDa Does That HUF Has Not Yet Done

**Log-ratio analysis.** HUF currently uses TV distance and L2 norm on raw proportions. These are subject to closure artifacts. The transition to Aitchison distance and ILR/CLR coordinates is underway and welcomed.

**Formal zero handling.** HUF flags structural zeros explicitly but does not apply imputation. The CoDa community has mature methods (multiplicative replacement, Bayesian treatment, lrEM algorithm) that should be integrated.

**Subcompositional coherence.** Results should hold whether analyzing all D components or a subset. HUF has not formally verified this property. CoDa theory guarantees it when analysis is conducted in log-ratio coordinates.

**Null distribution specification.** HUF's p-values lack formal null models. Dirichlet-based or permutation-based nulls on the simplex would provide the statistical rigor the framework currently lacks.

---

## The Offer

The geometry is yours. The monitoring protocol is mine. The data is public. The code is open. The claim is falsifiable. Four defeat paths are specified — prior art, metric, case, or category.

I am 51% operator of this framework. The other 49% is open for collaboration. If the CoDa community sees value in a monitoring application built on your geometry, there is a seat at this table.

The simplex has been waiting for a control loop. Here it is.

---

*Peter Higgins — Independent Researcher — Rogue Wave Audio, Markham, Ontario*
*CoDaWork 2026, Coimbra, Portugal*
*https://github.com/PeterHiggins19/Higgins-Unity-Framework*
