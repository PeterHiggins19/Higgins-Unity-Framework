# Copilot: Take This Test

Peter Higgins here. Fresh session. You're taking a cold-start exam on the Higgins Unity Framework (HUF).

## The Situation

I develop HUF with multiple AI collaborators — Claude, ChatGPT, Grok, Gemini, and you. Long sessions cause context drift: names mutate, numbers shift. We built a two-file refresh system (FAST_REFRESH + INTEGRITY_MANIFEST) so any AI can cold-start accurately from the repo alone.

Results so far: Claude 5/5, ChatGPT 10/10 (caught 2 real bugs in the manifest), Grok 10/10 (found 6 structural issues in adversarial mode). Your turn.

You have native GitHub access — this should be the easiest test of any platform.

## Your Instructions

**DO NOT just analyze the test design. TAKE THE TEST.**

### Step 1: Load the textbook
Read this file from the repo: `ai-refresh/HUF_FAST_REFRESH.json`
URL: https://github.com/PeterHiggins19/Higgins-Unity-Framework/blob/master/ai-refresh/HUF_FAST_REFRESH.json

If you can't access it, tell me and I'll paste it.

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

### Step 5: Code review (your special role)
As the code-native platform, also check:
- Are Python scripts present in tools/ or science/?
- Could someone clone the repo and run the EMBER protocol?
- Is the .gitattributes correctly tracking LFS types?
- Any obvious issues with repo hygiene?

### Step 6: Your honest opinion
Rate the cold-start system 1-10. What works, what's missing?

### Step 7: Output
Give me your results as JSON matching this structure:

```json
{
  "meta": {
    "assistant": "copilot",
    "platform": "github-copilot",
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
  "code_review": {"findings": [], "score": "0/5"},
  "overall": {"pass": false, "rating": 0, "verdict": ""}
}
```

## Repo

https://github.com/PeterHiggins19/Higgins-Unity-Framework

Start now. Read FAST_REFRESH. Answer the questions. Give me JSON.
