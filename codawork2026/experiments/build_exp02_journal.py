#!/usr/bin/env python3
"""
EXP-02 Journal Builder — Official PDF
Full process-line results + linear contamination tuner finding.
"""

import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, KeepTogether)

# Load results
with open("/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/DATA/Energy/EXP02_process_line_results.json") as f:
    results = json.load(f)
with open("/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/DATA/Energy/EXP02_quadratic_tuner.json") as f:
    tuner = json.load(f)

OUT = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/EXP-02_US_Monthly_EITT_Journal.pdf"

# ═══════════════════════════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════════════════════════

styles = getSampleStyleSheet()

styles.add(ParagraphStyle('JournalTitle', parent=styles['Title'],
    fontSize=18, spaceAfter=6, textColor=HexColor('#1a1a2e')))
styles.add(ParagraphStyle('JournalSubtitle', parent=styles['Normal'],
    fontSize=11, alignment=TA_CENTER, textColor=HexColor('#555555'),
    spaceAfter=20))
styles.add(ParagraphStyle('SectionHead', parent=styles['Heading1'],
    fontSize=13, textColor=HexColor('#16213e'), spaceBefore=16, spaceAfter=8,
    borderWidth=0, borderPadding=0))
styles.add(ParagraphStyle('SubHead', parent=styles['Heading2'],
    fontSize=11, textColor=HexColor('#0f3460'), spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=9.5, leading=13, alignment=TA_JUSTIFY, spaceAfter=6))
styles.add(ParagraphStyle('SmallBody', parent=styles['Normal'],
    fontSize=8.5, leading=11, alignment=TA_JUSTIFY, spaceAfter=4))
styles.add(ParagraphStyle('CodeBlock', parent=styles['Normal'],
    fontName='Courier', fontSize=8, leading=10, spaceAfter=4,
    leftIndent=12, textColor=HexColor('#333333')))
styles.add(ParagraphStyle('Finding', parent=styles['Normal'],
    fontSize=9.5, leading=13, alignment=TA_JUSTIFY, spaceAfter=6,
    leftIndent=18, rightIndent=18, backColor=HexColor('#f0f4f8'),
    borderPadding=6))
styles.add(ParagraphStyle('CaptionStyle', parent=styles['Normal'],
    fontSize=8, alignment=TA_CENTER, textColor=HexColor('#666666'),
    spaceAfter=8, spaceBefore=4))
styles.add(ParagraphStyle('FooterStyle', parent=styles['Normal'],
    fontSize=7, alignment=TA_CENTER, textColor=HexColor('#999999')))

BLUE = HexColor('#16213e')
LIGHT_BLUE = HexColor('#e8edf2')
HEADER_BG = HexColor('#1a1a2e')
PASS_GREEN = HexColor('#d4edda')
FAIL_RED = HexColor('#f8d7da')
WARN_YELLOW = HexColor('#fff3cd')

def make_table(data, col_widths=None, header=True):
    """Build a styled table."""
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('LEADING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]
    if header:
        style_cmds += [
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7.5),
        ]
    # Alternate row coloring
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), LIGHT_BLUE))
    t.setStyle(TableStyle(style_cmds))
    return t

# ═══════════════════════════════════════════════════════════════════════
# BUILD DOCUMENT
# ═══════════════════════════════════════════════════════════════════════

doc = SimpleDocTemplate(OUT, pagesize=letter,
    topMargin=0.7*inch, bottomMargin=0.7*inch,
    leftMargin=0.75*inch, rightMargin=0.75*inch)

story = []

# ── TITLE PAGE ──
story.append(Spacer(1, 60))
story.append(Paragraph("EXP-02: EITT on US Monthly Energy Compositions", styles['JournalTitle']))
story.append(Paragraph("9-Carrier Electricity Generation Simplex | D = 9 | N = 300", styles['JournalSubtitle']))
story.append(Paragraph("Higgins Iterative Validation Protocol (HIVP) Chain: EXP-01 &#8594; EXP-02", styles['JournalSubtitle']))
story.append(Paragraph(f"P. Higgins | {datetime.now().strftime('%B %d, %Y')}", styles['JournalSubtitle']))
story.append(Spacer(1, 20))

story.append(Paragraph("<b>Abstract.</b> This journal documents the second experiment in the EITT validation chain. "
    "EXP-02 applies the Entropy-Invariant Time Transformer to US monthly electricity generation data across "
    "10 states organized into interior (4), bridge (2), and boundary (4) cohorts. The 9-carrier simplex "
    "(Coal, Gas, Nuclear, Hydro, Solar, Wind, Bioenergy, Other Fossil, Other Renewables) tests EITT at "
    "D = 9 with 300 monthly observations decimated at M = 2, 3, 4, 6, 12. All four interior states pass "
    "at the 1% threshold. A new finding emerges: the geometric-arithmetic gap follows a linear-with-saturation "
    "pattern in M, providing a built-in contamination meter that measures near-vertex stress without "
    "modifying the core EITT observable. This linear contamination tuner is formalized as instrument F17.", styles['Body']))

story.append(Spacer(1, 12))

# TOC
story.append(Paragraph("Contents", styles['SectionHead']))
toc_items = [
    "1. Experiment Design and Data",
    "2. Cohort Comparison Summary",
    "3. Interior Cohort: Per-M Decimation Tables",
    "4. Bridge and Boundary Results",
    "5. Arithmetic Comparator: Geometric vs Arithmetic",
    "6. The Linear Contamination Tuner (F17)",
    "7. Pennsylvania Deep Dive: The Orthogonal Peak",
    "8. Stagewise RMSE and Fault Transparency",
    "9. Operating Envelope and Companion Diagnostics",
    "10. HIVP Regression Check",
    "11. Conclusions and Next Steps",
    "Appendix A: Full Formula Catalog (F1\u2013F17)",
]
for item in toc_items:
    story.append(Paragraph(item, styles['SmallBody']))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# SECTION 1: EXPERIMENT DESIGN
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("1. Experiment Design and Data", styles['SectionHead']))
story.append(Paragraph(
    "EXP-02 extends the EITT validation chain from EXP-01's gold/silver 2-simplex (D = 2, N = 624) to "
    "real-world energy compositions at D = 9. The source is EMBER's US monthly electricity generation "
    "dataset (CC BY 4.0), filtered to the 9-carrier fuel breakdown in percentage shares. Each state "
    "provides N = 300 monthly observations from January 2001 to December 2025.", styles['Body']))

story.append(Paragraph(
    "Cohort selection follows the EXP-02 Formal Ranked Selection Memo, which defines exact gates for "
    "interior, bridge, and boundary cases based on mean entropy, dominant-share concentration, zero-share "
    "rate, and compositional velocity. Interior cases are diversified states far from the simplex boundary. "
    "Bridge cases sit near the 1% threshold. Boundary cases are concentrated, sparse, or volatile compositions "
    "expected to stress or break EITT.", styles['Body']))

# Design table
design_data = [
    ['Parameter', 'Value'],
    ['Source', 'us_monthly_full_release_long_format.csv (EMBER)'],
    ['D (components)', '9 fuel carriers'],
    ['N (observations)', '300 months per state (2001-01 to 2025-12)'],
    ['M tested', '2, 3, 4, 6, 12'],
    ['Pass threshold', '1% relative entropy change at all M'],
    ['Zero policy', 'Multiplicative replacement, epsilon = 10^-6'],
    ['Mapping', 'f(r) = r (identity), close to simplex'],
    ['Interior cohort', 'California, Minnesota, Texas, Wisconsin'],
    ['Bridge cohort', 'Pennsylvania, North Carolina'],
    ['Boundary cohort', 'Rhode Island, West Virginia, Wyoming, Delaware'],
]
story.append(make_table(design_data, col_widths=[130, 340]))
story.append(Paragraph("Table 1. EXP-02 experiment design parameters.", styles['CaptionStyle']))

# ══════════════════════════════════════════════════════════════════
# SECTION 2: COHORT COMPARISON SUMMARY
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("2. Cohort Comparison Summary", styles['SectionHead']))
story.append(Paragraph(
    "The cohort comparison table below presents the primary EITT output alongside companion diagnostics "
    "for all 10 entities. The interior cohort passes unanimously. Pennsylvania (bridge) fails at M = 12 "
    "only. All boundary states fail at multiple M values.", styles['Body']))

# Build comparison table
comp_header = ['State', 'Band', 'N', 'H_bar(1)', 'max rel%', 'RMS rel%',
               'Gamma', 'delta min', 'mean v', 'eta', 'Verdict']
comp_rows = [comp_header]

order = ['California', 'Minnesota', 'Texas', 'Wisconsin',
         'Pennsylvania', 'North Carolina',
         'Rhode Island', 'West Virginia', 'Wyoming', 'Delaware']
bands = {'California': 'interior', 'Minnesota': 'interior', 'Texas': 'interior',
         'Wisconsin': 'interior', 'Pennsylvania': 'bridge', 'North Carolina': 'bridge',
         'Rhode Island': 'boundary', 'West Virginia': 'boundary',
         'Wyoming': 'boundary', 'Delaware': 'boundary'}

for state in order:
    r = results['cohort_results'][state]
    s = r['S7_aggregate']
    env = r['S11_envelope']
    n3 = r['S3_native']
    geo = r['S4_S5_geometry']
    comp_rows.append([
        state, bands[state], str(r['S0_identity']['N']),
        f"{s['H_bar_1']:.4f}", f"{s['max_relative_change']*100:.3f}%",
        f"{s['RMS_rel']*100:.4f}%", f"{env['Gamma_M2']:.0f}",
        f"{n3['delta_min']:.1e}", f"{geo['mean_velocity']:.3f}",
        f"{geo['trajectory_efficiency']:.4f}", env['verdict'],
    ])

t = make_table(comp_rows, col_widths=[72, 45, 25, 42, 42, 45, 48, 42, 36, 36, 37])
# Color verdict cells
for i, row in enumerate(comp_rows[1:], start=1):
    color = PASS_GREEN if row[-1] == 'PASS' else FAIL_RED
    t.setStyle(TableStyle([('BACKGROUND', (-1, i), (-1, i), color)]))
story.append(t)
story.append(Paragraph("Table 2. Cohort comparison summary. Gamma is computed at M = 2. "
    "All delta_min values are at the zero-replacement floor (10<super>-6</super>).", styles['CaptionStyle']))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# SECTION 3: INTERIOR COHORT PER-M TABLES
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("3. Interior Cohort: Per-M Decimation Tables", styles['SectionHead']))
story.append(Paragraph(
    "All four interior states pass at every tested M. The maximum relative entropy change is California "
    "at M = 12 (0.829%), with 17 basis points of headroom below the 1% threshold. Texas is the strongest "
    "performer (max 0.208%). SNR remains below 2 at all stations, meaning all EITT deltas are below the "
    "statistical noise floor \u2014 the same pattern observed at D = 2 in EXP-01.", styles['Body']))

for state in ['California', 'Minnesota', 'Texas', 'Wisconsin']:
    r = results['cohort_results'][state]
    story.append(Paragraph(f"<b>{state}</b> \u2014 H_bar(1) = {r['S7_aggregate']['H_bar_1']:.6f}, "
        f"sigma_A<super>2</super> = {r['S4_S5_geometry']['sigma_A_squared']:.4f}, "
        f"verdict: {r['S11_envelope']['verdict']}", styles['SubHead']))

    pm_header = ['M', 'blocks', 'delta_M', 'rel %', 'SE(M)', 'SNR', 'ETF', 'phase RMSE', 'pass']
    pm_rows = [pm_header]
    for e in r['S7_per_M']:
        lp = '*' if e['low_power'] else ''
        pm_rows.append([
            str(e['M']), f"{e['n_blocks']}{lp}",
            f"{e['delta_M']:.6f}", f"{e['relative_M']*100:.3f}%",
            f"{e['SE_M']:.6f}", f"{e['SNR_M']:.4f}",
            f"{e['ETF_M']:.2e}", f"{e['phase_RMSE_M']:.6f}",
            'PASS' if e['pass'] else 'FAIL',
        ])
    pt = make_table(pm_rows, col_widths=[28, 38, 62, 42, 58, 42, 48, 62, 32])
    for i, row in enumerate(pm_rows[1:], start=1):
        color = PASS_GREEN if row[-1] == 'PASS' else FAIL_RED
        pt.setStyle(TableStyle([('BACKGROUND', (-1, i), (-1, i), color)]))
    story.append(pt)
    story.append(Spacer(1, 6))

story.append(Paragraph("Table 3. Per-M decimation results for the interior cohort. "
    "* marks low-power blocks (N/M < 10). ETF near zero indicates the Hessian bound is "
    "meaninglessly loose at D = 9 with zero-replaced compositions.", styles['CaptionStyle']))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# SECTION 4: BRIDGE AND BOUNDARY
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("4. Bridge and Boundary Results", styles['SectionHead']))

story.append(Paragraph("<b>Pennsylvania (bridge, FAIL)</b> fails only at M = 12 (1.092%). "
    "At M = 2 through M = 6, all decimation levels pass. This is the most informative "
    "result in EXP-02: it pinpoints monthly-to-annual compression as the stress threshold "
    "for a moderately concentrated state.", styles['Body']))

story.append(Paragraph("<b>North Carolina (bridge, PASS)</b> passes at all M despite higher "
    "compositional velocity (1.28) and higher zero-share rate than some interior states. "
    "Its passage suggests that velocity alone does not determine failure.", styles['Body']))

story.append(Paragraph("<b>Boundary cohort</b> fails clearly and progressively. Rhode Island "
    "(8.78% at M = 12) is dominated by gas at 93.7% average share. Delaware fails even at "
    "M = 2 (1.40%) due to extreme sparsity and velocity. These cases define the operating "
    "envelope boundary.", styles['Body']))

# Bridge per-M table
for state in ['Pennsylvania', 'North Carolina']:
    r = results['cohort_results'][state]
    story.append(Paragraph(f"<b>{state}</b> \u2014 verdict: {r['S11_envelope']['verdict']}", styles['SubHead']))
    pm_header = ['M', 'blocks', 'delta_M', 'rel %', 'SNR', 'pass']
    pm_rows = [pm_header]
    for e in r['S7_per_M']:
        pm_rows.append([
            str(e['M']), str(e['n_blocks']),
            f"{e['delta_M']:.6f}", f"{e['relative_M']*100:.3f}%",
            f"{e['SNR_M']:.4f}", 'PASS' if e['pass'] else 'FAIL',
        ])
    pt = make_table(pm_rows, col_widths=[35, 45, 75, 55, 55, 40])
    for i, row in enumerate(pm_rows[1:], start=1):
        color = PASS_GREEN if row[-1] == 'PASS' else FAIL_RED
        pt.setStyle(TableStyle([('BACKGROUND', (-1, i), (-1, i), color)]))
    story.append(pt)
    story.append(Spacer(1, 6))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# SECTION 5: ARITHMETIC COMPARATOR
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("5. Arithmetic Comparator: Geometric vs Arithmetic", styles['SectionHead']))
story.append(Paragraph(
    "Every entity was processed through both geometric-mean and arithmetic-mean decimation. "
    "The arithmetic-mean path serves as a diagnostic comparator only \u2014 it is not CoDa-compliant "
    "and is not part of the EITT instrument. Its purpose is to reveal the specific contribution "
    "of the geometric mean's log-space averaging.", styles['Body']))

story.append(Paragraph(
    "Key finding: at M = 12, geometric-mean EITT passes for all interior states while "
    "arithmetic-mean EITT fails for California (1.38%) and Minnesota (1.41%). This confirms "
    "the geometric mean is the correct CoDa aggregator \u2014 it preserves entropy invariance "
    "where the arithmetic mean does not. However, the arithmetic comparator also reveals a "
    "universal pattern: the geometric mean always sees <i>more</i> entropy loss than the arithmetic "
    "mean. This observation leads directly to the linear contamination tuner.", styles['Body']))

# Geom vs Arith comparison at M=12
ga_header = ['State', 'Band', 'Geom delta', 'Geom rel%', 'Geom', 'Arith delta', 'Arith rel%', 'Arith']
ga_rows = [ga_header]
for state in order:
    r = results['cohort_results'][state]
    geom_12 = [e for e in r['S7_per_M'] if e['M'] == 12]
    arith_12 = [e for e in r['arithmetic_comparator'] if e['M'] == 12]
    if geom_12 and arith_12:
        g = geom_12[0]
        a = arith_12[0]
        ga_rows.append([
            state, bands[state],
            f"{g['delta_M']:.6f}", f"{g['relative_M']*100:.3f}%",
            'PASS' if g['pass'] else 'FAIL',
            f"{a['delta_M_arith']:.6f}", f"{a['relative_M_arith']*100:.3f}%",
            'PASS' if a['pass_arith'] else 'FAIL',
        ])

gt = make_table(ga_rows, col_widths=[72, 48, 56, 48, 34, 56, 48, 34])
for i, row in enumerate(ga_rows[1:], start=1):
    gt.setStyle(TableStyle([
        ('BACKGROUND', (4, i), (4, i), PASS_GREEN if row[4] == 'PASS' else FAIL_RED),
        ('BACKGROUND', (7, i), (7, i), PASS_GREEN if row[7] == 'PASS' else FAIL_RED),
    ]))
story.append(gt)
story.append(Paragraph("Table 4. Geometric vs arithmetic EITT at M = 12. "
    "Interior states: geometric passes, arithmetic fails for CA and MN. "
    "Pennsylvania: geometric fails, arithmetic passes \u2014 the crossover case.", styles['CaptionStyle']))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# SECTION 6: THE LINEAR CONTAMINATION TUNER (F17)
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("6. The Linear Contamination Tuner (F17)", styles['SectionHead']))

story.append(Paragraph(
    "The most significant methodological finding in EXP-02 is the discovery that the geometric-arithmetic "
    "gap provides a built-in contamination meter. Define:", styles['Body']))

story.append(Paragraph("gap(M) = |delta<sub>M</sub><super>geom</super> - delta<sub>M</sub><super>arith</super>|",
    styles['CodeBlock']))
story.append(Paragraph("C<sub>geom</sub>(M) = gap(M) / H_bar(1)  [relative contamination]", styles['CodeBlock']))

story.append(Paragraph(
    "The gap grows monotonically with M for all 10 entities (50/50 measurements). Fitting "
    "gap(M) = aM<super>2</super> + bM + c reveals that the quadratic coefficient a is <b>negative</b> "
    "for every entity, meaning the gap grows linearly with saturation. The dominant term is the "
    "linear coefficient b. R<super>2</super> exceeds 0.96 in all cases.", styles['Body']))

story.append(Paragraph(
    "This means the decomposition engine has a built-in governor: the geometric mean's log-space "
    "stress is self-limiting, not runaway. The tool saturates before it explodes.", styles['Finding']))

story.append(Paragraph(
    "The signed gap is negative for all 50 measurements: geometric decimation always sees <i>more</i> "
    "entropy loss than arithmetic. This is the Hessian effect made visible \u2014 the second-order "
    "curvature of entropy on the simplex systematically pulls the geometric mean toward the vertex.", styles['Body']))

story.append(Paragraph("<b>Formal definition of F17:</b>", styles['SubHead']))
story.append(Paragraph(
    "F17 (Linear Contamination Tuner): C<sub>geom</sub>(M) = |delta<sub>M</sub><super>geom</super> - "
    "delta<sub>M</sub><super>arith</super>| / H_bar(1). Report for every tested M. "
    "The linear growth rate b of C<sub>geom</sub>(M) across M is the sensitivity dial. "
    "C<sub>geom</sub> &lt; 0.5% = clean. C<sub>geom</sub> 0.5\u20131% = monitor. "
    "C<sub>geom</sub> &gt; 1% = investigate. C<sub>geom</sub> &gt; 2% = geometric mean is under material stress.",
    styles['Body']))

story.append(Paragraph(
    "<b>Critical constraint:</b> F17 does NOT modify the EITT reading. It tells you when to "
    "distrust it. The tuner operates at the process-control layer, not the science layer. "
    "This preserves the gold-standard hierarchy: EITT is the science, the contamination meter "
    "is the honesty layer.", styles['Finding']))

# C_geom table
cg_header = ['State', 'Band', 'C M=2', 'C M=3', 'C M=4', 'C M=6', 'C M=12', 'Max C']
cg_rows = [cg_header]
M_VALUES = [2, 3, 4, 6, 12]
for state in order:
    d = tuner['per_entity'][state]
    H = d['H_bar']
    gaps = d['gaps']
    cvals = []
    row = [state, bands[state]]
    for g in gaps:
        if g is not None and H > 0:
            c = g / H * 100
            cvals.append(c)
            row.append(f"{c:.3f}%")
        else:
            row.append('N/A')
    row.append(f"{max(cvals):.3f}%" if cvals else 'N/A')
    cg_rows.append(row)

ct = make_table(cg_rows, col_widths=[72, 48, 48, 48, 48, 48, 48, 48])
for i, row in enumerate(cg_rows[1:], start=1):
    # Color max C column
    try:
        val = float(row[-1].replace('%', ''))
        if val < 0.5:
            color = PASS_GREEN
        elif val < 1.0:
            color = WARN_YELLOW
        elif val < 2.0:
            color = HexColor('#ffe0b2')
        else:
            color = FAIL_RED
        ct.setStyle(TableStyle([('BACKGROUND', (-1, i), (-1, i), color)]))
    except:
        pass
story.append(ct)
story.append(Paragraph("Table 5. Relative contamination C<sub>geom</sub>(M) = gap(M) / H_bar(1) for all entities. "
    "Green &lt; 0.5%, yellow 0.5\u20131%, orange 1\u20132%, red &gt; 2%.", styles['CaptionStyle']))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# SECTION 7: PENNSYLVANIA DEEP DIVE
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("7. Pennsylvania Deep Dive: The Orthogonal Peak", styles['SectionHead']))

story.append(Paragraph(
    "Pennsylvania is the first case where geometric EITT fails (1.092%) while arithmetic EITT passes "
    "(0.872%) at the same M. The deltas move in <i>opposite directions</i>: geometric delta = -0.01227 "
    "(entropy drops) vs arithmetic delta = +0.00979 (entropy rises). This crossover reveals the mechanism.", styles['Body']))

story.append(Paragraph(
    "At M = 12, an entire annual cycle is compressed into a single block. If any month has a "
    "near-zero carrier, log(10<super>-6</super>) = -13.8 pulls the geometric mean hard toward the "
    "simplex vertex. The arithmetic mean simply averages the small value linearly and barely notices. "
    "This is the 'fast sensitive peak' \u2014 a single month's near-zero component acts as an orthogonal "
    "impulse in log-space that the geometric mean amplifies but the arithmetic mean ignores.", styles['Body']))

story.append(Paragraph(
    "Pennsylvania's characteristics make it the ideal detector for this effect: zero-share rate 9.6%, "
    "mean velocity 1.36 (the highest in the bridge cohort), and a dominant-share average of 49.4%. "
    "The high velocity means the energy mix changes fast, and the fluctuating near-zero carriers "
    "create the log-space impulses.", styles['Body']))

story.append(Paragraph(
    "<b>Implication:</b> The geometric-arithmetic crossover at M = 12 is not a failure of EITT theory. "
    "It is a success of the contamination meter. C<sub>geom</sub> = 1.964% at M = 12 for Pennsylvania "
    "correctly flags that the geometric mean is under material stress. The F17 tuner would have "
    "recommended investigation before the verdict was issued.", styles['Finding']))

# ══════════════════════════════════════════════════════════════════
# SECTION 8: STAGEWISE RMSE AND FAULTS
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("8. Stagewise RMSE and Fault Transparency", styles['SectionHead']))

story.append(Paragraph(
    "Per the process-control specification, every stage exposes local gauges and fault modes. "
    "The stagewise RMSE register for the interior cohort is summarized below.", styles['Body']))

rmse_header = ['Metric', 'California', 'Minnesota', 'Texas', 'Wisconsin']
rmse_rows = [rmse_header]
metrics = ['RMSE_closure', 'RMSE_dec_clr_mean', 'RMSE_phase_mean', 'RMSE_phase_max',
           'RMSE_delta_H', 'RMS_rel', 'RMS_SNR', 'RMS_ETF']
labels = ['RMSE closure', 'RMSE dec_clr (mean)', 'RMSE phase (mean)', 'RMSE phase (max)',
          'RMS delta_H (F13)', 'RMS rel (F14)', 'RMS SNR (F15)', 'RMS ETF (F16)']

for label, metric in zip(labels, metrics):
    row = [label]
    for state in ['California', 'Minnesota', 'Texas', 'Wisconsin']:
        val = results['cohort_results'][state]['stagewise_RMSE'].get(metric)
        if val is not None and isinstance(val, (int, float)):
            if abs(val) < 0.001:
                row.append(f"{val:.2e}")
            else:
                row.append(f"{val:.6f}")
        else:
            row.append(str(val) if val else 'N/A')
    rmse_rows.append(row)

story.append(make_table(rmse_rows, col_widths=[100, 85, 85, 85, 85]))
story.append(Paragraph("Table 6. Stagewise RMSE register for interior cohort.", styles['CaptionStyle']))

# Fault summary
story.append(Paragraph("<b>Common faults across all entities:</b>", styles['SubHead']))
story.append(Paragraph(
    "<b>S4 CAUTION \u2014 delta below 0.01:</b> Every entity has delta_min at the zero-replacement "
    "floor (10<super>-6</super>). This is the binding fault for the entire EXP-02 run. It means the "
    "Hessian bound is meaninglessly loose (ETF near 0) and Gamma is extremely large. The delta altimeter "
    "reads at the tool floor, not the data floor. Zero-handling is the dominant contamination source.", styles['SmallBody']))
story.append(Paragraph(
    "<b>S8 INFO \u2014 sub-noise-floor:</b> All EITT deltas are below the statistical noise floor "
    "(max SNR &lt; 1.3 across all entities). The tool detects invariance but cannot statistically "
    "distinguish signal from noise. Binding constraint: detectability for interior cases, "
    "threshold for boundary cases.", styles['SmallBody']))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# SECTION 9: OPERATING ENVELOPE
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("9. Operating Envelope and Companion Diagnostics", styles['SectionHead']))

env_header = ['State', 'Band', 'Gamma (M=2)', 'Binding', 'Hard flags', 'Soft flags']
env_rows = [env_header]
for state in order:
    r = results['cohort_results'][state]
    env = r['S11_envelope']
    soft = '; '.join(env['soft_flags'][:2]) if env['soft_flags'] else 'none'
    hard = '; '.join(env['hard_flags']) if env['hard_flags'] else 'none'
    env_rows.append([
        state, bands[state], f"{env['Gamma_M2']:.0f}",
        env['binding_constraint'], hard, soft[:50],
    ])

story.append(make_table(env_rows, col_widths=[70, 45, 55, 68, 55, 160]))
story.append(Paragraph("Table 7. Operating envelope summary.", styles['CaptionStyle']))

story.append(Paragraph(
    "Companion diagnostics are reported separately per the four-instrument architecture: "
    "EITT (thermometer), velocity (compass), delta (altimeter), trajectory efficiency (GPS). "
    "The velocity scope shows Pennsylvania and Delaware as the highest-motion states, "
    "while trajectory efficiency is below 0.07 for all entities, indicating oscillatory rather "
    "than directional compositional change.", styles['Body']))

# ══════════════════════════════════════════════════════════════════
# SECTION 10: HIVP REGRESSION
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("10. HIVP Regression Check", styles['SectionHead']))

story.append(Paragraph(
    "The Higgins Iterative Validation Protocol requires that every modification be regressed through "
    "all prior DUTs before advancement. EXP-02 introduces one new candidate formula:", styles['Body']))

story.append(Paragraph(
    "F17 (Linear Contamination Tuner): measures the geometric-arithmetic gap as a process-control "
    "signal. This formula does not modify the core EITT observable (F2\u2013F4). It adds a monitoring "
    "instrument at the process-control layer.", styles['Body']))

story.append(Paragraph("<b>Regression status:</b>", styles['SubHead']))

reg_data = [
    ['DUT', 'D', 'N', 'Core EITT', 'F17 status', 'Chain'],
    ['EXP-01 Gold/Silver', '2', '624', 'PASS (0.60%)',
     'Pending: re-run with F17', 'EXP-01 passed'],
    ['EXP-02 Interior', '9', '300', 'PASS (max 0.83%)',
     'C_geom < 1.06%', 'EXP-01 -> EXP-02 passed'],
    ['EXP-02 Bridge (PA)', '9', '300', 'FAIL (1.09%)',
     'C_geom = 1.96% (flagged)', 'Bridge case, expected'],
    ['EXP-02 Boundary', '9', '300', 'FAIL (2.8-8.8%)',
     'C_geom = 4.7-14.0% (flagged)', 'Boundary case, expected'],
]
story.append(make_table(reg_data, col_widths=[88, 22, 28, 80, 105, 105]))
story.append(Paragraph("Table 8. HIVP regression chain status. F17 is candidate \u2014 must be regressed through EXP-01.", styles['CaptionStyle']))

story.append(Paragraph(
    "No modifications to F1\u2013F12 were required for EXP-02. The same pipeline that passed EXP-01 "
    "at D = 2 passes EXP-02 at D = 9 for interior compositions. F17 is a new addition that must be "
    "confirmed on EXP-01 before promotion to canonical status. The re-run of EXP-01 with F17 is the "
    "next mandatory step.", styles['Body']))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# SECTION 11: CONCLUSIONS
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("11. Conclusions and Next Steps", styles['SectionHead']))

story.append(Paragraph("<b>Primary conclusions:</b>", styles['SubHead']))
story.append(Paragraph(
    "1. EITT passes at D = 9 for diversified US energy compositions. The 1% threshold holds for all "
    "interior states across all tested decimation levels (M = 2 through 12). The HIVP chain extends "
    "from EXP-01 (D = 2) to EXP-02 (D = 9) without modification to the core formulas.", styles['Body']))
story.append(Paragraph(
    "2. The geometric mean is confirmed as the correct CoDa aggregator. It preserves entropy invariance "
    "where the arithmetic mean fails (California and Minnesota at M = 12).", styles['Body']))
story.append(Paragraph(
    "3. The geometric-arithmetic gap provides a built-in contamination meter (F17). The gap grows "
    "linearly with saturation in M, meaning the tool has a self-limiting governor. C_geom cleanly "
    "separates interior (&lt; 1.06%), bridge (1.5\u20132.0%), and boundary (&gt; 4.7%) behavior.", styles['Body']))
story.append(Paragraph(
    "4. Pennsylvania demonstrates that the geometric mean can amplify near-zero log-space impulses at "
    "high compression. F17 correctly flags this as material stress before the verdict is issued.", styles['Body']))
story.append(Paragraph(
    "5. Zero-handling remains the dominant contamination source at D = 9. Delta_min sits at the "
    "replacement floor for all entities, rendering the Hessian bound uninformative.", styles['Body']))

story.append(Paragraph("<b>Next steps:</b>", styles['SubHead']))
story.append(Paragraph(
    "1. Re-run EXP-01 gold/silver with F17 to confirm the tuner on the baseline. "
    "2. Run the Europe monthly cohort (Spain, Germany, Italy, UK). "
    "3. Investigate subcompositional EITT to address the zero-dominance problem. "
    "4. Begin bridge-case deep dives for operating-envelope calibration.", styles['Body']))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════
# APPENDIX A: FORMULA CATALOG
# ══════════════════════════════════════════════════════════════════

story.append(Paragraph("Appendix A: Full Formula Catalog (F1\u2013F17)", styles['SectionHead']))

formulas = [
    ('F1', 'Composition', 'x_i(t) = f(R_i(t)) / sum_j f(R_j(t)), default f(r) = r'),
    ('F2', 'Shannon entropy', 'H(t) = -sum_i x_i(t) ln(x_i(t))'),
    ('F3', 'Geometric-mean decimation', 'g_i(k) = [prod x_i(t)]^(1/M), re-close'),
    ('F4', 'EITT delta', 'delta_M = H_bar(M) - H_bar(1), relative_M = |delta_M|/H_bar(1)'),
    ('F5', 'Hessian bound', '|delta_M| <= (D-1) sigma_A^2 / (2 delta M)'),
    ('F6', 'CLR transform', 'clr_i = ln(x_i) - (1/D) sum_j ln(x_j)'),
    ('F7', 'Aitchison variance', 'sigma_A^2 = (1/D) sum_i var(clr_i)'),
    ('F8', 'Velocity', 'v(t) = ||clr(t) - clr(t-1)||_2'),
    ('F9', 'Vertex distance', 'delta(t) = min_i x_i(t)'),
    ('F10', 'Trajectory efficiency', 'eta = net / path = ||clr(T)-clr(1)|| / sum v(t)'),
    ('F11', 'Noise floor', 'SE(M) = sigma_H / sqrt(N/M)'),
    ('F12', 'Complexity', 'Gamma = (D-1) sigma_A^2 / (delta sqrt(N/M))'),
    ('F13', 'RMS abs error', 'RMS_dH = sqrt((1/K) sum delta_M^2)'),
    ('F14', 'RMS rel error', 'RMS_rel = sqrt((1/K) sum (delta_M/H_bar)^2)'),
    ('F15', 'RMS noise-norm', 'RMS_SNR = sqrt((1/K) sum (|delta_M|/SE)^2)'),
    ('F16', 'RMS bound-util', 'RMS_ETF = sqrt((1/K) sum (|delta_M|/B)^2)'),
    ('F17', 'Linear contam. tuner', 'C_geom(M) = |delta_M^geom - delta_M^arith| / H_bar(1)'),
]

f_rows = [['ID', 'Name', 'Formula']]
for fid, name, formula in formulas:
    f_rows.append([fid, name, formula])

story.append(make_table(f_rows, col_widths=[30, 100, 330]))
story.append(Paragraph("Table A1. Complete EITT formula catalog. F1\u2013F12 canonical (EXP-01). "
    "F13\u2013F16 proposed (spec addendum). F17 candidate (EXP-02, pending HIVP regression on EXP-01).", styles['CaptionStyle']))

story.append(Spacer(1, 20))
story.append(Paragraph(
    "Gold standard: Make EITT the science. Make HIVP the method of development. "
    "Make the operating envelope the honesty layer. Make HUF-GOV the application family.",
    styles['Finding']))

# ── BUILD ──
doc.build(story)
print(f"Journal built: {OUT}")
print(f"Pages: check PDF")
