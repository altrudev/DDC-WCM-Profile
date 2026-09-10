# Security Policy

## Scope

This repository defines a public interoperability profile and conformance surface. It does not contain the proprietary DDC assurance engine.

Security issues may include:

- schema ambiguity that permits unsafe interpretation;
- fail-open behavior;
- reason-code or decision-precedence inconsistencies;
- canonicalization or digest-binding ambiguity;
- malformed evidence accepted as valid;
- profile downgrade or version-confusion paths;
- Action Receipt binding failures;
- vectors that incorrectly permit ALLOW;
- accidental disclosure of private DDC implementation details.

## Reporting

Please avoid publishing exploit details for a newly discovered security-sensitive defect before maintainers have had a reasonable opportunity to review it.

For ordinary specification defects, open a GitHub issue with a minimal reproducible example.

For issues involving sensitive implementation details or potential proprietary-information exposure, contact:

**inquiry@ddcal.ca**

Do not send credentials, private keys, production model weights, confidential customer evidence, or other secrets in a public issue.

## Security posture

Conformance to this profile is not certification of:

- WCM itself;
- confidential-computing hardware;
- physical custody;
- geographic location;
- model safety;
- deployment security.

The profile is designed to fail closed where mandatory assurance semantics are unknown, contradictory, or insufficiently evidenced.

## Proprietary boundary

Public security discussion SHOULD describe observable evidence, violated invariants, and externally visible outcomes without requiring disclosure of proprietary DDC scoring, weighting, radial-frequency algorithms, learned baselines, thresholds, or internal inference state.
