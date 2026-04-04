# CoDa Literature Cross-Reference to HUF–CoDa Entanglement Errors

## What the literature knows, what it doesn't, and what HUF reveals

*Peter Higgins · April 2026 · CoDaWork 2026 preparation*
*Companion to [ENTANGLEMENT_ERROR_ANALYSIS.md](ENTANGLEMENT_ERROR_ANALYSIS.md)*

This document maps each error source from the HUF–CoDa entanglement analysis against published CoDa literature. For each: what has CoDa already said about it, what remains unresolved, and what HUF's continuous monitoring perspective adds that the literature has not yet considered.

---

## E-01 — Wrong Geometry on the Simplex

### CoDa literature status: SOLVED (1986)

This is the founding problem. Aitchison (1986) demonstrated that Euclidean operations on the simplex produce spurious results — negative values, violated constraints, distorted distances. The Aitchison geometry (inner product, distance, perturbation) provides the correct metric space. Pawlowsky-Glahn and Egozcue formalized the Hilbert space structure of the simplex in 2001.

**Key references:**
- Aitchison, J. (1986). *The Statistical Analysis of Compositional Data.* Chapman & Hall.
- Pawlowsky-Glahn, V. & Egozcue, J.J. (2001). Geometric approach to statistical analysis on the simplex. *Stochastic Environmental Research and Risk Assessment*, 15(5), 384–398.
- Egozcue, J.J. et al. (2003). Isometric logratio transformations for compositional data analysis. *Mathematical Geology*, 35(3), 279–300.

**What CoDa knows:** The simplex has its own geometry. Euclidean methods don't work there. Aitchison distance is the natural metric.

**What HUF adds:** HUF was using TV distance (information-theoretic, Euclidean-adjacent) before encountering CoDa. The dual-metric engine in v3 now runs both TV and Aitchison on the same data. Where they agree, the signal is robust to geometry choice. Where they disagree, the divergence itself is diagnostic — it tells you whether the detected event is dominated by large carriers (TV-visible) or trace carriers (Aitchison-visible). No CoDa paper has proposed using metric disagreement as a diagnostic signal. CoDa treated this as a solved problem; HUF treats the solution as generating a new observable.

---

## E-02 — Closure Bias (Spurious Correlation)

### CoDa literature status: SOLVED in theory, PERSISTENT in practice

Karl Pearson identified spurious correlation in constrained data in 1897. Aitchison's logratio approach eliminates it when used correctly. But the problem persists in applied work — researchers routinely mix raw proportions with logratio results, or apply standard statistics to raw compositions without transformation.

**Key references:**
- Pearson, K. (1897). Mathematical contributions to the theory of evolution — on a form of spurious correlation. *Proceedings of the Royal Society*, 60, 489–498.
- Aitchison, J. (1986). Chapter 3: The difficulty with raw compositional data.
- Greenacre, M. et al. (2023). Aitchison's Compositional Data Analysis 40 Years On: A Reappraisal. *Statistical Science*, 38(3), 386–410. [Project Euclid](https://projecteuclid.org/journals/statistical-science/volume-38/issue-3/Aitchisons-Compositional-Data-Analysis-40-Years-on-A-Reappraisal/10.1214/22-STS880.short)

**What CoDa knows:** Work in logratio space and the problem goes away. The mathematics is settled.

**What HUF adds:** In continuous monitoring, the instrument pipeline has multiple stages — data ingestion, normalization, transformation, metric computation, visualization, governance decision. Closure bias can re-enter at any stage where raw proportions leak into a step that expects logratio inputs. HUF's governance framework (LOOP-001) requires documenting every transformation in the pipeline. This is an engineering discipline CoDa hasn't needed because CoDa typically processes complete datasets in a single analytical pass, not streaming data through a multi-stage instrument.

**New concern for CoDa:** Pipeline contamination — closure bias that enters through mixed-space operations in multi-stage workflows, not from ignorance of the theory.

---

## E-03 — Zero Replacement Artifact

### CoDa literature status: ACTIVE OPEN PROBLEM

This is arguably CoDa's most debated issue. The log-ratio framework requires strictly positive data. Real data have zeros — both "rounded zeros" (below detection limit) and "structural zeros" (genuinely absent component). The literature offers multiple replacement strategies, none universally satisfactory.

**Key references:**
- Martín-Fernández, J.A. et al. (2003). Dealing with zeros and missing values in compositional data sets using nonparametric imputation. *Mathematical Geology*, 35(3), 253–278. [Springer](https://link.springer.com/article/10.1023/A:1023866030544)
- Palarea-Albaladejo, J. & Martín-Fernández, J.A. (2015). zCompositions — R package for multivariate imputation of left-censored data under a compositional approach. *Chemometrics and Intelligent Laboratory Systems*, 143, 85–96.
- Greenacre, M. (2024). The chiPower transformation: a valid alternative to logratio transformations in compositional data analysis. *Advances in Data Analysis and Classification*, 18(3). [Springer](https://link.springer.com/article/10.1007/s11634-024-00600-x)
- Lubbe, S. et al. (2021). Comparison of zero replacement strategies for compositional data with large numbers of zeros. *Chemometrics and Intelligent Laboratory Systems*, 210. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0169743921000162)

**Current state of debate:**
- Multiplicative replacement (Martín-Fernández 2003): widely used, preserves ratios among non-zero parts, but the replacement value is arbitrary.
- Bayesian-multiplicative (Palarea-Albaladejo 2015, zCompositions): more principled, uses detection limit information, but still imputes values that weren't observed.
- chiPower transformation (Greenacre 2024): sidesteps the problem entirely by using power transforms instead of log-ratios, permitting zeros. Achieves "quasi-coherence" rather than exact subcompositional coherence.
- Structural zeros remain unsolved: "there is no general method for dealing with the structural zero" (Martín-Fernández 2003).

**What CoDa knows:** This is an active research front. No consensus solution exists for structural zeros. The community is split between "replace then transform" (classical) and "use different transforms that tolerate zeros" (Greenacre).

**What HUF adds:** In continuous monitoring, a zero is an event — a carrier disappeared. That's not a statistical nuisance to be replaced; it's potentially the most important thing that happened. HUF's governance framework treats carrier absence as a structural event (related to KILL-1.1 and dimensionality change, E-11). Replacing a real zero with a small positive value to keep the math happy is exactly the kind of instrument-generated signal HUF is designed to prevent.

**New concern for CoDa:** Zero replacement may mask the most important events in time series monitoring. A carrier going to zero is a phase transition, not a data cleaning problem. CoDa's mathematical necessity to avoid zeros is in direct tension with monitoring's need to detect absence.

---

## E-04 — Partition Choice Bias (SBP/ILR)

### CoDa literature status: ACKNOWLEDGED but UNDEREXPLORED

The ILR transformation requires choosing a Sequential Binary Partition. The literature acknowledges that infinitely many valid SBPs exist and that the choice affects interpretability, but treats the choice as a domain-knowledge decision, not an error source.

**Key references:**
- Egozcue, J.J. et al. (2003). Isometric logratio transformations for compositional data analysis. *Mathematical Geology*, 35(3), 279–300.
- Pawlowsky-Glahn, V. & Egozcue, J.J. (2011). Exploring compositional data with the CoDa-dendrogram. *Austrian Journal of Statistics*, 40(1&2), 103–113. [PDF](https://www.stat.tugraz.at/AJS/ausg111+2/111+2Pawlowsky.pdf)
- Fišerová, E. & Hron, K. (2011). On the interpretation of orthonormal coordinates for compositional data. *Mathematical Geosciences*, 43, 455–468.

**What CoDa knows:** ILR coordinates depend on basis choice. Different SBPs emphasize different contrasts. The CoDa-dendrogram helps visualize balance structure. But "the interpretation of ilr coordinates might be more tricky than in the case of clr coefficients as there are infinitely many possibilities" (Fišerová & Hron 2011). The main criterion is interpretability, not robustness.

**What HUF adds:** In continuous monitoring, the SBP is not just an analytical convenience — it defines the alarm structure. If the partition groups fossil vs non-fossil energy, balances trigger when that boundary shifts. If the partition groups dispatchable vs non-dispatchable, the same data triggers different alarms. HUF's 1→2→4 coherence chain provides a physically motivated SBP: the system's own hierarchical structure dictates the partition. But HUF also requires a robustness test: compute balances under alternative SBPs. If the alarm only exists under one partition, it's a partition artifact, not a system event.

**New concern for CoDa:** Partition sensitivity testing should be standard practice, not optional. In static analysis, a poor SBP gives less interpretable coordinates. In continuous monitoring, a poor SBP gives false alarms or missed alarms. The stakes are different.

---

## E-05 — Geometric Mean Flattening

### CoDa literature status: KNOWN but ACCEPTED as trade-off

The CLR transformation uses the geometric mean of all components as the denominator. This means every carrier contributes equally to the reference point, regardless of magnitude or relevance.

**Key references:**
- Aitchison, J. (1986). CLR, ALR, and ILR definitions and properties.
- Greenacre, M. (2019). Variable selection in compositional data analysis using pairwise logratios. *Mathematical Geosciences*, 51, 649–682.
- Greenacre, M. et al. (2023). Reappraisal, Section 4: "The chiPower transformation... each identified with single compositional parts, not ratios."

**What CoDa knows:** CLR is not a true coordinate system (the transformed values are linearly dependent — they sum to zero). The geometric mean gives equal weight to all parts. ALR avoids this by using a specific reference part, but loses symmetry. ILR balances avoid both problems but require the SBP choice. Greenacre's pairwise logratios approach avoids the geometric mean entirely by working with selected ratios.

**What HUF adds:** In a governance context, not all carriers are equally important. A 0.1% trace carrier has no governance relevance but shifts every CLR value when it enters or leaves. HUF's governance reference (the "1" in 1→2→4) provides a natural ALR denominator — the total generation, the microphone reference, the conserved whole. Using the governance reference as ALR denominator aligns the mathematical reference with the physical reference.

**New concern for CoDa:** The geometric mean is scale-democratic when not all parts deserve equal democratic weight in a monitoring context. CLR is appropriate for exploratory analysis where all parts are equally interesting. It's inappropriate for alarm systems where some parts matter more than others.

---

## E-06 — Stale Reference / Anchor Drift

### CoDa literature status: NOT ADDRESSED

CoDa is overwhelmingly applied to static datasets — geological samples, chemical assays, microbiome snapshots, time-use surveys. The concept of a "reference composition" that must be maintained and updated as part of a governance process does not exist in CoDa literature.

**Key references:** None found. This is a gap.

The closest analogue is the MEWMA-CoDa control chart literature (see E-07 below), which uses a target mean vector, but even there the reference is estimated from in-control Phase I data, not governed.

**What CoDa knows:** Nothing about this problem. It doesn't arise in static analysis.

**What HUF adds:** This is entirely HUF's contribution. In continuous monitoring, the reference composition is the "authorized" state — the declared proportional balance that governance has approved. Drift from this reference triggers investigation. But if the system legitimately transitions (policy change, structural reform) and the reference isn't updated, every subsequent reading shows "drift" that is really a stale reference. This is a governance error, not a mathematical error, and it requires a governance protocol (LOOP-001), not a statistical fix.

**New concern for CoDa:** If CoDa methods are applied to continuous monitoring (which the control chart literature is beginning to do), reference management becomes critical. Who declares the reference? When is it updated? What constitutes "authorized" vs "unauthorized" change? CoDa has no framework for this. HUF does.

---

## E-07 — Temporal Aliasing

### CoDa literature status: EMERGING (2023–2025)

Compositional time series is a young subfield. Most CoDa work treats compositions as independent observations. Recent work on control charts, forecasting, and ordinal CoDa time series is beginning to address temporal structure.

**Key references:**
- Weiß, C.H. (2024). Ordinal compositional data and time series. *Statistical Modelling*, 24(1). [SAGE](https://journals.sagepub.com/doi/full/10.1177/1471082X231190971)
- Nguyen, T.T.V. et al. (2025). SVDD control charts based on MEWMA technique for monitoring compositional data. *Computers & Industrial Engineering*. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0360835225000105)
- Shang, H.L. (2024). Weighted compositional functional data analysis for modeling and forecasting life-table death counts. *Journal of Forecasting*. [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/for.3171)
- CoDaWork2024 process monitoring session (Girona, 2024): neural network integration for out-of-control signal detection in compositional data.

**What CoDa knows:** Control charts for compositional data exist (MEWMA-CoDa, Hotelling T² with ILR). These use Aitchison geometry correctly. Variable sampling interval (VSI) schemes have been studied. But the fundamental question of compositional Nyquist — at what sampling rate does temporal aliasing corrupt the signal — has not been formalized.

**What HUF adds:** Perturbation velocity v(t) = d_A(x(t), x(t−1)) is meaningful only if the sampling interval captures the system dynamics. Annual EMBER data shows smooth transitions; monthly data would show seasonal oscillations; daily data would show dispatch volatility. The same system looks like smooth drift or wild oscillation depending on sampling rate. HUF proposes: halve the interval and check. If new events appear, you're aliased.

**New concern for CoDa:** Compositional Nyquist. The control chart literature assumes the sampling interval is appropriate, but provides no test for whether it is. HUF's velocity metric provides a natural test: if velocity doubles when interval halves, the original interval was insufficient.

---

## E-08 — Carrier Admission Error

### CoDa literature status: PARTIALLY ADDRESSED (subcomposition selection)

CoDa recognizes that the choice of which parts to include in a composition matters. Subcomposition coherence ensures that analysis of a subset is consistent with the full composition. But the question of whether a part *should* be included — domain justification for carrier admission — is treated as a pre-analytical decision, not a source of mathematical error.

**Key references:**
- Aitchison, J. (1986). Subcompositional coherence principle.
- Greenacre, M. (2019). Variable selection in compositional data.
- Greenacre, M. (2024). Amalgamation and amalgams for dimensionality reduction.

**What CoDa knows:** You can analyze subcompositions coherently. Amalgamation (combining parts) is valid. Variable selection methods exist. But these address "which parts are informative?" not "which parts are legitimate?"

**What HUF adds:** KILL-1.1 — carrier admitted without domain justification. In CoDa terms, adding a part to the composition changes the simplex dimension, which restructures all distances, log-ratios, and balances. In static analysis, this is an analytical choice. In continuous monitoring, it's a structural event that changes what the instrument can detect. HUF requires domain justification for every carrier and sensitivity testing: remove the carrier, recompute. If conclusions change, the carrier matters and its inclusion must be defended.

**New concern for CoDa:** Carrier admission should have a formal justification protocol, not just statistical variable selection. In monitoring, an unjustified carrier doesn't just reduce power — it changes the alarm structure.

---

## E-09 — Subcomposition Incoherence

### CoDa literature status: SOLVED (1986, refined 2023)

This is CoDa's signature contribution. The principle of subcompositional coherence guarantees that analysis of a subset of parts is consistent with analysis of the full composition, provided logratio methods are used.

**Key references:**
- Aitchison, J. (1986). The principle of subcompositional coherence.
- Egozcue, J.J. & Pawlowsky-Glahn, V. (2023). Subcompositional coherence and a new proportionality index of parts. *SORT*, 47(2), 229–244. [PDF](https://www.idescat.cat/sort/sort472/47.2.2.Egozcue-Glahn.pdf)
- Greenacre, M. et al. (2023). Reappraisal: argues "quasi-coherence" is sufficient; exact coherence unnecessary for practical purposes.

**What CoDa knows:** This is thoroughly understood. The 2023 debate between exact coherence (Egozcue/Pawlowsky-Glahn) and quasi-coherence (Greenacre) is active but technical, not fundamental.

**What HUF adds:** HUF was violating subcompositional coherence before CoDa integration (using TV distance on raw proportions for subcompositions). CoDa fixes this. This is one of the two errors (with E-01) that the union corrects rather than inherits. HUF acknowledges this openly.

**No new concern for CoDa.** HUF is the beneficiary here.

---

## E-10 — Instrument Memory (Stored Energy)

### CoDa literature status: NOT ADDRESSED

CoDa methods are stateless transformations. CLR(x) depends only on x. Aitchison distance d_A(x,y) depends only on x and y. There is no concept of instrument state, memory, or accumulated bias in CoDa's mathematical framework.

**Key references:** None found. The concept does not exist in CoDa literature.

The closest analogue is the MEWMA (Multivariate Exponentially Weighted Moving Average) control chart, which by definition carries forward a weighted history of past observations. The MEWMA-CoDa literature (Tran et al., 2020; Nguyen et al., 2025) uses this accumulated state to detect persistent small shifts — but does not discuss whether the accumulated state itself can become a source of error.

**What CoDa knows:** Nothing. This is an engineering concern that hasn't arisen in CoDa's application domains.

**What HUF adds:** This is HUF's core design principle. Open-loop means no stored energy in the instrument. Every reading must be computable from current observation + declared reference only. When you add a rolling baseline, an exponential moving average, or a historical anomaly buffer, the instrument acquires memory — it starts responding partly to its own past outputs rather than purely to the system. In PLL terms, this is the difference between a phase detector (stateless comparator) and a VCO (oscillator with inertia). HUF's LOOP-001 doctrine requires clear separation: raw metrics are stateless; trend analysis is a labeled governance overlay, not part of the instrument.

**New concern for CoDa:** As CoDa moves into control charts and real-time monitoring, the instruments will inevitably accumulate state (MEWMA already does). The literature needs to distinguish between the instrument's mathematical state and the system's physical state. Conflating them is the monitoring equivalent of closure bias — a constraint artifact masquerading as a system property.

---

## E-11 — Dimensionality Mismatch Over Time

### CoDa literature status: ACKNOWLEDGED as OPEN PROBLEM

Real compositions change dimensionality. New species appear. Energy sources emerge. Industries are created or destroyed. CoDa's log-ratio framework requires consistent dimensionality — you cannot compute d_A between a point in S³ and a point in S⁴.

**Key references:**
- No dedicated paper exists on this specific problem.
- Wang, H. et al. (2020). A classification framework for multivariate compositional data with Dirichlet feature embedding. *Knowledge-Based Systems*. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0950705120307437) — notes that "methods for multivariate compositional data variables with unequal sizes of parts are not sufficiently investigated."
- Amalgamation (Greenacre 2019, 2024) is the standard workaround: combine parts to restore consistent dimension. But amalgamation destroys information about the parts being combined.

**What CoDa knows:** This is a known gap. Amalgamation is the workaround. No principled framework exists for comparing compositions of different dimensions across time.

**What HUF adds:** In continuous monitoring, dimensionality changes are structural events — a new carrier appeared (solar energy in the 1990s), or an old carrier vanished (whale oil in the 1900s). These are not statistical problems to be papered over with amalgamation. They are the most important events the instrument can detect: the system changed its structure. HUF proposes treating dimensionality changes as first-class events: split the time series at the transition, analyze each epoch internally, and characterize the transition itself (which carriers entered or exited, what happened to the remaining balance).

**New concern for CoDa:** Dimensionality change is not a data problem — it's a system event. Amalgamation to restore consistent dimension is mathematically convenient but hides the very phenomenon monitoring is designed to detect. CoDa needs a framework for comparing compositions across structural transitions, not just within stable epochs.

---

## E-12 — Outlier Masking in Aitchison Space

### CoDa literature status: WELL-STUDIED for static data

Outlier detection in compositional data using robust methods has been studied extensively, primarily by Filzmoser and colleagues. The MCD (Minimum Covariance Determinant) estimator applied in ILR space, combined with robust Mahalanobis distances, is the standard approach.

**Key references:**
- Filzmoser, P. & Hron, K. (2008). Outlier detection for compositional data using robust methods. *Mathematical Geosciences*, 40, 233–248. [Springer](https://link.springer.com/article/10.1007/s11004-007-9141-5)
- Filzmoser, P. et al. (2009). Principal component analysis for compositional data with outliers. *Environmetrics*, 20(6), 621–632.
- R package: robCompositions (Templ, Hron, Filzmoser) — comprehensive robust CoDa toolkit.

**What CoDa knows:** Log-ratio transforms compress large values and expand small values. Outlier detection methods exist but are designed for cross-sectional data (identifying unusual samples), not temporal data (identifying unusual transitions).

**What HUF adds:** The dual-metric engine turns this compression into a diagnostic. Where TV distance shows a large event but Aitchison shows small → a dominant carrier moved (log compression minimized it). Where Aitchison shows large but TV shows small → a trace carrier moved (log expansion amplified it). The divergence between metrics tells you what kind of event occurred — dominant shift vs trace shift — without needing to identify outliers. This is a temporal diagnostic that has no equivalent in CoDa's cross-sectional outlier framework.

**New concern for CoDa:** Robust methods designed for identifying unusual samples need adaptation for identifying unusual transitions in time series. An observation that is a statistical outlier in cross-section might be a perfectly natural intermediate state in a transition. Conversely, an observation that looks normal in cross-section might represent an unprecedented rate of change.

---

## NEW: Concerns Not in Our Original Error Analysis

The literature review revealed additional issues that HUF–CoDa should track:

### E-13 — The Greenacre Quasi-Coherence Debate

**Status:** Active debate since 2023.

Greenacre et al. (2023) argue that exact subcompositional coherence is unnecessary — "quasi-coherence is sufficient." This opens CoDa to simpler transforms (chiPower, Box-Cox) that tolerate zeros but don't guarantee exact coherence. Egozcue and Pawlowsky-Glahn (2023) disagree, arguing that coherence is a principle, not a convenience.

**HUF implication:** If CoDa relaxes coherence, the mathematical guarantee behind E-09's correction disappears. HUF adopted CoDa partly for its coherence guarantees. If those become "approximate," HUF needs to quantify the approximation error. A new error source enters the instrument.

**References:**
- Greenacre, M. et al. (2023). [Reappraisal](https://projecteuclid.org/journals/statistical-science/volume-38/issue-3/Aitchisons-Compositional-Data-Analysis-40-Years-on-A-Reappraisal/10.1214/22-STS880.short)
- Egozcue, J.J. & Pawlowsky-Glahn, V. (2023). [Response in SORT](https://www.idescat.cat/sort/sort472/47.2.2.Egozcue-Glahn.pdf)

### E-14 — MEWMA State Accumulation in CoDa Control Charts

**Status:** Methodological gap in emerging literature.

The MEWMA-CoDa control charts (Tran 2020, Nguyen 2025) work by accumulating weighted history — this is their power for detecting small persistent shifts. But the accumulated state is never audited for self-referential bias. If the MEWMA smoothing constant λ is poorly chosen, the chart can either over-react (high λ = no memory, high false alarm) or under-react (low λ = heavy memory, slow detection). In HUF terms, this is the loop filter time constant — and it's a governance decision, not a statistical one.

**References:**
- Nguyen, T.T.V. et al. (2025). [SVDD-MEWMA](https://www.sciencedirect.com/science/article/abs/pii/S0360835225000105)
- Tran, P.H. et al. (2023). [VSI MEWMA-CoDa](https://www.tandfonline.com/doi/full/10.1080/02664763.2023.2170336)

### E-15 — Measurement Error Propagation Through Log-Ratio Transforms

**Status:** Studied but not resolved for monitoring.

Measurement error in raw compositions propagates non-linearly through log-ratio transforms. A small absolute error in a trace carrier becomes a large relative error after CLR or ILR transformation. This has been studied for laboratory analytical error (geochemistry), but not for the kinds of measurement error that arise in governance data — rounding, delayed reporting, classification changes, retroactive corrections.

**References:**
- Tran, K.P. et al. (2020). Performance of the MEWMA-CoDa control chart in the presence of measurement errors. [ResearchGate](https://www.researchgate.net/publication/343604479_Performance_of_the_MEWMA-CoDa_control_chart_in_the_presence_of_measurement_errors)

### E-16 — Ordinal Structure in Compositional Parts

**Status:** New research direction (2024).

Weiß (2024) identified that some compositions have parts with a natural order (e.g., severity levels, age groups, quality grades). Standard CoDa treats all parts as exchangeable — no ordering is assumed. When order exists and is ignored, monitoring power is wasted.

**HUF implication:** HUF's carrier groups (fossil fuels ordered by carbon intensity, species ordered by trophic level) may have ordinal structure that standard CoDa balances don't exploit.

**References:**
- Weiß, C.H. (2024). [Ordinal CoDa time series](https://journals.sagepub.com/doi/full/10.1177/1471082X231190971)

---

## Summary: What CoDa Knows vs What HUF Reveals

| Error | CoDa Status | What HUF Adds |
|-------|-------------|---------------|
| E-01 Wrong geometry | Solved (1986) | Metric disagreement as diagnostic signal |
| E-02 Closure bias | Solved in theory | Pipeline contamination in multi-stage instruments |
| E-03 Zero replacement | Active open problem | Zeros are events, not nuisances |
| E-04 Partition choice | Acknowledged, underexplored | Partition sensitivity testing as standard practice; physical SBP from system structure |
| E-05 Geometric mean | Known trade-off | Governance-weighted reference instead of democratic geometric mean |
| E-06 Stale reference | Not addressed | Entirely new — governance reference management |
| E-07 Temporal aliasing | Emerging (control charts) | Compositional Nyquist; velocity-based aliasing test |
| E-08 Carrier admission | Partial (variable selection) | Formal justification protocol with sensitivity testing |
| E-09 Subcomposition | Solved (1986, debated 2023) | HUF is beneficiary, not contributor |
| E-10 Stored energy | Not addressed | Instrument state vs system state distinction |
| E-11 Dimensionality change | Open problem | Dimensionality change as first-class event, not data problem |
| E-12 Outlier masking | Studied (cross-sectional) | Temporal diagnostics via dual-metric divergence |
| E-13 Quasi-coherence | Active debate (2023) | If coherence relaxes, approximation error enters instrument |
| E-14 MEWMA state | Methodological gap | Loop filter governance for control chart tuning |
| E-15 Measurement error | Studied for lab data | Non-linear propagation in governance data (rounding, reclassification) |
| E-16 Ordinal structure | New direction (2024) | Carrier ordering may improve monitoring power |

### CoDa concerns that map directly to our analysis: 8 of 12 (E-01 through E-05, E-08, E-09, E-12)
### Concerns not addressed in CoDa literature: 4 of 12 (E-06, E-07, E-10, E-11)
### New concerns revealed by the literature: 4 additional (E-13 through E-16)

---

## The Conversation for Coimbra

CoDa has spent 40 years perfecting the mathematics of static compositional analysis. HUF has spent 6 months discovering what happens when you apply that mathematics continuously, with governance, to systems that change in real time. The entanglement creates 17 error sources — 8 that CoDa already knows about, 4 that only appear under continuous monitoring, 4 that emerge from the current state of CoDa's own internal debates, and 1 (E-17) from the chiPower-HUF calibration tension discovered during collective review.

The offer: HUF brings the application context that reveals which CoDa concerns matter most in practice, and surfaces new ones that static analysis will never encounter. CoDa brings the mathematical rigor that eliminates errors HUF couldn't even detect on its own.

Neither instrument is complete alone. The entanglement makes both stronger — but only if we calibrate honestly.

---

*Cross-references: [ENTANGLEMENT_ERROR_ANALYSIS.md](ENTANGLEMENT_ERROR_ANALYSIS.md) (error tables), [BATTLE_CARD.md](BATTLE_CARD.md) (conference posture), [FORMULA_REFERENCE.md](FORMULA_REFERENCE.md) (all formulas), [THE_CORE.md](THE_CORE.md) (what HUF is), [VOCABULARY_CARD.md](VOCABULARY_CARD.md) (language guide)*
