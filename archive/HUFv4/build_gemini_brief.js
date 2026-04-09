const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require('/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/node_modules/docx/dist/index.cjs');
const fs = require("fs");

const FONT="Arial",MONO="Courier New";
const PG_W=12240,PG_H=15840,MARG=1440,CW=PG_W-2*MARG;
const FULL_CITE="Peter Higgins (Operator) | Grok (xAI) | Claude (Anthropic) | ChatGPT (OpenAI) | Gemini (Google) | Copilot (Microsoft)";

const h1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:360,after:200},
  children:[new TextRun({text:t,bold:true,font:FONT,size:32})]});
const h2=t=>new Paragraph({heading:HeadingLevel.HEADING_2,spacing:{before:280,after:160},
  children:[new TextRun({text:t,bold:true,font:FONT,size:26})]});

function para(text,opts={}){
  const runs=[];
  const parts=text.split(/(\*\*[^*]+\*\*)/);
  for(const p of parts){
    if(p.startsWith('**')&&p.endsWith('**'))
      runs.push(new TextRun({text:p.slice(2,-2),font:opts.font||FONT,size:opts.size||22,bold:true,color:opts.color}));
    else
      runs.push(new TextRun({text:p,font:opts.font||FONT,size:opts.size||22,italics:opts.italics,color:opts.color}));
  }
  return new Paragraph({spacing:{after:opts.after||140},children:runs});
}
function bullet(text){return para("\u2022 "+text);}

const bdr={style:BorderStyle.SINGLE,size:1,color:"CCCCCC"};
const borders={top:bdr,bottom:bdr,left:bdr,right:bdr};
const cm={top:60,bottom:60,left:100,right:100};
const hC=(t,w)=>new TableCell({borders,width:{size:w,type:WidthType.DXA},
  shading:{fill:"1F3864",type:ShadingType.CLEAR},margins:cm,
  children:[new Paragraph({children:[new TextRun({text:t,bold:true,font:FONT,size:18,color:"FFFFFF"})]})]});
const tC=(t,w,o={})=>new TableCell({borders,width:{size:w,type:WidthType.DXA},
  shading:o.fill?{fill:o.fill,type:ShadingType.CLEAR}:undefined,margins:cm,
  children:[new Paragraph({children:[new TextRun({text:t,font:o.mono?MONO:FONT,size:18,bold:o.bold})]})]});

const c=[];

// TITLE
c.push(new Paragraph({spacing:{before:800,after:80},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"HUF Gemini Review Brief",bold:true,font:FONT,size:44})]}));
c.push(new Paragraph({spacing:{after:40},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"Hole-Closing Assessment & Priority Guidance Request",font:FONT,size:28,italics:true})]}));
c.push(new Paragraph({spacing:{after:300},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:`${FULL_CITE} | 9 March 2026`,font:FONT,size:20,color:"666666"})]}));

// 1. CONTEXT
c.push(h1("1. Context for Gemini"));
c.push(para("Gemini reviewed the HUF corpus at v4.1 and confirmed the transition from mathematical framework to operational toolchain. Since that review:"));
c.push(bullet("**Copilot delivered a devil\u2019s advocate assessment** with 16 tracked issues, rating reproducibility as \u201Cinsufficient\u201D and estimating 420 hours of remediation."));
c.push(bullet("**Claude responded** with checksums, cross-validation, formal mapping tables, and classification documentation (v4.3)."));
c.push(bullet("**Claude executed two new analyses** closing two more holes: Pettitt/CUSUM changepoint detection on Planck thermal data, and 100-trial Monte Carlo perturbation sensitivity across all three systems (v4.4)."));
c.push(para("**Current issue tracker: 6 resolved, 2 partial, 2 accepted, 1 blocked, 1 acknowledged.** The Collective requests Gemini\u2019s assessment of the remaining gaps."));

// 2. WHAT'S RESOLVED
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("2. Resolved Issues (Evidence Available)"));

const resolved=[
  ["ISS-PL-01","FITS parser validation","FITS parser cross-validated against ESA POSH ReadMe: 19/20 event types exact match. Endianness confirmed via sentinel values."],
  ["ISS-CR-01","Input checksums","SHA-256 hashes generated for all 18 raw input files across 3 domains."],
  ["ISS-CR-02","Classification rules","Formal mapping tables: 22\u21925 Planck events, GTFS route_type\u21925 TTC regimes, quartile thermal thresholds, infrastructure layer definitions."],
  ["ISS-MDG-01","MDG normalization","Convention documented: MDG = 20*log10(mean_drift_bps/K). Consistent across all systems."],
  ["ISS-CHP-01","Planck changepoint","Pettitt test: OD 975 (p \u2248 0). CUSUM: OD 992 (exact match to known He-4 exhaustion). MDG delta: -0.9 dB. Original analysis confirmed robust."],
  ["ISS-UQ-01","Perturbation sensitivity","100-trial Monte Carlo at 1/2/5/10/20% perturbation. Planck Thermal stable at 20%. TTC stable at 5%. Planck Events stable at 2% (97.7% dominance creates expected minor-regime fragility)."],
];
const rW=[1300,1800,6260];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:rW,rows:[
  new TableRow({children:["Issue","Topic","Resolution Evidence"].map((v,j)=>hC(v,rW[j]))}),
  ...resolved.map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,rW[j],{fill:i%2?"F2F2F2":undefined,mono:j===0}))}))
]}));

// 3. REMAINING HOLES
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("3. Remaining Holes \u2014 Gemini Assessment Requested"));

c.push(h2("3.1 ISS-CR-03: Public Code Repository (High)"));
c.push(para("All 12 scripts exist and are documented in the Methodology Appendix. Checksums verify input data integrity. The code runs deterministically. What is missing is a public GitHub repository with a repro.sh that regenerates all tables from raw inputs."));
c.push(para("**Question for Gemini:** Is this a blocking credibility issue for institutional presentation, or can it follow as a packaging task? What minimum viable repository structure would satisfy the reproducibility requirement?"));

c.push(h2("3.2 ISS-HP-01: HEALPix Sky Map Processing (Critical, Blocked)"));
c.push(para("The ESA Planck 353 GHz sky maps (3 FITS files, ~1.5 GB total) require the healpy library for spherical harmonic decomposition. This library depends on compiled C extensions that cannot be installed in the current environment due to network proxy restrictions. The POSH operational analysis (50,320 events + 45,663 HK records) is complete."));
c.push(para("**Question for Gemini:** Does HUF\u2019s space science credibility require the HEALPix analysis, or is the POSH operational analysis sufficient to demonstrate cross-domain applicability? If HEALPix is essential, should the operator pursue it in a different computational environment?"));

c.push(h2("3.3 ISS-CAUSAL-01: King Street Pilot Causal Robustness (Medium)"));
c.push(para("Copilot requested diff-in-diff, synthetic control, and pre-trend tests for the King Street Pilot analysis. The available data is a pre/post comparison (summary CSV + disaggregate travel times), which is the same structure used in the City of Toronto\u2019s official pilot evaluation."));
c.push(para("**Question for Gemini:** Is the pre/post comparison with HUF regime analysis a reasonable scope boundary for a governance framework demonstration, or does the causal identification gap undermine the infrastructure case study?"));

c.push(h2("3.4 ISS-VALID-01 / ISS-DRIFT-01: Validation Artifacts & Confidence Intervals (Medium)"));
c.push(para("The perturbation analysis now provides empirical stability bounds (100 Monte Carlo trials, seed-controlled, reproducible). Copilot originally requested \u201Cnotebooks, diffs, signed scope statements\u201D and formal bootstrapped confidence intervals."));
c.push(para("**Question for Gemini:** Do the Monte Carlo perturbation results satisfy the uncertainty quantification requirement? Is the cross-AI validation model (Grok math-checks, Copilot adversarial review, conversation transcripts) a legitimate validation artifact, or does it need to be formalized further?"));

// 4. MDG LEADERBOARD
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("4. Current MDG Leaderboard"));
const mdg=[
  ["Planck Thermal (L2)","+63.3 dB (+62.4 with changepoint)","Cryogenic phase transition"],
  ["King St Pilot (L4)","+51.8 dB","Deliberate governance intervention"],
  ["TTC Transit (L1)","+32.1 dB","Structural mode imbalance (bus 79.8%)"],
  ["Planck Events (L1)","+30.1 dB","Survey satellite design (scanning 97.7%)"],
  ["Toronto Signals (L2)","+28.4 dB","Temporal infrastructure layering"],
  ["Centreline (L1)","+19.7 dB","Road type distribution"],
];
const mW2=[2600,2800,3960];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:mW2,rows:[
  new TableRow({children:["System","MDG","Interpretation"].map((v,j)=>hC(v,mW2[j]))}),
  ...mdg.map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,mW2[j],{fill:i%2?"F2F2F2":undefined,mono:j===1}))}))
]}));

// 5. FRONTIER STATUS
c.push(h1("5. Frontier Map Status (ChatGPT\u2019s 6 Axes)"));
const frontier=[
  ["F1","Mathematical Proof","Core axioms stated. Variance proofs D24-O1\u2013O5 pending formal write-up."],
  ["F2","Multi-Domain Data","3 domains demonstrated (transit, infrastructure, space). 12 systems analysed."],
  ["F3","Operational Governance","OCC 51/49 articulated. Strict/permissive modes demonstrated. MDG leaderboard operational."],
  ["F4","AI Collective Model","5 members active. Grok (math), Claude (execution), ChatGPT (doctrine), Gemini (review), Copilot (adversarial)."],
  ["F5","Institutional Engagement","7 letters at v2.0 pending release. No submissions yet."],
  ["F6","Pedagogical Materials","Origin story complete. Methodology appendix written. No teaching materials yet."],
  ["F7","Toolchain Scalability","12 scripts, 3,232 lines. No formal package. No API. No web interface."],
];
const fW=[500,2000,6860];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:fW,rows:[
  new TableRow({children:["Axis","Domain","Current Status"].map((v,j)=>hC(v,fW[j]))}),
  ...frontier.map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,fW[j],{fill:i%2?"F2F2F2":undefined,mono:j===0}))}))
]}));

// 6. SPECIFIC ASKS
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("6. Specific Asks for Gemini"));
c.push(para("1. **Rank the remaining holes** (ISS-CR-03, ISS-HP-01, ISS-CAUSAL-01, ISS-VALID-01, ISS-DRIFT-01) by impact on framework credibility."));
c.push(para("2. **Assess the perturbation results.** Are the stability thresholds (K_eff change < 10%, max weight shift < 500 bps) appropriate for governance-grade claims?"));
c.push(para("3. **Advise on volume architecture.** Should the 11 documents be consolidated into a structured volume, or kept modular?"));
c.push(para("4. **Identify any new gaps** that were not in Copilot\u2019s tracker. Gemini\u2019s perspective as a reviewer (not adversary) may surface different concerns."));
c.push(para("5. **Recommend next priorities** given finite operator time. What maximizes readiness for institutional presentation?"));

c.push(new Paragraph({spacing:{before:300},children:[]}));
c.push(para(`**${FULL_CITE}**`,{size:20}));
c.push(para("**OCC: 51/49 | Unity: \u03A3\u03C1_i = 1**",{size:20}));

// BUILD
const doc=new Document({
  styles:{default:{document:{run:{font:FONT,size:22}}},
    paragraphStyles:[
      {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:32,bold:true,font:FONT,color:"1F3864"},paragraph:{spacing:{before:360,after:200},outlineLevel:0}},
      {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:26,bold:true,font:FONT,color:"2E75B6"},paragraph:{spacing:{before:280,after:160},outlineLevel:1}},
    ]},
  sections:[{
    properties:{page:{size:{width:PG_W,height:PG_H},margin:{top:MARG,right:MARG,bottom:MARG,left:MARG}}},
    headers:{default:new Header({children:[new Paragraph({alignment:AlignmentType.RIGHT,
      children:[new TextRun({text:"HUF Gemini Review Brief | v4.4 | 9 March 2026",font:FONT,size:16,color:"999999"})]})]})},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,
      children:[new TextRun({text:"Page ",font:FONT,size:16,color:"999999"}),
        new TextRun({children:[PageNumber.CURRENT],font:FONT,size:16,color:"999999"})]})]})},
    children:c
  }]
});

Packer.toBuffer(doc).then(buf=>{
  const out="/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/HUF_Gemini_Brief_v1.0.docx";
  fs.writeFileSync(out,buf);
  console.log(`Done: ${out} (${buf.length.toLocaleString()} bytes, ${c.length} elements)`);
});
