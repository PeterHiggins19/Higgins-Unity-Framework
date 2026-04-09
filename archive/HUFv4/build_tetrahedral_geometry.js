// ══════════════════════════════════════════════════════════════════════
// HUF Tetrahedral Triad Geometry — Exploration Document
// How triad-union structures grow from flat triangles to 3D simplicial
// complexes, and what this predicts about HUF scaling
// ══════════════════════════════════════════════════════════════════════

const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, LevelFormat, PageNumber, PageBreak } = require('docx');

// ── Page Constants ──────────────────────────────────────────────────
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1440;
const CW = PAGE_W - 2 * MARGIN;

// ── Colors ──────────────────────────────────────────────────────────
const BLUE  = '1F3864';
const MID   = '2E75B6';
const DARK  = '333333';
const LGREY = 'F2F2F2';
const LBLUE = 'D6E4F0';
const WHITE = 'FFFFFF';
const GREEN = 'E2EFDA';
const GOLD  = 'FFF2CC';
const CORAL = 'E8D5C4';

// ── Borders ─────────────────────────────────────────────────────────
const bdr = { style: BorderStyle.SINGLE, size: 1, color: 'BBBBBB' };
const borders = { top: bdr, bottom: bdr, left: bdr, right: bdr };

// ── Styles ──────────────────────────────────────────────────────────
const styles = {
  default: { document: { run: { font: 'Times New Roman', size: 22 } } },
  paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 32, bold: true, font: 'Times New Roman', color: BLUE },
      paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 26, bold: true, font: 'Times New Roman', color: BLUE },
      paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
    { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: 23, bold: true, italics: true, font: 'Times New Roman', color: DARK },
      paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
  ],
};

const numbering = {
  config: [
    { reference: 'bullets', levels: [
      { level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      { level: 1, format: LevelFormat.BULLET, text: '\u25E6', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 1080, hanging: 360 } } } },
      { level: 2, format: LevelFormat.BULLET, text: '\u2013', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
    ]},
  ],
};

// ── Helpers ──────────────────────────────────────────────────────────
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1,
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 32, color: BLUE })] });

const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2,
  children: [new TextRun({ text: t, bold: true, font: 'Times New Roman', size: 26, color: BLUE })] });

const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3,
  children: [new TextRun({ text: t, bold: true, italics: true, font: 'Times New Roman', size: 23, color: DARK })] });

function P(content, opts = {}) {
  const { align, indent, spacing_after, bold, italics, color } = opts;
  const runs = [];
  if (typeof content === 'string') {
    runs.push(new TextRun({ text: content, font: 'Times New Roman', size: 22, color: color || DARK,
      bold: bold || false, italics: italics || false }));
  } else if (Array.isArray(content)) {
    content.forEach(c => {
      if (typeof c === 'string') {
        runs.push(new TextRun({ text: c, font: 'Times New Roman', size: 22, color: DARK }));
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

function bullet(text, level = 0) {
  const runs = [];
  if (typeof text === 'string') {
    runs.push(new TextRun({ text, font: 'Times New Roman', size: 22, color: DARK }));
  } else if (Array.isArray(text)) {
    text.forEach(c => {
      if (typeof c === 'string') {
        runs.push(new TextRun({ text: c, font: 'Times New Roman', size: 22, color: DARK }));
      } else {
        runs.push(new TextRun({ font: 'Times New Roman', size: 22, color: DARK, ...c }));
      }
    });
  }
  return new Paragraph({
    numbering: { reference: 'bullets', level },
    spacing: { after: 80 },
    children: runs,
  });
}

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
      children: [new TextRun({ text, font: 'Times New Roman', size: 20, color: DARK, bold: b || false })] })],
  });
}

const mono = (text) => new Paragraph({
  spacing: { after: 20 },
  children: [new TextRun({ text, font: 'Consolas', size: 19, color: DARK })],
});

const monoB = (text) => new Paragraph({
  spacing: { after: 20 },
  children: [new TextRun({ text, font: 'Consolas', size: 19, color: BLUE, bold: true })],
});

// ══════════════════════════════════════════════════════════════════════
// DOCUMENT CONTENT
// ══════════════════════════════════════════════════════════════════════

function buildContent() {
  const c = [];

  // ── TITLE PAGE ────────────────────────────────────────────────────
  c.push(new Paragraph({ spacing: { before: 3600 } }));
  c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: 'HUF Tetrahedral Triad Geometry', font: 'Times New Roman',
      size: 44, bold: true, color: BLUE })] }));
  c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new TextRun({ text: 'How Triad-Union Structures Grow from Flat Triangles',
      font: 'Times New Roman', size: 28, color: MID })] }));
  c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new TextRun({ text: 'to Three-Dimensional Simplicial Complexes',
      font: 'Times New Roman', size: 28, color: MID })] }));
  c.push(new Paragraph({ spacing: { before: 400 } }));
  c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'Exploration Document  \u00B7  [CONJECTURE]',
      font: 'Times New Roman', size: 24, color: DARK })] }));
  c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'Higgins Unity Framework v4.0 Corpus',
      font: 'Times New Roman', size: 22, color: DARK })] }));
  c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: 'March 2026',
      font: 'Times New Roman', size: 22, color: DARK })] }));
  c.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 200 },
    children: [new TextRun({ text: 'Author: Peter Higgins',
      font: 'Times New Roman', size: 24, italics: true, color: DARK })] }));
  c.push(new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'Document Builder: Claude (Anthropic)',
      font: 'Times New Roman', size: 20, color: '666666' })] }));
  c.push(new Paragraph({ children: [new PageBreak()] }));

  // ── 1. THE OBSERVATION ────────────────────────────────────────────
  c.push(H1('1. The Observation'));
  c.push(P('The HUF Triad Synthesis (v1.6) binds the three pillars of the framework\u2014Sufficiency Frontier, Fourth Category, and the Triad itself\u2014into a triangular relationship. Each pillar is a vertex; each connection between pillars is an edge. This is a flat object: a 2-simplex (triangle) in two dimensions.'));
  c.push(P('The question posed by Peter Higgins during the March 2026 review cycle is deceptively simple: what happens when this structure grows? If one triad is a triangle, and a triad-of-triads tiles the plane, then what shape does a triad-on-every-face produce in three dimensions? And can we predict how this geometry scales?'));
  c.push(P('The answer is yes. The growth pattern follows the mathematics of simplicial complexes\u2014the same structures that underpin the spectral sequences and persistent homology already in HUF\u2019s Phase 3 pipeline. The triad is not a flat design choice. It is the first visible face of a higher-dimensional geometry that the framework naturally inhabits.'));

  // ── 2. FROM TRIANGLE TO TETRAHEDRON ───────────────────────────────
  c.push(H1('2. From Triangle to Tetrahedron'));

  c.push(H2('2.1 The Flat Case: Triad as 2-Simplex'));
  c.push(P('A single HUF triad is a triangle\u2014the simplest possible closed structure with non-trivial internal relationships:'));
  c.push(bullet([{ text: '3 vertices ', bold: true }, '(elements/pillars)']));
  c.push(bullet([{ text: '3 edges ', bold: true }, '(pairwise connections)']));
  c.push(bullet([{ text: '1 face ', bold: true }, '(the triad itself\u2014the enclosed region)']));
  c.push(P('In HUF terms: the Sufficiency Frontier (SF), Fourth Category (FC), and Triad Synthesis each occupy a vertex. The edges represent their mutual dependencies\u2014SF constrains FC, FC operationalizes the Triad, the Triad synthesizes SF. This is a 2-simplex in the language of topology.'));

  c.push(H2('2.2 Triad of Triads: Flat Tiling (9 Elements, 3 Unions)'));
  c.push(P('When three triads share edges on a flat plane, you get a triangular tiling with 9 element-slots and 3 union points where triads meet. This is how HUF currently works at the corpus level: the three pillar documents, the Trace, the review catalog, and the exploration documents tile across a flat organizational surface. Each union point is a shared concern\u2014Category C (evidentiary hierarchy) sits at a union where multiple triads meet.'));
  c.push(P('But flat tiling has a limitation: every element participates in at most 2 triads (at a shared edge) or 1 triad (at an unshared vertex). The structure is wide but shallow. Growth adds breadth without adding depth.'));

  c.push(H2('2.3 The Tetrahedral Leap: 3D Triad Structure'));
  c.push(P([
    'A tetrahedron\u2014the simplest 3D solid\u2014has exactly ',
    { text: '4 triangular faces', bold: true },
    '. If each face is a triad, the structure gains a critical new property: ',
    { text: 'every element participates in 3 triads simultaneously', bold: true },
    '.'
  ]));

  // Tetrahedron properties table
  const tCols = [2400, 1200, 5760];
  c.push(new Table({
    width: { size: CW, type: WidthType.DXA }, columnWidths: tCols,
    rows: [
      new TableRow({ children: [
        headerCell('Property', tCols[0]), headerCell('Count', tCols[1]), headerCell('HUF Interpretation', tCols[2]),
      ]}),
      new TableRow({ children: [
        dataCell('Vertices', tCols[0], { shade: LBLUE }), dataCell('4', tCols[1], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('4 fundamental elements, each participating in 3 triads', tCols[2], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('Edges', tCols[0]), dataCell('6', tCols[1], { align: AlignmentType.CENTER }),
        dataCell('6 pairwise connections\u2014every element is directly linked to every other', tCols[2]),
      ]}),
      new TableRow({ children: [
        dataCell('Faces (triads)', tCols[0], { shade: LBLUE }), dataCell('4', tCols[1], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('4 triad constraints operating simultaneously on the same 4 elements', tCols[2], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('3-way unions', tCols[0]), dataCell('4', tCols[1], { align: AlignmentType.CENTER }),
        dataCell('Each vertex is the junction where 3 triads meet\u2014a 3-way union', tCols[2]),
      ]}),
      new TableRow({ children: [
        dataCell('Interior volume', tCols[0], { shade: LBLUE }), dataCell('1', tCols[1], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('The enclosed governance space\u2014the region all 4 triads collectively bound', tCols[2], { shade: LBLUE }),
      ]}),
    ],
  }));
  c.push(P(''));
  c.push(P([
    { text: 'Key insight: ', bold: true },
    'Peter\u2019s count of 12 points (4 faces \u00D7 3 vertices) reveals the ',
    { text: 'apparent ', italics: true },
    'complexity. The actual structure has only 4 unique vertices because each vertex is shared across 3 faces. The 12-to-4 collapse ratio (3:1) is itself a unity constraint: each element\u2019s identity is distributed across exactly 3 triad contexts. This is not redundancy\u2014it is structural reinforcement. An element that participates in 3 triads is 3 times more constrained than one that participates in only 1.'
  ]));

  // ── 3. THE ASCII GEOMETRY ─────────────────────────────────────────
  c.push(new Paragraph({ children: [new PageBreak()] }));
  c.push(H1('3. Visual Geometry'));
  c.push(P('The following diagrams show the progression from flat triad to tetrahedral structure.'));

  c.push(H2('3.1 Single Triad (2-Simplex)'));
  c.push(mono(''));
  c.push(mono('           A'));
  c.push(mono('          / \\'));
  c.push(mono('         /   \\'));
  c.push(mono('        / T\u2081  \\'));
  c.push(mono('       /       \\'));
  c.push(mono('      B \u2500\u2500\u2500\u2500\u2500\u2500\u2500 C'));
  c.push(mono(''));
  c.push(P('3 vertices (A, B, C), 3 edges, 1 face (T\u2081). Each element is in exactly 1 triad.', { italics: true }));

  c.push(H2('3.2 Triad of Triads (Flat Tiling)'));
  c.push(mono(''));
  c.push(mono('           A'));
  c.push(mono('          / \\'));
  c.push(mono('         / T\u2081 \\'));
  c.push(mono('        D\u2500\u2500\u2500\u2500\u2500E'));
  c.push(mono('       / \\ T\u2082/ \\'));
  c.push(mono('      / T\u2083\\/ T\u2084 \\'));
  c.push(mono('     F\u2500\u2500\u2500\u2500G\u2500\u2500\u2500\u2500\u2500H'));
  c.push(mono(''));
  c.push(P('Up to 8 vertices, 4 faces, shared edges. Elements at D, E, G participate in 2 triads. Still flat\u2014no depth.', { italics: true }));

  c.push(H2('3.3 Tetrahedron (3-Simplex)'));
  c.push(mono(''));
  c.push(mono('            D            Faces (triads):'));
  c.push(mono('           /|\\           T\u2081 = A-B-C  (base)'));
  c.push(mono('          / | \\          T\u2082 = A-B-D  (left)'));
  c.push(mono('         /  |  \\         T\u2083 = A-C-D  (right)'));
  c.push(mono('        /   |   \\        T\u2084 = B-C-D  (back)'));
  c.push(mono('       A\u2500\u2500\u2500\u253C\u2500\u2500\u2500C'));
  c.push(mono('        \\  |  /          Every vertex is in'));
  c.push(mono('         \\ | /           exactly 3 triads.'));
  c.push(mono('          \\|/'));
  c.push(mono('           B'));
  c.push(mono(''));
  c.push(P([
    { text: '4 vertices, 6 edges, 4 faces, 1 volume. ', bold: true },
    'Every element (A, B, C, D) participates in exactly 3 triads and is directly connected to every other element. The structure is maximally connected\u2014there are no missing edges.'
  ]));

  // ── 4. THE GROWTH LAW ─────────────────────────────────────────────
  c.push(new Paragraph({ children: [new PageBreak()] }));
  c.push(H1('4. The Growth Law: Simplicial Scaling'));
  c.push(P('The progression from triangle to tetrahedron follows a precise mathematical pattern. Each step adds one vertex (element) and one dimension, producing what topologists call an n-simplex.'));

  // Simplex growth table
  const sCols = [1100, 1200, 1000, 1000, 1000, 1060, 3000];
  c.push(new Table({
    width: { size: CW, type: WidthType.DXA }, columnWidths: sCols,
    rows: [
      new TableRow({ children: [
        headerCell('n-Simplex', sCols[0]), headerCell('Shape', sCols[1]),
        headerCell('Vertices', sCols[2]), headerCell('Edges', sCols[3]),
        headerCell('Faces', sCols[4]), headerCell('Triads per vertex', sCols[5]),
        headerCell('HUF Interpretation', sCols[6]),
      ]}),
      new TableRow({ children: [
        dataCell('0-simplex', sCols[0], { shade: LGREY }), dataCell('Point', sCols[1], { shade: LGREY }),
        dataCell('1', sCols[2], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('0', sCols[3], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('0', sCols[4], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('0', sCols[5], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('Single element (no governance)', sCols[6], { shade: LGREY }),
      ]}),
      new TableRow({ children: [
        dataCell('1-simplex', sCols[0]), dataCell('Line', sCols[1]),
        dataCell('2', sCols[2], { align: AlignmentType.CENTER }),
        dataCell('1', sCols[3], { align: AlignmentType.CENTER }),
        dataCell('0', sCols[4], { align: AlignmentType.CENTER }),
        dataCell('0', sCols[5], { align: AlignmentType.CENTER }),
        dataCell('Binary pair (no triad possible)', sCols[6]),
      ]}),
      new TableRow({ children: [
        dataCell('2-simplex', sCols[0], { shade: GOLD, bold: true }), dataCell('Triangle', sCols[1], { shade: GOLD }),
        dataCell('3', sCols[2], { shade: GOLD, align: AlignmentType.CENTER }),
        dataCell('3', sCols[3], { shade: GOLD, align: AlignmentType.CENTER }),
        dataCell('1', sCols[4], { shade: GOLD, align: AlignmentType.CENTER }),
        dataCell('1', sCols[5], { shade: GOLD, align: AlignmentType.CENTER }),
        dataCell('Single triad (current HUF pillar structure)', sCols[6], { shade: GOLD }),
      ]}),
      new TableRow({ children: [
        dataCell('3-simplex', sCols[0], { shade: GOLD, bold: true }), dataCell('Tetrahedron', sCols[1], { shade: GOLD }),
        dataCell('4', sCols[2], { shade: GOLD, align: AlignmentType.CENTER }),
        dataCell('6', sCols[3], { shade: GOLD, align: AlignmentType.CENTER }),
        dataCell('4', sCols[4], { shade: GOLD, align: AlignmentType.CENTER }),
        dataCell('3', sCols[5], { shade: GOLD, align: AlignmentType.CENTER }),
        dataCell('Tetrahedral governance (this exploration)', sCols[6], { shade: GOLD }),
      ]}),
      new TableRow({ children: [
        dataCell('4-simplex', sCols[0]), dataCell('5-cell', sCols[1]),
        dataCell('5', sCols[2], { align: AlignmentType.CENTER }),
        dataCell('10', sCols[3], { align: AlignmentType.CENTER }),
        dataCell('10', sCols[4], { align: AlignmentType.CENTER }),
        dataCell('6', sCols[5], { align: AlignmentType.CENTER }),
        dataCell('Hyper-tetrahedral (5 elements, 10 triads)', sCols[6]),
      ]}),
      new TableRow({ children: [
        dataCell('K-simplex', sCols[0], { shade: LGREY }), dataCell('K+1 cell', sCols[1], { shade: LGREY }),
        dataCell('K+1', sCols[2], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('K(K+1)/2', sCols[3], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('C(K+1,3)', sCols[4], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('C(K,2)', sCols[5], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('General: K+1 elements on probability simplex \u0394_K', sCols[6], { shade: LGREY }),
      ]}),
    ],
  }));
  c.push(P(''));

  c.push(H2('4.1 The General Formulas'));
  c.push(P('For a system with K+1 elements (a K-simplex), the structural counts are given by binomial coefficients:'));
  c.push(bullet([{ text: 'Vertices (elements): ', bold: true }, 'K + 1']));
  c.push(bullet([{ text: 'Edges (pairwise links): ', bold: true }, 'C(K+1, 2) = K(K+1)/2']));
  c.push(bullet([{ text: 'Triangular faces (triads): ', bold: true }, 'C(K+1, 3) = K(K+1)(K\u22121)/6']));
  c.push(bullet([{ text: 'Triads per vertex: ', bold: true }, 'C(K, 2) = K(K\u22121)/2']));
  c.push(bullet([{ text: 'Total d-faces: ', bold: true }, 'C(K+1, d+1) for any dimension d']));
  c.push(P('This means the number of triads grows cubically with the number of elements, while the number of triads constraining each element grows quadratically. The structure becomes exponentially more constrained as it scales\u2014each new element is not just added to the system, it is woven into every existing face.'));

  c.push(H2('4.2 The Apparent vs Actual Complexity'));
  c.push(P('Peter\u2019s original count\u2014"12 points on a tetrahedron"\u2014captures the apparent complexity: 4 faces \u00D7 3 vertices per face = 12 point-appearances. But through vertex-sharing, the actual count is 4 unique elements. This collapse ratio generalizes:'));

  const cCols = [2000, 2000, 2680, 2680];
  c.push(new Table({
    width: { size: CW, type: WidthType.DXA }, columnWidths: cCols,
    rows: [
      new TableRow({ children: [
        headerCell('Structure', cCols[0]), headerCell('Apparent Points', cCols[1]),
        headerCell('Actual Elements', cCols[2]), headerCell('Collapse Ratio', cCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('Triangle', cCols[0], { shade: LGREY }), dataCell('3 \u00D7 1 = 3', cCols[1], { shade: LGREY }),
        dataCell('3', cCols[2], { shade: LGREY }), dataCell('1:1 (no sharing)', cCols[3], { shade: LGREY }),
      ]}),
      new TableRow({ children: [
        dataCell('Tetrahedron', cCols[0]), dataCell('4 \u00D7 3 = 12', cCols[1]),
        dataCell('4', cCols[2]), dataCell('3:1', cCols[3]),
      ]}),
      new TableRow({ children: [
        dataCell('5-cell', cCols[0], { shade: LGREY }), dataCell('10 \u00D7 3 = 30', cCols[1], { shade: LGREY }),
        dataCell('5', cCols[2], { shade: LGREY }), dataCell('6:1', cCols[3], { shade: LGREY }),
      ]}),
      new TableRow({ children: [
        dataCell('K-simplex', cCols[0]), dataCell('C(K+1,3) \u00D7 3', cCols[1]),
        dataCell('K+1', cCols[2]), dataCell('K(K\u22121)/2 : 1', cCols[3]),
      ]}),
    ],
  }));
  c.push(P(''));
  c.push(P([
    { text: 'The collapse ratio equals the number of triads per vertex.', bold: true },
    ' This is not a coincidence\u2014it is a direct consequence of the simplex geometry. Each vertex appears once in each triad it belongs to, and it belongs to C(K,2) triads. The more interconnected the structure, the more "work" each element does\u2014and the more governed it is.'
  ]));

  // ── 5. CONNECTION TO HUF ──────────────────────────────────────────
  c.push(new Paragraph({ children: [new PageBreak()] }));
  c.push(H1('5. Connection to HUF Mathematics'));

  c.push(H2('5.1 The Probability Simplex IS This Geometry'));
  c.push(P([
    'The probability simplex \u0394_K\u2014where the ratio portfolio \u03C1 lives\u2014',
    { text: 'is', italics: true },
    ' a K-simplex. This is not an analogy. When HUF says \u03A3\u03C1\u1D62 = 1 with K elements, the space of all possible ratio states is literally a (K\u22121)-dimensional simplex embedded in K-dimensional space. The vertices of \u0394_K are the extreme allocations (one element gets 100%), the edges are binary mixtures, and the triangular faces are three-element subportfolios.'
  ]));
  c.push(P('This means every triangular face of the simplex is a triad\u2014a three-element sub-allocation that sums to some portion of the total budget. The tetrahedron is the simplex for K=4 elements. The HUF framework has been living on this geometry since its inception; this exploration simply names the structure and asks how it scales.'));

  c.push(H2('5.2 Faces as Sub-Governance Domains'));
  c.push(P('Each face of the simplex represents a governance sub-problem. On a tetrahedron with elements {A, B, C, D}:'));
  c.push(bullet([{ text: 'Face ABC: ', bold: true }, 'Governance of three elements ignoring D\u2019s share']));
  c.push(bullet([{ text: 'Face ABD: ', bold: true }, 'Governance of three elements ignoring C\u2019s share']));
  c.push(bullet([{ text: 'Face ACD: ', bold: true }, 'Governance of three elements ignoring B\u2019s share']));
  c.push(bullet([{ text: 'Face BCD: ', bold: true }, 'Governance of three elements ignoring A\u2019s share']));
  c.push(P([
    'This is exactly what the ',
    { text: 'spectral sequence filtration', bold: true },
    ' does in Phase 3 (Milestone M2). The filtration F\u2080 \u2192 F\u2081 \u2192 F\u2082 \u2192 F\u2083 moves from individual elements to groups to subsystems to the whole system. Each filtration level is examining a different face (or collection of faces) of the simplex. The pages of the spectral sequence (E\u2080, E\u2081, ...) are refinements of what happens on each face.'
  ]));

  c.push(H2('5.3 Vertex Multiplicity as Governance Depth'));
  c.push(P('The number of triads per vertex measures how deeply an element is embedded in the governance structure:'));

  const gCols = [2000, 2000, 5360];
  c.push(new Table({
    width: { size: CW, type: WidthType.DXA }, columnWidths: gCols,
    rows: [
      new TableRow({ children: [
        headerCell('Triads per Vertex', gCols[0]), headerCell('System Size', gCols[1]),
        headerCell('Governance Implication', gCols[2]),
      ]}),
      new TableRow({ children: [
        dataCell('1', gCols[0], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('K = 3 (triangle)', gCols[1], { shade: LGREY }),
        dataCell('Minimal governance: element checked by 1 triad only', gCols[2], { shade: LGREY }),
      ]}),
      new TableRow({ children: [
        dataCell('3', gCols[0], { align: AlignmentType.CENTER }),
        dataCell('K = 4 (tetrahedron)', gCols[1]),
        dataCell('Moderate: element cross-checked by 3 independent triads', gCols[2]),
      ]}),
      new TableRow({ children: [
        dataCell('6', gCols[0], { shade: LGREY, align: AlignmentType.CENTER }),
        dataCell('K = 5 (5-cell)', gCols[1], { shade: LGREY }),
        dataCell('Strong: element governed by 6 overlapping constraints', gCols[2], { shade: LGREY }),
      ]}),
      new TableRow({ children: [
        dataCell('K(K\u22121)/2', gCols[0], { align: AlignmentType.CENTER }),
        dataCell('General K', gCols[1]),
        dataCell('Each element is cross-validated by quadratically many triads', gCols[2]),
      ]}),
    ],
  }));
  c.push(P(''));
  c.push(P([
    'This is a ',
    { text: 'self-strengthening property', bold: true },
    ': as the system grows, each element becomes more constrained, not less. A 10-element system (9-simplex) has C(9,2) = 36 triads constraining each element and C(10,3) = 120 triads total. Drift in any single element is visible from 36 different triangular perspectives simultaneously. This is why MDG becomes more powerful with larger K\u2014it\u2019s not just a bigger portfolio, it\u2019s a more deeply cross-referenced one.'
  ]));

  // ── 6. PREDICTIVE GEOMETRY ────────────────────────────────────────
  c.push(new Paragraph({ children: [new PageBreak()] }));
  c.push(H1('6. Predictive Growth Mapping'));
  c.push(P('The simplicial scaling law allows us to predict exactly how any HUF-governed system grows as elements are added. This section maps the growth for concrete HUF applications.'));

  c.push(H2('6.1 Growth in Current HUF Domains'));
  const dCols = [2200, 800, 900, 1200, 1200, 3060];
  c.push(new Table({
    width: { size: CW, type: WidthType.DXA }, columnWidths: dCols,
    rows: [
      new TableRow({ children: [
        headerCell('Domain', dCols[0]), headerCell('K', dCols[1]),
        headerCell('Triads', dCols[2]), headerCell('Edges', dCols[3]),
        headerCell('Triads/Vtx', dCols[4]), headerCell('Structure', dCols[5]),
      ]}),
      new TableRow({ children: [
        dataCell('HUF Pillars', dCols[0], { shade: LBLUE }), dataCell('3', dCols[1], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('1', dCols[2], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('3', dCols[3], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('1', dCols[4], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('Triangle (current)', dCols[5], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('Planck HFI', dCols[0]), dataCell('6', dCols[1], { align: AlignmentType.CENTER }),
        dataCell('20', dCols[2], { align: AlignmentType.CENTER }),
        dataCell('15', dCols[3], { align: AlignmentType.CENTER }),
        dataCell('10', dCols[4], { align: AlignmentType.CENTER }),
        dataCell('5-simplex (6D polytope)', dCols[5]),
      ]}),
      new TableRow({ children: [
        dataCell('TTC Network', dCols[0], { shade: LBLUE }), dataCell('~10', dCols[1], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('120', dCols[2], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('45', dCols[3], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('36', dCols[4], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('9-simplex (high cross-constraint)', dCols[5], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('ML Softmax (10-class)', dCols[0]), dataCell('10', dCols[1], { align: AlignmentType.CENTER }),
        dataCell('120', dCols[2], { align: AlignmentType.CENTER }),
        dataCell('45', dCols[3], { align: AlignmentType.CENTER }),
        dataCell('36', dCols[4], { align: AlignmentType.CENTER }),
        dataCell('9-simplex (every class in 36 triads)', dCols[5]),
      ]}),
      new TableRow({ children: [
        dataCell('Sourdough Culture', dCols[0], { shade: LBLUE }), dataCell('~5', dCols[1], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('10', dCols[2], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('10', dCols[3], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('6', dCols[4], { shade: LBLUE, align: AlignmentType.CENTER }),
        dataCell('4-simplex (moderate cross-constraint)', dCols[5], { shade: LBLUE }),
      ]}),
      new TableRow({ children: [
        dataCell('Transformer Head', dCols[0]), dataCell('~512', dCols[1], { align: AlignmentType.CENTER }),
        dataCell('~22M', dCols[2], { align: AlignmentType.CENTER }),
        dataCell('~131K', dCols[3], { align: AlignmentType.CENTER }),
        dataCell('~130K', dCols[4], { align: AlignmentType.CENTER }),
        dataCell('511-simplex (astronomically constrained)', dCols[5]),
      ]}),
    ],
  }));
  c.push(P(''));

  c.push(H2('6.2 What the Growth Predicts'));
  c.push(P('The scaling law predicts several properties of HUF-governed systems as they grow:'));
  c.push(bullet([{ text: 'Drift detection sensitivity increases with K. ', bold: true }, 'More triads per element means more independent vantage points from which to detect redistribution. This is why large-K systems (like transformer attention with 512+ tokens) should be the easiest place to detect overfitting via MDG\u2014the simplex is so richly cross-referenced that even tiny drifts are visible from many perspectives.']));
  c.push(bullet([{ text: 'False discovery rate should decrease with K. ', bold: true }, 'Each detected drift must be consistent across C(K,2) triads. A false positive in one triad is unlikely to appear simultaneously in all other triads containing that element. This aligns with Grok\u2019s spectral filtering result: FDR dropped from 0.12 to 0.05 when multi-scale filtering was applied.']));
  c.push(bullet([{ text: 'Computational cost grows cubically. ', bold: true }, 'C(K+1, 3) triads means O(K\u00B3) face evaluations. For K > ~1000, sparse approximations are needed\u2014exactly as Grok noted (AE, computation cost O(n\u00B3)). The tetrahedral geometry predicts exactly when this scaling wall hits.']));
  c.push(bullet([{ text: 'Ground state stability increases with dimensionality. ', bold: true }, 'On a high-dimensional simplex, the uniform distribution (center of mass) is the point most constrained by all faces. Perturbations must fight against quadratically many restoring triads. This is a geometric explanation for why the ground state (\u03C1 = uniform) is an attractor.']));

  // ── 7. BEYOND THE TETRAHEDRON ─────────────────────────────────────
  c.push(new Paragraph({ children: [new PageBreak()] }));
  c.push(H1('7. Beyond the Tetrahedron: Simplicial Complexes'));
  c.push(P('Real systems are not single simplices\u2014they are compositions of simplices glued along shared faces. This is a simplicial complex: the most general structure that triad-union geometry can produce.'));

  c.push(H2('7.1 Gluing Rules'));
  c.push(P('When two tetrahedra share a triangular face, the result is a structure with 5 vertices, 2 volumes, and 1 shared triad. The shared face is a union point in 3D\u2014the exact analog of a shared edge in the flat tiling. The rules for valid gluing are:'));
  c.push(bullet([{ text: 'Face matching: ', bold: true }, 'Two simplices may share a face of any dimension (vertex, edge, triangle, etc.)']));
  c.push(bullet([{ text: 'Unity preservation: ', bold: true }, 'The shared face inherits \u03A3\u03C1\u1D62 = 1 from both parent simplices\u2014the constraint must be consistent']));
  c.push(bullet([{ text: 'No overlap: ', bold: true }, 'Two simplices cannot share a volume (interior)\u2014only boundary faces']));
  c.push(P('This is precisely the structure that persistent homology analyzes. TDA\u2019s Vietoris-Rips complex builds a simplicial complex from distance data, adding simplices as elements come within proximity thresholds. The barcodes track which simplices (triads, tetrahedra, etc.) persist across scales.'));

  c.push(H2('7.2 The HUF Filtration as Simplicial Growth'));
  c.push(P([
    'The spectral engine\u2019s filtration (F\u2080 \u2192 F\u2081 \u2192 F\u2082 \u2192 F\u2083) can now be understood geometrically. At each filtration level, you are building a larger simplicial complex from smaller ones:'
  ]));
  c.push(bullet([{ text: 'F\u2080 (raw elements): ', bold: true }, 'Each element is a 0-simplex (point). No triads yet.']));
  c.push(bullet([{ text: 'F\u2081 (groups): ', bold: true }, 'Elements grouped into sub-portfolios. Each group of 3+ elements forms a simplex. Triads appear.']));
  c.push(bullet([{ text: 'F\u2082 (subsystems): ', bold: true }, 'Groups glued along shared elements. Tetrahedral and higher structures form.']));
  c.push(bullet([{ text: 'F\u2083 (system): ', bold: true }, 'The entire system as one K-simplex. All C(K+1, 3) triads active.']));
  c.push(P([
    'The Temporal Sieve (dHUF/dt) operates on this growing complex. At F\u2080, it detects element-level velocity. At F\u2083, it detects system-level structural redistribution. The spectral pages E_r refine what survives across filtration levels\u2014and what survives is precisely the ',
    { text: 'persistent', italics: true },
    ' simplicial structure: the triads and higher faces that remain valid across all scales.'
  ]));

  // ── 8. MAPPING CONJECTURE ─────────────────────────────────────────
  c.push(H1('8. The Mapping Conjecture'));
  c.push(P([
    { text: 'Evidentiary Tier: [CONJECTURE]', bold: true, color: MID },
    ' \u2014 Structurally motivated, testable, not yet formalized.'
  ]));
  c.push(P('Based on the geometry described above, we propose the following conjecture for the collective record:'));
  c.push(P(''));
  c.push(P([
    { text: 'Conjecture (Simplicial Governance Scaling): ', bold: true, italics: true },
    { text: 'For any finite-budget system with K elements governed by the unity constraint \u03A3\u03C1\u1D62 = 1, the governance structure is a K\u22121 simplex with C(K,3) triad constraints. As K increases: (a) drift detection power increases as O(K\u00B2) per element, (b) false discovery rate decreases as the cross-validation depth grows, (c) ground state stability increases with dimensionality, and (d) computational cost for full triad evaluation scales as O(K\u00B3). The structure can be mapped and its growth predicted by the binomial coefficients of the simplicial complex.', italics: true }
  ]));
  c.push(P(''));
  c.push(P('This conjecture is testable. The Hell Test already provides a baseline: at K=2 (a single edge, 0 triads), detection is limited. At K=12 (Level 5 of the Hell Test, 220 triads), detection should be markedly more sensitive. The M3 calibration milestone (power analysis across varying K) would directly test this scaling law.'));

  // ── 9. IMPLICATIONS ───────────────────────────────────────────────
  c.push(new Paragraph({ children: [new PageBreak()] }));
  c.push(H1('9. Implications for Phase 3'));
  c.push(bullet([{ text: 'M1 (Sufficiency Theorem): ', bold: true }, 'The theorem already operates on \u0394_K. The tetrahedral geometry provides a visual and structural vocabulary for explaining why sufficiency holds\u2014each face of the simplex is a sub-governance domain, and sufficiency means that the face structure captures all governance-relevant information.']));
  c.push(bullet([{ text: 'M2 (Spectral Drift Engine): ', bold: true }, 'The filtration F\u2080\u2192F\u2083 IS the progressive construction of the simplicial complex. Each page E_r refines which faces (triads, tetrahedra, etc.) persist. The Temporal Sieve operates on the growing complex, detecting velocity on each face independently.']));
  c.push(bullet([{ text: 'M3 (Power Calibration): ', bold: true }, 'The O(K\u00B2) per-element scaling of governance depth predicts that detection power should increase with K. This is a testable prediction: run the Hell Test at K=2, 4, 8, 16, 32 and measure detection rate vs K.']));
  c.push(bullet([{ text: 'M4 (ML Validation): ', bold: true }, 'A 10-class CIFAR softmax output lives on a 9-simplex with 120 triads. Each triad is an independent overfitting detector. MDG aggregated across all 120 triads should be a more robust signal than MDG on the full 10-element portfolio alone.']));

  c.push(H1('10. Conclusion'));
  c.push(P('The observation that a tetrahedron carries a triad on every face is not a metaphor\u2014it is a direct consequence of the simplex geometry that HUF already inhabits. The ratio portfolio \u03C1 lives on \u0394_K, which is a (K\u22121)-simplex, and every triangular face of that simplex is a natural triad constraint. The growth from triangle to tetrahedron to higher simplices follows exact combinatorial laws (binomial coefficients), making the structure fully predictable.'));
  c.push(P('The key insight is dimensional: HUF\u2019s triad is not a flat design choice but the first visible face of a three-dimensional (and ultimately K-dimensional) governance geometry. Each new element adds a dimension, multiplies the triad count, and deepens the cross-validation web. The framework doesn\u2019t just grow\u2014it self-reinforces.'));
  c.push(P([
    'This exploration is labeled ',
    { text: '[CONJECTURE]', bold: true },
    '. The simplicial geometry is mathematical fact (the simplex IS a simplicial complex). The governance scaling predictions (O(K\u00B2) detection depth, decreasing FDR, cubic computational cost) are testable conjectures that the Phase 3 milestones can directly address.'
  ]));

  return c;
}

// ══════════════════════════════════════════════════════════════════════
// BUILD
// ══════════════════════════════════════════════════════════════════════

const doc = new Document({
  styles, numbering,
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
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: 'HUF Tetrahedral Triad Geometry  \u00B7  March 2026',
            font: 'Times New Roman', size: 18, color: '999999', italics: true })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: 'Page ', font: 'Times New Roman', size: 18, color: '999999' }),
            new TextRun({ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 18, color: '999999' }),
          ],
        })],
      }),
    },
    children: buildContent(),
  }],
});

const outPath = process.argv[2] || 'HUF_Tetrahedral_Triad_Geometry.md';
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outPath, buf);
  console.log(`\u2705 Built: ${outPath} (${(buf.length / 1024).toFixed(1)} KB)`);
});
