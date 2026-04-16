# April 15 Metallic-Ratio Escalation — Second Installment

**Status:** Dormant. Peter pasted a Grok session from 2026-04-15 that extended beyond the literature-verification task into a cascade of derivations on cut-and-project framing, metallic ratios (golden, silver, bronze, nickel), and an "EITT-KPZ scaling exponent." The substantive piece (literature verification) was filed properly in `briefings/lit-verification-001/GROK_LIT_VERIFY_001_RESULTS.json`. This file preserves the exploratory material with honest triage.

---

## What was kept

**The literature verification result.** "Novel" verdict for Penrose × CoDa with three properly classified near-misses. Filed as `GROK_LIT_VERIFY_001_RESULTS.json`. This is the clean deliverable and the real contribution of the session.

**The related-work paragraph.** Grok drafted a ready-to-paste related-work paragraph citing Mazáč (2023), Irwin et al. (2017), and StackExchange as incomplete prior work on self-similarity in aperiodic contexts. Usable for a future structural-observations paper. Reproduced below for reference:

> While aperiodic order and self-similar inflation rules have been extensively studied in pure mathematics and theoretical physics, no prior work has connected these concepts to compositional data analysis or entropy-invariant coarse-graining on the simplex. Mazáč (2023) developed efficient algorithms for computing exact patch frequencies in rhombic Penrose tilings and extended the method to Ammann–Beenker tilings using dualisation and algebraic-integer rings, but the treatment remains strictly geometric and contains no reference to compositional vectors, Aitchison geometry, geometric-mean decimation, or Shannon entropy invariance. Similarly, Irwin et al. (2017) explored quasicrystalline symbolic codes built from E₈ projections and 3-simplex integers in the context of a proposed unification of physics and number theory; although the term "simplex" appears, it denotes geometric tetrahedra rather than probability simplices, and the paper makes no mention of CoDa, EITT, or entropy-preserving time-series aggregation. Informal discussions in the physics community (e.g., Physics StackExchange threads on fractal properties of quasicrystals) likewise address self-similarity in Penrose tilings but stop short of any linkage to statistical or compositional frameworks.

**The phrase "entropy-invariant coarse-graining on the simplex."** Peter introduced this in the same message. It's a clean, accurate, one-line descriptor of what EITT is. Worth adopting as a consistent phrase in the repo going forward; does not require a separate file.

---

## What went to store

The rest of the session produced a pattern of derivations that look like independent results but are actually one observation repeated at different parameter values. Honest triage below.

### 1. The "cut-and-project analogue" framing

Grok framed EITT as "the compositional cut-and-project analogue" by pointing out that the clr transform lifts the simplex into a Euclidean subspace, block averaging happens in that subspace, and closure projects back onto the simplex — structurally parallel to the higher-dimensional lift, windowing, and projection that generate quasicrystal point sets from periodic lattices.

**What's real.** The structural parallel is legitimate. Lift → average-in-lift → project-back is the generic shape of both operations.

**What's not.** The parallel is an *analogy*, not an *identification*. The cut-and-project construction of quasicrystals uses specific irrational projection windows to guarantee aperiodicity; EITT doesn't. The clr embedding is isometric but rational; it doesn't involve irrational projection angles. Calling EITT "the compositional cut-and-project analogue" (definite article, noun phrase) overstates what the structural parallel supports.

**Disposition.** The clean form is "EITT and cut-and-project share a lift-average-project structure" — that's defensible. The escalated form "EITT is the cut-and-project analogue" is aspirational. Keep the defensible form in mind for informal discussion; don't promote the escalated form into repo claims.

### 2. Metallic-ratio block-size derivations (golden / silver / bronze / nickel)

Grok ran four parallel derivations showing that if you choose EITT block sizes from the Fibonacci / Pell / Bronze / Nickel integer sequences (which converge to the golden / silver / bronze / nickel ratios respectively), you get a hierarchical coarse-graining whose block-size ratio approaches the corresponding metallic ratio.

**What's real.** Each derivation is a valid algebraic substitution. Fibonacci numbers converge to φ by standard Binet analysis; Pell to δ; and so on. No objection at that level.

**What's not.** These are not four independent results. They are one observation — "if you pick block sizes whose ratios converge to some irrational λ, the hierarchy has scale ratio approaching λ" — substituted into four specific λ values. The "derivation" at each metallic ratio is the same three-step algebra with a different irrational plugged in. Treating them as a progression (golden → silver → bronze → nickel) creates the appearance of cumulative structure where there is none.

**Also.** The claim that metallic-ratio block sizes produce "exact Penrose-style / Ammann-Beenker-style self-similarity" for EITT confuses two different things. Penrose inflation is a specific deterministic geometric rule with local matching constraints that force aperiodicity. EITT with Fibonacci block sizes is just EITT applied at a specific sequence of block lengths. The hierarchies are structurally analogous at a high level but are not the same mathematical object.

**Disposition.** The one-line honest statement — "EITT decimation can be applied iteratively at any sequence of block sizes; sequences derived from integer recurrences whose ratios converge to quadratic irrationals produce hierarchies with asymptotic scale ratios equal to those irrationals" — is true and not worth a file. The escalated claim — "EITT embeds Penrose / Ammann-Beenker / bronze / nickel inflation directly" — is rhetoric on top of algebra.

### 3. "EITT-KPZ scaling exponent"

Grok derived that the leading entropy residual `δ_M ~ 1/M` under EITT, compared this to the KPZ growth exponent `β_KPZ = 1/3`, and asserted a "scaling exponent `β_EITT = 1`" as a parallel structural quantity.

**What's wrong with this comparison.** The two exponents are not comparable quantities.

- `β_KPZ = 1/3` is a universality-class exponent for a stochastic interface-growth process. It describes how height fluctuations scale with time in the presence of noise and nonlinearity. It's a statement about the statistics of a random process.
- `β_EITT = 1` (Grok's label) is the rate of CLT variance shrinkage for a deterministic operator. It follows trivially from the fact that block-averaging reduces variance by 1/M under any reasonable stationarity assumption.

Calling both "β" and putting them in the same table implies they're the same kind of object. They aren't. The first is a universality exponent; the second is an algebraic consequence of the CLT. The framing borrows physics prestige without doing physics work — exactly the pattern flagged in the April 14 adversarial review of the OTOC analogy.

**What might be real.** If compositional drift interfaces do exhibit universal fluctuation scaling (which is what the KPZ leg of the five-object cluster originally proposed), that exponent would need to be *measured* on real data. It would not be derivable by substitution into the second-order Hessian bound, because the second-order bound describes a deterministic operator while KPZ describes a stochastic one.

**Disposition.** The "β_EITT = 1 = KPZ exponent" claim should not appear in any repo document. The KPZ leg of the five-object cluster remains conjectural and requires actual measurement on interface-like compositional data, not algebraic derivation.

### 4. Quasicrystal physics applications

Grok proposed applying EITT to: atomic occupation fractions in high-entropy alloys, diffraction-pattern prediction in quasicrystal phases, quasicrystal growth modelling, and quantum many-body quasicrystals in cold atoms.

**What's real.** Each of these domains does contain compositional structure that EITT could in principle handle. Alloy mole fractions are simplex-valued. Diffraction intensities are nonnegative and can be normalized. These are legitimate potential validation domains.

**What's not.** Proposing an application is not the same as validating it. None of these was worked out beyond a paragraph of description. The quantitative connection between EITT's entropy preservation and diffraction-pattern sharpness in quasicrystals is assertion, not derivation.

**Disposition.** Add "alloy compositional monitoring" and "quasicrystal phase diagrams" to the candidate-domain list in `applications_brainstorm.md` (adjacent file in this same dormant folder). Flag as speculative. Do not promote to repo claims without actual data-driven validation.

---

## What to do with the Fibonacci/Pell self-similarity observation

The one piece of this material that could legitimately be promoted to the main repo, if anywhere, is the observation that iterative EITT decimation at Fibonacci-sequence block sizes produces a hierarchy with asymptotic scale ratio `φ`. This is a genuine corollary of the shape/magnitude decomposition from `EITT_WHY_IT_WORKS.md §7`: since shape functionals are invariant under any block-size choice, they are in particular invariant at Fibonacci block sizes, and the resulting hierarchy has the quasicrystal-inflation scale ratio asymptotically.

**However.** This corollary is a restatement rather than a new result. It doesn't add content to §7; it just specializes §7 to a particular integer sequence. Promoting it as its own subsection would create the appearance of new content where there isn't any.

**Recommended action.** No file update. If the five-AI literature verification comes back "Novel" across all pairings, and a structural-observations paper gets written, the Fibonacci/Pell corollary can appear as a one-paragraph remark in that paper. Not a repo section.

---

## Scoreboard for the April 15 session

| Item | Status |
|---|---|
| Literature verification result (Penrose × CoDa: Novel) | Kept — filed in `briefings/lit-verification-001/` |
| Related-work paragraph for future paper | Kept — reproduced above for later reuse |
| Phrase "entropy-invariant coarse-graining on the simplex" | Kept — adopt as consistent repo phrasing |
| Cut-and-project structural parallel | Partial keep — as informal analogy only |
| Metallic-ratio derivations (golden/silver/bronze/nickel) | Stored — one observation, not four results |
| "EITT-KPZ scaling exponent β = 1" | Stored — category error between deterministic CLT rate and universality exponent |
| Quasicrystal physics applications | Stored — speculative; added to candidate-domains list |
| Fibonacci/Pell self-similarity corollary | Stored — restatement of §7, not new content |

## Why this triage matters

The April 14 dormant README committed to "waffle gets divided into keep and store" as one of the three Phase 2 guardrails. This file is that guardrail operating on the April 15 session. The discipline preserves the repo's signal-to-noise ratio: the lit verification (signal) goes into briefings where it counts; the derivation cascade (noise, with one genuine observation mixed in) goes here where it's preserved but doesn't muddle the main claims.

The five-AI novelty verification is not yet complete. Four more branches are still pending. Nothing about the five-object cluster should advance beyond "hypothesized; Grok branch clean" until the other four return. Grok's enthusiasm for derivation after the task was complete should not be mistaken for additional evidence; it's the same kind of pattern-continuation already catalogued in `tensor_escalation.md`.
