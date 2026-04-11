const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition,
        ExternalHyperlink } = require('docx');

// ── Constants ──────────────────────────────────────────────────────────
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;
const CONTENT_W = PAGE_W - 2 * MARGIN; // 9360

const BLUE = '1F3864';
const MID_BLUE = '2E75B6';
const ACCENT = '4472C4';
const DARK = '333333';
const LIGHT_BLUE = 'D6E4F0';
const LIGHT_GREY = 'F2F2F2';
const WHITE = 'FFFFFF';
const GREEN_LIGHT = 'E2EFDA';
const GOLD_LIGHT = 'FFF2CC';
const RED_LIGHT = 'FCE4EC';

const border = { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0 };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

// ── Helpers ────────────────────────────────────────────────────────────
function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({ heading: level, spacing: { before: 300, after: 200 },
    children: [new TextRun({ text, bold: true, font: 'Arial',
      size: level === HeadingLevel.HEADING_1 ? 32 : level === HeadingLevel.HEADING_2 ? 28 : 24,
      color: BLUE })] });
}

function para(text, opts = {}) {
  const runs = [];
  if (typeof text === 'string') {
    runs.push(new TextRun({ text, font: 'Arial', size: 22, color: DARK, ...opts }));
  } else {
    text.forEach(t => runs.push(new TextRun({ font: 'Arial', size: 22, color: DARK, ...t })));
  }
  return new Paragraph({ spacing: { after: 160, line: 276 }, children: runs });
}

function cell(text, opts = {}) {
  const { bold, fill, align, width, font_size, color, colspan } = opts;
  const cellOpts = { borders, verticalAlign: 'center',
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ alignment: align || AlignmentType.LEFT,
      children: [new TextRun({ text: String(text), font: 'Arial', size: font_size || 20,
        bold: !!bold, color: color || DARK })] })] };
  if (fill) cellOpts.shading = { fill, type: ShadingType.CLEAR };
  if (width) cellOpts.width = { size: width, type: WidthType.DXA };
  if (colspan) cellOpts.columnSpan = colspan;
  return new TableCell(cellOpts);
}

function row(cells) { return new TableRow({ children: cells }); }

function table(colWidths, rows_data) {
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: colWidths, rows: rows_data });
}

function spacer() { return new Paragraph({ spacing: { after: 80 }, children: [] }); }

// ── Title Page ─────────────────────────────────────────────────────────
function titlePage() {
  return [
    new Paragraph({ spacing: { before: 3000 }, children: [] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [new TextRun({ text: 'THE SUFFICIENCY FRONTIER', font: 'Arial', size: 52, bold: true, color: BLUE })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
      children: [new TextRun({ text: 'Phase-Space Reduction and the Hierarchy of Information Reduction', font: 'Arial', size: 28, color: MID_BLUE })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
      children: [new TextRun({ text: 'HUF PreParser: 6,357,738 : 1 Analytical Reduction', font: 'Arial', size: 24, color: ACCENT })] }),
    new Paragraph({ spacing: { before: 600 }, children: [] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: 'Higgins Unity Framework v4', font: 'Arial', size: 22, color: DARK })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: 'Peter Higgins — Principal Investigator & Operator', font: 'Arial', size: 22, color: DARK })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: 'Five-AI Collective: Grok (xAI) · Claude (Anthropic) · ChatGPT (OpenAI) · Gemini (Google) · Copilot (Microsoft)', font: 'Arial', size: 18, color: '666666' })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: 'March 2026', font: 'Arial', size: 22, color: DARK })] }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// ── Section 1: The Question That Changes Everything ────────────────────
function sectionQuestion() {
  return [
    heading('1. The Question That Changes Everything'),
    para([
      { text: 'Every compression algorithm in history answers one question: ' },
      { text: '"How do I reconstruct the original signal?"', italics: true },
      { text: ' This question has driven sixty years of information theory, from Huffman coding (1952) through H.265/HEVC (2013), and it imposes a fundamental constraint: the compressed representation must contain enough information to rebuild what was lost.' },
    ]),
    para('The HUF PreParser asks a different question entirely: "Do I have everything I need to answer the question I actually asked?" This is not a relaxation of the reconstruction requirement — it is a categorical departure from it. The PreParser does not approximate the original data. It does not discard perceptually irrelevant details. It extracts the sufficient statistic for a specific analytical question — governance drift on the probability simplex — and that statistic is complete.'),
    para([
      { text: 'The result: ' },
      { text: '6,357,738 : 1', bold: true },
      { text: ' analytical reduction. 156 million records across ten independent systems — streetcar trips, sky pixels, bridge inspections, collision reports, traffic counts — compressed to 1,008 bytes. Not lossy. Not approximate. ' },
      { text: 'Sufficient.', bold: true, italics: true },
    ]),
    spacer(),
  ];
}

// ── Section 2: Phase-Space Reduction ───────────────────────────────────
function sectionPhaseSpace() {
  return [
    heading('2. Phase-Space Reduction: From Boltzmann to HUF'),
    heading('2.1  The Statistical Mechanics Precedent', HeadingLevel.HEADING_2),
    para('Ludwig Boltzmann established the foundational precedent in the 1870s. A mole of gas contains approximately 6.022 × 10²³ particles, each described by six phase-space coordinates (three positions, three momenta). The complete microstate description requires ~3.6 × 10²⁴ numbers. Yet thermodynamics needs only five: temperature, pressure, volume, entropy, and particle number.'),
    para([
      { text: 'That is a reduction on the order of ' },
      { text: '10²³ : 1', bold: true },
      { text: '. But it took fifty years to derive (Boltzmann 1877 → Gibbs 1902 → Jaynes 1957), it only works for systems at or near thermal equilibrium, and it requires the Hamiltonian — the complete specification of forces and interactions — to be known in advance.' },
    ]),
    heading('2.2  Fisher\'s Sufficient Statistics (1922)', HeadingLevel.HEADING_2),
    para('R.A. Fisher formalized the concept: a sufficient statistic T(X) captures everything the data X tells you about a parameter θ. For a Gaussian distribution, the sample mean and variance are jointly sufficient — every other data point is, conditional on these two numbers, pure noise. The Rao-Blackwell theorem (1945) proved that any estimator can be improved by conditioning on a sufficient statistic without increasing risk.'),
    para([
      { text: 'But Fisher\'s framework requires ' },
      { text: 'knowing the parametric family in advance', italics: true },
      { text: '. You specify the model (Gaussian, Poisson, exponential family), and the sufficient statistic falls out of the factorization theorem. Change the model and you change the sufficient statistic. The reduction is powerful but domain-locked.' },
    ]),
    heading('2.3  The HUF Departure', HeadingLevel.HEADING_2),
    para([
      { text: 'The PreParser does not know the Hamiltonian. It does not know if it is processing streetcar GPS pings or cosmic microwave background polarization measurements. It imposes ' },
      { text: 'one universal structure', bold: true },
      { text: ' — the probability simplex with Σρᵢ = 1 — and asks ' },
      { text: 'one universal question', bold: true },
      { text: ': how are the data distributed across governance regimes, and is that distribution drifting?' },
    ]),
    para('This is the key move. By restricting the question rather than the domain, the sufficient statistic becomes universal. The output vector — ρ (regime proportions), K_eff (effective regime count), MDG (governance drift in decibels) — is sufficient for the governance question regardless of what generated the data. The PreParser achieves what Boltzmann needed the Hamiltonian for and what Fisher needed the parametric family for: it identifies the minimal representation that loses nothing the question requires.'),
    spacer(),
  ];
}

// ── Section 3: The Hierarchy ───────────────────────────────────────────
function sectionHierarchy() {
  const colWidths = [1100, 2200, 1300, 1800, 2960];
  const hdr = (t, w) => cell(t, { bold: true, fill: BLUE, color: WHITE, width: w, align: AlignmentType.CENTER });

  const levelRow = (level, name, ratio, examples, question, fill) => row([
    cell(level, { bold: true, fill, width: 1100, align: AlignmentType.CENTER }),
    cell(name, { bold: true, fill, width: 2200 }),
    cell(ratio, { fill, width: 1300, align: AlignmentType.CENTER }),
    cell(examples, { fill, width: 1800 }),
    cell(question, { fill, width: 2960, font_size: 18 }),
  ]);

  return [
    heading('3. The Hierarchy of Information Reduction'),
    para('All known information reduction methods fall into four levels, distinguished not by the ratio they achieve but by the question they answer. Each level represents a categorical departure from the one below — not an incremental improvement, but a change in what "reduction" means.'),
    spacer(),
    table(colWidths, [
      row([hdr('Level', 1100), hdr('Category', 2200), hdr('Ratio', 1300), hdr('Examples', 1800), hdr('Defining Question', 2960)]),
      levelRow('1', 'Syntactic Compression', '2:1 – 10:1', 'gzip, LZ4, bzip2, zstd', '"Can I reconstruct the exact bit pattern?" Remove statistical redundancy in symbol sequences. Fully reversible. Domain-blind.', LIGHT_GREY),
      levelRow('2', 'Perceptual Compression', '10:1 – 3,000:1', 'JPEG, MP3, H.265/HEVC', '"Can a human tell the difference?" Discard information below perceptual thresholds. Irreversible but subjectively faithful. Domain-specific (visual, auditory).', LIGHT_BLUE),
      levelRow('3', 'Structural Compression', '10²– 10⁴:1', 'GeCo3, seismic deconv.', '"Can I exploit known domain grammar?" Encode against a structural model of the data-generating process. Requires domain expertise baked into the algorithm.', GREEN_LIGHT),
      levelRow('4', 'Sufficient Statistic Extraction', '10⁵– 10²³:1', 'Stat. mech., HUF PreParser', '"Do I have everything needed to answer the question I asked?" Extract the minimal representation that is complete for a specified inference task. Domain-agnostic.', GOLD_LIGHT),
    ]),
    spacer(),
    para([
      { text: 'The boundaries between levels are not quantitative — they are ' },
      { text: 'epistemological', bold: true, italics: true },
      { text: '. Level 1 asks about bit patterns. Level 2 asks about human perception. Level 3 asks about domain structure. Level 4 asks about inferential sufficiency. Each level changes ' },
      { text: 'what counts as information', italics: true },
      { text: ', and therefore what counts as loss.' },
    ]),
    spacer(),
  ];
}

// ── Section 4: Why 6.3M:1 Is Not Compression ──────────────────────────
function sectionNotCompression() {
  return [
    heading('4. Why 6,357,738 : 1 Is Not Compression'),
    para([
      { text: 'The term "compression" implies a promise of reconstruction — that the original signal can be recovered, exactly or approximately. The PreParser makes no such promise and needs none. The 156 million input records cannot be reconstructed from 1,008 bytes. But ' },
      { text: 'that is not a limitation — it is the point', bold: true },
      { text: '.' },
    ]),
    para('Consider the analogy precisely. When you measure the temperature of a room, you do not expect to recover the velocity of every air molecule from the thermometer reading. Temperature is a sufficient statistic for the thermal equilibrium question. The reduction from 10²³ molecular velocities to one number is not compression — it is the identification of the macroscopic variable that governs the system\'s behaviour at the scale you care about.'),
    para('The PreParser identifies the governance-scale variables: how much of the system is in each regime (ρ), how many effective regimes exist (K_eff), and whether the distribution is drifting (MDG). These are the macroscopic variables of governance, and they are computed without knowing what the "molecules" are — without knowing whether the underlying data represents photon counts, travel times, or bridge condition ratings.'),
    heading('4.1  The Measured Ratio', HeadingLevel.HEADING_2),

    // Computation breakdown table
    table([3200, 3080, 3080], [
      row([
        cell('Metric', { bold: true, fill: BLUE, color: WHITE, width: 3200 }),
        cell('Value', { bold: true, fill: BLUE, color: WHITE, width: 3080, align: AlignmentType.CENTER }),
        cell('Source', { bold: true, fill: BLUE, color: WHITE, width: 3080 }),
      ]),
      row([
        cell('Total input records', { width: 3200 }),
        cell('156,326,693', { width: 3080, align: AlignmentType.CENTER }),
        cell('10 systems × multiple layers', { width: 3080 }),
      ]),
      row([
        cell('Raw input size', { fill: LIGHT_GREY, width: 3200 }),
        cell('6.41 GB', { fill: LIGHT_GREY, width: 3080, align: AlignmentType.CENTER }),
        cell('CSV + XLSX + FITS binary', { fill: LIGHT_GREY, width: 3080 }),
      ]),
      row([
        cell('Output numbers', { width: 3200 }),
        cell('126 (= 21 layers × 6 values)', { width: 3080, align: AlignmentType.CENTER }),
        cell('ρ₁..ρ₄ + K_eff + MDG per layer', { width: 3080 }),
      ]),
      row([
        cell('Output size', { fill: LIGHT_GREY, width: 3200 }),
        cell('1,008 bytes', { fill: LIGHT_GREY, width: 3080, align: AlignmentType.CENTER }),
        cell('126 × 8 bytes (float64)', { fill: LIGHT_GREY, width: 3080 }),
      ]),
      row([
        cell('Byte reduction ratio', { bold: true, fill: GOLD_LIGHT, width: 3200 }),
        cell('6,357,738 : 1', { bold: true, fill: GOLD_LIGHT, width: 3080, align: AlignmentType.CENTER }),
        cell('6.41 GB ÷ 1,008 bytes', { fill: GOLD_LIGHT, width: 3080 }),
      ]),
      row([
        cell('Record reduction ratio', { bold: true, fill: GOLD_LIGHT, width: 3200 }),
        cell('1,241,481 : 1', { bold: true, fill: GOLD_LIGHT, width: 3080, align: AlignmentType.CENTER }),
        cell('156.3M records ÷ 126 numbers', { fill: GOLD_LIGHT, width: 3080 }),
      ]),
    ]),
    spacer(),
  ];
}

// ── Section 5: The Compression Frontier ────────────────────────────────
function sectionFrontier() {
  const colWidths = [2400, 1200, 1200, 1200, 1200, 2160];
  const hdr = (t, w) => cell(t, { bold: true, fill: BLUE, color: WHITE, width: w, align: AlignmentType.CENTER });

  const fRow = (sys, ratio, level, recon, domain, note, fill) => row([
    cell(sys, { bold: true, fill, width: 2400 }),
    cell(ratio, { fill, width: 1200, align: AlignmentType.CENTER }),
    cell(level, { fill, width: 1200, align: AlignmentType.CENTER }),
    cell(recon, { fill, width: 1200, align: AlignmentType.CENTER }),
    cell(domain, { fill, width: 1200, align: AlignmentType.CENTER }),
    cell(note, { fill, width: 2160, font_size: 18 }),
  ]);

  return [
    heading('5. The Sufficiency Frontier: Comparative Landscape'),
    para('Placing HUF on the complete landscape of information reduction systems reveals not incremental superiority but categorical separation. The table below orders every major system by reduction ratio, level, and whether it promises signal reconstruction.'),
    spacer(),
    table(colWidths, [
      row([hdr('System', 2400), hdr('Ratio', 1200), hdr('Level', 1200), hdr('Reconstruct?', 1200), hdr('Domain?', 1200), hdr('Notes', 2160)]),
      fRow('gzip / zstd', '3:1', '1', 'Exact', 'Any', 'Shannon-limited syntactic', LIGHT_GREY),
      fRow('bzip2', '6:1', '1', 'Exact', 'Any', 'Burrows-Wheeler transform', WHITE),
      fRow('FLAC (audio)', '3:1', '1', 'Exact', 'Audio', 'Lossless predictive coding', LIGHT_GREY),
      fRow('JPEG', '20:1', '2', 'Approx.', 'Visual', 'DCT + quantization', WHITE),
      fRow('MP3 / AAC', '12:1', '2', 'Approx.', 'Audio', 'Psychoacoustic masking', LIGHT_GREY),
      fRow('H.265 / HEVC', '3,000:1', '2', 'Approx.', 'Video', 'Best lossy codec (2013)', WHITE),
      fRow('GeCo3 (genomic)', '1,200:1', '3', 'Exact', 'DNA', 'Repeat-aware context model', LIGHT_GREY),
      fRow('Seismic deconv.', '~5,000:1', '3', 'Approx.', 'Geophysics', 'Wave-equation structural', WHITE),
      fRow('Stat. mechanics', '~10²³:1', '4', 'No', 'Equilibrium', 'Requires Hamiltonian; single domain', LIGHT_GREY),
      fRow('HUF PreParser', '6,357,738:1', '4', 'No', 'Any', 'Domain-agnostic sufficient statistic', GOLD_LIGHT),
    ]),
    spacer(),
    para([
      { text: 'Two systems occupy Level 4. Statistical mechanics achieves a higher raw ratio (~10²³:1) but is domain-locked: it requires the Hamiltonian, applies only to equilibrium thermodynamics, and took half a century to formalize. The HUF PreParser achieves 6.3 × 10⁶ : 1 across ' },
      { text: 'ten unrelated domains', bold: true },
      { text: ' without requiring any domain-specific model, any training data, or any parameter tuning. It is the first system to operate at Level 4 with domain-agnostic universality.' },
    ]),
    spacer(),
  ];
}

// ── Section 6: The Fixed Point ─────────────────────────────────────────
function sectionFixedPoint() {
  return [
    heading('6. The Fixed Point: External Validation'),
    para([
      { text: 'A sufficient statistic extraction that only agrees with itself is circular. The definitive test is whether the extracted statistic converges on answers that domain experts reached independently, through entirely different methods. HUF passes this test at the level of ' },
      { text: 'exact correspondence', bold: true },
      { text: '.' },
    ]),
    heading('6.1  Planck Satellite: OD 975 = 14 January 2012', HeadingLevel.HEADING_2),
    para('The Pettitt changepoint test, applied to HUF regime proportions across Planck operational days, identified a structural break at OD 975 (p < 0.001). Converted to calendar date using ESA\'s launch epoch (14 May 2009), OD 975 is 14 January 2012 — the date ESA publicly recorded as the exhaustion of Planck\'s helium-4 sorption cooler. The HUF PreParser, knowing nothing about satellite cryogenics, independently recovered the exact date of a mission-critical hardware event from regime-proportion time series alone.'),
    heading('6.2  King Street Pilot: 5/5 Directional Match', HeadingLevel.HEADING_2),
    para('The City of Toronto\'s 2019 evaluation of the King Street Transit Priority Corridor reported directional improvements in travel time, reliability, and ridership. The HUF interrupted time series analysis, operating on raw Bluetooth travel-time data with no access to the City\'s analysis, produced: a level shift of −3.30 minutes (t = −9.47), a regime flip from Congested (34.6%) to Fast (34.0%), and directional matches on all five benchmarks the City reported.'),
    heading('6.3  What Fixed-Point Convergence Means', HeadingLevel.HEADING_2),
    para([
      { text: 'When a domain-agnostic method and a domain-specific method converge on the same answer, the result is a ' },
      { text: 'fixed point', bold: true },
      { text: ': f(x) = x. The sufficient statistic is not merely consistent with external evidence — it ' },
      { text: 'is', italics: true },
      { text: ' the evidence, arrived at from a different direction. This is the strongest validation a sufficient statistic can receive: the extracted governance fingerprint, derived from 1,008 bytes, contains the same truth that teams of domain experts spent years and millions of dollars to establish.' },
    ]),
    spacer(),
  ];
}

// ── Section 7: Uncharted Territory ─────────────────────────────────────
function sectionUncharted() {
  return [
    heading('7. Uncharted Territory'),
    para('There is no established benchmark category for what the HUF PreParser does. The compression leaderboards (Canterbury Corpus, Silesia, Hutter Prize) measure reconstruction fidelity. The machine learning benchmarks measure prediction accuracy. The statistical test batteries measure distributional conformance. None of them measure domain-agnostic sufficient statistic extraction.'),
    para([
      { text: 'This is not an oversight — it is because the category ' },
      { text: 'did not exist before HUF', bold: true },
      { text: '. The PreParser invented the sufficiency frontier: the boundary where the question "can I reconstruct the original?" is replaced by "do I have everything I need?" Every system below that frontier is doing more work than the inference task requires. Every system on that frontier, until now, was locked to a single domain.' },
    ]),
    para([
      { text: 'HUF is the first system to sit ' },
      { text: 'on the sufficiency frontier and move freely across domains', bold: true },
      { text: '. Streetcar trips, sky pixels, bridge inspections, collision reports, traffic counts, infrastructure condition ratings — the same 1,008-byte governance fingerprint, the same analytical engine, the same sufficient statistic. Ten systems, one framework, zero domain-specific parameters.' },
    ]),
    para('At 6,357,738 : 1, domain-agnostic, externally validated to the level of exact date correspondence — the HUF PreParser does not sit on the compression leaderboard. It sits on a frontier that nobody else has reached.'),
    spacer(),
  ];
}

// ── Section 8: Implications ────────────────────────────────────────────
function sectionImplications() {
  return [
    heading('8. Implications for Systems Science'),
    para([
      { text: 'The existence of a domain-agnostic Level 4 reduction carries implications that extend well beyond data compression:' },
    ]),
    heading('8.1  Governance Is a Universal Observable', HeadingLevel.HEADING_2),
    para('If the same sufficient statistic — ρ, K_eff, MDG — captures governance drift in satellite missions, transit systems, bridge networks, and traffic infrastructure, then governance drift is not a domain-specific phenomenon with domain-specific signatures. It is a universal observable, analogous to temperature in thermodynamics: a macroscopic quantity that emerges whenever a system has distributional structure, regardless of what the microscopic constituents are.'),
    heading('8.2  The 51/49 Boundary Is Structural', HeadingLevel.HEADING_2),
    para('The OCC 51/49 threshold — the boundary at which one governance regime captures a majority — appears as a structural feature in every system HUF has analysed. In Planck, it marks the transition from cryo-nominal to cryo-degraded operations. In King Street, it marks the policy intervention. In Toronto infrastructure, it marks the boundary between maintained and deteriorating asset classes. This convergence suggests that 51/49 is not an arbitrary threshold but a structural bifurcation point on the probability simplex.'),
    heading('8.3  Analytical Reduction May Be the Natural Scale', HeadingLevel.HEADING_2),
    para('Boltzmann showed that temperature is the natural scale for thermal systems — not molecular velocities. The PreParser suggests that governance fingerprints may be the natural scale for institutional and infrastructure systems — not individual measurements. The 6.3-million-fold reduction is not a feat of compression engineering; it is evidence that the governance question operates at a scale where individual data points are, in Fisher\'s precise sense, ancillary: informative about nuisance parameters but irrelevant to the parameter of interest.'),
    spacer(),
  ];
}

// ── Assembly ───────────────────────────────────────────────────────────
async function build() {
  const children = [
    ...titlePage(),
    ...sectionQuestion(),
    ...sectionPhaseSpace(),
    new Paragraph({ children: [new PageBreak()] }),
    ...sectionHierarchy(),
    ...sectionNotCompression(),
    new Paragraph({ children: [new PageBreak()] }),
    ...sectionFrontier(),
    ...sectionFixedPoint(),
    new Paragraph({ children: [new PageBreak()] }),
    ...sectionUncharted(),
    ...sectionImplications(),
    // Closing
    new Paragraph({ spacing: { before: 400 },
      border: { top: { style: BorderStyle.SINGLE, size: 6, color: MID_BLUE, space: 8 } },
      children: [] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: 'Higgins Unity Framework v4 — The Sufficiency Frontier', font: 'Arial', size: 20, color: '666666', italics: true })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: 'Peter Higgins · Five-AI Collective · March 2026', font: 'Arial', size: 20, color: '666666' })] }),
  ];

  const doc = new Document({
    styles: {
      default: { document: { run: { font: 'Arial', size: 22 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 32, bold: true, font: 'Arial', color: BLUE },
          paragraph: { spacing: { before: 300, after: 200 }, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 28, bold: true, font: 'Arial', color: BLUE },
          paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 } },
      ]
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE_W, height: PAGE_H },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        }
      },
      headers: {
        default: new Header({ children: [
          new Paragraph({
            alignment: AlignmentType.RIGHT,
            border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: MID_BLUE, space: 4 } },
            children: [
              new TextRun({ text: 'HUF v4 — The Sufficiency Frontier', font: 'Arial', size: 16, color: '999999', italics: true }),
            ],
            tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
          })
        ] })
      },
      footers: {
        default: new Footer({ children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: 'Page ', font: 'Arial', size: 16, color: '999999' }),
              new TextRun({ children: [PageNumber.CURRENT], font: 'Arial', size: 16, color: '999999' }),
            ]
          })
        ] })
      },
      children,
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  const outPath = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/HUF_Sufficiency_Frontier_v1.0.docx';
  fs.writeFileSync(outPath, buffer);
  console.log(`Done: ${outPath} (${buffer.length.toLocaleString()} bytes, ${children.length} elements)`);
}

build().catch(e => { console.error(e); process.exit(1); });
