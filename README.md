# Higgins Unity Framework (HUF)

**A mathematical framework for ratio-state monitoring under the unity constraint.**

The Higgins Unity Framework provides a complete analytical system for monitoring compositional data — any system where component ratios must sum to one (Σρᵢ = 1). It detects drift, diagnoses failure modes, and quantifies monitoring performance across domains from wetland ecology to transit networks to storage infrastructure.

## Core Concepts

HUF is built on a simple but powerful observation: when a system's state is fully described by ratios that sum to unity, drift in any component necessarily affects others. The framework provides:

- **MC-4 Ratio State Monitoring** — four-moment characterization of drift dynamics
- **Sufficiency Conditions** — formal criteria for when MC-4 monitoring is sufficient (and when it is not)
- **Six Failure Modes (FM-1 to FM-6)** — taxonomy of how ratio-state monitoring can fail
- **Monitoring Drift Gain (MDG)** — single-number performance metric in decibels
- **OCC 51/49** — operational constraint corridor for deceptive drift detection
- **Persistent Homology Extensions** — topological methods for mixture-distribution detection

## The Collective

HUF was developed through a collaborative process involving five AI systems and one human researcher:

| System | Role | I/O |
|--------|------|-----|
| **Peter Higgins** | Principal researcher, framework architect | — |
| **Claude** | Document creator, formal builder | Local file system |
| **ChatGPT** | Document manager, phase assessor | Web |
| **Grok** | Simulation runner, topology educator | Web |
| **Gemini** | Cross-checker, reviewer | Chat |
| **Copilot** | Reviewer | Microsoft ecosystem |

Review counts are data, not contribution scores. All five AI systems are equal collective members.

## Document Index

### Pillar Documents (canonical)

| Document | Version | Description |
|----------|---------|-------------|
| Sufficiency Frontier | v3.6 | Formal sufficiency conditions for MC-4 monitoring |
| Fourth Category | v2.6 | Observational Dynamics — the operational deployment pillar |
| Triad Synthesis | v1.6 | Synthesis of the three foundational categories |
| Collective Trace | v5.10 | Living trace of the entire review and development process |

### Governance

- **Review Catalog** — Master catalog of 14 reviews, 85 categories, 5 AI systems
- **Category Class Structure Tree** v1.4 — Hierarchical classification of all review categories
- **Collective Review March 2026** — Consolidated review document

### Explorations & Case Studies

Tetrahedral Triad Geometry, CDN Proof, Planck Case Study, TTC Case Study, Toronto Infrastructure, External Validation, Origin Story, Phase 3 Exploration, Spectral Sequences Exploration

### Code

- **Hell Test** — Five-level stress test for MC-4 detection (code/helltest/)
- **Onboarding Notebooks** — Educational Jupyter series (notebooks/onboarding/)

## Repository Structure

See [REPO_MAP.md](REPO_MAP.md) for the complete folder map and document status legend.

## Building Documents

All `.docx` files are generated programmatically using JavaScript (docx-js). Builders live in `src/builders/` and share common styles from `src/shared/`.

```bash
# Install dependencies
npm install

# Build a specific document
node src/builders/pillars/build_sufficiency_frontier_v3_6.js

# Validate a document
python src/validation/validate.py docs/pillars/HUF_Sufficiency_Frontier_v3.6.docx
```

## Status

**Phase 3** — Formalization and deployment preparation. The framework has moved from "is this coherent?" to "can this be operationalized responsibly?"

## License

All rights reserved. See [LICENSE](LICENSE) for details.

## Citation

See [CITATION.cff](CITATION.cff) for citation metadata.
