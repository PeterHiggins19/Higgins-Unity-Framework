<!-- Markdown companion to Book0_HUF_QIT_Primer.docx — machine-readable version for AI ingestion -->

**HUF-QIT PRIMER**

Mathematical Foundations for Compositional Quantum Diagnostics

*Book 0 of the HUF-QIT Series*

Peter Higgins

Rogue Wave Audio

April 2026

*This document introduces all mathematical concepts, notation, and tools required to read the companion papers: Book 1 (The Observer Problem) and Book 2 (Quantum Toolkit Results).*

**PART I: COMPOSITIONAL DATA ANALYSIS (CoDa)**

**1. The Simplex and Closure**

A D-part composition x = (x₁,...,x_D) is a vector of positive components that sum to a constant κ (usually κ=1). It lives on the simplex S^D, a geometric space with special properties defined by this constant-sum constraint.

The closure operation transforms any positive vector y into a composition:

*C(y) = κ(y₁/Σⱼ yⱼ, ..., y_D/Σⱼ yⱼ)*

The constant-sum constraint matters because it creates spurious correlations in naive statistical analysis. If you ignore the constraint and treat compositions as unconstrained vectors, you will observe correlations between parts that are purely artifacts of the closure, not reflections of true relationships. This was first documented by Chayes (1960) and remains one of the most common errors in compositional data analysis.

Example: in energy portfolios, if Wind generation increases by 1%, Coal must decrease (since they sum to 100%). A standard correlation analysis will show spurious negative correlation even if Wind and Coal are independent in reality.

**2. Aitchison Geometry**

John Aitchison (1986) proved that the simplex is a vector space under two operations: perturbation (addition) and powering (scalar multiplication). This insight revolutionized compositional data analysis.

Perturbation (group operation on the simplex):

*x ⊕ p = C(x₁p₁, ..., x_D p_D)*

Powering (scalar multiplication):

*α ⊙ x = C(x₁^α, ..., x_D^α)*

Aitchison Inner Product:

*⟨x,y⟩_A = (1/2D) Σᵢ Σⱼ ln(xᵢ/xⱼ) ln(yᵢ/yⱼ)*

Aitchison Distance (metric derived from the inner product):

*d_A(x,y) = √(⟨x⊖y, x⊖y⟩_A)*

Aitchison Norm (distance from the simplex barycenter):

*||x||_A = d_A(x, barycenter)*

These definitions ensure that all classical multivariate statistics (distances, angles, projections) respect the constant-sum constraint and produce no spurious correlations.

**3. Log-Ratio Transforms**

Log-ratio transforms map compositions from the simplex into unconstrained Euclidean space, where standard statistical methods apply. Three main variants exist:

**Additive Log-Ratio (ALR)**

*z_i = ln(x_i / x_D), i=1..D-1*

Selects one part (x_D) as denominator. Simple but breaks symmetry; different parts in denominator yield different correlations in z-space.

**Centred Log-Ratio (CLR)**

*z_i = ln(x_i / g(x)), where g(x) = (∏ xⱼ)^(1/D)*

Divides each part by the geometric mean. Symmetric, but produces redundant output: Σz_i = 0 always, so only D−1 coordinates are free.

**Isometric Log-Ratio (ILR)**

*z = Ψ' · CLR(x)*

Ψ is a D×(D−1) contrast matrix that orthonormalizes the CLR. Produces D−1 independent coordinates that preserve all Aitchison distances. This is the gold standard for statistical analysis.

Sequential Binary Partition (SBP): A systematic way to construct Ψ from a tree that recursively splits the D parts into groups. Each node of the tree generates one row of Ψ.

Variation Matrix:

*T_ij = var(ln(x_i/x_j))*

Summarizes the variance of all pairwise log-ratios. High T_ij means parts i and j vary independently; low T_ij means they co-vary strongly.

| **Transform** | **Pros** | **Cons** |
|---|---|---|
| ALR | Simple; fast computation | Asymmetric; correlation depends on denominator choice |
| CLR | Symmetric; geometric mean is canonical | Redundant; Σz=0 constraint; not orthogonal |
| ILR | Orthogonal; D−1 free coordinates; preserves all distances | Requires contrast matrix construction; less interpretable |

**4. Subcompositional Coherence**

A diagnostic computed on a subset of parts should be consistent with the full composition. This principle is violated by naive statistical methods applied to compositions.

Example of failure: Suppose you rank energy carriers by variance in a 9-part composition. Then you exclude Nuclear and re-rank the same 8 remaining parts. The ordering should not change. But with raw proportions or ALR, the rankings often reverse, and correlations flip signs. This is subcompositional incoherence.

Aitchison's Theorem: ILR balances (the output of the ILR transform with an appropriate contrast matrix) are subcompositionally coherent. Raw proportions, ALR, and naive correlations are not.

This is why Book 1 and Book 2 use ILR-based diagnostics exclusively. The quantum framework relies on this coherence property.

**PART II: THE HIGGINS UNITY FRAMEWORK (HUF)**

**5. Origins: DADC and DADI**

The Higgins Unity Framework (HUF) originated in audio physics, specifically in the analysis of loudspeaker radiation patterns in the presence of cabinet geometry.

DADC (Dimension-Apportioned Diffraction Correction): A model that maps loudspeaker cabinet dimensions to the compositional distribution of acoustic gain across frequency. The total baffle step (a universal diffraction effect) equals 6.02 dB, which is the closure constant for this acoustic composition.

DADI (Dimension-Apportioned Diffraction Inference): The inverse problem. Given an external radiation pattern (measured or simulated), infer the cabinet geometry through a non-contact constrained boundary measurement. This is a classic ill-posed inverse problem with a unique solution under the closure constraint.

The audio-to-CoDa bridge:

-   Cabinet wall geometry = closure boundary

-   Radiation pattern = log-ratio transform

-   Diffraction correction = partial trace (see Section 15)

When Higgins applied these same structural principles to energy system compositions (NGFS data), the mathematics remained identical. This led to the realization that the framework is universal and extends to quantum mechanics.

**6. HUF Diagnostics**

HUF defines five core metrics for monitoring compositional systems:

**χ̄ (chi-bar)**

Mean Aitchison distance between consecutive timestep compositions.

*χ̄(t) = (1/T) Σₜ d_A(x(t), x(t+1))*

Measures the transition pace of the composition. High χ̄ = rapid shifts; low χ̄ = stable composition.

**CV(χ)**

Coefficient of variation of Aitchison distances across timesteps. Measures uniformity of pace. CV(χ) near 1 = highly erratic transitions; CV(χ) near 0 = uniform pace.

**W (Winding ratio)**

Total path length in Aitchison space divided by the geodesic (straight-line) distance.

*W = (Σₜ d_A(x(t), x(t+1))) / d_A(x(0), x(T))*

W=1 means a straight path through composition space; W>1 means meandering.

**Gov Efficiency**

Governance efficiency combines χ̄ and CV(χ).

*Gov = χ̄ / (1 + CV(χ))*

Quantifies steady, purposeful transition. High Gov = strong directional control.

**k₁ Distance**

Aitchison distance from the initial composition to the final composition.

*k₁ = d_A(x(0), x(T))*

The net displacement in composition space. Combined with W, gives a picture of efficiency.

**Carrier Gate (T6c)**

A fake-simplex detection test. Checks whether a claimed composition truly satisfies the closure constraint or is a disguised Euclidean vector. Used to validate data integrity.

**7. MC-4: The Fourth Monitoring Category**

Classical system monitoring divides observables into three categories:

-   Category 1 (Magnitude): How much? Total generation, absolute quantities.

-   Category 2 (Identity): What kind? The parts, the components, their labels.

-   Category 3 (Trend): Which direction? Increasing or decreasing? The sign of change.

HUF introduces Category 4:

-   Category 4 (Composition): Internal balance. How are the parts distributed relative to each other?

MC-4 detects deceptive drift: a composition can appear stable in Categories 1−3 (total is flat, parts are present, trend is neutral) while undergoing radical internal reorganization. This invisible compositional shift is undetectable by conventional monitoring and can have profound consequences for system stability or efficiency. The "invisible door" in the title refers to this hidden channel of change.

**8. EITT: Entropy-Invariant Time Transformer**

When time is compressed (e.g., aggregating daily data to monthly), the Aitchison variance of a composition typically drops 40−60%, and most statistical properties change. But Shannon entropy shows remarkable stability.

Shannon Entropy:

*H(x) = −Σᵢ xᵢ ln(xᵢ)*

EITT Claim: If you compress a timeseries of compositions using geometric-mean decimation (block_k), the Shannon entropy of the block mean equals the Shannon entropy of the original timeseries, for any k.

*H(block_k(X)) ≈ H(X) for all k*

Validation across real datasets:

-   EMBER monthly electricity data (341:1 compression): mean ΔH = 1.02%, all countries < 2%

-   NGFS Phase 4 energy scenarios (17 timesteps): ΔH < 5% across all regions and scenarios

Geometric mean is the entropy-preserving temporal filter. This property is critical for EITT and underlies the connection to quantum unitarity (Section 15, Isomorphism IV).

**9. The Open-Loop Doctrine (ADAC Fork)**

HUF-GOV (Governance without Feedback): The system is observed, diagnostics are computed, humans make decisions, but there is no automatic feedback loop. The instrument reads; the human decides; the loop stays open. This is the focus of Books 0−2.

HUF-CLS (Closed-Loop System): A future extension in which diagnostics automatically feed back into control setpoints, optimizing the composition in real-time. This is the road not taken in the current series.

Lead-Time Observation vs Prediction: HUF-GOV speaks defensively of "observation" and "lead-time metrics" rather than "prediction." The reason is philosophical: Book 1 (The Observer Problem) explores how observation itself alters the system state, especially in quantum regimes. Prediction is a stronger claim; observation is more modest and honest.

**PART III: QUANTUM MECHANICS ESSENTIALS**

**10. Hilbert Space and State Vectors**

A state vector |ψ⟩ lives in a Hilbert space H, a complex vector space with an inner product. The norm is defined by:

*⟨ψ|ψ⟩ = 1*

Basis: Any orthonormal set {|eᵢ⟩} forms a basis. A state is expressed as:

*|ψ⟩ = Σ cᵢ|eᵢ⟩ with Σ|cᵢ|² = 1*

Born Rule: The probability of measuring outcome i is |cᵢ|². This is a composition on the outcome simplex: the probabilities sum to 1, and they are normalized.

Density Matrix (pure state):

*ρ = |ψ⟩⟨ψ|*

Density Matrix (mixed state):

*ρ = Σ pᵢ|ψᵢ⟩⟨ψᵢ| with Σ pᵢ = 1 and Tr(ρ) = 1*

The trace condition enforces unit norm. The pᵢ form a probability composition.

**11. Entanglement and the Tensor Product**

Bipartite system (two subsystems A and B):

*H_AB = H_A ⊗ H_B*

Product State (no entanglement): Can be factored into separate A and B parts.

*|ψ⟩_AB = |a⟩|b⟩*

Entangled State: Cannot be factored.

*|ψ⟩_AB ≠ |a⟩|b⟩ for any |a⟩, |b⟩*

Bell State (maximally entangled):

*|Φ⁺⟩ = (1/√2)(|00⟩ + |11⟩)*

Partial Trace: Tracing out subsystem B leaves the reduced density matrix of A.

*ρ_A = Tr_B(ρ_AB)*

This operation is mathematically identical to the closure operation in CoDa (Section 15, Isomorphism III).

**12. Decoherence and Measurement**

Wigner's Friend (1961): A conscious observer measures a quantum system and records the outcome. An outside observer then measures the state of the first observer + system. Wigner showed that the outcomes can be incompatible, raising questions about the nature of measurement and consciousness.

Zurek's Einselection (2003): The environment interacts with a quantum system and selectively couples to certain basis states called pointer states. These are the only states that remain coherent after environment interaction. Einselection explains why we see definite outcomes without invoking collapse or consciousness.

Relaño's Framework (2020, arXiv:1908.09737v2): Extends decoherence to explain apparent wavefunction collapse as a consequence of environment overlap decay.

Environment Overlap Decay:

*|⟨ε₁(t)|ε₂(t)⟩|² → 0*

as time and environment size increase. When two possible environment states become orthogonal, interference between quantum branches vanishes, and the system appears to have collapsed.

**13. Bell Inequalities**

EPR Paradox (Einstein, Podolsky, Rosen 1935): If quantum mechanics is complete, measurements on one half of an entangled pair can instantly affect the other, violating locality. This led Einstein to dismiss the theory as incomplete.

Bell's Theorem (1964): No local hidden variable theory can reproduce all predictions of quantum mechanics. Formalized as Bell inequalities that are satisfied by local hidden variable theories but violated by quantum mechanics.

CHSH Inequality (Clauser, Horne, Shimony, Holt 1969): A practical form of Bell's inequality.

*S = |E(a,b) + E(a,b') + E(a',b) - E(a',b')| ≤ 2*

Here E(θ,φ) is the expectation value of a measurement with settings θ and φ. Classical theories predict S ≤ 2.

Tsirelson's Bound (1980): Quantum systems cannot exceed:

*S_max = 2√2 ≈ 2.83*

Leggett-Garg Inequality (1985): A temporal version of Bell's inequality that applies to a single system measured at three different times.

*K₃ = C₁₂ + C₂₃ - C₁₃ ≤ 1*

C_ij is the correlation between measurements at times i and j. Quantum systems can violate this bound.

**14. Quantum Information Tools**

Von Neumann Entropy (quantum generalization of Shannon entropy):

*S(ρ) = −Tr(ρ ln ρ)*

Measures the amount of quantum uncertainty in a state. S=0 for pure states, S=S_max for maximally mixed states.

Schmidt Decomposition: Any bipartite state can be written as:

*|ψ⟩_AB = Σᵢ λᵢ|aᵢ⟩|bᵢ⟩*

The λᵢ (Schmidt coefficients, which are singular values) quantify the degree of entanglement. Equal λᵢ means maximal entanglement.

Quantum Fidelity: A measure of how similar two quantum states are.

*F(ρ,σ) = (Tr√(√ρ σ √ρ))²*

F=1 if states are identical, F=0 if orthogonal.

Quantum Mutual Information: A measure of total correlation between subsystems A and B.

*I(A:B) = S(A) + S(B) - S(AB)*

I=0 if independent, I=S(A) if B is a copy of A (perfect correlation).

GHZ State (Greenberger-Horne-Zeilinger 1989): A tripartite maximally entangled state.

*|GHZ⟩ = (1/√2)(|000⟩ + |111⟩)*

All three qubits are perfectly correlated; measuring one determines the others.

**PART IV: THE BRIDGE --- CoDa ↔ QUANTUM**

**15. The Structural Isomorphism**

Nine deep mathematical correspondences exist between quantum mechanics and compositional data analysis. Below is the master table:

| **#** | **Quantum Concept** | **CoDa Concept** | **Mechanism** |
|---|---|---|---|
| I | Basis ambiguity | Log-ratio choice (ALR/CLR/ILR) | Gauge freedom |
| II | Pointer states | ILR balances | Environmental selection |
| III | Partial trace | Closure | Subspace projection |
| IV | Unitarity (conservation) | EITT (entropy invariance) | Geometric mean |
| V | Ext. interference → memory | Subcomp. recalculation | Decoherence effect |
| VI | No-go theorem | Subcomp. incoherence | Constraint violation |
| VII | Multiple observers | Multiple IAMs (interp.) | Frame dependence |
| VIII | Orthogonal injection | Perturbation | Non-contact forcing |
| IX | Ground state | Isotropic barycenter | Null state |

Each isomorphism is explored in detail in Books 1 and 2. The correspondence is not a metaphor; it is a rigorous mathematical equivalence under the right mapping of concepts.

**16. Notation Guide**

Below is the master table of all symbols used across Books 0, 1, and 2. Use this as a reference.

| **Symbol** | **Definition / Meaning** | **Domain / Type** | **First Use (Book)** |
|---|---|---|---|
| x, y, z | Composition (vector of parts) | Simplex S^D | Sec 1 |
| S^D | D-part simplex | Geometric space | Sec 1 |
| C(·) | Closure operation | S^D → S^D | Sec 1 |
| ⊕ | Perturbation (Aitchison addition) | S^D × S^D → S^D | Sec 2 |
| ⊙ | Powering (Aitchison scalar mult) | ℝ × S^D → S^D | Sec 2 |
| ⟨·,·⟩_A | Aitchison inner product | S^D × S^D → ℝ | Sec 2 |
| d_A(·,·) | Aitchison distance | S^D × S^D → ℝ≥0 | Sec 2 |
| \|\|·\|\|_A | Aitchison norm | S^D → ℝ≥0 | Sec 2 |
| CLR(·) | Centred log-ratio transform | S^D → ℝ^D (dependent) | Sec 3 |
| ALR(·) | Additive log-ratio transform | S^D → ℝ^(D-1) | Sec 3 |
| ILR(·) | Isometric log-ratio transform | S^D → ℝ^(D-1) | Sec 3 |
| Ψ | Contrast matrix for ILR | D×(D-1) matrix | Sec 3 |
| T_ij | Variation matrix (log-ratio var) | D×D symmetric | Sec 3 |
| χ̄ | Mean Aitchison distance (pace) | ℝ≥0 | Sec 6 |
| CV(χ) | Coefficient of variation (pace) | ℝ≥0 | Sec 6 |
| W | Winding ratio (path/geodesic) | ℝ≥1 | Sec 6 |
| k₁ | Start-to-end Aitchison distance | ℝ≥0 | Sec 6 |
| H(x) | Shannon entropy | ℝ≥0 | Sec 8 |
| \|ψ⟩ | Quantum state vector | Hilbert space H | Sec 10 |
| ρ | Density matrix | Hermitian, Tr(ρ)=1 | Sec 10 |
| Tr() | Trace (matrix diagonal sum) | Matrix → scalar | Sec 10 |
| ⊗ | Tensor product (Hilbert spaces) | H_A ⊗ H_B | Sec 11 |
| S(ρ) | Von Neumann entropy | ℝ≥0 | Sec 14 |
| F(ρ,σ) | Quantum fidelity | [0,1] | Sec 14 |
| I(A:B) | Quantum mutual information | ℝ≥0 | Sec 14 |
| λᵢ | Schmidt coefficients (singular values) | [0,1] sorted | Sec 14 |
| E(a,b) | Correlation in CHSH inequality | [-1,1] | Sec 13 |
| S_CHSH | CHSH inequality value | [0, 2√2] | Sec 13 |
| K₃ | Leggett-Garg 3-time correlator | [-1,1] | Sec 13 |

**APPENDIX A: Data Sources**

**NGFS Phase 4 V4.0 (Net Zero Scenarios)**

The NGFS Phase 4 dataset is a publicly available energy transition scenario suite developed by the Network for Greening the Financial System. It contains:

-   496,224 rows of energy data

-   62 geographic regions (countries + regional aggregates)

-   17 timesteps (5-year intervals: 2020, 2025, 2030, ..., 2100)

-   9 energy carriers: Coal, Gas, Oil, Nuclear, Hydro, Solar, Wind, Biomass, Geothermal

-   3 Integrated Assessment Models (IAMs): GCAM 6.0 NGFS, MESSAGEix-GLOBIOM 1.1, REMIND-MAgPIE 3.2-4.6

-   7 climate and policy scenarios (see table below)

| **Scenario** | **Description** | **Warming Target** |
|---|---|---|
| NDC (2000) | Nationally Determined Contributions only (baseline) | ~2.6°C |
| Current Policy | Policies enacted as of 2020 (no new action) | ~2.7°C |
| Delayed Transition | Late policy action (post-2030) | ~2.0°C |
| Net Zero 2050 | Rapid decarbonization to net-zero by 2050 | ~1.5°C |
| Net Zero 2060 | Decarbonization to net-zero by 2060 | ~1.6°C |
| Net Zero 2070 | Decarbonization to net-zero by 2070 | ~1.7°C |
| Below 2°C | Aggressive action for <2°C warming | ~1.8°C |

These scenarios represent a comprehensive space of possible energy system transitions, making them ideal for testing diagnostic frameworks like HUF and validating EITT claims.

**APPENDIX B: References**

[1] Aitchison, J. (1986). The Statistical Analysis of Compositional Data. Chapman & Hall.

[2] Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003). Isometric logratio transformations for compositional data analysis. Mathematical Geology, 35(3), 279--300.

[3] Pawlowsky-Glahn, V., & Buccianti, A. (Eds.). (2011). Compositional Data Analysis: Theory and Applications. John Wiley & Sons.

[4] Greenacre, M. (2018). Compositional Data Analysis in Practice. Chapman & Hall.

[5] Higgins, P. (2026). The Higgins Unity Framework: Theory and Application. Rogue Wave Audio Working Paper.

[6] Higgins, P. (2026). Entropy-Invariant Time Transformation (EITT) for Compositional Timeseries. Rogue Wave Audio Working Paper.

[7] Wigner, E. P. (1961). Remarks on the mind-body question. In I. J. Good (Ed.), The Scientist Speculates (pp. 284--302). Heinemann.

[8] Zurek, W. H. (2003). Decoherence, einselection, and the quantum origins of the classical. Reviews of Modern Physics, 75(3), 715--775.

[9] Relaño, A. (2020). Decoherence as explanation for apparent collapse in Wigner's friend scenario. arXiv preprint arXiv:1908.09737v2.

[10] Bell, J. S. (1964). On the Einstein Podolsky Rosen paradox. Physics Physique Физика, 1(3), 195--200.

[11] Clauser, J. F., Horne, M. A., Shimony, A., & Holt, R. A. (1969). Proposed experiment to test local hidden-variable theories. Physical Review Letters, 23(15), 880--884.

[12] Tsirelson, B. S. (1980). Quantum generalizations of Bell's inequality. Letters in Mathematical Physics, 4(2), 93--100.

[13] Leggett, A. J., & Garg, A. (1985). Quantum mechanics versus macroscopic realism: Is the flux there when nobody looks? Physical Review Letters, 54(9), 857--860.

[14] Greenberger, D. M., Horne, M. A., & Zeilinger, A. (1989). Going beyond Bell's theorem. In M. Kafatos (Ed.), Bell's Theorem, Quantum Theory and Conceptions of the Universe (pp. 69--72). Kluwer.

[15] Frauchiger, D., & Renner, R. (2018). Quantum theory cannot consistently describe the use of itself. Nature Communications, 9(1), 3711.

[16] Brukner, Č. (2018). On the quantum measurement problem. In Quantum [Un]Speakables II (pp. 95--117). Springer.

[17] Landauer, R. (1961). Irreversibility and heat generation in the computing process. IBM Journal of Research and Development, 5(3), 183--191.

[18] Coecke, B., & Duncan, R. (2011). Interacting quantum observables: Categorical algebra and diagrammatics. New Journal of Physics, 13(4), 043016.

[19] Orús, R. (2019). Tensor networks for complex quantum systems. Nature Reviews Physics, 1(9), 538--550.

[20] NGFS (Network for Greening the Financial System). (2024). Climate Scenarios V4.0. https://data.ene.iiasa.ac.at/ngfs/
