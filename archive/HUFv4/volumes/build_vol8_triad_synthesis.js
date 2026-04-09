const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition,
        LevelFormat, ExternalHyperlink } = require('docx');

// ── Shared constants ────────────────────────────────────────────────
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;
const CW = PAGE_W - 2 * MARGIN;

const BLUE = '1F3864', MID = '2E75B6', DARK = '333333';
const LGREY = 'F2F2F2', LBLUE = 'D6E4F0', WHITE = 'FFFFFF';
const GREEN = 'E2EFDA', GOLD = 'FFF2CC';

const bdr = { style: BorderStyle.SINGLE, size: 1, color: 'BBBBBB' };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };

// ── Helpers ─────────────────────────────────────────────────────────
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 28, color: BLUE })] });

const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 24, color: BLUE })] });

const H3 = (t) => new Paragraph({ spacing: { before: 200, after: 120 },
  children: [new TextRun({ text: t, bold: true, italics: true, font: 'Times New Roman', size: 22, color: DARK })] });

function P(content, opts = {}) {
  const { align, indent, spacing_after, bold, italics, color: col } = opts;
  const runs = [];
  if (typeof content === 'string') {
    runs.push(new TextRun({ text: content, font: 'Times New Roman', size: 22, color: col || DARK,
      bold: bold || false, italics: italics || false }));
  } else if (Array.isArray(content)) {
    content.forEach(c => {
      if (typeof c === 'string') runs.push(new TextRun({ text: c, font: 'Times New Roman', size: 22, color: col || DARK }));
      else runs.push(new TextRun({ font: 'Times New Roman', size: 22, color: DARK, ...c }));
    });
  }
  return new Paragraph({ spacing: { after: spacing_after || 160 }, alignment: align || AlignmentType.JUSTIFIED,
    indent: indent ? { left: indent } : undefined, children: runs });
}

function crossRef(text) {
  return new Paragraph({ spacing: { before: 80, after: 160 },
    children: [new TextRun({ text: '\u25B6 ' + text, font: 'Times New Roman', size: 20, italics: true, color: MID })] });
}

function headerCell(text, width) {
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: BLUE, type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, font: 'Times New Roman', size: 20, bold: true, color: WHITE })] })] });
}

function dataCell(text, width, opts = {}) {
  const { shade, align, bold: b } = opts;
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    children: [new Paragraph({ alignment: align || AlignmentType.LEFT,
      children: [new TextRun({ text: String(text), font: 'Times New Roman', size: 20, color: DARK, bold: b || false })] })] });
}

function makeTable(headers, rows, colWidths) {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  return new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((h, i) => headerCell(h, colWidths[i])) }),
      ...rows.map((row, ri) => new TableRow({
        children: row.map((cell, ci) => dataCell(cell, colWidths[ci], { shade: ri % 2 === 0 ? LGREY : undefined }))
      })),
    ] });
}

// ══════════════════════════════════════════════════════════════════════
// CONTENT
// ══════════════════════════════════════════════════════════════════════

const children = [];

// ── TITLE PAGE ──────────────────────────────────────────────────────
children.push(
  new Paragraph({ spacing: { before: 3000 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: 'THE HUF TRIAD', font: 'Times New Roman', size: 44, bold: true, color: BLUE })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: 'Bridging Sufficient Statistics and Ratio State Monitoring', font: 'Times New Roman', size: 28, color: MID })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: 'through Governance', font: 'Times New Roman', size: 28, color: MID })] }),
  new Paragraph({ spacing: { before: 400 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'Volume 8 \u2014 The Triad Synthesis', font: 'Times New Roman', size: 24, italics: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'Version 1.0 \u00B7 March 2026', font: 'Times New Roman', size: 22, color: DARK })] }),
  new Paragraph({ spacing: { before: 600 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: 'Peter Higgins', font: 'Times New Roman', size: 22, bold: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: 'Principal Investigator, Rogue Wave Audio, Markham, Ontario', font: 'Times New Roman', size: 20, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: 'With the Five-AI Collective: Claude, Grok, GPT, Gemini, DeepSeek', font: 'Times New Roman', size: 20, italics: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'Higgins Unity Framework v1.2.0 \u00B7 MIT License', font: 'Times New Roman', size: 20, color: '999999' })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── ABSTRACT ────────────────────────────────────────────────────────
children.push(
  H1('Abstract'),
  P('The Higgins Unity Framework (HUF) rests on three mutually reinforcing structures. Pillar 1, The Sufficiency Frontier, establishes that domain-agnostic sufficient statistic extraction can reduce 156 million heterogeneous records to a 1,008-byte portfolio state at a ratio of 6,357,738:1, placing HUF in an analytically distinct category beyond conventional compression and signal processing. Pillar 2, The Fourth Monitoring Category, introduces Ratio State Monitoring (MC-4) as a structurally new approach to governance observation: a degenerate state observer where the output is the state, requiring no dynamic model, no external threshold, and no domain-specific calibration. This document, Volume 8, is the third structure: the bridge that binds the two pillars through a comprehensive governance framework spanning nine volumes, from interactive playground notebooks to formal mathematical proofs.'),
  P('The Triad architecture ensures that any reader\u2014regardless of entry point or expertise\u2014can navigate the complete framework through cross-referenced volumes, a unified glossary of 30 terms, and progressive learning pathways from grade-school intuition to post-doctoral research. The unity constraint (\u03A3\u03C1\u1D62 = 1) serves as the common foundation across all volumes, all domains, and all levels of analysis.'),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── 1. THE TRIAD ARGUMENT ───────────────────────────────────────────
children.push(
  H1('1. The Triad Argument'),
  P('A framework that only describes what it extracts (Pillar 1) lacks operational guidance. A framework that only describes how it observes (Pillar 2) lacks theoretical grounding. Neither pillar alone constitutes a complete system. The Triad recognizes that theory, observation, and practice form an irreducible triple:'),
  P([
    { text: 'Pillar 1 (The Sufficiency Frontier)', bold: true },
    ' answers: what does HUF extract from data, and why is the extraction sufficient? It establishes the information-theoretic position of the PreParser\u2014not compression, not filtering, but sufficient statistic extraction on the probability simplex.',
  ]),
  P([
    { text: 'Pillar 2 (The Fourth Monitoring Category)', bold: true },
    ' answers: how does HUF observe a system\u2019s governance state, and why is this observation structurally new? It establishes MC-4 as the first monitoring category that uses a system\u2019s own declared intent as its reference.',
  ]),
  P([
    { text: 'The Governance Bridge (Volumes 0\u20138)', bold: true },
    ' answers: how does a practitioner, researcher, or policy maker actually use HUF? It provides the progressive learning pathway, the operational handbook, the empirical evidence, and the cross-domain validation that connects theory to practice.',
  ]),
  P('Removing any one of these three structures leaves the remaining two incomplete. Without Pillar 1, the governance framework lacks a rigorous account of what information it operates on. Without Pillar 2, the framework lacks a rigorous account of why its observation method is valid. Without the Governance Bridge, both pillars remain academic papers disconnected from operational reality.'),
  crossRef('Pillar 1: The Sufficiency Frontier (companion paper)'),
  crossRef('Pillar 2: The Fourth Monitoring Category (companion paper)'),
);

// ── 2. THE NINE VOLUMES ─────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('2. The Nine Volumes'),
  P('The Triad is organized into nine volumes, numbered 0 through 8. Volume 0 begins with no prerequisites; Volume 8 synthesizes the complete framework. A reader can enter at any volume; cross-references guide navigation to prerequisite material when needed.'),
);

const volumeTable = makeTable(
  ['Volume', 'Title', 'Audience', 'Core Question'],
  [
    ['0', 'The Playground', 'Anyone (zero prerequisites)', 'What does HUF feel like?'],
    ['1', 'Core Reference', 'Undergraduate \u2192 practitioner', 'What is the unity constraint?'],
    ['2', 'Case Studies', 'Practitioner \u2192 researcher', 'Where has HUF been confirmed?'],
    ['3', 'Mathematical Foundations', 'Graduate \u2192 researcher', 'Why does it work (proofs)?'],
    ['4', 'Ecological Applications', 'Ecologist \u2192 manager', 'How does HUF apply to wetlands?'],
    ['5', 'Governance & Operations', 'Manager \u2192 policy maker', 'How do I run HUF?'],
    ['6', 'Universal Applicability', 'Cross-disciplinary researcher', 'Why does it work everywhere?'],
    ['7', 'Technical Implementation', 'Developer \u2192 data scientist', 'How do I build HUF?'],
    ['8', 'The Triad Synthesis', 'All levels', 'How does it all fit together?'],
  ],
  [600, 2200, 2800, 3760]
);
children.push(volumeTable);

children.push(
  P(''),
  P('Each volume is self-contained for its declared audience while cross-referencing other volumes for depth. The progressive learning pathway ensures that no concept is used before it has been introduced at the appropriate level.'),
);

// ── 3. PILLAR 1 SYNOPSIS ────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('3. Pillar 1: The Sufficiency Frontier'),
  H2('3.1 Central Claim'),
  P('The HUF PreParser performs domain-agnostic sufficient statistic extraction. It processes 156 million records from 10 heterogeneous systems\u2014spanning mechanical degradation (BackBlaze), national energy portfolios (OWID), urban transit (TTC), astrophysical instrumentation (ESA Planck), biological fermentation (sourdough), ecological monitoring (Ramsar), digital infrastructure (CI/CD), acoustic physics (RogueWaveAudio), and municipal infrastructure (Toronto)\u2014and produces a 1,008-byte output that preserves all information necessary for portfolio governance inference.'),
  H2('3.2 The Hierarchy of Information Reduction'),
  P('Pillar 1 introduces a four-level hierarchy that positions HUF relative to established reduction methods:'),
);

const hierarchyTable = makeTable(
  ['Level', 'Name', 'Ratio Range', 'Mechanism', 'Examples'],
  [
    ['1', 'Syntactic', '2:1 \u2013 10:1', 'Redundancy removal', 'ZIP, gzip, LZ77'],
    ['2', 'Perceptual', '10:1 \u2013 3,000:1', 'Irrelevance removal', 'JPEG, MP3, H.265'],
    ['3', 'Structural', '10\u00B2 \u2013 10\u2074:1', 'Model-based extraction', 'PCA, wavelet, Kalman'],
    ['4', 'Sufficient Statistic', '10\u2075 \u2013 10\u00B2\u00B3:1', 'Inference-preserving extraction', 'Boltzmann, Fisher, HUF PreParser'],
  ],
  [700, 1600, 1600, 2600, 2860]
);
children.push(hierarchyTable);

children.push(
  P(''),
  P('HUF operates at Level 4. The 6,357,738:1 ratio is not compression; it is the extraction of the sufficient statistics for portfolio governance from raw heterogeneous data. The sufficiency frontier is the boundary in reduction-ratio space where this transition occurs.'),
  crossRef('Full treatment: Pillar 1 paper, Sections 3\u20135'),
  crossRef('Interactive examples: Vol 0, Notebooks 1\u20135'),
  crossRef('Mathematical proofs: Vol 3, Sections 9\u201310'),
);

// ── 4. PILLAR 2 SYNOPSIS ────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('4. Pillar 2: The Fourth Monitoring Category'),
  H2('4.1 Central Claim'),
  P('Three monitoring categories are established in the ecological and governance literature: Passive (MC-1), Mandated (MC-2), and Question-driven (MC-3). HUF introduces a fourth: Ratio State Monitoring (MC-4), which uses a system\u2019s own declared intent as the reference for observation. MC-4 is structurally distinct from the first three in five ways: it is self-referential, non-invasive, model-free, bidirectional, and cross-cycle.'),
  H2('4.2 The Degenerate Observer'),
  P('MC-4\u2019s mathematical basis is the degenerate state observer. In classical control theory, a state observer estimates internal states from outputs using a dynamic model. HUF requires no model: the state IS the output. On the probability simplex, y(t) = \u03C1(t), the estimation gain L = 0, and the estimation error is identically zero. This is Proposition 1 of Pillar 2.'),
  H2('4.3 Six Failure Modes'),
  P('Pillar 2 identifies six structurally invisible failure modes that MC-1 through MC-3 cannot detect:'),
);

const fmTable = makeTable(
  ['ID', 'Name', 'Description'],
  [
    ['FM-1', 'Ratio Blindness', 'Managing a finite-budget system by absolute metrics'],
    ['FM-2', 'Silent Reweighting', 'Gradual allocation drift without governance decision'],
    ['FM-3', 'Snapshot Error', 'Underestimating high-Q elements by single-cycle observation'],
    ['FM-4', 'Concentration Trap', 'Increasing share to decreasing number of elements'],
    ['FM-5', 'Fragmentation Spiral', 'Sub-threshold attention to too many elements'],
    ['FM-6', 'Orphan Element', 'Element present on paper but outside governance'],
  ],
  [700, 2200, 6460]
);
children.push(fmTable);

children.push(
  P(''),
  P('FM-1 is the enabling condition; FM-2 is the mechanism; FM-3 through FM-6 are consequences. The progression is structural, not incidental.'),
  crossRef('Full treatment: Pillar 2 paper, Sections 4\u20136'),
  crossRef('Operational guide: Vol 5, Sections 1\u20134'),
  crossRef('Case study evidence: Vol 2'),
);

// ── 5. THE GOVERNANCE BRIDGE ────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('5. The Governance Bridge'),
  P('The Governance Bridge translates Pillar 1\u2019s information theory and Pillar 2\u2019s monitoring theory into operational practice. It comprises the four standard artifacts, the Operator Control Contract, the convergence pathway, and the institutional memory mechanism.'),
  H2('5.1 Four Artifacts'),
  P('HUF produces four standard outputs at each reporting cycle: A-1 (Portfolio Share Table), A-2 (Trace Report), A-3 (Portfolio Change Log), and A-4 (Coverage Record). These artifacts are plain tabular outputs in CSV format that attach to existing governance reporting structures. They require no new data collection\u2014only the re-expression of existing data as proportional shares.'),
  H2('5.2 Operator Control Contract (OCC 51/49)'),
  P('The OCC ensures that the operator always retains majority control over governance decisions. The formal requirement is w_op \u2265 0.51, w_tool \u2264 0.49: HUF advises, it does not decide. This is not a philosophical aspiration but a formal constraint embedded in every HUF deployment.'),
  H2('5.3 Convergence to Ground State'),
  P('Under consistent application, the Mean Drift Gap (MDG) approaches zero over successive reporting cycles. The convergence pathway proceeds through five observable stages: Baseline (Cycle 1), Trajectory Establishment (Cycles 2\u20133), Q-Factor Characterization (Cycles 4\u20136), Ground State Approach (Cycles 7+), and Ground State Reached (variable). The rate of convergence depends on the Q-factor differential between portfolio elements.'),
  H2('5.4 Institutional Memory'),
  P('Proposition 7.5 (proved in Volume 3): a governance system operating under MC-4 accumulates institutional memory at one portfolio state per reporting cycle, permanently and without additional effort. After n cycles, the institution holds an n-period governance trajectory independent of personnel turnover, organizational restructuring, or administrative disruption.'),
  crossRef('Operational handbook: Vol 5'),
  crossRef('Mathematical proof: Vol 3, Proposition 7.5'),
  crossRef('Interactive simulation: Vol 0, Notebook 3 (sourdough convergence)'),
);

// ── 6. PROGRESSIVE LEARNING PATHWAY ─────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('6. Progressive Learning Pathway'),
  P('The Triad is designed for multiple entry points. Five recommended reading pathways serve different audiences:'),
);

const pathwayTable = makeTable(
  ['Audience', 'Pathway', 'Learning Goal'],
  [
    ['Newcomer', 'Vol 0 \u2192 Vol 1 \u2192 Vol 2 \u2192 Vol 8', 'Intuition, foundations, evidence, synthesis'],
    ['Practitioner', 'Vol 0 \u2192 Vol 1 \u2192 Vol 5 \u2192 Vol 4 or Vol 2', 'Hands-on deployment skills'],
    ['Researcher', 'Vol 8 \u2192 Vol 3 \u2192 Vol 6 \u2192 Pillar 1 \u2192 Pillar 2', 'Theoretical depth and novelty claims'],
    ['Developer', 'Vol 0 \u2192 Vol 7 \u2192 Vol 1 \u2192 Vol 3', 'Implementation, then understanding'],
    ['Policy Maker', 'Vol 8 \u2192 Vol 5 \u2192 Vol 4 \u2192 Vol 2', 'Big picture, then governance, then evidence'],
  ],
  [1500, 4360, 3500]
);
children.push(pathwayTable);

children.push(
  P(''),
  P('Within each volume, concepts build from simple to complex. Volume 0\u2019s five Jupyter notebooks progress from pizza slices to satellite telemetry. Volume 3 progresses from compositional data theory to open conjectures. No concept is introduced at a level higher than the audience can reach from the previous step.'),
);

// ── 7. CROSS-REFERENCE MATRIX ───────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('7. Cross-Reference Matrix'),
  P('Every core concept appears in multiple volumes at different depths. The codes below indicate treatment level: I = Introduced, D = Defined formally, P = Proved, A = Applied, E = Exemplified.'),
);

const xrefTable = makeTable(
  ['Concept', 'V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'],
  [
    ['Unity Constraint',    'I', 'D', 'A', 'P', 'A', 'A', 'D', 'A', 'D'],
    ['Mean Drift Gap',      'I', 'D', 'E', 'P', 'E', 'A', 'A', 'A', 'D'],
    ['Degenerate Observer',  '',  '',  '',  'P',  '',  'I', 'D',  '',  'D'],
    ['Four Artifacts',       '',  'D', 'E',  '',  'A', 'D',  '',  'A', 'D'],
    ['Six Failure Modes',    '',  'I', 'E',  '',  'A', 'D', 'A',  '',  'D'],
    ['Quality Factor (Q)',   '',  'I', 'E', 'P', 'A', 'A', 'A',  '',  'D'],
    ['OCC 51/49',            '',  'D',  '',   '',  'A', 'D',  '',  'A', 'D'],
    ['MC-1 through MC-4',    '',  'I', 'A',  '',  'A', 'D', 'D',  '',  'D'],
    ['Sufficiency Frontier',  '',  '',  '',  'P',  '',   '',  'D',  '',  'D'],
    ['Ground State',         'I', 'D', 'E', 'P', 'A', 'D', 'A',  '',  'D'],
    ['Institutional Memory',  '',  'I',  '',  'P', 'A', 'D', 'A',  '',  'D'],
    ['PROOF Line',           'I', 'D', 'E',  '',  'A', 'A',  '',  'A', 'D'],
    ['Leverage',             'I', 'D', 'E',  '',  'A', 'A',  '',  'A', 'D'],
    ['CDN',                   '',  'I', 'A', 'P',  '',   '',  'D', 'A', 'D'],
    ['Ostrom Principles',     '',   '',   '',   '',  'D', 'D', 'A',  '',  'D'],
  ],
  [1800, 500, 500, 500, 500, 500, 500, 500, 500, 560]
);
children.push(xrefTable);

// ── 8. UNIFIED GLOSSARY ─────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('8. Unified Glossary'),
  P('The following terms are used consistently across all nine volumes, both pillar papers, and all companion notebooks. Definitions are canonical; any document that uses a term differently has a gap to be resolved.'),
);

const glossaryTerms = [
  ['Budget Ceiling (M)', 'The total of a finite-budget system, indexed to 1.0.'],
  ['Element (i)', 'Any constituent of a portfolio holding a share of the ceiling.'],
  ['Share (\u03C1\u1D62)', 'An element\u2019s proportion of the budget ceiling. \u03C1\u1D62 = m\u1D62/M.'],
  ['Ratio State (\u03C1)', 'Complete system description: vector of shares summing to 1.'],
  ['Unity Constraint', '\u03A3\u03C1\u1D62 = 1. Foundational invariant. Tautological for proportions.'],
  ['Probability Simplex (S\u1D37)', 'Geometric space of all valid portfolio states.'],
  ['Declared Weight', 'The share an operator states each element should hold.'],
  ['Observed Share', 'The share an element actually holds in the current state.'],
  ['Drift Gap', '|\u03C1\u1D62\u1D48\u1D49\u1D9C \u2212 \u03C1\u1D62\u1D52\u1D47\u02E2|. Absolute difference per element.'],
  ['Mean Drift Gap (MDG)', 'Average drift gap across all elements. In percentage points.'],
  ['Silent Drift', 'Change not traceable to a recorded governance decision.'],
  ['Intentional Reweighting', 'Change traceable to a recorded governance decision.'],
  ['Leverage (1/\u03C1\u1D62)', 'Reciprocal of share. Measures sensitivity to removal.'],
  ['PROOF Line', 'Min elements for 80% of portfolio mass. Lower = more concentrated.'],
  ['Quality Factor (Q)', 'T_char/T_obs. Characteristic period to observation bandwidth.'],
  ['Ground State', 'MDG \u2192 0. All change declared. Self-correcting feedback.'],
  ['Action Window', 'Period when correction is cheapest.'],
  ['Failure Modes (FM-1\u2013FM-6)', 'Six structurally invisible governance failures.'],
  ['Aitchison Distance', 'Natural metric on the simplex. MDG is first-order approximation.'],
  ['CDN (\u03A9)', '|\u0394MDG| \u00D7 (K/K_eff). Cross-domain normalization.'],
  ['OCC 51/49', 'w_op \u2265 0.51. Operator retains majority control.'],
  ['Degenerate Observer', 'y(t) = \u03C1(t). State IS output. L = 0. No model needed.'],
  ['MC-4 (Ratio State Monitoring)', 'Fourth monitoring category. Self-referential, model-free.'],
  ['Institutional Memory', 'One portfolio state per cycle, permanently accumulated.'],
  ['Sufficiency Frontier', 'Boundary where reduction becomes sufficient statistic extraction.'],
  ['Four Artifacts (A-1\u2013A-4)', 'Share Table, Trace Report, Change Log, Coverage Record.'],
  ['Convergence Stages', 'Baseline \u2192 Trajectory \u2192 Q-characterization \u2192 Ground State.'],
  ['Ostrom Design Principles', 'Eight commons governance principles. HUF satisfies DP1\u20137.'],
  ['Pettitt Test', 'Non-parametric changepoint detection on MDG time series.'],
  ['ITS', 'Interrupted Time Series. Y = \u03B2\u2080 + \u03B2\u2081t + \u03B2\u2082D + \u03B2\u2083(t\u00D7D) + \u03B5.'],
];

const glossaryTable = makeTable(
  ['Term', 'Definition'],
  glossaryTerms,
  [2800, 6560]
);
children.push(glossaryTable);

// ── 9. EMPIRICAL FOUNDATION ─────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('9. Empirical Foundation'),
  P('The Triad rests on empirical confirmation across 10 domains. Three domains provide formal statistical confirmation (System A, B, C); seven additional domains provide supportive evidence through the PreParser corpus.'),
);

const empiricalTable = makeTable(
  ['System', 'Domain', 'Records', 'Key Result', 'Status'],
  [
    ['A', 'Sourdough fermentation', '~500', 'p=0.021 (Pettitt)', 'Confirmed'],
    ['B', 'Croatia Ramsar wetlands', '~2,000', 'p<0.0027 (ITS)', 'Confirmed'],
    ['C', 'Software CI/CD pipeline', '~10,000', 'p<0.0001 (Fisher)', 'Confirmed'],
    ['D', 'BackBlaze hard drives', '~1M', '9-quarter HDI portfolio', 'Supportive'],
    ['E', 'OWID energy mix', '~50,000', '3-country structural breaks', 'Supportive'],
    ['F', 'Toronto TTC transit', '~2.4M', 'King St 5/5 causal', 'Supportive'],
    ['G', 'ESA Planck HFI', '~5.7B', 'OD 975 exact match', 'Validated'],
    ['H', 'Toronto infrastructure', '~127M', 'Budget portfolio analysis', 'Supportive'],
    ['I', 'RogueWaveAudio', '~1.5M', 'Frequency portfolio', 'Supportive'],
    ['J', 'Published (Nature Sci Rep)', '\u2014', 'Peer-reviewed validation', 'Published'],
  ],
  [700, 2200, 1200, 2800, 2460]
);
children.push(empiricalTable);

children.push(
  P(''),
  P('The three-domain confirmation (Systems A, B, C) provides the formal statistical basis. The ESA Planck external validation (System G) provides the strongest single piece of evidence: a changepoint detected from data alone that matches a known physical event to the exact operational day.'),
  crossRef('Full evidence: Vol 2 (Case Studies)'),
  crossRef('PreParser corpus: Pillar 1, Section 5'),
);

// ── 10. OPEN PROBLEMS AND FUTURE WORK ───────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('10. Open Problems and Future Work'),
  H2('10.1 Mathematical'),
  P('The non-linear convergence proof remains open. Grok assessed this as requiring advanced mathematical tools beyond the current framework. A three-step traceable path has been defined: (1) empirical non-linear datasets from Phase D, (2) symbolic simulation of the governance correction map, (3) construction of a Lyapunov function for global asymptotic stability. Thirteen conjectures from the collective review (Layer 13 of the taxonomy) await formal proof or refutation.'),
  H2('10.2 Empirical'),
  P('Phase D of the Croatia Ramsar pilot has not yet begun. This requires the first institutional contact with Croatian conservation authorities. The pilot would provide the first real-world institutional deployment data, moving beyond retrospective analysis to prospective governance monitoring. Three reporting cycles minimum are needed for convergence trajectory analysis.'),
  H2('10.3 Domain Extension'),
  P('Four application domains have been sketched but not empirically tested: supply chain (System D), logistics (System E), manufacturing (System F), and AI governance (System G). Each has a conjectural threshold configuration documented in the taxonomy. Real-data validation requires domain partnerships.'),
  H2('10.4 Technical'),
  P('The HUF PreParser exists as a set of JavaScript builders and Python implementations. A formal API specification, automated testing framework, and deployment pipeline are needed for production use. Volume 7 addresses this gap.'),
);

// ── 11. THE FIVE-AI COLLECTIVE ──────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('11. The Five-AI Collective'),
  P('The HUF framework was developed through a distinctive collaboration between a human principal investigator and five AI systems, each contributing according to its strengths:'),
  P([{ text: 'Claude', bold: true }, ' (Anthropic): Primary research partner. Document architecture, mathematical formalization, code generation, cross-referencing. Builder of the document corpus and the Triad structure.']),
  P([{ text: 'Grok', bold: true }, ' (xAI): Mathematical extensions. Thirteen conjectures, Lyapunov stability analysis, Q-factor derivation, Ostrom mapping, four domain application paths. Go/No-Go verdicts on framework claims.']),
  P([{ text: 'GPT', bold: true }, ' (OpenAI): Literature review, citation verification, academic writing standards. External perspective on framework positioning.']),
  P([{ text: 'Gemini', bold: true }, ' (Google): Data processing pathways, geospatial analysis (Toronto infrastructure), cross-domain comparison methodology.']),
  P([{ text: 'DeepSeek', bold: true }, ' (DeepSeek): Mathematical verification, alternative proof strategies, edge case analysis.']),
  P('The Operator Control Contract (OCC 51/49) governs this collaboration: the human principal investigator retains majority decision authority over all framework claims, publication decisions, and governance design. The AI systems advise; they do not decide. This contract applies reflexively: HUF monitors its own development process as a portfolio of contributions.'),
);

// ── 12. CONCLUSION ──────────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('12. Conclusion'),
  P('The HUF Triad presents a complete framework for portfolio governance that is theoretically grounded (Pillar 1: sufficient statistics), observationally valid (Pillar 2: degenerate state observer), and operationally actionable (Volumes 0\u20138: progressive governance implementation). The unity constraint \u03A3\u03C1\u1D62 = 1 is the single invariant from which all structures derive. Because this constraint holds for any system where shares are defined as proportions of a fixed total, HUF\u2019s applicability is bounded only by the existence of a budget ceiling\u2014a condition satisfied across mechanical, biological, ecological, digital, astrophysical, acoustic, and institutional domains.'),
  P('The Triad is not a claim of completeness. Open problems remain in non-linear convergence theory, prospective institutional deployment, and domain extension. What the Triad does claim is structural coherence: the two pillar papers and nine governance volumes form a mutually reinforcing architecture where each component strengthens every other component through shared definitions, shared data, and shared mathematical foundations.'),
  P('Any reader can enter at any point. The cross-references will guide them to wherever they need to go next.'),
  P(''),
  P([
    { text: 'Nothing claims more than the artifacts support.', italics: true },
  ]),
  P(''),
  P([
    { text: 'Peter Higgins', bold: true },
    ' \u00B7 Principal Investigator \u00B7 Rogue Wave Audio \u00B7 Markham, Ontario',
  ]),
  P([
    { text: 'HUF v1.2.0 \u00B7 MIT License \u00B7 March 2026', italics: true, color: '999999' },
  ]),
  P([
    { text: 'Collective contributions: Claude, Copilot, Gemini, ChatGPT, Grok, DeepSeek', italics: true, color: '999999' },
  ]),
);

// ══════════════════════════════════════════════════════════════════════
// BUILD DOCUMENT
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
      page: {
        size: { width: PAGE_W, height: PAGE_H },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MID, space: 1 } },
          spacing: { after: 0 },
          children: [
            new TextRun({ text: 'HUF Triad \u2014 Volume 8', font: 'Times New Roman', size: 18, color: MID }),
            new TextRun({ text: '\tThe Triad Synthesis', font: 'Times New Roman', size: 18, italics: true, color: MID }),
          ],
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC', space: 1 } },
          children: [
            new TextRun({ text: 'Higgins Unity Framework v1.2.0 \u00B7 MIT License \u00B7 ', font: 'Times New Roman', size: 16, color: '999999' }),
            new TextRun({ text: 'Page ', font: 'Times New Roman', size: 16, color: '999999' }),
            new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 16, color: '999999' }),
          ],
        })],
      }),
    },
    children,
  }],
});

const OUT = __dirname.replace(/[/\\]volumes$/, '') + '/HUF_Triad_Synthesis_v1.0.docx';
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log(`\u2714 Generated: ${OUT} (${buf.length.toLocaleString()} bytes)`);
}).catch(err => { console.error('\u274c', err); process.exit(1); });
