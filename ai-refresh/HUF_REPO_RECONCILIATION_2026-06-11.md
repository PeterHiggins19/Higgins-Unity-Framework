# HUF repo reconciliation — live GitHub vs mirror (2026‑06‑11)

> **✅ SUPERSEDED 2026‑06‑11 — Peter chose the CLEAN START.** Rather than the careful pull‑and‑merge this report recommended, Peter **emptied the HUF repo** (CI "Validate Documents #92", `773f04d`, green) and is rebuilding the working tree coherently from the mirror — the same workflow as Hs. **Lose nothing still holds:** the prior state (the Git‑LFS migration, all 21+ commits, the `v0.1.0-codawork` tag, every document‑validation run) remains in the repository's git history, and a separate older HUF repo is preserved (private). So the "do not paste" warning below is **overridden by a conscious decision** — the loss it guarded against is averted because the old state lives in history, not because the divergence was merged. The rebuild target is now: make the mirror a **coherent lineage/support repo for Hˢ** (see `../README.md`, `../RELATIONSHIP_TO_Hs.md`, `../HUF_REPO_MAP.md`, `../AI_ASSIST.json`). The divergence analysis below is retained as the **record of why the clean start was the right call.** Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001.

---

### Original report (retained as record — its recommendation was superseded by the clean‑start decision above)

> **⚠️ DO NOT push the HUF mirror with the empty‑and‑repaste workflow.** Unlike the Hs repo (where the mirror is the source of truth), the **live HUF remote has evolved independently and is ahead of the mirror** — including a **Git LFS migration**. A naive paste‑over would undo the LFS migration, re‑bloat the repo, and risk losing 21 commits of remote work. This needs a careful **pull‑and‑merge**, not a paste. Verified per DVR‑1.0 (double‑verify: live `git ls-remote`/`git fetch` vs mirror).

---

## The three‑way state (verified)

| Where | State | Notes |
|---|---|---|
| **Live remote** (`github.com/PeterHiggins19/Higgins-Unity-Framework`, `master`) | HEAD **`58456fb`** (2026‑04‑24) + tag **`v0.1.0-codawork`** (`a25c4a0`) | **21 commits ahead** of the mirror's last local commit; **Git LFS migration applied** |
| **Mirror `.git`** (`Current-Repo/HUF`) | local `master` at **`498dece`** (2026‑04‑18, "EXP‑04/05 PLL‑EITT chain") | **stale by 21 commits** — never pulled the April 18→24 remote work |
| **Mirror working tree** | `498dece` base + **255 uncommitted edits** (months of work incl. this session's `huf-gov/` doctrine + NASA‑style governance) | full‑size binaries, **no `.gitattributes`/LFS config** |

`498dece` **is an ancestor of** `58456fb` (the remote is strictly ahead; the mirror's local history has nothing the remote lacks). The divergence is in the **working tree** vs the **remote's 21 commits**.

## What the remote did that the mirror never received (the risk)

`git diff 498dece..origin/master` = **898 files changed (+510,339 / −104,647)**. The dominant change is a **Git LFS migration** (2026‑04‑18→24):
- New `.gitattributes`: `*.docx *.pdf *.xlsx *.pptx *.png *.ipynb *.zip filter=lfs diff=lfs merge=lfs -text`.
- **~370 large binaries converted to LFS pointers** (130–131 bytes each; e.g. `science/quantum/Book0_HUF_QIT_Primer.docx` is now a pointer `oid sha256:9eb9fe… size 22671`, while the mirror still holds the full 22,671‑byte file).
- Plus 21 content commits: "Hs updates", "Hs corrections", "coda revisions", "coda refinements", "Science Discovered", "HUF EITT Clean", "EITT updates", "Higgins Decomposition", interleaved with merge commits.

**If the mirror were pasted over the originals/remote:** the full binaries (no LFS) would overwrite the LFS pointers → the LFS migration is undone, the repo re‑bloats, LFS server objects orphan, and the 21 remote commits' content is at risk. That is the loss the double‑verify just prevented.

## Safe reconciliation path (lose nothing)

Do this on your machine with git (GitHub Desktop or CLI), **not** a paste:

1. **Back up the mirror's working tree first** (copy `Current-Repo/HUF` aside) — lose nothing.
2. **Adopt LFS in the mirror:** `git lfs install`; bring in the remote `.gitattributes` (or `git checkout origin/master -- .gitattributes`).
3. **Pull/merge the remote:** `git pull origin master` (or `git merge origin/master`). The remote's LFS migration + 21 commits land; resolve conflicts.
4. **Re‑apply your real new content on top** — the working‑tree edits that matter (this session's `huf-gov/doctrine/`, `NASA_STYLE_GOVERNANCE.*`, `_legacy_2026-03/` move, `RATIO_BLINDNESS_DOCTRINE.md`, `AI_ASSIST.json`) — staged so binaries go through LFS via the new `.gitattributes`.
5. **Verify before/after:** `git lfs ls-files` shows binaries tracked; `git status` clean; then push. Confirm `git ls-remote origin master` matches your new HEAD (DVR §6 closure).

*The mirror's months of working‑tree edits are real and worth keeping — but they must be applied on top of the remote's current LFS state, not in place of it.*

## The older private repo (noted, preserved)

Per "lose nothing": an **older‑version HUF repo exists, now private and unused but present** (Peter). It is intentionally retained as historical archive; not in scope for this reconciliation; do not delete.

## What I did here (non‑destructive)

- `git ls-remote origin` + `git fetch --no-tags origin master` — read‑only; updated only the mirror's `origin/master` remote‑tracking ref (the remote commits are now available locally for the merge). **Local `master` and the working tree were NOT changed** (no pull, no checkout).
- Confirmed the LFS migration and quantified the divergence. Wrote this report.

*Verified against the web; the mirror is behind on history and diverged in the working tree; reconcile, don't paste. The instrument reads; the expert decides; lose nothing.*
