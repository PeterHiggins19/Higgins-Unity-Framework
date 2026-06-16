# HUF‑GOV — the governance system (front door)

*This is the **governance layer** of the Higgins framework: the rules that make the science trustworthy and the instrument safe to deploy. It is written for the people who **actually need the governance** — institutional reviewers, safety/standards bodies, deploying engineers, and future researchers tracing how a deterministic measurement instrument should be governed — not for the casual user. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. The current instrument is Hˢ; on any conflict about current state, `Hs/HS_FAST_REFRESH.json` wins.*

---

## What governance is for here

A deterministic instrument that reads the internal balance of systems can be used well or badly. HUF‑GOV is the **layer between the tool and its effects** — it keeps the instrument an *observation* device (the expert decides), bounds where it is valid, names where it must fail, and makes every step auditable. The governance is as much the product as the engine: it is why the framework can be trusted from a notebook to mission‑critical use.

## The five things you came here for

| If you need to… | Read |
|---|---|
| **Apply the operating doctrine** (the core rules) | [`doctrine/HUF_GOV_OPERATING_DOCTRINE_2026-06.md`](doctrine/HUF_GOV_OPERATING_DOCTRINE_2026-06.md) + [`doctrine/DOCTRINE_INDEX.json`](doctrine/DOCTRINE_INDEX.json) |
| **Map it to recognised governance** (NASA‑style methods) | [`NASA_STYLE_GOVERNANCE.md`](NASA_STYLE_GOVERNANCE.md) + `.json` |
| **Understand the monitoring claim** (why composition is the 4th category) | [`RATIO_BLINDNESS_DOCTRINE.md`](RATIO_BLINDNESS_DOCTRINE.md) |
| **Know what stays private** (engagement/contacts) | [`CARRIER_FILTER_DOCTRINE.md`](CARRIER_FILTER_DOCTRINE.md) |
| **Know who gets the credit** (the data, not the tool) | [`THE_DATA_IS_THE_STAR.md`](THE_DATA_IS_THE_STAR.md) — the 49/51 doctrine |
| **Read the charter** (the standing terms) | [`HUF_GOVERNANCE_CHARTER.md`](HUF_GOVERNANCE_CHARTER.md) |

## The operating doctrine — four rules (DOCTRINE_INDEX → the doc)

1. **Open‑Loop / Skydiver** — the instrument reads; it never decides, acts, or recommends. *The expert decides; the loop stays open.*
2. **Safe Operations** — perceive before acting; *sometimes do nothing*; always have a "hold and report" safe state (the HAL lesson). A null is a finding, not a failure.
3. **Kill‑Test** — if it cannot be broken it is not science; the boundary where the instrument is **inapplicable** (non‑proportional data, degenerate carriers, broken closure) is documented with the rigour of the successes.
4. **Composition Monitoring (MC‑4)** — magnitude / identity / trend are standardised; **composition is the missing fourth category**. Ignoring it is *ratio blindness* — about a quarter of the picture lost.

These are cross‑walked to **NASA‑style governance** (lifecycle gates, technical authority, IV&V, FDIR, configuration management, fail‑safe, human authority, documented limits, observability, risk‑informed decisions) — honestly tiered, with flight‑readiness kept at Tier 3.

## The standards (locked)

`standards/` carries **HUF‑STD‑001** (AI Use Declaration), **HUF‑STD‑002** (Tensor Train I/O), **HUF‑STD‑003** (Publication Standards), and the linear‑algebra `FOUNDATIONS`. They are additive‑only and locked; the engine reads from them.

## The standing disciplines (the same across HUF and Hˢ)

- **Honest‑broker** — results reported straight, nulls included; *interest expressed, never acquired*.
- **Claim tiers** — Tier 1 (verified/computed) · Tier 2 (standard math soundly applied / practiced doctrine) · Tier 3 (to earn). Every claim carries one.
- **Carrier filter** — personal contacts and private business development stay off the public repo.
- **Double‑Verify & Staged‑Recovery (DVR‑1.0)** — lose nothing; verify before *and* after; recover from any AI/human mistake. Defined at `Hs/ai-refresh/VERIFICATION_PROTOCOL.json`.
- **Single gate** — Peter is the sole commit/contact authority. No AI commits or sends.

## How to actually use this (for a deploying reviewer)

1. Confirm your data is **compositional** (parts of a whole) — if not, the Kill‑Test says HUF/Hˢ does not apply; stop here honestly.
2. Run the instrument (in the Hˢ repo) and read the diagnostics + `SS‑CCC‑LLL` codes; **you assign meaning** (open‑loop).
3. Check the **safe‑state codes** — a NULL flag means "no separation; advance via a targeted signature," not "failure."
4. Record provenance — the content hash makes the read reproducible; that is your audit receipt.
5. Keep the loop open: the instrument informs; the human decides and is accountable.

## History preserved

`_legacy_2026-03/` holds the March‑2026 governance originals (LOOP/SAFE/KILL/MONITOR + GOV‑003/HAGF/TRANS) verbatim — the doctrine above is their modernized form. Nothing was discarded (lose nothing).

*The instrument reads. The expert decides. The hashes carry the receipts. The loop stays open.*
