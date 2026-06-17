#!/usr/bin/env python3
"""
Hˢ DIAGNOSTIC CODE SYSTEM
===========================
Lightweight code generation for the Higgins Decomposition pipeline.
The pipeline emits structured codes; a separate reporter reads them.

Code Format: SS-CCC-LLL
  SS  = Stage (2 chars): pipeline step or extended test
  CCC = Condition (3 chars): what was detected
  LLL = Level (3 chars): severity / information class

Stages:
  GD = Guard (input validation)
  S4 = Step 4 (simplex closure)
  S5 = Step 5 (CLR transform)
  S6 = Step 6 (Aitchison variance)
  S7 = Step 7 (HVLD vertex lock)
  S8 = Step 8 (super squeeze)
  S9 = Step 9 (EITT entropy)
  SA = Step 10 (ternary projection)
  SB = Step 11 (complex plane)
  SC = Step 12 (helix/polar)
  XU = Extended universal panel
  XC = Extended conditional panel
  RP = Report summary

Levels:
  INF = Information (normal operation)
  WRN = Warning (attention needed)
  ERR = Error (operation failed or invalid)
  DIS = Discovery (noteworthy finding)
  CAL = Calibration (instrument calibration signal)

Author: Peter Higgins / Claude
Version: 1.0
"""

# ════════════════════════════════════════════════════════════
# CODE DICTIONARY
# ════════════════════════════════════════════════════════════

CODE_DICTIONARY = {
    # ── GUARDS ──
    "GD-D2M-ERR": {"short": "D < 2", "verbose": "Input rejected: D must be >= 2. The simplex requires at least 2 compositional parts."},
    "GD-N5M-ERR": {"short": "N < 5", "verbose": "Input rejected: N must be >= 5. The variance trajectory needs at least 3 non-zero points for a meaningful HVLD fit."},
    "GD-NAN-ERR": {"short": "NaN detected", "verbose": "Input rejected: data contains NaN values. Clean or impute before decomposition."},
    "GD-INF-ERR": {"short": "Inf detected", "verbose": "Input rejected: data contains Inf values. Check for division by zero or overflow."},
    "GD-SCL-ERR": {"short": "Scale disparity", "verbose": "Input rejected: max/min ratio exceeds 1e15. Normalise or partition before decomposition."},
    "GD-ALL-INF": {"short": "All guards pass", "verbose": "All 4 input guards passed. Data is valid for Hˢ pipeline processing."},

    # ── STEP 4: CLOSURE ──
    "S4-CLO-INF": {"short": "Closure OK", "verbose": "Simplex closure successful. All rows sum to 1.0 within tolerance 1e-12."},
    "S4-ZRP-INF": {"short": "Zero replacement", "verbose": "Multiplicative zero replacement applied. ZERO_DELTA = 1e-6."},
    "S4-ZRN-INF": {"short": "No zeros", "verbose": "No zero replacement needed. All input values are positive."},

    # ── STEP 5: CLR ──
    "S5-CLR-INF": {"short": "CLR complete", "verbose": "Centred log-ratio transform applied. All rows sum to zero in CLR space."},

    # ── STEP 6: VARIANCE ──
    "S6-VAR-INF": {"short": "Variance computed", "verbose": "Cumulative Aitchison variance trajectory σ²_A(t) computed for all time indices."},
    "S6-ZRO-WRN": {"short": "Zero variance", "verbose": "σ²_A is zero or near-zero. Data may be constant or degenerate."},
    "S6-RNG-INF": {"short": "Variance range", "verbose": "Variance trajectory range and final value recorded."},

    # ── STEP 7: HVLD ──
    "S7-BWL-INF": {"short": "HVLD bowl", "verbose": "HVLD vertex lock: bowl shape (a > 0). Variance is accelerating — system integrating."},
    "S7-HIL-INF": {"short": "HVLD hill", "verbose": "HVLD vertex lock: hill shape (a < 0). Variance is decelerating — system segregating."},
    "S7-HRQ-INF": {"short": "HVLD R² high", "verbose": "HVLD R² > 0.8. Quadratic fit describes the trajectory well."},
    "S7-LRQ-WRN": {"short": "HVLD R² low", "verbose": "HVLD R² < 0.5. Quadratic fit is poor — trajectory may be non-polynomial."},
    "S7-VTX-INF": {"short": "Vertex location", "verbose": "HVLD vertex (lock point) location recorded."},

    # ── STEP 8: SQUEEZE ──
    "S8-NAT-INF": {"short": "NATURAL", "verbose": "HTP classification: NATURAL. At least one transcendental match within δ < 1%."},
    "S8-INV-WRN": {"short": "INVESTIGATE", "verbose": "HTP classification: INVESTIGATE. Nearest match δ between 1% and 5%. Consider alternate decomposition."},
    "S8-FLG-WRN": {"short": "FLAG", "verbose": "HTP classification: FLAG. No match within 5%. System may be synthetic, adversarial, or improperly decomposed."},
    "S8-EUL-DIS": {"short": "Euler-family match", "verbose": "Nearest constant is from the Euler family (2π, e^π, π^e, or their reciprocals). Pipeline geometry resonates with system structure."},
    "S8-SQZ-INF": {"short": "Squeeze count", "verbose": "Number of transcendental proximity matches recorded."},
    "S8-TGT-DIS": {"short": "Tight match", "verbose": "Transcendental match tighter than δ < 0.001. Precision-level structural resonance."},

    # ── STEP 9: EITT ──
    "S9-ENT-INF": {"short": "Entropy computed", "verbose": "Shannon entropy H(t) computed for all observations. Normalised by H_max = ln(D)."},
    "S9-EIT-INF": {"short": "EITT pass", "verbose": "EITT invariance test passed at all tested compression ratios (variation < 5%)."},
    "S9-EIF-WRN": {"short": "EITT fail", "verbose": "EITT invariance test failed at one or more compression ratios."},
    "S9-CHS-INF": {"short": "Chaos low", "verbose": "Chaos detection: few deviations. System is compositionally smooth."},
    "S9-CHH-DIS": {"short": "Chaos high", "verbose": "Chaos detection: many deviations. System exhibits compositional turbulence — stalls, spikes, or reversals."},
    "S9-STL-DIS": {"short": "Stalls detected", "verbose": "Angular velocity stalls detected — entropy rate dropped below 15% of running mean."},
    "S9-SPK-DIS": {"short": "Spikes detected", "verbose": "Angular velocity spikes detected — entropy rate exceeded 3.5× running mean."},
    "S9-REV-DIS": {"short": "Reversals detected", "verbose": "Entropy reversals detected — ≥2 sign changes in 5 consecutive samples."},

    # ── STEPS 10-12: GEOMETRY ──
    "SA-TRN-INF": {"short": "Ternary OK", "verbose": "Ternary projection computed. Type: ternary (D=3), 1-simplex (D=2), or projected (D>3)."},
    "SB-CPX-INF": {"short": "Complex plane OK", "verbose": "Complex plane mapping computed. Centroid-relative coordinates."},
    "SC-HLX-INF": {"short": "Helix OK", "verbose": "3D helix/polar embedding computed. Radius, angle, angular velocity."},

    # ── EXTENDED UNIVERSAL ──
    "XU-PCC-INF": {"short": "Carrier decomposition", "verbose": "Per-carrier contribution computed. Shows which carrier drives the variance."},
    "XU-PCD-DIS": {"short": "Carrier dominance", "verbose": "One carrier contributes >60% of total variance. Strong structural signal."},
    "XU-MDN-INF": {"short": "Match density natural", "verbose": "Match density consistent with natural system (density >> synthetic baseline)."},
    "XU-MDS-CAL": {"short": "Match density low", "verbose": "Match density below natural baseline. May indicate synthetic data or sparse constant coverage."},
    "XU-DRI-INF": {"short": "Drift stable", "verbose": "Carrier drift trend: stable. Second half compositionally similar to first half."},
    "XU-DRU-DIS": {"short": "Drift increasing", "verbose": "Carrier drift trend: increasing. System is evolving — second half more dispersed."},
    "XU-DRD-DIS": {"short": "Drift decreasing", "verbose": "Carrier drift trend: decreasing. System is converging — second half more concentrated."},
    "XU-CDA-INF": {"short": "CoDa panel OK", "verbose": "CoDa structural panel computed: variation matrix, CLR summary, Aitchison distance."},
    "XU-CLM-INF": {"short": "Claim summary", "verbose": "Claim-status and envelope summary generated."},

    # ── EXTENDED CONDITIONAL ──
    "XC-PID-INF": {"short": "PID computed", "verbose": "Partial Information Decomposition computed. Redundant, unique, and synergistic carrier interactions quantified."},
    "XC-PIR-DIS": {"short": "PID redundancy", "verbose": "PID dominant mode: redundancy. Carriers share information — coupled dynamics."},
    "XC-PIU-DIS": {"short": "PID unique", "verbose": "PID dominant mode: unique. One carrier contributes information the others cannot — independent dynamics."},
    "XC-TEE-INF": {"short": "Transfer entropy", "verbose": "Transfer entropy matrix computed. Directed information flow between carriers quantified."},
    "XC-TEF-DIS": {"short": "TE dominant flow", "verbose": "Dominant directed information flow identified. One carrier informationally predicts another."},
    "XC-TEZ-CAL": {"short": "TE zero", "verbose": "Transfer entropy is zero across all pairs. System is compositionally memoryless at this aggregation level."},
    "XC-ORD-INF": {"short": "Order matters", "verbose": "Order sensitivity test: temporal/parametric order significantly affects the variance trajectory."},
    "XC-ORN-INF": {"short": "Order neutral", "verbose": "Order sensitivity test: shuffling order does not change the result. Structure is cross-sectional."},
    "XC-RPL-INF": {"short": "Ratio-pair lattice", "verbose": "Ratio-pair lattice computed. All pairwise log-ratios ranked by stability (CV)."},
    "XC-RPS-DIS": {"short": "Stable ratio found", "verbose": "A highly stable pairwise ratio detected (CV < 20%). These carriers are compositionally locked."},
    "XC-RPV-DIS": {"short": "Volatile ratio", "verbose": "A highly volatile pairwise ratio detected (CV > 50%). These carriers are compositionally independent."},
    "XC-ZCR-DIS": {"short": "Zero crossings", "verbose": "Carrier zero-crossing events detected. Compositions approaching simplex boundary — structural singularities."},

    # ── REPORT ──
    "RP-CMP-INF": {"short": "Run complete", "verbose": "Hˢ extended pipeline run completed successfully. All results available for reporting."},
    "RP-DTM-INF": {"short": "Deterministic", "verbose": "Pipeline is deterministic. Repeated runs on identical data produce bit-identical results."},
    "RP-VER-INF": {"short": "Version", "verbose": "Pipeline version and configuration recorded."},
}


def generate_codes(result):
    """Generate diagnostic codes from an Hˢ pipeline result dict.
    
    Parameters
    ----------
    result : dict
        Output from HigginsDecomposition.run_full_extended()
    
    Returns
    -------
    list of dict, each with: code, short, verbose, value (optional)
    """
    codes = []
    
    def emit(code, value=None):
        entry = CODE_DICTIONARY.get(code, {"short": code, "verbose": "Unknown code"})
        codes.append({"code": code, "short": entry["short"], "verbose": entry["verbose"], "value": value})
    
    s = result.get('steps', {})
    ext = result.get('extended', {})
    u = ext.get('universal', {})
    c = ext.get('conditional', {})
    
    # Guards
    emit("GD-ALL-INF")
    
    # Closure
    if s.get('step3_zero_replacement_applied'):
        emit("S4-ZRP-INF")
    else:
        emit("S4-ZRN-INF")
    emit("S4-CLO-INF", s.get('step3_closure_check'))
    
    # CLR
    emit("S5-CLR-INF")
    
    # Variance
    sig_final = s.get('step5_sigma2_final', 0)
    emit("S6-VAR-INF", sig_final)
    if sig_final < 1e-10:
        emit("S6-ZRO-WRN")
    emit("S6-RNG-INF", s.get('step5_sigma2_range'))
    
    # HVLD
    shape = s.get('step6_pll_shape', 'unknown')
    r2 = s.get('step6_pll_R2', 0)
    if shape == 'bowl':
        emit("S7-BWL-INF", r2)
    else:
        emit("S7-HIL-INF", r2)
    if r2 > 0.8:
        emit("S7-HRQ-INF", r2)
    elif r2 < 0.5:
        emit("S7-LRQ-WRN", r2)
    emit("S7-VTX-INF", s.get('step6_vertex'))
    
    # Squeeze
    sq = s.get('step7_squeeze_closest')
    if sq:
        delta = sq.get('delta', 999)
        const = sq.get('constant', '')
        if delta < 0.01:
            emit("S8-NAT-INF", {"constant": const, "delta": delta})
        elif delta < 0.05:
            emit("S8-INV-WRN", {"constant": const, "delta": delta})
        else:
            emit("S8-FLG-WRN", {"constant": const, "delta": delta})
        
        euler_family = ['2pi', 'e^pi', 'pi^e', '1/(2pi)', '1/(e^pi)', '1/(pi^e)']
        if const in euler_family:
            emit("S8-EUL-DIS", {"constant": const, "delta": delta})
        
        if delta < 0.001:
            emit("S8-TGT-DIS", {"constant": const, "delta": delta})
    else:
        emit("S8-FLG-WRN")
    
    emit("S8-SQZ-INF", s.get('step7_squeeze_count', 0))
    
    # EITT
    emit("S9-ENT-INF", s.get('step8_entropy_mean'))
    eitt = s.get('step8_eitt_invariance', {})
    all_pass = all(v.get('pass', False) for v in eitt.values()) if eitt else False
    if all_pass:
        emit("S9-EIT-INF")
    elif eitt:
        emit("S9-EIF-WRN")
    
    chaos = s.get('step9_chaos_detection', {})
    total_dev = chaos.get('total_deviations', 0)
    if total_dev < 10:
        emit("S9-CHS-INF", total_dev)
    else:
        emit("S9-CHH-DIS", total_dev)
    if chaos.get('stalls', 0) > 0:
        emit("S9-STL-DIS", chaos['stalls'])
    if chaos.get('spikes', 0) > 0:
        emit("S9-SPK-DIS", chaos['spikes'])
    if chaos.get('reversals', 0) > 0:
        emit("S9-REV-DIS", chaos['reversals'])
    
    # Geometry
    emit("SA-TRN-INF")
    emit("SB-CPX-INF")
    emit("SC-HLX-INF")
    
    # Extended universal
    if u:
        pcc = u.get('per_carrier_contribution', {})
        emit("XU-PCC-INF", pcc)
        if pcc.get('dominant_pct', 0) > 60:
            emit("XU-PCD-DIS", {"carrier": pcc.get('dominant_carrier'), "pct": pcc.get('dominant_pct')})
        
        md = u.get('match_density', {})
        if md.get('density', 0) > 10:
            emit("XU-MDN-INF", md)
        else:
            emit("XU-MDS-CAL", md)
        
        drift = u.get('carrier_drift', {})
        direction = drift.get('drift_direction', 'stable')
        if direction == 'stable':
            emit("XU-DRI-INF", drift)
        elif direction == 'increasing':
            emit("XU-DRU-DIS", drift)
        else:
            emit("XU-DRD-DIS", drift)
        
        emit("XU-CDA-INF")
        emit("XU-CLM-INF")
    
    # Extended conditional
    if c.get('PID'):
        pid = c['PID']
        emit("XC-PID-INF", pid)
        if pid.get('dominant') == 'redundancy':
            emit("XC-PIR-DIS")
        else:
            emit("XC-PIU-DIS")
    
    if c.get('transfer_entropy'):
        te = c['transfer_entropy']
        emit("XC-TEE-INF")
        if te.get('dominant_te', 0) > 0.001:
            emit("XC-TEF-DIS", {"flow": te.get('dominant_flow'), "te": te.get('dominant_te')})
        else:
            emit("XC-TEZ-CAL")
    
    if c.get('order_sensitivity'):
        os_r = c['order_sensitivity']
        if os_r.get('order_matters'):
            emit("XC-ORD-INF", os_r)
        else:
            emit("XC-ORN-INF", os_r)
    
    if c.get('ratio_pair_lattice'):
        rpl = c['ratio_pair_lattice']
        emit("XC-RPL-INF", rpl)
        # Check for very stable or volatile pairs
        for pname, pdata in rpl.get('pairs', {}).items():
            if pdata.get('cv', 100) < 20:
                emit("XC-RPS-DIS", {"pair": pname, "cv": pdata['cv']})
            if pdata.get('cv', 0) > 50:
                emit("XC-RPV-DIS", {"pair": pname, "cv": pdata['cv']})
    
    if c.get('zero_crossing'):
        emit("XC-ZCR-DIS", c['zero_crossing'])
    
    # Report
    emit("RP-CMP-INF")
    emit("RP-DTM-INF")
    emit("RP-VER-INF", result.get('pipeline_version'))
    
    return codes


def codes_to_summary(codes):
    """Generate a human-readable summary from diagnostic codes."""
    lines = []
    lines.append("Hˢ DIAGNOSTIC CODE REPORT")
    lines.append("=" * 60)
    
    errors = [c for c in codes if c['code'].endswith('-ERR')]
    warnings = [c for c in codes if c['code'].endswith('-WRN')]
    discoveries = [c for c in codes if c['code'].endswith('-DIS')]
    calibrations = [c for c in codes if c['code'].endswith('-CAL')]
    infos = [c for c in codes if c['code'].endswith('-INF')]
    
    lines.append(f"\nTotal codes: {len(codes)}")
    lines.append(f"  Errors:       {len(errors)}")
    lines.append(f"  Warnings:     {len(warnings)}")
    lines.append(f"  Discoveries:  {len(discoveries)}")
    lines.append(f"  Calibrations: {len(calibrations)}")
    lines.append(f"  Information:  {len(infos)}")
    
    if errors:
        lines.append("\n── ERRORS ──")
        for c in errors:
            lines.append(f"  [{c['code']}] {c['verbose']}")
    
    if warnings:
        lines.append("\n── WARNINGS ──")
        for c in warnings:
            lines.append(f"  [{c['code']}] {c['short']}")
    
    if discoveries:
        lines.append("\n── DISCOVERIES ──")
        for c in discoveries:
            val = f" → {c['value']}" if c['value'] else ""
            lines.append(f"  [{c['code']}] {c['short']}{val}")
    
    if calibrations:
        lines.append("\n── CALIBRATION SIGNALS ──")
        for c in calibrations:
            lines.append(f"  [{c['code']}] {c['short']}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print(f"Hˢ Diagnostic Code System v1.0")
    print(f"Total defined codes: {len(CODE_DICTIONARY)}")
    print(f"Stages: GD, S4-SC, XU, XC, RP")
    print(f"Levels: INF, WRN, ERR, DIS, CAL")
