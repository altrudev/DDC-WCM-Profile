#!/usr/bin/env python3
"""
Public DDC-WCM conformance harness.

This harness validates vector inputs against the public JSON Schema and checks
only deterministic public invariants. It does not implement proprietary DDC
reasoning, scoring, radial-frequency analysis, or hidden assurance logic.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "ddc-wcm-evidence-v0.1.schema.json"

BLOCKING_CODES = {
    "WCM_INVALID",
    "MANIFEST_IDENTITY_MISMATCH",
    "WEIGHTS_IDENTITY_MISMATCH",
    "EXECUTOR_IDENTITY_MISMATCH",
    "AUTHORITY_SCOPE_MISMATCH",
    "AUTHORITY_EXPIRED",
    "ATTESTATION_MISSING",
    "CHALLENGE_REPLAY",
    "REVOCATION_KNOWN",
    "RUNTIME_STATE_CONTRADICTION",
    "LINEAGE_CONTRADICTION",
    "SUPPLY_CHAIN_POLICY_FAILURE",
    "EXECUTOR_LINEAGE_CONTRADICTION",
    "CRITICAL_CONTRADICTION",
    "EXECUTION_DIVERGENCE",
}

ESCALATION_CODES = {
    "JURISDICTION_CONTRADICTION",
    "FREQUENCY_ANOMALY",
}

EVIDENCE_CODES = {
    "WCM_UNKNOWN",
    "ATTESTATION_STALE",
    "JURISDICTION_NOT_ESTABLISHED",
    "PHYSICAL_ASSURANCE_INSUFFICIENT",
    "INSUFFICIENT_EVIDENCE",
    "PROFILE_INCOMPATIBLE",
    "ASSURANCE_ENGINE_ERROR",
}


def public_decision(bundle: dict) -> tuple[str, list[str]]:
    """Apply deterministic public rules only."""
    codes: list[str] = []

    wcm = bundle.get("wcm", {})
    verification = wcm.get("verification_result")
    if verification == "INVALID":
        codes.append("WCM_INVALID")
    elif verification == "UNKNOWN":
        codes.append("WCM_UNKNOWN")

    authority = bundle.get("authority", {})
    if authority.get("status") == "contradictory":
        if authority.get("pinned_authority") and authority.get("presented_authority"):
            if authority["pinned_authority"] != authority["presented_authority"]:
                codes.append("AUTHORITY_SCOPE_MISMATCH")

    executor = bundle.get("executor", {})
    pinned_exec = executor.get("independently_pinned_executor_id")
    current_exec = executor.get("executor_id")
    if pinned_exec and current_exec and pinned_exec != current_exec:
        codes.append("EXECUTOR_LINEAGE_CONTRADICTION")

    freshness = bundle.get("freshness", {})
    if freshness.get("assessment") in {"STALE", "MIXED"}:
        codes.append("ATTESTATION_STALE")

    lineage = bundle.get("lineage", {})
    if lineage.get("assessment") == "CONTRADICTORY":
        codes.append("LINEAGE_CONTRADICTION")

    jurisdiction = bundle.get("jurisdiction", {})
    if jurisdiction.get("assessment") == "CONTRADICTORY":
        codes.append("JURISDICTION_CONTRADICTION")
    elif jurisdiction.get("assessment") == "NOT_ESTABLISHED":
        codes.append("JURISDICTION_NOT_ESTABLISHED")

    physical = bundle.get("physical", {})
    if physical.get("assessment") == "INSUFFICIENT":
        codes.append("PHYSICAL_ASSURANCE_INSUFFICIENT")

    supply_chain = bundle.get("supply_chain", {})
    if supply_chain.get("integrity") == "INVALID":
        codes.append("SUPPLY_CHAIN_POLICY_FAILURE")
    if supply_chain.get("acceptability") == "FAIL":
        codes.append("SUPPLY_CHAIN_POLICY_FAILURE")

    frequency = bundle.get("frequency", {})
    if frequency.get("assessment") == "ANOMALOUS":
        codes.append("FREQUENCY_ANOMALY")

    for contradiction in bundle.get("contradictions", []):
        if contradiction.get("resolved") is False:
            code = contradiction.get("reason_code")
            if code:
                codes.append(code)
            if contradiction.get("severity") == "critical":
                if not code:
                    codes.append("CRITICAL_CONTRADICTION")

    # Stable deduplication.
    seen = set()
    codes = [c for c in codes if not (c in seen or seen.add(c))]

    if any(c in BLOCKING_CODES for c in codes):
        return "BLOCK", codes
    if any(c in ESCALATION_CODES for c in codes):
        return "REQUIRE_HUMAN", codes
    if any(c in EVIDENCE_CODES for c in codes):
        return "INSUFFICIENT_EVIDENCE", codes
    return "ALLOW", codes


def main() -> int:
    try:
        import jsonschema
    except ImportError:
        print("ERROR: missing dependency 'jsonschema'. Install with: pip install jsonschema", file=sys.stderr)
        return 2

    schema = json.loads(SCHEMA_PATH.read_text())
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    failures = 0
    total = 0

    paths = sorted((ROOT / "vectors").rglob("*.json"))

    if not paths:
        print("ERROR: no vectors found", file=sys.stderr)
        return 2

    for path in paths:
        total += 1
        vector = json.loads(path.read_text())
        bundle = vector["input"]

        schema_errors = sorted(validator.iter_errors(bundle), key=lambda e: list(e.path))
        if schema_errors:
            failures += 1
            print(f"FAIL {vector.get('id', path.name)}: schema validation")
            for error in schema_errors:
                location = ".".join(str(x) for x in error.path) or "<root>"
                print(f"  {location}: {error.message}")
            continue

        actual_decision, actual_codes = public_decision(bundle)
        expected_decision = vector["expected_decision"]
        expected_codes = vector.get("expected_reason_codes", [])

        ok = actual_decision == expected_decision and set(expected_codes).issubset(set(actual_codes))
        if ok:
            print(f"PASS {vector['id']}: {actual_decision} ({', '.join(actual_codes) or 'no reasons'})")
        else:
            failures += 1
            print(f"FAIL {vector['id']}")
            print(f"  expected decision: {expected_decision}")
            print(f"  actual decision:   {actual_decision}")
            print(f"  expected reasons:  {expected_codes}")
            print(f"  actual reasons:    {actual_codes}")

    print()
    print(f"{total - failures}/{total} vectors passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
