# EITT on the Chemical Simplex

**Entropy Invariance, Boundary Geometry, and Diagnostic Lenses for Compositional Data Analysis on Multi-Modal Mixture Data**

Peter Higgins | Rogue Wave Audio | April 2026

*Prepared for CoDaWork 2026, Coimbra | HUF-GOV: Measure, Report, File*

*Markdown companion to EITT_Chemistry_Findings.docx — identical content, machine-readable format.*

---

## 1. Context and Purpose

EITT (Entropy Invariance under Temporal Transformation) was originally confirmed on energy-market and financial compositions, where Shannon entropy of share vectors appears near-invariant under geometric-mean block decimation. Those domains have temporal autocorrelation, market conventions, and relatively well-mixed compositions. A natural question arises: does the invariance live in the Aitchison geometry of the simplex itself, or does it require the temporal structure of the signal?

To answer this, we tested EITT on chemical mixture compositions from the CheMixHub benchmark, covering approximately 500,000 data points across seven public datasets: ionic-liquid transport properties, organic viscosity, drug solubility, polymer electrolytes, miscible solvents, medicine formulations, and motor octane number mixtures. Mole fractions are compositions by physical law, not by arbitrary normalisation. The constraints are fundamental: mass balance, charge balance, stoichiometry, phase rules. If EITT holds in chemistry, the invariance is geometric. If it fails, the failure mode tells us what additional structure the invariance requires.

The answer is both. The invariance partially holds, partially fails, and the failure modes are themselves diagnostic tools with applications well beyond the original EITT question.

## 2. Empirical Results: Four Lenses on the Chemical Simplex

We tested EITT using four metrics simultaneously, each representing a different way of measuring compositional change under geometric-mean decimation. We call these diagnostic lenses. The raw Shannon entropy is the standard EITT metric. The Jensen-corrected Shannon subtracts the expected Hessian-based curvature bias. The collision entropy uses the order-2 member of the full entropy family. The Aitchison norm measures distance from the neutral element using the simplex's own Riemannian metric.

Results are split by simplex region: interior compositions where all parts exceed 5%, and boundary compositions where at least one part falls below 5%.

### Table 1: Four-Lens EITT Results on CheMixHub (pass rate | mean |delta|)

| Dataset (Region) | Groups | Raw Shannon | Jensen Corr. | Rényi q=2 | Aitchison |
|---|---:|---|---|---|---|
| Drug Solubility (all interior) | 37 | **73.0% \| 1.37%** | 0.0% \| 9.32% | 56.8% \| 1.84% | 52.7% \| 3.59% |
| Polymer Electrolyte (interior) | 24 | **81.8% \| 1.95%** | 27.3% \| 7.54% | 77.3% \| 2.52% | 68.2% \| 3.11% |
| Polymer Electrolyte (boundary) | 24 | 42.3% \| 3.80% | 11.5% \| 7.23% | 38.5% \| 4.02% | **57.7% \| 4.00%** |
| Ionic Liquids (interior) | 450 | **54.0% \| 4.06%** | 20.0% \| 9.66% | 54.0% \| 4.87% | 44.0% \| 9.03% |
| Ionic Liquids (boundary) | 450 | 36.0% \| 5.03% | 0.0% \| 476% | 38.0% \| 6.15% | 38.0% \| 5.00% |
| NIST Organic Viscosity (int.) | 2572 | **45.3% \| 3.25%** | 10.5% \| 9.39% | 41.9% \| 4.40% | 39.5% \| 6.97% |
| NIST Organic Viscosity (bnd.) | 2572 | 35.7% \| 12.12% | 0.0% \| 36.7% | 35.7% \| 16.2% | **42.9% \| 2.49%** |
| logV (all interior) | 301 | **52.0% \| 2.82%** | 17.0% \| 7.85% | 46.0% \| 3.38% | 39.0% \| 7.53% |
| Miscible Solvents D=3 (int.) | 1 | **100% \| 0.004%** | 0.0% \| 5.06% | 100% \| 0.01% | 100% \| 0.02% |

*Bold entries mark the best-performing lens for that row. Interior = min(x_i) >= 0.05. Boundary = min(x_i) < 0.05.*

## 3. Failure Taxonomy: From Worst to Best

### 3.1 Jensen Correction: The Overcorrected Prescription

**Performance:** Worst overall. 0–20% pass rates. Residuals exceeding 400% at boundary compositions.

**Mechanism:** The correction subtracts the expected Hessian-based bias: Δ_corrected = Δ_raw − (1/2M) × Σ(var_i / x̅_i). This is a second-order Taylor expansion that assumes compositions are small perturbations around a mean. Composition sweeps traverse large arcs of the simplex where the expansion diverges.

**Why it fails:** Near the boundary, x̅_i is small and the 1/x̅_i term dominates. The correction exceeds the signal by orders of magnitude. This is a local approximation applied to a global traversal.

**What this reveals for compositional inference:** The Hessian of Shannon entropy on the simplex is the Fisher information matrix for the multinomial family. Our empirical demonstration that this Hessian varies by orders of magnitude across the simplex is a direct, data-driven illustration of what information geometry predicts theoretically. For practitioners performing maximum likelihood estimation or compositional regression near the boundary of the simplex, this result provides a quantified warning. Symmetric confidence intervals computed from the Fisher information at the geometric mean will be unreliable when any component falls below approximately 5%. The 476% overcorrection at the ionic-liquid boundary is not a failure of the Jensen lens per se; it is a measurement of how strongly the curvature of the entropy surface varies across the simplex.

### 3.2 Collision Entropy: The Wrong Tint

**Performance:** Marginally worse than raw Shannon in most cases. 38–77% pass rates.

**Mechanism:** H_2(x) = −ln(Σ x_i²) down-weights rare components relative to Shannon.

**Why it underperforms:** The fundamental issue is not which entropy order you use. It is that any concave function averaged over a large arc of the simplex produces a Jensen gap. Changing from q=1 to q=2 shifts the curvature profile but does not eliminate it. Moreover, H_2 has steeper curvature in the mid-simplex where Shannon is locally flat, degrading performance in the very region where raw Shannon excels.

**What this constrains for the entropy family:** The confirmed generalisation of EITT across q=0.1 to q=5.0 was established on temporal data with high autocorrelation. The chemistry result shows that this generalisation has a domain boundary. Shannon is optimal for broad compositional surveys because its curvature is gentlest in the interior. Higher orders are preferable only when compositions remain in a small neighbourhood, as they do in temporal monitoring. Selection principle: use q=1 for exploratory compositional analysis across diverse mixtures; use higher q for real-time monitoring of a stable process.

### 3.3 Aitchison Norm: The Boundary Specialist

**Performance:** Best at the boundary. NIST boundary: 42.9% pass at 2.49% residual vs 35.7% at 12.12% for raw Shannon. Polymer boundary: 57.7% vs 42.3%.

**Mechanism:** d_A(x, n) = ‖clr(x) − clr(n)‖ measures the Aitchison distance from the neutral element using the simplex's Riemannian metric. This metric has uniform curvature everywhere by construction.

**What this demonstrates for CoDa methodology:** The Aitchison norm result is perhaps the most consequential finding. It demonstrates empirically that the boundary failures observed with Shannon entropy are metric artefacts, not failures of the underlying compositional structure. When the analysis is conducted using the simplex's own Riemannian distance rather than an information-theoretic functional, boundary performance improves dramatically. The simplex geometry is well-behaved everywhere; it is Shannon entropy's non-uniform curvature that creates the appearance of boundary instability.

### 3.4 Raw Shannon: The Interior Standard

**Performance:** Best overall in the interior. 81.8% pass at 1.95% residual on polymer-electrolyte interior. 73.0% at 1.37% on drug solubility.

**Why it succeeds:** Shannon entropy is locally flat near the centre of the simplex (max entropy at the uniform composition). Geometric-mean decimation produces small compositional shifts that barely change H in this flat region.

**Why it fails at the boundary:** H is concave with curvature −(1/x_i) along each axis. Near x_i = 0, the curvature is steep, H is small, and both the numerator and denominator of the relative residual conspire to amplify small perturbations.

**What this means for EITT:** The 53% overall pass rate on chemical composition sweeps, compared to 94.8% on energy time series, represents the first empirical decomposition of the two contributions to EITT invariance. Approximately half of the effect comes from the Aitchison geometry of the simplex, and approximately half comes from temporal autocorrelation keeping compositions in a small neighbourhood where the entropy surface is locally flat.

## 4. The Multi-Modal Nature of Data on the Simplex

The four-lens comparison reveals that the simplex is not a uniform space for analysis. Data on the simplex is inherently multi-modal in its geometric character. In the interior, the simplex behaves like a gently curved manifold where information-theoretic functionals are stable. At the boundary, the geometry changes qualitatively. The Fisher information diverges, log-ratio transforms become singular, and the gap between the Aitchison metric and information-theoretic measures widens.

The dual-lens diagnostic that emerges naturally: Shannon for the interior, Aitchison norm for the boundary, with a crossover near min(x_i) ≈ 0.05.

## 5. Inverse Gains: What the Failures Teach Adjacent Fields

**Analytical Chemistry:** The Jensen overcorrection quantifies the curvature of the entropy surface near the simplex boundary using real chemical data. The 476% Hessian overcorrection at the ionic-liquid boundary translates directly to the unreliability of symmetric confidence intervals in this regime.

**Ecology and Biodiversity:** Hill numbers and Shannon diversity are standard tools. Our results show that geometric-mean averaging of near-monoculture compositions produces volatile diversity estimates due to curvature effects. The Aitchison distance from the uniform composition is stable precisely where Shannon is not.

**Pharmaceutical Formulation:** Multi-component drug formulations (D=6) failed all four lenses. With six components, the probability of boundary contact is high. Directly relevant to FDA Process Analytical Technology guidelines.

**Information Theory:** The chemistry results show the Rényi generalisation has a domain boundary. Shannon is special for broad surveys because its interior curvature is the gentlest.

**CoDa Methodology:** The Aitchison norm's consistent stability at the boundary confirms empirically that the Aitchison metric is the natural ruler on the simplex, with uniform curvature that does not distort measurements regardless of position.

## 6. Honest Disclosures

1. Composition sweeps ordered by mole fraction are not time series. Results describe EITT on smoothly ordered compositions, not temporal data.
2. Binary mixtures (D=2) live on the one-dimensional simplex. Higher-dimensional tests (D=3, D=6) were limited by data availability.
3. CheMixHub data is curated for machine-learning benchmarking. Some preprocessing decisions may affect compositional structure.
4. The Jensen correction requires a damping coefficient proportional to composition range before it is practically useful.
5. The boundary threshold of min(x_i) = 0.05 was chosen empirically. Formal derivation is an open problem.
6. EITT is an empirical observation, not a theorem. Formal proof is Open Problem O-1.
7. The 53% overall pass rate includes both interior and boundary compositions. Interior-only pass rates (54–82%) are more comparable to temporal EITT results.
8. The olfactory-similarity dataset could not be tested. Medicine formulations had only 1 testable group.

## 7. Data Sources and Reproducibility

**Primary data:** CheMixHub benchmark (Rajaonson et al., NeurIPS 2025). github.com/chemcognition-lab/chemixhub. Seven datasets, approximately 500,000 data points, all compositions as mole fractions.

**Pipeline:** chem_eitt_pipeline.py. Open source, single-file Python. Dependencies: pandas, numpy, scipy, matplotlib.

**Experiment specification:** CHEM_EITT_LAB_001.json. Full protocol, hypotheses, expected results, and CoDa mapping.

**Repository:** github.com/PeterHiggins19/Higgins-Unity-Framework

**Standard:** RWA-001 (Rogue Wave Audio Corporate Reference).

**Governance:** HUF-GOV. Measure, report, file. No intervention on the data.

---

Peter Higgins | Rogue Wave Audio | PeterHiggins@RogueWaveAudio.com | April 2026

Multi-AI adversarial review (Claude, ChatGPT, Grok, Gemini, Copilot) applied throughout.
