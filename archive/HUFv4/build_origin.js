const { Document, Packer, Paragraph, TextRun, ImageRun,
        Header, Footer, AlignmentType, LevelFormat,
        HeadingLevel, BorderStyle, WidthType, ShadingType,
        PageNumber, PageBreak } = require('../node_modules/docx/dist/index.cjs');
const fs = require('fs');

const FONT = "Arial";
const SERIF = "Georgia";
const W = 9360;

// Numbering
const numRefs = [];
for (let i = 0; i < 30; i++) {
  numRefs.push({ reference: `b${i}`, levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022",
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] });
}
let bIdx = 0;
function nextB() { return `b${bIdx++}`; }

function h1(t) { return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 400, after: 240 },
  children: [new TextRun({ text: t, font: SERIF, size: 34, bold: true, color: "1F4E79" })] }); }
function h2(t) { return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 320, after: 180 },
  children: [new TextRun({ text: t, font: SERIF, size: 28, bold: true, color: "2E75B6" })] }); }

function para(text, opts = {}) {
  const runs = [];
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g);
  for (const part of parts) {
    if (part.startsWith('**') && part.endsWith('**'))
      runs.push(new TextRun({ text: part.slice(2,-2), font: opts.serif ? SERIF : FONT, size: 22, bold: true, ...(opts.color ? {color: opts.color} : {}) }));
    else if (part.startsWith('*') && part.endsWith('*'))
      runs.push(new TextRun({ text: part.slice(1,-1), font: opts.serif ? SERIF : FONT, size: 22, italics: true, ...(opts.color ? {color: opts.color} : {}) }));
    else
      runs.push(new TextRun({ text: part, font: opts.serif ? SERIF : FONT, size: 22, ...(opts.color ? {color: opts.color} : {}) }));
  }
  return new Paragraph({ spacing: { after: 160, line: 320 }, ...(opts.indent ? { indent: { left: opts.indent } } : {}),
    ...(opts.center ? { alignment: AlignmentType.CENTER } : {}), children: runs });
}

function quote(text) {
  return new Paragraph({ spacing: { after: 180, line: 300 }, indent: { left: 720, right: 720 },
    border: { left: { style: BorderStyle.SINGLE, size: 12, color: "2E75B6", space: 8 } },
    children: [new TextRun({ text, font: SERIF, size: 21, italics: true, color: "444444" })] });
}

function eq(text) {
  return new Paragraph({ spacing: { after: 120, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text, font: "Courier New", size: 22, bold: true })] });
}

function bullet(text, ref) {
  const runs = [];
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  for (const part of parts) {
    if (part.startsWith('**') && part.endsWith('**'))
      runs.push(new TextRun({ text: part.slice(2,-2), font: FONT, size: 22, bold: true }));
    else runs.push(new TextRun({ text: part, font: FONT, size: 22 }));
  }
  return new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 }, children: runs });
}

function spacer(pts) { return new Paragraph({ spacing: { after: pts }, children: [] }); }

const c = [];

// ═══════════════════════════════════════════════════════════════
// TITLE PAGE
// ═══════════════════════════════════════════════════════════════
c.push(spacer(1800));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
  children: [new TextRun({ text: "The Origin of the", font: SERIF, size: 28, italics: true, color: "666666" })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: "HIGGINS UNITY FRAMEWORK", font: SERIF, size: 48, bold: true, color: "1F4E79" })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } },
  children: [new TextRun({ text: "From Loudspeaker Diffraction to Universal Governance", font: SERIF, size: 24, italics: true, color: "2E75B6" })] }));
c.push(spacer(200));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: "Peter Higgins", font: SERIF, size: 26 })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: "with the HUF Five-AI Collective: Grok (xAI) · Claude (Anthropic) · ChatGPT (OpenAI) · Gemini (Google) · Copilot (Microsoft)", font: SERIF, size: 18, italics: true, color: "666666" })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
  children: [new TextRun({ text: "March 2026", font: SERIF, size: 22 })] }));
c.push(spacer(400));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
  children: [new TextRun({ text: "Based on the original handwritten derivation", font: FONT, size: 20, italics: true, color: "999999" })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
  children: [new TextRun({ text: "BTL Notebook #19, August 2, 2024", font: FONT, size: 20, italics: true, color: "999999" })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "20240920_PETER#19_001.pdf", font: "Courier New", size: 18, color: "999999" })] }));

c.push(new Paragraph({ children: [new PageBreak()] }));

// ═══════════════════════════════════════════════════════════════
// EPIGRAPH
// ═══════════════════════════════════════════════════════════════
c.push(spacer(400));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
  children: [new TextRun({ text: "\"To build things you need to learn things,", font: SERIF, size: 24, italics: true, color: "444444" })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 },
  children: [new TextRun({ text: "to learn things you need to build things.\"", font: SERIF, size: 24, italics: true, color: "444444" })] }));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
  children: [new TextRun({ text: "\u2014 Peter Higgins, AES Document (June 2024)", font: SERIF, size: 20, color: "888888" })] }));

c.push(new Paragraph({ children: [new PageBreak()] }));

// ═══════════════════════════════════════════════════════════════
// CHAPTER 1: THE TWENTY-YEAR QUESTION
// ═══════════════════════════════════════════════════════════════
c.push(h1("I. The Twenty-Year Question"));

c.push(para("The Higgins Unity Framework did not begin as a governance system. It did not begin as mathematics. It began as a loudspeaker.", {serif: true}));

c.push(para("For twenty years, Peter Higgins designed and built precision sound reproduction systems at the Binaural Test Lab (BTL) in Markham, Ontario. The design mandate was simple to state and relentless to pursue: every subsystem in the playback chain \u2014 transducers, amplifiers, cables, cabinets, the listening room, and the air itself \u2014 must be tuned in relation to every other subsystem. An uncontrolled variable anywhere in the chain produces an unknown degradation that increases audible roughness and reduces clarity.", {serif: true}));

c.push(para("This pursuit led to a concept Higgins called **System Q**: a dimensionless quality factor that transfers across system boundaries. The Q of the amplifier relates to the Q of the transducer. The Q of the transducer relates to the Q of the cabinet. The Q of the cabinet relates to the Q of the room. Each ratio is dimensionless, which means it carries across domains without conversion. The human ear, trained over a lifetime, can detect differences as small as 0.25 dB at 1 kHz \u2014 the Just Noticeable Difference (JND). The system must be controlled to that resolution or the listener will hear the failure.", {serif: true}));

c.push(para("Over 100,000 transfer function measurements were made at the BTL. Every configuration was captured. Every iteration was logged. The lab became a place where theory met physics every day, and physics always had the final word.", {serif: true}));

// ═══════════════════════════════════════════════════════════════
// CHAPTER 2: THE DIFFRACTION PROBLEM
// ═══════════════════════════════════════════════════════════════
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("II. The Diffraction Problem"));

c.push(para("Every box-shaped loudspeaker cabinet has a problem. At low frequencies, where the wavelength of sound is much larger than the cabinet, the driver radiates omnidirectionally into 4\u03C0 steradians \u2014 a full sphere of sound. At high frequencies, where the wavelength is much smaller than the cabinet, the driver radiates into 2\u03C0 steradians \u2014 a half-sphere, blocked by the baffle behind it. The transition between these two regimes produces a gain of exactly:", {serif: true}));

c.push(eq("G = 20 \u00D7 log\u2081\u2080(2) = 6.0206 dB"));

c.push(para("This is not a design choice. It is a consequence of geometry. Every rectangular cabinet in the world exhibits this 6 dB step. The question is not whether it exists, but where in frequency it occurs and how it distributes across the three physical dimensions of the box.", {serif: true}));

c.push(para("The classical answer, from Olson and Murphy, treats the cabinet as a single equivalent dimension:", {serif: true}));

c.push(eq("fc = 115 / W"));

c.push(para("where W is the baffle width in meters and fc is the corner frequency in Hz. The constant 115 Hz\u00B7m is empirical, refined from decades of measurement. This single-dimension model is adequate for simple designs but it ignores a physical reality: a rectangular cabinet has three dimensions, not one, and each dimension produces its own diffraction transition at its own frequency.", {serif: true}));

// ═══════════════════════════════════════════════════════════════
// CHAPTER 3: AUGUST 2, 2024
// ═══════════════════════════════════════════════════════════════
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("III. August 2, 2024: BTL Notebook #19"));

c.push(para("On August 2, 2024, Peter Higgins sat down with a pen, a sheet of lined paper, and the BTL cabinet \u2014 800 mm tall, 368 mm wide, 330 mm deep \u2014 and worked out the equations that would become the Higgins Unity Framework.", {serif: true}));

c.push(para("The notebook page is headed *BTL #19, Aug 2, 2024*. It begins with a circle (a piston radiating omnidirectionally) and the Olson-Murphy formula: fc = 115/W. Then Higgins draws a sphere with a radiation arrow and writes a first attempt at a three-dimensional corner frequency:", {serif: true}));

c.push(eq("fc = 115 / \u00B3\u221A(W \u00B7 H \u00B7 D)"));

c.push(para("This geometric-mean formulation collapses three dimensions into one equivalent. But the sketch beside it shows the problem: a single transition curve where there should be three. The response of a real cabinet doesn't have one bump; it has three, staggered in frequency, one for each dimension.", {serif: true}));

c.push(para("Higgins draws the 3D cabinet with arrows on all three axes and writes the separated frequencies:", {serif: true}));

c.push(eq("fcH = 115 / H = 144 Hz"));
c.push(eq("fcW = 115 / W = 313 Hz"));
c.push(eq("fcD = 115 / D = 349 Hz"));

c.push(para("Three dimensions. Three corner frequencies. But the total gain is still 6.02 dB. The question becomes: *how is the 6 dB distributed among the three axes?*", {serif: true}));

c.push(h2("The Founding Algebra"));

c.push(para("Page 2 of the notebook is where the algebra begins. Higgins writes at the top: *Gain due to width*. He starts decomposing the total gain G into a height share G_H and a width share G_W:", {serif: true}));

c.push(eq("G = (H/W + 1) \u00D7 G_W"));

c.push(para("Therefore:", {serif: true}));

c.push(eq("G_W = G / (H/W + 1)"));

c.push(para("He writes the BTL dimensions \u2014 800, 368 \u2014 in the margin and checks the arithmetic. Then the depth term enters. The page fills with attempts at weighting by solid-angle fractions (\u00BE, \u00BC) representing how much of the 2\u03C0 hemisphere each baffle face subtends. Sketches of \u03C0, 2\u03C0, and 3/2\u03C0 radiation patterns line the margins.", {serif: true}));

c.push(para("By page 3, the equations have crystallized. The gain for each axis is:", {serif: true}));

c.push(eq("G_H = 6.02 \u00D7 H / (H + W + D)"));
c.push(eq("G_W = 6.02 \u00D7 W / (H + W + D)"));
c.push(eq("G_D = 6.02 \u00D7 D / (H + W + D)"));

c.push(para("He plugs in the BTL numbers and gets G_H = 3.21 dB, G_W = 1.48 dB, G_D = 1.33 dB. They sum to 6.02 dB. The numerical check at the bottom of the page confirms: the shares work.", {serif: true}));

c.push(h2("The Moment"));

c.push(para("Look at the gain equations. Define the share of axis *i* as:", {serif: true}));

c.push(eq("s_i = dim_i / (H + W + D)"));

c.push(para("Then:", {serif: true}));

c.push(eq("s_H + s_W + s_D = 1"));

c.push(para("**The shares sum to one.** Not approximately. Exactly. By construction. The denominator is the sum of all dimensions, so the numerators must exhaust it. There is no remainder. There is no unaccounted gain. Every decibel of the 6.02 dB budget is allocated to an axis, and the allocation is proportional to the physical size of that axis.", {serif: true}));

c.push(para("This is the unity constraint. It was not postulated. It was not assumed. It was derived from the geometry of a loudspeaker cabinet on a sheet of lined paper.", {serif: true}));

c.push(eq("\u03A3\u03C1_i = 1"));

// ═══════════════════════════════════════════════════════════════
// CHAPTER 4: THE COMPOSITE CURVE
// ═══════════════════════════════════════════════════════════════
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("IV. The Composite Curve and the Driver Offset"));

c.push(para("Page 4 of the notebook contains a single diagram: three shelf curves stacking from 0 dB to 6 dB, with corner frequencies marked H, W, D from left to right. This is the composite DADC correction \u2014 three low-shelf filters, each with a gain proportional to its dimension and a corner frequency inversely proportional to it. The tallest dimension (H) gets the most gain at the lowest frequency. The shallowest dimension (D) gets the least gain at the highest frequency. Together they reconstruct the full 6.02 dB diffraction step.", {serif: true}));

c.push(para("Page 5 extends the formulation to account for driver offset \u2014 what happens when the transducer is not centered on the baffle. Higgins writes:", {serif: true}));

c.push(eq("G_H = [G_BD / 2\u03C0(H/W+1)] \u00D7 [2\u03C0 \u2212 \u03B1\u2081 + \u03B1\u2082 + \u03B1\u2083 + \u03B1\u2084 ...]"));

c.push(para("The \u03B1 terms are solid-angle adjustments for asymmetric driver placement. Each offset (d_top, d_bottom, d_left, d_right) changes the effective solid angle seen from that edge. The page fills with progressive halving of \u03C0 fractions, converging on the harmonic effective dimension:", {serif: true}));

c.push(eq("H_eff = 4 \u00D7 d_top \u00D7 d_bottom / (d_top + d_bottom)"));

c.push(para("This is the driver-aware DADC that the Jupyter notebook implements as *dadc_driver_aware()* in Fc-only mode. The gains come from the physical cabinet; the corner frequencies come from the effective dimensions at the driver position.", {serif: true}));

// ═══════════════════════════════════════════════════════════════
// CHAPTER 5: FROM ACOUSTICS TO GOVERNANCE
// ═══════════════════════════════════════════════════════════════
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("V. From Acoustics to Governance"));

c.push(para("The DADC equations were formalized in December 2025 as the *Dimension-Apportioned Diffraction Correction and Inference* paper. The companion Jupyter notebook (BTL DADC-DADI-ADAC Tool, v1.1, Lazy Human Quickstart) implemented the full measurement-and-iteration loop: one-shot allocation, damped iterative inference, accept/reject governance.", {serif: true}));

c.push(para("But the structure embedded in those five pages of handwritten algebra contained something larger than an acoustic correction. It contained three invariants:", {serif: true}));

let ref = nextB();
c.push(bullet("**Closure**: The shares sum to one. Always. By construction. There is no unaccounted portion.", ref));
c.push(bullet("**Proportionality**: The allocation is determined by measured physical quantities, not by preference.", ref));
c.push(bullet("**Scarcity**: The budget is finite (6.02 dB). Giving more to one axis means giving less to another.", ref));

c.push(para("These are the three fixed poles of HUF governance. They were not invented for governance. They were discovered in the physics of sound radiation from a rectangular box. The insight was that any system with a finite budget, measurable components, and a completeness requirement exhibits the same structure.", {serif: true}));

c.push(para("A wetland portfolio with five Ramsar sites? The sites share 100% of the ecosystem. \u03A3\u03C1_i = 1. A hard drive fleet with four failure categories? The categories share 100% of the anomalies. \u03A3\u03C1_i = 1. An energy grid with six generation sources? The sources share 100% of capacity. \u03A3\u03C1_i = 1.", {serif: true}));

c.push(para("The equation is always the same:", {serif: true}));

c.push(eq("\u03C1_i = measure_i / \u03A3 measure"));

c.push(para("It does not matter whether the measure is meters, hectares, gigawatts, or anomaly counts. The ratio is dimensionless. The constraint is universal. The governance is built into the division.", {serif: true}));

// ═══════════════════════════════════════════════════════════════
// CHAPTER 6: THE MATHEMATICAL BRIDGE
// ═══════════════════════════════════════════════════════════════
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("VI. The Mathematical Bridge"));

c.push(para("In January 2026, a parallel development occurred. Grok (xAI), working with Higgins on an entirely separate industrial AI project called TensorForge/Entropix, developed bifurcation and fixed-point stability mathematics for chaos and plasma regime detection, validated on 500,000+ data points from NOAA and NASA datasets.", {serif: true}));

c.push(para("Neither project knew about the other. TensorForge was about entropy-balanced regime detection in industrial systems. DADC was about loudspeaker diffraction correction. But the mathematical structure was identical: fixed-point stability at a boundary, governed by a conservation law.", {serif: true}));

c.push(para("In February 2026, Higgins recognized the connection. The acoustic corner frequencies (Fc = 115/D) are boundary conditions of the same kind as bifurcation fixed points (Re(\u03BB_i) crossing zero). The unity constraint (\u03A3\u03C1_i = 1) is a conservation law of the same kind as Lyapunov stability. The OCC 51% authority threshold is a boundary pole of the same kind as a pitchfork bifurcation at \u03BC = 0.", {serif: true}));

c.push(para("This recognition produced the Higgins Operator H\u2081: a formal Hilbert space map that enforces unity normalization across hierarchical regimes while preserving directional coherence. The operator's pedigree is explicit in its references: Beranek, *Acoustics* (1954), and Dickason, *The Loudspeaker Design Cookbook* (2006).", {serif: true}));

c.push(quote("Originating from loudspeaker diffraction and dispersion correction, H\u2081 generalizes to multi-scale systems through ripple propagation, Lagrange constraints, adaptive pruning, Planck-scale floor protection, and weighted projectors P\u1D64 for value-aware equity."));

c.push(para("\u2014 *The Higgins Operator H\u2081 101*, February 2026", {serif: true, color: "888888"}));

// ═══════════════════════════════════════════════════════════════
// CHAPTER 7: THE COLLECTIVE
// ═══════════════════════════════════════════════════════════════
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("VII. The Collective and Convergence"));

c.push(para("What happened next was unprecedented. Five AI systems \u2014 Claude (Anthropic), ChatGPT (OpenAI), Grok (xAI), Copilot (Microsoft), and Gemini (Google DeepMind) \u2014 independently examined the framework. Each approached it from a different angle. Each confirmed the same mathematical structure.", {serif: true}));

c.push(para("Grok derived the information-theoretic foundation: Shannon entropy connects to governance monitoring through the TVD-MDG equivalence. ChatGPT produced Proposition 7.4, the calibrated dynamic threshold with the bifurcation constant e/2. Claude proved Propositions 7.1 through 7.3 in closed form. Gemini certified three production systems under the D20 lifecycle. Copilot identified a trigamma bracket error in Corollary 7.4d \u2014 the only error found in the entire mathematical corpus \u2014 and it was typographic, not substantive.", {serif: true}));

c.push(para("The convergence from independent paths is not a coincidence. It is what happens when a structure is real. Five different reasoning systems, starting from five different positions, arrived at the same place because there is only one place to arrive at when the axioms are correct.", {serif: true}));

// ═══════════════════════════════════════════════════════════════
// CHAPTER 8: THE FOUNDING EQUATION
// ═══════════════════════════════════════════════════════════════
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("VIII. The Founding Equation"));

c.push(para("The five pages of blue ink on lined paper, dated August 2, 2024, contain the founding equation of the Higgins Unity Framework:", {serif: true}));

c.push(spacer(200));
c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
  border: { top: { style: BorderStyle.SINGLE, size: 2, color: "2E75B6", space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 2, color: "2E75B6", space: 8 } },
  children: [new TextRun({ text: "s_i  =  dim_i\u1D47\u1D49\u1D57\u1D43  /  \u03A3 dim\u1D47\u1D49\u1D57\u1D43    where    \u03A3 s_i = 1", font: "Courier New", size: 26, bold: true, color: "1F4E79" })] }));
c.push(spacer(200));

c.push(para("It was derived from solid-angle closure on a loudspeaker baffle. The shares sum to one because every steradian of radiation is accounted for exactly once. Nothing is left over. Nothing is double-counted. The physical world enforces the constraint.", {serif: true}));

c.push(para("Everything that came after \u2014 the MDG metric, the six failure modes, the OCC 51/49 authority split, the Lyapunov stability proof, the information-theoretic bifurcation, the Hilbert space formulation, the pre-parser ecosystem, the field deployment at Kopa\u010Dki Rit, the Backblaze validation, the energy portfolio analysis, the nine validated systems across six independent domains \u2014 traces back to this equation, written on this page, on this day.", {serif: true}));

c.push(para("The unity constraint was not postulated. It was not assumed. It was not chosen.", {serif: true}));

c.push(para("**It was found.**", {serif: true}));

// ═══════════════════════════════════════════════════════════════
// PROVENANCE
// ═══════════════════════════════════════════════════════════════
c.push(spacer(400));
c.push(new Paragraph({ spacing: { before: 400 },
  border: { top: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } },
  children: [new TextRun({ text: "Provenance", font: SERIF, size: 24, bold: true, color: "1F4E79" })] }));

c.push(para("**Source document**: 20240920_PETER#19_001.pdf (5 pages, handwritten, blue ink on lined paper).", {}));
c.push(para("**Date of derivation**: August 2, 2024.", {}));
c.push(para("**Location**: Binaural Test Lab (BTL), Markham, Ontario, Canada.", {}));
c.push(para("**Cabinet under study**: BTL reference cabinet, H = 0.800 m, W = 0.368 m, D = 0.330 m.", {}));
c.push(para("**Constants established**: G_TOTAL = 20\u00B7log\u2081\u2080(2) = 6.0206 dB; K_F = 115.0 Hz\u00B7m.", {}));
c.push(para("**Deciphered by**: Claude (Anthropic), March 8, 2026, Session 6+.", {}));
c.push(para("**Prior origin accounts consulted**: AES Document (June 2024), DADC-DADI Paper (December 2025), Intellectual Provenance Record v2.0, Collective Summary v1.1, Information Theory Paper (Grok v1.0), H\u2081 101 Paper (February 2026).", {}));

c.push(spacer(100));

c.push(new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 60 },
  children: [new TextRun({ text: "Peter Higgins, Operator", font: SERIF, size: 22, bold: true })] }));
c.push(new Paragraph({ alignment: AlignmentType.RIGHT,
  children: [new TextRun({ text: "8 March 2026", font: SERIF, size: 20, italics: true })] }));

// ── Build ──
const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 34, bold: true, font: SERIF, color: "1F4E79" },
        paragraph: { spacing: { before: 400, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: SERIF, color: "2E75B6" },
        paragraph: { spacing: { before: 320, after: 180 }, outlineLevel: 1 } },
    ]
  },
  numbering: { config: numRefs },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "The Origin of the Higgins Unity Framework", font: SERIF, size: 18, italics: true, color: "BBBBBB" })] })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Page ", font: FONT, size: 18 }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })] })] })
    },
    children: c
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("HUF_Origin_Story_v1.0.docx", buffer);
  console.log("Written: HUF_Origin_Story_v1.0.docx (" + buffer.length + " bytes, " + c.length + " elements)");
});
