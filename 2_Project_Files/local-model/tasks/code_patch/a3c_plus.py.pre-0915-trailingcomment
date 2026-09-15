#!/usr/bin/env python3
"""a3c_plus.py <input.json> <product section file> — every line the BRIEF adds must be added.

2026-09-15 22:0x (KS-976 B r1): the model changed both `must_change` sites (A3b 2/2) and DROPPED the insert-only
hunk that defined the helper those sites call — tsc failed three assertions later. A3b sees removals only; this
is its twin for ADDITIONS: `defect_line.expected_plus` (built from the '+' lines of the brief's edit blocks) must
each appear as a '+' line in the PRODUCT section, compared whitespace-stripped. Prints the missing lines, one per
line; exit 0 when none. Used by checker.sh as A3c; runnable standalone on a run's artefacts (that is the arm)."""
import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
exp = d.get("defect_line", {}).get("expected_plus", [])
sec = open(sys.argv[2], encoding="utf-8", errors="replace").read().split("\n")
added = {l[1:].strip() for l in sec if l.startswith("+") and not l.startswith("+++")}
missing = [e for e in exp if e.strip() and e.strip() not in added]
for m in missing:
    print(m)
sys.exit(1 if missing else 0)
