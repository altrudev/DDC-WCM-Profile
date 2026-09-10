# Versioning and Compatibility

Status: Draft v0.1

## Profile identifier

The current profile identifier is:

`ddc-wcm/0.1`

The profile is pre-1.0 and may change incompatibly while the evidence contract, conformance corpus, and upstream WCM mappings are being validated.

## Compatibility rules

Implementations MUST fail closed when they encounter unsupported mandatory semantics.

An implementation MUST NOT reinterpret an unknown mandatory field, reason code, or profile revision as if it were understood.

Recommended handling:

- exact supported profile revision -> evaluate normally;
- newer compatible extension explicitly marked optional -> MAY ignore;
- unknown mandatory extension -> `INSUFFICIENT_EVIDENCE` or `BLOCK` according to policy;
- unsupported profile revision -> non-ALLOW with `PROFILE_INCOMPATIBLE`.

## Change classes

### Patch-level editorial change

A change MAY remain within the same profile identifier when it does not alter machine-readable semantics, required fields, decision precedence, or conformance outcomes.

Examples:

- typo fixes;
- explanatory prose;
- attribution updates;
- non-normative examples.

### Semantic revision

A new profile revision is REQUIRED when a change alters:

- required or prohibited evidence fields;
- field meaning or accepted values;
- decision semantics;
- reason-code meaning;
- fail-closed invariants;
- canonicalization rules;
- Action Receipt binding semantics;
- expected outcomes of normative conformance vectors.

## Extension model

Implementations MAY expose implementation-specific metadata under a clearly namespaced extension object in a future revision.

Extensions MUST NOT:

- weaken WCM validity requirements;
- silently override a public fail-closed invariant;
- change the meaning of a standard reason code;
- cause a conforming verifier to treat unsupported mandatory semantics as ALLOW.

## Upstream WCM tracking

DDC-WCM Profile does not imply compatibility with every WCM revision.

A conforming implementation SHOULD record the WCM/spec version actually verified and SHOULD pin any production interoperability claim to the tested WCM revision or range.

Upstream WCM changes affecting manifest identity, attestation semantics, challenge freshness, key release, lease behavior, revocation, derivative lineage, or receipt semantics MUST trigger interoperability review before compatibility is claimed.

## Stability target

The v0.x series is for design validation and interoperability testing.

A future v1.0 should require:

1. stable evidence schema;
2. stable reason-code namespace;
3. deterministic canonicalization;
4. positive and negative conformance vectors;
5. upstream-version compatibility statement;
6. independent implementation or interoperability review.
