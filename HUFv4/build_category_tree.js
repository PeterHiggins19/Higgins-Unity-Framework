// ══════════════════════════════════════════════════════════════════════
// HUF Category Class Structure Tree — Document Builder
// Maps all 85 categories (A–CH) from 14 reviews / 5 AI systems
// into a hierarchical tree showing how the review corpus organizes
// ══════════════════════════════════════════════════════════════════════

const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition,
        LevelFormat } = require('docx');

// ── Page Constants ──────────────────────────────────────────────────
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;
const CW = PAGE_W - 2 * MARGIN; // 9360

// ── Color Palette (HUF Standard) ────────────────────────────────────
const BLUE  = '1F3864';
const MID   = '2E75B6';
const DARK  = '333333';
const LGREY = 'F2F2F2';
const LBLUE = 'D6E4F0';
const WHITE = 'FFFFFF';
const GREEN = 'E2EFDA';
const GOLD  = 'FFF2CC';
const TEAL  = '1B5E5E';
const CORAL = 'E8D5C4';

// ── Borders ─────────────────────────────────────────────────────────
const bdr = { style: BorderStyle.SINGLE, size: 1, color: 'BBBBBB' };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };
const noBorder = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

// ── Style Definitions ───────────────────────────────────────────────
const styles = {
  default: { document: { run: { font: 'Times New Roman', size: 22 } } },
  paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 32, bold: true, font: 'Times New Roman', color: BLUE },
      paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 26, bold: true, font: 'Times New Roman', color: BLUE },
      paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
    { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 23, bold: true, italics: true, font: 'Times New Roman', color: DARK },
      paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
  ],
};

const numbering = {
  config: [
    { reference: 'bullets', levels: [
      { level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      { level: 1, format: LevelFormat.BULLET, text: '\u25E6', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 1080, hanging: 360 } } } },
      { level: 2, format: LevelFormat.BULLET, text: '\u2013', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
    ]},
  ],
};

// ── Helpers ──────────────────────────────────────────────────────────
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1,
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 32, color: BLUE })] });

const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2,
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 26, color: BLUE })] });

const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3,
  children: [new TextRun({ text: t, bold: true, italics: true, font: 'Times New Roman', size: 23, color: DARK })] });

function P(content, opts = {}) {
  const { align, indent, spacing_after, bold, italics, color } = opts;
  const runs = [];
  if (typeof content === 'string') {
    runs.push(new TextRun({ text: content, font: 'Times New Roman', size: 22, color: color || DARK,
      bold: bold || false, italics: italics || false }));
  } else if (Array.isArray(content)) {
    content.forEach(c => {
      if (typeof c === 'string') {
        runs.push(new TextRun({ text: c, font: 'Times New Roman', size: 22, color: DARK }));
      } else {
        runs.push(new TextRun({ font: 'Times New Roman', size: 22, color: DARK, ...c }));
      }
    });
  }
  return new Paragraph({
    spacing: { after: spacing_after || 160 },
    alignment: align || AlignmentType.JUSTIFIED,
    indent: indent ? { left: indent } : undefined,
    children: runs,
  });
}

function bullet(text, level = 0) {
  const runs = [];
  if (typeof text === 'string') {
    runs.push(new TextRun({ text, font: 'Times New Roman', size: 22, color: DARK }));
  } else if (Array.isArray(text)) {
    text.forEach(c => {
      if (typeof c === 'string') {
        runs.push(new TextRun({ text: c, font: 'Times New Roman', size: 22, color: DARK }));
      } else {
        runs.push(new TextRun({ font: 'Times New Roman', size: 22, color: DARK, ...c }));
      }
    });
  }
  return new Paragraph({
    numbering: { reference: 'bullets', level },
    spacing: { after: 80 },
    children: runs,
  });
}

function headerCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: BLUE, type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, font: 'Times New Roman', size: 20, bold: true, color: WHITE })] })],
  });
}

function dataCell(text, width, opts = {}) {
  const { shade, align, bold: b } = opts;
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    children: [new Paragraph({ alignment: align || AlignmentType.LEFT,
      children: [new TextRun({ text, font: 'Times New Roman', size: 20, color: DARK, bold: b || false })] })],
  });
}

function dataCellMulti(runs, width, opts = {}) {
  const { shade } = opts;
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    children: [new Paragraph({ children: runs.map(r =>
      new TextRun({ font: 'Times New Roman', size: 20, color: DARK, ...r })) })],
  });
}

// ── Section Break ───────────────────────────────────────────────────
function sectionBreak() {
  return new Paragraph({ spacing: { before: 120, after: 120 },
    children: [new TextRun({ text: '\u2500'.repeat(40), font: 'Times New Roman', size: 18, color: 'AAAAAA' })] });
}

// ══════════════════════════════════════════════════════════════════════
// DOCUMENT CONTENT
// ══════════════════════════════════════════════════════════════════════

function buildContent() {
  const children = [];

  // ── TITLE PAGE ────────────────────────────────────────────────────
  children.push(new Paragraph({ spacing: { before: 3600 } }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: 'HUF Category Class Structure Tree', font: 'Times New Roman',
      size: 44, bold: true, color: BLUE })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new TextRun({ text: 'Hierarchical Organization of the Collective Review Corpus',
      font: 'Times New Roman', size: 28, color: MID })] }));
  children.push(new Paragraph({ spacing: { before: 400 } }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: '85 Categories (A\u2013CH)  \u00B7  14 Reviews  \u00B7  5 AI Systems',
      font: 'Times New Roman', size: 24, color: DARK })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'Higgins Unity Framework v4.0 Corpus',
      font: 'Times New Roman', size: 22, color: DARK })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'March 2026',
      font: 'Times New Roman', size: 22, color: DARK })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 200 },
    children: [new TextRun({ text: 'Author: Peter Higgins',
      font: 'Times New Roman', size: 24, italics: true, color: DARK })] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'Document Builder: Claude (Anthropic)',
      font: 'Times New Roman', size: 20, color: '666666' })] }));

  children.push(new Paragraph({ children: [new PageBreak()] }));

  // ── 1. INTRODUCTION ───────────────────────────────────────────────
  children.push(H1('1. Introduction'));
  children.push(P('The Higgins Unity Framework (HUF) has undergone a comprehensive collective review process involving fourteen independent reviews from five AI systems: Claude, Grok, ChatGPT, Gemini, and Copilot. DeepSeek contributed one early review (R4). This process generated 85 distinct feedback categories, labeled A through CH, spanning mathematical validation, empirical verification, editorial improvements, tetrahedral geometry and scaling, research design, and operational governance. Review counts are data, not contribution scores\u2014all five systems are equal members of the collective.'));
  children.push(P('This document organizes all 85 categories into a hierarchical class structure tree, revealing how the review corpus itself constitutes a structured knowledge base. The tree exposes relationships between categories, maps them to HUF\u2019s pillar architecture, and identifies the evidentiary tiers that the collective consensus demands.'));
  children.push(P('The purpose is twofold: (1) to provide a navigational map of the entire review corpus for any reader approaching HUF for the first time, and (2) to serve as an appendix-ready reference that can be integrated into the Collective Trace or any future publication.'));

  // ── 2. REVIEW PROVENANCE ──────────────────────────────────────────
  children.push(H1('2. Review Provenance'));
  children.push(P('The thirteen reviews were conducted in March 2026. The five AI systems of the collective are listed below with their review contributions. Review counts are data; all five members contribute equally.'));

  // AI Systems table — 5 members
  const rCols = [1400, 1200, 2200, 4560];
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: rCols,
    rows: [
      new TableRow({ children: [
        headerCell('AI System', rCols[0]), headerCell('Reviews', rCols[1]),
        headerCell('Categories', rCols[2]), headerCell('Key Contributions', rCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('Claude', rCols[0], { shade: LGREY, bold: true }), dataCell('R5 (Moderator)', rCols[1], { shade: LGREY }),
        dataCell('Synthesis role', rCols[2], { shade: LGREY }),
        dataCell('5-tier evidentiary taxonomy, arbitration across all reviews, moderator assessments', rCols[3], { shade: LGREY }),
      ]}),
      new TableRow({ children: [
        dataCell('Grok', rCols[0], { bold: true }), dataCell('R2, R7, R10, R14', rCols[1]),
        dataCell('I\u2013M, AD\u2013AH, AX\u2013CH (23)', rCols[2]),
        dataCell('Citation verification, ML conjecture, TDA simulation, 10-architecture sweep, tetrahedral geometry, Ramsar application, sister sites, sufficiency simulations, detection metrics, PH mixture detection, Ramsar simulations, topology reference', rCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('ChatGPT', rCols[0], { shade: LGREY, bold: true }), dataCell('R1, R9, R12, R13', rCols[1], { shade: LGREY }),
        dataCell('A\u2013H, AO\u2013AW, BG\u2013BZ (37)', rCols[2], { shade: LGREY }),
        dataCell('Evidentiary hierarchy (C1), editorial prescription, theorem sharpening (C3/C4), milestone sequencing, phase assessment, four-layer architecture, action sequencing, meta-structural analysis, kinetic governance reframing', rCols[3], { shade: LGREY }),
      ]}),
      new TableRow({ children: [
        dataCell('Gemini', rCols[0], { bold: true }), dataCell('R3, R8, R11', rCols[1]),
        dataCell('N\u2013Q, AI\u2013AN, BC\u2013BF (14)', rCols[2]),
        dataCell('Logical closure verdict, Temporal Sieve (dHUF/dt), optical extension, Simplicial Consensus Logic, RTC cascade, scale-invariant observer', rCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('Copilot', rCols[0], { shade: LGREY, bold: true }), dataCell('R6', rCols[1], { shade: LGREY }),
        dataCell('W\u2013AC (7)', rCols[2], { shade: LGREY }),
        dataCell('Theorem formalization, UDI, ML experiment design, Phase 3 research specification', rCols[3], { shade: LGREY }),
      ]}),
    ],
  }));
  children.push(P(''));
  children.push(P('Note: DeepSeek contributed Review 4 (categories R\u2013V, 5 categories) covering scope conditions and operational stack design. Review counts by AI system: Grok (4), ChatGPT (4), Gemini (3), Claude (1), Copilot (1), DeepSeek (1). Total: 14 reviews, 85 categories.'));
  children.push(P(''));

  // ── 3. THE CLASS STRUCTURE TREE ───────────────────────────────────
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(H1('3. The Category Class Structure Tree'));
  children.push(P('The 85 categories organize into seven primary branches, each representing a distinct domain of concern within the HUF review corpus. The tree is not a linear sequence but a lattice: categories cross-reference each other, and several categories belong to more than one logical branch. The primary assignment reflects the category\u2019s strongest affinity.'));

  // ── BRANCH 1: INFRASTRUCTURE ──────────────────────────────────────
  children.push(H2('3.1 Branch I: Infrastructure & Governance'));
  children.push(P('Categories concerned with the repository, data provenance, evidentiary hierarchy, and release discipline. These are framework-level concerns that apply to every document in the corpus.'));

  const b1Cols = [900, 2700, 1200, 4560];
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b1Cols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b1Cols[0]), headerCell('Name', b1Cols[1]),
        headerCell('Review', b1Cols[2]), headerCell('Scope', b1Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('A', b1Cols[0], { bold: true, shade: LBLUE }), dataCell('Repo Structure & Build Discipline', b1Cols[1], { shade: LBLUE }),
        dataCell('R1', b1Cols[2], { shade: LBLUE }), dataCell('README, LICENSE, .gitignore, dist/ separation, build entry point', b1Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('B', b1Cols[0], { bold: true }), dataCell('Data Management & Provenance', b1Cols[1]),
        dataCell('R1', b1Cols[2]), dataCell('Data manifest, acquisition instructions, checksums, redistribution policy', b1Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('C', b1Cols[0], { bold: true, shade: GOLD }), dataCell('Evidentiary Hierarchy & Labeling', b1Cols[1], { shade: GOLD }),
        dataCell('R1', b1Cols[2], { shade: GOLD }), dataCell('5-tier taxonomy: [THEOREM] [EMPIRICAL] [IDENTITY] [CONJECTURE] [PEDAGOGICAL]', b1Cols[3], { shade: GOLD }),
      ]}),
      new TableRow({ children: [
        dataCell('H', b1Cols[0], { bold: true }), dataCell('Content Advisories', b1Cols[1]),
        dataCell('R1', b1Cols[2]), dataCell('Path scrubbing, release layering, AI-review labeling', b1Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('T', b1Cols[0], { bold: true, shade: LBLUE }), dataCell('Reproducibility & Evidence Requirements', b1Cols[1], { shade: LBLUE }),
        dataCell('R4', b1Cols[2], { shade: LBLUE }), dataCell('PreParser config packaging, power analyses, confusion matrices, FDR', b1Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('V', b1Cols[0], { bold: true }), dataCell('Operational Risk Solution', b1Cols[1]),
        dataCell('R4', b1Cols[2]), dataCell('3-layer gating stack: defaults, automated sensitivity, anti-gaming', b1Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AW', b1Cols[0], { bold: true, shade: LBLUE }), dataCell('Trace & Repo Management', b1Cols[1], { shade: LBLUE }),
        dataCell('R9', b1Cols[2], { shade: LBLUE }), dataCell('Hard-mark evidentiary tiers, advisory labels, benchmark manifest', b1Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BH', b1Cols[0], { bold: true }), dataCell('Four-Layer Program Architecture', b1Cols[1]),
        dataCell('R12', b1Cols[2]), dataCell('Hierarchical governance model: detect \u2192 isolate \u2192 aggregate \u2192 report', b1Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BM', b1Cols[0], { bold: true, shade: LBLUE }), dataCell('Review Process as Infrastructure', b1Cols[1], { shade: LBLUE }),
        dataCell('R12', b1Cols[2], { shade: LBLUE }), dataCell('Collective review discipline, audit trails, integration methodology', b1Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BP', b1Cols[0], { bold: true }), dataCell('Status Discipline Risk', b1Cols[1]),
        dataCell('R12', b1Cols[2]), dataCell('Release gating, completeness tracking, milestone validation', b1Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BS', b1Cols[0], { bold: true, shade: LBLUE }), dataCell('Release Discipline Risk', b1Cols[1], { shade: LBLUE }),
        dataCell('R12', b1Cols[2], { shade: LBLUE }), dataCell('Deployment safety, version control, rollback procedures', b1Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BU', b1Cols[0], { bold: true }), dataCell('Program-Level Synthesis Layer', b1Cols[1]),
        dataCell('R13', b1Cols[2]), dataCell('High-level governance synthesis, cross-module coherence, program-level architecture', b1Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BV', b1Cols[0], { bold: true, shade: LBLUE }), dataCell('Review Memory Reorganization', b1Cols[1], { shade: LBLUE }),
        dataCell('R13', b1Cols[2], { shade: LBLUE }), dataCell('Collective memory restructuring, artifact linking, review history synthesis', b1Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BZ', b1Cols[0], { bold: true }), dataCell('Risk as First-Class Category', b1Cols[1]),
        dataCell('R13', b1Cols[2]), dataCell('Risk governance framework, risk taxonomy, mitigation strategies integration', b1Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('CF', b1Cols[0], { bold: true, shade: LBLUE }), dataCell('Domain Integration Archive', b1Cols[1], { shade: LBLUE }),
        dataCell('R14', b1Cols[2], { shade: LBLUE }), dataCell('Ramsar domain data, archive structure, integration protocols, versioning', b1Cols[3], { shade: LBLUE }),
      ]}),
    ],
  }));
  children.push(P([
    { text: 'Keystone: ', bold: true },
    'Category C (Evidentiary Hierarchy) is the single highest-value item across the entire review corpus. All 9 reviews converge on the need for explicit evidentiary labeling. The 5-tier taxonomy\u2014[THEOREM], [EMPIRICAL], [IDENTITY], [CONJECTURE], [PEDAGOGICAL]\u2014was proposed in Review 5 (Claude) and endorsed by all subsequent reviewers.'
  ]));

  // ── BRANCH 2: PILLAR-SPECIFIC ─────────────────────────────────────
  children.push(H2('3.2 Branch II: Pillar-Specific Feedback'));
  children.push(P('Categories that target individual HUF pillar documents. These represent the editorial and content-level refinements each document needs for its next version.'));

  const b2Cols = [900, 2700, 1200, 4560];
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b2Cols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b2Cols[0]), headerCell('Name', b2Cols[1]),
        headerCell('Review', b2Cols[2]), headerCell('Target Document & Key Items', b2Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('D', b2Cols[0], { bold: true, shade: LBLUE }), dataCell('Sufficiency Frontier Specific', b2Cols[1], { shade: LBLUE }),
        dataCell('R1', b2Cols[2], { shade: LBLUE }), dataCell('SF v3.6 \u2192 v3.7: theorem form, benchmark, retained-vs-lost table', b2Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('E', b2Cols[0], { bold: true }), dataCell('Fourth Category Specific', b2Cols[1]),
        dataCell('R1', b2Cols[2]), dataCell('FC v2.6 \u2192 v2.7: theorem vs heuristic, "Where MC-4 Should Not Be Used"', b2Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('F', b2Cols[0], { bold: true, shade: LBLUE }), dataCell('Triad Synthesis Specific', b2Cols[1], { shade: LBLUE }),
        dataCell('R1', b2Cols[2], { shade: LBLUE }), dataCell('Triad v1.6 \u2192 v1.7: claim map matrix, cross-reference tightening', b2Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('G', b2Cols[0], { bold: true }), dataCell('Trace Specific', b2Cols[1]),
        dataCell('R1', b2Cols[2]), dataCell('Trace v5.5+: evidentiary status per section, framing note', b2Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('X', b2Cols[0], { bold: true, shade: GOLD }), dataCell('Sufficiency Theorem Formalization', b2Cols[1], { shade: GOLD }),
        dataCell('R6', b2Cols[2], { shade: GOLD }), dataCell('A1\u2013A3 axioms, 3-part theorem (sufficiency, minimality, uniqueness), C1\u2013C2', b2Cols[3], { shade: GOLD }),
      ]}),
      new TableRow({ children: [
        dataCell('AS', b2Cols[0], { bold: true, shade: GOLD }), dataCell('Sufficiency Theorem Sharpening', b2Cols[1], { shade: GOLD }),
        dataCell('R9', b2Cols[2], { shade: GOLD }), dataCell('C3 (hidden-state), C4 (changing-element), A2 foregrounding, Part 3 to appendix', b2Cols[3], { shade: GOLD }),
      ]}),
    ],
  }));
  children.push(P([
    { text: 'Keystone: ', bold: true },
    'Categories X and AS together define the formal Sufficiency Theorem with four counterexamples (C1: absolute magnitude, C2: temporal order, C3: hidden-state governance, C4: changing-element governance). This theorem is the mathematical anchor for the entire framework and the consensus #1 priority across all reviews.'
  ]));

  // ── BRANCH 3: VALIDATION ──────────────────────────────────────────
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(H2('3.3 Branch III: Validation & Verification'));
  children.push(P('Categories where reviewers tested, verified, or assessed the framework\u2019s claims. This branch contains the empirical evidence that the collective has independently confirmed HUF\u2019s mathematical and factual foundations.'));

  children.push(H3('3.3a Verdicts & Strengths'));
  const b3aCols = [900, 2700, 1200, 4560];
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('What Was Validated', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('I', b3aCols[0], { bold: true, shade: GREEN }), dataCell('Document-Level Sanity Verdicts', b3aCols[1], { shade: GREEN }),
        dataCell('R2', b3aCols[2], { shade: GREEN }), dataCell('All 4 pillars + builder: no contradictions, coherent, clean', b3aCols[3], { shade: GREEN }),
      ]}),
      new TableRow({ children: [
        dataCell('J', b3aCols[0], { bold: true, shade: GREEN }), dataCell('Math & Citation Verification', b3aCols[1], { shade: GREEN }),
        dataCell('R2', b3aCols[2], { shade: GREEN }), dataCell('Fisher 1922, Shannon 1948, Pettitt OD, TTC +20%, Q=83dB, JND=0.25dB', b3aCols[3], { shade: GREEN }),
      ]}),
      new TableRow({ children: [
        dataCell('N', b3aCols[0], { bold: true, shade: GREEN }), dataCell('Pillar-by-Pillar Logical Verdicts', b3aCols[1], { shade: GREEN }),
        dataCell('R3', b3aCols[2], { shade: GREEN }), dataCell('SF: "most aggressive"; FC: "logic holds"; Triad: "binds"; Trace: "sound"', b3aCols[3], { shade: GREEN }),
      ]}),
      new TableRow({ children: [
        dataCell('O', b3aCols[0], { bold: true, shade: GREEN }), dataCell('Validation Details', b3aCols[1], { shade: GREEN }),
        dataCell('R3', b3aCols[2], { shade: GREEN }), dataCell('6M:1 ratio, Planck OD, degenerate observer, softmax=unity, Car/Fuel', b3aCols[3], { shade: GREEN }),
      ]}),
      new TableRow({ children: [
        dataCell('R', b3aCols[0], { bold: true, shade: GREEN }), dataCell('Logical Strengths Confirmed', b3aCols[1], { shade: GREEN }),
        dataCell('R4', b3aCols[2], { shade: GREEN }), dataCell('Formalization, domain-agnostic framing, reproducibility, multiple validation modalities', b3aCols[3], { shade: GREEN }),
      ]}),
      new TableRow({ children: [
        dataCell('AI', b3aCols[0], { bold: true, shade: GREEN }), dataCell('Framework Evolution Assessment', b3aCols[1], { shade: GREEN }),
        dataCell('R8', b3aCols[2], { shade: GREEN }), dataCell('ML bridge: analogy\u2192identity; HUF-Org: validated; Car/Fuel: effective pedagogy', b3aCols[3], { shade: GREEN }),
      ]}),
    ],
  }));

  children.push(H3('3.3b Risk Analysis & Logical Gaps'));
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('Key Risks Identified', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('P', b3aCols[0], { bold: true, shade: CORAL }), dataCell('Logical Risks (Gemini)', b3aCols[1], { shade: CORAL }),
        dataCell('R3', b3aCols[2], { shade: CORAL }), dataCell('Scaling invariance (domain constants), deterministic pipeline custody', b3aCols[3], { shade: CORAL }),
      ]}),
      new TableRow({ children: [
        dataCell('S', b3aCols[0], { bold: true, shade: CORAL }), dataCell('Key Logical Gaps (DeepSeek)', b3aCols[1], { shade: CORAL }),
        dataCell('R4', b3aCols[2], { shade: CORAL }), dataCell('Sufficiency scope (S1), element ID (S2), Q-model (S3), conflation (S4), frontier (S5)', b3aCols[3], { shade: CORAL }),
      ]}),
      new TableRow({ children: [
        dataCell('AK', b3aCols[0], { bold: true, shade: CORAL }), dataCell('Logical Risks (Gemini Extended)', b3aCols[1], { shade: CORAL }),
        dataCell('R8', b3aCols[2], { shade: CORAL }), dataCell('Mapping discontinuity, identity leap, FDR, low-Q collapse, discrete vs continuous', b3aCols[3], { shade: CORAL }),
      ]}),
    ],
  }));

  children.push(H3('3.3c ML Validation'));
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('ML Validation Content', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('K', b3aCols[0], { bold: true, shade: GREEN }), dataCell('ML Conjecture Validation', b3aCols[1], { shade: GREEN }),
        dataCell('R2', b3aCols[2], { shade: GREEN }), dataCell('6/6 conjectures valid: softmax, overfitting, regularization, LR, validation, early stopping', b3aCols[3], { shade: GREEN }),
      ]}),
      new TableRow({ children: [
        dataCell('M', b3aCols[0], { bold: true }), dataCell('ML Simulation Results', b3aCols[1]),
        dataCell('R2', b3aCols[2]), dataCell('MLP 1.5M params, sin(x), 18750 bps drift, MDG inconclusive (init issue)', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AF', b3aCols[0], { bold: true, shade: GREEN }), dataCell('ML Architecture Sweep (10 archs)', b3aCols[1], { shade: GREEN }),
        dataCell('R7', b3aCols[2], { shade: GREEN }), dataCell('MLP, CNN, RNN, LSTM, Transformer, ViT, GAN, Diffusion, SD, ControlNet', b3aCols[3], { shade: GREEN }),
      ]}),
      new TableRow({ children: [
        dataCell('AG', b3aCols[0], { bold: true }), dataCell('Architecture-Specific HUF Insights', b3aCols[1]),
        dataCell('R7', b3aCols[2]), dataCell('LSTM gates=MC-4, attention=purest unity, GAN=dual regime, hallucinations=FM-5', b3aCols[3]),
      ]}),
    ],
  }));

  children.push(H3('3.3d Math Foundations'));
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('Math Foundation Content', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BI', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Sufficiency Theorem Maturation', b3aCols[1], { shade: LBLUE }),
        dataCell('R12', b3aCols[2], { shade: LBLUE }), dataCell('Refined proof structure, boundary conditions, uniqueness strengthening', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BJ', b3aCols[0], { bold: true }), dataCell('Temporal Sieve as Dynamical Core', b3aCols[1]),
        dataCell('R12', b3aCols[2]), dataCell('dHUF/dt phase portrait, attractor topology, structural redistribution rates', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('CA', b3aCols[0], { bold: true, shade: GREEN }), dataCell('Sufficiency Theorem Simulation', b3aCols[1], { shade: GREEN }),
        dataCell('R14', b3aCols[2], { shade: GREEN }), dataCell('KL divergence confirmation on exponential family, Fisher sufficiency validation', b3aCols[3], { shade: GREEN }),
      ]}),
    ],
  }));

  // ── BRANCH 4: EXTENSIONS & NEW DOMAINS ────────────────────────────
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(H2('3.4 Branch IV: Extensions & New Domains'));
  children.push(P('Categories where the review process extended HUF into new theoretical or application domains beyond the original corpus. These represent the frontier of the framework\u2019s reach.'));

  children.push(H3('3.4a Spectral Sequences & Topology'));
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('Spectral / Topological Content', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AD', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Spectral Sequence Validation', b3aCols[1], { shade: LBLUE }),
        dataCell('R7', b3aCols[2], { shade: LBLUE }), dataCell('6 conjectures validated: filtration, differentials, pages, E\u221E, barcodes, FDR', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('AE', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('TDA Simulation Results', b3aCols[1], { shade: LBLUE }),
        dataCell('R7', b3aCols[2], { shade: LBLUE }), dataCell('ripser on simplex: FDR 0.12\u21920.05, power 0.92, Aitchison distance', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('Y', b3aCols[0], { bold: true }), dataCell('Spectral Engine Specification', b3aCols[1]),
        dataCell('R6', b3aCols[2]), dataCell('F\u2080\u2192F\u2083 filtration, E\u2080\u2013E\u221E pages, persistence rule, Planck/TTC/Bio tests', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AJ', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Spectral Formalization Assessment', b3aCols[1], { shade: LBLUE }),
        dataCell('R8', b3aCols[2], { shade: LBLUE }), dataCell('Simplex as base space [THEOREM], pages as refinements [CONJECTURE]', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('AT', b3aCols[0], { bold: true }), dataCell('Spectral Strategy', b3aCols[1]),
        dataCell('R9', b3aCols[2]), dataCell('Start with persistence diagrams first; promote to spectral only if algebra adds value', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('CC', b3aCols[0], { bold: true, shade: GREEN }), dataCell('PH for Mixture Detection', b3aCols[1], { shade: GREEN }),
        dataCell('R14', b3aCols[2], { shade: GREEN }), dataCell('Persistent homology resolves mixture insufficiency, Power 0.95, FDR 0.04', b3aCols[3], { shade: GREEN }),
      ]}),
      new TableRow({ children: [
        dataCell('CG', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Topological Algebra Foundation', b3aCols[1], { shade: LBLUE }),
        dataCell('R14', b3aCols[2], { shade: LBLUE }), dataCell('Algebraic topology foundations for HUF extension, cohomology framework', b3aCols[3], { shade: LBLUE }),
      ]}),
    ],
  }));

  children.push(H3('3.4b Temporal Sieve, Optical, & Network'));
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('Domain Extension', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AM', b3aCols[0], { bold: true, shade: GOLD }), dataCell('Temporal Sieve & Ratio Velocity', b3aCols[1], { shade: GOLD }),
        dataCell('R8', b3aCols[2], { shade: GOLD }), dataCell('dHUF/dt: structural redistribution invisible to absolute sensors', b3aCols[3], { shade: GOLD }),
      ]}),
      new TableRow({ children: [
        dataCell('AL', b3aCols[0], { bold: true }), dataCell('Optical Instrumentation Extension', b3aCols[1]),
        dataCell('R8', b3aCols[2]), dataCell('Microscope/telescope: resolution budget = unity, Abbe/diffraction limits', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AH', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Network Packet Demo', b3aCols[1], { shade: LBLUE }),
        dataCell('R7', b3aCols[2], { shade: LBLUE }), dataCell('ping 8.8.8.8: \u03C1_success + \u03C1_lost = 1, MDG rises 0\u219260.8 dB', b3aCols[3], { shade: LBLUE }),
      ]}),
    ],
  }));

  children.push(H3('3.4c Empirical Validation'));
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('Validation Content', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BL', b3aCols[0], { bold: true }), dataCell('Hell Test Sensitivity Boundary', b3aCols[1]),
        dataCell('R12', b3aCols[2]), dataCell('Extreme condition testing, phase transition stability, boundary layer dynamics', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BQ', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Detection Metrics Gap', b3aCols[1], { shade: LBLUE }),
        dataCell('R12', b3aCols[2], { shade: LBLUE }), dataCell('Reconciliation of detection metrics across domains, unified measurement protocol', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BN', b3aCols[0], { bold: true }), dataCell('Static-to-Dynamic Conceptual Shift', b3aCols[1]),
        dataCell('R12', b3aCols[2]), dataCell('Paradigm shift from equilibrium to kinetic frameworks, temporal evolution architecture', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BW', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Kinetic Governance Reframing', b3aCols[1], { shade: LBLUE }),
        dataCell('R13', b3aCols[2], { shade: LBLUE }), dataCell('HUF as kinetic governance framework not just descriptive simplex, dynamic allocation architecture', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('CB', b3aCols[0], { bold: true, shade: GREEN }), dataCell('Detection Performance Quantification', b3aCols[1], { shade: GREEN }),
        dataCell('R14', b3aCols[2], { shade: GREEN }), dataCell('Power 0.88, FDR 0.08, ROC AUC 0.92 across mixture detection domains', b3aCols[3], { shade: GREEN }),
      ]}),
    ],
  }));

  // ── BRANCH 5: PHASE 3 RESEARCH ────────────────────────────────────
  children.push(H2('3.5 Branch V: Phase 3 Research Design'));
  children.push(P('Categories that define the forward research program. Phase 3 transitions HUF from empirical validation to formal research, with four milestones: M1 (Sufficiency Theorem), M2 (Spectral Drift Engine), M3/M3b (Power Calibration / UDI), and M4 (ML Validation).'));

  children.push(H3('3.5a Roadmap & Milestones'));
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('Phase 3 Component', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('W', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Phase 3 Roadmap (4 Milestones)', b3aCols[1], { shade: LBLUE }),
        dataCell('R6', b3aCols[2], { shade: LBLUE }), dataCell('M1\u2192M2\u2192M3\u2192M4 sequencing with outputs and dependencies', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('AO', b3aCols[0], { bold: true }), dataCell('Phase 3 Milestone Logical Analysis', b3aCols[1]),
        dataCell('R8', b3aCols[2]), dataCell('Evidentiary tier per milestone: M1=[THEOREM], M2=[CONJECTURE], M3=[MODEL], M4=[EXPERIMENT]', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AR', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Milestone Sequencing & Priority', b3aCols[1], { shade: LBLUE }),
        dataCell('R9', b3aCols[2], { shade: LBLUE }), dataCell('M1 is "the hinge"; M2 is "strongest next"; M3 after M2 stability; M4 downstream', b3aCols[3], { shade: LBLUE }),
      ]}),
    ],
  }));

  children.push(H3('3.5b Research Specifications'));
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('Specification Content', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('Z', b3aCols[0], { bold: true }), dataCell('UDI Prototype Specification', b3aCols[1]),
        dataCell('R6', b3aCols[2]), dataCell('4-component (D,P,R,F), logistic squash, calibration plan, JSON schema', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AU', b3aCols[0], { bold: true, shade: CORAL }), dataCell('UDI Cautions', b3aCols[1], { shade: CORAL }),
        dataCell('R9', b3aCols[2], { shade: CORAL }), dataCell('No "universal" too early; weights may not transfer; add Q-missing rule', b3aCols[3], { shade: CORAL }),
      ]}),
      new TableRow({ children: [
        dataCell('AA', b3aCols[0], { bold: true }), dataCell('ML Experiment Specification', b3aCols[1]),
        dataCell('R6', b3aCols[2]), dataCell('CIFAR-10, ResNet-18, 4 regimes (R1\u2013R4), ratio extraction, ML filtration', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AB', b3aCols[0], { bold: true }), dataCell('ML Experiment Hypotheses & Plots', b3aCols[1]),
        dataCell('R6', b3aCols[2]), dataCell('H1\u2013H4 hypotheses, 8 plot specifications', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AV', b3aCols[0], { bold: true, shade: CORAL }), dataCell('ML Experiment Design Improvements', b3aCols[1], { shade: CORAL }),
        dataCell('R9', b3aCols[2], { shade: CORAL }), dataCell('max-share penalty too brittle; 3\u00D73 ablation (penalties \u00D7 extractions)', b3aCols[3], { shade: CORAL }),
      ]}),
      new TableRow({ children: [
        dataCell('AN', b3aCols[0], { bold: true }), dataCell('Formalization Requirements', b3aCols[1]),
        dataCell('R8', b3aCols[2]), dataCell('Differential gating theorem, scaling invariance proof, TDA integration', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BY', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Milestone Governance Sharpening', b3aCols[1], { shade: LBLUE }),
        dataCell('R13', b3aCols[2], { shade: LBLUE }), dataCell('Milestone clarity, governance milestone sequencing, temporal sharpening of research phases', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('CD', b3aCols[0], { bold: true, shade: GREEN }), dataCell('Ramsar Global Wetland Simulation', b3aCols[1], { shade: GREEN }),
        dataCell('R14', b3aCols[2], { shade: GREEN }), dataCell('Multi-site Ramsar data simulations, governance protocols, coordinated monitoring', b3aCols[3], { shade: GREEN }),
      ]}),
      new TableRow({ children: [
        dataCell('CE', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Mer Bleue Case Study', b3aCols[1], { shade: LBLUE }),
        dataCell('R14', b3aCols[2], { shade: LBLUE }), dataCell('Mer Bleue wetland simulation, MDG 39.3 dB validation, real-world application', b3aCols[3], { shade: LBLUE }),
      ]}),
    ],
  }));

  // ── BRANCH 6: SYNTHESIS & RECOMMENDATIONS ─────────────────────────
  children.push(H2('3.6 Branch VI: Synthesis, Recommendations, & Future'));
  children.push(P('Categories that synthesize across the corpus, provide reviewer-specific suggestions, and identify future research directions.'));

  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b3aCols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b3aCols[0]), headerCell('Name', b3aCols[1]),
        headerCell('Review', b3aCols[2]), headerCell('Content', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('L', b3aCols[0], { bold: true }), dataCell('Grok-Specific Suggestions', b3aCols[1]),
        dataCell('R2', b3aCols[2]), dataCell('Visuals, GTFS live validation, builder params, CNN/MNIST sim, identity vs metaphor', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('Q', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Gemini-Specific Observations', b3aCols[1], { shade: LBLUE }),
        dataCell('R3', b3aCols[2], { shade: LBLUE }), dataCell('"Logical closure", "mathematical hinges", institutional adoption, AI safety, Planck OD gap', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('U', b3aCols[0], { bold: true }), dataCell('DeepSeek Concrete Recommendations', b3aCols[1]),
        dataCell('R4', b3aCols[2]), dataCell('Scope protocol, detection metrics, gating audit, sufficiency theorem, simulation studies', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AP', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Key Structural Insights (Phase 3)', b3aCols[1], { shade: LBLUE }),
        dataCell('R8', b3aCols[2], { shade: LBLUE }), dataCell('Temporal Sieve IS d_r; persistent homology resolves scaling; M3 standalone', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('AQ', b3aCols[0], { bold: true }), dataCell('Cross-Reference to Collective Gaps', b3aCols[1]),
        dataCell('R8', b3aCols[2]), dataCell('Maps each Phase 3 component to review gaps it resolves', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AC', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Future Directions (5 Domains)', b3aCols[1], { shade: LBLUE }),
        dataCell('R6', b3aCols[2], { shade: LBLUE }), dataCell('Math foundations, topology, biology, neuroscience, ML/AI, governance', b3aCols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BG', b3aCols[0], { bold: true }), dataCell('Phase Change Recognition', b3aCols[1]),
        dataCell('R12', b3aCols[2]), dataCell('Detection of regime shifts, phase portrait bifurcations, transition metadata', b3aCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BT', b3aCols[0], { bold: true, shade: LBLUE }), dataCell('Immediate Action Sequencing', b3aCols[1], { shade: LBLUE }),
        dataCell('R12', b3aCols[2], { shade: LBLUE }), dataCell('Real-time decision hierarchy, priority ranking, fault-driven escalation', b3aCols[3], { shade: LBLUE }),
      ]}),
    ],
  }));

  // ── BRANCH 7: TETRAHEDRAL GEOMETRY & SCALING ───────────────────────
  children.push(H2('3.7 Branch VII: Tetrahedral Geometry & Scaling'));
  children.push(P('Categories from Reviews 10, 11, and 12 that establish the tetrahedral geometry framework and its scaling properties. These categories introduce consensus-based architectures for geometry validation, economic impact estimation, and recursive scaling through homology-driven aggregation. Three keystones anchor this branch: Simplicial Consensus Logic (BD), Recursive Tetrahedral Cascade (BE), and Scale-Invariant Degenerate State Observer (BF). Review 12 adds integration, intrinsic geometry, and risk assessment.'));

  const b7Cols = [900, 2700, 1200, 4560];
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: b7Cols,
    rows: [
      new TableRow({ children: [
        headerCell('Cat', b7Cols[0]), headerCell('Name', b7Cols[1]),
        headerCell('Review', b7Cols[2]), headerCell('Content & Scope', b7Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AX', b7Cols[0], { bold: true, shade: LBLUE }), dataCell('Tetrahedral Geometry Validation', b7Cols[1], { shade: LBLUE }),
        dataCell('R10', b7Cols[2], { shade: LBLUE }), dataCell('Math verified against Hatcher topology, all Q1\u2013Q6 resolved, simplicial validation', b7Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('AY', b7Cols[0], { bold: true }), dataCell('Ramsar as 4th Tetrahedral Face', b7Cols[1]),
        dataCell('R10', b7Cols[2]), dataCell('Homology sim H\u2080=1, H\u2081=3, H\u2082=1, face assignments, data collection specification', b7Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('AZ', b7Cols[0], { bold: true, shade: LBLUE }), dataCell('Croatia-Canada Sister Sites', b7Cols[1], { shade: LBLUE }),
        dataCell('R10', b7Cols[2], { shade: LBLUE }), dataCell('Crna Mlaka + Mer Bleue dual simulation, exchange protocol, validation framework', b7Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BA', b7Cols[0], { bold: true }), dataCell('Economic Impact Estimation', b7Cols[1]),
        dataCell('R10', b7Cols[2]), dataCell('Short-term $10\u201350M, medium $1\u20135B, long-term $100\u2013500B impact modeling', b7Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BB', b7Cols[0], { bold: true, shade: LBLUE }), dataCell('IUCN Red List Comparison', b7Cols[1], { shade: LBLUE }),
        dataCell('R10', b7Cols[2], { shade: LBLUE }), dataCell('HUF vs IUCN hybrid proposal, comparative analysis framework', b7Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BC', b7Cols[0], { bold: true }), dataCell('Tetrahedral Geometry Evaluation', b7Cols[1]),
        dataCell('R11', b7Cols[2]), dataCell('Endorsed geometry conjectures, flagged aggregation gap, homology mapping audit', b7Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BD', b7Cols[0], { bold: true, shade: GOLD }), dataCell('Simplicial Consensus Logic \u2605', b7Cols[1], { shade: GOLD }),
        dataCell('R11', b7Cols[2], { shade: GOLD }), dataCell('[KEYSTONE] 3-stage aggregator: project\u2192gate\u2192vote logic, consensus proof', b7Cols[3], { shade: GOLD }),
      ]}),
      new TableRow({ children: [
        dataCell('BE', b7Cols[0], { bold: true, shade: GOLD }), dataCell('Recursive Tetrahedral Cascade (RTC) \u2605', b7Cols[1], { shade: GOLD }),
        dataCell('R11', b7Cols[2], { shade: GOLD }), dataCell('[KEYSTONE] 3\u207f hierarchical architecture, Level 0\u20133 recursion, cascade termination', b7Cols[3], { shade: GOLD }),
      ]}),
      new TableRow({ children: [
        dataCell('BF', b7Cols[0], { bold: true, shade: GOLD }), dataCell('Scale-Invariant Degenerate State Observer \u2605', b7Cols[1], { shade: GOLD }),
        dataCell('R11', b7Cols[2], { shade: GOLD }), dataCell('[KEYSTONE] "4 regimes or 4 million, single simplex point", regime-invariant detection', b7Cols[3], { shade: GOLD }),
      ]}),
      new TableRow({ children: [
        dataCell('BK', b7Cols[0], { bold: true }), dataCell('Tetrahedral Architecture Integration', b7Cols[1]),
        dataCell('R12', b7Cols[2]), dataCell('Embedding tetrahedral geometry into operational pipelines, simplex-to-code mapping', b7Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('BO', b7Cols[0], { bold: true, shade: LBLUE }), dataCell('Scale as Intrinsic Geometry', b7Cols[1], { shade: LBLUE }),
        dataCell('R12', b7Cols[2], { shade: LBLUE }), dataCell('Scaling as geometric transformation, hierarchical refinement, dimension-invariant operations', b7Cols[3], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('BR', b7Cols[0], { bold: true, shade: CORAL }), dataCell('Scaling Overclaim Risk', b7Cols[1], { shade: CORAL }),
        dataCell('R12', b7Cols[2], { shade: CORAL }), dataCell('Boundary conditions for tetrahedral scaling, asymptotic failure modes, extrapolation limits', b7Cols[3], { shade: CORAL }),
      ]}),
      new TableRow({ children: [
        dataCell('BX', b7Cols[0], { bold: true }), dataCell('Scaling Caution Structure', b7Cols[1]),
        dataCell('R13', b7Cols[2]), dataCell('Scaling governance, caution framework, boundaries of applicability, architectural constraints', b7Cols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('CH', b7Cols[0], { bold: true, shade: GREEN }), dataCell('Ramsar Article 3.2 Alignment', b7Cols[1], { shade: GREEN }),
        dataCell('R14', b7Cols[2], { shade: GREEN }), dataCell('HUF alignment with Ramsar Article 3.2 wise use principles, governance protocols', b7Cols[3], { shade: GREEN }),
      ]}),
    ],
  }));
  children.push(P([
    { text: 'Keystones (R11/Gemini): ', bold: true },
    'Categories BD, BE, and BF together define the tetrahedral scaling architecture. BD provides the consensus mechanism (project\u2192gate\u2192vote), BE implements recursive aggregation through 3\u207f hierarchy, and BF guarantees scale-invariance through degenerate state observation. This triad unifies geometry with operational aggregation.'
  ]));

  // ── 4. CROSS-CUTTING THEMES ───────────────────────────────────────
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(H1('4. Cross-Cutting Themes'));
  children.push(P('Several themes emerge that cut across all six branches, binding the category tree into a coherent whole.'));

  children.push(H2('4.1 The Sufficiency Hinge'));
  children.push(P([
    'The most referenced single concern across all reviews is the sufficiency claim. Categories ',
    { text: 'D, S, X, AS, N, P', bold: true },
    ' all converge on one sentence that the collective demands appear in the next version of the Sufficiency Frontier:'
  ]));
  children.push(P('\u03C1 is a sufficient statistic for governance inference if and only if the governance objective is a function of the allocation vector alone. When the inference requires absolute magnitudes, temporal microstructure, or element-internal state, \u03C1 is not sufficient and additional statistics are required.', { italics: true, indent: 720 }));
  children.push(P('This statement, with four formal counterexamples (C1\u2013C4), is the mathematical anchor for the entire framework.'));

  children.push(H2('4.2 The Evidentiary Taxonomy'));
  children.push(P([
    'Categories ',
    { text: 'C, AW, AI', bold: true },
    ' define the five-tier labeling system that every document must adopt. The taxonomy resolves the central tension across reviews: ChatGPT wanted labels, Grok wanted tests, Gemini wanted hinge identification, DeepSeek wanted scope conditions. The five tiers\u2014[THEOREM], [EMPIRICAL], [IDENTITY], [CONJECTURE], [PEDAGOGICAL]\u2014do all four simultaneously.'
  ]));

  children.push(H2('4.3 The ML Bridge Validation'));
  children.push(P([
    'Categories ',
    { text: 'K, M, AF, AG, AA, AB, AV', bold: true },
    ' collectively validate the HUF-to-ML mapping across 10+ architectures, 6 conjectures, and 4 experimental regimes. The consensus: Softmax = Unity is [IDENTITY] (mathematical fact). The full operational mapping (overfitting = Deceptive Drift, regularization = MC-4, etc.) is [CONJECTURE]\u2014structurally compelling, testable, not yet theorem-level.'
  ]));

  children.push(H2('4.4 The Spectral Frontier'));
  children.push(P([
    'Categories ',
    { text: 'AD, AE, Y, AJ, AT, AM', bold: true },
    ' define HUF\u2019s extension into topological data analysis. The Temporal Sieve (dHUF/dt as Ratio Velocity) is the most significant new concept to emerge from the review process. The consensus strategy: start with persistence diagrams, promote to full spectral sequence formalism only if the page-by-page algebra adds clear value beyond what TDA alone provides.'
  ]));

  children.push(H2('4.5 The Detection Gap'));
  children.push(P([
    'Categories ',
    { text: 'T, S, AK, AU', bold: true },
    ' identify the single largest gap for peer review readiness: detection performance metrics. The framework lacks false discovery rates, power analyses, ROC curves, and confusion matrices for MDG/Pettitt/ITS across the corpus. DeepSeek elevated this to Critical priority. The HUF Ping Hell Test (5-level stress test, 156,100 simulated pings) provides initial M3 milestone data: 5/11 structural failures detected, 6 subtle/gradual events missed\u2014establishing the detection sensitivity boundary.'
  ]));

  children.push(H2('4.6 The Tetrahedral Scaling Architecture'));
  children.push(P([
    'Categories ',
    { text: 'AX, AY, AZ, BA, BB, BC, BD, BE, BF', bold: true },
    ' from Reviews 10\u201311 introduce a unified scaling framework grounded in tetrahedral geometry. The Recursive Tetrahedral Cascade (BE) enables hierarchical aggregation across 3\u207f levels without loss of homological structure. The Scale-Invariant Degenerate State Observer (BF) guarantees that detection operates identically whether observing 4 regimes or 4 million instances\u2014a single simplex point. The Simplicial Consensus Logic (BD) bridges these through a three-stage aggregator (project\u2192gate\u2192vote) that preserves consensus proof at every level. Together, they extend HUF from a detection framework into a universal architecture for consensus-driven governance across arbitrary scales.'
  ]));

  // ── 5. CATEGORY-TO-MILESTONE MAP ──────────────────────────────────
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(H1('5. Category-to-Milestone Map'));
  children.push(P('Each Phase 3 milestone draws on specific review categories. This map shows which categories feed each milestone, enabling targeted work.'));

  const mCols = [1200, 1800, 6360];
  children.push(new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: mCols,
    rows: [
      new TableRow({ children: [
        headerCell('Milestone', mCols[0]), headerCell('Tier', mCols[1]), headerCell('Contributing Categories', mCols[2]),
      ]}),
      new TableRow({ children: [
        dataCell('M1', mCols[0], { bold: true, shade: LBLUE }), dataCell('[THEOREM]', mCols[1], { shade: LBLUE }),
        dataCell('D (SF specific), X (theorem formalization), AS (sharpening + C3/C4), S (scope gaps), N (hinge identification), U4 (formal recommendation)', mCols[2], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('M2', mCols[0], { bold: true }), dataCell('[CONJECTURE]', mCols[1]),
        dataCell('Y (spectral engine spec), AD (spectral validation), AE (TDA simulation), AJ (formalization), AT (strategy), AM (Temporal Sieve), AN (requirements), AP1 (Sieve = d_r)', mCols[2]),
      ]}),
      new TableRow({ children: [
        dataCell('M3', mCols[0], { bold: true, shade: LBLUE }), dataCell('[MODEL]', mCols[1], { shade: LBLUE }),
        dataCell('T (reproducibility), S3 (Q-model), AK3 (FDR), AQ4 (gap resolution), Hell Test results (5/11 detected)', mCols[2], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('M3b', mCols[0], { bold: true }), dataCell('[MODEL]', mCols[1]),
        dataCell('Z (UDI spec), AU (cautions), AC9 (governance direction)', mCols[2]),
      ]}),
      new TableRow({ children: [
        dataCell('M4', mCols[0], { bold: true, shade: LBLUE }), dataCell('[EXPERIMENT]', mCols[1], { shade: LBLUE }),
        dataCell('K (conjecture validation), M (sim results), AA (experiment spec), AB (hypotheses), AV (design improvements), AF (architecture sweep), AG (insights), L5 (CNN/MNIST)', mCols[2], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('Tetrahedral Scale', mCols[0], { bold: true, shade: GOLD }), dataCell('[ARCHITECTURE]', mCols[1], { shade: GOLD }),
        dataCell('AX (geometry validation), AY (Ramsar face), AZ (sister sites), BA (economics), BB (IUCN), BC (evaluation), BD (consensus logic), BE (RTC), BF (scale observer)', mCols[2], { shade: GOLD }),
      ]}),
    ],
  }));

  // ── 6. VISUAL TREE (TEXT) ─────────────────────────────────────────
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(H1('6. Visual Tree Representation'));
  children.push(P('The following text-based tree provides a compact navigational view of all 49 categories organized by branch. Gold highlighting indicates keystone categories that anchor the branch.'));

  const treeLine = (text, opts = {}) => new Paragraph({
    spacing: { after: 20 },
    children: [new TextRun({ text, font: 'Consolas', size: 19, color: opts.color || DARK, bold: opts.bold || false })],
  });

  children.push(treeLine('HUF REVIEW CORPUS', { bold: true, color: BLUE }));
  children.push(treeLine('\u2502'));
  children.push(treeLine('\u251C\u2500\u2500 I. INFRASTRUCTURE & GOVERNANCE'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [A] Repo Structure .................. R1/ChatGPT'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [B] Data Management ................. R1/ChatGPT'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [C] Evidentiary Hierarchy \u2605 ......... R1/ChatGPT  [KEYSTONE]'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [H] Content Advisories .............. R1/ChatGPT'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [T] Reproducibility ................. R4/DeepSeek'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [V] Operational Risk Solution ........ R4/DeepSeek'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [AW] Trace & Repo Management ........ R9/ChatGPT'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [BH] Four-Layer Architecture ......... R12/ChatGPT'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [BM] Review Process Infrastructure ... R12/ChatGPT'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [BP] Status Discipline Risk ......... R12/ChatGPT'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [BS] Release Discipline Risk ........ R12/ChatGPT'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [BU] Program-Level Synthesis ........ R13/ChatGPT'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [BV] Review Memory Reorganization ... R13/ChatGPT'));
  children.push(treeLine('\u2502   \u2514\u2500\u2500 [BZ] Risk as First-Class Category ... R13/ChatGPT'));
  children.push(treeLine('\u2502'));
  children.push(treeLine('\u251C\u2500\u2500 II. PILLAR-SPECIFIC FEEDBACK'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [D] Sufficiency Frontier ............ R1/ChatGPT  \u2192 SF v3.7'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [E] Fourth Category ................. R1/ChatGPT  \u2192 FC v2.7'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [F] Triad Synthesis ................. R1/ChatGPT  \u2192 Triad v1.7'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [G] Trace ........................... R1/ChatGPT  \u2192 Trace v5.7'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [X] Sufficiency Theorem \u2605 .......... R6/Copilot   [KEYSTONE]'));
  children.push(treeLine('\u2502   \u2514\u2500\u2500 [AS] Theorem Sharpening \u2605 .......... R9/ChatGPT   [KEYSTONE]'));
  children.push(treeLine('\u2502'));
  children.push(treeLine('\u251C\u2500\u2500 III. VALIDATION & VERIFICATION'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 Verdicts: [I] [J] [N] [O] [R] [AI] . R2/R3/R4/R8'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 Risks:   [P] [S] [AK] .............. R3/R4/R8'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 ML:      [K] [M] [AF] [AG] ......... R2/R7'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 Math:    [BI] [BJ] ................. R12/ChatGPT'));
  children.push(treeLine('\u2502   \u2514\u2500\u2500 Validation: [BL] [BQ] [BN] ........ R12/ChatGPT'));
  children.push(treeLine('\u2502'));
  children.push(treeLine('\u251C\u2500\u2500 IV. EXTENSIONS & NEW DOMAINS'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 Spectral: [AD] [AE] [Y] [AJ] [AT] . R6/R7/R8/R9'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [AM] Temporal Sieve \u2605 .............. R8/Gemini    [KEYSTONE]'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [AL] Optical Instrumentation ........ R8/Gemini'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [AH] Network Packet Demo ........... R7/Grok'));
  children.push(treeLine('\u2502   \u2514\u2500\u2500 [BW] Kinetic Governance Reframing ... R13/ChatGPT'));
  children.push(treeLine('\u2502'));
  children.push(treeLine('\u251C\u2500\u2500 V. PHASE 3 RESEARCH DESIGN'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 Roadmap: [W] [AO] [AR] ............. R6/R8/R9'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 Specs:   [Z] [AA] [AB] [AV] [AN] ... R6/R8/R9'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 Cautions: [AU] ..................... R9/ChatGPT'));
  children.push(treeLine('\u2502   \u2514\u2500\u2500 [BY] Milestone Governance Sharpening R13/ChatGPT'));
  children.push(treeLine('\u2502'));
  children.push(treeLine('\u251C\u2500\u2500 VI. SYNTHESIS & RECOMMENDATIONS'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [L] Grok Suggestions ............... R2/Grok'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [Q] Gemini Observations ............ R3/Gemini'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [U] DeepSeek Recommendations ....... R4/DeepSeek'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [AP] Structural Insights ........... R8/Gemini'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [AQ] Cross-Reference Map ........... R8/Gemini'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [AC] Future Directions ............. R6/Copilot'));
  children.push(treeLine('\u2502   \u251C\u2500\u2500 [BG] Phase Change Recognition ....... R12/ChatGPT'));
  children.push(treeLine('\u2502   \u2514\u2500\u2500 [BT] Immediate Action Sequencing ... R12/ChatGPT'));
  children.push(treeLine('\u2502'));
  children.push(treeLine('\u2514\u2500\u2500 VII. TETRAHEDRAL GEOMETRY & SCALING'));
  children.push(treeLine('    \u251C\u2500\u2500 [AX] Geometry Validation ........... R10/Grok'));
  children.push(treeLine('    \u251C\u2500\u2500 [AY] Ramsar 4th Face .............. R10/Grok'));
  children.push(treeLine('    \u251C\u2500\u2500 [AZ] Sister Sites .................. R10/Grok'));
  children.push(treeLine('    \u251C\u2500\u2500 [BA] Economic Impact ............... R10/Grok'));
  children.push(treeLine('    \u251C\u2500\u2500 [BB] IUCN Comparison ............... R10/Grok'));
  children.push(treeLine('    \u251C\u2500\u2500 [BC] Geometry Evaluation ............ R11/Gemini'));
  children.push(treeLine('    \u251C\u2500\u2500 [BD] Simplicial Consensus \u2605 ........ R11/Gemini  [KEYSTONE]'));
  children.push(treeLine('    \u251C\u2500\u2500 [BE] Recursive Cascade (RTC) \u2605 ...... R11/Gemini  [KEYSTONE]'));
  children.push(treeLine('    \u251C\u2500\u2500 [BF] Scale-Invariant Observer \u2605 ..... R11/Gemini  [KEYSTONE]'));
  children.push(treeLine('    \u251C\u2500\u2500 [BK] Tetrahedral Integration ....... R12/ChatGPT'));
  children.push(treeLine('    \u251C\u2500\u2500 [BO] Scale as Intrinsic Geometry ... R12/ChatGPT'));
  children.push(treeLine('    \u251C\u2500\u2500 [BR] Scaling Overclaim Risk ........ R12/ChatGPT'));
  children.push(treeLine('    \u2514\u2500\u2500 [BX] Scaling Caution Structure ..... R13/ChatGPT'));

  // ── 7. CONCLUSION ─────────────────────────────────────────────────
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(H1('7. Conclusion'));
  children.push(P('The 85-category structure reveals that the HUF collective review process has generated a corpus that is itself a structured knowledge base\u2014not merely a collection of feedback. The seven-branch tree shows clear separation of concerns between infrastructure (Branch I), pillar refinement (Branch II), independent validation (Branch III), frontier extensions (Branch IV), research design (Branch V), cross-review synthesis (Branch VI), and tetrahedral scaling architecture (Branch VII). Reviews 12\u201314 (ChatGPT and Grok) added 28 new categories spanning governance architecture, mathematical maturation, empirical validation boundaries, detection performance metrics, topological algebra, and Ramsar applications.'));
  children.push(P('Six keystone categories anchor the entire tree:'));
  children.push(bullet([
    { text: 'Category C (Evidentiary Hierarchy): ', bold: true },
    'The single highest-priority item across all 13 reviews. Defines the 5-tier taxonomy that every document must adopt.'
  ]));
  children.push(bullet([
    { text: 'Categories X + AS (Sufficiency Theorem): ', bold: true },
    'The mathematical anchor. Four counterexamples (C1\u2013C4) define the exact boundary of what HUF can and cannot claim.'
  ]));
  children.push(bullet([
    { text: 'Category AM (Temporal Sieve): ', bold: true },
    'The most significant new concept to emerge from reviews 1\u20139. dHUF/dt as Ratio Velocity operationalizes HUF\u2019s unique detection capability.'
  ]));
  children.push(bullet([
    { text: 'Categories BD, BE, BF (Tetrahedral Scaling): ', bold: true },
    'The architectural keystones from reviews 10\u201311. BD (Simplicial Consensus Logic) provides three-stage aggregation, BE (Recursive Tetrahedral Cascade) enables 3\u207f hierarchical recursion, and BF (Scale-Invariant Observer) guarantees regime-invariant detection from 4 to 4 million instances.'
  ]));
  children.push(P('The tree also reveals what the review process did not generate: no category questions whether the core mathematics (\u03A3\u03C1\u1D62 = 1 on the simplex) is sound. All 13 reviews confirm internal consistency, mathematical validity, and absence of pseudoscience. The remaining work is labeling, scope, and detection performance\u2014not foundations.'));
  children.push(P('This document is designed to be appended to the Collective Trace as a navigational appendix, enabling any new reader or reviewer to locate any review item by category, branch, reviewer, or Phase 3 milestone.'));

  return children;
}

// ══════════════════════════════════════════════════════════════════════
// BUILD DOCUMENT
// ══════════════════════════════════════════════════════════════════════

const doc = new Document({
  styles,
  numbering,
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
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: 'HUF Category Class Structure Tree  \u00B7  March 2026',
            font: 'Times New Roman', size: 18, color: '999999', italics: true })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: 'Page ', font: 'Times New Roman', size: 18, color: '999999' }),
            new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 18, color: '999999' }),
          ],
        })],
      }),
    },
    children: buildContent(),
  }],
});

const outPath = process.argv[2] || 'HUF_Category_Class_Structure_Tree_v1.4.docx';
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outPath, buf);
  console.log(`\u2705 Built: ${outPath} (${(buf.length / 1024).toFixed(1)} KB)`);
});
