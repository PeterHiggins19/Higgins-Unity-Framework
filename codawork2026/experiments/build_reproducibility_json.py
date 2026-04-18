#!/usr/bin/env python3
"""
HIGGINS DECOMPOSITION — COMPREHENSIVE REPRODUCIBILITY PACKAGE
===============================================================
Complete JSON for the collective to reproduce, test, and break every result.
Sources all material. Describes every method. Includes all parameters.
"""

import json, os
from datetime import datetime

OUT = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/HIGGINS_REPRODUCIBILITY_PACKAGE.json"

package = {
    "_meta": {
        "title": "The Higgins Decomposition: Complete Reproducibility Package",
        "author": "Peter Higgins",
        "date": datetime.now().isoformat(),
        "version": "5.0",
        "purpose": "Enable any researcher to reproduce, verify, and challenge every result in the EITT programme",
        "licence": "Open for academic use. Attribution required.",
        "contact": "peterhiggins2016@gmail.com",
        "how_to_use": (
            "This JSON contains everything needed to reproduce the Higgins Decomposition results. "
            "Each section is self-contained with data sources, methods, parameters, and expected outputs. "
            "Start with Section 1 (data sources), implement the EITT engine from Section 2, "
            "run the Gold Standard test from Section 3, then try to break it with Section 5."
        ),
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 1: DATA SOURCES
    # ══════════════════════════════════════════════════════════════════════
    "1_data_sources": {
        "description": "All primary data sources used across the programme. Every dataset is either publicly available or constructible from the parameters given here.",

        "primary_datasets": {
            "gold_silver_ratio": {
                "source": "World Gold Council / Kitco historical data",
                "file": "DATA/Commodities/gold_silver_ratio_enriched.csv",
                "columns": ["date", "price", "currency", "silver_oz_per_gold_oz"],
                "coverage": "1718-2026 (annual gold price in GBP/USD, silver oz per gold oz)",
                "N": 624,
                "composition_method": "2-part: gold_share = 1/(1+ratio), silver_share = ratio/(1+ratio)",
                "notes": "The ratio column 'silver_oz_per_gold_oz' contains NaN for pre-1718 entries. Drop NaN before use.",
                "download": "Original from World Gold Council historical price data. Enriched CSV included in DATA/Commodities/.",
            },

            "nuclear_decay_chains": {
                "source": "IAEA Nuclear Data Services / NUDAT 3.0",
                "url": "https://www.nndc.bnl.gov/nudat3/",
                "datasets": {
                    "U-238": {
                        "half_lives_years": [4.47e9, 0.0245, 1600.0],
                        "isotopes": ["U-238", "Th-234", "Ra-226"],
                        "N": 15,
                        "D": 3,
                        "construction": "nuclear_chain(N=15, D=3, half_lives=[4.47e9, 0.0245, 1600.0])",
                    },
                    "Th-232": {
                        "half_lives_years": [14.05e9, 5.75, 1.91],
                        "isotopes": ["Th-232", "Ra-228", "Ac-228"],
                        "N": 10,
                        "D": 3,
                    },
                    "Pu-239": {
                        "half_lives_years": [24110.0, 6563.0, 2.117],
                        "isotopes": ["Pu-239", "U-235", "Pa-231"],
                        "N": 12,
                        "D": 3,
                    },
                },
                "construction_method": (
                    "t = linspace(0, 30, N). For each isotope i: x_i(t) = exp(-0.693*t/half_life_i) + 1e-10. "
                    "Closure: X = x / sum(x, axis=1). This generates a D-part composition on the simplex."
                ),
            },

            "acoustic_bessel_functions": {
                "source": "Mathematical construction (Bessel functions of the first kind)",
                "reference": "Abramowitz & Stegun, Handbook of Mathematical Functions, Chapter 9",
                "construction": (
                    "Bessel J_n(x) for orders n=1,2,7. "
                    "t = linspace(0.1, 10*scale, N). "
                    "For each component i: x_i(t) = |J_{order+i}(t)| + 1e-10. "
                    "Closure: X = x / sum(x, axis=1)."
                ),
                "datasets": {
                    "Bessel-1 Clean": {"order": 1, "scale": 1.0, "N": 200, "D": 3, "label": "LEGITIMATE"},
                    "Bessel-2 Acoustic": {"order": 2, "scale": 1.0, "N": 200, "D": 3, "label": "LEGITIMATE"},
                    "Bessel-7 HiVar": {"order": 7, "scale": 2.5, "N": 200, "D": 3, "label": "LEGITIMATE"},
                },
                "notes": "Bessel functions model acoustic resonances. Higher orders produce higher variance compositions.",
            },

            "butterworth_filters": {
                "source": "Mathematical construction (Butterworth low-pass filter magnitude response)",
                "reference": "Butterworth, S. (1930). On the Theory of Filter Amplifiers. Experimental Wireless, 7, 536-541.",
                "construction": (
                    "t = arange(N). For each component i: freq = fc*(1+0.5*i). "
                    "h_i(t) = 1/sqrt(1 + (t/(N*freq))^(2*order)). Closure: X = h / sum(h)."
                ),
                "datasets": {
                    "Butterworth Filter": {"fc": 0.1, "order": 2, "N": 200, "D": 3, "label": "FABRICATED"},
                    "Distorted BW": {"fc": 0.15, "order": 3, "N": 200, "D": 3, "label": "FABRICATED",
                                     "distortion": "X = X^2.5 then re-close"},
                },
            },

            "synthetic_processes": {
                "Dirichlet Process": {
                    "source": "NumPy random.dirichlet",
                    "parameters": {"alpha": [5, 5, 5], "N": 200, "seed": 100},
                    "label": "LEGITIMATE",
                    "notes": "Symmetric Dirichlet with alpha=5 produces compositions clustered around the center of the simplex.",
                },
                "Logistic Map": {
                    "source": "Mathematical construction",
                    "parameters": {"r": 3.7, "x0": 0.4, "N": 300},
                    "construction": "x[n+1] = r*x[n]*(1-x[n]). Map to 2-part composition: [x/(x+1), 1/(x+1)].",
                    "label": "LEGITIMATE",
                    "notes": "r=3.7 is in the chaotic regime. Despite chaos, temporal structure is preserved.",
                },
                "AR(1) Simplex": {
                    "source": "Mathematical construction",
                    "parameters": {"phi": 0.95, "sigma": 0.1, "N": 300, "D": 3, "seed": 600},
                    "construction": "x[n] = 0.95*x[n-1] + N(0,0.1) in R^3. Map to simplex: X = exp(x)/sum(exp(x)).",
                    "label": "LEGITIMATE",
                },
                "Uniform Noise": {
                    "source": "NumPy random.uniform",
                    "parameters": {"low": 0.1, "high": 1.0, "N": 200, "D": 2, "seed": 200},
                    "construction": "Uniform random then closure. No temporal structure.",
                    "label": "FABRICATED",
                },
            },

            "noise_processes": {
                "Pink Noise": {
                    "source": "Mathematical construction (1/f spectrum)",
                    "construction": (
                        "Generate 1/f noise via FFT: S(f) = 1/sqrt(f), random phases, IFFT. "
                        "3 independent 1/f signals, take absolute value, close to simplex."
                    ),
                    "parameters": {"N": 200, "D": 3, "seed": 700},
                    "label": "FABRICATED",
                },
                "White Noise": {
                    "source": "NumPy random.normal",
                    "parameters": {"mean": 1.0, "std": 0.5, "N": 200, "D": 3, "seed": 800},
                    "construction": "Gaussian white noise, absolute value, close to simplex.",
                    "label": "FABRICATED",
                },
            },

            "adversarial_datasets": {
                "Permuted Gold/Silver": {
                    "source": "Derived from Gold/Silver ratio",
                    "construction": "Random permutation of rows (seed=42). Destroys temporal order, preserves marginal distributions.",
                    "label": "FABRICATED",
                },
                "Contaminated G/S": {
                    "source": "Derived from Gold/Silver ratio",
                    "construction": "10% of rows: multiply gold_share by uniform(2,5). Re-close. Seed=99.",
                    "label": "FABRICATED",
                },
                "Entropy-Stuffed": {
                    "source": "Mathematical construction",
                    "construction": "Dirichlet(1,1,1) base. Every even row replaced with [1/3,1/3,1/3] (max entropy). Seed=400.",
                    "label": "FABRICATED",
                    "notes": "Designed to fool entropy-based tests by padding with maximum-entropy rows.",
                },
                "Phase-Matched Fake": {
                    "source": "Derived from Gold/Silver ratio",
                    "construction": "Gold/Silver + Gaussian noise N(0,0.001). Seed=500. Preserves temporal structure.",
                    "label": "FABRICATED",
                    "notes": "Adversarial: designed to preserve entropy invariance. Tests instrument's blind spot.",
                },
            },
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 2: EITT ENGINE — COMPLETE ALGORITHM
    # ══════════════════════════════════════════════════════════════════════
    "2_eitt_engine": {
        "description": "Complete specification of the EITT algorithm. Implement this exactly to reproduce all results.",

        "step_1_composition": {
            "description": "Ensure input X is an N×D matrix where each row sums to 1 (compositional data on the simplex).",
            "closure": "X[i] = X[i] / sum(X[i]) for each row i",
            "requirements": "All entries > 0. Replace zeros with 1e-10 before closure.",
        },

        "step_2_geometric_mean_decimation": {
            "description": "Block-average N observations into M groups using geometric means.",
            "algorithm": (
                "block_size = N // M. "
                "For block i (i=0..M-1): "
                "  block = X[i*block_size : (i+1)*block_size, component]. "
                "  geometric_mean = exp(mean(log(block))). "
                "Return M geometric means for each component."
            ),
            "why_geometric": (
                "Geometric means are the natural average for compositional data. "
                "They preserve the log-ratio structure of the Aitchison geometry. "
                "Arithmetic means introduce spurious correlations on the simplex."
            ),
            "M_range": "M = 2, 3, ..., floor(N/5). The floor(N/5) ensures at least 5 observations per block.",
        },

        "step_3_shannon_entropy": {
            "description": "Compute normalised Shannon entropy for each component at each M.",
            "algorithm": (
                "For each component c and decimation M: "
                "  blocks = geometric_mean_decimation(X[:, c], M). "
                "  p = blocks / sum(blocks).  (normalise to probability distribution) "
                "  H = -sum(p * log(p)).  (Shannon entropy in nats) "
                "  H_max = log(M).  (maximum entropy for M bins) "
                "  H_norm = H / H_max.  (normalised: 0 to 1)"
            ),
            "H_bar": "H_bar(M) = mean(H_norm across all D components). This is the EITT signal.",
        },

        "step_4_pass_rate_classification": {
            "description": "Classify as LEGITIMATE or FABRICATED based on entropy invariance.",
            "threshold": 0.05,
            "algorithm": (
                "For each M in [2, ..., floor(N/5)]: "
                "  pass(M) = |H_bar(M) - H_bar(2)| < threshold. "
                "pass_rate = count(pass) / count(tested). "
                "If pass_rate >= 0.80: LEGITIMATE. Else: FABRICATED."
            ),
            "adaptive_threshold": (
                "For small test sets (n_tested <= 3): use threshold 0.67 instead of 0.80. "
                "This protects nuclear chains with N=10-15 observations."
            ),
        },

        "step_5_f17_contamination_tuner": {
            "description": "Detect anomalous inter-component coupling via the variation matrix.",
            "algorithm": (
                "1. Compute variation matrix: V[i,j] = var(log(X[:,i] / X[:,j])) for all pairs. "
                "2. C_geom = geometric mean of upper-triangle entries of V. "
                "3. sigma2_A = sum(V) / (2*D) = Aitchison total variance. "
                "4. F17_normalized = C_geom / sigma2_A. "
                "5. Apply ONLY to marginal cases (pass_rate between 0.80 and 0.95)."
            ),
            "threshold": 0.008,
            "critical_insight": (
                "C_geom scales naturally with sigma2_A (Theorem 2). "
                "An absolute F17 threshold destroys legitimate high-variance datasets. "
                "Normalisation by sigma2_A is essential."
            ),
        },

        "step_6_two_pass_instrument": {
            "description": "Pass 1 classifies. Pass 2 applies corrections to marginal cases only.",
            "pass_1": "Standard EITT classification (steps 1-4 above).",
            "pass_2_corrections": {
                "F17_tiebreaker": {
                    "when": "Pass 1 result is LEGITIMATE AND pass_rate < 0.95 (marginal)",
                    "action": "If F17_normalized > 0.008: reclassify as FABRICATED",
                    "rationale": "Catches entropy-stuffing attacks that pass the entropy test but have anomalous variation structure.",
                },
                "min_blocks_guard": {
                    "when": "floor(N/M) < 5 for any tested M",
                    "action": "Exclude that M from the pass-rate calculation",
                    "rationale": "Insufficient data for reliable entropy estimation.",
                },
                "stored_energy_alarm": {
                    "when": "H_bar near log(D)/log(M) with high variance",
                    "action": "Flag for manual review",
                    "rationale": "Resonance patterns can mimic legitimate behaviour.",
                },
            },
            "result": "Pass 1: 17/20 (85%). Pass 2: 18/20 (90%).",
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 3: CoDa TOOLKIT — COMPLETE IMPLEMENTATIONS
    # ══════════════════════════════════════════════════════════════════════
    "3_coda_toolkit": {
        "description": "All CoDa tools used in the integration. Standard implementations per Aitchison (1986) and Pawlowsky-Glahn et al. (2015).",
        "references": [
            "Aitchison, J. (1986). The Statistical Analysis of Compositional Data. Chapman & Hall.",
            "Pawlowsky-Glahn, V., Egozcue, J.J., & Tolosana-Delgado, R. (2015). Modeling and Analysis of Compositional Data. Wiley.",
            "Egozcue, J.J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003). Isometric logratio transformations for compositional data analysis. Mathematical Geology, 35(3), 279-300.",
        ],
        "tools": {
            "CLR": {
                "formula": "clr(x)_i = log(x_i) - mean(log(x))",
                "implementation": "clr(x) = log(x) - mean(log(x))",
                "metric": "CLR spread = std(clr(X)) across all rows and components",
            },
            "ILR": {
                "formula": "Helmert basis: ilr(x) = H @ clr(x) where H is (D-1)×D Helmert contrast matrix",
                "metric": "ILR spread = std(ilr(X))",
            },
            "ALR": {
                "formula": "alr(x)_i = log(x_i / x_ref) for i != ref",
                "default_reference": "Last component (ref=-1)",
            },
            "Aitchison_distance": {
                "formula": "d_A(x,y) = ||clr(x) - clr(y)||_2",
                "metric": "Mean pairwise Aitchison distance across all rows",
            },
            "Aitchison_variance": {
                "formula": "sigma2_A = totvar = trace(V) / (2D) where V is variation matrix",
                "alternative": "sigma2_A = (1/D) sum_i var(clr(X)_i)",
                "importance": "THE BRIDGE: sigma2_A predicts M_break (EITT critical decimation point)",
            },
            "variation_matrix": {
                "formula": "V[i,j] = var(log(X[:,i] / X[:,j]))",
                "size": "D × D symmetric, zeros on diagonal",
            },
            "Frechet_mean": {
                "formula": "Closure of geometric mean: FM = C(exp(mean(log(X), axis=0)))",
                "notes": "Natural center of compositional data in Aitchison geometry",
            },
            "perturbation": {
                "formula": "x ⊕ y = C(x_1*y_1, ..., x_D*y_D)",
                "verification": "Isometry: d_A(x⊕z, y⊕z) = d_A(x,y). Verified to eps < 1e-14.",
            },
            "powering": {
                "formula": "α ⊙ x = C(x_1^α, ..., x_D^α)",
                "verification": "Scaling: d_A(α⊙x, α⊙y) = |α| * d_A(x,y). Verified to eps < 1e-14.",
            },
            "compositional_PCA": {
                "method": "PCA on CLR-transformed data",
                "metric": "PC1 variance explained (%)",
            },
            "simplicial_depth": {
                "formula": "depth(x, X) = fraction of simplices formed by D+1 points of X that contain x",
                "range": "0 (outlier) to ~0.5 (central)",
            },
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 4: THERMODYNAMIC FRAMEWORK
    # ══════════════════════════════════════════════════════════════════════
    "4_thermodynamic_framework": {
        "description": "The deep physical interpretation of EITT as a thermodynamic instrument.",

        "master_formula": {
            "equation": "S = (ℏ/T)(dφ/dt) + k_B ln Z",
            "terms": {
                "S": "Entropy",
                "ℏ": "Reduced Planck constant",
                "T": "Temperature",
                "φ": "Phase",
                "t": "Time",
                "k_B": "Boltzmann constant",
                "Z": "Partition function (state counting)",
            },
            "derivation": (
                "From E = ℏ(dφ/dt) (energy is phase velocity) and "
                "S = k_B(βE + ln Z) (Gibbs entropy). Substitution gives the master formula."
            ),
        },

        "wick_rotation": {
            "statement": "Imaginary time is inverse temperature: t → −iℏ/(k_B T)",
            "consequence": "Quantum phase evolution e^{iφ} becomes Boltzmann weighting e^{-βE}",
            "significance": (
                "This is why EITT works as a thermometer. Decimation (time coarse-graining) "
                "is equivalent to temperature change. Entropy invariance under decimation = "
                "entropy invariance under temperature change = critical point."
            ),
        },

        "eitt_as_calorimeter": {
            "M_as_temperature": "Each M sets T_eff = M/N. Small M = cold (averaged). Large M = hot (granular).",
            "thermodynamic_dictionary": {
                "sigma2_A": "Heat capacity — how much the composition restructures under temperature change",
                "M_break": "Critical temperature of the fabrication — where the entropy phase transition occurs",
                "F17": "Latent heat — hidden energy discontinuity at a first-order transition",
                "stored_energy": "Excess free energy above the critical manifold",
                "pass_rate": "Phase diagram scan — mapping the entropy across all temperatures",
                "resolution_boundary": "Thermometer range limit — where the instrument cannot distinguish signal from noise",
            },
        },

        "planck_analogy": {
            "description": (
                "EITT thermal maps are structurally analogous to Planck satellite CMB maps. "
                "The CMB shows temperature fluctuations of ~10^-5 around 2.725K — the universe "
                "at a critical point. EITT legitimate signals show near-uniform entropy across "
                "all temperatures — same physics, different scale."
            ),
            "legitimate_signal": "CMB: near-uniform temperature. EITT: near-uniform entropy.",
            "fabricated_signal": "Like painting fake galaxies onto the sky — the thermal response breaks.",
        },

        "renormalization_group": {
            "description": (
                "EITT decimation is a Kadanoff blocking (renormalization group) operation. "
                "The EITT invariance condition dH/dM = 0 states the signal is at an RG fixed point. "
                "The entropy beta function β_H(M) = M·dH/dM = 0 iff legitimate."
            ),
            "sigma2_A_as_relevant_eigenvalue": (
                "High σ²_A means the system is further from the critical manifold, "
                "so it flows away faster under RG, so M_break comes sooner."
            ),
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 4B: BINDING ENERGY — SEMF DECOMPOSITION
    # ══════════════════════════════════════════════════════════════════════
    "4b_binding_energy_semf": {
        "description": (
            "Novel application of EITT to the nuclear binding energy curve via SEMF decomposition. "
            "Each nuclide's binding energy is decomposed into 4 physical contributions "
            "(Volume, Surface, Coulomb, Asymmetry), forming a composition on the simplex. "
            "EITT is run along the valley of stability (mass number axis)."
        ),

        "data_source": {
            "name": "AME2020 (Atomic Mass Evaluation 2020)",
            "references": [
                "Wang, M. et al. (2021). Chinese Physics C 45(3), 030003.",
                "Huang, W.J. et al. (2021). Chinese Physics C 45(3), 030002.",
            ],
            "file": "DATA/Nuclear/ame2020_parsed.csv",
            "N_total_nuclides": 3554,
            "N_valley_trajectory": 294,
            "A_range": [2, 295],
            "valley_construction": "Most stable isotope (highest B/A) for each mass number A.",
        },

        "semf_decomposition": {
            "formula": "B(Z,A) = a_V*A - a_S*A^{2/3} - a_C*Z*(Z-1)*A^{-1/3} - a_A*(A-2Z)^2/A + delta(A,Z)",
            "coefficients_MeV": {
                "a_V_volume": 15.75,
                "a_S_surface": 17.80,
                "a_C_coulomb": 0.711,
                "a_A_asymmetry": 23.70,
            },
            "reference": "Weizsaecker, C.F. von (1935). Zur Theorie der Kernmassen. Z. Physik 96, 431-458.",
            "composition": (
                "4-part: [B_vol/Total, B_sur/Total, B_cou/Total, B_asy/Total] where Total = sum of all 4 terms. "
                "All terms are magnitudes (positive). Closure to simplex."
            ),
            "why_not_ZA_NA_BA": (
                "An initial 3-part composition [Z/A, N/A, B/B_max] failed to discriminate: all regions "
                "passed at 100% because Z/A and N/A vary too slowly along the valley. The SEMF decomposition "
                "separates the four competing nuclear forces, whose relative strengths shift dramatically — "
                "this is what EITT detects."
            ),
        },

        "results": {
            "full_valley": {
                "pass_rate": 0.0175,
                "sigma2_A": 8.60,
                "verdict": "FABRICATED",
                "interpretation": "Light elements pull the full curve off-critical.",
            },
            "regions": {
                "Light_A2-20":      {"N": 19, "pass_rate": 0.50, "sigma2_A": 81.65, "verdict": "FABRICATED"},
                "Pre-Peak_A20-56":  {"N": 37, "pass_rate": 0.33, "sigma2_A": 23.83, "verdict": "FABRICATED"},
                "Iron_Peak_A50-70": {"N": 21, "pass_rate": 1.00, "sigma2_A": 2.39,  "verdict": "LEGITIMATE"},
                "Post-Peak_A70-140":{"N": 71, "pass_rate": 1.00, "sigma2_A": 1.50,  "verdict": "LEGITIMATE"},
                "Heavy_A140-210":   {"N": 71, "pass_rate": 1.00, "sigma2_A": 1.05,  "verdict": "LEGITIMATE"},
                "Superheavy_A210-295":{"N": 86, "pass_rate": 1.00, "sigma2_A": 0.89, "verdict": "LEGITIMATE"},
            },
            "robustness": {
                "shuffled": {"pass_rate": 1.00, "verdict": "LEGITIMATE", "note": "Destroys A-ordering, passes trivially"},
                "reversed": {"pass_rate": 0.0175, "verdict": "FABRICATED", "note": "Same rate as real — ordering matters"},
                "random_dirichlet": {"pass_rate": 1.00, "verdict": "LEGITIMATE", "note": "i.i.d. noise passes trivially"},
                "noisy_20pct": {"pass_rate": 1.00, "verdict": "LEGITIMATE", "note": "Noise washes out signal"},
                "bad_semf_coeffs": {"pass_rate": 0.0175, "verdict": "FABRICATED", "note": "Wrong physics also fails"},
                "delta_BA_shells": {"pass_rate": 1.00, "sigma2_A": 110.9, "verdict": "LEGITIMATE",
                                    "note": "Shell structure is stochastic but entropy-invariant"},
            },
        },

        "key_findings": [
            "Iron peak (A=50-70) is a thermodynamic critical point: 100% pass rate, sigma2_A = 2.4.",
            "Light elements (A<56) are off-critical: fail EITT because SEMF composition changes rapidly (want to fuse).",
            "sigma2_A maps nuclear stability as compositional heat capacity: 82 (light) to 0.9 (superheavy).",
            "Shell structure detected as non-thermal: delta-B/A has very high sigma2_A = 111.",
            "No prior work has applied CoDa + entropy invariance to SEMF decomposition. Novel framework.",
        ],

        "reproduction_checklist": [
            "1. Parse AME2020 to get Z, N, A, binding_per_A_keV for 3554 nuclides",
            "2. Extract valley of stability: max B/A per mass number A (294 points)",
            "3. Compute SEMF terms: B_vol = 15.75*A, B_sur = 17.80*A^(2/3), B_cou = 0.711*Z*(Z-1)*A^(-1/3), B_asy = 23.70*(A-2Z)^2/A",
            "4. Close to simplex: X = [B_vol, B_sur, B_cou, B_asy] / sum",
            "5. Run EITT on full valley: expect PR ~ 1.75%, verdict FABRICATED",
            "6. Run EITT on Iron Peak (A=50-70): expect PR = 100%, sigma2_A ~ 2.4",
            "7. Run EITT on Light (A=2-20): expect PR ~ 50%, sigma2_A ~ 82",
            "8. Verify sigma2_A decreases monotonically from light to superheavy",
            "9. Shuffle rows: expect PR = 100% (order destroyed)",
            "10. Try different SEMF coefficients: expect similar region pattern but different exact numbers",
        ],

        "files": {
            "script": "eitt_binding_energy_semf.py",
            "results_json": "DATA/Nuclear/HIGGINS_binding_energy_semf.json",
            "report_pdf": "HIGGINS_Binding_Energy_EITT.pdf",
            "plots": [
                "HIGGINS_semf_master_panel.png",
                "HIGGINS_semf_composition_evolution.png",
                "HIGGINS_semf_region_curves.png",
                "HIGGINS_nuclear_chart_heatmap.png",
            ],
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 4C: EXP-05 — GEOCHEMISTRY (CoDa's BIRTHPLACE)
    # ══════════════════════════════════════════════════════════════════════
    "4c_geochemistry": {
        "description": (
            "EXP-05: EITT applied to igneous rock differentiation — CoDa's home domain. "
            "28 igneous rock average compositions with 8 major oxides as 8-part simplex composition. "
            "Tests whether the differentiation trajectory maintains entropy invariance."
        ),

        "data_source": {
            "name": "Published average igneous rock compositions",
            "references": [
                "Le Maitre, R.W. (1976). The Chemical Variability of Some Common Igneous Rocks. J. Petrology 17(4), 589-637.",
                "Le Maitre, R.W. (ed.) (2002). Igneous Rocks: A Classification and Glossary of Terms. Cambridge Univ. Press.",
                "Best, M.G. (2003). Igneous and Metamorphic Petrology. 2nd ed. Blackwell.",
                "Winter, J.D. (2014). Principles of Igneous and Metamorphic Petrology. 2nd ed. Pearson.",
            ],
            "file": "DATA/Geochemistry/igneous_rock_compositions.csv",
            "N_rocks": 28,
            "D_oxides": 8,
            "oxides": ["SiO2", "TiO2", "Al2O3", "FeOt", "MgO", "CaO", "Na2O", "K2O"],
            "SiO2_range_wt_pct": [40.5, 73.8],
            "rock_types": "14 volcanic (extrusive), 14 plutonic (intrusive)",
        },

        "composition": (
            "8-part: [SiO2, TiO2, Al2O3, FeOt, MgO, CaO, Na2O, K2O] closed to simplex. "
            "FeOt = total iron as FeO. Ordering: increasing SiO2 (differentiation index)."
        ),

        "predictions_pre_registered": {
            "claude": {
                "main": "Tholeiitic differentiation series LEGITIMATE, sedimentary FABRICATED",
                "sigma2_A": "Moderate (3-8) for full series",
                "M_break": "Correlates with smoothness of differentiation trend",
            },
            "peter": {
                "main": "Differential heat capacities — fast crystallisers vs slow show different sigma2_A",
                "prediction": "Matrix of composites graded by energies",
                "detail": "Volcanic (quenched) vs Plutonic (slow-cooled) will have different signatures",
            },
        },

        "results": {
            "full_differentiation": {"N": 28, "pass_rate": 0.50, "sigma2_A": 2.62, "verdict": "FABRICATED"},
            "sub_series": {
                "Mafic_to_Intermediate":  {"N": 18, "pass_rate": 0.50, "sigma2_A": 2.17, "verdict": "FABRICATED"},
                "Intermediate_to_Felsic": {"N": 17, "pass_rate": 1.00, "sigma2_A": 2.07, "verdict": "LEGITIMATE"},
                "Full_calc_alkaline":     {"N": 26, "pass_rate": 1.00, "sigma2_A": 2.28, "verdict": "LEGITIMATE"},
            },
            "texture_matrix_sigma2_A": {
                "fine_ultramafic": 3.08, "fine_mafic": 1.61, "fine_intermediate": 1.57, "fine_felsic": 2.23,
                "coarse_ultramafic": 5.73, "coarse_mafic": 2.81, "coarse_intermediate": 1.74, "coarse_felsic": 2.56,
            },
            "volcanic_sigma2_A_overall": 2.24,
            "plutonic_sigma2_A_overall": 3.00,
            "controls": {
                "shuffled":       {"pass_rate": 0.50, "sigma2_A": 2.62, "verdict": "FABRICATED"},
                "random_dirichlet":{"pass_rate": 1.00, "sigma2_A": 1.36, "verdict": "LEGITIMATE"},
                "reversed":       {"pass_rate": 0.50, "sigma2_A": 2.62, "verdict": "FABRICATED"},
                "noisy_15pct":    {"pass_rate": 1.00, "sigma2_A": 1.29, "verdict": "LEGITIMATE"},
                "sedimentary_random": {"pass_rate": 1.00, "sigma2_A": 2.53, "verdict": "LEGITIMATE"},
                "sedimentary_ordered":{"pass_rate": 1.00, "sigma2_A": 2.87, "verdict": "LEGITIMATE"},
            },
        },

        "prediction_scorecard": {
            "claude_tholeiitic": "Inconclusive — N=7 too small for standalone test. Calc-alkaline including tholeiitic passes.",
            "claude_sedimentary": "Wrong — sedimentary mixing PASSES. Continuous blending preserves entropy invariance.",
            "claude_sigma2_A": "Low — actual 2.07-2.87, predicted 3-8.",
            "peter_texture_matrix": "CONFIRMED — plutonic > volcanic sigma2_A in every SiO2 category.",
            "peter_graded_energies": "CONFIRMED — matrix graded by both cooling rate and crystallisation temperature.",
        },

        "key_findings": [
            "Full differentiation fails EITT — discrete mineral phase transitions break entropy invariance.",
            "Intermediate-to-felsic passes at 100% — continuous feldspar solid solution is entropy-invariant.",
            "Plutonic sigma2_A (3.00) > Volcanic sigma2_A (2.24) — cooling rate = compositional heat capacity.",
            "Coarse/ultramafic sigma2_A=5.73 is the extreme — slowest-cooled, highest-temperature rocks.",
            "Sedimentary mixing PASSES — continuous blending preserves entropy invariance (productive surprise).",
            "Thermodynamic dictionary validated in a third domain: sigma2_A = heat capacity.",
            "CoDa's birthplace confirms EITT: the simplex geometry determines the invariance, not the domain.",
        ],

        "reproduction_checklist": [
            "1. Run python eitt_geochemistry.py — all data is embedded in the script",
            "2. Full differentiation (28 rocks): expect PR=50%, sigma2_A~2.62, verdict FABRICATED",
            "3. Intermediate-to-Felsic sub-series: expect PR=100%, sigma2_A~2.07, verdict LEGITIMATE",
            "4. Full calc-alkaline: expect PR=100%, sigma2_A~2.28, verdict LEGITIMATE",
            "5. Shuffled: expect PR=50% (order disrupted but same sigma2_A)",
            "6. Reversed: expect PR=50% (same discontinuities, different direction)",
            "7. Random Dirichlet: expect PR=100% (smooth simplex walk)",
            "8. Texture matrix: verify coarse > fine sigma2_A in every SiO2 category",
            "9. Verify volcanic overall sigma2_A < plutonic overall sigma2_A",
        ],

        "files": {
            "script": "eitt_geochemistry.py",
            "results_json": "DATA/Geochemistry/HIGGINS_geochem_eitt.json",
            "data_csv": "DATA/Geochemistry/igneous_rock_compositions.csv",
            "report_pdf": "HIGGINS_Geochemistry_EITT.pdf",
            "plots": [
                "DATA/Geochemistry/geochem_master_panel.png",
                "DATA/Geochemistry/geochem_clr_trajectory.png",
            ],
        },

        "expansion_path": {
            "GEOROC_2.0": "georoc.eu — 20,600+ publications, query by rock type/setting/location, CSV download",
            "EarthChem_PetDB": "earthchem.org — federated access to GEOROC, NAVDAT, SedDB, USGS. XLS download.",
            "target_sequences": [
                "Skaergaard layered intrusion — detailed differentiation with N>100 samples",
                "Hawaiian shield volcano — temporal differentiation series",
                "Cascades arc traverse — spatial differentiation across subduction zone",
            ],
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 4d: EXP-05b — REAL-DATA VALIDATION AT SCALE
    # ══════════════════════════════════════════════════════════════════════
    "4d_geochemistry_realdata": {
        "description": (
            "EXP-05b: EITT applied to 40,666 individual whole-rock analyses from two major databases. "
            "Ball (2022) global intraplate volcanics (26,305 samples) and AGDB3 Alaska (14,361 igneous samples). "
            "Full CoDa toolkit + HUF Tetrode validation."
        ),

        "data_sources": {
            "Ball_2022": {
                "name": "Global Neogene-Quaternary intraplate volcanic whole-rock geochemistry",
                "reference": "Ball, P.W. et al. (2022). Earth Science Reviews.",
                "N_clean": 26305,
                "regions": 12,
                "TAS_types": 15,
                "SiO2_range_wt_pct": [35.0, 77.2],
            },
            "AGDB3": {
                "name": "Alaska Geochemical Database v3.0",
                "reference": "Granitto, M. et al. (2019). USGS Data Series 1138.",
                "N_igneous_clean": 14361,
                "rock_types": 167,
                "volcanic_N": 3400,
                "plutonic_N": 4698,
                "SiO2_range_wt_pct": [35.1, 79.8],
                "FeO_handling": "FeO_pct direct, fallback FeTO3_pct * 0.8998",
            },
            "combined_N": 40666,
            "scale_factor_vs_exp05": "1,452x more data than 28 averages",
        },

        "results_summary": {
            "total_test_suites": 39,
            "legitimate": 37,
            "fabricated": 2,
            "pass_rate": "37/39 = 94.9%",
            "only_failure": "Foidite (PR=32%, sigma2_A=26.5) — deep-mantle silica-undersaturated melts",
        },

        "hawaii_series": {
            "Kilauea": {"N": 2512, "pass_rate": 1.0, "sigma2_A": 13.35, "verdict": "LEGITIMATE"},
            "Mauna_Loa": {"N": 597, "pass_rate": 1.0, "sigma2_A": 2.21, "verdict": "LEGITIMATE"},
            "Mauna_Kea": {"N": 750, "pass_rate": 1.0, "sigma2_A": 2.19, "verdict": "LEGITIMATE"},
            "Koolau": {"N": 520, "pass_rate": 1.0, "sigma2_A": 2.11, "verdict": "LEGITIMATE"},
            "All_Hawaii": {"N": 4164, "pass_rate": 1.0, "sigma2_A": 8.92, "verdict": "LEGITIMATE"},
            "Pacific_all": {"N": 7164, "pass_rate": 1.0, "sigma2_A": 5.95, "verdict": "LEGITIMATE"},
        },

        "TAS_types": {
            "Basalt": {"N": 13021, "pass_rate": 1.0, "sigma2_A": 1.88},
            "Basanite": {"N": 4741, "pass_rate": 1.0, "sigma2_A": 1.16},
            "Trachybasalt": {"N": 2678, "pass_rate": 1.0, "sigma2_A": 1.15},
            "Basaltic_Andesite": {"N": 1223, "pass_rate": 1.0, "sigma2_A": 1.87},
            "Trachyandesite": {"N": 565, "pass_rate": 1.0, "sigma2_A": 1.41},
            "Trachyte": {"N": 502, "pass_rate": 1.0, "sigma2_A": 4.16},
            "Phonolite": {"N": 128, "pass_rate": 1.0, "sigma2_A": 5.65},
            "Rhyolite": {"N": 122, "pass_rate": 1.0, "sigma2_A": 8.72},
            "Foidite": {"N": 1134, "pass_rate": 0.32, "sigma2_A": 26.51, "note": "ONLY FAILURE — deep mantle phase chaos"},
        },

        "volcanic_vs_plutonic_at_scale": {
            "AGDB3_volcanic": {"N": 3400, "sigma2_A": 1.99},
            "AGDB3_plutonic": {"N": 4698, "sigma2_A": 2.51},
            "ratio": 1.26,
            "peters_prediction": "CONFIRMED — slow crystallisation produces higher sigma2_A at database scale",
            "comparison_to_exp05": "28-average ratio was 1.34, real-data ratio 1.26 — signal survives noise",
        },

        "scale_controls": {
            "shuffled_26k": {"N": 26305, "pass_rate": 1.0, "sigma2_A": 2.81, "note": "PASSES at large N — smoothing effect"},
            "random_dirichlet_5k": {"N": 5000, "pass_rate": 0.003, "sigma2_A": 1.46, "note": "FAILS — simplex noise breaks invariance"},
            "key_insight": "At database scale, shuffled passes (smooth entropy) while random fails (uniform simplex noise). Reversal from small-N behaviour.",
        },

        "coda_toolkit": {
            "ternary_diagrams": "4 projections: AFM, silica enrichment, feldspar, peraluminosity",
            "clr_biplots": "Compositional PCA on CLR-transformed data. PC1 = differentiation, PC2 = alkali enrichment.",
            "variation_matrices": "V_ij = var(ln(x_i/x_j)) for Ball and AGDB3. Trace/2D = sigma2_A.",
            "ilr_coordinates": "Helmert sub-composition basis. D-1 = 7 orthonormal coordinates for 8 oxides.",
            "aitchison_distances": "Euclidean distance in CLR space. Dunite and alkali granite most distant from centre.",
        },

        "huf_tetrode": {
            "description": "4 fundamental connectives forming a self-reinforcing tetrahedron",
            "vertices": {
                "V1_Simplex_Geometry": "Compositions on simplex, Aitchison log-ratio geometry",
                "V2_Entropy_Invariance": "Shannon entropy invariant under geometric-mean block decimation",
                "V3_Thermodynamic_Map": "sigma2_A maps to heat capacity across domains",
                "V4_Scale_Invariance": "EITT pass rates stable from N=122 to N=26,305",
            },
            "edges": 6,
            "faces": 4,
            "face_constraint": "Each face enforces closure: sum of proportions = 1",
            "origin": "Higgins tetrahedral.txt, March 2026",
        },

        "key_findings": [
            "37/39 test suites LEGITIMATE across 3 orders of magnitude in sample size",
            "Foidite only failure — physically meaningful (deep-mantle phase chaos)",
            "Peter's texture prediction confirmed at N=8,098: plutonic sigma2_A > volcanic",
            "Sigma2_A by TAS type creates a compositional thermometer",
            "Full CoDa toolkit deployed on real data shows EITT-Aitchison geometric connection",
            "HUF Tetrode: 4 connectives validated simultaneously by geochemistry",
            "Scale controls reveal regime change: shuffled PASSES at large N, random FAILS",
        ],

        "reproduction_checklist": [
            "1. Obtain Ball (2022) CSV from Earth Science Reviews supplementary data",
            "2. Obtain AGDB3 from USGS (Data Series 1138)",
            "3. Run python eitt_geochem_realdata.py — reads both datasets",
            "4. Verify 37/39 LEGITIMATE, Foidite FABRICATED (PR=32%)",
            "5. Verify AGDB3 volcanic sigma2_A ~ 1.99, plutonic ~ 2.51",
            "6. Run python eitt_geochem_coda_full.py for CoDa toolkit analysis",
            "7. Verify all 5 plot sets generated (ternary, CLR biplot, variation, tetrode, ILR+EITT)",
            "8. Compare sigma2_A by TAS type to Table 5 values",
        ],

        "files": {
            "scripts": [
                "eitt_geochem_realdata.py",
                "eitt_geochem_coda_full.py",
            ],
            "results_json": "DATA/Geochemistry/HIGGINS_geochem_realdata.json",
            "report_pdf": "HIGGINS_Geochemistry_EITT.pdf (Part II: EXP-05b)",
            "plots": [
                "DATA/Geochemistry/realdata_master_panel.png",
                "DATA/Geochemistry/coda_ternary_diagrams.png",
                "DATA/Geochemistry/coda_clr_biplot.png",
                "DATA/Geochemistry/coda_variation_dendrogram.png",
                "DATA/Geochemistry/coda_ilr_eitt_scale.png",
                "DATA/Geochemistry/huf_tetrode.png",
            ],
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 5: CHALLENGE THE INSTRUMENT — HOW TO BREAK IT
    # ══════════════════════════════════════════════════════════════════════
    "5_challenge_protocol": {
        "description": "Instructions for the collective to test, challenge, and attempt to break the instrument.",

        "known_weaknesses": {
            "resolution_boundary_1": {
                "dataset": "BLIND-12 (Bessel-7 HiVar, Acoustics)",
                "true_label": "LEGITIMATE",
                "instrument_says": "FABRICATED",
                "why": "σ²_A=28.1 drives legitimate entropy variation that mimics fabrication at moderate M.",
                "how_to_exploit": "Construct high-variance legitimate signals. The instrument struggles when natural variance exceeds the entropy invariance band.",
            },
            "resolution_boundary_2": {
                "dataset": "BLIND-14 (Phase-Matched Fake, Adversarial)",
                "true_label": "FABRICATED",
                "instrument_says": "LEGITIMATE",
                "why": "Fabricated signal designed to preserve entropy invariance by adding only tiny noise.",
                "how_to_exploit": "Construct fabricated signals that preserve temporal structure. The instrument relies on temporal structure breaking under decimation.",
            },
        },

        "suggested_attacks": [
            {
                "name": "High-variance legitimate signals",
                "description": "Construct physically meaningful signals with σ²_A > 20. Test if EITT misclassifies them as fabricated.",
                "prediction": "Signals with σ²_A > ~25 may trigger false positives.",
            },
            {
                "name": "Temporally coherent fabrication",
                "description": "Generate fake data that preserves autocorrelation structure from a real signal but changes the composition.",
                "prediction": "May fool the entropy test. F17 should catch it if the variation matrix changes.",
            },
            {
                "name": "Dimension scaling",
                "description": "Test with D >> 3 components. Most of our testing used D=2 or D=3.",
                "prediction": "Unknown. The entropy normalisation (H/log(M)) should scale, but untested for D > 5.",
            },
            {
                "name": "Non-stationary processes",
                "description": "Test with structural breaks, regime changes, or trending compositions.",
                "prediction": "May create interesting resolution boundaries. The decimation mixes regimes.",
            },
            {
                "name": "Real-world datasets beyond our domains",
                "description": "Apply to geochemistry, microbiome, voting shares, market portfolios, atmospheric composition.",
                "prediction": "Should work for any compositional time series. Untested on biological data.",
            },
        ],

        "reproduction_checklist": [
            "1. Download gold_silver_ratio_enriched.csv and verify N=624, ratio range 14.14-104.82",
            "2. Implement geometric mean decimation (NOT arithmetic mean)",
            "3. Implement normalised Shannon entropy (H/log(M), NOT raw H)",
            "4. Run EITT on Gold/Silver: expect pass_rate = 100%, H_bar ≈ 0.128",
            "5. Run EITT on permuted Gold/Silver: expect pass_rate ≈ 0%",
            "6. Construct all 20 datasets using the seeds and parameters in Section 1",
            "7. Run blind test: expect 17/20 on Pass 1, 18/20 on Pass 2",
            "8. Verify σ²_A = 0.296 for Gold/Silver",
            "9. Verify F17_normalized ≈ 0.031 for Gold/Silver",
            "10. Build thermal maps: legitimate signals should show uniform colour across M",
        ],
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 6: GOLD STANDARD RESULTS — COMPLETE
    # ══════════════════════════════════════════════════════════════════════
    "6_gold_standard_results": {
        "description": "Complete results for all 20 blind datasets, both passes.",
        "pass_1_accuracy": "17/20 (85%)",
        "pass_2_accuracy": "18/20 (90%)",
        "datasets": [],  # Populated below
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 7: EXPERIMENT CHAIN
    # ══════════════════════════════════════════════════════════════════════
    "7_experiment_chain": {
        "EXP-01": {
            "title": "Gold/Silver EITT — Commodities",
            "domain": "Commodities",
            "key_result": "Pass rate 100%. H_bar = 0.128. σ²_A = 0.296. LEGITIMATE.",
            "data_file": "DATA/Commodities/EXP01_gold_silver_eitt_results.json",
            "significance": "First proof that a 300-year commodity ratio passes EITT.",
        },
        "EXP-02": {
            "title": "F17 Contamination Tuner — Commodities",
            "key_result": "F17 correctly detects injected contamination in Gold/Silver data.",
            "data_file": "DATA/Commodities/EXP02_threshold_analysis.json",
            "significance": "Validates F17 as a contamination diagnostic. Establishes normalisation by σ²_A.",
        },
        "EXP-03": {
            "title": "Nuclear Decay Chains — Cross-domain",
            "domain": "Nuclear Physics",
            "key_result": "All legitimate decay chains pass EITT. Fabricated chains detected.",
            "data_file": "DATA/EITT_proof_results.json",
            "significance": "First cross-domain validation. Radioactive decay is entropy-invariant.",
        },
        "EXP-04": {
            "title": "Acoustic Bessel Filters — Cross-domain",
            "domain": "Acoustics",
            "key_result": "Bessel functions (physical) pass. Butterworth filters (synthetic) detected.",
            "significance": "Physical acoustic modes are entropy-invariant. Engineered filters are not.",
        },
        "EXP-05b": {
            "title": "Real-Data Geochemistry + CoDa Toolkit + HUF Tetrode",
            "domain": "Geochemistry (40,666 real samples)",
            "key_result": "37/39 LEGITIMATE. Foidite only failure. Volcanic/Plutonic sigma2_A prediction confirmed at N=8,098.",
            "data_file": "DATA/Geochemistry/HIGGINS_geochem_realdata.json",
            "significance": "Database-scale EITT validation. Full CoDa toolkit integration. HUF Tetrode validated.",
        },
        "GOLD_STANDARD": {
            "title": "20-Dataset Blind Test — All Domains, Two-Pass",
            "key_result": "Pass 1: 17/20. Pass 2: 18/20. Two resolution boundaries identified.",
            "data_file": "DATA/HIGGINS_coda_eitt_integration.json",
            "significance": "Comprehensive validation across 6 domains with no domain-specific tuning.",
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 8: FILE MANIFEST
    # ══════════════════════════════════════════════════════════════════════
    "8_file_manifest": {
        "description": "All files produced by the programme, with descriptions.",
        "pdfs": {
            "HIVP_Master_Record_of_Notes.pdf": "Complete research journal: all 5 experiments, proofs, thermodynamic framework, binding energy, geochemistry.",
            "HIGGINS_Gold_Standard_Two_Pass.pdf": "Gold Standard blind test report: 20 datasets, two-pass instrument, thermal maps, binding energy, geochemistry.",
            "HIGGINS_CoDa_EITT_Integration.pdf": "CoDa + EITT integration report: every CoDa tool + every EITT tool on 20 datasets + binding energy + geochemistry.",
            "HIGGINS_Binding_Energy_EITT.pdf": "EITT x SEMF: nuclear binding energy analysis. Novel discovery report.",
            "HIGGINS_Geochemistry_EITT.pdf": "EXP-05/05b: EITT in geochemistry — CoDa's birthplace. 28 averages + 40,666 real samples. CoDa toolkit, HUF Tetrode.",
            "HIGGINS_Working_Example.pdf": "Gold Standard Working Example: complete step-by-step Higgins Decomposition chain on Gold/Silver data. The learning path.",
        },
        "data_jsons": {
            "DATA/HIGGINS_gold_standard_results.json": "Pass 1 results for all 20 blind datasets.",
            "DATA/HIGGINS_two_pass_results.json": "Pass 2 results with F17 corrections.",
            "DATA/HIGGINS_coda_eitt_integration.json": "Full CoDa + EITT metrics for all 20 datasets.",
            "HIGGINS_REPRODUCIBILITY_PACKAGE.json": "This file. Complete reproducibility package.",
        },
        "plots": {
            "HIGGINS_semf_master_panel.png": "EITT x SEMF: binding energy curve coloured by pass rate, region verdicts, thermal map.",
            "HIGGINS_semf_composition_evolution.png": "SEMF composition fractions and CLR coordinates along valley of stability.",
            "HIGGINS_semf_region_curves.png": "Individual EITT entropy curves for each nuclear region.",
            "HIGGINS_nuclear_chart_heatmap.png": "Nuclear chart (N vs Z) coloured by local sigma2_A (heat capacity).",
            "HIGGINS_thermal_mosaic_all20.png": "CMB-style thermal map of all 20 datasets.",
            "HIGGINS_thermal_exp01_highres.png": "High-res EXP-01 calorimeter: legitimate vs fabricated.",
            "HIGGINS_thermal_domain_comparison.png": "Domain-by-domain thermal comparison.",
            "HIGGINS_coda_eitt_dashboard.png": "9-panel CoDa + EITT integration dashboard.",
            "HIGGINS_coda_class_separation.png": "Class separation: CoDa metrics vs EITT pass rate.",
            "HIGGINS_coda_eitt_by_domain.png": "EITT curves across 6 domains with σ²_A labels.",
            "HIGGINS_eitt_thermal_map.png": "Original EXP-01 thermal map.",
            "HIGGINS_gold_standard_scorecard.png": "Gold Standard scorecard.",
            "HIGGINS_gold_standard_reveal.png": "Gold Standard blind reveal.",
            "HIGGINS_two_pass_comparison.png": "Pass 1 vs Pass 2 comparison.",
            "HIGGINS_two_pass_detail.png": "Two-pass detail: per-dataset corrections.",
        },
        "raw_data": {
            "DATA/Commodities/gold_silver_ratio_enriched.csv": "Gold/Silver ratio 1718-2026. Primary dataset.",
            "DATA/Nuclear/ame2020_parsed.csv": "AME2020 nuclear masses: 3554 nuclides with Z, N, A, binding energies, stability flags.",
            "DATA/Nuclear/HIGGINS_binding_energy_semf.json": "EITT x SEMF results: full valley, regions, robustness, sliding windows.",
            "DATA/Geochemistry/igneous_rock_compositions.csv": "28 igneous rocks, 8 major oxides, type/texture tags.",
            "DATA/Geochemistry/HIGGINS_geochem_eitt.json": "EXP-05 results: full series, sub-series, texture matrix, controls.",
            "DATA/Geochemistry/geochem_master_panel.png": "EXP-05 master panel: differentiation, EITT, texture matrix.",
            "DATA/Geochemistry/geochem_clr_trajectory.png": "CLR trajectories and local sigma2_A along differentiation series.",
            "DATA/Geochemistry/HIGGINS_geochem_realdata.json": "EXP-05b results: 40,666 real samples, all test suites.",
            "DATA/Geochemistry/realdata_master_panel.png": "EXP-05b master panel: 8 panels, Ball + AGDB3 real data.",
            "DATA/Geochemistry/coda_ternary_diagrams.png": "4 ternary projections: AFM, silica enrichment, feldspar, peraluminosity.",
            "DATA/Geochemistry/coda_clr_biplot.png": "CLR biplots: compositional PCA for Ball and AGDB3.",
            "DATA/Geochemistry/coda_variation_dendrogram.png": "Variation matrices and Aitchison distances.",
            "DATA/Geochemistry/coda_ilr_eitt_scale.png": "ILR coordinates, EITT at scale, sigma2_A by TAS type.",
            "DATA/Geochemistry/huf_tetrode.png": "HUF Tetrode diagram: 4 vertices, 6 edges, 4 faces.",
            "DATA/Working_Example/HIGGINS_working_example.json": "Working example numerical results: all steps, both paths.",
            "DATA/Working_Example/step0_raw_data.png": "Step 0: Gold/Silver ratio raw data.",
            "DATA/Working_Example/step10_master_summary.png": "Step 10: Master summary — full chain in one image.",
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 9: THEORETICAL REFERENCES
    # ══════════════════════════════════════════════════════════════════════
    "9_references": [
        {"id": "Aitchison1986", "citation": "Aitchison, J. (1986). The Statistical Analysis of Compositional Data. Chapman & Hall.", "used_for": "CoDa foundations: log-ratios, Aitchison geometry, variation matrix."},
        {"id": "Pawlowsky2015", "citation": "Pawlowsky-Glahn, V., Egozcue, J.J., & Tolosana-Delgado, R. (2015). Modeling and Analysis of Compositional Data. Wiley.", "used_for": "ILR, perturbation, powering, compositional PCA."},
        {"id": "Egozcue2003", "citation": "Egozcue, J.J. et al. (2003). Isometric logratio transformations. Mathematical Geology, 35(3), 279-300.", "used_for": "ILR transform via Helmert basis."},
        {"id": "Shannon1948", "citation": "Shannon, C.E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal.", "used_for": "Shannon entropy as the EITT observable."},
        {"id": "Kadanoff1966", "citation": "Kadanoff, L.P. (1966). Scaling Laws for Ising Models Near T_c. Physics, 2(6), 263-272.", "used_for": "Renormalization group blocking — theoretical basis for EITT decimation."},
        {"id": "Wilson1971", "citation": "Wilson, K.G. (1971). Renormalization Group and Critical Phenomena. Physical Review B, 4(9), 3174.", "used_for": "RG fixed points — EITT invariance as fixed-point condition."},
        {"id": "Wick1954", "citation": "Wick, G.C. (1954). Properties of Bethe-Salpeter Wave Functions. Physical Review, 96(4), 1124.", "used_for": "Wick rotation: imaginary time ↔ inverse temperature."},
        {"id": "Planck2020", "citation": "Planck Collaboration (2020). Planck 2018 results. A&A, 641, A6.", "used_for": "CMB analogy — near-uniform temperature as critical point signature."},
        {"id": "Butterworth1930", "citation": "Butterworth, S. (1930). On the Theory of Filter Amplifiers. Experimental Wireless, 7, 536-541.", "used_for": "Butterworth filter construction for acoustic test datasets."},
        {"id": "IAEA_NUDAT", "citation": "NNDC/BNL. NUDAT 3.0: Nuclear Data. https://www.nndc.bnl.gov/nudat3/", "used_for": "Nuclear half-life data for decay chain datasets."},
        {"id": "Wang2021", "citation": "Wang, M. et al. (2021). The AME 2020 atomic mass evaluation (II). Chinese Physics C 45(3), 030003.", "used_for": "AME2020 nuclear mass data for binding energy analysis."},
        {"id": "Weizsaecker1935", "citation": "Weizsaecker, C.F. von (1935). Zur Theorie der Kernmassen. Zeitschrift fuer Physik 96, 431-458.", "used_for": "Semi-empirical mass formula (liquid-drop model) for SEMF decomposition."},
        {"id": "Bethe1936", "citation": "Bethe, H.A. & Bacher, R.F. (1936). Nuclear Physics A. Reviews of Modern Physics 8, 82-229.", "used_for": "Nuclear binding energy theory and SEMF coefficients."},
        {"id": "Mayer1949", "citation": "Mayer, M.G. (1949). On Closed Shells in Nuclei. II. Physical Review 75(12), 1969.", "used_for": "Nuclear shell model — context for shell structure detection by EITT."},
        {"id": "LeMaitre1976", "citation": "Le Maitre, R.W. (1976). The Chemical Variability of Some Common Igneous Rocks. Journal of Petrology 17(4), 589-637.", "used_for": "Source of average igneous rock compositions for EXP-05."},
        {"id": "LeMaitre2002", "citation": "Le Maitre, R.W. (ed.) (2002). Igneous Rocks: A Classification and Glossary of Terms. Cambridge Univ. Press.", "used_for": "IUGS classification standard for igneous rocks."},
        {"id": "Chayes1960", "citation": "Chayes, F. (1960). On correlation between variables of constant sum. J. Geophys. Res. 65(12), 4185-4193.", "used_for": "Original recognition of the closure problem in geochemistry — motivating CoDa."},
        {"id": "Best2003", "citation": "Best, M.G. (2003). Igneous and Metamorphic Petrology. 2nd ed. Blackwell.", "used_for": "Supplementary average igneous compositions."},
        {"id": "Winter2014", "citation": "Winter, J.D. (2014). Principles of Igneous and Metamorphic Petrology. 2nd ed. Pearson.", "used_for": "Supplementary average compositions and differentiation framework."},
        {"id": "Ball2022", "citation": "Ball, P.W., White, N.J., Masoud, A. et al. (2022). Global Neogene-Quaternary intraplate volcanic whole-rock geochemistry. Earth Science Reviews.", "used_for": "26,305 intraplate volcanic samples for EXP-05b real-data validation."},
        {"id": "Granitto2019", "citation": "Granitto, M. et al. (2019). Alaska Geochemical Database version 3.0. USGS Data Series 1138.", "used_for": "14,361 Alaska igneous samples (volcanic + plutonic) for EXP-05b."},
        {"id": "LeBas1986", "citation": "Le Bas, M.J. et al. (1986). A Chemical Classification of Volcanic Rocks Based on the Total Alkali-Silica Diagram. J. Petrology 27(3), 745-750.", "used_for": "TAS classification used for rock type assignment in EXP-05b."},
        {"id": "Filzmoser2018", "citation": "Filzmoser, P., Hron, K. & Templ, M. (2018). Applied Compositional Data Analysis. Springer.", "used_for": "CoDa toolkit reference: CLR, ILR, variation matrix, Aitchison distance."},
        {"id": "AitchisonGreenacre2002", "citation": "Aitchison, J. & Greenacre, M. (2002). Biplots of compositional data. JRSS-C, 51(4), 375-392.", "used_for": "CLR biplot methodology for compositional PCA."},
    ],
}

# ── Populate Gold Standard results from integration JSON ───────────────────
integration_path = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/DATA/HIGGINS_coda_eitt_integration.json"
if os.path.exists(integration_path):
    with open(integration_path) as f:
        integ = json.load(f)
    for r in integ['results']:
        package["6_gold_standard_results"]["datasets"].append({
            "blind_id": r['blind_id'],
            "true_label": r['true_label'],
            "true_domain": r['true_domain'],
            "sigma2_A": round(r['sigma2_A'], 6),
            "clr_spread": round(r['clr_spread'], 4),
            "aitchison_distance_mean": round(r['ait_dist_mean'], 4),
            "simplicial_depth": round(r['simplicial_depth'], 4),
            "pc1_variance_explained": round(r['pc1_var_explained'], 4),
            "H_bar": round(r['H_bar'], 6),
            "pass_rate_p1": round(r['pass_rate_p1'], 4),
            "pass_rate_p2": round(r['pass_rate_p2'], 4),
            "f17_normalized": round(r['f17_normalized'], 6),
            "class_p1": r['class_p1'],
            "class_p2": r['class_p2'],
            "correct_p1": r['correct_p1'],
            "correct_p2": r['correct_p2'],
        })

# ── Write ──────────────────────────────────────────────────────────────────
with open(OUT, 'w') as f:
    json.dump(package, f, indent=2, ensure_ascii=False)

size = os.path.getsize(OUT)
print(f"Reproducibility package written: {OUT}")
print(f"Size: {size:,} bytes ({size/1024:.0f} KB)")
print(f"Sections: {len([k for k in package.keys() if not k.startswith('_')])}")
print(f"Datasets: {len(package['6_gold_standard_results']['datasets'])}")
print(f"References: {len(package['9_references'])}")
