# What EITT Offers CoDa — And Why CoDa Should Care

**For:** CoDaWork 2026, Coimbra
**Posture:** Gift, not claim. Open problem, not closed theorem.

---

## The One-Paragraph Version

We found that when you use the geometric mean — your central operation — as a temporal filter on compositional time series, Shannon entropy is empirically near-invariant across temporal resolutions. We have now confirmed this across five domains: energy (electricity generation, 7 countries, 0.18–1.02%), hardware degradation (Backblaze drive stats, K=4, 24 months, 0.03%), financial markets (120-stock price-level portfolio, K=9, 74 months, 0.08% — note: price-level weighted, not market-cap), and cosmological observation (Planck 353 GHz half-mission split, 0.3%). We also found that when EITT fails — as it does on the gold/silver ratio at K=2 over 338 years (6.7%) — increasing the dimensionality to K=4 by recovering hidden volatility and momentum carriers restores invariance to 0.38%. The failure diagnoses missing dimensions. We ran 17 adversarial tests on energy data and found honest boundary conditions — the effect requires temporal autocorrelation. We identified the residual as a second-order Jensen correction. We cannot prove it analytically. That is why we are here.

---

## What This Means for CoDa

The geometric mean is the centre of Aitchison geometry. It defines the CLR transform. It defines the Frechet mean. It is a central CoDa operation. We have found that this operation has a property we have not found documented in the literature we reviewed: it preserves information content across temporal scales in the datasets we tested.

This is not an addition to the CoDa framework. It is a discovery about a tool the framework already uses. Every CoDa practitioner who has ever computed a geometric mean of compositions over a time window has been performing an entropy-preserving operation without knowing it.

---

## The Temporal Chain: d(CoDa)/dt

EITT answers what is conserved. But compositions also move — and the temporal derivative of that movement has a structure that supports EITT and deepens it.

Three layers exist, two already implemented in our tools, one identified but not yet visualized:

**Layer 1 — Perturbation velocity: |d(CoDa)/dt| on the simplex.** The Aitchison distance between consecutive time points, d_A(x(t), x(t−1)). This is the scalar speed of compositional change — how fast the system is moving, without direction. It is already computed in both the Spectrum Analyzer v3 and the CoDa Explorer. Spikes correspond to structural shocks (Fukushima 2011, UK coal exit 2016).

**Layer 2 — Balance trajectory: B(t) = ilr(x(t)).** The ILR coordinates over time — the structural path. Each balance tracks the ratio between two groups of carriers. B₁ (fossil vs. renewable) crossing zero is the energy transition. This is the integral of the structural motion, already plotted in both tools.

**Layer 3 — Balance derivative: dB/dt.** The instantaneous rate of structural change along each ILR partition. This is the missing middle layer. dB₁/dt tells you how fast fossil is losing ground to renewable right now. The sign gives direction. The magnitude gives speed. The second derivative d²B/dt² tells you whether the transition is accelerating.

**Why this matters for CoDa:** In raw proportions, Σ dx_i/dt = 0 always. That zero-sum constraint is not a limitation — it IS the relay chain. Every gain in one carrier is financed by losses in others. But in ILR coordinates, the balance derivatives are free — each dB/dt moves independently. This is why ILR is the correct coordinate system for compositional temporal analysis: it decomposes the constrained relay into independent structural movements along interpretable partitions.

**The connection to EITT:** The balance derivative describes the motion. EITT describes what is conserved when you compress the time record of that motion. They are complementary: d(CoDa)/dt tells you "how fast and in which direction is the composition moving?" EITT tells you "does the information content survive temporal aggregation of that movement?" Together, they form the temporal analysis framework that CoDa's spatial geometry has not yet developed.

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

**It enables multi-resolution comparison.** Any CoDa practitioner working with time series at different resolutions (daily monitoring vs. annual reports, monthly surveys vs. decadal trends) gains a guarantee: if you decimate with the geometric mean, you're not destroying information content. That's a practical tool.

**It connects CoDa to information theory.** CoDa and information theory have developed largely independently despite sharing the simplex. EITT is a bridge. If the CoDa community can prove EITT analytically, that's a paper that both communities cite.

**It gives CoDa a temporal derivative framework.** The d(CoDa)/dt chain — perturbation velocity as scalar speed, balance trajectory as structural path, balance derivative dB/dt as directed rate — provides CoDa with a structured approach to compositional time series that goes beyond "do CoDa at each time point independently." The zero-sum constraint in raw proportions (Σ dx_i/dt = 0) forces the relay structure; ILR coordinates decompose that relay into independent structural rates. This is the temporal analysis layer CoDa's spatial geometry has not formalized.

**It opens new research directions.** The 3 conjectures (Hessian sufficiency, autocorrelation threshold, Fisher-Rao interpretation) are each worth a paper. The Renyi generalization question (does EITT hold for all q-orders?) maps directly to ecology's Hill numbers. The maximum entropy convergence (H* approaches ln(D)) has thermodynamic implications. The d(CoDa)/dt chain adds further directions: whether balance smoothness (small |dB/dt|) predicts EITT holding (confirmed: Backblaze B2 has 100% monotonicity and the tightest EITT at 0.03%), whether d²B/dt² reveals regime transition onset, and whether the balance derivative connects to Hron's functional CoDa framework as a natural velocity field on the simplex. The EITT inversion principle — increasing K to recover hidden carriers when EITT fails — opens a new direction in compositional dimensionality analysis: using entropy invariance as a criterion for the true number of parts in a system.

---

## The Bridge to Other Fields

If CoDa validates EITT, here is what opens up:

**Ecology:** Shannon-Wiener diversity index = Shannon entropy. Species composition = compositional data. If EITT holds, temporal aggregation of biodiversity surveys using geometric means preserves the diversity index. Every ecologist monitoring species composition over time can use this. Contact point: Chao's iNEXT framework.

**Biomedical signal processing:** Multiscale entropy (Costa et al. 2002) coarse-grains with arithmetic mean on scalars. EITT offers the compositional version using the CoDa-correct operation. New territory for complexity analysis of compositional biomarkers.

**Information geometry:** The Hessian of entropy on the simplex is the core structure. Amari, Ay, Erb have the framework. If EITT's residual is a quadratic form under the Fisher-Rao metric, that's a geometric proof.

**Maximum entropy:** H* approaches ln(D) — the maximum entropy composition. The geometric mean may be driving temporally autocorrelated compositions toward maximum entropy under aggregation. This would be a compositional realization of the second law.

**Jensen inequality refinements:** The Hessian footprint IS the second-order Jensen correction. Recent work on tight bounds for twice-differentiable functions applies directly. CoDa data provides a concrete, empirically testable case.

**Renyi / Tsallis:** Does EITT hold for H_q (order q) or only for Shannon (q = 1)? If all q, the entire diversity profile is invariant. If only q = 1, Shannon has a special role. Either result is publishable.

---

## What We Are NOT Claiming

We are not claiming a theorem. We are not claiming universal domain independence. We are not claiming this works everywhere. We are presenting an empirical finding confirmed across five domains with defined boundary conditions, a mechanistic explanation, reproducible code, and an open mathematical problem. When it fails, we show why and what fixing it reveals. We are here because CoDa has the tools to resolve this. We would welcome help formalizing it — or breaking it.

**Honesty disclosure (April 9, 2026 adversarial audit):** (1) The financial sector composition uses mean closing price across a 120-stock personal portfolio, not market-capitalization weighting from a standard index. The EITT result (0.08%) is real on this specific composition but the domain label should not be read as "equity market." (2) The Planck spatial EITT claim (18.1% failure) is invalid — HEALPix NESTED pixel ordering does not preserve spatial locality, so the "spatial decimation" was actually random pixel grouping. Only the temporal half-mission split (0.3%) is valid. (3) At 2:1 compression, arithmetic-mean decimation also preserves entropy to within 1%. The geometric mean's advantage appears at higher compression ratios. (4) The K=4 gold/silver reconstruction passes out-of-sample (train on first 200 years, test on last 138 years: 0.003%) and is robust across 100% of 180 hyperparameter combinations tested — the result is not fragile. (5) Bootstrap 95% CIs computed for all domains.

---

## Governance

CGS-2 (n=3), GDoF 264. No new constants. All operations are native CoDa.
