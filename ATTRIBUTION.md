# Attribution and Upstream Relationship

## Weight Custody Manifest (WCM)

**Weight Custody Manifest (WCM)** is an open standard introduced publicly by **OPAQUE Systems** on September 9, 2026 for governing when and where protected AI model weights may be unlocked in customer-controlled, sovereign, and on-premises infrastructure.

The public launch and surrounding work prominently involve **Imran Siddique, Chief Platform Officer at OPAQUE Systems**, who is quoted in OPAQUE's WCM announcement describing the purpose and trust model of the standard.

Upstream WCM materials are maintained in the AgenTrust ecosystem, including the public Weight Custody Manifest repository and related specification, SDK, threat-model, and conformance materials.

Official upstream references:

- OPAQUE WCM announcement: https://www.opaque.co/resources/articles/opaque-introduces-an-open-standard-that-unlocks-frontier-models-for-sovereign-and-on-premises-deployment
- WCM project: https://agentrust-io.com/wcm
- WCM source repository: https://github.com/agentrust-io/weight-custody-manifest
- OPAQUE Systems: https://www.opaque.co/

## DDC-WCM Profile

**DDC-WCM Profile** is an independent interoperability and assurance profile created by **Altru.dev**.

This project does not claim authorship or ownership of WCM. It treats WCM as an upstream external protocol and defines a separate evidence and assurance boundary around WCM outputs.

The DDC-WCM Profile focuses on questions outside WCM's core custody-validation role, including:

- cross-evidence coherence;
- authority continuity;
- executor and runtime consistency;
- lineage consistency;
- physical-assurance separation;
- jurisdiction evidence;
- supply-chain acceptability;
- contradiction reporting;
- longitudinal and frequency-oriented observations;
- binding assurance outcomes into DDC Action Receipts.

## Independence statement

DDC-WCM Profile is **not affiliated with, sponsored by, endorsed by, or maintained by OPAQUE Systems, Imran Siddique, AgenTrust, or the WCM maintainers**, unless such a relationship is explicitly established in writing in the future.

References to WCM, OPAQUE Systems, Imran Siddique, and AgenTrust are for attribution, interoperability, research, and technical identification of the upstream work.

## Trademark and project-name notice

All third-party names, marks, project names, and repository names remain the property of their respective owners.

Use of the term **WCM** in the name **DDC-WCM Profile** identifies the upstream protocol with which this independent profile interoperates; it does not imply ownership, endorsement, certification, or official status.

## Licensing boundary

Where upstream WCM materials are referenced, their own licensing terms apply to those materials.

The Apache-2.0 license in this repository applies only to the public DDC-WCM Profile materials distributed here, unless a file explicitly states otherwise.

The proprietary DDC assurance engine and unpublished DDC methods are outside this repository and outside the scope of this repository's Apache-2.0 grant.
