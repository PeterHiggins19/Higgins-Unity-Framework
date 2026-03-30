# Higgins Unity Framework (HUF)

**Composition Monitoring as a Fourth Category of System Observation**

Most institutions monitor the systems they are responsible for using three categories of information: magnitude (how much), identity (which), and trend (what direction). The fourth category — composition — asks how the internal parts are arranged relative to each other, regardless of total volume. When any system's elements are normalized so that proportions sum to one, the resulting structure lives on a mathematical simplex, and structural changes on that simplex carry lead-time information that the first three categories cannot access.

The mathematics is not new. Compositional data analysis on the simplex was formalized by John Aitchison in 1982 (Journal of the Royal Statistical Society). The measurement taxonomy was formalized by Stanley Smith Stevens at Harvard in 1946. What is new is the application: treating compositional structure as a primary monitoring observable rather than a post-hoc statistical correction.

This framework was developed over five months by Peter Higgins, with five AI systems (Claude, ChatGPT, Gemini, Copilot, Grok) contributing under human direction. The operator governed the process. The AI systems were the instruments. The loop stayed open.

---

## Repository Structure

### `huf-gov/` — Open-Loop Composition Monitoring Instrument

The instrument that reads. It computes carrier proportions, structural drift velocity, effective complexity, and concentration metrics. It offers no recommendations. It takes no actions. It closes no loops.

- **`science/`** — Formal taxonomy (MONITOR-001), paper skeleton, teaching materials
- **`evidence/`** — Case studies across six domains with real-world data
- **`governance/`** — Safe operations doctrine, human operator manual, kill test (19 failure modes)
- **`tools/`** — Working spectrum analyzer, Ramsar demo wrapper

### `huf-cls/` — Closed-Loop Composition Control System

The actuator that could act. It includes a sigmoid mapping function, contraction parameter, phase-lock mechanism, and feedback architecture. It is the parachute-pulling arm. It is published here under the same MIT license as HUF-GOV because the author concluded that suppression is not governance — understanding is.

- **`architecture/`** — CL-01 through CL-05 control loop stack
- **`formulas/`** — Sigmoid actuator, contraction parameter, Keff_fill derivations
- **`calibration/`** — CL-05 calibration study, sensitivity analysis
- **`routing/`** — Multi-AI routing assessments and integration work

### `context-books/` — Audience-Specific Explanations

Four editions of the core theory, each written for a different audience: general, engineering, physics, sciences. Same content, different entry points.

### `math-books/` — Formal Mathematics Reference

Four editions of the mathematical foundations. 42 numbered items across Areas A–F with full proofs. Audience-specific editions available.

### `process/` — How We Got Here

Collective review traces, session ledgers, governance documents. Included for transparency. This is the process record of five AI systems and one human operator building a framework over five months.

### `reference/` — Deep Technical Material

Technical notes, formal proofs, code appendix, wiki documentation, and all machine-readable JSON specifications.

### `drafts/` — Work in Progress

Submission papers (pre-validation), the Human-AI Accord (untested governance proposal). Included because the work is ours and hiding drafts is not transparency.

---

## Where to Start

1. **If you have five minutes:** Read `huf-gov/governance/HANDOFF-001.docx` — the coldest, most external-ready summary of what this is.

2. **If you have thirty minutes:** Read the teaching progression in `huf-gov/science/` — fuel gauge to rocket equation in four levels.

3. **If you want the evidence:** Start with `huf-gov/evidence/case-studies/energy/` (Germany, EMBER dataset, p = 0.0016) and `huf-gov/evidence/case-studies/ramsar/` (wetland habitat composition).

4. **If you want the math:** The formal taxonomy is in `huf-gov/science/MONITOR-001.json`. The proofs are in `math-books/`.

5. **If you want to break it:** Read `huf-gov/governance/kill-test.json` — nineteen documented failure modes, the things this framework cannot do, must not do, and will fail at.

---

## The Four Monitoring Categories

| Category | Name | Question | Status |
|----------|------|----------|--------|
| MC-1 | Magnitude Monitoring | How much? | Universally deployed |
| MC-2 | Identity Monitoring | Who or what? | Universally deployed |
| MC-3 | Trend Monitoring | Which direction? | Universally deployed |
| MC-4 | Composition Monitoring | What is the internal balance? | Diagnostically invisible in standard practice |

---

## Key Evidence

- **Electricity generation (EMBER):** Germany — structural concentration p = 0.0016 behind stable total generation
- **GDP composition (World Bank):** Japan p = 0.0098, China p = 0.0196 — internal drift behind stable headline GDP
- **Scale invariance:** 35 million tests, 10 to 10 million elements, zero violations, 5.23 sigma
- **Ecosystem monitoring (Ramsar template):** Structural thinning of habitat diversity behind stable total-area figures

---

## On HUF-CLS Being Public

The closed-loop system was originally held behind engineered breakers. The decision to publish it under MIT license was made on March 29, 2026. The reasoning: suppression does not prevent misuse — it prevents understanding. If someone will close the loop, it is better that the architecture, the failure modes, and the governance principles are public knowledge than that they are reinvented without them.

The instrument reads. The human decides. That principle does not change because the formulas are visible. It changes when humans stop reading.

---

## Contact

Peter Higgins
Rogue Wave Audio
Markham, Ontario, Canada
PeterHiggins@RogueWaveAudio.com

---

## License

MIT License. See [LICENSE](LICENSE).

Developed with Claude (Anthropic), ChatGPT (OpenAI), Gemini (Google), Copilot (Microsoft), and Grok (xAI) under human direction. March 2026.
