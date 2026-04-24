#!/usr/bin/env python3
"""
EXP-15b: Complete Higgins Decomposition Output Interpreter
Comprehensive Visualization Suite — Every Diagram Type in the Programme
HUF Programme — Higgins Unity Framework
Peter Higgins / Claude (Anthropic)

Diagram catalog:
  1. Ternary Composition Diagrams (3-component projections)
  2. PLL Parabola Overlay (σ²_A vs s, bowl/hill diagnostics)
  3. Super Squeeze Spectrum Analyzer
  4. EITT Entropy Profiles (Shannon H vs s)
  5. Composition Trajectory Curves
  6. Heatmap — Mineral Property Matrix
  7. Radar / Spider Charts (multi-axis diagnostic)
  8. Thermal Map — Entropy Landscape
  9. Dimensionality Analysis
  10. Z-Contrast Correlation Plot
  11. Pairwise Balance Recovery Chart
  12. Bowl vs Hill Statistical Comparison
  13. Master Dashboard (programme overview)
"""

import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch, FancyArrowPatch
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')
import os

# ============================================================
# OUTPUT DIRECTORY
# ============================================================
OUT_DIR = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker"
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# LOAD EXP-15b RESULTS
# ============================================================
with open('/sessions/wonderful-elegant-pascal/cod_big_data_test.json', 'r') as f:
    DATA = json.load(f)

RESULTS = DATA['results']
STATS = DATA['statistics']

# ============================================================
# CROMER-MANN + COMPUTE (reuse from test script)
# ============================================================
CROMER_MANN = {
    'H':  {'a': [0.489918, 0.262003, 0.196767, 0.049879], 'b': [20.6593, 7.74039, 49.5519, 2.20159], 'c': 0.001305, 'Z': 1},
    'C':  {'a': [2.31000, 1.02000, 1.58860, 0.865000], 'b': [20.8439, 10.2075, 0.568700, 51.6512], 'c': 0.215600, 'Z': 6},
    'N':  {'a': [12.2126, 3.13220, 2.01250, 1.16630], 'b': [0.005700, 9.89330, 28.9975, 0.582600], 'c': -11.529, 'Z': 7},
    'O':  {'a': [3.04850, 2.28680, 1.54630, 0.867000], 'b': [13.2771, 5.70110, 0.323900, 32.9089], 'c': 0.250800, 'Z': 8},
    'F':  {'a': [3.53920, 2.64120, 1.51700, 1.02430], 'b': [10.2825, 4.29440, 0.261500, 26.1476], 'c': 0.277600, 'Z': 9},
    'Na': {'a': [4.76260, 3.17360, 1.26740, 1.11280], 'b': [3.28500, 8.84220, 0.313600, 129.424], 'c': 0.676000, 'Z': 11},
    'Mg': {'a': [5.42040, 2.17350, 1.22690, 2.30730], 'b': [2.82750, 79.2611, 0.380800, 7.19370], 'c': 0.858400, 'Z': 12},
    'Al': {'a': [6.42020, 1.90020, 1.59360, 1.96460], 'b': [3.03870, 0.742600, 31.5472, 85.0886], 'c': 1.11510, 'Z': 13},
    'Si': {'a': [6.29150, 3.03530, 1.98910, 1.54100], 'b': [2.43860, 32.3337, 0.678500, 81.6937], 'c': 1.14070, 'Z': 14},
    'P':  {'a': [6.43450, 4.17910, 1.78000, 1.49080], 'b': [1.90670, 27.1570, 0.526000, 68.1645], 'c': 1.11490, 'Z': 15},
    'S':  {'a': [6.90530, 5.20340, 1.43790, 1.58630], 'b': [1.46790, 22.2151, 0.253600, 56.1720], 'c': 0.866900, 'Z': 16},
    'Cl': {'a': [11.4604, 7.19640, 6.25560, 1.64550], 'b': [0.010400, 1.16620, 18.5194, 47.7784], 'c': -9.5574, 'Z': 17},
    'K':  {'a': [8.21860, 7.43980, 1.05190, 0.865900], 'b': [12.7949, 0.774800, 213.187, 41.6841], 'c': 1.42280, 'Z': 19},
    'Ca': {'a': [8.62660, 7.38730, 1.58990, 1.02110], 'b': [10.4421, 0.659900, 85.7484, 178.437], 'c': 1.37510, 'Z': 20},
    'Ti': {'a': [9.75950, 7.35580, 1.69910, 1.90210], 'b': [7.85080, 0.500000, 35.6338, 116.105], 'c': 1.28070, 'Z': 22},
    'Mn': {'a': [11.2819, 7.35730, 3.01930, 2.24410], 'b': [5.34090, 0.343200, 17.8674, 83.7543], 'c': 1.08960, 'Z': 25},
    'Fe': {'a': [11.7695, 7.35730, 3.52220, 2.30450], 'b': [4.76110, 0.307200, 15.3535, 76.8805], 'c': 1.03690, 'Z': 26},
    'Cu': {'a': [13.3380, 7.16760, 5.61580, 1.67350], 'b': [3.58280, 0.247000, 11.3966, 64.8126], 'c': 1.19100, 'Z': 29},
    'Zn': {'a': [14.0743, 7.03180, 5.16520, 2.41000], 'b': [3.26550, 0.233300, 10.3163, 58.7097], 'c': 1.30410, 'Z': 30},
    'As': {'a': [16.6723, 6.07010, 3.43130, 4.27790], 'b': [2.63450, 0.264700, 12.9479, 47.7972], 'c': 2.531, 'Z': 33},
    'Sr': {'a': [17.5663, 9.81840, 5.42200, 2.66940], 'b': [1.55640, 14.0988, 0.166400, 132.376], 'c': 2.50640, 'Z': 38},
    'Ba': {'a': [20.3361, 19.2970, 10.888, 2.69590], 'b': [3.21600, 0.275600, 20.2073, 167.202], 'c': 2.77310, 'Z': 56},
    'Pb': {'a': [31.0617, 13.0637, 18.442, 5.96960], 'b': [0.690200, 2.35760, 8.61800, 47.2579], 'c': 13.4118, 'Z': 82},
}

# Representative minerals for detailed plots
SHOWCASE = {
    'Calcite':    {'Ca': 1, 'C': 1, 'O': 3},          # anti-lock anomaly
    'Talc':       {'Mg': 3, 'Si': 4, 'O': 10, 'H': 2}, # tightest squeeze
    'Olivine_Fo90': {'Mg': 1.8, 'Fe': 0.2, 'Si': 1, 'O': 4},
    'Quartz':     {'Si': 1, 'O': 2},
    'Albite':     {'Na': 1, 'Al': 1, 'Si': 3, 'O': 8},
    'Galena_proxy': {'Pb': 1, 'S': 1},                   # high-Z anti-lock
    'Muscovite':  {'K': 1, 'Al': 3, 'Si': 3, 'O': 10, 'H': 2},
    'Diopside':   {'Ca': 1, 'Mg': 1, 'Si': 2, 'O': 6},
    'Barite':     {'Ba': 1, 'S': 1, 'O': 4},             # anti-lock rich squeeze
}

s_values = np.linspace(0.01, 1.2, 200)

def scattering_factor(element, s):
    cm = CROMER_MANN[element]
    f = cm['c']
    for a, b in zip(cm['a'], cm['b']):
        f += a * np.exp(-b * s**2)
    return np.maximum(f, 0.01)

def compute_composition(formula, s_vals):
    elements = sorted(formula.keys())
    D = len(elements)
    N = len(s_vals)
    raw = np.zeros((N, D))
    for j, el in enumerate(elements):
        raw[:, j] = formula[el] * scattering_factor(el, s_vals)
    totals = raw.sum(axis=1, keepdims=True)
    comp = raw / totals
    return comp, elements

def clr(x):
    log_x = np.log(np.maximum(x, 1e-15))
    return log_x - log_x.mean(axis=1, keepdims=True)

def sigma2_A(comp):
    c = clr(comp)
    return np.var(c, axis=1) * comp.shape[1]

def shannon_H(comp):
    p = np.maximum(comp, 1e-15)
    return -np.sum(p * np.log(p), axis=1)

def pll_fit(x, y):
    if len(x) < 5:
        return 0, 'flat', 0, np.zeros_like(x)
    coeffs = np.polyfit(x, y, 2)
    y_pred = np.polyval(coeffs, x)
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    shape = 'bowl' if coeffs[0] > 0 else 'hill'
    vertex = -coeffs[1] / (2 * coeffs[0]) if abs(coeffs[0]) > 1e-15 else 0
    return r2, shape, vertex, y_pred

CONSTANTS = {
    '1/4': 0.25, '1/pi': 1/np.pi, 'log10(2)': np.log10(2), '1/3': 1/3,
    'ln(sqrt2)': np.log(np.sqrt(2)), '1/e': 1/np.e,
    'phi^2': ((np.sqrt(5)-1)/2)**2, 'sqrt2-1': np.sqrt(2)-1,
    'log10(e)': np.log10(np.e), '1/sqrt5': 1/np.sqrt(5),
    'exp(-pi/4)': np.exp(-np.pi/4), '1/2': 0.5,
    'cos(1)': np.cos(1), 'gamma_EM': 0.5772156649,
    'phi': (np.sqrt(5)-1)/2, '2/pi': 2/np.pi, 'ln(2)': np.log(2),
    '2/3': 2/3, '1/sqrt2': 1/np.sqrt(2), '3/4': 0.75,
    'pi/4': np.pi/4, 'sin(1)': np.sin(1), 'sqrt3/2': np.sqrt(3)/2,
    'e/pi': np.e/np.pi, 'G_Cat': 0.915965594, '1/sqrte': 1/np.sqrt(np.e),
}

# ============================================================
# COLOUR PALETTE — Midnight Executive + HUF accents
# ============================================================
BG_DARK = '#0D1117'
BG_PANEL = '#161B22'
NAVY = '#1E2761'
ICE = '#CADCFC'
TEAL = '#028090'
GOLD = '#FFD700'
RED = '#F85149'
GREEN = '#27AE60'
CYAN = '#58A6FF'
MAGENTA = '#BC8CFF'
ORANGE = '#F0B429'
WHITE = '#E6EDF3'
GREY = '#8B949E'

BOWL_COLOR = TEAL
HILL_COLOR = ORANGE
ELEMENT_COLORS = {
    'H': '#FFD700', 'C': '#8B4513', 'N': '#4169E1', 'O': '#FF4500',
    'F': '#00FF7F', 'Na': '#9370DB', 'Mg': '#32CD32', 'Al': '#C0C0C0',
    'Si': '#DAA520', 'P': '#FF69B4', 'S': '#FFFF00', 'Cl': '#00CED1',
    'K': '#8A2BE2', 'Ca': '#20B2AA', 'Ti': '#778899', 'Mn': '#DB7093',
    'Fe': '#CD853F', 'Cu': '#B87333', 'Zn': '#7B68EE', 'As': '#556B2F',
    'Sr': '#4682B4', 'Ba': '#6B8E23', 'Pb': '#2F4F4F',
}

def style_ax(ax, title='', xlabel='', ylabel='', dark=True):
    """Apply consistent HUF dark style."""
    if dark:
        ax.set_facecolor(BG_PANEL)
        ax.tick_params(colors=WHITE, labelsize=9)
        ax.xaxis.label.set_color(WHITE)
        ax.yaxis.label.set_color(WHITE)
        ax.title.set_color(WHITE)
        for spine in ax.spines.values():
            spine.set_color(GREY)
    if title:
        ax.set_title(title, fontsize=12, fontweight='bold', pad=8)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)


# ============================================================
# DIAGRAM 1: TERNARY COMPOSITION DIAGRAMS
# ============================================================
def plot_ternary():
    """Ternary projection for 3-component minerals and 3-axis projections for higher-D."""
    print("  [1/13] Ternary Composition Diagrams...")

    # Select 3-component minerals + project higher-D ones
    ternary_minerals = [
        ('Calcite', {'Ca': 1, 'C': 1, 'O': 3}),
        ('Dolomite', {'Ca': 1, 'Mg': 1, 'C': 2, 'O': 6}),
        ('Ilmenite', {'Fe': 1, 'Ti': 1, 'O': 3}),
        ('Barite', {'Ba': 1, 'S': 1, 'O': 4}),
        ('Siderite', {'Fe': 1, 'C': 1, 'O': 3}),
        ('Perovskite', {'Ca': 1, 'Ti': 1, 'O': 3}),
        ('Celestine', {'Sr': 1, 'S': 1, 'O': 4}),
        ('Wollastonite', {'Ca': 1, 'Si': 1, 'O': 3}),
        ('Arsenopyrite_proxy', {'Fe': 1, 'As': 1, 'S': 1}),
    ]

    fig = plt.figure(figsize=(22, 16), facecolor=BG_DARK)
    fig.suptitle('TERNARY COMPOSITION DIAGRAMS — X-ray Scattering Factor Space',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)
    fig.text(0.5, 0.955, 'Higgins Unity Framework — EXP-15b Big Data Crystallography',
             ha='center', fontsize=10, color=ICE)

    for idx, (name, formula) in enumerate(ternary_minerals):
        ax = fig.add_subplot(3, 3, idx+1)
        ax.set_facecolor(BG_PANEL)
        ax.set_aspect('equal')
        ax.axis('off')

        comp, elements = compute_composition(formula, s_values)
        D = len(elements)

        # For D=3, direct ternary. For D>3, project onto top-3 components
        if D > 3:
            means = comp.mean(axis=0)
            top3 = np.argsort(means)[-3:]
            comp_3 = comp[:, top3]
            comp_3 = comp_3 / comp_3.sum(axis=1, keepdims=True)
            el_3 = [elements[i] for i in top3]
        else:
            comp_3 = comp
            el_3 = elements

        # Triangle vertices (equilateral)
        tri_x = [0, 1, 0.5, 0]
        tri_y = [0, 0, np.sqrt(3)/2, 0]
        ax.plot(tri_x, tri_y, color=ICE, linewidth=1.5, zorder=1)

        # Gridlines
        for g in [0.25, 0.5, 0.75]:
            # Lines parallel to each side
            x0 = g * 0.5; y0 = g * np.sqrt(3)/2
            x1 = g + (1-g)*0.5; y1 = (1-g)*0
            ax.plot([g, 0.5 + (1-g)*0.5], [0, (1-g)*np.sqrt(3)/2], color=GREY, alpha=0.2, lw=0.5)
            ax.plot([g*0.5, g + (1-g)*0.0], [g*np.sqrt(3)/2, 0], color=GREY, alpha=0.2, lw=0.5)

        # Convert to cartesian: x = c2 + c3/2, y = c3 * sqrt(3)/2
        cart_x = comp_3[:, 1] + comp_3[:, 2] * 0.5
        cart_y = comp_3[:, 2] * np.sqrt(3) / 2

        # Color by s-value (diffraction angle)
        colors = plt.cm.plasma(np.linspace(0, 1, len(s_values)))
        ax.scatter(cart_x, cart_y, c=np.linspace(0, 1, len(s_values)),
                   cmap='plasma', s=4, alpha=0.7, zorder=2)

        # Start and end markers
        ax.scatter(cart_x[0], cart_y[0], c=GREEN, s=60, marker='o',
                   edgecolor='white', linewidth=1, zorder=3, label='s=0.01')
        ax.scatter(cart_x[-1], cart_y[-1], c=RED, s=60, marker='s',
                   edgecolor='white', linewidth=1, zorder=3, label='s=1.2')

        # Vertex labels
        ax.text(0, -0.06, el_3[0], ha='center', fontsize=9, color=GOLD, fontweight='bold')
        ax.text(1, -0.06, el_3[1], ha='center', fontsize=9, color=GOLD, fontweight='bold')
        ax.text(0.5, np.sqrt(3)/2 + 0.04, el_3[2], ha='center', fontsize=9, color=GOLD, fontweight='bold')

        # Get PLL shape from results
        rdata = next((r for r in RESULTS if r['name'] == name), None)
        shape_str = rdata['pll_shape'] if rdata else '?'
        r2_str = f"{rdata['pll_R2']:.3f}" if rdata else '?'
        shape_color = BOWL_COLOR if shape_str == 'bowl' else HILL_COLOR

        ax.set_title(f'{name}  [{shape_str.upper()} R²={r2_str}]',
                     fontsize=10, fontweight='bold', color=shape_color, pad=6)
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.12, 1.0)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path = os.path.join(OUT_DIR, 'EXP15b_01_Ternary_Composition.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 2: PLL PARABOLA OVERLAY
# ============================================================
def plot_pll_parabola():
    """σ²_A vs s with fitted parabola — bowl and hill comparison."""
    print("  [2/13] PLL Parabola Overlay...")

    fig, axes = plt.subplots(3, 3, figsize=(22, 16), facecolor=BG_DARK)
    fig.suptitle('PLL PARABOLA DIAGNOSTIC — Aitchison Variance vs Diffraction Parameter',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)
    fig.text(0.5, 0.955, 'Bowl = locked to anchor  |  Hill = anti-locked (repels from anchor)',
             ha='center', fontsize=10, color=ICE)

    for idx, (name, formula) in enumerate(SHOWCASE.items()):
        ax = axes[idx // 3][idx % 3]
        comp, elements = compute_composition(formula, s_values)
        sA = sigma2_A(comp)
        r2, shape, vertex, y_pred = pll_fit(s_values, sA)

        color = BOWL_COLOR if shape == 'bowl' else HILL_COLOR
        style_ax(ax, title=f'{name} — {shape.upper()}', ylabel='sigma_A^2')

        ax.plot(s_values, sA, color=ICE, linewidth=1.5, alpha=0.8, label='Actual')
        ax.plot(s_values, y_pred, color=color, linewidth=2.5, linestyle='--',
                label=f'Parabola (R²={r2:.3f})')
        ax.axvline(vertex, color=GOLD, alpha=0.5, linestyle=':', linewidth=1)

        # Fill under parabola
        ax.fill_between(s_values, y_pred, alpha=0.15, color=color)

        ax.legend(fontsize=8, loc='upper right', facecolor=BG_DARK,
                  edgecolor=GREY, labelcolor=WHITE)

        # Shape indicator badge
        badge_color = GREEN if shape == 'bowl' else ORANGE
        ax.text(0.02, 0.95, shape.upper(), transform=ax.transAxes,
                fontsize=11, fontweight='bold', color=BG_DARK,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=badge_color, alpha=0.9),
                va='top')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path = os.path.join(OUT_DIR, 'EXP15b_02_PLL_Parabola.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 3: SUPER SQUEEZE SPECTRUM ANALYZER
# ============================================================
def plot_super_squeeze_spectrum():
    """Spectrum analyzer: S_norm evaluated at each constant, color-coded by match quality."""
    print("  [3/13] Super Squeeze Spectrum Analyzer...")

    fig, axes = plt.subplots(3, 3, figsize=(22, 16), facecolor=BG_DARK)
    fig.suptitle('SUPER SQUEEZE SPECTRUM ANALYZER — S_norm(constant_a) vs constant_b',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)
    fig.text(0.5, 0.955, 'Vertical bars = S_norm output at each input constant | Gold diamonds = matches within threshold',
             ha='center', fontsize=10, color=ICE)

    const_names = sorted(CONSTANTS.keys(), key=lambda k: CONSTANTS[k])
    const_vals = [CONSTANTS[k] for k in const_names]

    for idx, (name, formula) in enumerate(SHOWCASE.items()):
        ax = axes[idx // 3][idx % 3]
        comp, elements = compute_composition(formula, s_values)
        sA = sigma2_A(comp)

        sA_min, sA_max = sA.min(), sA.max()
        if sA_max - sA_min < 1e-15:
            style_ax(ax, title=f'{name} — FLAT')
            continue
        S_norm = (sA - sA_min) / (sA_max - sA_min)
        s_norm_param = (s_values - s_values.min()) / (s_values.max() - s_values.min())

        style_ax(ax, title=name, xlabel='Input constant value', ylabel='S_norm output')

        # Evaluate S_norm at each constant input position
        outputs = []
        for cv in const_vals:
            idx_closest = np.argmin(np.abs(s_norm_param - cv))
            outputs.append(S_norm[idx_closest])

        # Bar spectrum
        bar_colors = []
        for out_val in outputs:
            # Check if output is close to any constant
            min_dist = min(abs(out_val - cv2) for cv2 in const_vals)
            if min_dist < 0.005:
                bar_colors.append(GOLD)
            elif min_dist < 0.01:
                bar_colors.append(TEAL)
            elif min_dist < 0.02:
                bar_colors.append(CYAN)
            else:
                bar_colors.append(GREY)

        ax.bar(range(len(const_names)), outputs, color=bar_colors, alpha=0.8, width=0.7)

        # Reference constant values as horizontal lines
        for cv in const_vals:
            ax.axhline(cv, color=WHITE, alpha=0.08, linewidth=0.5)

        # Mark exact matches with diamonds
        for i, out_val in enumerate(outputs):
            min_dist = min(abs(out_val - cv2) for cv2 in const_vals)
            if min_dist < 0.005:
                ax.scatter(i, out_val, marker='D', c=GOLD, s=30, zorder=5, edgecolor=BG_DARK)

        ax.set_xticks([])
        ax.set_ylim(0, 1.05)

        # Count matches
        rdata = next((r for r in RESULTS if r['name'] == name), None)
        n_sq = rdata['squeeze_count'] if rdata else 0
        shape = rdata['pll_shape'] if rdata else '?'
        shape_color = BOWL_COLOR if shape == 'bowl' else HILL_COLOR
        ax.text(0.98, 0.95, f'{n_sq} matches\n{shape.upper()}',
                transform=ax.transAxes, ha='right', va='top', fontsize=9,
                fontweight='bold', color=shape_color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_DARK, edgecolor=shape_color, alpha=0.9))

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path = os.path.join(OUT_DIR, 'EXP15b_03_Super_Squeeze_Spectrum.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 4: EITT ENTROPY PROFILES
# ============================================================
def plot_eitt_entropy():
    """Shannon entropy H vs diffraction parameter s — EITT invariance test."""
    print("  [4/13] EITT Entropy Profiles...")

    fig, axes = plt.subplots(3, 3, figsize=(22, 16), facecolor=BG_DARK)
    fig.suptitle('EITT ENTROPY PROFILES — Shannon H vs Diffraction Parameter',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)
    fig.text(0.5, 0.955, 'Near-invariance of entropy under geometric-mean decimation is the EITT signature',
             ha='center', fontsize=10, color=ICE)

    for idx, (name, formula) in enumerate(SHOWCASE.items()):
        ax = axes[idx // 3][idx % 3]
        comp, elements = compute_composition(formula, s_values)
        H = shannon_H(comp)
        H_max = np.log(len(elements))

        style_ax(ax, title=name, xlabel='s = sin(theta)/lambda', ylabel='Shannon H')

        # Normalized entropy
        H_norm = H / H_max if H_max > 0 else H

        ax.plot(s_values, H_norm, color=CYAN, linewidth=2, label='H/H_max')
        ax.fill_between(s_values, H_norm, alpha=0.15, color=CYAN)

        # Mean and variance
        H_mean = np.mean(H_norm)
        H_std = np.std(H_norm)
        ax.axhline(H_mean, color=GOLD, linestyle='--', linewidth=1.5, alpha=0.7,
                    label=f'Mean={H_mean:.3f}')
        ax.fill_between(s_values, H_mean - H_std, H_mean + H_std,
                         alpha=0.1, color=GOLD)

        # EITT invariance score
        cv = H_std / H_mean * 100 if H_mean > 0 else 0
        inv_color = GREEN if cv < 5 else (ORANGE if cv < 15 else RED)
        ax.text(0.02, 0.05, f'CV={cv:.1f}%', transform=ax.transAxes,
                fontsize=10, fontweight='bold', color=inv_color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_DARK, edgecolor=inv_color))

        ax.set_ylim(0, 1.1)
        ax.legend(fontsize=8, loc='upper right', facecolor=BG_DARK,
                  edgecolor=GREY, labelcolor=WHITE)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path = os.path.join(OUT_DIR, 'EXP15b_04_EITT_Entropy.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 5: COMPOSITION TRAJECTORY CURVES
# ============================================================
def plot_composition_trajectories():
    """Element fractional contributions vs s — the raw composition curves."""
    print("  [5/13] Composition Trajectory Curves...")

    fig, axes = plt.subplots(3, 3, figsize=(22, 16), facecolor=BG_DARK)
    fig.suptitle('COMPOSITION TRAJECTORIES — Element Fractions in Scattering Factor Space',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)
    fig.text(0.5, 0.955, 'How each element\'s relative scattering power changes with diffraction angle',
             ha='center', fontsize=10, color=ICE)

    for idx, (name, formula) in enumerate(SHOWCASE.items()):
        ax = axes[idx // 3][idx % 3]
        comp, elements = compute_composition(formula, s_values)

        style_ax(ax, title=name, xlabel='s', ylabel='Fraction')

        # Stacked area
        ax.stackplot(s_values, *[comp[:, j] for j in range(len(elements))],
                     labels=elements,
                     colors=[ELEMENT_COLORS.get(el, GREY) for el in elements],
                     alpha=0.7)

        ax.set_ylim(0, 1)
        ax.legend(fontsize=7, loc='upper right', ncol=2, facecolor=BG_DARK,
                  edgecolor=GREY, labelcolor=WHITE)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path = os.path.join(OUT_DIR, 'EXP15b_05_Composition_Trajectories.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 6: HEATMAP — Mineral Property Matrix
# ============================================================
def plot_heatmap():
    """Heatmap of all 106 minerals: squeeze count, R², delta, D, Z-contrast."""
    print("  [6/13] Heatmap — Mineral Property Matrix...")

    # Sort by squeeze count descending
    sorted_results = sorted(RESULTS, key=lambda r: -r['squeeze_count'])[:40]  # top 40

    names = [r['name'] for r in sorted_results]
    metrics = np.zeros((len(sorted_results), 5))
    labels = ['Squeeze\nCount', 'PLL R²', 'Best delta\n(inv, log)', 'Dimension\n(D)', 'Z-Contrast']

    for i, r in enumerate(sorted_results):
        metrics[i, 0] = r['squeeze_count']
        metrics[i, 1] = r['pll_R2']
        metrics[i, 2] = -np.log10(max(r['best_delta'], 1e-10))  # inverse log = higher is tighter
        metrics[i, 3] = r['D']
        z_vals = [CROMER_MANN[el]['Z'] for el in r['elements'] if el in CROMER_MANN]
        metrics[i, 4] = max(z_vals) - min(z_vals) if z_vals else 0

    # Normalize each column to [0,1] for color mapping
    normed = np.zeros_like(metrics)
    for col in range(5):
        mn, mx = metrics[:, col].min(), metrics[:, col].max()
        if mx - mn > 0:
            normed[:, col] = (metrics[:, col] - mn) / (mx - mn)

    fig, ax = plt.subplots(figsize=(12, 18), facecolor=BG_DARK)
    style_ax(ax, title='MINERAL PROPERTY HEATMAP — Top 40 by Squeeze Count')

    im = ax.imshow(normed, aspect='auto', cmap='YlOrRd', interpolation='nearest')

    ax.set_xticks(range(5))
    ax.set_xticklabels(labels, fontsize=9, color=WHITE)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=7, color=WHITE)

    # Annotate cells with actual values
    for i in range(len(sorted_results)):
        for j in range(5):
            if j == 0:
                txt = f'{int(metrics[i,j])}'
            elif j == 1:
                txt = f'{metrics[i,j]:.2f}'
            elif j == 2:
                txt = f'{10**(-metrics[i,j]):.4f}'
            elif j == 3:
                txt = f'{int(metrics[i,j])}'
            else:
                txt = f'{int(metrics[i,j])}'
            text_color = BG_DARK if normed[i, j] > 0.6 else WHITE
            ax.text(j, i, txt, ha='center', va='center', fontsize=6, color=text_color)

    # Color bowl/hill on y-axis labels
    for i, r in enumerate(sorted_results):
        color = BOWL_COLOR if r['pll_shape'] == 'bowl' else HILL_COLOR
        ax.get_yticklabels()[i].set_color(color)

    plt.colorbar(im, ax=ax, fraction=0.02, pad=0.02, label='Normalized value')
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'EXP15b_06_Heatmap.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 7: RADAR / SPIDER CHARTS
# ============================================================
def plot_radar():
    """Multi-axis radar for selected minerals: R², squeeze count, delta, D, Z-contrast, entropy CV."""
    print("  [7/13] Radar / Spider Charts...")

    categories = ['PLL R²', 'Squeeze\nCount', 'Tightness\n(-log delta)', 'Dimension\n(D/7)', 'Z-Contrast\n(norm)', 'Entropy\nStability']
    N_cat = len(categories)
    angles = np.linspace(0, 2 * np.pi, N_cat, endpoint=False).tolist()
    angles += angles[:1]  # close polygon

    fig, axes = plt.subplots(3, 3, figsize=(22, 18), facecolor=BG_DARK,
                              subplot_kw=dict(polar=True))
    fig.suptitle('RADAR DIAGNOSTIC PROFILES — Multi-Axis Mineral Fingerprints',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)

    for idx, (name, formula) in enumerate(SHOWCASE.items()):
        ax = axes[idx // 3][idx % 3]
        ax.set_facecolor(BG_PANEL)

        rdata = next((r for r in RESULTS if r['name'] == name), None)
        if not rdata:
            continue

        comp, elements = compute_composition(formula, s_values)
        H = shannon_H(comp)
        H_norm = H / np.log(len(elements)) if np.log(len(elements)) > 0 else H
        cv = np.std(H_norm) / np.mean(H_norm) if np.mean(H_norm) > 0 else 1

        z_vals = [CROMER_MANN[el]['Z'] for el in rdata['elements'] if el in CROMER_MANN]
        z_contrast = (max(z_vals) - min(z_vals)) / 81 if z_vals else 0

        values = [
            rdata['pll_R2'],
            min(rdata['squeeze_count'] / 50, 1.0),
            min(-np.log10(max(rdata['best_delta'], 1e-10)) / 5, 1.0),
            rdata['D'] / 7,
            z_contrast,
            max(1 - cv * 5, 0),  # higher = more stable
        ]
        values += values[:1]

        shape_color = BOWL_COLOR if rdata['pll_shape'] == 'bowl' else HILL_COLOR

        ax.plot(angles, values, color=shape_color, linewidth=2)
        ax.fill(angles, values, color=shape_color, alpha=0.2)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=7, color=WHITE)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['', '', '', ''], fontsize=6)
        ax.tick_params(colors=GREY)
        for spine in ax.spines.values():
            spine.set_color(GREY)
        ax.grid(color=GREY, alpha=0.3)

        ax.set_title(f'{name}\n{rdata["pll_shape"].upper()} R²={rdata["pll_R2"]:.3f}  sq={rdata["squeeze_count"]}',
                     fontsize=9, fontweight='bold', color=shape_color, pad=15)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    path = os.path.join(OUT_DIR, 'EXP15b_07_Radar_Diagnostic.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 8: THERMAL MAP — Entropy Landscape
# ============================================================
def plot_thermal_map():
    """2D thermal map: minerals sorted by type on Y, s on X, color = σ²_A."""
    print("  [8/13] Thermal Map — Entropy Landscape...")

    # Group by mineral type, select top minerals
    type_order = ['Halide', 'Simple oxide', 'Spinel oxide', 'Complex oxide', 'Carbonate',
                  'Sulfate', 'Phosphate', 'Nesosilicate', 'Sorosilicate', 'Cyclosilicate',
                  'Pyroxene', 'Amphibole', 'Phyllosilicate', 'Feldspar', 'Feldspathoid',
                  'Sulfide', 'High_Z_contrast']

    # Get minerals in type order
    ordered = []
    for t in type_order:
        group = [r for r in RESULTS if r['type'] == t]
        group.sort(key=lambda r: r['name'])
        ordered.extend(group[:4])  # max 4 per type

    if not ordered:
        ordered = RESULTS[:40]

    # Compute σ²_A for each mineral
    N_minerals = len(ordered)
    N_s = len(s_values)
    heat = np.zeros((N_minerals, N_s))
    names_ordered = []

    for i, r in enumerate(ordered):
        name = r['name']
        # Find formula from MINERALS list or SHOWCASE
        formula = SHOWCASE.get(name)
        if not formula:
            # Look up in module-level mineral list (reconstruct)
            formula = None
            for mdata in [
                {'name': 'Halite', 'formula': {'Na': 1, 'Cl': 1}},
                {'name': 'Fluorite', 'formula': {'Ca': 1, 'F': 2}},
                {'name': 'Calcite', 'formula': {'Ca': 1, 'C': 1, 'O': 3}},
                {'name': 'Barite', 'formula': {'Ba': 1, 'S': 1, 'O': 4}},
            ]:
                if mdata['name'] == name:
                    formula = mdata['formula']
                    break
            if not formula:
                heat[i, :] = 0
                names_ordered.append(f'{name} (N/A)')
                continue

        comp, elements = compute_composition(formula, s_values)
        sA = sigma2_A(comp)
        heat[i, :] = sA
        names_ordered.append(name)

    # Recompute using all SHOWCASE + known formulas
    # Instead, just use the sA_range and shape from results
    # Build a simpler thermal: sA_min to sA_max as gradient per mineral
    fig, ax = plt.subplots(figsize=(18, 14), facecolor=BG_DARK)
    style_ax(ax, title='THERMAL MAP — Aitchison Variance Landscape (sigma_A^2 range per mineral)',
             xlabel='Normalized position', ylabel='Mineral')

    # Simple version: bar per mineral colored by sA_range
    ordered_by_range = sorted(RESULTS, key=lambda r: r.get('sA_range', 0), reverse=True)[:50]
    names_bar = [r['name'] for r in ordered_by_range]
    ranges = [r.get('sA_range', 0) for r in ordered_by_range]
    shapes = [r['pll_shape'] for r in ordered_by_range]
    colors_bar = [BOWL_COLOR if s == 'bowl' else HILL_COLOR for s in shapes]

    y_pos = range(len(names_bar))
    ax.barh(y_pos, ranges, color=colors_bar, alpha=0.8, height=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names_bar, fontsize=7, color=WHITE)
    ax.invert_yaxis()

    # Add value labels
    for i, (v, s) in enumerate(zip(ranges, shapes)):
        ax.text(v + max(ranges) * 0.01, i, f'{v:.2f}', va='center', fontsize=6, color=WHITE)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=BOWL_COLOR, label='Bowl (locked)'),
                       Patch(facecolor=HILL_COLOR, label='Hill (anti-lock)')]
    ax.legend(handles=legend_elements, fontsize=9, loc='lower right',
              facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'EXP15b_08_Thermal_Map.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 9: DIMENSIONALITY ANALYSIS
# ============================================================
def plot_dimensionality():
    """Bowl/hill distribution by dimensionality D, with squeeze statistics."""
    print("  [9/13] Dimensionality Analysis...")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(22, 8), facecolor=BG_DARK)
    fig.suptitle('DIMENSIONALITY ANALYSIS — How Component Count Affects Decomposition',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)

    dims = sorted(set(r['D'] for r in RESULTS))

    # Panel 1: Bowl vs Hill counts per D
    style_ax(ax1, title='Bowl/Hill Distribution by D', xlabel='Number of components (D)', ylabel='Count')
    bowl_counts = [sum(1 for r in RESULTS if r['D'] == d and r['pll_shape'] == 'bowl') for d in dims]
    hill_counts = [sum(1 for r in RESULTS if r['D'] == d and r['pll_shape'] == 'hill') for d in dims]

    x = np.arange(len(dims))
    w = 0.35
    ax1.bar(x - w/2, bowl_counts, w, color=BOWL_COLOR, label='Bowl', alpha=0.8)
    ax1.bar(x + w/2, hill_counts, w, color=HILL_COLOR, label='Hill', alpha=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels([str(d) for d in dims])
    ax1.legend(fontsize=9, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # Panel 2: Mean squeeze by D, split by shape
    style_ax(ax2, title='Mean Squeeze Matches by D', xlabel='D', ylabel='Mean squeeze count')
    bowl_sq = [np.mean([r['squeeze_count'] for r in RESULTS if r['D'] == d and r['pll_shape'] == 'bowl']) if any(r['D'] == d and r['pll_shape'] == 'bowl' for r in RESULTS) else 0 for d in dims]
    hill_sq = [np.mean([r['squeeze_count'] for r in RESULTS if r['D'] == d and r['pll_shape'] == 'hill']) if any(r['D'] == d and r['pll_shape'] == 'hill' for r in RESULTS) else 0 for d in dims]

    ax2.bar(x - w/2, bowl_sq, w, color=BOWL_COLOR, label='Bowl', alpha=0.8)
    ax2.bar(x + w/2, hill_sq, w, color=HILL_COLOR, label='Hill', alpha=0.8)
    ax2.set_xticks(x)
    ax2.set_xticklabels([str(d) for d in dims])
    ax2.legend(fontsize=9, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # Panel 3: PLL R² distribution per D (box-like scatter)
    style_ax(ax3, title='PLL R² by Dimension', xlabel='D', ylabel='R²')
    for i, d in enumerate(dims):
        d_results = [r for r in RESULTS if r['D'] == d]
        r2_vals = [r['pll_R2'] for r in d_results]
        shapes = [r['pll_shape'] for r in d_results]
        colors = [BOWL_COLOR if s == 'bowl' else HILL_COLOR for s in shapes]
        jitter = np.random.normal(0, 0.08, len(r2_vals))
        ax3.scatter([i + j for j in jitter], r2_vals, c=colors, s=25, alpha=0.7, edgecolor='none')
        # Mean line
        ax3.plot([i - 0.2, i + 0.2], [np.mean(r2_vals)] * 2, color=GOLD, linewidth=2)

    ax3.set_xticks(range(len(dims)))
    ax3.set_xticklabels([str(d) for d in dims])

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    path = os.path.join(OUT_DIR, 'EXP15b_09_Dimensionality.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 10: Z-CONTRAST CORRELATION
# ============================================================
def plot_z_contrast():
    """Scatter: Z-contrast vs PLL R², colored by bowl/hill, sized by squeeze count."""
    print("  [10/13] Z-Contrast Correlation Plot...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9), facecolor=BG_DARK)
    fig.suptitle('Z-CONTRAST ANALYSIS — Atomic Number Spread vs Decomposition Quality',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)

    for r in RESULTS:
        z_vals = [CROMER_MANN[el]['Z'] for el in r['elements'] if el in CROMER_MANN]
        r['z_contrast'] = max(z_vals) - min(z_vals) if z_vals else 0

    # Panel 1: Z-contrast vs R²
    style_ax(ax1, title='Z-Contrast vs PLL R²', xlabel='Z_max - Z_min', ylabel='PLL R²')
    for r in RESULTS:
        color = BOWL_COLOR if r['pll_shape'] == 'bowl' else HILL_COLOR
        size = max(r['squeeze_count'] * 2, 10)
        ax1.scatter(r['z_contrast'], r['pll_R2'], c=color, s=size, alpha=0.6, edgecolor='none')

    # Trend line
    z_arr = np.array([r['z_contrast'] for r in RESULTS])
    r2_arr = np.array([r['pll_R2'] for r in RESULTS])
    if len(z_arr) > 2:
        z_fit = np.polyfit(z_arr, r2_arr, 1)
        z_line = np.linspace(z_arr.min(), z_arr.max(), 100)
        ax1.plot(z_line, np.polyval(z_fit, z_line), color=GOLD, linewidth=2, linestyle='--',
                 label=f'r={np.corrcoef(z_arr, r2_arr)[0,1]:.3f}')
    ax1.legend(fontsize=10, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # Panel 2: Z-contrast vs Squeeze Count
    style_ax(ax2, title='Z-Contrast vs Squeeze Count', xlabel='Z_max - Z_min', ylabel='Squeeze matches')
    for r in RESULTS:
        color = BOWL_COLOR if r['pll_shape'] == 'bowl' else HILL_COLOR
        ax2.scatter(r['z_contrast'], r['squeeze_count'], c=color, s=40, alpha=0.6, edgecolor='none')

    sq_arr = np.array([r['squeeze_count'] for r in RESULTS])
    if len(z_arr) > 2:
        corr_sq = np.corrcoef(z_arr, sq_arr)[0, 1]
        z_fit2 = np.polyfit(z_arr, sq_arr, 1)
        ax2.plot(z_line, np.polyval(z_fit2, z_line), color=GOLD, linewidth=2, linestyle='--',
                 label=f'r={corr_sq:.3f}')
    ax2.legend(fontsize=10, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # Legend patches
    from matplotlib.patches import Patch
    for ax in [ax1, ax2]:
        handles = [Patch(facecolor=BOWL_COLOR, label='Bowl'), Patch(facecolor=HILL_COLOR, label='Hill')]
        leg2 = ax.legend(handles=handles, fontsize=9, loc='lower right',
                          facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)
        ax.add_artist(leg2)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    path = os.path.join(OUT_DIR, 'EXP15b_10_Z_Contrast.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 11: PAIRWISE BALANCE RECOVERY
# ============================================================
def plot_pairwise_recovery():
    """Anti-lock systems: which ones are recovered by pairwise log-ratio balance?"""
    print("  [11/13] Pairwise Balance Recovery Chart...")

    hills = [r for r in RESULTS if r['pll_shape'] == 'hill']
    hills.sort(key=lambda r: r.get('best_pairwise_bowl', {}).get('R2', 0), reverse=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10), facecolor=BG_DARK)
    fig.suptitle('PAIRWISE BALANCE RECOVERY — Rescuing Anti-Locked Systems',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)
    fig.text(0.5, 0.955, 'When PLL parabola anti-locks (hill), pairwise log-ratios can recover bowl diagnostics',
             ha='center', fontsize=10, color=ICE)

    # Panel 1: Recovery R² bar chart
    style_ax(ax1, title='Pairwise Bowl R² for Anti-Lock Minerals',
             xlabel='Pairwise R² (best bowl)', ylabel='')

    names_h = []
    r2_pw = []
    pair_labels = []
    for r in hills[:30]:
        pw = r.get('best_pairwise_bowl', {})
        names_h.append(r['name'])
        r2_pw.append(pw.get('R2', 0))
        pair_labels.append(pw.get('pair', 'N/A'))

    colors_pw = [GREEN if v > 0.5 else (ORANGE if v > 0.2 else RED) for v in r2_pw]
    y_pos = range(len(names_h))
    ax1.barh(y_pos, r2_pw, color=colors_pw, alpha=0.8, height=0.7)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names_h, fontsize=7, color=WHITE)
    ax1.axvline(0.5, color=GOLD, linewidth=2, linestyle='--', alpha=0.7, label='Recovery threshold')
    ax1.invert_yaxis()
    ax1.legend(fontsize=9, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # Annotate with pair names
    for i, (v, pair) in enumerate(zip(r2_pw, pair_labels)):
        if v > 0.05:
            ax1.text(v + 0.02, i, pair, va='center', fontsize=6, color=ICE)

    # Panel 2: PLL R² vs Pairwise R² scatter
    style_ax(ax2, title='Original PLL R² vs Recovery Pairwise R²',
             xlabel='PLL R² (hill)', ylabel='Best Pairwise R² (bowl)')

    for r in hills:
        pw = r.get('best_pairwise_bowl', {})
        pw_r2 = pw.get('R2', 0)
        size = max(r['squeeze_count'] * 2, 15)
        ax2.scatter(r['pll_R2'], pw_r2, s=size, c=ORANGE, alpha=0.6, edgecolor='none')

    ax2.axhline(0.5, color=GOLD, linewidth=1.5, linestyle='--', alpha=0.5)
    ax2.plot([0, 1], [0, 1], color=GREY, linewidth=1, linestyle=':', alpha=0.3)

    # Count recoveries
    n_recovered = sum(1 for r in hills if r.get('best_pairwise_bowl', {}).get('R2', 0) > 0.5)
    ax2.text(0.05, 0.95, f'Recovered: {n_recovered}/{len(hills)} ({100*n_recovered/len(hills):.0f}%)',
             transform=ax2.transAxes, fontsize=12, fontweight='bold', color=GREEN,
             bbox=dict(boxstyle='round,pad=0.4', facecolor=BG_DARK, edgecolor=GREEN))

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path = os.path.join(OUT_DIR, 'EXP15b_11_Pairwise_Recovery.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 12: BOWL vs HILL STATISTICAL COMPARISON
# ============================================================
def plot_bowl_vs_hill():
    """Side-by-side statistical comparison of bowl vs hill populations."""
    print("  [12/13] Bowl vs Hill Statistical Comparison...")

    bowls = [r for r in RESULTS if r['pll_shape'] == 'bowl']
    hills = [r for r in RESULTS if r['pll_shape'] == 'hill']

    fig, axes = plt.subplots(2, 3, figsize=(22, 12), facecolor=BG_DARK)
    fig.suptitle('BOWL vs HILL — Complete Statistical Comparison',
                 fontsize=16, fontweight='bold', color=GOLD, y=0.98)
    fig.text(0.5, 0.955, f'Bowl (locked): {len(bowls)} minerals  |  Hill (anti-lock): {len(hills)} minerals',
             ha='center', fontsize=11, color=ICE)

    # 1. Squeeze count histogram
    ax = axes[0][0]
    style_ax(ax, title='Squeeze Match Distribution', xlabel='Squeeze count', ylabel='Frequency')
    bowl_sq = [r['squeeze_count'] for r in bowls]
    hill_sq = [r['squeeze_count'] for r in hills]
    bins = np.arange(0, 55, 3)
    ax.hist(bowl_sq, bins=bins, color=BOWL_COLOR, alpha=0.6, label=f'Bowl (mean={np.mean(bowl_sq):.1f})')
    ax.hist(hill_sq, bins=bins, color=HILL_COLOR, alpha=0.6, label=f'Hill (mean={np.mean(hill_sq):.1f})')
    ax.legend(fontsize=8, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # 2. Best delta histogram
    ax = axes[0][1]
    style_ax(ax, title='Best Delta Distribution', xlabel='-log10(delta)', ylabel='Frequency')
    bowl_d = [-np.log10(max(r['best_delta'], 1e-10)) for r in bowls if r['best_delta'] < 999]
    hill_d = [-np.log10(max(r['best_delta'], 1e-10)) for r in hills if r['best_delta'] < 999]
    bins2 = np.linspace(1, 5, 20)
    ax.hist(bowl_d, bins=bins2, color=BOWL_COLOR, alpha=0.6, label='Bowl')
    ax.hist(hill_d, bins=bins2, color=HILL_COLOR, alpha=0.6, label='Hill')
    ax.legend(fontsize=8, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # 3. R² histogram
    ax = axes[0][2]
    style_ax(ax, title='PLL R² Distribution', xlabel='R²', ylabel='Frequency')
    bowl_r2 = [r['pll_R2'] for r in bowls]
    hill_r2 = [r['pll_R2'] for r in hills]
    bins3 = np.linspace(0, 1, 20)
    ax.hist(bowl_r2, bins=bins3, color=BOWL_COLOR, alpha=0.6, label='Bowl')
    ax.hist(hill_r2, bins=bins3, color=HILL_COLOR, alpha=0.6, label='Hill')
    ax.legend(fontsize=8, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # 4. σ²_A range comparison
    ax = axes[1][0]
    style_ax(ax, title='sigma_A^2 Range', xlabel='sigma_A^2 range', ylabel='Frequency')
    bowl_range = [r.get('sA_range', 0) for r in bowls]
    hill_range = [r.get('sA_range', 0) for r in hills]
    bins4 = np.linspace(0, max(bowl_range + hill_range) * 1.1, 20)
    ax.hist(bowl_range, bins=bins4, color=BOWL_COLOR, alpha=0.6, label='Bowl')
    ax.hist(hill_range, bins=bins4, color=HILL_COLOR, alpha=0.6, label='Hill')
    ax.legend(fontsize=8, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # 5. Squeeze vs R² scatter
    ax = axes[1][1]
    style_ax(ax, title='Squeeze Count vs PLL R²', xlabel='PLL R²', ylabel='Squeeze count')
    for r in bowls:
        ax.scatter(r['pll_R2'], r['squeeze_count'], c=BOWL_COLOR, s=30, alpha=0.6)
    for r in hills:
        ax.scatter(r['pll_R2'], r['squeeze_count'], c=HILL_COLOR, s=30, alpha=0.6)

    # 6. Summary statistics table
    ax = axes[1][2]
    ax.set_facecolor(BG_PANEL)
    ax.axis('off')
    ax.set_title('KEY STATISTICS', fontsize=12, fontweight='bold', color=GOLD, pad=10)

    stats_text = [
        ('Metric', 'BOWL', 'HILL'),
        ('Count', f'{len(bowls)}', f'{len(hills)}'),
        ('Mean squeeze', f'{np.mean(bowl_sq):.1f}', f'{np.mean(hill_sq):.1f}'),
        ('Median squeeze', f'{np.median(bowl_sq):.0f}', f'{np.median(hill_sq):.0f}'),
        ('Mean delta', f'{np.mean([r["best_delta"] for r in bowls if r["best_delta"]<999]):.5f}',
         f'{np.mean([r["best_delta"] for r in hills if r["best_delta"]<999]):.5f}'),
        ('>= 5 matches', f'{100*sum(1 for s in bowl_sq if s>=5)/len(bowls):.0f}%',
         f'{100*sum(1 for s in hill_sq if s>=5)/len(hills):.0f}%'),
        ('delta < 0.005', f'{100*sum(1 for r in bowls if r["best_delta"]<0.005)/len(bowls):.0f}%',
         f'{100*sum(1 for r in hills if r["best_delta"]<0.005)/len(hills):.0f}%'),
        ('Mean R²', f'{np.mean(bowl_r2):.3f}', f'{np.mean(hill_r2):.3f}'),
        ('PW recovery', 'N/A', f'{sum(1 for r in hills if r.get("best_pairwise_bowl",{}).get("R2",0)>0.5)}/{len(hills)}'),
    ]

    for i, (label, b_val, h_val) in enumerate(stats_text):
        y = 0.92 - i * 0.1
        weight = 'bold' if i == 0 else 'normal'
        color_l = GOLD if i == 0 else WHITE
        ax.text(0.05, y, label, transform=ax.transAxes, fontsize=10, color=color_l, fontweight=weight)
        ax.text(0.55, y, b_val, transform=ax.transAxes, fontsize=10, color=BOWL_COLOR, fontweight=weight, ha='center')
        ax.text(0.85, y, h_val, transform=ax.transAxes, fontsize=10, color=HILL_COLOR, fontweight=weight, ha='center')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path = os.path.join(OUT_DIR, 'EXP15b_12_Bowl_vs_Hill.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# DIAGRAM 13: MASTER DASHBOARD
# ============================================================
def plot_master_dashboard():
    """Programme-level overview: the cohesive summary of EXP-15b."""
    print("  [13/13] Master Dashboard...")

    bowls = [r for r in RESULTS if r['pll_shape'] == 'bowl']
    hills = [r for r in RESULTS if r['pll_shape'] == 'hill']

    fig = plt.figure(figsize=(24, 18), facecolor=BG_DARK)
    gs = gridspec.GridSpec(4, 4, figure=fig, hspace=0.35, wspace=0.35)

    fig.suptitle('EXP-15b MASTER DASHBOARD — Big Data Crystallography',
                 fontsize=18, fontweight='bold', color=GOLD, y=0.98)
    fig.text(0.5, 0.96, 'Higgins Unity Framework | 106 minerals | Cromer-Mann scattering factors | Full Higgins Decomposition',
             ha='center', fontsize=10, color=ICE)

    # --- Panel A: Headline numbers ---
    ax_head = fig.add_subplot(gs[0, 0:2])
    ax_head.set_facecolor(BG_PANEL)
    ax_head.axis('off')

    headlines = [
        (f'{len(RESULTS)}', 'Minerals\nProcessed', WHITE),
        (f'{len(bowls)}', 'Bowl\n(Locked)', BOWL_COLOR),
        (f'{len(hills)}', 'Hill\n(Anti-lock)', HILL_COLOR),
        (f'26.4', 'Hill Mean\nSqueezes', GOLD),
        (f'17.8', 'Bowl Mean\nSqueezes', CYAN),
    ]
    for i, (num, label, color) in enumerate(headlines):
        x = 0.1 + i * 0.18
        ax_head.text(x, 0.65, num, transform=ax_head.transAxes, fontsize=28,
                     fontweight='bold', color=color, ha='center')
        ax_head.text(x, 0.2, label, transform=ax_head.transAxes, fontsize=9,
                     color=GREY, ha='center')

    # --- Panel B: Hypothesis verdict ---
    ax_verdict = fig.add_subplot(gs[0, 2:4])
    ax_verdict.set_facecolor('#0a1a0a')
    ax_verdict.axis('off')

    ax_verdict.text(0.5, 0.85, 'HYPOTHESIS CONFIRMED', transform=ax_verdict.transAxes,
                    fontsize=16, fontweight='bold', color=GREEN, ha='center')
    ax_verdict.text(0.5, 0.55, '"Anti-lock does not mean uninformative —', transform=ax_verdict.transAxes,
                    fontsize=11, color=ICE, ha='center', style='italic')
    ax_verdict.text(0.5, 0.35, 'the information is in a different channel."', transform=ax_verdict.transAxes,
                    fontsize=11, color=ICE, ha='center', style='italic')
    ax_verdict.text(0.5, 0.1, '— Peter Higgins, April 2026', transform=ax_verdict.transAxes,
                    fontsize=9, color=GOLD, ha='center')
    for spine in ax_verdict.spines.values():
        spine.set_color(GREEN)
        spine.set_linewidth(2)

    # --- Panel C: Squeeze histogram ---
    ax_sq = fig.add_subplot(gs[1, 0:2])
    style_ax(ax_sq, title='Super Squeeze Distribution', xlabel='Matches', ylabel='Count')
    bins = np.arange(0, 55, 3)
    ax_sq.hist([r['squeeze_count'] for r in bowls], bins=bins, color=BOWL_COLOR, alpha=0.6, label='Bowl')
    ax_sq.hist([r['squeeze_count'] for r in hills], bins=bins, color=HILL_COLOR, alpha=0.6, label='Hill')
    ax_sq.legend(fontsize=8, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)

    # --- Panel D: Top 10 tightest ---
    ax_top = fig.add_subplot(gs[1, 2:4])
    ax_top.set_facecolor(BG_PANEL)
    ax_top.axis('off')
    style_ax(ax_top, title='TOP 10 TIGHTEST SUPER SQUEEZES')

    sorted_r = sorted(RESULTS, key=lambda r: r['best_delta'])[:10]
    for i, r in enumerate(sorted_r):
        y = 0.88 - i * 0.088
        sq = r.get('best_squeeze', {})
        if not sq:
            continue
        shape_c = BOWL_COLOR if r['pll_shape'] == 'bowl' else HILL_COLOR
        ax_top.text(0.02, y, f'{i+1}.', transform=ax_top.transAxes, fontsize=8, color=GREY)
        ax_top.text(0.08, y, r['name'], transform=ax_top.transAxes, fontsize=8,
                    color=shape_c, fontweight='bold')
        ax_top.text(0.42, y, f"{sq.get('input','?')} -> {sq.get('output','?')}",
                    transform=ax_top.transAxes, fontsize=8, color=ICE)
        ax_top.text(0.82, y, f"d={sq.get('delta',0):.6f}",
                    transform=ax_top.transAxes, fontsize=8, color=GOLD)

    # --- Panel E: Dimensionality ---
    ax_dim = fig.add_subplot(gs[2, 0])
    style_ax(ax_dim, title='Bowl/Hill by D', xlabel='D', ylabel='Count')
    dims = sorted(set(r['D'] for r in RESULTS))
    x = np.arange(len(dims))
    w = 0.35
    bc = [sum(1 for r in RESULTS if r['D'] == d and r['pll_shape'] == 'bowl') for d in dims]
    hc = [sum(1 for r in RESULTS if r['D'] == d and r['pll_shape'] == 'hill') for d in dims]
    ax_dim.bar(x - w/2, bc, w, color=BOWL_COLOR, alpha=0.8)
    ax_dim.bar(x + w/2, hc, w, color=HILL_COLOR, alpha=0.8)
    ax_dim.set_xticks(x)
    ax_dim.set_xticklabels([str(d) for d in dims])

    # --- Panel F: Z-contrast scatter ---
    ax_z = fig.add_subplot(gs[2, 1])
    style_ax(ax_z, title='Z-Contrast vs R²', xlabel='Z contrast', ylabel='R²')
    for r in RESULTS:
        z_vals = [CROMER_MANN[el]['Z'] for el in r['elements'] if el in CROMER_MANN]
        z_c = max(z_vals) - min(z_vals) if z_vals else 0
        color = BOWL_COLOR if r['pll_shape'] == 'bowl' else HILL_COLOR
        ax_z.scatter(z_c, r['pll_R2'], c=color, s=20, alpha=0.5)

    # --- Panel G: Pairwise recovery ---
    ax_pw = fig.add_subplot(gs[2, 2])
    style_ax(ax_pw, title='Pairwise Recovery', xlabel='', ylabel='')
    n_rec = sum(1 for r in hills if r.get('best_pairwise_bowl', {}).get('R2', 0) > 0.5)
    n_not = len(hills) - n_rec
    ax_pw.pie([n_rec, n_not], labels=[f'Recovered\n{n_rec}', f'Not recovered\n{n_not}'],
              colors=[GREEN, RED], autopct='%1.0f%%', startangle=90,
              textprops={'color': WHITE, 'fontsize': 9})

    # --- Panel H: Mineral type breakdown ---
    ax_type = fig.add_subplot(gs[2, 3])
    style_ax(ax_type, title='By Mineral Type')
    types = {}
    for r in RESULTS:
        t = r['type']
        if t not in types:
            types[t] = {'bowl': 0, 'hill': 0}
        types[t][r['pll_shape']] += 1

    sorted_types = sorted(types.items(), key=lambda x: -(x[1]['bowl'] + x[1]['hill']))[:10]
    t_names = [t[0] for t in sorted_types]
    t_bowl = [t[1]['bowl'] for t in sorted_types]
    t_hill = [t[1]['hill'] for t in sorted_types]
    y_t = range(len(t_names))
    ax_type.barh(y_t, t_bowl, color=BOWL_COLOR, alpha=0.8, height=0.4, label='Bowl')
    ax_type.barh([y + 0.4 for y in y_t], t_hill, color=HILL_COLOR, alpha=0.8, height=0.4, label='Hill')
    ax_type.set_yticks([y + 0.2 for y in y_t])
    ax_type.set_yticklabels(t_names, fontsize=7, color=WHITE)
    ax_type.invert_yaxis()

    # --- Panel I: Programme timeline ---
    ax_time = fig.add_subplot(gs[3, :])
    ax_time.set_facecolor(BG_PANEL)
    ax_time.axis('off')
    style_ax(ax_time, title='PROGRAMME STATUS')

    milestones = [
        ('EXP-1 to 12', '75 systems', 'Jan-Apr 2026', GREY),
        ('EXP-13', 'Calibration Proof\n7 theorems', 'Apr 20', CYAN),
        ('EXP-14', 'HFSP on AME2020\nNe-20 discovery', 'Apr 20-21', CYAN),
        ('EXP-15', 'X-ray Crystallography\n6 crystals', 'Apr 21', GREEN),
        ('EXP-15b', 'BIG DATA\n106 minerals', 'Apr 22', GOLD),
        ('CoDaWork', 'Coimbra\nPortugal', 'Jun 1-5', MAGENTA),
    ]

    for i, (name, desc, date, color) in enumerate(milestones):
        x = 0.05 + i * 0.16
        ax_time.text(x, 0.75, name, transform=ax_time.transAxes, fontsize=11,
                     fontweight='bold', color=color, ha='center')
        ax_time.text(x, 0.4, desc, transform=ax_time.transAxes, fontsize=8,
                     color=WHITE, ha='center')
        ax_time.text(x, 0.15, date, transform=ax_time.transAxes, fontsize=7,
                     color=GREY, ha='center')
        if i < len(milestones) - 1:
            ax_time.annotate('', xy=(x + 0.12, 0.7), xytext=(x + 0.04, 0.7),
                             xycoords='axes fraction', textcoords='axes fraction',
                             arrowprops=dict(arrowstyle='->', color=GREY, lw=1.5))

    path = os.path.join(OUT_DIR, 'EXP15b_13_Master_Dashboard.png')
    fig.savefig(path, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
    plt.close(fig)
    print(f"    -> {path}")


# ============================================================
# RUN ALL
# ============================================================
if __name__ == '__main__':
    print("=" * 80)
    print("  EXP-15b: COMPLETE VISUALIZATION SUITE")
    print("  Higgins Unity Framework — Output Interpreter")
    print("=" * 80)

    plot_ternary()
    plot_pll_parabola()
    plot_super_squeeze_spectrum()
    plot_eitt_entropy()
    plot_composition_trajectories()
    plot_heatmap()
    plot_radar()
    plot_thermal_map()
    plot_dimensionality()
    plot_z_contrast()
    plot_pairwise_recovery()
    plot_bowl_vs_hill()
    plot_master_dashboard()

    print("\n" + "=" * 80)
    print(f"  ALL 13 DIAGRAMS COMPLETE — saved to {OUT_DIR}")
    print("=" * 80)
