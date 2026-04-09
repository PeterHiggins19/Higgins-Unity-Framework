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
const h3=t=>new Paragraph({spacing:{before:240,after:120},
  children:[new TextRun({text:t,bold:true,font:FONT,size:22})]});

function para(text,opts={}){
  const runs=[];
  const parts=text.split(/(\*\*[^*]+\*\*)/);
  for(const p of parts){
    if(p.startsWith('**')&&p.endsWith('**'))
      runs.push(new TextRun({text:p.slice(2,-2),font:opts.font||FONT,size:opts.size||22,bold:true,color:opts.color}));
    else
      runs.push(new TextRun({text:p,font:opts.font||FONT,size:opts.size||22,italics:opts.italics,color:opts.color,bold:opts.bold}));
  }
  return new Paragraph({spacing:{after:opts.after||140},children:runs});
}

function bullet(text,opts={}){
  return para("\u2022 "+text,opts);
}

const bdr={style:BorderStyle.SINGLE,size:1,color:"CCCCCC"};
const borders={top:bdr,bottom:bdr,left:bdr,right:bdr};
const cm={top:60,bottom:60,left:100,right:100};
const hC=(t,w)=>new TableCell({borders,width:{size:w,type:WidthType.DXA},
  shading:{fill:"1F3864",type:ShadingType.CLEAR},margins:cm,
  children:[new Paragraph({children:[new TextRun({text:t,bold:true,font:FONT,size:18,color:"FFFFFF"})]})]});
const tC=(t,w,o={})=>new TableCell({borders,width:{size:w,type:WidthType.DXA},
  shading:o.fill?{fill:o.fill,type:ShadingType.CLEAR}:undefined,margins:cm,
  children:[new Paragraph({children:[new TextRun({text:t,font:o.mono?MONO:FONT,size:o.size||18,bold:o.bold})]})]});

const c=[];

// TITLE
c.push(new Paragraph({spacing:{before:600,after:80},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"HUF Collective Trace Report v4.4",bold:true,font:FONT,size:40})]}));
c.push(new Paragraph({spacing:{after:40},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"Hole-Closing Update: Changepoint Detection + Perturbation Analysis",font:FONT,size:24,italics:true})]}));
c.push(new Paragraph({spacing:{after:60},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"Prepared for Gemini (Google) Review",font:FONT,size:22,color:"2E75B6"})]}));
c.push(new Paragraph({spacing:{after:300},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:`${FULL_CITE} | 9 March 2026`,font:FONT,size:20,color:"666666"})]}));

// 1. OPERATOR STATEMENT
c.push(h1("1. Operator Statement"));
c.push(para("This update closes two Copilot-identified holes and prepares a brief for Gemini to review the remaining gaps and advise on next steps. Since v4.3, Claude has executed:"));
c.push(bullet("**ISS-CHP-01 (Planck changepoint):** Pettitt test and CUSUM analysis on 45,663 HFI 100mK temperature records. CUSUM identifies the cryogenic depletion boundary at **OD 992 exactly** \u2014 matching the known He-4 exhaustion date of 14 January 2012. Pettitt places it at OD 975 (17 days early, detecting the pre-depletion thermal gradient). Both are highly significant (p \u2248 0). MDG shifts only -0.9 dB from the original midpoint analysis."));
c.push(bullet("**ISS-UQ-01 (Perturbation sensitivity):** 100-trial Monte Carlo perturbation analysis at 1%, 2%, 5%, 10%, and 20% random reclassification rates across three systems. Planck Thermal is the most robust (stable at 20%). TTC is stable at 5%. Planck Events is sensitive above 2%, which is expected and informative \u2014 the 97.7% scanning dominance means minor regimes are inherently fragile to reclassification noise."));
c.push(para("The operator notes: **two more Copilot issues are now resolved with data.** The issue tracker is updating accordingly."));

// 2. CHANGEPOINT RESULTS
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("2. ISS-CHP-01: Planck Thermal Changepoint Results"));
c.push(h2("2.1 Methods"));
c.push(para("Two independent non-parametric changepoint detection methods were applied to the full 45,663-record HFI 100mK bolometer plate temperature time series:"));
c.push(bullet("**Pettitt test:** Rank-based scan for a single changepoint that maximizes the Mann-Whitney U statistic. Non-parametric \u2014 no distributional assumptions."));
c.push(bullet("**CUSUM (Cumulative Sum):** Cumulative deviation from the grand mean. The changepoint is where |CUSUM| is maximized."));

c.push(h2("2.2 Results"));
const cpData=[
  ["Method","Changepoint OD","Significance","Distance from Known Event"],
  ["Pettitt","OD 975","p \u2248 0 (K = 505,828,494)","-17 ODs (pre-depletion gradient)"],
  ["CUSUM","OD 992","Max |CUSUM| = 8,348.6","0 ODs (exact match)"],
  ["Original midpoint","OD 854","(no statistical test)","-138 ODs"],
];
const cpW=[1500,1800,2800,3260];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:cpW,rows:[
  new TableRow({children:cpData[0].map((v,j)=>hC(v,cpW[j]))}),
  ...cpData.slice(1).map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,cpW[j],{fill:i%2?"F2F2F2":undefined}))}))
]}));

c.push(h2("2.3 Temperature Comparison"));
const tempData=[
  ["Metric","Pre-Changepoint (OD 91\u2013975)","Post-Changepoint (OD 975\u20131617)"],
  ["Records","26,761","18,902"],
  ["Mean HFI90","0.102723 K","0.850084 K"],
  ["Range","0.102565 \u2013 0.103879 K","0.102760 \u2013 0.930111 K"],
  ["Temperature jump","\u2014","0.747 K (747,361 \u00B5K)"],
];
const tpW=[2000,3680,3680];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:tpW,rows:[
  new TableRow({children:tempData[0].map((v,j)=>hC(v,tpW[j]))}),
  ...tempData.slice(1).map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,tpW[j],{fill:i%2?"F2F2F2":undefined}))}))
]}));

c.push(h2("2.4 Impact on MDG"));
c.push(para("Using the Pettitt boundary instead of the mission midpoint, the thermal MDG shifts from +63.3 dB to **+62.4 dB** (delta = -0.9 dB). This is a negligible change that confirms the original analysis was robust even with an imprecise split point. The cryogenic phase transition is so dramatic (0.747 K jump) that the exact boundary matters less than the physical event itself."));

// 3. PERTURBATION RESULTS
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("3. ISS-UQ-01: Perturbation Sensitivity Results"));
c.push(h2("3.1 Method"));
c.push(para("For each system, N=100 Monte Carlo trials at each perturbation level (1%, 2%, 5%, 10%, 20%). At each level, X% of records are randomly reassigned to a different regime. Stability criterion: K_eff changes less than 10% AND maximum weight shift less than 500 bps."));

c.push(h2("3.2 Planck Events (Layer 1)"));
const evData=[
  ["Perturb %","Mean K_eff","Std","Max \u0394\u03C1 (bps)","Stable?"],
  ["1%","1.0684","0.0002","97.2","YES"],
  ["2%","1.0899","0.0003","194.2","YES"],
  ["5%","1.1583","0.0004","485.9","NO"],
  ["10%","1.2856","0.0008","971.5","NO"],
  ["20%","1.6011","0.0013","1942.6","NO"],
];
const pW=[1200,1800,1200,2400,2760];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:pW,rows:[
  new TableRow({children:evData[0].map((v,j)=>hC(v,pW[j]))}),
  ...evData.slice(1).map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,pW[j],{fill:i%2?"F2F2F2":undefined,mono:j>0&&j<4}))}))
]}));
c.push(para("**Interpretation:** Planck Events are dominated at 97.7% by Scanning Operations. Perturbing even 5% of events pushes the minor regimes past the 500 bps threshold. This is not a weakness of HUF \u2014 it is an accurate characterization of a system where one regime is structurally dominant. The perturbation result tells you that the minor-regime weights are classification-sensitive, which is exactly what governance monitoring should flag."));

c.push(h2("3.3 Planck Thermal (Layer 2)"));
const thData=[
  ["Perturb %","Mean K_eff","Std","Max \u0394\u03C1 (bps)","Stable?"],
  ["1%","3.6308","0.0015","16.4","YES"],
  ["2%","3.6401","0.0023","32.5","YES"],
  ["5%","3.6670","0.0033","80.5","YES"],
  ["10%","3.7098","0.0043","158.6","YES"],
  ["20%","3.7874","0.0052","311.4","YES"],
];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:pW,rows:[
  new TableRow({children:thData[0].map((v,j)=>hC(v,pW[j]))}),
  ...thData.slice(1).map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,pW[j],{fill:i%2?"F2F2F2":undefined,mono:j>0&&j<4}))}))
]}));
c.push(para("**Interpretation:** The thermal classification is **exceptionally robust** \u2014 stable even at 20% perturbation. The quartile-based thresholds produce near-uniform regimes, and the cryogenic depletion signal is so strong that random reclassification cannot wash it out. This is the strongest stability result in the corpus."));

c.push(h2("3.4 TTC Transit"));
const ttcData=[
  ["Perturb %","Mean K_eff","Std","Max \u0394\u03C1 (bps)","Stable?"],
  ["1%","1.8759","0.0007","64.2","YES"],
  ["2%","1.9058","0.0011","128.2","YES"],
  ["5%","1.9992","0.0018","321.1","YES"],
  ["10%","2.1664","0.0028","641.1","NO"],
  ["20%","2.5500","0.0050","1283.5","NO"],
];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:pW,rows:[
  new TableRow({children:ttcData[0].map((v,j)=>hC(v,pW[j]))}),
  ...ttcData.slice(1).map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,pW[j],{fill:i%2?"F2F2F2":undefined,mono:j>0&&j<4}))}))
]}));
c.push(para("**Interpretation:** TTC is stable up to 5% perturbation (K_eff change = 8.3%, max \u0394\u03C1 = 321 bps). The bus-dominance pattern (79.8%) is resilient to moderate classification noise. The 10% instability reflects the same structural concentration as Planck Events."));

// 4. UPDATED ISSUE TRACKER
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("4. Copilot Issue Tracker \u2014 Updated Status"));

const issues=[
  ["ISS-PL-01","FITS parser validation","Low","RESOLVED","Cross-validated 19/20 exact match"],
  ["ISS-CR-01","Input checksums","Medium","RESOLVED","SHA-256 for all 18 raw input files"],
  ["ISS-CR-02","Classification rules","Medium","RESOLVED","Formal mapping tables published"],
  ["ISS-MDG-01","MDG normalization","Medium","RESOLVED","Convention documented: 20*log10(drift_bps/K)"],
  ["ISS-CHP-01","Planck changepoint","Medium","RESOLVED","Pettitt OD 975, CUSUM OD 992 (exact He-4 match)"],
  ["ISS-UQ-01","Uncertainty quantification","Medium","RESOLVED","100-trial Monte Carlo at 5 perturbation levels"],
  ["ISS-CR-03","Public code repository","High","ACCEPTED","huf_core repo planned, 16 hrs"],
  ["ISS-HP-01","HEALPix processing","Critical","BLOCKED","Library access blocked by proxy, 80 hrs"],
  ["ISS-CAUSAL-01","King St causal robustness","Medium","ACCEPTED","Diff-in-diff when data permits, 24 hrs"],
  ["ISS-VALID-01","Validation artifacts","Medium","PARTIAL","Cross-AI transcripts + perturbation results now available"],
  ["ISS-DRIFT-01","Drift confidence intervals","Medium","PARTIAL","Perturbation analysis provides empirical bounds"],
  ["ISS-GOV-01","OCC governance minutes","Low","ACKNOWLEDGED","Trace reports serve as governance record"],
];
const iW=[1300,1800,900,1100,4260];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:iW,rows:[
  new TableRow({children:["Issue","Description","Severity","Status","Evidence"].map((v,j)=>hC(v,iW[j]))}),
  ...issues.map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,iW[j],{fill:i%2?"F2F2F2":undefined,mono:j===0,bold:j===3&&v==="RESOLVED"}))}))
]}));

c.push(para("**Summary: 6 resolved, 2 partial, 2 accepted, 1 blocked, 1 acknowledged.** Up from 4 resolved in v4.3."));

// 5. GEMINI REVIEW BRIEF
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("5. Brief for Gemini Review"));
c.push(para("The Collective requests Gemini\u2019s review on the following questions:"));

c.push(h2("5.1 Remaining Holes Assessment"));
c.push(para("Six issues are resolved with data. The remaining open items are:"));
c.push(bullet("**ISS-CR-03 (Public repo):** Operator decision. The code exists, the checksums exist, the methodology appendix documents everything. Is a formal GitHub repository essential for the framework\u2019s credibility at this stage, or can it follow?"));
c.push(bullet("**ISS-HP-01 (HEALPix):** Blocked by proxy restrictions. The Planck 353 GHz sky maps require healpy for spherical harmonic analysis. Can HUF make a credible claim on space science without processing the actual sky maps, given the POSH operational analysis is complete?"));
c.push(bullet("**ISS-CAUSAL-01 (King St causal):** Copilot wants diff-in-diff and synthetic control. The City of Toronto\u2019s own evaluation used the same pre/post structure we have. Is this a reasonable scope boundary, or should we pursue more granular travel-time data?"));
c.push(bullet("**ISS-VALID-01 / ISS-DRIFT-01 (Validation + confidence):** The perturbation analysis now provides empirical stability bounds. Is this sufficient for the \u201Cuncertainty quantification\u201D that Copilot requested, or do we need formal bootstrapped confidence intervals?"));

c.push(h2("5.2 Volume Architecture"));
c.push(para("The corpus is growing. We now have:"));
c.push(bullet("3 case study documents (TTC, Toronto Infrastructure, Planck)"));
c.push(bullet("1 origin story"));
c.push(bullet("4 trace reports (v4.0 through v4.4)"));
c.push(bullet("1 Copilot response document"));
c.push(bullet("1 methodology appendix"));
c.push(bullet("1 code appendix (internal use)"));
c.push(para("Does Gemini see a natural volume structure here? Should we consolidate into a Volume 4 series with chapters, or keep the modular document approach?"));

c.push(h2("5.3 Frontier Assessment"));
c.push(para("ChatGPT\u2019s six-axis frontier map identified: F1 (mathematical proof), F2 (multi-domain data), F3 (operational governance), F4 (AI Collective model), F5 (institutional engagement), F6 (pedagogical materials), F7 (toolchain scalability). Where does Gemini see the framework on each axis after the changepoint and perturbation results?"));

c.push(h2("5.4 Next Priorities"));
c.push(para("The operator asks Gemini to rank the remaining work items by impact. Given finite time, what should be done next to maximize the framework\u2019s credibility and readiness for institutional presentation?"));

// 6. COLLECTIVE CONTRIBUTIONS
c.push(new Paragraph({children:[new PageBreak()]}));
c.push(h1("6. Collective Contributions (8\u20139 March 2026)"));
const roles=[
  ["Grok (xAI)","Proposed TTC domain. Calibrated K=4\u20135 on Backblaze. Validated TTC math. Designed GTFS parsing spec. Suggested GTFS-RT."],
  ["Claude (Anthropic)","All data analyses (4.26M + 64K + 472K + 50K + 45K records). Pure Python FITS parser. Cross-validation. Checksums. Copilot response. **Changepoint detection (Pettitt + CUSUM). Perturbation sensitivity analysis (300 Monte Carlo trials across 3 systems).** All documents."],
  ["ChatGPT (OpenAI)","Six-axis frontier map. Flow-Stack Doctrine. Cascade model."],
  ["Gemini (Google)","Progress review. Framework-to-toolchain transition confirmation. **Requested for hole-closing review in v4.4.**"],
  ["Copilot (Microsoft)","Devil\u2019s advocate review. 16-issue tracker. Strongest adversarial contribution. Identified the holes we are now closing."],
];
const rW=[2200,7160];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:rW,rows:[
  new TableRow({children:["Member","Contribution"].map((v,j)=>hC(v,rW[j]))}),
  ...roles.map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,rW[j],{fill:i%2?"F2F2F2":undefined}))}))
]}));

// 7. DOCUMENT MANIFEST
c.push(h1("7. Document Manifest (v4.4)"));
const manifest=[
  ["HUF_Collective_Trace_v4.4.docx","This document \u2014 hole-closing update with Gemini brief"],
  ["HUF_Collective_Trace_v4.3.docx","Post-Copilot review trace"],
  ["HUF_Copilot_Response_v1.0.docx","Formal response to 14 Copilot issues"],
  ["HUF_Planck_CaseStudy_v1.0.docx","System 12: ESA Planck two-layer analysis"],
  ["HUF_TTC_CaseStudy_v1.0.docx","System 10: TTC GTFS transit analysis"],
  ["HUF_Toronto_Infrastructure_v1.0.docx","System 11: Four-layer infrastructure cascade"],
  ["HUF_Origin_Story_v1.0.docx","From loudspeaker diffraction to universal governance"],
  ["HUF_Methodology_Appendix_v1.0.docx","Computational methods, algorithms, pipeline (human-readable)"],
  ["HUF_Code_Appendix_v1.0.docx","Full source code (12 scripts, 3,232 lines) \u2014 internal use"],
  ["checksums.txt","SHA-256 hashes for all 18 raw input files"],
];
const mW=[3800,5560];
c.push(new Table({width:{size:CW,type:WidthType.DXA},columnWidths:mW,rows:[
  new TableRow({children:["Document","Purpose"].map((v,j)=>hC(v,mW[j]))}),
  ...manifest.map((r,i)=>new TableRow({children:r.map((v,j)=>tC(v,mW[j],{fill:i%2?"F2F2F2":undefined,mono:j===0}))}))
]}));

// CLOSING
c.push(new Paragraph({spacing:{before:300},children:[]}));
c.push(para("The holes are closing. Six of Copilot\u2019s issues are now resolved with executed analysis and evidence. The operator requests Gemini\u2019s assessment of the remaining gaps and guidance on priorities for the next phase."));
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
      children:[new TextRun({text:"HUF Collective Trace v4.4 | Hole-Closing | 9 March 2026",font:FONT,size:16,color:"999999"})]})]})},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,
      children:[new TextRun({text:"Page ",font:FONT,size:16,color:"999999"}),
        new TextRun({children:[PageNumber.CURRENT],font:FONT,size:16,color:"999999"})]})]})},
    children:c
  }]
});

Packer.toBuffer(doc).then(buf=>{
  const out="/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/HUF_Collective_Trace_v4.4.docx";
  fs.writeFileSync(out,buf);
  console.log(`Done: ${out} (${buf.length.toLocaleString()} bytes, ${c.length} elements)`);
});
