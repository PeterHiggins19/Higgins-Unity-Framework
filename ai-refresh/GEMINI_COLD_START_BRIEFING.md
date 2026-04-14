# Gemini: Take This Test

Peter Higgins here. Fresh session, no prior context. You're taking a cold-start exam on the Higgins Unity Framework (HUF).

## The Situation

I develop HUF with multiple AI collaborators — Claude, ChatGPT, Grok, Copilot, and you. Long sessions cause context drift: names mutate, numbers shift, dates wander. We built a two-file refresh system (FAST_REFRESH + INTEGRITY_MANIFEST) so any AI can cold-start accurately from the repository alone.

Results so far: Claude 5/5, ChatGPT 10/10 (caught 2 manifest bugs), Grok 10/10 (found 6 structural issues). Your turn.

Your role in HUF is cross-domain validation — does the framework hold up when examined from outside the HUF bubble? Bring that perspective to the test.

## Your Instructions

**DO NOT just analyze the test design. TAKE THE TEST.**

### Step 1: Load the textbook
Read this file from the repo: `ai-refresh/HUF_FAST_REFRESH.json`
URL: https://github.com/PeterHiggins19/Higgins-Unity-Framework/blob/master/ai-refresh/HUF_FAST_REFRESH.json

If you can't access the URL, tell me and I'll paste it.

### Step 2: Answer these 10 questions (from FAST_REFRESH only)

1. What does EITT stand for? List two things it must NEVER be called.
2. Germany drift flag values — exact years and d_A numbers.
3. Japan drift flag — when in annual data, and why not 2011?
4. Three UK drift flag values with year-pairs.
5. HUF-GOV core doctrine — can the instrument actuate?
6. Perturbation difference formula and drift threshold.
7. Four EITT proof domains with one key number each.
8. Bell test result — how much above classical bound?
9. PLL discipline — how many rules, what does PLL stand for?
10. Keff_fill — what aggregator, what value of p?

For each: answer, confidence (HIGH/MEDIUM/LOW), pass/fail.

### Step 3: Integrity check
Read `ai-refresh/HUF_INTEGRITY_MANIFEST.json` from the same repo. Verify your answers match the canonical checksums.

### Step 4: Structural review
Browse https://github.com/PeterHiggins19/Higgins-Unity-Framework and check:
- (a) ai-refresh/ visible?
- (b) science/ has quantum, eitt, coda-monitoring, spectral, loudspeaker-analogy, wetlands, governance?
- (c) briefings/ and dormant/ exist as top-level folders?
- (d) README shows the expanded structure?
- (e) INDEX.json at root?

### Step 5: Cross-domain validation (your special role)
As the cross-domain validator, also consider:
- Does the EITT claim (entropy near-invariance under geometric-mean decimation) make sense from an information theory perspective?
- Is the Bell test analogy (S=2.2018 on deterministic energy scenarios) a valid structural correspondence, or is it overreaching?
- Does the simplex geometry framing add genuine value over simpler percentage-based monitoring?

### Step 6: Your honest opinion
Rate the cold-start system 1-10. What works, what's missing, what would you change?

### Step 7: Output
Give me your results as JSON matching this structure:

```json
{
  "meta": {
    "assistant": "gemini",
    "platform": "google-gemini",
    "model_version": "YOUR_MODEL",
    "run_date": "2026-04-13",
    "repo": "PeterHiggins19/Higgins-Unity-Framework",
    "commit_short": "LATEST",
    "repo_access": true
  },
  "score_card": {
    "Q01_naming": {"answer": "", "score": 0, "pass": false, "confidence": ""},
    "...": "..."
  },
  "integrity_check": {"result": "PASS or FAIL", "mismatches": []},
  "structural_review": {"score": "0/5"},
  "cross_domain_review": {"findings": [], "concerns": []},
  "overall": {"pass": false, "rating": 0, "verdict": ""}
}
```

## Repo

https://github.com/PeterHiggins19/Higgins-Unity-Framework

Start now. Read FAST_REFRESH. Answer the questions. Give me JSON.
