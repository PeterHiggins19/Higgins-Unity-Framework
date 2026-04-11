#!/usr/bin/env python3
"""
COMPREHENSIVE EITT RE-TEST — April 10, 2026
============================================
Post-ILR-fix, post-honesty-audit, all corrections applied.

Tests:
1. All existing domains: Gold/Silver K=2, Energy K=7, Financial K=9
2. Bootstrap CIs on all domains
3. Multi-ratio EITT (2:1, 3:1, 5:1, 10:1) — where arith vs geom should diverge
4. Proper ILR balance entropy (test EITT on ILR-transformed balances)
5. Aitchison distance under decimation (new: does distance to Fréchet mean shrink?)
6. Subcompositional coherence test (new: does EITT hold on subcompositions?)
7. Higher compression arithmetic-mean comparison (ATK-09 extension)
8. Pairwise log-ratio stability under decimation (Peter's "turns ratio" idea)

Date: 2026-04-10
"""
import csv, math, os, sys, random
from collections import defaultdict

EPSILON = 1e-12

# ══════════════════════════════════════════════════════════════
# CORE CoDa FUNCTIONS
# ══════════════════════════════════════════════════════════════

def shannon_entropy(p):
    return -sum(pi * math.log(pi) for pi in p if pi > EPSILON)

def geometric_mean(vals):
    if not vals or any(v <= 0 for v in vals):
        return EPSILON
    return math.exp(sum(math.log(v) for v in vals) / len(vals))

def arithmetic_mean(vals):
    return sum(vals) / len(vals) if vals else 0

def clr_transform(x):
    g = geometric_mean(x)
    return [math.log(xi / g) for xi in x]

def ilr_balance(x, group1_idx, group2_idx):
    """Proper ILR balance: sqrt(r*s/(r+s)) * ln(geomean(g1)/geomean(g2))"""
    r = len(group1_idx)
    s = len(group2_idx)
    g1 = geometric_mean([x[i] for i in group1_idx])
    g2 = geometric_mean([x[i] for i in group2_idx])
    return math.sqrt(r * s / (r + s)) * math.log(g1 / g2)

def geom_mean_compositions(comps):
    K = len(comps[0])
    gm = [geometric_mean([c[j] for c in comps]) for j in range(K)]
    total = sum(gm)
    return [g / total for g in gm] if total > 0 else [1/K]*K

def arith_mean_compositions(comps):
    K = len(comps[0])
    am = [arithmetic_mean([c[j] for c in comps]) for j in range(K)]
    total = sum(am)
    return [a / total for a in am] if total > 0 else [1/K]*K

def aitchison_distance(x, y):
    clr_x = clr_transform(x)
    clr_y = clr_transform(y)
    return math.sqrt(sum((a - b)**2 for a, b in zip(clr_x, clr_y)))

def pairwise_log_ratio(x, i, j):
    """Log-ratio between parts i and j: ln(x_i / x_j) — Peter's 'turns ratio'"""
    return math.log(max(x[i], EPSILON) / max(x[j], EPSILON))

# ══════════════════════════════════════════════════════════════
# EITT AT MULTIPLE COMPRESSION RATIOS
# ══════════════════════════════════════════════════════════════

def run_eitt_multi_ratio(compositions, ratios=[2, 3, 5, 10], use_arithmetic=False):
    """Run EITT at multiple decimation ratios"""
    n = len(compositions)
    base_entropies = [shannon_entropy(c) for c in compositions]
    base_H = arithmetic_mean(base_entropies)

    results = {}
    for w in ratios:
        if n < w * 2:
            continue
        agg_comps = []
        for i in range(0, n - w + 1, w):
            chunk = compositions[i:i+w]
            if len(chunk) == w:
                if use_arithmetic:
                    agg_comps.append(arith_mean_compositions(chunk))
                else:
                    agg_comps.append(geom_mean_compositions(chunk))

        if agg_comps:
            agg_H = arithmetic_mean([shannon_entropy(c) for c in agg_comps])
            delta = agg_H - base_H
            pct = delta / base_H * 100 if base_H > 0 else 0
            results[w] = {'agg_H': agg_H, 'delta': delta, 'pct': pct, 'n_blocks': len(agg_comps)}

    results['base_H'] = base_H
    return results

# ══════════════════════════════════════════════════════════════
# NEW TEST: SUBCOMPOSITIONAL COHERENCE
# ══════════════════════════════════════════════════════════════

def test_subcompositional_eitt(compositions, sub_indices, label=""):
    """
    Test EITT on a subcomposition (subset of parts, re-normalised).
    If EITT holds on full comp, does it hold on subcomp?
    This tests CoDa's subcompositional coherence principle.
    """
    sub_comps = []
    for c in compositions:
        sub = [max(c[i], EPSILON) for i in sub_indices]
        total = sum(sub)
        sub_comps.append([s / total for s in sub])

    return run_eitt_multi_ratio(sub_comps, ratios=[2, 3, 5])

# ══════════════════════════════════════════════════════════════
# NEW TEST: PAIRWISE LOG-RATIO STABILITY ("TURNS RATIOS")
# ══════════════════════════════════════════════════════════════

def test_pairwise_logratio_stability(compositions, ratios=[2, 3, 5]):
    """
    Peter's idea: do pairwise log-ratios (turns ratios) remain stable
    under geometric-mean decimation?

    For each pair (i,j), compute ln(x_i/x_j) at original resolution,
    then after decimation. Compare variance of the log-ratio series.
    """
    K = len(compositions[0])
    n = len(compositions)
    results = {}

    for w in ratios:
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

        # For each pair, compute mean log-ratio before and after
        pair_results = []
        for i in range(K):
            for j in range(i + 1, K):
                orig_lrs = [pairwise_log_ratio(c, i, j) for c in compositions]
                agg_lrs = [pairwise_log_ratio(c, i, j) for c in agg_comps]

                orig_mean = arithmetic_mean(orig_lrs)
                agg_mean = arithmetic_mean(agg_lrs)

                orig_var = arithmetic_mean([(lr - orig_mean)**2 for lr in orig_lrs])
                agg_var = arithmetic_mean([(lr - agg_mean)**2 for lr in agg_lrs])

                # Mean shift and variance ratio
                mean_shift = agg_mean - orig_mean
                var_ratio = agg_var / orig_var if orig_var > 0 else float('inf')

                pair_results.append({
                    'pair': (i, j),
                    'orig_mean': orig_mean,
                    'agg_mean': agg_mean,
                    'mean_shift': mean_shift,
                    'orig_var': orig_var,
                    'agg_var': agg_var,
                    'var_ratio': var_ratio
                })

        results[w] = pair_results

    return results

# ══════════════════════════════════════════════════════════════
# NEW TEST: AITCHISON DISTANCE CONTRACTION
# ══════════════════════════════════════════════════════════════

def test_aitchison_contraction(compositions, ratios=[2, 3, 5]):
    """
    Under geometric-mean decimation, does the Aitchison distance
    between consecutive compositions shrink? This tests whether
    decimation acts as a contraction mapping on the simplex.
    """
    results = {}

    # Original consecutive distances
    orig_dists = []
    for i in range(len(compositions) - 1):
        orig_dists.append(aitchison_distance(compositions[i], compositions[i+1]))

    orig_mean_dist = arithmetic_mean(orig_dists)
    orig_max_dist = max(orig_dists)

    for w in ratios:
        n = len(compositions)
        if n < w * 2:
            continue

        agg_comps = []
        for i in range(0, n - w + 1, w):
            chunk = compositions[i:i+w]
            if len(chunk) == w:
                agg_comps.append(geom_mean_compositions(chunk))

        if len(agg_comps) < 2:
            continue

        agg_dists = []
        for i in range(len(agg_comps) - 1):
            agg_dists.append(aitchison_distance(agg_comps[i], agg_comps[i+1]))

        agg_mean_dist = arithmetic_mean(agg_dists)
        agg_max_dist = max(agg_dists)

        results[w] = {
            'orig_mean_dist': orig_mean_dist,
            'agg_mean_dist': agg_mean_dist,
            'contraction': agg_mean_dist / orig_mean_dist if orig_mean_dist > 0 else float('inf'),
            'orig_max': orig_max_dist,
            'agg_max': agg_max_dist
        }

    return results

# ══════════════════════════════════════════════════════════════
# BOOTSTRAP CI (from honesty_tests.py)
# ══════════════════════════════════════════════════════════════

def block_bootstrap_eitt(compositions, n_bootstrap=1000):
    n = len(compositions)
    block_size = max(2, int(math.sqrt(n)))

    base_entropies = [shannon_entropy(c) for c in compositions]
    base_H = arithmetic_mean(base_entropies)

    # 2:1 decimation
    agg_comps = []
    for i in range(0, n - 1, 2):
        agg_comps.append(geom_mean_compositions(compositions[i:i+2]))
    agg_H = arithmetic_mean([shannon_entropy(c) for c in agg_comps])
    base_pct = (agg_H - base_H) / base_H * 100 if base_H > 0 else 0

    bootstrap_pcts = []
    for _ in range(n_bootstrap):
        indices = []
        while len(indices) < n:
            start = random.randint(0, n - block_size)
            indices.extend(range(start, min(start + block_size, n)))
        indices = indices[:n]
        boot_comps = [compositions[i] for i in indices]

        boot_ents = [shannon_entropy(c) for c in boot_comps]
        boot_base = arithmetic_mean(boot_ents)
        boot_agg = []
        for i in range(0, n - 1, 2):
            boot_agg.append(geom_mean_compositions([boot_comps[i], boot_comps[min(i+1, n-1)]]))
        boot_agg_H = arithmetic_mean([shannon_entropy(c) for c in boot_agg])
        boot_pct = (boot_agg_H - boot_base) / boot_base * 100 if boot_base > 0 else 0
        bootstrap_pcts.append(boot_pct)

    bootstrap_pcts.sort()
    nb = len(bootstrap_pcts)
    ci_lo = bootstrap_pcts[int(0.025 * nb)]
    ci_hi = bootstrap_pcts[int(0.975 * nb)]

    return base_pct, ci_lo, ci_hi

# ══════════════════════════════════════════════════════════════
# DATA LOADERS
# ══════════════════════════════════════════════════════════════

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

def load_energy():
    fp = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Energy/yearly_full_release_long_format.csv'
    if not os.path.exists(fp):
        return None, None
    subcats = defaultdict(lambda: defaultdict(float))
    with open(fp) as f:
        for row in csv.DictReader(f):
            if (row.get('Area') == 'World' and
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

def load_europe_energy():
    """Load European country-level energy data for additional testing"""
    fp = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Energy/europe_yearly_full_release_long_format.csv'
    if not os.path.exists(fp):
        return None, None

    # Get Germany as a specific country test
    subcats = defaultdict(lambda: defaultdict(float))
    with open(fp) as f:
        for row in csv.DictReader(f):
            if (row.get('Area') == 'Germany' and
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

# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    random.seed(42)

    out_path = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Githubrepo/HUF/code/analysis/comprehensive_retest_2026april10.txt'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, 'w') as out:
        out.write("=" * 80 + "\n")
        out.write("COMPREHENSIVE EITT RE-TEST — 2026-04-10\n")
        out.write("Post-ILR-fix, post-honesty-audit, all corrections applied\n")
        out.write("=" * 80 + "\n\n")

        # ── Load all datasets ──
        print("Loading gold/silver...", file=sys.stderr)
        gs_comps, gs_years = load_gold_silver()

        print("Loading energy (world)...", file=sys.stderr)
        en_comps, en_years = load_energy()

        print("Loading financial...", file=sys.stderr)
        fi_comps, fi_months, fi_sectors = load_financial()

        print("Loading energy (Germany)...", file=sys.stderr)
        de_comps, de_years = load_europe_energy()

        datasets = []
        if gs_comps:
            datasets.append(('Gold/Silver K=2', gs_comps, gs_years, 2))
        if en_comps:
            datasets.append(('Energy World K=7', en_comps, en_years, 7))
        if fi_comps:
            datasets.append(('Financial K=%d (price-level, NOT market-cap)' % len(fi_comps[0]), fi_comps, fi_months, len(fi_comps[0])))
        if de_comps:
            datasets.append(('Energy Germany K=7', de_comps, de_years, 7))

        # ══════════════════════════════════════════════════════════
        # TEST 1: MULTI-RATIO EITT (Geometric Mean)
        # ══════════════════════════════════════════════════════════
        out.write("\n" + "=" * 80 + "\n")
        out.write("TEST 1: MULTI-RATIO EITT (Geometric Mean Decimation)\n")
        out.write("Testing at 2:1, 3:1, 5:1, 10:1 compression\n")
        out.write("=" * 80 + "\n\n")

        for name, comps, labels, K in datasets:
            out.write(f"\n{name}: N={len(comps)}, Period: {labels[0]}→{labels[-1]}\n")
            results = run_eitt_multi_ratio(comps, ratios=[2, 3, 5, 10])
            out.write(f"  Base H = {results['base_H']:.6f}\n")
            for w in [2, 3, 5, 10]:
                if w in results:
                    r = results[w]
                    status = "PASS" if abs(r['pct']) < 2.0 else "FAIL"
                    out.write(f"  {w}:1  →  H={r['agg_H']:.6f}  Δ={r['pct']:+.4f}%  (n={r['n_blocks']})  [{status}]\n")

        # ══════════════════════════════════════════════════════════
        # TEST 2: ARITHMETIC vs GEOMETRIC AT HIGHER RATIOS
        # ══════════════════════════════════════════════════════════
        out.write("\n\n" + "=" * 80 + "\n")
        out.write("TEST 2: ARITHMETIC vs GEOMETRIC MEAN — HIGHER COMPRESSION RATIOS\n")
        out.write("ATK-09 extension: at 2:1 both pass; do they diverge at 5:1, 10:1?\n")
        out.write("=" * 80 + "\n\n")

        for name, comps, labels, K in datasets:
            out.write(f"\n{name}:\n")
            geom_r = run_eitt_multi_ratio(comps, ratios=[2, 3, 5, 10], use_arithmetic=False)
            arith_r = run_eitt_multi_ratio(comps, ratios=[2, 3, 5, 10], use_arithmetic=True)

            out.write(f"  {'Ratio':<8} {'Geom Δ%':>10} {'Arith Δ%':>10} {'Gap':>10} {'Diverges?':>10}\n")
            out.write(f"  {'─'*48}\n")
            for w in [2, 3, 5, 10]:
                if w in geom_r and w in arith_r:
                    gp = geom_r[w]['pct']
                    ap = arith_r[w]['pct']
                    gap = abs(ap) - abs(gp)
                    diverges = "YES" if gap > 0.5 else "no"
                    out.write(f"  {w}:1{'':<5} {gp:+10.4f} {ap:+10.4f} {gap:+10.4f} {diverges:>10}\n")

        # ══════════════════════════════════════════════════════════
        # TEST 3: BOOTSTRAP CIs ON ALL DOMAINS
        # ══════════════════════════════════════════════════════════
        out.write("\n\n" + "=" * 80 + "\n")
        out.write("TEST 3: BOOTSTRAP CONFIDENCE INTERVALS (1000 replicates)\n")
        out.write("=" * 80 + "\n\n")

        for name, comps, labels, K in datasets:
            print(f"  Bootstrap CI: {name}...", file=sys.stderr)
            base_pct, ci_lo, ci_hi = block_bootstrap_eitt(comps)
            out.write(f"{name}:\n")
            out.write(f"  Point estimate: {base_pct:+.6f}%\n")
            out.write(f"  95% CI: [{ci_lo:.6f}%, {ci_hi:.6f}%]\n")
            out.write(f"  CI width: {ci_hi - ci_lo:.6f}%\n")
            ci_excludes_zero = (ci_lo > 0 or ci_hi < 0)
            out.write(f"  CI excludes zero: {'YES — systematic bias' if ci_excludes_zero else 'NO — consistent with invariance'}\n\n")

        # ══════════════════════════════════════════════════════════
        # TEST 4: SUBCOMPOSITIONAL COHERENCE
        # ══════════════════════════════════════════════════════════
        out.write("\n" + "=" * 80 + "\n")
        out.write("TEST 4: SUBCOMPOSITIONAL COHERENCE (CoDa principle)\n")
        out.write("Does EITT hold on subcompositions? If yes, confirms CoDa compatibility.\n")
        out.write("=" * 80 + "\n\n")

        if en_comps:
            # Energy K=7: indices 0=Coal 1=Gas 2=Nuclear 3=Hydro 4=Wind 5=Solar 6=Other_renew
            subcases = [
                ("Fossil only (Coal/Gas)", [0, 1]),
                ("Fossil+Nuclear (Coal/Gas/Nuc)", [0, 1, 2]),
                ("Renewables only (Hydro/Wind/Solar/Other)", [3, 4, 5, 6]),
                ("Coal/Gas/Wind/Solar (transition mix)", [0, 1, 4, 5]),
            ]

            for sub_name, indices in subcases:
                out.write(f"  Energy {sub_name}:\n")
                sub_r = test_subcompositional_eitt(en_comps, indices)
                for w in [2, 3, 5]:
                    if w in sub_r:
                        r = sub_r[w]
                        status = "PASS" if abs(r['pct']) < 2.0 else "FAIL"
                        out.write(f"    {w}:1  Δ={r['pct']:+.4f}%  [{status}]\n")
                out.write("\n")

        if fi_comps and len(fi_comps[0]) >= 6:
            # Financial: take first 3 and last 3 sectors as subcompositions
            K_fi = len(fi_comps[0])
            subcases_fi = [
                ("First 3 sectors", list(range(3))),
                ("Last 3 sectors", list(range(K_fi-3, K_fi))),
                ("Sectors 0,2,4,6", [i for i in [0,2,4,6] if i < K_fi]),
            ]
            for sub_name, indices in subcases_fi:
                out.write(f"  Financial {sub_name}:\n")
                sub_r = test_subcompositional_eitt(fi_comps, indices)
                for w in [2, 3, 5]:
                    if w in sub_r:
                        r = sub_r[w]
                        status = "PASS" if abs(r['pct']) < 2.0 else "FAIL"
                        out.write(f"    {w}:1  Δ={r['pct']:+.4f}%  [{status}]\n")
                out.write("\n")

        # ══════════════════════════════════════════════════════════
        # TEST 5: AITCHISON DISTANCE CONTRACTION
        # ══════════════════════════════════════════════════════════
        out.write("\n" + "=" * 80 + "\n")
        out.write("TEST 5: AITCHISON DISTANCE CONTRACTION UNDER DECIMATION\n")
        out.write("Does geometric-mean decimation contract distances on the simplex?\n")
        out.write("=" * 80 + "\n\n")

        for name, comps, labels, K in datasets:
            if K < 2:
                continue
            out.write(f"{name}:\n")
            ait_r = test_aitchison_contraction(comps, ratios=[2, 3, 5])
            for w in [2, 3, 5]:
                if w in ait_r:
                    r = ait_r[w]
                    out.write(f"  {w}:1  Mean dist: {r['orig_mean_dist']:.4f} → {r['agg_mean_dist']:.4f}  ")
                    out.write(f"(ratio={r['contraction']:.4f}, max: {r['orig_max']:.4f} → {r['agg_max']:.4f})\n")
            contracts = all(ait_r[w]['contraction'] < 1.0 for w in ait_r if isinstance(w, int))
            out.write(f"  Contraction mapping: {'YES — distances shrink' if contracts else 'NO'}\n\n")

        # ══════════════════════════════════════════════════════════
        # TEST 6: PAIRWISE LOG-RATIO STABILITY ("TURNS RATIOS")
        # ══════════════════════════════════════════════════════════
        out.write("\n" + "=" * 80 + "\n")
        out.write("TEST 6: PAIRWISE LOG-RATIO STABILITY ('TURNS RATIOS')\n")
        out.write("Peter's idea: do pairwise log-ratios (exchange rates between parts)\n")
        out.write("preserve their mean under geometric-mean decimation?\n")
        out.write("=" * 80 + "\n\n")

        for name, comps, labels, K in datasets:
            if K > 9:
                out.write(f"{name}: Skipped (K={K} too large, {K*(K-1)//2} pairs)\n\n")
                continue

            out.write(f"{name} (K={K}, {K*(K-1)//2} pairs):\n")
            plr_r = test_pairwise_logratio_stability(comps, ratios=[2, 5])

            for w in [2, 5]:
                if w not in plr_r:
                    continue
                pairs = plr_r[w]
                mean_shifts = [abs(p['mean_shift']) for p in pairs]
                var_ratios = [p['var_ratio'] for p in pairs]

                out.write(f"\n  {w}:1 decimation:\n")
                out.write(f"    Mean |shift| across all pairs: {arithmetic_mean(mean_shifts):.6f}\n")
                out.write(f"    Max |shift|: {max(mean_shifts):.6f}\n")
                out.write(f"    Mean variance ratio (agg/orig): {arithmetic_mean(var_ratios):.4f}\n")
                out.write(f"    All means preserved (<0.1): {'YES' if max(mean_shifts) < 0.1 else 'NO'}\n")

                # Show top 3 most-shifted pairs
                pairs_sorted = sorted(pairs, key=lambda p: abs(p['mean_shift']), reverse=True)
                out.write(f"    Most shifted pairs:\n")
                for p in pairs_sorted[:3]:
                    i, j = p['pair']
                    out.write(f"      ({i},{j}): mean {p['orig_mean']:.4f} → {p['agg_mean']:.4f}  (shift={p['mean_shift']:+.4f}, var ratio={p['var_ratio']:.4f})\n")
            out.write("\n")

        # ══════════════════════════════════════════════════════════
        # TEST 7: ILR BALANCE ENTROPY (NEW)
        # ══════════════════════════════════════════════════════════
        out.write("\n" + "=" * 80 + "\n")
        out.write("TEST 7: ILR BALANCE BEHAVIOUR UNDER DECIMATION\n")
        out.write("Do ILR balances (proper normalisation) show any structure change?\n")
        out.write("=" * 80 + "\n\n")

        if en_comps:
            # Energy SBP: B1 = Fossil(0,1) vs Renew(3,4,5,6), then B2 = Coal(0) vs Gas(1), B3 = Wind(4) vs Solar(5)
            out.write("Energy World — ILR Balances (corrected normalisation):\n")
            out.write("  SBP: B1=Fossil|Renew, B2=Coal|Gas, B3=Wind|Solar\n\n")

            # Compute ILR balances for each year
            balances_orig = []
            for c in en_comps:
                b1 = ilr_balance(c, [0, 1], [3, 4, 5, 6])  # Fossil vs Renew (excl nuclear)
                b2 = ilr_balance(c, [0], [1])  # Coal vs Gas
                b3 = ilr_balance(c, [4], [5])  # Wind vs Solar
                balances_orig.append([b1, b2, b3])

            # Decimate the raw compositions, THEN compute ILR
            for w in [2, 3, 5]:
                n = len(en_comps)
                agg_comps = []
                for i in range(0, n - w + 1, w):
                    chunk = en_comps[i:i+w]
                    if len(chunk) == w:
                        agg_comps.append(geom_mean_compositions(chunk))

                balances_agg = []
                for c in agg_comps:
                    b1 = ilr_balance(c, [0, 1], [3, 4, 5, 6])
                    b2 = ilr_balance(c, [0], [1])
                    b3 = ilr_balance(c, [4], [5])
                    balances_agg.append([b1, b2, b3])

                # Compare means and variances
                for bi, bname in enumerate(['B1 Fossil|Renew', 'B2 Coal|Gas', 'B3 Wind|Solar']):
                    orig_vals = [b[bi] for b in balances_orig]
                    agg_vals = [b[bi] for b in balances_agg]

                    orig_m = arithmetic_mean(orig_vals)
                    agg_m = arithmetic_mean(agg_vals)
                    orig_v = arithmetic_mean([(v - orig_m)**2 for v in orig_vals])
                    agg_v = arithmetic_mean([(v - agg_m)**2 for v in agg_vals])

                    out.write(f"  {w}:1  {bname}: mean {orig_m:.4f}→{agg_m:.4f} (Δ={agg_m-orig_m:+.4f}), var {orig_v:.4f}→{agg_v:.4f} (ratio={agg_v/orig_v:.4f})\n")
                out.write("\n")

        # ══════════════════════════════════════════════════════════
        # SUMMARY
        # ══════════════════════════════════════════════════════════
        out.write("\n" + "=" * 80 + "\n")
        out.write("SUMMARY — COMPREHENSIVE RE-TEST\n")
        out.write("=" * 80 + "\n\n")

        out.write("Test 1 (Multi-ratio EITT):      Geometric-mean decimation residuals at multiple ratios\n")
        out.write("Test 2 (Arith vs Geom):          Higher compression ratios to separate the two means\n")
        out.write("Test 3 (Bootstrap CIs):           Statistical confidence on all domains\n")
        out.write("Test 4 (Subcomp coherence):       EITT on subsets of parts — CoDa compatibility\n")
        out.write("Test 5 (Aitchison contraction):   Does decimation shrink simplex distances?\n")
        out.write("Test 6 (Turns ratios):            Pairwise log-ratio stability under decimation\n")
        out.write("Test 7 (ILR balance behaviour):   Corrected ILR balances under decimation\n")
        out.write("\nAll tests run with corrected ILR normalisation (sqrt(r*s/(r+s)) coefficients)\n")
        out.write("All labels honest: financial = price-level portfolio, not market-cap\n")
        out.write("Date: 2026-04-10\n")

    print(f"\nResults written to: {out_path}", file=sys.stderr)
    return out_path

if __name__ == '__main__':
    main()
