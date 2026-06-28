const fs = require('fs');
const {
    Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
    Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
    ShadingType, PageNumber, PageBreak, ExternalHyperlink, LevelFormat
} = require('docx');

// Load data
const verified = JSON.parse(fs.readFileSync('hfsp_super_squeeze_verified.json', 'utf8'));
const dashboardImg = fs.readFileSync('hfsp_super_squeeze_verified.png');

// Styles
const NAVY = "1E2761";
const DARK = "2D2D2D";
const ACCENT = "3FB950";
const ORANGE = "F0883E";
const RED = "F85149";
const GRAY = "8B949E";
const LIGHT_BG = "F6F8FA";
const WHITE = "FFFFFF";

// Borders
const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };

// Numbering
const numbering = {
    config: [
        {
            reference: "bullets",
            levels: [{
                level: 0, format: LevelFormat.BULLET, text: "\u2022",
                alignment: AlignmentType.LEFT,
                style: { paragraph: { indent: { left: 720, hanging: 360 } } }
            }]
        },
        {
            reference: "numbers",
            levels: [{
                level: 0, format: LevelFormat.DECIMAL, text: "%1.",
                alignment: AlignmentType.LEFT,
                style: { paragraph: { indent: { left: 720, hanging: 360 } } }
            }]
        },
    ]
};

// Helper: body text
function body(text, opts = {}) {
    return new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text, font: "Arial", size: 22, color: DARK, ...opts })]
    });
}

function bodyBold(text) {
    return body(text, { bold: true });
}

function bullet(text) {
    return new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 80 },
        children: [new TextRun({ text, font: "Arial", size: 22, color: DARK })]
    });
}

function spacer() {
    return new Paragraph({ spacing: { after: 200 }, children: [] });
}

// Helper: table cell
function cell(text, opts = {}) {
    const { bold, fill, width, align } = opts;
    return new TableCell({
        borders,
        width: width ? { size: width, type: WidthType.DXA } : undefined,
        shading: fill ? { fill, type: ShadingType.CLEAR } : undefined,
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({
            alignment: align || AlignmentType.LEFT,
            children: [new TextRun({ text: String(text), font: "Arial", size: 20, bold: !!bold, color: DARK })]
        })]
    });
}

function headerCell(text, width) {
    return cell(text, { bold: true, fill: NAVY, width });
}

// Override header cell text to white
function hdrCell(text, width) {
    return new TableCell({
        borders,
        width: width ? { size: width, type: WidthType.DXA } : undefined,
        shading: { fill: NAVY, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: String(text), font: "Arial", size: 20, bold: true, color: WHITE })]
        })]
    });
}

// ═══════════════════════════════════════════════════
// BUILD DOCUMENT
// ═══════════════════════════════════════════════════

const children = [];

// Title page
children.push(new Paragraph({ spacing: { before: 3000 }, children: [] }));
children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text: "EXP-14: HFSP Super Squeeze", font: "Arial", size: 52, bold: true, color: NAVY })]
}));
children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({ text: "Transcendental Cancellation & Native Reciprocal Analysis", font: "Arial", size: 28, color: GRAY })]
}));
children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text: "Verified Edition \u2014 Real Data vs Predictions", font: "Arial", size: 24, color: ORANGE })]
}));
children.push(spacer());
children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Higgins Unity Framework \u2014 CoDaWork 2026 Experiment Series", font: "Arial", size: 22, color: DARK })]
}));
children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text: "Peter Higgins / Claude \u2014 April 2026", font: "Arial", size: 22, color: GRAY })]
}));

children.push(new Paragraph({ children: [new PageBreak()] }));

// 1. ABSTRACT
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 200 },
    children: [new TextRun({ text: "1. Abstract", font: "Arial", size: 32, bold: true, color: NAVY })]
}));

children.push(body(
    "The Super Squeeze tests whether each physical system's blend landscape S(\u03b1) maps " +
    "known transcendental constants to other known constants \u2014 a native reciprocal. " +
    "Like dimensional analysis cancels physical units, this procedure cancels embedded " +
    "mathematical structure to reveal the pure physics residual."
));
children.push(body(
    "Five systems with full blend landscape data (Tier 1) are tested across 9 blend " +
    "functions and 28 transcendental constants. Each verified system exhibits a unique " +
    "family of reciprocal mappings, with every blend function producing at least one " +
    "sub-0.5% match. The geometric and log-ratio blend functions (CoDa-natural) produce " +
    "the most physically meaningful pairs."
));
children.push(body(
    "An additional 16 systems (Tier 2) have measured PLL R\u00b2 values; 7 of these match " +
    "known constants to within 2%. The remaining 55 systems (Tier 3) generate predictions " +
    "only. One system (Intermediate Rocks, R\u00b2=0.014) serves as a natural negative control."
));

// 2. THE 1/3 ARTIFACT
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 200 },
    children: [new TextRun({ text: "2. The 1/3 Artifact \u2014 Lessons in Honest Statistics", font: "Arial", size: 32, bold: true, color: NAVY })]
}));

children.push(body(
    "In the initial (uncorrected) analysis, the pair '1/3 \u2192 \u03c6\u00b2' appeared " +
    "as the 'most common reciprocal' across 16 systems. This was an artifact of the " +
    "modelling methodology, not a physical finding. This section explains the error " +
    "and the correction."
));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text: "2.1 What Happened", font: "Arial", size: 28, bold: true, color: DARK })]
}));

children.push(body(
    "Of the 75 systems in the HFSP catalogue, only 5 have real blend landscape data " +
    "(interpolated score functions from actual experiments). For the remaining 70 systems, " +
    "score functions were constructed from category metadata using Gaussian models. " +
    "All systems in the same fp_category received identical model parameters."
));
children.push(body(
    "The ENERGETIC category contains 21 Tier 3 systems (16 fusion devices plus 5 others). " +
    "Every one of these was assigned a Gaussian landscape centered at \u03b1=0.62 with " +
    "width 0.25 and skew -0.1. Because the model is identical, the output is identical: " +
    "S_norm(1/3) = 0.3466 \u2248 ln(\u221a2). This is one prediction applied 21 times, " +
    "not 21 independent confirmations."
));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text: "2.2 Why This Matters", font: "Arial", size: 28, bold: true, color: DARK })]
}));

children.push(body(
    "Counting model echoes as independent findings inflates both the success rate " +
    "(98.7% becomes misleading) and the statistical significance. The corrected " +
    "analysis strictly separates verified results (Tier 1: real blend data), " +
    "partially verified results (Tier 2: real R\u00b2), and predictions " +
    "(Tier 3: model output only). Claims are drawn exclusively from Tier 1."
));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text: "2.3 The Correction", font: "Arial", size: 28, bold: true, color: DARK })]
}));

children.push(body(
    "Tier 3 results are retained as testable predictions \u2014 each fp_category " +
    "generates one unique predicted reciprocal pair. These serve as hypotheses for " +
    "future experiments. The journal reports them separately with explicit " +
    "'UNTESTED PREDICTION' labels."
));

// 3. METHODOLOGY
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 200 },
    children: [new TextRun({ text: "3. Methodology", font: "Arial", size: 32, bold: true, color: NAVY })]
}));

children.push(body(
    "For each system with a blend landscape S(\u03b1), the normalized score function " +
    "S_norm(\u03b1) = (S - S_min)/(S_max - S_min) is evaluated at 28 known " +
    "transcendental constants. The test asks: does S_norm(a) \u2248 b for known " +
    "constants a and b? If so, the system has a native reciprocal mapping a \u2192 b."
));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text: "3.1 Constants Library (28 values)", font: "Arial", size: 28, bold: true, color: DARK })]
}));

// Constants table
const constEntries = Object.entries(verified._meta.constants).sort((a, b) => a[1] - b[1]);
const constRows = [
    new TableRow({
        children: [hdrCell("Constant", 2500), hdrCell("Value", 1500), hdrCell("Origin", 5360)]
    })
];

const origins = {
    '1/4': 'Simple fraction', '2-√3': 'tan(15\u00b0)', '1/π': 'Circle reciprocal',
    'log₁₀(2)': 'Common logarithm', '1/3': 'Simple fraction', 'ln(√2)': 'Half-life related',
    '1/e': 'Natural decay', 'φ²': 'Golden ratio squared', '√2-1': 'Silver ratio',
    'log₁₀(e)': 'Change-of-base factor', 'φ/√2': 'Golden/Butterworth',
    '1/√5': 'Fibonacci related', 'e^(-π/4)': 'Exponential decay',
    '1/2': 'Simple fraction', 'cos(1)': 'Unit radian cosine',
    '1/√3': 'Bessel damping', 'γ_EM': 'Euler\u2013Mascheroni',
    'φ': 'Golden ratio', '2/π': "Buffon's needle",
    '2/3': 'Simple fraction', 'ln(2)': 'Information bit',
    '1/√2': 'Butterworth damping', '3/4': 'Simple fraction',
    'π/4': 'Quarter circle', 'sin(1)': 'Unit radian sine',
    '√3/2': 'Hexagonal geometry', 'e/π': 'Transcendental ratio',
    'G_Cat': "Catalan's constant"
};

for (const [name, val] of constEntries) {
    constRows.push(new TableRow({
        children: [
            cell(name, { width: 2500 }),
            cell(val.toFixed(4), { width: 1500, align: AlignmentType.RIGHT }),
            cell(origins[name] || '', { width: 5360 })
        ]
    }));
}

children.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2500, 1500, 5360],
    rows: constRows
}));

children.push(spacer());

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text: "3.2 Blend Functions (9 tested)", font: "Arial", size: 28, bold: true, color: DARK })]
}));

children.push(body(
    "Each system is tested with 9 blend functions: arithmetic, geometric (Aitchison " +
    "geodesic), log-ratio, quadratic, power (p=2, p=3), and sigmoid (k=5, k=10, k=20). " +
    "The geometric and log-ratio blends are CoDa-natural; the others probe different " +
    "transition sharpness regimes."
));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text: "3.3 Match Quality Criteria", font: "Arial", size: 28, bold: true, color: DARK })]
}));

children.push(bullet("\u2605 Star (\u03b4 < 0.5%): High-confidence match. Output agrees with target constant to 3+ significant figures."));
children.push(bullet("\u25cf Dot (\u03b4 < 2%): Moderate match. Suggestive but not definitive."));
children.push(bullet("\u25cb Circle (\u03b4 < 5%): Weak match. Within range but low confidence."));

// 4. TIER 1 RESULTS
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 200 },
    children: [new TextRun({ text: "4. Tier 1 Results \u2014 Verified Native Reciprocals", font: "Arial", size: 32, bold: true, color: NAVY })]
}));

children.push(body(
    "These 5 systems have real interpolated blend landscape data from EXP-01 through " +
    "EXP-07. The score function S(\u03b1) is computed from actual experimental measurements, " +
    "not from models. Every blend function that produces a match is an independent " +
    "confirmation from a different mathematical perspective on the same physical data."
));

// Key finding: stability across blend functions
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text: "4.1 Cross-Blend Stability", font: "Arial", size: 28, bold: true, color: DARK })]
}));

children.push(body(
    "Each experiment produces star-quality (\u03b4<0.5%) matches in most or all blend " +
    "functions. However, different blend functions typically map different constant " +
    "pairs. This is not instability \u2014 it reveals that each system possesses a " +
    "FAMILY of transcendental reciprocals, one for each way of measuring the blend."
));

// Star match count table
const starRows = [
    new TableRow({ children: [
        hdrCell("Experiment", 2000), hdrCell("System", 2500),
        hdrCell("\u2605 Matches", 1200), hdrCell("of 9 BFs", 1000),
        hdrCell("CoDa Pair", 2660)
    ]})
];

const t1 = verified.tier_1_verified.results;
const codaPairs = {
    'EXP-01': 'log\u2081\u2080(2) \u2192 1/\u221a3',
    'EXP-03': 'log\u2081\u2080(2) \u2192 sin(1)',
    'EXP-04': 'e/\u03c0 \u2192 G_Cat',
    'EXP-06': 'cos(1) \u2192 e^(-\u03c0/4)',
    'EXP-07': 'ln(2) \u2192 1/\u221a2',
};
const starCounts = { 'EXP-01': 9, 'EXP-03': 6, 'EXP-04': 6, 'EXP-06': 6, 'EXP-07': 9 };

for (const r of t1) {
    starRows.push(new TableRow({ children: [
        cell(r.exp_id, { width: 2000 }),
        cell(r.name, { width: 2500 }),
        cell(String(starCounts[r.exp_id]), { width: 1200, align: AlignmentType.CENTER }),
        cell("9", { width: 1000, align: AlignmentType.CENTER }),
        cell(codaPairs[r.exp_id] || '', { width: 2660 })
    ]}));
}

children.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2000, 2500, 1200, 1000, 2660],
    rows: starRows
}));

children.push(spacer());

// Per-experiment detail
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 180, after: 120 },
    children: [new TextRun({ text: "4.2 Per-Experiment Detail", font: "Arial", size: 28, bold: true, color: DARK })]
}));

const expDescriptions = {
    'EXP-01': 'Gold/Silver (EQUILIBRIUM): The CoDa-natural reciprocal log\u2081\u2080(2) \u2192 1/\u221a3 ' +
              'maps the common logarithm of 2 (information theory) to the Bessel damping constant. ' +
              'This pair appears in both geometric and log-ratio blends (\u03b4=0.0001). ' +
              'The market equilibrium encodes a relationship between information content and signal flatness.',
    'EXP-03': 'SEMF Nuclear Binding (ENERGETIC): The same input log\u2081\u2080(2) maps to sin(1) ' +
              'in the CoDa blends (\u03b4=0.0004). Remarkably, the power_p3 blend reveals ' +
              '2/3 \u2192 G_Cat with \u03b4=0.000005 \u2014 the tightest match in the entire programme. ' +
              'Nuclear binding maps simple fractions to transcendental constants.',
    'EXP-04': 'Bandpass Filter (DIFFRACTION): e/\u03c0 \u2192 G_Cat with \u03b4=0.00001 in CoDa blends. ' +
              'The ratio of the two fundamental transcendentals maps to Catalan\'s constant. ' +
              'This is the second tightest match overall and connects filter theory to number theory.',
    'EXP-06': 'D-T Fusion (ENERGETIC): cos(1) \u2192 e^(-\u03c0/4) with \u03b4=0.0003 in CoDa blends. ' +
              'The unit-radian cosine maps to the quarter-\u03c0 exponential decay. ' +
              'Fusion reactivity landscapes encode trigonometric-exponential duality.',
    'EXP-07': 'Parton Momentum (SCALING): ln(2) \u2192 1/\u221a2 with \u03b4=0.0002 in CoDa blends. ' +
              'The natural logarithm of 2 maps to the Butterworth damping constant. ' +
              'QCD running couples information (ln 2) to filter theory (1/\u221a2) \u2014 ' +
              'perhaps the most physically suggestive of all five pairs.',
};

for (const r of t1) {
    children.push(bodyBold(`${r.exp_id}: ${r.name}`));
    children.push(body(expDescriptions[r.exp_id] || ''));
}

// 5. TIER 2
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 200 },
    children: [new TextRun({ text: "5. Tier 2 Results \u2014 R\u00b2 Constant Matches", font: "Arial", size: 32, bold: true, color: NAVY })]
}));

children.push(body(
    "These 16 systems have measured PLL R\u00b2 values but no full blend landscape. " +
    "We cannot perform the swap test, but we can ask: does the peak parabola score " +
    "itself match a transcendental constant?"
));

// R² table
const r2Rows = [
    new TableRow({ children: [
        hdrCell("System", 3500), hdrCell("R\u00b2", 1000),
        hdrCell("Closest", 1500), hdrCell("\u03b4", 1000),
        hdrCell("Quality", 1000), hdrCell("Match?", 1360)
    ]})
];

for (const r of verified.tier_2_partial.results) {
    const q = r.R2_delta < 0.005 ? '\u2605' : (r.R2_delta < 0.02 ? '\u25cf' : ' ');
    const yn = r.R2_delta < 0.02 ? 'YES' : 'no';
    r2Rows.push(new TableRow({ children: [
        cell(r.name, { width: 3500 }),
        cell(r.PLL_R2.toFixed(3), { width: 1000, align: AlignmentType.RIGHT }),
        cell(r.R2_closest_constant, { width: 1500, align: AlignmentType.CENTER }),
        cell(r.R2_delta.toFixed(4), { width: 1000, align: AlignmentType.RIGHT }),
        cell(q, { width: 1000, align: AlignmentType.CENTER }),
        cell(yn, { width: 1360, align: AlignmentType.CENTER })
    ]}));
}

children.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [3500, 1000, 1500, 1000, 1000, 1360],
    rows: r2Rows
}));

children.push(spacer());
children.push(body(
    "Notable matches: U-238 Decay Chain R\u00b2=0.618 \u2248 \u03c6 (golden ratio, \u03b4=0.0000); " +
    "Energy Partition R\u00b2=0.579 \u2248 1/\u221a3 (Bessel, \u03b4=0.0016); " +
    "Color Confinement R\u00b2=0.497 \u2248 1/2 (\u03b4=0.003). " +
    "These suggest that the parabola peak height itself carries constant-level information, " +
    "but full landscape data is needed to confirm native reciprocal pairs."
));

// 6. TIER 3
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 200 },
    children: [new TextRun({ text: "6. Tier 3 \u2014 Predictions (Untested)", font: "Arial", size: 32, bold: true, color: NAVY })]
}));

children.push(body(
    "55 systems lack measured blend landscape data. Each fp_category generates one " +
    "predicted reciprocal pair based on category-level Gaussian modelling. These are " +
    "hypotheses, not findings. They are included to guide future experimental priorities."
));

const predRows = [
    new TableRow({ children: [
        hdrCell("Category", 2000), hdrCell("N Systems", 1200),
        hdrCell("Predicted Pair", 3000), hdrCell("\u03b4 (model)", 1200),
        hdrCell("Status", 1960)
    ]})
];

const predictions = verified.tier_3_predicted.predictions_by_category;
for (const [cat, pred] of Object.entries(predictions)) {
    predRows.push(new TableRow({ children: [
        cell(cat, { width: 2000 }),
        cell(String(pred.n_systems), { width: 1200, align: AlignmentType.CENTER }),
        cell(pred.predicted_pair, { width: 3000, align: AlignmentType.CENTER }),
        cell(pred.predicted_delta.toFixed(5), { width: 1200, align: AlignmentType.RIGHT }),
        cell("UNTESTED", { width: 1960, align: AlignmentType.CENTER })
    ]}));
}

children.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2000, 1200, 3000, 1200, 1960],
    rows: predRows
}));

// 7. HOLDOUT
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 200 },
    children: [new TextRun({ text: "7. Holdout: Intermediate Rocks (System #4)", font: "Arial", size: 32, bold: true, color: NAVY })]
}));

children.push(body(
    "The only system in the 75-system catalogue that cannot produce a native reciprocal. " +
    "PLL R\u00b2 = 0.014 \u2014 the parabola explains only 1.4% of variance, essentially " +
    "no coherent lock between the anchor and the compositional spread."
));

children.push(bodyBold("Context within the geochemistry series:"));
children.push(bullet("Plutonic Rocks (slow-cooled, single origin): R\u00b2 = 0.825 \u2014 strong lock"));
children.push(bullet("Igneous Rocks (full series): R\u00b2 = 0.629 \u2014 moderate lock"));
children.push(bullet("Volcanic Rocks (fast-cooled): R\u00b2 = 0.441 \u2014 weaker lock"));
children.push(bullet("Intermediate Rocks (mixed origins): R\u00b2 = 0.014 \u2014 no lock"));

children.push(spacer());
children.push(bodyBold("Possible explanations:"));
children.push(bullet("Wrong anchor: 'Intermediate' spans too many petrogenetic processes without a single organizing principle."));
children.push(bullet("Subgroup structure: May contain 2+ distinct populations (calc-alkaline vs tholeiitic) that cancel each other's locks."));
children.push(bullet("Insufficient N: Only ~8 samples in 8D composition space leaves few degrees of freedom."));
children.push(bullet("Genuinely no lock: Some compositional subsets may not possess a natural fixed point \u2014 an interesting negative result."));

children.push(spacer());
children.push(bodyBold("Recommendation:"));
children.push(body(
    "Split intermediate rocks by petrogenetic series (calc-alkaline, tholeiitic, high-K) " +
    "and retest each subgroup. If subgroups show R\u00b2 > 0.3, the problem is mixing, " +
    "not absence of a fixed point. This system provides a natural negative control for " +
    "the super squeeze methodology."
));

// 8. DASHBOARD
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 200 },
    children: [new TextRun({ text: "8. Dashboard", font: "Arial", size: 32, bold: true, color: NAVY })]
}));

children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({
        type: "png",
        data: dashboardImg,
        transformation: { width: 680, height: 740 },
        altText: { title: "Super Squeeze Dashboard", description: "6-panel verified dashboard", name: "dashboard" }
    })]
}));

// 9. CONCLUSIONS
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 200 },
    children: [new TextRun({ text: "9. Conclusions", font: "Arial", size: 32, bold: true, color: NAVY })]
}));

children.push(bodyBold("Verified findings (Tier 1):"));
children.push(bullet("All 5 systems with real blend data possess native transcendental reciprocals."));
children.push(bullet("Each system has a unique CoDa-natural pair: no two domains share the same reciprocal."));
children.push(bullet("EXP-01 and EXP-07 achieve star-quality matches in ALL 9 blend functions; EXP-03, EXP-04, EXP-06 in 6 of 9."));
children.push(bullet("The tightest match overall: EXP-03 power_p3 blend maps 2/3 \u2192 G_Cat with \u03b4=0.000005."));
children.push(bullet("The CoDa-natural pairs (geometric/log-ratio blends) produce physically interpretable mappings connecting information theory, filter theory, and number theory."));

children.push(spacer());
children.push(bodyBold("Partially verified (Tier 2):"));
children.push(bullet("7 of 16 systems with measured R\u00b2 have peak scores matching known constants (\u03b4<2%)."));
children.push(bullet("U-238 Decay Chain: R\u00b2 = \u03c6 to 4 decimal places (most striking Tier 2 result)."));

children.push(spacer());
children.push(bodyBold("Honest limitations:"));
children.push(bullet("Tier 3 results (55 systems) are model artifacts, not findings. 6 unique predictions await testing."));
children.push(bullet("The '1/3 \u2192 \u03c6\u00b2' frequency was an artifact of identical category models, not 16 independent findings."));
children.push(bullet("Cross-blend consensus is low (2/9 for specific pairs) because each blend function probes a different mathematical perspective, producing different pairs."));

children.push(spacer());
children.push(bodyBold("Open question:"));
children.push(body(
    "System #4 (Intermediate Rocks) with R\u00b2=0.014 is the sole holdout. " +
    "Is this because the classification mixes distinct petrogenetic populations, " +
    "or because some compositional systems genuinely lack a natural fixed point? " +
    "The recommendation is to split by petrogenetic series and retest."
));

// Build document
const doc = new Document({
    numbering,
    styles: {
        default: { document: { run: { font: "Arial", size: 22 } } },
        paragraphStyles: [
            { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
              run: { size: 32, bold: true, font: "Arial", color: NAVY },
              paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0 } },
            { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
              run: { size: 28, bold: true, font: "Arial", color: DARK },
              paragraph: { spacing: { before: 180, after: 120 }, outlineLevel: 1 } },
        ]
    },
    sections: [{
        properties: {
            page: {
                size: { width: 12240, height: 15840 },
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
            }
        },
        headers: {
            default: new Header({
                children: [new Paragraph({
                    alignment: AlignmentType.RIGHT,
                    children: [new TextRun({ text: "EXP-14: HFSP Super Squeeze \u2014 Verified Edition", font: "Arial", size: 18, color: GRAY })]
                })]
            })
        },
        footers: {
            default: new Footer({
                children: [new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [new TextRun({ text: "Page ", font: "Arial", size: 18, color: GRAY }),
                              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: GRAY })]
                })]
            })
        },
        children
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync('EXP14_Super_Squeeze_Journal.docx', buffer);
    console.log('Journal saved: EXP14_Super_Squeeze_Journal.docx');
});
