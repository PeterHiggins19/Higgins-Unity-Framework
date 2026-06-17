# AI-refresh — 2026-06-07 corpus reconciliation (HUF)

**Audience.** Any AI agent or collaborator picking up the Higgins-Unity-Framework (HUF) repo on or after 2026-06-07.
**Prepared by.** Cowork (Opus 4.8) session acting as corpus authority. Verified against the GitHub REST API and the local mirror `Current-Repo/HUF`. Actual commits/pushes remain Peter's gate via GitHub Desktop.
**Companion.** Mirror-root `CORPUS_MAP_2026-06-07.md` + `CORPUS_MANIFEST_2026-06-07.json` (the whole-corpus picture across all three repos).

---

## Why this file exists

HUF's canonical loaders had drifted: `HUF_ADMIN.json` was last updated 2026-04-22 and `HUF_FAST_REFRESH.json` 2026-04-28, while the repo accumulated a large body of uncommitted April work and the project's centre of gravity moved to the **higgins-decomposition (Hs)** repo for the CoDaWork 2026 conference. This record reconciles the state so the next session starts grounded.

## Current state (verified 2026-06-07)

| Fact | Value |
|---|---|
| GitHub remote | `PeterHiggins19/Higgins-Unity-Framework` (branch `master`) |
| Remote last push | **2026-04-24** |
| Mirror last commit | 2026-04-18 (`498dece`) |
| Uncommitted in mirror | **193 files** — 151 new + 42 modified |
| Admin / refresh | `HUF_ADMIN.json` was 04-22, `HUF_FAST_REFRESH.json` was 04-28 (both `_meta.updated` bumped to 2026-06-07 with this reconciliation) |

### What the 193 uncommitted files are (factual, from the working tree)

- **`codawork2026/` (~130 files)** — a full experiment package: EXP-01…EXP-18b "12-step canonical" runs (paired `.json` + `.png`), per-experiment **integrity certificates**, validation/summary reports, and bundled `data/` (Acoustics, Commodities, Energy, Nuclear). Never committed.
- **`ai-refresh/` (~13 new + several modified)** — April cross-AI material: ChatGPT scientific review (04-19) and updates (04-20, 04-23), a Gemini O1 analytic-proof + conversation, `HUF_COMPLETE_REFERENCE.json`, `HUF_MASTER_CHECKSUM_CATALOG.json`, `Higgins_Decomposition_Migration_Manifest.json`, EITT component/testing registries, CoDaWork presentation outline; plus modified cold-start briefings and test-results.
- **`science/` (~6 new + modified)** — EITT mathematics/decomposition docs, cross-disciplinary value matrix, quantum primers, reference material.
- **Modified at root**: `INDEX.json`, `README.md`, the two admin/refresh JSONs, integrity manifest, mathematical addendum, master lineage, phase markers.

All of this dates to April; HUF saw no substantial new work after ~2026-04-28. The "very behind" condition is **uncommitted April work + a stale GitHub remote**, not missing recent work.

## Action owed (Peter, via GitHub Desktop)

1. Review and **commit the `codawork2026/` experiment package** (with its integrity certificates) and the `ai-refresh/` + `science/` additions.
2. **Push** `master` to GitHub (remote is ~7 weeks behind).
3. If the GitHub-Desktop originals folder is ahead of this mirror, reconcile against it before committing.

## Honest-broker note (carry forward)

EITT (Entropy-Invariant Time Transformer) is, per the current Hs working notes, a **diagnostic / null-model**: roughly half of the observed invariance is attributable to temporal autocorrelation, and the internal 0.18% / 341:1 figures are unverified. Do **not** present EITT as a denoiser, reconstructor, or controller. The higgins-decomposition (Hs) repo holds the current canonical claim tiers (confirmed / experimental / not-implemented); HUF documents must not inflate beyond them.

---

*Reconciliation record only — no canonical names, numbers, or formulas were changed. The instrument reads. The expert decides. The hashes carry the receipts.*
