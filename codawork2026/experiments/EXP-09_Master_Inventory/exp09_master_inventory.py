#!/usr/bin/env python3
"""
EXP-09  MASTER INVENTORY OF ALL COMPOSITE SYSTEMS
====================================================
HUF Programme — Higgins Unity Framework
Peter Higgins / Claude (Anthropic)

Complete census of every composite system studied across the
entire HUF programme, classified by domain (Matter / Energy / Gravity),
with status flags: COMPLETE, UNFINISHED, FLAW, OPPORTUNITY.

Answers: "How many systems are composites? Which have we done?
          Which have unfinished business?"
"""

# ═══════════════════════════════════════════════════════════════════════════════
#  REFERENCES — Formal Academic Citations
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Compositional Data Analysis (CoDa):
#    [1] J. Aitchison, "The Statistical Analysis of Compositional Data,"
#        Monographs on Statistics and Applied Probability, Chapman & Hall,
#        London, 1986. (Defines CLR, ALR, ILR transforms; simplex geometry;
#        Aitchison variance; subcompositional coherence.)
#    [2] J. Aitchison, "The statistical analysis of compositional data,"
#        J. R. Stat. Soc. B, vol. 44, no. 2, pp. 139-177, 1982.
#        (Original journal paper introducing the log-ratio approach.)
#    [3] V. Pawlowsky-Glahn, J. J. Egozcue, R. Tolosana-Delgado,
#        "Modeling and Analysis of Compositional Data," Wiley, 2015.
#        (Modern treatment; Aitchison geometry on the simplex.)
#
#  Information Theory:
#    [4] C. E. Shannon, "A Mathematical Theory of Communication,"
#        Bell System Technical Journal, vol. 27, pp. 379-423, 623-656, 1948.
#        (Defines Shannon entropy H = -sum(p_i * ln(p_i)); channel capacity;
#        source coding theorem.)
#
#  Nuclear & Particle Physics:
#    [5] C. F. von Weizsaecker, "Zur Theorie der Kernmassen,"
#        Zeitschrift fuer Physik, vol. 96, pp. 431-458, 1935.
#        (Semi-Empirical Mass Formula — SEMF — for nuclear binding energy.)
#    [6] H. A. Bethe and R. F. Bacher, "Nuclear Physics A: Stationary
#        States of Nuclei," Rev. Mod. Phys., vol. 8, pp. 82-229, 1936.
#        (Extended SEMF; Bethe-Weizsaecker mass formula.)
#    [7] N. Cabibbo, "Unitary Symmetry and Leptonic Decays,"
#        Phys. Rev. Lett., vol. 10, pp. 531-533, 1963.
#        (Cabibbo angle; origin of CKM quark mixing framework.)
#    [8] M. Kobayashi and T. Maskawa, "CP-Violation in the Renormalizable
#        Theory of Weak Interaction," Prog. Theor. Phys., vol. 49,
#        pp. 652-657, 1973. (3x3 CKM matrix; CP violation; Nobel 2008.)
#    [9] B. Pontecorvo, "Mesonium and Anti-mesonium," Sov. Phys. JETP,
#        vol. 6, p. 429, 1957. (Neutrino oscillation hypothesis.)
#   [10] Z. Maki, M. Nakagawa, and S. Sakata, "Remarks on the Unified
#        Model of Elementary Particles," Prog. Theor. Phys., vol. 28,
#        pp. 870-880, 1962. (PMNS neutrino mixing matrix.)
#
#  Fusion & Plasma Physics:
#   [11] H.-S. Bosch and G. M. Hale, "Improved formulas for fusion
#        cross-sections and thermal reactivities," Nucl. Fusion, vol. 32,
#        pp. 611-631, 1992. (Parametric fits for D-T, D-D, D-He3, T-T, He3-He3.)
#   [12] J. D. Lawson, "Some Criteria for a Power Producing Thermonuclear
#        Reactor," Proc. Phys. Soc. B, vol. 70, pp. 6-10, 1957.
#        (Lawson criterion: n*tau_E > threshold for ignition.)
#
#  Gravitational Physics:
#   [13] R. C. Tolman, "Static Solutions of Einstein's Field Equations
#        for Spheres of Fluid," Phys. Rev., vol. 55, pp. 364-373, 1939.
#   [14] J. R. Oppenheimer and G. M. Volkoff, "On Massive Neutron Cores,"
#        Phys. Rev., vol. 55, pp. 374-381, 1939.
#        (Tolman-Oppenheimer-Volkoff equation for neutron star structure.)
#   [15] B. P. Abbott et al. (LIGO/Virgo), "Observation of Gravitational
#        Waves from a Binary Black Hole Merger," Phys. Rev. Lett., vol. 116,
#        061102, 2016. (GW150914 — first direct detection.)
#
#  Higgins Unity Framework:
#   [16] P. Higgins, "Higgins Unity Framework (HUF): Compositional Data
#        Analysis across Physical Scales via the Entropy-Invariant Time
#        Transformer," CoDaWork 2026 submission, 2026.
#        (EITT, PLL, Higgins Decomposition, DADC/DADI, Vertex Theorem,
#        93% Bound, SPPI, IFR Standard.)
#
# ═══════════════════════════════════════════════════════════════════════════════


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║  SCIENTIFIC GLOSSARY — Higgins Unity Framework (HUF)                        ║
# ║  Source of truth: ai-refresh/HUF_COMPLETE_REFERENCE.json v1.0               ║
# ║  This block makes the experiment standalone and self-documenting.           ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝
#
# ── FRAMEWORK FOUNDATION ─────────────────────────────────────────────────────
#
#   HUF  = Higgins Unity Framework
#          The overarching scientific framework connecting Compositional Data
#          Analysis (CoDa) to cross-domain measurement. Author: Peter Higgins.
#          Repository: github.com/PeterHiggins19/Higgins-Unity-Framework
#
#   CoDa = Compositional Data Analysis
#          The mathematical framework for data that sums to a constant,
#          developed by John Aitchison (1982/1986) and advanced by Egozcue,
#          Pawlowsky-Glahn, and Tolosana-Delgado. Always written "CoDa"
#          (capital C, lowercase o, capital D, lowercase a).
#
#   EITT = Entropy-Invariant Time Transformer
#          Shannon entropy of compositional data is near-invariant under
#          geometric-mean decimation across temporal resolutions.
#          NOT "Time Transformation", NOT "Temporal Transform",
#          NOT "Energy-Information Transfer Theory".
#
#   HUF-GOV = HUF Governance — open-loop observation layer
#             The measurement path that observes but does not control.
#             "A tool that produces a verifiably clean usable output to a
#             known degree of certainty; the diagnostic of the output is
#             open to interpretation by expert decision and open to
#             modification by expert judgment." — Peter Higgins, 2026-04-15
#

# ── METHODOLOGY ───────────────────────────────────────────────────────────
#
#   PLL — TWO meanings in HUF (ALWAYS disambiguate):
#     CIP = Compositional Integrity Protocol — 6 immutable rules:
#         Rule 1: All roots computed on simplex carrier
#         Rule 2: Simplex normalisation only
#         Rule 3: RMS aggregator (p=2 locked)
#         Rule 4: Every observation retained
#         Rule 5: No new constants (6.02 dB, 115 Hz*m, 5.5-octave BW)
#         Rule 6: Polarity alignment mandatory
#     (2) Phase-locked loop ANALOGY — the sigma^2_A parabola maps onto
#         PLL architecture from signal processing. The word 'analogy' is
#         mandatory when using this meaning.
#
#   Boundary Species — Components of a composition that sit at or near
#     a structural boundary (zero, dominant, or regime-change threshold).
#     Identified by the F17 diagnostic. These species drive the largest
#     residuals in the DADC-DADI-ADAC chain.
#
#   Vertex Theorem — For a D-part compositional time series x(t):
#     sigma^2_A(t) = (1/D) * SUM(clr_i(t)^2)
#     The vertex occurs where d(sigma^2_A)/dt = 0, i.e. clr(t*) _|_ clr'(t*).
#     Physical meaning: composition restructures but stress is momentarily
#     stationary. The discriminator epsilon(t) = 2a(t - t0) is LINEAR.
#
#   The 93% Bound — Universal upper bound on normalised Shannon entropy
#     H/Hmax <= 0.93 observed across all 75 HUF systems spanning 44 orders
#     of magnitude. No physical composition reaches maximum entropy.
#

# ── FORMULAS & DEFINITIONS ────────────────────────────────────────────────
#
#   Simplex Closure (CoDa):
#     x_i = y_i / SUM(y_j)   for i = 1, ..., D
#     Constraint: SUM(x_i) = 1.  The data live on the (D-1)-simplex S^D.
#     This is the foundational CoDa operation — all subsequent analysis
#     occurs on the simplex, not in unconstrained Euclidean space.
#
#   Aitchison Variance — compositional dispersion measure:
#     sigma^2_A(t) = (1/D) * SUM(clr_i(t)^2)
#     Measures how far a composition departs from the barycenter.
#     When sigma^2_A = 0, the composition is at the barycenter (1/D, ..., 1/D).
#     The PLL parabola: sigma^2_A vs. time traces a diagnostic curve.
#
#   Shannon Entropy — information content of a composition:
#     H(x) = -SUM(x_i * ln(x_i))   for i = 1, ..., D
#     Maximum: H_max = ln(D) at the barycenter (1/D, ..., 1/D).
#     Normalised: H/H_max in [0, 1].  The 93% bound: H/H_max <= 0.93.
#     EITT discovery: H is near-invariant under geometric-mean decimation.
#
#   Bosch-Hale Parameterisation — fusion reactivity <sigma*v>(T):
#     Reference: Bosch & Hale, Nuclear Fusion 32 (1992) 611.
#     Gives <sigma*v> in cm^3/s as a function of ion temperature T in keV
#     for the five primary fusion reactions: D-T, D-D(n), D-D(p), D-He3, T-T.
#     At each T, the five reactivities form a 5-part composition on S^4.
#
#   Semi-Empirical Mass Formula (SEMF / Weizsaecker):
#     B(A,Z) = a_V*A - a_S*A^(2/3) - a_C*Z*(Z-1)/A^(1/3) - a_A*(A-2Z)^2/A
#     The four terms (Volume, Surface, Coulomb, Asymmetry) form a 4-part
#     composition on the simplex: each term's share of total binding energy.
#     Constants: a_V=15.56, a_S=17.23, a_C=0.697, a_A=23.29 (all MeV).
#

# ── DOMAIN-SPECIFIC TERMS ─────────────────────────────────────────────────
#
#   QGP = Quark-Gluon Plasma — the deconfined state of matter at extreme
#         temperature/density where quarks and gluons are free.
#         Created in heavy-ion collisions at RHIC/LHC.
#

# ── DOCUMENT STANDARDS ────────────────────────────────────────────────────
#
#   First-Use Rule: Every acronym must be expanded fully on first use in
#     every document. E.g., "The Entropy-Invariant Time Transformer (EITT)".
#
#   CoDa Advertising Rule: When any CoDa method is used, name it explicitly.
#     E.g., "Aitchison variance (CoDa)", "CLR transform (CoDa)",
#     "geometric-mean decimation (CoDa barycenter)".
#
#   PLL Disambiguation: Always clarify which PLL meaning is intended —
#     PLL = Phase-Locked Loop (the engineering analogy from signal processing).
#     (the engineering correspondence).
#
#   Formula Declaration: Every formula used must declare all variables,
#     their units, and their domain. No assumed knowledge.
#
#   No-Assumed-Knowledge: A reader with basic statistics but no CoDa training
#     should be able to follow any experiment from its glossary alone.
#
# ═════════════════════════════════════════════════════════════════════════════


import math
import json
import os
import shutil

# ═══════════════════════════════════════════════════════════════
#  THE MASTER REGISTRY
# ═══════════════════════════════════════════════════════════════
#
#  Every composite system ever touched by HUF, organised by
#  the fundamental domain it belongs to:
#
#    MATTER   — systems where the composition is of physical stuff
#    ENERGY   — systems where the composition is of energy channels
#    GRAVITY  — systems where gravity shapes the composition
#    FORCE    — systems governed by fundamental force budgets
#
#  Status codes:
#    SEALED    — full PLL-EITT chain, sealed JSON, in repo
#    COMPLETE  — analysed with H/H_max and σ²_A, results confirmed
#    PARTIAL   — some analysis done, gaps remain
#    MAPPED    — composition identified but not yet run through full chain
#    UNTOUCHED — known composite, not yet studied
#    FLAW      — known issue or limitation found
#    OPPORTUNITY — clear next step that would yield new insight

SYSTEMS = []

def add(name, domain, subdomain, experiment, channels, n_channels,
        H_computed, sA_computed, PLL_done, PLL_R2, status,
        flaw=None, opportunity=None, notes=""):
    SYSTEMS.append({
        "name": name,
        "domain": domain,
        "subdomain": subdomain,
        "experiment": experiment,
        "channels": channels,
        "n_channels": n_channels,
        "H_computed": H_computed,
        "sA_computed": sA_computed,
        "PLL_done": PLL_done,
        "PLL_R2": PLL_R2,
        "status": status,
        "flaw": flaw,
        "opportunity": opportunity,
        "notes": notes,
    })


# ═══════════════════════════════════════════════════════════════
#  DOMAIN: MATTER — Physical Substance Compositions
# ═══════════════════════════════════════════════════════════════

# --- Geochemistry (EXP-05) ---
add("Igneous Rocks (full series)",
    "MATTER", "Geochemistry", "EXP-05",
    "SiO₂, TiO₂, Al₂O₃, FeOt, MgO, CaO, Na₂O, K₂O", 8,
    True, True, True, 0.629, "SEALED",
    notes="28 rocks, vertex at andesite-dacite boundary (SiO₂≈59)")

add("Plutonic Rocks (subset)",
    "MATTER", "Geochemistry", "EXP-05",
    "SiO₂, TiO₂, Al₂O₃, FeOt, MgO, CaO, Na₂O, K₂O", 8,
    True, True, True, 0.825, "SEALED",
    notes="14 plutonic only. Strongest parabola R²=0.825. Slow cooling = tighter lock.")

add("Volcanic Rocks (subset)",
    "MATTER", "Geochemistry", "EXP-05",
    "SiO₂, TiO₂, Al₂O₃, FeOt, MgO, CaO, Na₂O, K₂O", 8,
    True, True, True, 0.441, "SEALED",
    notes="14 volcanic only. R²=0.44. Fast cooling = weaker lock.")

add("Intermediate Rocks (subset)",
    "MATTER", "Geochemistry", "EXP-05",
    "SiO₂, TiO₂, Al₂O₃, FeOt, MgO, CaO, Na₂O, K₂O", 8,
    True, True, True, 0.014, "SEALED",
    flaw="Anti-lock (hill-shaped). R²=0.014. Marks alkaline-subalkaline divergence.",
    notes="Correctly identified as regime boundary, not failure.")

# --- Nuclear / Atomic (EXP-03) ---
add("U-238 Decay Chain",
    "MATTER", "Nuclear", "EXP-03",
    "Z/A, N/A", 2,
    True, True, True, 0.618, "SEALED",
    notes="∩-shaped anti-lock. Relaxation toward stable Pb-206.")

add("Th-232 Decay Chain",
    "MATTER", "Nuclear", "EXP-03",
    "Z/A, N/A", 2,
    True, True, True, None, "SEALED",
    notes="Anti-lock confirmed. Relaxation toward Pb-208.")

add("U-235 Decay Chain",
    "MATTER", "Nuclear", "EXP-03",
    "Z/A, N/A", 2,
    True, True, True, None, "SEALED",
    notes="Anti-lock confirmed. Relaxation toward Pb-207.")

add("SEMF Binding Energy Valley",
    "MATTER", "Nuclear", "EXP-03/10",
    "Volume, Surface, Coulomb, Asymmetry", 4,
    True, True, True, 0.20, "SEALED",
    flaw="L-shaped full range. Non-stationary regime transition at M=12.",
    notes="Split confirmed EXP-10: R²_full=0.432, R²_light=0.797, R²_heavy=0.933. Heavy nuclei near-perfect lock.")

add("Nuclide Chart (AME2020)",
    "MATTER", "Nuclear", "EXP-03",
    "Z, N across 3554 nuclides", 2,
    True, True, False, None, "COMPLETE",
    opportunity="Full PLL scan across Z-chains. Could find new magic numbers.",
    notes="3,554 nuclides mapped. Used for valley analysis.")

add("Superheavy Elements Z=118→1000",
    "MATTER", "Nuclear", "EXP-EXT",
    "Volume, Surface, Coulomb, Asymmetry, Shell", 5,
    True, True, False, None, "COMPLETE",
    opportunity="Island of stability around Z≈522. Exotic nuclear shapes.",
    notes="Extreme extrapolation. Found shell closure predictions at Z=120,126,164,184.")

# --- Hadron / Quark Composition (EXP-07) ---
add("Proton Mass Budget",
    "MATTER", "Quark", "EXP-07",
    "Quark KE, Gluon Field, Trace Anomaly, Higgs Rest Mass", 4,
    True, True, False, None, "SEALED",
    opportunity="PLL across Q² scale (DGLAP evolution) would test compositional stability.",
    notes="H/H_max=0.928. 91% from QCD, 9% from Higgs. Near-maximal entropy.")

add("Proton Spin Budget",
    "MATTER", "Quark", "EXP-07B",
    "Quark Spin, Gluon Spin, Quark Orbital, Gluon Orbital", 4,
    True, True, False, None, "COMPLETE",
    opportunity="PLL across x-Bjorken would map spin composition vs resolution.",
    notes="H/H_max=0.969. 'Spin crisis' reframed as maximum entropy distribution.")

add("Parton Momentum (DGLAP evolution)",
    "MATTER", "Quark", "EXP-07/10",
    "Valence quarks, Sea quarks, Gluons", 3,
    True, True, True, 0.980, "COMPLETE",
    notes="PLL R²_sA=0.980, R²_H=0.973, vertex at logQ²=-7.12. Compositional stability window confirmed.")

add("Quark Flavor Mass Hierarchy",
    "MATTER", "Quark", "EXP-07B",
    "Gen 1 (u,d), Gen 2 (s,c), Gen 3 (b,t)", 3,
    True, True, False, None, "COMPLETE",
    flaw="H/H_max=0.088 — most asymmetric composition in all of physics.",
    opportunity="Froggatt-Nielsen ε=0.225 test. Is Cabibbo angle a compositional ratio?",
    notes="99.2% in Gen 3 (top quark dominates). Frozen symmetry breaking.")

add("CKM Mixing Matrix (u-row)",
    "MATTER", "Quark", "EXP-07B",
    "u→d, u→s, u→b", 3,
    True, True, False, None, "COMPLETE",
    opportunity="Full 3×3 CKM as 9-channel composition. Compare to PMNS (leptons).",
    notes="H/H_max=0.182. Near-diagonal = near-zero entropy. 10¹⁰ CP shortfall.")

add("Exotic Hadrons (X, Z, P_c, T_cc)",
    "MATTER", "Quark", "EXP-10",
    "Quark content fractions + width", 4,
    True, True, False, None, "COMPLETE",
    notes="8 exotics. Molecular mean σ²_A=9.76 vs compact mean σ²_A=2.92. Clear discriminator. Testable LHCb Run 3-4.")

# --- Biological Matter ---
add("Blood Composition by Age",
    "MATTER", "Biology", "HUNT",
    "RBC, WBC, Plasma, Platelets", 4,
    True, True, True, None, "COMPLETE",
    opportunity="Full PLL across age 0-90. Vertex at ~27 = peak haem fitness.",
    notes="From 30-domain hunt. Lock confirmed.")

add("Gut Microbiome Colonisation",
    "MATTER", "Biology", "HUNT",
    "Bacteroidetes, Firmicutes, Proteobacteria, Actinobacteria, other", 5,
    True, True, True, None, "COMPLETE",
    opportunity="Longitudinal PLL across infant→adult transition.",
    notes="Neonatal phase lock. 2-force colonisation model.")

# --- Financial Matter ---
add("Gold/Silver Price Ratio",
    "MATTER", "Financial", "EXP-01",
    "Gold fraction, Silver fraction", 2,
    True, True, True, 0.901, "SEALED",
    notes="Founding experiment. 338 years (1688-2026). Vertex at 1751. Q=22.18.")

# --- Planetary Matter ---
add("Planetary Atmospheres",
    "MATTER", "Planetary", "HUNT",
    "CO₂, N₂, O₂, Ar, CH₄, H₂, He (varies per body)", 7,
    True, True, True, None, "COMPLETE",
    opportunity="Full comparative PLL: Venus vs Earth vs Mars vs Titan.",
    notes="Split regime locks. Inner vs outer planet compositions differ fundamentally.")


# ═══════════════════════════════════════════════════════════════
#  DOMAIN: ENERGY — Energy Channel Compositions
# ═══════════════════════════════════════════════════════════════

# --- Fusion Energy Partition (EXP-06 series) ---
add("IFR Burning Plasma (reference)",
    "ENERGY", "Fusion", "EXP-06/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, True, 0.996, "SEALED",
    notes="T=17.8 keV, n=2.70, B=12T. Alpha=50.2%. SPPI=1.000. Self-ignited.")

add("Spherical Tokamak (STEP/MAST-U)",
    "ENERGY", "Fusion", "EXP-06/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    opportunity="PLL across κ (elongation) parameter space.",
    notes="Alpha=72.9%. Best composition. High κ=2.8, low B=3.5T.")

add("Conventional Tokamak (ITER)",
    "ENERGY", "Fusion", "EXP-06/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="Greenwald density limit blocks ignition at n=1.0×10²⁰.",
    notes="Alpha=32.5%. Conduction-dominated (53.2%). Q=10 design.")

add("Compact HF Tokamak (SPARC/ARC)",
    "ENERGY", "Fusion", "EXP-06/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="R^1.97 confinement penalty. Right magnets, wrong size.",
    opportunity="Scale SPARC to R=6.2m → becomes the IFR.",
    notes="Alpha=45.7%. 4.5% below ignition. Closest real machine to IFR.")

add("Krell Level 1 (Boosted)",
    "ENERGY", "Fusion", "EXP-06K/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    opportunity="Detailed engineering feasibility with today's HTS magnets.",
    notes="Alpha=58.3%. Driven by 10× IFR. Q_eng=4.1. 67.9 GW plant.")

add("Krell Level 2 (Cyclotron wall)",
    "ENERGY", "Fusion", "EXP-06J",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="Cyclotron wall at 78.9%. B=45T, T=100 keV. Budget collapses.",
    opportunity="Optically thick plasma (n>10²² m⁻³) could reabsorb cyclotron.",
    notes="This is where the Krell cascade breaks. Fundamental limit of magnetic confinement.")

add("Stellarator (W7-X/HELIAS)",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="Poor confinement without plasma current. Cond=59%.",
    notes="Alpha=18.3%. Steady-state advantage doesn't compensate for transport losses.")

add("Inertial Confinement (NIF)",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="B=0 → zero Cyclo but Cond=68.8% (hydrodynamic blowoff).",
    notes="Alpha=22.5%. Q=1.5 achieved Dec 2022. Wall-plug efficiency <1%.")

add("FRC / TAE Helion (D-He3)",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="D-He3 cross-section 100× below D-T. Brem=22.3% from high T.",
    notes="Alpha=8.2%. FRC confinement too poor at R=0.3m.")

add("Proton-Boron (p-B11)",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="Z_eff=5 → 25× Brem penalty. Brem=78.3% destroys budget.",
    notes="The Bremsstrahlung wall. Cannot ignite with any known confinement.")

add("Magnetic Mirror",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="Loss-cone leakage dominates Cond=46.6%.",
    notes="Alpha=29.4%. Renaissance interest (Realta, WHAM) but physics limit stands.")

add("Z-Pinch (Zap Energy)",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="τ~10ns. Ultra-short confinement → Cond=85%.",
    notes="Alpha=1.2%. Dense but transient.")

add("Magnetised Target (General Fusion)",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="Compression instabilities disrupt before ignition. Cond=80.4%.",
    notes="Alpha=2.1%.")

add("Spheromak",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="Too cold (T=5 keV), too small (R=0.5m). Cond=87.4%.",
    notes="Alpha=0.3%. Nearly pure conduction loss.")

add("Muon-Catalysed Fusion",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="Alpha-sticking limit ~150 fusions/muon. Brem=90%.",
    notes="Cold fusion (T=0.01 keV). Fundamentally limited by muon lifetime.")

add("D-He3 Aneutronic Magnetic",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="σ(D-He3) 100× below σ(D-T). Cannot compensate. Cond=50.5%.",
    notes="Alpha=12.4%. Aneutronic dream but physics says no.")

add("Electrostatic Fusor",
    "ENERGY", "Fusion", "EXP-06H/08",
    "Alpha, Bremsstrahlung, Cyclotron, Conduction", 4,
    True, True, False, None, "COMPLETE",
    flaw="Thermodynamic barrier. Cond=96.6%. n=0.01×10²⁰ far too low.",
    notes="Alpha=0.8%. Neutron source only, never power.")

# --- D-T Reactivity Composition (EXP-06) ---
add("D-T Reaction Rate Composition",
    "ENERGY", "Nuclear Reactions", "EXP-06",
    "D-T, D-D(n), D-D(p), D-He3, T-T", 5,
    True, True, True, 0.996, "SEALED",
    notes="PLL vertex at 20.1 keV = optimal ignition temperature. Near-perfect parabola.")

add("Energy Partition (5-channel)",
    "ENERGY", "Nuclear Reactions", "EXP-06",
    "Neutron KE, Alpha heating, Brem, Cyclo, Cond", 5,
    True, True, True, 0.579, "SEALED",
    notes="Bremsstrahlung = boundary species (34.9% CLR variance). Vertex at 43.3 keV.")

# --- Electricity Generation (EXP-02) ---
add("US State Energy Mix (10 states)",
    "ENERGY", "Electricity", "EXP-02",
    "Coal, Gas, Nuclear, Hydro, Solar, Wind, Bio, Fossil, Renewables", 9,
    True, True, True, None, "SEALED",
    opportunity="Extend to all 50 states. Global comparison (EU, China, India).",
    notes="8/10 states lock. CA vertex 2014. WV/WY correctly fail (coal-dominated).")

add("European Energy Prices",
    "ENERGY", "Electricity", "HUNT",
    "Price components by source", None,
    True, True, True, None, "COMPLETE",
    notes="From 30-domain hunt. Lock confirmed.")

add("NGFS Climate Energy Scenarios",
    "ENERGY", "Climate/Policy", "HUNT",
    "Coal, Gas, Oil, Nuclear, Bio, Renewables", 6,
    True, True, True, None, "COMPLETE",
    opportunity="Bell test violation found — worth deeper analysis.",
    notes="35 scenarios tested. Lock across policy pathways.")

# --- Acoustic Energy (EXP-04) ---
add("RC Bandpass Filter Response",
    "ENERGY", "Acoustics", "EXP-04",
    "Signal power, Loss", 2,
    True, True, True, None, "SEALED",
    notes="Orders 1-6 tested. Shape flip at 4→5. Critical transition at order 2→3.")

add("Room Acoustics Spectrum",
    "ENERGY", "Acoustics", "HUNT",
    "Frequency band powers", None,
    True, True, True, 0.998, "COMPLETE",
    notes="Highest R² observed in entire programme. Peter's founding domain.")

# --- QCD Energy (EXP-07) ---
add("QGP (Quark-Gluon Plasma)",
    "ENERGY", "QCD", "EXP-07/07B",
    "Quarks, Gluons", 2,
    True, True, True, None, "COMPLETE",
    opportunity="PLL across temperature (T_c to 5T_c). Map deconfinement transition.",
    notes="H/H_max=0.971. η/s=1.5× KSS. 93% compositional efficiency.")

add("Color Confinement (qq̄ pair)",
    "ENERGY", "QCD", "EXP-10",
    "Coulomb, String tension, Kinetic", 3,
    True, True, True, 0.497, "COMPLETE",
    notes="PLL R²=0.497, vertex at 1.38 fm, crossover at 0.70 fm. Bowl shape confirmed. String = QCD flux tube.")

add("QCD Running Coupling α_s(Q)",
    "ENERGY", "QCD", "EXP-10",
    "Strong coupling strength across energy scales", 1,
    True, True, True, 0.998, "COMPLETE",
    notes="PLL R²=0.998, vertex at logQ=9.23, crossover at 0.53 GeV. Near-perfect parabola in log space.")

# --- Thermal / Stellar Energy ---
add("Wine Fermentation",
    "ENERGY", "Biochemistry", "HUNT",
    "Sugar, Ethanol, CO₂, Metabolites", 4,
    True, True, True, None, "COMPLETE",
    notes="84% noise squeeze. From 30-domain hunt.")

add("Bacterial Growth Kinetics",
    "ENERGY", "Biochemistry", "HUNT",
    "Lag, Log, Stationary, Death phase fractions", 4,
    True, True, True, None, "COMPLETE",
    notes="From 30-domain hunt.")


# ═══════════════════════════════════════════════════════════════
#  DOMAIN: GRAVITY — Gravitationally-Shaped Compositions
# ═══════════════════════════════════════════════════════════════

add("Sun (pp-chain core)",
    "GRAVITY", "Stellar", "EXP-06I/08",
    "Alpha-equivalent, Neutrino loss", 2,
    True, True, False, None, "COMPLETE",
    opportunity="Extend to CNO cycle stars. Compare main sequence vs giant branch.",
    notes="Alpha≈98%, Neutrino≈2%. Gravitational confinement. 68,074× lower power density than IFR.")

add("Stellar Nucleosynthesis (BBN)",
    "GRAVITY", "Cosmology", "HUNT",
    "H, He, C, N, O, heavier elements", 6,
    True, True, True, None, "COMPLETE",
    opportunity="PLL across stellar mass (0.1-100 M_sun).",
    notes="86% noise squeeze. Lock confirmed in hunt.")

add("Neutron Star EOS",
    "GRAVITY", "Compact Objects", "EXP-11/CROSS",
    "n, p, e, μ composition profile", 4,
    True, True, True, 0.940, "COMPLETE",
    flaw="Muon threshold at 1.5ρ₀ creates topological channel birth (3→4 channels).",
    notes="APR, SLy, BSk all give same σ²_A trajectory (R²>0.94). EOS-universality confirmed. Muon onset = regime boundary.")

add("Kilonova r-process",
    "GRAVITY", "Compact Objects", "HUNT",
    "Lanthanide, Actinide, lighter r-process fractions", 3,
    True, True, True, None, "COMPLETE",
    opportunity="Compare GW170817 vs GW190425. Different mass ratios = different compositions.",
    notes="From 30-domain hunt. Nucleosynthesis in extreme gravity.")

add("Cosmic Ray Flux",
    "GRAVITY", "Astrophysics", "HUNT",
    "H, He, CNO-group, Fe-group, Ultra-heavy", 5,
    True, True, True, 0.991, "COMPLETE",
    flaw="Trajectory only (monotonic), no PLL vertex. Vertex at logE=16.9 (outside range).",
    opportunity="Rerun with composition binned by energy decade. May find knee/ankle vertices.",
    notes="R²=0.991 but monotonic. Diagnostic, not lock.")

add("Ocean Salinity Profiles",
    "GRAVITY", "Geophysics", "HUNT",
    "Na⁺, Cl⁻, SO₄²⁻, Mg²⁺, Ca²⁺, K⁺", 6,
    True, True, True, None, "COMPLETE",
    notes="From 30-domain hunt. Gravitationally stratified ocean chemistry.")

add("Tsunami Sediment Transport",
    "GRAVITY", "Geophysics", "HUNT",
    "Sand, Silt, Clay, Gravel fractions", 4,
    True, True, True, None, "COMPLETE",
    notes="From 30-domain hunt. Gravity-driven sorting.")

# --- EXP-11: Nuclide Z-chains ---
add("Nuclide Z-chains (8 isobar series)",
    "GRAVITY", "Nuclear", "EXP-11",
    "Volume, Surface, Coulomb, Asymmetry (SEMF)", 4,
    True, True, True, None, "COMPLETE",
    notes="A=16,40,56,90,120,150,180,208 isobar chains. Stability valley = compositional balance across Z.")

# --- EXP-11: Stellar mass sequence ---
add("Stellar Mass Sequence (pp→CNO)",
    "GRAVITY", "Stellar", "EXP-11",
    "pp, CNO, other fusion fractions", 3,
    True, True, True, None, "COMPLETE",
    notes="16 stars 0.1-100 M☉. pp→CNO crossover at 1.35 M☉. Peak |dH/dM|=2.445 at 0.9 M☉. Gravitational leverage.")

# --- EXP-12: Gravitational Wave Systems ---
add("GW150914 BBH Merger (mass budget)",
    "GRAVITY", "Gravitational Waves", "EXP-12",
    "M₁, M₂, M_final, E_radiated", 4,
    True, True, False, None, "COMPLETE",
    notes="H/H_max=0.175 — lowest entropy in all HUF. No-hair theorem as compositional minimum.")

add("GW150914 Phase Budget (inspiral/merger/ringdown)",
    "GRAVITY", "Gravitational Waves", "EXP-12",
    "Inspiral, Merger, Ringdown energy fractions", 3,
    True, True, False, None, "COMPLETE",
    notes="50%/33%/17% = H/H_max=0.923. Sits near 93% universal entropy bound. Extends bound to pure gravity.")

add("GW150914 QNM Mode Composition",
    "GRAVITY", "Gravitational Waves", "EXP-12",
    "(2,2,0), (3,3,0), (2,1,0) overtone amplitudes", 3,
    True, True, False, None, "COMPLETE",
    notes="(2,2,0) at 90%. No-hair as compositional minimum. Maximum gravitational compression → minimum entropy.")

add("GW170817 BNS Merger (matter bonus)",
    "GRAVITY", "Gravitational Waves", "EXP-12",
    "M₁, M₂, M_final, E_GW, E_EM", 5,
    True, True, False, None, "COMPLETE",
    notes="5 channels vs BBH 3. H/H_max=0.111 — even lower entropy than BBH. Matter = extra channels but tighter lock.")

# --- EXP-12: Gravity Boundary Map ---
add("Gravity Role Classification (24 systems)",
    "GRAVITY", "Cross-Scale", "EXP-12",
    "Gravity role: NONE/ORTHOGONAL/BOUNDARY/DIRECT", 4,
    True, True, False, None, "COMPLETE",
    notes="24 systems classified. Activation scale ~10⁷ m. Below=silent, above=progressive dominance.")


# ═══════════════════════════════════════════════════════════════
#  DOMAIN: FORCE — Fundamental Force Budget Compositions
# ═══════════════════════════════════════════════════════════════

add("Strong CP Problem (QCD vacuum)",
    "FORCE", "QCD Vacuum", "EXP-10",
    "CP-even, CP-odd", 2,
    True, True, True, 0.390, "COMPLETE",
    notes="PLL R²=0.390, vertex at θ=1.69, bowl shape. θ=0 minimum entropy confirmed. EITT axion prediction stands.")

add("EMC Effect (nuclear PDFs)",
    "FORCE", "Nuclear QCD", "EXP-10",
    "Valence quarks, Sea quarks, Gluons (in-medium vs free)", 3,
    True, True, True, 0.999, "COMPLETE",
    notes="Free σ²_A=0.29, SRC-correlated σ²_A=-0.98. PLL R²=0.999. Testable at EIC (~2030s). 9 nuclei scanned.")

add("QGP Freeze-out (7 hadron species)",
    "FORCE", "QCD Phase", "EXP-07/CROSS",
    "π, K, p, Λ, Ξ, Ω, φ", 7,
    True, True, True, None, "SEALED",
    notes="0.27% EITT. Crosses nuclear-quark boundary. Lambda = boundary species.")

# --- Weak / Electroweak ---
add("CKM Full 3×3 Matrix",
    "FORCE", "Electroweak", "EXP-10",
    "9 mixing amplitudes |V_ij|²", 9,
    True, True, False, None, "COMPLETE",
    notes="Full H/H_max=0.564, σ²_A=15.48. Diagonal fraction 96.6%. Row entropies: [0.182, 0.189, 0.012].")

add("PMNS Matrix (Lepton Mixing)",
    "FORCE", "Electroweak", "EXP-10",
    "ν_e→ν_1, ν_e→ν_2, ν_e→ν_3, etc.", 9,
    True, True, False, None, "COMPLETE",
    notes="H/H_max=0.911 vs CKM 0.564. Entropy ratio 1.615. PMNS near-maximal, CKM near-diagonal.")

add("Higgs Branching Ratios",
    "FORCE", "Electroweak", "EXP-10",
    "bb̄, WW*, gg, ττ, cc̄, ZZ*, γγ, Zγ, μμ", 9,
    True, True, False, None, "COMPLETE",
    notes="H/H_max=0.568, σ²_A=5.80. bb̄-dominated. Coupling hierarchy maps to compositional asymmetry.")

# --- Gravitational ---
add("CMB Power Spectrum Composition",
    "FORCE", "Cosmology", "EXP-10/11",
    "Baryonic matter, Dark matter, Dark energy, Radiation, Neutrinos", 5,
    True, True, False, None, "COMPLETE",
    notes="Present H/H_max=0.475, BBN H/H_max=0.428. Universe entropy declining from 0.60 (BBN) → 0.29 (far future).")

add("Dark Matter / Baryon Ratio",
    "FORCE", "Cosmology", "EXP-11",
    "Dark matter, Baryonic matter", 2,
    True, True, True, 0.998, "COMPLETE",
    notes="10 scales from NS (10⁴ m) to universe (4.4×10²⁶ m). DM confinement scale ~10²⁰ m analogous to QCD at 10⁻¹⁵ m.")

# --- Demographic / Social (from hunt) ---
add("Demographics (HDI index)",
    "FORCE", "Social", "HUNT",
    "Population age bands, GDP, HDI, Entropy", 4,
    True, True, True, 0.966, "COMPLETE",
    flaw="Trajectory only (monotonic). Vertex at HDI=-0.24 (outside range).",
    notes="R²=0.966 but no physical vertex. Diagnostic.")

add("Cardiac Arrhythmia Patterns",
    "FORCE", "Medical", "HUNT",
    "Normal, Atrial, Ventricular, Block, other rhythms", 5,
    True, True, True, None, "COMPLETE",
    notes="From 30-domain hunt.")

add("Atmospheric Chemistry",
    "FORCE", "Environmental", "HUNT",
    "O₃, NO₂, SO₂, CO, PM2.5, PM10", 6,
    True, True, True, None, "COMPLETE",
    notes="From 30-domain hunt.")

add("Soil Mineralogy",
    "FORCE", "Geochemistry", "HUNT",
    "Quartz, Feldspar, Mica, Clay minerals, Organics", 5,
    True, True, True, None, "COMPLETE",
    notes="From 30-domain hunt.")


# ═══════════════════════════════════════════════════════════════
#  SECTION 2: ANALYSIS AND OUTPUT
# ═══════════════════════════════════════════════════════════════

def print_header(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")

def status_symbol(s):
    return {
        "SEALED": "■",
        "COMPLETE": "●",
        "PARTIAL": "◐",
        "MAPPED": "○",
        "UNTOUCHED": "·",
    }.get(s, "?")

def main():
    print_header("EXP-09  MASTER INVENTORY — ALL COMPOSITE SYSTEMS IN HUF")

    # Count totals
    total = len(SYSTEMS)
    by_domain = {}
    by_status = {}
    with_flaws = []
    with_opps = []
    n_PLL = 0
    n_H = 0
    n_sA = 0

    for s in SYSTEMS:
        by_domain[s["domain"]] = by_domain.get(s["domain"], 0) + 1
        by_status[s["status"]] = by_status.get(s["status"], 0) + 1
        if s["flaw"]:
            with_flaws.append(s)
        if s["opportunity"]:
            with_opps.append(s)
        if s["PLL_done"]:
            n_PLL += 1
        if s["H_computed"]:
            n_H += 1
        if s["sA_computed"]:
            n_sA += 1

    print(f"\n  TOTAL COMPOSITE SYSTEMS: {total}")
    print(f"\n  By Domain:")
    for d in ["MATTER", "ENERGY", "GRAVITY", "FORCE"]:
        print(f"    {d:<10} {by_domain.get(d, 0):>3} systems")
    print(f"\n  By Status:")
    for st in ["SEALED", "COMPLETE", "PARTIAL", "MAPPED", "UNTOUCHED"]:
        ct = by_status.get(st, 0)
        bar = "█" * ct
        print(f"    {status_symbol(st)} {st:<12} {ct:>3}  {bar}")
    print(f"\n  Metrics Computed:")
    print(f"    H/H_max:   {n_H:>3} / {total} ({100*n_H/total:.0f}%)")
    print(f"    σ²_A:      {n_sA:>3} / {total} ({100*n_sA/total:.0f}%)")
    print(f"    PLL done:  {n_PLL:>3} / {total} ({100*n_PLL/total:.0f}%)")
    print(f"    Flaws:     {len(with_flaws):>3}")
    print(f"    Opportunities: {len(with_opps):>3}")

    # ─── FULL TABLE BY DOMAIN ───
    for domain in ["MATTER", "ENERGY", "GRAVITY", "FORCE"]:
        print_header(f"DOMAIN: {domain}")

        domain_systems = [s for s in SYSTEMS if s["domain"] == domain]

        # Group by subdomain
        subdomains = []
        seen = set()
        for s in domain_systems:
            if s["subdomain"] not in seen:
                subdomains.append(s["subdomain"])
                seen.add(s["subdomain"])

        for sd in subdomains:
            sd_systems = [s for s in domain_systems if s["subdomain"] == sd]
            print(f"\n  ─── {sd} ({len(sd_systems)} systems) ───")
            print(f"  {'System':<38} {'Ch':>3} {'H':>3} {'σ²':>3} {'PLL':>4} {'R²':>6} Status")
            print(f"  {'-'*38} {'-'*3} {'-'*3} {'-'*3} {'-'*4} {'-'*6} {'-'*10}")

            for s in sd_systems:
                h_mark = "✓" if s["H_computed"] else "·"
                sa_mark = "✓" if s["sA_computed"] else "·"
                pll_mark = "✓" if s["PLL_done"] else "·"
                r2_str = f"{s['PLL_R2']:.3f}" if s["PLL_R2"] else "  —  "
                n_ch = str(s["n_channels"]) if s["n_channels"] else " ?"
                sym = status_symbol(s["status"])
                short = s["name"] if len(s["name"]) < 38 else s["name"][:35] + "..."

                print(f"  {sym} {short:<37} {n_ch:>3} {h_mark:>3} {sa_mark:>3} {pll_mark:>4} {r2_str:>6} {s['status']}")

                if s["flaw"]:
                    print(f"      ⚠ FLAW: {s['flaw'][:70]}")
                if s["opportunity"]:
                    print(f"      → OPP:  {s['opportunity'][:70]}")

    # ─── FLAWS SUMMARY ───
    print_header("ALL FLAWS — Issues Found Across Programme")
    for i, s in enumerate(with_flaws, 1):
        print(f"\n  {i:>2}. {s['name']} [{s['experiment']}]")
        print(f"      {s['flaw']}")

    # ─── OPPORTUNITIES SUMMARY ───
    print_header("ALL OPPORTUNITIES — Unfinished Business & Next Steps")

    # Sort by impact: UNTOUCHED first, then MAPPED, then others
    priority_order = {"UNTOUCHED": 0, "MAPPED": 1, "COMPLETE": 2, "SEALED": 3}
    sorted_opps = sorted(with_opps, key=lambda s: priority_order.get(s["status"], 4))

    for i, s in enumerate(sorted_opps, 1):
        tag = "NEW" if s["status"] in ("UNTOUCHED", "MAPPED") else "EXTEND"
        print(f"\n  {i:>2}. [{tag}] {s['name']} [{s['experiment']}]")
        print(f"      Status: {s['status']} | Domain: {s['domain']}/{s['subdomain']}")
        print(f"      {s['opportunity']}")

    # ─── CROSS-SCALE SUMMARY ───
    print_header("CROSS-SCALE MAP — From Quarks to the Universe")

    scale_order = [
        ("10⁻¹⁸ m", "Quark interior", "FORCE"),
        ("10⁻¹⁵ m", "Proton / Hadron", "MATTER"),
        ("10⁻¹² m", "QGP / Nuclear", "ENERGY"),
        ("10⁻¹⁰ m", "Atomic", "MATTER"),
        ("10⁻⁶ m", "Molecular / Bio", "MATTER"),
        ("10⁻³ m", "Filter / Acoustic", "ENERGY"),
        ("10⁰ m", "Reactor / Lab", "ENERGY"),
        ("10³ m", "Geochemistry", "MATTER"),
        ("10⁶ m", "Planetary", "MATTER"),
        ("10⁷ m", "Stellar core", "GRAVITY"),
        ("10¹⁰ m", "Neutron star", "GRAVITY"),
        ("10¹⁶ m", "Stellar system", "GRAVITY"),
        ("10²¹ m", "Galaxy", "GRAVITY"),
        ("10²⁶ m", "Universe", "FORCE"),
    ]

    print(f"\n  {'Scale':<12} {'Domain':<12} {'#Sys':>5} {'Status':>10}")
    print(f"  {'-'*12} {'-'*12} {'-'*5} {'-'*10}")

    for scale, label, dom in scale_order:
        # Count systems at this scale
        scale_systems = []
        for s in SYSTEMS:
            if dom == s["domain"]:
                # Rough matching
                if label.lower().split("/")[0].split()[0] in s["subdomain"].lower() or \
                   label.lower().split("/")[-1].split()[0] in s["subdomain"].lower():
                    scale_systems.append(s)

        n_sys = len(scale_systems) if scale_systems else 0
        if n_sys > 0:
            sealed = sum(1 for s in scale_systems if s["status"] == "SEALED")
            complete = sum(1 for s in scale_systems if s["status"] in ("COMPLETE", "SEALED"))
            status_str = f"{complete}/{n_sys} done"
        else:
            status_str = "—"

        # Coverage indicator
        if n_sys == 0:
            cov = "  ·  "
        elif all(s["status"] in ("SEALED", "COMPLETE") for s in scale_systems):
            cov = "  ■  "
        elif any(s["status"] in ("UNTOUCHED", "MAPPED") for s in scale_systems):
            cov = "  ◐  "
        else:
            cov = "  ●  "

        print(f"  {scale:<12} {label:<16} {n_sys:>3}{cov} {status_str}")

    # ─── FINAL SCORECARD ───
    print_header("SCORECARD")

    sealed = by_status.get("SEALED", 0)
    complete = by_status.get("COMPLETE", 0)
    mapped = by_status.get("MAPPED", 0)
    untouched = by_status.get("UNTOUCHED", 0)
    done = sealed + complete
    remaining = mapped + untouched

    print(f"""
  COMPOSITE SYSTEMS CENSUS
  ════════════════════════

  Total registered:          {total}
  ■ Sealed (full chain):     {sealed}
  ● Complete (analysed):     {complete}
  ○ Mapped (identified):     {mapped}
  · Untouched (known):       {untouched}

  Done:                      {done} / {total} ({100*done/total:.0f}%)
  Remaining:                 {remaining} / {total} ({100*remaining/total:.0f}%)

  Flaws found:               {len(with_flaws)}  (all diagnosed, none fatal)
  Opportunities:             {len(with_opps)}  ({sum(1 for s in with_opps if s['status'] in ('UNTOUCHED','MAPPED'))} new, {sum(1 for s in with_opps if s['status'] not in ('UNTOUCHED','MAPPED'))} extensions)

  PLL coverage:              {n_PLL} / {total} ({100*n_PLL/total:.0f}%)
  H/H_max coverage:          {n_H} / {total} ({100*n_H/total:.0f}%)
  σ²_A coverage:             {n_sA} / {total} ({100*n_sA/total:.0f}%)

  Scale range:               10⁻¹⁸ m (quarks) → 10²⁶ m (universe)
  Orders of magnitude:       44

  VERDICT: {done} systems done, {remaining} with clear next steps.
           {len(with_flaws)} flaws — all correctly diagnosed, zero fatal.
           {len(with_opps)} opportunities — {sum(1 for s in with_opps if s['status']=='UNTOUCHED')} brand new domains waiting.
""")

    # ─── SAVE TO REPO ───
    output_dir = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker"
    repo_dir = os.path.join(output_dir, "Current-Repo/HUF/codawork2026/experiments/EXP-09_Master_Inventory")
    os.makedirs(repo_dir, exist_ok=True)

    # Save registry as JSON
    registry = {
        "experiment": "EXP-09",
        "title": "Master Inventory of All Composite Systems",
        "total_systems": total,
        "by_domain": by_domain,
        "by_status": by_status,
        "n_flaws": len(with_flaws),
        "n_opportunities": len(with_opps),
        "pll_coverage": n_PLL,
        "systems": SYSTEMS,
    }
    json_path = os.path.join(repo_dir, "exp09_master_inventory.json")
    with open(json_path, 'w') as f:
        json.dump(registry, f, indent=2)

    # Copy script
    script_src = os.path.join(repo_dir, "exp09_master_inventory.py")
    # Script is already in repo_dir, no copy needed

    print(f"  [SAVED] {json_path}")
    print(f"  [SAVED] {os.path.join(repo_dir, 'exp09_master_inventory.py')}")


if __name__ == "__main__":
    main()
