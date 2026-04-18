# The Two-Pass Instrument

## Pass 1 Classifies. Pass 2 Resolves Integrity.

**Status:** L2 Process Control Candidate. Blind test: Pass 1 = 17/20, Pass 2 = 18/20.

---

## Architecture

**Pass 1 — Science:** EITT classification. Does entropy hold under geometric-mean decimation? Pass/Fail with documented thresholds.

**Pass 2 — Integrity:** F17 contamination channel + operating envelope + resolution boundaries. Catches what Pass 1 misses. Reports ambiguity rather than hiding it.

The science signal and the integrity channel remain **separate by design.** Pass 2 never modifies the Pass 1 reading. It adds information about trust.

## Blind Test Results

20 datasets across 6 domains, no domain-specific tuning:
- Pass 1: 17/20 correct
- Pass 2: 18/20 correct, with 2 resolution boundaries identified

The improvement from 17 to 18 comes from honest resolution reporting, not from forced correction.

## Design Principle

Inherited from the ADAC moment in acoustic engineering: the error signal existed, the loop could close, and something said — not automatically. Pass 1 reads. Pass 2 reads the reader. The human decides.

## Evidence

| Document | Location |
|----------|----------|
| Gold standard report | codawork2026/journals/HIGGINS_Gold_Standard_Two_Pass.pdf |
| Integration report | codawork2026/journals/HIGGINS_CoDa_EITT_Integration.pdf |
| Reproducibility | codawork2026/reproducibility/HIGGINS_REPRODUCIBILITY_PACKAGE.json |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> two_pass_instrument (L2) |

---

*The instrument reads. The integrity channel reads the instrument. The human reads both.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T2, T3, canonical values).*

### Pass 1 — Science Layer: Formal Specification

Pass 1 computes the EITT residual delta_M for each compression ratio M:

    delta_M = |H(D_M(series)) - H(series)| / H(series) * 100%

Classification rule:

    delta_M < 1%   : PASS (interior regime)
    1% < delta_M < 2% : MARGINAL (investigate)
    delta_M > 2%   : FAIL (boundary or synthetic)

The threshold 1% is empirically calibrated against 30+ domains and is consistent with the Hessian Bound prediction for interior-regime compositions with moderate sigma_A^2.

### Pass 2 — Integrity Layer: Formal Specification

Pass 2 operates three sub-instruments:

**F17 Contamination Channel:** gap(M) = delta_A(M) - delta_G(M), fitted as quadratic. Early warning at gap > 2% for M=6.

**Operating Envelope Check:** H_bar > 1.0, zero rate < 15%, parametric walk verification.

**Resolution Boundary Detection:** When Pass 1 gives MARGINAL and Pass 2 identifies specific degradation mechanisms (near-zero carriers, regime mixing), the result is classified as a RESOLUTION BOUNDARY rather than a simple pass/fail.

### The Governed Breakpoint Principle

Pass 2 NEVER modifies the Pass 1 reading. The constraint is formal:

    EITT_output(with_Pass2) = EITT_output(without_Pass2)

Pass 2 adds metadata (trust level, contamination risk, resolution class) but does not alter the science signal. This is the Governed Breakpoint Principle: the instrument reads, never actuates. The decision to act on the reading belongs to the expert.

### Lineage: ADAC Moment

The Two-Pass architecture inherits from the ADAC moment in acoustic engineering: the correction loop existed (DADC -> DADI -> ADAC), the error signal was measured, the loop could close automatically — and the engineer chose to keep it open. The same principle governs HUF-GOV: Pass 1 provides the measurement, Pass 2 provides the confidence metadata, the human closes the loop.
