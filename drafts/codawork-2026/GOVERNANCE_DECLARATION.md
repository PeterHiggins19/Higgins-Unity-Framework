# HUF Governance Declaration — The Dirty Laundry

**Status:** Living document — April 5, 2026
**Author:** Peter Higgins, with the HUF Collective (Claude, ChatGPT, Grok, Copilot, Gemini)
**Purpose:** Declare everything we know, everything we doubt, everything we do not know, and everything that might be wrong — so that others can learn from our exposure rather than be harmed by our concealment
**Principle:** Look both ways before crossing the street

---

## Why This Document Exists

Most frameworks are presented as accomplishments. Here is what we built. Here is what it does. Here is why it works.

This document is the opposite. Here is what we do not know. Here is what might be wrong. Here is what we doubt. Here is what scares us.

The reason is simple: concealment kills systems. Not malicious concealment — the kind where someone hides a flaw to sell a product — but the far more common kind where someone does not declare a limitation because they have not thought to look for it, or because the culture of their discipline does not reward the declaration of ignorance.

HUF was built by an engineer who said: "I am building a tool to protect myself from my own ignorance." This document is HUF protecting itself from its own ignorance. Everything declared here is a known unknown — a boundary we have found but not yet crossed. The unknown unknowns, by definition, are not here. They will appear. When they do, they get added to this document, not hidden from it.

*"So confused how did the world evolve to this point so blind?" — Peter Higgins, April 5, 2026*

---

## Part I: What HUF Is and Is Not

### What HUF is:
A monitoring and governance doctrine for compositional systems. An instrument that watches compositions change over time and tells the operator when something significant happened, what kind of event it was, and where in the structure the event occurred. A Q-inquisitor that measures coupling quality between subsystems.

### What HUF is not:

**HUF is not a mathematical framework.** CoDa is the mathematical framework. HUF uses CoDa's mathematics (Aitchison geometry, log-ratio transforms, SBP decomposition) but does not extend, modify, or replace them. HUF's contribution is governance — the doctrine of when to measure, what to measure, how to interpret the measurement, and when to act. If the mathematics is wrong, HUF is wrong.

**HUF is not a prediction engine.** HUF does not forecast what a composition will do next. HUF observes what a composition just did and classifies the event. Anyone who asks "what will the wetland look like in 10 years?" is asking the wrong instrument. HUF answers: "what just changed, and should you be concerned?"

**HUF is not peer-reviewed science.** As of April 2026, no HUF publication has undergone formal peer review. The Coimbra presentation will be the first exposure to an academic audience. Every claim in every HUF document should be read with this in mind: it is an engineer's proposal, tested by an AI collective, awaiting scientific scrutiny.

**HUF is not a finished instrument.** The 17-error catalogue (E-01 through E-17) documents the known failure modes. The 10-gap Ramsar complexity study documents the deployment limitations. The 3^n confidence index rates HUF itself at n=1 (opinion) on most claims. This is a prototype, not a product.

**HUF is not independent of its creator's biases.** Peter Higgins is a loudspeaker engineer. HUF thinks like a loudspeaker engineer. The vocabulary (phase, coherence, Q, coupling, resonance) comes from that domain. The instincts (always two measurements, open loop first, never trust automatic correction) come from that domain. These instincts may be exactly right for compositional monitoring, or they may be inappropriate metaphors that happen to produce plausible-looking results. The CoDa community is the correct body to determine which.

---

## Part II: The Known Unknowns

These are things we know we do not know. Each is a declared gap in HUF's foundation.

### KU-01: Is Ecological Data Genuinely Compositional?

HUF and CoDa both assume compositions — parts summing to a whole, where the relative proportions carry the signal. For energy data (megawatt-hours per fuel type as a share of total generation), this is defensible: the national grid is a constraint, and the proportions are physically meaningful.

For ecological data, the argument is weaker. Species abundances at a wetland site can be expressed as proportions — but should they be? The total abundance may carry ecological information (high total = productive ecosystem, low total = stressed ecosystem). By converting to proportions, we discard the total. CoDa says the total is uninformative because it depends on survey effort. Ecology says the total may be informative because it reflects carrying capacity. We do not know which is correct. GAP-01 in the Ramsar complexity study addresses this. It is unresolved.

### KU-02: Are the Three Diagnostics Genuinely Independent?

The 3^n confidence framework assumes TV, Aitchison distance, and coherence residual are independent diagnostics. They are mathematically distinct: TV operates on absolute differences, Aitchison operates on log-ratios, CR operates on SBP residuals. But they all operate on the same underlying data. If the data has a systematic bias (e.g., reporting error), all three diagnostics may be affected in correlated ways.

We have not conducted a formal independence analysis. The claim of independence is architectural (the three diagnostics use different mathematical operations) rather than empirical (we measured independence on real data). This is a known gap. It is at the foundation of the confidence framework.

### KU-03: Does the Coherence Residual Measure What We Think It Measures?

The coherence residual (THE_THIRD_DIAGNOSTIC.md) is defined as the difference between observed balance change and predicted balance change given parent-level changes. We interpret this as "coupling leakage across SBP branches." But this interpretation depends on the SBP being ecologically meaningful (GAP-04). If the SBP is arbitrary, the coherence residual is measuring artefacts of an arbitrary partition, not ecological coupling.

We have not validated the coherence residual on real ecological data. The concept is theoretically motivated and physically intuitive (it generalises Small's Q parameter), but it has not been empirically tested. Any claim about what the coherence residual detects is, at this stage, a hypothesis.

### KU-04: Is the Greenacre Bridge Honest?

HUF proposes to bridge the Egozcue-Greenacre debate by measuring coherence empirically rather than taking sides. This sounds diplomatic. But HUF's architecture (SBP decomposition, subcompositional coherence as a diagnostic) is architecturally aligned with Egozcue's position. The coherence residual is meaningful precisely because HUF assumes subcompositional coherence as the default — which is Egozcue's framework.

If Greenacre is correct that strict subcompositional coherence is too strong an assumption, HUF's coherence residual may be chronically elevated — measuring a mathematical property of the partition rather than an ecological property of the system. The "empirical test" may be biased by the instrument's architecture.

We have declared this tension. We have not resolved it. The honest position: HUF is an Egozcue-architecture instrument proposing to measure the Greenacre question. Whether the instrument can be fair to a question when it is built on one side of the answer is an open philosophical and mathematical question.

### KU-05: Can a Loudspeaker Engineer Contribute to Compositional Data Analysis?

This is the most fundamental known unknown and the one most likely to be answered at Coimbra.

The argument for: HUF was built on a genuine compositional system (constrained energy distribution across loudspeaker drivers). The paired-measurement doctrine, the coherence chain, the audit trail, the GOV/CLS fork — all emerge from real engineering problems that happen to be compositional. The fact that an engineer independently discovered properties of the simplex (isotropic ground state, constrained energy budget, dimensionality change as a diagnostic event) suggests the compositional structure is real, not projected.

The argument against: loudspeaker engineering is not ecology, energy, or macroeconomics. The intuitions that work for 4 carriers in a controlled laboratory may not transfer to 200 carriers in an uncontrolled ecosystem. The engineering vocabulary may alienate rather than illuminate. The entire HUF project may be an elaborate exercise in pattern matching — seeing simplices where there are none, because the engineer has a hammer (compositional geometry) and everything looks like a nail (a simplex).

We do not know which argument wins. The Coimbra presentation is the test.

### KU-06: Is the AI Collective a Strength or a Liability?

HUF was developed with extensive AI assistance. Six AI systems (Claude, ChatGPT, Grok, Copilot, Gemini, and various earlier interactions) have contributed to the framework's development, error detection, document creation, and adversarial testing.

The strength argument: the collective provides adversarial verification from multiple architectures, each with different training data, different biases, and different failure modes. Five independent AI reviewers converging on the same assessment is evidence (not proof) of robustness.

The liability argument: all six AI systems are language models with known limitations — hallucination, sycophancy, pattern-matching without understanding. If all six converge on the same assessment, it may be because they share a common bias (e.g., tendency to validate the user's framework) rather than because the framework is sound. The collective may be an echo chamber of correlated errors, not an adversarial verification network.

We have attempted to mitigate this by: using different AI architectures, requesting adversarial reviews (not just confirmations), filing every review with gold/rough diamonds/tailings structure, and inviting human expert review (Coimbra). But we have not independently audited the collective's convergence for correlated bias. This is a known gap.

### KU-07: Is the Error Catalogue Complete?

The 17-error catalogue (E-01 through E-17) plus 2 future directions (E-18, E-19) plus 6 scaling errors (ES-01 through ES-06) constitutes 25 identified failure modes. This is more than any comparable framework has published.

But completeness cannot be proven — only refuted. The catalogue was built by one engineer and five AI systems over a period of days. An ecologist, a statistician, a systems engineer, and a wetland manager would each likely identify failure modes that this group missed. The catalogue is the best we have. It is not the best that is possible.

### KU-08: Does the 3^n Framework Actually Work?

The Systems Confidence Index is a concept, not a theorem. The claim that n=3 constitutes "validation" and n=4 constitutes "certification" is intuitive but unproven. The exponential growth of 3^n is dramatic — perhaps unrealistically dramatic. Real-world diagnostics may show sub-exponential confidence growth due to residual dependencies.

The framework has not been tested on any real system. It has not been compared to existing confidence frameworks (Dempster-Shafer, Bayesian updating, reliability analysis). It has not been reviewed by a statistician or a metrologist.

It is a working hypothesis at n=1.

---

## Part III: The Doubts

These are not gaps in knowledge but uncertainties in judgment — things where reasonable people could disagree with the choices HUF has made.

### D-01: Is the White Flag Posture Correct?

HUF approaches CoDa with deliberate humility: "I'm not here to defend a framework. I'm here to learn from this room." This posture is strategically chosen to reduce adoption friction. But it may also reduce impact. If HUF's contributions are real, excessive humility may cause the audience to dismiss them as provisional rather than recognising them as substantive. There is a line between productive humility and self-undermining diffidence. We do not know if HUF is on the right side of it.

### D-02: Should HUF Integrate or Branch?

Peter's preference: integrate with CoDa and let the system grow naturally. The alternative: develop independently, using CoDa's mathematics but building HUF's own toolchain, publication stream, and community. Integration is slower but more robust — if accepted. Branching is faster but risks isolation and duplication of effort. The choice depends on the Coimbra response, which is not yet known.

### D-03: Is the Ramsar Application Premature?

HUF has not been validated on any ecological dataset. Proposing Ramsar deployment — the largest wetland monitoring system in the world — as a validation ground may be perceived as audacious rather than visionary. A more cautious path: validate on small ecological datasets first, then scale. The risk of the cautious path: HUF may never reach Ramsar, because small-scale validation lacks the impact to attract CoDa collaboration. The risk of the ambitious path: HUF may be dismissed as unrealistic by the CoDa audience.

### D-04: Is the Screwdriver-and-Math-Book Framing Patronising?

The framing: "I picked up the screwdriver first. The CoDa community picked up the math book first. Neither side was wrong. Neither side was complete." This is intended to convey mutual respect and complementarity. But it could be read as: an engineer telling mathematicians that their work is incomplete and needs his practical contribution. The audience's reaction will determine whether the framing lands as alliance or as condescension.

### D-05: Are We Overthinking This?

HUF now has: 25 error sources, 10 deployment gaps, 3 diagnostics, a confidence index, a scaling solution, a Q-inquisitor concept, a lineage document, a governance declaration, 14-slide presentation, poster layout, demo script, adversarial panel, room control strategy, engineered dataset, battle card, prep guide, trim list, conjecture, vocabulary tools, and this document.

For a framework that monitors compositions, this is a lot of meta-documentation. The CoDa community may want to see: clean mathematics, a working tool, and real data. Everything else may be noise. We do not know if the documentation corpus is a strength (thoroughness) or a weakness (over-engineering).

---

## Part IV: What We Believe Despite the Doubts

This section exists because honest declaration of ignorance, taken to its extreme, produces paralysis. Here is what we believe, after accounting for everything above.

1. **Compositional data is real.** The simplex constraint exists in physics (loudspeaker energy), economics (market shares), ecology (community composition), and any system where parts sum to a whole. CoDa's mathematics is the correct tool for these systems. This belief is well-supported by fifty years of Aitchison-school research.

2. **Governance is missing.** CoDa has the geometry. Nobody has the governance — the doctrine of when to measure, what to do when things change, and how to manage the instrument over time. This gap is real. It is not just HUF's opinion. Every practical deployment of CoDa methods in monitoring contexts faces this gap.

3. **The paired-measurement doctrine works.** Always two results. Always examine both. Disagreement is diagnostic. This principle has been validated in loudspeaker engineering for decades and transfers to compositional monitoring without modification. The dual-metric protocol (TV + Aitchison) is the simplest implementation.

4. **The alliance is worth building.** CoDa gives HUF mathematical rigour it cannot build alone. HUF gives CoDa a governance doctrine it has not built yet. Ramsar gives both a validation ground that neither can access alone. The three-way alliance is not guaranteed to succeed. But the alternative — each system operating in isolation — guarantees continued fragmentation.

5. **Transparency is non-negotiable.** This document exists because hiding limitations is more dangerous than declaring them. If HUF is wrong about something, finding out sooner is better than finding out later. If HUF is right about something, the declaration of doubt does not diminish the rightness — it makes the rightness more credible when it survives scrutiny.

---

## Part V: The Invitation

This document is an open declaration. Anyone who reads it is invited to:

- **Identify a gap we missed.** Add it. The gap register is not closed.
- **Resolve a known unknown.** If you have evidence that addresses KU-01 through KU-08, we want to see it. Agreement or refutation — both are valuable.
- **Challenge a belief.** If items 1-5 in Part IV are wrong, we need to know. The white flag is genuine.
- **Extend the error catalogue.** E-17 was found by Grok. E-18 and E-19 were speculative extensions. E-20 and beyond are waiting to be discovered by someone who sees what we missed.
- **Test the instrument on real data.** The strongest possible contribution: take HUF's diagnostics, apply them to real compositional data, and report what happens. The framework is at n=1. Every independent test moves it toward n=2.

*"Let us show all our dirty laundry so others can better learn by exposure, not concealment due to lack of declaration of the known first and the unknown that is always present at deeper or higher layers."*
— Peter Higgins

---

## Part VI: One Sentence

HUF declares 8 known unknowns, 5 unresolved doubts, and an incomplete error catalogue as a matter of principle — because a framework that conceals its limitations is more dangerous than one that has limitations, and because every gap declared is an invitation for someone who can see what we cannot.

---

**Cross-references:**
- RAMSAR_COMPLEXITY_GAP.md — the deployment-specific gap register (10 gaps)
- ENTANGLEMENT_ERROR_ANALYSIS.md — the error catalogue (E-01 through E-17, ES-01 through ES-06)
- CONFIDENCE_INDEX.md — the framework that rates HUF's own confidence level
- Q_INQUISITOR.md — the diagnostic philosophy
- THE_LINEAGE.md — the origin story that explains why HUF thinks like it does
- WHAT_HUF_IS.md — the definitive description including what HUF is not
