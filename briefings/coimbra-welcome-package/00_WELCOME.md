# 00 — Welcome

## Who this is for

- Researchers in compositional data analysis looking for a monitoring tool that respects Aitchison geometry.
- Domain scientists (energy, ecology, hydrology, oceanography, chemistry, finance) with time-indexed compositional data and suspicion that existing tools are missing something.
- Methodologists interested in the shape/magnitude decomposition and its implications for statistical testing on the simplex.
- Engineers who build monitoring instruments and care about the discipline of inert measurement.
- Anyone arriving at CoDaWork 2026 in Coimbra who hears "EITT" and wants to know what that is.

## What HUF is

A working tool for monitoring structural drift in compositional time series. The instrument reads. The human interprets. The loop stays open.

Three diagnostics are computed at each time step: total variation distance on raw proportions, Aitchison distance on log-ratio coordinates, and a coherence residual measuring cross-branch coupling in sequential binary partition decompositions. Metric agreement is treated as robustness; metric disagreement is treated as diagnostic information, not error.

EITT (Entropy-Invariant Time Transformer) is the tool's time-series extension. Under stated conditions, Shannon entropy of compositional data is near-invariant under geometric-mean block decimation. Four empirical proofs anchor the claim:

| Domain | Compression | Entropy variation | Source |
|---|---|---|---|
| European daily wholesale prices | 341:1 | 0.18% | `ai-refresh/HUF_FAST_REFRESH.json` proof_1 |
| EMBER monthly generation (6 countries) | 12:1 | 1.02% mean (all < 2%) | proof_2 |
| NGFS Phase 4 scenarios (35 pathways) | 5-year geometric | 1.8% vs 14.2% arithmetic | proof_3 |
| CheMixHub chemical mixtures (500k points) | multi-lens | 54–82% interior pass | proof_4 |

## What HUF-GOV is, precisely

> **HUF-GOV is a tool that produces a verifiably clean usable output to a known degree of certainty; the diagnostic of the output is open to interpretation by expert decision and open to modification by expert judgment.**
> — Peter Higgins, 2026-04-15

Five clauses. Each does work:

1. **A tool.** Not a framework, theory, or method. Built, verified, used. The noun matters.
2. **Verifiably clean usable output.** Unambiguous, actionable, checkable without trust.
3. **Known degree of certainty.** The Hessian bound quantifies it. The safety document says where it holds.
4. **Diagnostic open to interpretation by expert decision.** The tool reports; you interpret. That's not a weakness, that's scope.
5. **Open to modification by expert judgment.** The tool evolves under use. Find its limits, contribute corrections.

Full unpacking in `science/governance/HUF_GOV_CANONICAL_DEFINITION.md`.

## Who built it

Peter Higgins, Rogue Wave Audio, Markham, Ontario, Canada. Independent researcher. Thirty-five years at the industrial machine interface — Dage X-ray, Fuji placement, Electrovert wave solder, AOI, PLCs, first-generation industrial AI. The framework grew out of a basement lab (the BTL, Binaural Test Lab) built for loudspeaker diffraction measurement.

The mathematics was discovered empirically in acoustic engineering between 2024 and 2025 before the CoDa community's vocabulary was applied to it. The screwdriver and the math book met in April 2026. This welcome package is one of the fruits of that meeting.

The Rogue Wave Audio repo (engineering home) and the Higgins Unity Framework repo (scientific framework home) are siblings. Both are open-source. Both link reciprocally. See [`MASTER_LINEAGE.json`](../../ai-refresh/MASTER_LINEAGE.json) for the full arc.

## Who helps if you get stuck

Five AI systems have worked on the framework throughout its development and are prepared to help new users get started. Each has a different strength. See [`04_MEET_THE_COLLECTIVE.md`](04_MEET_THE_COLLECTIVE.md) for who they are and how to engage them.

## What you get for reading further

The rest of this welcome package will tell you, in order:

- Where the tool succeeds and where it fails (no hiding)
- What's stable, what needs verification, what's a possibility worth investigating
- Which domains are ready to use today
- Who your allies are
- What adopting the tool buys you, and what community-wide standardization enables

## The first step

Read `01_SUCCESS_AND_FAILURE.md`. Then decide whether to keep going. The tool is not for everyone, and the welcome package is designed to help you determine fit before you invest further.
