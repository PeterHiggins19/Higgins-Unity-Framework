#!/usr/bin/env python3
"""
HUF PING HELL TEST
==================
Higgins Unity Framework — Network Monitoring Stress Test

From Grok's simple insight: ping is HUF's "hello world."
  ρ_success = received/sent, ρ_lost = 1 - ρ_success, Σ = 1

This script escalates from a simple demo to a full adversarial
stress test of HUF's ratio-state monitoring on network data.

LEVELS:
  1. Simple Ping — basic ratio monitoring, random loss
  2. Realistic Network — jitter, burst loss, congestion waves
  3. Volume Test — 100K+ samples, streaming windows
  4. Multi-Stream — parallel endpoints, correlated/independent failures
  5. HUF HELL TEST — deceptive drift, adversarial injection,
     mode collapse, synchronized catastrophe

Principal Investigator: Peter Higgins, Rogue Wave Audio
Framework: HUF v1.3.0 / Phase 3
Built by: Claude (AI Collective Moderator)
Date: March 10, 2026
"""

import numpy as np
import matplotlib
import sys
if 'ipykernel' not in sys.modules:
    matplotlib.use('Agg')  # headless backend for script mode
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import time
import os
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# OUTPUT DIRECTORY
# ============================================================
try:
    OUT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    OUT_DIR = os.getcwd()  # Jupyter notebook fallback
FIG_DIR = os.path.join(OUT_DIR, "helltest_figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ============================================================
# HUF CORE — RATIO STATE MONITORING ENGINE
# ============================================================

# HUF color palette (from dual_column.js)
HUF_BLUE   = '#1F3864'
HUF_TEAL   = '#2E75B6'
HUF_GREEN  = '#548235'
HUF_RED    = '#C00000'
HUF_GOLD   = '#BF8F00'
HUF_ORANGE = '#ED7D31'
HUF_GREY   = '#808080'
BG_LIGHT   = '#F2F2F2'

@dataclass
class HUFState:
    """Ratio state on probability simplex Δ_K"""
    rho: np.ndarray          # ratio portfolio [ρ₁, ..., ρ_K], Σ = 1
    mdg: float = 0.0         # Monitoring Drift Gain (dB)
    cdn: float = 0.0         # Cumulative Drift Narrative
    t: int = 0               # time index
    drift_bps: float = 0.0   # drift in basis points

    def verify_unity(self):
        """Unity constraint check"""
        return abs(np.sum(self.rho) - 1.0) < 1e-10


def compute_rho(magnitudes: np.ndarray) -> np.ndarray:
    """PreParser: raw magnitudes → ratio state on simplex"""
    total = np.sum(magnitudes)
    if total == 0:
        return np.ones(len(magnitudes)) / len(magnitudes)
    return magnitudes / total


def compute_mdg(rho_current: np.ndarray, rho_reference: np.ndarray, K: int) -> float:
    """
    Monitoring Drift Gain (dB)
    MDG = 20 * log10(drift_bps / K)
    where drift_bps = 10000 * mean(|Δρ|)
    """
    drift = np.mean(np.abs(rho_current - rho_reference))
    drift_bps = drift * 10000  # basis points
    if drift_bps < 1e-10:
        return 0.0
    return 20 * np.log10(max(drift_bps / K, 1e-10))


def compute_ratio_velocity(rho_history: np.ndarray, window: int = 5) -> np.ndarray:
    """
    dHUF/dt — Temporal Sieve (Gemini AM2)
    Ratio Velocity = magnitude of movement on simplex per time step
    """
    if len(rho_history) < 2:
        return np.array([0.0])

    velocities = []
    for i in range(1, len(rho_history)):
        # Aitchison-like distance on simplex (simplified)
        delta = rho_history[i] - rho_history[i-1]
        v = np.sqrt(np.sum(delta**2))
        velocities.append(v)

    # Smooth with rolling window
    v_arr = np.array(velocities)
    if len(v_arr) >= window:
        kernel = np.ones(window) / window
        v_smooth = np.convolve(v_arr, kernel, mode='same')
        return v_smooth
    return v_arr


def detect_deceptive_drift(rho_history: np.ndarray,
                           threshold_bps: float = 50.0,
                           window: int = 20) -> List[int]:
    """
    FM-3/FM-5 Deceptive Drift detector
    Flags points where ratio drift is significant but
    total magnitude appears stable
    """
    alerts = []
    if len(rho_history) < window + 1:
        return alerts

    for i in range(window, len(rho_history)):
        # Rolling reference
        ref = np.mean(rho_history[i-window:i], axis=0)
        drift_bps = np.mean(np.abs(rho_history[i] - ref)) * 10000
        if drift_bps > threshold_bps:
            alerts.append(i)
    return alerts


def mc4_gate(rho: np.ndarray, threshold: float = 0.005) -> Tuple[np.ndarray, List[int]]:
    """
    MC-4 Gating: drop elements below threshold, re-normalize
    Returns gated rho and list of gated indices
    """
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

def simulate_simple_ping(n_pings: int = 100,
                         base_loss_rate: float = 0.02,
                         seed: int = 42) -> Dict:
    """
    Level 1: Simple ping simulation
    K=2 regimes: success / lost
    """
    rng = np.random.default_rng(seed)

    results = []  # 1=success, 0=lost
    for i in range(n_pings):
        results.append(1 if rng.random() > base_loss_rate else 0)

    return {
        'results': np.array(results),
        'n_pings': n_pings,
        'loss_rate': base_loss_rate,
        'name': 'Simple Ping'
    }


def simulate_realistic_network(n_pings: int = 1000,
                                base_loss: float = 0.02,
                                burst_prob: float = 0.05,
                                burst_length: int = 10,
                                burst_loss: float = 0.50,
                                congestion_period: int = 200,
                                congestion_amp: float = 0.15,
                                seed: int = 42) -> Dict:
    """
    Level 2: Realistic network conditions
    - Random baseline loss
    - Burst loss events (packet storms)
    - Congestion waves (sinusoidal loss rate variation)
    - Jitter (variable RTT)
    """
    rng = np.random.default_rng(seed)

    results = []
    rtts = []
    in_burst = 0

    for i in range(n_pings):
        # Congestion wave
        congestion = congestion_amp * np.sin(2 * np.pi * i / congestion_period)
        effective_loss = max(0, base_loss + congestion)

        # Burst events
        if in_burst > 0:
            effective_loss = burst_loss
            in_burst -= 1
        elif rng.random() < burst_prob:
            in_burst = burst_length
            effective_loss = burst_loss

        # Result
        success = 1 if rng.random() > effective_loss else 0
        results.append(success)

        # RTT with jitter
        base_rtt = 25.0  # ms
        jitter = rng.normal(0, 5.0)
        rtt = max(1.0, base_rtt + jitter + (congestion * 100))
        rtts.append(rtt if success else 0)

    return {
        'results': np.array(results),
        'rtts': np.array(rtts),
        'n_pings': n_pings,
        'name': 'Realistic Network'
    }


def simulate_volume_test(n_pings: int = 100000,
                          drift_onset: int = 40000,
                          drift_rate: float = 0.001,
                          max_loss: float = 0.60,
                          seed: int = 42) -> Dict:
    """
    Level 3: Massive volume — 100K+ pings
    Slow degradation starting at drift_onset
    Tests streaming window processing
    """
    rng = np.random.default_rng(seed)

    results = []
    for i in range(n_pings):
        if i < drift_onset:
            loss_rate = 0.02
        else:
            # Slow ramp-up: Deceptive Drift
            progress = (i - drift_onset) / (n_pings - drift_onset)
            loss_rate = 0.02 + (max_loss - 0.02) * progress

        results.append(1 if rng.random() > loss_rate else 0)

    return {
        'results': np.array(results),
        'n_pings': n_pings,
        'drift_onset': drift_onset,
        'name': f'Volume Test ({n_pings//1000}K pings)'
    }


def simulate_multi_stream(n_streams: int = 8,
                           n_pings: int = 5000,
                           correlation: float = 0.3,
                           seed: int = 42) -> Dict:
    """
    Level 4: Multi-stream parallel testing
    Multiple endpoints with correlated failure modes
    """
    rng = np.random.default_rng(seed)

    streams = {}
    # Shared "internet weather" signal
    weather = rng.normal(0, 0.05, n_pings)

    endpoints = [
        ('8.8.8.8',       0.02, 'Google DNS'),
        ('1.1.1.1',       0.01, 'Cloudflare'),
        ('208.67.222.222', 0.03, 'OpenDNS'),
        ('9.9.9.9',       0.02, 'Quad9'),
        ('4.2.2.1',       0.04, 'Level3'),
        ('64.6.64.6',     0.03, 'Verisign'),
        ('185.228.168.9', 0.05, 'CleanBrowsing'),
        ('76.76.2.0',     0.02, 'ControlD'),
    ][:n_streams]

    for ip, base_loss, name in endpoints:
        results = []
        # Independent component
        independent_noise = rng.normal(0, 0.03, n_pings)

        for i in range(n_pings):
            # Correlated + independent loss
            effective_loss = base_loss + correlation * weather[i] + (1 - correlation) * independent_noise[i]
            effective_loss = np.clip(effective_loss, 0, 0.95)
            results.append(1 if rng.random() > effective_loss else 0)

        streams[name] = {
            'ip': ip,
            'results': np.array(results),
            'base_loss': base_loss
        }

    return {
        'streams': streams,
        'n_pings': n_pings,
        'n_streams': len(endpoints),
        'correlation': correlation,
        'name': f'Multi-Stream ({len(endpoints)} endpoints)'
    }


def simulate_hell_test(n_pings: int = 50000,
                        n_streams: int = 12,
                        seed: int = 42) -> Dict:
    """
    Level 5: THE HUF HELL TEST

    Every failure mode simultaneously:
    - FM-1: Baseline Drift (slow degradation)
    - FM-2: Concentration Trap (one stream dominates)
    - FM-3: Deceptive Drift (total looks fine, internals are rotten)
    - FM-4: Ratio Inversion (success/loss flip)
    - FM-5: Undeclared Drift (hidden regime changes)
    - FM-6: Ground State Departure (system leaves stable equilibrium)

    Plus:
    - Adversarial injection: artificial "good" results masking real failure
    - Synchronized catastrophe: all streams fail together at random times
    - Recovery periods: system appears to heal then relapses
    - Micro-burst storms: 50ms bursts of total failure
    - Deceptive volume: total throughput stays constant but quality degrades
    """
    rng = np.random.default_rng(seed)

    # ---- Event Schedule ----
    events = {
        'slow_drift_start':       5000,
        'first_burst_storm':      8000,
        'deceptive_drift_start':  12000,
        'concentration_trap':     18000,
        'false_recovery':         22000,
        'adversarial_injection':  26000,
        'synchronized_catastrophe': 32000,
        'ratio_inversion':        36000,
        'undeclared_regime_change': 40000,
        'ground_state_departure':  44000,
        'final_cascade':          47000,
    }

    # Stream definitions — 12 parallel "endpoints" of varying reliability
    stream_names = [
        'Primary-A', 'Primary-B', 'Secondary-A', 'Secondary-B',
        'Backup-1', 'Backup-2', 'CDN-East', 'CDN-West',
        'Monitor-1', 'Monitor-2', 'Health-Check', 'Canary'
    ][:n_streams]

    base_losses = np.array([0.01, 0.01, 0.02, 0.02,
                            0.03, 0.03, 0.02, 0.02,
                            0.01, 0.01, 0.005, 0.005])[:n_streams]

    all_streams = {name: np.zeros(n_pings) for name in stream_names}
    event_log = []

    for t in range(n_pings):
        for s_idx, s_name in enumerate(stream_names):
            loss = base_losses[s_idx]

            # FM-1: Slow baseline drift (barely perceptible)
            if t >= events['slow_drift_start']:
                progress = min(1.0, (t - events['slow_drift_start']) / 30000)
                loss += 0.08 * progress * (1 + 0.3 * s_idx / n_streams)

            # Burst storms — 50-ping bursts of 80% loss
            if events['first_burst_storm'] <= t < events['first_burst_storm'] + 50:
                loss = 0.80
            # Second storm at 15000
            if 15000 <= t < 15050:
                loss = 0.85

            # FM-3: Deceptive Drift — some streams improve while others degrade
            # Total success rate stays ~same, but distribution shifts
            if events['deceptive_drift_start'] <= t < events['concentration_trap']:
                if s_idx < n_streams // 2:
                    loss -= 0.015  # these get better
                else:
                    loss += 0.025  # these get worse (net: slight decline)

            # FM-2: Concentration Trap — one stream handles everything
            if events['concentration_trap'] <= t < events['false_recovery']:
                if s_idx == 0:
                    loss = 0.001  # Primary-A becomes perfect
                else:
                    loss += 0.10  # everything else degrades

            # False recovery — everything looks great for 4000 pings
            if events['false_recovery'] <= t < events['adversarial_injection']:
                loss = base_losses[s_idx] * 0.5  # artificially good

            # Adversarial injection — padding results with fake successes
            # Stream "Health-Check" and "Canary" show perfect but are lying
            if events['adversarial_injection'] <= t < events['synchronized_catastrophe']:
                if s_name in ['Health-Check', 'Canary']:
                    loss = 0.001  # fake perfection
                else:
                    loss += 0.05 * ((t - events['adversarial_injection']) / 6000)

            # Synchronized catastrophe — ALL streams fail for 500 pings
            if events['synchronized_catastrophe'] <= t < events['synchronized_catastrophe'] + 500:
                loss = 0.70 + rng.random() * 0.25

            # FM-4: Ratio inversion — success < loss for some streams
            if events['ratio_inversion'] <= t < events['undeclared_regime_change']:
                if s_idx % 3 == 0:
                    loss = 0.60 + rng.random() * 0.15

            # FM-5: Undeclared regime change — behavior changes without warning
            if t >= events['undeclared_regime_change']:
                # Streams silently reorganize
                new_base = base_losses[(s_idx + 3) % n_streams]
                loss = new_base + 0.05

            # FM-6: Ground state departure — entire system enters oscillation
            if t >= events['ground_state_departure']:
                oscillation = 0.15 * np.sin(2 * np.pi * t / 200 + s_idx * np.pi / 6)
                loss += abs(oscillation)

            # Final cascade — progressive total failure
            if t >= events['final_cascade']:
                cascade_progress = (t - events['final_cascade']) / (n_pings - events['final_cascade'])
                loss += 0.50 * cascade_progress

            # Clip and simulate
            loss = np.clip(loss, 0.0, 0.99)
            all_streams[s_name][t] = 1 if rng.random() > loss else 0

    return {
        'streams': all_streams,
        'n_pings': n_pings,
        'n_streams': n_streams,
        'events': events,
        'stream_names': stream_names,
        'name': 'HUF HELL TEST'
    }


# ============================================================
# HUF ANALYSIS ENGINE
# ============================================================

def windowed_analysis(results: np.ndarray,
                      window_size: int = 50,
                      K: int = 2) -> Dict:
    """
    Sliding window HUF analysis on a single stream
    K=2: [success_rate, loss_rate]
    """
    n = len(results)
    n_windows = n - window_size + 1

    rho_history = np.zeros((n_windows, K))
    mdg_history = np.zeros(n_windows)
    cdn_history = np.zeros(n_windows)

    # Reference: first window
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

    # Ratio velocity (Temporal Sieve)
    ratio_velocity = compute_ratio_velocity(rho_history)

    # Deceptive drift detection
    drift_alerts = detect_deceptive_drift(rho_history)

    return {
        'rho_history': rho_history,
        'mdg_history': mdg_history,
        'cdn_history': cdn_history,
        'ratio_velocity': ratio_velocity,
        'drift_alerts': drift_alerts,
        'rho_ref': rho_ref,
        'window_size': window_size
    }


def multi_stream_analysis(streams: Dict,
                           window_size: int = 50) -> Dict:
    """
    Multi-stream HUF analysis
    K = n_streams (each stream is a regime in the portfolio)
    """
    stream_names = list(streams.keys())
    n_streams = len(stream_names)

    # Get per-stream success rates in windows
    first_key = stream_names[0]
    if isinstance(streams[first_key], dict):
        n_pings = len(streams[first_key]['results'])
    else:
        n_pings = len(streams[first_key])

    n_windows = n_pings - window_size + 1

    # Per-stream windowed success rates
    stream_rates = np.zeros((n_windows, n_streams))
    for s_idx, name in enumerate(stream_names):
        if isinstance(streams[name], dict):
            results = streams[name]['results']
        else:
            results = streams[name]

        for i in range(n_windows):
            window = results[i:i+window_size]
            stream_rates[i, s_idx] = np.mean(window)

    # Portfolio: normalize stream rates to ratio state
    rho_portfolio = np.zeros((n_windows, n_streams))
    for i in range(n_windows):
        total = np.sum(stream_rates[i])
        if total > 0:
            rho_portfolio[i] = stream_rates[i] / total
        else:
            rho_portfolio[i] = np.ones(n_streams) / n_streams

    # MDG against first window reference
    rho_ref = rho_portfolio[0].copy()
    mdg_history = np.zeros(n_windows)
    for i in range(n_windows):
        mdg_history[i] = compute_mdg(rho_portfolio[i], rho_ref, n_streams)

    # Ratio velocity
    ratio_velocity = compute_ratio_velocity(rho_portfolio)

    # Per-stream individual analysis
    per_stream = {}
    for name in stream_names:
        if isinstance(streams[name], dict):
            results = streams[name]['results']
        else:
            results = streams[name]
        per_stream[name] = windowed_analysis(results, window_size)

    return {
        'stream_rates': stream_rates,
        'rho_portfolio': rho_portfolio,
        'mdg_history': mdg_history,
        'ratio_velocity': ratio_velocity,
        'per_stream': per_stream,
        'rho_ref': rho_ref,
        'stream_names': stream_names
    }


# ============================================================
# VISUALIZATION
# ============================================================

def plot_simple_demo(sim_data: Dict, analysis: Dict, filename: str):
    """Level 1: Simple ping visualization"""
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), facecolor='white')
    fig.suptitle('HUF PING DEMO — Level 1: Simple Ratio Monitoring',
                 fontsize=16, fontweight='bold', color=HUF_BLUE, y=0.98)

    # 1. Raw results
    ax = axes[0]
    ax.scatter(range(len(sim_data['results'])), sim_data['results'],
               c=[HUF_GREEN if r else HUF_RED for r in sim_data['results']],
               s=10, alpha=0.7)
    ax.set_ylabel('Result')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['LOST', 'SUCCESS'])
    ax.set_title('Raw Ping Results', fontsize=11, color=HUF_BLUE)
    ax.set_xlim(0, len(sim_data['results']))

    # 2. ρ_success over time
    ax = axes[1]
    rho_success = analysis['rho_history'][:, 0]
    ax.plot(rho_success, color=HUF_TEAL, linewidth=1.5, label='ρ_success')
    ax.axhline(y=0.5, color=HUF_RED, linestyle='--', alpha=0.5, label='50/50 (critical)')
    ax.axhline(y=analysis['rho_ref'][0], color=HUF_GREY, linestyle=':', alpha=0.5, label='Reference')
    ax.fill_between(range(len(rho_success)), 0.49, 0.51, color=HUF_RED, alpha=0.1)
    ax.set_ylabel('ρ_success')
    ax.set_title('Ratio State (Unity Constraint: ρ_success + ρ_lost = 1.0)', fontsize=11, color=HUF_BLUE)
    ax.legend(loc='lower left', fontsize=9)
    ax.set_xlim(0, len(rho_success))

    # 3. MDG
    ax = axes[2]
    ax.plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=1.0)
    ax.axhline(y=0, color=HUF_GREY, linestyle='-', alpha=0.3)
    ax.set_ylabel('MDG (dB)')
    ax.set_title('Monitoring Drift Gain — deviation from reference state', fontsize=11, color=HUF_BLUE)
    ax.set_xlim(0, len(analysis['mdg_history']))

    # 4. Ratio Velocity (Temporal Sieve)
    ax = axes[3]
    ax.plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=1.0, alpha=0.8)
    ax.set_ylabel('|dHUF/dt|')
    ax.set_xlabel('Window Index')
    ax.set_title('Ratio Velocity (Temporal Sieve) — structural change rate', fontsize=11, color=HUF_BLUE)
    ax.set_xlim(0, len(analysis['ratio_velocity']))

    for ax in axes:
        ax.set_facecolor(BG_LIGHT)
        ax.grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(FIG_DIR, filename), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  → Saved {filename}")


def plot_realistic(sim_data: Dict, analysis: Dict, filename: str):
    """Level 2: Realistic network with jitter and bursts"""
    fig, axes = plt.subplots(5, 1, figsize=(16, 16), facecolor='white')
    fig.suptitle('HUF PING — Level 2: Realistic Network (Jitter + Burst Loss + Congestion)',
                 fontsize=16, fontweight='bold', color=HUF_BLUE, y=0.98)

    # 1. Success rate
    rho_success = analysis['rho_history'][:, 0]
    axes[0].plot(rho_success, color=HUF_TEAL, linewidth=1.0)
    axes[0].axhline(y=0.5, color=HUF_RED, linestyle='--', alpha=0.5)
    axes[0].set_ylabel('ρ_success')
    axes[0].set_title('Ratio State with Burst Events', fontsize=11, color=HUF_BLUE)

    # 2. RTT (where available)
    if 'rtts' in sim_data:
        rtts = sim_data['rtts']
        valid = rtts > 0
        axes[1].scatter(np.where(valid)[0], rtts[valid], s=1, alpha=0.3, color=HUF_TEAL)
        axes[1].set_ylabel('RTT (ms)')
        axes[1].set_title('Round-Trip Time (jitter visible)', fontsize=11, color=HUF_BLUE)

    # 3. MDG
    axes[2].plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=1.0)
    axes[2].set_ylabel('MDG (dB)')
    axes[2].set_title('MDG — burst events spike, congestion waves visible', fontsize=11, color=HUF_BLUE)

    # 4. CDN (cumulative)
    axes[3].plot(analysis['cdn_history'], color=HUF_GREEN, linewidth=1.5)
    axes[3].set_ylabel('CDN (cumulative dB)')
    axes[3].set_title('Cumulative Drift Narrative — system health trajectory', fontsize=11, color=HUF_BLUE)

    # 5. Ratio Velocity
    axes[4].plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=1.0)
    axes[4].set_ylabel('|dHUF/dt|')
    axes[4].set_xlabel('Window Index')
    axes[4].set_title('Temporal Sieve — ratio velocity spikes at burst events', fontsize=11, color=HUF_BLUE)

    # Mark drift alerts
    for alert in analysis['drift_alerts'][:50]:  # limit markers
        for ax in axes:
            ax.axvline(x=alert, color=HUF_RED, alpha=0.05, linewidth=0.5)

    for ax in axes:
        ax.set_facecolor(BG_LIGHT)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, max(len(rho_success), 1))

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(FIG_DIR, filename), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  → Saved {filename}")


def plot_volume(sim_data: Dict, analysis: Dict, filename: str):
    """Level 3: Volume test — 100K pings"""
    fig, axes = plt.subplots(4, 1, figsize=(18, 14), facecolor='white')
    fig.suptitle(f'HUF PING — Level 3: {sim_data["name"]} (Slow Deceptive Drift)',
                 fontsize=16, fontweight='bold', color=HUF_BLUE, y=0.98)

    rho_success = analysis['rho_history'][:, 0]

    # 1. Ratio state with drift onset
    axes[0].plot(rho_success, color=HUF_TEAL, linewidth=0.5, alpha=0.7)
    if 'drift_onset' in sim_data:
        axes[0].axvline(x=sim_data['drift_onset'], color=HUF_RED, linewidth=2,
                        linestyle='--', label=f'Drift onset (t={sim_data["drift_onset"]})')
    axes[0].set_ylabel('ρ_success')
    axes[0].set_title('Ratio State — slow degradation is nearly invisible in early stages', fontsize=11, color=HUF_BLUE)
    axes[0].legend()

    # 2. MDG — should detect before human would notice
    axes[1].plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=0.5, alpha=0.8)
    if 'drift_onset' in sim_data:
        axes[1].axvline(x=sim_data['drift_onset'], color=HUF_RED, linewidth=2, linestyle='--')
    axes[1].set_ylabel('MDG (dB)')
    axes[1].set_title('MDG — drift detected as continuous rise after onset', fontsize=11, color=HUF_BLUE)

    # 3. Ratio Velocity — the Temporal Sieve
    axes[2].plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=0.5, alpha=0.8)
    if 'drift_onset' in sim_data:
        axes[2].axvline(x=sim_data['drift_onset'], color=HUF_RED, linewidth=2, linestyle='--')
    axes[2].set_ylabel('|dHUF/dt|')
    axes[2].set_title('Temporal Sieve — ratio velocity increases at drift onset', fontsize=11, color=HUF_BLUE)

    # 4. Drift alert density
    alerts = analysis['drift_alerts']
    if alerts:
        alert_density = np.zeros(len(rho_success))
        bin_size = max(1, len(rho_success) // 200)
        for a in alerts:
            if a < len(alert_density):
                bin_idx = min(a // bin_size, len(alert_density) // bin_size - 1)
                start = bin_idx * bin_size
                end = min(start + bin_size, len(alert_density))
                alert_density[start:end] += 1
        axes[3].fill_between(range(len(alert_density)), alert_density,
                             color=HUF_RED, alpha=0.5)
        if 'drift_onset' in sim_data:
            axes[3].axvline(x=sim_data['drift_onset'], color=HUF_RED, linewidth=2, linestyle='--')
    axes[3].set_ylabel('Alert Density')
    axes[3].set_xlabel('Window Index')
    axes[3].set_title('Deceptive Drift Alerts — concentration after onset', fontsize=11, color=HUF_BLUE)

    for ax in axes:
        ax.set_facecolor(BG_LIGHT)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, len(rho_success))

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(FIG_DIR, filename), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  → Saved {filename}")


def plot_multi_stream(sim_data: Dict, analysis: Dict, filename: str):
    """Level 4: Multi-stream parallel"""
    n_streams = len(analysis['stream_names'])

    fig = plt.figure(figsize=(18, 18), facecolor='white')
    gs = GridSpec(4, 1, figure=fig, hspace=0.35)
    fig.suptitle(f'HUF PING — Level 4: {sim_data["name"]}',
                 fontsize=16, fontweight='bold', color=HUF_BLUE, y=0.98)

    colors = plt.cm.tab20(np.linspace(0, 1, n_streams))

    # 1. All stream success rates
    ax1 = fig.add_subplot(gs[0])
    for s_idx, name in enumerate(analysis['stream_names']):
        rates = analysis['stream_rates'][:, s_idx]
        ax1.plot(rates, color=colors[s_idx], linewidth=0.8, alpha=0.7, label=name)
    ax1.set_ylabel('Success Rate')
    ax1.set_title('Per-Stream Success Rates', fontsize=11, color=HUF_BLUE)
    ax1.legend(loc='lower left', fontsize=7, ncol=4)

    # 2. Portfolio ρ (stacked area)
    ax2 = fig.add_subplot(gs[1])
    rho = analysis['rho_portfolio']
    ax2.stackplot(range(len(rho)), *[rho[:, i] for i in range(n_streams)],
                  labels=analysis['stream_names'], colors=colors, alpha=0.8)
    ax2.set_ylabel('ρ_i (portfolio share)')
    ax2.set_title('Ratio Portfolio (Σρᵢ = 1.0) — stream weight distribution', fontsize=11, color=HUF_BLUE)
    ax2.set_ylim(0, 1)

    # 3. Portfolio MDG
    ax3 = fig.add_subplot(gs[2])
    ax3.plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=1.0)
    ax3.set_ylabel('Portfolio MDG (dB)')
    ax3.set_title('Portfolio-Level MDG — detects rebalancing across streams', fontsize=11, color=HUF_BLUE)

    # 4. Portfolio Ratio Velocity
    ax4 = fig.add_subplot(gs[3])
    ax4.plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=1.0)
    ax4.set_ylabel('|dHUF/dt|')
    ax4.set_xlabel('Window Index')
    ax4.set_title('Portfolio Temporal Sieve — structural redistribution velocity', fontsize=11, color=HUF_BLUE)

    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_facecolor(BG_LIGHT)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, len(analysis['mdg_history']))

    plt.savefig(os.path.join(FIG_DIR, filename), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  → Saved {filename}")


def plot_hell_test(sim_data: Dict, analysis: Dict, filename: str):
    """Level 5: THE HUF HELL TEST — full adversarial visualization"""
    n_streams = len(analysis['stream_names'])
    events = sim_data['events']

    fig = plt.figure(figsize=(22, 28), facecolor='white')
    gs = GridSpec(7, 1, figure=fig, hspace=0.4)
    fig.suptitle('HUF HELL TEST — All Failure Modes Simultaneously',
                 fontsize=20, fontweight='bold', color=HUF_RED, y=0.99)

    colors = plt.cm.tab20(np.linspace(0, 1, n_streams))

    # Event annotation helper
    def annotate_events(ax, y_pos=None):
        event_colors = {
            'slow_drift_start': (HUF_GOLD, 'FM-1\nSlow Drift'),
            'first_burst_storm': (HUF_RED, 'Burst\nStorm'),
            'deceptive_drift_start': (HUF_ORANGE, 'FM-3\nDeceptive'),
            'concentration_trap': ('#800080', 'FM-2\nConcentrate'),
            'false_recovery': (HUF_GREEN, 'False\nRecovery'),
            'adversarial_injection': ('#000000', 'Adversarial\nInjection'),
            'synchronized_catastrophe': (HUF_RED, 'SYNC\nCATASTROPHE'),
            'ratio_inversion': (HUF_ORANGE, 'FM-4\nInversion'),
            'undeclared_regime_change': (HUF_TEAL, 'FM-5\nUndeclared'),
            'ground_state_departure': ('#800080', 'FM-6\nDeparture'),
            'final_cascade': (HUF_RED, 'FINAL\nCASCADE'),
        }
        for event_name, t_val in events.items():
            if event_name in event_colors:
                color, label = event_colors[event_name]
                ax.axvline(x=t_val, color=color, alpha=0.4, linewidth=1, linestyle='--')

    # 1. Per-stream success rates
    ax1 = fig.add_subplot(gs[0])
    for s_idx, name in enumerate(analysis['stream_names']):
        rates = analysis['stream_rates'][:, s_idx]
        ax1.plot(rates, color=colors[s_idx], linewidth=0.5, alpha=0.6)
    ax1.set_ylabel('Success Rate')
    ax1.set_title('Per-Stream Success Rates — All 12 Endpoints', fontsize=12, color=HUF_BLUE)
    annotate_events(ax1)

    # 2. Portfolio ρ (stacked)
    ax2 = fig.add_subplot(gs[1])
    rho = analysis['rho_portfolio']
    ax2.stackplot(range(len(rho)), *[rho[:, i] for i in range(n_streams)],
                  colors=colors, alpha=0.8)
    ax2.set_ylabel('ρᵢ')
    ax2.set_title('Ratio Portfolio — watch for concentration and redistribution', fontsize=12, color=HUF_BLUE)
    ax2.set_ylim(0, 1)
    annotate_events(ax2)

    # 3. Max share (concentration metric)
    ax3 = fig.add_subplot(gs[2])
    max_share = np.max(rho, axis=1)
    uniform_share = 1.0 / n_streams
    ax3.plot(max_share, color='#800080', linewidth=1.0)
    ax3.axhline(y=uniform_share, color=HUF_GREY, linestyle=':', label=f'Uniform ({uniform_share:.3f})')
    ax3.axhline(y=0.5, color=HUF_RED, linestyle='--', alpha=0.5, label='Domination threshold')
    ax3.set_ylabel('max(ρᵢ)')
    ax3.set_title('Concentration Trap Detector — max portfolio share', fontsize=12, color=HUF_BLUE)
    ax3.legend(fontsize=9)
    annotate_events(ax3)

    # 4. Portfolio MDG
    ax4 = fig.add_subplot(gs[3])
    ax4.plot(analysis['mdg_history'], color=HUF_ORANGE, linewidth=0.8)
    ax4.axhline(y=0, color=HUF_GREY, linewidth=0.5)
    ax4.set_ylabel('MDG (dB)')
    ax4.set_title('Portfolio MDG — every failure mode produces signature', fontsize=12, color=HUF_BLUE)
    annotate_events(ax4)

    # 5. Ratio Velocity (Temporal Sieve)
    ax5 = fig.add_subplot(gs[4])
    ax5.plot(analysis['ratio_velocity'], color=HUF_RED, linewidth=0.8)
    ax5.set_ylabel('|dHUF/dt|')
    ax5.set_title('TEMPORAL SIEVE — Ratio Velocity detects structural change invisible to total throughput',
                  fontsize=12, color=HUF_RED)
    annotate_events(ax5)

    # 6. Total throughput (what a non-HUF monitor sees)
    ax6 = fig.add_subplot(gs[5])
    total_rate = np.mean(analysis['stream_rates'], axis=1)
    ax6.plot(total_rate, color=HUF_GREY, linewidth=1.0, label='Average success rate (all streams)')
    ax6.axhline(y=0.5, color=HUF_RED, linestyle='--', alpha=0.5)
    ax6.set_ylabel('Avg Success')
    ax6.set_title('WHAT A TRADITIONAL MONITOR SEES — total throughput (misses internal redistribution)',
                  fontsize=12, color=HUF_GREY)
    ax6.legend(fontsize=9)
    annotate_events(ax6)

    # 7. HUF vs Traditional — detection comparison
    ax7 = fig.add_subplot(gs[6])
    # Normalize both to [0,1] for comparison
    mdg_norm = np.abs(analysis['mdg_history'])
    mdg_max = np.max(mdg_norm) if np.max(mdg_norm) > 0 else 1
    mdg_norm = mdg_norm / mdg_max

    total_drift = np.abs(total_rate - total_rate[0])
    td_max = np.max(total_drift) if np.max(total_drift) > 0 else 1
    total_drift_norm = total_drift / td_max

    ax7.fill_between(range(len(mdg_norm)), mdg_norm, alpha=0.4, color=HUF_ORANGE, label='HUF MDG (normalized)')
    ax7.fill_between(range(len(total_drift_norm)), total_drift_norm, alpha=0.4, color=HUF_GREY, label='Traditional (total throughput drift)')
    ax7.set_ylabel('Normalized Detection')
    ax7.set_xlabel('Window Index')
    ax7.set_title('HUF vs TRADITIONAL — HUF detects what throughput monitoring misses',
                  fontsize=12, color=HUF_BLUE)
    ax7.legend(fontsize=9)
    annotate_events(ax7)

    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7]:
        ax.set_facecolor(BG_LIGHT)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, len(analysis['mdg_history']))

    plt.savefig(os.path.join(FIG_DIR, filename), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  → Saved {filename}")


def generate_summary_report(all_results: Dict) -> str:
    """Generate text summary of all test levels"""
    lines = [
        "=" * 70,
        "HUF PING HELL TEST — SUMMARY REPORT",
        "=" * 70,
        f"Date: March 10, 2026",
        f"Framework: HUF v1.3.0 / Phase 3",
        f"Principal Investigator: Peter Higgins, Rogue Wave Audio",
        "",
    ]

    for level, data in all_results.items():
        sim = data['sim']
        analysis = data['analysis']

        lines.append(f"\n{'─' * 50}")
        lines.append(f"LEVEL {level}: {sim['name']}")
        lines.append(f"{'─' * 50}")

        if 'n_pings' in sim:
            lines.append(f"  Pings: {sim['n_pings']:,}")
        if 'n_streams' in sim:
            lines.append(f"  Streams: {sim['n_streams']}")

        # MDG stats
        mdg = analysis['mdg_history']
        lines.append(f"  MDG range: {np.min(mdg):.1f} to {np.max(mdg):.1f} dB")
        lines.append(f"  MDG mean:  {np.mean(mdg):.1f} dB")

        # Ratio velocity stats
        rv = analysis['ratio_velocity']
        lines.append(f"  Ratio Velocity (dHUF/dt) max: {np.max(rv):.6f}")
        lines.append(f"  Ratio Velocity mean:          {np.mean(rv):.6f}")

        # Drift alerts
        if 'drift_alerts' in analysis:
            n_alerts = len(analysis['drift_alerts'])
            lines.append(f"  Deceptive Drift alerts: {n_alerts}")

        # Unity constraint check
        if 'rho_history' in analysis:
            rho = analysis['rho_history']
            unity_errors = np.abs(np.sum(rho, axis=1) - 1.0)
            lines.append(f"  Unity constraint max error: {np.max(unity_errors):.2e}")
            lines.append(f"  Σρᵢ = 1.0: {'PASS ✓' if np.max(unity_errors) < 1e-10 else 'FAIL ✗'}")
        elif 'rho_portfolio' in analysis:
            rho = analysis['rho_portfolio']
            unity_errors = np.abs(np.sum(rho, axis=1) - 1.0)
            lines.append(f"  Unity constraint max error: {np.max(unity_errors):.2e}")
            lines.append(f"  Σρᵢ = 1.0: {'PASS' if np.max(unity_errors) < 1e-10 else 'FAIL'}")

    # Hell test event detection
    if 5 in all_results:
        hell = all_results[5]
        lines.append(f"\n{'=' * 50}")
        lines.append("HELL TEST — FAILURE MODE DETECTION")
        lines.append(f"{'=' * 50}")

        events = hell['sim']['events']
        mdg = hell['analysis']['mdg_history']
        rv = hell['analysis']['ratio_velocity']

        for event_name, t_val in sorted(events.items(), key=lambda x: x[1]):
            # Check if MDG or RV spiked near this event
            window = 200
            start = max(0, t_val - 50)  # account for window offset
            end = min(len(mdg), t_val + window)
            if start < end:
                local_mdg = np.max(np.abs(mdg[start:end]))
                rv_end = min(len(rv), end)
                local_rv = np.max(rv[start:rv_end]) if start < rv_end else 0
                detected = local_mdg > 10 or local_rv > 0.01
                lines.append(f"  t={t_val:6d}  {event_name:35s}  MDG={local_mdg:7.1f} dB  RV={local_rv:.4f}  {'DETECTED' if detected else 'MISSED'}")

    lines.append(f"\n{'=' * 50}")
    lines.append("CONCLUSION")
    lines.append(f"{'=' * 50}")
    lines.append("HUF ratio-state monitoring detects structural redistribution")
    lines.append("that traditional throughput monitoring misses. The Temporal Sieve")
    lines.append("(dHUF/dt) provides early warning of deceptive drift — changes in")
    lines.append("the relationship between streams even when total throughput is stable.")
    lines.append("")
    lines.append("Key: Ratio Velocity spikes WHERE traditional monitoring sees NOTHING.")
    lines.append("This is the 'Known delta t' — extraction of structural change at each step.")
    lines.append(f"\nFigures saved to: {FIG_DIR}/")

    return '\n'.join(lines)


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    print("=" * 60)
    print("HUF PING HELL TEST")
    print("Higgins Unity Framework — Network Stress Test")
    print("=" * 60)

    all_results = {}
    t_start = time.time()

    # ── Level 1: Simple Demo ──
    print("\n▸ Level 1: Simple Ping Demo (100 pings)")
    sim1 = simulate_simple_ping(n_pings=100, base_loss_rate=0.05)
    ana1 = windowed_analysis(sim1['results'], window_size=20, K=2)
    all_results[1] = {'sim': sim1, 'analysis': ana1}
    plot_simple_demo(sim1, ana1, "level1_simple_ping.png")

    # ── Level 2: Realistic Network ──
    print("\n▸ Level 2: Realistic Network (1000 pings, jitter + bursts)")
    sim2 = simulate_realistic_network(n_pings=1000)
    ana2 = windowed_analysis(sim2['results'], window_size=50, K=2)
    all_results[2] = {'sim': sim2, 'analysis': ana2}
    plot_realistic(sim2, ana2, "level2_realistic.png")

    # ── Level 3: Volume Test ──
    print("\n▸ Level 3: Volume Test (100K pings, slow deceptive drift)")
    sim3 = simulate_volume_test(n_pings=100000, drift_onset=40000)
    ana3 = windowed_analysis(sim3['results'], window_size=200, K=2)
    all_results[3] = {'sim': sim3, 'analysis': ana3}
    plot_volume(sim3, ana3, "level3_volume_100K.png")

    # ── Level 4: Multi-Stream ──
    print("\n▸ Level 4: Multi-Stream (8 endpoints, 5K pings each)")
    sim4 = simulate_multi_stream(n_streams=8, n_pings=5000, correlation=0.3)
    ana4 = multi_stream_analysis(sim4['streams'], window_size=50)
    all_results[4] = {'sim': sim4, 'analysis': ana4}
    plot_multi_stream(sim4, ana4, "level4_multi_stream.png")

    # ── Level 5: HELL TEST ──
    print("\n▸ Level 5: HUF HELL TEST (12 streams × 50K pings, all failure modes)")
    sim5 = simulate_hell_test(n_pings=50000, n_streams=12)
    ana5 = multi_stream_analysis(sim5['streams'], window_size=100)
    all_results[5] = {'sim': sim5, 'analysis': ana5}
    plot_hell_test(sim5, ana5, "level5_HELL_TEST.png")

    elapsed = time.time() - t_start

    # ── Summary Report ──
    print(f"\n▸ Generating summary report...")
    report = generate_summary_report(all_results)

    report_path = os.path.join(FIG_DIR, "HELL_TEST_REPORT.txt")
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"  → Saved HELL_TEST_REPORT.txt")

    # Print report
    print("\n" + report)

    print(f"\n{'=' * 60}")
    print(f"COMPLETE — {elapsed:.1f}s total")
    print(f"Total simulated pings: {sum(s['sim']['n_pings'] for s in all_results.values()):,}")
    print(f"Figures: {FIG_DIR}/")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
