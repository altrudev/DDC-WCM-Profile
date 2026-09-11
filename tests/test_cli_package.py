from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ddc_wcm.cli import _schema, check_bundle, main
from ddc_wcm.decision import public_decision
from ddc_wcm.mapping import map_manifest


def test_packaged_schema_matches_normative_schema():
    normative = json.loads((ROOT / "schema" / "ddc-wcm-evidence-v0.1.schema.json").read_text())
    assert _schema() == normative


def test_packaged_cli_checks_allow_bundle(capsys):
    path = ROOT / "vectors" / "valid" / "DW-000-valid-baseline.json"
    vector = json.loads(path.read_text())
    temp = ROOT / "tests" / ".tmp-cli-allow.json"
    try:
        temp.write_text(json.dumps(vector["input"]))
        rc = check_bundle(temp, json_output=True)
        output = json.loads(capsys.readouterr().out)
        assert rc == 0
        assert output["schema_valid"] is True
        assert output["decision"] == "ALLOW"
    finally:
        temp.unlink(missing_ok=True)


def test_packaged_cli_preserves_non_allow_exit_code(capsys):
    path = ROOT / "fixtures" / "mapped" / "ddc-wcm-from-wcm-v0.15.synthetic.json"
    rc = check_bundle(path, json_output=True)
    output = json.loads(capsys.readouterr().out)
    assert rc == 3
    assert output["decision"] == "INSUFFICIENT_EVIDENCE"
    assert "WCM_UNKNOWN" in output["reason_codes"]


def test_packaged_mapper_matches_mapping_fixture():
    manifest = json.loads(
        (ROOT / "fixtures" / "upstream" / "wcm-v0.15-manifest.synthetic.json").read_text()
    )
    expected = json.loads(
        (ROOT / "fixtures" / "mapped" / "ddc-wcm-from-wcm-v0.15.synthetic.json").read_text()
    )
    actual = map_manifest(manifest, "sha256:" + ("e" * 64))
    assert actual == expected
    decision, reasons = public_decision(actual)
    assert decision == "INSUFFICIENT_EVIDENCE"
    assert "WCM_UNKNOWN" in reasons


def test_cli_version(capsys):
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    assert capsys.readouterr().out.strip() == "ddc-wcm 0.1.0"
