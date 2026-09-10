# Adversarial Vectors

These vectors define public interoperability scenarios and expected dispositions. They are not a disclosure of proprietary DDC inference logic.

Initial flagship cases:

- **DW-001 — Valid but wrong authority**: valid model, signature, attestation, and environment; independently pinned authority does not match. Expected: BLOCK.
- **DW-002 — Valid but malicious workload**: WCM-valid measurement; independent supply-chain assurance finds prohibited behavior. Expected: BLOCK.
- **DW-003 — Valid but contradictory jurisdiction**: WCM valid; independent location evidence materially conflicts. Expected: REQUIRE_HUMAN or BLOCK by policy.
- **DW-004 — Individually valid, temporally anomalous**: cryptographically valid release burst materially outside expected behavior. Expected: REQUIRE_HUMAN / containment / BLOCK by policy.
- **DW-005 — Attestation-key compromise simulation**: cryptographically valid attestation conflicts with independently established executor lineage/state. Expected: BLOCK.

Future vectors should separate:

- valid;
- invalid;
- contradictory;
- insufficient-evidence;
- execution-divergence cases.

A conforming test harness MUST include positive ALLOW cases so an implementation cannot pass by rejecting every request.
