from __future__ import annotations

BLOCKING_CODES={"WCM_INVALID","MANIFEST_IDENTITY_MISMATCH","WEIGHTS_IDENTITY_MISMATCH","EXECUTOR_IDENTITY_MISMATCH","AUTHORITY_SCOPE_MISMATCH","AUTHORITY_EXPIRED","ATTESTATION_MISSING","CHALLENGE_REPLAY","REVOCATION_KNOWN","RUNTIME_STATE_CONTRADICTION","LINEAGE_CONTRADICTION","SUPPLY_CHAIN_POLICY_FAILURE","EXECUTOR_LINEAGE_CONTRADICTION","CRITICAL_CONTRADICTION","EXECUTION_DIVERGENCE"}
ESCALATION_CODES={"JURISDICTION_CONTRADICTION","FREQUENCY_ANOMALY"}
EVIDENCE_CODES={"WCM_UNKNOWN","ATTESTATION_STALE","JURISDICTION_NOT_ESTABLISHED","PHYSICAL_ASSURANCE_INSUFFICIENT","INSUFFICIENT_EVIDENCE","PROFILE_INCOMPATIBLE","ASSURANCE_ENGINE_ERROR"}

def public_decision(bundle: dict) -> tuple[str,list[str]]:
    codes=[]
    verification=bundle.get("wcm",{}).get("verification_result")
    if verification=="INVALID": codes.append("WCM_INVALID")
    elif verification=="UNKNOWN": codes.append("WCM_UNKNOWN")
    a=bundle.get("authority",{})
    if a.get("status")=="contradictory" and a.get("pinned_authority") and a.get("presented_authority") and a["pinned_authority"]!=a["presented_authority"]:
        codes.append("AUTHORITY_SCOPE_MISMATCH")
    e=bundle.get("executor",{})
    if e.get("independently_pinned_executor_id") and e.get("executor_id") and e["independently_pinned_executor_id"]!=e["executor_id"]:
        codes.append("EXECUTOR_LINEAGE_CONTRADICTION")
    if bundle.get("freshness",{}).get("assessment") in {"STALE","MIXED"}: codes.append("ATTESTATION_STALE")
    if bundle.get("lineage",{}).get("assessment")=="CONTRADICTORY": codes.append("LINEAGE_CONTRADICTION")
    j=bundle.get("jurisdiction",{}).get("assessment")
    if j=="CONTRADICTORY": codes.append("JURISDICTION_CONTRADICTION")
    elif j=="NOT_ESTABLISHED": codes.append("JURISDICTION_NOT_ESTABLISHED")
    if bundle.get("physical",{}).get("assessment")=="INSUFFICIENT": codes.append("PHYSICAL_ASSURANCE_INSUFFICIENT")
    sc=bundle.get("supply_chain",{})
    if sc.get("integrity")=="INVALID" or sc.get("acceptability")=="FAIL": codes.append("SUPPLY_CHAIN_POLICY_FAILURE")
    if bundle.get("frequency",{}).get("assessment")=="ANOMALOUS": codes.append("FREQUENCY_ANOMALY")
    for contradiction in bundle.get("contradictions",[]):
        if contradiction.get("resolved") is False:
            code=contradiction.get("reason_code")
            if code: codes.append(code)
            elif contradiction.get("severity")=="critical": codes.append("CRITICAL_CONTRADICTION")
    seen=set(); codes=[c for c in codes if not (c in seen or seen.add(c))]
    if any(c in BLOCKING_CODES for c in codes): return "BLOCK",codes
    if any(c in ESCALATION_CODES for c in codes): return "REQUIRE_HUMAN",codes
    if any(c in EVIDENCE_CODES for c in codes): return "INSUFFICIENT_EVIDENCE",codes
    return "ALLOW",codes
