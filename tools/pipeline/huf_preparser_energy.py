#!/usr/bin/env python3
"""
HUF Pre-Parser: Energy v1.0.0
==============================
Reads the Our World in Data (OWID) / Ember energy dataset and outputs
HUF Data Intermediate (HDI) JSON files for electricity generation portfolios.

Any country's electricity generation mix is a finite-budget system:
total generation = sum of generation by source. This is the unity constraint.
HUF treats each energy source as a portfolio element with weight rho_i.

DATA SOURCE:
  Our World in Data — owid-energy-data.csv
  License: CC-BY-4.0
  Download: https://github.com/owid/energy-data
  Direct:   https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv

USAGE — TWO MODES:

  1. DOWNLOAD MODE (auto-fetches the CSV):
     python huf_preparser_energy.py --download
     python huf_preparser_energy.py --download --country "United Kingdom" --years 2000-2024
     python huf_preparser_energy.py --download --country "Croatia" --years 1990-2024

  2. LOCAL MODE (use a pre-downloaded CSV):
     python huf_preparser_energy.py owid-energy-data.csv
     python huf_preparser_energy.py owid-energy-data.csv --country "Germany" --years 2010-2024
     python huf_preparser_energy.py owid-energy-data.csv --list-countries

OPTIONS:
  --country NAME     Process one country (default: all countries)
  --countries A,B,C  Process multiple countries (comma-separated)
  --years START-END  Year range (e.g., 2000-2024; default: all available)
  --k6               Use K=6 portfolio: Coal, Gas, Nuclear, Hydro, Wind, Solar (default)
  --k8               Use K=8 portfolio: adds Oil and Bioenergy
  --list-countries   Print all available country names and exit
  --output, -o       Output HDI file path (default: auto)
  --quiet, -q        Suppress progress output

HUF Document ID: HUF.SOFTWARE.TOOL.PREPARSER_ENERGY.v1.0.0
Status: draft | OCC: OP=0.51 TOOL=0.49

Author: Claude (Session 6) for Peter Higgins / HUF Collective
License: Same as HUF project
"""

import argparse
import csv
import hashlib
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Try to import urllib for download mode
try:
    import urllib.request
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False

# === HUF ENERGY PORTFOLIO CONFIGURATIONS ===

# K=6: The six major electricity generation sources
PORTFOLIO_K6 = {
    "Coal": {
        "key": "coal_electricity",
        "description": "Electricity from coal combustion (TWh)",
    },
    "Gas": {
        "key": "gas_electricity",
        "description": "Electricity from natural gas combustion (TWh)",
    },
    "Nuclear": {
        "key": "nuclear_electricity",
        "description": "Electricity from nuclear fission (TWh)",
    },
    "Hydro": {
        "key": "hydro_electricity",
        "description": "Electricity from hydroelectric generation (TWh)",
    },
    "Wind": {
        "key": "wind_electricity",
        "description": "Electricity from wind generation (TWh)",
    },
    "Solar": {
        "key": "solar_electricity",
        "description": "Electricity from solar generation (TWh)",
    },
}

# K=8: Adds Oil and Bioenergy
PORTFOLIO_K8 = {
    **PORTFOLIO_K6,
    "Oil": {
        "key": "oil_electricity",
        "description": "Electricity from oil combustion (TWh)",
    },
    "Bioenergy": {
        "key": "biofuel_electricity",
        "description": "Electricity from biofuel/bioenergy sources (TWh)",
    },
}

PARSER_VERSION = "huf-preparser-energy-1.0.0"
OWID_CSV_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
OWID_GITHUB_URL = "https://github.com/owid/energy-data"


def compute_sha256(filepath):
    """Compute SHA-256 hash for provenance."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def download_owid_csv(output_dir="."):
    """Download the OWID energy CSV to a local directory."""
    if not HAS_URLLIB:
        print("ERROR: urllib not available. Download the CSV manually from:", file=sys.stderr)
        print(f"  {OWID_CSV_URL}", file=sys.stderr)
        sys.exit(1)

    output_path = os.path.join(output_dir, "owid-energy-data.csv")
    print(f"Downloading OWID energy data...")
    print(f"  URL: {OWID_CSV_URL}")
    print(f"  Saving to: {output_path}")

    try:
        urllib.request.urlretrieve(OWID_CSV_URL, output_path)
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"  Downloaded: {size_mb:.1f} MB")
        return output_path
    except Exception as e:
        print(f"ERROR downloading: {e}", file=sys.stderr)
        print(f"Download manually from: {OWID_CSV_URL}", file=sys.stderr)
        sys.exit(1)


def read_energy_csv(csv_path, portfolio, country_filter=None, year_start=None,
                    year_end=None, quiet=False):
    """
    Read the OWID energy CSV and extract portfolio data.
    Returns dict of {country: {year: snapshot_data}}.
    """
    if not quiet:
        print(f"Reading {csv_path}...")

    start = time.time()
    country_data = defaultdict(dict)
    rows_read = 0
    rows_used = 0
    countries_seen = set()

    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)

        # Validate columns exist
        fieldnames = reader.fieldnames or []
        required = ["country", "year"] + [p["key"] for p in portfolio.values()]
        missing = [k for k in required if k not in fieldnames]
        if missing:
            # Try alternative column names
            alt_missing = []
            for m in missing:
                if m == "country" and "entity" in fieldnames:
                    continue  # OWID sometimes uses 'entity'
                alt_missing.append(m)
            if alt_missing:
                print(f"WARNING: CSV missing columns: {alt_missing}", file=sys.stderr)
                print(f"Available columns (first 30): {fieldnames[:30]}", file=sys.stderr)

        for row in reader:
            rows_read += 1

            # Get country — OWID uses 'country' column
            country = row.get("country", row.get("entity", "")).strip()
            if not country:
                continue

            countries_seen.add(country)

            # Apply country filter
            if country_filter and country not in country_filter:
                continue

            # Get year
            try:
                year = int(row.get("year", "0"))
            except (ValueError, TypeError):
                continue

            # Apply year filter
            if year_start and year < year_start:
                continue
            if year_end and year > year_end:
                continue

            # Extract generation values
            generation = {}
            total = 0
            has_data = False

            for label, config in portfolio.items():
                key = config["key"]
                val_str = row.get(key, "").strip()
                try:
                    val = float(val_str) if val_str else 0.0
                except (ValueError, TypeError):
                    val = 0.0
                # Treat negative values as zero (some datasets use -1 for missing)
                if val < 0:
                    val = 0.0
                generation[label] = val
                total += val
                if val > 0:
                    has_data = True

            # Skip rows with no electricity data
            if not has_data or total <= 0:
                continue

            # Compute compositional weights
            K = len(portfolio)
            rho = {label: round(gen / total, 6) for label, gen in generation.items()}

            # MDG vs neutral
            neutral = 1.0 / K
            mdg_bps = round(sum(abs(rho[label] - neutral) for label in portfolio) * 10000)

            # Leverage
            leverage = {
                label: round(1.0 / rho[label], 4) if rho[label] > 0 else float("inf")
                for label in portfolio
            }

            # PROOF line: minimum elements to reach 80% of total
            sorted_rho = sorted(rho.values(), reverse=True)
            cumsum = 0
            proof_line = 0
            for val in sorted_rho:
                cumsum += val
                proof_line += 1
                if cumsum >= 0.80:
                    break

            # Governance thresholds
            thresholds = {
                "advisory_bps": round(58 * K / 4),   # Scale thresholds by K
                "alert_bps": round(96 * K / 4),
                "critical_bps": round(193 * K / 4),
            }
            if mdg_bps > thresholds["critical_bps"]:
                governance_status = "CRITICAL"
            elif mdg_bps > thresholds["alert_bps"]:
                governance_status = "ALERT"
            elif mdg_bps > thresholds["advisory_bps"]:
                governance_status = "ADVISORY"
            else:
                governance_status = "NOMINAL"

            # Detect dominant source and orphan candidates
            dominant = max(rho, key=rho.get)
            orphans = [label for label, r in rho.items() if 0 < r < 0.02]

            country_data[country][year] = {
                "year": year,
                "total_generation_twh": round(total, 3),
                "K": K,
                "generation_twh": {label: round(g, 3) for label, g in generation.items()},
                "rho": rho,
                "leverage": leverage,
                "mdg_bps": mdg_bps,
                "proof_line": proof_line,
                "governance_status": governance_status,
                "dominant_source": dominant,
                "dominant_share_pct": round(rho[dominant] * 100, 1),
                "orphan_candidates": orphans,
                "thresholds": thresholds,
            }
            rows_used += 1

    elapsed = time.time() - start
    if not quiet:
        print(f"  Read {rows_read:,} rows in {elapsed:.1f}s")
        print(f"  {rows_used:,} data points across {len(country_data)} countries")
        print(f"  Total countries in dataset: {len(countries_seen)}")

    return country_data, countries_seen


def compute_drift_analysis(snapshots):
    """
    Compute year-over-year drift for a country's time series.
    Returns drift metrics for each consecutive year pair.
    """
    years = sorted(snapshots.keys())
    if len(years) < 2:
        return {}

    drift_series = {}
    for i in range(1, len(years)):
        prev_year = years[i - 1]
        curr_year = years[i]
        prev = snapshots[prev_year]["rho"]
        curr = snapshots[curr_year]["rho"]

        # Year-over-year drift per element
        element_drift = {}
        total_drift = 0
        for label in prev:
            delta = curr.get(label, 0) - prev.get(label, 0)
            element_drift[label] = round(delta * 10000)  # basis points
            total_drift += abs(delta)

        drift_series[curr_year] = {
            "from_year": prev_year,
            "element_drift_bps": element_drift,
            "total_drift_bps": round(total_drift * 10000),
            "largest_gainer": max(element_drift, key=element_drift.get),
            "largest_loser": min(element_drift, key=element_drift.get),
        }

    return drift_series


def build_hdi(csv_path, portfolio, country_filter=None, year_start=None,
              year_end=None, output_path=None, quiet=False):
    """
    Main entry: read CSV, compute governance diagnostics, output HDI JSON.
    """
    portfolio_name = f"K={len(portfolio)}"
    if output_path is None:
        if country_filter and len(country_filter) == 1:
            safe_name = list(country_filter)[0].replace(" ", "_").replace("/", "_")
            output_path = os.path.join(
                os.path.dirname(csv_path) or ".",
                f"energy_hdi_{safe_name}_{portfolio_name}.json"
            )
        else:
            output_path = os.path.join(
                os.path.dirname(csv_path) or ".",
                f"energy_hdi_all_{portfolio_name}.json"
            )

    if not quiet:
        print(f"HUF Pre-Parser: Energy {PARSER_VERSION}")
        print(f"Portfolio: {portfolio_name} ({', '.join(portfolio.keys())})")
        if country_filter:
            print(f"Countries: {', '.join(sorted(country_filter))}")
        if year_start or year_end:
            print(f"Years: {year_start or 'earliest'}-{year_end or 'latest'}")
        print()

    # Compute source hash
    if not quiet:
        print("Computing SHA-256...", end="", flush=True)
    source_hash = compute_sha256(csv_path)
    if not quiet:
        print(f" {source_hash[:16]}...")
        print()

    # Read data
    country_data, all_countries = read_energy_csv(
        csv_path, portfolio, country_filter, year_start, year_end, quiet
    )

    if not country_data:
        print("ERROR: No data found matching filters", file=sys.stderr)
        sys.exit(1)

    # Build country entries with drift analysis
    countries_output = {}
    for country in sorted(country_data.keys()):
        snapshots = country_data[country]
        drift = compute_drift_analysis(snapshots)

        # Summary stats
        years = sorted(snapshots.keys())
        latest = snapshots[years[-1]]
        earliest = snapshots[years[0]]

        # Long-term drift (first vs last year)
        if len(years) >= 2:
            long_drift = {}
            for label in portfolio:
                delta = latest["rho"].get(label, 0) - earliest["rho"].get(label, 0)
                long_drift[label] = round(delta * 10000)
        else:
            long_drift = None

        countries_output[country] = {
            "years_available": len(years),
            "year_range": [years[0], years[-1]],
            "latest_total_twh": latest["total_generation_twh"],
            "latest_rho": latest["rho"],
            "latest_governance_status": latest["governance_status"],
            "latest_mdg_bps": latest["mdg_bps"],
            "latest_proof_line": latest["proof_line"],
            "latest_dominant_source": latest["dominant_source"],
            "latest_dominant_share_pct": latest["dominant_share_pct"],
            "latest_orphan_candidates": latest["orphan_candidates"],
            "long_term_drift_bps": long_drift,
            "snapshots": {str(y): s for y, s in sorted(snapshots.items())},
            "drift_series": {str(y): d for y, d in sorted(drift.items())},
        }

        if not quiet:
            # Print summary for each country
            status = latest["governance_status"]
            dom = latest["dominant_source"]
            dom_pct = latest["dominant_share_pct"]
            mdg = latest["mdg_bps"]
            orphans = latest["orphan_candidates"]
            print(f"  {country}: {len(years)} years ({years[0]}-{years[-1]}), "
                  f"latest={latest['total_generation_twh']:.0f} TWh, "
                  f"dominant={dom} ({dom_pct}%), "
                  f"MDG={mdg} bps [{status}]"
                  f"{f', orphans: {orphans}' if orphans else ''}")

    # Build HDI
    hdi = {
        "hdi_version": "2.0",
        "parser_version": PARSER_VERSION,
        "parse_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "huf_doc_id": "HUF.REL.CASE.DATA.ENERGY_HDI",
        "mode": "energy",
        "source": {
            "name": "Our World in Data — Energy Dataset (Ember + IEA + IRENA)",
            "url": OWID_GITHUB_URL,
            "download_url": OWID_CSV_URL,
            "license": "CC-BY-4.0",
            "file": os.path.basename(csv_path),
            "file_size_bytes": os.path.getsize(csv_path),
            "sha256": source_hash,
        },
        "portfolio_definition": {
            label: {"key": config["key"], "description": config["description"]}
            for label, config in portfolio.items()
        },
        "countries": countries_output,
        "summary": {
            "total_countries": len(countries_output),
            "portfolio_size": len(portfolio),
            "portfolio_name": portfolio_name,
            "year_filter": [year_start, year_end],
            "country_filter": sorted(country_filter) if country_filter else None,
        },
    }

    # Write HDI
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(hdi, f, indent=2, ensure_ascii=False)

    output_size = os.path.getsize(output_path)
    input_size = os.path.getsize(csv_path)

    if not quiet:
        print(f"\n{'='*60}")
        print(f"HDI output: {output_path}")
        print(f"  Size: {output_size:,} bytes ({output_size / 1024:.1f} KB)")
        print(f"  Reduction: {input_size / output_size:,.1f}x "
              f"({output_size / input_size * 100:.2f}% of source)")
        print(f"  Countries: {len(countries_output)}")
        total_snapshots = sum(c["years_available"] for c in countries_output.values())
        print(f"  Total year-snapshots: {total_snapshots}")
        print(f"\nDone. HDI file ready for upload to Claude or any HUF analysis environment.")

    return hdi


def list_countries(csv_path):
    """Print all unique country names in the dataset."""
    countries = set()
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            country = row.get("country", row.get("entity", "")).strip()
            if country:
                countries.add(country)
    for c in sorted(countries):
        print(c)
    print(f"\nTotal: {len(countries)} countries/regions")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "HUF Pre-Parser: Energy — Convert OWID energy data to "
            "HUF Data Intermediate (HDI) format for electricity generation portfolios."
        ),
        epilog=(
            "EXAMPLES:\n"
            "  Download and process:  python huf_preparser_energy.py --download\n"
            "  Single country:        python huf_preparser_energy.py owid-energy-data.csv --country \"United Kingdom\" --years 2000-2024\n"
            "  Multiple countries:    python huf_preparser_energy.py owid-energy-data.csv --countries \"Germany,France,Poland\" --years 2010-2024\n"
            "  Croatia for Ramsar:    python huf_preparser_energy.py owid-energy-data.csv --country \"Croatia\" --years 1990-2024\n"
            "  Full 8-source portfolio: python huf_preparser_energy.py owid-energy-data.csv --country \"China\" --k8\n"
            "  List countries:        python huf_preparser_energy.py owid-energy-data.csv --list-countries\n"
            "\n"
            "DATA SOURCE: Our World in Data / Ember (CC-BY-4.0)\n"
            "Download: https://github.com/owid/energy-data\n"
            "\n"
            "Part of the Higgins Unity Framework (HUF) - compositional governance for real data."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input_csv", nargs="?", default=None,
        help="Path to owid-energy-data.csv (or use --download)"
    )
    parser.add_argument("--download", action="store_true",
                        help="Auto-download the OWID energy CSV before processing")
    parser.add_argument("--country", help="Process one country (exact name)")
    parser.add_argument("--countries",
                        help="Process multiple countries (comma-separated)")
    parser.add_argument("--years",
                        help="Year range: START-END (e.g., 2000-2024)")
    parser.add_argument("--k6", action="store_true", default=True,
                        help="K=6 portfolio: Coal, Gas, Nuclear, Hydro, Wind, Solar (default)")
    parser.add_argument("--k8", action="store_true",
                        help="K=8 portfolio: adds Oil and Bioenergy")
    parser.add_argument("--list-countries", action="store_true",
                        help="List all country names in the dataset and exit")
    parser.add_argument("-o", "--output", help="Output HDI file path (default: auto)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress progress output")

    args = parser.parse_args()

    # Handle download mode
    csv_path = args.input_csv
    if args.download:
        csv_path = download_owid_csv(".")
    elif csv_path is None:
        # Check if owid-energy-data.csv exists in current directory
        if os.path.exists("owid-energy-data.csv"):
            csv_path = "owid-energy-data.csv"
        else:
            print("ERROR: No input CSV specified. Either:", file=sys.stderr)
            print("  1. Provide path:  python huf_preparser_energy.py owid-energy-data.csv", file=sys.stderr)
            print("  2. Auto-download: python huf_preparser_energy.py --download", file=sys.stderr)
            print(f"  3. Download manually from: {OWID_CSV_URL}", file=sys.stderr)
            sys.exit(1)

    if not os.path.exists(csv_path):
        print(f"ERROR: File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    # List countries mode
    if args.list_countries:
        list_countries(csv_path)
        return

    # Select portfolio
    portfolio = PORTFOLIO_K8 if args.k8 else PORTFOLIO_K6

    # Parse country filter
    country_filter = None
    if args.country:
        country_filter = {args.country}
    elif args.countries:
        country_filter = {c.strip() for c in args.countries.split(",")}

    # Parse year range
    year_start = None
    year_end = None
    if args.years:
        parts = args.years.split("-")
        if len(parts) == 2:
            year_start = int(parts[0])
            year_end = int(parts[1])
        elif len(parts) == 1:
            year_start = year_end = int(parts[0])

    build_hdi(
        csv_path, portfolio,
        country_filter=country_filter,
        year_start=year_start,
        year_end=year_end,
        output_path=args.output,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    main()
