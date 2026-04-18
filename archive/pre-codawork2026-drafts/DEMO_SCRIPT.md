# CoDaWork 2026 — Live Demo Script

**Source:** Copilot collective review, April 4, 2026.
**Classification:** Rough diamond — conference preparation material.
**Duration:** 4-5 minutes
**Tone:** Calm, precise, instrument-first
**Goal:** Show the union's value without overselling

---

## 0. Opening Line (Before touching the tool)

"Let me show you the instrument. This is the CoDa Calibration Demonstrator — an open-loop, stateless monitoring tool that produces a full audit trail of compositional events."

*Pause. Let the room settle.*

---

## 1. Load the Dataset

*(Click "Load Sample" or load the prepared ecological dataset.)*

"This dataset is a multi-site ecological composition — five carriers, twenty years. Nothing exotic. The point is not the domain; the point is the motion."

---

## 2. Show the Ratio-State Panel (Ternary or ILR)

*(Select three carriers for ternary; or switch to ILR if needed.)*

"This is the ratio-state at a single point in time. CoDa gives us the geometry — the simplex, the balances, the ILR coordinates. HUF doesn't change any of that. What HUF adds is the ability to watch this point move."

*Move the year slider slowly.*

"As I slide through time, you can see the composition drift. This is the first part of the audit trail: the raw motion."

---

## 3. Switch to Velocity Panel

*(Click the velocity/TV/Aitchison panel.)*

"Now we look at the perturbation velocity — the year-to-year change in the ratio-state. This is where the union becomes visible."

*Point to the two curves.*

"The blue curve is Total Variation. The red curve is Aitchison distance. We do not fuse them. We compare them. When they disagree, that disagreement is a diagnostic signal."

*Pause. Let them absorb that.*

---

## 4. Highlight a Disagreement Event

*(Click on a point where TV and Aitchison diverge.)*

"Here is a disagreement event. CoDa alone cannot see this. HUF alone cannot interpret it. The union can. This tells us the composition changed in a way that is geometrically significant but not mass-significant — or vice versa. That's actionable information."

---

## 5. Show a Structural Shock

*(Click on a spike.)*

"This is a structural shock — a discontinuity in the motion. The analyzer detects it automatically using a median-scaled threshold. Every shock is logged in the audit trail with its metric signature."

*Pause.*

"This is the second part of the audit trail: the shocks."

---

## 6. Trigger a Zero Event

*(If your dataset has zeros; if not, simulate by selecting a year where a carrier drops sharply.)*

"Now watch what happens when a carrier approaches zero. In CoDa, zero is a mathematical problem. In HUF, zero is an event. The analyzer records the event before any transform is applied."

*Point to the event log.*

"This is the third part of the audit trail: zero events."

---

## 7. Show Dimensionality Change Detection

*(If your dataset includes a carrier entering/exiting; if not, describe it.)*

"Dimensionality change is error E-11 in the entanglement catalogue. CoDa transforms assume fixed dimension. Monitoring does not. The analyzer detects dimensionality changes and logs them."

*Point to the log.*

"This is the fourth part of the audit trail: dimensionality changes."

---

## 8. Summarize the Audit Trail

*(Scroll through the event log.)*

"So the audit trail consists of:

1. Drift events
2. Metric disagreements
3. Structural shocks
4. Zero events
5. Dimensionality changes

This is the value HUF brings to CoDa. Not new geometry. Not new transforms. Just the ability to watch compositions move — and to record every event that matters."

---

## 9. Closing Line

"This is the union: CoDa gives us the geometry. HUF gives us the audit trail. Together, they form a calibrated monitoring instrument."

*Stop. Let the silence work for you.*

---

## Audience Interaction Script (Questions YOU Ask THEM)

### Opening Prompt — Establishing the Frame

"Before I touch anything, let me ask you something: When a composition moves, what do you consider an event worth recording?"

*Let them answer. They will say: drift, shocks, zeros, outliers, dimensionality changes.*

"Excellent — those are exactly the five event types this instrument records."

### Interaction 1 — Drift

*(Show the ternary or ILR panel.)*

"When you see this point move year to year, what do you want to know? Magnitude? Direction? Stability?"

*Let them answer.*

"That's the perturbation velocity. CoDa gives us the geometry; HUF gives us the motion."

### Interaction 2 — Dual Metric Disagreement

*(Show TV vs Aitchison curves.)*

"If Total Variation and Aitchison distance disagree, what does that tell you? Is that noise, or is that information?"

*Let them debate.*

"In this instrument, disagreement is a diagnostic signal. It's not an error — it's a clue."

### Interaction 3 — Structural Shock

*(Click on a spike.)*

"Would you call this a shock? And if so, what threshold would you use?"

*Let them propose thresholds.*

"We use a median-scaled threshold. It's simple, robust, and domain-agnostic."

### Interaction 4 — Zero Event

*(Show a zero event.)*

"In CoDa, zero is a mathematical problem. In monitoring, is zero a problem — or an event?"

*Let them argue.*

"In this instrument, zero is an event. We detect it before any transform."

### Interaction 5 — Dimensionality Change

*(Show a carrier entering/exiting.)*

"If a carrier disappears or appears, should the instrument treat that as drift, or as a dimensionality change?"

*Let them answer.*

"This is error E-11 in the entanglement catalogue. The analyzer detects it and logs it."

### Closing Prompt

"Given these five event types — drift, disagreement, shocks, zeros, dimensionality — is there any event you would want a monitoring instrument to record that this one does not?"

*Let them think.*

"That's the audit trail. That's the value HUF brings to CoDa."
