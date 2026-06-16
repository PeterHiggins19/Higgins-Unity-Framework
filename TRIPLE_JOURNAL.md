# Triple journal — the system-wide journal index (RWA · HUF · Hˢ)

*A reference copy of the whole system's activity, carried **identically in all three repos**. From any one repo you can see what the other two keep and what recent change touched more than one of them. Part of the shared "map of the whole" set — see [`DOCUMENT_DISTRIBUTION.md`](DOCUMENT_DISTRIBUTION.md). Companion machine-readable log: [`TRIPLE_JOURNAL.json`](TRIPLE_JOURNAL.json). Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001; honest-broker; lose nothing; Peter is the gate.*

**What this is, and why it exists.** Each repo keeps its own detailed journals (§1). This file does three small things on top of that: it **indexes** every repo's journals so any reader can jump straight to another repo's history; it keeps a **cross-repo change log** (§2) of edits that affect more than one repo; and because it lives in triplicate, it is a **distributed backup** — if one repo's history is lost, the cross-repo record survives in the other two. A minor but real help in complexity management: the load of "knowing what everyone is doing" is distributed, not centralized.

---

## 1 · Per-repo journal index — where each repo keeps its own history

| Repo | Primary journal hub | Also | Source of truth |
|---|---|---|---|
| **Hˢ** (run it) | [`../higgins-decomposition` → `EXPERIMENTS_JOURNAL.md`](EXPERIMENTS_JOURNAL.md) — full experiment lineage; per-experiment `JOURNAL.md` under `experiments/` and `HCI-CNT/experiments/` | `CHANGELOG.md` · `ai-refresh/PUSHES_INDEX.md` · `ai-refresh/HS_TRACKING_LOG.json` · `ai-refresh/JOURNALING_PROTOCOL.md` | `HS_FAST_REFRESH.json` |
| **HUF** (govern it) | `ai-refresh/MASTER_LINEAGE.json` — the arc-of-discovery index; `briefings/THE_LINEAGE.md` — founding narrative | `ai-refresh/PHASE_MARKERS.json` · `ai-refresh/AI_REFRESH_2026-06-07_corpus_reconciliation.md` · the `session_log` array in `HUF_FAST_REFRESH.json` | `ai-refresh/HUF_FAST_REFRESH.json` |
| **RWA** (it began in sound) | `LINEAGE.md` — the arc from the RWA side | `RWA_ADMIN.json` · `AI_REFRESH_2026-06-07_corpus_reconciliation.md` · `HUF_RELATIONSHIP.json` | `RWA_FAST_REFRESH.json` |

*(Paths are repo-relative; resolve cross-repo paths with `CROSS_BRAIN.md`. From RWA or HUF, an Hˢ path like `EXPERIMENTS_JOURNAL.md` means `../higgins-decomposition/EXPERIMENTS_JOURNAL.md` → the Hˢ repo.)*

System-wide arc, source to network: [`ARC_OF_DISCOVERY.md`](ARC_OF_DISCOVERY.md). Pre-push manifests sit at the development-mirror root (e.g. `PUSH_READY_2026-06-11_arc_eitt.md`).

---

## 2 · Cross-repo change log — changes that touched more than one repo

Newest first. Log here **only** changes that affect more than one repo (or that the others should know about); single-repo work stays in that repo's own journals (§1). Each entry: date · what · repos affected · shared files touched.

| Date | Change | Repos | Shared files touched |
|---|---|---|---|
| 2026-06-12 | **RWA-001 made the single contact authority** — personal addresses scrubbed (carrier-filter); all active contact-bearing JSONs now reference `RWA-001` | RWA · HUF · Hˢ | `RWA-001.json` (new `contact_authority` block) + `contact_authority` pointers across the admin/science JSONs |
| 2026-06-12 | **History thread + graduate-school ai-refresh** — the common development+necessity thread, and the deep onboarding curriculum woven from it; ai-refresh entry points elevated | RWA · HUF · Hˢ | `HISTORY_THREAD.md`, `GRADUATE_SCHOOL.md` (+ ai-refresh JSON pointers) |
| 2026-06-12 | **Triple journal added** — this system-wide journal index + cross-repo log, identical in all three | RWA · HUF · Hˢ | `TRIPLE_JOURNAL.md`, `TRIPLE_JOURNAL.json` (registered in `DOCUMENT_DISTRIBUTION.*`) |
| 2026-06-12 | **Document-distribution policy + coherence verifier** — the general rule (three homes; single source of truth; the shared set) + `verify_tri_repo_coherence.py` | RWA · HUF · Hˢ | `DOCUMENT_DISTRIBUTION.md`, `DOCUMENT_DISTRIBUTION.json` |
| 2026-06-12 | **Unified `.gitattributes`** — one file-handling policy (no LFS; text raw + LF). Fixed RWA's `arc_of_discovery.svg` shipping as an LFS pointer | RWA · HUF · Hˢ | `.gitattributes` |
| 2026-06-12 | **`CROSS_BRAIN.md` made a true all-three file** — RWA now carries it (was URL-only); pre-existing Hˢ↔HUF §3 drift reconciled | RWA · HUF · Hˢ | `CROSS_BRAIN.md` |
| 2026-06-11 | **EITT repositioned** — "key point of contact, divided influence"; "Transformer" documented as the Smaart-v9 phase-wrap etymology | HUF (system-wide concept) | `science/eitt/EITT_THE_PLACE_IT_HOLDS.md`, `HUF_FAST_REFRESH.json`, README |
| 2026-06-11 | **Arc of Discovery + three-level READMEs + maintained References/Acknowledgments** | RWA · HUF · Hˢ | `ARC_OF_DISCOVERY.md`, `arc_of_discovery.svg`, README Level-1 + References blocks |
| 2026-06-11 | **Ground-state headwater documented + cross-refs threaded** (the 3ⁿ index ↔ ground state ↔ network) | RWA (home) → HUF · Hˢ | `THE_GROUND_STATE.md`, `LINEAGE.md`, `HUF_RELATIONSHIP.json`, `CONFIDENCE_INDEX.md` |
| 2026-06-11 | **Pushes landed** — Hˢ CI #75 `148d0fb` · HUF #93 `24caaed` · RWA #4 `c97b83d` | RWA · HUF · Hˢ | (sites brought current) |

---

## 3 · How to keep it

1. **One change, three copies.** This file is in the shared set: when you log a cross-repo change, write the same entry in all three repos in the same change.
2. **Cross-repo only.** Single-repo work belongs in that repo's own journals (§1), not here — keep this log small and high-signal.
3. **Verify before push.** Run `verify_tri_repo_coherence.py` (development-mirror root) so the three copies stay byte-identical.
4. **Lose nothing.** This log is a backup; never trim history — append.

*Each repo carries the whole record. Anyone, anywhere in the system, can see what the others are doing — and no single repo holds the only copy.*
