# Testing Outside the Repository

You can test evidence produced by another machine, application, WCM integration, or lab workflow without committing that evidence to this repository.

## External bundle check

Install the one public dependency:

```bash
python -m pip install jsonschema
```

Then, from a clone of DDC-WCM-Profile, point the checker at any JSON file on your machine:

```bash
python conformance/check_external.py /path/to/evidence.json
```

For machine-readable output:

```bash
python conformance/check_external.py /path/to/evidence.json --json
```

The evidence file may live outside the repository and SHOULD remain outside the repository when it contains private deployment information.

## Exit codes

- `0` — schema-valid and public decision is `ALLOW`
- `1` — schema validation failure
- `2` — tool/input/dependency error
- `3` — schema-valid but public decision is non-ALLOW

A nonzero exit is therefore suitable for shell scripts and external CI.

## What this tests

The checker performs:

1. DDC-WCM JSON Schema validation;
2. profile identifier validation;
3. public deterministic invariant evaluation;
4. public decision/reason-code output.

It does **not** run proprietary DDC analysis.

## Independent-machine test

For a clean-room style test, clone the public repository on a separate computer or VM and run the checker against evidence generated elsewhere.

Example:

```bash
git clone https://github.com/altrudev/DDC-WCM-Profile.git
cd DDC-WCM-Profile
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python conformance/check_external.py /tmp/my-evidence.json --json
```

This verifies that the public interoperability contract can be consumed independently of DDCRE, DDCAL, or the private DDC engine.

## Higher-assurance external test

For stronger evidence, run the same pinned repository revision through a separate CI runner, VM, or governed executor and retain:

- tested commit SHA;
- input evidence digest;
- command;
- stdout/stderr;
- exit code;
- executor identity;
- timestamp;
- signature/receipt if available.

That produces an independently reproducible profile-conformance result.
