#!/usr/bin/env python3
"""Seat R 44th -- widen tools/sweep_edit_ra44.py's predecessor-generation class by the EXACT alternative 43.
The lineage's ONE accepted exception to report-not-edit (A43-plan:2, Wednesday): a blind residue scanner is
worse than none. A hand repair a replay of the port would CLOBBER. NEVER a bracket class ([34][0-9] would match
my own generation and my successor's). COUNT-ASSERTED both before and after; comment lines are never touched.
usage: fix_sweep_ra44.py <path to tools/sweep_edit_ra44.py>      (writes in place; record it in your handover)"""
import ast, sys
P = sys.argv[1]
OLD, NEW = "|40|41|42)", "|40|41|42|43)"
WANT_LINES, WANT_OCC = 5, 9                    # R 43rd's census for the 42 widening; the drafter's port reads the same
with open(P, encoding="utf-8") as f: lines = f.read().split("\n")
live = [(i + 1, l.count(OLD)) for i, l in enumerate(lines) if l.count(OLD) and not l.lstrip().startswith("#")]
com = [(i + 1, l.count(OLD)) for i, l in enumerate(lines) if l.count(OLD) and l.lstrip().startswith("#")]
print("census of %r: LIVE lines %d (%d occ); COMMENT lines %d (not touched)" % (OLD, len(live), sum(n for _, n in live), len(com)))
if (len(live), sum(n for _, n in live)) != (WANT_LINES, WANT_OCC):
    print("REFUSED: want %d live lines / %d occurrences" % (WANT_LINES, WANT_OCC)); sys.exit(2)
out = [l.replace(OLD, NEW) if (l.count(OLD) and not l.lstrip().startswith("#")) else l for l in lines]
HDR = ["# [R44-HDR] Seat R 44th -- sweep_edit_ra44.py: the predecessor-generation class is widened by ONE exact",
       "# [R44-HDR] alternative, the number forty-three, at 9 live occurrences across 5 lines. No bracket class.",
       "# [R44-HDR] This paragraph spells the classes in words so the census above stays honest."]
res = "\n".join(HDR) + "\n" + "\n".join(out)
if res.count(NEW) != WANT_OCC or res.count(OLD) != 0:
    print("REFUSED: post-edit count new=%d old=%d" % (res.count(NEW), res.count(OLD))); sys.exit(3)
ast.parse(res)
with open(P, "w", encoding="utf-8") as f: f.write(res)
print("WROTE %s (%d lines, %d occurrences widened, %d header lines, ast.parse OK)" % (P, WANT_LINES, WANT_OCC, len(HDR)))
