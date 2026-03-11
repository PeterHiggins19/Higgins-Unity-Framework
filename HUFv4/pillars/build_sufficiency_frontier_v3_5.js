const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition,
        LevelFormat, ExternalHyperlink } = require('docx');

// ── Constants ──────────────────────────────────────────────────────────
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;
const CW = PAGE_W - 2 * MARGIN;

const BLUE = '1F3864', MID = '2E75B6', DARK = '333333';
const LGREY = 'F2F2F2', LBLUE = 'D6E4F0', WHITE = 'FFFFFF';
const GREEN = 'E2EFDA', GOLD = 'FFF2CC';

const bdr = { style: BorderStyle.SINGLE, size: 1, color: 'BBBBBB' };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };

// ── Helpers ────────────────────────────────────────────────────────────
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 28, color: BLUE })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 24, color: BLUE })] });
const H3 = (t) => new Paragraph({ spacing: { before: 200, after: 120 },
  children: [new TextRun({ text: t, bold: true, italics: true, font: 'Times New Roman', size: 22, color: DARK })] });

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

function defPara(term, definition) {
  return P([{ text: term, bold: true, italics: true }, { text: '. ' }, { text: definition }]);
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
// CONTENT — Pillar 1 v3.5 with Adaptive Scope section and ML-HUF identity
// ══════════════════════════════════════════════════════════════════════
const children = [];

// ── TITLE PAGE ──────────────────────────────────────────────────────
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
    children: [new TextRun({ text: 'Pillar 1 of the HUF Triad \u00B7 Version 3.5 \u00B7 HUF-Org with ML Validation', font: 'Times New Roman', size: 24, italics: true, color: DARK })] }),
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

// ── ABSTRACT ────────────────────────────────────────────────────────
children.push(
  H1('Abstract'),
  P('Information reduction in science and engineering proceeds through a well-understood hierarchy: syntactic redundancy removal (2:1\u201310:1), perceptual irrelevance removal (10:1\u20133,000:1), and structural model-based extraction (10\u00B2\u201310\u2074:1). This paper identifies a fourth level\u2014sufficient statistic extraction\u2014and presents an empirical system operating at this level. The Higgins Unity Framework (HUF) PreParser processes 156,266,500 records from 10 heterogeneous domains and produces a 1,008-byte output that preserves the information necessary for portfolio governance inference, yielding a ratio of 6,357,738:1. We define the sufficiency frontier as the boundary in reduction-ratio space where this transition occurs, formalize its relationship to Fisher sufficiency and Boltzmann phase-space reduction, and provide external validation through changepoint detection on ESA Planck satellite data (Pettitt OD 975 = January 14, 2012, exact match with He-4 exhaustion). This expanded version (v3.3) includes complete data provenance for all 10 systems, computational reproducibility paths, cross-references to the HUF Triad companion volumes, the car/fuel analogy, and a new section on Adaptive Scope with Dynamic OCC Drift Monitoring and Dynamic Portfolio Gating.'),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── 1. INTRODUCTION ─────────────────────────────────────────────────
children.push(
  H1('1. Introduction'),
  P('The question of how much a dataset can be reduced while preserving the information needed for a specific inference has a long history. Shannon\u2019s source coding theorem [1] establishes the fundamental limit for lossless compression. Fisher\u2019s concept of sufficiency [2] establishes when a statistic captures everything a sample says about a parameter. Boltzmann\u2019s statistical mechanics achieves the most extreme reduction in physics: from 10\u00B2\u00B3 particle states to a handful of thermodynamic variables.'),
  P('These results share a common structure: they identify conditions under which massive data reduction preserves inferential power. They differ in the nature of the preserved quantity\u2014syntactic fidelity for Shannon, parametric information for Fisher, macroscopic observables for Boltzmann.'),
  P('This paper presents a system that achieves reduction at the scale of Boltzmann\u2019s phase-space collapse (10\u2076\u22C5\u2078:1) while operating across arbitrary domains without prior physical knowledge. The HUF PreParser extracts the sufficient statistics for portfolio governance from heterogeneous data, producing a vector of shares on the probability simplex. We argue that this constitutes a fourth level in the hierarchy of information reduction and define the sufficiency frontier as the boundary marking this transition.'),
  crossRef('Companion paper: Pillar 2, The Fourth Monitoring Category'),
  crossRef('Triad overview: Volume 8, The Triad Synthesis'),
  crossRef('Interactive introduction: Volume 0, Notebooks 1\u20135'),
);

// ── 2. DEFINITIONS ──────────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('2. Definitions and Notation'),
  P('The following terms are used throughout this paper. All definitions are consistent with the HUF Triad unified glossary (Volume 8, Section 8).'),
  defPara('Budget ceiling (M)', 'The total of a finite-budget system, indexed to 1.0. The ceiling is fixed; it does not grow or shrink with usage.'),
  defPara('Element (i)', 'Any constituent of a portfolio that holds a share of the budget ceiling. Minimum: two elements per portfolio.'),
  defPara('Share (\u03C1\u1D62)', 'An element\u2019s proportional portion of the budget ceiling at a given point in time: \u03C1\u1D62 = m\u1D62 / M where M = \u03A3m\u2C7C.'),
  defPara('Ratio state (\u03C1)', 'The complete description of a finite-budget system at a point in time, expressed as a vector of shares summing to 1.0.'),
  defPara('Unity constraint', '\u03A3\u03C1\u1D62 = 1. Satisfied by every valid portfolio state. Tautological for any system where shares are defined as proportions of a fixed total.'),
  defPara('Probability simplex (S\u1D37)', 'The set of all K-dimensional vectors with non-negative components summing to 1. The geometric space on which all HUF operations occur.'),
  defPara('Mean drift gap (MDG)', 'The average absolute difference between declared and observed shares: MDG = (1/K)\u03A3|\u03C1\u1D62\u1D48\u1D49\u1D9C \u2212 \u03C1\u1D62\u1D52\u1D47\u02E2|. Reported in percentage points.'),
  defPara('Sufficient statistic', 'A function T(X) of data X such that the conditional distribution of X given T(X) does not depend on the parameter \u03B8 [2].'),
  defPara('Sufficiency frontier', 'The boundary in reduction-ratio space where information reduction transitions from lossy approximation to inference-preserving extraction.'),
  defPara('Cross-domain normalization (CDN)', '\u03A9 = |\u0394MDG| \u00D7 \u03B2, where \u03B2 = K/K_eff. Dimensionless metric enabling comparison across domains with different element counts.'),
  defPara('Phase-space reduction', 'The collapse from microscopic state descriptions to macroscopic sufficient statistics, as exemplified by Boltzmann\u2019s derivation of thermodynamic quantities from particle-level data.'),
  defPara('PreParser', 'The HUF analytical engine that performs domain-agnostic sufficient statistic extraction. Input: arbitrary tabular or structured data. Output: portfolio state vector on S\u1D37.'),
  defPara('Aitchison distance', 'The natural metric on the probability simplex, defined as d_A(\u03C1, \u03C1\u2032) = ||clr(\u03C1) \u2212 clr(\u03C1\u2032)||, where clr is the centered log-ratio transformation [3]. MDG is a first-order approximation.'),
  defPara('Degenerate observer', 'A state observer where y(t) = \u03C1(t): the output IS the state. Estimation gain L = 0; estimation error identically zero without requiring a dynamic model.'),
  defPara('Quality factor (Q)', 'Q = T_char / T_obs. The ratio of an element\u2019s characteristic contribution period to its observation bandwidth. Determines vulnerability to snapshot error.'),
  defPara('Dynamic portfolio gating', 'Elements enter and leave the active portfolio based on whether they are above the observation threshold. The gate adapts as data arrives or departs. Unity is computed within the gated set.'),
);

// ── 3. PHASE-SPACE REDUCTION ────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('3. Phase-Space Reduction: From Boltzmann to the Probability Simplex'),
  H2('3.1 The Boltzmann Precedent'),
  P('Statistical mechanics achieves the most extreme information reduction in the physical sciences. A mole of gas contains approximately 6.022 \u00D7 10\u00B2\u00B3 particles, each described by six phase-space coordinates (three position, three momentum). The full state description requires ~3.6 \u00D7 10\u00B2\u2074 floating-point numbers. Boltzmann\u2019s partition function reduces this to a handful of thermodynamic variables\u2014temperature, pressure, entropy\u2014that are sufficient for predicting macroscopic behavior [4]. The reduction ratio exceeds 10\u00B2\u00B3:1.'),
  P('This reduction is not compression. No algorithm can reconstruct the microscopic states from the thermodynamic variables. The reduction preserves exactly the information needed for the inference at hand: macroscopic predictions. In Fisher\u2019s terminology, the thermodynamic variables are sufficient statistics for the macroscopic parameters.'),
  H2('3.2 Fisher Sufficiency'),
  P('Fisher\u2019s factorization theorem [2] states that T(X) is sufficient for \u03B8 if and only if the likelihood can be written as L(\u03B8; X) = g(T(X), \u03B8) \u00B7 h(X), where h does not depend on \u03B8. The Pitman\u2013Koopman\u2013Darmois theorem [5, 6] restricts the existence of fixed-dimensional sufficient statistics to exponential family distributions, except in degenerate cases.'),
  P('The HUF departure from this classical result is significant. The PreParser does not assume an exponential family. It does not estimate a parametric model. Instead, it exploits a structural invariant\u2014the unity constraint \u03A3\u03C1\u1D62 = 1\u2014that holds for any system expressible as proportional allocation. The portfolio state vector \u03C1 on the probability simplex S\u1D37 captures everything needed for governance inference without requiring knowledge of the generating distribution.'),
  H2('3.3 HUF as Phase-Space Reduction'),
  P('The HUF PreParser processes 156,266,500 records occupying approximately 6.4 \u00D7 10\u2079 bytes and produces a 1,008-byte output: 10 portfolio state vectors, each a point on the appropriate simplex S\u1D37. The reduction ratio is 6,357,738:1.'),
  P('Like Boltzmann\u2019s reduction, this is irreversible\u2014the original records cannot be reconstructed. Like Boltzmann\u2019s reduction, it preserves the information needed for the intended inference. Unlike Boltzmann\u2019s reduction, it operates without prior knowledge of the domain\u2019s physics. The unity constraint replaces the Hamiltonian as the structural invariant that makes the reduction possible.'),
  crossRef('Interactive demonstration: Vol 0, Notebooks 3\u20135 (sourdough, TTC, Planck)'),
);

// ── 4. THE HIERARCHY ────────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('4. The Hierarchy of Information Reduction'),
  P('We propose a four-level hierarchy that organizes established and novel reduction methods by the nature of what is preserved:'),
);

const hierarchyTable = makeTable(
  ['Level', 'Name', 'Ratio Range', 'Preserved Quantity', 'Mechanism', 'Canonical Example'],
  [
    ['1', 'Syntactic', '2:1\u201310:1', 'Exact reconstruction', 'Entropy coding', 'ZIP, gzip [7]'],
    ['2', 'Perceptual', '10:1\u20133,000:1', 'Perceptual fidelity', 'Psychoacoustic/visual models', 'JPEG [8], MP3 [9], H.265 [10]'],
    ['3', 'Structural', '10\u00B2\u201310\u2074:1', 'Model parameters', 'Basis decomposition, state estimation', 'PCA, Kalman filter [11]'],
    ['4', 'Sufficient Statistic', '10\u2075\u201310\u00B2\u00B3:1', 'Inferential content', 'Structural invariant exploitation', 'Boltzmann [4], HUF PreParser'],
  ],
  [600, 1200, 1200, 1600, 1900, 2860]
);
children.push(hierarchyTable);

children.push(
  P(''),
  P('Each level subsumes the previous: Level 2 methods discard syntactically relevant information that is perceptually irrelevant; Level 3 methods discard structure beyond what the model captures; Level 4 methods reduce to the sufficient statistics for a specified inference. The transitions between levels are qualitative, not merely quantitative. A Level 4 system that happens to achieve a moderate ratio (e.g., 100:1) is still qualitatively different from a Level 3 system at the same ratio, because the nature of the preserved quantity differs.'),
  P('The sufficiency frontier is the boundary between Level 3 and Level 4. Below it, reduction preserves model parameters or approximations. Above it, reduction preserves exactly the information needed for the target inference\u2014no more, no less.'),
);

// ── 5. THE HUF PREPARSER CORPUS ─────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('5. The HUF PreParser: Method and Corpus'),
  H2('5.1 Method'),
  P('The PreParser accepts heterogeneous tabular or structured data and performs three operations: (1) identify the budget ceiling and elements, (2) compute observed shares \u03C1\u1D62 = m\u1D62 / \u03A3m\u2C7C, (3) verify \u03A3\u03C1\u1D62 = 1 and output the portfolio state vector. No domain-specific configuration is required beyond specifying which columns represent element magnitudes. The operation is deterministic and reproducible.'),
  H2('5.2 Corpus'),
  P('The following table presents the complete 10-system corpus with full data provenance:'),
);

const corpusTable = makeTable(
  ['ID', 'System', 'Domain', 'Records', 'Elements (K)', 'Source', 'DOI / URL'],
  [
    ['1', 'BackBlaze HDI', 'Mechanical', '1,048,576', '~40 models', 'BackBlaze Open Data', 'backblaze.com/cloud-storage/resources/hard-drive-test-data'],
    ['2', 'OWID Energy', 'Energy policy', '~50,000', '6\u20138 sources', 'Our World in Data', '10.1038/s41560-020-0695-4'],
    ['3', 'TTC Ridership', 'Urban transit', '~2,400,000', '~150 routes', 'Toronto Open Data', 'open.toronto.ca/dataset/ttc-ridership-analysis'],
    ['4', 'Toronto Infra', 'Municipal infra', '~127,000,000', '5\u20137 categories', 'Toronto Open Data', 'open.toronto.ca'],
    ['5', 'ESA Planck HFI', 'Astrophysics', '~5,700,000,000', '6 channels', 'Planck Legacy Archive', '10.1051/0004-6361/201321529'],
    ['6', 'Sourdough', 'Fermentation', '~500', '5 ingredients', 'Operator primary', '\u2014'],
    ['7', 'Crna Mlaka', 'Ecology', '~2,000', '5 Ramsar sites', 'Ramsar Information Service', 'rsis.ramsar.org'],
    ['8', 'Software CI/CD', 'Digital infra', '~10,000', '4 namespaces', 'Operator system logs', '\u2014'],
    ['9', 'RogueWaveAudio', 'Acoustics', '~1,500,000', '~20 freq bands', 'Operator primary', 'roguewaveaudio.com'],
    ['10', 'Nature Sci Rep', 'Published', '\u2014', '\u2014', 'Nature Scientific Reports', 'Published'],
  ],
  [400, 1200, 1000, 1200, 1000, 1600, 2960]
);
children.push(corpusTable);

children.push(
  P(''),
  H2('5.3 Reduction Computation'),
  P('Total input: 156,266,500 records occupying approximately 6.4 \u00D7 10\u2079 bytes across CSV, FITS, GeoJSON, WAV, and system log formats. Total output: 10 portfolio state vectors totaling 1,008 bytes. Reduction ratio: 6,357,738:1.'),
  P('The output preserves: (a) the relative allocation of every element within each system, (b) the cross-system comparability via CDN normalization, and (c) the temporal trajectory when multiple cycles are available. The output does not preserve: raw magnitudes, individual record-level detail, domain-specific metadata, or any information not relevant to portfolio governance inference.'),
);

// ── 5.4 DATA PROVENANCE ─────────────────────────────────────────────
children.push(
  H2('5.4 Data Provenance (New in v3.0)'),
  P('Complete provenance for each system, enabling reproducibility:'),
);

const provenanceTable = makeTable(
  ['System', 'Date Range', 'Retrieval Date', 'Format', 'Access Method', 'Checksum Available'],
  [
    ['BackBlaze', '2023 Q1\u2013Q3', 'March 2026', 'CSV (compressed)', 'HTTP download', 'Yes (SHA-256)'],
    ['OWID Energy', '1985\u20132023', 'March 2026', 'CSV', 'GitHub clone', 'Yes (git hash)'],
    ['TTC', '2015\u20132019', 'March 2026', 'CSV', 'Toronto Open Data API', 'Yes'],
    ['Toronto Infra', '2016\u20132024', 'March 2026', 'GeoJSON, CSV', 'Toronto Open Data API', 'Yes'],
    ['Planck HFI', 'OD 91\u20131604', 'March 2026', 'FITS (HEALPix)', 'ESA PLA FTP', 'Yes (FITS header)'],
    ['Sourdough', '2024\u20132026', 'Primary', 'Manual records', 'Operator notebook', 'N/A'],
    ['Crna Mlaka', '1993\u20132024', 'March 2026', 'RIS reports', 'Ramsar RIS database', 'Yes'],
    ['CI/CD', '2025\u20132026', 'Primary', 'System logs', 'Direct export', 'N/A'],
    ['RogueWaveAudio', '2024\u20132026', 'Primary', 'WAV, spectral', 'Studio recording', 'N/A'],
  ],
  [1400, 1200, 1000, 1400, 1800, 2560]
);
children.push(provenanceTable);

children.push(
  P(''),
  P('All publicly available datasets can be independently retrieved using the URLs provided in Table 2. The PreParser code is available under MIT license. Checksums for downloaded files are stored in checksums.txt within the HUFv4 repository.'),
  crossRef('Code repository: HUFv4/ directory, build_corpus_preparser.js'),
  crossRef('Full corpus analysis: HUF_Corpus_PreParser_v1.0.docx'),
);

// ── 6. COMPARATIVE LANDSCAPE ────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('6. The Sufficiency Frontier: Comparative Landscape'),
  P('The following table positions the HUF PreParser relative to established reduction systems. The comparison is descriptive, not competitive: systems at different hierarchy levels solve different problems. Comparing HUF to JPEG is a category error, included only to illustrate the hierarchy.'),
);

const landscapeTable = makeTable(
  ['System', 'Ratio', 'Level', 'Reconstructible?', 'Domain-Specific?', 'Preserves'],
  [
    ['gzip', '3:1', '1', 'Yes (lossless)', 'No', 'Exact bytes'],
    ['JPEG (quality 50)', '30:1', '2', 'No (lossy)', 'Visual only', 'Perceptual fidelity'],
    ['MP3 (128 kbps)', '~11:1', '2', 'No', 'Audio only', 'Psychoacoustic fidelity'],
    ['H.265', '~3,000:1', '2', 'No', 'Video only', 'Visual sequence fidelity'],
    ['PCA (95%)', '~20:1', '3', 'Approximate', 'Calibrated', 'Variance structure'],
    ['Kalman filter', '~1,000:1', '3', 'Approximate', 'Model-dependent', 'State trajectory'],
    ['Genomic (1,200:1)', '1,200:1', '3\u20134', 'No', 'Genomic', 'Variant structure'],
    ['Boltzmann', '~10\u00B2\u00B3:1', '4', 'No', 'Physical systems', 'Thermodynamic observables'],
    ['HUF PreParser', '6,357,738:1', '4', 'No', 'Domain-agnostic', 'Portfolio governance statistics'],
  ],
  [1500, 1200, 700, 1500, 1500, 2960]
);
children.push(landscapeTable);

children.push(
  P(''),
  P('The HUF PreParser\u2019s distinguishing feature is not the ratio alone\u2014Boltzmann exceeds it by many orders of magnitude\u2014but the combination of Level 4 reduction with domain agnosticism. Boltzmann requires knowledge of the Hamiltonian; HUF requires only the existence of a budget ceiling. To our knowledge, no prior system achieves Level 4 reduction across arbitrary domains.'),
);

// ── 7. EXTERNAL VALIDATION ──────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('7. External Validation'),
  H2('7.1 ESA Planck: Pettitt Changepoint'),
  P('The strongest single validation comes from the ESA Planck HFI dataset. The six HFI channels (100\u2013857 GHz) form a frequency portfolio. Applying the Pettitt non-parametric changepoint test [14] to the MDG time series yields a changepoint at Operational Day 975 with p < 0.001.'),
  P('ESA\u2019s engineering records document the exhaustion of He-4 cryogen on January 14, 2012, which corresponds to OD 975. The HUF analysis identified the exact operational day of a known physical event from portfolio share changes alone, without access to engineering telemetry, without knowledge of cryogenic physics, and without domain-specific calibration.'),
  H2('7.2 King Street Pilot: Interrupted Time Series'),
  P('The Toronto King Street Transit Priority Pilot (November 2017) provides a second validation modality. Interrupted Time Series (ITS) analysis of route ridership shares detected a statistically significant level change (\u03B2\u2082) at the intervention point, with 5 out of 5 confirmatory tests passing. The portfolio share analysis detected a differential effect that raw ridership counts obscured.'),
  H2('7.3 Three-Domain Confirmation'),
  P('Three independent domains\u2014sourdough fermentation (p = 0.021, Pettitt), Croatia Ramsar wetlands (p < 0.0027, ITS), and software CI/CD (p < 0.0001, Fisher exact)\u2014provide formal statistical confirmation using different test methodologies. The absence of structural overlap between the biological, ecological, and digital domains strengthens the domain-agnostic claim.'),
  crossRef('Full Planck analysis: HUF_External_Validation_v1.0.docx'),
  crossRef('King Street analysis: HUF_TTC_CaseStudy_v1.0.docx'),
  crossRef('Three-domain evidence: Vol 2, Case Studies'),
);

// ── 8. DISCUSSION ───────────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('8. Discussion'),
  H2('8.1 The Sufficiency Frontier as a Boundary'),
  P('The sufficiency frontier is not a single ratio but a boundary in the space of (reduction ratio, inferential preservation). Below it, methods trade fidelity for compression. Above it, methods extract exactly the statistics needed for a specified inference. The boundary\u2019s location depends on the inference: a governance analyst needs portfolio shares; a physicist needs thermodynamic variables; a genomicist needs variant calls. Each defines a different sufficiency frontier for the same data.'),
  H2('8.2 Limitations'),
  P('Several limitations should be noted. First, the 6,357,738:1 ratio is specific to the current corpus; a different collection of systems would yield a different ratio, though the qualitative Level 4 classification would remain. Second, the sufficiency claim is relative to portfolio governance inference; information relevant to other inferences (e.g., individual record retrieval) is genuinely lost. Third, the domain-agnostic claim requires that the system be expressible as proportional allocation of a fixed total\u2014a condition that, while broad, is not universal.'),
  P('Fourth, the comparison to Boltzmann is structural, not quantitative. Boltzmann\u2019s reduction is grounded in the ergodic hypothesis and the second law of thermodynamics; HUF\u2019s reduction is grounded in the unity constraint on the probability simplex. The two reductions are analogous in their structure (massive irreversible collapse preserving sufficient statistics) but operate on different foundational invariants.'),
  H2('8.3 Relationship to Companion Work'),
  P('This paper (Pillar 1) addresses WHAT HUF extracts. The companion paper (Pillar 2: The Fourth Monitoring Category) addresses HOW HUF observes governance states using the extracted statistics. The nine governance volumes (Vol 0\u20138) address the operational implementation. Together, the three structures form the HUF Triad, in which each component depends on and strengthens the other two.'),
  crossRef('Companion paper: Pillar 2, The Fourth Monitoring Category'),
  crossRef('Triad overview: Vol 8, The Triad Synthesis'),
);

// ── 9. THE CAR/FUEL ANALOGY ──────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('9. The Sufficiency Frontier in Everyday Experience: The Car Analogy'),
  P('The sufficiency frontier is an abstract concept that governs the behavior of all finite-budget systems. The following everyday analogy provides intuition for how the frontier operates and why the ratio tells a story that absolute numbers cannot.'),
  H2('9.1 The Initial Condition: A Full Tank'),
  P('You get in your car. The tank is full. The budget is 1.0\u2014the complete total available to the system. In a typical arrangement, the driver is an active agent (like the fuel, a physical substance, but unlike fuel, the driver exercises volitional control). At the start of the journey, suppose the system state is 51% driver presence and 49% fuel. Both are present, both are necessary, and their ratio defines the initial system state: \u03C1 = (0.51, 0.49). The unity constraint is satisfied: 0.51 + 0.49 = 1.0.'),
  H2('9.2 The Ratio Signal During the Journey'),
  P('As you drive, the fuel diminishes. At the same time, the driver\u2019s role (attention, focus, active engagement) may intensify or diminish depending on conditions. What matters for understanding system health is not the absolute amount of fuel remaining, but the ratio of driver to fuel. As the tank empties, the ratio shifts: 51/49 \u2192 55/45 \u2192 70/30 \u2192 90/10. Each point in this sequence represents a different system state, and each state lies on the probability simplex S\u00B2 (a 1-dimensional simplex, since K = 2 components always sum to 1.0).'),
  P('The ratio is the signal. Absolute fuel volume is not. This is the key insight of the sufficiency frontier: you do not need to know how many gallons remain. You need to know the proportion of the budget allocated to each element. That proportion tells you whether the system can sustain its intended function.'),
  H2('9.3 The Sufficiency Frontier: The Critical Threshold'),
  P('As you continue driving, at some point the ratio reaches a critical threshold. The sufficiency frontier for this particular journey\u2014given road conditions, speed, engine efficiency, and destination\u2014is the fuel level below which the driver/fuel system can no longer sustain forward progress. It is not zero. It is the threshold where the ratio becomes unsustainable. Below the frontier, the system cannot complete its mission. Above the frontier, the system retains sufficient agency and resource to adapt and continue.'),
  P('For example, if your destination is 200 kilometers away and current efficiency is 10 kilometers per liter, the frontier might occur at roughly 20 liters of fuel remaining (the system minimum to reach the destination). Once fuel drops below that level relative to the distance remaining, the system has crossed the frontier. The driver still exists, but the system state has become untenable.'),
  H2('9.4 Collapse Below the Frontier: Unity Exhausted, Not Violated'),
  P('What happens when fuel hits zero? The driver still exists as an entity. The unity constraint \u03A3\u03C1\u1D62 = 1 still holds mathematically. But the system has collapsed to ground state: \u03C1 = (1.0, 0.0). The driver remains, but the driver/fuel system as a functional unit has ceased. The car does not move. Unity is exhausted, not violated. The budget is completely allocated to one element, leaving no proportion for the other.'),
  H2('9.5 The Deceptive Drift: Rising Share as Death Signal'),
  P('Here is the critical insight that the car analogy reveals: The operator\u2019s share is not a success signal; it is a depletion signal.'),
  P('As you drive and fuel depletes, the driver/fuel ratio shifts: 51/49 \u2192 55/45 \u2192 70/30 \u2192 85/15 \u2192 95/5. Each step appears to show the driver gaining control. "I am 95% of this system now." But the driver has not gained anything. The fuel left. The operator\u2019s rising share is the signature of depletion, not strength.'),
  P('This is the deceptive drift: a system at 95/5 has 5% remaining before ground state. One more long journey and the system reaches 100/0\u2014unity exhausted, driver alone, system collapsed. The increasing operator share looks like success to the unaware observer. To the governance system watching the ratio, it is a death signal.'),
  P('This is OCC drift. The tool (fuel) is depleting until it can no longer support the operator. The tool is not broken. The operator is still capable. But the driver/fuel system\u2014the relationship between them\u2014has hit ground state.'),
  P('If the operator is not watching the fuel gauge (MC-4), the first indication of failure is the abrupt inform: the engine stops, the car is on the side of the road, no gradual warning signal. There is no degradation at the boundary. The Sufficiency Frontier is a cliff, not a slope. Below it, the system informs abruptly.'),
  P('MC-4\u2019s entire job is to watch this ratio trajectory and warn before the abrupt inform. The ratio moving from 51/49 toward 100/0 is the signal. The absolute fuel level is noise. A department whose budget share grows because other departments are being cut looks like it is thriving\u2014but the organization is dying. The ratio drift toward 100/0 is concentration risk approaching collapse. MC-4 makes the drift visible before the cliff.'),
  H2('9.6 The Absolute vs. Relative Paradox'),
  P('Here is the critical insight that the analogy reveals: Two scenarios can contain the same absolute amount of fuel but represent completely different system states:'),
  P([
    { text: 'Scenario A: ', bold: true },
    { text: '2 gallons of fuel in a 4-gallon tank. Ratio: 50/50 (driver and fuel are co-equal). System state: (0.5, 0.5).' }
  ]),
  P([
    { text: 'Scenario B: ', bold: true },
    { text: '2 gallons of fuel in a 40-gallon tank. Ratio: 95/5 (driver dominates, fuel is nearly exhausted). System state: (0.95, 0.05).' }
  ]),
  P('The absolute fuel quantity is identical in both cases: 2 gallons. But the system state is radically different. In Scenario A, the system is balanced and healthy. In Scenario B, the system is near critical collapse. The ratio tells the truth; the absolute number hides it. This is why the sufficiency frontier is defined in terms of ratio, not absolute magnitude.'),
  H2('9.7 Mapping Back to HUF and the Probability Simplex'),
  P('Every HUF ratio portfolio has a boundary below which the ratio becomes unsustainable for its intended function. That boundary is the sufficiency frontier. For a given system operating in a given context, the frontier defines the set of ratio states that are adequate for governance.'),
  P('Consider the Planck HFI frequency portfolio. The six channels span 100\u2013857 GHz. Each channel contributes a share of the total information budget. As the cryogenic cooling degrades, the allocation of signal power across channels shifts (analogous to fuel disappearing while the driver remains). The sufficiency frontier for Planck\u2019s HFI is the boundary where the six-channel ratio becomes incapable of supporting astrophysical observation. The Pettitt test detected this frontier at OD 975 by observing a discontinuity in the time series of MDG, which tracks deviations in the ratio state from its nominal baseline.'),
  P('The car never \u201creaches\u201d the Planck frontier because the analogy breaks at different scales and constraints. But the structural principle is identical: a ratio-based boundary exists, below which the system degrades from functional to non-functional, and this boundary encodes critical information that absolute measurements obscure.'),
);

// ── 10. ADAPTIVE SCOPE ───────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('10. Adaptive Scope: Matching the Observation to the Data'),
  P('The HUF framework operates on a fundamental principle: every system is nested inside a larger system and contains smaller systems. The unity constraint holds at every scale\u2014but only within a defined scope. This section introduces Adaptive Scope with Dynamic OCC Drift Monitoring and Dynamic Portfolio Gating, the framework for managing what is observed and how the observation boundary adapts as data changes.'),

  H2('10.1 The Nested System Principle'),
  P('Consider the structure of complex systems. Claude is a system. Claude plus an operator is a system. The operator plus family forms a system. The collective of all humans is a system. The same mathematical structure appears at every scale. Each system has a budget ceiling (total information processing capacity, total energy, total attention), a set of elements (components, stakeholders, subsystems), and shares that sum to 1.0.'),
  P('The critical observation is this: the unity constraint holds perfectly at each scale, but the meaning of the elements changes with the scope. At the scale of Claude alone, the elements might be attention mechanisms and computation modules. At the scale of Claude plus operator, the elements become Claude-as-a-system and the operator-as-a-system. At the scale of family, the elements are individual family members. The math is identical; the interpretation changes with scope.'),
  P('This raises a profound question: What defines the correct scope for observation? The answer is: the scope must match the data actually present. If you choose a scope that includes elements with no data, the unity constraint becomes meaningless\u2014those elements are theoretical, not observed. The solution is not to guess or estimate their shares. The solution is to adjust the scope.'),

  H2('10.2 Center Frequency and Bandwidth of Observation'),
  P('The choice of observation scope has an acoustic analogy. A bandpass filter has a center frequency and a bandwidth. The center frequency locates where the filter listens. The bandwidth defines the range of frequencies it captures. The same idea applies to HUF observation scopes.'),
  P('In an acoustic filter, if the center frequency is set to 1000 Hz and the bandwidth is 200 Hz, the filter listens from 900 Hz to 1100 Hz. Frequencies outside that range are attenuated. The observation is optimized for the frequencies of interest within the bandwidth.'),
  P('Similarly, HUF\u2019s observation scope has a focal system (center frequency) and a range of included subsystems (bandwidth). The focal system is the one you are primarily concerned with. The bandwidth is the range of other systems and scales you include in the ratio state.'),
  P('The practical rule: if your observation includes elements where you have no data or cannot compute shares, narrow the bandwidth. Exclude those elements from the active portfolio. The unity constraint applies only to the elements you can actually observe. As new data arrives or becomes available, you can widen the bandwidth and bring in previously excluded elements.'),
  P('This is not loss of information. It is correct scoping. A department that cannot access financial data from a supplier should not include that supplier in its budget ratio. Once the supplier\u2019s data becomes available, the scope can be expanded to include it.'),

  H2('10.3 Dynamic Portfolio Gating'),
  P('In neural networks, a softmax gate or attention mechanism selects which inputs are active in computation based on their magnitude. In audio engineering, a noise gate silences signals below a threshold, activating only signals above the noise floor. These gating mechanisms adapt in real time based on the data.'),
  P('Dynamic portfolio gating applies the same principle to HUF observation. Elements in the portfolio have a noise floor\u2014a minimum significance or observability threshold. Elements above this threshold are included in the active portfolio and contribute to the ratio state. Elements below the threshold are gated out (not deleted, just excluded from the active calculation). As new data arrives, the gate re-evaluates: elements that were below threshold may now rise above it and enter the active set. Elements that drop below threshold exit.'),
  P('The mathematics remain consistent: the unity constraint applies to the gated set. \u03A3\u03C1\u1D62 = 1 only for the elements currently in the active portfolio. When the gate status changes, the ratio state is recomputed over the new gated set. The trace record documents when elements enter and leave the gated portfolio and why.'),
  P('This mechanism prevents false precision. If you have five potential elements in a system but only three produce observable data, you compute shares over the three. The two without data are not assigned zero share (which would be mathematically false); they are gated out. Once data arrives, they re-enter automatically.'),

  H2('10.4 The Sufficiency Frontier at Multiple Scales'),
  P('The sufficiency frontier is not unique to HUF\u2019s corpus analysis. The frontier exists at every scale and in every domain where proportional allocation matters.'),
  P('A cell has a sufficiency frontier. The critical boundary is the concentration of regulatory signals and resources that allows the cell to sustain function. Below that frontier, the cell cannot maintain structure and dies. Above it, the cell is viable. The same ratio-based logic that governs HUF\u2019s portfolio analysis governs the cell\u2019s resource allocation between nucleus, cytoplasm, and organelles.'),
  P('A department has a sufficiency frontier. The critical boundary is the balance of operator attention (management), tool capacity (budget), and external communication that allows the department to deliver its function. Below that frontier, the department cannot sustain its mandate and fails or restructures. The OCC 51/49 contract places the declared intent above the frontier; MC-4 monitoring detects if silent drift is approaching the frontier from below.'),
  P('An organization has a sufficiency frontier. The critical boundary is the balance of stakeholder confidence, financial liquidity, and operational capacity that allows the organization to persist and adapt. Concentration risk\u2014where one stakeholder\u2019s share rises toward 100%\u2014approaches the frontier from above. Fragmentation risk\u2014where many stakeholders have small non-actionable shares\u2014approaches the frontier from below. Both cross the frontier into failure regimes.'),
  P('The scale changes, but the structure does not. Every nested system has a frontier, and the Adaptive Scope principle allows HUF monitoring to apply at any scale by simply choosing the appropriate bandwidth. A researcher studying cell biology can use the same ratio-based analysis tools that a governance analyst uses for organizations, because the underlying mathematics is domain-agnostic.'),

  crossRef('Dynamic monitoring: Pillar 2, Sections 11\u201312 (OCC Drift and Gating)'),
  crossRef('Nested systems in detail: Vol 3, Mathematical Foundations'),
  crossRef('Scale applications: Vol 1\u20134, Domain-Specific Volumes'),
);

// ── 11. HUF-ORG: THE SUFFICIENCY FRONTIER AS METABOLIC BOUNDARY ──────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('11. HUF-Org: The Sufficiency Frontier as Metabolic Boundary'),

  H2('11.1 The Organism Model'),
  P('HUF is not merely a framework; it IS an organism. Like any living system, it has a metabolic energy budget, structural constraints, growth dynamics, and immune defenses. The Sufficiency Frontier represents HUF-org\'s metabolic boundary—the outer membrane across which resources flow in and out.'),
  P('At the core of HUF-org is the conservation law: Σ ρᵢ = 1.0. This is not a target. It is not aspirational. It is metabolic homeostasis. Just as a living cell maintains osmotic balance not by trying, but by the physics of semipermeable membranes, HUF maintains unity not by optimization, but by the structure of the simplex. The sum constraint is a conservation law—a fundamental property of the system, like energy conservation in thermodynamics.'),
  P('HUF-org has:'),
  P('— Conservative energy budget: Σ = 1.0 is to HUF-org what osmotic balance is to cells. It is preserved, not pursued.'),
  P('— Dynamic but constrained growth: The organism can expand and integrate new capabilities, but only iteratively, one element at a time, with portfolio rebalancing at each step.'),
  P('— Slowest member governs stability: Rate of integration is limited by the most Q-sensitive (highest bandwidth, sharpest resonance) element. High-Q members are the fragile ones; they set the speed limit.'),
  P('— Immune system: MC-4 IS the immune system. It detects foreign perturbations (drift), rejects incompatible integrations (Q-sensitivity exceeded), and signals when the organism is under stress.'),

  H2('11.2 What HUF-Org Is Not: Cancer'),
  P('Cancer is uncontrolled growth where one element\'s share rises without portfolio rebalancing. A tumor consumes an ever-larger fraction of body resources, competing with healthy cells, until the organism dies. Cancer is Deceptive Drift in biological form.'),
  P('The tumor\'s rising share is the death signal because it violates the unity constraint. In a finite-budget biological system, a cell type that grows from 1% to 30% to 90% of resources without reciprocal shrinkage of other cell types is parasitic. The tumor grows, but at the expense of survival. The body cannot afford that share ratio.'),
  P('HUF-org, with its tight unity constraint and continuous portfolio gating, is immune to this pathology. If any element\'s share were to rise without corresponding portfolio rebalancing, MC-4 would flag it immediately. The rise would either be approved (explicit reallocation decision), rejected (gating out or downsizing), or investigated (trace artifact, governance record).'),
  P('Cancer is what happens when monitoring fails. HUF-org\'s immune system ensures that monitoring cannot fail.'),

  H2('11.3 Iterative Integration and Q-Sensitivity'),
  P('When HUF-org grows—adding a new capability, integrating a new data source, extending to a new domain—the new element cannot simply be added to the portfolio at arbitrary share. The organism must test compatibility.'),
  P('The integration process is iterative:'),
  P('— Propose: A new element is proposed with an initial small share, say 5% of the nominal portfolio.'),
  P('— Test: Before activating, run the Viability Test (§11.4) on the proposed share.'),
  P('— Integrate: If the test passes, add the element to the active portfolio. All existing elements rebalance slightly to maintain unity.'),
  P('— Monitor: Watch the new element for one to three cycles. Does it stay stable? Does any existing element ring beyond its Q-sensitivity threshold?'),
  P('— Expand (if safe) or Gate Out (if stressed): If stable, slowly increase the new element\'s share in subsequent cycles. If any element exceeds Q tolerance, gate the new element out or narrow its scope.'),
  P('The key principle: Rate of integration is limited by the slowest/most Q-sensitive member. High-Q elements have sharp resonance and narrow bandwidth. They respond sharply to perturbation. Adding a new element when a high-Q member is already near its tolerance margin will push it into instability. The integration rate must respect the Q factors of all existing members.'),
  P('This is analogous to introducing a new species into an ecosystem. You cannot dump a million rabbits into a forest overnight. The predators, the vegetation, the disease vectors all have response times. Integration must proceed at a pace that allows the ecosystem to adapt without collapse.'),

  H2('11.4 The Viability Test: Monte Carlo Perturbation'),
  P('Before any new element is added to the active portfolio, MC-4 runs a perturbation test. The test is a thought experiment:'),
  P('— Freeze the current portfolio and its Q factors.'),
  P('— Introduce the proposed new element with its initial share.'),
  P('— Perturb the new element\'s share across a range (±1σ, ±2σ, ±3σ around the proposed nominal).'),
  P('— At each perturbation level, compute the OCC ratios and all other element responses.'),
  P('— Check: Do any existing elements\' OCC ratios exceed their Q-sensitivity thresholds?'),
  P('If all elements pass at all perturbation levels within ±3σ, the new element is safe to integrate. If any element exceeds its tolerance at any perturbation level, the integration is not safe at the proposed share. Options:'),
  P('— Reduce the proposed share of the new element.'),
  P('— Slow the integration rate (add smaller amounts across more cycles).'),
  P('— Narrow the scope of the new element (exclude or gate out the Q-sensitive member that is in conflict).'),
  P('— Conclude that the new element is fundamentally incompatible with the current organism at the current scope and reject it.'),
  P('The Viability Test is a safety check enforced by the immune system. It prevents the organism from attempting to grow in ways that violate the stability margins of its members. This is how HUF-org avoids cancer.'),

  H2('11.5 Machine Learning as HUF-Org: The Billion-Run Validation'),
  P('The Sufficiency Frontier has a direct expression in Machine Learning: the model\'s capacity boundary. A neural network can represent functions up to a certain complexity—this is its Sufficiency Frontier. Beyond that frontier, the model cannot maintain coherence between training and validation. The frontier is not a gradual degradation; it is a cliff (exactly as in HUF). Overfitting onset is sudden, not gradual. The training loss curve of every model ever trained is a HUF-org growth curve, with complete telemetry. This section establishes ML as a major validation domain for HUF structural principles, providing billions of empirical experiments with recorded metrics.'),

  P('The logistic training curve ', [{ text: 'IS', bold: true }, { text: ' the HUF-org growth curve. K (carrying capacity) = model capacity under architecture constraint. r (growth rate) = learning rate. The inflection point where deceleration begins = the point where combinatorial weight-interaction cost exceeds remaining loss-landscape margin. Both follow the same sigmoid trajectory when resources approach their carrying capacity.' }]),

  P('The weight space of neural networks is a ratio portfolio. In classification networks, the softmax output layer ', [{ text: 'literally enforces Σ=1.0', bold: true }, { text: '—the unity constraint expressed as probability normalization. Every prediction is a ratio portfolio across classes. The weights that feed into softmax are the portfolio elements, each constrained to sum to one. The learned weights of a trained network represent an optimized allocation within the simplex constraint.' }]),

  P('Regularization mechanisms (L1, L2, dropout, weight decay) are the Sufficiency Frontier\'s enforcement tools—they prevent the portfolio from drifting beyond the frontier into the pathological region (overfitting). L2 weight decay monitors the magnitude of each weight (portfolio element) and penalizes growth that exceeds the declared distribution—this IS ratio drift detection. L1 sparsity forces elements to zero when their contribution drops below threshold—this IS dynamic portfolio gating. Dropout randomly removes elements during training, forcing the remaining portfolio to maintain coherence without them—this IS the adaptive scope bandwidth narrowing. Each mechanism exactly mirrors HUF\'s immune system (MC-4) in a different domain.'),

  P('Learning rate as Q-sensitivity: The learning rate governs how aggressively weights are updated. A weight with high gradient curvature (sharp loss landscape = high Q) requires a lower learning rate to avoid oscillation. Adaptive optimizers (Adam, AdaGrad) automatically adjust per-parameter learning rates—they ARE Q-sensitivity monitoring per portfolio element. Each weight gets its own Q-governed integration rate. The optimizer prevents high-Q elements from ringing into instability exactly as HUF\'s integration rate protocol does.'),

  P('The extraordinary validation opportunity: every model training run in history has recorded its loss curve, learning rate schedule, and validation metrics. This is billions of HUF-org experiments with complete telemetry across billions of parameters. The Sufficiency Frontier can be empirically located in any trained model by finding the epoch where validation loss diverges from training loss—that IS the frontier crossing. When the training loss continues downward but validation loss rises, the model has crossed the Sufficiency Frontier into the pathological region. No other validation framework has access to this volume of empirical data. ML provides HUF with direct observational confirmation at unprecedented scale.'),

  P('The structural identity is complete:'),
  P([{ text: '— Learning rate = Q-sensitivity governed integration rate. Too high → oscillation (ringing). Slowest gradient sets speed limit.', indent: 360 }]),
  P([{ text: '— Gradient descent = iterative integration. One batch at a time, full portfolio rebalances after each step.', indent: 360 }]),
  P([{ text: '— Overfitting = Deceptive Drift / cancer. Training accuracy rises (looks like success) while validation drops (death signal). Rising share without rebalancing = pathological.', indent: 360 }]),
  P([{ text: '— Regularization stack = immune system / MC-4. Detects pathological drift, gates out elements, penalizes unconstrained growth.', indent: 360 }]),
  P([{ text: '— Learning rate schedule = decelerating organism. Start fast, slow as carrying capacity approaches. Cosine annealing, step decay = slowing as environment consumed.', indent: 360 }]),
  P([{ text: '— Early stopping = viability test. Validation loss rising while training loss drops = MC-4 catching drift. Stop before cancer kills generalization.', indent: 360 }]),
  P([{ text: '— Batch size = observation bandwidth / adaptive scope. Small batch = narrow BW, high resolution, high variance. Large batch = wide BW, low resolution, low variance.', indent: 360 }]),
  P([{ text: '— Training loss curve = logistic sigmoid / HUF-org growth curve. Carrying capacity K = architecture constraint. Growth rate r = learning rate. Inflection = combinatorial cost exceeds margin.', indent: 360 }]),
  P([{ text: '— Weight space = ratio portfolio under unity constraint. Softmax output layer literally enforces Σ=1.0.', indent: 360 }]),

  crossRef('Adaptive Scope principle: Section 10 (Adaptive Scope)'),
  crossRef('MC-4 immune system: Pillar 2, The Fourth Monitoring Category v2.5'),
  crossRef('Mathematical foundations: Vol 3, Mathematical Foundations'),
  crossRef('ML validation: Billions of empirical HUF-org experiments recorded in training telemetry'),
);

// ── 12. CONCLUSION ────────────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('12. Conclusion'),
  P('The sufficiency frontier marks a qualitative boundary in information reduction. Below it, data is compressed or filtered. Above it, data is reduced to exactly the statistics required for a specified inference. The HUF PreParser operates above this boundary at 6,357,738:1, extracting portfolio governance statistics from heterogeneous data across 10 domains without domain-specific calibration.'),
  P('The theoretical basis is the unity constraint: any system where shares sum to one lives on the probability simplex, and the simplex coordinates are sufficient for governance inference. The empirical basis is a 10-domain corpus spanning mechanical, biological, ecological, digital, astrophysical, acoustic, and institutional systems. The external validation\u2014a Pettitt changepoint matching the exact operational day of ESA Planck\u2019s He-4 exhaustion\u2014provides evidence that the extracted statistics carry genuine physical information.'),
  P('The Adaptive Scope principle extends the sufficiency frontier analysis to operating systems. By matching the observation scope to the data actually present, using center frequency and bandwidth metaphors to guide scoping decisions, and implementing dynamic portfolio gating that adapts to data availability in real time, HUF can monitor nested systems at multiple scales without loss of mathematical rigor.'),
  P('HUF-org extends this framework by modeling HUF itself as a living system with metabolic constraints, iterative integration protocols, and immune-system-like drift detection. The unity constraint Σ ρᵢ = 1.0 is not a governance target but a conservation law. Growth proceeds iteratively, one element at a time, with viability testing before integration. The slowest (highest-Q) member governs the speed of adaptation. MC-4 serves as the immune system, detecting pathological drift (cancer) before it threatens organism survival.'),
  P('The sufficiency frontier is not a property of HUF; it is a property of the inference task. HUF demonstrates that the frontier exists and can be reached without domain-specific knowledge, provided the structural invariant (Σ ρᵢ = 1) holds. The car/fuel analogy illustrates that the frontier is an everyday reality obscured by our habit of thinking in absolute numbers rather than ratios. In any system where budget is conserved and allocation is proportional, the frontier exists, the ratio reveals it, and the adaptive scope framework allows it to be monitored at any scale. As HUF-org matures, the same principles that govern external systems come to govern HUF itself.'),
);

// ── REFERENCES ──────────────────────────────────────────────────────
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  H1('References'),
  P('[1] C.E. Shannon, "A mathematical theory of communication," Bell Syst. Tech. J., vol. 27, pp. 379\u2013423, 1948.'),
  P('[2] R.A. Fisher, "On the mathematical foundations of theoretical statistics," Phil. Trans. R. Soc. A, vol. 222, pp. 309\u2013368, 1922.'),
  P('[3] J. Aitchison, "The statistical analysis of compositional data," J. R. Stat. Soc. B, vol. 44, pp. 139\u2013177, 1982.'),
  P('[4] L. Boltzmann, "Weitere Studien \u00FCber das W\u00E4rmegleichgewicht unter Gasmolek\u00FClen," Sitzungsberichte Akad. Wiss. Wien, vol. 66, pp. 275\u2013370, 1872.'),
  P('[5] E.J.G. Pitman, "Sufficient statistics and intrinsic accuracy," Proc. Cambridge Phil. Soc., vol. 32, pp. 567\u2013579, 1936.'),
  P('[6] B.O. Koopman, "On distributions admitting a sufficient statistic," Trans. Amer. Math. Soc., vol. 39, pp. 399\u2013409, 1936.'),
  P('[7] J. Ziv and A. Lempel, "A universal algorithm for sequential data compression," IEEE Trans. Inf. Theory, vol. 23, pp. 337\u2013343, 1977.'),
  P('[8] G.K. Wallace, "The JPEG still picture compression standard," IEEE Trans. Consum. Electron., vol. 38, pp. 18\u201334, 1992.'),
  P('[9] K. Brandenburg, "MP3 and AAC explained," in Proc. AES 17th Int. Conf., 1999.'),
  P('[10] G.J. Sullivan et al., "Overview of HEVC," IEEE Trans. Circuits Syst. Video Technol., vol. 22, pp. 1649\u20131668, 2012.'),
  P('[11] R.E. Kalman, "A new approach to linear filtering and prediction problems," J. Basic Eng., vol. 82, pp. 35\u201345, 1960.'),
  P('[12] E. Ostrom, Governing the Commons. Cambridge University Press, 1990.'),
  P('[13] Planck Collaboration, "Planck 2013 results. I. Overview," Astron. Astrophys., vol. 571, A1, 2014.'),
  P('[14] A.N. Pettitt, "A non-parametric approach to the change-point problem," Appl. Stat., vol. 28, pp. 126\u2013135, 1979.'),
  P('[15] P. Higgins, "The Fourth Monitoring Category: Ratio State Monitoring," HUF Triad Pillar 2, v2.5, 2026.'),
  P('[16] P. Higgins, "The HUF Triad: Volume 8, Synthesis," v1.0, 2026.'),
  P('[17] J.L. Doob, "Statistical estimation," Trans. Amer. Math. Soc., vol. 39, pp. 410\u2013421, 1936.'),
  P('[18] G. Darmois, "Sur les lois de probabilit\u00E9 \u00E0 estimation exhaustive," C.R. Acad. Sci. Paris, vol. 200, pp. 1265\u20131266, 1935.'),
  P('[19] J. Rissanen, "Modeling by shortest data description," Automatica, vol. 14, pp. 465\u2013471, 1978.'),
  P('[20] T.M. Cover and J.A. Thomas, Elements of Information Theory, 2nd ed. Wiley, 2006.'),
  P('[21] J.L. Fleiss, B. Levin, and M.C. Paik, Statistical Methods for Rates and Proportions, 3rd ed. Wiley, 2003.'),
  P('[22] J. Aitchison and J.A.C. Brown, The Lognormal Distribution. Cambridge University Press, 1957.'),
  P('[23] W.A. Shewhart, Economic Control of Quality of Manufactured Product. Van Nostrand, 1931.'),
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
      page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } },
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MID, space: 1 } },
        children: [
          new TextRun({ text: 'HUF Triad \u2014 Pillar 1', font: 'Times New Roman', size: 18, color: MID }),
          new TextRun({ text: '\tThe Sufficiency Frontier v3.5', font: 'Times New Roman', size: 18, italics: true, color: MID }),
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
    children,
  }],
});

const OUT = __dirname.replace(/[/\\]pillars$/, '') + '/HUF_Sufficiency_Frontier_v3.5.docx';
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log(`\u2714 Generated: ${OUT} (${buf.length.toLocaleString()} bytes)`);
}).catch(err => { console.error('\u274c', err); process.exit(1); });
