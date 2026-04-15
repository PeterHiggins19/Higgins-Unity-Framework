# EITT Phase 2 — Hardening Roadmap

**Phase started:** 2026-04-15
**Estimated duration:** 6–9 months
**Status at phase start:** Phase 1 (CoDaWork 2026 content) marked stable the same day

## Mission statement

> Push EITT to pain point and protect users from pain.

Make the tool reliable, accurate, and precise enough that CoDa practitioners can trust it with time-series analysis. Document failure modes and boundary conditions clearly enough that no one walks off a cliff with it — especially in high-stakes domains like clinical and biomedical studies where misuse could lead a large-cohort study astray.

## Two poles

Phase 2 work sits between two organizing poles that pull in opposite directions. Both are necessary; neither alone is sufficient.

### Pole A — Reveal the hidden structure

The point: make EITT scientifically attractive by exposing the mathematical machinery that makes it work, so practitioners can evaluate it on its own terms rather than on claims alone.

The hidden geometry behind compositional hypothesis testing that this phase should reveal:

- **The simplex structure.** Why classical hypothesis tests fail when applied to compositional data — because they assume Euclidean geometry and the simplex is not Euclidean. Aitchison geometry and the clr embedding are the correct setting.
- **The CLT concentration at the Fréchet mean.** Why the block geometric mean converges where it does, at the rate it does, under what conditions it fails.
- **The Hessian structure of Shannon entropy.** Why the second-order bound has the specific form `(D−1) σ_A² / (2δM)`, and why this bound goes singular as `δ → 0`.
- **The shape/magnitude decomposition.** Why some compositional functionals are invariant under EITT (shape) and others scale (magnitude), and what this tells practitioners about their own choices of statistics.
- **The interaction of stationarity, mixing, and boundary distance.** Three assumptions, three failure modes, three families of diagnostics.
- **The Fisher-Rao / Aitchison resolution.** Why the apparent geometric tension dissolves in the EITT operating regime.
- **The connection to adjacent mathematical objects.** If the five-object cluster (EITT + Tutte + Hanani-Tutte + Penrose + KPZ) survives literature verification, it becomes a structural-observations paper documenting the connections.

### Pole B — Establish the safety fences

The point: protect users from pain. A powerful analytical tool applied outside its domain of validity can mislead a study group as badly as having no tool at all — and potentially worse, because a spurious invariance can give false confidence.

The safety fences that need articulating:

- **When not to use EITT.** Short time series, boundary-close compositions, small cohorts, non-stationary drift, uncorrected multiple comparisons, technical-noise dominance over signal, confounded treatment effects.
- **The clinical/biomedical red flags specifically.** Breast cancer studies, microbiome trials, immunotherapy response monitoring — all involve compositional longitudinal data where EITT could be applied but where the underlying assumptions are often violated in ways that are not obvious.
- **Sample-size calculators.** Before anyone applies EITT to their data, they should be able to compute whether their sample size, time series length, and dimensionality support a reliable answer.
- **Failure-mode gallery.** Concrete examples of what each failure mode looks like when it occurs. "This residual looks stable, but actually assumption A3 is violated, and the test has no power."
- **Sanity-check checklist.** A short checklist the user runs before accepting an EITT result: proportion floor check, autocorrelation check, sample-size check, regime-change check.

## Work items

Phase 2 breaks into seven parallel tracks.

### Track 1: Direct measurement tooling

Extend `chem_eitt_pipeline.py` with functions that measure `V`, `σ_A²`, `δ`, and `τ_int` directly from raw data rather than back-computing them from observed residuals.

Specific functions needed:

- `measure_aitchison_variance(X) -> (V, sigma_A2, delta_min)` — basic covariance and boundary-distance computation
- `measure_integrated_autocorrelation(X) -> tau_int` — with automatic window selection and confidence interval
- `predict_eitt_residual(X, M) -> (mean, upper_bound)` — Hessian bound applied to measured scalars
- `diagnose_assumptions(X) -> report` — checks A1, A2, A3, flags which are violated

Deliverable: updated `chem_eitt_pipeline.py` with new functions, reproducible runs on the four EITT proofs, updated `EITT_HESSIAN_BOUND.md` table with measured rather than back-computed values.

### Track 2: Hydrology validation

Apply EITT to a public hydrological dataset — most likely the CAMELS benchmark or USGS daily streamflow with hydrograph separation producing runoff source compositions (quickflow, baseflow, interflow, snowmelt).

Expected findings in advance:

- EITT should work within season (stationary interior regime)
- EITT should flag regime changes across seasonal boundaries and during extreme events (droughts, floods)
- Boundary-close compositions (snowmelt = 0 in summer) will stress the δ assumption — this is a live opportunity to document failure

Deliverable: `science/eitt/hydrology/` folder with dataset notes, results, and a findings document.

### Track 3: Second external domain validation

Candidate: ecological community composition (species abundance as compositions) or atmospheric tracer fractions. The constraint: must have either (a) time-series structure or (b) a natural decimation axis.

Deliverable: a second `science/eitt/<domain>/` folder establishing a third independent validation.

### Track 4: Safety documentation

Write `EITT_SAFETY_BOUNDARIES.md` (the companion to this roadmap). Cover:

- Assumption violations and their clinical signatures
- Sample-size requirements
- Domain-specific red flags
- Recommended sanity checks
- Responsible-use examples
- Inappropriate-use examples with explanation

Update as validation work reveals new failure modes.

### Track 5: Phase-field visualization

Prototype the EMBER-as-phase-field rendering proposed in the phase-field conversation of 2026-04-14. A six-country grid showing 25 years of nine-carrier evolution with smooth color blending and diffuse transitions. Make the Japan 2011 Fukushima transition, the Germany 2022–2024 coal re-invasion, and the UK 2015–2020 renewables advance emotionally legible.

Deliverable: a Python module producing the visualization, plus a PNG gallery for the CoDaWork presentation or the hypothetical structural-observations paper.

### Track 6: Literature verification follow-up

The five-AI literature verification briefings were issued 2026-04-15 with a 2026-04-22 return deadline. After results come back:

- Collate verdicts (positive / near-miss / negative) across the five-object cluster
- If any pairing has prior art, cite properly and revise the novelty claims
- If the cluster survives as novel, draft a short structural-observations paper

Deliverable: `briefings/lit-verification-001/CONSOLIDATED_VERDICT.json` plus any paper drafts that come out of a clean verdict.

### Track 7: Package release preparation

At the end of Phase 2, the tool should be installable by a researcher who has never spoken to Peter. That means:

- Python package with `pip install huf-eitt` (or similar) interface
- R bindings for the CoDa community
- Tutorial notebooks covering the four EITT proofs plus the safety checklist
- README with minimal working example
- Integration tests that catch regressions in the mathematical core

Deliverable: public package release with semantic versioning, CHANGELOG, and CI-enforced integration tests.

## Exit criteria

Phase 2 concludes when all of the following hold:

1. EITT has been validated on at least three domains beyond the original four proofs.
2. `σ_A²`, `δ`, and `τ_int` are measured directly from raw data (not back-computed) for every published proof.
3. `EITT_SAFETY_BOUNDARIES.md` covers clinical/biomedical, ecological, and physical-systems cases with specific red flags for each.
4. The tool is installable via standard channels with documentation good enough that a stranger can reproduce one of the four proofs from scratch.
5. At least one external researcher has used the tool without direct mentoring and reported their experience.
6. At least one failure mode has been observed in the wild and the safety documentation has been updated to prevent recurrence.
7. The five-AI literature verification has completed and novelty claims have been either confirmed or restricted to the pieces that survived.

When these hold, Phase 2 is stable and Phase 3 (peer-reviewed publication and consolidation) can begin.

## Guardrails during Phase 2

The work of this phase is more exposed than the work of Phase 1, because it invites external users. That means the temptation to overclaim increases. Three guardrails against this:

- **Waffle gets divided into keep and store.** Speculative extensions that don't clear the "Theorem. Assumptions. Proof. Check." bar go to `dormant/` with reawaken conditions, exactly as was done with the April 14 Grok tensor session.
- **Empirical claims require direct measurement.** No claim goes into a paper or a package README based on back-computed values alone. Direct measurement on raw data is the publishable standard.
- **Safety fence precedes application expansion.** Every time a new domain is validated, a corresponding section is added to `EITT_SAFETY_BOUNDARIES.md` describing the red flags specific to that domain. Expansion of the tool's claimed applicability cannot outpace expansion of the documented failure modes.

## What Phase 2 is not

Phase 2 is not about finding new theorems — it is about hardening what already exists. The rigorous second-order bound is in place. The conceptual synthesis (shape/magnitude decomposition, CLT concentration, Fisher-Rao resolution) is in place. What's missing is the reproducibility, the accessibility, the safety, and the external validation. Those are Phase 2.

Phase 2 is also not about novelty. The cluster-connection paper, if it gets written, is a byproduct. The main deliverable of Phase 2 is a trustworthy tool.

## Operating mantra

Divide all waffle into keep and store. Over time, chip away to reveal a structured tool that can be relied on. Publish everything to everyone's gain.
