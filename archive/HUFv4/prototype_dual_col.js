#!/usr/bin/env node
// Prototype: dual-column layout test
const { Document, Packer, Paragraph, TextRun, PageBreak, Header, Footer,
        AlignmentType, HeadingLevel, BorderStyle, PageNumber } = require('docx');
const { createDualHelpers } = require('/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/shared/dual_column');
const fs = require('fs');

const dc = createDualHelpers({ palette: 'huf' });

const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;

const P = (t) => new Paragraph({ spacing: { after: 120 },
  children: [new TextRun({ text: t, font: 'Times New Roman', size: 20, color: '333333' })] });

const Peq = (t) => new Paragraph({ spacing: { before: 80, after: 80 }, alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: t, font: 'Times New Roman', size: 20, italics: true, color: '333333' })] });

async function build() {
  const children = [
    // Title
    new Paragraph({ spacing: { before: 1200, after: 200 }, alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: 'DUAL-COLUMN PROTOTYPE', font: 'Times New Roman', size: 36, bold: true, color: '1F3864' })] }),
    new Paragraph({ spacing: { after: 400 }, alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: 'Context | Analytic — Two Reading Paths', font: 'Times New Roman', size: 24, italics: true, color: '2E75B6' })] }),

    new Paragraph({ children: [new PageBreak()] }),

    // Section 1
    dc.sectionHead('1. The Unity Constraint'),
    dc.colLabels(),
    dc.dual(
      'Imagine a car with a full tank of fuel. The tank has a fixed size. No matter how you drive, the total capacity of the tank does not change. You can use fuel or save it, but you cannot create more than the tank holds. This is the unity constraint: the total budget is fixed.',
      'Let the system state be a probability vector ρ = (ρ₁, ρ₂, ..., ρₙ) on the n-simplex Δⁿ. The unity constraint requires Σᵢ ρᵢ = 1.0 exactly. This is not a target — it is a conservation law. The simplex boundary is the Sufficiency Frontier: the set of states where at least one ρᵢ = 0.'
    ),
    dc.dual(
      'The driver controls how the fuel is used. The driver is always in charge — 51% of the decision authority. The fuel provides the remaining 49%. Together they form a complete system. But if the fuel runs out, the system stops. The driver is still there, but the partnership has no budget.',
      'The Operator Control Contract (OCC) establishes ρ_operator ≥ 0.51. The operator retains majority governance. The tool contribution ρ_tool = 1 - ρ_operator. At ρ_tool → 0, the system approaches ground state. The H1 operator preserves directional coherence: H1|ψ⟩ = μ(|ψ⟩)·u where μ = ⟨u|P|u⟩.'
    ),

    dc.subHead('1.1 The Deceptive Drift'),
    dc.dual(
      'As fuel depletes, the driver\'s share of the total system rises. At first: 51/49. Then 60/40. Then 80/20. Each step looks like the driver is gaining control. It feels like success. But the rising share IS the death signal. The system is running out of fuel while the driver celebrates the rising ratio.',
      'OCC drift: as ρ_tool → 0, ρ_operator → 1. The ratio ρ_operator/ρ_tool diverges. MC-4 monitors this drift. The critical threshold is not ρ_operator = 1 (which is undefined on the simplex boundary) but the rate dρ_operator/dt. Accelerating drift indicates imminent frontier breach. The Sufficiency Frontier is a cliff, not a slope.'
    ),

    dc.subHead('1.2 Machine Learning Parallel'),
    dc.dual(
      'A neural network learns from training data, one batch at a time. Early on, learning is fast — lots of obvious patterns to absorb. As training continues, progress slows. The model approaches its carrying capacity. If pushed beyond this point, it starts memorizing training examples instead of learning general patterns. This is overfitting — the ML equivalent of cancer.',
      'Let L(θ) be the loss function over parameters θ. Gradient descent: θ_{t+1} = θ_t - η∇L(θ_t). The learning rate η governs integration speed (Q-sensitivity). Overfitting: L_train ↓ while L_val ↑. This divergence IS the Sufficiency Frontier crossing. Regularization (L2: λ||θ||², dropout, batch norm) enforces the unity constraint on internal representations. Softmax output: Σᵢ σᵢ = 1.0 — literal unity enforcement.'
    ),

    new Paragraph({ children: [new PageBreak()] }),

    // Section 2 — full width for tables/emphasis
    dc.sectionHead('2. HUF-Org: The Framework as Organism'),
    dc.colLabels(),
    dc.dual(
      'HUF is not a tool applied to systems — it IS a system. A living organism with a metabolic budget, an immune system, growth protocols, and viability tests. The organism conserves energy (unity constraint). It integrates new elements one at a time (iterative integration). Its growth rate is limited by its most fragile member (Q-sensitivity). It can detect cancer (Deceptive Drift) through its immune system (MC-4).',
      'The HUF-Org stability criterion: for a new element ρ_{n+1} to be integrated into an n-element portfolio, the perturbation δρᵢ induced on all existing elements i ∈ {1...n} must satisfy |δρᵢ| < Qᵢ⁻¹ · ε for all i, where Qᵢ is the quality factor of element i and ε is the stability margin. The integration rate r is bounded: r ≤ min(Qᵢ⁻¹) — the slowest member governs.'
    ),

    // Cross-reference as full-width
    dc.fullWidth(
      new Paragraph({ spacing: { before: 80, after: 120 },
        children: [new TextRun({ text: '▶ Three substrates — biological tissue, acoustic transducers, silicon neural networks — obey identical mathematics under the unity constraint Σρᵢ = 1.0.', font: 'Times New Roman', size: 20, italics: true, color: '2E75B6' })] })
    ),
  ];

  const doc = new Document({
    styles: {
      default: { document: { run: { font: 'Times New Roman', size: 20 } } },
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE_W, height: PAGE_H },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: '2E75B6', space: 1 } },
            children: [
              new TextRun({ text: 'HUF Dual-Column Prototype', font: 'Times New Roman', size: 16, color: '2E75B6' }),
              new TextRun({ text: '\tContext | Analytic', font: 'Times New Roman', size: 16, italics: true, color: '999999' }),
            ],
            tabStops: [{ type: require('docx').TabStopType.RIGHT, position: require('docx').TabStopPosition.MAX }],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: 'Page ', font: 'Times New Roman', size: 16, color: '999999' }),
              new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 16, color: '999999' }),
            ],
          })],
        }),
      },
      children,
    }],
  });

  const buf = await Packer.toBuffer(doc);
  const outPath = '/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HUFv4/PROTOTYPE_dual_column.docx';
  fs.writeFileSync(outPath, buf);
  console.log(`✅ Prototype: ${outPath} (${buf.length.toLocaleString()} bytes)`);
}

build().catch(err => { console.error('❌', err.message); process.exit(1); });
