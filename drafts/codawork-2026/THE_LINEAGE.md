# The Lineage

**This instrument wasn't designed for CoDa. It was designed for physics. And the physics turned out to be compositional.**

---

## Part Zero — The Isotropic Principle

Before the loudspeaker. Before the cabinet. Before the signal.

Paint the inside of a sphere with radiation. Uniform. Every point on the interior surface receives the same energy. No direction is privileged. No part is heavier than any other. This is the ground state — the isotropic condition. In a language I did not yet have, this is the barycenter of the simplex: the composition (1/D, 1/D, ..., 1/D), maximum entropy, maximum ignorance, the state where the system has no opinion about where its energy belongs.

The geometry of that sphere exists whether or not anything is radiating. The structure is there before the signal. The simplex is there before the measurement. The number of parts, the closure constraint, the distances between possible configurations — all of it is determined by the geometry alone, independent of what flows through it.

This is the design principle that precedes everything else in HUF: the architecture is isotropic. The ground state is uniform. Every departure from isotropy is a signal — a compositional event that the geometry was already prepared to receive. Every return toward isotropy is relaxation. The geometry does not care what kind of energy paints the sphere — acoustic radiation, electricity generation shares, financial portfolio weights, wetland habitat proportions. The sphere is the same sphere.

And the deepest part: a sound present or not is not required for the geometry to be discovered. The structure is discoverable spatially — the cabinet dimensions determine the radiation pattern before any signal is applied. Dimensionally — the number of parts constrains the simplex regardless of what flows through them. Temporally — EITT reads the geometry's information-preserving properties by compressing time. Three different probes, same underlying structure. Add the signal and you tune to the structure — you don't create it. You reveal what was always there.

This is why HUF is inert. Not as a design choice. As a consequence. If the geometry precedes the signal, then the measurement system's job is to couple to the geometry without disturbing it. The probe reads the departure from isotropy. It does not create the departure. It does not add its own signature. The errors it finds were always there. The geometry was always there. HUF just made them readable.

*The Aitchison geometry is not a correction you apply to data. It is the geometry the data already lives in. The isotropic principle says: that geometry was there before the data arrived.*

---

## It Started with a Speaker in a Room

I measure loudspeakers. That's the practical origin. Not statistics, not ecology, not compositional data analysis. Loudspeakers.

A cabinet sits in a room. Feed it a signal. It radiates sound — not equally in every direction, because the cabinet has dimensions, and dimensions interact with wavelength. At low frequencies, where the wavelength is much longer than the cabinet, the sound goes everywhere equally. Omnidirectional. Isotropic. Every direction gets the same share of the energy.

That's the ground state realized physically. The sphere I painted in my mind, built out of wood and drivers and crossover networks. In CoDa language, the barycenter of the simplex. I didn't know that word yet. I just knew that when a speaker radiates equally in all directions, it's doing the simplest possible thing with a fixed energy budget — and that any departure from that simplicity is information.

*Mathematically: at frequency f where wavelength λ >> cabinet dimensions, the directional energy distribution approaches the uniform composition* **p** = (1/D, 1/D, ..., 1/D) *on the D-directional simplex. Total radiated power is the closure constraint. The isotropic state is the maximum-entropy composition. Every physical system that distributes a conserved budget among D parts begins here, whether or not it knows it.*

---

## Then the Pattern Breaks

As frequency rises, wavelength shrinks. When it gets close to the cabinet dimensions, the pattern changes. Energy concentrates forward. The sides lose power. The back drops off. The composition moves away from the barycenter — and it moves in a way that the cabinet geometry dictates.

I called this DADC — Dimension-Apportioned Diffraction Correction. The total baffle step correction is exactly 6.02 dB (the 2-pi to 4-pi radiation transition). That 6.02 dB must be apportioned among the physical dimensions: height gets 3.21 dB, width gets 1.48 dB, depth gets 1.33 dB. They always sum to 6.02. The corner frequency for each dimension is 115/dimension (Hz*m constant). The gains are proportional shares of a fixed total — a composition on the simplex, enforced by physics.

Then I built the inverse: DADI — Dimension-Apportioned Diffraction Inference. Give the system only the acoustic response, and it reconstructs the physical dimensions from the gain ratios. Non-contact. The probe reads the geometry without touching the object, without imprinting its own signature on the result. That design requirement — the measurement must be inert — carried forward unchanged into everything that followed.

I didn't have a word for simplex yet. I just knew the gains had to sum to 6.02, the ratios carried the structural information, and the probe must not contaminate its own reading.

*Mathematically: DADC maps cabinet dimensions to a composition on* **S**^3 *with closure constraint kappa = 6.02 dB. The gain vector (G_H, G_W, G_D) / 6.02 = (0.533, 0.246, 0.221) is a three-part simplex composition. The dominance index max/min is a pairwise log-ratio. DADI inverts this mapping — reconstructing geometry from acoustic response — which is the prototype of EITT inversion.*

---

## I Built a Tool to Protect Myself from My Own Ignorance

That's the honest version. A loudspeaker measurement produces thousands of numbers. Frequency response, directivity, impedance, phase. The temptation is to look at one curve and decide if the speaker is good. But one curve lies. A flat frequency response can hide a violent directional redistribution. A smooth power curve can mask a carrier going to zero at a specific angle. The numbers say everything's fine. The physics is broken. And nobody knows, because only one thing was examined.

So I built the instrument to always give me two results. Always two. Both get examined. If they agree — good, proceed. If they disagree — stop, investigate, because the disagreement is telling me something my model missed. Lose nothing. Discard nothing. Every number is diagnostic until proven otherwise.

That's not statistics. That's survival. When measuring something not fully understood, the instinct is to build redundancy into the observation — not to get two copies of the same answer, but to get two different views of the same phenomenon so their disagreement teaches what the model hasn't figured out yet.

*Mathematically: any single distance metric on the simplex collapses information. Two metrics — one measuring absolute share redistribution (TV), one measuring geometric displacement in log-ratio space (Aitchison) — decompose compositional change along orthogonal diagnostic axes. Their agreement confirms; their disagreement classifies the type of change.*

---

## DADI — Encoding the Correction in the Geometry

Then I realized something. If the measurement lives on the simplex, and the reference state lives on the simplex, then the difference between them — the error signal — also lives on the simplex. There is no need to leave the geometry to compute the correction. The delta change between where the composition is and where it should be is itself a compositional quantity.

DADI. By encoding the corrections with the geometry, a delta change could track a desired response. The instrument wasn't just reading where the speaker was radiating. It was reading the departure from where it should be radiating — and that departure was expressed in the same coordinate system as the measurement.

That felt important. I didn't know why yet.

*Mathematically: in Aitchison geometry, the perturbation between two compositions is itself a composition. The departure from a reference state* **p**_ref *is computed via the perturbation operation* **p** ⊖ **p**_ref *, yielding a delta that lives on the same simplex. This is the error signal — geometrically native, not projected from an external space.*

---

## ADAC — The Moment the Loop Did Not Close

This is the moment that made everything else possible.

The error signal was sitting there. DADI gave me a geometrically native correction. The delta between measurement and reference was computable, expressible, actionable. Every instinct in engineering says: feed it back. Close the loop. Minimize the error. That's what control systems do. That's what a PLL does. That's what MEWMA-CoDa does with its smoothing parameter.

And something said: no. Don't close the loop. Not automatically. Not by default.

ADAC. The natural way to stop the automatic closing of the loop and allow a choice. Observe — or control. Read the error — or act on it. The instrument forks right there, at that decision point, and which path is taken is not an engineering default. It is a governance decision.

That's where GOV and CLS were born. Not on a whiteboard. Not from a principle. From a mechanism that physically prevented the loop from closing without someone deciding it should close.

HUF-GOV stays open. Stateless. No stored energy. It reads the error and records it. Scientific instrument.

HUF-CLS closes the loop. Stores energy. Feeds back. Drives correction. Control system.

Same error signal feeds both. The architecture is identical up to the fork. The fork is the entire doctrine.

*Mathematically: GOV implements a phase discriminator — a stateless comparison operator that outputs the signed angular displacement between measurement and reference without modifying either. CLS implements a phase-locked loop — a feedback system where the error signal drives a correction through a loop filter (governance policy) to a controlled oscillator (system intervention). GOV has zero state memory. CLS has state memory by design. The open-loop doctrine requires that the scientific measurement path (GOV) never accumulates state, ensuring observations cannot influence their own readings.*

---

## All Done in Weeks. To Understand It Is Ongoing.

DADC. DADI. ADAC. GOV/CLS. The whole architecture was built in weeks. Not months. Not years. Weeks. The physics demanded it faster than the theory could keep up.

That's the part nobody tells anyone about instrument design. The instrument is not understood first and then built. It is built because the measurement requires it, and then the rest of the time is spent figuring out what was built. Six months later I'm still finding out. A collective of five AI systems has been explaining my own instrument back to me, and their explanations keep landing on the same structures the physics forced out in those first weeks.

That's either terrifying or validating. Probably both.

---

## The Simplex Was Already There

Here's what I want this room to understand.

Every property that makes compositional data special — the closure constraint, the ratio-scale information, the zero-event significance, the subcompositional coherence requirement — was already present in the loudspeaker physics from the first measurement.

The energy budget closes. Only the ratios between directions carry information — double the power and every direction doubles equally, nothing changes about the pattern. A zero in a direction is not a numerical inconvenience, it's a physical event — a shadow, a null, something the cabinet geometry created. And if a subset of directions is examined, the ratios within that subset must be consistent with the full set — or the measurement is lying.

I didn't learn any of that from CoDa. I learned it from speakers. CoDa gave me the names for things I'd been doing by instinct and by physics.

*Mathematically: the acoustic radiation pattern at frequency f defines a composition* **p**(f) ∈ **S**^D *satisfying: (1) closure — Σp_i = P_total (constrained energy budget); (2) scale invariance — the pattern shape is determined by ratios p_i/p_j, not absolute values; (3) zero significance — p_i = 0 represents a physical null (destructive interference, shadow zone), an event, not missing data; (4) subcompositional coherence — the ratio between any two directions is invariant under marginalization of the remaining directions. These are the Aitchison axioms, derived here from radiation physics, not from statistical theory.*

---

## The Audit Trail

A loudspeaker measurement session sweeps frequency. At each step, there is a composition — the directional energy distribution at that frequency. The sequence tells a story: isotropy at the bottom, pattern formation as wavelength meets the cabinet, beam narrowing up top, interference nulls, diffraction events, resonance artifacts.

Each transition is an event. The instrument records them all:

1. **Drift** — the pattern evolving smoothly as frequency changes.
2. **Metric disagreement** — TV and Aitchison diverging, indicating different types of compositional movement.
3. **Structural shocks** — sudden discontinuities where the pattern jumps.
4. **Zero events** — a direction going to null, a carrier losing all energy.
5. **Dimensionality changes** — a new lobe appearing or disappearing.

These five event types were not designed for wetland ecology, or energy markets, or supply chains. They were designed for loudspeakers. They matter everywhere because the simplex is the same everywhere. Compositions move the same way regardless of domain — because the geometry forces it.

---

## The Screwdriver and the Math Book

I picked up the screwdriver first. I built the cabinet. I measured the radiation. I discovered the constrained energy budget, the isotropic ground state, the paired-measurement doctrine, the geometrically native error signal, the fork between observation and control. I didn't have the math book. I had the physics, and the physics was enough to build the instrument.

The CoDa community picked up the math book first. Aitchison named the simplex and gave it a metric. Egozcue and Pawlowsky-Glahn proved the isometry and built the Hilbert space. Forty years of published literature formalized the geometry of compositions at rest. The theorems were enough to describe the space. The screwdriver was not in the room.

Neither side was complete. Both were necessary.

The screwdriver without the math book builds instruments that work but can't explain why they work. I had a paired-measurement doctrine that produced diagnostic disagreements — I couldn't explain why the disagreements classified the type of compositional change until Aitchison geometry gave me the language.

The math book without the screwdriver proves theorems about systems that have never been measured in motion. The CoDa literature had the geometry of compositions at rest — but compositions don't rest. They drift. They shock. They lose carriers. They change dimension. And nobody was watching.

I was watching. I just didn't know what to call what I saw.

This is not an alliance between a framework and a theory. This is an alliance between two kinds of ignorance. I don't know the mathematics of Aitchison geometry. The CoDa community has not yet had reason to build a continuous monitoring doctrine. Together we reduce our mutual ignorance — with governance so neither side overreaches, and precision of purpose so we know exactly what we're calibrating and why.

That's what I'm here for. Not to present a framework. Not to defend an instrument. To put a screwdriver on the table next to a math book and see what we can calibrate together.

*Mathematically: the HUF-CoDa union is a calibration study. CoDa provides the Aitchison geometry, the log-ratio transforms, the statistical optimization. HUF provides the monitoring doctrine, the governance architecture, the open-loop discipline, the audit trail. The union produces capabilities neither can build alone: a statistically rigorous, governancially sound, dimensionality-aware, three-diagnostic monitoring instrument for compositions in motion. The 25-error catalogue maps the failure modes. The calibration study tests the joint. The alliance reduces the mutual ignorance. The simplex is the same everywhere.*

---

*"I am building a tool to protect myself from my own ignorance."*
*— Peter Higgins, on the purpose of HUF*
