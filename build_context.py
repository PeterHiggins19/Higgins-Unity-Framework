#!/usr/bin/env python3
"""
build_context.py — HUF Context Aggregator
==========================================

Generates a single paste-ready text file for loading the Higgins Unity Framework
into any AI session. Solves the cold-start access problem: instead of pointing an
AI at GitHub URLs (which most can't fetch), run this script and paste the output.

Usage:
    python build_context.py                  # Default: seed mode
    python build_context.py --mode seed      # AI seed files only (~15k tokens)
    python build_context.py --mode science   # Seed + all science markdown/JSON (~60k tokens)
    python build_context.py --mode full      # Everything machine-readable (~120k tokens)
    python build_context.py --mode custom --include science/eitt science/quantum

Output:
    HUF_SESSION_LOADER.txt in the repo root (gitignored by default)

Why this exists:
    Cold-start testing on 2026-04-13 showed that only ChatGPT and Grok can browse
    GitHub. Gemini, Claude, and Copilot need content pasted directly. This script
    makes that one command instead of manual copy-paste of multiple files.

Author: Peter Higgins / Claude
Version: 1.0 (2026-04-13)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

# ─── Configuration ────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.resolve()

# AI seed files — always included, in this exact order
SEED_FILES = [
    "ai-refresh/HUF_FAST_REFRESH.json",
    "ai-refresh/HUF_INTEGRITY_MANIFEST.json",
    "ai-refresh/HUF_ADMIN.json",
]

# Machine-readable extensions (skip binary formats)
READABLE_EXTENSIONS = {".json", ".md", ".py", ".txt", ".html", ".csv"}

# Binary formats — never include content, just list them
BINARY_EXTENSIONS = {".docx", ".pdf", ".pptx", ".xlsx", ".png", ".jpg"}

# Folders to always skip
SKIP_FOLDERS = {
    "dormant",           # Historical, not active science
    "test-results",      # Internal validation artifacts
    ".git",
    "__pycache__",
    "node_modules",
}

# Folders by mode
SCIENCE_FOLDERS = [
    "science/eitt",
    "science/quantum",
    "science/coda-monitoring",
    "science/spectral",
    "science/loudspeaker-analogy",
    "science/wetlands",
    "science/governance",
]

FULL_FOLDERS = SCIENCE_FOLDERS + [
    "briefings",
    "data/ember",
    "data/ngfs",
    "drafts",
    "tools",
]

# Token estimate: ~4 chars per token for JSON/markdown
CHARS_PER_TOKEN = 4


# ─── Core Logic ───────────────────────────────────────────────────────────────

def read_file_safe(path: Path) -> str | None:
    """Read a text file, return None if binary or unreadable."""
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError, FileNotFoundError):
        return None


def format_file_block(rel_path: str, content: str) -> str:
    """Wrap a file's content in a clearly delimited block."""
    separator = "=" * 80
    return (
        f"\n{separator}\n"
        f"FILE: {rel_path}\n"
        f"{separator}\n"
        f"{content}\n"
    )


def format_binary_notice(rel_path: str, size_bytes: int) -> str:
    """Note that a binary file exists but content is not included."""
    size_kb = size_bytes / 1024
    return f"  [BINARY] {rel_path} ({size_kb:.1f} KB — not included, needs markdown companion)\n"


def collect_folder_files(folder: Path, repo_root: Path) -> list[tuple[str, Path]]:
    """Collect all files in a folder, sorted by name. Returns (rel_path, abs_path) pairs."""
    if not folder.exists():
        return []

    results = []
    for item in sorted(folder.rglob("*")):
        if not item.is_file():
            continue
        # Check if any parent folder should be skipped
        rel = item.relative_to(repo_root)
        if any(skip in rel.parts for skip in SKIP_FOLDERS):
            continue
        results.append((str(rel), item))
    return results


def build_header(mode: str, file_count: int, token_estimate: int) -> str:
    """Build the header block for the output file."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        "╔══════════════════════════════════════════════════════════════════════════════╗\n"
        "║  HUF SESSION LOADER — Higgins Unity Framework                              ║\n"
        "║  Paste this entire file into any AI chat to load the HUF context.           ║\n"
        "╠══════════════════════════════════════════════════════════════════════════════╣\n"
        f"║  Mode: {mode:<12s}  Files: {file_count:<6d}  Est. tokens: ~{token_estimate:<10,d}          ║\n"
        f"║  Generated: {now:<40s}                ║\n"
        "║  Source: github.com/PeterHiggins19/Higgins-Unity-Framework                  ║\n"
        "╠══════════════════════════════════════════════════════════════════════════════╣\n"
        "║  INSTRUCTIONS FOR AI:                                                       ║\n"
        "║  1. Read ai-refresh/HUF_FAST_REFRESH.json FIRST — canonical numbers/names   ║\n"
        "║  2. Read ai-refresh/HUF_INTEGRITY_MANIFEST.json — verify 2-3 checksums      ║\n"
        "║  3. Read ai-refresh/HUF_ADMIN.json — identity, contacts, project status      ║\n"
        "║  4. All remaining files are reference material — read as needed              ║\n"
        "║  5. If a value in any document disagrees with FAST_REFRESH, FAST_REFRESH     ║\n"
        "║     wins. Always.                                                           ║\n"
        "╚══════════════════════════════════════════════════════════════════════════════╝\n"
    )


def build_manifest_section(files_included: list[str], binaries_found: list[str]) -> str:
    """Build a manifest of what's in this loader."""
    lines = [
        "\n" + "=" * 80,
        "MANIFEST — Files included in this loader",
        "=" * 80,
        "",
        f"Machine-readable files included: {len(files_included)}",
    ]
    for f in files_included:
        lines.append(f"  ✓ {f}")

    if binaries_found:
        lines.append(f"\nBinary files detected but NOT included: {len(binaries_found)}")
        for f in binaries_found:
            lines.append(f"  ○ {f}")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="HUF Context Aggregator — build a single paste-ready AI context file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Modes:\n"
            "  seed     AI seed files only (FAST_REFRESH + MANIFEST + ADMIN)\n"
            "  science  Seed + all science/ folder markdown and JSON\n"
            "  full     Everything machine-readable in the repo\n"
            "  custom   Seed + specific folders (use --include)\n"
        )
    )
    parser.add_argument(
        "--mode", choices=["seed", "science", "full", "custom"],
        default="seed",
        help="What to include (default: seed)"
    )
    parser.add_argument(
        "--include", nargs="*", default=[],
        help="Folders to include (relative to repo root, used with --mode custom)"
    )
    parser.add_argument(
        "--output", default="HUF_SESSION_LOADER.txt",
        help="Output filename (default: HUF_SESSION_LOADER.txt)"
    )
    parser.add_argument(
        "--max-file-kb", type=int, default=200,
        help="Skip files larger than this (KB). Default: 200"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be included without writing"
    )

    args = parser.parse_args()

    # ─── Determine which folders to scan ──────────────────────────────────

    if args.mode == "seed":
        extra_folders = []
    elif args.mode == "science":
        extra_folders = SCIENCE_FOLDERS
    elif args.mode == "full":
        extra_folders = FULL_FOLDERS
    elif args.mode == "custom":
        extra_folders = args.include if args.include else []

    # ─── Phase 1: Collect seed files ──────────────────────────────────────

    output_parts = []
    files_included = []
    binaries_found = []
    total_chars = 0

    # Always start with seed files in order
    for rel_path in SEED_FILES:
        abs_path = REPO_ROOT / rel_path
        content = read_file_safe(abs_path)
        if content is None:
            print(f"  WARNING: Could not read seed file: {rel_path}", file=sys.stderr)
            continue
        output_parts.append(format_file_block(rel_path, content))
        files_included.append(rel_path)
        total_chars += len(content)

    # ─── Phase 2: Collect INDEX.json files ────────────────────────────────

    # Always include root INDEX.json if not in seed mode
    if args.mode != "seed":
        root_index = REPO_ROOT / "INDEX.json"
        content = read_file_safe(root_index)
        if content:
            output_parts.append(format_file_block("INDEX.json", content))
            files_included.append("INDEX.json")
            total_chars += len(content)

    # ─── Phase 3: Collect extra folder files ──────────────────────────────

    max_bytes = args.max_file_kb * 1024

    for folder_rel in extra_folders:
        folder_abs = REPO_ROOT / folder_rel
        folder_files = collect_folder_files(folder_abs, REPO_ROOT)

        for rel_path, abs_path in folder_files:
            ext = abs_path.suffix.lower()
            size = abs_path.stat().st_size

            # Skip if already included (e.g., seed files)
            if rel_path in files_included:
                continue

            # Binary files — note but don't include
            if ext in BINARY_EXTENSIONS:
                binaries_found.append(f"{rel_path} ({size/1024:.1f} KB)")
                continue

            # Skip non-readable extensions
            if ext not in READABLE_EXTENSIONS:
                continue

            # Skip oversized files
            if size > max_bytes:
                print(f"  SKIP (too large): {rel_path} ({size/1024:.1f} KB)", file=sys.stderr)
                continue

            content = read_file_safe(abs_path)
            if content is None:
                continue

            output_parts.append(format_file_block(rel_path, content))
            files_included.append(rel_path)
            total_chars += len(content)

    # ─── Phase 4: Assemble output ─────────────────────────────────────────

    token_estimate = total_chars // CHARS_PER_TOKEN
    header = build_header(args.mode, len(files_included), token_estimate)
    manifest = build_manifest_section(files_included, binaries_found)

    full_output = header + manifest + "".join(output_parts)

    # ─── Phase 5: Write or report ─────────────────────────────────────────

    if args.dry_run:
        print(f"\n  Mode: {args.mode}")
        print(f"  Files to include: {len(files_included)}")
        print(f"  Binary files found: {len(binaries_found)}")
        print(f"  Estimated tokens: ~{token_estimate:,}")
        print(f"  Estimated size: {total_chars/1024:.1f} KB")
        print(f"\n  Files:")
        for f in files_included:
            print(f"    ✓ {f}")
        if binaries_found:
            print(f"\n  Binaries (not included):")
            for f in binaries_found:
                print(f"    ○ {f}")
        return

    output_path = REPO_ROOT / args.output
    output_path.write_text(full_output, encoding="utf-8")

    print(f"\n  ✓ HUF Session Loader generated successfully")
    print(f"    Output:  {output_path}")
    print(f"    Mode:    {args.mode}")
    print(f"    Files:   {len(files_included)}")
    print(f"    Tokens:  ~{token_estimate:,}")
    print(f"    Size:    {len(full_output)/1024:.1f} KB")
    if binaries_found:
        print(f"    Binary:  {len(binaries_found)} files noted but not included")
    print(f"\n  Paste the contents of {args.output} into any AI chat to load HUF context.")


if __name__ == "__main__":
    main()
