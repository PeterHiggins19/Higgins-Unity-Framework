# HUF Repository Map

*Updated: 2026-04-09 (S016 — EITT discovery, repo reorganization)*

## Folder Structure

```
HUF/
├── README.md                      # What HUF claims, EITT discovery, how to test it
├── START_HERE.md                  # Tiered entry paths (60s, 5m, 30m) + CoDa welcome
├── CITATION.cff                   # Academic citation metadata
├── CONTRIBUTING.md                # 5-AI collective development model
├── VERSION_MANIFEST.json          # Machine-readable version tracking
├── package.json                   # Node.js dependency (docx-js) for build system
│
├── huf-gov/                       # The open-loop instrument
│   ├── science/                   # MONITOR-001 taxonomy, papers
│   ├── evidence/case-studies/     # Energy, GDP, Backblaze, Ramsar, Planck, Toronto
│   ├── governance/                # LOOP-001, KILL-001, SAFE-001, HANDOFF-001
│   └── tools/spectrum-analyzer/   # v3 HTML analyzer + JSX source
│
├── huf-cls/                       # The closed-loop actuator (published for transparency)
│   ├── architecture/              # CL-01 through CL-05
│   ├── formulas/                  # Sigmoid actuator, K_eff, amplifier
│   └── calibration/               # CL-05 sensitivity analysis
│
├── reference/                     # Foundation
│   ├── machine-readable/          # 68+ JSON specifications
│   ├── pillars/                   # Theory, methodology, architecture (.docx)
│   ├── technical-notes/           # PLL, calibration, architecture, interaction studies
│   └── wiki/                      # Quick-reference articles
│
├── data/                          # Reproducible datasets
│   ├── manifests/                 # Data, benchmark, and release manifests
│   ├── checksums/                 # SHA256 document integrity hashes
│   ├── codawork-samples/S016/     # EITT adversarial, midrange confirmation, residual
│   └── eitt_lab/                  # ★ EITT calibration lab
│       ├── copilot_outputs/       # Calibrator suite, boundary condition, PCA variants
│       └── claude_analysis/       # Residual analysis (Hessian footprint)
│
├── drafts/                        # Submission papers, conference materials, work in progress
│   ├── codawork-2026/             # CoDaWork 2026 full preparation suite
│   │   ├── EITT_FINDING.md        # ★ The EITT discovery
│   │   ├── EITT_CODA_POSITION.md  # ★ What EITT offers CoDa
│   │   ├── EITT_ENTROPY_LANDSCAPE.md # ★ EITT vs 10 entropy territories
│   │   ├── EITT_COMPLETE_EXPLANATION.md # ★ Plain-language walkthrough
│   │   ├── DANCE_CARD.md          # Conference strategy + 8 union territories
│   │   ├── THE_CORE.md            # Coherence chain for CoDa community
│   │   ├── FORMULA_REFERENCE.md   # HUF↔CoDa formula reference
│   │   ├── BATTLE_CARD.md         # 10 hardest questions
│   │   └── ...                    # Abstract, translator, explorer, ternary, etc.
│   ├── accord/                    # Human-AI Accord
│   └── papers/                    # Academic submissions
│
├── docs/                          # Generated canonical documents
│   ├── explorations/              # Case studies (Backblaze, energy, CDN, Planck, TTC)
│   ├── governance/                # Review catalog, governance explainer, provenance
│   ├── papers/                    # 7 academic submissions (CBD, CoDa, GEOBON, IEEE, etc.)
│   ├── reference/                 # Handbooks, math foundations, Ramsar package
│   ├── appendices/                # Code appendix, methodology appendix
│   └── wiki/                      # Quick-reference markdown articles
│
├── src/                           # Document build system
│   ├── builders/                  # JavaScript docx-js builder scripts
│   │   ├── pillars/               # Pillar document builders
│   │   ├── volumes/               # Volume builders (Triad Synthesis)
│   │   ├── governance/            # Trace and tree builders
│   │   ├── explorations/          # Case study and proof builders
│   │   └── reviews/               # AI review document builders
│   ├── shared/                    # Common modules (styles, citations, glossary)
│   └── validation/                # validate.py (docx integrity checker)
│
├── code/                          # Executable analysis tools
│   ├── analysis/                  # Backblaze, energy analysis scripts
│   ├── helltest/                  # MC-4 detection stress test (scripts, notebooks, results)
│   └── tools/                     # JSX diagnostic utilities
│
├── notebooks/                     # Educational content
│   └── onboarding/                # HUF onboarding series (00-04)
│
├── context-books/                 # 4 audience editions (general, engineering, physics, sciences)
├── math-books/                    # Formal proofs (42 numbered items)
│
├── process/                       # Development record
│   ├── collective-reports/        # AI collective reviews and master packages
│   ├── governance-docs/           # Voting register, decision log, deployment strategy
│   ├── review-traces/             # Version-traced review documents (v1.0-v5.10)
│   └── session-ledgers/           # Per-session JSON records
│
├── archive/                       # Preserved history (nothing deleted, just organized)
│   ├── HUFv4/                     # Pre-Phase 3 working directory (version histories)
│   ├── concepts/                  # Experimental research (Kardashev, unity-vcore)
│   ├── legacy-builders/           # Superseded builder scripts
│   ├── legacy-generated-docs/     # Superseded .docx outputs
│   ├── legacy-traces/             # Early review traces
│   ├── papers-v1/                 # First-draft academic papers
│   ├── prototypes/                # Layout prototypes
│   ├── ramsar-pre-standardized/   # Early Ramsar materials
│   ├── superseded/                # Explicitly superseded items
│   └── tools-pre-coda/            # Pre-CoDa analyzer versions
│
└── .github/workflows/             # CI: validate and build
```

★ = New in S016 (April 2026) — EITT discovery materials

## Document Status Legend

| Status | Meaning |
|--------|---------|
| **Canonical** | Current latest version, lives in `docs/` |
| **Active Draft** | Work in progress, lives in `drafts/` |
| **Superseded** | Replaced by newer version; preserved in git history or `archive/` |
| **Archival** | Historical artifact; lives in `archive/` with provenance note |
| **Experimental** | Exploratory work; lives in `code/` or `archive/concepts/` |

## Release Policy

Only canonical documents live on `main`. Superseded versions are accessible through git tags, commit history, or GitHub Releases (binary attachments). The `VERSION_MANIFEST.json` tracks what is current.

## For CoDa Researchers

If you're arriving from CoDaWork 2026 or the compositional data analysis community, start with [`START_HERE.md`](START_HERE.md) — the "For CoDa" section points directly to the EITT finding and all supporting materials. The short version: we found that Shannon entropy is near-invariant under geometric-mean temporal decimation, and we think the CoDa community is best positioned to prove (or disprove) it.
