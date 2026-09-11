from __future__ import annotations
import argparse,json,sys
from importlib.resources import files
from pathlib import Path
import jsonschema
from .decision import public_decision
from .mapping import map_manifest

def _schema():
    return json.loads(files("ddc_wcm").joinpath("data/ddc-wcm-evidence-v0.1.schema.json").read_text())

def check_bundle(path:Path,json_output:bool=False)->int:
    try: bundle=json.loads(path.read_text())
    except Exception as exc:
        print(f"ERROR: cannot read bundle: {exc}",file=sys.stderr); return 2
    schema=_schema(); cls=jsonschema.validators.validator_for(schema); cls.check_schema(schema)
    errors=sorted(cls(schema).iter_errors(bundle),key=lambda e:list(e.path))
    if errors:
        result={"schema_valid":False,"decision":"INSUFFICIENT_EVIDENCE","reason_codes":["PROFILE_INCOMPATIBLE"],"errors":[{"path":".".join(str(x) for x in e.path) or "<root>","message":e.message} for e in errors]}
        if json_output: print(json.dumps(result,indent=2,sort_keys=True))
        else:
            print("SCHEMA: FAIL")
            for x in result["errors"]: print(f"  {x['path']}: {x['message']}")
        return 1
    decision,reasons=public_decision(bundle)
    result={"schema_valid":True,"profile":bundle.get("profile"),"decision":decision,"reason_codes":reasons}
    if json_output: print(json.dumps(result,indent=2,sort_keys=True))
    else:
        print("SCHEMA: PASS"); print(f"PROFILE: {bundle.get('profile')}"); print(f"DECISION: {decision}"); print("REASONS: "+(", ".join(reasons) if reasons else "none"))
    return 0 if decision=="ALLOW" else 3

def map_file(args)->int:
    try: manifest=json.loads(args.manifest.read_text())
    except Exception as exc:
        print(f"ERROR: cannot read manifest: {exc}",file=sys.stderr); return 2
    bundle=map_manifest(manifest,args.manifest_hash,args.verification_result)
    encoded=json.dumps(bundle,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.write_text(encoded)
    else: print(encoded,end="")
    return 0

def main(argv=None)->int:
    p=argparse.ArgumentParser(prog="ddc-wcm",description="Public DDC-WCM interoperability CLI")
    p.add_argument("--version",action="version",version="ddc-wcm 0.1.0")
    sub=p.add_subparsers(dest="command",required=True)
    c=sub.add_parser("check"); c.add_argument("bundle",type=Path); c.add_argument("--json",action="store_true")
    m=sub.add_parser("map-wcm"); m.add_argument("manifest",type=Path); m.add_argument("--manifest-hash",required=True); m.add_argument("--verification-result",choices=["VALID","INVALID","UNKNOWN"],default="UNKNOWN"); m.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    return check_bundle(args.bundle,args.json) if args.command=="check" else map_file(args)

if __name__=="__main__": raise SystemExit(main())
