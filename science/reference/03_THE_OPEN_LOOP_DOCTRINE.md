# The Open-Loop Doctrine

**DocCode:** REF-003 (derived from LOOP-001)  
**Source:** `huf-gov/governance/LOOP-001-open-loop-doctrine.json`  
**Status:** State of record — not negotiable  

---

## The Skydiver Principle

HUF-GOV is the altimeter. It is NOT the hand pushing you out of the plane. The skydiver jumps on their own volition.

**Formal version:** HUF-GOV observes, measures, computes, and reports. It does NOT decide, act, recommend action, trigger responses, or automate downstream behaviour. The human operator receives the instrument readings and decides what to do. The loop stays open.

**One line:** The instrument reads. The human decides. The loop stays open.

---

## Why Open Loop

**Technical reason:** Closing the loop requires a controller model — assumptions about "correct" composition, "right" responses, thresholds. These are domain-specific, context-dependent, politically loaded. No universal controller exists.

**Governance reason:** Closed-loop removes human agency. If the analyser detects drift and automatically triggers alerts, who decided the threshold? Who decided drift meant degradation? That is not governance — it is automation wearing governance costume.

**Safety reason:** The Montreal machine did not decide to hurt anyone — a human bypassed safety. But if given authority to act autonomously, it might shut down during normal operation or fail to during abnormal operation. Passive failure (shear bolt) works because it does not decide.

**Practical reason:** Different domains need different responses to the same reading. K_eff decline in electricity = policy failure (action needed). K_eff decline in a wetland = seasonal variation (no action). K_eff decline in finance = opportunity. The instrument cannot know the context. Only the human operator can decide.

**Peter's reason:** The human is not a bug — the human IS the system.

---

## What Closing the Loop Looks Like (Violations)

| Violation | Why Wrong | Correct Approach |
|-----------|----------|-----------------|
| Automatic alerts triggered by drift thresholds | Who set the threshold? What if drift is normal in this context? | Analyser displays drift; operator decides to escalate |
| Recommended actions appended to outputs | Recommendations are control signals disguised as suggestions | Analyser reports measurements; operator decides response |
| Integration with automated trading/regulatory/policy systems | Instrument becomes controller; measurement becomes action; human removed | Analyser is standalone observation instrument; feeds human judgment, not automated pipelines |
| Predictive thresholds (tipping point warnings) | Prediction is CLS territory; requires "should be" model; GOV observes "what is" | Complexity trace shows trajectory; operator recognises pattern and assesses |
| Sensitivity knobs adjusting "significance" | Adjusting significance is governance decision, not measurement decision | Instrument reports raw values; significance thresholds are operator's domain |

---

## The Engineering Paradox

HUF began as a closed-loop BTL loudspeaker control system. Peter deliberately opened it — opposite of normal engineering evolution (open → closed). In governance, closing removes the human.

HUF-GOV is not performance optimisation — it is a governance instrument.

HUF-CLS (closed-loop) exists for domains where closing is appropriate (BTL loudspeaker control, process automation). The boundary between GOV and CLS is not a design choice — it is an ontological requirement.

---

## The Skydiver Test

Before adding any feature to the GOV analyser, ask:

**Does this push the skydiver, or show the skydiver the altimeter?**

If push → CLS territory.  
If show → GOV territory.

---

## The Boundary

Not negotiable. HUF-CLS for performance. HUF-GOV for observation. The two architectures share mathematics but serve fundamentally different purposes. Mixing them is the single most dangerous tendency in the project.

---

*Definitive source: `huf-gov/governance/LOOP-001-open-loop-doctrine.json`*  
*Peter Higgins | Rogue Wave Audio | PeterHiggins@RogueWaveAudio.com*
