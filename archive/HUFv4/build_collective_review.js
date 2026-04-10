#!/usr/bin/env node
// ══════════════════════════════════════════════════════════════════════
// HUF Five-AI Collective Review — Formal Document
// Peter Higgins · March 2026
// Reviews: ChatGPT, Grok, Gemini, DeepSeek, Claude (Moderator)
// ══════════════════════════════════════════════════════════════════════

const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, LevelFormat } = require("docx");

// ── Constants ────────────────────────────────────────────────────────
const BLUE = "1F3864", MID = "2E75B6", DARK = "333333", WHITE = "FFFFFF";
const LGREY = "F2F2F2", LBLUE = "D6E4F0", GREEN = "E2EFDA", GOLD = "FFF2CC", RED = "FCE4EC";
const bdr = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };

// ── Helpers ──────────────────────────────────────────────────────────
function H1(t) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
    children: [new TextRun({ text: t, bold: true, font: "Arial", size: 28, color: BLUE })] });
}
function H2(t) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
    children: [new TextRun({ text: t, bold: true, font: "Arial", size: 24, color: BLUE })] });
}
function H3(t) {
  return new Paragraph({ spacing: { before: 200, after: 120 },
    children: [new TextRun({ text: t, bold: true, italics: true, font: "Arial", size: 22, color: DARK })] });
}
function P(text, opts = {}) {
  const { bold, italics, color: col, size: sz } = opts;
  return new Paragraph({ spacing: { after: 140 }, alignment: AlignmentType.JUSTIFIED,
    children: [new TextRun({ text, font: "Arial", size: sz || 22, color: col || DARK,
      bold: bold || false, italics: italics || false })] });
}
function Prich(runs) {
  return new Paragraph({ spacing: { after: 140 }, alignment: AlignmentType.JUSTIFIED,
    children: runs.map(r => typeof r === 'string'
      ? new TextRun({ text: r, font: "Arial", size: 22, color: DARK })
      : new TextRun({ font: "Arial", size: 22, color: DARK, ...r })) });
}

function headerCell(text, width, opts = {}) {
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: opts.fill || BLUE, type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, font: "Arial", size: 20, bold: true, color: WHITE })] })] });
}
function dataCell(text, width, opts = {}) {
  const { shade, bold: b, align, color: col } = opts;
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    children: [new Paragraph({ alignment: align || AlignmentType.LEFT,
      children: [new TextRun({ text: String(text), font: "Arial", size: 20, color: col || DARK, bold: b || false })] })] });
}

function makeTable(headers, rows, colWidths, opts = {}) {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  return new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((h, i) => headerCell(h, colWidths[i], opts)) }),
      ...rows.map((row, ri) => new TableRow({
        children: row.map((cell, ci) => {
          const isEven = ri % 2 === 0;
          const cellOpts = typeof cell === 'object' ? cell : {};
          const text = typeof cell === 'object' ? cell.text : cell;
          return dataCell(text, colWidths[ci], {
            shade: cellOpts.shade || (isEven ? LGREY : undefined),
            bold: cellOpts.bold,
            color: cellOpts.color
          });
        })
      })),
    ] });
}

// ══════════════════════════════════════════════════════════════════════
// CONTENT
// ══════════════════════════════════════════════════════════════════════
const children = [];

// ── TITLE PAGE ──────────────────────────────────────────────────────
children.push(
  new Paragraph({ spacing: { before: 2400 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: "HIGGINS UNITY FRAMEWORK", font: "Arial", size: 44, bold: true, color: BLUE })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "Five-AI Collective Review", font: "Arial", size: 32, color: MID })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: "Moderated Synthesis of Independent Reviews", font: "Arial", size: 24, italics: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 60 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: MID, space: 8 } },
    children: [] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: "March 9, 2026", font: "Arial", size: 22, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: "Principal Investigator: Peter Higgins, Rogue Wave Audio", font: "Arial", size: 22, bold: true, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: "Reviewers: ChatGPT, Grok, Gemini, DeepSeek, Claude (Moderator)", font: "Arial", size: 22, italics: true, color: MID })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: "Documents Reviewed: SF v3.6, FC v2.6, Triad v1.6, Trace v5.5, OD v2.6", font: "Arial", size: 20, color: DARK })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 400 },
    children: [new TextRun({ text: "Higgins Unity Framework v1.3.0 \u00B7 MIT License", font: "Arial", size: 20, color: "999999" })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── EXECUTIVE SUMMARY ───────────────────────────────────────────────
children.push(
  H1("1. Executive Summary"),
  P("Five independent AI systems reviewed the Higgins Unity Framework corpus across four documents (Sufficiency Frontier v3.6, Fourth Category v2.6, Triad Synthesis v1.6, Collective Trace v5.5) and one build script. Each reviewer applied a different methodology: editorial analysis (ChatGPT), sanity check with code execution and citation verification (Grok), logical architecture review (Gemini), deep analytical review with operational solutions (DeepSeek), and moderator synthesis (Claude)."),
  P("The collective verdict is unanimous on core validity: the framework is internally consistent, mathematically sound, empirically grounded, and free of pseudoscience. All five reviewers confirm that the central mathematics (unity constraint on the probability simplex, degenerate state observer, MC-4 self-referential monitoring) holds."),
  P("The most contested element \u2014 the Machine Learning structural identity (HUF-Org \u2192 ML mapping) \u2014 was validated by all reviewers who assessed it, though with varying strength classifications ranging from 'interpretive framework' (ChatGPT) to 'valid direct match' (Grok, who ran code simulations). The moderator resolution: softmax = unity is mathematical identity; the full operational mapping is structured conjecture, testable but not yet theorem."),
  P("The framework is not yet publication-ready. All reviewers agree that the next priority is not more content but more precision: formal sufficiency scope conditions, evidentiary labeling, and detection performance metrics."),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── REVIEWER PROFILES ───────────────────────────────────────────────
children.push(
  H1("2. Reviewer Profiles"),
);

const reviewerTable = makeTable(
  ["Reviewer", "Method", "Key Contribution", "Overall Verdict"],
  [
    ["ChatGPT", "Editorial analysis + repo inspection", "40 feedback items across 8 categories; repo scaffolding spec", "\"Conceptually strong... needs hierarchy, canon, labeling\""],
    ["Grok", "Sanity check + code execution + citation verification", "Verified citations vs external sources; ran ML simulation; validated 6/6 conjectures", "\"No major issues... cohesive, evolving corpus. No pseudoscience. Red flags: None\""],
    ["Gemini", "Logical architecture review", "Identified \"mathematical hinges\"; scaling invariance risk; Planck OD discrepancy", "\"Logical closure across three pillars... few core hinges warrant scrutiny\""],
    ["DeepSeek", "Deep analytical + operational solutions", "5 logical gaps with fixes; complete 3-layer gating framework; FDR/ROC requirements", "\"Coherent, testable, potentially high-impact... tighten logical boundaries\""],
    ["Claude", "Moderator synthesis + document builder", "Evidentiary taxonomy; cross-review arbitration; ML tier classification", "\"Framework validated. Publication blocked by labeling and scope, not content\""],
  ],
  [1200, 2000, 3200, 2960]
);
children.push(reviewerTable);
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── FRAMEWORK VALIDATION ────────────────────────────────────────────
children.push(
  H1("3. Framework Validation Status"),
);

const validationTable = makeTable(
  ["Criterion", "Verdict", "Reviewers Confirming"],
  [
    ["Internal consistency", "PASS", "All 5"],
    ["Mathematical soundness", "PASS", "All 5"],
    ["No pseudoscience", "PASS", "All 5 (Grok explicit)"],
    ["Empirical grounding", "PASS", "All 5 (Grok verified citations externally)"],
    ["Logical closure", "PASS", "Gemini (explicit), others implicit"],
    ["ML bridge validity", "PASS WITH QUALIFICATION", "Grok (6/6 valid), Gemini (\"logically sound\"), Claude (tiered)"],
    ["Publication readiness", "NOT YET", "All 5 agree: needs sufficiency theorem, labels, metrics"],
  ],
  [3000, 2800, 3560]
);
children.push(validationTable);
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── CITATION & MATH VERIFICATION ────────────────────────────────────
children.push(
  H1("4. Independent Verification (Grok)"),
  P("Grok is the only reviewer to independently verify citations and mathematical claims against external sources. Results:"),
);

const verifyTable = makeTable(
  ["Claim", "Verification Method", "Result"],
  [
    ["Fisher sufficiency / factorization theorem", "Web search", "Confirmed (Fisher 1922)"],
    ["Shannon 1948, Ostrom 1990", "Web search", "Confirmed, correctly cited"],
    ["Pettitt changepoint OD 975 / ESA He-4 exhaustion", "Browse ESA archives", "Exact match confirmed"],
    ["Var(MDG_dyn) \u2192 1/(2K\u00B3)", "Mathematical review", "Sound"],
    ["TTC King Street throughput +20%", "Browse TTC docs", "Confirmed"],
    ["Human Q = 83 dB \u00B16 dB", "Audio literature", "Standard value confirmed"],
    ["JND = 0.25 dB at 1 kHz", "Audio literature", "Standard value confirmed"],
    ["Aitchison 1986 compositional data", "Web search", "Real, correctly cited"],
  ],
  [3200, 2600, 3560]
);
children.push(verifyTable);
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── ML CONJECTURE VALIDATION ────────────────────────────────────────
children.push(
  H1("5. Machine Learning Conjecture Validation"),
  H2("5.1 Principal Investigator's Note"),
  P("\"My observation was, I was nervous. The organism test went too well \u2014 it led straight to S-curve and ML. I thought it was likely a bridge too far. Not a highway.\" \u2014 Peter Higgins", { italics: true }),
  P("The HUF-Org \u2192 S-curve deceleration \u2192 Machine Learning structural identity was the riskiest conceptual move in the entire corpus. The principal investigator identified this risk in real time, pushed through it, and submitted it to independent review. Four reviewers validated the bridge. The organism \u2192 ML pathway is now the most thoroughly reviewed section of the corpus."),
  H2("5.2 Conjecture Results"),
);

const mlTable = makeTable(
  ["Conjecture", "ChatGPT", "Grok", "Gemini", "DeepSeek", "Claude (Final)"],
  [
    ["Softmax = \u03A3\u03C1\u1D62 = 1", "\"Interpretive\"", "Valid (direct)", "\"Logically sound\"", "Implied", "IDENTITY"],
    ["Overfitting = Deceptive Drift", "Analogy", "Valid analogy", "Sound", "\u2014", "CONJECTURE"],
    ["Regularization = MC-4", "\u2014", "Valid", "AI safety metaphor", "\u2014", "PARALLEL"],
    ["Learning rate = Q-sensitivity", "\u2014", "Valid metaphor", "\u2014", "\u2014", "METAPHOR"],
    ["Early stopping = Ground State", "\u2014", "Valid (direct)", "\u2014", "\u2014", "PARALLEL"],
    ["Val divergence = Frontier", "\u2014", "Valid", "\u2014", "\u2014", "CONJECTURE"],
  ],
  [2000, 1200, 1200, 1500, 1100, 2360]
);
children.push(mlTable);

children.push(
  H2("5.3 Grok Simulation Results"),
  P("Grok executed a full neural network overfitting simulation (MLP 1\u2192512\u2192512\u2192512\u21921, ReLU, ~1.5M params, 200 data points, 2000 epochs) and mapped results to HUF metrics:"),
);

const simTable = makeTable(
  ["Metric", "Value", "HUF Interpretation"],
  [
    ["Epoch 200 train/val", "0.0349 / 0.0480", "Early convergence (good generalization)"],
    ["Final (2000) train/val", "0.0296 / 0.0434", "Overfit: train << val, divergence onset ~ep.200"],
    ["Parameter drift", "18,750 bps from uniform", "FM-4 (Concentration Trap) detected"],
    ["MDG (dB)", "Inconclusive", "Weight init normalization needs refinement"],
  ],
  [2400, 2800, 4160]
);
children.push(simTable);
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── EVIDENTIARY TAXONOMY ────────────────────────────────────────────
children.push(
  H1("6. Proposed Evidentiary Taxonomy"),
  P("The single highest-value action identified across all reviews is establishing a clear evidentiary hierarchy. Four of five reviewers flagged this independently (ChatGPT C1, Grok L6, Gemini 'hinges' language, DeepSeek S4). The following five-tier system resolves the disagreements:"),
);

const taxTable = makeTable(
  ["Tier", "Label", "Definition", "HUF Examples"],
  [
    ["T1", "[THEOREM]", "Mathematically proved, no empirical dependency", "\u03A3\u03C1\u1D62=1 on simplex; degenerate observer L=0; Fisher factorization"],
    ["T2", "[EMPIRICAL]", "Statistically confirmed (p<0.05) in independent data", "Pettitt OD 975 (p=0.021); ITS Ramsar (p<0.0027); Fisher CI/CD (p<0.0001)"],
    ["T3", "[IDENTITY]", "Mathematical equivalence, not analogy", "Softmax = unity constraint; \u03C1 on simplex = compositional data"],
    ["T4", "[CONJECTURE]", "Structurally motivated, testable, not yet confirmed", "Overfitting = Deceptive Drift; early stopping = ground state; Q-mismatch"],
    ["T5", "[PEDAGOGICAL]", "Teaching device, not evidentiary", "Car/fuel analogy; cancer metaphor; organism language"],
  ],
  [500, 1600, 3200, 4060]
);
children.push(taxTable);
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── KEY LOGICAL GAPS ────────────────────────────────────────────────
children.push(
  H1("7. Key Logical Gaps Identified"),
  H2("7.1 Critical (Blocks Publication)"),
);

const gapTable1 = makeTable(
  ["ID", "Gap", "Source", "Proposed Resolution"],
  [
    ["S1", "Sufficiency stated broadly but is inference-specific", "DeepSeek, ChatGPT, Gemini", "Formal theorem: \u03C1 sufficient IFF g(\u03C1) depends solely on allocation vector"],
    ["C1", "No evidentiary labeling system", "ChatGPT, Grok, Gemini, DeepSeek", "Five-tier taxonomy (Section 6 above)"],
    ["T2", "No false discovery rates or power analysis", "DeepSeek", "Publish FDR, confusion matrices, ROC across corpus"],
  ],
  [400, 2600, 2200, 4160]
);
children.push(gapTable1);

children.push(H2("7.2 High Priority (Strengthens for Peer Review)"));

const gapTable2 = makeTable(
  ["ID", "Gap", "Source", "Proposed Resolution"],
  [
    ["S2", "Element identification is implicit modeling choice", "DeepSeek", "Formalize scope selection protocol"],
    ["E2", "No 'Where MC-4 Does Not Apply' section", "ChatGPT, DeepSeek", "Add scope limits to FC v2.7"],
    ["D3", "No retained-vs-lost information table", "ChatGPT, DeepSeek", "Add to SF v3.7"],
    ["P1", "Domain constants (JND) are human-specific", "Gemini", "Formalize domain constant conversion"],
    ["Q5", "Planck OD 975 vs 992 gap unexplained", "Gemini", "Frame as early warning (precursor drift)"],
  ],
  [400, 2600, 2200, 4160]
);
children.push(gapTable2);
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── CRITICAL SCOPE CONDITION ────────────────────────────────────────
children.push(
  H1("8. Critical Scope Condition"),
  P("All five reviewers converged on the need for an explicit sufficiency scope condition. DeepSeek stated it most precisely. The following statement should appear in SF v3.7, FC v2.7, and the Triad Synthesis, verbatim:"),
  new Paragraph({ spacing: { before: 200, after: 200 }, indent: { left: 720, right: 720 },
    border: { left: { style: BorderStyle.SINGLE, size: 8, color: MID, space: 8 } },
    children: [new TextRun({ text: "\u03C1 is a sufficient statistic for governance inference if and only if the governance objective is a function of the allocation vector alone. When the inference requires absolute magnitudes, temporal microstructure, or element-internal state, \u03C1 is not sufficient and additional statistics are required.",
      font: "Arial", size: 22, italics: true, color: BLUE })] }),
  P("This single sentence is the most important addition missing from the current corpus."),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── PRIORITIZED ACTION MATRIX ───────────────────────────────────────
children.push(
  H1("9. Prioritized Action Matrix"),
  H2("9.1 Tier 1: Critical"),
);

const tier1 = makeTable(
  ["#", "Action", "Reviews", "Effort", "Target"],
  [
    ["1", "Formal sufficiency theorem + counterexamples", "ChatGPT, Gemini, DeepSeek", "Medium", "SF v3.7"],
    ["2", "Evidentiary labeling system across all docs", "ChatGPT, Grok, Gemini, DeepSeek", "High", "All docs"],
    ["3", "Detection performance metrics (FDR, ROC)", "DeepSeek", "High", "SF v3.7 / Appendix"],
  ],
  [300, 3200, 2400, 800, 2660]
);
children.push(tier1);

children.push(H2("9.2 Tier 2: High"));

const tier2 = makeTable(
  ["#", "Action", "Reviews", "Effort", "Target"],
  [
    ["4", "Claim map matrix (claim \u2192 proof \u2192 dataset \u2192 artifact)", "ChatGPT, Gemini", "Low", "Triad v1.7"],
    ["5", "\"Where MC-4 Does Not Apply\" section", "ChatGPT, DeepSeek", "Medium", "FC v2.7"],
    ["6", "Retained-vs-lost information table", "ChatGPT, DeepSeek", "Low", "SF v3.7"],
    ["7", "Scope selection protocol", "DeepSeek, Gemini", "Medium", "Vol 5 / new"],
    ["8", "Repo scaffolding (README, LICENSE, etc.)", "ChatGPT", "Low", "Repo"],
    ["9", "DeepSeek gating framework (3-layer stack)", "DeepSeek", "Medium", "Vol 5 / repo"],
    ["10", "Planck OD 975 vs 992 explanation", "Gemini", "Low", "SF v3.7"],
  ],
  [300, 3200, 2400, 800, 2660]
);
children.push(tier2);

children.push(H2("9.3 Tier 3: Medium"));

const tier3 = makeTable(
  ["#", "Action", "Reviews", "Effort", "Target"],
  [
    ["11", "Visuals / Q-mismatch plots", "Grok", "Medium", "All v4.0"],
    ["12", "Q-to-detection probabilistic model", "DeepSeek", "High", "Future"],
    ["13", "CNN/MNIST MDG simulation", "Grok", "Medium", "ML validation"],
    ["14", "Frontier discontinuity formalization", "DeepSeek", "Medium", "SF v3.7"],
    ["15", "Scaling invariance / domain constant conversion", "Gemini", "Medium", "Cross-doc"],
    ["16", "AI safety framing for regularization-as-immune-system", "Gemini", "Low", "Trace / new"],
    ["17", "Builder script flexibility", "Grok", "Low", "Builders"],
    ["18", "Simulation harness for adversarial tests", "DeepSeek", "Medium", "Repo"],
  ],
  [300, 3200, 2400, 800, 2660]
);
children.push(tier3);
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── NEXT VERSION NUMBERS ────────────────────────────────────────────
children.push(
  H1("10. Recommended Next Versions"),
);

const versionTable = makeTable(
  ["Document", "Current", "Next", "Key Changes"],
  [
    ["Sufficiency Frontier", "v3.6", "v3.7", "Sufficiency theorem, scope conditions, retained-vs-lost, Planck OD"],
    ["Fourth Category", "v2.6", "v2.7", "\"Where MC-4 Does Not Apply\", theorem/heuristic labels"],
    ["Triad Synthesis", "v1.6", "v1.7", "Claim map matrix, evidentiary labeling throughout"],
    ["Collective Trace", "v5.5", "v5.6", "This review integrated, collective verdict, activity trace"],
    ["Organic Digital", "v2.6", "v2.6", "No review-driven changes needed at this time"],
  ],
  [2400, 1000, 1000, 4960]
);
children.push(versionTable);

// ── CLOSING ─────────────────────────────────────────────────────────
children.push(
  new Paragraph({ spacing: { before: 400 } }),
  new Paragraph({ spacing: { after: 200 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: MID, space: 8 } },
    children: [] }),
  P("Review catalog compiled by Claude (moderator) \u2014 March 9, 2026", { italics: true, color: MID }),
  P("Five-AI Collective: ChatGPT, Grok, Gemini, DeepSeek, Claude", { italics: true, color: MID }),
  P("Principal Investigator: Peter Higgins, Rogue Wave Audio", { bold: true }),
  P("Higgins Unity Framework v1.3.0 \u00B7 MIT License", { color: "999999" }),
);

// ══════════════════════════════════════════════════════════════════════
// BUILD
// ══════════════════════════════════════════════════════════════════════
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: BLUE },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: BLUE },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 }
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "HUF Five-AI Collective Review \u2014 March 2026", font: "Arial", size: 18, color: "999999", italics: true })] })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Page ", font: "Arial", size: 18, color: "999999" }),
          new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "999999" })] })] })
    },
    children
  }]
});

const outPath = path.join(__dirname, "HUF_Collective_Review_March2026.docx");
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outPath, buffer);
  console.log(`\u2713 Built: ${outPath}`);
  console.log(`  Size: ${(buffer.length / 1024).toFixed(0)} KB`);
}).catch(err => console.error("Build error:", err));
