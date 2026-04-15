# Higgins Unity Framework (HUF)

**An independent research project in Compositional Data Analysis (CoDa) and entropy-invariant monitoring on the simplex.** This is a scientific research repository — not a game engine, not a Unity plugin, not a software library.

*Author: Peter Higgins, Rogue Wave Audio, Markham, Ontario, Canada*

**Core discovery:** The Entropy-Invariant Time Transformer (EITT) — Shannon entropy of compositional time series is empirically near-invariant under geometric-mean decimation. Measured at **0.18% variation** across a 341:1 compression ratio. Validated across energy systems, chemistry (500,000 data points), hardware reliability, and climate scenarios.

**Disciplines:** Compositional Data Analysis, Shannon entropy, Aitchison geometry, simplex monitoring, quantum information correspondence, energy transition analysis.

**Conference:** CoDaWork 2026, Coimbra, Portugal (June 2026). Abstract page 25.

**Phase status (2026-04-15):** Phase 1 (CoDaWork 2026 submission content) marked STABLE. Phase 2 (EITT hardening for broader adoption) started the same day. Mission for Phase 2: *push EITT to pain point and protect users from pain.* See [`ai-refresh/PHASE_MARKERS.json`](ai-refresh/PHASE_MARKERS.json), [`science/eitt/EITT_PHASE_2_ROADMAP.md`](science/eitt/EITT_PHASE_2_ROADMAP.md), and [`science/eitt/EITT_SAFETY_BOUNDARIES.md`](science/eitt/EITT_SAFETY_BOUNDARIES.md).

---

## What This Project Is

HUF proposes that **composition** — the internal proportional balance of a system's parts — can be monitored as a primary observable alongside magnitude, identity, and trend. The instrument reads. The human expert decides. The loop stays open.

The framework builds on Aitchison (1982/1986) simplex geometry and Shannon (1948) entropy, applying them to longitudinal monitoring of any system where parts share a conserved whole: energy grids, chemical mixtures, drive fleets, financial portfolios, wetland ecosystems.

---

## The Discovery: EITT (Entropy-Invariant Time Transformer)

Shannon entropy appears empirically near-invariant under geometric-mean block decimation of compositional time series. This is not a theorem — it is an empirical observation awaiting formal proof.

Measured: **0.18% variation** across a 341:1 compression ratio (daily to annual European electricity compositions, 8 carriers, 4089 trading days). Confirmed independently on EMBER monthly generation data (6 countries, mean 1.02%, all below 2%) and NGFS Phase 4 climate scenarios (35 scenarios, all below 5%).

**April 2026 — Chemistry extension.** EITT tested on 500,000 chemical mixture data points (CheMixHub benchmark, 7 datasets). Four diagnostic lenses applied simultaneously (Shannon, Jensen-corrected, Renyi q=2, Aitchison norm). Interior compositions pass at 54-82%. Boundary compositions reveal simplex curvature effects. First empirical decomposition: approximately 50% of the invariance comes from Aitchison geometry, approximately 50% from temporal autocorrelation.

This produced three new frameworks:

| Framework | What It Does | Document |
|-----------|-------------|----------|
| **EITT Findings** | Raw science. Four-lens results, failure taxonomy, multi-modal simplex | [`science/eitt/`](science/eitt/EITT_Chemistry_Findings.md) |
| **HUF-IDX** | Development index. What residuals mean. Domain distance from ground zero | [`science/eitt/`](science/eitt/INDEX.json) |
| **PRISM** | Operational layer. Ranked resource allocation targets from residual analysis | [`science/eitt/`](science/eitt/PRISM_Chemistry_Analysis.md) |

**Posture:** We found this empirically. We can't prove it. Can you?

---

## The Four Monitoring Categories

| Category | Name | Question | Status |
|----------|------|----------|--------|
| MC-1 | Magnitude Monitoring | How much? | Universally deployed |
| MC-2 | Identity Monitoring | Who or what? | Universally deployed |
| MC-3 | Trend Monitoring | Which direction? | Universally deployed |
| **MC-4** | **Composition Monitoring** | **What is the balance?** | **Proposed (HUF)** |

---

## Repository Structure

```
HUF/
├── ai-refresh/                     # AI STARTS HERE — fast context loading
│   ├── HUF_FAST_REFRESH.json       #   All canonical values, single file
│   ├── HUF_INTEGRITY_MANIFEST.json #   Hash verification, drift patterns
│   └── huf_spec_v2.0.json          #   Complete framework specification
│
├── science/                        # All scientific work by subject
│   ├── reference/                  #   Core reference (9 docs, ~105 min)
│   ├── core/                       #   EITT maths, formulas, user handbook
│   ├── methodology/                #   Governance scale, confidence index
│   ├── chemistry/                  #   CheMixHub results, HUF-IDX, PRISM
│   ├── quantum/                    #   HUF-QIT: 9 isomorphisms, Bell test
│   ├── eitt/                       #   EITT evidence: 4 proofs, adversarial
│   ├── coda-monitoring/            #   Perturbation drift detection protocol
│   ├── spectral/                   #   Frequency-domain analysis
│   ├── loudspeaker-analogy/        #   Origin: crossover networks as CoDa
│   ├── wetlands/                   #   Ramsar Convention monitoring
│   └── governance/                 #   201-country ranking outputs
│
├── huf-gov/                        # Active governance
│   ├── governance/                 #   Standards, protocols, kill tests
│   ├── science/                    #   Monitoring taxonomy, ontology
│   └── evidence/                   #   Case studies (energy, backblaze, etc.)
│
├── tools/                          # Everything runnable
│   ├── pipeline/                   #   EITT pipeline, preparsers, scripts
│   ├── diagnostics/                #   Validators, dashboards, UML diagrams
│   ├── spectrum-analyzer/          #   HUF Spectrum Analyzer (all versions)
│   └── shared/                     #   Build utilities, styles, glossary
│
├── drafts/                         # Conference materials, papers, proposals
│   ├── codawork-2026/              #   CoDaWork 2026, Coimbra
│   │   ├── presentation/           #     Main talk slide deck
│   │   ├── primers/                #     4 personalized researcher primers
│   │   ├── preparation/            #     Q&A prep, conversation guide
│   │   └── extended/               #     Extended results, EITT handout
│   ├── papers/                     #   Paper submissions (7 venues)
│   ├── proposals/                  #   Unified proposal, integration briefs
│   └── books/                      #   Book-length QIT treatments
│
├── briefings/                      # Session briefings & AI handoffs
│
├── data/                           # Datasets by domain
│   ├── backblaze/                  #   Hard drive failure data
│   ├── energy/                     #   EMBER/OWID energy data
│   ├── ember/                      #   EMBER processed results
│   ├── ngfs/                       #   NGFS Phase 4 scenarios
│   ├── codawork-samples/           #   Reproducible CoDaWork samples
│   ├── eitt-lab/                   #   EITT lab package
│   └── toronto/                    #   TTC transit data
│
├── dormant/                        # Paused branches — sleeping, not dead
│   ├── pre-coda-metrics/           #   Pre-CoDa metric formulations
│   ├── early-governance/           #   Multi-AI collective experiments
│   ├── planck-case/                #   Planck sky map analysis
│   ├── peterson-outreach/          #   Peterson letters (paused)
│   ├── hagf/                       #   Adaptive governance (superseded)
│   └── deceptive-drift/            #   Arithmetic hiding composition changes
│
└── archive/                        # Superseded work — what failed speaks loudest
```

---

## For AI Systems

**Start here:** Read [`ai-refresh/HUF_FAST_REFRESH.json`](ai-refresh/HUF_FAST_REFRESH.json) first. It contains every canonical name, number, formula, and structural rule. If anything elsewhere disagrees with FAST_REFRESH, the FAST_REFRESH wins. Then verify with [`ai-refresh/HUF_INTEGRITY_MANIFEST.json`](ai-refresh/HUF_INTEGRITY_MANIFEST.json). Then read [`INDEX.json`](INDEX.json) for the full file map.

**Context aggregator:** Run `python build_context.py --mode seed` to generate a single paste-ready text file containing the full AI seed layer. Modes: `seed` (~9k tokens), `science` (~232k tokens), `full` (~346k tokens).

**Known drift traps:** EITT is "Entropy-Invariant Time Transformer" (never Ternary). Japan drift flag is 2013-2014 (never 2011-2012). Germany is 2023-2024/2024-2025 (never 2011). UK has three specific values (2.98, 3.23, 3.26), never "approximately 3".

---

## Start Here (Humans)

| Time | What | Where |
|------|------|-------|
| 5 min | The cylinder problem and fuel gauge — one-page HUF | [`science/reference/`](science/reference/01_EXECUTIVE_SUMMARY.md) |
| 105 min | **Reference Collection** — 9 documents, full learning path | [`science/reference/INDEX.md`](science/reference/INDEX.md) |
| 15 min | **User Handbook** — fast summary + guided links | [`science/core/HUF_USER_HANDBOOK.md`](science/core/HUF_USER_HANDBOOK.md) |
| 20 min | Chemistry results (the new frontier) | [`science/chemistry/`](science/chemistry/) |
| 30 min | The kill test — 19 documented failure modes | [`huf-gov/governance/`](huf-gov/governance/) |
| 10 min | Quantum correspondence (advanced) | [`science/quantum/`](science/quantum/) |

If you want to break it, the kill test is where to start.

---

## What HUF Claims

- Composition can be monitored directly, not only as a statistical correction.
- In some systems, structural change appears in ratio-state before magnitude-based indicators visibly fail.
- This can be tested across any domain where a conserved whole divides into meaningful parts.

## What HUF Does Not Claim

- New simplex mathematics. The foundations are Aitchison (1982), Shannon (1948), Stevens (1946), Amari (1985).
- Universal validity. Cross-domain validity must be earned domain by domain.
- That every compositional change is harmful, actionable, or predictive.
- That HUF replaces domain expertise, causal explanation, or policy judgment.
- That autonomous intervention is justified on compositional readings alone.

---

## Dormant Branches

Nothing dies here — only goes dormant. The `dormant/` folder preserves paused work with documented reasons and conditions for reawakening. The `archive/` folder holds superseded and rejected approaches as reference for what was tried and why. What failed always speaks louder.

---

## Governance

**Standard:** RWA-001 (Rogue Wave Audio Corporate Reference)

**Protocol:** HUF-GOV. Measure, report, file. No intervention on the data.

**Multi-AI Review:** All core findings subjected to adversarial review by Claude, ChatGPT, Grok, Gemini, and Copilot.

---

## License

MIT. See [LICENSE](LICENSE).

## Citation

See [CITATION.cff](CITATION.cff).

## Contact

Peter Higgins | Rogue Wave Audio | PeterHiggins@RogueWaveAudio.com

Repository: [github.com/PeterHiggins19/Higgins-Unity-Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework)
