# 02 — What Needs Work, What Needs Verification, What Are Possibilities

The honest status board as of 2026-04-15. Three categories.

## Needs work (committed, scheduled)

These are items where the mathematics or methodology is clear and the work is execution rather than discovery. They are on the Phase 2 roadmap (`science/eitt/EITT_PHASE_2_ROADMAP.md`) with target completion during 2026.

**Direct measurement of σ_A², δ, τ_int from raw data.** The Hessian bound's empirical check table currently back-computes `V/δ` from observed residuals. Extending `chem_eitt_pipeline.py` with `measure_aitchison_variance(X) → (V, sigma_A2, delta_min)` and `measure_integrated_autocorrelation(X) → tau_int` converts back-computation to direct measurement. Closes an explicit TODO in `EITT_HESSIAN_BOUND.md §8`.

**Hydrology validation.** Apply EITT to CAMELS catchment benchmark or USGS daily streamflow with hydrograph separation (runoff source fractions: quickflow, baseflow, interflow, snowmelt). Expected behavior: works within season (stationary), flags seasonal transitions (non-stationary), fails at `δ → 0` (snowmelt off-season). This is the first domain extension planned beyond the four proofs.

**Second external domain.** Candidate: ecological community composition or atmospheric tracer fractions. Constraint: must have time-series structure or a natural decimation axis.

**Safety boundaries maintained and extended.** `EITT_SAFETY_BOUNDARIES.md` is a living document. Every new failure mode observed in the wild goes in. Every new domain validated adds a section with domain-specific red flags. Maintenance guardrail: application expansion cannot outpace documentation of failure modes.

**Package release preparation.** Python package with `pip install`, documentation, tutorial notebooks covering the four proofs plus the safety checklist, integration tests. External-researcher-ready by Phase 2 exit criterion.

**Phase-field visualization prototype.** EMBER data as a phase-field rendering for the CoDaWork talk. Six-country grid × 25 years × nine carriers with smooth color blending. Not analytical — visual. For presentation use.

**BTL Advanced ODL lab study (proposed).** A stereo pair of Binaural Test Lab Advanced Organic Digital Loudspeakers under Smaart v9 monitoring as a physical systems cross-validation platform. Four lines of inquiry: DADC validation, EITT on measured frequency-response time series, shape/magnitude in acoustic space, HUF-GOV in operation. Hardware-dependent; proposal stage.

## Needs verification (claims outstanding)

These are claims that are stated in the framework but have not been independently confirmed. Running verification is a dependency for any formal publication.

**Five-AI literature verification.** Issued 2026-04-15, deadline 2026-04-22. Five branches:

- **Claude** — Tutte × CoDa, Hanani-Tutte × entropy Taylor expansion (combinatorial graph theory) — PENDING
- **ChatGPT** — Pawlowsky-Glahn / Egozcue / Tolosana-Delgado 2020–2025 canon review — PENDING
- **Grok** — Penrose / aperiodic order × CoDa — RETURNED (Novel, 3 near-misses, no positive hits)
- **Gemini** — KPZ universality × CoDa — PENDING
- **Copilot** — arXiv crossover and preprint discovery — PENDING

Consolidation planned 2026-04-24. Three possible outcomes: Novel (full cluster stands), Partially novel (specific pairings have prior art, restrict claims), Not novel (cluster exists in literature; framework shifts from structural-observations to applied-methodology).

**Rényi q=2 performance near boundaries (Prediction 4 in `EITT_WHY_IT_WORKS.md §5`).** The prediction states that collision entropy should outperform Shannon near simplex boundaries because its Hessian is bounded independent of `δ`. Partially tested in CheMixHub multi-lens analysis; full direct test at boundary compositions is outstanding.

**1/M scaling of the residual (Prediction 1).** The residual should decrease linearly in 1/M for moderate M and saturate at large M. Tested piecemeal across the four proofs at different M values; a direct test on a single dataset across a range of M values has not been run.

**K_eff² scaling (Prediction 3).** Concentrated compositions should be tighter than the nominal bound predicts. Supported by Japan vs France EMBER comparison; more domains would strengthen it.

**Self-lineage RWA↔HUF cross-references.** MASTER_LINEAGE.json and HUF_RELATIONSHIP.json claim specific concept continuities (e.g., "entropix" → EITT, "regimes" → HUF regime vocabulary, "v-infinity-core" → VCore stack). These claims are asserted; someone should walk the RWA concepts/ folders and verify each claim carefully.

## Possibilities (worth investigating; not promised)

These are directions the framework opens but has not committed to pursuing. They are recorded so that future work has a register of candidates.

**Hanani–Tutte parity formulation of the Hessian bound.** The second-order bound derivation uses the fact that first-order Taylor terms vanish in expectation — a parity argument. Reformulating the derivation explicitly as a parity cancellation might produce a cleaner presentation readable by topological-graph-theorists. See `dormant/grok-tensor-exploration-apr14/apr15_metallic_ratio_escalation.md`.

**Tutte-matching connection to sequential binary partition existence.** SBP theory (Egozcue & Pawlowsky-Glahn 2005) uses orthogonality conditions for balance-basis construction. Whether Tutte's matching theorem provides an alternative existence condition is an open question deserving a serious look.

**Multifractal spectrum of EITT-decimated series.** Self-similarity under geometric-mean decimation is clear; formal multifractal singularity spectrum computation on the four proofs is not done.

**Wasserstein gradient flow connection.** EITT and Wasserstein gradient flow of entropy are orthogonal operators on the simplex (EITT preserves shape, Wasserstein destroys it). Making this formal via Otto calculus or Ambrosio-Gigli-Savaré framework would situate EITT in a broader mathematical context.

**Compositional quasi-crystal interpretation.** EITT-decimated series with Fibonacci or Pell block sizes exhibit self-similar hierarchy analogous to Penrose / Ammann–Beenker inflation. Whether this is a formal correspondence or a structural analogy is an open question. See `dormant/grok-tensor-exploration-apr14/` for triaged speculation.

**Cross-domain coupling of HUF flags.** If Germany's electricity mix drift in 2023–2024 is driven by the same macro forces as Japan's generation changes in 2013–2015, the drifts should correlate in time. A multi-country coupled-drift analysis could reveal shared structural forcing.

**Compositional spectral analysis.** Treating EITT-decimated trajectories in clr space as quasi-periodic signals opens the possibility of spectral decomposition that respects simplex geometry. Connects to the Pawlowsky-Glahn / Egozcue group's compositional time-series methods.

**Application to clinical longitudinal data under proper sample-size discipline.** The safety document rules out small-cohort misuse, but longitudinal compositional clinical studies with adequate sample size (N > 100, T > 10 time points, cohort-level analysis) are a legitimate future target. Waiting for a clinical collaborator rather than pushing into the domain unilaterally.

**Quantum-chaos application to real billiard data.** The repo's quantum-information correspondence contains speculative claims (dormant). Real experimental data (microwave billiards, cold-atom many-body) would either validate the analogy or falsify it. Needs a quantum-chaos collaborator.

**RWA BTL Advanced ODL physical platform.** The proposed lab study (above, under "needs work") is also a possibility space — if the platform runs all four lines of inquiry successfully, it becomes a permanent cross-validation resource for any HUF method. If any line fails, the failure is informative.

## How to contribute to any of these

The maintenance rule in `ai-refresh/PHASE_MARKERS.json` under `operating_principles.lineage_cross_reference` says: when any new document is promoted to the main repo, the author adds an entry to MASTER_LINEAGE.json's cross-reference map identifying its RWA / H1 / or earlier-HUF ancestor.

The waffle-division rule from Phase 2 says: speculative work goes to `dormant/` with reawaken conditions; rigorous work goes to the main repo with assumptions, proof sketch, and check.

If you have a candidate contribution, the entry point is to open an issue on the public HUF repo identifying which category (work / verification / possibility) it fits and what the expected work product is.
