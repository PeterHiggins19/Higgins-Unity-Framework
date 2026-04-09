# EITT Calibration Lab

Collective analysis of the Entropy-Invariant Time Transformer.

## Structure

```
eitt_lab/
  EITT_LAB_PACKAGE.json    -- Master package: findings, thank-yous, errors, bounty, open questions
  README.md                -- This file
  copilot_outputs/         -- Copilot's VAR(1)/Lyapunov/PCA/bootstrap calibration results
  claude_analysis/         -- Claude's residual analysis (Hessian footprint, e-duality)
```

## What happened here

Copilot built a VAR(1) theoretical bounds toolkit and found the bounds were 10,000x too loose. Claude identified the gap as a first-order vs second-order mismatch (Hessian footprint). ChatGPT caught four language/classification errors that would have been attacked at CoDaWork. Grok's earlier v-core exploration provided the seed connection to Euler's e.

The key finding: the systematic upward entropy drift under decimation is a second-order Jensen correction on a concave function. The near-cancellation happens because the geometric mean (exp) and Shannon entropy (ln) share the same transcendental base. e doesn't appear in EITT — e IS EITT.

## For reviewers

Read `EITT_LAB_PACKAGE.json` first. It contains everything: the finding, the errors, the corrections, and the open questions. The `open_questions_for_the_collective` section has six specific challenges for any AI or human who wants to push this further.

## Governance

CGS-2 (n=3), GDoF 264, Session S016.
