from __future__ import annotations
import argparse,json,sys,subprocess
from importlib.resources import files
from pathlib import Path
import jsonschema
from .decision import public_decision
from .mapping import map_manifest
from .verifier import VerificationAdapterError, run_wcm_verify, sha256_file

def _schema():
    return json.loads(files("ddc_wcm").joinpath("data/ddc-wcm-evidence-v0.2.schema.json").read_text())

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

def verify_wcm_file(args)->int:
    try:
        evidence,report=run_wcm_verify(args.manifest,args.key_file,args.wcm_executable)
    except (VerificationAdapterError,OSError,subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}",file=sys.stderr); return 2
    doc={"schema":"ddc-wcm-verifier-evidence/1","evidence":evidence,"upstream_report":report}
    encoded=json.dumps(doc,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.write_text(encoded)
    else: print(encoded,end="")
    return 0 if evidence["result"]=="VALID" else 4

def map_file(args)->int:
    try:
        manifest=json.loads(args.manifest.read_text())
        manifest_hash=sha256_file(args.manifest.resolve(strict=True))
    except Exception as exc:
        print(f"ERROR: cannot read manifest: {exc}",file=sys.stderr); return 2
    bundle=map_manifest(manifest,manifest_hash,verification_evidence=None)
    encoded=json.dumps(bundle,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.write_text(encoded)
    else: print(encoded,end="")
    return 0

def verify_and_map_file(args)->int:
    try:
        manifest=json.loads(args.manifest.read_text())
        evidence,report=run_wcm_verify(args.manifest,args.key_file,args.wcm_executable)
        bundle=map_manifest(manifest,evidence["manifest_hash"],verification_evidence=evidence)
    except (VerificationAdapterError,OSError,subprocess.SubprocessError,ValueError) as exc:
        print(f"ERROR: {exc}",file=sys.stderr); return 2
    if args.receipt_output:
        args.receipt_output.write_text(json.dumps({"schema":"ddc-wcm-verifier-evidence/1","evidence":evidence,"upstream_report":report},indent=2,sort_keys=True)+"\n")
    encoded=json.dumps(bundle,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.write_text(encoded)
    else: print(encoded,end="")
    return 0 if evidence["result"]=="VALID" else 4

def main(argv=None)->int:
    p=argparse.ArgumentParser(prog="ddc-wcm",description="Public DDC-WCM interoperability CLI")
    p.add_argument("--version",action="version",version="ddc-wcm 0.2.0")
    sub=p.add_subparsers(dest="command",required=True)
    c=sub.add_parser("check"); c.add_argument("bundle",type=Path); c.add_argument("--json",action="store_true")
    v=sub.add_parser("verify-wcm",help="Execute upstream WCM verification and emit bound verifier evidence")
    v.add_argument("manifest",type=Path); v.add_argument("--key-file",type=Path,action="append",required=True)
    v.add_argument("--wcm-executable",default="wcm"); v.add_argument("--output",type=Path)
    m=sub.add_parser("map-wcm"); m.add_argument("manifest",type=Path); m.add_argument("--output",type=Path)\n    vm=sub.add_parser("verify-and-map",help="Execute upstream WCM verification and immediately map bound evidence")\n    vm.add_argument("manifest",type=Path); vm.add_argument("--key-file",type=Path,action="append",required=True); vm.add_argument("--wcm-executable",default="wcm"); vm.add_argument("--receipt-output",type=Path); vm.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    if args.command=="check": return check_bundle(args.bundle,args.json)
    if args.command=="verify-wcm": return verify_wcm_file(args)
    return map_file(args)

if __name__=="__main__": raise SystemExit(main())
