# Mapping Fixtures

These fixtures are synthetic interoperability examples. They do not contain real model weights, production identities, valid signatures, or confidential deployment evidence.

- `upstream/wcm-v0.15-manifest.synthetic.json` represents the shape of a WCM manifest reviewed against the pinned upstream v0.15 baseline.
- `mapped/ddc-wcm-from-wcm-v0.15.synthetic.json` is the expected conservative DDC-WCM mapping of that manifest.

The signature value in the upstream fixture is intentionally non-cryptographic. These fixtures test field mapping only; they MUST NOT be interpreted as WCM verification evidence.

The mapped fixture deliberately produces a non-ALLOW state because a WCM manifest alone cannot prove current runtime state, actual jurisdiction, or authoritative WCM verification.
