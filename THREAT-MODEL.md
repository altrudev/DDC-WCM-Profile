# Threat Model

Status: Draft v0.1

## Objective

This threat model covers the interoperability boundary between WCM evidence, independent contextual evidence, an assurance provider, and a consequential custody or execution transition.

It does not replace the WCM threat model and does not claim to solve limitations of confidential-computing hardware.

## Protected properties

The profile seeks to preserve:

1. exact subject/artifact identity;
2. exact authority and delegated scope;
3. executor identity continuity;
4. runtime-state consistency;
5. WCM evidence integrity and provenance;
6. evidence freshness;
7. lineage continuity;
8. explicit treatment of physical-custody uncertainty;
9. jurisdiction-evidence integrity;
10. supply-chain policy consistency;
11. contradiction visibility;
12. accountability for the final transition.

## Adversary classes

Representative adversaries include:

- attacker presenting a new policy for legitimate weights;
- compromised executor;
- operator controlling surrounding infrastructure;
- malicious or compromised runtime image;
- supply-chain attacker;
- network attacker;
- insider with partial authority;
- attacker replaying valid historical evidence;
- attacker exploiting stale revocation or location evidence;
- attacker presenting individually valid but mutually inconsistent evidence;
- attacker causing the executed action to diverge from the approved action.

## Security hypotheses

### H1 — Validity is not coherence
Individually valid cryptographic assertions may collectively describe an inconsistent reality.

### H2 — Integrity is not acceptability
A correctly hashed and signed workload may still violate policy or contain malicious behavior.

### H3 — Attestation is not physical-custody proof
TEE validity does not establish that the hardware owner, facility, or physical environment is trustworthy.

### H4 — Policy location is not location evidence
A jurisdiction field defines a requirement; it does not independently prove actual physical location.

### H5 — Freshness is multidimensional
Fresh attestation paired with stale authority, revocation, executor, or jurisdiction evidence can be unsafe.

### H6 — Time-series behavior can be material
A sequence of individually valid events may become suspicious because of rate, oscillation, transition rarity, or cross-channel divergence.

## Representative attacks

### A1 — Authority substitution
Attacker references legitimate model weights from a policy or authority context that was not independently authorized.

Expected: BLOCK.

### A2 — Executor swap after valid attestation
Attestation is valid but the release or execution target differs from the executor whose identity was established.

Expected: BLOCK.

### A3 — Stale revocation
Attestation is fresh but revocation evidence is outside policy freshness.

Expected: non-ALLOW.

### A4 — Valid malicious workload
Measurement and signature are correct, but independent supply-chain assurance identifies prohibited behavior.

Expected: BLOCK.

### A5 — Jurisdiction contradiction
Manifest requires jurisdiction X while independent evidence materially contradicts the claimed location.

Expected: REQUIRE_HUMAN or BLOCK by policy.

### A6 — Temporal burst
Many valid release requests occur in a pattern materially outside the expected operating regime.

Expected: REQUIRE_HUMAN, containment, or BLOCK by policy.

### A7 — Attestation-key compromise simulation
Cryptographically valid attestation conflicts with independently established executor lineage or state.

Expected: BLOCK.

### A8 — Execution divergence
Approved action differs materially from the action actually performed.

Expected: receipt records EXECUTION_DIVERGENCE and the transition is not represented as successful.

## Non-goals

This profile does not guarantee:

- resistance to all physical extraction attacks;
- correctness of CPU/GPU vendors;
- correctness of WCM itself;
- trustworthy geolocation from untrusted sensors;
- absence of malicious code solely from signatures or hashes;
- production security merely from conformance.

## Disclosure boundary

The threat model is intentionally public. Countermeasure interfaces and expected outcomes may be public. Proprietary DDC inference algorithms and internal detection mechanics are not part of this document.
