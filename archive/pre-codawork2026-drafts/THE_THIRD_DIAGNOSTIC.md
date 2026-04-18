# The Third Diagnostic

**TV measures what moved. Aitchison measures how the geometry changed. The coherence residual measures whether the instrument itself is still telling the truth.**

---

## The Two Diagnostics That Exist

HUF was built on a paired-measurement doctrine: always two results, always examine both, disagreement is information.

**Total Variation** answers: how much mass moved between carriers? It operates on raw proportions. It is sensitive to dominant carriers. It was HUF's first metric, born in the loudspeaker lab, predating CoDa.

**Aitchison distance** answers: how did the composition change geometrically on the simplex? It operates on log-ratios. It is sensitive to trace carriers. It is the CoDa-correct metric, adopted after Aitchison's geometry gave HUF the mathematical language for what it had been measuring.

Where they agree: the event is robust. Where they disagree: the disagreement classifies the event — dominant carrier restructuring versus trace carrier perturbation.

Two diagnostics. Two views. The doctrine works.

But both diagnostics answer the same kind of question: **what happened to the composition?** Neither asks a different question — one that the Ramsar deployment demands and the CoDa community needs answered.

---

## The Question Neither Metric Asks

The scaling solution — telescoping coherence — decomposes a deep hierarchy into a tree of binary balances via the Sequential Binary Partition. Each balance is a 1→2 problem. Each balance is assumed to be a valid subcomposition — meaning the ratio captured by that balance is independent of what happens in other branches of the tree.

That assumption is subcompositional coherence. Egozcue requires it. The ILR transform depends on it. The telescope's entire architecture depends on it.

Greenacre says: strict coherence is an idealization. In real systems — especially ecological systems — coherence is approximate. Species interact across group boundaries. Trophic levels are coupled. A change in one branch of the SBP tree can leak into another branch, not because the composition changed, but because the ecological coupling between branches changed.

In a loudspeaker, strict coherence holds because the crossover network enforces isolation between frequency bands. The physics guarantees it. The SBP is clean.

In a wetland with 500 species across 5 trophic levels, coherence is not guaranteed. It is not engineered. It is ecological — which means it is entangled, variable, and potentially the most important signal in the system.

Neither TV nor Aitchison measures this. TV measures share movement within the composition. Aitchison measures geometric displacement within the composition. Neither measures **whether the partition is still valid** — whether the structural relationships that define the SBP are holding or breaking.

That is the missing diagnostic.

---

## The Coherence Residual

When a balance at one SBP node changes, that change is potentially a mixture of two signals:

**Signal** — a real event within that branch. Species within the group changed their ratios because of something happening to them directly. Habitat loss. Predation pressure. Disease. Climate. A real ecological event, local to that branch.

**Coupling artifact** — leakage from events in other branches. Species in this group didn't change because of anything happening to them. They changed because species in a *different* group shifted, and the ecological coupling between groups transmitted the perturbation across the partition boundary. The balance moved, but not because of a within-branch event.

In a strictly coherent system, the coupling artifact is zero. Every balance change is pure signal. The SBP decomposition is exact. The telescope works perfectly.

In Greenacre's quasi-coherent world, the coupling artifact is nonzero and variable. Balance changes are mixtures of signal and leakage. The telescope still works — but it needs a way to separate the two.

The **coherence residual** at a given SBP node measures: how much of this balance change is attributable to events outside this branch?

*Formally: for a binary balance b_i at SBP node i, the coherence residual CR_i is the partial derivative of b_i with respect to perturbations in balances outside branch i. In a strictly coherent system, CR_i = 0 for all i. In a quasi-coherent system, CR_i measures the cross-branch coupling at node i at time t.*

---

## Three Diagnostics

The instrument now carries three diagnostics at every SBP node, at every time step:

**TV distance** — how much mass moved between the two groups at this node?

**Aitchison distance** — how did the log-ratio geometry change at this node?

**Coherence residual** — how much of this change leaked from other branches?

The first two diagnose the composition. The third diagnoses the partition.

The first two tell the ecologist what happened to the species. The third tells the ecologist whether the species groups are still behaving as groups — or whether the ecological structure itself is changing.

### Agreement patterns

**All three small:** Nothing happened. The composition is stable and the partition is clean. The telescope stays wide.

**TV and Aitchison large, coherence residual small:** A real event, local to this branch. The partition held. The telescope zooms in. Standard audit trail entry.

**TV and Aitchison large, coherence residual large:** An event occurred, but part of it leaked from another branch. The telescope zooms in AND flags the coupling. The audit trail records both the event and the structural coupling that contaminated it. The ecologist knows to look across branches, not just within.

**TV and Aitchison small, coherence residual large:** The composition at this node barely moved — but the coupling from other branches changed. The ecological relationships are restructuring even though the species counts look stable. This is a **structural event** — the most important kind for long-term monitoring, and the kind that classical analysis completely misses.

That fourth pattern is the one Ramsar needs most. A wetland where the species counts are stable but the ecological coupling between trophic levels is quietly restructuring is a wetland that *looks* healthy and *is* failing. The composition hasn't moved yet. The structure underneath is already broken. The coherence residual catches it. TV and Aitchison cannot.

---

## What This Gives the CoDa Community

The Egozcue-Greenacre debate on subcompositional coherence has been theoretical. Both positions are defensible mathematically. Neither has been tested empirically at scale because no instrument existed to measure coherence as a continuous variable across time.

The coherence residual changes that. It makes coherence measurable, not assumed.

At every SBP node, at every time step, across 2,500 Ramsar wetlands, the coherence residual produces a number. Aggregate those numbers and the CoDa community gets what it has never had: an empirical map of where strict coherence holds and where it doesn't, in real ecological systems, at global scale, over decades.

If strict coherence holds across most wetlands most of the time — the ILR decomposition is validated for ecological monitoring. Egozcue's framework stands. The telescope works as designed.

If quasi-coherence is the norm — the coherence residual shows exactly where and when it breaks. The CoDa community gets a roadmap for extending the theory to coupled systems. Greenacre's position is vindicated with data, not argument.

If coherence varies by trophic level, by latitude, by wetland type, by season — the CoDa community gets the most detailed empirical study of subcompositional coherence ever conducted. Published results. Physical validation. 2,500 sites. Decades of data.

The measurement settles the debate regardless of which side wins. That is the offering.

---

## What This Gives Ramsar

Ramsar monitors wetlands. The current monitoring regime tracks species counts, habitat areas, water levels. These are magnitudes. They tell the site manager: how much of each thing is there?

CoDa gives Ramsar the correct mathematics for analyzing those numbers as compositions — ratios, balances, geometric structure. That is an immediate upgrade to every analysis Ramsar already performs.

HUF gives Ramsar the audit trail — drift events, metric disagreements, structural shocks, zero events, dimensionality changes. That is the temporal monitoring layer CoDa does not yet provide.

The coherence residual gives Ramsar something neither CoDa nor HUF alone can deliver: **early warning of structural ecological change**.

A wetland where species counts are stable but cross-trophic coupling is changing is a wetland where the food web is restructuring. The birds are still there. The fish are still there. The plants are still there. But the relationships between them — who eats whom, who competes with whom, who depends on whom — are shifting. The composition looks fine. The structure is failing.

That is the ecological equivalent of deceptive drift. The total SPL is stable. The spectral balance is broken. The listener hears something wrong before any single measurement shows a failure.

Except the listener, in Ramsar's case, is the ecosystem. And by the time the species counts change, the structural damage is already done.

The coherence residual detects the structural change while the composition still looks healthy. That is the early warning. That is what 172 countries need from a monitoring instrument. That is what the planet needs from mathematics.

---

## The Conference Offering

Three sentences. One for each audience.

**To the CoDa community:** "The coherence residual makes subcompositional coherence measurable, not assumed. It provides the first empirical instrument for testing the Egozcue-Greenacre question at scale, across 2,500 wetlands, over decades. The data will settle the debate."

**To Ramsar:** "The coherence residual detects ecological structural change while species counts are still stable. It provides early warning of food web restructuring — the most dangerous kind of wetland degradation, because it is invisible to magnitude monitoring."

**To both:** "CoDa gives Ramsar the correct mathematics. Ramsar gives CoDa the largest compositional monitoring application in history. The coherence residual is the bridge — it serves CoDa's theoretical needs and Ramsar's conservation needs with the same measurement."

---

## The Doctrine Holds

The paired-measurement doctrine said: always two results, always examine both. TV and Aitchison.

The third diagnostic does not replace the pair. It adds a measurement of the measurement — a diagnostic on whether the instrument's own structural assumptions are holding. The composition is monitored by TV and Aitchison. The partition is monitored by the coherence residual. The instrument watches the system AND watches itself.

That is the engineering instinct from day one in Sherbrooke: the managers see the setpoint, the engineers see the actual, and underneath it all, a silent alarm triggers when the two diverge. The setpoint is the SBP. The actual is the ecological coupling. The coherence residual is the silent alarm.

*"I am building a tool to protect myself from my own ignorance."*

The third diagnostic protects the instrument from its own assumption — that the partition holds. When it doesn't, the instrument knows. When it does, the instrument can prove it.

Save the wetlands. Save the planet. Save ourselves. Mathematics has a purpose. This is it.

---

*Three diagnostics. Three questions. Three answers.*
*TV: What moved?*
*Aitchison: How did the geometry change?*
*Coherence residual: Is the instrument still telling the truth?*
