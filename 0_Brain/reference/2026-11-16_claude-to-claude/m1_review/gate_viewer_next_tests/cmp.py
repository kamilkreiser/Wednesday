#!/usr/bin/env python3
"""Compare two diff_gate.py outputs record by record, byte for byte (setup records: only their `ok`/`gate` fields)."""
import json, sys
import re
KEY = re.compile(r"(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
def load(f):
    """Normalise ONLY the paired peer's key (random per run): every occurrence must be the same key within one run."""
    keys, out = set(), []
    for l in open(f):
        keys.update(KEY.findall(l))
        out.append(json.loads(KEY.sub("<PEER-KEY>", l)))
    assert len(keys) <= 1, f"more than one peer key in {f}: {keys}"
    print(f"{f}: 64-hex key occurrences normalised: {sum(1 for l in open(f) for _ in KEY.finditer(l))} (one key)")
    return out
a = load(sys.argv[1]); b = load(sys.argv[2])
diffs = 0
if len(a) != len(b):
    print("RECORD COUNT DIFFERS", len(a), len(b)); diffs += 1
for x, y in zip(a, b):
    if x != y:
        diffs += 1
        print("DIFF", x.get("kind"), x.get("label"))
        for k in sorted(set(x) | set(y)):
            if x.get(k) != y.get(k):
                print("   ", k, "A:", repr(x.get(k))[:300]); print("   ", k, "B:", repr(y.get(k))[:300])
n_hook = sum(1 for x in a if x["kind"] == "hook"); n_ipc = sum(1 for x in a if x["kind"] == "ipc")
print(f"records {len(a)} (hook {n_hook}, ipc {n_ipc}); differing records: {diffs}")
sys.exit(1 if diffs else 0)
