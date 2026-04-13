#!/usr/bin/env python3
"""
CoDaWork 2026 — Compositional monitoring of energy-mix drift on the simplex
Higgins P.

Exact protocol matching the accepted abstract:
  1. Extract 9-carrier compositions from EMBER yearly data
  2. Perturbation between consecutive years (compositional ratio)
  3. Aitchison distance for drift magnitude
  4. Effective diversity / concentration measure
  
Data: EMBER CC BY 4.0, Germany / Japan / United Kingdom, 2000–2025
Carriers: Coal, Gas, Nuclear, Hydro, Solar, Wind, Bioenergy, Other Fossil, Other Renewables
"""

import csv, json, math, sys
import numpy as np
from collections import defaultdict

# ── Configuration ──────────────────────────────────────────────────
DATA_PATH = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Energy/yearly_full_release_long_format.csv"
COUNTRIES = ["Germany", "Japan", "United Kingdom"]
CARRIERS = ["Coal", "Gas", "Nuclear", "Hydro", "Solar", "Wind", "Bioenergy", "Other Fossil", "Other Renewables"]
D = len(CARRIERS)  # 9 parts → 8-simplex
YEAR_RANGE = range(2000, 2026)
ZERO_REPLACEMENT = 1e-6  # Multiplicative replacement for essential/rounded zeros

OUT_PATH = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Energy/codawork2026_results.json"

# ── 1. Data Extraction ─────────────────────────────────────────────
def load_ember_compositions():
    """Extract 9-carrier compositions (TWh) per country-year."""
    raw = defaultdict(lambda: defaultdict(dict))  # raw[country][year][carrier]
    
    with open(DATA_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            area = row['Area']
            if area not in COUNTRIES:
                continue
            try:
                year = int(row['Year'])
            except ValueError:
                continue
            if year not in YEAR_RANGE:
                continue
            if (row['Category'] == 'Electricity generation' and 
                row['Subcategory'] == 'Fuel' and 
                row['Unit'] == 'TWh' and
                row['Variable'] in CARRIERS):
                try:
                    val = float(row['Value'])
                except (ValueError, TypeError):
                    val = 0.0
                raw[area][year][row['Variable']] = val
    
    # Build composition arrays
    compositions = {}  # compositions[country] = {year: np.array}
    for country in COUNTRIES:
        compositions[country] = {}
        for year in YEAR_RANGE:
            vals = np.array([raw[country][year].get(c, 0.0) for c in CARRIERS])
            # Handle zeros: multiplicative replacement
            total = vals.sum()
            if total <= 0:
                continue
            # Close to proportions
            props = vals / total
            # Multiplicative zero replacement (preserving ratios of non-zero parts)
            n_zeros = np.sum(props <= 0)
            if n_zeros > 0:
                delta = ZERO_REPLACEMENT
                props_replaced = props.copy()
                for i in range(D):
                    if props_replaced[i] <= 0:
                        props_replaced[i] = delta
                # Re-close: non-zero parts share the displaced mass
                non_zero_mask = props > 0
                displaced = n_zeros * delta
                factor = (1.0 - displaced) / props[non_zero_mask].sum()
                props_replaced[non_zero_mask] = props[non_zero_mask] * factor
                props = props_replaced
            
            compositions[country][year] = props
    
    return compositions

# ── 2. CoDa Operations ─────────────────────────────────────────────
def closure(x):
    """Close a vector to the simplex."""
    return x / x.sum()

def perturbation(x, y):
    """Perturbation x ⊕ y (element-wise product, then close)."""
    return closure(x * y)

def perturbation_difference(x, y):
    """Compute y ⊖ x = y ⊕ x^(-1) — the compositional change from x to y."""
    # y ⊖ x = C(y₁/x₁, y₂/x₂, ..., yD/xD)
    ratio = y / x
    return closure(ratio)

def clr(x):
    """Centred log-ratio transform."""
    log_x = np.log(x)
    return log_x - log_x.mean()

def aitchison_distance(x, y):
    """Aitchison distance d_A(x, y) = ||clr(x) - clr(y)||."""
    diff = clr(x) - clr(y)
    return np.sqrt(np.dot(diff, diff))

def aitchison_norm(x):
    """Aitchison norm ||x||_A = ||clr(x)||."""
    c = clr(x)
    return np.sqrt(np.dot(c, c))

# ── 3. Concentration & Effective Diversity ─────────────────────────
def shannon_entropy(x):
    """Shannon entropy H(x) = -Σ xᵢ ln(xᵢ)."""
    return -np.sum(x * np.log(x))

def effective_number(x):
    """Effective number of carriers N_eff = exp(H(x))."""
    return np.exp(shannon_entropy(x))

def simpson_concentration(x):
    """Simpson concentration C = Σ xᵢ²."""
    return np.sum(x**2)

def max_entropy(D):
    """Maximum entropy for D parts = ln(D)."""
    return np.log(D)

# ── 4. Full Protocol ───────────────────────────────────────────────
def run_monitoring_protocol(compositions, country):
    """Run the complete monitoring protocol for one country."""
    years = sorted(compositions[country].keys())
    
    results = {
        "country": country,
        "carriers": CARRIERS,
        "D": D,
        "years": years,
        "compositions": {},
        "perturbation_series": [],
        "aitchison_distances": [],
        "cumulative_distances": [],
        "effective_diversity": [],
        "simpson_concentration": [],
        "aitchison_norms": [],
        "shannon_entropy": [],
        "drift_flags": [],
    }
    
    # Store compositions
    for y in years:
        comp = compositions[country][y]
        results["compositions"][y] = {c: round(float(comp[i]), 8) for i, c in enumerate(CARRIERS)}
    
    # Compute metrics for each year
    cumulative_d = 0.0
    barycenter = np.ones(D) / D  # isotropic reference
    
    for i, y in enumerate(years):
        comp = compositions[country][y]
        
        # Effective diversity
        H = shannon_entropy(comp)
        N_eff = effective_number(comp)
        C_simp = simpson_concentration(comp)
        a_norm = aitchison_norm(comp)
        
        results["effective_diversity"].append({"year": y, "N_eff": round(float(N_eff), 4)})
        results["simpson_concentration"].append({"year": y, "C": round(float(C_simp), 6)})
        results["aitchison_norms"].append({"year": y, "norm": round(float(a_norm), 4)})
        results["shannon_entropy"].append({"year": y, "H": round(float(H), 4), "H_max": round(float(max_entropy(D)), 4), "H_ratio": round(float(H / max_entropy(D)), 4)})
        
        # Perturbation and distance (year-on-year)
        if i > 0:
            prev_comp = compositions[country][years[i-1]]
            prev_year = years[i-1]
            
            # Perturbation difference
            p_diff = perturbation_difference(prev_comp, comp)
            
            # Aitchison distance
            d_A = aitchison_distance(prev_comp, comp)
            cumulative_d += d_A
            
            # Aitchison norm of perturbation (should equal distance)
            p_norm = aitchison_norm(p_diff)
            
            results["perturbation_series"].append({
                "from_year": prev_year,
                "to_year": y,
                "perturbation": {c: round(float(p_diff[j]), 8) for j, c in enumerate(CARRIERS)},
                "perturbation_clr": {c: round(float(clr(p_diff)[j]), 4) for j, c in enumerate(CARRIERS)},
            })
            
            results["aitchison_distances"].append({
                "from_year": prev_year,
                "to_year": y,
                "d_A": round(float(d_A), 4),
                "perturbation_norm": round(float(p_norm), 4),
            })
            
            results["cumulative_distances"].append({
                "year": y,
                "cumulative_d_A": round(float(cumulative_d), 4),
            })
    
    # Drift flags: identify years where d_A exceeds mean + 2σ
    distances = [d["d_A"] for d in results["aitchison_distances"]]
    if distances:
        mean_d = np.mean(distances)
        std_d = np.std(distances)
        threshold = mean_d + 2 * std_d
        
        results["drift_statistics"] = {
            "mean_d_A": round(float(mean_d), 4),
            "std_d_A": round(float(std_d), 4),
            "threshold_2sigma": round(float(threshold), 4),
            "median_d_A": round(float(np.median(distances)), 4),
            "max_d_A": round(float(np.max(distances)), 4),
            "total_cumulative": round(float(cumulative_d), 4),
        }
        
        for entry in results["aitchison_distances"]:
            if entry["d_A"] > threshold:
                results["drift_flags"].append({
                    "from_year": entry["from_year"],
                    "to_year": entry["to_year"],
                    "d_A": entry["d_A"],
                    "sigma_excess": round((entry["d_A"] - mean_d) / std_d, 2),
                })
    
    # Distance from 2000 baseline to each subsequent year
    baseline = compositions[country][years[0]]
    results["distance_from_baseline"] = []
    for y in years:
        d_from_base = aitchison_distance(baseline, compositions[country][y])
        results["distance_from_baseline"].append({
            "year": y,
            "d_A_from_2000": round(float(d_from_base), 4),
        })
    
    return results

# ── 5. Main ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("CoDaWork 2026 — Compositional monitoring of energy-mix drift")
    print("=" * 65)
    
    print("\n[1] Loading EMBER data...")
    compositions = load_ember_compositions()
    
    for country in COUNTRIES:
        years = sorted(compositions[country].keys())
        print(f"  {country}: {len(years)} years ({min(years)}-{max(years)})")
        # Show 2000 and latest composition
        for y in [min(years), max(years)]:
            comp = compositions[country][y]
            parts = ", ".join(f"{c}={comp[i]:.3f}" for i, c in enumerate(CARRIERS))
            print(f"    {y}: [{parts}]")
    
    all_results = {}
    
    for country in COUNTRIES:
        print(f"\n[2] Running protocol for {country}...")
        results = run_monitoring_protocol(compositions, country)
        all_results[country] = results
        
        # Summary
        stats = results["drift_statistics"]
        print(f"  Mean d_A = {stats['mean_d_A']:.4f}, σ = {stats['std_d_A']:.4f}")
        print(f"  Threshold (μ+2σ) = {stats['threshold_2sigma']:.4f}")
        print(f"  Max d_A = {stats['max_d_A']:.4f}")
        print(f"  Total cumulative drift = {stats['total_cumulative']:.4f}")
        
        # Top 5 largest year-on-year distances
        sorted_d = sorted(results["aitchison_distances"], key=lambda x: -x["d_A"])
        print(f"  Top 5 drift years:")
        for entry in sorted_d[:5]:
            print(f"    {entry['from_year']}→{entry['to_year']}: d_A = {entry['d_A']:.4f}")
        
        # Drift flags
        if results["drift_flags"]:
            print(f"  ⚑ DRIFT FLAGS (>{stats['threshold_2sigma']:.4f}):")
            for flag in results["drift_flags"]:
                print(f"    {flag['from_year']}→{flag['to_year']}: d_A = {flag['d_A']:.4f} ({flag['sigma_excess']}σ above mean)")
        
        # Effective diversity trend
        n_eff_start = results["effective_diversity"][0]
        n_eff_end = results["effective_diversity"][-1]
        print(f"  Effective diversity: {n_eff_start['N_eff']:.2f} ({n_eff_start['year']}) → {n_eff_end['N_eff']:.2f} ({n_eff_end['year']})")
        
        # Distance from baseline
        d_latest = results["distance_from_baseline"][-1]
        print(f"  Total structural shift from 2000: d_A = {d_latest['d_A_from_2000']:.4f}")
    
    # Save full results
    # Convert numpy types for JSON
    def convert(obj):
        if isinstance(obj, (np.integer,)): return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return obj
    
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            return convert(obj)
    
    with open(OUT_PATH, 'w') as f:
        json.dump(all_results, f, indent=2, cls=NpEncoder)
    print(f"\n[✓] Full results saved to {OUT_PATH}")
    
    # ── KEY ABSTRACT CLAIMS VERIFICATION ──
    print("\n" + "=" * 65)
    print("ABSTRACT CLAIM VERIFICATION")
    print("=" * 65)
    
    # Japan: Fukushima spike 2011-2012
    jp_distances = {d["to_year"]: d["d_A"] for d in all_results["Japan"]["aitchison_distances"]}
    print(f"\n1. Japan post-Fukushima nuclear withdrawal:")
    for y in [2011, 2012, 2013]:
        if y in jp_distances:
            print(f"   {y-1}→{y}: d_A = {jp_distances[y]:.4f}")
    
    # Germany: nuclear phase-out
    de_distances = {d["to_year"]: d["d_A"] for d in all_results["Germany"]["aitchison_distances"]}
    print(f"\n2. Germany nuclear phase-out trajectory:")
    de_nuc = {y: all_results["Germany"]["compositions"][y]["Nuclear"] for y in sorted(all_results["Germany"]["compositions"].keys())}
    for y in [2011, 2015, 2020, 2022, 2023, 2024, 2025]:
        if y in de_nuc:
            print(f"   {y}: Nuclear share = {de_nuc[y]:.4f} ({de_nuc[y]*100:.1f}%)")
    
    # UK: coal exit
    uk_distances = {d["to_year"]: d["d_A"] for d in all_results["United Kingdom"]["aitchison_distances"]}
    print(f"\n3. United Kingdom coal exit:")
    uk_coal = {y: all_results["United Kingdom"]["compositions"][y]["Coal"] for y in sorted(all_results["United Kingdom"]["compositions"].keys())}
    for y in [2000, 2005, 2010, 2015, 2020, 2024, 2025]:
        if y in uk_coal:
            print(f"   {y}: Coal share = {uk_coal[y]:.4f} ({uk_coal[y]*100:.1f}%)")
    
    print("\n[✓] Protocol complete.")
