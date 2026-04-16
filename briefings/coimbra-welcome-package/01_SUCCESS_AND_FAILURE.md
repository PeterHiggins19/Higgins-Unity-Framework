# 01 — Where HUF Succeeds, Where HUF Fails

A working tool has both. The honest listing is your best protection against misuse.

## Where HUF succeeds

### Empirically validated

**Four proofs, each on real data, each reproducible:**

**Proof 1 — European daily wholesale electricity prices.** Eight countries as price-share compositions, 4,089 daily observations, 341:1 compression (daily → annual via geometric mean). Shannon entropy variation: 0.18%. Aitchison variance drop: 55%. Total variation drop: 99.7%. This is the strongest single proof.

**Proof 2 — EMBER monthly generation mixes.** Nine fuel types across six countries (France, Germany, Japan, Poland, United Kingdom, United States), 12:1 compression (monthly → annual). Mean entropy variation: 1.02%. Every country-fuel combination stays below 2%.

**Proof 3 — NGFS Phase 4 climate scenarios.** 35 global pathways, 6 energy carriers, 2020–2100 horizon. Geometric 5-year mean: 1.8% entropy variation (max 4.7%). Arithmetic 5-year mean: 14.2% (max 28.6%). Geometric decimation is 8× tighter than arithmetic — the central validation of EITT's claim that the geometric-mean barycenter is the correct averaging operator for compositional data.

**Proof 4 — CheMixHub chemical mixtures.** Approximately 500,000 chemical mixture data points across 7 public datasets, multiple entropy lenses (Shannon, Jensen-corrected, Rényi q=2, Aitchison norm). Interior compositions pass at 54–82% depending on lens. Boundary compositions reveal simplex curvature effects — this is where EITT's limits become visible and where the safety boundary documentation originates.

### Theoretically supported

**Second-order Hessian bound.** `|E[δ_M]| ≤ (D-1) σ_A² / (2δM) + O(M^{-3/2})` under three stated assumptions: interior bound (x_i ≥ δ > 0), finite variance, sufficient mixing. Proof sketch and full empirical check against the four proofs in `science/eitt/EITT_HESSIAN_BOUND.md`.

**Shape/magnitude decomposition.** The general principle behind EITT: shape functionals (entropy, correlation structure, principal balances, affinity clusters) are invariant under geometric-mean decimation; magnitude functionals (Aitchison variance, total variation) scale as 1/M. Details and the Fisher-Rao resolution in `science/eitt/EITT_WHY_IT_WORKS.md §7`.

### Infrastructure

**Cold-start test passed by four AI systems.** Claude, ChatGPT, Grok, Gemini each read the repo cold and correctly answered ten technical questions. Fifth (Copilot) pending. This is the verifiability requirement operationalized: any AI or human stranger can become productive in minutes by reading `ai-refresh/HUF_FAST_REFRESH.json` once.

**Cross-domain consistency.** The same mathematics that flags drift in German electricity (d_A = 9.0712 at 2023–2024), Japan (d_A = 9.0477 at 2013–2014 absorbing the Fukushima shock), and the UK (three flags at 2004–2005, 2017–2018, 2019–2020) generalizes to Backblaze hard-drive reliability data (900,000+ drives, same pattern families under different physics).

## Where HUF fails

### Adversarial suite (documented failures)

Seventeen tests in `science/eitt/EITT_Adversarial_001.json`. Ten pass (real-world data). Seven fail (synthetic):

- Dirichlet random noise — no temporal autocorrelation, mixing assumption (A3) violated.
- Monotonic linear drift — non-stationary, stationarity assumption violated.
- Step-function regime shifts — non-stationary by construction.
- Oscillating extremes — pathological autocorrelation structure.
- Plus three additional synthetic adversaries with specific signatures.

**Boundary condition:** EITT holds for compositional time series with reasonable temporal autocorrelation. It does NOT hold for arbitrary simplex-valued sequences. Real-world borderline fail documented: Estonia oil-shale at 8.43% (single country, specific feedstock regime).

### Simplex boundary failures

When minimum proportion `δ` approaches zero, the Hessian of Shannon entropy (diagonal entries `1/x_i`) explodes. Documented failure: Jensen correction overcorrects by 476% at ionic-liquid boundaries (CheMixHub Proof 4, `claim_5_jensen_overcorrection` in `science/eitt/INDEX.json`).

**Boundary condition:** Do not apply EITT with Shannon entropy to compositions where `min(x_i) < 0.01` in any significant fraction of the data. Use Aitchison norm or Rényi q=2 collision entropy instead — their curvature is bounded independent of `δ`.

### Sample-size failures

The bound becomes vacuous when:

- **Short time series.** M < 5 points — second-order CLT approximation not justified.
- **Small cohorts.** For clinical/biomedical data, < 20 subjects — EITT lacks power regardless of nominal bound.
- **Many carriers, short series.** D > 10 with M < 100 — the `D²/M` scaling makes the bound too loose to be useful.

### Methodology failures (explicitly flagged)

- **HUF is not a two-sample test.** It is a within-series consistency check. Do not compare two populations via EITT residual magnitude.
- **"EITT invariant" does not mean "no effect occurred."** It means the compositional structure stayed within a specific bound under stated assumptions. The inverse does not hold.
- **EITT residuals are not clinical effect sizes.** Do not report them as such to non-compositional audiences.

### Speculative extensions safely stored (not promoted)

Work that did not clear the "Theorem. Assumptions. Proof. Check." bar lives in `dormant/grok-tensor-exploration-apr14/`:

- Higher-order Taylor tensors (orders 3–10) — pattern correct but asymptotic, not convergent
- "EITT-KPZ scaling exponent" — category error between deterministic CLT rate and universality-class exponent
- Quantum billiards with fabricated numerical example — the specific number (139,866,380.217) should not appear anywhere
- Many-body quantum extension — conflates Shannon with von Neumann entropy
- Multifractal conjecture — uncomputed

These are preserved for honest reference, not promoted as claims. See `dormant/grok-tensor-exploration-apr14/README.md` and `tensor_escalation.md` for the triage logic.

## The safety fence

`science/eitt/EITT_SAFETY_BOUNDARIES.md` is the living document that operationalizes the failure modes above into a usable safety manual. It covers:

- The three core assumptions (A1 interior, A2 finite variance, A3 mixing) and their characteristic failure signatures
- Sample-size requirements with rough rules
- Domain-specific red flags for clinical/biomedical, environmental, financial, and physical systems
- Canonical misuse example (15-patient, 3-time-point, 50-taxa breast cancer microbiome study — explicitly out of scope)
- Five-point sanity-check checklist before trusting any EITT result
- Responsible-use examples vs inappropriate-use examples

**Read the safety document before applying EITT to any consequential decision.** The failure modes are documented precisely so that no one has to rediscover them the hard way.

## Summary table

| Aspect | Status |
|---|---|
| Empirical validation | Four proofs on real data, reproducible |
| Theoretical foundation | Second-order Hessian bound proved under three assumptions |
| Shape/magnitude generalization | Conceptual synthesis complete, formal work ongoing |
| Cross-AI verifiability | Passed by 4/5 AI systems cold-start |
| Adversarial robustness | 10/17 pass, 7 documented failures with specific signatures |
| Boundary behavior | Failure mode documented; Aitchison-norm / Rényi q=2 rescue for boundary cases |
| Clinical/biomedical readiness | NOT READY — safety document explicit on why |
| Environmental/hydrological readiness | READY for stationary within-season analysis, not across regime transitions |
| Energy/climate scenario readiness | READY — this is the primary validated domain |
| Package release | In preparation (Phase 2 track 7) |
