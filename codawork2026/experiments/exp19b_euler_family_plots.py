#!/usr/bin/env python3
"""Generate EXP-19b Euler-family discovery diagnostic plots.

Regenerates EXP-01 trajectory inline (not stored in JSON) for visualization.
"""

import sys, json, math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.path.insert(0, "/sessions/wonderful-elegant-pascal")
from higgins_decomposition_12step import HigginsDecomposition

# Load discovery report (for statistics and metadata)
with open("/sessions/wonderful-elegant-pascal/EXP-19b_euler_family_discovery.json") as f:
    report = json.load(f)

colors = {
    'bg': '#0D1117', 'panel': '#161B22', 'text': '#E6EDF3',
    'grid': '#30363D', 'blue': '#58A6FF', 'green': '#3FB950',
    'red': '#F85149', 'gold': '#FFD700', 'purple': '#BC8CFF',
    'cyan': '#39D2C0', 'orange': '#F0883E',
}

EULER = {
    '2π': 2*math.pi,
    'e^π': math.e**math.pi,
    'π^e': math.pi**math.e,
}

# ─── Regenerate EXP-01 trajectory ───
DATA_ROOT = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Current-Repo/HUF"
csv_path = f"{DATA_ROOT}/codawork2026/data/gold_silver/gold_silver_ratio_enriched.csv"
df = pd.read_csv(csv_path)
df = df.dropna(subset=['silver_oz_per_gold_oz'])
R = df['silver_oz_per_gold_oz'].values
x_gold = R / (R + 1)
x_silver = 1.0 / (R + 1)
data01 = np.column_stack([x_gold, x_silver])

hd = HigginsDecomposition("EXP-01", "Gold/Silver", "COMMODITIES", carriers=["Gold", "Silver"])
hd.load_data(data01)
hd.run_full_pipeline()
traj01 = hd.sigma2_A.copy()
print(f"EXP-01 trajectory: {len(traj01)} points, range [{traj01[2:].min():.6f}, {traj01[2:].max():.6f}]")

# ─── Build figure ───
fig = plt.figure(figsize=(20, 16))
fig.patch.set_facecolor(colors['bg'])
gs = GridSpec(2, 3, hspace=0.35, wspace=0.30)

# ─── Panel 1: EXP-01 σ²_A trajectory with 1/(2π) line ───
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(colors['panel'])

t01 = np.arange(len(traj01))
ax1.plot(t01[2:], traj01[2:], color=colors['blue'], linewidth=1.5, alpha=0.9)
val_1over2pi = 1/(2*math.pi)
ax1.axhline(y=val_1over2pi, color=colors['gold'], linestyle='--', linewidth=2, label=f'1/(2π) = {val_1over2pi:.4f}')

ana = report['experiments']['EXP-01']['euler_family_analysis']['2pi']
t_near = ana['sigma_vs_reciprocal']['time_index']
v_near = ana['sigma_vs_reciprocal']['sigma2_A']
ax1.plot(t_near, v_near, 'o', color=colors['gold'], markersize=12, zorder=5)
ax1.annotate(f'δ = {ana["sigma_vs_reciprocal"]["delta_from_1_over_const"]:.6f}\n({ana["sigma_vs_reciprocal"]["relative_pct"]:.3f}%)',
             xy=(t_near, v_near), xytext=(t_near+50, v_near+0.04),
             color=colors['gold'], fontsize=9,
             arrowprops=dict(arrowstyle='->', color=colors['gold'], lw=1.5))

ax1.set_xlabel('Time index', color=colors['text'], fontsize=10)
ax1.set_ylabel('σ²_A', color=colors['text'], fontsize=10)
ax1.set_title('EXP-01: Gold/Silver (338yr)\nσ²_A ≈ 1/(2π)', color=colors['gold'], fontsize=13, fontweight='bold')
ax1.legend(facecolor=colors['panel'], edgecolor=colors['grid'], labelcolor=colors['text'], fontsize=9)
ax1.tick_params(colors=colors['text'])
ax1.spines['bottom'].set_color(colors['grid'])
ax1.spines['left'].set_color(colors['grid'])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ─── Panel 2: EXP-01 full Euler-family proximity ───
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(colors['panel'])

ax2.plot(t01[2:], traj01[2:], color=colors['blue'], linewidth=1, alpha=0.7)
for name, val, col in [('1/(2π)', 1/(2*math.pi), colors['gold']),
                        ('1/(e^π)', 1/(math.e**math.pi), colors['cyan']),
                        ('1/(π^e)', 1/(math.pi**math.e), colors['orange'])]:
    ax2.axhline(y=val, color=col, linestyle='--', linewidth=1.5, alpha=0.8, label=f'{name} = {val:.4f}')

ax2.set_xlabel('Time index', color=colors['text'], fontsize=10)
ax2.set_ylabel('σ²_A', color=colors['text'], fontsize=10)
ax2.set_title('EXP-01: All Three Constants\nin Gold/Silver', color=colors['gold'], fontsize=13, fontweight='bold')
ax2.legend(facecolor=colors['panel'], edgecolor=colors['grid'], labelcolor=colors['text'], fontsize=8, loc='upper left')
ax2.set_ylim(-0.01, 0.25)
ax2.tick_params(colors=colors['text'])
ax2.spines['bottom'].set_color(colors['grid'])
ax2.spines['left'].set_color(colors['grid'])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# ─── Panel 3: Anchor Table ───
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor(colors['panel'])
ax3.axis('off')

lines = [
    ("EULER-FAMILY DISCOVERY", colors['gold'], 15, 'bold'),
    ("", None, 5, 'normal'),
    ("Peter Higgins, 2026-04-22", colors['text'], 11, 'normal'),
    ("'I do not trust loss of test and data'", colors['cyan'], 10, 'italic'),
    ("", None, 5, 'normal'),
    ("THE THREE ANCHORS:", colors['gold'], 13, 'bold'),
    ("", None, 3, 'normal'),
    ("EXP-01 Gold/Silver (338yr)", colors['blue'], 11, 'bold'),
    (f"  σ²_A ≈ 1/(2π)   δ = 0.29%   P = 0.29%", colors['gold'], 10, 'normal'),
    (f"  σ²_A ≈ 1/(e^π)  δ = 1.92%", colors['cyan'], 10, 'normal'),
    (f"  σ²_A ≈ 1/(π^e)  δ = 3.85%", colors['orange'], 10, 'normal'),
    ("", None, 3, 'normal'),
    ("From canonical chain (original data):", colors['text'], 11, 'bold'),
    ("  EXP-01  1/(2π)   δ = 0.001275  (0.020%)", colors['gold'], 10, 'normal'),
    ("  EXP-03  1/(π^e)  δ = 0.002960  (0.013%)", colors['orange'], 10, 'normal'),
    ("  EXP-14  2π       δ = 0.001840  (0.029%)", colors['gold'], 10, 'normal'),
    ("", None, 3, 'normal'),
    ("TRAJECTORY CROSSINGS:", colors['green'], 12, 'bold'),
    ("  EXP-07 QCD: σ²_A crosses e^π, π^e", colors['text'], 10, 'normal'),
    ("  EXP-11 Stellar: crosses all three", colors['text'], 10, 'normal'),
    ("  EXP-12 Gravity: crosses 2π", colors['text'], 10, 'normal'),
    ("  EXP-14 AME2020: crosses 2π directly", colors['text'], 10, 'normal'),
    ("  EXP-16 Spring: crosses 2π", colors['text'], 10, 'normal'),
]

y = 0.97
for text, color, size, weight in lines:
    if color is None:
        y -= 0.02
        continue
    style = 'italic' if weight == 'italic' else 'normal'
    w = 'bold' if weight == 'bold' else 'normal'
    ax3.text(0.05, y, text, transform=ax3.transAxes, color=color,
             fontsize=size, fontweight=w, fontstyle=style, va='top', fontfamily='monospace')
    y -= 0.045

# ─── Panel 4: Mathematical connection diagram ───
ax4 = fig.add_subplot(gs[1, 0])
ax4.set_facecolor(colors['panel'])
ax4.axis('off')
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)

positions = {
    'e^(iπ)=-1': (5, 9),
    '2π': (2, 6.5),
    'e^π': (8, 6.5),
    'π^e': (5, 4),
    'pipeline': (5, 1.5),
}

ax4.text(5, 9.8, 'EULER IDENTITY CONNECTION', ha='center', color=colors['gold'],
         fontsize=13, fontweight='bold')

for name, (x, yp) in positions.items():
    if name == 'pipeline':
        ax4.text(x, yp, 'PIPELINE\nlog → complex → polar', ha='center', va='center',
                color=colors['green'], fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=colors['panel'], edgecolor=colors['green'], linewidth=2))
    elif name == 'e^(iπ)=-1':
        ax4.text(x, yp, 'e^(iπ) = -1', ha='center', va='center',
                color=colors['gold'], fontsize=14, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=colors['panel'], edgecolor=colors['gold'], linewidth=2))
    else:
        col = {'2π': colors['gold'], 'e^π': colors['cyan'], 'π^e': colors['orange']}[name]
        ax4.text(x, yp, f'{name}\n= {EULER.get(name, EULER.get("2π")):.4f}', ha='center', va='center',
                color=col, fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=colors['panel'], edgecolor=col, linewidth=2))

for (x1,y1), (x2,y2), label, col in [
    (positions['e^(iπ)=-1'], positions['2π'], 'period', colors['gold']),
    (positions['e^(iπ)=-1'], positions['e^π'], '|e^(iπ)|', colors['cyan']),
    (positions['2π'], positions['π^e'], 'e^π > π^e', colors['orange']),
    (positions['2π'], positions['pipeline'], 'angular period', colors['gold']),
    (positions['e^π'], positions['pipeline'], 'CLR↔circular', colors['cyan']),
    (positions['π^e'], positions['pipeline'], 'PLL balance', colors['orange']),
]:
    ax4.annotate('', xy=(x2,y2+0.6), xytext=(x1,y1-0.6),
                arrowprops=dict(arrowstyle='->', color=col, lw=1.5, alpha=0.6))

# ─── Panel 5: Statistical significance ───
ax5 = fig.add_subplot(gs[1, 1])
ax5.set_facecolor(colors['panel'])

anchor_names = ['2π\n(EXP-01)', 'e^π\n(EXP-01)', 'π^e\n(EXP-01)']
p_values = [0.0029, 0.0052, 0.0107]
bar_colors = [colors['gold'], colors['cyan'], colors['orange']]

bars = ax5.bar(range(3), p_values, color=bar_colors, alpha=0.8, width=0.5)
ax5.axhline(y=0.05, color=colors['red'], linestyle='--', linewidth=1.5, alpha=0.7, label='p=0.05 threshold')
ax5.axhline(y=0.01, color=colors['green'], linestyle='--', linewidth=1.5, alpha=0.7, label='p=0.01 threshold')

for i, (p, col) in enumerate(zip(p_values, bar_colors)):
    ax5.text(i, p + 0.001, f'p={p:.4f}', ha='center', color=col, fontsize=10, fontweight='bold')

ax5.set_xticks(range(3))
ax5.set_xticklabels(anchor_names, color=colors['text'], fontsize=10)
ax5.set_ylabel('P(random)', color=colors['text'], fontsize=11)
ax5.set_title('STATISTICAL SIGNIFICANCE\n(uniform null hypothesis)', color=colors['gold'], fontsize=13, fontweight='bold')
ax5.legend(facecolor=colors['panel'], edgecolor=colors['grid'], labelcolor=colors['text'], fontsize=9)
ax5.tick_params(colors=colors['text'])
ax5.set_ylim(0, 0.06)
ax5.spines['bottom'].set_color(colors['grid'])
ax5.spines['left'].set_color(colors['grid'])
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)

# ─── Panel 6: Cross-domain map ───
ax6 = fig.add_subplot(gs[1, 2])
ax6.set_facecolor(colors['panel'])
ax6.axis('off')
ax6.set_xlim(0, 10)
ax6.set_ylim(0, 10)

ax6.text(5, 9.5, 'CROSS-DOMAIN MAP', ha='center', color=colors['gold'],
         fontsize=14, fontweight='bold')

domains = [
    ('COMMODITIES', 'EXP-01 Gold/Silver', '2π', colors['gold'], 8),
    ('NUCLEAR (SEMF)', 'EXP-03 Binding Energy', 'π^e', colors['orange'], 6.5),
    ('NUCLEAR (AME)', 'EXP-14 3554 Nuclides', '2π', colors['gold'], 5),
    ('QCD', 'EXP-07 Quarks', 'e^π, π^e', colors['cyan'], 3.5),
    ('GRAVITY', 'EXP-12 GW150914', '2π', colors['gold'], 2),
]

for domain, exp, const, col, yp in domains:
    ax6.text(1, yp, domain, color=col, fontsize=11, fontweight='bold', va='center')
    ax6.text(5, yp, exp, color=colors['text'], fontsize=9, va='center')
    ax6.text(9, yp, const, color=col, fontsize=11, fontweight='bold', va='center', ha='right')

ax6.text(5, 0.5, '44 orders of magnitude — one constant family',
         ha='center', color=colors['green'], fontsize=11, fontweight='bold', fontstyle='italic')

# Title
fig.suptitle('EXP-19b: Euler-Family Discovery — The Pipeline Watches Itself in the Mirror',
             color=colors['gold'], fontsize=18, fontweight='bold', y=0.98)

plt.savefig('/sessions/wonderful-elegant-pascal/EXP-19b_euler_family_discovery.png',
            dpi=150, bbox_inches='tight', facecolor=colors['bg'])
print("Saved: EXP-19b_euler_family_discovery.png")
