#!/usr/bin/env python3
"""
HUF Backblaze — Full CoDa + EITT + d(CoDa)/dt Analysis
========================================================
Reads pre-parsed monthly HDI snapshots and computes:
  1. Aitchison distance (year-over-year and consecutive)
  2. CLR transform time series
  3. ILR balances with proper √(rs/(r+s)) scaling
  4. Shannon entropy + K_eff per month
  5. EITT test: geometric-mean decimation ladder
  6. d(CoDa)/dt chain: perturbation velocity, dB/dt, d²B/dt²
  7. TV distance for dual-metric comparison
  8. Relay chain analysis (zero-sum constraint)

Data: 24 monthly snapshots (Jan 2024 – Dec 2025), K=4 carriers
  Mechanical (SMART 5), Electronic (SMART 187),
  Media (SMART 197), Offline (SMART 198)

Peter Higgins · HUF Collective · April 2026
"""

import json
import math
import os
import sys

# ─── Load Data ───────────────────────────────────────────────────────────

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..',
    'data', 'backblaze', '2026march8', 'backblaze_full_monthly.hdi.json')

with open(DATA_PATH) as f:
    hdi = json.load(f)

snapshots = hdi['snapshots']
dates = sorted(snapshots.keys())
labels = ['Mechanical', 'Electronic', 'Media', 'Offline']
K = 4

# Build composition array
compositions = []
for d in dates:
    rho = snapshots[d]['rho']
    compositions.append([rho[l] for l in labels])

EPSILON = 1e-10  # zero guard

# ─── Helper Functions ────────────────────────────────────────────────────

def shannon_entropy(x):
    """H(x) = -Σ x_i ln(x_i)"""
    return -sum(xi * math.log(max(xi, EPSILON)) for xi in x)

def k_eff(x):
    """K_eff = exp(H(x))"""
    return math.exp(shannon_entropy(x))

def geometric_mean(x):
    """g(x) = (∏ x_i)^(1/D)"""
    product = 1.0
    for xi in x:
        product *= max(xi, EPSILON)
    return product ** (1.0 / len(x))

def clr_transform(x):
    """CLR(x)_i = ln(x_i / g(x))"""
    g = geometric_mean(x)
    return [math.log(max(xi, EPSILON) / g) for xi in x]

def aitchison_distance(x, y):
    """d_A(x,y) = ||CLR(x) - CLR(y)||_2"""
    cx = clr_transform(x)
    cy = clr_transform(y)
    return math.sqrt(sum((a - b)**2 for a, b in zip(cx, cy)))

def tv_distance(x, y):
    """d_TV(x,y) = 0.5 * Σ|x_i - y_i|"""
    return 0.5 * sum(abs(a - b) for a, b in zip(x, y))

def ilr_balances(x):
    """
    ILR balances for K=4 with SBP:
      B1: Mechanical vs (Electronic + Media + Offline)  [1 vs 3]
      B2: Electronic vs (Media + Offline)               [1 vs 2]
      B3: Media vs Offline                              [1 vs 1]

    b_k = √(r*s/(r+s)) * ln(g(x+) / g(x-))
    """
    m, e, med, o = [max(xi, EPSILON) for xi in x]

    # B1: Mechanical(1) vs Electronic+Media+Offline(3)
    g_plus = m  # geometric mean of 1 element = itself
    g_minus = (e * med * o) ** (1.0/3.0)
    B1 = math.sqrt(1*3/(1+3)) * math.log(g_plus / g_minus)

    # B2: Electronic(1) vs Media+Offline(2)
    g_plus2 = e
    g_minus2 = (med * o) ** (1.0/2.0)
    B2 = math.sqrt(1*2/(1+2)) * math.log(g_plus2 / g_minus2)

    # B3: Media(1) vs Offline(1)
    B3 = math.sqrt(1*1/(1+1)) * math.log(med / o)

    return [B1, B2, B3]

def geom_mean_composition(comp_list):
    """Geometric mean of a list of compositions (element-wise, then close)."""
    K = len(comp_list[0])
    products = [1.0] * K
    n = len(comp_list)
    for c in comp_list:
        for i in range(K):
            products[i] *= max(c[i], EPSILON)
    raw = [p ** (1.0/n) for p in products]
    total = sum(raw)
    return [r / total for r in raw]

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: BASIC CoDa METRICS PER MONTH
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("  HUF BACKBLAZE — FULL CoDa + EITT + d(CoDa)/dt ANALYSIS")
print("  24 Monthly Snapshots · Jan 2024 – Dec 2025 · K=4 Carriers")
print("=" * 80)

print("\n─── SECTION 1: Monthly CoDa Metrics ───────────────────────────────\n")
print(f"{'Date':<12} {'H(x)':<8} {'K_eff':<7} {'‖x‖_A':<8} {'CLR[Mech]':<10} {'CLR[Elec]':<10} {'CLR[Med]':<10} {'CLR[Off]':<10}")
print("─" * 80)

entropies = []
k_effs = []
clr_series = []
balance_series = []

for i, d in enumerate(dates):
    x = compositions[i]
    H = shannon_entropy(x)
    Ke = k_eff(x)
    clr = clr_transform(x)
    bal = ilr_balances(x)

    # Aitchison norm (distance from uniform)
    uniform = [0.25] * K
    a_norm = aitchison_distance(x, uniform)

    entropies.append(H)
    k_effs.append(Ke)
    clr_series.append(clr)
    balance_series.append(bal)

    print(f"{d:<12} {H:<8.4f} {Ke:<7.3f} {a_norm:<8.4f} {clr[0]:<10.4f} {clr[1]:<10.4f} {clr[2]:<10.4f} {clr[3]:<10.4f}")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: PERTURBATION VELOCITY (d(CoDa)/dt — Layer 1)
# ═══════════════════════════════════════════════════════════════════════════

print("\n─── SECTION 2: Perturbation Velocity (Scalar Speed) ────────────────\n")
print(f"{'Period':<25} {'d_A':<10} {'d_TV':<10} {'Agree?':<8} {'Diagnostic'}")
print("─" * 80)

velocities_a = []
velocities_tv = []

for i in range(1, len(dates)):
    x_prev = compositions[i-1]
    x_curr = compositions[i]
    da = aitchison_distance(x_curr, x_prev)
    dtv = tv_distance(x_curr, x_prev)
    velocities_a.append(da)
    velocities_tv.append(dtv)

    # Diagnostic: do they agree?
    mean_da = sum(velocities_a) / len(velocities_a) if velocities_a else da
    mean_tv = sum(velocities_tv) / len(velocities_tv) if velocities_tv else dtv

    da_high = da > 1.5 * mean_da if len(velocities_a) > 3 else False
    tv_high = dtv > 1.5 * mean_tv if len(velocities_tv) > 3 else False

    if da_high and tv_high:
        diag = "BOTH HIGH — robust event"
    elif da_high and not tv_high:
        diag = "Aitchison only — trace shift"
    elif tv_high and not da_high:
        diag = "TV only — dominant shift"
    else:
        diag = "normal"

    agree = "YES" if (da_high == tv_high) else "DIVERGE"

    print(f"{dates[i-1][:7]}→{dates[i][:7]:<14} {da:<10.6f} {dtv:<10.6f} {agree:<8} {diag}")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: ILR BALANCE TRAJECTORY + dB/dt + d²B/dt² (Layers 2–4)
# ═══════════════════════════════════════════════════════════════════════════

print("\n─── SECTION 3: ILR Balance Trajectory ─────────────────────────────\n")
print(f"{'Date':<12} {'B1(M/rest)':<12} {'B2(E/MO)':<12} {'B3(Med/Off)':<12}")
print("─" * 52)
for i, d in enumerate(dates):
    b = balance_series[i]
    print(f"{d:<12} {b[0]:<12.6f} {b[1]:<12.6f} {b[2]:<12.6f}")

print("\n─── SECTION 3b: Balance Derivatives dB/dt ─────────────────────────\n")
print(f"{'Period':<20} {'dB1/dt':<12} {'dB2/dt':<12} {'dB3/dt':<12} {'Relay signal'}")
print("─" * 72)

db_dt = []
for i in range(1, len(dates)):
    db = [balance_series[i][k] - balance_series[i-1][k] for k in range(3)]
    db_dt.append(db)

    # Relay detection: which partition is moving fastest?
    max_idx = max(range(3), key=lambda k: abs(db[k]))
    bal_labels = ['Mech↔rest', 'Elec↔Med+Off', 'Med↔Off']
    direction = "↑" if db[max_idx] > 0 else "↓"

    print(f"{dates[i-1][:7]}→{dates[i][:7]:<9} {db[0]:<12.6f} {db[1]:<12.6f} {db[2]:<12.6f} {bal_labels[max_idx]} {direction}")

print("\n─── SECTION 3c: Balance Acceleration d²B/dt² ──────────────────────\n")
print(f"{'Period':<20} {'d²B1/dt²':<12} {'d²B2/dt²':<12} {'d²B3/dt²':<12} {'Note'}")
print("─" * 72)

for i in range(1, len(db_dt)):
    d2b = [db_dt[i][k] - db_dt[i-1][k] for k in range(3)]

    # Check if any acceleration is changing sign (inflection)
    notes = []
    for k in range(3):
        if len(db_dt) > i and db_dt[i][k] * db_dt[i-1][k] < 0:
            notes.append(f"B{k+1} reversed")
    note = "; ".join(notes) if notes else ""

    print(f"{dates[i][:7]}→{dates[i+1][:7]:<9} {d2b[0]:<12.6f} {d2b[1]:<12.6f} {d2b[2]:<12.6f} {note}")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: RELAY CHAIN ANALYSIS (Zero-Sum in Raw Space)
# ═══════════════════════════════════════════════════════════════════════════

print("\n─── SECTION 4: Relay Chain (Σ dx_i/dt = 0 verification) ───────────\n")
print(f"{'Period':<20} {'dMech':<10} {'dElec':<10} {'dMed':<10} {'dOff':<10} {'Sum':<10} {'Relay'}")
print("─" * 80)

for i in range(1, len(dates)):
    dx = [compositions[i][k] - compositions[i-1][k] for k in range(K)]
    total = sum(dx)

    # Identify relay: who gained, who lost?
    gainers = [labels[k] for k in range(K) if dx[k] > 0.001]
    losers = [labels[k] for k in range(K) if dx[k] < -0.001]
    relay = f"{'+'.join(losers)}→{'+'.join(gainers)}" if gainers and losers else "stable"

    print(f"{dates[i-1][:7]}→{dates[i][:7]:<9} {dx[0]:<10.4f} {dx[1]:<10.4f} {dx[2]:<10.4f} {dx[3]:<10.4f} {total:<10.6f} {relay}")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: EITT TEST — Entropy Under Geometric-Mean Decimation
# ═══════════════════════════════════════════════════════════════════════════

print("\n─── SECTION 5: EITT — Entropy Invariance Under Decimation ─────────\n")

# Base: monthly entropy
H_monthly = [shannon_entropy(c) for c in compositions]
H_monthly_mean = sum(H_monthly) / len(H_monthly)

print(f"Monthly entropy: mean={H_monthly_mean:.6f}  min={min(H_monthly):.6f}  max={max(H_monthly):.6f}")
print(f"Monthly entropy range: {(max(H_monthly)-min(H_monthly))/H_monthly_mean*100:.4f}%\n")

# Decimation ladder: 1-month, 2-month, 3-month, 4-month, 6-month, 12-month
decimation_levels = [1, 2, 3, 4, 6, 12]

print(f"{'Window':<15} {'Ratio':<8} {'H(geom mean)':<14} {'Δ from monthly':<16} {'% change'}")
print("─" * 65)

for window in decimation_levels:
    # Create geometric-mean decimated compositions
    decimated = []
    for start in range(0, len(compositions) - window + 1, window):
        block = compositions[start:start+window]
        gm = geom_mean_composition(block)
        decimated.append(gm)

    if len(decimated) < 2:
        continue

    # Compute entropy of decimated compositions
    H_dec = [shannon_entropy(c) for c in decimated]
    H_dec_mean = sum(H_dec) / len(H_dec)
    delta = H_dec_mean - H_monthly_mean
    pct = delta / H_monthly_mean * 100

    print(f"{window}-month{'':<9} {window}:1{'':<5} {H_dec_mean:<14.6f} {delta:<+16.6f} {pct:<+.4f}%")

# Also compute Aitchison variance at each level for comparison
print(f"\n{'Window':<15} {'Aitchison var':<15} {'Δ from monthly':<16} {'% change'}")
print("─" * 55)

for window in decimation_levels:
    decimated = []
    for start in range(0, len(compositions) - window + 1, window):
        block = compositions[start:start+window]
        gm = geom_mean_composition(block)
        decimated.append(gm)

    if len(decimated) < 2:
        continue

    # Aitchison variance: mean of CLR squared values
    vars_a = []
    for c in decimated:
        clr_c = clr_transform(c)
        var_a = sum(v**2 for v in clr_c) / K
        vars_a.append(var_a)

    mean_var = sum(vars_a) / len(vars_a)

    if window == 1:
        base_var = mean_var
        print(f"{window}-month{'':<9} {mean_var:<15.6f} {'(reference)':<16} {'0.0000%'}")
    else:
        delta = mean_var - base_var
        pct = delta / base_var * 100
        print(f"{window}-month{'':<9} {mean_var:<15.6f} {delta:<+16.6f} {pct:<+.4f}%")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: DISTANCE MATRIX (Year-over-Year)
# ═══════════════════════════════════════════════════════════════════════════

print("\n─── SECTION 6: Aitchison Distance Matrix (selected pairs) ─────────\n")

# Show distance between Jan of each year and every subsequent month
jan24_idx = 0   # 2024-01-01
jan25_idx = 12  # 2025-01-01
dec25_idx = 23  # 2025-12-01

key_pairs = [
    (0, 6, "Jan→Jul 2024 (6 months)"),
    (0, 12, "Jan 2024→Jan 2025 (12 months)"),
    (0, 23, "Jan 2024→Dec 2025 (24 months)"),
    (12, 23, "Jan→Dec 2025 (12 months)"),
    (6, 18, "Jul 2024→Jul 2025 (12 months)"),
]

for i, j, desc in key_pairs:
    da = aitchison_distance(compositions[i], compositions[j])
    dtv = tv_distance(compositions[i], compositions[j])
    print(f"  {desc:<40} d_A={da:.6f}  d_TV={dtv:.6f}")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7: SUMMARY AND DISCOVERIES
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("  SUMMARY — KEY FINDINGS")
print("=" * 80)

# 1. EITT result
H_annual = []
for year_start in range(0, 24, 12):
    block = compositions[year_start:year_start+12]
    if len(block) == 12:
        gm = geom_mean_composition(block)
        H_annual.append(shannon_entropy(gm))

H_annual_mean = sum(H_annual) / len(H_annual) if H_annual else 0
eitt_pct = abs(H_annual_mean - H_monthly_mean) / H_monthly_mean * 100

print(f"\n  EITT (Backblaze hardware data):")
print(f"  Monthly entropy mean:  {H_monthly_mean:.6f}")
print(f"  Annual entropy mean:   {H_annual_mean:.6f}")
print(f"  EITT residual:         {eitt_pct:.4f}%")
print(f"  Compression ratio:     12:1 (monthly → annual)")
if eitt_pct < 2.0:
    print(f"  VERDICT:               EITT HOLDS on hardware degradation data")
else:
    print(f"  VERDICT:               EITT FAILS — {eitt_pct:.2f}% exceeds threshold")

# 2. Dominant relay
print(f"\n  RELAY CHAIN:")
total_dx = [0]*K
for i in range(1, len(dates)):
    for k in range(K):
        total_dx[k] += compositions[-1][k] - compositions[0][k]

for k in range(K):
    direction = "↑" if total_dx[k] > 0 else "↓"
    print(f"  {labels[k]:<15} net Δρ = {total_dx[k]:+.4f} {direction}")
print(f"  Σ Δρ = {sum(total_dx):.6f} (closure check)")

# 3. Balance trajectory summary
b_first = balance_series[0]
b_last = balance_series[-1]
print(f"\n  BALANCE TRAJECTORY (Jan 2024 → Dec 2025):")
bal_names = ['B1 Mech↔rest', 'B2 Elec↔Med+Off', 'B3 Med↔Off']
for k in range(3):
    delta = b_last[k] - b_first[k]
    direction = "→ Mech gaining" if k==0 and delta>0 else "→ Mech losing" if k==0 and delta<0 else ""
    if k==1: direction = "→ Elec gaining" if delta>0 else "→ Elec losing"
    if k==2: direction = "→ Media gaining" if delta>0 else "→ Offline gaining"
    print(f"  {bal_names[k]:<20} {b_first[k]:+.4f} → {b_last[k]:+.4f}  ΔB={delta:+.4f} {direction}")

# 4. Persistence check
print(f"\n  TEMPORAL PERSISTENCE (smoothness of balance trajectories):")
for k in range(3):
    vals = [balance_series[i][k] for i in range(len(dates))]
    diffs = [vals[i+1] - vals[i] for i in range(len(vals)-1)]
    sign_changes = sum(1 for i in range(len(diffs)-1) if diffs[i]*diffs[i+1] < 0)
    monotonic_pct = (1 - sign_changes / max(len(diffs)-1, 1)) * 100
    print(f"  {bal_names[k]:<20} sign changes in dB/dt: {sign_changes}/{len(diffs)-1}  monotonicity: {monotonic_pct:.0f}%")

# 5. Mean perturbation velocity
mean_va = sum(velocities_a) / len(velocities_a)
max_va = max(velocities_a)
max_va_idx = velocities_a.index(max_va)
print(f"\n  PERTURBATION VELOCITY:")
print(f"  Mean d_A (consecutive):  {mean_va:.6f}")
print(f"  Max d_A:                 {max_va:.6f} ({dates[max_va_idx][:7]}→{dates[max_va_idx+1][:7]})")
print(f"  Cumulative drift (24mo): {aitchison_distance(compositions[0], compositions[-1]):.6f}")

print(f"\n{'=' * 80}")
print(f"  Governance: CGS-2 (n=3), GDoF 264. No new constants.")
print(f"  Data: Backblaze Drive Stats, CC BY 4.0 equivalent")
print(f"  HUF:1.1.8 | OP_MIN=0.51 | TOOL_MAX=0.49")
print(f"{'=' * 80}")
