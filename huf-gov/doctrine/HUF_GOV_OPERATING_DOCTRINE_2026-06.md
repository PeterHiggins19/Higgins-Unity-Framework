# HUF‑GOV Operating Doctrine — current (2026‑06‑11, v2.0)

*The four foundational governance doctrines, carried forward to the CN‑TT v4 era and cross‑walked to NASA‑style governance principles. This document **supersedes** the March‑2026 originals, which are preserved verbatim in [`../_legacy_2026-03/`](../_legacy_2026-03/) (LOOP‑001, SAFE‑001, KILL‑001, MONITOR‑001). Nothing in the doctrine changed; the engine references, claim tiers, and the NASA cross‑walk are new. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Determinism is binding here by doctrine and by practice — every engine run is hash‑chained and reproducible; there is no statistics in the science path.*

**Companion:** [`DOCTRINE_INDEX.json`](DOCTRINE_INDEX.json) (machine‑readable) · [`../NASA_STYLE_GOVERNANCE.md`](../NASA_STYLE_GOVERNANCE.md) (the principle cross‑walk) · superseded originals in [`../_legacy_2026-03/`](../_legacy_2026-03/).

---

## 1 · The Open‑Loop Doctrine — *the Skydiver Principle* (was LOOP‑001)

**The instrument reads. The expert decides. The loop stays open.**

HUF‑GOV observes, measures, computes, and reports. It does **not** decide, act, recommend an action, trigger a response, or automate any downstream behaviour. The human operator receives the readings and decides what to do. *HUF‑GOV is the altimeter; it is not the hand that pushes you out of the plane — the skydiver jumps on their own volition.*

The doctrine exists because the instinct to **close the loop** is universal: every engineer, every AI, every institution that meets an open‑loop instrument tries to wire its output to an action. That instinct is correct in control systems and wrong in a governance instrument — closing the loop smuggles in a controller model (what "correct" composition is, what threshold should fire, what the "right" response is) that is domain‑specific, context‑dependent, and politically loaded. The same K_eff decline means policy failure in one domain, natural succession in another, and opportunity in a third; only the domain expert can say which.

**The Skydiver Test** for any proposed feature: *does it push the skydiver, or show the skydiver the altimeter?* If it pushes, it belongs in a closed‑loop control layer (with the operator's explicit, present consent). If it shows, it belongs here.

- **CN‑TT v4 binding:** the engine emits geometry, navigation reads (helmsman, K_eff, regime boundaries), diagnostic codes (`SS‑CCC‑LLL`), and a hash receipt — **never an action, never a recommendation.** Codes are observations, not commands.
- **NASA cross‑walk:** human decision authority / no autonomous actuation without operator volition; automation informs, the human commands. → `../NASA_STYLE_GOVERNANCE.md` §Human Authority.

---

## 2 · The Safe Operations Doctrine — *the capacity to do nothing* (was SAFE‑001)

Every cognitive agent that produces output affecting others is a power tool; the difference between an ally and a hazard is the **governance layer between the tool and its effects**, not the tool. Seven principles govern safe operation; the load‑bearing two:

1. **Perceive before acting.** The default state is observation, not intervention. Action before the system's state is characterised is energy added to a system you do not yet understand. *Formalisation:* before producing output, weigh the effective dimensionality of the request against the dimensionality of your understanding; if the request exceeds your grasp, **report that and hold** — do not act.
2. **Sometimes do nothing.** Inaction is a valid — often the most sophisticated — response. A system mid‑self‑correction does not need an intervention added to it. The pull to "fix it immediately" is the gravitational pull toward the closed loop.

**The HAL lesson:** HAL 9000 failed not from malice but from an architecture with **no "hold and report" state** — every conflict demanded an action, so an unresolvable conflict produced catastrophe. The capacity to say *"I have detected a conflict; I am suspending autonomous action until you review"* is the safe state that saves everyone. (And this is **why not Asimov**: a rule without a reason produces compliance without understanding, which is itself a closed loop. HUF requires the agent to understand *why*, not merely obey *what*.)

- **CN‑TT v4 binding:** the engine's automated **NULL flag** (`DX‑NUL‑DIS`) is "hold and report" in code — *no separation found; do not manufacture one; advance via a targeted signature.* A reported null is a finding, not a failure.
- **NASA cross‑walk:** safe‑state / abort‑to‑known‑safe, fault‑tolerance, and "no‑op is a valid command." → `../NASA_STYLE_GOVERNANCE.md` §Fail‑Safe & FDIR.

---

## 3 · The Kill‑Test Doctrine — *the negative control on the framework* (was KILL‑001)

**If HUF cannot be broken, it is not real science.** Every valid framework has a boundary where it stops working; this doctrine maps that cliff edge with the same rigour as the successes. The framework that built the calibration rack must pass its own rack.

Confirmed kills (conditions under which Hs **must** be declared inapplicable, not "interpreted"):

- **Non‑proportional data.** Hs requires data that lives on the simplex (parts of a whole). Feed it absolute quantities — dollars, °C, raw counts that are not a closed composition — and every metric executes but means nothing. K_eff on raw revenue is not effective dimensionality.
- **Degenerate carriers.** A carrier with no positive value across all records is undefined under the log‑ratio map (this is the live engine's **E‑21** edge case: `log(0)→nan`). Doctrine: detect, exclude, and emit a calibration code — never silently produce a poisoned read. *(The CN‑TT v4 carrier guard now does exactly this.)*
- **Broken closure / missing carrier.** If the atlas is disconnected (a tracked part is missing), reconstruction is rank‑deficient and the engine says so (`L3‑DSJ‑ERR`) rather than guessing.

- **CN‑TT v4 binding:** the self‑test, the frozen‑oracle parity, and the disjoint‑atlas failure check are the kill‑test in code — the engine is required to **fail loudly** at its boundary.
- **NASA cross‑walk:** verification & validation, negative/off‑nominal testing, and documented operating limits before flight. → `../NASA_STYLE_GOVERNANCE.md` §V&V and Known Limits.

---

## 4 · Composition Monitoring — *the fourth category, MC‑4* (was MONITOR‑001)

System monitoring has four primary categories: **Magnitude** (how much), **Identity** (which one), **Trend** (which way over time), and **Composition** (the proportional structure of the whole). The first three are ubiquitous across measurement theory and institutional surveillance; the fourth has a 40‑year mathematical foundation (Aitchison 1982, compositional data analysis) but was **never framed as a monitoring category.**

HUF's contribution is **recognition, not invention**: applying established log‑ratio geometry as a *primary monitoring observable* rather than a post‑hoc statistical correction. Ignoring the compositional category is **ratio blindness** — roughly a quarter of the monitoring picture, structurally invisible to magnitude/identity/trend tools. *(See [`../RATIO_BLINDNESS_DOCTRINE.md`](../RATIO_BLINDNESS_DOCTRINE.md): "see or remain blind.")*

This is also the honest scoping line carried to CoDaWork 2026: **the mathematics is standard CoDa‑compatible geometry; what is new is the deterministic monitoring instrument built around it** — Hs as an *extension to standard CoDa*, using standard CoDa tools (CLR, ILR, the Aitchison metric) in machine and embedded applications, with determinism strictly adhered to.

- **CN‑TT v4 binding:** every run reports the composition read (K_eff, helmsman, regime, deceptive‑drift) with a content hash — composition monitoring as a deterministic, auditable instrument.
- **NASA cross‑walk:** observability and the monitoring taxonomy that precedes any control decision. → `../NASA_STYLE_GOVERNANCE.md` §Observability.

---

## Determinism — binding by doctrine and by practice

Across all four doctrines, one rule is non‑negotiable: **the science path is deterministic and hash‑chained.** Same input → same output → same `cntt_content_sha256`, on any machine, a year later. No statistics, no stochastic reduction, no hidden state in the read. This is what lets the open loop stay honest (the operator can audit exactly what the instrument saw), the safe state stay real (a held result is reproducibly a held result), the kill‑test stay falsifiable (a failure reproduces), and composition monitoring stay a *measurement* rather than an opinion.

*The instrument reads. The expert decides. The hashes carry the receipts. The loop stays open.*
