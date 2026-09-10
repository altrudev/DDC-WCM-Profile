# Reason Codes

Status: Draft v0.1

Reason codes are public interoperability outputs. They explain *what class of condition affected the decision* without disclosing proprietary DDC inference mechanics.

## Deterministic semantics

A conforming implementation MUST apply these rules:

1. `BLOCK` MUST include at least one blocking reason code.
2. `REQUIRE_HUMAN` MUST include at least one ambiguity, contradiction, or policy-escalation reason code.
3. `INSUFFICIENT_EVIDENCE` MUST include at least one evidence-quality or compatibility reason code.
4. `ALLOW` MUST NOT include any blocking reason code.
5. Unknown reason codes MUST NOT be silently treated as non-blocking.
6. Multiple reason codes MAY be emitted when more than one material condition applies.

## Blocking reason codes

- `WCM_INVALID`
- `MANIFEST_IDENTITY_MISMATCH`
- `WEIGHTS_IDENTITY_MISMATCH`
- `EXECUTOR_IDENTITY_MISMATCH`
- `AUTHORITY_SCOPE_MISMATCH`
- `AUTHORITY_EXPIRED`
- `ATTESTATION_MISSING`
- `CHALLENGE_REPLAY`
- `REVOCATION_KNOWN`
- `RUNTIME_STATE_CONTRADICTION`
- `LINEAGE_CONTRADICTION`
- `SUPPLY_CHAIN_POLICY_FAILURE`
- `EXECUTOR_LINEAGE_CONTRADICTION`
- `CRITICAL_CONTRADICTION`
- `EXECUTION_DIVERGENCE`

## Non-ALLOW evidence/compatibility codes

- `WCM_UNKNOWN`
- `ATTESTATION_STALE`
- `JURISDICTION_NOT_ESTABLISHED`
- `PHYSICAL_ASSURANCE_INSUFFICIENT`
- `INSUFFICIENT_EVIDENCE`
- `PROFILE_INCOMPATIBLE`
- `ASSURANCE_ENGINE_ERROR`

## Escalation-capable codes

These MAY map to `REQUIRE_HUMAN` or `BLOCK` depending on policy severity:

- `JURISDICTION_CONTRADICTION`
- `FREQUENCY_ANOMALY`

## Decision precedence

When multiple conditions apply, implementations MUST use the most restrictive applicable result:

```text
BLOCK
  >
REQUIRE_HUMAN
  >
INSUFFICIENT_EVIDENCE
  >
ALLOW
```

If a blocking code is present, the final result MUST be `BLOCK`.

## Proprietary boundary

Public reason codes identify the externally visible condition class only. Implementations are not required to reveal internal scoring, radial/frequency transforms, thresholds, feature weights, hidden dimensions, or contradiction-ranking methods.
