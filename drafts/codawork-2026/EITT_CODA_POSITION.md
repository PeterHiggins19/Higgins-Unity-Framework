# What EITT Offers CoDa — And Why CoDa Should Care

**For:** CoDaWork 2026, Coimbra
**Posture:** Gift, not claim. Open problem, not closed theorem.

---

## The One-Paragraph Version

We found that when you use the geometric mean — your central operation — as a temporal filter on compositional time series, Shannon entropy is empirically near-invariant across temporal resolutions. Daily, weekly, monthly, quarterly, annual — the entropy barely moves. We measured 0.18% variation across 341:1 compression on European electricity prices (8 carriers, 4089 days), and confirmed independently at 1.02% on monthly electricity generation (6 countries, 9 fuel types, 12:1 compression). We ran 17 adversarial tests and found honest boundary conditions — the effect requires temporal autocorrelation. We identified the residual as a second-order Jensen correction (the Hessian footprint of entropy's concavity on the simplex). We cannot prove it analytically. That is why we are here.

---

## What This Means for CoDa

The geometric mean is the centre of Aitchison geometry. It defines the CLR transform. It defines the Frechet mean. It is a central CoDa operation. We have found that this operation has a property we have not found documented in the literature we reviewed: it preserves information content across temporal scales in the datasets we tested.

This is not an addition to the CoDa framework. It is a discovery about a tool the framework already uses. Every CoDa practitioner who has ever computed a geometric mean of compositions over a time window has been performing an entropy-preserving operation without knowing it.

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

**Testing on non-energy domains.** We have only tested energy data. CoDa researchers work with geological, ecological, economic, and genomic compositions. A single confirmation outside energy makes the finding much stronger. A single failure outside energy defines a new boundary condition.

**Credibility for the broader landscape.** EITT connects to ecology (Shannon-Wiener diversity), biomedical signal processing (multiscale entropy), information geometry, Renyi/Tsallis generalizations, and maximum entropy principles. We cannot approach those communities alone. With CoDa researchers alongside us, we can.

---

## Why CoDa Should Care

**It elevates the geometric mean.** The geometric mean is already the most important operation in CoDa. If it also preserves Shannon entropy, that's a new argument for why CoDa's approach is natural and correct. The geometric mean isn't just algebraically convenient — it's information-theoretically principled.

**It enables multi-resolution comparison.** Any CoDa practitioner working with time series at different resolutions (daily monitoring vs. annual reports, monthly surveys vs. decadal trends) gains a guarantee: if you decimate with the geometric mean, you're not destroying information content. That's a practical tool.

**It connects CoDa to information theory.** CoDa and information theory have developed largely independently despite sharing the simplex. EITT is a bridge. If the CoDa community can prove EITT analytically, that's a paper that both communities cite.

**It opens new research directions.** The 3 conjectures (Hessian sufficiency, autocorrelation threshold, Fisher-Rao interpretation) are each worth a paper. The Renyi generalization question (does EITT hold for all q-orders?) maps directly to ecology's Hill numbers. The maximum entropy convergence (H* approaches ln(D)) has thermodynamic implications.

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

We are not claiming a theorem. We are not claiming domain independence. We are not claiming this works everywhere. We are presenting an empirical finding with defined boundary conditions, a mechanistic explanation, reproducible code, and an open mathematical problem. We are here because CoDa has the tools to resolve this. We would welcome help formalizing it — or breaking it.

---

## Governance

CGS-2 (n=3), GDoF 264. No new constants. All operations are native CoDa.
