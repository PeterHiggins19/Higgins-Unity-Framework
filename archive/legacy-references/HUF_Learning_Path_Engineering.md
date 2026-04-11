# HUF Learning Path — Engineering Edition v1.1

**Enter cold. Exit hot.**

All paths are relative to the `Claude CoWorker/` folder on your machine.

> **Arriving from CoDa / Compositional Data Analysis?** Start with [`START_HERE.md`](../START_HERE.md) → "For CoDa / Compositional Data Analysts" section, then read [`THE_CORE.md`](../drafts/codawork-2026/THE_CORE.md) and [`FORMULA_REFERENCE.md`](../drafts/codawork-2026/FORMULA_REFERENCE.md). Come back here afterward for the full engineering depth — this path is 25–35 hours and assumes no CoDa background.

---

## Phase 1 — Why This Exists (1–2 hours)

Read these first. No math yet. Just the story and the big picture.

| # | Document | Location |
|---|----------|----------|
| 1 | **Origin Story** — How PLL for BTL loudspeakers led to a universal operator on the simplex. | `HUF/pillars/HUF_Origin_Story_v1.0.docx` |
| 2 | **Development Phase Close** — Peter's closing statement and the full scope of what was built. | `HUF/HUF_Development_Phase_Close_v1.0.md` |
| 3 | **Deployment Strategy & Partnership Proposal** — "A standard of standards." What HUF is, why it matters across domains, and where it's going. | `HUF/governance/HUF_Deployment_Strategy_Partnership_Proposal_Mar2026.docx` |

---

## Phase 2 — The Framework in Your Language (4–6 hours)

The context book explains what. The math book proves why. Read the Engineering editions — they speak your vocabulary.

| # | Document | Location |
|---|----------|----------|
| 4 | **Context Book — Engineering Edition** — The carrier ontology, CL-01 through CL-05, MC-1 through MC-4, IMC-PID tuning, all explained in control-systems and process-engineering language. | `HUF/corpus/context-books/HUF_Advanced_Theory_and_Concepts_Engineering_Edition.docx` |
| 5 | **Math Book — Engineering Edition** — 42 numbered items across Areas A–F (A.1–A.7, B.1–B.6, C.1–C.7, D.1–D.6, E.1–E.11, F.1–F.5); 23 indexed formal results with full proofs. Same content as every other edition; the examples and framing are engineering. | `HUF/corpus/math-books/HUF_Advanced_Mathematics_Reference_Engineering_Edition.docx` |

---

## Phase 3 — Know the Boundaries First (2–3 hours)

Before you see HUF applied, know where it does and does not work. An engineer who understands the failure envelope reads every case study differently.

| # | Document | Location |
|---|----------|----------|
| 6 | **Where HUF Does Not Apply** — Honest about the limits. Read this before you try to use HUF on something it wasn't built for. | `HUF/technical-notes/HUF_Where_HUF_Does_Not_Apply_v1.0.docx` |
| 7 | **Scrutiny Edition** — The adversarial review. Every weakness probed, every assumption challenged. You now have enough framework knowledge to understand what it's attacking. | `HUF/corpus/scrutiny-edition/HUF_v2.12_Scrutiny_Edition.docx` |

---

## Phase 4 — See It Work (3–4 hours)

Theory and boundaries established. Now see HUF applied. Pick the case studies closest to your domain, but read at least two.

| # | Document | Location |
|---|----------|----------|
| 8 | **Energy Case Study** — HUF applied to national energy generation portfolios (UK, Croatia, China). ρ = generation mix, Keff = energy transition index. | `HUF/case-studies/energy/HUF_Energy_Case_Study_v1.0.docx` |
| 9 | **Backblaze Case Study v3.0** — HUF applied to hard drive reliability portfolios. Data-rich, quarterly HDI data included. | `HUF/case-studies/backblaze/HUF_Backblaze_Case_Study_v3.0.docx` |
| 10 | **Toronto Infrastructure Case Study** — HUF applied to urban infrastructure (TTC transit). | `HUF/case-studies/toronto/HUF_Toronto_Infrastructure_v1.0.docx` |
| 11 | **Planck Case Study** — HUF applied to cosmological data. The most abstract application. | `HUF/case-studies/planck/HUF_Planck_CaseStudy_v1.0.docx` |
| 12 | **Ramsar Croatia Package** — HUF applied to wetland ecological character monitoring under the Ramsar Convention. | `HUF/case-studies/ramsar/HUF_Ramsar_Croatia_Package_Feb2026.docx` |

---

## Phase 5 — The Application That Started It All (2–3 hours)

This is where HUF was born. PLL control for BTL loudspeakers — the acoustic origin.

| # | Document | Location |
|---|----------|----------|
| 13 | **Organic Digital Loudspeakers v2.6** — The full RWA paper. 17-section dual-column technical paper. PLL control, DADC-DADI correction, Cortex-matched crossover, the complete acoustic methodology that produced HUF. | `RogueWaveAudio/Organic_Digital_Loudspeakers_v2.6.docx` |
| 14 | **BTL Build Guide v1.0** — Practical build guide for Binaural Test Lab loudspeakers. Hardware meets theory. | `RogueWaveAudio/BTL_Build_Guide_v1.0.docx` |
| 15 | **DADC-DADI** — Dimension-Apportioned Diffraction Correction and Inference. The correction algorithm. | `RogueWaveAudio/Dimension-Apportioned Diffraction Correction and Inference (DADC-DADI).docx` |

---

## Phase 6 — Deep Cuts (4–6 hours, read as needed)

The technical notes and pillar documents that fill in the engineering specifics. Not all are required — pick based on interest.

**Control Architecture & PLL:**

| # | Document | Location |
|---|----------|----------|
| 16 | **Closed Loop Control Architecture CL-01 through CL-05** — The five control layers in full technical detail. | `HUF/technical-notes/HUF_Closed_Loop_Control_Architecture_CL01-CL05.docx` |
| 17 | **PLL Engineering Precedent Note** — How phase-locked loop topology from acoustics maps to governance on the simplex. Topology and failure modes transfer; parameter values require calibration. | `HUF/technical-notes/HUF_PLL_Engineering_Precedent_Note.docx` |
| 18 | **CL-05 Calibration Study Note** — Audit-grade calibration at the highest control layer. | `HUF/technical-notes/HUF_CL05_Calibration_Study_Note.docx` |

**System Architecture:**

| # | Document | Location |
|---|----------|----------|
| 19 | **System Discriminator Intake SD-01 through SD-04** — How HUF classifies what enters the monitoring pipeline. | `HUF/technical-notes/HUF_System_Discriminator_Intake_SD01-SD04.docx` |
| 20 | **Tunable Sensing Architecture v2.0** — Adaptive sensing layer. | `HUF/technical-notes/HUF_Tunable_Sensing_Architecture_v2.0.docx` |
| 21 | **VCore Stack Brief** — The Thunderstruck / Liquid Audio Engine / V∞Core computational stack. | `HUF/technical-notes/HUF_VCore_Stack_Brief_v1.0.docx` |

**Mathematical Extensions:**

| # | Document | Location |
|---|----------|----------|
| 22 | **Fourth Category v2.6** — MC-4 monitoring in full detail. The active feedback control category. | `HUF/pillars/HUF_Fourth_Category_v2.6.docx` |
| 23 | **Sufficiency Frontier v3.6** — When is enough data enough? The statistical threshold framework. | `HUF/pillars/HUF_Sufficiency_Frontier_v3.6.docx` |
| 24 | **Triad Synthesis v1.6** — The three-way relationship between carrier, observable, and metric. | `HUF/pillars/HUF_Triad_Synthesis_v1.6.docx` |
| 25 | **Category Class Structure Tree v1.4** — The full taxonomy of HUF monitoring categories and classes. | `HUF/pillars/HUF_Category_Class_Structure_Tree_v1.4.docx` |
| 26 | **Cross-Domain Amplification Note** — How results in one domain strengthen the standard across all domains. | `HUF/technical-notes/HUF_Cross_Domain_Amplification_Note.docx` |
| 27 | **Grok SOPDT Robustness Derivation** — SOPDT quartic, nth-order generalization, FOPDT tuning table. External contribution (Grok). | `HUF/technical-notes/HUF_Grok_SOPDT_Robustness_Derivation_v1.0.docx` |

---

## Phase 7 — Build With It (2–3 hours)

| # | Document | Location |
|---|----------|----------|
| 28 | **Systems Developer Manual** — How to implement HUF in software. The builder's guide. | `HUF/corpus/developer-manual/HUF_Systems_Developer_Manual.docx` |
| 29 | **Code Appendix** — Reference implementations. | `HUF/pillars/HUF_Code_Appendix_v1.0.docx` |

---

## Phase 8 — Governance & Provenance (optional, 2–3 hours)

For readers who want to participate in shaping the standard, not just use it.

| # | Document | Location |
|---|----------|----------|
| 30 | **Governance Explainer** — How huf.org operates, the tiered model, the council structure. | `HUF/governance/HUF_Governance_Explainer_v1.0_Mar2026.docx` |
| 31 | **Collective Voting Register** — How decisions are made and recorded. | `HUF/governance/HUF_Collective_Voting_Register.docx` |
| 32 | **Operator Decision Log** — The decision trail. Every fork in the road, documented. | `HUF/governance/HUF_Operator_Decision_Log_v1_2.docx` |
| 33 | **Register Packet v3.1** — The complete machine-readable manifest of the framework. | `HUF/corpus/register-packet/HUF_Final_Register_Packet_v3.1.json` |

---

## Phase 9 — The Review Record (reference, dip in as needed)

32 collective review trace documents across 4 rounds. These are the receipts — proof that every result was independently reviewed by the 5-AI collective.

| Round | Documents | Location |
|-------|-----------|----------|
| v1 | Traces v1.0 through v1.5 + Addenda IV–V | `HUF/review-trace/v1/` |
| v2 | Traces v2.0 through v2.3 | `HUF/review-trace/v2/` |
| v4 | Traces v4.0 through v4.8 | `HUF/review-trace/v4/` |
| v5 | Traces v5.0 through v5.10 + March 2026 collective review | `HUF/review-trace/v5/` |

---

## Phase 10 — Domain Papers (pick your target)

These are the submission papers for specific organizations. Read the one that matches your interest.

| # | Document | Location |
|---|----------|----------|
| 34 | **IFAC/IEEE Control Systems** — HUF for the control engineering community. | `HUF/papers/HUF_ORG_Paper_IFAC_IEEE_ControlSystems_v2.0.docx` |
| 35 | **CoDa / Mathematical Geosciences** — HUF for the compositional data analysis community. | `HUF/papers/HUF_ORG_Paper_CoDa_MathGeosciences_v2.0.docx` |
| 36 | **Horizon Europe** — HUF as a funded research programme. | `HUF/papers/HUF_ORG_Paper_HorizonEurope_CaseForSupport_v2.0.docx` |
| 37 | **Ramsar Technical Committee** — HUF for wetland monitoring governance. | `HUF/papers/HUF_ORG_Paper_Ramsar_TechnicalCommittee_v2.0.docx` |
| 38 | **CBD Submission** — HUF as a GBF headline indicator. | `HUF/papers/HUF_ORG_Paper_CBD_Submission_v2.0.docx` |
| 39 | **GEO BON EBV Application** — HUF as an Essential Biodiversity Variable candidate. | `HUF/papers/HUF_ORG_Paper_GEOBON_EBV_Application_v2.0.docx` |
| 40 | **NERC Responsive Mode** — HUF for UK environmental monitoring. | `HUF/papers/HUF_ORG_Paper_NERC_ResponsiveMode_v2.0.docx` |

---

## Quick Reference — Wiki Articles

Short-form reference material for quick lookups.

| Document | Location |
|----------|----------|
| HUF Taxonomy Complete | `HUF/wiki/wiki_huf_taxonomy_complete.md` |
| Fourth Monitoring Category (expanded) | `HUF/wiki/wiki_fourth_monitoring_category_expanded.md` |
| Manufacturing & Electronics Assembly | `HUF/wiki/wiki_manufacturing_electronics_assembly.md` |
| Operator Entry Points | `HUF/wiki/wiki_operator_entry_points.md` |

---

**Total estimated reading time: 25–35 hours for the full path.**
**Minimum viable path (Phases 1–3 + item 16 + items 8–9): 10–14 hours.**

*An engineer enters cold at Phase 1 with a story about a man who wanted to hear Mozart better. By Phase 3 they know what it can't do. By Phase 4 they've seen it work. They exit hot at Phase 7 ready to build. Everything in between is the simplex.*
