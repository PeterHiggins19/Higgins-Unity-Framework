# AI Refresh Layer

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

## Cold-Start Test

`AI_COLD_START_TEST.json` — cross-platform test protocol. Results stored in `test-results/`.

## Known Drift Errors (caught 2026-04-13)

- **EITT name:** Always "Entropy-Invariant Time Transformer". NEVER "Ternary" or "Temporal".
- **Japan drift flag:** 2013-2014 (NOT 2011-2012). Fukushima March 2011, but annual data absorbs by 2013-2014.
- **Germany drift flags:** 2023-2024 d_A=9.07, 2024-2025 d_A=5.73. NOT 2011 moratorium.
- **UK flags:** Three specific values (2.98, 3.23, 3.26) with year-pairs. NEVER "approximately 3".

## Conflict Resolution

- `HUF_ADMIN.json` wins on identity, contacts, naming, URLs.
- `HUF_FAST_REFRESH.json` wins on numbers, formulas, science.
- If both address the same field, they must agree. Any disagreement is a bug — report to Peter.
