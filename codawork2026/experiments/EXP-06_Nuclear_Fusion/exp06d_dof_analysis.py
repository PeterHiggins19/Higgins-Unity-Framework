#!/usr/bin/env python3
"""
EXP-06D  DEGREES OF FREEDOM ANALYSIS — BURNING PLASMA
======================================================

Question: How many independent degrees of freedom control the
energy partition composition in the burning plasma regime?

If DOF = 2, the entire compositional state is a surface that can be
mapped, visualised, and navigated with two control knobs.

Approach
--------
1. Formal channel count: 6 channels on 5-simplex
2. Dead channel elimination: which channels are negligible?
3. Control parameter count: (T, n) at fixed (B, Zeff) = 2 params
4. CLR principal component analysis: how many PCs explain >99%?
5. Intrinsic dimensionality estimation
6. If DOF=2: map the full (T, n) control surface with ignition
   boundary, PLL vertex curve, and boundary species regions

Physics
-------
In burning plasma (T=15-50 keV, n=1.0-3.0 x10^20):
  P_alpha  = (1/4) n^2 <sigma_v> E_alpha     — the fusion fire
  P_brem   = C_b n^2 sqrt(T) Zeff            — radiation floor
  P_cyc    = C_c n T^2 B^2 / (1+0.12T)       — cyclotron
  P_cond   = 3 n 1e20 T 1.602e-16 / (2 tau)  — conduction escape
  P_line   = C_L n^2 f_Z Z^2 sqrt(T)         — impurity line rad
  P_ohmic  = 5e3 T^(-3/2)                    — Spitzer (dead at high T)

At T > 15 keV:
  P_ohmic < 0.01% of total    — DEAD
  P_line  < 0.5% of total     — NEAR-DEAD

Effective system: 4 active channels -> 3-simplex
Parameterised by: (T, n) at fixed (B, Zeff) -> 2D surface in 3-simplex

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
#  PHYSICS (from EXP-06C)
# ============================================================

E_ALPHA_J = 5.64e-13
C_BREM = 5.35e3
C_CYC = 6.2e1
C_LINE = 1.0e3

def bosch_hale_DT(T):
    T = float(T)
    if T < 0.5: return 1e-40
    BG, mrc2 = 34.3827, 1124656.0
    C1,C2,C3 = 1.17302e-9, 1.51361e-2, 7.51886e-2
    C4,C5,C6,C7 = 4.60643e-3, 1.35e-2, -1.0675e-4, 1.366e-5
    numer = T*(C2+T*(C4+T*C6))
    denom = 1.0+T*(C3+T*(C5+T*C7))
    r = numer/denom
    if abs(1.0-r)<1e-15: return 1e-40
    theta = T/(1.0-r)
    if theta<=0: return 1e-40
    xi = (BG**2/(4.0*theta))**(1.0/3.0)
    try: sv = C1*theta*math.sqrt(xi/(mrc2*T**3))*math.exp(-3.0*xi)
    except: return 1e-40
    return max(sv*1e-6, 1e-40)

def tau_E(B_T=5.3, n_20=1.0, P_MW=50.0):
    n_19=n_20*10; eps=2.0/6.2
    try:
        t = (0.0562*15.0**0.93*B_T**0.15*n_19**0.41
             *max(P_MW,0.1)**(-0.69)*6.2**1.97
             *eps**0.58*1.7**0.78*2.5**0.19)
    except: t=0.1
    return max(t, 0.01)

def power_balance(T, n, B=5.3, Zeff=1.5):
    sv = bosch_hale_DT(T)
    P_alpha = 0.25*(n*1e20)**2*sv*E_ALPHA_J
    P_brem = C_BREM*n**2*math.sqrt(max(T,0.01))*Zeff
    P_cyc = C_CYC*n*T**2*B**2/(1.0+0.12*T)
    P_line = C_LINE*n**2*0.02*36*math.sqrt(max(T,0.01))
    P_ohmic = 5e3*max(T,0.1)**(-1.5)
    P_MW = max(P_alpha*830/1e6, 1.0)
    te = tau_E(B, n, max(P_MW,1.0))
    P_cond = 3.0*n*1e20*T*1.602e-16/(2.0*te)
    P_loss = P_brem+P_cyc+P_line+P_cond
    ignited = P_alpha >= P_loss
    return {
        "P_alpha":P_alpha, "P_brem":P_brem, "P_cyc":P_cyc,
        "P_line":P_line, "P_cond":P_cond, "P_ohmic":P_ohmic,
        "P_loss":P_loss, "ignited":ignited,
        "margin": P_alpha-P_loss,
        "Q": 5*P_alpha/max(P_loss-P_alpha,1e-30) if P_alpha<P_loss else float('inf'),
    }

ALL_CH = ["P_alpha","P_brem","P_cyc","P_line","P_cond","P_ohmic"]
NAMES = {"P_alpha":"Alpha","P_brem":"Brem","P_cyc":"Cyclo",
         "P_line":"Line","P_cond":"Cond","P_ohmic":"Ohmic"}

def pb_to_comp(pb):
    vals = [max(pb[c],1e-30) for c in ALL_CH]
    s = sum(vals)
    return [v/s for v in vals]

def clr(x):
    n=len(x); safe=[max(xi,1e-20) for xi in x]
    lg=[math.log(xi) for xi in safe]; m=sum(lg)/n
    return [l-m for l in lg]


# ============================================================
#  ANALYSIS 1: CHANNEL MAGNITUDE SURVEY
# ============================================================

def channel_survey():
    """Survey power fractions across the burning plasma window."""
    print("="*70)
    print("  ANALYSIS 1: CHANNEL MAGNITUDE SURVEY")
    print("  Burning plasma regime: T=15-50 keV, n=1.0-3.0")
    print("="*70)

    temps = [15,18,20,22,25,28,30,35,40,45,50]
    densities = [1.0, 1.5, 2.0, 2.5, 3.0]

    dead_channels = {"P_ohmic": [], "P_line": []}
    all_fracs = {ch: [] for ch in ALL_CH}

    print(f"\n  {'T':>4s} {'n':>4s} | {'Alpha':>7s} {'Brem':>7s} {'Cyclo':>7s} "
          f"{'Line':>7s} {'Cond':>7s} {'Ohmic':>7s} | {'IGN':>4s}")
    print(f"  {'-'*70}")

    for T in temps:
        for n in densities:
            pb = power_balance(T, n)
            comp = pb_to_comp(pb)
            fracs = {ALL_CH[i]: comp[i]*100 for i in range(6)}
            for ch in ALL_CH:
                all_fracs[ch].append(fracs[ch])
            dead_channels["P_ohmic"].append(fracs["P_ohmic"])
            dead_channels["P_line"].append(fracs["P_line"])

            if n == 2.0:  # print representative slice
                ign = "YES" if pb["ignited"] else "no"
                print(f"  {T:4d} {n:4.1f} | "
                      f"{fracs['P_alpha']:6.2f}% {fracs['P_brem']:6.2f}% "
                      f"{fracs['P_cyc']:6.2f}% {fracs['P_line']:6.2f}% "
                      f"{fracs['P_cond']:6.2f}% {fracs['P_ohmic']:6.4f}% | {ign}")

    print(f"\n  Channel ranges across full window:")
    for ch in ALL_CH:
        mn = min(all_fracs[ch])
        mx = max(all_fracs[ch])
        print(f"    {NAMES[ch]:6s}: {mn:7.4f}% - {mx:7.2f}%")

    ohmic_max = max(dead_channels["P_ohmic"])
    line_max = max(dead_channels["P_line"])
    print(f"\n  P_ohmic max fraction: {ohmic_max:.4f}% -> {'DEAD' if ohmic_max < 0.1 else 'ALIVE'}")
    print(f"  P_line  max fraction: {line_max:.4f}%  -> {'DEAD' if line_max < 1.0 else 'ALIVE'}")

    n_dead = sum(1 for x in [ohmic_max, line_max] if x < 1.0)
    active = 6 - n_dead
    simplex_dim = active - 1
    print(f"\n  Active channels: {active}")
    print(f"  Simplex dimension: {simplex_dim}")
    print(f"  Control parameters (T, n) at fixed (B, Zeff): 2")
    print(f"  -> Composition lives on a 2D surface within the {simplex_dim}-simplex")

    return {
        "active_channels": active,
        "dead_channels": ["P_ohmic"] + (["P_line"] if line_max < 1.0 else []),
        "simplex_dim": simplex_dim,
        "control_params": 2,
        "ohmic_max_pct": round(ohmic_max, 6),
        "line_max_pct": round(line_max, 4),
    }


# ============================================================
#  ANALYSIS 2: CLR PRINCIPAL COMPONENT ANALYSIS
# ============================================================

def clr_pca():
    """
    PCA on CLR-transformed compositions in burning plasma window.
    How many components explain >99% of variance?
    """
    print(f"\n{'='*70}")
    print("  ANALYSIS 2: CLR PRINCIPAL COMPONENT ANALYSIS")
    print("="*70)

    # Dense grid in burning plasma window
    temps = [15+i*0.5 for i in range(71)]   # 15-50 keV
    densities = [1.0+i*0.05 for i in range(41)]  # 1.0-3.0

    clr_data = []
    meta = []
    for T in temps:
        for n in densities:
            pb = power_balance(T, n)
            comp = pb_to_comp(pb)
            clr_data.append(clr(comp))
            meta.append({"T": T, "n": n, "ignited": pb["ignited"]})

    N = len(clr_data)
    D = len(clr_data[0])
    print(f"  Grid: {len(temps)} x {len(densities)} = {N} points, D={D}")

    # Compute mean
    mean = [sum(clr_data[i][j] for i in range(N))/N for j in range(D)]

    # Center
    centered = [[clr_data[i][j]-mean[j] for j in range(D)] for i in range(N)]

    # Covariance matrix (D x D)
    cov = [[0.0]*D for _ in range(D)]
    for i in range(D):
        for j in range(D):
            cov[i][j] = sum(centered[k][i]*centered[k][j] for k in range(N)) / (N-1)

    # Power iteration for eigenvalues (we need all D=6)
    # Use Jacobi eigenvalue algorithm for symmetric matrix
    eigenvalues = jacobi_eigenvalues(cov, D)
    eigenvalues.sort(reverse=True)

    total_var = sum(eigenvalues)
    cum_var = 0
    print(f"\n  Eigenvalues of CLR covariance matrix:")
    dof_99 = D
    dof_95 = D
    for i, ev in enumerate(eigenvalues):
        cum_var += ev
        frac = ev/total_var*100 if total_var > 0 else 0
        cum_pct = cum_var/total_var*100 if total_var > 0 else 0
        print(f"    PC{i+1}: eigenvalue={ev:.6f}  "
              f"variance={frac:.2f}%  cumulative={cum_pct:.2f}%")
        if cum_pct >= 99.0 and dof_99 == D:
            dof_99 = i + 1
        if cum_pct >= 95.0 and dof_95 == D:
            dof_95 = i + 1

    print(f"\n  Components for 95% variance: {dof_95}")
    print(f"  Components for 99% variance: {dof_99}")
    print(f"  EFFECTIVE DOF = {dof_99}")

    if dof_99 <= 2:
        print(f"\n  *** DOF = {dof_99} ***")
        print(f"  The burning plasma composition is a 2D surface.")
        print(f"  Two control knobs (T, n) fully determine the state.")
        print(f"  THIS IS CONTROLLABLE.")

    return {
        "N": N, "D": D,
        "eigenvalues": [round(e, 6) for e in eigenvalues],
        "variance_explained": [round(e/total_var*100, 2) for e in eigenvalues],
        "dof_95": dof_95,
        "dof_99": dof_99,
        "controllable": dof_99 <= 2,
    }


def jacobi_eigenvalues(A, n, max_iter=200):
    """Jacobi eigenvalue algorithm for symmetric matrix."""
    # Copy matrix
    M = [row[:] for row in A]

    for _ in range(max_iter):
        # Find largest off-diagonal element
        max_val = 0
        p, q = 0, 1
        for i in range(n):
            for j in range(i+1, n):
                if abs(M[i][j]) > max_val:
                    max_val = abs(M[i][j])
                    p, q = i, j

        if max_val < 1e-12:
            break

        # Compute rotation angle
        if abs(M[p][p] - M[q][q]) < 1e-15:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan2(2*M[p][q], M[p][p]-M[q][q])

        c = math.cos(theta)
        s = math.sin(theta)

        # Apply Jacobi rotation
        new_M = [row[:] for row in M]

        for i in range(n):
            if i != p and i != q:
                new_M[i][p] = c*M[i][p] + s*M[i][q]
                new_M[p][i] = new_M[i][p]
                new_M[i][q] = -s*M[i][p] + c*M[i][q]
                new_M[q][i] = new_M[i][q]

        new_M[p][p] = c**2*M[p][p] + 2*s*c*M[p][q] + s**2*M[q][q]
        new_M[q][q] = s**2*M[p][p] - 2*s*c*M[p][q] + c**2*M[q][q]
        new_M[p][q] = 0
        new_M[q][p] = 0

        M = new_M

    return [M[i][i] for i in range(n)]


# ============================================================
#  ANALYSIS 3: SOLVE TO 2 DOF — THE CONTROL SURFACE
# ============================================================

def control_surface():
    """
    Map the full (T, n) control surface at fixed B=5.3, Zeff=1.5.
    At each point compute:
      - Active composition (4 channels: Alpha, Brem, Cyclo, Cond)
      - Ignition status
      - Q factor
      - PLL sigma^2_A (local neighbourhood)
      - Boundary species
    """
    print(f"\n{'='*70}")
    print("  ANALYSIS 3: THE 2-DOF CONTROL SURFACE")
    print("  (T, n) plane at B=5.3T, Zeff=1.5")
    print("="*70)

    ACTIVE = ["P_alpha", "P_brem", "P_cyc", "P_cond"]
    ACT_NAMES = {"P_alpha":"Alpha","P_brem":"Brem","P_cyc":"Cyclo","P_cond":"Cond"}

    # Dense grid
    T_vals = [15.0 + i*0.25 for i in range(141)]   # 15-50
    n_vals = [1.0 + i*0.02 for i in range(101)]     # 1.0-3.0

    grid = []
    ignition_boundary = []  # (T, n) pairs on the boundary

    for ni, n in enumerate(n_vals):
        prev_ign = False
        for ti, T in enumerate(T_vals):
            pb = power_balance(T, n)

            # Active composition (4 channels, closed)
            raw = [max(pb[ch], 1e-30) for ch in ACTIVE]
            s = sum(raw)
            comp4 = [r/s for r in raw]

            # CLR of 4-channel composition
            clr4 = clr(comp4)

            # Boundary species (instantaneous)
            max_j = max(range(4), key=lambda j: abs(clr4[j]))
            bs = ACTIVE[max_j]

            point = {
                "T": T, "n": n,
                "comp": {ACTIVE[j]: round(comp4[j], 6) for j in range(4)},
                "clr": {ACTIVE[j]: round(clr4[j], 4) for j in range(4)},
                "ignited": pb["ignited"],
                "Q": min(pb["Q"], 1e8),
                "margin": pb["margin"],
                "bs": bs,
            }
            grid.append(point)

            # Track ignition boundary
            if pb["ignited"] and not prev_ign:
                ignition_boundary.append({"T": T, "n": n})
            if not pb["ignited"] and prev_ign:
                ignition_boundary.append({"T": T, "n": n, "exit": True})
            prev_ign = pb["ignited"]

    total = len(grid)
    n_ign = sum(1 for g in grid if g["ignited"])
    print(f"  Grid: {len(T_vals)} x {len(n_vals)} = {total} points")
    print(f"  Ignited: {n_ign} ({100*n_ign/total:.1f}%)")

    # Boundary species map
    bs_count = {}
    for g in grid:
        bs_count[g["bs"]] = bs_count.get(g["bs"], 0) + 1
    print(f"\n  Boundary species distribution across control surface:")
    for bs, cnt in sorted(bs_count.items(), key=lambda x: -x[1]):
        print(f"    {ACT_NAMES.get(bs, bs):6s}: {cnt:5d} ({100*cnt/total:.1f}%)")

    # Ignition boundary curve
    entry_pts = [p for p in ignition_boundary if "exit" not in p]
    exit_pts = [p for p in ignition_boundary if "exit" in p]
    print(f"\n  Ignition boundary: {len(entry_pts)} entry points, {len(exit_pts)} exit points")

    if entry_pts:
        min_T = min(p["T"] for p in entry_pts)
        max_T = max(p["T"] for p in entry_pts)
        min_n = min(p["n"] for p in entry_pts)
        max_n = max(p["n"] for p in entry_pts)
        print(f"  Entry T range: {min_T:.1f} - {max_T:.1f} keV")
        print(f"  Entry n range: {min_n:.2f} - {max_n:.2f} x10^20")

    if exit_pts:
        min_Te = min(p["T"] for p in exit_pts)
        max_Te = max(p["T"] for p in exit_pts)
        print(f"  Exit  T range: {min_Te:.1f} - {max_Te:.1f} keV")

    # Print ignition window at select densities
    print(f"\n  Ignition windows (T range at each n):")
    for n_show in [1.2, 1.5, 1.8, 2.0, 2.2, 2.5, 3.0]:
        n_pts = [g for g in grid if abs(g["n"]-n_show) < 0.015 and g["ignited"]]
        if n_pts:
            t_min = min(g["T"] for g in n_pts)
            t_max = max(g["T"] for g in n_pts)
            width = t_max - t_min
            print(f"    n={n_show:.1f}: T = {t_min:.1f} - {t_max:.1f} keV  "
                  f"(width {width:.1f} keV)")
        else:
            print(f"    n={n_show:.1f}: NO IGNITION")

    # PLL along T at fixed n (local sigma^2_A)
    print(f"\n  PLL sigma^2_A profiles along T at fixed n:")
    for n_show in [1.5, 2.0, 2.5]:
        n_pts = [(g["T"], g["comp"]) for g in grid if abs(g["n"]-n_show)<0.015]
        if len(n_pts) < 20:
            continue
        clr_vecs = [clr([c[ch] for ch in ACTIVE]) for _, c in n_pts]
        T_list = [p[0] for p in n_pts]

        # Sliding window sigma^2_A
        w = 10
        sig_curve = []
        t_curve = []
        for i in range(w, len(clr_vecs)-w):
            window = clr_vecs[i-w:i+w+1]
            n_w = len(window)
            D4 = 4
            vs = 0
            for j in range(D4):
                col = [v[j] for v in window]
                mu = sum(col)/n_w
                vs += sum((c-mu)**2 for c in col)/(n_w-1)
            sig_curve.append(vs/D4)
            t_curve.append(T_list[i])

        if len(t_curve) < 5:
            continue

        # Parabola fit
        n_p = len(t_curve)
        Sx=sum(t_curve); Sy=sum(sig_curve)
        Sx2=sum(t**2 for t in t_curve); Sx3=sum(t**3 for t in t_curve)
        Sx4=sum(t**4 for t in t_curve)
        Sxy=sum(t*s for t,s in zip(t_curve,sig_curve))
        Sx2y=sum(t**2*s for t,s in zip(t_curve,sig_curve))
        M=[[n_p,Sx,Sx2],[Sx,Sx2,Sx3],[Sx2,Sx3,Sx4]]
        v=[Sy,Sxy,Sx2y]
        def d3(m):
            return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
                   -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
                   +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
        dd = d3(M)
        if abs(dd) > 1e-30:
            Ma=[[v[i] if j==0 else M[i][j] for j in range(3)] for i in range(3)]
            Mb=[[v[i] if j==1 else M[i][j] for j in range(3)] for i in range(3)]
            Mc=[[v[i] if j==2 else M[i][j] for j in range(3)] for i in range(3)]
            a=d3(Ma)/dd; b=d3(Mb)/dd; c=d3(Mc)/dd
            ym=Sy/n_p
            sst=sum((s-ym)**2 for s in sig_curve)
            ssr=sum((s-(a+b*t+c*t**2))**2 for t,s in zip(t_curve,sig_curve))
            R2=1-ssr/sst if sst>0 else 0
            vtx = -b/(2*c) if abs(c)>1e-15 else 0
            shape = "bowl" if c>0 else "hill"
            print(f"    n={n_show:.1f}: PLL R^2={R2:.4f}  {shape}  "
                  f"vertex T={vtx:.1f} keV")

    # Alpha-Cond ratio analysis
    print(f"\n  Alpha/Cond ratio across ignition window:")
    for g in grid:
        if abs(g["n"]-2.0)<0.015 and g["T"] in [15,18,20,22,25,28,30]:
            ac = g["comp"]["P_alpha"]/g["comp"]["P_cond"] if g["comp"]["P_cond"]>0 else 0
            ign = "IGN" if g["ignited"] else "   "
            print(f"    T={g['T']:4.0f}  Alpha={g['comp']['P_alpha']*100:5.1f}%  "
                  f"Cond={g['comp']['P_cond']*100:5.1f}%  "
                  f"ratio={ac:.3f}  {ign}")

    return {
        "grid_size": total,
        "n_ignited": n_ign,
        "frac_ignited": round(n_ign/total, 4),
        "bs_distribution": {ACT_NAMES.get(k,k): cnt for k, cnt in bs_count.items()},
        "ignition_entry": entry_pts[:20],
        "ignition_exit": exit_pts[:20],
    }


# ============================================================
#  ANALYSIS 4: THE REDUCTION — ALPHA vs COND
# ============================================================

def alpha_cond_reduction():
    """
    Since Alpha+Cond >> Brem+Cyclo in burning plasma,
    test whether the system reduces to a single ratio: Alpha/Cond.
    If so, DOF = 1 for the dominant physics, with Brem+Cyclo as
    a slowly-varying background.
    """
    print(f"\n{'='*70}")
    print("  ANALYSIS 4: ALPHA-COND REDUCTION")
    print("  Does the system reduce to Alpha/Cond + background?")
    print("="*70)

    T_vals = [15.0+i*0.5 for i in range(71)]
    n_vals = [1.0+i*0.05 for i in range(41)]

    ac_ratios = []
    rad_fracs = []  # brem + cyc fraction

    for T in T_vals:
        for n in n_vals:
            pb = power_balance(T, n)
            raw = [max(pb[ch],1e-30) for ch in ["P_alpha","P_brem","P_cyc","P_cond"]]
            s = sum(raw)
            comp = [r/s for r in raw]
            alpha_f = comp[0]
            cond_f = comp[3]
            rad_f = comp[1] + comp[2]  # brem + cyc
            ac_ratios.append(alpha_f/cond_f if cond_f > 1e-10 else 999)
            rad_fracs.append(rad_f)

    rad_mean = sum(rad_fracs)/len(rad_fracs)
    rad_std = math.sqrt(sum((r-rad_mean)**2 for r in rad_fracs)/len(rad_fracs))
    rad_cv = rad_std/rad_mean if rad_mean > 0 else 0

    print(f"  Radiation fraction (Brem+Cyclo):")
    print(f"    Mean:  {rad_mean*100:.2f}%")
    print(f"    Stdev: {rad_std*100:.2f}%")
    print(f"    CV:    {rad_cv:.4f}")

    if rad_cv < 0.5:
        print(f"    -> Radiation is SLOWLY VARYING (CV < 0.5)")
        print(f"    -> Effective 1 DOF: Alpha/Cond ratio determines state")
        print(f"    -> With (T, n) as controls: 2 knobs, 1 effective output")
        print(f"    -> OVER-DETERMINED: we have MORE control than DOF")
        print(f"    -> This means there are MULTIPLE paths to each state")
    else:
        print(f"    -> Radiation varies significantly (CV >= 0.5)")
        print(f"    -> 2 effective DOF needed")

    # Ignition condition in terms of Alpha/Cond
    print(f"\n  Ignition threshold in Alpha/Cond ratio:")
    ign_ratios = []
    for T in T_vals:
        for n in n_vals:
            pb = power_balance(T, n)
            if pb["ignited"]:
                raw = [max(pb[ch],1e-30) for ch in ["P_alpha","P_brem","P_cyc","P_cond"]]
                s = sum(raw)
                ign_ratios.append(raw[0]/raw[3] if raw[3]>0 else 999)

    if ign_ratios:
        min_ratio = min(ign_ratios)
        print(f"    Minimum Alpha/Cond at ignition: {min_ratio:.4f}")
        print(f"    Ignition requires Alpha/Cond > {min_ratio:.3f}")
        print(f"    In composition terms: Alpha > {min_ratio/(1+min_ratio)*100:.1f}% "
              f"of (Alpha+Cond)")
    else:
        print(f"    No ignition points found")

    return {
        "rad_mean_pct": round(rad_mean*100, 2),
        "rad_std_pct": round(rad_std*100, 2),
        "rad_cv": round(rad_cv, 4),
        "slowly_varying": rad_cv < 0.5,
        "min_ignition_ratio": round(min(ign_ratios), 4) if ign_ratios else None,
    }


# ============================================================
#  ANALYSIS 5: FORMAL DOF STATEMENT
# ============================================================

def formal_dof(survey, pca, surface, reduction):
    """Synthesise all analyses into a formal DOF statement."""
    print(f"\n{'='*70}")
    print("  FORMAL DEGREES OF FREEDOM STATEMENT")
    print("="*70)

    print(f"""
  SYSTEM: Tokamak burning plasma energy partition
  REGIME: T = 15-50 keV, n = 1.0-3.0 x10^20 m^-3

  CHANNEL ANALYSIS:
    Total channels:   6  (Alpha, Brem, Cyclo, Line, Cond, Ohmic)
    Dead channels:    {len(survey['dead_channels'])}  ({', '.join(survey['dead_channels'])})
    Active channels:  {survey['active_channels']}
    Simplex dim:      {survey['simplex_dim']}

  PCA ANALYSIS (CLR space):
    PC1 explains:     {pca['variance_explained'][0]:.1f}% of variance
    PC2 explains:     {pca['variance_explained'][1]:.1f}% of variance
    PC1+PC2:          {sum(pca['variance_explained'][:2]):.1f}%
    DOF for 95%:      {pca['dof_95']}
    DOF for 99%:      {pca['dof_99']}

  CONTROL PARAMETERS:
    Free:     T (temperature), n (density)  = 2
    Fixed:    B (magnetic field), Zeff (impurity) = set by machine/control
    -> Control DOF = 2

  REDUCTION:
    Radiation (Brem+Cyclo) CV = {reduction['rad_cv']:.4f}
    -> {'SLOWLY VARYING' if reduction['slowly_varying'] else 'SIGNIFICANT'}
    -> Effective physics DOF: {'1 (Alpha/Cond ratio)' if reduction['slowly_varying'] else '2'}

  VERDICT:
""")

    if pca["dof_99"] <= 2:
        print(f"    *** DEGREES OF FREEDOM = {pca['dof_99']} ***")
        print(f"    *** THE SYSTEM IS CONTROLLABLE ***")
        print(f"")
        print(f"    The burning plasma energy partition has {pca['dof_99']} effective")
        print(f"    compositional degrees of freedom, matched exactly by")
        print(f"    {2} control parameters (T, n).")
        if reduction["slowly_varying"]:
            print(f"")
            print(f"    Moreover: with radiation as a slow background,")
            print(f"    the dominant physics reduces to 1 DOF (Alpha/Cond),")
            print(f"    controlled by 2 knobs -> OVER-DETERMINED.")
            print(f"    Multiple paths exist to each operating point.")
            if reduction["min_ignition_ratio"]:
                print(f"")
                print(f"    IGNITION CONDITION (reduced form):")
                print(f"      Alpha/Cond > {reduction['min_ignition_ratio']:.3f}")
                threshold = reduction["min_ignition_ratio"]/(1+reduction["min_ignition_ratio"])
                print(f"      i.e. Alpha must exceed {threshold*100:.1f}% of (Alpha+Cond)")
    else:
        print(f"    DOF = {pca['dof_99']} (> 2)")
        print(f"    Additional control parameters may be needed.")

    return pca["dof_99"]


# ============================================================
#  MAIN
# ============================================================

def main():
    print("="*70)
    print("  EXP-06D  DEGREES OF FREEDOM — BURNING PLASMA")
    print("  Can we solve to 2 DOF?")
    print("="*70)

    survey = channel_survey()
    pca = clr_pca()
    surface = control_surface()
    reduction = alpha_cond_reduction()
    dof = formal_dof(survey, pca, surface, reduction)

    # Save
    output = {
        "experiment": "EXP-06D",
        "title": "Degrees of Freedom Analysis - Burning Plasma",
        "date": datetime.now().isoformat(),
        "author": "Peter Higgins",
        "computed_by": "Claude (Anthropic)",
        "survey": survey,
        "pca": pca,
        "control_surface": {
            "grid_size": surface["grid_size"],
            "n_ignited": surface["n_ignited"],
            "bs_distribution": surface["bs_distribution"],
        },
        "reduction": reduction,
        "formal_dof": dof,
        "verdict": "CONTROLLABLE" if dof <= 2 else "UNDER-DETERMINED",
    }

    outpath = os.path.join(os.path.dirname(__file__), "exp06d_dof_analysis.json")
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {outpath}")


if __name__ == "__main__":
    main()
