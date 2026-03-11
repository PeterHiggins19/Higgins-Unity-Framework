const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require("../node_modules/docx/dist/index.cjs");
const fs = require("fs");

const FONT = "Arial";
const SERIF = "Georgia";
const MONO = "Courier New";
const PG_W = 12240, PG_H = 15840, MARG = 1440;
const CW = PG_W - 2 * MARG; // 9360

// Helpers
const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: t, bold: true, font: FONT, size: 32 })] });
const h2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: t, bold: true, font: FONT, size: 26 })] });
const h3 = t => new Paragraph({ spacing: { before: 200, after: 120 },
  children: [new TextRun({ text: t, bold: true, font: FONT, size: 22 })] });

function para(text, opts = {}) {
  const runs = [];
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  for (const p of parts) {
    if (p.startsWith("**") && p.endsWith("**")) {
      runs.push(new TextRun({ text: p.slice(2, -2), bold: true, font: opts.font || FONT, size: opts.size || 22 }));
    } else {
      runs.push(new TextRun({ text: p, font: opts.font || FONT, size: opts.size || 22,
        italics: opts.italics || false, color: opts.color }));
    }
  }
  return new Paragraph({ spacing: { after: opts.after || 160 }, alignment: opts.align, children: runs });
}

function eq(text) {
  return new Paragraph({ spacing: { before: 120, after: 120 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text, font: MONO, size: 22 })] });
}

let bulletIdx = 0;
const numConfig = [];
for (let i = 0; i < 30; i++) {
  numConfig.push({ reference: `b${i}`, levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022",
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] });
}
function bullet(text) {
  const ref = `b${bulletIdx++}`;
  const runs = [];
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  for (const p of parts) {
    if (p.startsWith("**") && p.endsWith("**")) {
      runs.push(new TextRun({ text: p.slice(2, -2), bold: true, font: FONT, size: 22 }));
    } else {
      runs.push(new TextRun({ text: p, font: FONT, size: 22 }));
    }
  }
  return new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 }, children: runs });
}

// Table helpers
const bdr = { style: BorderStyle.SINGLE, size: 1, color: "999999" };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };
const cellMar = { top: 60, bottom: 60, left: 100, right: 100 };

function hdrCell(text, w) {
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA },
    shading: { fill: "1F3864", type: ShadingType.CLEAR },
    margins: cellMar,
    children: [new Paragraph({ children: [new TextRun({ text, bold: true, font: FONT, size: 20, color: "FFFFFF" })] })] });
}
function cell(text, w, opts = {}) {
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA },
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
    margins: cellMar,
    children: [new Paragraph({ alignment: opts.align,
      children: [new TextRun({ text: String(text), font: opts.mono ? MONO : FONT, size: 20, bold: opts.bold })] })] });
}

// ===================== CONTENT =====================
const c = [];

// Title
c.push(new Paragraph({ spacing: { before: 600, after: 80 }, alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "HUF Case Study: Toronto Transit Commission", bold: true, font: FONT, size: 40 })] }));
c.push(new Paragraph({ spacing: { after: 80 }, alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "Applying the Higgins Unity Framework to GTFS Schedule Data", font: FONT, size: 24, italics: true })] }));
c.push(new Paragraph({ spacing: { after: 40 }, alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "System 10 | K = 5 | Transit Scheduling Domain", font: MONO, size: 20 })] }));
c.push(new Paragraph({ spacing: { after: 300 }, alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "Peter Higgins (Operator) | Grok (xAI) | Claude (Anthropic) | ChatGPT (OpenAI) | Gemini (Google) | Copilot (Microsoft) | 8 March 2026", font: FONT, size: 20, color: "666666" })] }));

// 1. EXECUTIVE SUMMARY
c.push(h1("1. Executive Summary"));
c.push(para("This document presents the tenth validated application of the Higgins Unity Framework (HUF), applied to the Toronto Transit Commission (TTC) General Transit Feed Specification (GTFS) dataset. The analysis processes 4,261,499 stop-events across 230 routes, 133,903 trips, and 9,388 stops to demonstrate that HUF's unity constraint, Monitoring Drift Gain (MDG), and OCC 51/49 governance model apply naturally to urban transit scheduling."));
c.push(para("The TTC system is inherently lopsided: local bus service dominates at 79.8% of all stop-events, with subway comprising only 3.7%. This structural imbalance\u2014which HUF detects as high-drift strict-mode regimes\u2014reflects a real governance question facing transit authorities: how to allocate resources across fundamentally different service modes while maintaining system coherence."));
c.push(para("The inter-day drift analysis (weekday to weekend) reveals Express Bus service drops from 7.1% to 3.1% of system capacity on Sundays, a 399 basis-point drift that HUF flags as the largest single regime shift in the system. This aligns with known TTC scheduling practice and validates MDG as a monitoring instrument for transit operations."));

// 2. DATA SOURCE
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("2. Data Source and Scope"));
c.push(para("The dataset is the official TTC GTFS feed (February 2026 service period, valid 2026-02-08 to 2026-03-14), obtained from the TTC's open data portal. GTFS is the international standard for public transit scheduling, comprising eight interlinked tables:"));

const dataRows = [
  ["agency.txt", "1 record", "TTC agency metadata"],
  ["calendar.txt", "13 service patterns", "Weekday / Saturday / Sunday schedules"],
  ["calendar_dates.txt", "~50 exceptions", "Holiday and special service overrides"],
  ["routes.txt", "230 routes", "Route definitions with mode classification"],
  ["trips.txt", "133,903 trips", "Individual scheduled vehicle runs"],
  ["stop_times.txt", "4,261,499 records", "Every scheduled stop-event (arrival/departure)"],
  ["stops.txt", "9,388 stops", "Physical stop locations with coordinates"],
  ["shapes.txt", "~500K points", "Geographic route geometries"],
];

const dcw = [2800, 2000, 4560];
c.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: dcw,
  rows: [
    new TableRow({ children: [hdrCell("File", dcw[0]), hdrCell("Scale", dcw[1]), hdrCell("Content", dcw[2])] }),
    ...dataRows.map((r, i) => new TableRow({ children: [
      cell(r[0], dcw[0], { mono: true, fill: i % 2 ? "F2F2F2" : undefined }),
      cell(r[1], dcw[1], { align: AlignmentType.RIGHT, fill: i % 2 ? "F2F2F2" : undefined }),
      cell(r[2], dcw[2], { fill: i % 2 ? "F2F2F2" : undefined }),
    ] }))
  ]
}));
c.push(para(""));
c.push(para("The primary capacity measure is **stop-events** (rows in stop_times.txt), not trip counts. A single subway trip touching 30 stations generates 30 stop-events, providing a more accurate representation of service delivery than raw trip counts."));

// 3. REGIME CLASSIFICATION
c.push(h1("3. Regime Classification"));
c.push(para("Routes are classified into K = 5 regimes based on GTFS route_type and route numbering conventions:"));

const regRows = [
  ["Subway", "route_type = 1", "3", "Lines 1 (Yonge-University), 2 (Bloor-Danforth), 4 (Sheppard)"],
  ["LRT (Lines 5\u20136)", "route_type = 0, num \u2208 {5,6}", "2", "Line 5 Eglinton, Line 6 Finch West (+ shuttles)"],
  ["Streetcar", "route_type = 0, 500-series", "18", "501 Queen, 504 King, 510 Spadina, etc."],
  ["Express Bus", "route_num \u2265 900", "28", "900 Airport, 925 Don Mills, 939 Finch, etc."],
  ["Local Bus", "All remaining", "179", "Regular, Night (300s), Community (400s)"],
];

const rcw = [1600, 2200, 900, 4660];
c.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: rcw,
  rows: [
    new TableRow({ children: [hdrCell("Regime", rcw[0]), hdrCell("Classification Rule", rcw[1]),
      hdrCell("Routes", rcw[2]), hdrCell("Examples", rcw[3])] }),
    ...regRows.map((r, i) => new TableRow({ children: [
      cell(r[0], rcw[0], { bold: true, fill: i % 2 ? "F2F2F2" : undefined }),
      cell(r[1], rcw[1], { mono: true, fill: i % 2 ? "F2F2F2" : undefined }),
      cell(r[2], rcw[2], { align: AlignmentType.CENTER, fill: i % 2 ? "F2F2F2" : undefined }),
      cell(r[3], rcw[3], { fill: i % 2 ? "F2F2F2" : undefined }),
    ] }))
  ]
}));
c.push(para(""));
c.push(para("The choice of K = 5 follows Grok's independent calibration on Backblaze data, where K = 4\u20135 emerged from four separate methods (variance minimization, mean balancing, scaling fit, threshold alignment). For transit, K = 5 captures the natural mode hierarchy: heavy rail, light rail, streetcar, express overlay, and local network."));

// 4. HUF RESULTS
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("4. HUF Allocation and MDG Results"));

c.push(h2("4.1 Allocation Weights"));
c.push(para("The allocation weight \u03C1_i for each regime is computed as the fraction of total stop-events:"));
c.push(eq("\u03C1_i = (stop-events in regime i) / (total stop-events)"));
c.push(eq("\u03A3\u03C1_i = 1.0000000000  \u2714 Unity holds"));

const allocRows = [
  ["Local Bus", "179", "100,054", "3,402,706", "0.798476", "79.85%"],
  ["Streetcar", "18", "15,342", "475,878", "0.111669", "11.17%"],
  ["Express Bus", "28", "10,393", "183,660", "0.043098", "4.31%"],
  ["Subway", "3", "6,243", "158,386", "0.037167", "3.72%"],
  ["LRT", "2", "1,871", "40,869", "0.009590", "0.96%"],
];

const acw = [1500, 800, 1200, 1700, 1400, 900];  // sums ~ 7500, pad rest
const acwFull = [1500, 900, 1400, 2000, 1800, 1660];
c.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: acwFull,
  rows: [
    new TableRow({ children: [hdrCell("Regime", acwFull[0]), hdrCell("Routes", acwFull[1]),
      hdrCell("Trips", acwFull[2]), hdrCell("Stop-Events", acwFull[3]),
      hdrCell("\u03C1_i", acwFull[4]), hdrCell("%", acwFull[5])] }),
    ...allocRows.map((r, i) => new TableRow({ children: r.map((v, j) =>
      cell(v, acwFull[j], {
        bold: j === 0,
        align: j > 0 ? AlignmentType.RIGHT : undefined,
        mono: j >= 4,
        fill: i % 2 ? "F2F2F2" : undefined
      })
    ) })),
    new TableRow({ children: [
      cell("TOTAL", acwFull[0], { bold: true, fill: "E8E8E8" }),
      cell("230", acwFull[1], { align: AlignmentType.RIGHT, bold: true, fill: "E8E8E8" }),
      cell("133,903", acwFull[2], { align: AlignmentType.RIGHT, bold: true, fill: "E8E8E8" }),
      cell("4,261,499", acwFull[3], { align: AlignmentType.RIGHT, bold: true, fill: "E8E8E8" }),
      cell("1.000000", acwFull[4], { align: AlignmentType.RIGHT, mono: true, bold: true, fill: "E8E8E8" }),
      cell("100.00%", acwFull[5], { align: AlignmentType.RIGHT, bold: true, fill: "E8E8E8" }),
    ] }),
  ]
}));

c.push(para(""));
c.push(h2("4.2 Monitoring Drift Gain"));
c.push(para("MDG measures deviation from uniform allocation (1/K = 0.2000):"));
c.push(eq("MDG = 20 \u00D7 log\u2081\u2080(drift_bps / K)"));
c.push(eq("drift_bps = |\u03C1_i \u2212 1/K| \u00D7 10,000"));

const mdgRows = [
  ["Local Bus", "5,984.8", "+61.6", "STRICT"],
  ["Streetcar", "883.3", "+44.9", "STRICT"],
  ["Express Bus", "1,569.0", "+49.9", "STRICT"],
  ["Subway", "1,628.3", "+50.3", "STRICT"],
  ["LRT", "1,904.1", "+51.6", "STRICT"],
];

const mcw = [2000, 2000, 2000, 3360];
c.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: mcw,
  rows: [
    new TableRow({ children: [hdrCell("Regime", mcw[0]), hdrCell("Drift (bps)", mcw[1]),
      hdrCell("MDG (dB)", mcw[2]), hdrCell("Governance Mode", mcw[3])] }),
    ...mdgRows.map((r, i) => new TableRow({ children: [
      cell(r[0], mcw[0], { bold: true, fill: i % 2 ? "F2F2F2" : undefined }),
      cell(r[1], mcw[1], { align: AlignmentType.RIGHT, mono: true, fill: i % 2 ? "F2F2F2" : undefined }),
      cell(r[2], mcw[2], { align: AlignmentType.RIGHT, mono: true, fill: i % 2 ? "F2F2F2" : undefined }),
      cell(r[3], mcw[3], { bold: true, fill: i % 2 ? "F2F2F2" : undefined }),
    ] }))
  ]
}));

c.push(para(""));
c.push(para("All five regimes are in strict mode. This is expected and informative: a transit system is not designed for uniform allocation across modes. The high MDG values reflect structural design choices, not failures. The value of HUF here is not to enforce uniformity but to **quantify the degree of structural imbalance** and monitor it over time."));

// 4.3 Statistics
c.push(h2("4.3 System Statistics"));

const statRows = [
  ["Var(\u03C1)", "0.09067303"],
  ["Theoretical 1/(2K\u00B3)", "0.00400000"],
  ["Ratio (empirical/theoretical)", "22.67"],
  ["Herfindahl index", "0.653365"],
  ["Effective K", "1.53"],
  ["Shannon entropy", "1.0488 bits"],
  ["Maximum entropy (log\u2082 5)", "2.3219 bits"],
  ["Entropy efficiency", "45.2%"],
];

const scw = [4680, 4680];
c.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: scw,
  rows: [
    new TableRow({ children: [hdrCell("Metric", scw[0]), hdrCell("Value", scw[1])] }),
    ...statRows.map((r, i) => new TableRow({ children: [
      cell(r[0], scw[0], { fill: i % 2 ? "F2F2F2" : undefined }),
      cell(r[1], scw[1], { mono: true, align: AlignmentType.RIGHT, fill: i % 2 ? "F2F2F2" : undefined }),
    ] }))
  ]
}));

c.push(para(""));
c.push(para("The Herfindahl index of 0.653 yields an effective K of 1.53, meaning the system behaves as if it has roughly 1.5 equal-weight regimes. This is the most concentrated system in the HUF corpus\u2014more concentrated than Backblaze (K_eff \u2248 3.2) or the Croatia Ramsar network (K_eff \u2248 4.1). Transit systems are inherently hierarchical, which makes them an important test case for HUF's ability to characterize rather than merely detect imbalance."));

// 5. INTER-DAY DRIFT
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("5. Inter-Day Drift Analysis"));
c.push(para("The GTFS calendar defines three primary service patterns: weekday (service_id=1), Saturday (service_id=2), and Sunday (service_id=3). HUF treats each as a temporal snapshot and measures allocation drift between them."));

c.push(h2("5.1 Allocation by Day Type"));

const dayRows = [
  ["Local Bus", "0.773879", "0.807667", "0.806954"],
  ["Streetcar", "0.101796", "0.115174", "0.118906"],
  ["Express Bus", "0.070888", "0.032365", "0.031006"],
  ["Subway", "0.042435", "0.035311", "0.033947"],
  ["LRT", "0.011003", "0.009482", "0.009188"],
];

const ddcw = [2000, 2200, 2580, 2580];
c.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: ddcw,
  rows: [
    new TableRow({ children: [hdrCell("Regime", ddcw[0]), hdrCell("\u03C1 Weekday", ddcw[1]),
      hdrCell("\u03C1 Saturday", ddcw[2]), hdrCell("\u03C1 Sunday", ddcw[3])] }),
    ...dayRows.map((r, i) => new TableRow({ children: r.map((v, j) =>
      cell(v, ddcw[j], {
        bold: j === 0, mono: j > 0,
        align: j > 0 ? AlignmentType.RIGHT : undefined,
        fill: i % 2 ? "F2F2F2" : undefined
      })
    ) })),
  ]
}));

c.push(para(""));
c.push(h2("5.2 Drift Decomposition"));

const driftRows = [
  ["Local Bus", "+337.9", "+330.8", "Bus absorbs weekend share"],
  ["Streetcar", "+133.8", "+171.1", "Streetcar gains on weekends"],
  ["Express Bus", "\u2212385.2", "\u2212398.8", "Largest single-regime shift"],
  ["Subway", "\u221271.2", "\u221284.9", "Moderate weekend reduction"],
  ["LRT", "\u221215.2", "\u221218.2", "Near-stable (low base)"],
];

const drcw = [1800, 1500, 1500, 4560];
c.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: drcw,
  rows: [
    new TableRow({ children: [hdrCell("Regime", drcw[0]), hdrCell("Wd\u2192Sat (bps)", drcw[1]),
      hdrCell("Wd\u2192Sun (bps)", drcw[2]), hdrCell("Interpretation", drcw[3])] }),
    ...driftRows.map((r, i) => new TableRow({ children: r.map((v, j) =>
      cell(v, drcw[j], {
        bold: j === 0 || (j < 3 && i === 2),
        mono: j === 1 || j === 2,
        align: (j === 1 || j === 2) ? AlignmentType.RIGHT : undefined,
        fill: i === 2 ? "FFF3E0" : (i % 2 ? "F2F2F2" : undefined),
      })
    ) })),
  ]
}));

c.push(para(""));
c.push(para("**Key finding:** Express Bus service drops from 7.1% to 3.1% on Sundays (\u0394 = \u2212399 bps), the largest single-regime inter-day drift. This reflects TTC's deliberate reduction of commuter-oriented express overlays on weekends. Conversely, Local Bus absorbs the freed capacity, rising from 77.4% to 80.7%."));
c.push(para("The total weekday-to-Sunday drift is 1,004 bps with MDG = +32.1 dB. For comparison, the Backblaze system shows typical inter-snapshot drifts of 50\u2013250 bps. Transit scheduling is a higher-drift environment by design."));

// 6. GOVERNANCE
c.push(h1("6. OCC 51/49 Governance Implications"));
c.push(para("Under HUF governance, the operator (51% authority) retains decision rights over transit allocation. The framework's role is monitoring, not prescription. For the TTC case:"));
c.push(bullet("**All regimes in strict mode** \u2014 high drifts from uniform are structural and intentional. The operator acknowledges this as design policy, not drift failure."));
c.push(bullet("**Express Bus weekend reduction** is the primary actionable drift. The 399 bps weekday-to-Sunday shift should be explicitly documented in service planning as a known governance parameter."));
c.push(bullet("**LRT near-nominal** \u2014 Lines 5 and 6 show the smallest inter-day drifts (15\u201318 bps), suggesting stable, schedule-invariant service. This is consistent with their dedicated right-of-way operations."));
c.push(bullet("**Subway drift moderate** (71\u201385 bps weekday\u2192weekend) \u2014 reflects reduced frequency, not route changes. The operator may choose to maintain this in permissive mode given predictable patterns."));

// 7. CROSS-SYSTEM COMPARISON
c.push(new Paragraph({ children: [new PageBreak()] }));
c.push(h1("7. Cross-System Comparison"));
c.push(para("The TTC becomes the tenth system validated under HUF, and the first in the transit/infrastructure domain:"));

const sysRows = [
  ["1", "Sourdough Fermentation", "4", "Nutrition", "\u2248 2.8"],
  ["2", "Croatia Ramsar Wetland", "5", "Ecology", "\u2248 4.1"],
  ["3", "Software Pipeline", "4", "Technology", "\u2248 3.5"],
  ["4", "Backblaze HDD Fleet", "4", "Technology", "\u2248 3.2"],
  ["5\u20138", "Energy (Croatia/UK/China)", "4\u20135", "Energy", "\u2248 3\u20134"],
  ["9", "Acoustic BTL Cabinet", "3", "Acoustics", "\u2248 2.6"],
  ["10", "TTC Transit (Toronto)", "5", "Transit", "1.53"],
];

const syscw = [600, 2800, 800, 1800, 3360];
c.push(new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: syscw,
  rows: [
    new TableRow({ children: [hdrCell("#", syscw[0]), hdrCell("System", syscw[1]),
      hdrCell("K", syscw[2]), hdrCell("Domain", syscw[3]), hdrCell("Effective K (Herfindahl)", syscw[4])] }),
    ...sysRows.map((r, i) => new TableRow({ children: r.map((v, j) =>
      cell(v, syscw[j], {
        bold: i === 6, mono: j === 2 || j === 4,
        align: (j === 0 || j === 2 || j === 4) ? AlignmentType.CENTER : undefined,
        fill: i === 6 ? "E8F5E9" : (i % 2 ? "F2F2F2" : undefined),
      })
    ) })),
  ]
}));

c.push(para(""));
c.push(para("The TTC's effective K of 1.53 is the lowest in the corpus, confirming that transit systems exhibit extreme hierarchical concentration. This extends HUF's validated domain from relatively balanced systems (Ramsar, K_eff \u2248 4.1) to highly asymmetric ones, demonstrating the framework's generality."));

// 8. METHODOLOGICAL NOTES
c.push(h1("8. Methodological Notes"));
c.push(bullet("**Capacity measure:** Stop-events (not trips, not routes) are the correct capacity proxy for transit. A single Line 1 trip generates ~32 stop-events; a single bus trip generates ~25\u201340. This weights capacity by service reach."));
c.push(bullet("**K selection:** K = 5 follows the natural GTFS route_type taxonomy plus express/local split. Alternative K = 4 (merging LRT into Streetcar) yields similar structure with K_eff = 1.52."));
c.push(bullet("**Temporal grain:** The GTFS feed covers one service period (Feb 8 \u2013 Mar 14, 2026). Multi-period analysis would require historical GTFS archives to compute true time-series MDG."));
c.push(bullet("**Data provenance:** TTC open data, GTFS format (gtfs.org standard). No sampling\u2014full enumeration of all 4.26M scheduled stop-events."));
c.push(bullet("**Grok contribution:** Grok independently proposed the TTC domain and calibrated K = 4 on Backblaze. This case study validates the cross-domain K calibration principle."));

// 9. PROVENANCE
c.push(h1("9. Provenance"));
c.push(para("**Dataset:** TTC GTFS Open Data Feed, February 2026 service period", { size: 20 }));
c.push(para("**Agency:** Toronto Transit Commission (TTC), Toronto, Ontario, Canada", { size: 20 }));
c.push(para("**Analysis date:** 8 March 2026", { size: 20 }));
c.push(para("**Analysts:** Peter Higgins (Operator) | Grok (xAI) | Claude (Anthropic) | ChatGPT (OpenAI) | Gemini (Google) | Copilot (Microsoft)", { size: 20 }));
c.push(para("**Framework version:** HUF v4.0, Trace v4.0", { size: 20 }));
c.push(para("**System designation:** HUF System 10 (Transit Scheduling)", { size: 20 }));
c.push(para("**Constants applied:** K = 5, MDG threshold = 49 bps, OCC = 51/49", { size: 20 }));
c.push(para("**Unity verified:** \u03A3\u03C1_i = 1.0000000000 (all snapshots)", { size: 20 }));

// === BUILD DOC ===
const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: FONT, color: "1F3864" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: FONT, color: "2E75B6" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
    ]
  },
  numbering: { config: numConfig },
  sections: [{
    properties: {
      page: {
        size: { width: PG_W, height: PG_H },
        margin: { top: MARG, right: MARG, bottom: MARG, left: MARG }
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "HUF System 10 | TTC Transit | v1.0", font: FONT, size: 16, color: "999999" })] })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Page ", font: FONT, size: 16, color: "999999" }),
          new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: "999999" })] })] })
    },
    children: c
  }]
});

Packer.toBuffer(doc).then(buf => {
  const out = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/HUF_TTC_CaseStudy_v1.0.docx";
  fs.writeFileSync(out, buf);
  console.log(`\u2714 Written ${out} (${buf.length} bytes, ${c.length} elements)`);
});
