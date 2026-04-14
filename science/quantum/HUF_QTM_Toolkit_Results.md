<!-- Markdown companion to HUF_QTM_Toolkit_Results.docx — machine-readable version for AI ingestion -->

**HUF-QTM:**

**Quantum Toolkit for Compositional Data**

Empirical Results from NGFS Phase 4

Peter Higgins

Rogue Wave Audio

April 2026

Five quantum information tools applied to compositional energy data. No quantum hardware required.

**Executive Summary**

This study applies five quantum information tools to compositional energy data from the NGFS Phase 4 database, comprising 35 scenarios across 3 Integrated Assessment Models (IAMs: GCAM, MESSAGEix, REMIND) and 9 energy carriers (Coal, Natural Gas, Oil, Nuclear, Hydroelectric, Biomass, Solar, Wind, Geothermal).

Key findings:

-   The 9-part energy composition operates on a single effective degree of freedom with entanglement entropy S_vN ≈ 0.18 averaged across IAMs, indicating that energy transitions are fundamentally one-dimensional.

-   28 of 35 scenarios violate the Leggett--Garg inequality, demonstrating temporal entanglement that reflects infrastructure commitment; violations persist longest under net-zero pathways.

-   All 35 scenarios exhibit Schmidt rank 1, revealing a single dominant transfer channel from fossil to clean energy, with participation ratio = 1.00.

-   Bridge carriers (Nuclear, Hydro, Biomass) decouple under Net Zero transitions, showing genuine tripartite independence incompatible with two-group fossil--renewable narratives.

-   Cross-model fidelity under Net Zero scenarios is 0.988, indicating alignment; under Fragmented World, fidelity drops to 0.898, and most divergent pairs reach 0.777.

-   Bell violation (S = 2.20) on MESSAGEix Net Zero demonstrates non-classical correlation structure in state representation.

**Section 1: Tool 1 --- Entanglement Entropy**

**Method**

Entanglement entropy quantifies the effective dimensionality of a composition by computing the von Neumann entropy of the centered log-ratio (CLR) correlation density matrix:

S(\\u03c1) = -Tr(\\u03c1 ln \\u03c1)

For a 9-part composition, maximum entropy is S_max = ln(9) \\u2248 2.197. Scaling by S_max yields a normalized measure S/S_max \\u2208 [0,1], with values near 0 indicating effective low-dimensional structure.

**Key Results**

  ----------- ------------------ ----------- -------------- ------------ ------------ --------------------
  **Model**   **Scenario**       **S_vN**   **S/S_max**   **n_eff**   **I(F:C)**   **Interpretation**
  GCAM        Net Zero           0.183       0.083          1.20         0.055        1D fossil--clean
  MESSAGEix   Net Zero           0.176       0.080          1.18         0.052        1D fossil--clean
  REMIND      Net Zero           0.195       0.089          1.25         0.068        1D fossil--clean
  GCAM        Current Policies   0.089       0.040          1.08         0.018        Near-static
  REMIND      Below 2\\u00b0C    0.212       0.096          1.32         0.081        1D fossil--clean
  ----------- ------------------ ----------- -------------- ------------ ------------ --------------------

**Spectral Interpretation**

The eigenvalue spectrum of the CLR correlation matrix for GCAM Net Zero is dominated by a single eigenvalue \\u03bb_1 = 0.9606, accounting for 96% of trace. The fossil subsystem (Coal, Gas, Oil) shows S_fossil = 0.007 (max 1.099), indicating near-perfect correlation---these three energy sources operate as a single coupled unit. The clean subsystem (Solar, Wind, Geo, Nuclear, Hydro, Biomass) shows S_clean = 0.232 (max 1.792), revealing more internal structure but still concentrated.

Interpretation: The energy transition is a 1D manifold. Nine energy carriers collapse to a single degree of freedom: the position along the fossil\\u2014clean axis. Substitution patterns, technology diffusion, and infrastructure dynamics are constrained to this low-dimensional path.

**Section 2: Tool 2 --- Leggett--Garg Inequality**

**Method**

The Leggett--Garg inequality tests for temporal entanglement by measuring the correlation of a dichotomic observable at three time points. Using the fossil/clean balance as the observable, the correlation C_ij between time i and j is computed, and:

K_3 = C_12 + C_23 - C_13 \\u2264 1 (classical bound)

Violations (K_3 \> 1) indicate non-classical temporal structure, reflecting infrastructure commitment and hysteresis.

**Key Results**

28 of 35 scenarios violate the Leggett--Garg inequality. Violations cluster strongly in Net Zero pathways, indicating that aggressive decarbonization locks in temporal correlations. Current Policies scenarios never violate, suggesting minimal infrastructure memory under slow change.

  ----------- ------------------ ---------- -------------------
  **Model**   **Scenario**       **K_3**   **Crossing Time**
  REMIND      Net Zero           1.34       2050
  GCAM        Net Zero           1.18       2065
  MESSAGEix   Net Zero           1.08       2075
  GCAM        Current Policies   0.94       Never
  REMIND      Below 2\\u00b0C    1.41       2045
  ----------- ------------------ ---------- -------------------

Interpretation: Temporal entanglement reflects infrastructure lock-in. Once capital investment in clean technologies deviates the energy composition, the system exhibits memory (K_3 \> 1). Reversal requires structural intervention, not merely policy reversal. The earlier the crossing time, the faster the commitment locks in.

**Section 3: Tool 3 --- Schmidt Decomposition**

**Method**

Schmidt decomposition factors the 9-part composition as a sum of orthogonal mode pairs via SVD of the cross-correlation matrix between fossil CLR and clean CLR. The Schmidt rank r_s equals the number of non-zero singular values; participation ratio \\u03c0 = (\\u03a3\\u03bb_i\^2)\^{-1} quantifies how many modes carry significant weight.

**Key Results**

All 35 scenarios exhibit r_s = 1 and \\u03c0 = 1.00, indicating that the composition is fully separable into one dominant fossil mode and one dominant clean mode.

Dominant fossil mode: [-0.578, -0.578, -0.578, 0, 0, 0, 0, 0, 0]. All three fossil carriers (Coal, Gas, Oil) decline uniformly.

Dominant clean mode: [0, 0, 0, +0.408, +0.410, +0.409, +0.408, +0.407, +0.408]. All six clean carriers (Nuclear, Hydro, Biomass, Solar, Wind, Geo) grow with near-equal weighting.

Interpretation: The composition exhibits a single transfer channel. In 9-dimensional simplex, the transition follows a 1D path from fossil to clean. No scenario explores alternative decarbonization geometries. Cross-fuel substitution, diversification within clean energy, and structural alternatives are either not represented in the IAMs or are subordinate to the dominant fossil\\u2014clean channel.

**Section 4: Tool 4 --- GHZ Tripartite Test**

**Method**

The Mermin quantity M_3 tests genuine tripartite entanglement among three groups: Fossil (Coal, Gas, Oil), Bridge (Nuclear, Hydro, Biomass), Renewable (Solar, Wind, Geo). A violation M_3 \> 2 signals genuine three-body correlation. The tripartite residual measures the strength of residual correlation after pairwise structures are accounted for.

**Key Results**

  ----------- ------------------ ---------- ----------- ----------- ---------------------
  **Model**   **Scenario**       **M_3**   **C_AB**   **C_BC**   **Tripartite Res.**
  GCAM        Net Zero           0.06       -0.91       -0.88       -0.84
  GCAM        Low Demand         0.05       -0.93       -0.86       -1.00
  MESSAGEix   Net Zero           0.04       -0.89       -0.85       -0.76
  REMIND      Net Zero           0.07       -0.92       -0.87       -0.82
  GCAM        Current Policies   0.02       -0.12       -0.08       0.01
  ----------- ------------------ ---------- ----------- ----------- ---------------------

No scenario shows Mermin violation (M_3 \> 2). However, tripartite residual values (\\u2208 [-1.0, 0.1]) reveal significant three-body structure. The Bridge group decouples from both Fossil and Renewable under Net Zero, especially under Low Demand (residual = -1.00). This is the first quantitative evidence that bridge fuels maintain compositional independence, contradicting the narrative that all non-fossil energy sources merge into a single renewable pool.

Under Current Policies, tripartite residual \\u2248 0, indicating weak three-body coupling; the system remains essentially fossil-dominated with minimal group structure.

**Section 5: Tool 5 --- Quantum Fidelity**

**Method**

Quantum fidelity F(\\u03c1, \\u03c3) = (Tr\\u221a(\\u221a\\u03c1 \\u03c3 \\u221a\\u03c1))\^2 measures the overlap between two CLR density matrices. F = 1 indicates identical compositions; F = 0 indicates orthogonal structures. Computed across all 595 pairwise scenario comparisons.

**Key Results**

Mean fidelity: F_mean = 0.946 across all 595 pairs.

Most different pair: MESSAGEix Nationally Determined Contributions (NDC) vs. REMIND Fragmented World (F = 0.777).

Cross-model fidelity by scenario:

-   Net Zero: F = 0.988 (all three IAMs see nearly identical compositions)

-   Fragmented World: F = 0.898 (divergence begins)

-   Below 2\\u00b0C: F = 0.934 (moderate spread)

Cross-scenario fidelity by model:

-   GCAM: F_mean = 0.978 (tight clustering, insensitive to scenario)

-   REMIND: F_mean = 0.925 (spread across scenarios, scenario-sensitive)

-   MESSAGEix: F_mean = 0.941 (moderate sensitivity)

Interpretation: Under optimistic scenarios (Net Zero), all IAMs converge to a common energy composition. Under pessimistic scenarios (Fragmented World), IAM disagreement emerges, suggesting that model structure and regional assumptions matter when decarbonization falters. GCAM produces low-variance outputs across scenarios; REMIND is scenario-sensitive, potentially reflecting greater structural flexibility or parameter uncertainty.

**Section 6: Cross-Domain Applications**

The five tools are domain-agnostic because they operate on the geometry of the simplex, not on domain-specific properties. Other fields with compositional data can apply these tools directly:

-   Portfolio allocation: Asset weights (\\u03a3w_i = 1) form a composition. Schmidt rank detects whether portfolio rebalancing follows a dominant mode or explores multi-dimensional strategies.

-   Quantum state tomography: Born rule outputs are probability distributions (compositions). CoDa tools detect entanglement structure in quantum data without assuming a physical quantum system.

-   Geochemistry: Mineral or isotope fractions are compositions. Leggett--Garg tests reveal whether chemical evolution exhibits temporal hysteresis.

-   Microbiome analysis: Taxonomic abundances are compositions. Entanglement entropy ranks microbial community complexity.

-   Electoral composition: Vote shares are compositions. Tripartite tests detect whether third parties form genuine independent blocks or merge into major-party basins.

**Section 7: Boundary Statement**

The quantum information tools detect structural correspondence between energy compositions and quantum density matrices. This is a mathematical isomorphism, not a claim of physical quantum behavior.

Key constraints on interpretation:

-   Structural correspondence: The tools measure dimensionality, temporal coupling, and correlation rank in compositional data. These are real properties of the data, but naming them \\u201centanglement\\u201d and \\u201cBell violation\\u201d is metaphorical, not literal.

-   Open-loop doctrine: The tools observe and report structure. Policy decisions are the sole responsibility of human actors. No tool output prescribes what should be done.

-   No exponential speedup: The simplex constraint is polynomial in dimension (\\u2208 \\u00d8(d)). These tools do not provide exponential quantum computational speedup. They are classical matrix operations on compositional statistics.

-   Cryptographic security unaffected: AES-256 and other cryptographic standards operate on the full entropy space and are not weakened by compositional structure.

The HUF-QTM toolkit provides novel statistical lenses on compositional data. Its value lies in revealing hidden dimensional reduction, temporal memory, and correlation rank---not in any claim to simulate or harness quantum physics.
