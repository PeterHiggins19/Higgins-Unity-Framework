# EITT — the place it holds: a key point of contact with divided influence

*Status note, 2026-06-11. Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. Honest-broker; claim tiers marked. This document fixes EITT's role within the greater system of HUF after the maturation of the deterministic instrument (CN-TT v4). It does not retract the finding; it places it.*

---

## 1 · What EITT is (unchanged)

**EITT — Entropy-Invariant Time Transformer.** Canonical name preserved (drift guard: never "Ternary Transform," never "Temporal Transform"). The finding, in one sentence: *Shannon entropy of compositional time series is empirically near-invariant under geometric-mean decimation across temporal resolutions.* Measured at **0.18% variation over a 341:1 compression**, and confirmed across energy (EMBER), chemistry (≈500,000 points), hardware reliability, climate scenarios, and 40,666 igneous rocks.

That measurement is real and stands. What has changed is not the result but its **place** in the system.

## 2 · The divided influence

EITT's influence within HUF is genuinely **divided** — large in some directions, small in others — and naming that division honestly is the point of this document.

**Engine influence — minor.** In the live deterministic instrument (CN-TT v4) EITT is implemented as `eitt_bench_test(...)` — an entropy gate (default 5%) over a block-size sweep `M = 2…128`. It is *one diagnostic among many* (the navigation family, helmsman, attractor fit, depth tower, the SS-CCC-LLL codes). The instrument's determinism, closure, tiling, and hash-receipts do **not** depend on EITT being true. Remove it and the engine still runs, bit-for-bit. As a *capability*, EITT is a test tool, and the code already says so by calling it a bench test.

**Conceptual influence — major.** EITT is the **temporal face of the framework's central thesis**: that a composition's timescale is *intrinsic*, not imposed. It is the time-domain twin of the acoustic ground state — where DADC says "the corner frequency is forced by wavelength over dimension," EITT says "the entropy survives decimation because the timescale was intrinsic to begin with." Drop the engine machinery; this statement remains half the spine of the framework's certainty argument. (See `THE_GROUND_STATE.md` in the RWA repo and step 6 of `ARC_OF_DISCOVERY.md`.)

**Community influence — major.** EITT is HUF's **primary point of contact with the compositional-data-analysis community**. It is offered as a *falsifiable, shared open problem*: the invariance is measured but **not proven**, and the honest invitation is "*can it be derived from Aitchison geometry?*" That question is a peer's question, not a claim — which is why it is the right thing to hand to Egozcue, Hron, and Pawlowsky-Glahn, and the natural bridge to applied members (portfolio, microbiome, geochemistry). It is the "gift to CoDa": the place where HUF meets the field on equal terms.

## 3 · The honest qualifier (why the influence is divided, not uniform)

The chemistry decomposition is the reason the word is **divided** and not simply "major." Roughly **half** of the observed invariance is ordinary **Aitchison geometry** (already proven, not mysterious) and roughly half is **temporal autocorrelation**. So the genuinely novel, genuinely unproven part is smaller than the original headline implied. Claim tiers:

- The invariance **as a measurement**: Tier 1 (observed, reproduced across domains).
- The invariance **as a theorem** (a derivation of *why*): Tier 3 — to earn.

This is the discipline working as intended: the measurement is kept; the mystery is sized honestly; the open part is handed out as a problem, not asserted as a proof.

## 4 · The name is earned — windings, phase wraps, and "Explain It To Them"

The name is not loose, and an earlier draft that called "Transformer" a weak word was wrong. **"Transformer" is a precise acoustic-measurement metaphor.** A transformer is built of *windings* — turns. In FFT group-phase analysis (Smaart v9), phase **wraps**: against a fixed delay it accumulates with frequency and rolls over, 360° → 0°, again and again, and you recover true phase/time by **counting the wraps**. Each wrap is a turn — a winding. EITT's "Transformer" is exactly that: a **time/phase counter that wraps and flips**, the thing that steps structure across temporal resolutions — which is what geometric-mean decimation does to a compositional series. The decimation *is* the wrap-counting, in the time domain.

The acronym carries a second, human meaning by design. **EITT = "Explain It To Them"** — the instant understanding is unleashed (Khan; Ricardo Montalbán; the same click when a collaborator finally *gets it*). At the moment it was minted the name fit on both axes at once: the engineering (a phase-wrap transformer) and the aha (the explanation landing).

So the name **stays**. The only real liability — an outside reader meeting "Transformer" and thinking of machine learning — is fixed not by renaming but by **documenting the etymology** (this section), turning an apparent borrow back into the earned engineering term it always was. The drift guard stays in force: EITT is *Entropy-Invariant Time Transformer*, never "Ternary." Operationally the engine still names the diagnostic `eitt_bench_test`; conceptually the full name now reads correctly, because its origin is on the record. *Lose nothing — including the reason for the name.*

## 5 · Where it sits in the discipline

Within Compositional Constraint Diagnostics (CCD), EITT remains "the first instrument" — but understood precisely: it is the **contact instrument**, the one HUF hands the community, not the **load-bearing engine** (that is CN-TT v4). First in order of introduction; not first in structural weight.

## 6 · One line

> EITT is a key point of contact with divided influence: minor as an engine capability (`eitt_bench_test`), major as the temporal statement of the framework's thesis and as the falsifiable open problem that joins HUF to the CoDa community. The finding stands; its place is now named.

---

**Cross-references:** `HUF/README.md` (front-page framing) · `ai-refresh/HUF_FAST_REFRESH.json` (`canonical_names.EITT.role_2026-06`) · `ARC_OF_DISCOVERY.md` step 6 · RWA `THE_GROUND_STATE.md` (the frequency-domain twin) · `science/methodology/CONFIDENCE_INDEX.md` · engine `Hˢ HCI-CNTT/engine/diagnostics.py` (`eitt_bench_test`).
