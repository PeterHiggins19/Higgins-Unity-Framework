#!/usr/bin/env python3
"""
HIGGINS TRANSCENDENTAL PRETEST (HTP)
=====================================
Rapid pre-classifier for compositional systems based on the
Transcendental Naturalness Hypothesis (Peter Higgins, 2026).

Runs Steps 4-8 of the Higgins Decomposition pipeline against
the expanded 35-constant transcendental library. Classifies each
system as NATURAL, INVESTIGATE, or FLAG.

All results are stored in a permanent collection JSON for
proof-of-theory data accumulation.

Author: Peter Higgins / Claude
Date: 2026-04-23
"""

import sys, os, json, time, hashlib
import numpy as np

sys.path.insert(0, "/sessions/wonderful-elegant-pascal")
from higgins_decomposition_12step import HigginsDecomposition, NumpyEncoder

# ============================================================
# EXPANDED TRANSCENDENTAL LIBRARY (35 constants)
# ============================================================
EXPANDED_CONSTANTS = {
    # Original 29
    "pi": np.pi, "1/pi": 1.0/np.pi, "e": np.e, "1/e": 1.0/np.e,
    "ln2": np.log(2), "1/ln2": 1.0/np.log(2),
    "phi": (1+np.sqrt(5))/2, "phi^2": ((1+np.sqrt(5))/2)**2,
    "1/phi": 2.0/(1+np.sqrt(5)),
    "sqrt2": np.sqrt(2), "1/sqrt2": 1.0/np.sqrt(2),
    "sqrt3": np.sqrt(3), "1/sqrt3": 1.0/np.sqrt(3),
    "euler_gamma": 0.5772156649015329, "catalan": 0.9159655941772190,
    "ln10": np.log(10), "1/ln10": 1.0/np.log(10),
    "pi/4": np.pi/4, "2pi": 2.0*np.pi,
    "e^pi": np.e**np.pi, "pi^e": np.pi**np.e,
    "sqrt5": np.sqrt(5), "1/sqrt5": 1.0/np.sqrt(5),
    "ln_phi": np.log((1+np.sqrt(5))/2), "pi^2/6": np.pi**2/6,
    "apery": 1.2020569031595942, "khinchin": 2.6854520010653064,
    "feigenbaum_delta": 4.6692016091029906, "feigenbaum_alpha": 2.5029078750958928,
    # 6 new (April 2026)
    "1/(2pi)": 1.0/(2.0*np.pi),
    "1/(e^pi)": 1.0/(np.e**np.pi),
    "1/(pi^e)": 1.0/(np.pi**np.e),
    "omega_lambert": 0.5671432904097838,
    "dottie": 0.7390851332151607,
    "glaisher_kinkelin": 1.2824271291006226,
}

# ============================================================
# PRETEST ENGINE
# ============================================================

def run_pretest(data, name="unnamed", domain="UNKNOWN", carriers=None,
                threshold_natural=0.01, threshold_investigate=0.05):
    """
    Run HTP on a data matrix.

    Parameters
    ----------
    data : np.ndarray, shape (N, D)
    name : str
    domain : str
    carriers : list of str
    threshold_natural : float (default 0.01 = 1% absolute)
    threshold_investigate : float (default 0.05 = 5% absolute)

    Returns
    -------
    dict with classification, matches, nearest approach, and full diagnostics
    """
    data = np.array(data, dtype=np.float64)
    N, D = data.shape
    if carriers is None:
        carriers = [f"C{i}" for i in range(D)]

    t0 = time.time()

    # Run Steps 1-8 of the pipeline
    hd = HigginsDecomposition("HTP", name, domain, carriers=carriers)
    hd.load_data(data)
    hd.close_to_simplex()
    hd.clr_transform()
    hd.aitchison_variance()
    hd.pll_parabola()

    # Expanded squeeze against 35 constants
    valid = hd.sigma2_A[2:]
    matches = []
    nearest = {"constant": None, "delta": float('inf'), "relative_pct": float('inf')}

    for cname, cval in EXPANDED_CONSTANTS.items():
        if cval <= 0:
            continue
        for idx, sv in enumerate(valid):
            if sv <= 0:
                continue
            for tv, label in [(sv, "direct"), (1.0/sv if sv > 1e-15 else 0, "reciprocal")]:
                if tv <= 0:
                    continue
                delta = abs(tv - cval)
                rel_pct = delta / cval * 100

                # Track nearest approach (any threshold)
                if delta < nearest["delta"]:
                    nearest = {
                        "constant": cname,
                        "constant_value": float(cval),
                        "delta": float(delta),
                        "relative_pct": float(rel_pct),
                        "test_type": label,
                        "time_index": int(idx + 2),
                        "sigma2_A": float(sv),
                    }

                if delta < threshold_investigate:
                    matches.append({
                        "constant": cname,
                        "constant_value": float(cval),
                        "delta": float(delta),
                        "relative_pct": float(rel_pct),
                        "test_type": label,
                        "time_index": int(idx + 2),
                        "sigma2_A": float(sv),
                        "is_natural_match": delta < threshold_natural,
                    })

    matches.sort(key=lambda m: m["delta"])
    elapsed = time.time() - t0

    # Classification
    natural_matches = [m for m in matches if m["is_natural_match"]]
    if natural_matches:
        classification = "NATURAL"
    elif matches:
        classification = "INVESTIGATE"
    else:
        classification = "FLAG"

    result = {
        "system": name,
        "domain": domain,
        "N": N,
        "D": D,
        "carriers": carriers,
        "data_hash": hashlib.sha256(data.tobytes()).hexdigest()[:16],
        "classification": classification,
        "n_natural_matches": len(natural_matches),
        "n_investigate_matches": len(matches) - len(natural_matches),
        "n_total_matches": len(matches),
        "nearest_approach": nearest,
        "top_matches": matches[:10],
        "sigma2_A_range": [float(valid.min()), float(valid.max())] if len(valid) > 0 else [0, 0],
        "sigma2_A_final": float(hd.sigma2_A[-1]) if N > 0 else 0,
        "pll_R2": float(hd.pll_result.get("R2", 0)) if hd.pll_result else 0,
        "pll_shape": hd.pll_result.get("shape", "unknown") if hd.pll_result else "unknown",
        "elapsed_s": float(elapsed),
        "library_size": len(EXPANDED_CONSTANTS),
        "thresholds": {"natural": threshold_natural, "investigate": threshold_investigate},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    return result


def sweep_and_store(systems, output_path):
    """
    Run HTP on multiple systems and store results.

    Parameters
    ----------
    systems : list of dict, each with keys: data, name, domain, carriers
    output_path : str, path to JSON output

    Returns
    -------
    dict with summary and per-system results
    """
    results = []
    for sys_info in systems:
        r = run_pretest(
            data=sys_info["data"],
            name=sys_info["name"],
            domain=sys_info["domain"],
            carriers=sys_info.get("carriers"),
        )
        results.append(r)
        tag = {"NATURAL": "✓", "INVESTIGATE": "?", "FLAG": "✗"}[r["classification"]]
        print(f"  {tag} {r['system']:<40} {r['classification']:<12} "
              f"matches={r['n_total_matches']:>4}  "
              f"nearest={r['nearest_approach']['constant']} δ={r['nearest_approach']['delta']:.6f}")

    # Summary
    n_natural = sum(1 for r in results if r["classification"] == "NATURAL")
    n_investigate = sum(1 for r in results if r["classification"] == "INVESTIGATE")
    n_flag = sum(1 for r in results if r["classification"] == "FLAG")

    collection = {
        "pretest": "Higgins Transcendental Pretest (HTP)",
        "version": "1.0",
        "library_size": len(EXPANDED_CONSTANTS),
        "hypothesis": "Transcendental Naturalness Hypothesis — Peter Higgins, 2026",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": {
            "total_systems": len(results),
            "NATURAL": n_natural,
            "INVESTIGATE": n_investigate,
            "FLAG": n_flag,
            "natural_pct": round(n_natural / len(results) * 100, 1) if results else 0,
        },
        "systems": results,
    }

    with open(output_path, 'w') as f:
        json.dump(collection, f, indent=2, cls=NumpyEncoder)

    print(f"\n  Summary: {n_natural} NATURAL, {n_investigate} INVESTIGATE, {n_flag} FLAG")
    print(f"  Saved: {output_path}")
    return collection


if __name__ == "__main__":
    print(f"HTP Library: {len(EXPANDED_CONSTANTS)} constants")
    print("Import and use run_pretest() or sweep_and_store()")
