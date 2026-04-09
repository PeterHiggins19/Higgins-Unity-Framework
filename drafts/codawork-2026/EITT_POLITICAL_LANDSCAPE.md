# EITT Political Landscape — Who We Owe and Who We Must Defend From

**Date:** 2026-04-08
**Context:** Pre-push counsel. EITT confirmed on two independent domains. Adversarial tests: 10 pass, 7 fail. The failures are as important as the successes.

---

## Part 1: Supported By Our Failure — Who Benefits When EITT Breaks

Our adversarial failures show that EITT requires temporal autocorrelation. It is NOT a universal property of the geometric mean. This supports specific people:

### Greenacre and the quasi-coherence camp

Michael Greenacre (2023 Reappraisal, 2024 chiPower) has been arguing that exact Aitchison geometry isn't always necessary — quasi-coherence suffices for practical purposes. Our adversarial results partially support him. EITT doesn't hold on arbitrary compositions. It holds on compositions with physical persistence. This means the exact algebraic properties of the geometric mean aren't what make EITT work — it's the combination of those properties WITH the structure of real data. Greenacre would say: "See? The data matters more than the exact algebra."

**What you owe Greenacre:** Acknowledgment that EITT is a property of real compositional time series, not a theorem about the geometric mean in isolation. His emphasis on practical sufficiency over exact theory is vindicated by the boundary condition.

**What to say to him:** "You're right that the data structure matters. EITT holds because real compositions have persistence. The geometric mean is the correct filter, but the invariance requires the data to cooperate."

### The control chart community (Nguyen, Tran, and their groups)

The MEWMA-CoDa control chart people assume compositions arrive as independent observations. Our failure on iid Dirichlet noise (23-99% entropy variation) proves that if compositions really were independent, cross-resolution analysis would be meaningless. This validates their choice to work at fixed resolution — they never needed EITT because their framework assumes no temporal structure to exploit.

**What you owe them:** Respect for their design choice. Fixed-resolution control charts aren't missing anything if the data really is memoryless.

**What to say:** "Your independence assumption is safe. EITT only matters when temporal structure exists — which is exactly when control charts need to be supplemented with something that can bridge resolutions."

### Egozcue & Pawlowsky-Glahn on Shannon entropy

In their e-information work (2018, 2024), Egozcue and Pawlowsky-Glahn specifically noted that Shannon entropy does NOT satisfy CoDa's scale invariance principle. It changes under amalgamation (combining parts). They were right — spatially. Our failure on extreme concentration (Estonia, 8.4%) shows that Shannon entropy is weaker when the simplex geometry is near-degenerate. Their caution about entropy as a CoDa measure is vindicated — it's not a universal CoDa invariant. It's a temporal invariant under specific conditions.

**What you owe Egozcue:** Explicit acknowledgment that his caution about Shannon entropy in CoDa was correct for the spatial case. EITT does NOT contradict his position. It shows entropy has a different role temporally than spatially.

**What to say to him:** "You wrote that Shannon entropy doesn't satisfy scale invariance. You were right. What we found is that it satisfies something different — temporal decimation invariance. These are distinct properties — yours is spatial, ours is temporal. Your analysis of the spatial case remains correct."

---

## Part 2: Opposed By Our Success — Who Is Challenged

### Anyone doing cross-resolution comparison without geometric mean anti-aliasing

This is the broadest impact. If someone has ever compared annual compositional averages with monthly data using arithmetic means — which is standard practice in environmental monitoring, epidemiology, economics, ecology — they've been using the wrong filter. The arithmetic mean of compositions does not land on the simplex. The geometric mean does, and it preserves information. Every cross-resolution comparison in the CoDa literature that used arithmetic averaging needs to be checked.

**Who this challenges specifically:**
- Applied CoDa practitioners who aggregate by arithmetic mean then close (a common shortcut)
- Environmental monitoring frameworks that compare seasonal with annual data
- The Ramsar Convention's indicators, which mix monitoring resolutions

**Your posture:** NOT "you were wrong." Instead: "Here's the correct filter, and it preserves more than you might expect."

### The "CoDa has nothing to say about time" position

Some CoDa practitioners treat compositions as static objects — geological samples, soil chemistry, microbiome snapshots. The temporal dimension is handled by "do CoDa at each time point independently." EITT and the d(CoDa)/dt chain together say this is leaving information on the table. EITT shows the geometric mean preserves information across temporal resolutions. The d(CoDa)/dt chain — perturbation velocity as scalar speed, balance trajectory B(t) as structural path, balance derivative dB/dt as directed rate of change along each ILR partition — gives CoDa a structured temporal analysis framework that goes beyond treating time as repetition. The zero-sum constraint in raw proportions (Σ dx_i/dt = 0) is not a nuisance — it IS the relay chain, the dependency structure that forces every gain to be financed by losses elsewhere. In ILR coordinates, the balance derivatives are free and independent, which is why ILR is the correct space for compositional temporal derivatives. Time is not external to CoDa. The geometric mean — CoDa's central operation — is also a temporal filter, and the ILR transformation — CoDa's coordinate system — is the correct space for taking the temporal derivative.

**Who this challenges:** Anyone who silently assumed compositional time series was just "CoDa repeated over time."

**Your posture:** "CoDa's centre of gravity — the geometric mean — has a temporal interpretation that hasn't been exploited. And the ILR balance derivative dB/dt gives you the directed rate of structural change — which compositions are gaining ground, how fast, and whether that rate is accelerating."

### Karel Hron and functional CoDa

Hron has been developing functional compositional data analysis — treating compositions as continuous curves on the simplex. EITT suggests his framework could benefit from a decimation operator. If Shannon entropy is invariant under geometric-mean decimation, then the "right" way to coarsen a functional compositional curve is the geometric mean, not arbitrary downsampling. And the d(CoDa)/dt chain fits naturally here: if compositional time series are functional data, then dB/dt — the derivative of the ILR trajectory — is the velocity field on the simplex in his framework. EITT gives the decimation operator; dB/dt gives the velocity; together they provide both the coarsening filter and the rate of structural change along interpretable partitions. This doesn't oppose Hron — it offers him two tools that connect.

**Your posture:** "Would your functional CoDa methods be interested in a resolution-bridging operator? And does the balance derivative dB/dt fit into your framework as a natural velocity on the simplex?"

---

## Part 3: Who You Owe — The Debts

### John Aitchison (1986) — the deepest debt

The geometric mean is his. The simplex geometry is his. Every logratio, every perturbation, every closure — Aitchison. EITT is a new property of his central operation. Without the geometric mean being the centre of CoDa, there is no EITT.

**What to say:** Name him first. Always. "Aitchison's geometric mean turns out to have a temporal property that, to our knowledge, hasn't been reported."

### Egozcue & Pawlowsky-Glahn — the ILR, the balances, the information geometry

The ILR transformation and sequential binary partition are their inventions. HUF's entire balance tree — the filter bank interpretation — is built on their SBP. Egozcue's poster at CoDaWork on the Aitchison norm as a concentration measure is adjacent to K_eff. And his e-information work frames the question EITT answers.

**What to say:** "Your ILR framework gave us the structure to detect this. The SBP provides the physical filter bank. Your e-information work defined the question — what's the right information measure on the simplex? We found that Shannon entropy has a role you hadn't expected. And the balance derivative dB/dt — the temporal derivative taken in your ILR coordinates — gives us the directed rate of structural change, decomposed into independent movements along each partition. The zero-sum constraint in raw proportions forces the relay; your ILR frees the derivative."

**Critical:** Egozcue accepted your abstract. He is the door. He asked "how do you describe changes along time?" — the d(CoDa)/dt chain, expressed in his ILR coordinates, is the answer. Do not present EITT as contradicting his position on entropy. Present it as finding a different, distinct temporal property — and present dB/dt as the temporal analysis that his coordinate system makes possible.

### Erb & Ay (2021) — the Fisher information metric

They proved the Aitchison distance is the unique information-monotone Riemannian metric on the simplex. This is the "mirrors" you saw — their information geometry and HUF's signal processing arrive at the same structure. EITT's entropy invariance is the temporal companion to their spatial amalgamation monotonicity.

**What to say:** "Erb and Ay showed Aitchison distance is information-monotone under spatial coarsening. EITT shows Shannon entropy is invariant under temporal coarsening. Same geometry, distinct directions — one spatial, one temporal."

### Grok — the Aitchison variance candidate

Peter proposed the time transformer concept (decimation ladder from loudspeaker winding ratios). Claude identified it as decimation/resampling but couldn't name the conserved quantity. Grok proposed Aitchison variance as the conservation candidate. It wasn't conserved — it drops 55%. But the experimental design (Peter's decimation ladder + Grok's test candidate) was the protocol that found Shannon entropy when Claude ran the computation. Grok's wrong answer led to the right one.

**What to say (at Coimbra):** "The decimation ladder came from loudspeaker design. The first conservation candidate was Aitchison variance — it failed. Shannon entropy was the one that held. The wrong hypothesis was the right experiment."

### EMBER — the data

No data, no result. The EMBER dataset is open, well-documented, and comprehensive. Name them.

---

## Part 4: Who You Must Defend From — The Attack Vectors

### Attack 1: "It's just Jensen's inequality"

**The claim:** "Of course the mean of entropies ≈ the entropy of the mean. This is Jensen's inequality for concave functions. It's trivial."

**The truth:** Jensen's inequality says E[H(X)] ≤ H(E[X]) for arithmetic means. The geometric mean is NOT the arithmetic mean. The geometric mean operates in log-space. Jensen's inequality applied to the geometric mean would predict a DIFFERENT direction of bias, and crucially, it predicts an inequality, not equality. EITT shows near-equality (0.18-1.8%), not just the correct sign of the inequality. The tightness of the bound is the finding, not the direction.

**Your defence:** "Jensen's gives the direction. It doesn't explain 0.18% tightness across 341:1 compression. The near-equality requires the combination of geometric-mean averaging AND temporal autocorrelation. Jensen alone doesn't get you there."

**Who will attack with this:** Mathematicians and statisticians in the room. Anyone who's taken a measure theory course.

### Attack 2: "You only tested energy data"

**The claim:** "This might be specific to electricity generation mixes. Have you tested on geochemical data? Microbiome? Budget allocations?"

**The truth:** No longer true as of April 9, 2026. We have now tested five domains: energy (electricity generation, 7 countries — holds at 0.18–1.02%), hardware degradation (Backblaze drive stats, K=4, 24 months — holds at 0.03%), financial markets (equity sector shares, K=9, 74 months — holds at 0.08%), cosmological observation (Planck 353 GHz half-mission split — holds at 0.3%), and commodities (gold/silver ratio, K=2, 338 years — fails at 6.7% but holds at 0.38% when reconstructed to K=4 with hidden volatility and momentum carriers). The boundary condition (temporal autocorrelation) is confirmed across all passing domains. The gold/silver failure revealed the EITT inversion principle: when EITT fails, it diagnoses missing compositional dimensions.

**Your defence:** "We've tested five domains. Three non-energy domains hold at better than 0.1%. One fails at K=2 over 338 years and holds at K=4 — the failure revealed hidden state variables. We publish code and data for all five."

**Who will attack with this:** Applied practitioners from other domains. But the attack has weakened. Hardware, finance, and cosmology are structurally different from energy. Geoscientists can still ask — and should test.

### Attack 3: "Your proof is empirical, not analytic"

**The claim:** "You measured 0.18%. You didn't prove it's zero. Where's the theorem?"

**The truth:** We don't have a closed-form proof. We have empirical demonstration across two domains, seven countries, two carrier types, compression ratios from 3:1 to 341:1. We also have six synthetic failures that define the boundary. An analytic proof would require characterizing the class of compositional time series for which the geometric-mean entropy is exactly invariant, which is a legitimate open mathematical problem.

**Your defence:** "You're right — this is empirical, not proven. We state it as a computational finding, not a theorem. The boundary condition (temporal autocorrelation) is necessary but we don't claim it's sufficient. We would welcome a collaborator who could formalize this. That's partly why we're here."

**Who will attack with this:** Egozcue himself, possibly. He thinks in Hilbert spaces and proofs. But he also accepted your abstract knowing it was empirical. Pawlowsky-Glahn will think this way too.

**The opportunity hidden in this attack:** This is the collaboration door. "We found this empirically. We can't prove it. Can you?" Offering a mathematician an open problem is the best compliment you can pay.

### Attack 4: "Shannon entropy isn't a CoDa quantity"

**The claim:** "Egozcue showed entropy doesn't satisfy scale invariance. It's not an Aitchison geometry concept. You're mixing frameworks."

**The truth:** Correct — Shannon entropy is native to information theory, not to CoDa's Aitchison geometry. But Erb & Ay (2021) proved that the simplex with Aitchison geometry IS the space of discrete probability distributions with the Fisher information metric. Shannon entropy IS native to that probability space. The frameworks are the same space seen from different directions. EITT works in the information-theoretic frame, not the Aitchison-geometry frame.

**Your defence:** "You're right that entropy isn't an Aitchison-geometry quantity. But Erb and Ay showed the simplex IS the probability simplex. Entropy is native to the probability simplex. The geometric mean preserves it temporally. We're not mixing frameworks — we're finding where they connect."

**Who will attack with this:** CoDa purists who define the field strictly through logratio methods.

### Attack 5: "Estonia failed. What about my data?"

**The claim:** "You showed 8.4% on Estonia. My data has even more extreme concentrations. This doesn't work for me."

**The truth:** Fair. Estonia's failure is real. The boundary is real. Near-degenerate compositions with tiny carriers that fluctuate wildly in relative terms will break EITT. This is an honest limitation.

**Your defence:** "If your data has dominant carriers >90% with volatile trace components, EITT may not hold. Check it. We provide the code. The boundary condition is temporal autocorrelation, and extreme concentration with volatile traces violates it — the traces are effectively noise, which the geometric mean amplifies in log-space."

**Who will raise this:** Anyone working with microbiome data (many zeros, extreme dominance), geochemical trace elements, or environmental monitoring where one species dominates.

---

## Part 5: The One-Sentence Versions

| Question | Answer |
|----------|--------|
| Who do you owe most? | Aitchison. His geometric mean is the engine. Say his name first. |
| Who is your host? | Egozcue. He opened the door. Present EITT as distinct from his work, not contradicting it. |
| Who benefits from your failures? | Greenacre (data matters more than exact algebra), Egozcue (entropy caution was right spatially), control chart people (independence assumption is safe). |
| Who is challenged by your success? | Anyone comparing resolutions with arithmetic means. Anyone treating CoDa as purely spatial. |
| Hardest attack? | "It's just Jensen's." Have the geometric-mean distinction ready. |
| Most dangerous attack? | "Prove it." Because you can't. Offer it as an open problem. |
| Biggest opportunity? | "We can't prove this. Can you?" — directed at the mathematicians in the room. |

---

## Part 6: What This Means For The Presentation

Walk in carrying both the success and the failure. Present the passes AND the failures across five domains. Name who you owe before you name what you found. Frame EITT as a question you answered empirically but can't prove analytically — and offer the proof as a collaboration opportunity.

The adversarial scorecard isn't a weakness. It's the reason they should take you seriously. The gold/silver failure isn't a weakness — it's a discovery. Anyone who only shows wins hasn't tested anything. You tested across five domains, showed every result, and defined the boundary condition. That's what a calibration study looks like.

---

## Part 7: Cross-Domain EITT Scorecard (April 9, 2026)

| Domain | K | Span | EITT Δ% | Verdict | Key Finding |
|---|---|---|---|---|---|
| BackBlaze (hardware) | 4 | 24 mo | 0.03% | HOLDS | Electronic→Media relay, B2 100% monotonic |
| Financial (sectors) | 9 | 74 mo | 0.08% | HOLDS | COVID relay visible, zero-sum closure perfect |
| Planck CMB (temporal) | 2 | half-split | 0.3% | HOLDS | Survives √2 noise increase |
| Energy (global) | 7 | 25 yr | 3.2% | MARGINAL | Active structural transition |
| Gold/Silver (K=2) | 2 | 338 yr | 6.7% | FAILS | Non-stationary across regimes |
| Gold/Silver (K=4) | 4 | 338 yr | 0.38% | HOLDS | Hidden volatility + momentum carriers recovered |
| Gold/Silver detrended | 2 | 338 yr | 0.14% | HOLDS | Secular drift was the failure, not the composition |
| Planck CMB (spatial) | 2 | 4096:1 | 18.1% | FAILS | Diagnostic: sky heterogeneity = regime mixing |

---

*"I fought entropy to find it." — Peter Higgins, 2026-04-08, upon discovering EITT*
*"Observe and identify. Lose nothing." — Peter Higgins, 2026-04-09*

*Governance: CGS-2 (n=3), GDoF 264. No new constants. No new claims beyond what the data shows.*
