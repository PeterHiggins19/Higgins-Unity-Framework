# CoDaWork 2026 Abstract — DRAFT v2

**SEND TO:** codawork2026@coda-association.org
**FORMAT:** Plain text (copy everything below the line, no formatting)
**REVISION NOTE:** Updated from v1 to incorporate the union thesis and 16-error calibration framing. Revised during Grok collective review, April 3, 2026.

---

Title: Compositional monitoring of energy-mix drift on the simplex

Author: Peter Higgins

Affiliation: Independent researcher, Markham, Ontario, Canada

Keywords: compositional time series, perturbation, drift detection, energy mix

Abstract:

Monitoring frameworks typically compare observed values against external thresholds or conceptual models. None, to the author's knowledge, operates natively on compositions — tracking how the proportional allocation of a finite system evolves over time using the geometric structure of the simplex.

This contribution proposes a monitoring protocol that treats energy-generation portfolios as compositional data and detects structural drift using tools from compositional data analysis. Each reporting period produces a composition in the simplex. Change between periods is measured as perturbation rather than arithmetic difference, consistent with Aitchison geometry. The magnitude of change is quantified using the Aitchison distance.

The protocol is applied to publicly available electricity generation data from EMBER (CC BY 4.0) for Germany, Japan, and the United Kingdom over 2000–2025, with nine carrier types forming compositions on the 8-simplex. The resulting compositional time series reveal structural transitions invisible to non-compositional methods. A concentration measure related to effective diversity is computed alongside the compositional trajectory.

The central claim is that combining standard compositional tools with an explicit monitoring doctrine produces capabilities neither community can build alone. This union inherits all error sources from both sides and generates new ones; a 16-error calibration catalogue (with detection tests and governance actions) is supplied to make the combined instrument falsifiable. All data, code, and documentation are publicly available.

---

## Word count: 208

## Changes from v1:

- **Central claim rewritten** — v1 claimed "no existing monitoring framework performs compositional change detection." v2 claims the *union* of compositional tools + monitoring doctrine produces capabilities neither side builds alone. Stronger thesis, less defensive.
- **16-error calibration study mentioned** — signals to reviewers that this is a calibrated instrument, not an untested pitch.
- **"Falsifiable" added** — the instrument ships with its own failure mode catalogue.
- **Country-specific examples removed** — tightened word count. The examples are in the packet, not the abstract.
- **"Four specific ways it could be defeated" removed** — replaced by the stronger 16-error calibration framing (which subsumes it).
- **Egozcue's four points still addressed:** no HUF acronyms, perturbation not subtraction, simplex not constant-sum, concentration measure linked to effective diversity.

## Notes for Peter (do not send)

- Abstract went from 283 → 208 words. Tighter, stronger.
- If committee already has v1 and you want to update, send a one-line note: "Revised abstract reflecting additional analysis. Same title, same data, stronger central claim."
- The 16-error catalogue is the new centerpiece — engineers and mathematicians both respect calibration studies.
