# Why DDC and WCM Are Combined

DDC-WCM Profile was not created to repackage WCM, attach DDC to another project, or duplicate work already performed by OPAQUE or the WCM maintainers.

WCM was selected because it presents a particularly clear example of a broader assurance problem DDC is intended to address.

WCM can determine whether model-weight custody evidence satisfies a defined cryptographic and policy framework. That is an important and distinct function.

DDC asks a different question:

**Does the total available evidence describe one coherent reality in which the proposed action should actually be allowed?**

Those questions are related, but they are not equivalent.

A WCM verification result may establish that an attestation, manifest, measurement, authority condition, or key-release requirement is valid according to WCM. DDC does not replace that determination.

Instead, DDC examines whether that valid result remains consistent with other relevant evidence, such as:

- executor identity;
- human and organizational authority;
- runtime state;
- artifact and derivative lineage;
- supply-chain evidence;
- physical-control assumptions;
- jurisdiction evidence;
- freshness across multiple evidence channels;
- contradictory observations;
- unusual longitudinal or frequency behavior.

The reason for combining the two systems is therefore architectural rather than organizational.

WCM provides an authoritative custody-evidence channel.

DDC provides an independent coherence layer around that evidence.

DDC Action Receipt can then bind the resulting decision to the consequential action that actually occurred.

In simplified form:

```text
WCM
  answers:
  "Does the custody evidence satisfy the custody policy?"

DDC
  answers:
  "Does this evidence remain coherent with the wider state of the system?"

DDC Action Receipt
  answers:
  "Can we prove why the resulting action was allowed, blocked, or escalated?"
```

This separation is intentional.

The DDC-WCM Profile is therefore best understood as an interoperability experiment around a general principle:

**A cryptographically valid assertion can still exist inside an incoherent system state.**

WCM is a strong and concrete environment in which to test that principle because it already defines meaningful custody, attestation, lineage, and release semantics.

The goal of this profile is not to make DDC dependent on WCM.

The goal is to test whether DDC can consume a mature external trust signal without weakening it, duplicating it, or confusing cryptographic validity with broader assurance.

The same architectural pattern may later apply to other evidence systems, including software provenance, identity credentials, hardware attestation, signed policy decisions, execution receipts, and physical-device authorization.

WCM is the first interoperability target because its trust boundary makes this distinction unusually clear.
