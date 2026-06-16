# HUF‑Gov Doctrine — Ratio Blindness ("See or Remain Blind")

*A HUF‑Gov governance doctrine and the motivating principle of **MC‑4**. 2026‑06‑11. Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. Companion to [`CARRIER_FILTER_DOCTRINE.md`](CARRIER_FILTER_DOCTRINE.md), [`HUF_GOVERNANCE_CHARTER.md`](HUF_GOVERNANCE_CHARTER.md), and the instrument note [`../discoveries/instruments/MC4_COMPOSITION_MONITORING.md`](../discoveries/instruments/MC4_COMPOSITION_MONITORING.md). Claim‑tiered.*

---

## The doctrine in one line

> **Monitoring has four categories. Most instruments use three. The fourth — composition — is where the ratios live, and ignoring it is *Ratio Blindness*: a standing, undiagnosed cost. Once the ratios are seen, they cannot be unseen.**

## The four monitoring categories (and why "1/4")

HUF names four categories of monitoring (see `MC4_COMPOSITION_MONITORING.md`):

| | Category | Answers | Sees ratios? |
|---|---|---|---|
| **MC‑1** | Magnitude | *how much?* | no |
| **MC‑2** | Identity | *what is it?* | no |
| **MC‑3** | Trend | *where is it going?* | no |
| **MC‑4** | **Composition** | *when did the composition change, which carrier moved, and was it real or noise?* | **yes** |

Conventional instruments implement MC‑1…MC‑3 and stop. They watch levels, identities, and trends — all **magnitude** views — and are structurally blind to the **compositional** view. That is the basis of the **cost factor of ¼**: of the four monitoring categories, the entire fourth one goes undiagnosed. **Ratio Blindness ≈ one quarter of the available monitoring knowledge left on the table, by construction.** This is the **MC‑4** corollary of HUF‑Gov.

**Honest tiering of the ¼.** The ¼ is a *principled category‑count heuristic* — one of four named monitoring categories is entirely absent — not a measured universal constant. The *magnitude* of what MC‑4 recovers in any given system is domain‑dependent: sometimes the compositional view merely confirms the magnitude view (agreement = robustness); sometimes it recovers an effect the magnitude view scored as zero. The doctrine's claim is structural (a whole category is missing), not that exactly 25% of every signal is always lost.

## Why "once seen, ratios cannot be ignored"

Compositional information is **subcompositionally coherent, scale‑invariant, and permutation‑invariant** (the Aitchison properties). A magnitude monitor can sit entirely inside its normal bands while the *ratios* rotate — the classic deceptive drift: *one curve lies, two curves diagnose.* Once an MC‑4 read is placed beside the magnitude read, the gap is visible and not honestly deniable: the composition either moved or it did not, and the receipt (a content hash) says which. Seeing is irreversible; that is the doctrine's force.

## Evidence that Ratio Blindness is real (not rhetorical)

- **COPD clinical trial (Narayana & Chotirmall, CoDaWork 2026).** Standard MC‑1/MC‑3 methods — diversity indices, Bray‑Curtis dissimilarity, PERMANOVA — found **no** doxycycline effect (p > 0.05). The compositional (MC‑4) view — inverse perturbation, Aitchison norm — **unmasked** significant, time‑structured treatment effects. Here the magnitude view diagnosed ≈ 0 of a real effect: total Ratio Blindness on that question.
- **Hs general gas‑composition study (this corpus, `Hs/industrial-instruments/gas-composition-study/`).** On a closed‑loop O2/CO2/N2 series, **40 of 60 timesteps had every single‑channel magnitude alarm green** while the composition was demonstrably moving; in a deliberately sub‑threshold window the MC‑4 motion (Aitchison step) ran **≈ 2.5× the nominal baseline** with all single‑channel alarms still green, and Hs named the driving carrier at each step. Magnitude monitoring was blind; composition monitoring was not.

## Governance implications (HUF‑Gov)

- **See or remain blind is a choice, and HUF offers the seeing.** The instrument that reads MC‑4 (Hˢ / CN‑TT) exists, is deterministic, and is hash‑chained. Whether a given operator or field chooses to read the fourth category is now a decision, not a limitation.
- **Carrier‑filter governs disclosure.** What is published vs held is decided per [`CARRIER_FILTER_DOCTRINE.md`](CARRIER_FILTER_DOCTRINE.md). Publishing a compositional analysis on *public* data makes the cost of Ratio Blindness *publicly* visible — a transparency consequence, stated plainly and without coercion: once the public can see what magnitude monitoring misses, the choice to remain blind carries a now‑visible cost. We extend the seeing as assistance; we do not weaponise it.
- **Falsifiable, like MC‑4.** The MC‑4 claim carries four defeat paths (prior‑art / metric / case / category — see the instrument note). Ratio Blindness inherits that discipline: if a magnitude‑only method can be shown to recover everything MC‑4 recovers on a given problem, the cost factor for that problem is zero, and we say so.

## Claim tiers
- **Tier 1 (verified):** MC‑4 reads composition deterministically with a hash; the COPD and gas‑study instances above are real (cited/computed).
- **Tier 2 (sound):** the four‑category framing; the ¼ as a category‑count heuristic; "once seen, cannot be ignored" as a property of Aitchison coherence.
- **Tier 3 (to earn / doctrine):** any claim that the cost is *exactly* ¼ in a specific domain; that is measured per case, never assumed.

*The percentages can lie. The simplex cannot. Three categories measure magnitude; the fourth reads the ratios. See, or remain blind.*
