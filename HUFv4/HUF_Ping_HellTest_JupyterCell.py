# ============================================================
# HUF PING HELL TEST — PASTE THIS ENTIRE CELL INTO JUPYTER
# ============================================================
# Higgins Unity Framework — Network Monitoring Stress Test
# Copy everything below into a single Jupyter cell and run.
# No file dependencies. No __file__. No Agg backend.
# Works in JupyterLab, Jupyter Notebook, Google Colab.
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import time
import os
from typing import List, Dict, Tuple

import warnings
warnings.filterwarnings('ignore')

# Inline display for Jupyter
try:
    get_ipython().run_line_magic('matplotlib', 'inline')
except:
    pass

# ============================================================
# OUTPUT DIRECTORY (saves figures alongside notebook)
# ============================================================
FIG_DIR = os.path.join(os.getcwd(), "helltest_figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ============================================================
# HUF CORE — RATIO STATE MONITORING ENGINE
# ============================================================

# HUF color palette
HUF_BLUE   = '#1F3864'
HUF_TEAL   = '#2E75B6'
HUF_GREEN  = '#548235'
HUF_RED    = '#C00000'
HUF_GOLD   = '#BF8F00'
HUF_ORANGE = '#ED7D31'
HUF_GREY   = '#808080'
BG_LIGHT   = '#F2F2F2'


def compute_rho(magnitudes):
    """PreParser: raw magnitudes -> ratio state on simplex"""
    total = np.sum(magnitudes)
    if total == 0:
        return np.ones(len(magnitudes)) / len(magnitudes)
    return magnitudes / total


def compute_mdg(rho_current, rho_reference, K):
    """Monitoring Drift Gain (dB): MDG = 20*log10(drift_bps / K)"""
    drift = np.mean(np.abs(rho_current - rho_reference))
    drift_bps = drift * 10000
    if drift_bps < 1e-10:
        return 0.0
    return 20 * np.log10(max(drift_bps / K, 1e-10))


def compute_ratio_velocity(rho_history, window=5):
    """dHUF/dt — Temporal Sieve (Gemini AM2)"""
    if len(rho_history) < 2:
        return np.array([0.0])
    velocities = []
    for i in range(1, len(rho_history)):
        delta = rho_history[i] - rho_history[i-1]
        v = np.sqrt(np.sum(delta**2))
        velocities.append(v)
    v_arr = np.array(velocities)
    if len(v_arr) >= window:
        kernel = np.ones(window) / window
        v_smooth = np.convolve(v_arr, kernel, mode='same')
        return v_smooth
    return v_arr


def detect_deceptive_drift(rho_history, threshold_bps=50.0, window=20):
    """FM-3/FM-5 Deceptive Drift detector"""
    alerts = []
    if len(rho_history) < window + 1:
        return alerts
    for i in range(window, len(rho_history)):
        ref = np.mean(rho_history[i-window:i], axis=0)
        drift_bps = np.mean(np.abs(rho_history[i] - ref)) * 10000
        if drift_bps > threshold_bps:
            alerts.append(i)
    return alerts


def mc4_gate(rho, threshold=0.005):
    """MC-4 Gating: drop elements below threshold, re-normalize"""
    gated = []
    rho_gated = rho.copy()
    for i in range(len(rho)):
        if rho[i] < threshold:
            gated.append(i)
            rho_gated[i] = 0.0
    total = np.sum(rho_gated)
    if total > 0:
        rho_gated = rho_gated / total
    return rho_gated, gated


# ============================================================
# PING SIMULATORS
# ============================================================

def simulate_simple_ping(n_pings=100, base_loss_rate=0.02, seed=42):
    """Level 1: Simple ping, K=2 (success/lost)"""
    rng = np.random.default_rng(seed)
    results = np.array([1 if rng.random() > base_loss_rate else 0 for _ in range(n_pings)])
    return {'results': results, 'n_pings': n_pings, 'loss_rate': base_loss_rate, 'name': 'Simple Ping'}


def simulate_realistic_network(n_pings=1000, base_loss=0.02, burst_prob=0.05,
                                burst_length=10, burst_loss=0.50,
                                congestion_period=200, congestion_amp=0.15, seed=42):
    """Level 2: Jitter, burst loss, congestion waves"""
    rng = np.random.default_rng(seed)
    results = []
    rtts = []
    in_burst = 0
    for i in range(n_pings):
        congestion = congestion_amp * np.sin(2 * np.pi * i / congestion_period)
        effective_loss = max(0, base_loss + congestion)
        if in_burst > 0:
            effective_loss = burst_loss
            in_burst -= 1
        elif rng.random() < burst_prob:
            in_burst = burst_length
            effective_loss = burst_loss
        success = 1 if rng.random() > effective_loss else 0
        results.append(success)
        base_rtt = 25.0
        jitter = rng.normal(0, 5.0)
        rtt = max(1.0, base_rtt + jitter + (congestion * 100))
        rtts.append(rtt if success else 0)
    return {'results': np.array(results), 'rtts': np.array(rtts), 'n_pings': n_pings, 'name': 'Realistic Network'}


def simulate_volume_test(n_pings=100000, drift_onset=40000, drift_rate=0.001, max_loss=0.60, seed=42):
    """Level 3: 100K+ pings, slow deceptive degradation"""
    rng = np.random.default_rng(seed)
    results = []
    for i in range(n_pings):
        if i < drift_onset:
            loss_rate = 0.02
        else:
            progress = (i - drift_onset) / (n_pings - drift_onset)
            loss_rate = 0.02 + (max_loss - 0.02) * progress
        results.append(1 if rng.random() > loss_rate else 0)
    return {'results': np.array(results), 'n_pings': n_pings, 'drift_onset': drift_onset,
            'name': f'Volume Test ({n_pings//1000}K pings)'}


def simulate_multi_stream(n_streams=8, n_pings=5000, correlation=0.3, seed=42):
    """Level 4: Multi-stream parallel, correlated failures"""
    rng = np.random.default_rng(seed)
    streams = {}
    weather = rng.normal(0, 0.05, n_pings)
    endpoints = [
        ('8.8.8.8', 0.02, 'Google DNS'), ('1.1.1.1', 0.01, 'Cloudflare'),
        ('208.67.222.222', 0.03, 'OpenDNS'), ('9.9.9.9', 0.02, 'Quad9'),
        ('4.2.2.1', 0.04, 'Level3'), ('64.6.64.6', 0.03, 'Verisign'),
        ('185.228.168.9', 0.05, 'CleanBrowsing'), ('76.76.2.0', 0.02, 'ControlD'),
    ][:n_streams]
    for ip, base_loss, name in endpoints:
        ind_noise = rng.normal(0, 0.03, n_pings)
        results = []
        for i in range(n_pings):
            eff = np.clip(base_loss + correlation * weather[i] + (1-correlation) * ind_noise[i], 0, 0.95)
            results.append(1 if rng.random() > eff else 0)
        streams[name] = {'ip': ip, 'results': np.array(results), 'base_loss': base_loss}
    return {'streams': streams, 'n_pings': n_pings, 'n_streams': len(endpoints),
            'correlation': correlation, 'name': f'Multi-Stream ({len(endpoints)} endpoints)'}


def simulate_hell_test(n_pings=50000, n_streams=12, seed=42):
    """Level 5: THE HUF HELL TEST — all failure modes simultaneously"""
    rng = np.random.default_rng(seed)
    events = {
        'slow_drift_start': 5000, 'first_burst_storm': 8000,
        'deceptive_drift_start': 12000, 'concentration_trap': 18000,
        'false_recovery': 22000, 'adversarial_injection': 26000,
        'synchronized_catastrophe': 32000, 'ratio_inversion': 36000,
        'undeclared_regime_change': 40000, 'ground_state_departure': 44000,
        'final_cascade': 47000,
    }
    stream_names = ['Primary-A', 'Primary-B', 'Secondary-A', 'Secondary-B',
                    'Backup-1', 'Backup-2', 'CDN-East', 'CDN-West',
                    'Monitor-1', 'Monitor-2', 'Health-Check', 'Canary'][:n_streams]
    base_losses = np.array([0.01, 0.01, 0.02, 0.02, 0.03, 0.03,
                            0.02, 0.02, 0.01, 0.01, 0.005, 0.005])[:n_streams]
    all_streams = {name: np.zeros(n_pings) for name in stream_names}

    for t in range(n_pings):
        for s_idx, s_name in enumerate(stream_names):
            loss = base_losses[s_idx]
            # FM-1: Slow baseline drift
            if t >= events['slow_drift_start']:
                progress = min(1.0, (t - events['slow_drift_start']) / 30000)
                loss += 0.08 * progress * (1 + 0.3 * s_idx / n_streams)
            # Burst storms
            if events['first_burst_storm'] <= t < events['first_burst_storm'] + 50:
                loss = 0.80
            if 15000 <= t < 15050:
                loss = 0.85
            # FM-3: Deceptive Drift
            if events['deceptive_drift_start'] <= t < events['concentration_trap']:
                if s_idx < n_streams // 2:
                    loss -= 0.015
                else:
                    loss += 0.025
            # FM-2: Concentration Trap
            if events['concentration_trap'] <= t < events['false_recovery']:
                if s_idx == 0:
                    loss = 0.001
                else:
                    loss += 0.10
            # False recovery
            if events['false_recovery'] <= t < events['adversarial_injection']:
                loss = base_losses[s_idx] * 0.5
            # Adversarial injection
            if events['adversarial_injection'] <= t < events['synchronized_catastrophe']:
                if s_name in ['Health-Check', 'Canary']:
                    loss = 0.001
                else:
                    loss += 0.05 * ((t - events['adversarial_injection']) / 6000)
            # Synchronized catastrophe
            if events['synchronized_catastrophe'] <= t < events['synchronized_catastrophe'] + 500:
                loss = 0.70 + rng.random() * 0.25
            # FM-4: Ratio inversion
            if events['ratio_inversion'] <= t < events['undeclared_regime_change']:
                if s_idx % 3 == 0:
                    loss = 0.60 + rng.random() * 0.15
            # FM-5: Undeclared regime change
            if t >= events['undeclared_regime_change']:
                new_base = base_losses[(s_idx + 3) % n_streams]
                loss = new_base + 0.05
            # FM-6: Ground state departure
            if t >= events['ground_state_departure']:
                oscillation = 0.15 * np.sin(2 * np.pi * t / 200 + s_idx * np.pi / 6)
                loss += abs(oscillation)
            # Final cascade
            if t >= events['final_cascade']:
                cascade_progress = (t - events['final_cascade']) / (n_pings - events['final_cascade'])
                loss += 0.50 * cascade_progress
            loss = np.clip(loss, 0.0, 0.99)
            all_streams[s_name][t] = 1 if rng.random() > loss else 0

    return {'streams': all_streams, 'n_pings': n_pings, 'n_streams': n_streams,
            'events': events, 'stream_names': stream_names, 'name': 'HUF HELL TEST'}


# ============================================================
# HUF ANALYSIS ENGINE
# ============================================================

def windowed_analysis(results, window_size=50, K=2):
    """Sliding window HUF analysis on a single stream"""
    n = len(results)
    n_windows = n - window_size + 1
    rho_history = np.zeros((n_windows, K))
    mdg_history = np.zeros(n_windows)
    cdn_history = np.zeros(n_windows)
    first_window = results[:window_size]
    successes = np.sum(first_window)
    rho_ref = compute_rho(np.array([successes, window_size - successes], dtype=float))
    cdn = 0.0
    for i in range(n_windows):
        window = results[i:i+window_size]
        successes = np.sum(window)
        rho = compute_rho(np.array([successes, window_size - successes], dtype=float))
        rho_history[i] = rho
        mdg = compute_mdg(rho, rho_ref, K)
        mdg_history[i] = mdg
        cdn += mdg
        cdn_history[i] = cdn
    ratio_velocity = compute_ratio_velocity(rho_history)
    drift_alerts = detect_deceptive_drift(rho_history)
    return {'rho_history': rho_history, 'mdg_history': mdg_history, 'cdn_history': cdn_history,
            'ratio_velocity': ratio_velocity, 'drift_alerts': drift_alerts,
            'rho_ref': rho_ref, 'window_size': window_size}


def multi_stream_analysis(streams, window_size=50):
    """Multi-stream HUF portfolio analysis"""
    stream_names = list(streams.keys())
    n_streams = len(stream_names)
    first_key = stream_names[0]
    if isinstance(streams[first_key], dict):
        n_pings = len(streams[first_key]['results'])
    else:
        n_pings = len(streams[first_key])
    n_windows = n_pings - window_size + 1
    stream_rates = np.zeros((n_windows, n_streams))
    for s_idx, name in enumerate(stream_names):
        res = streams[name]['results'] if isinstance(streams[name], dict) else streams[name]
        for i in range(n_windows):
            stream_rates[i, s_idx] = np.mean(res[i:i+window_size])
    rho_portfolio = np.zeros((n_windows, n_streams))
    for i in range(n_windows):
        total = np.sum(stream_rates[i])
        if total > 0:
            rho_portfolio[i] = stream_rates[i] / total
        else:
            rho_portfolio[i] = np.ones(n_streams) / n_streams
    rho_ref = rho_portfolio[0].copy()
    mdg_history = np.zeros(n_windows)
    for i in range(n_windows):
        mdg_history[i] = compute_mdg(rho_portfolio[i], rho_ref, n_streams)
    ratio_velocity = compute_ratio_velocity(rho_portfolio)
    per_stream = {}
    for name in stream_names:
        res = streams[name]['results'] if isinstance(streams[name], dict) else streams[name]
        per_stream[name] = windowed_analysis(res, window_size)
    return {'stream_rates': stream_rates, 'rho_portfolio': rho_portfolio,
            'mdg_history': mdg_history, 'ratio_velocity': ratio_velocity,
            'per_stream': per_stream, 'rho_ref': rho_ref, 'stream_names': stream_names}


# ============================================================
# VISUALIZATION (all use plt.show() for Jupyter inline display)
# ============================================================

def plot_simple_demo(sim_data, analysis):
    """Level 1: Simple ping visualization"""
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), facecolor='white')
    fig.suptitle('HUF PING DEMO - Level 1: Simple Ratio Monitoring',
                 fontsize=16, fontweight='bold', color=HUF_BLUE, y=0.98)
    ax = axes[0]
    ax.scatter(range(len(sim_data['results'])), sim_data['results'],
               c=[HUF_GREEN if r else HUF_RED for r in sim_data['results']], s=10, alpha=0.7)
    ax.set_ylabel('Result'); ax.set_yticks([0, 1]); ax.set_yticklabels(['LOST', 'SUCCESS'])
    ax.set_title('Raw Ping Results', fontsize=11, color=HUF_BLUE)
    ax = axes[1]
    rho_s = analysis['rho_history'][:, 0]
    ax.plot(rho_s, color=HUF_TEAL, linewidth=1.5, label='rho_success')
    ax.axhline(y=0.5, color=HUF_RED, linestyle='--', alpha=0.5, label='50/50 (critical)')
    ax.axhline(y=analysis['rho_ref'][0], color=HUF_GREY, linestyle=':', alpha=0.5, label='Reference')
    ax.set_ylabel('rho_success')
    ax.set_title('Ratio State (Unity: rho_success + rho_lost = 1.0)', fontsize=11, color=HUF_BLUE)
    ax.legend(loc='lower left', fontsize=9)
    ax = axes[2]
    ax.plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=1.0)
    ax.axhline(y=0, color=HUF_GREY, linestyle='-', alpha=0.3)
    ax.set_ylabel('MDG (dB)')
    ax.set_title('Monitoring Drift Gain', fontsize=11, color=HUF_BLUE)
    ax = axes[3]
    ax.plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=1.0, alpha=0.8)
    ax.set_ylabel('|dHUF/dt|'); ax.set_xlabel('Window Index')
    ax.set_title('Ratio Velocity (Temporal Sieve)', fontsize=11, color=HUF_BLUE)
    for a in axes:
        a.set_facecolor(BG_LIGHT); a.grid(True, alpha=0.3)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(FIG_DIR, "level1_simple_ping.png"), dpi=150, bbox_inches='tight')
    plt.show()


def plot_realistic(sim_data, analysis):
    """Level 2: Realistic network"""
    fig, axes = plt.subplots(5, 1, figsize=(16, 16), facecolor='white')
    fig.suptitle('HUF PING - Level 2: Realistic Network', fontsize=16, fontweight='bold', color=HUF_BLUE, y=0.98)
    rho_s = analysis['rho_history'][:, 0]
    axes[0].plot(rho_s, color=HUF_TEAL, linewidth=1.0)
    axes[0].axhline(y=0.5, color=HUF_RED, linestyle='--', alpha=0.5)
    axes[0].set_ylabel('rho_success'); axes[0].set_title('Ratio State with Burst Events', fontsize=11, color=HUF_BLUE)
    if 'rtts' in sim_data:
        rtts = sim_data['rtts']; valid = rtts > 0
        axes[1].scatter(np.where(valid)[0], rtts[valid], s=1, alpha=0.3, color=HUF_TEAL)
        axes[1].set_ylabel('RTT (ms)'); axes[1].set_title('Round-Trip Time', fontsize=11, color=HUF_BLUE)
    axes[2].plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=1.0)
    axes[2].set_ylabel('MDG (dB)'); axes[2].set_title('MDG - burst spikes, congestion waves', fontsize=11, color=HUF_BLUE)
    axes[3].plot(analysis['cdn_history'], color=HUF_GREEN, linewidth=1.5)
    axes[3].set_ylabel('CDN (cumulative dB)'); axes[3].set_title('Cumulative Drift Narrative', fontsize=11, color=HUF_BLUE)
    axes[4].plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=1.0)
    axes[4].set_ylabel('|dHUF/dt|'); axes[4].set_xlabel('Window Index')
    axes[4].set_title('Temporal Sieve', fontsize=11, color=HUF_BLUE)
    for a in axes:
        a.set_facecolor(BG_LIGHT); a.grid(True, alpha=0.3)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(FIG_DIR, "level2_realistic.png"), dpi=150, bbox_inches='tight')
    plt.show()


def plot_volume(sim_data, analysis):
    """Level 3: Volume test"""
    fig, axes = plt.subplots(4, 1, figsize=(18, 14), facecolor='white')
    fig.suptitle(f'HUF PING - Level 3: {sim_data["name"]}', fontsize=16, fontweight='bold', color=HUF_BLUE, y=0.98)
    rho_s = analysis['rho_history'][:, 0]
    axes[0].plot(rho_s, color=HUF_TEAL, linewidth=0.5, alpha=0.7)
    if 'drift_onset' in sim_data:
        axes[0].axvline(x=sim_data['drift_onset'], color=HUF_RED, linewidth=2, linestyle='--',
                        label=f'Drift onset (t={sim_data["drift_onset"]})')
    axes[0].set_ylabel('rho_success'); axes[0].set_title('Ratio State - slow drift', fontsize=11, color=HUF_BLUE)
    axes[0].legend()
    axes[1].plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=0.5, alpha=0.8)
    if 'drift_onset' in sim_data:
        axes[1].axvline(x=sim_data['drift_onset'], color=HUF_RED, linewidth=2, linestyle='--')
    axes[1].set_ylabel('MDG (dB)'); axes[1].set_title('MDG - continuous rise after onset', fontsize=11, color=HUF_BLUE)
    axes[2].plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=0.5, alpha=0.8)
    if 'drift_onset' in sim_data:
        axes[2].axvline(x=sim_data['drift_onset'], color=HUF_RED, linewidth=2, linestyle='--')
    axes[2].set_ylabel('|dHUF/dt|'); axes[2].set_title('Temporal Sieve', fontsize=11, color=HUF_BLUE)
    alerts = analysis['drift_alerts']
    if alerts:
        alert_density = np.zeros(len(rho_s))
        bin_size = max(1, len(rho_s) // 200)
        for a in alerts:
            if a < len(alert_density):
                idx = min(a // bin_size, len(alert_density) // bin_size - 1)
                start = idx * bin_size
                end = min(start + bin_size, len(alert_density))
                alert_density[start:end] += 1
        axes[3].fill_between(range(len(alert_density)), alert_density, color=HUF_RED, alpha=0.5)
        if 'drift_onset' in sim_data:
            axes[3].axvline(x=sim_data['drift_onset'], color=HUF_RED, linewidth=2, linestyle='--')
    axes[3].set_ylabel('Alert Density'); axes[3].set_xlabel('Window Index')
    axes[3].set_title('Deceptive Drift Alerts', fontsize=11, color=HUF_BLUE)
    for a in axes:
        a.set_facecolor(BG_LIGHT); a.grid(True, alpha=0.3); a.set_xlim(0, len(rho_s))
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(FIG_DIR, "level3_volume_100K.png"), dpi=150, bbox_inches='tight')
    plt.show()


def plot_multi_stream(sim_data, analysis):
    """Level 4: Multi-stream"""
    n_str = len(analysis['stream_names'])
    fig = plt.figure(figsize=(18, 18), facecolor='white')
    gs = GridSpec(4, 1, figure=fig, hspace=0.35)
    fig.suptitle(f'HUF PING - Level 4: {sim_data["name"]}', fontsize=16, fontweight='bold', color=HUF_BLUE, y=0.98)
    colors = plt.cm.tab20(np.linspace(0, 1, n_str))
    ax1 = fig.add_subplot(gs[0])
    for s_idx, name in enumerate(analysis['stream_names']):
        ax1.plot(analysis['stream_rates'][:, s_idx], color=colors[s_idx], linewidth=0.8, alpha=0.7, label=name)
    ax1.set_ylabel('Success Rate'); ax1.set_title('Per-Stream Success Rates', fontsize=11, color=HUF_BLUE)
    ax1.legend(loc='lower left', fontsize=7, ncol=4)
    ax2 = fig.add_subplot(gs[1])
    rho = analysis['rho_portfolio']
    ax2.stackplot(range(len(rho)), *[rho[:, i] for i in range(n_str)], colors=colors, alpha=0.8)
    ax2.set_ylabel('rho_i'); ax2.set_title('Ratio Portfolio (sum = 1.0)', fontsize=11, color=HUF_BLUE)
    ax2.set_ylim(0, 1)
    ax3 = fig.add_subplot(gs[2])
    ax3.plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=1.0)
    ax3.set_ylabel('Portfolio MDG (dB)'); ax3.set_title('Portfolio MDG', fontsize=11, color=HUF_BLUE)
    ax4 = fig.add_subplot(gs[3])
    ax4.plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=1.0)
    ax4.set_ylabel('|dHUF/dt|'); ax4.set_xlabel('Window Index')
    ax4.set_title('Portfolio Temporal Sieve', fontsize=11, color=HUF_BLUE)
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_facecolor(BG_LIGHT); ax.grid(True, alpha=0.3)
    plt.savefig(os.path.join(FIG_DIR, "level4_multi_stream.png"), dpi=150, bbox_inches='tight')
    plt.show()


def plot_hell_test(sim_data, analysis):
    """Level 5: THE HUF HELL TEST"""
    n_str = len(analysis['stream_names'])
    events = sim_data['events']
    fig = plt.figure(figsize=(22, 28), facecolor='white')
    gs = GridSpec(7, 1, figure=fig, hspace=0.4)
    fig.suptitle('HUF HELL TEST - All Failure Modes Simultaneously',
                 fontsize=20, fontweight='bold', color=HUF_RED, y=0.99)
    colors = plt.cm.tab20(np.linspace(0, 1, n_str))

    def mark_events(ax):
        for _, t_val in events.items():
            ax.axvline(x=t_val, color=HUF_GREY, alpha=0.3, linewidth=0.5, linestyle='--')

    ax1 = fig.add_subplot(gs[0])
    for s_idx, name in enumerate(analysis['stream_names']):
        ax1.plot(analysis['stream_rates'][:, s_idx], color=colors[s_idx], linewidth=0.5, alpha=0.6)
    ax1.set_ylabel('Success Rate'); ax1.set_title('Per-Stream Success Rates (12 Endpoints)', fontsize=12, color=HUF_BLUE)
    mark_events(ax1)

    ax2 = fig.add_subplot(gs[1])
    rho = analysis['rho_portfolio']
    ax2.stackplot(range(len(rho)), *[rho[:, i] for i in range(n_str)], colors=colors, alpha=0.8)
    ax2.set_ylabel('rho_i'); ax2.set_ylim(0, 1)
    ax2.set_title('Ratio Portfolio - watch for concentration/redistribution', fontsize=12, color=HUF_BLUE)
    mark_events(ax2)

    ax3 = fig.add_subplot(gs[2])
    max_share = np.max(rho, axis=1)
    ax3.plot(max_share, color='#800080', linewidth=1.0)
    ax3.axhline(y=1.0/n_str, color=HUF_GREY, linestyle=':', label=f'Uniform ({1.0/n_str:.3f})')
    ax3.axhline(y=0.5, color=HUF_RED, linestyle='--', alpha=0.5, label='Domination threshold')
    ax3.set_ylabel('max(rho_i)'); ax3.set_title('Concentration Trap Detector', fontsize=12, color=HUF_BLUE)
    ax3.legend(fontsize=9); mark_events(ax3)

    ax4 = fig.add_subplot(gs[3])
    ax4.plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=0.8)
    ax4.axhline(y=0, color=HUF_GREY, linewidth=0.5)
    ax4.set_ylabel('MDG (dB)'); ax4.set_title('Portfolio MDG', fontsize=12, color=HUF_BLUE)
    mark_events(ax4)

    ax5 = fig.add_subplot(gs[4])
    ax5.plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=0.8)
    ax5.set_ylabel('|dHUF/dt|')
    ax5.set_title('TEMPORAL SIEVE - detects structural change invisible to throughput', fontsize=12, color=HUF_RED)
    mark_events(ax5)

    ax6 = fig.add_subplot(gs[5])
    total_rate = np.mean(analysis['stream_rates'], axis=1)
    ax6.plot(total_rate, color=HUF_GREY, linewidth=1.0, label='Avg success rate')
    ax6.axhline(y=0.5, color=HUF_RED, linestyle='--', alpha=0.5)
    ax6.set_ylabel('Avg Success')
    ax6.set_title('TRADITIONAL MONITOR - misses internal redistribution', fontsize=12, color=HUF_GREY)
    ax6.legend(fontsize=9); mark_events(ax6)

    ax7 = fig.add_subplot(gs[6])
    mdg_norm = np.abs(analysis['mdg_history'])
    mx = np.max(mdg_norm) if np.max(mdg_norm) > 0 else 1
    mdg_norm = mdg_norm / mx
    total_drift = np.abs(total_rate - total_rate[0])
    td_mx = np.max(total_drift) if np.max(total_drift) > 0 else 1
    total_drift_norm = total_drift / td_mx
    ax7.fill_between(range(len(mdg_norm)), mdg_norm, alpha=0.4, color=HUF_ORANGE, label='HUF MDG (normalized)')
    ax7.fill_between(range(len(total_drift_norm)), total_drift_norm, alpha=0.4, color=HUF_GREY, label='Traditional')
    ax7.set_ylabel('Normalized'); ax7.set_xlabel('Window Index')
    ax7.set_title('HUF vs TRADITIONAL', fontsize=12, color=HUF_BLUE)
    ax7.legend(fontsize=9); mark_events(ax7)

    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7]:
        ax.set_facecolor(BG_LIGHT); ax.grid(True, alpha=0.3); ax.set_xlim(0, len(analysis['mdg_history']))
    plt.savefig(os.path.join(FIG_DIR, "level5_HELL_TEST.png"), dpi=150, bbox_inches='tight')
    plt.show()


# ============================================================
# RUN ALL LEVELS
# ============================================================

print("=" * 60)
print("HUF PING HELL TEST")
print("Higgins Unity Framework - Network Stress Test")
print("=" * 60)

all_results = {}
t_start = time.time()

# Level 1
print("\nLevel 1: Simple Ping Demo (100 pings)")
sim1 = simulate_simple_ping(n_pings=100, base_loss_rate=0.05)
ana1 = windowed_analysis(sim1['results'], window_size=20, K=2)
all_results[1] = {'sim': sim1, 'analysis': ana1}
plot_simple_demo(sim1, ana1)

# Level 2
print("\nLevel 2: Realistic Network (1000 pings)")
sim2 = simulate_realistic_network(n_pings=1000)
ana2 = windowed_analysis(sim2['results'], window_size=50, K=2)
all_results[2] = {'sim': sim2, 'analysis': ana2}
plot_realistic(sim2, ana2)

# Level 3
print("\nLevel 3: Volume Test (100K pings, slow deceptive drift)")
sim3 = simulate_volume_test(n_pings=100000, drift_onset=40000)
ana3 = windowed_analysis(sim3['results'], window_size=200, K=2)
all_results[3] = {'sim': sim3, 'analysis': ana3}
plot_volume(sim3, ana3)

# Level 4
print("\nLevel 4: Multi-Stream (8 endpoints)")
sim4 = simulate_multi_stream(n_streams=8, n_pings=5000, correlation=0.3)
ana4 = multi_stream_analysis(sim4['streams'], window_size=50)
all_results[4] = {'sim': sim4, 'analysis': ana4}
plot_multi_stream(sim4, ana4)

# Level 5
print("\nLevel 5: HUF HELL TEST (12 streams x 50K pings)")
sim5 = simulate_hell_test(n_pings=50000, n_streams=12)
ana5 = multi_stream_analysis(sim5['streams'], window_size=100)
all_results[5] = {'sim': sim5, 'analysis': ana5}
plot_hell_test(sim5, ana5)

elapsed = time.time() - t_start

# Summary
print(f"\n{'=' * 60}")
print(f"COMPLETE - {elapsed:.1f}s total")
total_pings = sum(d['sim']['n_pings'] for d in all_results.values())
print(f"Total simulated pings: {total_pings:,}")

# Unity constraint verification
print(f"\nUnity Constraint Verification:")
for level, data in all_results.items():
    ana = data['analysis']
    if 'rho_history' in ana:
        err = np.max(np.abs(np.sum(ana['rho_history'], axis=1) - 1.0))
    else:
        err = np.max(np.abs(np.sum(ana['rho_portfolio'], axis=1) - 1.0))
    status = "PASS" if err < 1e-10 else "FAIL"
    print(f"  Level {level}: max error = {err:.2e}  [{status}]")

# Hell test event detection
if 5 in all_results:
    hell = all_results[5]
    events = hell['sim']['events']
    mdg = hell['analysis']['mdg_history']
    rv = hell['analysis']['ratio_velocity']
    print(f"\nHell Test Event Detection:")
    for event_name, t_val in sorted(events.items(), key=lambda x: x[1]):
        start = max(0, t_val - 50)
        end = min(len(mdg), t_val + 200)
        if start < end:
            local_mdg = np.max(np.abs(mdg[start:end]))
            rv_end = min(len(rv), end)
            local_rv = np.max(rv[start:rv_end]) if start < rv_end else 0
            detected = local_mdg > 10 or local_rv > 0.01
            tag = "DETECTED" if detected else "missed"
            print(f"  t={t_val:6d}  {event_name:35s}  MDG={local_mdg:7.1f}dB  RV={local_rv:.4f}  [{tag}]")

print(f"\nFigures saved to: {FIG_DIR}/")
print(f"{'=' * 60}")
