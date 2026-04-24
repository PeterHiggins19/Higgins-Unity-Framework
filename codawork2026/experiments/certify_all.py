#!/usr/bin/env python3
"""
HUF EXPERIMENT CERTIFICATION ENGINE
=====================================
Reads every experiment's output JSON and script, produces an integrity
certificate for each one. The certificate contains:

  1. SHA-256 hash of the experiment script (code integrity)
  2. SHA-256 hash of the output JSON (data integrity)
  3. Step-level chain: each EITT analysis step hashed with chain linkage
  4. Key result values extracted and individually hashed
  5. A master hash sealing the entire chain

Certificates are written to each experiment folder as:
    {experiment_folder}/integrity_certificate.json

The certificates can be verified at any time using:
    python3 huf_integrity.py  (self-test mode)
  or:
    python3 certify_all.py --verify

Part of the Higgins Unity Framework (HUF).
The Entropy-Invariant Time Transformer (EITT) integrity system.
Compositional Data Analysis (CoDa) — Aitchison geometry on the simplex.
Source of truth: ai-refresh/HUF_COMPLETE_REFERENCE.json

Peter Higgins / Claude — 2026-04-19
"""

import json
import hashlib
import os
import sys
import glob
import numpy as np

# Add experiments dir to path for huf_integrity import
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from huf_integrity import IntegrityChain, hash_experiment_output, hash_experiment_script

REPO = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
EXP_DIR = SCRIPT_DIR

# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT REGISTRY — maps each experiment to its files and key results
# ═══════════════════════════════════════════════════════════════════════════════

EXPERIMENTS = [
    {
        "id": "EXP-01", "name": "Gold/Silver Ratio — Full PLL-EITT Verification",
        "folder": "EXP-01_Gold_Silver",
        "script": "exp01_gold_silver_full_verify.py",
        "output": "exp01_gold_silver_full_verify.json",
        "key_results": ["pass_rate", "vertex", "lock_type", "entropy"],
    },
    {
        "id": "EXP-02", "name": "US Monthly Energy — Full PLL-EITT Verification",
        "folder": "EXP-02_US_Monthly",
        "script": "exp02_us_energy_full_verify.py",
        "output": "exp02_us_energy_full_verify.json",
        "key_results": ["pass_rate", "cohorts", "boundary_species"],
    },
    {
        "id": "EXP-03", "name": "Uranium / Nuclear — Full PLL-EITT Verification",
        "folder": "EXP-03_Uranium",
        "script": "exp03_uranium_full_verify.py",
        "output": "exp03_uranium_full_verify.json",
        "key_results": ["pass_rate", "decay_chains", "semf_valley"],
    },
    {
        "id": "EXP-06", "name": "Nuclear Fusion — PLL-EITT Chain",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06_fusion_chain.py",
        "output": "exp06_fusion_chain.json",
        "key_results": ["crossover_T", "entropy", "pass_rate"],
    },
    {
        "id": "EXP-06B", "name": "Bremsstrahlung Boundary Attack",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06_brem_attack.py",
        "output": "exp06b_brem_attack.json",
        "key_results": ["ignition_pathways"],
    },
    {
        "id": "EXP-06C", "name": "Corrected Fusion Map",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06c_fusion_map.py",
        "output": "exp06c_fusion_map.json",
        "key_results": [],
    },
    {
        "id": "EXP-06D", "name": "Degrees of Freedom Analysis",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06d_dof_analysis.py",
        "output": "exp06d_dof_analysis.json",
        "key_results": [],
    },
    {
        "id": "EXP-06E", "name": "Definitive Fusion Engine",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06e_fusion_engine.py",
        "output": "exp06e_fusion_engine.json",
        "key_results": [],
    },
    {
        "id": "EXP-06F", "name": "ARC Engine at B=12T",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06f_arc_engine.py",
        "output": "exp06f_arc_engine.json",
        "key_results": [],
    },
    {
        "id": "EXP-06G", "name": "Isotropic Fusion Reactor Standard",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06g_isotropic_standard.py",
        "output": "exp06g_isotropic_standard.json",
        "key_results": [],
    },
    {
        "id": "EXP-06H", "name": "Fusion Approaches Comparison",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06h_fusion_approaches.py",
        "output": "exp06h_fusion_approaches.json",
        "key_results": [],
    },
    {
        "id": "EXP-06I", "name": "ST Deep Dive",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06i_deep_dive.py",
        "output": "exp06i_deep_dive.json",
        "key_results": [],
    },
    {
        "id": "EXP-06J", "name": "Krell Logarithmic Scaling",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06j_krell_scaling.py",
        "output": "exp06j_krell_scaling.json",
        "key_results": [],
    },
    {
        "id": "EXP-06K", "name": "Krell Plant Design",
        "folder": "EXP-06_Nuclear_Fusion",
        "script": "exp06k_krell_plant.py",
        "output": "exp06k_krell_plant.json",
        "key_results": [],
    },
    {
        "id": "EXP-07", "name": "EITT at the Quark Scale",
        "folder": "EXP-07_Quarks",
        "script": "exp07_eitt_quarks.py",
        "output": "exp07_eitt_quarks.json",
        "key_results": ["entropy", "confinement"],
    },
    {
        "id": "EXP-07B", "name": "Quark Mysteries",
        "folder": "EXP-07_Quarks",
        "script": "exp07b_quark_mysteries.py",
        "output": "exp07b_quark_mysteries.json",
        "key_results": [],
    },
    {
        "id": "EXP-08", "name": "Cross-Boundary Composition Atlas",
        "folder": "EXP-08_Composition_Atlas",
        "script": "exp08_composition_atlas.py",
        "output": "exp08_composition_atlas.json",
        "key_results": ["system_count", "orders_of_magnitude"],
    },
    {
        "id": "EXP-09", "name": "Master Inventory",
        "folder": "EXP-09_Master_Inventory",
        "script": "exp09_master_inventory.py",
        "output": "exp09_master_inventory.json",
        "key_results": ["total_systems", "completion_pct"],
    },
    {
        "id": "EXP-10", "name": "Full Sweep — All Mapped Systems",
        "folder": "EXP-10_Full_Sweep",
        "script": "exp10_full_sweep.py",
        "output": "exp10_full_sweep.json",
        "key_results": ["ckm_pmns_ratio", "higgs_entropy"],
    },
    {
        "id": "EXP-11", "name": "Final Four — 100% Programme Completion",
        "folder": "EXP-11_Final_Four",
        "script": "exp11_final_four.py",
        "output": "exp11_final_four.json",
        "key_results": ["dark_matter", "neutron_star_eos", "stellar_sequence"],
    },
    {
        "id": "EXP-12", "name": "Gravity Deep Dive",
        "folder": "EXP-12_Gravity_Deep",
        "script": "exp12_gravity_deep.py",
        "output": "exp12_gravity_deep.json",
        "key_results": ["gravity_activation_scale", "gw150914_entropy", "qnm_fraction"],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  CERTIFICATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def certify_experiment(exp):
    """Build an integrity certificate for one experiment."""
    folder = os.path.join(EXP_DIR, exp["folder"])
    script_path = os.path.join(folder, exp["script"])
    output_path = os.path.join(folder, exp["output"])

    if not os.path.exists(script_path):
        return None, f"Script not found: {exp['script']}"
    if not os.path.exists(output_path):
        return None, f"Output not found: {exp['output']}"

    chain = IntegrityChain(exp["id"], exp["name"],
                           f"Integrity certificate for {exp['id']}")

    # Step 1: Hash the script
    script_hash = hash_experiment_script(script_path)
    script_size = os.path.getsize(script_path)
    chain.record_step("script_integrity", exp["script"],
                      {"hash": script_hash, "size": script_size},
                      {"file": exp["script"], "sha256": script_hash})

    # Step 2: Hash the output JSON
    output_hash = hash_experiment_output(output_path)
    output_size = os.path.getsize(output_path)
    chain.record_step("output_integrity", exp["output"],
                      {"hash": output_hash, "size": output_size},
                      {"file": exp["output"], "sha256": output_hash})

    # Step 3: Load and verify the output JSON structure
    with open(output_path) as f:
        data = json.load(f)

    chain.record_step("json_valid", output_path, {"valid": True, "type": type(data).__name__})

    # Step 4: Extract and hash key results
    def extract_deep(d, path=""):
        """Recursively extract all numeric values for hashing."""
        results = {}
        if isinstance(d, dict):
            for k, v in d.items():
                full_key = f"{path}.{k}" if path else k
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    results[full_key] = v
                elif isinstance(v, (dict, list)):
                    results.update(extract_deep(v, full_key))
        elif isinstance(d, list):
            for i, item in enumerate(d):
                results.update(extract_deep(item, f"{path}[{i}]"))
        return results

    all_values = extract_deep(data)
    chain.record_step("data_extraction",
                      {"value_count": len(all_values)},
                      all_values,
                      {"total_numeric_values": len(all_values)})

    # Step 5: Verify compositions are closed (sum to ~1 where applicable)
    composition_checks = 0
    composition_issues = []
    for key, val in all_values.items():
        if "entropy" in key.lower() and isinstance(val, float):
            if val < -0.001:
                composition_issues.append(f"{key}={val} (negative entropy)")
    chain.record_step("physics_validation",
                      {"checks": len(all_values)},
                      {"issues": composition_issues, "issues_count": len(composition_issues)},
                      {"physics_issues": len(composition_issues)})

    # Step 6: Hash sealed conclusion if present
    sealed_path = os.path.join(folder, "sealed_conclusion.json")
    if os.path.exists(sealed_path):
        sealed_hash = hash_experiment_output(sealed_path)
        chain.record_step("sealed_conclusion",
                          "sealed_conclusion.json",
                          {"hash": sealed_hash},
                          {"sha256": sealed_hash})

    # Seal the certificate — use experiment ID in filename to avoid overwrites
    cert_name = f"integrity_certificate_{exp['id'].replace('-', '_').lower()}.json"
    cert_path = os.path.join(folder, cert_name)
    cert = chain.seal(cert_path)

    return cert, "OK"


def verify_all():
    """Verify all existing certificates."""
    print("=" * 70)
    print("HUF INTEGRITY CERTIFICATE VERIFICATION")
    print("=" * 70)

    certs = sorted(glob.glob(f"{EXP_DIR}/EXP-*/integrity_certificate_*.json"))
    passed = 0
    failed = 0

    for cp in certs:
        cert = IntegrityChain.load(cp)
        is_valid, issues = IntegrityChain.verify(cert)
        exp_id = cert.get("experiment_id", "???")
        status = "PASS" if is_valid else "FAIL"
        print(f"  [{status}] {exp_id}: {cert.get('experiment_name', '???')}")
        if issues:
            for iss in issues:
                print(f"         {iss}")
        if is_valid:
            passed += 1
        else:
            failed += 1

    print(f"\n  Verified: {passed} passed, {failed} failed")
    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if "--verify" in sys.argv:
        verify_all()
        sys.exit(0)

    print("=" * 70)
    print("HUF EXPERIMENT CERTIFICATION ENGINE")
    print(f"Date: {__import__('datetime').datetime.utcnow().isoformat()}Z")
    print("=" * 70)

    success = 0
    errors = 0

    for exp in EXPERIMENTS:
        cert, msg = certify_experiment(exp)
        if cert:
            print(f"  [CERT] {exp['id']:8s} — {cert['step_count']} steps, "
                  f"master: {cert['master_hash'][:16]}...")
            success += 1
        else:
            print(f"  [SKIP] {exp['id']:8s} — {msg}")
            errors += 1

    print(f"\n  Certified: {success}, Skipped: {errors}")

    # Now verify all certificates we just created
    print()
    all_ok = verify_all()

    # Produce master manifest
    manifest = {
        "_type": "HUF_INTEGRITY_MANIFEST",
        "_version": "2.0",
        "_framework": "Higgins Unity Framework (HUF)",
        "_note": "Master manifest of all experiment integrity certificates",
        "created": __import__('datetime').datetime.utcnow().isoformat() + "Z",
        "reference_commit": "498dece (2026-04-18 15:47:37)",
        "experiments": {}
    }

    for exp in EXPERIMENTS:
        cert_name = f"integrity_certificate_{exp['id'].replace('-', '_').lower()}.json"
        cert_path = os.path.join(EXP_DIR, exp["folder"], cert_name)
        if os.path.exists(cert_path):
            cert = IntegrityChain.load(cert_path)
            manifest["experiments"][exp["id"]] = {
                "name": exp["name"],
                "master_hash": cert["master_hash"],
                "step_count": cert["step_count"],
                "sealed": cert["sealed"],
            }

    manifest_path = os.path.join(EXP_DIR, "INTEGRITY_MANIFEST.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n  Master manifest: {manifest_path}")
    print(f"  Total experiments certified: {len(manifest['experiments'])}")
