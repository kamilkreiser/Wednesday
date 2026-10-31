#!/usr/bin/env python3
"""Render evidence/mutants_run.log into the verdict's markdown table."""
import json
G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate61-r1r2-1868"
rows = ["| # | Mutant | W real-Postgres (8) | W unit (19) | Gate 61 probe (10) | Result |", "|---|---|---|---|---|---|"]
k = n = 0
for l in open(f"{G}/evidence/mutants_run.log"):
    if '"mutant"' not in l:
        continue
    d = json.loads(l)
    mid, _, desc = d["mutant"].partition(" ")
    def cell(j):
        v = d["jobs"][j]
        if v["invalid"]:
            return "INVALID (0 collected)"
        if not v["killed_by"]:
            return "survives"
        return f"killed ({len(v['killed_by'])}): " + "; ".join(x.split(" ")[0] for x in v["killed_by"])
    n += 1
    k += 1 if d["killed"] else 0
    rows.append(f"| {mid} | {desc} | {cell('w_integ')} | {cell('w_unit')} | {cell('probe')} | **{'KILLED' if d['killed'] else 'SURVIVED'}** |")
print("\n".join(rows))
print(f"\n**{k}/{n} killed.**")
