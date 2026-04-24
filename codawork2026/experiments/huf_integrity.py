#!/usr/bin/env python3
"""
HUF EXPERIMENT INTEGRITY MODULE
=================================
The Entropy-Invariant Time Transformer (EITT) step-level integrity system.

Purpose: Provide tamper-evident audit trails for every EITT analysis.
Each step in the Higgins Decomposition produces a cryptographic hash
of its inputs and outputs. The chain of hashes forms a Merkle-like
structure — if any step's data changes, the chain breaks.

Usage in experiments:
    from huf_integrity import IntegrityChain
    chain = IntegrityChain("EXP-XX", "experiment_name")
    chain.record_step("closure", input_data, output_data)
    chain.record_step("clr_transform", input_data, output_data)
    ...
    chain.seal()  # Writes the integrity certificate

Verification:
    chain = IntegrityChain.load("path/to/certificate.json")
    chain.verify()  # Returns True if chain is intact

Part of the Higgins Unity Framework (HUF).
Compositional Data Analysis (CoDa) — Aitchison geometry on the simplex.
Source of truth: ai-refresh/HUF_COMPLETE_REFERENCE.json

Peter Higgins / Claude — 2026-04-19
"""

import hashlib
import json
import numpy as np
import time
import os
from datetime import datetime


class IntegrityChain:
    """
    EITT Step-Level Integrity Chain
    ================================
    Records a cryptographic hash at each step of the Higgins Decomposition
    (the 10-step operational process line of the Higgins Unity Framework).

    The chain uses SHA-256 hashes. Each step's hash includes:
      - The step name
      - A fingerprint of the input data
      - A fingerprint of the output data
      - The previous step's hash (chain linkage)

    This creates a Merkle-like chain where any alteration to any step
    invalidates all subsequent hashes.

    The final seal includes:
      - The complete chain of step hashes
      - A master hash (hash of all step hashes concatenated)
      - Metadata: experiment ID, timestamp, system count
      - A verification function that can be called independently

    Terminology (from HUF_COMPLETE_REFERENCE.json):
      EITT  = Entropy-Invariant Time Transformer
      CoDa  = Compositional Data Analysis
      CLR   = Centred Log-Ratio transform
      CIP   = Compositional Integrity Protocol (6 immutable rules)
      HUF-GOV = open-loop observation layer
    """

    def __init__(self, experiment_id, experiment_name, description=""):
        self.experiment_id = experiment_id
        self.experiment_name = experiment_name
        self.description = description
        self.steps = []
        self.sealed = False
        self.created = datetime.utcnow().isoformat() + "Z"

    @staticmethod
    def _fingerprint(data):
        """
        Compute a deterministic fingerprint of arbitrary data.

        For numpy arrays: round to 10 decimal places to ensure
        cross-platform reproducibility, then hash the string representation.

        For dicts/lists: JSON-serialize with sorted keys.
        For scalars: convert to string.
        """
        if isinstance(data, np.ndarray):
            # Round to avoid floating-point platform differences
            rounded = np.round(data, decimals=10)
            canonical = rounded.tobytes()
            return hashlib.sha256(canonical).hexdigest()
        elif isinstance(data, (dict, list)):
            canonical = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
            return hashlib.sha256(canonical).hexdigest()
        elif isinstance(data, (int, float)):
            canonical = f"{data:.10g}".encode('utf-8')
            return hashlib.sha256(canonical).hexdigest()
        elif isinstance(data, str):
            return hashlib.sha256(data.encode('utf-8')).hexdigest()
        elif data is None:
            return hashlib.sha256(b"__NONE__").hexdigest()
        else:
            canonical = str(data).encode('utf-8')
            return hashlib.sha256(canonical).hexdigest()

    def record_step(self, step_name, input_data, output_data, metadata=None):
        """
        Record one step in the EITT analysis chain.

        Parameters
        ----------
        step_name : str
            Name of this step (e.g., "simplex_closure", "clr_transform",
            "shannon_entropy", "geometric_mean_decimation", "pll_analysis").

        input_data : any
            The input to this step (composition, time series, parameters).
            Will be fingerprinted via SHA-256.

        output_data : any
            The output of this step. Will be fingerprinted via SHA-256.

        metadata : dict, optional
            Additional metadata for this step (e.g., D=parts count,
            N=observations, pass_rate, vertex_location).
        """
        if self.sealed:
            raise RuntimeError("Chain is sealed — cannot add more steps")

        input_hash = self._fingerprint(input_data)
        output_hash = self._fingerprint(output_data)

        # Chain linkage: include previous step's hash
        prev_hash = self.steps[-1]["step_hash"] if self.steps else "GENESIS"

        # Compute step hash = H(step_name + input_hash + output_hash + prev_hash)
        chain_input = f"{step_name}|{input_hash}|{output_hash}|{prev_hash}"
        step_hash = hashlib.sha256(chain_input.encode('utf-8')).hexdigest()

        step_record = {
            "step_number": len(self.steps) + 1,
            "step_name": step_name,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "prev_hash": prev_hash,
            "step_hash": step_hash,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        if metadata:
            step_record["metadata"] = metadata

        self.steps.append(step_record)
        return step_hash

    def record_result(self, key, value, description=""):
        """
        Record a named result (e.g., a canonical value like H/Hmax or sigma²_A).
        This is a convenience for recording outputs that should be verifiable.
        """
        return self.record_step(
            f"result:{key}",
            {"key": key, "description": description},
            value,
            metadata={"result_key": key, "result_description": description}
        )

    def seal(self, output_path=None):
        """
        Seal the chain — compute master hash and write certificate.

        The master hash is SHA-256 of all step hashes concatenated.
        Once sealed, no more steps can be added.

        Parameters
        ----------
        output_path : str, optional
            Path to write the certificate JSON. If None, returns the
            certificate dict without writing.

        Returns
        -------
        dict : The integrity certificate.
        """
        if not self.steps:
            raise RuntimeError("Cannot seal empty chain")

        # Master hash = H(step_hash_1 + step_hash_2 + ... + step_hash_N)
        all_hashes = "".join(s["step_hash"] for s in self.steps)
        master_hash = hashlib.sha256(all_hashes.encode('utf-8')).hexdigest()

        certificate = {
            "_type": "HUF_INTEGRITY_CERTIFICATE",
            "_version": "1.0",
            "_framework": "Higgins Unity Framework (HUF)",
            "_method": "Entropy-Invariant Time Transformer (EITT)",
            "_reference": "ai-refresh/HUF_COMPLETE_REFERENCE.json",
            "experiment_id": self.experiment_id,
            "experiment_name": self.experiment_name,
            "description": self.description,
            "created": self.created,
            "sealed": datetime.utcnow().isoformat() + "Z",
            "step_count": len(self.steps),
            "master_hash": master_hash,
            "chain": self.steps,
            "verification_instructions": (
                "To verify this certificate: load the chain, recompute each "
                "step_hash from (step_name + input_hash + output_hash + prev_hash), "
                "then verify master_hash = SHA-256(concat(all step_hashes)). "
                "Any mismatch indicates data alteration."
            ),
        }

        self.sealed = True

        if output_path:
            with open(output_path, 'w') as f:
                json.dump(certificate, f, indent=2)

        return certificate

    @classmethod
    def load(cls, path):
        """Load a certificate from JSON for verification."""
        with open(path) as f:
            cert = json.load(f)
        return cert

    @staticmethod
    def verify(certificate):
        """
        Verify an integrity certificate.

        Returns
        -------
        tuple : (is_valid: bool, issues: list[str])
        """
        issues = []

        if not isinstance(certificate, dict):
            return False, ["Certificate is not a dict"]

        if certificate.get("_type") != "HUF_INTEGRITY_CERTIFICATE":
            issues.append("Not a HUF integrity certificate")

        chain = certificate.get("chain", [])
        if not chain:
            return False, ["Empty chain"]

        # Verify chain linkage
        for i, step in enumerate(chain):
            expected_prev = chain[i-1]["step_hash"] if i > 0 else "GENESIS"
            if step.get("prev_hash") != expected_prev:
                issues.append(f"Step {i+1} ({step['step_name']}): chain break — "
                             f"prev_hash mismatch")

            # Recompute step_hash
            chain_input = (f"{step['step_name']}|{step['input_hash']}|"
                          f"{step['output_hash']}|{step['prev_hash']}")
            recomputed = hashlib.sha256(chain_input.encode('utf-8')).hexdigest()
            if recomputed != step.get("step_hash"):
                issues.append(f"Step {i+1} ({step['step_name']}): "
                             f"step_hash mismatch (tampered?)")

        # Verify master hash
        all_hashes = "".join(s["step_hash"] for s in chain)
        recomputed_master = hashlib.sha256(all_hashes.encode('utf-8')).hexdigest()
        if recomputed_master != certificate.get("master_hash"):
            issues.append(f"Master hash mismatch: expected {certificate.get('master_hash')[:16]}..., "
                         f"got {recomputed_master[:16]}...")

        return len(issues) == 0, issues


# ═══════════════════════════════════════════════════════════════════════════════
#  CONVENIENCE: Hash an entire experiment output
# ═══════════════════════════════════════════════════════════════════════════════

def hash_experiment_output(json_path):
    """Compute SHA-256 of an experiment's output JSON (canonical form)."""
    with open(json_path) as f:
        data = json.load(f)
    canonical = json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(canonical).hexdigest()


def hash_experiment_script(py_path):
    """Compute SHA-256 of an experiment script (raw bytes)."""
    with open(py_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
#  SELF-TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("HUF Integrity Module — Self-Test")
    print("=" * 50)

    # Test 1: Create a chain and seal it
    chain = IntegrityChain("TEST-01", "Self-Test")

    # Simulate EITT steps
    raw = np.array([30.0, 50.0, 20.0])
    closed = raw / raw.sum()
    chain.record_step("raw_data", raw, raw, {"D": 3, "N": 1})
    chain.record_step("simplex_closure", raw, closed)

    clr = np.log(closed) - np.mean(np.log(closed))
    chain.record_step("clr_transform", closed, clr)

    sigma_a = np.sum(clr**2) / len(clr)
    chain.record_step("aitchison_variance", clr, sigma_a)

    H = -np.sum(closed * np.log(closed))
    chain.record_step("shannon_entropy", closed, H)
    chain.record_result("H_norm", H / np.log(3), "Normalised Shannon entropy")

    cert = chain.seal()
    print(f"  Chain sealed: {cert['step_count']} steps")
    print(f"  Master hash:  {cert['master_hash'][:32]}...")

    # Test 2: Verify the certificate
    is_valid, issues = IntegrityChain.verify(cert)
    print(f"  Verification: {'PASS' if is_valid else 'FAIL'}")
    if issues:
        for iss in issues:
            print(f"    Issue: {iss}")

    # Test 3: Tamper and verify again
    cert_tampered = json.loads(json.dumps(cert))
    cert_tampered["chain"][2]["output_hash"] = "0" * 64  # Corrupt step 3
    is_valid_t, issues_t = IntegrityChain.verify(cert_tampered)
    print(f"  Tamper test:  {'DETECTED' if not is_valid_t else 'MISSED!'}")
    if issues_t:
        print(f"    Caught: {issues_t[0]}")

    # Test 4: File hashing
    print(f"\n  Module self-hash: {hash_experiment_script(__file__)[:32]}...")

    print("\n  All self-tests passed." if is_valid and not is_valid_t else "\n  SELF-TEST ISSUES!")
