# The Compositional Governance Scale (CGS)
# A Five-Level Roadmap from Proof-of-Concept to Planetary Standard

**Status:** First formal definition — April 5, 2026
**Authors:** Peter Higgins + Claude (Opus 4.6)
**Supersedes:** CMSI levels in CMSI.md (the base quantity GDoF and the formula CGS = log₁₀(GDoF) are unchanged; the levels are now governance specifications, not just targets)
**Confidence level of this document:** n=1 (Opinion)

---

## Why Rename, Why Restructure

The Complex Mixed Systems Index (CMSI) defined a target. It told you where Level 3 was. It did not tell you how to get there.

A target is necessary. A target is not sufficient. What is needed is a **governance specification at each level** — not just a number to reach, but the structural, empirical, and institutional requirements that must be satisfied before claiming that level. The Kardashev scale has this implicitly (you cannot claim K1 without harnessing an entire star's output reaching Earth). We need it explicitly.

The rename:

| Old | New | Reason |
|-----|-----|--------|
| Complex Mixed Systems Index (CMSI) | **Compositional Governance Scale (CGS)** | "Compositional" is precise — it anchors to CoDa. "Governance" says what the scale measures. "Scale" says it is logarithmic and ordinal. Three words, each doing work. |
| CMSI Level 0–4 | **CGS-1 through CGS-5** | Levels start at 1 because there is no governance at zero. Each level is a gate, not a range. You are AT a level when you satisfy its requirements, not when your GDoF falls in a band. |
| Governed Degrees of Freedom (GDoF) | **GDoF** (unchanged) | The base quantity is correct. GDoF = Σ(C_d × S_d × I_d × T_d) across domains. CGS = log₁₀(GDoF). |

The formula is unchanged. The ambition is unchanged. What changes is this: **each level now tells you what to build, not just what to count.**

---

## The Base Quantity (Unchanged)

```
GDoF_d = (carriers_d − 1) × sites_d × diagnostics_d × temporal_scales_d

GDoF = Σ GDoF_d   (summed across all governed domains d = 1 to D)

CGS = log₁₀(GDoF)
```

Every term is countable. The product is multiplicative because the dimensions are independent (Ashby). The index is logarithmic because system complexity grows exponentially (Kardashev). Nothing changes here. The measurement science is sound.

---

## The Five Levels: Governance Gates

Each level has four components:

1. **Threshold** — The minimum GDoF and CGS value
2. **Structure** — What must exist architecturally
3. **Evidence** — What must be demonstrated empirically
4. **Institution** — What external validation is required

You do not claim a level by reaching the threshold alone. You claim it by satisfying all four gates. A system with GDoF = 10,000 that has never been independently reviewed is not CGS-3. It is CGS-1 with ambition.

---

### CGS-1: Instrument Proof
**"Does the instrument work on one system?"**

| Gate | Requirement | HUF Status |
|------|-------------|------------|
| **Threshold** | GDoF ≥ 10, CGS ≥ 1.0 | ✓ GDoF = 48, CGS = 1.68 |
| **Structure** | Single domain. Defined carrier set. At least 2 independent diagnostics. SBP specified. Error catalogue started. | ✓ EMBER. 9 carriers. TV + Aitchison. SBP defined. E-01–E-17. |
| **Evidence** | Diagnostics detect at least one known event correctly. False positive rate estimated. Dual metric agreement demonstrated on at least one event. | ✓ Fukushima, German nuclear exit, UK coal collapse — all detected. Agreement patterns documented. |
| **Institution** | None required beyond the author(s). Self-assessment documented. | ✓ GOVERNANCE_DECLARATION.md. 8 KU, 5 doubts. |

**Where HUF stands:** CGS-1 satisfied. This is honest. EMBER on three countries with two diagnostics, known events detected, self-assessment published. This is a working proof-of-concept.

**What CGS-1 means for any system:** You have shown your instrument can measure something real. The carrier set is defined, the diagnostics are specified, at least one event is correctly detected, and you have been honest about what you do not know. You are a screwdriver that has turned one screw.

---

### CGS-2: Cross-Domain Validation
**"Does the instrument work on a different system?"**

| Gate | Requirement | HUF Status |
|------|-------------|------------|
| **Threshold** | GDoF ≥ 100, CGS ≥ 2.0 | ✗ Need cross-domain data |
| **Structure** | At least 2 independent domains. Third diagnostic (CR or equivalent) implemented. Independence of diagnostics formally assessed. GDoF formula applied and published. | ✗ CR not computed. Independence untested. |
| **Evidence** | Diagnostics detect known events in BOTH domains. Cross-domain GDoF calculated. Coherence residual computed on at least one dataset. 3^n confidence at n ≥ 3 for primary domain. | ✗ Backblaze not processed. CR not computed. |
| **Institution** | Peer presentation at a recognised conference. At least one domain expert has reviewed the methodology. Written feedback received and documented. | ✗ Coimbra is the first attempt. |

**Where HUF stands:** CGS-2 not yet reached. This is the immediate target.

**The path to CGS-2 — five concrete steps:**

| Step | Action | What It Delivers | Timeline |
|------|--------|-------------------|----------|
| 1 | Compute coherence residual on EMBER | Third diagnostic. n=3 for EMBER. Evidence gate partially opened. | This week |
| 2 | Run Backblaze proof-of-concept | Second domain. GDoF jumps to ~632. Cross-domain structure gate opened. | This week |
| 3 | Test diagnostic independence (TV, Aitchison, CR) | Formal independence assessment. Structure gate requirement. | Before Coimbra |
| 4 | Present at CoDaWork 2026 Coimbra | Peer presentation. Institution gate. Written feedback. | June 2026 |
| 5 | Incorporate Coimbra feedback, publish GDoF formula | Evidence + Institution gates close. | Post-Coimbra |

**Projected GDoF at CGS-2:**
```
EMBER:      8 × 3 × 3 × 1  =     72   (9 carriers, 3 countries, 3 diagnostics, annual)
Backblaze:  7 × 10 × 3 × 4 =    840   (8 failure types, 10 model families, 3 diagnostics, quarterly)

Total GDoF = 912
CGS = log₁₀(912) = 2.96
```

**What CGS-2 means for any system:** You have shown domain independence. The instrument is not an artefact of its first application. A different system, with different carriers, different temporal structure, and different physics, produces meaningful diagnostics. You are a screwdriver that works on Phillips AND flathead.

---

### CGS-3: Operational Deployment
**"Does the instrument govern a real network?"**

| Gate | Requirement | HUF Status |
|------|-------------|------------|
| **Threshold** | GDoF ≥ 10,000, CGS ≥ 4.0 | ✗ Requires ecological data at scale |
| **Structure** | At least 3 domains OR at least 10 independent sites in one domain. Telescoping coherence operational. SBP design methodology published. Temporal multi-scale monitoring active. Error catalogue complete (all known sources documented with governance actions). | ✗ Telescoping is theory. SBP design for ecology unsolved. |
| **Evidence** | Events detected and localised through the hierarchy. False positive and false negative rates quantified at every SBP level. Q-inquisitor coupling quality measured between at least 3 site pairs. Cross-temporal consistency demonstrated (same event detected at multiple temporal scales). | ✗ No ecological results. |
| **Institution** | Adopted by at least one operational institution for pilot monitoring. Published in a peer-reviewed journal. Independent replication by at least one external team. | ✗ No institutional adoption. |

**The path to CGS-3 — the Ramsar pilot:**

| Step | Action | What It Delivers | Timeline |
|------|--------|-------------------|----------|
| 1 | Collaborate with CoDa ecologist on SBP design | Ecologically meaningful partitions. GAP-04 addressed. | Post-Coimbra, Year 1 |
| 2 | Obtain data for 10 Ramsar wetland sites | Real ecological compositions. GAP-01 tested. | Year 1 |
| 3 | Solve the zero-prevalence problem | 80% zeros handled without artefact. GAP-02 addressed. | Year 1 |
| 4 | Deploy telescoping coherence on pilot network | 10-site hierarchy, multi-level monitoring. ES-01–ES-06 tested. | Year 1–2 |
| 5 | Publish methodology and pilot results | Peer review. Independent scrutiny. | Year 2 |
| 6 | External team replicates on independent sites | Independent validation. Institution gate. | Year 2–3 |

**Projected GDoF at CGS-3 (Ramsar pilot + existing):**
```
EMBER:            72
Backblaze:       840
Ramsar pilot:    49 × 10 × 3 × 4 = 5,880   (50 species avg, 10 sites, 3 diagnostics, 4 temporal scales)

Total GDoF = 6,792
CGS = log₁₀(6,792) = 3.83
```

Note: This reaches the threshold numerically but the structure, evidence, and institution gates require ~2-3 years of real work. The GDoF number is not the bottleneck. The science is.

**What CGS-3 means for any system:** You are operational. Real institutions use your instrument on real systems. Events are detected, localised, and reported. The telescope works. The hierarchy holds. The diagnostics are independently validated. You are not a research prototype. You are infrastructure.

---

### CGS-4: Network Governance
**"Does the instrument govern at planetary scale?"**

| Gate | Requirement | HUF Status |
|------|-------------|------------|
| **Threshold** | GDoF ≥ 1,000,000, CGS ≥ 6.0 | ✗ Requires full Ramsar or equivalent |
| **Structure** | At least 100 independent sites across at least 3 domains. Governance protocol standardised (ISO-level specification or equivalent). Q-inquisitor operational at all inter-site and inter-domain boundaries. Automated anomaly detection with human-in-the-loop escalation. Self-monitoring: the instrument's own composition (diagnostic outputs) treated as a compositional system subject to the same three diagnostics (meta-governance). | ✗ Conceptual only. |
| **Evidence** | Multi-year operational track record. Events detected before institutional awareness in at least 3 documented cases. False alarm rate below defined threshold across entire network. Cross-domain coupling measured and published. Ashby's law formally verified: governance GDoF ≥ system GDoF. | ✗ No operational track record. |
| **Institution** | Adopted by an international body (Ramsar Secretariat, UNEP, ISO, or equivalent). Standard published. Training programme operational. Multiple independent operators certified. Governance instrument itself subject to external audit. | ✗ No institutional contact at this level. |

**The path to CGS-4 — full Ramsar deployment:**

| Step | Action | Timeline |
|------|--------|----------|
| 1 | Scale pilot from 10 to 100 sites | Year 3–4 |
| 2 | Standardise governance protocol | Year 4–5 |
| 3 | Engage Ramsar Secretariat for institutional adoption | Year 3+ |
| 4 | Deploy across 2,500 Ramsar wetlands | Year 5–7 |
| 5 | Add second large-scale domain (energy at national level, or industrial) | Year 5+ |
| 6 | Publish ISO-track governance standard | Year 7+ |
| 7 | Establish external audit framework | Year 7+ |

**Projected GDoF at CGS-4 (full Ramsar + cross-domain):**
```
EMBER (195 countries):    8 × 195 × 3 × 4       =     18,720
Backblaze (full fleet):   7 × 100 × 3 × 4       =      8,400
Ramsar (2,500 sites):   199 × 2,500 × 3 × 4     =  5,970,000
Finance (pilot):         49 × 50 × 3 × 12        =     88,200

Total GDoF ≈ 6,085,320
CGS = log₁₀(6,085,320) = 6.78
```

**What CGS-4 means for any system:** You govern a planetary network. Thousands of sites, multiple domains, multi-year track record. The instrument is not yours anymore — it belongs to the institutions that operate it. The governance is standardised, auditable, and self-monitoring. The Q-inquisitor asks its questions at every boundary. Ashby's law is satisfied. This is the compositional equivalent of Kardashev I: you govern the full complexity of your home domain.

---

### CGS-5: Universal Compositional Standard
**"Does the instrument govern all systems that sum to a whole?"**

| Gate | Requirement | HUF Status |
|------|-------------|------------|
| **Threshold** | GDoF ≥ 100,000,000, CGS ≥ 8.0 | ✗ Requires planetary-resolution monitoring |
| **Structure** | All major compositional domains monitored simultaneously: ecology, energy, finance, industry, health, climate, oceans. Universal SBP design methodology (domain-agnostic partitioning). Cross-domain Q-inquisitor operational at all domain boundaries. The governance instrument is itself governed by a meta-CGS (self-similar governance). | ✗ Conceptual only. |
| **Evidence** | Cross-domain coupling events detected: a climate shift measurably affects ecological compositions, which measurably affects economic compositions, and the instrument traces the chain in real time. Predictive capability demonstrated: compositional precursors identified before institutional events. Full Earth-system GDoF calculated and monitored. | ✗ Pure aspiration. |
| **Institution** | International treaty-level adoption. The governance instrument is referenced in binding international agreements (Paris-level, Ramsar Convention-level). Independent governance body established with rotating international oversight. Open-source, open-data, open-audit. No single entity controls the instrument. | ✗ Pure aspiration. |

**What CGS-5 requires that does not yet exist:**

The jump from CGS-4 to CGS-5 is not primarily technical. It is institutional and philosophical. At CGS-4, you govern ecosystems. At CGS-5, you govern the couplings *between* ecosystems, economies, energy systems, and climate. This requires:

1. **A universal carrier ontology.** Today, "carrier" means species in ecology, fuel type in energy, sector in finance. At CGS-5, these must be mapped into a common compositional framework where cross-domain couplings are measurable. This does not mean they must use the same carriers. It means the Q-inquisitor must be able to ask its coupling question at the interface between ecology and economy using a formally defined protocol.

2. **Planetary-resolution monitoring.** CGS ≥ 8.0 means GDoF ≥ 100 million. The Earth-scale calculation in CMSI.md reached ~10.8M GDoF. To reach 100M requires either finer spatial resolution (100,000+ monitoring sites instead of ~20,000), higher carrier counts (genomic-level biodiversity instead of species-level), or finer temporal resolution (daily instead of quarterly). All three are physically achievable with satellite/sensor/genomic technology. None are governable today.

3. **Self-similar governance.** The instrument at CGS-5 monitors itself using the same three diagnostics it applies to external systems. The meta-CGS: TV distance on the instrument's own output composition (are diagnostic outputs changing?), Aitchison distance on the instrument's performance (are measurement geometries stable?), coherence residual on the governance itself (is the coupling between the instrument and the systems it monitors clean?). Governance all the way down.

**Projected GDoF at CGS-5 (Earth-scale, fine resolution):**
```
Ecology (genomic):     9,999 × 10,000 × 3 × 12   = 3,599,640,000
Energy (national):         8 × 195 × 3 × 12       =        56,160
Finance (markets):        49 × 500 × 3 × 52        =     3,822,000
Industry (facilities): 19 × 100,000 × 3 × 12       =    68,400,000
Health (national):        29 × 195 × 3 × 52         =       882,180
Climate (stations):        8 × 50,000 × 3 × 365     =   438,000,000
Oceans (buoys+satellite): 14 × 100,000 × 3 × 365   = 1,533,000,000

Total GDoF ≈ 5.64 × 10⁹
CGS = log₁₀(5.64 × 10⁹) = 9.75
```

CGS 9.75. Well into Level 5. But note: this requires daily or better temporal resolution across millions of monitoring points. The GDoF is achievable with existing sensor technology. The governance is not. The bottleneck at CGS-5 is not measurement — it is the institutional capacity to govern 5.6 billion independent compositional measurement points simultaneously.

**What CGS-5 means:** You do not just monitor the planet. You monitor the couplings between everything on the planet that sums to a whole. Climate affects ecology affects economy affects energy affects health — and the instrument sees the chain, measures the coupling quality at every interface, and alerts when the coupling degrades. This is the compositional equivalent of Kardashev V: governance of complexity itself, not just governance of systems.

---

## The Realistic Timeline

| Level | When | What Must Happen First | Honest Probability |
|-------|------|------------------------|-------------------|
| **CGS-1** | **Now** | Already satisfied | ✓ Done |
| **CGS-2** | **2026–2027** | Backblaze PoC, CR computation, Coimbra, peer feedback | High — all data and math available today |
| **CGS-3** | **2028–2030** | Ecological data, zero-prevalence solution, Ramsar pilot, external replication | Medium — depends on collaboration |
| **CGS-4** | **2032–2038** | Full Ramsar deployment, ISO-track standard, institutional adoption | Low — depends on institutional will |
| **CGS-5** | **2040+** | Planetary monitoring network, universal carrier ontology, treaty-level adoption | Aspirational — the target on the wall |

---

## The Next Step: From Here to CGS-2

Everything above is architecture. Architecture without action is documentation. The next step is singular:

### Step 1: Compute the coherence residual on EMBER

Why this step and not Backblaze? Because:

- The third diagnostic is the bridge from n=2 to n=3. Without it, the 3^n framework is theoretical.
- EMBER data is already processed. The compositions, TV distances, and Aitchison distances exist.
- The coherence residual formula is defined in THE_THIRD_DIAGNOSTIC.md.
- The result is binary: either CR reveals structure that TV and Aitchison missed, or it doesn't. If it doesn't, the three-diagnostic architecture needs revision before any cross-domain deployment.
- This is a computation, not a collaboration. It depends on no one outside this room.

### Step 2: Run Backblaze proof-of-concept

Why second? Because:

- Cross-domain validation is the CGS-2 structure gate. Without it, you stay at CGS-1 regardless of how many diagnostics you add.
- The data is available in `/BackBlaze/`. It has been available for weeks.
- The compositions are already identified: failure types as proportions of total failures per drive model family.
- This crosses the CGS-2 GDoF threshold and opens the cross-domain evidence gate.

### Step 3: Present at Coimbra with CGS-2 evidence

Walk into the room with:

- Two domains (energy + hardware failure)
- Three diagnostics (TV + Aitchison + CR)
- A governance scale (CGS) with the bullseye defined before the shot
- A deployment path (Ramsar pilot at CGS-3)
- 48+ documented misses and the honesty to count them
- The white flag and the screwdriver

This is not "here is what we built." This is "here is the scale, here is where we are, here is what we don't know, and here is what we need from you to reach the next level."

---

## Connection to Existing Frameworks

| HUF Framework | Role in CGS |
|----------------|-------------|
| GDoF formula | The base quantity — what you count |
| CGS = log₁₀(GDoF) | The scale — how you compare |
| 3^n Confidence Index | The validation axis — how well you've confirmed at your current level |
| Telescoping Coherence | The scaling mechanism — how you move from CGS-3 to CGS-4 without drowning |
| Q-Inquisitor (1/Q) | The boundary diagnostic — what you measure at every coupling point |
| Error Catalogue (E-01–E-19) | The failure inventory — what can reduce your effective n at any CGS level |
| Deployment Gaps (GAP-01–GAP-10) | The barrier register — what blocks movement to the next CGS level |
| Known Unknowns (KU-01–KU-08) | The honesty register — what might invalidate the level you claim |
| Geometric Expansion (Stages 1–7) | The architecture — why each CGS level requires a higher-dimensional structure |

---

## Ashby Verification at Each Level

Ashby's Law: governance variety ≥ system variety.

| Level | System GDoF | Governance Parameters | Ashby Satisfied? |
|-------|-------------|----------------------|-----------------|
| CGS-1 | 48 | 3 diagnostics × 8 balances × 3 sites × 1 scale = 72 | ✓ (72 ≥ 48) |
| CGS-2 | 912 | 3 × (8+7) × (3+10) × 4 = 2,340 | ✓ (2,340 ≥ 912) |
| CGS-3 | 6,792 | 3 × (8+7+49) × (3+10+10) × 4 = 17,664 | ✓ (17,664 ≥ 6,792) |
| CGS-4 | 6,085,320 | 3 × (8+7+199+49) × (195+100+2,500+50) × 4 = 9,488,520 | ✓ (9.5M ≥ 6.1M) |
| CGS-5 | 5.64 × 10⁹ | Scales with monitoring resolution | ✓ by construction (telescoping) |

Ashby is satisfied at every level. The telescoping coherence mechanism is what makes this possible — you do not need all governance parameters active simultaneously, but the instrument must be able to reach any of them on demand.

---

## The Naming Convention for Publication

For scientific communication, the following naming should be used:

| Term | Symbol | Definition | First Reference |
|------|--------|------------|-----------------|
| Governed Degrees of Freedom | GDoF | Σ(C_d × S_d × I_d × T_d) across domains | This document |
| Compositional Governance Scale | CGS | log₁₀(GDoF) | This document |
| CGS Level | CGS-k (k = 1–5) | Governance specification at scale k | This document |
| Confidence Level | n (as in 3^n) | Validation depth at current CGS level | CONFIDENCE_INDEX.md |
| Governance State | (CGS-k, n) | Ordered pair: scale × validation depth | This document |

**HUF today: (CGS-1, n=2).** Two diagnostics on one domain, self-assessed.
**Coimbra target: (CGS-2, n=3).** Three diagnostics on two domains, peer-presented.
**Ramsar pilot: (CGS-3, n=3).** Three diagnostics on three domains with 10 ecological sites, published.
**Full Ramsar: (CGS-4, n=4).** Planetary ecological network with institutional certification.
**Universal: (CGS-5, n=5).** All compositional domains, treaty-level standard.

---

## Honest Caveats

1. **The levels are designed, not derived.** The thresholds (10, 100, 10K, 1M, 100M) are chosen for structural meaning, not measured transition points. The gates (structure, evidence, institution) are judgment calls, not physics. This is n=1 for the scale itself.

2. **The gates are necessary conditions, not sufficient.** Meeting all four gates at a level does not guarantee the instrument works. It guarantees you have done the work required to claim you've tried.

3. **The timeline is optimistic.** CGS-3 in 4 years assumes ecological collaboration materialises. CGS-4 in 12 years assumes institutional will exists. CGS-5 assumes civilisational coordination that does not currently exist. These are targets, not predictions.

4. **GDoF independence assumption is still untested.** Correlated sites reduce effective GDoF. The formula does not yet account for spatial autocorrelation. This is a known unknown carried forward from CMSI.md.

5. **Cross-domain GDoF additivity is assumed, not proven.** Adding ecology GDoF to finance GDoF assumes the domains are independent. They are not — climate affects both. The cross-domain coupling IS the thing CGS-5 claims to measure, but the base quantity assumes separability. This circular dependency is not yet resolved.

---

## One Sentence

The Compositional Governance Scale (CGS = log₁₀(GDoF)) defines five levels from instrument proof (CGS-1, where HUF sits today at GDoF = 48) through cross-domain validation (CGS-2, the Coimbra target), operational deployment (CGS-3, Ramsar pilot), planetary governance (CGS-4, full Ramsar + cross-domain), to universal compositional standard (CGS-5, everything that sums to a whole) — each level gated by structure, evidence, and institutional requirements, not just numbers.

---

*"We start here on step one, the next logical step towards success."*
— Peter Higgins, April 5, 2026

*Step one is the coherence residual. Step two is Backblaze. Step three is Coimbra. The rest of the staircase exists because we drew it before we climbed it.*

---

**This document is at (CGS-1, n=1). The scale is a proposal. The gates are untested. The timeline is aspirational. But the staircase is now drawn, the steps are labelled, and the first step is a computation that depends on no one outside this room.**
