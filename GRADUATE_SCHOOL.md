# The graduate school — the deep onboarding curriculum (RWA · HUF · Hˢ)

*The graduate-level AI-refresh. The fast-refresh JSON in each repo makes you **operational** in minutes; this curriculum makes you **fluent** — not just what the system is, but why each part was necessary and how to uphold it. Identical in all three repos; part of the shared "map of the whole" — see [`DOCUMENT_DISTRIBUTION.md`](DOCUMENT_DISTRIBUTION.md). Weaves in [`HISTORY_THREAD.md`](HISTORY_THREAD.md). For any AI or human joining the system. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001; honest-broker; lose nothing; Peter is the sole commit/contact gate. Cross-repo paths resolve via [`CROSS_BRAIN.md`](CROSS_BRAIN.md).*

---

## How to use this

Read the courses in order. Each states its **necessity** (the need that forced it — the spine is `HISTORY_THREAD.md`), its **required reading** (canonical documents in their home repos; resolve cross-repo references with `CROSS_BRAIN.md`), and its **outcome** (what you must be able to *do*). Two tracks share this campus: the **fast track** (the fast-refresh JSON — operational) and the **deep track** (this curriculum — trustworthy). Graduate the deep track and you can be trusted to change the system, not just run it.

## The disposition (non-negotiable, taught in every course)

- **Honest-broker.** Report nulls straight. Express interest, never acquire it. The instrument flags; the expert decides — the loop stays open.
- **Claim tiers.** Tier 1 = measured/computed · Tier 2 = standard math soundly applied / practiced doctrine · Tier 3 = to earn. Label every claim.
- **Lose nothing.** The past is the strength and the future; archive, never delete.
- **Determinism.** Same input, same output, same receipt — held by the *process* as strictly as by the math.

## Prerequisites

- Compositional data analysis: the simplex, closure, CLR/ILR, Aitchison geometry, the barycentre. (HUF repo `science/reference/`; and the canon in the References block — Aitchison 1986; Egozcue et al. 2003; Pawlowsky-Glahn, Egozcue & Tolosana-Delgado 2015.)
- The arc, at a glance: `ARC_OF_DISCOVERY.md` (the what/why/when/how) and `HISTORY_THREAD.md` (the chain of necessity).

## Core courses

**Course 0 — Orientation: the three homes and the map of the whole.**
*Necessity:* you cannot navigate a three-repository system without its map. *Reading:* `DOCUMENT_DISTRIBUTION.md`, `CROSS_BRAIN.md`, `ARC_OF_DISCOVERY.md`, `HISTORY_THREAD.md`, `TRIPLE_JOURNAL.md`. *Outcome:* name which repo owns what (**run it → Hˢ · govern it → HUF · it began in sound → RWA**); resolve any cross-repo path; find any repo's journals; state the shared "map of the whole" set.

**Course 1 — The ground state and diffraction (the headwater).**
*Necessity:* every claim of certainty rests here — the structure was forced by physics, not chosen. *Reading:* RWA repo `THE_GROUND_STATE.md` and the DADC paper. *Outcome:* derive the **6.02 dB** apportionment (`G_dim = 6.02·dim/S`, `f_c = 115/dim`); explain why the isotropic ground state is the simplex **barycentre**; explain why time is read off the boundary rather than tacked on as an integral.

**Course 2 — The simplex and composition monitoring (MC-4).**
*Necessity:* the loudspeaker's conserved budget is the general object; monitoring composition is a category in its own right. *Reading:* HUF repo `science/coda-monitoring/` and the MC-4 material. *Outcome:* state the four monitoring categories and MC-4's falsifiable claim; explain shape vs magnitude (apportionment vs scale).

**Course 3 — EITT: the temporal face, and its place.**
*Necessity:* time is intrinsic to a composition; and a framework must size its own claims honestly. *Reading:* HUF repo `science/eitt/EITT_THE_PLACE_IT_HOLDS.md`. *Outcome:* state EITT's **divided influence** (engine-minor `eitt_bench_test`; concept- and community-major); explain the "Transformer" etymology (Smaart-v9 phase-wrap windings); give the honest qualifier (≈50% Aitchison geometry / ≈50% temporal autocorrelation; Tier 1 measurement, Tier 3 proof).

**Course 4 — The deterministic instrument (CN-TT v4).**
*Necessity:* a claim without a receipt is an opinion. *Reading:* Hˢ repo `HCI-CNTT/CNTT_COMPLETE_SPECIFICATION.md`; run `HCI-CNTT/run_cntt.py`. *Outcome:* run the engine on a composition; explain closure → CLR → tiling → diagnostics → hash; explain the cross-platform determinism contract and the frozen oracle.

**Course 5 — Confidence: the 3ⁿ index.**
*Necessity:* no prior standard existed for confidence in a large system of systems. *Reading:* HUF repo `science/methodology/CONFIDENCE_INDEX.md`. *Outcome:* state `C_n = 1 − (1−p)^(3ⁿ)`; explain n=1 opinion (3 checks) / n=2 agreement (9) / n=3 validation (27); explain why three — *the minimum to locate an error, not merely detect it.*

**Course 6 — Redundancy and the network.**
*Necessity:* safety-critical use needs backup you can verify, not trust. *Reading:* Hˢ repo `experiments/clifford_tiling_redundancy_2026-06/` and `experiments/network_redundancy_2026-06/`; `CROSS_BRAIN.md` §3. *Outcome:* explain the triple-channel 2-of-3 vote and its verdicts (`RC-CON-INF` / `RC-ISO-WRN` / `RC-HLT-ERR`); explain "any node checks any node" via determinism + content hash.

**Course 7 — Governance and doctrine.**
*Necessity:* pure math without governance is a tool with no guard. *Reading:* HUF repo `huf-gov/` (open-loop / safe-ops / kill-test / MC-4), `HUF-STD-001/002/003`, and the DVR-1.0 protocol. *Outcome:* apply the claim tiers; keep the loop open; run the kill test; state who holds the commit/contact gate (Peter, always).

**Course 8 — Operating discipline and coherence.**
*Necessity:* a distributed system that cannot prove its own coherence will drift. *Reading:* `DOCUMENT_DISTRIBUTION.md`, `verify_tri_repo_coherence.py` (development-mirror root), `TRIPLE_JOURNAL.md`, and DVR-1.0's failure modes. *Outcome:* keep the shared set byte-identical (change once, mirror to all three); run the verifier; log cross-repo changes in the triple journal; and know the one tool that lies about coherence — **the Linux sandbox mount serves stale/torn reads of just-edited files (FM-1); verify on Windows or with the harness Grep tool, never the sandbox.**

## Qualifying examination

You graduate when you can answer these from memory, with claim tiers:

1. Why is the isotropic ground state the barycentre, and why does that ground the framework's certainty? *(Course 1)*
2. Where does time enter, and why is it not tacked on? *(Courses 1, 3)*
3. What makes the instrument trustworthy without trusting its author? *(Course 4)*
4. Why three, not two? *(Course 5)*
5. How does any node check any other? *(Course 6)*
6. What is EITT's place, and why is its influence divided? *(Course 3)*
7. How do you keep three repositories coherent — and which tool must you never trust to tell you they are? *(Course 8)*
8. What are the three claim tiers, and where on the arc does each step sit? *(Courses 1–7)*
9. State the chain of necessity in one breath. *(`HISTORY_THREAD.md`)*

## Graduation

You are fluent — and trustworthy to change the system — when you can run the instrument, recite the chain of necessity from ground state to network, place any document in its correct home, keep the shared set byte-identical, and uphold the honest-broker discipline: flag but never decide, report nulls straight, label every claim by tier, and lose nothing.

*The fast-refresh makes you operational. The graduate school makes you trustworthy. The thread is the curriculum's spine; the discipline is its degree.*
