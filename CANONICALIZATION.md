# Canonicalization and Digest Binding

Status: Draft v0.1

## Purpose

DDC-WCM evidence may be referenced from a DDC Action Receipt by digest. Cross-implementation digest equivalence requires deterministic serialization.

## Canonical form

For profile v0.1, implementations claiming interoperable evidence-bundle digests SHOULD use **JSON Canonicalization Scheme (JCS), RFC 8785**.

The digest procedure is:

1. validate the evidence object against the applicable DDC-WCM schema;
2. remove no fields and add no inferred fields during canonicalization;
3. serialize the JSON object using RFC 8785 JCS;
4. encode the canonical JSON as UTF-8;
5. compute SHA-256 over those exact bytes;
6. encode the binding as `sha256:<lowercase-hex>`.

Conceptually:

```text
digest = "sha256:" + hex(
    SHA256(
        UTF8(
            JCS(evidence_bundle)
        )
    )
)
```

## Binding invariant

The digest MUST identify the exact evidence bundle used for the assurance decision.

A verifier MUST NOT recompute the digest over a semantically reconstructed, reordered-by-custom-rules, normalized, redacted, or enriched object unless that transformation is itself part of a separately identified profile.

## Numbers and Unicode

Implementations MUST follow RFC 8785 rules for JSON number serialization and string handling when claiming JCS interoperability.

Ad hoc use of language-default JSON serialization is insufficient for cross-implementation digest equivalence.

## Redaction

If evidence must be redacted for disclosure, the redacted representation is a different artifact and MUST have its own digest.

A public receipt MAY bind both:

- the confidential authoritative evidence digest; and
- a separately identified redacted disclosure artifact digest.

The receipt MUST NOT imply that the redacted artifact is byte-identical to the authoritative evidence.

## Algorithm agility

Profile v0.1 standardizes SHA-256 for evidence-bundle binding.

Future profiles MAY introduce additional digest algorithms, but the algorithm identifier MUST be explicit and downgrade behavior MUST fail closed.

## Domain separation

Where the digest is signed as part of a larger protocol, implementations SHOULD provide protocol-level domain separation so that an evidence-bundle digest cannot be confused with a digest from another object class.

A future profile revision may standardize a byte-level domain-separation prefix.
