from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_PATH = ROOT / "conformance" / "run.py"

spec = importlib.util.spec_from_file_location("ddc_wcm_conformance", RUN_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def vector_paths():
    yield from sorted((ROOT / "vectors").rglob("*.json"))


def test_schema_is_valid_json_and_declares_profile():
    schema = json.loads((ROOT / "schema" / "ddc-wcm-evidence-v0.1.schema.json").read_text())
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["properties"]["profile"]["const"] == "ddc-wcm/0.1"
    assert schema["additionalProperties"] is False


def test_all_vectors_match_public_decision_contract():
    paths = list(vector_paths())
    assert paths, "no vectors found"

    for path in paths:
        vector = json.loads(path.read_text())
        decision, reason_codes = module.public_decision(vector["input"])

        assert decision == vector["expected_decision"], (
            f"{vector['id']}: expected {vector['expected_decision']}, got {decision}; "
            f"reasons={reason_codes}"
        )
        assert set(vector.get("expected_reason_codes", [])).issubset(set(reason_codes)), (
            f"{vector['id']}: missing expected reason codes; "
            f"expected={vector.get('expected_reason_codes', [])}, actual={reason_codes}"
        )


def test_positive_vector_prevents_block_everything_implementation():
    vector = json.loads((ROOT / "vectors" / "valid" / "DW-000-valid-baseline.json").read_text())
    decision, reasons = module.public_decision(vector["input"])
    assert decision == "ALLOW"
    assert not reasons
