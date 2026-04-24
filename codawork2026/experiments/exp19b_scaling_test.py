#!/usr/bin/env python3
"""
EXP-19b SUPPLEMENT: Scaling test to demonstrate O(N²) → O(N) speedup
at larger N values where the asymptotic improvement is visible.
"""

import sys
import time
import numpy as np
import json

sys.path.insert(0, "/sessions/wonderful-elegant-pascal")
from higgins_decomposition_12step import HigginsDecomposition, NumpyEncoder
from exp19b_pipeline_optimization import HigginsDecomposition_OptF

def make_test_data(N, D=3):
    """Generate a compositional test dataset of size N×D."""
    np.random.seed(42)
    raw = np.random.dirichlet(np.ones(D), size=N)
    return raw

def time_pipeline(pipeline_class, data, label, n_runs=3):
    """Time a pipeline class over n_runs, return median."""
    times = []
    for _ in range(n_runs):
        hd = pipeline_class(
            "scaling-test", label, "SCALING",
            carriers=[f"C{i}" for i in range(data.shape[1])]
        )
        hd.load_data(data)
        t0 = time.time()
        hd.run_full_pipeline()
        times.append(time.time() - t0)
    return np.median(times)

# Test at multiple N values
N_values = [100, 200, 500, 1000, 2000, 5000, 10000]
results = []

print(f"{'N':>7} | {'Original':>10} | {'Optimized':>10} | {'Speedup':>8} | {'Ratio':>8}")
print(f"{'-'*7}-+-{'-'*10}-+-{'-'*10}-+-{'-'*8}-+-{'-'*8}")

for N in N_values:
    data = make_test_data(N)

    t_orig = time_pipeline(HigginsDecomposition, data, f"original-N{N}")
    t_opt = time_pipeline(HigginsDecomposition_OptF, data, f"optimized-N{N}")

    speedup = t_orig / t_opt if t_opt > 0 else 0
    ratio_expected = N / 200  # Expected linear scaling of speedup with N

    results.append({
        "N": N,
        "original_s": t_orig,
        "optimized_s": t_opt,
        "speedup": speedup,
    })

    print(f"{N:>7} | {t_orig:>9.4f}s | {t_opt:>9.4f}s | {speedup:>7.2f}x | N/{N//1:>5}")

# Save
with open("/sessions/wonderful-elegant-pascal/EXP-19b_scaling_results.json", 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to EXP-19b_scaling_results.json")
