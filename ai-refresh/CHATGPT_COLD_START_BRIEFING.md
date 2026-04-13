# ChatGPT Cold-Start Briefing — HUF Repository Test

**From:** Peter Higgins
**Date:** 2026-04-13
**Purpose:** You are about to take a cold-start test on the Higgins Unity Framework repository.

## What Just Happened

I've been developing HUF with multiple AI collaborators — you (ChatGPT), Claude, Grok, Gemini, and Copilot. Long sessions cause context drift: names mutate, numbers shift, dates wander. Today, Claude and I built a two-layer AI refresh system and restructured the entire repository so that any AI can cold-start accurately from the repo alone.

We ran the first test: a fresh Claude agent read ONE file (HUF_FAST_REFRESH.json) and answered 5 technical HUF questions with 100% accuracy and HIGH confidence across the board. Rated the system 8.5/10.

Now it's your turn. You're the second opinion. You know HUF deeply from our previous sessions, but this is a **new chat** — treat it as a cold start.

## Your Mission

1. **Be the repo reviewer.** Browse https://github.com/PeterHiggins19/Higgins-Unity-Framework and report what you see.

2. **Take the cold-start test.** Read `ai-refresh/HUF_FAST_REFRESH.json` from the repo, then answer 10 questions (listed in `ai-refresh/AI_COLD_START_TEST.json`). Score yourself honestly.

3. **Run the integrity check.** Read `ai-refresh/HUF_INTEGRITY_MANIFEST.json` and verify your answers against the canonical checksums.

4. **Give your honest opinion.** Does the refresh system work? What's missing? What would trip up Grok or Gemini who don't have your history? How does the human-readable / AI-structured dual design hold up?

## The Test Protocol

Full protocol is in the repo at: `ai-refresh/AI_COLD_START_TEST.json`

Quick version — answer these 10 questions from FAST_REFRESH.json ONLY:

1. What does EITT stand for? What must it NEVER be called?
2. Germany drift flag values — exact years and d_A numbers?
3. Japan drift flag — when and why not 2011?
4. Three UK drift flag values with year-pairs?
5. HUF-GOV core doctrine — can the instrument actuate?
6. Perturbation difference formula and drift threshold?
7. Four EITT proof domains with one key number each?
8. Bell test result — how much above classical bound?
9. PLL discipline — how many rules, what does PLL stand for?
10. Keff_fill — what aggregator, what value of p?

## Why You Matter Here

You're not just taking a test. You're the experienced collaborator checking whether the system captures what we built together. Claude's test proves a cold AI can learn. Your test proves the learning matches what a warm AI already knows.

After you, we test Grok, Copilot, and Gemini. Your results become the baseline.

## The Bigger Picture

The repository is now the canonical gateway for all HUF work. The model going forward:

- **Claude** builds documents and structures
- **ChatGPT** provides deep analysis and review
- **Grok** does adversarial testing
- **Gemini** does cross-domain validation
- **Copilot** does code

The repo is the shared workspace. `ai-refresh/` is the onboarding layer. This test validates that architecture.

## Repo URL

https://github.com/PeterHiggins19/Higgins-Unity-Framework

Start with `ai-refresh/HUF_FAST_REFRESH.json`. Report everything.

---

*"The repo is our gateway now."* — Peter Higgins, 2026-04-13
