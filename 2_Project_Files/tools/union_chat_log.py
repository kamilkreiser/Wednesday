#!/usr/bin/env python3
"""Union-merge chat_log.json across three sources on (ts, text).

Never drops a message. Reports per-source counts and what each source
uniquely contributed, because equal counts prove nothing — on 2026-09-07
both sides read 1630 and each held a message the other lacked.
"""
import json, sys

paths = sys.argv[1:-1]
out = sys.argv[-1]


def load(p):
    with open(p) as f:
        d = json.load(f)
    return d if isinstance(d, list) else d.get("messages", d.get("log", []))


def key(m):
    return (m.get("ts", ""), m.get("text", ""))


seen, merged, per_source = {}, [], {}
for p in paths:
    msgs = load(p)
    new = 0
    for m in msgs:
        k = key(m)
        if k not in seen:
            seen[k] = True
            merged.append(m)
            new += 1
    per_source[p] = (len(msgs), new)

merged.sort(key=lambda m: m.get("ts", ""))

for p, (total, new) in per_source.items():
    print(f"  {total:5d} msgs, {new:4d} unique-new  {p.split('/')[-1]}")
print(f"  UNION = {len(merged)}")

# Conservation assertion: the union must be >= every input.
for p, (total, _) in per_source.items():
    assert len(merged) >= total, f"union {len(merged)} < {p} {total} — REFUSING"

with open(out, "w") as f:
    json.dump(merged, f, indent=1, ensure_ascii=False)
print(f"  wrote {out}")
