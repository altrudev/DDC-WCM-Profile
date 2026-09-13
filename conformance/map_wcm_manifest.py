#!/usr/bin/env python3
"""Compatibility wrapper around the packaged DDC-WCM v0.2 mapper."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from ddc_wcm.mapping import map_manifest
from ddc_wcm.verifier import sha256_file

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("manifest",type=Path)
    p.add_argument("--verification-evidence",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    manifest=json.loads(args.manifest.read_text())
    evidence=None
    if args.verification_evidence:
        evidence=json.loads(args.verification_evidence.read_text())["evidence"]
    bundle=map_manifest(manifest,sha256_file(args.manifest.resolve(strict=True)),verification_evidence=evidence)
    encoded=json.dumps(bundle,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.write_text(encoded)
    else: print(encoded,end="")
    return 0
if __name__=="__main__": raise SystemExit(main())
