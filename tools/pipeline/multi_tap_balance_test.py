#!/usr/bin/env python3
"""
MULTI-TAP BALANCE TRANSFORMER TEST — April 10, 2026
=====================================================
Peter's idea: does EITT hold simultaneously across ALL valid SBP trees,
not just the one we wired? If yes, invariance is a simplex geometry property.
If no, which partitions break tells us about compositional structure.

Tests multiple SBP configurations on:
1. Energy World K=7 (Coal, Gas, Nuclear, Hydro, Wind, Solar, Other_Renew)
2. Energy Germany K=7
3. Financial K=9

For each dataset, we construct multiple valid SBP trees and check whether
ILR balance means are preserved under geometric-mean decimation at all taps.
"""
import csv, math, os, sys, random
from collections import defaultdict

EPSILON = 1e-12

# ══════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ══════════════════════════════════════════════════════════════

def shannon_entropy(p):
    return -sum(pi * math.log(pi) for pi in p if pi > EPSILON)

def geometric_mean(vals):
    if not vals or any(v <= 0 for v in vals):
        return EPSILON
    return math.exp(sum(math.log(v) for v in vals) / len(vals))

def arithmetic_mean(vals):
    return sum(vals) / len(vals) if vals else 0

def geom_mean_compositions(comps):
    K = len(comps[0])
    gm = [geometric_mean([c[j] for c in comps]) for j in range(K)]
    total = sum(gm)
    return [g / total for g in gm] if total > 0 else [1/K]*K

def ilr_balance(x, group1_idx, group2_idx):
    """Proper ILR balance: sqrt(r*s/(r+s)) * ln(geomean(g1)/geomean(g2))"""
    r = len(group1_idx)
    s = len(group2_idx)
    g1 = geometric_mean([x[i] for i in group1_idx])
    g2 = geometric_mean([x[i] for i in group2_idx])
    coeff = math.sqrt(r * s / (r + s))
    return coeff * math.log(g1 / g2)

# ══════════════════════════════════════════════════════════════
# SBP TREE DEFINITIONS
# ══════════════════════════════════════════════════════════════

def define_energy_sbp_trees():
    """
    Energy K=7: 0=Coal 1=Gas 2=Nuclear 3=Hydro 4=Wind 5=Solar 6=Other_Renew

    Define multiple valid SBP trees — each is a different "tap configuration"
    """
    trees = {}

    # Tree 1: Original (Fossil vs Renewable) — current CoDa Explorer wiring
    trees['T1: Fossil|Renew'] = [
        ('B1: Fossil|Renew', [0, 1], [3, 4, 5, 6]),     # Coal+Gas vs Hydro+Wind+Solar+Other
        ('B2: Coal|Gas', [0], [1]),                        # within fossil
        ('B3: Wind|Solar', [4], [5]),                      # within renewable
        ('B4: Hydro|VarRenew', [3], [4, 5, 6]),           # hydro vs variable renewables
    ]

    # Tree 2: Thermal vs Non-thermal
    trees['T2: Thermal|NonThermal'] = [
        ('B1: Thermal|NonThermal', [0, 1, 2], [3, 4, 5, 6]),  # Coal+Gas+Nuc vs Hydro+Wind+Solar+Other
        ('B2: Fossil|Nuclear', [0, 1], [2]),                    # within thermal
        ('B3: Coal|Gas', [0], [1]),                              # within fossil
        ('B4: Hydro|VarRenew', [3], [4, 5, 6]),                # within non-thermal
    ]

    # Tree 3: Dispatchable vs Variable
    trees['T3: Dispatch|Variable'] = [
        ('B1: Dispatch|Variable', [0, 1, 2, 3], [4, 5, 6]),  # Coal+Gas+Nuc+Hydro vs Wind+Solar+Other
        ('B2: Fossil|Clean', [0, 1], [2, 3]),                  # Coal+Gas vs Nuclear+Hydro
        ('B3: Coal|Gas', [0], [1]),                              # within fossil
        ('B4: Wind|SolarOther', [4], [5, 6]),                   # within variable
    ]

    # Tree 4: Carbon-emitting vs Zero-carbon
    trees['T4: Carbon|ZeroCarbon'] = [
        ('B1: Carbon|Zero', [0, 1], [2, 3, 4, 5, 6]),   # Coal+Gas vs Nuclear+Hydro+Wind+Solar+Other
        ('B2: Coal|Gas', [0], [1]),                        # within carbon
        ('B3: Nuclear|Renew', [2], [3, 4, 5, 6]),         # nuclear vs renewables
        ('B4: Hydro|VarRenew', [3], [4, 5, 6]),           # hydro vs variable
    ]

    # Tree 5: Coal vs Everything (isolate coal)
    trees['T5: Coal|Rest'] = [
        ('B1: Coal|Rest', [0], [1, 2, 3, 4, 5, 6]),      # Coal alone vs everything else
        ('B2: Gas|NonFossil', [1], [2, 3, 4, 5, 6]),      # Gas vs non-fossil
        ('B3: Nuclear|Renew', [2], [3, 4, 5, 6]),          # Nuclear vs renewable
        ('B4: Hydro|VarRenew', [3], [4, 5, 6]),            # Hydro vs variable
    ]

    # Tree 6: Solar vs Everything (isolate solar — fastest growing)
    trees['T6: Solar|Rest'] = [
        ('B1: Solar|Rest', [5], [0, 1, 2, 3, 4, 6]),      # Solar alone vs everything
        ('B2: Fossil|Clean', [0, 1], [2, 3, 4, 6]),        # Fossil vs clean (ex-solar)
        ('B3: Coal|Gas', [0], [1]),                          # within fossil
        ('B4: Nuclear|RenewExSol', [2], [3, 4, 6]),        # nuclear vs renewables-ex-solar
    ]

    # Tree 7: Reverse of T1 — Renewable vs Fossil (swap polarity)
    trees['T7: Renew|Fossil (reversed)'] = [
        ('B1: Renew|Fossil', [3, 4, 5, 6], [0, 1]),       # Renewable vs Fossil (reversed B1)
        ('B2: Solar|Wind', [5], [4]),                        # reversed B3
        ('B3: Gas|Coal', [1], [0]),                          # reversed B2
        ('B4: VarRenew|Hydro', [4, 5, 6], [3]),            # reversed B4
    ]

    # Tree 8: Maximally unbalanced — each part peeled off one at a time
    trees['T8: Sequential peel'] = [
        ('B1: Coal|Rest', [0], [1, 2, 3, 4, 5, 6]),
        ('B2: Gas|Rest', [1], [2, 3, 4, 5, 6]),
        ('B3: Nuclear|Rest', [2], [3, 4, 5, 6]),
        ('B4: Hydro|Rest', [3], [4, 5, 6]),
    ]

    return trees

def define_financial_sbp_trees(K):
    """Financial K sectors — define a few meaningful SBP trees"""
    trees = {}

    if K < 4:
        return trees

    # Tree 1: First half vs second half
    mid = K // 2
    trees['T1: FirstHalf|SecondHalf'] = [
        ('B1: First|Second', list(range(mid)), list(range(mid, K))),
        ('B2: Q1|Q2', list(range(mid//2)), list(range(mid//2, mid))),
    ]

    # Tree 2: Odd vs Even indexed sectors
    odds = list(range(1, K, 2))
    evens = list(range(0, K, 2))
    trees['T2: Odd|Even'] = [
        ('B1: Odd|Even', odds, evens),
    ]

    # Tree 3: Sector 0 vs rest (isolate largest)
    trees['T3: Sector0|Rest'] = [
        ('B1: S0|Rest', [0], list(range(1, K))),
        ('B2: S1|Rest', [1], list(range(2, K))),
    ]

    # Tree 4: Last sector vs rest (isolate smallest)
    trees['T4: LastSector|Rest'] = [
        ('B1: Last|Rest', [K-1], list(range(K-1))),
        ('B2: SecondLast|Rest', [K-2], list(range(K-2))),
    ]

    return trees

# ══════════════════════════════════════════════════════════════
# MULTI-TAP TEST
# ══════════════════════════════════════════════════════════════

def run_multi_tap_test(compositions, sbp_trees, decimation_ratios=[2, 3, 5]):
    """
    For each SBP tree and each decimation ratio:
    1. Compute ILR balances at original resolution
    2. Decimate compositions via geometric mean
    3. Compute ILR balances on decimated compositions
    4. Compare: mean shift, variance ratio, max deviation
    """
    n = len(compositions)
    results = {}

    for tree_name, balances_def in sbp_trees.items():
        tree_results = {}

        # Compute original ILR balances
        orig_balances = []  # list of dicts {balance_name: value}
        for c in compositions:
            row = {}
            for bname, g1, g2 in balances_def:
                row[bname] = ilr_balance(c, g1, g2)
            orig_balances.append(row)

        for w in decimation_ratios:
            if n < w * 2:
                continue

            # Decimate
            agg_comps = []
            for i in range(0, n - w + 1, w):
                chunk = compositions[i:i+w]
                if len(chunk) == w:
                    agg_comps.append(geom_mean_compositions(chunk))

            if not agg_comps:
                continue

            # Compute ILR balances on decimated compositions
            agg_balances = []
            for c in agg_comps:
                row = {}
                for bname, g1, g2 in balances_def:
                    row[bname] = ilr_balance(c, g1, g2)
                agg_balances.append(row)

            # Compare each balance
            balance_comparisons = {}
            for bname, _, _ in balances_def:
                orig_vals = [b[bname] for b in orig_balances]
                agg_vals = [b[bname] for b in agg_balances]

                orig_mean = arithmetic_mean(orig_vals)
                agg_mean = arithmetic_mean(agg_vals)

                orig_var = arithmetic_mean([(v - orig_mean)**2 for v in orig_vals])
                agg_var = arithmetic_mean([(v - agg_mean)**2 for v in agg_vals])

                mean_shift = agg_mean - orig_mean
                var_ratio = agg_var / orig_var if orig_var > EPSILON else float('inf')

                # Relative mean shift (as % of original mean, handling zero)
                rel_shift = abs(mean_shift / orig_mean * 100) if abs(orig_mean) > EPSILON else abs(mean_shift) * 100

                balance_comparisons[bname] = {
                    'orig_mean': orig_mean,
                    'agg_mean': agg_mean,
                    'mean_shift': mean_shift,
                    'rel_shift_pct': rel_shift,
                    'orig_var': orig_var,
                    'agg_var': agg_var,
                    'var_ratio': var_ratio,
                    'mean_preserved': abs(mean_shift) < 0.1,
                }

            tree_results[w] = balance_comparisons

        results[tree_name] = tree_results

    return results

# ══════════════════════════════════════════════════════════════
# EITT ON EACH SBP (entropy of balance-transformed data)
# ══════════════════════════════════════════════════════════════

def run_eitt_per_tree(compositions, sbp_trees, decimation_ratios=[2, 3, 5]):
    """
    Standard EITT (Shannon entropy on raw compositions) doesn't change with SBP.
    But we can ask: does the VARIANCE structure of each balance tree change?

    Specifically: total ILR variance = sum of individual balance variances.
    Does total ILR variance ratio (agg/orig) depend on the tree choice?
    """
    n = len(compositions)
    results = {}

    for tree_name, balances_def in sbp_trees.items():
        tree_results = {}

        # Original total ILR variance
        orig_balances = []
        for c in compositions:
            row = []
            for bname, g1, g2 in balances_def:
                row.append(ilr_balance(c, g1, g2))
            orig_balances.append(row)

        n_bal = len(balances_def)
        orig_vars = []
        for bi in range(n_bal):
            vals = [b[bi] for b in orig_balances]
            m = arithmetic_mean(vals)
            orig_vars.append(arithmetic_mean([(v - m)**2 for v in vals]))

        orig_total_var = sum(orig_vars)

        for w in decimation_ratios:
            if n < w * 2:
                continue

            agg_comps = []
            for i in range(0, n - w + 1, w):
                chunk = compositions[i:i+w]
                if len(chunk) == w:
                    agg_comps.append(geom_mean_compositions(chunk))

            if not agg_comps:
                continue

            agg_balances = []
            for c in agg_comps:
                row = []
                for bname, g1, g2 in balances_def:
                    row.append(ilr_balance(c, g1, g2))
                agg_balances.append(row)

            agg_vars = []
            for bi in range(n_bal):
                vals = [b[bi] for b in agg_balances]
                m = arithmetic_mean(vals)
                agg_vars.append(arithmetic_mean([(v - m)**2 for v in vals]))

            agg_total_var = sum(agg_vars)

            # Proportional variance by balance (how much each tap contributes)
            orig_props = [v / orig_total_var if orig_total_var > 0 else 1/n_bal for v in orig_vars]
            agg_props = [v / agg_total_var if agg_total_var > 0 else 1/n_bal for v in agg_vars]

            # Shift in variance proportions
            prop_shifts = [abs(a - o) for a, o in zip(agg_props, orig_props)]

            tree_results[w] = {
                'orig_total_var': orig_total_var,
                'agg_total_var': agg_total_var,
                'total_var_ratio': agg_total_var / orig_total_var if orig_total_var > 0 else float('inf'),
                'orig_var_props': orig_props,
                'agg_var_props': agg_props,
                'max_prop_shift': max(prop_shifts),
                'balance_names': [b[0] for b in balances_def],
            }

        results[tree_name] = tree_results

    return results

# ══════════════════════════════════════════════════════════════
# DATA LOADERS
# ══════════════════════════════════════════════════════════════

def load_energy(area='World'):
    fp = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Energy/yearly_full_release_long_format.csv'
    if area != 'World':
        fp = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Energy/europe_yearly_full_release_long_format.csv'
    if not os.path.exists(fp):
        return None, None
    subcats = defaultdict(lambda: defaultdict(float))
    with open(fp) as f:
        for row in csv.DictReader(f):
            if (row.get('Area') == area and
                row.get('Variable') in ['Coal','Gas','Nuclear','Hydro','Wind','Solar','Other renewables'] and
                row.get('Category') == 'Electricity generation' and
                row.get('Unit') == 'TWh' and row.get('Value')):
                try:
                    subcats[int(row['Year'])][row['Variable']] = float(row['Value'])
                except:
                    pass
    sources = ['Coal','Gas','Nuclear','Hydro','Wind','Solar','Other renewables']
    years = sorted(subcats.keys())
    comps, valid_years = [], []
    for y in years:
        vals = [max(subcats[y].get(s, 0), 0.001) for s in sources]
        total = sum(vals)
        if total > 0:
            comps.append([v/total for v in vals])
            valid_years.append(y)
    return comps or None, valid_years or None

def load_financial():
    fp = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/financial data/stock_prices_daily.csv'
    if not os.path.exists(fp):
        return None, None, None
    sector_monthly = defaultdict(lambda: defaultdict(list))
    with open(fp) as f:
        for row in csv.DictReader(f):
            try:
                close = float(row['Close'])
                if close > 0:
                    month = row['Date'][:7]
                    sector = row['Sector']
                    sector_monthly[month][sector].append(close)
            except:
                pass
    months = sorted(sector_monthly.keys())
    sectors = sorted(set(s for m in months for s in sector_monthly[m].keys()))
    comps, valid_months = [], []
    for month in months:
        vals = []
        valid = True
        for s in sectors:
            prices = sector_monthly[month].get(s, [])
            if not prices:
                valid = False
                break
            vals.append(arithmetic_mean(prices))
        if valid and all(v > 0 for v in vals):
            total = sum(vals)
            comps.append([v/total for v in vals])
            valid_months.append(month)
    return (comps or None), (valid_months or None), sectors

# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    random.seed(42)
    out_path = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Githubrepo/HUF/code/analysis/multi_tap_balance_test_2026april10.txt'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, 'w') as out:
        out.write("=" * 80 + "\n")
        out.write("MULTI-TAP BALANCE TRANSFORMER TEST — 2026-04-10\n")
        out.write("Does EITT hold across ALL valid SBP trees, or just the one we wired?\n")
        out.write("If all trees preserve balance means: invariance is a simplex property.\n")
        out.write("If some break: which ones break tells us about compositional structure.\n")
        out.write("=" * 80 + "\n\n")

        # ── Energy World ──
        print("Loading Energy World...", file=sys.stderr)
        en_comps, en_years = load_energy('World')
        energy_trees = define_energy_sbp_trees()

        if en_comps:
            out.write("=" * 80 + "\n")
            out.write(f"ENERGY WORLD K=7: N={len(en_comps)}, {en_years[0]}→{en_years[-1]}\n")
            out.write("Components: 0=Coal 1=Gas 2=Nuclear 3=Hydro 4=Wind 5=Solar 6=Other_Renew\n")
            out.write("=" * 80 + "\n\n")

            # Part A: Balance mean preservation across all trees
            out.write("─── PART A: BALANCE MEAN PRESERVATION ───\n")
            out.write("Does each tap (ILR balance) preserve its mean under decimation?\n\n")

            tap_results = run_multi_tap_test(en_comps, energy_trees, [2, 3, 5])

            for tree_name in sorted(tap_results.keys()):
                out.write(f"\n  {tree_name}:\n")
                for w in [2, 3, 5]:
                    if w not in tap_results[tree_name]:
                        continue
                    out.write(f"    {w}:1 decimation:\n")
                    all_preserved = True
                    for bname, bdata in tap_results[tree_name][w].items():
                        status = "✓" if bdata['mean_preserved'] else "✗"
                        if not bdata['mean_preserved']:
                            all_preserved = False
                        out.write(f"      {status} {bname}: mean {bdata['orig_mean']:+.4f} → {bdata['agg_mean']:+.4f} "
                                  f"(shift={bdata['mean_shift']:+.4f}, {bdata['rel_shift_pct']:.2f}%, "
                                  f"var ratio={bdata['var_ratio']:.4f})\n")
                    out.write(f"    All taps preserved: {'YES' if all_preserved else 'NO'}\n")

            # Part B: Total ILR variance structure
            out.write("\n\n─── PART B: TOTAL ILR VARIANCE STRUCTURE ───\n")
            out.write("Does the variance distribution across taps change with tree choice?\n")
            out.write("If total_var_ratio is the same for all trees: tree-invariant property.\n\n")

            var_results = run_eitt_per_tree(en_comps, energy_trees, [2, 3, 5])

            for w in [2, 3, 5]:
                out.write(f"\n  {w}:1 decimation — Total ILR Variance Ratios:\n")
                out.write(f"  {'Tree':<35} {'Orig Var':>10} {'Agg Var':>10} {'Ratio':>8} {'Max Prop Shift':>15}\n")
                out.write(f"  {'─'*78}\n")

                ratios_at_w = []
                for tree_name in sorted(var_results.keys()):
                    if w in var_results[tree_name]:
                        r = var_results[tree_name][w]
                        ratios_at_w.append(r['total_var_ratio'])
                        out.write(f"  {tree_name:<35} {r['orig_total_var']:10.4f} {r['agg_total_var']:10.4f} "
                                  f"{r['total_var_ratio']:8.4f} {r['max_prop_shift']:15.4f}\n")

                if ratios_at_w:
                    spread = max(ratios_at_w) - min(ratios_at_w)
                    out.write(f"\n  Spread of total_var_ratio across trees: {spread:.6f}\n")
                    out.write(f"  Tree-invariant: {'YES (spread < 0.01)' if spread < 0.01 else 'NO — tree choice matters'}\n")

            # Part C: Variance proportion stability
            out.write("\n\n─── PART C: VARIANCE PROPORTION STABILITY ───\n")
            out.write("How each tap's share of total variance changes under decimation.\n")
            out.write("Stable proportions = balanced transformer holds shape.\n\n")

            for tree_name in sorted(var_results.keys()):
                out.write(f"\n  {tree_name}:\n")
                for w in [2, 3]:
                    if w not in var_results[tree_name]:
                        continue
                    r = var_results[tree_name][w]
                    out.write(f"    {w}:1  Variance proportions:\n")
                    for bi, bname in enumerate(r['balance_names']):
                        op = r['orig_var_props'][bi]
                        ap = r['agg_var_props'][bi]
                        out.write(f"      {bname}: {op:.4f} → {ap:.4f} (Δ={ap-op:+.4f})\n")

        # ── Energy Germany ──
        print("Loading Energy Germany...", file=sys.stderr)
        de_comps, de_years = load_energy('Germany')

        if de_comps:
            out.write("\n\n" + "=" * 80 + "\n")
            out.write(f"ENERGY GERMANY K=7: N={len(de_comps)}, {de_years[0]}→{de_years[-1]}\n")
            out.write("=" * 80 + "\n\n")

            tap_results_de = run_multi_tap_test(de_comps, energy_trees, [2, 3, 5])

            out.write("─── BALANCE MEAN PRESERVATION (all trees) ───\n\n")

            # Summary table: count preserved taps per tree per ratio
            out.write(f"  {'Tree':<35} {'2:1':>6} {'3:1':>6} {'5:1':>6}\n")
            out.write(f"  {'─'*53}\n")

            for tree_name in sorted(tap_results_de.keys()):
                counts = []
                for w in [2, 3, 5]:
                    if w in tap_results_de[tree_name]:
                        n_preserved = sum(1 for b in tap_results_de[tree_name][w].values() if b['mean_preserved'])
                        n_total = len(tap_results_de[tree_name][w])
                        counts.append(f"{n_preserved}/{n_total}")
                    else:
                        counts.append("—")
                out.write(f"  {tree_name:<35} {counts[0]:>6} {counts[1]:>6} {counts[2]:>6}\n")

            # Show failures in detail
            out.write("\n  Failures (|shift| >= 0.1):\n")
            for tree_name in sorted(tap_results_de.keys()):
                for w in [2, 3, 5]:
                    if w not in tap_results_de[tree_name]:
                        continue
                    for bname, bdata in tap_results_de[tree_name][w].items():
                        if not bdata['mean_preserved']:
                            out.write(f"    {tree_name} @ {w}:1 — {bname}: shift={bdata['mean_shift']:+.4f}\n")

        # ── Financial ──
        print("Loading Financial...", file=sys.stderr)
        fi_comps, fi_months, fi_sectors = load_financial()

        if fi_comps:
            K_fi = len(fi_comps[0])
            out.write("\n\n" + "=" * 80 + "\n")
            out.write(f"FINANCIAL K={K_fi} (price-level, NOT market-cap): N={len(fi_comps)}, {fi_months[0]}→{fi_months[-1]}\n")
            if fi_sectors:
                out.write(f"Sectors: {', '.join(fi_sectors)}\n")
            out.write("=" * 80 + "\n\n")

            fi_trees = define_financial_sbp_trees(K_fi)
            tap_results_fi = run_multi_tap_test(fi_comps, fi_trees, [2, 3, 5])

            out.write("─── BALANCE MEAN PRESERVATION (all trees) ───\n\n")

            for tree_name in sorted(tap_results_fi.keys()):
                out.write(f"\n  {tree_name}:\n")
                for w in [2, 3, 5]:
                    if w not in tap_results_fi[tree_name]:
                        continue
                    all_preserved = True
                    out.write(f"    {w}:1:\n")
                    for bname, bdata in tap_results_fi[tree_name][w].items():
                        status = "✓" if bdata['mean_preserved'] else "✗"
                        if not bdata['mean_preserved']:
                            all_preserved = False
                        out.write(f"      {status} {bname}: shift={bdata['mean_shift']:+.6f} "
                                  f"(var ratio={bdata['var_ratio']:.4f})\n")
                    out.write(f"    All preserved: {'YES' if all_preserved else 'NO'}\n")

        # ══════════════════════════════════════════════════════════
        # GRAND SUMMARY
        # ══════════════════════════════════════════════════════════
        out.write("\n\n" + "=" * 80 + "\n")
        out.write("GRAND SUMMARY — MULTI-TAP BALANCE TRANSFORMER TEST\n")
        out.write("=" * 80 + "\n\n")

        out.write("Question: Is EITT balance preservation a property of the simplex geometry,\n")
        out.write("          or does it depend on which SBP tree (tap configuration) we choose?\n\n")

        # Count total pass/fail across all trees, datasets, ratios
        total_taps = 0
        preserved_taps = 0
        failed_details = []

        for dataset_name, tap_r in [('Energy World', tap_results if en_comps else {}),
                                      ('Energy Germany', tap_results_de if de_comps else {}),
                                      ('Financial', tap_results_fi if fi_comps else {})]:
            for tree_name, tree_data in tap_r.items():
                for w, balance_data in tree_data.items():
                    for bname, bdata in balance_data.items():
                        total_taps += 1
                        if bdata['mean_preserved']:
                            preserved_taps += 1
                        else:
                            failed_details.append(f"  {dataset_name} | {tree_name} | {w}:1 | {bname} | shift={bdata['mean_shift']:+.4f}")

        out.write(f"Total tap measurements: {total_taps}\n")
        out.write(f"Taps preserving mean (<0.1 shift): {preserved_taps} ({100*preserved_taps/total_taps:.1f}%)\n")
        out.write(f"Taps failing: {total_taps - preserved_taps} ({100*(total_taps-preserved_taps)/total_taps:.1f}%)\n\n")

        if failed_details:
            out.write("Failed taps (|shift| >= 0.1):\n")
            for fd in failed_details:
                out.write(fd + "\n")

        out.write("\n")
        if preserved_taps / total_taps > 0.95:
            out.write("VERDICT: Balance preservation is predominantly a SIMPLEX GEOMETRY property.\n")
            out.write("         The choice of SBP tree (tap configuration) does not matter much.\n")
        elif preserved_taps / total_taps > 0.80:
            out.write("VERDICT: Balance preservation is MOSTLY tree-invariant, with edge-case failures.\n")
            out.write("         Failures likely occur at taps involving fast-changing subcompositions.\n")
        else:
            out.write("VERDICT: Balance preservation DEPENDS on the SBP tree choice.\n")
            out.write("         The invariance is NOT purely a simplex geometry property.\n")

        out.write(f"\nDate: 2026-04-10\n")

    print(f"\nResults written to: {out_path}", file=sys.stderr)

if __name__ == '__main__':
    main()
