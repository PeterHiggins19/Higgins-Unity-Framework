const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak } = require('/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/node_modules/docx/dist/index.cjs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

function hdr(level, text) {
    return new Paragraph({ heading: level, children: [new TextRun({ text, bold: true })] });
}
function para(text, opts = {}) {
    return new Paragraph({ spacing: { after: 120 }, ...opts,
        children: [new TextRun({ text, size: 22, font: "Arial", ...opts.run })] });
}
function boldPara(label, value) {
    return new Paragraph({ spacing: { after: 80 },
        children: [
            new TextRun({ text: label, bold: true, size: 22, font: "Arial" }),
            new TextRun({ text: value, size: 22, font: "Arial" }),
        ]
    });
}
function dataRow(cells, shade) {
    return new TableRow({
        children: cells.map((text, i) => new TableCell({
            borders, margins: cellMargins,
            width: { size: i === 0 ? 3200 : 1540, type: WidthType.DXA },
            shading: shade ? { fill: "F0F4F8", type: ShadingType.CLEAR } : undefined,
            children: [new Paragraph({ children: [new TextRun({ text: String(text), size: 20, font: "Arial" })] })]
        }))
    });
}
function headerRow(cells) {
    return new TableRow({
        children: cells.map((text, i) => new TableCell({
            borders, margins: cellMargins,
            width: { size: i === 0 ? 3200 : 1540, type: WidthType.DXA },
            shading: { fill: "2E4057", type: ShadingType.CLEAR },
            children: [new Paragraph({ children: [new TextRun({ text, size: 20, font: "Arial", bold: true, color: "FFFFFF" })] })]
        }))
    });
}

const children = [
    // Title block
    hdr(HeadingLevel.HEADING_1, "HUF System 12: ESA Planck Satellite Mission"),
    para("Higgins Unity Framework Case Study — Planck Operational State History (POSH)"),
    boldPara("Version: ", "1.0  |  Date: 2026-03-08  |  Peter Higgins (Operator) | Grok (xAI) | Claude (Anthropic) | ChatGPT (OpenAI) | Gemini (Google) | Copilot (Microsoft)"),
    boldPara("Data Source: ", "ESA Planck Legacy Archive, POSH Catalog R0.14 (PSO_Posh_Cat_R0.14.fits)"),
    boldPara("Domain: ", "Space Science — Satellite Mission Operations"),
    new Paragraph({ children: [new PageBreak()] }),

    // 1. Mission Overview
    hdr(HeadingLevel.HEADING_2, "1. Mission Overview"),
    para("The European Space Agency's Planck satellite (2009-2013) mapped the Cosmic Microwave Background radiation with unprecedented precision across nine frequency channels from 30 to 857 GHz. The Planck Operational State History (POSH) catalog records every significant event during the 4.44-year mission: slews between scan positions, cryogenic system operations, calibration observations, instrument anomalies, and orbital manoeuvres."),
    para("The POSH catalog contains 50,320 time-stamped events across 22 distinct event types, plus 45,663 housekeeping records capturing thermal, positional, and radiation data for each stable pointing period. This dataset represents one of the most meticulously documented space missions in history."),
    boldPara("Mission Duration: ", "1,623 days (May 2009 - October 2013)"),
    boldPara("Total Events: ", "50,320 across 22 event types"),
    boldPara("Stable Pointings: ", "45,663 with 101 housekeeping parameters each"),
    boldPara("FITS Extensions: ", "3 (Events, HouseKeeping, EventIDs lookup)"),
    boldPara("Data Processing: ", "Pure Python binary FITS parser (no astropy dependency)"),

    // 2. Layer 1
    hdr(HeadingLevel.HEADING_2, "2. Layer 1: Event-Type Regime Classification"),
    para("HUF classifies the 50,320 mission events into regimes based on operational function. The raw 22-type distribution reveals an extremely concentrated system dominated by slew_events (46,076, 91.57%), with dtcp_period and od_boundaries as distant secondary types. This is consolidated into K=5 functionally meaningful regimes."),

    hdr(HeadingLevel.HEADING_3, "2.1 Raw Distribution (K=22)"),
    new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3200, 1540, 1540, 1540, 1540],
        rows: [
            headerRow(["Event Type", "Count", "Share", "HHI Contrib", "Cumulative"]),
            dataRow(["slew_events", "46,076", "91.57%", "0.8385", "91.57%"], true),
            dataRow(["dtcp_period", "1,536", "3.05%", "0.0009", "94.62%"], false),
            dataRow(["od_boundaries", "1,531", "3.04%", "0.0009", "97.67%"], true),
            dataRow(["scs_operations", "192", "0.38%", "<0.0001", "98.05%"], false),
            dataRow(["rf_period", "166", "0.33%", "<0.0001", "98.38%"], true),
            dataRow(["(17 others)", "819", "1.63%", "<0.0003", "100.00%"], false),
        ]
    }),
    para(""),
    boldPara("Raw K=22: ", "HHI = 0.840340, Effective K = 1.19 — the most concentrated system in the HUF corpus"),

    hdr(HeadingLevel.HEADING_3, "2.2 Consolidated Regime Distribution (K=5)"),
    para("Natural consolidation groups the 22 event types by operational function:"),
    new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3200, 1540, 1540, 1540, 1540],
        rows: [
            headerRow(["Regime", "Count", "rho_i", "Types Incl.", "Function"]),
            dataRow(["Scanning Operations", "49,165", "0.977047", "4", "Slews + DTCP + OD + PSO"], true),
            dataRow(["Mission Management", "436", "0.008665", "7", "Events + RF + Orbit"], false),
            dataRow(["Instrument Operations", "324", "0.006439", "5", "SCS + HFI/LFI ops"], true),
            dataRow(["Anomalies & Faults", "320", "0.006359", "5", "Cryo + Instr + SVM"], false),
            dataRow(["Calibration & Sources", "75", "0.001490", "1", "Planet scans"], true),
        ]
    }),
    para(""),
    boldPara("Unity Verification: ", "sum(rho_i) = 1.0000000000"),
    boldPara("HHI = ", "0.954780  |  Effective K = 1.05"),
    para("This is the most extreme concentration in the HUF corpus. Planck spent 97.7% of its mission time on its primary function — scanning the sky. The remaining 2.3% splits across management, operations, anomalies, and calibration. For comparison, TTC transit (System 10) had K_eff = 1.53 and Toronto road network (System 11) had K_eff = 3.50."),

    hdr(HeadingLevel.HEADING_3, "2.3 Inter-Phase Drift Analysis"),
    para("Splitting the 1,623-day mission at midpoint reveals operational evolution:"),
    new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3200, 1540, 1540, 1540, 1540],
        rows: [
            headerRow(["Regime", "H1 rho", "H2 rho", "Drift (bps)", "Direction"]),
            dataRow(["Scanning Operations", "0.968636", "0.984644", "+160.1", "Intensifying"], true),
            dataRow(["Mission Management", "0.014991", "0.002950", "-120.4", "Declining"], false),
            dataRow(["Instrument Operations", "0.006114", "0.006732", "+6.2", "Stable"], true),
            dataRow(["Anomalies & Faults", "0.008417", "0.004501", "-39.2", "Improving"], false),
            dataRow(["Calibration & Sources", "0.001842", "0.001173", "-6.7", "Declining"], true),
        ]
    }),
    para(""),
    boldPara("Maximum Drift: ", "Scanning Operations at +160.1 bps (H1 to H2)"),
    boldPara("MDG = ", "20 x log10(|160.1| / 5) = +30.1 dB"),
    para("The drift tells a clear operational story: as the mission matured, Planck spent progressively more time on its core scanning function and less on management overhead and fault recovery. Anomaly rates halved from H1 to H2, indicating a stabilizing mission profile."),
    new Paragraph({ children: [new PageBreak()] }),

    // 3. Layer 2
    hdr(HeadingLevel.HEADING_2, "3. Layer 2: Housekeeping Thermal Stability"),
    para("The second HUF layer analyses the 45,663 stable pointing records using the HFI 100 mK bolometer plate temperature (HFI90_Average). This is the most thermally sensitive instrument stage — the dilution refrigerator that cooled the High Frequency Instrument detectors to 0.1 Kelvin for CMB observations."),

    hdr(HeadingLevel.HEADING_3, "3.1 Thermal Parameter Space"),
    boldPara("Operational Days: ", "91 to 1,617 (1,527 days)"),
    boldPara("HFI 100mK Range: ", "0.102565 K to 0.930111 K"),
    boldPara("HFI 100mK Median: ", "0.102756 K"),
    boldPara("Mean Dwell Duration: ", "2,627.8 seconds (~43.8 minutes per pointing)"),
    para("The enormous range in HFI90 temperature (0.1 K to 0.93 K) reflects the known Planck mission event: the exhaustion of helium-3 and helium-4 coolant in the sorption and dilution coolers. When the cryogenic chain depleted, the bolometer plate warmed from its operational ~0.1 K to nearly 1 K, ending HFI science observations."),

    hdr(HeadingLevel.HEADING_3, "3.2 Thermal Regime Distribution (K=4)"),
    para("HUF classifies each pointing by its deviation from the mission median temperature into quartile-based stability regimes:"),
    new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3200, 1540, 1540, 1540, 1540],
        rows: [
            headerRow(["Regime", "Count", "rho_i", "Dev. Range", "Interpretation"]),
            dataRow(["Ultra-Stable", "11,416", "0.250005", "<= 2.25e-5 K", "Prime science"], true),
            dataRow(["Stable", "11,416", "0.250005", "2.3e-5 - 7.2e-5 K", "Good science"], false),
            dataRow(["Nominal", "16,631", "0.364212", "7.2e-5 - 0.793 K", "Mixed quality"], true),
            dataRow(["Disturbed", "6,200", "0.135777", "> 0.793 K", "Cryo depleted"], false),
        ]
    }),
    para(""),
    boldPara("Unity: ", "sum(rho_i) = 1.0000000000"),
    boldPara("HHI = ", "0.276091  |  Effective K = 3.62"),
    para("Unlike the hyper-concentrated event layer (K_eff = 1.05), the thermal layer shows substantial diversity across regimes (K_eff = 3.62). This reflects the mission's dramatic thermal evolution as cryogen supplies depleted."),

    hdr(HeadingLevel.HEADING_3, "3.3 Thermal Drift: Mission Half Comparison"),
    para("Splitting at operational day 854 (mission midpoint) reveals the most dramatic drift in the entire HUF corpus:"),
    new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3200, 1540, 1540, 1540, 1540],
        rows: [
            headerRow(["Regime", "H1 rho", "H2 rho", "Drift (bps)", "Interpretation"]),
            dataRow(["Ultra-Stable", "0.481339", "0.013249", "-4,680.9", "Cryo depletion"], true),
            dataRow(["Stable", "0.443237", "0.052244", "-3,909.9", "Cryo depletion"], false),
            dataRow(["Nominal", "0.075424", "0.659769", "+5,843.4", "Transition zone"], true),
            dataRow(["Disturbed", "0.000000", "0.274737", "+2,747.4", "Post-cryo ops"], false),
        ]
    }),
    para(""),
    boldPara("Maximum Thermal Drift: ", "Nominal regime at +5,843.4 bps"),
    boldPara("MDG_thermal = ", "20 x log10(|5,843.4| / 4) = +63.3 dB"),
    para("This +63.3 dB MDG is the highest drift signal in the entire HUF corpus, surpassing King Street Pilot (+51.8 dB) and all prior systems. It captures a physical phase transition: the irreversible depletion of Planck's cryogenic consumables. In the first mission half, 92.5% of pointings were Ultra-Stable or Stable. In the second half, only 6.5% maintained those regimes while 93.5% shifted to Nominal or Disturbed."),
    new Paragraph({ children: [new PageBreak()] }),

    // 4. Cross-Layer Synthesis
    hdr(HeadingLevel.HEADING_2, "4. Cross-Layer Synthesis"),
    para("The two layers reveal complementary facets of the Planck mission:"),

    hdr(HeadingLevel.HEADING_3, "4.1 Concentration vs. Diversity"),
    para("Layer 1 (events) shows extreme concentration: the satellite did essentially one thing — scan the sky (K_eff = 1.05). Layer 2 (thermal) shows rich diversity in how well it did it (K_eff = 3.62). This is the HUF analogue of saying 'single mission, multiple operating conditions' — a pattern unique to space science in the corpus."),

    hdr(HeadingLevel.HEADING_3, "4.2 Drift as Physical Narrative"),
    para("The event drift (+160 bps, MDG +30.1 dB) tells an operational story: the mission became more efficient over time, spending more time scanning and less on management. The thermal drift (+5,843 bps, MDG +63.3 dB) tells a physical story: consumable resources were exhausted, fundamentally altering the instrument's capability. Together they demonstrate HUF's ability to distinguish operational evolution from physical degradation."),

    hdr(HeadingLevel.HEADING_3, "4.3 Corpus Position"),
    new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2340, 1170, 1170, 1170, 1170, 1170, 1170],
        rows: [
            new TableRow({
                children: ["System", "K", "K_eff", "HHI", "Max Drift", "MDG", "Domain"].map((text, i) =>
                    new TableCell({
                        borders, margins: cellMargins,
                        width: { size: i === 0 ? 2340 : 1170, type: WidthType.DXA },
                        shading: { fill: "2E4057", type: ShadingType.CLEAR },
                        children: [new Paragraph({ children: [new TextRun({ text, size: 18, font: "Arial", bold: true, color: "FFFFFF" })] })]
                    })
                )
            }),
            new TableRow({
                children: ["Planck Events", "5", "1.05", "0.9548", "+160 bps", "+30.1 dB", "Space Sci."].map((text, i) =>
                    new TableCell({
                        borders, margins: cellMargins,
                        width: { size: i === 0 ? 2340 : 1170, type: WidthType.DXA },
                        shading: { fill: "F0F4F8", type: ShadingType.CLEAR },
                        children: [new Paragraph({ children: [new TextRun({ text, size: 18, font: "Arial" })] })]
                    })
                )
            }),
            new TableRow({
                children: ["Planck Thermal", "4", "3.62", "0.2761", "+5,843 bps", "+63.3 dB", "Space Sci."].map((text, i) =>
                    new TableCell({
                        borders, margins: cellMargins,
                        width: { size: i === 0 ? 2340 : 1170, type: WidthType.DXA },
                        children: [new Paragraph({ children: [new TextRun({ text, size: 18, font: "Arial" })] })]
                    })
                )
            }),
            new TableRow({
                children: ["TTC Transit", "5", "1.53", "0.6526", "+160 bps", "+30.1 dB", "Transit"].map((text, i) =>
                    new TableCell({
                        borders, margins: cellMargins,
                        width: { size: i === 0 ? 2340 : 1170, type: WidthType.DXA },
                        shading: { fill: "F0F4F8", type: ShadingType.CLEAR },
                        children: [new Paragraph({ children: [new TextRun({ text, size: 18, font: "Arial" })] })]
                    })
                )
            }),
            new TableRow({
                children: ["Toronto Infra", "6", "3.50", "0.2857", "+1,559 bps", "+51.8 dB", "Infra"].map((text, i) =>
                    new TableCell({
                        borders, margins: cellMargins,
                        width: { size: i === 0 ? 2340 : 1170, type: WidthType.DXA },
                        children: [new Paragraph({ children: [new TextRun({ text, size: 18, font: "Arial" })] })]
                    })
                )
            }),
        ]
    }),
    para(""),
    para("System 12 extends HUF into its third domain (space science), joining transit and infrastructure. The Planck thermal layer holds the corpus MDG record at +63.3 dB."),
    new Paragraph({ children: [new PageBreak()] }),

    // 5. OCC 51/49
    hdr(HeadingLevel.HEADING_2, "5. OCC 51/49 Governance Note"),
    para("The Planck POSH analysis was conducted under full HUF protocol. The pure Python FITS parser bypassed proxy-blocked astronomy libraries while maintaining data fidelity — all 50,320 events and 45,663 housekeeping records were extracted and verified against the POSH ReadMe documentation (50,319 events plus 1 mission launch marker = 50,320). The two-layer architecture follows the established cascade pattern from System 11 (Toronto Infrastructure)."),
    para("The extraordinary MDG of +63.3 dB in the thermal layer is not an anomaly — it reflects a genuine physical phase transition (cryogenic depletion) that HUF was designed to detect. This validates the framework's sensitivity to irreversible state changes, complementing the reversible cyclical drifts observed in transit systems."),

    // 6. Technical Notes
    hdr(HeadingLevel.HEADING_2, "6. Technical Notes"),
    boldPara("FITS Parsing: ", "Custom pure-Python binary parser implementing FITS standard (2880-byte blocks, ASCII headers, big-endian binary table extensions). No external astronomy library dependencies."),
    boldPara("Event Classification: ", "22 raw types consolidated to 5 functional regimes based on POSH Event Description Document (PSO_Posh_Cat_R0.14.pdf) taxonomy."),
    boldPara("Thermal Classification: ", "Quartile-based deviation from mission median HFI90 temperature (100mK bolometer plate stage)."),
    boldPara("Temporal Split: ", "Mission midpoint for both layers. Event layer: equal time. HK layer: OD 854 midpoint of OD 91-1617 range."),
    boldPara("HFI Sky Maps: ", "Three additional FITS files (HFI_SkyMap_353_2048_R3.01, 1.9GB each) contain 353 GHz full-sky temperature maps at HEALPix NSIDE=2048 resolution. These await HEALPix-capable processing for potential Layer 3 spatial analysis."),

    // Footer
    para(""),
    para("HUF Collective Document — System 12 of 12", { run: { italics: true, size: 18, color: "888888" } }),
    para("Prepared for the Higgins Unity Framework corpus under OCC 51/49 governance.", { run: { italics: true, size: 18, color: "888888" } }),
];

const doc = new Document({
    styles: {
        default: { document: { run: { font: "Arial", size: 22 } } },
        paragraphStyles: [
            { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 32, bold: true, font: "Arial", color: "1A365D" },
                paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
            { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 28, bold: true, font: "Arial", color: "2E4057" },
                paragraph: { spacing: { before: 200, after: 160 }, outlineLevel: 1 } },
            { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 24, bold: true, font: "Arial", color: "3D5A80" },
                paragraph: { spacing: { before: 160, after: 120 }, outlineLevel: 2 } },
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
            default: new Header({ children: [
                new Paragraph({ children: [
                    new TextRun({ text: "HUF System 12: ESA Planck POSH  |  Higgins Unity Framework", size: 16, font: "Arial", color: "888888", italics: true })
                ]})
            ]})
        },
        footers: {
            default: new Footer({ children: [
                new Paragraph({ alignment: AlignmentType.CENTER, children: [
                    new TextRun({ text: "Page ", size: 16, font: "Arial", color: "888888" }),
                    new TextRun({ children: [PageNumber.CURRENT], size: 16, font: "Arial", color: "888888" }),
                ]})
            ]})
        },
        children
    }]
});

Packer.toBuffer(doc).then(buffer => {
    const outPath = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/HUF_Planck_CaseStudy_v1.0.docx";
    fs.writeFileSync(outPath, buffer);
    console.log(`Written: ${outPath} (${buffer.length.toLocaleString()} bytes)`);
});
