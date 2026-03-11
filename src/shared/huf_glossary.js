// ══════════════════════════════════════════════════════════════════════
// HUF Triad — Unified Glossary
// 27+ terms with consistent definitions across all volumes
// Source: wiki_huf_taxonomy_complete.md Layer 2 + extensions
// ══════════════════════════════════════════════════════════════════════

const GLOSSARY = [
  { term: 'Budget Ceiling', symbol: 'M', definition: 'The total of a finite-budget system, indexed to 1.0. The ceiling is fixed; it does not grow or shrink with usage.', volume: 'Vol 1' },
  { term: 'Element', symbol: 'i', definition: 'Any constituent of a portfolio that holds a share of the budget ceiling. Minimum: two elements.', volume: 'Vol 1' },
  { term: 'Share', symbol: '\u03C1\u1D62', definition: 'An element\u2019s proportional portion of the budget ceiling at a given point in time. Always a ratio, never an absolute. \u03C1\u1D62 = m\u1D62 / M where M = \u03A3m\u2C7C.', volume: 'Vol 1' },
  { term: 'Ratio State', symbol: '\u03C1', definition: 'The complete description of a finite-budget system at a point in time, expressed as a vector of shares summing to 1.0.', volume: 'Vol 1' },
  { term: 'Unity Constraint', symbol: '\u03A3\u03C1\u1D62 = 1', definition: 'The foundational constraint of HUF. Satisfied by every valid portfolio state. Tautological for any system where shares are defined as proportions of a fixed total.', volume: 'Vol 1' },
  { term: 'Probability Simplex', symbol: 'S\u1D37', definition: 'The geometric space of all valid portfolio states: the set of K-dimensional vectors whose components are non-negative and sum to 1. All HUF operations occur on or near this surface.', volume: 'Vol 3' },
  { term: 'Declared Weight', symbol: '\u03C1\u1D62\u1D48\u1D49\u1D9C', definition: 'The share an operator states each element should hold, prior to observation. Also sums to 1.0.', volume: 'Vol 1' },
  { term: 'Observed Share', symbol: '\u03C1\u1D62\u1D52\u1D47\u02E2', definition: 'The share an element actually holds in the current ratio state, computed from the system\u2019s declared outputs.', volume: 'Vol 1' },
  { term: 'Drift Gap', symbol: '|\u03C1\u1D62\u1D48\u1D49\u1D9C \u2212 \u03C1\u1D62\u1D52\u1D47\u02E2|', definition: 'The absolute difference between an element\u2019s declared weight and its observed share.', volume: 'Vol 1' },
  { term: 'Mean Drift Gap', symbol: 'MDG', definition: 'The average drift gap across all elements: (1/K) \u03A3 |\u03C1\u1D62\u1D48\u1D49\u1D9C \u2212 \u03C1\u1D62\u1D52\u1D47\u02E2|. Expressed in percentage points (pp).', volume: 'Vol 1' },
  { term: 'Intentional Reweighting', symbol: '\u2014', definition: 'A change in ratio state traceable to a recorded governance decision.', volume: 'Vol 5' },
  { term: 'Silent Drift', symbol: '\u2014', definition: 'A change in ratio state not traceable to any recorded decision. The primary detection target of HUF.', volume: 'Vol 5' },
  { term: 'Leverage', symbol: '1/\u03C1\u1D62', definition: 'The reciprocal of an element\u2019s observed share. Unitless. Measures sensitivity to removal or under-resourcing.', volume: 'Vol 1' },
  { term: 'PROOF Line', symbol: '\u2014', definition: 'The minimum number of elements required to hold a specified fraction (default 80%) of portfolio mass. Lower = more concentrated.', volume: 'Vol 2' },
  { term: 'Quality Factor', symbol: 'Q', definition: 'Q = T_char / T_obs. The ratio of an element\u2019s characteristic contribution period to its observation bandwidth. High-Q elements contribute specifically and cyclically; low-Q elements contribute broadly and steadily.', volume: 'Vol 3' },
  { term: 'Ground State', symbol: 'MDG \u2192 0', definition: 'The portfolio condition in which mean drift gap approaches zero, all allocation change is declared, and the feedback loop is self-correcting.', volume: 'Vol 1' },
  { term: 'Action Window', symbol: '\u2014', definition: 'The period during which correction of observed drift is cheapest \u2014 open when drift is detectable and before it compounds.', volume: 'Vol 5' },
  { term: 'Ratio Blindness', symbol: 'FM-1', definition: 'The systematic failure that occurs when a finite-budget system is managed using absolute metrics. Root cause of all six failure modes.', volume: 'Vol 2' },
  { term: 'Silent Reweighting', symbol: 'FM-2', definition: 'Gradual allocation drift occurring below the threshold of formal governance decisions. The mechanism through which all subsequent failure modes operate.', volume: 'Vol 2' },
  { term: 'Snapshot Error', symbol: 'FM-3', definition: 'Systematic underestimation of high-Q elements by single-cycle observation. Phase read as contribution.', volume: 'Vol 2' },
  { term: 'Concentration Trap', symbol: 'FM-4', definition: 'Portfolio allocating an increasing share to a decreasing number of dominant elements. Efficient short-term, fragile long-term.', volume: 'Vol 2' },
  { term: 'Fragmentation Spiral', symbol: 'FM-5', definition: 'Portfolio allocating sub-threshold attention to too many elements simultaneously. No element receives effective attention.', volume: 'Vol 2' },
  { term: 'Orphan Element', symbol: 'FM-6', definition: 'An element present on paper but effectively outside the governance system. Terminal state of FM-4 or FM-5 for a specific element.', volume: 'Vol 2' },
  { term: 'Aitchison Distance', symbol: 'd_A', definition: 'The natural metric on the probability simplex. MDG is a first-order approximation. Used for rigorous distance measurement between portfolio states.', volume: 'Vol 3' },
  { term: 'Cross-Domain Normalization', symbol: 'CDN', definition: '\u03A9 = |\u0394MDG| \u00D7 \u03B2 where \u03B2 = K/K_eff. Allows comparison of drift signals across domains with different element counts.', volume: 'Vol 6' },
  { term: 'Operator Control Contract', symbol: 'OCC 51/49', definition: 'w_op \u2265 0.51, w_tool \u2264 0.49. The operator always retains majority control over governance decisions. HUF advises; it does not decide.', volume: 'Vol 5' },
  { term: 'Degenerate Observer', symbol: 'L = 0', definition: 'A state observer where the state IS the output: y(t) = \u03C1(t). Zero estimation error without requiring a dynamic model. The mathematical basis of MC-4.', volume: 'Vol 3' },
  { term: 'Institutional Memory', symbol: '\u2014', definition: 'The accumulated record of a governance system\u2019s ratio states, declared intents, and responses across all reporting cycles. Accumulates at one state per cycle, permanently.', volume: 'Vol 5' },
  { term: 'Sufficiency Frontier', symbol: '\u2014', definition: 'The boundary in reduction-ratio space where information reduction transitions from lossy compression to sufficient statistic extraction. HUF operates beyond this frontier at 6,357,738:1.', volume: 'Vol 6' },
  { term: 'Monitoring Category 4', symbol: 'MC-4', definition: 'Ratio State Monitoring. The fourth monitoring category, introduced by HUF. Uses the system\u2019s own declared intent as the reference. Self-referential, non-invasive, model-free, bidirectional, cross-cycle.', volume: 'Vol 5' },
];

module.exports = { GLOSSARY };
