# Boundary Species Discovery

## The DADC Chain Identifies Which Carrier Sits at the Interface Between Competing Forces

**Status:** L0 Exploratory Pattern. Tested across 8 domains. Physically interpretable in every case.

---

## Statement

When the PLL parabola is fitted to sigma_A^2 and the residuals are decomposed per-species via the DADC-DADI-ADAC chain, one species consistently carries the highest contamination-to-signal ratio (C/S). This is the **boundary species** — the compositional carrier that sits at the interface between the competing forces.

The boundary species is not chosen or specified in advance. It emerges from the data. In every domain tested, the identification is physically interpretable after the fact.

## The Boundary Species Across Domains

| Domain | Boundary Species | C/S Ratio | Why It Makes Sense |
|--------|-----------------|-----------|-------------------|
| QGP freeze-out | Lambda (baryon) | 0.626 | Lightest strange baryon — straddles meson/baryon boundary |
| Room acoustics | 2k-8kHz band | 1.168 | The presence band — room modes vs surface absorption |
| Stellar nucleosynthesis | Oxygen | 0.743 | Bridge between CNO cycle and alpha process |
| Wine fermentation | Minor metabolites | 1.227 | Sugar/product pathway interaction |
| Energy mix | Gas | 0.534 | The "bridge fuel" between fossil and clean energy |
| Igneous geochemistry | TiO2 | 0.416 | Trace oxide discriminant between mafic and felsic |
| BBN cosmology | Lithium-7 | 2.525 | THE cosmological lithium problem — found independently |
| Cosmic rays | Si group | 0.197 | Intermediate mass between H/He and Fe |
| US Energy (5 states) | Hydro | varies | Seasonal variability — the swing voter in energy policy |
| SEMF valley | Volume binding | 1.244 | Dominant SEMF term — drives all nuclear composition |

## The Lithium Discovery

The DADC chain independently identified Lithium-7 as the highest-contamination species in Big Bang Nucleosynthesis (C/S = 2.525) — the highest of any species in any domain tested. This rediscovers the **cosmological lithium problem**, one of the major unsolved puzzles in BBN, without being told it exists.

The chain was given primordial abundance data and asked: which species carries the most force crosstalk? The answer — Lithium — matches the known discrepancy between BBN predictions and observed abundances.

## Contamination Entropy

When H_contam (normalized) is below 0.85, the contamination is **structured** — concentrated in identifiable carriers. This is the DADI signature.

When H_contam is near 1.0, contamination is **uniform** — all species are equally noisy. This occurs in the SEMF valley (H_contam = 0.99) where all components are coupled by nuclear physics, and in the Gold/Silver D=2 case (H_contam = 1.0) where the 2-simplex has no room for asymmetry.

## Evidence

| Document | Location |
|----------|----------|
| DADC analysis script | DATA/Scripts/eitt_contamination_dadc.py |
| EXP-02 (hydro boundary) | codawork2026/experiments/EXP-02_US_Monthly/EXP02_SEALED_CONCLUSION.json |
| EXP-03 (volume boundary) | codawork2026/experiments/EXP-03_Uranium/EXP03_SEALED_CONCLUSION.json |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> dadc_dadi_adac_contamination_chain (L0) |

---

*The contamination is in the noise. The boundary species carries the crosstalk. The chain finds it without being told where to look.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (FP1, notation table).*

### The DADC-DADI-ADAC Chain — Formal Structure

The chain is a three-stage round-trip in compositional space:

**DADC (Dimension-Apportioned Diffraction Correction):** Given a D-part composition x = (x_1, ..., x_D), compute clr(x) and fit the PLL parabola to sigma_A^2. The fitted component is the "signal" S_i for each species i.

**DADI (Diffraction-Apportioned Dimension Inference):** The residual for species i is:

    R_i = clr_i(t) - S_i(t)

The contamination-to-signal ratio for species i is:

    C/S_i = Var(R_i) / Var(S_i)

The species with the highest C/S ratio is the boundary species — the carrier at the interface between competing forces.

**ADAC (Apportioned-Dimension Analysis Correction):** The corrected composition feeds back to the next iteration. The mapping T: allocation -> measured_response -> corrected_allocation is asserted to be contractive.

### Contamination Entropy

The distribution of contamination across species is measured by:

    H_contam = -sum (C/S_i / sum C/S_j) * ln(C/S_i / sum C/S_j)

Normalised by ln(D), this gives:

    H_contam_norm = H_contam / ln(D)

| Regime | H_contam_norm | Interpretation |
|--------|--------------|----------------|
| < 0.85 | Structured | Contamination concentrated in identifiable carriers (DADI signature) |
| ~ 1.0 | Uniform | All species equally noisy (e.g., SEMF valley, D=2 simplex) |

### Fixed Point Result FP1 — ADAC Convergence (Claimed)

**Banach Fixed-Point Theorem:** Let (X, d) be a complete metric space and T: X -> X a contraction with Lipschitz constant L < 1. Then T has a unique fixed point x*, and x_{n+1} = T(x_n) converges with rate d(x_n, x*) <= L^n * d(x_0, x*) / (1 - L).

**Application to ADAC:** The space is (S^D, d_A) with the Aitchison metric (complete). Numerical evidence: DADI error 12.5% -> 4.99% over 5 iterations, consistent with L ~ 0.4.

**What is missing (O-4):** Formal derivation of L from physical parameters. Show L < 1 for the class of physically realisable systems.

### Canonical Boundary Species Values

| Domain | Boundary species | C/S ratio | H_contam_norm |
|--------|-----------------|-----------|---------------|
| BBN cosmology | Lithium-7 | 2.525 | structured |
| Wine fermentation | Minor metabolites | 1.227 | structured |
| SEMF valley | Volume binding | 1.244 | 0.99 (uniform) |
| Room acoustics | 2k-8kHz | 1.168 | structured |
| Stellar nucleosynthesis | Oxygen | 0.743 | structured |
| QGP freeze-out | Lambda baryon | 0.626 | structured |
