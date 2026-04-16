# 03 — Best Use Cases

Where HUF is ready to use today, with expected performance and sample-size guidance. Ordered from strongest fit to caveat-heavy.

## Tier 1 — Direct validated fit

Domains where HUF has been validated on real data and is ready for production use with normal care.

### Energy mix monitoring (national or regional)

**Data shape:** Time series of generation-mix compositions (coal, gas, nuclear, hydro, wind, solar, bioenergy, etc.). Monthly or finer resolution. 2+ years of history ideally.

**Sample-size guidance:** D = 6–9 carriers, M ≥ 12 for monthly → annual, expect residual ≈ 1% under stationary conditions.

**Expected performance:** Stable within-regime. Flags policy shocks, infrastructure events, demand shifts. Validated across six countries (France, Germany, Japan, Poland, UK, USA) via EMBER Proof 2. Drift flags at Germany 2023–2024 (d_A = 9.0712), Japan 2013–2014 (post-Fukushima absorption), UK 2004–2005, 2017–2018, 2019–2020.

**Caveats:** Nuclear-dominant regimes have lower K_eff and behave differently than diversified regimes. Trade-deficit countries may show drift that is really an import-composition change.

### Climate scenario downscaling

**Data shape:** NGFS Phase 4 or CMIP6-style scenario trajectories. Energy carriers summing to total primary energy. Decadal horizon.

**Sample-size guidance:** D = 6 carriers, M ≥ 5 for 5-year decimation, expect geometric residual ≈ 1.8% (vs 14% for arithmetic).

**Expected performance:** Geometric decimation preserves scenario compositional structure 8× better than arithmetic. Use for ensemble consistency checks, regime-shift detection across policy transitions, NGFS-to-MESSAGEix/REMIND hand-off.

**Caveats:** Scenarios are modeled data, not measurements. Decimation across scenario pathway bifurcations (e.g., NDC vs Net Zero trajectories branching) is non-stationary by construction.

### Electricity price monitoring (daily → annual)

**Data shape:** Daily wholesale price shares across 6+ trading zones. Long history (years+).

**Sample-size guidance:** D = 6–10 zones, M = 250+ daily observations per annual block, expect residual < 0.2%.

**Expected performance:** Extremely tight (Proof 1: 0.18% at 341:1 compression). Near-best-case for EITT.

**Caveats:** Market structure changes (merit-order reforms, interconnection capacity changes) are non-stationary and will flag.

### Hardware reliability tracking (failure-mode compositional data)

**Data shape:** Failure-mode fractions across drive populations (or general fleet reliability). Monthly aggregation across large fleets.

**Sample-size guidance:** Validated on Backblaze 900,000+ drive dataset. Per-model fleets of 1,000+ drives typical.

**Expected performance:** Same pattern families as energy data under different physics. Flags operational regime changes, batch-quality transitions.

**Caveats:** Very rare failure modes (δ → 0) need amalgamation or Aitchison-norm lens.

## Tier 2 — Strong fit, plan validation

Domains where the mathematics clearly applies and Phase 2 work is in progress. Usable now with extra verification.

### Hydrological monitoring (runoff composition)

**Data shape:** Daily or finer runoff fractions (quickflow, baseflow, interflow, snowmelt). Multi-year record.

**Sample-size guidance:** D = 4–6 flow components, M = 30+ daily → monthly. Expect < 2% within-season residual.

**Expected performance:** Works within season (stationary regime), flags seasonal transitions and extreme events. Phase 2 Track 2 validation in progress against CAMELS or USGS datasets.

**Caveats:** Snowmelt goes to zero in summer — δ → 0 problem. Use Aitchison-norm lens or segment analysis by season.

### Ecological community composition monitoring

**Data shape:** Normalized species abundances in stable ecological communities. Long-term monitoring stations.

**Sample-size guidance:** Amalgamate rare species (< 1% abundance) or use Aitchison-norm lens. D ≤ 15 after amalgamation preferred.

**Expected performance:** Well-designed monitoring protocols satisfy assumptions. Ready for application but not yet validated in Phase 2.

**Caveats:** Sampling variance of rare species inflates σ_A² artificially. Seasonal dynamics may require within-season analysis rather than across-season.

### Atmospheric trace-gas or aerosol monitoring

**Data shape:** Normalized source fractions from inverse modeling or tracer-tracer analysis.

**Sample-size guidance:** D = 5–10 sources, M = 12+ months. Rare sources (volcanic aerosol off-eruption) at boundaries.

**Expected performance:** Theoretical fit; practical validation pending.

**Caveats:** Temporal autocorrelation of atmospheric species is often weak (synoptic timescales); effective M after accounting for τ_int may be smaller than nominal.

## Tier 3 — Use with care

Domains where HUF can provide insight but where caveats dominate the design.

### Financial portfolio composition monitoring

**Data shape:** Asset-class or sector fractions in portfolios over time.

**Sample-size guidance:** D varies widely; T often inadequate (monthly rebalancing = M ≈ 12/year).

**Expected performance:** Mechanically valid but portfolios reallocate strategically; drift is endogenous rather than exogenous. HUF-GOV flags are diagnostic of the manager's decisions, not external shocks.

**Caveats:** Crisis-period heavy-tail distributions stress the finite-variance assumption (A2). Segment pre-/post-crisis.

### Manufacturing quality control (production-mix monitoring)

**Data shape:** Output composition of a production process (product variants, defect modes, material streams).

**Sample-size guidance:** Depends on production rate; typically short windows between product changeovers.

**Expected performance:** Valid for stable production runs. Flag false-positives expected at process changes unless changeovers are treated as segment boundaries.

## Domain-specific red flags

Read `science/eitt/EITT_SAFETY_BOUNDARIES.md` for the full catalog. Abbreviated red flags per domain:

**Clinical / biomedical** — NOT a validated use case at this time. Explicit misuse example in the safety document (15-patient, 3-time-point microbiome study). Requires adequate cohort size, appropriate handling of rare species, multiple-testing correction, and careful separation of treatment effects from stationarity.

**Financial** — heavy tails, regime shifts, endogenous drift. Segment carefully.

**Environmental** — seasonal transitions, rare-component boundaries, sensor drift.

**Physical / chemical** — near-phase-boundary δ → 0 behavior; use Aitchison-norm.

## Sample-size calculator (rough rule)

For target residual tightness ε (e.g., ε = 0.05 for 5% residual):

    M · δ · H̄ > (D−1) · σ_A² / ε

Where:
- D = number of carriers
- M = block size (compression ratio)
- δ = minimum observed proportion
- σ_A² = Aitchison variance of the clr-transformed series (trace of Σ)
- H̄ = mean Shannon entropy

If your dataset doesn't satisfy this inequality, the bound is too loose to be useful. You can tighten by: aggregating rare carriers (raise δ), extending the series (raise M), selecting a stationary segment (reduce effective σ_A²), or using a bounded-curvature entropy lens (Aitchison-norm, Rényi q=2).

## What you get wrong first (the common misuses)

In order of frequency of observed or predicted misuse:

1. **Treating "EITT invariant" as evidence of no effect.** It is evidence that the compositional structure stayed within a specific bound. The inverse does not hold.
2. **Reporting EITT residuals as clinical or managerial effect sizes.** They are not effect sizes. They are internal consistency checks with bounded certainty.
3. **Applying to short time series.** Fewer than 5 time points cannot support the second-order Taylor approximation.
4. **Smoothing through known regime changes.** If a policy change or treatment transition occurred in the window, segment around it; do not smooth across.
5. **Ignoring the boundary condition.** `min(x_i) < 0.01` triggers the 1/x_i Hessian explosion; use Aitchison-norm or amalgamate.

The sanity-check checklist in `EITT_SAFETY_BOUNDARIES.md §Sanity check` runs through all five before any consequential decision. Use it.
