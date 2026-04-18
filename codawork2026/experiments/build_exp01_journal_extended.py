"""
Build EXTENDED EXP-01 Experiment Journal — Professional PDF
Gold/Silver 338-Year 2-Simplex EITT Validation
Rounds 1, 2, 2b, 2c, and 3 — Complete iterative record
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from datetime import datetime

# ─── Colors ──────────────────────────────────────────────────────────────
NAVY = HexColor('#1B2A4A')
STEEL = HexColor('#4A6FA5')
LIGHT_BLUE = HexColor('#E8EFF7')
LIGHT_GRAY = HexColor('#F5F5F5')
MEDIUM_GRAY = HexColor('#CCCCCC')
DARK_GRAY = HexColor('#333333')
ACCENT_GREEN = HexColor('#2E7D32')
ACCENT_RED = HexColor('#C62828')
ACCENT_AMBER = HexColor('#F57F17')
WARM_CREAM = HexColor('#FAFAF5')
BROWN = HexColor('#5D3A1A')
BROWN_LIGHT = HexColor('#8B4513')
TEAL = HexColor('#00695C')

# ─── Document setup ──────────────────────────────────────────────────────
output_path = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/EXP-01_Gold_Silver_EITT_Journal.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    topMargin=0.8*inch,
    bottomMargin=0.7*inch,
    leftMargin=0.9*inch,
    rightMargin=0.9*inch,
    title="EXP-01: EITT Validation on Gold/Silver 338-Year 2-Simplex — Extended Journal",
    author="Peter Higgins — Higgins Unity Framework"
)

styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle(
    'JournalTitle', parent=styles['Title'],
    fontName='Helvetica-Bold', fontSize=20, leading=24,
    textColor=NAVY, spaceAfter=4, alignment=TA_LEFT
))
styles.add(ParagraphStyle(
    'JournalSubtitle', parent=styles['Normal'],
    fontName='Helvetica', fontSize=12, leading=16,
    textColor=STEEL, spaceAfter=12, alignment=TA_LEFT
))
styles.add(ParagraphStyle(
    'SectionHead', parent=styles['Heading1'],
    fontName='Helvetica-Bold', fontSize=14, leading=18,
    textColor=NAVY, spaceBefore=18, spaceAfter=8,
    borderWidth=0, borderPadding=0
))
styles.add(ParagraphStyle(
    'SubsectionHead', parent=styles['Heading2'],
    fontName='Helvetica-Bold', fontSize=11, leading=14,
    textColor=STEEL, spaceBefore=12, spaceAfter=6
))
styles.add(ParagraphStyle(
    'HufBodyText', parent=styles['Normal'],
    fontName='Helvetica', fontSize=10, leading=14,
    textColor=DARK_GRAY, alignment=TA_JUSTIFY, spaceAfter=6
))
styles.add(ParagraphStyle(
    'BodyBold', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=10, leading=14,
    textColor=DARK_GRAY, spaceAfter=6
))
styles.add(ParagraphStyle(
    'TableHeader', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=9, leading=12,
    textColor=white, alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    'TableCell', parent=styles['Normal'],
    fontName='Helvetica', fontSize=9, leading=12,
    textColor=DARK_GRAY, alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    'TableCellLeft', parent=styles['Normal'],
    fontName='Helvetica', fontSize=9, leading=12,
    textColor=DARK_GRAY, alignment=TA_LEFT
))
styles.add(ParagraphStyle(
    'CommentStyle', parent=styles['Normal'],
    fontName='Helvetica-Oblique', fontSize=10, leading=13,
    textColor=HexColor('#555555'), leftIndent=12, rightIndent=12,
    spaceBefore=4, spaceAfter=8
))
styles.add(ParagraphStyle(
    'VerdictPass', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=12, leading=16,
    textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=8, spaceAfter=8
))
styles.add(ParagraphStyle(
    'VerdictCaution', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=12, leading=16,
    textColor=ACCENT_AMBER, alignment=TA_CENTER, spaceBefore=8, spaceAfter=8
))
styles.add(ParagraphStyle(
    'FooterStyle', parent=styles['Normal'],
    fontName='Helvetica', fontSize=8, leading=10,
    textColor=MEDIUM_GRAY, alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    'InjectionHead', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=11, leading=14,
    textColor=BROWN_LIGHT, spaceBefore=12, spaceAfter=6
))
styles.add(ParagraphStyle(
    'InjectionBody', parent=styles['Normal'],
    fontName='Helvetica', fontSize=10, leading=14,
    textColor=BROWN, alignment=TA_JUSTIFY,
    leftIndent=6, rightIndent=6, spaceAfter=6
))
styles.add(ParagraphStyle(
    'Equation', parent=styles['Normal'],
    fontName='Courier', fontSize=10, leading=14,
    textColor=DARK_GRAY, alignment=TA_CENTER,
    spaceBefore=6, spaceAfter=6
))
styles.add(ParagraphStyle(
    'RoundBanner', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=13, leading=17,
    textColor=TEAL, spaceBefore=6, spaceAfter=4,
    alignment=TA_LEFT
))
styles.add(ParagraphStyle(
    'NegativeResult', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=10, leading=14,
    textColor=ACCENT_RED, spaceAfter=6
))

# ─── Helper functions ────────────────────────────────────────────────────
def make_hr():
    return HRFlowable(width="100%", thickness=0.5, color=MEDIUM_GRAY, spaceBefore=4, spaceAfter=8)

def make_thick_hr():
    return HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceBefore=6, spaceAfter=10)

def make_teal_hr():
    return HRFlowable(width="100%", thickness=1.0, color=TEAL, spaceBefore=4, spaceAfter=8)

def make_table(headers, rows, col_widths=None, header_color=NAVY):
    """Create a styled data table."""
    header_cells = [Paragraph(h, styles['TableHeader']) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(str(c), styles['TableCell']) for c in row])

    if col_widths is None:
        col_widths = [doc.width / len(headers)] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ('BOX', (0, 0), (-1, -1), 1, header_color),
    ]))
    return t

# ─── Page number callback ────────────────────────────────────────────────
def add_page_number(canvas_obj, doc_obj):
    canvas_obj.saveState()
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(MEDIUM_GRAY)
    page_num = canvas_obj.getPageNumber()
    text = f"EXP-01 Extended | Higgins Unity Framework | Page {page_num}"
    canvas_obj.drawCentredString(doc_obj.pagesize[0] / 2.0, 0.4 * inch, text)
    canvas_obj.restoreState()

# ─── Build document ──────────────────────────────────────────────────────
story = []

# ═══════════════════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 0.6*inch))

story.append(Paragraph("EXPERIMENT JOURNAL", ParagraphStyle(
    'ExpLabel', parent=styles['Normal'],
    fontName='Helvetica', fontSize=11, leading=14,
    textColor=STEEL, spaceAfter=2, letterSpacing=3
)))
story.append(Spacer(1, 4))
story.append(Paragraph("EXP-01", ParagraphStyle(
    'ExpNum', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=36, leading=40,
    textColor=NAVY, spaceAfter=8
)))
story.append(make_thick_hr())
story.append(Paragraph(
    "EITT Validation on the Gold/Silver Ratio",
    styles['JournalTitle']
))
story.append(Paragraph(
    "A 338-Year 2-Simplex Test of Entropy Invariance Under Geometric-Mean Decimation",
    styles['JournalSubtitle']
))
story.append(Paragraph(
    "Extended Journal — Rounds 1 through 3 with Iterative Corrections",
    ParagraphStyle('EditionNote', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=TEAL, spaceAfter=16)
))

# Metadata box
meta_data = [
    ['Researcher', 'Peter Higgins'],
    ['Affiliation', 'Independent Researcher, Markham, Ontario, Canada'],
    ['Framework', 'Higgins Unity Framework (HUF)'],
    ['Date', 'April 16, 2026'],
    ['Series', 'HUF Phase 2 — EITT Hardening'],
    ['Status', 'COMPLETE — CAUTION (EITT holds; delta approaching boundary)'],
    ['Rounds', '5 (Round 1, 2, 2b, 2c, 3)'],
]
meta_table = Table(meta_data, colWidths=[1.5*inch, 4.5*inch])
meta_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('TEXTCOLOR', (0, 0), (0, -1), STEEL),
    ('TEXTCOLOR', (1, 0), (1, -1), DARK_GRAY),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (0, -1), 12),
]))
story.append(meta_table)

story.append(Spacer(1, 0.3*inch))

# Table of contents
story.append(Paragraph("Contents", styles['SubsectionHead']))
toc_items = [
    "Part I — Base Experiment",
    "  1. Experiment Definition",
    "  2. Dataset Identity",
    "  3. Method",
    "  4. Round 1 Results — Base EITT Test",
    "  5. Systems Perspective Injection — P. Higgins",
    "  6. Round 1 Assessment",
    "  7. Forward Amplification",
    "  8. Provenance and Reproducibility",
    "Part II — Iterative Corrections and Retesting",
    "  9. Round 2 — Companion Diagnostics (Velocity, Delta, Winding)",
    "  10. Round 2b — Error Verification: Is the Delta Trend Real?",
    "  11. Round 2c — Methodology Research: CoDa Community Standards",
    "  12. Round 3 — Adjusted Tool and Retesting",
    "  13. Failed Correction Log: Velocity-Weighted Entropy",
    "  14. Final Dashboard and Assessment",
    "Part III — EITT Tool Specification",
    "  15. Complete Formula Catalog (12 formulas)",
    "  16. Error Bound Scaling with System Complexity",
    "  17. State Machine Diagnostic (12 states)",
    "  18. Operating Envelope and Safety Boundaries",
    "  19. Additional Concepts for Tool Strengthening",
    "  20. Regression Chain Methodology (HIVP)",
]
for item in toc_items:
    story.append(Paragraph(item, ParagraphStyle(
        'TOCItem', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=DARK_GRAY, leftIndent=12, spaceAfter=2
    )))

story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(
    "Part of the HUF Experiment Series for CoDaWork 2026 and beyond. "
    "Each journal is a standalone, publishable record designed for independent peer review.",
    ParagraphStyle('Footnote', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9, leading=12,
        textColor=MEDIUM_GRAY, alignment=TA_CENTER)
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 1. EXPERIMENT DEFINITION
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("1. Experiment Definition", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph("1.1 Objective", styles['SubsectionHead']))
story.append(Paragraph(
    "Test whether Shannon entropy is near-invariant under geometric-mean block decimation "
    "of the gold/silver price ratio treated as a 2-simplex composition. This is the simplest "
    "possible EITT validation: D = 2 (two components), annual resolution, spanning 338 years "
    "of recorded price history across multiple monetary regimes.",
    styles['HufBodyText']
))

story.append(Paragraph("1.2 The EITT Claim", styles['SubsectionHead']))
story.append(Paragraph(
    "The Entropy-Invariant Time Transformer (EITT) states that for compositional time series "
    "(vectors of proportions summing to unity), Shannon entropy is near-invariant under "
    "geometric-mean block decimation across temporal resolutions. Formally:",
    styles['HufBodyText']
))
story.append(Paragraph(
    "H(M) = H(1) + delta<sub>M</sub>,    where |delta<sub>M</sub>| is small relative to H(1)",
    styles['Equation']
))
story.append(Paragraph(
    "The second-order Hessian bound (Higgins, 2026) predicts:",
    styles['HufBodyText']
))
story.append(Paragraph(
    "|delta<sub>M</sub>| &lt;= (D-1) sigma<sub>A</sub><super>2</super> / (2 delta M) + O(M<super>-3/2</super>)",
    styles['Equation']
))

story.append(Paragraph("1.3 Why Gold/Silver?", styles['SubsectionHead']))
story.append(Paragraph(
    "The gold/silver price ratio is one of the oldest continuously recorded economic "
    "quantities. The enriched dataset spans 1688 to 2026 with 624 annual observations. "
    "The ratio R (ounces of silver per ounce of gold) maps naturally to a 2-simplex:",
    styles['HufBodyText']
))
story.append(Paragraph(
    "x<sub>gold</sub> = R / (R + 1),     x<sub>silver</sub> = 1 / (R + 1),     x<sub>gold</sub> + x<sub>silver</sub> = 1",
    styles['Equation']
))
story.append(Paragraph(
    "This dataset offers three unique advantages: extreme temporal depth (338 years), "
    "passage through multiple monetary regimes (gold standard, Bretton Woods, floating "
    "rates), and minimal dimensionality (D = 2) that isolates the core EITT mechanism "
    "from higher-dimensional effects.",
    styles['HufBodyText']
))

story.append(Paragraph("1.4 Hypotheses", styles['SubsectionHead']))
hyp_data = [
    ['H0', 'Shannon entropy changes significantly under decimation (EITT fails)'],
    ['H1', 'Shannon entropy is near-invariant: |delta_M|/H < 1% for all M tested'],
    ['H2', 'The Hessian bound correctly predicts the upper limit of |delta_M|'],
    ['H3', 'Different historical regimes show different EITT behavior'],
]
hyp_table = Table(hyp_data, colWidths=[0.5*inch, 5.5*inch])
hyp_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('TEXTCOLOR', (0, 0), (0, -1), STEEL),
    ('TEXTCOLOR', (1, 0), (1, -1), DARK_GRAY),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
]))
story.append(hyp_table)

# ═══════════════════════════════════════════════════════════════════════
# 2. DATASET IDENTITY
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(Paragraph("2. Dataset Identity", styles['SectionHead']))
story.append(make_hr())

ds_rows = [
    ['Source', 'MeasuringWorth / World Gold Council (enriched)'],
    ['File', 'DATA/Commodities/gold_silver_ratio_enriched.csv'],
    ['Format', 'CSV: date, price, currency, silver_oz_per_gold_oz'],
    ['Total rows', '1,769 (1258 CE to 2026 CE)'],
    ['Usable rows', '624 (1688 to 2026 — rows with gold/silver ratio)'],
    ['Currency', 'GBP (1688-1870s), USD (1880s-2026)'],
    ['Resolution', 'Annual (one observation per year)'],
    ['Gaps', 'None in usable range'],
    ['Integrity', 'SHA-256 of source file recorded in HUF_INTEGRITY_MANIFEST'],
]
ds_table = Table(ds_rows, colWidths=[1.3*inch, 4.7*inch])
ds_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('TEXTCOLOR', (0, 0), (0, -1), NAVY),
    ('TEXTCOLOR', (1, 0), (1, -1), DARK_GRAY),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (0, -1), 10),
    ('LINEBELOW', (0, 0), (-1, -2), 0.3, LIGHT_BLUE),
    ('LINEBELOW', (0, -1), (-1, -1), 1, NAVY),
]))
story.append(ds_table)

story.append(Spacer(1, 8))
story.append(Paragraph("2.1 Descriptive Statistics", styles['SubsectionHead']))

desc_headers = ['Statistic', 'Gold/Silver Ratio', 'x_gold', 'x_silver']
desc_rows = [
    ['N', '624', '624', '624'],
    ['Mean', '54.35', '0.9689', '0.0311'],
    ['Std Dev', '32.77', '0.0163', '0.0163'],
    ['Min', '14.14', '0.9339', '0.0095'],
    ['Max', '104.82', '0.9905', '0.0661'],
    ['Min proportion (delta)', '—', '—', '0.0095'],
]
story.append(make_table(desc_headers, desc_rows,
    col_widths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch]))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Comment:</b> The composition is strongly asymmetric — gold dominates at 93-99% "
    "of the simplex. The minimum proportion delta = 0.0095 (silver, 21st century) places "
    "the data near the simplex boundary. This is a natural stress test of the delta parameter "
    "in the Hessian bound.",
    styles['CommentStyle']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 3. METHOD
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("3. Method", styles['SectionHead']))
story.append(make_hr())

steps = [
    ("<b>Step 1 — Composition formation.</b> The gold/silver ratio R is converted to a "
     "2-simplex composition: x<sub>gold</sub> = R/(R+1), x<sub>silver</sub> = 1/(R+1). "
     "Closure is verified (sum = 1.0 to machine precision)."),
    ("<b>Step 2 — Native entropy.</b> Shannon entropy H = -Sum(x<sub>i</sub> ln x<sub>i</sub>) "
     "is computed for each annual observation. The mean H-bar(1) and standard deviation are recorded."),
    ("<b>Step 3 — Geometric-mean block decimation.</b> For each decimation ratio M in "
     "{2, 3, 5, 10, 20, 50}, consecutive blocks of M years are combined via the "
     "component-wise geometric mean, then re-closed to the simplex. Shannon entropy is "
     "computed for each decimated block."),
    ("<b>Step 4 — EITT evaluation.</b> The entropy change delta<sub>M</sub> = H-bar(M) - H-bar(1) "
     "and the relative change |delta<sub>M</sub>|/H-bar are computed. EITT holds if relative "
     "change remains below 1% across all M."),
    ("<b>Step 5 — Hessian bound check.</b> The Aitchison variance is measured directly from "
     "the clr-transformed data and compared to actual |delta<sub>M</sub>|."),
    ("<b>Step 6 — Era decomposition.</b> The data is split into five historical regimes "
     "and EITT is tested within each regime at M = 2."),
]
for step in steps:
    story.append(Paragraph(step, styles['HufBodyText']))

# ═══════════════════════════════════════════════════════════════════════
# 4. ROUND 1 RESULTS
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(Paragraph("4. Round 1 Results — Base EITT Test", styles['SectionHead']))
story.append(make_hr())
story.append(Paragraph("ROUND 1 — April 16, 2026", styles['RoundBanner']))
story.append(make_teal_hr())

story.append(Paragraph("4.1 EITT Decimation Results", styles['SubsectionHead']))

eitt_headers = ['M', 'N blocks', 'H-bar(M)', 'sigma_H', 'delta_M', '|delta_M|/H-bar']
eitt_rows = [
    ['1 (native)', '624', '0.127939', '0.074454', '—', '—'],
    ['2', '312', '0.127903', '0.074380', '-0.000037', '0.029%'],
    ['3', '208', '0.127869', '0.074305', '-0.000070', '0.055%'],
    ['5', '124', '0.128120', '0.074360', '+0.000181', '0.141%'],
    ['10', '62', '0.128006', '0.074139', '+0.000066', '0.052%'],
    ['20', '31', '0.127845', '0.073858', '-0.000095', '0.074%'],
    ['50', '12', '0.128710', '0.074134', '+0.000770', '0.602%'],
]
story.append(make_table(eitt_headers, eitt_rows,
    col_widths=[0.8*inch, 0.8*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.2*inch]))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "Native entropy H-bar = 0.1279 (18.5% of maximum ln(2) = 0.6931). "
    "Maximum relative change: 0.60% at M = 50 (12 blocks of 50 years).",
    styles['HufBodyText']
))
story.append(Paragraph(
    "VERDICT: EITT HOLDS — Maximum relative entropy change 0.60% across all decimation levels",
    styles['VerdictPass']
))

story.append(Paragraph("4.2 Hessian Bound Verification", styles['SubsectionHead']))
story.append(Paragraph(
    "Measured Aitchison variance: sigma<sub>A</sub><super>2</super> = 0.1479. "
    "Minimum proportion: delta = 0.00945. Dimension: D = 2.",
    styles['HufBodyText']
))

hess_headers = ['M', 'Predicted |delta_M|', 'Actual |delta_M|', 'Ratio (pred/actual)', 'Bound holds?']
hess_rows = [
    ['2',  '3.9128', '0.000037', '~106,000x', 'YES'],
    ['3',  '2.6085', '0.000070', '~37,000x',  'YES'],
    ['5',  '1.5651', '0.000181', '~8,600x',   'YES'],
    ['10', '0.7826', '0.000066', '~11,900x',  'YES'],
    ['20', '0.3913', '0.000095', '~4,100x',   'YES'],
    ['50', '0.1565', '0.000770', '~203x',     'YES'],
]
story.append(make_table(hess_headers, hess_rows,
    col_widths=[0.6*inch, 1.3*inch, 1.2*inch, 1.4*inch, 1.1*inch]))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Comment:</b> The Hessian bound holds at every level but is extremely "
    "conservative — overpredicting by factors of 200x to 106,000x. This feeds forward "
    "to EXP-06 (Hessian bound direct parameter measurement across domains).",
    styles['CommentStyle']
))

story.append(Paragraph("4.3 Era Decomposition", styles['SubsectionHead']))
story.append(Paragraph(
    "The 338-year record spans five distinct monetary regimes. EITT is tested within "
    "each regime at M = 2 to detect regime-dependent behavior.",
    styles['HufBodyText']
))

era_headers = ['Era', 'N', 'Ratio (mean)', 'delta_min', 'H-bar', 'delta at M=2', 'Relative']
era_rows = [
    ['Pre-Industrial\n(1688-1799)',       '112', '15.0', '0.0597', '0.2342', '-0.000001', '0.0006%'],
    ['Industrial Rev.\n(1800-1899)',       '100', '17.5', '0.0278', '0.2154', '-0.000007', '0.0032%'],
    ['Gold Standard\n(1900-1970)',         '71',  '43.9', '0.0099', '0.1192', '-0.001141', '0.9568%'],
    ['Post-Bretton\nWoods (1971-2000)',    '30',  '53.6', '0.0110', '0.1003', '-0.000173', '0.1728%'],
    ['21st Century\n(2001-2026)',          '311', '82.9', '0.0095', '0.0662', '-0.000059', '0.0897%'],
]
story.append(make_table(era_headers, era_rows,
    col_widths=[1.1*inch, 0.4*inch, 0.9*inch, 0.7*inch, 0.7*inch, 0.9*inch, 0.8*inch]))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 5. PETER'S INJECTION — SYSTEMS PERSPECTIVE
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("5. Systems Perspective Injection — P. Higgins", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph(
    "Researcher's Note (verbatim injection, April 16 2026):",
    styles['InjectionHead']
))
story.append(Paragraph(
    "Consider from a systems perspective: velocity and windings and transitions and costs. "
    "Cost of stagnation. Cost of action. Cost of what else?",
    styles['InjectionBody']
))

story.append(Spacer(1, 8))
story.append(Paragraph("5.1 Velocity of the Composition", styles['SubsectionHead']))
story.append(Paragraph(
    "The pre-industrial era shows near-zero compositional velocity — the ratio drifts by "
    "+/- 0.3 around a mean of 15.0 for over a century. EITT reports near-perfect invariance "
    "(0.0006%), but this raises a deeper question: <b>is perfect invariance the same as "
    "perfect health?</b> A system with zero velocity is not evolving. The pre-industrial "
    "gold/silver ratio was held nearly constant by bimetallic currency standards — not by "
    "market equilibrium, but by <b>regulatory lock-in</b>.",
    styles['HufBodyText']
))

story.append(Paragraph("5.2 Windings and Transitions", styles['SubsectionHead']))
story.append(Paragraph(
    "Pre-industrial (delta = 0.060) to 21st century (delta = 0.010) is a one-way walk toward "
    "the gold vertex. Each regime shift pushes the composition closer to a vertex and does not "
    "bring it back. <b>A composition that is drifting toward a vertex may report healthy "
    "entropy invariance within each epoch while silently approaching the safety boundary.</b>",
    styles['HufBodyText']
))

story.append(Paragraph("5.3 Cost Analysis", styles['SubsectionHead']))

cost_data = [
    ['Cost Type', 'Manifestation', 'Gold/Silver Example', 'HUF-GOV Implication'],
    ['Cost of\nStagnation',
     'System locked in\nsuboptimal state',
     'Bimetallic standard held\nratio at ~15:1 for a century',
     'Perfect EITT invariance\nmay mask regulatory lock-in'],
    ['Cost of\nAction',
     'Entropy disruption\nduring regime change',
     'Abandoning gold standard\n(1971): volatility jumped 5x',
     'Regime transitions are the\nmost dangerous moments'],
    ['Cost of\nInaction at\nVertex',
     'Approaching simplex\nboundary without\ncorrection',
     '21st century: silver at\n<1% of composition',
     'Near-vertex compositions\nhave fragile EITT invariance'],
    ['Cost of\nIgnoring\nVelocity',
     'Missing slow drift\nwhile local health\nlooks good',
     'Five eras, each healthy,\nbut trajectory is monotone\ntoward vertex',
     'EITT alone is insufficient.\nVelocity is a required\ncompanion diagnostic'],
]
cost_table = Table(cost_data, colWidths=[0.9*inch, 1.3*inch, 1.7*inch, 1.8*inch])
cost_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BROWN),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('LEADING', (0, 0), (-1, -1), 10),
    ('TEXTCOLOR', (0, 1), (0, -1), BROWN),
    ('TEXTCOLOR', (1, 1), (-1, -1), DARK_GRAY),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
    ('BOX', (0, 0), (-1, -1), 1, BROWN),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#FFF8F0')]),
]))
story.append(cost_table)

story.append(Spacer(1, 10))
story.append(Paragraph(
    "<b>Conclusion from injection:</b> EITT measures local compositional health. "
    "A complete HUF-GOV diagnostic must pair EITT (the thermometer) "
    "with compositional velocity (the compass) and vertex-distance monitoring (the altimeter).",
    styles['HufBodyText']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 6. ROUND 1 ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("6. Round 1 Assessment", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph("6.1 Hypothesis Outcomes", styles['SubsectionHead']))
hyp_result_data = [
    ['Hypothesis', 'Outcome', 'Evidence'],
    ['H0: EITT fails', 'REJECTED', 'Max relative change 0.60%'],
    ['H1: EITT holds (<1%)', 'SUPPORTED', 'All M from 2 to 50: |delta_M|/H < 1%'],
    ['H2: Hessian bound\npredicts upper limit', 'SUPPORTED\n(very loose)', 'Bound holds by 200x to 106,000x'],
    ['H3: Eras differ', 'SUPPORTED', 'Pre-Industrial: 0.0006%\nGold Standard: 0.9568%'],
]
hyp_table2 = Table(hyp_result_data, colWidths=[1.3*inch, 1.2*inch, 3.5*inch])
hyp_table2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
    ('FONTNAME', (2, 1), (2, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEADING', (0, 0), (-1, -1), 12),
    ('TEXTCOLOR', (1, 1), (1, 1), ACCENT_RED),
    ('TEXTCOLOR', (1, 2), (1, 2), ACCENT_GREEN),
    ('TEXTCOLOR', (1, 3), (1, 3), ACCENT_GREEN),
    ('TEXTCOLOR', (1, 4), (1, 4), ACCENT_GREEN),
    ('ALIGN', (0, 0), (1, -1), 'CENTER'),
    ('ALIGN', (2, 0), (2, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
    ('BOX', (0, 0), (-1, -1), 1, NAVY),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
]))
story.append(hyp_table2)

story.append(Paragraph("6.2 Round 1 Conclusions", styles['SubsectionHead']))
story.append(Paragraph(
    "<b>Positive:</b> EITT holds on the simplest possible composition (D = 2) across 338 years, "
    "through five monetary regimes. This is the baseline: if EITT failed here, it would fail everywhere.",
    styles['HufBodyText']
))
story.append(Paragraph(
    "<b>Negative:</b> The Hessian bound is wildly conservative for D = 2. It needs tightening "
    "or an alternative formulation for low-dimensional cases.",
    styles['HufBodyText']
))
story.append(Paragraph(
    "<b>New insight:</b> EITT alone is a necessary but insufficient diagnostic. "
    "Velocity, winding, and vertex-distance monitoring are required companions.",
    styles['HufBodyText']
))

# ═══════════════════════════════════════════════════════════════════════
# 7. FORWARD AMPLIFICATION
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(Paragraph("7. Forward Amplification", styles['SectionHead']))
story.append(make_hr())

fwd_data = [
    ['Finding', 'Feeds Into', 'Specific Question'],
    ['EITT holds at D=2,\ndelta=0.0095', 'EXP-02 (Energy)', 'Does EITT hold at D=6-8?'],
    ['Hessian bound is\n200-106,000x loose', 'EXP-06 (Hessian)', 'Is the bound tighter at higher D?'],
    ['Gold Standard era\nshows 0.96% drift', 'EXP-04 (Financial)', 'Does external forcing break\nEITT predictably?'],
    ['Zero velocity masks\nstasis', 'All future EXPs', 'Add velocity diagnostic to\nevery EITT pipeline'],
    ['Monotone vertex\napproach across eras', 'EXP-02, EXP-03', 'Do other domains oscillate\nor also drift monotonically?'],
]
fwd_table = Table(fwd_data, colWidths=[1.4*inch, 1.2*inch, 3.0*inch])
fwd_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), STEEL),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEADING', (0, 0), (-1, -1), 11),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
    ('BOX', (0, 0), (-1, -1), 1, STEEL),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_BLUE]),
]))
story.append(fwd_table)

# ═══════════════════════════════════════════════════════════════════════
# 8. PROVENANCE
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 16))
story.append(Paragraph("8. Provenance and Reproducibility", styles['SectionHead']))
story.append(make_hr())

prov_data = [
    ['Software', 'Python 3, NumPy, SciPy, CSV standard library'],
    ['Scripts', 'exp01_gold_silver_eitt.py, exp01_round2_diagnostics.py,\nexp01_error_verification.py, exp01_round3_adjustments.py'],
    ['Results files', 'EXP01_gold_silver_eitt_results.json,\nEXP01_round2_diagnostics.json,\nEXP01_round3_adjustments.json'],
    ['Random seed', 'N/A — deterministic (except bootstrap in Round 2b: seed=42)'],
    ['Reproducibility', 'Fully reproducible: same input file yields identical output'],
    ['HUF version', 'Phase 2 (EITT Hardening), commit a9d19d8+'],
    ['Cross-reference', 'HUF-GOV canonical: "A tool that produces a verifiably\nclean usable output to a known degree of certainty."'],
]
prov_table = Table(prov_data, colWidths=[1.3*inch, 4.7*inch])
prov_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('LEADING', (0, 0), (-1, -1), 12),
    ('TEXTCOLOR', (0, 0), (0, -1), NAVY),
    ('TEXTCOLOR', (1, 0), (1, -1), DARK_GRAY),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (0, -1), 10),
    ('LINEBELOW', (0, 0), (-1, -2), 0.3, LIGHT_BLUE),
    ('LINEBELOW', (0, -1), (-1, -1), 1, NAVY),
]))
story.append(prov_table)

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# ─── PART II: EXTENDED ROUNDS ────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("PART II — ITERATIVE CORRECTIONS AND RETESTING", ParagraphStyle(
    'PartTitle', parent=styles['Title'],
    fontName='Helvetica-Bold', fontSize=16, leading=20,
    textColor=TEAL, spaceAfter=4, alignment=TA_CENTER
)))
story.append(make_teal_hr())
story.append(Paragraph(
    "Following the gold-standard iterative methodology: test the tool, prove the worth, "
    "validate the result. Only then try the next step. Feed back corrections, extend the "
    "journal, retest. If a tool yields a result, test before advancement.",
    ParagraphStyle('PartSubtitle', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=10, leading=14,
        textColor=TEAL, alignment=TA_CENTER, spaceAfter=16)
))

# ═══════════════════════════════════════════════════════════════════════
# 9. ROUND 2 — COMPANION DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("9. Round 2 — Companion Diagnostics", styles['SectionHead']))
story.append(make_hr())
story.append(Paragraph("ROUND 2 — April 16, 2026", styles['RoundBanner']))
story.append(make_teal_hr())

story.append(Paragraph(
    "Round 1 established that EITT holds. Peter's systems injection (Section 5) identified "
    "that EITT alone is insufficient — velocity, vertex distance, and trajectory efficiency "
    "are required companion instruments. Round 2 builds these instruments.",
    styles['HufBodyText']
))

# 9.1 Velocity
story.append(Paragraph("9.1 Compositional Velocity", styles['SubsectionHead']))
story.append(Paragraph(
    "Velocity is measured as the absolute change in clr-transformed composition per year. "
    "In the 2-simplex, clr<sub>gold</sub> = ln(x<sub>gold</sub>) - 0.5[ln(x<sub>gold</sub>) + "
    "ln(x<sub>silver</sub>)]. Annual velocity = |clr(t) - clr(t-1)|.",
    styles['HufBodyText']
))

vel_headers = ['Era', 'Mean Velocity', 'Max Velocity', 'Std Dev', 'N']
vel_rows = [
    ['Pre-Industrial (1688-1799)',    '0.0043', '0.0245', '0.0042', '111'],
    ['Industrial Rev. (1800-1899)',   '0.0096', '0.1032', '0.0157', '100'],
    ['Gold Standard (1900-1970)',     '0.0495', '0.2398', '0.0526', '71'],
    ['Post-Bretton Woods (1971-2000)','0.0654', '0.1932', '0.0482', '30'],
    ['21st Century (2001-2026)',      '0.0112', '0.1519', '0.0182', '311'],
]
story.append(make_table(vel_headers, vel_rows,
    col_widths=[1.6*inch, 1.0*inch, 1.0*inch, 0.9*inch, 0.5*inch], header_color=TEAL))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Key finding:</b> Velocity increased 15x from Pre-Industrial (0.004) to Post-Bretton Woods "
    "(0.065). The 21st century shows a return to low velocity (0.011), but at a much more "
    "asymmetric composition. Maximum velocity occurred in 1921 (0.240), during the gold "
    "standard era's price volatility.",
    styles['HufBodyText']
))

# 9.2 Vertex Distance
story.append(Paragraph("9.2 Vertex Distance (Delta Monitoring)", styles['SubsectionHead']))
story.append(Paragraph(
    "Delta = min(x<sub>gold</sub>, x<sub>silver</sub>) — the minimum proportion, measuring "
    "distance from the nearest simplex vertex. When delta approaches zero, the composition "
    "is degenerate and entropy approaches zero. This is the alarm bell.",
    styles['HufBodyText']
))

delta_headers = ['Era', 'Mean Delta', 'Min Delta', 'Slope/yr', 'Direction']
delta_rows = [
    ['Pre-Industrial',    '0.0627', '0.0597', '+0.000010', 'Stable'],
    ['Industrial Rev.',   '0.0561', '0.0278', '-0.000199', 'Toward vertex'],
    ['Gold Standard',     '0.0261', '0.0099', '+0.000013', 'Stable (low)'],
    ['Post-Bretton Woods','0.0209', '0.0110', '-0.000722', 'Toward vertex'],
    ['21st Century',      '0.0123', '0.0095', '-0.000186', 'Toward vertex'],
]
story.append(make_table(delta_headers, delta_rows,
    col_widths=[1.4*inch, 1.0*inch, 0.9*inch, 1.0*inch, 1.2*inch], header_color=TEAL))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Global trend:</b> Slope = <b>-0.00019 per year</b>. Current delta = 0.0160. "
    "At this rate, delta reaches the 0.01 safety boundary around 2058.",
    styles['HufBodyText']
))
story.append(Paragraph(
    "<b>ALARM: This is the most important finding in EXP-01.</b> While EITT holds beautifully "
    "within each era, the composition is on a slow, persistent march toward the gold vertex. "
    "The silver component is shrinking at approximately 0.02 percentage points per year. This "
    "is invisible to intra-epoch EITT but clearly visible to the delta monitor.",
    styles['CommentStyle']
))

# 9.3 Winding / Trajectory
story.append(Paragraph("9.3 Trajectory Efficiency (Winding Analysis)", styles['SubsectionHead']))
story.append(Paragraph(
    "Trajectory efficiency = net displacement / total path length. An efficiency of 1.0 means "
    "straight-line motion; 0.0 means pure oscillation with no net movement. This measures "
    "whether the composition is going somewhere or just wandering.",
    styles['HufBodyText']
))

wind_headers = ['Era', 'Net Disp.', 'Path Length', 'Efficiency', 'Direction']
wind_rows = [
    ['Pre-Industrial',    '0.026', '0.478', '0.055 (5.5%)',  'Toward gold'],
    ['Industrial Rev.',   '0.392', '0.960', '0.408 (40.8%)', 'Toward gold'],
    ['Gold Standard',     '0.242', '3.497', '0.069 (6.9%)',  'Toward center'],
    ['Post-Bretton Woods','0.371', '1.833', '0.202 (20.2%)', 'Toward gold'],
    ['21st Century',      '0.004', '3.426', '0.001 (0.1%)',  'Toward center'],
    ['OVERALL',           '0.707', '10.392','0.068 (6.8%)',  'Toward gold'],
]
story.append(make_table(wind_headers, wind_rows,
    col_widths=[1.4*inch, 0.8*inch, 0.9*inch, 1.1*inch, 1.2*inch], header_color=TEAL))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Key finding:</b> Overall trajectory efficiency is only 6.8% — the composition wanders "
    "enormously (93% oscillation) but makes slow net progress toward the gold vertex. "
    "The 21st century is nearly pure oscillation (0.1% efficiency) at a dangerously "
    "asymmetric position. The reversal rate across all years is 54%.",
    styles['HufBodyText']
))

# 9.4 Combined Health
story.append(Paragraph("9.4 Combined Health Assessment", styles['SubsectionHead']))

health_headers = ['Era', 'EITT %', 'Velocity', 'Delta', 'Efficiency', 'Health']
health_rows = [
    ['Pre-Industrial',    '0.0006%', '0.004', '0.063', '5.5%',  'HEALTHY'],
    ['Industrial Rev.',   '0.0032%', '0.010', '0.056', '40.8%', 'HEALTHY'],
    ['Gold Standard',     '0.9568%', '0.049', '0.026', '6.9%',  'OK'],
    ['Post-Bretton Woods','0.1728%', '0.065', '0.021', '20.2%', 'OK'],
    ['21st Century',      '0.0897%', '0.011', '0.012', '0.1%',  'CAUTION'],
]
story.append(make_table(health_headers, health_rows,
    col_widths=[1.3*inch, 0.8*inch, 0.7*inch, 0.7*inch, 0.8*inch, 1.0*inch], header_color=TEAL))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "The 21st Century era is rated CAUTION: EITT holds (0.09%) but delta is low (0.012), "
    "velocity is low (0.011), and trajectory efficiency is near zero (0.1%). The composition "
    "is parked near a vertex, barely moving, with the silver share at historical lows.",
    styles['CommentStyle']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 10. ROUND 2b — ERROR VERIFICATION
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("10. Round 2b — Error Verification", styles['SectionHead']))
story.append(make_hr())
story.append(Paragraph("ROUND 2b — April 16, 2026", styles['RoundBanner']))
story.append(make_teal_hr())

story.append(Paragraph(
    "Peter's question (verbatim):",
    styles['InjectionHead']
))
story.append(Paragraph(
    "Could this be composite errors, multi-step accumulated computation error summations?",
    styles['InjectionBody']
))

story.append(Spacer(1, 8))
story.append(Paragraph(
    "This is the right question. The global delta trend of -0.00019/yr drives the key finding "
    "in Round 2 (delta approaching 0.01 boundary by ~2058). If this trend is an artifact of "
    "accumulated floating-point error, cascading computation steps, or statistical noise, the "
    "alarm is false. Seven independent tests were run to answer this question.",
    styles['HufBodyText']
))

story.append(Paragraph("10.1 Test Battery", styles['SubsectionHead']))

err_headers = ['Test', 'Method', 'Result']
err_rows = [
    ['1. Accumulation\ncheck',
     'Each delta(t) is computed\nindependently from raw data.\nNo running sums.',
     'PASS — No accumulation\npossible by construction'],
    ['2. Float32 vs\nFloat64',
     'Recompute in float32 and\nfloat64; compare slopes.',
     'PASS — Slopes identical\nto 6 significant figures'],
    ['3. Reversal of\ntime',
     'Reverse the time series;\nfit slope to reversed delta.',
     'PASS — Positive slope\n(mirror image), same magnitude'],
    ['4. Shuffle test\n(N=1000)',
     'Randomly permute years;\nmeasure slope on each\npermutation.',
     'PASS — Zero of 1000\nshuffles match real slope;\np < 0.001'],
    ['5. t-statistic',
     'OLS regression of delta\non year; compute t-stat.',
     'PASS — t = -72.6;\np effectively zero'],
    ['6. Bootstrap CI\n(N=10000)',
     'Resample with replacement;\nbuild 95% CI for slope.',
     'PASS — 95% CI:\n[-0.000191, -0.000188];\nexcludes zero'],
    ['7. Independent\nrecalculation',
     'Recalculate delta from\nR/(R+1) at every year;\nverify no propagation.',
     'PASS — Each delta is\na pure function of that\nyear\'s ratio only'],
]
err_table = Table(
    [[Paragraph(c, styles['TableCellLeft']) for c in ['Test', 'Method', 'Result']]] +
    [[Paragraph(str(c), styles['TableCellLeft']) for c in row] for row in err_rows],
    colWidths=[1.2*inch, 2.2*inch, 2.2*inch],
    repeatRows=1
)
err_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TEAL),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('LEADING', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
    ('BOX', (0, 0), (-1, -1), 1, TEAL),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#E0F2F1')]),
]))
story.append(err_table)

story.append(Spacer(1, 8))
story.append(Paragraph("10.2 Verdict", styles['SubsectionHead']))
story.append(Paragraph(
    "VERDICT: The delta trend is REAL — not accumulated computation error",
    styles['VerdictPass']
))
story.append(Paragraph(
    "The trend is simply the gold/silver ratio increasing from ~15:1 in 1688 to ~83:1 in "
    "2026. As R increases, x<sub>silver</sub> = 1/(R+1) decreases, and delta = "
    "min(x<sub>gold</sub>, x<sub>silver</sub>) = x<sub>silver</sub> decreases with it. "
    "Each year's delta is an independent, non-accumulated calculation from that year's "
    "ratio. The regression t-statistic of -72.6 with a 95% bootstrap CI of [-0.000191, "
    "-0.000188] makes the trend unambiguous.",
    styles['HufBodyText']
))
story.append(Paragraph(
    "<b>Physical interpretation:</b> Over 338 years, gold has become progressively more "
    "expensive relative to silver. The composition has drifted monotonically toward the "
    "gold vertex. This is a real economic phenomenon, not an artifact.",
    styles['HufBodyText']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 11. ROUND 2c — METHODOLOGY RESEARCH
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("11. Round 2c — Methodology Research", styles['SectionHead']))
story.append(make_hr())
story.append(Paragraph("ROUND 2c — April 16, 2026", styles['RoundBanner']))
story.append(make_teal_hr())

story.append(Paragraph(
    "Peter's directive: check how other scientists structure research studies like this. "
    "Hone our craft. Web research was conducted on CoDa methodology, Aitchison geometry "
    "reappraisals, CoDaWork conference standards, and laboratory notebook best practices.",
    styles['HufBodyText']
))

story.append(Paragraph("11.1 CoDa Community Requirements Identified", styles['SubsectionHead']))

coda_headers = ['Requirement', 'Source', 'Status in EXP-01']
coda_rows = [
    ['Subcompositional\ncoherence',
     'Aitchison (1986), CoDaWork\nstandard methodology',
     'NOT YET TESTED in Round 1-2.\nQueued for Round 3.'],
    ['Scale invariance',
     'Fundamental CoDa axiom:\nresults must not depend\non measurement units',
     'NOT YET TESTED.\nQueued for Round 3.'],
    ['Use of appropriate\ngeometry',
     'Aitchison geometry, clr/ilr\ntransforms, not raw\nproportions',
     'PARTIAL — clr used for\nvelocity. EITT uses raw\nShannon entropy.'],
    ['Mapping sensitivity',
     'Results should be robust\nto ratio-to-composition\nmapping choice',
     'NOT YET TESTED.\nQueued for Round 3.'],
    ['Proper use of\nFrechet mean',
     'Geometric mean for\ncompositional averaging,\nnot arithmetic mean',
     'PASS — Geometric-mean\ndecimation is the EITT\nmethod by construction.'],
]
coda_table = Table(
    [[Paragraph(c, styles['TableCellLeft']) for c in ['Requirement', 'Source', 'Status in EXP-01']]] +
    [[Paragraph(str(c), styles['TableCellLeft']) for c in row] for row in coda_rows],
    colWidths=[1.5*inch, 1.8*inch, 2.3*inch],
    repeatRows=1
)
coda_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TEAL),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('LEADING', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
    ('BOX', (0, 0), (-1, -1), 1, TEAL),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#E0F2F1')]),
]))
story.append(coda_table)

story.append(Spacer(1, 8))
story.append(Paragraph("11.2 Notebook Best Practices Applied", styles['SubsectionHead']))
story.append(Paragraph(
    "Research into scientific notebook methodology (laboratory notebooks, open-science "
    "standards) confirmed the iterative journal format as appropriate. Key principles adopted: "
    "record negative results honestly (Section 13), document all corrections with before/after "
    "states, maintain chronological round numbering, separate data from interpretation, and "
    "ensure every computation is reproducible from archived scripts.",
    styles['HufBodyText']
))
story.append(Paragraph(
    "The CoDa methodology research identified three gaps in our Round 1-2 work: "
    "subcompositional coherence, scale invariance, and mapping sensitivity had not been tested. "
    "These became the targets for Round 3.",
    styles['HufBodyText']
))

# ═══════════════════════════════════════════════════════════════════════
# 12. ROUND 3 — ADJUSTED TOOL & RETESTING
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(Paragraph("12. Round 3 — Adjusted Tool and Retesting", styles['SectionHead']))
story.append(make_hr())
story.append(Paragraph("ROUND 3 — April 16, 2026", styles['RoundBanner']))
story.append(make_teal_hr())

story.append(Paragraph(
    "Round 3 addresses the three gaps identified in the methodology research (Round 2c) "
    "and adopts the corrected dashboard architecture from the failed velocity-weighting "
    "attempt (Section 13). Four instruments are now run as separate readings, not merged.",
    styles['HufBodyText']
))

story.append(Paragraph("12.1 Subcompositional Coherence", styles['SubsectionHead']))
story.append(Paragraph(
    "For D = 2, subcompositional coherence is trivially satisfied: there is only one possible "
    "subcomposition (the full composition itself). The test verified that swapping the labeling "
    "order (gold/silver vs silver/gold) produces identical EITT results. "
    "<b>RESULT: PASSED.</b> This becomes the key test at D >= 3 in EXP-02.",
    styles['HufBodyText']
))

story.append(Paragraph("12.2 Scale Invariance", styles['SubsectionHead']))
story.append(Paragraph(
    "The gold/silver ratio was scaled by factors of 10<super>0</super> through "
    "10<super>10</super> before composition formation. The EITT results were identical "
    "across all scales (to machine precision). This is expected: the R/(R+1) mapping is "
    "invariant to multiplicative scaling of R. <b>RESULT: PASSED.</b>",
    styles['HufBodyText']
))

story.append(Paragraph("12.3 Mapping Sensitivity", styles['SubsectionHead']))
story.append(Paragraph(
    "Three different ratio-to-composition mappings were tested:",
    styles['HufBodyText']
))

map_headers = ['Mapping', 'Formula', 'Max |delta_M|/H-bar']
map_rows = [
    ['Standard',       'x = R/(R+1)',                '0.141%'],
    ['Inverse',        'x = (1/R)/(1/R + 1)',        '0.141%'],
    ['Sqrt-dampened',  'x = sqrt(R)/(sqrt(R) + 1)',  '0.070%'],
]
story.append(make_table(map_headers, map_rows,
    col_widths=[1.2*inch, 2.3*inch, 1.5*inch], header_color=TEAL))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "EITT holds under all three mappings. The sqrt-dampened mapping produces even smaller "
    "entropy changes (0.070%), which is expected since sqrt compression reduces the dominance "
    "of extreme ratios. <b>RESULT: PASSED — EITT is robust to mapping choice.</b>",
    styles['HufBodyText']
))

story.append(Paragraph("12.4 Corrections Applied in Round 3", styles['SubsectionHead']))

corr_items = [
    "Velocity-weighted entropy REMOVED (failed in Round 2 — see Section 13)",
    "Dashboard architecture adopted: EITT + companions as 4 separate instruments",
    "Subcompositional coherence verified (CoDa methodology requirement)",
    "Scale invariance verified",
    "Mapping sensitivity tested — EITT is robust to mapping choice",
]
for i, item in enumerate(corr_items, 1):
    story.append(Paragraph(
        f"<b>{i}.</b> {item}",
        styles['HufBodyText']
    ))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 13. FAILED CORRECTION LOG
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("13. Failed Correction Log: Velocity-Weighted Entropy", styles['SectionHead']))
story.append(make_hr())
story.append(Paragraph("NEGATIVE RESULT — Documented for Transparency", styles['NegativeResult']))

story.append(Paragraph(
    "During Round 2, an attempt was made to create a velocity-weighted entropy measure that "
    "would unify EITT and compositional velocity into a single diagnostic number. The idea: "
    "weight each year's entropy by the inverse of its velocity, so that high-velocity periods "
    "(where the composition is changing rapidly) would count less.",
    styles['HufBodyText']
))

story.append(Paragraph("13.1 What Was Tried", styles['SubsectionHead']))
story.append(Paragraph(
    "Weighted entropy H<sub>w</sub> = Sum(w<sub>t</sub> H<sub>t</sub>) / Sum(w<sub>t</sub>), "
    "where w<sub>t</sub> = 1 / (velocity<sub>t</sub> + epsilon). The intention was that "
    "slow-moving periods (high weight) would dominate the weighted average, producing a "
    "more stable entropy estimate.",
    styles['HufBodyText']
))

story.append(Paragraph("13.2 What Happened", styles['SubsectionHead']))
story.append(Paragraph(
    "Unweighted entropy: H = 0.1279. Weighted entropy: H<sub>w</sub> = 0.1950. "
    "The weighting inflated entropy by 52%. Worse, the EITT deltas under the weighted "
    "measure were much larger — the invariance property was destroyed by the weighting. "
    "Low-velocity periods (pre-industrial) have intrinsically different base entropy than "
    "high-velocity periods. Weighting mixes incomparable regimes.",
    styles['HufBodyText']
))

story.append(Paragraph("13.3 Why It Failed", styles['SubsectionHead']))
story.append(Paragraph(
    "The fundamental error: velocity and entropy are not on the same scale or in the same "
    "space. Velocity is a rate in clr-space; entropy is a scalar in probability-space. Mixing "
    "them via weighting is like using temperature to weight pressure readings — technically "
    "computable but physically meaningless. The correct approach, adopted in Round 3, is to "
    "keep them as <b>separate instruments on a dashboard</b>, each read independently.",
    styles['HufBodyText']
))

story.append(Paragraph("13.4 Lesson Learned", styles['SubsectionHead']))
story.append(Paragraph(
    "This failure validated Peter's systems perspective: the instruments must be separate. "
    "EITT is the thermometer. Velocity is the compass. Delta is the altimeter. Trajectory "
    "efficiency is the GPS. You don't improve a thermometer by bolting a compass to it. "
    "This is now codified as a design principle for all future HUF diagnostics: "
    "<b>separate instruments, separate readings, combined interpretation.</b>",
    styles['HufBodyText']
))

# ═══════════════════════════════════════════════════════════════════════
# 14. FINAL DASHBOARD AND ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 16))
story.append(Paragraph("14. Final Dashboard and Assessment", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph("14.1 Dashboard Output — Round 3 (Final)", styles['SubsectionHead']))

dash_data = [
    ['Instrument', 'Reading', 'Status', 'Interpretation'],
    ['EITT\n(Thermometer)',
     'Max 0.60%\nacross all M',
     'PASS',
     'Entropy invariance holds.\nCore EITT claim validated.'],
    ['Velocity\n(Compass)',
     'Current: 0.011/yr\nOverall: 0.017/yr',
     'LOW',
     'Composition barely moving\nin 21st century. Near-stasis.'],
    ['Delta\n(Altimeter)',
     'Current: 0.0160\nTrend: -0.00019/yr',
     'CAUTION',
     'Approaching 0.01 boundary.\nProjected arrival: ~2058.'],
    ['Trajectory\n(GPS)',
     'Efficiency: 6.8%\n21st cent: 0.1%',
     'MIXED',
     '93% oscillation overall.\nNet drift toward gold vertex.'],
]
dash_table = Table(
    [[Paragraph(c, ParagraphStyle('DashHead', parent=styles['TableHeader'],
        fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=white, alignment=TA_CENTER))
      for c in dash_data[0]]] +
    [[Paragraph(str(c), styles['TableCellLeft']) for c in row] for row in dash_data[1:]],
    colWidths=[1.1*inch, 1.3*inch, 0.8*inch, 2.4*inch],
    repeatRows=1
)
dash_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('LEADING', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('ALIGN', (2, 1), (2, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
    ('BOX', (0, 0), (-1, -1), 1.5, NAVY),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    # Color-code the status column
    ('TEXTCOLOR', (2, 1), (2, 1), ACCENT_GREEN),   # PASS
    ('TEXTCOLOR', (2, 2), (2, 2), STEEL),           # LOW
    ('TEXTCOLOR', (2, 3), (2, 3), ACCENT_AMBER),    # CAUTION
    ('TEXTCOLOR', (2, 4), (2, 4), ACCENT_AMBER),    # MIXED
    ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
]))
story.append(dash_table)

story.append(Spacer(1, 8))
story.append(Paragraph(
    "OVERALL ASSESSMENT: CAUTION — EITT holds; delta approaching boundary",
    styles['VerdictCaution']
))

story.append(Paragraph("14.2 What EXP-01 Establishes (Final)", styles['SubsectionHead']))

final_items = [
    ("<b>EITT is validated at D = 2.</b> The entropy-invariance claim holds across 338 years, "
     "five monetary regimes, seven decimation levels, and three composition mappings. "
     "Maximum relative change: 0.60%."),
    ("<b>The Hessian bound holds but is very conservative.</b> Predicted values exceed "
     "actual by 200x to 106,000x. The bound needs tightening for low-D systems."),
    ("<b>CoDa methodology requirements are satisfied.</b> Subcompositional coherence, "
     "scale invariance, and mapping sensitivity all pass."),
    ("<b>The delta trend is real.</b> Seven independent verification tests confirm the "
     "-0.00019/yr slope (t = -72.6, bootstrap CI excludes zero). The gold/silver ratio's "
     "long-term increase is a genuine economic phenomenon driving the composition toward "
     "the gold vertex."),
    ("<b>EITT alone is insufficient.</b> The systems-perspective injection and subsequent "
     "rounds established that velocity, delta, and trajectory efficiency are required "
     "companion diagnostics. Attempting to merge them (velocity-weighted entropy) failed. "
     "They must remain separate instruments."),
    ("<b>The dashboard architecture is validated.</b> Four instruments, four separate "
     "readings, combined interpretation. This becomes the standard for all subsequent "
     "HUF experiments."),
]
for item in final_items:
    story.append(Paragraph(item, styles['HufBodyText']))

story.append(Paragraph("14.3 Readiness for EXP-02", styles['SubsectionHead']))
story.append(Paragraph(
    "EXP-01 is exhausted at the D = 2 level. All identified gaps have been addressed: "
    "companion diagnostics built (Round 2), error verification complete (Round 2b), "
    "CoDa methodology compliance verified (Rounds 2c/3), negative result documented "
    "(Section 13), and final dashboard architecture established (Section 14). "
    "The next step is EXP-02: EITT on the EMBER energy mix at D = 6-8, where "
    "subcompositional coherence becomes a non-trivial test and the Hessian bound "
    "should tighten with higher dimensionality.",
    styles['HufBodyText']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# ─── PART III: TOOL SPECIFICATION ─────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("PART III — EITT TOOL SPECIFICATION", ParagraphStyle(
    'PartTitle3', parent=styles['Title'],
    fontName='Helvetica-Bold', fontSize=16, leading=20,
    textColor=NAVY, spaceAfter=4, alignment=TA_CENTER
)))
story.append(make_thick_hr())
story.append(Paragraph(
    "Complete formulas, error bound scaling, state machine diagnostic, and operating "
    "envelope. Established on the gold standard (D = 2) to serve as the reference "
    "specification for all higher-dimensional experiments.",
    ParagraphStyle('PartSub3', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=10, leading=14,
        textColor=NAVY, alignment=TA_CENTER, spaceAfter=16)
))

# ═══════════════════════════════════════════════════════════════════════
# 15. COMPLETE FORMULA CATALOG
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("15. Complete Formula Catalog", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph(
    "Every computation in the EITT diagnostic pipeline is specified here. No formula "
    "is implicit. Any implementation that reproduces these formulas on the same input "
    "must produce identical output (to floating-point precision).",
    styles['HufBodyText']
))

# Formula table
formula_data = [
    ['ID', 'Name', 'Formula', 'Domain'],
    ['F1', 'Composition\nformation',
     'x_i(t) = f(R_i(t)) / sum_j f(R_j(t))\nwhere f is the mapping function\n(standard: f(r) = r)',
     'R_i > 0\nsum(x_i) = 1'],
    ['F2', 'Shannon\nentropy',
     'H(t) = -sum_i x_i(t) ln(x_i(t))\n(natural logarithm)',
     '0 <= H <= ln(D)'],
    ['F3', 'Geometric-mean\ndecimation',
     'g_i(k) = [prod x_i(t)]^{1/M}\nfor t in block k\nx_M_i(k) = g_i(k) / sum_j g_j(k)',
     'M >= 2\nN/M >= 3'],
    ['F4', 'EITT delta',
     'delta_M = H_bar(M) - H_bar(1)\nrelative = |delta_M| / H_bar(1)',
     'PASS if relative\n< 1% for all M'],
    ['F5', 'Hessian\nbound',
     '|delta_M| <= (D-1) sigma_A^2\n               / (2 delta M)',
     'delta = min_i x_i\nover all t'],
    ['F6', 'CLR\ntransform',
     'clr_i(t) = ln(x_i(t))\n  - (1/D) sum_j ln(x_j(t))\nProperty: sum_i clr_i = 0',
     'x_i > 0\nfor all i'],
    ['F7', 'Aitchison\nvariance',
     'sigma_A^2 = (1/D) sum_i var(clr_i)\n(variance across time for each\ncomponent, averaged over D)',
     'sigma_A^2 >= 0'],
    ['F8', 'Compositional\nvelocity',
     'v(t) = ||clr(t) - clr(t-1)||_2\n(Euclidean norm in clr space\n= Aitchison distance)',
     'v(t) >= 0'],
    ['F9', 'Vertex\ndistance',
     'delta(t) = min_i x_i(t)\nslope = OLS(delta ~ t)\nt_cross = t where\n  delta(t_cross) = 0.01',
     'delta in (0, 1/D]'],
    ['F10', 'Trajectory\nefficiency',
     'net = ||clr(T) - clr(1)||_2\npath = sum_t v(t)\neta = net / path',
     'eta in [0, 1]'],
    ['F11', 'Statistical\nnoise floor',
     'SE(M) = sigma_H / sqrt(N/M)\nSNR = |delta_M| / SE(M)\nReliable if SNR > 2',
     'N/M >= 3'],
    ['F12', 'Complexity\nparameter',
     'Gamma = (D-1) sigma_A^2\n  / (delta sqrt(N/M))\nLow Gamma = easy test\nHigh Gamma = hard test',
     'Gamma >= 0'],
]

formula_table = Table(
    [[Paragraph(c, ParagraphStyle('FH', parent=styles['TableHeader'],
        fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=white, alignment=TA_CENTER))
      for c in formula_data[0]]] +
    [[Paragraph(str(c), ParagraphStyle('FC', parent=styles['TableCellLeft'],
        fontName='Courier' if j == 2 else 'Helvetica', fontSize=7, leading=9, textColor=DARK_GRAY))
      for j, c in enumerate(row)] for row in formula_data[1:]],
    colWidths=[0.4*inch, 0.9*inch, 2.6*inch, 1.3*inch],
    repeatRows=1
)
formula_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('LEADING', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
    ('BOX', (0, 0), (-1, -1), 1, NAVY),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
]))
story.append(formula_table)

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 16. ERROR BOUND SCALING
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("16. Error Bound Scaling with System Complexity", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph(
    "The Hessian bound B(D, sigma, delta, M) = (D-1) sigma<sub>A</sub><super>2</super> / "
    "(2 delta M) depends on four parameters. As experiments move from D = 2 (gold/silver) "
    "to D = 7 (energy mix) and beyond, the bound changes dramatically. Understanding this "
    "scaling is essential for predicting where EITT will hold and where it may fail.",
    styles['HufBodyText']
))

story.append(Paragraph("16.1 Sensitivity Coefficients", styles['SubsectionHead']))
story.append(Paragraph(
    "Elasticity measures the percentage change in the bound per percentage change in each "
    "parameter. At the EXP-01 operating point (D = 2, sigma<sub>A</sub><super>2</super> = 0.148, "
    "delta = 0.0095, M = 2):",
    styles['HufBodyText']
))

sens_headers = ['Parameter', 'Symbol', 'EXP-01 Value', 'Elasticity', 'Interpretation']
sens_rows = [
    ['Components', 'D', '2', '+2.00', 'Bound doubles per unit increase in D'],
    ['Aitchison var.', 'sigma_A^2', '0.148', '+1.00', 'Bound scales linearly with variance'],
    ['Min proportion', 'delta', '0.0095', '-0.90', 'CRITICAL: bound explodes as delta->0'],
    ['Decimation', 'M', '2', '-0.67', 'Bound shrinks with coarser decimation'],
]
story.append(make_table(sens_headers, sens_rows,
    col_widths=[0.9*inch, 0.7*inch, 0.8*inch, 0.8*inch, 2.4*inch]))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Critical finding:</b> Delta (minimum proportion) is the dominant risk factor. The "
    "1/delta dependence means that as a composition approaches a vertex, the theoretical "
    "bound on EITT error grows without limit. At delta = 0.001 (1 part in 1000), the bound "
    "is 10x larger than at delta = 0.01. This is why the delta monitor (Section 9.2) is the "
    "alarm bell of the system.",
    styles['HufBodyText']
))

story.append(Paragraph("16.2 Empirical Tightness Factor (ETF)", styles['SubsectionHead']))
story.append(Paragraph(
    "The ETF measures how close the actual EITT delta is to the theoretical bound. "
    "ETF = |delta<sub>M</sub>| / B(M). ETF = 1 means the bound is perfectly tight; "
    "ETF near 0 means the bound is extremely loose.",
    styles['HufBodyText']
))

etf_headers = ['M', 'ETF', 'log10(1/ETF)', 'Interpretation']
etf_rows = [
    ['2',  '9.35 x 10^-6', '5.0', 'Bound is 107,000x loose'],
    ['3',  '2.70 x 10^-5', '4.6', 'Bound is 37,000x loose'],
    ['5',  '1.16 x 10^-4', '3.9', 'Bound is 8,600x loose'],
    ['10', '8.50 x 10^-5', '4.1', 'Bound is 11,800x loose'],
    ['20', '2.42 x 10^-4', '3.6', 'Bound is 4,100x loose'],
    ['50', '4.92 x 10^-3', '2.3', 'Bound is 200x loose'],
]
story.append(make_table(etf_headers, etf_rows,
    col_widths=[0.5*inch, 1.2*inch, 1.1*inch, 2.8*inch]))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Mean ETF at D = 2: 9.0 x 10<super>-4</super></b> (bound is ~1,100x loose on average). "
    "The ETF increases with M (bound tightens at coarser decimation), which is consistent "
    "with the higher-order O(M<super>-3/2</super>) terms becoming more significant at large M. "
    "The key open question for EXP-02: <b>does ETF increase with D?</b> If yes, the bound "
    "tightens naturally at higher dimensions and becomes a useful operational limit.",
    styles['HufBodyText']
))

story.append(Paragraph("16.3 Noise Floor Discovery", styles['SubsectionHead']))
story.append(Paragraph(
    "A critical finding: at D = 2 with N = 624, <b>all EITT deltas are below the statistical "
    "noise floor</b>. The noise floor SE(M) = sigma<sub>H</sub> / sqrt(N/M) exceeds the "
    "actual |delta<sub>M</sub>| by factors of 25x to 100x. The entropy invariance at D = 2 "
    "is so strong that the EITT deltas are literally indistinguishable from zero against "
    "sampling noise.",
    styles['HufBodyText']
))

noise_headers = ['M', 'Noise Floor (SE)', 'Actual |delta|', 'SNR', 'Status']
noise_rows = [
    ['2',  '0.004215', '0.000037', '0.009', 'Below noise (invariance perfect)'],
    ['3',  '0.005162', '0.000070', '0.014', 'Below noise (invariance perfect)'],
    ['5',  '0.006686', '0.000181', '0.027', 'Below noise (invariance perfect)'],
    ['10', '0.009455', '0.000066', '0.007', 'Below noise (invariance perfect)'],
    ['20', '0.013372', '0.000095', '0.007', 'Below noise (invariance perfect)'],
    ['50', '0.021492', '0.000770', '0.036', 'Below noise (invariance perfect)'],
]
story.append(make_table(noise_headers, noise_rows,
    col_widths=[0.5*inch, 1.1*inch, 1.0*inch, 0.6*inch, 2.4*inch]))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Implication:</b> At D = 2, EITT is not just passing — it is passing by such a "
    "margin that the test has no statistical power to detect failure. The gold/silver "
    "system is in the \"trivially invariant\" regime. Higher D systems (EXP-02 onward) will "
    "have larger actual deltas and may rise above the noise floor, giving the test real "
    "discriminating power. This is why the gold standard is the gold standard: if it "
    "failed here, the theory would be dead.",
    styles['CommentStyle']
))

story.append(Paragraph("16.4 Predicted Bounds for Future Experiments", styles['SubsectionHead']))

pred_headers = ['Experiment', 'D', 'N', 'Bound (M=2)', 'Gamma', 'DOF', 'Prediction']
pred_rows = [
    ['EXP-01 Gold/Silver',   '2',  '624', '3.91',   '0.89',   '311', 'TRIVIAL — proved here'],
    ['EXP-02 Energy',        '7',  '60',  '75.00',  '54.77',  '174', 'HARDER — bound is loose\nbut Gamma is high'],
    ['EXP-03 Employment',    '5',  '30',  '15.00',  '15.49',  '56',  'MODERATE — low N is\nthe main risk'],
    ['EXP-04 Financial',     '4',  '250', '120.00', '42.93',  '372', 'HARD — low delta (0.005)\ndominates the bound'],
    ['EXP-05 Cross-domain',  '10', '50',  '450.00', '360.00', '216', 'VERY HARD — high D and\nlow delta combined'],
]
story.append(make_table(pred_headers, pred_rows,
    col_widths=[1.2*inch, 0.3*inch, 0.4*inch, 0.7*inch, 0.6*inch, 0.5*inch, 1.8*inch]))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>The complexity parameter Gamma</b> = (D-1) sigma<sub>A</sub><super>2</super> / "
    "(delta sqrt(N/M)) is the single number that predicts how hard the EITT test will be. "
    "EXP-01 has Gamma = 0.89. EXP-05 has Gamma = 360. The progression from easy to hard "
    "is by design — the experiment ladder is ordered by expected difficulty.",
    styles['HufBodyText']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 17. STATE MACHINE DIAGNOSTIC
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("17. State Machine Diagnostic", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph(
    "The EITT diagnostic pipeline is formalized as a 12-state machine. Each state has "
    "defined inputs, outputs, validation gates, and failure modes. The pipeline is strictly "
    "sequential: no state may be entered until all predecessor validations pass. This "
    "prevents cascading errors — a concern Peter correctly identified in Round 2b.",
    styles['HufBodyText']
))

# State machine table
sm_data = [
    ['State', 'Name', 'Key Formula', 'Validation Gate', 'Failure Mode'],
    ['S0', 'RAW_DATA',
     'R(t) = raw_value(t)',
     'N >= 20, no NaN/Inf,\nchronological order',
     'ABORT'],
    ['S1', 'COMPOSITION',
     'x_i = f(R_i) / sum f(R_j)',
     'sum(x_i) = 1,\nall x_i > 0, D >= 2',
     'ABORT'],
    ['S2', 'NATIVE\nENTROPY',
     'H = -sum x_i ln(x_i)',
     'H >= 0, H <= ln(D)\nfor all t',
     'WARN if at\nlimits'],
    ['S3', 'CLR\nTRANSFORM',
     'clr_i = ln(x_i)\n- (1/D) sum ln(x_j)',
     'sum(clr_i) = 0\nfor all t',
     'WARN if high\nvariance'],
    ['S4', 'DECIMATION',
     'g_i = [prod x_i]^{1/M}\nx_M_i = g_i / sum g_j',
     'N/M >= 10 preferred\nN/M >= 3 minimum',
     'SKIP if\nN/M < 3'],
    ['S5', 'EITT\nEVAL',
     'delta_M = H(M) - H(1)\nrel = |delta_M|/H',
     'rel < 1% PASS\nrel < 5% WARN',
     'FAIL if\nrel > 1%'],
    ['S6', 'HESSIAN\nCHECK',
     'B = (D-1)s^2/(2dM)\nETF = |delta|/B',
     'actual <= predicted\nfor all M',
     'CRITICAL if\nbound violated'],
    ['S7', 'VELOCITY',
     'v(t) = ||clr(t)\n  - clr(t-1)||',
     'v >= 0; flag if\nmean v < 0.001',
     'WARN: possible\nstasis'],
    ['S8', 'DELTA\nMONITOR',
     'delta(t) = min_i x_i\nslope via OLS',
     'delta > 0.01 SAFE\ndelta > 0.001 WARN',
     'ALARM if\ndelta < 0.01'],
    ['S9', 'TRAJECTORY',
     'eta = net_disp\n  / path_length',
     'eta in [0, 1]',
     'INFO only'],
    ['S10', 'CODA\nCOMPLIANCE',
     'Subcomp + Scale\n+ Mapping tests',
     'All three\nmust PASS',
     'FAIL: cannot\npublish'],
    ['S11', 'DASHBOARD',
     'Overall = worst of\n(EITT, delta) status',
     'All instruments\nhave valid readings',
     'Always\nproduces output'],
]

sm_table = Table(
    [[Paragraph(c, ParagraphStyle('SMH', parent=styles['TableHeader'],
        fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=white, alignment=TA_CENTER))
      for c in sm_data[0]]] +
    [[Paragraph(str(c), ParagraphStyle('SMC', parent=styles['TableCellLeft'],
        fontName='Courier' if j == 2 else 'Helvetica', fontSize=7, leading=9, textColor=DARK_GRAY))
      for j, c in enumerate(row)] for row in sm_data[1:]],
    colWidths=[0.4*inch, 0.7*inch, 1.4*inch, 1.3*inch, 0.9*inch],
    repeatRows=1
)
sm_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('LEADING', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
    ('BOX', (0, 0), (-1, -1), 1, NAVY),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
]))
story.append(sm_table)

story.append(Spacer(1, 8))
story.append(Paragraph("17.1 State Transition Rules", styles['SubsectionHead']))

story.append(Paragraph(
    "<b>Sequential execution:</b> S0 -> S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S7 -> S8 -> "
    "S9 -> S10 -> S11. No state may be skipped except S4 (when N/M < 3 for a specific M "
    "value, that M is skipped but the pipeline continues with valid M values).",
    styles['HufBodyText']
))
story.append(Paragraph(
    "<b>Abort conditions:</b> S0 or S1 failure aborts the entire pipeline. The data is "
    "unsuitable for EITT analysis. All results are invalidated.",
    styles['HufBodyText']
))
story.append(Paragraph(
    "<b>Fail conditions:</b> S5 (EITT > 1%) or S10 (CoDa non-compliance) produce a FAIL "
    "verdict. The pipeline continues to completion for diagnostic purposes, but the overall "
    "result is FAIL. The remaining instruments (velocity, delta, trajectory) explain <i>why</i> "
    "it failed.",
    styles['HufBodyText']
))
story.append(Paragraph(
    "<b>Critical condition:</b> S6 (Hessian bound violated) means the actual entropy change "
    "exceeds the theoretical prediction. This would indicate a gap in the theory itself. "
    "No Critical condition has been observed in any experiment to date.",
    styles['HufBodyText']
))
story.append(Paragraph(
    "<b>Dashboard logic (S11):</b> The overall assessment is the <i>worst</i> of the EITT "
    "status and the delta status, modified by velocity and trajectory context. A system "
    "can have PASS on EITT but CAUTION overall if delta is low. A system cannot have "
    "PASS overall if EITT has failed.",
    styles['HufBodyText']
))

story.append(Paragraph("17.2 Error Non-Propagation Guarantee", styles['SubsectionHead']))
story.append(Paragraph(
    "Peter's Round 2b question — could accumulated computation errors produce false trends? "
    "— is answered architecturally by the state machine design. <b>No state uses running "
    "sums or accumulated values from previous states.</b> Each state computes from raw or "
    "independently derived quantities:",
    styles['HufBodyText']
))

nonprop_items = [
    "S2 (entropy): computed from x(t), which is computed from R(t). No accumulation.",
    "S4 (decimation): geometric mean within each block. Blocks are independent.",
    "S5 (EITT delta): difference of two independently computed means. No chain.",
    "S7 (velocity): each v(t) uses only two adjacent timepoints. No running sum.",
    "S8 (delta): each delta(t) = min(x(t)), computed from that year's composition only.",
    "S9 (trajectory): net displacement uses only first and last points. Path length is a sum of independent v(t) values, but even if one v(t) has error, it does not propagate to others.",
]
for i, item in enumerate(nonprop_items, 1):
    story.append(Paragraph(f"<b>{i}.</b> {item}", ParagraphStyle(
        'NonProp', parent=styles['HufBodyText'], fontSize=9, leading=12, leftIndent=12)))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "This is a design invariant, not an accident. The EITT pipeline is deliberately "
    "constructed to prevent error accumulation. Every measurement is a fresh computation "
    "from primary data.",
    styles['CommentStyle']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 18. OPERATING ENVELOPE AND SAFETY BOUNDARIES
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("18. Operating Envelope and Safety Boundaries", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph(
    "The EITT tool has a defined operating envelope — the region of parameter space where "
    "results are reliable. Outside this envelope, the tool may still produce numbers, but "
    "those numbers should not be trusted.",
    styles['HufBodyText']
))

story.append(Paragraph("18.1 Hard Boundaries (ABORT)", styles['SubsectionHead']))

hard_headers = ['Parameter', 'Minimum', 'Reason']
hard_rows = [
    ['N (observations)', '>= 20', 'Below 20, statistics are unreliable for any M'],
    ['D (components)', '>= 2', 'D = 1 has no compositional structure'],
    ['delta (min prop.)', '> 0', 'Zero proportion = degenerate composition = undefined entropy'],
    ['N/M (blocks)', '>= 3', 'Below 3 blocks, mean and std are meaningless'],
]
story.append(make_table(hard_headers, hard_rows,
    col_widths=[1.2*inch, 1.0*inch, 3.4*inch], header_color=ACCENT_RED))

story.append(Paragraph("18.2 Soft Boundaries (WARN)", styles['SubsectionHead']))

soft_headers = ['Parameter', 'Threshold', 'Warning']
soft_rows = [
    ['delta', '< 0.02', 'Approaching vertex; Hessian bound loosening rapidly'],
    ['delta', '< 0.01', 'CAUTION — at safety boundary; EITT may be fragile'],
    ['N/M', '< 10', 'Low statistical power; SE may exceed actual delta'],
    ['velocity', '< 0.001', 'Near-stasis; EITT invariance may mask regulatory lock-in'],
    ['EITT relative', '> 0.5%', 'Approaching 1% threshold; investigate regime effects'],
    ['Gamma', '> 100', 'System is in difficult parameter space; expect loose bounds'],
]
story.append(make_table(soft_headers, soft_rows,
    col_widths=[1.0*inch, 0.8*inch, 3.8*inch], header_color=ACCENT_AMBER))

story.append(Paragraph("18.3 EXP-01 Position in the Operating Envelope", styles['SubsectionHead']))
story.append(Paragraph(
    "The gold/silver system sits comfortably inside the operating envelope on all parameters "
    "except delta. Current delta = 0.0160, which is above the 0.01 safety boundary but "
    "trending toward it at -0.00019/yr. The system crossed the 0.02 soft boundary during "
    "the 21st century era. All other parameters (N = 624, D = 2, Gamma = 0.89) are well "
    "within safe limits. The composition is in the <b>delta-limited regime</b>: vertex "
    "proximity is the binding constraint, not dimensionality, sample size, or variance.",
    styles['HufBodyText']
))

# ═══════════════════════════════════════════════════════════════════════
# 19. ADDITIONAL CONCEPTS AND TOOL STRENGTHENING
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(Paragraph("19. Additional Concepts for Tool Strengthening", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph(
    "The following concepts are proposed additions to the EITT diagnostic toolkit, "
    "motivated by the analysis in Sections 15-18. Each addresses a specific gap or "
    "opportunity identified during EXP-01.",
    styles['HufBodyText']
))

story.append(Paragraph("19.1 Adaptive Decimation Schedule", styles['SubsectionHead']))
story.append(Paragraph(
    "Currently, M is chosen from a fixed set {2, 3, 5, 10, 20, 50}. When N is small "
    "(EXP-02: N = 60, EXP-03: N = 30), many of these produce fewer than 3 blocks. An "
    "adaptive schedule M* = {M : N/M >= 10} ensures all tested decimation levels have "
    "adequate statistical power. For N = 30, this gives M* = {2, 3}. For N = 60, "
    "M* = {2, 3, 5, 6}. The tool should compute M* automatically and report which "
    "levels were tested and which were skipped.",
    styles['HufBodyText']
))

story.append(Paragraph("19.2 Confidence Intervals on EITT Delta", styles['SubsectionHead']))
story.append(Paragraph(
    "The current test reports |delta<sub>M</sub>|/H-bar as a point estimate. Adding a "
    "bootstrap confidence interval (as demonstrated in Round 2b for the delta trend) "
    "would allow statements like \"EITT relative change = 0.14% [0.02%, 0.31%] at 95% CI.\" "
    "This transforms the binary PASS/FAIL into a graded assessment and enables power "
    "analysis: how large would the true EITT delta need to be for us to detect it given "
    "our sample size?",
    styles['HufBodyText']
))

story.append(Paragraph("19.3 Effective D (Dimensionality Reduction)", styles['SubsectionHead']))
story.append(Paragraph(
    "In a D-component system, some components may be near-zero or perfectly correlated, "
    "reducing the effective dimensionality. D<sub>eff</sub> can be estimated from the "
    "eigenspectrum of the clr covariance matrix. If D<sub>eff</sub> << D, the Hessian "
    "bound should use D<sub>eff</sub> rather than D, producing a tighter (more useful) "
    "prediction. This is especially relevant for EXP-05 (cross-domain, D = 10) where "
    "some components may be linearly dependent.",
    styles['HufBodyText']
))

story.append(Paragraph("19.4 Regime-Aware EITT", styles['SubsectionHead']))
story.append(Paragraph(
    "EXP-01 showed that the Gold Standard era (0.96%) nearly breached the 1% threshold "
    "while other eras were far below. A regime-aware variant would: (a) detect structural "
    "breaks in the composition using CUSUM or Bai-Perron tests, (b) run EITT within each "
    "detected regime, (c) report per-regime verdicts alongside the global verdict. This "
    "prevents a single disrupted regime from masking otherwise excellent invariance.",
    styles['HufBodyText']
))

story.append(Paragraph("19.5 Tightened Bound for Near-Vertex Compositions", styles['SubsectionHead']))
story.append(Paragraph(
    "The EXP-01 Hessian bound is 1,100x loose on average at D = 2. The 1/delta term is "
    "the main contributor to looseness. For compositions that are <i>consistently</i> near "
    "a vertex (as opposed to occasionally visiting one), a tighter bound may exist. "
    "Specifically: if delta(t) is approximately constant (low velocity), the block geometric "
    "mean preserves the vertex proximity, and the entropy perturbation is controlled by "
    "the <i>variance of delta</i> rather than delta itself. A candidate tightened bound:",
    styles['HufBodyText']
))
story.append(Paragraph(
    "|delta_M| &lt;= (D-1) * var(delta) / (2 * mean(delta)^2 * M)",
    styles['Equation']
))
story.append(Paragraph(
    "This would replace the global delta with local statistics of delta, potentially "
    "reducing the bound by orders of magnitude for near-vertex systems like gold/silver. "
    "Validation of this tighter bound is a candidate for a Round 4 within EXP-01 or "
    "a dedicated section in EXP-06.",
    styles['HufBodyText']
))

story.append(Paragraph("19.6 Cross-Experiment Normalization via Gamma", styles['SubsectionHead']))
story.append(Paragraph(
    "The complexity parameter Gamma = (D-1) sigma<sub>A</sub><super>2</super> / "
    "(delta sqrt(N/M)) provides a single-number summary of how \"hard\" the EITT test is "
    "for a given system. Plotting |delta<sub>M</sub>|/H-bar against Gamma across all "
    "experiments would reveal whether EITT difficulty scales predictably with system "
    "complexity. If the relationship is monotone, Gamma becomes a pre-test screening "
    "metric: compute Gamma before running EITT to predict whether the test will be "
    "informative, marginal, or impossible.",
    styles['HufBodyText']
))

story.append(Paragraph("19.7 HUF-GOV Tool Certification Statement", styles['SubsectionHead']))
story.append(Paragraph(
    "The HUF-GOV canonical definition: \"A tool that produces a verifiably clean usable "
    "output to a known degree of certainty.\" The EITT diagnostic pipeline, as specified "
    "in this section, meets this standard:",
    styles['HufBodyText']
))

cert_items = [
    "<b>Verifiably clean:</b> Every formula is explicit (Section 15). Every computation "
    "is non-accumulating (Section 17.2). Reproducibility is deterministic.",
    "<b>Usable output:</b> The 4-instrument dashboard (Section 14) produces an actionable "
    "reading (PASS / OK / CAUTION / ALARM / FAIL) with supporting evidence.",
    "<b>Known degree of certainty:</b> The Hessian bound (F5) provides a theoretical "
    "maximum error. The noise floor (F11) provides a statistical minimum detectable "
    "signal. The ETF (Section 16.2) quantifies the gap between theory and observation. "
    "The operating envelope (Section 18) defines where these guarantees hold.",
]
for item in cert_items:
    story.append(Paragraph(item, styles['HufBodyText']))

story.append(Spacer(1, 10))
story.append(Paragraph(
    "This tool specification is the gold standard. Every future experiment inherits "
    "this pipeline, these formulas, this state machine, and these safety boundaries. "
    "Deviations must be documented and justified. Extensions must be validated against "
    "the D = 2 baseline before deployment at higher dimensions.",
    styles['CommentStyle']
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════
# 20. REGRESSION CHAIN METHODOLOGY (HIVP)
# ═══════════════════════════════════════════════════════════════════════
story.append(Paragraph("20. Regression Chain Methodology", styles['SectionHead']))
story.append(make_hr())

story.append(Paragraph(
    "Higgins Iterative Validation Protocol (HIVP) — P. Higgins, April 16, 2026",
    styles['InjectionHead']
))

story.append(Paragraph(
    "Every new experiment (DUT — Device Under Test) produces feedforward results and "
    "modifications to the method. Before advancing to the next DUT, the modified concept "
    "is <b>regressed through all previous DUTs</b>. If any previous DUT fails under the "
    "modified concept, the feedforward result is either <b>fixed</b> (adjusted until all "
    "DUTs pass) or <b>rejected</b> (the modification is rolled back). The chain only "
    "advances when the entire history passes.",
    styles['HufBodyText']
))

story.append(Paragraph("20.1 Formal Protocol", styles['SubsectionHead']))
story.append(Paragraph(
    "1. RUN(DUT<sub>k</sub>) with current concept. "
    "2. COLLECT feedforward and modifications. "
    "3. APPLY modifications to produce candidate concept. "
    "4. RE-RUN all DUT<sub>1</sub> through DUT<sub>k-1</sub> with candidate concept. "
    "5. If ANY fail: FIX or REJECT modification, return to step 3. "
    "6. If ALL pass: adopt candidate concept, ADVANCE to DUT<sub>k+1</sub>.",
    styles['Equation']
))

story.append(Paragraph("20.2 Properties", styles['SubsectionHead']))

prop_items = [
    "<b>No forward-only science.</b> Every modification is tested against the full history. "
    "A finding from DUT<sub>5</sub> cannot silently break DUT<sub>1</sub>.",
    "<b>Chain grows monotonically.</b> Each successful DUT adds to the regression suite. "
    "The tool gets more reliable with each experiment, not less.",
    "<b>Fix-or-reject is binary.</b> No 'accept with reservations.' Either the modification "
    "passes all previous DUTs, or it doesn't advance.",
    "<b>Order matters.</b> The chain is ordered easy-to-hard (by Gamma). If a hard DUT "
    "forces a modification that breaks an easy DUT, something fundamental is wrong.",
    "<b>Termination.</b> The chain terminates when all DUTs pass (method validated) or "
    "when a modification cannot be fixed without breaking earlier DUTs (boundary of "
    "applicability found — itself a valuable finding).",
]
for item in prop_items:
    story.append(Paragraph(item, styles['HufBodyText']))

story.append(Paragraph("20.3 Current Chain State", styles['SubsectionHead']))

chain_headers = ['Step', 'DUT', 'Gamma', 'Status', 'Feedforward']
chain_rows = [
    ['1', 'EXP-01 Gold/Silver\n(D=2, N=624)', '0.89', 'PASS',
     'EITT holds 0.60% max;\nnoise floor; Hessian bound;\ndashboard architecture;\nGamma parameter'],
    ['2', 'EXP-02 Energy\n(D=7, N~60)', '~55', 'PENDING', '—'],
    ['3', 'EXP-03 Employment\n(D=5, N~30)', '~15', 'PENDING', '—'],
    ['4', 'EXP-04 Financial\n(D=4, N~250)', '~43', 'PENDING', '—'],
    ['5', 'EXP-05 Cross-domain\n(D=10, N~50)', '~360', 'PENDING', '—'],
]
story.append(make_table(chain_headers, chain_rows,
    col_widths=[0.4*inch, 1.3*inch, 0.6*inch, 0.7*inch, 2.4*inch], header_color=TEAL))

story.append(Spacer(1, 8))
story.append(Paragraph(
    "When EXP-02 completes, its modifications will be regressed against EXP-01. If EXP-01 "
    "still passes under the modified concept, the chain advances. If not, we fix or reject. "
    "This is the methodology that earns generality rather than assuming it.",
    styles['HufBodyText']
))

story.append(Paragraph("20.4 Why This Matters", styles['SubsectionHead']))
story.append(Paragraph(
    "Most scientific papers validate on one dataset and claim generality. The regression "
    "chain earns generality by testing every modification against every previous validation. "
    "In software engineering this is continuous integration. In manufacturing it is closed-loop "
    "process control. In science, it is almost never done systematically. The HIVP makes it "
    "the default: no advancement without full regression. The chain state table (above) is "
    "a living document that shows exactly which experiments have been cross-validated and "
    "which modifications have survived the full gauntlet.",
    styles['HufBodyText']
))

story.append(Paragraph(
    "This methodology is itself a contribution to the EITT tool specification. It answers "
    "the question 'how do you know this generalizes?' with: 'because every modification "
    "is regressed through the full chain, and the chain only advances when all previous "
    "steps pass.'",
    styles['CommentStyle']
))

# ═══════════════════════════════════════════════════════════════════════
# CLOSING
# ═══════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 24))
story.append(make_thick_hr())
story.append(Paragraph(
    "Higgins Unity Framework — Experiment Journal EXP-01 (Extended with Tool Specification)<br/>"
    "5 rounds | 20 sections | April 16, 2026<br/>"
    "github.com/PeterHiggins19/Higgins-Unity-Framework<br/>"
    "Contact: PeterHiggins@roguewaveaudio.com",
    ParagraphStyle('EndMatter', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11,
        textColor=MEDIUM_GRAY, alignment=TA_CENTER)
))

# ─── Build ───────────────────────────────────────────────────────────
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"Extended journal saved to: {output_path}")
print(f"Total pages: check PDF")
