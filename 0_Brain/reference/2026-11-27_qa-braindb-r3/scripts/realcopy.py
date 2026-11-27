#!/usr/bin/env python3
"""realcopy.py <lanecopy brain-db dir> <real tree> <dest tree>: copy ONLY the files the lane's own scan() would index
(its shipped wednesday.scope, all deciders applied) into a scratch tree. Read-only on the real tree. Also prints
real-tree measurements of the rules index against lesson file names (names only)."""
import sys, os, shutil
lane, real, dest = sys.argv[1:4]
sys.path.insert(0, lane)
sys.dont_write_bytecode = True
import braindb_index as bi
sc = bi.load_scope(os.path.join(lane, "scope", "wednesday.scope"), "wednesday")
res = bi.scan(real, sc, want_text=False)
n = 0
for rel in sorted(res["files"]):
    d = os.path.join(dest, rel); os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copyfile(os.path.join(real, rel), d); n += 1
kinds = {}
for rel, f in res["files"].items(): kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1
print("copied %d files: %s" % (n, kinds))
print("skipped %d, unreadable %d, untagged %d, rejected rows %d" % (len(res["skipped"]), len(res["unreadable"]), len(res["untagged"]), res["rejected_rows"]))
# names-only measurement: rules-index keys vs lesson file names on disk
L = os.path.join(real, "0_Brain/learnings")
names = set(x for x in os.listdir(L) if x.startswith("20") and x.endswith(".md"))
rows, rej = bi.read_rules(bi.read_file(os.path.join(L, "_rules_index.tsv"))[1])
keys = set(r["base"] for r in rows)
orphan = sorted(k for k in keys if k not in names)
norow = sorted(x for x in names if x not in keys)
other_only = set()
for k in keys:
    rs = [r for r in rows if r["base"] == k]
    if not any(("all" in r["seats"] or "wednesday" in r["seats"]) for r in rs): other_only.add(k)
print("REAL TREE: lesson files %d ; well-formed rows %d ; rejected rows %d ; distinct keys %d" % (len(names), len(rows), len(rej), len(keys)))
print("REAL TREE: rows whose key matches NO lesson file: %d %s" % (len(orphan), orphan[:5]))
print("REAL TREE: lesson files with NO row (decided by tier alone): %d" % len(norow))
for x in norow[:12]: print("     no row: " + x)
print("REAL TREE: keys scoped to other seats only: %d ; of those matching no file: %d" % (len(other_only), len([k for k in other_only if k not in names])))
import unicodedata
print("REAL TREE: lesson names not ASCII: %d ; names not NFC: %d" % (len([x for x in names if not x.isascii()]), len([x for x in names if unicodedata.normalize('NFC', x) != x])))
