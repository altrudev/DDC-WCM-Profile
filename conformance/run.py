#!/usr/bin/env python3
"""Public DDC-WCM v0.2 conformance harness."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from ddc_wcm.decision import public_decision
SCHEMA_PATH=ROOT/"schema"/"ddc-wcm-evidence-v0.2.schema.json"

def main()->int:
    try: import jsonschema
    except ImportError:
        print("ERROR: missing dependency 'jsonschema'. Install with: pip install jsonschema",file=sys.stderr); return 2
    schema=json.loads(SCHEMA_PATH.read_text())
    cls=jsonschema.validators.validator_for(schema); cls.check_schema(schema); validator=cls(schema)
    paths=sorted((ROOT/"vectors").rglob("*.json"))
    if not paths: print("ERROR: no vectors found",file=sys.stderr); return 2
    failures=0
    for path in paths:
        vector=json.loads(path.read_text()); bundle=vector["input"]
        errors=sorted(validator.iter_errors(bundle),key=lambda e:list(e.path))
        if errors:
            failures+=1; print(f"FAIL {vector.get('id',path.name)}: schema validation")
            for error in errors:
                loc=".".join(str(x) for x in error.path) or "<root>"
                print(f"  {loc}: {error.message}")
            continue
        actual,codes=public_decision(bundle)
        expected=vector["expected_decision"]; expected_codes=vector.get("expected_reason_codes",[])
        ok=actual==expected and set(expected_codes).issubset(set(codes))
        if ok: print(f"PASS {vector['id']}: {actual} ({', '.join(codes) or 'no reasons'})")
        else:
            failures+=1; print(f"FAIL {vector['id']}"); print(f"  expected decision: {expected}"); print(f"  actual decision:   {actual}"); print(f"  expected reasons:  {expected_codes}"); print(f"  actual reasons:    {codes}")
    print(); print(f"{len(paths)-failures}/{len(paths)} vectors passed")
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
