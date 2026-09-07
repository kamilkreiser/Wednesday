#!/usr/bin/env python3
"""Union-merge decisions.json across sources on card `id`.

Rule (learned the hard way on 2026-09-07, when a blanket checkout of
0_Brain/dashboard/data destroyed four of Kam's rulings): union on `id`, and
where a card appears in more than one source, KEEP THE RULED VERSION.
A ruled card never loses to an open one. Nothing is ever dropped.
"""
import json, sys

paths = sys.argv[1:-1]
out = sys.argv[-1]


def load(p):
    with open(p) as f:
        d = json.load(f)
    return d if isinstance(d, list) else d.get("decisions", [])


def is_ruled(c):
    return c.get("status") == "ruled" or bool(c.get("ruled_choice"))


merged = {}
order = []
per_source = {}
upgrades = []

for p in paths:
    cards = load(p)
    new = 0
    for c in cards:
        cid = c.get("id")
        if cid is None:
            continue
        if cid not in merged:
            merged[cid] = c
            order.append(cid)
            new += 1
        elif is_ruled(c) and not is_ruled(merged[cid]):
            # a ruled version beats an open one, whichever side it came from
            upgrades.append(cid)
            merged[cid] = c
    per_source[p] = (len(cards), new)

for p, (total, new) in per_source.items():
    print(f"  {total:4d} cards, {new:3d} unique-new  {p.split('/')[-1]}")
print(f"  UNION = {len(order)} cards")
if upgrades:
    print(f"  kept the RULED version for: {', '.join(upgrades)}")

# Conservation: the union must be at least as large as every input.
for p, (total, _) in per_source.items():
    assert len(order) >= total, f"union {len(order)} < {p} {total} — REFUSING"

# No ruled card may be dropped: every ruled id in any source must be ruled in the union.
ruled_in = set()
for p in paths:
    for c in load(p):
        if is_ruled(c) and c.get("id"):
            ruled_in.add(c["id"])
lost = [i for i in ruled_in if not is_ruled(merged.get(i, {}))]
assert not lost, f"RULED cards would lose their ruling: {lost} — REFUSING"
print(f"  {len(ruled_in)} ruled cards, all still ruled in the union")

with open(out, "w") as f:
    json.dump([merged[i] for i in order], f, indent=1, ensure_ascii=False)
print(f"  wrote {out}")
