#!/usr/bin/env python3
"""
HUF Pre-Parser v3.0.0
=====================
Reads Backblaze data (zip files, directories of CSVs, or a folder of zips)
and outputs HUF Data Intermediate (HDI) JSON files.

Reduces ~8.5 GB of quarterly zips -> ~100-500 KB HDI file by extracting only
the aggregate portfolio statistics that HUF compositional analysis requires.

MODES:
  Batch mode:    python huf_preparser.py D:\HUF_DATA\BackBlaze
                 (auto-discovers all data_Q*.zip files, processes sequentially)

  Single zip:    python huf_preparser.py data_Q4_2025.zip

  Directory:     python huf_preparser.py D:\data_Q4_2025\data_Q4_2025
                 (directory of YYYY-MM-DD.csv files)

Batch mode auto-discovers data_Q*.zip files in a folder, sorts them
chronologically, streams through each zip without extraction, and
outputs one combined HDI file covering the full date range.

OPTIONS:
  --output, -o      Output HDI file path (default: auto-named in input dir)
  --models           Include per-model breakdown (larger output)
  --date YYYY-MM-DD  Process only a specific date
  --sample N         Process every Nth day only (e.g. --sample 7 for weekly)
  --first-of-month   Process only the 1st of each month (quick longitudinal)
  --flag-truncated   Auto-flag files significantly smaller than median (default: on)
  --quiet, -q        Suppress progress output

HUF Document ID: HUF.SOFTWARE.TOOL.PREPARSER_BACKBLAZE.v3.0.0
Status: draft | OCC: OP=0.51 TOOL=0.49

Author: Claude (Session 6) for Peter Higgins / HUF Collective
License: Same as HUF project
"""

import argparse
import csv
import hashlib
import io
import json
import os
import statistics
import sys
import time
import zipfile
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# === HUF CONFIGURATION ===
# These are the SMART attributes that define HUF's K=4 reliability portfolio.
# Each maps to a compositional component (governance "node").
HUF_PORTFOLIO = {
    "Mechanical": {
        "key": "smart_5_raw",
        "description": "Reallocated Sectors Count - physical media reallocation",
    },
    "Electronic": {
        "key": "smart_187_raw",
        "description": "Reported Uncorrectable Errors - controller/firmware errors",
    },
    "Media": {
        "key": "smart_197_raw",
        "description": "Current Pending Sector Count - sectors awaiting reallocation",
    },
    "Offline": {
        "key": "smart_198_raw",
        "description": "Offline Uncorrectable - sectors failed offline scan",
    },
}

PARSER_VERSION = "huf-preparser-3.0.0"

# Truncation detection: if a file is less than this fraction of the median
# file size, flag it as potentially truncated
TRUNCATION_THRESHOLD = 0.50  # 50% of median = likely truncated


def compute_sha256(filepath):
    """Compute SHA-256 hash for provenance tracking."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def compute_dir_hash(file_list):
    """Compute a combined hash of all CSV files in the directory (sorted by name)."""
    h = hashlib.sha256()
    for filepath in sorted(file_list):
        h.update(filepath.encode("utf-8"))
        h.update(str(os.path.getsize(filepath)).encode("utf-8"))
    return h.hexdigest()


# ─────────────────────────────────────────────────────────
# CORE: Process a single CSV (works for both zip and file)
# ─────────────────────────────────────────────────────────

def process_csv_stream(text_stream, label, include_models=False, quiet=False):
    """
    Process a CSV text stream and return a snapshot dict.
    Works for both zip entries and local files.
    """
    if not quiet:
        print(f"  {label}...", end="", flush=True)

    start = time.time()
    reader = csv.DictReader(text_stream)

    # Validate required columns
    fieldnames = reader.fieldnames or []
    required_keys = [p["key"] for p in HUF_PORTFOLIO.values()]
    missing = [k for k in required_keys if k not in fieldnames]
    if missing:
        raise ValueError(
            f"CSV missing required SMART columns: {missing}. "
            f"Available: {fieldnames[:20]}..."
        )

    fleet_size = 0
    total_anomalous = 0
    anomaly_counts = {lbl: 0 for lbl in HUF_PORTFOLIO}
    failure_count = 0

    model_data = defaultdict(lambda: {
        "fleet": 0, "anomalous": 0,
        "anomaly_counts": {lbl: 0 for lbl in HUF_PORTFOLIO},
        "failures": 0,
    }) if include_models else None

    for row in reader:
        fleet_size += 1
        model = row.get("model", "UNKNOWN") if include_models else None

        drive_anomalous = False
        for lbl, config in HUF_PORTFOLIO.items():
            key = config["key"]
            val_str = row.get(key, "0").strip()
            try:
                val = int(val_str) if val_str else 0
            except (ValueError, TypeError):
                try:
                    val = int(float(val_str))
                except (ValueError, TypeError):
                    val = 0

            if val > 0:
                anomaly_counts[lbl] += 1
                drive_anomalous = True
                if include_models and model:
                    model_data[model]["anomaly_counts"][lbl] += 1

        if drive_anomalous:
            total_anomalous += 1
            if include_models and model:
                model_data[model]["anomalous"] += 1

        failure_str = row.get("failure", "0").strip()
        if failure_str == "1":
            failure_count += 1
            if include_models and model:
                model_data[model]["failures"] += 1

        if include_models and model:
            model_data[model]["fleet"] += 1

    elapsed = time.time() - start
    K = len(HUF_PORTFOLIO)

    # Compositional weights
    total_anomaly_events = sum(anomaly_counts.values())
    if total_anomaly_events > 0:
        rho = {lbl: round(c / total_anomaly_events, 6)
               for lbl, c in anomaly_counts.items()}
    else:
        rho = {lbl: round(1.0 / K, 6) for lbl in HUF_PORTFOLIO}

    # MDG vs neutral
    neutral = 1.0 / K
    mdg_bps = round(sum(abs(rho[lbl] - neutral) for lbl in HUF_PORTFOLIO) * 10000)

    # Leverage
    leverage = {lbl: round(1.0 / rho[lbl], 4) if rho[lbl] > 0 else float("inf")
                for lbl in HUF_PORTFOLIO}

    # Governance status
    thresholds = {"advisory_bps": 58, "alert_bps": 96, "critical_bps": 193}
    if mdg_bps > thresholds["critical_bps"]:
        status = "CRITICAL"
    elif mdg_bps > thresholds["alert_bps"]:
        status = "ALERT"
    elif mdg_bps > thresholds["advisory_bps"]:
        status = "ADVISORY"
    else:
        status = "NOMINAL"

    snapshot = {
        "fleet_size": fleet_size,
        "total_anomalous_drives": total_anomalous,
        "anomaly_rate_pct": round(total_anomalous / fleet_size * 100, 4) if fleet_size > 0 else 0,
        "total_anomaly_events": total_anomaly_events,
        "failure_count": failure_count,
        "K": K,
        "component_labels": list(HUF_PORTFOLIO.keys()),
        "component_keys": [p["key"] for p in HUF_PORTFOLIO.values()],
        "anomaly_counts": anomaly_counts,
        "rho": rho,
        "leverage": leverage,
        "mdg_bps": mdg_bps,
        "governance_status": status,
        "thresholds": thresholds,
        "processing_time_seconds": round(elapsed, 2),
    }

    if include_models and model_data:
        model_breakdown = {}
        for mdl, data in sorted(model_data.items(), key=lambda x: -x[1]["fleet"]):
            mdl_total = sum(data["anomaly_counts"].values())
            if mdl_total > 0:
                mdl_rho = {lbl: round(c / mdl_total, 6)
                           for lbl, c in data["anomaly_counts"].items()}
            else:
                mdl_rho = {lbl: round(1.0 / K, 6) for lbl in HUF_PORTFOLIO}
            model_breakdown[mdl] = {
                "fleet": data["fleet"],
                "anomalous": data["anomalous"],
                "failures": data["failures"],
                "anomaly_counts": dict(data["anomaly_counts"]),
                "rho": mdl_rho,
            }
        snapshot["model_breakdown"] = model_breakdown

    if not quiet:
        print(f" {fleet_size:,} drives, {total_anomalous:,} anomalous, "
              f"MDG={mdg_bps} bps [{status}] ({elapsed:.1f}s)")

    return snapshot


# ─────────────────────────────────────────────────────────
# DIRECTORY MODE: Walk date-sequenced CSVs
# ─────────────────────────────────────────────────────────

def discover_csv_dates(directory):
    """
    Scan directory for YYYY-MM-DD.csv files.
    Returns sorted list of (date_str, filepath, filesize) tuples.
    """
    found = []
    for f in os.listdir(directory):
        if not f.endswith(".csv"):
            continue
        basename = f.replace(".csv", "")
        try:
            datetime.strptime(basename, "%Y-%m-%d")
            fpath = os.path.join(directory, f)
            found.append((basename, fpath, os.path.getsize(fpath)))
        except ValueError:
            pass
    found.sort(key=lambda x: x[0])
    return found


def detect_truncated(csv_list):
    """
    Detect truncated files by comparing sizes to median.
    Returns dict of date -> truncation_info for flagged files.
    """
    if len(csv_list) < 3:
        return {}

    sizes = [s for _, _, s in csv_list]
    med = statistics.median(sizes)
    threshold = med * TRUNCATION_THRESHOLD

    flagged = {}
    for date_str, fpath, size in csv_list:
        if size < threshold:
            flagged[date_str] = {
                "file_size_bytes": size,
                "median_size_bytes": int(med),
                "ratio": round(size / med, 4),
                "verdict": "LIKELY TRUNCATED",
            }
    return flagged


def build_hdi_from_directory(directory, output_path=None, include_models=False,
                              date_filter=None, sample_every=1, quiet=False):
    """
    Directory mode: process YYYY-MM-DD.csv files sequentially.
    Starts from first date found, increments by 1 day, stops when next file missing.
    """
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f"ERROR: Not a directory: {directory}", file=sys.stderr)
        sys.exit(1)

    dir_name = os.path.basename(directory)
    if output_path is None:
        output_path = os.path.join(directory, f"{dir_name}.hdi.json")

    if not quiet:
        print(f"HUF Pre-Parser {PARSER_VERSION} — Directory Mode")
        print(f"Input: {directory}")

    # Discover all CSVs
    csv_list = discover_csv_dates(directory)
    if not csv_list:
        print("ERROR: No date-named CSV files found in directory", file=sys.stderr)
        sys.exit(1)

    # Filter to specific date if requested
    if date_filter:
        csv_list = [(d, p, s) for d, p, s in csv_list if d == date_filter]
        if not csv_list:
            print(f"ERROR: Date {date_filter} not found", file=sys.stderr)
            sys.exit(1)

    # Apply sampling
    if sample_every > 1:
        csv_list = csv_list[::sample_every]

    # Detect truncation
    all_csvs_for_truncation = discover_csv_dates(directory)  # full list for median
    truncated = detect_truncated(all_csvs_for_truncation)

    total_bytes = sum(s for _, _, s in csv_list)
    if not quiet:
        print(f"Found {len(csv_list)} CSV files to process "
              f"({total_bytes / 1024 / 1024 / 1024:.2f} GB)")
        if sample_every > 1:
            print(f"  Sampling: every {sample_every} day(s)")
        if truncated:
            print(f"  WARNING: {len(truncated)} file(s) flagged as potentially truncated:")
            for date_str, info in sorted(truncated.items()):
                print(f"    {date_str}.csv: {info['file_size_bytes']/1024/1024:.1f} MB "
                      f"(median: {info['median_size_bytes']/1024/1024:.1f} MB, "
                      f"ratio: {info['ratio']:.2%})")
        print()

    # Compute directory hash for provenance
    if not quiet:
        print("Computing directory hash...", end="", flush=True)
    dir_hash = compute_dir_hash([p for _, p, _ in all_csvs_for_truncation])
    if not quiet:
        print(f" {dir_hash[:16]}...")
        print()

    # Process each CSV sequentially
    snapshots = {}
    start_date = csv_list[0][0]
    end_date = csv_list[-1][0]
    processed = 0
    skipped_truncated = 0

    for date_str, fpath, fsize in csv_list:
        is_truncated = date_str in truncated

        if not quiet and is_truncated:
            print(f"  WARNING: {date_str} is likely truncated "
                  f"({fsize/1024/1024:.1f} MB vs ~{truncated[date_str]['median_size_bytes']/1024/1024:.0f} MB median)")

        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                snapshot = process_csv_stream(
                    f, date_str, include_models=include_models, quiet=quiet
                )

            # Add file metadata
            snapshot["source_file"] = os.path.basename(fpath)
            snapshot["source_file_size_bytes"] = fsize
            if is_truncated:
                snapshot["truncation_warning"] = truncated[date_str]

            snapshots[date_str] = snapshot
            processed += 1

        except Exception as e:
            if not quiet:
                print(f"  ERROR processing {date_str}: {e}")
            snapshots[date_str] = {"error": str(e), "source_file": os.path.basename(fpath)}

    # Check for gaps in the date sequence
    date_gaps = []
    if len(csv_list) > 1:
        all_found_dates = set(d for d, _, _ in all_csvs_for_truncation)
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        while current <= end:
            ds = current.strftime("%Y-%m-%d")
            if ds not in all_found_dates:
                date_gaps.append(ds)
            current += timedelta(days=1)

    # Build HDI document
    hdi = {
        "hdi_version": "2.0",
        "parser_version": PARSER_VERSION,
        "parse_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "huf_doc_id": "HUF.REL.CASE.DATA.BACKBLAZE_HDI",
        "mode": "directory",
        "source": {
            "name": "Backblaze Hard Drive Test Data",
            "url": "https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data",
            "directory": directory,
            "total_csv_files": len(all_csvs_for_truncation),
            "total_bytes": sum(s for _, _, s in all_csvs_for_truncation),
            "dir_hash": dir_hash,
        },
        "portfolio_definition": {
            label: {"key": config["key"], "description": config["description"]}
            for label, config in HUF_PORTFOLIO.items()
        },
        "data_quality": {
            "truncated_files": truncated if truncated else {},
            "date_gaps": date_gaps,
            "truncation_threshold": TRUNCATION_THRESHOLD,
            "total_files_flagged": len(truncated),
            "total_date_gaps": len(date_gaps),
        },
        "snapshots": snapshots,
        "summary": {
            "total_snapshots": len(snapshots),
            "processed": processed,
            "date_range": [start_date, end_date],
            "sample_interval": sample_every,
            "include_model_breakdown": include_models,
        },
    }

    # Write HDI
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(hdi, f, indent=2, ensure_ascii=False)

    output_size = os.path.getsize(output_path)
    if not quiet:
        print(f"\n{'='*60}")
        print(f"HDI output: {output_path}")
        print(f"  Size: {output_size:,} bytes ({output_size / 1024:.1f} KB)")
        print(f"  Reduction: {total_bytes / output_size:,.0f}x "
              f"({output_size / total_bytes * 100:.4f}% of source CSV data)")
        print(f"  Snapshots: {processed} processed")
        if truncated:
            print(f"  Truncated: {len(truncated)} file(s) flagged")
        if date_gaps:
            print(f"  Gaps: {len(date_gaps)} missing date(s)")
        print(f"\nDone. HDI file ready for upload to Claude or any HUF analysis environment.")

    return hdi


# ─────────────────────────────────────────────────────────
# ZIP MODE: Read from zip file (original v1.0 behavior)
# ─────────────────────────────────────────────────────────

def find_csv_entries_in_zip(zf):
    """Find all date-named CSV entries in a zip file."""
    entries = {}
    for info in zf.infolist():
        name = info.filename
        if name.endswith(".csv") and not name.startswith("__MACOSX"):
            basename = os.path.basename(name).replace(".csv", "")
            try:
                datetime.strptime(basename, "%Y-%m-%d")
                entries[basename] = info
            except ValueError:
                pass
    return entries


def build_hdi_from_zip(zip_path, output_path=None, include_models=False,
                        date_filter=None, sample_every=1, quiet=False):
    """
    Zip mode: read CSVs from zip without full extraction.
    """
    if not os.path.exists(zip_path):
        print(f"ERROR: File not found: {zip_path}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        output_path = zip_path.rsplit(".", 1)[0] + ".hdi.json"

    if not quiet:
        print(f"HUF Pre-Parser {PARSER_VERSION} — Zip Mode")
        print(f"Input: {zip_path} ({os.path.getsize(zip_path) / 1024 / 1024:.1f} MB)")
        print(f"Computing SHA-256...", end="", flush=True)

    source_hash = compute_sha256(zip_path)
    if not quiet:
        print(f" {source_hash[:16]}...")

    with zipfile.ZipFile(zip_path, "r") as zf:
        entries = find_csv_entries_in_zip(zf)
        if not entries:
            print("ERROR: No date-named CSV files found in zip", file=sys.stderr)
            sys.exit(1)

        sorted_dates = sorted(entries.keys())

        if date_filter:
            if date_filter in entries:
                sorted_dates = [date_filter]
            else:
                print(f"ERROR: Date {date_filter} not found. "
                      f"Available: {sorted_dates}", file=sys.stderr)
                sys.exit(1)

        if sample_every > 1:
            sorted_dates = sorted_dates[::sample_every]

        if not quiet:
            print(f"Found {len(sorted_dates)} CSV snapshot(s) to process")
            print()

        snapshots = {}
        for date_str in sorted_dates:
            entry = entries[date_str]
            with zf.open(entry) as f:
                text_stream = io.TextIOWrapper(f, encoding="utf-8", errors="replace")
                snapshots[date_str] = process_csv_stream(
                    text_stream, date_str,
                    include_models=include_models, quiet=quiet
                )

    hdi = {
        "hdi_version": "2.0",
        "parser_version": PARSER_VERSION,
        "parse_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "huf_doc_id": "HUF.REL.CASE.DATA.BACKBLAZE_HDI",
        "mode": "zip",
        "source": {
            "name": "Backblaze Hard Drive Test Data",
            "url": "https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data",
            "file": os.path.basename(zip_path),
            "file_size_bytes": os.path.getsize(zip_path),
            "sha256": source_hash,
        },
        "portfolio_definition": {
            label: {"key": config["key"], "description": config["description"]}
            for label, config in HUF_PORTFOLIO.items()
        },
        "snapshots": snapshots,
        "summary": {
            "total_snapshots": len(snapshots),
            "date_range": [sorted_dates[0], sorted_dates[-1]] if len(sorted_dates) > 1 else sorted_dates,
            "sample_interval": sample_every,
            "include_model_breakdown": include_models,
        },
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(hdi, f, indent=2, ensure_ascii=False)

    output_size = os.path.getsize(output_path)
    input_size = os.path.getsize(zip_path)
    if not quiet:
        print(f"\n{'='*60}")
        print(f"HDI output: {output_path}")
        print(f"  Size: {output_size:,} bytes ({output_size / 1024:.1f} KB)")
        print(f"  Reduction: {input_size / output_size:,.0f}x")
        print(f"  Snapshots: {len(snapshots)}")
        print(f"\nDone. HDI file ready for upload to Claude or any HUF analysis environment.")

    return hdi


# ─────────────────────────────────────────────────────────
# BATCH MODE: Process a folder of quarterly zip files
# ─────────────────────────────────────────────────────────

def discover_zip_files(directory):
    """
    Find all Backblaze quarterly zip files in a directory.
    Matches data_Q*.zip pattern, sorts chronologically.
    """
    zips = []
    for f in os.listdir(directory):
        if f.endswith(".zip") and f.startswith("data_Q"):
            fpath = os.path.join(directory, f)
            # Extract quarter info for sorting: data_Q1_2024.zip -> (2024, 1)
            parts = f.replace(".zip", "").split("_")  # ['data', 'Q1', '2024']
            try:
                quarter = int(parts[1].replace("Q", ""))
                year = int(parts[2])
                zips.append((year, quarter, f, fpath, os.path.getsize(fpath)))
            except (IndexError, ValueError):
                # Non-standard name, still include but sort by name
                zips.append((9999, 0, f, fpath, os.path.getsize(fpath)))
    zips.sort()
    return zips


def build_hdi_from_batch(directory, output_path=None, include_models=False,
                          date_filter=None, sample_every=1, first_of_month=False,
                          quiet=False):
    """
    Batch mode: process all data_Q*.zip files in a directory.
    Streams through each zip sequentially, combines into one HDI.
    """
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f"ERROR: Not a directory: {directory}", file=sys.stderr)
        sys.exit(1)

    zip_list = discover_zip_files(directory)
    if not zip_list:
        print(f"ERROR: No data_Q*.zip files found in {directory}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        suffix = "_weekly" if sample_every == 7 else "_monthly" if first_of_month else ""
        output_path = os.path.join(directory, f"backblaze_full{suffix}.hdi.json")

    total_zip_bytes = sum(size for _, _, _, _, size in zip_list)
    if not quiet:
        print(f"HUF Pre-Parser {PARSER_VERSION} — Batch Mode")
        print(f"Directory: {directory}")
        print(f"Found {len(zip_list)} quarterly zip files ({total_zip_bytes / 1024**3:.1f} GB):")
        for yr, qtr, fname, fpath, size in zip_list:
            print(f"  {fname:30s} {size / 1024**2:,.0f} MB")
        if sample_every > 1:
            print(f"Sampling: every {sample_every} day(s)")
        if first_of_month:
            print(f"Sampling: first of each month only")
        print()

    # Process each zip in order
    all_snapshots = {}
    all_source_files = []
    total_zips_processed = 0
    total_csvs_processed = 0
    batch_start_time = time.time()

    for yr, qtr, fname, fpath, fsize in zip_list:
        if not quiet:
            print(f"{'─'*60}")
            print(f"Processing {fname} ({fsize / 1024**2:,.0f} MB)...")

        try:
            with zipfile.ZipFile(fpath, "r") as zf:
                entries = find_csv_entries_in_zip(zf)
                if not entries:
                    if not quiet:
                        print(f"  WARNING: No date-named CSVs found, skipping")
                    continue

                sorted_dates = sorted(entries.keys())

                # Apply date filter
                if date_filter:
                    sorted_dates = [d for d in sorted_dates if d == date_filter]

                # Apply first-of-month filter
                if first_of_month:
                    sorted_dates = [d for d in sorted_dates
                                    if d.endswith("-01")]

                # Apply sampling
                if sample_every > 1:
                    sorted_dates = sorted_dates[::sample_every]

                if not quiet:
                    total_in_zip = len(entries)
                    print(f"  {total_in_zip} CSVs in zip, processing {len(sorted_dates)}")

                zip_processed = 0
                for date_str in sorted_dates:
                    entry = entries[date_str]
                    try:
                        with zf.open(entry) as f:
                            text_stream = io.TextIOWrapper(f, encoding="utf-8",
                                                           errors="replace")
                            snapshot = process_csv_stream(
                                text_stream, date_str,
                                include_models=include_models, quiet=quiet
                            )
                        snapshot["source_zip"] = fname
                        all_snapshots[date_str] = snapshot
                        zip_processed += 1
                        total_csvs_processed += 1
                    except Exception as e:
                        if not quiet:
                            print(f"  ERROR on {date_str}: {e}")
                        all_snapshots[date_str] = {
                            "error": str(e),
                            "source_zip": fname
                        }

                all_source_files.append({
                    "file": fname,
                    "size_bytes": fsize,
                    "total_csvs": len(entries),
                    "processed": zip_processed,
                    "date_range": [sorted(entries.keys())[0],
                                   sorted(entries.keys())[-1]],
                })
                total_zips_processed += 1

        except zipfile.BadZipFile:
            if not quiet:
                print(f"  ERROR: Bad zip file, skipping")
            all_source_files.append({
                "file": fname, "size_bytes": fsize, "error": "Bad zip file"
            })

    batch_elapsed = time.time() - batch_start_time

    if not all_snapshots:
        print("ERROR: No data processed from any zip file", file=sys.stderr)
        sys.exit(1)

    # Sort all snapshots chronologically
    sorted_all_dates = sorted(all_snapshots.keys())

    # Detect date gaps across the full range
    date_gaps = []
    if len(sorted_all_dates) > 1 and not first_of_month and sample_every == 1:
        start_dt = datetime.strptime(sorted_all_dates[0], "%Y-%m-%d")
        end_dt = datetime.strptime(sorted_all_dates[-1], "%Y-%m-%d")
        all_dates_set = set(sorted_all_dates)
        current = start_dt
        while current <= end_dt:
            ds = current.strftime("%Y-%m-%d")
            if ds not in all_dates_set:
                date_gaps.append(ds)
            current += timedelta(days=1)

    # Build HDI
    hdi = {
        "hdi_version": "3.0",
        "parser_version": PARSER_VERSION,
        "parse_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "huf_doc_id": "HUF.REL.CASE.DATA.BACKBLAZE_HDI",
        "mode": "batch",
        "source": {
            "name": "Backblaze Hard Drive Test Data",
            "url": "https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data",
            "directory": directory,
            "zip_files": all_source_files,
            "total_zip_files": len(zip_list),
            "total_zip_bytes": total_zip_bytes,
        },
        "portfolio_definition": {
            label: {"key": config["key"], "description": config["description"]}
            for label, config in HUF_PORTFOLIO.items()
        },
        "data_quality": {
            "date_gaps": date_gaps[:50] if len(date_gaps) > 50 else date_gaps,
            "total_date_gaps": len(date_gaps),
        },
        "snapshots": {d: all_snapshots[d] for d in sorted_all_dates},
        "summary": {
            "total_snapshots": total_csvs_processed,
            "total_zips_processed": total_zips_processed,
            "date_range": [sorted_all_dates[0], sorted_all_dates[-1]],
            "sample_interval": sample_every,
            "first_of_month": first_of_month,
            "include_model_breakdown": include_models,
            "processing_time_seconds": round(batch_elapsed, 1),
        },
    }

    # Write HDI
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(hdi, f, indent=2, ensure_ascii=False)

    output_size = os.path.getsize(output_path)
    if not quiet:
        print(f"\n{'='*60}")
        print(f"BATCH COMPLETE")
        print(f"{'='*60}")
        print(f"HDI output: {output_path}")
        print(f"  Size: {output_size:,} bytes ({output_size / 1024:.1f} KB)")
        print(f"  Reduction: {total_zip_bytes / output_size:,.0f}x "
              f"({output_size / total_zip_bytes * 100:.6f}% of source zips)")
        print(f"  Zips processed: {total_zips_processed} / {len(zip_list)}")
        print(f"  Snapshots: {total_csvs_processed}")
        print(f"  Date range: {sorted_all_dates[0]} to {sorted_all_dates[-1]}")
        if date_gaps:
            print(f"  Date gaps: {len(date_gaps)}")
        print(f"  Wall time: {batch_elapsed/60:.1f} minutes")
        print(f"\nDone. HDI file ready for upload to Claude or any HUF analysis environment.")

    return hdi


# ─────────────────────────────────────────────────────────
# MAIN ENTRY
# ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=(
            "HUF Pre-Parser v3: Convert Backblaze data (zip, directory, or batch of zips) "
            "to HUF Data Intermediate (HDI) format."
        ),
        epilog=(
            "EXAMPLES:\n"
            "  Batch (all zips):  python huf_preparser.py D:\\HUF_DATA\\BackBlaze\n"
            "  Batch weekly:      python huf_preparser.py D:\\HUF_DATA\\BackBlaze --sample 7\n"
            "  Batch monthly:     python huf_preparser.py D:\\HUF_DATA\\BackBlaze --first-of-month\n"
            "  Single zip:        python huf_preparser.py data_Q4_2025.zip\n"
            "  Directory of CSVs: python huf_preparser.py D:\\data_Q4_2025\\data_Q4_2025\n"
            "  One date:          python huf_preparser.py D:\\HUF_DATA\\BackBlaze --date 2025-10-01\n"
            "  With models:       python huf_preparser.py D:\\HUF_DATA\\BackBlaze --models --first-of-month\n"
            "\n"
            "BATCH MODE auto-detects when a directory contains data_Q*.zip files\n"
            "and processes them all sequentially into one combined HDI.\n"
            "\n"
            "Part of the Higgins Unity Framework (HUF) - compositional governance for real data."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input_path",
        help="Path to: a folder of data_Q*.zip files (batch), a single .zip, or a directory of CSVs"
    )
    parser.add_argument("-o", "--output", help="Output HDI file path (default: auto)")
    parser.add_argument("--models", action="store_true",
                        help="Include per-model breakdown (larger output)")
    parser.add_argument("--date", help="Process only this date (YYYY-MM-DD)")
    parser.add_argument("--sample", type=int, default=1,
                        help="Process every Nth day (e.g. --sample 7 for weekly)")
    parser.add_argument("--first-of-month", action="store_true",
                        help="Process only the 1st of each month (quick longitudinal view)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress progress output")

    args = parser.parse_args()

    input_path = args.input_path

    # Auto-detect mode
    if os.path.isdir(input_path):
        # Check if directory contains data_Q*.zip files -> batch mode
        has_zips = any(f.startswith("data_Q") and f.endswith(".zip")
                       for f in os.listdir(input_path))
        # Check if directory contains YYYY-MM-DD.csv files -> directory mode
        has_csvs = any(f.endswith(".csv") and len(f) == 14  # YYYY-MM-DD.csv
                       for f in os.listdir(input_path))

        if has_zips:
            build_hdi_from_batch(
                input_path,
                output_path=args.output,
                include_models=args.models,
                date_filter=args.date,
                sample_every=args.sample,
                first_of_month=args.first_of_month,
                quiet=args.quiet,
            )
        elif has_csvs:
            build_hdi_from_directory(
                input_path,
                output_path=args.output,
                include_models=args.models,
                date_filter=args.date,
                sample_every=args.sample,
                quiet=args.quiet,
            )
        else:
            print(f"ERROR: '{input_path}' contains no data_Q*.zip or YYYY-MM-DD.csv files",
                  file=sys.stderr)
            sys.exit(1)

    elif os.path.isfile(input_path) and input_path.lower().endswith(".zip"):
        build_hdi_from_zip(
            input_path,
            output_path=args.output,
            include_models=args.models,
            date_filter=args.date,
            sample_every=args.sample,
            quiet=args.quiet,
        )
    else:
        print(f"ERROR: '{input_path}' is not a directory or .zip file", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
