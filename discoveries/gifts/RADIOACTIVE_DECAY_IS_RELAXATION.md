# Radioactive Decay Is Compositional Relaxation

## The Anti-Lock Signature in Nuclear Decay Chains

**Status:** Verified in EXP-03. All three chains show hill-shaped sigma_A^2.

---

## Statement

Radioactive decay, viewed as a simplex walk in (Z/A, N/A) composition space, is compositional relaxation. The sigma_A^2 trajectory along each decay chain is hill-shaped (inverted parabola) — the anti-lock signature.

The unstable heavy nucleus starts at peak compositional stress and relaxes step-by-step toward stable lead. There is no equilibrium to lock onto — only relaxation toward the endpoint.

## The Three Chains

| Chain | Steps | EITT max deviation | PLL shape | Interpretation |
|-------|-------|--------------------|-----------|----------------|
| U-238 to Pb-206 | 15 | 0.12% | hill (R^2=0.62) | Starts at peak stress, relaxes through 8 alpha + 6 beta decays |
| Th-232 to Pb-208 | 11 | 0.06% | hill (R^2=0.35) | Entire chain is descending arm — every step reduces stress |
| U-235 to Pb-207 | 12 | 0.003% | hill (R^2=0.14) | Complex path — competing alpha/beta channels create weaker structure |

All three show EITT deviations under 0.2%. Radioactive decay preserves compositional entropy to extraordinary precision.

## Physical Meaning

The hill-shaped (anti-lock) PLL signature means: the system "chose its fate" at the top of the hill (the unstable parent nucleus). Each subsequent decay step is a roll downhill toward the stable configuration (lead). The vertex — if it exists within the chain — marks the moment of maximum compositional stress, after which relaxation dominates.

This is the mirror image of the Gold/Silver parabola (bowl-shaped, stable lock). Decay is anti-lock by nature: there is no restoring force, only dissipation.

## Evidence

| Document | Location |
|----------|----------|
| EXP-03 Sealed | codawork2026/experiments/EXP-03_Uranium/EXP03_SEALED_CONCLUSION.json |

---

*Decay is the system rolling downhill. The anti-lock signature reads the slope.*

---

## Mathematical Addendum

*Appended 2026-04-18. Cross-reference: ai-refresh/HUF_MATHEMATICAL_ADDENDUM.json (T1, C1.2, SEMF formulas).*

### Formal Framework

Each step in a decay chain transforms the nucleus from (Z, A) to (Z', A') by either:

    Alpha decay: (Z, A) -> (Z-2, A-4)    [removes He-4]
    Beta decay:  (Z, A) -> (Z+1, A)      [neutron -> proton]

Each step produces a new SEMF 4-part composition x(Z', A') = C(E_V', E_S', E_C', E_A'). The sequence of compositions forms a parametric walk on S^4.

### Anti-Lock Classification (C1.2)

By Corollary C1.2, a < 0 classifies the parabola as a hill (anti-lock). For decay chains:

    sigma_A^2(step) ~ sigma_A^2(0) - |a| * step^2

The parent nucleus starts at maximum compositional stress. Each decay step reduces sigma_A^2 — the system relaxes toward the stable endpoint (Pb isotopes, sigma_A^2 ~ 1.1).

### EITT Performance on Decay Chains

Decay chains are true parametric walks: each step IS a physical transformation with similar-magnitude perturbation. This is why EITT works extraordinarily well:

| Chain | Steps | Max delta_M | Why so small |
|-------|-------|------------|-------------|
| U-238 -> Pb-206 | 15 | 0.12% | Regular stepping, smooth composition change |
| Th-232 -> Pb-208 | 11 | 0.06% | Most regular stepping pattern |
| U-235 -> Pb-207 | 12 | 0.003% | Complex alpha/beta interleaving averages well |

### Connection to PLL Engineering

| Decay concept | PLL equivalent |
|---------------|---------------|
| Parent nucleus (top of hill) | VCO at power-on (maximum frequency error) |
| Each decay step | Phase comparator correction pulse |
| Pb-206/207/208 (stable endpoint) | Locked frequency (zero error) |
| Hill-shaped sigma_A^2 | Pull-in transient (anti-lock capture) |
| No restoring force | Open-loop decay (no feedback) |

This mapping is analogical (L0) — the physics is entirely different, but the mathematical structure (hill-shaped relaxation of a variance measure along a parametric walk) is identical.
