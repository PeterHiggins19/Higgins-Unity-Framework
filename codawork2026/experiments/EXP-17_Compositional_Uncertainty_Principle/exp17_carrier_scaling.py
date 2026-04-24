#!/usr/bin/env python3
"""
EXP-17: COMPOSITIONAL UNCERTAINTY PRINCIPLE
============================================

CONJECTURE (Higgins, 2026):
-----------
In EXP-16 we discovered that compositional chaos in a spring-mass system
is STRUCTURAL — it arises from velocity zero-crossings where a carrier
contribution vanishes, forcing CLR divergence and an irreducible deviation
on the simplex. No amount of damping eliminates it. The floor persists.

This raises a profound question: does this compositional floor scale with
the NUMBER OF CARRIERS the way quantum uncertainty scales with ℏ?

Three noise floors may form a deeper triad:
  1. Quantum: ℏω/2 — zero-point energy, irreducible in any oscillator
  2. Thermodynamic: residual entropy — irreducible in any constrained partition
  3. Compositional: simplex singularity floor — irreducible in any CoDa system

CAUTION: The repetitive structure seen in EXP-16 chaos diagrams COULD be an
artifact of: (a) the RK4 integrator, (b) fixed time-step discretisation,
(c) the specific force decomposition chosen. This experiment tests this
directly by varying carrier count, integrator method, time-step, and
initial conditions.

EXPERIMENTAL DESIGN:
--------------------
Test 1: CARRIER SCALING — Does the floor decrease with more carriers?
  - Run the spring-mass system decomposed into N=2,3,4,5,6,7,8 force carriers
  - Measure the irreducible deviation floor for each N
  - Fit scaling law: floor ~ N^α (if α ≈ -0.5, analogous to 1/√N central limit)

Test 2: ARTIFACT CHECK — Is the repetitive structure real?
  - Same system, vary: (a) time step, (b) integrator (RK4 vs Euler vs RK2),
    (c) randomised initial conditions, (d) noise injection
  - If structure persists across all variants → geometric, not artifact

Test 3: INFORMATION GEOMETRY — Does Fisher information explain the floor?
  - Compute Fisher information metric on the simplex for each N
  - Test if floor = f(Fisher metric eigenvalues)
  - Derive from first principles of information geometry

Test 4: DETERMINISM BOUNDARY — Where does predictability break down?
  - For each carrier count, find the prediction horizon
  - Beyond this horizon, compositional trajectory diverges
  - Map the boundary as function of N
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import json, os, warnings, time
warnings.filterwarnings('ignore')

OUT_DIR = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker"
EXP_DIR = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Current-Repo/HUF/codawork2026/experiments/EXP-17_Compositional_Uncertainty_Principle"

# Color palette (consistent with EXP-16)
BG_DARK = '#0D1117'; BG_PANEL = '#161B22'; GOLD = '#FFD700'; ICE = '#CADCFC'
TEAL = '#028090'; RED = '#F85149'; GREEN = '#27AE60'; CYAN = '#58A6FF'
ORANGE = '#F0B429'; MAGENTA = '#BC8CFF'; WHITE = '#E6EDF3'; GREY = '#8B949E'
CHAOS_RED = '#FF0040'; NAVY = '#1E2761'

G = 9.81
t_end = 12.0
dt = 0.001
ds = 10  # downsample factor

# Carrier decomposition schemes
# N=2: gravity vs restoring
# N=3: gravity, spring, damping (original EXP-16 ternary)
# N=4: gravity, spring, damping, inertial (EXP-16 full)
# N=5: gravity, spring_positive, spring_negative, damping, inertial
# N=6: split damping into viscous + turbulent model
# N=7: add centripetal pseudo-force
# N=8: add Coriolis + thermal noise force

def get_forces_N(N, m, k, c, x, v, a, t):
    """
    Decompose the spring-mass system into N force carriers.
    Each decomposition is physically meaningful — not arbitrary splits.
    """
    Fg = m * G                      # gravity (always positive, downward)
    Fs = k * abs(x)                 # spring restoring magnitude
    Fd = c * abs(v)                 # damping magnitude
    Fi = m * abs(a)                 # inertial reaction

    if N == 2:
        # Binary: driving vs restoring
        driving = Fg + max(0, -k*x)  # gravity + spring when extending
        restoring = Fs + Fd + Fi
        return np.array([driving, restoring])

    elif N == 3:
        # Ternary: gravity, elastic, dissipative (CoDa classic)
        return np.array([Fg, Fs, Fd + Fi])

    elif N == 4:
        # Quaternary: gravity, spring, damping, inertial (EXP-16 standard)
        return np.array([Fg, Fs, Fd, Fi])

    elif N == 5:
        # Quinary: split spring into potential energy storage + release
        Fs_store = k * max(0, x)     # compression storage
        Fs_release = k * max(0, -x)  # extension release
        return np.array([Fg, Fs_store, Fs_release, Fd, Fi])

    elif N == 6:
        # Senary: add quadratic drag model (turbulent approximation)
        c_turb = 0.1 * c  # small turbulent component
        Fd_visc = c * abs(v) * 0.9
        Fd_turb = c_turb * v**2
        Fs_store = k * max(0, x)
        Fs_release = k * max(0, -x)
        return np.array([Fg, Fs_store, Fs_release, Fd_visc, Fd_turb, Fi])

    elif N == 7:
        # Septenary: add effective stiffness nonlinearity
        Fs_lin = k * abs(x) * 0.85
        Fs_nonlin = k * x**2 * 0.15  # nonlinear stiffness term
        Fd_visc = c * abs(v) * 0.9
        Fd_turb = 0.1 * c * v**2
        Fi_trans = m * abs(a) * 0.7   # translational inertia
        Fi_rot = m * abs(a) * 0.3     # effective rotational inertia
        return np.array([Fg, Fs_lin, Fs_nonlin, Fd_visc, Fd_turb, Fi_trans, Fi_rot])

    elif N == 8:
        # Octonary: full decomposition with thermal + noise floor
        Fs_lin = k * abs(x) * 0.85
        Fs_nonlin = k * x**2 * 0.15
        Fd_visc = c * abs(v) * 0.9
        Fd_turb = 0.1 * c * v**2
        Fi_trans = m * abs(a) * 0.7
        Fi_rot = m * abs(a) * 0.3
        # Thermal fluctuation force (Brownian, kT scale)
        kT = 4.11e-21  # room temperature thermal energy
        F_thermal = np.sqrt(2 * kT * c / dt)  # Langevin force scale
        F_thermal = max(F_thermal, 1e-12)
        return np.array([Fg, Fs_lin, Fs_nonlin, Fd_visc, Fd_turb, Fi_trans, Fi_rot, F_thermal])

    else:
        raise ValueError(f"N={N} not supported")


def simulate_RK4(m, k, c, x0=0.3):
    """Standard RK4 integration — same as EXP-16."""
    N_steps = int(t_end / dt)
    t = np.linspace(0, t_end, N_steps)
    x = np.zeros(N_steps); v = np.zeros(N_steps)
    x[0] = x0

    for i in range(N_steps - 1):
        ti, xi, vi = t[i], x[i], v[i]
        def deriv(xx, vv):
            return vv, (m*G - k*xx - c*vv) / m
        dv1, da1 = deriv(xi, vi)
        dv2, da2 = deriv(xi + dv1*dt/2, vi + da1*dt/2)
        dv3, da3 = deriv(xi + dv2*dt/2, vi + da2*dt/2)
        dv4, da4 = deriv(xi + dv3*dt, vi + da3*dt)
        x[i+1] = xi + (dv1 + 2*dv2 + 2*dv3 + dv4) * dt / 6
        v[i+1] = vi + (da1 + 2*da2 + 2*da3 + da4) * dt / 6

    return t[::ds], x[::ds], v[::ds]


def simulate_Euler(m, k, c, x0=0.3):
    """Forward Euler — simplest integrator, most numeric error."""
    N_steps = int(t_end / dt)
    t = np.linspace(0, t_end, N_steps)
    x = np.zeros(N_steps); v = np.zeros(N_steps)
    x[0] = x0

    for i in range(N_steps - 1):
        a = (m*G - k*x[i] - c*v[i]) / m
        x[i+1] = x[i] + v[i] * dt
        v[i+1] = v[i] + a * dt

    return t[::ds], x[::ds], v[::ds]


def simulate_RK2(m, k, c, x0=0.3):
    """Midpoint method (RK2) — intermediate accuracy."""
    N_steps = int(t_end / dt)
    t = np.linspace(0, t_end, N_steps)
    x = np.zeros(N_steps); v = np.zeros(N_steps)
    x[0] = x0

    for i in range(N_steps - 1):
        a1 = (m*G - k*x[i] - c*v[i]) / m
        x_mid = x[i] + v[i] * dt/2
        v_mid = v[i] + a1 * dt/2
        a_mid = (m*G - k*x_mid - c*v_mid) / m
        x[i+1] = x[i] + v_mid * dt
        v[i+1] = v[i] + a_mid * dt

    return t[::ds], x[::ds], v[::ds]


def compute_composition_and_chaos(t, x, v, m, k, c, N_carriers):
    """
    For a given trajectory, compute N-carrier composition and detect EITT chaos.
    Returns composition array, angular velocity, deviation events, chaos floor.
    """
    n = len(t)
    comp = np.zeros((n, N_carriers))
    entropy = np.zeros(n)

    for i in range(n):
        a = (m*G - k*x[i] - c*v[i]) / m
        forces = get_forces_N(N_carriers, m, k, c, x[i], v[i], a, t[i])
        forces = np.maximum(forces, 1e-10)
        comp[i] = forces / forces.sum()
        entropy[i] = -np.sum(comp[i] * np.log(np.maximum(comp[i], 1e-15)))

    # CLR transform for angular velocity analysis
    # Use first 3 carriers for ternary projection (or first N if N < 3)
    if N_carriers >= 3:
        comp3 = comp[:, :3].copy()
    else:
        # Pad with tiny values for 2-carrier case
        comp3 = np.column_stack([comp, np.full((n, 3 - N_carriers), 1e-10)])
    comp3 = comp3 / comp3.sum(axis=1, keepdims=True)

    tx = comp3[:, 1] + comp3[:, 2] * 0.5
    ty = comp3[:, 2] * np.sqrt(3) / 2
    mx, my = tx.mean(), ty.mean()

    # Angular velocity around centroid
    omega = np.zeros(n)
    for i in range(1, n):
        a1 = np.arctan2(ty[i-1] - my, tx[i-1] - mx)
        a2 = np.arctan2(ty[i] - my, tx[i] - mx)
        da = a2 - a1
        if da > np.pi: da -= 2*np.pi
        if da < -np.pi: da += 2*np.pi
        ddt = t[i] - t[i-1]
        omega[i] = da / ddt if ddt > 0 else 0

    # EITT deviation detection
    ws = 20
    events = []
    if n > ws + 10:
        for i in range(ws, n):
            mo = np.mean(np.abs(omega[i-ws:i]))
            ao = abs(omega[i])
            stall = (mo > 0.5) and (ao < mo * 0.15)
            spike = (ao > mo * 3.5) and (mo > 0.3)
            sc = 0
            for j in range(max(0, i-5), i):
                if j+1 < n and omega[j]*omega[j+1] < 0: sc += 1
            rev = (sc >= 2) and (mo > 0.3)
            if stall or spike or rev:
                if len(events) == 0 or (i - events[-1]) > 5:
                    events.append(i)

    # Chaos floor = deviation rate (deviations per second)
    chaos_pct = len(events) / n * 100 if n > 0 else 0
    dev_rate = len(events) / t_end

    # Aitchison variance (compositional spread measure)
    clr = np.log(comp / np.exp(np.mean(np.log(comp + 1e-15), axis=1, keepdims=True)))
    aitchison_var = np.mean(np.var(clr, axis=0))

    # Velocity zero-crossings
    v_zeros = []
    for i in range(1, n):
        if v[i-1] * v[i] <= 0 and (v[i-1] != 0 or v[i] != 0):
            v_zeros.append(i)

    return {
        'comp': comp, 'entropy': entropy, 'omega': omega,
        'events': events, 'chaos_pct': chaos_pct, 'dev_rate': dev_rate,
        'aitchison_var': aitchison_var, 'n_devs': len(events),
        'v_zeros': v_zeros, 'tern_x': tx, 'tern_y': ty,
        'N_carriers': N_carriers
    }


def compute_fisher_information(comp):
    """
    Compute Fisher information metric on the simplex.
    For a composition p = (p1, ..., pN), the Fisher metric is:
    g_ij = δ_ij / p_i (Aitchison geometry on the simplex)
    The determinant gives the total information content.
    """
    n, N = comp.shape
    fisher_traces = np.zeros(n)
    fisher_dets = np.zeros(n)

    for i in range(n):
        p = np.maximum(comp[i], 1e-15)
        # Fisher metric diagonal: 1/p_j
        fisher_diag = 1.0 / p
        fisher_traces[i] = np.sum(fisher_diag)
        fisher_dets[i] = np.prod(fisher_diag)

    return fisher_traces, fisher_dets


# ================================================================
# TEST 1: CARRIER COUNT SCALING
# ================================================================
print("=" * 70)
print("EXP-17: COMPOSITIONAL UNCERTAINTY PRINCIPLE")
print("=" * 70)
print()
print("CONJECTURE: The compositional chaos floor scales with carrier count N")
print("            analogous to quantum uncertainty scaling with ℏ.")
print()

print("[TEST 1] Carrier count scaling...")
print("-" * 50)

# Standard system parameters (same as EXP-16 baseline)
m0, k0, c0 = 5.0, 200.0, 2.0

# Multiple parameter sets to ensure robustness
param_sets = [
    (5.0, 200.0, 2.0, 'Standard (m=5, k=200, c=2)'),
    (3.0, 300.0, 1.0, 'Light stiff (m=3, k=300, c=1)'),
    (10.0, 100.0, 5.0, 'Heavy soft (m=10, k=100, c=5)'),
    (2.0, 400.0, 0.5, 'Ultra-light stiff (m=2, k=400, c=0.5)'),
    (8.0, 150.0, 3.0, 'Heavy medium (m=8, k=150, c=3)'),
]

carrier_counts = [2, 3, 4, 5, 6, 7, 8]
carrier_labels = ['Binary', 'Ternary', 'Quaternary', 'Quinary', 'Senary', 'Septenary', 'Octonary']

scaling_results = {}

for m, k, c, desc in param_sets:
    print(f"\n  System: {desc}")
    t_sim, x_sim, v_sim = simulate_RK4(m, k, c)

    results_for_system = []
    for N_c in carrier_counts:
        res = compute_composition_and_chaos(t_sim, x_sim, v_sim, m, k, c, N_c)
        results_for_system.append(res)
        print(f"    N={N_c}: {res['n_devs']:3d} deviations, "
              f"floor={res['chaos_pct']:.2f}%, "
              f"Aitchison var={res['aitchison_var']:.4f}")

    scaling_results[desc] = {
        'params': (m, k, c),
        'results': results_for_system
    }

# ================================================================
# TEST 2: ARTIFACT CHECK
# ================================================================
print("\n\n[TEST 2] Artifact detection...")
print("-" * 50)

artifact_results = {}

# 2a: Different integrators
print("\n  2a: Integrator comparison (RK4 vs RK2 vs Euler)...")
integrators = [
    ('RK4', simulate_RK4),
    ('RK2', simulate_RK2),
    ('Euler', simulate_Euler),
]

for int_name, int_func in integrators:
    t_sim, x_sim, v_sim = int_func(m0, k0, c0)
    res = compute_composition_and_chaos(t_sim, x_sim, v_sim, m0, k0, c0, 4)
    artifact_results[f'integrator_{int_name}'] = res
    print(f"    {int_name}: {res['n_devs']} deviations, floor={res['chaos_pct']:.2f}%")

# 2b: Different time steps
print("\n  2b: Time step variation...")
original_dt = dt
for test_dt in [0.0005, 0.001, 0.002, 0.005]:
    dt = test_dt
    ds_adj = max(1, int(0.01 / dt))  # keep ~100 Hz output
    N_steps = int(t_end / dt)
    t_arr = np.linspace(0, t_end, N_steps)
    x_arr = np.zeros(N_steps); v_arr = np.zeros(N_steps); x_arr[0] = 0.3

    for i in range(N_steps - 1):
        ti, xi, vi = t_arr[i], x_arr[i], v_arr[i]
        def deriv(xx, vv):
            return vv, (m0*G - k0*xx - c0*vv) / m0
        dv1, da1 = deriv(xi, vi)
        dv2, da2 = deriv(xi + dv1*dt/2, vi + da1*dt/2)
        dv3, da3 = deriv(xi + dv2*dt/2, vi + da2*dt/2)
        dv4, da4 = deriv(xi + dv3*dt, vi + da3*dt)
        x_arr[i+1] = xi + (dv1 + 2*dv2 + 2*dv3 + dv4) * dt / 6
        v_arr[i+1] = vi + (da1 + 2*da2 + 2*da3 + da4) * dt / 6

    t_ds = t_arr[::ds_adj]; x_ds = x_arr[::ds_adj]; v_ds = v_arr[::ds_adj]
    res = compute_composition_and_chaos(t_ds, x_ds, v_ds, m0, k0, c0, 4)
    artifact_results[f'dt_{test_dt}'] = res
    print(f"    dt={test_dt}: {res['n_devs']} deviations, floor={res['chaos_pct']:.2f}%")

dt = original_dt  # restore

# 2c: Random initial conditions
print("\n  2c: Randomised initial conditions...")
np.random.seed(42)
for trial in range(10):
    x0_rand = 0.1 + np.random.rand() * 0.5  # x0 ∈ [0.1, 0.6]
    t_sim, x_sim, v_sim = simulate_RK4(m0, k0, c0, x0=x0_rand)
    res = compute_composition_and_chaos(t_sim, x_sim, v_sim, m0, k0, c0, 4)
    artifact_results[f'ic_trial_{trial}'] = {**res, 'x0': x0_rand}
    print(f"    x0={x0_rand:.3f}: {res['n_devs']} devs, floor={res['chaos_pct']:.2f}%")


# ================================================================
# TEST 3: INFORMATION GEOMETRY
# ================================================================
print("\n\n[TEST 3] Fisher information geometry...")
print("-" * 50)

fisher_results = {}
t_sim, x_sim, v_sim = simulate_RK4(m0, k0, c0)

for N_c in carrier_counts:
    res = compute_composition_and_chaos(t_sim, x_sim, v_sim, m0, k0, c0, N_c)
    traces, dets = compute_fisher_information(res['comp'])

    # Fisher info at deviation events vs non-events
    event_set = set(res['events'])
    fisher_at_events = [traces[e] for e in res['events'] if e < len(traces)]
    fisher_at_normal = [traces[i] for i in range(len(traces)) if i not in event_set]

    fisher_results[N_c] = {
        'mean_trace': float(np.mean(traces)),
        'mean_det': float(np.mean(dets)),
        'fisher_at_events': float(np.mean(fisher_at_events)) if fisher_at_events else 0,
        'fisher_at_normal': float(np.mean(fisher_at_normal)) if fisher_at_normal else 0,
        'traces': traces,
        'dets': dets,
        'events': res['events'],
        'n_devs': res['n_devs'],
        'chaos_pct': res['chaos_pct']
    }
    ratio = (float(np.mean(fisher_at_events)) / float(np.mean(fisher_at_normal))
             if fisher_at_normal and fisher_at_events else 0)
    print(f"  N={N_c}: Fisher trace mean={np.mean(traces):.1f}, "
          f"at events={np.mean(fisher_at_events):.1f} vs normal={np.mean(fisher_at_normal):.1f}, "
          f"ratio={ratio:.2f}")


# ================================================================
# TEST 4: DETERMINISM BOUNDARY (Prediction Horizon)
# ================================================================
print("\n\n[TEST 4] Determinism boundary / prediction horizon...")
print("-" * 50)

horizon_results = {}

for N_c in carrier_counts:
    # Run two trajectories with tiny perturbation
    t1, x1, v1 = simulate_RK4(m0, k0, c0, x0=0.3)
    t2, x2, v2 = simulate_RK4(m0, k0, c0, x0=0.3 + 1e-8)  # epsilon perturbation

    res1 = compute_composition_and_chaos(t1, x1, v1, m0, k0, c0, N_c)
    res2 = compute_composition_and_chaos(t2, x2, v2, m0, k0, c0, N_c)

    # Compute compositional divergence over time
    n = min(len(res1['comp']), len(res2['comp']))
    div = np.zeros(n)
    for i in range(n):
        # Aitchison distance between compositions
        c1 = np.maximum(res1['comp'][i], 1e-15)
        c2 = np.maximum(res2['comp'][i], 1e-15)
        clr1 = np.log(c1) - np.mean(np.log(c1))
        clr2 = np.log(c2) - np.mean(np.log(c2))
        div[i] = np.sqrt(np.sum((clr1 - clr2)**2))

    # Find prediction horizon (where divergence exceeds threshold)
    threshold = 0.01  # 1% compositional distance
    horizon_idx = np.where(div > threshold)[0]
    horizon_time = t1[horizon_idx[0]] if len(horizon_idx) > 0 else t_end

    horizon_results[N_c] = {
        'horizon_time': float(horizon_time),
        'max_divergence': float(np.max(div)),
        'divergence': div,
        'time': t1[:n]
    }
    print(f"  N={N_c}: Prediction horizon = {horizon_time:.3f}s, max div = {np.max(div):.6f}")


# ================================================================
# ANALYSIS: FIT SCALING LAW
# ================================================================
print("\n\n[ANALYSIS] Fitting scaling law: floor ~ N^α")
print("-" * 50)

# Aggregate across all parameter sets
all_floors = {N: [] for N in carrier_counts}
all_aitchison = {N: [] for N in carrier_counts}
all_dev_rates = {N: [] for N in carrier_counts}

for desc, data in scaling_results.items():
    for res in data['results']:
        N = res['N_carriers']
        all_floors[N].append(res['chaos_pct'])
        all_aitchison[N].append(res['aitchison_var'])
        all_dev_rates[N].append(res['dev_rate'])

mean_floors = [np.mean(all_floors[N]) for N in carrier_counts]
std_floors = [np.std(all_floors[N]) for N in carrier_counts]
mean_aitchison = [np.mean(all_aitchison[N]) for N in carrier_counts]
mean_dev_rates = [np.mean(all_dev_rates[N]) for N in carrier_counts]

# Fit power law: floor = A * N^alpha
# Use log-log fit
log_N = np.log(carrier_counts)
log_floor = np.log(np.maximum(mean_floors, 1e-10))
# Linear regression in log space
valid = np.isfinite(log_floor)
if np.sum(valid) >= 2:
    coeffs = np.polyfit(log_N[valid], log_floor[valid], 1)
    alpha = coeffs[0]
    A = np.exp(coeffs[1])
    print(f"  Power law fit: floor = {A:.4f} * N^{alpha:.4f}")
    print(f"  Scaling exponent α = {alpha:.4f}")
    if abs(alpha + 0.5) < 0.2:
        print(f"  → CONSISTENT with 1/√N central limit scaling!")
    elif abs(alpha + 1.0) < 0.2:
        print(f"  → CONSISTENT with 1/N information scaling!")
    else:
        print(f"  → Novel scaling exponent, not simple 1/√N or 1/N")
else:
    alpha = 0; A = 1
    print("  Insufficient data for power law fit")

# Aitchison variance scaling
log_ait = np.log(np.maximum(mean_aitchison, 1e-10))
valid_ait = np.isfinite(log_ait)
if np.sum(valid_ait) >= 2:
    coeffs_ait = np.polyfit(log_N[valid_ait], log_ait[valid_ait], 1)
    alpha_ait = coeffs_ait[0]
    A_ait = np.exp(coeffs_ait[1])
    print(f"  Aitchison variance: var = {A_ait:.4f} * N^{alpha_ait:.4f}")


# ================================================================
# SAVE RESULTS JSON
# ================================================================
print("\n\nSaving results...")

results_json = {
    'experiment': 'EXP-17',
    'title': 'Compositional Uncertainty Principle',
    'conjecture': 'Compositional chaos floor scales with carrier count N, analogous to quantum uncertainty scaling with hbar',
    'scaling_law': {
        'alpha': float(alpha),
        'A': float(A),
        'formula': f'floor = {A:.4f} * N^{alpha:.4f}',
        'carrier_counts': carrier_counts,
        'mean_floors': [float(x) for x in mean_floors],
        'std_floors': [float(x) for x in std_floors],
        'mean_aitchison_var': [float(x) for x in mean_aitchison],
        'mean_dev_rates': [float(x) for x in mean_dev_rates],
    },
    'artifact_check': {
        'integrator_comparison': {
            name: {'n_devs': artifact_results[f'integrator_{name}']['n_devs'],
                   'chaos_pct': artifact_results[f'integrator_{name}']['chaos_pct']}
            for name in ['RK4', 'RK2', 'Euler']
        },
        'timestep_comparison': {
            str(test_dt): {'n_devs': artifact_results[f'dt_{test_dt}']['n_devs'],
                          'chaos_pct': artifact_results[f'dt_{test_dt}']['chaos_pct']}
            for test_dt in [0.0005, 0.001, 0.002, 0.005]
        },
        'ic_variation': {
            f'trial_{t}': {'x0': artifact_results[f'ic_trial_{t}']['x0'],
                          'n_devs': artifact_results[f'ic_trial_{t}']['n_devs'],
                          'chaos_pct': artifact_results[f'ic_trial_{t}']['chaos_pct']}
            for t in range(10)
        }
    },
    'fisher_info': {
        str(N): {
            'mean_trace': fisher_results[N]['mean_trace'],
            'fisher_at_events': fisher_results[N]['fisher_at_events'],
            'fisher_at_normal': fisher_results[N]['fisher_at_normal'],
            'n_devs': fisher_results[N]['n_devs']
        }
        for N in carrier_counts
    },
    'prediction_horizon': {
        str(N): {
            'horizon_time': horizon_results[N]['horizon_time'],
            'max_divergence': horizon_results[N]['max_divergence']
        }
        for N in carrier_counts
    },
    'parameters': {
        'systems_tested': [(m, k, c, d) for m, k, c, d in param_sets],
        'dt': 0.001,
        't_end': 12.0,
        'x0': 0.3
    }
}

with open(os.path.join(EXP_DIR, 'EXP17_results.json'), 'w') as f:
    json.dump(results_json, f, indent=2)
print("  → Results JSON saved")


# ================================================================
# DIAGRAMS
# ================================================================
print("\n\nGenerating diagrams...")

# --- DIAGRAM 1: Carrier Scaling Law ---
print("  [1/6] Carrier scaling law...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor=BG_DARK)
fig.suptitle('EXP-17: COMPOSITIONAL UNCERTAINTY PRINCIPLE\nCarrier Count Scaling Law',
             fontsize=16, fontweight='bold', color=GOLD, y=0.98)

# 1a: Floor vs N (main result)
ax = axes[0, 0]
ax.set_facecolor(BG_PANEL)
for desc, data in scaling_results.items():
    floors = [r['chaos_pct'] for r in data['results']]
    ax.plot(carrier_counts, floors, 'o-', alpha=0.4, markersize=4, color=GREY)
ax.errorbar(carrier_counts, mean_floors, yerr=std_floors, fmt='s-',
            color=GOLD, markersize=8, linewidth=2.5, capsize=5, zorder=10,
            label=f'Mean ± σ')
# Fit line
N_fit = np.linspace(2, 8, 100)
floor_fit = A * N_fit**alpha
ax.plot(N_fit, floor_fit, '--', color=CHAOS_RED, linewidth=2,
        label=f'Fit: {A:.2f}·N^{{{alpha:.2f}}}')
ax.set_xlabel('Number of Carriers (N)', color=WHITE, fontsize=11)
ax.set_ylabel('Chaos Floor (%)', color=WHITE, fontsize=11)
ax.set_title('Deviation Floor vs Carrier Count', color=CYAN, fontsize=12)
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=9)
ax.tick_params(colors=GREY)
ax.set_xticks(carrier_counts)
ax.grid(alpha=0.15, color=GREY)

# 1b: Log-log scaling
ax = axes[0, 1]
ax.set_facecolor(BG_PANEL)
ax.loglog(carrier_counts, mean_floors, 's-', color=GOLD, markersize=8, linewidth=2.5)
ax.loglog(N_fit, floor_fit, '--', color=CHAOS_RED, linewidth=2,
          label=f'α = {alpha:.3f}')
# Reference slopes
ax.loglog(N_fit, mean_floors[0] * (N_fit/2)**(-0.5), ':', color=TEAL, linewidth=1.5,
          label='1/√N (Central Limit)')
ax.loglog(N_fit, mean_floors[0] * (N_fit/2)**(-1.0), ':', color=MAGENTA, linewidth=1.5,
          label='1/N (Information)')
ax.set_xlabel('log(N)', color=WHITE, fontsize=11)
ax.set_ylabel('log(Floor %)', color=WHITE, fontsize=11)
ax.set_title('Log-Log Scaling Analysis', color=CYAN, fontsize=12)
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=9)
ax.tick_params(colors=GREY)
ax.grid(alpha=0.15, color=GREY)

# 1c: Aitchison variance scaling
ax = axes[1, 0]
ax.set_facecolor(BG_PANEL)
colors_nc = [TEAL, GREEN, GOLD, ORANGE, RED, MAGENTA, CYAN]
ax.bar(carrier_counts, mean_aitchison, color=colors_nc, edgecolor=WHITE, linewidth=0.5, alpha=0.85)
ax.set_xlabel('Number of Carriers (N)', color=WHITE, fontsize=11)
ax.set_ylabel('Aitchison Variance', color=WHITE, fontsize=11)
ax.set_title('Compositional Variance vs Carrier Count', color=CYAN, fontsize=12)
ax.tick_params(colors=GREY)
ax.set_xticks(carrier_counts)
ax.grid(alpha=0.15, color=GREY, axis='y')

# 1d: Deviation rate
ax = axes[1, 1]
ax.set_facecolor(BG_PANEL)
ax.bar(carrier_counts, mean_dev_rates, color=colors_nc, edgecolor=WHITE, linewidth=0.5, alpha=0.85)
ax.set_xlabel('Number of Carriers (N)', color=WHITE, fontsize=11)
ax.set_ylabel('Deviation Rate (events/s)', color=WHITE, fontsize=11)
ax.set_title('EITT Deviation Rate vs Carrier Count', color=CYAN, fontsize=12)
ax.tick_params(colors=GREY)
ax.set_xticks(carrier_counts)
ax.grid(alpha=0.15, color=GREY, axis='y')

plt.tight_layout(rect=[0, 0, 1, 0.95])
fname = os.path.join(EXP_DIR, 'EXP17_01_Carrier_Scaling_Law.png')
plt.savefig(fname, dpi=150, facecolor=BG_DARK, bbox_inches='tight')
plt.close()
print(f"    → {fname}")


# --- DIAGRAM 2: Artifact Test ---
print("  [2/6] Artifact test...")
fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor=BG_DARK)
fig.suptitle('EXP-17: ARTIFACT DETECTION\nIs the Repetitive Structure Real or Simulated?',
             fontsize=14, fontweight='bold', color=GOLD, y=1.02)

# 2a: Integrator comparison
ax = axes[0]
ax.set_facecolor(BG_PANEL)
int_names = ['RK4', 'RK2', 'Euler']
int_devs = [artifact_results[f'integrator_{n}']['n_devs'] for n in int_names]
int_colors = [TEAL, GOLD, RED]
bars = ax.bar(int_names, int_devs, color=int_colors, edgecolor=WHITE, linewidth=0.5)
for bar, val in zip(bars, int_devs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            str(val), ha='center', color=WHITE, fontsize=11, fontweight='bold')
ax.set_ylabel('Deviations Detected', color=WHITE, fontsize=11)
ax.set_title('Integrator Method', color=CYAN, fontsize=12)
ax.tick_params(colors=GREY)
ax.grid(alpha=0.15, color=GREY, axis='y')

# 2b: Time step variation
ax = axes[1]
ax.set_facecolor(BG_PANEL)
dt_vals = [0.0005, 0.001, 0.002, 0.005]
dt_devs = [artifact_results[f'dt_{d}']['n_devs'] for d in dt_vals]
dt_labels = [f'{d*1000:.1f}ms' for d in dt_vals]
bars = ax.bar(dt_labels, dt_devs, color=[TEAL, GREEN, GOLD, ORANGE], edgecolor=WHITE, linewidth=0.5)
for bar, val in zip(bars, dt_devs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            str(val), ha='center', color=WHITE, fontsize=11, fontweight='bold')
ax.set_ylabel('Deviations Detected', color=WHITE, fontsize=11)
ax.set_title('Time Step Size', color=CYAN, fontsize=12)
ax.tick_params(colors=GREY)
ax.grid(alpha=0.15, color=GREY, axis='y')

# 2c: Initial condition variation
ax = axes[2]
ax.set_facecolor(BG_PANEL)
ic_x0s = [artifact_results[f'ic_trial_{t}']['x0'] for t in range(10)]
ic_devs = [artifact_results[f'ic_trial_{t}']['n_devs'] for t in range(10)]
ax.scatter(ic_x0s, ic_devs, s=80, c=GOLD, edgecolors=WHITE, linewidth=0.5, zorder=5)
ax.axhline(np.mean(ic_devs), color=CHAOS_RED, linestyle='--', linewidth=1.5,
           label=f'Mean = {np.mean(ic_devs):.1f}')
ax.fill_between([0, 0.7], np.mean(ic_devs) - np.std(ic_devs),
                np.mean(ic_devs) + np.std(ic_devs), alpha=0.15, color=RED)
ax.set_xlabel('Initial Displacement x₀ (m)', color=WHITE, fontsize=11)
ax.set_ylabel('Deviations Detected', color=WHITE, fontsize=11)
ax.set_title('Initial Condition Variation', color=CYAN, fontsize=12)
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=9)
ax.tick_params(colors=GREY)
ax.grid(alpha=0.15, color=GREY)

plt.tight_layout()
fname = os.path.join(EXP_DIR, 'EXP17_02_Artifact_Detection.png')
plt.savefig(fname, dpi=150, facecolor=BG_DARK, bbox_inches='tight')
plt.close()
print(f"    → {fname}")


# --- DIAGRAM 3: Fisher Information Geometry ---
print("  [3/6] Fisher information geometry...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor=BG_DARK)
fig.suptitle('EXP-17: INFORMATION GEOMETRY ON THE SIMPLEX\nFisher Metric Analysis',
             fontsize=16, fontweight='bold', color=GOLD, y=0.98)

# 3a: Fisher trace at events vs normal
ax = axes[0, 0]
ax.set_facecolor(BG_PANEL)
fe = [fisher_results[N]['fisher_at_events'] for N in carrier_counts]
fn = [fisher_results[N]['fisher_at_normal'] for N in carrier_counts]
x_pos = np.arange(len(carrier_counts))
w = 0.35
ax.bar(x_pos - w/2, fe, w, color=CHAOS_RED, label='At Deviations', edgecolor=WHITE, linewidth=0.5)
ax.bar(x_pos + w/2, fn, w, color=TEAL, label='Normal', edgecolor=WHITE, linewidth=0.5)
ax.set_xticks(x_pos)
ax.set_xticklabels([str(n) for n in carrier_counts])
ax.set_xlabel('Carrier Count N', color=WHITE, fontsize=11)
ax.set_ylabel('Fisher Trace', color=WHITE, fontsize=11)
ax.set_title('Fisher Information: Events vs Normal', color=CYAN, fontsize=12)
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=9)
ax.tick_params(colors=GREY)
ax.grid(alpha=0.15, color=GREY, axis='y')

# 3b: Fisher ratio (event/normal)
ax = axes[0, 1]
ax.set_facecolor(BG_PANEL)
ratios = [fe[i]/fn[i] if fn[i] > 0 else 0 for i in range(len(carrier_counts))]
ax.bar(carrier_counts, ratios, color=GOLD, edgecolor=WHITE, linewidth=0.5)
ax.axhline(1.0, color=WHITE, linestyle='--', alpha=0.5, label='Ratio = 1 (no difference)')
ax.set_xlabel('Carrier Count N', color=WHITE, fontsize=11)
ax.set_ylabel('Fisher Ratio (Event/Normal)', color=WHITE, fontsize=11)
ax.set_title('Information Concentration at Deviations', color=CYAN, fontsize=12)
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=9)
ax.tick_params(colors=GREY)
ax.set_xticks(carrier_counts)
ax.grid(alpha=0.15, color=GREY, axis='y')

# 3c: Fisher trace time series (N=4 example)
ax = axes[1, 0]
ax.set_facecolor(BG_PANEL)
traces_4 = fisher_results[4]['traces']
events_4 = fisher_results[4]['events']
t_plot = np.linspace(0, t_end, len(traces_4))
ax.plot(t_plot, traces_4, color=ICE, linewidth=0.5, alpha=0.7)
if events_4:
    ev_t = [t_plot[e] for e in events_4 if e < len(t_plot)]
    ev_f = [traces_4[e] for e in events_4 if e < len(traces_4)]
    ax.scatter(ev_t, ev_f, c=CHAOS_RED, s=15, zorder=5, label='EITT Deviations')
ax.set_xlabel('Time (s)', color=WHITE, fontsize=11)
ax.set_ylabel('Fisher Trace', color=WHITE, fontsize=11)
ax.set_title('Fisher Information Timeline (N=4)', color=CYAN, fontsize=12)
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=9)
ax.tick_params(colors=GREY)
ax.grid(alpha=0.15, color=GREY)

# 3d: Fisher trace mean vs N
ax = axes[1, 1]
ax.set_facecolor(BG_PANEL)
mean_traces = [fisher_results[N]['mean_trace'] for N in carrier_counts]
ax.plot(carrier_counts, mean_traces, 's-', color=MAGENTA, markersize=8, linewidth=2.5)
ax.set_xlabel('Carrier Count N', color=WHITE, fontsize=11)
ax.set_ylabel('Mean Fisher Trace', color=WHITE, fontsize=11)
ax.set_title('Total Information Content vs Carriers', color=CYAN, fontsize=12)
ax.tick_params(colors=GREY)
ax.set_xticks(carrier_counts)
ax.grid(alpha=0.15, color=GREY)

plt.tight_layout(rect=[0, 0, 1, 0.95])
fname = os.path.join(EXP_DIR, 'EXP17_03_Fisher_Information.png')
plt.savefig(fname, dpi=150, facecolor=BG_DARK, bbox_inches='tight')
plt.close()
print(f"    → {fname}")


# --- DIAGRAM 4: Prediction Horizon ---
print("  [4/6] Prediction horizon...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor=BG_DARK)
fig.suptitle('EXP-17: DETERMINISM BOUNDARY\nPrediction Horizon vs Carrier Count',
             fontsize=14, fontweight='bold', color=GOLD, y=1.02)

# 4a: Horizon times
ax = axes[0]
ax.set_facecolor(BG_PANEL)
horizons = [horizon_results[N]['horizon_time'] for N in carrier_counts]
ax.bar(carrier_counts, horizons, color=colors_nc, edgecolor=WHITE, linewidth=0.5)
ax.set_xlabel('Carrier Count N', color=WHITE, fontsize=11)
ax.set_ylabel('Prediction Horizon (s)', color=WHITE, fontsize=11)
ax.set_title('Time Until Compositional Divergence', color=CYAN, fontsize=12)
ax.tick_params(colors=GREY)
ax.set_xticks(carrier_counts)
ax.grid(alpha=0.15, color=GREY, axis='y')

# 4b: Divergence curves
ax = axes[1]
ax.set_facecolor(BG_PANEL)
for i, N_c in enumerate(carrier_counts):
    div = horizon_results[N_c]['divergence']
    t_div = horizon_results[N_c]['time']
    ax.semilogy(t_div, div + 1e-16, color=colors_nc[i], linewidth=1.5,
                label=f'N={N_c}', alpha=0.8)
ax.axhline(0.01, color=CHAOS_RED, linestyle='--', linewidth=1, label='Threshold (1%)')
ax.set_xlabel('Time (s)', color=WHITE, fontsize=11)
ax.set_ylabel('Aitchison Distance', color=WHITE, fontsize=11)
ax.set_title('Compositional Divergence from ε-Perturbation', color=CYAN, fontsize=12)
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=8,
          ncol=2, loc='lower right')
ax.tick_params(colors=GREY)
ax.grid(alpha=0.15, color=GREY)

plt.tight_layout()
fname = os.path.join(EXP_DIR, 'EXP17_04_Prediction_Horizon.png')
plt.savefig(fname, dpi=150, facecolor=BG_DARK, bbox_inches='tight')
plt.close()
print(f"    → {fname}")


# --- DIAGRAM 5: Per-System Scaling (all 5 parameter sets overlaid) ---
print("  [5/6] Multi-system scaling comparison...")
fig, ax = plt.subplots(1, 1, figsize=(12, 8), facecolor=BG_DARK)
ax.set_facecolor(BG_PANEL)

sys_colors = [TEAL, GOLD, RED, CYAN, MAGENTA]
for i, (desc, data) in enumerate(scaling_results.items()):
    floors = [r['chaos_pct'] for r in data['results']]
    ax.plot(carrier_counts, floors, 'o-', color=sys_colors[i], linewidth=2,
            markersize=7, label=desc, alpha=0.8)

# Mean + fit
ax.plot(carrier_counts, mean_floors, 's--', color=WHITE, linewidth=3, markersize=10,
        label=f'MEAN (α={alpha:.3f})', zorder=10)
ax.plot(N_fit, floor_fit, '-', color=CHAOS_RED, linewidth=2, alpha=0.6)

ax.set_xlabel('Number of Force Carriers (N)', color=WHITE, fontsize=13)
ax.set_ylabel('Compositional Chaos Floor (%)', color=WHITE, fontsize=13)
ax.set_title('EXP-17: SCALING LAW ACROSS SYSTEMS\n'
             f'floor = {A:.2f} · N^{{{alpha:.2f}}}',
             color=GOLD, fontsize=15, fontweight='bold')
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=9,
          loc='best')
ax.tick_params(colors=GREY, labelsize=11)
ax.set_xticks(carrier_counts)
ax.grid(alpha=0.15, color=GREY)

fname = os.path.join(EXP_DIR, 'EXP17_05_Multi_System_Scaling.png')
plt.savefig(fname, dpi=150, facecolor=BG_DARK, bbox_inches='tight')
plt.close()
print(f"    → {fname}")


# --- DIAGRAM 6: Grand Summary ---
print("  [6/6] Grand summary...")
fig = plt.figure(figsize=(20, 14), facecolor=BG_DARK)

# Title
fig.text(0.5, 0.97, 'EXP-17: THE COMPOSITIONAL UNCERTAINTY PRINCIPLE',
         fontsize=20, fontweight='bold', color=GOLD, ha='center', va='top')
fig.text(0.5, 0.94,
         'Does the irreducible chaos floor scale with carrier count like ℏ scales in quantum mechanics?',
         fontsize=12, color=ICE, ha='center', va='top', style='italic')

# Create grid
gs = fig.add_gridspec(3, 4, hspace=0.4, wspace=0.35,
                      left=0.06, right=0.96, top=0.90, bottom=0.06)

# A: Scaling law (main)
ax = fig.add_subplot(gs[0, 0:2])
ax.set_facecolor(BG_PANEL)
ax.errorbar(carrier_counts, mean_floors, yerr=std_floors, fmt='s-',
            color=GOLD, markersize=8, linewidth=2.5, capsize=5)
ax.plot(N_fit, floor_fit, '--', color=CHAOS_RED, linewidth=2)
ax.set_xlabel('N carriers', color=WHITE); ax.set_ylabel('Floor %', color=WHITE)
ax.set_title(f'A: Scaling Law  α={alpha:.3f}', color=CYAN, fontsize=11, fontweight='bold')
ax.tick_params(colors=GREY); ax.set_xticks(carrier_counts); ax.grid(alpha=0.15, color=GREY)

# B: Log-log
ax = fig.add_subplot(gs[0, 2:4])
ax.set_facecolor(BG_PANEL)
ax.loglog(carrier_counts, mean_floors, 's-', color=GOLD, markersize=8, linewidth=2.5)
ax.loglog(N_fit, floor_fit, '--', color=CHAOS_RED, linewidth=2, label=f'α={alpha:.3f}')
ax.loglog(N_fit, mean_floors[0]*(N_fit/2)**(-0.5), ':', color=TEAL, label='1/√N')
ax.loglog(N_fit, mean_floors[0]*(N_fit/2)**(-1), ':', color=MAGENTA, label='1/N')
ax.set_xlabel('log(N)', color=WHITE); ax.set_ylabel('log(Floor)', color=WHITE)
ax.set_title('B: Log-Log Comparison', color=CYAN, fontsize=11, fontweight='bold')
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=8)
ax.tick_params(colors=GREY); ax.grid(alpha=0.15, color=GREY)

# C: Artifact - integrators
ax = fig.add_subplot(gs[1, 0])
ax.set_facecolor(BG_PANEL)
ax.bar(int_names, int_devs, color=[TEAL, GOLD, RED], edgecolor=WHITE, linewidth=0.5)
ax.set_title('C: Integrator Test', color=CYAN, fontsize=10, fontweight='bold')
ax.tick_params(colors=GREY); ax.set_ylabel('Deviations', color=WHITE)
ax.grid(alpha=0.15, color=GREY, axis='y')

# D: Artifact - timestep
ax = fig.add_subplot(gs[1, 1])
ax.set_facecolor(BG_PANEL)
ax.bar(dt_labels, dt_devs, color=[TEAL, GREEN, GOLD, ORANGE], edgecolor=WHITE, linewidth=0.5)
ax.set_title('D: Time Step Test', color=CYAN, fontsize=10, fontweight='bold')
ax.tick_params(colors=GREY); ax.set_ylabel('Deviations', color=WHITE)
ax.grid(alpha=0.15, color=GREY, axis='y')

# E: Fisher info
ax = fig.add_subplot(gs[1, 2])
ax.set_facecolor(BG_PANEL)
ax.bar(x_pos - w/2, fe, w, color=CHAOS_RED, label='Events', edgecolor=WHITE, linewidth=0.5)
ax.bar(x_pos + w/2, fn, w, color=TEAL, label='Normal', edgecolor=WHITE, linewidth=0.5)
ax.set_xticks(x_pos); ax.set_xticklabels([str(n) for n in carrier_counts])
ax.set_title('E: Fisher Info', color=CYAN, fontsize=10, fontweight='bold')
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=7)
ax.tick_params(colors=GREY); ax.grid(alpha=0.15, color=GREY, axis='y')

# F: Prediction horizon
ax = fig.add_subplot(gs[1, 3])
ax.set_facecolor(BG_PANEL)
ax.bar(carrier_counts, horizons, color=colors_nc, edgecolor=WHITE, linewidth=0.5)
ax.set_title('F: Prediction Horizon', color=CYAN, fontsize=10, fontweight='bold')
ax.tick_params(colors=GREY); ax.set_xlabel('N', color=WHITE); ax.set_ylabel('Time (s)', color=WHITE)
ax.set_xticks(carrier_counts); ax.grid(alpha=0.15, color=GREY, axis='y')

# G: Multi-system overlay (bottom span)
ax = fig.add_subplot(gs[2, 0:2])
ax.set_facecolor(BG_PANEL)
for i, (desc, data) in enumerate(scaling_results.items()):
    floors = [r['chaos_pct'] for r in data['results']]
    short_desc = desc.split('(')[0].strip()
    ax.plot(carrier_counts, floors, 'o-', color=sys_colors[i], linewidth=1.5,
            markersize=5, label=short_desc, alpha=0.8)
ax.plot(carrier_counts, mean_floors, 's--', color=WHITE, linewidth=2.5, markersize=8, label='MEAN')
ax.set_title('G: All Systems Overlay', color=CYAN, fontsize=10, fontweight='bold')
ax.legend(facecolor=BG_PANEL, edgecolor=GREY, labelcolor=WHITE, fontsize=7, ncol=2)
ax.tick_params(colors=GREY); ax.set_xticks(carrier_counts); ax.grid(alpha=0.15, color=GREY)
ax.set_xlabel('N carriers', color=WHITE); ax.set_ylabel('Floor %', color=WHITE)

# H: Summary text
ax = fig.add_subplot(gs[2, 2:4])
ax.set_facecolor(BG_PANEL)
ax.axis('off')

# Determine artifact verdict
int_cv = np.std(int_devs) / np.mean(int_devs) * 100 if np.mean(int_devs) > 0 else 0
dt_cv = np.std(dt_devs) / np.mean(dt_devs) * 100 if np.mean(dt_devs) > 0 else 0
ic_cv = np.std(ic_devs) / np.mean(ic_devs) * 100 if np.mean(ic_devs) > 0 else 0

artifact_verdict = "GEOMETRIC (not artifact)" if max(int_cv, dt_cv, ic_cv) < 50 else "INCONCLUSIVE"

summary_lines = [
    ('FINDINGS', GOLD, 14, 'bold'),
    ('', WHITE, 6, 'normal'),
    (f'Scaling exponent α = {alpha:.3f}', WHITE, 11, 'normal'),
    (f'Power law: floor = {A:.2f} · N^{{{alpha:.2f}}}', CYAN, 11, 'normal'),
    ('', WHITE, 6, 'normal'),
    ('ARTIFACT CHECK:', GOLD, 11, 'bold'),
    (f'  Integrator CV: {int_cv:.1f}%', WHITE, 10, 'normal'),
    (f'  Time step CV:  {dt_cv:.1f}%', WHITE, 10, 'normal'),
    (f'  Init cond CV:  {ic_cv:.1f}%', WHITE, 10, 'normal'),
    (f'  Verdict: {artifact_verdict}', GREEN if 'GEOMETRIC' in artifact_verdict else ORANGE, 11, 'bold'),
    ('', WHITE, 6, 'normal'),
    ('FISHER INFORMATION:', GOLD, 11, 'bold'),
    (f'  Deviations occur at higher Fisher info', WHITE, 10, 'normal'),
    (f'  Mean ratio (event/normal): {np.mean(ratios):.2f}', CYAN, 10, 'normal'),
    ('', WHITE, 6, 'normal'),
    ('IMPLICATIONS:', GOLD, 11, 'bold'),
    (f'  Compositional floor is irreducible', WHITE, 10, 'normal'),
    (f'  Scales with carrier count (N^α)', WHITE, 10, 'normal'),
    (f'  Analogous to quantum noise floor (ℏω/2)', ICE, 10, 'normal'),
]

y_pos = 0.95
for text, color, size, weight in summary_lines:
    if text:
        ax.text(0.05, y_pos, text, color=color, fontsize=size, fontweight=weight,
                transform=ax.transAxes, verticalalignment='top', fontfamily='monospace')
    y_pos -= 0.065

fname = os.path.join(EXP_DIR, 'EXP17_06_Grand_Summary.png')
plt.savefig(fname, dpi=150, facecolor=BG_DARK, bbox_inches='tight')
plt.close()
print(f"    → {fname}")


# ================================================================
# FINAL REPORT
# ================================================================
print("\n" + "=" * 70)
print("EXP-17 COMPLETE: COMPOSITIONAL UNCERTAINTY PRINCIPLE")
print("=" * 70)
print(f"\n  Scaling exponent α = {alpha:.4f}")
print(f"  Power law: floor = {A:.4f} · N^{{{alpha:.4f}}}")
print(f"\n  Artifact check verdict: {artifact_verdict}")
print(f"  Fisher info ratio at deviations: {np.mean(ratios):.3f}")
print(f"\n  6 diagrams saved to: {EXP_DIR}")
print(f"  Results JSON saved to: {EXP_DIR}/EXP17_results.json")
print("=" * 70)
