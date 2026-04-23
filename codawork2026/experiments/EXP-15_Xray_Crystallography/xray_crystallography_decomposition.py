#!/usr/bin/env python3
"""
X-Ray Crystallography Higgins Decomposition
=============================================
EXP-15: Dual-anchor test on crystallographic systems

MATTER perspective: Site occupancy compositions (structural attractor)
ENERGY perspective: Scattering power partition (diffraction attractor)

Uses Cromer-Mann coefficients for atomic scattering factors:
  f(s) = Σᵢ aᵢ exp(-bᵢ s²) + c    where s = sin(θ)/λ  (Å⁻¹)

These are the standard ITC (International Tables for Crystallography) values.
Source: International Tables Vol C, Table 6.1.1.4
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from itertools import combinations

# ═══════════════════════════════════════════════════════════════════
# CROMER-MANN ATOMIC SCATTERING FACTORS
# f(s) = a1*exp(-b1*s²) + a2*exp(-b2*s²) + a3*exp(-b3*s²) + a4*exp(-b4*s²) + c
# s = sin(θ)/λ in Å⁻¹
# Source: International Tables for Crystallography, Vol C
# ═══════════════════════════════════════════════════════════════════

CROMER_MANN = {
    # Element: (a1, b1, a2, b2, a3, b3, a4, b4, c)
    'Na': (4.7626, 3.2850, 3.1736, 8.8422, 1.2674, 0.3136, 1.1128, 129.424, 0.676),
    'Cl': (11.4604, 0.0104, 7.1964, 1.1662, 6.2556, 18.5194, 1.6455, 47.7784, -9.5574),
    'O':  (3.0485, 13.2771, 2.2868, 5.7011, 1.5463, 0.3239, 0.8670, 32.9089, 0.2508),
    'Si': (6.2915, 2.4386, 3.0353, 32.3337, 1.9891, 0.6785, 1.5410, 81.6937, 1.1407),
    'Al': (6.4202, 3.0387, 1.9002, 0.7426, 1.5936, 31.5472, 1.9646, 85.0886, 1.1151),
    'Fe': (11.7695, 4.7611, 7.3573, 0.3072, 3.5222, 15.3535, 2.3045, 76.8805, 1.0369),
    'Mg': (5.4204, 2.8275, 2.1735, 79.2611, 1.2269, 0.3808, 2.3073, 7.1937, 0.8584),
    'Ca': (8.6266, 10.4421, 7.3873, 0.6599, 1.5899, 85.7484, 1.0211, 178.437, 1.3751),
    'K':  (8.2186, 12.7949, 7.4398, 0.7748, 1.0519, 213.187, 0.8659, 41.6841, 1.4228),
    'Ti': (9.7595, 7.8508, 7.3558, 0.5000, 1.6991, 35.6338, 1.9021, 116.105, 1.2807),
    'Mn': (11.2819, 5.3409, 7.3573, 0.3432, 3.0193, 17.8674, 2.2441, 83.7543, 1.0896),
    'C':  (2.3100, 20.8439, 1.0200, 10.2075, 1.5886, 0.5687, 0.8650, 51.6512, 0.2156),
    'N':  (12.2126, 0.0057, 3.1322, 9.8933, 2.0125, 28.9975, 1.1663, 0.5826, -11.529),
    'H':  (0.4930, 10.5109, 0.3229, 26.1257, 0.1402, 3.1424, 0.0408, 57.7998, 0.0030),
    'P':  (6.4345, 1.9067, 4.1791, 27.1570, 1.7800, 0.5260, 1.4908, 68.1645, 1.1149),
    'S':  (6.9053, 1.4679, 5.2034, 22.2151, 1.4379, 0.2536, 1.5863, 56.1720, 0.8669),
    'F':  (3.5392, 10.2825, 2.6412, 4.2944, 1.5170, 0.2615, 1.0243, 26.1476, 0.2776),
}

def scattering_factor(element, s):
    """Compute f(s) for an element at sin(θ)/λ = s"""
    a1, b1, a2, b2, a3, b3, a4, b4, c = CROMER_MANN[element]
    s2 = s**2
    return (a1 * np.exp(-b1 * s2) + a2 * np.exp(-b2 * s2) +
            a3 * np.exp(-b3 * s2) + a4 * np.exp(-b4 * s2) + c)


# ═══════════════════════════════════════════════════════════════════
# TEST CRYSTALS
# ═══════════════════════════════════════════════════════════════════

CRYSTALS = {
    'NaCl': {
        'name': 'Halite (NaCl)',
        'category': 'Simple ionic',
        'elements': ['Na', 'Cl'],
        'stoichiometry': [1, 1],  # atoms per formula unit
        'description': 'Rock salt structure — simplest ionic crystal',
        'domain_matter': 'Geochemistry',
        'domain_energy': 'Diffraction',
    },
    'Olivine_Fo90': {
        'name': 'Olivine Fo90 (Mg₁.₈Fe₀.₂SiO₄)',
        'category': 'Nesosilicate',
        'elements': ['Mg', 'Fe', 'Si', 'O'],
        'stoichiometry': [1.8, 0.2, 1, 4],
        'description': 'Mantle mineral — connects to geochemistry programme',
        'domain_matter': 'Geochemistry',
        'domain_energy': 'Diffraction',
    },
    'Quartz': {
        'name': 'Quartz (SiO₂)',
        'category': 'Tectosilicate',
        'elements': ['Si', 'O'],
        'stoichiometry': [1, 2],
        'description': 'Most common mineral on Earth — framework silicate',
        'domain_matter': 'Geochemistry',
        'domain_energy': 'Diffraction',
    },
    'Garnet_Alm': {
        'name': 'Almandine Garnet (Fe₃Al₂Si₃O₁₂)',
        'category': 'Nesosilicate',
        'elements': ['Fe', 'Al', 'Si', 'O'],
        'stoichiometry': [3, 2, 3, 12],
        'description': 'Complex silicate — 3 distinct crystallographic sites',
        'domain_matter': 'Geochemistry',
        'domain_energy': 'Diffraction',
    },
    'Calcite': {
        'name': 'Calcite (CaCO₃)',
        'category': 'Carbonate',
        'elements': ['Ca', 'C', 'O'],
        'stoichiometry': [1, 1, 3],
        'description': 'Carbonate mineral — connects to geochemistry (CaO)',
        'domain_matter': 'Geochemistry',
        'domain_energy': 'Diffraction',
    },
    'Perovskite': {
        'name': 'Perovskite (CaTiO₃)',
        'category': 'Oxide',
        'elements': ['Ca', 'Ti', 'O'],
        'stoichiometry': [1, 1, 3],
        'description': 'Lower mantle mineral — high-pressure phase',
        'domain_matter': 'Geochemistry',
        'domain_energy': 'Diffraction',
    },
}


# ═══════════════════════════════════════════════════════════════════
# CoDa TOOLKIT (from the programme)
# ═══════════════════════════════════════════════════════════════════

def closure(x):
    """Simplex closure"""
    x = np.maximum(x, 1e-15)
    return x / x.sum(axis=-1, keepdims=True)

def clr(X):
    """Centered log-ratio transform"""
    logX = np.log(np.maximum(X, 1e-15))
    return logX - logX.mean(axis=-1, keepdims=True)

def sigma2_A(X):
    """Aitchison variance for each row"""
    c = clr(X)
    return np.sum(c**2, axis=-1) / X.shape[-1]

def shannon_H(X):
    """Shannon entropy"""
    X = np.maximum(X, 1e-15)
    return -np.sum(X * np.log(X), axis=-1)

def aitchison_dist(x, y):
    """Aitchison distance between two compositions"""
    return np.sqrt(np.sum((clr(x) - clr(y))**2))

def pll_fit(driver, response):
    """Fit PLL parabola: response = a*driver² + b*driver + c"""
    if len(driver) < 4:
        return {'R2': 0, 'a': 0, 'b': 0, 'c': 0, 'shape': 'insufficient', 'vertex': 0}
    A = np.column_stack([driver**2, driver, np.ones(len(driver))])
    try:
        coeffs, _, _, _ = np.linalg.lstsq(A, response, rcond=None)
    except:
        return {'R2': 0, 'a': 0, 'b': 0, 'c': 0, 'shape': 'error', 'vertex': 0}
    a, b, c = coeffs
    y_pred = A @ coeffs
    ss_res = np.sum((response - y_pred)**2)
    ss_tot = np.sum((response - response.mean())**2)
    R2 = 1 - ss_res / ss_tot if ss_tot > 1e-20 else 0
    shape = 'bowl' if a > 0 else 'hill'
    vertex = -b / (2 * a) if abs(a) > 1e-15 else 0
    return {'R2': R2, 'a': a, 'b': b, 'c': c, 'shape': shape, 'vertex': vertex}


# ═══════════════════════════════════════════════════════════════════
# SUPER SQUEEZE CONSTANTS
# ═══════════════════════════════════════════════════════════════════

CONSTANTS = {
    '1/√2': 1/np.sqrt(2), '1/√3': 1/np.sqrt(3), '1/√5': 1/np.sqrt(5),
    'ln(2)': np.log(2), '1/e': 1/np.e, '1/π': 1/np.pi, '2/π': 2/np.pi,
    'π/4': np.pi/4, 'e/π': np.e/np.pi, 'φ': (np.sqrt(5)-1)/2,
    'φ²': ((np.sqrt(5)-1)/2)**2, '√2-1': np.sqrt(2)-1, '2-√3': 2-np.sqrt(3),
    'γ_EM': 0.5772, 'G_Cat': 0.9160, 'log₁₀(2)': np.log10(2),
    'log₁₀(e)': np.log10(np.e), 'ln(√2)': np.log(np.sqrt(2)),
    'sin(1)': np.sin(1), 'cos(1)': np.cos(1), '√3/2': np.sqrt(3)/2,
    'φ/√2': (np.sqrt(5)-1)/2/np.sqrt(2), 'e^(-π/4)': np.exp(-np.pi/4),
    '1/4': 0.25, '1/3': 1/3, '1/2': 0.5, '2/3': 2/3, '3/4': 0.75,
}


def super_squeeze(s_values, comp_trajectory, label=""):
    """Run the super squeeze on a compositional trajectory.
    s_values: parameter values (sin(θ)/λ)
    comp_trajectory: (N, D) array of compositions
    Returns list of matches.
    """
    # Compute σ²_A along trajectory
    sA = sigma2_A(comp_trajectory)

    # Normalize both driver and response to [0,1]
    s_min, s_max = s_values.min(), s_values.max()
    s_norm = (s_values - s_min) / (s_max - s_min) if s_max > s_min else np.full_like(s_values, 0.5)

    sA_min, sA_max = sA.min(), sA.max()
    sA_norm = (sA - sA_min) / (sA_max - sA_min) if sA_max > sA_min else np.full_like(sA, 0.5)

    matches = []
    for cn, cv in sorted(CONSTANTS.items(), key=lambda x: x[1]):
        if 0.01 < cv < 0.99:
            # Interpolate σ²_A at this normalized position
            val = float(np.interp(cv, s_norm, sA_norm))
            # Find closest constant
            best = min(CONSTANTS.items(), key=lambda x: abs(val - x[1]) if x[0] != cn else 999)
            delta = abs(val - best[1])
            if delta < 0.02:
                matches.append({
                    'input': cn, 'input_val': cv,
                    'output': best[0], 'output_val': best[1],
                    'actual': val, 'delta': delta,
                })
    return matches


# ═══════════════════════════════════════════════════════════════════
# MAIN ANALYSIS: BUILD COMPOSITIONAL TRAJECTORIES
# ═══════════════════════════════════════════════════════════════════

print("=" * 100)
print("  X-RAY CRYSTALLOGRAPHY HIGGINS DECOMPOSITION")
print("  EXP-15: Dual-Anchor Test on Crystallographic Systems")
print("=" * 100)

# s = sin(θ)/λ range: 0 to 1.2 Å⁻¹ (covers typical diffraction range)
s_range = np.linspace(0.01, 1.2, 200)

results = {}

for crystal_id, crystal in CRYSTALS.items():
    print(f"\n{'─' * 80}")
    print(f"  CRYSTAL: {crystal['name']}")
    print(f"  Type: {crystal['category']} | Elements: {', '.join(crystal['elements'])}")
    print(f"{'─' * 80}")

    elements = crystal['elements']
    stoich = np.array(crystal['stoichiometry'])
    D = len(elements)

    # ── STEP 1: Compute scattering factors across s range ──
    f_values = np.zeros((len(s_range), D))
    for j, elem in enumerate(elements):
        f_values[:, j] = scattering_factor(elem, s_range) * stoich[j]

    # ── STEP 2: Build scattering COMPOSITION (fractional contribution) ──
    # Each element's contribution to total scattering as a fraction
    f_total = f_values.sum(axis=1, keepdims=True)
    comp = closure(np.maximum(f_values, 1e-10))

    # ── STEP 3: CoDa analysis ──
    sA = sigma2_A(comp)
    H = shannon_H(comp)
    N_eff = np.exp(H)
    clr_vals = clr(comp)

    # ── STEP 4: PLL fit (σ²_A vs s as driver) ──
    pll_sa = pll_fit(s_range, sA)

    # Also fit H vs s
    pll_h = pll_fit(s_range, H)

    # Also fit σ²_A vs H
    pll_sa_h = pll_fit(sA, H)

    print(f"\n  ENERGY (Diffraction) perspective:")
    print(f"    PLL(σ²_A vs s):  R²={pll_sa['R2']:.4f}  shape={pll_sa['shape']}  vertex_s={pll_sa['vertex']:.4f}")
    print(f"    PLL(H vs s):     R²={pll_h['R2']:.4f}  shape={pll_h['shape']}  vertex_s={pll_h['vertex']:.4f}")
    print(f"    PLL(σ²_A vs H):  R²={pll_sa_h['R2']:.4f}  shape={pll_sa_h['shape']}")

    # ── STEP 5: Identify anchor compositions ──
    # ENERGY anchor: composition at s=0 (forward scattering, all Z electrons)
    comp_s0 = comp[0]
    # MATTER anchor: composition at s where σ²_A is minimum (structural equilibrium)
    idx_min_sA = np.argmin(sA)
    comp_structural = comp[idx_min_sA]
    s_structural = s_range[idx_min_sA]

    # DIFFRACTION anchor: composition at Bragg-like peak (max σ²_A change)
    grad_sA = np.gradient(sA, s_range)
    idx_max_grad = np.argmax(np.abs(grad_sA))
    comp_bragg = comp[idx_max_grad]
    s_bragg = s_range[idx_max_grad]

    print(f"\n  Anchors:")
    print(f"    Forward scattering (s→0):  [{', '.join(f'{x:.4f}' for x in comp_s0)}]")
    print(f"    Structural (min σ²_A at s={s_structural:.3f}):  [{', '.join(f'{x:.4f}' for x in comp_structural)}]")
    print(f"    Bragg (max |dσ²_A/ds| at s={s_bragg:.3f}):  [{', '.join(f'{x:.4f}' for x in comp_bragg)}]")

    # ── STEP 6: Compute Aitchison distances from anchors ──
    dA_from_s0 = np.array([aitchison_dist(comp[i], comp_s0) for i in range(len(s_range))])
    dA_from_struct = np.array([aitchison_dist(comp[i], comp_structural) for i in range(len(s_range))])

    # PLL on distance-from-anchor
    pll_dA_s0 = pll_fit(s_range, dA_from_s0)
    pll_dA_struct = pll_fit(s_range, dA_from_struct)

    print(f"\n  PLL on Aitchison distance from anchors:")
    print(f"    d_A(x, x_s0) vs s:      R²={pll_dA_s0['R2']:.4f}  shape={pll_dA_s0['shape']}")
    print(f"    d_A(x, x_struct) vs s:   R²={pll_dA_struct['R2']:.4f}  shape={pll_dA_struct['shape']}")

    # ── STEP 7: Super Squeeze ──
    print(f"\n  SUPER SQUEEZE:")
    sq_matches = super_squeeze(s_range, comp, crystal['name'])

    if sq_matches:
        sq_matches.sort(key=lambda x: x['delta'])
        print(f"    Found {len(sq_matches)} matches (δ < 0.02):")
        for m in sq_matches[:8]:
            star = '★' if m['delta'] < 0.005 else '●' if m['delta'] < 0.01 else ' '
            print(f"    {star} S_norm({m['input']}={m['input_val']:.4f}) = {m['actual']:.4f} "
                  f"≈ {m['output']} ({m['output_val']:.4f})  δ={m['delta']:.5f}")
    else:
        print("    No matches found at δ < 0.02")

    # ── STEP 8: Pairwise balance analysis (intermediate rocks method) ──
    if D >= 3:
        print(f"\n  PAIRWISE BALANCE ANALYSIS:")
        pair_results = []
        for i, j in combinations(range(D), 2):
            lr = np.log(comp[:, i] / comp[:, j])
            pll_lr = pll_fit(lr, sA)
            pair_results.append({
                'pair': f'ln({elements[i]}/{elements[j]})',
                'R2': pll_lr['R2'],
                'shape': pll_lr['shape'],
                'vertex': pll_lr['vertex'],
            })
        pair_results.sort(key=lambda x: -x['R2'])
        for p in pair_results[:5]:
            flag = '★' if p['R2'] > 0.5 and p['shape'] == 'bowl' else '●' if p['R2'] > 0.3 else ' '
            print(f"    {flag} {p['pair']:20s}  R²={p['R2']:.4f}  {p['shape']}  vertex={p['vertex']:.3f}")

    # ── Store results ──
    results[crystal_id] = {
        'name': crystal['name'],
        'elements': elements,
        'D': D,
        'N': len(s_range),
        'pll_sA_vs_s': {'R2': pll_sa['R2'], 'shape': pll_sa['shape'], 'vertex': pll_sa['vertex']},
        'pll_H_vs_s': {'R2': pll_h['R2'], 'shape': pll_h['shape'], 'vertex': pll_h['vertex']},
        'pll_sA_vs_H': {'R2': pll_sa_h['R2'], 'shape': pll_sa_h['shape']},
        'pll_dA_forward': {'R2': pll_dA_s0['R2'], 'shape': pll_dA_s0['shape']},
        'pll_dA_structural': {'R2': pll_dA_struct['R2'], 'shape': pll_dA_struct['shape']},
        'squeeze_matches': len(sq_matches) if sq_matches else 0,
        'best_match': sq_matches[0] if sq_matches else None,
        'composition_range': {
            'sA_min': float(sA.min()), 'sA_max': float(sA.max()),
            'H_min': float(H.min()), 'H_max': float(H.max()),
        },
    }


# ═══════════════════════════════════════════════════════════════════
# VISUALIZATION
# ═══════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(24, 20))
fig.suptitle('EXP-15: X-Ray Crystallography Higgins Decomposition\n'
             'Dual-Anchor Test — ENERGY (Diffraction) × MATTER (Structural)',
             fontsize=16, fontweight='bold', y=0.98)

crystal_list = list(CRYSTALS.keys())
colors_map = ['#3FB950', '#F0883E', '#8B5CF6', '#F85149', '#028090', '#D29922']

# Panel 1: Scattering compositions for all crystals
ax1 = fig.add_subplot(3, 3, 1)
for idx, cid in enumerate(crystal_list):
    crystal = CRYSTALS[cid]
    elements = crystal['elements']
    stoich = np.array(crystal['stoichiometry'])
    f_vals = np.zeros((len(s_range), len(elements)))
    for j, elem in enumerate(elements):
        f_vals[:, j] = scattering_factor(elem, s_range) * stoich[j]
    comp = closure(np.maximum(f_vals, 1e-10))
    # Plot the dominant component's fraction
    dominant = np.argmax(comp[0])
    ax1.plot(s_range, comp[:, dominant], color=colors_map[idx], linewidth=2,
             label=f'{cid}: {elements[dominant]}')
ax1.set_xlabel('sin(θ)/λ (Å⁻¹)')
ax1.set_ylabel('Dominant component fraction')
ax1.set_title('Scattering Composition\n(dominant element)')
ax1.legend(fontsize=7, loc='best')
ax1.grid(True, alpha=0.3)

# Panel 2: σ²_A trajectories
ax2 = fig.add_subplot(3, 3, 2)
for idx, cid in enumerate(crystal_list):
    crystal = CRYSTALS[cid]
    elements = crystal['elements']
    stoich = np.array(crystal['stoichiometry'])
    f_vals = np.zeros((len(s_range), len(elements)))
    for j, elem in enumerate(elements):
        f_vals[:, j] = scattering_factor(elem, s_range) * stoich[j]
    comp = closure(np.maximum(f_vals, 1e-10))
    sA = sigma2_A(comp)
    ax2.plot(s_range, sA, color=colors_map[idx], linewidth=2, label=cid)
ax2.set_xlabel('sin(θ)/λ (Å⁻¹)')
ax2.set_ylabel('σ²_A')
ax2.set_title('Aitchison Variance\nvs Diffraction Parameter')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# Panel 3: Shannon entropy trajectories
ax3 = fig.add_subplot(3, 3, 3)
for idx, cid in enumerate(crystal_list):
    crystal = CRYSTALS[cid]
    elements = crystal['elements']
    stoich = np.array(crystal['stoichiometry'])
    f_vals = np.zeros((len(s_range), len(elements)))
    for j, elem in enumerate(elements):
        f_vals[:, j] = scattering_factor(elem, s_range) * stoich[j]
    comp = closure(np.maximum(f_vals, 1e-10))
    H = shannon_H(comp)
    ax3.plot(s_range, H, color=colors_map[idx], linewidth=2, label=cid)
ax3.set_xlabel('sin(θ)/λ (Å⁻¹)')
ax3.set_ylabel('H (nats)')
ax3.set_title('Shannon Entropy\nvs Diffraction Parameter')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# Panel 4: PLL parabola for each crystal (σ²_A vs H)
ax4 = fig.add_subplot(3, 3, 4)
for idx, cid in enumerate(crystal_list):
    crystal = CRYSTALS[cid]
    elements = crystal['elements']
    stoich = np.array(crystal['stoichiometry'])
    f_vals = np.zeros((len(s_range), len(elements)))
    for j, elem in enumerate(elements):
        f_vals[:, j] = scattering_factor(elem, s_range) * stoich[j]
    comp = closure(np.maximum(f_vals, 1e-10))
    sA = sigma2_A(comp)
    H = shannon_H(comp)
    r2 = results[cid]['pll_sA_vs_H']['R2']
    shape = results[cid]['pll_sA_vs_H']['shape']
    ax4.scatter(sA, H, c=colors_map[idx], s=8, alpha=0.6,
               label=f'{cid}: R²={r2:.3f} ({shape})')
ax4.set_xlabel('σ²_A')
ax4.set_ylabel('H (nats)')
ax4.set_title('PLL: σ²_A vs H\n(core diagnostic)')
ax4.legend(fontsize=7)
ax4.grid(True, alpha=0.3)

# Panel 5: PLL R² summary bar chart
ax5 = fig.add_subplot(3, 3, 5)
r2_vals = [results[cid]['pll_sA_vs_s']['R2'] for cid in crystal_list]
shapes = [results[cid]['pll_sA_vs_s']['shape'] for cid in crystal_list]
bar_colors = ['#3FB950' if s == 'bowl' else '#F85149' for s in shapes]
bars = ax5.barh(range(len(crystal_list)), r2_vals, color=bar_colors)
ax5.set_yticks(range(len(crystal_list)))
ax5.set_yticklabels([CRYSTALS[cid]['name'][:20] for cid in crystal_list], fontsize=8)
ax5.set_xlabel('PLL R² (green=bowl, red=hill)')
ax5.set_title('PLL R²: σ²_A vs s\n(ENERGY perspective)')
ax5.invert_yaxis()
for i, (v, s) in enumerate(zip(r2_vals, shapes)):
    ax5.text(v + 0.01, i, f'{v:.3f} ({s})', va='center', fontsize=7)

# Panel 6: Olivine detailed composition trajectory
ax6 = fig.add_subplot(3, 3, 6)
crystal = CRYSTALS['Olivine_Fo90']
elements = crystal['elements']
stoich = np.array(crystal['stoichiometry'])
f_vals = np.zeros((len(s_range), len(elements)))
for j, elem in enumerate(elements):
    f_vals[:, j] = scattering_factor(elem, s_range) * stoich[j]
comp_olv = closure(np.maximum(f_vals, 1e-10))
for j, elem in enumerate(elements):
    ax6.plot(s_range, comp_olv[:, j], linewidth=2, label=elem)
ax6.set_xlabel('sin(θ)/λ (Å⁻¹)')
ax6.set_ylabel('Fraction of total scattering')
ax6.set_title('Olivine Fo90\nFull Composition Trajectory')
ax6.legend()
ax6.grid(True, alpha=0.3)

# Panel 7: Garnet detailed composition
ax7 = fig.add_subplot(3, 3, 7)
crystal = CRYSTALS['Garnet_Alm']
elements = crystal['elements']
stoich = np.array(crystal['stoichiometry'])
f_vals = np.zeros((len(s_range), len(elements)))
for j, elem in enumerate(elements):
    f_vals[:, j] = scattering_factor(elem, s_range) * stoich[j]
comp_gar = closure(np.maximum(f_vals, 1e-10))
for j, elem in enumerate(elements):
    ax7.plot(s_range, comp_gar[:, j], linewidth=2, label=elem)
ax7.set_xlabel('sin(θ)/λ (Å⁻¹)')
ax7.set_ylabel('Fraction of total scattering')
ax7.set_title('Almandine Garnet\nFull Composition Trajectory')
ax7.legend()
ax7.grid(True, alpha=0.3)

# Panel 8: Squeeze results summary
ax8 = fig.add_subplot(3, 3, 8)
ax8.axis('off')
text_lines = ["SUPER SQUEEZE RESULTS\n"]
for cid in crystal_list:
    r = results[cid]
    if r['best_match']:
        m = r['best_match']
        text_lines.append(f"{cid}: {r['squeeze_matches']} matches")
        text_lines.append(f"  Best: {m['input']}→{m['output']}  δ={m['delta']:.5f}")
    else:
        text_lines.append(f"{cid}: No matches")
    text_lines.append("")

text_lines.append("\nPLL SUMMARY (σ²_A vs s)")
for cid in crystal_list:
    r = results[cid]
    text_lines.append(f"{cid}: R²={r['pll_sA_vs_s']['R2']:.4f} ({r['pll_sA_vs_s']['shape']})")

ax8.text(0.05, 0.95, '\n'.join(text_lines), transform=ax8.transAxes, fontsize=8,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Panel 9: N_eff trajectories
ax9 = fig.add_subplot(3, 3, 9)
for idx, cid in enumerate(crystal_list):
    crystal = CRYSTALS[cid]
    elements = crystal['elements']
    stoich = np.array(crystal['stoichiometry'])
    f_vals = np.zeros((len(s_range), len(elements)))
    for j, elem in enumerate(elements):
        f_vals[:, j] = scattering_factor(elem, s_range) * stoich[j]
    comp = closure(np.maximum(f_vals, 1e-10))
    H = shannon_H(comp)
    N_eff = np.exp(H)
    ax9.plot(s_range, N_eff, color=colors_map[idx], linewidth=2, label=cid)
ax9.set_xlabel('sin(θ)/λ (Å⁻¹)')
ax9.set_ylabel('N_eff = exp(H)')
ax9.set_title('Effective Diversity\nvs Diffraction Parameter')
ax9.legend(fontsize=8)
ax9.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('xray_crystallography_decomposition.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"\n{'=' * 100}")
print("  Dashboard saved to xray_crystallography_decomposition.png")

# Save results
output = {
    'experiment': 'EXP-15: X-Ray Crystallography Higgins Decomposition',
    'date': '2026-04-21',
    'author': 'Peter Higgins / Claude',
    'method': 'Cromer-Mann scattering factors → compositional trajectory → 10-step Higgins Decomposition',
    's_range': 'sin(θ)/λ = 0.01 to 1.2 Å⁻¹ (200 points)',
    'source': 'International Tables for Crystallography, Vol C, Table 6.1.1.4',
    'crystals': {},
}
for cid, r in results.items():
    r_clean = {}
    for k, v in r.items():
        if k == 'best_match' and v is not None:
            r_clean[k] = {kk: (float(vv) if isinstance(vv, (np.floating, float)) else vv) for kk, vv in v.items()}
        elif isinstance(v, dict):
            r_clean[k] = {kk: (float(vv) if isinstance(vv, (np.floating, float)) else vv) for kk, vv in v.items()}
        else:
            r_clean[k] = v
    output['crystals'][cid] = r_clean

with open('xray_crystallography_decomposition.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)
print("  Results saved to xray_crystallography_decomposition.json")
print("=" * 100)
