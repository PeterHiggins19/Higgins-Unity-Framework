# HUF Repository Map

## Folder Structure

```
HUF/
├── docs/                          # Canonical documents (latest versions only)
│   ├── index.md                   # Reading order and document status
│   ├── pillars/                   # The four core HUF papers
│   │   ├── HUF_Sufficiency_Frontier_v3.6.docx
│   │   ├── HUF_Fourth_Category_v2.6.docx
│   │   ├── HUF_Triad_Synthesis_v1.6.docx
│   │   └── HUF_Collective_Trace_v5.10.docx
│   ├── governance/                # Review tracking and category classification
│   │   ├── review_catalog.md
│   │   ├── HUF_Category_Class_Structure_Tree_v1.4.docx
│   │   └── HUF_Collective_Review_March2026.docx
│   ├── explorations/              # Case studies, proofs, formal explorations
│   ├── reviews/                   # Individual AI system review documents
│   └── appendices/                # Code appendix, methodology appendix
├── src/                           # Source code
│   ├── builders/                  # JavaScript docx-js builder scripts
│   │   ├── pillars/               # Pillar document builders
│   │   ├── volumes/               # Volume builders (Triad Synthesis)
│   │   ├── governance/            # Trace and tree builders
│   │   ├── explorations/          # Case study and proof builders
│   │   └── reviews/               # AI review document builders
│   ├── shared/                    # Common modules (styles, citations, glossary)
│   └── validation/                # Document validation scripts
├── code/                          # Executable code and experiments
│   └── helltest/                  # MC-4 detection stress test
│       ├── scripts/               # Python scripts
│       ├── notebooks/             # Jupyter notebooks
│       └── results/               # Generated figures and reports
├── notebooks/                     # Educational content
│   └── onboarding/                # HUF onboarding notebook series (00-04)
├── data/                          # Manifests and integrity data
│   ├── manifests/                 # Data, benchmark, and release manifests
│   └── checksums/                 # SHA256 document integrity hashes
├── archive/                       # Non-canonical historical artifacts
│   ├── prototypes/                # Layout prototypes
│   ├── legacy-generated-docs/     # Superseded .docx (prefer git history)
│   └── legacy-builders/           # Superseded builder scripts
└── .github/workflows/             # CI: validate and build
```

## Document Status Legend

| Status | Meaning |
|--------|---------|
| **Canonical** | Current latest version, lives in `docs/` |
| **Superseded** | Replaced by a newer version; preserved in git history |
| **Archival** | Historical artifact; lives in `archive/` if needed |
| **Experimental** | Work in progress; lives in `code/` or working branch |

## Release Policy

Only canonical documents live on `main`. Superseded versions are accessible through git tags, commit history, or GitHub Releases (binary attachments). The `VERSION_MANIFEST.json` tracks what is current.
