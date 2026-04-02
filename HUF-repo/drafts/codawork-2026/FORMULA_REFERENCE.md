# HUF ↔ CoDa Formula Quick Reference

## Study Card — Print This

---

## 1. THE SAMPLE SPACE

| Concept | HUF Notation | CoDa Notation | Formula |
|---------|-------------|---------------|---------|
| Composition | ρ(t) = (ρ₁,...,ρ_D) | x = (x₁,...,x_D) | Σxᵢ = 1, all xᵢ > 0 |
| Simplex | "Unity constraint" | S^D | S^D = {x ∈ ℝ^D : xᵢ > 0, Σxᵢ = κ} |
| Closure operator | Normalize to 1 | C(·) | C(z₁,...,z_D) = (z₁/Σzⱼ,...,z_D/Σzⱼ) |
| Parts / carriers | ρᵢ (share) | xᵢ (component) | One element's proportion of the whole |

**Peter's version:** The simplex is a fuel gauge that reads every fuel in the tank simultaneously.

---

## 2. OPERATIONS ON THE SIMPLEX

| Operation | HUF Analogy | CoDa Name | Formula |
|-----------|------------|-----------|---------|
| "Addition" | Gain adjustment | Perturbation (⊕) | x ⊕ p = C(x₁p₁, x₂p₂, ..., x_DpD) |
| "Subtraction" | Gain difference | Perturbation difference (⊖) | x ⊖ y = C(x₁/y₁, x₂/y₂, ..., x_D/yD) |
| "Scalar multiply" | Power scaling | Powering (⊙) | α ⊙ x = C(x₁^α, x₂^α, ..., x_D^α) |
| Change between periods | Period-to-period drift | Perturbation | Δ(t) = x(t) ⊖ x(t−1) = C(xᵢ(t)/xᵢ(t−1)) |
| No change | Flat signal | Neutral element | n = C(1, 1, ..., 1) = (1/D, ..., 1/D) |

**Key insight:** On the simplex, change is multiplicative (ratios), not additive (subtraction). Perturbation IS the compositional first-difference.

---

## 3. LOG-RATIO TRANSFORMS

These move data from the simplex (constrained) to real space (unconstrained) so standard statistics apply.

| Transform | Formula | Properties | Use when |
|-----------|---------|------------|----------|
| **ALR** (Additive) | ALR(x)ᵢ = ln(xᵢ / x_D) | Simple. Asymmetric — depends on choice of denominator. NOT isometric. | Quick exploration. Not for formal analysis. |
| **CLR** (Centered) | CLR(x)ᵢ = ln(xᵢ / g(x)) where g(x) = (∏xⱼ)^(1/D) | Symmetric. Lives on hyperplane (singular covariance). Sum = 0 always. | Visualization, biplots. Intuitive. |
| **ILR** (Isometric) | ILR(x) = Ψ' · CLR(x) where Ψ is contrast matrix | Isometric (preserves distances). Full-rank. Lives in ℝ^(D-1). | Formal statistical analysis. The gold standard. |

**Peter's version:**
- ALR = measuring everything against one reference. Like setting one instrument to 0 dB and reading others relative to it. Biased by choice of reference.
- CLR = measuring everything against the geometric mean. Like measuring every instrument against the room average. Symmetric but redundant (D values for D-1 dimensions).
- ILR = measuring contrasts between groups. Like crossover frequencies — fossil vs renewable, then coal vs gas within fossil. No redundancy, no bias.

### Geometric Mean

g(x) = (x₁ · x₂ · ... · x_D)^(1/D)

This is the CoDa "center." The CLR of every component is its distance from this center in log-space.

---

## 4. DISTANCE MEASURES

| Metric | Formula | HUF Analogy | Simplex-native? |
|--------|---------|-------------|-----------------|
| **Aitchison distance** | d_A(x,y) = ‖CLR(x) − CLR(y)‖₂ | Total harmonic distortion | ✅ YES — the natural metric |
| Expanded form | d_A(x,y) = √[ (1/D) Σᵢ<ⱼ (ln(xᵢ/xⱼ) − ln(yᵢ/yⱼ))² ] | RMS of all pairwise log-ratio changes | ✅ |
| **TV distance** | d_TV(x,y) = ½ Σ|xᵢ − yᵢ| | L1 on raw shares | ❌ Not simplex-native |
| **L2 / Euclidean** | d_L2(x,y) = √(Σ(xᵢ − yᵢ)²) | Euclidean on raw shares | ❌ Not simplex-native |
| **Aitchison norm** | ‖x‖_A = d_A(x, n) where n = (1/D,...,1/D) | Distance from uniform | ✅ Measures concentration |

**Why Aitchison distance is "right":**
- Scale invariant (doubling all values doesn't change distance)
- Subcompositionally coherent (same result on subset)
- Permutation invariant (doesn't depend on component ordering)
- TV and L2 can give spurious results from closure

**The bridge:** K_eff = exp(Shannon entropy) measures effective diversity. Aitchison norm measures concentration (distance from uniform). Egozcue's poster at CoDaWork explores this relationship. **This is the open collaboration point.**

---

## 5. BALANCES (ILR COORDINATES)

Built from a Sequential Binary Partition (SBP) — a tree that splits carriers into groups.

### Example SBP for energy data:

```
All 9 carriers
├── Fossil (coal, gas, oil)          vs  Non-fossil (nuclear, hydro, wind, solar, bio, other)
│   ├── Coal  vs  Gas+Oil                    ├── Nuclear+Hydro  vs  Wind+Solar+Bio+Other
│   │       ├── Gas vs Oil                   │       ├── Wind vs Solar+Bio+Other
│   │                                        │       │       ├── Solar vs Bio+Other
│   │                                        │       │               ├── Bio vs Other
│   │                                        ├── Nuclear vs Hydro
```

### Balance formula:

b_k = √(r·s/(r+s)) · ln(g(x⁺)/g(x⁻))

Where:
- r = number of parts in the "+" group
- s = number of parts in the "−" group
- g(x⁺) = geometric mean of the "+" group
- g(x⁻) = geometric mean of the "−" group

**Peter's version:** Each balance is a crossover point. B1 = fossil vs non-fossil (the main crossover). B2 = coal vs gas (low-frequency split within fossil). B3 = wind vs solar (high-frequency split within renewables). The tree IS the crossover network.

---

## 6. CONCENTRATION & DIVERSITY

| Measure | Formula | What it tells you |
|---------|---------|-------------------|
| Shannon entropy | H(x) = −Σ xᵢ ln(xᵢ) | Diversity of the mix (higher = more spread) |
| K_eff (effective number) | K_eff = exp(H(x)) = exp(−Σ xᵢ ln(xᵢ)) | How many carriers are "effectively present" |
| Aitchison norm | ‖x‖_A = √[ (1/D) Σᵢ<ⱼ (ln(xᵢ/xⱼ))² ] | Distance from uniform distribution (higher = more concentrated) |
| Simplex variance | Var_A(x) = (1/D) Σ [CLR(xᵢ)]² | Total compositional variability |

**The relationship:** K_eff and Aitchison norm measure opposite things. K_eff ↑ means more diversity (spread). ‖x‖_A ↑ means more concentration (peaked). They're anti-correlated but the exact functional relationship is an **open question** — Egozcue's poster topic.

---

## 7. COMPOSITIONAL TIME SERIES

| Concept | Formula | HUF term |
|---------|---------|----------|
| Trajectory on simplex | {x(t)}ₜ₌₁ᵀ ∈ S^D | Composition time series |
| Period-to-period change | Δ(t) = x(t) ⊖ x(t−1) | Perturbation / drift |
| Perturbation velocity | v(t) = d_A(x(t), x(t−1)) | Year-over-year Aitchison distance |
| Cumulative drift | D(t₁,t₂) = d_A(x(t₁), x(t₂)) | Mean Drift Gap (MDG) |
| Regime boundary | t* where v(t*) >> mean(v) | Structural break |
| Distance matrix | M_ij = d_A(x(tᵢ), x(tⱼ)) | Pairwise year×year Aitchison distances |

**What to look for:**
- Perturbation velocity spike → sudden structural change (Fukushima 2011)
- Sustained high velocity → ongoing transition (German Energiewende)
- Block structure in distance matrix → distinct regimes
- CLR time series crossing zero → component going from below-average to above-average share

---

## 8. THE ZERO PROBLEM

| Zero type | Meaning | Example | Treatment |
|-----------|---------|---------|-----------|
| Rounded | Below detection limit | 0.001% solar in 1990 | Multiplicative replacement, lrEM, BM method |
| Count | Sampling artifact | Zero sightings of rare species | Bayesian-multiplicative (Martín-Fernández) |
| Structural | True absence | Country with no nuclear | **Hardest case.** Flag explicitly. May need sub-composition excluding that carrier. |

**HUF approach:** Structural zeros flagged in metadata as governance events ("this country has zero nuclear capacity by policy decision"). This is actually interpretable in CoDa terms — it's a sub-composition. When a carrier is structurally absent, analyze the remaining D-1 carriers as a sub-composition on S^(D-1).

---

## 9. SUBCOMPOSITIONAL COHERENCE

**The test:** If you analyze all 9 energy carriers and get result R₁, then analyze only the 3 fossil fuels and get result R₂, does R₂ agree with the fossil-fuel portion of R₁?

**In Aitchison geometry:** ✅ Yes, guaranteed. Log-ratios between fossil fuels are the same whether you include renewables or not.

**In raw proportions (TV, L2):** ❌ Not guaranteed. Shares of fossil fuels change when you renormalize the sub-composition.

**Why this matters for Peter:** If someone asks "is your drift detection subcompositionally coherent?" — the honest answer is "in TV/L2, probably not. In Aitchison distance, it should be by construction. That's one reason I want to move to Aitchison distance."

---

## 10. CRITICAL FORMULAS — MEMORIZE THESE

**Closure:**
C(z) = z / Σzᵢ

**Perturbation (compositional change):**
x ⊕ p = C(x₁p₁, ..., x_DpD)

**CLR transform:**
CLR(x)ᵢ = ln(xᵢ) − (1/D)Σln(xⱼ)

**Aitchison distance:**
d_A(x,y) = ‖CLR(x) − CLR(y)‖₂

**Balance:**
b = √(rs/(r+s)) · ln(g(x⁺)/g(x⁻))

**Perturbation velocity:**
v(t) = d_A(x(t), x(t−1))

**K_eff:**
K_eff = exp(−Σ xᵢ ln(xᵢ))

These seven formulas are the entire mathematical vocabulary of the conference. Everything else is built from them.

---

*Print this. Read it on the plane. Read it again at breakfast in Coimbra. By Tuesday you'll be thinking in these formulas without translating.*
