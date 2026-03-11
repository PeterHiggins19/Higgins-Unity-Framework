// ══════════════════════════════════════════════════════════════════════════════
// HUF Dual-Column Infrastructure — Context | Analytic
// Shared module for all HUF document builders
// Design: Peter Higgins — "two column paths linearly through the documents,
//         on the left context on the right analytic"
// ══════════════════════════════════════════════════════════════════════════════
//
// USAGE:
//   const { createDualHelpers } = require('./shared/dual_column');
//   const dc = createDualHelpers({ palette: 'huf' }); // or 'rwa'
//
//   children: [
//     dc.sectionHead('1. Introduction'),
//     dc.colLabels(),
//     dc.dual(
//       'The car has a full tank...',              // Context (left)
//       'Let Σρᵢ = 1.0 define the unity...'        // Analytic (right)
//     ),
//     dc.dualRich(
//       [P('Narrative paragraph 1'), P('Narrative paragraph 2')],
//       [P('Equation here'), equation('H1|ψ⟩ = μ·u')]
//     ),
//     dc.subHead('1.1 The Precision Problem'),
//     dc.fullWidth(P('This paragraph spans both columns for emphasis.')),
//     dc.fullWidthTable(existingTable),
//   ]

const { Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, BorderStyle, WidthType, ShadingType } = require('docx');

// ── Palettes ────────────────────────────────────────────────────────────────
const PALETTES = {
  huf: {
    headBg:    '1F3864',  // Deep blue — section heading background
    headText:  'FFFFFF',
    ctxLabel:  '2E75B6',  // Mid blue — context column header
    anaLabel:  '1F3864',  // Deep blue — analytic column header
    ctxLabelText: 'FFFFFF',
    anaLabelText: 'FFFFFF',
    ctxBg:     'FFFFFF',  // White — context background
    anaBg:     'F0F4FA',  // Very light blue — analytic background
    ctxTag:    '2E75B6',  // Color for "CONTEXT" label
    anaTag:    '1F3864',  // Color for "ANALYTIC" label
    border:    'CCCCCC',
    textColor: '333333',
  },
  rwa: {
    headBg:    '0D4F4F',  // Deep teal
    headText:  'FFFFFF',
    ctxLabel:  '1A7A7A',  // Mid teal
    anaLabel:  '0D4F4F',  // Deep teal
    ctxLabelText: 'FFFFFF',
    anaLabelText: 'FFFFFF',
    ctxBg:     'FFFFFF',
    anaBg:     'EDF5F5',  // Very light teal
    ctxTag:    '1A7A7A',
    anaTag:    '0D4F4F',
    border:    'BBBBBB',
    textColor: '2D2D2D',
  },
};

function createDualHelpers(opts = {}) {
  const pal = PALETTES[opts.palette || 'huf'];
  const PAGE_W = opts.pageWidth || 12240;
  const MARGIN = opts.margin || 1440;
  const CW = PAGE_W - 2 * MARGIN;
  const COL_L = Math.floor(CW * 0.50);
  const COL_R = CW - COL_L;

  const thinBdr = { style: BorderStyle.SINGLE, size: 1, color: pal.border };
  const borders = { top: thinBdr, bottom: thinBdr, left: thinBdr, right: thinBdr };
  const noBdrTop = { ...borders, top: { style: BorderStyle.NONE, size: 0 } };
  const cellPad = { top: 60, bottom: 60, left: 120, right: 120 };

  // ── Helper: make a text run ──
  function tr(text, overrides = {}) {
    return new TextRun({ text, font: 'Times New Roman', size: 20, color: pal.textColor, ...overrides });
  }

  // ── Helper: make a simple paragraph ──
  function sp(text, overrides = {}) {
    const runs = typeof text === 'string'
      ? [tr(text, overrides)]
      : text.map(t => typeof t === 'string' ? tr(t) : tr(t.text || '', t));
    return new Paragraph({ spacing: { after: 120 }, children: runs });
  }

  // ── Section heading — full width, colored background ──
  function sectionHead(text) {
    return new Table({
      width: { size: CW, type: WidthType.DXA },
      columnWidths: [CW],
      rows: [new TableRow({
        children: [new TableCell({
          width: { size: CW, type: WidthType.DXA },
          columnSpan: 2,
          borders,
          shading: { fill: pal.headBg, type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 160, right: 160 },
          children: [new Paragraph({
            spacing: { before: 60, after: 60 },
            children: [tr(text, { bold: true, size: 26, color: pal.headText })],
          })],
        })],
      })],
    });
  }

  // ── Sub-heading — full width, lighter ──
  function subHead(text) {
    return new Table({
      width: { size: CW, type: WidthType.DXA },
      columnWidths: [CW],
      rows: [new TableRow({
        children: [new TableCell({
          width: { size: CW, type: WidthType.DXA },
          columnSpan: 2,
          borders,
          shading: { fill: pal.anaBg, type: ShadingType.CLEAR },
          margins: { top: 60, bottom: 60, left: 160, right: 160 },
          children: [new Paragraph({
            spacing: { before: 40, after: 40 },
            children: [tr(text, { bold: true, size: 22, color: pal.headBg })],
          })],
        })],
      })],
    });
  }

  // ── Column labels row (CONTEXT | ANALYTIC) ──
  function colLabels() {
    return new Table({
      width: { size: CW, type: WidthType.DXA },
      columnWidths: [COL_L, COL_R],
      rows: [new TableRow({
        children: [
          new TableCell({
            width: { size: COL_L, type: WidthType.DXA },
            borders,
            shading: { fill: pal.ctxLabel, type: ShadingType.CLEAR },
            margins: { top: 40, bottom: 40, left: 120, right: 120 },
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [tr('CONTEXT', { bold: true, size: 18, color: pal.ctxLabelText })],
            })],
          }),
          new TableCell({
            width: { size: COL_R, type: WidthType.DXA },
            borders,
            shading: { fill: pal.anaLabel, type: ShadingType.CLEAR },
            margins: { top: 40, bottom: 40, left: 120, right: 120 },
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [tr('ANALYTIC', { bold: true, size: 18, color: pal.anaLabelText })],
            })],
          }),
        ],
      })],
    });
  }

  // ── Dual content row (string | string) ──
  function dual(ctxText, anaText) {
    return new Table({
      width: { size: CW, type: WidthType.DXA },
      columnWidths: [COL_L, COL_R],
      rows: [new TableRow({
        children: [
          new TableCell({
            width: { size: COL_L, type: WidthType.DXA },
            borders: noBdrTop,
            margins: cellPad,
            shading: { fill: pal.ctxBg, type: ShadingType.CLEAR },
            children: [sp(ctxText)],
          }),
          new TableCell({
            width: { size: COL_R, type: WidthType.DXA },
            borders: noBdrTop,
            margins: cellPad,
            shading: { fill: pal.anaBg, type: ShadingType.CLEAR },
            children: [sp(anaText, { italics: true })],
          }),
        ],
      })],
    });
  }

  // ── Dual content row (Paragraph[] | Paragraph[]) ──
  function dualRich(ctxParas, anaParas) {
    return new Table({
      width: { size: CW, type: WidthType.DXA },
      columnWidths: [COL_L, COL_R],
      rows: [new TableRow({
        children: [
          new TableCell({
            width: { size: COL_L, type: WidthType.DXA },
            borders: noBdrTop,
            margins: cellPad,
            shading: { fill: pal.ctxBg, type: ShadingType.CLEAR },
            children: Array.isArray(ctxParas) ? ctxParas : [ctxParas],
          }),
          new TableCell({
            width: { size: COL_R, type: WidthType.DXA },
            borders: noBdrTop,
            margins: cellPad,
            shading: { fill: pal.anaBg, type: ShadingType.CLEAR },
            children: Array.isArray(anaParas) ? anaParas : [anaParas],
          }),
        ],
      })],
    });
  }

  // ── Full width content (spans both columns) ──
  function fullWidth(content) {
    const children = Array.isArray(content) ? content : [content];
    return new Table({
      width: { size: CW, type: WidthType.DXA },
      columnWidths: [CW],
      rows: [new TableRow({
        children: [new TableCell({
          width: { size: CW, type: WidthType.DXA },
          columnSpan: 2,
          borders: noBdrTop,
          margins: cellPad,
          children,
        })],
      })],
    });
  }

  // ── Full width for existing Table objects ──
  function fullWidthTable(table) {
    return table; // Tables already span full width; just return as-is
  }

  // ── Spacer row ──
  function spacer(height = 120) {
    return new Paragraph({ spacing: { before: height, after: 0 }, children: [] });
  }

  return {
    sectionHead,
    subHead,
    colLabels,
    dual,
    dualRich,
    fullWidth,
    fullWidthTable,
    spacer,
    COL_L,
    COL_R,
    CW,
    palette: pal,
  };
}

module.exports = { createDualHelpers, PALETTES };
