# NASA‑Style Governance — methods & principles, mapped to Hs practice (2026‑06‑11)

*How Hˢ / HUF‑GOV adopts NASA‑style governance **methods and principles** as a discipline — by mapping what the framework **already does** to the corresponding NASA practice, and naming honestly where it is aspiration rather than achievement. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Companion: [`doctrine/HUF_GOV_OPERATING_DOCTRINE_2026-06.md`](doctrine/HUF_GOV_OPERATING_DOCTRINE_2026-06.md) · machine form [`NASA_STYLE_GOVERNANCE.json`](NASA_STYLE_GOVERNANCE.json).*

> **Honest scoping (read first).** Hˢ is **not** NASA‑certified and makes no such claim. This document adopts NASA‑*style* governance — the principles and methods NASA uses to make high‑consequence systems trustworthy — as a self‑imposed discipline, because Hˢ aims to be an instrument trustworthy *from a notebook to mission‑critical and flight systems*. Each mapping below carries a claim tier: **Tier 1** = already implemented and verified · **Tier 2** = practiced as discipline/doctrine · **Tier 3** = aspiration, to earn. The flight/space‑readiness framing is **Tier 3** throughout.

---

## Why NASA‑style, and why it fits

NASA governance exists to answer one question under high consequence: *how do we know this will do what we say, and fail safely when it doesn't?* Hˢ was built around the same question in a different register — a deterministic, hash‑chained instrument whose whole value is that you can **audit exactly what it saw and reproduce it.** That makes the NASA toolkit a natural fit: determinism gives verification teeth, the frozen oracle gives configuration management, the open‑loop doctrine gives human command authority, and the kill‑test gives documented operating limits. The point is not to cosplay an agency; it is to borrow the disciplines that make instruments trustworthy.

---

## The cross‑walk — NASA principle → Hs practice

| NASA principle / method | What it means | How Hˢ already does it | Tier |
|---|---|---|---|
| **Project lifecycle + Key Decision Points** (NPR 7120.5: Pre‑Phase‑A → F, gate reviews SRR/PDR/CDR/FRR) | Work advances only through explicit gates, each a go/no‑go decision | The geosensing **HGS‑000…008 Pre‑Phase‑A spec suite**; the **CCTT 7‑phase protocol** with two explicit operator gates (adapter‑select, self‑verify); the **push protocol** with a green‑CI gate before each release | T2 |
| **Technical Authority** (Programmatic, Engineering, Safety & Mission Assurance — independent of the project manager) | Decisions carry named, separable authorities; no single role overrides safety | **Peter = sole commit/contact authority** (programmatic gate); the **frozen oracle** (CNT v3.2.0 / CNQ v2.0.0) = engineering authority that the live engine must reproduce bit‑for‑bit; the **honest‑broker + claim‑tier discipline** = mission‑assurance authority | T2 |
| **Independent Verification & Validation (IV&V)** | A party independent of the builder confirms the system meets spec | **Frozen‑oracle parity** (live CN‑TT v4 must match the archived oracle on real Backblaze data); the **engine self‑test** (BIST); the **HUF AI Collective** cross‑checks (Claude/ChatGPT/Grok/Gemini/Copilot); the **open cross‑platform reproduction challenge** (independent `cnq_content_sha256`) | T1 / T2 |
| **FDIR — Fault Detection, Isolation, Recovery** | The system detects faults, isolates the bad component, and recovers to a safe state | Hˢ's **internal‑vs‑external shock classifier** (tells a real compositional change from a sensor fault and isolates the channel); `SELF_DIAGNOSTICS_AND_LIFECYCLE.md`; the **E‑21 carrier guard** (detect → exclude → calibration code) | T1 |
| **Configuration Management** (every artefact versioned, traceable, reproducible) | You can say exactly what was built and reproduce it | **Hash‑chained provenance** (`cntt_content_sha256` at every step), the **version triple**, the **frozen oracle**, and the **push/CHANGELOG/PUSHES_INDEX chain** — bit‑for‑bit CM | T1 |
| **Fail‑safe & safe‑state** (abort to a known safe state; no‑op is valid) | When in doubt, hold safely rather than act wrongly | The **Safe Operations Doctrine** (hold‑and‑report); the automated **NULL flag** `DX‑NUL‑DIS` (no separation → don't manufacture one); the **disjoint‑atlas error** `L3‑DSJ‑ERR` (refuse to guess a broken reconstruction) | T1 / T2 |
| **Human command authority** (automation informs; the human commands; no autonomous actuation without operator volition) | The crew is never removed from the loop | The **Open‑Loop / Skydiver Doctrine** — the engine emits diagnostics and codes, **never an action**; the operator decides | T2 |
| **Verification & documented operating limits** (off‑nominal testing; know where it breaks) | The envelope is mapped, not assumed | The **Kill‑Test Doctrine** — confirmed kills (non‑proportional data, degenerate carriers/E‑21, broken closure) documented with the rigour of the successes | T1 / T2 |
| **Observability before control** (you must be able to see the state before you act on it) | Monitoring precedes any control decision | **Composition Monitoring (MC‑4)** — the 4th monitoring category (Magnitude/Identity/Trend/**Composition**); ratio blindness named and closed | T2 |
| **Risk‑informed decision making** (decisions weigh and record risk; nulls and limits are data) | Risk is surfaced, not hidden | Claim tiers on every assertion; **nulls reported straight** (Crohn p=0.78; GLDS‑1 global null); the **Investigation Catalog** keeps even falsified branches on record | T1 / T2 |
| **Flight readiness / Earth‑space twin** (a system is certified for the environment it will fly in) | Prove it works in the real operating environment | `SPACE_READINESS_AND_CHALLENGE.md` — a deterministic Earth/space twin study: because the engine adds **zero variance**, any Earth‑vs‑orbit difference is the environment, not the tool | **T3 (aspiration)** |

---

## The lifecycle, in Hs terms

NASA advances a project through gated phases; Hˢ already has the shape of this, and naming it makes the gates explicit:

- **Pre‑Phase‑A (concept):** the geosensing/flight spec suite (HGS‑000…008), feasibility studies, the candidate/frontier roadmap. *Gate:* does the concept survive the kill‑test?
- **Phase A/B (definition / preliminary design):** a domain study built on real data with a named domain expert (geology‑wehner, microbiome). *Gate:* CCTT phase‑2 adapter‑select — is the carrier meaning correct?
- **Phase C/D (build / verify):** engine run + self‑test + frozen‑oracle parity + figures + writeup. *Gate:* CCTT phase‑6 self‑verify, and a green CI before any push.
- **Phase E (operate):** the deterministic instrument in use; FDIR running; the operator deciding. *Gate:* the open loop — every reading is the operator's to act on.
- **Phase F (closeout):** journal, hash‑chain the record, archive. The receipts persist.

---

## What this is not (the honest line)

This is a **governance discipline**, not a certification. Hˢ has not been through a NASA review board, holds no flight heritage, and the space‑readiness work is a deterministic *argument* and an open *challenge*, not a flown result. What is real today is the discipline itself: determinism that makes verification meaningful, a frozen oracle that makes configuration management exact, FDIR that is implemented and tested, and a human‑authority doctrine that keeps the loop open. Adopting NASA‑style methods is how Hˢ earns the right, over time, to be trusted in higher‑consequence settings — one verified gate at a time.

*The instrument reads. The expert decides. The hashes carry the receipts. The loop stays open.*
