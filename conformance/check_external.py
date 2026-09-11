#!/usr/bin/env python3
"""Validate and evaluate an external DDC-WCM evidence bundle.

This tool accepts a JSON file from anywhere on the local filesystem. The file
never needs to be copied into this repository.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_PATH = ROOT / "conformance" / "run.py"
SCHEMA_PATH = ROOT / "schema" / "ddc-wcm-evidence-v0.1.schema.json"


def load_decision_module():
    spec = importlib.util.spec_from_file_location("ddc_wcm_conformance", RUN_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load public conformance module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an external DDC-WCM evidence bundle and apply public deterministic rules."
    )
    parser.add_argument("bundle", type=Path, help="Path to a DDC-WCM JSON evidence bundle")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable result")
    args = parser.parse_args()

    try:
        import jsonschema
    except ImportError:
        print("ERROR: install dependency with: python -m pip install jsonschema", file=sys.stderr)
        return 2

    try:
        bundle = json.loads(args.bundle.read_text())
    except Exception as exc:
        print(f"ERROR: cannot read bundle: {exc}", file=sys.stderr)
        return 2

    schema = json.loads(SCHEMA_PATH.read_text())
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    errors = sorted(validator.iter_errors(bundle), key=lambda e: list(e.path))
    if errors:
        result = {
            "schema_valid": False,
            "decision": "INSUFFICIENT_EVIDENCE",
            "reason_codes": ["PROFILE_INCOMPATIBLE"],
            "errors": [
                {
                    "path": ".".join(str(x) for x in error.path) or "<root>",
                    "message": error.message,
                }
                for error in errors
            ],
        }
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print("SCHEMA: FAIL")
            for item in result["errors"]:
                print(f"  {item['path']}: {item['message']}")
        return 1

    module = load_decision_module()
    decision, reasons = module.public_decision(bundle)
    result = {
        "schema_valid": True,
        "profile": bundle.get("profile"),
        "decision": decision,
        "reason_codes": reasons,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("SCHEMA: PASS")
        print(f"PROFILE: {bundle.get('profile')}")
        print(f"DECISION: {decision}")
        print("REASONS: " + (", ".join(reasons) if reasons else "none"))

    return 0 if decision == "ALLOW" else 3


if __name__ == "__main__":
    raise SystemExit(main())
