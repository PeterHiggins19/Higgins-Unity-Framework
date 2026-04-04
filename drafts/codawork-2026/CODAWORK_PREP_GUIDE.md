# CoDaWork Preparation Guide

## What is CoDaWork?

CoDaWork is a small, specialist workshop — not a massive conference. It runs every two years and draws maybe 50–100 people, almost all of whom work directly with compositional data. The 2026 edition is the 11th. Previous editions were held in Girona, Siena, Toulouse, Vienna. The atmosphere is collegial, not adversarial — but the audience knows their mathematics cold.

CoDaWork typically includes a one-day introductory CoDa course on the first day (June 1), followed by four days of talks, posters, and discussion. There is usually a Density Data Analysis (DDA) satellite meeting as well.

The workshop covers applications in geosciences, biology, genetics, economics, ecology, psychology, official statistics, and more. Energy-mix monitoring would be a new application domain for this community — which is exactly why MC-4 could be interesting to them.

---

## The People in the Room

These are the names you're most likely to encounter. Knowing who they are and what they work on will help you navigate conversations.

**Vera Pawlowsky-Glahn** (University of Girona) — Co-developed the modern algebraic-geometric structure of the simplex with Egozcue. Co-author of the standard textbook *Modeling and Analysis of Compositional Data* (Wiley, 2015). If she's in the room, she is the senior figure.

**Juan José Egozcue** (UPC Barcelona) — The other half of the Pawlowsky-Egozcue partnership. Developed the isometric log-ratio (ilr) transformation. Deeply mathematical — thinks in terms of Hilbert spaces on the simplex.

**Javier Palarea-Albaladejo** (BioSS, Scotland) — Expert on zero handling in compositional data. Author of the `zCompositions` R package. If your EMBER data has any zero entries (e.g., a country with 0% nuclear), he will ask how you handled them.

**Jan Graffelman** (UPC Barcelona) — Works on compositional biplots, genetics applications, and Hardy-Weinberg equilibrium as a compositional problem. Strong on visualization.

**Josep Antoni Martín-Fernández** (University of Girona) — Zero replacement methods, Bayesian approaches to count zeros. Collaborates frequently with Palarea-Albaladejo.

**Karel Hron** (Palacký University, Czech Republic) — ilr coordinates, functional compositional data. Bridging CoDa with functional data analysis.

**Peter Filzmoser** (TU Wien) — Robust statistics for compositional data. Outlier detection on the simplex.

**Raimon Tolosana-Delgado** (Helmholtz, Freiberg) — Geosciences applications, co-author of the Wiley textbook with Pawlowsky-Glahn and Egozcue.

---

## What You Must Know (the non-negotiables)

### 1. The Simplex and Aitchison Geometry

Compositional data live on the simplex: S^D = {(x₁,...,x_D) : xᵢ > 0, Σxᵢ = κ}. Aitchison (1982) showed the simplex has its own geometry — with two operations:

- **Perturbation** (the "addition" on the simplex): x ⊕ y = C(x₁y₁, ..., x_Dy_D), where C is the closure operator (rescales to sum to κ). Think of it as shifting a composition.
- **Powering** (the "scalar multiplication"): α ⊙ x = C(x₁^α, ..., x_D^α). Scales the ratios.

With these two operations, the simplex becomes a vector space — the Aitchison simplex. This is the foundation everything else is built on.

**Why it matters for you:** Your MC-4 framework operates on the simplex. You use Σρᵢ = 1. The CoDa community will want to know whether you've thought about your work in terms of Aitchison geometry, not just raw proportions.

### 2. Log-Ratio Transformations

Because the simplex is constrained (parts sum to 1), standard Euclidean statistics don't apply directly. The solution: transform to real space using log-ratios.

- **ALR (Additive Log-Ratio):** ln(xᵢ/x_D) — simple, but asymmetric (depends on which part is the denominator). Not an isometry.
- **CLR (Centered Log-Ratio):** ln(xᵢ/g(x)) where g(x) is the geometric mean. Symmetric, but the result lives in a hyperplane (singular covariance matrix).
- **ILR (Isometric Log-Ratio):** Projects onto an orthonormal basis in the simplex. Preserves distances and angles. This is what most CoDa researchers prefer for formal analysis.

**Why it matters for you:** Your TV distance and L2 norm operate on raw proportions. A CoDa purist will ask: "Why didn't you use Aitchison distance?" You should have an answer ready. (The honest answer: TV and L2 are standard in information theory and monitoring; Aitchison distance would be worth comparing, and your EMBER dataset is there for anyone to run that comparison.)

### 3. Aitchison Distance

d_A(x,y) = √(Σᵢ<ⱼ (ln(xᵢ/xⱼ) - ln(yᵢ/yⱼ))²) · (1/D)

Or equivalently: the Euclidean distance between the CLR-transformed vectors.

**Why it matters for you:** This is the "right" distance on the simplex according to CoDa theory. The conference demonstrator now computes both TV distance and Aitchison distance side-by-side as a dual-metric protocol. If someone asks "have you computed Aitchison distance?", the answer is: "Yes — we now run both TV and Aitchison on every observation. Agreement is treated as robustness; disagreement is treated as diagnostic information (dominant vs trace carrier movement). The open question is which metric should anchor the monitoring protocol."

### 4. The Zero Problem

Log-ratios require strictly positive data. Zeros break everything. The CoDa community has spent decades on this. Three types:

- **Rounded zeros:** Below detection limit. Replace with imputed values (Palarea-Albaladejo's `zCompositions` package).
- **Count zeros:** Sampling artifacts. Bayesian-multiplicative treatment (Martín-Fernández et al. 2015).
- **Essential (structural) zeros:** True absence of a component. The hardest case — no consensus solution.

**Why it matters for you:** Your EMBER data has structural zeros (e.g., countries with zero nuclear power). Your metadata YAML notes "zeros represent true absence of that carrier." A CoDa expert will probe this. Your answer: you treat them as structural zeros and flag them explicitly, but you haven't applied log-ratio imputation — that's an open question for CoDa collaboration.

### 5. The Closure Problem (Spurious Correlation)

Karl Pearson (1897) warned that correlations between parts of a composition are spurious — if one part goes up, others must go down. This is the constant-sum constraint. The CoDa framework exists precisely to handle this. Standard regression/correlation on raw proportions gives misleading results.

**Why it matters for you:** If you present drift detection based on raw proportions, someone will ask whether your detected "drift" is a real structural change or an artifact of closure. Having Aitchison distance as a parallel metric would address this.

---

## What You Should Know (strengthens your position)

### 6. Compositional Time Series

This is a relatively underdeveloped area in CoDa — which is exactly where your work fits. Most CoDa research is cross-sectional (one snapshot of a composition). Tracking how compositions change over time is active research.

Key concept: a compositional time series is a sequence of points on the simplex. Change between periods can be measured as perturbation: the "difference" between x(t) and x(t-1) is x(t) ⊖ x(t-1) = C(x₁(t)/x₁(t-1), ..., x_D(t)/x_D(t-1)). This is the compositional equivalent of a first difference.

### 7. Balances

Balances are special ilr coordinates defined by a sequential binary partition (SBP) of the parts. Each balance captures the log-ratio between two groups of parts. They're interpretable: e.g., "fossil fuels vs renewables" could be a balance in your energy data.

**Why it matters for you:** If someone suggests expressing your EMBER data in terms of balances rather than raw proportions, this is a constructive suggestion — it could make your drift detection more interpretable.

### 8. CoDa-Dendrogram (Balance Dendrograms)

A visualization tool showing the hierarchical partition of parts into balances. Shows which groups of parts covary and which are independent. CoDa researchers use these routinely.

### 9. Compositional Biplots

The CoDa equivalent of PCA biplots. Based on CLR-transformed data. Shows the relationship between samples and parts simultaneously. Graffelman is the expert on these.

---

## Questions They Will Likely Ask You

1. **"Why TV distance / L2 norm instead of Aitchison distance?"**
   → The conference demonstrator now computes both. TV distance is retained for monitoring interpretability; Aitchison distance is the simplex-native geometric metric. Agreement between them is treated as robustness; disagreement is treated as diagnostic (dominant vs trace carrier movement). The open question is which should anchor the monitoring protocol — that's exactly why I'm here.

2. **"How do you handle zeros in your compositions?"**
   → Event-first protocol: a carrier reaching zero is treated first as a domain event (flag it, record the TV velocity spike), then CoDa zero-handling is applied only if further geometric analysis is required. Greenacre's chiPower is being explored as a post-event correction layer that preserves subcompositional coherence. Open to CoDa community guidance on best practice. This is documented as E-03/E-17 in the 17-error calibration catalogue.

3. **"Have you considered log-ratio transformations?"**
   → Yes. CLR and ILR are now implemented in the conference demonstrator alongside the original TV-based metrics. The conference posture is that Aitchison distance and log-ratio views are included for exploratory calibration — the open question is not whether they exist in the toolchain, but how they should anchor the monitoring protocol, what the correct null model is, and how zeros and subcompositions should be governed.

4. **"What's new here? The simplex is well-studied."**
   → The math is not new. The claim is that nobody has built a formal monitoring protocol on compositional data that tracks declared-vs-observed allocation with change detection. The four defeat paths in the packet are there precisely to test this.

5. **"Where's the null distribution for your p-value?"**
   → You flagged this yourself in the packet. The p=0.0016 comes from a Pettitt test on a sliding window, but no formal null model (Dirichlet, permutation, bootstrap) is specified. That's an open gap you've disclosed.

6. **"What about subcompositional coherence?"**
   → This is a CoDa concept: results should be the same whether you analyze all D parts or a subset. If you monitor 9 fuel types but someone analyzes only the 3 fossil fuels, do your drift results hold? Worth thinking about.

7. **"How is this different from monitoring Dirichlet-distributed data?"**
   → The Dirichlet is a parametric model on the simplex. Your approach is model-free — it doesn't assume any distribution. A Dirichlet-based monitoring scheme would be a specific parametric alternative. Whether model-free or parametric detection is better is an empirical question your data could help answer.

---

## Key Reading List (Priority Order)

1. **Aitchison, J. (1986/2003).** *The Statistical Analysis of Compositional Data.* The original. Dense but foundational. The 2003 reprint has corrections.

2. **Pawlowsky-Glahn, V., Egozcue, J.J., & Tolosana-Delgado, R. (2015).** *Modeling and Analysis of Compositional Data.* Wiley. The modern standard textbook. Start with chapters 1–4.

3. **Aitchison, J. (2003).** *A Concise Guide to Compositional Data Analysis.* Free PDF (lecture notes from a CoDaWork course). Shorter and more accessible than the book.

4. **Pawlowsky-Glahn, V. & Egozcue, J.J.** Lecture notes on CoDa — freely available at compositionaldata.com. Good for the algebra.

5. **Palarea-Albaladejo, J. & Martín-Fernández, J.A. (2015).** "zCompositions — R package for multivariate imputation of left-censored data under a compositional approach." — For the zero problem.

6. **Filzmoser, P., Hron, K., & Templ, M. (2018).** *Applied Compositional Data Analysis.* Springer. More practical/applied than Pawlowsky-Glahn. Good for R code examples.

---

## Your Strongest Positions

- **The application is genuinely new.** CoDa theory is mature; monitoring applications are not. Nobody at CoDaWork has published a compositional change-detection protocol for energy markets.
- **You brought the data.** Real EMBER data, 3 countries, 26 years, 9 carriers, CoDa-ready CSV. Researchers love having something concrete to work with.
- **You invited defeat.** The four defeat paths signal you're serious. Academics respect the posture of "break this, please" over "look what I built."
- **You disclosed every weakness.** The metric correction, the null-model gap, the zero-handling question. This is what honest research looks like.

## Your Known Vulnerabilities

- **Log-ratio and Aitchison distance: implemented, not validated.** The conference demonstrator now includes CLR, ILR, and Aitchison distance alongside the original TV-based metrics. But "implemented for exploratory calibration" is not "settled as validated monitoring protocol." A CoDa purist will want to know which anchors the monitoring — that question is explicitly open.
- **No null distribution.** The p-value has no formal null model.
- **Independent researcher.** No institutional backing. This is neither good nor bad, but it means you'll be evaluated purely on the work.
- **AI-assisted development.** If asked, disclose matter-of-factly. Don't lead with it.
