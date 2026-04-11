# Contributing to HUF

## The Collective Model

HUF is developed by a five-AI collective (Claude, Grok, ChatGPT, Gemini, Copilot) coordinated by Peter Higgins. Each system contributes reviews, simulations, or formal builds. Contributions are tracked in `docs/governance/review_catalog.md`.

## Build Workflow

### Prerequisites

- Node.js 18+
- Python 3.10+
- npm packages: `docx` (docx-js)

### Building a Document

```bash
npm install
node src/builders/pillars/build_sufficiency_frontier_v3_6.js
```

### Validating a Document

```bash
python src/validation/validate.py docs/pillars/HUF_Sufficiency_Frontier_v3.6.docx
```

Validation checks paragraph count, structural integrity, and XML well-formedness.

## Versioning

Documents use semantic versioning: `vMAJOR.MINOR`.

- **Major** increments signal structural or conceptual changes.
- **Minor** increments signal additions, corrections, or refinements.

Builder scripts are named to match: `build_sufficiency_frontier_v3_6.js` builds `HUF_Sufficiency_Frontier_v3.6.docx`.

Only the latest canonical version lives in `docs/`. Superseded versions are preserved in git history.

## Review Process

1. Reviews are submitted by any collective member.
2. Claude catalogs the review in `review_catalog.md` with extracted categories and an assessment.
3. The Category Class Structure Tree and Collective Trace are updated to reflect new categories.
4. Categories use alphabetical naming: A-Z, then AA-AZ, BA-BZ, CA-CH, etc.

## Release Policy

- **Main branch** holds the canonical surface only.
- **Git tags** mark milestone versions (e.g., `v3.6-SF`, `v5.10-trace`).
- **GitHub Releases** attach binary snapshots of generated `.docx` files.
- Superseded `.docx` files are not committed to main.

## Style Guide

All documents follow the HUF style system defined in `src/shared/huf_styles.js`:

- Font: Times New Roman
- Heading color: #1F3864
- Standard table formatting with blue headers and alternating rows
- Five-tier evidentiary taxonomy: [THEOREM], [EMPIRICAL], [IDENTITY], [CONJECTURE], [PEDAGOGICAL]
