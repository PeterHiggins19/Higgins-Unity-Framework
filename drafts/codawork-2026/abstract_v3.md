# CoDaWork 2026 Abstract — DRAFT v3

**SEND TO:** codawork2026@coda-association.org
**FORMAT:** Plain text (copy everything below the line, no formatting)
**REVISION NOTE:** Updated from v2 to incorporate the third diagnostic (coherence residual), cross-domain validation (Backblaze), and 25-error calibration catalogue. Revised April 5, 2026.

---

Title: Compositional monitoring of energy-mix drift on the simplex

Author: Peter Higgins

Affiliation: Independent researcher, Markham, Ontario, Canada

Keywords: compositional time series, perturbation, drift detection, energy mix, subcompositional coherence

Abstract:

This contribution presents a calibration study of a compositional monitoring instrument, not a finished framework. The instrument treats energy-generation portfolios as compositional data and detects structural drift using tools from compositional data analysis.

Three diagnostics are computed at each time step: total variation distance on raw proportions, Aitchison distance on log-ratio coordinates, and a coherence residual measuring cross-branch coupling in sequential binary partition decompositions. The diagnostics are not fused; metric agreement is treated as robustness and metric disagreement as diagnostic information.

The protocol is applied to publicly available electricity generation data from EMBER (CC BY 4.0) for Germany, Japan, and the United Kingdom over 2000–2025, with nine carrier types forming compositions on the 8-simplex. The coherence residual reveals that strict subcompositional coherence does not hold in these data (mean CR ≈ 0.58), and that 31% of year-to-year transitions exhibit invisible structural change — cross-branch coupling that total variation and Aitchison distance classify as stable. Cross-domain validation on hardware reliability data (Backblaze, 900,000+ drives) produces the same pattern families under different physics.

A 25-error calibration catalogue with detection tests and governance actions makes the combined instrument falsifiable. All data, code, and documentation are publicly available.

---

## Word count: 197

## Changes from v2:

- **Three diagnostics explicitly named** — v2 said "dual-metric protocol" (TV + Aitchison). v3 adds the coherence residual as the third diagnostic, matching the Conference Core Stack alignment sentences.
- **Coherence residual results included** — the spearpoint finding (strict coherence does not hold, 31% invisible structural change) is now in the abstract itself, not just the companion documents.
- **Cross-domain validation added** — Backblaze mentioned as single credibility sentence. Different physics, same mathematics — domain independence demonstrated.
- **25-error catalogue** — v2 said "17-error." v3 says 25 (E-01–E-17 active + E-18/E-19 future + ES-01–ES-06 scaling). Matches GOVERNANCE_DECLARATION and SYSTEM_MAP counts.
- **"Calibration study" framing explicit in opening sentence** — matches Conference Core Stack alignment sentence 1.
- **"Not a finished framework" in opening sentence** — sets expectation immediately.
- **Keyword added** — "subcompositional coherence" added to keywords (this is now a CoDa finding, not just HUF).
- **Country-specific narrative still omitted** — available in packet and CR results document.
- **Egozcue's four points still addressed:** no HUF acronyms in abstract body, perturbation not subtraction, simplex not constant-sum, concentration linked to effective diversity (implicit in CR).

## Notes for Peter (do not send)

- Abstract went from 208 → 197 words. Even tighter.
- This version contains the actual result (CR ≈ 0.58, 31% structural), not just the claim. Reviewers can evaluate evidence in the abstract itself.
- If committee already has v2, send: "Revised abstract incorporating new empirical results (third diagnostic computed, cross-domain validation completed). Same title, same data, stronger evidence."
- The three alignment sentences from the Conference Core Stack are all present: calibration study (sentence 1), three diagnostics (sentence 2), 25-error catalogue (sentence 3).
