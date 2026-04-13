# The EITT Decomposition Framework

## Entropy Contour Navigation on the Compositional Simplex

**Status**: Working paper — extends EITT from diagnostic to decomposition method  
**Date**: 2026-04-11  
**For**: CoDaWork 2026, Coimbra  
**Prerequisite**: Familiarity with EITT (06_EITT_CODA_MATHEMATICS)

---

## The Starting Point

EITT measures whether Shannon entropy is preserved under geometric-mean temporal decimation. It returns a residual. If the residual is small, the process passes. If large, it fails. The failure is diagnostic — it tells you something about the data.

This document asks a different question.

Stop treating the residual as a verdict. Start treating it as a *coordinate*.

---

## 1. The Entropy Landscape

The compositional simplex $\mathcal{S}^D$ is a curved manifold. Shannon entropy $H(\mathbf{x}) = -\sum x_i \ln x_i$ defines a scalar field on this manifold — every point on the simplex has an entropy value. The level sets of this field are **entropy contours**: surfaces of constant entropy.

At the centre of the simplex (uniform composition), entropy is maximal. At the boundaries (one component dominates), entropy is minimal. The contours are nested, roughly concentric, bulging outward in the interior and compressing near the edges.

The Fisher-Rao metric gives this landscape a Riemannian structure. The Hessian of $H$ has diagonal entries $-1/x_i$. This curvature is gentle in the interior (all $x_i$ moderate) and severe at the boundary (any $x_i \to 0$). The curvature is not a mystery — it is fully characterised.

A compositional time series traces a **trajectory** across this landscape.

---

## 2. Two Kinds of Motion

At any point along the trajectory, the instantaneous velocity of the composition can be decomposed into two orthogonal components with respect to the local entropy contour:

**Parallel motion** $(\mathbf{v}_\parallel)$: Movement along the entropy contour. The composition changes, but entropy stays the same. In ILR coordinates, this is the component of the balance velocity that lies tangent to the local $H = \text{const}$ surface.

**Perpendicular motion** $(\mathbf{v}_\perp)$: Movement across entropy contours. The composition changes *and* entropy changes. This is the component of the balance velocity normal to the local $H = \text{const}$ surface.

$$\mathbf{v}(t) = \mathbf{v}_\parallel(t) + \mathbf{v}_\perp(t)$$

The parallel component is what EITT can safely decimate — it moves through the simplex without disturbing the entropy landscape. The perpendicular component is what creates the EITT residual — it is the motion that geometric-mean averaging cannot absorb.

### Definition 2.1 (Entropy Gradient on the Simplex)

The gradient of Shannon entropy in CLR coordinates:

$$\nabla_{\text{clr}} H(\mathbf{x}) = \text{clr}\left(-\ln x_i - 1\right)_{i=1}^D$$

At composition $\mathbf{x}$, this vector points in the direction of maximum entropy increase. It is perpendicular to the local entropy contour.

### Definition 2.2 (Parallel-Perpendicular Decomposition)

For a balance velocity vector $\mathbf{v}(t)$ in ILR space, decompose with respect to the entropy gradient:

$$\mathbf{v}_\perp(t) = \frac{\langle \mathbf{v}(t),\, \hat{\mathbf{n}}(t) \rangle_A}{\langle \hat{\mathbf{n}}(t),\, \hat{\mathbf{n}}(t) \rangle_A} \hat{\mathbf{n}}(t)$$

$$\mathbf{v}_\parallel(t) = \mathbf{v}(t) - \mathbf{v}_\perp(t)$$

where $\hat{\mathbf{n}}(t) = \text{ilr}(\nabla_{\text{clr}} H(\mathbf{x}(t)))$ is the entropy gradient projected into ILR coordinates.

---

## 3. The Crossing Detector

EITT, reinterpreted: the residual $\delta_M$ measures the accumulated perpendicular motion over the decimation window.

When the trajectory runs parallel to entropy contours, block-averaging produces compositions on approximately the same contour. Entropy is preserved. $\delta_M \approx 0$.

When the trajectory cuts across contours, block-averaging produces compositions that sample different entropy levels. The geometric mean lands on a contour that differs from the mean of the individual contour values. $\delta_M \neq 0$.

### Definition 3.1 (Crossing Intensity)

At time $t$, define the **entropy crossing intensity**:

$$\chi(t) = \frac{\lvert \mathbf{v}_\perp(t) \rvert}{\lvert \mathbf{v}(t) \rvert}$$

This is the fraction of total compositional motion directed across entropy contours. $\chi \in [0, 1]$.

- $\chi = 0$: Pure parallel motion. No entropy contour crossing. EITT safe.
- $\chi = 1$: Pure perpendicular motion. Maximum entropy disruption. EITT fails.
- $\chi$ between: Mixed. The trajectory is angled relative to the contours.

### Proposition 3.2 (Crossing Intensity and EITT Residual)

For a compositional process with approximately constant crossing intensity $\chi$ and Aitchison variance $\sigma_A^2$:

$$\lvert \delta_M \rvert \approx \chi \cdot \sigma_A^2 \cdot g(\kappa, M)$$

where $g(\kappa, M)$ captures the curvature and block-width dependence. The residual is proportional to crossing intensity. EITT doesn't measure "how much the process moves" — it measures "how much the process moves *across* entropy contours."

---

## 4. The Winding Ratio

A trajectory can cross the same entropy contour multiple times. An oscillating composition swings back and forth across contours — high crossing count, but net perpendicular displacement may be small. A transitioning composition cuts steadily through contours — each crossing is permanent.

### Definition 4.1 (Entropy Contour Crossing Count)

For a trajectory $\lbrace\mathbf{x}(t)\rbrace_{t=1}^N$ and a reference entropy level $H_0$, define the **crossing count**:

$$C(H_0) = \#\lbrace t : H(\mathbf{x}(t)) = H_0 \text{ and } \text{sign}(\dot{H}(t^-)) \neq \text{sign}(\dot{H}(t^+)) \rbrace$$

The number of times the trajectory passes through the contour $H = H_0$.

### Definition 4.2 (Winding Ratio)

The **winding ratio** over the trajectory:

$$W = \frac{C(\bar{H})}{L_A}$$

where $\bar{H}$ is the mean entropy of the trajectory and $L_A = \sum_{t=1}^{N-1} d_A(\mathbf{x}(t), \mathbf{x}(t+1))$ is the total Aitchison path length.

$W$ is the crossing density: how many times the process crosses its own mean entropy contour, per unit distance travelled on the simplex.

**High $W$** (many crossings per unit path): The process oscillates around a stable entropy level. It is exploring the simplex while staying near one contour. Stationary. EITT-friendly.

**Low $W$** (few crossings per unit path): The process is moving steadily away from its starting entropy. It is transitioning. Each step carries it across new contours. Non-stationary. EITT-challenging.

**Zero $W$**: The process never recrosses its mean contour. Pure transition. This is what Solar does in the global electricity mix — a monotonic departure from its historical entropy neighbourhood.

### Remark 4.3 (Winding Ratio as Stationarity Diagnostic)

The winding ratio gives a continuous, entropy-geometric measure of stationarity that does not require arbitrary window sizes or significance thresholds. A process with $W > W_{\text{crit}}$ is oscillatory with respect to entropy. A process with $W < W_{\text{crit}}$ is transitional. The critical value $W_{\text{crit}}$ is determined by the curvature of the simplex at the mean composition — it depends on $D$ and on where the trajectory lives (interior vs boundary).

---

## 5. Three Layers of the Instrument

EITT began as a single diagnostic: does the residual pass or fail? The decomposition framework extends it to three layers, each built from the one below.

### Layer 1: The Residual (Existing EITT)

**Input**: Compositional time series, block width $M$.  
**Output**: $\delta_M$ — a single number.  
**Question answered**: Is entropy approximately preserved under decimation?  
**Nature**: Binary. Pass or fail.

This is the instrument as originally built. It works. It detects non-stationarity, identifies hidden dimensions (inversion), and motivates adaptive block widths. All prior EITT results live here.

### Layer 2: The Crossing Diagnostic (New)

**Input**: Compositional time series.  
**Output**: $\chi(t)$ — crossing intensity at each time step. $W$ — winding ratio over the trajectory.  
**Question answered**: How is the process moving relative to entropy contours? Is it oscillating or transitioning?  
**Nature**: Continuous. A profile, not a verdict.

Layer 2 explains *why* Layer 1 gives the answer it gives. When EITT fails, Layer 2 tells you whether the failure is because the process is cutting across contours (high $\chi$) or because it never returns to its starting contour (low $W$). These are different kinds of non-stationarity and they call for different responses.

### Layer 3: The Decomposition (New)

**Input**: Compositional time series.  
**Output**: Two separated series — the parallel component $\lbrace\mathbf{v}_\parallel(t)\rbrace$ and the perpendicular component $\lbrace\mathbf{v}_\perp(t)\rbrace$.  
**Question answered**: What part of the compositional motion preserves entropy, and what part disrupts it?  
**Nature**: Structural. A separation, not a measurement.

Layer 3 is the operational extension. Instead of rejecting a non-stationary process (Layer 1) or characterising its failure mode (Layer 2), Layer 3 *decomposes* the process into the part that EITT can safely handle and the part that carries the entropy signal.

The parallel component can be decimated normally — it moves along entropy contours and will produce small residuals by construction. The perpendicular component is the entropy-changing signal — it should be reported, not averaged away. Decimating the perpendicular component is what creates the EITT residual in the first place.

**The decomposition lets EITT work on non-stationary data** by isolating the non-stationary component of the motion rather than rejecting the entire trajectory.

---

## 6. Connecting to Prior Results

Every prior EITT result can be reinterpreted through the decomposition framework.

### The Solar | Rest B1 Failure (Observation 3.2.1 in EITT Mathematics)

Solar's exponential growth is almost entirely **perpendicular motion** — it is cutting steadily across entropy contours as its share of the electricity mix grows monotonically. The winding ratio is near zero: Solar never recrosses its historical entropy contour. Every other SBP dilutes this perpendicular signal across multiple balance coordinates. Solar | Rest concentrates it.

Layer 1 reports: B1 fails.  
Layer 2 reports: $\chi \approx 1$ for B1, $W \approx 0$ for the Solar component.  
Layer 3 separates: the perpendicular component is the entire Solar growth trajectory; the parallel component is the redistribution among other sources at roughly constant total entropy.

### The Chemistry Boundary Effect (EITT Chemistry Findings)

Compositions near the simplex boundary live in a region where the Hessian $-1/x_i$ is large. The entropy contours are compressed together. Even small compositional movements cross many contours. This means $\chi$ is elevated not because the process is moving fast, but because the contour spacing is tight.

Layer 1 reports: High residuals at the boundary.  
Layer 2 reports: Elevated $\chi$ driven by curvature, not velocity.  
Layer 3 separates: In the interior, most motion is parallel. At the boundary, the same magnitude of motion has a larger perpendicular component because the contours are closer together. This is a geometric property, not a process property.

### Adaptive Decimation (EITT Mathematics, Section 7)

The balance velocity $V(t)$ is a partial version of crossing intensity $\chi(t)$. It measures total speed without separating parallel from perpendicular. The decomposition framework refines adaptive decimation: instead of slowing the block width when *total* velocity is high, slow it only when *perpendicular* velocity is high. A process that is moving fast but parallel to contours can be decimated aggressively. A process that is moving slowly but perpendicular to contours cannot.

### EITT Inversion (EITT Mathematics, Section 6)

Upward inversion (gold/silver $K = 2 \to K = 4$): The amalgamated composition has high perpendicular motion because hidden dimensions are being projected onto a lower-dimensional simplex, distorting the entropy contour alignment. Adding dimensions restores the trajectory to a region where its natural motion is more parallel.

Downward inversion (China $K = 9 \to K = 3$): Individual non-stationary components (Solar, Wind) carry high perpendicular motion. Amalgamation averages out the perpendicular components of offsetting transitions, reducing net $\chi$.

Inversion is a dimension search for the simplex where the trajectory has the minimum crossing intensity.

### The HUF Development Index

The HUF-IDX measures a domain's distance from "ground zero" — complete comprehension. In the decomposition framework, this distance is the integrated perpendicular displacement: how far the domain's compositional reality has moved away from the entropy contour where EITT invariance holds perfectly. Domains with high HUF-IDX live in high-curvature boundary regions (chemistry) or on rapidly transitioning trajectories (energy solar). The index is the accumulated perpendicular distance.

---

## 7. What This Changes

### For EITT

The pass/fail diagnostic becomes the first layer of a three-layer instrument. Nothing is lost — Layer 1 results stand exactly as published. Layers 2 and 3 explain why they hold and extend the method to cases where Layer 1 alone cannot operate.

### For HUF-GOV

The open-loop doctrine is preserved. The instrument still reads; the human still decides. But the instrument now reads three things instead of one: the residual, the crossing profile, and the decomposed components. The loop stays open. The information content increases.

### For PRISM Resource Allocation

PRISM currently ranks allocation targets by EITT failure magnitude. The decomposition framework refines this: rank by perpendicular motion, not total residual. A domain with high residual but oscillatory crossings (high $W$) may need less attention than a domain with moderate residual but monotonic transition (low $W$). The winding ratio distinguishes "noisy but stable" from "quiet but departing."

### For CoDa

The parallel-perpendicular decomposition is not specific to Shannon entropy. Any smooth scalar field on the simplex induces contours. The Aitchison norm, total variance, any Renyi entropy — each defines its own contour landscape. The framework generalises: for any functional $F: \mathcal{S}^D \to \mathbb{R}$, decompose compositional motion into the $F$-preserving and $F$-changing components. Shannon entropy was first. It will not be last.

---

## 8. Open Problems

### D-1. Formal Proof of Proposition 3.2

Prove the proportionality between EITT residual and crossing intensity under stated conditions. The mechanism is clear from the Taylor expansion of $H$ around the Fréchet mean, but a formal bound incorporating $\chi$ as an explicit parameter is needed.

### D-2. Winding Ratio Critical Values

Determine $W_{\text{crit}}$ as a function of $D$ and mean composition. This likely connects to the curvature tensor of the Fisher-Rao metric at the mean — a known quantity.

### D-3. Optimal Decomposition-Aware Decimation

Given the parallel-perpendicular decomposition, what is the optimal decimation strategy? Decimate the parallel component at maximum $M$, report the perpendicular component at full resolution? Or is there a mixed strategy that preserves more information?

### D-4. Multi-Functional Decomposition

Perform the decomposition simultaneously for Shannon entropy, Renyi entropy at multiple $q$, and the Aitchison norm. Do the perpendicular directions coincide? If so, there is a single "entropy-changing direction" on the simplex. If not, different functionals probe different aspects of compositional change.

### D-5. Empirical Validation

Compute $\chi(t)$ and $W$ on all existing EITT datasets (gold/silver, energy, financial, chemistry). Do they predict the Layer 1 pass/fail results? Does the winding ratio separate oscillatory from transitional non-stationarity as theorised?

---

## 9. Honest Disclosures

1. Layers 2 and 3 are theoretical extensions. No empirical computation of $\chi(t)$ or $W$ has been performed yet.
2. The entropy gradient in Definition 2.1 requires compositions strictly in the simplex interior. Boundary compositions need regularisation or perturbation before the gradient is well-defined — the same boundary issue that affects EITT itself.
3. The parallel-perpendicular decomposition depends on the choice of functional ($H$, $H_q$, etc.). Different functionals give different decompositions. This is a feature (multi-functional analysis) but also a complexity.
4. The winding ratio $W$ is defined with respect to a single reference contour ($\bar{H}$). A richer characterisation might use the full crossing spectrum across all contour levels.
5. The claim that "Layer 3 lets EITT work on non-stationary data" is a conjecture. It requires empirical validation that decimating only the parallel component produces small residuals on processes where full decimation fails.
6. This framework does not close O-3 from the EITT Mathematics document. It reframes O-3 as a decomposition problem rather than a curvature interpretation problem, but the formal connection to Fisher-Rao geometry remains to be established.

---

## 10. The Instrument Reads Three Things Now

EITT asked one question: is entropy preserved?

The decomposition framework asks three:

1. Is entropy preserved? *(Layer 1 — the residual)*
2. How is the process moving relative to entropy contours? *(Layer 2 — crossing intensity and winding ratio)*
3. What part of the motion preserves entropy, and what part changes it? *(Layer 3 — the decomposition)*

The first question is a diagnostic. The second is a characterisation. The third is a method.

The instrument reads. The human decides. The loop stays open. The resolution increases.

---

*This document extends the EITT framework described in 06_EITT_CODA_MATHEMATICS.md. All prior results remain valid as Layer 1 observations. Layers 2 and 3 await empirical validation.*
