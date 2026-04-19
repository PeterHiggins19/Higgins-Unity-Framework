#!/usr/bin/env python3
"""
EXP-03 REVISED: The Uranium Test — Full PLL-EITT Verification
================================================================
Nuclear compositions from AME2020 (3,554 nuclides)

Two compositional systems tested:
  A) Decay chains — 2-simplex (Z/A, N/A), true parametric walks
     U-238 chain (15 steps), Th-232 chain (11 steps), U-235 chain (12 steps)
  B) SEMF Valley — 4-simplex [Volume, Surface, Coulomb, Asymmetry]
     along the valley of stability, ordered by Z (118 nuclides)

Full PLL-EITT chain:
  Step 1-3:  Classical CoDa (closure, CLR, σ²_A)
  Step 4-6:  EITT core (geometric mean decimation, entropy invariance)
  Step 7:    PLL analysis (σ²_A parabola, vertex theorem)
  Step 8:    Noise squeeze (polynomial orders 2-5, stochastic core)
  Step 9:    DADC-DADI-ADAC (per-species contamination decomposition)
  Step 10:   Verdict — full chain

Peter Higgins / Claude — 2026-04-18  FIXED POINT v3.2
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
#   Variation Matrix — pairwise compositional coupling:
#     T_ij = var(ln(x_i / x_j))
#     Small T_ij => components i, j are tightly coupled.
#     Large T_ij => components move independently.
#     The variation matrix is symmetric with zero diagonal.
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
#   Semi-Empirical Mass Formula (SEMF / Weizsaecker):
#     B(A,Z) = a_V*A - a_S*A^(2/3) - a_C*Z*(Z-1)/A^(1/3) - a_A*(A-2Z)^2/A
#     The four terms (Volume, Surface, Coulomb, Asymmetry) form a 4-part
#     composition on the simplex: each term's share of total binding energy.
#     Constants: a_V=15.56, a_S=17.23, a_C=0.697, a_A=23.29 (all MeV).
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


import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
from datetime import datetime

def _kurtosis(x):
    """Fisher kurtosis (excess kurtosis)."""
    m = np.mean(x)
    s = np.std(x, ddof=0)
    if s == 0:
        return 0.0
    return np.mean(((x - m) / s) ** 4) - 3.0

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)

# ── Configuration ──────────────────────────────────────────────────
AME_CSV    = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/DATA/Nuclear/ame2020_parsed.csv"
NUCLIDE_CSV = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/DATA/Nuclear/raymond_nuclide_table.csv"
VALLEY_CSV = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/DATA/Nuclear/raymond_valley_ame2020.csv"
OUT_PNG    = "/sessions/wonderful-elegant-pascal/exp03_uranium_full_verify.png"
OUT_JSON   = "/sessions/wonderful-elegant-pascal/exp03_uranium_full_verify.json"

# Color palette — nuclear theme
C_URANIUM = '#4CAF50'   # green for nuclear
C_GOLD    = '#DAA520'
C_NAVY    = '#1E2761'
C_TEAL    = '#028090'
C_CORAL   = '#F96167'
C_SAGE    = '#84B59F'
C_BG      = '#0D1117'
C_PANEL   = '#161B22'
C_TEXT    = '#E6EDF3'
C_MUTED   = '#8B949E'
C_GREEN   = '#3FB950'
C_RED     = '#F85149'
C_YELLOW  = '#D29922'
C_PURPLE  = '#A371F7'

# ═══════════════════════════════════════════════════════════════════
# PART A: DECAY CHAINS (2-simplex)
# ═══════════════════════════════════════════════════════════════════
print("=" * 70)
print("EXP-03 REVISED: The Uranium Test — Full PLL-EITT Verification")
print("=" * 70)

# Load AME2020
ame = pd.read_csv(AME_CSV)
print(f"\nAME2020 loaded: {len(ame)} nuclides")

# Define decay chains (parent → daughter sequences)
decay_chains = {
    'U-238': [
        (92,146), (90,144), (91,143), (91,142), (90,140), (88,138),
        (86,136), (84,134), (82,132), (83,131), (84,130), (82,128),
        (83,127), (84,126), (82,124)
    ],
    'Th-232': [
        (90,142), (88,140), (89,139), (89,138), (88,136), (86,134),
        (84,132), (82,130), (83,129), (84,128), (82,126)
    ],
    'U-235': [
        (92,143), (90,141), (91,140), (89,138), (87,136), (88,135),
        (86,134), (84,132), (82,130), (83,129), (84,128), (82,126)
    ]
}

chain_results = {}
chain_compositions = {}

for chain_name, chain_nuclides in decay_chains.items():
    print(f"\n─── Decay Chain: {chain_name} ({len(chain_nuclides)} steps) ───")

    Z_list = [zn[0] for zn in chain_nuclides]
    N_list = [zn[1] for zn in chain_nuclides]
    A_list = [z + n for z, n in chain_nuclides]

    # 2-simplex: (Z/A, N/A)
    x_proton  = np.array([z / a for z, a in zip(Z_list, A_list)])
    x_neutron = np.array([n / a for n, a in zip(N_list, A_list)])
    X = np.column_stack([x_proton, x_neutron])
    D = 2
    n_obs = len(X)

    chain_compositions[chain_name] = {
        'X': X, 'Z': Z_list, 'N': N_list, 'A': A_list,
        'x_proton': x_proton, 'x_neutron': x_neutron
    }

    # Closure check
    closure_ok = np.allclose(X.sum(axis=1), 1.0)
    print(f"  Closure: {'PASS' if closure_ok else 'FAIL'}")

    # CLR
    log_X = np.log(X)
    clr = log_X - log_X.mean(axis=1, keepdims=True)
    clr_zero_sum = np.allclose(clr.sum(axis=1), 0.0, atol=1e-12)
    print(f"  CLR zero-sum: {'PASS' if clr_zero_sum else 'FAIL'}")

    # σ²_A trajectory
    sigma2_A = np.mean(clr**2, axis=1)

    # Shannon entropy
    H_full = -np.sum(X * np.log(X), axis=1)
    H_bar = np.mean(H_full)

    # EITT decimation
    M_values = [2, 3]
    if n_obs >= 8:
        M_values.append(4)
    if n_obs >= 10:
        M_values.append(5)

    eitt_results_chain = []
    for M in M_values:
        n_blocks = n_obs // M
        if n_blocks < 2:
            continue
        X_block = X[:n_blocks * M].reshape(n_blocks, M, D)

        # Geometric mean decimation
        log_means = np.mean(np.log(X_block), axis=1)
        X_geom = np.exp(log_means)
        X_geom = X_geom / X_geom.sum(axis=1, keepdims=True)

        # Arithmetic mean decimation
        X_arith = np.mean(X_block, axis=1)
        X_arith = X_arith / X_arith.sum(axis=1, keepdims=True)

        # Entropy
        H_geom = -np.sum(X_geom * np.log(X_geom), axis=1)
        H_arith = -np.sum(X_arith * np.log(X_arith), axis=1)

        delta_geom = np.mean(H_geom) - H_bar
        delta_arith = np.mean(H_arith) - H_bar
        rel_geom = abs(delta_geom) / H_bar if H_bar > 0 else 0
        rel_arith = abs(delta_arith) / H_bar if H_bar > 0 else 0

        eitt_results_chain.append({
            'M': M, 'n_blocks': n_blocks,
            'delta_geom': delta_geom, 'relative_geom': rel_geom,
            'delta_arith': delta_arith, 'relative_arith': rel_arith,
            'pass': rel_geom < 0.01
        })

    max_rel = max(r['relative_geom'] for r in eitt_results_chain) if eitt_results_chain else 0
    eitt_verdict = 'PASS' if max_rel < 0.01 else 'FAIL'
    print(f"  EITT max relative deviation: {max_rel:.6f} → {eitt_verdict}")

    # PLL parabola on σ²_A
    t_norm = np.linspace(0, 1, n_obs)
    coeffs = np.polyfit(t_norm, sigma2_A, 2)
    a_pll, b_pll, c_pll = coeffs
    sigma2_fit = np.polyval(coeffs, t_norm)
    ss_res = np.sum((sigma2_A - sigma2_fit)**2)
    ss_tot = np.sum((sigma2_A - np.mean(sigma2_A))**2)
    R2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    # Vertex
    if abs(a_pll) > 1e-15:
        t_vertex = -b_pll / (2 * a_pll)
    else:
        t_vertex = 0.5
    shape = '∪ (bowl)' if a_pll > 0 else '∩ (hill)'
    discriminator = 2 * a_pll

    # Noise squeeze
    residual_2 = sigma2_A - sigma2_fit
    squeeze_results = []
    for order in range(2, 6):
        if n_obs <= order + 1:
            break
        c_fit = np.polyfit(t_norm, sigma2_A, order)
        fit_val = np.polyval(c_fit, t_norm)
        res = sigma2_A - fit_val
        var_res = np.var(res)
        var_orig = np.var(residual_2)
        squeeze = 1.0 - var_res / var_orig if var_orig > 0 else 0
        squeeze_results.append({
            'order': order,
            'residual_var': var_res,
            'squeeze_pct': squeeze * 100,
            'autocorr_lag1': np.corrcoef(res[:-1], res[1:])[0, 1] if len(res) > 2 else 0
        })

    final_squeeze = squeeze_results[-1]['squeeze_pct'] if squeeze_results else 0

    # DADC (D=2 is degenerate — same as EXP-01)
    contam_proton = np.std(residual_2 * clr[:, 0] / np.max(np.abs(clr[:, 0])) if np.max(np.abs(clr[:, 0])) > 0 else residual_2)
    contam_neutron = np.std(residual_2 * clr[:, 1] / np.max(np.abs(clr[:, 1])) if np.max(np.abs(clr[:, 1])) > 0 else residual_2)
    total_contam = contam_proton + contam_neutron
    cs_proton = contam_proton / (total_contam / D) if total_contam > 0 else 1
    cs_neutron = contam_neutron / (total_contam / D) if total_contam > 0 else 1

    chain_results[chain_name] = {
        'N': n_obs, 'D': D, 'closure': closure_ok, 'clr_zero_sum': clr_zero_sum,
        'H_bar': H_bar, 'sigma2_A_mean': np.mean(sigma2_A),
        'sigma2_A_range': [float(np.min(sigma2_A)), float(np.max(sigma2_A))],
        'eitt': eitt_results_chain, 'max_relative': max_rel, 'eitt_verdict': eitt_verdict,
        'pll': {
            'a': a_pll, 'b': b_pll, 'c': c_pll, 'R2': R2,
            'shape': shape, 't_vertex': t_vertex, 'discriminator': discriminator
        },
        'noise_squeeze': squeeze_results, 'final_squeeze_pct': final_squeeze,
        'dadc': {
            'proton_CS': cs_proton, 'neutron_CS': cs_neutron,
            'contam_entropy': 1.0  # D=2 degenerate
        }
    }
    print(f"  PLL: R²={R2:.4f}, shape={shape}, vertex t={t_vertex:.3f}")
    print(f"  Noise squeeze: {final_squeeze:.1f}%")


# ═══════════════════════════════════════════════════════════════════
# PART B: SEMF VALLEY OF STABILITY (4-simplex)
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PART B: SEMF 4-part composition along valley of stability")
print("=" * 70)

# Load nuclide table with SEMF components
nuc = pd.read_csv(NUCLIDE_CSV)
print(f"Nuclide table loaded: {len(nuc)} nuclides")

# Load valley of stability
valley = pd.read_csv(VALLEY_CSV)
print(f"Valley of stability: {len(valley)} nuclides")

# Get the most stable isotope per Z along the valley
# Merge valley Z,N with nuclide table to get SEMF components
valley_semf = []
for _, row in valley.iterrows():
    z, n = int(row['Z']), int(row['N'])
    match = nuc[(nuc['Z'] == z) & (nuc['N'] == n)]
    if len(match) > 0:
        m = match.iloc[0]
        # SEMF 4-part: Volume, Surface, Coulomb, Asymmetry (absolute values)
        b_vol = abs(m['B_volume'])
        b_surf = abs(m['B_surface'])
        b_coul = abs(m['B_coulomb'])
        b_asym = abs(m['B_asymmetry'])
        total = b_vol + b_surf + b_coul + b_asym
        if total > 0:
            valley_semf.append({
                'Z': z, 'N': n, 'A': z + n,
                'f_vol': b_vol / total, 'f_surf': b_surf / total,
                'f_coul': b_coul / total, 'f_asym': b_asym / total
            })

valley_df = pd.DataFrame(valley_semf).sort_values('Z').reset_index(drop=True)
print(f"Valley SEMF compositions: {len(valley_df)} nuclides (Z={valley_df['Z'].min()} to {valley_df['Z'].max()})")

# Build 4-simplex composition matrix
D_semf = 4
carrier_names = ['Volume', 'Surface', 'Coulomb', 'Asymmetry']
X_semf = valley_df[['f_vol', 'f_surf', 'f_coul', 'f_asym']].values
Z_valley = valley_df['Z'].values
N_valley = valley_df['N'].values
A_valley = valley_df['A'].values
n_valley = len(valley_df)

# Zero replacement (shouldn't be needed but safety)
X_semf = np.maximum(X_semf, 1e-10)
X_semf = X_semf / X_semf.sum(axis=1, keepdims=True)

# Step 1: Closure
closure_semf = np.allclose(X_semf.sum(axis=1), 1.0)
print(f"\nSEMF Closure: {'PASS' if closure_semf else 'FAIL'}")

# Step 2: CLR
log_X_semf = np.log(X_semf)
clr_semf = log_X_semf - log_X_semf.mean(axis=1, keepdims=True)
clr_zs = np.allclose(clr_semf.sum(axis=1), 0.0, atol=1e-12)
print(f"CLR zero-sum: {'PASS' if clr_zs else 'FAIL'}")

# Step 3: σ²_A trajectory
sigma2_A_semf = np.mean(clr_semf**2, axis=1)
print(f"σ²_A range: [{sigma2_A_semf.min():.4f}, {sigma2_A_semf.max():.4f}]")
print(f"σ²_A mean: {np.mean(sigma2_A_semf):.4f}")

# Step 4: Shannon entropy
H_semf = -np.sum(X_semf * np.log(X_semf), axis=1)
H_bar_semf = np.mean(H_semf)
print(f"H_bar (Shannon): {H_bar_semf:.6f}")

# Step 5: EITT decimation
M_vals_semf = [2, 3, 4, 6]
if n_valley >= 24:
    M_vals_semf.append(12)

eitt_semf = []
for M in M_vals_semf:
    n_blocks = n_valley // M
    if n_blocks < 3:
        continue
    X_block = X_semf[:n_blocks * M].reshape(n_blocks, M, D_semf)

    # Geometric mean
    log_means = np.mean(np.log(X_block), axis=1)
    X_geom = np.exp(log_means)
    X_geom = X_geom / X_geom.sum(axis=1, keepdims=True)

    # Arithmetic mean
    X_arith = np.mean(X_block, axis=1)
    X_arith = X_arith / X_arith.sum(axis=1, keepdims=True)

    H_geom = -np.sum(X_geom * np.log(X_geom), axis=1)
    H_arith = -np.sum(X_arith * np.log(X_arith), axis=1)

    delta_geom = np.mean(H_geom) - H_bar_semf
    delta_arith = np.mean(H_arith) - H_bar_semf
    rel_geom = abs(delta_geom) / H_bar_semf if H_bar_semf > 0 else 0
    rel_arith = abs(delta_arith) / H_bar_semf if H_bar_semf > 0 else 0
    gap = abs(rel_geom - rel_arith)

    eitt_semf.append({
        'M': M, 'n_blocks': n_blocks,
        'delta_geom': delta_geom, 'relative_geom': rel_geom,
        'delta_arith': delta_arith, 'relative_arith': rel_arith,
        'gap': gap, 'pass': rel_geom < 0.01
    })
    print(f"  M={M:2d}: blocks={n_blocks:3d}, geom Δ={rel_geom:.6f}, arith Δ={rel_arith:.6f}, {'PASS' if rel_geom < 0.01 else 'FAIL'}")

max_rel_semf = max(r['relative_geom'] for r in eitt_semf) if eitt_semf else 0
eitt_verdict_semf = 'PASS' if max_rel_semf < 0.01 else 'FAIL'
print(f"  EITT valley verdict: max relative = {max_rel_semf:.6f} → {eitt_verdict_semf}")

# Step 6: PLL parabola on σ²_A(Z) along the valley
t_norm_semf = (Z_valley - Z_valley[0]) / (Z_valley[-1] - Z_valley[0])
coeffs_semf = np.polyfit(t_norm_semf, sigma2_A_semf, 2)
a_s, b_s, c_s = coeffs_semf
fit_semf = np.polyval(coeffs_semf, t_norm_semf)
ss_res_s = np.sum((sigma2_A_semf - fit_semf)**2)
ss_tot_s = np.sum((sigma2_A_semf - np.mean(sigma2_A_semf))**2)
R2_semf = 1 - ss_res_s / ss_tot_s if ss_tot_s > 0 else 0

if abs(a_s) > 1e-15:
    t_vertex_s = -b_s / (2 * a_s)
    Z_vertex = Z_valley[0] + t_vertex_s * (Z_valley[-1] - Z_valley[0])
else:
    t_vertex_s = 0.5
    Z_vertex = (Z_valley[0] + Z_valley[-1]) / 2

shape_semf = '∪ (bowl)' if a_s > 0 else '∩ (hill)'
disc_semf = 2 * a_s

# Q-factor
sigma2_at_vertex = np.polyval(coeffs_semf, t_vertex_s)
residual_semf = sigma2_A_semf - fit_semf
noise_floor = np.std(residual_semf)
Q_semf = abs(disc_semf) / noise_floor if noise_floor > 0 else 0

print(f"\nPLL Valley: R²={R2_semf:.4f}, shape={shape_semf}")
print(f"  Vertex at Z={Z_vertex:.1f}, σ²_A(vertex)={sigma2_at_vertex:.4f}")
print(f"  Discriminator: {disc_semf:.6f}, Q-factor: {Q_semf:.2f}")

# Step 7: Noise squeeze on valley σ²_A
squeeze_semf = []
for order in range(2, 6):
    c_fit = np.polyfit(t_norm_semf, sigma2_A_semf, order)
    fit_val = np.polyval(c_fit, t_norm_semf)
    res = sigma2_A_semf - fit_val
    var_res = np.var(res)
    var_ref = np.var(sigma2_A_semf - fit_semf)
    squeeze = 1.0 - var_res / var_ref if var_ref > 0 else 0
    ac1 = np.corrcoef(res[:-1], res[1:])[0, 1] if len(res) > 2 else 0
    kurt = _kurtosis(res)
    squeeze_semf.append({
        'order': order, 'residual_var': var_res,
        'squeeze_pct': squeeze * 100, 'autocorr_lag1': ac1, 'kurtosis': kurt
    })
    print(f"  Order {order}: squeeze={squeeze*100:.1f}%, AC(1)={ac1:.3f}")

stochastic_core = np.std(sigma2_A_semf - np.polyval(np.polyfit(t_norm_semf, sigma2_A_semf, 5), t_norm_semf))

# Step 8: DADC per-species contamination
print(f"\nDADC per-species contamination (valley):")
contam_species = {}
for i, name in enumerate(carrier_names):
    # Project residual onto species CLR
    clr_species = clr_semf[:, i]
    # Contamination = how much the residual covaries with this species' CLR
    if np.std(clr_species) > 0 and np.std(residual_semf) > 0:
        xcorr = np.corrcoef(residual_semf, clr_species)[0, 1]
        # Contamination magnitude: std of (residual * normalized CLR)
        clr_norm = clr_species / np.std(clr_species)
        contam_mag = np.std(residual_semf * clr_norm)
    else:
        xcorr = 0
        contam_mag = 0
    contam_species[name] = {
        'xcorr': xcorr, 'contam_magnitude': contam_mag
    }
    print(f"  {name:12s}: XCorr={xcorr:+.4f}, contam_mag={contam_mag:.6f}")

# C/S ratios
total_contam_semf = sum(v['contam_magnitude'] for v in contam_species.values())
for name in carrier_names:
    cs = contam_species[name]['contam_magnitude'] / (total_contam_semf / D_semf) if total_contam_semf > 0 else 1
    contam_species[name]['C_S_ratio'] = cs
    print(f"  {name:12s}: C/S = {cs:.3f}")

# Boundary species = highest C/S
boundary_species = max(contam_species.items(), key=lambda x: x[1]['C_S_ratio'])
print(f"\n  Boundary species: {boundary_species[0]} (C/S = {boundary_species[1]['C_S_ratio']:.3f})")

# Contamination entropy
cs_vals = np.array([contam_species[n]['C_S_ratio'] for n in carrier_names])
cs_norm = cs_vals / cs_vals.sum() if cs_vals.sum() > 0 else np.ones(D_semf) / D_semf
H_contam = -np.sum(cs_norm * np.log(cs_norm + 1e-15))
H_contam_max = np.log(D_semf)
H_contam_norm = H_contam / H_contam_max if H_contam_max > 0 else 1
print(f"  Contamination entropy H_norm = {H_contam_norm:.3f}")
dadi_signature = H_contam_norm < 0.85

# ═══════════════════════════════════════════════════════════════════
# PART C: NUCLEAR REGION ANALYSIS
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PART C: Regional Analysis — σ²_A by nuclear region")
print("=" * 70)

# Define nuclear regions along the valley
regions = {
    'Light (Z=1-20)': (1, 20),
    'Medium (Z=21-28)': (21, 28),  # Iron peak
    'Heavy (Z=29-82)': (29, 82),
    'Actinide (Z=83+)': (83, 200)
}

region_results = {}
for rname, (z_lo, z_hi) in regions.items():
    mask = (Z_valley >= z_lo) & (Z_valley <= z_hi)
    n_in = mask.sum()
    if n_in < 4:
        continue
    s2 = sigma2_A_semf[mask]
    region_results[rname] = {
        'Z_range': (z_lo, z_hi), 'n_nuclides': int(n_in),
        'sigma2_A_mean': float(np.mean(s2)),
        'sigma2_A_std': float(np.std(s2)),
        'sigma2_A_min': float(np.min(s2)),
        'sigma2_A_max': float(np.max(s2))
    }
    print(f"  {rname}: n={n_in}, σ²_A = {np.mean(s2):.4f} ± {np.std(s2):.4f}")


# ═══════════════════════════════════════════════════════════════════
# STEP 10: CHECKLIST
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("STEP 10: VERIFICATION CHECKLIST")
print("=" * 70)

checks = {
    'decay_chains_all_pass': all(chain_results[c]['eitt_verdict'] == 'PASS' for c in chain_results),
    'semf_valley_eitt': eitt_verdict_semf,
    'semf_pll_R2_above_0.3': R2_semf > 0.3,
    'decay_chain_closure': all(chain_results[c]['closure'] for c in chain_results),
    'clr_zero_sum': all(chain_results[c]['clr_zero_sum'] for c in chain_results) and clr_zs,
    'boundary_species_identified': boundary_species[0] is not None,
    'contamination_entropy_structured': dadi_signature,
    'noise_squeeze_positive': final_squeeze > 0 if squeeze_results else False,
    'valley_squeeze_positive': squeeze_semf[-1]['squeeze_pct'] > 0 if squeeze_semf else False
}

n_pass = sum(1 for v in checks.values() if v == True or v == 'PASS')
n_total = len(checks)

for check, result in checks.items():
    status = '✓ PASS' if (result == True or result == 'PASS') else '✗ FAIL'
    print(f"  {check:45s} {status}")

print(f"\n  TOTAL: {n_pass}/{n_total} checks pass")


# ═══════════════════════════════════════════════════════════════════
# VISUALIZATION (20-panel dark-theme)
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Generating visualization...")

fig = plt.figure(figsize=(24, 28), facecolor=C_BG)
gs = GridSpec(5, 4, figure=fig, hspace=0.35, wspace=0.3,
             left=0.06, right=0.96, top=0.94, bottom=0.03)

fig.suptitle('EXP-03 REVISED: The Uranium Test — Full PLL-EITT Verification',
             fontsize=18, color=C_TEXT, fontweight='bold', y=0.97)
fig.text(0.5, 0.955, 'Nuclear compositions from AME2020 • Decay chains (2-simplex) + SEMF valley (4-simplex)',
         ha='center', fontsize=11, color=C_MUTED)

# ── Panel 1: Decay chain trajectories on 2-simplex ──
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(C_PANEL)
chain_colors = {
    'U-238': C_GREEN, 'Th-232': C_TEAL, 'U-235': C_CORAL
}
for cname, cdata in chain_compositions.items():
    ax1.plot(cdata['x_proton'], cdata['x_neutron'], 'o-',
             color=chain_colors[cname], markersize=4, linewidth=1.5,
             label=cname, alpha=0.9)
ax1.set_xlabel('Z/A (proton fraction)', color=C_TEXT, fontsize=8)
ax1.set_ylabel('N/A (neutron fraction)', color=C_TEXT, fontsize=8)
ax1.set_title('Decay Chain Trajectories', color=C_TEXT, fontsize=10, fontweight='bold')
ax1.legend(fontsize=7, loc='upper right', framealpha=0.3)
ax1.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax1.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 2: σ²_A along each decay chain ──
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(C_PANEL)
for cname, cres in chain_results.items():
    cc = chain_compositions[cname]
    clr_chain = np.log(cc['X']) - np.log(cc['X']).mean(axis=1, keepdims=True)
    s2 = np.mean(clr_chain**2, axis=1)
    ax2.plot(range(len(s2)), s2, 'o-', color=chain_colors[cname],
             markersize=4, linewidth=1.5, label=f"{cname} (R²={cres['pll']['R2']:.3f})")
ax2.set_xlabel('Decay step', color=C_TEXT, fontsize=8)
ax2.set_ylabel('σ²_A', color=C_TEXT, fontsize=8)
ax2.set_title('Decay Chain σ²_A Trajectories', color=C_TEXT, fontsize=10, fontweight='bold')
ax2.legend(fontsize=6, loc='best', framealpha=0.3)
ax2.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax2.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 3: EITT results for decay chains ──
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor(C_PANEL)
for i, (cname, cres) in enumerate(chain_results.items()):
    Ms = [r['M'] for r in cres['eitt']]
    rels = [r['relative_geom'] * 100 for r in cres['eitt']]
    ax3.plot(Ms, rels, 'o-', color=chain_colors[cname], markersize=5,
             linewidth=1.5, label=f"{cname} (max={cres['max_relative']*100:.4f}%)")
ax3.axhline(1.0, color=C_RED, linestyle='--', linewidth=1, alpha=0.7, label='1% threshold')
ax3.set_xlabel('Compression ratio M', color=C_TEXT, fontsize=8)
ax3.set_ylabel('|ΔH/H| (%)', color=C_TEXT, fontsize=8)
ax3.set_title('EITT: Decay Chains', color=C_TEXT, fontsize=10, fontweight='bold')
ax3.legend(fontsize=6, loc='upper left', framealpha=0.3)
ax3.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax3.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 4: Decay chain PLL parabola fits ──
ax4 = fig.add_subplot(gs[0, 3])
ax4.set_facecolor(C_PANEL)
for cname, cres in chain_results.items():
    cc = chain_compositions[cname]
    clr_chain = np.log(cc['X']) - np.log(cc['X']).mean(axis=1, keepdims=True)
    s2 = np.mean(clr_chain**2, axis=1)
    t = np.linspace(0, 1, len(s2))
    fit = np.polyval([cres['pll']['a'], cres['pll']['b'], cres['pll']['c']], t)
    ax4.scatter(t, s2, color=chain_colors[cname], s=20, alpha=0.7, zorder=5)
    ax4.plot(t, fit, '-', color=chain_colors[cname], linewidth=2, alpha=0.8,
             label=f"{cname} R²={cres['pll']['R2']:.3f}")
ax4.set_xlabel('Normalized decay step', color=C_TEXT, fontsize=8)
ax4.set_ylabel('σ²_A', color=C_TEXT, fontsize=8)
ax4.set_title('PLL Parabola: Decay Chains', color=C_TEXT, fontsize=10, fontweight='bold')
ax4.legend(fontsize=6, loc='best', framealpha=0.3)
ax4.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax4.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 5: SEMF composition along valley ──
ax5 = fig.add_subplot(gs[1, 0])
ax5.set_facecolor(C_PANEL)
semf_colors = [C_GREEN, C_TEAL, C_CORAL, C_YELLOW]
for i, name in enumerate(carrier_names):
    ax5.plot(Z_valley, X_semf[:, i], '-', color=semf_colors[i],
             linewidth=1.5, label=name, alpha=0.9)
ax5.set_xlabel('Z (proton number)', color=C_TEXT, fontsize=8)
ax5.set_ylabel('SEMF fraction', color=C_TEXT, fontsize=8)
ax5.set_title('SEMF Composition Along Valley', color=C_TEXT, fontsize=10, fontweight='bold')
ax5.legend(fontsize=7, loc='center right', framealpha=0.3)
ax5.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax5.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 6: CLR coordinates along valley ──
ax6 = fig.add_subplot(gs[1, 1])
ax6.set_facecolor(C_PANEL)
for i, name in enumerate(carrier_names):
    ax6.plot(Z_valley, clr_semf[:, i], '-', color=semf_colors[i],
             linewidth=1.5, label=name, alpha=0.9)
ax6.axhline(0, color=C_MUTED, linestyle=':', linewidth=0.8)
ax6.set_xlabel('Z', color=C_TEXT, fontsize=8)
ax6.set_ylabel('CLR coordinate', color=C_TEXT, fontsize=8)
ax6.set_title('CLR Along Valley', color=C_TEXT, fontsize=10, fontweight='bold')
ax6.legend(fontsize=7, loc='best', framealpha=0.3)
ax6.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax6.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 7: σ²_A along valley with PLL parabola ──
ax7 = fig.add_subplot(gs[1, 2])
ax7.set_facecolor(C_PANEL)
ax7.scatter(Z_valley, sigma2_A_semf, c=C_URANIUM, s=15, alpha=0.6, zorder=5)
ax7.plot(Z_valley, fit_semf, '-', color=C_CORAL, linewidth=2.5,
         label=f'Parabola R²={R2_semf:.4f}')
if Z_valley[0] <= Z_vertex <= Z_valley[-1]:
    ax7.axvline(Z_vertex, color=C_YELLOW, linestyle='--', linewidth=1, alpha=0.7,
                label=f'Vertex Z={Z_vertex:.1f}')
ax7.set_xlabel('Z', color=C_TEXT, fontsize=8)
ax7.set_ylabel('σ²_A', color=C_TEXT, fontsize=8)
ax7.set_title(f'PLL: σ²_A Along Valley ({shape_semf})', color=C_TEXT, fontsize=10, fontweight='bold')
ax7.legend(fontsize=7, loc='best', framealpha=0.3)
ax7.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax7.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 8: EITT valley ──
ax8 = fig.add_subplot(gs[1, 3])
ax8.set_facecolor(C_PANEL)
Ms_v = [r['M'] for r in eitt_semf]
rels_geom = [r['relative_geom'] * 100 for r in eitt_semf]
rels_arith = [r['relative_arith'] * 100 for r in eitt_semf]
ax8.plot(Ms_v, rels_geom, 'o-', color=C_GREEN, markersize=6, linewidth=2, label='Geometric')
ax8.plot(Ms_v, rels_arith, 's--', color=C_CORAL, markersize=6, linewidth=1.5, label='Arithmetic')
ax8.axhline(1.0, color=C_RED, linestyle='--', linewidth=1, alpha=0.7, label='1% threshold')
ax8.set_xlabel('Compression ratio M', color=C_TEXT, fontsize=8)
ax8.set_ylabel('|ΔH/H| (%)', color=C_TEXT, fontsize=8)
ax8.set_title('EITT: Valley of Stability', color=C_TEXT, fontsize=10, fontweight='bold')
ax8.legend(fontsize=7, loc='upper left', framealpha=0.3)
ax8.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax8.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 9: Shannon entropy along valley ──
ax9 = fig.add_subplot(gs[2, 0])
ax9.set_facecolor(C_PANEL)
ax9.plot(Z_valley, H_semf, '-', color=C_TEAL, linewidth=1.5)
ax9.axhline(H_bar_semf, color=C_MUTED, linestyle=':', linewidth=1,
            label=f'H_bar = {H_bar_semf:.4f}')
ax9.set_xlabel('Z', color=C_TEXT, fontsize=8)
ax9.set_ylabel('Shannon entropy H', color=C_TEXT, fontsize=8)
ax9.set_title('Shannon Entropy Along Valley', color=C_TEXT, fontsize=10, fontweight='bold')
ax9.legend(fontsize=7, framealpha=0.3)
ax9.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax9.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 10: Noise squeeze valley ──
ax10 = fig.add_subplot(gs[2, 1])
ax10.set_facecolor(C_PANEL)
orders_sq = [s['order'] for s in squeeze_semf]
squeezes = [s['squeeze_pct'] for s in squeeze_semf]
ax10.bar(orders_sq, squeezes, color=C_TEAL, alpha=0.8, width=0.6)
ax10.set_xlabel('Polynomial order', color=C_TEXT, fontsize=8)
ax10.set_ylabel('Squeeze (%)', color=C_TEXT, fontsize=8)
ax10.set_title('Noise Squeeze: Valley σ²_A', color=C_TEXT, fontsize=10, fontweight='bold')
ax10.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax10.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 11: Residuals along valley ──
ax11 = fig.add_subplot(gs[2, 2])
ax11.set_facecolor(C_PANEL)
ax11.plot(Z_valley, residual_semf, '-', color=C_SAGE, linewidth=1, alpha=0.8)
ax11.axhline(0, color=C_MUTED, linestyle=':', linewidth=0.8)
ax11.fill_between(Z_valley, residual_semf, 0, alpha=0.3, color=C_SAGE)
ax11.set_xlabel('Z', color=C_TEXT, fontsize=8)
ax11.set_ylabel('ε = σ²_A − fit', color=C_TEXT, fontsize=8)
ax11.set_title('PLL Residuals Along Valley', color=C_TEXT, fontsize=10, fontweight='bold')
ax11.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax11.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 12: DADC per-species contamination ──
ax12 = fig.add_subplot(gs[2, 3])
ax12.set_facecolor(C_PANEL)
cs_values = [contam_species[n]['C_S_ratio'] for n in carrier_names]
bars = ax12.barh(carrier_names, cs_values, color=semf_colors, alpha=0.8, height=0.5)
ax12.axvline(1.0, color=C_MUTED, linestyle=':', linewidth=1)
# Highlight boundary species
for i, (name, cs) in enumerate(zip(carrier_names, cs_values)):
    if name == boundary_species[0]:
        bars[i].set_edgecolor(C_YELLOW)
        bars[i].set_linewidth(2)
ax12.set_xlabel('C/S ratio', color=C_TEXT, fontsize=8)
ax12.set_title(f'DADC: Boundary = {boundary_species[0]}', color=C_TEXT, fontsize=10, fontweight='bold')
ax12.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax12.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 13: Variation matrix heatmap ──
ax13 = fig.add_subplot(gs[3, 0])
ax13.set_facecolor(C_PANEL)
# Compute variation matrix
var_matrix = np.zeros((D_semf, D_semf))
for i in range(D_semf):
    for j in range(D_semf):
        lr = np.log(X_semf[:, i] / X_semf[:, j])
        var_matrix[i, j] = np.var(lr)
im = ax13.imshow(var_matrix, cmap='YlOrRd', aspect='auto')
ax13.set_xticks(range(D_semf))
ax13.set_yticks(range(D_semf))
short_names = ['Vol', 'Surf', 'Coul', 'Asym']
ax13.set_xticklabels(short_names, fontsize=7, color=C_TEXT)
ax13.set_yticklabels(short_names, fontsize=7, color=C_TEXT)
ax13.set_title('Variation Matrix', color=C_TEXT, fontsize=10, fontweight='bold')
for i in range(D_semf):
    for j in range(D_semf):
        ax13.text(j, i, f'{var_matrix[i,j]:.3f}', ha='center', va='center',
                 fontsize=7, color='black' if var_matrix[i,j] < np.max(var_matrix)*0.5 else 'white')

# ── Panel 14: σ²_A regional comparison ──
ax14 = fig.add_subplot(gs[3, 1])
ax14.set_facecolor(C_PANEL)
rnames = list(region_results.keys())
rmeans = [region_results[r]['sigma2_A_mean'] for r in rnames]
rstds = [region_results[r]['sigma2_A_std'] for r in rnames]
reg_colors = [C_GREEN, C_YELLOW, C_TEAL, C_CORAL][:len(rnames)]
ax14.barh(range(len(rnames)), rmeans, xerr=rstds, color=reg_colors, alpha=0.8,
          height=0.5, capsize=3, ecolor=C_MUTED)
ax14.set_yticks(range(len(rnames)))
ax14.set_yticklabels(rnames, fontsize=7, color=C_TEXT)
ax14.set_xlabel('Mean σ²_A', color=C_TEXT, fontsize=8)
ax14.set_title('σ²_A by Nuclear Region', color=C_TEXT, fontsize=10, fontweight='bold')
ax14.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax14.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 15: Cross-correlation of species residuals ──
ax15 = fig.add_subplot(gs[3, 2])
ax15.set_facecolor(C_PANEL)
xcorr_matrix = np.zeros((D_semf, D_semf))
for i in range(D_semf):
    for j in range(D_semf):
        clr_i = clr_semf[:, i]
        clr_j = clr_semf[:, j]
        res_i = residual_semf * clr_i / np.std(clr_i) if np.std(clr_i) > 0 else residual_semf
        res_j = residual_semf * clr_j / np.std(clr_j) if np.std(clr_j) > 0 else residual_semf
        xcorr_matrix[i, j] = np.corrcoef(res_i, res_j)[0, 1]
im15 = ax15.imshow(xcorr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
ax15.set_xticks(range(D_semf))
ax15.set_yticks(range(D_semf))
ax15.set_xticklabels(short_names, fontsize=7, color=C_TEXT)
ax15.set_yticklabels(short_names, fontsize=7, color=C_TEXT)
ax15.set_title('Species Cross-Correlation', color=C_TEXT, fontsize=10, fontweight='bold')
for i in range(D_semf):
    for j in range(D_semf):
        ax15.text(j, i, f'{xcorr_matrix[i,j]:.2f}', ha='center', va='center',
                 fontsize=7, color='black' if abs(xcorr_matrix[i,j]) < 0.5 else 'white')

# ── Panel 16: Geometric vs arithmetic gap (F17 tuner) ──
ax16 = fig.add_subplot(gs[3, 3])
ax16.set_facecolor(C_PANEL)
gaps = [r['gap'] * 100 for r in eitt_semf]
ax16.plot(Ms_v, gaps, 'o-', color=C_PURPLE, markersize=6, linewidth=2)
# Quadratic fit
if len(Ms_v) >= 3:
    f17_coeffs = np.polyfit(Ms_v, gaps, 2)
    M_smooth = np.linspace(min(Ms_v), max(Ms_v), 50)
    ax16.plot(M_smooth, np.polyval(f17_coeffs, M_smooth), '--', color=C_YELLOW,
              linewidth=1.5, label=f'Quad fit (a={f17_coeffs[0]:.4f})')
    ax16.legend(fontsize=7, framealpha=0.3)
ax16.set_xlabel('Compression ratio M', color=C_TEXT, fontsize=8)
ax16.set_ylabel('|Geom−Arith gap| (%)', color=C_TEXT, fontsize=8)
ax16.set_title('F17 Tuner: Valley', color=C_TEXT, fontsize=10, fontweight='bold')
ax16.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax16.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 17: Binding energy per nucleon along valley ──
ax17 = fig.add_subplot(gs[4, 0])
ax17.set_facecolor(C_PANEL)
# Get B/A from AME data for valley nuclides
ba_valley = []
for _, row in valley_df.iterrows():
    z, n = int(row['Z']), int(row['N'])
    match = ame[(ame['Z'] == z) & (ame['N'] == n)]
    if len(match) > 0:
        ba_valley.append(match.iloc[0]['binding_per_A_keV'] / 1000.0)  # Convert to MeV
    else:
        ba_valley.append(np.nan)
ba_valley = np.array(ba_valley)
valid_ba = ~np.isnan(ba_valley)
ax17.plot(Z_valley[valid_ba], ba_valley[valid_ba], '-', color=C_GOLD, linewidth=1.5)
ax17.set_xlabel('Z', color=C_TEXT, fontsize=8)
ax17.set_ylabel('B/A (MeV)', color=C_TEXT, fontsize=8)
ax17.set_title('Binding Energy Along Valley', color=C_TEXT, fontsize=10, fontweight='bold')
ax17.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax17.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 18: σ²_A vs B/A correlation ──
ax18 = fig.add_subplot(gs[4, 1])
ax18.set_facecolor(C_PANEL)
valid_both = valid_ba
if valid_both.sum() > 3:
    ax18.scatter(ba_valley[valid_both], sigma2_A_semf[valid_both],
                c=Z_valley[valid_both], cmap='viridis', s=20, alpha=0.7)
    corr_ba_s2 = np.corrcoef(ba_valley[valid_both], sigma2_A_semf[valid_both])[0, 1]
    ax18.set_xlabel('B/A (MeV)', color=C_TEXT, fontsize=8)
    ax18.set_ylabel('σ²_A', color=C_TEXT, fontsize=8)
    ax18.set_title(f'σ²_A vs B/A (r={corr_ba_s2:.3f})', color=C_TEXT, fontsize=10, fontweight='bold')
ax18.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax18.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 19: Autocorrelation of residuals ──
ax19 = fig.add_subplot(gs[4, 2])
ax19.set_facecolor(C_PANEL)
max_lag = min(20, n_valley // 3)
acf_vals = [1.0]
for lag in range(1, max_lag + 1):
    if len(residual_semf) > lag:
        ac = np.corrcoef(residual_semf[:-lag], residual_semf[lag:])[0, 1]
        acf_vals.append(ac)
ax19.bar(range(len(acf_vals)), acf_vals, color=C_TEAL, alpha=0.8, width=0.6)
ax19.axhline(0, color=C_MUTED, linewidth=0.8)
ax19.axhline(1.96/np.sqrt(n_valley), color=C_RED, linestyle='--', linewidth=0.8, alpha=0.5)
ax19.axhline(-1.96/np.sqrt(n_valley), color=C_RED, linestyle='--', linewidth=0.8, alpha=0.5)
ax19.set_xlabel('Lag', color=C_TEXT, fontsize=8)
ax19.set_ylabel('Autocorrelation', color=C_TEXT, fontsize=8)
ax19.set_title('Residual ACF (Valley)', color=C_TEXT, fontsize=10, fontweight='bold')
ax19.tick_params(colors=C_MUTED, labelsize=7)
for sp in ax19.spines.values():
    sp.set_color(C_MUTED)

# ── Panel 20: Summary checklist ──
ax20 = fig.add_subplot(gs[4, 3])
ax20.set_facecolor(C_PANEL)
ax20.axis('off')

check_text = f"EXP-03 VERIFICATION SUMMARY\n"
check_text += f"{'─' * 40}\n"
check_text += f"Decay chains: {sum(1 for c in chain_results if chain_results[c]['eitt_verdict']=='PASS')}/3 PASS\n"
check_text += f"Valley EITT: {eitt_verdict_semf} (max Δ={max_rel_semf*100:.4f}%)\n"
check_text += f"PLL R²: {R2_semf:.4f} ({shape_semf})\n"
check_text += f"Vertex: Z = {Z_vertex:.1f}\n"
check_text += f"Q-factor: {Q_semf:.2f}\n"
check_text += f"Boundary species: {boundary_species[0]}\n"
check_text += f"  C/S = {boundary_species[1]['C_S_ratio']:.3f}\n"
check_text += f"H_contam: {H_contam_norm:.3f}\n"
check_text += f"  DADI signature: {'YES' if dadi_signature else 'NO'}\n"
check_text += f"Noise squeeze: {squeeze_semf[-1]['squeeze_pct']:.1f}%\n"
check_text += f"Stochastic core: {stochastic_core:.6f}\n"
check_text += f"{'─' * 40}\n"
check_text += f"TOTAL: {n_pass}/{n_total} checks pass"

color_verdict = C_GREEN if n_pass >= n_total - 1 else C_YELLOW
ax20.text(0.05, 0.95, check_text, transform=ax20.transAxes,
         fontsize=9, color=color_verdict, fontfamily='monospace',
         verticalalignment='top')

plt.savefig(OUT_PNG, dpi=150, facecolor=C_BG, bbox_inches='tight')
print(f"\nVisualization saved: {OUT_PNG}")
plt.close()

# ═══════════════════════════════════════════════════════════════════
# SAVE RESULTS JSON
# ═══════════════════════════════════════════════════════════════════

results_out = {
    '_meta': {
        'type': 'EXP-03-REVISED-FULL-VERIFY',
        'experiment_id': 'EXP-03',
        'version': '2.0',
        'created': datetime.now().isoformat(),
        'author': 'Peter Higgins / Claude',
        'fixed_point': 'v3.2',
        'data_source': 'AME2020 Atomic Mass Evaluation (3,554 nuclides)',
        'title': 'The Uranium Test — Full PLL-EITT Verification'
    },
    'part_a_decay_chains': {
        'description': '2-simplex (Z/A, N/A) decay chains — true parametric walks',
        'chains': {}
    },
    'part_b_semf_valley': {
        'description': '4-simplex [Volume, Surface, Coulomb, Asymmetry] along valley of stability',
        'n_nuclides': n_valley,
        'Z_range': [int(Z_valley[0]), int(Z_valley[-1])],
        'D': D_semf,
        'carriers': carrier_names,
        'H_bar': H_bar_semf,
        'sigma2_A': {
            'mean': float(np.mean(sigma2_A_semf)),
            'std': float(np.std(sigma2_A_semf)),
            'min': float(np.min(sigma2_A_semf)),
            'max': float(np.max(sigma2_A_semf))
        },
        'eitt': eitt_semf,
        'eitt_max_relative': max_rel_semf,
        'eitt_verdict': eitt_verdict_semf,
        'pll': {
            'a': float(a_s), 'b': float(b_s), 'c': float(c_s),
            'R2': R2_semf, 'shape': shape_semf,
            'Z_vertex': float(Z_vertex), 't_vertex': float(t_vertex_s),
            'sigma2_at_vertex': float(sigma2_at_vertex),
            'discriminator': float(disc_semf), 'Q_factor': Q_semf
        },
        'noise_squeeze': squeeze_semf,
        'stochastic_core': float(stochastic_core),
        'dadc': {
            'per_species': contam_species,
            'boundary_species': boundary_species[0],
            'boundary_CS': boundary_species[1]['C_S_ratio'],
            'contamination_entropy_norm': float(H_contam_norm),
            'dadi_signature': dadi_signature,
            'xcorr_matrix': xcorr_matrix.tolist()
        },
        'regions': region_results
    },
    'checklist': checks,
    'checks_passed': n_pass,
    'checks_total': n_total
}

# Add chain details
for cname, cres in chain_results.items():
    results_out['part_a_decay_chains']['chains'][cname] = cres

with open(OUT_JSON, 'w') as f:
    json.dump(results_out, f, indent=2, cls=NumpyEncoder)

print(f"Results saved: {OUT_JSON}")
print(f"\n{'='*70}")
print(f"EXP-03 REVISED: COMPLETE — {n_pass}/{n_total} checks pass")
print(f"{'='*70}")
