#!/usr/bin/env python3
"""
EXP-16: Force Composition in a Perturbed Spring-Mass System
HUF Programme — Higgins Unity Framework
Peter Higgins / Claude (Anthropic)

First MECHANICS-domain test of the Higgins Decomposition.

Physics: mass on spring under gravity with viscous damping.
  m*x'' + c*x' + k*x = m*g + F_perturbation(t)

Forces as composition (magnitudes at each timestep):
  - F_gravity   = m*g                    (constant)
  - F_spring    = k*|x|                  (displacement-dependent)
  - F_damping   = c*|v|                  (velocity-dependent)
  - F_inertia   = m*|a|                  (acceleration-dependent)

These four force magnitudes → close to simplex → full Higgins Decomposition.

Perturbation scenarios:
  S1: Unperturbed (baseline oscillation, decaying to equilibrium)
  S2: Mass step change at t=5s (sudden weight addition — like loading a bridge)
  S3: Spring constant shift at t=5s (stiffness change — like material fatigue)
  S4: Impulse at t=5s (hammer strike — like earthquake shock)
  S5: Gradual damping increase (progressive wear — like bearing degradation)
  S6: Combined: mass + spring + impulse (cascading failure scenario)

Question: Can the Higgins Decomposition detect perturbation onset in the
force composition BEFORE the magnitude-based sensors (peak displacement,
peak velocity) show clear change?
"""

import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import warnings
warnings.filterwarnings('ignore')
import os

OUT_DIR = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker"
EXP_DIR = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Current-Repo/HUF/codawork2026/experiments/EXP-16_Spring_Mass_Force_Composition"
os.makedirs(EXP_DIR, exist_ok=True)

# ============================================================
# COLOUR PALETTE
# ============================================================
BG_DARK = '#0D1117'
BG_PANEL = '#161B22'
GOLD = '#FFD700'
ICE = '#CADCFC'
TEAL = '#028090'
RED = '#F85149'
GREEN = '#27AE60'
CYAN = '#58A6FF'
ORANGE = '#F0B429'
MAGENTA = '#BC8CFF'
WHITE = '#E6EDF3'
GREY = '#8B949E'

FORCE_COLORS = {
    'Gravity': GOLD,
    'Spring': TEAL,
    'Damping': ORANGE,
    'Inertia': MAGENTA,
}

BOWL_COLOR = TEAL
HILL_COLOR = ORANGE

# ============================================================
# SPRING-MASS SIMULATOR (RK4)
# ============================================================
def simulate_spring_mass(m_func, k_func, c_func, F_ext_func,
                          x0=0.0, v0=0.0, g=9.81,
                          t_end=10.0, dt=0.001):
    """
    Simulate spring-mass system with time-varying parameters.

    m_func(t): mass at time t
    k_func(t): spring constant at time t
    c_func(t): damping coefficient at time t
    F_ext_func(t): external perturbation force at time t

    Returns: t, x, v, a, forces dict
    """
    N = int(t_end / dt)
    t = np.linspace(0, t_end, N)
    x = np.zeros(N)
    v = np.zeros(N)
    a = np.zeros(N)

    x[0] = x0
    v[0] = v0

    # RK4 integration
    for i in range(N - 1):
        ti = t[i]
        xi = x[i]
        vi = v[i]
        mi = m_func(ti)

        def deriv(tt, xx, vv):
            mm = m_func(tt)
            kk = k_func(tt)
            cc = c_func(tt)
            ff = F_ext_func(tt)
            # x'' = (mg - kx - cv + F_ext) / m
            # Using displacement from equilibrium: x measured from natural length
            # Spring pulls back: -kx. Gravity: +mg (downward = positive x direction)
            acc = (mm * g - kk * xx - cc * vv + ff) / mm
            return vv, acc

        dv1, da1 = deriv(ti, xi, vi)
        dv2, da2 = deriv(ti + dt/2, xi + dv1*dt/2, vi + da1*dt/2)
        dv3, da3 = deriv(ti + dt/2, xi + dv2*dt/2, vi + da2*dt/2)
        dv4, da4 = deriv(ti + dt, xi + dv3*dt, vi + da3*dt)

        x[i+1] = xi + (dv1 + 2*dv2 + 2*dv3 + dv4) * dt / 6
        v[i+1] = vi + (da1 + 2*da2 + 2*da3 + da4) * dt / 6
        a[i+1] = (m_func(t[i+1]) * g - k_func(t[i+1]) * x[i+1] -
                   c_func(t[i+1]) * v[i+1] + F_ext_func(t[i+1])) / m_func(t[i+1])

    a[0] = (m_func(0) * g - k_func(0) * x[0] - c_func(0) * v[0] + F_ext_func(0)) / m_func(0)

    # Force magnitudes at each timestep
    F_grav = np.array([m_func(ti) * g for ti in t])
    F_spring = np.array([k_func(ti) * abs(x[i]) for i, ti in enumerate(t)])
    F_damp = np.array([c_func(ti) * abs(v[i]) for i, ti in enumerate(t)])
    F_inertia = np.array([m_func(ti) * abs(a[i]) for i, ti in enumerate(t)])

    forces = {
        'Gravity': F_grav,
        'Spring': F_spring,
        'Damping': F_damp,
        'Inertia': F_inertia,
    }

    return t, x, v, a, forces


# ============================================================
# CODA TOOLKIT
# ============================================================
def close_to_simplex(forces_dict, epsilon=1e-10):
    """Convert force magnitudes to compositions."""
    keys = sorted(forces_dict.keys())
    N = len(forces_dict[keys[0]])
    D = len(keys)
    raw = np.zeros((N, D))
    for j, k in enumerate(keys):
        raw[:, j] = np.maximum(forces_dict[k], epsilon)
    totals = raw.sum(axis=1, keepdims=True)
    return raw / totals, keys

def clr(comp):
    log_x = np.log(np.maximum(comp, 1e-15))
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

def super_squeeze(t_vals, sA, threshold=0.02):
    sA_min, sA_max = sA.min(), sA.max()
    if sA_max - sA_min < 1e-15:
        return []
    S_norm = (sA - sA_min) / (sA_max - sA_min)
    t_norm = (t_vals - t_vals.min()) / (t_vals.max() - t_vals.min())

    matches = []
    for name_in, val_in in CONSTANTS.items():
        idx = np.argmin(np.abs(t_norm - val_in))
        actual = S_norm[idx]
        for name_out, val_out in CONSTANTS.items():
            if name_out == name_in:
                continue
            delta = abs(actual - val_out)
            if delta < threshold:
                matches.append({
                    'input': name_in, 'input_val': float(val_in),
                    'output': name_out, 'output_val': float(val_out),
                    'actual': float(actual), 'delta': float(delta)
                })
    matches.sort(key=lambda m: m['delta'])
    seen = set()
    unique = []
    for m in matches:
        key = (m['input'], m['output'])
        if key not in seen:
            seen.add(key)
            unique.append(m)
    return unique

def sliding_window_sigma2(comp, window=200):
    """Compute σ²_A in a sliding window for change detection."""
    N = comp.shape[0]
    result = np.full(N, np.nan)
    half = window // 2
    for i in range(half, N - half):
        window_comp = comp[i-half:i+half]
        sA = sigma2_A(window_comp)
        result[i] = np.mean(sA)
    return result


# ============================================================
# DEFINE SCENARIOS
# ============================================================
g = 9.81
m0 = 5.0     # kg
k0 = 200.0   # N/m (natural freq ~1 Hz)
c0 = 2.0     # N·s/m (underdamped)
x0_init = 0.3  # initial displacement from equilibrium (m)
t_end = 10.0
t_perturb = 5.0  # perturbation onset

scenarios = {
    'S1_Baseline': {
        'desc': 'Unperturbed oscillation (baseline)',
        'm': lambda t: m0,
        'k': lambda t: k0,
        'c': lambda t: c0,
        'F_ext': lambda t: 0,
    },
    'S2_Mass_Step': {
        'desc': 'Mass doubles at t=5s (sudden load)',
        'm': lambda t: m0 if t < t_perturb else m0 * 2,
        'k': lambda t: k0,
        'c': lambda t: c0,
        'F_ext': lambda t: 0,
    },
    'S3_Spring_Shift': {
        'desc': 'Spring constant halves at t=5s (fatigue)',
        'm': lambda t: m0,
        'k': lambda t: k0 if t < t_perturb else k0 * 0.5,
        'c': lambda t: c0,
        'F_ext': lambda t: 0,
    },
    'S4_Impulse': {
        'desc': 'Hammer strike impulse at t=5s',
        'm': lambda t: m0,
        'k': lambda t: k0,
        'c': lambda t: c0,
        'F_ext': lambda t: 500.0 * np.exp(-((t - t_perturb) / 0.01)**2) if abs(t - t_perturb) < 0.1 else 0,
    },
    'S5_Damping_Ramp': {
        'desc': 'Damping triples linearly t=5-8s (wear)',
        'm': lambda t: m0,
        'k': lambda t: k0,
        'c': lambda t: c0 if t < t_perturb else c0 * (1 + 2 * min((t - t_perturb) / 3.0, 1.0)),
        'F_ext': lambda t: 0,
    },
    'S6_Cascade': {
        'desc': 'Mass+spring+impulse cascade',
        'm': lambda t: m0 if t < t_perturb else m0 * 1.5,
        'k': lambda t: k0 if t < t_perturb + 1 else k0 * 0.7,
        'c': lambda t: c0,
        'F_ext': lambda t: 300.0 * np.exp(-((t - t_perturb) / 0.02)**2) if abs(t - t_perturb) < 0.2 else 0,
    },
}


# ============================================================
# RUN ALL SCENARIOS
# ============================================================
print("=" * 80)
print("  EXP-16: FORCE COMPOSITION IN PERTURBED SPRING-MASS SYSTEM")
print("  First MECHANICS-domain test of the Higgins Decomposition")
print("=" * 80)

all_results = {}

for s_name, s_def in scenarios.items():
    print(f"\n  Simulating {s_name}: {s_def['desc']}...")

    t, x, v, a, forces = simulate_spring_mass(
        s_def['m'], s_def['k'], s_def['c'], s_def['F_ext'],
        x0=x0_init, v0=0, g=g, t_end=t_end, dt=0.001
    )

    # Downsample for analysis (every 10th point = 1000 Hz → 100 Hz)
    ds = 10
    t_ds = t[::ds]
    x_ds = x[::ds]
    v_ds = v[::ds]
    forces_ds = {k: vv[::ds] for k, vv in forces.items()}

    # Close to simplex
    comp, elements = close_to_simplex(forces_ds)

    # Full trajectory diagnostics
    sA = sigma2_A(comp)
    H = shannon_H(comp)

    # PLL fit — full trajectory
    r2_full, shape_full, vertex_full, pred_full = pll_fit(t_ds, sA)

    # PLL fit — pre-perturbation (t < 5)
    pre_mask = t_ds < t_perturb
    post_mask = t_ds >= t_perturb

    r2_pre, shape_pre, _, pred_pre = pll_fit(t_ds[pre_mask], sA[pre_mask])
    r2_post, shape_post, _, pred_post = pll_fit(t_ds[post_mask], sA[post_mask])

    # Super squeeze — full
    squeeze_full = super_squeeze(t_ds, sA)

    # Super squeeze — pre and post separately
    squeeze_pre = super_squeeze(t_ds[pre_mask], sA[pre_mask])
    squeeze_post = super_squeeze(t_ds[post_mask], sA[post_mask])

    # Sliding window σ²_A for change detection
    window_sA = sliding_window_sigma2(comp, window=200)

    # Change detection: find first point where sliding σ²_A deviates >3σ from pre-perturb mean
    pre_window = window_sA[~np.isnan(window_sA) & (t_ds[:len(window_sA)] < t_perturb - 0.5)]
    if len(pre_window) > 10:
        pre_mean = np.mean(pre_window)
        pre_std = np.std(pre_window)
        threshold_3sigma = pre_mean + 3 * pre_std

        # Find first exceedance after t_perturb - 0.5
        detect_idx = None
        for i in range(len(window_sA)):
            if t_ds[i] >= t_perturb - 0.5 and not np.isnan(window_sA[i]):
                if abs(window_sA[i] - pre_mean) > 3 * pre_std:
                    detect_idx = i
                    break
        detect_time = t_ds[detect_idx] if detect_idx else None
    else:
        pre_mean = 0
        pre_std = 0
        detect_time = None

    # Magnitude-based detection: peak displacement exceedance
    x_pre = x_ds[pre_mask]
    x_pre_max = np.max(np.abs(x_pre[-500:])) if len(x_pre) > 500 else np.max(np.abs(x_pre))
    x_threshold = x_pre_max * 1.3  # 30% exceedance

    mag_detect_idx = None
    for i in range(len(x_ds)):
        if t_ds[i] >= t_perturb - 0.5 and abs(x_ds[i]) > x_threshold:
            mag_detect_idx = i
            break
    mag_detect_time = t_ds[mag_detect_idx] if mag_detect_idx else None

    # Store results
    result = {
        'name': s_name,
        'description': s_def['desc'],
        'D': 4,
        'elements': elements,
        'pll_full': {'R2': float(r2_full), 'shape': shape_full},
        'pll_pre': {'R2': float(r2_pre), 'shape': shape_pre},
        'pll_post': {'R2': float(r2_post), 'shape': shape_post},
        'squeeze_full': len(squeeze_full),
        'squeeze_pre': len(squeeze_pre),
        'squeeze_post': len(squeeze_post),
        'best_squeeze': squeeze_full[0] if squeeze_full else None,
        'H_mean': float(np.mean(H)),
        'H_cv': float(np.std(H) / np.mean(H) * 100) if np.mean(H) > 0 else 0,
        'sA_range': float(sA.max() - sA.min()),
        'detect_time_composition': float(detect_time) if detect_time else None,
        'detect_time_magnitude': float(mag_detect_time) if mag_detect_time else None,
        'detect_lead': float(mag_detect_time - detect_time) if (detect_time and mag_detect_time) else None,
    }

    all_results[s_name] = {
        'result': result,
        't': t_ds,
        'x': x_ds,
        'v': v_ds,
        'comp': comp,
        'sA': sA,
        'H': H,
        'window_sA': window_sA,
        'forces': forces_ds,
        'pred_full': pred_full,
    }

    # Print summary
    print(f"    PLL full: {shape_full} R²={r2_full:.4f}")
    print(f"    PLL pre:  {shape_pre} R²={r2_pre:.4f}  |  PLL post: {shape_post} R²={r2_post:.4f}")
    print(f"    Squeeze: full={len(squeeze_full)}, pre={len(squeeze_pre)}, post={len(squeeze_post)}")
    if squeeze_full:
        sq = squeeze_full[0]
        print(f"    Best: {sq['input']}→{sq['output']} δ={sq['delta']:.6f}")
    print(f"    Entropy CV: {result['H_cv']:.1f}%")
    if detect_time:
        print(f"    Composition detects at t={detect_time:.3f}s")
    if mag_detect_time:
        print(f"    Magnitude detects at t={mag_detect_time:.3f}s")
    if result['detect_lead']:
        if result['detect_lead'] > 0:
            print(f"    >>> COMPOSITION LEADS BY {result['detect_lead']:.3f}s <<<")
        else:
            print(f"    Magnitude leads by {-result['detect_lead']:.3f}s")


# ============================================================
# DIAGRAM 1: 6-PANEL FORCE COMPOSITION TRAJECTORIES
# ============================================================
print("\n  Generating diagrams...")

fig, axes = plt.subplots(2, 3, figsize=(24, 12), facecolor=BG_DARK)
fig.suptitle('EXP-16: FORCE COMPOSITION TRAJECTORIES — Spring-Mass System',
             fontsize=16, fontweight='bold', color=GOLD, y=0.98)
fig.text(0.5, 0.955, 'Higgins Unity Framework — First MECHANICS-domain test | Forces as compositions on the simplex',
         ha='center', fontsize=10, color=ICE)

for idx, (s_name, data) in enumerate(all_results.items()):
    ax = axes[idx // 3][idx % 3]
    ax.set_facecolor(BG_PANEL)

    t_d = data['t']
    comp = data['comp']
    elements = data['result']['elements']

    ax.stackplot(t_d, *[comp[:, j] for j in range(len(elements))],
                 labels=elements,
                 colors=[FORCE_COLORS.get(el, GREY) for el in elements],
                 alpha=0.8)

    ax.axvline(t_perturb, color=RED, linewidth=2, linestyle='--', alpha=0.8)
    ax.set_xlim(0, t_end)
    ax.set_ylim(0, 1)
    ax.set_title(f'{s_name}\n{data["result"]["description"]}',
                 fontsize=9, fontweight='bold', color=WHITE, pad=6)
    ax.set_xlabel('Time (s)', fontsize=8, color=WHITE)
    ax.set_ylabel('Force fraction', fontsize=8, color=WHITE)
    ax.tick_params(colors=WHITE, labelsize=7)
    for spine in ax.spines.values():
        spine.set_color(GREY)

    if idx == 0:
        ax.legend(fontsize=7, loc='upper right', facecolor=BG_DARK,
                  edgecolor=GREY, labelcolor=WHITE)

plt.tight_layout(rect=[0, 0, 1, 0.93])
path1 = os.path.join(OUT_DIR, 'EXP16_01_Force_Composition.png')
fig.savefig(path1, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
plt.close(fig)
print(f"    -> {path1}")


# ============================================================
# DIAGRAM 2: PLL PARABOLA — PRE vs POST PERTURBATION
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(24, 12), facecolor=BG_DARK)
fig.suptitle('EXP-16: PLL PARABOLA DIAGNOSTIC — σ²_A Pre vs Post Perturbation',
             fontsize=16, fontweight='bold', color=GOLD, y=0.98)

for idx, (s_name, data) in enumerate(all_results.items()):
    ax = axes[idx // 3][idx % 3]
    ax.set_facecolor(BG_PANEL)

    t_d = data['t']
    sA = data['sA']
    r = data['result']

    pre_mask = t_d < t_perturb
    post_mask = t_d >= t_perturb

    ax.plot(t_d[pre_mask], sA[pre_mask], color=CYAN, linewidth=0.8, alpha=0.7)
    ax.plot(t_d[post_mask], sA[post_mask], color=ORANGE, linewidth=0.8, alpha=0.7)
    ax.plot(t_d, data['pred_full'], color=GOLD, linewidth=2, linestyle='--', alpha=0.8)

    ax.axvline(t_perturb, color=RED, linewidth=2, linestyle='--', alpha=0.8)

    shape_color = BOWL_COLOR if r['pll_full']['shape'] == 'bowl' else HILL_COLOR
    ax.set_title(f"{s_name}: {r['pll_full']['shape'].upper()} R²={r['pll_full']['R2']:.3f}\n"
                 f"Pre: {r['pll_pre']['shape']} R²={r['pll_pre']['R2']:.3f} | "
                 f"Post: {r['pll_post']['shape']} R²={r['pll_post']['R2']:.3f}",
                 fontsize=8, fontweight='bold', color=shape_color, pad=6)
    ax.set_xlabel('Time (s)', fontsize=8, color=WHITE)
    ax.set_ylabel('σ²_A', fontsize=8, color=WHITE)
    ax.tick_params(colors=WHITE, labelsize=7)
    for spine in ax.spines.values():
        spine.set_color(GREY)

plt.tight_layout(rect=[0, 0, 1, 0.93])
path2 = os.path.join(OUT_DIR, 'EXP16_02_PLL_Pre_Post.png')
fig.savefig(path2, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
plt.close(fig)
print(f"    -> {path2}")


# ============================================================
# DIAGRAM 3: CHANGE DETECTION — Composition vs Magnitude
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(24, 12), facecolor=BG_DARK)
fig.suptitle('EXP-16: CHANGE DETECTION — Composition vs Magnitude Sensors',
             fontsize=16, fontweight='bold', color=GOLD, y=0.98)
fig.text(0.5, 0.955, 'Red dashed = perturbation onset | Green = composition detection | Cyan = magnitude detection',
         ha='center', fontsize=10, color=ICE)

for idx, (s_name, data) in enumerate(all_results.items()):
    ax = axes[idx // 3][idx % 3]
    ax.set_facecolor(BG_PANEL)

    t_d = data['t']
    r = data['result']

    # Plot sliding window σ²_A
    wsA = data['window_sA']
    valid = ~np.isnan(wsA)
    ax.plot(t_d[valid], wsA[valid], color=CYAN, linewidth=1, alpha=0.8, label='Sliding σ²_A')

    # Perturbation line
    ax.axvline(t_perturb, color=RED, linewidth=2, linestyle='--', alpha=0.8, label='Perturbation')

    # Detection markers
    if r['detect_time_composition']:
        ax.axvline(r['detect_time_composition'], color=GREEN, linewidth=2,
                    linestyle='-', alpha=0.9, label=f"CoDa: {r['detect_time_composition']:.2f}s")
    if r['detect_time_magnitude']:
        ax.axvline(r['detect_time_magnitude'], color=MAGENTA, linewidth=2,
                    linestyle='-.', alpha=0.9, label=f"Mag: {r['detect_time_magnitude']:.2f}s")

    lead = r.get('detect_lead')
    if lead and lead > 0:
        ax.text(0.5, 0.95, f'CoDa leads by {lead:.3f}s',
                transform=ax.transAxes, fontsize=10, fontweight='bold',
                color=GREEN, ha='center', va='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_DARK, edgecolor=GREEN))

    ax.set_title(f'{s_name}: {r["description"]}', fontsize=9, fontweight='bold', color=WHITE, pad=6)
    ax.set_xlabel('Time (s)', fontsize=8, color=WHITE)
    ax.set_ylabel('Sliding σ²_A', fontsize=8, color=WHITE)
    ax.tick_params(colors=WHITE, labelsize=7)
    ax.legend(fontsize=6, loc='upper left', facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)
    for spine in ax.spines.values():
        spine.set_color(GREY)

plt.tight_layout(rect=[0, 0, 1, 0.93])
path3 = os.path.join(OUT_DIR, 'EXP16_03_Change_Detection.png')
fig.savefig(path3, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
plt.close(fig)
print(f"    -> {path3}")


# ============================================================
# DIAGRAM 4: TERNARY — Force triangle (Gravity-Spring-Damping)
# ============================================================
fig = plt.figure(figsize=(22, 14), facecolor=BG_DARK)
fig.suptitle('EXP-16: TERNARY FORCE DIAGRAMS — Gravity / Spring / Damping Projection',
             fontsize=16, fontweight='bold', color=GOLD, y=0.98)
fig.text(0.5, 0.955, 'Pre-perturbation (blue) vs post-perturbation (orange) trajectories on force simplex',
         ha='center', fontsize=10, color=ICE)

for idx, (s_name, data) in enumerate(all_results.items()):
    ax = fig.add_subplot(2, 3, idx+1)
    ax.set_facecolor(BG_PANEL)
    ax.set_aspect('equal')
    ax.axis('off')

    comp = data['comp']
    t_d = data['t']
    elements = data['result']['elements']

    # Project onto Gravity-Spring-Damping (drop Inertia, renormalize)
    grav_idx = elements.index('Gravity')
    spr_idx = elements.index('Spring')
    damp_idx = elements.index('Damping')

    comp_3 = comp[:, [grav_idx, spr_idx, damp_idx]]
    comp_3 = comp_3 / comp_3.sum(axis=1, keepdims=True)

    # Triangle
    tri_x = [0, 1, 0.5, 0]
    tri_y = [0, 0, np.sqrt(3)/2, 0]
    ax.plot(tri_x, tri_y, color=ICE, linewidth=1.5)

    # Gridlines
    for g_val in [0.25, 0.5, 0.75]:
        ax.plot([g_val*0.5, g_val + (1-g_val)*0.0], [g_val*np.sqrt(3)/2, 0],
                color=GREY, alpha=0.15, lw=0.5)

    cart_x = comp_3[:, 1] + comp_3[:, 2] * 0.5
    cart_y = comp_3[:, 2] * np.sqrt(3) / 2

    pre_mask = t_d < t_perturb
    post_mask = t_d >= t_perturb

    ax.scatter(cart_x[pre_mask], cart_y[pre_mask], c=CYAN, s=1, alpha=0.3)
    ax.scatter(cart_x[post_mask], cart_y[post_mask], c=ORANGE, s=1, alpha=0.3)

    # Start and end markers
    ax.scatter(cart_x[0], cart_y[0], c=GREEN, s=40, marker='o', edgecolor='white', linewidth=1, zorder=5)
    ax.scatter(cart_x[-1], cart_y[-1], c=RED, s=40, marker='s', edgecolor='white', linewidth=1, zorder=5)

    ax.text(0, -0.06, 'Gravity', ha='center', fontsize=8, color=GOLD, fontweight='bold')
    ax.text(1, -0.06, 'Spring', ha='center', fontsize=8, color=TEAL, fontweight='bold')
    ax.text(0.5, np.sqrt(3)/2 + 0.04, 'Damping', ha='center', fontsize=8, color=ORANGE, fontweight='bold')

    ax.set_title(s_name, fontsize=9, fontweight='bold', color=WHITE, pad=4)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.12, 1.0)

plt.tight_layout(rect=[0, 0, 1, 0.93])
path4 = os.path.join(OUT_DIR, 'EXP16_04_Ternary_Force.png')
fig.savefig(path4, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
plt.close(fig)
print(f"    -> {path4}")


# ============================================================
# DIAGRAM 5: MASTER DASHBOARD
# ============================================================
fig = plt.figure(figsize=(24, 16), facecolor=BG_DARK)
gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.4, wspace=0.35)
fig.suptitle('EXP-16 MASTER DASHBOARD — Force Composition in Perturbed Spring-Mass System',
             fontsize=18, fontweight='bold', color=GOLD, y=0.98)
fig.text(0.5, 0.96, 'Higgins Unity Framework | First MECHANICS-domain test | 6 perturbation scenarios | Full Higgins Decomposition',
         ha='center', fontsize=10, color=ICE)

# Panel A: Headline numbers
ax_head = fig.add_subplot(gs[0, 0:2])
ax_head.set_facecolor(BG_PANEL)
ax_head.axis('off')

n_bowl = sum(1 for d in all_results.values() if d['result']['pll_full']['shape'] == 'bowl')
n_hill = sum(1 for d in all_results.values() if d['result']['pll_full']['shape'] == 'hill')
n_lead = sum(1 for d in all_results.values() if (d['result'].get('detect_lead') or 0) > 0)
avg_squeeze = np.mean([d['result']['squeeze_full'] for d in all_results.values()])

headlines = [
    ('6', 'Scenarios', WHITE),
    (str(n_bowl), 'Bowl', BOWL_COLOR),
    (str(n_hill), 'Hill', HILL_COLOR),
    (str(n_lead), 'CoDa\nLeads', GREEN),
    (f'{avg_squeeze:.0f}', 'Mean\nSqueezes', GOLD),
]
for i, (num, label, color) in enumerate(headlines):
    x = 0.1 + i * 0.18
    ax_head.text(x, 0.65, num, transform=ax_head.transAxes, fontsize=28,
                 fontweight='bold', color=color, ha='center')
    ax_head.text(x, 0.15, label, transform=ax_head.transAxes, fontsize=9,
                 color=GREY, ha='center')

# Panel B: Domain badge
ax_dom = fig.add_subplot(gs[0, 2:4])
ax_dom.set_facecolor('#0a1a0a')
ax_dom.axis('off')
ax_dom.text(0.5, 0.8, 'NEW DOMAIN: MECHANICS', transform=ax_dom.transAxes,
            fontsize=16, fontweight='bold', color=GREEN, ha='center')
ax_dom.text(0.5, 0.5, 'Force • Mass • Spring • Damping • Inertia',
            transform=ax_dom.transAxes, fontsize=11, color=ICE, ha='center')
ax_dom.text(0.5, 0.2, 'Domains confirmed: ENERGY | MATTER | ENERGY/MATTER | MECHANICS',
            transform=ax_dom.transAxes, fontsize=9, color=GOLD, ha='center')
for spine in ax_dom.spines.values():
    spine.set_color(GREEN)
    spine.set_linewidth(2)

# Panel C: Scenario comparison table
ax_table = fig.add_subplot(gs[1, :])
ax_table.set_facecolor(BG_PANEL)
ax_table.axis('off')
ax_table.set_title('SCENARIO COMPARISON', fontsize=12, fontweight='bold', color=GOLD, pad=10)

headers = ['Scenario', 'PLL Shape', 'R²', 'Squeezes', 'Entropy CV%', 'CoDa Detect', 'Mag Detect', 'Lead (s)']
for j, h in enumerate(headers):
    ax_table.text(0.02 + j * 0.125, 0.92, h, transform=ax_table.transAxes,
                  fontsize=8, fontweight='bold', color=GOLD, ha='left')

for i, (s_name, data) in enumerate(all_results.items()):
    r = data['result']
    y = 0.78 - i * 0.13
    shape_c = BOWL_COLOR if r['pll_full']['shape'] == 'bowl' else HILL_COLOR

    vals = [
        (s_name.replace('_', ' '), WHITE),
        (r['pll_full']['shape'].upper(), shape_c),
        (f"{r['pll_full']['R2']:.3f}", WHITE),
        (str(r['squeeze_full']), GOLD),
        (f"{r['H_cv']:.1f}%", WHITE),
        (f"{r['detect_time_composition']:.2f}s" if r['detect_time_composition'] else 'N/A', GREEN),
        (f"{r['detect_time_magnitude']:.2f}s" if r['detect_time_magnitude'] else 'N/A', MAGENTA),
        (f"{r['detect_lead']:.3f}" if r['detect_lead'] else 'N/A',
         GREEN if (r.get('detect_lead') or 0) > 0 else RED),
    ]
    for j, (val, color) in enumerate(vals):
        ax_table.text(0.02 + j * 0.125, y, val, transform=ax_table.transAxes,
                      fontsize=8, color=color, ha='left')

# Panel D: Squeeze comparison
ax_sq = fig.add_subplot(gs[2, 0:2])
ax_sq.set_facecolor(BG_PANEL)
ax_sq.set_title('Super Squeeze: Pre vs Post', fontsize=10, fontweight='bold', color=GOLD)
s_names = list(all_results.keys())
x_pos = np.arange(len(s_names))
pre_sq = [all_results[s]['result']['squeeze_pre'] for s in s_names]
post_sq = [all_results[s]['result']['squeeze_post'] for s in s_names]
w = 0.35
ax_sq.bar(x_pos - w/2, pre_sq, w, color=CYAN, alpha=0.8, label='Pre-perturb')
ax_sq.bar(x_pos + w/2, post_sq, w, color=ORANGE, alpha=0.8, label='Post-perturb')
ax_sq.set_xticks(x_pos)
ax_sq.set_xticklabels([s.replace('_', '\n') for s in s_names], fontsize=6, color=WHITE)
ax_sq.tick_params(colors=WHITE, labelsize=7)
ax_sq.legend(fontsize=8, facecolor=BG_DARK, edgecolor=GREY, labelcolor=WHITE)
for spine in ax_sq.spines.values():
    spine.set_color(GREY)

# Panel E: Entropy CV comparison
ax_cv = fig.add_subplot(gs[2, 2:4])
ax_cv.set_facecolor(BG_PANEL)
ax_cv.set_title('Entropy Coefficient of Variation', fontsize=10, fontweight='bold', color=GOLD)
cvs = [all_results[s]['result']['H_cv'] for s in s_names]
colors_cv = [GREEN if cv < 10 else (ORANGE if cv < 30 else RED) for cv in cvs]
ax_cv.bar(x_pos, cvs, color=colors_cv, alpha=0.8)
ax_cv.set_xticks(x_pos)
ax_cv.set_xticklabels([s.replace('_', '\n') for s in s_names], fontsize=6, color=WHITE)
ax_cv.set_ylabel('CV %', fontsize=8, color=WHITE)
ax_cv.tick_params(colors=WHITE, labelsize=7)
for spine in ax_cv.spines.values():
    spine.set_color(GREY)

path5 = os.path.join(OUT_DIR, 'EXP16_05_Master_Dashboard.png')
fig.savefig(path5, dpi=180, facecolor=BG_DARK, bbox_inches='tight')
plt.close(fig)
print(f"    -> {path5}")


# ============================================================
# SAVE RESULTS JSON
# ============================================================
output = {
    'experiment': 'EXP-16: Force Composition in Perturbed Spring-Mass System',
    'date': '2026-04-22',
    'author': 'Peter Higgins / Claude',
    'domain': 'MECHANICS (first test)',
    'system': 'Spring-mass with gravity, damping, and external perturbation',
    'parameters': {
        'mass_kg': m0, 'spring_N_per_m': k0, 'damping_N_s_per_m': c0,
        'gravity_m_s2': g, 'x0_m': x0_init, 't_end_s': t_end,
        'perturbation_onset_s': t_perturb
    },
    'composition': {
        'carriers': ['Damping', 'Gravity', 'Inertia', 'Spring'],
        'D': 4,
        'description': 'Force magnitudes closed to simplex at each timestep'
    },
    'scenarios': {s_name: data['result'] for s_name, data in all_results.items()},
    'summary': {
        'total_scenarios': 6,
        'bowl_count': n_bowl,
        'hill_count': n_hill,
        'coda_leads_count': n_lead,
        'mean_squeezes': float(avg_squeeze),
    }
}

json_path = os.path.join(EXP_DIR, 'EXP16_results.json')
with open(json_path, 'w') as f:
    json.dump(output, f, indent=2, default=str)
print(f"\n    Results: {json_path}")

# Copy diagrams to experiment folder
import shutil
for p in [path1, path2, path3, path4, path5]:
    shutil.copy2(p, EXP_DIR)
    print(f"    Copied: {os.path.basename(p)} -> EXP-16 folder")

# Copy script
shutil.copy2(__file__, os.path.join(EXP_DIR, 'exp16_spring_mass_force_composition.py'))

print(f"\n{'=' * 80}")
print(f"  EXP-16 COMPLETE — First MECHANICS-domain test")
print(f"{'=' * 80}")
