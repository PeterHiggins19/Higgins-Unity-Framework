// ══════════════════════════════════════════════════════════════════════
// HUF Triad — Shared Styles
// Times New Roman academic formatting, consistent across all volumes
// ══════════════════════════════════════════════════════════════════════

const { Paragraph, TextRun, Table, TableRow, TableCell, Header, Footer,
        AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
        PageNumber, PageBreak, TabStopType, TabStopPosition,
        LevelFormat, ExternalHyperlink } = require('docx');

// ── Page Constants ──────────────────────────────────────────────────
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;
const CW = PAGE_W - 2 * MARGIN; // 9360 DXA content width

// ── Color Palette ───────────────────────────────────────────────────
const BLUE = '1F3864';
const MID = '2E75B6';
const DARK = '333333';
const LGREY = 'F2F2F2';
const LBLUE = 'D6E4F0';
const WHITE = 'FFFFFF';
const GREEN = 'E2EFDA';
const GOLD = 'FFF2CC';

// ── Borders ─────────────────────────────────────────────────────────
const bdr = { style: BorderStyle.SINGLE, size: 1, color: 'BBBBBB' };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };

// ── Heading Helpers ─────────────────────────────────────────────────
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 28, color: BLUE })] });

const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 24, color: BLUE })] });

const H3 = (t) => new Paragraph({ spacing: { before: 200, after: 120 },
  children: [new TextRun({ text: t, bold: true, italics: true, font: 'Times New Roman', size: 22, color: DARK })] });

// ── Paragraph Helper ────────────────────────────────────────────────
function P(content, opts = {}) {
  const { align, indent, spacing_after, bold, italics, color } = opts;
  const runs = [];
  if (typeof content === 'string') {
    runs.push(new TextRun({ text: content, font: 'Times New Roman', size: 22, color: color || DARK,
      bold: bold || false, italics: italics || false }));
  } else if (Array.isArray(content)) {
    content.forEach(c => {
      if (typeof c === 'string') {
        runs.push(new TextRun({ text: c, font: 'Times New Roman', size: 22, color: color || DARK }));
      } else {
        runs.push(new TextRun({ font: 'Times New Roman', size: 22, color: DARK, ...c }));
      }
    });
  }
  return new Paragraph({
    spacing: { after: spacing_after || 160 },
    alignment: align || AlignmentType.JUSTIFIED,
    indent: indent ? { left: indent } : undefined,
    children: runs,
  });
}

// ── Table Helpers ───────────────────────────────────────────────────
function headerCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: BLUE, type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, font: 'Times New Roman', size: 20, bold: true, color: WHITE })] })],
  });
}

function dataCell(text, width, opts = {}) {
  const { shade, align, bold: b } = opts;
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    children: [new Paragraph({ alignment: align || AlignmentType.LEFT,
      children: [new TextRun({ text: String(text), font: 'Times New Roman', size: 20, color: DARK, bold: b || false })] })],
  });
}

function makeTable(headers, rows, colWidths) {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((h, i) => headerCell(h, colWidths[i])) }),
      ...rows.map((row, ri) => new TableRow({
        children: row.map((cell, ci) => dataCell(cell, colWidths[ci], { shade: ri % 2 === 0 ? LGREY : undefined }))
      })),
    ],
  });
}

// ── Cross-Reference Note ────────────────────────────────────────────
function crossRef(text) {
  return new Paragraph({
    spacing: { before: 80, after: 160 },
    children: [new TextRun({ text: '\u25B6 ' + text, font: 'Times New Roman', size: 20, italics: true, color: MID })],
  });
}

// ── Section Break ───────────────────────────────────────────────────
function sectionBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ── Standard Header/Footer ──────────────────────────────────────────
function makeHeader(title, volLabel) {
  return new Header({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MID, space: 1 } },
      spacing: { after: 0 },
      children: [
        new TextRun({ text: `HUF Triad \u2014 ${volLabel}`, font: 'Times New Roman', size: 18, color: MID }),
        new TextRun({ text: `\t${title}`, font: 'Times New Roman', size: 18, italics: true, color: MID }),
      ],
      tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
    })],
  });
}

function makeFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC', space: 1 } },
      children: [
        new TextRun({ text: 'Higgins Unity Framework v1.2.0 \u00B7 MIT License \u00B7 ', font: 'Times New Roman', size: 16, color: '999999' }),
        new TextRun({ text: 'Page ', font: 'Times New Roman', size: 16, color: '999999' }),
        new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 16, color: '999999' }),
      ],
    })],
  });
}

// ── Standard Document Styles ────────────────────────────────────────
const standardStyles = {
  default: { document: { run: { font: 'Times New Roman', size: 22 } } },
  paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 28, bold: true, font: 'Times New Roman', color: BLUE },
      paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 24, bold: true, font: 'Times New Roman', color: BLUE },
      paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
  ],
};

// ── Standard Page Properties ────────────────────────────────────────
function standardPage(volLabel, title) {
  return {
    page: {
      size: { width: PAGE_W, height: PAGE_H },
      margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
    },
  };
}

module.exports = {
  PAGE_W, PAGE_H, MARGIN, CW,
  BLUE, MID, DARK, LGREY, LBLUE, WHITE, GREEN, GOLD,
  bdr, borders,
  H1, H2, H3, P,
  headerCell, dataCell, makeTable,
  crossRef, sectionBreak,
  makeHeader, makeFooter,
  standardStyles, standardPage,
};
