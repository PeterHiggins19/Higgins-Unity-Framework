# AI Refresh Layer

**For any AI starting HUF work: read these files first, in this order.**

| Order | File | Purpose |
|-------|------|---------|
| 1 | `HUF_FAST_REFRESH.json` | All canonical names, numbers, formulas, structure. If anything elsewhere disagrees, this wins. |
| 2 | `HUF_INTEGRITY_MANIFEST.json` | SHA-256 hash verification, known drift patterns, refresh protocol. |
| 3 | `huf_spec_v2.0.json` | Complete HUF framework specification v2.0. |

## Known Drift Errors (caught 2026-04-13)

- **EITT name:** Always "Entropy-Invariant Time Transformer". NEVER "Ternary" or "Temporal".
- **Japan drift flag:** 2013-2014 (NOT 2011-2012). Fukushima March 2011, but annual data absorbs by 2013-2014.
- **Germany drift flags:** 2023-2024 d_A=9.07, 2024-2025 d_A=5.73. NOT 2011 moratorium.
- **UK flags:** Three specific values (2.98, 3.23, 3.26) with year-pairs. NEVER "approximately 3".
