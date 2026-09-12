# Upstream WCM Compatibility Baseline

Status: Draft v0.1

This file records the upstream WCM material against which the current DDC-WCM Profile was reviewed. It is a traceability baseline, not a claim of official compatibility certification.

## Baseline reviewed

Upstream repository:

`agentrust-io/weight-custody-manifest`

Pinned upstream revision reviewed:

`718d6e308e7988d4d5af41fdf71ac44738fc49d5`

Observed upstream specification:

`SPEC.md v0.15` (pre-1.0)

Observed Python SDK release:

`0.28.1`

Observed manifest schema family:

`wcm-manifest-v1`

## Why this pin exists

WCM is pre-1.0 and continues to evolve. DDC-WCM Profile therefore MUST NOT imply that a profile reviewed against one WCM revision automatically remains valid against later WCM changes.

The pinned upstream revision provides a reproducible point for:

- evidence-field mapping;
- custody-policy semantics;
- attestation and challenge assumptions;
- release and renewal semantics;
- derivative-lineage assumptions;
- threat-model comparison;
- conformance-vector interpretation.

## Compatibility boundary

DDC-WCM Profile does not reimplement WCM verification.

A deployment claiming DDC-WCM interoperability MUST use a WCM verifier appropriate to the WCM material being consumed.

If upstream WCM changes any load-bearing semantic relevant to:

- manifest identity;
- weights identity;
- authority pinning;
- attestation structure;
- challenge freshness;
- transport-key/channel binding;
- revocation;
- release or renewal;
- trusted time;
- derivative lineage;
- custody receipts;
- hardware-profile semantics;

then DDC-WCM compatibility SHOULD be reviewed before the newer WCM revision is treated as covered.

## Upstream change policy

A newer WCM commit does not automatically invalidate this profile, but it also does not automatically extend this profile's reviewed scope.

Future reviews SHOULD append a new compatibility record containing:

1. WCM commit SHA;
2. WCM spec version;
3. SDK version, where applicable;
4. schema version;
5. material semantic changes;
6. DDC-WCM fields affected;
7. conformance vectors added or changed;
8. resulting compatibility disposition.

## Current disposition

For the baseline above:

- WCM remains authoritative for WCM-specific cryptographic and custody validity.
- DDC-WCM consumes WCM verification as one evidence channel.
- DDC-WCM adds independent contextual-coherence semantics without overriding WCM failure.
- No official endorsement, certification, or upstream adoption is implied.


## Compatibility review — current upstream main

Reviewed upstream revision:

`e06eeb08dc3262e86d00329ac5d46977f4e83849`

Review date: 2026-09-12.

### Schema comparison

Relative to the original pinned baseline
`718d6e308e7988d4d5af41fdf71ac44738fc49d5`:

- no top-level manifest fields were removed;
- no top-level required fields changed;
- builder, release-terms, custody, and required-serving-image structures remained compatible;
- serving-image status, physical-hardening, and trusted-time enumerations remained unchanged;
- `release_policy.platform_integrity` was added as an optional field;
- new definitions `PlatformIntegrity` and `PlatformIntegrityRequirement` were added.

### DDC-WCM treatment

The additive `platform_integrity` policy is explicitly mapped into
`physical.platform_integrity_policy`.

The mapping preserves the distinction between:

- **required policy state** — what the manifest requires; and
- **observed platform state** — what independent evidence proves.

A manifest that requires alias checking or ciphertext hiding does not by itself
cause `physical.assessment` to become `SUFFICIENT`.

### Disposition

**Compatible with additive mapping support.**

This disposition covers the manifest-schema delta reviewed at the revision above.
It is not a blanket claim that all future WCM changes are compatible, and it does
not constitute upstream certification or endorsement.
