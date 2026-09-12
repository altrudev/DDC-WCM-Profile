# Changelog

All notable changes to the DDC-WCM Profile are recorded here.

The profile is pre-1.0. Semantic changes that alter interoperability behavior require a profile revision according to VERSIONING.md.

## Unreleased

### Added

- Current-upstream WCM platform-integrity policy mapping and fixtures.

- Upstream WCM attribution and independence statement.
- Architectural rationale for combining DDC with WCM.
- Pinned upstream WCM compatibility baseline.
- Public deterministic reason-code semantics.
- DDC Action Receipt evidence-digest binding.
- RFC 8785 JCS + SHA-256 canonicalization profile.
- Security/disclosure policy.
- Versioning and compatibility rules.
- Apache-2.0 NOTICE boundary.
- Public conformance harness.
- DSR-compatible pytest wrapper.
- Positive ALLOW baseline and contradiction-focused vectors.
- Additional fail-closed vectors for WCM invalid/unknown, stale evidence, insufficient physical assurance, and unresolved critical contradiction.

### Changed

- Hardened evidence schema by rejecting undeclared fields across core evidence domains.
- Made the decision object optional in the base evidence schema so pre-decision evidence can be validated without circularity.
- Expanded vector discovery to all vector categories recursively.
- Replaced the abbreviated license text with the complete Apache License 2.0 text.

### Security

- Explicitly separates cryptographic validity from contextual coherence.
- WCM failure cannot be overridden by DDC-WCM.
- Unknown mandatory semantics are non-ALLOW.
- Critical unresolved contradictions prevent ALLOW.
- Public conformance includes an ALLOW case so reject-all implementations cannot pass.
- Interoperable receipt digests now have deterministic canonicalization guidance.
