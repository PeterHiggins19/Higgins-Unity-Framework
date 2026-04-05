# Scaling Coherence: From 1→2→4 to Deep Hierarchies

**The scaling path needs its own calibration study.**

*Peter Higgins + Claude · April 2026*
*Status: Working document — solution architecture for Ramsar-scale deployment*

---

## The Problem

HUF's coherence chain was born as 1→2→4. One signal, two groups, four drivers. Clean binary structure. Small simplices at every level. The crossover frequencies define the partition. The mathematics is well-behaved.

Ramsar needs 1→n1→n2→n3. One wetland, several trophic groups, dozens of families, hundreds of species. The chain could be 1→5→50→500. At that scale, nine mathematical problems emerge that do not exist in 1→2→4:

1. High-dimensional simplices at each level
2. SBP design explosion (combinatorial partition choices)
3. Coherence gate proliferation (false alarm accumulation)
4. Information compression across multiple aggregation levels
5. Zero event amplification (more carriers = more zeros)
6. Compositional Nyquist mismatch (different levels move at different speeds)
7. Log-ratio numerical instability in large groups
8. Subcompositional coherence verification at scale
9. Stored energy heterogeneity across levels (CLS path)

None are fatal individually. Together they change the regime.

---

## The Solution: Telescoping Coherence

The solution is already embedded in the mathematics. The SBP converts any n-carrier simplex into exactly (n−1) binary balances. Each binary balance is a log-ratio of the geometric means of two groups. Each binary balance is a 1→2 problem.

HUF was designed for 1→2 problems.

The deep hierarchy does not need to be monitored as a deep hierarchy. It needs to be decomposed into a tree of binary balances, each monitored independently, with a gating protocol that determines when to drill deeper.

### The Principle

A 500-species wetland with 5 trophic groups, 50 families, and 500 species does not require a single 500-dimensional simplex monitor. It requires:

- 4 binary balances at Level 1 (5 trophic groups → 4 ILR balances via SBP)
- ~45 binary balances at Level 2 (50 families → ~45 ILR balances, distributed across groups)
- ~450 binary balances at Level 3 (500 species → ~450 ILR balances, distributed across families)

Total: ~499 binary balance monitors. Each one is a 1→2 coherence check — the regime HUF was built for.

### The Telescope

Not all 499 balances need active monitoring at every time step. The telescope operates:

**Wide field** — Monitor the Level 1 balances (4 checks). These capture macro-structural shifts: is the bird/fish/plant/invertebrate balance changing? The dual metric (TV + Aitchison) runs on these 4 balances. If all stable, the telescope stays wide. Audit trail records: no events at macro level.

**Zoom on anomaly** — When a Level 1 balance triggers (drift, shock, disagreement, zero, dimensionality change), open the coherence gate for the affected group. Now monitor the Level 2 balances within that group (~10 checks for the triggered group). The telescope narrows to the branch where the event occurred.

**Deep zoom** — When a Level 2 balance triggers within the anomalous group, open the Level 3 gate for the affected family. Now monitor the species-level balances within that family (~10 checks). The telescope has found the branch, the twig, and now seeks the leaf.

**Event resolution** — The audit trail records the telescope's path: "Level 1 balance (birds vs fish) shifted → Level 2 balance (waders vs raptors within birds) shifted → Level 3 balance (species X collapsed within waders)." The event is localized through the hierarchy without ever monitoring all 499 balances simultaneously.

---

## How This Solves Each Problem

### 1. High-dimensional simplices → eliminated

Each comparison is binary. The maximum simplex dimension at any single check is S¹ — one log-ratio, one balance, one number. The 500-dimensional simplex is never constructed.

### 2. SBP design explosion → constrained by ecology

The SBP at each level must come from the system's natural structure, not from mathematical convenience. At Level 1, the trophic groups define the partition. At Level 2, the taxonomic families. At Level 3, the species within families. The ecology dictates the partition — the same way the crossover frequencies dictate it in the loudspeaker. If the system does not suggest a natural partition at a given level, that level should not exist in the chain.

*Design rule: every SBP node must be ecologically motivated. If the partition is arbitrary, the balance is meaningless regardless of mathematical validity.*

### 3. Coherence gate proliferation → managed by telescope

Not all gates are open simultaneously. At rest, only the Level 1 gates are active (4 checks). The false alarm rate is governed by 4 gates, not 499. Gates at deeper levels open only when triggered by a parent-level anomaly. The effective false alarm rate at any time is bounded by the number of currently active gates, which is typically small.

*Governing equation: effective false alarm rate = 1 − (1−α)^k where k = number of currently active gates, not total gates in the tree.*

### 4. Information compression → explicit and auditable

Each binary balance answers one structural question: "Is the ratio between these two groups changing?" The compression at each level is deliberate and interpretable. A Level 1 balance says: "Birds vs fish — is the ratio shifting?" A Level 2 balance says: "Within birds, waders vs raptors — is the ratio shifting?" The audit trail records which questions were asked and what the answers were.

The compression is a feature, not a loss. The telescope's power is that it asks the right question at the right level and only drills deeper when the answer demands it.

### 5. Zero amplification → localized

A zero at Level 3 (one species disappears) affects only the binary balances involving that species — typically 1 balance at Level 3 and its parent balance at Level 2. It does not propagate to all 499 balances. The zero-event protocol (detect before transform) is applied locally at the affected balance. The containing group's aggregate at the parent level may shift, triggering the telescope to zoom in — which is the correct response.

*The zero does not break the hierarchy. It triggers the telescope.*

### 6. Compositional Nyquist → level-specific sampling

Each level of the telescope can operate at its own effective sampling rate. Level 1 balances (macro trophic structure) may be monitored annually. Level 2 balances (family structure within a triggered group) may be monitored seasonally. Level 3 balances (species within a triggered family) may be monitored monthly or event-driven.

The telescope's gating protocol naturally handles the Nyquist mismatch: deep levels are only sampled when the parent level says something is moving. This is demand-driven sampling, not uniform sampling. It avoids both under-sampling fast events (because the telescope zooms when needed) and over-sampling slow structure (because the wide field is sufficient when nothing moves).

### 7. Log-ratio stability → guaranteed by binary structure

Each binary balance involves the geometric mean of two groups. The geometric mean of a group with k members is the k-th root of the product. In a binary balance, each side of the ratio is a single geometric mean. The numerical stability of a two-group geometric mean ratio is far better than a 500-part CLR. The ILR via SBP ensures that no single computation involves more than two group-means.

*Exception: if one group is very large (200 species) and contains values near zero, the geometric mean can underflow. Mitigation: apply zero-event detection before computing the geometric mean. Zeros are events, not values.*

### 8. Subcompositional coherence → verified per balance

Each binary balance is a subcomposition with exactly two parts. Subcompositional coherence for a 2-part subcomposition is trivially satisfied — the ratio between the two parts is invariant under marginalization by construction. The Egozcue requirement holds at every node of the SBP tree without additional verification.

*The coherence requirement that is hard to verify for a 500-part composition is automatically satisfied when the composition is decomposed into binary balances.*

### 9. Stored energy heterogeneity → irrelevant for GOV

HUF-GOV is stateless. There is no stored energy at any level. Each binary balance comparison is independent. The heterogeneous stored energy problem only arises in HUF-CLS (the control path), which is not part of the scientific monitoring instrument.

If CLS is ever deployed at Ramsar scale, the stored energy at each level must be governed independently — but that is a governance problem, not a mathematical one, and it is deferred by design.

---

## The Audit Trail in a Deep Hierarchy

The telescope produces a structured audit trail:

```
Event 2031-Q2:
  Level 1: Bird/Fish balance shifted (TV: 0.03, Aitchison: 0.12 — DISAGREEMENT)
    → Telescope opened Level 2 for Birds
  Level 2: Wader/Raptor balance within Birds shifted (TV: 0.08, Aitchison: 0.09 — AGREEMENT)
    → Telescope opened Level 3 for Waders
  Level 3: Species X → ZERO EVENT (carrier exited composition)
    → Event classified: species loss in waders, detected at Level 3,
      visible as trace-carrier Aitchison shift at Level 1
  Resolution: deep event propagated through 3 levels in 1 monitoring cycle
  Metric signature: TV/Aitchison disagreement at Level 1 indicated trace-carrier
    movement — confirmed by species-level zero event at Level 3
```

The audit trail records not just the event but the telescope's path through the hierarchy. The disagreement pattern at Level 1 (TV small, Aitchison large) correctly predicted that the event was a trace-carrier perturbation before the telescope found the specific species.

---

## What This Means for Ramsar

The 2,500 Ramsar wetlands do not need 2,500 instances of a 500-dimensional monitor. Each wetland needs:

1. An ecologically motivated SBP (trophic groups → families → species)
2. A telescope with Level 1 balances in continuous monitoring
3. Demand-driven zoom to deeper levels when Level 1 triggers
4. A structured audit trail recording the telescope's path

The governance overhead is proportional to the number of active events, not the number of species. A stable wetland requires 4-6 Level 1 balance checks per monitoring cycle. A wetland in crisis triggers the telescope and temporarily requires deeper monitoring — which is precisely when deeper monitoring is justified.

The scaling is logarithmic with hierarchy depth, not exponential with carrier count. A 500-species wetland monitored through a 3-level SBP tree requires ~4 active balance checks in steady state and ~20-30 during an event investigation. Not 499.

---

## The Calibration Study for Scaling

This solution architecture needs its own error catalogue — the scaling entanglement analysis. Candidate error sources specific to deep hierarchies:

- **ES-01**: SBP design error — partition does not reflect ecological structure
- **ES-02**: Telescope latency — deep event occurs between Level 1 sampling cycles
- **ES-03**: Cross-branch interference — event in one branch masks event in another at the parent level
- **ES-04**: Geometric mean collapse — simultaneous zeros in a large group underflow the group mean
- **ES-05**: Partition instability — the ecological structure itself changes (new trophic relationships), invalidating the SBP
- **ES-06**: Level-crossing artifacts — an event that is real at Level 3 but cancels at Level 2 (compositional Simpson's paradox)

These six error sources are the beginning of the scaling calibration study. Each needs a detection test and a governance action, following the pattern of E-01 through E-17.

---

## One Sentence

The deep hierarchy is not a bigger 1→2→4 — it is a forest of 1→2 problems, monitored through a telescope that zooms where the signal demands, governed by the same open-loop doctrine that began with one loudspeaker in one room.

---

*"The scaling path needs its own calibration study."*
*— Peter Higgins, on the transition from 1→2→4 to Ramsar*
