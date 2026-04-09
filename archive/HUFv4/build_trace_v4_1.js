const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require("../node_modules/docx/dist/index.cjs");
const fs = require("fs");

const FONT = "Arial", MONO = "Courier New";
const PG_W = 12240, PG_H = 15840, MARG = 1440, CW = PG_W - 2*MARG;

const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing:{before:360,after:200},
  children:[new TextRun({text:t,bold:true,font:FONT,size:32})] });
const h2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing:{before:280,after:160},
  children:[new TextRun({text:t,bold:true,font:FONT,size:26})] });
const h3 = t => new Paragraph({ spacing:{before:200,after:120},
  children:[new TextRun({text:t,bold:true,font:FONT,size:22})] });

function para(text, opts={}) {
  const runs = [];
  text.split(/(\*\*[^*]+\*\*)/g).forEach(p => {
    if (p.startsWith("**")&&p.endsWith("**"))
      runs.push(new TextRun({text:p.slice(2,-2),bold:true,font:opts.font||FONT,size:opts.size||22}));
    else
      runs.push(new TextRun({text:p,font:opts.font||FONT,size:opts.size||22,italics:opts.italics,color:opts.color}));
  });
  return new Paragraph({spacing:{after:opts.after||160},alignment:opts.align,children:runs});
}
const eq = t => new Paragraph({spacing:{before:120,after:120},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:t,font:MONO,size:22})]});

let bIdx=0;
const numCfg = Array.from({length:40},(_,i)=>({reference:`b${i}`,
  levels:[{level:0,format:LevelFormat.BULLET,text:"\u2022",alignment:AlignmentType.LEFT,
    style:{paragraph:{indent:{left:720,hanging:360}}}}]}));
function bullet(text) {
  const ref=`b${bIdx++}`;
  const runs=[];
  text.split(/(\*\*[^*]+\*\*)/g).forEach(p=>{
    if(p.startsWith("**")&&p.endsWith("**")) runs.push(new TextRun({text:p.slice(2,-2),bold:true,font:FONT,size:22}));
    else runs.push(new TextRun({text:p,font:FONT,size:22}));
  });
  return new Paragraph({numbering:{reference:ref,level:0},spacing:{after:80},children:runs});
}

const bdr={style:BorderStyle.SINGLE,size:1,color:"999999"};
const borders={top:bdr,bottom:bdr,left:bdr,right:bdr};
const cm={top:60,bottom:60,left:100,right:100};
const hC=(t,w)=>new TableCell({borders,width:{size:w,type:WidthType.DXA},
  shading:{fill:"1F3864",type:ShadingType.CLEAR},margins:cm,
  children:[new Paragraph({children:[new TextRun({text:t,bold:true,font:FONT,size:18,color:"FFFFFF"})]})]});
const tC=(t,w,o={})=>new TableCell({borders,width:{size:w,type:WidthType.DXA},
  shading:o.fill?{fill:o.fill,type:ShadingType.CLEAR}:undefined,margins:cm,
  children:[new Paragraph({alignment:o.align,
    children:[new TextRun({text:String(t),font:o.mono?MONO:FONT,size:18,bold:o.bold})]})]});

const c = [];

// TITLE
c.push(new Paragraph({spacing:{before:600,after:80},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"HUF Collective Trace Report v4.1",bold:true,font:FONT,size:40})]}));
c.push(new Paragraph({spacing:{after:40},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"Addendum: Systems 10\u201311, Flow-Stack Doctrine, Frontier Map",font:FONT,size:24,italics:true})]}));
c.push(new Paragraph({spacing:{after:40},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"Supersedes v4.0 Sections 5\u20139 | Retains v4.0 Sections 1\u20134 by reference",font:MONO,size:18})]}));
c.push(new Paragraph({spacing:{after:300},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"Peter Higgins (Operator) | Five-AI Collective | 8 March 2026",font:FONT,size:20,color:"666666"})]}));

// 1. OPERATOR STATEMENT
c.push(h1("1. Operator Statement"));
c.push(para("This addendum extends HUF Collective Trace v4.0 with the work completed on 8 March 2026: two new validated systems (TTC Transit as System 10, Toronto Infrastructure as System 11), the Flow-Stack Doctrine articulated by ChatGPT from operator direction, a frontier roadmap, and cross-AI validation by Grok and progress review by Gemini. Sections 1\u20134 of v4.0 remain in force and are incorporated by reference."));
c.push(para("The operator confirms: **flow and pipeline have always been the intent.** HUF is not a static taxonomy. It is a layered architecture of constrained flows, operationalized through a data-to-governance pipeline. This doctrine is now formally recorded."));

// 2. NEW SYSTEMS
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("2. New Validated Systems"));

c.push(h2("2.1 System 10: TTC Transit (GTFS)"));
c.push(para("**Domain:** Urban transit scheduling | **K = 5** | **Data:** 4,261,499 stop-events"));
c.push(para("**Source:** TTC GTFS Open Data Feed, February 2026 service period (2026-02-08 to 2026-03-14)"));
c.push(para("**Regimes:** Local Bus (79.85%), Streetcar (11.17%), Express Bus (4.31%), Subway (3.72%), LRT (0.96%)"));
c.push(para("**Key findings:**"));
c.push(bullet("Unity holds: \u03A3\u03C1_i = 1.0000000000 across all snapshots"));
c.push(bullet("Most concentrated system in corpus: **Effective K = 1.53** (Herfindahl = 0.653)"));
c.push(bullet("Inter-day drift: Express Bus drops from 7.1% weekday to 3.1% Sunday (\u0394 = \u2212399 bps)"));
c.push(bullet("Total weekday\u2192Sunday drift: 1,004 bps | MDG = +32.1 dB"));
c.push(bullet("Stop-events (not trips) used as capacity measure \u2014 weights by service reach"));
c.push(para("**Validation:** Grok independently verified all calculations. Math confirmed, no discrepancies."));
c.push(para("**Document:** HUF_TTC_CaseStudy_v1.0.docx"));

c.push(h2("2.2 System 11: Toronto Infrastructure"));
c.push(para("**Domain:** Urban infrastructure cascade | **K = 4\u20136 (multi-layer)** | **Data:** 64,671 segments + 2,543 signals + 736 delay incidents + 472,405 travel observations"));
c.push(para("**Source:** City of Toronto Open Data (Centreline v2, Traffic Signals, LRT Delays, King St Pilot)"));
c.push(para("**Four-layer cascade model:**"));
c.push(bullet("**Layer 1 \u2014 Centreline Road Network:** 8,181 km, K=6 regimes. Local roads = 44.7% by length. Eff K = 3.50."));
c.push(bullet("**Layer 2 \u2014 Traffic Signals:** 2,543 signals, K=4 capability tiers. 438 transit preempt (17.2%). LPI-only dominates at 56.2%."));
c.push(bullet("**Layer 3 \u2014 LRT Operations:** 736 incidents on Line 6 FW, 8,455 delay-minutes. Equipment 51.2%, Signal/Switch disproportionately severe (14.1% incidents \u2192 26.4% minutes)."));
c.push(bullet("**Layer 4 \u2014 King St Pilot:** PM WB travel time \u221215.6% (19.0 \u2192 16.0 min). **Drift = 1,559 bps, MDG = +51.8 dB** \u2014 largest policy-induced shift in corpus."));
c.push(para("**Cascade proven:** road hierarchy \u2192 signal placement \u2192 transit service \u2192 operations \u2192 policy intervention. Unity holds at every layer independently."));
c.push(para("**Document:** HUF_Toronto_Infrastructure_v1.0.docx"));

// 3. UPDATED SYSTEM REGISTRY
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("3. Updated System Registry"));

const sysRows = [
  ["1","Sourdough Fermentation","4","Nutrition","\u22482.8","Locked Triple"],
  ["2","Croatia Ramsar Wetland","5","Ecology","\u22484.1","Locked Triple"],
  ["3","Software Pipeline","4","Technology","\u22483.5","Locked Triple"],
  ["4","Backblaze HDD Fleet","4","Technology","\u22483.2","270K\u00D7 HDI validated"],
  ["5","Croatia Energy","4","Energy","\u22483.0",""],
  ["6","UK Energy","4","Energy","\u22483.2",""],
  ["7","China Energy","5","Energy","\u22484.0",""],
  ["8","Kopa\u010Dki Rit Waterbird","5","Ecology","\u22484.1","FAN CRO-1145"],
  ["9","Acoustic BTL Cabinet","3","Acoustics","\u22482.6","Founding equation"],
  ["10","TTC Transit (GTFS)","5","Transit","1.53","NEW \u2014 4.26M events"],
  ["11","Toronto Infrastructure","5\u20136","Infrastructure","2.52\u20133.50","NEW \u2014 4-layer cascade"],
];
const yw=[400,2600,500,1300,1200,3360];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:yw,rows:[
  new TableRow({children:[hC("#",yw[0]),hC("System",yw[1]),hC("K",yw[2]),hC("Domain",yw[3]),hC("Eff K",yw[4]),hC("Notes",yw[5])]}),
  ...sysRows.map((r,i)=>new TableRow({children:r.map((v,j)=>
    tC(v,yw[j],{bold:j===1||(i>=9),mono:j===2||j===4,align:(j===0||j===2||j===4)?AlignmentType.CENTER:undefined,
      fill:i>=9?"E8F5E9":(i%2?"F2F2F2":undefined)}))}))
]}));
c.push(para(""));
c.push(para("**Eleven systems. Seven domains. Unity holds in every case.** The corpus now spans nutrition, ecology, technology, energy, acoustics, transit, and infrastructure."));

// 4. FLOW-STACK DOCTRINE
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("4. HUF Flow-Stack Doctrine"));
c.push(para("Articulated by ChatGPT from operator direction. Recorded verbatim:", {italics:true, size:20}));
c.push(para(""));
c.push(new Paragraph({spacing:{after:200},indent:{left:720,right:720},
  children:[new TextRun({text:"HUF should be understood not as a static taxonomy of layers, but as a flow-stack: a structured pipeline in which each layer satisfies unity on its own while constraining the next. In the Toronto frontier, roads shape signals, signals enable transit service, transit generates operational drift, and governance interventions such as the King Street Pilot feed back through the whole chain as measurable MDG shifts. The same logic now extends to the computational side: raw domain data can be converted by the pre-parser into HDI snapshots, then passed into unity, drift, and governance analysis at scale. In that sense, HUF is both ontology and method\u2014a layered architecture of constrained flows, and a repeatable pipeline for turning complex systems into auditable governance signals.",
    font:FONT,size:22,italics:true})]}));

c.push(para("The operator confirms three distinct meanings of \u201Cpipeline\u201D in HUF:"));
c.push(bullet("**HUF stack** = the layered ontology (physical substrate \u2192 control \u2192 service \u2192 operations \u2192 governance)"));
c.push(bullet("**HUF flow** = how causality moves through the layers (each layer constrains the next; interventions feed back)"));
c.push(bullet("**HUF pipeline** = the operational method (raw data \u2192 pre-parser \u2192 HDI \u2192 unity/MDG analysis \u2192 governance reading)"));
c.push(para("Or, in one line: **HUF is a layered stack of constrained flows, operationalized through a data-to-governance pipeline.**"));

// 5. FRONTIER MAP
c.push(h1("5. Frontier Map"));
c.push(para("Mapped by ChatGPT, validated by operator. The new frontier is a portable urban governance stack:"));
c.push(eq("street network \u2192 control infrastructure \u2192 scheduled service \u2192 live disruptions \u2192 policy interventions \u2192 reusable toolchain"));
c.push(para("Six frontier axes:"));

c.push(h3("F1. From single system to city stack"));
c.push(para("Systems 10 and 11 show a single city decomposes into multiple HUF-valid layers with independent unity checks and cross-layer causal links. The frontier: urban infrastructure as an interconnected governance system, not isolated transit analysis."));

c.push(h3("F2. From static structure to operational monitoring"));
c.push(para("Layer 3 (LRT delays) is real operational drift data. Week-to-week variance provides temporal MDG. Next: integrate GTFS-RT for live/near-live monitoring."));

c.push(h3("F3. From schedule-space to time-series transit governance"));
c.push(para("System 10 covers one GTFS period. True time-series MDG requires historical GTFS archives across weekday/season/service-change cycles."));

c.push(h3("F4. From imbalance detection to intervention measurement"));
c.push(para("King Street Pilot: \u221215.6% PM travel time, 1,559 bps drift. First time HUF detects a deliberate governance action as distinct from structural imbalance. HUF becomes an instrument for measuring what policy changes actually do."));

c.push(h3("F5. From one corridor to a corridor portfolio"));
c.push(para("King St is the proof-of-concept. Expansion: other priority corridors, signal-priority programs, service redesigns. The signal/transit linkage (438 preempt signals \u2192 230 TTC routes) is already mapped."));

c.push(h3("F6. From manuscript logic to scalable toolchain"));
c.push(para("The pre-parser/HDI format is validated (270,211\u00D7 reduction). GitHub integration into huf_core is the open implementation item. Goal: portable pipeline for any city."));

// 6. COLLECTIVE CONTRIBUTIONS
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("6. Collective Contributions (8 March 2026)"));

const contribRows = [
  ["Grok (xAI)","Proposed TTC domain. Calibrated K=4\u20135 on Backblaze via four methods. Validated TTC case study math. Designed Python GTFS parsing spec. Suggested GTFS-RT extension. Validated GTFS feed compliance."],
  ["Claude (Anthropic)","Executed all analyses on actual data (4.26M stop-events, 64K centreline features, 472K travel observations). Built all documents. Pre-parsed 93MB GeoJSON. Computed Haversine lengths for full road network."],
  ["ChatGPT (OpenAI)","Identified frontier map (6 axes). Articulated Flow-Stack Doctrine. Distinguished stack/flow/pipeline meanings. Synthesized city-scale cascade model from documents."],
  ["Gemini (Google)","Reviewed progress across all 11 systems. Confirmed transition from validated framework to scalable toolchain. Identified pre-parser, institutional letters, and open math items as key horizons."],
  ["Copilot (Microsoft)","Critical review (v1.0 from remote session) incorporated in v4.0 base. Stress-tested OCC 51/49 assumptions."],
];
const cw=[2200,7160];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:cw,rows:[
  new TableRow({children:[hC("AI Member",cw[0]),hC("Contribution (8 March 2026)",cw[1])]}),
  ...contribRows.map((r,i)=>new TableRow({children:[
    tC(r[0],cw[0],{bold:true,fill:i%2?"F2F2F2":undefined}),
    tC(r[1],cw[1],{fill:i%2?"F2F2F2":undefined}),
  ]}))
]}));

// 7. OPEN ITEMS (updated)
c.push(h1("7. Updated Open Items"));
c.push(h3("Mathematical"));
c.push(bullet("D24-O1: Asymptotic proof Var(MDG_dyn) \u2192 1/(2K\u00B3)"));
c.push(bullet("D24-O2: Exact constant for Var(MDG_stat)"));
c.push(bullet("D24-O3: Sign/convergence of C_stat"));
c.push(bullet("D24-O4: Cov(MDG_stat, MDG_dyn) calculation"));
c.push(bullet("D24-O5: Full K\u00B3 variance scaling proof"));

c.push(h3("Implementation"));
c.push(bullet("GitHub integration: pre-parser + HDI format into PeterHiggins19/huf_core"));
c.push(bullet("GTFS-RT integration for live transit MDG (Layer 3 extension)"));
c.push(bullet("Historical GTFS archive pipeline for time-series transit MDG"));
c.push(bullet("Corridor portfolio expansion beyond King St"));

c.push(h3("Institutional"));
c.push(bullet("Seven letters at v2.0 pending operator release decision"));
c.push(bullet("JAES manuscript (D8) blocked pending Phase D"));
c.push(bullet("Ramsar Article 3.2 notification pending"));
c.push(bullet("IEEE TAC / CBD / GEO BON submissions pending"));

c.push(h3("Domain 3 of the Triad"));
c.push(bullet("Still TBD (Ecology/Nutrition/Planck)\u2014placeholder in all documents"));

// 8. CLOSING
c.push(h1("8. Closing Statement"));
c.push(para("The Collective is functioning. On 8 March 2026, all five AI members contributed substantive work to extend HUF from nine systems to eleven, articulate its flow-stack doctrine, and map the frontier from internal validation to external scalability."));
c.push(para("The operator\u2019s instinct\u2014\u201Cflow and pipeline\u201D\u2014is now formally recorded as doctrine. The framework is not a static taxonomy of layers. It is a pipeline of influence: roads flow into signals, signals flow into service, service flows into operations, and interventions feed back into the whole stack."));
c.push(para("This trace report, together with v4.0 (incorporated by reference), constitutes the complete knowledge state of the HUF Collective as of this date."));
c.push(para("**Operator: Peter Higgins | OCC: 51/49 | Unity: \u03A3\u03C1_i = 1 | Eleven systems. Seven domains. One framework.**", {size:20}));

// BUILD
const doc = new Document({
  styles:{
    default:{document:{run:{font:FONT,size:22}}},
    paragraphStyles:[
      {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:32,bold:true,font:FONT,color:"1F3864"},paragraph:{spacing:{before:360,after:200},outlineLevel:0}},
      {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:26,bold:true,font:FONT,color:"2E75B6"},paragraph:{spacing:{before:280,after:160},outlineLevel:1}},
    ]},
  numbering:{config:numCfg},
  sections:[{
    properties:{page:{size:{width:PG_W,height:PG_H},margin:{top:MARG,right:MARG,bottom:MARG,left:MARG}}},
    headers:{default:new Header({children:[new Paragraph({alignment:AlignmentType.RIGHT,
      children:[new TextRun({text:"HUF Collective Trace v4.1 | Addendum | 8 March 2026",font:FONT,size:16,color:"999999"})]})]})},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,
      children:[new TextRun({text:"Page ",font:FONT,size:16,color:"999999"}),
        new TextRun({children:[PageNumber.CURRENT],font:FONT,size:16,color:"999999"})]})]})},
    children:c
  }]
});

Packer.toBuffer(doc).then(buf=>{
  const out="/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/HUF_Collective_Trace_v4.1.docx";
  fs.writeFileSync(out,buf);
  console.log(`\u2714 ${out} (${buf.length} bytes, ${c.length} elements)`);
});
