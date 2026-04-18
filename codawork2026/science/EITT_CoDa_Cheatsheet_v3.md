# EITT + CoDa: Complete Study & Position Sheet

Peter Higgins | Rogue Wave Audio | CoDaWork 2026, Coimbra | April 2026

*Markdown companion to EITT_CoDa_Cheatsheet_v3.pdf — identical content, machine-readable format.*

---

## 1. Glossary of Terms — Grouped by Origin

### CoDa Standard Terms (Aitchison, Egozcue, Pawlowsky-Glahn et al.)

*These are established terms from the Compositional Data Analysis literature. HUF did not invent them.*

| Term | Symbol / Formula | What It Means |
|---|---|---|
| Aitchison distance | d_A(x,y) = ‖clr(x)-clr(y)‖₂ | The natural ruler on the simplex. Measures how different two compositions are in log-ratio space. |
| Aitchison geometry | (S^D, ⊕, ⊙, ⟨,⟩_A) | The Hilbert space structure of the simplex: perturbation, powering, inner product. |
| Aitchison norm | ‖x‖_A = d_A(x, n) | Distance from the uniform composition. Measures concentration. |
| ALR (Additive Log-Ratio) | alr(x)_i = ln(x_i/x_D) | All parts vs one reference. Simple but NOT isometric. Depends on which part chosen. |
| Balance (ILR coordinate) | y_k = sqrt(rs/(r+s)) ln(g(G+)/g(G-)) | A single ILR coordinate. Normalised log-ratio of geometric means of two groups. |
| CLR (Centered Log-Ratio) | clr(x)_i = ln(x_i/g(x)) | Each part vs geometric mean of all. Symmetric but singular (D values, D-1 dims). |
| Closure | C(z) = (z_i/Σz_j) | Force any vector to sum to 1 (or κ). The gate onto the simplex. |
| CoDa | Compositional Data Analysis | The field. Parts of a whole. Founded by Aitchison (1986). |
| Composition | x = (x₁,...,x_D) in S^D | D positive numbers summing to 1. One point on the simplex. |
| Fréchet mean | x̄ = argmin Σ d_A(x,x(t))² | The "average" minimising total Aitchison distance. = geometric mean on the simplex. |
| Geometric mean (of comps) | x̄_G = C(∏ x_i(t)^(1/N)) | Per-part geometric mean, re-close. Fréchet mean on the simplex. |
| ILR (Isometric Log-Ratio) | y = Ψᵀ · clr(x) in ℝ^(D-1) | Gold standard transform. Preserves distances, full-rank, unconstrained. |
| Isometry | d_A(x,y) = ‖ilr(x)-ilr(y)‖₂ | ILR preserves Aitchison distances as Euclidean distances. No distortion. |
| Neutral element | n = (1/D, ..., 1/D) | Uniform composition. Max entropy state. "No opinion" on where energy belongs. |
| Pairwise log-ratio | λ_ij = ln(x_i/x_j) | Exchange rate between parts i and j. The fundamental atom of CoDa. |
| Perturbation | x ⊕ p = C(x₁p₁,...,x_Dp_D) | Simplex "addition". Multiply parts by factors, re-close. |
| Powering | α ⊙ x = C(x₁^α,...,x_D^α) | Simplex "scalar multiplication". Amplifies or compresses all contrasts. |
| SBP (Sequential Binary Partition) | Tree of binary splits on D parts | The wiring diagram for ILR balances. Choice does not affect total variance. |
| Shannon entropy | H(x) = −Σ x_i ln x_i | Diversity/evenness. H=0 at monoculture, H=ln(D) at uniform. Standard info theory. |
| Simplex | S^D = {x: x_i>0, Σx_i=1} | The sample space for compositions. A (D-1)-dimensional constrained surface. |
| Subcomposition | x_S = C(x_i : i ∈ S) | Pick subset of parts, re-close. Like looking at only fossil fuels. |
| Subcomp. coherence | Results on sub = results on full | Valid CoDa operations give same answer on any subcomposition. Aitchison has this. |
| Total Aitchison variance | totvar = Σ Var(y_k) | Total spread. = sum of ILR balance variances. SBP-invariant. |

### HUF Terms (Higgins, Rogue Wave Audio — the monitoring framework)

*These are terms introduced by HUF. They use CoDa mathematics but the concepts are new.*

| Term | Symbol / Formula | What It Means |
|---|---|---|
| Adaptive decimation | D_adapt | Variable-width block averaging. d(CoDa)/dt sets the block width. |
| Autocorrelation boundary | 3 tests: lag-1, block var ratio, entropy drift sign | The stationarity check. If these fail, data changes too fast for EITT at that ratio. |
| Balance velocity | v_k(t) = \|dy_k/dt\| | How fast a balance is changing. The derivative of one ILR coordinate. |
| Block decimation | D_M[{x(t)}] = {x̄_G^(b)} | Chop time series into blocks of M, replace each with geometric mean. Core EITT operation. |
| d(CoDa)/dt | V(t) = max_k \|dy_k/dt\| | Max balance velocity across all taps. The tap controller. Determines safe averaging window. |
| Deceptive drift | K_eff drops while TV stays calm | Concentration building behind apparent stability. The silent failure MC-4 detects. |
| EITT | Entropy Invariance under Temporal Transformation | Core finding: Shannon entropy barely changes under geometric-mean decimation. |
| EITT Inversion | K fails → increase K → passes | When EITT fails, increasing K restores it. Failure diagnoses hidden structure. |
| EITT residual | δ_M = [mean H(dec) − mean H(orig)] / mean H(orig) × 100% | % change in mean entropy after decimation. Small = invariance holds. Typically <1%. |
| HUF-GOV | Open-loop governance | Measure, report, file. No intervention. The scientific instrument. Stateless. |
| HUF-CLS | Closed-loop system | Measure, interpret, adjust, re-measure. Feedback. Licensed through RWA. |
| Isotropic Principle | Ground state = (1/D,...,1/D) | The geometry exists before the signal. Every departure from isotropy is a signal. |
| K_eff (effective carriers) | K_eff = exp(H(x)) | How many carriers are "effectively present". = perplexity in NLP, Hill number q=1. |
| MC-4 | Composition Monitoring | The fourth monitoring category (after Magnitude, Identity, Trend). No ISO standard covers it. |
| Multi-tap test | 8 SBP trees × 3 datasets × 3 ratios | Test EITT across ALL valid SBP trees. 94.8% pass. Geometry property, not wiring artefact. |
| TV distance (as diagnostic) | d_TV = 0.5 Σ \|x_i−y_i\| | L1 on raw shares. NOT simplex-native. Used as comparison diagnostic alongside d_A. |

## 2. Key CoDa Theories and Who Produced Them

| Theory / Result | Who | When | What It Established |
|---|---|---|---|
| Log-ratio approach to compositional data | John Aitchison | 1982, 1986 | Founded CoDa. Showed Euclidean statistics on the simplex are invalid. |
| ILR transform and Hilbert space structure | Egozcue, Pawlowsky-Glahn, Mateu-Figueras, Barceló-Vidal | 2003 | Proved the simplex is a Hilbert space. Built the ILR transform. |
| Aitchison inner product and geometry | Pawlowsky-Glahn, Egozcue | 2001 | Formalised the inner product, norm, and distance on the simplex. |
| Textbook: "Modeling and Analysis of CoDa" | Pawlowsky-Glahn, Egozcue, Tolosana-Delgado | 2015 | The definitive reference. Unifies 30 years of CoDa theory. |
| Hill numbers and diversity unification | Hill (1973); Chao, Jost (2012); Chao et al. (2014) | 1973–2014 | K_eff = exp(H) IS Hill number of order 1. Unified diversity indices. |
| Subcompositional coherence principle | Aitchison (1986); Egozcue, Pawlowsky-Glahn (2003) | 1986–2003 | Results must be invariant to which subset of parts you examine. |
| Perturbation algebra on the simplex | Aitchison (1986); Barceló-Vidal, Mateu-Figueras (2001) | 1986–2001 | The simplex forms an Abelian group under perturbation. |
| SBP and balance decomposition | Egozcue, Pawlowsky-Glahn (2005) | 2005 | Any valid binary partition produces D-1 orthonormal balances. |
| Fisher-Rao metric on the simplex | Amari (1985); Erb, Ay (2020) | 1985–2020 | Connects CoDa to information geometry. Chentsov uniqueness theorem. |
| Shannon entropy and information theory | Shannon (1948) | 1948 | H(x) = −Σ x_i ln x_i. EITT says it is near-invariant under CoDa temporal decimation. |

## 3. Formula Reference — Grouped

### CoDa Simplex Operations (standard)

| Operation | Formula | Analogy |
|---|---|---|
| Closure | C(z) = (z_i / Σz_j) | Normalise to 100% |
| Perturbation ⊕ | x ⊕ p = C(x₁p₁, ..., x_Dp_D) | Gain adjustment |
| Pert. difference ⊖ | x ⊖ y = C(x₁/y₁, ..., x_D/y_D) | Compositional first-difference |
| Powering ⊙ | α ⊙ x = C(x₁^α, ..., x_D^α) | Contrast amplifier |
| Geometric mean | g(x) = (∏ x_i)^(1/D) | The CoDa "center" |
| Neutral element | n = (1/D, ..., 1/D) | Flat signal / max entropy |

### CoDa Log-Ratio Transforms (standard)

| Transform | Formula | Dim | Use |
|---|---|---|---|
| CLR | clr(x)_i = ln(x_i/g(x)) | ℝ^D (sing.) | Visualisation, biplots |
| ILR | y = Ψᵀ · clr(x) | ℝ^(D-1) (full) | Formal statistics, gold standard |
| ILR balance | y_k = sqrt(rs/(r+s)) ln(g(G+)/g(G-)) | Scalar | Each tap on the transformer |
| ALR | alr(x)_i = ln(x_i/x_D) | ℝ^(D-1) (not iso) | Quick exploration only |

### HUF / EITT-Specific Formulas (new work)

| Formula | Definition | Status |
|---|---|---|
| Block decimation | D_M: replace each block of M with x̄_G = C(∏ x_i(t)^(1/M)) | Definition |
| CLR identity | clr(x̄_G) = (1/M) Σ clr(x(t)) over block | Mathematical |
| ILR identity | ilr_k(x̄_G) = (1/M) Σ ilr_k(x(t)) over block | Proved (10⁻¹⁶) |
| EITT residual | δ_M = [mean H(dec) − mean H(orig)] / mean H(orig) × 100% | Empirical <2% |
| Hessian footprint | δH ~ (1/2) tr[ \|Hess H\| · Cov(x̄_G) ], Hess_ii = −1/x_i | Approx. bound |
| Balance mean shift | Δȳ_k = mean(ilr_k after D_M) − mean(ilr_k before) | <0.1 at M=2 |
| Balance velocity | v_k(t) = \|y_k(t+1) − y_k(t-1)\| / 2 | Operationalised |
| Max rate (tap controller) | V(t) = max_k v_k(t) | Operationalised |
| Adaptive block width | M(t) = M_max if V(t)≤θ_L; 2 if V(t)≥θ_H; interpolate | Operationalised |

### CoDa / Info Theory Distances (who owns what)

| Metric | Formula | Origin |
|---|---|---|
| Aitchison distance | d_A = ‖clr(x)-clr(y)‖₂ | CoDa (Aitchison) |
| Aitchison inner product | ⟨x,y⟩_A = (1/D) Σ ln(x_i/x_j) ln(y_i/y_j) | CoDa (Pawlowsky-Glahn) |
| Shannon entropy | H(x) = −Σ x_i ln x_i | Info theory (Shannon 1948) |
| K_eff | K_eff = exp(H(x)) | Ecology (Hill 1973) / HUF naming |
| TV distance | d_TV = 0.5 Σ \|x_i−y_i\| | Standard (NOT simplex-native) |
| Total Aitchison variance | totvar = Σ Var(y_k) | CoDa (Egozcue 2003) |

## 4. Results: Three Layers

### Layer 1 — Mathematical (proved to machine precision)

| Result | Statement | Why |
|---|---|---|
| Balance mean preservation | ilr_k(x̄_G) = (1/M) Σ ilr_k(x(t)) exactly | ILR is linear isometry; geom mean = arith mean in CLR |
| SBP invariance | Holds for ALL valid SBP trees simultaneously | Total ILR var = total Aitchison var, independent of SBP |
| Log-ratio means | Mean of ln(x_i/x_j) preserved under decimation | λ_ij = clr_i − clr_j, linear in CLR |
| Variance reduction | Var(y_k) shrinks, ratio is SBP-invariant (spread <0.006) | Block averaging reduces variance; isometry preserves ratios |

### Layer 2 — Empirical (observed, not proved)

| Result | Evidence | Caveat |
|---|---|---|
| \|δ_M\| < 2% at 2:1 | 4 domains, bootstrap CIs, all pass | Requires near-stationarity |
| Multi-tap: 94.8% pass | 213 measurements, 8 SBP trees | Failures = Solar (fast) or Nuclear (break) |
| Subcomp EITT | Fossil, Financial subsets pass | Renewables-only fails (−4.5%) |
| EITT Inversion | K=2 fails, K=4 passes (gold/silver) | Bidirectional: upward + downward confirmed |
| Adaptive decimation | Gold/Silver 10:1: +1.39% fixed → −0.43% adaptive | Adds hyperparameters |
| Rényi generalisation | Confirmed q=0.1 to 5.0, all near-invariant | Shannon is not special. Lives in geometry. |

### Layer 3 — Open Problems (for the CoDa community)

| Problem | Description |
|---|---|
| O-1: Formal bound | Prove \|δ_M\| ≤ f(D, σ_A², ρ₁, M) for stationary processes |
| O-2: Variance decomp | Is the variance reduction factor determined by temporal dependence alone? |
| O-3: Fisher-Rao | Curvature interpretation of EITT residual under Fisher-Rao metric? |
| O-4: Subcomp conditions | When does full-comp EITT imply subcompositional EITT? |
| O-5: Adaptive optimality | Optimal M*(t) minimising \|δ\| subject to compression constraint? |

## 5. Empirical Scorecard

| Domain | D | N | δ 2:1 | 95% CI | Status |
|---|---:|---:|---|---|---|
| Gold/Silver prices | 2 | 339 | +0.085% | [−0.19%, +0.16%] | **PASS** |
| Energy World | 7 | 25 | −0.589% | [−0.97%, +0.20%] | **PASS** |
| Financial (price-level) | 9 | 74 | +0.004% | [+0.004%, +0.006%]* | **PASS*** |
| Energy Germany | 7 | 36 | +0.029% | [−0.12%, +0.09%] | **PASS** |

*Financial CI excludes zero (tiny systematic +0.004% bias). Not market-cap weighted.*

## 6. Honest Disclosures

1. EITT is an empirical observation, NOT a theorem. Formal proof is Open Problem O-1.
2. Geometric-mean superiority over arithmetic mean NOT empirically demonstrated at low compression.
3. Spatial EITT has been RETRACTED (HEALPix NESTED ordering error).
4. Financial = mean closing prices (price-level, K=9), NOT market-cap.
5. d(CoDa)/dt is operationalised but not formally optimised.
6. EITT Inversion: bidirectional confirmed but needs more domains.
7. Adaptive decimation adds hyperparameters; cannot rescue fully non-stationary data.
8. Aitchison distances EXPAND under decimation. EITT is NOT contraction/smoothing.

## 7. Our Position in One Paragraph

Shannon entropy of a compositional time series appears empirically near-invariant under geometric-mean temporal decimation, provided the process is near-stationary. This holds across the full Rényi family (q = 0.1 to 5.0), confirming the phenomenon lives in the Aitchison geometry, not in a special property of Shannon entropy. ILR balance means are exactly preserved (mathematical, not empirical) regardless of SBP tree choice. When the invariance fails, the failure is diagnostic: upward inversion identifies hidden structure, downward inversion identifies non-stationarity. The balance velocity d(CoDa)/dt serves as the control signal that determines the safe compression window. The formal proof bounding the residual in terms of Aitchison variance and temporal dependence is an open problem we bring to the CoDa community.

---

Peter Higgins | Rogue Wave Audio | PeterHiggins@RogueWaveAudio.com | April 2026

All code, data, and test results: github.com/PeterHiggins19/Higgins-Unity-Framework

Multi-AI adversarial review (Claude, ChatGPT, Grok, Gemini, Copilot) applied throughout.
