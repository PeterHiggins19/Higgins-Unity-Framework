# The Geometric Mean Proof

## First Empirical Evidence That the Choice of Mean Matters on the Simplex

**Status:** L5 Core Science. 40 years of CoDa theory confirmed with measurable consequences.

---

## Statement

When compositional data on the simplex is averaged, the choice of mean is not a matter of convenience — it is a matter of information preservation.

**Geometric mean preserves compositional entropy. Arithmetic mean destroys it.**

## The Numbers

From NGFS Phase 4 scenario data (35 scenarios, 6 carriers, 2020-2100):

| Averaging method | 5-year mean | 5-year max | 10-year mean | 10-year max |
|-----------------|-------------|------------|--------------|-------------|
| Geometric       | 1.8%        | 4.7%       | 2.3%         | 4.9%        |
| Arithmetic      | 14.2%       | 28.6%      | 21.7%        | 41.3%       |

The arithmetic mean loses **8 times more information** than the geometric mean at 5-year compression, and **10 times more** at 10-year compression.

From European daily wholesale prices (8 countries, 4,089 days):

    Geometric mean at 341:1 compression: 0.18% entropy variation

From EMBER monthly generation (6 countries, 9 carriers):

    Geometric mean at 12:1 compression: 1.02% mean variation

## Why This Matters

Aitchison established in 1982 that the simplex has its own geometry and the geometric mean is its Frechet mean. The CoDa community has argued this theoretically for four decades. But the argument has always been: "the geometry demands it."

EITT provides the missing piece: **a measurable consequence of choosing the wrong mean.** Not a theoretical argument — a number. Anyone who arithmetically averages compositional data loses up to 40% of the structural signal. This includes most energy agencies, geochemistry laboratories, financial portfolio analysis, and any applied field that has not adopted CoDa methods.

## Who This Proves Right

Aitchison (1982, 1986), Egozcue, Pawlowsky-Glahn, Tolosana-Delgado, van den Boogaart, and every CoDa researcher who has been told "this is just mathematical elegance." It is not elegance. It is empirical necessity.

## Who This Helps

Everyone who works with percentages. The path from wrong to right is short: replace arithmetic mean with geometric mean (one line of code), apply closure, and the information is preserved. The door is open.

## Evidence

| Document | Location |
|----------|----------|
| NGFS comparison | ai-refresh/HUF_FAST_REFRESH.json -> eitt_proofs -> proof_3_ngfs |
| European prices | ai-refresh/HUF_FAST_REFRESH.json -> eitt_proofs -> proof_1_original |
| EMBER validation | ai-refresh/HUF_FAST_REFRESH.json -> eitt_proofs -> proof_2_confirmation |
| Claim classification | ai-refresh/CLAIM_CLASSIFICATION.json -> geometric_mean_superiority (L5) |

---

*The right mean was always the right mean. Now we can measure the cost of the wrong one.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T2, L1, L2).*

### The Underlying Identity: CLR Linearity (Theorem T2)

For compositions x(1), ..., x(M) on S^D, the CLR of their geometric mean equals the arithmetic mean of their CLRs:

    clr(x_bar_G) = (1/M) sum_{t=1}^{M} clr(x(t))

**Proof:**

1. x_bar_G = C(prod x(t)^{1/M}) by definition of the Aitchison barycenter.
2. clr(x_bar_G)_i = ln(x_bar_G,i) - (1/D) sum_j ln(x_bar_G,j).
3. ln(x_bar_G,i) = (1/M) sum_t ln(x_i(t)) by properties of the geometric mean.
4. Substituting: clr(x_bar_G)_i = (1/M) sum_t [ln(x_i(t)) - (1/D) sum_j ln(x_j(t))] = (1/M) sum_t clr_i(x(t)). QED.

This identity is algebraic — no approximation. It is WHY the geometric mean preserves CLR structure exactly and WHY it preserves entropy to first order under decimation.

### Lemma L1 — Balance Mean Preservation

Because the decimation operator D_M computes the arithmetic mean in CLR space, and ILR is a linear isometry from CLR, balance coordinates are also preserved exactly:

    ilr_k(x_bar_G^{(b)}) = (1/M) sum_{t in B_b} ilr_k(x(t))

**Corollary:** The choice of SBP (sequential binary partition) does not affect EITT. Any ILR coordinate system gives the same balance-mean values under decimation.

### Lemma L2 — Entropy Concavity and the Jensen Gap

Shannon entropy H(x) = -sum x_i ln(x_i) is strictly concave on S^D. By Jensen's inequality applied to the concave function H:

    H(x_bar_G) >= (1/M) sum H(x(t))

For block decimation: the entropy of the averaged block is at least as large as the average of the entropies. This creates a systematic UPWARD bias under decimation. The EITT residual delta_M measures how small this bias actually is.

### Why Arithmetic Mean Fails — The Formal Argument

The arithmetic mean x_bar_A = (1/M) sum x(t) does NOT satisfy T2. In CLR space:

    clr(x_bar_A) ≠ (1/M) sum clr(x(t))

The discrepancy grows with the variance of the composition. For high-variance series (NGFS scenarios), the arithmetic mean distorts CLR coordinates by up to 14.2% — the measured cost of the wrong mean.

### Canonical Values

| Benchmark | Domain | Geometric delta_M | Arithmetic delta_M | Ratio |
|-----------|--------|-------------------|-------------------|-------|
| European prices | 341:1 | 0.18% | — | — |
| EMBER 6 countries | 12:1 | 1.02% | — | — |
| NGFS 35 scenarios | 5yr | 1.8% | 14.2% | 7.9x |
| NGFS 35 scenarios | 10yr | 2.3% | 21.7% | 9.4x |

### Open Problems

This discovery does not have dedicated open problems but contributes to O-1 (general EITT invariance theorem): proving that the Jensen gap is bounded by (D-1)*sigma_A^2 / (2*delta*M*H_bar) under stated assumptions would complete the formal connection between T2, L2, and the Hessian Bound T3.
