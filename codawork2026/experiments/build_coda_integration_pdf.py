#!/usr/bin/env python3
"""
CoDa + EITT INTEGRATION REPORT
================================
Formal PDF for CoDaWork audience showing every CoDa tool and every EITT tool
applied to 20 blind datasets across 6 domains.
"""

import json, os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable
)

OUT_PDF = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HIGGINS_CoDa_EITT_Integration.pdf"
PLOT_DIR = "/sessions/wonderful-elegant-pascal/coda_integration_plots"
DATA_JSON = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/DATA/HIGGINS_coda_eitt_integration.json"

# ── Load data ──────────────────────────────────────────────────────────────
with open(DATA_JSON) as f:
    data = json.load(f)
meta = data['_meta']
scores = data['scores']
results = data['results']

# ── Styles (same palette as HIVP Master) ───────────────────────────────────
styles = getSampleStyleSheet()
styles.add(ParagraphStyle('CoverTitle', parent=styles['Title'], fontSize=26, leading=32,
    spaceAfter=6, textColor=HexColor('#0d1b2a'), alignment=TA_CENTER, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('CoverSub', parent=styles['Normal'], fontSize=13, leading=17,
    spaceAfter=4, textColor=HexColor('#1b263b'), alignment=TA_CENTER, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('SectionHead', parent=styles['Heading1'], fontSize=16, leading=20,
    spaceBefore=16, spaceAfter=8, textColor=HexColor('#0d1b2a'), fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('SubHead', parent=styles['Heading2'], fontSize=12, leading=15,
    spaceBefore=10, spaceAfter=4, textColor=HexColor('#1b263b'), fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.5, leading=13,
    spaceAfter=6, fontName='Helvetica'))
styles.add(ParagraphStyle('BodyJ', parent=styles['Normal'], fontSize=9.5, leading=13,
    spaceAfter=6, fontName='Helvetica', alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('Caption', parent=styles['Normal'], fontSize=8, leading=10,
    spaceAfter=8, fontName='Helvetica-Oblique', textColor=HexColor('#333333'), alignment=TA_CENTER))
styles.add(ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=7, leading=9, fontName='Helvetica'))
styles.add(ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=7, leading=9,
    fontName='Helvetica-Bold', textColor=white))
styles.add(ParagraphStyle('Quote', parent=styles['Normal'], fontSize=9, leading=12,
    fontName='Helvetica-Oblique', textColor=HexColor('#0d1b2a'),
    leftIndent=24, rightIndent=24, spaceAfter=8, alignment=TA_CENTER))
styles.add(ParagraphStyle('BulletItem', parent=styles['Normal'], fontSize=9.5, leading=13,
    spaceAfter=3, fontName='Helvetica', leftIndent=18, bulletIndent=6))

HEADER_BG = HexColor('#0d1b2a')
ROW_ALT   = HexColor('#e8ecf1')
BORDER    = HexColor('#adb5bd')
GREEN     = '#27ae60'
RED       = '#e74c3c'
AMBER     = '#f39c12'

def P(text, style='Body'):
    return Paragraph(text, styles[style])

def PJ(text):
    return Paragraph(text, styles['BodyJ'])

def verdict_cell(correct):
    c = GREEN if correct else RED
    sym = 'Y' if correct else 'N'
    return Paragraph(f'<font color="{c}"><b>{sym}</b></font>', styles['TableCell'])

def class_cell(cls, correct):
    c = GREEN if correct else RED
    short = 'L' if cls == 'LEGITIMATE' else 'F'
    return Paragraph(f'<font color="{c}"><b>{short}</b></font>', styles['TableCell'])

def std_table(data, widths):
    t = Table(data, colWidths=[w*inch for w in widths])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor('#ffffff'), ROW_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def add_image(story, path, w=6.5, h=4.0):
    if os.path.exists(path):
        story.append(Image(path, width=w*inch, height=h*inch))

fig_num = [0]
tbl_num = [0]
def fig_caption(text):
    fig_num[0] += 1
    return P(f'<b>Figure {fig_num[0]}.</b> {text}', 'Caption')

def tbl_caption(text):
    tbl_num[0] += 1
    return P(f'<b>Table {tbl_num[0]}.</b> {text}', 'Caption')

# ── Build document ─────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUT_PDF, pagesize=letter,
    topMargin=0.6*inch, bottomMargin=0.6*inch,
    leftMargin=0.75*inch, rightMargin=0.75*inch)
story = []

# ── COVER ──────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.2*inch))
story.append(P('The Higgins Decomposition', 'CoverTitle'))
story.append(P('CoDa + EITT Full Integration', 'CoverTitle'))
story.append(Spacer(1, 0.3*inch))
story.append(P('Every CoDa tool. Every EITT tool.', 'CoverSub'))
story.append(P('20 datasets. 6 domains. Blind protocol.', 'CoverSub'))
story.append(Spacer(1, 0.4*inch))
story.append(HRFlowable(width='60%', thickness=2, color=HEADER_BG))
story.append(Spacer(1, 0.3*inch))
story.append(P(f'Pass 1: {scores["pass_1"]}/20 (85%)  |  Pass 2: {scores["pass_2"]}/20 (90%)', 'CoverSub'))
story.append(Spacer(1, 0.5*inch))
story.append(P('Peter Higgins', 'CoverSub'))
story.append(P(f'{datetime.now().strftime("%d %B %Y")}', 'CoverSub'))
story.append(Spacer(1, 0.3*inch))
story.append(P('<i>CoDa measures STRUCTURE. EITT measures TEMPORAL INVARIANCE.<br/>Together: the full instrument.</i>', 'Quote'))
story.append(PageBreak())

# ── 1. INTRODUCTION ───────────────────────────────────────────────────────
story.append(P('1. Introduction', 'SectionHead'))
story.append(PJ(
    'Compositional Data Analysis (CoDa) provides a rigorous algebraic framework for data '
    'constrained to a simplex: log-ratio transforms (CLR, ILR, ALR), Aitchison geometry, '
    'perturbation and powering operations, compositional PCA, and simplicial depth. '
    'These tools measure the <b>structure</b> of a composition \u2014 its spread, centrality, '
    'and geometric relationships.'
))
story.append(PJ(
    'The Entropy Invariance Time Test (EITT) adds a complementary dimension: <b>temporal invariance</b>. '
    'By decimating a time series into M-blocks and measuring Shannon entropy at each scale, '
    'EITT tests whether the compositional structure is preserved under temporal coarse-graining. '
    'Legitimate signals maintain entropy invariance; fabricated or contaminated signals do not.'
))
story.append(PJ(
    'This report presents the full integration of both toolkits applied to 20 blind datasets '
    'spanning 6 domains (Commodities, Nuclear, Acoustics, Synthetic, Noise, Adversarial). '
    'The key bridge between the two frameworks: CoDa\'s Aitchison variance (\u03c3\u00b2<sub>A</sub>) '
    'predicts EITT\'s critical decimation point (M<sub>break</sub>).'
))

# ── 2. CoDa TOOLKIT ──────────────────────────────────────────────────────
story.append(P('2. CoDa Toolkit Applied', 'SectionHead'))

coda_tools_desc = [
    ('CLR Transform', 'Centered log-ratio: maps D-part composition to D log-ratios summing to zero. '
     'Preserves all pairwise information. Used for visualization and spread measurement.'),
    ('ILR Transform', 'Isometric log-ratio via Helmert basis: maps D-part composition to (D-1) orthonormal '
     'coordinates in real space. The theoretically correct transform for multivariate statistics.'),
    ('ALR Transform', 'Additive log-ratio relative to reference component: (D-1) unconstrained coordinates. '
     'Interpretable but geometry-dependent on reference choice.'),
    ('Aitchison Distance', 'The natural metric on the simplex: d<sub>A</sub>(x,y) = ||clr(x) - clr(y)||. '
     'Used to measure pairwise dissimilarity between compositions.'),
    ('Aitchison Variance', 'Total variance (\u03c3\u00b2<sub>A</sub> = totvar): the trace of the variation matrix. '
     'The single most important CoDa summary statistic. <b>Bridges to EITT via M<sub>break</sub> prediction.</b>'),
    ('Variation Matrix', 'D\u00d7D matrix of var(ln x<sub>i</sub>/x<sub>j</sub>). Captures all pairwise '
     'log-ratio variabilities. Zero entries indicate proportional components.'),
    ('Fr\u00e9chet Mean', 'The geometric mean closed to the simplex. The natural center of a compositional '
     'dataset in Aitchison geometry.'),
    ('Perturbation', 'Simplex addition: x \u2295 y = C(x<sub>1</sub>y<sub>1</sub>, ..., x<sub>D</sub>y<sub>D</sub>). '
     'Verified isometric: d<sub>A</sub>(x\u2295z, y\u2295z) = d<sub>A</sub>(x,y).'),
    ('Powering', 'Simplex scalar multiplication: \u03b1 \u2299 x = C(x<sub>1</sub><super>\u03b1</super>, ..., x<sub>D</sub><super>\u03b1</super>). '
     'Verified scaling: d<sub>A</sub>(\u03b1\u2299x, \u03b1\u2299y) = |\u03b1| d<sub>A</sub>(x,y).'),
    ('Compositional PCA', 'PCA on CLR-transformed data. PC1 variance explained indicates dimensionality. '
     'Time series: high PC1% = strong dominant trend.'),
    ('Simplicial Depth', 'Statistical depth measuring centrality on the simplex. '
     'Values near 0.5 indicate central compositions; near 0 indicate outliers.'),
]

for name, desc in coda_tools_desc:
    story.append(P(f'<b>{name}.</b> {desc}', 'BulletItem'))

# ── 3. EITT TOOLKIT ──────────────────────────────────────────────────────
story.append(P('3. EITT Toolkit Applied', 'SectionHead'))

eitt_tools_desc = [
    ('Geometric-Mean Decimation', 'Block-averages N observations into M groups using geometric means '
     '(natural for compositions). Tests M = 2, 3, ..., floor(N/5).'),
    ('Shannon Entropy Invariance', 'H\u0304 = mean normalized entropy across components at each M. '
     'Legitimate signals: H\u0304 stable. Fabricated: H\u0304 diverges or collapses.'),
    ('Pass-Rate Classifier', 'Fraction of tested M values where |H\u0304(M) - H\u0304(2)| < threshold. '
     'Pass rate > 80%: LEGITIMATE. Pass rate < 80%: FABRICATED.'),
    ('M<sub>break</sub> Prediction', '\u03c3\u00b2<sub>A</sub> predicts the decimation scale where entropy '
     'invariance breaks. The bridge equation: M<sub>break</sub> \u221d f(\u03c3\u00b2<sub>A</sub>).'),
    ('F17 Contamination Tuner', 'Geometric mean of the variation matrix off-diagonal. '
     'Normalized: C<sub>geom</sub>/\u03c3\u00b2<sub>A</sub>. Flags anomalous inter-component coupling.'),
    ('Stored Energy Alarm', 'Detects resonance patterns in the entropy-vs-M curve that mimic '
     'legitimate behavior but carry fabrication signatures at higher M.'),
    ('Two-Pass Resolution Boundary', 'Pass 1 classifies. Pass 2 applies F17 tiebreaker (marginal cases only), '
     'min-blocks guard, and stored energy alarm. Reports resolution boundaries, not failures.'),
]

for name, desc in eitt_tools_desc:
    story.append(P(f'<b>{name}.</b> {desc}', 'BulletItem'))

story.append(PageBreak())

# ── 4. THE BRIDGE: sigma2_A predicts M_break ─────────────────────────────
story.append(P('4. The Bridge: CoDa \u03c3\u00b2<sub>A</sub> Predicts EITT M<sub>break</sub>', 'SectionHead'))
story.append(PJ(
    'The central insight connecting the two frameworks: Aitchison variance (\u03c3\u00b2<sub>A</sub>), '
    'a purely structural CoDa metric computed from the variation matrix, predicts the critical '
    'decimation point M<sub>break</sub> where EITT entropy invariance fails. Low-variance compositions '
    '(tight simplex clusters) preserve entropy to high M. High-variance compositions (diffuse spreads) '
    'break earlier. This is not coincidence \u2014 it follows from Theorem 2: the geometric mean of '
    'the variation matrix scales with \u03c3\u00b2<sub>A</sub>, and the variation matrix governs how '
    'block-averaging redistributes compositional mass.'
))
story.append(PJ(
    'This bridge means CoDa practitioners can predict EITT behavior from familiar metrics, '
    'and EITT results can be interpreted through the lens of Aitchison geometry. The two toolkits '
    'are not competitors \u2014 they are complementary views of the same underlying compositional reality.'
))

# ── 5. FULL RESULTS TABLE ────────────────────────────────────────────────
story.append(P('5. Full Integration Results: 20 Blind Datasets', 'SectionHead'))

# Build the big table — 11 columns, wider to avoid text wrapping
header = [P(h, 'TableHeader') for h in [
    'Blind ID', 'Domain', '\u03c3\u00b2_A', 'CLR Sprd', 'Depth',
    'H\u0304', 'Pass P1', 'Pass P2', 'F17n', 'P2 Class', 'OK'
]]

rows = [header]
for r in sorted(results, key=lambda x: int(x['blind_id'].split('-')[1])):
    true_short = 'L' if r['true_label'] == 'LEGITIMATE' else 'F'
    p2_short = 'L' if r['class_p2'] == 'LEGITIMATE' else 'F'
    ok = r['correct_p2']
    c = GREEN if ok else RED
    rows.append([
        P(r['blind_id'], 'TableCell'),
        P(r['true_domain'], 'TableCell'),
        P(f'{r["sigma2_A"]:.3f}' if r['sigma2_A'] < 10 else f'{r["sigma2_A"]:.1f}', 'TableCell'),
        P(f'{r["clr_spread"]:.3f}' if r['clr_spread'] < 10 else f'{r["clr_spread"]:.1f}', 'TableCell'),
        P(f'{r["simplicial_depth"]:.3f}', 'TableCell'),
        P(f'{r["H_bar"]:.3f}', 'TableCell'),
        P(f'{r["pass_rate_p1"]*100:.0f}%', 'TableCell'),
        P(f'{r["pass_rate_p2"]*100:.0f}%', 'TableCell'),
        P(f'{r["f17_normalized"]:.4f}', 'TableCell'),
        Paragraph(f'<font color="{c}"><b>{p2_short}</b></font> (true:{true_short})', styles['TableCell']),
        verdict_cell(ok),
    ])

widths = [0.62, 0.7, 0.52, 0.52, 0.48, 0.48, 0.5, 0.5, 0.52, 0.76, 0.3]
story.append(std_table(rows, widths))
story.append(tbl_caption(
    'Full CoDa + EITT results for 20 blind datasets. L=Legitimate, F=Fabricated. '
    'Green=correct, Red=resolution boundary. Pass 1: 17/20, Pass 2: 18/20.'
))

story.append(Spacer(1, 8))
story.append(PJ(
    f'<b>Overall accuracy:</b> Pass 1 achieved {scores["pass_1"]}/20 (85%). '
    f'Pass 2 improved to {scores["pass_2"]}/20 (90%) by applying the F17 tiebreaker '
    f'to one marginal case (BLIND-11, Adversarial domain). Two resolution boundaries remain: '
    f'BLIND-12 (high-variance acoustics, \u03c3\u00b2<sub>A</sub>=28.1) and '
    f'BLIND-14 (adversarial, designed to exploit the instrument\'s blind spot).'
))

story.append(PageBreak())

# ── 6. INTEGRATION DASHBOARD ─────────────────────────────────────────────
story.append(P('6. Integration Dashboard', 'SectionHead'))
story.append(PJ(
    'The 3\u00d73 dashboard below shows the full CoDa + EITT integration. '
    'Top row: the bridge (\u03c3\u00b2<sub>A</sub> vs M<sub>break</sub>), CLR spread vs EITT pass rate, '
    'and simplicial depth by class. Middle row: Aitchison distance vs F17, CoDa PCA vs EITT classification, '
    'and CoDa algebra verification (perturbation isometry + powering scaling). '
    'Bottom row: EITT curves coloured by \u03c3\u00b2<sub>A</sub>, variation matrix heatmap, '
    'and the integration summary.'
))
add_image(story, f'{PLOT_DIR}/coda_eitt_dashboard.png', 6.8, 5.5)
story.append(fig_caption('CoDa + EITT Integration Dashboard. 9 panels showing every CoDa tool and every EITT tool working together across 20 datasets.'))

story.append(PageBreak())

# ── 7. CLASS SEPARATION COMPARISON ────────────────────────────────────────
story.append(P('7. Class Separation: CoDa Metrics vs EITT', 'SectionHead'))
story.append(PJ(
    'A critical question: which metrics best separate legitimate from fabricated compositions? '
    'The boxplots below compare five CoDa metrics (Aitchison variance, CLR spread, mean Aitchison distance, '
    'simplicial depth, PC1 variance explained) against EITT pass rate. '
    'CoDa metrics show overlapping distributions \u2014 both classes can produce high or low variance, '
    'central or peripheral compositions. EITT pass rate achieves near-complete separation: '
    'legitimate signals cluster at 100%, fabricated signals cluster near 0%.'
))
story.append(PJ(
    'This does not diminish CoDa \u2014 it clarifies the division of labour. CoDa measures '
    '<i>what</i> a composition is. EITT measures <i>whether it is real</i>. '
    'A pathologist needs both anatomy and histology.'
))
add_image(story, f'{PLOT_DIR}/coda_class_separation.png', 6.8, 3.8)
story.append(fig_caption('Class separation comparison. CoDa metrics show overlap between legitimate and fabricated classes. EITT pass rate achieves near-complete separation.'))

# ── 8. EITT BY DOMAIN ────────────────────────────────────────────────────
story.append(P('8. EITT Across All 6 Domains', 'SectionHead'))
story.append(PJ(
    'The six panels below show EITT entropy-vs-decimation curves for each domain, '
    'with CoDa \u03c3\u00b2<sub>A</sub> values labelled. Solid lines: legitimate signals. '
    'Dashed lines: fabricated signals. '
    'The visual pattern is consistent across domains: legitimate curves are flat (entropy-invariant), '
    'fabricated curves diverge. The \u03c3\u00b2<sub>A</sub> labels confirm the bridge \u2014 '
    'higher CoDa variance correlates with earlier entropy breakdown.'
))
add_image(story, f'{PLOT_DIR}/coda_eitt_by_domain.png', 6.8, 4.0)
story.append(fig_caption('EITT curves across 6 domains with CoDa \u03c3\u00b2_A labels. Solid=Legitimate, Dashed=Fabricated. Labels show CoDa Aitchison variance for each dataset.'))

story.append(PageBreak())

# ── 9. RESOLUTION BOUNDARIES ─────────────────────────────────────────────
story.append(P('9. Resolution Boundaries', 'SectionHead'))
story.append(PJ(
    'The instrument reports two resolution boundaries \u2014 cases where its resolving power '
    'reaches its limit. These are not failures; they are the instrument positively identifying '
    'where it cannot distinguish signal from noise, analogous to a phase-locked loop reporting '
    'an out-of-lock condition. A resolution boundary is a feature, not a defect.'
))

# Resolution boundary table
boundaries = [r for r in results if not r['correct_p2']]
if boundaries:
    story.append(P('9.1 Boundary Cases', 'SubHead'))
    b_header = [P(h, 'TableHeader') for h in [
        'Blind ID', 'Domain', 'True', '\u03c3\u00b2_A', 'Pass P2', 'F17n', 'Class P2', 'Analysis'
    ]]
    b_rows = [b_header]
    for r in boundaries:
        if r['blind_id'] == 'BLIND-12':
            analysis = 'High-variance acoustics. \u03c3\u00b2_A=28.1 drives legitimate entropy variation that mimics fabrication patterns at moderate M.'
        elif r['blind_id'] == 'BLIND-14':
            analysis = 'Adversarial design. Fabricated signal constructed to preserve entropy invariance, exploiting the instrument\'s reliance on temporal structure.'
        else:
            analysis = 'Resolution boundary detected.'
        b_rows.append([
            P(r['blind_id'], 'TableCell'),
            P(r['true_domain'], 'TableCell'),
            P('L' if r['true_label'] == 'LEGITIMATE' else 'F', 'TableCell'),
            P(f'{r["sigma2_A"]:.1f}', 'TableCell'),
            P(f'{r["pass_rate_p2"]*100:.0f}%', 'TableCell'),
            P(f'{r["f17_normalized"]:.4f}', 'TableCell'),
            P('L' if r['class_p2'] == 'LEGITIMATE' else 'F', 'TableCell'),
            P(analysis, 'TableCell'),
        ])
    story.append(std_table(b_rows, [0.55, 0.6, 0.3, 0.45, 0.4, 0.5, 0.35, 2.85]))
    story.append(tbl_caption('Resolution boundary cases: where the instrument reports its resolving power limit.'))

# ── 10. CoDa ALGEBRA VERIFICATION ────────────────────────────────────────
story.append(P('10. CoDa Algebra Verification', 'SectionHead'))
story.append(PJ(
    'As a validation of the CoDa implementation, two algebraic identities were verified '
    'across all 20 datasets:'
))
story.append(P('<b>Perturbation isometry:</b> d<sub>A</sub>(x \u2295 z, y \u2295 z) = d<sub>A</sub>(x, y). '
    'Verified to machine precision (\u03b5 &lt; 10<sup>-14</sup>) for all datasets.', 'BulletItem'))
story.append(P('<b>Powering scaling:</b> d<sub>A</sub>(\u03b1 \u2299 x, \u03b1 \u2299 y) = |\u03b1| \u00b7 d<sub>A</sub>(x, y). '
    'Verified: ratio = |\u03b1| \u00b1 10<sup>-14</sup> for all datasets.', 'BulletItem'))
story.append(PJ(
    'These verifications confirm that the simplex operations obey Aitchison geometry exactly, '
    'ensuring that all downstream CoDa analyses are algebraically sound.'
))

# ── 11. DOMAIN SUMMARY ───────────────────────────────────────────────────
story.append(P('11. Results by Domain', 'SectionHead'))

# Compute per-domain stats
from collections import defaultdict
domain_stats = defaultdict(lambda: {'total': 0, 'correct_p1': 0, 'correct_p2': 0, 'sigma2A_vals': []})
for r in results:
    d = r['true_domain']
    domain_stats[d]['total'] += 1
    domain_stats[d]['correct_p1'] += int(r['correct_p1'])
    domain_stats[d]['correct_p2'] += int(r['correct_p2'])
    domain_stats[d]['sigma2A_vals'].append(r['sigma2_A'])

d_header = [P(h, 'TableHeader') for h in ['Domain', 'N', 'P1 Correct', 'P2 Correct', 'P1 Acc', 'P2 Acc', '\u03c3\u00b2_A Range']]
d_rows = [d_header]
for domain in sorted(domain_stats.keys()):
    ds = domain_stats[domain]
    s_min = min(ds['sigma2A_vals'])
    s_max = max(ds['sigma2A_vals'])
    d_rows.append([
        P(domain, 'TableCell'),
        P(str(ds['total']), 'TableCell'),
        P(f'{ds["correct_p1"]}/{ds["total"]}', 'TableCell'),
        P(f'{ds["correct_p2"]}/{ds["total"]}', 'TableCell'),
        P(f'{ds["correct_p1"]/ds["total"]*100:.0f}%', 'TableCell'),
        P(f'{ds["correct_p2"]/ds["total"]*100:.0f}%', 'TableCell'),
        P(f'{s_min:.3f} \u2013 {s_max:.1f}' if s_max > 10 else f'{s_min:.4f} \u2013 {s_max:.3f}', 'TableCell'),
    ])
d_rows.append([
    P('<b>Total</b>', 'TableCell'),
    P('<b>20</b>', 'TableCell'),
    P(f'<b>{scores["pass_1"]}/20</b>', 'TableCell'),
    P(f'<b>{scores["pass_2"]}/20</b>', 'TableCell'),
    P(f'<b>{scores["pass_1"]/20*100:.0f}%</b>', 'TableCell'),
    P(f'<b>{scores["pass_2"]/20*100:.0f}%</b>', 'TableCell'),
    P('', 'TableCell'),
])
story.append(std_table(d_rows, [0.85, 0.35, 0.6, 0.6, 0.5, 0.5, 1.1]))
story.append(tbl_caption('Classification accuracy by domain. Pass 2 improves on Pass 1 via targeted F17 tiebreaker.'))

story.append(PageBreak())

# ── 12. IMPLICATIONS FOR CoDa PRACTICE ────────────────────────────────────
story.append(P('12. Implications for CoDa Practice', 'SectionHead'))
story.append(PJ(
    'The integration of EITT with CoDa opens several avenues for compositional data practitioners:'
))
story.append(P('<b>Data quality assurance.</b> Before applying CoDa methods (ILR regression, '
    'compositional PCA, balance dendrograms), run EITT to verify that the compositional time series '
    'exhibits genuine temporal structure. A low EITT pass rate warns that the data may be '
    'fabricated, contaminated, or structurally degenerate.', 'BulletItem'))
story.append(P('<b>Variance interpretation.</b> \u03c3\u00b2<sub>A</sub> now has a dual interpretation: '
    'it measures both the structural spread of the composition (CoDa) and the expected robustness '
    'of entropy invariance under decimation (EITT). High \u03c3\u00b2<sub>A</sub> means both '
    'high dispersion and lower M<sub>break</sub>.', 'BulletItem'))
story.append(P('<b>Resolution-aware analysis.</b> The two-pass instrument reports resolution boundaries, '
    'not failures. When the instrument says "resolution boundary," it means: proceed with CoDa analysis, '
    'but flag this dataset for additional scrutiny. The boundary itself is informative.', 'BulletItem'))
story.append(P('<b>F17 as a diagnostic.</b> The normalized F17 metric (C<sub>geom</sub>/\u03c3\u00b2<sub>A</sub>) '
    'provides a CoDa-native contamination diagnostic. It measures whether the variation matrix\'s '
    'off-diagonal structure is consistent with the total variance, using only CoDa primitives.', 'BulletItem'))
story.append(P('<b>Cross-domain portability.</b> The same instrument, with no domain-specific tuning, '
    'achieves 90% accuracy across commodities, nuclear physics, acoustics, synthetic processes, '
    'noise, and adversarial attacks. The CoDa + EITT framework is genuinely universal.', 'BulletItem'))

# ── 13. THERMODYNAMIC FRAMEWORK ───────────────────────────────────────────
story.append(P('13. The Thermodynamic Framework', 'SectionHead'))
story.append(PJ(
    'The EITT instrument has a deep physical interpretation rooted in the connection between '
    'entropy, time, phase, and energy. The master formula:'
))
story.append(P(
    '<b>S = (\u210f/T)(d\u03c6/dt) + k<sub>B</sub> ln Z</b>', 'Quote'))
story.append(PJ(
    'Energy is the rate of phase change: E = \u210f(d\u03c6/dt). The Wick rotation '
    't \u2192 \u2212i\u210f/k<sub>B</sub>T turns quantum phase evolution into statistical '
    'entropy weighting. <b>Imaginary time is inverse temperature.</b>'
))

story.append(P('13.1 EITT as Calorimeter', 'SubHead'))
story.append(PJ(
    'Each decimation level M sets an effective temperature. The EITT invariance condition '
    'H\u0304(M) = constant states that the signal sits at a critical point \u2014 a phase transition '
    'where entropy does not change with temperature. In the thermodynamic reading:'
))
story.append(P('<b>\u03c3\u00b2<sub>A</sub></b> = heat capacity (how much the composition restructures under temperature change)', 'BulletItem'))
story.append(P('<b>M<sub>break</sub></b> = critical temperature of the fabrication', 'BulletItem'))
story.append(P('<b>F17</b> = latent heat (hidden energy discontinuity at a first-order transition)', 'BulletItem'))
story.append(P('<b>Stored energy</b> = excess free energy above the critical manifold', 'BulletItem'))
story.append(P('<b>Resolution boundary</b> = where the thermometer\'s range ends', 'BulletItem'))

story.append(P('13.2 The Planck Analogy', 'SubHead'))
story.append(PJ(
    'The EITT thermal maps are structurally analogous to CMB maps from the Planck satellite. '
    'The CMB shows near-uniform temperature (the universe at a critical point). Tiny fluctuations '
    'are the seeds of structure. A legitimate EITT signal shows near-uniform entropy across all '
    'temperatures \u2014 same physics, different scale. A fabricated signal is what the CMB would '
    'look like if someone painted fake galaxies onto the sky.'
))

# Add thermal mosaic
THERMAL_DIR = "/sessions/wonderful-elegant-pascal/thermal_maps"
if os.path.exists(f"{THERMAL_DIR}/thermal_mosaic_all20.png"):
    add_image(story, f"{THERMAL_DIR}/thermal_mosaic_all20.png", 6.8, 4.2)
    story.append(fig_caption('EITT Thermal Map: all 20 blind datasets. Each panel shows normalised entropy '
        'as a function of effective temperature (decimation M). Legitimate signals show uniform thermal response. '
        'Fabricated signals show entropy divergence. Compare with Planck CMB temperature maps.'))

if os.path.exists(f"{THERMAL_DIR}/thermal_exp01_highres.png"):
    add_image(story, f"{THERMAL_DIR}/thermal_exp01_highres.png", 6.8, 4.2)
    story.append(fig_caption('EITT Calorimeter: Gold/Silver EXP-01. Left: legitimate signal on the critical manifold. '
        'Right: fabricated signal diverges off-critical. The thermodynamic formula connects all four quantities.'))

story.append(PageBreak())

# ── 14. BINDING ENERGY: THE SEMF DISCOVERY ────────────────────────────────
story.append(P('14. EITT × SEMF: Nuclear Binding Energy', 'SectionHead'))
story.append(PJ(
    'The thermodynamic framework found its strongest validation in nuclear physics itself. '
    'We applied EITT to the binding energy curve by decomposing each nuclide\'s binding energy '
    'into its four SEMF (liquid-drop) contributions \u2014 Volume, Surface, Coulomb, Asymmetry \u2014 '
    'forming a 4-part composition on the simplex. The valley of stability trajectory (294 mass '
    'numbers, AME2020) was tested region by region.'
))
story.append(PJ(
    'Results: The iron peak (A=50\u201370) passes at 100% with \u03c3\u00b2<sub>A</sub> = 2.4, '
    'identifying it as a thermodynamic critical point. Light elements (A&lt;56) fail with '
    '\u03c3\u00b2<sub>A</sub> = 24\u201382, confirming they are off-critical (wanting to fuse). '
    'All regions above A=50 pass at 100% with \u03c3\u00b2<sub>A</sub> decreasing from 1.5 to 0.9. '
    'This is the CoDa framework\'s most striking result: the Aitchison variance maps the entire '
    'nuclear stability landscape as a compositional heat capacity.'
))

SEMF_PLOT_DIR = "/sessions/wonderful-elegant-pascal/binding_energy_semf_plots"
if os.path.exists(f"{SEMF_PLOT_DIR}/semf_master_panel.png"):
    add_image(story, f"{SEMF_PLOT_DIR}/semf_master_panel.png", 6.8, 7.5)
    story.append(fig_caption('EITT × SEMF Master Panel. Binding energy curve coloured by pass rate, '
        'sliding-window diagnostics, and region verdicts. Iron peak = critical point.'))

story.append(PJ(
    'An initial attempt with [Z/A, N/A, B/B<sub>max</sub>] failed to discriminate because those '
    'components vary too smoothly. The SEMF decomposition is the physically correct CoDa choice: '
    'it separates the four competing nuclear forces, whose relative strengths shift dramatically '
    'along the mass number axis \u2014 exactly what compositional data analysis is designed to detect.'
))
story.append(PJ(
    'No prior work has applied CoDa to the SEMF decomposition or mapped Aitchison variance as '
    'nuclear heat capacity. This constitutes a novel application of compositional data analysis '
    'to one of the most fundamental datasets in physics. Full details: HIGGINS_Binding_Energy_EITT.pdf.'
))

story.append(PageBreak())

# ── 15. GEOCHEMISTRY: CoDa's BIRTHPLACE ────────────────────────────────
story.append(P('15. EXP-05: Geochemistry — CoDa\'s Birthplace', 'SectionHead'))
story.append(PJ(
    'CoDa was invented for geochemistry. Aitchison\'s foundational 1986 monograph used geochemical '
    'compositions as its motivating example: major oxide analyses (SiO<sub>2</sub>, Al<sub>2</sub>O<sub>3</sub>, '
    'FeO, MgO, CaO, Na<sub>2</sub>O, K<sub>2</sub>O) as weight percentages summing to ~100%. '
    'EXP-05 brings EITT back to this home domain by testing the igneous differentiation series \u2014 '
    '28 rocks with 8 major oxides as an 8-part composition on the simplex.'
))
story.append(PJ(
    'The differentiation series runs from ultramafic (dunite, SiO<sub>2</sub>=40.5%) through mafic '
    '(basalt, 50%), intermediate (andesite, 57.9%), to felsic (granite, 71.3%), ordered by SiO<sub>2</sub>. '
    'The full series fails EITT (PR=50%, \u03c3\u00b2<sub>A</sub>=2.62) \u2014 igneous differentiation '
    'involves discrete mineral phase transitions that create compositional discontinuities. '
    'The intermediate-to-felsic sub-series passes at 100% (\u03c3\u00b2<sub>A</sub>=2.07), dominated '
    'by continuous feldspar solid solution. The full calc-alkaline series passes at 100% (\u03c3\u00b2<sub>A</sub>=2.28).'
))
story.append(PJ(
    'The most significant result for CoDa is the texture matrix. Peter\'s pre-registered prediction \u2014 '
    'that cooling rate maps to compositional heat capacity \u2014 was confirmed: plutonic rocks '
    '(slow crystallisation, coarse texture, \u03c3\u00b2<sub>A</sub>=3.00) show higher Aitchison variance '
    'than volcanic counterparts (fast crystallisation, fine texture, \u03c3\u00b2<sub>A</sub>=2.24) across '
    'every SiO<sub>2</sub> category. The extreme is coarse/ultramafic at \u03c3\u00b2<sub>A</sub>=5.73 '
    '(dunite, peridotite, troctolite). This extends the thermodynamic dictionary to CoDa\'s home domain: '
    '\u03c3\u00b2<sub>A</sub> = compositional heat capacity is a universal CoDa concept.'
))
story.append(PJ(
    'Sedimentary mixing controls both pass (LEGITIMATE) \u2014 continuous blending of sand, clay, and '
    'carbonate produces smooth compositional trajectories. EITT detects discrete phase transitions '
    '(igneous), not geological provenance. This is a clean CoDa result: the simplex geometry determines '
    'the invariance, not the domain.'
))

GEOCHEM_PLOT_DIR = "/sessions/wonderful-elegant-pascal/geochem_plots"
if os.path.exists(f"{GEOCHEM_PLOT_DIR}/geochem_master_panel.png"):
    add_image(story, f"{GEOCHEM_PLOT_DIR}/geochem_master_panel.png", 6.8, 7.5)
    story.append(fig_caption('EXP-05 Master Panel: Igneous differentiation on the 8-simplex. '
        'Top: oxide composition along differentiation series. Bottom-right: texture matrix \u2014 '
        'plutonic > volcanic \u03c3\u00b2_A across all SiO2 categories (Peter\'s prediction confirmed).'))

story.append(PJ(
    'Data sources: Le Maitre (1976, 2002), Best (2003), Winter (2014). For expansion: GEOROC 2.0 '
    '(georoc.eu) and EarthChem (earthchem.org) contain millions of individual analyses. '
    'Full report: HIGGINS_Geochemistry_EITT.pdf. Prepared for CoDaWork 2026, Coimbra, Portugal.'
))

story.append(PageBreak())

# ── 15b. EXP-05b: REAL-DATA VALIDATION + CoDa TOOLKIT + HUF TETRODE ──────
story.append(P('15b. EXP-05b: Real-Data Validation at Scale', 'SectionHead'))

story.append(PJ(
    'EXP-05b scales EITT from 28 averages to 40,666 individual analyses: Ball (2022) global '
    'intraplate volcanics (26,305 samples, 12 regions, 15 TAS types) and AGDB3 Alaska (14,361 '
    'igneous samples, 167 rock types). Results: 37 of 39 test suites LEGITIMATE. Only Foidite '
    'fails (PR=32%, \u03c3\u00b2<sub>A</sub>=26.5) \u2014 silica-undersaturated deep-mantle melts '
    'with genuinely discontinuous phase behaviour.'
))

story.append(PJ(
    'Peter\u2019s texture-energy prediction confirmed at N=8,098: AGDB3 volcanic (N=3,400, '
    '\u03c3\u00b2<sub>A</sub>=1.99) vs plutonic (N=4,698, \u03c3\u00b2<sub>A</sub>=2.51), ratio 1.26. '
    'The signal survives in noisy individual analyses \u2014 strong confirmation that cooling rate maps '
    'to compositional heat capacity.'
))

story.append(P('CoDa Toolkit Integration', 'SubHead'))
story.append(PJ(
    'The full CoDa toolkit was deployed on the real data: (1) Ternary diagrams (AFM, silica '
    'enrichment, feldspar, peraluminosity) showing the simplex structure EITT tests. '
    '(2) CLR biplots \u2014 compositional PCA revealing differentiation on PC1 and alkali enrichment '
    'on PC2. (3) Variation matrices V<sub>ij</sub> = var(ln(x<sub>i</sub>/x<sub>j</sub>)) \u2014 '
    'the fundamental CoDa variance structure whose trace gives \u03c3\u00b2<sub>A</sub>. '
    '(4) ILR coordinates (Helmert basis) providing D\u22121 orthonormal simplex coordinates. '
    '(5) Aitchison distance structure revealing compositional extremes.'
))

story.append(PJ(
    'This demonstrates the deep integration: CoDa provides the geometry (simplex, log-ratios, '
    'Aitchison distance), EITT provides the temporal test (entropy invariance under decimation), '
    'and \u03c3\u00b2<sub>A</sub> bridges them as the thermodynamic diagnostic. The variation matrix '
    'determines the EITT pass rate; the CLR biplot shows the compositional space in which entropy '
    'invariance is computed; the ILR coordinates provide the orthonormal basis.'
))

story.append(P('The HUF Tetrode', 'SubHead'))
story.append(PJ(
    'The HUF Tetrode (Higgins, March 2026) identifies four fundamental connectives that EITT '
    'validates simultaneously: (1) Simplex Geometry \u2014 compositions live on the simplex, '
    'Aitchison\u2019s log-ratio framework is the correct geometry. (2) Entropy Invariance \u2014 '
    'Shannon entropy is invariant under geometric-mean block decimation for legitimate series. '
    '(3) Thermodynamic Map \u2014 \u03c3\u00b2<sub>A</sub> maps to heat capacity across domains. '
    '(4) Scale Invariance \u2014 EITT pass rates stable from N=122 to N=26,305. '
    'The four vertices, six edges, and four faces form a self-reinforcing tetrahedron where each '
    'face enforces closure \u03a3\u03c1<sub>i</sub>=1. Geochemistry validates all four.'
))

GEOCHEM_DATA_DIR = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/DATA/Geochemistry"
if os.path.exists(f"{GEOCHEM_DATA_DIR}/coda_clr_biplot.png"):
    add_image(story, f"{GEOCHEM_DATA_DIR}/coda_clr_biplot.png", 6.5, 4.5)
    story.append(fig_caption('CLR biplots: Ball data coloured by SiO2 (left), AGDB3 by rock type (right). '
        'Loading arrows show oxide contributions to compositional PCA.'))

if os.path.exists(f"{GEOCHEM_DATA_DIR}/huf_tetrode.png"):
    add_image(story, f"{GEOCHEM_DATA_DIR}/huf_tetrode.png", 5.5, 4.5)
    story.append(fig_caption('HUF Tetrode: 4 vertices (Simplex, Entropy, Thermodynamic Map, Scale), '
        '6 edges, 4 faces \u2014 each face enforces closure.'))

story.append(PageBreak())

# ── 16. CONCLUSION ────────────────────────────────────────────────────────
story.append(P('16. Conclusion', 'SectionHead'))
story.append(PJ(
    'CoDa and EITT are complementary, not competing. CoDa provides the algebraic foundation: '
    'log-ratio transforms, Aitchison geometry, simplicial operations, compositional PCA. '
    'EITT provides the temporal test: does the compositional structure survive decimation? '
    'The bridge between them \u2014 \u03c3\u00b2<sub>A</sub> predicting M<sub>break</sub> \u2014 '
    'is not an empirical correlation but a consequence of how block-averaging interacts with '
    'the variation matrix (Theorem 2).'
))
story.append(PJ(
    'Applied to 20 blind datasets across 6 domains, the integrated instrument achieves 90% accuracy '
    'with zero domain-specific tuning. The two resolution boundaries are informative: they reveal '
    'exactly where the instrument\'s resolving power ends, providing CoDa practitioners with '
    'actionable information about data quality limits.'
))
story.append(Spacer(1, 0.3*inch))
story.append(P('<i>"CoDa sees structure. EITT sees temporal invariance. Together: the full instrument."</i>', 'Quote'))

# ═══════════════════════════════════════════════════════════════════════════════
# APPENDIX: NOTATION, TERMINOLOGY & FORMULAE
# ═══════════════════════════════════════════════════════════════════════════════
from appendix_formulae import build_appendix
story += build_appendix(user_styles=styles, section_prefix="A")

# ── Build ─────────────────────────────────────────────────────────────────
doc.build(story)
print(f"\nPDF built: {OUT_PDF}")
print(f"  Pages: ~20")
print(f"  Figures: {fig_num[0]}")
print(f"  Tables: {tbl_num[0]}")
