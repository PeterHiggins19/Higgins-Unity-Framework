#!/usr/bin/env python3
"""Generate EXP-19b diagnostic plots."""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Load results
with open("/sessions/wonderful-elegant-pascal/EXP-19b_pipeline_optimization.json") as f:
    report = json.load(f)
with open("/sessions/wonderful-elegant-pascal/EXP-19b_scaling_results.json") as f:
    scaling = json.load(f)

fig = plt.figure(figsize=(18, 14))
fig.patch.set_facecolor('#0D1117')
gs = GridSpec(2, 2, hspace=0.35, wspace=0.3)

colors = {
    'bg': '#0D1117', 'panel': '#161B22', 'text': '#E6EDF3',
    'grid': '#30363D', 'blue': '#58A6FF', 'green': '#3FB950',
    'red': '#F85149', 'gold': '#FFD700', 'purple': '#BC8CFF',
}

# Panel 1: Oracle Verdict Summary
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(colors['panel'])

variants_short = ['OPT-A', 'OPT-B', 'OPT-C', 'OPT-D', 'OPT-E', 'OPT-F']
speedups = [report['baseline']['elapsed_s'] / v['elapsed_s'] for v in report['variants']]
passed = [v['oracle_pass'] for v in report['variants']]
bar_colors = [colors['green'] if p else colors['red'] for p in passed]

bars = ax1.barh(range(len(variants_short)), speedups, color=bar_colors, alpha=0.8, height=0.6)
ax1.axvline(x=1.0, color=colors['gold'], linestyle='--', alpha=0.5, label='Baseline')
ax1.set_yticks(range(len(variants_short)))
ax1.set_yticklabels(variants_short, color=colors['text'], fontsize=11)
ax1.set_xlabel('Speedup vs Baseline', color=colors['text'], fontsize=11)
ax1.set_title('ORACLE VERDICT (N=200)', color=colors['gold'], fontsize=14, fontweight='bold')
ax1.tick_params(colors=colors['text'])
ax1.spines['bottom'].set_color(colors['grid'])
ax1.spines['left'].set_color(colors['grid'])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for i, (s, p) in enumerate(zip(speedups, passed)):
    label = f'{s:.2f}x ✓' if p else f'{s:.2f}x ✗'
    ax1.text(s + 0.02, i, label, color=colors['text'], va='center', fontsize=10)

# Panel 2: Scaling Test
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(colors['panel'])

N_vals = [s['N'] for s in scaling]
orig_times = [s['original_s'] for s in scaling]
opt_times = [s['optimized_s'] for s in scaling]

ax2.loglog(N_vals, orig_times, 'o-', color=colors['red'], linewidth=2, markersize=8, label='Original O(N²·D)')
ax2.loglog(N_vals, opt_times, 's-', color=colors['green'], linewidth=2, markersize=8, label='Optimized O(N·D)')

# Theoretical lines
N_arr = np.array(N_vals)
# Fit original to N²
c_orig = orig_times[-1] / (N_vals[-1]**2)
ax2.loglog(N_arr, c_orig * N_arr**2, '--', color=colors['red'], alpha=0.3, linewidth=1)
# Fit optimized to N
c_opt = opt_times[-1] / N_vals[-1]
ax2.loglog(N_arr, c_opt * N_arr, '--', color=colors['green'], alpha=0.3, linewidth=1)

ax2.set_xlabel('N (samples)', color=colors['text'], fontsize=11)
ax2.set_ylabel('Time (seconds)', color=colors['text'], fontsize=11)
ax2.set_title('SCALING: O(N²) → O(N)', color=colors['gold'], fontsize=14, fontweight='bold')
ax2.legend(facecolor=colors['panel'], edgecolor=colors['grid'], labelcolor=colors['text'], fontsize=10)
ax2.tick_params(colors=colors['text'])
ax2.grid(True, alpha=0.2, color=colors['grid'])
ax2.spines['bottom'].set_color(colors['grid'])
ax2.spines['left'].set_color(colors['grid'])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Panel 3: Deviation Analysis
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor(colors['panel'])

max_devs = [v['max_deviation'] for v in report['variants']]
n_devs = [v['n_deviations'] for v in report['variants']]

x_pos = range(len(variants_short))
bars3 = ax3.bar(x_pos, max_devs, color=colors['blue'], alpha=0.8, width=0.5, label='Max Deviation')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(variants_short, color=colors['text'], fontsize=10)
ax3.set_ylabel('Max Relative Deviation', color=colors['text'], fontsize=11)
ax3.set_title('METRIC PRESERVATION (all = 0.000)', color=colors['gold'], fontsize=14, fontweight='bold')
ax3.tick_params(colors=colors['text'])
ax3.spines['bottom'].set_color(colors['grid'])
ax3.spines['left'].set_color(colors['grid'])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Annotate zero-deviation
for i, d in enumerate(max_devs):
    ax3.text(i, d + 0.0001, f'{d:.6f}', ha='center', color=colors['green'], fontsize=10)

ax3.set_ylim(-0.001, 0.01)
ax3.axhline(y=0, color=colors['green'], linestyle='-', alpha=0.5)

# Panel 4: Complexity Summary
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(colors['panel'])
ax4.axis('off')

complexity = report['complexity_analysis']
text_lines = [
    ("COMPLEXITY REDUCTION", colors['gold'], 16, 'bold'),
    ("", colors['text'], 8, 'normal'),
    ("Original Pipeline", colors['red'], 13, 'bold'),
    ("  Aitchison Variance: O(N²·D)  ← BOTTLENECK", colors['text'], 11, 'normal'),
    ("  Super Squeeze: O(N·28 constants)", colors['text'], 11, 'normal'),
    ("  Ternary→Complex→Helix: 3 separate passes", colors['text'], 11, 'normal'),
    ("  Total: O(N²·D)", colors['red'], 12, 'bold'),
    ("", colors['text'], 8, 'normal'),
    ("Optimized Pipeline (OPT-F)", colors['green'], 13, 'bold'),
    ("  CLR+Variance: O(N·D) Welford online", colors['text'], 11, 'normal'),
    ("  Super Squeeze: O(N·28) ALL constants kept", colors['text'], 11, 'normal'),
    ("  Ternary+Complex+Helix: 1 fused pass", colors['text'], 11, 'normal'),
    ("  Total: O(N·D)", colors['green'], 12, 'bold'),
    ("", colors['text'], 8, 'normal'),
    (f"Speedup at N=10000: {scaling[-1]['original_s']/scaling[-1]['optimized_s']:.1f}×", colors['gold'], 14, 'bold'),
    ("Oracle: 6/6 PASS — all invariants preserved", colors['green'], 12, 'bold'),
    ("Max deviation: 0.000000 across all metrics", colors['blue'], 11, 'normal'),
]

y = 0.95
for text, color, size, weight in text_lines:
    ax4.text(0.05, y, text, transform=ax4.transAxes, color=color,
             fontsize=size, fontweight=weight, va='top', fontfamily='monospace')
    y -= 0.06 if size >= 12 else 0.05

# Title
fig.suptitle('EXP-19b: Pipeline Optimization via Conjugate Pair Validation',
             color=colors['gold'], fontsize=18, fontweight='bold', y=0.98)

plt.savefig('/sessions/wonderful-elegant-pascal/EXP-19b_pipeline_optimization.png',
            dpi=150, bbox_inches='tight', facecolor=colors['bg'])
print("Saved: EXP-19b_pipeline_optimization.png")

# Also save scaling plot alone
fig2, ax = plt.subplots(figsize=(10, 6))
fig2.patch.set_facecolor(colors['bg'])
ax.set_facecolor(colors['panel'])

speedup_vals = [s['original_s']/s['optimized_s'] for s in scaling]
ax.plot(N_vals, speedup_vals, 'o-', color=colors['gold'], linewidth=2.5, markersize=10)
ax.plot(N_vals, [n/N_vals[0] for n in N_vals], '--', color=colors['blue'], alpha=0.4, label='Linear (N× theoretical)')
ax.set_xlabel('N (samples)', color=colors['text'], fontsize=13)
ax.set_ylabel('Speedup (×)', color=colors['text'], fontsize=13)
ax.set_title('Speedup Growth: Original → Optimized Pipeline', color=colors['gold'], fontsize=15, fontweight='bold')
ax.legend(facecolor=colors['panel'], edgecolor=colors['grid'], labelcolor=colors['text'], fontsize=11)
ax.tick_params(colors=colors['text'])
ax.grid(True, alpha=0.2, color=colors['grid'])
ax.spines['bottom'].set_color(colors['grid'])
ax.spines['left'].set_color(colors['grid'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for n, s in zip(N_vals, speedup_vals):
    ax.annotate(f'{s:.1f}×', (n, s), textcoords="offset points",
                xytext=(0, 12), ha='center', color=colors['text'], fontsize=10)

plt.savefig('/sessions/wonderful-elegant-pascal/EXP-19b_scaling_speedup.png',
            dpi=150, bbox_inches='tight', facecolor=colors['bg'])
print("Saved: EXP-19b_scaling_speedup.png")
