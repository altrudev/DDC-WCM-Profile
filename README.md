# DDC–WCM Profile

**Open interoperability profile for evaluating whether Weight Custody Manifest (WCM) evidence and independently observed execution evidence form a sufficiently coherent basis for a consequential model-custody transition.**

> Status: **Draft v0.1 / experimental**
>
> This project does **not** implement or disclose the proprietary DDC reasoning engine. It defines an open evidence contract, decision semantics, interoperability rules, and adversarial test surface.

## Why this exists

WCM was selected as the first external interoperability target because it exposes a clear assurance boundary: a cryptographically valid custody assertion can still exist inside a wider system state that is contradictory, stale, wrongly authorized, physically uncertain, or otherwise incoherent.

The combination is architectural rather than organizational. WCM remains authoritative for custody validity; DDC independently evaluates whether that evidence remains coherent with the wider execution context. DDC does not replace WCM, and this profile does not make DDC dependent on WCM.

See [RATIONALE.md](RATIONALE.md) for the full design rationale.

The DDC–WCM Profile defines a boundary between:

- **WCM validity** — whether WCM custody evidence satisfies WCM rules;
- **DDC coherence assessment** — whether the wider evidence describes a sufficiently coherent reality for the proposed transition; and
- **action accountability** — how the resulting decision and execution can be bound into a verifiable action receipt.

## Core invariant

```text
WCM_VALID = true
does not imply
DDC_ALLOW = true
```

A conforming DDC–WCM assurance provider MUST NOT override a WCM failure.

```text
WCM_BLOCK -> DDC_BLOCK
```

## Public interface

This repository may define:

- normalized WCM evidence inputs;
- evidence dimensions and provenance requirements;
- decision states and reason codes;
- fail-closed invariants;
- interoperability schemas;
- adversarial and contradiction-focused test vectors;
- Action Receipt bindings;
- reference plumbing that does not contain proprietary assurance logic.

## Explicitly out of scope

This repository does **not** disclose:

- DDC radial-frequency algorithms;
- dimensional weighting;
- proprietary scoring or confidence aggregation;
- contradiction-resolution algorithms;
- threshold derivation;
- learned behavioral baselines;
- hidden or experimental assurance dimensions;
- internal DDC state transitions;
- proprietary heuristics or training/research methods.

Implementations may evaluate longitudinal, relational, temporal, and frequency-based inconsistencies across evidence channels without exposing how those assessments are derived internally.

## Decision states

The profile defines four top-level assurance outcomes:

- `ALLOW`
- `BLOCK`
- `REQUIRE_HUMAN`
- `INSUFFICIENT_EVIDENCE`

A provider may expose public reason codes while keeping proprietary inference details private.

## Evidence dimensions

Draft v0.1 standardizes public evidence contracts for:

1. artifact identity;
2. authority;
3. executor identity;
4. runtime state;
5. WCM attestation;
6. freshness;
7. lineage;
8. physical assurance;
9. jurisdiction;
10. supply-chain assurance;
11. contradiction reporting;
12. longitudinal/frequency observations.

These are interoperability dimensions, not a disclosure of the internal DDC model.

## Architecture

```text
WCM
  cryptographic custody validity
        |
        v
DDC-WCM normalized evidence
        |
        v
Assurance provider
        |
   +----+----+----------------+
   |         |                |
 ALLOW     BLOCK      REQUIRE_HUMAN /
                    INSUFFICIENT_EVIDENCE
        |
        v
Governed execution
        |
        v
DDC Action Receipt binding
```

## Safety and claims

DDC–WCM does not certify WCM, confidential-computing hardware, physical custody, geographic location, or model safety.

It evaluates whether WCM evidence and independently observed evidence form a sufficiently coherent basis for the proposed transition.

Conformance to this profile is not equivalent to secure deployment.

## Upstream attribution

**Weight Custody Manifest (WCM)** is an upstream open standard introduced publicly by **OPAQUE Systems**. **Imran Siddique, Chief Platform Officer at OPAQUE Systems**, is prominently associated with its public launch and is quoted by OPAQUE explaining WCM's purpose and trust model.

DDC-WCM Profile is an independent Altru.dev interoperability and assurance project. It does not claim authorship of WCM and is not affiliated with, sponsored by, endorsed by, or maintained by OPAQUE Systems, Imran Siddique, AgenTrust, or the WCM maintainers.

See [ATTRIBUTION.md](ATTRIBUTION.md) for the full upstream attribution and independence statement.

## Relationship to WCM

WCM remains authoritative for WCM verification. This profile consumes WCM results as an authoritative evidence channel and does not reimplement or weaken WCM's own verification requirements.

This project is an independent interoperability effort and is not affiliated with, endorsed by, or a substitute for the WCM project or its maintainers.

## Repository layout

```text
PROFILE.md
THREAT-MODEL.md
schema/
  ddc-wcm-evidence-v0.1.schema.json
vectors/
  README.md
  contradictory/
examples/
  evidence-bundle.json
```

## License

Apache-2.0 for the public profile, schemas, examples, and test vectors unless otherwise noted.

The DDC assurance engine and associated proprietary methods are not licensed or distributed by this repository.

## Public conformance harness

The repository includes a deliberately limited public harness that validates only the open interoperability contract.

```bash
python -m pip install -r requirements.txt
python conformance/run.py
```

The harness:

- validates the JSON Schema;
- validates every public vector input;
- applies deterministic public invariants;
- checks expected decisions and required public reason codes;
- includes a positive ALLOW baseline so "block everything" cannot pass.

It does **not** implement proprietary DDC reasoning, radial-frequency transforms, hidden dimensions, learned baselines, weighting, threshold derivation, or private contradiction-resolution logic.

A successful public conformance run therefore means **profile-contract conformance**, not full DDC assurance and not secure-deployment certification.

