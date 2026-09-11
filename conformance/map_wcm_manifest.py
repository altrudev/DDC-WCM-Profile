#!/usr/bin/env python3
"""Map a WCM manifest into a conservative DDC-WCM evidence skeleton.

The mapper does not verify WCM cryptography or runtime state. By default it
marks WCM verification UNKNOWN and leaves independently observed state unknown.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PINNED_WCM_REVISION = "718d6e308e7988d4d5af41fdf71ac44738fc49d5"
PINNED_WCM_SPEC = "v0.15"


def map_manifest(
    manifest: dict,
    manifest_hash: str,
    verification_result: str = "UNKNOWN",
    upstream_revision: str = PINNED_WCM_REVISION,
    spec_version: str = PINNED_WCM_SPEC,
) -> dict:
    release_terms = manifest.get("release_terms", {})
    release_policy = manifest.get("release_policy", {})
    custody = manifest.get("custody", {})
    builder = manifest.get("builder", {})
    serving = release_policy.get("required_serving_image", {})
    rights = manifest.get("rights_holder") or {}
    provenance = manifest.get("provenance") or {}
    model_signing = provenance.get("model_signing") or {}

    accepted_measurements = []
    for item in serving.get("accepted_measurements", []):
        if item.get("status") in {"current", "retiring"} and item.get("measurement"):
            accepted_measurements.append(item["measurement"])

    jurisdiction = release_terms.get("jurisdiction_restriction")
    jurisdiction_required = [jurisdiction] if jurisdiction else []

    bundle = {
        "profile": "ddc-wcm/0.1",
        "request": {
            "operation": "wcm.key_release",
            "request_id": "manifest-mapping-unbound",
        },
        "subject": {
            "weights_hash": manifest["weights_hash"],
            "manifest_hash": manifest_hash,
        },
        "authority": {
            "status": "unknown",
            "presented_authority": builder.get("identity", ""),
            "builder_signing_key": builder.get("signing_key", ""),
            "custodian": custody.get("custodian", ""),
            "custodian_type": custody.get("custodian_type", ""),
            "permitted_environments": release_terms.get("permitted_environments", []),
            "derivative_policy": release_terms.get("derivatives") or "",
        },
        "wcm": {
            "verification_result": verification_result,
            "spec_version": spec_version,
            "manifest_version": manifest.get("manifest_version", ""),
            "upstream_revision": upstream_revision,
        },
        "executor": {},
        "runtime": {
            "approved_measurements": accepted_measurements,
            "required_serving_image_signer": serving.get("signer", ""),
            "required_hw_platforms": release_policy.get("required_hw_platform", []),
            "kbs_measurement": (custody.get("kbs_image") or {}).get("measurement", ""),
            "enclave_id": custody.get("enclave_id", ""),
        },
        "freshness": {
            "assessment": "UNKNOWN",
            "trusted_time_source": release_policy.get("trusted_time_source", "none-best-effort"),
            "attestation_cadence": custody.get("attestation_cadence", ""),
            "kbs_attestation_cadence": custody.get("kbs_attestation_cadence"),
            "attestation_revocation_check": release_policy.get("attestation_revocation_check"),
        },
        "lineage": {
            "assessment": "UNKNOWN",
            "derivative_policy": release_terms.get("derivatives"),
        },
        "physical": {
            "assessment": "UNKNOWN",
            "required_hardening": release_policy.get("physical_hardening", "not-required"),
        },
        "jurisdiction": {
            "required": jurisdiction_required,
            "assessment": "NOT_ESTABLISHED" if jurisdiction_required else "UNKNOWN",
            "evidence": [],
        },
        "supply_chain": {
            "integrity": "UNKNOWN",
            "acceptability": "UNKNOWN",
            "expected_serving_image_signer": serving.get("signer", ""),
            "expected_kbs_signer": (custody.get("kbs_image") or {}).get("signer", ""),
        },
        "frequency": {"assessment": "UNKNOWN"},
        "contradictions": [],
        "uncertainty": {
            "assessment": "HIGH",
            "notes": [
                "Manifest mapping contains policy assertions, not observed runtime state.",
                "Independent WCM verification and contextual evidence are still required.",
            ],
        },
    }

    if manifest.get("derived_from"):
        bundle["lineage"]["parent_weights_hash"] = manifest["derived_from"]
    if rights.get("base"):
        bundle["lineage"]["rights_holder_base"] = rights["base"]
    if "derivative" in rights:
        bundle["lineage"]["rights_holder_derivative"] = rights.get("derivative")
    if model_signing.get("signed_digest"):
        bundle["supply_chain"]["model_signing_digest"] = model_signing["signed_digest"]

    # Remove empty-string optional fields rather than representing absence as data.
    for section in ("authority", "runtime", "supply_chain"):
        empty = [k for k, v in bundle[section].items() if v == ""]
        for key in empty:
            del bundle[section][key]

    return bundle


def main() -> int:
    parser = argparse.ArgumentParser(description="Map a WCM manifest to a DDC-WCM evidence skeleton.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--manifest-hash", required=True, help="Digest of the exact WCM manifest artifact")
    parser.add_argument(
        "--verification-result",
        choices=["VALID", "INVALID", "UNKNOWN"],
        default="UNKNOWN",
        help="Use VALID only when supplied by an authoritative WCM verifier",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text())
    bundle = map_manifest(manifest, args.manifest_hash, args.verification_result)
    encoded = json.dumps(bundle, indent=2, sort_keys=True) + "\n"

    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
