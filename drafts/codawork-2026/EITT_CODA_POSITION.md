# What EITT Offers CoDa — And Why CoDa Should Care

**For:** CoDaWork 2026, Coimbra
**Posture:** Gift, not claim. Open problem, not closed theorem.

---

## The One-Paragraph Version

We found that when you use the geometric mean — your central operation — as a temporal filter on compositional time series, Shannon entropy is empirically near-invariant across temporal resolutions. We have now confirmed this across five domains: energy (electricity generation, 7 countries, 0.18–1.02%), hardware degradation (Backblaze drive stats, K=4, 24 months, 0.03%), financial markets (120-stock price-level portfolio, K=9, 74 months, 0.08% — note: price-level weighted, not market-cap), commodities (gold/silver, K=2, 339 years, +0.08% at 2:1), and cosmological observation (Planck 353 GHz half-mission split, 0.3%). We further confirmed that the invariance holds for the entire Renyi entropy family from q=0.1 to q=5.0 — Shannon is not special; the phenomenon lives in the Aitchison geometry. When EITT fails, the failure is bidirectionally diagnostic: at K=2 gold/silver (6.7% at 365:1), increasing dimensionality to K=4 restores invariance (upward inversion — hidden dimensions); at K=9 China electricity (−2.22%), decreasing dimensionality to K=3 restores invariance (downward inversion — exposed non-stationarity). The direction of the fix identifies the pathology. We ran 17 adversarial tests on energy data and found honest boundary conditions — the effect requires temporal autocorrelation. We identified the residual as a second-order Jensen correction. We cannot prove it analytically. That is why we are here.

### Engineering Origin

This framework traces to a loudspeaker diffraction correction method (DADC-DADI-ADAC) developed in the Rogue Wave Audio Binaural Test Lab in late 2024. The total baffle step correction (6.02 dB) is a closure constraint apportioned among the physical dimensions of a cabinet — a composition on the simplex, before we knew the word. The inverse stage (DADI) reconstructs object geometry from acoustic response without imprinting the probe's own signature on the result. The design requirement that the measurement system must be inert carried forward unchanged into the compositional monitoring framework.

---

## What This Means for CoDa

The geometric mean is the centre of Aitchison geometry. It defines the CLR transform. It defines the Frechet mean. It is a central CoDa operation. We have found that this operation has a property we have not found documented in the literature we reviewed: it preserves information content across temporal scales in the datasets we tested.

This is not an addition to the CoDa framework. It is a discovery about a tool the framework already uses. Every CoDa practitioner who has ever computed a geometric mean of compositions over a time window has been performing an entropy-preserving operation without knowing it.

---

## Operationalized: The Temporal Chain d(CoDa)/dt

*d(CoDa)/dt has been operationalized as the tap controller for adaptive decimation. When composition changes slowly, you can compress aggressively. When it changes fast, you must use smaller blocks. The maximum balance velocity across ILR coordinates determines the maximum safe averaging window at each time step.*

EITT answers what is conserved. Compositions also move — and the temporal derivative of that movement has confirmed operational structure. We have identified three layers:

**Layer 1 — Perturbation velocity: |d(CoDa)/dt| on the simplex.** The Aitchison distance between consecutive time points, d_A(x(t), x(t−1)). This is the scalar speed of compositional change — how fast the system is moving, without direction. It is already computed in both the Spectrum Analyzer v3 and the CoDa Explorer. Spikes correspond to structural shocks (Fukushima 2011, UK coal exit 2016).

**Layer 2 — Balance trajectory: B(t) = ilr(x(t)).** The ILR coordinates over time — the structural path. Each balance tracks the ratio between two groups of carriers. B₁ (fossil vs. renewable) crossing zero is the energy transition. This is the integral of the structural motion, already plotted in both tools.

**Layer 3 — Balance derivative: dB/dt.** The instantaneous rate of structural change along each ILR partition. This is the missing middle layer. dB₁/dt tells you how fast fossil is losing ground to renewable right now. The sign gives direction. The magnitude gives speed. The second derivative d²B/dt² tells you whether the transition is accelerating.

**Why this may matter for CoDa:** In raw proportions, Σ dx_i/dt = 0 always — this is a mathematical identity of closure, not an empirical finding. But in ILR coordinates, the balance derivatives are free — each dB/dt moves independently. If this decomposition proves useful, ILR would be the natural coordinate system for compositional temporal derivatives.

**Confirmed connection to EITT:** The balance derivative describes the motion. EITT describes what is conserved when you compress the time record. They are complementary: d(CoDa)/dt serves as the rate controller that determines the maximum safe compression window. Adaptive decimation using d(CoDa)/dt as the tap controller was tested on gold/silver (fixed 10:1 fails at +1.39%, adaptive passes at -0.43% with 10:1 effective compression) and energy solar|rest balance (fixed fails, adaptive passes at 3.6:1 compression). It fails on Germany, where the entire series is non-stationary — confirming that when there is no slow regime, no averaging is safe.

---

## What We Offer

**The finding:** Shannon entropy near-invariance under geometric-mean decimation (EITT). Two independent proofs on different domains, different carriers, different resolutions.

**The boundary:** 17 adversarial tests. 10 pass, 7 fail. The failures define where EITT breaks — no temporal autocorrelation, no invariance. This is what separates a calibration study from a sales pitch.

**The mechanism:** The residual is a second-order Jensen correction. The Hessian of Shannon entropy (diagonal: -1/x_i) interacts with the variance reduction from block averaging. The correction is small because exp (in the geometric mean) and ln (in entropy) are inverse functions — first-order effects cancel by construction. Euler's e is the shared base.

**The theoretical gap:** Copilot's VAR(1) calibration lab showed theoretical linear bounds of 100-1000%, vs observed 0.03%. A gap of 10,000x. This rules out linear autoregressive dynamics as the explanation. Something deeper is preserving entropy, and linear models cannot see it.

**The open problem:** Derive a closed-form expression or tight asymptotic bound for the entropy change under M-block geometric decimation of a stationary compositional process. The boundary condition (temporal autocorrelation) needs to be made quantitative. Three conjectures are proposed (Hessian leading term, threshold function, Fisher-Rao interpretation).

**Reproducible artifacts:** All scripts, data, calibration outputs, and analysis are packaged in the repo. Anyone can run them.

---

## What We Need From CoDa

**An analytic proof or disproof.** We have the empirical evidence. CoDa has the algebraic and geometric machinery to either prove this or find the counterexample that breaks it.

**The information-geometric connection.** The Hessian of Shannon entropy on the simplex is related to the Fisher information matrix. Erb & Ay have worked on the Fisher metric for CoDa. If EITT can be expressed in terms of the Fisher-Rao geometry, that would be a deep structural result.

**Testing on non-energy domains.** We have now tested four non-energy domains (hardware, financial, cosmological, commodities). Three hold. One fails at K=2 and holds at K=4 — revealing the EITT inversion principle. Honesty notes: the financial composition is price-level weighted from a 120-stock personal portfolio (not market-cap weighted from a standard index), and the Planck spatial decimation was incorrectly implemented (HEALPix NESTED ordering does not preserve spatial locality — only the temporal half-mission split is valid). Bootstrap confidence intervals have been computed for all domains (see code/analysis/honesty_tests_results_2026april9.txt). CoDa researchers working with geological, ecological, and genomic compositions can extend the table further.

**Credibility for the broader landscape.** EITT connects to ecology (Shannon-Wiener diversity), biomedical signal processing (multiscale entropy), information geometry, Renyi/Tsallis generalizations, and maximum entropy principles. We cannot approach those communities alone. With CoDa researchers alongside us, we can.

---

## Why CoDa Should Care

**It elevates the geometric mean.** The geometric mean is already the most important operation in CoDa. If it also preserves Shannon entropy, that's a new argument for why CoDa's approach is natural and correct. The geometric mean isn't just algebraically convenient — it's information-theoretically principled.

**It may enable multi-resolution comparison.** Any CoDa practitioner working with time series at different resolutions (daily monitoring vs. annual reports, monthly surveys vs. decadal trends) could benefit: if geometric-mean decimation preserves entropy, you're not destroying information content. This requires validation on each practitioner's data — we are not claiming a guarantee, only showing where it held in ours.

**It connects CoDa to information theory.** CoDa and information theory have developed largely independently despite sharing the simplex. EITT is a bridge. If the CoDa community can prove EITT analytically, that's a paper that both communities cite.

**It provides a temporal derivative framework.** The d(CoDa)/dt chain — perturbation velocity, balance trajectory, balance derivative dB/dt — has been operationalized as the tap controller for adaptive decimation. The maximum balance velocity across ILR coordinates determines the maximum safe averaging window. Tested: gold/silver adaptive decimation rescued a 10:1 fixed failure (+1.39%) to a pass (-0.43%); solar|rest balance rescued at 3.6:1 effective compression. Germany failed — confirming that when the entire series is non-stationary, no averaging is safe. The formal optimality of the adaptive block-width function remains open (O-6 in EITT_CODA_MATHEMATICS).

**It opens research questions.** Three conjectures (Hessian sufficiency, autocorrelation threshold, Fisher-Rao interpretation) are each testable. The Renyi generalization is now empirically confirmed (q=0.1 to 5.0) but the formal proof remains open. The EITT inversion principle now has two examples in opposite directions: gold/silver upward (K=2 to K=4, hidden dimensions) and China downward (K=9 to K=3, exposed non-stationarity) — bidirectional inversion is established. The d(CoDa)/dt chain is operationalized as the adaptive decimation tap controller, with empirical validation on two datasets and one confirmed failure mode (globally non-stationary series). The formal optimality of the adaptive block-width function remains open (O-6).

---

## The Bridge to Other Fields

If CoDa validates EITT, here is what opens up:

**Ecology:** Shannon-Wiener diversity index = Shannon entropy. Species composition = compositional data. If EITT holds, temporal aggregation of biodiversity surveys using geometric means preserves the diversity index. Every ecologist monitoring species composition over time can use this. Contact point: Chao's iNEXT framework.

**Biomedical signal processing:** Multiscale entropy (Costa et al. 2002) coarse-grains with arithmetic mean on scalars. EITT offers the compositional version using the CoDa-correct operation. New territory for complexity analysis of compositional biomarkers.

**Information geometry:** The Hessian of entropy on the simplex is the core structure. Amari, Ay, Erb have the framework. If EITT's residual is a quadratic form under the Fisher-Rao metric, that's a geometric proof.

**Maximum entropy:** H* approaches ln(D) — the maximum entropy composition. The geometric mean may be driving temporally autocorrelated compositions toward maximum entropy under aggregation. This would be a compositional realization of the second law.

**Jensen inequality refinements:** The Hessian footprint IS the second-order Jensen correction. Recent work on tight bounds for twice-differentiable functions applies directly. CoDa data provides a concrete, empirically testable case.

**Renyi / Tsallis — CONFIRMED:** EITT holds for all tested Renyi orders q = 0.1 to 5.0, and for Tsallis entropy at the same values. |delta| < 2% across the entire range, across all tested datasets. Shannon is not special. The near-invariance is a property of the geometric-mean decimation operator (Aitchison geometry), not of any specific entropy functional. This means the entire diversity profile is invariant — Simpson's index (q=2), Herfindahl index (economics, also q=2), Gibbs entropy (physics), and every other smooth functional on the simplex. The formal proof that geometric-mean decimation preserves the Renyi family remains open.

---

## What We Are NOT Claiming

We are not claiming a theorem. We are not claiming universal domain independence. We are not claiming this works everywhere. We are presenting an empirical finding confirmed across five domains with defined boundary conditions, a mechanistic explanation, reproducible code, and an open mathematical problem. When it fails, we show why and what fixing it reveals. We are here because CoDa has the tools to resolve this. We would welcome help formalizing it — or breaking it.

**Honesty disclosure (April 9, 2026 adversarial audit):** (1) The financial sector composition uses mean closing price across a 120-stock personal portfolio, not market-capitalization weighting from a standard index. The EITT result (0.08%) is real on this specific composition but the domain label should not be read as "equity market." (2) The Planck spatial EITT claim (18.1% failure) is invalid — HEALPix NESTED pixel ordering does not preserve spatial locality, so the "spatial decimation" was actually random pixel grouping. Only the temporal half-mission split (0.3%) is valid. (3) At 2:1 compression, arithmetic-mean decimation also preserves entropy to within 1%. The geometric mean's advantage appears at higher compression ratios. (4) The K=4 gold/silver reconstruction passes out-of-sample (train on first 200 years, test on last 138 years: 0.003%) and is robust across 100% of 180 hyperparameter combinations tested — the result is not fragile. (5) Bootstrap 95% CIs computed for all domains.

---

## Governance

CGS-2 (n=3), GDoF 264. No new constants. All operations are native CoDa.
