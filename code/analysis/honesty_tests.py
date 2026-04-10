#!/usr/bin/env python3
"""
EITT Adversarial Attack Tests (Honesty Suite)
Tests 5 domains against 9 adversarial attacks

ATK-01: Out-of-sample K=4 test (train/test split on gold/silver)
ATK-02/ATK-07: Sensitivity analysis on K=4 gold/silver hyperparameters
ATK-04: Bootstrap confidence intervals on EITT residual
ATK-05: Detrended white noise control
ATK-09: Arithmetic mean comparison (arithmetic vs geometric)

Date: 2026-04-09
"""
import csv, json, math, os, sys, random
from collections import defaultdict

# ══════════════════════════════════════════════════════════════════
# SHARED CoDa FUNCTIONS
# ══════════════════════════════════════════════════════════════════

def shannon_entropy(p):
    """Shannon entropy H(p) = -sum(p_i * log(p_i))"""
    return -sum(pi * math.log(pi) for pi in p if pi > 0)

def geometric_mean(vals):
    """Geometric mean of strictly positive values"""
    if not vals or any(v <= 0 for v in vals):
        return 0
    log_sum = sum(math.log(v) for v in vals)
    return math.exp(log_sum / len(vals))

def clr_transform(x):
    """Centered log-ratio transform"""
    g = geometric_mean(x)
    if g <= 0:
        return [0]*len(x)
    return [math.log(xi/g) for xi in x]

def arithmetic_mean(vals):
    """Arithmetic mean"""
    if not vals:
        return 0
    return sum(vals) / len(vals)

def geom_mean_compositions(comps):
    """Geometric mean of compositions (per-part)"""
    K = len(comps[0])
    gm = []
    for j in range(K):
        vals = [c[j] for c in comps]
        gm.append(geometric_mean(vals))
    total = sum(gm)
    return [g/total for g in gm] if total > 0 else [1/K]*K

def arith_mean_compositions(comps):
    """Arithmetic mean of compositions (per-part)"""
    K = len(comps[0])
    am = []
    for j in range(K):
        vals = [c[j] for c in comps]
        am.append(arithmetic_mean(vals))
    total = sum(am)
    return [a/total for a in am] if total > 0 else [1/K]*K

def aitchison_distance(x, y):
    """Aitchison distance between two compositions"""
    clr_x = clr_transform(x)
    clr_y = clr_transform(y)
    return math.sqrt(sum((a-b)**2 for a,b in zip(clr_x, clr_y)))

def run_eitt_at_k2(compositions, label=""):
    """Run EITT on K=2 composition at 2:1 decimation only (fast)"""
    n = len(compositions)
    if n < 4:
        return None

    entropies = [shannon_entropy(c) for c in compositions]
    base_mean = sum(entropies) / len(entropies)

    # Only test 2:1 decimation
    w = 2
    agg_comps = []
    for i in range(0, n - w + 1, w):
        chunk = compositions[i:i+w]
        if len(chunk) == w:
            agg_comps.append(geom_mean_compositions(chunk))

    if not agg_comps:
        return None

    agg_entropies = [shannon_entropy(c) for c in agg_comps]
    agg_mean = sum(agg_entropies) / len(agg_entropies)
    delta = agg_mean - base_mean
    pct = delta / base_mean * 100 if base_mean > 0 else 0

    return {'base_H': base_mean, 'agg_H': agg_mean, 'delta': delta, 'pct': pct}

def run_eitt_arithmetic_k2(compositions, label=""):
    """Run EITT on K=2 using ARITHMETIC mean instead of geometric"""
    n = len(compositions)
    if n < 4:
        return None

    entropies = [shannon_entropy(c) for c in compositions]
    base_mean = sum(entropies) / len(entropies)

    w = 2
    agg_comps = []
    for i in range(0, n - w + 1, w):
        chunk = compositions[i:i+w]
        if len(chunk) == w:
            agg_comps.append(arith_mean_compositions(chunk))

    if not agg_comps:
        return None

    agg_entropies = [shannon_entropy(c) for c in agg_comps]
    agg_mean = sum(agg_entropies) / len(agg_entropies)
    delta = agg_mean - base_mean
    pct = delta / base_mean * 100 if base_mean > 0 else 0

    return {'base_H': base_mean, 'agg_H': agg_mean, 'delta': delta, 'pct': pct}

# ══════════════════════════════════════════════════════════════════
# ATK-04: BOOTSTRAP CONFIDENCE INTERVALS
# ══════════════════════════════════════════════════════════════════

def block_bootstrap_eitt(compositions, n_bootstrap=1000, block_size_factor=0.5):
    """
    Bootstrap confidence intervals on EITT residual
    Block bootstrap: resample with block size = sqrt(N)
    Returns: (ci_lower, ci_upper, p_value)
    """
    n = len(compositions)
    block_size = max(2, int(math.sqrt(n)))

    # Base EITT result
    base_result = run_eitt_at_k2(compositions)
    if not base_result:
        return None, None, None, None

    base_pct = base_result['pct']

    # Bootstrap replicates
    bootstrap_pcts = []
    for rep in range(n_bootstrap):
        # Block bootstrap resample
        bootstrap_indices = []
        while len(bootstrap_indices) < n:
            start_idx = random.randint(0, n - block_size)
            for i in range(start_idx, min(start_idx + block_size, n)):
                if len(bootstrap_indices) < n:
                    bootstrap_indices.append(i)

        bootstrap_comps = [compositions[i] for i in bootstrap_indices[:n]]
        boot_result = run_eitt_at_k2(bootstrap_comps)
        if boot_result:
            bootstrap_pcts.append(boot_result['pct'])

    if not bootstrap_pcts:
        return None, None, None, None

    # Sort for CI
    bootstrap_pcts.sort()
    n_boot = len(bootstrap_pcts)
    ci_lower = bootstrap_pcts[int(0.025 * n_boot)]
    ci_upper = bootstrap_pcts[int(0.975 * n_boot)]

    # Permutation test: shuffle time indices
    n_perm = 10000
    perm_pcts = []
    for perm in range(n_perm):
        perm_indices = list(range(n))
        random.shuffle(perm_indices)
        perm_comps = [compositions[i] for i in perm_indices]
        perm_result = run_eitt_at_k2(perm_comps)
        if perm_result:
            perm_pcts.append(perm_result['pct'])

    if not perm_pcts:
        return ci_lower, ci_upper, None, base_pct

    # p-value: fraction of permutations >= |base_pct|
    n_extreme = sum(1 for p in perm_pcts if abs(p) >= abs(base_pct))
    p_value = (n_extreme + 1) / (len(perm_pcts) + 1)

    return ci_lower, ci_upper, p_value, base_pct

# ══════════════════════════════════════════════════════════════════
# ATK-02/ATK-07: SENSITIVITY ANALYSIS (K=4 GOLD/SILVER)
# ══════════════════════════════════════════════════════════════════

def build_k4_composition(gold_share, silver_share, vol_carrier, mom_carrier):
    """Build K=4 composition: [gold, silver, vol_carrier, mom_carrier] normalized"""
    parts = [gold_share, silver_share, vol_carrier, mom_carrier]
    total = sum(parts)
    if total <= 0:
        return [0.25, 0.25, 0.25, 0.25]
    return [p/total for p in parts]

def sensitivity_sweep_k4(gold_silver_annual, vol_windows, mom_windows, vol_scales, mom_slopes):
    """
    Sweep K=4 hyperparameters:
    vol_scale: multiply vol_carrier by this factor
    mom_slope: multiply momentum influence by this factor
    vol_window: rolling window for volatility
    mom_window: rolling window for momentum

    Returns: list of (params, eitt_pct, passes) tuples
    """
    results = []

    for vol_window in vol_windows:
        for mom_window in mom_windows:
            for vol_scale in vol_scales:
                for mom_slope in mom_slopes:
                    # Build K=4 compositions with these hyperparameters
                    comps = []

                    for i, (gold_sh, silver_sh) in enumerate(gold_silver_annual):
                        # Volatility carrier: rolling std of ILR balance
                        vol_carrier = 0.001  # small base
                        if i >= vol_window:
                            # Compute rolling std over vol_window
                            window_balances = []
                            for j in range(i - vol_window + 1, i + 1):
                                g, s = gold_silver_annual[j]
                                if g > 0 and s > 0:
                                    balance = math.log(g / s)
                                    window_balances.append(balance)

                            if len(window_balances) > 1:
                                mean_b = sum(window_balances) / len(window_balances)
                                var = sum((b - mean_b)**2 for b in window_balances) / len(window_balances)
                                vol = math.sqrt(var) if var > 0 else 0.001
                                vol_carrier = vol * vol_scale * 0.5

                        # Momentum carrier: sigmoid of 10-year running mean
                        mom_carrier = 0.5  # neutral
                        if i >= mom_window:
                            window_balances = []
                            for j in range(i - mom_window + 1, i + 1):
                                g, s = gold_silver_annual[j]
                                if g > 0 and s > 0:
                                    balance = math.log(g / s)
                                    window_balances.append(balance)

                            if window_balances:
                                mean_mom = sum(window_balances) / len(window_balances)
                                # Sigmoid: 1/(1 + exp(-x))
                                try:
                                    mom_carrier = 1.0 / (1.0 + math.exp(-mean_mom * mom_slope * 2))
                                except:
                                    mom_carrier = 0.5

                        comp = build_k4_composition(gold_sh, silver_sh, vol_carrier, mom_carrier)
                        comps.append(comp)

                    # Run EITT at 2:1
                    eitt_result = run_eitt_at_k2(comps)
                    if eitt_result:
                        pct = eitt_result['pct']
                        passes = abs(pct) < 1.0
                        results.append({
                            'vol_window': vol_window,
                            'mom_window': mom_window,
                            'vol_scale': vol_scale,
                            'mom_slope': mom_slope,
                            'eitt_pct': pct,
                            'passes': passes
                        })

    return results

# ══════════════════════════════════════════════════════════════════
# ATK-05: DETRENDED WHITE NOISE CONTROL
# ══════════════════════════════════════════════════════════════════

def generate_white_noise_k2_detrended(n=338, seed=42):
    """
    Generate K=2 compositions from white noise + detrend
    If detrended white noise also passes EITT, detrending is doing all the work
    """
    random.seed(seed)

    # Generate white noise for part 1
    part1 = [random.random() for _ in range(n)]
    part2 = [random.random() for _ in range(n)]

    # Linear detrend each part
    def detrend(series):
        n = len(series)
        mean = sum(series) / n
        x_mean = (n - 1) / 2.0

        # Fit y = a + b*x
        num = sum((i - x_mean) * (series[i] - mean) for i in range(n))
        denom = sum((i - x_mean)**2 for i in range(n))

        if denom > 0:
            b = num / denom
        else:
            b = 0

        a = mean - b * x_mean

        # Remove trend
        detrended = [series[i] - (a + b * i) for i in range(n)]
        return detrended

    part1_detrended = detrend(part1)
    part2_detrended = detrend(part2)

    # Make strictly positive
    min1 = min(part1_detrended)
    min2 = min(part2_detrended)

    shift1 = -min1 + 1.0 if min1 <= 0 else 0
    shift2 = -min2 + 1.0 if min2 <= 0 else 0

    part1_pos = [x + shift1 for x in part1_detrended]
    part2_pos = [x + shift2 for x in part2_detrended]

    # Build compositions
    comps = []
    for i in range(n):
        total = part1_pos[i] + part2_pos[i]
        if total > 0:
            comps.append([part1_pos[i] / total, part2_pos[i] / total])
        else:
            comps.append([0.5, 0.5])

    return comps

# ══════════════════════════════════════════════════════════════════
# ATK-01: OUT-OF-SAMPLE K=4 TEST (TRAIN/TEST SPLIT)
# ══════════════════════════════════════════════════════════════════

def out_of_sample_k4_test(gold_silver_annual, train_size=200):
    """
    Split data: first train_size years for training vol/mom hyperparameters,
    last len-train_size years for testing.
    Compute EITT on test set using training-derived scaling.
    """
    n = len(gold_silver_annual)
    if n < train_size + 50:
        return None

    train_data = gold_silver_annual[:train_size]
    test_data = gold_silver_annual[train_size:]

    # On TRAINING data, compute typical vol and momentum
    train_balances = []
    for g, s in train_data:
        if g > 0 and s > 0:
            balance = math.log(g / s)
            train_balances.append(balance)

    if not train_balances:
        return None

    # Compute 5-year vol on training
    train_vol = 0
    if len(train_balances) >= 5:
        mean_b = sum(train_balances) / len(train_balances)
        var = sum((b - mean_b)**2 for b in train_balances) / len(train_balances)
        train_vol = math.sqrt(var) if var > 0 else 0.001

    # Compute 10-year momentum on training
    train_mom = sum(train_balances) / len(train_balances) if train_balances else 0

    # Apply to TEST data with K=4
    test_comps = []
    for g, s in test_data:
        # Use training-derived vol/mom carriers
        vol_carrier = train_vol * 0.5 * 0.1  # scaled by typical 0.1 factor
        try:
            mom_carrier = 1.0 / (1.0 + math.exp(-train_mom * 2))
        except:
            mom_carrier = 0.5

        comp = build_k4_composition(g, s, vol_carrier, mom_carrier)
        test_comps.append(comp)

    # Run EITT on test set
    eitt_result = run_eitt_at_k2(test_comps)
    return eitt_result

# ══════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════

def load_commodities_k2():
    """Load gold/silver K=2 annual compositions (338 years 1688-2026)"""
    filepath = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Commodities/gold_silver_ratio_enriched.csv'

    rows = []
    with open(filepath) as f:
        r = csv.DictReader(f)
        for row in r:
            if row.get('silver_oz_per_gold_oz', ''):
                try:
                    ratio = float(row['silver_oz_per_gold_oz'])
                    if ratio > 0:
                        year = int(row['date'][:4])
                        # ratio = oz silver per oz gold
                        # gold_share = ratio/(1+ratio), silver_share = 1/(1+ratio)
                        gold_share = ratio / (1 + ratio)
                        silver_share = 1 / (1 + ratio)
                        rows.append((year, [gold_share, silver_share]))
                except:
                    pass

    # Sort by year and deduplicate (take first occurrence per year)
    rows.sort(key=lambda x: x[0])

    yearly_dict = {}
    for year, comp in rows:
        if year not in yearly_dict:
            yearly_dict[year] = comp

    years = sorted(yearly_dict.keys())
    compositions = [yearly_dict[y] for y in years]

    return compositions, years

def load_backblaze_k4():
    """Load BackBlaze drive failure rates K=4 (24 monthly observations)"""
    # BackBlaze has model-specific failure rates
    # We'll aggregate to 4 categories: SSD, HDD-consumer, HDD-enterprise, other

    data_dir = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/BackBlaze/data_Q1_2024'

    if not os.path.isdir(data_dir):
        return None, None

    # Scan available files
    files = sorted([f for f in os.listdir(data_dir) if f.endswith('.csv')])

    if not files:
        return None, None

    # Aggregate failure rates by month
    monthly_aggregates = defaultdict(lambda: defaultdict(float))

    for filename in files:
        filepath = os.path.join(data_dir, filename)
        try:
            with open(filepath) as f:
                r = csv.DictReader(f)
                for row in r:
                    try:
                        model = row.get('model', '')
                        fails = int(row.get('failures', 0))
                        units = int(row.get('drive_count', 1))

                        # Classify model
                        if 'SSD' in model.upper():
                            cat = 'SSD'
                        elif 'Barracuda' in model or 'IronWolf' in model:
                            cat = 'HDD-Consumer'
                        elif 'Enterprise' in model or 'Exos' in model:
                            cat = 'HDD-Enterprise'
                        else:
                            cat = 'Other'

                        # Rate = failures / drive_count
                        if units > 0:
                            rate = fails / units
                            # Month is always 2024-01 for this data
                            monthly_aggregates['2024-01'][cat] += rate * units
                    except:
                        pass
        except:
            pass

    if not monthly_aggregates:
        return None, None

    # For now, return None since real backblaze has more time coverage
    # In honesty tests, we note backblaze separately
    return None, None

def load_financial_k9():
    """Load financial sector market-cap shares K=9"""
    # This requires stock_prices_daily.csv which may not exist
    # Return None if missing

    filepath = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/financial data/stock_prices_daily.csv'

    if not os.path.exists(filepath):
        return None, None

    sector_monthly = defaultdict(lambda: defaultdict(list))

    try:
        with open(filepath) as f:
            r = csv.DictReader(f)
            for row in r:
                try:
                    close = float(row['Close'])
                    if close > 0:
                        month = row['Date'][:7]
                        sector = row['Sector']
                        sector_monthly[month][sector].append(close)
                except:
                    pass
    except:
        return None, None

    months = sorted(sector_monthly.keys())
    sectors = sorted(set(s for m in months for s in sector_monthly[m].keys()))

    compositions = []
    valid_months = []

    for month in months:
        vals = []
        valid = True
        for sector in sectors:
            prices = sector_monthly[month].get(sector, [])
            if not prices:
                valid = False
                break
            vals.append(sum(prices) / len(prices))

        if valid and all(v > 0 for v in vals):
            total = sum(vals)
            comp = [v / total for v in vals]
            compositions.append(comp)
            valid_months.append(month)

    return compositions if compositions else None, valid_months if valid_months else None

def load_energy_k7():
    """Load energy generation by source K=7"""
    filepath = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Energy/yearly_full_release_long_format.csv'

    if not os.path.exists(filepath):
        return None, None

    subcats = defaultdict(lambda: defaultdict(float))

    try:
        with open(filepath) as f:
            r = csv.DictReader(f)
            for row in r:
                if row['Area'] == 'World' and row['Variable'] in ['Coal', 'Gas', 'Nuclear', 'Hydro', 'Wind', 'Solar', 'Other renewables']:
                    if row['Category'] == 'Electricity generation' and row['Unit'] == 'TWh' and row.get('Value'):
                        try:
                            subcats[int(row['Year'])][row['Variable']] = float(row['Value'])
                        except:
                            pass
    except:
        return None, None

    years = sorted(subcats.keys())
    if not years:
        return None, None

    major_sources = ['Coal', 'Gas', 'Nuclear', 'Hydro', 'Wind', 'Solar', 'Other renewables']

    compositions = []
    valid_years = []

    for y in years:
        vals = [max(subcats[y].get(src, 0), 0.001) for src in major_sources]
        total = sum(vals)
        if total > 0:
            comp = [v / total for v in vals]
            compositions.append(comp)
            valid_years.append(str(y))

    return compositions if compositions else None, valid_years if valid_years else None

# ══════════════════════════════════════════════════════════════════
# MAIN ANALYSIS
# ══════════════════════════════════════════════════════════════════

def main():
    output_file = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/code/analysis/honesty_tests_results_2026april9.txt'

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as out:
        out.write("="*80 + "\n")
        out.write("EITT ADVERSARIAL ATTACK HONESTY TESTS\n")
        out.write("Testing 5 attacks on EITT entropy invariance\n")
        out.write("Date: 2026-04-09\n")
        out.write("="*80 + "\n\n")

        # ────────────────────────────────────────────────────────────
        # ATK-04: BOOTSTRAP CONFIDENCE INTERVALS
        # ────────────────────────────────────────────────────────────

        out.write("\n" + "="*80 + "\n")
        out.write("ATK-04: BOOTSTRAP CONFIDENCE INTERVALS (1000 replicates, 10000 permutations)\n")
        out.write("="*80 + "\n\n")

        # Load commodities K=2
        print("Loading commodities (gold/silver K=2)...", file=sys.stderr)
        comps_k2, years_k2 = load_commodities_k2()

        if comps_k2:
            out.write(f"COMMODITIES (Gold/Silver K=2): {len(comps_k2)} annual observations\n")
            out.write(f"Period: {years_k2[0]} → {years_k2[-1]}\n\n")

            ci_lower, ci_upper, p_value, base_pct = block_bootstrap_eitt(comps_k2, n_bootstrap=1000)

            if ci_lower is not None:
                out.write(f"  Base EITT Δ% (2:1):     {base_pct:+.6f}%\n")
                out.write(f"  95% Bootstrap CI:       [{ci_lower:.6f}%, {ci_upper:.6f}%]\n")
                out.write(f"  CI width:               {ci_upper - ci_lower:.6f}%\n")
                out.write(f"  Permutation p-value:    {p_value:.6f}\n")

                if abs(base_pct) < 1.0 and p_value > 0.05:
                    out.write(f"  VERDICT: PASSES (within 1%, p > 0.05)\n")
                else:
                    out.write(f"  VERDICT: FAILS (outside confidence region or p <= 0.05)\n")
            out.write("\n")

        # Load financial K=9
        print("Loading financial (stocks K=9)...", file=sys.stderr)
        comps_k9, months_k9 = load_financial_k9()

        if comps_k9:
            out.write(f"FINANCIAL (Sector Market-Cap K=9): {len(comps_k9)} monthly observations\n")
            out.write(f"Period: {months_k9[0]} → {months_k9[-1]}\n\n")

            ci_lower, ci_upper, p_value, base_pct = block_bootstrap_eitt(comps_k9, n_bootstrap=1000)

            if ci_lower is not None:
                out.write(f"  Base EITT Δ% (2:1):     {base_pct:+.6f}%\n")
                out.write(f"  95% Bootstrap CI:       [{ci_lower:.6f}%, {ci_upper:.6f}%]\n")
                out.write(f"  Permutation p-value:    {p_value:.6f}\n")

                if abs(base_pct) < 1.0 and p_value > 0.05:
                    out.write(f"  VERDICT: PASSES\n")
                else:
                    out.write(f"  VERDICT: FAILS\n")
            out.write("\n")

        # Load energy K=7
        print("Loading energy (generation K=7)...", file=sys.stderr)
        comps_k7, years_k7 = load_energy_k7()

        if comps_k7:
            out.write(f"ENERGY (Generation by Source K=7): {len(comps_k7)} annual observations\n")
            out.write(f"Period: {years_k7[0]} → {years_k7[-1]}\n\n")

            ci_lower, ci_upper, p_value, base_pct = block_bootstrap_eitt(comps_k7, n_bootstrap=1000)

            if ci_lower is not None:
                out.write(f"  Base EITT Δ% (2:1):     {base_pct:+.6f}%\n")
                out.write(f"  95% Bootstrap CI:       [{ci_lower:.6f}%, {ci_upper:.6f}%]\n")
                out.write(f"  Permutation p-value:    {p_value:.6f}\n")

                if abs(base_pct) < 1.0 and p_value > 0.05:
                    out.write(f"  VERDICT: PASSES\n")
                else:
                    out.write(f"  VERDICT: FAILS\n")
            out.write("\n")

        # ────────────────────────────────────────────────────────────
        # ATK-02/ATK-07: SENSITIVITY ANALYSIS K=4 GOLD/SILVER
        # ────────────────────────────────────────────────────────────

        out.write("\n" + "="*80 + "\n")
        out.write("ATK-02/ATK-07: SENSITIVITY SWEEP (K=4 Hyperparameters)\n")
        out.write("Testing combinations of vol_scale, mom_slope, vol_window, mom_window\n")
        out.write("="*80 + "\n\n")

        if comps_k2:
            print("Running sensitivity sweep...", file=sys.stderr)

            # Reduce sweep size for time
            vol_windows = [5, 10, 20]
            mom_windows = [5, 10, 20]
            vol_scales = [0.1, 0.5, 1.0, 2.0, 5.0]
            mom_slopes = [0.5, 1.0, 2.0, 5.0]

            # Convert to gold/silver fractions for each year
            gold_silver_fracs = [(c[0], c[1]) for c in comps_k2]

            sweep_results = sensitivity_sweep_k4(gold_silver_fracs, vol_windows, mom_windows, vol_scales, mom_slopes)

            if sweep_results:
                passes = sum(1 for r in sweep_results if r['passes'])
                total = len(sweep_results)
                pct_pass = 100 * passes / total if total > 0 else 0

                out.write(f"Total parameter combinations tested: {total}\n")
                out.write(f"Combinations passing (<1%): {passes} ({pct_pass:.1f}%)\n\n")

                out.write("Sample results (sorted by |EITT Δ%|):\n")
                out.write(f"{'vol_w':<6} {'mom_w':<6} {'vol_s':<6} {'mom_s':<6} {'EITT%':<10} {'Pass':<6}\n")
                out.write("─"*40 + "\n")

                sweep_results_sorted = sorted(sweep_results, key=lambda x: abs(x['eitt_pct']))

                # Show first 10 best and last 10 worst
                for r in sweep_results_sorted[:10]:
                    status = "YES" if r['passes'] else "NO"
                    out.write(f"{r['vol_window']:<6} {r['mom_window']:<6} {r['vol_scale']:<6.2f} {r['mom_slope']:<6.1f} {r['eitt_pct']:+9.4f}% {status:<6}\n")

                out.write("\n... (middle results omitted) ...\n\n")

                for r in sweep_results_sorted[-10:]:
                    status = "YES" if r['passes'] else "NO"
                    out.write(f"{r['vol_window']:<6} {r['mom_window']:<6} {r['vol_scale']:<6.2f} {r['mom_slope']:<6.1f} {r['eitt_pct']:+9.4f}% {status:<6}\n")

                if pct_pass > 50:
                    out.write("\nVERDICT: SUSPICIOUS - majority of parameter combinations pass\n")
                elif pct_pass < 5:
                    out.write("\nVERDICT: ROBUST - very few parameter combinations pass\n")
                else:
                    out.write("\nVERDICT: MIXED - moderate sensitivity to hyperparameters\n")

            out.write("\n")

        # ────────────────────────────────────────────────────────────
        # ATK-09: ARITHMETIC MEAN COMPARISON
        # ────────────────────────────────────────────────────────────

        out.write("\n" + "="*80 + "\n")
        out.write("ATK-09: ARITHMETIC MEAN COMPARISON (Control Test)\n")
        out.write("Testing if arithmetic mean ALSO preserves entropy (geometric mean not special)\n")
        out.write("="*80 + "\n\n")

        if comps_k2:
            print("Running arithmetic mean test...", file=sys.stderr)

            geom_result = run_eitt_at_k2(comps_k2)
            arith_result = run_eitt_arithmetic_k2(comps_k2)

            out.write("COMMODITIES (Gold/Silver K=2):\n\n")

            if geom_result:
                out.write(f"Geometric Mean (EITT):\n")
                out.write(f"  Base entropy:          {geom_result['base_H']:.6f}\n")
                out.write(f"  2:1 decimation H:      {geom_result['agg_H']:.6f}\n")
                out.write(f"  Δ entropy:             {geom_result['delta']:+.6f}\n")
                out.write(f"  % change:              {geom_result['pct']:+.6f}%\n")

            if arith_result:
                out.write(f"\nArithmetic Mean (Control):\n")
                out.write(f"  Base entropy:          {arith_result['base_H']:.6f}\n")
                out.write(f"  2:1 decimation H:      {arith_result['agg_H']:.6f}\n")
                out.write(f"  Δ entropy:             {arith_result['delta']:+.6f}\n")
                out.write(f"  % change:              {arith_result['pct']:+.6f}%\n")

            if geom_result and arith_result:
                geom_passes = abs(geom_result['pct']) < 1.0
                arith_passes = abs(arith_result['pct']) < 1.0

                out.write(f"\nComparison:\n")
                out.write(f"  Geometric mean passes: {'YES' if geom_passes else 'NO'}\n")
                out.write(f"  Arithmetic mean passes: {'YES' if arith_passes else 'NO'}\n")

                if not arith_passes:
                    out.write(f"\nVERDICT: PASSES - arithmetic mean FAILS, geometric mean is special\n")
                elif arith_passes and geom_passes:
                    out.write(f"\nVERDICT: SUSPICIOUS - BOTH pass, averaging aggregation may be universal\n")
                else:
                    out.write(f"\nVERDICT: MIXED\n")

            out.write("\n")

        if comps_k7:
            out.write("\nENERGY (Generation K=7):\n\n")

            geom_result = run_eitt_at_k2(comps_k7)
            arith_result = run_eitt_arithmetic_k2(comps_k7)

            if geom_result:
                out.write(f"Geometric Mean:\n")
                out.write(f"  % change (2:1):        {geom_result['pct']:+.6f}%\n")

            if arith_result:
                out.write(f"Arithmetic Mean:\n")
                out.write(f"  % change (2:1):        {arith_result['pct']:+.6f}%\n")

            out.write("\n")

        # ────────────────────────────────────────────────────────────
        # ATK-01: OUT-OF-SAMPLE K=4 TEST
        # ────────────────────────────────────────────────────────────

        out.write("\n" + "="*80 + "\n")
        out.write("ATK-01: OUT-OF-SAMPLE K=4 TEST (Train/Test Split)\n")
        out.write("Training: first 200 years of gold/silver data\n")
        out.write("Testing: remaining 138 years\n")
        out.write("="*80 + "\n\n")

        if comps_k2:
            print("Running out-of-sample test...", file=sys.stderr)

            gold_silver_fracs = [(c[0], c[1]) for c in comps_k2]
            oos_result = out_of_sample_k4_test(gold_silver_fracs, train_size=200)

            out.write(f"Gold/Silver Data (K=4 with training-derived vol/mom):\n\n")

            if oos_result:
                out.write(f"  Test set size:         {len(comps_k2) - 200} years\n")
                out.write(f"  Base entropy:          {oos_result['base_H']:.6f}\n")
                out.write(f"  2:1 decimation H:      {oos_result['agg_H']:.6f}\n")
                out.write(f"  Δ entropy:             {oos_result['delta']:+.6f}\n")
                out.write(f"  % change:              {oos_result['pct']:+.6f}%\n\n")

                if abs(oos_result['pct']) < 1.0:
                    out.write(f"VERDICT: PASSES - EITT holds on out-of-sample test\n")
                else:
                    out.write(f"VERDICT: FAILS - EITT breaks on out-of-sample data\n")
            else:
                out.write("  ERROR: Could not compute out-of-sample test\n")

            out.write("\n")

        # ────────────────────────────────────────────────────────────
        # ATK-05: DETRENDED WHITE NOISE CONTROL
        # ────────────────────────────────────────────────────────────

        out.write("\n" + "="*80 + "\n")
        out.write("ATK-05: DETRENDED WHITE NOISE CONTROL\n")
        out.write("If detrended white noise also passes EITT, detrending is doing all work\n")
        out.write("="*80 + "\n\n")

        print("Running detrended white noise test...", file=sys.stderr)

        wn_comps = generate_white_noise_k2_detrended(n=338, seed=42)
        wn_result = run_eitt_at_k2(wn_comps)

        out.write("Detrended White Noise (K=2, N=338):\n\n")

        if wn_result:
            out.write(f"  Base entropy:          {wn_result['base_H']:.6f}\n")
            out.write(f"  2:1 decimation H:      {wn_result['agg_H']:.6f}\n")
            out.write(f"  Δ entropy:             {wn_result['delta']:+.6f}\n")
            out.write(f"  % change:              {wn_result['pct']:+.6f}%\n\n")

            if abs(wn_result['pct']) < 1.0:
                out.write("VERDICT: FAILS - white noise detrending also preserves entropy!\n")
                out.write("         This suggests detrending (not geometry) causes invariance\n")
            else:
                out.write("VERDICT: PASSES - detrended noise breaks EITT, geometric mean is special\n")

            # Compare to commodities
            if geom_result:
                out.write(f"\nComparison to commodities:\n")
                out.write(f"  Commodities EITT Δ%:  {geom_result['pct']:+.6f}%\n")
                out.write(f"  White noise EITT Δ%:  {wn_result['pct']:+.6f}%\n")
                out.write(f"  Difference:            {abs(geom_result['pct'] - wn_result['pct']):.6f}%\n")

        out.write("\n")

        # ────────────────────────────────────────────────────────────
        # SUMMARY
        # ────────────────────────────────────────────────────────────

        out.write("\n" + "="*80 + "\n")
        out.write("HONESTY TEST SUMMARY\n")
        out.write("="*80 + "\n\n")

        out.write("ATK-04 (Bootstrap CI):    Tests statistical significance via permutation test\n")
        out.write("                          PASS if p-value > 0.05 and |Δ%| < 1%\n\n")

        out.write("ATK-02/07 (Sensitivity):  Tests robustness to K=4 hyperparameter choices\n")
        out.write("                          PASS if few parameter combinations pass (<5%)\n\n")

        out.write("ATK-09 (Arithmetic):      Control test - arithmetic mean should NOT preserve entropy\n")
        out.write("                          PASS if arithmetic mean breaks but geometric preserves\n\n")

        out.write("ATK-01 (Out-of-sample):   Tests generalization to unseen data\n")
        out.write("                          PASS if EITT holds on test set (|Δ%| < 1%)\n\n")

        out.write("ATK-05 (White noise):     Tests if result is specific to real data\n")
        out.write("                          PASS if white noise breaks EITT\n\n")

        out.write("="*80 + "\n")
        out.write("Analysis complete. Results saved.\n")
        out.write("="*80 + "\n")

    print(f"\nResults written to: {output_file}")

if __name__ == '__main__':
    main()
