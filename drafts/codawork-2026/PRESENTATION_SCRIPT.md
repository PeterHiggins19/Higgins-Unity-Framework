# CoDaWork 2026 — Presentation Script (10–12 minutes)

**Source:** Copilot collective review, April 4, 2026.
**Classification:** Rough diamond — conference preparation material.

---

## Slide 1 — Title

**The CoDa–HUF Union: A Calibration Study of a Combined Monitoring Instrument**

"Good afternoon. My name is Peter Higgins. Today I'm presenting a calibration study — not a new framework, not a replacement for CoDa, but a disciplined examination of what happens when we combine two instruments that were built for different purposes but converge on the same architecture."

---

## Slide 2 — The Lineage (Where This Instrument Came From)

"Before I show the union, let me explain where this instrument came from. It was not designed for CoDa. It was designed for loudspeakers.

A loudspeaker cabinet radiates acoustic energy. At any given frequency, that energy distributes itself across directions — forward, backward, up, down. The total is fixed. It is a constrained energy budget. The directional distribution is a composition. It lives on a simplex.

At low frequencies, the radiation is omnidirectional — the isotropic ground state. Equal energy in all directions. The barycenter of the simplex. As frequency rises and wavelength meets the cabinet dimensions, the pattern breaks isotropy. Energy concentrates. Carriers become unequal. The composition moves.

I built an instrument to watch it move — because I was building a tool to protect myself from my own ignorance. Two measurements, always. Both examined, always. Disagreement is a diagnostic. Departure from isotropy is an event. Lose nothing. Discard nothing.

Every property that defines compositional data — the closure constraint, the ratio-scale information, the zero-event significance — was already present in the physics. The simplex was already there. I just didn't know its name."

---

## Slide 3 — Why We're Here

"CoDa perfected the geometry of compositions at rest. HUF was built to monitor compositions in motion. When we combine them, the union inherits all error sources from both — plus new ones that exist in neither alone. This presentation is the result of a two-day entanglement session that mapped those errors and produced the first calibration study of a combined CoDa monitoring instrument."

---

## Slide 4 — The Trigger

"This began with a simple question: What source of error does CoDa bring into a monitoring instrument, and what breaks at the joint? That question triggered a full audit of transforms, metrics, stored energy, dimensionality, and governance. The result was a 17-error catalogue."

---

## Slide 5 — The Discovery

"We discovered that MEWMA-CoDa and HUF are building the same instrument from opposite ends. MEWMA brings smoothing, stored energy, and ARL optimization. HUF brings stateless monitoring, open-loop doctrine, and coherence chain governance. The union is the complete instrument."

---

## Slide 6 — What HUF Is

"HUF is a multichannel coherent detector. HUF-GOV is a phase discriminator — stateless, open loop, no stored energy. HUF-CLS is the PLL — closed loop, with governance as the loop filter. Only HUF-GOV belongs in scientific monitoring. This distinction resolved the PLL objection raised by Jack, and it is now formalized in WHAT_HUF_IS.md."

---

## Slide 7 — The 17 Error Sources

"The union inherits 12 initial errors, 4 from literature cross-reference, and 1 new concern discovered during review. Each error has a detection test and a governance action. This is the first failure-mode catalogue for a CoDa monitoring instrument."

---

## Slide 8 — Zero Tension (E-03)

"In CoDa, zero is a mathematical problem. In HUF, zero is an event. The union protocol is simple: detect the event first, then apply the transform. This resolves the tension without hiding the signal."

---

## Slide 9 — Dual Metric Diagnostic

"The analyzer uses Total Variation and Aitchison distance. We do not fuse them. We compare them. Disagreement is a diagnostic signal — not an error. This is not an ad hoc design choice — HUF was built from the beginning on a paired-measurement doctrine: always two results, always examine both, lose nothing. When CoDa brought Aitchison distance to the union, the architecture already had a slot for it. The principle predates the union and was validated by it."

---

## Slide 10 — Dimensionality-Aware Time Series

"CoDa transforms assume fixed dimensionality. Monitoring does not. E-11 documents the consequences of dimensionality change. The analyzer detects this and records it in the audit trail."

---

## Slide 11 — The Analyzer (Demonstrator)

"This is the CoDa Calibration Demonstrator. It is open loop, stateless, and observational. It produces a full audit trail of events: drift events, metric disagreements, structural shocks, zero events, dimensionality changes. This is the value HUF brings to CoDa."

---

## Slide 12 — The Union Thesis

"CoDa perfected the geometry of compositions at rest. HUF discovered what happens when compositions move. The union is the instrument that watches them move and signals when to care."

---

## Slide 13 — Deployment Path

"The path is simple: Coimbra, then validation, then Ramsar pilot, then standardization. We begin with calibration, not claims."

---

## Slide 14 — Closing

"This is not a new framework. This is a calibration study. The union is the instrument. The audit trail is the value. Thank you."

---

## White Flag Opening (Peter's chosen posture)

"I'm not here to defend a framework. I'm here to learn from this room. I brought a calibration study, not a claim. And I'm waving a white flag because I'd rather understand the objections than win an argument."

---

## Two-Minute Elevator Pitch

"CoDa has mastered the geometry of compositions at rest. But the world we measure — ecosystems, energy systems, supply chains — is not at rest. It moves. And when compositions move, we need a monitoring instrument that can detect events, track drift, identify shocks, and maintain coherence over time.

HUF was built for that purpose. It is a multichannel coherent detector — stateless, open loop, and designed to produce an audit trail of events. When we combine HUF with CoDa, we get something neither can produce alone: a calibrated, dual-metric, dimensionality-aware monitoring instrument.

The April entanglement session produced a 17-error catalogue — the first failure-mode study of a CoDa monitoring instrument. This is not a new framework. This is a calibration study. The union is the instrument. The audit trail is the value."
