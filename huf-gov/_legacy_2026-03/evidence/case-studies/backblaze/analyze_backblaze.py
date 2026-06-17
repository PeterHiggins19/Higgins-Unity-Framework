"""
HUF K=4 Real Data Analysis — Backblaze Enterprise HDD Statistics
Computes ρᵢ values and MDG from actual SMART attribute data.
"""
import csv
import sys
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = "backblaze_hdd_data/2025-01-01_huf_k4.csv"

# Counters
total_drives = 0
total_failures = 0

# SMART anomaly counts (across entire fleet)
fleet_smart5 = 0    # Reallocated Sectors (Mechanical)
fleet_smart187 = 0  # Uncorrectable Errors (Electronic)
fleet_smart197 = 0  # Current Pending Sectors (Media)
fleet_smart198 = 0  # Offline Uncorrectable

# Failure mode classification (among failure=1 drives only)
fail_mechanical = 0   # smart_5_raw > 0
fail_electronic = 0   # smart_187_raw > 0
fail_media = 0        # smart_197_raw > 0
fail_sudden = 0       # no SMART warning
fail_multi = 0        # multiple indicators (for reporting)

print("=" * 70)
print("HUF K=4 REAL DATA ANALYSIS — Backblaze Q1 2025")
print("=" * 70)
print(f"\nReading: {DATA_FILE}")

# Read header to find column indices
with open(DATA_FILE, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    idx = {col: i for i, col in enumerate(header)}
    fail_idx = idx['failure']
    s5_idx = idx['smart_5_raw']
    s187_idx = idx['smart_187_raw']
    s197_idx = idx['smart_197_raw']
    s198_idx = idx['smart_198_raw']

    print(f"Columns: failure={fail_idx}, smart_5_raw={s5_idx}, "
          f"smart_187_raw={s187_idx}, smart_197_raw={s197_idx}, smart_198_raw={s198_idx}")
    print("\nProcessing rows...")

    for row in reader:
        total_drives += 1

        # Parse values (empty = 0)
        def val(i):
            v = row[i].strip() if i < len(row) else ''
            if v == '' or v == 'NA':
                return 0
            try:
                return float(v)
            except ValueError:
                return 0

        failure = int(val(fail_idx))
        s5 = val(s5_idx)
        s187 = val(s187_idx)
        s197 = val(s197_idx)
        s198 = val(s198_idx)

        # Fleet-wide SMART anomaly counts
        if s5 > 0:
            fleet_smart5 += 1
        if s187 > 0:
            fleet_smart187 += 1
        if s197 > 0:
            fleet_smart197 += 1
        if s198 > 0:
            fleet_smart198 += 1

        # Failure mode classification
        if failure == 1:
            total_failures += 1
            has_s5 = s5 > 0
            has_s187 = s187 > 0
            has_s197 = s197 > 0
            indicators = sum([has_s5, has_s187, has_s197])

            if indicators > 1:
                fail_multi += 1

            if indicators == 0:
                fail_sudden += 1
            elif has_s5:
                fail_mechanical += 1
            elif has_s187:
                fail_electronic += 1
            elif has_s197:
                fail_media += 1

print(f"\n{'=' * 70}")
print(f"FLEET OVERVIEW — {DATA_FILE}")
print(f"{'=' * 70}")
print(f"Total drives monitored:     {total_drives:>10,}")
print(f"Total failures (failure=1): {total_failures:>10,}")
print(f"Annualized failure rate:    {total_failures/total_drives*365*100:>10.2f}%")

print(f"\n{'─' * 70}")
print(f"FLEET-WIDE SMART ANOMALY COUNTS (all drives, not just failed)")
print(f"{'─' * 70}")
print(f"SMART 5  > 0 (Reallocated Sectors):  {fleet_smart5:>8,}  ({fleet_smart5/total_drives*100:.3f}%)")
print(f"SMART 187 > 0 (Uncorrectable Errors):{fleet_smart187:>8,}  ({fleet_smart187/total_drives*100:.3f}%)")
print(f"SMART 197 > 0 (Current Pending):     {fleet_smart197:>8,}  ({fleet_smart197/total_drives*100:.3f}%)")
print(f"SMART 198 > 0 (Offline Uncorrectable):{fleet_smart198:>8,}  ({fleet_smart198/total_drives*100:.3f}%)")

print(f"\n{'─' * 70}")
print(f"FAILURE MODE CLASSIFICATION (among {total_failures} failed drives)")
print(f"{'─' * 70}")

if total_failures == 0:
    print("No failures found on this day — cannot compute failure-mode ρᵢ.")
    print("Falling back to fleet-wide SMART anomaly proportions for ρᵢ.\n")

    # Use fleet anomaly proportions instead
    total_anomalies = fleet_smart5 + fleet_smart187 + fleet_smart197
    # Estimate "sudden" as drives with failure=1 and no SMART flags — but no failures
    # Use published proportions for sudden as fallback
    print("Using fleet SMART anomaly proportions (Mechanical/Electronic/Media)")
    if total_anomalies > 0:
        r1 = fleet_smart5 / total_anomalies
        r2 = fleet_smart187 / total_anomalies
        r3 = fleet_smart197 / total_anomalies
        print(f"  Mechanical (SMART 5):   {r1:.4f}")
        print(f"  Electronic (SMART 187): {r2:.4f}")
        print(f"  Media (SMART 197):      {r3:.4f}")
        print(f"  (Sudden cannot be estimated from fleet anomalies alone)")
else:
    print(f"Mechanical  (SMART 5 > 0):   {fail_mechanical:>4}  ({fail_mechanical/total_failures*100:.1f}%)")
    print(f"Electronic  (SMART 187 > 0): {fail_electronic:>4}  ({fail_electronic/total_failures*100:.1f}%)")
    print(f"Media       (SMART 197 > 0): {fail_media:>4}  ({fail_media/total_failures*100:.1f}%)")
    print(f"Sudden      (no warning):    {fail_sudden:>4}  ({fail_sudden/total_failures*100:.1f}%)")
    print(f"Multi-indicator overlap:     {fail_multi:>4}  ({fail_multi/total_failures*100:.1f}%)")

# Compute ρ values from fleet-wide SMART anomaly distribution
# This gives the compositional "attention budget" across the fleet
print(f"\n{'=' * 70}")
print(f"HUF K=4 COMPOSITIONAL ANALYSIS")
print(f"{'=' * 70}")

# Method: proportion of SMART-anomalous drives across 4 categories
# For "Sudden" estimation: use ratio of (failures with no SMART flag) to total
# If no failures, estimate from published ~12% of failures being sudden
total_flagged = fleet_smart5 + fleet_smart187 + fleet_smart197 + fleet_smart198

print(f"\nFLEET ANOMALY METHOD (all drives with elevated SMART values):")
print(f"Total drives with any key SMART anomaly: {total_flagged:,}")

if total_flagged > 0:
    rho_mech = fleet_smart5 / total_flagged
    rho_elec = fleet_smart187 / total_flagged
    rho_media = fleet_smart197 / total_flagged
    rho_offline = fleet_smart198 / total_flagged
    print(f"  ρ₁ Mechanical (SMART 5):    {rho_mech:.4f}  (ref 0.25, Δ = {rho_mech-0.25:+.4f})")
    print(f"  ρ₂ Electronic (SMART 187):  {rho_elec:.4f}  (ref 0.25, Δ = {rho_elec-0.25:+.4f})")
    print(f"  ρ₃ Media (SMART 197):       {rho_media:.4f}  (ref 0.25, Δ = {rho_media-0.25:+.4f})")
    print(f"  ρ₄ Offline (SMART 198):     {rho_offline:.4f}  (ref 0.25, Δ = {rho_offline-0.25:+.4f})")
    total_rho = rho_mech + rho_elec + rho_media + rho_offline
    print(f"  Σρᵢ = {total_rho:.4f}  (closure check)")

    # MDG
    mdg = (abs(rho_mech - 0.25) + abs(rho_elec - 0.25) +
           abs(rho_media - 0.25) + abs(rho_offline - 0.25)) / 4
    mdg_bps = mdg * 10000
    print(f"\n  MDG = Σ|Δρᵢ| / K = {mdg:.4f}")
    print(f"  MDG in basis points: {mdg_bps:.1f} bps")

    # Thresholds (K=4)
    print(f"\n  {'Threshold':<20} {'bps':>10}  {'Status'}")
    print(f"  {'─'*50}")
    print(f"  {'Advisory (3σ)':<20} {'58':>10}  {'EXCEEDED' if mdg_bps > 58 else 'OK'}")
    print(f"  {'Alert (5σ)':<20} {'96':>10}  {'EXCEEDED' if mdg_bps > 96 else 'OK'}")
    print(f"  {'Critical (10σ)':<20} {'193':>10}  {'EXCEEDED' if mdg_bps > 193 else 'OK'}")
    print(f"  {'OBSERVED MDG':<20} {mdg_bps:>10.1f}  ", end="")
    if mdg_bps > 193:
        print("STATUS: CRITICAL")
    elif mdg_bps > 96:
        print("STATUS: ALERT")
    elif mdg_bps > 58:
        print("STATUS: ADVISORY")
    else:
        print("STATUS: NORMAL")

# If we have failures, also compute from failure modes
if total_failures > 0:
    print(f"\nFAILURE MODE METHOD (among failed drives only, K=4):")
    f_total = fail_mechanical + fail_electronic + fail_media + fail_sudden
    if f_total > 0:
        r1 = fail_mechanical / f_total
        r2 = fail_electronic / f_total
        r3 = fail_media / f_total
        r4 = fail_sudden / f_total
        print(f"  ρ₁ Mechanical: {r1:.4f}  (Δ = {r1-0.25:+.4f})")
        print(f"  ρ₂ Electronic: {r2:.4f}  (Δ = {r2-0.25:+.4f})")
        print(f"  ρ₃ Media:      {r3:.4f}  (Δ = {r3-0.25:+.4f})")
        print(f"  ρ₄ Sudden:     {r4:.4f}  (Δ = {r4-0.25:+.4f})")
        mdg2 = (abs(r1-0.25) + abs(r2-0.25) + abs(r3-0.25) + abs(r4-0.25)) / 4
        print(f"  MDG = {mdg2:.4f} = {mdg2*10000:.1f} bps")

# Compare to estimated values
print(f"\n{'=' * 70}")
print(f"COMPARISON: ESTIMATED vs REAL")
print(f"{'=' * 70}")
est = {"Mechanical": 0.41, "Electronic": 0.36, "Media": 0.11, "Sudden": 0.12}
print(f"  {'Node':<15} {'Estimated':>10} {'Real (fleet)':>12} {'Δ':>10}")
print(f"  {'─'*50}")
if total_flagged > 0:
    real = {"Mechanical": rho_mech, "Electronic": rho_elec, "Media": rho_media, "Sudden": rho_offline}
    for k in est:
        rk = real.get(k, 0)
        print(f"  {k:<15} {est[k]:>10.4f} {rk:>12.4f} {rk-est[k]:>+10.4f}")
    print(f"\n  Estimated MDG: 1,350.0 bps")
    print(f"  Real MDG:      {mdg_bps:.1f} bps")
    sig = "SIGNIFICANTLY DIFFERENT" if abs(mdg_bps - 1350) > 100 else "CONSISTENT"
    print(f"  Assessment:    {sig}")

print(f"\n{'=' * 70}")
print("Analysis complete.")
