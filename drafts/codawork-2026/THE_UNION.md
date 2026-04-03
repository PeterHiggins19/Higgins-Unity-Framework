# The Union

## Conjoining the CoDa ecosystem with the HUF ecosystem to transform a collection of separate compositional tools into a single instrument for the physical sciences

*Peter Higgins · April 2026 · CoDaWork 2026*

---

## The Problem Both Communities Have

CoDa has spent 40 years perfecting the mathematics of compositional data — Aitchison geometry, log-ratio transformations, subcompositional coherence, robust estimation, outlier detection. The tools are precise, proven, and elegant. They work beautifully on collected datasets.

HUF has spent 6 months discovering what happens when you try to monitor compositions continuously in real systems — energy grids, wetland ecosystems, transit networks, GDP — where the data never stops arriving, the system changes dimensionality, governance decisions intervene, and the question is not "what does this dataset reveal?" but "is this system drifting right now, and does anyone know?"

CoDa has the math but no monitoring doctrine. HUF has the monitoring doctrine but borrowed math. Neither is complete.

The MEWMA-CoDa control chart researchers (Tran, Nguyen, Zaidi, 2020–2025) are building the bridge from CoDa's side — taking Aitchison geometry into continuous monitoring using statistical process control. They have already encountered problems HUF predicted: stored energy in the instrument (MEWMA accumulation), sampling rate sensitivity (VSI schemes), and out-of-control pattern diagnosis (neural network post-processing). They are solving these problems statistically.

HUF encountered the same problems from the engineering side and solved them differently: no stored energy (open-loop doctrine), governance-referenced alarms (not statistical control limits), and coherence chain diagnosis (not neural network pattern matching).

The union is not HUF adopting CoDa or CoDa adopting HUF. The union is recognizing that both communities are building the same instrument from opposite ends, and connecting them produces something neither can build alone.

---

## What Each Brings

### CoDa provides to HUF:

| Contribution | What it fixes in HUF |
|---|---|
| Aitchison geometry (distance, perturbation, inner product) | HUF was using TV distance — wrong geometry on the simplex (E-01) |
| Subcompositional coherence | HUF analyzed subsets without consistency guarantee (E-09) |
| Log-ratio transforms (CLR, ILR) | Maps simplex to real space where standard statistics work |
| Robust estimation (MCD, robCompositions) | Outlier handling that respects simplex structure |
| Optimal ARL calculation (MEWMA-CoDa) | Statistical power that HUF's governance thresholds don't provide |
| SVDD for non-Gaussian compositions | Alarm boundaries for compositions that aren't Dirichlet-distributed |
| Variable Sampling Interval (VSI) | Adaptive sampling rates HUF hasn't formalized |
| 40 years of peer-reviewed theory | Legitimacy HUF cannot earn alone in 6 months |

### HUF provides to CoDa:

| Contribution | What it fixes in CoDa |
|---|---|
| Governance reference management | CoDa has no concept of "authorized composition" — who declares the reference, when is it updated (E-06) |
| Open-loop doctrine (LOOP-001) | CoDa control charts accumulate state without auditing it (E-10, E-14) |
| Stored energy audit | MEWMA smoothing constant λ is a governance decision, not just a statistical parameter |
| Multi-domain scalability | Same instrument architecture from energy to wetlands to GDP — CoDa applications are domain-siloed |
| Dimensionality change as event | CoDa has no framework for compositions that gain or lose parts over time (E-11) |
| Zeros as events, not nuisances | A carrier going to zero is potentially the most important signal, not a data cleaning problem (E-03) |
| Kill test (19 failure modes) | CoDa control charts have no published failure mode catalogue |
| Coherence chain (1→2→4) | Physically motivated SBP from system hierarchy, not analyst convenience (E-04) |
| Dual-metric diagnostic | TV vs Aitchison disagreement as a signal, not a problem (E-01, E-12) |
| Compositional Nyquist test | Halve the interval, check for new events — no CoDa formalization exists (E-07) |

---

## What Only the Union Produces

These capabilities exist in neither system alone:

### 1. A statistically optimal AND governancially sound monitoring instrument

MEWMA-CoDa optimizes ARL (average run length) — the statistical trade-off between false alarms and missed detections. HUF's governance framework asks: what is the *cost* of a false alarm vs the *cost* of a missed event in this specific domain? In energy monitoring, a false alarm means unnecessary investigation. In wetland monitoring, a missed event means irreversible species loss. The optimal λ is different not because the math is different but because the stakes are different. The union uses CoDa's ARL optimization to set the statistical floor, then HUF's governance doctrine to set the operational ceiling.

### 2. Multi-carrier interaction monitoring at global scale

CoDa control charts monitor single processes — one production line, one chemical reactor, one European plant. HUF monitors systems where multiple carrier groups interact across scales — national energy grids where 6 carriers interact across 25 years, 172 Ramsar Convention countries where species compositions interact across 2,500 wetlands. The coherence chain (1→2→4) provides the hierarchical structure: group coherence gates inter-group analysis. A MEWMA-CoDa chart on each carrier group, governed by HUF's coherence protocol, produces an instrument that detects drift within groups AND structural change between groups.

### 3. A calibrated entanglement with documented error sources

The entanglement error analysis (companion document) identifies 17 error sources — 12 mapped across HUF-alone, CoDa-alone, and the union, plus 5 discovered during literature cross-reference and collective review. Every error source has a detection test and a governance action. No existing CoDa tool or HUF tool has a published error catalogue of this kind. The union is the first compositional monitoring instrument that ships with its own calibration study.

### 5. A calibrated zero-handling protocol (Greenacre complementarity)

Greenacre's chiPower framework addresses the zero problem through power-transform methods that preserve subcompositional coherence while avoiding classical imputation artifacts. HUF's E-03 zeros-tension analysis approaches the same inadequacy from the monitoring doctrine direction: a carrier reaching exactly zero is first treated as a domain event (phase transition, extinction, market exit) before any geometric correction is applied. The two positions are complementary rather than opposing — both reject classical replacement as insufficient, one for mathematical fidelity, the other for observational fidelity. The union therefore gains a zero-handling protocol that respects both statistical rigor and monitoring priority (E-17).

### 4. Dimensionality-aware time series

CoDa cannot compare compositions of different dimension. Real systems change dimension. The union tracks dimensionality changes as structural events — splitting the time series at transitions, analyzing each epoch internally, and characterizing the transition itself. This is the compositional equivalent of detecting a phase change in physics: the state space itself transformed.

---

## The Architecture

```
                    THE UNION — INSTRUMENT ARCHITECTURE

    ┌─────────────────────────────────────────────────────────┐
    │                    SYSTEM (physical)                     │
    │  Energy grid · Wetland · GDP · Transit · Any domain      │
    │  with a conserved whole divisible into meaningful parts   │
    └────────────────────────┬────────────────────────────────┘
                             │
                        raw data flow
                             │
    ┌────────────────────────▼────────────────────────────────┐
    │              TRANSFORM LAYER (CoDa)                      │
    │                                                          │
    │  Closure check → Zero event detection → ILR/CLR          │
    │  Carrier admission audit (KILL-1.1)                      │
    │  SBP from coherence chain (1→2→4), not convenience       │
    └────────────────────────┬────────────────────────────────┘
                             │
                     transformed vectors
                             │
    ┌────────────────────────▼────────────────────────────────┐
    │              METRIC LAYER (CoDa + HUF)                   │
    │                                                          │
    │  Aitchison distance    ─┐                                │
    │  TV distance            ├─ dual-metric diagnostic        │
    │  Metric disagreement   ─┘                                │
    │                                                          │
    │  Perturbation velocity v(t) = d_A(x(t), x(t−1))         │
    │  K_eff = exp(−Σ xᵢ ln xᵢ)  (effective carriers)        │
    │  ILR balances per coherence chain hierarchy              │
    │  MEWMA accumulated statistic (labeled: STORED ENERGY)    │
    │  Hotelling T² or SVDD boundary                           │
    └────────────────────────┬────────────────────────────────┘
                             │
                    metric outputs (stateless + stateful)
                             │
    ┌────────────────────────▼────────────────────────────────┐
    │              ALARM LAYER (HUF governance)                │
    │                                                          │
    │  Reference: declared composition (governance-set)        │
    │  Statistical floor: ARL-optimized control limit (CoDa)   │
    │  Operational ceiling: domain cost function (HUF)         │
    │                                                          │
    │  Alarm if: metric exceeds BOTH floors                    │
    │  Diagnosis: which carrier group? (coherence chain)       │
    │            which variable? (neural net, optional)        │
    │                                                          │
    │  Stored energy audit: is MEWMA state influencing alarm?  │
    │  Nyquist check: is sampling rate sufficient?             │
    │  Dimensionality check: did a carrier enter or exit?      │
    └────────────────────────┬────────────────────────────────┘
                             │
                        alarm / no alarm
                             │
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼──────────┐        ┌────────▼─────────┐
    │   huf-gov            │        │   huf-cls          │
    │   OPEN LOOP          │        │   CLOSED LOOP      │
    │                      │        │                    │
    │   Instrument reads.  │        │   System acts.     │
    │   Human decides.     │        │   Breakers armed.  │
    │   LOOP-001.          │        │   CL-01 to CL-05.  │
    │                      │        │   KILL-001 active.  │
    │   DEFAULT MODE       │        │   REQUIRES CONSENT  │
    └──────────────────────┘        └────────────────────┘
```

---

## The Path to Deployment

### Phase 1 — Coimbra (June 2026)
Present the union thesis. Show the 17-error calibration study. Demonstrate v3 analyzer with dual metrics on EMBER data. Identify CoDa researchers interested in continuous monitoring. Identify MEWMA-CoDa researchers (Tran, Nguyen group) for direct collaboration.

### Phase 2 — Validation (2026–2027)
Joint paper with CoDa co-author(s): formal comparison of MEWMA-CoDa and HUF on the same dataset (EMBER Germany, known ground truth). Quantify: does governance reference management improve detection over statistical reference estimation? Does dual-metric diagnostic catch events that single-metric charts miss? Does coherence chain diagnosis outperform neural network diagnosis in interpretability?

### Phase 3 — Ramsar Pilot (2027–2028)
Deploy the union instrument on Ramsar Convention wetland data. 172 countries, 2,500 wetlands, compositional species data already being collected. CoDa provides the transform layer. HUF provides the governance layer. MEWMA-CoDa provides the statistical power. The coherence chain monitors species composition within wetlands AND structural change across the network.

### Phase 4 — Instrument Standard
Publish the union instrument specification: transform protocol, metric protocol, alarm protocol, error catalogue, governance requirements. Open-source. MIT license. The instrument that reads. The human decides.

---

## One Sentence

CoDa perfected the geometry of compositions at rest; HUF discovered what happens when compositions move; the union is the instrument that watches them move and tells you when to care.

---

*This document is the thesis statement for CoDaWork 2026. All supporting materials are in this folder: [ENTANGLEMENT_ERROR_ANALYSIS.md](ENTANGLEMENT_ERROR_ANALYSIS.md) (17 error sources), [CODA_LITERATURE_CROSS_REFERENCE.md](CODA_LITERATURE_CROSS_REFERENCE.md) (what CoDa knows vs what HUF reveals), [THE_CORE.md](THE_CORE.md) (coherence chain), [FORMULA_REFERENCE.md](FORMULA_REFERENCE.md) (all formulas), [BATTLE_CARD.md](BATTLE_CARD.md) (honest answers to hard questions), [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) (metaphors for non-specialists).*
