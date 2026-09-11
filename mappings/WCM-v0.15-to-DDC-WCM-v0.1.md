# WCM v0.15 → DDC-WCM v0.1 Mapping

Status: Draft / reviewed against pinned upstream WCM commit `718d6e308e7988d4d5af41fdf71ac44738fc49d5`.

This mapping describes how public WCM manifest fields contribute to a DDC-WCM evidence bundle. It does not replace WCM verification and does not infer runtime facts that a manifest cannot prove.

## Mapping principles

1. **WCM remains authoritative for WCM validity.**
2. A manifest field is treated as a policy/identity assertion unless independent evidence establishes observed state.
3. Static manifest data MUST NOT be promoted into runtime, physical, jurisdiction, freshness, or attestation proof without a separate evidence source.
4. Missing runtime evidence remains unknown or insufficient; it is not synthesized from manifest intent.
5. DDC-WCM reason codes and decisions are evaluated only after normalization.

## Field mapping

| WCM field | DDC-WCM target | Meaning |
| --- | --- | --- |
| `weights_hash` | `subject.weights_hash` | Exact protected model artifact identity |
| manifest digest (computed externally) | `subject.manifest_hash` | Exact WCM manifest artifact identity |
| `manifest_version` | `wcm.spec_version` or implementation metadata | WCM manifest/version context |
| `builder.identity` | `authority.presented_authority` | Manifest-declared builder identity |
| `builder.signing_key` | authority/signature evidence | Builder signing-key identity |
| `signatures[]` | authority/signature evidence | WCM signature layer; validity remains a WCM concern |
| `release_terms.jurisdiction_restriction` | `jurisdiction.required` | Policy requirement, not physical-location proof |
| `release_terms.permitted_environments` | authority/policy evidence | Allowed deployment environment scope |
| `release_terms.derivatives` | lineage policy | Machine-checkable derivative permission |
| `derived_from` | `lineage.parent_weights_hash` | Parent artifact linkage |
| `rights_holder` | authority/lineage evidence | Rights/authority context |
| `provenance.model_signing` | `supply_chain` / provenance evidence | Upstream model-signing reference |
| `release_policy.required_hw_platform` | physical/runtime policy | Required platform class, not observed hardware |
| `release_policy.required_serving_image.accepted_measurements[]` | runtime policy | Approved measurements, not observed measurement |
| `release_policy.required_serving_image.signer` | supply-chain/runtime policy | Expected serving-image signer |
| `release_policy.physical_hardening` | physical policy | Required hardening posture, not proof it exists |
| `release_policy.trusted_time_source` | freshness/time policy | Required time-source posture |
| `release_policy.attestation_revocation_check` | freshness/revocation policy | Required revocation behavior |
| `release_policy.replay_protection` | WCM policy | Replay-protection requirement |
| `release_policy.required_gpu_measurement` | runtime/attestation policy | Required GPU measurement |
| `custody.custodian` | authority/executor context | Declared custodian |
| `custody.custodian_type` | authority/physical context | Declared custody mode |
| `custody.kbs_image.measurement` | runtime policy | Expected KBS measurement |
| `custody.kbs_image.signer` | supply-chain/runtime policy | Expected KBS signer |
| `custody.enclave_id` | runtime/executor policy | Declared enclave identity |
| `custody.attestation_cadence` | freshness policy | Required re-attestation cadence |
| `custody.kbs_attestation_cadence` | freshness policy | Required KBS cadence |

## Important non-equivalences

These mappings are intentionally one-way and conservative.

### Jurisdiction

`release_terms.jurisdiction_restriction = "CA"`

means:

> deployment policy requires Canada.

It does **not** mean:

> the workload is currently physically in Canada.

That second statement requires independent evidence.

### Serving-image measurement

An accepted WCM measurement means:

> this measurement is allowed by policy.

It does **not** prove:

> this is the measurement currently running.

Observed measurement must come from verified attestation/runtime evidence.

### Physical hardening

A WCM physical-hardening requirement means:

> this deployment is required to meet a physical-control posture.

It does **not** prove that those controls are present or effective.

### Builder/custodian identity

Manifest-declared identities are evidence assertions. DDC-WCM may compare them against independently pinned identities, delegation records, executor identities, or human authority.

## Runtime-only evidence

The following DDC-WCM fields cannot be established from the WCM manifest alone:

- `wcm.verification_result`;
- actual attestation evidence;
- actual executor identity;
- current runtime measurement;
- challenge freshness;
- revocation freshness;
- current physical state;
- actual jurisdiction;
- longitudinal/frequency state;
- independent supply-chain acceptability;
- contradiction resolution.

A mapper MUST leave these unknown unless supplied by an independent evidence source.

## Fail-closed rule

A manifest-only mapping MUST NOT produce `ALLOW`.

Until WCM verification and required independent runtime/context evidence are supplied, the correct state is non-ALLOW, normally `INSUFFICIENT_EVIDENCE`.
