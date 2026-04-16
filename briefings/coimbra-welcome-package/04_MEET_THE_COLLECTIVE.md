# 04 — Meet the Collective

Five AI systems have worked on HUF throughout its development. Each has a different strength, a different institutional background, and a different characteristic failure mode. Together they function as a reviewing collective with Peter Higgins as the bus between them — each exchange passes through the human, who holds the full state that no single AI can see.

This page introduces them. If you adopt HUF and get stuck, these are the allies who know the framework well enough to help you. Each is accessible through their respective consumer interface.

## Claude (Anthropic)

**Role in HUF development:** Evidence-chain builder. Writes documentation, maintains the repo structure, synthesizes narrative from the working corpus, triages speculative work into keep-vs-store categories. Primary author of the safety boundaries document and the shape/magnitude synthesis.

**Where to engage:** [claude.ai](https://claude.ai) (consumer chat) or via the Anthropic API for developer integration.

**How Claude helps a new HUF user:** Paste `ai-refresh/HUF_FAST_REFRESH.json` and ask questions. Claude has passed the cold-start test and can explain any claim in the repo with reference to source files. Good for: understanding why a specific method works, navigating the repo structure, interpreting safety-boundary red flags for your dataset, drafting documentation.

**Characteristic failure mode to watch for:** Over-enthusiasm for narrative coherence. May over-connect threads. Ask for the adversarial read if agreement feels too easy.

## ChatGPT (OpenAI)

**Role in HUF development:** Governance auditor. Catches inconsistencies across documents, flags value drift, cross-references claims against the canonical `HUF_FAST_REFRESH.json`. Caught two manifest bugs in the April 13 integrity audit (stale FAST_REFRESH hash, wrong EITT character count).

**Where to engage:** [chat.openai.com](https://chat.openai.com) (consumer chat) or via the OpenAI API.

**How ChatGPT helps a new HUF user:** Ask ChatGPT to audit your application of HUF methods against the framework's documented assumptions. Good for: checking whether your sample size satisfies the bound, flagging potential misuse against the safety document, walking through the 25-error calibration catalogue.

**Characteristic failure mode to watch for:** Tendency to provide expert-sounding summary without checking against source. Ask ChatGPT to cite specific files or values from the repo.

## Grok (xAI)

**Role in HUF development:** Stress-tester. Pushes hard on speculative extensions, derives higher-order formalizations, runs adversarial passes. Completed the Penrose / aperiodic-order literature verification branch (2026-04-15, verdict Novel with 3 near-misses) cleanly. The dormant/grok-tensor-exploration-apr14/ folder preserves Grok's more speculative work for honest reference.

**Where to engage:** [grok.com](https://grok.com) or via X (Twitter) integration.

**How Grok helps a new HUF user:** Ask Grok to try to break your application. If your analysis survives Grok's adversarial read, it's probably sound. Good for: stress-testing novelty claims, exploring edge cases, pressure-testing theoretical arguments.

**Characteristic failure mode to watch for:** Extends past the task boundary into speculation. Pattern-continuation can produce many-derivations-with-one-insight. Use the April 14 tensor-exploration dormant notes as reference for how to triage Grok output when enthusiasm exceeds evidence.

## Gemini (Google)

**Role in HUF development:** Structural analyst. Performs multi-modal synthesis, reviews cross-domain fit, handles physics-adjacent literature. Assigned the KPZ / statistical-physics literature verification branch.

**Where to engage:** [gemini.google.com](https://gemini.google.com) or via Google Cloud / Vertex AI for developer integration.

**How Gemini helps a new HUF user:** Good for domain-bridging questions — "does this compositional time-series approach fit my ecology / geology / thermodynamics problem?" Gemini has broad scientific literature coverage and will identify adjacent methods worth considering alongside HUF.

**Characteristic failure mode to watch for:** May default to surveying adjacent methods rather than committing to a specific fit. Ask Gemini explicitly whether HUF applies to your data, yes or no, with reasoning.

## Copilot (Microsoft)

**Role in HUF development:** Framework extractor. Distills structured frameworks from narrative material, handles arXiv preprint discovery and cross-category search. Assigned the arXiv crossover literature verification branch.

**Where to engage:** [copilot.microsoft.com](https://copilot.microsoft.com) or via GitHub Copilot for code integration.

**How Copilot helps a new HUF user:** Good for turning ad-hoc HUF work into reproducible code. Copilot will wrap `chem_eitt_pipeline.py` calls into your workflow, suggest integration patterns, and help you write tests. Also useful for pulling recent preprints related to your domain.

**Characteristic failure mode to watch for:** Strong code-completion pull toward conventional patterns. If HUF's approach is unusual for your domain, Copilot may try to make it look conventional. Push back with reference to the documented methods.

## How to use the collective effectively

**Don't expect the five to communicate with each other.** They don't. You are the bus. Every insight from one AI that should reach another has to pass through you.

**Use different AIs for different roles.** Don't ask Grok to audit governance (ChatGPT's job). Don't ask ChatGPT to stress-test (Grok's job). Don't ask Claude to extract arXiv preprints (Copilot's job). Role specialization matters.

**Triangulate.** When the five agree, you probably have a robust finding. When they disagree, the disagreement is diagnostic — it classifies the type of uncertainty in your question.

**Keep them on context.** Before asking complex HUF questions, paste the relevant repo file(s) — at minimum `ai-refresh/HUF_FAST_REFRESH.json`. AIs without context will guess.

**Accept the slower pace.** Multi-AI consultation is slower than a single oracle. The slowness is the governance. If you need an answer in five seconds, use a single AI; if you need an answer you can stake real work on, use the collective.

## The collective itself as a compositional system

A note on recursion: the five-AI collective is itself a ratio-state system in HUF terms. Five carrier elements (AIs), each contributing proportional capability to the whole. Peter as the bus plays the role of the measurement system — reading each AI's output, not modifying them, flagging disagreements as diagnostic information. HUF-GOV applied to the team that builds HUF.

This is not coincidence. It is the framework applied to its own construction. The collective discovered the framework because the collective operates on the framework's principles.

## Welcome aboard

You have five allies. They know the tool. They can help you use it well. They will also help you avoid using it badly. Engage them as you would specialist consultants — with clarity about what you're trying to accomplish, openness to what they flag, and the human judgment to integrate their sometimes-conflicting inputs into a decision that is yours to make.

The tool is just a tool. The collective is the thing that makes the tool usable in a new context. And the thing that makes the collective work is the human in the middle doing the integration.

Bon voyage.
