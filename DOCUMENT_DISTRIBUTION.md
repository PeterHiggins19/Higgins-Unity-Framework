# Document distribution — the general rule for the three-repository system

*One system, three repositories. This file is **identical in all three** — each carries the map of the whole. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker; lose nothing; Peter is the sole commit/contact gate. Companion machine-readable registry: [`DOCUMENT_DISTRIBUTION.json`](DOCUMENT_DISTRIBUTION.json). Resolver for cross-repo links: [`CROSS_BRAIN.md`](CROSS_BRAIN.md).*

---

## 1 · The three homes

Every document has a natural home, decided by what it *is*:

| Repo | Role — one line | What it holds |
|---|---|---|
| **Hˢ** — higgins-decomposition | **pure math · the general instrument** | the deterministic engine (CN-TT v4), specs, run path, diagnostics, experiments, the conference face — anything you *run* |
| **HUF** — Higgins-Unity-Framework | **governance** | doctrine, standards, charters, claim-tiers, the development history and lineage, the confidence model — the rules that make the math trustworthy |
| **RWA** — Rogue-Wave-Audio | **everything organic sound** | the Binaural Test Lab, loudspeaker design, DADC/DADI/ADAC diffraction, the ground-state origin — where the instrument was built, with a screwdriver |

A useful mnemonic for *which repo*: **run it → Hˢ · govern it → HUF · it began in sound → RWA.**

## 2 · The general rule — single source of truth

**Every document lives in exactly one home repo. The other repos reference it; they never fork it.** Cross-repo references resolve through `CROSS_BRAIN.md` (so a path like `../HUF/<x>` is interpretable standalone on GitHub). When a repo needs to point at content owned elsewhere, it carries a short **pointer stub**, not a copy — e.g. Hˢ's `huf-gov/doctrine/README.md` points to the canonical doctrine in HUF.

Routing, by kind of document:

| If the document is about… | …its home is | Examples |
|---|---|---|
| the engine, an algorithm, a spec, a run, a diagnostic, an experiment | **Hˢ** | `HCI-CNTT/`, `CNTT_COMPLETE_SPECIFICATION.md`, `experiments/`, `run_cntt.py` |
| doctrine, a standard, a charter, claim-tiers, lineage narrative, admin governance, the confidence ladder | **HUF** | `huf-gov/`, `HUF-STD-001/002/003`, `science/methodology/CONFIDENCE_INDEX.md`, `briefings/THE_LINEAGE.md`, `science/eitt/EITT_THE_PLACE_IT_HOLDS.md` |
| acoustics, the BTL, diffraction, a loudspeaker paper, the ground state, lab identity | **RWA** | `THE_GROUND_STATE.md`, the DADC paper, the ODL papers, `RWA-001.json`, `LINEAGE.md` |

If a document could plausibly live in two homes, pick the home that matches its **primary verb** (run / govern / sound), give it one canonical home, and reference it from the others.

## 3 · The shared set — "the map of the whole"

A small, explicit set of files is the deliberate exception to single-source: these are kept **byte-identical in all three repos**, because each repo must be able to orient a reader to the entire system on its own. The shared set is:

| File | What it is |
|---|---|
| `CROSS_BRAIN.md` | the two-brain map (governance + math), the cross-repo resolver, the network capability |
| `ARC_OF_DISCOVERY.md` + `arc_of_discovery.svg` | the nine-step arc, source to network (the executive summary + its flowchart) |
| `DOCUMENT_DISTRIBUTION.md` + `DOCUMENT_DISTRIBUTION.json` | this policy and its machine-readable registry |
| `TRIPLE_JOURNAL.md` + `TRIPLE_JOURNAL.json` | the system-wide journal index + cross-repo change log (a distributed, triplicate backup of cross-repo changes) |
| `HISTORY_THREAD.md` | the common development+necessity thread — the through-line of why each step was forced |
| `GRADUATE_SCHOOL.md` | the graduate-level onboarding curriculum (the deep ai-refresh; weaves in the history thread) |
| `.gitattributes` | the unified file-handling policy (no LFS; text raw + LF-normalized) |
| README **Level-1 block** (the shared system message) and the **References & Acknowledgments** block | the identical opening and the maintained credits, carried inside each repo's own README |

Nothing else is duplicated. If you find the same substantive document in two repos and it is **not** on this list, that is drift — consolidate it to one home and leave a pointer.

## 4 · How to distribute and keep coherent

1. **Author once, in the home repo.** New content goes to its home (§2). Other repos get a pointer if they need one.
2. **For the shared set (§3): change once, mirror to all three in the same change.** Never let the copies diverge between pushes.
3. **Verify parity before every push.** Run the verifier (`verify_tri_repo_coherence.py` at the development-mirror root) — it md5-compares every shared file and the README shared blocks across the three sibling folders and reports any drift. Confirm parity with this or with the harness `Grep` tool — **not** the Linux sandbox, whose mount can serve torn reads of just-edited files.
4. **Lose nothing.** Superseded material is archived, never deleted; the past is the strength.
5. **The gate is human.** No AI commits or contacts on its own; Peter approves every push.

## 5 · Why three

Three homes, three pointers, one shared map — the same triangulation the instrument runs on. One repo is a point; two is a line; three is a plane, the minimum that lets any reader (human or machine) confirm both their **position** (which home they are in) and the system's **status** (the shared map they all carry). Coherence is not a clean-up step here; it is the architecture.

*Run it → Hˢ. Govern it → HUF. It began in sound → RWA. The map of the whole rides in all three.*
