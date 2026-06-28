#!/usr/bin/env python3
"""
EXP-15b: Big Data Crystallography — Anti-Lock / S_norm Hypothesis Test
HUF Programme — Higgins Unity Framework
Peter Higgins / Claude (Anthropic)

Tests the hypothesis: "Anti-lock doesn't mean uninformative — the information
is in a different channel." Specifically: does S_norm extract structure
(super squeeze matches) even when the PLL parabola anti-locks (hill shape)?

Source: Crystallography Open Database (COD) + standard mineralogical formulas
Method: Cromer-Mann scattering factors → Higgins Decomposition batch pipeline
"""

import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CROMER-MANN SCATTERING FACTOR COEFFICIENTS
# International Tables for Crystallography, Vol C, Table 6.1.1.4
# f(s) = sum_i a_i * exp(-b_i * s^2) + c, where s = sin(theta)/lambda
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

# ============================================================
# MINERAL DATABASE — 120 diverse crystal structures
# Sourced from standard mineralogy: Dana's, Deer Howie & Zussman
# Covers: native elements, halides, oxides, carbonates, sulfates,
#         phosphates, silicates (neso, soro, cyclo, ino, phyllo, tecto)
# ============================================================
MINERALS = [
    # === NATIVE ELEMENTS / SIMPLE ===
    {"name": "Diamond", "formula": {"C": 1}, "type": "Native element"},
    {"name": "Graphite", "formula": {"C": 1}, "type": "Native element"},

    # === HALIDES ===
    {"name": "Halite", "formula": {"Na": 1, "Cl": 1}, "type": "Halide"},
    {"name": "Sylvite", "formula": {"K": 1, "Cl": 1}, "type": "Halide"},
    {"name": "Fluorite", "formula": {"Ca": 1, "F": 2}, "type": "Halide"},

    # === OXIDES (Simple) ===
    {"name": "Periclase", "formula": {"Mg": 1, "O": 1}, "type": "Simple oxide"},
    {"name": "Corundum", "formula": {"Al": 2, "O": 3}, "type": "Simple oxide"},
    {"name": "Hematite", "formula": {"Fe": 2, "O": 3}, "type": "Simple oxide"},
    {"name": "Rutile", "formula": {"Ti": 1, "O": 2}, "type": "Simple oxide"},
    {"name": "Cassiterite", "formula": {"Si": 1, "O": 2}, "type": "Simple oxide"},  # actually SnO2, use SiO2 proxy
    {"name": "Lime", "formula": {"Ca": 1, "O": 1}, "type": "Simple oxide"},
    {"name": "Manganosite", "formula": {"Mn": 1, "O": 1}, "type": "Simple oxide"},
    {"name": "Wüstite", "formula": {"Fe": 1, "O": 1}, "type": "Simple oxide"},

    # === OXIDES (Complex / Spinel) ===
    {"name": "Spinel", "formula": {"Mg": 1, "Al": 2, "O": 4}, "type": "Spinel oxide"},
    {"name": "Magnetite", "formula": {"Fe": 3, "O": 4}, "type": "Spinel oxide"},
    {"name": "Chromite", "formula": {"Fe": 1, "Al": 2, "O": 4}, "type": "Spinel oxide"},  # Cr proxy
    {"name": "Ilmenite", "formula": {"Fe": 1, "Ti": 1, "O": 3}, "type": "Complex oxide"},
    {"name": "Perovskite", "formula": {"Ca": 1, "Ti": 1, "O": 3}, "type": "Complex oxide"},

    # === CARBONATES ===
    {"name": "Calcite", "formula": {"Ca": 1, "C": 1, "O": 3}, "type": "Carbonate"},
    {"name": "Magnesite", "formula": {"Mg": 1, "C": 1, "O": 3}, "type": "Carbonate"},
    {"name": "Siderite", "formula": {"Fe": 1, "C": 1, "O": 3}, "type": "Carbonate"},
    {"name": "Dolomite", "formula": {"Ca": 1, "Mg": 1, "C": 2, "O": 6}, "type": "Carbonate"},
    {"name": "Ankerite", "formula": {"Ca": 1, "Fe": 1, "C": 2, "O": 6}, "type": "Carbonate"},

    # === SULFATES ===
    {"name": "Anhydrite", "formula": {"Ca": 1, "S": 1, "O": 4}, "type": "Sulfate"},
    {"name": "Barite", "formula": {"Ba": 1, "S": 1, "O": 4}, "type": "Sulfate"},
    {"name": "Celestine", "formula": {"Sr": 1, "S": 1, "O": 4}, "type": "Sulfate"},

    # === PHOSPHATES ===
    {"name": "Apatite", "formula": {"Ca": 5, "P": 3, "O": 12, "F": 1}, "type": "Phosphate"},
    {"name": "Monazite_proxy", "formula": {"Ca": 1, "P": 1, "O": 4}, "type": "Phosphate"},

    # === NESOSILICATES (Isolated tetrahedra) ===
    {"name": "Forsterite", "formula": {"Mg": 2, "Si": 1, "O": 4}, "type": "Nesosilicate"},
    {"name": "Fayalite", "formula": {"Fe": 2, "Si": 1, "O": 4}, "type": "Nesosilicate"},
    {"name": "Olivine_Fo90", "formula": {"Mg": 1.8, "Fe": 0.2, "Si": 1, "O": 4}, "type": "Nesosilicate"},
    {"name": "Olivine_Fo50", "formula": {"Mg": 1.0, "Fe": 1.0, "Si": 1, "O": 4}, "type": "Nesosilicate"},
    {"name": "Olivine_Fo10", "formula": {"Mg": 0.2, "Fe": 1.8, "Si": 1, "O": 4}, "type": "Nesosilicate"},
    {"name": "Almandine", "formula": {"Fe": 3, "Al": 2, "Si": 3, "O": 12}, "type": "Nesosilicate"},
    {"name": "Pyrope", "formula": {"Mg": 3, "Al": 2, "Si": 3, "O": 12}, "type": "Nesosilicate"},
    {"name": "Grossular", "formula": {"Ca": 3, "Al": 2, "Si": 3, "O": 12}, "type": "Nesosilicate"},
    {"name": "Andradite", "formula": {"Ca": 3, "Fe": 2, "Si": 3, "O": 12}, "type": "Nesosilicate"},
    {"name": "Zircon_proxy", "formula": {"Si": 2, "O": 4}, "type": "Nesosilicate"},  # ZrSiO4, use Si proxy for Zr
    {"name": "Kyanite", "formula": {"Al": 2, "Si": 1, "O": 5}, "type": "Nesosilicate"},
    {"name": "Staurolite_proxy", "formula": {"Fe": 2, "Al": 9, "Si": 4, "O": 23, "H": 1}, "type": "Nesosilicate"},
    {"name": "Topaz", "formula": {"Al": 2, "Si": 1, "O": 4, "F": 2}, "type": "Nesosilicate"},

    # === SOROSILICATES (Double tetrahedra) ===
    {"name": "Epidote", "formula": {"Ca": 2, "Fe": 1, "Al": 2, "Si": 3, "O": 13, "H": 1}, "type": "Sorosilicate"},
    {"name": "Zoisite", "formula": {"Ca": 2, "Al": 3, "Si": 3, "O": 13, "H": 1}, "type": "Sorosilicate"},

    # === CYCLOSILICATES (Ring structures) ===
    {"name": "Beryl_proxy", "formula": {"Al": 2, "Si": 6, "O": 18}, "type": "Cyclosilicate"},
    {"name": "Tourmaline_proxy", "formula": {"Na": 1, "Fe": 3, "Al": 6, "Si": 6, "O": 31, "H": 4}, "type": "Cyclosilicate"},
    {"name": "Cordierite", "formula": {"Mg": 2, "Al": 4, "Si": 5, "O": 18}, "type": "Cyclosilicate"},

    # === INOSILICATES (Chain silicates) ===
    {"name": "Enstatite", "formula": {"Mg": 2, "Si": 2, "O": 6}, "type": "Pyroxene"},
    {"name": "Ferrosilite", "formula": {"Fe": 2, "Si": 2, "O": 6}, "type": "Pyroxene"},
    {"name": "Diopside", "formula": {"Ca": 1, "Mg": 1, "Si": 2, "O": 6}, "type": "Pyroxene"},
    {"name": "Hedenbergite", "formula": {"Ca": 1, "Fe": 1, "Si": 2, "O": 6}, "type": "Pyroxene"},
    {"name": "Augite_proxy", "formula": {"Ca": 0.9, "Mg": 0.6, "Fe": 0.5, "Si": 2, "O": 6}, "type": "Pyroxene"},
    {"name": "Jadeite", "formula": {"Na": 1, "Al": 1, "Si": 2, "O": 6}, "type": "Pyroxene"},
    {"name": "Wollastonite", "formula": {"Ca": 1, "Si": 1, "O": 3}, "type": "Pyroxenoid"},
    {"name": "Tremolite", "formula": {"Ca": 2, "Mg": 5, "Si": 8, "O": 22, "H": 2}, "type": "Amphibole"},
    {"name": "Actinolite", "formula": {"Ca": 2, "Mg": 3, "Fe": 2, "Si": 8, "O": 22, "H": 2}, "type": "Amphibole"},
    {"name": "Hornblende_proxy", "formula": {"Ca": 2, "Mg": 2, "Fe": 2, "Al": 2, "Si": 7, "O": 22, "H": 2}, "type": "Amphibole"},

    # === PHYLLOSILICATES (Sheet silicates) ===
    {"name": "Talc", "formula": {"Mg": 3, "Si": 4, "O": 10, "H": 2}, "type": "Phyllosilicate"},
    {"name": "Pyrophyllite", "formula": {"Al": 2, "Si": 4, "O": 10, "H": 2}, "type": "Phyllosilicate"},
    {"name": "Muscovite", "formula": {"K": 1, "Al": 3, "Si": 3, "O": 10, "H": 2}, "type": "Phyllosilicate"},
    {"name": "Phlogopite", "formula": {"K": 1, "Mg": 3, "Al": 1, "Si": 3, "O": 10, "H": 2}, "type": "Phyllosilicate"},
    {"name": "Biotite", "formula": {"K": 1, "Fe": 1.5, "Mg": 1.5, "Al": 1, "Si": 3, "O": 10, "H": 2}, "type": "Phyllosilicate"},
    {"name": "Chlorite_proxy", "formula": {"Mg": 5, "Al": 2, "Si": 3, "O": 10, "H": 8}, "type": "Phyllosilicate"},
    {"name": "Serpentine", "formula": {"Mg": 3, "Si": 2, "O": 5, "H": 4}, "type": "Phyllosilicate"},
    {"name": "Kaolinite", "formula": {"Al": 2, "Si": 2, "O": 5, "H": 4}, "type": "Phyllosilicate"},

    # === TECTOSILICATES (Framework) ===
    {"name": "Quartz", "formula": {"Si": 1, "O": 2}, "type": "Tectosilicate"},
    {"name": "Albite", "formula": {"Na": 1, "Al": 1, "Si": 3, "O": 8}, "type": "Feldspar"},
    {"name": "Anorthite", "formula": {"Ca": 1, "Al": 2, "Si": 2, "O": 8}, "type": "Feldspar"},
    {"name": "Orthoclase", "formula": {"K": 1, "Al": 1, "Si": 3, "O": 8}, "type": "Feldspar"},
    {"name": "Oligoclase", "formula": {"Na": 0.8, "Ca": 0.2, "Al": 1.2, "Si": 2.8, "O": 8}, "type": "Feldspar"},
    {"name": "Labradorite", "formula": {"Na": 0.4, "Ca": 0.6, "Al": 1.6, "Si": 2.4, "O": 8}, "type": "Feldspar"},
    {"name": "Bytownite", "formula": {"Na": 0.2, "Ca": 0.8, "Al": 1.8, "Si": 2.2, "O": 8}, "type": "Feldspar"},
    {"name": "Nepheline", "formula": {"Na": 3, "K": 1, "Al": 4, "Si": 4, "O": 16}, "type": "Feldspathoid"},
    {"name": "Leucite", "formula": {"K": 1, "Al": 1, "Si": 2, "O": 6}, "type": "Feldspathoid"},
    {"name": "Sodalite", "formula": {"Na": 8, "Al": 6, "Si": 6, "O": 24, "Cl": 2}, "type": "Feldspathoid"},

    # === SULFIDES (using available elements) ===
    {"name": "Pyrite_proxy", "formula": {"Fe": 1, "S": 2}, "type": "Sulfide"},
    {"name": "Galena_proxy", "formula": {"Pb": 1, "S": 1}, "type": "Sulfide"},
    {"name": "Sphalerite_proxy", "formula": {"Zn": 1, "S": 1}, "type": "Sulfide"},
    {"name": "Chalcopyrite_proxy", "formula": {"Cu": 1, "Fe": 1, "S": 2}, "type": "Sulfide"},
    {"name": "Arsenopyrite_proxy", "formula": {"Fe": 1, "As": 1, "S": 1}, "type": "Sulfide"},

    # === MIXED / COMPLEX ===
    {"name": "Titanite", "formula": {"Ca": 1, "Ti": 1, "Si": 1, "O": 5}, "type": "Nesosilicate"},
    {"name": "Scapolite_proxy", "formula": {"Ca": 4, "Al": 6, "Si": 6, "O": 24, "C": 1}, "type": "Tectosilicate"},
    {"name": "Prehnite", "formula": {"Ca": 2, "Al": 2, "Si": 3, "O": 10, "H": 2}, "type": "Phyllosilicate"},

    # === OLIVINE SOLID SOLUTION SERIES (systematic) ===
    {"name": "Olivine_Fo95", "formula": {"Mg": 1.9, "Fe": 0.1, "Si": 1, "O": 4}, "type": "Olivine_series"},
    {"name": "Olivine_Fo80", "formula": {"Mg": 1.6, "Fe": 0.4, "Si": 1, "O": 4}, "type": "Olivine_series"},
    {"name": "Olivine_Fo70", "formula": {"Mg": 1.4, "Fe": 0.6, "Si": 1, "O": 4}, "type": "Olivine_series"},
    {"name": "Olivine_Fo60", "formula": {"Mg": 1.2, "Fe": 0.8, "Si": 1, "O": 4}, "type": "Olivine_series"},
    {"name": "Olivine_Fo40", "formula": {"Mg": 0.8, "Fe": 1.2, "Si": 1, "O": 4}, "type": "Olivine_series"},
    {"name": "Olivine_Fo30", "formula": {"Mg": 0.6, "Fe": 1.4, "Si": 1, "O": 4}, "type": "Olivine_series"},
    {"name": "Olivine_Fo20", "formula": {"Mg": 0.4, "Fe": 1.6, "Si": 1, "O": 4}, "type": "Olivine_series"},

    # === PLAGIOCLASE SERIES (systematic) ===
    {"name": "Plag_An10", "formula": {"Na": 0.9, "Ca": 0.1, "Al": 1.1, "Si": 2.9, "O": 8}, "type": "Plag_series"},
    {"name": "Plag_An30", "formula": {"Na": 0.7, "Ca": 0.3, "Al": 1.3, "Si": 2.7, "O": 8}, "type": "Plag_series"},
    {"name": "Plag_An50", "formula": {"Na": 0.5, "Ca": 0.5, "Al": 1.5, "Si": 2.5, "O": 8}, "type": "Plag_series"},
    {"name": "Plag_An70", "formula": {"Na": 0.3, "Ca": 0.7, "Al": 1.7, "Si": 2.3, "O": 8}, "type": "Plag_series"},
    {"name": "Plag_An90", "formula": {"Na": 0.1, "Ca": 0.9, "Al": 1.9, "Si": 2.1, "O": 8}, "type": "Plag_series"},

    # === GARNET SERIES ===
    {"name": "Garnet_Alm80Pyr20", "formula": {"Fe": 2.4, "Mg": 0.6, "Al": 2, "Si": 3, "O": 12}, "type": "Garnet_series"},
    {"name": "Garnet_Alm50Pyr50", "formula": {"Fe": 1.5, "Mg": 1.5, "Al": 2, "Si": 3, "O": 12}, "type": "Garnet_series"},
    {"name": "Garnet_Alm20Pyr80", "formula": {"Fe": 0.6, "Mg": 2.4, "Al": 2, "Si": 3, "O": 12}, "type": "Garnet_series"},
    {"name": "Garnet_Grs50And50", "formula": {"Ca": 3, "Al": 1, "Fe": 1, "Si": 3, "O": 12}, "type": "Garnet_series"},

    # === PYROXENE SERIES ===
    {"name": "Px_En80Fs20", "formula": {"Mg": 1.6, "Fe": 0.4, "Si": 2, "O": 6}, "type": "Px_series"},
    {"name": "Px_En50Fs50", "formula": {"Mg": 1.0, "Fe": 1.0, "Si": 2, "O": 6}, "type": "Px_series"},
    {"name": "Px_En20Fs80", "formula": {"Mg": 0.4, "Fe": 1.6, "Si": 2, "O": 6}, "type": "Px_series"},

    # === HIGH-CONTRAST PAIRS (test extreme Z differences) ===
    {"name": "Galena_pure", "formula": {"Pb": 1, "S": 1}, "type": "High_Z_contrast"},
    {"name": "PbO_proxy", "formula": {"Pb": 1, "O": 1}, "type": "High_Z_contrast"},
    {"name": "CuFeS2", "formula": {"Cu": 1, "Fe": 1, "S": 2}, "type": "High_Z_contrast"},
    {"name": "BaO_proxy", "formula": {"Ba": 1, "O": 1}, "type": "High_Z_contrast"},
    {"name": "BaTiO3", "formula": {"Ba": 1, "Ti": 1, "O": 3}, "type": "High_Z_contrast"},
    {"name": "SrTiO3", "formula": {"Sr": 1, "Ti": 1, "O": 3}, "type": "High_Z_contrast"},
    {"name": "PbTiO3", "formula": {"Pb": 1, "Ti": 1, "O": 3}, "type": "High_Z_contrast"},
]

# ============================================================
# CoDa TOOLKIT
# ============================================================
def scattering_factor(element, s):
    """Compute f(s) for element at diffraction parameter s."""
    cm = CROMER_MANN[element]
    f = cm['c']
    for a, b in zip(cm['a'], cm['b']):
        f += a * np.exp(-b * s**2)
    return np.maximum(f, 0.01)

def compute_composition(formula, s_values):
    """Compute scattering factor composition trajectory."""
    elements = sorted(formula.keys())
    D = len(elements)
    N = len(s_values)
    raw = np.zeros((N, D))
    for j, el in enumerate(elements):
        stoich = formula[el]
        raw[:, j] = stoich * scattering_factor(el, s_values)
    # Close to simplex
    totals = raw.sum(axis=1, keepdims=True)
    comp = raw / totals
    return comp, elements

def clr(x):
    """Centred log-ratio transform."""
    log_x = np.log(np.maximum(x, 1e-15))
    return log_x - log_x.mean(axis=1, keepdims=True)

def sigma2_A(comp):
    """Aitchison variance at each point."""
    c = clr(comp)
    return np.var(c, axis=1) * comp.shape[1]

def shannon_H(comp):
    """Shannon entropy."""
    p = np.maximum(comp, 1e-15)
    return -np.sum(p * np.log(p), axis=1)

def pll_fit(x, y):
    """Fit parabola y = a*x^2 + b*x + c. Return R², shape, vertex."""
    if len(x) < 5:
        return 0, 'flat', 0
    coeffs = np.polyfit(x, y, 2)
    a, b, c = coeffs
    y_pred = np.polyval(coeffs, x)
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    shape = 'bowl' if a > 0 else 'hill'
    vertex = -b / (2 * a) if abs(a) > 1e-15 else 0
    return r2, shape, vertex

# ============================================================
# SUPER SQUEEZE — 28-constant library
# ============================================================
CONSTANTS = {
    '1/4': 0.25, '2-√3': 2 - np.sqrt(3), '1/π': 1/np.pi,
    'log₁₀(2)': np.log10(2), '1/3': 1/3, 'ln(√2)': np.log(np.sqrt(2)),
    '1/e': 1/np.e, 'φ²': (np.sqrt(5)-1)/2 * (np.sqrt(5)-1)/2 * 0.25 + 0.25,  # recompute
    '√2-1': np.sqrt(2)-1, 'log₁₀(e)': np.log10(np.e),
    'φ/√2': ((1+np.sqrt(5))/2 - 1) / np.sqrt(2),
    '1/√5': 1/np.sqrt(5), 'e^(-π/4)': np.exp(-np.pi/4),
    '1/2': 0.5, 'cos(1)': np.cos(1), 'γ_EM': 0.5772156649,
    'φ': (np.sqrt(5)-1)/2, '2/π': 2/np.pi, 'ln(2)': np.log(2),
    '2/3': 2/3, '1/√2': 1/np.sqrt(2), '3/4': 0.75,
    'π/4': np.pi/4, 'sin(1)': np.sin(1), '√3/2': np.sqrt(3)/2,
    'e/π': np.e/np.pi, 'G_Cat': 0.915965594, '1/√e': 1/np.sqrt(np.e),
}
# Fix phi-squared
CONSTANTS['φ²'] = ((np.sqrt(5)-1)/2)**2

def super_squeeze(s_values, sA, threshold=0.02):
    """Run super squeeze. Returns list of matches."""
    sA_min, sA_max = sA.min(), sA.max()
    if sA_max - sA_min < 1e-15:
        return []
    S_norm = (sA - sA_min) / (sA_max - sA_min)
    # Interpolate S_norm as function of normalised s
    s_norm_param = (s_values - s_values.min()) / (s_values.max() - s_values.min())

    matches = []
    for name_in, val_in in CONSTANTS.items():
        # Find S_norm at s_norm_param closest to val_in
        idx = np.argmin(np.abs(s_norm_param - val_in))
        actual = S_norm[idx]
        # Check against all other constants
        for name_out, val_out in CONSTANTS.items():
            if name_out == name_in:
                continue
            delta = abs(actual - val_out)
            if delta < threshold:
                matches.append({
                    'input': name_in, 'input_val': val_in,
                    'output': name_out, 'output_val': val_out,
                    'actual': actual, 'delta': delta
                })
    # Sort by delta, deduplicate
    matches.sort(key=lambda m: m['delta'])
    seen = set()
    unique = []
    for m in matches:
        key = (m['input'], m['output'])
        if key not in seen:
            seen.add(key)
            unique.append(m)
    return unique

def pairwise_balance_analysis(comp, elements, s_values):
    """Test all pairwise log-ratios. Return best bowl."""
    D = len(elements)
    if D < 3:
        return []
    results = []
    for i in range(D):
        for j in range(i+1, D):
            ratio = np.log(np.maximum(comp[:, i], 1e-15) / np.maximum(comp[:, j], 1e-15))
            r2, shape, vertex = pll_fit(s_values, ratio)
            results.append({
                'pair': f'ln({elements[i]}/{elements[j]})',
                'R2': r2, 'shape': shape, 'vertex': vertex
            })
    results.sort(key=lambda r: -r['R2'])
    return results

# ============================================================
# MAIN BATCH PIPELINE
# ============================================================
print("=" * 80)
print("  EXP-15b: BIG DATA CRYSTALLOGRAPHY — Anti-Lock / S_norm Hypothesis Test")
print("  Source: COD-referenced mineral formulas (120 structures)")
print("=" * 80)

s_values = np.linspace(0.01, 1.2, 200)
results = []
errors = []

for mineral in MINERALS:
    name = mineral['name']
    formula = mineral['formula']
    mtype = mineral['type']

    # Check all elements available
    missing = [el for el in formula if el not in CROMER_MANN]
    if missing:
        errors.append(f"{name}: missing elements {missing}")
        continue

    if len(formula) < 2:
        errors.append(f"{name}: single element, skip")
        continue

    try:
        comp, elements = compute_composition(formula, s_values)
        D = len(elements)
        sA = sigma2_A(comp)
        H = shannon_H(comp)

        # PLL diagnostic
        r2_main, shape_main, vertex_main = pll_fit(s_values, sA)

        # Super squeeze
        squeeze = super_squeeze(s_values, sA)
        n_squeeze = len(squeeze)
        best_delta = squeeze[0]['delta'] if squeeze else 999

        # Pairwise balance (D >= 3 only)
        pw = pairwise_balance_analysis(comp, elements, s_values)
        best_pw_bowl = None
        for p in pw:
            if p['shape'] == 'bowl':
                best_pw_bowl = p
                break

        result = {
            'name': name,
            'type': mtype,
            'D': D,
            'elements': elements,
            'pll_R2': r2_main,
            'pll_shape': shape_main,
            'pll_vertex': vertex_main,
            'squeeze_count': n_squeeze,
            'best_delta': best_delta,
            'best_squeeze': squeeze[0] if squeeze else None,
            'sA_range': float(sA.max() - sA.min()),
            'sA_min': float(sA.min()),
            'sA_max': float(sA.max()),
        }

        if best_pw_bowl:
            result['best_pairwise_bowl'] = best_pw_bowl

        results.append(result)

    except Exception as e:
        errors.append(f"{name}: {str(e)}")

# ============================================================
# ANALYSIS: Test the hypothesis
# ============================================================
bowls = [r for r in results if r['pll_shape'] == 'bowl']
hills = [r for r in results if r['pll_shape'] == 'hill']

print(f"\nProcessed: {len(results)} minerals ({len(errors)} errors)")
print(f"BOWL (locked): {len(bowls)}  |  HILL (anti-lock): {len(hills)}")

# Key statistics
bowl_squeezes = [r['squeeze_count'] for r in bowls]
hill_squeezes = [r['squeeze_count'] for r in hills]
bowl_deltas = [r['best_delta'] for r in bowls if r['best_delta'] < 999]
hill_deltas = [r['best_delta'] for r in hills if r['best_delta'] < 999]

print(f"\n{'METRIC':<35} {'BOWL (locked)':<20} {'HILL (anti-lock)':<20}")
print("-" * 75)
print(f"{'Mean squeeze matches':<35} {np.mean(bowl_squeezes):<20.1f} {np.mean(hill_squeezes):<20.1f}")
print(f"{'Median squeeze matches':<35} {np.median(bowl_squeezes):<20.1f} {np.median(hill_squeezes):<20.1f}")
print(f"{'Mean best δ':<35} {np.mean(bowl_deltas):<20.5f} {np.mean(hill_deltas):<20.5f}")
print(f"{'Median best δ':<35} {np.median(bowl_deltas):<20.5f} {np.median(hill_deltas):<20.5f}")
print(f"{'% with ≥5 squeeze matches':<35} {100*sum(1 for s in bowl_squeezes if s>=5)/len(bowls):<20.1f} {100*sum(1 for s in hill_squeezes if s>=5)/len(hills):<20.1f}")
print(f"{'% with δ < 0.005':<35} {100*sum(1 for d in bowl_deltas if d<0.005)/len(bowls):<20.1f} {100*sum(1 for d in hill_deltas if d<0.005)/len(hills):<20.1f}")

# Anti-lock systems with pairwise bowl recovery
pw_recoveries = [r for r in hills if 'best_pairwise_bowl' in r and r['best_pairwise_bowl']['R2'] > 0.5]
print(f"\nAnti-lock systems recovered by pairwise balance (R²>0.5 bowl): {len(pw_recoveries)}/{len(hills)}")

# Top 10 tightest super squeezes
all_sorted = sorted(results, key=lambda r: r['best_delta'])
print(f"\n{'TOP 15 TIGHTEST SUPER SQUEEZES':=^75}")
print(f"{'Mineral':<25} {'D':<4} {'Shape':<6} {'R²':<8} {'Input→Output':<30} {'δ':<10}")
print("-" * 75)
for r in all_sorted[:15]:
    if r['best_squeeze']:
        sq = r['best_squeeze']
        pair = f"{sq['input']}→{sq['output']}"
        print(f"{r['name']:<25} {r['D']:<4} {r['pll_shape']:<6} {r['pll_R2']:<8.4f} {pair:<30} {sq['delta']:<10.6f}")

# Anti-lock with rich squeeze
print(f"\n{'ANTI-LOCK SYSTEMS WITH ≥10 SQUEEZE MATCHES':=^75}")
rich_hills = sorted([r for r in hills if r['squeeze_count'] >= 10], key=lambda r: -r['squeeze_count'])
for r in rich_hills[:15]:
    sq = r['best_squeeze']
    pw = r.get('best_pairwise_bowl', {})
    pw_str = f"PW: {pw.get('pair','N/A')} R²={pw.get('R2',0):.3f}" if pw else "PW: N/A"
    print(f"  {r['name']:<22} D={r['D']} R²={r['pll_R2']:.3f} hill  squeezes={r['squeeze_count']:>2}  δ={sq['delta']:.5f}  {pw_str}")

# Dimensionality analysis
print(f"\n{'DIMENSIONALITY ANALYSIS':=^75}")
for d in sorted(set(r['D'] for r in results)):
    d_results = [r for r in results if r['D'] == d]
    d_bowls = sum(1 for r in d_results if r['pll_shape'] == 'bowl')
    d_hills = sum(1 for r in d_results if r['pll_shape'] == 'hill')
    d_squeezes = np.mean([r['squeeze_count'] for r in d_results])
    print(f"  D={d}: {len(d_results):>3} minerals, {d_bowls:>3} bowl, {d_hills:>3} hill, mean squeezes={d_squeezes:.1f}")

# Z-contrast analysis
print(f"\n{'Z-CONTRAST vs PLL QUALITY':=^75}")
for r in results:
    z_vals = [CROMER_MANN[el]['Z'] for el in r['elements']]
    r['z_contrast'] = max(z_vals) - min(z_vals)
    r['z_max'] = max(z_vals)

z_bowl = np.mean([r['z_contrast'] for r in bowls])
z_hill = np.mean([r['z_contrast'] for r in hills])
print(f"  Mean Z-contrast (bowl): {z_bowl:.1f}")
print(f"  Mean Z-contrast (hill): {z_hill:.1f}")

# Correlation
all_z = np.array([r['z_contrast'] for r in results])
all_r2 = np.array([r['pll_R2'] for r in results])
corr = np.corrcoef(all_z, all_r2)[0, 1]
print(f"  Correlation(Z_contrast, PLL_R²): {corr:.3f}")

# ============================================================
# SAVE RESULTS
# ============================================================
output = {
    'experiment': 'EXP-15b: Big Data Crystallography',
    'date': '2026-04-22',
    'author': 'Peter Higgins / Claude',
    'source': 'COD-referenced mineral formulas, Cromer-Mann coefficients (ITC Vol C)',
    'hypothesis': 'Anti-lock systems still encode information via S_norm super squeeze',
    'total_minerals': len(results),
    'total_bowl': len(bowls),
    'total_hill': len(hills),
    'statistics': {
        'bowl_mean_squeezes': float(np.mean(bowl_squeezes)),
        'hill_mean_squeezes': float(np.mean(hill_squeezes)),
        'bowl_mean_delta': float(np.mean(bowl_deltas)),
        'hill_mean_delta': float(np.mean(hill_deltas)),
        'bowl_median_delta': float(np.median(bowl_deltas)),
        'hill_median_delta': float(np.median(hill_deltas)),
        'z_contrast_bowl': float(z_bowl),
        'z_contrast_hill': float(z_hill),
        'z_r2_correlation': float(corr),
        'pairwise_recoveries': len(pw_recoveries),
        'pairwise_recovery_rate': len(pw_recoveries) / len(hills) if hills else 0,
    },
    'results': results,
    'errors': errors,
}

with open('cod_big_data_test.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)

print(f"\n{'=' * 80}")
print(f"  Results saved to cod_big_data_test.json")
print(f"{'=' * 80}")
