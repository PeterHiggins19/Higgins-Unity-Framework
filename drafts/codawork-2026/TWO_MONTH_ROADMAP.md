# Two-Month Roadmap: April 6 – June 5, 2026

**Purpose:** Identify the weakest points in HUF-GOV and allocate the remaining time before Coimbra to maximum effect.
**Governance state at start:** (CGS-2, n=3). Corpus: 312 files. Three diagnostics operational on two domains.
**Created:** April 5, 2026.

---

## What Has Been Resolved (Since FULL_SYSTEM_ASSESSMENT.xlsx)

Before spending time on anything, acknowledge what moved off the critical list in the last 48 hours:

| Zero | Was | Now | Status |
|------|-----|-----|--------|
| Z-03 Coherence residuals computed | 0 | 74 EMBER + 35 Backblaze = 109 | **RESOLVED** |
| Z-05 Domains validated | 1 (EMBER) | 2 (EMBER + Backblaze) | **RESOLVED** |
| M-01 No real data beyond EMBER | CRITICAL | Backblaze cross-domain done | **PARTIALLY RESOLVED** |
| M-02 CR is pure theory | CRITICAL | Computed, four patterns found | **RESOLVED** |
| Abstract outdated | v2, 17 errors, dual metric | v3, 25 errors, three diagnostics | **RESOLVED** |
| Presentation script outdated | 14 slides, no CR | 16 slides, CR + Backblaze | **RESOLVED** |
| Conference alignment | Inconsistent across artifacts | Three alignment sentences enforced | **RESOLVED** |

These were the right things to do first. What remains is harder.

---

## The Weakness Map: What Can Still Kill You at Coimbra

Ranked by threat severity — highest first. Each item tagged by whether it needs **depth** (go deeper on existing evidence) or **width** (broaden to new evidence or domains).

### TIER 1 — Could Lose the Room in 60 Seconds

**W-1. Diagnostic independence is untested.** [DEPTH]
The 3^n confidence framework claims three independent diagnostics. If someone asks "have you tested whether TV, Aitchison, and CR are correlated?" and the answer is "no," the confidence framework collapses publicly. This is KU-02, Z-04, M-03. It is the single most dangerous untested claim.

*What it takes:* Compute pairwise Spearman and Pearson correlation between TV, Aitchison distance, and mean CR across all 74 EMBER transitions and 35 Backblaze transitions. Report a 3×3 correlation matrix. If r > 0.7 for any pair, the diagnostics are not independent and n must be downgraded. If r < 0.3, independence holds. Between 0.3 and 0.7 is the grey zone — report honestly. This is one afternoon of computation.

*Outcome if done:* Either the independence claim is confirmed (strengthens everything) or it's refuted (forces honest recalibration — still better than being caught at Coimbra). Either way, you know.

**W-2. CR method has no theoretical grounding.** [DEPTH]
The normalised coupling indicator is "proof-of-concept for the proof-of-concept." If a mathematician asks "where does this formula come from?" the answer is "I made it up to see if coupling was detectable." That may be honest, but it invites dismissal.

*What it takes:* Two possible paths. (a) Show that the ad hoc CR correlates with conditional mutual information between SBP branches — this would ground the measure in information theory. (b) Run a simulation: generate compositions with known coupling structure (controlled cross-branch correlation), compute the ad hoc CR, and show it tracks the known coupling. Option (b) is more tractable and more convincing to engineers. Both require a few days of focused computation.

*Outcome if done:* The CR goes from "I measured something" to "I measured the right thing." The Egozcue-Greenacre claim gains teeth.

**W-3. Thresholds are arbitrary.** [DEPTH]
TV > 0.05, Aitchison > 0.5, CR > 0.4. If someone asks "why those numbers?" the current answer is "judgment call." That is fine for a first computation. It is not fine for a conference presentation that puts pattern percentages (31% STRUCTURAL) on a slide.

*What it takes:* Sensitivity analysis. Sweep each threshold through a range (e.g., TV from 0.01 to 0.15 in steps of 0.01, Aitchison from 0.1 to 1.5 in steps of 0.1, CR from 0.1 to 0.8 in steps of 0.05). For each combination, count patterns. Plot stability: if the 31% STRUCTURAL finding persists across a wide threshold range, it is robust. If it flips at small perturbations, it is an artefact. Alternatively: derive thresholds from the data (e.g., 75th percentile of each diagnostic as the "large" threshold). One day of computation, one day of analysis.

*Outcome if done:* Either the patterns are robust (present the stability plot as supplementary evidence) or they are fragile (revise the claims downward, but do so before Coimbra catches you).

**W-4. SBP sensitivity is unanalyzed.** [DEPTH]
The 8-node SBP for EMBER puts Fossil vs Non-Fossil at the root. A different analyst might put Dispatchable vs Intermittent at the root. Different SBP → different balances → different CR. If the 31% STRUCTURAL finding is an artefact of one particular partition, the CR is measuring the analyst's choices, not the energy system.

*What it takes:* Design one alternative SBP for EMBER. The natural alternative: Dispatchable (Coal, Gas, Nuclear, Hydro) vs Intermittent (Solar, Wind) vs Other (Oil, Other Fossil, Other Renewables) at the root. Rerun the CR computation with this SBP. Compare pattern distributions. If both SBPs produce ~30% STRUCTURAL, the finding is robust to partition choice. If one produces 5% and the other 31%, the SBP dependence is a problem that must be disclosed. Two to three days of computation.

*Outcome if done:* Answers the most likely technical objection at Coimbra. "We tested two physically motivated SBPs and the finding holds" is a powerful defence. Or, "we found SBP sensitivity and report it honestly" — still better than not knowing.

### TIER 2 — Could Undermine Credibility Over Coffee

**W-5. Zero human domain expert has reviewed HUF.** [WIDTH]
Six AI systems and one engineer. Zero ecologists. Zero statisticians. Zero CoDa practitioners. This is M-04 and Z-01/Z-02. Coimbra is the first human expert review. Going in completely unreviewed by anyone outside the AI collective is a risk.

*What it takes:* One pre-submission review. Options: (a) email the abstract v3 and COHERENCE_RESIDUAL_RESULTS.md to a CoDa-friendly researcher (Egozcue responded to the first abstract — he is the obvious candidate). (b) Post on a CoDa forum or mailing list asking for feedback. (c) Find an ecologist who works with compositional species data and ask them to read GAP-01 and GAP-04. Even one human perspective changes the collective from n=0 (human review) to n=1. The difference between zero and one is infinite.

*What it takes from Peter:* One email. The documents are ready.

**W-6. No ecological data has ever been processed.** [WIDTH]
EMBER is energy. Backblaze is hardware. Ramsar is ecology. The ecological path is the deployment argument, but zero ecological data has touched the instrument. This is Z-06.

*What it takes:* Source one real ecological dataset. Options: (a) Ramsar Information Service (RIS) — public species lists for Ramsar sites. Not ideal (sparse, categorical), but real. (b) GBIF (Global Biodiversity Information Facility) — occurrence data that can be aggregated to site-level compositions. (c) BirdLife International — waterbird census data, some publicly available. (d) Long Term Ecological Research (LTER) network — multi-year species composition data at fixed sites. Run the three diagnostics on even a single site's species composition time series. Any result is better than zero. Even a negative result ("the diagnostics don't find structure in ecological data") is publishable and honest. One to two weeks for data sourcing and processing.

*Outcome if done:* The talk changes from "we plan to apply this to ecology" to "we have a pilot result from ecological data." That is a different sentence at Coimbra.

**W-7. Backblaze has no human-readable writeup.** [DEPTH]
The JSON exists. COHERENCE_RESIDUAL_RESULTS.md exists for EMBER. There is no BACKBLAZE_RESULTS.md. The collective cannot review what it cannot read. Quick document — half a day.

### TIER 3 — Strategic Weaknesses (Important but Not Urgent for Coimbra)

**W-8. The 3^n framework is at n=0.** [DEPTH]
The confidence index itself has never been tested. Is it a useful framing or an elaborate metaphor? This is M-05 and KU-08. Not critical for Coimbra (it is Second Room material), but important for credibility if someone asks.

**W-9. CGS levels are defined, not derived.** [DEPTH]
The thresholds (10, 100, 10,000, etc.) are chosen for structural meaning, not empirically derived. Not a Coimbra risk (CGS is Second Room), but a long-term credibility issue.

**W-10. Cross-domain additivity assumed, not proven.** [WIDTH]
GDoF sums across domains. But if EMBER and Backblaze share systematic biases (both are industrial data, both have similar temporal resolution), the sum may overstate independence. Need a genuinely different domain (ecological, financial, social) to test whether addition is honest.

---

## The Two-Month Calendar

### Week 1 (April 6–12): Kill the Killers

| Day | Task | Type | Addresses |
|-----|------|------|-----------|
| Mon–Tue | Diagnostic independence test: correlation matrix for TV, Aitchison, CR across EMBER + Backblaze | DEPTH | W-1 |
| Wed | Threshold sensitivity sweep on EMBER | DEPTH | W-3 |
| Thu–Fri | Alternative SBP design + rerun CR on EMBER | DEPTH | W-4 |

**Exit criterion:** By end of Week 1, you know whether the three diagnostics are independent, whether the patterns are robust to thresholds, and whether the SBP matters. These are three binary answers. All three must be known before you present.

### Week 2 (April 13–19): Ground the CR

| Day | Task | Type | Addresses |
|-----|------|------|-----------|
| Mon–Wed | CR simulation study: generate compositions with known coupling, verify CR tracks it | DEPTH | W-2 |
| Thu | Write BACKBLAZE_RESULTS.md | DEPTH | W-7 |
| Fri | Write up Week 1–2 results into a single VALIDATION_REPORT.md | DEPTH | All Tier 1 |

**Exit criterion:** The CR has either a simulation-backed validation or a documented limitation. The Backblaze results are human-readable. A single document summarises what was tested and what was found.

### Week 3 (April 20–26): Seek Width

| Day | Task | Type | Addresses |
|-----|------|------|-----------|
| Mon–Tue | Source ecological dataset (GBIF, LTER, or Ramsar RIS) | WIDTH | W-6 |
| Wed–Thu | Process ecological pilot: three diagnostics on one real site | WIDTH | W-6 |
| Fri | Send pre-submission email to one human reviewer | WIDTH | W-5 |

**Exit criterion:** Either you have a pilot ecological result (even preliminary) or you have documented why ecological data could not be sourced in time. One human has been asked to review.

### Week 4 (April 27 – May 3): Consolidate

| Day | Task | Type | Addresses |
|-----|------|------|-----------|
| Mon–Tue | Integrate all new results into conference artifacts (abstract, script, packet) | DEPTH | Consistency |
| Wed | Update error catalogue if new errors discovered during validation | DEPTH | KU-07 |
| Thu–Fri | Collective review: distribute VALIDATION_REPORT.md to all AI reviewers | DEPTH | KU-06 |

**Exit criterion:** Conference artifacts reflect actual evidence. Any new errors are catalogued. The collective has reviewed the validation work.

### Weeks 5–6 (May 4–17): Depth or Width — Choose Based on Results

**If diagnostic independence holds and patterns are robust:**
Focus on WIDTH. Add a third domain. Financial data (GDP compositions by sector) is publicly available from World Bank. Process one country's sectoral GDP composition over 20+ years. If the same pattern families appear in energy, hardware, AND economics, domain independence is triple-confirmed. CGS-2 is unassailable.

**If diagnostic independence is weak or patterns are fragile:**
Focus on DEPTH. Redesign the CR to address the correlation. Consider normalising each diagnostic to remove shared variance before pattern classification. Rerun everything. The honest path: downgrade claims and present the limitation transparently. A calibration study that finds its own limitations is more credible than one that ignores them.

**If ecological pilot succeeded:**
Expand. Process 3–5 ecological sites. Design an ecological SBP template. Write a short ECOLOGICAL_PILOT_RESULTS.md. This single document may be the most impactful thing at Coimbra — it proves the instrument works beyond industrial data.

**If ecological pilot failed or data could not be sourced:**
Document why. "We attempted ecological validation and encountered [specific obstacles]" is a legitimate conference contribution. It demonstrates rigour and invites collaboration — which is the Conference Core Stack's "ask."

### Weeks 7–8 (May 18–June 5): Conference Preparation

| Task | Priority |
|------|----------|
| Final consistency pass across all artifacts (repeat the three-sentence audit) | CRITICAL |
| Rehearse presentation (time it, refine pacing, practice slide 10 CR explanation) | CRITICAL |
| Prepare for top 5 adversarial questions (update ADVERSARIAL_PANEL.md with new results) | HIGH |
| Print Conference Core Stack as pocket reference | HIGH |
| Prepare 2-page handout for interested researchers (abstract v3 + CR results summary) | HIGH |
| Update analyzer HTML to show three diagnostics (currently shows dual metric) | MODERATE |
| Pack poster if presenting (update POSTER_LAYOUT.md with CR + Backblaze) | MODERATE |
| Final collective distribution (CRPT-009 or CRPT-010 with all validation results) | MODERATE |

---

## The Depth vs Width Decision Framework

The fundamental tension:

**Depth** means going deeper on EMBER and Backblaze — testing independence, calibrating thresholds, validating the CR method, running sensitivity analyses. Depth makes existing claims bulletproof. Depth answers the mathematician who asks "have you tested this?"

**Width** means adding new domains — ecological data, financial data, a third physical system. Width demonstrates universality. Width answers the skeptic who says "this might just work on energy data."

**The HUF-GOV principle resolves the tension:** HUF-GOV is open-loop. It reads the state. It does not act on it. The governance question is: which investment yields the highest information per hour?

**Weeks 1–2 are non-negotiable depth.** The independence test, threshold sensitivity, and SBP sensitivity are existential. They cannot be skipped regardless of how attractive width looks. If the independence test fails, width is meaningless — you are measuring the same thing three times.

**Weeks 3–4 are strategic width.** Once depth is secure, one ecological pilot and one human review are the highest-value width investments. They change the narrative from "energy and hardware" to "energy, hardware, and a first look at ecology."

**Weeks 5–6 are results-dependent.** The calendar forks based on what Weeks 1–4 reveal. This is the HUF-GOV doctrine applied to its own development: measure first, then decide.

**Weeks 7–8 are presentation polish.** No new science. Only packaging.

---

## The Honest Assessment of What Is Achievable

| Item | Achievable in 2 months? | Confidence |
|------|------------------------|------------|
| Diagnostic independence test | Yes — computation only | HIGH |
| Threshold sensitivity analysis | Yes — computation only | HIGH |
| SBP sensitivity (one alternative) | Yes — computation only | HIGH |
| CR simulation validation | Probably — requires careful design | MEDIUM |
| Backblaze writeup | Yes — documentation only | HIGH |
| One ecological pilot dataset | Maybe — depends on data availability | MEDIUM |
| One human expert review | Maybe — depends on responsiveness | LOW-MEDIUM |
| Third domain (financial/GDP) | Maybe — if Weeks 1–4 go well | MEDIUM |
| Full CR formalisation (information theory) | Unlikely in 2 months | LOW |
| Ecological SBP design template | Unlikely without ecologist input | LOW |
| Formal peer review pre-submission | Unlikely in timeline | LOW |

The realistic target: arrive at Coimbra with the independence test done, the thresholds calibrated, the SBP sensitivity analysed, the CR simulation-validated, and one ecological pilot attempted. That changes the talk from "we computed this once" to "we tested our own instrument and here is what survived."

---

## What Not to Spend Time On

These are tempting but wrong for the next two months:

1. **More documentation.** 312 files is enough. The corpus needs validation, not expansion. Every new document that does not contain empirical results is overhead.

2. **CGS refinement.** The levels are fine. Do not re-derive thresholds or add new governance gates. CGS is Second Room material. Spend zero time on it until after Coimbra.

3. **Peterson letter follow-up.** Off Table. The science must land first. If Coimbra goes well, the Peterson conversation changes entirely. If Coimbra goes poorly, the Peterson conversation is premature.

4. **Analyzer UI improvements.** The analyzer works. It demonstrates the concept. Do not polish the interface when the mathematics needs validation.

5. **New error sources.** The catalogue has 25 entries. Do not add more unless validation genuinely discovers one. The time for cataloguing is over. The time for testing is now.

6. **Scaling/telescoping implementation.** ES-01 through ES-06 are correctly identified. Implementation is for post-Coimbra. Do not build what has not been validated.

---

## One Sentence

The next two months are not about building more — they are about testing what has already been built, starting with the three things that could end the conversation at Coimbra before it begins: diagnostic independence, threshold robustness, and SBP sensitivity.

---

*Generated April 5, 2026. Governance state: (CGS-2, n=3). Next review: end of Week 2 (April 19).*
*PeterHiggins@RogueWaveAudio.com*
