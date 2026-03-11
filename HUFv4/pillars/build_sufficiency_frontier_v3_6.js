const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition,
        LevelFormat, ExternalHyperlink } = require('docx');
const { createDualHelpers } = require('../shared/dual_column');

// ── Initialize dual-column helpers ──────────────────────────────────────
const dc = createDualHelpers({ palette: 'huf' });

// ── Legacy helpers (for title, abstract, references) ──────────────────
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;
const CW = PAGE_W - 2 * MARGIN;
const BLUE = '1F3864', MID = '2E75B6', DARK = '333333';
const LGREY = 'F2F2F2', WHITE = 'FFFFFF';
const bdr = { style: BorderStyle.SINGLE, size: 1, color: 'BBBBBB' };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };

const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 28, color: BLUE })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 24, color: BLUE })] });

function P(content, opts = {}) {
  const { align, indent, spacing_after } = opts;
  const runs = [];
  if (typeof content === 'string') {
    runs.push(new TextRun({ text: content, font: 'Times New Roman', size: 22, color: DARK }));
  } else {
    content.forEach(c => runs.push(new TextRun({ font: 'Times New Roman', size: 22, color: DARK, ...c })));
  }
  const pOpts = { spacing: { after: spacing_after || 180, line: 276 }, children: runs };
  if (align) pOpts.alignment = align;
  if (indent) pOpts.indent = indent;
  return new Paragraph(pOpts);
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

// ══════════════════════════════════════════════════════════════════════════════
// CONTENT — Pillar 1 v3.6 — DUAL-COLUMN RESTRUCTURE
// ══════════════════════════════════════════════════════════════════════════════
const children = [];

// ── TITLE PAGE ──────────────────────────────────────────────────────────────
children.push(
  new Paragraph({ spacing: { before: 3000 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: 'THE SUFFICIENCY FRONTIER', font: 'Times New Roman', size: 44, bold: true, color: BLUE })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: 'Domain-Agnostic Sufficient Statistic Extraction', font: 'Times New Roman', size: 28, color: MID })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: 'at 6,357,738:1', font: 'Times New Roman', size: 28, color: MID })] }),
  new Paragraph({ spacing: { before: 400 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'Pillar 1 of the HUF Triad \u00B7 Version 3.6 \u00B7 Dual-Column Edition', font: 'Times New Roman', size: 24, italics: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'March 2026', font: 'Times New Roman', size: 22, color: DARK })] }),
  new Paragraph({ spacing: { before: 600 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: 'Peter Higgins', font: 'Times New Roman', size: 22, bold: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: 'Rogue Wave Audio, Markham, Ontario', font: 'Times New Roman', size: 20, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'HUF v1.2.0 \u00B7 MIT License', font: 'Times New Roman', size: 20, color: '999999' })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── ABSTRACT (single column) ────────────────────────────────────────────────
children.push(
  H1('Abstract'),
  P('Information reduction in science and engineering proceeds through a well-understood hierarchy: syntactic redundancy removal (2:1\u201310:1), perceptual irrelevance removal (10:1\u20133,000:1), and structural model-based extraction (10\u00B2\u201310\u2074:1). This paper identifies a fourth level\u2014sufficient statistic extraction\u2014and presents an empirical system operating at this level. The Higgins Unity Framework (HUF) PreParser processes 156,266,500 records from 10 heterogeneous domains and produces a 1,008-byte output that preserves the information necessary for portfolio governance inference, yielding a ratio of 6,357,738:1. We define the sufficiency frontier as the boundary in reduction-ratio space where this transition occurs, formalize its relationship to Fisher sufficiency and Boltzmann phase-space reduction, and provide external validation through changepoint detection on ESA Planck satellite data (Pettitt OD 975 = January 14, 2012, exact match with He-4 exhaustion). This expanded version (v3.6) presents the framework in dual-column format: Context (left, narrative) and Analytic (right, mathematical). Both paths are complete and complementary.'),
  new Paragraph({ children: [new PageBreak()] }),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 1. INTRODUCTION — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  dc.sectionHead('1. Introduction'),
  dc.colLabels(),
  dc.dual(
    'The question of how much a dataset can be reduced while preserving the information needed for a specific inference has a long history.',
    'Given data X and parameter θ, Fisher sufficiency defines T(X) sufficient for θ if P(X|T(X),θ) = P(X|T(X)) for all θ.'
  ),
  dc.dual(
    'Shannon\'s source coding theorem establishes the fundamental limit for lossless compression. Fisher\'s concept of sufficiency establishes when a statistic captures everything a sample says about a parameter. Boltzmann\'s statistical mechanics achieves the most extreme reduction in physics: from 10²³ particle states to a handful of thermodynamic variables.',
    'Theorem (Factorization): T(X) is sufficient for θ ⟺ L(θ;X) = g(T(X),θ)·h(X) where h(X) does not depend on θ. The Pitman–Koopman–Darmois (PKD) theorem restricts fixed-dimensional sufficiency to exponential families.'
  ),
  dc.dual(
    'These results share a common structure: they identify conditions under which massive data reduction preserves inferential power. They differ in the nature of the preserved quantity—syntactic fidelity for Shannon, parametric information for Fisher, macroscopic observables for Boltzmann.',
    'HUF departure: No exponential family assumption. No parametric model estimation. Instead: exploits structural invariant Σρᵢ=1 on probability simplex ΔK where ρ ∈ {ρ₁,...,ρK}, ρᵢ ≥ 0, Σρᵢ = 1.0.'
  ),
  dc.dual(
    'This paper presents a system that achieves reduction at the scale of Boltzmann\'s phase-space collapse (10⁷⁶·⁸:1) while operating across arbitrary domains without prior physical knowledge. The HUF PreParser extracts the sufficient statistics for portfolio governance from heterogeneous data, producing a vector of shares on the probability simplex. We argue that this constitutes a fourth level in the hierarchy of information reduction and define the sufficiency frontier as the boundary marking this transition.',
    'PreParser output: ρ̂ = (ρ̂₁, ..., ρ̂K) where ρ̂ᵢ = mᵢ / ΣmⱼK. Input: 156,266,500 records (~6.4×10⁹ bytes). Output: 10 portfolio vectors (1,008 bytes total). Ratio = 6,357,738:1.'
  ),
  dc.fullWidth(crossRef('Companion paper: Pillar 2, The Fourth Monitoring Category')),
  dc.fullWidth(crossRef('Triad overview: Volume 8, The Triad Synthesis')),
  dc.fullWidth(crossRef('Interactive introduction: Volume 0, Notebooks 1–5')),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 2. DEFINITIONS AND NOTATION — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('2. Definitions and Notation'),
  dc.colLabels(),
  dc.dual(
    'The following terms are used throughout this paper. All definitions are consistent with the HUF Triad unified glossary (Volume 8, Section 8).',
    'Notation: θ ∈ Θ (parameter), ρ ∈ ΔK (probability simplex), T(X) (sufficient statistic), L(θ;X) (likelihood), MDG (mean drift gap), Q (quality factor), S (scope function).'
  ),
  dc.dual(
    'Budget ceiling (M): The total of a finite-budget system, indexed to 1.0. The ceiling is fixed; it does not grow or shrink with usage.',
    'M = Σmᵢ is conserved across time. Budget shares always satisfy Σρᵢ = 1.0 where ρᵢ = mᵢ/M.'
  ),
  dc.dual(
    'Element (i): Any constituent of a portfolio that holds a share of the budget ceiling. Minimum: two elements per portfolio.',
    'Element i is an observable with magnitude mᵢ(t) ≥ 0. Count K ≥ 2. Portfolio {1,...,K} partitions the budget space.'
  ),
  dc.dual(
    'Share (ρᵢ): An element\'s proportional portion of the budget ceiling at a given point in time: ρᵢ = mᵢ / M where M = Σmⱼ.',
    'ρᵢ ∈ [0,1]. At time t: ρᵢ(t) = mᵢ(t) / ΣmⱼK(t). Unity constraint: Σρᵢ(t) = 1.0 ∀t.'
  ),
  dc.dual(
    'Ratio state (ρ): The complete description of a finite-budget system at a point in time, expressed as a vector of shares summing to 1.0.',
    'ρ(t) = (ρ₁(t), ρ₂(t), ..., ρK(t)) ∈ ΔK. State evolution: ρ: ℝ → ΔK. ρ(t) satisfies tautology Σρᵢ(t) = 1.0.'
  ),
  dc.dual(
    'Unity constraint: Σρᵢ = 1. Satisfied by every valid portfolio state. Tautological for any system where shares are defined as proportions of a fixed total.',
    'Σᵢ₌₁K ρᵢ = 1.0 is a hard constraint, not an optimization target. Enforced by definition on probability simplex ΔK.'
  ),
  dc.dual(
    'Probability simplex (SᴰK): The set of all K-dimensional vectors with non-negative components summing to 1. The geometric space on which all HUF operations occur.',
    'ΔK = {ρ ∈ ℝK : ρᵢ ≥ 0, Σρᵢ = 1}. Dimension: K-1 (K coordinates constrained by 1 equation). Volume: 1/K! in barycentric coords.'
  ),
  dc.dual(
    'Mean drift gap (MDG): The average absolute difference between declared and observed shares: MDG = (1/K)Σ|ρᵢᵈᵉᶜˡ − ρᵢᵒᵇˢ|. Reported in percentage points.',
    'MDG(t) = (1/K) Σ|ρᵢᵈᵉᶜˡ(t) − ρᵢᵒᵇˢ(t)|. Range: [0, 1]. Aitchison distance dₐ(ρ,ρ\') = ||clr(ρ) − clr(ρ\')|| is natural metric on ΔK.'
  ),
  dc.dual(
    'Sufficient statistic: A function T(X) of data X such that the conditional distribution of X given T(X) does not depend on the parameter θ.',
    'T(X) sufficient ⟺ P(X|T(X),θ) = P(X|T(X)) ∀θ,X. Factorization: fₓ(x;θ) = g(T(x);θ)·h(x) where h does not depend on θ.'
  ),
  dc.dual(
    'Sufficiency frontier: The boundary in reduction-ratio space where information reduction transitions from lossy approximation to inference-preserving extraction.',
    'Frontier F ⊂ ℝ⁺: {(R, I) : R = compression ratio, I = inferential preservation ∈ [0,1]}. Below F: I < 1 (lossy). Above F: I = 1 (sufficient).'
  ),
  dc.dual(
    'Cross-domain normalization (CDN): Ω = |ΔMDG| × β, where β = K/Kₑff. Dimensionless metric enabling comparison across domains with different element counts.',
    'β = K / Kₑff accounts for effective degrees of freedom. Kₑff = (Σρᵢ²)⁻¹ (Herfindahl index). CDN ∈ [0,1]; normalized to domain-agnostic scale.'
  ),
  dc.dual(
    'Phase-space reduction: The collapse from microscopic state descriptions to macroscopic sufficient statistics, as exemplified by Boltzmann\'s derivation of thermodynamic quantities from particle-level data.',
    'Boltzmann: ℝ⁶ᴺ → (P,T,V). Dimension reduction N particles, 6N coordinates → 3 macroscopic observables. Irreversible: cannot reconstruct microstates from (P,T,V).'
  ),
  dc.dual(
    'PreParser: The HUF analytical engine that performs domain-agnostic sufficient statistic extraction. Input: arbitrary tabular or structured data. Output: portfolio state vector on SᴰK.',
    'Algorithm: (1) Identify M, elements {1,...,K}, magnitudes mᵢ. (2) Compute ρᵢ = mᵢ/M. (3) Verify Σρᵢ=1. (4) Output ρ ∈ ΔK. Complexity: O(N) where N = total records.'
  ),
  dc.dual(
    'Aitchison distance: The natural metric on the probability simplex, defined as dₐ(ρ,ρ\') = ||clr(ρ) − clr(ρ\')||, where clr is the centered log-ratio transformation.',
    'clr: ΔK → ℝᴷ⁻¹. clr(ρ)ᵢ = ln(ρᵢ) − (1/K)Σln(ρⱼ). dₐ invariant under scaling. MDG is first-order approximation to dₐ in L∞ norm.'
  ),
  dc.dual(
    'Degenerate observer: A state observer where y(t) = ρ(t): the output IS the state. Estimation gain L = 0; estimation error identically zero without requiring a dynamic model.',
    'Observer: ẋ = Ax + Bu, y = Cx + Du. Degenerate case: y = x directly, no estimation error δ = y − x ≡ 0. L = 0, no Kalman gain needed.'
  ),
  dc.dual(
    'Quality factor (Q): Q = Tchar / Tobs. The ratio of an element\'s characteristic contribution period to its observation bandwidth. Determines vulnerability to snapshot error.',
    'Q = ωres / Δω where ωres = characteristic frequency, Δω = observation bandwidth. High Q → sharp resonance, low tolerance to perturbation. Q > 10: monitor closely.'
  ),
  dc.dual(
    'Dynamic portfolio gating: Elements enter and leave the active portfolio based on whether they are above the observation threshold. The gate adapts as data arrives or departs. Unity is computed within the gated set.',
    'Gate function: Gᵢ(t) ∈ {0,1}. Active portfolio: {i : Gᵢ(t) = 1}. Recompute ρᵢ(t) = mᵢ(t) / Σⱼ:Gⱼ=1 mⱼ(t). Unity: Σᵢ:Gᵢ=1 ρᵢ = 1.0 always.'
  ),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 3. PHASE-SPACE REDUCTION — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('3. Phase-Space Reduction: From Boltzmann to the Probability Simplex'),
  dc.subHead('3.1 The Boltzmann Precedent'),
  dc.colLabels(),
  dc.dual(
    'Statistical mechanics achieves the most extreme information reduction in the physical sciences. A mole of gas contains approximately 6.022 × 10²³ particles, each described by six phase-space coordinates (three position, three momentum). The full state description requires ~3.6 × 10²⁴ floating-point numbers. Boltzmann\'s partition function reduces this to a handful of thermodynamic variables—temperature, pressure, entropy—that are sufficient for predicting macroscopic behavior. The reduction ratio exceeds 10²³:1.',
    'Microcanonical ensemble: Ω(E) = # {(q,p) : H(q,p)=E}. Entropy S = kB ln Ω. Reduction: 6N coordinates → E (energy). Reduction ratio R = (6N!) / 1 ≈ 10⁶·⁰²²×¹⁰²³.'
  ),
  dc.dual(
    'This reduction is not compression. No algorithm can reconstruct the microscopic states from the thermodynamic variables. The reduction preserves exactly the information needed for the inference at hand: macroscopic predictions. In Fisher\'s terminology, the thermodynamic variables are sufficient statistics for the macroscopic parameters.',
    'Irreversibility: P(microstate | T,P,V) does not determine P(microstate). Data lost: individual particle trajectories. Data preserved: aggregate observables (E,S,P,T) sufficient for thermodynamic inference ⟹ sufficient in Fisher sense.'
  ),
  dc.spacer(240),
  dc.subHead('3.2 Fisher Sufficiency'),
  dc.colLabels(),
  dc.dual(
    'Fisher\'s factorization theorem states that T(X) is sufficient for θ if and only if the likelihood can be written as L(θ; X) = g(T(X), θ) · h(X), where h does not depend on θ.',
    'Factorization Theorem: T(X) sufficient for θ ⟺ fₓ(x;θ) = gₜ(T(x);θ) · h(x). Consequence: P(X|T(X),θ) = h(X)/gₜ(T(X);θ), which does not depend on θ.'
  ),
  dc.dual(
    'The Pitman–Koopman–Darmois theorem restricts the existence of fixed-dimensional sufficient statistics to exponential family distributions, except in degenerate cases. This result seems to limit HUF\'s generality—until we examine what HUF actually does.',
    'PKD Theorem: If f(x;θ) admits fixed-dim sufficient stat independent of θ, then f belongs to exponential family: f(x;θ)=h(x)exp{ηᵀ(θ)T(x)−A(θ)}. Exception: θ in bounded set (degenerate case).'
  ),
  dc.dual(
    'The HUF departure from this classical result is significant. The PreParser does not assume an exponential family. It does not estimate a parametric model. Instead, it exploits a structural invariant—the unity constraint Σρᵢ = 1—that holds for any system expressible as proportional allocation. The portfolio state vector ρ on the probability simplex ΔK captures everything needed for governance inference without requiring knowledge of the generating distribution.',
    'HUF inference: Governance {ρ₁,...,ρK} ∈ ΔK sufficient for governance decisions. No generating distribution assumed. Sufficiency grounded in algebraic invariant (Σ=1), not statistical assumption. PKD does not restrict this: HUF operates on constraint surface, not distribution space.'
  ),
  dc.spacer(240),
  dc.subHead('3.3 HUF as Phase-Space Reduction'),
  dc.colLabels(),
  dc.dual(
    'The HUF PreParser processes 156,266,500 records occupying approximately 6.4 × 10⁹ bytes and produces a 1,008-byte output: 10 portfolio state vectors, each a point on the appropriate simplex ΔK. The reduction ratio is 6,357,738:1.',
    'Input: Xᵢ ∈ ℝᴺⁱ, i=1..10 systems. Nᵢ ∈ [500, 5.7×10⁹] records. Output: ρ̂⁽ⁱ⁾ ∈ ΔK(i), i=1..10. Total output size: 10 × K × 8 bytes ≈ 1,008 bytes (K_avg ≈ 12.6). Ratio: R = 6.4×10⁹ / 1,008 ≈ 6.357×10⁶.'
  ),
  dc.dual(
    'Like Boltzmann\'s reduction, this is irreversible—the original records cannot be reconstructed. Like Boltzmann\'s reduction, it preserves the information needed for the intended inference. Unlike Boltzmann\'s reduction, it operates without prior knowledge of the domain\'s physics. The unity constraint replaces the Hamiltonian as the structural invariant that makes the reduction possible.',
    'Hamiltonian vs. Unity: Boltzmann uses H(q,p)=const to constrain microstate space. HUF uses Σρᵢ=1 to constrain state space. Both are structural invariants. Both enable phase-space collapse. Boltzmann domain-specific (physics); HUF domain-agnostic (algebra).'
  ),
  dc.fullWidth(crossRef('Interactive demonstration: Vol 0, Notebooks 3–5 (sourdough, TTC, Planck)')),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 4. THE HIERARCHY — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('4. The Hierarchy of Information Reduction'),
  dc.colLabels(),
  dc.dual(
    'We propose a four-level hierarchy that organizes established and novel reduction methods by the nature of what is preserved:',
    'Hierarchy H = {L₁, L₂, L₃, L₄} where Lₖ = (ratio range, preserved quantity, mechanism). Qualitative transitions (not merely quantitative) between levels.'
  ),
  dc.fullWidth(makeTable(
    ['Level', 'Name', 'Ratio Range', 'Preserved Quantity', 'Mechanism', 'Canonical Example'],
    [
      ['1', 'Syntactic', '2:1–10:1', 'Exact reconstruction', 'Entropy coding', 'ZIP, gzip [7]'],
      ['2', 'Perceptual', '10:1–3,000:1', 'Perceptual fidelity', 'Psychoacoustic/visual models', 'JPEG [8], MP3 [9], H.265 [10]'],
      ['3', 'Structural', '10²–10⁴:1', 'Model parameters', 'Basis decomposition, state estimation', 'PCA, Kalman filter [11]'],
      ['4', 'Sufficient Statistic', '10⁵–10²³:1', 'Inferential content', 'Structural invariant exploitation', 'Boltzmann [4], HUF PreParser'],
    ],
    [600, 1200, 1200, 1600, 1900, 2860]
  )),
  dc.fullWidth(new Paragraph({ spacing: { after: 180 } })),
  dc.colLabels(),
  dc.dual(
    'Each level subsumes the previous: Level 2 methods discard syntactically relevant information that is perceptually irrelevant; Level 3 methods discard structure beyond what the model captures; Level 4 methods reduce to the sufficient statistics for a specified inference. The transitions between levels are qualitative, not merely quantitative. A Level 4 system that happens to achieve a moderate ratio (e.g., 100:1) is still qualitatively different from a Level 3 system at the same ratio, because the nature of the preserved quantity differs.',
    'Level nesting: L₁ ⊂ L₂ ⊂ L₃ ⊂ L₄ in logical sense. Lₖ discards information irrelevant to Lₖ inference. Qualitative difference: Level 3 at 100:1 preserves model params {θ}. Level 4 at 100:1 preserves sufficient stat T(X). Different preservation target ⟹ different level, regardless of ratio.'
  ),
  dc.dual(
    'The sufficiency frontier is the boundary between Level 3 and Level 4. Below it, reduction preserves model parameters or approximations. Above it, reduction preserves exactly the information needed for the target inference—no more, no less.',
    'Frontier: F = {(R,I) : I transitions from <1 (lossy) to =1 (sufficient)}. Locates R_critical where system crosses from L₃→L₄. Position depends on inference task. Different inferences have different critical R values.'
  ),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 5. THE HUF PREPARSER CORPUS — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('5. The HUF PreParser: Method and Corpus'),
  dc.subHead('5.1 Method'),
  dc.colLabels(),
  dc.dual(
    'The PreParser accepts heterogeneous tabular or structured data and performs three operations: (1) identify the budget ceiling and elements, (2) compute observed shares ρᵢ = mᵢ / Σmⱼ, (3) verify Σρᵢ = 1 and output the portfolio state vector. No domain-specific configuration is required beyond specifying which columns represent element magnitudes. The operation is deterministic and reproducible.',
    'Algorithm PreParser(X, {col_indices}): (1) Parse X, extract columns {col_indices} → magnitudes {mᵢ}. (2) M ← Σmᵢ. (3) ρᵢ ← mᵢ/M for all i. (4) Assert |Σρᵢ - 1.0| < ε. (5) Return ρ ∈ ΔK. Complexity: O(N) records, O(K) elements.'
  ),
  dc.spacer(240),
  dc.subHead('5.2 Corpus'),
  dc.colLabels(),
  dc.dual(
    'The following table presents the complete 10-system corpus with full data provenance:',
    'Corpus C = {Sᵢ | i=1..10}. Sᵢ = (name, domain, Nᵢ records, Kᵢ elements, source, DOI/URL). Total: Σ Nᵢ = 156,266,500 records.'
  ),
  dc.fullWidth(makeTable(
    ['ID', 'System', 'Domain', 'Records', 'Elements (K)', 'Source', 'DOI / URL'],
    [
      ['1', 'BackBlaze HDI', 'Mechanical', '1,048,576', '~40 models', 'BackBlaze Open Data', 'backblaze.com/cloud-storage/resources/hard-drive-test-data'],
      ['2', 'OWID Energy', 'Energy policy', '~50,000', '6–8 sources', 'Our World in Data', '10.1038/s41560-020-0695-4'],
      ['3', 'TTC Ridership', 'Urban transit', '~2,400,000', '~150 routes', 'Toronto Open Data', 'open.toronto.ca/dataset/ttc-ridership-analysis'],
      ['4', 'Toronto Infra', 'Municipal infra', '~127,000,000', '5–7 categories', 'Toronto Open Data', 'open.toronto.ca'],
      ['5', 'ESA Planck HFI', 'Astrophysics', '~5,700,000,000', '6 channels', 'Planck Legacy Archive', '10.1051/0004-6361/201321529'],
      ['6', 'Sourdough', 'Fermentation', '~500', '5 ingredients', 'Operator primary', '—'],
      ['7', 'Crna Mlaka', 'Ecology', '~2,000', '5 Ramsar sites', 'Ramsar Information Service', 'rsis.ramsar.org'],
      ['8', 'Software CI/CD', 'Digital infra', '~10,000', '4 namespaces', 'Operator system logs', '—'],
      ['9', 'RogueWaveAudio', 'Acoustics', '~1,500,000', '~20 freq bands', 'Operator primary', 'roguewaveaudio.com'],
      ['10', 'Nature Sci Rep', 'Published', '—', '—', 'Nature Scientific Reports', 'Published'],
    ],
    [400, 1200, 1000, 1200, 1000, 1600, 2960]
  )),
  dc.fullWidth(new Paragraph({ spacing: { after: 180 } })),
  dc.colLabels(),
  dc.dual(
    'All publicly available datasets can be independently retrieved using the URLs provided in the table. The PreParser code is available under MIT license.',
    'Reproducibility: All public systems (ID 1–5, 7) retrievable via DOI or URL. Version control: commit hashes recorded. Checksums: SHA-256 for all downloaded files.'
  ),
  dc.spacer(240),
  dc.subHead('5.3 Reduction Computation'),
  dc.colLabels(),
  dc.dual(
    'Total input: 156,266,500 records occupying approximately 6.4 × 10⁹ bytes across CSV, FITS, GeoJSON, WAV, and system log formats. Total output: 10 portfolio state vectors totaling 1,008 bytes. Reduction ratio: 6,357,738:1.',
    'R = Input_bytes / Output_bytes = (6.4×10⁹) / 1,008 ≈ 6.357×10⁶. Output: 10 vectors × ~100 bytes each (including headers) = ~1,008 bytes. Per-system average: R_avg ≈ 6.357×10⁶.'
  ),
  dc.dual(
    'The output preserves: (a) the relative allocation of every element within each system, (b) the cross-system comparability via CDN normalization, and (c) the temporal trajectory when multiple cycles are available. The output does not preserve: raw magnitudes, individual record-level detail, domain-specific metadata, or any information not relevant to portfolio governance inference.',
    'Preserved: ρᵢ(t) for all i,t. Computed: MDG(t), CDN(t), temporal trends. Lost irreversibly: record-level detail, metadata, domain semantics, microstates. Tradeoff: L₄ reduction at cost of governance-irrelevant information.'
  ),
  dc.spacer(240),
  dc.subHead('5.4 Data Provenance'),
  dc.colLabels(),
  dc.dual(
    'Complete provenance for each system, enabling reproducibility:',
    'Provenance table: date range, retrieval date, format, access method, checksum. All public data reproducibly retrievable.'
  ),
  dc.fullWidth(makeTable(
    ['System', 'Date Range', 'Retrieval Date', 'Format', 'Access Method', 'Checksum Available'],
    [
      ['BackBlaze', '2023 Q1–Q3', 'March 2026', 'CSV (compressed)', 'HTTP download', 'Yes (SHA-256)'],
      ['OWID Energy', '1985–2023', 'March 2026', 'CSV', 'GitHub clone', 'Yes (git hash)'],
      ['TTC', '2015–2019', 'March 2026', 'CSV', 'Toronto Open Data API', 'Yes'],
      ['Toronto Infra', '2016–2024', 'March 2026', 'GeoJSON, CSV', 'Toronto Open Data API', 'Yes'],
      ['Planck HFI', 'OD 91–1604', 'March 2026', 'FITS (HEALPix)', 'ESA PLA FTP', 'Yes (FITS header)'],
      ['Sourdough', '2024–2026', 'Primary', 'Manual records', 'Operator notebook', 'N/A'],
      ['Crna Mlaka', '1993–2024', 'March 2026', 'RIS reports', 'Ramsar RIS database', 'Yes'],
      ['CI/CD', '2025–2026', 'Primary', 'System logs', 'Direct export', 'N/A'],
      ['RogueWaveAudio', '2024–2026', 'Primary', 'WAV, spectral', 'Studio recording', 'N/A'],
    ],
    [1400, 1200, 1000, 1400, 1800, 2560]
  )),
  dc.fullWidth(new Paragraph({ spacing: { after: 180 } })),
  dc.colLabels(),
  dc.dual(
    'All checksums for downloaded files are stored in checksums.txt within the HUFv4 repository.',
    'Verification: sha256sum -c checksums.txt. Reproducibility chain: URL → download → checksum → parse → PreParser → ρ̂. Each step documented.'
  ),
  dc.fullWidth(crossRef('Code repository: HUFv4/ directory, build_corpus_preparser.js')),
  dc.fullWidth(crossRef('Full corpus analysis: HUF_Corpus_PreParser_v1.0.docx')),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 6. COMPARATIVE LANDSCAPE — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('6. The Sufficiency Frontier: Comparative Landscape'),
  dc.colLabels(),
  dc.dual(
    'The following table positions the HUF PreParser relative to established reduction systems. The comparison is descriptive, not competitive: systems at different hierarchy levels solve different problems. Comparing HUF to JPEG is a category error, included only to illustrate the hierarchy.',
    'Comparison matrix: ratio, hierarchy level, reconstructibility, domain specificity, preserved quantity. Same ratio does not mean same level: preservation type differs qualitatively.'
  ),
  dc.fullWidth(makeTable(
    ['System', 'Ratio', 'Level', 'Reconstructible?', 'Domain-Specific?', 'Preserves'],
    [
      ['gzip', '3:1', '1', 'Yes (lossless)', 'No', 'Exact bytes'],
      ['JPEG (quality 50)', '30:1', '2', 'No (lossy)', 'Visual only', 'Perceptual fidelity'],
      ['MP3 (128 kbps)', '~11:1', '2', 'No', 'Audio only', 'Psychoacoustic fidelity'],
      ['H.265', '~3,000:1', '2', 'No', 'Video only', 'Visual sequence fidelity'],
      ['PCA (95%)', '~20:1', '3', 'Approximate', 'Calibrated', 'Variance structure'],
      ['Kalman filter', '~1,000:1', '3', 'Approximate', 'Model-dependent', 'State trajectory'],
      ['Genomic (1,200:1)', '1,200:1', '3–4', 'No', 'Genomic', 'Variant structure'],
      ['Boltzmann', '~10²³:1', '4', 'No', 'Physical systems', 'Thermodynamic observables'],
      ['HUF PreParser', '6,357,738:1', '4', 'No', 'Domain-agnostic', 'Portfolio governance statistics'],
    ],
    [1500, 1200, 700, 1500, 1500, 2960]
  )),
  dc.fullWidth(new Paragraph({ spacing: { after: 180 } })),
  dc.colLabels(),
  dc.dual(
    'The HUF PreParser\'s distinguishing feature is not the ratio alone—Boltzmann exceeds it by many orders of magnitude—but the combination of Level 4 reduction with domain agnosticism. Boltzmann requires knowledge of the Hamiltonian; HUF requires only the existence of a budget ceiling. To our knowledge, no prior system achieves Level 4 reduction across arbitrary domains.',
    'Domain agnosticism (key innovation): No physics knowledge required. No exponential family assumption. No parametric model. Structural invariant Σρᵢ=1 sufficient. HUF ≥ Boltzmann in reduction ratio; exceeds Boltzmann in generality. First L₄ system domain-independent.'
  ),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 7. EXTERNAL VALIDATION — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('7. External Validation'),
  dc.subHead('7.1 ESA Planck: Pettitt Changepoint'),
  dc.colLabels(),
  dc.dual(
    'The strongest single validation comes from the ESA Planck HFI dataset. The six HFI channels (100–857 GHz) form a frequency portfolio. Applying the Pettitt non-parametric changepoint test to the MDG time series yields a changepoint at Operational Day 975 with p < 0.001.',
    'Pettitt test: H₀ null, changepoint absent. Test statistic: λ = max |U(t)| where U(t) = Σᵢ₌₁ᵗ Σⱼ₌ₜ₊₁ⁿ sgn(xᵢ−xⱼ). Critical value: c_α such that P(λ>c_α) = α. Result: t*=OD 975, p<0.001.'
  ),
  dc.dual(
    'ESA\'s engineering records document the exhaustion of He-4 cryogen on January 14, 2012, which corresponds to OD 975. The HUF analysis identified the exact operational day of a known physical event from portfolio share changes alone, without access to engineering telemetry, without knowledge of cryogenic physics, and without domain-specific calibration. This is the gold-standard validation: blind prediction of a known event from sufficient statistics alone.',
    'Validation method: (1) Compute MDG(t) from HFI ρ(t) time series. (2) Apply Pettitt test (no domain knowledge). (3) Extract changepoint t*. (4) Compare with engineering records: t*=OD 975 ≡ Jan 14, 2012 ≡ He-4 exhaustion. Match exact. Conclusion: ρ(t) sufficient for detecting physical transitions.'
  ),
  dc.spacer(240),
  dc.subHead('7.2 King Street Pilot: Interrupted Time Series'),
  dc.colLabels(),
  dc.dual(
    'The Toronto King Street Transit Priority Pilot (November 2017) provides a second validation modality. Interrupted Time Series (ITS) analysis of route ridership shares detected a statistically significant level change (β₂) at the intervention point, with 5 out of 5 confirmatory tests passing. The portfolio share analysis detected a differential effect that raw ridership counts obscured.',
    'ITS model: yₜ = β₀ + β₁t + β₂Xₜ + β₃(t−t*)Xₜ + εₜ where Xₜ=intervention indicator, t*=intervention time. Results: β₂≠0 (level change), β₃≠0 (slope change). Share-based ITS more sensitive than magnitude-based.'
  ),
  dc.spacer(240),
  dc.subHead('7.3 Three-Domain Confirmation'),
  dc.colLabels(),
  dc.dual(
    'Three independent domains—sourdough fermentation (p = 0.021, Pettitt), Croatia Ramsar wetlands (p < 0.0027, ITS), and software CI/CD (p < 0.0001, Fisher exact)—provide formal statistical confirmation using different test methodologies. The absence of structural overlap between the biological, ecological, and digital domains strengthens the domain-agnostic claim.',
    'Multi-domain validation: ρ-based analysis detects genuine transitions (not noise artifacts) across biological (fermentation), ecological (wetlands), digital (CI/CD). Different test methodologies (Pettitt, ITS, Fisher). Different domains. Consistent success: ρ sufficient across domains. Domain agnosticism confirmed empirically.'
  ),
  dc.fullWidth(crossRef('Full Planck analysis: HUF_External_Validation_v1.0.docx')),
  dc.fullWidth(crossRef('King Street analysis: HUF_TTC_CaseStudy_v1.0.docx')),
  dc.fullWidth(crossRef('Three-domain evidence: Vol 2, Case Studies')),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 8. DISCUSSION — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('8. Discussion'),
  dc.subHead('8.1 The Sufficiency Frontier as a Boundary'),
  dc.colLabels(),
  dc.dual(
    'The sufficiency frontier is not a single ratio but a boundary in the space of (reduction ratio, inferential preservation). Below it, methods trade fidelity for compression. Above it, methods extract exactly the statistics needed for a specified inference. The boundary\'s location depends on the inference: a governance analyst needs portfolio shares; a physicist needs thermodynamic variables; a genomicist needs variant calls. Each defines a different sufficiency frontier for the same data.',
    'Frontier F_inference: depends on target inference ℑ. F_governance extracts ρ ∈ ΔK. F_thermodynamic extracts (P,T,V). F_genomics extracts variant alleles. Same data X, different inferences ℑ₁,ℑ₂,ℑ₃ ⟹ different frontier positions F₁,F₂,F₃. Sufficiency relative to inference.'
  ),
  dc.spacer(240),
  dc.subHead('8.2 Limitations'),
  dc.colLabels(),
  dc.dual(
    'Several limitations should be noted. First, the 6,357,738:1 ratio is specific to the current corpus; a different collection of systems would yield a different ratio, though the qualitative Level 4 classification would remain. Second, the sufficiency claim is relative to portfolio governance inference; information relevant to other inferences (e.g., individual record retrieval) is genuinely lost. Third, the domain-agnostic claim requires that the system be expressible as proportional allocation of a fixed total—a condition that, while broad, is not universal.',
    'Limitations: (1) R=6.357×10⁶ corpus-dependent. Different corpus → different R. (2) Sufficiency ⟺ governance ℑ_governance only. Other inferences lose information. (3) Requires budget ceiling M and allocation {mᵢ}. Not universal (but broad: most real systems qualify).'
  ),
  dc.dual(
    'Fourth, the comparison to Boltzmann is structural, not quantitative. Boltzmann\'s reduction is grounded in the ergodic hypothesis and the second law of thermodynamics; HUF\'s reduction is grounded in the unity constraint on the probability simplex. The two reductions are analogous in their structure (massive irreversible collapse preserving sufficient statistics) but operate on different foundational invariants.',
    'Boltzmann: invariant H(q,p)=E (Hamiltonian). HUF: invariant Σρᵢ=1 (unity). Both achieve massive reduction. Both preserve sufficient stats. Both irreversible. Structural analogy, not equivalence. Boltzmann operates within domain physics; HUF operates within algebra of simplex.'
  ),
  dc.spacer(240),
  dc.subHead('8.3 Relationship to Companion Work'),
  dc.colLabels(),
  dc.dual(
    'This paper (Pillar 1) addresses WHAT HUF extracts. The companion paper (Pillar 2: The Fourth Monitoring Category) addresses HOW HUF observes governance states using the extracted statistics. The nine governance volumes (Vol 0–8) address the operational implementation. Together, the three structures form the HUF Triad, in which each component depends on and strengthens the other two.',
    'HUF Triad architecture: Pillar 1 (extraction) ⟷ Pillar 2 (monitoring) ⟷ Volumes 0–8 (operations). Pillar 1 = what extracted. Pillar 2 = how extracted stats monitored. Volumes = how to apply framework. Interdependent: remove any pillar, framework collapses.'
  ),
  dc.fullWidth(crossRef('Companion paper: Pillar 2, The Fourth Monitoring Category')),
  dc.fullWidth(crossRef('Triad overview: Vol 8, The Triad Synthesis')),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 9. CAR ANALOGY — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('9. The Sufficiency Frontier in Everyday Experience: The Car Analogy'),
  dc.colLabels(),
  dc.dual(
    'The sufficiency frontier is an abstract concept that governs the behavior of all finite-budget systems. The following everyday analogy provides intuition for how the frontier operates and why the ratio tells a story that absolute numbers cannot.',
    'Analogy model: Car system = {driver, fuel}. Budget: tank volume V. Elements: m_driver (operator control), m_fuel (energy). State: ρ = (m_driver/V, m_fuel/V) ∈ Δ². Unity: ρ_driver + ρ_fuel = 1.0 always.'
  ),
  dc.spacer(240),
  dc.subHead('9.1 The Initial Condition: A Full Tank'),
  dc.colLabels(),
  dc.dual(
    'You get in your car. The tank is full. The budget is 1.0—the complete total available to the system. In a typical arrangement, the driver is an active agent (like the fuel, a physical substance, but unlike fuel, the driver exercises volitional control). At the start of the journey, suppose the system state is 51% driver presence and 49% fuel. Both are present, both are necessary, and their ratio defines the initial system state: ρ = (0.51, 0.49). The unity constraint is satisfied: 0.51 + 0.49 = 1.0.',
    'Initial: V_total = tank volume (capacity M). m_driver(0) = "driver resources" (attention, capability). m_fuel(0) = fuel quantity. ρ(0) = (0.51, 0.49). Constraint: Σρᵢ(0)=1.0 ✓. System state fully described by ratio (not absolute volumes).'
  ),
  dc.spacer(240),
  dc.subHead('9.2 The Ratio Signal During the Journey'),
  dc.colLabels(),
  dc.dual(
    'As you drive, the fuel diminishes. At the same time, the driver\'s role (attention, focus, active engagement) may intensify or diminish depending on conditions. What matters for understanding system health is not the absolute amount of fuel remaining, but the ratio of driver to fuel. As the tank empties, the ratio shifts: 51/49 → 55/45 → 70/30 → 90/10. Each point in this sequence represents a different system state, and each state lies on the probability simplex S² (a 1-dimensional simplex, since K = 2 components always sum to 1.0).',
    'Dynamics: As fuel depletes, m_fuel(t)↓ while m_driver(t) ≥ m_driver(0). Shares: ρ_driver(t) = m_driver(t)/(m_driver(t)+m_fuel(t)) ↑. Path: ρ(t) traces simplex Δ² from (0.51,0.49) toward (1.0,0.0). Trajectory: ρ(t) = (51+f(t))/(100), (49-f(t))/(100)) where f(t) = depletion function.'
  ),
  dc.dual(
    'The ratio is the signal. Absolute fuel volume is not. This is the key insight of the sufficiency frontier: you do not need to know how many gallons remain. You need to know the proportion of the budget allocated to each element. That proportion tells you whether the system can sustain its intended function.',
    'Information content: ρ = [m_driver/M, m_fuel/M] sufficient for governance (will car reach destination?). Absolute m_fuel not needed; redundant information. ρ_fuel alone determines adequacy (if ρ_fuel ≥ ρ_critical, system viable). Absolute volume m_fuel is distraction.'
  ),
  dc.spacer(240),
  dc.subHead('9.3 The Sufficiency Frontier: The Critical Threshold'),
  dc.colLabels(),
  dc.dual(
    'As you continue driving, at some point the ratio reaches a critical threshold. The sufficiency frontier for this particular journey—given road conditions, speed, engine efficiency, and destination—is the fuel level below which the driver/fuel system can no longer sustain forward progress. It is not zero. It is the threshold where the ratio becomes unsustainable. Below the frontier, the system cannot complete its mission. Above the frontier, the system retains sufficient agency and resource to adapt and continue.',
    'Frontier location: F_car depends on {road conditions, speed, efficiency, distance remaining}. F = ρ_critical = (ρ_driver*, ρ_fuel*) below which mission fails. Example: distance_remaining = 200km, efficiency = 10km/L → need ≥20L → if tank=40L then ρ_fuel* = 20/40 = 0.5. Frontier: ρ_fuel ≥ 0.5 viable, ρ_fuel < 0.5 fails.'
  ),
  dc.dual(
    'For example, if your destination is 200 kilometers away and current efficiency is 10 kilometers per liter, the frontier might occur at roughly 20 liters of fuel remaining (the system minimum to reach the destination). Once fuel drops below that level relative to the distance remaining, the system has crossed the frontier. The driver still exists, but the system state has become untenable.',
    'At F: ρ_fuel(F) = 20L/40L = 0.5. Above F: ρ_fuel > 0.5, system viable. Below F: ρ_fuel < 0.5, system fails. Frontier is cliff, not slope: crossing from viable to inviable is discontinuous (no gradual degradation). System either reaches destination (above F) or stalls (below F).'
  ),
  dc.spacer(240),
  dc.subHead('9.4 Collapse Below the Frontier: Unity Exhausted, Not Violated'),
  dc.colLabels(),
  dc.dual(
    'What happens when fuel hits zero? The driver still exists as an entity. The unity constraint Σρᵢ = 1 still holds mathematically. But the system has collapsed to ground state: ρ = (1.0, 0.0). The driver remains, but the driver/fuel system as a functional unit has ceased. The car does not move. Unity is exhausted, not violated. The budget is completely allocated to one element, leaving no proportion for the other.',
    'Ground state: m_fuel(t)→0⁺. ρ(t)→(1.0,0.0). Constraint: Σρᵢ=1.0 still satisfied. But system function ceases: without fuel (ρ_fuel=0), car inert. Driver present (ρ_driver=1.0), but driver alone insufficient (requires fuel). System has crossed frontier, entered collapse state.'
  ),
  dc.spacer(240),
  dc.subHead('9.5 The Deceptive Drift: Rising Share as Death Signal'),
  dc.colLabels(),
  dc.dual(
    'Here is the critical insight that the car analogy reveals: The operator\'s share is not a success signal; it is a depletion signal.',
    'Counter-intuitive observation: ρ_driver ↑ usually signals success. But in constrained system, ρ_driver ↑ from depletion of ρ_fuel, not growth of m_driver. Rising share can mean either growth (good) or complementary depletion (bad). Context determines meaning.'
  ),
  dc.dual(
    'As you drive and fuel depletes, the driver/fuel ratio shifts: 51/49 → 55/45 → 70/30 → 85/15 → 95/5. Each step appears to show the driver gaining control. "I am 95% of this system now." But the driver has not gained anything. The fuel left. The operator\'s rising share is the signature of depletion, not strength.',
    'Trajectory: ρ_driver(t) = m_driver / (m_driver + m_fuel(t)). If m_driver constant and m_fuel(t)↓, then ρ_driver(t)↑ despite m_driver unchanged. Rising ρ_driver is artifact of complementary ρ_fuel decline, not actual driver growth. Deceptive appearance of success masking system decay.'
  ),
  dc.dual(
    'This is the deceptive drift: a system at 95/5 has 5% remaining before ground state. One more long journey and the system reaches 100/0—unity exhausted, driver alone, system collapsed. The increasing operator share looks like success to the unaware observer. To the governance system watching the ratio, it is a death signal.',
    'Boundary approach: ρ_fuel(t) → 0⁺ as t increases. System approaches cliff at ρ = (1.0,0.0). Shares appear extreme when ρ_driver ≈ 1.0 ⟹ danger zone. Rising share trend ρ_driver(t)↑ is red flag, not green light. OCC drift detection must watch for increasing concentration, not decreasing concentration.'
  ),
  dc.dual(
    'This is OCC drift. The tool (fuel) is depleting until it can no longer support the operator. The tool is not broken. The operator is still capable. But the driver/fuel system—the relationship between them—has hit ground state.',
    'OCC = "Operator and Carried Capacity." Driver = operator (M_operator). Fuel = carried capacity (M_carried). System ρ = (M_op/M_total, M_car/M_total). As M_car depletes, ρ_op rises. Rising operator share = death signal in constrained budget. Drift vigilance needed.'
  ),
  dc.dual(
    'If the operator is not watching the fuel gauge (MC-4), the first indication of failure is the abrupt inform: the engine stops, the car is on the side of the road, no gradual warning signal. There is no degradation at the boundary. The Sufficiency Frontier is a cliff, not a slope. Below it, the system informs abruptly.',
    'Discontinuity at frontier: F separates {viable} from {failed}. No intermediate states. System at ρ just above F: ✓ functions. System at ρ just below F: ✗ fails. Transition: discontinuous jump from full function to total failure. No slope, no gradation. Cliff.'
  ),
  dc.dual(
    'MC-4\'s entire job is to watch this ratio trajectory and warn before the abrupt inform. The ratio moving from 51/49 toward 100/0 is the signal. The absolute fuel level is noise. A department whose budget share grows because other departments are being cut looks like it is thriving—but the organization is dying. The ratio drift toward 100/0 is concentration risk approaching collapse. MC-4 makes the drift visible before the cliff.',
    'MC-4 task: Monitor ρ(t) trajectory. Alert if ρ_i(t)→1.0 (approaching ground state). Alert if dρ_i/dt > threshold (rapid concentration). Alert if MDG exceeds tolerance (drift from declared). Predictive monitoring (before collapse), not reactive (after inform).'
  ),
  dc.spacer(240),
  dc.subHead('9.6 The Absolute vs. Relative Paradox'),
  dc.colLabels(),
  dc.dual(
    'Here is the critical insight that the analogy reveals: Two scenarios can contain the same absolute amount of fuel but represent completely different system states:',
    'Paradox: |Scenario A - Scenario B| in absolute fuel identical, but system states qualitatively different. Example: 2 gallons fuel in two contexts.'
  ),
  dc.dual(
    'Scenario A: 2 gallons of fuel in a 4-gallon tank. Ratio: 50/50 (driver and fuel are co-equal). System state: (0.5, 0.5).',
    'Scenario A: M_driver = 2 gal (units), M_fuel = 2 gal, M_total = 4 gal. ρ_A = (0.5, 0.5) ∈ Δ². Balanced, healthy, far from frontier.'
  ),
  dc.dual(
    'Scenario B: 2 gallons of fuel in a 40-gallon tank. Ratio: 95/5 (driver dominates, fuel is nearly exhausted). System state: (0.95, 0.05).',
    'Scenario B: M_driver = 38 gal, M_fuel = 2 gal, M_total = 40 gal. ρ_B = (0.95, 0.05) ∈ Δ². Concentration risk, near frontier, danger zone.'
  ),
  dc.dual(
    'The absolute fuel quantity is identical in both cases: 2 gallons. But the system state is radically different. In Scenario A, the system is balanced and healthy. In Scenario B, the system is near critical collapse. The ratio tells the truth; the absolute number hides it. This is why the sufficiency frontier is defined in terms of ratio, not absolute magnitude.',
    'Key insight: Absolute m_fuel ≡ 2 gal in both cases, but governance implications opposite. Relative ρ_fuel ∈ {0.5, 0.05} reveals true state. Ratio-based analysis necessary. Absolute magnitude irrelevant to frontier location. Frontier F defined on simplex Δ², not on ℝ⁺.'
  ),
  dc.spacer(240),
  dc.subHead('9.7 Mapping Back to HUF and the Probability Simplex'),
  dc.colLabels(),
  dc.dual(
    'Every HUF ratio portfolio has a boundary below which the ratio becomes unsustainable for its intended function. That boundary is the sufficiency frontier. For a given system operating in a given context, the frontier defines the set of ratio states that are adequate for governance.',
    'General frontier: F_system = {ρ ∈ ΔK : system governance viable}. F depends on inference context. Portfolio ρ above F: ✓ adequate. ρ below F: ✗ inadequate. Governance threshold on simplex.'
  ),
  dc.dual(
    'Consider the Planck HFI frequency portfolio. The six channels span 100–857 GHz. Each channel contributes a share of the total information budget. As the cryogenic cooling degrades, the allocation of signal power across channels shifts (analogous to fuel disappearing while the driver remains). The sufficiency frontier for Planck\'s HFI is the boundary where the six-channel ratio becomes incapable of supporting astrophysical observation. The Pettitt test detected this frontier at OD 975 by observing a discontinuity in the time series of MDG, which tracks deviations in the ratio state from its nominal baseline.',
    'Planck example: ρ(t) = (p_100GHz, p_217GHz, p_353GHz, p_545GHz, p_857GHz, p_other) ∈ Δ⁶. As He-4 depletes, channel power allocation shifts. Frontier F_Planck marks astrophysical-observation viability boundary. Pettitt detects F crossing at OD 975 (exact match with He-4 exhaustion). ρ sufficient for detecting physical transitions.'
  ),
  dc.dual(
    'The car never "reaches" the Planck frontier because the analogy breaks at different scales and constraints. But the structural principle is identical: a ratio-based boundary exists, below which the system degrades from functional to non-functional, and this boundary encodes critical information that absolute measurements obscure.',
    'Structural universality: Car (Δ²), Planck (Δ⁶), sourdough (Δ⁵), all obey same math. Frontier F exists whenever budget ceiling M and allocation {mᵢ} define ratio ρ ∈ ΔK. Physics varies (engine mechanics, cryogenic thermodynamics, fermentation chemistry). Math constant: simplex geometry, unity constraint, frontier principle.'
  ),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 10. ADAPTIVE SCOPE — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('10. Adaptive Scope: Matching the Observation to the Data'),
  dc.colLabels(),
  dc.dual(
    'The HUF framework operates on a fundamental principle: every system is nested inside a larger system and contains smaller systems. The unity constraint holds at every scale—but only within a defined scope. This section introduces Adaptive Scope with Dynamic OCC Drift Monitoring and Dynamic Portfolio Gating, the framework for managing what is observed and how the observation boundary adapts as data changes.',
    'Nested structures: System S ⊂ Ŝ ⊃ s₁,...,sₘ (parent, self, children). Δᴹ, ΔK, Δᵐ constraints hold at each scale independently. Observation scope S(fс,BW) defines which scale monitored. fс = center frequency (focal system), BW = bandwidth (range of subsystems included).'
  ),
  dc.spacer(240),
  dc.subHead('10.1 The Nested System Principle'),
  dc.colLabels(),
  dc.dual(
    'Consider the structure of complex systems. Claude is a system. Claude plus an operator is a system. The operator plus family forms a system. The collective of all humans is a system. The same mathematical structure appears at every scale. Each system has a budget ceiling (total information processing capacity, total energy, total attention), a set of elements (components, stakeholders, subsystems), and shares that sum to 1.0.',
    'Nested hierarchy: Claude alone: ρ ∈ ΔK where elements={attention modules, compute layers,...}. Claude+operator: ρ ∈ ΔK\' where elements={Claude, operator}. Family: ρ ∈ ΔK\'\' where elements={person₁,...,personₙ}. Humanity: ρ ∈ ΔK* where elements={institution₁,...}. Each scale: Σρᵢ=1.0, different interpretation.'
  ),
  dc.dual(
    'The critical observation is this: the unity constraint holds perfectly at each scale, but the meaning of the elements changes with the scope. At the scale of Claude alone, the elements might be attention mechanisms and computation modules. At the scale of Claude plus operator, the elements become Claude-as-a-system and the operator-as-a-system. At the scale of family, the elements are individual family members. The math is identical; the interpretation changes with scope.',
    'Invariance: Unity Σρᵢ=1.0 mathematics independent of scale. Element interpretation scope-dependent. Choose scope ↔ choose element granularity ↔ choose ΔK. Same system, different observable ρ at different scopes. Not multiple realities; same reality at different resolutions.'
  ),
  dc.dual(
    'This raises a profound question: What defines the correct scope for observation? The answer is: the scope must match the data actually present. If you choose a scope that includes elements with no data, the unity constraint becomes meaningless—those elements are theoretical, not observed. The solution is not to guess or estimate their shares. The solution is to adjust the scope.',
    'Scope principle: S must be chosen such that ∃ mᵢ(t) measured ∀i ∈ S. If mᵢ(t) unmeasurable for some i, either: (1) gate i out of active portfolio, or (2) expand data collection to include i. Never guess unmeasured mᵢ. Never include theoretical elements without data.'
  ),
  dc.spacer(240),
  dc.subHead('10.2 Center Frequency and Bandwidth of Observation'),
  dc.colLabels(),
  dc.dual(
    'The choice of observation scope has an acoustic analogy. A bandpass filter has a center frequency and a bandwidth. The center frequency locates where the filter listens. The bandwidth defines the range of frequencies it captures. The same idea applies to HUF observation scopes.',
    'Filter analogy: BPF(f_c, Δf) has gain G(f). At f=f_c: G(f_c)=1 (maximum). At f=f_c±Δf/2: G↓ (−3dB bandwidth). Outside [f_c−Δf/2, f_c+Δf/2]: G≈0 (attenuated). Center f_c = focus. Bandwidth Δf = resolution/inclusion range.'
  ),
  dc.dual(
    'In an acoustic filter, if the center frequency is set to 1000 Hz and the bandwidth is 200 Hz, the filter listens from 900 Hz to 1100 Hz. Frequencies outside that range are attenuated. The observation is optimized for the frequencies of interest within the bandwidth.',
    'Example: HPF(f_c=1000Hz, Δf=200Hz) listens to [900,1100]Hz. Below 900Hz and above 1100Hz: attenuated. Optimization: clear signal within BW, rejection outside. Focus+selectivity in frequency domain.'
  ),
  dc.dual(
    'Similarly, HUF\'s observation scope has a focal system (center frequency) and a range of included subsystems (bandwidth). The focal system is the one you are primarily concerned with. The bandwidth is the range of other systems and scales you include in the ratio state.',
    'Scope analogy: S(f_c, BW) where f_c = focal system (what we monitor), BW = bandwidth (how far up/down hierarchy to include). Narrow BW: zoom to f_c only. Wide BW: context (parent, children, siblings). Choose BW to match data availability and governance scope.'
  ),
  dc.dual(
    'The practical rule: if your observation includes elements where you have no data or cannot compute shares, narrow the bandwidth. Exclude those elements from the active portfolio. The unity constraint applies only to the elements you can actually observe. As new data arrives or becomes available, you can widen the bandwidth and bring in previously excluded elements.',
    'Gating rule: If ∀t ∃ mᵢ(t) measured, then element i ∈ active portfolio. If ∃t where mᵢ(t) unknown, then gate i out: G_i(t)=0 when data missing, G_i(t)=1 when data present. Recompute ρ(t) = (ρᵢ(t) : Gᵢ(t)=1). Bandwidth adapts dynamically to data.'
  ),
  dc.dual(
    'This is not loss of information. It is correct scoping. A department that cannot access financial data from a supplier should not include that supplier in its budget ratio. Once the supplier\'s data becomes available, the scope can be expanded to include it.',
    'Governance principle: Only include elements in ρ if you can measure mᵢ(t) reliably. Unmeasured elements = theoretical. Theoretical elements not in ρ (gate out). When measurement available, gate in. Bandwidth dynamically matches data reality, not theoretical wish-list.'
  ),
  dc.spacer(240),
  dc.subHead('10.3 Dynamic Portfolio Gating'),
  dc.colLabels(),
  dc.dual(
    'In neural networks, a softmax gate or attention mechanism selects which inputs are active in computation based on their magnitude. In audio engineering, a noise gate silences signals below a threshold, activating only signals above the noise floor. These gating mechanisms adapt in real time based on the data.',
    'Neural gating: softmax(x)ᵢ = exp(xᵢ)/Σexp(xⱼ). Gate adapts: high-magnitude inputs amplified, low-magnitude inputs suppressed. Attention: αᵢ = softmax(qᵀkᵢ) weights by relevance. Both: dynamic, data-driven, adaptive.'
  ),
  dc.dual(
    'Dynamic portfolio gating applies the same principle to HUF observation. Elements in the portfolio have a noise floor—a minimum significance or observability threshold. Elements above this threshold are included in the active portfolio and contribute to the ratio state. Elements below the threshold are gated out (not deleted, just excluded from the active calculation). As new data arrives, the gate re-evaluates: elements that were below threshold may now rise above it and enter the active set. Elements that drop below threshold exit.',
    'Portfolio gate: G_i(t) = 1 if mᵢ(t) > threshold τᵢ, else G_i(t)=0. Active set: A(t) = {i : G_i(t)=1}. Recompute ρ(t) = (m_i(t) / ΣⱼϵA(t) m_j(t) : i ∈ A(t)). Gate threshold τᵢ set by domain (e.g., signal-to-noise). Adaptive: threshold evaluated at each t.'
  ),
  dc.dual(
    'The mathematics remain consistent: the unity constraint applies to the gated set. Σρᵢ = 1 only for the elements currently in the active portfolio. When the gate status changes, the ratio state is recomputed over the new gated set. The trace record documents when elements enter and leave the gated portfolio and why.',
    'Unity on gated set: Σᵢ∈A(t) ρᵢ(t) = 1.0 always. Changes to A(t) trigger recompute of all ρᵢ(t). Gating events logged: (t, i, event={enter|exit}, reason). Trace enables forensic understanding of why scope changed.'
  ),
  dc.dual(
    'This mechanism prevents false precision. If you have five potential elements in a system but only three produce observable data, you compute shares over the three. The two without data are not assigned zero share (which would be mathematically false); they are gated out. Once data arrives, they re-enter automatically.',
    'False precision avoidance: Never set ρᵢ=0 for unmeasured element. Instead: gate out. ρ computed only over {i : Gᵢ(t)=1}. When measurement arrives, re-gate. No phantom zeros. No forced precision beyond what data supports.'
  ),
  dc.spacer(240),
  dc.subHead('10.4 The Sufficiency Frontier at Multiple Scales'),
  dc.colLabels(),
  dc.dual(
    'The sufficiency frontier is not unique to HUF\'s corpus analysis. The frontier exists at every scale and in every domain where proportional allocation matters.',
    'Frontier universality: F_cell, F_department, F_organization, F_ecosystem all exist. Structure identical across scales: viable ↔ inviable boundary on simplex Δᴷ. Location (position in Δᴷ) scale-dependent; mathematical structure universal.'
  ),
  dc.dual(
    'A cell has a sufficiency frontier. The critical boundary is the concentration of regulatory signals and resources that allows the cell to sustain function. Below that frontier, the cell cannot maintain structure and dies. Above it, the cell is viable. The same ratio-based logic that governs HUF\'s portfolio analysis governs the cell\'s resource allocation between nucleus, cytoplasm, and organelles.',
    'Cell frontier: ρ = (m_nucleus, m_cytoplasm, m_mitochondria, m_other) ∈ Δ⁴. Viability requires ρ within safe region of Δ⁴. Below frontier (e.g., m_mitochondria→0): energy starvation, cell death. Above frontier: sustainable. Scale: nanometers; math: same.'
  ),
  dc.dual(
    'A department has a sufficiency frontier. The critical boundary is the balance of operator attention (management), tool capacity (budget), and external communication that allows the department to deliver its function. Below that frontier, the department cannot sustain its mandate and fails or restructures. The OCC 51/49 contract places the declared intent above the frontier; MC-4 monitoring detects if silent drift is approaching the frontier from below.',
    'Department frontier: ρ = (m_operator, m_budget, m_external_comms) ∈ Δ³. OCC contract specifies ρ_operator ≈ 0.51, ρ_budget ≈ 0.49 as nominal. Frontier F_dept below nominal. Drift toward (0.95, 0.05, 0) approaches frontier → danger. MC-4 detects drift trajectory before crossing.'
  ),
  dc.dual(
    'An organization has a sufficiency frontier. The critical boundary is the balance of stakeholder confidence, financial liquidity, and operational capacity that allows the organization to persist and adapt. Concentration risk—where one stakeholder\'s share rises toward 100%—approaches the frontier from above. Fragmentation risk—where many stakeholders have small non-actionable shares—approaches the frontier from below. Both cross the frontier into failure regimes.',
    'Org frontier: ρ = (m_stakeholder_confidence, m_liquidity, m_capacity) ∈ Δ³. Concentration risk: ρ_stakeholder→1.0 (frontier above). Fragmentation: many elements with ρᵢ<<threshold (frontier below). Either direction → failure. Healthy org stays interior to Δ³, away from boundary.'
  ),
  dc.dual(
    'The scale changes, but the structure does not. Every nested system has a frontier, and the Adaptive Scope principle allows HUF monitoring to apply at any scale by simply choosing the appropriate bandwidth. A researcher studying cell biology can use the same ratio-based analysis tools that a governance analyst uses for organizations, because the underlying mathematics is domain-agnostic.',
    'Universal applicability: Tools(H,Δᴷ,ρ,F) domain-independent. Cell biology: Δ⁴ (organelles). Governance: Δ² or Δ³ (resources). Ecology: Δ⁵ (species/habitats). Same tools. Different K, different F location, same mathematics. Domain agnosticism proven structurally.'
  ),
  dc.fullWidth(crossRef('Dynamic monitoring: Pillar 2, Sections 11–12 (OCC Drift and Gating)')),
  dc.fullWidth(crossRef('Nested systems in detail: Vol 3, Mathematical Foundations')),
  dc.fullWidth(crossRef('Scale applications: Vol 1–4, Domain-Specific Volumes')),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 11. HUF-ORG AND MACHINE LEARNING — DUAL COLUMN (condensed)
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('11. HUF-Org: The Sufficiency Frontier as Metabolic Boundary'),
  dc.subHead('11.1 The Organism Model'),
  dc.colLabels(),
  dc.dual(
    'HUF is not merely a framework; it IS an organism. Like any living system, it has a metabolic energy budget, structural constraints, growth dynamics, and immune defenses. The Sufficiency Frontier represents HUF-org\'s metabolic boundary—the outer membrane across which resources flow in and out.',
    'HUF-org ≡ living system: Budget M=1.0 (conservation). Elements {1,...,K} (capabilities). ρ(t) ∈ ΔK (state). Homeostasis: Σρᵢ=1.0 (metabolic law). Growth: iterative, bounded by Q-factors. Immunity: MC-4 monitors drift.'
  ),
  dc.dual(
    'At the core of HUF-org is the conservation law: Σ ρᵢ = 1.0. This is not a target. It is not aspirational. It is metabolic homeostasis. Just as a living cell maintains osmotic balance not by trying, but by the physics of semipermeable membranes, HUF maintains unity not by optimization, but by the structure of the simplex. The sum constraint is a conservation law—a fundamental property of the system, like energy conservation in thermodynamics.',
    'Conservation: Σρᵢ = 1.0 ⟺ constraint surface in ℝᴷ. Not optimization target (no objective function). Constraint topology (structure) ensures ρ always on surface. Like cell membrane forces osmotic balance, simplex topology forces unity. Involuntary (structural) not voluntary (chosen).'
  ),
  dc.spacer(240),
  dc.subHead('11.2 ML as HUF-Org: The Billion-Run Validation'),
  dc.colLabels(),
  dc.dual(
    'Every ML training run is a HUF-org experiment. The model\'s loss surface is a Sufficiency Frontier. Training loss decreases monotonically (organism growing), but validation loss has a minimum beyond which it rises (frontier crossed → overfitting). The frontier is not a gradual degradation; it is a cliff—exactly as in HUF. Every trained model ever recorded provides empirical evidence of the Sufficiency Frontier.',
    'ML = HUF experiment: Loss L(θ) ≡ governance metric. Epoch t ≡ time. Weights θ ≡ portfolio elements. Softmax layer: Σhⱼ = 1.0 (unity in output). Training curve sigmoid ≡ logistic growth (HUF-org trajectory). Overfitting crossover ≡ frontier crossing. Billions of recorded experiments.'
  ),
  dc.dual(
    'The logistic training curve IS the HUF-org growth curve. K (carrying capacity) = model capacity under architecture constraint. r (growth rate) = learning rate. The inflection point where deceleration begins = the point where combinatorial weight-interaction cost exceeds remaining loss-landscape margin. Both follow the same sigmoid trajectory when resources approach their carrying capacity.',
    'Logistic: dρ/dt = rρ(1−ρ/K). ρ(t) ≡ training accuracy. r = learning rate. K = architecture capacity. Training curve: sigmoid rise, inflection, plateau. Inflection: capacity limit approached. Beyond: weight-interaction complexity → diminishing returns. HUF-org sigmoid identical.'
  ),
  dc.dual(
    'Regularization mechanisms (L1, L2, dropout, weight decay) are the Sufficiency Frontier\'s enforcement tools—they prevent the portfolio from drifting beyond the frontier into the pathological region (overfitting). L2 weight decay monitors the magnitude of each weight (portfolio element) and penalizes growth that exceeds the declared distribution—this IS ratio drift detection. L1 sparsity forces elements to zero when their contribution drops below threshold—this IS dynamic portfolio gating. Dropout randomly removes elements during training, forcing the remaining portfolio to maintain coherence without them—this IS the adaptive scope bandwidth narrowing.',
    'Regularization ≡ MC-4: L2 decay: penalize |θ| → detects ρ drift. L1 sparse: zero weak θ → gate out low-share elements. Dropout: remove random θ → test robustness to gating. Early stopping: validation loss rise → detect frontier crossing. Empirical: billions of models show regularization prevents frontier crossing → overfitting blocked.'
  ),
  dc.fullWidth(crossRef('Adaptive Scope principle: Section 10 (Adaptive Scope)')),
  dc.fullWidth(crossRef('MC-4 immune system: Pillar 2, The Fourth Monitoring Category v2.5')),
  dc.fullWidth(crossRef('Mathematical foundations: Vol 3, Mathematical Foundations')),
  dc.fullWidth(crossRef('ML validation: Billions of empirical HUF-org experiments recorded in training telemetry')),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// § 12. CONCLUSION — DUAL COLUMN
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  dc.sectionHead('12. Conclusion'),
  dc.colLabels(),
  dc.dual(
    'The sufficiency frontier marks a qualitative boundary in information reduction. Below it, data is compressed or filtered. Above it, data is reduced to exactly the statistics required for a specified inference. The HUF PreParser operates above this boundary at 6,357,738:1, extracting portfolio governance statistics from heterogeneous data across 10 domains without domain-specific calibration.',
    'Frontier position: Located via empirical reduction R = input_bytes / output_bytes. Theoretical anchoring: Fisher sufficiency + Boltzmann phase-space collapse + unity constraint. Empirical validation: external tests (Planck changepoint OD 975, King Street ITS, three-domain confirmation).'
  ),
  dc.dual(
    'The theoretical basis is the unity constraint: any system where shares sum to one lives on the probability simplex, and the simplex coordinates are sufficient for governance inference. The empirical basis is a 10-domain corpus spanning mechanical, biological, ecological, digital, astrophysical, acoustic, and institutional systems. The external validation—a Pettitt changepoint matching the exact operational day of ESA Planck\'s He-4 exhaustion—provides evidence that the extracted statistics carry genuine physical information.',
    'Theory: Σρᵢ=1 + ρ∈ΔK ⟹ ρ sufficient for governance ℑ_governance. No domain-specific physics required. No parametric model. Algebra alone suffices. Empirical: 10 systems, 156M records, 6.4GB input, 1008B output, R=6.357×10⁶. Validation: Pettitt t*=OD975 ≡ He-4 exhaustion (p<0.001). Blind prediction confirms sufficiency.'
  ),
  dc.dual(
    'The Adaptive Scope principle extends the sufficiency frontier analysis to operating systems. By matching the observation scope to the data actually present, using center frequency and bandwidth metaphors to guide scoping decisions, and implementing dynamic portfolio gating that adapts to data availability in real time, HUF can monitor nested systems at multiple scales without loss of mathematical rigor.',
    'Scope: S(f_c, BW) defines observation bandwidth. Match to data: include elements with mᵢ(t) measurable; gate out unobservable. Dynamic gating: A(t)={i:Gᵢ(t)=1}. Recompute ρ(t) over A(t). Trace governance: record entry/exit events. Mathematically sound: Σᵢ∈A(t) ρᵢ(t)=1.0 always.'
  ),
  dc.dual(
    'HUF-org extends this framework by modeling HUF itself as a living system with metabolic constraints, iterative integration protocols, and immune-system-like drift detection. The unity constraint Σ ρᵢ = 1.0 is not a governance target but a conservation law. Growth proceeds iteratively, one element at a time, with viability testing before integration. The slowest (highest-Q) member governs the speed of adaptation. MC-4 serves as the immune system, detecting pathological drift (cancer) before it threatens organism survival.',
    'HUF-org: Conservation Σ=1.0 (not target, physics). Growth: iterative, Viability Test vetoes unsafe integration. Q-sensitivity: slowest member rate-limits. MC-4 immune system: detects drift, gates incompatible elements, signals stress. Organism model: empirically grounded in billions of ML training curves (overfitting = frontier crossing = cancer detection).'
  ),
  dc.dual(
    'The sufficiency frontier is not a property of HUF; it is a property of the inference task. HUF demonstrates that the frontier exists and can be reached without domain-specific knowledge, provided the structural invariant (Σ ρᵢ = 1) holds. The car/fuel analogy illustrates that the frontier is an everyday reality obscured by our habit of thinking in absolute numbers rather than ratios. In any system where budget is conserved and allocation is proportional, the frontier exists, the ratio reveals it, and the adaptive scope framework allows it to be monitored at any scale. As HUF-org matures, the same principles that govern external systems come to govern HUF itself.',
    'Universal principle: F_inference ⊂ ΔK exists for any task requiring proportional allocation decision. ρ coordinates sufficient for F-aware governance. Absolute magnitudes distract. Ratio structure reveals frontier. Adaptive scope extends to arbitrary K, arbitrary domains, arbitrary scales. Self-applicability: HUF watching HUF watching HUF... recursive sufficiency.'
  ),
  dc.spacer(),
);

// ══════════════════════════════════════════════════════════════════════════════
// REFERENCES (single column)
// ══════════════════════════════════════════════════════════════════════════════
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('References'),
  P('[1] C.E. Shannon, "A mathematical theory of communication," Bell Syst. Tech. J., vol. 27, pp. 379–423, 1948.'),
  P('[2] R.A. Fisher, "On the mathematical foundations of theoretical statistics," Phil. Trans. R. Soc. A, vol. 222, pp. 309–368, 1922.'),
  P('[3] J. Aitchison, "The statistical analysis of compositional data," J. R. Stat. Soc. B, vol. 44, pp. 139–177, 1982.'),
  P('[4] L. Boltzmann, "Weitere Studien über das Wärmegleichgewicht unter Gasmolekülen," Sitzungsberichte Akad. Wiss. Wien, vol. 66, pp. 275–370, 1872.'),
  P('[5] E.J.G. Pitman, "Sufficient statistics and intrinsic accuracy," Proc. Cambridge Phil. Soc., vol. 32, pp. 567–579, 1936.'),
  P('[6] B.O. Koopman, "On distributions admitting a sufficient statistic," Trans. Amer. Math. Soc., vol. 39, pp. 399–409, 1936.'),
  P('[7] J. Ziv and A. Lempel, "A universal algorithm for sequential data compression," IEEE Trans. Inf. Theory, vol. 23, pp. 337–343, 1977.'),
  P('[8] G.K. Wallace, "The JPEG still picture compression standard," IEEE Trans. Consum. Electron., vol. 38, pp. 18–34, 1992.'),
  P('[9] K. Brandenburg, "MP3 and AAC explained," in Proc. AES 17th Int. Conf., 1999.'),
  P('[10] G.J. Sullivan et al., "Overview of HEVC," IEEE Trans. Circuits Syst. Video Technol., vol. 22, pp. 1649–1668, 2012.'),
  P('[11] R.E. Kalman, "A new approach to linear filtering and prediction problems," J. Basic Eng., vol. 82, pp. 35–45, 1960.'),
  P('[12] E. Ostrom, Governing the Commons. Cambridge University Press, 1990.'),
  P('[13] Planck Collaboration, "Planck 2013 results. I. Overview," Astron. Astrophys., vol. 571, A1, 2014.'),
  P('[14] A.N. Pettitt, "A non-parametric approach to the change-point problem," Appl. Stat., vol. 28, pp. 126–135, 1979.'),
  P('[15] P. Higgins, "The Fourth Monitoring Category: Ratio State Monitoring," HUF Triad Pillar 2, v2.5, 2026.'),
  P('[16] P. Higgins, "The HUF Triad: Volume 8, Synthesis," v1.0, 2026.'),
  P('[17] J.L. Doob, "Statistical estimation," Trans. Amer. Math. Soc., vol. 39, pp. 410–421, 1936.'),
  P('[18] G. Darmois, "Sur les lois de probabilité à estimation exhaustive," C.R. Acad. Sci. Paris, vol. 200, pp. 1265–1266, 1935.'),
  P('[19] J. Rissanen, "Modeling by shortest data description," Automatica, vol. 14, pp. 465–471, 1978.'),
  P('[20] T.M. Cover and J.A. Thomas, Elements of Information Theory, 2nd ed. Wiley, 2006.'),
  P('[21] J.L. Fleiss, B. Levin, and M.C. Paik, Statistical Methods for Rates and Proportions, 3rd ed. Wiley, 2003.'),
  P('[22] J. Aitchison and J.A.C. Brown, The Lognormal Distribution. Cambridge University Press, 1957.'),
  P('[23] W.A. Shewhart, Economic Control of Quality of Manufactured Product. Van Nostrand, 1931.'),
);

// ══════════════════════════════════════════════════════════════════════════════
// BUILD DOCUMENT
// ══════════════════════════════════════════════════════════════════════════════
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
      page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } },
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MID, space: 1 } },
        children: [
          new TextRun({ text: 'HUF Triad — Pillar 1', font: 'Times New Roman', size: 18, color: MID }),
          new TextRun({ text: '\tThe Sufficiency Frontier v3.6', font: 'Times New Roman', size: 18, italics: true, color: MID }),
        ],
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
      })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC', space: 1 } },
        children: [
          new TextRun({ text: 'HUF v1.2.0 · MIT License · ', font: 'Times New Roman', size: 16, color: '999999' }),
          new TextRun({ text: 'Page ', font: 'Times New Roman', size: 16, color: '999999' }),
          new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 16, color: '999999' }),
        ],
      })] }),
    },
    children,
  }],
});

const OUT = __dirname.replace(/[/\\]pillars$/, '') + '/HUF_Sufficiency_Frontier_v3.6.docx';
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log(`✔ Generated: ${OUT} (${buf.length.toLocaleString()} bytes)`);
  console.log(`✔ Version: 3.6 (Dual-Column Edition)`);
  console.log(`✔ Sections: 1-12 (Title, Abstract, 12 content sections, References)`);
  console.log(`✔ Format: Two-column (Context | Analytic) for all content sections`);
  process.exit(0);
}).catch(e => {
  console.error('Error:', e);
  process.exit(1);
});
