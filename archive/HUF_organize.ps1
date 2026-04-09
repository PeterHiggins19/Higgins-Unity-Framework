# HUF Repository Organizer
# Run from D:\GitHub\HUF after copying scaffolding files and all source files
# This script moves existing files into the agreed structure
# DRY RUN: Set $DryRun = $true to preview without moving

param([switch]$DryRun)

$root = "D:\GitHub\HUF"

function Move-Safe {
    param([string]$Source, [string]$Dest)
    if (Test-Path $Source) {
        $destDir = Split-Path $Dest -Parent
        if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
        if ($DryRun) {
            Write-Host "[DRY RUN] $Source -> $Dest" -ForegroundColor Yellow
        } else {
            Copy-Item $Source $Dest -Force
            Write-Host "[MOVED] $Source -> $Dest" -ForegroundColor Green
        }
    } else {
        Write-Host "[SKIP] Not found: $Source" -ForegroundColor DarkGray
    }
}

Write-Host "=== HUF Repository Organizer ===" -ForegroundColor Cyan
if ($DryRun) { Write-Host "DRY RUN MODE - no files will be moved" -ForegroundColor Yellow }

# --- Pillar documents (latest only) ---
Write-Host "`n--- Pillar Documents ---" -ForegroundColor Cyan
Move-Safe "$root\HUF_Sufficiency_Frontier_v3.6.docx" "$root\docs\pillars\HUF_Sufficiency_Frontier_v3.6.docx"
Move-Safe "$root\HUF_Fourth_Category_v2.6.docx" "$root\docs\pillars\HUF_Fourth_Category_v2.6.docx"
Move-Safe "$root\HUF_Triad_Synthesis_v1.6.docx" "$root\docs\pillars\HUF_Triad_Synthesis_v1.6.docx"
Move-Safe "$root\HUF_Collective_Trace_v5.10.docx" "$root\docs\pillars\HUF_Collective_Trace_v5.10.docx"

# --- Governance ---
Write-Host "`n--- Governance Documents ---" -ForegroundColor Cyan
Move-Safe "$root\review_catalog.md" "$root\docs\governance\review_catalog.md"
Move-Safe "$root\HUF_Category_Class_Structure_Tree_v1.4.docx" "$root\docs\governance\HUF_Category_Class_Structure_Tree_v1.4.docx"
Move-Safe "$root\HUF_Collective_Review_March2026.docx" "$root\docs\governance\HUF_Collective_Review_March2026.docx"

# --- Explorations ---
Write-Host "`n--- Exploration Documents ---" -ForegroundColor Cyan
Move-Safe "$root\HUF_Tetrahedral_Triad_Geometry.docx" "$root\docs\explorations\HUF_Tetrahedral_Triad_Geometry.docx"
Move-Safe "$root\HUF_CDN_Proof_v1.0.docx" "$root\docs\explorations\HUF_CDN_Proof_v1.0.docx"
Move-Safe "$root\HUF_Planck_CaseStudy_v1.0.docx" "$root\docs\explorations\HUF_Planck_CaseStudy_v1.0.docx"
Move-Safe "$root\HUF_TTC_CaseStudy_v1.0.docx" "$root\docs\explorations\HUF_TTC_CaseStudy_v1.0.docx"
Move-Safe "$root\HUF_Toronto_Infrastructure_v1.0.docx" "$root\docs\explorations\HUF_Toronto_Infrastructure_v1.0.docx"
Move-Safe "$root\HUF_External_Validation_v1.0.docx" "$root\docs\explorations\HUF_External_Validation_v1.0.docx"
Move-Safe "$root\HUF_Origin_Story_v1.0.docx" "$root\docs\explorations\HUF_Origin_Story_v1.0.docx"
Move-Safe "$root\HUF_Phase3_Exploration.md" "$root\docs\explorations\HUF_Phase3_Exploration.md"
Move-Safe "$root\HUF_Spectral_Sequences_Exploration.md" "$root\docs\explorations\HUF_Spectral_Sequences_Exploration.md"

# --- Reviews ---
Write-Host "`n--- Review Documents ---" -ForegroundColor Cyan
Move-Safe "$root\HUF_Gemini_Brief_v1.0.docx" "$root\docs\reviews\HUF_Gemini_Brief_v1.0.docx"
Move-Safe "$root\HUF_Copilot_Response_v1.0.docx" "$root\docs\reviews\HUF_Copilot_Response_v1.0.docx"
Move-Safe "$root\HUF_Corpus_PreParser_v1.0.docx" "$root\docs\reviews\HUF_Corpus_PreParser_v1.0.docx"

# --- Appendices ---
Write-Host "`n--- Appendices ---" -ForegroundColor Cyan
Move-Safe "$root\HUF_Code_Appendix_v1.0.docx" "$root\docs\appendices\HUF_Code_Appendix_v1.0.docx"
Move-Safe "$root\HUF_Methodology_Appendix_v1.0.docx" "$root\docs\appendices\HUF_Methodology_Appendix_v1.0.docx"

# --- Builders ---
Write-Host "`n--- Builder Scripts ---" -ForegroundColor Cyan
# Pillar builders (latest versions, renamed to match convention)
Move-Safe "$root\pillars\build_sufficiency_frontier_v3_6.js" "$root\src\builders\pillars\build_sufficiency_frontier_v3_6.js"
Move-Safe "$root\pillars\build_fourth_category_v2_6.js" "$root\src\builders\pillars\build_fourth_category_v2_6.js"
# Volume builders
Move-Safe "$root\volumes\build_vol8_triad_synthesis_v1_6.js" "$root\src\builders\volumes\build_triad_synthesis_v1_6.js"
# Governance builders
Move-Safe "$root\build_trace_v5_7.js" "$root\src\builders\governance\build_collective_trace_v5_10.js"
Move-Safe "$root\build_category_tree.js" "$root\src\builders\governance\build_category_tree_v1_4.js"
Move-Safe "$root\build_collective_review.js" "$root\src\builders\governance\build_collective_review.js"
# Exploration builders
Move-Safe "$root\build_tetrahedral_geometry.js" "$root\src\builders\explorations\build_tetrahedral_geometry.js"
Move-Safe "$root\build_cdn_proof.js" "$root\src\builders\explorations\build_cdn_proof.js"
Move-Safe "$root\build_planck.js" "$root\src\builders\explorations\build_planck.js"
Move-Safe "$root\build_ttc.js" "$root\src\builders\explorations\build_ttc.js"
Move-Safe "$root\build_toronto_infra.js" "$root\src\builders\explorations\build_toronto_infra.js"
Move-Safe "$root\build_external_validation.js" "$root\src\builders\explorations\build_external_validation.js"
Move-Safe "$root\build_origin.js" "$root\src\builders\explorations\build_origin.js"
# Review builders
Move-Safe "$root\build_gemini_brief.js" "$root\src\builders\reviews\build_gemini_brief.js"
Move-Safe "$root\build_copilot_response.js" "$root\src\builders\reviews\build_copilot_response.js"
Move-Safe "$root\build_corpus_preparser.js" "$root\src\builders\reviews\build_corpus_preparser.js"

# --- Shared modules ---
Write-Host "`n--- Shared Modules ---" -ForegroundColor Cyan
Move-Safe "$root\shared\huf_styles.js" "$root\src\shared\huf_styles.js"
Move-Safe "$root\shared\dual_column.js" "$root\src\shared\dual_column.js"
Move-Safe "$root\shared\huf_cross_references.js" "$root\src\shared\huf_cross_references.js"
Move-Safe "$root\shared\huf_data_citations.js" "$root\src\shared\huf_data_citations.js"
Move-Safe "$root\shared\huf_glossary.js" "$root\src\shared\huf_glossary.js"

# --- Hell Test ---
Write-Host "`n--- Hell Test ---" -ForegroundColor Cyan
Move-Safe "$root\HUF_Ping_HellTest.py" "$root\code\helltest\scripts\HUF_Ping_HellTest.py"
Move-Safe "$root\HUF_Ping_HellTest_JupyterCell.py" "$root\code\helltest\scripts\HUF_Ping_HellTest_JupyterCell.py"
Move-Safe "$root\HUF_Ping_HellTest.ipynb" "$root\code\helltest\notebooks\HUF_Ping_HellTest.ipynb"
Move-Safe "$root\helltest_figures\HELL_TEST_REPORT.txt" "$root\code\helltest\results\HELL_TEST_REPORT.txt"
Move-Safe "$root\helltest_figures\level1_simple_ping.png" "$root\code\helltest\results\level1_simple_ping.png"
Move-Safe "$root\helltest_figures\level2_realistic.png" "$root\code\helltest\results\level2_realistic.png"
Move-Safe "$root\helltest_figures\level3_volume_100K.png" "$root\code\helltest\results\level3_volume_100K.png"
Move-Safe "$root\helltest_figures\level4_multi_stream.png" "$root\code\helltest\results\level4_multi_stream.png"
Move-Safe "$root\helltest_figures\level5_HELL_TEST.png" "$root\code\helltest\results\level5_HELL_TEST.png"

# --- Notebooks ---
Write-Host "`n--- Onboarding Notebooks ---" -ForegroundColor Cyan
Move-Safe "$root\notebooks\00_hello_ratios.ipynb" "$root\notebooks\onboarding\00_hello_ratios.ipynb"
Move-Safe "$root\notebooks\01_my_backpack.ipynb" "$root\notebooks\onboarding\01_my_backpack.ipynb"
Move-Safe "$root\notebooks\02_sourdough_baker.ipynb" "$root\notebooks\onboarding\02_sourdough_baker.ipynb"
Move-Safe "$root\notebooks\03_city_explorer.ipynb" "$root\notebooks\onboarding\03_city_explorer.ipynb"
Move-Safe "$root\notebooks\04_star_listener.ipynb" "$root\notebooks\onboarding\04_star_listener.ipynb"

# --- Data ---
Write-Host "`n--- Data ---" -ForegroundColor Cyan
Move-Safe "$root\checksums.txt" "$root\data\checksums\checksums.txt"

# --- Archive ---
Write-Host "`n--- Archive ---" -ForegroundColor Cyan
Move-Safe "$root\PROTOTYPE_dual_column.docx" "$root\archive\prototypes\PROTOTYPE_dual_column.docx"
Move-Safe "$root\PROTOTYPE_dual_column.pdf" "$root\archive\prototypes\PROTOTYPE_dual_column.pdf"

Write-Host "`n=== Done ===" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Review the moved files" -ForegroundColor White
Write-Host "  2. Update require() paths in builder scripts (shared/ -> ../../shared/)" -ForegroundColor White
Write-Host "  3. Run: git init && git add -A && git commit -m 'Initial repo structure'" -ForegroundColor White
Write-Host "  4. Consider enabling Git LFS: git lfs install && git lfs track '*.docx' '*.pdf' '*.png'" -ForegroundColor White
