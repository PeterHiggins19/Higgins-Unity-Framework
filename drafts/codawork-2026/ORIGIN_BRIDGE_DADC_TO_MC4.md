# From Loudspeaker to Simplex: How DADC-DADI Became MC-4

## The Engineering DNA of the Higgins Unity Framework

**Peter Higgins | Rogue Wave Audio | April 2026**

---

> **Terminology Key — CoDa vs HUF**
>
> *Standard CoDa terms* (Aitchison, Egozcue, Pawlowsky-Glahn et al.): simplex, closure constraint, Aitchison geometry/distance/metric, log-ratio transforms (ILR, CLR, ALR), perturbation, powering, subcompositional coherence, Sequential Binary Partition (SBP), geometric mean / Fréchet mean, compositional data analysis (CoDa).
>
> *HUF terms* (Higgins, Rogue Wave Audio): MC-4 (Composition Monitoring — the fourth monitoring category), EITT (Entropy Invariance under Temporal Transformation), DADC-DADI-ADAC (Dimension-Apportioned Diffraction Correction / Inference / Adaptive Closure), HUF-GOV (open-loop governance) / HUF-CLS (closed-loop system), carriers / carrier elements, K_eff (effective number of carriers = exp(H)), Total Variation (TV) as diagnostic, d(CoDa)/dt (balance velocity / adaptive decimation controller), deceptive drift, Ratio State Monitoring (RSM), BTL (Binaural Test Lab), the Isotropic Principle, "HUF is inert."

---

## The Isotropic Principle

Before the loudspeaker. Before the cabinet. Before the first measurement. The design principle: paint the inside of a sphere with radiation, uniformly. Every point receives equal energy. No direction privileged. The geometry of that sphere exists whether or not anything is radiating. The simplex is there before the signal. The structure precedes the measurement. Add a signal and you tune to the structure --- you reveal what was always there. This is the ground state of HUF: isotropic, maximum entropy, the composition (1/D, 1/D, ..., 1/D). Every departure from isotropy is a signal. Every return is relaxation. The geometry does not care what kind of energy paints the sphere.

## The Claim

Every concept in the Higgins Unity Framework --- MC-4 composition monitoring, EITT entropy invariance, bidirectional inversion, adaptive decimation, the "HUF is inert" principle --- traces its engineering DNA to this isotropic principle and its first physical realization: a loudspeaker diffraction correction method developed in the Rogue Wave Audio Binaural Test Lab in late 2024 through 2025. The method is called DADC-DADI-ADAC: Dimension-Apportioned Diffraction Correction, Dimension-Apportioned Diffraction Inference, and Apparent Dimension Apportioning Correction.

This document maps the direct conceptual lineage from the acoustic system to the compositional monitoring framework.

---

## Part 1: What DADC-DADI Actually Is

### The Physical Problem

A rectangular loudspeaker cabinet (the BTL: H=0.800 m, W=0.368 m, D=0.330 m) radiates sound omnidirectionally. When the wavelength of a sound is larger than the cabinet, the sound radiates into full 4-pi steradian space. When the wavelength is smaller than a dimension, that dimension creates a baffle step --- a 6.02 dB transition from 4-pi to 2-pi radiation. The question: how do you correct for this?

### The Insight: Apportion by Dimension

Peter's key insight was that the total baffle step correction (exactly 6.02 dB = 20*log10(2)) is a **fixed budget** that must be **apportioned among the physical dimensions** of the object. Each dimension receives a share of the total gain proportional to its contribution:

| Dimension | Length | Gain (G) | Corner Frequency (Fc) |
|-----------|--------|----------|-----------------------|
| Height | 0.800 m | 3.21 dB | 144 Hz |
| Width | 0.368 m | 1.48 dB | 312 Hz |
| Depth | 0.330 m | 1.33 dB | 348 Hz |
| **Total** | | **6.02 dB** | |

The gains always sum to 6.02 dB. The corner frequency for each dimension is 115/dimension (Hz*m constant). Every dimension's share is determined by its ratio to the sum of all dimensions.

### The Three Stages

**DADC (Forward):** Encode the cabinet geometry into its acoustic transfer function. The physical dimensions determine the proportional gain corrections. This is the forward mapping from geometry to composition.

**DADI (Inverse):** Given only the measured acoustic response, reconstruct the physical dimensions. If you know the gains and corner frequencies, you can infer H, W, and D. This is the inverse mapping --- from composition back to geometry.

**ADAC (Closure):** The adaptive feedback loop. Measure, infer, correct, re-measure. The loop converges (proved via Banach fixed-point theorem) because the mapping is contractive. DADI error reduces from 12.5% to 4.99% over 5 iterations. ADAC achieves RMSE < 0.05 dB.

### The Design Requirement: Inert Measurement

The entire DADC-DADI-ADAC chain was designed as a **non-contact diagnostic**. The acoustic probe reads the geometry of the object without imprinting its own signature on the result. The gains are determined by the object, not the probe. The measurement system is inert.

---

## Part 2: The Compositional Structure Hidden in Plain Sight

### The 6.02 dB Budget Is a Closure Constraint

The total correction is exactly 6.02 dB regardless of cabinet shape. This is the acoustic analogue of the simplex closure constraint: parts must sum to a constant (kappa = 1 for compositions, 6.02 dB for diffraction correction). The individual gains are the **proportional parts** of a fixed whole.

The DADC gain vector **is a composition**:

```
G_H / 6.02 = 0.533    (height's share)
G_W / 6.02 = 0.246    (width's share)
G_D / 6.02 = 0.221    (depth's share)
Sum        = 1.000    (closure)
```

### The Dominance Index Is a Log-Ratio

DADC classifies cabinets by their Dominance Index: D = max(H,W,D) / min(H,W,D). For the BTL, D = 0.800/0.330 = 2.424. This is a **pairwise log-ratio** --- the fundamental atom of compositional data analysis. The dominance index determines whether corrections are proportional (D > 2, "long"), reciprocal (D < 1.5, "short"), or hybrid (1.5 < D < 2).

In CoDa terms: the regime classification is determined by the Aitchison distance between the most extreme parts of the composition. Large ratios mean the composition is unbalanced (one dimension dominates). Small ratios mean near-uniformity.

### The Corner Frequency Is a Scale Parameter

Fc = 115/dimension (Hz*m). This maps each part's physical scale to a frequency --- a temporal scale. The larger the dimension, the lower the frequency where its correction kicks in. This is an early version of what became the EITT insight: **the relationship between physical scale and temporal scale is mediated by the compositional structure**.

### DADI Inversion Is EITT Inversion

DADI reconstructs dimensions from the acoustic response by inverting the gain ratios:

```
W/H = G_H / G_W    (ratio preserved)
D/H = G_H / G_D    (ratio preserved)
H = 115 / Fc_H     (absolute scaling from one corner frequency)
```

This is inversion on the simplex. The ratios between parts are recovered from the observed response, then anchored to absolute scale by a single reference measurement. When the inversion fails --- when the reconstructed dimensions don't match the physical cabinet --- it diagnoses a problem: either a hidden dimension (a driver the model didn't account for) or a non-stationary condition (the room changed between measurements).

This is exactly what EITT inversion does: when entropy invariance fails at dimension K, increase K (hidden dimensions) or decrease K (non-stationarity). The direction of the fix is diagnostic.

### The Banach Convergence Is the Stationarity Condition

ADAC converges because the mapping is contractive (Banach fixed-point theorem, |m| < 1). It fails to converge when the system is non-stationary --- when the room changes faster than the adaptation loop can track.

In EITT terms: geometric-mean decimation preserves entropy when the process is near-stationary within blocks. When the composition changes faster than the block width, the invariance breaks. The convergence condition is the same: the system must be slower than the observer.

---

## Part 3: The Generalization Chain

### From Cabinet to Composition

| DADC-DADI-ADAC | MC-4 / EITT |
|----------------|-------------|
| Cabinet dimensions (H, W, D) | Compositional parts (x_1, ..., x_D) |
| Total gain = 6.02 dB | Closure constraint: sum = kappa |
| Gain apportioned by dimension | Proportional share on the simplex |
| Dominance Index = max/min | Pairwise log-ratio |
| Corner frequency = 115/dim | Temporal scale = f(compositional dimension) |
| DADC forward mapping | Geometric-mean decimation (encode) |
| DADI inverse inference | EITT inversion (decode) |
| ADAC adaptive closure | Adaptive decimation via d(CoDa)/dt |
| Banach convergence | Stationarity within blocks |
| Acoustic probe is inert | HUF is inert |
| Transfer function linearity | Entropy near-invariance |
| Error < 0.05 dB RMSE | Error < 0.6% delta at 2:1 |

### What Changed

The generalization from DADC to MC-4 required three conceptual steps:

1. **From Euclidean to Aitchison geometry.** DADC works in dB space (logarithmic). The CoDa formalization made this explicit: the simplex has its own geometry where the geometric mean is the correct average and log-ratios are the natural coordinates. DADC was already working in the right space without naming it.

2. **From spatial to temporal.** DADC apportions corrections across spatial dimensions of a physical object. EITT apportions information preservation across temporal blocks of a time series. The scale parameter (115 Hz*m for DADC, compression ratio M for EITT) mediates the relationship between the compositional structure and the observation scale.

3. **From single object to arbitrary system.** A loudspeaker cabinet has 3 parts (H, W, D). An energy grid has 7-9 parts. A financial portfolio has hundreds. A wetland ecosystem has dozens of habitat types. The mathematics is the same. The simplex is the simplex regardless of dimension.

### What Didn't Change

The design principle survived intact: **the measurement system must not impart its own signature on the result.** DADC reads cabinet geometry from the acoustic response without touching the cabinet. HUF reads compositional drift from time series without transforming the data. The errors it finds were always there. It just made them readable.

---

## Part 4: The Constants That Carried Forward

Two constants from the BTL acoustic work survive unchanged into the full HUF framework:

**6.02 dB** --- the 2-pi to 4-pi radiation gain, equal to 20*log10(2). This is the acoustic expression of a binary doubling. In EITT terms, the 2:1 compression ratio (the simplest decimation) is the fundamental test. The residual at M=2 is the primary diagnostic.

**115 Hz*m** --- the wavenumber-dimension product that sets each part's corner frequency. This is the scale constant that links physical dimension to temporal frequency. In EITT, the equivalent is the relationship between block width M and the temporal autocorrelation length of the process.

These are not arbitrary parameters. They are physical constants of the acoustic system that became structural constants of the compositional framework. The framework didn't invent them. It inherited them from the physics.

---

## Part 5: The Timeline

| Date | Event | Document |
|------|-------|----------|
| Jun 2024 | AES paper draft begins | `aes doc.docx` |
| Dec 5, 2024 | DADC-DADI formal writeup | `Dimension-Apportioned Diffraction Correction and Inference (DADC-DADI).docx` |
| Dec 6, 2024 | DADI inverse method documented | Embedded in DADC-DADI docx (separate section) |
| Dec 21, 2024 | Full AES LaTeX manuscript | `DIMENSION-APPORTIONED DIFFRACTION CORRECTION 3.txt` |
| Jan-Feb 2025 | BTL Lab certification and measurement | BTL Certification, Design, Linear Design PDFs |
| Nov 2025 | Working with Grok --- DADC dimensional inversion loop recognized as general principle | Grok session (not recorded; confirmed by operator) |
| Late 2025 | HUF framework formalization begins | HUF repository initialized |
| Feb 2026 | Ratio State Monitoring name locked for literature submission | Operator approval |
| Mar 2026 | Organic Digital Loudspeakers v2.6 | `Organic_Digital_Loudspeakers_v2.6.docx` |
| Apr 2026 | EITT discovery, CoDa formalization, MC-4 positioning | EITT_CODA_MATHEMATICS.md, MASTER_SYNTHESIS.md |

The gap between December 2024 (DADC-DADI) and November 2025 (generalization insight with Grok) is the incubation period. Peter was building and certifying the BTL system, running acoustic measurements, and refining the ADAC feedback loop. The compositional insight emerged when he saw the dimensional inversion working and asked: what else can this principle do?

---

## Part 6: What This Means for the CoDa Presentation

The DADC-DADI origin story is not an anecdote. It is evidence that the compositional monitoring framework was **discovered empirically before it was formalized mathematically**. Peter was working with log-ratios, closure constraints, proportional apportioning, inversion diagnostics, and convergence conditions in an acoustic system before he had ever heard of Aitchison geometry.

This is significant because it demonstrates that:

1. **The compositional structure is real**, not imposed. A loudspeaker cabinet enforces its own simplex. The gains must sum to 6.02 dB because physics requires it. The CoDa framework isn't a mathematical convenience --- it's the geometry the data already lives in.

2. **The inversion principle is general.** DADI inversion (reconstruct dimensions from response) and EITT inversion (reconstruct dimensionality from entropy residual) are the same operation. Both diagnose hidden structure by checking what survives a forward-inverse cycle.

3. **The "inert measurement" principle has engineering provenance.** It's not a philosophical slogan. It's a design requirement from acoustic measurement: the probe must not contaminate its own reading. This requirement carried forward unchanged into the compositional monitoring framework.

4. **The constants are physical.** 6.02 dB and 115 Hz*m are not tuning parameters. They are properties of acoustic wave propagation. Their survival into the compositional framework suggests that the mathematical structures underlying MC-4 and EITT have physical roots deeper than the specific application domains.

---

## Closing

The Rogue Wave Audio Binaural Test Lab is where MC-4 was born, before it had a name, before it had a mathematical framework, before it had an ISO positioning document. It was born as a practical problem: how do you apportion a fixed correction budget across the dimensions of a physical object, read the result back from the acoustic response, and do it all without the measurement system leaving a fingerprint?

The answer to that question is the answer to every question MC-4 asks.

---

*Source files: `RogueWaveAudio/Dimension-Apportioned Diffraction Correction and Inference (DADC-DADI).docx`, `RogueWaveAudio/aes doc.docx`, `RogueWaveAudio/BTL/BTL Small Studio Lab/DIMENSION-APPORTIONED DIFFRACTION CORRECTION 3.txt`, `RogueWaveAudio/CODE/BTL_DADC_DADI_ADAC_Tool_v1_1_lazyhuman_quickstart_FIXED2.ipynb`*

*Cross-referenced with: Grok session records (April 10, 2026), EITT_CODA_MATHEMATICS.md, MASTER_SYNTHESIS.md, SCALING_ERROR_ARGUMENT.md*

*All BTL measurement data in repository: `RogueWaveAudio/BTL/BTL Small Studio Lab/`*
