# HUF repo map — what's here and how to read it (2026‑06‑11)

*A single legible map of the HUF repository at the clean‑start rebuild. HUF accumulated a lot ("it went everywhere it could"); this map says what each part is and whether it's **support/current** or **historical/preserved** — without moving or deleting anything (lose nothing). The current instrument is Hˢ; see [`RELATIONSHIP_TO_Hs.md`](RELATIONSHIP_TO_Hs.md). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001.*

---

## Front door (read in this order)

1. [`README.md`](README.md) — what HUF is + the role banner.
2. [`RELATIONSHIP_TO_Hs.md`](RELATIONSHIP_TO_Hs.md) — HUF's place in the arc; the HUF↔Hˢ division of labour.
3. [`AI_ASSIST.json`](AI_ASSIST.json) — the bring‑your‑own‑AI hub; climbs forward to the Hˢ repo.
4. `ai-refresh/HUF_FAST_REFRESH.json` — HUF's own source of truth (history). *On any conflict about the **current** state, `Hs/HS_FAST_REFRESH.json` wins.*

## Top‑level folders

| Folder | ~files | Role | Status |
|---|---|---|---|
| `huf-gov/` | 63 | **Governance (current discipline)** — `doctrine/` (open‑loop/safe‑ops/kill‑test/MC‑4), `NASA_STYLE_GOVERNANCE`, charter, carrier filter, ratio blindness, `standards/` (HUF‑STD‑001/002/003), `_legacy_2026-03/` | **SUPPORT (current)** |
| `ai-refresh/` | 38 | **Admin chain** — HUF_FAST_REFRESH, HUF_ADMIN, MASTER_LINEAGE, PHASE_MARKERS, cross‑AI cold‑start briefings + reviews, the HUF→Hˢ migration manifest | **SUPPORT (current)** |
| `science/` | 122 | **Scientific record** — coda‑monitoring, geochemistry, quantum, wetlands, spectral | SUPPORT (historical record) |
| `codawork2026/` | 453 | The CoDaWork 2026 package (experiments, deliverables) — *the live conference face is in `Hs/CODA-Association/`* | HISTORICAL (superseded by Hˢ's) |
| `briefings/` | 32 | Narrative briefings incl. `THE_LINEAGE.md` (founding narrative) | SUPPORT (lineage) |
| `discoveries/` | 17 | Discovery write‑ups | HISTORICAL record |
| `drafts/` | 28 | In‑progress / draft material | HISTORICAL drafts |
| `dormant/` | 34 | Dormant / parked experiments | HISTORICAL (preserved, lose nothing) |
| `archive/` | 603 | The big historical archive — prior versions, letters, papers, staged docs | HISTORICAL (preserved) |
| `tools/` | 40 | Supporting tooling | SUPPORT |
| `data/` | 79 | Datasets used by the studies | SUPPORT (instrument‑not‑data: read where it lives) |

## Reading rule

- **Want the current instrument / to run something?** → the [Hˢ repo](https://github.com/PeterHiggins19/higgins-decomposition). HUF does not hold the live engine.
- **Want to understand where an idea came from, or the governance?** → here: `RELATIONSHIP_TO_Hs.md`, `huf-gov/`, `briefings/THE_LINEAGE.md`, `ai-refresh/MASTER_LINEAGE.json`.
- **Historical/archived material is preserved, not promoted** — it carries its original claim tiers; the current canon is Hˢ's.

## What the rebuild did (and didn't)

- **Did:** added the role banner + `RELATIONSHIP_TO_Hs.md` + the `AI_ASSIST.json` hub + this map; kept the `huf-gov/` governance modernization (doctrine + NASA‑style + ratio‑blindness) from the 2026‑06‑11 session; kept the LFS `.gitattributes` (binaries stay lean).
- **Didn't:** delete or relocate any historical content; rewrite the science record; touch the Hˢ canon. The big admin JSONs (`HUF_FAST_REFRESH.json`, `HUF_ADMIN.json`) are edited Windows‑side per DVR‑1.0 (the sandbox truncates them).

*The past is the strength and the future. Lose nothing; make it legible.*
