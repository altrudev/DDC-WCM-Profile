from __future__ import annotations

import argparse
import json
import subprocess
import sys
from importlib.resources import files
from pathlib import Path

import jsonschema

from .decision import public_decision
from .mapping import map_manifest
from .verifier import VerificationAdapterError, run_wcm_verify, sha256_file


def _schema() -> dict:
    return json.loads(
        files("ddc_wcm")
        .joinpath("data/ddc-wcm-evidence-v0.2.schema.json")
        .read_text()
    )


def check_bundle(path: Path, json_output: bool = False) -> int:
    try:
        bundle = json.loads(path.read_text())
    except Exception as exc:
        print(f"ERROR: cannot read bundle: {exc}", file=sys.stderr)
        return 2

    schema = _schema()
    cls = jsonschema.validators.validator_for(schema)
    cls.check_schema(schema)
    errors = sorted(cls(schema).iter_errors(bundle), key=lambda e: list(e.path))
    if errors:
        result = {
            "schema_valid": False,
            "decision": "INSUFFICIENT_EVIDENCE",
            "reason_codes": ["PROFILE_INCOMPATIBLE"],
            "errors": [
                {
                    "path": ".".join(str(x) for x in e.path) or "<root>",
                    "message": e.message,
                }
                for e in errors
            ],
        }
        if json_output:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print("SCHEMA: FAIL")
            for item in result["errors"]:
                print(f"  {item['path']}: {item['message']}")
        return 1

    decision, reasons = public_decision(bundle)
    result = {
        "schema_valid": True,
        "profile": bundle.get("profile"),
        "decision": decision,
        "reason_codes": reasons,
    }
    if json_output:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("SCHEMA: PASS")
        print(f"PROFILE: {bundle.get('profile')}")
        print(f"DECISION: {decision}")
        print("REASONS: " + (", ".join(reasons) if reasons else "none"))
    return 0 if decision == "ALLOW" else 3


def _write_json(doc: dict, output: Path | None) -> None:
    encoded = json.dumps(doc, indent=2, sort_keys=True) + "\n"
    if output:
        output.write_text(encoded)
    else:
        print(encoded, end="")


def verify_wcm_file(args: argparse.Namespace) -> int:
    try:
        evidence, report = run_wcm_verify(
            args.manifest, args.key_file, args.wcm_executable
        )
    except (VerificationAdapterError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    _write_json(
        {
            "schema": "ddc-wcm-verifier-evidence/1",
            "evidence": evidence,
            "upstream_report": report,
        },
        args.output,
    )
    return 0 if evidence["result"] == "VALID" else 4


def map_file(args: argparse.Namespace) -> int:
    try:
        manifest_path = args.manifest.resolve(strict=True)
        manifest = json.loads(manifest_path.read_text())
        manifest_hash = sha256_file(manifest_path)
    except Exception as exc:
        print(f"ERROR: cannot read manifest: {exc}", file=sys.stderr)
        return 2

    bundle = map_manifest(manifest, manifest_hash, verification_evidence=None)
    _write_json(bundle, args.output)
    return 0


def verify_and_map_file(args: argparse.Namespace) -> int:
    try:
        manifest_path = args.manifest.resolve(strict=True)
        manifest = json.loads(manifest_path.read_text())
        evidence, report = run_wcm_verify(
            manifest_path, args.key_file, args.wcm_executable
        )
        bundle = map_manifest(
            manifest,
            evidence["manifest_hash"],
            verification_evidence=evidence,
        )
    except (
        VerificationAdapterError,
        OSError,
        subprocess.SubprocessError,
        ValueError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.receipt_output:
        _write_json(
            {
                "schema": "ddc-wcm-verifier-evidence/1",
                "evidence": evidence,
                "upstream_report": report,
            },
            args.receipt_output,
        )
    _write_json(bundle, args.output)
    return 0 if evidence["result"] == "VALID" else 4


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="ddc-wcm",
        description="Public DDC-WCM interoperability CLI",
    )
    parser.add_argument("--version", action="version", version="ddc-wcm 0.2.0")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check")
    check.add_argument("bundle", type=Path)
    check.add_argument("--json", action="store_true")

    verify = sub.add_parser(
        "verify-wcm",
        help="Execute upstream WCM verification and emit bound verifier evidence",
    )
    verify.add_argument("manifest", type=Path)
    verify.add_argument("--key-file", type=Path, action="append", required=True)
    verify.add_argument("--wcm-executable", default="wcm")
    verify.add_argument("--output", type=Path)

    mapping = sub.add_parser(
        "map-wcm",
        help="Map a manifest without asserting WCM validity",
    )
    mapping.add_argument("manifest", type=Path)
    mapping.add_argument("--output", type=Path)

    verify_map = sub.add_parser(
        "verify-and-map",
        help="Execute upstream WCM verification and immediately map bound evidence",
    )
    verify_map.add_argument("manifest", type=Path)
    verify_map.add_argument("--key-file", type=Path, action="append", required=True)
    verify_map.add_argument("--wcm-executable", default="wcm")
    verify_map.add_argument("--receipt-output", type=Path)
    verify_map.add_argument("--output", type=Path)

    args = parser.parse_args(argv)
    if args.command == "check":
        return check_bundle(args.bundle, args.json)
    if args.command == "verify-wcm":
        return verify_wcm_file(args)
    if args.command == "verify-and-map":
        return verify_and_map_file(args)
    return map_file(args)


if __name__ == "__main__":
    raise SystemExit(main())
