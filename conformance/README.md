# Public Conformance Harness

The public harness validates the open interoperability surface only.

It does **not** implement DDC radial-frequency reasoning, private scoring,
threshold derivation, hidden dimensions, learned baselines, or proprietary
contradiction-resolution logic.

## Run

```bash
python -m pip install -r requirements.txt
python conformance/run.py
```

A successful run requires:

1. the schema itself to be valid;
2. every vector input to validate against the schema;
3. public deterministic invariants to produce the vector's expected decision;
4. every expected reason code to appear in the public result.

The harness intentionally contains positive and non-ALLOW cases so rejecting
all inputs cannot satisfy conformance.
