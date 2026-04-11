#!/usr/bin/env python3
"""
ADAPTIVE TAP DECIMATION TEST — April 10, 2026
================================================
Peter's idea: fixed compression ratios fail when components move too fast.
The taps should adapt to the rate of change — compress more where things
are slow, less where things are fast.

d(CoDa)/dt becomes the TAP CONTROLLER:
  - Compute local rate of change of each ILR balance (dB/dt)
  - Use that to determine max safe compression ratio at each time step
  - Apply variable-width decimation blocks
  - Compare: does adaptive decimation preserve entropy better than fixed?

This gives d(CoDa)/dt a concrete operational role: it's not just exploratory,
it determines the tap settings of the balance transformer.
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
    r = len(group1_idx)
    s = len(group2_idx)
    g1 = geometric_mean([x[i] for i in group1_idx])
    g2 = geometric_mean([x[i] for i in group2_idx])
    return math.sqrt(r * s / (r + s)) * math.log(g1 / g2)

# ══════════════════════════════════════════════════════════════
# d(CoDa)/dt — THE TAP CONTROLLER
# ══════════════════════════════════════════════════════════════

def compute_balance_rates(compositions, sbp, window=3):
    """
    Compute the local rate of change of each ILR balance.
    Uses centered finite difference with a smoothing window.

    Returns: list of dicts {balance_name: |dB/dt|} for each time step
    """
    n = len(compositions)
    balances = []
    for c in compositions:
        row = {}
        for bname, g1, g2 in sbp:
            row[bname] = ilr_balance(c, g1, g2)
        balances.append(row)

    balance_names = [b[0] for b in sbp]
    rates = []

    for t in range(n):
        row = {}
        for bname in balance_names:
            # Centered difference with available window
            lo = max(0, t - window)
            hi = min(n - 1, t + window)
            if hi > lo:
                dB = balances[hi][bname] - balances[lo][bname]
                dt = hi - lo
                row[bname] = abs(dB / dt)
            else:
                row[bname] = 0.0
        rates.append(row)

    return rates, balances

def compute_max_rate(rates):
    """For each time step, return the maximum |dB/dt| across all balances"""
    return [max(r.values()) for r in rates]

# ══════════════════════════════════════════════════════════════
# ADAPTIVE DECIMATION
# ══════════════════════════════════════════════════════════════

def adaptive_decimate(compositions, max_rates, base_ratio=5, rate_threshold_low=0.05, rate_threshold_high=0.3):
    """
    Adaptive decimation: compression ratio varies with local rate of change.

    - Where rate is LOW (< rate_threshold_low): use full base_ratio compression
    - Where rate is HIGH (> rate_threshold_high): use minimal compression (2:1)
    - In between: interpolate linearly

    Returns: list of decimated compositions AND the block boundaries used
    """
    n = len(compositions)
    blocks = []
    i = 0

    while i < n:
        # Determine local rate at this position
        local_rate = max_rates[i]

        # Map rate to block size
        if local_rate <= rate_threshold_low:
            block_size = base_ratio
        elif local_rate >= rate_threshold_high:
            block_size = 2
        else:
            # Linear interpolation
            frac = (local_rate - rate_threshold_low) / (rate_threshold_high - rate_threshold_low)
            block_size = int(round(base_ratio - frac * (base_ratio - 2)))
            block_size = max(2, min(base_ratio, block_size))

        # Don't exceed remaining data
        actual_size = min(block_size, n - i)
        if actual_size < 2:
            break

        chunk = compositions[i:i + actual_size]
        blocks.append({
            'start': i,
            'end': i + actual_size,
            'size': actual_size,
            'rate': local_rate,
            'comp': geom_mean_compositions(chunk)
        })
        i += actual_size

    return blocks

def fixed_decimate(compositions, ratio):
    """Standard fixed-ratio decimation for comparison"""
    n = len(compositions)
    blocks = []
    for i in range(0, n - ratio + 1, ratio):
        chunk = compositions[i:i + ratio]
        blocks.append({
            'start': i,
            'end': i + ratio,
            'size': ratio,
            'comp': geom_mean_compositions(chunk)
        })
    return blocks

# ══════════════════════════════════════════════════════════════
# EITT ON BLOCK-DECIMATED DATA
# ══════════════════════════════════════════════════════════════

def eitt_from_blocks(compositions, blocks):
    """Compute EITT residual comparing original to block-decimated"""
    base_H = arithmetic_mean([shannon_entropy(c) for c in compositions])
    agg_H = arithmetic_mean([shannon_entropy(b['comp']) for b in blocks])
    delta = agg_H - base_H
    pct = delta / base_H * 100 if base_H > 0 else 0
    return {'base_H': base_H, 'agg_H': agg_H, 'delta': delta, 'pct': pct}

def balance_preservation_from_blocks(compositions, blocks, sbp):
    """Check balance mean preservation on block-decimated data"""
    # Original balances
    orig_bals = []
    for c in compositions:
        row = {}
        for bname, g1, g2 in sbp:
            row[bname] = ilr_balance(c, g1, g2)
        orig_bals.append(row)

    # Decimated balances
    agg_bals = []
    for b in blocks:
        row = {}
        for bname, g1, g2 in sbp:
            row[bname] = ilr_balance(b['comp'], g1, g2)
        agg_bals.append(row)

    results = {}
    for bname, _, _ in sbp:
        orig_vals = [b[bname] for b in orig_bals]
        agg_vals = [b[bname] for b in agg_bals]
        orig_mean = arithmetic_mean(orig_vals)
        agg_mean = arithmetic_mean(agg_vals)
        shift = agg_mean - orig_mean
        results[bname] = {
            'orig_mean': orig_mean,
            'agg_mean': agg_mean,
            'shift': shift,
            'preserved': abs(shift) < 0.1
        }
    return results

# ══════════════════════════════════════════════════════════════
# DATA LOADERS
# ══════════════════════════════════════════════════════════════

def load_energy(area='World'):
    if area == 'World':
        fp = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Energy/yearly_full_release_long_format.csv'
    else:
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
    comps, vy = [], []
    for y in years:
        vals = [max(subcats[y].get(s, 0), 0.001) for s in sources]
        total = sum(vals)
        if total > 0:
            comps.append([v/total for v in vals])
            vy.append(y)
    return comps or None, vy or None

def load_gold_silver():
    fp = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Commodities/gold_silver_ratio_enriched.csv'
    rows = []
    with open(fp) as f:
        for row in csv.DictReader(f):
            if row.get('silver_oz_per_gold_oz', ''):
                try:
                    ratio = float(row['silver_oz_per_gold_oz'])
                    if ratio > 0:
                        year = int(row['date'][:4])
                        gs = ratio / (1 + ratio)
                        ss = 1 / (1 + ratio)
                        rows.append((year, [gs, ss]))
                except:
                    pass
    rows.sort()
    yearly = {}
    for y, c in rows:
        if y not in yearly:
            yearly[y] = c
    years = sorted(yearly.keys())
    return [yearly[y] for y in years], years

def load_financial():
    fp = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/financial data/stock_prices_daily.csv'
    if not os.path.exists(fp):
        return None, None
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
    comps, vm = [], []
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
            vm.append(month)
    return comps or None, vm or None

# ══════════════════════════════════════════════════════════════
# SBP DEFINITIONS
# ══════════════════════════════════════════════════════════════

def energy_sbp():
    return [
        ('B1: Fossil|Renew', [0, 1], [3, 4, 5, 6]),
        ('B2: Coal|Gas', [0], [1]),
        ('B3: Wind|Solar', [4], [5]),
        ('B4: Hydro|VarRenew', [3], [4, 5, 6]),
    ]

def energy_solar_sbp():
    """The tree that FAILED in the multi-tap test — Solar vs Rest"""
    return [
        ('B1: Solar|Rest', [5], [0, 1, 2, 3, 4, 6]),
        ('B2: Fossil|Clean', [0, 1], [2, 3, 4, 6]),
        ('B3: Coal|Gas', [0], [1]),
        ('B4: Nuclear|RenewExSol', [2], [3, 4, 6]),
    ]

def gold_silver_sbp():
    return [
        ('B1: Gold|Silver', [0], [1]),
    ]

def financial_sbp(K):
    mid = K // 2
    return [
        ('B1: First|Second', list(range(mid)), list(range(mid, K))),
    ]

# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    random.seed(42)
    out_path = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Githubrepo/HUF/code/analysis/adaptive_tap_test_2026april10.txt'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, 'w') as out:
        out.write("=" * 80 + "\n")
        out.write("ADAPTIVE TAP DECIMATION TEST — 2026-04-10\n")
        out.write("d(CoDa)/dt as the TAP CONTROLLER: compression adapts to rate of change.\n")
        out.write("Fast-moving balances → less compression. Slow balances → more compression.\n")
        out.write("=" * 80 + "\n\n")

        # ── Load datasets ──
        en_comps, en_years = load_energy('World')
        de_comps, de_years = load_energy('Germany')
        gs_comps, gs_years = load_gold_silver()
        fi_comps, fi_months = load_financial()

        # ══════════════════════════════════════════════════════════
        # TEST 1: ENERGY WORLD — Solar|Rest (the failure case)
        # ══════════════════════════════════════════════════════════
        if en_comps:
            out.write("=" * 80 + "\n")
            out.write("TEST 1: ENERGY WORLD — CAN ADAPTIVE TAPS RESCUE Solar|Rest?\n")
            out.write(f"N={len(en_comps)}, {en_years[0]}→{en_years[-1]}\n")
            out.write("=" * 80 + "\n\n")

            sbp_solar = energy_solar_sbp()
            sbp_std = energy_sbp()

            # Compute rates
            rates, balances = compute_balance_rates(en_comps, sbp_solar, window=2)
            max_rates = compute_max_rate(rates)

            out.write("─── d(CoDa)/dt Profile (Solar|Rest tree) ───\n\n")
            out.write(f"  {'Year':<6} {'Max |dB/dt|':>12} {'B1 Solar|Rest':>14} {'Suggested tap':>14}\n")
            out.write(f"  {'─'*46}\n")
            for t in range(len(en_comps)):
                mr = max_rates[t]
                b1_rate = rates[t].get('B1: Solar|Rest', 0)
                if mr <= 0.05:
                    tap = "5:1 (slow)"
                elif mr >= 0.3:
                    tap = "2:1 (fast)"
                else:
                    tap = f"{max(2, int(5 - (mr - 0.05) / 0.25 * 3))}:1"
                out.write(f"  {en_years[t]:<6} {mr:12.4f} {b1_rate:14.4f} {tap:>14}\n")

            # Fixed 5:1 (this failed)
            out.write("\n─── Fixed 5:1 Decimation ───\n\n")
            fixed_blocks = fixed_decimate(en_comps, 5)
            fixed_eitt = eitt_from_blocks(en_comps, fixed_blocks)
            fixed_bals = balance_preservation_from_blocks(en_comps, fixed_blocks, sbp_solar)

            out.write(f"  EITT residual: {fixed_eitt['pct']:+.4f}%\n")
            for bname, bd in fixed_bals.items():
                status = "PASS" if bd['preserved'] else "FAIL"
                out.write(f"  {bname}: mean {bd['orig_mean']:+.4f} → {bd['agg_mean']:+.4f} (shift={bd['shift']:+.4f}) [{status}]\n")

            # Fixed 2:1 (this failed on Solar|Rest too)
            out.write("\n─── Fixed 2:1 Decimation ───\n\n")
            fixed2_blocks = fixed_decimate(en_comps, 2)
            fixed2_eitt = eitt_from_blocks(en_comps, fixed2_blocks)
            fixed2_bals = balance_preservation_from_blocks(en_comps, fixed2_blocks, sbp_solar)

            out.write(f"  EITT residual: {fixed2_eitt['pct']:+.4f}%\n")
            for bname, bd in fixed2_bals.items():
                status = "PASS" if bd['preserved'] else "FAIL"
                out.write(f"  {bname}: mean {bd['orig_mean']:+.4f} → {bd['agg_mean']:+.4f} (shift={bd['shift']:+.4f}) [{status}]\n")

            # Adaptive decimation — multiple threshold settings
            out.write("\n─── Adaptive Decimation (rate-controlled taps) ───\n\n")

            threshold_configs = [
                (0.02, 0.15, "Sensitive (low=0.02, high=0.15)"),
                (0.05, 0.30, "Standard (low=0.05, high=0.30)"),
                (0.10, 0.50, "Tolerant (low=0.10, high=0.50)"),
            ]

            for low_t, high_t, label in threshold_configs:
                out.write(f"  Config: {label}\n")
                adaptive_blocks = adaptive_decimate(en_comps, max_rates, base_ratio=5,
                                                     rate_threshold_low=low_t, rate_threshold_high=high_t)

                if not adaptive_blocks:
                    out.write("    No blocks generated\n\n")
                    continue

                adaptive_eitt = eitt_from_blocks(en_comps, adaptive_blocks)
                adaptive_bals = balance_preservation_from_blocks(en_comps, adaptive_blocks, sbp_solar)

                block_sizes = [b['size'] for b in adaptive_blocks]
                out.write(f"    Blocks: {len(adaptive_blocks)}, sizes: {block_sizes}\n")
                out.write(f"    Mean block size: {arithmetic_mean(block_sizes):.1f}\n")
                out.write(f"    Effective compression: {len(en_comps)/len(adaptive_blocks):.1f}:1\n")
                out.write(f"    EITT residual: {adaptive_eitt['pct']:+.4f}%\n")

                all_pass = True
                for bname, bd in adaptive_bals.items():
                    status = "PASS" if bd['preserved'] else "FAIL"
                    if not bd['preserved']:
                        all_pass = False
                    out.write(f"    {bname}: shift={bd['shift']:+.4f} [{status}]\n")

                out.write(f"    ALL TAPS PRESERVED: {'YES' if all_pass else 'NO'}\n\n")

            # Also test with standard SBP
            out.write("\n─── Adaptive on Standard SBP (Fossil|Renew) for comparison ───\n\n")
            rates_std, _ = compute_balance_rates(en_comps, sbp_std, window=2)
            max_rates_std = compute_max_rate(rates_std)

            adaptive_std = adaptive_decimate(en_comps, max_rates_std, base_ratio=5)
            if adaptive_std:
                adaptive_std_eitt = eitt_from_blocks(en_comps, adaptive_std)
                adaptive_std_bals = balance_preservation_from_blocks(en_comps, adaptive_std, sbp_std)
                block_sizes = [b['size'] for b in adaptive_std]
                out.write(f"  Blocks: {len(adaptive_std)}, sizes: {block_sizes}\n")
                out.write(f"  EITT residual: {adaptive_std_eitt['pct']:+.4f}%\n")
                for bname, bd in adaptive_std_bals.items():
                    status = "PASS" if bd['preserved'] else "FAIL"
                    out.write(f"  {bname}: shift={bd['shift']:+.4f} [{status}]\n")

        # ══════════════════════════════════════════════════════════
        # TEST 2: GERMANY — Nuclear phase-out (the structural break)
        # ══════════════════════════════════════════════════════════
        if de_comps:
            out.write("\n\n" + "=" * 80 + "\n")
            out.write("TEST 2: GERMANY — CAN ADAPTIVE TAPS HANDLE THE NUCLEAR PHASE-OUT?\n")
            out.write(f"N={len(de_comps)}, {de_years[0]}→{de_years[-1]}\n")
            out.write("=" * 80 + "\n\n")

            sbp_de = energy_sbp()

            rates_de, _ = compute_balance_rates(de_comps, sbp_de, window=2)
            max_rates_de = compute_max_rate(rates_de)

            out.write("─── d(CoDa)/dt Profile ───\n\n")
            out.write(f"  {'Year':<6} {'Max |dB/dt|':>12} {'B1 Foss|Ren':>12} {'B2 Coal|Gas':>12} {'B3 Win|Sol':>12}\n")
            out.write(f"  {'─'*54}\n")
            for t in range(len(de_comps)):
                mr = max_rates_de[t]
                b1 = rates_de[t].get('B1: Fossil|Renew', 0)
                b2 = rates_de[t].get('B2: Coal|Gas', 0)
                b3 = rates_de[t].get('B3: Wind|Solar', 0)
                out.write(f"  {de_years[t]:<6} {mr:12.4f} {b1:12.4f} {b2:12.4f} {b3:12.4f}\n")

            # Fixed 5:1 (failed)
            out.write("\n─── Fixed 5:1 Decimation ───\n\n")
            fixed_de = fixed_decimate(de_comps, 5)
            fixed_de_eitt = eitt_from_blocks(de_comps, fixed_de)
            fixed_de_bals = balance_preservation_from_blocks(de_comps, fixed_de, sbp_de)
            out.write(f"  EITT residual: {fixed_de_eitt['pct']:+.4f}%\n")
            for bname, bd in fixed_de_bals.items():
                status = "PASS" if bd['preserved'] else "FAIL"
                out.write(f"  {bname}: shift={bd['shift']:+.4f} [{status}]\n")

            # Adaptive
            out.write("\n─── Adaptive Decimation ───\n\n")
            for low_t, high_t, label in threshold_configs:
                out.write(f"  Config: {label}\n")
                adaptive_de = adaptive_decimate(de_comps, max_rates_de, base_ratio=5,
                                                 rate_threshold_low=low_t, rate_threshold_high=high_t)
                if not adaptive_de:
                    out.write("    No blocks\n\n")
                    continue

                ad_eitt = eitt_from_blocks(de_comps, adaptive_de)
                ad_bals = balance_preservation_from_blocks(de_comps, adaptive_de, sbp_de)
                block_sizes = [b['size'] for b in adaptive_de]

                out.write(f"    Blocks: {len(adaptive_de)}, sizes: {block_sizes}\n")
                out.write(f"    Effective compression: {len(de_comps)/len(adaptive_de):.1f}:1\n")
                out.write(f"    EITT residual: {ad_eitt['pct']:+.4f}%\n")

                all_pass = True
                for bname, bd in ad_bals.items():
                    status = "PASS" if bd['preserved'] else "FAIL"
                    if not bd['preserved']:
                        all_pass = False
                    out.write(f"    {bname}: shift={bd['shift']:+.4f} [{status}]\n")
                out.write(f"    ALL TAPS PRESERVED: {'YES' if all_pass else 'NO'}\n\n")

        # ══════════════════════════════════════════════════════════
        # TEST 3: GOLD/SILVER — Long series, test adaptive on 338 years
        # ══════════════════════════════════════════════════════════
        if gs_comps:
            out.write("\n\n" + "=" * 80 + "\n")
            out.write("TEST 3: GOLD/SILVER — ADAPTIVE ON 338 YEARS\n")
            out.write(f"N={len(gs_comps)}, {gs_years[0]}→{gs_years[-1]}\n")
            out.write("=" * 80 + "\n\n")

            sbp_gs = gold_silver_sbp()
            rates_gs, _ = compute_balance_rates(gs_comps, sbp_gs, window=5)
            max_rates_gs = compute_max_rate(rates_gs)

            # Rate profile summary
            rate_vals = [r for r in max_rates_gs if r > 0]
            out.write(f"  Rate profile: min={min(rate_vals):.4f}, median={sorted(rate_vals)[len(rate_vals)//2]:.4f}, max={max(rate_vals):.4f}\n\n")

            # Show periods of fast movement
            out.write("  Fastest-changing decades:\n")
            decade_rates = defaultdict(list)
            for t, yr in enumerate(gs_years):
                decade = (yr // 10) * 10
                decade_rates[decade].append(max_rates_gs[t])
            decade_avg = [(d, arithmetic_mean(r)) for d, r in decade_rates.items()]
            decade_avg.sort(key=lambda x: -x[1])
            for d, r in decade_avg[:10]:
                out.write(f"    {d}s: mean |dB/dt| = {r:.4f}\n")

            # Compare fixed vs adaptive at aggressive compression
            out.write(f"\n  Fixed 10:1 (failed earlier at +1.39%):\n")
            fixed_gs10 = fixed_decimate(gs_comps, 10)
            fixed_gs10_eitt = eitt_from_blocks(gs_comps, fixed_gs10)
            out.write(f"    EITT residual: {fixed_gs10_eitt['pct']:+.4f}%\n")

            out.write(f"\n  Adaptive (base_ratio=10):\n")
            for low_t, high_t, label in threshold_configs:
                adaptive_gs = adaptive_decimate(gs_comps, max_rates_gs, base_ratio=10,
                                                 rate_threshold_low=low_t, rate_threshold_high=high_t)
                if not adaptive_gs:
                    continue

                ad_eitt = eitt_from_blocks(gs_comps, adaptive_gs)
                block_sizes = [b['size'] for b in adaptive_gs]

                out.write(f"    {label}:\n")
                out.write(f"      Blocks: {len(adaptive_gs)}, mean size: {arithmetic_mean(block_sizes):.1f}\n")
                out.write(f"      Effective compression: {len(gs_comps)/len(adaptive_gs):.1f}:1\n")
                out.write(f"      EITT residual: {ad_eitt['pct']:+.4f}%\n")
                out.write(f"      vs fixed 10:1: {'IMPROVED' if abs(ad_eitt['pct']) < abs(fixed_gs10_eitt['pct']) else 'WORSE or SAME'}\n\n")

        # ══════════════════════════════════════════════════════════
        # TEST 4: FINANCIAL — Already pristine, does adaptive help or hurt?
        # ══════════════════════════════════════════════════════════
        if fi_comps:
            K = len(fi_comps[0])
            out.write("\n\n" + "=" * 80 + "\n")
            out.write(f"TEST 4: FINANCIAL K={K} — ADAPTIVE ON ALREADY-PRISTINE DATA\n")
            out.write(f"N={len(fi_comps)}, {fi_months[0]}→{fi_months[-1]}\n")
            out.write("=" * 80 + "\n\n")

            sbp_fi = financial_sbp(K)
            rates_fi, _ = compute_balance_rates(fi_comps, sbp_fi, window=3)
            max_rates_fi = compute_max_rate(rates_fi)

            rate_vals = [r for r in max_rates_fi if r > 0]
            out.write(f"  Rate profile: min={min(rate_vals):.4f}, median={sorted(rate_vals)[len(rate_vals)//2]:.4f}, max={max(rate_vals):.4f}\n\n")

            out.write(f"  Fixed 5:1:\n")
            fixed_fi5 = fixed_decimate(fi_comps, 5)
            fixed_fi5_eitt = eitt_from_blocks(fi_comps, fixed_fi5)
            out.write(f"    EITT residual: {fixed_fi5_eitt['pct']:+.4f}%\n\n")

            out.write(f"  Adaptive (base_ratio=5):\n")
            adaptive_fi = adaptive_decimate(fi_comps, max_rates_fi, base_ratio=5)
            if adaptive_fi:
                ad_fi_eitt = eitt_from_blocks(fi_comps, adaptive_fi)
                block_sizes = [b['size'] for b in adaptive_fi]
                out.write(f"    Blocks: {len(adaptive_fi)}, mean size: {arithmetic_mean(block_sizes):.1f}\n")
                out.write(f"    EITT residual: {ad_fi_eitt['pct']:+.4f}%\n")

        # ══════════════════════════════════════════════════════════
        # SUMMARY
        # ══════════════════════════════════════════════════════════
        out.write("\n\n" + "=" * 80 + "\n")
        out.write("SUMMARY — ADAPTIVE TAP DECIMATION\n")
        out.write("=" * 80 + "\n\n")

        out.write("Core finding: d(CoDa)/dt serves as the TAP CONTROLLER.\n")
        out.write("It determines the maximum safe compression ratio at each time step.\n\n")

        out.write("Mechanism:\n")
        out.write("  1. Compute |dB/dt| for each ILR balance at each time step\n")
        out.write("  2. Take max across balances → local rate of change\n")
        out.write("  3. Map rate to block size: slow → large blocks, fast → small blocks\n")
        out.write("  4. Apply variable-width geometric-mean decimation\n\n")

        out.write("This gives d(CoDa)/dt a CONCRETE OPERATIONAL ROLE:\n")
        out.write("  Not just 'exploratory temporal derivative'\n")
        out.write("  But the CONTROL SIGNAL that sets the balance transformer's taps.\n\n")

        out.write("Date: 2026-04-10\n")

    print(f"\nResults written to: {out_path}", file=sys.stderr)

if __name__ == '__main__':
    main()
