# The Core of HUF

## Explained for the CoDa Community

---

## Start with a loudspeaker.

Not a theory. Not a paper. A loudspeaker.

A professional studio monitoring loudspeaker has four drivers: a woofer, a mid-woofer, a midrange, and a tweeter. Each driver reproduces a portion of the audible frequency spectrum. Together, the four drivers must reconstruct the full signal — faithfully, completely, with nothing added and nothing lost.

The four drivers form a composition. Each driver carries a share of the total acoustic energy. The shares must sum to the whole. This is a composition on S³.

A microphone measures the result. One measurement point. One carrier. This is the reference — the ground truth of what the system actually produced. Call it the 1-composition.

The loudspeaker operates in stereo. Two channels — left and right. Each channel carries a share of the stereo image. The two channels must be coherent: matched in level, time-aligned, spectrally balanced. This is a composition on S¹. Call it the 2-composition.

Within each stereo channel, the four drivers must be coherent: the crossover network divides the spectrum, each driver carries its assigned band, no gaps, no overlaps, no destructive interference. This is a composition on S³. Call it the 4-composition.

The system is hierarchical:

```
1-composition (mic / reference)
  └── 2-composition (stereo pair)
        └── 4-composition (drivers per channel)
```

One locks two. Two locks four. Coherence flows downward. If the stereo pair is incoherent, it doesn't matter whether the individual drivers are perfect — the output is wrong. If the drivers within a channel are incoherent, it doesn't matter whether the stereo balance is perfect — the output is wrong.

**Group coherence is the gate to inter-group analysis.**

You cannot meaningfully study the relationship between the stereo channels until each channel is internally coherent. You cannot meaningfully study the relationship between the loudspeaker and the microphone reference until the stereo image is coherent. Each level of the hierarchy must be compositionally stable before the next level up carries meaning.

---

## Now forget the loudspeaker.

Replace the four drivers with four energy carriers: coal, gas, nuclear, renewable.

Replace the stereo pair with two carrier groups: fossil and non-fossil.

Replace the microphone with total electricity generation — the single reference measurement.

The structure is identical:

```
1-composition (total generation / reference)
  └── 2-composition (fossil vs non-fossil)
        └── 4-composition (coal, gas, nuclear, renewable)
```

One locks two. Two locks four. Group coherence gates inter-group analysis. A country's fossil-vs-non-fossil balance only means something if the carriers within each group are compositionally accounted for. The total generation figure only means something if the two groups sum to it coherently.

---

## Now forget energy.

Replace the carriers with species in a wetland. Replace the groups with trophic levels. Replace total generation with total biomass.

```
1-composition (total biomass / reference)
  └── 2-composition (flora vs fauna)
        └── N-composition (species within each kingdom)
```

Same structure. Same hierarchy. Same coherence chain.

---

## The pattern is universal.

Any system where a finite total is divided among carriers, which are organized into groups, which nest into a single reference measurement, has this structure. The simplex is the space. The hierarchy is the architecture. The coherence chain is the monitoring protocol.

This is HUF.

---

## What the coherence chain does.

At each level of the hierarchy, HUF asks two questions:

**1. Is this group internally coherent?**

Measure the composition within the group. Compute the perturbation between consecutive time periods. Compute the Aitchison distance. If the distance is small — the group is stable. If the distance is large — something moved. This is standard CoDa analysis applied at the group level.

**2. Is the change authorized?**

This is the question CoDa does not ask, because CoDa is an analytical framework, not a monitoring framework. HUF adds the governance layer: was the perturbation accompanied by a governance record? Did someone decide to change the composition, or did it drift on its own?

If authorized: normal operation. The system was intentionally reweighted.
If unauthorized: silent drift. The composition changed with no corresponding decision. This is the detection target.

---

## The control option.

The hierarchy can operate in two modes:

**Open loop:** Observe, measure, record. The composition evolves. You watch. You detect drift. You report. This is what CoDa does — analysis of compositional data. HUF does this too.

**Closed loop:** Observe, measure, compare to declared state, correct. The composition deviates from the intended allocation. The system responds. In the loudspeaker, this is the DSP correction sent back through the amplifier. In an energy grid, this would be a policy adjustment. In a wetland, this would be a conservation intervention.

The switch between open and closed loop is the governance threshold — the point where passive observation becomes active response. In HUF, this is called the governance boundary. The mathematics on both sides of that boundary are identical. The Aitchison distance doesn't care whether you're observing or correcting. The distinction is operational, not geometric.

---

## What this means for CoDa.

The simplex, perturbation, Aitchison distance, log-ratio transforms, balances, sequential binary partitions — these are the mathematical tools that formalize what the coherence chain does at each level. CoDa provides the geometry. HUF provides the architecture.

Specifically:

| CoDa provides | HUF adds |
|--------------|----------|
| The simplex as sample space | Nested simplices in hierarchy |
| Perturbation as change measure | Perturbation as drift detection trigger |
| Aitchison distance as metric | Aitchison distance as alarm threshold |
| Balances as interpretable coordinates | Balances as the crossover network between groups |
| Sequential binary partition | The hierarchy itself — 1→2→4→N |
| Subcompositional coherence | Group coherence as gate to inter-group analysis |
| Analysis of completed datasets | Continuous, period-by-period monitoring |
| No governance concept | Authorized vs unauthorized change |
| Open loop (observe) | Open or closed loop (observe or correct) |

---

## Where this came from.

This did not come from reading papers. It came from tuning loudspeakers.

For forty years, Peter Higgins operated a physical system where four drivers had to sum to a coherent whole, where two channels had to be matched, where one microphone told the truth, and where every adjustment was either intentional or a problem. He built the monitoring protocol with his hands and his ears before he had any mathematical language for it.

The mathematical language already existed. Aitchison formalized the simplex in 1982. Egozcue and Pawlowsky-Glahn built the Hilbert space structure. The CoDa community developed log-ratios, balances, perturbation algebra, distance measures, zero handling, subcompositional coherence — forty years of rigorous geometry.

Two parallel forty-year efforts. One built the geometry. One built the monitoring protocol. Neither knew the other existed.

They meet in Coimbra, June 2026.

---

## The offer.

The geometry is yours. The coherence chain is mine. The data is public. The code is open. The claim is falsifiable.

I am not claiming new mathematics. I am claiming a new use: hierarchical compositional monitoring with governance distinction, built on your geometry, applicable to any system that sums to a whole.

If this is already known — show me, and I will withdraw the claim.
If this is new — help me formalize it, and the door opens to every compositional system on the planet.

The first application is energy. The next is wetland ecosystems under the Ramsar Convention. After that, every domain in the regime catalogue.

One hierarchy at a time. One coherence chain at a time. One room at a time.

This room first.

---

*Peter Higgins — Independent Researcher — Rogue Wave Audio, Markham, Ontario*
*CoDaWork 2026, Coimbra, Portugal*
