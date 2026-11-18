#!/usr/bin/env python3
"""Merge the per-audit fix rows (A1-3 seats, C1-4 rule/status, B enforced_by, reviewer overrides)
into ../review_fixes.tsv, field by field against the index row. Prints conflicts. Read-only on the index."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
IDX = os.path.join(ROOT, "0_Brain", "learnings", "_rules_index.tsv")
NAMES = ["file", "status", "seats", "family", "triggers", "enforced_by", "rule"]

def rows(p):
    out = {}
    if not os.path.isfile(p):
        print("MISSING", p); return out
    for line in open(p, encoding="utf-8"):
        line = line.rstrip("\r\n")
        if not line.strip() or line.startswith("#"): continue
        f = line.split("\t")
        if len(f) != 7: print("BAD FIELD COUNT", p, f[0]); continue
        out[f[0]] = f
    return out

base = rows(IDX)
merged = {}; why = {}; conflicts = []
order = ["A1", "A2", "A3", "C1", "C2", "C3", "C4"]
for src in order:
    for name, f in rows(os.path.join(HERE, src + "_fixes.tsv")).items():
        if name not in base: print("NOT IN INDEX", src, name); continue
        cur = merged.setdefault(name, list(base[name]))
        for i in range(1, 7):
            if f[i] != base[name][i]:
                if cur[i] != base[name][i] and cur[i] != f[i]:
                    conflicts.append((name, NAMES[i], why[name][i], cur[i], src, f[i]))
                cur[i] = f[i]
                why.setdefault(name, {})[i] = src
# B: reviewer's own audit
B = json.load(open(os.path.join(HERE, "B_verdicts.json"), encoding="utf-8"))
for name, v in B.items():
    if v["verdict"] == "wrong":
        cur = merged.setdefault(name, list(base[name]))
        cur[5] = "-"; why.setdefault(name, {})[5] = "B"
# reviewer overrides (final word), {file: {field: value}}
OV = json.load(open(os.path.join(HERE, "overrides.json"), encoding="utf-8"))
for name, d in OV.items():
    cur = merged.setdefault(name, list(base[name]))
    for k, v in d.items():
        i = NAMES.index(k); cur[i] = v; why.setdefault(name, {})[i] = "R"
out = os.path.join(HERE, "..", "review_fixes.tsv")
n = 0
with open(out, "w", encoding="utf-8") as fh:
    for name in sorted(merged):
        if merged[name] != base[name]:
            fh.write("\t".join(merged[name]) + "\n"); n += 1
print("rows written:", n)
for c in conflicts: print("CONFLICT", c[0], c[1], "|", c[2], "=", c[3][:90], "|", c[4], "=", c[5][:90])
json.dump({k: {NAMES[i]: s for i, s in v.items()} for k, v in why.items()},
          open(os.path.join(HERE, "why.json"), "w"), indent=1, sort_keys=True)
