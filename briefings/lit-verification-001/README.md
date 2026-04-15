# Literature Verification 001 — Distributed Novelty Check

**Issued:** 2026-04-15
**Coordinator:** Peter Higgins
**Deadline:** 2026-04-22 (one week)
**Purpose:** Verify novelty of the five-object cluster before any paper or abstract claims novelty formally.

## The claim under test

A five-object mathematical cluster is proposed as the organizing structure behind the Higgins Unity Framework's EITT work:

1. **EITT** — Entropy-Invariant Time Transformer; Shannon entropy near-invariant under geometric-mean block decimation of compositions
2. **Tutte's theorem** — perfect matching existence in graphs, mapped to sequential binary partition (SBP) decomposition existence in CoDa
3. **Hanani–Tutte theorem** — planarity via even-crossing parity, mapped to parity cancellation in the Taylor expansion of Shannon entropy
4. **Penrose tilings** — aperiodic long-range order with local matching rules, mapped to self-similar inflation under EITT decimation
5. **KPZ universality** — interface-growth scaling exponents, conjectured applicable to compositional drift interfaces

The unifying principle: **shape/magnitude decomposition** — all five objects are about local compatibility rules producing global structure with mismatch as the diagnostic.

## Branch assignments

| AI | Branch | Focus | File |
|---|---|---|---|
| Claude | Combinatorial graph theory | Tutte + Hanani–Tutte × CoDa | `HUF_CLAUDE_LIT_VERIFY_001.json` |
| ChatGPT | CoDa canon review | Pawlowsky-Glahn / Egozcue / Tolosana-Delgado 2020–2025 publications + textbook + proceedings | `HUF_CHATGPT_LIT_VERIFY_001.json` |
| Grok | Penrose / aperiodic | Penrose tilings, aperiodic order, quasi-crystals, self-similar time series × CoDa | `HUF_GROK_LIT_VERIFY_001.json` |
| Gemini | KPZ / statistical physics | KPZ universality, interface growth, random matrix theory, Wasserstein flows × CoDa | `HUF_GEMINI_LIT_VERIFY_001.json` |
| Copilot | arXiv crossover | arXiv preprints, cross-listings, cited-by extensions | `HUF_COPILOT_LIT_VERIFY_001.json` |

## How to use these briefings

1. Paste each JSON into the respective AI's chat interface as a single message.
2. Each briefing is self-contained — the AI will have enough context to execute without seeing the repo.
3. Each AI returns a JSON results file (format specified inside each briefing).
4. Collate the five returned files.
5. If any branch returns a positive hit, the novelty claim for that pairing must be revised.

## What counts as a positive hit

A paper (or preprint) that **explicitly** makes one of the claimed connections:

- Tutte's theorem applied to SBP / balance-basis existence → positive for the Tutte-CoDa pairing
- Hanani–Tutte parity argument applied to entropy expansions or compositional averaging → positive for Hanani–Tutte-CoDa pairing
- Penrose / aperiodic-order / quasi-crystal framework applied to compositional time series → positive for Penrose-CoDa pairing
- KPZ universality class, scaling exponents, or interface-growth theory applied to compositional drift or simplex-valued processes → positive for KPZ-CoDa pairing
- Shape/magnitude decomposition as an organizing principle for compositional analysis → positive for the overall cluster framing

## What counts as a near-miss

A paper in adjacent territory that does not complete the connection. Examples:

- Self-similarity of compositional time series without the aperiodic-order / Penrose framework
- Wasserstein gradient flows on the simplex in pure-math papers without CoDa applications
- Graph-theoretic structure of balance trees without matching-theorem existence conditions
- Random-matrix treatments of compositional covariance without universality-class framing

Near-misses are valuable references for the discussion section of any future paper. They do not falsify novelty.

## Collation template

Once all five return, build a consolidated table:

| Pairing | Claude | ChatGPT | Grok | Gemini | Copilot | Consolidated verdict |
|---|---|---|---|---|---|---|
| EITT itself | - | - | - | - | - | - |
| Tutte × CoDa | - | - | - | - | - | - |
| Hanani–Tutte × CoDa | - | - | - | - | - | - |
| Penrose × CoDa | - | - | - | - | - | - |
| KPZ × CoDa | - | - | - | - | - | - |
| Shape/magnitude frame | - | - | - | - | - | - |

Consolidated verdicts:
- **Novel** — no positive hits across any branch
- **Partially novel** — specific pairings have prior work; revise claims for those
- **Not novel** — the organizing principle or multiple pairings exist in the literature; major revision needed

## What to do with the results

If verdict is "Novel":

- The cluster is publishable as a structural-observations paper
- Abstract v4's EITT segue can stand as written
- Candidate venues: CoDa journals, information geometry venues, statistical physics ↔ statistics crossover journals

If "Partially novel":

- Identify the specific pairings with prior art
- Revise the framework papers (`EITT_WHY_IT_WORKS.md`, the future structural-observations paper) to cite prior work
- The remaining novel pairings still support a restricted-scope paper
- Abstract v4 segue may need light revision

If "Not novel":

- The framework's specific contributions (second-order Hessian bound, empirical validation on four domains, shape/magnitude decomposition framing) may still be valuable
- The claim structure shifts from "new cluster identified" to "applied known cluster to new domain"
- Paper venue shifts from structural-observations to applied-methodology
- Abstract v4 segue should be reframed more modestly

## Timing and follow-up

- Briefings go out: 2026-04-15
- Results due back: 2026-04-22
- Collation and verdict: 2026-04-24
- Abstract amendment decision (based on verdict): before 2026-05-01 (CoDaWork deadline)
- Final Book of Abstracts: 2026-05-15

If any branch returns a positive hit earlier, escalate immediately rather than waiting for the deadline.

## Files in this folder

- `README.md` (this file)
- `HUF_CLAUDE_LIT_VERIFY_001.json`
- `HUF_CHATGPT_LIT_VERIFY_001.json`
- `HUF_GROK_LIT_VERIFY_001.json`
- `HUF_GEMINI_LIT_VERIFY_001.json`
- `HUF_COPILOT_LIT_VERIFY_001.json`

Return files (to be filled in as AIs complete their branches):

- `CLAUDE_LIT_VERIFY_001_RESULTS.json` (pending)
- `CHATGPT_LIT_VERIFY_001_RESULTS.json` (pending)
- `GROK_LIT_VERIFY_001_RESULTS.json` (pending)
- `GEMINI_LIT_VERIFY_001_RESULTS.json` (pending)
- `COPILOT_LIT_VERIFY_001_RESULTS.json` (pending)
