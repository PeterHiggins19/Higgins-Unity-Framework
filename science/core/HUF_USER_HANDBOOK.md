# Higgins Unity Framework — User Handbook
**DocCode:** HUF-HB-001  
**Title:** HUF User Handbook (Quick Reference + Guided Links)  
**Version:** 1.1  
**Status:** Draft "state of record" (handbook track)  
**Date:** 2026-04-11  
**Maintainer:** Higgins Unity Framework Collective  

---

## Purpose

This handbook is the *fast path* into HUF: a readable overview that lets a new reader:
1) understand what HUF is trying to do,  
2) learn the key terms *without* reading everything at once, and  
3) jump from any brief topic to the deeper "source" document(s).

> **Design intent:** keep the *context* flowing and human-readable; keep the *math* compact and boxed inside "Analytic" panels.

---

## How to use this handbook

### If you only have 15 minutes
1) Read **What HUF Is** → then **The Four Monitoring Categories**.  
2) Skim the category descriptions below.  
3) Pick *one* deep-dive path: **Math (CoDa)** or **Chemistry (EITT/PRISM)**.

### If you're building or auditing systems
Follow the links in each section and keep notes on:
- **Frame**: what is being measured and in what coordinate system?
- **Invariants**: what must remain true under transformation?
- **Shadows**: what projections reveal what the full object hides?
- **Actuation**: what interventions close the loop?

---

## Start here (core orientation)

- **What HUF Is (plain-language overview)**  
  → [`science/core/WHAT_HUF_IS.md`](WHAT_HUF_IS.md)

- **The Core (foundational concepts)**  
  → [`science/core/THE_CORE.md`](THE_CORE.md)

- **EITT Finding (what the method sees in practice)**  
  → [`science/core/EITT_Finding.md`](EITT_Finding.md)

- **EITT + CoDa Mathematics (formal backbone)**  
  → [`science/core/EITT_CODA_MATHEMATICS.md`](EITT_CODA_MATHEMATICS.md)

- **Complete Explanation (the full narrative)**  
  → [`science/core/EITT_Complete_Explanation.md`](EITT_Complete_Explanation.md)

- **Formula Reference (all key equations)**  
  → [`science/core/FORMULA_REFERENCE.md`](FORMULA_REFERENCE.md)

---

## The Four Monitoring Categories

> Think of HUF as a *multi-frame measurement standard*. The first three categories are universally deployed. The fourth — composition monitoring — is the one HUF proposes.

| Category | Name | Question | Status |
|----------|------|----------|--------|
| MC-1 | Magnitude Monitoring | How much? | Universally deployed |
| MC-2 | Identity Monitoring | Who or what? | Universally deployed |
| MC-3 | Trend Monitoring | Which direction? | Universally deployed |
| **MC-4** | **Composition Monitoring** | **What is the balance?** | **Proposed (HUF)** |

### MC-1, MC-2, MC-3 (the established three)
These are the monitoring categories every domain already uses. They answer magnitude, identity, and trend. They are necessary but insufficient — they can miss structural redistribution that changes the system's character without changing its headline totals.

### MC-4: Composition Monitoring (HUF's proposal)
**What it is:** monitoring the internal proportional balance of a system's parts as a primary observable.  
**Why it matters:** it exposes **ratio blindness** — when people treat relative quantities as if they were absolute, or miss redistribution that headline totals don't show.

**Read more:**  
- [`science/core/WHAT_HUF_IS.md`](WHAT_HUF_IS.md)  
- [`drafts/codawork-2026/MC4_ISO_Positioning_Document.docx`](../../drafts/codawork-2026/MC4_ISO_Positioning_Document.docx)

---

## CoDa: The Mathematical Foundation

**Compositional Data Analysis (CoDa)** is the mathematics of ratios where "parts of a whole" live on the simplex. HUF does not claim new CoDa mathematics — it claims a monitoring application built on the Aitchison framework.

Key concepts: closure, log-ratio transforms (ilr/alr/clr), Aitchison distance, simplex geometry.

**Read more:**  
- [`science/core/EITT_CODA_MATHEMATICS.md`](EITT_CODA_MATHEMATICS.md)  
- [`science/core/FORMULA_REFERENCE.md`](FORMULA_REFERENCE.md)  
- [`drafts/codawork-2026/EITT_CoDa_Cheatsheet.pdf`](../../drafts/codawork-2026/EITT_CoDa_Cheatsheet.pdf)  
- [`drafts/codawork-2026/HUF_MC4_CoDaWork_Packet_v3.pdf`](../../drafts/codawork-2026/HUF_MC4_CoDaWork_Packet_v3.pdf)

---

## EITT in one page

**EITT (Entropy Invariance under Temporal Transformation):** Shannon entropy appears empirically near-invariant under geometric-mean block decimation of compositional time series.

Measured: **0.18% variation** across a 341:1 compression ratio (daily → annual European electricity compositions). Confirmed across energy, hardware, cosmology, commodities, and chemistry (500,000 data points).

### The Chemistry Extension (April 2026)

Four diagnostic lenses applied to chemical mixture data:

| Lens | Best Region | Key Finding |
|------|------------|-------------|
| Raw Shannon | Interior (54–82% pass) | Interior standard; curvature diverges at boundary |
| Jensen-corrected | Neither (overcorrects) | Taylor expansion diverges on global traversals |
| Rényi q=2 | Marginal improvement | Wrong curvature order for the simplex |
| Aitchison norm | Boundary (closes gap from 16% to 2.5%) | Uniform curvature; the CoDa metric works |

**Read more:**  
- [`science/chemistry/EITT_Chemistry_Findings.docx`](../chemistry/EITT_Chemistry_Findings.docx) — raw science, four-lens table, failure taxonomy  
- [`science/chemistry/HUF_Development_Index.docx`](../chemistry/HUF_Development_Index.docx) — what residuals mean, domain distance from ground zero  
- [`science/chemistry/PRISM_Chemistry_Analysis.docx`](../chemistry/PRISM_Chemistry_Analysis.docx) — ranked resource allocation targets  
- [`science/chemistry/chem_eitt_pipeline.py`](../chemistry/chem_eitt_pipeline.py) — the pipeline (open source, runs on a laptop)

---

## Three frameworks from the chemistry work

| Framework | What It Does | Document |
|-----------|-------------|----------|
| **EITT Findings** | Raw science. Four-lens results, failure taxonomy, multi-modal simplex | [`EITT_Chemistry_Findings.docx`](../chemistry/EITT_Chemistry_Findings.docx) |
| **HUF-IDX** | Development index. What residuals mean. Domain distance from ground zero | [`HUF_Development_Index.docx`](../chemistry/HUF_Development_Index.docx) |
| **PRISM** | Operational layer. Ranked resource allocation targets from residual analysis | [`PRISM_Chemistry_Analysis.docx`](../chemistry/PRISM_Chemistry_Analysis.docx) |

---

## Key idea: Shadows, orthogonal views, and "seeing shape"

A **shadow** is a projection of the full system onto a reduced frame where:
- the signal becomes simpler,  
- invariants become visible, and  
- confounds become separable.

In CoDa language, a shadow can be a log-ratio coordinate view (ilr/alr/clr) or a projection along an Aitchison-orthogonal basis.

### How do we infer shape from shadows?
Use a **probe-and-rotate** routine:

1) **Define the frame**: choose what "counts as a part," and choose the closure (what sums to 1).  
2) **Choose probe contrasts**: pick log-ratio contrasts that correspond to real hypotheses.  
3) **Rotate basis**: change coordinate frames to see which features are invariant.  
4) **Compare shadows**: if multiple projections agree, you've found structure. If they disagree, you've found hidden coupling or a frame error.

**Read more:**  
- [`science/core/EITT_CODA_MATHEMATICS.md`](EITT_CODA_MATHEMATICS.md)  
- [`science/methodology/COMPOSITIONAL_GOVERNANCE_SCALE.md`](../methodology/COMPOSITIONAL_GOVERNANCE_SCALE.md)

---

## Tooling (when you want repeatability)

| Tool | Purpose | Location |
|------|---------|----------|
| Chemistry EITT pipeline | Run EITT on compositional data | [`tools/pipeline/chem_eitt_pipeline.py`](../../tools/pipeline/chem_eitt_pipeline.py) |
| HUF preparsers | Parse energy, backblaze, and general data | [`tools/pipeline/`](../../tools/pipeline/) |
| Spectrum Analyzer | Interactive visualization | [`tools/spectrum-analyzer/`](../../tools/spectrum-analyzer/) |
| Diagnostics | Validation, dashboards | [`tools/diagnostics/`](../../tools/diagnostics/) |

---

## Governance, confidence, and scale

These documents translate "insight" into "controlled use":

- **HUF Governance Charter**  
  → [`huf-gov/HUF_GOVERNANCE_CHARTER.md`](../../huf-gov/HUF_GOVERNANCE_CHARTER.md)

- **Confidence Index**  
  → [`science/methodology/CONFIDENCE_INDEX.md`](../methodology/CONFIDENCE_INDEX.md)

- **Compositional Governance Scale**  
  → [`science/methodology/COMPOSITIONAL_GOVERNANCE_SCALE.md`](../methodology/COMPOSITIONAL_GOVERNANCE_SCALE.md)

- **Kill Test (19 documented failure modes)**  
  → [`huf-gov/governance/KILL-001-kill-test.json`](../../huf-gov/governance/KILL-001-kill-test.json)

**Protocol:** HUF-GOV. Measure, report, file. No intervention on the data.

---

## Category Discovery Checklist

Use this when you suspect **ratio blindness**, projection effects ("shadows"), or stale mappings are hiding *real* structure. The goal is to decide whether your current category set is (a) sufficient, (b) missing one or more categories, or (c) using the right categories but the **wrong frame**.

### 1) Define the observation set
- What are you trying to explain (phenomenon, boundary, time scale)?
- What data is "in-bounds" vs "out-of-bounds" for this pass?
- Write the **current category mapping** you're using (even if you think it's wrong).

### 2) Audit the measurement layer (before theory)
- Units, normalization, and reference baselines (what is held constant?).
- Missingness, censoring, and known confounds.
- Are you mixing *levels* (individual vs group, local vs global) without an explicit bridge?

> **Analytic:** Category discovery fails most often at the measurement layer. If the baseline or normalization is drifting, you'll "discover" phantom categories that are just instrument movement.

### 3) Do a closure check on existing categories
- Can the current categories reproduce the observations **without** ad-hoc exceptions?
- Identify "residual structure": what's left over after the best-faith mapping?

> **Analytic:** If your residuals are *structured* (repeatable shape, phase lag, regime dependence), you're not done. If they're *unstructured* (noise-like), you may already have closure.

### 4) Run an orthogonal view sweep (shadow hunting)
- Re-express the same situation in at least **3 frames** (different axes / viewpoints).
- Track what stays invariant vs what appears/disappears under rotation.
- Anything that looks "magical" often becomes ordinary in a better frame.

Practical prompts:
- "What would I call this if I wasn't allowed to use the current category names?"
- "What's the simplest *projection* that would create this apparent pattern?"

### 5) Perform a ratio audit (anti-ratio blindness)
- List the **key ratios** the system implies (cost/benefit, signal/noise, input/output, gain/loss).
- Rewrite in log space where useful (ratios become differences).
- Look for ratios that remain stable across contexts — those are candidates for anchors.

### 6) Fixed-pole (anchor) test
Treat categories as coordinate choices around **fixed poles**: reference points that remain stable while everything else moves.
- Identify 1-2 anchors that do *not* change under the transformations you care about.
- If you can't find anchors, you may be missing a category **or** your frame is misaligned.
- If anchors exist, use them to define the "frame rails" for the rest of the mapping.

> **Analytic:** In the meromorphic analogy: fixed poles are structural constraints. They don't *explain* everything — they *pin* the allowable explanations.

### 7) Filter / phase / frequency scan (time-scale discovery)
When a category is missing, it often shows up as a **time-scale** you didn't model.
- Look for delays, phase flips, hysteresis, resonance, "ringing," overshoot/undershoot.
- Separate fast dynamics (impulse response) from slow dynamics (drift / adaptation).

> **Analytic:** A clean way to spot hidden structure is to ask: "What frequency band is this effect living in?" Distinct bands often imply distinct categories or subcategories.

### 8) Probe with controlled perturbations
- Change one input at a time (or simulate doing so) and predict the response using current categories.
- Where predictions fail consistently, log the *conditions* of failure (regimes).

### 9) Propose the smallest new category that collapses residuals
- Add **one** candidate category at a time.
- Prefer categories that:
  - reduce exceptions,
  - improve cross-domain portability,
  - and preserve the anchors from Step 6.

### 10) Validate across domains (integration test)
- Does the new category help in *another* domain without breaking the old one?
- If it only helps in one narrow corner, it might be a *feature* or *parameter*, not a category.

### 11) Record + reconcile (machine track vs human track)
- **Trace (machine):** update mappings, invariants, tests, and "why this category exists."
- **Manual (human):** explain the intuition, examples, and cultural interpretability.
- Add a glossary term and a doc index stub so the discovery is searchable and teachable.

### Quick "go / no-go" signals
- **Go (likely new category):** structured residuals, stable anchors, repeatable failure regimes, distinct time-scale behavior.
- **No-go (frame issue):** residuals vanish under rotation, ratios stabilize after renormalization, anchors emerge after redefining baselines.
- **Stop (data issue):** effects track measurement drift, sampling artifacts, or mixed levels without a bridge.

---

## Glossary (living; extend as needed)

- **Actuation:** Intervention/control step that changes the system, ideally under governance.  
- **Aitchison geometry:** Geometry for compositional data; distances/angles in the simplex.  
- **Closure:** Normalization of components to a constant sum (often 1).  
- **CoDa:** Compositional Data Analysis; ratio-based reasoning.  
- **Contrast:** A log-ratio comparison between parts (a hypothesis encoded as a coordinate).  
- **EITT:** Entropy Invariance under Temporal Transformation; Shannon entropy near-invariant under geometric-mean block decimation.  
- **Fixed pole:** An invariant anchor/boundary that stays stable across transformations.  
- **Frame:** A coordinate system + assumptions defining what is measurable/meaningful.  
- **HUF-IDX:** HUF Development Index; measures a domain's distance from ground zero via EITT residuals.  
- **MC-4:** Monitoring Category 4; composition monitoring as a primary observable.  
- **PRISM:** Post-Residual Investigation for System Maturation; converts diagnostic residuals into ranked resource allocation targets.  
- **Ratio blindness:** Mistaking relative quantities for absolute ones; ignoring compositional constraints.  
- **Shadow:** A projection of a higher-dimensional structure into a simpler frame that reveals invariants.

---

**DocCode:** HUF-HB-001  
**Path:** `science/core/HUF_USER_HANDBOOK.md`  
**Status:** Draft (handbook track)  
**Keywords:** HUF, handbook, overview, index, CoDa, EITT, PRISM, MC-4, HUF-IDX, shadows
