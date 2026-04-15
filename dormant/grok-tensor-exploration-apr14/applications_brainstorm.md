# Applications Brainstorm — Domains Worth Trying EITT On

**Status:** Dormant. Sketched protocols, none executed. Kept as a candidate work list for anyone wanting to extend EITT beyond the four published proofs.

## Format

For each domain: the compositional quantity, the block-decimation interpretation, the plausibility of (A1) and (A3) from `EITT_HESSIAN_BOUND.md`, and what would be learned.

---

## Turbulence

- **Compositional quantity.** Normalized Reynolds-stress tensor components (six-component traceless tensor, renormalized to sum to 1), or turbulent kinetic energy partitioned across wavelength bands.
- **Decimation interpretation.** Block averaging over hourly or large-eddy-simulation time steps → daily or seasonal statistics.
- **(A1) interior bound.** Plausible for fully developed turbulence away from walls. Fails in laminar sublayers.
- **(A3) mixing.** Strong by construction in fully developed turbulence.
- **What would be learned.** Whether EITT's Shannon residual tracks the Kolmogorov K41 scaling of the energy cascade, or whether it captures intermittency corrections the K41 picture misses. Published K41 data from atmospheric surface layer or DNS of homogeneous isotropic turbulence would suffice for a pilot.

## Hydrology

- **Compositional quantity.** Runoff source fractions (quickflow, baseflow, interflow, snowmelt) from hydrograph separation.
- **Decimation interpretation.** Daily gauge compositions → monthly → seasonal.
- **(A1) interior bound.** Fails seasonally — snowmelt goes to zero in summer, quickflow dominates during storms. This is a domain where `δ` drops to ~0 cyclically.
- **(A3) mixing.** Strong on annual cycle, weak on event cycle.
- **What would be learned.** Whether the bound holds within season (stationary regime) and breaks across season boundaries (regime change). This is a natural test for the drift-detection side of the framework: flag phenological transitions and anthropogenic catchment changes.
- **Candidate dataset.** USGS daily streamflow with hydrograph separation, or the CAMELS catchment benchmark.

## Oceanography

- **Compositional quantity.** Water-mass source fractions from optimum multiparameter analysis (OMP): North Atlantic Deep Water, Antarctic Intermediate Water, Antarctic Bottom Water, etc.
- **Decimation interpretation.** Profile-by-profile fractions → seasonal or basin-mean fractions.
- **(A1) interior bound.** Plausible in ocean interior. Fails near frontal zones where a water mass drops to zero.
- **(A3) mixing.** Good on climatological scales. Weak during eddy-shedding events.
- **What would be learned.** Whether EITT distinguishes climatological mean states (expected invariance) from decadal variability modes like the AMO or ENSO (expected drift flags). Candidate dataset: Argo float climatologies.

## Atmospheric composition

- **Compositional quantity.** Normalized greenhouse-gas or aerosol source fractions (anthropogenic CO₂, natural CO₂, fossil CH₄, biogenic CH₄, sea-salt aerosol, mineral dust, etc.) from inverse modeling or tracer-tracer analysis.
- **Decimation interpretation.** Hourly station data → monthly → annual.
- **(A1) interior bound.** Often fails for minor species (e.g., volcanic aerosol is zero most of the time).
- **(A3) mixing.** Strong on synoptic scale. Weak across eruption events.
- **What would be learned.** Whether EITT can serve as an emission-attribution consistency check for inverse models, separating modeled regime changes from artifacts of finite observational coverage.

## Climate scenarios (already in Proof 3)

- **Compositional quantity.** NGFS energy-carrier fractions per scenario pathway.
- **Already tested.** This is `proof_3_ngfs` in `FAST_REFRESH`. 1.8% geometric vs 14.2% arithmetic mean variation over 5-year windows.
- **What would extend this.** Apply EITT across the full CMIP6 scenario ensemble (SSP1-1.9 through SSP5-8.5) and track whether the residual flags scenario families that make inconsistent carrier-mix assumptions.

## Quantum billiards (speculative, see `tensor_escalation.md` §4)

- **Compositional quantity.** Normalized eigenstate probability densities `|ψ_n|²` binned over phase-space cells.
- **Decimation interpretation.** Block averaging over consecutive eigenstates ordered by energy.
- **(A1) interior bound.** Depends on scarring — fully ergodic eigenstates are interior, scarred ones concentrate and drive `δ → 0`.
- **(A3) mixing.** The analogue of mixing for eigenstate sequences is spectral statistics. For chaotic billiards (Wigner–Dyson), strong. For integrable billiards (Poisson), weak.
- **What would be learned.** Whether EITT distinguishes integrable from chaotic billiards via the residual being inside or outside the Hessian bound. This would be a genuine application — not an analogy — and is the most interesting item on this list scientifically. Requires actual eigenfunction computation (finite-element Helmholtz solver), which has not been done.

## Ecology and community composition

- **Compositional quantity.** Normalized species abundances in an ecological community.
- **Decimation interpretation.** Sub-plot samples → plot means → site means.
- **(A1) interior bound.** Fails for rare species (`δ ≈ 1/N` for sample size `N`).
- **(A3) mixing.** Weak for spatial data — species are spatially autocorrelated but not temporally mixed in the same sense.
- **What would be learned.** Whether EITT reproduces classical diversity-scaling results (species-area relationship, Preston log-normal) from a different mathematical direction. Candidate datasets: Barro Colorado Island tree census, bird atlas data.

---

## Selection heuristic

Of the list, the three most likely to produce clean, publishable results without additional theoretical work are:

1. **Climate scenarios across CMIP6 ensembles.** Directly extends Proof 3. Data exists, code exists.
2. **Hydrological regime-change detection in CAMELS.** Tests the drift-flag side of the framework on a dataset where ground-truth regime changes are annotated.
3. **Quantum billiards.** Genuine physics application. Requires new code (Helmholtz solver), but the payoff is distinguishing EITT-as-analogy from EITT-as-real-quantum-diagnostic.

The others are all defensible but would need more preliminary work.
