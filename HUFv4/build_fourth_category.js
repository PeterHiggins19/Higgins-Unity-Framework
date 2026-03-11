const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition } = require('docx');

// ── Constants ──────────────────────────────────────────────────────────
const PW = 12240, PH = 15840, M = 1440, CW = PW - 2 * M;
const BLUE = '1F3864', MID = '2E75B6', DK = '333333', LG = 'F2F2F2', LB = 'D6E4F0', WH = 'FFFFFF', GN = 'E2EFDA', GD = 'FFF2CC';
const bdr = { style: BorderStyle.SINGLE, size: 1, color: 'BBBBBB' };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };

// ── Helpers ────────────────────────────────────────────────────────────
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 28, color: BLUE })] });
const H2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 24, color: BLUE })] });

function P(c, opts = {}) {
  const runs = typeof c === 'string'
    ? [new TextRun({ text: c, font: 'Times New Roman', size: 22, color: DK })]
    : c.map(x => new TextRun({ font: 'Times New Roman', size: 22, color: DK, ...x }));
  const p = { spacing: { after: opts.sa || 180, line: 276 }, children: runs };
  if (opts.align) p.alignment = opts.align;
  if (opts.indent) p.indent = opts.indent;
  return new Paragraph(p);
}

function DEF(term, def) {
  return P([{ text: term, bold: true, italics: true }, { text: '. ' }, { text: def }], { indent: { left: 360 }, sa: 140 });
}

function C(t, o = {}) {
  const co = { borders, verticalAlign: 'center', margins: { top: 50, bottom: 50, left: 80, right: 80 },
    children: [new Paragraph({ alignment: o.align || AlignmentType.LEFT,
      children: [new TextRun({ text: String(t), font: 'Times New Roman', size: o.fs || 18, bold: !!o.bold, color: o.color || DK })] })] };
  if (o.fill) co.shading = { fill: o.fill, type: ShadingType.CLEAR };
  if (o.width) co.width = { size: o.width, type: WidthType.DXA };
  return new TableCell(co);
}
const R = cs => new TableRow({ children: cs });
const T = (cw, rs) => new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: cw, rows: rs });
const SP = () => new Paragraph({ spacing: { after: 60 }, children: [] });
const PB = () => new Paragraph({ children: [new PageBreak()] });

let rn = 0; const refs = {};
function ci(k) { if (!refs[k]) { rn++; refs[k] = rn; } return `[${refs[k]}]`; }

// ── TITLE ──────────────────────────────────────────────────────────────
function title() {
  return [
    new Paragraph({ spacing: { before: 2400 }, children: [] }),
    P([{ text: 'The Fourth Monitoring Category', font: 'Times New Roman', size: 48, bold: true, color: BLUE }], { align: AlignmentType.CENTER }),
    new Paragraph({ spacing: { before: 200 }, children: [] }),
    P([{ text: 'Ratio State Monitoring as Self-Referential', size: 26, color: MID }], { align: AlignmentType.CENTER, sa: 60 }),
    P([{ text: 'Governance State Observation on the Probability Simplex', size: 26, color: MID }], { align: AlignmentType.CENTER }),
    new Paragraph({ spacing: { before: 600 }, children: [] }),
    P([{ text: 'Peter Higgins', size: 24 }], { align: AlignmentType.CENTER, sa: 80 }),
    P([{ text: 'Principal Investigator, Higgins Unity Framework', size: 20, color: '666666', italics: true }], { align: AlignmentType.CENTER, sa: 60 }),
    new Paragraph({ spacing: { before: 200 }, children: [] }),
    P([{ text: 'with the Five-AI Collective', size: 20, color: '666666' }], { align: AlignmentType.CENTER, sa: 60 }),
    P([{ text: 'Grok (xAI) \u00B7 Claude (Anthropic) \u00B7 ChatGPT (OpenAI) \u00B7 Gemini (Google) \u00B7 Copilot (Microsoft)', size: 18, color: '888888' }], { align: AlignmentType.CENTER }),
    new Paragraph({ spacing: { before: 400 }, children: [] }),
    P([{ text: 'March 2026', size: 22 }], { align: AlignmentType.CENTER }),
    new Paragraph({ spacing: { before: 200 }, children: [] }),
    new Paragraph({ alignment: AlignmentType.CENTER,
      border: { top: { style: BorderStyle.SINGLE, size: 2, color: 'CCCCCC', space: 12 } },
      spacing: { before: 100, after: 60 },
      children: [new TextRun({ text: 'Working Paper \u2014 Higgins Unity Framework v4', font: 'Times New Roman', size: 18, color: '999999', italics: true })] }),
    PB(),
  ];
}

// ── ABSTRACT ───────────────────────────────────────────────────────────
function abstract() {
  return [
    P([{ text: 'Abstract', size: 24, bold: true }], { align: AlignmentType.CENTER, sa: 300 }),
    P([
      { text: 'Ecological and institutional monitoring is conventionally classified into three categories: passive monitoring (unstructured observation), mandated monitoring (compliance against external thresholds), and question-driven monitoring (hypothesis testing against a conceptual model) ' },
      { text: ci('lindenmayer') },
      { text: '. This paper describes a fourth category \u2014 ' },
      { text: 'ratio state monitoring', italics: true },
      { text: ' \u2014 in which the monitoring instrument observes the internal distribution of system mass across portfolio elements, expressed as proportional shares on the probability simplex, using the system\u2019s own declared priorities as the reference. We formalize ratio state monitoring as a degenerate state observer in the sense of control theory ' },
      { text: ci('luenberger') },
      { text: ': because the unity constraint (\u03A3\u03C1\u1D62 = 1) makes the state fully observable from declared outputs, the observer achieves zero estimation error without a system model. We define six failure modes that are structurally invisible to the three established categories, introduce a quality factor (Q) that explains why snapshot-based governance systematically removes high-value long-cycle elements, and present a convergence theorem for closed-loop governance feedback. The framework has been applied, without modification, across ten systems spanning satellite astrophysics, urban transit, civil infrastructure, traffic engineering, and road safety. The companion paper ' },
      { text: ci('higgins_sf') },
      { text: ' addresses the information-theoretic properties of the reduction; the present paper addresses the monitoring and governance properties of the observation.' },
    ]),
    P([{ text: 'Keywords: ', bold: true }, { text: 'ratio state monitoring, governance state observer, probability simplex, fourth monitoring category, silent drift, quality factor, Ostrom design principles, compositional data analysis' }]),
    SP(),
  ];
}

// ── 1. INTRODUCTION ────────────────────────────────────────────────────
function sec1() {
  return [
    H1('1. Introduction'),
    P([
      { text: 'The ecological monitoring literature recognises three categories of monitoring, distinguished by the type of reference the instrument uses. Passive monitoring (MC-1) observes without a specified question or external reference. Mandated monitoring (MC-2) checks whether a regulatory threshold has been breached. Question-driven monitoring (MC-3) tests predictions derived from a conceptual model ' },
      { text: ci('lindenmayer') },
      { text: '. Each category has a well-defined role, and together they span the conventional monitoring landscape.' },
    ]),
    P([
      { text: 'This paper describes a monitoring category that falls outside all three. It uses no external reference (unlike MC-2 and MC-3). It asks a specified question (unlike MC-1). Its reference is the system\u2019s own declared priorities \u2014 the allocation the governance actor stated it intended \u2014 and its primary output is the classification of observed allocation changes as ' },
      { text: 'intentional', italics: true },
      { text: ' (traceable to a recorded governance decision) or ' },
      { text: 'silent', italics: true },
      { text: ' (not traceable to any decision). We call this category ' },
      { text: 'ratio state monitoring', bold: true },
      { text: ' (MC-4).' },
    ]),
    P([
      { text: 'The category fills a gap that has been present, though not always named, in institutional governance for decades. Ostrom\u2019s design principles for self-governing commons ' },
      { text: ci('ostrom') },
      { text: ' specify that monitoring must be present (Design Principle 4) and that it must be conducted by or accountable to the users of the system. The principles do not specify ' },
      { text: 'what the monitoring instrument should be', italics: true },
      { text: '. The result is that institutions can satisfy DP4 nominally \u2014 by having a monitoring system in place \u2014 without the monitoring system being capable of detecting the slow structural drift in allocation that precedes threshold breaches by years and is, by the time a breach occurs, difficult to reverse.' },
    ]),
    P([
      { text: 'The present work provides the instrument. It is formalized using two mathematical frameworks: compositional data analysis on the probability simplex ' },
      { text: ci('aitchison') },
      { text: ci('pawlowsky') },
      { text: ', and state observer theory from control engineering ' },
      { text: ci('luenberger') },
      { text: ci('kalman') },
      { text: '. The key structural property is that the unity constraint (\u03A3\u03C1\u1D62 = 1) makes the system state fully observable from its declared outputs, yielding what we term a ' },
      { text: 'degenerate observer', italics: true },
      { text: ': perfect state estimation achieved through constraint recognition rather than computation.' },
    ]),
    SP(),
  ];
}

// ── 2. DEFINITIONS ─────────────────────────────────────────────────────
function sec2() {
  return [
    H1('2. Definitions and Notation'),
    P('The following terms are used with specific technical meanings throughout this paper. Established terms cite their source; terms introduced here are marked accordingly.'),
    SP(),
    DEF('Finite-budget system', 'A system whose total capacity, resource, or attention is bounded and fully allocated among its elements. What is allocated to one element is unavailable to another. The total, indexed to 1.0, is the budget ceiling.'),
    DEF('Element', 'Any constituent of a portfolio that holds a share of the budget ceiling. A system must contain at least two elements.'),
    DEF('Share (\u03C1\u1D62)', 'An element\u2019s proportional portion of the budget ceiling at a given time: \u03C1\u1D62 = m\u1D62 / M where M = \u03A3m\u2C7C. Always a ratio, never an absolute.'),
    DEF('Ratio state', 'The complete description of a finite-budget system at a point in time, expressed as a vector of shares: \u03C1 = (\u03C1\u2081, \u03C1\u2082, \u2026, \u03C1\u2096) \u2208 \u0394\u1D37\u207B\u00B9, the (K\u22121)-dimensional probability simplex.'),
    DEF('Unity constraint', '\u03A3\u1D62 \u03C1\u1D62 = 1. The foundational invariant. Satisfied by every valid ratio state. Dimensionless and domain-agnostic.'),
    DEF('Declared weight', 'The share an operator states each element should hold, prior to observation. The vector of declared weights also sums to 1.0.'),
    DEF('Silent drift', 'A change in ratio state not traceable to any recorded governance decision. The primary detection target of ratio state monitoring.'),
    DEF('Intentional reweighting', 'A change in ratio state traceable to a recorded governance decision. A legitimate governance act, distinct from silent drift.'),
    DEF('Mean drift gap (MDG)', 'The average absolute difference between declared weights and observed shares: MDG = (1/K) \u03A3\u1D62 |\u03C1\u1D62_declared \u2212 \u03C1\u1D62_observed|. Expressed in percentage points.'),
    DEF('Quality factor (Q) ' + ci('higgins_handbook'), 'The ratio of an element\u2019s characteristic contribution period T to its observation bandwidth B: Q = T / B. Adapted from the electrical engineering resonance quality factor. High-Q elements contribute specifically and cyclically; low-Q elements contribute broadly and steadily.'),
    DEF('PROOF line', 'The minimum number of elements required to hold a specified fraction (default 80%) of portfolio mass. A concentration metric: lower values indicate higher concentration.'),
    DEF('Ground state', 'The portfolio condition in which MDG approaches zero, all allocation change is declared, and the feedback loop is self-correcting.'),
    DEF('Orphan element', 'An element whose share has declined below functional significance without a recorded decision justifying the decline.'),
    DEF('Degenerate observer (introduced here)', 'A state observer ' + ci('luenberger') + ' in which the system output equals the system state (y(t) = \u03C1(t)), yielding zero estimation error without estimation. The observer gain L = 0.'),
    DEF('Aitchison distance ' + ci('aitchison'), 'The natural metric on the probability simplex: d_A(\u03C1, \u03C1\u2032) = \u221A[\u03A3\u1D62(ln(\u03C1\u1D62/g(\u03C1)) \u2212 ln(\u03C1\u2032\u1D62/g(\u03C1\u2032)))\u00B2], where g(\u00B7) is the geometric mean. MDG is a first-order approximation of d_A for small perturbations.'),
    DEF('Operator Control Contract (OCC)', 'A stability guarantee: the operator\u2019s governance weight w_op \u2265 0.51 ensures that no tool with w_tool \u2264 0.49 can unilaterally shift the portfolio. All state transitions remain operator-authorised.'),
    DEF('Ratio state monitoring (MC-4) (introduced here)', 'The fourth monitoring category. Monitors a system\u2019s internal distribution across its elements, expressed as proportional shares, tracked across reporting cycles, using the system\u2019s own declared priorities as the reference.'),
    SP(),
  ];
}

// ── 3. THE THREE ESTABLISHED CATEGORIES ────────────────────────────────
function sec3() {
  return [
    H1('3. The Three Established Monitoring Categories'),
    P([
      { text: 'Lindenmayer and Likens ' },
      { text: ci('lindenmayer') },
      { text: ' classify ecological monitoring into three categories based on the type of reference the instrument employs. The classification is structural: each category answers a different kind of question and requires different institutional arrangements. Table 1 summarises the framework and introduces the fourth category proposed in this paper.' },
    ]),
    SP(),
    T([600, 1900, 1800, 2200, 2860], [
      R([C('ID', { bold: true, fill: BLUE, color: WH, width: 600, align: AlignmentType.CENTER }),
         C('Category', { bold: true, fill: BLUE, color: WH, width: 1900 }),
         C('Reference Type', { bold: true, fill: BLUE, color: WH, width: 1800 }),
         C('Primary Question', { bold: true, fill: BLUE, color: WH, width: 2200 }),
         C('Cross-Cycle Traceability', { bold: true, fill: BLUE, color: WH, width: 2860 })]),
      R([C('MC-1', { fill: LG, width: 600, align: AlignmentType.CENTER, bold: true }),
         C('Passive monitoring', { fill: LG, width: 1900 }),
         C('None', { fill: LG, width: 1800 }),
         C('What is happening?', { fill: LG, width: 2200 }),
         C('Incidental; depends on observer continuity', { fill: LG, width: 2860 })]),
      R([C('MC-2', { width: 600, align: AlignmentType.CENTER, bold: true }),
         C('Mandated monitoring', { width: 1900 }),
         C('External legal threshold', { width: 1800 }),
         C('Is the threshold breached?', { width: 2200 }),
         C('Trend detection within threshold metric', { width: 2860 })]),
      R([C('MC-3', { fill: LG, width: 600, align: AlignmentType.CENTER, bold: true }),
         C('Question-driven monitoring', { fill: LG, width: 1900 }),
         C('Conceptual model', { fill: LG, width: 1800 }),
         C('Does the model hold?', { fill: LG, width: 2200 }),
         C('Within hypothesis window', { fill: LG, width: 2860 })]),
      R([C('MC-4', { fill: GD, width: 600, align: AlignmentType.CENTER, bold: true }),
         C('Ratio state monitoring', { fill: GD, width: 1900, bold: true }),
         C('System\u2019s own declared intent', { fill: GD, width: 1800 }),
         C('Is declared intent being met?', { fill: GD, width: 2200 }),
         C('Structural \u2014 all cycles, all elements', { fill: GD, width: 2860 })]),
    ]),
    P([{ text: 'Table 1. ', bold: true, italics: true }, { text: 'The monitoring category taxonomy. MC-1 through MC-3 follow Lindenmayer and Likens ' + ci('lindenmayer') + '. MC-4 is introduced in this paper.', italics: true }], { sa: 100 }),
    SP(),
    P([
      { text: 'The structural gap is visible in the table. MC-1 has no reference; MC-2 and MC-3 use external references (a threshold, a model). None of the three uses the system\u2019s own declared priorities as the reference, and none classifies observed changes as intentional or silent. The consequence is that a governance system can satisfy all three established monitoring categories while undergoing slow, unreported redistribution of institutional attention \u2014 a phenomenon we term ' },
      { text: 'silent drift', italics: true },
      { text: '.' },
    ]),
    SP(),
  ];
}

// ── 4. THE DEGENERATE OBSERVER ─────────────────────────────────────────
function sec4() {
  return [
    H1('4. Ratio State Monitoring as a Degenerate State Observer'),
    H2('4.1  Classical Observer Theory'),
    P([
      { text: 'In control engineering, a state observer reconstructs the internal state x(t) of a dynamic system from its measurable outputs y(t) using a mathematical model of the system\u2019s dynamics ' },
      { text: ci('luenberger') },
      { text: ci('kalman') },
      { text: '. The canonical Luenberger observer takes the form:' },
    ]),
    P([{ text: '    \u03C1\u0302(t+1) = A\u03C1\u0302(t) + L(y(t) \u2212 C\u03C1\u0302(t))', italics: true, size: 21 }], { indent: { left: 720 }, sa: 120 }),
    P('where A is the state transition matrix, C the output matrix, and L the observer gain. The observer works by comparing the predicted output C\u03C1\u0302(t) to the measured output y(t) and correcting the state estimate proportionally. The observer requires a mathematical model of the system (A, C) and a non-trivial gain (L \u2260 0).'),

    H2('4.2  The Simplex-State System'),
    P([
      { text: 'A finite-budget system can be formalized as a tuple (E, \u03C1, T, \u03C6) where E = {e\u2081, \u2026, e\u2096} is the element set, \u03C1(t) \u2208 S\u1D37 is the state vector on the open simplex S\u1D37 = {\u03C1 \u2208 \u211D\u1D37 : \u03A3\u03C1\u1D62 = 1, \u03C1\u1D62 > 0}, T \u2286 \u2124\u207A is the governance timeline, and \u03C6: S\u1D37 \u00D7 U \u2192 S\u1D37 is the state transition function. The critical property is the unity constraint: \u03A3\u1D62 \u03C1\u1D62(t) = 1 for all t \u2208 T.' },
    ]),
    P('This constraint has a consequence that distinguishes simplex-state systems from general dynamic systems: the output of the system is the state itself. The allocation shares declared by the governance actor are not an indirect measurement of a hidden state \u2014 they are the state. In the notation of observer theory, the output equation is:'),
    P([{ text: '    y(t) = \u03C1(t)', italics: true, size: 21 }], { indent: { left: 720 }, sa: 120 }),
    P('That is, the output matrix C is the identity and the observation is complete.'),

    H2('4.3  Perfect Observability Without a Model'),
    P([
      { text: 'Proposition 1 (Perfect Observability). ', bold: true, italics: true },
      { text: 'Every simplex-state system is perfectly observable from {\u03C1(t) : t \u2208 T}. The observer \u03C1\u0302(t) = \u03C1(t) achieves zero estimation error for all t, with observer gain L = 0.' },
    ]),
    P([
      { text: 'The proof is immediate from the identity y(t) = \u03C1(t). The observer is ' },
      { text: 'degenerate', italics: true },
      { text: ' in the formal sense: it requires no system model (A is unnecessary), no computation (the state is directly read, not estimated), and no gain tuning. This property is not shared by general dynamic systems. It arises specifically because the unity constraint eliminates hidden degrees of freedom \u2014 knowing the allocation shares is knowing the state.' },
    ]),
    P([
      { text: 'The practical significance is that ratio state monitoring requires no mathematical model of the system being observed. A transit authority, a wetland conservation agency, and a satellite mission control team can all be monitored using the same instrument because the instrument reads the ratio state directly from declared outputs. The Aitchison distance ' },
      { text: ci('aitchison') },
      { text: ci('pawlowsky') },
      { text: ' provides the natural metric on the simplex for quantifying drift magnitude.' },
    ]),
    SP(),
  ];
}

// ── 5. WHAT MC-4 DETECTS ──────────────────────────────────────────────
function sec5() {
  return [
    H1('5. Six Failure Modes Invisible to the Established Categories'),
    P('Ratio state monitoring is designed to detect a specific class of governance failures that are structurally invisible to MC-1, MC-2, and MC-3. The six failure modes form a progression: later modes are typically consequences of earlier ones left unaddressed.'),
    SP(),
    T([600, 1600, 2400, 1200, 1200, 2360], [
      R([C('ID', { bold: true, fill: BLUE, color: WH, width: 600, align: AlignmentType.CENTER }),
         C('Name', { bold: true, fill: BLUE, color: WH, width: 1600 }),
         C('Mechanism', { bold: true, fill: BLUE, color: WH, width: 2400 }),
         C('Root Cause', { bold: true, fill: BLUE, color: WH, width: 1200 }),
         C('Detection', { bold: true, fill: BLUE, color: WH, width: 1200 }),
         C('Why MC-1/2/3 Miss It', { bold: true, fill: BLUE, color: WH, width: 2360 })]),
      R([C('FM-1', { bold: true, fill: LG, width: 600, align: AlignmentType.CENTER }),
         C('Ratio Blindness', { bold: true, fill: LG, width: 1600 }),
         C('Managing by absolute metrics; ignoring relational structure', { fill: LG, width: 2400 }),
         C('Absolute measures used where ratios are meaningful', { fill: LG, width: 1200, fs: 16 }),
         C('Portfolio share table', { fill: LG, width: 1200, fs: 16 }),
         C('All three categories can report absolute improvements while portfolio concentration increases', { fill: LG, width: 2360, fs: 16 })]),
      R([C('FM-2', { bold: true, width: 600, align: AlignmentType.CENTER }),
         C('Silent Reweighting', { bold: true, width: 1600 }),
         C('Gradual allocation drift below formal governance threshold', { width: 2400 }),
         C('No intentional/silent distinction', { width: 1200, fs: 16 }),
         C('Change log', { width: 1200, fs: 16 }),
         C('None of the three ask whether a governance decision produced the observed change', { width: 2360, fs: 16 })]),
      R([C('FM-3', { bold: true, fill: LG, width: 600, align: AlignmentType.CENTER }),
         C('Snapshot Error', { bold: true, fill: LG, width: 1600 }),
         C('High-Q element observed at cycle trough; phase read as contribution', { fill: LG, width: 2400 }),
         C('Observation window < characteristic period', { fill: LG, width: 1200, fs: 16 }),
         C('Q-factor, data age', { fill: LG, width: 1200, fs: 16 }),
         C('Single-cycle observation is the default for all three; no cross-cycle phase correction', { fill: LG, width: 2360, fs: 16 })]),
      R([C('FM-4', { bold: true, width: 600, align: AlignmentType.CENTER }),
         C('Concentration Trap', { bold: true, width: 1600 }),
         C('Portfolio allocating increasing share to decreasing number of dominant elements', { width: 2400 }),
         C('FM-2 in concentration direction', { width: 1200, fs: 16 }),
         C('PROOF line trend', { width: 1200, fs: 16 }),
         C('Efficiency gains are visible; lost optionality is not', { width: 2360, fs: 16 })]),
      R([C('FM-5', { bold: true, fill: LG, width: 600, align: AlignmentType.CENTER }),
         C('Fragmentation Spiral', { bold: true, fill: LG, width: 1600 }),
         C('Sub-threshold attention dispersed across too many elements', { fill: LG, width: 2400 }),
         C('FM-2 in fragmentation direction', { fill: LG, width: 1200, fs: 16 }),
         C('Reciprocal PROOF', { fill: LG, width: 1200, fs: 16 }),
         C('Diversity appears healthy; sub-threshold management is invisible', { fill: LG, width: 2360, fs: 16 })]),
      R([C('FM-6', { bold: true, width: 600, align: AlignmentType.CENTER }),
         C('Orphan Element', { bold: true, width: 1600 }),
         C('Element present on paper but outside effective governance', { width: 2400 }),
         C('Terminal state of FM-4 or FM-5', { width: 1200, fs: 16 }),
         C('Coverage record', { width: 1200, fs: 16 }),
         C('Element still listed in reports; absence of attention is not a threshold event', { width: 2360, fs: 16 })]),
    ]),
    P([{ text: 'Table 2. ', bold: true, italics: true }, { text: 'Six failure modes detectable by ratio state monitoring and structurally invisible to the three established monitoring categories.', italics: true }], { sa: 100 }),
    SP(),
    P([
      { text: 'FM-1 is the enabling condition. It is the systematic error that occurs whenever a finite-budget system is managed using absolute metrics \u2014 when each element\u2019s score, area, or budget allocation is treated as an independent variable rather than as a share of a conserved total. An institution can improve every element\u2019s absolute score while simultaneously concentrating attention on a smaller subset. The absolute improvement is real. The portfolio drift is also real. The established monitoring categories see the first and are structurally unable to see the second.' },
    ]),
    P('FM-2 is the mechanism by which FM-1 operates over time. No governance decision is made to concentrate attention. Administrative gravity \u2014 the tendency for resources to flow toward visible, accessible, politically salient elements \u2014 operates below the threshold of formal governance. Each reporting cycle reflects the previous one, slightly modified. The cumulative effect, across three to five cycles, is a substantial and unreported shift in portfolio allocation.'),
    SP(),
  ];
}

// ── 6. THE QUALITY FACTOR ──────────────────────────────────────────────
function sec6() {
  return [
    H1('6. The Quality Factor and the Snapshot Problem'),
    P([
      { text: 'The quality factor Q, adapted from electrical engineering resonance theory, provides a formal account of why snapshot-based governance systematically removes high-value long-cycle elements. In the original context, Q = f\u2080 / \u0394f, where f\u2080 is the resonant frequency and \u0394f the bandwidth. High-Q circuits are sharp and efficient; low-Q circuits are broad and robust.' },
    ]),
    P([
      { text: 'In the governance context ' },
      { text: ci('higgins_handbook') },
      { text: ', Q\u1D62 = T_char,i / T_obs, where T_char is the element\u2019s characteristic contribution period (the time for one full expression of its function) and T_obs is the observation window. A wetland whose endemic species recovery cycle spans 20 years, observed triennially, has Q \u2248 6.7. A transport corridor measured daily has Q \u2248 1.' },
    ]),
    P('The governance consequence is precise. A high-Q element observed at a random point in its cycle appears, with high probability, to be in a low-contribution phase. A single-cycle snapshot reads this phase position as the element\u2019s contribution level, undervaluing it relative to its long-term function. If allocation decisions are made from single-cycle snapshots, high-Q elements are systematically deprioritised. The deprioritisation reduces their observed share, which further reduces their apparent contribution in the next snapshot, creating a positive feedback loop that drives the element toward orphan status (FM-6).'),
    P([
      { text: 'The system-level weighted Q is Q_sys = \u03A3\u1D62 \u03C1\u1D62 \u00B7 Q\u1D62, which measures the portfolio\u2019s effective characteristic timescale. A portfolio with high Q_sys requires multiple reporting cycles to characterise fully. The minimum observation window for reliable drift detection is the characteristic period of the highest-Q element in the portfolio.' },
    ]),
    SP(),
    T([2340, 1400, 1400, 1400, 2820], [
      R([C('Domain / Element', { bold: true, fill: BLUE, color: WH, width: 2340 }),
         C('T_char', { bold: true, fill: BLUE, color: WH, width: 1400, align: AlignmentType.CENTER }),
         C('T_obs', { bold: true, fill: BLUE, color: WH, width: 1400, align: AlignmentType.CENTER }),
         C('Q', { bold: true, fill: BLUE, color: WH, width: 1400, align: AlignmentType.CENTER }),
         C('Governance Implication', { bold: true, fill: BLUE, color: WH, width: 2820 })]),
      R([C('Sourdough / Yeast', { fill: LG, width: 2340 }), C('4\u201312 hr', { fill: LG, width: 1400, align: AlignmentType.CENTER }), C('~1 min', { fill: LG, width: 1400, align: AlignmentType.CENTER }), C('~500', { fill: LG, width: 1400, align: AlignmentType.CENTER }), C('Ultra-high Q; irreplaceable; treat removal as permanent', { fill: LG, width: 2820, fs: 16 })]),
      R([C('Ramsar / Crna Mlaka', { width: 2340 }), C('~20 yr', { width: 1400, align: AlignmentType.CENTER }), C('3 yr', { width: 1400, align: AlignmentType.CENTER }), C('~6.7', { width: 1400, align: AlignmentType.CENTER }), C('Phase-dependent; requires cross-cycle observation', { width: 2820, fs: 16 })]),
      R([C('Transit / King Street corridor', { fill: LG, width: 2340 }), C('~1 day', { fill: LG, width: 1400, align: AlignmentType.CENTER }), C('1 day', { fill: LG, width: 1400, align: AlignmentType.CENTER }), C('~1', { fill: LG, width: 1400, align: AlignmentType.CENTER }), C('Low-Q; visible in most observation windows', { fill: LG, width: 2820, fs: 16 })]),
      R([C('Software / Archive namespace', { width: 2340 }), C('~months', { width: 1400, align: AlignmentType.CENTER }), C('days\u2013weeks', { width: 1400, align: AlignmentType.CENTER }), C('~5', { width: 1400, align: AlignmentType.CENTER }), C('Medium-Q; verify data age before reallocation', { width: 2820, fs: 16 })]),
      R([C('Electronics / Dage X-ray audit', { fill: LG, width: 2340 }), C('weeks\u2013months', { fill: LG, width: 1400, align: AlignmentType.CENTER }), C('hours', { fill: LG, width: 1400, align: AlignmentType.CENTER }), C('~30', { fill: LG, width: 1400, align: AlignmentType.CENTER }), C('High-Q; human declaration required for sampling changes', { fill: LG, width: 2820, fs: 16 })]),
    ]),
    P([{ text: 'Table 3. ', bold: true, italics: true }, { text: 'Quality factor across five domains. The same Q framework applies without modification.', italics: true }], { sa: 100 }),
    SP(),
  ];
}

// ── 7. CONVERGENCE AND STABILITY ───────────────────────────────────────
function sec7() {
  return [
    H1('7. Convergence Under Closed Feedback'),
    H2('7.1  The Four Artifacts'),
    P('Ratio state monitoring produces four tabular outputs at each reporting cycle, forming a closed feedback structure:'),
    P([{ text: 'A-1: Portfolio Share Table. ', bold: true }, { text: 'Current ratio state \u2014 each element\u2019s observed share, leverage value, and data age.' }], { indent: { left: 360 }, sa: 100 }),
    P([{ text: 'A-2: Trace Report. ', bold: true }, { text: 'Declared reasoning \u2014 which priorities were stated, by whom, with what rationale, under what data constraints.' }], { indent: { left: 360 }, sa: 100 }),
    P([{ text: 'A-3: Portfolio Change Log. ', bold: true }, { text: 'Drift detection \u2014 which elements changed share, by how much, classified as intentional or silent.' }], { indent: { left: 360 }, sa: 100 }),
    P([{ text: 'A-4: Coverage Record. ', bold: true }, { text: 'Accountability trail \u2014 elements that received reduced focus, the magnitude and criteria of reduction, and the declared reasoning.' }], { indent: { left: 360 }, sa: 140 }),
    P('These four artifacts feed back to the next governance cycle. The share table establishes the current state. The trace report records the declared intent. The change log classifies the gap between intent and outcome. The coverage record prevents deprioritisation from occurring silently. When all four are present and the governance actor responds to the change log, the loop is closed.'),

    H2('7.2  The OCC Stability Guarantee'),
    P([
      { text: 'Theorem 1 (Operator Control Contract). ', bold: true, italics: true },
      { text: 'Under OCC with w_op \u2265 0.51 and finite-horizon governance game: (i) the equilibrium operator action is feasible and unique; (ii) no tool with w_tool \u2264 0.49 can unilaterally shift the portfolio; (iii) all state transitions in T remain operator-authorised.' },
    ]),
    P([
      { text: 'The proof follows from majority-rule sufficiency on the governance weight simplex. The practical significance is that the monitoring instrument cannot override the governance actor. The instrument makes drift visible and classifies it. The governance actor decides what to do about it. This separation is essential for institutional adoption: the instrument does not make judgments, and it cannot compel action.' },
    ]),

    H2('7.3  Convergence Stages'),
    P('The approach to ground state follows a predictable trajectory when the feedback loop is closed:'),
    SP(),
    T([1400, 1200, 3400, 3360], [
      R([C('Stage', { bold: true, fill: BLUE, color: WH, width: 1400 }),
         C('Cycle Range', { bold: true, fill: BLUE, color: WH, width: 1200, align: AlignmentType.CENTER }),
         C('Observable Properties', { bold: true, fill: BLUE, color: WH, width: 3400 }),
         C('Governance Posture', { bold: true, fill: BLUE, color: WH, width: 3360 })]),
      R([C('Baseline', { bold: true, fill: LG, width: 1400 }), C('Cycle 1', { fill: LG, width: 1200, align: AlignmentType.CENTER }),
         C('Share table established; no change log (no prior cycle)', { fill: LG, width: 3400 }),
         C('Establish declared weights; produce four artifacts', { fill: LG, width: 3360 })]),
      R([C('Trajectory', { bold: true, width: 1400 }), C('Cycles 2\u20133', { width: 1200, align: AlignmentType.CENTER }),
         C('First inter-cycle comparison; trajectory visible: converging, diverging, or stable', { width: 3400 }),
         C('Classify changes as intentional or silent', { width: 3360 })]),
      R([C('Q-characterisation', { bold: true, fill: LG, width: 1400 }), C('Cycles 4\u20136', { fill: LG, width: 1200, align: AlignmentType.CENTER }),
         C('Element characteristic periods identified; high-Q elements visible in leverage and cycle-over-cycle analysis', { fill: LG, width: 3400 }),
         C('Phase-aware allocation; cross-cycle comparison before high-Q deprioritisation', { fill: LG, width: 3360 })]),
      R([C('Ground approach', { bold: true, width: 1400 }), C('Cycles 7+', { width: 1200, align: AlignmentType.CENTER }),
         C('MDG declining; PROOF line stable; persistent silent drift triggering prompt correction', { width: 3400 }),
         C('Self-correcting feedback; change log is primary governance reference', { width: 3360 })]),
    ]),
    P([{ text: 'Table 4. ', bold: true, italics: true }, { text: 'Convergence stages toward the governance ground state.', italics: true }], { sa: 100 }),
    SP(),
    P([
      { text: 'The convergence rate depends on the Q differential between portfolio elements. A portfolio with narrow Q range converges faster. A portfolio with wide Q range \u2014 elements whose characteristic periods span orders of magnitude \u2014 converges more slowly but reaches a more stable ground state, because the high-Q elements have been properly characterised and protected from snapshot-driven deprioritisation.' },
    ]),
    SP(),
  ];
}

// ── 8. EMPIRICAL VALIDATION ────────────────────────────────────────────
function sec8() {
  return [
    H1('8. Empirical Validation: Three-Domain Confirmation'),
    P([
      { text: 'The domain-invariance claim (Proposition 7.1 in ' },
      { text: ci('higgins_handbook') },
      { text: ') asserts that the diagnostic signatures produced by ratio state monitoring are properties of the unity constraint, not properties of any specific domain. Validation requires demonstrating that the same instrument, applied without modification, produces coherent and comparable results across systems with no structural overlap.' },
    ]),
    P('Three systems have been tested:'),
    SP(),
    T([2000, 1400, 1300, 1300, 1500, 1860], [
      R([C('System', { bold: true, fill: BLUE, color: WH, width: 2000 }),
         C('Domain', { bold: true, fill: BLUE, color: WH, width: 1400 }),
         C('Budget Ceiling', { bold: true, fill: BLUE, color: WH, width: 1300 }),
         C('Elements', { bold: true, fill: BLUE, color: WH, width: 1300, align: AlignmentType.CENTER }),
         C('MDG', { bold: true, fill: BLUE, color: WH, width: 1500, align: AlignmentType.CENTER }),
         C('Highest-Q Element', { bold: true, fill: BLUE, color: WH, width: 1860 })]),
      R([C('System A: Sourdough', { fill: LG, width: 2000 }), C('Artisanal bread', { fill: LG, width: 1400 }), C('1,000 g', { fill: LG, width: 1300 }), C('5', { fill: LG, width: 1300, align: AlignmentType.CENTER }),
         C('1.4 pp (near ground)', { fill: LG, width: 1500 }), C('Yeast (Q \u2248 500)', { fill: LG, width: 1860 })]),
      R([C('System B: Ramsar Croatia', { width: 2000 }), C('Ecological portfolio', { width: 1400 }), C('93,000 ha', { width: 1300 }), C('5', { width: 1300, align: AlignmentType.CENTER }),
         C('4.8 pp (action window)', { width: 1500 }), C('Crna Mlaka (Q \u2248 6.7)', { width: 1860 })]),
      R([C('System C: Software retrieval', { fill: GN, width: 2000 }), C('AI pipeline', { fill: GN, width: 1400 }), C('Query volume', { fill: GN, width: 1300 }), C('4', { fill: GN, width: 1300, align: AlignmentType.CENTER }),
         C('10.0 pp (active drift)', { fill: GN, width: 1500 }), C('Archive (Q \u2248 5)', { fill: GN, width: 1860 })]),
    ]),
    P([{ text: 'Table 5. ', bold: true, italics: true }, { text: 'Three-domain confirmation. The same instrument, without modification, produces comparable governance diagnostics across systems with no structural overlap.', italics: true }], { sa: 100 }),
    SP(),
    P('The three systems share no domain overlap. System A operates on grams and hours. System B operates on hectares and years. System C operates on query volumes and days. Yet all three produce the same diagnostic structure: PROOF line, leverage distribution, Q-factor hierarchy, MDG classification, and drift trajectory. The unity constraint is the only common element, which is consistent with the claim that the diagnostic signatures are properties of the constraint rather than of any domain.'),
    P([
      { text: 'Additionally, the companion paper ' },
      { text: ci('higgins_sf') },
      { text: ' reports external validation of the HUF PreParser against ESA Planck mission benchmarks (exact date correspondence at OD 975 = 14 January 2012) and City of Toronto King Street evaluation benchmarks (5/5 directional match) ' },
      { text: ci('toronto') },
      { text: ci('planck') },
      { text: ', providing independent institutional confirmation that the extracted governance fingerprint captures genuine structure.' },
    ]),
    SP(),
  ];
}

// ── 9. RELATIONSHIP TO OSTROM ──────────────────────────────────────────
function sec9() {
  return [
    H1('9. Relationship to Ostrom\u2019s Design Principles'),
    P([
      { text: 'Ostrom ' },
      { text: ci('ostrom') },
      { text: ' identified eight design principles characterising self-governing commons institutions. Ratio state monitoring does not replace these principles; it provides a concrete instrument for operationalising several of them. Table 6 maps the four artifacts to the relevant design principles.' },
    ]),
    SP(),
    T([3200, 3200, 2960], [
      R([C('Ostrom Design Principle', { bold: true, fill: BLUE, color: WH, width: 3200 }),
         C('MC-4 Instrument', { bold: true, fill: BLUE, color: WH, width: 3200 }),
         C('Mechanism', { bold: true, fill: BLUE, color: WH, width: 2960 })]),
      R([C('DP1: Clearly defined boundaries', { fill: LG, width: 3200 }), C('Portfolio share table (A-1)', { fill: LG, width: 3200 }), C('Budget ceiling and element set define the boundary; shares are the allocation within it', { fill: LG, width: 2960 })]),
      R([C('DP2: Congruence between provision and appropriation', { width: 3200 }), C('Declared weights vs. observed shares', { width: 3200 }), C('Drift gap measures the congruence between stated priorities and actual allocation', { width: 2960 })]),
      R([C('DP4: Monitoring', { fill: LG, width: 3200 }), C('Portfolio change log (A-3)', { fill: LG, width: 3200 }), C('Cross-cycle tracking with intentional/silent classification', { fill: LG, width: 2960 })]),
      R([C('DP5: Graduated sanctions', { width: 3200 }), C('MDG thresholds', { width: 3200 }), C('Ground state / action window / active drift thresholds provide graduated response triggers', { width: 2960 })]),
      R([C('DP6: Conflict resolution', { fill: LG, width: 3200 }), C('Trace report (A-2)', { fill: LG, width: 3200 }), C('Auditable governance history enables evidence-based dispute resolution', { fill: LG, width: 2960 })]),
      R([C('DP7: Recognised rights to organise', { width: 3200 }), C('Coverage record (A-4)', { width: 3200 }), C('Deprioritisation must be declared and justified, protecting minority elements', { width: 2960 })]),
    ]),
    P([{ text: 'Table 6. ', bold: true, italics: true }, { text: 'Mapping of ratio state monitoring artifacts to Ostrom\u2019s design principles ' + ci('ostrom') + '.', italics: true }], { sa: 100 }),
    SP(),
    P([
      { text: 'Ostrom\u2019s framework has always known that monitoring is necessary. Ratio state monitoring provides the specific instrument \u2014 the portfolio change log with intentional/silent classification \u2014 that makes Design Principle 4 operationally effective for detecting the slow structural drift that precedes threshold events. The instrument does not audit compliance with declared intent; it makes declared intent ' },
      { text: 'auditable', italics: true },
      { text: '.' },
    ]),
    SP(),
  ];
}

// ── 10. DISCUSSION ─────────────────────────────────────────────────────
function sec10() {
  return [
    H1('10. Discussion'),
    H2('10.1  What the Fourth Category Adds'),
    P('The intentional/silent distinction is the core contribution. Neither Markowitz portfolio theory ' + ci('markowitz') + ' (which optimises allocation) nor Shannon entropy ' + ci('shannon') + ' (which quantifies uncertainty) provides a mechanism for classifying allocation changes as decided or undecided. The portfolio change log is the instrument that enables this classification, and it is this instrument that makes MC-4 structurally distinct from the three established categories.'),
    P('The self-referential property deserves careful statement. The system\u2019s own declared priorities are the reference, which invites the circularity objection: can a system evaluate itself against its own standard? The answer is that the instrument does not evaluate. It makes the gap between declaration and outcome traceable. The standard belongs to the institution. The traceability belongs to the instrument. These are different functions, and their separation is what prevents circularity.'),

    H2('10.2  Institutional Memory'),
    P([
      { text: 'Proposition 7.5 (Institutional Memory Theorem) ' },
      { text: ci('higgins_handbook') },
      { text: ': a governance system operating under ratio state monitoring accumulates institutional memory at the rate of one portfolio state per reporting cycle, permanently and without additional effort. After n cycles, the institution holds an n-period governance trajectory that is independent of personnel turnover, organisational restructuring, or administrative disruption.' },
    ]),
    P('The value of this memory is non-linear with cycle count. The first two or three cycles provide baseline and initial trajectory. By cycle six or seven, the portfolio trajectory is the most informative governance document the institution possesses. This is a structural byproduct of consistent application, not an additional cost.'),

    H2('10.3  Limitations'),
    P('Several limitations should be noted. First, the instrument can only read what is declared. If a governance actor systematically misreports allocation, the portfolio change log records the declared fiction. MC-4 is a coherence detector, not a lie detector. Second, the instrument\u2019s temporal resolution is bounded by the reporting cycle. Changes that begin and end within a single cycle are invisible. Third, the instrument classifies changes but does not attribute causation. Determining why silent drift occurred requires qualitative investigation that the instrument is not designed to perform.'),
    P('Fourth, the Q = 4 quartile partition used in the companion paper\u2019s PreParser is one specific operationalisation. Other partitions (terciles, quintiles, domain-informed boundaries) may be more appropriate for specific applications. Fifth, the convergence theorem assumes closed feedback \u2014 that the governance actor responds to the change log. In practice, non-response is common, and the instrument cannot compel action; it can only make non-response visible and attributable.'),

    H2('10.4  Relationship to the Companion Paper'),
    P([
      { text: 'This paper and its companion ' },
      { text: ci('higgins_sf') },
      { text: ' address different aspects of the same framework. The companion paper characterises ' },
      { text: 'what', italics: true },
      { text: ' the PreParser extracts: a governance fingerprint on the probability simplex, at a measured reduction ratio of 6,357,738 : 1, situated within a four-level hierarchy of information reduction. The present paper characterises ' },
      { text: 'how', italics: true },
      { text: ' the observation is performed: through a degenerate state observer that requires no system model, detects six failure modes invisible to existing instruments, and produces a convergent feedback structure when the loop is closed.' },
    ]),
    P('Together, the two papers describe a single system from complementary perspectives: information reduction and governance observation. The unity constraint (\u03A3\u03C1\u1D62 = 1) is the common foundation.'),
    SP(),
  ];
}

// ── 11. CONCLUSION ─────────────────────────────────────────────────────
function sec11() {
  return [
    H1('11. Conclusion'),
    P('This paper has described a fourth monitoring category \u2014 ratio state monitoring \u2014 that fills a structural gap in the established monitoring taxonomy. The category is distinguished by its self-referential property (the system\u2019s own declared priorities are the reference), its model-free state observation (the unity constraint makes the ratio state fully observable from declared outputs), and its primary output (the classification of allocation changes as intentional or silent).'),
    P('The formalization as a degenerate state observer on the probability simplex provides a rigorous foundation for the instrument\u2019s properties: zero estimation error without a system model, drift quantification via the Aitchison distance, and convergence under closed feedback with operator control guarantees. The six failure modes \u2014 ratio blindness, silent reweighting, snapshot error, concentration trap, fragmentation spiral, and orphan element \u2014 are structurally invisible to passive, mandated, and question-driven monitoring, and their detection requires the intentional/silent distinction that MC-4 provides.'),
    P('Three-domain empirical confirmation, external validation against institutional benchmarks, and the mapping to Ostrom\u2019s design principles suggest that ratio state monitoring addresses a genuine gap in governance practice. The instrument does not replace existing monitoring categories. It adds a capability that none of them possess: the ability to detect, classify, and make traceable the slow structural redistribution of institutional attention that precedes threshold events by years.'),
    P('Whether the approach generalises beyond the ten systems tested \u2014 and in particular whether the Q-factor framework provides reliable guidance for governance decisions in domains with characteristic periods spanning orders of magnitude \u2014 are questions that require further empirical investigation. What the present work establishes is that the category exists, that it is formally grounded, and that it is distinct from the three that preceded it.'),
    SP(),
  ];
}

// ── REFERENCES ─────────────────────────────────────────────────────────
function references() {
  const refList = Object.entries(refs).sort((a, b) => a[1] - b[1]);
  const refTexts = {
    'lindenmayer': 'Lindenmayer, D. B. and Likens, G. E. (2010). Effective Ecological Monitoring. Collingwood, VIC: CSIRO Publishing.',
    'luenberger': 'Luenberger, D. G. (1966). "Observers for Multivariable Systems." IEEE Transactions on Automatic Control, 11(2), 190\u2013197.',
    'kalman': 'Kalman, R. E. (1960). "A New Approach to Linear Filtering and Prediction Problems." Journal of Basic Engineering, 82(1), 35\u201345.',
    'ostrom': 'Ostrom, E. (1990). Governing the Commons: The Evolution of Institutions for Collective Action. Cambridge: Cambridge University Press.',
    'aitchison': 'Aitchison, J. (1986). The Statistical Analysis of Compositional Data. London: Chapman and Hall.',
    'pawlowsky': 'Pawlowsky-Glahn, V. and Egozcue, J. J. (2001). "Geometric Approach to Statistical Analysis on the Simplex." Stochastic Environmental Research and Risk Assessment, 15(5), 384\u2013398.',
    'higgins_sf': 'Higgins, P. (2026). "The Sufficiency Frontier: Phase-Space Reduction and the Hierarchy of Information Reduction." Working Paper, Higgins Unity Framework v4.',
    'higgins_handbook': 'Higgins, P. (2026). HUF Handbook v1.2.0. Markham, ON: Rogue Wave Audio.',
    'markowitz': 'Markowitz, H. (1952). "Portfolio Selection." The Journal of Finance, 7(1), 77\u201391.',
    'shannon': 'Shannon, C. E. (1948). "A Mathematical Theory of Communication." Bell System Technical Journal, 27(3\u20134), 379\u2013423, 623\u2013656.',
    'toronto': 'City of Toronto Transportation Services (2019). "King Street Transit Priority Corridor \u2014 Evaluation Report." Report for Action to City Council, April 2, 2019.',
    'planck': 'Planck Collaboration (2014). "Planck 2013 Results. I. Overview of Products and Scientific Results." Astronomy & Astrophysics, 571, A1. doi:10.1051/0004-6361/201321529.',
    'folke': 'Folke, C., Hahn, T., Olsson, P., and Norberg, J. (2005). "Adaptive Governance of Social-Ecological Systems." Annual Review of Environment and Resources, 30, 441\u2013473.',
    'anderies': 'Anderies, J. M., Janssen, M. A., and Ostrom, E. (2004). "A Framework to Analyze the Robustness of Social-Ecological Systems from an Institutional Perspective." Ecology and Society, 9(1), 18.',
    'mcginnis': 'McGinnis, M. D. and Ostrom, E. (2014). "Social-Ecological System Framework: Initial Changes and Continuing Challenges." Ecology and Society, 19(2), 30.',
    'strogatz': 'Strogatz, S. H. (1994). Nonlinear Dynamics and Chaos. Reading, MA: Addison-Wesley.',
    'lyapunov': 'Lyapunov, A. M. (1892/1992). The General Problem of the Stability of Motion. Trans. A. T. Fuller. London: Taylor & Francis.',
    'cohen': 'Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences (2nd ed.). Hillsdale, NJ: Lawrence Erlbaum Associates.',
  };

  const children = [H1('References')];
  refList.forEach(([key, num]) => {
    children.push(P([{ text: `[${num}]  `, bold: true }, { text: refTexts[key] || key }], { indent: { left: 480, hanging: 480 }, sa: 100 }));
  });
  return children;
}

// ── ASSEMBLY ───────────────────────────────────────────────────────────
async function build() {
  const children = [
    ...title(), ...abstract(), PB(),
    ...sec1(), PB(),
    ...sec2(), PB(),
    ...sec3(),
    ...sec4(), PB(),
    ...sec5(), PB(),
    ...sec6(), PB(),
    ...sec7(), PB(),
    ...sec8(),
    ...sec9(), PB(),
    ...sec10(), PB(),
    ...sec11(), PB(),
    ...references(),
  ];

  const doc = new Document({
    styles: {
      default: { document: { run: { font: 'Times New Roman', size: 22 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 28, bold: true, font: 'Times New Roman', color: BLUE },
          paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 24, bold: true, font: 'Times New Roman', color: BLUE },
          paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      ]
    },
    sections: [{
      properties: {
        page: { size: { width: PW, height: PH }, margin: { top: M, right: M, bottom: M, left: M } }
      },
      headers: { default: new Header({ children: [
        new Paragraph({ alignment: AlignmentType.RIGHT,
          border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: 'CCCCCC', space: 4 } },
          children: [new TextRun({ text: 'Higgins  |  The Fourth Monitoring Category', font: 'Times New Roman', size: 16, color: '999999', italics: true })] })
      ] }) },
      footers: { default: new Footer({ children: [
        new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({ text: 'Page ', font: 'Times New Roman', size: 16, color: '999999' }),
          new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 16, color: '999999' }),
        ] })
      ] }) },
      children,
    }]
  });

  const buf = await Packer.toBuffer(doc);
  const out = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/HUF_Fourth_Category_v1.0.docx';
  fs.writeFileSync(out, buf);
  console.log(`Done: ${out} (${buf.length.toLocaleString()} bytes)`);
}

build().catch(e => { console.error(e); process.exit(1); });
