from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


class VerificationAdapterError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _detect_version(exe: str) -> str:
    first = Path(exe).read_text(errors="ignore").splitlines()[0] if Path(exe).is_file() else ""
    if not first.startswith("#!"):
        raise VerificationAdapterError("cannot determine WCM verifier interpreter")
    interpreter = first[2:].strip().split()[0]
    proc = subprocess.run(
        [interpreter, "-c", "import importlib.metadata as m; print(m.version('weight-custody-manifest'))"],
        capture_output=True, text=True, timeout=15,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise VerificationAdapterError("cannot determine installed WCM verifier version")
    return proc.stdout.strip()

def run_wcm_verify(
    manifest: Path,
    key_files: list[Path],
    wcm_executable: str = "wcm",
) -> tuple[dict, dict]:
    if not key_files:
        raise VerificationAdapterError("at least one trusted WCM key file is required")
    exe = shutil.which(wcm_executable)
    if not exe:
        raise VerificationAdapterError(f"WCM verifier executable not found: {wcm_executable}")

    manifest = manifest.resolve(strict=True)
    keys = [p.resolve(strict=True) for p in key_files]
    argv = [exe, "verify", str(manifest)]
    for key in keys:
        argv.extend(["--key-file", str(key)])

    proc = subprocess.run(argv, capture_output=True, timeout=120)
    stdout = proc.stdout
    stderr = proc.stderr

    try:
        report = json.loads(stdout.decode("utf-8"))
    except Exception as exc:
        raise VerificationAdapterError(
            "WCM verifier did not return a JSON verification report"
        ) from exc
    if not isinstance(report, dict) or not isinstance(report.get("ok"), bool):
        raise VerificationAdapterError("WCM verifier report missing boolean 'ok'")

    result = "VALID" if report["ok"] and proc.returncode == 0 else "INVALID"
    if report["ok"] and proc.returncode != 0:
        raise VerificationAdapterError("WCM verifier report/exit-code contradiction")
    if not report["ok"] and proc.returncode == 0:
        raise VerificationAdapterError("WCM verifier report/exit-code contradiction")

    evidence = {
        "source": "executed-wcm-cli",
        "verifier_name": "weight-custody-manifest",
        "verifier_version": _detect_version(exe),
        "verifier_executable": exe,
        "verifier_executable_hash": sha256_file(Path(exe)),
        "manifest_hash": sha256_file(manifest),
        "report_hash": sha256_bytes(stdout),
        "trusted_key_hashes": [sha256_file(p) for p in keys],
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "result": result,
        "exit_code": proc.returncode,
    }
    if stderr:
        evidence["stderr_hash"] = sha256_bytes(stderr)
    return evidence, report
