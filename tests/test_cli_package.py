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
from ddc_wcm.verifier import VerificationAdapterError, run_wcm_verify, sha256_file


def test_packaged_schema_matches_normative_schema():
    normative = json.loads((ROOT / "schema" / "ddc-wcm-evidence-v0.2.schema.json").read_text())
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
    actual = map_manifest(manifest, "sha256:" + ("e" * 64), verification_evidence=None)
    assert actual == expected
    decision, reasons = public_decision(actual)
    assert decision == "INSUFFICIENT_EVIDENCE"
    assert "WCM_UNKNOWN" in reasons


def test_cli_version(capsys):
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    assert capsys.readouterr().out.strip() == "ddc-wcm 0.2.0"


def test_packaged_mapper_handles_platform_integrity():
    manifest = json.loads(
        (ROOT / "fixtures" / "upstream" / "wcm-current-platform-integrity.synthetic.json").read_text()
    )
    expected = json.loads(
        (ROOT / "fixtures" / "mapped" / "ddc-wcm-current-platform-integrity.synthetic.json").read_text()
    )
    actual = map_manifest(
        manifest,
        "sha256:" + ("e" * 64),
        upstream_revision="e06eeb08dc3262e86d00329ac5d46977f4e83849",
        spec_version="v0.15",
        verification_evidence=None,
    )
    assert actual == expected
    assert actual["physical"]["platform_integrity_policy"]["alias_check_complete"] == "required"
    assert actual["physical"]["assessment"] == "UNKNOWN"


def test_mapper_rejects_verifier_evidence_for_other_manifest():
    manifest = json.loads(
        (ROOT / "fixtures" / "upstream" / "wcm-v0.15-manifest.synthetic.json").read_text()
    )
    evidence = {
        "source": "executed-wcm-cli",
        "verifier_name": "weight-custody-manifest",
        "verifier_version": "0.28.1",
        "verifier_executable": "/usr/bin/wcm",
        "verifier_executable_hash": "sha256:" + ("f" * 64),
        "manifest_hash": "sha256:" + ("d" * 64),
        "report_hash": "sha256:" + ("b" * 64),
        "trusted_key_hashes": ["sha256:" + ("c" * 64)],
        "verified_at": "2026-09-13T00:00:00Z",
        "result": "VALID",
        "exit_code": 0,
    }
    try:
        map_manifest(manifest, "sha256:" + ("e" * 64), verification_evidence=evidence)
    except ValueError as exc:
        assert "different manifest digest" in str(exc)
    else:
        raise AssertionError("mismatched verifier evidence was accepted")


def test_executed_wcm_verifier_adapter_binds_inputs(tmp_path, monkeypatch):
    import subprocess as _subprocess
    import ddc_wcm.verifier as verifier

    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"manifest":"fixture"}\n')
    key = tmp_path / "builder.pub"
    key.write_text("trusted-public-key\n")
    exe = tmp_path / "wcm"
    exe.write_text("#!/usr/bin/python3\n")

    monkeypatch.setattr(verifier.shutil, "which", lambda name: str(exe))

    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        if argv[0] == str(exe):
            report = {
                "ok": True,
                "signatures": [],
                "missing_roles": [],
                "errors": [],
            }
            return _subprocess.CompletedProcess(argv, 0, json.dumps(report).encode(), b"")
        return _subprocess.CompletedProcess(argv, 0, "0.28.1\n", "")

    monkeypatch.setattr(verifier.subprocess, "run", fake_run)
    evidence, report = run_wcm_verify(manifest, [key])

    assert report["ok"] is True
    assert evidence["result"] == "VALID"
    assert evidence["manifest_hash"] == sha256_file(manifest)
    assert evidence["trusted_key_hashes"] == [sha256_file(key)]
    assert evidence["verifier_version"] == "0.28.1"
    assert evidence["exit_code"] == 0
    assert calls[0][0] == str(exe)


def test_executed_wcm_verifier_rejects_report_exit_contradiction(tmp_path, monkeypatch):
    import subprocess as _subprocess
    import ddc_wcm.verifier as verifier

    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"manifest":"fixture"}\n')
    key = tmp_path / "builder.pub"
    key.write_text("trusted-public-key\n")
    exe = tmp_path / "wcm"
    exe.write_text("#!/usr/bin/python3\n")
    monkeypatch.setattr(verifier.shutil, "which", lambda name: str(exe))

    def fake_run(argv, **kwargs):
        if argv[0] == str(exe):
            report = {"ok": True, "signatures": [], "missing_roles": [], "errors": []}
            return _subprocess.CompletedProcess(argv, 1, json.dumps(report).encode(), b"")
        return _subprocess.CompletedProcess(argv, 0, "0.28.1\n", "")

    monkeypatch.setattr(verifier.subprocess, "run", fake_run)
    try:
        run_wcm_verify(manifest, [key])
    except VerificationAdapterError as exc:
        assert "contradiction" in str(exc)
    else:
        raise AssertionError("report/exit contradiction was accepted")
