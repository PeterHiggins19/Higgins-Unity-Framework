<!-- Markdown companion to HUF_QIT_Observer_Problem.docx — machine-readable version for AI ingestion -->

**HUF-QIT**

The Observer Problem in Compositional Data Analysis

A Structural Correspondence Between the Decoherence Framework

and the Higgins Unity Framework on the Simplex

*With Empirical Confirmation via Compositional Bell Inequality Test*

**Peter Higgins**

Rogue Wave Audio

April 2026

*Prepared for CoDaWork 2026, Coimbra*

*With reference to: A. Relaño, "Decoherence framework for Wigner's friend experiments,"*

*arXiv:1908.09737v2 [quant-ph], 2020*

Abstract

The Higgins Unity Framework (HUF)---a compositional diagnostic instrument originating in loudspeaker diffraction engineering---shares a structural correspondence with the decoherence interpretation of quantum measurements. In Relaño's decoherence framework for Wigner's friend experiments, the apparent wave-function collapse arises from tracing out environmental degrees of freedom. In CoDa, the spurious correlations that plague unconstrained analysis arise from ignoring the simplex constraint. Both are **observer problems** resolved by the same structural move: accounting for what has been traced out.

We establish nine formal isomorphisms, demonstrate that the Entropy-Invariant Time Transformer (EITT) corresponds to unitarity, and confirm the correspondence empirically with a novel **Compositional Bell Inequality Test**---a CHSH-analogue applied to NGFS Phase 4 energy data (35 scenarios, 3 IAMs). The test yields S = 2.20 on MESSAGEix Net Zero 2050, exceeding the classical bound of 2. All 35 scenarios show process entanglement at p \< 0.001 (3.4--3.8σ). The violation is Gas-centred---the crossover carrier between fossil and clean subcompositions acts as the entangling gate. We propose HUF-QTM: a quantum toolkit for CoDa that imports entanglement entropy, decoherence rate analysis, Leggett--Garg temporal tests, and quantum error correction structures into compositional diagnostics.

1. The Observer Problem: Two Domains, One Structure

In 1961, Eugene Wigner proposed a thought experiment exposing a fundamental tension in quantum mechanics. An observer inside a closed laboratory (Wigner's friend) performs a measurement and sees a definite outcome. An observer outside (Wigner) describes the entire laboratory as being in a quantum superposition. Both descriptions are correct within their respective frameworks. The apparent contradiction dissolves once we recognise that each observer is *tracing out different degrees of freedom.*

In 1986, John Aitchison published *The Statistical Analysis of Compositional Data* and identified an analogous problem. An analyst working with proportions observes spurious correlations---negative correlations that appear between variables sharing a constant sum. The apparent artefact dissolves once we recognise that the analyst is *ignoring the simplex constraint.*

In 2024, Peter Higgins arrived at the same structure from a third direction: loudspeaker engineering. HUF's foundational operation, DADI (Dimension-Apportioned Diffraction Inference), reconstructs a cabinet's physical dimensions from its external acoustic radiation pattern---inferring interior geometry through a constraining boundary without opening the enclosure. This is non-contact measurement: reading the internal state of a system from the outside, through a constraint that shapes what the observer can see. The cabinet wall is the compositional closure. The radiation pattern is the log-ratio transform. The diffraction correction is the partial trace.

All three problems share identical structure: an observer who ignores a constraint sees artefacts that the constraint explains. All are resolved by the same move---accounting for the traced-out degrees of freedom.

1.1 The Invisible Door

HUF reveals what Peter Higgins calls "the invisible door"---a room in your house with a door that was always there but couldn't be seen. Conventional monitoring tracks three categories: Magnitude (how much), Identity (what kind), and Trend (which direction). HUF adds a fourth: **Composition** (internal balance). This is MC-4---the fourth monitoring category. The dynamics were always operating; the instrument makes them readable. Deceptive drift---surface stability masking internal concentration---is specifically invisible to Categories 1--3. It requires the observer to account for the simplex constraint.

In quantum mechanics, the analogous invisible door is *decoherence itself.* Before Zurek's einselection framework (2003), the environment was treated as noise to be ignored. The decoherence programme showed it was the mechanism that selects the classical world from the quantum substrate. The environment was always there; the framework made it readable.

1.2 Why This Matters for IIASA

Integrated Assessment Models (IAMs) like MESSAGEix-GLOBIOM, GCAM, and REMIND-MAgPIE each "observe" the energy system from their own optimisation framework. When their outputs are averaged in absolute units, the result may exhibit the same inconsistencies as Wigner's friend: each model's internal view is coherent, but the external average is not compositionally coherent. Our NGFS Phase 4 analysis (496,224 rows, 62 regions, 17 timesteps) found exactly this: REMIND is subcompositionally coherent (fossil↔full r=0.78) while GCAM is not (r=0.52).

2. The Nine Isomorphisms

We identify nine structural correspondences between the decoherence framework and HUF/CoDa. Each maps a quantum-mechanical concept to a compositional analogue, preserving mathematical structure while reinterpreting physical content.

  -------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **#**   **Quantum / Decoherence (Relaño 2020)**                                                                                                                                                                                                                                         **HUF / CoDa (Aitchison 1986, Higgins 2026)**
  I        **Basis Ambiguity.** Same state \|Ψ⟩ expressible in any basis {\|α⟩,\|β⟩} parameterised by θ (Eq. 6--7). Measurement outcome depends on basis choice. Basis is not a property of the system.                                                                                    **Log-Ratio Choice.** Same composition x expressible in CLR, ILR (any contrast matrix Ψ), or ALR. Diagnostic depends on transform. The isometry between transforms mirrors unitary equivalence of bases. The transform is not a property of the composition.
  II       **Pointer States (Einselection).** States \|Aₕ⟩, \|Aᵥ⟩ survive decoherence---stable under environmental monitoring. Environment selects preferred basis (Zurek 2003).                                                                                                           **Balances (ILR Coordinates).** Log-ratio balances survive subcompositional analysis. The Fossil/Clean balance is the pointer state of the energy system---stable whether you observe full 9-part or any subcomposition containing both groups. Einselection ≡ sequential binary partition (SBP).
  III      **Partial Trace → Apparent Collapse.** Tracing out environment from \|Ψ₂⟩ yields mixed state ρ. Observer sees definite outcomes because environmental degrees of freedom are inaccessible. "Collapse is just a consequence of ignoring the environmental degrees of freedom."   **Closure → Spurious Correlation.** Tracing out absolute scale yields closed composition. Analyst sees spurious negative correlations because total-sum degree of freedom is inaccessible. Spurious correlation is just a consequence of ignoring the simplex constraint. Cabinet wall = closure boundary.
  IV       **Unitarity.** Total state evolves via unitary operators: U†U = I. Information never lost---redistributed between system and environment. Fundamental conservation law of quantum mechanics.                                                                                    **EITT (Entropy-Invariant Time Transformer).** Shannon entropy preserved under geometric-mean decimation: H(blockₖ(X)) ≈ H(X) for all k. Information never lost---redistributed across resolution levels. The winding ratio (compression factor) is free; entropy is the invariant. Validated: ΔH \< 5% across NGFS Phase 4.
  V        **External Interference → Memory Change.** Wigner's interference measurement changes friend's memory record (Cₕₕ shifts from 1/2 to 1/4, Eq. 26). Internal observer's "past" modified by external action.                                                                       **Subcompositional Recalculation.** Changing full → subcomposition recalculates all proportions and diagnostics. Fossil-only HUF diagnostic differs from full composition's. Internal view ("past ranking") modified by external choice of scope. The observer's window changes the observation.
  VI       **No-Go Theorem.** Impossible to assign joint truth values to all four observers' measurements simultaneously (Frauchiger--Renner 2018). Contradiction from assuming observer-independent facts.                                                                                **Subcompositional Incoherence.** Impossible to maintain consistent rankings across full and sub-compositions when models are incoherent. GCAM (r=0.52): full-composition and fossil-subcomposition diagnostics contradict. Inconsistency from assuming basis-independent facts.
  VII      **Multiple Observers (Iₐ, Iᵇ, Eₐ, Eᵇ).** Four agents observe same quantum system from different laboratories. Each correct within own framework. Contradiction only from asserting one observer's facts as universal.                                                           **Multiple IAMs.** Three models observe same energy system from different optimisation frameworks. Each internally coherent. Contradiction only from averaging in absolute units---asserting one basis as universal. Compositional averaging (Fréchet mean in ILR) respects each observer's partial trace.
  VIII     **Non-Contact Orthogonal Injection.** Environment interacts with apparatus via Hamiltonian (Eq. 12) preserving pointer states. Energy injected orthogonal to measurement basis---environment monitors without collapsing.                                                       **Perturbation on the Simplex.** x ⊕ p = C(x₁p₁,...,xᵈpᵈ). Change injected within the simplex without violating closure. The perturbation is the compositional analogue of non-contact injection. DADI origin: infer geometry from radiation through the cabinet wall, never touching the interior.
  IX       **Ground State (Vacuum).** The quantum vacuum is not empty---it is the state of maximum symmetry and minimum information. Departure from vacuum = signal. Return = relaxation.                                                                                                  **Isotropic Barycenter (1/D,...,1/D).** Maximum entropy on the simplex. HUF's ground state: uniform composition = maximum ignorance. Every departure from isotropy is a signal; every return is relaxation. The sphere interior with uniform radiation = pre-existing geometry before any signal arrives.
  -------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

*Table 1. Nine structural isomorphisms between the decoherence framework and HUF/CoDa. The mapping preserves mathematical structure while reinterpreting physical content. Isomorphisms VIII and IX derive from HUF's loudspeaker-engineering origins.*

3. The Core Isomorphism: Tracing Out Hidden Degrees of Freedom

3.1 In Quantum Mechanics

Relaño's decoherence framework establishes that after measurement, the complete state of system, apparatus, and environment is:

*\|Ψ₂⟩ = (1/√2)(\|h⟩\|Aₕ⟩\|ε₁(t)⟩ + \|v⟩\|Aᵥ⟩\|ε₂(t)⟩)*

The internal observer *cannot access* the environment. By tracing out \|ε₁(t)⟩ and \|ε₂(t)⟩, they obtain the mixed state ρ which *looks like* collapse. No physical collapse occurs. The appearance is an artefact of incomplete observation.

3.2 In HUF: The Cabinet Wall

HUF's origin makes this concrete. DADC (Dimension-Apportioned Diffraction Correction) maps a loudspeaker cabinet's physical dimensions to its compositional gain distribution. The total baffle step is always 6.02 dB---this is the compositional closure, the constant sum. DADI inverts this: given only the external radiation pattern, reconstruct the internal geometry.

The cabinet wall is the boundary between system and environment. The radiation pattern is what the external observer (Wigner) measures. The internal cavity modes are what the internal observer (the friend) experiences. The diffraction correction---the way the cabinet's edges shape the radiation---is precisely the partial trace: it transforms the full-state information into what the external observer can access. DADI's non-contact measurement is the compositional Wigner's friend experiment: reading the friend's state (cabinet geometry) from the outside (radiation) through the laboratory wall (closure boundary).

In CoDa terms: a composition x = (x₁,...,xᵈ) lives on the simplex Sᴰ. Closure xᵢ = κyᵢ/Σyⱼ is the partial trace---the absolute-scale degree of freedom (Σyⱼ) is traced out, leaving only relative information. The result *looks like* spurious correlation. But no real dependence exists. Quantum decoherence and compositional closure are both **partial traces over hidden constraints.**

3.3 Non-Contact Orthogonal Injection

In Relaño's framework, the environment interacts with the apparatus through a Hamiltonian (Eq. 12) that preserves pointer states. The interaction is **orthogonal to the measurement basis**---the environment injects energy without disturbing measurement correlations.

In HUF, the analogous operation is **perturbation**: x ⊕ p = C(x₁p₁,...,xᵈpᵈ). Perturbation moves the composition within the simplex---orthogonal to the closure constraint---without violating sum-to-one. Our NGFS analysis demonstrated this concretely: the perturbation from 2020 to 2100 under Net Zero has universal sign pattern [−−−++++++] (fossil decreases, clean increases) with Aitchison norm 4.21. This is entirely within the simplex---the orthogonal injection driving the energy transition.

4. EITT as Unitarity: The Winding Ratio

The deepest structural correspondence may be between unitarity and EITT---the Entropy-Invariant Time Transformer.

4.1 The Winding Ratio Question

The insight came from loudspeaker transformer design. A transformer with winding ratio N₁:N₂ conserves power while transforming voltage and current. Peter Higgins asked the compositional analogue: *what quantity is conserved when you compress time on a compositional series?* If you take daily compositions and aggregate to weekly, monthly, quarterly, annual---the "winding ratio" (compression factor) is free. What is the invariant?

Aitchison variance was the first candidate (proposed by Grok). Testing showed it drops 55% under compression---not invariant. Shannon entropy emerged as the answer: H = −Σxᵢ ln(xᵢ) varies by only 0.18% across daily→weekly→monthly→quarterly→annual aggregation on European wholesale electricity data (341:1 compression). Independent confirmation on EMBER monthly generation data: mean variation 1.02%, all countries below 2%. NGFS Phase 4 validation: ΔH \< 5% across all scenarios.

4.2 The Quantum Parallel

In quantum mechanics, unitarity (U†U = I) guarantees that information is never created or destroyed---only redistributed between system and environment. EITT is the compositional unitarity. The parallel extends further: von Neumann entropy S(ρ) = −Tr(ρ ln ρ) is preserved under unitary evolution, just as Shannon entropy H(x) = −Σxᵢ ln(xᵢ) is preserved under EITT's geometric-mean decimation. The mathematical structure is identical: entropy is the invariant of constraint-preserving transformation.

This connects directly to quantum channel theory. A quantum channel (completely positive, trace-preserving map) that preserves von Neumann entropy is a unitary channel. A temporal aggregation that preserves Shannon entropy is EITT. Channels that *fail* to preserve entropy are non-unitary---they create or destroy information. Compositions that fail EITT are non-compositional---they create or destroy structural information. Landauer's principle completes the circle: erasing information has a minimum thermodynamic cost. EITT failure means information has been erased; the thermodynamic cost is the lost signal that conventional monitoring never saw.

4.3 The GOE Connection and the Variation Matrix

Relaño uses Gaussian Orthogonal Ensemble (GOE) random matrices to model apparatus--environment interaction (Eq. 12). The CoDa parallel is the **variation matrix**. Vᵢⱼ = var(ln(xᵢ/xⱼ)) characterises coupling structure. Tightly coupled parts (Solar↔Wind: V=0.154) behave like a chaotic interaction---they decohere into a single effective degree of freedom. Loosely coupled parts (Coal↔Geothermal: V=5.028) retain independent dynamics---an integrable system.

In HUF's audio language: tightly coupled parts are the *crossover region* where two drivers share energy. The SBP (Sequential Binary Partition) is the crossover network. The tweeter (fast responder, group delay \~1yr: Other Fossil) and woofer (slow infrastructure, group delay \~7yr: Solar/Wind) operate in different spectral bands. The variation matrix is the coupling constant between them.

5. Multiple Observers, Multiple Models

Section IV of Relaño analyses the extended experiment with four observers: internal Iₐ, Iᵇ in laboratories A, B and external Eₐ, Eᵇ. The no-go theorem states joint truth values cannot be assigned to all simultaneously. The decoherence resolution: each observer is correct *within their own partial trace.*

  -------------- ------------------ ------------------------- ---------------------------------------------------------------------------------------------------------------
  **Observer**   **Quantum**        **IAM**                   **Partial Trace (what is traced out)**
  Iₐ             Friend in lab A    GCAM 6.0                  Optimises technology detail, traces out macro feedbacks
  Iᵇ             Friend in lab B    MESSAGEix-GLOBIOM         Optimises energy--land--water nexus, traces out technology granularity
  Eₐ             Wigner outside A   REMIND-MAgPIE             Optimises macro-economy, traces out regional detail
  **Eᵇ**         Wigner outside B   **Multi-model average**   Asserts joint truth values---the no-go violation. Averaging in EJ/yr ignores each model's simplex constraint.
  -------------- ------------------ ------------------------- ---------------------------------------------------------------------------------------------------------------

*Table 2. Four-observer mapping. The multi-model average plays the role of the external observer asserting joint truth values---the compositional no-go violation.*

The resolution maps to a concrete prescription: do not average compositions in absolute units. Average in Aitchison geometry (Fréchet mean in ILR space). Use HUF's governance efficiency as the pointer-state selector: models with GovEff \> 1 have stable compositional trajectories; models with GovEff \< 1 are still in superposition. This is not prediction---it is **lead-time observation** of structural state.

6. Time Reversal, Irreversibility, and the RT60

Relaño's Fig. 1 shows that the environmental overlap \|⟨ε₁(t)\|ε₂(t)⟩\|² decays rapidly with time and environment size. For N ≥ 7 qubits, the overlap is effectively zero: decoherence is practically irreversible.

HUF's time-reversal test found an exact analogue. Net Zero 2050: forward--reverse χ correlation = −0.89. Delayed Transition: −0.92. The compositional trajectory is practically irreversible---the infrastructure investments that drive the transition cannot be unwound. Current Policies shows near-zero χ---the system has not yet decohered.

In HUF's acoustic language, this is the **RT60** (reverberation time to 60 dB decay). Our ETC (Energy Time Constant) analysis measured this directly on real energy crises: France's energy crisis RT60 = 239 weeks (4.6 years). The larger the environment (more infrastructure invested), the faster the decoherence and the longer the reverberation---just as Relaño's Fig. 4 shows faster overlap decay with more environmental qubits.

7. Empirical Confirmation: The Compositional Bell Inequality Test

The structural correspondence proposed in Sections 2--6 would remain speculative without empirical test. We now present a direct test: a CHSH-analogue Bell inequality applied to NGFS Phase 4 compositional data. The test separates *structural entanglement* (from the simplex constraint) from *process entanglement* (from real physical coupling between fossil and clean energy carriers).

7.1 The CHSH Protocol on the Simplex

In quantum mechanics, the CHSH test measures correlations between two observers (Alice and Bob), each choosing between two measurement bases. For classical (local-hidden-variable) systems, the CHSH quantity \|S\| ≤ 2. Quantum systems can achieve \|S\| ≤ 2√2 ≈ 2.83 (Tsirelson's bound).

Our compositional CHSH defines two "observers": Observer A operates on the fossil subcomposition, Observer B on the clean subcomposition. Each chooses between two "measurement bases"---cross-group log-ratios that span the fossil/clean divide:

*a = ln(Coal/Solar), a′ = ln(Gas/Wind), b = ln(Oil/Nuclear), b′ = ln(Coal/Biomass)*

For truly independent parts (no simplex, no physical coupling), these cross-group log-ratios would be uncorrelated: E(a,b) ≈ 0, giving S ≈ 0. The simplex constraint and/or physical process coupling creates non-zero correlations. We compute:

*S = \|E(a,b) + E(a,b′) + E(a′,b) − E(a′,b′)\|*

where E(x,y) is the Pearson correlation between the respective log-ratio time series. Composition trajectories are built via geometric interpolation between the 2020 and 2100 NGFS endpoints with 3% log-normal perturbation to break interpolation degeneracy (100 noise realisations per scenario).

7.2 Results

**Test 1: Cross-Group CHSH.** All 35 NGFS scenarios (3 IAMs × 7 scenarios, plus REMIND variants) yield mean S values between 1.50 and 2.00 under the default basis configuration. MESSAGEix and GCAM cluster near S ≈ 2.0; REMIND shows more variance (S = 1.50--1.99) reflecting its different internal coupling structure.

**Test 2: Monte Carlo Null Distribution.** 10,000 simulations with independent lognormal parts establish the null: open (unclosed) mean S = 0.57, 95th percentile = 1.26, maximum S = 1.94. The closure boost factor for cross-group log-ratios is exactly 1.00×. This is not a surprise---it is Aitchison's theorem: log-ratios ln(xᵢ/xⱼ) are invariant to closure because the divisor Σxₖ cancels. The "entanglement" does not appear in individual log-ratios; it appears in the correlation structure between combinations of log-ratios---exactly where CHSH looks.

**Test 3: Real vs Null.** All 35 scenarios show S at 3.4σ to 3.8σ above the null distribution (p \< 0.001). This is not closure artefact. This is *process entanglement*---the physical coupling between fossil decline and clean growth that the energy transition creates.

**Test 4: Full Basis Scan.** Scanning all 18,360 cross-group log-ratio configurations on MESSAGEix Net Zero 2050 yields:

  ------------------------------ ----------------- -------------------------------------------
  **Statistic**                  **Value**         **Interpretation**
  Maximum S                      2.2018            Exceeds classical bound of 2
  Configurations with S \> 2     12.31%            2,260 of 18,360 violate classical bound
  Configurations with S \> 2√2   0.00%             None exceed Tsirelson bound
  Mean S across all configs      1.9195            System-wide coupling near classical limit
  Best basis: a                  ln(Gas/Nuclear)   Gas as crossover pivot
  Best basis: a′                 ln(Gas/Biomass)   Gas bridges fossil/clean boundary
  Best basis: b                  ln(Gas/Hydro)     Hydro as stable clean reference
  Best basis: b′                 ln(Oil/Nuclear)   Oil--Nuclear substitution axis
  ------------------------------ ----------------- -------------------------------------------

*Table 4. Full basis scan results for MESSAGEix Net Zero 2050. S = 2.20 confirms that the compositional energy system operates in the quantum-analogue regime---between the classical bound and Tsirelson's bound.*

7.3 The Gas Pivot: Crossover Frequency of the Energy Transition

Every top CHSH configuration involves Gas. This is not accidental. Gas sits at the boundary between fossil and clean subcompositions: it is a fossil fuel whose role in the transition is to *bridge* the gap as coal retires and renewables scale. In HUF's audio language, Gas is the **crossover frequency**---the point where the tweeter (fast-responding renewables) and woofer (slow-declining fossil) share energy. In quantum terms, Gas is the **entangling gate**: the part whose behaviour couples the two subcompositions, creating correlations that exceed what closure alone can produce.

The Bell test identifies this quantitatively. The variation matrix already showed Solar↔Wind coupling (V=0.154). The CHSH test adds a new dimension: it identifies *cross-group* coupling and locates its pivot. Standard CoDa tools (variation matrix, ILR) characterise within-group structure. The Bell test characterises **between-group entanglement**---a new diagnostic that neither CoDa nor quantum information theory had separately.

7.4 What the Bell Test Means for CoDa

The compositional Bell test is not a metaphor. It is a calculable quantity on real data that cleanly separates two effects no existing CoDa tool separates: (1) structural correlation from the simplex constraint, and (2) process correlation from genuine physical coupling between subcompositions. The closure boost factor of 1.00× for log-ratios confirms Aitchison's subcompositional coherence theorem. The S \> 2 violation at 12.31% of configurations confirms that NGFS energy compositions carry process entanglement beyond structural necessity. The Bell test gives CoDa practitioners a new diagnostic category: **cross-group entanglement strength.**

8. Spooky Action at a Distance: Hidden Variables Reinterpreted

Einstein's discomfort with quantum entanglement---"spooky action at a distance"---rested on the intuition that if measuring particle A instantaneously determines the state of distant particle B, then either information travels faster than light, or there are hidden variables that pre-determined both outcomes. Bell's theorem (1964) ruled out the hidden-variable option for quantum mechanics. The consensus since then: entanglement is genuinely nonlocal.

HUF offers a third interpretation---not as a replacement for quantum mechanics, but as a structural insight into *why the mathematics works the way it does.*

8.1 The Constraint IS the Entanglement

The Hilbert space norm Σ\|ψᵢ\|² = 1 and the simplex constraint Σxᵢ = 1 are mathematically homomorphic normalisation conditions. In both cases, fixing one component's value automatically constrains all others. This is not information transmission---it is **constraint propagation.** When you measure Coal's share of the energy mix, you have not "sent a signal" to Solar. You have *used up part of the budget,* and the remaining budget must accommodate the other parts.

Bell's hidden variable would be a pre-determined label attached to each particle. The simplex/Hilbert constraint is not a hidden variable in this sense---it is a **structural condition** that creates the appearance of nonlocal correlation without any signal, hidden or otherwise. The "hidden variable" is the constraint itself: the norm, the closure, the boundary condition. It was never hidden---it was just being ignored. This is precisely Isomorphism III: partial trace over hidden constraints.

8.2 Higher Dimensions, Not Spooky Physics

Viewed through HUF, the apparent spookiness dissolves into geometry. A D-part composition lives on a (D−1)-dimensional simplex embedded in D-dimensional Euclidean space. The constraint removes one degree of freedom. From inside the simplex, the correlation between parts *looks like* action at a distance. From outside---in the full D-dimensional space---it is simply the projection onto a submanifold.

Quantum entanglement works the same way. A two-qubit system lives in a 4-dimensional Hilbert space. The tensor product structure means that marginalising over one qubit projects onto a 2-dimensional subspace. The correlations that "spookily" link the two qubits are a consequence of living on a constrained manifold---the unit sphere in 4D---and projecting down. No signal is transmitted. The "distance" that troubled Einstein is an artefact of the embedding. The physics lives on the constraint surface, where everything is local.

This is not a hidden variable theory. It does not violate Bell's theorem. It is *consistent* with Bell's result: the constraint cannot be decomposed into local hidden variables precisely because it is a **global topological property** of the manifold. The simplex cannot be decomposed into independent parts---that is what closure means. The unit sphere cannot be decomposed into independent qubit states---that is what entanglement means. The mathematics is the same. The spookiness is relativistic only if you insist on the embedding space; on the constraint surface, it is geometry.

9. HUF-QTM: A Quantum Toolkit for Compositional Data

The correspondence is not merely theoretical. It suggests concrete tools that CoDa can import from quantum information theory, and tools that quantum information can import from CoDa. We propose HUF-QTM---the quantum module of the Higgins Unity Framework.

9.1 Quantum Tools for CoDa

  ---------------------------- -------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------
  **Quantum Tool**             **CoDa Analogue**                                        **What It Gives CoDa**
  Von Neumann Entropy S(ρ)     Shannon entropy on simplex H(x)                          EITT validation framework; maps to quantum channel capacity theory
  Entanglement Entropy         Cross-group mutual information between subcompositions   Quantifies total fossil↔clean coupling beyond variation matrix (pairwise)
  Bell/CHSH Inequality         Compositional Bell Test (this paper, Section 7)          Separates structural from process entanglement; locates coupling pivots
  Leggett--Garg Inequality     Temporal compositional Bell test on single time series   Tests whether composition at t₁ constrains composition at t₂ (temporal entanglement); direct link to EITT
  GHZ Test                     Three-subcomposition consistency check                   Tests whether fossil/clean/other subdivisions maintain tripartite coherence
  Quantum Error Correction     Compositional error detection (HUF T6c carrier gate)     Identifies data violating simplex constraint; fake-simplex detection; stabiliser-code structure for diagnostic redundancy
  Quantum State Tomography     Full compositional profiling from partial observations   Reconstruct full composition from incomplete measurement (missing carriers); analogous to density matrix reconstruction from POVM outcomes
  Tensor Networks              Hierarchical SBP decomposition                           Matrix Product State structure for multi-scale compositional analysis; tree tensor = SBP tree
  Decoherence Rate             RT60 / ETC (Energy Time Constant)                        Theory for how quickly transitions become irreversible as function of active carrier count (Relaño's N-dependence)
  Quantum Mutual Information   Aitchison inner product between subcompositions          Measures total correlation (classical + quantum) between subsystems; basis-independent coupling metric
  ---------------------------- -------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------

*Table 5. HUF-QTM toolkit: quantum information tools mapped to CoDa applications. Each has a concrete implementation path using existing CoDa mathematics.*

9.2 CoDa Tools for Quantum Information

The correspondence runs both ways. Born rule outputs---measurement outcome probabilities from quantum state tomography---are naturally compositional: they sum to 1. Every POVM measurement produces a composition on the outcome simplex. Quantum process tomography's transition probability matrices are compositional by definition. The quantum information community currently analyses these with maximum-likelihood estimation and Bayesian methods. CoDa offers:

**Aitchison geometry** for measurement outcome spaces, replacing ad hoc distance metrics with the unique geometry respecting the probability simplex. **ILR balances** for identifying which measurement outcomes carry independent information (pointer states in the measurement basis). **EITT** for testing whether quantum processes preserve information under temporal subsampling---a new diagnostic for quantum channel unitarity. **Subcompositional coherence** for verifying that partial tomography is consistent with full tomography---the quantum no-go theorem as a practical diagnostic.

The question is not only "who in quantum needs CoDa tools?" but "who in CoDa needs quantum tools?" The answer: everyone who works with compositions that have structured internal coupling---energy systems, geochemistry, microbiomes, portfolio allocation. The Bell test is the proof of concept. HUF-QTM is the toolkit.

9.3 What Data Can Be Tested

Monte Carlo simulation and ANOVA are now legitimate on compositional data---provided they operate in Aitchison geometry. Data is data: once the simplex constraint is respected, standard statistical machinery applies. The Bell test's Monte Carlo null distribution (Section 7.2) demonstrates this directly: 10,000 simulations, proper closure, proper log-ratio computation, proper null hypothesis testing. No special quantum data is required. The structural isomorphism means that any compositional dataset with subgroup structure can be Bell-tested.

Open quantum datasets do exist for cross-validation: quantum state tomography outcome frequencies (naturally compositional), quantum process tomography transition matrices, and entangled-state benchmark datasets from the quantum machine learning community. These provide a direct test: apply CoDa diagnostics to quantum measurement data and verify that the isomorphisms hold empirically on quantum substrates, not just classical compositions. The bridge is bidirectional.

10. HUF-QTM Empirical Results: Five Tools on NGFS Phase 4

We applied the five HUF-QTM tools to all 35 NGFS Phase 4 world-level scenarios. These are, to our knowledge, the first applications of quantum information diagnostics to compositional data. Full results are reported in the companion document; key findings are summarised here.

10.1 Entanglement Entropy: One Degree of Freedom

The von Neumann entropy of the CLR density matrix ranges from S/Sₘₐₓ = 0.007 to 0.168 across all scenarios, yielding effective dimensionality of 1.02 to 1.45 out of 9 parts. The energy transition, across all carriers and all models, operates on essentially **one effective degree of freedom.** The fossil subsystem entropy is near zero (S = 0.007 for GCAM Net Zero; maximum possible = 1.099)---Coal, Gas, and Oil move as a perfectly correlated block. The clean subsystem shows more internal structure (S = 0.232), but still far below its maximum of 1.792. REMIND shows the highest entanglement entropy; MESSAGEix the lowest.

10.2 Leggett--Garg: Temporal Entanglement

28 of 35 scenarios violate the Leggett--Garg inequality (K₃ \> 1), confirming that the composition at time t₁ constrains the composition at t₃ beyond what classical macrorealism permits. The crossing times---when fossil/clean balance inverts---are physically meaningful: REMIND Net Zero crosses at 2050, GCAM at 2065, MESSAGEix at 2075. Current Policies scenarios never cross. This is temporal decoherence made observable: once enough infrastructure is committed, the composition's future is structurally determined.

10.3 Schmidt Decomposition: The Single Transfer Channel

Every scenario shows Schmidt rank 1---a pure product state in the fossil∣clean bipartition. The dominant fossil mode is equal-weight (−0.578, −0.578, −0.578): all three fossil carriers decline uniformly. The dominant clean mode is near-equal across all six clean carriers (+0.408 to +0.410). The entire 9-part energy transition reduces to a **single fossil→clean transfer channel.** In audio terms: the crossover network has one pole. The implication is profound: despite 9 carriers, 7 scenarios, and 3 models, the compositional dynamics are one-dimensional.

10.4 GHZ Tripartite: Bridge Carrier Independence

The Mermin quantity M₃ = 0.06 across all scenarios (well below the classical bound of 2), so no Mermin violation occurs. However, the tripartite residual---measuring genuine three-body correlation that pairwise analysis misses---reaches −0.84 for GCAM Net Zero and −1.00 for GCAM Low Demand. In these scenarios, the Bridge group (Nuclear, Hydro, Biomass) **decouples from the Fossil↔Renewable axis.** This is the first quantitative evidence that "bridge fuel" carriers have genuine compositional independence under aggressive transition scenarios---they are not interpolating between fossil and clean but operating on their own dynamics.

10.5 Quantum Fidelity: Who Sees the Same System?

Mean fidelity across all 595 scenario pairs is F = 0.946. Cross-model fidelity reveals that Net Zero (F = 0.988) produces the most coherent inter-model agreement; Fragmented World (F = 0.898) the least. The most distinguishable pair in the entire dataset: MESSAGEix Nationally Determined vs REMIND Fragmented World (F = 0.777). GCAM and MESSAGEix have tight internal fidelity (F \> 0.97 across their own scenarios); REMIND shows genuine spread (F = 0.925). The fidelity matrix answers a question no existing CoDa tool addresses: *do different observers see the same compositional structure, or different ones?*

11. Cross-Domain Application: Financial Compositions

The HUF-QTM toolkit is domain-agnostic because the mathematics is domain-agnostic. Any system where variables are constrained to sum to a constant---portfolio weights, electoral vote shares, geochemical abundances, microbiome relative abundances, market share data---lives on a simplex and is amenable to all five tools.

11.1 Portfolio Allocation as Composition

Financial portfolio allocation is a composition: Σwᵢ = 1, where wᵢ are asset weights. Modern Portfolio Theory (Markowitz 1952) computes correlations between asset returns in absolute units, ignoring the simplex constraint on weights. This is precisely the unclosed CoDa error---and it produces the same spurious correlations that Aitchison identified in 1986. The HUF-QTM tools offer:

**Bell test:** separates structural correlation (assets must sum to 100% of capital) from process correlation (genuine economic coupling between sectors). When S \> 2, the portfolio has real cross-sector entanglement.

**Schmidt decomposition:** reveals how many independent risk modes a portfolio actually has---likely 3--5 rather than the hundreds of individual assets.

**Leggett--Garg:** tests whether portfolio composition at Q1 constrains Q3 beyond classical independence---the structural basis for momentum and mean-reversion.

**Entanglement entropy:** measures total systemic coupling. High S/Sₘₐₓ = systemic risk. Low S/Sₘₐₓ = genuine diversification.

**Fidelity matrix:** compares whether different fund managers, indices, or allocation strategies see the same market structure or genuinely different compositional states.

11.2 Boundary: Observation, Not Optimisation

The open-loop doctrine applies with particular force in financial applications. HUF-QTM tools *observe* compositional structure; they do not optimise portfolios, execute trades, or generate signals. The instrument reads; the human decides; the loop stays open. The simplex provides polynomial-dimensional constraint propagation, not exponential quantum computation. These tools cannot break encryption, gain computational speedup, or replace quantitative trading algorithms. They can reveal structural entanglement that conventional analysis misses---which is diagnostic power, not predictive power.

12. Implications for CoDa Theory

12.1 A Physics-Grade Calibration Certificate

CoDa's existing foundation is algebraic. The quantum correspondence adds a *physical interpretation* layer:

  ------------------------------------------ ------------------------------------------------- ---------------------------------------------------
  **CoDa Algebraic Fact**                    **Quantum Interpretation**                        **HUF Audio Origin**
  Closure is a linear projection             Partial trace over hidden degrees of freedom      Cabinet wall between cavity and radiation
  Aitchison distance is an inner product     Distinguishability after tracing out constraint   Spectral distance between two radiation patterns
  Perturbation is group operation on Sᴰ      Non-contact orthogonal injection                  Acoustic forcing through enclosure boundary
  ILR balances are orthonormal coordinates   Pointer states selected by einselection           SBP crossover: drivers grouped by group delay
  EITT: entropy preserved under decimation   Unitarity: information never lost                 Winding ratio: power conserved across transformer
  Subcompositional incoherence               No-go theorem violation                           Driver phase cancellation at crossover
  Zero replacement                           Measurement precision boundary                    Noise floor of the measurement instrument
  Isotropic barycenter (1/D,...,1/D)        Quantum vacuum / ground state                     Isotropic radiator: uniform sphere radiation
  **Bell test S \> 2**                       **CHSH violation = entanglement**                 **Cross-group coupling beyond crossover**
  ------------------------------------------ ------------------------------------------------- ---------------------------------------------------

*Table 6. Triple mapping expanded: CoDa algebra, quantum physics, and HUF audio engineering. The Bell test result (highlighted) is the new empirical entry, confirmed on NGFS Phase 4 data.*

13. Boundary Statement

This correspondence is **structural, not physical.** We do not claim that compositions are quantum systems or that the simplex is a Hilbert space. The claim is narrower: the mathematical structure of the observer problem---hidden constraints producing apparent artefacts when ignored---is identical in both domains.

HUF remains an open-loop diagnostic instrument. The ADAC fork---the architectural decision between observation (HUF-GOV) and control (HUF-CLS)---stays on the observation side. The instrument reads; the human decides; the loop stays open. The quantum correspondence gives the stethoscope a physics-grade calibration certificate. It explains *why* HUF works by showing that its core operations mirror operations with deep physical foundations. But it does not change what HUF does: observe compositional trajectories, not optimise them.

The Section 8 reinterpretation of "spooky action" as constraint propagation does not challenge Bell's theorem---it is *consistent* with Bell's result. The simplex constraint cannot be decomposed into local independent variables, which is precisely what Bell proved for quantum entanglement. The insight is not that Bell was wrong, but that the mathematics of why he was right is the same mathematics of why closure creates spurious correlations. Both are global topological properties of constrained manifolds.

The correspondence also respects the pre-existing condition (ONTO-001): HUF does not create ratio-state systems; they already exist. The simplex is there before measurement begins. Neither creates the physics. Both reveal the structure.

14. Conclusion

The decoherence framework for Wigner's friend experiments and the Higgins Unity Framework share an identical structural core: both are theories of what happens when an observer ignores a constraint. In quantum mechanics, ignoring the environment produces apparent collapse. In CoDa, ignoring the simplex produces spurious correlation. In loudspeaker engineering, ignoring the cabinet wall produces a diffraction anomaly. All are resolved by the same move---accounting for the traced-out degrees of freedom.

We have established nine formal isomorphisms that preserve this structure across three domains. We have confirmed the correspondence empirically with a compositional Bell inequality test on NGFS Phase 4 data: S = 2.20 on MESSAGEix Net Zero 2050, exceeding the classical bound and demonstrating process entanglement at p \< 0.001 across all 35 scenarios. The violation is Gas-centred---the crossover carrier acts as the entangling gate.

The most consequential implication may be Isomorphism IV: EITT as unitarity. If EITT is the compositional analogue of quantum unitarity, then it is not merely a useful diagnostic---it is the *fundamental conservation law* of compositional systems, and its violation signals that data is not genuinely compositional in the same way that non-unitarity signals that physics is not genuinely quantum.

HUF-QTM provides the toolkit: Bell tests for cross-group entanglement, Leggett--Garg for temporal entanglement, entanglement entropy for total coupling, quantum error correction for diagnostic redundancy, and tensor networks for multi-scale decomposition. The bridge is bidirectional: CoDa offers quantum information Aitchison geometry, ILR pointer-state identification, EITT channel diagnostics, and subcompositional coherence testing.

For the CoDa community: the tools you have built over four decades are not merely algebraically convenient---they are the unique correct tools for constrained observation, just as quantum mechanics is the unique correct framework for constrained physical measurement. The Bell test proves it empirically.

The simplex is not a nuisance. It is the entangling gate.

**EITT**

*Explain It To Them.*

References

[1] A. Relaño, "Decoherence framework for Wigner's friend experiments," arXiv:1908.09737v2, 2020.

[2] D. Frauchiger and R. Renner, "Quantum theory cannot consistently describe the use of itself," Nat. Comm. 9, 3711, 2018.

[3] C. Brukner, "A no-go theorem for observer-independent facts," Entropy 20, 350, 2018.

[4] W. H. Zurek, "Decoherence, einselection, and the quantum origins of the classical," Rev. Mod. Phys. 75, 715, 2003.

[5] J. Aitchison, "The Statistical Analysis of Compositional Data," Chapman & Hall, London, 1986.

[6] J. J. Egozcue et al., "Isometric logratio transformations for compositional data analysis," Math. Geol. 35(3), 279--300, 2003.

[7] V. Pawlowsky-Glahn and A. Buccianti (eds.), "Compositional Data Analysis: Theory and Applications," Wiley, 2011.

[8] M. Greenacre, "Compositional Data Analysis in Practice," CRC Press, 2018.

[9] P. Higgins, "HUF: Higgins Unity Framework for Compositional Diagnostics," Rogue Wave Audio Working Paper, 2026.

[10] NGFS Phase 4, "Climate Scenarios for Central Banks and Supervisors," V4.0 IAM Data, 2024.

[11] P. Higgins, "EITT: Entropy-Invariant Time Transformer," Rogue Wave Audio Working Paper, 2026.

[12] J. S. Bell, "On the Einstein Podolsky Rosen paradox," Physics Physique Fizika 1(3), 195--200, 1964.

[13] J. F. Clauser, M. A. Horne, A. Shimony, R. A. Holt, "Proposed experiment to test local hidden-variable theories," Phys. Rev. Lett. 23(15), 880--884, 1969.

[14] B. S. Cirel'son, "Quantum generalizations of Bell's inequality," Lett. Math. Phys. 4, 93--98, 1980.

[15] A. J. Leggett and A. Garg, "Quantum mechanics versus macroscopic realism," Phys. Rev. Lett. 54(9), 857--860, 1985.

[16] D. M. Greenberger, M. A. Horne, A. Zeilinger, "Going beyond Bell's theorem," in *Bell's Theorem, Quantum Theory and Conceptions of the Universe*, Kluwer, 1989.

[17] R. Landauer, "Irreversibility and heat generation in the computing process," IBM J. Res. Dev. 5(3), 183--191, 1961.

[18] B. Coecke and R. Duncan, "Interacting quantum observables: categorical algebra and diagrammatics," New J. Phys. 13, 043016, 2011.

[19] R. Orús, "Tensor networks for complex quantum systems," Nat. Rev. Phys. 1, 538--550, 2019.
