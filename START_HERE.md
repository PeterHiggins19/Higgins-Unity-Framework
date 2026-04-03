# HUF — Start Here

## 60-Second Version

HUF monitors the *internal balance* of systems where parts sum to a whole. A country's electricity mix, a wetland's species distribution, a market's sector allocation — when the total looks stable but the parts quietly rearrange, HUF detects it. The math is not new (Aitchison, 1982). The monitoring application is.

## 5-Minute Path

| Step | What | File | Time |
|------|------|------|------|
| 1 | See it work | Open [`HUF_Spectrum_Analyzer_v3.html`](huf-gov/tools/spectrum-analyzer/HUF_Spectrum_Analyzer_v3.html) in a browser. Click "Germany." Scrub through years. Watch the gauges and all 10 panels. | 2 min |
| 2 | Read the claim | [`README.md`](README.md) — What HUF claims, what it does not claim, how to test it. | 2 min |
| 3 | Try to break it | [`KILL-001`](huf-gov/governance/KILL-001-kill-test.json) — 19 documented failure modes. If you find one not on this list, open an issue. | 1 min |

## 30-Minute Path

| Step | What | File |
|------|------|------|
| 1 | The coldest summary | [`HANDOFF-001.docx`](huf-gov/governance/HANDOFF-001.docx) |
| 2 | The monitoring taxonomy (MC-1 through MC-4) | [`MONITOR-001.json`](huf-gov/science/MONITOR-001.json) |
| 3 | A reproducible case (Germany electricity, EMBER data) | [`energy/`](huf-gov/evidence/case-studies/energy/) |
| 4 | The kill test (19 failure modes) | [`KILL-001`](huf-gov/governance/KILL-001-kill-test.json) |
| 5 | The v3 analyzer (10 panels, dual metrics) | [`HUF_Spectrum_Analyzer_v3.html`](huf-gov/tools/spectrum-analyzer/HUF_Spectrum_Analyzer_v3.html) |

## For Engineers

Start with the [HUF Learning Path — Engineering Edition](reference/HUF_Learning_Path_Engineering.md). Ten phases, 25–35 hours total, minimum viable path in 10–14 hours.

## For CoDa / Compositional Data Analysts

Start with the [CoDaWork 2026 conference materials](drafts/codawork-2026/). Key files:

| File | What it covers |
|------|---------------|
| [`THE_CORE.md`](drafts/codawork-2026/THE_CORE.md) | The 1→2→4 coherence chain — how HUF's monitoring architecture maps to nested compositions on the simplex |
| [`huf_coda_translator.md`](drafts/codawork-2026/huf_coda_translator.md) | Full HUF↔CoDa vocabulary translation table |
| [`FORMULA_REFERENCE.md`](drafts/codawork-2026/FORMULA_REFERENCE.md) | Every CoDa formula (CLR, ILR, Aitchison distance, perturbation, balances) mapped to HUF equivalents |
| [`EXECUTIVE_SUMMARY.md`](drafts/codawork-2026/EXECUTIVE_SUMMARY.md) | The cylinder analogy — what HUF does in plain language |
| [`abstract_v1.md`](drafts/codawork-2026/abstract_v1.md) | The CoDaWork 2026 accepted abstract |
| [`HUF_Spectrum_Analyzer_v3.html`](huf-gov/tools/spectrum-analyzer/HUF_Spectrum_Analyzer_v3.html) | Unified analyzer with CoDa methods (CLR, ILR balances, Aitchison distance matrix, perturbation velocity) |

## For Everyone Else

Read the [Executive Summary](drafts/codawork-2026/EXECUTIVE_SUMMARY.md). It uses two metaphors: a cylinder that looks like a circle from one end and a rectangle from the side (HUF watches the cylinder, not the shadows), and a fuel gauge that shows the tank is full but doesn't tell you the fuel changed.

## Tools

| Tool | What it does | Location |
|------|-------------|----------|
| **Spectrum Analyzer v3** | 10-panel dual-metric dashboard (TV + Aitchison). Gauges, ternary, CLR, ILR balances, perturbation velocity, Aitchison distance matrix, 2025 crisis snapshots. Open in any browser. | [`HUF_Spectrum_Analyzer_v3.html`](huf-gov/tools/spectrum-analyzer/HUF_Spectrum_Analyzer_v3.html) |
| **CoDa Explorer** | 6-panel CoDa-focused visualization (ternary, time prism, CLR, perturbation, balances, distance matrix) | [`huf_coda_explorer.html`](drafts/codawork-2026/huf_coda_explorer.html) |
| **Ternary Diagram** | Interactive ternary with Fossil/Nuclear/Renewable trajectories for 3 countries | [`ternary_ember.html`](drafts/codawork-2026/ternary_ember.html) |
Pre-CoDa tools (v2, Universal) are in [`archive/tools-pre-coda/`](archive/tools-pre-coda/) for reference.

## Key Concepts (Quick Reference)

| Concept | One-line explanation |
|---------|---------------------|
| Composition | A vector of proportions that sums to a constant — a point on the simplex |
| Simplex (S^D) | The geometric space where compositions live |
| Perturbation | Compositional change measured as ratios, not differences |
| Aitchison distance | The natural metric on the simplex — RMS of all pairwise log-ratio changes |
| CLR transform | Centered log-ratio — maps simplex to real space for standard statistics |
| ILR balances | Interpretable log-ratio coordinates from a hierarchical partition of carriers |
| K_eff | Effective number of carriers — exp(Shannon entropy). Measures diversity. |
| Silent drift | Composition changed but no governance decision was logged |
| MC-4 | Composition Monitoring — the fourth monitoring category, diagnostically invisible in standard practice |
| Coherence chain | Nested carrier groups (1→2→4) where group coherence gates inter-group analysis |

## CoDa Methods in HUF (new in v3)

The v3 analyzer implements Compositional Data Analysis methods alongside original HUF metrics:

| Method | Implementation | Panel |
|--------|---------------|-------|
| Aitchison distance d_A(x,y) | √[(1/D) Σᵢ<ⱼ (ln(xᵢ/xⱼ) − ln(yᵢ/yⱼ))²] | Panels 7, 8, gauges |
| CLR transform | ln(xᵢ / geometric mean) | Panel 5 |
| ILR balances | √(rs/(r+s)) · ln(g(x⁺)/g(x⁻)) via SBP | Panel 6 |
| Perturbation velocity | v(t) = d_A(x(t), x(t−1)) | Panel 7 |
| Aitchison distance matrix | Pairwise d_A for all year pairs | Panel 8 |
| Ternary sub-composition | Closure of Fossil/Nuclear/Renewable | Panel 4 |

These complement HUF's original metrics (TV distance, K_eff complexity, peak carrier change) to provide dual-metric monitoring — both information-theoretic and simplex-native measures on the same data.

## Repository Map

```
HUF-repo/
├── README.md                    ← What HUF claims and how to test it
├── START_HERE.md                ← You are here
├── LICENSE                      ← MIT
│
├── huf-gov/                     ← The open-loop instrument
│   ├── science/                 ← MONITOR-001 taxonomy, papers
│   ├── evidence/case-studies/   ← Energy, GDP, Backblaze, Ramsar, Planck, Toronto
│   ├── governance/              ← LOOP-001, KILL-001, SAFE-001, HANDOFF-001
│   └── tools/spectrum-analyzer/ ← v3 HTML analyzer + JSX source
│
├── huf-cls/                     ← The closed-loop actuator (published for transparency)
│   ├── architecture/            ← CL-01 through CL-05
│   ├── formulas/                ← Sigmoid actuator, K_eff, amplifier
│   └── calibration/             ← CL-05 sensitivity analysis
│
├── reference/                   ← Foundation
│   ├── machine-readable/        ← 68 JSON specifications
│   ├── pillars/                 ← Theory, methodology, architecture (.docx)
│   ├── technical-notes/         ← PLL, calibration, architecture, interaction studies
│   └── wiki/                    ← 4 quick-reference articles
│
├── drafts/codawork-2026/        ← CoDaWork 2026 conference materials (18 files)
│   ├── THE_CORE.md              ← Core explanation of HUF for CoDa community
│   ├── FORMULA_REFERENCE.md     ← HUF↔CoDa formula quick reference
│   ├── VOCABULARY_CARD.md       ← CoDa vocabulary cheat sheet
│   ├── BATTLE_CARD.md           ← 10 hardest questions with honest answers
│   ├── EXECUTIVE_SUMMARY.md     ← Cylinder + fuel gauge metaphors
│   ├── RESEARCHERS_CARD.md      ← Who's who at CoDaWork
│   └── ...                      ← Abstract, translator, explorer, ternary, etc.
│
├── context-books/               ← 4 audience editions (general, engineering, physics, sciences)
├── math-books/                  ← Formal proofs (42 numbered items)
├── data/                        ← Sample datasets
├── archive/                     ← Superseded files (v1 papers, pre-CoDa tools)
└── process/                     ← Development record (26 collective review traces)
```

## What's New (April 2026)

- **CoDaWork 2026 accepted.** Abstract accepted by Prof. Egozcue (Scientific Committee Chair). Conference June 1-6, Coimbra, Portugal.
- **v3 Spectrum Analyzer.** 10 panels, dual metrics (TV + Aitchison distance), CoDa methods (CLR, ILR, perturbation velocity, Aitchison distance matrix), 2025 crisis snapshots.
- **CoDa integration.** Full translation between HUF vocabulary and Compositional Data Analysis terminology. Aitchison geometry formalized as the geometric foundation of HUF's monitoring architecture.
- **18 conference preparation files** covering formulas, vocabulary, researchers, battle card, executive summary, core explanation, and the HUF↔CoDa translator.
- **Coherence chain formalized.** The 1→2→4 nested carrier group hierarchy identified as the core of HUF — from loudspeaker drivers to energy carriers to wetland species.

## How to Test HUF on a New Domain

1. Choose a system where parts sum to a meaningful whole.
2. Define the carriers (the parts).
3. Normalize each time period into a composition on the simplex.
4. Compute perturbation velocity (Aitchison distance between consecutive periods).
5. Look for spikes (structural shocks) and sustained trends (drift).
6. Compare against known events — do the compositional signals match reality?
7. Publish what you find, especially negative results.

The [food production prompt](drafts/codawork-2026/) provides a template for applying HUF to FAO crop data using any AI system and the public GitHub repo.

## Contact

Peter Higgins — Rogue Wave Audio — Markham, Ontario, Canada
[PeterHiggins@RogueWaveAudio.com](mailto:PeterHiggins@RogueWaveAudio.com)
[GitHub](https://github.com/PeterHiggins19/Higgins-Unity-Framework)

MIT License. Developed with Claude, ChatGPT, Gemini, Copilot, Grok, and DeepSeek under human direction.
