# HUF-CLS — Closed-Loop Composition Control System

**The actuator that could act.**

HUF-CLS is the closed-loop counterpart to HUF-GOV. Where HUF-GOV reads — computing carrier proportions, structural drift, and concentration metrics without taking action — HUF-CLS contains the architecture for acting on those readings: sigmoid mapping functions, contraction parameters, phase-lock mechanisms, and feedback control loops.

HUF-CLS is the parachute-pulling arm. HUF-GOV tells you the canopy is collapsing. HUF-CLS could pull the cord.

---

## Why This Is Public

This system was originally held behind engineered breakers. The decision to publish it under the same MIT license as HUF-GOV was made on March 29, 2026.

The reasoning: suppression does not prevent misuse — it prevents understanding. If someone will close the loop, it is better that the architecture, the failure modes, and the governance principles are public knowledge than that they are reinvented without safeguards.

The instrument reads. The human decides. That principle does not change because the formulas are visible. It changes when humans stop reading.

---

## Contents

**`architecture/`** — CL-01 through CL-05 control loop stack. The full closed-loop architecture from basic feedback (CL-01) through multi-AI routing (CL-05).

**`formulas/`** — Sigmoid actuator function, contraction parameter (K_eff fill), and amplifier derivations. The mathematical machinery that maps composition readings to control actions.

**`calibration/`** — CL-05 calibration study and sensitivity analysis. How the control parameters behave under perturbation.

**`routing/`** — Multi-AI routing assessments. How CL-05 was evaluated across five AI systems for integration readiness.

---

## The Governance Principle

HUF-CLS without HUF-GOV's open-loop doctrine is dangerous. The control loops in this directory are designed to be operated by humans who have read the governance documentation in `../huf-gov/governance/`. The kill test (`../huf-gov/governance/kill-test.json`) documents nineteen failure modes — several of which are specific to closed-loop operation.

Do not close the loop without reading the failure modes first.

---

## License

MIT License. Same terms as all HUF components. See [LICENSE](../LICENSE).
