# Higgins Unity Framework (HUF)

*Compositional structure as an open-loop monitoring signal.*

HUF proposes that **composition** — the internal proportional balance of a system's parts — can be monitored as a primary observable alongside magnitude, identity, and trend. The instrument reads. The human expert decides.

---

## The Discovery: EITT

**Entropy Invariance under Temporal Transformation.** Shannon entropy appears empirically near-invariant under geometric-mean block decimation of compositional time series.

Measured: **0.18% variation** across a 341:1 compression ratio (daily to annual European electricity compositions, 8 carriers, 4089 trading days). Confirmed across energy, hardware degradation, cosmological observation, commodities, and chemistry.

**April 2026: Chemistry extension.** EITT tested on 500,000 chemical mixture data points (CheMixHub benchmark, 7 datasets). Four diagnostic lenses applied simultaneously. Interior compositions pass at 54-82%. Boundary compositions reveal simplex curvature effects. First empirical decomposition of geometric vs. dynamic contributions to the invariance.

This produced three new frameworks:

| Framework | What It Does | Document |
|-----------|-------------|----------|
| **EITT Findings** | Raw science. Four-lens results, failure taxonomy, multi-modal simplex | [`science/chemistry/`](science/chemistry/EITT_Chemistry_Findings.docx) |
| **HUF-IDX** | Development index. What residuals mean. Domain distance from ground zero | [`science/chemistry/`](science/chemistry/HUF_Development_Index.docx) |
| **PRISM** | Operational layer. Ranked resource allocation targets from residual analysis | [`science/chemistry/`](science/chemistry/PRISM_Chemistry_Analysis.docx) |

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
├── science/                    # The unified front
│   ├── chemistry/              # EITT chemistry results, HUF-IDX, PRISM
│   ├── core/                   # EITT mathematics, complete explanation, formulas
│   └── methodology/            # Compositional governance scale, confidence index
│
├── huf-gov/                    # Active governance
│   ├── governance/             # Standards, protocols, kill tests
│   ├── science/                # Monitoring taxonomy, ontological foundation
│   └── evidence/               # Case studies (energy, backblaze, planck, ramsar)
│
├── tools/                      # Everything runnable
│   ├── pipeline/               # EITT pipeline, preparsers, analysis scripts
│   ├── diagnostics/            # Validators, dashboards, diagnostic JSX
│   ├── spectrum-analyzer/      # HUF Spectrum Analyzer (all versions)
│   └── shared/                 # Build utilities, styles, glossary
│
├── drafts/codawork-2026/       # CoDaWork 2026 conference materials
│
├── data/                       # Datasets (energy, backblaze, toronto, eitt-lab)
│
└── archive/                    # Development history (everything pre-restructure)
```

---

## Start Here

| Time | What | Where |
|------|------|-------|
| 15 min | **User Handbook** — fast summary + guided links into the full document set | [`science/core/HUF_USER_HANDBOOK.md`](science/core/HUF_USER_HANDBOOK.md) |
| 5 min | What HUF is, in plain language | [`science/core/WHAT_HUF_IS.md`](science/core/WHAT_HUF_IS.md) |
| 10 min | The EITT finding and the numbers | [`science/core/EITT_Finding.md`](science/core/EITT_Finding.md) |
| 15 min | Full explanation with CoDa mathematics | [`science/core/EITT_CODA_MATHEMATICS.md`](science/core/EITT_CODA_MATHEMATICS.md) |
| 20 min | Chemistry results (the new frontier) | [`science/chemistry/`](science/chemistry/) |
| 30 min | The kill test — 19 documented failure modes | [`huf-gov/governance/`](huf-gov/governance/) |

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
