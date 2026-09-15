#!/usr/bin/env python3
"""d6_ranges.py <before.md> <after.md> <sections: "a-b,c-d" 0-based [start,end) on the BEFORE file> — D6 for doc_patch.

2026-09-15 23:1x (KS-1045 A r1, IMPROVEMENTS row 92): D6 used to read each hunk's DECLARED old range from the `@@` header.
The model's headers are routinely miscounted (D2 needs --recount on most runs), and a hunk whose context runs past EOF
declares a range the file does not have — so a CORRECT edit inside `## Stage gate summary` (the last section, 8 lines)
read as "170-176 outside the required sections". A header is a representation of the edit; the edit itself is the
difference between before.md and after.md. This measures THAT: every changed/deleted/inserted region, located on the
BEFORE file (0-based, half-open), must lie inside one of the given section ranges. Prints the offending regions, one per
line, as 1-based inclusive old-file lines; exit 0 when none. Arms: local-model/tests/d6_arms.sh."""
import difflib
import sys

before = open(sys.argv[1], encoding="utf-8").read().split("\n")
after = open(sys.argv[2], encoding="utf-8").read().split("\n")
ranges = []
for part in sys.argv[3].split(","):
    part = part.strip()
    if not part:
        continue
    a, b = part.split("-")
    ranges.append((int(a), int(b)))
bad = []
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
    if tag == "equal":
        continue
    # an insertion at i1 (i1 == i2) belongs to the line it is inserted before; anchor it on i1-1 when i1 is at a section's end
    s, e = (i1, i2) if i2 > i1 else (max(i1 - 1, 0), i1)
    if not any(s >= a and e <= b for a, b in ranges):
        bad.append(f"{s + 1}-{max(e, s + 1)}")
for b_ in bad:
    print(b_)
sys.exit(1 if bad else 0)
