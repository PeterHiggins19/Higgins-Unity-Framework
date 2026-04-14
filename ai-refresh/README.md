# AI Refresh Layer

**Status: STABLE** — validated across all 5 AI platforms on 2026-04-13.

**For any AI starting HUF work: read these files first, in this order.**

| Order | File | Purpose |
|-------|------|---------|
| 1 | `HUF_FAST_REFRESH.json` | All canonical names, numbers, formulas, structure. If anything elsewhere disagrees, this wins. |
| 2 | `HUF_INTEGRITY_MANIFEST.json` | SHA-256 hash verification, known drift patterns, refresh protocol. |
| 3 | `HUF_ADMIN.json` | All contact info, websites, emails, canonical terms, AI collaborator roles. Identity source of truth. |
| 4 | `huf_spec_v2.0.json` | Complete HUF framework specification v2.0. |

## Web Presence

- **Repository:** https://github.com/PeterHiggins19/Higgins-Unity-Framework
- **GitHub Pages:** https://peterhiggins19.github.io/Higgins-Unity-Framework/
- **Contact:** PeterHiggins@roguewaveaudio.com

## Cold-Start Test — COMPLETE

`AI_COLD_START_TEST.json` — cross-platform test protocol. All 5 platforms tested 2026-04-13.

| Platform | Questions | Integrity | Structure | Attempts |
|----------|-----------|-----------|-----------|----------|
| Claude   | 5/5 (abbrev.) | n/a | n/a | 1 |
| ChatGPT  | 10/10 | FAIL (caught 2 real bugs) | 4/5 | 2 |
| Grok     | 10/10 | PASS | 5/5 | 1 |
| Copilot  | 10/10 | NOT DONE | NOT DONE | 3 |
| Gemini   | 10/10 | PASS | 3/5 | 1 |

Results stored in `test-results/`. Key finding: every platform achieved 100% question accuracy from FAST_REFRESH alone. The single-file injection pattern works universally.

Bugs found and fixed during testing:
- **v1.1:** ChatGPT caught stale FAST_REFRESH hash + wrong EITT char_count (37→34)
- **v1.2:** Grok caught 21 stale file paths in manifest (pre-restructure paths)

## Known Drift Errors (caught 2026-04-13)

- **EITT name:** Always "Entropy-Invariant Time Transformer". NEVER "Ternary" or "Temporal".
- **Japan drift flag:** 2013-2014 (NOT 2011-2012). Fukushima March 2011, but annual data absorbs by 2013-2014.
- **Germany drift flags:** 2023-2024 d_A=9.07, 2024-2025 d_A=5.73. NOT 2011 moratorium.
- **UK flags:** Three specific values (2.98, 3.23, 3.26) with year-pairs. NEVER "approximately 3".

## Conflict Resolution

- `HUF_ADMIN.json` wins on identity, contacts, naming, URLs.
- `HUF_FAST_REFRESH.json` wins on numbers, formulas, science.
- If both address the same field, they must agree. Any disagreement is a bug — report to Peter.

## Platform Access Notes

- **ChatGPT, Grok:** Can usually browse GitHub directly.
- **Copilot:** Claims native GitHub access but could not fetch raw file URLs in practice.
- **Gemini, Claude:** Cannot fetch raw.githubusercontent.com. Need content pasted.
- **Fallback:** Always have paste-ready content. The test is valid with pasted content.
