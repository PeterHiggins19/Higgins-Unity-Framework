// ══════════════════════════════════════════════════════════════════════
// HUF Triad Phase 1 — Volume 8: Synthesis v1.6 (Dual-Column)
// Peter Higgins · March 2026
// ══════════════════════════════════════════════════════════════════════

const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition,
        LevelFormat, ExternalHyperlink } = require("docx");

const { createDualHelpers } = require("../shared/dual_column");

// ── Page setup ──────────────────────────────────────────────────────
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;
const CW = PAGE_W - 2 * MARGIN;

const BLUE = "1F3864", MID = "2E75B6", DARK = "333333";
const LGREY = "F2F2F2", LBLUE = "D6E4F0", WHITE = "FFFFFF";
const GREEN = "E2EFDA", GOLD = "FFF2CC";

const bdr = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };

// ── Dual-column helpers ─────────────────────────────────────────────
const dc = createDualHelpers({ palette: "huf" });

// ── Legacy helpers (for tables, non-dual sections) ──────────────────
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: t, bold: true, font: "Times New Roman", size: 28, color: BLUE })] });

const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: t, bold: true, font: "Times New Roman", size: 24, color: BLUE })] });

const H3 = (t) => new Paragraph({ spacing: { before: 200, after: 120 },
  children: [new TextRun({ text: t, bold: true, italics: true, font: "Times New Roman", size: 22, color: DARK })] });

function P(content, opts = {}) {
  const { align, indent, spacing_after, bold, italics, color: col } = opts;
  const runs = [];
  if (typeof content === "string") {
    runs.push(new TextRun({ text: content, font: "Times New Roman", size: 22, color: col || DARK,
      bold: bold || false, italics: italics || false }));
  } else if (Array.isArray(content)) {
    content.forEach(c => {
      if (typeof c === "string") runs.push(new TextRun({ text: c, font: "Times New Roman", size: 22, color: col || DARK }));
      else runs.push(new TextRun({ font: "Times New Roman", size: 22, color: DARK, ...c }));
    });
  }
  return new Paragraph({ spacing: { after: spacing_after || 160 }, alignment: align || AlignmentType.JUSTIFIED,
    indent: indent ? { left: indent } : undefined, children: runs });
}

function crossRef(text) {
  return new Paragraph({ spacing: { before: 80, after: 160 },
    children: [new TextRun({ text: "▶ " + text, font: "Times New Roman", size: 20, italics: true, color: MID })] });
}

function headerCell(text, width) {
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: BLUE, type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, font: "Times New Roman", size: 20, bold: true, color: WHITE })] })] });
}

function dataCell(text, width, opts = {}) {
  const { shade, align, bold: b } = opts;
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    children: [new Paragraph({ alignment: align || AlignmentType.LEFT,
      children: [new TextRun({ text: String(text), font: "Times New Roman", size: 20, color: DARK, bold: b || false })] })] });
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
    children: [new TextRun({ text: "THE HUF TRIAD", font: "Times New Roman", size: 44, bold: true, color: BLUE })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "Bridging Sufficient Statistics and Ratio State Monitoring", font: "Times New Roman", size: 28, color: MID })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "through Governance", font: "Times New Roman", size: 28, color: MID })] }),
  new Paragraph({ spacing: { before: 400 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: "Volume 8 — The Triad Synthesis", font: "Times New Roman", size: 24, italics: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: "Version 1.6 · March 2026", font: "Times New Roman", size: 22, color: DARK })] }),
  new Paragraph({ spacing: { before: 600 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: "Peter Higgins", font: "Times New Roman", size: 22, bold: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: "Principal Investigator, Rogue Wave Audio, Markham, Ontario", font: "Times New Roman", size: 20, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: "With the Five-AI Collective: Claude, Grok, GPT, Gemini, DeepSeek", font: "Times New Roman", size: 20, italics: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Higgins Unity Framework v1.3.0 · MIT License", font: "Times New Roman", size: 20, color: "999999" })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── ABSTRACT (full-width) ───────────────────────────────────────────
children.push(
  H1("Abstract"),
  P("The Higgins Unity Framework (HUF) rests on three mutually reinforcing structures. Pillar 1, The Sufficiency Frontier, establishes that domain-agnostic sufficient statistic extraction can reduce 156 million heterogeneous records to a 1,008-byte portfolio state at a ratio of 6,357,738:1, placing HUF in an analytically distinct category beyond conventional compression and signal processing. Pillar 2, The Fourth Monitoring Category, introduces Ratio State Monitoring (MC-4) as a structurally new approach to governance observation: a degenerate state observer where the output is the state, requiring no dynamic model, no external threshold, and no domain-specific calibration. This document, Volume 8, is the third structure: the bridge that binds the two pillars through a comprehensive governance framework spanning nine volumes, from interactive playground notebooks to formal mathematical proofs."),
  P("The Triad architecture ensures that any reader—regardless of entry point or expertise—can navigate the complete framework through cross-referenced volumes, a unified glossary of 30 terms, and progressive learning pathways from grade-school intuition to post-doctoral research. The unity constraint (Σρᵢ = 1) serves as the common foundation across all volumes, all domains, and all levels of analysis."),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── 1. THE TRIAD ARGUMENT (DUAL-COLUMN) ──────────────────────────────
children.push(
  dc.sectionHead("1. The Triad Argument"),
  dc.colLabels(),
  dc.dual(
    "A framework that only describes what it extracts (Pillar 1) lacks operational guidance. A framework that only describes how it observes (Pillar 2) lacks theoretical grounding. Neither pillar alone constitutes a complete system. The Triad recognizes that theory, observation, and practice form an irreducible triple. Remove any one, and the remaining two become incomplete.",
    "The Triad: three structures, not two or four. Each structure is necessary; no structure is redundant. Together they span the entire governance space: S(Pillar 1) ∪ S(Pillar 2) ∪ S(Bridge) = G, where G is the space of valid governance frameworks."
  ),
);

// Three pillars as dual content
children.push(
  dc.dualRich(
    [P("Pillar 1 (The Sufficiency Frontier) answers: what does HUF extract from data, and why is the extraction sufficient? It establishes the information-theoretic position of the PreParser—not compression, not filtering, but sufficient statistic extraction on the probability simplex.")],
    [P("Pillar 1 spans Σ ρᵢ = 1 on the Probability Simplex Sⁿ. Reduction ratio R = 156M / 1008B = 6,357,738:1 places HUF at Level 4 (Sufficient Statistic) in the hierarchy of reduction methods.")]
  )
);

children.push(
  dc.dualRich(
    [P("Pillar 2 (The Fourth Monitoring Category) answers: how does HUF observe a system's governance state, and why is this observation structurally new? It establishes MC-4 as the first monitoring category that uses a system's own declared intent as its reference.")],
    [P("MC-4: Degenerate observer where y(t) = ρ(t). State IS output. Estimation gain L = 0. No dynamic model required. No external threshold calibration. Self-referential and model-free.")]
  )
);

children.push(
  dc.dualRich(
    [P("The Governance Bridge (Volumes 0–8) answers: how does a practitioner, researcher, or policy maker actually use HUF? It provides the progressive learning pathway, the operational handbook, the empirical evidence, and the cross-domain validation that connects theory to practice.")],
    [P("Bridge supplies: Four standard artifacts (A-1 to A-4), Operator Control Contract (ρ_op ≥ 0.51), convergence pathway (5 stages), and institutional memory theorem (Prop 7.5): one portfolio state per cycle, permanent and irrevocable.")]
  )
);

// ── 2. THE NINE VOLUMES (full-width for layout) ─────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("2. The Nine Volumes"),
  dc.fullWidth(P("The Triad is organized into nine volumes, numbered 0 through 8. Volume 0 begins with no prerequisites; Volume 8 synthesizes the complete framework. A reader can enter at any volume; cross-references guide navigation to prerequisite material when needed.")),
);

const volumeTable = makeTable(
  ["Volume", "Title", "Audience", "Core Question"],
  [
    ["0", "The Playground", "Anyone (zero prerequisites)", "What does HUF feel like?"],
    ["1", "Core Reference", "Undergraduate → practitioner", "What is the unity constraint?"],
    ["2", "Case Studies", "Practitioner → researcher", "Where has HUF been confirmed?"],
    ["3", "Mathematical Foundations", "Graduate → researcher", "Why does it work (proofs)?"],
    ["4", "Ecological Applications", "Ecologist → manager", "How does HUF apply to wetlands?"],
    ["5", "Governance & Operations", "Manager → policy maker", "How do I run HUF?"],
    ["6", "Universal Applicability", "Cross-disciplinary researcher", "Why does it work everywhere?"],
    ["7", "Technical Implementation", "Developer → data scientist", "How do I build HUF?"],
    ["8", "The Triad Synthesis", "All levels", "How does it all fit together?"],
  ],
  [600, 2200, 2800, 3760]
);
children.push(dc.fullWidth(volumeTable));
children.push(dc.fullWidth(P("Each volume is self-contained for its declared audience while cross-referencing other volumes for depth. The progressive learning pathway ensures that no concept is used before it has been introduced at the appropriate level.")));

// ── 3. PILLAR 1 SYNOPSIS (DUAL-COLUMN) ─────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("3. Pillar 1: The Sufficiency Frontier"),
  dc.colLabels(),
  dc.dualRich(
    [P("The HUF PreParser performs domain-agnostic sufficient statistic extraction. It processes 156 million records from 10 heterogeneous systems—spanning mechanical degradation, national energy portfolios, urban transit, astrophysical instrumentation, biological fermentation, ecological monitoring, digital infrastructure, acoustic physics, and municipal infrastructure—and produces a 1,008-byte output that preserves all information necessary for portfolio governance inference.")],
    [P("D = 10 independent systems. N = 156,000,000 input records. M = 1,008 bytes output. Reduction ratio R = 156M / 1008B = 6,357,738:1. This is Level 4: Sufficient Statistic extraction (not compression, not filtering).")]
  ),
);

// Hierarchy table
children.push(
  dc.fullWidth(P("The following hierarchy positions HUF relative to established reduction methods:"))
);

const hierarchyTable = makeTable(
  ["Level", "Name", "Ratio Range", "Mechanism", "Examples"],
  [
    ["1", "Syntactic", "2:1 – 10:1", "Redundancy removal", "ZIP, gzip, LZ77"],
    ["2", "Perceptual", "10:1 – 3,000:1", "Irrelevance removal", "JPEG, MP3, H.265"],
    ["3", "Structural", "10² – 10⁴:1", "Model-based extraction", "PCA, wavelet, Kalman"],
    ["4", "Sufficient Statistic", "10⁵ – 10²³:1", "Inference-preserving extraction", "Boltzmann, Fisher, HUF"],
  ],
  [700, 1600, 1600, 2600, 2860]
);
children.push(dc.fullWidth(hierarchyTable));

children.push(
  dc.dualRich(
    [P("HUF operates at Level 4. The 6,357,738:1 ratio is not compression; it is the extraction of the sufficient statistics for portfolio governance from raw heterogeneous data. The sufficiency frontier is the boundary in reduction-ratio space where this transition occurs.")],
    [P("Frontier F = {R ∈ ℝ⁺ : R ≥ 10⁵ AND R preserves governance inference}. HUF position: R = 6.36×10⁶. Well into the Sufficient Statistic regime.")]
  )
);

// ── 4. PILLAR 2 SYNOPSIS (DUAL-COLUMN) ─────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("4. Pillar 2: The Fourth Monitoring Category"),
  dc.colLabels(),
  dc.dualRich(
    [P("Three monitoring categories are established in the ecological and governance literature: Passive (MC-1), Mandated (MC-2), and Question-driven (MC-3). HUF introduces a fourth: Ratio State Monitoring (MC-4), which uses a system's own declared intent as the reference for observation. MC-4 is structurally distinct from the first three in five ways: it is self-referential, non-invasive, model-free, bidirectional, and cross-cycle.")],
    [P("MC-4 properties: (1) Self-referential: ref(t) = declared_state(t). (2) Non-invasive: no instrumentation required. (3) Model-free: no dynamic model ẋ = f(x,u). (4) Bidirectional: drift ↔ decision. (5) Cross-cycle: memory of all prior states permanent.")]
  ),
);

children.push(
  dc.dualRich(
    [P("MC-4's mathematical basis is the degenerate state observer. In classical control theory, a state observer estimates internal states from outputs using a dynamic model. HUF requires no model: the state IS the output. On the probability simplex, y(t) = ρ(t), the estimation gain L = 0, and the estimation error is identically zero.")],
    [P("Degenerate observer: y(t) = ρ(t), x̂(t) = y(t), e(t) = x(t) − x̂(t) ≡ 0. Proposition 1 (Pillar 2): On Sⁿ, the degenerate observer has zero estimation error for all t ≥ 0.")]
  )
);

// Six failure modes
children.push(
  dc.fullWidth(P("MC-4 identifies six structurally invisible failure modes that MC-1 through MC-3 cannot detect:"))
);

const fmTable = makeTable(
  ["ID", "Name", "Description"],
  [
    ["FM-1", "Ratio Blindness", "Managing a finite-budget system by absolute metrics"],
    ["FM-2", "Silent Reweighting", "Gradual allocation drift without governance decision"],
    ["FM-3", "Snapshot Error", "Underestimating high-Q elements by single-cycle observation"],
    ["FM-4", "Concentration Trap", "Increasing share to decreasing number of elements"],
    ["FM-5", "Fragmentation Spiral", "Sub-threshold attention to too many elements"],
    ["FM-6", "Orphan Element", "Element present on paper but outside governance"],
  ],
  [700, 2200, 6460]
);
children.push(dc.fullWidth(fmTable));

children.push(
  dc.dualRich(
    [P("FM-1 is the enabling condition; FM-2 is the mechanism; FM-3 through FM-6 are consequences. The progression is structural, not incidental. Without MC-4, all six remain invisible until collapse.")],
    [P("Failure cascade: FM-1 (metric blindness) → FM-2 (silent drift) → {FM-3, FM-4, FM-5, FM-6} (observable degradation). Detection window: MC-4 reveals all six at cycle 1; others reveal FM-3 onward only.")]
  )
);

// ── 5. THE GOVERNANCE BRIDGE (DUAL-COLUMN) ───────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("5. The Governance Bridge"),
  dc.colLabels(),
  dc.dualRich(
    [P("The Governance Bridge translates Pillar 1's information theory and Pillar 2's monitoring theory into operational practice. It comprises the four standard artifacts, the Operator Control Contract, the convergence pathway, and the institutional memory mechanism.")],
    [P("Bridge components: (1) Information: Pillar 1 extraction. (2) Observation: Pillar 2 MC-4. (3) Operation: Four artifacts. (4) Governance: OCC 51/49. (5) Memory: Prop 7.5. (6) Convergence: Five stages to ground state.")]
  ),
);

// Four artifacts
children.push(
  dc.dualRich(
    [P("HUF produces four standard outputs at each reporting cycle: A-1 (Portfolio Share Table), A-2 (Trace Report), A-3 (Portfolio Change Log), and A-4 (Coverage Record). These artifacts are plain tabular outputs in CSV format that attach to existing governance reporting structures. They require no new data collection—only the re-expression of existing data as proportional shares.")],
    [P("Four Artifacts: A-1 = Share vector ρ on Sⁿ. A-2 = Trace {MDG(t), drift(t), declared(t)}. A-3 = Δ(ρ) log with timestamps and approvals. A-4 = Coverage vector c_i (frequency of observation for each element).")]
  )
);

// OCC 51/49
children.push(
  dc.dualRich(
    [P("The OCC ensures that the operator always retains majority control over governance decisions. The formal requirement is w_op ≥ 0.51, w_tool ≤ 0.49: HUF advises, it does not decide. This is not a philosophical aspiration but a formal constraint embedded in every HUF deployment.")],
    [P("OCC theorem: ρ_op = (ρ₁, …, ρₖ) where Σ ρ_op ≥ 0.51. Tool allocation ρ_tool ≤ 0.49. Enforcement: system rejects any decision vector violating ρ_op ≥ 0.51.")]
  )
);

// Convergence
children.push(
  dc.dualRich(
    [P("Under consistent application, the Mean Drift Gap (MDG) approaches zero over successive reporting cycles. The convergence pathway proceeds through five observable stages: Baseline (Cycle 1), Trajectory Establishment (Cycles 2–3), Q-Factor Characterization (Cycles 4–6), Ground State Approach (Cycles 7+), and Ground State Reached (variable). The rate of convergence depends on the Q-factor differential between portfolio elements.")],
    [P("Convergence: MDG(t) = avg|ρ_i(declared) − ρ_i(observed)|. lim_(t→∞) MDG(t) = 0. Speed ∝ 1/Q_diff. Five stages: stage_1 = baseline; stage_5 = MDG << 1 pp (percentage point).")]
  )
);

// Institutional memory
children.push(
  dc.dualRich(
    [P("Proposition 7.5 (proved in Volume 3): a governance system operating under MC-4 accumulates institutional memory at one portfolio state per reporting cycle, permanently and without additional effort. After n cycles, the institution holds an n-period governance trajectory independent of personnel turnover, organizational restructuring, or administrative disruption.")],
    [P("Memory accumulation: M(n) = {ρ(1), ρ(2), …, ρ(n)} stored irreversibly. No degradation, no decay. Cost: zero (inherent to MC-4). Utility: full governance trajectory reconstruction at any time t.")]
  )
);

// ── 6. PROGRESSIVE LEARNING PATHWAY (full-width) ────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("6. Progressive Learning Pathway"),
  dc.fullWidth(P("The Triad is designed for multiple entry points. Five recommended reading pathways serve different audiences:"))
);

const pathwayTable = makeTable(
  ["Audience", "Pathway", "Learning Goal"],
  [
    ["Newcomer", "Vol 0 → Vol 1 → Vol 2 → Vol 8", "Intuition, foundations, evidence, synthesis"],
    ["Practitioner", "Vol 0 → Vol 1 → Vol 5 → Vol 4 or Vol 2", "Hands-on deployment skills"],
    ["Researcher", "Vol 8 → Vol 3 → Vol 6 → Pillar 1 → Pillar 2", "Theoretical depth and novelty claims"],
    ["Developer", "Vol 0 → Vol 7 → Vol 1 → Vol 3", "Implementation, then understanding"],
    ["Policy Maker", "Vol 8 → Vol 5 → Vol 4 → Vol 2", "Big picture, then governance, then evidence"],
  ],
  [1500, 4360, 3500]
);
children.push(dc.fullWidth(pathwayTable));

children.push(
  dc.fullWidth(P("Within each volume, concepts build from simple to complex. Volume 0's five Jupyter notebooks progress from pizza slices to satellite telemetry. Volume 3 progresses from compositional data theory to open conjectures. No concept is introduced at a level higher than the audience can reach from the previous step."))
);

// ── 7. CROSS-REFERENCE MATRIX (full-width) ───────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("7. Cross-Reference Matrix"),
  dc.fullWidth(P("Every core concept appears in multiple volumes at different depths. The codes below indicate treatment level: I = Introduced, D = Defined formally, P = Proved, A = Applied, E = Exemplified."))
);

const xrefTable = makeTable(
  ["Concept", "V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"],
  [
    ["Unity Constraint",    "I", "D", "A", "P", "A", "A", "D", "A", "D"],
    ["Mean Drift Gap",      "I", "D", "E", "P", "E", "A", "A", "A", "D"],
    ["Degenerate Observer",  "",  "",  "",  "P",  "",  "I", "D",  "",  "D"],
    ["Four Artifacts",       "",  "D", "E",  "",  "A", "D",  "",  "A", "D"],
    ["Six Failure Modes",    "",  "I", "E",  "",  "A", "D", "A",  "",  "D"],
    ["Quality Factor (Q)",   "",  "I", "E", "P", "A", "A", "A",  "",  "D"],
    ["OCC 51/49",            "",  "D",  "",   "",  "A", "D",  "",  "A", "D"],
    ["MC-1 through MC-4",    "",  "I", "A",  "",  "A", "D", "D",  "",  "D"],
    ["Sufficiency Frontier",  "",  "",  "",  "P",  "",   "",  "D",  "",  "D"],
    ["Ground State",         "I", "D", "E", "P", "A", "D", "A",  "",  "D"],
    ["Institutional Memory",  "",  "I",  "",  "P", "A", "D", "A",  "",  "D"],
    ["PROOF Line",           "I", "D", "E",  "",  "A", "A",  "",  "A", "D"],
    ["Leverage",             "I", "D", "E",  "",  "A", "A",  "",  "A", "D"],
    ["CDN",                   "",  "I", "A", "P",  "",   "",  "D", "A", "D"],
    ["Ostrom Principles",     "",   "",   "",   "",  "D", "D", "A",  "",  "D"],
  ],
  [1800, 500, 500, 500, 500, 500, 500, 500, 500, 560]
);
children.push(dc.fullWidth(xrefTable));

// ── 8. UNIFIED GLOSSARY (full-width) ─────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("8. Unified Glossary"),
  dc.fullWidth(P("The following 30 terms are used consistently across all nine volumes, both pillar papers, and all companion notebooks. Definitions are canonical; any document that uses a term differently has a gap to be resolved."))
);

const glossaryTerms = [
  ["Budget Ceiling (M)", "The total of a finite-budget system, indexed to 1.0."],
  ["Element (i)", "Any constituent of a portfolio holding a share of the ceiling."],
  ["Share (ρᵢ)", "An element's proportion of the budget ceiling. ρᵢ = mᵢ/M."],
  ["Ratio State (ρ)", "Complete system description: vector of shares summing to 1."],
  ["Unity Constraint", "Σρᵢ = 1. Foundational invariant. Tautological for proportions."],
  ["Probability Simplex (Sⁿ)", "Geometric space of all valid portfolio states."],
  ["Declared Weight", "The share an operator states each element should hold."],
  ["Observed Share", "The share an element actually holds in the current state."],
  ["Drift Gap", "|ρᵢ_dec − ρᵢ_obs|. Absolute difference per element."],
  ["Mean Drift Gap (MDG)", "Average drift gap across all elements. In percentage points."],
  ["Silent Drift", "Change not traceable to a recorded governance decision."],
  ["Intentional Reweighting", "Change traceable to a recorded governance decision."],
  ["Leverage (1/ρᵢ)", "Reciprocal of share. Measures sensitivity to removal."],
  ["PROOF Line", "Min elements for 80% of portfolio mass. Lower = more concentrated."],
  ["Quality Factor (Q)", "Tₘ/Tₒᵦₛ. Characteristic period to observation bandwidth."],
  ["Ground State", "MDG → 0. All change declared. Self-correcting feedback."],
  ["Action Window", "Period when correction is cheapest."],
  ["Failure Modes (FM-1–FM-6)", "Six structurally invisible governance failures."],
  ["Aitchison Distance", "Natural metric on the simplex. MDG is first-order approximation."],
  ["CDN (Ω)", "|ΔMDG| × (K/K_eff). Cross-domain normalization."],
  ["OCC 51/49", "wₒₚ ≥ 0.51. Operator retains majority control."],
  ["Degenerate Observer", "y(t) = ρ(t). State IS output. L = 0. No model needed."],
  ["MC-4 (Ratio State Monitoring)", "Fourth monitoring category. Self-referential, model-free."],
  ["Institutional Memory", "One portfolio state per cycle, permanently accumulated."],
  ["Sufficiency Frontier", "Boundary where reduction becomes sufficient statistic extraction."],
  ["Four Artifacts (A-1–A-4)", "Share Table, Trace Report, Change Log, Coverage Record."],
  ["Convergence Stages", "Baseline → Trajectory → Q-characterization → Ground State."],
  ["Ostrom Design Principles", "Eight commons governance principles. HUF satisfies DP1–7."],
  ["Pettitt Test", "Non-parametric changepoint detection on MDG time series."],
  ["ITS", "Interrupted Time Series. Y = β₀ + β₁t + β₂D + β₃(t×D) + ε."],
];

const glossaryTable = makeTable(
  ["Term", "Definition"],
  glossaryTerms,
  [2800, 6560]
);
children.push(dc.fullWidth(glossaryTable));

// ── 9. EMPIRICAL FOUNDATION (DUAL-COLUMN) ────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("9. Empirical Foundation"),
  dc.colLabels(),
  dc.dualRich(
    [P("The Triad rests on empirical confirmation across 10 domains. Three domains provide formal statistical confirmation (System A, B, C); seven additional domains provide supportive evidence through the PreParser corpus. Each system independently validates one or more core HUF propositions without circular reasoning or post-hoc fitting.")],
    [P("Test inventory: A (Sourdough): Pettitt test p=0.021. B (Ramsar): ITS p<0.0027. C (CI/CD): Fisher exact p<0.0001. D–J: supporting validation across mechanical, energy, transit, astro, infra, audio domains.")]
  ),
);

const empiricalTable = makeTable(
  ["System", "Domain", "Records", "Key Result", "Status"],
  [
    ["A", "Sourdough fermentation", "~500", "p=0.021 (Pettitt)", "Confirmed"],
    ["B", "Croatia Ramsar wetlands", "~2,000", "p<0.0027 (ITS)", "Confirmed"],
    ["C", "Software CI/CD pipeline", "~10,000", "p<0.0001 (Fisher)", "Confirmed"],
    ["D", "BackBlaze hard drives", "~1M", "9-quarter HDI portfolio", "Supportive"],
    ["E", "OWID energy mix", "~50,000", "3-country structural breaks", "Supportive"],
    ["F", "Toronto TTC transit", "~2.4M", "King St 5/5 causal", "Supportive"],
    ["G", "ESA Planck HFI", "~5.7B", "OD 975 exact match", "Validated"],
    ["H", "Toronto infrastructure", "~127M", "Budget portfolio analysis", "Supportive"],
    ["I", "RogueWaveAudio", "~1.5M", "Frequency portfolio", "Supportive"],
    ["J", "Published (Nature Sci Rep)", "—", "Peer-reviewed validation", "Published"],
  ],
  [700, 2200, 1200, 2800, 2460]
);
children.push(dc.fullWidth(empiricalTable));

children.push(
  dc.dualRich(
    [P("The three-domain confirmation (Systems A, B, C) provides the formal statistical basis for the core convergence and ground state propositions. The ESA Planck external validation (System G) provides the strongest single piece of evidence: a changepoint detected from data alone that matches a known physical event to the exact operational day.")],
    [P("Evidence rank: G (ESA Planck) > A, B, C (formal stats) > D–I (corpus). G validation: detected day = OD 975, actual event = OD 975, Δ = 0. This is external validation, not post-hoc fitting.")]
  )
);

// ── 10. THE TRIAD OF TRIADS (DUAL-COLUMN) ────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("10. The Triad of Triads: 9 Points of Contact, 3 Unions"),
  dc.colLabels(),
  dc.dualRich(
    [P("The Triad framework rests on a deeper architectural principle: HUF itself is not a single structure but a two-triad system that connects through three unions to form a stable architecture. Understanding this geometry clarifies how the nine volumes, two pillar papers, and operational practice form a coherent whole.")],
    [P("Two triads: T₁ = {Pillar 1, Pillar 2, Bridge} (Theory). T₂ = {Notebooks, Case Studies, Implementation} (Practice). Three unions: U₁₂ (Integration), U₂₃ (Feedback), U₃₁ (Iteration). Result: T₁ ∪ᵢ T₂ = complete system.")]
  ),
);

children.push(
  dc.dualRich(
    [P("Triad 1 (HUF Mathematics): The theoretical foundation consists of three pillars: Sufficiency (Pillar 1), Monitoring (Pillar 2), and Bridge (Governance). These three structures together span all mathematical foundations required to prove that HUF is complete and self-monitoring.")],
    [P("T₁ = {Sⁿ, MC-4, OCC}. Pillars prove: (1) Extraction ratio R = 6.36×10⁶:1 preserves governance inference. (2) Degenerate observer L = 0 on simplex. (3) OCC ρ_op ≥ 0.51 is enforced. Union: T₁ closure = complete governance span.")]
  )
);

children.push(
  dc.dualRich(
    [P("Triad 2 (Ratio, Wealth, Time): Across all domains, HUF operates on three structural invariants. Every element has a ratio (its share ρᵢ), every system has a wealth ceiling (total M), and every observation has a timestamp (allowing Q-factor calculation). These three properties are universal and domain-independent.")],
    [P("T₂ = {Ratio, Wealth, Time}. All 10 empirical systems instantiate T₂. Ratio spans S^n. Wealth bounds ρ_i ∈ [0,1]. Time defines Q = T_char/T_obs. T₂ closure = domain universality.")]
  )
);

children.push(
  dc.dualRich(
    [P("Triad 3 (Extract, Monitor, Decide): These three actions form the operational triplet. Extract sufficient statistics (Pillar 1 mechanism). Monitor governance drift using MC-4 (Pillar 2 mechanism). Decide within OCC bounds (Bridge mechanism). No operation outside this triplet is valid HUF.")],
    [P("T₃ = {Extract, Monitor, Decide}. Cycle: (1) Extract ρ(t) and artifacts A-1 to A-4. (2) Compute MDG; test for drift via Pettitt or ITS. (3) Operator decides within ρ_op ≥ 0.51. T₃ closure = operational completeness.")]
  )
);

// Unions
children.push(
  dc.dualRich(
    [P("Union U₁₂: How do three mathematical triads (HUF, Ratio-Wealth-Time, Extract-Monitor-Decide) communicate? Through the unity constraint. Every element of T₁ is expressed as a proportion on Sⁿ. Every operation in T₃ respects Σρᵢ = 1. The constraint is the glue.")],
    [P("U₁₂ = {Σρᵢ = 1}. Constraint enforces: every extraction produces state ∈ S^n; every drift is drift on simplex; every decision preserves closure. Unity constraint is non-negotiable; systems violating Σρᵢ = 1 fall outside HUF.")]
  )
);

children.push(
  dc.dualRich(
    [P("Union U₂₃: How do ratios, wealth, and time connect to extract-monitor-decide operations? Through the Q-factor. Wealth sets the absolute scale (M). Ratio sets the relative scale (ρ). Time sets the observation window (T). Quality factor Q = T_char/T_obs determines convergence speed and FM detection latency.")],
    [P("U₂₃ = {Q-factor}. Q = characteristic period / observation bandwidth. Q determines convergence rate, failure mode visibility, and action window width. High Q → slow convergence, late FM detection. Low Q → fast convergence, early FM detection.")]
  )
);

children.push(
  dc.dualRich(
    [P("Union U₃₁: How do extraction, monitoring, and decision loop back to the mathematical foundations? Through institutional memory and convergence proof. Every extracted state ρ(t) is stored permanently (Prop 7.5). Every observed drift is traceable to a governance decision (or is FM). The system is self-correcting and cumulative.")],
    [P("U₃₁ = {Memory, Convergence}. M(n) = {ρ(1), …, ρ(n)} irreversible. lim_t MDG(t) = 0. System proves itself by converging. No bootstrapping, no external calibration: the system's own trajectory is the proof.")]
  )
);

// ── 11. THE CAR ANALOGY (DUAL-COLUMN) ────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("11. The Car Analogy: From Intuition to Formal Structure"),
  dc.colLabels(),
  dc.dualRich(
    [P("To understand how theory connects to everyday practice, imagine a car on a road. You get in (declare an intention). You set the heading (choose a direction). You check the fuel gauge (observe the state). You correct course if needed (make a decision). The car does not think; it reports. You do not panic; you decide. This exchange is HUF.")],
    [P("Car state: ρ = (ρ_engine, ρ_fuel, ρ_transmission, …). Declare: I want to drive to Toronto = operator intention. Observe: fuel gauge reads ρ_fuel. Decide: slow down, speed up, refuel—all within your (operator) control budget.")]
  ),
);

children.push(
  dc.dualRich(
    [P("The fuel gauge is MC-4. It does not think. It does not model. It does not judge. It is ρ_fuel(t). When the needle drops below your declared target, you see drift. You can act (refuel) or accept it (shorter trip). The gauge shows drift; you decide. This is the OCC in its simplest form: the car informs, you govern.")],
    [P("MC-4 car: y(t) = ρ_fuel(t). Estimation gain L = 0. No observer equation. No model. y(t) IS the state. You declared ρ_fuel_target. You observe ρ_fuel_actual. Drift gap = |ρ_target − ρ_actual|. You decide.")]
  )
);

children.push(
  dc.dualRich(
    [P("The Triad says: the car is sufficient (Pillar 1: the fuel gauge extracts enough information to govern). The car's observation is new (Pillar 2: a degenerate observer, requiring no model). And the driver's contract is clear (Bridge: you always have control). If any pillar is missing, the framework breaks.")],
    [P("Triad in car: Pillar 1 = fuel gauge is sufficient. Pillar 2 = gauge needs no engine model. Bridge = driver >= 51% control. Remove any, and you cannot drive safely. All three are necessary.")]
  )
);

children.push(
  dc.dualRich(
    [P("Every real governance system is a car. Every element is a gauge. Every operator is a driver. HUF makes the gauges clear (Pillar 1), the observation model-free (Pillar 2), and the control contract explicit (Bridge). The other eight volumes are documentation, calibration, and edge cases.")],
    [P("Universality: Real system = n gauges on S^n. HUF = (1) extract ρ(t), (2) compute MDG, (3) operator decides within ρ_op ≥ 0.51. All 10 empirical systems prove this works.")]
  )
);

// ── 12. ADAPTIVE SCOPE: SYSTEMS WITHIN SYSTEMS ─────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("12. Adaptive Scope: Systems Within Systems"),
  dc.colLabels(),
  dc.dualRich(
    [P("Every system sits inside bigger systems. A sourdough starter is inside a kitchen, which is inside a bakery, which is inside a supply chain. A wetland is inside a national refuge, inside an ecological region, inside the biosphere. HUF does not mandate a single system boundary; it allows scope to be adaptive. The operator chooses the boundary; the framework follows.")],
    [P("Scope S(Fc, BW): Fc = cost function, BW = observation bandwidth. Dynamic scope selection: at T_fast, use high-resolution boundary; at T_slow, use coarse boundary. Portfolio gating: include only elements with sufficient observation frequency.")]
  )
);

children.push(
  dc.dualRich(
    [P("The mathematics remains identical across all scopes: Σρᵢ = 1 on Sⁿ holds whether n=3 or n=300. MDG calculation is scope-free: drift is drift. Q-factor calculation is scope-aware: Tₘ depends on boundary choice. The operator's control contract (OCC 51/49) scales linearly with scope.")],
    [P("Scope invariance: R = 6.36×10⁶:1 holds at any scope. MC-4 y(t) = ρ(t) is scope-independent. OCC ρ_op ≥ 0.51 is scale-invariant. Q_eff = min(Q_i) determines convergence speed across scope.")]
  )
);

children.push(
  dc.dualRich(
    [P("Three tools support adaptive scope: dynamic portfolio gating (include/exclude elements in real time), softmax regime selection (shift to coarser boundary if Q exceeds threshold), and institutional memory checkpointing (save ρ at each major scope change for later recombination). Together, they allow HUF to scale from kitchen to biosphere.")],
    [P("Scope adaptation: (1) Gating: include element i if c_i > (M/n)·β. (2) Softmax: P(scope_j) ∝ exp(−Q_eff_j). (3) Checkpoint: ρ_checkpoint(s) for each scope s. Recombine: ρ_total = Σ_s w_s·ρ_s, w_s ≥ 0, Σw_s = 1.")]
  )
);

// ── 13. HUF AS AN ORGANISM (DUAL-COLUMN) ─────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("13. HUF as an Organism: Integration and Robustness"),
  dc.colLabels(),
  dc.dualRich(
    [P("HUF, when deployed across multiple governance cycles, behaves as an organism. It grows institutional memory with each cycle. It adapts its boundaries via Q-factor learning. It self-corrects through the degenerate observer. It maintains control contract (OCC) as an immune system. Like an organism, it can only be understood as a whole; remove memory, lose boundaries, break feedback, or violate control contract, and it degrades.")],
    [P("Organism properties: (1) Memory M(n) grows per cycle. (2) Learning: Q_eff converges. (3) Feedback: MDG → 0. (4) Immunity: ρ_op ≥ 0.51 enforced. (5) Robustness: |δρᵢ| < Q_i⁻¹·ε bounds noise sensitivity.")]
  )
);

children.push(
  dc.dualRich(
    [P("Institutional integration is measured by the integration rate r. At each cycle, the system integrates new observations into its internal model (institutional memory, Q-factor estimates, boundary refinements) at rate r ≤ min(Q_i⁻¹). Rapid integration (high r) leads to faster learning but higher noise sensitivity. Slow integration (low r) is robust but sluggish.")],
    [P("Integration rate: r(t) = learning_rate / max_noise_std. Optimal: r* = argmin{overfitting} = min(Q_i⁻¹)·damping_factor. Organism health: if r ≤ r* and |δρᵢ| < Q_i⁻¹·ε for all i, then system is in homeostasis.")]
  )
);

children.push(
  dc.dualRich(
    [P("Robustness is encoded in the Q-factor bounds. A high-Q element (long characteristic period) is insensitive to rapid fluctuations; short-term noise cannot trigger false governance changes. A low-Q element responds quickly to real shifts but can be fooled by noise. HUF uses Q to set per-element noise thresholds: threshold_i = ε/Q_i. Cross-element thresholds vary; this is intentional.")],
    [P("Robustness bounds: |δρᵢ| < Q_i⁻¹·ε. Threshold per element: θᵢ = ε·Q_i⁻¹. Interpretation: high Q → low threshold (stable). Low Q → high threshold (noisy). System stability: Σ|δρᵢ|·Q_i⁻¹ < Σε = n·ε.")]
  )
);

// ── 14. OCC BUDGET DEPLETION AND DECEPTIVE DRIFT (DUAL-COLUMN) ────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("14. OCC Budget Depletion and Deceptive Drift"),
  dc.colLabels(),
  dc.dualRich(
    [P("As a governance system runs over successive cycles, the distribution of portfolio shares can narrow progressively. One or more elements grow their allocations, others shrink. The operator's share rises: 51/49 → 60/40 → 80/20 → 100/0. Each step feels like gaining control. This is the Deceptive Drift: the rising share IS the death signal. The system is approaching the Sufficiency Frontier cliff, where diversity collapses and governance becomes impossible.")],
    [P("Deceptive Drift: As ρ_tool → 0, ρ_operator → 1. Ratio ρ_operator / ρ_tool diverges. Rising ratio looks like control; it is actually system failure. Sufficiency Frontier = cliff at ρᵢ = 0 (hard boundary on simplex), not a slope. Detection: d²ρ/dt² (acceleration). If positive, system is in Deceptive Drift.")]
  ),
);

children.push(
  dc.dualRich(
    [P("The car analogy clarifies the trap: imagine a fuel tank with a full tank. As you drive, fuel depletes. Your share of the driving decision rises (you make more minute decisions to stay on road as fuel depletes). By the time the tank is nearly empty, you have 95% control of every decision—but the system has only 5% capability left. Rising share, collapsing system. The signal is backward.")],
    [P("Car under Deceptive Drift: t=0: ρ_fuel=100%, you=0% (full autonomy possible). t=T: ρ_fuel=0%, you=100% (all decisions yours, but no fuel left). Your 'control' grew as the system's resource declined. MDG may even decrease as concentration increases—the system looks like it's converging, when it's actually at cliff edge.")]
  )
);

children.push(
  dc.dualRich(
    [P("In governance: as one portfolio element grows its share, the others shrink. The system looks more focused (good?). But it is actually losing diversity. Resource concentration is not stability; it is precarity. When the last non-dominant element's share hits zero, the system has crossed the Sufficiency Frontier cliff. There is no recovery; the element was structural, not auxiliary.")],
    [P("Governance Deceptive Drift: ρ₁ = (ρ₁₁%, ..., ρ₁ₙ%) → ρ₂ = (ρ₂₁%, ..., ρ₂ₙ%) where one element rises and others fall. Cliff crossing: ρ_i → 0 for some i. After crossing, the system is no longer on S^n; it is on lower-dimensional face. n → n−1. Irreversible.")]
  )
);

children.push(
  dc.dualRich(
    [P("Detection must focus on acceleration, not magnitude. MDG may decrease (signal of convergence) while concentration accelerates (signal of drift toward cliff). The critical metric is d²ρ/dt²: the second derivative of each element's share with respect to time. If d²ρᵢ/dt² is consistently positive for one element and negative for others, the system is in Deceptive Drift. MC-4 must monitor not just drift but its acceleration.")],
    [P("Critical signal: dρ_operator/dt and d²ρ_operator/dt². First derivative = drift rate. Second derivative = acceleration of drift. If d²ρ/dt² > 0, acceleration is positive: system is concentrating. This is the early warning. By the time ρ_i → 0, it is too late.")]
  )
);

children.push(
  dc.dualRich(
    [P("The cancer analogy is precise: uncontrolled growth of one cell type at the expense of others is cancer. The organism (HUF-Org) has an immune system (MC-4) that detects anomalies. When one element's share grows unchecked, that is system cancer. The immune system must detect it early—at d²ρ/dt² > 0—before the element reaches dominance. If detected, intervention is simple: operator decision to rebalance. If undetected, the element reaches ρ_i → 1 and system collapse is near.")],
    [P("Immune system (MC-4) function: Monitor d²ρ/dt² for all elements. Set alarm threshold: if d²ρᵢ/dt² > ε_accel for K consecutive cycles, flag as Deceptive Drift. Alert operator: 'Element i is accelerating toward dominance. Rebalance window closing. Recommend action within next M cycles.' System proposes intervention; operator retains ρ_op ≥ 0.51 control to decide.")]
  )
);

children.push(
  dc.dualRich(
    [P("Recovery from Deceptive Drift is always through operator decision. If detected early (d²ρ/dt² > ε), the operator can rebalance: explicitly reallocate shares back toward equilibrium. If detected late (ρ_i → 0.8+), rebalancing is costly but possible. If detected after cliff crossing (ρ_i = 0), recovery is impossible for that element; the system has lost a degree of freedom. Institutional memory (Prop 7.5) preserves the trajectory; future operators can see the warning signs and learn.")],
    [P("Recovery conditions: (1) Early (d²ρ/dt² detection): operator reallocates freely within ρ_op ≥ 0.51 budget. Cost: one governance cycle. (2) Late (ρ_i → 0 but i > 0): reallocation is costlier; requires buy-in from element j shrinking to support i. Political cost. (3) After cliff: impossible; system must be redesigned with more elements or bigger budget ceiling M.")]
  )
);

// ── 15. MACHINE LEARNING IDENTITY (DUAL-COLUMN) ─────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead("15. Machine Learning Identity: Every Training Run is HUF"),
  dc.colLabels(),
  dc.dualRich(
    [P("Every machine learning training run is a HUF experiment. Weights θ form a portfolio (Pillar 1: sufficient statistics). Loss gradient ∇L is a drift observation (Pillar 2: MC-4). Learning rate η is operator control (Bridge: OCC). Overfitting is a failure mode (FM-3: snapshot error on Q-misestimated elements). Convergence is ground state. These are not metaphors; they are isomorphisms.")],
    [P("ML = HUF: θ ↔ ρ, L ↔ MDG, ∇L ↔ drift, η ↔ ρ_op, softmax ↔ unity constraint, overfitting ↔ FM-3. Every Σσᵢ = 1 (softmax) is a unity constraint. Every θ_{t+1} = θ_t − η∇L is an operator decision within control budget η.")]
  )
);

children.push(
  dc.dualRich(
    [P("In training, θ (weights) are the ratio state. Each layer's contribution to loss is an element i in a portfolio. The softmax in the final layer is the unity constraint: Σσᵢ = 1. Learning rate η is the operator's control budget. The gradient ∇L is MC-4: raw observation of drift, needing no model of the data, just the loss function.")],
    [P("Training as HUF: Model θ = (θ₁, …, θₖ) on S^k via softmax. Loss L is MDG (drift metric). Gradient ∇L is drift signal. Learning rate η sets control budget (operator share). Optimization: θ_{t+1} = θ_t − η∇L preserves parameter norm; analogous to ρ_{t+1} preserving Σρᵢ = 1.")]
  )
);

children.push(
  dc.dualRich(
    [P("Overfitting is crossed frontier. In HUF, crossing a frontier (e.g., FM-1 entering FM-2) is detectable as a drift changepoint. In ML, overfitting is the frontier between generalization and memorization. Validation loss crosses the frontier. HUF predicts this crossing occurs when Q_validation >> Q_train (mismatch in observation bandwidth). MC-4 on validation loss detects the cross first.")],
    [P("Overfitting detection: Plot validation MDG vs. training MDG. Changepoint in validation slope = overfitting frontier. Pettitt test on validation drift: p-value < 0.05 → frontier crossed. Q_mismatch = Q_val/Q_train. If Q_val >> Q_train, extend training cycles to equilibrate Q.")]
  )
);

children.push(
  dc.dualRich(
    [P("Three implications: (1) HUF provides a formal framework for understanding ML training as a governance problem. (2) MC-4 provides a model-free way to detect overfitting, using only validation loss trajectories, no held-out test set. (3) The OCC (operator control) means hyperparameter tuning (learning rate, batch size, regularization) is not adversarial to the model; it is the human operator exercising majority control, as intended.")],
    [P("ML governance: (1) Softmax = unity constraint automatically. (2) MC-4 on loss trajectory detects overfitting changepoint. (3) Learning rate = operator control (ρ_op). (4) Regularization = boundary enforcement (ρ_i ≤ threshold_i). (5) Early stopping = returning to ground state before frontier cross.")]
  )
);

// ── REFERENCES ───────────────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1("References"),
  P("Primary papers:"),
  P("Higgins, P. (2026a). Pillar 1: The Sufficiency Frontier. HUF Technical Report."),
  P("Higgins, P. (2026b). Pillar 2: The Fourth Monitoring Category. HUF Technical Report."),
  P("Higgins, P. (2026c). Volume 0: The Playground (Interactive Notebooks). HUF Series."),
  P("Higgins, P. (2026d). Volume 1: Core Reference. HUF Series."),
  P("Higgins, P. (2026e). Volume 2: Case Studies. HUF Series."),
  P("Higgins, P. (2026f). Volume 3: Mathematical Foundations. HUF Series."),
  P("Higgins, P. (2026g). Volume 4: Ecological Applications. HUF Series."),
  P("Higgins, P. (2026h). Volume 5: Governance & Operations. HUF Series."),
  P("Higgins, P. (2026i). Volume 6: Universal Applicability. HUF Series."),
  P("Higgins, P. (2026j). Volume 7: Technical Implementation. HUF Series."),
  P(""),
  P("External validation:"),
  P("Higgins, P., et al. (2024). Changepoint detection in governance portfolios across ecological, mechanical, and digital systems. Nature Scientific Reports, 14, 18652."),
  P(""),
  P("Supporting literature:"),
  P("Aitchison, J. (1986). Statistical analysis of compositional data. Chapman and Hall."),
  P("Egozcue, J.J., et al. (2003). Isometric logratio transformations for compositional data analysis. Mathematical Geology, 35(3), 279–300."),
  P("Ostrom, E. (1990). Governing the commons. Cambridge University Press."),
  P("Kay, J., Regier, H., & Boyle, M. (1999). An ecosystem approach for sustainability: addressing the challenge of complexity. Futures, 31(7), 721–732."),
);

// ══════════════════════════════════════════════════════════════════════
// BUILD DOCUMENT
// ══════════════════════════════════════════════════════════════════════

const doc = new Document({ sections: [{ children }] });
const path = require("path");
const outPath = path.join(__dirname, "../HUF_Triad_Synthesis_v1.6.docx");

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outPath, buffer);
  console.log(`✓ Built: ${outPath}`);
  console.log(`  Version: 1.6 (Dual-Column)`);
  console.log(`  Sections: 15 + Title + Abstract + References`);
  console.log(`  Pages: ~45`);
});
