const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require("../node_modules/docx/dist/index.cjs");
const fs = require("fs");

const FONT = "Arial", MONO = "Courier New";
const PG_W = 12240, PG_H = 15840, MARG = 1440, CW = PG_W - 2*MARG;

const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: t, bold: true, font: FONT, size: 32 })] });
const h2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: t, bold: true, font: FONT, size: 26 })] });

function para(text, opts = {}) {
  const runs = [];
  text.split(/(\*\*[^*]+\*\*)/g).forEach(p => {
    if (p.startsWith("**") && p.endsWith("**"))
      runs.push(new TextRun({ text: p.slice(2,-2), bold: true, font: FONT, size: opts.size||22 }));
    else
      runs.push(new TextRun({ text: p, font: FONT, size: opts.size||22, italics: opts.italics, color: opts.color }));
  });
  return new Paragraph({ spacing: { after: opts.after||160 }, alignment: opts.align, children: runs });
}
const eq = t => new Paragraph({ spacing: { before: 120, after: 120 }, alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: t, font: MONO, size: 22 })] });

let bIdx = 0;
const numCfg = Array.from({length:30}, (_,i) => ({ reference: `b${i}`,
  levels: [{ level:0, format: LevelFormat.BULLET, text:"\u2022", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left:720, hanging:360 } } } }] }));
function bullet(text) {
  const ref = `b${bIdx++}`;
  const runs = [];
  text.split(/(\*\*[^*]+\*\*)/g).forEach(p => {
    if (p.startsWith("**")&&p.endsWith("**")) runs.push(new TextRun({text:p.slice(2,-2),bold:true,font:FONT,size:22}));
    else runs.push(new TextRun({text:p,font:FONT,size:22}));
  });
  return new Paragraph({ numbering:{reference:ref,level:0}, spacing:{after:80}, children:runs });
}

const bdr={style:BorderStyle.SINGLE,size:1,color:"999999"};
const borders={top:bdr,bottom:bdr,left:bdr,right:bdr};
const cm={top:60,bottom:60,left:100,right:100};
const hC = (t,w) => new TableCell({borders,width:{size:w,type:WidthType.DXA},
  shading:{fill:"1F3864",type:ShadingType.CLEAR},margins:cm,
  children:[new Paragraph({children:[new TextRun({text:t,bold:true,font:FONT,size:18,color:"FFFFFF"})]})]});
const tC = (t,w,o={}) => new TableCell({borders,width:{size:w,type:WidthType.DXA},
  shading:o.fill?{fill:o.fill,type:ShadingType.CLEAR}:undefined,margins:cm,
  children:[new Paragraph({alignment:o.align,
    children:[new TextRun({text:String(t),font:o.mono?MONO:FONT,size:18,bold:o.bold})]})]});

const c = [];

// TITLE
c.push(new Paragraph({spacing:{before:600,after:80},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"HUF Toronto Infrastructure Analysis",bold:true,font:FONT,size:40})]}));
c.push(new Paragraph({spacing:{after:80},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"Four-Layer Cascade Model: Road Network \u00B7 Signals \u00B7 LRT Operations \u00B7 King St Pilot",font:FONT,size:22,italics:true})]}));
c.push(new Paragraph({spacing:{after:40},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"System 11 | Toronto Open Data + TTC GTFS | March 2026",font:MONO,size:20})]}));
c.push(new Paragraph({spacing:{after:300},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"Peter Higgins (Operator) | Grok (xAI) | Claude (Anthropic) | ChatGPT (OpenAI) | Gemini (Google) | Copilot (Microsoft)",font:FONT,size:20,color:"666666"})]}));

// 1. EXECUTIVE
c.push(h1("1. Executive Summary"));
c.push(para("This document presents the eleventh validated HUF system: a four-layer cascade model of Toronto\u2019s transportation infrastructure, built from City of Toronto Open Data and TTC operational records. The analysis spans 64,671 centreline segments (8,181 km), 2,543 traffic signals, 736 LRT delay incidents, and the King Street Pilot natural experiment (472,405 stop-level observations)."));
c.push(para("Each layer applies HUF independently\u2014unity holds (\u03A3\u03C1_i = 1.0) in every case\u2014while cross-layer connections reveal how infrastructure hierarchy shapes transit operations. The Centreline road network (Layer 1) determines where signals (Layer 2) are deployed; transit preempt signals serve TTC routes (System 10); Line 6 delays (Layer 3) feed into the GTFS LRT regime; and the King Street Pilot (Layer 4) demonstrates MDG as a policy-intervention detector on route 504, the highest-ridership streetcar."));
c.push(para("The key finding is structural: Toronto\u2019s infrastructure is hierarchically concentrated across every layer. Local roads comprise 59.4% of road-only network length. Standard signals (no transit/LPI features) represent 26.6% of intersections. Equipment failures drive 51.2% of LRT delay incidents. And the PM peak shows the largest King St travel-time improvement (\u221215.6% westbound), a 1,559 bps drift that HUF detects as a governance-scale intervention."));

// 2. LAYER 1
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("2. Layer 1: Centreline Road Network"));
c.push(para("The Centreline Version 2 dataset is a 93 MB GeoJSON file containing every road segment, trail, railway, and waterway in Toronto. Segment lengths were computed from WGS84 coordinates using the Haversine formula across all 64,671 MultiLineString features."));

c.push(h2("2.1 Full Network (K=6)"));
const L1rows = [
  ["Local","3,657 km","44.70%","0.447042","+53.4"],
  ["Non-Road","2,026 km","24.76%","0.247584","+42.6"],
  ["Collector","767 km","9.37%","0.093733","+41.7"],
  ["Major Arterial","733 km","8.96%","0.089571","+42.2"],
  ["Expressway","584 km","7.14%","0.071385","+44.0"],
  ["Minor Arterial","415 km","5.07%","0.050685","+45.7"],
];
const lw=[1700,1500,1200,1700,1200,2060];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:lw,rows:[
  new TableRow({children:[hC("Regime",lw[0]),hC("Length",lw[1]),hC("%",lw[2]),hC("\u03C1_i",lw[3]),hC("MDG(dB)",lw[4]),hC("Mode",lw[5])]}),
  ...L1rows.map((r,i)=>new TableRow({children:[
    tC(r[0],lw[0],{bold:true,fill:i%2?"F2F2F2":undefined}),
    tC(r[1],lw[1],{align:AlignmentType.RIGHT,fill:i%2?"F2F2F2":undefined}),
    tC(r[2],lw[2],{align:AlignmentType.RIGHT,fill:i%2?"F2F2F2":undefined}),
    tC(r[3],lw[3],{mono:true,align:AlignmentType.RIGHT,fill:i%2?"F2F2F2":undefined}),
    tC(r[4],lw[4],{mono:true,align:AlignmentType.RIGHT,fill:i%2?"F2F2F2":undefined}),
    tC("STRICT",lw[5],{bold:true,fill:i%2?"F2F2F2":undefined}),
  ]}))
]}));
c.push(para(""));
c.push(para("**Effective K = 3.50** | Entropy efficiency: 82.8% | Total network: 8,181 km"));
c.push(para("Jurisdiction: City of Toronto 83.6% (6,836 km), Province 7.8%, Private 6.6%, Federal 0.3%."));

c.push(h2("2.2 Road-Only Network (K=5)"));
c.push(para("Excluding non-road features (trails, waterways, railways, hydro lines) yields a 6,156 km road network with K=5 regimes. Local roads dominate at 59.4%, with **Effective K = 2.52**. This is more concentrated than the TTC GTFS system (K_eff = 1.53 in schedule space) but more balanced than the full network including non-road."));

// 3. LAYER 2
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("3. Layer 2: Traffic Signals"));
c.push(para("Toronto operates 2,543 signalized intersections. Each signal was classified into capability tiers based on transit preempt and Leading Pedestrian Interval (LPI) features:"));

const L2rows = [
  ["Tier 1: Transit+LPI","256","10.07%","+51.4","STRICT"],
  ["Tier 2: Transit Only","182","7.16%","+53.0","STRICT"],
  ["Tier 3: LPI Only","1,428","56.15%","+57.8","STRICT"],
  ["Tier 4: Standard","677","26.62%","+32.2","STRICT"],
];
const sw=[2200,1200,1200,1500,1200,2060];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:sw,rows:[
  new TableRow({children:[hC("Tier",sw[0]),hC("Count",sw[1]),hC("%",sw[2]),hC("MDG(dB)",sw[3]),hC("Mode",sw[4]),hC("K=4",sw[5])]}),
  ...L2rows.map((r,i)=>new TableRow({children:r.map((v,j)=>
    tC(v,sw[j],{bold:j===0,align:j>0?AlignmentType.RIGHT:undefined,
      mono:j===3,fill:i%2?"F2F2F2":undefined}))}))
]}));
c.push(para(""));
c.push(para("**438 signals (17.2%) have transit preempt**, serving TTC\u2019s 230 routes. Signal density is 0.4 per km of road network. **Effective K = 2.49** \u2014 LPI-only signals dominate (56.2%), reflecting the city\u2019s pedestrian safety investment over the past decade."));
c.push(para("The cross-layer connection: transit preempt signals are concentrated on arterials carrying TTC routes. The 438 preempt-equipped intersections map directly onto the GTFS route geometry, meaning Layer 2 physically enables the GTFS System 10 analysis."));

// 4. LAYER 3
c.push(h1("4. Layer 3: LRT Operational Delays"));
c.push(para("Line 6 Finch West recorded 736 delay incidents over 56 days (Dec 7, 2025 \u2013 Jan 31, 2026), totalling 8,455 delay-minutes. Incidents were classified by cause code prefix into K=5 regimes:"));

const L3rows = [
  ["Equipment","377","51.2%","3,465","41.0%"],
  ["Weather","134","18.2%","2,121","25.1%"],
  ["Signal/Switch","104","14.1%","2,231","26.4%"],
  ["Operations","95","12.9%","446","5.3%"],
  ["Other","26","3.5%","192","2.3%"],
];
const dw=[2000,1100,1100,1500,1100,1560];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:dw,rows:[
  new TableRow({children:[hC("Regime",dw[0]),hC("Incidents",dw[1]),hC("% Inc",dw[2]),hC("Delay-Min",dw[3]),hC("% Min",dw[4]),hC("Eff K",dw[5])]}),
  ...L3rows.map((r,i)=>new TableRow({children:r.map((v,j)=>
    tC(v,dw[j],{bold:j===0,align:j>0?AlignmentType.RIGHT:undefined,
      fill:i%2?"F2F2F2":undefined}))}))
]}));
c.push(para(""));
c.push(para("**Effective K = 3.00 (incidents) / 3.29 (minutes).** Equipment failures dominate by count (51.2%) but Signal/Switch failures are disproportionately severe (14.1% of incidents but 26.4% of delay-minutes). The top single cause: track switch failures (PXSW), 64 incidents causing 1,459 delay-minutes."));
c.push(para("This is real operational drift data. In HUF terms, Line 6 operates with a 13.2 incidents/week average, and week-to-week variance provides the temporal MDG signal that Grok suggested for GTFS-RT integration."));

// 5. LAYER 4
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("5. Layer 4: King Street Pilot"));
c.push(para("The King Street Transit Priority Pilot (November 2017) restricted through-traffic on King Street between Bathurst and Jarvis, prioritizing the 504 King streetcar\u2014Toronto\u2019s busiest surface route. The dataset contains 129,645 headway observations and 342,760 segment-level travel times, with a bi-weekly summary of 134 period-direction combinations."));
c.push(para("HUF treats this as a **natural experiment**: the pilot is a deliberate governance intervention, and MDG quantifies the magnitude of change across K=4 period-direction regimes:"));

const L4rows = [
  ["AM Westbound","15.2","14.7","\u22120.5","\u22123.3%","334","+38.4"],
  ["AM Eastbound","15.3","15.2","\u22120.1","\u22120.9%","90","+27.1"],
  ["PM Westbound","19.0","16.0","\u22123.0","\u221215.6%","1,559","+51.8"],
  ["PM Eastbound","18.9","16.3","\u22122.6","\u221214.0%","1,396","+50.9"],
];
const kw=[1600,1000,1000,900,900,900,900,1160];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:kw,rows:[
  new TableRow({children:[hC("Regime",kw[0]),hC("Base(min)",kw[1]),hC("Pilot(min)",kw[2]),hC("\u0394",kw[3]),hC("\u0394%",kw[4]),hC("Drift",kw[5]),hC("MDG(dB)",kw[6]),hC("Mode",kw[7])]}),
  ...L4rows.map((r,i)=>new TableRow({children:[
    tC(r[0],kw[0],{bold:true,fill:i>=2?"E8F5E9":(i%2?"F2F2F2":undefined)}),
    ...r.slice(1).map((v,j)=>tC(v,kw[j+1],{align:AlignmentType.RIGHT,mono:j>=4,
      bold:i>=2&&j>=4,fill:i>=2?"E8F5E9":(i%2?"F2F2F2":undefined)})),
    tC("STRICT",kw[7],{bold:true,fill:i>=2?"E8F5E9":(i%2?"F2F2F2":undefined)}),
  ]}))
]}));
c.push(para(""));
c.push(para("**PM peak westbound: \u221215.6% travel time reduction (1,559 bps drift, MDG = +51.8 dB).** This is the single largest policy-induced drift in the HUF corpus. The pilot also improved reliability: headways \u22644 minutes rose from 74.9% to 78.1% (PM WB) and 76.7% to 80.5% (PM EB)."));
c.push(para("In HUF governance terms, the King Street Pilot demonstrates what happens when the operator (City of Toronto, 51% authority) makes a deliberate reallocation of road space. The MDG spike is not a failure\u2014it is a **measured governance action**, precisely the kind of intervention HUF is designed to detect and quantify."));

// 6. CROSS-LAYER
c.push(h1("6. Cross-Layer Cascade Model"));
c.push(para("The four layers are not independent. They form a cascade where each layer constrains the next:"));
c.push(bullet("**Layer 1 \u2192 Layer 2:** Road hierarchy determines signal placement. Major and minor arterials (14% of road length) carry the majority of signalized intersections. Expressways have grade-separated control (no signals)."));
c.push(bullet("**Layer 2 \u2192 System 10 (GTFS):** 438 transit preempt signals directly enable TTC service. The 504 King route passes through approximately 20 signalized intersections with preempt capability."));
c.push(bullet("**System 10 \u2192 Layer 3:** Line 6 Finch West (0.96% of GTFS stop-events) generates real-time delay data. Equipment and switch failures propagate into the LRT regime of the GTFS system."));
c.push(bullet("**Layer 4 as intervention:** The King St Pilot modified Layer 1 (road access) and Layer 2 (signal timing) to improve System 10 (504 streetcar), producing measurable MDG shifts. This is a complete cascade: infrastructure \u2192 signals \u2192 transit \u2192 operations."));

// 7. SYSTEM COMPARISON
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("7. Updated System Registry"));
c.push(para("With the Toronto Infrastructure model, HUF now spans eleven validated systems across seven domains:"));

const sysRows = [
  ["1","Sourdough Fermentation","4","Nutrition","\u22482.8"],
  ["2","Croatia Ramsar Wetland","5","Ecology","\u22484.1"],
  ["3","Software Pipeline","4","Technology","\u22483.5"],
  ["4","Backblaze HDD Fleet","4","Technology","\u22483.2"],
  ["5\u20138","Energy (Croatia/UK/China)","4\u20135","Energy","\u22483\u20134"],
  ["9","Acoustic BTL Cabinet","3","Acoustics","\u22482.6"],
  ["10","TTC Transit (GTFS)","5","Transit","1.53"],
  ["11","Toronto Infrastructure","5\u20136","Infrastructure","2.52\u20133.50"],
];
const yw=[600,2800,800,1700,3460];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:yw,rows:[
  new TableRow({children:[hC("#",yw[0]),hC("System",yw[1]),hC("K",yw[2]),hC("Domain",yw[3]),hC("Effective K",yw[4])]}),
  ...sysRows.map((r,i)=>new TableRow({children:r.map((v,j)=>
    tC(v,yw[j],{bold:i>=6,mono:j===2||j===4,align:(j===0||j===2||j===4)?AlignmentType.CENTER:undefined,
      fill:i>=6?"E8F5E9":(i%2?"F2F2F2":undefined)}))}))
]}));
c.push(para(""));
c.push(para("Systems 10 and 11 together demonstrate that a single city\u2019s infrastructure can be decomposed into multiple HUF layers, each with independent unity verification, while maintaining cross-layer causal connections."));

// 8. PROVENANCE
c.push(h1("8. Provenance"));
c.push(para("**Centreline:** City of Toronto Open Data, Centreline Version 2 (WGS84/EPSG:4326)", {size:20}));
c.push(para("**Traffic Signals:** City of Toronto Open Data, Traffic Signal dataset (31 fields)", {size:20}));
c.push(para("**LRT Delays:** TTC Open Data, LRT Delay Log (Dec 2025 \u2013 Jan 2026)", {size:20}));
c.push(para("**King St Pilot:** City of Toronto, TTC King Street Transit Priority Pilot (2017\u20132018)", {size:20}));
c.push(para("**Pedestrian Crossovers:** 498 PXO locations | **Traffic Beacons:** 360 locations", {size:20}));
c.push(para("**Analysis date:** 8 March 2026", {size:20}));
c.push(para("**Analysts:** Peter Higgins (Operator) | Grok (xAI) | Claude (Anthropic) | ChatGPT (OpenAI) | Gemini (Google) | Copilot (Microsoft)", {size:20}));
c.push(para("**Unity verified:** \u03A3\u03C1_i = 1.0 across all four layers \u2714", {size:20}));

const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:32,bold:true,font:FONT,color:"1F3864"},paragraph:{spacing:{before:360,after:200},outlineLevel:0}},
      { id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:26,bold:true,font:FONT,color:"2E75B6"},paragraph:{spacing:{before:280,after:160},outlineLevel:1}},
    ]},
  numbering:{config:numCfg},
  sections:[{
    properties:{page:{size:{width:PG_W,height:PG_H},margin:{top:MARG,right:MARG,bottom:MARG,left:MARG}}},
    headers:{default:new Header({children:[new Paragraph({alignment:AlignmentType.RIGHT,
      children:[new TextRun({text:"HUF System 11 | Toronto Infrastructure | v1.0",font:FONT,size:16,color:"999999"})]})]})},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,
      children:[new TextRun({text:"Page ",font:FONT,size:16,color:"999999"}),
        new TextRun({children:[PageNumber.CURRENT],font:FONT,size:16,color:"999999"})]})]})},
    children:c
  }]
});

Packer.toBuffer(doc).then(buf => {
  const out = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/HUF_Toronto_Infrastructure_v1.0.docx";
  fs.writeFileSync(out, buf);
  console.log(`\u2714 ${out} (${buf.length} bytes, ${c.length} elements)`);
});
