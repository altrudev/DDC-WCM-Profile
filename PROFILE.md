# DDC–WCM Interoperability Profile v0.1

Status: Draft / Experimental

## 1. Purpose

This profile defines a public interoperability boundary for combining WCM custody evidence with independent contextual assurance.

It specifies what evidence may be exchanged, what minimum invariants apply, what decisions may be returned, and how contradictions and uncertainty must be represented.

It intentionally does not specify how a proprietary DDC implementation derives deeper coherence judgments.

## 2. Normative language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, MAY, and OPTIONAL are to be interpreted as normative requirements.

## 3. Fundamental rules

1. WCM verification remains authoritative for WCM-specific validity.
2. A WCM failure MUST NOT be overridden by this profile.
3. Missing mandatory evidence MUST NOT silently become ALLOW.
4. Parsing or normalization failures MUST NOT silently discard security-relevant fields.
5. An unresolved critical contradiction MUST prevent ALLOW.
6. Unsupported mandatory profile semantics MUST produce an incompatible or non-ALLOW result.
7. The exact approved request MUST be bound to the executed action.
8. Material execution divergence MUST be recorded.

## 4. Decision states

### ALLOW
Available evidence is sufficient and no blocking contradiction or policy violation remains.

### BLOCK
A mandatory invariant, WCM condition, policy requirement, identity binding, or critical consistency condition failed.

### REQUIRE_HUMAN
Evidence is materially ambiguous or contradictory and policy requires an explicit human transition.

### INSUFFICIENT_EVIDENCE
Required evidence for a meaningful assurance decision is unavailable, stale, untrusted, or incomplete.

## 5. Evidence domains

### 5.1 Artifact identity
Public contract fields may include:
- model identifier;
- weights digest;
- encrypted artifact digest;
- WCM manifest identifier;
- WCM manifest digest;
- derivative parent identifier.

### 5.2 Authority
Public contract fields may include:
- manifest signer identity;
- independently pinned authority identity;
- human or organizational authority reference;
- delegation chain references;
- requested operation;
- authorized scope;
- validity period.

### 5.3 Executor identity
Public contract fields may include:
- executor identifier;
- executor signing key/fingerprint;
- execution environment identity;
- software version;
- capability declaration;
- session or boot identity.

### 5.4 Runtime state
Public contract fields may include:
- runtime/workload measurement;
- execution image identifier;
- serving state;
- lease state;
- managed-key state;
- relevant version information.

### 5.5 WCM attestation
A normalized WCM result may include:
- verification outcome;
- WCM/spec version;
- challenge or nonce digest;
- CPU evidence digest;
- GPU evidence digest;
- transport/channel binding digest;
- accepted measurement;
- verification timestamp;
- lease metadata.

The profile MUST NOT redefine WCM's cryptographic validation rules.

### 5.6 Freshness
Freshness SHOULD be represented per evidence channel, not as one global timestamp.

Examples:
- attestation age;
- challenge age;
- revocation-check age;
- executor-presence age;
- jurisdiction-evidence age;
- authority age;
- policy age.

### 5.7 Lineage
Implementations SHOULD preserve enough references to reconstruct relevant lineage across:
model -> manifest -> executor -> release -> derivative.

### 5.8 Physical assurance
Physical assurance MUST remain distinct from TEE/attestation validity.

A valid TEE assertion MUST NOT automatically imply trustworthy physical custody.

### 5.9 Jurisdiction
Jurisdiction MUST distinguish:
- policy requirement;
- claimed location;
- independent supporting evidence;
- conflicting evidence;
- resulting assessment.

Ordinary network location alone SHOULD NOT be represented as proof of physical jurisdiction.

### 5.10 Supply-chain assurance
Artifact integrity MUST be represented separately from artifact acceptability.

A byte-for-byte valid and correctly signed artifact can still be unacceptable for policy, safety, provenance, or behavior reasons.

### 5.11 Contradictions
Material contradictions SHOULD be explicit objects rather than hidden inside a scalar score.

A contradiction record SHOULD identify:
- dimensions involved;
- severity;
- conflicting observations;
- provenance;
- whether resolved;
- public reason code.

### 5.12 Longitudinal/frequency observations
The profile MAY expose observations such as:
- state-transition rarity;
- request bursts;
- identity oscillation;
- measurement churn;
- failure clustering;
- cross-channel divergence;
- periodic anomalies.

The algorithm used to derive such observations is implementation-private.

## 6. Fail-closed invariants

At minimum:

- WCM_INVALID -> BLOCK
- WCM_UNKNOWN -> non-ALLOW
- manifest identity mismatch -> BLOCK
- weights identity mismatch -> BLOCK
- executor identity mismatch -> BLOCK
- expired/replayed challenge -> BLOCK
- required attestation absent -> BLOCK
- known revocation -> BLOCK
- unresolved critical contradiction -> BLOCK
- assurance-engine error -> non-ALLOW
- evidence parser failure -> non-ALLOW
- unsupported mandatory profile version -> non-ALLOW
- material execution divergence -> recorded and non-success disposition

## 7. Public reason codes

Initial reason-code namespace:

- WCM_INVALID
- WCM_UNKNOWN
- MANIFEST_IDENTITY_MISMATCH
- WEIGHTS_IDENTITY_MISMATCH
- EXECUTOR_IDENTITY_MISMATCH
- AUTHORITY_SCOPE_MISMATCH
- AUTHORITY_EXPIRED
- ATTESTATION_MISSING
- ATTESTATION_STALE
- CHALLENGE_REPLAY
- REVOCATION_KNOWN
- RUNTIME_STATE_CONTRADICTION
- LINEAGE_CONTRADICTION
- JURISDICTION_CONTRADICTION
- JURISDICTION_NOT_ESTABLISHED
- PHYSICAL_ASSURANCE_INSUFFICIENT
- SUPPLY_CHAIN_POLICY_FAILURE
- FREQUENCY_ANOMALY
- EXECUTOR_LINEAGE_CONTRADICTION
- CRITICAL_CONTRADICTION
- INSUFFICIENT_EVIDENCE
- PROFILE_INCOMPATIBLE
- ASSURANCE_ENGINE_ERROR
- EXECUTION_DIVERGENCE

## 8. Proprietary boundary

A conforming provider is not required to disclose:
- scoring formulas;
- radial/frequency transforms;
- hidden dimensions;
- model weights;
- heuristics;
- thresholds;
- baseline construction;
- contradiction-ranking logic;
- confidence aggregation;
- internal state transitions.

Public outputs SHOULD remain explainable through evidence references and reason codes without disclosing proprietary inference mechanisms.

## 9. Action Receipt binding

A DDC Action Receipt integration SHOULD bind this evidence bundle by cryptographic digest rather than duplicating the entire WCM payload.

The receipt should preserve:
- requested operation;
- authority reference;
- subject/model identity;
- DDC-WCM evidence digest;
- public decision;
- reason codes;
- executed action;
- execution divergence, if any.

## 10. Compatibility

Profile identifier:

`ddc-wcm/0.1`

Pre-1.0 revisions may change. Implementations MUST reject unsupported mandatory semantics rather than guessing.
