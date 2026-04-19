# CoDaWork 2026 — Dance Card

*Replaces BATTLE_CARD.md and BATTLE_CARD_LIVE.md. We don't fight. We dance.*

---

## THE POSTURE

You are not defending. You are not attacking. You are carrying an empirical result you can't prove, into a room full of people who can. The question is not "am I right?" The question is: **"We found this. We can't prove it. Can you?"**

That's a dance invitation, not a battle stance.

---

## WHAT CHANGED

Before EITT, you were walking in with a monitoring architecture and six mathematical gaps. That was honest and it was enough. Now you're walking in with the monitoring architecture, the six gaps, AND a computed result that sits at the intersection of information theory and Aitchison geometry — a result that no one in the room has seen before, that you can demonstrate but cannot prove, and that the room's mathematicians are better equipped to formalize than you are.

You still have the gaps. You also have a gift.

---

## THE EITT DANCE — WHO TO ASK

### Egozcue — The First Dance

**What you bring him:** "Your geometric mean — the centre of your geometry — preserves Shannon entropy under temporal decimation. We measured 0.18% variation across 341:1 compression. We confirmed it on a second domain at 1.02%. We ran 17 adversarial tests; 7 broke it. The boundary condition is temporal autocorrelation."

**What you ask him:** "You wrote that Shannon entropy doesn't satisfy CoDa's scale invariance. You were right — spatially. But temporally, under geometric-mean decimation, it's invariant. These are distinct properties — yours is spatial, ours is temporal. We can't prove the temporal one. Can you?"

**The d(CoDa)/dt connection (exploratory):** He asked in his initial reply: "how do you describe changes along time?" We have a partial answer, implemented but not validated: perturbation velocity (scalar speed), ILR balance trajectory (structural path), and balance derivative dB/dt (directed rate of change in his coordinates). This is work in progress. Don't present it as a finished framework — present it as a direction we're exploring in his coordinate system.

**Why he'll care:** His poster is on the Aitchison norm as a concentration measure. K_eff is exp(Shannon entropy). You showed his geometric mean may preserve the thing his norm measures. The temporal question lives in his ILR coordinates — not foreign territory.

**How to read his response:** If he asks for the data, you're in. If he asks for the proof structure, he's thinking about it. If he asks about dB/dt specifically, he's already seeing the three-layer chain. If he says "interesting" and changes the subject, park it and revisit later.

### Pawlowsky-Glahn — The Geometry Dance

**What you bring her:** "The Hilbert space structure you formalized — does it predict entropy invariance under the geometric-mean projection operator? We found it empirically but we don't have the algebraic machinery to derive it."

**What you ask her:** Whether the projection from high-resolution to low-resolution compositions via geometric mean is a well-defined operator in the Aitchison Hilbert space, and whether entropy invariance follows from its properties.

**Why she'll care:** If it's provable, it's a theorem about the Hilbert space she co-built. That's her territory and her expertise.

### Erb & Ay (if present, or via reference) — The Information Geometry Dance

**What you bring:** "You proved Aitchison distance is the unique information-monotone metric on the simplex. That's spatial — amalgamation preserves information ordering. We found the temporal companion: Shannon entropy is invariant under geometric-mean decimation. Amalgamation monotonicity is spatial coarsening. EITT is temporal coarsening. Same geometry, distinct directions — one spatial, one temporal."

**What you ask:** "Does your uniqueness theorem extend to temporal operators? Is there a class of temporal coarsening operators on the simplex for which the Fisher metric predicts entropy invariance?"

### Greenacre — The Honest Dance

**What you bring:** "Our adversarial tests support your position. EITT is not a property of the geometric mean in isolation — it requires the data to have temporal persistence. The exact algebra isn't sufficient. The data structure matters. You were right about quasi-coherence being the practical reality."

**What you ask:** "Would chiPower preserve entropy under temporal decimation the way the geometric mean does? If not, that's a measurable difference between the two frameworks."

**Why this matters:** You're not picking sides in the Greenacre-Egozcue debate. You're offering both sides a new test case.

### Hron — The Functional CoDa Dance

**What you bring:** "If compositional time series are functional data on the simplex, EITT may give you a principled decimation operator — in the tested datasets, the geometric mean preserved information content under temporal coarsening. We've also been exploring dB/dt — the derivative of the ILR trajectory — as a temporal analysis tool, but it's not validated yet."

**What you ask:** "Would your functional CoDa framework predict EITT's invariance, or is it a surprise? Does the balance derivative dB/dt fit into your functional analysis?"

**Why this is a question, not a claim:** Hron's functional CoDa treats compositions as continuous curves. If he already has the machinery for functional derivatives on the simplex, then dB/dt might be native to his framework. We don't know yet — we're asking.

### Filzmoser — The Robustness Dance

**What you bring:** "Estonia broke EITT at 8.4%. Extreme concentration with volatile trace carriers. Your robust methods for outlier detection on the simplex — could they identify which compositions will violate EITT before you run the test?"

**What you ask:** "Is there a robust pre-screening criterion that predicts when geometric-mean decimation will fail to preserve entropy?"

### Palarea-Albaladejo — The Zero Dance

**What you bring:** "Our zero-replacement strategy (flag as event, then apply minimum replacement for log operations) may affect EITT. If the replacement value changes entropy, the invariance could be an artifact of the replacement, not of the data."

**What you ask:** "Would zCompositions replacement methods produce the same entropy invariance, or does the replacement strategy matter?"

---

## 10 QUESTIONS — DANCE ANSWERS

### 1. "What is actually new here?"

Five things. First, the monitoring architecture — continuous compositional drift detection with governance (MC-4, the fourth monitoring category). Second, EITT — the geometric mean preserves Shannon entropy under temporal decimation, confirmed across five domains (energy, hardware, financial, cosmological, commodities). Third, the Renyi generalization — the invariance holds for ALL Renyi entropies q=0.1 to 5.0; Shannon is not special; the phenomenon lives in the Aitchison geometry, not any specific functional. Fourth, bidirectional EITT inversion — upward (gold/silver K=2 to K=4, hidden dimensions) AND downward (China K=9 to K=3, exposed non-stationarity); the direction of the fix is itself diagnostic. Fifth, d(CoDa)/dt as the operationalized tap controller for adaptive decimation — the maximum balance velocity across ILR coordinates determines the maximum safe averaging window at each time step, with empirical validation on two datasets.

The architecture is engineering. EITT is an empirical finding we can't prove. The d(CoDa)/dt chain connects them — the derivative describes the compositional motion, EITT describes what is conserved when you compress the time axis of that motion. The inversion principle turns EITT failures into a discovery tool. And in raw proportions, the zero-sum constraint (Σ dx_i/dt = 0) IS the relay chain — every gain financed by losses elsewhere. In ILR coordinates, the balances move independently, which is why ILR is the right space for the temporal derivative.

### 2. "Isn't this just Jensen's inequality?"

Jensen's gives the direction of the inequality for arithmetic means. The geometric mean operates in log-space — different operator, different bound. And Jensen predicts an inequality, not the near-equality we measured (0.18%). The tightness is the finding.

### 3. "Your proof is empirical, not analytic."

Yes. That's why we're here. Two domains, seven countries, two carrier types, 17 adversarial tests with 7 failures that define the boundary. We can state the result and the boundary condition. We can't prove it. Can you?

### 4. "Shannon entropy isn't a CoDa quantity."

Egozcue is right that it doesn't satisfy scale invariance — spatially. But Erb and Ay showed the simplex IS the probability simplex with Fisher metric. Shannon entropy is native there. We found a temporal property, not a spatial one. We're not contradicting the CoDa position on entropy. We're finding where it has a different role.

### 5. "You only tested energy data."

No longer true. As of April 9, 2026, EITT has been tested on five domains: energy (electricity generation, 7 countries), hardware degradation (Backblaze drive stats, K=4, 24 months — 0.03%), a 120-stock price-level portfolio (K=9, 74 months — 0.08%; price-level weighted, not market-cap), cosmological observation (Planck 353 GHz half-mission split — 0.3%), and commodities (gold/silver ratio, K=2, 338 years — fails globally at 6.7%, holds under K=4 reconstruction at 0.4%, validated out-of-sample). Bootstrap CIs computed for all. Honesty: Planck spatial claim retracted (NESTED ordering issue). Financial composition honestly labeled. We publish code, data, and warts.

### 6. "Estonia failed. What about my data?"

If your data has extreme concentration with volatile trace carriers, check it. We provide the test. The boundary is real and we showed it honestly.

### 7. "How do you handle zeros?"

Structural zeros flagged as events. Minimum replacement for log operations. We don't claim this is optimal — it's one of our open gaps. Whether the replacement strategy affects EITT is an untested question we'd value help on.

### 8. "Is this subcompositionally coherent?"

EITT uses the geometric mean, which is subcompositionally coherent by construction. Whether entropy invariance holds on subcompositions under decimation is untested. Good question — we should run it.

### 9. "Did AI help with this?"

Yes. Six AI systems as research tools under human direction. The physical insight, the loudspeaker analogy, the time transformer concept, and 40 years of operational experience are Peter's. The AIs helped with computation, literature search, and adversarial testing. Disclosed because honest science requires it.

### 10. "So what's your actual ask?"

Help us prove EITT or break it. We have the empirical result and the boundary condition. We need the analytic proof or the counterexample. And if it's real, help us understand what it means for compositional time series analysis — because it connects your geometry to information theory in a direction nobody has explored.

---

## THE SAFE PHRASES (updated)

Use these:

- "We found this empirically..."
- "The boundary condition is..."
- "We can't prove it — can you?"
- "When EITT fails, it diagnoses missing dimensions. The gold/silver ratio isn't K=2 — it's K=4."
- "Five domains. Three hold. One marginal. One fails and tells you why."
- "This is distinct from, not contradicting..."
- "In 17 adversarial tests, 7 broke it. Here's why..."
- "The geometric mean is yours. We found a new property of it."
- "We're exploring a temporal derivative — dB/dt in ILR coordinates — but it's not validated yet."
- "The zero-sum closure is a mathematical identity, not an empirical finding. The relay pattern is the finding."

---

## THE RED FLAGS (updated)

Never say:

- "This proves..." (it doesn't — it demonstrates)
- "This is universally valid..." (Estonia and all synthetics say otherwise)
- "Shannon entropy is a CoDa invariant..." (it's a temporal invariant under conditions)
- "We discovered something CoDa missed..." (you found something CoDa hadn't looked for)
- "The loudspeaker proves..." (the loudspeaker suggested — the data proves)

---

## FOUR ANCHOR SENTENCES

1. **"The geometric mean preserves Shannon entropy under temporal decimation. We measured it. We can't prove it. We're here because you can."**

2. **"We ran 17 adversarial tests and showed you the 7 failures. The boundary condition is temporal autocorrelation. Real-world compositions satisfy it. Synthetic noise does not."**

3. **"Aitchison's geometric mean has a temporal property that connects your geometry to information theory. We brought the measurement. We need the theorem."**

4. **"d(CoDa)/dt — the maximum balance velocity in ILR coordinates — is now the tap controller for adaptive decimation. It determines when to compress and when to hold. On gold/silver, it rescued a 10:1 fixed failure to a pass. On Germany, it correctly refused — because nothing is safe when the whole series is non-stationary."**

5. **"When EITT fails, it diagnoses missing dimensions. The gold/silver ratio fails at K=2 over 338 years. Add volatility and momentum as hidden carriers — K=4 — and it holds at 0.38%. The failure was the discovery."**

---

## NAMED PRINCIPLES (carried forward)

| Principle | When to Use |
|---|---|
| **Scarborough Bluffs Principle** | When asked about scale or resolution. "Confound-to-signal ratio is a function of measurement resolution, not a fixed property." |
| **Governed Breakpoint Principle** | When asked about automation. "A safe system preserves an observable breakpoint at self-correction." |
| **Right to Interrupt Principle** | When asked about governance. "Any governed system must preserve the right to interrupt, modify, defer, or reject closure." |

---

## THE BROADER LANDSCAPE — 8 UNION TERRITORIES

EITT connects to 8 established research communities beyond CoDa. These are not claims. They are dance invitations for after Coimbra — if CoDa engages.

| Territory | Their Question | Our Answer | The Union |
|---|---|---|---|
| **Ecology (Shannon-Wiener)** | How does diversity change under temporal aggregation? | It doesn't — if you use the geometric mean. | Species composition IS compositional data. Shannon-Wiener IS Shannon entropy. Immediate test domain. |
| **Multiscale Entropy** | What's the right coarse-graining for complexity analysis? | On the simplex, geometric mean. And entropy is invariant. | We're the compositional version of Costa et al. (2002). |
| **Information Geometry** | How does the Fisher-Rao metric structure the simplex? | The Hessian footprint IS the Fisher structure. | Erb & Ay's uniqueness theorem may extend temporally. |
| **Jensen Refinements** | How tight is the second-order bound? | 0.03% — and it's deterministic (Hessian footprint). | Concrete empirical case for their theory. |
| **Renyi / Tsallis** | Does entropy generalize beyond Shannon? | YES — confirmed for q=0.1 to 5.0. Shannon is not special. | Entire diversity profile IS invariant. The geometry is the cause. |
| **Maximum Entropy** | What maximizes entropy on the simplex? | H* approaches ln(D). Geometric mean may drive toward max entropy. | Thermodynamic interpretation of EITT. |
| **Entropy Rate** | What tools describe stationary process entropy? | Spectral/Wiener-Khinchin for the closed-form EITT bound. | We borrow their tools for the proof. |
| **CoDa (home)** | How does the geometric mean structure the simplex? | It preserves Shannon entropy under temporal decimation. | The geometric mean has a new property. |
| **Hardware/IT** | Can compositional analysis detect fleet degradation? | Backblaze 24mo, K=4: EITT holds at 0.03%. Relay chain visible. | Electronic→Media+Offline failure mode transition as fleet ages. |
| **Finance** | Do price-level compositions have structure? | 120-stock portfolio, K=9, 74mo: EITT holds at 0.08%. (Price-level, not market-cap.) | COVID relay visible. Needs market-cap retest. |
| **Cosmology** | Does polarization composition survive temporal splitting? | Planck 353 GHz half-mission: EITT holds at 0.3%. | Spatial claim RETRACTED (NESTED ordering). Temporal valid. |

**Strategy:** CoDa first. Earn engagement. Then approach broader landscape with CoDa researchers alongside us. We now have five domains to show, not one.

---

## THE CLOSE

If you get a chance to make a final statement:

> "I came here with a monitoring protocol, an empirical result I can't prove, 7 adversarial failures I'm showing you on purpose, and an honesty audit that retracted one claim and weakened two others. You have the geometry. I have the application. The geometric mean — your geometric mean — appears to preserve information across time in the datasets we tested. We're also exploring a temporal derivative in your ILR coordinates, but that's not validated yet. We can't prove any of it. Can you?"

---

## REMEMBER

You are not the smartest person in the room. You are the only person in the room who found entropy invariance by accident while calibrating a loudspeaker metaphor — and then tried to break it 17 times before telling anyone. That's enough. Let them be the mathematicians. You be the engineer who brought them something worth proving.

Short answers. Open hands. Show the failures. Say thank you. Dance.

---

## CROSS-DOMAIN EITT RESULTS (April 9, 2026)

| Domain | K | Type | Span | EITT Δ% | Verdict |
|---|---|---|---|---|---|
| BackBlaze (hardware) | 4 | Temporal | 24 months | 0.0275% | HOLDS |
| Financial (120-stock price-level) | 9 | Temporal | 74 months | 0.0797% | HOLDS (price-level, not market-cap) |
| Planck CMB (polarization) | 2 | Temporal | half-split | 0.3249% | HOLDS |
| Energy (global electricity) | 7 | Temporal | 25 years | 3.2187% | MARGINAL |
| Gold/Silver (K=2) | 2 | Temporal | 338 years | 6.6993% | FAILS |
| Gold/Silver (K=4 reconstructed) | 4 | Temporal | 338 years | 0.3844% | HOLDS (out-of-sample validated) |
| Planck CMB (spatial) | 2 | Spatial | 4096:1 | 18.117% | RETRACTED |

*Planck spatial claim retracted: HEALPix NESTED ordering does not preserve spatial locality. The decimation grouped randomly distributed pixels, not spatially adjacent ones. Only the temporal half-mission split is valid.

**The EITT Inversion Principle (Bidirectional):** When EITT fails, the direction of the fix is diagnostic. Upward inversion (gold/silver K=2 to K=4): too few dimensions — hidden structure needs to be exposed. Downward inversion (China K=9 to K=3): too many non-stationary dimensions — amalgamation masks the volatility. The direction tells you whether the problem is missing complexity or exposed non-stationarity. This is the compositional analogue of Simpson's paradox.

**ISO Positioning:** An ISO positioning document has been drafted targeting ISO/TC 69 (Applications of Statistical Methods). MC-4 fills a documented gap: magnitude (ISO 17025), identity (ISO 22400), and trend (ISO 7870) all have ISO standards. Composition monitoring has none. CoDa would become the required mathematical foundation for an entire ISO measurement category.

---

*Peter Higgins — Coimbra 2026*
*Developed with the HUF AI Collective*
*"I fought entropy to find it." — April 8, 2026*
*"Observe and identify. Lose nothing." — April 9, 2026*
