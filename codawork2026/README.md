# CoDaWork 2026 — Complete Deliverables Package

**11th International Workshop on Compositional Data Analysis**
**1–5 June 2026, Coimbra, Portugal**

**Presenter:** Peter Higgins, Rogue Wave Audio
**Abstract:** "Compositional monitoring of energy-mix drift on the simplex" (Proceedings p. 25)

---

## What's Here

This folder contains **everything needed** for CoDaWork 2026 — presentation materials, all supporting experiments, reproducible data, and the complete evidence chain. Nothing outside this folder is required to understand, verify, or extend the work presented at Coimbra.

---

## Structure

```
codawork2026/
├── presentation/              # The talk itself
│   ├── CoDaWork2026_Higgins_Talk.pptx    # 15-minute slide deck
│   └── abstract_v3_submitted.md          # Submitted abstract text
│
├── journals/                  # All formal PDF documents
│   ├── HIVP_Master_Record_of_Notes.pdf   # Master record (32pp)
│   ├── HIGGINS_Gold_Standard_Two_Pass.pdf # Gold Standard instrument (25pp)
│   ├── HIGGINS_CoDa_EITT_Integration.pdf # CoDa integration (23pp)
│   ├── HIGGINS_Geochemistry_EITT.pdf     # Geochemistry validation (29pp)
│   ├── HIGGINS_Working_Example.pdf       # Step-by-step teaching (23pp)
│   ├── HIGGINS_Gold_Standard_Report.pdf  # Gold standard report
│   ├── HIGGINS_Binding_Energy_EITT.pdf   # Nuclear binding energy
│   ├── EXP-01_Gold_Silver_EITT_Journal.pdf
│   ├── EXP-02_US_Monthly_EITT_Journal.pdf
│   ├── EXP-03_Uranium_Test_Journal.pdf
│   └── EXP-04_Microphone_Valley_Journal.pdf
│
├── experiments/               # All computation scripts and builders
│   ├── Working_Example/       # Gold Standard Working Example
│   │   ├── step0–step10 PNG plots (11 figures)
│   │   └── HIGGINS_working_example.json  # Complete numerical results
│   ├── build_*.py             # PDF builders (reproducible)
│   └── appendix_formulae.py   # Shared formula module
│
├── reproducibility/           # Verification package
│   └── HIGGINS_REPRODUCIBILITY_PACKAGE.json (v5.0, 12 sections, 24 refs)
│
├── primers/                   # Personalized researcher briefings
│   ├── CoDaWork2026_Primer_Narayana.docx
│   ├── CoDaWork2026_Primer_Ascari.docx
│   ├── CoDaWork2026_Primer_VegaBaquero.docx
│   └── CoDaWork2026_Primer_KanjiradanVeetil.docx
│
├── preparation/               # Q&A and conversation strategy
│   ├── CoDaWork2026_QA_Preparation.docx
│   └── CoDaWork2026_ConversationGuide.docx
│
├── extended/                  # Extended results and conference handouts
│   ├── CoDaWork2026_Higgins_Extended_Results.docx
│   ├── CoDaWork2026_EITT_Handout.docx
│   ├── CoDaWork2026_EITT_CoffeeTable.docx
│   ├── CoDaWork2026_Handout_CoDa_TimeSeries.docx   # General handout: CoDa + time series
│   └── CoDaWork2026_Handout_Geochemistry_Bridge.docx # Bridge handout: geochemistry → time
│
├── science/                   # Key supporting science documents
│   ├── EITT_CoDa_Cheatsheet_v3.pdf      # One-page EITT summary
│   ├── EITT_WHY_IT_WORKS.md             # Shape/magnitude decomposition
│   ├── EITT_HESSIAN_BOUND.md            # Second-order bound
│   ├── EITT_SAFETY_BOUNDARIES.md        # When NOT to use EITT
│   ├── EITT_CODA_MATHEMATICS.md         # Full CoDa math treatment
│   ├── FORMULA_REFERENCE.md             # All formulas in one place
│   └── EITT_Adversarial_001.json        # 17-test adversarial suite
│
└── data/                      # Supporting datasets
    ├── ember/                 # EMBER energy results + protocol
    ├── gold_silver/           # Gold/Silver ratio (624 obs, 1688–2026)
    ├── geochemistry/          # Ball 2022 + AGDB3 geochemistry
    └── ngfs/                  # NGFS Phase 4 scenario data
```

## The Experiment Chain

| ID | Domain | Samples | Result | Status |
|----|--------|---------|--------|--------|
| EXP-01 | Gold/Silver Ratio | 624 | PR=97%, M_break=105 | LEGITIMATE |
| EXP-02 | US Monthly Electricity | 302 | PR=94%, all 9 carriers pass | LEGITIMATE |
| EXP-03 | Uranium-235 Binding | 235 | PR=78%, nuclear shell effects | LEGITIMATE |
| EXP-04 | Microphone Valley | 82 | PR=88%, 3-part closure confirmed | LEGITIMATE |
| EXP-05 | Geochemistry (synthetic) | 500 | PR=89–95% across series | LEGITIMATE |
| EXP-05b | Geochemistry (real data) | 40,666 | 37/39 TAS types pass | LEGITIMATE |

## Key Numbers

- **EITT Proof 1:** 0.18% entropy variation across 341:1 compression (daily→annual European electricity)
- **EITT Proof 2:** Mean 1.02% variation, all 6 countries below 2% (monthly→annual EMBER)
- **Chemistry:** 500,000 data points, 4 diagnostic lenses, interior compositions pass 54–82%
- **Geochemistry:** 40,666 rocks, 8 oxides, 37/39 TAS types LEGITIMATE, Foidite sole anomaly
- **Bell Test:** Best S=2.2018 (12.31% above classical bound), MESSAGEix Net Zero

## Posture

*We found this empirically. We can't prove it. Can you?*

Their tools. Their geometry. Our application. Their language.
