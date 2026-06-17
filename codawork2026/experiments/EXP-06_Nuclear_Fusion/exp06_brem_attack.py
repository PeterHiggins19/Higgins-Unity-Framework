#!/usr/bin/env python3
"""
EXP-06B  BREMSSTRAHLUNG BOUNDARY ATTACK
========================================
Multi-dimensional compositional assault on the primary barrier to ignition.

Strategy
--------
Bremsstrahlung was identified as the boundary species in tokamak energy
partition (EXP-06, F3).  This script attacks the boundary from every
available axis:

  Phase 1 — Temperature sweep:  fixed n, vary T, find where Brem loses
            boundary dominance
  Phase 2 — Density sweep:      fixed T, vary n, find the flip
  Phase 3 — Impurity control:   vary Zeff (effective charge), the knob
            that directly scales Bremsstrahlung
  Phase 4 — Magnetic field:     vary B, which scales cyclotron losses
  Phase 5 — Full (n, T) plane:  2D scan, map the boundary species
            across the ignition landscape
  Phase 6 — Ignition surface:   find the exact boundary where
            alpha > losses (Lawson)
  Phase 7 — Path to ignition:   compositional trajectory from cold
            plasma to burning plasma, tracking boundary species flips
  Phase 8 — Frequency analysis: treat σ^2_A along ignition path as
            signal, decompose
  Phase 9 — Flip catalogue:     every (n, T, B, Zeff) where the
            boundary species changes identity
  Phase 10 — Aneutronic escape: does D-He3 bypass the Brem barrier?

Physics
-------
Power densities (W/m^3):
  P_α    = (1/4) n^2 <σv>_DT E_α          alpha heating (50:50 D:T)
  P_brem = C_b n^2 √T Zeff                Bremsstrahlung radiation
  P_cyc  = C_c n T^2 B^2 / (1 + aT)        cyclotron (with reabsorption)
  P_cond = (3/2) n T / τ_E               conduction losses
  P_line = C_L n^2 f_Z Z^2_imp √T          line radiation (impurities)

where:
  n in 10^2⁰ m⁻^3, T in keV, B in Tesla
  E_α = 3.52 MeV = 5.64e-13 J
  C_b = 5.35e3 W·m^3·keV^(-1/2) (for n in 10^2⁰ m⁻^3)
  τ_E from ITER IPB98(y,2) scaling

Author: Peter Higgins (HUF programme)
Computed by: Claude (Anthropic)
Date: 2026-04-18
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
#   Contamination Doctrine — A new domain must not alter constants or
#     methods established on prior domains. If Domain N+1 requires a change,
#     ALL prior domains must be re-verified with the change. If any prior
#     domain fails, the change is rejected.
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
#   Centred Log-Ratio Transform (CLR) — CoDa coordinate mapping:
#     clr(x)_i = ln(x_i) - (1/D) * SUM(ln(x_j))
#     Maps simplex compositions to unconstrained Euclidean space.
#     The geometric mean g(x) = exp((1/D) * SUM(ln(x_j))) is the reference.
#     Property: SUM(clr_i) = 0 (zero-sum constraint in CLR space).
#
#   Shannon Entropy — information content of a composition:
#     H(x) = -SUM(x_i * ln(x_i))   for i = 1, ..., D
#     Maximum: H_max = ln(D) at the barycenter (1/D, ..., 1/D).
#     Normalised: H/H_max in [0, 1].  The 93% bound: H/H_max <= 0.93.
#     EITT discovery: H is near-invariant under geometric-mean decimation.
#
#   Geometric-Mean Decimation — temporal resolution compression (EITT core):
#     Given compositions x(t_1), ..., x(t_k) in a block:
#     x_bar_i = C[ exp( (1/k) * SUM(ln(x_i(t_j))) ) ]
#     where C[.] is simplex closure.
#     This is the Aitchison barycenter — the correct CoDa mean.
#     CRITICAL: Arithmetic mean DESTROYS entropy invariance.
#     Only geometric-mean decimation preserves it.
#
#   Bosch-Hale Parameterisation — fusion reactivity <sigma*v>(T):
#     Reference: Bosch & Hale, Nuclear Fusion 32 (1992) 611.
#     Gives <sigma*v> in cm^3/s as a function of ion temperature T in keV
#     for the five primary fusion reactions: D-T, D-D(n), D-D(p), D-He3, T-T.
#     At each T, the five reactivities form a 5-part composition on S^4.
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


import json, math, os, sys
from datetime import datetime

# ─────────────────────────────────────────────────────────
#  Physical constants and Bosch-Hale D-T reactivity
# ─────────────────────────────────────────────────────────

E_ALPHA_J = 5.64e-13    # 3.52 MeV in Joules
E_ALPHA_keV = 3520.0    # 3.52 MeV in keV

# Bremsstrahlung coefficient
# P_brem = C_b * n_20^2 * sqrt(T_keV) * Zeff  [W/m^3]
# where n_20 is density in units of 10^20 m^-3
C_BREM = 5.35e3  # W·m^3·keV^(-1/2)

# Cyclotron coefficient (with wall reflection/reabsorption)
# P_cyc = C_c * n_20 * T^2 * B^2 / (1 + 0.12*T)  approximate
C_CYC = 6.2e1  # W·m·keV^-2·T^-2  (order of magnitude, with reabsorption)

# Line radiation coefficient
C_LINE = 1.0e3  # W·m^3·keV^(-1/2) per Z^2·f_Z


def bosch_hale_DT(T_keV):
    """D-T reactivity <σv> in m^3/s from Bosch-Hale."""
    T = float(T_keV)
    if T < 0.5:
        return 1e-40

    BG = 34.3827
    mrc2 = 1124656.0
    C1, C2, C3 = 1.17302e-9, 1.51361e-2, 7.51886e-2
    C4, C5, C6, C7 = 4.60643e-3, 1.35000e-2, -1.06750e-4, 1.36600e-5

    numer = T * (C2 + T * (C4 + T * C6))
    denom = 1.0 + T * (C3 + T * (C5 + T * C7))
    ratio = numer / denom
    if abs(1.0 - ratio) < 1e-15:
        return 1e-40
    theta = T / (1.0 - ratio)
    if theta <= 0:
        return 1e-40

    xi = (BG ** 2 / (4.0 * theta)) ** (1.0 / 3.0)
    try:
        sv = C1 * theta * math.sqrt(xi / (mrc2 * T ** 3)) * math.exp(-3.0 * xi)
    except (OverflowError, ValueError):
        return 1e-40
    # Convert from cm^3/s to m^3/s
    return max(sv * 1e-6, 1e-40)


def bosch_hale_DHe3(T_keV):
    """D-He3 reactivity <σv> in m^3/s."""
    T = float(T_keV)
    if T < 0.5:
        return 1e-40

    BG = 68.7508
    mrc2 = 1124572.0
    C1 = 5.51036e-10
    C2, C3 = 6.41918e-3, -2.02896e-3
    C4, C5, C6, C7 = -1.91080e-5, 1.35776e-4, 0.0, 0.0

    numer = T * (C2 + T * (C4 + T * C6))
    denom = 1.0 + T * (C3 + T * (C5 + T * C7))
    ratio = numer / denom
    if abs(1.0 - ratio) < 1e-15:
        return 1e-40
    theta = T / (1.0 - ratio)
    if theta <= 0:
        return 1e-40

    xi = (BG ** 2 / (4.0 * theta)) ** (1.0 / 3.0)
    try:
        sv = C1 * theta * math.sqrt(xi / (mrc2 * T ** 3)) * math.exp(-3.0 * xi)
    except (OverflowError, ValueError):
        return 1e-40
    return max(sv * 1e-6, 1e-40)


# ─────────────────────────────────────────────────────────
#  ITER IPB98(y,2) confinement time scaling
# ─────────────────────────────────────────────────────────

def tau_E_iter(I_MA=15.0, B_T=5.3, n_20=1.0, P_MW=50.0,
               R=6.2, a=2.0, kappa=1.7, M=2.5):
    """
    ITER IPB98(y,2) energy confinement time scaling (s).
    τ_E = 0.0562 * I^0.93 * B^0.15 * n_19^0.41 * P^-0.69
          * R^1.97 * ε^0.58 * κ^0.78 * M^0.19
    where ε = a/R, n_19 in 10^19 m^-3
    """
    n_19 = n_20 * 10.0  # convert to 10^19
    epsilon = a / R
    try:
        tau = (0.0562
               * I_MA ** 0.93
               * B_T ** 0.15
               * n_19 ** 0.41
               * max(P_MW, 0.1) ** (-0.69)
               * R ** 1.97
               * epsilon ** 0.58
               * kappa ** 0.78
               * M ** 0.19)
    except (OverflowError, ValueError):
        tau = 0.1
    return max(tau, 0.01)


# ─────────────────────────────────────────────────────────
#  Power balance at a single operating point
# ─────────────────────────────────────────────────────────

def power_balance(T_keV, n_20, B_T=5.3, Zeff=1.5, f_imp=0.02, Z_imp=6):
    """
    Compute all power densities at given (T, n, B, Zeff).
    Returns dict of power components in W/m^3 and derived quantities.
    """
    T = float(T_keV)
    n = float(n_20)

    # Alpha heating: P_α = (1/4) n^2 <σv> E_α
    # Factor 1/4: equal mix D:T, so n_D = n_T = n/2
    sv_dt = bosch_hale_DT(T)
    P_alpha = 0.25 * (n * 1e20) ** 2 * sv_dt * E_ALPHA_J  # W/m^3

    # Bremsstrahlung: P_brem = C_b * n^2 * √T * Zeff
    P_brem = C_BREM * n ** 2 * math.sqrt(max(T, 0.01)) * Zeff

    # Cyclotron (with reabsorption): P_cyc = C_c * n * T^2 * B^2 / (1 + 0.12T)
    P_cyc = C_CYC * n * T ** 2 * B_T ** 2 / (1.0 + 0.12 * T)

    # Line radiation from impurities: P_line = C_L * n^2 * f_imp * Z^2_imp * √T
    P_line = C_LINE * n ** 2 * f_imp * Z_imp ** 2 * math.sqrt(max(T, 0.01))

    # Conduction: P_cond = (3/2) n T / τ_E
    # Need total heating power for τ_E calculation — use iterative approx
    P_heat_est = max(P_alpha, 1.0)  # MW estimate
    V_plasma = 830.0  # m^3 approximate ITER plasma volume
    P_MW = P_heat_est * V_plasma / 1e6
    tau = tau_E_iter(I_MA=15.0, B_T=B_T, n_20=n, P_MW=max(P_MW, 1.0))
    # Energy density: W = (3/2) n_e k_B T -> in useful units:
    # P_cond = 3 * n_20 * 1e20 * T * 1.602e-16 / (2 * τ_E)  W/m^3
    P_cond = 3.0 * n * 1e20 * T * 1.602e-16 / (2.0 * tau)

    # Total losses
    P_loss = P_brem + P_cyc + P_line + P_cond

    # Q factor (ratio of fusion power to external heating needed)
    # P_fusion = 5 * P_alpha (neutrons carry 4x the alpha energy)
    P_fusion = 5.0 * P_alpha
    P_external = max(P_loss - P_alpha, 0.0)
    Q = P_fusion / P_external if P_external > 0 else float('inf')

    # Ignition condition: P_alpha >= P_loss
    ignited = P_alpha >= P_loss

    return {
        "T_keV": T,
        "n_20": n,
        "B_T": B_T,
        "Zeff": Zeff,
        "P_alpha": P_alpha,
        "P_brem": P_brem,
        "P_cyc": P_cyc,
        "P_line": P_line,
        "P_cond": P_cond,
        "P_loss": P_loss,
        "P_fusion": P_fusion,
        "Q": Q,
        "tau_E": tau,
        "ignited": ignited,
        "margin": P_alpha - P_loss,  # positive = ignited
    }


def power_to_composition(pb):
    """Convert power balance to composition (5 channels)."""
    channels = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond"]
    vals = [max(pb[c], 1e-30) for c in channels]
    total = sum(vals)
    return {c: v / total for c, v in zip(channels, vals)}


# ─────────────────────────────────────────────────────────
#  CoDa toolkit (compact)
# ─────────────────────────────────────────────────────────

def clr_transform(x):
    n = len(x)
    x_safe = [max(xi, 1e-20) for xi in x]
    log_x = [math.log(xi) for xi in x_safe]
    mean_log = sum(log_x) / n
    return [lx - mean_log for lx in log_x]


def aitchison_variance(clr_vectors):
    if len(clr_vectors) < 2:
        return 0.0
    n = len(clr_vectors)
    D = len(clr_vectors[0])
    var_sum = 0.0
    for j in range(D):
        col = [v[j] for v in clr_vectors]
        mean_j = sum(col) / n
        var_j = sum((c - mean_j) ** 2 for c in col) / (n - 1)
        var_sum += var_j
    return var_sum / D


def shannon_entropy(x):
    s = sum(x)
    if s <= 0:
        return 0.0
    H = 0.0
    for p in x:
        p_norm = p / s
        if p_norm > 0:
            H -= p_norm * math.log(p_norm)
    return H


def boundary_species(compositions, channels):
    D = len(channels)
    clr_vecs = [clr_transform([c[ch] for ch in channels]) for c in compositions]
    n = len(clr_vecs)
    if n < 2:
        return "?", {}, 0.0

    var_by_ch = {}
    total_var = 0.0
    for j, ch in enumerate(channels):
        col = [v[j] for v in clr_vecs]
        mean_j = sum(col) / n
        var_j = sum((c - mean_j) ** 2 for c in col) / (n - 1)
        var_by_ch[ch] = var_j
        total_var += var_j

    fracs = {ch: var_by_ch[ch] / total_var if total_var > 0 else 0 for ch in channels}
    bs = max(fracs, key=fracs.get)
    return bs, fracs, total_var


def parabola_fit(x, y):
    n = len(x)
    if n < 3:
        return 0, 0, 0, 0.0

    Sx = sum(x); Sx2 = sum(xi**2 for xi in x)
    Sx3 = sum(xi**3 for xi in x); Sx4 = sum(xi**4 for xi in x)
    Sy = sum(y); Sxy = sum(xi*yi for xi, yi in zip(x, y))
    Sx2y = sum(xi**2*yi for xi, yi in zip(x, y))

    M = [[n, Sx, Sx2], [Sx, Sx2, Sx3], [Sx2, Sx3, Sx4]]
    v = [Sy, Sxy, Sx2y]

    def det3(m):
        return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
               -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
               +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))

    D_d = det3(M)
    if abs(D_d) < 1e-30:
        return 0, 0, 0, 0.0

    Ma = [[v[i] if j==0 else M[i][j] for j in range(3)] for i in range(3)]
    Mb = [[v[i] if j==1 else M[i][j] for j in range(3)] for i in range(3)]
    Mc = [[v[i] if j==2 else M[i][j] for j in range(3)] for i in range(3)]

    a = det3(Ma)/D_d; b = det3(Mb)/D_d; c = det3(Mc)/D_d

    y_mean = Sy/n
    ss_tot = sum((yi-y_mean)**2 for yi in y)
    ss_res = sum((yi-(a+b*xi+c*xi**2))**2 for xi, yi in zip(x, y))
    R2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0.0
    return a, b, c, R2


def eitt_test(comp_arrays):
    n = len(comp_arrays)
    D = len(comp_arrays[0])
    H_full = sum(shannon_entropy(c) for c in comp_arrays) / n

    decimated = []
    for i in range(0, n-1, 2):
        gm = [math.sqrt(comp_arrays[i][j]*comp_arrays[i+1][j]) for j in range(D)]
        s = sum(gm)
        decimated.append([g/s for g in gm])

    if not decimated:
        return 100.0, False
    H_dec = sum(shannon_entropy(c) for c in decimated) / len(decimated)
    drift = abs(H_dec - H_full) / abs(H_full) * 100.0 if H_full != 0 else 0.0
    return drift, drift < 1.0


# ─────────────────────────────────────────────────────────
#  PHASE 1: Temperature sweep — find the flip
# ─────────────────────────────────────────────────────────

def phase1_temperature_sweep(n_20=1.0, B_T=5.3, Zeff=1.5):
    """Sweep T from 1-100 keV, track boundary species and ignition."""
    print(f"\n{'='*65}")
    print(f"  PHASE 1: TEMPERATURE SWEEP  (n={n_20}, B={B_T}T, Zeff={Zeff})")
    print(f"{'='*65}")

    channels = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond"]
    temps = [1.0 + i * 0.5 for i in range(199)]  # 1 to 100 keV
    results = []
    compositions = []
    flips = []
    prev_bs = None

    for T in temps:
        pb = power_balance(T, n_20, B_T, Zeff)
        comp = power_to_composition(pb)
        compositions.append(comp)

        # Sliding window boundary species (window of 11)
        if len(compositions) >= 11:
            window = compositions[-11:]
            bs, fracs, _ = boundary_species(window, channels)
        else:
            bs = "P_brem"
            fracs = {}

        if prev_bs and bs != prev_bs:
            flips.append({
                "T_keV": T,
                "from": prev_bs,
                "to": bs,
                "ignited": pb["ignited"],
                "Q": round(pb["Q"], 2) if pb["Q"] < 1e10 else "inf",
                "margin": round(pb["margin"], 2),
            })
            Q_str = f"{pb['Q']:.1f}" if pb['Q'] < 1e10 else "inf"
            print(f"  FLIP at T={T:.1f} keV: {prev_bs} -> {bs}  "
                  f"Q={Q_str}  "
                  f"{'IGNITED' if pb['ignited'] else 'sub-ignition'}")
        prev_bs = bs

        results.append({
            "T_keV": T,
            "boundary_species": bs,
            "P_alpha": pb["P_alpha"],
            "P_brem": pb["P_brem"],
            "P_cyc": pb["P_cyc"],
            "P_line": pb["P_line"],
            "P_cond": pb["P_cond"],
            "Q": pb["Q"],
            "ignited": pb["ignited"],
            "margin": pb["margin"],
        })

    # PLL on the trajectory
    clr_vecs = [clr_transform([c[ch] for ch in channels]) for c in compositions]
    w = 15
    sigma_curve = []
    t_curve = []
    for i in range(w, len(clr_vecs) - w):
        sv = aitchison_variance(clr_vecs[i-w:i+w+1])
        sigma_curve.append(sv)
        t_curve.append(temps[i])

    if len(t_curve) > 5:
        a, b, c, R2 = parabola_fit(t_curve, sigma_curve)
        vertex_T = -b/(2*c) if abs(c) > 1e-15 else 0
        shape = "bowl" if c > 0 else "hill"
        print(f"\n  PLL: R^2={R2:.4f}, {shape}, vertex={vertex_T:.1f} keV")
    else:
        R2, vertex_T, shape = 0, 0, "?"

    # EITT
    comp_arrays = [[c[ch] for ch in channels] for c in compositions]
    drift, passed = eitt_test(comp_arrays)
    print(f"  EITT: drift={drift:.3f}% -> {'PASS' if passed else 'FAIL'}")

    # Find ignition temperature
    ign_T = None
    for r in results:
        if r["ignited"] and ign_T is None:
            ign_T = r["T_keV"]

    print(f"  Ignition temperature: {ign_T:.1f} keV" if ign_T else "  No ignition achieved")
    print(f"  Boundary species flips: {len(flips)}")

    return {
        "phase": 1,
        "label": f"Temperature sweep n={n_20} B={B_T} Zeff={Zeff}",
        "flips": flips,
        "n_flips": len(flips),
        "ignition_T_keV": ign_T,
        "PLL_R2": round(R2, 4),
        "PLL_vertex_keV": round(vertex_T, 1),
        "PLL_shape": shape,
        "EITT_drift": round(drift, 3),
        "EITT_pass": passed,
        "n_points": len(results),
    }


# ─────────────────────────────────────────────────────────
#  PHASE 2: Density sweep — attack from n axis
# ─────────────────────────────────────────────────────────

def phase2_density_sweep(T_keV=15.0, B_T=5.3, Zeff=1.5):
    """Sweep n from 0.1 to 5.0 x 10^2⁰ m⁻^3."""
    print(f"\n{'='*65}")
    print(f"  PHASE 2: DENSITY SWEEP  (T={T_keV} keV, B={B_T}T, Zeff={Zeff})")
    print(f"{'='*65}")

    channels = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond"]
    densities = [0.1 + i * 0.025 for i in range(197)]  # 0.1 to 5.0
    compositions = []
    flips = []
    prev_bs = None

    for n in densities:
        pb = power_balance(T_keV, n, B_T, Zeff)
        comp = power_to_composition(pb)
        compositions.append(comp)

        if len(compositions) >= 11:
            bs, fracs, _ = boundary_species(compositions[-11:], channels)
        else:
            bs = "?"

        if prev_bs and bs != prev_bs:
            flips.append({"n_20": round(n, 3), "from": prev_bs, "to": bs,
                         "ignited": pb["ignited"],
                         "Q": round(pb["Q"], 2) if pb["Q"] < 1e10 else "inf"})
            print(f"  FLIP at n={n:.3f}: {prev_bs} -> {bs}  "
                  f"{'IGNITED' if pb['ignited'] else 'sub-ignition'}")
        prev_bs = bs

    # PLL
    clr_vecs = [clr_transform([c[ch] for ch in channels]) for c in compositions]
    w = 15
    sigma_curve = []; d_curve = []
    for i in range(w, len(clr_vecs) - w):
        sv = aitchison_variance(clr_vecs[i-w:i+w+1])
        sigma_curve.append(sv); d_curve.append(densities[i])

    R2, vertex_n = 0, 0
    if len(d_curve) > 5:
        a, b, c, R2 = parabola_fit(d_curve, sigma_curve)
        vertex_n = -b/(2*c) if abs(c) > 1e-15 else 0
        shape = "bowl" if c > 0 else "hill"
        print(f"\n  PLL: R^2={R2:.4f}, {shape}, vertex n={vertex_n:.2f}x10^2⁰")

    print(f"  Flips: {len(flips)}")

    return {
        "phase": 2,
        "label": f"Density sweep T={T_keV} B={B_T} Zeff={Zeff}",
        "flips": flips, "n_flips": len(flips),
        "PLL_R2": round(R2, 4),
        "PLL_vertex_n20": round(vertex_n, 3),
    }


# ─────────────────────────────────────────────────────────
#  PHASE 3: Zeff sweep — the impurity control knob
# ─────────────────────────────────────────────────────────

def phase3_zeff_sweep(T_keV=15.0, n_20=1.0, B_T=5.3):
    """
    Zeff directly scales Bremsstrahlung.  Sweep from 1.0 (pure DT)
    to 4.0 (heavily contaminated).
    """
    print(f"\n{'='*65}")
    print(f"  PHASE 3: IMPURITY (Zeff) SWEEP  (T={T_keV}, n={n_20}, B={B_T})")
    print(f"{'='*65}")

    channels = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond"]
    zeffs = [1.0 + i * 0.015 for i in range(201)]  # 1.0 to 4.0
    compositions = []
    flips = []
    prev_bs = None
    ignition_lost_at = None

    for z in zeffs:
        pb = power_balance(T_keV, n_20, B_T, z)
        comp = power_to_composition(pb)
        compositions.append(comp)

        if len(compositions) >= 7:
            bs, fracs, _ = boundary_species(compositions[-7:], channels)
        else:
            bs = "?"

        if prev_bs and bs != prev_bs:
            flips.append({"Zeff": round(z, 3), "from": prev_bs, "to": bs,
                         "ignited": pb["ignited"]})
            print(f"  FLIP at Zeff={z:.3f}: {prev_bs} -> {bs}")

        if not pb["ignited"] and ignition_lost_at is None and z > 1.0:
            ignition_lost_at = round(z, 3)

        prev_bs = bs

    # Track Bremsstrahlung fraction across Zeff
    brem_fracs = []
    for comp in compositions:
        total = sum(comp[ch] for ch in channels)
        brem_fracs.append(comp["P_brem"] / total if total > 0 else 0)

    print(f"  Brem fraction at Zeff=1.0: {brem_fracs[0]*100:.1f}%")
    print(f"  Brem fraction at Zeff=4.0: {brem_fracs[-1]*100:.1f}%")
    if ignition_lost_at:
        print(f"  Ignition lost at Zeff = {ignition_lost_at}")
    else:
        print(f"  Ignition maintained across full Zeff range")

    return {
        "phase": 3,
        "label": f"Zeff sweep T={T_keV} n={n_20}",
        "flips": flips,
        "ignition_lost_at_Zeff": ignition_lost_at,
        "brem_frac_Zeff1": round(brem_fracs[0], 4),
        "brem_frac_Zeff4": round(brem_fracs[-1], 4),
    }


# ─────────────────────────────────────────────────────────
#  PHASE 4: B-field sweep — cyclotron vs Bremsstrahlung
# ─────────────────────────────────────────────────────────

def phase4_bfield_sweep(T_keV=15.0, n_20=1.0, Zeff=1.5):
    """Sweep B from 1 to 15 Tesla."""
    print(f"\n{'='*65}")
    print(f"  PHASE 4: MAGNETIC FIELD SWEEP  (T={T_keV}, n={n_20}, Zeff={Zeff})")
    print(f"{'='*65}")

    channels = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond"]
    bfields = [1.0 + i * 0.07 for i in range(201)]  # 1 to 15 T
    compositions = []
    flips = []
    prev_bs = None

    for B in bfields:
        pb = power_balance(T_keV, n_20, B, Zeff)
        comp = power_to_composition(pb)
        compositions.append(comp)

        if len(compositions) >= 7:
            bs, fracs, _ = boundary_species(compositions[-7:], channels)
        else:
            bs = "?"

        if prev_bs and bs != prev_bs:
            flips.append({"B_T": round(B, 2), "from": prev_bs, "to": bs,
                         "ignited": pb["ignited"]})
            print(f"  FLIP at B={B:.2f}T: {prev_bs} -> {bs}")
        prev_bs = bs

    print(f"  Flips: {len(flips)}")
    return {
        "phase": 4,
        "label": f"B-field sweep T={T_keV} n={n_20} Zeff={Zeff}",
        "flips": flips, "n_flips": len(flips),
    }


# ─────────────────────────────────────────────────────────
#  PHASE 5: Full (n, T) plane scan
# ─────────────────────────────────────────────────────────

def phase5_nT_plane(B_T=5.3, Zeff=1.5):
    """
    2D scan across the (n, T) ignition landscape.
    Map boundary species, ignition boundary, Q contours.
    """
    print(f"\n{'='*65}")
    print(f"  PHASE 5: (n, T) PLANE SCAN  (B={B_T}T, Zeff={Zeff})")
    print(f"{'='*65}")

    channels = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond"]
    temps = [5.0 + i * 1.0 for i in range(96)]      # 5-100 keV
    densities = [0.2 + i * 0.1 for i in range(49)]   # 0.2-5.0 x10^2⁰

    grid = []
    ignition_boundary = []
    bs_map = {}

    for n in densities:
        prev_ignited = False
        for T in temps:
            pb = power_balance(T, n, B_T, Zeff)
            comp = power_to_composition(pb)

            # Per-point boundary species (instantaneous)
            vals = [comp[ch] for ch in channels]
            clr = clr_transform(vals)
            max_idx = max(range(len(clr)), key=lambda i: abs(clr[i]))
            inst_bs = channels[max_idx]

            grid.append({
                "T": T, "n": n,
                "ignited": pb["ignited"],
                "Q": min(pb["Q"], 1e6),
                "margin": pb["margin"],
                "bs": inst_bs,
                "brem_frac": comp["P_brem"],
                "alpha_frac": comp["P_alpha"],
            })

            # Track ignition boundary
            if pb["ignited"] and not prev_ignited:
                ignition_boundary.append({"n_20": round(n, 2), "T_keV": T})
            prev_ignited = pb["ignited"]

    # Count boundary species in different regions
    pre_ignition = [g for g in grid if not g["ignited"]]
    post_ignition = [g for g in grid if g["ignited"]]

    pre_bs_count = {}
    for g in pre_ignition:
        pre_bs_count[g["bs"]] = pre_bs_count.get(g["bs"], 0) + 1

    post_bs_count = {}
    for g in post_ignition:
        post_bs_count[g["bs"]] = post_bs_count.get(g["bs"], 0) + 1

    print(f"\n  Grid: {len(temps)} x {len(densities)} = {len(grid)} points")
    print(f"  Ignited: {len(post_ignition)} / {len(grid)} ({100*len(post_ignition)/len(grid):.1f}%)")
    print(f"\n  Pre-ignition boundary species distribution:")
    for bs, count in sorted(pre_bs_count.items(), key=lambda x: -x[1]):
        print(f"    {bs:12s}: {count:5d} ({100*count/max(len(pre_ignition),1):.1f}%)")
    print(f"\n  Post-ignition boundary species distribution:")
    for bs, count in sorted(post_bs_count.items(), key=lambda x: -x[1]):
        print(f"    {bs:12s}: {count:5d} ({100*count/max(len(post_ignition),1):.1f}%)")

    print(f"\n  Ignition boundary (minimum T for each n):")
    for ib in ignition_boundary[:10]:
        print(f"    n={ib['n_20']:.1f}x10^2⁰  ->  T_ign={ib['T_keV']:.0f} keV")
    if len(ignition_boundary) > 10:
        print(f"    ... ({len(ignition_boundary)} boundary points total)")

    return {
        "phase": 5,
        "label": f"(n,T) plane B={B_T} Zeff={Zeff}",
        "grid_size": len(grid),
        "n_ignited": len(post_ignition),
        "frac_ignited": round(len(post_ignition)/len(grid), 4),
        "pre_ignition_bs": pre_bs_count,
        "post_ignition_bs": post_bs_count,
        "ignition_boundary": ignition_boundary,
    }


# ─────────────────────────────────────────────────────────
#  PHASE 6: Path to ignition — optimal trajectory
# ─────────────────────────────────────────────────────────

def phase6_ignition_path(B_T=5.3, Zeff=1.5):
    """
    Simulate a startup trajectory: simultaneous density ramp and
    temperature ramp from cold to burning plasma.
    Track the compositional evolution and boundary species flips.
    """
    print(f"\n{'='*65}")
    print(f"  PHASE 6: PATH TO IGNITION  (B={B_T}T, Zeff={Zeff})")
    print(f"{'='*65}")

    channels = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond"]

    # Three startup paths:
    paths = {
        "Path A: T-first (ITER-like)": {
            "desc": "Heat at low density, then ramp n",
            "trajectory": [],
        },
        "Path B: n-first (high-density)": {
            "desc": "Compress to high density, then heat",
            "trajectory": [],
        },
        "Path C: diagonal (balanced)": {
            "desc": "Simultaneous T and n ramp",
            "trajectory": [],
        },
    }

    # Path A: T from 2->20 at n=0.3, then n from 0.3->2.0 at T=20
    for i in range(100):
        T = 2.0 + i * 0.18   # 2 -> 20 keV
        n = 0.3
        paths["Path A: T-first (ITER-like)"]["trajectory"].append((T, n))
    for i in range(100):
        T = 20.0
        n = 0.3 + i * 0.017  # 0.3 -> 2.0
        paths["Path A: T-first (ITER-like)"]["trajectory"].append((T, n))

    # Path B: n from 0.3->2.0 at T=3, then T from 3->20 at n=2.0
    for i in range(100):
        T = 3.0
        n = 0.3 + i * 0.017
        paths["Path B: n-first (high-density)"]["trajectory"].append((T, n))
    for i in range(100):
        T = 3.0 + i * 0.17
        n = 2.0
        paths["Path B: n-first (high-density)"]["trajectory"].append((T, n))

    # Path C: diagonal
    for i in range(200):
        T = 2.0 + i * 0.09   # 2 -> 20
        n = 0.3 + i * 0.0085  # 0.3 -> 2.0
        paths["Path C: diagonal (balanced)"]["trajectory"].append((T, n))

    path_results = {}

    for name, pdata in paths.items():
        print(f"\n  --- {name} ---")
        print(f"  {pdata['desc']}")

        traj = pdata["trajectory"]
        compositions = []
        flips = []
        prev_bs = None
        ignition_step = None

        for step, (T, n) in enumerate(traj):
            pb = power_balance(T, n, B_T, Zeff)
            comp = power_to_composition(pb)
            compositions.append(comp)

            if len(compositions) >= 7:
                bs, fracs, _ = boundary_species(compositions[-7:], channels)
            else:
                bs = "?"

            if prev_bs and bs != prev_bs:
                flips.append({
                    "step": step, "T_keV": round(T, 1), "n_20": round(n, 2),
                    "from": prev_bs, "to": bs, "ignited": pb["ignited"],
                })
                print(f"    Step {step:3d}: FLIP {prev_bs} -> {bs} "
                      f"(T={T:.1f}, n={n:.2f}) "
                      f"{'*** IGNITED ***' if pb['ignited'] else ''}")

            if pb["ignited"] and ignition_step is None:
                ignition_step = step
                print(f"    Step {step:3d}: *** IGNITION *** T={T:.1f} keV, n={n:.2f}x10^2⁰")

            prev_bs = bs

        # PLL on path
        clr_vecs = [clr_transform([c[ch] for ch in channels]) for c in compositions]
        w = 10
        sigma_curve = []; idx_curve = []
        for i in range(w, len(clr_vecs)-w):
            sv = aitchison_variance(clr_vecs[i-w:i+w+1])
            sigma_curve.append(sv); idx_curve.append(i)

        R2 = 0
        if len(idx_curve) > 5:
            _, _, _, R2 = parabola_fit(idx_curve, sigma_curve)

        # EITT
        comp_arrays = [[c[ch] for ch in channels] for c in compositions]
        drift, passed = eitt_test(comp_arrays)

        print(f"    PLL R^2={R2:.4f}, EITT drift={drift:.3f}%")
        print(f"    Flips: {len(flips)}, Ignition at step: {ignition_step}")

        path_results[name] = {
            "flips": flips, "n_flips": len(flips),
            "ignition_step": ignition_step,
            "PLL_R2": round(R2, 4),
            "EITT_drift": round(drift, 3),
            "EITT_pass": passed,
        }

    return {"phase": 6, "paths": path_results}


# ─────────────────────────────────────────────────────────
#  PHASE 7: Zeff as attack vector — find the kill zone
# ─────────────────────────────────────────────────────────

def phase7_zeff_kill_zone():
    """
    For each temperature, find the critical Zeff where ignition is lost.
    This maps the "kill surface" in (T, Zeff) space.
    """
    print(f"\n{'='*65}")
    print(f"  PHASE 7: Zeff KILL ZONE — critical impurity levels")
    print(f"{'='*65}")

    kill_surface = []
    for T in range(5, 101):
        for n_test in [0.5, 1.0, 1.5, 2.0]:
            # Binary search for critical Zeff
            z_lo, z_hi = 1.0, 10.0
            # First check if ignition possible at Zeff=1
            pb = power_balance(T, n_test, 5.3, 1.0)
            if not pb["ignited"]:
                continue

            for _ in range(30):
                z_mid = (z_lo + z_hi) / 2
                pb = power_balance(T, n_test, 5.3, z_mid)
                if pb["ignited"]:
                    z_lo = z_mid
                else:
                    z_hi = z_mid

            z_crit = (z_lo + z_hi) / 2
            kill_surface.append({
                "T_keV": T,
                "n_20": n_test,
                "Zeff_critical": round(z_crit, 3),
            })

    # Report
    print(f"\n  Kill surface: {len(kill_surface)} points")
    for n_test in [0.5, 1.0, 1.5, 2.0]:
        points = [k for k in kill_surface if k["n_20"] == n_test]
        if points:
            min_z = min(k["Zeff_critical"] for k in points)
            max_z = max(k["Zeff_critical"] for k in points)
            T_at_max_z = max(points, key=lambda k: k["Zeff_critical"])
            print(f"  n={n_test}: Zeff_crit range [{min_z:.2f}, {max_z:.2f}], "
                  f"most tolerant at T={T_at_max_z['T_keV']} keV")

    return {"phase": 7, "kill_surface": kill_surface}


# ─────────────────────────────────────────────────────────
#  PHASE 8: Aneutronic escape — does D-He3 bypass Brem?
# ─────────────────────────────────────────────────────────

def phase8_aneutronic():
    """
    D-He3 fusion: no neutrons, all charged products (proton + alpha).
    All fusion energy heats plasma directly — no neutron losses.
    But higher Coulomb barrier means higher T needed.
    Does the boundary species analysis change?
    """
    print(f"\n{'='*65}")
    print(f"  PHASE 8: ANEUTRONIC ESCAPE — D-He3 pathway")
    print(f"{'='*65}")

    channels = ["P_alpha_p", "P_brem", "P_cyc", "P_line", "P_cond"]
    temps = [10.0 + i * 2.0 for i in range(196)]  # 10-400 keV
    compositions = []
    flips = []
    prev_bs = None
    ignition_step = None

    E_DHe3 = 18.3 * 1.602e-16 * 1e3  # 18.3 MeV in J — ALL to charged particles

    for T in temps:
        n_20 = 2.0  # higher density needed for D-He3
        B_T = 8.0   # stronger field for higher-T confinement

        sv = bosch_hale_DHe3(T)
        # n_D = n_He3 = n/2 (assuming equal mix)
        P_fusion = 0.25 * (n_20 * 1e20) ** 2 * sv * E_DHe3

        P_brem = C_BREM * n_20 ** 2 * math.sqrt(max(T, 0.01)) * 1.33  # Zeff ≈ 1.33 for D-He3
        P_cyc = C_CYC * n_20 * T ** 2 * B_T ** 2 / (1.0 + 0.12 * T)
        P_line = C_LINE * n_20 ** 2 * 0.01 * 4 * math.sqrt(max(T, 0.01))  # low impurity

        P_MW = max(P_fusion * 830 / 1e6, 1.0)
        tau = tau_E_iter(I_MA=15.0, B_T=B_T, n_20=n_20, P_MW=P_MW)
        P_cond = 3.0 * n_20 * 1e20 * T * 1.602e-16 / (2.0 * tau)

        vals = [max(P_fusion, 1e-30), max(P_brem, 1e-30),
                max(P_cyc, 1e-30), max(P_line, 1e-30), max(P_cond, 1e-30)]
        total = sum(vals)
        comp = {ch: v/total for ch, v in zip(channels, vals)}
        compositions.append(comp)

        ignited = P_fusion >= (P_brem + P_cyc + P_line + P_cond)

        if len(compositions) >= 7:
            bs, fracs, _ = boundary_species(compositions[-7:], channels)
        else:
            bs = "?"

        if prev_bs and bs != prev_bs:
            flips.append({"T_keV": T, "from": prev_bs, "to": bs, "ignited": ignited})
            print(f"  FLIP at T={T:.0f} keV: {prev_bs} -> {bs} "
                  f"{'IGNITED' if ignited else ''}")

        if ignited and ignition_step is None:
            ignition_step = T
            print(f"  *** D-He3 IGNITION at T={T:.0f} keV ***")

        prev_bs = bs

    # Global boundary species
    bs_global, fracs_global, _ = boundary_species(compositions, channels)
    print(f"\n  Global boundary species: {bs_global}")
    for ch in channels:
        print(f"    {ch:12s}: {fracs_global.get(ch, 0)*100:.1f}%")
    print(f"  D-He3 ignition temperature: {ignition_step} keV" if ignition_step
          else "  D-He3 does NOT ignite in this parameter range")

    # EITT
    comp_arrays = [[c[ch] for ch in channels] for c in compositions]
    drift, passed = eitt_test(comp_arrays)
    print(f"  EITT: drift={drift:.3f}% -> {'PASS' if passed else 'FAIL'}")

    return {
        "phase": 8,
        "label": "D-He3 aneutronic pathway",
        "global_boundary_species": bs_global,
        "boundary_fracs": {k: round(v, 4) for k, v in fracs_global.items()},
        "ignition_T_keV": ignition_step,
        "flips": flips,
        "EITT_drift": round(drift, 3),
    }


# ─────────────────────────────────────────────────────────
#  PHASE 9: Frequency analysis — σ^2_A spectral decomposition
# ─────────────────────────────────────────────────────────

def phase9_frequency_analysis():
    """
    Treat σ^2_A(T) along the temperature sweep as a 1D signal.
    Compute its 'spectrum' via polynomial residual decomposition
    at different scales.
    """
    print(f"\n{'='*65}")
    print(f"  PHASE 9: FREQUENCY / SCALE DECOMPOSITION")
    print(f"{'='*65}")

    channels = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond"]
    temps = [1.0 + i * 0.5 for i in range(199)]
    compositions = []

    for T in temps:
        pb = power_balance(T, 1.0, 5.3, 1.5)
        compositions.append(power_to_composition(pb))

    clr_vecs = [clr_transform([c[ch] for ch in channels]) for c in compositions]

    # Multi-scale σ^2_A: different window sizes
    scales = [5, 10, 15, 25, 40, 60]
    scale_results = []

    for w in scales:
        sigma_curve = []; t_curve = []
        for i in range(w, len(clr_vecs)-w):
            sv = aitchison_variance(clr_vecs[i-w:i+w+1])
            sigma_curve.append(sv); t_curve.append(temps[i])

        if len(t_curve) < 10:
            continue

        _, _, _, R2 = parabola_fit(t_curve, sigma_curve)

        # Variance of σ^2_A curve itself
        mean_s = sum(sigma_curve) / len(sigma_curve)
        var_s = sum((s - mean_s)**2 for s in sigma_curve) / len(sigma_curve)

        scale_results.append({
            "window": w,
            "window_keV": round(w * 0.5, 1),
            "n_points": len(t_curve),
            "mean_sigma2_A": round(mean_s, 4),
            "var_sigma2_A": round(var_s, 6),
            "PLL_R2": round(R2, 4),
        })
        print(f"  Window {w:2d} ({w*0.5:.1f} keV): mean σ^2_A={mean_s:.4f}, "
              f"var(σ^2_A)={var_s:.6f}, PLL R^2={R2:.4f}")

    # Vertex theorem inner product spectrum
    print(f"\n  Vertex theorem zero crossings by scale:")
    for w in [5, 15, 30]:
        if w >= len(clr_vecs) // 3:
            continue
        # Compute inner products at this scale
        crossings = 0
        prev_ip = None
        for i in range(w, len(clr_vecs)-w):
            dt = 1.0
            deriv = [(clr_vecs[min(i+w, len(clr_vecs)-1)][j] -
                      clr_vecs[max(i-w, 0)][j]) / (2*w) for j in range(5)]
            ip = sum(clr_vecs[i][j] * deriv[j] for j in range(5))
            if prev_ip is not None and prev_ip * ip < 0:
                crossings += 1
            prev_ip = ip
        print(f"    Scale w={w}: {crossings} zero crossings")

    return {"phase": 9, "scale_results": scale_results}


# ─────────────────────────────────────────────────────────
#  PHASE 10: The flip catalogue
# ─────────────────────────────────────────────────────────

def phase10_flip_catalogue():
    """
    Systematic catalogue of every boundary species flip in the
    (T, n, Zeff) parameter space.  Where does Brem lose control?
    """
    print(f"\n{'='*65}")
    print(f"  PHASE 10: COMPREHENSIVE FLIP CATALOGUE")
    print(f"{'='*65}")

    channels = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond"]
    flips = []

    # Scan T at multiple (n, Zeff) combinations
    conditions = [
        (0.5, 1.0), (0.5, 1.5), (0.5, 2.0), (0.5, 3.0),
        (1.0, 1.0), (1.0, 1.5), (1.0, 2.0), (1.0, 3.0),
        (1.5, 1.0), (1.5, 1.5), (1.5, 2.0), (1.5, 3.0),
        (2.0, 1.0), (2.0, 1.5), (2.0, 2.0), (2.0, 3.0),
        (3.0, 1.0), (3.0, 1.5), (3.0, 2.0), (3.0, 3.0),
    ]

    for n_20, Zeff in conditions:
        compositions = []
        prev_bs = None
        for Ti in range(1, 101):
            T = float(Ti)
            pb = power_balance(T, n_20, 5.3, Zeff)
            comp = power_to_composition(pb)
            compositions.append(comp)

            if len(compositions) >= 5:
                bs, _, _ = boundary_species(compositions[-5:], channels)
            else:
                bs = "?"

            if prev_bs and bs != prev_bs:
                flips.append({
                    "n_20": n_20, "Zeff": Zeff, "T_keV": T,
                    "from": prev_bs, "to": bs,
                    "ignited": pb["ignited"],
                })
            prev_bs = bs

    # Analyse flip patterns
    from_brem = [f for f in flips if f["from"] == "P_brem"]
    to_brem = [f for f in flips if f["to"] == "P_brem"]
    at_ignition = [f for f in flips if f["ignited"]]

    print(f"\n  Total flips catalogued: {len(flips)}")
    print(f"  Flips FROM Bremsstrahlung: {len(from_brem)}")
    print(f"  Flips TO Bremsstrahlung: {len(to_brem)}")
    print(f"  Flips at ignition: {len(at_ignition)}")

    # What does Brem flip to?
    brem_destinations = {}
    for f in from_brem:
        dest = f["to"]
        brem_destinations[dest] = brem_destinations.get(dest, 0) + 1

    print(f"\n  When Brem loses boundary status, it flips to:")
    for dest, count in sorted(brem_destinations.items(), key=lambda x: -x[1]):
        print(f"    {dest:12s}: {count} times")

    # Temperature ranges where Brem is NOT the boundary species
    print(f"\n  Representative flip temperatures (from Brem):")
    for f in from_brem[:15]:
        print(f"    n={f['n_20']}, Zeff={f['Zeff']}: T={f['T_keV']} keV -> {f['to']} "
              f"{'[IGNITED]' if f['ignited'] else ''}")

    return {
        "phase": 10,
        "total_flips": len(flips),
        "from_brem": len(from_brem),
        "to_brem": len(to_brem),
        "at_ignition": len(at_ignition),
        "brem_destinations": brem_destinations,
        "all_flips": flips,
    }


# ─────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  EXP-06B  BREMSSTRAHLUNG BOUNDARY ATTACK")
    print("  Full-spectrum compositional assault on the ignition barrier")
    print("=" * 65)

    all_results = {}

    # Phase 1: Temperature sweeps at different conditions
    all_results["phase1_default"] = phase1_temperature_sweep(n_20=1.0, B_T=5.3, Zeff=1.5)
    all_results["phase1_high_n"] = phase1_temperature_sweep(n_20=2.0, B_T=5.3, Zeff=1.5)
    all_results["phase1_clean"] = phase1_temperature_sweep(n_20=1.0, B_T=5.3, Zeff=1.0)
    all_results["phase1_dirty"] = phase1_temperature_sweep(n_20=1.0, B_T=5.3, Zeff=3.0)

    # Phase 2: Density sweeps
    all_results["phase2_15keV"] = phase2_density_sweep(T_keV=15.0)
    all_results["phase2_25keV"] = phase2_density_sweep(T_keV=25.0)

    # Phase 3: Zeff sweeps
    all_results["phase3_15keV"] = phase3_zeff_sweep(T_keV=15.0)
    all_results["phase3_25keV"] = phase3_zeff_sweep(T_keV=25.0)
    all_results["phase3_50keV"] = phase3_zeff_sweep(T_keV=50.0)

    # Phase 4: B-field
    all_results["phase4"] = phase4_bfield_sweep()

    # Phase 5: (n,T) plane
    all_results["phase5"] = phase5_nT_plane()

    # Phase 6: Paths to ignition
    all_results["phase6"] = phase6_ignition_path()

    # Phase 7: Zeff kill zone
    all_results["phase7"] = phase7_zeff_kill_zone()

    # Phase 8: Aneutronic escape
    all_results["phase8"] = phase8_aneutronic()

    # Phase 9: Frequency analysis
    all_results["phase9"] = phase9_frequency_analysis()

    # Phase 10: Flip catalogue
    all_results["phase10"] = phase10_flip_catalogue()

    # ── GRAND SUMMARY ──
    print(f"\n{'='*65}")
    print(f"  GRAND SUMMARY — BREMSSTRAHLUNG BOUNDARY ATTACK")
    print(f"{'='*65}")

    p1 = all_results["phase1_default"]
    p5 = all_results["phase5"]
    p6 = all_results["phase6"]
    p7 = all_results["phase7"]
    p8 = all_results["phase8"]
    p10 = all_results["phase10"]

    print(f"\n  Default ignition temperature: {p1.get('ignition_T_keV', '?')} keV")
    print(f"  PLL vertex (T-sweep): {p1.get('PLL_vertex_keV', '?')} keV")
    print(f"  Ignited fraction of (n,T) plane: {p5.get('frac_ignited', 0)*100:.1f}%")
    print(f"  Total boundary species flips catalogued: {p10.get('total_flips', 0)}")
    print(f"  Flips FROM Bremsstrahlung: {p10.get('from_brem', 0)}")
    print(f"  D-He3 aneutronic ignition: {p8.get('ignition_T_keV', 'NOT ACHIEVED')}")

    # Path comparison
    if "paths" in p6:
        print(f"\n  Path comparison:")
        for name, data in p6["paths"].items():
            ign = data.get("ignition_step", "never")
            nf = data.get("n_flips", 0)
            print(f"    {name:35s}: ignition step={ign}, flips={nf}")

    # ── Save ──
    output = {
        "experiment": "EXP-06B",
        "title": "Bremsstrahlung Boundary Attack",
        "date": datetime.now().isoformat(),
        "author": "Peter Higgins",
        "computed_by": "Claude (Anthropic)",
        "phases": 10,
        "results": {},
    }

    for key, val in all_results.items():
        # Serialise, truncating large arrays
        try:
            serialised = json.loads(json.dumps(val, default=str))
        except:
            serialised = str(val)

        # Truncate flip lists if huge
        if isinstance(serialised, dict) and "all_flips" in serialised:
            if len(serialised["all_flips"]) > 100:
                serialised["all_flips_sample"] = serialised["all_flips"][:50]
                serialised["all_flips_count"] = len(serialised["all_flips"])
                del serialised["all_flips"]

        if isinstance(serialised, dict) and "kill_surface" in serialised:
            if len(serialised["kill_surface"]) > 100:
                serialised["kill_surface_sample"] = serialised["kill_surface"][::5]
                serialised["kill_surface_count"] = len(serialised["kill_surface"])
                del serialised["kill_surface"]

        output["results"][key] = serialised

    outpath = os.path.join(os.path.dirname(__file__), "exp06b_brem_attack.json")
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {outpath}")

    return output


if __name__ == "__main__":
    main()
