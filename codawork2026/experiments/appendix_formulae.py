"""
SHARED APPENDIX GENERATOR
===========================
Produces a publication-ready Notation, Terminology & Formulae appendix
for any Higgins Decomposition PDF. Returns a list of ReportLab flowables.

Usage:
    from appendix_formulae import build_appendix
    story += build_appendix(styles_dict, section_start="A")
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)


# ── Colour constants ─────────────────────────────────────────────────────────
HBG   = HexColor('#0d1b2a')
HBG2  = HexColor('#0f3460')
RA    = HexColor('#f0f4f8')
BD    = HexColor('#adb5bd')
MATH_BG = HexColor('#f8f9fa')
TERM_BG = HexColor('#eef2f7')


def _ensure_styles(ss):
    """Return a dict of styles, creating any that are missing."""
    needed = {
        'AppH':    dict(parent='Heading1', fontSize=15, leading=19, spaceBefore=16,
                        spaceAfter=8, textColor=HBG, fontName='Helvetica-Bold'),
        'AppSubH': dict(parent='Heading2', fontSize=11, leading=14, spaceBefore=12,
                        spaceAfter=4, textColor=HexColor('#1a1a2e'), fontName='Helvetica-Bold'),
        'AppBody': dict(parent='Normal', fontSize=9.5, leading=13, spaceAfter=6,
                        fontName='Helvetica', alignment=TA_JUSTIFY),
        'AppMath': dict(parent='Normal', fontSize=9, leading=13, spaceAfter=6,
                        fontName='Courier', leftIndent=24, rightIndent=24,
                        textColor=HexColor('#1a1a2e'), backColor=MATH_BG),
        'AppTH':   dict(parent='Normal', fontSize=7.5, leading=9,
                        fontName='Helvetica-Bold', textColor=white),
        'AppTC':   dict(parent='Normal', fontSize=7.5, leading=9, fontName='Helvetica'),
        'AppTCB':  dict(parent='Normal', fontSize=7.5, leading=9, fontName='Helvetica-Bold'),
        'AppTCM':  dict(parent='Normal', fontSize=7.5, leading=9, fontName='Courier',
                        textColor=HexColor('#1a1a2e')),
        'AppCap':  dict(parent='Normal', fontSize=8, leading=10, spaceAfter=8,
                        fontName='Helvetica-Oblique', textColor=HexColor('#333333'),
                        alignment=TA_CENTER),
        'AppNote': dict(parent='Normal', fontSize=8.5, leading=11, spaceAfter=4,
                        fontName='Helvetica-Oblique', textColor=HexColor('#555555'),
                        leftIndent=18, rightIndent=18),
    }
    out = {}
    from reportlab.lib.styles import getSampleStyleSheet
    base = getSampleStyleSheet()
    for name, kw in needed.items():
        if name in ss:
            out[name] = ss[name]
        else:
            parent_name = kw.pop('parent')
            parent = base[parent_name]
            style = ParagraphStyle(name, parent=parent, **kw)
            out[name] = style
            # Put defaults back for next call
            kw['parent'] = parent_name
    return out


def _std_table(rows, widths, header_bg=HBG):
    """Build a consistently styled table."""
    t = Table(rows, colWidths=[w * inch for w in widths])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_bg),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, RA]),
        ('GRID', (0, 0), (-1, -1), 0.5, BD),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t


def build_appendix(user_styles=None, section_prefix="A"):
    """
    Build the complete Notation, Terminology & Formulae appendix.

    Parameters
    ----------
    user_styles : dict or reportlab StyleSheet, optional
        Existing styles to reuse. Missing styles are auto-created.
    section_prefix : str
        Letter/number prefix for appendix sections (default "A").

    Returns
    -------
    list of Flowables
        Ready to append to a ReportLab story list.
    """
    ss = _ensure_styles(user_styles or {})
    story = []

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # APPENDIX HEADER
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph(
        f"Appendix {section_prefix}: Notation, Terminology &amp; Formulae",
        ss['AppH']))
    story.append(Paragraph(
        "This appendix collects every symbol, term, and formula used in this document "
        "so that it may be read as a standalone work. Definitions follow the conventions "
        "of Aitchison (1986) for compositional data analysis and standard notation for "
        "information theory and statistical mechanics.",
        ss['AppBody']))

    # ═══════════════════════════════════════════════════════════════════════
    # A.1  NOTATION TABLE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph(f"{section_prefix}.1  Symbol Reference", ss['AppSubH']))

    hdr = [
        Paragraph('<b>Symbol</b>', ss['AppTH']),
        Paragraph('<b>Name</b>', ss['AppTH']),
        Paragraph('<b>Definition / Units</b>', ss['AppTH']),
    ]
    symbols = [
        ('x = (x<sub>1</sub>, ... , x<sub>D</sub>)',
         'Composition',
         'A vector on the D-part simplex S<super>D</super>: x<sub>i</sub> &gt; 0, sum = 1.'),
        ('D',
         'Number of parts',
         'Dimension of the compositional vector (e.g. D = 4 for SEMF).'),
        ('N',
         'Sample size',
         'Number of observations (rows) in the compositional time series.'),
        ('M',
         'Decimation level',
         'Number of blocks in EITT decimation. Range: M = 2 to floor(N/5).'),
        ('H(M)',
         'Shannon entropy at M',
         'H = -sum(p<sub>i</sub> ln p<sub>i</sub>), where p<sub>i</sub> are the block geometric-mean probabilities.'),
        ('H<sub>norm</sub>(M)',
         'Normalised entropy',
         'H<sub>norm</sub> = H(M) / ln(M). Scaled to [0, 1].'),
        ('H-bar(M)',
         'Mean normalised entropy',
         'H-bar = (1/D) sum<sub>c</sub> H<sub>norm,c</sub>(M). Average across all D components.'),
        ('PR',
         'Pass rate',
         'Fraction of tested M values where |H-bar(M) - H-bar(2)| &lt; 0.05.'),
        ('sigma<super>2</super><sub>A</sub>',
         'Aitchison variance (total variance)',
         'sigma<super>2</super><sub>A</sub> = (1/2D) sum<sub>i,j</sub> var(ln x<sub>i</sub>/x<sub>j</sub>) = (1/D) sum<sub>i</sub> var(clr<sub>i</sub>).'),
        ('clr(x)',
         'Centred log-ratio',
         'clr(x)<sub>i</sub> = ln(x<sub>i</sub>) - (1/D) sum<sub>j</sub> ln(x<sub>j</sub>). Maps simplex to R<super>D</super>.'),
        ('ilr(x)',
         'Isometric log-ratio',
         'ilr(x) = H &middot; clr(x), where H is the (D-1) x D Helmert contrast matrix. Isometry into R<super>D-1</super>.'),
        ('alr(x)',
         'Additive log-ratio',
         'alr(x)<sub>i</sub> = ln(x<sub>i</sub> / x<sub>ref</sub>). Not isometric. Reference-dependent.'),
        ('d<sub>A</sub>(x, y)',
         'Aitchison distance',
         'd<sub>A</sub> = || clr(x) - clr(y) ||<sub>2</sub>. The natural metric on the simplex.'),
        ('V',
         'Variation matrix',
         'V<sub>ij</sub> = var(ln(x<sub>i</sub>/x<sub>j</sub>)). D x D symmetric, zeros on diagonal.'),
        ('C(x)',
         'Closure operator',
         'C(x)<sub>i</sub> = x<sub>i</sub> / sum(x). Projects to the simplex.'),
        ('x (circleplus) y',
         'Perturbation',
         'x (circleplus) y = C(x<sub>1</sub>y<sub>1</sub>, ... , x<sub>D</sub>y<sub>D</sub>). The "addition" of CoDa.'),
        ('alpha (circledot) x',
         'Powering',
         'alpha (circledot) x = C(x<sub>1</sub><super>alpha</super>, ... , x<sub>D</sub><super>alpha</super>). The "scalar multiplication" of CoDa.'),
        ('M<sub>break</sub>',
         'Break point',
         'First M where relative EITT deviation exceeds 1%. Lock range width.'),
        ('F17',
         'F17 contamination tuner',
         'C<sub>geom</sub>(M) = |delta<sub>geom</sub> - delta<sub>arith</sub>| / H-bar. Detects anomalous coupling.'),
        ('F17<sub>norm</sub>',
         'Normalised F17',
         'F17<sub>norm</sub> = C<sub>geom</sub> / sigma<super>2</super><sub>A</sub>. Scale-invariant contamination alarm.'),
        ('S',
         'Thermodynamic entropy',
         'S = k<sub>B</sub>(beta E + ln Z). Gibbs entropy of the canonical ensemble.'),
        ('beta',
         'Inverse temperature',
         'beta = 1 / (k<sub>B</sub> T). Conjugate variable to energy.'),
        ('Z',
         'Partition function',
         'Z = sum<sub>i</sub> e<super>-beta E<sub>i</sub></super>. Normalisation of the Boltzmann distribution.'),
        ('phi',
         'Phase',
         'Quantum phase angle. E = hbar (d-phi/dt).'),
    ]

    rows = [hdr]
    for sym, name, defn in symbols:
        rows.append([
            Paragraph(sym, ss['AppTCM']),
            Paragraph(name, ss['AppTCB']),
            Paragraph(defn, ss['AppTC']),
        ])

    story.append(_std_table(rows, [1.8, 1.3, 3.6]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # A.2  TERMINOLOGY / GLOSSARY
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph(f"{section_prefix}.2  Glossary of Terms", ss['AppSubH']))

    terms = [
        ('EITT',
         'Entropy Invariance Two-pass Test',
         'The primary instrument. Tests whether Shannon entropy is invariant under '
         'geometric-mean block decimation across all scales M. Pass 1 classifies; Pass 2 '
         'applies F17, min-blocks guard, and stored energy alarm to marginal cases.'),
        ('CoDa',
         'Compositional Data Analysis',
         'The mathematical framework for data that sums to a constant (Aitchison, 1986). '
         'Operates in log-ratio coordinates (CLR, ILR, ALR) on the simplex.'),
        ('Simplex',
         'S<super>D</super> = {x in R<super>D</super> : x<sub>i</sub> &gt; 0, sum = 1}',
         'The sample space of compositions. A (D-1)-dimensional manifold in R<super>D</super>.'),
        ('LEGITIMATE',
         'EITT classification',
         'Pass rate &gt;= 80%. Entropy invariant under decimation. '
         'Thermodynamic interpretation: at a critical point (RG fixed point).'),
        ('FABRICATED',
         'EITT classification',
         'Pass rate &lt; 80%. Entropy varies with decimation. '
         'Thermodynamic interpretation: off-critical, signal has a characteristic energy scale.'),
        ('Geometric-mean decimation',
         'The EITT operator',
         'Partition N observations into M blocks. Within each block, compute the geometric '
         'mean: G = exp(mean(ln(x))). This preserves the Aitchison geometry of the simplex, '
         'unlike arithmetic means which introduce spurious correlations.'),
        ('Resolution boundary',
         'Instrument limit',
         'A classification where the instrument correctly reports that it cannot resolve '
         'the signal. Not a failure — the instrument is working by identifying the edge '
         'of its resolving power. Analogous to a PLL reporting out-of-lock.'),
        ('HIVP',
         'Higgins Iterative Validation Protocol',
         'The validation chain: each experiment must reproduce all prior results before '
         'extending to a new domain.'),
        ('PLL analogy',
         'Phase-locked loop',
         'EITT is formally analogous to a PLL. H-bar = VCO signal. M = time. '
         'Pass/fail = lock detect. Slope of EITT degradation = error voltage. '
         'M<sub>break</sub> = lock range boundary. F17 = phase noise alarm.'),
        ('Wick rotation',
         'Imaginary time = inverse temperature',
         'The substitution t to -i hbar / (k<sub>B</sub> T) maps quantum phase evolution '
         'e<super>i phi</super> to Boltzmann weighting e<super>-beta E</super>. '
         'Connects EITT decimation (resolution change) to temperature change.'),
        ('Kadanoff blocking',
         'Renormalization group decimation',
         'EITT geometric-mean block averaging is a Kadanoff blocking (RG) operation. '
         'Entropy invariance under blocking = RG fixed point = thermodynamic criticality.'),
        ('Stored energy attack',
         'Integrity test',
         'Deliberately injecting external correction factors into EITT. All five attack '
         'modes (calibration injection, entropy stuffing, cross-domain transplant, '
         'reverse engineering, progressive contamination) are detected by the F17 alarm.'),
        ('Rayleigh pattern',
         'Contamination response',
         'Progressive contamination produces a rise-peak-decay in pass count: the Rayleigh '
         'envelope. Same statistics as incoherent energy added to a coherent system '
         '(room acoustics, fading channels).'),
        ('SEMF',
         'Semi-Empirical Mass Formula',
         'The Weizsaecker liquid-drop model of nuclear binding energy: '
         'B = a<sub>V</sub>A - a<sub>S</sub>A<super>2/3</super> - a<sub>C</sub>Z(Z-1)A<super>-1/3</super> '
         '- a<sub>A</sub>(A-2Z)<super>2</super>/A + delta. Four terms = four-part composition.'),
        ('Valley of stability',
         'Nuclear chart trajectory',
         'The most stable isotope (highest B/A) at each mass number A. '
         'The 1D trajectory through the nuclear chart used for EITT analysis.'),
        ('Frechet mean',
         'Compositional centre',
         'The closure of the geometric mean: FM = C(exp(mean(ln(X)))). '
         'The natural centre of mass in Aitchison geometry.'),
        ('Simplicial depth',
         'Outlier measure',
         'Fraction of simplices formed by (D+1) sample points that contain x. '
         'Range 0 (outlier) to ~0.5 (central). Tukey depth adapted to the simplex.'),
    ]

    t_hdr = [
        Paragraph('<b>Term</b>', ss['AppTH']),
        Paragraph('<b>Full Name / Type</b>', ss['AppTH']),
        Paragraph('<b>Definition</b>', ss['AppTH']),
    ]
    t_rows = [t_hdr]
    for term, fullname, defn in terms:
        t_rows.append([
            Paragraph(f'<b>{term}</b>', ss['AppTCB']),
            Paragraph(fullname, ss['AppTC']),
            Paragraph(defn, ss['AppTC']),
        ])
    story.append(_std_table(t_rows, [1.3, 1.6, 3.8]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # A.3  COMPLETE FORMULA REFERENCE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph(f"{section_prefix}.3  Formula Reference", ss['AppSubH']))

    story.append(Paragraph(f"<b>{section_prefix}.3.1  EITT Core Formulae</b>", ss['AppBody']))

    formulas_eitt = [
        ('Geometric-mean block average',
         'G<sub>i</sub>(c, M)  =  exp( (1/B) sum<sub>k in block i</sub> ln x<sub>k,c</sub> )',
         'B = floor(N/M) observations per block. Applied independently per component c.'),
        ('Block probability',
         'p<sub>i</sub>(c, M)  =  G<sub>i</sub>(c, M) / sum<sub>j</sub> G<sub>j</sub>(c, M)',
         'Normalises geometric-mean blocks to a probability distribution over M bins.'),
        ('Shannon entropy per component',
         'H<sub>c</sub>(M)  =  - sum<sub>i=1</sub><super>M</super> p<sub>i</sub> ln p<sub>i</sub>',
         'Entropy in nats. Maximum value = ln(M) for uniform distribution.'),
        ('Normalised entropy',
         'H<sub>norm,c</sub>(M)  =  H<sub>c</sub>(M) / ln(M)',
         'Scaled to [0, 1]. Allows comparison across different M values.'),
        ('Mean normalised entropy',
         'H-bar(M)  =  (1/D) sum<sub>c=1</sub><super>D</super> H<sub>norm,c</sub>(M)',
         'The EITT signal. Average over all D compositional components.'),
        ('Pass criterion',
         '|H-bar(M) - H-bar(2)|  &lt;  0.05',
         'Each M is tested against the reference value H-bar(2).'),
        ('Pass rate',
         'PR  =  (number of M passing) / (number of M tested)',
         'PR &gt;= 0.80: LEGITIMATE.   PR &lt; 0.80: FABRICATED.'),
        ('EITT slope',
         'slope(M)  =  d(relative %)/dM',
         'Rate of entropy degradation. Flat = in lock (PLL analogy). Rising = losing lock.'),
    ]

    f_hdr = [
        Paragraph('<b>Formula</b>', ss['AppTH']),
        Paragraph('<b>Expression</b>', ss['AppTH']),
        Paragraph('<b>Notes</b>', ss['AppTH']),
    ]
    f_rows = [f_hdr]
    for name, expr, note in formulas_eitt:
        f_rows.append([
            Paragraph(name, ss['AppTCB']),
            Paragraph(expr, ss['AppTCM']),
            Paragraph(note, ss['AppTC']),
        ])
    story.append(_std_table(f_rows, [1.6, 2.5, 2.6]))
    story.append(Spacer(1, 0.15 * inch))

    # ── CoDa Formulae ────────────────────────────────────────────────────
    story.append(Paragraph(f"<b>{section_prefix}.3.2  CoDa Core Formulae</b>", ss['AppBody']))

    formulas_coda = [
        ('Closure',
         'C(x)<sub>i</sub>  =  x<sub>i</sub> / sum<sub>j</sub> x<sub>j</sub>',
         'Projects any positive vector onto the simplex.'),
        ('CLR transform',
         'clr(x)<sub>i</sub>  =  ln(x<sub>i</sub>) - (1/D) sum<sub>j</sub> ln(x<sub>j</sub>)',
         'Maps simplex to R<super>D</super>. Sum of clr components = 0. Not injective (rank D-1).'),
        ('ILR transform',
         'ilr(x)  =  H &middot; clr(x)',
         'H = Helmert contrast matrix, (D-1) x D. Isometric bijection to R<super>D-1</super>.'),
        ('ALR transform',
         'alr(x)<sub>i</sub>  =  ln(x<sub>i</sub> / x<sub>D</sub>)',
         'Additive log-ratio. Simple but reference-dependent and non-isometric.'),
        ('Aitchison distance',
         'd<sub>A</sub>(x,y)  =  sqrt( sum<sub>i</sub> (clr(x)<sub>i</sub> - clr(y)<sub>i</sub>)<super>2</super> )',
         'Equivalent to || clr(x) - clr(y) ||<sub>2</sub>. The natural Riemannian metric.'),
        ('Aitchison variance',
         'sigma<super>2</super><sub>A</sub>  =  (1/2D) sum<sub>i,j</sub> V<sub>ij</sub>',
         'Total variance. Also = (1/D) sum<sub>i</sub> var(clr(X)<sub>i</sub>). Measures compositional spread.'),
        ('Variation matrix',
         'V<sub>ij</sub>  =  var( ln(X<sub>:,i</sub> / X<sub>:,j</sub>) )',
         'D x D symmetric. The fundamental dispersion measure in CoDa.'),
        ('Perturbation',
         'x (circleplus) y  =  C(x<sub>1</sub>y<sub>1</sub>, ..., x<sub>D</sub>y<sub>D</sub>)',
         'Group operation on the simplex. Isometry: d<sub>A</sub>(x+z, y+z) = d<sub>A</sub>(x,y).'),
        ('Powering',
         'alpha (circledot) x  =  C(x<sub>1</sub><super>alpha</super>, ..., x<sub>D</sub><super>alpha</super>)',
         'Scalar multiplication on the simplex. Scaling: d<sub>A</sub>(a*x, a*y) = |a| d<sub>A</sub>(x,y).'),
        ('Frechet mean',
         'FM(X)  =  C( exp( (1/N) sum<sub>k</sub> ln x<sub>k</sub> ) )',
         'The compositional centre of mass. Geometric mean, then closure.'),
    ]

    f_rows2 = [f_hdr]
    for name, expr, note in formulas_coda:
        f_rows2.append([
            Paragraph(name, ss['AppTCB']),
            Paragraph(expr, ss['AppTCM']),
            Paragraph(note, ss['AppTC']),
        ])
    story.append(_std_table(f_rows2, [1.6, 2.5, 2.6]))
    story.append(Spacer(1, 0.15 * inch))

    # ── F17 and Two-Pass Formulae ────────────────────────────────────────
    story.append(Paragraph(f"<b>{section_prefix}.3.3  F17 Contamination Tuner &amp; Two-Pass Instrument</b>",
                           ss['AppBody']))

    formulas_f17 = [
        ('F17 raw',
         'C<sub>geom</sub>(M) = |delta<sub>geom</sub> - delta<sub>arith</sub>| / H-bar(M)',
         'Measures gap between geometric and arithmetic decimation.'),
        ('F17 normalised',
         'F17<sub>norm</sub> = mean(C<sub>geom</sub>) / sigma<super>2</super><sub>A</sub>',
         'Scale-invariant. Threshold: F17<sub>norm</sub> &gt; 0.008 triggers alarm.'),
        ('Pass 2 tiebreaker',
         'If PR in [0.80, 0.95] AND F17<sub>norm</sub> &gt; 0.008:  reclassify FABRICATED',
         'Applied only to marginal cases. Catches entropy-stuffing attacks.'),
        ('Min-blocks guard',
         'Exclude M where floor(N/M) &lt; 5',
         'Insufficient data for reliable entropy estimation at high M.'),
        ('Stored energy alarm',
         'Flag if H-bar approaches ln(D)/ln(M) with high block variance',
         'Detects resonance artefacts that mimic legitimate behaviour.'),
    ]

    f_rows3 = [f_hdr]
    for name, expr, note in formulas_f17:
        f_rows3.append([
            Paragraph(name, ss['AppTCB']),
            Paragraph(expr, ss['AppTCM']),
            Paragraph(note, ss['AppTC']),
        ])
    story.append(_std_table(f_rows3, [1.6, 2.5, 2.6]))
    story.append(Spacer(1, 0.15 * inch))

    # ── Thermodynamic Formulae ───────────────────────────────────────────
    story.append(Paragraph(f"<b>{section_prefix}.3.4  Thermodynamic Framework</b>", ss['AppBody']))

    formulas_thermo = [
        ('Master formula',
         'S  =  (hbar / T)(d-phi / dt)  +  k<sub>B</sub> ln Z',
         'Entropy = energetic (phase velocity) + combinatorial (state counting).'),
        ('Energy-phase relation',
         'E  =  hbar (d-phi / dt)',
         'Energy is the rate of quantum phase change.'),
        ('Gibbs entropy',
         'S  =  k<sub>B</sub>( beta E  +  ln Z )',
         'From the canonical ensemble. beta = 1/(k<sub>B</sub> T).'),
        ('Wick rotation',
         't  to  -i hbar / (k<sub>B</sub> T)',
         'Maps quantum phase e<super>i phi</super> to Boltzmann weight e<super>-beta E</super>.'),
        ('Effective temperature',
         'T<sub>eff</sub>  =  M / N',
         'EITT decimation level as temperature. Small M = cold. Large M = hot.'),
        ('Criticality condition',
         'dH-bar / dM  =  0   for all M',
         'Entropy independent of temperature = RG fixed point = critical point.'),
        ('RG beta function',
         'beta<sub>H</sub>(M)  =  M &middot; dH / dM  =  0  iff legitimate',
         'The Callan-Symanzik equation for the EITT flow.'),
    ]

    f_rows4 = [f_hdr]
    for name, expr, note in formulas_thermo:
        f_rows4.append([
            Paragraph(name, ss['AppTCB']),
            Paragraph(expr, ss['AppTCM']),
            Paragraph(note, ss['AppTC']),
        ])
    story.append(_std_table(f_rows4, [1.6, 2.5, 2.6]))
    story.append(Spacer(1, 0.15 * inch))

    # ── SEMF Formulae ────────────────────────────────────────────────────
    story.append(Paragraph(f"<b>{section_prefix}.3.5  SEMF (Nuclear Binding Energy)</b>", ss['AppBody']))

    formulas_semf = [
        ('Total binding energy',
         'B(Z,A) = a<sub>V</sub>A - a<sub>S</sub>A<super>2/3</super> - a<sub>C</sub>Z(Z-1)A<super>-1/3</super> - a<sub>A</sub>(A-2Z)<super>2</super>/A + delta',
         'Semi-empirical mass formula (Weizsaecker, 1935). delta = pairing term.'),
        ('Volume term',
         'B<sub>vol</sub> = a<sub>V</sub> A        (a<sub>V</sub> = 15.75 MeV)',
         'Bulk nuclear attraction. Proportional to mass number.'),
        ('Surface term',
         'B<sub>sur</sub> = a<sub>S</sub> A<super>2/3</super>        (a<sub>S</sub> = 17.80 MeV)',
         'Surface tension correction. Scales as surface area.'),
        ('Coulomb term',
         'B<sub>cou</sub> = a<sub>C</sub> Z(Z-1) A<super>-1/3</super>        (a<sub>C</sub> = 0.711 MeV)',
         'Proton electrostatic repulsion. Grows quadratically with Z.'),
        ('Asymmetry term',
         'B<sub>asy</sub> = a<sub>A</sub> (A-2Z)<super>2</super> / A        (a<sub>A</sub> = 23.70 MeV)',
         'Neutron-proton imbalance penalty. Favours N approx Z.'),
        ('SEMF 4-part composition',
         'x = C(B<sub>vol</sub>, B<sub>sur</sub>, B<sub>cou</sub>, B<sub>asy</sub>)',
         'Closure of the four term magnitudes to the simplex.'),
        ('sigma<super>2</super><sub>A</sub> as heat capacity',
         'Low sigma<super>2</super><sub>A</sub> = stable (iron peak, 2.4). High = unstable (light, 82).',
         'Maps nuclear stability landscape as compositional heat capacity.'),
    ]

    f_rows5 = [f_hdr]
    for name, expr, note in formulas_semf:
        f_rows5.append([
            Paragraph(name, ss['AppTCB']),
            Paragraph(expr, ss['AppTCM']),
            Paragraph(note, ss['AppTC']),
        ])
    story.append(_std_table(f_rows5, [1.6, 2.5, 2.6]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # A.4  THERMODYNAMIC DICTIONARY
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph(f"{section_prefix}.4  Thermodynamic Dictionary", ss['AppSubH']))
    story.append(Paragraph(
        "Each EITT quantity has a precise thermodynamic analogue. This table maps the "
        "information-theoretic framework to equilibrium statistical mechanics.",
        ss['AppBody']))

    td_hdr = [
        Paragraph('<b>EITT Quantity</b>', ss['AppTH']),
        Paragraph('<b>Thermodynamic Analogue</b>', ss['AppTH']),
        Paragraph('<b>Physical Interpretation</b>', ss['AppTH']),
    ]
    td_rows = [td_hdr]
    td_data = [
        ('H-bar(M)', 'Free energy F(T)', 'The state function evaluated at effective temperature M/N.'),
        ('dH-bar/dM = 0', 'Critical point (RG fixed point)', 'The system is scale-invariant. Entropy independent of resolution.'),
        ('sigma<super>2</super><sub>A</sub>', 'Heat capacity C<sub>V</sub>', 'How much the composition restructures when temperature changes. High = easily changed.'),
        ('M<sub>break</sub>', 'Critical temperature T<sub>c</sub>', 'The temperature at which the entropy phase transition occurs.'),
        ('F17', 'Latent heat L', 'Hidden energy discontinuity at a first-order transition.'),
        ('Stored energy', 'Excess free energy Delta-F', 'Energy above the critical manifold. Any injection = contamination.'),
        ('Pass rate', 'Phase diagram scan', 'Maps entropy across all temperatures. 100% = everywhere critical.'),
        ('LEGITIMATE', 'At criticality', 'Thermodynamic equilibrium. Maximum stability. RG fixed point.'),
        ('FABRICATED', 'Off-critical', 'Not at equilibrium. Wants to evolve: fuse (light nuclei) or fission (heavy).'),
        ('Resolution boundary', 'Thermometer range limit', 'Where the calorimeter can no longer distinguish signal from noise.'),
        ('Rayleigh envelope', 'Incoherent energy response', 'Rise-peak-decay under progressive contamination = noise + coherent signal statistics.'),
    ]
    for q, th, interp in td_data:
        td_rows.append([
            Paragraph(q, ss['AppTCB']),
            Paragraph(th, ss['AppTCB']),
            Paragraph(interp, ss['AppTC']),
        ])
    story.append(_std_table(td_rows, [1.5, 1.8, 3.4]))
    story.append(Spacer(1, 0.15 * inch))

    # ═══════════════════════════════════════════════════════════════════════
    # A.5  KEY THEOREMS AND PROPERTIES
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph(f"{section_prefix}.5  Key Theorems &amp; Properties", ss['AppSubH']))

    theorems = [
        ('Theorem 1: Entropy invariance',
         'For a legitimate compositional time series on S<super>D</super>, '
         'H-bar(M) is invariant (within threshold epsilon) under geometric-mean block '
         'decimation for all M in [2, floor(N/5)].'),
        ('Theorem 2: sigma<super>2</super><sub>A</sub> predicts M<sub>break</sub>',
         'The Aitchison variance sigma<super>2</super><sub>A</sub> of the full composition '
         'predicts the EITT break point M<sub>break</sub>. Higher sigma<super>2</super><sub>A</sub> '
         'implies earlier M<sub>break</sub>. This is not empirical — it follows from how block-averaging '
         'interacts with the variation matrix.'),
        ('Theorem 3: Geometric mean preserves Aitchison geometry',
         'The geometric mean is the Frechet mean in Aitchison distance. Block-averaging with geometric '
         'means preserves the log-ratio structure of the simplex. Arithmetic means do not.'),
        ('Theorem 4: F17 normalisation',
         'The raw F17 contamination signal C<sub>geom</sub> scales with sigma<super>2</super><sub>A</sub>. '
         'Normalising F17 by sigma<super>2</super><sub>A</sub> yields a scale-invariant alarm. '
         'An absolute threshold would destroy legitimate high-variance datasets.'),
        ('Property: Perturbation isometry',
         'd<sub>A</sub>(x (circleplus) z, y (circleplus) z) = d<sub>A</sub>(x, y). '
         'Translation on the simplex preserves distances. Verified to machine precision.'),
        ('Property: Powering scaling',
         'd<sub>A</sub>(alpha (circledot) x, alpha (circledot) y) = |alpha| &middot; d<sub>A</sub>(x, y). '
         'Scalar multiplication scales distances. Verified to machine precision.'),
        ('Property: CLR orthogonality',
         'sum<sub>i</sub> clr(x)<sub>i</sub> = 0 for all x. The CLR maps to a (D-1)-dimensional '
         'hyperplane in R<super>D</super>.'),
    ]

    for title, body in theorems:
        story.append(KeepTogether([
            Paragraph(f"<b>{title}</b>", ss['AppBody']),
            Paragraph(body, ss['AppNote']),
            Spacer(1, 0.06 * inch),
        ]))

    story.append(Spacer(1, 0.2 * inch))

    # ═══════════════════════════════════════════════════════════════════════
    # A.6  REFERENCES
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph(f"{section_prefix}.6  References", ss['AppSubH']))

    refs = [
        "Aitchison, J. (1986). <i>The Statistical Analysis of Compositional Data</i>. Chapman &amp; Hall.",
        "Pawlowsky-Glahn, V., Egozcue, J.J. &amp; Tolosana-Delgado, R. (2015). <i>Modeling and Analysis of Compositional Data</i>. Wiley.",
        "Egozcue, J.J., Pawlowsky-Glahn, V., Mateu-Figueras, G. &amp; Barcelo-Vidal, C. (2003). Isometric logratio transformations for compositional data analysis. <i>Mathematical Geology</i>, 35(3), 279-300.",
        "Shannon, C.E. (1948). A Mathematical Theory of Communication. <i>Bell System Technical Journal</i>, 27(3), 379-423.",
        "Kadanoff, L.P. (1966). Scaling Laws for Ising Models Near T<sub>c</sub>. <i>Physics</i>, 2(6), 263-272.",
        "Wilson, K.G. (1971). Renormalization Group and Critical Phenomena. <i>Physical Review B</i>, 4(9), 3174.",
        "Wilson, K.G. (1975). The renormalization group: Critical phenomena and the Kondo problem. <i>Reviews of Modern Physics</i>, 47(4), 773.",
        "Wick, G.C. (1954). Properties of Bethe-Salpeter Wave Functions. <i>Physical Review</i>, 96(4), 1124.",
        "Planck Collaboration (2020). Planck 2018 results. VI. Cosmological parameters. <i>A&amp;A</i>, 641, A6.",
        "Weizsaecker, C.F. von (1935). Zur Theorie der Kernmassen. <i>Zeitschrift fuer Physik</i>, 96, 431-458.",
        "Bethe, H.A. &amp; Bacher, R.F. (1936). Nuclear Physics A. <i>Reviews of Modern Physics</i>, 8, 82-229.",
        "Wang, M. et al. (2021). The AME 2020 atomic mass evaluation (II). <i>Chinese Physics C</i>, 45(3), 030003.",
        "Mayer, M.G. (1949). On Closed Shells in Nuclei. II. <i>Physical Review</i>, 75(12), 1969.",
        "Lunney, D., Pearson, J.M. &amp; Thibault, C. (2003). Recent trends in the determination of nuclear masses. <i>Reviews of Modern Physics</i>, 75(3), 1021.",
        "Butterworth, S. (1930). On the Theory of Filter Amplifiers. <i>Experimental Wireless</i>, 7, 536-541.",
    ]
    for i, ref in enumerate(refs):
        story.append(Paragraph(f"[{i+1}] {ref}",
                               ParagraphStyle(f'ref_{i}', parent=ss['AppTC'],
                                              fontSize=7.5, leading=9.5, spaceAfter=2,
                                              leftIndent=18, firstLineIndent=-18)))

    story.append(Spacer(1, 0.3 * inch))
    story.append(HRFlowable(width="50%", thickness=1, color=HBG))
    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph(
        "<i>End of Appendix. This document is self-contained.</i>",
        ss['AppCap']))

    return story
