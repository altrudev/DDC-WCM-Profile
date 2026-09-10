# DDC Action Receipt Binding

Status: Draft v0.1

## Purpose

This document defines how a DDC-WCM evidence bundle is bound into a DDC Action Receipt without duplicating the full WCM payload.

## Binding invariant

The Action Receipt MUST bind the exact evidence bundle used for the decision by cryptographic digest.

The receipt SHOULD preserve at least:

- requested action;
- authority reference;
- model/weights identity;
- WCM manifest identity;
- DDC-WCM profile identifier;
- DDC-WCM evidence-bundle digest;
- final decision;
- public reason codes;
- execution result;
- execution divergence, if any.

## Recommended binding object

```json
{
  "type": "ddc-wcm",
  "profile": "ddc-wcm/0.1",
  "digest": "sha256:<digest-of-canonical-evidence-bundle>",
  "decision": "ALLOW",
  "reason_codes": []
}
```

## Canonicalization

Interoperable profile v0.1 bindings SHOULD use RFC 8785 JSON Canonicalization Scheme (JCS) and SHA-256 as defined in [CANONICALIZATION.md](CANONICALIZATION.md).

A receipt claiming interoperable digest equivalence MUST bind the exact canonical evidence bytes used for the assurance decision. Redacted or transformed evidence is a distinct artifact and requires its own digest.

## Execution divergence

If the executed action differs materially from the approved request, the resulting Action Receipt MUST include:

`EXECUTION_DIVERGENCE`

and MUST NOT represent the transition as an unqualified success.

## Non-duplication rule

The receipt MAY embed selected human-readable fields, but the authoritative DDC-WCM evidence bundle SHOULD remain a separately addressable artifact bound by digest.
