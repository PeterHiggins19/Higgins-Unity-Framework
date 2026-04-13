#!/usr/bin/env python3
"""
CHEM_EITT_LAB_001 — Chemistry EITT Test Pipeline
==================================================
Tests Shannon-entropy near-invariance under geometric-mean block decimation
on chemical mixture compositions (mole fractions) from the CheMixHub benchmark.

Author:  Peter Higgins | Rogue Wave Audio
Contact: PeterHiggins@RogueWaveAudio.com
Repo:    github.com/PeterHiggins19/Higgins-Unity-Framework
Standard: RWA-001

Usage:
    1. Clone CheMixHub:  git clone https://github.com/chemcognition-lab/chemixhub.git
    2. Run:  python chem_eitt_pipeline.py --data-dir ./chemixhub/datasets

    Or point --data-dir at any folder containing processed_data.csv files
    with columns: mole_fraction_1, mole_fraction_2, ..., temperature_K

Dependencies:
    pip install pandas numpy scipy matplotlib seaborn --break-system-packages
"""

import argparse
import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore', category=RuntimeWarning)

# ─────────────────────────────────────────────────────────────────────
# CoDa OPERATIONS (standard Aitchison geometry)
# ─────────────────────────────────────────────────────────────────────

def closure(x, kappa=1.0):
    """Close a composition to sum to kappa. CoDa standard (Aitchison 1986)."""
    x = np.asarray(x, dtype=float)
    x = np.clip(x, 1e-15, None)  # avoid zeros
    return kappa * x / x.sum(axis=-1, keepdims=True)

def geometric_mean_rows(X):
    """Per-part geometric mean across rows. CoDa standard (Aitchison)."""
    log_X = np.log(np.clip(X, 1e-15, None))
    return np.exp(log_X.mean(axis=0))

def clr(x):
    """Centered log-ratio transform. CoDa standard (Aitchison 1986)."""
    x = np.clip(x, 1e-15, None)
    log_x = np.log(x)
    return log_x - log_x.mean(axis=-1, keepdims=True)

def shannon_entropy(x):
    """Shannon entropy H(x) = -sum(x_i * ln(x_i)). Information theory (Shannon 1948)."""
    x = np.asarray(x, dtype=float)
    x = closure(x)  # ensure valid composition
    x = np.clip(x, 1e-15, None)
    return -np.sum(x * np.log(x), axis=-1)

def k_eff(x):
    """Effective number of carriers. K_eff = exp(H(x)). HUF naming (Hill 1973)."""
    return np.exp(shannon_entropy(x))

def aitchison_distance(x, y):
    """Aitchison distance. d_A(x,y) = ||clr(x) - clr(y)||_2. CoDa standard."""
    return np.linalg.norm(clr(closure(x)) - clr(closure(y)))

def tv_distance(x, y):
    """Total variation distance. d_TV = 0.5 * sum|x_i - y_i|. Standard (NOT simplex-native)."""
    return 0.5 * np.sum(np.abs(closure(x) - closure(y)))


# ─────────────────────────────────────────────────────────────────────
# CORRECTIVE LENSES (Higgins, Rogue Wave Audio — April 2026)
# Three approaches to flatten entropy curvature across the simplex
# ─────────────────────────────────────────────────────────────────────

def renyi_entropy(x, q=2.0):
    """
    Rényi entropy H_q(x) = (1/(1-q)) * ln(sum(x_i^q)).
    q=1 recovers Shannon (limit). q=2 = collision entropy.
    q>1 naturally down-weights rare components (boundary smoothing).

    Confirmed by HUF for q=0.1 to 5.0: Shannon is not special.
    Rényi generalisation of EITT (Higgins, Rogue Wave Audio).
    """
    x = np.asarray(x, dtype=float)
    x = closure(x)
    x = np.clip(x, 1e-15, None)
    if np.isclose(q, 1.0):
        return shannon_entropy(x)
    return (1.0 / (1.0 - q)) * np.log(np.sum(x**q, axis=-1))

def aitchison_norm_from_neutral(x):
    """
    Aitchison distance from neutral element: ||x||_A = d_A(x, n).
    n = (1/D, ..., 1/D) = uniform composition (max entropy state).

    This has UNIFORM curvature everywhere on the simplex because the
    Aitchison metric is the natural Riemannian metric on S^D.
    No boundary distortion — the simplex's own ruler.

    CoDa standard metric (Aitchison 1986, Pawlowsky-Glahn & Egozcue 2001).
    """
    x = np.asarray(x, dtype=float)
    x = closure(x)
    x = np.clip(x, 1e-15, None)
    if x.ndim == 1:
        D = len(x)
        n = np.ones(D) / D
        return np.linalg.norm(clr(x) - clr(n))
    else:
        D = x.shape[1]
        n = np.ones(D) / D
        clr_n = clr(n)
        return np.linalg.norm(clr(x) - clr_n, axis=-1)

def jensen_correction(x, M):
    """
    Estimate the expected Jensen gap for geometric-mean averaging
    at composition x with block size M.

    For H(x) near a point x_bar, the bias from averaging M nearby
    compositions is approximately:

        E[H(geom_mean)] - H(x_bar) ≈ (1/2M) * tr(Hess_H(x_bar) . Cov)

    For Shannon entropy: Hess_ii = -1/x_i (diagonal).
    The trace simplifies to: sum(-1/x_i * var_i) / (2M)

    We estimate var_i from the data spread and return the correction.
    This is the "prescription" for the corrective lens.

    HUF new work (Higgins, Rogue Wave Audio, April 2026).
    """
    x = np.asarray(x, dtype=float)
    x = closure(x)
    x = np.clip(x, 1e-15, None)

    if x.ndim == 1:
        # Single composition — return the curvature magnitude
        return np.sum(1.0 / x)  # trace of -Hessian
    else:
        # For an array: compute local curvature at each point
        # Hessian diagonal of Shannon: d²H/dx_i² = -1/x_i
        # Correction ≈ (1/2M) * sum(var_i / x_i_bar)
        x_bar = closure(geometric_mean_rows(x))
        local_var = np.var(x, axis=0)
        hess_diag = 1.0 / np.clip(x_bar, 1e-10, None)  # |Hess_ii|
        correction = np.sum(hess_diag * local_var) / (2.0 * M)
        return correction


# ─────────────────────────────────────────────────────────────────────
# EITT DECIMATION (HUF — Higgins, Rogue Wave Audio)
# ─────────────────────────────────────────────────────────────────────

def block_decimate(compositions, M):
    """
    Geometric-mean block decimation at block size M.

    For each non-overlapping block of M consecutive compositions,
    compute the per-part geometric mean and re-close.

    This is the core EITT operation (Higgins, Rogue Wave Audio).
    The geometric mean is the CoDa standard centre (Fréchet mean on the simplex).
    """
    n = len(compositions)
    n_blocks = n // M
    if n_blocks < 2:
        return None  # not enough data for meaningful decimation

    trimmed = compositions[:n_blocks * M]
    blocks = trimmed.reshape(n_blocks, M, -1)

    decimated = np.zeros((n_blocks, compositions.shape[1]))
    for i in range(n_blocks):
        decimated[i] = closure(geometric_mean_rows(blocks[i]))

    return decimated


def eitt_test(compositions, M_values=(2, 3, 5)):
    """
    Run the EITT entropy-invariance test at multiple decimation ratios
    with THREE CORRECTIVE LENSES:

    1. RAW Shannon:        delta_M uncorrected (original EITT metric)
    2. JENSEN-CORRECTED:   delta_M minus the expected Hessian-based bias
    3. RÉNYI q=2:          collision entropy (naturally down-weights boundary)
    4. AITCHISON NORM:     d_A(x, neutral) — uniform curvature everywhere

    Each lens gives its own PASS/FAIL at |delta| < 2%.

    EITT (Higgins, Rogue Wave Audio). Lenses (Higgins, April 2026).
    """
    results = {}

    H_orig = shannon_entropy(compositions)
    mean_H_orig = np.mean(H_orig)

    if mean_H_orig < 1e-10:
        return None  # degenerate — essentially a pure component

    # Also compute alternative metrics on original
    R2_orig = renyi_entropy(compositions, q=2.0)
    mean_R2_orig = np.mean(R2_orig)
    AN_orig = aitchison_norm_from_neutral(compositions)
    mean_AN_orig = np.mean(AN_orig)

    results['original'] = {
        'n': len(compositions),
        'mean_H': float(mean_H_orig),
        'std_H': float(np.std(H_orig)),
        'mean_K_eff': float(np.mean(k_eff(compositions))),
        'mean_Renyi_q2': float(mean_R2_orig),
        'mean_Aitch_norm': float(mean_AN_orig),
    }

    for M in M_values:
        dec = block_decimate(compositions, M)
        if dec is None:
            continue

        # ── LENS 1: Raw Shannon ──
        H_dec = shannon_entropy(dec)
        mean_H_dec = np.mean(H_dec)
        delta_M_raw = (mean_H_dec - mean_H_orig) / mean_H_orig * 100.0

        # ── LENS 2: Jensen-corrected Shannon ──
        # Subtract the expected Hessian bias from the raw delta
        j_correction = jensen_correction(compositions, M)
        # Correction is in absolute H units; convert to percentage of mean_H
        j_correction_pct = j_correction / mean_H_orig * 100.0
        delta_M_corrected = delta_M_raw - j_correction_pct

        # ── LENS 3: Rényi q=2 (collision entropy) ──
        R2_dec = renyi_entropy(dec, q=2.0)
        mean_R2_dec = np.mean(R2_dec)
        delta_M_renyi = (mean_R2_dec - mean_R2_orig) / mean_R2_orig * 100.0 if abs(mean_R2_orig) > 1e-10 else float('nan')

        # ── LENS 4: Aitchison norm from neutral ──
        AN_dec = aitchison_norm_from_neutral(dec)
        mean_AN_dec = np.mean(AN_dec)
        delta_M_aitch = (mean_AN_dec - mean_AN_orig) / mean_AN_orig * 100.0 if abs(mean_AN_orig) > 1e-10 else float('nan')

        # Bootstrap 95% CI on raw delta_M
        n_boot = 500
        boot_deltas = np.zeros(n_boot)
        for b in range(n_boot):
            idx_orig = np.random.randint(0, len(H_orig), size=len(H_orig))
            idx_dec = np.random.randint(0, len(H_dec), size=len(H_dec))
            boot_mean_orig = np.mean(H_orig[idx_orig])
            boot_mean_dec = np.mean(H_dec[idx_dec])
            if boot_mean_orig > 1e-10:
                boot_deltas[b] = (boot_mean_dec - boot_mean_orig) / boot_mean_orig * 100.0

        ci_lo, ci_hi = np.percentile(boot_deltas, [2.5, 97.5])

        # Aitchison variance comparison
        clr_orig = clr(compositions)
        clr_dec = clr(dec)
        aitch_var_orig = np.mean(np.var(clr_orig, axis=0))
        aitch_var_dec = np.mean(np.var(clr_dec, axis=0))
        var_ratio = aitch_var_dec / aitch_var_orig if aitch_var_orig > 1e-15 else float('nan')

        results[f'M={M}'] = {
            'n_blocks': len(dec),
            # Raw Shannon (original EITT)
            'delta_M_pct': float(delta_M_raw),
            'PASS': abs(delta_M_raw) < 2.0,
            'ci_95': [float(ci_lo), float(ci_hi)],
            # Jensen-corrected (Lens 1: prescription glasses)
            'delta_M_corrected_pct': float(delta_M_corrected),
            'jensen_correction_pct': float(j_correction_pct),
            'PASS_corrected': abs(delta_M_corrected) < 2.0,
            # Rényi q=2 (Lens 2: built-in boundary smoothing)
            'delta_M_renyi_q2_pct': float(delta_M_renyi),
            'PASS_renyi': abs(delta_M_renyi) < 2.0 if not np.isnan(delta_M_renyi) else False,
            # Aitchison norm (Lens 3: uniform curvature ruler)
            'delta_M_aitchison_pct': float(delta_M_aitch),
            'PASS_aitchison': abs(delta_M_aitch) < 2.0 if not np.isnan(delta_M_aitch) else False,
            # Diagnostics
            'aitchison_var_ratio': float(var_ratio),
            'mean_K_eff_dec': float(np.mean(k_eff(dec))),
        }

    return results


# ─────────────────────────────────────────────────────────────────────
# STATIONARITY CHECK (HUF diagnostic — autocorrelation boundary)
# ─────────────────────────────────────────────────────────────────────

def stationarity_check(compositions):
    """
    Check lag-1 autocorrelation in CLR coordinates.
    High autocorrelation → smooth evolution → EITT should hold.
    Low autocorrelation → jumpy/random → EITT may fail.
    """
    clr_coords = clr(compositions)
    n, D = clr_coords.shape
    if n < 4:
        return {'lag1_mean': float('nan'), 'stationary': None}

    lag1_corrs = []
    for d in range(D):
        series = clr_coords[:, d]
        if np.std(series) < 1e-15:
            continue
        corr = np.corrcoef(series[:-1], series[1:])[0, 1]
        if not np.isnan(corr):
            lag1_corrs.append(corr)

    mean_lag1 = np.mean(lag1_corrs) if lag1_corrs else float('nan')
    return {
        'lag1_mean': float(mean_lag1),
        'high_autocorrelation': mean_lag1 > 0.5 if not np.isnan(mean_lag1) else None,
    }


# ─────────────────────────────────────────────────────────────────────
# DATA LOADING — CheMixHub format
# ─────────────────────────────────────────────────────────────────────

def find_datasets(data_dir):
    """Find all processed CSV files in CheMixHub directory structure.

    CheMixHub layout:
        datasets/<name>/processed_data/processed_<Name>.csv
        datasets/<name>/processed_data/compounds.csv
    """
    data_dir = Path(data_dir)
    found = []

    # Strategy 1: CheMixHub naming — processed_*.csv inside processed_data/
    for csv_path in sorted(data_dir.rglob('processed_*.csv')):
        # Skip compounds.csv (metadata, not mixture data)
        if 'compounds' in csv_path.name.lower():
            continue
        dataset_name = csv_path.parent.parent.name  # datasets/<name>/processed_data/
        found.append((dataset_name, csv_path))

    # Strategy 2: fallback — any processed_data.csv
    if not found:
        for csv_path in sorted(data_dir.rglob('processed_data.csv')):
            dataset_name = csv_path.parent.parent.name
            found.append((dataset_name, csv_path))

    # Strategy 3: any CSV at top level
    if not found:
        for csv_path in sorted(data_dir.glob('*.csv')):
            found.append((csv_path.stem, csv_path))

    return found


def parse_list_string(s):
    """Parse a string like '[0.9537, 0.0463]' into a list of floats."""
    import ast
    try:
        if isinstance(s, (list, np.ndarray)):
            return [float(x) for x in s]
        s = str(s).strip()
        result = ast.literal_eval(s)
        return [float(x) for x in result]
    except (ValueError, SyntaxError):
        return None


def extract_compositions(df):
    """
    Extract mole-fraction composition columns from a CheMixHub dataframe.

    CheMixHub ILThermo format:
        cmp_mole_fractions = "[0.9537, 0.0463]"  (string-encoded list)
        cmp_ids = "[0.0, 625.0]"                  (compound identifiers)

    Other datasets may have explicit columns or different patterns.

    Returns (compositions_array, column_names) or (None, None).
    """
    # ── Strategy 1: CheMixHub string-encoded list columns ──
    list_col_candidates = [c for c in df.columns if any(
        p in c.lower() for p in ['mole_fraction', 'mol_frac', 'molefraction']
    )]

    for col in list_col_candidates:
        sample = df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else None
        if sample is not None and isinstance(sample, str) and '[' in sample:
            print(f"  Parsing list-encoded column: {col}")
            parsed = df[col].apply(parse_list_string)
            valid_mask = parsed.apply(lambda x: x is not None and len(x) >= 2)
            if valid_mask.sum() < 10:
                continue

            # Determine D from the MOST COMMON length (handles variable-length mixtures)
            lengths = parsed[valid_mask].apply(len)
            D = int(lengths.mode().iloc[0])
            # Only keep rows matching the most common length
            length_mask = parsed.apply(lambda x: x is not None and len(x) == D)
            valid_mask = valid_mask & length_mask
            if valid_mask.sum() < 10:
                continue

            comp_names = [f'x_{i+1}' for i in range(D)]
            print(f"  D = {D} parts ({valid_mask.sum()} valid rows of {len(df)})")

            # Build array
            comp_array = np.full((len(df), D), np.nan)
            for idx in range(len(df)):
                if valid_mask.iloc[idx]:
                    vals = parsed.iloc[idx]
                    comp_array[idx] = vals[:D]

            # Store validity mask in df for later filtering
            df['_comp_valid'] = valid_mask.values
            return comp_array, comp_names

    # ── Strategy 2: multiple explicit mole fraction columns ──
    frac_cols = [c for c in df.columns if any(
        p in c.lower() for p in ['mole_fraction', 'mol_frac', 'mole_frac']
    )]
    frac_cols += [c for c in df.columns if c.lower() in ('x_1', 'x_2', 'x_3', 'x1', 'x2', 'x3')]
    frac_cols = list(dict.fromkeys(frac_cols))

    if len(frac_cols) >= 2:
        comp = df[frac_cols].apply(pd.to_numeric, errors='coerce').values
        row_sums = np.nansum(comp, axis=1)
        if np.nanmedian(row_sums) > 0.5 and np.nanmedian(row_sums) < 2.0:
            return comp, frac_cols

    # ── Strategy 3: single fraction column (binary → infer x_2 = 1 - x_1) ──
    single_frac = [c for c in df.columns if 'fraction' in c.lower() and 'mass' not in c.lower()]
    if len(single_frac) == 1:
        x1 = pd.to_numeric(df[single_frac[0]], errors='coerce').values
        valid = ~np.isnan(x1) & (x1 > 0) & (x1 < 1)
        if np.sum(valid) > 100:
            x2 = 1.0 - x1
            comp = np.column_stack([x1, x2])
            return comp, [single_frac[0], f'1-{single_frac[0]}']

    # ── Strategy 4: numeric columns summing to ~1.0 ──
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    exclude_patterns = ['temp', 'press', 'viscosity', 'density', 'conductiv',
                        'enthalpy', 'solubility', 'index', 'id', 'year', 'log',
                        'target', 'label', 'split', 'unnamed', 'error',
                        'frequency', 'value', 'assumption']
    candidate_cols = [c for c in numeric_cols if not any(
        p in c.lower() for p in exclude_patterns
    )]

    if len(candidate_cols) >= 2:
        comp = df[candidate_cols].values.astype(float)
        row_sums = np.nansum(comp, axis=1)
        if np.nanmedian(row_sums) > 0.8 and np.nanmedian(row_sums) < 1.2:
            return comp, candidate_cols

    return None, None


def extract_axis_column(df):
    """Find the temperature or condition axis for ordering."""
    # Exact CheMixHub column names first
    for exact in ['Temperature, K', 'Temperature', 'temperature', 'T']:
        if exact in df.columns:
            return exact
    # Fuzzy match
    for pattern in ['temperature', 'temp', 'T_K', 't_k', 'T(K)', 'pressure', 'press']:
        matches = [c for c in df.columns if pattern.lower() in c.lower()]
        if matches:
            return matches[0]
    return None


def group_by_mixture(df, comp_cols, comp_array, axis_col, min_points=10):
    """
    Group data by unique compound pair (cmp_ids), creating composition sweeps.

    IMPORTANT: We group by compound pair ONLY, not by mole fraction.
    Within each group, rows have DIFFERENT compositions of the same compounds.
    We sort by x_1 (first mole fraction) to create a composition-sweep axis.

    This ensures EITT is tested on VARYING compositions, not trivially
    constant ones.

    If a temperature axis is available AND there are many rows at the same
    composition, we also create T-sweep groups as a secondary test.

    Returns list of (group_name, sorted_compositions_array).
    """
    groups = []

    # ── Strategy 1: CheMixHub — group by cmp_ids, sort by composition ──
    id_col = None
    for candidate in ['cmp_ids', 'compound_ids', 'mixture_id', 'cmp_ids_solvent']:
        if candidate in df.columns:
            id_col = candidate
            break

    if id_col:
        df = df.copy()
        grouped = df.groupby(id_col)
        n_comp_sweep = 0
        n_t_sweep = 0

        for name, group_df in grouped:
            indices = group_df.index
            comp = comp_array[indices]
            valid_mask = ~np.isnan(comp).any(axis=1) & (comp > 0).all(axis=1)
            comp_valid = comp[valid_mask]

            if len(comp_valid) < min_points:
                continue

            # Check if compositions actually vary
            comp_range = np.ptp(comp_valid[:, 0])  # range of x_1

            if comp_range > 0.01:
                # COMPOSITION SWEEP: sort by x_1 (first mole fraction)
                sort_idx = np.argsort(comp_valid[:, 0])
                comp_sorted = comp_valid[sort_idx]
                # Deduplicate: take unique compositions (average duplicates)
                _, unique_idx = np.unique(np.round(comp_sorted[:, 0], 6), return_index=True)
                comp_unique = comp_sorted[unique_idx]
                if len(comp_unique) >= min_points:
                    groups.append((f'comp_sweep|{str(name)[:60]}', comp_unique))
                    n_comp_sweep += 1

            # Also try T-sweep at fixed composition (if T available)
            if axis_col and axis_col in group_df.columns and comp_range > 0.01:
                # For each distinct composition, create a T-sweep
                frac_col = None
                for c in ['cmp_mole_fractions', 'cmp_mole_fractions_solvent']:
                    if c in group_df.columns:
                        frac_col = c
                        break
                if frac_col:
                    for frac_val, sub_df in group_df.groupby(frac_col):
                        if len(sub_df) >= min_points:
                            sub_indices = sub_df.sort_values(axis_col).index
                            sub_comp = comp_array[sub_indices]
                            sub_valid = ~np.isnan(sub_comp).any(axis=1) & (sub_comp > 0).all(axis=1)
                            sub_comp = sub_comp[sub_valid]
                            # Only include if composition actually varies
                            # (it might be constant for T-sweep — skip if so)
                            if len(sub_comp) >= min_points and np.ptp(sub_comp[:, 0]) > 0.001:
                                groups.append((f't_sweep|{str(name)[:40]}|{str(frac_val)[:30]}', sub_comp))
                                n_t_sweep += 1

        if groups:
            print(f"  → {n_comp_sweep} composition sweeps, {n_t_sweep} T-sweeps with varying comp")
            return groups

    # ── Strategy 2: explicit identifier columns ──
    id_cols = [c for c in df.columns if any(
        p in c.lower() for p in ['smiles', 'compound', 'system', 'name', 'formula']
    )]

    if id_cols:
        group_col = id_cols[0]
        grouped = df.groupby(group_col)

        for name, group_df in grouped:
            indices = group_df.index
            comp = comp_array[indices]
            valid_mask = ~np.isnan(comp).any(axis=1) & (comp > 0).all(axis=1)
            comp_valid = comp[valid_mask]

            if len(comp_valid) >= min_points and np.ptp(comp_valid[:, 0]) > 0.01:
                sort_idx = np.argsort(comp_valid[:, 0])
                groups.append((str(name)[:80], comp_valid[sort_idx]))

    # ── Strategy 3: fallback — full dataset sorted by x_1 ──
    if not groups:
        comp = comp_array.copy()
        valid_mask = ~np.isnan(comp).any(axis=1) & (comp > 0).all(axis=1)
        comp_valid = comp[valid_mask]
        if len(comp_valid) >= min_points and np.ptp(comp_valid[:, 0]) > 0.01:
            sort_idx = np.argsort(comp_valid[:, 0])
            groups.append(('full_dataset_by_x1', comp_valid[sort_idx]))

    return groups


# ─────────────────────────────────────────────────────────────────────
# SYNTHETIC DATA GENERATOR (for testing without CheMixHub)
# ─────────────────────────────────────────────────────────────────────

def generate_synthetic_mixture_data(n_points=200, D=3, seed=42):
    """
    Generate synthetic compositional data mimicking a smooth T-sweep
    of a chemical mixture.

    Simulates a ternary mixture where component ratios change smoothly
    with temperature (like a distillation curve).
    """
    rng = np.random.default_rng(seed)

    # Smooth underlying trend (logistic transitions)
    t = np.linspace(0, 1, n_points)

    # Component 1: decreases (like a volatile species evaporating)
    alpha_1 = 0.5 * (1 - np.tanh(4 * (t - 0.5)))
    # Component 2: increases then decreases (intermediate)
    alpha_2 = 0.8 * np.exp(-20 * (t - 0.4)**2)
    # Component 3: increases (like a heavy species concentrating)
    alpha_3 = 0.3 + 0.5 * t

    # Stack and add small noise
    raw = np.column_stack([alpha_1, alpha_2, alpha_3])
    noise = rng.normal(0, 0.02, raw.shape)
    raw = np.clip(raw + noise, 0.01, None)

    # Close to simplex
    compositions = closure(raw)
    temperatures = np.linspace(300, 500, n_points)  # 300K to 500K

    return compositions, temperatures


def generate_phase_transition_data(n_points=200, D=3, seed=42):
    """
    Generate synthetic data with a phase transition (discontinuity).
    EITT should FAIL here — this is the negative control.
    """
    rng = np.random.default_rng(seed)

    t = np.linspace(0, 1, n_points)
    mid = n_points // 2

    # Smooth before transition
    alpha_1 = np.concatenate([
        0.6 * np.ones(mid) + rng.normal(0, 0.02, mid),
        0.2 * np.ones(n_points - mid) + rng.normal(0, 0.02, n_points - mid)
    ])
    alpha_2 = np.concatenate([
        0.3 * np.ones(mid) + rng.normal(0, 0.02, mid),
        0.7 * np.ones(n_points - mid) + rng.normal(0, 0.02, n_points - mid)
    ])
    alpha_3 = np.concatenate([
        0.1 * np.ones(mid) + rng.normal(0, 0.01, mid),
        0.1 * np.ones(n_points - mid) + rng.normal(0, 0.01, n_points - mid)
    ])

    raw = np.column_stack([alpha_1, alpha_2, alpha_3])
    raw = np.clip(raw, 0.01, None)
    compositions = closure(raw)
    temperatures = np.linspace(300, 500, n_points)

    return compositions, temperatures


# ─────────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────────────

def run_pipeline(data_dir=None, output_dir=None, max_groups=50):
    """
    Run the full CHEM_EITT_LAB_001 pipeline.

    If data_dir is provided, loads CheMixHub data.
    Otherwise, runs on synthetic data as a proof-of-concept.
    """
    if output_dir is None:
        output_dir = Path('.')
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    # ── SYNTHETIC TESTS (always run as baseline) ──────────────
    print("=" * 70)
    print("CHEM_EITT_LAB_001 — Chemistry EITT Test Pipeline")
    print("Peter Higgins | Rogue Wave Audio | PeterHiggins@RogueWaveAudio.com")
    print("=" * 70)

    print("\n── SYNTHETIC BASELINE TESTS ──")

    # Test 1: Smooth mixture evolution (should PASS)
    print("\n[SYNTHETIC] Smooth ternary mixture (T-sweep, no phase transition):")
    comp_smooth, T_smooth = generate_synthetic_mixture_data()
    stat_smooth = stationarity_check(comp_smooth)
    print(f"  Points: {len(comp_smooth)}, D: {comp_smooth.shape[1]}")
    print(f"  Lag-1 autocorrelation (CLR): {stat_smooth['lag1_mean']:.3f}")

    result_smooth = eitt_test(comp_smooth)
    if result_smooth:
        o = result_smooth['original']
        print(f"  Original: H={o['mean_H']:.4f}  K_eff={o['mean_K_eff']:.2f}  "
              f"Renyi_q2={o['mean_Renyi_q2']:.4f}  Aitch_norm={o['mean_Aitch_norm']:.4f}")
        print(f"  {'M':>4s}  {'RAW delta':>10s}  {'JENSEN':>10s}  {'RENYI q=2':>10s}  {'AITCHISON':>10s}")
        for key, val in result_smooth.items():
            if key.startswith('M='):
                print(f"  {key:>4s}  {val['delta_M_pct']:+8.3f}%  "
                      f"{val['delta_M_corrected_pct']:+8.3f}%  "
                      f"{val['delta_M_renyi_q2_pct']:+8.3f}%  "
                      f"{val['delta_M_aitchison_pct']:+8.3f}%")
        all_results.append(('synthetic_smooth', result_smooth))

    # Test 2: Phase transition (should FAIL — negative control)
    print("\n[SYNTHETIC] Phase-transition mixture (discontinuity at midpoint):")
    comp_phase, T_phase = generate_phase_transition_data()
    stat_phase = stationarity_check(comp_phase)
    print(f"  Points: {len(comp_phase)}, D: {comp_phase.shape[1]}")
    print(f"  Lag-1 autocorrelation (CLR): {stat_phase['lag1_mean']:.3f}")

    result_phase = eitt_test(comp_phase)
    if result_phase:
        o = result_phase['original']
        print(f"  Original: H={o['mean_H']:.4f}  K_eff={o['mean_K_eff']:.2f}  "
              f"Renyi_q2={o['mean_Renyi_q2']:.4f}  Aitch_norm={o['mean_Aitch_norm']:.4f}")
        print(f"  {'M':>4s}  {'RAW delta':>10s}  {'JENSEN':>10s}  {'RENYI q=2':>10s}  {'AITCHISON':>10s}")
        for key, val in result_phase.items():
            if key.startswith('M='):
                print(f"  {key:>4s}  {val['delta_M_pct']:+8.3f}%  "
                      f"{val['delta_M_corrected_pct']:+8.3f}%  "
                      f"{val['delta_M_renyi_q2_pct']:+8.3f}%  "
                      f"{val['delta_M_aitchison_pct']:+8.3f}%")
        all_results.append(('synthetic_phase_transition', result_phase))

    # ── REAL DATA (if available) ─────────────────────────────
    if data_dir and Path(data_dir).exists():
        print(f"\n── REAL DATA from {data_dir} ──")
        datasets = find_datasets(data_dir)

        if not datasets:
            print(f"  No processed CSV files found in {data_dir}")
            print("  Expected structure: datasets/<name>/processed_data/processed_<Name>.csv")

        for ds_name, csv_path in datasets:
            print(f"\n[DATASET] {ds_name}")
            print(f"  File: {csv_path}")

            try:
                df = pd.read_csv(csv_path, low_memory=False)
                print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")

                comp_data, comp_cols = extract_compositions(df)
                if comp_data is None:
                    print(f"  ⚠ Could not identify composition columns. Columns: {list(df.columns)[:10]}")
                    continue

                print(f"  Composition columns: {comp_cols}")
                print(f"  D = {len(comp_cols)} parts")

                axis_col = extract_axis_column(df)
                print(f"  Axis column: {axis_col or 'none found'}")

                groups = group_by_mixture(df, comp_cols, comp_data, axis_col, min_points=10)
                print(f"  Mixture groups with >= 10 points: {len(groups)}")

                # Track all four lenses: Raw, Jensen-corrected, Rényi q=2, Aitchison norm
                # Split by interior vs boundary
                lens_names = ['raw', 'corrected', 'renyi', 'aitchison']
                lens_keys = ['PASS', 'PASS_corrected', 'PASS_renyi', 'PASS_aitchison']
                delta_keys = ['delta_M_pct', 'delta_M_corrected_pct', 'delta_M_renyi_q2_pct', 'delta_M_aitchison_pct']

                # Counters per lens, per region
                counts = {region: {lens: {'pass': 0, 'fail': 0, 'deltas': []}
                          for lens in lens_names}
                          for region in ['all', 'interior', 'boundary']}
                n_tested = 0
                boundary_cutoff = 0.05

                for grp_name, grp_comp in groups[:max_groups]:
                    grp_comp = closure(np.clip(grp_comp, 1e-10, None))

                    # Classify interior vs boundary
                    min_per_row = grp_comp.min(axis=1)
                    frac_near_edge = np.mean(min_per_row < boundary_cutoff)
                    region = 'interior' if frac_near_edge < 0.25 else 'boundary'

                    result = eitt_test(grp_comp, M_values=(2, 3))
                    if result is None:
                        continue

                    n_tested += 1
                    for key, val in result.items():
                        if not key.startswith('M='):
                            continue
                        for lens, pass_key, delta_key in zip(lens_names, lens_keys, delta_keys):
                            passed = val.get(pass_key, False)
                            delta = val.get(delta_key, float('nan'))
                            for r in ['all', region]:
                                if passed:
                                    counts[r][lens]['pass'] += 1
                                else:
                                    counts[r][lens]['fail'] += 1
                                if not np.isnan(delta):
                                    counts[r][lens]['deltas'].append(delta)

                    all_results.append((f'{ds_name}/{grp_name}', result))

                if n_tested > 0:
                    # Print four-lens comparison table
                    print(f"  {'':20s} {'RAW':>12s} {'JENSEN':>12s} {'RENYI q=2':>12s} {'AITCHISON':>12s}")
                    for region_label, region_key in [('ALL', 'all'), ('INTERIOR', 'interior'), ('BOUNDARY', 'boundary')]:
                        row = f"  {region_label:20s}"
                        has_data = False
                        for lens in lens_names:
                            c = counts[region_key][lens]
                            total = c['pass'] + c['fail']
                            if total > 0:
                                has_data = True
                                rate = c['pass'] / total * 100
                                mean_abs = np.mean(np.abs(c['deltas'])) if c['deltas'] else 0
                                row += f" {rate:5.1f}%|{mean_abs:4.2f}%"
                            else:
                                row += f"     {'---':>7s}"
                        if has_data:
                            print(row)

            except Exception as e:
                print(f"  ERROR: {e}")
                continue

    else:
        print("\n── NO REAL DATA DIRECTORY PROVIDED ──")
        print("  To run on CheMixHub data:")
        print("    git clone https://github.com/chemcognition-lab/chemixhub.git")
        print("    python chem_eitt_pipeline.py --data-dir ./chemixhub/datasets")

    # ── SUMMARY ──────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total experiments: {len(all_results)}")

    n_total_pass = 0
    n_total_fail = 0
    for name, res in all_results:
        for key, val in res.items():
            if key.startswith('M='):
                if val['PASS']:
                    n_total_pass += 1
                else:
                    n_total_fail += 1

    total = n_total_pass + n_total_fail
    if total > 0:
        print(f"EITT PASS: {n_total_pass}/{total} ({n_total_pass/total*100:.1f}%)")
        print(f"EITT FAIL: {n_total_fail}/{total} ({n_total_fail/total*100:.1f}%)")

    print("\nGovernance: HUF-GOV (measure, report, file)")
    print("Standard:   RWA-001")
    print("Contact:    PeterHiggins@RogueWaveAudio.com")
    print("=" * 70)

    return all_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='CHEM_EITT_LAB_001 — Chemistry EITT Test Pipeline'
    )
    parser.add_argument('--data-dir', type=str, default=None,
                        help='Path to CheMixHub datasets directory')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Directory for output files')
    parser.add_argument('--max-groups', type=int, default=50,
                        help='Maximum mixture groups to test per dataset')

    args = parser.parse_args()
    run_pipeline(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        max_groups=args.max_groups
    )
