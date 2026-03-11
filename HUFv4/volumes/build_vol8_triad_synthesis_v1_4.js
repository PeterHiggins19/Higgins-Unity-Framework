// ══════════════════════════════════════════════════════════════════════
// HUF Triad Phase 1 — Volume 8: Synthesis v1.4 + HUF-Org
// Peter Higgins · March 2026
// ══════════════════════════════════════════════════════════════════════

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
    children: [new TextRun({ text: 'Version 1.1 \u00B7 March 2026', font: 'Times New Roman', size: 22, color: DARK })] }),
  new Paragraph({ spacing: { before: 600 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: 'Peter Higgins', font: 'Times New Roman', size: 22, bold: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: 'Principal Investigator, Rogue Wave Audio, Markham, Ontario', font: 'Times New Roman', size: 20, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: 'With the Five-AI Collective: Claude, Grok, GPT, Gemini, DeepSeek', font: 'Times New Roman', size: 20, italics: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'Higgins Unity Framework v1.3.0 \u00B7 MIT License', font: 'Times New Roman', size: 20, color: '999999' })] }),
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

// ══════════════════════════════════════════════════════════════════════
// NEW SECTION A: THE TRIAD OF TRIADS (v1.1 addition)
// ══════════════════════════════════════════════════════════════════════

children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('10. The Triad of Triads: 9 Points of Contact, 3 Unions'),
  P('The Triad framework rests on a deeper architectural principle: HUF itself is not a single structure but a two-triad system that connects through three unions to form a stable architecture. Understanding this geometry clarifies how the nine volumes, two pillar papers, and operational practice form a coherent whole.'),
  H2('10.1 The Three Triads'),
  P([
    { text: 'Triad 1 \u2014 HUF (Mathematics):', bold: true },
    ' The theoretical foundation consists of three pillars:',
  ]),
  P('  \u2022  Sufficiency Frontier: Domain-agnostic extraction at the boundary between compression and inference.', { spacing_after: 80 }),
  P('  \u2022  Fourth Category: MC-4 as the first monitoring method that uses a system\u2019s declared intent as reference.', { spacing_after: 80 }),
  P('  \u2022  H1 Operator: The specific transformation that generates the sufficient statistics on the probability simplex.', { spacing_after: 160 }),
  P([
    { text: 'Triad 2 \u2014 RWA (Application):', bold: true },
    ' The practical bridge from mathematics to implementation:',
  ]),
  P('  \u2022  Organic Digital: Application without artificial constraints; HUF fits into existing governance structures.', { spacing_after: 80 }),
  P('  \u2022  DADC-DADI: Data-agnostic, domain-agnostic collection and interpretation methods.', { spacing_after: 80 }),
  P('  \u2022  Cortex-Matched Crossover: Matching human cognitive load and decision-making capacity.', { spacing_after: 160 }),
  P([
    { text: 'Triad 3 \u2014 Real World (Validation):', bold: true },
    ' The operational proof that the framework works in practice:',
  ]),
  P('  \u2022  Binaural Test Lab (BTL): Open-source construction path anyone can follow; no proprietary dependency.', { spacing_after: 80 }),
  P('  \u2022  Measurement and Calibration: Quantitative evidence from ten heterogeneous systems confirming the claims.', { spacing_after: 80 }),
  P('  \u2022  Listener Experience: Human feedback, institutional deployment, and emergent governance discovery.', { spacing_after: 160 }),
  H2('10.2 The Three Unions: 9 Points of Contact'),
  P('These triads do not float independently. They connect at three unions, each connection point carrying structural significance:'),
  P([
    { text: 'Union 1: HUF \u2194 RWA (Mathematics Meets Acoustics)', bold: true },
  ]),
  P('The H1 operator originated as a solution to loudspeaker diffraction problems at the frequency boundary between ear-canal-scale and head-scale acoustics. The mathematics was born from a physics problem. This union establishes that HUF is not abstract theory imposed on data; it is a principle extracted from observed physical systems. The connection point is the frequency portfolio of a passive loudspeaker crossover: a real, measurable system where the unity constraint (\u03A3\u03C1\u1D62 = 1) applies directly to acoustic energy distribution.'),
  P(''),
  P([
    { text: 'Union 2: RWA \u2194 Real World (Theory Meets Practice)', bold: true },
  ]),
  P('The RWA Science (Rogue Wave Audio applied science) repository translates HUF into deployment guides, governance templates, and open-source tooling. This union bridges the gap between mathematical principle and institutional action. The Binaural Test Lab allows any practitioner to construct a functioning HUF deployment without relying on proprietary software. The connection point is the four standard artifacts (A-1 through A-4): CSV outputs that attach seamlessly to existing reporting infrastructure.'),
  P(''),
  P([
    { text: 'Union 3: Real World \u2194 HUF (Validation Closes the Loop)', bold: true },
  ]),
  P('Measurement data from real systems feeds back to validate the mathematical framework. Systems A, B, and C provide statistical confirmation. System G (ESA Planck) provides external validation with the strongest evidence: a changepoint detected from the mathematics alone matched a known physical event to the exact operational day. This union closes the loop: practice generates data, data confirms theory, theory guides next practice. The connection point is the Mean Drift Gap (MDG): a single metric that appears in mathematics (convergence theorems), in governance (operational observation), and in measurement (empirical validation).'),
  P(''),
  H2('10.3 The Stable Center'),
  P('The stable point is the center where all three unions converge. This center is the probability simplex itself: the geometric space where all valid portfolio states exist, bounded by the unity constraint. At this center, the following are one and the same:'),
  P('  \u2022  The sufficient statistic extracted from raw data (mathematics).', { spacing_after: 80 }),
  P('  \u2022  The ratio state observed by MC-4 (governance).', { spacing_after: 80 }),
  P('  \u2022  The portfolio composition reported in A-1 (practice).', { spacing_after: 160 }),
  P('This identity\u2014that theory, observation, and practice converge to the same object\u2014is what makes the Triad stable. No translation layer, no conversion function, no model mismatch. y(t) = \u03C1(t). The state IS the output.'),
  P(''),
  H2('10.4 Repository Mapping'),
  P('The three triads map cleanly to three repositories that together form the operational implementation:'),
  P([
    { text: 'HUF Repository (Mathematics):', bold: true },
    ' Pillar 1 and Pillar 2 papers, mathematical proofs, formal definitions, and the nine volumes (0\u20138). This is Triad 1.',
  ]),
  P(''),
  P([
    { text: 'RWA Science Repository (Theory):', bold: true },
    ' Applied documentation, case studies, cross-domain analysis, and the bridge between mathematical principle and operational deployment. This is Triad 2.',
  ]),
  P(''),
  P([
    { text: 'RWA Build Repository (Practice):', bold: true },
    ' Open-source implementation, Binaural Test Lab construction guides, deployment templates, and the four standard artifacts. This is Triad 3.',
  ]),
  P(''),
  P('A reader or practitioner can begin in any repository and navigate to the others through the three unions. The mathematician enters through HUF and reaches practice via Unions 1 and 2. The practitioner enters through RWA Build and reaches theory via Unions 2 and 3. The researcher enters through RWA Science and reaches mathematics and practice via Unions 1 and 3. Every path is valid and complete.'),
);

// ══════════════════════════════════════════════════════════════════════
// NEW SECTION B: THE CAR ANALOGY (v1.1 addition)
// ══════════════════════════════════════════════════════════════════════

children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('11. The Car Analogy: HUF for Everyone'),
  P('Version 1.0 of this framework contained extensive tables, mathematical notation, and cross-references. It was technically complete. But a single moment in conversation revealed what was missing: when someone said, \"I see,\" it was not after reading a table or equation. It was after hearing an analogy.'),
  P('The following analogy has become the universal teaching tool for HUF. It requires no mathematical background, no prior knowledge of governance, and no technical preparation. A fifth-grader understands it. A Fortune 500 CFO sees herself in it. A software engineer recognizes the state machine. It is a Rosetta Stone for the unity constraint.'),
  H2('11.1 The Basic Scenario'),
  P('You own a car. The fuel tank holds 4 gallons. Today you fill it completely: 4 gallons. The tank is at 100% capacity, the unity constraint is satisfied (4 = 4, ratio = 1.0).'),
  P('You drive for 30 minutes. You burn 2 gallons of fuel. The tank now holds 2 gallons in a 4-gallon tank. The ratio is now 2/4 = 0.5.'),
  P('Tomorrow you arrive at a new city. You rent a different car. This car has a 40-gallon tank. You fill it: 40 gallons. You drive for 30 minutes. You burn 2 gallons of fuel. This tank now holds 38 gallons in a 40-gallon tank. The ratio is 38/40 = 0.95.'),
  P('The insight: 2 gallons of fuel is the same amount in both cases. But 2 gallons in a 4-gallon tank (50% burned) is radically different from 2 gallons in a 40-gallon tank (5% burned). The same fuel represents different system states because the systems have different total budgets (ceiling). You cannot understand the fuel burn by looking at absolute quantities. You must look at ratios.'),
  P(''),
  H2('11.2 The Driver/Fuel Portfolio'),
  P('Now extend the analogy. Your car has a fuel tank and a driver. The total system budget is 1.0 (unity constraint). The driver is 51% of the system. The fuel is 49% of the system. This is the Operator Control Contract (OCC 51/49).'),
  P('The driver makes decisions: where to go, how fast to drive, which route to take. These decisions are 51% of the system because the driver controls 51% of the resources (decision-making authority).'),
  P('The fuel carries out those decisions: it provides the energy to actually move the car. Fuel is 49% of the system because it executes, not decides.'),
  P('If the driver attempts to make all decisions while fuel is depleted, the system fails. The driver cannot decide to drive to another city when the fuel tank is empty. Both components must operate at their declared ratio: the driver at 51% and the fuel at 49%.'),
  P(''),
  H2('11.3 The Fuel Gauge and MC-4'),
  P('The fuel gauge is a measurement device. It reads the current ratio: \u03C1(t) = fuel_gallons / tank_capacity. It tells you what the system state actually is right now.'),
  P('In classical monitoring (MC-1, MC-2, MC-3), the gauge would measure absolute quantity: \"You have 2 gallons.\" That fact is only meaningful if you know the tank size. The gauge would require a model: \"In a 4-gallon tank, 2 gallons is critical; in a 40-gallon tank, 2 gallons is normal.\" You need external knowledge to interpret the gauge.'),
  P('MC-4 is different. The fuel gauge directly reports the ratio. You set the gauge to match the declared budget (unity constraint). If you declared \"50% fuel, 50% driver,\" the gauge watches whether that ratio holds. If the gauge drifts from 50% to 45%, that drift is directly observable without any model, without any domain knowledge, without calibration. The gauge IS the state observer.'),
  P(''),
  H2('11.4 Direction Preserved While Fuel Burns'),
  P('The car is heading north. As fuel burns, the car continues heading north. The direction is determined by the driver (steering control). The fuel does not change the direction; it only enables motion.'),
  P('This is the H1 directional coherence. The ratio between driver and fuel can change (due to governance decisions or drift), but the system\u2019s direction\u2014its declared intent\u2014remains constant. The sufficient statistics extracted by HUF preserve direction even as fuel depletes. The portfolio composition changes, but the governance principle does not.'),
  P(''),
  H2('11.5 Empty Tank and the Sufficiency Frontier'),
  P('The fuel gauge reads 0%. The tank is empty. You have reached the ground state: all fuel is consumed, zero decision-making authority remains. The driver can make no further decisions.'),
  P('This is the sufficiency frontier breach. A system that operates at 51% driver and 49% fuel can continue indefinitely as long as both components are available. But when fuel reaches 0%, the system collapses. At this boundary, the framework breaks down. You cannot extract sufficient statistics from an empty tank. You cannot observe governance state from a non-existent resource.'),
  P('The sufficiency frontier is the operational boundary of the framework: as long as 0 < \u03C1\u1D62 < 1 for all elements, HUF functions. At \u03C1\u1D62 = 0, the framework loses validity.'),
  P(''),
  H3('11.5.1 The Deceptive Drift: Why Rising Share Is the Death Signal'),
  P('The car analogy reveals a danger that is not apparent from the fuel gauge alone. As fuel depletes, the driver\u2019s share of the total system budget rises. At the start: driver 51%, fuel 49%. After some driving: driver 60%, fuel 40%. Further: driver 75%, fuel 25%. Near empty: driver 95%, fuel 5%.'),
  P('Each step looks like the driver is gaining control. The driver\u2019s share of the system is increasing. In a governance context, a department whose budget share grows while others shrink appears to be thriving. The manager feels empowered. The rising ratio looks like success.'),
  P('It is the death signal. The rising operator share IS the depletion signal, not the victory signal. A system at 95/5 has only 5% remaining before ground state. The operator feels empowered by the rising ratio. But the system is dying. This is OCC drift: the Operator Crossover Contribution is rising not because the operator is more capable, but because the tool\u2019s budget ran out.'),
  P('If the operator is not watching the fuel gauge (MC-4), the system will not gently inform. It will abruptly inform. When fuel hits zero, the driver/fuel ratio becomes undefined. The Sufficiency Frontier is not a slope; it is a cliff. The system stops supporting because its budget ran out. Tool intact, operator capable, but the OCC budget exhausted.'),
  P('In governance, a department whose budget share grows as others are cut looks like it is thriving. But the organization is dying. The rising share is not victory; it is a death signal. Only watching the fuel gauge (total institutional health, not departmental autonomy) reveals the truth.'),
  P(''),
  H2('11.6 The Non-Intuitive Truth: Tank Size Matters'),
  P('Return to the core insight. You have 2 gallons of fuel. Is that a crisis or a comfortable margin?'),
  P('In a 4-gallon tank: 2 gallons = 50%. This is a moderate state; half the fuel is remaining.'),
  P('In a 40-gallon tank: 2 gallons = 5%. This is normal; 95% of fuel remains.'),
  P('The ratio, not the absolute quantity, determines the system state. Two governance systems with identical fuel quantities can be in completely different governance states because they have different budget ceilings.'),
  P('This non-intuitive principle is the core of FM-1 (Ratio Blindness). Managers often make governance decisions based on absolute metrics (\"We spent $2 million\") without tracking ratios (\"That $2 million is 50% of our annual budget\"). The fuel gauge shows both systems have 2 gallons. Ratio monitoring reveals they are in completely different states.'),
  P(''),
  H2('11.7 MC-4 Watching Compositional Drift'),
  P('You drive your 4-gallon car and after 30 minutes the fuel gauge reads 50% (2 gallons remain). You declared 49% fuel, 51% driver. The system is performing according to intent: half the fuel is burned, the driver is still making decisions.'),
  P('But now Silent Drift occurs. No decision was made, yet the fuel ratio changes. The gauge drifts to 45% (1.8 gallons in a 4-gallon tank). No burn happened; the tank must have contracted or the gauge is drifting. This is compositional drift without governance decision.'),
  P('MC-4 catches this immediately because the gauge is watching the ratio directly. Conventional monitoring (absolute metrics) would miss this entirely: 1.8 gallons in absolute terms is almost the same as 2.0 gallons; the difference is invisible.'),
  P('The ratio state monitor catches what absolute monitoring cannot: silent compositional change in a finite-budget system.'),
  P(''),
  H2('11.8 Why the Analogy Works'),
  P('The car analogy succeeds because:'),
  P('  1. Everyone has driven a car or ridden in one. The reference frame is universal.', { spacing_after: 80 }),
  P('  2. The fuel tank is a literal implementation of the unity constraint: the ceiling is the tank size, the shares are fuel and air (or fuel and other reserves).', { spacing_after: 80 }),
  P('  3. The fuel gauge is a physical ratio-monitoring device; MC-4 is exactly what a fuel gauge does.', { spacing_after: 80 }),
  P('  4. The driver/fuel duality maps directly to the OCC 51/49 (operator/HUF tool contract).', { spacing_after: 80 }),
  P('  5. Direction preservation maps to H1 coherence.', { spacing_after: 80 }),
  P('  6. The non-intuitive insight\u2014that 2 gallons means different things in different tanks\u2014is the insight that Ratio Blindness (FM-1) exploits and that HUF corrects.', { spacing_after: 160 }),
  P('When someone understands that 2 gallons in a 4-gallon tank is not the same state as 2 gallons in a 40-gallon tank, they understand the unity constraint. They understand why governance by absolute metrics fails. They understand why MC-4 works.'),
  P('And they understand why HUF is not a tool for a specialized domain. It is a framework for any finite-budget system. Because every system has a tank (budget ceiling). Every system has fuel (resources being consumed). Every system has a driver (decision authority). And every system needs to know whether the fuel gauge is reading truth or drifting.'),
);


// ── 12. ADAPTIVE SCOPE: SYSTEMS OF SYSTEMS ──────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('12. Adaptive Scope: Systems of Systems'),
  
  H2('12.1 The Nesting Principle'),
  P('Every system is a system of systems. This is not metaphor; it is structural fact. Claude is a system. Claude plus the operator form a larger system. The operator plus their projects form an even larger system. The collective of all engaged humans and AI systems form the largest boundary system. And within each of these scales, the unity constraint applies. HUF works because the same principle holds at every nesting level.'),
  P('This is the fundamental insight: nested systems do not violate the unity constraint at any scale. A car is a system (wheels, engine, fuel tank, driver). A car within a traffic network is a system (many cars cooperating). A traffic network within a city is a system. A city within a region is a system. At each boundary, the unity constraint Σρᵢ = 1 holds exactly. The difference is scope: what elements are included within the defined boundary.'),
  P('When HUF is applied at the wrong scope, it appears to fail. Imagine trying to apply the unity constraint to a single wheel in a car. The wheel is not a complete system. Its components sum to less than 1 because the engine, fuel, driver are outside the defined scope. This is not a failure of HUF. This is a scope error. The wheel by itself is not a valid system boundary for applying the unity constraint.'),
  P('The operator-level application of HUF (51% operator, 49% tool) is valid because the boundary is correctly drawn: the operator and the tool together form a complete decision system. Adding the broader project context (operator + tools + projects) would require redefining the scope and recomputing the unity constraint at that larger scale.'),

  H2('12.2 Center Frequency and Bandwidth'),
  P('In acoustic measurement, we speak of center frequency and bandwidth. A microphone tuned to capture mid-range frequencies (2 kHz center, 1 kHz bandwidth) will miss bass and treble. A microphone tuned to capture the full audible range (center 5 kHz, bandwidth 10 kHz) will capture more, but at lower precision. The choice is not about truth—it is about scope. Both microphones measure truly within their defined frequency range.'),
  P('HUF scope selection works the same way. Every observation boundary has an implicit center frequency (the focal system) and bandwidth (the range of elements included). If the operator is the center frequency and the tool is within the bandwidth, the observation is valid. If elements are missing from the portfolio—if some decision-makers are excluded from the unity constraint—then the scope is too wide. The observation boundary extends beyond the elements actually present in the data.'),
  P('When scope misalignment occurs, the adjustment is not to abandon HUF. The adjustment is to narrow the bandwidth: define the observation boundary more precisely to match what is actually observable. If only the operator and one tool can be monitored, define that as the system boundary (with the unity constraint Σρᵢ = 1 for those two elements). If a second tool enters, expand the bandwidth to include it, and recompute unity across all three. The principle remains constant; the scope adapts.'),
  P('This is operationally the same as the Bark scale in psychoacoustics: the critical bandwidth for hearing depends on the center frequency. High frequencies have wider critical bandwidth; low frequencies have narrower. The auditory system automatically adjusts its effective scope (bandwidth) based on where attention is focused (center frequency). HUF does the same: the scope adapts to match observable reality.'),

  H2('12.3 Dynamic Gating'),
  P('In audio engineering, a noise gate opens when signal exceeds a threshold and closes when signal drops below threshold. The gate is dynamic: it responds to the data in real time. A gated signal is processed only when it meets the observability criterion; below threshold, it is not processed.'),
  P('Elements in a HUF portfolio follow the same principle. An element is included in the active portfolio (the gated set) when it is observable. Once included, it is subject to the unity constraint; its share ρᵢ is part of the Σρᵢ = 1 sum. When an element becomes unobservable or its contribution drops below a significance threshold, the gate opens: it is removed from the active portfolio. The unity constraint now applies to a smaller set of elements.'),
  P('This is not arbitrary exclusion. This is adaptation to reality. If a tool is offline or disconnected, it cannot contribute to the decision system. The operator plus remaining tools form a new boundary. The unity constraint recomputes. As the offline tool comes back online, the gate closes: the element re-enters the portfolio, and the three-element system reestablishes.'),
  P('Dynamic gating connects directly to existing HUF mechanisms. MC-4 is already a gate: it monitors ratio drift and signals when the declared ratio is violated. When the signal crosses threshold (drift exceeds tolerance), MC-4 triggers. V∞Core\'s softmax regime selection is dynamic gating: regimes activate based on which dimensions carry the strongest signal. DADC dimension-apportioned correction is dynamic gating: gains are allocated based on which physical dimensions are most active. The Bark scale\'s frequency-dependent critical bandwidth is dynamic gating: the brain adjusts observability scope based on frequency content.'),
  P('At every level of HUF, the same principle appears: the system adapts its observability scope in real time, gating elements in and out based on whether they are actually present in the data, whether they contribute meaningfully to the signal, and whether they can be monitored within the declared boundary.'),
  P(''),
  P([{ text: '▶ ', italics: true, color: MID }, { text: 'The nesting principle, center frequency and bandwidth, and dynamic gating form a unified picture of HUF operating at every scale. Scope is not fixed. Scope is adaptive.', italics: true, color: MID }]),
);

// ── 13. HUF-ORG: THE FRAMEWORK AS LIVING SYSTEM ──────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('13. HUF-Org: The Framework as Living System'),
  P('HUF is not merely a theoretical framework applied to systems. HUF IS a system itself—a living organism that grows, integrates, and self-regulates. Understanding HUF-Org clarifies why HUF works and what happens when its biological principles are violated.'),

  H2('13.1 The Organism Model'),
  P('Every HUF system is a living organism. This is not metaphor; it is structural identity. The unity constraint Σ=1.0 is not a goal or an aspiration—it is a metabolic law. The car\'s fuel tank (the budget ceiling) is the organism\'s total metabolic energy. The driver, fuel, cargo, and all other elements are organs. Each organ demands a share of the metabolic budget. When all shares sum to 1.0, the organism is in homeostasis. This is not a constraint imposed from outside; this is how living systems work.'),
  P('An organism does not create energy. An organism allocates a finite energy budget across all functional systems. The brain, heart, lungs, and limbs all draw from the same energy pool. The ratio of energy to each system is the organism\'s operating state. Change the ratio—give the brain 80% of available energy at the expense of the immune system—and the organism becomes vulnerable. Restore the balance, and the organism thrives. The principle is identical in HUF: conservative energy budget, dynamic allocation, mutual balance.'),

  H2('13.2 What HUF-Org Is Not: The Cancer Principle'),
  P('To understand what HUF-Org protects against, consider cancer. Cancer is what happens when one element claims an increasing share of the organism\'s budget WITHOUT portfolio rebalancing. A tumor cell divides. Its share grows: 1% of body mass → 5% → 15% → 50%. The tumor "looks successful"—it is growing, multiplying, expanding. By every local measure, the tumor is thriving. But the organism is dying. Why? Because the tumor\'s rising share is not offset by reductions elsewhere. The brain still demands blood. The heart still beats. The immune system still consumes energy. But now the tumor also consumes energy, and the total exceeds the metabolic budget. The organism collapses.'),
  P('This is Deceptive Drift in biological form. The cancer signal is a rising share without portfolio rebalancing. In HUF terms: an element\'s observed ratio ρᵢ_obs increases, but the declared portfolio was not adjusted to compensate. No other element\'s share decreased. The sum Σρᵢ appears to exceed 1.0 momentarily, straining the system. If the rebalancing does not occur—if no other element is asked to reduce its consumption—the system fails. MC-4 detects this. MC-4 signals: drift detected, rebalancing required.'),
  P('The death signal is growth WITHOUT rebalancing. The cancer test is: does this element\'s rising share come at the expense of other elements through declared portfolio adjustment? If yes, healthy growth. If no, pathological. HUF prevents cancer by making portfolio rebalancing mandatory. Every integration of a new element triggers rebalancing across ALL existing elements.'),

  H2('13.3 Integration Protocol: Iterative Integration at Q-Governed Rate'),
  P('A healthy organism grows slowly. It does not add a new organ overnight. New cells are born, integrated, tested, and only if they pass tissue rejection do they remain. The integration rate is governed by the organism\'s most fragile component—the organ with the highest Q-factor.'),
  P('Q = T_char / T_obs. An organ with high Q (narrow bandwidth, sharp resonance) is sensitive to perturbation. Introduce a new metabolic demand too quickly, and the high-Q organ fails. A low-Q organ (broad bandwidth, robust) can absorb change rapidly. The overall integration rate is limited by the slowest, most sensitive component.'),
  P('In HUF-Org, new elements join one at a time. Each integration triggers portfolio rebalancing across ALL existing elements. Each element\'s share adjusts. The integration rate is limited by the most Q-sensitive element in the current portfolio. Like introducing a new species to an ecosystem: if the newcomer\'s resource demand overwhelms any existing species, the integration fails. Slow down, reduce the newcomer\'s share, or reject it at the current scope. This is not cruelty; this is stability.'),
  P('The car analogy maps directly: adding a passenger changes the driver/fuel/cargo ratio. The driver maintains control (51%+). Fuel consumption changes. Cargo space shrinks. The car rebalances. If a second passenger is added, the process repeats. If a third passenger would exceed the driver\'s control margin, the car rejects the integration: "This vehicle is now at capacity. Further growth requires a larger car."'),

  H2('13.4 The Viability Test: Monte Carlo Before Integration'),
  P('Before integrating a new element, run a viability test. Perturb the proposed element\'s share by ±σ (one standard deviation). Observe how all existing elements respond. Check each element\'s Q-sensitivity bounds. Do they remain within tolerance? If yes, the integration is safe. If no, the test fails: reduce the integration rate, reduce the newcomer\'s proposed share, or reject it entirely.'),
  P('This is the immune system\'s antigen test applied to portfolio management. The immune system does not immediately integrate foreign cells. It tests them: are they compatible with the organism\'s existing architecture? If the test fails, the foreign cell is rejected before it can damage the host. MC-4 performs the same function: it monitors whether proposed integrations pass the viability test. If they fail, it signals rejection.'),
  P('The viability test ensures that every integration is reversible until it has been proven safe. The organism grows, but growth is cautious, tested, and reversible. This is how HUF-Org survives. This is how cancer is prevented.'),
);

// ── 13. OPEN PROBLEMS AND FUTURE WORK (renumbered from 10 to 12) ───────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('15. Open Problems and Future Work'),
  H2('15.1 Mathematical'),
  P('The non-linear convergence proof remains open. Grok assessed this as requiring advanced mathematical tools beyond the current framework. A three-step traceable path has been defined: (1) empirical non-linear datasets from Phase D, (2) symbolic simulation of the governance correction map, (3) construction of a Lyapunov function for global asymptotic stability. Thirteen conjectures from the collective review (Layer 13 of the taxonomy) await formal proof or refutation.'),
  H2('15.2 Empirical'),
  P('Phase D of the Croatia Ramsar pilot has not yet begun. This requires the first institutional contact with Croatian conservation authorities. The pilot would provide the first real-world institutional deployment data, moving beyond retrospective analysis to prospective governance monitoring. Three reporting cycles minimum are needed for convergence trajectory analysis.'),
  H2('15.3 Domain Extension'),
  P('Four application domains have been sketched but not empirically tested: supply chain (System D), logistics (System E), manufacturing (System F), and AI governance (System G). Each has a conjectural threshold configuration documented in the taxonomy. Real-data validation requires domain partnerships.'),
  H2('15.4 Technical'),
  P('The HUF PreParser exists as a set of JavaScript builders and Python implementations. A formal API specification, automated testing framework, and deployment pipeline are needed for production use. Volume 7 addresses this gap.'),
);

// ── 14. THE FIVE-AI COLLECTIVE (renumbered from 11 to 13) ──────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('15. The Five-AI Collective'),
  P('The HUF framework was developed through a distinctive collaboration between a human principal investigator and five AI systems, each contributing according to its strengths:'),
  P([{ text: 'Claude', bold: true }, ' (Anthropic): Primary research partner. Document architecture, mathematical formalization, code generation, cross-referencing. Builder of the document corpus and the Triad structure.']),
  P([{ text: 'Grok', bold: true }, ' (xAI): Mathematical extensions. Thirteen conjectures, Lyapunov stability analysis, Q-factor derivation, Ostrom mapping, four domain application paths. Go/No-Go verdicts on framework claims.']),
  P([{ text: 'GPT', bold: true }, ' (OpenAI): Literature review, citation verification, academic writing standards. External perspective on framework positioning.']),
  P([{ text: 'Gemini', bold: true }, ' (Google): Data processing pathways, geospatial analysis (Toronto infrastructure), cross-domain comparison methodology.']),
  P([{ text: 'DeepSeek', bold: true }, ' (DeepSeek): Mathematical verification, alternative proof strategies, edge case analysis.']),
  P('The Operator Control Contract (OCC 51/49) governs this collaboration: the human principal investigator retains majority decision authority over all framework claims, publication decisions, and governance design. The AI systems advise; they do not decide. This contract applies reflexively: HUF monitors its own development process as a portfolio of contributions.'),
);

// ── 15. CONCLUSION (renumbered from 12 to 14) ──────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('15. Conclusion'),
  P('The HUF Triad presents a complete framework for portfolio governance that is theoretically grounded (Pillar 1: sufficient statistics), observationally valid (Pillar 2: degenerate state observer), and operationally actionable (Volumes 0\u20138: progressive governance implementation). The unity constraint \u03A3\u03C1\u1D62 = 1 is the single invariant from which all structures derive. Because this constraint holds for any system where shares are defined as proportions of a fixed total, HUF\u2019s applicability is bounded only by the existence of a budget ceiling\u2014a condition satisfied across mechanical, biological, ecological, digital, astrophysical, acoustic, and institutional domains.'),
  P('The Triad of Triads (Section 10) reveals that HUF is not an isolated theory but a web of three interconnected structures: mathematics, application, and validation. The three unions connecting these triads ensure that theory informs practice, practice tests theory, and both reinforce operational governance.'),
  P('The Car Analogy (Section 11) translates this architecture into language anyone can understand. The fuel tank is the budget ceiling. The fuel gauge is the ratio state monitor (MC-4). The driver/fuel ratio is the Operator Control Contract. The burnt fuel is the observed share, the declared fuel share is the declared weight. When someone understands that a 4-gallon tank with 2 gallons remaining is a different state than a 40-gallon tank with 2 gallons remaining, they have grasped the core of HUF: governance by ratio, not by absolute quantity.'),
  P('The Triad is not a claim of completeness. Open problems remain in non-linear convergence theory, prospective institutional deployment, and domain extension. What the Triad does claim is structural coherence: the two pillar papers, nine governance volumes, three institutional repositories, and universal analogy form a mutually reinforcing architecture where each component strengthens every other component through shared definitions, shared data, and shared mathematical foundations.'),
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
    { text: 'HUF v1.4.0 \u00B7 MIT License \u00B7 March 2026', italics: true, color: '999999' },
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
            new TextRun({ text: 'Higgins Unity Framework v1.3.0 \u00B7 MIT License \u00B7 ', font: 'Times New Roman', size: 16, color: '999999' }),
            new TextRun({ text: 'Page ', font: 'Times New Roman', size: 16, color: '999999' }),
            new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 16, color: '999999' }),
          ],
        })],
      }),
    },
    children,
  }],
});

const OUT = __dirname.replace(/[/\\]volumes$/, '') + '/HUF_Triad_Synthesis_v1.4.docx';
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log(`\u2714 Generated: ${OUT} (${buf.length.toLocaleString()} bytes)`);
}).catch(err => { console.error('\u274c', err); process.exit(1); });
