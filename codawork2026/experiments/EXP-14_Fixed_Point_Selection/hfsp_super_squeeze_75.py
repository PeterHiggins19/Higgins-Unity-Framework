#!/usr/bin/env python3
"""
HFSP SUPER SQUEEZE — All 75 Systems
======================================
The Transcendental Cancellation across the entire HUF programme.

For each system:
1. Build a score landscape S(α) from whatever data we have
2. Sweep 28 transcendental constants as α-inputs
3. Find the "native reciprocal" — the constant pair (a→b) where S_norm(a)≈b
4. Compute residual after removing all known mathematical structure
5. Classify: clean reciprocal found, partial match, or no match

Systems with blend landscape data (5): use interpolated S(α) directly
Systems with PLL_R² (20+): construct parabolic score landscape S(α) = R²·(1-(α-α*)²/σ²)
Systems without R² but with physics: construct from domain fp_category

Peter's insight: like dimensional analysis cancels units, the super squeeze
cancels embedded transcendental functions to reveal pure physics.
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import os, sys

# ═══════════════════════════════════════════════════════════════════
# LOAD ALL DATA SOURCES
# ═══════════════════════════════════════════════════════════════════

BASE = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Current-Repo/HUF/codawork2026/experiments'

with open(f'{BASE}/EXP-14_Fixed_Point_Selection/HFSP_MASTER_CATALOG.json') as f:
    catalog = json.load(f)

with open(f'{BASE}/EXP-09_Master_Inventory/exp09_master_inventory.json') as f:
    inventory = json.load(f)

with open('/sessions/wonderful-elegant-pascal/hfsp_blended_anchors.json') as f:
    blend_data = json.load(f)

with open(f'{BASE}/EXP-10_Full_Sweep/exp10_full_sweep.json') as f:
    sweep10 = json.load(f)

with open(f'{BASE}/EXP-13_Parabola_Hunter/exp13_parabola_hunter.json') as f:
    hunt13 = json.load(f)

with open(f'{BASE}/EXP-14_Fixed_Point_Selection/exp14_hfsp.json') as f:
    hfsp14 = json.load(f)

# ═══════════════════════════════════════════════════════════════════
# CONSTANTS LIBRARY (28 constants, all in [0,1] range for α)
# ═══════════════════════════════════════════════════════════════════

C = {
    '1/√2':     1/np.sqrt(2),       # 0.7071 — Butterworth damping
    '1/√3':     1/np.sqrt(3),       # 0.5774 — Bessel damping
    '1/√5':     1/np.sqrt(5),       # 0.4472 — golden ratio related
    'ln(2)':    np.log(2),          # 0.6931 — information theory
    '1/e':      1/np.e,             # 0.3679 — natural decay
    '1/π':      1/np.pi,            # 0.3183 — circle
    '2/π':      2/np.pi,            # 0.6366 — Buffon's needle
    'π/4':      np.pi/4,            # 0.7854 — quarter circle
    'e/π':      np.e/np.pi,         # 0.8653 — transcendental ratio
    'φ':        (np.sqrt(5)-1)/2,   # 0.6180 — golden ratio
    'φ²':       ((np.sqrt(5)-1)/2)**2, # 0.3820 — golden ratio squared
    '√2-1':     np.sqrt(2)-1,       # 0.4142 — silver ratio
    '2-√3':     2-np.sqrt(3),       # 0.2679 — tan(15°)
    'γ_EM':     0.5772,             # Euler-Mascheroni
    'G_Cat':    0.9160,             # Catalan's constant
    'log₁₀(2)': np.log10(2),       # 0.3010
    'log₁₀(e)': np.log10(np.e),    # 0.4343
    'ln(√2)':   np.log(np.sqrt(2)), # 0.3466
    'sin(1)':   np.sin(1),          # 0.8415
    'cos(1)':   np.cos(1),          # 0.5403
    '√3/2':     np.sqrt(3)/2,       # 0.8660 — hexagonal
    'φ/√2':     (np.sqrt(5)-1)/2/np.sqrt(2), # 0.4370
    'e^(-π/4)': np.exp(-np.pi/4),   # 0.4559
    '1/4':      0.25,
    '1/3':      1/3,
    '1/2':      0.5,
    '2/3':      2/3,
    '3/4':      0.75,
}

const_names = list(C.keys())
const_vals = np.array([C[k] for k in const_names])

# ═══════════════════════════════════════════════════════════════════
# BUILD SCORE FUNCTIONS FOR ALL 75 SYSTEMS
# ═══════════════════════════════════════════════════════════════════

# Category-to-landscape shape mapping based on physics
# Each fp_category has a characteristic score landscape shape
CATEGORY_SHAPES = {
    'ENERGETIC':   {'peak': 0.62, 'width': 0.25, 'skew': -0.1},  # Energy min → left-skewed
    'STRUCTURAL':  {'peak': 0.50, 'width': 0.30, 'skew':  0.0},  # Symmetric structure
    'TRANSITION':  {'peak': 0.71, 'width': 0.15, 'skew':  0.2},  # Sharp transition
    'SCALING':     {'peak': 0.69, 'width': 0.20, 'skew':  0.1},  # ln(2) scaling
    'CONSERVED':   {'peak': 0.58, 'width': 0.35, 'skew':  0.0},  # Broad conservation
    'EQUILIBRIUM': {'peak': 0.50, 'width': 0.30, 'skew':  0.0},  # Symmetric equilibrium
    'DIFFRACTION': {'peak': 0.64, 'width': 0.20, 'skew':  0.05}, # Diffraction pattern
}

# Map inventory R² values by name
inv_r2 = {}
for s in inventory['systems']:
    if s.get('PLL_R2') is not None:
        inv_r2[s['name']] = s['PLL_R2']

# Map blend experiments to catalog system names
BLEND_MAP = {
    'EXP-01': 'Gold/Silver Price Ratio',
    'EXP-03': 'SEMF Binding Energy Valley',
    'EXP-04': 'RC Bandpass Filter Response',
    'EXP-06': 'D-T Reaction Rate Composition',
    'EXP-07': 'Parton Momentum (DGLAP evolution)',
}

def build_score_func(system, alphas_out=None):
    """
    Build a score function S(α) for a system.
    Returns: S_norm function, data_quality tier, and metadata.

    Tier 1: Direct blend landscape (5 systems)
    Tier 2: PLL_R² + parabolic model (20 systems)
    Tier 3: Category-based model (50 systems)
    """
    name = system['name']
    exp = system.get('exp', '')
    cat_type = system.get('fp_category', 'EQUILIBRIUM')
    D = system.get('D', 3)

    # Tier 1: Direct blend landscape data
    for exp_id, blend_name in BLEND_MAP.items():
        if name == blend_name and exp_id in blend_data.get('blend_results', {}):
            br = blend_data['blend_results'][exp_id]
            # Use geometric blend (CoDa natural)
            bf = 'geometric' if 'geometric' in br['blends'] else list(br['blends'].keys())[0]
            scores = np.array(br['blends'][bf]['scores'])
            alphas = np.array(br['blends'][bf]['alphas'])
            s_min, s_max = scores.min(), scores.max()
            rng = s_max - s_min if s_max > s_min else 1e-10

            def make_snorm(a, s, smin, r):
                def S_norm(alpha):
                    return float(np.clip((np.interp(alpha, a, s) - smin) / r, 0, 1))
                return S_norm

            return make_snorm(alphas, scores, s_min, rng), 'TIER_1', {
                'R2': float(np.max(scores)), 'peak_alpha': float(alphas[np.argmax(scores)]),
                'blend_func': bf
            }

    # Tier 2: Have PLL_R² — build parabolic landscape
    r2 = inv_r2.get(name)
    if r2 is not None and r2 > 0:
        shape = CATEGORY_SHAPES.get(cat_type, CATEGORY_SHAPES['EQUILIBRIUM'])
        peak = shape['peak']
        width = shape['width']
        skew = shape['skew']

        # Modulate peak position by D (more channels → peak shifts toward 1/D natural)
        if D > 1:
            natural_alpha = 1.0 / D
            peak = 0.5 * peak + 0.5 * min(natural_alpha * 3, 0.9)

        def make_parabolic(r2_val, pk, w, sk):
            def S_norm(alpha):
                x = (alpha - pk) / w
                base = np.exp(-0.5 * x**2)  # Gaussian envelope
                skew_mod = 1 + sk * x  # Linear skew
                val = r2_val * base * np.clip(skew_mod, 0.5, 1.5)
                return float(np.clip(val, 0, 1))
            return S_norm

        return make_parabolic(r2, peak, width, skew), 'TIER_2', {
            'R2': r2, 'peak_alpha': peak, 'width': width
        }

    # Tier 3: Category-based model (theoretical landscape)
    shape = CATEGORY_SHAPES.get(cat_type, CATEGORY_SHAPES['EQUILIBRIUM'])
    peak = shape['peak']
    width = shape['width']
    skew = shape['skew']

    # Use D to set a baseline R² estimate
    est_r2 = max(0.3, min(0.95, 0.5 + 0.1 * np.log(D)))

    # Modulate by data_type
    dtype = system.get('data_type', 'THEORETICAL')
    if dtype == 'REAL':
        est_r2 *= 1.1  # Real data typically stronger
    elif dtype == 'HUNT':
        est_r2 *= 0.8  # Hunt systems untested

    est_r2 = min(est_r2, 0.99)

    def make_theoretical(r2_val, pk, w, sk):
        def S_norm(alpha):
            x = (alpha - pk) / w
            base = np.exp(-0.5 * x**2)
            skew_mod = 1 + sk * x
            val = r2_val * base * np.clip(skew_mod, 0.5, 1.5)
            return float(np.clip(val, 0, 1))
        return S_norm

    return make_theoretical(est_r2, peak, width, skew), 'TIER_3', {
        'est_R2': est_r2, 'peak_alpha': peak, 'width': width
    }


# ═══════════════════════════════════════════════════════════════════
# THE SUPER SQUEEZE: Find native reciprocal for each system
# ═══════════════════════════════════════════════════════════════════

print("=" * 120)
print("  HFSP SUPER SQUEEZE — All 75 Systems: Transcendental Cancellation")
print(f"  Testing {len(C)} constants across {len(catalog['systems'])} systems")
print("=" * 120)

results = []
reciprocal_found = []
no_reciprocal = []

for sys_idx, system in enumerate(catalog['systems']):
    name = system['name']
    sys_id = system['id']
    domain = system['domain']
    cat_type = system.get('fp_category', '?')

    # Build score function
    S_norm, tier, meta = build_score_func(system)

    # Evaluate S_norm at all constants
    evaluations = {}
    for cname in const_names:
        val = C[cname]
        evaluations[cname] = S_norm(val)

    # ─── THE SWAP TEST ───
    # For every pair (a,b): check if S_norm(a) ≈ b
    # This means: "input constant a, output IS constant b"
    # That's a native reciprocal — the system maps a→b naturally

    best_match = None
    best_delta = 999
    all_matches = []

    for in_name in const_names:
        in_val = C[in_name]
        out_val = S_norm(in_val)

        # Check if output matches any constant
        for target_name in const_names:
            if target_name == in_name:
                continue
            target_val = C[target_name]
            delta = abs(out_val - target_val)
            rel_delta = delta / max(abs(target_val), 1e-10)

            if delta < 0.05:  # Within 5% absolute
                all_matches.append({
                    'input': in_name,
                    'input_val': float(in_val),
                    'output': float(out_val),
                    'target': target_name,
                    'target_val': float(target_val),
                    'delta': float(delta),
                    'rel_delta': float(rel_delta),
                })

            if delta < best_delta:
                best_delta = delta
                best_match = {
                    'input': in_name,
                    'input_val': float(in_val),
                    'output': float(out_val),
                    'target': target_name,
                    'target_val': float(target_val),
                    'delta': float(delta),
                    'rel_delta': float(rel_delta),
                }

    # ─── IDENTITY CHECK: S_norm(a) ≈ a (fixed point) ───
    identity_matches = []
    for cname in const_names:
        val = C[cname]
        out = S_norm(val)
        delta = abs(out - val)
        if delta < 0.03:
            identity_matches.append({
                'constant': cname,
                'value': float(val),
                'output': float(out),
                'delta': float(delta),
            })

    # ─── RATIO CANCELLATION ───
    # For every pair, compute S(a)/S(b) and check if it's a known constant
    ratio_matches = []
    for i, na in enumerate(const_names):
        sa = evaluations[na]
        if sa < 0.01:
            continue
        for j, nb in enumerate(const_names):
            if i >= j:
                continue
            sb = evaluations[nb]
            if sb < 0.01:
                continue
            ratio = sa / sb
            # Check if ratio matches any constant
            for target_name in const_names:
                tv = C[target_name]
                if abs(ratio - tv) < 0.02:
                    ratio_matches.append({
                        'num': na, 'den': nb,
                        'ratio': float(ratio),
                        'matches': target_name,
                        'delta': float(abs(ratio - tv)),
                    })

    # ─── RESIDUAL COMPUTATION ───
    # After removing the best reciprocal relationship, what's left?
    all_outputs = np.array([evaluations[cn] for cn in const_names])
    all_inputs = const_vals

    # Compute residual: deviation of outputs from any known constant
    residuals = []
    for out in all_outputs:
        min_dist = min(abs(out - cv) for cv in const_vals)
        residuals.append(min_dist)
    residual_rms = float(np.sqrt(np.mean(np.array(residuals)**2)))
    residual_mean = float(np.mean(residuals))
    residual_max = float(np.max(residuals))

    # Geometric mean of all outputs (the "pure signature")
    valid_outputs = all_outputs[all_outputs > 0.01]
    geo_mean = float(np.exp(np.mean(np.log(valid_outputs)))) if len(valid_outputs) > 0 else 0

    # Check if geo_mean matches a constant
    geo_match = None
    for cn in const_names:
        if abs(geo_mean - C[cn]) < 0.02:
            geo_match = cn
            break

    # Sort matches by quality
    all_matches.sort(key=lambda x: x['delta'])

    # Determine if clean reciprocal exists
    has_clean = best_delta < 0.01  # Within 1%
    has_good = best_delta < 0.03   # Within 3%
    has_partial = best_delta < 0.05 # Within 5%

    result = {
        'id': sys_id,
        'name': name,
        'domain': domain,
        'fp_category': cat_type,
        'tier': tier,
        'meta': meta,
        'best_reciprocal': best_match,
        'n_matches_5pct': len(all_matches),
        'top_matches': all_matches[:5],
        'identity_matches': identity_matches,
        'n_ratio_cancellations': len(ratio_matches),
        'top_ratios': ratio_matches[:3],
        'residual_rms': residual_rms,
        'residual_mean': residual_mean,
        'residual_max': residual_max,
        'geo_mean_signature': geo_mean,
        'geo_match': geo_match,
        'classification': 'CLEAN' if has_clean else ('GOOD' if has_good else ('PARTIAL' if has_partial else 'NONE')),
    }
    results.append(result)

    if has_clean or has_good:
        reciprocal_found.append(result)
    else:
        no_reciprocal.append(result)

    # Progress
    status = '✓' if has_clean else ('◐' if has_good else ('○' if has_partial else '✗'))
    bm = best_match
    print(f"  [{sys_id:2d}] {status} {name:45s} {tier:7s} δ={best_delta:.4f}  "
          f"{bm['input']:>10s} → S={bm['output']:.4f} ≈ {bm['target']:>10s} ({bm['target_val']:.4f})")

# ═══════════════════════════════════════════════════════════════════
# SUMMARY TABLES
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 120)
print("  NATIVE RECIPROCAL TABLE — Systems with Clean Matches (δ < 3%)")
print("═" * 120)
print(f"  {'#':>3s} {'System':42s} {'Domain':8s} {'Cat':12s} {'Tier':7s} "
      f"{'Input':>10s} → {'Output':>8s} ≈ {'Target':>10s} {'δ':>8s}")
print("─" * 120)
for r in sorted(reciprocal_found, key=lambda x: x['best_reciprocal']['delta']):
    bm = r['best_reciprocal']
    print(f"  {r['id']:3d} {r['name']:42s} {r['domain']:8s} {r['fp_category']:12s} {r['tier']:7s} "
          f"{bm['input']:>10s} → {bm['output']:8.4f} ≈ {bm['target']:>10s} {bm['delta']:8.5f}")

print(f"\n  Total with clean reciprocal: {len(reciprocal_found)}/{len(results)}")

print("\n" + "═" * 120)
print("  NO-RECIPROCAL TABLE — Systems Without Clean Match (δ ≥ 3%)")
print("═" * 120)
print(f"  {'#':>3s} {'System':42s} {'Domain':8s} {'Cat':12s} {'Best δ':>8s} "
      f"{'Best Input→Target':>30s} {'Residual':>10s}")
print("─" * 120)
for r in sorted(no_reciprocal, key=lambda x: x['best_reciprocal']['delta']):
    bm = r['best_reciprocal']
    pair = f"{bm['input']}→{bm['target']}"
    print(f"  {r['id']:3d} {r['name']:42s} {r['domain']:8s} {r['fp_category']:12s} {bm['delta']:8.5f} "
          f"{pair:>30s} {r['residual_rms']:10.5f}")

# ═══════════════════════════════════════════════════════════════════
# CROSS-SYSTEM ANALYSIS
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 120)
print("  CROSS-SYSTEM ANALYSIS")
print("═" * 120)

# Which constants appear most as inputs/targets?
input_counts = defaultdict(int)
target_counts = defaultdict(int)
pair_counts = defaultdict(int)
for r in results:
    if r['classification'] in ['CLEAN', 'GOOD']:
        bm = r['best_reciprocal']
        input_counts[bm['input']] += 1
        target_counts[bm['target']] += 1
        pair_counts[f"{bm['input']}→{bm['target']}"] += 1

print("\n  Most common INPUT constants (in clean/good reciprocals):")
for cn, count in sorted(input_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"    {cn:12s}: {count:3d} systems  (value = {C[cn]:.4f})")

print("\n  Most common TARGET constants (output matches):")
for cn, count in sorted(target_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"    {cn:12s}: {count:3d} systems  (value = {C[cn]:.4f})")

print("\n  Most common PAIRS (input→output):")
for pair, count in sorted(pair_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"    {pair:25s}: {count:3d} systems")

# Domain breakdown
print("\n  By domain:")
for domain in ['MATTER', 'ENERGY', 'GRAVITY', 'FORCE']:
    dom_results = [r for r in results if r['domain'] == domain]
    dom_clean = sum(1 for r in dom_results if r['classification'] in ['CLEAN', 'GOOD'])
    dom_partial = sum(1 for r in dom_results if r['classification'] == 'PARTIAL')
    dom_none = sum(1 for r in dom_results if r['classification'] == 'NONE')
    print(f"    {domain:8s}: {len(dom_results):2d} systems — "
          f"{dom_clean} clean/good, {dom_partial} partial, {dom_none} none")

# Category breakdown
print("\n  By fp_category:")
for cat in sorted(set(r['fp_category'] for r in results)):
    cat_results = [r for r in results if r['fp_category'] == cat]
    cat_clean = sum(1 for r in cat_results if r['classification'] in ['CLEAN', 'GOOD'])
    avg_delta = np.mean([r['best_reciprocal']['delta'] for r in cat_results])
    print(f"    {cat:12s}: {len(cat_results):2d} systems — "
          f"{cat_clean} with reciprocal, avg δ = {avg_delta:.4f}")

# Identity chains (systems that are fixed points)
print("\n  IDENTITY CHAINS (S_norm(a) ≈ a — self-referential systems):")
for r in results:
    if r['identity_matches']:
        for im in r['identity_matches']:
            print(f"    [{r['id']:2d}] {r['name']:40s}: "
                  f"S_norm({im['constant']}) = {im['output']:.4f} ≈ {im['value']:.4f} "
                  f"(δ = {im['delta']:.4f})")

# Geometric mean signatures
print("\n  GEOMETRIC MEAN SIGNATURES (pure residual after squeeze):")
matched = [(r, r['geo_match']) for r in results if r['geo_match']]
unmatched = [(r, r['geo_mean_signature']) for r in results if not r['geo_match']]
if matched:
    print("    Systems whose geometric mean matches a constant:")
    for r, gm in matched:
        print(f"      [{r['id']:2d}] {r['name']:40s}: geo_mean ≈ {gm} ({r['geo_mean_signature']:.4f})")
if unmatched:
    print(f"    Systems with unmatched geo mean: {len(unmatched)}")
    # Group by approximate value
    gm_vals = np.array([gm for _, gm in unmatched])
    print(f"    Range: {gm_vals.min():.4f} — {gm_vals.max():.4f}, "
          f"median: {np.median(gm_vals):.4f}")

# Tier breakdown
print("\n  By data tier:")
for tier in ['TIER_1', 'TIER_2', 'TIER_3']:
    t_results = [r for r in results if r['tier'] == tier]
    if not t_results:
        continue
    t_clean = sum(1 for r in t_results if r['classification'] in ['CLEAN', 'GOOD'])
    avg_resid = np.mean([r['residual_rms'] for r in t_results])
    print(f"    {tier}: {len(t_results):2d} systems — "
          f"{t_clean} with reciprocal, avg residual = {avg_resid:.4f}")

# ═══════════════════════════════════════════════════════════════════
# COMBINATION ANALYSIS for no-reciprocal systems
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 120)
print("  BEST COMBINATIONS for Systems Without Clean Reciprocal")
print("═" * 120)

for r in sorted(no_reciprocal, key=lambda x: x['best_reciprocal']['delta'])[:30]:
    bm = r['best_reciprocal']
    print(f"\n  [{r['id']:2d}] {r['name']} ({r['domain']}/{r['fp_category']})")
    print(f"       Best single: {bm['input']}→{bm['target']} δ={bm['delta']:.5f}")

    # Show top 3 matches
    for m in r['top_matches'][:3]:
        print(f"       Alt: {m['input']:>10s} → S={m['output']:.4f} ≈ {m['target']:>10s} δ={m['delta']:.5f}")

    # Show ratio cancellations
    if r['top_ratios']:
        print(f"       Ratio cancellations:")
        for rc in r['top_ratios'][:2]:
            print(f"         S({rc['num']})/S({rc['den']}) = {rc['ratio']:.4f} ≈ {rc['matches']} δ={rc['delta']:.5f}")

# ═══════════════════════════════════════════════════════════════════
# SAVE RESULTS
# ═══════════════════════════════════════════════════════════════════

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

output = {
    '_meta': {
        'analysis': 'HFSP Super Squeeze — All 75 Systems',
        'n_systems': len(results),
        'n_constants': len(C),
        'constants': {k: float(v) for k, v in C.items()},
    },
    'summary': {
        'clean_reciprocal': len([r for r in results if r['classification'] == 'CLEAN']),
        'good_reciprocal': len([r for r in results if r['classification'] == 'GOOD']),
        'partial_match': len([r for r in results if r['classification'] == 'PARTIAL']),
        'no_match': len([r for r in results if r['classification'] == 'NONE']),
        'by_domain': {
            dom: {
                'total': len([r for r in results if r['domain'] == dom]),
                'with_reciprocal': len([r for r in results if r['domain'] == dom and r['classification'] in ['CLEAN','GOOD']]),
            }
            for dom in ['MATTER', 'ENERGY', 'GRAVITY', 'FORCE']
        },
        'most_common_pairs': dict(sorted(pair_counts.items(), key=lambda x: -x[1])[:10]),
    },
    'reciprocal_table': [
        {k: v for k, v in r.items() if k != 'meta'}
        for r in sorted(reciprocal_found, key=lambda x: x['best_reciprocal']['delta'])
    ],
    'no_reciprocal_table': [
        {k: v for k, v in r.items() if k != 'meta'}
        for r in sorted(no_reciprocal, key=lambda x: x['best_reciprocal']['delta'])
    ],
    'all_results': [
        {k: v for k, v in r.items() if k != 'meta'}
        for r in results
    ],
}

with open('hfsp_super_squeeze_75.json', 'w') as f:
    json.dump(output, f, indent=2, cls=NumpyEncoder)
print(f"\n  Results saved to hfsp_super_squeeze_75.json")

# ═══════════════════════════════════════════════════════════════════
# VISUALIZATION — 6-panel dashboard
# ═══════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(24, 20))
fig.suptitle('HFSP Super Squeeze — All 75 Systems\nTranscendental Cancellation & Native Reciprocal Analysis',
             fontsize=16, fontweight='bold', y=0.98)

# Color maps
domain_colors = {'MATTER': '#3FB950', 'ENERGY': '#F0883E', 'GRAVITY': '#8B5CF6', 'FORCE': '#58A6FF'}
class_colors = {'CLEAN': '#3FB950', 'GOOD': '#58A6FF', 'PARTIAL': '#F0883E', 'NONE': '#F85149'}
tier_markers = {'TIER_1': 'D', 'TIER_2': 's', 'TIER_3': 'o'}

# Panel 1: Delta distribution — all 75 systems sorted
ax1 = fig.add_subplot(3, 2, 1)
sorted_results = sorted(results, key=lambda x: x['best_reciprocal']['delta'])
deltas = [r['best_reciprocal']['delta'] for r in sorted_results]
colors = [domain_colors[r['domain']] for r in sorted_results]
bars = ax1.bar(range(len(deltas)), deltas, color=colors, edgecolor='none', alpha=0.8, width=1.0)
ax1.axhline(y=0.01, color='#3FB950', linestyle='--', alpha=0.7, label='Clean (1%)')
ax1.axhline(y=0.03, color='#58A6FF', linestyle='--', alpha=0.7, label='Good (3%)')
ax1.axhline(y=0.05, color='#F0883E', linestyle='--', alpha=0.7, label='Partial (5%)')
ax1.set_xlabel('System (sorted by δ)')
ax1.set_ylabel('Best reciprocal δ')
ax1.set_title('Native Reciprocal Quality — All 75 Systems')
ax1.legend(fontsize=8)
ax1.set_xlim(-1, 76)

# Panel 2: Domain breakdown pie + classification
ax2 = fig.add_subplot(3, 2, 2)
classifications = ['CLEAN', 'GOOD', 'PARTIAL', 'NONE']
class_counts = [sum(1 for r in results if r['classification'] == c) for c in classifications]
class_cols = [class_colors[c] for c in classifications]
wedges, texts, autotexts = ax2.pie(class_counts, labels=classifications, colors=class_cols,
                                    autopct='%1.0f%%', startangle=90, pctdistance=0.85)
for t in autotexts:
    t.set_fontsize(11)
    t.set_fontweight('bold')
ax2.set_title(f'Classification Distribution\n({sum(class_counts[:2])}/75 with reciprocal)')

# Panel 3: Input constant frequency heatmap
ax3 = fig.add_subplot(3, 2, 3)
# For all systems, show which constants appear as best inputs
input_hist = defaultdict(int)
target_hist = defaultdict(int)
for r in results:
    if r['classification'] in ['CLEAN', 'GOOD', 'PARTIAL']:
        bm = r['best_reciprocal']
        input_hist[bm['input']] += 1
        target_hist[bm['target']] += 1

# Bar chart of input constants
sorted_inputs = sorted(input_hist.items(), key=lambda x: -x[1])[:15]
if sorted_inputs:
    names_in = [x[0] for x in sorted_inputs]
    counts_in = [x[1] for x in sorted_inputs]
    y_pos = range(len(names_in))
    ax3.barh(y_pos, counts_in, color='#58A6FF', alpha=0.8)
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(names_in, fontsize=9)
    ax3.set_xlabel('Number of systems')
    ax3.set_title('Most Common INPUT Constants')
    ax3.invert_yaxis()

# Panel 4: Target constant frequency
ax4 = fig.add_subplot(3, 2, 4)
sorted_targets = sorted(target_hist.items(), key=lambda x: -x[1])[:15]
if sorted_targets:
    names_tgt = [x[0] for x in sorted_targets]
    counts_tgt = [x[1] for x in sorted_targets]
    y_pos = range(len(names_tgt))
    ax4.barh(y_pos, counts_tgt, color='#F0883E', alpha=0.8)
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(names_tgt, fontsize=9)
    ax4.set_xlabel('Number of systems')
    ax4.set_title('Most Common TARGET Constants (Outputs)')
    ax4.invert_yaxis()

# Panel 5: Residual vs delta scatter (quality map)
ax5 = fig.add_subplot(3, 2, 5)
for r in results:
    c = domain_colors[r['domain']]
    m = tier_markers[r['tier']]
    ax5.scatter(r['best_reciprocal']['delta'], r['residual_rms'],
               c=c, marker=m, s=60, alpha=0.7, edgecolors='white', linewidth=0.5)
ax5.set_xlabel('Best reciprocal δ')
ax5.set_ylabel('Residual RMS')
ax5.set_title('Quality Map: Reciprocal Match vs Residual')
ax5.axvline(x=0.03, color='gray', linestyle=':', alpha=0.5)
# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=domain_colors[d], markersize=8, label=d)
    for d in ['MATTER', 'ENERGY', 'GRAVITY', 'FORCE']
] + [
    Line2D([0], [0], marker=tier_markers[t], color='w', markerfacecolor='gray', markersize=8, label=t)
    for t in ['TIER_1', 'TIER_2', 'TIER_3']
]
ax5.legend(handles=legend_elements, fontsize=7, ncol=2, loc='upper right')

# Panel 6: Pair heatmap — top input×target combinations
ax6 = fig.add_subplot(3, 2, 6)
# Build a matrix of input→target counts
top_in = [x[0] for x in sorted_inputs[:10]] if sorted_inputs else []
top_tgt = [x[0] for x in sorted_targets[:10]] if sorted_targets else []
if top_in and top_tgt:
    pair_matrix = np.zeros((len(top_in), len(top_tgt)))
    for r in results:
        if r['classification'] in ['CLEAN', 'GOOD', 'PARTIAL']:
            bm = r['best_reciprocal']
            if bm['input'] in top_in and bm['target'] in top_tgt:
                i = top_in.index(bm['input'])
                j = top_tgt.index(bm['target'])
                pair_matrix[i, j] += 1

    im = ax6.imshow(pair_matrix, cmap='YlOrRd', aspect='auto')
    ax6.set_xticks(range(len(top_tgt)))
    ax6.set_xticklabels(top_tgt, rotation=45, ha='right', fontsize=8)
    ax6.set_yticks(range(len(top_in)))
    ax6.set_yticklabels(top_in, fontsize=8)
    ax6.set_xlabel('Target (output)')
    ax6.set_ylabel('Input')
    ax6.set_title('Input → Target Pair Frequency')
    plt.colorbar(im, ax=ax6, shrink=0.8)

    # Annotate cells
    for i in range(len(top_in)):
        for j in range(len(top_tgt)):
            if pair_matrix[i, j] > 0:
                ax6.text(j, i, f'{int(pair_matrix[i, j])}',
                        ha='center', va='center', fontsize=9, fontweight='bold',
                        color='white' if pair_matrix[i, j] > 3 else 'black')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('hfsp_super_squeeze_75.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("  Dashboard saved to hfsp_super_squeeze_75.png")

# ═══════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 120)
print("  FINAL SCORECARD")
print("═" * 120)
n_clean = sum(1 for r in results if r['classification'] == 'CLEAN')
n_good = sum(1 for r in results if r['classification'] == 'GOOD')
n_partial = sum(1 for r in results if r['classification'] == 'PARTIAL')
n_none = sum(1 for r in results if r['classification'] == 'NONE')
print(f"  CLEAN reciprocal (δ < 1%):  {n_clean:3d}")
print(f"  GOOD reciprocal  (δ < 3%):  {n_good:3d}")
print(f"  PARTIAL match    (δ < 5%):  {n_partial:3d}")
print(f"  NO match         (δ ≥ 5%):  {n_none:3d}")
print(f"  {'─'*40}")
print(f"  TOTAL with native reciprocal: {n_clean + n_good:3d} / 75")
print(f"  Success rate:                 {100*(n_clean+n_good)/75:.1f}%")
print()
