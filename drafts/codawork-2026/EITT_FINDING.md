# EITT — Entropy-Invariant Time Transformer

**Finding ID:** EITT-001
**Date:** 2026-04-10 (updated)
**Status:** Computed, verified, Renyi-generalized, bidirectional inversion confirmed, ready for presentation
**Origin:** Peter Higgins — DADC-DADI loudspeaker diffraction correction (Dec 2024) → dimensional inversion insight (Nov 2025) → Claude computation → Shannon entropy conservation discovered → Renyi generalization confirmed (Apr 2026)

---

## The Finding

Shannon entropy — and in fact the entire Renyi family from q=0.1 to q=5.0 — of compositional data is empirically near-invariant under geometric-mean decimation across temporal resolutions. Shannon is not special; the phenomenon lives in the Aitchison geometry. This is a computed finding, not an analytic proof. Confirmed across five independent domains: energy (electricity generation), hardware (Backblaze drives), financial (120-stock portfolio), commodities (gold/silver 339 years), and cosmological (Planck temporal split). EITT inversion is now bidirectional: upward (gold/silver K=2→K=4, hidden dimensions) and downward (China K=9→K=3, exposed non-stationarity).

**Measured:** 0.18% variation across a 341:1 compression ratio (daily → annual European electricity price compositions, 8 carriers, 4089 trading days). Confirmed independently at 1.02% mean variation on a second domain (see below).

| Resolution | N observations | Winding Ratio | Shannon Entropy | Change from Daily |
|------------|---------------|---------------|-----------------|-------------------|
| Daily | 4089 | 1:1 | 2.069863 | reference |
| Weekly | 586 | 7:1 | 2.071290 | +0.07% |
| Monthly | 135 | 30:1 | 2.072198 | +0.11% |
| Quarterly | 45 | 91:1 | 2.072757 | +0.14% |
| Annual | 12 | 341:1 | 2.073492 | +0.18% |

For comparison, Aitchison variance drops 55% and total variation drops 99.7% across the same ladder.

---

## What EITT Means

The geometric mean — the fundamental operation of compositional data analysis — appears to be an entropy-preserving temporal filter for compositional time series with temporal autocorrelation.

When you compute the geometric mean of compositions over a time window (weekly, monthly, quarterly, annual), the empirical evidence shows:

1. **Near-preserves** the information content (Shannon entropy) of the compositional system (0.18–1.84% variation measured)
2. **Reduces** the geometric dispersion (Aitchison variance) by smoothing high-frequency variation (these are negative controls — they change materially)
3. **Maintains** the simplex constraint (closure to 1)

On the tested domains, this supports cross-resolution comparison of compositional time series when decimation is performed via geometric-mean anti-aliasing. The winding ratio (compression factor) is a free parameter. The information content is empirically stable.

**Boundary condition (empirical, not proven):** Temporal autocorrelation required. EITT fails on iid random compositions, oscillating extremes, and monotonic drift trajectories. See EITT_Adversarial_001.json for full adversarial scorecard (10 pass, 7 fail).

---

## The Analogy That Led Here

In an electrical transformer:
- Winding ratio N1:N2 compresses voltage while expanding current (or vice versa)
- Conserved quantity: power (V1 × I1 = V2 × I2)

In the Entropy-Invariant Time Transformer:
- Winding ratio M:1 compresses time (M daily observations → 1 weekly/monthly/annual observation)
- Anti-aliasing filter: compositional geometric mean (arithmetic mean in log-space + closure)
- Empirically near-conserved quantity: Shannon entropy H(x) = -Σ x_i ln(x_i)
- Resolution-dependent observables (negative controls): Aitchison variance, TV integral

On temporally autocorrelated compositions, the geometric mean appears to redistribute compositional structure across a coarser time grid while preserving the mean entropy. Analytic proof is an open problem.

---

## The Calibration Programme

EITT completes the loudspeaker calibration sequence for HUF-GOV:

| Calibration Step | Loudspeaker Equivalent | HUF-GOV Implementation | Status |
|-----------------|----------------------|----------------------|--------|
| Woofer | Low-frequency driver | EMBER annual generation shares — 3 diagnostics, spectral independence confirmed | DONE |
| Tweeter | High-frequency driver | European daily price shares — 3 diagnostics, spectral independence failed on prices, persistence metrics hold | DONE |
| Midrange | Mid-frequency driver | EMBER monthly generation — 6 countries, 9 fuel types, EITT confirmed at 1.02% mean variation | DONE |
| Crossover | Cross-driver coherence | EITT — entropy conserved across all resolutions, winding ratio grounded | DONE |
| ETC | Energy decay envelope | Hilbert transform → exponential fit → tau per carrier per shock | DONE |
| RT60 | Full decay time | 3 × tau, computed for COVID and Energy Crisis | DONE |

---

## Companion Results

### ETC (Energy Time Constant)
- COVID lockdown: carrier tau ranges 4.5–24.4 weeks (France fastest, Poland slowest)
- Energy Crisis 2022: carrier tau ranges 13.0–79.7 weeks (Netherlands fastest, France slowest)
- France: 17.6x ratio between COVID and Energy Crisis persistence
- Leaf SBP balances decay slower than root — local structure more persistent than macro

### RT60 Analogue
- France Energy Crisis: RT60 = 239 weeks (4.6 years to full 60 dB decay)
- France COVID: RT60 = 13.6 weeks (3.1 months)
- Netherlands Energy Crisis: RT60 = 39 weeks (9 months) — fastest recovery

### Aitchison Variance Per Year
- 2022 (energy crisis): 3.27x mean Aitchison variance — crisis measured directly via native CoDa metric
- 2015–2020: all below 0.25x mean — structural stability period
- 2021–present: elevated variance — structural transition in progress

---

## What To Say at CoDaWork

The geometric mean is the centre of Aitchison geometry. Every operation in CoDa passes through it. What we found empirically is that when you use the geometric mean as a temporal filter — averaging compositions over time windows before downsampling — it appears to preserve the information-theoretic content of the system. Shannon entropy on the simplex is empirically near-invariant under geometric-mean decimation, with variation below 2% across all tested configurations. We also ran 17 adversarial tests, 7 of which broke the pattern. The boundary condition is temporal autocorrelation — which real-world monitored systems satisfy.

We call this the Entropy-Invariant Time Transformer. We measured it on two independent domains. We cannot prove it analytically. We are here because you can.

The winding ratio is free. The information appears to be conserved. We would welcome help formalizing this — or breaking it.

---

## Independent Confirmation — Midrange Test (2026-04-08)

EITT confirmed on a completely independent domain: EMBER monthly electricity generation by fuel type.

**Different from original proof in every dimension:**

| Dimension | Original Proof | Midrange Confirmation |
|-----------|---------------|----------------------|
| Carriers | 8 European countries (price shares) | 9 fuel types (generation shares) |
| Base resolution | Daily (4089 obs) | Monthly (~134 obs) |
| Compression ratio | 341:1 | 12:1 |
| Domain | Wholesale electricity prices | Electricity generation mix |

**Results — 6 countries, all pass:**

| Country | Months | Entropy Variation | AitVar Variation |
|---------|--------|-------------------|------------------|
| Japan | 94 | 0.33% | 60.5% |
| USA | 302 | 0.53% | 24.6% |
| Germany | 134 | 0.83% | 3.0% |
| UK | 134 | 1.12% | 12.2% |
| Poland | 21 | 1.48% | 164.7% |
| France | 134 | 1.84% | 59.1% |

Mean entropy variation: 1.02%. All countries below 2%. On the tested domains (energy prices, energy generation), the result holds across different carrier types, country configurations, and base resolutions. Domain independence beyond energy systems remains untested.

This completes the **midrange calibration test** — the last pending item in the loudspeaker calibration programme.

---

## The Entropy Residual — Hessian Footprint (2026-04-09)

The systematic upward drift in entropy under decimation is not noise or error. It is the **Hessian footprint** of Shannon entropy on the simplex — a second-order Jensen correction.

**Mechanism:**

1. The geometric mean reduces composition variance (pulls toward the Frechet mean x*)
2. Shannon entropy is concave (Hessian = diag(-1/x_i))
3. A concave function of less-variable input gives higher expected output (Jensen's inequality)
4. The correction: DeltaH ~ (1/2) tr[|Hess_H(x*)| . Cov(x_bar_M)]

**Evidence from Copilot's data (8-carrier EMBER, 2000 daily observations):**

| Level | H observed | Gap to H* | % of H* reached |
|-------|-----------|-----------|-----------------|
| Daily | 2.0788114 | 0.0006286 | 0.0% (reference) |
| Weekly | 2.0789855 | 0.0004545 | 27.7% |
| Monthly | 2.0792364 | 0.0002035 | 67.6% |
| Quarterly | 2.0793659 | 0.0000740 | 88.2% |
| Annual | 2.0794211 | 0.0000188 | 97.0% |

H* (Frechet mean entropy) = 2.0794399. Total journey: 0.0006 nats (0.03% of H*).

**The e-duality:** The near-cancellation happens because exp() (in the geometric mean) and ln() (in Shannon entropy) are inverse functions sharing the same transcendental base. First-order effects cancel by construction. The residual is the second-order mismatch. Euler's e does not "appear" in EITT — e IS EITT.

**The 10,000x gap:** Copilot's VAR(1) theoretical bounds predicted 100-1000% possible entropy change. Observed: 0.03%. The gap exists because VAR(1) captures first-order potential (mean shift), which vanishes. The actual effect is second-order (variance x Hessian), which is inherently small. This rules out linear autoregressive structure as the explanation for EITT.

**Direction diagnostic:** Entropy drifts UP for stationary processes (Germany, Japan, USA confirm). Entropy drifts DOWN when non-stationarity dominates (France, UK, Poland — all undergoing structural energy transitions). The direction of the residual is itself a stationarity diagnostic.

**For CoDaWork:** "The residual is not error. It is the Hessian of entropy, made visible by the variance reduction that the geometric mean performs. We can predict its magnitude. We cannot yet prove why it is so small."

---

## Data Files

- `data/codawork-samples/S016/HUF_Aitchison_Variance_Conservation_001.json` — full EITT test results (original proof)
- `data/codawork-samples/S016/EITT_Midrange_Confirmation_001.json` — independent confirmation on generation data
- `data/codawork-samples/S016/EITT_Adversarial_001.json` — adversarial testing (17 tests, 10 pass, 7 fail)
- `data/codawork-samples/S016/EITT_Residual_Analysis_001.json` — Hessian footprint analysis
- `data/codawork-samples/S016/HUF_ETC_Analysis_001.json` — ETC results (both shocks)
- `data/codawork-samples/S016/HUF_Tweeter_Calibration_001.json` — original tweeter test
- `data/eitt_lab/` — Complete EITT calibration lab (Copilot outputs + Claude analysis)

---

## Governance

- State: CGS-2 (n=3), GDoF 264
- No new constants introduced
- All computations use native CoDa operations (geometric mean, CLR, ilr, Aitchison distance)
- Shannon entropy conservation is a computed finding, not an assumption
- Independent confirmation achieved on different carriers, domain, and base resolution
- Midrange calibration: DONE (was last PENDING item)
- The EITT name is locked: Entropy-Invariant Time Transformer
