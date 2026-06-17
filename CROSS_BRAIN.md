# The cross‑brain — governance (HUF) + pure math (Hˢ), and the network they enable

*2026‑06‑11. One system, two repositories, designed to reference and **check** each other (with a third repo, RWA, upstream as the **headwater/origin** — see the resolver and headwater note in §2). This file is identical in all three repos — each carries the map of the whole — and it is also the **canonical resolver** for cross‑repo references, so they stay valid whether you read them in the development mirror (where the two repos are sibling folders) or standalone on GitHub. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001.*

---

## 1 · The two halves

| | **Hˢ — higgins‑decomposition** | **HUF — Higgins‑Unity‑Framework** |
|---|---|---|
| Brain | **pure math** — the deterministic instrument (CN‑TT v4: closure → CLR → tiling → diagnostics → hash) | **governance** — the doctrine, standards, lineage, and development history that make the math trustworthy and safe to deploy |
| Holds | the live engine, the frozen oracle, the run path, the conference face | open‑loop/safe‑ops/kill‑test/MC‑4 doctrine, HUF‑STD‑001/002/003, the arc of discovery |
| Checks the other | runs the governance's rules in code (codes, FDIR, DVR) and stress‑tests them on real data | bounds the math (where it applies, where it must fail), keeps the loop open, certifies the claims |
| Source of truth | `HS_FAST_REFRESH.json` (**wins on any conflict about current state**) | `ai-refresh/HUF_FAST_REFRESH.json` (HUF history) |

Neither half is dependable alone. Pure math without governance is a tool with no guard; governance without a deterministic instrument is a rulebook with nothing to measure. Together they are a **cross‑brain**: the math gives the governance teeth (a hash receipt for every claim), and the governance gives the math a conscience (the open loop, the safe state, the honest null). RWA is the **headwater** upstream of both — where the instrument was built, in sound.

## 2 · Cross‑reference resolver (so references never break)

In the development mirror, Hˢ and HUF are sibling folders under `Current-Repo/`, so a relative path like `../HUF/...` resolves. **On GitHub they are separate repositories.** Resolve any cross‑repo reference this way:

| A reference of the form… | …means | Standalone URL |
|---|---|---|
| `../HUF/<path>` or `../../HUF/<path>` | the **HUF** repo at `<path>` | `https://github.com/PeterHiggins19/Higgins-Unity-Framework` |
| `../higgins-decomposition/<path>` or `../Hs/<path>` | the **Hˢ** repo at `<path>` | `https://github.com/PeterHiggins19/higgins-decomposition` |
| `../Rogue-Wave-Audio/<path>` or `../RWA/<path>` | the **RWA** origin repo at `<path>` | `https://github.com/PeterHiggins19/Rogue-Wave-Audio` |

So every relative cross‑repo path in any repo is **interpretable** even when the repos are read standalone — translate the prefix to the URL above. *(Single‑source rule: shared governance like the operating doctrine is canonical in HUF; Hˢ carries a pointer stub at `huf-gov/doctrine/README.md`, not a duplicate. See `DOCUMENT_DISTRIBUTION.md` for the full routing rule.)* *(Headwater: the origin of the whole arc is the RWA repo — `../Rogue-Wave-Audio/THE_GROUND_STATE.md` traces the one formula — 6.02 dB apportioned on the simplex, time forced by the boundary not tacked on — forward through the 3ⁿ confidence index to this network.)*

## 3 · The network it enables — any node checks any node

The cross‑brain's deepest property is that the instrument designed to read compositions can **read the composition of its own readers.** Because every Hˢ read is *deterministic and hash‑receipted*, the same composition yields the same content hash on any node, anywhere. From that one fact:

- **Determinism is the cross‑verify primitive.** A node verifies a peer's read by recomputing it and comparing the receipt (hash). No trust required — reproduction is the proof. *(This is the open cross‑platform reproduction challenge, made operational.)*
- **Any node checks any other, no matter what it processes.** A gas mask reading {O₂, CO₂, N₂, agent} and a geo probe reading {SiO₂, Al₂O₃, …} produce hash‑receipted reads in the *same form*. A node with spare capacity can recompute a peer's input and confirm its receipt — **the geo probe on the wall is a backup channel for the gas mask in the infirmary**, because both are just compositions to the instrument.
- **The triple‑channel, generalized to a network.** Three methods in one box become N nodes in a network. A majority vote emits the same FDIR verdicts — `RC‑CON‑INF` (consensus), `RC‑ISO‑WRN` (isolate the minority node), `RC‑HLT‑ERR` (no majority → halt‑and‑report, the safe state). Detect with two, isolate with three, scale to N.

**Verified (Tier 1):** `experiments/network_redundancy_2026-06/` — node B reproduces node A's receipt bit‑for‑bit; a geo‑probe node verifies a gas‑mask node by recomputing its input; a 5‑node network isolates a faulty node by majority. The single‑box version is `experiments/clifford_tiling_redundancy_2026-06/` (tiling + Clifford + matrix, with the 2‑of‑3 vote).

## 4 · Why the future can depend on it

The discipline is determinism — *by doctrine and by practice* — and that is what propagates: **the determinism in everything the framework does becomes determinism in what everyone who uses it does.** Same input, same output, same receipt, on a notebook or a sensor mesh or a flight system. The governance keeps the loop open (the instrument flags; the expert decides), the FDIR vote grades confidence at every scale, and the cross‑brain keeps the rules and the math honest against each other.

- **Tier 1 (now):** the cross‑verification primitive — determinism + identical hashes — is implemented and verified (self‑test + the two experiments).
- **Tier 3 (the vision):** a deployed network of Hˢ‑instrumented devices lending each other redundancy across domains. Real, grounded in the primitive — but to earn, not yet claimed.

*All possible because it is all just the way the system was designed to handle compositions — including itself. The instrument reads. The expert decides. The hashes carry the receipts. The loop stays open.*
