# Entropy Invariance Under Geometric-Mean Decimation of Compositional Time Series

## A Pure CoDa Formalization

**Status**: Empirical observations with mathematical framing  
**Date**: 2026-04-10  
**For**: CoDaWork 2026, Coimbra — and any CoDa practitioner  

---

## 0. Notation and Conventions

Throughout, we work on the open D-part simplex:

$$\mathcal{S}^D = \{ \mathbf{x} \in \mathbb{R}^D : x_i > 0,\ \sum_{i=1}^D x_i = \kappa \}$$

with closure operator $\mathcal{C}(\mathbf{z}) = \kappa \cdot (z_1/\sum z_j, \ldots, z_D/\sum z_j)$ and $\kappa = 1$ unless stated otherwise.

The Aitchison geometry equips $\mathcal{S}^D$ with:

- **Perturbation**: $\mathbf{x} \oplus \mathbf{p} = \mathcal{C}(x_1 p_1, \ldots, x_D p_D)$
- **Powering**: $\alpha \odot \mathbf{x} = \mathcal{C}(x_1^\alpha, \ldots, x_D^\alpha)$
- **Aitchison inner product**: $\langle \mathbf{x}, \mathbf{y} \rangle_A = \frac{1}{D} \sum_{i<j} \ln\frac{x_i}{x_j} \ln\frac{y_i}{y_j}$
- **Aitchison norm**: $\| \mathbf{x} \|_A = \sqrt{\langle \mathbf{x}, \mathbf{x} \rangle_A}$
- **Aitchison distance**: $d_A(\mathbf{x}, \mathbf{y}) = \| \mathbf{x} \ominus \mathbf{y} \|_A$

The geometric mean of a set of compositions $\{\mathbf{x}(t)\}_{t=1}^N$ is the Fréchet mean in Aitchison geometry:

$$\bar{\mathbf{x}}_G = \mathcal{C}\left(\prod_{t=1}^N x_1(t)^{1/N},\ \ldots,\ \prod_{t=1}^N x_D(t)^{1/N}\right) = \frac{1}{N} \odot \bigoplus_{t=1}^N \mathbf{x}(t)$$

Shannon entropy of a composition $\mathbf{x} \in \mathcal{S}^D$ with $\kappa = 1$:

$$H(\mathbf{x}) = -\sum_{i=1}^D x_i \ln x_i$$

The ILR transform with respect to a Sequential Binary Partition (SBP) $\Psi$:

$$\mathbf{y} = \text{ilr}(\mathbf{x}) = \Psi^\top \cdot \text{clr}(\mathbf{x}) \in \mathbb{R}^{D-1}$$

where each ILR balance coordinate is:

$$y_k = \sqrt{\frac{r_k s_k}{r_k + s_k}} \ln \frac{g(\mathbf{x}_{G_k^+})}{g(\mathbf{x}_{G_k^-})}$$

with $r_k = |G_k^+|$, $s_k = |G_k^-|$ the group sizes, and $g(\cdot)$ the geometric mean of the indexed parts.

---

## 1. Geometric-Mean Temporal Decimation

### Definition 1.1 (Block Decimation Operator)

Let $\{\mathbf{x}(t)\}_{t=1}^N$ be a compositional time series on $\mathcal{S}^D$. For block width $M \geq 2$, define the **geometric-mean block decimation** operator $\mathcal{D}_M$:

$$\mathcal{D}_M\left[\{\mathbf{x}(t)\}\right] = \left\{\bar{\mathbf{x}}_G^{(b)}\right\}_{b=1}^{\lfloor N/M \rfloor}$$

where

$$\bar{\mathbf{x}}_G^{(b)} = \mathcal{C}\left(\prod_{t=(b-1)M+1}^{bM} x_i(t)^{1/M}\right)_{i=1}^D$$

Each block of $M$ consecutive compositions is replaced by their Aitchison-geometric mean. The decimated series has $\lfloor N/M \rfloor$ elements.

**Remark.** This is the natural averaging operation on $\mathcal{S}^D$ under Aitchison geometry. Block geometric means correspond to the Fréchet mean on the simplex, equivalently to the arithmetic mean in CLR coordinates:

$$\text{clr}(\bar{\mathbf{x}}_G^{(b)}) = \frac{1}{M} \sum_{t=(b-1)M+1}^{bM} \text{clr}(\mathbf{x}(t))$$

### Definition 1.2 (EITT Residual)

The **entropy invariance residual** at decimation ratio $M$ is:

$$\Delta H_M = \frac{1}{\lfloor N/M \rfloor} \sum_{b=1}^{\lfloor N/M \rfloor} H(\bar{\mathbf{x}}_G^{(b)}) - \frac{1}{N} \sum_{t=1}^N H(\mathbf{x}(t))$$

expressed as a percentage of the base entropy:

$$\delta_M = \frac{\Delta H_M}{\bar{H}} \times 100\%$$

where $\bar{H} = \frac{1}{N}\sum_t H(\mathbf{x}(t))$.

---

## 2. Empirical Observation: Entropy Near-Invariance

### Observation 2.1 (EITT)

For stationary or slowly-varying compositional time series, the entropy residual $\delta_M$ is small:

$$|\delta_M| < 2\% \quad \text{when the autocorrelation boundary is satisfied}$$

Tested on:

| Domain | D | N | M | $\delta_M$ | 95% Bootstrap CI |
|--------|---|---|---|------------|-----------------|
| Gold/Silver prices | 2 | 339 | 2:1 | +0.085% | [−0.187%, +0.165%] |
| World electricity | 7 | 25 | 2:1 | −0.589% | [−0.969%, +0.204%] |
| Financial (price-level) | 9 | 74 | 2:1 | +0.004% | [+0.004%, +0.006%] |
| Germany electricity | 7 | 36 | 2:1 | +0.029% | [−0.119%, +0.086%] |

### Remark 2.2 (Not a Theorem)

This is an empirical observation, not a proved theorem. A second-order Taylor expansion of $H$ around the Fréchet mean $\mathbf{x}^*$ gives:

$$\Delta H_M \approx \frac{1}{2} \text{tr}\left[|\text{Hess}\,H(\mathbf{x}^*)| \cdot \text{Cov}(\bar{\mathbf{x}}_G^{(b)})\right]$$

The Hessian of $H$ on $\mathcal{S}^D$ is diagonal with $\partial^2 H / \partial x_i^2 = -1/x_i$. The geometric-mean decimation reduces $\text{Cov}(\bar{\mathbf{x}}_G^{(b)})$ relative to $\text{Cov}(\mathbf{x}(t))$, making $\Delta H_M$ small when the series is near-stationary. The first-order term vanishes because $\exp$ and $\ln$ (in the geometric mean and entropy respectively) share base $e$.

A formal proof bounding $|\delta_M|$ in terms of the Aitchison variance of the process remains open.

### Observation 2.3 (Multi-Ratio Behaviour)

$|\delta_M|$ grows with $M$. For gold/silver:

| M | $\delta_M$ |
|---|-----------|
| 2:1 | +0.085% |
| 3:1 | −0.077% |
| 5:1 | +0.530% |
| 10:1 | +1.388% |

The invariance degrades as $M$ increases. It fails ($|\delta_M| > 2\%$) when $M$ is large enough that the block width spans a non-stationary regime.

---

## 3. ILR Balance Preservation Under Decimation

### Definition 3.1 (Balance Mean Shift)

Let $\Psi$ be any valid SBP on $D$ parts, and $y_k(t) = \text{ilr}_k(\mathbf{x}(t))$ the $k$-th balance coordinate. After geometric-mean decimation $\mathcal{D}_M$, compute balances on the decimated compositions:

$$\tilde{y}_k^{(b)} = \text{ilr}_k(\bar{\mathbf{x}}_G^{(b)})$$

The **balance mean shift** is:

$$\Delta \bar{y}_k = \frac{1}{\lfloor N/M \rfloor}\sum_b \tilde{y}_k^{(b)} - \frac{1}{N}\sum_t y_k(t)$$

### Observation 3.2 (Multi-Tap Balance Preservation)

$\Delta \bar{y}_k$ is small ($< 0.1$) for all tested SBP trees, simultaneously. Tested across 8 distinct SBP configurations on energy data (D = 7):

| SBP Configuration | Balance Taps | 2:1 All Pass? | 3:1 All Pass? |
|-------------------|-------------|--------------|--------------|
| Fossil \| Renewable | 4 | Yes | Yes |
| Thermal \| Non-thermal | 4 | Yes | Yes |
| Dispatchable \| Variable | 4 | Yes | Yes |
| Carbon \| Zero-carbon | 4 | Yes | Yes |
| Coal \| Rest (sequential peel) | 4 | Yes | Yes |
| Solar \| Rest | 4 | **No** (B1 fails) | **No** (B1 fails) |
| Reversed polarity | 4 | Yes | Yes |
| Sequential peel | 4 | Yes | Yes |

Total: 213 tap measurements, 202 pass (94.8%).

### Proposition 3.3 (Why Balance Means Are Preserved — Informal)

Because $\mathcal{D}_M$ computes the arithmetic mean in CLR space (Def. 1.1 Remark), and the ILR transform is a linear isometry from CLR to balance coordinates:

$$\text{ilr}_k(\bar{\mathbf{x}}_G^{(b)}) = \text{ilr}_k\left(\text{clr}^{-1}\left(\frac{1}{M}\sum_{t \in \text{block}} \text{clr}(\mathbf{x}(t))\right)\right) = \frac{1}{M}\sum_{t \in \text{block}} y_k(t)$$

The block-level balance IS the arithmetic mean of the within-block balances. The mean of block means approaches the grand mean as block boundaries become symmetric.

**This is a property of the Aitchison geometry, not of the data.** The only data-dependent condition is whether the block boundaries introduce systematic asymmetry (i.e., whether the process is stationary within blocks).

### Observation 3.4 (Variance Reduction)

The ILR balance variance ratio under decimation is:

$$\frac{\text{Var}(\tilde{y}_k)}{\text{Var}(y_k)} \approx 0.92\text{-}0.96 \quad \text{at } M = 2$$

This ratio is approximately constant across all balances and all SBP trees (spread < 0.006 across 8 trees). The variance reduction is **SBP-invariant**, consistent with it being a property of the Aitchison inner product structure.

### Observation 3.5 (Total Variance Conservation)

The total ILR variance $V_{\text{tot}} = \sum_{k=1}^{D-1} \text{Var}(y_k)$ is related to the total Aitchison variance of the process. Under decimation, $V_{\text{tot}}$ reduces by a factor independent of SBP choice (spread < 0.01 across all trees).

This is expected: total ILR variance equals total Aitchison variance regardless of the chosen SBP (a known property of isometric coordinates).

---

## 4. Pairwise Log-Ratio Stability

### Definition 4.1 (Pairwise Log-Ratio)

For parts $i, j$:

$$\lambda_{ij}(t) = \ln \frac{x_i(t)}{x_j(t)}$$

This is the fundamental atom of compositional analysis. All log-ratio transforms (ALR, CLR, ILR) are linear combinations of pairwise log-ratios.

### Observation 4.2 (Mean Preservation)

Under geometric-mean decimation $\mathcal{D}_M$:

$$\left|\frac{1}{\lfloor N/M \rfloor}\sum_b \lambda_{ij}(\bar{\mathbf{x}}_G^{(b)}) - \frac{1}{N}\sum_t \lambda_{ij}(t)\right| < 0.02$$

for all tested pairs, at $M = 2$. The mean pairwise log-ratio is preserved.

**This follows from Proposition 3.3**: since $\text{clr}(\bar{\mathbf{x}}_G^{(b)})$ is the arithmetic mean of block CLR values, and $\lambda_{ij} = \text{clr}_i - \text{clr}_j$, the decimated log-ratio is the block mean of within-block log-ratios.

### Observation 4.3 (Variance Reduction)

$$\frac{\text{Var}(\lambda_{ij} \text{ after } \mathcal{D}_M)}{\text{Var}(\lambda_{ij} \text{ original})} \approx 0.82\text{-}0.99$$

Variance of pairwise log-ratios shrinks under decimation. The "exchange rates" between parts become smoother while their means hold.

---

## 5. Subcompositional Coherence of EITT

### Definition 5.1 (Subcomposition)

For index set $S \subset \{1, \ldots, D\}$ with $|S| \geq 2$, the subcomposition is:

$$\mathbf{x}_S = \mathcal{C}(x_i : i \in S) \in \mathcal{S}^{|S|}$$

### Observation 5.2 (EITT on Subcompositions)

If EITT holds on the full composition ($|\delta_M| < 2\%$), it generally holds on subcompositions:

| Subcomposition | Parts | $\delta_2$ |
|----------------|-------|-----------|
| Energy: Fossil only | Coal, Gas | −0.103% |
| Energy: Fossil + Nuclear | Coal, Gas, Nuclear | +0.069% |
| Energy: Coal/Gas/Wind/Solar | Transition mix | −1.638% |
| Financial: any 3-sector subset | Various | < 0.07% |

**Exception**: Energy renewables-only (Hydro, Wind, Solar, Other) gives $\delta_2 = -4.5\%$. This subcomposition is non-stationary (exponential growth of wind and solar). The failure is diagnostic: it identifies which subcomposition violates the stationarity assumption.

### Remark 5.3 (Coherence Is Expected)

The closure operation and geometric-mean decimation commute with subcomposition extraction when the parts are independent. Formally: $\mathcal{C}_S(\mathcal{D}_M[\mathbf{x}]) = \mathcal{D}_M[\mathcal{C}_S(\mathbf{x})]$ when the subcomposition is not correlated with the complement. Violations indicate dependence structure between subcompositions — itself a diagnostic.

---

## 6. The Failure Diagnostic: EITT Inversion

### Definition 6.1 (Marginal EITT)

Given a compositional time series on $\mathcal{S}^D$, form the marginal composition on $\mathcal{S}^K$ where $K < D$ by amalgamating parts:

$$x_j^{(K)} = \sum_{i \in A_j} x_i, \quad j = 1, \ldots, K$$

for some partition $\{A_1, \ldots, A_K\}$ of $\{1, \ldots, D\}$.

### Observation 6.2 (EITT Inversion Principle)

When EITT fails at dimension $K$ (i.e., $|\delta_M| > 2\%$), increasing $K$ by splitting the amalgamated parts can restore invariance. The failure at $K$ diagnoses **hidden compositional structure** within the amalgamated parts.

**Empirical precedent 1** (upward inversion): Gold/silver at K = 2 gives $\delta_{365:1} = +6.7\%$ (fails). Reconstructing K = 4 (adding volatility and momentum carriers) gives $\delta_{365:1} = +0.38\%$ (passes). The K = 2 failure diagnosed two hidden dimensions.

**Empirical precedent 2** (downward inversion — China electricity): China electricity generation (Ember data, 2000–2024, N = 25) at full K = 9 gives $\delta_{2:1} = -2.22\%$ (fails). Amalgamating to K = 3 (Fossil, Nuclear, Renewable) gives $\delta_{2:1} = -1.13\%$ (passes). Amalgamating further to K = 2 (Fossil, Non-Fossil) gives $\delta_{2:1} = -0.90\%$ (passes).

| China Electricity | K | $\delta_{2:1}$ | $\delta_{3:1}$ | Status |
|-------------------|---|----------------|----------------|--------|
| Full (9 fuels) | 9 | −2.22% | −2.33% | **FAIL** |
| Fossil/Nuclear/Renewable | 3 | −1.13% | −1.12% | PASS |
| Fossil/Non-Fossil | 2 | −0.90% | −0.89% | PASS |

The direction of inversion is reversed: here the *full* composition fails because individual parts (solar, wind) are changing too fast, and amalgamation *masks* the non-stationarity. This is the complement of the gold/silver case.

### Remark 6.3 (Compositional Interpretation — Bidirectional Inversion)

EITT inversion works in both directions:

- **Upward** (gold/silver): K too small → amalgamated parts hide internal structure → increase K restores invariance. Diagnosis: missing dimensions.
- **Downward** (China): K too large → individual parts are non-stationary → decrease K by amalgamation masks the non-stationarity. Diagnosis: exposed non-stationarity.

In CoDa terms: the EITT residual is sensitive to the choice of compositional dimension. When it fails, the *direction* of the fix (increase K or decrease K) is itself diagnostic. Upward inversion identifies hidden structure; downward inversion identifies non-stationary subcomponents. This is the compositional analogue of Simpson's paradox — marginal behaviour can differ from conditional behaviour, and the discrepancy itself carries information.

---

## 7. Adaptive Decimation: d(CoDa)/dt as Rate Controller

### Definition 7.1 (Compositional Rate of Change)

For a compositional time series $\{\mathbf{x}(t)\}$ and SBP $\Psi$, define the **balance velocity** at time $t$:

$$v_k(t) = \left|\frac{dy_k}{dt}\right| \approx \left|\frac{y_k(t+1) - y_k(t-1)}{2}\right|$$

and the **maximum compositional rate**:

$$V(t) = \max_{k=1,\ldots,D-1} v_k(t)$$

### Definition 7.2 (Adaptive Block Width)

Given thresholds $0 < \theta_L < \theta_H$ and maximum block width $M_{\max}$, define:

$$M(t) = \begin{cases} M_{\max} & \text{if } V(t) \leq \theta_L \\ 2 & \text{if } V(t) \geq \theta_H \\ \text{round}\left(M_{\max} - \frac{V(t) - \theta_L}{\theta_H - \theta_L}(M_{\max} - 2)\right) & \text{otherwise} \end{cases}$$

The adaptive decimation operator $\mathcal{D}_{\text{adapt}}$ applies variable-width blocks: starting at $t$, consume $M(t)$ consecutive compositions, compute their geometric mean, advance to $t + M(t)$, repeat.

### Observation 7.3 (Adaptive Decimation Results)

| Dataset | Fixed $\delta_{10:1}$ | Adaptive $\delta$ | Effective compression |
|---------|----------------------|-------------------|----------------------|
| Gold/Silver (N=339) | +1.388% (fail) | −0.432% (pass) | 10.0:1 |
| Energy World Solar\|Rest (N=25) | B1 shift −0.12 (fail) | B1 shift +0.08 (pass) | 3.6:1 |

**Where it fails**: Germany (N=36), where the entire series is non-stationary. When there is no slow regime to compress, adaptive taps cannot help.

### Remark 7.4 (Operational Interpretation)

$V(t)$ serves as a **stationarity diagnostic**: it identifies when and where the compositional process is changing too fast for any given compression level. This gives d(CoDa)/dt a concrete operational role — it is the control signal that determines the maximum safe averaging window at each time step.

Even when adaptive decimation fails to rescue the entropy invariance, $V(t)$ itself is informative: the temporal profile of maximum balance velocity identifies structural breaks, transition periods, and the specific balances (parts) responsible.

---

## 8. Renyi/Tsallis Generalization: Shannon Is Not Special

### Observation 8.1 (Renyi Invariance)

Define the Renyi entropy of order $q$ on $\mathcal{S}^D$:

$$H_q(\mathbf{x}) = \frac{1}{1-q} \ln \sum_{i=1}^D x_i^q, \quad q > 0,\ q \neq 1$$

with $\lim_{q \to 1} H_q = H$ (Shannon). Under geometric-mean decimation $\mathcal{D}_M$, the Renyi residual $\delta_M^{(q)}$ was tested across $q \in [0.1, 5.0]$:

| $q$ | Energy World $\delta_{2:1}$ | Gold/Silver $\delta_{2:1}$ | India $\delta_{2:1}$ |
|-----|---------------------------|---------------------------|---------------------|
| 0.1 | −0.15% | — | — |
| 0.5 | −0.33% | +0.13% | −0.12% |
| 1.0 | −0.42% (Shannon) | +0.19% (Shannon) | −0.02% (Shannon) |
| 2.0 | −0.45% | +0.20% | +0.21% |
| 5.0 | −0.49% | — | — |

All $|\delta_M^{(q)}| < 2\%$ across the entire tested range. The Tsallis entropy $S_q = (1 - \sum x_i^q)/(q-1)$ shows the same pattern.

### Remark 8.2 (Interpretation: The Geometry, Not The Functional)

The near-invariance is **not a property of Shannon entropy**. It is a property of the geometric-mean decimation operator acting on the simplex. Any smooth functional $F: \mathcal{S}^D \to \mathbb{R}$ whose Hessian is bounded will exhibit near-invariance when the process has small Aitchison variance, because:

1. $\mathcal{D}_M$ computes arithmetic means in CLR space (Def. 1.1 Remark)
2. The CLR mean is close to the original compositions when variance is small
3. Any smooth $F$ evaluated at the mean is close to the mean of $F$ (Jensen's inequality remainder)

The q-scan shows a weak monotonic trend: $|\delta|$ increases slightly with $q$ on energy data (from 0.15% at $q=0.1$ to 0.49% at $q=5.0$). This is consistent with higher-order Renyi entropies being more sensitive to the tails of the composition.

**This resolves the "why Shannon?" question**: Shannon was our initial observable, but the phenomenon lives in the Aitchison geometry. Shannon entropy is not privileged — it was simply the first functional we tested.

---

## 9. Arithmetic vs Geometric Mean: An Open Problem

### Observation 8.1

At $M = 2:1$, both geometric-mean and arithmetic-mean decimation produce small residuals across all tested datasets:

| Dataset | $\delta_2^{\text{geom}}$ | $\delta_2^{\text{arith}}$ | Gap |
|---------|------------------------|--------------------------|-----|
| Gold/Silver | +0.085% | +0.138% | 0.053% |
| Energy World | −0.589% | −0.565% | 0.024% |
| Financial | +0.004% | +0.005% | 0.001% |

The gap remains small even at $M = 10:1$.

### Remark 8.2

CoDa theory prescribes the geometric mean as the correct averaging operation on the simplex (it is the Fréchet mean under the Aitchison metric). The arithmetic mean is NOT a simplex operation — it does not respect the Aitchison geometry. However, for near-stationary processes with small variance, the two means are close (first-order equivalence).

Empirically discriminating them requires either: (a) high compression ratios on long series, (b) high-variance compositional processes, or (c) theoretical arguments from the Aitchison geometry.

**This is an honest limitation**: we cannot empirically demonstrate geometric-mean superiority on the current datasets. The theoretical argument is correct but the empirical evidence is inconclusive.

---

## 10. Aitchison Distance Behaviour Under Decimation

### Observation 9.1 (Distance Expansion)

Consecutive Aitchison distances **grow** under decimation:

$$\frac{\bar{d}_A(\bar{\mathbf{x}}_G^{(b)}, \bar{\mathbf{x}}_G^{(b+1)})}{\bar{d}_A(\mathbf{x}(t), \mathbf{x}(t+1))} \approx M^{0.5\text{-}1.0}$$

Decimation is NOT a contraction mapping on $(\mathcal{S}^D, d_A)$.

### Remark 9.2 (Interpretation)

This is physically natural: decimated compositions span longer time intervals and are therefore further apart. The entropy remains approximately invariant while distances grow — this distinguishes EITT from a smoothing or contraction property. The invariance is specific to the Shannon entropy functional, not a general metric-space property of the decimation operator.

---

## 11. Summary of Established Results

| Property | Status | Evidence |
|----------|--------|----------|
| $\lvert\delta_M\rvert < 2\%$ at $M = 2{:}1$ for stationary series | **Empirical** | 4 domains, bootstrap CIs |
| ILR balance means preserved under $\mathcal{D}_M$ | **Mathematical** (from linearity of CLR averaging) + **Empirical** (8 SBP trees, 213 measurements, 94.8% pass) |
| Balance preservation is SBP-invariant | **Mathematical** (from isometry of ILR) + **Empirical** (variance ratio spread < 0.006 across trees) |
| Pairwise log-ratio means preserved | **Mathematical** (from CLR linearity) + **Empirical** |
| Failures diagnose non-stationarity | **Empirical** (Solar, Germany nuclear) |
| EITT inversion recovers hidden dimensions | **Empirical** (Gold/Silver K=2 → K=4, China K=9 → K=3) |
| EITT inversion is bidirectional | **Empirical** (upward: gold/silver; downward: China) |
| Renyi/Tsallis invariance holds for $q \in [0.1, 5.0]$ | **Empirical** (3 domains, fine q-scan) — Shannon is NOT special |
| d(CoDa)/dt identifies safe compression window | **Empirical** (adaptive decimation) |
| Geometric ≠ arithmetic mean empirically | **NOT demonstrated** on current data |

---

## 12. Open Problems for the CoDa Community

### O-1. Formal Bound on $|\delta_M|$

Prove: for a stationary compositional process $\{\mathbf{x}(t)\}$ on $\mathcal{S}^D$ with Aitchison variance $\sigma_A^2$ and lag-1 autocorrelation $\rho_1$, there exists a bound:

$$|\delta_M| \leq f(D, \sigma_A^2, \rho_1, M)$$

The Taylor expansion (Remark 2.2) suggests $|\delta_M| = O(\sigma_A^2)$ but a formal bound incorporating the temporal dependence structure is needed.

### O-2. Connection to Aitchison Variance Decomposition

The total Aitchison variance decomposes as $\text{totvar} = \sum_{k=1}^{D-1} \text{Var}(y_k)$ for any SBP. Under decimation, this total variance reduces by a factor that appears SBP-independent (Observation 3.5). Is this factor determined by the temporal dependence structure alone?

### O-3. Fisher-Rao Geometric Interpretation

Shannon entropy defines a Riemannian metric on the simplex (the Fisher-Rao metric). Under this metric, geometric-mean decimation may have a natural geometric interpretation as projection onto a submanifold. Does the EITT residual have a curvature interpretation?

### O-4. Renyi/Tsallis Generalization — PARTIALLY ANSWERED

Does the near-invariance hold for Renyi entropy $H_q(\mathbf{x}) = \frac{1}{1-q}\ln\sum x_i^q$ at $q \neq 1$?

**Empirical answer**: YES, for all tested $q$-values from 0.1 to 5.0.

| $q$ | Energy World $\delta_{2:1}^{\text{Renyi}}$ | Gold/Silver $\delta_{2:1}^{\text{Renyi}}$ | India $\delta_{2:1}^{\text{Renyi}}$ |
|-----|---------------------------------------------|---------------------------------------------|--------------------------------------|
| 0.5 | −0.33% | +0.13% | −0.12% |
| 1.0 | −0.42% (Shannon) | +0.19% (Shannon) | −0.02% (Shannon) |
| 2.0 | −0.45% | +0.20% | +0.21% |
| 3.0 | −0.46% | +0.20% | +0.26% |
| 5.0 | −0.49% | — | — |

All $|\delta| < 2\%$ across the entire range $q \in [0.1, 5.0]$. The invariance is **not Shannon-specific**. It appears to be a property of the geometric-mean decimation operator (Aitchison geometry), not of the entropy functional.

**Remaining open question**: A formal proof that geometric-mean decimation preserves the Renyi family. The mechanism likely follows from the same CLR-linearity that preserves balance means (Proposition 3.3), combined with the fact that $\sum x_i^q$ is a smooth functional on the simplex whose Hessian structure parallels Shannon's.

### O-5. Formal Conditions for Subcompositional EITT

Under what conditions on the dependence between $\mathbf{x}_S$ and $\mathbf{x}_{S^c}$ does EITT on the full composition imply EITT on the subcomposition? The renewable-only failure (Observation 5.2) suggests the condition relates to the stationarity of $\mathbf{x}_S$ alone, but a formal statement is needed.

### O-6. Adaptive Decimation Optimality

Given a non-stationary compositional process, does there exist an optimal adaptive block-width function $M^*(t)$ that minimizes $|\delta|$ subject to a constraint on effective compression ratio? What is the relationship between $M^*(t)$ and the balance velocity $V(t)$?

---

## Appendix A. Relationship to Standard CoDa Constructs

| This document | Standard CoDa | Reference |
|---------------|---------------|-----------|
| Geometric-mean decimation $\mathcal{D}_M$ | Fréchet mean on $(\mathcal{S}^D, d_A)$ over temporal blocks | Pawlowsky-Glahn & Egozcue (2001) |
| ILR balance $y_k$ | ILR coordinate w.r.t. SBP | Egozcue et al. (2003) |
| $\sqrt{r_k s_k/(r_k+s_k)}$ coefficient | ILR normalisation constant | Egozcue & Pawlowsky-Glahn (2005) |
| Pairwise log-ratio $\lambda_{ij}$ | Component of Aitchison inner product | Aitchison (1986) |
| Subcompositional EITT | Subcompositional coherence | Aitchison (1986), §6 |
| Balance velocity $v_k(t)$ | First difference of ILR coordinates | (new — exploratory) |
| EITT inversion | — | (new — empirical) |
| Entropy near-invariance under $\mathcal{D}_M$ | — | (new — empirical) |

---

## Appendix B. What Is NOT Claimed

1. EITT is not a theorem. It is an empirical observation awaiting formal proof.
2. The geometric-mean advantage over arithmetic mean is not empirically demonstrated at low compression ratios.
3. The spatial extension (applying $\mathcal{D}_M$ across spatial patches rather than time) has been **retracted** due to a HEALPix NESTED ordering error that invalidated the spatial adjacency assumption.
4. The financial dataset uses mean closing prices (price-level portfolio, K=9), NOT market-capitalisation weights.
5. d(CoDa)/dt (balance velocity, adaptive decimation) is an operational heuristic, not a formally optimised procedure.
6. Adaptive decimation adds hyperparameters ($\theta_L$, $\theta_H$) and cannot rescue data that is non-stationary everywhere.

---

*All empirical results are reproducible from the scripts in `code/analysis/`. All raw data is in the repository.*
