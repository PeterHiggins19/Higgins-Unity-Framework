# EITT and the Entropy Landscape — Where We Sit

**Purpose:** Before pushing, map every entropy formula we use against the broader literature. Know who has been here before, what they asked, what they answered, where we overlap, and where we're standing on genuinely new ground.

**Date:** 2026-04-09, Session S016

---

> **Terminology Key — CoDa vs HUF**
>
> *Standard CoDa terms* used in this document: simplex, Aitchison geometry/distance, geometric mean / Fréchet mean, CLR transform, compositional data analysis (CoDa), subcompositional coherence, perturbation algebra.
>
> *Standard information theory / entropy terms*: Shannon entropy H(x), Rényi entropy H_q, Fisher information, Fisher-Rao metric, Jensen's inequality, entropy rate, entropy power inequality, rate-distortion theory.
>
> *HUF terms* introduced by this work: EITT (Entropy Invariance under Temporal Transformation), K_eff (effective number of carriers = exp(H)), Hessian footprint (the Jensen correction applied to EITT), geometric-mean decimation (the CoDa-correct temporal coarse-graining operation), d(CoDa)/dt (balance velocity), adaptive decimation, MC-4 (Composition Monitoring).

---

## Our Formulas — What We Use and Why

We use 6 entropy-related formulas. Every one of them is standard. What's new is what we DO with them together.

### Formula 1: Shannon Entropy

    H(x) = -Σ xᵢ ln(xᵢ)

**What it asks:** How evenly spread is this composition? How much information does it carry?

**What we use it for:** The conserved quantity under EITT. We compute H at every resolution level (daily, weekly, monthly, quarterly, annual) and show it barely changes.

**Who else uses it:** Everyone. Shannon (1948), ecology (Shannon-Wiener diversity index), information theory, statistical mechanics, machine learning. This is the most studied formula in information science.

### Formula 2: Effective Number of Carriers (K_eff)

    K_eff = exp(H(x))

**What it asks:** How many carriers are "effectively present"? (The exponential of entropy converts nats to a count.)

**What we use it for:** Governance diagnostics — tracking the effective dimensionality of monitored systems. Also known as the "perplexity" in NLP, "Hill number of order 1" in ecology.

**Who else uses it:** Ecology (Hill numbers, Chao's iNEXT framework), NLP (perplexity), diversity science.

### Formula 3: The Hessian of Shannon Entropy

    ∂²H/∂xᵢ² = -1/xᵢ    (diagonal, off-diagonal = 0 on the simplex interior)

**What it asks:** How curved is the entropy surface at this composition?

**What we use it for:** The Hessian footprint — explaining the systematic residual drift in EITT. The curvature of entropy at the Fréchet mean determines the magnitude of the Jensen correction.

**Who else uses it:** Information geometry (related to Fisher information matrix). The Hessian of entropy on the simplex is well-known to be diagonal with entries -1/xᵢ. This is standard differential geometry.

### Formula 4: Second-Order Jensen Correction

    ΔH ≈ (1/2) tr[ |Hess_H(x*)| · Cov(x̄_M) ]

**What it asks:** How much does entropy change when you reduce the variance of compositions by block-averaging?

**What we use it for:** Predicting and explaining the EITT residual. This is the leading-order correction from Jensen's inequality for a concave function.

**Who else uses it:** The general second-order Taylor expansion of a concave function around its mean is textbook. Recent work (2025) on "Refinements of Jensen's Inequality for Twice-Differentiable Functions with Bounded Hessians" extends this. But applying it specifically to Shannon entropy under compositional geometric-mean decimation — we have not found this in the literature.

### Formula 5: Compositional Geometric Mean

    x̄_geo = C( exp( (1/M) Σ ln(xₜ) ) )

**What it asks:** What is the CoDa-correct average of M consecutive compositions?

**What we use it for:** The anti-aliasing filter in EITT. This is the temporal decimation operation.

**Who else uses it:** Aitchison (1982) established the geometric mean as the natural centre of compositional data. Pawlowsky-Glahn and Egozcue formalized it in the Aitchison geometry. Every CoDa practitioner uses this. What nobody has done (that we can find) is study what it does to Shannon entropy when applied as a temporal filter.

### Formula 6: Fréchet Mean Entropy (H*)

    H* = H(x*)  where  x* = lim_{M→∞} x̄_M  (the Fréchet mean)

**What it asks:** What entropy does the system converge to under infinite averaging?

**What we use it for:** The asymptotic target of EITT convergence. All decimation levels are approaching H* from below.

**Who else uses it:** Fréchet means on manifolds are well-studied in differential geometry. The entropy at the Fréchet mean is a natural quantity but we haven't found it explicitly studied in the context of temporal decimation.

---

## The Literature Landscape — 10 Territories

### Territory 1: Shannon Entropy on the Simplex (CoDa)

**Who:** Aitchison (1982), Pawlowsky-Glahn, Egozcue, Mateu-Figueras, Barceló-Vidal.

**What they ask:** How to do statistics on the simplex. Log-ratio transforms, Aitchison distance, perturbation algebra.

**What they answer:** A complete algebraic and geometric framework for compositional data.

**What they DON'T ask:** How entropy behaves under temporal operations within that framework.

**Our relation:** We use their tools (geometric mean, CLR, Aitchison distance). EITT is a new finding within their framework. They built the house. We found something in a room they hadn't opened.

### Territory 2: Information Geometry on the Simplex

**Who:** Amari, Ay, Jost, Lê, Schwachhöfer. Also Erb & Ay specifically on the Fisher metric for CoDa.

**What they ask:** What is the natural Riemannian geometry of probability distributions? How do the Fisher-Rao metric and alpha-connections structure the simplex?

**What they answer:** The Fisher-Rao metric is the unique Riemannian metric invariant under sufficient statistics (Chentsov's theorem). The simplex embeds onto a radius-2 sphere.

**What they DON'T ask:** How these geometric structures interact with temporal aggregation.

**Our relation:** The Hessian of entropy (-1/xᵢ) is related to the Fisher information matrix. Copilot's Conjecture 3 proposes that EITT's residual can be expressed as a quadratic form under the Fisher-Rao metric. This is an open connection we're flagging, not claiming.

### Territory 3: Block Entropy / Multiscale Entropy

**Who:** Costa, Goldberger, Peng (multiscale entropy, 2002). Richman & Moorman (sample entropy). Widespread in biomedical signal analysis.

**What they ask:** How does entropy change across temporal scales? (Usually for univariate time series, not compositions.)

**What they answer:** Multiscale entropy algorithms coarse-grain a time series by averaging in windows, then compute sample entropy at each scale. Healthy systems show complexity across scales; diseased systems lose it.

**What they DON'T ask:** What happens when the coarse-graining is a COMPOSITIONAL geometric mean on the simplex instead of an arithmetic mean on the real line.

**Our relation:** EITT is a compositional analogue of multiscale entropy analysis. The key difference: they use arithmetic mean for coarse-graining (which doesn't respect the simplex). We use geometric mean (which does). Their entropy typically changes across scales. Ours doesn't. That's the finding.

### Territory 4: Entropy Rate of Stochastic Processes

**Who:** Shannon (1948), Cover & Thomas (textbook). Standard information theory.

**What they ask:** What is the per-symbol information rate of a stationary process? h = lim H(X_n | X_{n-1}, ..., X_1).

**What they answer:** For stationary ergodic processes, the entropy rate exists and equals the conditional entropy.

**What they DON'T ask:** How entropy of block-averaged compositions (not joint block entropy) behaves under geometric-mean decimation.

**Our relation:** Different quantity. Block entropy H(X_1, ..., X_M) is about the joint distribution. Our entropy H(x̄_M) is about the marginal distribution of the block-averaged composition. These are related but not the same. We're measuring something the entropy rate literature doesn't directly address.

### Territory 5: Diversity Indices in Ecology (Shannon-Wiener)

**Who:** Shannon & Weaver (1949), Simpson (1949), Hill (1973), Chao & Jost (2012), Chao et al. (2014, iNEXT).

**What they ask:** How do you compare diversity across communities with different sample sizes? How does diversity change over time?

**What they answer:** Hill numbers (effective species counts parameterized by order q) unify all common diversity indices. Coverage-based rarefaction/extrapolation (iNEXT) standardizes comparison.

**What they DON'T ask:** Whether diversity indices are invariant under geometric-mean temporal aggregation. Their temporal work focuses on fair comparison despite unequal sampling, not on invariance under aggregation.

**Our relation:** Shannon-Wiener IS Shannon entropy. Species composition IS compositional data. Ecological community monitoring IS compositional time series. EITT directly applies to ecology — if temporal aggregation of species abundances uses the geometric mean, Shannon-Wiener diversity should be near-invariant. This is testable and has immediate practical implications for biodiversity monitoring. Chao's group at CoDaWork would be a natural audience.

### Territory 6: Jensen's Inequality Refinements

**Who:** Dragomir, Pearce (classical). Recent: refinements for twice-differentiable functions (2025 arXiv).

**What they ask:** How tight can we make Jensen's bound? What does the second-order (Hessian) correction look like?

**What they answer:** For f with m ≤ f'' ≤ M, the gap between E[f(X)] and f(E[X]) can be bounded by (1/2)Var(X) times curvature bounds. Grüss-type refinements add skewness/kurtosis terms.

**Our relation:** Our Hessian footprint formula IS the second-order Jensen correction applied to Shannon entropy on the simplex. The general framework exists. What's new is applying it to compositional geometric-mean decimation and finding that the correction is tiny (0.03%) because exp and ln cancel to first order. The remainder bound is the open mathematical problem.

### Territory 7: Rényi and Tsallis Entropy Generalizations

**Who:** Rényi (1961), Tsallis (1988). Widespread in statistical mechanics and ecology.

**What they ask:** What happens to entropy when you parameterize sensitivity to rare vs. common events? (Rényi order q.)

**What they answer:** H_q = (1/(1-q)) ln(Σ pᵢ^q). Shannon is the limit q → 1. Different q values weight the tail differently.

**Our relation:** EITT is tested for Shannon (q = 1) only. Whether the invariance holds for other q is an open question. If it holds for ALL q, that's a much stronger result (invariance of the entire diversity profile). If it holds only for q = 1, that's interesting because it would mean Shannon has a special role. Either way, it's a natural next experiment.

### Territory 8: Maximum Entropy on the Simplex

**Who:** Jaynes (1957, MaxEnt principle). Recent: Compositional Maximum Entropy (CME) methods for microbiome data (2022).

**What they ask:** Given constraints, what distribution maximizes entropy? On the simplex, the uniform composition (1/D, ..., 1/D) achieves maximum entropy ln(D).

**Our relation:** The Fréchet mean x* in our data is near-uniform (xᵢ* ≈ 0.125 for D = 8). H* ≈ 2.0794, while max possible is ln(8) ≈ 2.0794. The Fréchet mean IS nearly the maximum entropy composition. This is not a coincidence — it may be telling us that the geometric mean of temporally autocorrelated compositions converges toward maximum entropy. That would be a thermodynamic interpretation of EITT.

### Territory 9: Entropy Power Inequality

**Who:** Shannon (1948), Stam (1959), Blachman (1965). Information theory.

**What they ask:** How does entropy behave under addition of independent random variables?

**What they answer:** 2^(2h(X+Y)) ≥ 2^(2h(X)) + 2^(2h(Y)). Entropy power is superadditive.

**Our relation:** Weak. EPI concerns sums of independents. EITT concerns geometric means of correlated compositions. Different operation, different structure. Not obviously connected, but the superadditivity intuition ("mixing doesn't destroy information") resonates.

### Territory 10: Rate-Distortion Theory

**Who:** Shannon (1959), Berger (1971). Lossy compression theory.

**What they ask:** What's the minimum bit rate needed to represent a source within distortion D?

**Our relation:** Speculative but provocative. EITT says temporal decimation (extreme lossy compression — throwing away most data points) doesn't destroy information content (entropy). This is the opposite of typical rate-distortion behavior. If EITT holds, the geometric mean is an "entropy-lossless compressor" for compositional time series. This could connect to optimal coding theory on the simplex.

---

## The Gap Map — What's New vs. What's Known

### They have the question, we have the answer:

1. **"How does diversity change under temporal aggregation?"** (Ecology) — We answer: it doesn't, if you use the geometric mean.

2. **"What is the compositional analogue of multiscale entropy?"** (Biomedical signal processing) — We answer: geometric-mean coarse-graining on the simplex, and entropy is near-invariant.

3. **"How tight is the second-order Jensen bound for entropy on the simplex?"** (Information theory) — We answer: the observed correction is ~0.03%, and it's deterministic (Hessian footprint).

### We have the question, they may have the answer:

1. **"Can you derive the closed-form EITT bound?"** — Jensen refinement literature + spectral theory for stationary processes may provide the tools.

2. **"Does EITT hold for Rényi entropy (all q)?"** — Ecology's Hill numbers framework provides the testing structure.

3. **"Is there a Fisher-Rao geometric explanation?"** — Information geometry on the simplex (Amari, Erb & Ay) provides the language.

4. **"Why is the correction so small?"** — The exp/ln duality is suggestive but not a proof. Chentsov's uniqueness theorem for the Fisher-Rao metric might connect.

### Nobody has asked or answered (our genuinely novel ground):

1. **Shannon entropy near-invariance under geometric-mean temporal decimation.** Not in the CoDa literature. Not in information theory. Not in ecology. Not in multiscale entropy. We looked.

2. **The Hessian footprint as a systematic, predictable residual.** The Jensen correction framework exists, but applying it to this specific setting and showing the 10,000x gap with linear bounds — new.

3. **Direction of entropy drift as a stationarity diagnostic.** Upward = stationary, downward = non-stationary. We haven't seen this used elsewhere.

4. **The exp/ln duality as mechanism for first-order cancellation.** The observation that the geometric mean and Shannon entropy share the same transcendental base, causing first-order effects to cancel — we haven't found this stated anywhere.

---

## The Honest Audit — What Could Someone Claim We Missed?

**Attack 1:** "That's just Jensen's inequality. Everyone knows concave functions do this."
**Defence:** Jensen tells you entropy goes UP under variance reduction. It doesn't tell you the change is 0.03%. The smallness is the finding, not the direction.

**Attack 2:** "Multiscale entropy already does coarse-graining."
**Defence:** Multiscale entropy uses arithmetic mean (not CoDa-correct) on scalar time series (not compositions). Our setting is geometrically and structurally different.

**Attack 3:** "Shannon-Wiener is old. This is just ecology."
**Defence:** The formula is old. The invariance under temporal geometric-mean decimation is new. Nobody in ecology has reported this.

**Attack 4:** "You only tested energy data."
**Defence:** Correct. Domain independence beyond energy is explicitly untested and we say so.

**Attack 5:** "The Hessian of entropy is well-known."
**Defence:** Yes. What's new is that it predicts the EITT residual to within reasonable accuracy, that the first-order term vanishes by exp/ln duality, and that VAR(1) bounds miss this by 10,000x.

---

## Governance

CGS-2 (n=3), GDoF 264. No new constants. All formulas are standard. The novelty is in the combination and the empirical finding, not in the individual components.
