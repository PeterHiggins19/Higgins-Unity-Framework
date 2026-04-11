# Chemistry as a Compositional Data Laboratory for EITT Testing

**Peter Higgins | Rogue Wave Audio | PeterHiggins@RogueWaveAudio.com**
**April 2026 | HUF-GOV: Measure, Report, File**

---

## 1. Why Chemistry

EITT (Entropy Invariance under Temporal Transformation) has been confirmed in energy markets (gold/silver, fossil fuels, German renewables) and financial data (9-asset price-level compositions). Every one of these domains has compositions — parts of a whole that sum to one — evolving through time. But the constraints in financial and energy markets are *conventions*: market caps, portfolio weights, energy-mix shares.

Chemistry gives us something harder: **constraints that are laws of nature**. Mass is conserved. Charge is conserved. Atoms in a reaction obey stoichiometry. Phase equilibria are dictated by thermodynamics, not human behaviour. If EITT holds in chemistry, the near-invariance of Shannon entropy under geometric-mean decimation is not a quirk of autocorrelated time series in social systems. It lives in the Aitchison geometry of the simplex itself.

If EITT fails in chemistry, that failure tells us exactly what the invariance *needs*: temporal persistence, smooth evolution, absence of phase discontinuities. Either outcome is valuable.

---

## 2. How Chemistry Maps to CoDa

| Chemistry concept | CoDa concept | Who defined it |
|---|---|---|
| Mole fractions of a mixture | Composition on the simplex S^D | Aitchison (1986) |
| Mass balance (sum = 1) | Closure C(z) = z / sum(z) | Aitchison (1986) |
| Changing mixture ratios | Perturbation x (+) p | Aitchison (1986) |
| Geometric mean of compositions | Fréchet mean on the simplex | Egozcue, Pawlowsky-Glahn (2001) |
| CLR/ILR transforms of mole fractions | Standard CoDa transforms | Aitchison (1986); Egozcue et al. (2003) |
| Aitchison distance between mixtures | d_A(x,y) = ‖clr(x) - clr(y)‖ | Aitchison (1986) |
| Shannon entropy of mixture | H(x) = -sum(x_i ln x_i) | Shannon (1948) |
| Effective number of species | K_eff = exp(H(x)) = Hill number q=1 | Hill (1973); HUF naming |
| Temperature sweep along mixtures | Pseudo-time axis for decimation | HUF new application |
| Phase boundary / miscibility gap | Non-stationarity boundary | HUF diagnostic |

The mapping is natural because **mole fractions are already compositions**. They live on the simplex by physical law, not by arbitrary normalisation. Every CoDa operation (perturbation, CLR, ILR, Aitchison distance) applies directly. No reframing needed.

---

## 3. Data Sources — Scouted and Ranked

### Rank 1: CheMixHub (EXCELLENT)

**Repository:** github.com/chemcognition-lab/chemixhub

CheMixHub is a benchmark for chemical mixture property prediction, containing approximately 500,000 data points from 7 public datasets, with all compositions standardised to mole fractions. This is exactly what we need.

**Key datasets for EITT:**

**ILThermo Viscosity** — 75,992 data points. Binary ionic-liquid mixtures from 699 distinct molecules. Temperature sweeps at fixed composition, or composition sweeps at fixed T. Hard constraints: mole fractions sum to 1, Arrhenius-type temperature dependence. This is the primary experiment target.

**ILThermo Transport (large-scale)** — 116,896 data points. The largest single mixture dataset publicly available. Binary and ternary ionic liquid mixtures with transport properties measured across temperature.

**Miscible Solvents** — ~19,000 data points. Binary and ternary solvent mixtures with density and enthalpy of mixing. Generated from molecular dynamics. Good for composition-sweep decimation (treating mole-fraction ratio as the "time" axis).

**Drug Solubility** — Solubility of drugs in mixed solvents. Composition sweep with a hard phase boundary (solubility limit). Natural negative control: EITT should break at the precipitation boundary.

**Solid Polymer Electrolyte** — Polymer-salt compositions with ionic conductivity. Percolation threshold provides another phase-like boundary for testing EITT failure modes.

**NIST Organic Viscosity** — Binary organic mixtures with viscosity measurements at multiple temperatures and compositions.

**Data format:** CSV (processed_data.csv per dataset), mole fractions pre-computed, ready for CoDa analysis.

### Rank 2: ChemKED-database (MODERATE)

**Repository:** github.com/pr-omethe-us/ChemKED-database

YAML-format database of combustion kinetics experiments. Fuel/oxidizer/diluent mixtures specified as mole fractions, with ignition delay times at various temperatures and pressures.

**Why interesting:** Stoichiometric constraints are the hardest chemical constraint. Atoms are strictly conserved in every reaction. If EITT holds on stoichiometrically constrained compositions, the geometry argument is very strong.

**Limitations:** Data is per-experiment, not time series. Need to construct pseudo-time axes from T or P sweeps. Lower data volume than CheMixHub. YAML parsing required (PyKED package available).

### Rank 3: InterMat / NIST (POOR — reject for EITT)

**Repository:** github.com/usnistgov/intermat

DFT interface calculations for material heterostructures. Crystal structures and lattice parameters, not mixture compositions. Would require heavy reframing to map to CoDa. Not recommended for EITT testing.

**Retain as reference:** If someone converts site-occupancy data (fractional occupancy of crystal sites by different elements) to compositions, this becomes interesting — but that's a different project.

---

## 4. Constraint Taxonomy — What Makes Chemistry Special

Chemistry provides five types of hard constraint that energy/financial systems don't have:

**Mass balance:** Total mass is conserved. Every atom that enters a system must be accounted for. In CoDa terms: the composition is *physically* closed, not just mathematically normalised.

**Charge balance:** For ionic systems (the entire ILThermo dataset), net charge must be zero. This is an additional linear constraint on the simplex, restricting the feasible region.

**Stoichiometry:** In reaction networks, the number of each type of atom is conserved. This defines a stoichiometric compatibility class — a subspace of the simplex. Compositions can only evolve *within* this subspace.

**Phase rules:** Gibbs' phase rule (F = C - P + 2) limits the degrees of freedom. At a phase boundary, the system jumps from one composition to another. This is the chemistry analogue of non-stationarity.

**Solubility/miscibility limits:** Hard boundaries in composition space where the system physically cannot exist as a single phase. Cross this boundary and the composition splits into two phases — a discontinuity that should break EITT.

---

## 5. Prioritised Experiment Plan

### Experiment 1 (Primary): ILThermo Viscosity T-Sweep

**What:** For each unique binary ionic-liquid mixture in CheMixHub's ILThermo viscosity dataset, sort by temperature, treat T as pseudo-time, apply geometric-mean decimation at M = 2, 3, 5.

**Why first:** Largest dataset, cleanest compositions, temperature provides a smooth ordering axis with high autocorrelation.

**Expected:** EITT should PASS for most mixtures along smooth T-sweeps. Failures should cluster near phase transitions or data quality issues.

**Metrics:** delta_M (EITT residual), bootstrap 95% CI, Aitchison variance ratio, K_eff.

### Experiment 2: Miscible Solvents Composition Sweep

**What:** For binary/ternary solvent mixtures, order by mole fraction of one component (0 to 1). Treat this as "time." Decimate.

**Why:** Tests whether EITT holds on a *composition axis* rather than a *time axis*. If it does, the invariance is about simplex geometry, not temporal autocorrelation.

**Expected:** Should work for smooth mixing curves. May fail near ideal/non-ideal mixing transitions.

### Experiment 3: Drug Solubility — Phase Boundary Test

**What:** Composition sweep for drug-in-mixed-solvent systems. Look for the solubility limit.

**Why:** Natural negative control. The solubility boundary is a phase transition — EITT should break here.

**Expected:** PASS before the boundary, FAIL across it. If K_eff detects the transition before delta_M blows up, that's a diagnostic win (deceptive drift analogue).

### Experiment 4: Polymer Electrolyte — Percolation Threshold

**What:** Salt concentration sweep in polymer electrolytes. Ionic conductivity changes dramatically at the percolation threshold.

**Why:** Tests EITT at a different type of phase transition — not liquid-solid, but connected-disconnected ion transport network.

**Expected:** EITT should fail at the percolation threshold. Interesting if K_eff tracks the transition.

### Experiment 5: ChemKED — Stoichiometric Combustion

**What:** Fuel/oxidizer/diluent mole fractions from combustion experiments. Group by fuel type, sweep T or P.

**Why:** Hardest constraint test. Stoichiometry is exact atom conservation.

**Expected:** If EITT holds here, the simplex geometry argument is very strong. If it fails, stoichiometric constraints may restrict the simplex in ways that break the averaging assumption.

---

## 6. What We Learn Either Way

**If EITT holds in chemistry:** The near-invariance of Shannon entropy under geometric-mean decimation is a fundamental property of the Aitchison geometry on the simplex, observable in any domain with smooth compositional evolution. It's not a quirk of market autocorrelation. This is the strongest possible validation — chemistry constraints are laws of nature.

**If EITT fails in chemistry:** The invariance requires specific temporal structure (persistence, smoothness) that chemical systems may not always have. The failure modes map to the energy-domain findings: phase transitions are like solar/nuclear breaks, discontinuous reactions are like regime changes. The failure taxonomy becomes richer and more precisely characterised.

**Either way:** We learn where the boundaries of EITT are. And chemistry gives us the most controlled environment possible to study those boundaries, because the constraints are known exactly, not estimated from data.

---

## 7. Practical Next Steps

1. **Clone CheMixHub** and inspect the actual CSV column structure for ILThermo viscosity.
2. **Run chem_eitt_pipeline.py** on the ILThermo data. Report results.
3. **If compositions need reformatting** (e.g., SMILES + mole_fraction rather than explicit component columns), update the pipeline's extract_compositions function.
4. **Run experiments 2-5** in order of priority.
5. **Document all results** in CHEM_EITT_LAB_001_RESULTS.json — same format as EITT_LAB_PACKAGE.
6. **Write up findings** for CoDaWork 2026 submission or supplementary material.
7. **If failures found:** characterise the failure mode precisely. What constraint geometry breaks EITT? This is the interesting science.

---

## 8. Honest Disclosures

1. Temperature sweep is a pseudo-time axis. Results must be interpreted as "EITT on smoothly ordered compositions" not "EITT on temporal data."
2. Binary mixtures (D=2) live on S^1, which is trivially one-dimensional. Ternary and higher are more interesting for CoDa.
3. CheMixHub data is curated for ML benchmarking. Some preprocessing choices may affect compositional structure.
4. We have not yet run on real chemistry data. This document is a research plan, not a results report.
5. The synthetic pipeline validates that the code works. Real-data results may differ substantially.

---

## Sources

- [CheMixHub repository](https://github.com/chemcognition-lab/chemixhub) — Rajaonson et al., NeurIPS 2025
- [CheMixHub project page](https://chemcognition-lab.github.io/chemixhub/)
- [ChemKED-database](https://github.com/pr-omethe-us/ChemKED-database) — Weber & Niemeyer, SciPy 2016
- [InterMat / NIST](https://github.com/usnistgov/intermat) — NIST interface materials
- [ILThermo database](https://ilthermo.boulder.nist.gov/) — NIST Standard Reference Database 147

---

*Governance: HUF-GOV | Standard: RWA-001 | Repository: github.com/PeterHiggins19/Higgins-Unity-Framework*
