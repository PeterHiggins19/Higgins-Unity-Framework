#!/usr/bin/env python3
"""
EXP-06  Nuclear Fusion — Full PLL-EITT Chain
=============================================
Series 2, Experiment 1

Compositional analysis of thermonuclear fusion reactivities.

Physical basis
--------------
The five primary fusion reactions each have a reactivity <σv>(T) that
depends on plasma ion temperature T.  At each temperature the five
reactivities form a composition — their *relative* magnitudes live on
the 4-simplex.  Sweeping T from 1 keV to 1000 keV traces a
compositional trajectory through the simplex.

Reactions
---------
  R1  D + T   → He-4 (3.5 MeV) + n (14.1 MeV)      — D-T
  R2  D + D   → He-3 (0.82 MeV) + n (2.45 MeV)      — D-D(n)
  R3  D + D   → T (1.01 MeV) + p (3.02 MeV)          — D-D(p)
  R4  D + He3 → He-4 (3.6 MeV) + p (14.7 MeV)        — D-He3
  R5  T + T   → He-4 + 2n (11.3 MeV)                  — T-T

Reactivity parameterisation: Bosch & Hale, Nuclear Fusion 32 (1992) 611.
The Bosch-Hale fit gives <σv> in cm³/s as a function of T in keV.

HUF toolkit applied
-------------------
  • EITT  — entropy invariance two-pass test (legitimacy)
  • PLL   — parabolic lock/anti-lock in σ²_A(T)
  • Noise squeeze — higher-order polynomial residual extraction
  • Vertex theorem — orthogonality at σ²_A extrema
  • Boundary species — per-reaction CLR variance decomposition

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

# ── FORMULAS & DEFINITIONS ────────────────────────────────────────────────
#
#   Simplex Closure (CoDa):
#     x_i = y_i / SUM(y_j)   for i = 1, ..., D
#     Constraint: SUM(x_i) = 1.  The data live on the (D-1)-simplex S^D.
#     This is the foundational CoDa operation — all subsequent analysis
#     occurs on the simplex, not in unconstrained Euclidean space.
#
#   Centred Log-Ratio Transform (CLR) — CoDa coordinate mapping:
#     clr(x)_i = ln(x_i) - (1/D) * SUM(ln(x_j))
#     Maps simplex compositions to unconstrained Euclidean space.
#     The geometric mean g(x) = exp((1/D) * SUM(ln(x_j))) is the reference.
#     Property: SUM(clr_i) = 0 (zero-sum constraint in CLR space).
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
#  Bosch-Hale reactivity parameterisation
# ─────────────────────────────────────────────────────────
# Reference: Bosch & Hale, Nucl. Fusion 32 (1992) 611-631
# <σv> = C1 * θ * sqrt( ξ / (mrc2 * T^3) ) * exp(-3*ξ)
# where θ = T / (1 - T*(C2 + T*(C4 + T*C6)) / (1 + T*(C3 + T*(C5 + T*C7))))
# and   ξ = (B_G^2 / (4*θ))^(1/3)
#
# Each reaction has its own set of coefficients.

# Coefficients: [B_G, mrc2, C1, C2, C3, C4, C5, C6, C7]
# B_G in keV^(1/2), mrc2 in keV, C1-C7 dimensionless or keV-based

BOSCH_HALE = {
    "D-T": {
        "B_G": 34.3827,
        "mrc2": 1124656.0,
        "C1": 1.17302e-9,
        "C2": 1.51361e-2,
        "C3": 7.51886e-2,
        "C4": 4.60643e-3,
        "C5": 1.35000e-2,
        "C6": -1.06750e-4,
        "C7": 1.36600e-5,
    },
    "D-D(n)": {
        # D(d,n)He3
        "B_G": 31.3970,
        "mrc2": 937814.0,
        "C1": 5.43360e-12,
        "C2": 5.85778e-3,
        "C3": 7.68222e-3,
        "C4": 0.0,
        "C5": -2.96400e-6,
        "C6": 0.0,
        "C7": 0.0,
    },
    "D-D(p)": {
        # D(d,p)T
        "B_G": 31.3970,
        "mrc2": 937814.0,
        "C1": 5.65718e-12,
        "C2": 3.41267e-3,
        "C3": 1.99167e-3,
        "C4": 0.0,
        "C5": 1.05060e-5,
        "C6": 0.0,
        "C7": 0.0,
    },
    "D-He3": {
        "B_G": 68.7508,
        "mrc2": 1124572.0,
        "C1": 5.51036e-10,
        "C2": 6.41918e-3,
        "C3": -2.02896e-3,
        "C4": -1.91080e-5,
        "C5": 1.35776e-4,
        "C6": 0.0,
        "C7": 0.0,
    },
    "T-T": {
        "B_G": 38.3950,
        "mrc2": 1124656.0,
        "C1": 1.28500e-10,
        "C2": 2.55200e-3,
        "C3": 5.84200e-3,
        "C4": 0.0,
        "C5": 0.0,
        "C6": 0.0,
        "C7": 0.0,
    },
}


def bosch_hale_reactivity(T_keV, params):
    """
    Compute <σv> in cm³/s for a given ion temperature T (keV).
    Bosch & Hale parameterisation (Nucl. Fusion 32, 1992, 611).
    """
    T = float(T_keV)
    if T < 0.2:
        return 1e-40  # below validity; return negligible

    BG = params["B_G"]
    mrc2 = params["mrc2"]
    C1 = params["C1"]
    C2 = params["C2"]
    C3 = params["C3"]
    C4 = params["C4"]
    C5 = params["C5"]
    C6 = params["C6"]
    C7 = params["C7"]

    # Compute θ
    numer = T * (C2 + T * (C4 + T * C6))
    denom = 1.0 + T * (C3 + T * (C5 + T * C7))
    ratio = numer / denom
    if abs(1.0 - ratio) < 1e-15:
        return 1e-40
    theta = T / (1.0 - ratio)

    if theta <= 0:
        return 1e-40  # outside parameterisation validity

    # Compute ξ
    xi = (BG ** 2 / (4.0 * theta)) ** (1.0 / 3.0)

    # Compute <σv>
    try:
        sv = C1 * theta * math.sqrt(xi / (mrc2 * T ** 3)) * math.exp(-3.0 * xi)
    except (OverflowError, ValueError):
        return 1e-40
    return max(sv, 1e-40)


# ─────────────────────────────────────────────────────────
#  Generate reactivity dataset across temperature range
# ─────────────────────────────────────────────────────────

def generate_reactivity_dataset():
    """
    Compute reactivities for all 5 reactions at temperatures from 1 to 1000 keV.
    Returns list of dicts with T and reactivity values.
    """
    reactions = ["D-T", "D-D(n)", "D-D(p)", "D-He3", "T-T"]

    # Temperature grid: logarithmic spacing for better coverage
    # 1 to 1000 keV, 200 points
    temps = []
    for i in range(200):
        T = 1.0 * math.exp(i * math.log(1000.0) / 199.0)
        temps.append(round(T, 4))

    dataset = []
    for T in temps:
        row = {"T_keV": T}
        for rxn in reactions:
            sv = bosch_hale_reactivity(T, BOSCH_HALE[rxn])
            row[rxn] = sv
        dataset.append(row)

    return dataset, reactions


def reactivity_to_composition(dataset, reactions):
    """
    Convert absolute reactivities to compositional fractions.
    At each temperature, the 5 reactivities are normalised to sum to 1.
    """
    compositions = []
    for row in dataset:
        total = sum(row[rxn] for rxn in reactions)
        if total < 1e-80:
            comp = {rxn: 1.0/len(reactions) for rxn in reactions}
        else:
            comp = {rxn: row[rxn] / total for rxn in reactions}
        comp["T_keV"] = row["T_keV"]
        compositions.append(comp)
    return compositions


# ─────────────────────────────────────────────────────────
#  CoDa tools  (from HUF toolkit)
# ─────────────────────────────────────────────────────────

def close_composition(x, kappa=1.0):
    """Closure operator: rescale to sum to kappa."""
    s = sum(x)
    if s == 0:
        return [kappa / len(x)] * len(x)
    return [xi * kappa / s for xi in x]


def clr_transform(x):
    """Centred log-ratio transform."""
    n = len(x)
    # Replace zeros with small value
    x_safe = [max(xi, 1e-20) for xi in x]
    log_x = [math.log(xi) for xi in x_safe]
    mean_log = sum(log_x) / n
    return [lx - mean_log for lx in log_x]


def aitchison_variance(clr_vectors):
    """
    Aitchison variance σ²_A = (1/D) Σ_j var(clr_j) across samples.
    Input: list of CLR vectors (each a list of D values).
    """
    if not clr_vectors:
        return 0.0
    n = len(clr_vectors)
    D = len(clr_vectors[0])
    if n < 2:
        return 0.0

    var_sum = 0.0
    for j in range(D):
        col = [v[j] for v in clr_vectors]
        mean_j = sum(col) / n
        var_j = sum((c - mean_j) ** 2 for c in col) / (n - 1)
        var_sum += var_j
    return var_sum / D


def aitchison_total_variance(clr_vectors):
    """Total variance = D * σ²_A = Σ_j var(clr_j)."""
    if not clr_vectors:
        return 0.0
    n = len(clr_vectors)
    D = len(clr_vectors[0])
    if n < 2:
        return 0.0

    var_sum = 0.0
    for j in range(D):
        col = [v[j] for v in clr_vectors]
        mean_j = sum(col) / n
        var_j = sum((c - mean_j) ** 2 for c in col) / (n - 1)
        var_sum += var_j
    return var_sum


def shannon_entropy(x):
    """Shannon entropy H = -Σ p_i log(p_i), base e."""
    x_closed = close_composition(x)
    H = 0.0
    for p in x_closed:
        if p > 0:
            H -= p * math.log(p)
    return H


# ─────────────────────────────────────────────────────────
#  EITT — Entropy Invariance Two-pass Test
# ─────────────────────────────────────────────────────────

def eitt_test(compositions, label=""):
    """
    EITT: geometric-mean block decimation.
    Legitimate data: entropy drift < 1%.
    """
    n = len(compositions)
    D = len(compositions[0])

    # Full entropy
    H_full = sum(shannon_entropy(c) for c in compositions) / n

    # Decimated: geometric mean of consecutive pairs
    decimated = []
    for i in range(0, n - 1, 2):
        gm = []
        for j in range(D):
            gm.append(math.sqrt(compositions[i][j] * compositions[i + 1][j]))
        decimated.append(close_composition(gm))

    if not decimated:
        return {"label": label, "pass": False, "drift_pct": 100.0}

    H_dec = sum(shannon_entropy(c) for c in decimated) / len(decimated)

    if H_full == 0:
        drift = 0.0
    else:
        drift = abs(H_dec - H_full) / abs(H_full) * 100.0

    return {
        "label": label,
        "H_full": round(H_full, 6),
        "H_decimated": round(H_dec, 6),
        "drift_pct": round(drift, 4),
        "pass": drift < 1.0,
        "verdict": "LEGITIMATE" if drift < 1.0 else "SUSPECT",
    }


# ─────────────────────────────────────────────────────────
#  PLL parabola + Noise Squeeze + Vertex Theorem
# ─────────────────────────────────────────────────────────

def parabola_fit_lstsq(x, y):
    """Least-squares parabola y = a + bx + cx²."""
    n = len(x)
    if n < 3:
        return 0, 0, 0, 0.0

    Sx = sum(x)
    Sx2 = sum(xi**2 for xi in x)
    Sx3 = sum(xi**3 for xi in x)
    Sx4 = sum(xi**4 for xi in x)
    Sy = sum(y)
    Sxy = sum(xi * yi for xi, yi in zip(x, y))
    Sx2y = sum(xi**2 * yi for xi, yi in zip(x, y))

    # Normal equations: M [a, b, c]^T = v
    M = [
        [n, Sx, Sx2],
        [Sx, Sx2, Sx3],
        [Sx2, Sx3, Sx4],
    ]
    v = [Sy, Sxy, Sx2y]

    # Solve with Cramer's rule
    def det3(m):
        return (
            m[0][0] * (m[1][1]*m[2][2] - m[1][2]*m[2][1])
          - m[0][1] * (m[1][0]*m[2][2] - m[1][2]*m[2][0])
          + m[0][2] * (m[1][0]*m[2][1] - m[1][1]*m[2][0])
        )

    D_det = det3(M)
    if abs(D_det) < 1e-30:
        return 0, 0, 0, 0.0

    Ma = [[v[i] if j == 0 else M[i][j] for j in range(3)] for i in range(3)]
    Mb = [[v[i] if j == 1 else M[i][j] for j in range(3)] for i in range(3)]
    Mc = [[v[i] if j == 2 else M[i][j] for j in range(3)] for i in range(3)]

    a = det3(Ma) / D_det
    b = det3(Mb) / D_det
    c = det3(Mc) / D_det

    # R²
    y_mean = Sy / n
    ss_tot = sum((yi - y_mean)**2 for yi in y)
    ss_res = sum((yi - (a + b*xi + c*xi**2))**2 for xi, yi in zip(x, y))
    R2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    return a, b, c, R2


def poly_fit_lstsq(x, y, degree):
    """General least-squares polynomial fit. Returns coefficients and R²."""
    n = len(x)
    if n <= degree:
        return [0] * (degree + 1), 0.0

    # Build Vandermonde-like normal equations
    # Sum x^(i+j) for i,j in 0..degree
    powers = {}
    for k in range(2 * degree + 1):
        powers[k] = sum(xi**k for xi in x)

    # Build matrix and vector
    M = [[powers[i + j] for j in range(degree + 1)] for i in range(degree + 1)]
    v = [sum(xi**i * yi for xi, yi in zip(x, y)) for i in range(degree + 1)]

    # Gaussian elimination
    sz = degree + 1
    aug = [M[i][:] + [v[i]] for i in range(sz)]

    for col in range(sz):
        # Pivot
        max_row = col
        for row in range(col + 1, sz):
            if abs(aug[row][col]) > abs(aug[max_row][col]):
                max_row = row
        aug[col], aug[max_row] = aug[max_row], aug[col]

        if abs(aug[col][col]) < 1e-30:
            continue

        for row in range(col + 1, sz):
            factor = aug[row][col] / aug[col][col]
            for k in range(col, sz + 1):
                aug[row][k] -= factor * aug[col][k]

    # Back substitution
    coeffs = [0.0] * sz
    for i in range(sz - 1, -1, -1):
        if abs(aug[i][i]) < 1e-30:
            continue
        coeffs[i] = aug[i][sz]
        for j in range(i + 1, sz):
            coeffs[i] -= aug[i][j] * coeffs[j]
        coeffs[i] /= aug[i][i]

    # R²
    y_mean = sum(y) / n
    ss_tot = sum((yi - y_mean)**2 for yi in y)
    ss_res = 0.0
    for xi, yi in zip(x, y):
        pred = sum(coeffs[k] * xi**k for k in range(sz))
        ss_res += (yi - pred)**2
    R2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    return coeffs, R2


def pll_analysis(temperatures, compositions, reactions, label=""):
    """
    PLL: compute σ²_A in sliding windows along the temperature trajectory.
    Then fit parabola to σ²_A(T).
    """
    D = len(reactions)
    n = len(compositions)

    # Compute CLR vectors
    clr_vecs = []
    for comp in compositions:
        vals = [comp[rxn] for rxn in reactions]
        clr_vecs.append(clr_transform(vals))

    # Global σ²_A
    global_var = aitchison_variance(clr_vecs)

    # Sliding window σ²_A — window size ~15% of data
    w = max(5, n // 7)
    half_w = w // 2
    sigma_a_curve = []
    t_curve = []

    for i in range(half_w, n - half_w):
        window = clr_vecs[max(0, i - half_w):min(n, i + half_w + 1)]
        if len(window) >= 3:
            sv = aitchison_variance(window)
            sigma_a_curve.append(sv)
            t_curve.append(temperatures[i])

    if len(t_curve) < 5:
        return {
            "label": label,
            "global_sigma2_A": round(global_var, 6),
            "parabola_R2": 0.0,
            "status": "INSUFFICIENT_DATA"
        }

    # Use log(T) as the ordinate — temperature spans 3 decades
    log_t = [math.log10(t) for t in t_curve]

    # Fit parabola
    a, b, c, R2 = parabola_fit_lstsq(log_t, sigma_a_curve)

    # Vertex location
    if abs(c) > 1e-15:
        vertex_log_t = -b / (2 * c)
        vertex_T = 10 ** vertex_log_t
    else:
        vertex_log_t = 0
        vertex_T = 0

    # Shape
    shape = "bowl (lock)" if c > 0 else "hill (anti-lock)" if c < 0 else "flat"

    # Is vertex within data range?
    vertex_in_range = min(log_t) <= vertex_log_t <= max(log_t) if c != 0 else False

    return {
        "label": label,
        "global_sigma2_A": round(global_var, 6),
        "total_variance": round(global_var * D, 6),
        "parabola_a": round(a, 8),
        "parabola_b": round(b, 8),
        "parabola_c": round(c, 8),
        "parabola_R2": round(R2, 4),
        "vertex_log10_T": round(vertex_log_t, 4),
        "vertex_T_keV": round(vertex_T, 2),
        "shape": shape,
        "vertex_in_range": vertex_in_range,
        "window_size": w,
        "n_windows": len(t_curve),
        "sigma_a_curve": [(round(t, 2), round(s, 6)) for t, s in zip(t_curve, sigma_a_curve)],
    }


def noise_squeeze(temperatures, compositions, reactions, label=""):
    """
    Noise squeeze: fit polynomials of increasing degree to σ²_A(T).
    Measure how much residual variance is extracted at each order.
    """
    D = len(reactions)
    n = len(compositions)

    clr_vecs = [clr_transform([comp[rxn] for rxn in reactions]) for comp in compositions]

    w = max(5, n // 7)
    half_w = w // 2
    sigma_curve = []
    log_t_curve = []

    for i in range(half_w, n - half_w):
        window = clr_vecs[max(0, i - half_w):min(n, i + half_w + 1)]
        if len(window) >= 3:
            sigma_curve.append(aitchison_variance(window))
            log_t_curve.append(math.log10(temperatures[i]))

    if len(log_t_curve) < 6:
        return {"label": label, "status": "INSUFFICIENT_DATA"}

    results = []
    for deg in range(2, 8):
        coeffs, R2 = poly_fit_lstsq(log_t_curve, sigma_curve, deg)
        results.append({"degree": deg, "R2": round(R2, 6)})

    # Squeeze = (R2_deg6 - R2_deg2) / (1 - R2_deg2)
    R2_2 = results[0]["R2"]
    R2_6 = results[4]["R2"] if len(results) > 4 else results[-1]["R2"]
    squeeze = (R2_6 - R2_2) / (1 - R2_2) if R2_2 < 1.0 else 0.0

    return {
        "label": label,
        "polynomial_fits": results,
        "squeeze_ratio": round(squeeze, 4),
        "squeeze_pct": round(squeeze * 100, 2),
    }


def vertex_theorem_check(temperatures, compositions, reactions, label=""):
    """
    Vertex Theorem T1: d(σ²_A)/dt = (2/D) Σ clr_i · clr'_i
    At extrema, clr(t*) ⊥ clr'(t*).

    We check this numerically by computing the inner product at the
    estimated vertex and verifying it approaches zero.
    """
    D = len(reactions)
    n = len(compositions)

    clr_vecs = [clr_transform([comp[rxn] for rxn in reactions]) for comp in compositions]

    # Numerical derivatives: clr'_i ≈ (clr_{i+1} - clr_{i-1}) / 2
    inner_products = []
    log_temps = [math.log10(t) for t in temperatures]

    for i in range(1, n - 1):
        dt = log_temps[i + 1] - log_temps[i - 1]
        if abs(dt) < 1e-15:
            continue
        clr_deriv = [(clr_vecs[i + 1][j] - clr_vecs[i - 1][j]) / dt for j in range(D)]
        ip = sum(clr_vecs[i][j] * clr_deriv[j] for j in range(D))
        inner_products.append({
            "T_keV": round(temperatures[i], 2),
            "log10_T": round(log_temps[i], 4),
            "inner_product": round(ip, 6),
            "abs_ip": round(abs(ip), 6),
        })

    if not inner_products:
        return {"label": label, "status": "INSUFFICIENT_DATA"}

    # Find where inner product crosses zero (sign changes)
    zero_crossings = []
    for i in range(len(inner_products) - 1):
        ip1 = inner_products[i]["inner_product"]
        ip2 = inner_products[i + 1]["inner_product"]
        if ip1 * ip2 < 0:  # sign change
            # Linear interpolation for zero crossing
            frac = abs(ip1) / (abs(ip1) + abs(ip2))
            T_cross = inner_products[i]["T_keV"] + frac * (
                inner_products[i + 1]["T_keV"] - inner_products[i]["T_keV"]
            )
            log_T_cross = inner_products[i]["log10_T"] + frac * (
                inner_products[i + 1]["log10_T"] - inner_products[i]["log10_T"]
            )
            zero_crossings.append({
                "T_keV": round(T_cross, 2),
                "log10_T": round(log_T_cross, 4),
                "residual_ip": round(abs(ip1) * (1 - frac) + abs(ip2) * frac, 6),
            })

    # Also find the absolute minimum of |inner_product|
    min_ip = min(inner_products, key=lambda x: x["abs_ip"])

    return {
        "label": label,
        "n_points": len(inner_products),
        "zero_crossings": zero_crossings,
        "n_crossings": len(zero_crossings),
        "min_abs_inner_product": min_ip,
        "orthogonality_confirmed": len(zero_crossings) > 0,
    }


def boundary_species_analysis(compositions, reactions, label=""):
    """
    Per-reaction CLR variance decomposition.
    Identifies which reaction channel dominates compositional variability.
    """
    D = len(reactions)
    clr_vecs = [clr_transform([comp[rxn] for rxn in reactions]) for comp in compositions]
    n = len(clr_vecs)

    if n < 2:
        return {"label": label, "status": "INSUFFICIENT_DATA"}

    var_by_reaction = {}
    total_var = 0.0

    for j, rxn in enumerate(reactions):
        col = [v[j] for v in clr_vecs]
        mean_j = sum(col) / n
        var_j = sum((c - mean_j) ** 2 for c in col) / (n - 1)
        var_by_reaction[rxn] = var_j
        total_var += var_j

    # Fractions
    results = []
    for rxn in reactions:
        frac = var_by_reaction[rxn] / total_var if total_var > 0 else 0
        results.append({
            "reaction": rxn,
            "clr_variance": round(var_by_reaction[rxn], 6),
            "fraction_of_total": round(frac, 4),
            "fraction_pct": round(frac * 100, 2),
        })

    results.sort(key=lambda x: x["clr_variance"], reverse=True)
    boundary = results[0]["reaction"]

    return {
        "label": label,
        "boundary_species": boundary,
        "boundary_fraction_pct": results[0]["fraction_pct"],
        "decomposition": results,
        "total_clr_variance": round(total_var, 6),
    }


# ─────────────────────────────────────────────────────────
#  Energy partition analysis
# ─────────────────────────────────────────────────────────

def generate_energy_partition_dataset():
    """
    Supplementary compositional dataset: energy partition in a tokamak
    as a function of plasma temperature.

    At each temperature, the fusion power output is distributed among:
      - Neutron kinetic energy (escapes plasma)
      - Alpha particle heating (heats plasma)
      - Bremsstrahlung radiation losses
      - Cyclotron radiation losses
      - Conduction/convection losses

    These are simplified physics-based models to create a realistic
    compositional trajectory.
    """
    temps = []
    for i in range(100):
        T = 1.0 + i * 0.99  # 1 to 100 keV
        temps.append(round(T, 2))

    components = ["Neutron_KE", "Alpha_heating", "Bremsstrahlung", "Cyclotron", "Conduction"]
    dataset = []

    for T in temps:
        # D-T reactivity drives neutron and alpha production
        sv_dt = bosch_hale_reactivity(T, BOSCH_HALE["D-T"])

        # Neutron carries 14.1/17.6 = 80.1% of fusion energy
        neutron_frac = 0.801
        alpha_frac = 0.199

        # Scale by reactivity (normalised)
        sv_ref = bosch_hale_reactivity(15.0, BOSCH_HALE["D-T"])
        fusion_power = sv_dt / (sv_ref if sv_ref > 1e-40 else 1e-40)

        # Bremsstrahlung: ∝ n²√T ∝ T^0.5 (simplified)
        brem = 0.02 * T ** 0.5

        # Cyclotron: ∝ nT B² ∝ T (simplified, strong B)
        cycl = 0.001 * T

        # Conduction: ∝ T^(5/2) / (n τ_E) — simplified
        cond = 0.005 * T ** 1.5

        # Raw values
        raw = [
            max(fusion_power * neutron_frac, 1e-10),
            max(fusion_power * alpha_frac, 1e-10),
            max(brem, 1e-10),
            max(cycl, 1e-10),
            max(cond, 1e-10),
        ]
        total = sum(raw)
        comp = {c: r / total for c, r in zip(components, raw)}
        comp["T_keV"] = T
        dataset.append(comp)

    return dataset, components, temps


# ─────────────────────────────────────────────────────────
#  Dirichlet control (fabricated data for EITT comparison)
# ─────────────────────────────────────────────────────────

def generate_dirichlet_control(n, D, seed=42):
    """Generate Dirichlet-random compositions (no physical structure)."""
    import random
    rng = random.Random(seed)
    comps = []
    for _ in range(n):
        # Gamma(1,1) → Dirichlet uniform
        raw = [rng.gammavariate(1.0, 1.0) for _ in range(D)]
        total = sum(raw)
        comps.append([r / total for r in raw])
    return comps


# ─────────────────────────────────────────────────────────
#  Run full chain
# ─────────────────────────────────────────────────────────

def run_chain(temperatures, compositions, reactions, label):
    """Execute complete PLL-EITT chain on a dataset."""
    # Extract composition arrays
    comp_arrays = [[comp[rxn] for rxn in reactions] for comp in compositions]

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  n={len(compositions)}, D={len(reactions)}")
    print(f"  T range: {temperatures[0]:.1f} – {temperatures[-1]:.1f} keV")
    print(f"{'='*60}")

    # 1. EITT
    eitt = eitt_test(comp_arrays, label)
    print(f"  EITT: H_full={eitt['H_full']:.4f}, H_dec={eitt['H_decimated']:.4f}, "
          f"drift={eitt['drift_pct']:.3f}% → {eitt['verdict']}")

    # 2. PLL
    pll = pll_analysis(temperatures, compositions, reactions, label)
    print(f"  PLL:  R²={pll.get('parabola_R2', 0):.4f}, shape={pll.get('shape','?')}, "
          f"vertex={pll.get('vertex_T_keV', 0):.1f} keV")
    print(f"        σ²_A={pll.get('global_sigma2_A', 0):.6f}")

    # 3. Noise squeeze
    ns = noise_squeeze(temperatures, compositions, reactions, label)
    print(f"  Squeeze: {ns.get('squeeze_pct', 0):.1f}%")
    if "polynomial_fits" in ns:
        for pf in ns["polynomial_fits"]:
            print(f"    deg {pf['degree']}: R²={pf['R2']:.6f}")

    # 4. Vertex theorem
    vt = vertex_theorem_check(temperatures, compositions, reactions, label)
    print(f"  Vertex Theorem: {vt.get('n_crossings', 0)} zero-crossing(s)")
    if vt.get("zero_crossings"):
        for zc in vt["zero_crossings"]:
            print(f"    T={zc['T_keV']:.1f} keV (log₁₀T={zc['log10_T']:.3f})")

    # 5. Boundary species
    bs = boundary_species_analysis(compositions, reactions, label)
    print(f"  Boundary species: {bs.get('boundary_species','?')} "
          f"({bs.get('boundary_fraction_pct', 0):.1f}%)")
    for item in bs.get("decomposition", []):
        print(f"    {item['reaction']:8s}: {item['fraction_pct']:5.1f}%")

    return {
        "label": label,
        "n_samples": len(compositions),
        "D": len(reactions),
        "T_range_keV": [temperatures[0], temperatures[-1]],
        "eitt": eitt,
        "pll": pll,
        "noise_squeeze": ns,
        "vertex_theorem": vt,
        "boundary_species": bs,
    }


def main():
    print("=" * 60)
    print("  EXP-06  NUCLEAR FUSION — PLL-EITT CHAIN")
    print("  Series 2, Experiment 1")
    print("  Bosch-Hale reactivity parameterisation")
    print("=" * 60)

    # ── Generate primary dataset ──
    dataset, reactions = generate_reactivity_dataset()
    compositions = reactivity_to_composition(dataset, reactions)
    temperatures = [row["T_keV"] for row in dataset]

    print(f"\nDataset: {len(dataset)} temperature points, {len(reactions)} reactions")
    print(f"Temperature range: {temperatures[0]:.1f} – {temperatures[-1]:.1f} keV")
    print(f"Reactions: {', '.join(reactions)}")

    # Print a few sample compositions
    print("\nSample compositions (selected temperatures):")
    for idx in [0, 25, 50, 75, 100, 125, 150, 175, 199]:
        if idx < len(compositions):
            T = temperatures[idx]
            comp = compositions[idx]
            parts = " | ".join(f"{rxn}: {comp[rxn]:.4f}" for rxn in reactions)
            print(f"  T={T:7.1f} keV → {parts}")

    all_results = {}

    # ── Suite 1: Full temperature range ──
    r = run_chain(temperatures, compositions, reactions, "Full range (1-1000 keV)")
    all_results["full_range"] = r

    # ── Suite 2: ITER-relevant range (5-30 keV) ──
    iter_idx = [i for i, T in enumerate(temperatures) if 5 <= T <= 30]
    if len(iter_idx) > 5:
        r = run_chain(
            [temperatures[i] for i in iter_idx],
            [compositions[i] for i in iter_idx],
            reactions,
            "ITER range (5-30 keV)"
        )
        all_results["iter_range"] = r

    # ── Suite 3: Low temperature (1-10 keV) ──
    low_idx = [i for i, T in enumerate(temperatures) if T <= 10]
    if len(low_idx) > 5:
        r = run_chain(
            [temperatures[i] for i in low_idx],
            [compositions[i] for i in low_idx],
            reactions,
            "Low temperature (1-10 keV)"
        )
        all_results["low_temp"] = r

    # ── Suite 4: High temperature (100-1000 keV) ──
    high_idx = [i for i, T in enumerate(temperatures) if T >= 100]
    if len(high_idx) > 5:
        r = run_chain(
            [temperatures[i] for i in high_idx],
            [compositions[i] for i in high_idx],
            reactions,
            "High temperature (100-1000 keV)"
        )
        all_results["high_temp"] = r

    # ── Suite 5: D-T ignition window (8-25 keV) ──
    ignition_idx = [i for i, T in enumerate(temperatures) if 8 <= T <= 25]
    if len(ignition_idx) > 5:
        r = run_chain(
            [temperatures[i] for i in ignition_idx],
            [compositions[i] for i in ignition_idx],
            reactions,
            "Ignition window (8-25 keV)"
        )
        all_results["ignition_window"] = r

    # ── Suite 6: Energy partition (tokamak) ──
    energy_data, energy_comps_names, energy_temps = generate_energy_partition_dataset()
    r = run_chain(
        energy_temps,
        energy_data,
        energy_comps_names,
        "Energy partition (tokamak model)"
    )
    all_results["energy_partition"] = r

    # ── Suite 7: Aneutronic subset (D-He3 + D-D only) ──
    # Recompute compositions with only D-D(n), D-D(p), D-He3
    aneutronic_rxns = ["D-D(n)", "D-D(p)", "D-He3"]
    aneutronic_comps = []
    for row in dataset:
        total = sum(row[rxn] for rxn in aneutronic_rxns)
        if total < 1e-80:
            comp = {rxn: 1.0/3 for rxn in aneutronic_rxns}
        else:
            comp = {rxn: row[rxn] / total for rxn in aneutronic_rxns}
        comp["T_keV"] = row["T_keV"]
        aneutronic_comps.append(comp)

    r = run_chain(temperatures, aneutronic_comps, aneutronic_rxns,
                  "Aneutronic subset (D-D + D-He3)")
    all_results["aneutronic"] = r

    # ── Suite 8: Reversed trajectory (control) ──
    r = run_chain(
        list(reversed(temperatures)),
        list(reversed(compositions)),
        reactions,
        "Reversed (1000→1 keV) — control"
    )
    all_results["reversed_control"] = r

    # ── Suite 9: Dirichlet random (control) ──
    dirichlet = generate_dirichlet_control(200, 5, seed=42)
    fake_reactions = reactions
    fake_temps = list(range(1, 201))
    fake_comps = [{rxn: d[j] for j, rxn in enumerate(fake_reactions)} for d in dirichlet]
    for i, fc in enumerate(fake_comps):
        fc["T_keV"] = fake_temps[i]

    r = run_chain(fake_temps, fake_comps, fake_reactions,
                  "Dirichlet random — FABRICATED control")
    all_results["dirichlet_control"] = r

    # ── Suite 10: D-T dominance onset analysis ──
    # Find where D-T first exceeds 50%, 90%, 99% of total reactivity
    dt_milestones = {}
    for comp, T in zip(compositions, temperatures):
        frac_dt = comp["D-T"]
        if frac_dt >= 0.50 and "50pct" not in dt_milestones:
            dt_milestones["50pct"] = T
        if frac_dt >= 0.90 and "90pct" not in dt_milestones:
            dt_milestones["90pct"] = T
        if frac_dt >= 0.99 and "99pct" not in dt_milestones:
            dt_milestones["99pct"] = T

    print(f"\n{'='*60}")
    print("  D-T DOMINANCE MILESTONES")
    print(f"{'='*60}")
    for k, v in sorted(dt_milestones.items()):
        print(f"  D-T ≥ {k}: T = {v:.1f} keV")
    all_results["dt_dominance"] = dt_milestones

    # ── Suite 11: Cross-reaction texture matrix ──
    # Compare σ²_A across different sub-selections of reactions
    print(f"\n{'='*60}")
    print("  CROSS-REACTION TEXTURE MATRIX")
    print(f"{'='*60}")

    texture = {}
    subsets = {
        "All 5 reactions": reactions,
        "D-T + D-D only": ["D-T", "D-D(n)", "D-D(p)"],
        "D-T + D-He3": ["D-T", "D-He3"],
        "D-D branches only": ["D-D(n)", "D-D(p)"],
        "Non-DT": ["D-D(n)", "D-D(p)", "D-He3", "T-T"],
    }

    for name, rxn_subset in subsets.items():
        sub_comps = []
        for row in dataset:
            total = sum(row[rxn] for rxn in rxn_subset)
            if total < 1e-80:
                comp = {rxn: 1.0/len(rxn_subset) for rxn in rxn_subset}
            else:
                comp = {rxn: row[rxn] / total for rxn in rxn_subset}
            sub_comps.append(comp)

        clr_vecs = [clr_transform([c[rxn] for rxn in rxn_subset]) for c in sub_comps]
        sva = aitchison_variance(clr_vecs)
        texture[name] = round(sva, 6)
        print(f"  {name:25s}: σ²_A = {sva:.6f}")

    all_results["texture_matrix"] = texture

    # ── Summary ──
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")

    for key in ["full_range", "iter_range", "low_temp", "high_temp",
                "ignition_window", "energy_partition", "aneutronic",
                "reversed_control", "dirichlet_control"]:
        if key in all_results:
            r = all_results[key]
            eitt_v = r["eitt"]["verdict"]
            pll_r2 = r["pll"].get("parabola_R2", 0)
            shape = r["pll"].get("shape", "?")
            vtx = r["pll"].get("vertex_T_keV", 0)
            bs = r["boundary_species"].get("boundary_species", "?")
            sq = r["noise_squeeze"].get("squeeze_pct", 0)
            print(f"  {r['label']:40s} EITT:{eitt_v:10s} PLL R²={pll_r2:.4f} "
                  f"{shape:16s} vertex={vtx:7.1f} keV  BS={bs:8s}  SQ={sq:.1f}%")

    # ── Save results ──
    output = {
        "experiment": "EXP-06",
        "title": "Nuclear Fusion Reactivity Compositional Analysis",
        "series": 2,
        "date": datetime.now().isoformat(),
        "author": "Peter Higgins",
        "computed_by": "Claude (Anthropic)",
        "parameterisation": "Bosch & Hale, Nucl. Fusion 32 (1992) 611",
        "reactions": reactions,
        "n_temperatures": len(temperatures),
        "T_range_keV": [temperatures[0], temperatures[-1]],
        "results": {},
    }

    # Serialise — strip the large sigma_a_curve for JSON size
    for key, val in all_results.items():
        if isinstance(val, dict) and "pll" in val:
            val_copy = json.loads(json.dumps(val, default=str))
            # Keep sigma curve but truncate if huge
            if "pll" in val_copy and "sigma_a_curve" in val_copy["pll"]:
                curve = val_copy["pll"]["sigma_a_curve"]
                if len(curve) > 50:
                    # Sample every nth
                    step = len(curve) // 50
                    val_copy["pll"]["sigma_a_curve_sampled"] = curve[::step]
                    del val_copy["pll"]["sigma_a_curve"]
            output["results"][key] = val_copy
        else:
            output["results"][key] = val

    outpath = os.path.join(os.path.dirname(__file__), "exp06_fusion_chain.json")
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {outpath}")

    return output


if __name__ == "__main__":
    main()
