# What HUF Is

## A proper technical description for engineers, scientists, and anyone who listens carefully

*Peter Higgins · April 2026*

---

## Origin

HUF began as a loudspeaker measurement technique.

A BTL (Binaural Test Lab) loudspeaker system divides a single audio signal into frequency bands — each band routed to a dedicated driver. The signal enters as a whole. The crossover network partitions it. The drivers reproduce their portions. The room recombines them at the listener's ear. At every stage, the parts must sum to the whole. At every stage, the balance matters.

> **BTL** — Binaural Test Lab. The name refers to both the physical laboratory in Markham, Ontario (purpose-built by Peter Higgins for loudspeaker measurement and closed-loop validation) and the loudspeaker system itself. The lineage is deliberate: Bell Telephone Labs (BTL) developed stereo nearly a century ago. The canonical definition is in RWA-001.

The crossover network is a Sequential Binary Partition. The drivers are carriers. The acoustic output at the listening position is a composition on the simplex — a vector of proportions summing to a conserved total. If the composition is correct, the sound is coherent. If a driver drifts — aging suspension, thermal compression, misalignment — the composition shifts, and the listener hears something wrong before any single measurement shows a failure.

That observation — that compositional drift is detectable before component failure — is the origin of HUF. Everything that followed was the discovery that this property is not unique to loudspeakers.

---

## What It Actually Is

HUF is a **multichannel coherent detector** for compositional systems.

It is not a phase-locked loop. It is not a control system. It is not a search engine, a prediction model, or an optimization algorithm. It is a receiver.

In communications terms:

A transmitter encodes information onto a carrier by modulating it — shifting the carrier's frequency, phase, or amplitude. The receiver recovers the information by comparing the received signal against a known reference. If the receiver's reference matches the carrier, the demodulated output is the information signal. If the reference is wrong, the output is noise.

HUF works the same way, except the "transmitter" is a physical system (an energy grid, a wetland, an economy), the "carriers" are the compositional parts (fuel types, species, economic sectors), the "modulation" is whatever the real world does to the balance of those parts (policy, climate, market forces, decay), and the "reference" is the declared composition — the proportional balance that governance has authorized or that the system was designed to maintain.

HUF compares the observed composition against the reference and outputs the difference. That difference is the signal. Drift magnitude, drift direction, drift velocity, which carrier group moved, whether the change was authorized — all of that is readable from the difference, provided the reference is correct.

If the reference is wrong — stale, unauthorized, never properly declared — the output is noise. Just like an unlocked receiver.

---

## The Architecture, Properly Named

### HUF-GOV: The Detector (Open Loop)

HUF-GOV is a **phase discriminator** — the stateless comparison stage of a coherent receiver.

| Stage | Communications Equivalent | HUF-GOV Implementation |
|-------|--------------------------|----------------------|
| Reference | Local oscillator | Declared composition — set by governance, fixed until governance updates it |
| Input signal | Received modulated carrier | Observed composition — the data arriving from the system |
| Comparison | Phase detector / discriminator | Aitchison distance, perturbation velocity, TV distance, ILR balances — all computed from (reference, observation) pair |
| Output | Demodulated information signal | Drift magnitude, drift direction, velocity, carrier group identification |
| Memory | None | None. Each comparison is independent. No state carried forward. |
| Feedback | None | None. The detector does not adjust the system or itself. |

This is the instrument. It reads. It does not decide. It does not act. It has no stored energy — no smoothing, no accumulation, no averaging that would cause the instrument to respond partly to its own past outputs instead of purely to the system.

The human decides what the reading means. The human decides whether to act. The instrument stays open-loop.

### HUF-CLS: The Loop (Closed Loop)

HUF-CLS is a **phase-locked loop** — the full control architecture where detection drives correction.

| Stage | PLL Equivalent | HUF-CLS Implementation |
|-------|---------------|----------------------|
| Phase detector | Same as above | HUF-GOV detector output (drift signal) |
| Loop filter | Low-pass filter / PI controller | Governance policy — how fast to respond, how much correction to allow |
| VCO | Voltage-controlled oscillator | System intervention — policy adjustment, resource reallocation, operational change |
| Capture range | Maximum frequency offset for lock acquisition | Breaker 16 — maximum authorized correction magnitude |
| Lock condition | Output frequency matches input | Observed composition returns to declared reference |
| Stored energy | VCO inertia, filter capacitance | Institutional momentum, policy latency, resource commitments |

This is the control system. It adjusts the system based on the detector's readings. It has stored energy by design — governance decisions have inertia, resources have commitment periods, policies resist change. That stored energy is acknowledged, documented, and governed through CL-01 to CL-05 with 19 documented failure modes (KILL-001).

HUF-CLS is not being presented at CoDaWork 2026. It is published for transparency, not for deployment. The conference presentation concerns the detector only.

---

## Why "Multichannel Coherent"

A single-channel detector monitors one carrier against one reference. A thermometer. A pressure gauge. Useful but limited — it tells you about one variable.

HUF monitors multiple carriers simultaneously against a common reference frame. This is what makes it a compositional instrument rather than a collection of individual monitors. The carriers are not independent — they share a constant sum. When one moves, others must accommodate. The information is in the *relationship between carriers*, not in any single carrier's value.

The coherence chain (1→2→4) structures how carriers are grouped and analyzed:

- **1** — the whole. Total generation. Total species count. GDP. The single reference that defines the composition.
- **2** — the first partition. Fossil vs non-fossil. Predator vs prey. Goods vs services. The coarsest meaningful division.
- **4+** — the second partition. Coal/gas/oil/nuclear/hydro/solar. Individual species. Sector breakdown. The carriers that compose each group.

Group coherence gates inter-group analysis. If the carriers within a group are incoherent (drifting relative to each other), the group's aggregate behavior is unreliable as a signal — it's like reading the output of a loudspeaker where the drivers are fighting each other. You fix the intra-group coherence before you trust the inter-group comparison.

This hierarchical structure is a physically motivated Sequential Binary Partition — the partition comes from the system's own architecture, not from the analyst's convenience. In a loudspeaker, the crossover frequencies define the partition. In an energy grid, the dispatchable/non-dispatchable boundary defines it. In a wetland, the trophic levels define it. The system tells you how to partition it.

---

## The Dual Metric

HUF runs two distance metrics on every reading:

**TV distance** (Total Variation) — information-theoretic, operates on raw proportions, linear, sensitive to absolute changes in dominant carriers. This was HUF's original metric, predating the CoDa integration.

**Aitchison distance** — simplex-native, operates on log-ratios, sensitive to relative changes across all carriers including traces. This is the CoDa-correct metric, adopted after discovering the Aitchison geometry.

Where they agree: the signal is robust to metric choice. Real event.

Where they disagree: the divergence is diagnostic.
- TV large, Aitchison small → a dominant carrier moved. The log-ratio compression minimized it.
- Aitchison large, TV small → a trace carrier moved. The log-ratio expansion amplified it.

The disagreement tells you what *kind* of event occurred — dominant restructuring vs trace perturbation — without needing to identify the specific carrier first. No existing CoDa tool uses metric disagreement as a diagnostic signal. This is HUF's contribution to the measurement architecture.

---

## Who Employs This

### Scientists who monitor compositions that change over time

Ecologists tracking species composition in wetlands, forests, fisheries. Geochemists monitoring groundwater chemistry. Epidemiologists watching disease composition. Climate scientists tracking energy mix, land use, atmospheric composition. Anyone whose system has parts that sum to a meaningful whole and whose question is not "what does this dataset reveal?" but "is this system drifting right now?"

The Ramsar Convention (172 countries, 2,500 wetlands) is the strategic deployment target — they already collect compositional data, already have monitoring teams, already have governance structure. They need the instrument.

### Engineers who build systems with compositional balance

Power grid operators managing generation mix. Manufacturing engineers monitoring process compositions (alloy ratios, chemical blends, assembly proportions). Quality engineers who already use control charts and will recognize the MEWMA-CoDa connection. Network engineers monitoring traffic composition.

These are the people who already think in proportions but monitor in magnitudes — who watch individual gauges instead of the balance between them. The fuel gauge metaphor: tank full, needle didn't move, but the fuel changed. The engine is tuned for one blend and fails on another.

### Governance bodies who authorize compositional decisions

Energy regulators who approve generation mix transitions. Environmental agencies who set species conservation targets. Financial regulators who monitor portfolio concentration. Any authority that declares "this is the intended balance" and needs to know when reality departs from intention — and whether the departure was authorized.

### Who does NOT employ this

Anyone whose system does not have parts summing to a meaningful whole. Anyone whose question is prediction rather than detection. Anyone who wants the instrument to make decisions. HUF reads. The human decides.

---

## From Loudspeaker to Universal Instrument

The path was not direct.

A loudspeaker crossover partitions a signal into frequency bands. Each band drives a transducer. The transducers are the carriers. Their compositional balance defines the tonal character at the listening position. When that balance drifts — thermal compression, aging, mechanical wear — the listener perceives degradation before any single driver fails. The composition changed. The total SPL didn't.

The question was: is this property unique to loudspeakers, or is it general?

Energy grids have the same structure. The total generation is the signal. The fuel types are the carriers. The generation mix is the composition. When the mix drifts — coal retires, solar surges, gas fills gaps — the total may stay stable while the internal structure transforms. Germany's electricity generation: total stable for 25 years, internal composition in continuous upheaval. p = 0.0016 on the structural concentration test.

Wetlands have the same structure. GDP has the same structure. Transit networks have the same structure.

The loudspeaker was the first system. The simplex was the geometry. The phase detector was the architecture. The crossover was the partition. The drivers were the carriers. Everything else was discovering that the same instrument works everywhere a conserved whole divides into meaningful parts.

Forty years of active filter crossover design. Six months of formalization. The instrument was always there. It just needed the right mathematics — and the right community — to name what it does.

---

## The Next Step

The mathematics already exists. Aitchison formalized the simplex geometry in 1982. Egozcue and Pawlowsky-Glahn built the Hilbert space structure. The MEWMA-CoDa researchers built statistically optimal control charts. Filzmoser built robust outlier detection.

The monitoring doctrine already exists. HUF's open-loop discipline, governance reference management, kill test, coherence chain, stored energy audit, and 16-error calibration study.

What doesn't exist yet is the union. The instrument that combines CoDa's mathematical rigour with HUF's monitoring architecture. The instrument that is statistically optimal AND governancially sound. The instrument that watches compositions move and tells you when to care.

That union is the purpose of CoDaWork 2026.

One microphone. Two channels. Four drivers. One framework.

---

*For the mathematics: [FORMULA_REFERENCE.md](FORMULA_REFERENCE.md)*
*For the error sources: [ENTANGLEMENT_ERROR_ANALYSIS.md](ENTANGLEMENT_ERROR_ANALYSIS.md)*
*For the literature: [CODA_LITERATURE_CROSS_REFERENCE.md](CODA_LITERATURE_CROSS_REFERENCE.md)*
*For the union thesis: [THE_UNION.md](THE_UNION.md)*
*For the honest answers: [BATTLE_CARD.md](BATTLE_CARD.md)*
*For Sharon: [FOR_SHARON.md](FOR_SHARON.md)*
