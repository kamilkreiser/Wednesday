#!/usr/bin/env python3
"""Seat R 44th -- re-hash a _TOOL_HASHES table against a TRUE record folder (never a promoted copy).
Row shape is `<rel> <sha16> <lines>` (R 43rd read it backwards once: EQUAL 0 / MISSING 451).
usage: verify_table_ra44.py <record folder> <table file>      prints: N rows EQUAL a DIFFER b MISSING c, then the odd rows,
then two CONTROLS that must fire (a tampered row reads DIFFER; a row with a fabricated path reads MISSING)."""
import hashlib, os, sys
root, table = sys.argv[1], sys.argv[2]
with open(table, encoding="utf-8") as f:
    rows = [l.split() for l in f.read().splitlines() if l.strip()]
assert rows and all(len(r) == 3 for r in rows), "table rows must be <rel> <sha16> <lines>"
def check(rel, want):
    p = os.path.join(root, rel)
    if not os.path.isfile(p): return "MISSING"
    with open(p, "rb") as g: h = hashlib.sha256(g.read()).hexdigest()[:16]
    return "EQUAL" if h == want else "DIFFER"
res = [(check(rel, h), rel) for rel, h, _n in rows]
eq = sum(1 for s, _ in res if s == "EQUAL"); df = [r for s, r in res if s == "DIFFER"]; ms = [r for s, r in res if s == "MISSING"]
print("%d rows EQUAL %d DIFFER %d MISSING %d" % (len(rows), eq, len(df), len(ms)))
for r in df: print("  DIFFER ", r)
for r in ms: print("  MISSING", r)
c1 = check(rows[0][0], "0" * 16)
c2 = check("no/such/file.py", rows[0][1])
print("CONTROL tampered row reads %s (must be DIFFER); fabricated path reads %s (must be MISSING)" % (c1, c2))
sys.exit(0 if (c1 == "DIFFER" and c2 == "MISSING") else 4)
