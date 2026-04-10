# Higgins Unity Framework (HUF)

*A proposal to treat compositional structure as an open-loop monitoring signal.*

HUF proposes that **composition** — the internal proportional balance of a system's parts — can be monitored as a primary observable alongside magnitude, identity, and trend. The claim is not new mathematics. The claim is a **monitoring application**: when a meaningful whole is divided into parts and expressed as proportions, the resulting ratio-state may reveal structural drift, concentration, hollowing, or redistribution that headline totals do not show.

HUF is presented here as an **open-loop framework**. The instrument reads. The human expert decides.

---

## New Discovery: Entropy-Invariant Time Transformer (EITT)

**April 2026.** Shannon entropy appears empirically near-invariant under geometric-mean temporal decimation of compositional time series in the energy datasets we tested.

Measured: **0.18% variation** across a 341:1 compression ratio (daily → annual European electricity compositions, 8 carriers, 4089 trading days). Confirmed independently on 6 countries at **1.02% mean variation**, then driven to **0.029%** on a third independent test (EMBER monthly data, Copilot calibrator suite).

For comparison, Aitchison variance drops 55% and total variation drops 99.7% across the same ladder. Shannon entropy changed very little in the tested ladders.

In the tested datasets, the geometric mean — a central operation in CoDa — appeared to act as an entropy-stabilizing temporal filter. Whether this generalizes, and why, remains open.

**Cross-domain confirmation (April 9, 2026).** EITT has now been tested on five domains beyond energy: hardware degradation (Backblaze drive stats, K=4, 24 months — 0.03%), a 120-stock price-level portfolio (K=9, 74 months — 0.08%; price-level weighted, not market-cap), cosmological observation (Planck 353 GHz half-mission temporal split — 0.3%), and commodities (gold/silver ratio, K=2, 338 years — fails at 6.7%, holds at 0.38% when reconstructed to K=4, validated out-of-sample). Bootstrap confidence intervals computed for all domains. The EITT inversion principle: when EITT fails on K parts, increasing K until it holds reveals the system's true dimensionality. **Honesty notes:** The Planck spatial EITT claim has been retracted (HEALPix NESTED pixel ordering does not preserve spatial locality). The financial composition is from a personal stock selection, not a standard index. At 2:1 compression, arithmetic-mean decimation also preserves entropy; the geometric mean's advantage appears at higher compression ratios. See code/analysis/honesty_tests_results_2026april9.txt for full adversarial test results.

We are presenting this as an empirical finding with a mapped boundary, not as a theorem.

**Exploratory: d(CoDa)/dt.** Alongside EITT, we are exploring a temporal derivative chain for compositions: perturbation velocity (scalar speed on the simplex), ILR balance trajectory (structural path), and balance derivative dB/dt (directed rate of structural change along each partition). This is a promising extension, not a settled result. It has been implemented in the tools and produces interpretable outputs on the tested datasets, but it has not been independently validated or formally connected to EITT. We include it here as work in progress.

| What to read | File | Time |
|--------------|------|------|
| The finding, the numbers, the mechanism | [`EITT_FINDING.md`](drafts/codawork-2026/EITT_FINDING.md) | 10 min |
| Plain-language explanation of everything | [`EITT_COMPLETE_EXPLANATION.md`](drafts/codawork-2026/EITT_COMPLETE_EXPLANATION.md) | 15 min |
| What this offers CoDa specifically | [`EITT_CODA_POSITION.md`](drafts/codawork-2026/EITT_CODA_POSITION.md) | 10 min |
| How EITT relates to 10 entropy territories | [`EITT_ENTROPY_LANDSCAPE.md`](drafts/codawork-2026/EITT_ENTROPY_LANDSCAPE.md) | 20 min |
| Adversarial testing (10 pass, 7 fail, boundary mapped) | [`EITT_Adversarial_001.json`](data/codawork-samples/S016/EITT_Adversarial_001.json) | 10 min |
| Copilot's calibrator lab and boundary condition | [`data/eitt_lab/`](data/eitt_lab/) | 30 min |
| The residual explained (Hessian footprint) | [`EITT_Residual_Analysis_001.json`](data/codawork-samples/S016/EITT_Residual_Analysis_001.json) | 15 min |

**Posture:** We found this empirically. We can't prove it. Can you?

---

## What HUF claims

- Composition can be monitored directly, rather than treated only as a statistical correction or secondary view.
- In some systems, meaningful structural change may appear in ratio-state before conventional magnitude-based indicators visibly fail.
- This proposal can be tested across domains where a conserved or interpretable whole can be divided into meaningful parts.

## What HUF does not claim

- HUF does **not** claim new simplex or compositional mathematics. The mathematical foundations are Aitchison (1982), Stevens (1946), Shannon (1948), and Amari (1985).
- HUF does **not** claim universal validity across all domains. Cross-domain validity must be earned domain by domain.
- HUF does **not** claim that every compositional change is harmful, actionable, or predictive.
- HUF does **not** replace domain expertise, causal explanation, or policy judgment.
- HUF does **not** justify autonomous intervention on the basis of compositional readings alone.
- HUF is a monitoring proposal, not a settled scientific result.

## How to test HUF

1. Choose a domain with a meaningful whole and clearly defined parts.
2. Normalize the parts into proportions.
3. Compare compositional signals against standard indicators and expert judgment.
4. Check whether HUF-style monitoring adds earlier, clearer, or more reliable signal.
5. Publish negative results, failure cases, and domain limits alongside positive findings.

The standard for progress is independent replication, not internal coherence.

---

## Start here

| Time | Read | File |
|------|------|------|
| 5 min | The scientist handoff — the coldest summary of what this is | [`HANDOFF-001.docx`](huf-gov/governance/HANDOFF-001.docx) |
| 15 min | The monitoring taxonomy — what the four categories are and why the fourth was missing | [`MONITOR-001.json`](huf-gov/science/MONITOR-001.json) |
| 30 min | A reproducible case — Germany electricity, EMBER dataset, p = 0.0016 | [`energy/`](huf-gov/evidence/case-studies/energy/) |
| 30 min | The kill test — 19 documented failure modes, the things this framework cannot do | [`KILL-001-kill-test.json`](huf-gov/governance/KILL-001-kill-test.json) |

If you want to break it, the kill test is where to start.

**New:** For a faster onboarding path with CoDa integration, see [`START_HERE.md`](START_HERE.md) — 60-second, 5-minute, and 30-minute entry paths plus the full repository map.

---

## The four monitoring categories

| Category | Name | Question | Status |
|----------|------|----------|--------|
| MC-1 | Magnitude Monitoring | How much? | Universally deployed |
| MC-2 | Identity Monitoring | Who or what? | Universally deployed |
| MC-3 | Trend Monitoring | Which direction? | Universally deployed |
| **MC-4** | **Composition Monitoring** | **What is the internal balance?** | **Diagnostically invisible in standard practice** |

The mathematics is not new. Compositional data analysis on the simplex was formalized by John Aitchison in 1982 (Journal of the Royal Statistical Society). The measurement taxonomy was formalized by Stanley Smith Stevens at Harvard in 1946. What is new is the application: treating compositional structure as a primary monitoring observable rather than a post-hoc statistical correction.

---

## Evidence

Each case below is reproducible from files in this repository.

- **Electricity generation (EMBER):** Germany — structural concentration p = 0.0016 behind stable total generation. See [`ember-drift-analysis.json`](huf-gov/evidence/case-studies/energy/ember-drift-analysis.json) and [`HUF_Energy_Case_Study_v1.0.docx`](huf-gov/evidence/case-studies/energy/HUF_Energy_Case_Study_v1.0.docx).
- **GDP composition (World Bank):** Japan p = 0.0098, China p = 0.0196 — internal drift behind stable headline GDP. See [`GDP_Deceptive_Drift_Analysis_v2.0.json`](huf-gov/evidence/case-studies/gdp/GDP_Deceptive_Drift_Analysis_v2.0.json).
- **Scale invariance:** 35 million tests, 10 to 10 million elements, zero violations, 5.23 sigma. See [`RSM_Scale_Invariance_Simulation_v1.0.json`](huf-gov/evidence/scale-invariance/RSM_Scale_Invariance_Simulation_v1.0.json).
- **Ecosystem monitoring (Ramsar template):** Structural thinning of habitat diversity behind stable total-area figures. See [`ramsar/`](huf-gov/evidence/case-studies/ramsar/).

**Limitations:** The forward signal findings are conditional on internal concentration regimes. HUF does not detect external shocks (earthquakes, pandemics, policy interventions). Negative cases — Fukushima, COVID-19, Australian bushfires — are documented alongside the positive findings.

---

## Documented failure modes

The full kill test is in [`KILL-001-kill-test.json`](huf-gov/governance/KILL-001-kill-test.json). Key failure modes include:

- **KILL-1.1:** Carrier admitted without domain justification — the instrument reads noise as structure.
- **KILL-1.2:** Fewer than 3 carriers — the simplex is too low-dimensional for meaningful composition.
- **KILL-3.3:** Fabricated or synthetic data — garbage in, structurally plausible garbage out.
- **KILL-4.1:** Automated actuation without human review — the loop closes without consent.
- **KILL-4.4:** Framework applied to a domain where proportional structure has no physical meaning.

If you find a failure mode not on this list, please open an issue.

---

## Repository structure

### Core framework

| Directory | Function | Description |
|-----------|----------|-------------|
| [`huf-gov/`](huf-gov/) | **Observation** | The open-loop instrument. Science, evidence, governance, tools. |
| [`huf-cls/`](huf-cls/) | **Control** | The closed-loop actuator. Included for transparency. Not part of the Coimbra / CoDaWork ask. |
| [`reference/`](reference/) | **Foundation** | 68 machine-readable JSON specifications, technical notes, pillar documents. |

### Supporting material

| Directory | Description |
|-----------|-------------|
| [`context-books/`](context-books/) | Four audience-specific editions of the core theory (general, engineering, physics, sciences). |
| [`math-books/`](math-books/) | Formal mathematical foundations. 42 numbered items with full proofs. |
| [`process/`](process/) | How this was built — collective review traces, session ledgers, governance documents. |
| [`drafts/`](drafts/) | Submission papers (pre-validation), the Human-AI Accord, EITT materials. Work in progress. |
| [`data/`](data/) | Reproducible datasets: EMBER energy, CoDaWork samples, EITT lab (calibration, adversarial, residual). |
| [`code/`](code/) | Analysis scripts (Backblaze, energy, HellTest stress tests), diagnostic tools. |
| [`src/`](src/) | Document generation build system (JS builders + shared modules + Python validation). |
| [`notebooks/`](notebooks/) | Onboarding Jupyter series (5 interactive tutorials). |
| [`docs/`](docs/) | Generated canonical documents: explorations, governance, 7 academic paper drafts, reference. |

### Governance documents

| Document | What it does |
|----------|-------------|
| [`LOOP-001`](huf-gov/governance/LOOP-001-open-loop-doctrine.json) | Open-loop doctrine — the instrument reads, the human decides. |
| [`KILL-001`](huf-gov/governance/KILL-001-kill-test.json) | Kill test — 19 failure modes. |
| [`SAFE-001`](huf-gov/governance/SAFE-001.json) | Safe operations doctrine — 7 principles. |
| [`HAGF-001`](huf-gov/governance/HAGF-001.json) | Human-AI governance framework. |

### Tools

| Tool | Description |
|------|-------------|
| [`Spectrum Analyzer v3 (HTML)`](huf-gov/tools/spectrum-analyzer/HUF_Spectrum_Analyzer_v3.html) | **Unified dual-metric dashboard.** 10 panels: original HUF metrics (K_eff, TV velocity, peak) + CoDa methods (CLR, ILR balances, Aitchison distance, perturbation velocity, distance matrix). Ternary simplex, carrier ribbon, complexity heatmap, 2025 crisis snapshots. Zero dependencies — open in any browser. |
| [`Spectrum Analyzer v3 (JSX)`](huf-gov/tools/spectrum-analyzer/HUF_Spectrum_Analyzer_v3.jsx) | React/JSX version with phase display, carrier ribbon, group phase. |
| [`CoDa Explorer`](drafts/codawork-2026/huf_coda_explorer.html) | 6-panel CoDa visualization: ternary, time prism, CLR, perturbation velocity, ILR balances, Aitchison distance matrix. CoDaWork 2026 conference tool. |
| [`Ternary EMBER`](drafts/codawork-2026/ternary_ember.html) | Interactive ternary diagram (Fossil/Nuclear/Renewable) for 3 countries 2000–2025. CoDaWork 2026 pedagogical tool. |
| [`Ramsar Demo`](huf-gov/tools/ramsar-demo/Ramsar_Wetlands_Template.json) | Wetland species composition monitoring template. |

Pre-CoDa tools (v2 analyzer, Universal analyzer) have been moved to [`archive/tools-pre-coda/`](archive/tools-pre-coda/). Git history preserves all prior states.

### CoDaWork 2026 Conference Materials

Abstract accepted by Prof. Juan Jose Egozcue, Chair of the Scientific Committee. Conference: June 1-6, 2026, Coimbra, Portugal. See [`drafts/codawork-2026/`](drafts/codawork-2026/) for the full preparation suite including formulas, vocabulary, researcher profiles, battle card, executive summary, core explanation, the HUF-CoDa translator, and all EITT materials.

**New in April 2026 — EITT:** The Entropy-Invariant Time Transformer discovery. Shannon entropy near-invariant under geometric-mean temporal decimation. Full finding, adversarial testing, residual analysis, calibration lab, boundary conditions, and an entropy landscape mapping EITT against 10 existing entropy territories. See [`EITT_FINDING.md`](drafts/codawork-2026/EITT_FINDING.md) and [`data/eitt_lab/`](data/eitt_lab/).

**Entry point for CoDa community:** [`START_HERE.md`](START_HERE.md) — includes a "For CoDa / Compositional Data Analysts" section with direct links to all relevant materials including EITT.

---

## On HUF-CLS being public

The closed-loop system was originally held behind engineered breakers. The decision to publish it under MIT license was made on March 29, 2026. The reasoning: suppression does not prevent misuse — it prevents understanding. If someone will close the loop, it is better that the architecture, the failure modes, and the governance principles are public knowledge than that they are reinvented without them.

Read the CLS README before exploring: [`huf-cls/README.md`](huf-cls/README.md).

---

## Process and provenance

This framework was developed over six months by Peter Higgins, with six AI systems (Claude, ChatGPT, Gemini, Copilot, Grok, DeepSeek) contributing under human direction. The operator governed the process. The AI systems were the instruments. The loop stayed open.

The complete development record — 26 collective review traces, session ledgers, voting registers, and governance documents — is in [`process/`](process/). It is included because the provenance chain is part of the claim: this was built with documented governance, not invented overnight.

---

## Contact

Peter Higgins
Rogue Wave Audio
Markham, Ontario, Canada
[PeterHiggins@RogueWaveAudio.com](mailto:PeterHiggins@RogueWaveAudio.com)

---

## License

MIT License. See [LICENSE](LICENSE).

Developed with Claude (Anthropic), ChatGPT (OpenAI), Gemini (Google), Copilot (Microsoft), Grok (xAI), and DeepSeek under human direction. 2025–2026.
