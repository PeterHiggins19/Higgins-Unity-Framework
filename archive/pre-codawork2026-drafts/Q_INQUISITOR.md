# The Q-Inquisitor — HUF as Intersystem Quality Diagnostic

**Status:** Working concept — April 5, 2026
**Origin:** Peter Higgins, building on Richard H. Small's Q-parameter framework (1972)
**Style:** EITT — human story first, mathematics second

---

## 1. The Loudspeaker Engineer Already Solved This Problem

In 1972, Richard H. Small published a pair of papers that changed loudspeaker engineering forever. Before Small, loudspeaker design was empirical — build it, listen, adjust, repeat. Small introduced Q parameters: dimensionless ratios that describe how energy couples between systems.

- **Q_es** — how the electrical system couples to the mechanical system
- **Q_ms** — how the mechanical system dissipates energy on its own
- **Q_ts** — the total system quality, combining both

These are not measurements of what happens *inside* each system. They are measurements of what happens *between* systems. A loudspeaker with Q_ts = 0.707 has critically damped coupling — energy crosses the electrical-mechanical boundary cleanly, no ringing, no overshoot. A loudspeaker with Q_ts = 1.5 has underdamped coupling — energy sloshes back and forth across the boundary, producing audible resonance that wasn't in the signal.

The Q parameter does not care what the signal is. It does not care whether the music is jazz or speech or silence. It measures coupling quality. That is all it does. And that single measurement tells the engineer more about system health than any amount of frequency response measurement.

*Small's Q parameters are dimensionless ratios describing energy coupling between subsystems. Q_ts = Q_es × Q_ms / (Q_es + Q_ms). The critical insight: system health is diagnosed at the boundary, not within the subsystem. A frequency response measurement captures what the system does. A Q measurement captures how well the system is coupled.*

---

## 2. The Same Problem Appears Everywhere

Every complex system has internal subsystems that must exchange information, energy, or material across boundaries. The quality of that coupling determines system health more than the performance of any individual subsystem.

**In ecology:** Species populations (subsystems) exchange energy through food webs (boundaries). A wetland where the predator-prey coupling is tight shows different dynamics than one where the coupling is loose — even if the individual population counts look identical.

**In energy:** Generation technologies (subsystems) share a constrained national grid (boundary). A country where coal and renewables are tightly coupled through grid dispatch shows different transition dynamics than one where they operate independently — even if the total generation looks the same.

**In CoDa:** Compositional parts (subsystems) are constrained to the simplex (boundary). The subcompositional coherence question — whether a sub-composition behaves the same way inside a larger composition as it does alone — is a coupling question. It asks: does the boundary between this group of parts and the rest of the composition transmit information cleanly, or does it distort?

In every case, the diagnostic question is the same: **is the coupling clean, or is energy leaking across boundaries in ways the system did not intend?**

*The generalised Q-diagnostic: given a system S decomposed into subsystems {S_1, ..., S_k} with coupling boundaries {B_12, B_13, ...}, measure the ratio of intended energy transfer to total energy transfer at each boundary. When the ratio is 1, coupling is clean. When the ratio deviates from 1, energy is leaking — either damped (ratio < 1, energy lost at the boundary) or resonant (ratio > 1, energy amplified at the boundary).*

---

## 3. HUF Is a Q-Inquisitor

HUF does not measure what happens inside a compositional subsystem. HUF measures what happens at the boundaries between subsystems.

The coherence chain (1→2→4) is a hierarchy of coupling boundaries:

- **Level 1 (1→2):** The total composition splits into two groups. The boundary is a single SBP balance. The Q-question: does the energy exchange between these two groups behave as the partition predicts?
- **Level 2 (2→4):** Each group splits again. Two new boundaries. The Q-question at each: does the sub-partition behave consistently with the parent partition?
- **Level n:** Recursive decomposition. At each level, the Q-question is the same: is the coupling at this boundary clean?

The three diagnostics map directly to Q-parameter thinking:

| HUF Diagnostic | Q Analogue | What It Measures |
|---|---|---|
| TV distance | Signal magnitude | How much moved (amplitude of the event) |
| Aitchison distance | Frequency response | How the geometry changed (shape of the event) |
| Coherence residual | **Q parameter** | How much leaked across the boundary (coupling quality) |

TV and Aitchison measure the signal. The coherence residual measures the coupling. Just as Small's Q_ts tells the engineer more about system health than any frequency response curve, the coherence residual tells the analyst more about structural integrity than any compositional distance metric.

*HUF's Q-inquisitor function: at each SBP node, compute the coherence residual CR = observed balance change − predicted balance change given parent-level changes only. CR ≈ 0 means the partition is coherent (energy stays within the boundary). CR ≫ 0 means energy leaked from other branches (the partition is structurally unsound). The ratio CR/Aitchison distance is the compositional analogue of 1/Q — a dimensionless coupling diagnostic.*

---

## 4. Why Nobody Built the Translator

Small's Q parameters work because they sit at the boundary between electrical engineering and mechanical engineering and acoustical engineering. Before Small, each discipline measured its own subsystem and blamed the others when the loudspeaker didn't sound right. Small said: stop measuring inside. Measure at the joint. The joint tells you everything.

The same institutional separation exists today between CoDa, ecological monitoring, and systems governance:

- **CoDa** measures the geometry of compositions. Beautifully. But it measures *inside* the simplex.
- **Ecological monitoring** measures species counts and population trends. Accurately. But it measures *inside* each site.
- **Systems governance** manages policy and intervention. Carefully. But it governs *inside* each jurisdiction.

Nobody is measuring the coupling between these systems. Nobody is asking Small's question: what happens at the boundary?

HUF is the translator because it was built at a boundary. The Binaural Test Lab is where the electrical signal meets the mechanical driver meets the acoustic room meets the human ear. Four systems, three boundaries, and every single measurement Peter Higgins ever made was a coupling measurement. The entire HUF doctrine — paired results, audit trails, coherence gates, the GOV/CLS fork — was designed to diagnose coupling quality.

When HUF encountered CoDa, it did not encounter a foreign system. It encountered a system that had perfected the *interior* measurement (Aitchison geometry) but had not yet built the *boundary* measurement (coherence residual). HUF had the boundary measurement but not the interior geometry. The union is not a merger. It is a Q-parameter: a diagnostic that measures how well two systems couple.

*The institutional Q-parameter: HUF measures coupling quality between CoDa's mathematical framework and real-world deployment requirements. If the coupling is clean (HUF diagnostics confirm CoDa predictions), deployment proceeds. If the coupling is lossy (HUF diagnostics diverge from CoDa predictions), the loss points to a specific boundary failure — a specific error source in the E-01 through E-17 catalogue. The error catalogue IS the Q-map of the HUF-CoDa boundary.*

---

## 5. The Inquisitor's Questions

A Q-inquisitor asks exactly three questions at every boundary:

1. **Is the coupling clean?** (Coherence residual ≈ 0)
   → If yes: the partition is valid, the subsystems are behaving independently within their boundary. Proceed.

2. **If the coupling is dirty, where is the leak?** (Which SBP branch shows residual?)
   → The leak identifies the specific subsystem pair whose relationship has changed. This is diagnostic, not judgment.

3. **Is the leak growing?** (Temporal trend of coherence residual)
   → A stable leak is a known structural feature (quasi-coherence in Greenacre's terms). A growing leak is a structural failure in progress. This is the alarm.

These three questions are domain-independent. They work for loudspeakers, energy grids, wetland ecology, and any other system that can be decomposed into coupled subsystems on a simplex. HUF does not need to understand the domain. HUF needs to understand the coupling.

*The Q-inquisitor protocol: (1) Decompose the composition via SBP into subsystems. (2) At each SBP node, compute CR. (3) If CR > threshold, identify the leaking branch pair. (4) Track CR over time. (5) If dCR/dt > 0, raise the alarm. (6) The operator — the human — decides what the alarm means. HUF never decides. HUF inquires.*

---

## 6. From Thiele-Small to Aitchison-Small

This is not a metaphor. The mathematical structure is the same.

Thiele and Small decomposed the loudspeaker into coupled subsystems (electrical, mechanical, acoustic) and measured dimensionless ratios at the boundaries. Aitchison decomposed the composition into parts on a simplex and measured distances in log-ratio space. The missing piece — the piece HUF supplies — is the boundary diagnostic: a dimensionless ratio that measures coupling quality between compositional subsystems.

If the CoDa community accepts this framing, the instrument has a name that both engineers and mathematicians can read:

**The Aitchison-Small Diagnostic** — interior geometry from Aitchison, boundary coupling from Small, governance from the engineer who stood in the room where both were needed.

*Or, more precisely: Aitchison gives the metric. Small gives the diagnostic philosophy. HUF gives the governance. The union gives the instrument.*

---

## 7. One Sentence

HUF is a Q-inquisitor: it measures coupling quality at the boundaries between compositional subsystems, using the same diagnostic philosophy that Richard H. Small used to measure coupling quality between the electrical, mechanical, and acoustic subsystems of a loudspeaker — because the question "is the energy crossing this boundary cleanly?" is the same question regardless of what the energy is or what the boundary separates.

---

*"I picked up the screwdriver first. The CoDa community picked up the math book first. Small picked up both in 1972 and asked a question neither side had thought to ask: what happens at the joint?"*
— Peter Higgins

---

**Cross-references:**
- THE_LINEAGE.md — the BTL origin story and how the physics turned out to be compositional
- THE_THIRD_DIAGNOSTIC.md — the coherence residual as the formal Q-parameter for compositional systems
- SCALING_COHERENCE.md — the telescoping hierarchy of Q-measurements across deep SBP trees
- CONFIDENCE_INDEX.md — the 3^n framework for when a Q-measurement becomes validation
- WHAT_HUF_IS.md — the definitive instrument description
