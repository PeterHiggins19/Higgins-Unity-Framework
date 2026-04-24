#!/usr/bin/env python3
"""
EXP-19: FOURIER CONJUGATE PAIR STUDY
=====================================
Systematic test of ALL known Fourier transform pairs through the
Higgins Decomposition 12-step pipeline.

Hypothesis: If the pipeline performs non-contact information recovery,
then running both sides of a Fourier conjugate pair through the instrument
should produce predictable, structurally related signatures. The pipeline
should preserve — not destroy — the conjugate relationship.

Method: For each known pair (f(t), F(ω)):
  1. Generate 3-part compositional data using f(t) as the generating function
  2. Generate 3-part compositional data using F(ω) as the generating function
  3. Run both through the 12-step Higgins Decomposition
  4. Compare: PLL shape, R², squeeze, entropy, angular velocity, chaos
  5. Look for reciprocal/symmetric/predictable relationships

The compositional embedding works as follows:
  Given a generating function g(x), we create a 3-part composition:
    Part 1 = |g(x)|          (signal energy)
    Part 2 = |g'(x)|         (rate of change energy)
    Part 3 = 1 - Part1 - Part2  (complement / residual)
  Each part is floored at ε=0.001, then the row is closed to sum to 1.
  This gives us a trajectory on the 3-simplex driven by the function's shape.

Fourier Pairs Tested:
  01. rect(t)       ↔  sinc(f)         — Rectangle / Cardinal sine
  02. tri(t)        ↔  sinc²(f)        — Triangle / Sinc-squared
  03. Gauss(t)      ↔  Gauss(f)        — Self-conjugate
  04. exp(-a|t|)    ↔  Lorentz(f)      — Bilateral exponential / Lorentzian
  05. δ(t)          ↔  1               — Dirac delta / Constant (limit case)
  06. cos(2πf₀t)    ↔  δ-pair          — Cosine / Delta pair (limit case)
  07. shah(t)        ↔  shah(f)         — Dirac comb / Self-conjugate
  08. sech(πt)      ↔  sech(πf)        — Hyperbolic secant / Self-conjugate
  09. exp(-at)u(t)  ↔  1/(a+2πif)      — One-sided exp / Complex Lorentzian
  10. sinc²(t)      ↔  tri(f)          — Reverse of pair 02
  11. J₀(2πt)       ↔  rect/√(1-f²)   — Bessel J₀ / Semicircle
  12. chirp(t)      ↔  chirp(f)        — Linear chirp / Self-conjugate (magnitude)

Author: Peter Higgins / Claude
Date: 2026-04-22
Experiment: EXP-19
Domain: INFORMATION THEORY / FOURIER ANALYSIS
"""

import sys
import os
import json
import numpy as np
import math

sys.path.insert(0, "/sessions/wonderful-elegant-pascal")
from higgins_decomposition_12step import HigginsDecomposition, NumpyEncoder, _bessel_j1

# ============================================================
# GENERATING FUNCTIONS — Both sides of each Fourier pair
# ============================================================

N = 200  # samples per experiment
EPS = 0.001  # floor value for zero replacement


def make_composition(g_values, dg_values):
    """Convert function values and derivative values into 3-part compositions.

    Part 1: |g(x)| normalized — signal amplitude energy
    Part 2: |g'(x)| normalized — rate-of-change energy
    Part 3: residual — information complement

    This maps any real function onto the 3-simplex, preserving its
    structural character (oscillatory, monotone, peaked, flat, etc.)
    """
    g_abs = np.abs(g_values)
    dg_abs = np.abs(dg_values)

    # Normalize each to [0, 1] range
    g_max = g_abs.max() if g_abs.max() > 0 else 1.0
    dg_max = dg_abs.max() if dg_abs.max() > 0 else 1.0

    p1 = g_abs / g_max * 0.6 + 0.05   # signal: 5% to 65%
    p2 = dg_abs / dg_max * 0.3 + 0.05  # derivative: 5% to 35%

    # Ensure p1 + p2 < 1
    total = p1 + p2
    mask = total > 0.90
    if mask.any():
        scale = 0.90 / total[mask]
        p1[mask] *= scale
        p2[mask] *= scale

    p3 = 1.0 - p1 - p2  # residual

    # Floor and re-close
    data = np.column_stack([p1, p2, p3])
    data = np.maximum(data, EPS)
    data = data / data.sum(axis=1, keepdims=True)

    return data


def numerical_derivative(values, dx):
    """Central difference derivative."""
    dv = np.zeros_like(values)
    dv[1:-1] = (values[2:] - values[:-2]) / (2 * dx)
    dv[0] = (values[1] - values[0]) / dx
    dv[-1] = (values[-1] - values[-2]) / dx
    return dv


# ============================================================
# PAIR 01: rect(t) ↔ sinc(f)
# ============================================================

def gen_rect(t_range=(-3, 3)):
    """Rectangle function: 1 for |t| < 0.5, else 0 (smoothed edges)."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    # Smooth rect with steep sigmoid for compositional continuity
    steepness = 50
    g = 1.0 / (1.0 + np.exp(-steepness * (t + 0.5))) - 1.0 / (1.0 + np.exp(-steepness * (t - 0.5)))
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "rect(t)"

def gen_sinc(f_range=(-10, 10)):
    """Sinc function: sin(πf)/(πf)."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = np.sinc(f)  # numpy sinc is sin(πx)/(πx)
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "sinc(f)"


# ============================================================
# PAIR 02: tri(t) ↔ sinc²(f)
# ============================================================

def gen_tri(t_range=(-3, 3)):
    """Triangle function: 1-|t| for |t| < 1, else 0."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = np.maximum(1.0 - np.abs(t), 0.0)
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "tri(t)"

def gen_sinc2(f_range=(-10, 10)):
    """Sinc-squared: [sin(πf)/(πf)]²."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = np.sinc(f) ** 2
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "sinc²(f)"


# ============================================================
# PAIR 03: Gaussian ↔ Gaussian (self-conjugate)
# ============================================================

def gen_gaussian_t(t_range=(-4, 4)):
    """Gaussian: exp(-πt²)."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = np.exp(-np.pi * t**2)
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "Gauss(t)"

def gen_gaussian_f(f_range=(-4, 4)):
    """Gaussian in frequency domain: exp(-πf²)."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = np.exp(-np.pi * f**2)
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "Gauss(f)"


# ============================================================
# PAIR 04: exp(-a|t|) ↔ Lorentzian 2a/(a²+4π²f²)
# ============================================================

def gen_bilateral_exp(t_range=(-5, 5), a=1.0):
    """Bilateral exponential: exp(-a|t|)."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = np.exp(-a * np.abs(t))
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "exp(-|t|)"

def gen_lorentzian(f_range=(-5, 5), a=1.0):
    """Lorentzian: 2a/(a² + 4π²f²)."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = 2 * a / (a**2 + 4 * np.pi**2 * f**2)
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "Lorentz(f)"


# ============================================================
# PAIR 05: δ(t) ↔ 1 (Dirac delta / Constant) — limit case
# ============================================================

def gen_delta_approx(t_range=(-5, 5), sigma=0.05):
    """Narrow Gaussian approximation to δ(t)."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = np.exp(-t**2 / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "δ(t)≈narrow"

def gen_constant(f_range=(-5, 5)):
    """Constant function (FT of delta)."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = np.ones(N)
    dg = np.zeros(N)  # derivative of constant = 0
    # Add tiny variation to avoid degenerate composition
    g += np.random.RandomState(19).normal(0, 0.001, N)
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "const(f)"


# ============================================================
# PAIR 06: cos(2πf₀t) ↔ ½[δ(f-f₀) + δ(f+f₀)]
# ============================================================

def gen_cosine(t_range=(-5, 5), f0=2.0):
    """Cosine: cos(2πf₀t)."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = np.cos(2 * np.pi * f0 * t)
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "cos(2πf₀t)"

def gen_delta_pair(f_range=(-5, 5), f0=2.0, sigma=0.1):
    """Pair of narrow Gaussians at ±f₀ (FT of cosine)."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = (np.exp(-(f - f0)**2 / (2*sigma**2)) +
         np.exp(-(f + f0)**2 / (2*sigma**2))) / (2 * sigma * np.sqrt(2*np.pi))
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "δ-pair(f)"


# ============================================================
# PAIR 07: shah(t) ↔ shah(f) (Dirac comb — self-conjugate)
# ============================================================

def gen_shah_t(t_range=(-5, 5), period=1.0, sigma=0.05):
    """Dirac comb approximation: periodic narrow Gaussians."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = np.zeros(N)
    for k in range(int(t_range[0]/period) - 1, int(t_range[1]/period) + 2):
        g += np.exp(-(t - k*period)**2 / (2*sigma**2))
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "shah(t)"

def gen_shah_f(f_range=(-5, 5), period=1.0, sigma=0.05):
    """Dirac comb in frequency domain."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = np.zeros(N)
    for k in range(int(f_range[0]/period) - 1, int(f_range[1]/period) + 2):
        g += np.exp(-(f - k*period)**2 / (2*sigma**2))
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "shah(f)"


# ============================================================
# PAIR 08: sech(πt) ↔ sech(πf) (self-conjugate)
# ============================================================

def gen_sech_t(t_range=(-4, 4)):
    """Hyperbolic secant: sech(πt) = 1/cosh(πt)."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = 1.0 / np.cosh(np.pi * t)
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "sech(πt)"

def gen_sech_f(f_range=(-4, 4)):
    """Hyperbolic secant in freq domain: sech(πf)."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = 1.0 / np.cosh(np.pi * f)
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "sech(πf)"


# ============================================================
# PAIR 09: exp(-at)·u(t) ↔ 1/(a+2πif) — one-sided exponential
# ============================================================

def gen_onesided_exp(t_range=(-1, 8), a=1.0):
    """One-sided exponential: exp(-at) for t≥0, 0 otherwise."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = np.where(t >= 0, np.exp(-a * t), 0.0)
    # Smooth transition at t=0
    transition = 1.0 / (1.0 + np.exp(-50 * t))
    g = np.exp(-a * np.abs(t)) * transition
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "exp(-t)·u(t)"

def gen_complex_lorentz_mag(f_range=(-5, 5), a=1.0):
    """Magnitude of 1/(a+2πif) — the FT of one-sided exponential."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = 1.0 / np.sqrt(a**2 + (2*np.pi*f)**2)
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "|1/(a+2πif)|"


# ============================================================
# PAIR 10: sinc²(t) ↔ tri(f) — reverse of pair 02
# ============================================================

def gen_sinc2_t(t_range=(-10, 10)):
    """Sinc-squared in time domain."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = np.sinc(t) ** 2
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "sinc²(t)"

def gen_tri_f(f_range=(-3, 3)):
    """Triangle in frequency domain."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    g = np.maximum(1.0 - np.abs(f), 0.0)
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "tri(f)"


# ============================================================
# PAIR 11: J₀(2πt) ↔ rect(f)/√(1-f²) — Bessel / Semicircle
# ============================================================

def _bessel_j0(x):
    """J₀(x) via Miller backward recurrence (same algorithm as J₁)."""
    if abs(x) < 1e-15:
        return 1.0
    ax = abs(x)
    start_n = max(60, int(ax) + 30)
    jnp1 = 0.0
    jn = 1.0
    j_values = {}
    for n in range(start_n, 0, -1):
        jnm1 = 2.0 * n / ax * jn - jnp1
        j_values[n - 1] = jnm1
        jnp1 = jn
        jn = jnm1
    norm_sum = j_values.get(0, jn)
    for k in range(1, start_n // 2 + 1):
        if 2 * k in j_values:
            norm_sum += 2.0 * j_values[2 * k]
    scale = 1.0 / norm_sum
    return j_values.get(0, jn) * scale

def gen_bessel_j0(t_range=(0.1, 15)):
    """Bessel J₀(2πt)."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    g = np.array([_bessel_j0(2 * np.pi * ti) for ti in t])
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "J₀(2πt)"

def gen_semicircle(f_range=(-1.5, 1.5)):
    """rect(f)/√(1-f²) — FT of J₀, with smooth cutoff at |f|=1."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    f_clipped = np.clip(np.abs(f), 0, 0.999)
    g = np.where(np.abs(f) < 0.999, 1.0 / np.sqrt(1.0 - f_clipped**2), 0.01)
    # Smooth edges
    edge = 1.0 / (1.0 + np.exp(50 * (np.abs(f) - 0.98)))
    g = g * edge + 0.01 * (1 - edge)
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "1/√(1-f²)"


# ============================================================
# PAIR 12: chirp(t) ↔ chirp(f) — self-conjugate in magnitude
# ============================================================

def gen_chirp_t(t_range=(0, 10)):
    """Linear chirp: cos(πβt²) with Gaussian envelope."""
    t = np.linspace(t_range[0], t_range[1], N)
    dt = t[1] - t[0]
    beta = 2.0  # chirp rate
    envelope = np.exp(-0.1 * (t - 5)**2)
    g = envelope * np.cos(np.pi * beta * t**2)
    dg = numerical_derivative(g, dt)
    return make_composition(g, dg), "chirp(t)"

def gen_chirp_f(f_range=(-10, 10)):
    """Chirp in frequency: |FT of chirp| ~ chirp-like structure."""
    f = np.linspace(f_range[0], f_range[1], N)
    df = f[1] - f[0]
    beta = 2.0
    # Stationary phase: FT of Gaussian chirp is also a Gaussian chirp
    # |F(f)| ~ (1/√β) * exp(-π f²/β) * cos(πf²/β - π/4) approximately
    envelope = np.exp(-0.1 * f**2)
    g = envelope * np.cos(np.pi * f**2 / beta - np.pi/4)
    dg = numerical_derivative(g, df)
    return make_composition(g, dg), "chirp(f)"


# ============================================================
# MASTER EXPERIMENT RUNNER
# ============================================================

FOURIER_PAIRS = [
    ("01", "rect ↔ sinc",           gen_rect,           gen_sinc,            "CLASSIC"),
    ("02", "tri ↔ sinc²",           gen_tri,            gen_sinc2,           "CLASSIC"),
    ("03", "Gauss ↔ Gauss",         gen_gaussian_t,     gen_gaussian_f,      "SELF-CONJUGATE"),
    ("04", "exp(-|t|) ↔ Lorentz",   gen_bilateral_exp,  gen_lorentzian,      "CLASSIC"),
    ("05", "δ(t) ↔ const",          gen_delta_approx,   gen_constant,        "LIMIT"),
    ("06", "cos ↔ δ-pair",          gen_cosine,         gen_delta_pair,      "CLASSIC"),
    ("07", "shah ↔ shah",            gen_shah_t,         gen_shah_f,          "SELF-CONJUGATE"),
    ("08", "sech ↔ sech",           gen_sech_t,         gen_sech_f,          "SELF-CONJUGATE"),
    ("09", "exp·u(t) ↔ |1/(a+jω)|", gen_onesided_exp,  gen_complex_lorentz_mag, "CAUSAL"),
    ("10", "sinc² ↔ tri",           gen_sinc2_t,        gen_tri_f,           "CLASSIC (REVERSE)"),
    ("11", "J₀ ↔ 1/√(1-f²)",       gen_bessel_j0,      gen_semicircle,      "BESSEL"),
    ("12", "chirp ↔ chirp",         gen_chirp_t,        gen_chirp_f,         "SELF-CONJUGATE"),
]


def run_pair(pair_num, pair_name, gen_time, gen_freq, pair_type):
    """Run both sides of a Fourier pair through the 12-step pipeline."""

    # Generate time-domain composition
    data_t, label_t = gen_time()
    # Generate frequency-domain composition
    data_f, label_f = gen_freq()

    # Run time-domain side
    hd_t = HigginsDecomposition(
        f"EXP-19-{pair_num}T", f"Fourier Pair {pair_num}: {label_t}",
        "FOURIER_CONJUGATE", carriers=["Signal", "Derivative", "Residual"]
    )
    hd_t.load_data(data_t)
    result_t = hd_t.run_full_pipeline()

    # Run frequency-domain side
    hd_f = HigginsDecomposition(
        f"EXP-19-{pair_num}F", f"Fourier Pair {pair_num}: {label_f}",
        "FOURIER_CONJUGATE", carriers=["Signal", "Derivative", "Residual"]
    )
    hd_f.load_data(data_f)
    result_f = hd_f.run_full_pipeline()

    return {
        "pair_num": pair_num,
        "pair_name": pair_name,
        "pair_type": pair_type,
        "time_domain": {
            "label": label_t,
            "result": result_t,
        },
        "freq_domain": {
            "label": label_f,
            "result": result_f,
        },
    }


def extract_metrics(result):
    """Pull key metrics from a pipeline result."""
    steps = result.get("steps", {})
    return {
        "pll_shape": steps.get("step6_pll_shape", "?"),
        "pll_R2": steps.get("step6_pll_R2", 0),
        "squeeze_mean": steps.get("step7_squeeze_mean", 0),
        "squeeze_count": steps.get("step7_squeeze_count", 0),
        "entropy_mean": steps.get("step8_entropy_mean", 0),
        "entropy_cv": steps.get("step8_entropy_cv", 0),
        "angular_vel_std": steps.get("step9_angular_velocity_std", 0),
        "chaos_total": steps.get("step10_chaos", {}).get("total_deviations", 0) if isinstance(steps.get("step10_chaos"), dict) else 0,
        "chaos_reversals": steps.get("step10_chaos", {}).get("reversals", 0) if isinstance(steps.get("step10_chaos"), dict) else 0,
        "radius_range": steps.get("step12_radius_range", [0, 0]),
        "data_hash": result.get("data_hash_sha256_16", ""),
    }


def compute_pair_relationships(met_t, met_f):
    """Compute relationships between the time and frequency side metrics."""
    rels = {}

    # PLL shape relationship
    rels["pll_shape_match"] = met_t["pll_shape"] == met_f["pll_shape"]
    rels["pll_shape_pair"] = f"{met_t['pll_shape']} / {met_f['pll_shape']}"

    # Squeeze ratio
    if met_f["squeeze_mean"] > 1e-10:
        rels["squeeze_ratio_t_over_f"] = met_t["squeeze_mean"] / met_f["squeeze_mean"]
    else:
        rels["squeeze_ratio_t_over_f"] = float('inf')

    # Entropy difference
    rels["entropy_delta"] = met_t["entropy_mean"] - met_f["entropy_mean"]
    rels["entropy_ratio"] = met_t["entropy_mean"] / met_f["entropy_mean"] if met_f["entropy_mean"] > 1e-10 else float('inf')

    # Angular velocity ratio
    if met_f["angular_vel_std"] > 1e-10:
        rels["angular_vel_ratio"] = met_t["angular_vel_std"] / met_f["angular_vel_std"]
    else:
        rels["angular_vel_ratio"] = float('inf')

    # Chaos structure similarity
    total_chaos = met_t["chaos_total"] + met_f["chaos_total"]
    if total_chaos > 0:
        rels["chaos_symmetry"] = 1.0 - abs(met_t["chaos_total"] - met_f["chaos_total"]) / total_chaos
    else:
        rels["chaos_symmetry"] = 1.0  # Both zero = perfect symmetry

    # R² comparison
    rels["R2_delta"] = abs(met_t["pll_R2"] - met_f["pll_R2"])

    return rels


def main():
    print("=" * 80)
    print("  EXP-19: FOURIER CONJUGATE PAIR STUDY")
    print("  Testing ALL known Fourier transform pairs through Higgins Decomposition")
    print("=" * 80)

    all_results = {}
    all_metrics = {}
    all_relationships = {}

    for pair_num, pair_name, gen_t, gen_f, pair_type in FOURIER_PAIRS:
        print(f"\n  Pair {pair_num}: {pair_name} [{pair_type}]")

        pair_result = run_pair(pair_num, pair_name, gen_t, gen_f, pair_type)
        all_results[pair_num] = pair_result

        met_t = extract_metrics(pair_result["time_domain"]["result"])
        met_f = extract_metrics(pair_result["freq_domain"]["result"])
        all_metrics[pair_num] = {"time": met_t, "freq": met_f}

        rels = compute_pair_relationships(met_t, met_f)
        all_relationships[pair_num] = rels

        # Print summary line
        shape_sym = "=" if rels["pll_shape_match"] else "≠"
        print(f"    Time:  PLL={met_t['pll_shape']:5s}  R²={met_t['pll_R2']:.4f}  "
              f"σ²_A={met_t['squeeze_mean']:.4f}  H={met_t['entropy_mean']:.4f}  "
              f"ω_σ={met_t['angular_vel_std']:.4f}  chaos={met_t['chaos_total']}")
        print(f"    Freq:  PLL={met_f['pll_shape']:5s}  R²={met_f['pll_R2']:.4f}  "
              f"σ²_A={met_f['squeeze_mean']:.4f}  H={met_f['entropy_mean']:.4f}  "
              f"ω_σ={met_f['angular_vel_std']:.4f}  chaos={met_f['chaos_total']}")
        print(f"    Shape: {rels['pll_shape_pair']}  "
              f"σ²_ratio={rels['squeeze_ratio_t_over_f']:.3f}  "
              f"H_ratio={rels['entropy_ratio']:.3f}  "
              f"ω_ratio={rels['angular_vel_ratio']:.3f}  "
              f"chaos_sym={rels['chaos_symmetry']:.3f}")

    # ============================================================
    # ANALYSIS: Pattern Discovery
    # ============================================================
    print("\n" + "=" * 80)
    print("  MASTER COMPARISON TABLE")
    print("=" * 80)

    print(f"\n  {'Pair':28s} {'Type':16s} {'PLL t/f':12s} {'σ²_A ratio':>10s} "
          f"{'H ratio':>8s} {'ω ratio':>8s} {'Chaos sym':>9s} {'ΔR²':>6s}")
    print("  " + "-" * 98)

    for pair_num, pair_name, _, _, pair_type in FOURIER_PAIRS:
        rels = all_relationships[pair_num]
        met_t = all_metrics[pair_num]["time"]
        met_f = all_metrics[pair_num]["freq"]

        sq_ratio = rels["squeeze_ratio_t_over_f"]
        sq_str = f"{sq_ratio:.3f}" if sq_ratio < 1000 else "∞"

        ang_ratio = rels["angular_vel_ratio"]
        ang_str = f"{ang_ratio:.3f}" if ang_ratio < 1000 else "∞"

        print(f"  {pair_num}. {pair_name:24s} {pair_type:16s} "
              f"{rels['pll_shape_pair']:12s} {sq_str:>10s} "
              f"{rels['entropy_ratio']:>8.3f} {ang_str:>8s} "
              f"{rels['chaos_symmetry']:>9.3f} {rels['R2_delta']:>6.3f}")

    # ============================================================
    # KEY FINDINGS
    # ============================================================
    print("\n" + "=" * 80)
    print("  KEY FINDINGS")
    print("=" * 80)

    # 1. Self-conjugate pairs should give identical/near-identical metrics
    self_conj = [p for p in FOURIER_PAIRS if p[4] == "SELF-CONJUGATE"]
    print(f"\n  1. SELF-CONJUGATE PAIRS (should show ~1.0 ratios):")
    for pair_num, pair_name, _, _, _ in self_conj:
        rels = all_relationships[pair_num]
        sq = rels["squeeze_ratio_t_over_f"]
        h = rels["entropy_ratio"]
        w = rels["angular_vel_ratio"]
        near_unity = all(0.5 < r < 2.0 for r in [sq, h, w] if r < 1000)
        verdict = "PRESERVED" if near_unity else "BROKEN"
        print(f"    {pair_num}. {pair_name:24s}: σ²={sq:.3f} H={h:.3f} ω={w:.3f} → {verdict}")

    # 2. Classic pairs — do they show reciprocal structure?
    classic = [p for p in FOURIER_PAIRS if "CLASSIC" in p[4]]
    print(f"\n  2. CLASSIC PAIRS (testing for reciprocal signatures):")
    for pair_num, pair_name, _, _, _ in classic:
        rels = all_relationships[pair_num]
        met_t = all_metrics[pair_num]["time"]
        met_f = all_metrics[pair_num]["freq"]
        shape_sym = "SAME" if rels["pll_shape_match"] else "RECIPROCAL"
        print(f"    {pair_num}. {pair_name:24s}: PLL={shape_sym}  "
              f"ΔH={rels['entropy_delta']:+.4f}  chaos_sym={rels['chaos_symmetry']:.3f}")

    # 3. PLL shape preservation
    shape_matches = sum(1 for r in all_relationships.values() if r["pll_shape_match"])
    shape_total = len(all_relationships)
    print(f"\n  3. PLL SHAPE PRESERVATION: {shape_matches}/{shape_total} pairs share the same PLL shape")

    # 4. Overall information recovery score
    print(f"\n  4. INFORMATION RECOVERY ASSESSMENT:")
    recovery_scores = []
    for pair_num in all_relationships:
        rels = all_relationships[pair_num]
        # For self-conjugate: score = closeness to 1.0
        # For classic: score = consistency of relationships
        sq = rels["squeeze_ratio_t_over_f"]
        h = rels["entropy_ratio"]
        chaos = rels["chaos_symmetry"]

        if sq < 1000 and h < 1000:
            # Geometric mean of closeness-to-unity for self-conjugate,
            # or stability of ratio for classic pairs
            score = chaos  # chaos symmetry as baseline
            recovery_scores.append(score)

    if recovery_scores:
        mean_recovery = np.mean(recovery_scores)
        print(f"    Mean chaos symmetry across all pairs: {mean_recovery:.3f}")
        print(f"    (1.0 = perfect symmetry, 0.0 = completely asymmetric)")

    # ============================================================
    # SAVE RESULTS
    # ============================================================
    EXP_DIR = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Current-Repo/HUF/codawork2026/experiments"

    # Prepare serializable results
    save_data = {
        "experiment": "EXP-19",
        "name": "Fourier Conjugate Pair Study",
        "domain": "INFORMATION THEORY / FOURIER ANALYSIS",
        "date": "2026-04-22",
        "hypothesis": "Higgins Decomposition preserves Fourier conjugate structure — "
                      "predictable relationships between f(t) and F(ω) on the simplex.",
        "method": "12 known Fourier pairs, each side embedded as 3-part composition "
                  "[|g|, |g'|, residual], run through canonical 12-step pipeline.",
        "pairs_tested": len(FOURIER_PAIRS),
        "pair_catalog": {p[0]: {"name": p[1], "type": p[4]} for p in FOURIER_PAIRS},
        "metrics": {},
        "relationships": all_relationships,
        "findings": {
            "pll_shape_matches": shape_matches,
            "pll_shape_total": shape_total,
            "mean_chaos_symmetry": float(np.mean(recovery_scores)) if recovery_scores else 0,
        },
    }

    # Add per-pair metrics (without full pipeline results to keep size manageable)
    for pair_num in all_metrics:
        save_data["metrics"][pair_num] = all_metrics[pair_num]

    # Also save full pipeline results for each pair
    full_results = {}
    for pair_num, pair_data in all_results.items():
        full_results[pair_num] = {
            "pair_name": pair_data["pair_name"],
            "pair_type": pair_data["pair_type"],
            "time_domain": pair_data["time_domain"]["result"],
            "freq_domain": pair_data["freq_domain"]["result"],
        }
    save_data["full_pipeline_results"] = full_results

    # Save
    out_path = os.path.join(EXP_DIR, "EXP-19_12step_canonical.json")
    with open(out_path, 'w') as f:
        json.dump(save_data, f, indent=2, cls=NumpyEncoder)
    print(f"\n  Saved: {out_path}")
    print(f"  Size: {os.path.getsize(out_path):,} bytes")

    return save_data


if __name__ == "__main__":
    results = main()
