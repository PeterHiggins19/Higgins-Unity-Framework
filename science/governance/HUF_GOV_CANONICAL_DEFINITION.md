# HUF-GOV — Canonical Definition

**Issued:** 2026-04-15
**Author:** Peter Higgins
**Status:** Canonical. This is the design statement of HUF-GOV. Every other governance document in the repo should be read as an unpacking of the five clauses below.

## The definition

> **HUF-GOV is a tool that produces a verifiably clean usable output to a known degree of certainty; the diagnostic of the output is open to interpretation by expert decision and open to modification by expert judgment.**

One sentence. Five clauses. Each load-bearing.

## The five clauses unpacked

### 1. A tool

Not a framework. Not a theory. Not a method. A tool.

The noun choice matters. Tools are built, verified, and used. They are not proved and accepted. They are not doctrinal. They are not self-contained explanations of the world. They are instruments that let a human do work they could not do as well without.

Every downstream property inherits from this. Tools have makers, versions, maintenance cycles, user documentation, known failure modes, sharpness that can be restored. The language of tools is the language of engineering, not of philosophy.

This is consistent with the framework's lineage: the instrument was built at the Binaural Test Lab because the measurement required it, then generalized because the mathematics turned out to apply elsewhere. HUF-GOV is an instrument. It reads. It reports. It does not conclude.

### 2. Verifiably clean usable output

Three compressed requirements. Each is a design obligation.

**Clean** means unambiguous. The output of HUF-GOV is not a narrative or a qualitative judgment. It is a number, a flag, a ratio, a bounded residual — something a second person reading the same output will interpret as the same thing. This is why `EITT_HESSIAN_BOUND.md` has explicit constants rather than vague claims. This is why drift flags carry their exact `d_A` values.

**Usable** means actionable at the point of decision. The output is not an intermediate quantity that requires further transformation before a decision can be made. It is the number the expert takes to their judgment call. This is why `EITT_WHY_IT_WORKS.md §7` separates shape from magnitude — shape functionals are the usable outputs; magnitude functionals are the scale on which those outputs should be read.

**Verifiable** means the user does not need to trust the tool. They can check. The `ai-refresh/HUF_INTEGRITY_MANIFEST.json` has SHA-256 checksums. The `ai-refresh/HUF_FAST_REFRESH.json` is the single source of truth against which any document can be cross-referenced. The four-AI cold-start test was itself a verification ritual: can a stranger AI read the repo cold and produce correct answers? Yes. That is the verifiability requirement operationalized.

### 3. Known degree of certainty

Bounded precision is part of the contract. HUF-GOV does not claim universal validity. It claims validity under specific, stated conditions, and quantifies what uncertainty remains when those conditions hold.

This is what the Hessian bound does. `|δ_M| ≤ (D-1) σ_A² / (2δM) + O(M^{-3/2})` is the "known degree" in mathematical form. Under the three stated assumptions (A1 interior bound, A2 finite variance, A3 mixing), the residual is bounded by an explicit constant. Outside those assumptions, the bound does not apply.

This is also what `EITT_SAFETY_BOUNDARIES.md` does. The safety document names the regimes where the certainty holds — stationary autocorrelated data with proportions bounded away from zero — and names the regimes where it does not hold, with specific failure-mode signatures for each. A clinical trial with 15 patients and 3 time points is explicitly out of scope. A seasonal hydrological regime change is explicitly out of scope within the stationary analysis.

The certainty is bounded. The bounds are published. The user can check their own application against the bounds before trusting the output.

### 4. Diagnostic open to interpretation by expert decision

The output of HUF-GOV is a diagnostic, not a conclusion.

The flag says `d_A = 9.0712 for Germany 2023–2024`. What that means for energy policy, for infrastructure investment, for regulatory action — that is the domain expert's call. The tool does not overreach into meaning.

This is the resolution of what might otherwise look like unfalsifiability. HUF-GOV is not refusing to be checked; it is refusing to make a claim outside its competence. The output itself is verifiably clean and bounded in certainty. The interpretation is human because the interpretation is domain-specific and value-laden, and the tool does not have domain expertise or values. The expert does.

The open-loop doctrine is an expression of this clause. The scientific-measurement path (HUF-GOV) cannot close its own loop because closure is interpretation, and interpretation is not the tool's to make.

### 5. Open to modification by expert judgment

The tool itself is not frozen.

Safety boundaries are a living document. When a new failure mode is observed in the wild, it goes into the safety document. When a new domain is validated, the applicability claims are extended. When a new failure mode emerges that the current methodology cannot handle, the dormant folder preserves the attempt while the main repo records the retraction.

The tool evolves under expert use. Experts who find its limits contribute corrections. The maintenance is open, the versioning is explicit (semantic versioning in the integrity manifest), and the scope is explicitly revisable.

This is the opposite of a black box. Black boxes freeze at deployment and age badly. HUF-GOV is designed to age well — the tool you use in 2027 will be the tool with 2026's mistakes corrected.

## What this definition makes clear

**HUF-GOV is not automated decision-making.** It does not replace experts. It provides experts with cleaner inputs to their decisions.

**HUF-GOV is not a closed theory.** It does not claim universal truth. It claims bounded utility under stated conditions.

**HUF-GOV is not unfalsifiable.** Its outputs are verifiably clean and quantified in certainty. Its claims are checkable. Its failure modes are published. It refuses only claims that would be outside its competence — namely, claims about what its outputs mean in domains it does not know.

**HUF-GOV is not static.** It evolves. The relationship between the tool and its users is reciprocal: users contribute refinement, the tool gains discipline and reach.

## Relationship to HUF-CLS

HUF-CLS (closed-loop system) is the other path from the ADAC fork. Where HUF-GOV observes and reports, HUF-CLS acts. HUF-CLS takes the error signal and drives correction automatically.

HUF-CLS has the same architectural plumbing as HUF-GOV up to the fork, but its output is control action, not a diagnostic. The five-clause definition above does not apply unchanged to HUF-CLS because HUF-CLS is permitted to close the loop, which means its output is not purely diagnostic. The certainty bounds apply, the verifiability requirement applies, but the interpretation clause shifts — closed-loop systems interpret their own outputs by design.

HUF-CLS is not the subject of this document. This document defines HUF-GOV specifically, and deliberately. The scope separation between the two is why they exist as distinct architectures.

## Cross-references

- `ai-refresh/HUF_FAST_REFRESH.json` — the canonical definition is quoted there in the `identity` section with a five-clause unpacking
- `science/eitt/EITT_HESSIAN_BOUND.md` — the quantified-certainty clause operationalized as a theorem
- `science/eitt/EITT_SAFETY_BOUNDARIES.md` — the bounded-certainty clause operationalized as failure-mode documentation
- `science/eitt/EITT_WHY_IT_WORKS.md` — the verifiably-clean-usable-output clause operationalized as the shape/magnitude decomposition
- `briefings/THE_LINEAGE.md` — the founding narrative, including the ADAC moment where HUF-GOV was seeded
- `ai-refresh/MASTER_LINEAGE.json` — the arc showing how the five clauses were assembled over three years of engineering and theory work

## Status

This sentence is the design statement of HUF-GOV. It should be quoted verbatim in any paper, abstract, or presentation that asks "what is HUF-GOV?" The unpacking in this document can be cited as supplementary but the one-line definition is the canonical form.
