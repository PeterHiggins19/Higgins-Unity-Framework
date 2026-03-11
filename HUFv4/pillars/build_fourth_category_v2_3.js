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

function crossRef(text) {
  return new Paragraph({ spacing: { before: 80, after: 160 },
    children: [new TextRun({ text: '\u25B6 ' + text, font: 'Times New Roman', size: 20, italics: true, color: MID })] });
}

function hc(t, w) {
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA },
    shading: { fill: BLUE, type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: t, font: 'Times New Roman', size: 20, bold: true, color: WH })] })] });
}
function dc(t, w, opts = {}) {
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA },
    shading: opts.shade ? { fill: opts.shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    children: [new Paragraph({ alignment: opts.align || AlignmentType.LEFT,
      children: [new TextRun({ text: String(t), font: 'Times New Roman', size: 20, color: DK, bold: opts.bold || false })] })] });
}
function makeT(hds, rows, ws) {
  const tw = ws.reduce((a, b) => a + b, 0);
  return new Table({ width: { size: tw, type: WidthType.DXA }, columnWidths: ws,
    rows: [
      new TableRow({ children: hds.map((h, i) => hc(h, ws[i])) }),
      ...rows.map((r, ri) => new TableRow({ children: r.map((c, ci) => dc(c, ws[ci], { shade: ri % 2 === 0 ? LG : undefined })) })),
    ] });
}

// ══════════════════════════════════════════════════════════════════════
const ch = [];

// ── TITLE ───────────────────────────────────────────────────────────
ch.push(
  new Paragraph({ spacing: { before: 3000 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: 'THE FOURTH MONITORING CATEGORY', font: 'Times New Roman', size: 44, bold: true, color: BLUE })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: 'Ratio State Monitoring as a Degenerate State Observer', font: 'Times New Roman', size: 28, color: MID })] }),
  new Paragraph({ spacing: { before: 400 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'Pillar 2 of the HUF Triad \u00B7 Version 2.3', font: 'Times New Roman', size: 24, italics: true, color: DK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'March 2026', font: 'Times New Roman', size: 22, color: DK })] }),
  new Paragraph({ spacing: { before: 600 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: 'Peter Higgins', font: 'Times New Roman', size: 22, bold: true, color: DK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: 'Rogue Wave Audio, Markham, Ontario', font: 'Times New Roman', size: 20, color: DK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'HUF v1.2.0 \u00B7 MIT License', font: 'Times New Roman', size: 20, color: '999999' })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── ABSTRACT ────────────────────────────────────────────────────────
ch.push(
  H1('Abstract'),
  P('Three monitoring categories are established in the environmental and governance literature: Passive (MC-1), Mandated (MC-2), and Question-driven (MC-3). This paper introduces a fourth: Ratio State Monitoring (MC-4). MC-4 is structurally distinct from its predecessors in five properties: it is self-referential (uses the system\u2019s own declared intent as its reference), non-invasive (reads existing outputs), model-free (requires no mathematical model), bidirectional (detects concentration and fragmentation under the same constraint), and cross-cycle (produces a traceable governance record across all reporting periods). The mathematical basis is the degenerate state observer: on the probability simplex, the state IS the output, the estimation gain is zero, and the estimation error is identically zero without requiring a dynamic model. We identify six structurally invisible failure modes, derive the Quality Factor Q that explains systematic underweighting of high-cycle elements, map the framework to Ostrom\u2019s design principles for commons governance, and present three-domain empirical confirmation. This expanded version (v2.3) includes the Car/Fuel Dashboard analogy for intuitive understanding of MC-4 monitoring, Dynamic OCC Drift Monitoring with real-time ratio oscillation detection, Dynamic Portfolio Gating with adaptive thresholds, full data tables, Toronto King Street causal analysis, 13 open conjectures from the collective review, and cross-references to the HUF Triad.'),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── 1. INTRODUCTION ─────────────────────────────────────────────────
ch.push(
  H1('1. Introduction'),
  P('Monitoring is the systematic observation of a system\u2019s state for the purpose of informing governance decisions. The ecological monitoring literature recognizes three categories, distinguished by their reference standard: Passive monitoring (MC-1) observes without a structured reference; Mandated monitoring (MC-2) compares against external legal thresholds; Question-driven monitoring (MC-3) tests a conceptual model [1, 2].'),
  P('Each category has a blind spot. MC-1 detects events but cannot attribute them. MC-2 detects threshold breaches but ignores structural changes below the threshold. MC-3 detects model violations but cannot see what falls outside its hypothesis frame. All three share a deeper limitation: they cannot distinguish between intentional allocation changes and silent drift in a system\u2019s resource distribution [3].'),
  P('This paper introduces a fourth monitoring category\u2014Ratio State Monitoring (MC-4)\u2014that addresses this structural gap. MC-4 monitors the proportional allocation of a finite-budget system against its own declared priorities. It detects silent drift (undeclared reallocation), distinguishes it from intentional reweighting (declared reallocation), and produces a cross-cycle governance record. The instrument is the unity constraint: \u03A3\u03C1\u1D62 = 1, the tautological requirement that shares of a fixed total sum to that total.'),
  crossRef('Companion paper: Pillar 1, The Sufficiency Frontier'),
  crossRef('Triad overview: Volume 8, The Triad Synthesis'),
  crossRef('Operational implementation: Volume 5, Governance & Operations'),
);

// ── 2. DEFINITIONS ──────────────────────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('2. Definitions'),
  P('All terms are consistent with the HUF Triad unified glossary (Volume 8, Section 8). Terms are listed in dependency order.'),
  DEF('Budget ceiling (M)', 'The total of a finite-budget system, indexed to 1.0.'),
  DEF('Element (i)', 'Any constituent holding a share of the budget ceiling. Minimum two elements.'),
  DEF('Share (\u03C1\u1D62)', 'An element\u2019s proportion of the total: \u03C1\u1D62 = m\u1D62 / \u03A3m\u2C7C.'),
  DEF('Unity constraint', '\u03A3\u03C1\u1D62 = 1. The foundational invariant.'),
  DEF('Declared weight (\u03C1\u1D62\u1D48\u1D49\u1D9C)', 'The share an operator states each element should hold.'),
  DEF('Observed share (\u03C1\u1D62\u1D52\u1D47\u02E2)', 'The share an element actually holds, computed from outputs.'),
  DEF('Silent drift', 'Change in ratio state not traceable to a recorded governance decision.'),
  DEF('Intentional reweighting', 'Change traceable to a recorded governance decision.'),
  DEF('Mean drift gap (MDG)', '(1/K)\u03A3|\u03C1\u1D62\u1D48\u1D49\u1D9C \u2212 \u03C1\u1D62\u1D52\u1D47\u02E2|. Average drift across all elements.'),
  DEF('Leverage (1/\u03C1\u1D62)', 'Reciprocal of share. Sensitivity to removal.'),
  DEF('PROOF line', 'Minimum elements for 80% of portfolio mass.'),
  DEF('Quality factor (Q)', 'T_char/T_obs. Characteristic period to observation bandwidth ratio.'),
  DEF('Ground state', 'MDG \u2192 0. All change declared. Self-correcting feedback loop.'),
  DEF('Degenerate observer', 'State observer where y(t) = \u03C1(t). L = 0. Zero estimation error.'),
  DEF('Action window', 'Period during which correction is cheapest.'),
  DEF('Orphan element', 'Element present on paper but outside effective governance.'),
  DEF('OCC 51/49', 'Operator Control Contract: w_op \u2265 0.51, w_tool \u2264 0.49.'),
  DEF('Dynamic OCC drift', 'Real-time oscillation of the OCC ratio around the declared 51/49 nominal.'),
  DEF('Drift monitor', 'Instrument that tracks OCC ratio oscillation, tool depletion signals, and approaches to ground state.'),
  DEF('Portfolio gating', 'Dynamic inclusion/exclusion of elements based on observability threshold.'),
);

// ── 3. THREE ESTABLISHED CATEGORIES ─────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('3. Three Established Monitoring Categories'),
);
ch.push(makeT(
  ['Category', 'Reference', 'Primary Question', 'Intentional/Silent', 'Cross-Cycle'],
  [
    ['MC-1: Passive', 'None', 'What is happening?', 'Absent', 'Incidental'],
    ['MC-2: Mandated', 'External threshold', 'Is threshold breached?', 'Absent', 'Trend only'],
    ['MC-3: Question-driven', 'Conceptual model', 'Does the model hold?', 'Absent', 'Within hypothesis'],
    ['MC-4: Ratio State', 'Own declared intent', 'Is intent being met?', 'Primary output', 'Structural \u2014 all cycles'],
  ],
  [1500, 1700, 2200, 1800, 2160]
));
ch.push(
  P(''),
  P('MC-4\u2019s five defining properties distinguish it from the first three: (1) self-referential\u2014the system\u2019s own declared priorities serve as the reference; (2) non-invasive\u2014reads existing outputs without new data collection; (3) model-free\u2014requires no mathematical model of the system\u2019s dynamics; (4) bidirectional\u2014detects concentration and fragmentation under the same constraint; (5) cross-cycle\u2014produces a traceable governance record across all reporting periods.'),
);

// ── 4. THE DEGENERATE STATE OBSERVER ────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('4. The Degenerate State Observer'),
  P('In classical control theory, a state observer (Luenberger observer [4]) estimates internal states x(t) from outputs y(t) and a known dynamic model:'),
  P('\u0078\u0302\u2019(t) = A\u0078\u0302(t) + Bu(t) + L(y(t) \u2212 C\u0078\u0302(t))', { align: AlignmentType.CENTER }),
  P('where L is the observer gain chosen to make the estimation error e(t) = x(t) \u2212 \u0078\u0302(t) converge to zero. This requires: (a) a known system model (A, B, C), (b) observability of the pair (A, C), and (c) design of the gain matrix L.'),
  P([{ text: 'Proposition 1 (Perfect Observability). ', bold: true }, { text: 'On the probability simplex S\u1D37, the portfolio state \u03C1(t) is directly observable. The output equation is y(t) = \u03C1(t) (i.e., C = I, the identity). No dynamic model is required. The estimation gain L = 0, and the estimation error e(t) = 0 identically.' }]),
  P('Proof. Portfolio shares are defined as \u03C1\u1D62 = m\u1D62 / \u03A3m\u2C7C. The shares are computable from the system\u2019s own declared outputs without an intermediate model. Since y(t) = \u03C1(t), no estimation is performed; the state is read, not estimated. The estimation error is zero not by asymptotic convergence but by construction.'),
  P('This is a degenerate case in the technical sense: the observer collapses because the problem it is designed to solve\u2014estimating states from outputs\u2014does not arise. On the simplex, the state IS the output. This degeneracy is not a limitation; it is the foundation of MC-4\u2019s model-free property.'),
  crossRef('Mathematical foundations: Vol 3, Section 3'),
);

// ── 5. SIX FAILURE MODES ────────────────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('5. Six Failure Modes'),
  P('MC-4 identifies six structurally invisible failure modes. Each is invisible to MC-1 through MC-3 because they require the intentional/silent classification that only ratio state monitoring provides.'),
);
ch.push(makeT(
  ['ID', 'Name', 'Root Cause', 'Detection Artifact', 'Operational Flag'],
  [
    ['FM-1', 'Ratio Blindness', 'Using absolute metrics for proportional systems', 'Portfolio share table', 'MDG > 5pp'],
    ['FM-2', 'Silent Reweighting', 'No intentional/silent classification mechanism', 'Change log', 'Unattributed shift'],
    ['FM-3', 'Snapshot Error', 'Observation window shorter than characteristic period', 'Data-age flag', 'High leverage + stale data'],
    ['FM-4', 'Concentration Trap', 'FM-2 running in concentration direction', 'PROOF line trend', 'PROOF \u2264 2 or decreasing'],
    ['FM-5', 'Fragmentation Spiral', 'FM-2 running in fragmentation direction', 'Leverage distribution', 'Many small shares clustering'],
    ['FM-6', 'Orphan Element', 'FM-4 or FM-5 carried to element endpoint', 'Coverage record', 'Declining share, no rationale'],
  ],
  [600, 1600, 2200, 1800, 3160]
));
ch.push(
  P(''),
  P('The six modes form a progression. FM-1 (Ratio Blindness) is the enabling condition: without it, none of the others arise. FM-2 (Silent Reweighting) is the mechanism. FM-3 amplifies FM-2 by making high-Q elements look unresponsive. FM-4 and FM-5 are directional variants of FM-2. FM-6 is the terminal state for any element caught in FM-4 or FM-5.'),
  crossRef('Operational field guide: Vol 5, Section 3'),
  crossRef('Interactive examples: Vol 0, Notebooks 1\u20132 (pizza, backpack)'),
);

// ── 6. QUALITY FACTOR Q ─────────────────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('6. The Quality Factor'),
  P('Q = T_char / T_obs quantifies an element\u2019s vulnerability to snapshot error. High-Q elements contribute in narrow time windows relative to the observation period, making them systematically underweighted by single-cycle assessment.'),
);
ch.push(makeT(
  ['Domain', 'Element', 'T_char', 'T_obs', 'Q', 'Governance Risk'],
  [
    ['Sourdough', 'Yeast', '4\u201312 hours', '~0.02 hours', '~833', 'Ultra-high: removal kills the loaf'],
    ['Ramsar', 'Crna Mlaka', 'Multi-year', '~3 months', '~12', 'High: survey timing matters'],
    ['Software', 'Archive NS', 'Months', 'Days\u2013weeks', '~5', 'Medium: research-event driven'],
    ['Transit', 'Line 4 Sheppard', 'Seasonal', 'Daily counts', '~3', 'Low: broadly visible'],
    ['Planck HFI', '100 GHz', 'Continuous', 'Each OD', '~1', 'Low: always visible'],
  ],
  [1100, 1300, 1200, 1200, 700, 3860]
));
ch.push(
  P(''),
  P('The Q factor explains a systematic deprioritization mechanism: high-Q elements are measured during troughs and judged unimportant, justifying further funding cuts, creating a positive feedback loop. The coverage record (Artifact A-4) is the governance instrument that breaks this loop by requiring documented rationale for any deprioritization of a high-Q element.'),
);

// ── 7. CONVERGENCE AND FOUR ARTIFACTS ───────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('7. Convergence to Ground State'),
  H2('7.1 Four Artifacts'),
  P('MC-4 produces four standard outputs at each reporting cycle: A-1 (Portfolio Share Table) providing the instantaneous snapshot; A-2 (Trace Report) recording declared reasoning; A-3 (Portfolio Change Log) classifying each change as intentional or silent; A-4 (Coverage Record) documenting deprioritization decisions. All four are plain tabular CSV files that attach to existing governance reporting.'),
  H2('7.2 The OCC Theorem'),
  P([{ text: 'Theorem 1 (Operator Control). ', bold: true }, { text: 'Under the OCC 51/49, every governance decision requires w_op \u2265 0.51 operator weight. The tool (HUF) provides diagnostic information with w_tool \u2264 0.49. No automated action is taken without operator declaration. The governance record attributes every decision to a named authority.' }]),
  H2('7.3 Convergence Stages'),
);
ch.push(makeT(
  ['Stage', 'Cycle', 'Observable Properties', 'Governance Posture'],
  [
    ['Baseline', '1', 'First share table; no change log', 'Establish declared weights'],
    ['Trajectory', '2\u20133', 'First inter-cycle comparison; trend visible', 'Begin classifying changes'],
    ['Q-characterization', '4\u20136', 'Element cycles identified; orphan alerts', 'Phase-aware allocation'],
    ['Ground approach', '7+', 'MDG declining; PROOF stable', 'Self-correcting feedback'],
    ['Ground state', 'Variable', 'MDG \u2248 0; all change declared', 'Self-governing'],
  ],
  [1500, 800, 3500, 3560]
));
ch.push(
  P(''),
  H2('7.4 Institutional Memory (New in v2.0)'),
  P([{ text: 'Proposition 7.5. ', bold: true }, { text: 'A governance system operating under MC-4 accumulates institutional memory at the rate of one portfolio state per reporting cycle, permanently and without additional effort. After n cycles, the institution holds an n-period governance trajectory that is independent of personnel turnover, organizational restructuring, or administrative disruption.' }]),
  P('The value of the institutional memory is non-linear with cycle count. The first two or three cycles provide thin context. By cycle six or seven, the trajectory becomes the most valuable governance document the institution possesses. The record captures not just what happened, but what was declared, what was detected, and what was done about it.'),
  crossRef('Proof: Vol 3, Mathematical Foundations'),
  crossRef('Operational deployment: Vol 5, Sections 3\u20135'),
);

// ── 8. EMPIRICAL VALIDATION ─────────────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('8. Three-Domain Empirical Validation (Expanded in v2.0)'),
  H2('8.1 System A: Sourdough Fermentation'),
  P('Budget ceiling: 1,000g. Five elements: flour (50.0%), water (35.0%), starter (13.0%), salt (1.8%), yeast (0.12%). Pettitt changepoint test applied to MDG time series across 12 baking cycles: p = 0.021. Yeast leverage 833 (ultra-high Q) confirms that the smallest element carries the highest governance significance. Near ground state: MDG = 1.4pp.'),
  H2('8.2 System B: Croatia Ramsar Wetlands'),
  P('Budget ceiling: 93,000 hectares. Five Ramsar sites: Lonjsko Polje (55.6%), Kopa\u010Dki rit (24.0%), Neretva Delta (12.0%), Crna Mlaka (0.67%), Vransko jezero (7.7%). Interrupted Time Series analysis: p < 0.0027. Crna Mlaka leverage 149 (high Q). Action window open: MDG = 4.8pp.'),
  P('The Croatia analysis provides the policy-relevant case. Crna Mlaka\u2014the smallest site by area\u2014has the highest leverage. Under absolute-metric governance (FM-1), it would be deprioritized as "small." Under ratio state monitoring, its high leverage flags it for governance attention. The coverage record (A-4) would require documented rationale for any reduction in its share.'),
  H2('8.3 System C: Software CI/CD Pipeline'),
  P('Budget ceiling: total query volume (30-day window). Four namespaces. Fisher exact test: p < 0.0001. Active drift: MDG = 10.0pp. This system operates at completely different temporal and structural scales from Systems A and B, confirming the domain-agnostic claim.'),
  H2('8.4 Toronto King Street Pilot (New in v2.0)'),
  P('The Toronto TTC King Street Transit Priority Pilot (November 2017) provides a causal validation. ITS analysis of ridership share detected a significant level change at the intervention point (5/5 confirmatory tests passing). The portfolio analysis detected a differential effect that absolute ridership counts obscured\u2014a direct demonstration of FM-1 (Ratio Blindness) in urban planning.'),
  H2('8.5 ESA Planck HFI (New in v2.0)'),
  P('Pettitt changepoint on the Planck HFI frequency portfolio MDG series returned OD 975 (p < 0.001). ESA\u2019s engineering records document He-4 cryogen exhaustion on January 14, 2012 = OD 975. The HUF analysis identified the exact day of a known physical event from portfolio share data alone. This external validation confirms that the ratio state captures genuine physical information.'),
  crossRef('Full Planck analysis: HUF_External_Validation_v1.0.docx'),
  crossRef('Full case studies: Vol 2'),
);

// ── 9. OSTROM MAPPING ───────────────────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('9. Ostrom Design Principles Mapping'),
  P('Elinor Ostrom\u2019s eight design principles for long-enduring commons governance [5] provide an independent benchmark for evaluating MC-4. The mapping below shows which HUF mechanisms satisfy each principle:'),
);
ch.push(makeT(
  ['DP', 'Ostrom Principle', 'HUF Mechanism', 'Artifact'],
  [
    ['1', 'Clearly defined boundaries', 'Budget ceiling; element enumeration', 'A-1'],
    ['2', 'Proportional allocation', 'Unity constraint; share computation', 'A-1, A-2'],
    ['3', 'Collective-choice arrangements', 'OCC 51/49; operator declaration', 'A-2'],
    ['4', 'Monitoring by accountable parties', 'Change log; drift classification', 'A-3'],
    ['5', 'Graduated sanctions', 'MDG thresholds; escalation pathway', 'A-3'],
    ['6', 'Conflict resolution mechanisms', 'Trace report; declared rationale', 'A-2, A-4'],
    ['7', 'Recognition of self-governance', 'Ground state convergence', 'All four'],
    ['8', 'Nested enterprises', 'CDN cross-domain normalization', 'A-1'],
  ],
  [500, 2600, 3200, 3060]
));
ch.push(
  P(''),
  P('HUF satisfies Design Principles 1 through 7 through its standard artifacts and governance mechanisms. Principle 8 (nested enterprises) is addressed through CDN, which enables comparison across governance levels and domains.'),
);

// ── 10. MC-4 IN EVERYDAY EXPERIENCE: CAR DASHBOARD ────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('10. MC-4 in Everyday Experience: The Car Dashboard (New in v2.1)'),
  P('The Fourth Monitoring Category can be understood through the analogy of a car\u2019s fuel system and its monitoring instruments. This section explains MC-4 by mapping it to the dashboard metrics drivers use every day.'),

  H2('10.1 Traditional Monitoring (MC-1, MC-2, MC-3) as Absolute Metrics'),
  P('Consider the fuel gauge and engine temperature gauge on a car dashboard. These are absolute metrics:'),
  P('MC-1 (Passive): The fuel gauge simply reads "you have 3 gallons." It observes the absolute level without a structured reference. A driver might see the needle move but cannot distinguish between a slow leak, a broken pump, or normal consumption.'),
  P('MC-2 (Mandated): A warning light triggers at a threshold\u2014e.g., "low fuel" when below 1 gallon. The car obeys an external standard (legal fuel reserve requirements) without explaining structural change.'),
  P('MC-3 (Question-driven): A question-driven system might ask "If I drive at 65 mph, will I reach the gas station at mile 52?" This tests a specific model without seeing broader patterns.'),
  P('All three focus on ', [{ text: 'absolutes', bold: true }, { text: ': fuel level, temperature, distance. They are essential. But they miss a critical structural shift.' }]),

  H2('10.2 The Ratio: Driver + Fuel'),
  P('Now introduce MC-4. Instead of asking "How much fuel?", ask "What is the ratio of driver to fuel in the system?"'),
  P('When you fill your tank: driver 51 gallons, fuel 49 gallons. Ratio = 1.04 (roughly 51/49). This is your system\u2019s declared weight\u2014the proportion between driver and fuel.'),
  P('As you drive:'),
  P([
    { text: 'Cycle 1: Driver 55 gallons, Fuel 45 gallons. Ratio = 1.22 (55/45). Fuel share dropped from 49% to 45%.', indent: 360 },
  ]),
  P([
    { text: 'Cycle 2: Driver 70 gallons, Fuel 30 gallons. Ratio = 2.33 (70/30). Fuel share dropped from 45% to 30%.', indent: 360 },
  ]),
  P([
    { text: 'Cycle 3: Driver 85 gallons, Fuel 15 gallons. Ratio = 5.67 (85/15). Fuel share is now 15%.', indent: 360 },
  ]),

  P('The fuel ', [{ text: 'absolute', bold: true }, { text: ' (MC-1) says: "You started with 49 gallons, now you have 15. You\u2019ve consumed 34 gallons." The gauge dutifully reports the level.' }]),
  P('MC-4 says something different: "Your driver/fuel ratio has ', [{ text: 'drifted 40% from nominal', bold: true }, { text: '. The system is moving toward failure. The composition has fundamentally changed."' }]),

  H2('10.3 MC-4 Detects Drift Before Absolutes Alarm'),
  P('Here is MC-4\u2019s critical advantage: ', [{ text: 'it detects problems before MC-1 sees them.', bold: true }]),
  P('Imagine a slow leak in your fuel tank. After one hour:'),
  P('- MC-1 fuel gauge: 48 gallons (down from 49). Still green. Unremarkable.'),
  P('- MC-4 ratio: Fuel share dropped from 49% to 48%. Driver/fuel ratio is now 1.08 instead of 1.04. Drift detected.'),
  P('After six hours:'),
  P('- MC-1 fuel gauge: 43 gallons. Still usable. Driver can ignore it.'),
  P('- MC-4 ratio: Fuel share is now 43/51 = 0.45. Driver/fuel ratio is 1.19. Compositional shift of 14% from baseline. Early warning: "The system is drifting."'),
  P('After 12 hours:'),
  P('- MC-1 fuel gauge: 37 gallons. "Low fuel" warning triggers.'),
  P('- MC-4 ratio: Fuel share = 37/51 = 0.42. Driver/fuel ratio = 1.38. Drift of 33%. MC-4 flagged the problem hours ago.'),

  P('MC-4\u2019s power is simple: ', [{ text: 'the ratio changes before the absolute collapses.', bold: true }, { text: ' A silent leak (silent drift in FM-2) is invisible in the absolute level until the warning light triggers. MC-4 sees it immediately.' }]),

  H2('10.4 The Deceptive Drift: OCC Budget Depletion'),
  P('MC-4 watches the driver/fuel ratio. As fuel depletes: 51/49 \u2192 55/45 \u2192 70/30 \u2192 85/15 \u2192 95/5.'),
  P('At each step, the operator\u2019s share of the system is ', [{ text: 'increasing.', bold: true }, { text: ' This looks like success\u2014"the operator is 95% of the system." But it is the opposite.' }]),
  P('The operator did not gain resources. The tool lost them. The rising operator share is the signature of OCC drift\u2014the tool\u2019s budget running out. The operator cannot control what the tool cannot provide. As the tool\u2019s allocation shrinks from 49% to 5%, the system approaches collapse.'),
  P('If the operator is not watching MC-4\u2019s ratio reports, the first indication of failure is the "abrupt inform"\u2014the engine stops, the car is on the side of the road. No gradual warning. MC-4\u2019s entire purpose is to prevent abrupt inform by making the drift trajectory visible ', [{ text: 'before the cliff.', bold: true }]),
  P('The ratio moving from 51/49 toward 100/0 is the signal. The absolute tool capacity is noise. In governance: when one stakeholder\u2019s share grows while others diminish, it is not a sign of that stakeholder\u2019s strength\u2014it is a sign of system collapse. The department whose budget share grows because other departments are being cut looks like it is thriving. The organization is dying. MC-4 makes the composition shift visible before the resource depletion becomes irreversible.'),

  H2('10.5 The Car Dashboard as MC-4 Instrument'),
  P('Modern cars have an onboard diagnostics computer (OBD). It tracks:'),
  P('- Fuel level (MC-1): absolute gauge reading.'),
  P('- Fuel consumption rate (MC-3): question-driven model\u2014"If I drive 50 miles, how much fuel remains?"'),
  P('- Efficiency ratio (MC-4): miles-per-gallon, or more directly, the ratio of distance to fuel burned.'),
  P('The OBD screen shows: "MPG: 24.3. Avg: 23.8. Trend: declining."'),
  P('That trend line is MC-4. It says: "Your distance-to-fuel ratio is shifting away from your baseline. Something is changing in the system\u2019s composition\u2014engine efficiency, driving pattern, or fuel quality. The ratio drift appeared before any absolute metric alarmed."'),

  H2('10.6 Mapping to Real Domains'),
  P('In the car analogy:'),
  P([
    { text: 'Driver/Fuel ratio = PV/SST ratio (in auditory cortex)', indent: 360 },
    { text: 'Driver/Fuel ratio = Lactobacillus/Saccharomyces ratio (in sourdough)', indent: 360 },
    { text: 'Driver/Fuel ratio = protection-site area / total protected area (in Ramsar wetlands)', indent: 360 },
    { text: 'Driver/Fuel ratio = operator weight / tool weight (in governance systems)', indent: 360 },
  ]),

  P('In each case:'),
  P('- Absolute metrics (MC-1, MC-2, MC-3) observe the individual elements. "The PV count is 30. The Lactobacillus population is 10^8. The wetland area is 93,000 ha."'),
  P('- MC-4 observes the ', [{ text: 'ratio between elements', bold: true }, { text: '. "The PV/SST ratio has shifted from 3.08 to 1.20. The Lactobacillus/Saccharomyces ratio is drifting. The protected-area / total-area share is declining."' }]),

  P('Ratios change before totals collapse. Composition shifts before absolutes alarm. This is the insight MC-4 brings to every finite-budget system.'),

  H2('10.7 Why Ratios Matter for Governance'),
  P('In a car, if your driver/fuel ratio drifts, you have an action window: you can diagnose the leak, repair it, or refuel before the system fails. If you wait for the absolute fuel level to trigger the warning light, your window may be gone.'),
  P('In governance systems, the same principle applies. A governance system declaring "operator: 51%, tool: 49%" (the OCC contract) must monitor that ratio. If silent drift moves it to "operator: 48%, tool: 52%", the system has drifted out of declared control before anyone noticed\u2014and before absolute metrics (budget, performance, participation) showed alarm.'),
  P('MC-4 creates an institutional memory of these ratio shifts: Cycle 1, Cycle 2, Cycle 3, etc. The trajectory becomes visible. Intentional reweighting (declared) is distinguished from silent drift (undeclared). What was invisible becomes traceable.'),

  H2('10.8 The Universality of the Ratio'),
  P('The car dashboard analogy demonstrates MC-4\u2019s domain-agnostic claim. Whether the system is:'),
  P([
    { text: 'A fuel tank (driver + fuel)', indent: 360 },
    { text: 'A neural circuit (PV + SST)', indent: 360 },
    { text: 'A biological culture (bacteria A + bacteria B)', indent: 360 },
    { text: 'A governance structure (operator + tool)', indent: 360 },
  ]),
  P('The structure is identical. Absolute metrics tell you what; ratios tell you how the system is ', [{ text: 'changing in composition', bold: true }, { text: '. MC-4 is universal precisely because it operates on this ratio structure, not on domain-specific knowledge.' }]),
);

// ── 11. DYNAMIC OCC DRIFT MONITORING AND PORTFOLIO GATING ─────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('11. Dynamic OCC Drift Monitoring and Portfolio Gating (New in v2.3)'),
  P('The OCC 51/49 contract declares the intended allocation between operator and tool. But this contract is not static. Real-time monitoring reveals that the actual ratio oscillates around the declared nominal, and these oscillations carry signal. This section presents the framework for Dynamic OCC Drift Monitoring\u2014the real-time observation of ratio oscillation\u2014and Dynamic Portfolio Gating\u2014the adaptive inclusion/exclusion of elements based on observability.'),

  H2('11.1 The OCC as Dynamic State'),
  P('The OCC 51/49 is the declared intent: operator weight w_op \u2265 0.51, tool weight w_tool \u2264 0.49. But the OCC is not a fixed contract enforced at every instant. Like all ratio states on the probability simplex, the OCC oscillates in real time around the nominal.'),
  P('Consider a governance system over 10 reporting cycles. The declared weights are: operator 51%, tool 49%. The observed weights across cycles might be:'),
  P([{ text: '   Cycle 1: 51%, 49% | Cycle 2: 52%, 48% | Cycle 3: 50%, 50% | Cycle 4: 53%, 47% | Cycle 5: 51%, 49%', indent: 360 }]),
  P([{ text: '   Cycle 6: 49%, 51% | Cycle 7: 48%, 52% | Cycle 8: 51%, 49% | Cycle 9: 50%, 50% | Cycle 10: 51%, 49%', indent: 360 }]),
  P('The mean observed ratio is 50.6% / 49.4%, which oscillates around the declared 51/49. The oscillation pattern\u2014bounded by 48% to 53% for the operator\u2014is the signal. The oscillations are not errors; they are the system\u2019s normal dynamic behavior.'),
  P('The critical observation is that oscillation is ', [{ text: 'bounded.', bold: true }, { text: ' When the tool is doing heavy work, the operator\u2019s share temporarily drops (cycles 6\u20137). When the operator makes a critical decision, their share temporarily rises (cycles 2, 4). But the ratio returns to the declared nominal. This is healthy oscillation.' }]),
  P('Unhealthy drift is ', [{ text: 'unbounded', bold: true }, { text: ' oscillation that does not return: operator share climbs from 51% to 65% to 75% and stays there. This is silent drift\u2014the tool is being depleted without declared reweighting. MC-4\u2019s drift monitor detects this by tracking whether the oscillation is bounded (healthy) or trending away from the nominal (drifting).' }]),

  H2('11.2 Dynamic Portfolio Gating'),
  P('Elements in a HUF portfolio vary in observability. Some produce continuous data streams. Others produce data only at specific events. Still others may be included in the declared portfolio but have insufficient data to compute a reliable share estimate.'),
  P('Dynamic portfolio gating applies a threshold. Elements above the observability threshold are included in the active portfolio. Elements below the threshold are gated out\u2014excluded from the ratio calculation but recorded in the governance trace. As data arrives, the gate re-evaluates.'),
  P('The rule: let G be the set of gated-in elements. The unity constraint applies to G: \u03A3_{i \u2208 G} \u03C1_i = 1. When an element crosses the observability threshold:'),
  P('- ', [{ text: 'Entering the gated set:', bold: true }, { text: ' Normalize all shares in G to sum to 1 again. The shares of previously gated elements rise slightly.' }]),
  P('- ', [{ text: 'Exiting the gated set:', bold: true }, { text: ' Remove the element from G, normalize the remaining shares, and record the reason for gating out in the coverage record (A-4).' }]),
  P('Example: A portfolio has five declared elements, but element 5 has produced no observable data for three cycles. It is gated out. The ratio is computed over the four gated-in elements. When data for element 5 arrives, it re-enters with a fresh share estimate. No data is lost; the gate adapts to maintain observability.'),

  H2('11.3 Scope Adjustment'),
  P('In classical signal processing, if a bandpass filter detects that important frequency content is falling outside the passband, the center frequency and bandwidth are adjusted. The scope of observation expands or contracts to match the domain.'),
  P('The same principle applies to HUF. If MC-4 detects that the portfolio is not summing to 1.0 within tolerance, or if multiple elements are gated out due to insufficient data, the scope is too wide. The solution is to adjust the center frequency (focal system) and bandwidth (included subsystems) until all elements within the scope have adequate observability.'),
  P('Practically, this means:'),
  P('- If a declared system is missing data, narrow the scope by excluding it from the ratio calculation until data becomes available.'),
  P('- If a system contains too many micro-elements with sparse data, aggregate them into fewer macro-elements.'),
  P('- If data suddenly becomes unavailable for critical elements, adjust the bandwidth immediately and document the change in the trace report (A-2).'),
  P('This is not loss of information. It is maintaining observability. A system observer should only claim to monitor what can be observed. False precision\u2014computing shares over gated-out elements with assumed zero values\u2014is worse than admitting that the scope is temporarily narrower.'),

  H2('11.4 MC-4 at Every Scale'),
  P('The OCC is specific to human governance systems, but the principle of Dynamic Drift Monitoring applies to every nested scale.'),
  P('', [{ text: 'Claude monitoring its own context window:', bold: true }, { text: ' The budget is 200,000 tokens. The operator allocation (user input) and tool allocation (Claude\u2019s reasoning, output generation) oscillate around a nominal. MC-4 watches: Is the token usage drifting toward 100% tool consumption, leaving no room for operator output? This is the internal analogue of OCC drift.' }]),
  P('', [{ text: 'A project manager watching team allocation:', bold: true }, { text: ' The budget is 40 person-hours per week. Five team members. The ratio of developer-hours to meeting-hours is the OCC analogue. If meetings consume 60% without explicit reallocation decisions, silent drift is occurring. MC-4 detects it.' }]),
  P('', [{ text: 'A biological cortex balancing PV and SST interneurons:', bold: true }, { text: ' The budget is total synaptic resources. The PV/SST ratio is the dynamic state. If PV grows from a nominal 40/60 to 70/30 without matching neural plasticity changes, it signals an imbalance. The same monitoring principle applies.' }]),
  P('In each case, the structure is: (1) declare the intended ratio, (2) monitor the actual ratio in real time, (3) distinguish intentional changes from silent drift, (4) maintain a trace record. This is MC-4, and it applies at every nested scale from token budgets to cortical circuits.'),

  crossRef('OCC detailed theory: Pillar 1, Section 9 (Car Analogy)'),
  crossRef('Scope matching: Pillar 1, Section 10 (Adaptive Scope)'),
  crossRef('Operational protocols: Vol 5, Sections 4\u20136'),
);

// ── 12. OPEN CONJECTURES ─────────────────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('12. Open Conjectures from the Collective Review (New in v2.0)'),
  P('The Five-AI Collective review (February 2026) produced 13 conjectures that extend the MC-4 framework. Each is labeled [CONJECTURE], indicating it has not been formally proved within the HUF framework. These are candidates for future proof or refutation.'),
);
ch.push(makeT(
  ['ID', 'Conjecture', 'Status'],
  [
    ['G.1', 'Boundary entropy is maximized at uniform distribution, minimized at full concentration', 'Open'],
    ['G.2', 'Lyapunov stability: declared-weight fixed point attracts under governance correction', 'Open'],
    ['G.3', 'MC-4 portfolios show lower variance in site scores than unmonitored portfolios', 'Testable'],
    ['G.4', 'Every finite collective-action resource with a budget ceiling is a valid HUF domain', 'Broad claim'],
    ['G.5', 'HUF artifacts satisfy Ostrom DP 1, 2, 4, and 7', 'Partially mapped'],
    ['G.6', 'Silent drift (FM-2) is the computational analogue of Ostrom monitoring failure', 'Strong argument'],
    ['G.7', 'Change log is a sufficient implementation of Ostrom DP 4', 'Plausible'],
    ['G.8', 'Ground state satisfies Ostrom self-governing commons conditions', 'Connects to convergence'],
    ['G.9', 'Sensitivity parameter s scales as ~1/Q', 'Operational link'],
    ['G.10', 'Per-cycle drift rate d scales as ~1 \u2212 1/Q', 'Drift dynamics'],
    ['G.11', 'Non-linear Lyapunov function exists for governance correction map', 'Hardest open problem'],
    ['G.12', 'HUF detects silent supplier concentration in procurement portfolios', 'Testable'],
    ['G.13', 'HUF detects silent model-capability concentration in AI portfolios', 'Proposed by Grok'],
  ],
  [500, 6200, 2660]
));

// ── 13. DISCUSSION ───────────────────────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('13. Discussion'),
  H2('13.1 What MC-4 Is Not'),
  P('MC-4 does not replace domain-specific assessment. It does not provide ecological, engineering, or financial expertise. It does not independently verify the accuracy of declared data. It does not compel corrective action. MC-4 is a governance diagnostic: it makes the gap between declared intent and observed allocation visible, attributable, and traceable across reporting cycles.'),
  H2('13.2 Limitations'),
  P('The framework assumes: (a) a well-defined budget ceiling exists, (b) element shares can be computed from available data, (c) declared weights are provided in good faith, and (d) the governance system has the capacity to respond to detected drift. When any of these assumptions fails, MC-4\u2019s diagnostic value degrades. In particular, fabricated declarations would produce an accurate record of a false history\u2014the institutional memory theorem records what was declared, not whether it was true.'),
  H2('13.3 Relationship to Companion Work'),
  P('This paper (Pillar 2) addresses HOW HUF observes. The companion paper (Pillar 1: The Sufficiency Frontier) addresses WHAT HUF extracts from data. The nine volumes of the HUF Triad address operational implementation, empirical evidence, mathematical foundations, and domain-specific applications. Together, the three structures form a complete framework.'),
  crossRef('Companion paper: Pillar 1, The Sufficiency Frontier'),
  crossRef('Triad overview: Vol 8, The Triad Synthesis'),
);

// ── 14. CONCLUSION ──────────────────────────────────────────────────
ch.push(
  H1('14. Conclusion'),
  P('Ratio State Monitoring (MC-4) is a structurally distinct monitoring category that detects silent drift in finite-budget systems by comparing observed allocation against declared intent. Its mathematical basis\u2014the degenerate state observer on the probability simplex\u2014requires no dynamic model, no external threshold, and no domain-specific calibration. Its practical output\u2014four standard artifacts attached to existing governance reporting\u2014provides an institutional memory that accumulates at one state per cycle, permanently.'),
  P('Three-domain confirmation across biological, ecological, and digital systems demonstrates domain-agnostic applicability. External validation on ESA Planck satellite data demonstrates that the ratio state carries genuine physical information. Thirteen open conjectures define the research frontier for formal extension.'),
  P('Dynamic OCC Drift Monitoring reveals that the OCC contract oscillates around the declared nominal, and these oscillations are the system\u2019s normal behavior. Silent drift is unbounded oscillation that does not return. Dynamic Portfolio Gating adapts the active portfolio in real time based on observability, maintaining the unity constraint and preventing false precision.'),
  P('MC-4 does not decide; it makes visible. The operator retains majority control (OCC 51/49). The governance record attributes every detection, every response, and every non-response to a named authority. What was invisible becomes traceable. What was silent becomes documented.'),
  P('The car dashboard analogy\u2014watching the driver/fuel ratio drift as the absolute level changes\u2014provides intuitive understanding of why monitoring composition matters as much as monitoring absolutes. In every domain, from fuel systems to biological circuits to governance structures, the ratio tells a story the absolute cannot. Dynamic drift monitoring and adaptive gating ensure that the observation boundary stays matched to the data actually present, at every scale.'),
  P(''),
  P([{ text: 'Nothing claims more than the artifacts support.', italics: true }]),
);

// ── REFERENCES ──────────────────────────────────────────────────────
ch.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('15. References'),
  P('[1] A. Spellerberg, "Monitoring ecological change," 2nd ed. Cambridge University Press, 2005.'),
  P('[2] D. Lindenmayer and G. Likens, "Effective ecological monitoring," CSIRO Publishing, 2010.'),
  P('[3] P. Higgins, "HUF Handbook v1.2.0," Rogue Wave Audio, 2026.'),
  P('[4] D. Luenberger, "Observing the state of a linear system," IEEE Trans. Mil. Electron., vol. 8, pp. 74\u201380, 1964.'),
  P('[5] E. Ostrom, "Governing the Commons," Cambridge University Press, 1990.'),
  P('[6] J. Aitchison, "The statistical analysis of compositional data," J.R. Stat. Soc. B, vol. 44, pp. 139\u2013177, 1982.'),
  P('[7] R.A. Fisher, "On the mathematical foundations of theoretical statistics," Phil. Trans. R. Soc. A, vol. 222, pp. 309\u2013368, 1922.'),
  P('[8] W.A. Shewhart, "Economic Control of Quality of Manufactured Product," Van Nostrand, 1931.'),
  P('[9] Planck Collaboration, "Planck 2013 results. I. Overview," Astron. Astrophys., vol. 571, A1, 2014.'),
  P('[10] A.N. Pettitt, "A non-parametric approach to the change-point problem," Appl. Stat., vol. 28, pp. 126\u2013135, 1979.'),
  P('[11] P. Higgins, "The Sufficiency Frontier," HUF Triad Pillar 1, v3.3, 2026.'),
  P('[12] P. Higgins, "The HUF Triad: Volume 8, Synthesis," v1.0, 2026.'),
  P('[13] R.E. Kalman, "A new approach to linear filtering and prediction problems," J. Basic Eng., vol. 82, pp. 35\u201345, 1960.'),
  P('[14] J.L. Fleiss et al., "Statistical Methods for Rates and Proportions," 3rd ed. Wiley, 2003.'),
  P('[15] T.M. Cover and J.A. Thomas, "Elements of Information Theory," 2nd ed. Wiley, 2006.'),
  P('[16] D.L. Donoho, "Compressed sensing," IEEE Trans. Inf. Theory, vol. 52, pp. 1289\u20131306, 2006.'),
  P('[17] L. Boltzmann, "Weitere Studien \u00FCber das W\u00E4rmegleichgewicht," Sitzungsber. Akad. Wiss. Wien, vol. 66, pp. 275\u2013370, 1872.'),
  P('[18] J. Aitchison and J.A.C. Brown, "The Lognormal Distribution," Cambridge University Press, 1957.'),
);

// ══════════════════════════════════════════════════════════════════════
// BUILD
// ══════════════════════════════════════════════════════════════════════
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
    ],
  },
  sections: [{
    properties: {
      page: { size: { width: PW, height: PH }, margin: { top: M, right: M, bottom: M, left: M } },
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MID, space: 1 } },
        children: [
          new TextRun({ text: 'HUF Triad \u2014 Pillar 2', font: 'Times New Roman', size: 18, color: MID }),
          new TextRun({ text: '\tThe Fourth Monitoring Category v2.3', font: 'Times New Roman', size: 18, italics: true, color: MID }),
        ],
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
      })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC', space: 1 } },
        children: [
          new TextRun({ text: 'HUF v1.2.0 \u00B7 MIT License \u00B7 ', font: 'Times New Roman', size: 16, color: '999999' }),
          new TextRun({ text: 'Page ', font: 'Times New Roman', size: 16, color: '999999' }),
          new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 16, color: '999999' }),
        ],
      })] }),
    },
    children: ch,
  }],
});

const OUT = __dirname.replace(/[/\\]pillars$/, '') + '/HUF_Fourth_Category_v2.3.docx';
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log(`\u2714 Generated: ${OUT} (${buf.length.toLocaleString()} bytes)`);
}).catch(err => { console.error('\u274c', err); process.exit(1); });
