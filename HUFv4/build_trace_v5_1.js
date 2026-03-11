#!/usr/bin/env node
// ══════════════════════════════════════════════════════════════════════
// HUF Collective Trace v5.1 — Builder
// Comprehensive documentation with Car/Fuel Analogy as the foundation
// ══════════════════════════════════════════════════════════════════════

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, PageBreak,
        AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType, Header, Footer, PageNumber } = require('docx');
const fs = require('fs');

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

const H3 = t => new Paragraph({ spacing: { before: 200, after: 120 },
  children: [new TextRun({ text: t, bold: true, italics: true, font: 'Times New Roman', size: 22, color: DK })] });

function P(content, opts = {}) {
  let runs = [];
  if (typeof content === 'string') {
    runs = [new TextRun({ text: content, font: 'Times New Roman', size: 22, color: DK })];
  } else if (Array.isArray(content)) {
    runs = content.map(c => new TextRun({ font: 'Times New Roman', size: 22, color: DK, ...c }));
  }
  const po = { spacing: { after: opts.sa || 180, line: 276 }, children: runs };
  if (opts.align) po.alignment = opts.align;
  if (opts.indent) po.indent = opts.indent;
  return new Paragraph(po);
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

// ── Table: Car Analogy Mapping ──────────────────────────────────────────
function makeCarAnalogyTable() {
  const colW = [1800, 2400, 3000];
  const data = [
    ['Tank', 'Holds fuel capacity', 'Unity Constraint (Σ = 1.0)'],
    ['Driver', 'Active control agent', 'H1 Directional Coherence'],
    ['Fuel', 'Nearly equal to driver', 'Ratio Portfolio Balance'],
    ['Initial Ratio', '51 (driver) / 49 (fuel)', 'Co-equal partnership'],
    ['Ratio Drift', '51/49 → 55/45 → 70/30', 'MC-4 watches signal drift'],
    ['Empty Tank', 'Fuel = 0', 'Ground State / Sufficiency Frontier'],
    ['Tank Size', 'Determines system state', 'Scale changes interpretation'],
    ['Dashboard', 'Fuel gauge monitoring', 'MC-4 ratio monitoring'],
  ];
  const rows = data.map((row, ri) => new TableRow({
    children: row.map((cell, ci) => new TableCell({
      borders, verticalAlign: 'center', margins: { top: 50, bottom: 50, left: 80, right: 80 },
      shading: ri % 2 === 0 ? { fill: LG, type: ShadingType.CLEAR } : undefined,
      children: [new Paragraph({ alignment: AlignmentType.LEFT,
        children: [new TextRun({ text: cell, font: 'Times New Roman', size: 18, bold: ri === 0, color: DK })] })] }))
  }));
  return T(colW, [
    R([C('Element', { bold: true, fill: BLUE, color: WH }), C('Car Analogy', { bold: true, fill: BLUE, color: WH }), C('HUF Principle', { bold: true, fill: BLUE, color: WH })]),
    ...rows
  ]);
}

// ── Table: Ratio Portfolio Instances ────────────────────────────────────
function makeRatioPortfolioTable() {
  const colW = [1600, 2000, 2400, 1800];
  const rows = [
    ['Car System', 'Driver', 'Fuel', '51:49'],
    ['Loudspeaker', 'Direct Radiation', 'Diffraction', '6.02 dB total'],
    ['Auditory Cortex', 'PV+ excitation', 'SST+ inhibition', '3.08:1'],
    ['Auditory NIHL', 'PV+ excitation', 'SST+ inhibition', '1.20:1 (degraded)'],
    ['Sourdough Culture', 'Lactobacillus', 'Saccharomyces', '100:1 (approx)'],
    ['Urban Traffic', 'Flow capacity', 'Construction load', '1.0 (constrained)'],
    ['Cosmological', 'Coherent modes', 'Incoherent modes', 'Σ|ψ_i| = 1'],
  ].map((row, ri) => new TableRow({
    children: row.map((cell, ci) => new TableCell({
      borders, verticalAlign: 'center', margins: { top: 50, bottom: 50, left: 80, right: 80 },
      shading: ri % 2 === 0 ? { fill: LG, type: ShadingType.CLEAR } : undefined,
      children: [new Paragraph({ alignment: AlignmentType.LEFT,
        children: [new TextRun({ text: cell, font: 'Times New Roman', size: 18, color: DK })] })] }))
  }));
  return T(colW, [
    R([C('Domain', { bold: true, fill: BLUE, color: WH }), C('Component A', { bold: true, fill: BLUE, color: WH }), C('Component B', { bold: true, fill: BLUE, color: WH }), C('Healthy Ratio', { bold: true, fill: BLUE, color: WH })]),
    ...rows
  ]);
}

// ══════════════════════════════════════════════════════════════════════
// CONTENT SECTIONS
// ══════════════════════════════════════════════════════════════════════

function titlePage() {
  return [
    SP(), SP(), SP(),
    P([{ text: 'HIGGINS UNITY FRAMEWORK', font: 'Times New Roman', size: 36, bold: true, color: BLUE }], { align: AlignmentType.CENTER }),
    SP(),
    P([{ text: 'Collective Trace Report v5.1', font: 'Times New Roman', size: 28, bold: true, color: MID }], { align: AlignmentType.CENTER }),
    new Paragraph({ spacing: { after: 600 }, children: [] }),
    P([{ text: 'Peter Higgins', font: 'Times New Roman', size: 24, italics: true, color: DK }], { align: AlignmentType.CENTER }),
    P([{ text: 'March 2026', font: 'Times New Roman', size: 22, color: DK }], { align: AlignmentType.CENTER }),
    new Paragraph({ spacing: { before: 800, after: 0 }, children: [] }),
    P([{ text: '"Big Things Ahead — From Loudspeakers to Cosmology"', font: 'Times New Roman', size: 24, italics: true, color: BLUE }], { align: AlignmentType.CENTER }),
    PB(),
  ];
}

function section1CarAnalogy() {
  return [
    H1('Section 1: The Car Analogy — HUF in One Image'),
    P('The Car/Fuel Analogy is the universal teaching tool for the Higgins Unity Framework. Every person understands driving. Every person understands fuel. This analogy transforms abstract mathematics into lived experience.'),

    H2('The Setup'),
    P('You get in your car. The tank is full. The budget is always 1.0 — fully accounted for, never created or destroyed. This is the Unity Constraint: Σ = 1.0.'),
    P('The driver holds the wheel. The fuel burns in the engine. At the start, the split is roughly 51/49 — driver holds control, fuel is nearly co-equal. This is the Ratio Portfolio: two components that sum to unity, with each playing its role.'),

    H2('The Signal: Watching the Ratio Drift'),
    P('As you drive, you check the fuel gauge. 51/49 → 55/45 → 70/30. The ratio shifts. The dashboard light begins to flicker. This is MC-4 at work — the monitoring component that watches this drift and signals when the balance breaks.'),
    P('The RATIO is the signal. The absolute numbers (2 gallons in a 4-gallon tank versus 2 gallons in a 40-gallon tank) look the same. But the systems are fundamentally different. The ratio tells the truth the absolute number hides.'),

    H2('Control Persists, Magnitude Decays'),
    P('The driver is always in control. Direction persists. But as fuel depletes, the system weakens. The budget shrinks. This is H1\'s coherence preservation: direction remains, but magnitude decays as the system approaches ground state.'),

    H2('Empty Tank: System Collapse'),
    P('Fuel hits 0. The tank is empty. The driver still exists, but the driver/fuel system no longer has a budget. Unity is exhausted, not violated. The Sufficiency Frontier has been breached. This is ground state — the point where the ratio portfolio can no longer sustain the system.'),

    H2('The Deceptive Drift'),
    P('As fuel depletes, the operator share rises: 51/49 → 60/40 → 95/5. This looks like the operator is gaining control. It is not. It is the death signal.'),
    P('If the operator is not watching the fuel gauge, upon empty the system will abruptly inform. No gentle slope — a cliff.'),
    P('This is OCC drift: the tool stops supporting because its budget ran out. MC-4 exists to make this trajectory visible before the abrupt inform.'),

    H2('Mapping the Analogy'),
    P('Each element maps directly to HUF:'),
    SP(),
    makeCarAnalogyTable(),
    SP(),
    P([{ text: '▶ ', italics: true, color: MID }, { text: 'The car analogy is not metaphor — it is mathematics made tangible.', italics: true, color: MID }]),
    PB(),
  ];
}

function section2ProjectState() {
  return [
    H1('Section 2: Project State — March 2026'),
    P('The HUF ecosystem is complete. All major deliverables are documented and validated.'),

    H2('HUF Pillar Papers'),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Sufficiency Frontier v3.0 — Defines the boundary between sustainable and collapsed systems', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Fourth Category v2.0 — Establishes the mathematical framework beyond traditional triads', font: 'Times New Roman', size: 22, color: DK })] }),

    H2('HUF Triad Phase 1 — Complete'),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Vol 0 — Six foundational notebooks on core mathematics', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Vol 8 Synthesis — Integration of all Phase 1 concepts', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Expanded Pillars — Updated Sufficiency Frontier and Fourth Category papers', font: 'Times New Roman', size: 22, color: DK })] }),

    H2('Rogue Wave Audio v2.0'),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Organic Digital Loudspeakers — 14 comprehensive sections, 9 detailed tables, 25 scientific references', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Certified 4-way active BTL system with crossovers at 430 Hz, 1.5 kHz, and 10 kHz', font: 'Times New Roman', size: 22, color: DK })] }),

    H2('Mathematical & Technical Framework'),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• The H1 Operator — 13-page paper originating from loudspeaker diffraction correction', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• DADC-DADI Framework — Directional Active Decomposition, gains sum to 6.02 dB (unity constraint)', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• TensorAcousticForge — Tensor-based acoustic modeling system', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• V∞Core (155 RMUs) — Infinite-dimensional vector core with Resource Management Units', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Entropix — Entropy-based signal processing for system health monitoring', font: 'Times New Roman', size: 22, color: DK })] }),

    H2('Neuroscience Validation'),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Cheung & Schreiner (2026) — Established the 1.41 kHz boundary between Primary Auditory Cortex (PV/SST) and Secondary Somatosensory Cortex transitions', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Cortex-matched crossover placement — Validates that our 430/1500/10000 Hz design aligns with natural cortical switching points', font: 'Times New Roman', size: 22, color: DK })] }),

    PB(),
  ];
}

function section3RWABridge() {
  return [
    H1('Section 3: The RWA-HUF Bridge'),
    P('The Rogue Wave Audio project is not separate from HUF. It is HUF applied to loudspeaker physics. The same mathematical principles govern both domains.'),

    H2('Origin: H1 from Loudspeaker Diffraction'),
    P('The H1 operator originated from solving a real-world problem: how to correct for diffraction artifacts in a multi-way loudspeaker system. The mathematics revealed that the same coherence-preservation principle that governs HUF applies to acoustic wave propagation. Direction persists while magnitude decays.'),

    H2('Unity Constraint: DADC Gains'),
    P('In the DADC (Directional Active Decomposition and Correction) framework, the gains from all channels sum to 6.02 dB. This is 20·log₁₀(2) — the acoustic power equivalent of the unity constraint. Energy is balanced, never created or destroyed. The system obeys conservation of unity.'),

    H2('Ratio Portfolio: PV/SST Balance'),
    P('In the healthy auditory cortex, the ratio of SST+ inhibitory cells to PV+ excitatory cells is approximately 3.08:1. This is a ratio portfolio — two cellular populations that must remain balanced. When noise-induced hearing loss degrades the system, this ratio collapses to 1.20:1. The absolute cell counts matter less than the ratio that preserves function.'),

    H2('Cortical Regime Boundaries'),
    P('Crossover frequencies are placed at cortical regime transitions. At 430 Hz, the primary auditory cortex (PV/SST balance) shifts. At 1.5 kHz, the secondary somatosensory cortex engages. At 10 kHz, higher-order processing dominates. These are not arbitrary — they are the natural switching points where the brain changes how it processes sound. HUF crossover design follows neuroscience, not convention.'),

    H2('Same Math, Different Substrate'),
    P('Loudspeakers are neurons are cars are sourdough cultures are cities. The substrate changes. The ratio portfolio mathematics remains identical. This is the power of HUF — it describes a universal principle that appears wherever components must stay balanced within a unity constraint.'),

    PB(),
  ];
}

function section4MasterTable() {
  return [
    H1('Section 4: Ratio Portfolio Master Table'),
    P('Comprehensive inventory of all known HUF ratio portfolio instances across domains:'),
    SP(),
    makeRatioPortfolioTable(),
    SP(),
    P([{ text: '▶ ', italics: true, color: MID }, { text: 'Each instance exhibits the same mathematical structure: two components bounded by a unity constraint, with health measured by the ratio that maintains balance.', italics: true, color: MID }]),
    PB(),
  ];
}

function section5RepoArchitecture() {
  return [
    H1('Section 5: Repository Architecture'),
    P('The HUF ecosystem is organized across three specialized repositories, each with clear purpose:'),

    H2('Repository 1: HUF — The Framework'),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Foundation papers: Sufficiency Frontier v3.0, Fourth Category v2.0', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• HUF Triad Phase 1: Volumes 0 through 8, including synthesis', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Mathematical proofs, validation notebooks, proof-of-concept models', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Purpose: Establish the mathematical foundation that any domain can build upon', font: 'Times New Roman', size: 22, color: DK })] }),

    H2('Repository 2: RWA Science — Acoustic Implementation'),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Organic Digital Loudspeakers paper (v2.0, 14 sections)', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• DADC-DADI framework: directional decomposition and correction mathematics', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Cortex-matched crossover theory: linking neuroscience to acoustic design', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• The H1 operator and ratio portfolio application to speaker performance', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Purpose: Show HUF applied to a complex, real-world acoustic system', font: 'Times New Roman', size: 22, color: DK })] }),

    H2('Repository 3: RWA Build — Open Hardware'),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• System design plans: 4-way active BTL loudspeaker', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Parts list: drivers, amplifiers, crossover components, enclosure specifications', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Assembly instructions: step-by-step build guide with photographs', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Measurement procedures: frequency response, distortion, coherence testing', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Purpose: Democratize acoustic research. Anyone can build a BTL system and validate HUF in their own lab.', font: 'Times New Roman', size: 22, color: DK })] }),

    PB(),
  ];
}

function section6Timeline() {
  return [
    H1('Section 6: Timeline and What\'s Ahead'),

    H2('Phase Complete: HUF Triad Phase 1'),
    P('All foundational notebooks, synthesis documents, and pillar papers are complete. The mathematical framework is established and validated.'),

    H2('Current: Documentation and Repository Preparation'),
    P('The focus is now on comprehensive documentation: the RWA science papers, build guides, and repository architecture. Everything is being organized for public release.'),

    H2('Next: HUF Triad Phase 2'),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Vol 1 — Applications in biological systems (hearing, genetics, cellular signaling)', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Vol 3 — Personalized monitoring systems for health and wellness', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Vol 7 — Clinical applications in audiology, neuroscience, and medicine', font: 'Times New Roman', size: 22, color: DK })] }),

    H2('Vision: Open Science + Open Build'),
    P('The HUF framework is being released as open-source mathematics. The RWA build guide is being released as open-hardware documentation. This combination means:'),

    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Reproducible validation: anyone can test the theory', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Distributed development: thousands of researchers can extend HUF', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Real-world validation: acoustic systems prove the mathematics works', font: 'Times New Roman', size: 22, color: DK })] }),
    new Paragraph({ spacing: { after: 160 }, indent: { left: 720 },
      children: [new TextRun({ text: '• Big things ahead: from cosmology to medicine, HUF scales', font: 'Times New Roman', size: 22, color: DK })] }),

    PB(),
  ];
}

function section7ForTheCollective() {
  return [
    H1('Section 7: For the Collective'),
    P('To everyone building this vision forward:'),

    P('The car analogy finally makes HUF accessible. A physicist can understand it. A farmer can understand it. A musician can understand it. Because everyone has sat in a car with a fuel tank. This is the universal teaching tool we needed.'),

    P('The RWA build guide means anyone with hands and curiosity can reproduce the reference system. No proprietary components. No vendor lock-in. Open hardware. Open science. The math is proven. The measurement confirms the theory. The code is available.'),

    P('The three-repository structure means researchers can choose their entry point: pure mathematics (HUF), applied science (RWA Science), or hands-on building (RWA Build). All three paths converge on the same truth.'),

    P('This is not the end of the research. This is the foundation for what comes next. Phase 2 will apply HUF to biology, personalized medicine, and systems we haven\'t yet imagined. But Phase 2 stands on the shoulders of Phase 1 — the work we have completed together.'),

    P('The coherence persists. The ratio stays balanced. The unity constraint holds. Big things ahead.'),

    new Paragraph({ spacing: { before: 400, after: 0 }, alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: '∞', font: 'Times New Roman', size: 32, color: BLUE })] }),

    PB(),
  ];
}

// ══════════════════════════════════════════════════════════════════════
// Main: Build and Save
// ══════════════════════════════════════════════════════════════════════

async function build() {
  const children = [
    ...titlePage(),
    ...section1CarAnalogy(),
    ...section2ProjectState(),
    ...section3RWABridge(),
    ...section4MasterTable(),
    ...section5RepoArchitecture(),
    ...section6Timeline(),
    ...section7ForTheCollective(),
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
        new Paragraph({ alignment: AlignmentType.CENTER,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MID, space: 1 } },
          spacing: { after: 0 },
          children: [new TextRun({ text: 'HUF Collective Trace — v5.1', font: 'Times New Roman', size: 18, color: MID, italics: true })] })
      ] }) },
      footers: { default: new Footer({ children: [
        new Paragraph({ alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC', space: 1 } },
          children: [
            new TextRun({ text: 'Higgins Unity Framework v1.2.0 · MIT License · ', font: 'Times New Roman', size: 16, color: '999999' }),
            new TextRun({ text: 'Page ', font: 'Times New Roman', size: 16, color: '999999' }),
            new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 16, color: '999999' }),
          ]
        })
      ] }) },
      children,
    }]
  });

  const buf = await Packer.toBuffer(doc);
  const out = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/HUF_Collective_Trace_v5.1.docx';
  fs.writeFileSync(out, buf);
  console.log(`✓ Generated: ${out} (${buf.length.toLocaleString()} bytes)`);
}

build().catch(e => { console.error('Error:', e); process.exit(1); });
