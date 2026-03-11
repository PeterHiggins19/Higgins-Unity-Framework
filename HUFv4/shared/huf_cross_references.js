// ══════════════════════════════════════════════════════════════════════
// HUF Triad — Cross-Reference Matrix
// Every concept, which volumes treat it, at what depth
// ══════════════════════════════════════════════════════════════════════

// Depth codes: I = Introduced, D = Defined, P = Proved, A = Applied, E = Example
const XREF = [
  { concept: 'Unity Constraint (\u03A3\u03C1\u1D62 = 1)',       vol0: 'I', vol1: 'D', vol2: 'A', vol3: 'P', vol4: 'A', vol5: 'A', vol6: 'D', vol7: 'A', vol8: 'D' },
  { concept: 'Ratio State',                                      vol0: 'I', vol1: 'D', vol2: 'A', vol3: 'P', vol4: 'A', vol5: 'A', vol6: 'D', vol7: 'A', vol8: 'D' },
  { concept: 'Mean Drift Gap (MDG)',                              vol0: 'I', vol1: 'D', vol2: 'E', vol3: 'P', vol4: 'E', vol5: 'A', vol6: 'A', vol7: 'A', vol8: 'D' },
  { concept: 'Probability Simplex',                               vol0: '',  vol1: 'I', vol2: '',  vol3: 'D', vol4: '',  vol5: '',  vol6: 'D', vol7: 'A', vol8: 'D' },
  { concept: 'Degenerate Observer',                               vol0: '',  vol1: '',  vol2: '',  vol3: 'P', vol4: '',  vol5: 'I', vol6: 'D', vol7: '',  vol8: 'D' },
  { concept: 'Four Artifacts (A-1\u2013A-4)',                     vol0: '',  vol1: 'D', vol2: 'E', vol3: '',  vol4: 'A', vol5: 'D', vol6: '',  vol7: 'A', vol8: 'D' },
  { concept: 'Six Failure Modes (FM-1\u2013FM-6)',               vol0: '',  vol1: 'I', vol2: 'E', vol3: '',  vol4: 'A', vol5: 'D', vol6: 'A', vol7: '',  vol8: 'D' },
  { concept: 'Quality Factor (Q)',                                vol0: '',  vol1: 'I', vol2: 'E', vol3: 'P', vol4: 'A', vol5: 'A', vol6: 'A', vol7: '',  vol8: 'D' },
  { concept: 'OCC 51/49',                                         vol0: '',  vol1: 'D', vol2: '',  vol3: '',  vol4: 'A', vol5: 'D', vol6: '',  vol7: 'A', vol8: 'D' },
  { concept: 'Monitoring Categories (MC-1\u2013MC-4)',           vol0: '',  vol1: 'I', vol2: 'A', vol3: '',  vol4: 'A', vol5: 'D', vol6: 'D', vol7: '',  vol8: 'D' },
  { concept: 'Sufficiency Frontier',                              vol0: '',  vol1: '',  vol2: '',  vol3: 'P', vol4: '',  vol5: '',  vol6: 'D', vol7: '',  vol8: 'D' },
  { concept: 'Cross-Domain Normalization (CDN)',                  vol0: '',  vol1: 'I', vol2: 'A', vol3: 'P', vol4: '',  vol5: '',  vol6: 'D', vol7: 'A', vol8: 'D' },
  { concept: 'Ground State',                                      vol0: 'I', vol1: 'D', vol2: 'E', vol3: 'P', vol4: 'A', vol5: 'D', vol6: 'A', vol7: '',  vol8: 'D' },
  { concept: 'Institutional Memory',                              vol0: '',  vol1: 'I', vol2: '',  vol3: 'P', vol4: 'A', vol5: 'D', vol6: 'A', vol7: '',  vol8: 'D' },
  { concept: 'Aitchison Geometry',                                vol0: '',  vol1: '',  vol2: '',  vol3: 'D', vol4: '',  vol5: '',  vol6: 'D', vol7: '',  vol8: 'I' },
  { concept: 'Fisher Sufficiency',                                vol0: '',  vol1: '',  vol2: '',  vol3: 'D', vol4: '',  vol5: '',  vol6: 'D', vol7: '',  vol8: 'I' },
  { concept: 'PROOF Line',                                        vol0: 'I', vol1: 'D', vol2: 'E', vol3: '',  vol4: 'A', vol5: 'A', vol6: '',  vol7: 'A', vol8: 'D' },
  { concept: 'Leverage',                                          vol0: 'I', vol1: 'D', vol2: 'E', vol3: '',  vol4: 'A', vol5: 'A', vol6: '',  vol7: 'A', vol8: 'D' },
  { concept: 'Ostrom Design Principles',                          vol0: '',  vol1: '',  vol2: '',  vol3: '',  vol4: 'D', vol5: 'D', vol6: 'A', vol7: '',  vol8: 'D' },
  { concept: 'Convergence Stages',                                vol0: '',  vol1: 'I', vol2: 'E', vol3: 'P', vol4: '',  vol5: 'D', vol6: '',  vol7: '',  vol8: 'D' },
];

// Reading pathway annotations
const PATHWAYS = {
  'newcomer':     ['Vol 0', 'Vol 1', 'Vol 2', 'Vol 8'],
  'practitioner': ['Vol 0', 'Vol 1', 'Vol 5', 'Vol 4 or Vol 2'],
  'researcher':   ['Vol 8', 'Vol 3', 'Vol 6', 'Pillar 1', 'Pillar 2'],
  'developer':    ['Vol 0', 'Vol 7', 'Vol 1', 'Vol 3'],
  'policy_maker': ['Vol 8', 'Vol 5', 'Vol 4', 'Vol 2'],
};

module.exports = { XREF, PATHWAYS };
