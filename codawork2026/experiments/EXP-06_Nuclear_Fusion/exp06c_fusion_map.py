#!/usr/bin/env python3
"""
EXP-06C  CORRECTED FULL-KIT FUSION MAP
=======================================
Series 2, Experiment 1 — Final integrated run

Corrections from EXP-06B boundary attack:
  1. Line radiation (impurity Z^2-scaled) is the true instantaneous
     boundary species, not Bremsstrahlung
  2. Conduction (tau_E governed) is the ignition-window boundary species
  3. Bremsstrahlung is the floor — constant drain, low CLR variance
  4. Diagonal startup path is optimal (fewest flips, fastest ignition)
  5. D-He3 aneutronic does NOT ignite in magnetic confinement
  6. Density is the escape route — buys Zeff tolerance margin

This script maps the complete path to ignition step by step,
applying every HUF tool at every stage:

  STEP 1  Cold plasma startup (T=1-5 keV)
  STEP 2  Ohmic heating plateau (T=5-8 keV)
  STEP 3  Auxiliary heating ramp (T=8-12 keV)
  STEP 4  L-H transition zone (T=12-15 keV)
  STEP 5  H-mode approach to ignition (T=15-20 keV)
  STEP 6  Burning plasma (T=20-30 keV)
  STEP 7  Thermonuclear burn (T=30-50 keV)

At each step we run the FULL kit:
  - EITT integrity
  - PLL parabola (local and cumulative)
  - Noise squeeze
  - Vertex theorem
  - Boundary species decomposition
  - Flip detection
  - Q-factor tracking
  - Ignition margin

Then we do cross-step analysis:
  - Full trajectory PLL
  - Boundary species evolution map
  - Cumulative noise squeeze
  - Vertex theorem across the entire path
  - Comparison: 3 startup strategies (T-first, n-first, diagonal)

Physics model (corrected):
  P_alpha = (1/4) n^2 <sigma_v>_DT E_alpha
  P_brem  = 5.35e3 * n^2 * sqrt(T) * Zeff
  P_cyc   = 6.2e1 * n * T^2 * B^2 / (1 + 0.12*T)
  P_line  = 1.0e3 * n^2 * f_Z * Z_imp^2 * sqrt(T)
  P_cond  = 3 * n * 1e20 * T * 1.602e-16 / (2 * tau_E)
  P_ohmic = eta * J^2 (Ohmic heating, Spitzer resistivity)

  tau_E from ITER IPB98(y,2) scaling

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


import json, math, os
from datetime import datetime

# ============================================================
#  PHYSICS ENGINE
# ============================================================

E_ALPHA_J = 5.64e-13
C_BREM = 5.35e3
C_CYC = 6.2e1
C_LINE = 1.0e3


def bosch_hale_DT(T):
    """D-T reactivity <sigma_v> in m^3/s."""
    T = float(T)
    if T < 0.5:
        return 1e-40
    BG, mrc2 = 34.3827, 1124656.0
    C1, C2, C3 = 1.17302e-9, 1.51361e-2, 7.51886e-2
    C4, C5, C6, C7 = 4.60643e-3, 1.35e-2, -1.0675e-4, 1.366e-5
    numer = T * (C2 + T * (C4 + T * C6))
    denom = 1.0 + T * (C3 + T * (C5 + T * C7))
    r = numer / denom
    if abs(1.0 - r) < 1e-15:
        return 1e-40
    theta = T / (1.0 - r)
    if theta <= 0:
        return 1e-40
    xi = (BG**2 / (4.0 * theta))**(1.0/3.0)
    try:
        sv = C1 * theta * math.sqrt(xi / (mrc2 * T**3)) * math.exp(-3.0 * xi)
    except (OverflowError, ValueError):
        return 1e-40
    return max(sv * 1e-6, 1e-40)


def tau_E(I_MA=15.0, B_T=5.3, n_20=1.0, P_MW=50.0,
          R=6.2, a=2.0, kappa=1.7, M=2.5):
    """ITER IPB98(y,2) energy confinement time (s)."""
    n_19 = n_20 * 10.0
    eps = a / R
    try:
        t = (0.0562 * I_MA**0.93 * B_T**0.15 * n_19**0.41
             * max(P_MW, 0.1)**(-0.69) * R**1.97
             * eps**0.58 * kappa**0.78 * M**0.19)
    except (OverflowError, ValueError):
        t = 0.1
    return max(t, 0.01)


def power_balance(T, n, B=5.3, Zeff=1.5, f_imp=0.02, Z_imp=6):
    """Full power balance at (T keV, n x10^20 m^-3, B Tesla, Zeff)."""
    sv = bosch_hale_DT(T)
    P_alpha = 0.25 * (n * 1e20)**2 * sv * E_ALPHA_J
    P_brem = C_BREM * n**2 * math.sqrt(max(T, 0.01)) * Zeff
    P_cyc = C_CYC * n * T**2 * B**2 / (1.0 + 0.12 * T)
    P_line = C_LINE * n**2 * f_imp * Z_imp**2 * math.sqrt(max(T, 0.01))
    # Ohmic heating (Spitzer): P_ohmic ~ eta_0 * T^(-3/2) * J^2
    # At ITER current density J ~ 1 MA/m^2:
    P_ohmic = 5e3 * max(T, 0.1)**(-1.5)  # approximate W/m^3
    # Conduction
    V = 830.0
    P_heat = max(P_alpha + P_ohmic, 1.0)
    P_MW = P_heat * V / 1e6
    te = tau_E(B_T=B, n_20=n, P_MW=max(P_MW, 1.0))
    P_cond = 3.0 * n * 1e20 * T * 1.602e-16 / (2.0 * te)
    P_loss = P_brem + P_cyc + P_line + P_cond
    P_gain = P_alpha + P_ohmic  # total heating
    P_fusion = 5.0 * P_alpha
    P_ext = max(P_loss - P_alpha, 0.0)  # external needed if alpha alone insufficient
    Q = P_fusion / P_ext if P_ext > 1e-30 else float('inf')
    # TRUE ignition: alpha ALONE sustains burn (no Ohmic needed)
    ignited = P_alpha >= P_loss

    return {
        "T": T, "n": n, "B": B, "Zeff": Zeff,
        "P_alpha": P_alpha, "P_brem": P_brem, "P_cyc": P_cyc,
        "P_line": P_line, "P_cond": P_cond, "P_ohmic": P_ohmic,
        "P_loss": P_loss, "P_gain": P_gain,
        "P_fusion": P_fusion, "Q": Q, "tau_E": te,
        "ignited": ignited, "margin": P_gain - P_loss,
    }


# ============================================================
#  COMPOSITIONAL ENGINE (6 channels now: alpha, brem, cyc, line, cond, ohmic)
# ============================================================

CHANNELS = ["P_alpha", "P_brem", "P_cyc", "P_line", "P_cond", "P_ohmic"]
CH_SHORT = {"P_alpha": "Alpha", "P_brem": "Brem", "P_cyc": "Cyclo",
            "P_line": "Line", "P_cond": "Cond", "P_ohmic": "Ohmic"}


def pb_to_comp(pb):
    """Power balance dict -> closed composition (6 parts)."""
    vals = [max(pb[ch], 1e-30) for ch in CHANNELS]
    s = sum(vals)
    return [v / s for v in vals]


def clr(x):
    n = len(x)
    safe = [max(xi, 1e-20) for xi in x]
    lg = [math.log(xi) for xi in safe]
    m = sum(lg) / n
    return [l - m for l in lg]


def aitchison_var(clr_vecs):
    if len(clr_vecs) < 2:
        return 0.0
    n = len(clr_vecs)
    D = len(clr_vecs[0])
    vs = 0.0
    for j in range(D):
        col = [v[j] for v in clr_vecs]
        mu = sum(col) / n
        vs += sum((c - mu)**2 for c in col) / (n - 1)
    return vs / D


def shannon_H(x):
    s = sum(x)
    if s <= 0:
        return 0.0
    h = 0.0
    for p in x:
        pn = p / s
        if pn > 0:
            h -= pn * math.log(pn)
    return h


def eitt(comps):
    """EITT on list of composition arrays. Returns (drift%, passed)."""
    n = len(comps)
    D = len(comps[0])
    H_full = sum(shannon_H(c) for c in comps) / n
    dec = []
    for i in range(0, n - 1, 2):
        gm = [math.sqrt(comps[i][j] * comps[i+1][j]) for j in range(D)]
        s = sum(gm)
        dec.append([g / s for g in gm])
    if not dec:
        return 100.0, False
    H_dec = sum(shannon_H(c) for c in dec) / len(dec)
    drift = abs(H_dec - H_full) / abs(H_full) * 100 if H_full != 0 else 0
    return round(drift, 4), drift < 1.0


def boundary_decomp(clr_vecs):
    """Per-channel CLR variance decomposition."""
    n = len(clr_vecs)
    D = len(clr_vecs[0])
    if n < 2:
        return {}, "?", 0
    var_ch = []
    tv = 0
    for j in range(D):
        col = [v[j] for v in clr_vecs]
        mu = sum(col) / n
        vj = sum((c - mu)**2 for c in col) / (n - 1)
        var_ch.append(vj)
        tv += vj
    fracs = {CHANNELS[j]: round(var_ch[j] / tv * 100, 2) if tv > 0 else 0
             for j in range(D)}
    bs = max(fracs, key=fracs.get)
    return fracs, bs, tv


def parabola_fit(x, y):
    n = len(x)
    if n < 3:
        return 0, 0, 0, 0
    Sx = sum(x); Sx2 = sum(xi**2 for xi in x)
    Sx3 = sum(xi**3 for xi in x); Sx4 = sum(xi**4 for xi in x)
    Sy = sum(y); Sxy = sum(a*b for a, b in zip(x, y))
    Sx2y = sum(a**2*b for a, b in zip(x, y))
    M = [[n,Sx,Sx2],[Sx,Sx2,Sx3],[Sx2,Sx3,Sx4]]
    v = [Sy, Sxy, Sx2y]
    def d3(m):
        return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
               -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
               +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    dd = d3(M)
    if abs(dd) < 1e-30:
        return 0, 0, 0, 0
    Ma = [[v[i] if j==0 else M[i][j] for j in range(3)] for i in range(3)]
    Mb = [[v[i] if j==1 else M[i][j] for j in range(3)] for i in range(3)]
    Mc = [[v[i] if j==2 else M[i][j] for j in range(3)] for i in range(3)]
    a = d3(Ma)/dd; b = d3(Mb)/dd; c = d3(Mc)/dd
    ym = Sy/n
    sst = sum((yi-ym)**2 for yi in y)
    ssr = sum((yi-(a+b*xi+c*xi**2))**2 for xi, yi in zip(x, y))
    R2 = 1 - ssr/sst if sst > 0 else 0
    return a, b, c, R2


def poly_fit(x, y, deg):
    """General polynomial fit. Returns (coeffs, R2)."""
    n = len(x)
    if n <= deg:
        return [0]*(deg+1), 0
    pw = {}
    for k in range(2*deg+1):
        pw[k] = sum(xi**k for xi in x)
    M = [[pw[i+j] for j in range(deg+1)] for i in range(deg+1)]
    v = [sum(xi**i*yi for xi, yi in zip(x, y)) for i in range(deg+1)]
    sz = deg + 1
    aug = [M[i][:] + [v[i]] for i in range(sz)]
    for col in range(sz):
        mr = col
        for row in range(col+1, sz):
            if abs(aug[row][col]) > abs(aug[mr][col]):
                mr = row
        aug[col], aug[mr] = aug[mr], aug[col]
        if abs(aug[col][col]) < 1e-30:
            continue
        for row in range(col+1, sz):
            f = aug[row][col] / aug[col][col]
            for k in range(col, sz+1):
                aug[row][k] -= f * aug[col][k]
    coeffs = [0.0]*sz
    for i in range(sz-1, -1, -1):
        if abs(aug[i][i]) < 1e-30:
            continue
        coeffs[i] = aug[i][sz]
        for j in range(i+1, sz):
            coeffs[i] -= aug[i][j]*coeffs[j]
        coeffs[i] /= aug[i][i]
    ym = sum(y)/n
    sst = sum((yi-ym)**2 for yi in y)
    ssr = sum((yi-sum(coeffs[k]*xi**k for k in range(sz)))**2
              for xi, yi in zip(x, y))
    R2 = 1-ssr/sst if sst > 0 else 0
    return coeffs, R2


def noise_squeeze(x, y):
    """Fit degrees 2-7, return squeeze ratio."""
    fits = []
    for d in range(2, 8):
        _, R2 = poly_fit(x, y, d)
        fits.append({"deg": d, "R2": round(R2, 6)})
    R2_2 = fits[0]["R2"]
    R2_6 = fits[4]["R2"] if len(fits) > 4 else fits[-1]["R2"]
    sq = (R2_6 - R2_2) / (1 - R2_2) if R2_2 < 1.0 else 0
    return fits, round(sq * 100, 2)


def vertex_theorem(clr_vecs, x_vals):
    """Find zero crossings of (2/D) sum clr_i * clr'_i."""
    D = len(clr_vecs[0])
    n = len(clr_vecs)
    ips = []
    for i in range(1, n-1):
        dx = x_vals[i+1] - x_vals[i-1]
        if abs(dx) < 1e-15:
            continue
        deriv = [(clr_vecs[i+1][j] - clr_vecs[i-1][j]) / dx for j in range(D)]
        ip = sum(clr_vecs[i][j] * deriv[j] for j in range(D)) * 2.0 / D
        ips.append({"x": x_vals[i], "ip": ip})
    crossings = []
    for i in range(len(ips)-1):
        if ips[i]["ip"] * ips[i+1]["ip"] < 0:
            frac = abs(ips[i]["ip"]) / (abs(ips[i]["ip"]) + abs(ips[i+1]["ip"]))
            xc = ips[i]["x"] + frac * (ips[i+1]["x"] - ips[i]["x"])
            crossings.append(round(xc, 2))
    min_ip = min(ips, key=lambda p: abs(p["ip"])) if ips else {"x": 0, "ip": 0}
    return crossings, min_ip


# ============================================================
#  FULL-KIT STEP ANALYSIS
# ============================================================

def full_kit_on_segment(comps, x_vals, label):
    """Run every HUF tool on a segment of compositions."""
    D = len(comps[0])
    n = len(comps)
    clr_vecs = [clr(c) for c in comps]

    # EITT
    drift, passed = eitt(comps)

    # Global sigma^2_A
    sig2 = aitchison_var(clr_vecs)

    # Boundary species
    fracs, bs, tv = boundary_decomp(clr_vecs)

    # PLL (sliding window)
    w = max(3, n // 5)
    sig_curve = []
    x_curve = []
    for i in range(w, n-w):
        sv = aitchison_var(clr_vecs[i-w:i+w+1])
        sig_curve.append(sv)
        x_curve.append(x_vals[i])

    R2, vtx, shape = 0, 0, "?"
    if len(x_curve) >= 5:
        a, b, c, R2 = parabola_fit(x_curve, sig_curve)
        if abs(c) > 1e-15:
            vtx = -b / (2*c)
        shape = "bowl" if c > 0 else "hill" if c < 0 else "flat"

    # Noise squeeze
    sq_fits, sq_pct = ([], 0)
    if len(x_curve) >= 8:
        sq_fits, sq_pct = noise_squeeze(x_curve, sig_curve)

    # Vertex theorem
    crossings, min_ip = vertex_theorem(clr_vecs, x_vals)

    return {
        "label": label,
        "n": n, "D": D,
        "x_range": [round(x_vals[0], 2), round(x_vals[-1], 2)],
        "EITT_drift": drift, "EITT_pass": passed,
        "sigma2_A": round(sig2, 6),
        "total_var": round(tv, 6),
        "boundary_species": bs,
        "boundary_short": CH_SHORT.get(bs, bs),
        "decomposition": fracs,
        "PLL_R2": round(R2, 4),
        "PLL_vertex": round(vtx, 2),
        "PLL_shape": shape,
        "squeeze_pct": sq_pct,
        "squeeze_fits": sq_fits,
        "VT_crossings": crossings,
        "VT_n_crossings": len(crossings),
        "VT_min_ip": {"x": round(min_ip["x"], 2), "ip": round(min_ip["ip"], 6)},
    }


# ============================================================
#  STARTUP PATH GENERATOR
# ============================================================

STEPS = [
    ("Cold startup",        1.0,  5.0,  0.3, 0.5),
    ("Ohmic plateau",       5.0,  8.0,  0.5, 0.7),
    ("Aux heating ramp",    8.0, 12.0,  0.7, 1.0),
    ("L-H transition",     12.0, 15.0,  1.0, 1.3),
    ("H-mode to ignition", 15.0, 20.0,  1.3, 1.8),
    ("Burning plasma",     20.0, 30.0,  1.8, 2.2),
    ("Thermonuclear burn", 30.0, 50.0,  2.2, 2.5),
]


def generate_path(path_type="diagonal", Zeff=1.5, B=5.3, pts_per_step=50):
    """Generate a startup trajectory with (T, n) at each point."""
    all_T = []
    all_n = []
    step_bounds = []  # (start_idx, end_idx, label)

    idx = 0
    for label, T0, T1, n0, n1 in STEPS:
        start = idx
        for i in range(pts_per_step):
            frac = i / (pts_per_step - 1)
            if path_type == "diagonal":
                T = T0 + frac * (T1 - T0)
                n = n0 + frac * (n1 - n0)
            elif path_type == "T_first":
                # Heat first, then compress
                if frac < 0.6:
                    T = T0 + (frac / 0.6) * (T1 - T0)
                    n = n0
                else:
                    T = T1
                    n = n0 + ((frac - 0.6) / 0.4) * (n1 - n0)
            elif path_type == "n_first":
                # Compress first, then heat
                if frac < 0.6:
                    T = T0
                    n = n0 + (frac / 0.6) * (n1 - n0)
                else:
                    T = T0 + ((frac - 0.6) / 0.4) * (T1 - T0)
                    n = n1
            all_T.append(round(T, 3))
            all_n.append(round(n, 4))
            idx += 1
        step_bounds.append((start, idx - 1, label))

    return all_T, all_n, step_bounds


def run_path(path_type, Zeff=1.5, B=5.3):
    """Run full-kit analysis on a startup path."""
    print(f"\n{'='*70}")
    print(f"  PATH: {path_type.upper()}  (Zeff={Zeff}, B={B}T)")
    print(f"{'='*70}")

    all_T, all_n, step_bounds = generate_path(path_type, Zeff, B)
    N = len(all_T)

    # Compute power balance and compositions for every point
    pbs = []
    comps = []
    for T, n in zip(all_T, all_n):
        pb = power_balance(T, n, B, Zeff)
        pbs.append(pb)
        comps.append(pb_to_comp(pb))

    # Track flips, ignition, Q along the path
    clr_all = [clr(c) for c in comps]
    w_flip = 7
    flip_log = []
    prev_bs = None
    ignition_idx = None
    Q_track = []

    for i in range(N):
        Q_track.append({"idx": i, "T": all_T[i], "n": all_n[i],
                        "Q": min(pbs[i]["Q"], 1e8),
                        "ignited": pbs[i]["ignited"],
                        "margin": pbs[i]["margin"]})

        if pbs[i]["ignited"] and ignition_idx is None:
            ignition_idx = i

        if i >= w_flip:
            _, bs_now, _ = boundary_decomp(clr_all[i-w_flip:i+1])
            if prev_bs and bs_now != prev_bs:
                flip_log.append({
                    "idx": i, "T": all_T[i], "n": all_n[i],
                    "from": CH_SHORT.get(prev_bs, prev_bs),
                    "to": CH_SHORT.get(bs_now, bs_now),
                    "ignited": pbs[i]["ignited"],
                })
            prev_bs = bs_now

    # ── Per-step full-kit analysis ──
    step_results = []
    for start, end, label in step_bounds:
        seg_comps = comps[start:end+1]
        seg_x = list(range(start, end+1))
        r = full_kit_on_segment(seg_comps, seg_x, label)

        # Add step-specific physics
        r["T_range"] = [all_T[start], all_T[end]]
        r["n_range"] = [all_n[start], all_n[end]]
        r["Q_start"] = round(min(pbs[start]["Q"], 1e8), 2)
        r["Q_end"] = round(min(pbs[end]["Q"], 1e8), 2)
        r["ignited_at_end"] = pbs[end]["ignited"]
        r["margin_end"] = round(pbs[end]["margin"], 2)

        # Power fractions at end of step
        pb_end = pbs[end]
        total_p = sum(max(pb_end[ch], 1e-30) for ch in CHANNELS)
        r["power_fracs_end"] = {CH_SHORT.get(ch, ch): round(pb_end[ch] / total_p * 100, 2)
                                for ch in CHANNELS}

        step_results.append(r)

        print(f"\n  STEP: {label}")
        print(f"    T: {r['T_range'][0]:.1f} -> {r['T_range'][1]:.1f} keV"
              f"   n: {r['n_range'][0]:.2f} -> {r['n_range'][1]:.2f} x10^20")
        print(f"    EITT: {r['EITT_drift']:.3f}% {'PASS' if r['EITT_pass'] else 'FAIL'}")
        print(f"    sigma^2_A = {r['sigma2_A']:.6f}")
        print(f"    PLL: R^2={r['PLL_R2']:.4f}  {r['PLL_shape']}  vertex={r['PLL_vertex']:.1f}")
        print(f"    Squeeze: {r['squeeze_pct']:.1f}%")
        print(f"    VT crossings: {r['VT_n_crossings']}  {r['VT_crossings']}")
        print(f"    Boundary species: {r['boundary_short']}")
        for ch, frac in sorted(r['decomposition'].items(),
                               key=lambda x: -x[1]):
            print(f"      {CH_SHORT.get(ch, ch):6s}: {frac:.1f}%")
        print(f"    Q: {r['Q_start']:.1f} -> {r['Q_end']:.1f}"
              f"   {'*** IGNITED ***' if r['ignited_at_end'] else 'sub-ignition'}")
        print(f"    Power at end: ", end="")
        print("  ".join(f"{k}={v:.1f}%" for k, v in
                        sorted(r['power_fracs_end'].items(), key=lambda x: -x[1])))

    # ── Full trajectory analysis ──
    print(f"\n{'='*70}")
    print(f"  FULL TRAJECTORY ANALYSIS: {path_type.upper()}")
    print(f"{'='*70}")

    full_r = full_kit_on_segment(comps, list(range(N)), f"Full {path_type}")

    print(f"  EITT: {full_r['EITT_drift']:.3f}% {'PASS' if full_r['EITT_pass'] else 'FAIL'}")
    print(f"  sigma^2_A = {full_r['sigma2_A']:.6f}")
    print(f"  PLL: R^2={full_r['PLL_R2']:.4f}  {full_r['PLL_shape']}  vertex={full_r['PLL_vertex']:.1f}")
    print(f"  Squeeze: {full_r['squeeze_pct']:.1f}%")
    print(f"  VT crossings: {full_r['VT_n_crossings']}")
    print(f"  Boundary species: {full_r['boundary_short']}")
    for ch, frac in sorted(full_r['decomposition'].items(), key=lambda x: -x[1]):
        print(f"    {CH_SHORT.get(ch, ch):6s}: {frac:.1f}%")

    print(f"\n  Flip log ({len(flip_log)} flips):")
    for f in flip_log:
        tag = " *** IGNITION ***" if f["ignited"] else ""
        print(f"    idx={f['idx']:3d}  T={f['T']:.1f}  n={f['n']:.2f}"
              f"  {f['from']:6s} -> {f['to']:6s}{tag}")

    if ignition_idx is not None:
        print(f"\n  IGNITION at step {ignition_idx}:"
              f" T={all_T[ignition_idx]:.1f} keV, n={all_n[ignition_idx]:.2f}")
    else:
        print(f"\n  NO IGNITION on this path")

    # ── Boundary species evolution map ──
    print(f"\n  Boundary species evolution (every 25 steps):")
    for i in range(0, N, 25):
        end_i = min(i + 25, N)
        seg = clr_all[i:end_i]
        if len(seg) < 3:
            continue
        _, bs_seg, _ = boundary_decomp(seg)
        pb_i = pbs[i]
        print(f"    [{i:3d}-{end_i:3d}] T={all_T[i]:5.1f} n={all_n[i]:.2f}"
              f"  BS={CH_SHORT.get(bs_seg, bs_seg):6s}"
              f"  Q={min(pb_i['Q'], 1e8):.1f}"
              f"  {'IGN' if pb_i['ignited'] else '   '}")

    return {
        "path_type": path_type,
        "Zeff": Zeff, "B": B,
        "N": N,
        "step_results": step_results,
        "full_trajectory": full_r,
        "flip_log": flip_log,
        "n_flips": len(flip_log),
        "ignition_idx": ignition_idx,
        "ignition_T": all_T[ignition_idx] if ignition_idx else None,
        "ignition_n": all_n[ignition_idx] if ignition_idx else None,
    }


# ============================================================
#  COMPARISON: ZEFF SENSITIVITY ACROSS PATHS
# ============================================================

def zeff_sensitivity():
    """Run diagonal path at multiple Zeff values."""
    print(f"\n{'='*70}")
    print(f"  ZEFF SENSITIVITY ANALYSIS")
    print(f"{'='*70}")

    results = []
    for Zeff in [1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0]:
        all_T, all_n, _ = generate_path("diagonal", Zeff, 5.3)
        ign = None
        for i, (T, n) in enumerate(zip(all_T, all_n)):
            pb = power_balance(T, n, 5.3, Zeff)
            if pb["ignited"] and ign is None:
                ign = i
                break

        comps = [pb_to_comp(power_balance(T, n, 5.3, Zeff))
                 for T, n in zip(all_T, all_n)]
        clr_vecs = [clr(c) for c in comps]
        sig2 = aitchison_var(clr_vecs)
        _, bs, _ = boundary_decomp(clr_vecs)

        ign_T = all_T[ign] if ign else None
        ign_n = all_n[ign] if ign else None

        results.append({
            "Zeff": Zeff,
            "ignition_idx": ign,
            "ignition_T": ign_T,
            "ignition_n": ign_n,
            "sigma2_A": round(sig2, 6),
            "boundary_species": CH_SHORT.get(bs, bs),
        })

        tag = f"T={ign_T:.1f} n={ign_n:.2f}" if ign else "NO IGNITION"
        print(f"  Zeff={Zeff:.1f}: {tag}  sigma^2_A={sig2:.4f}  BS={CH_SHORT.get(bs, bs)}")

    return results


# ============================================================
#  FABRICATED CONTROL
# ============================================================

def fabricated_control():
    """Dirichlet random compositions for EITT comparison."""
    print(f"\n{'='*70}")
    print(f"  FABRICATED CONTROL (Dirichlet)")
    print(f"{'='*70}")

    import random
    rng = random.Random(42)
    comps = []
    for _ in range(350):
        raw = [rng.gammavariate(1.0, 1.0) for _ in range(6)]
        s = sum(raw)
        comps.append([r / s for r in raw])

    r = full_kit_on_segment(comps, list(range(350)), "Dirichlet fabricated")

    print(f"  EITT: {r['EITT_drift']:.3f}% {'PASS' if r['EITT_pass'] else 'FAIL'}")
    print(f"  PLL: R^2={r['PLL_R2']:.4f}  {r['PLL_shape']}")
    print(f"  Squeeze: {r['squeeze_pct']:.1f}%")
    print(f"  VT crossings: {r['VT_n_crossings']}")
    print(f"  BS: {r['boundary_short']}")

    return r


# ============================================================
#  MAIN
# ============================================================

def main():
    print("=" * 70)
    print("  EXP-06C  CORRECTED FULL-KIT FUSION MAP")
    print("  Step-by-step path to ignition with all HUF tools")
    print("=" * 70)

    results = {}

    # Three paths
    for pt in ["diagonal", "T_first", "n_first"]:
        results[pt] = run_path(pt)

    # Zeff sensitivity
    results["zeff_sensitivity"] = zeff_sensitivity()

    # Fabricated control
    results["fabricated"] = fabricated_control()

    # ── GRAND COMPARISON ──
    print(f"\n{'='*70}")
    print(f"  GRAND COMPARISON")
    print(f"{'='*70}")
    print(f"  {'Path':<15s} {'Ign step':>8s} {'Ign T':>7s} {'Ign n':>7s}"
          f" {'Flips':>5s} {'PLL R2':>7s} {'Squeeze':>8s} {'EITT':>6s}")
    print(f"  {'-'*65}")
    for pt in ["diagonal", "T_first", "n_first"]:
        r = results[pt]
        fr = r["full_trajectory"]
        ign = r["ignition_idx"]
        it = f"{r['ignition_T']:.1f}" if r["ignition_T"] else "NONE"
        ine = f"{r['ignition_n']:.2f}" if r["ignition_n"] else ""
        print(f"  {pt:<15s} {str(ign):>8s} {it:>7s} {ine:>7s}"
              f" {r['n_flips']:>5d} {fr['PLL_R2']:>7.4f}"
              f" {fr['squeeze_pct']:>7.1f}% {fr['EITT_drift']:>5.3f}%")

    fab = results["fabricated"]
    print(f"  {'FABRICATED':<15s} {'N/A':>8s} {'N/A':>7s} {'N/A':>7s}"
          f" {'N/A':>5s} {fab['PLL_R2']:>7.4f}"
          f" {fab['squeeze_pct']:>7.1f}% {fab['EITT_drift']:>5.3f}%")

    # ── Step-by-step boundary species map for winning path ──
    winner = "diagonal"
    print(f"\n{'='*70}")
    print(f"  STEP-BY-STEP MAP: {winner.upper()} PATH")
    print(f"{'='*70}")
    for sr in results[winner]["step_results"]:
        print(f"\n  [{sr['label']}]")
        print(f"    T: {sr['T_range'][0]:.1f}-{sr['T_range'][1]:.1f} keV"
              f"  |  n: {sr['n_range'][0]:.2f}-{sr['n_range'][1]:.2f}"
              f"  |  Q: {sr['Q_start']:.1f}->{sr['Q_end']:.1f}"
              f"  |  {'IGNITED' if sr['ignited_at_end'] else 'sub-ign'}")
        print(f"    EITT={sr['EITT_drift']:.3f}%"
              f"  PLL R^2={sr['PLL_R2']:.4f} ({sr['PLL_shape']})"
              f"  Sq={sr['squeeze_pct']:.1f}%"
              f"  VT={sr['VT_n_crossings']} crossings")
        print(f"    BS={sr['boundary_short']}"
              f"  sigma^2_A={sr['sigma2_A']:.6f}")
        print(f"    Power: ", end="")
        print("  ".join(f"{k}={v:.1f}%" for k, v in
                        sorted(sr['power_fracs_end'].items(), key=lambda x: -x[1])))

    # ── Save ──
    output = {
        "experiment": "EXP-06C",
        "title": "Corrected Full-Kit Fusion Map",
        "date": datetime.now().isoformat(),
        "author": "Peter Higgins",
        "computed_by": "Claude (Anthropic)",
        "corrections_from": "EXP-06B Bremsstrahlung Boundary Attack",
        "channels": CHANNELS,
        "channel_labels": CH_SHORT,
        "steps": [s[2] for s in STEPS],
        "results": {},
    }

    for key, val in results.items():
        try:
            output["results"][key] = json.loads(json.dumps(val, default=str))
        except:
            output["results"][key] = str(val)

    outpath = os.path.join(os.path.dirname(__file__), "exp06c_fusion_map.json")
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {outpath}")

    return output


if __name__ == "__main__":
    main()
