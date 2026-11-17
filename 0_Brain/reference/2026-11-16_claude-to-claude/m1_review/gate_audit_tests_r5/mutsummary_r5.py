#!/usr/bin/env python3
"""Summarise mutate_r5 logs: every `test X ... FAILED` line; gate_r5 tests are the ones named r5_*.
usage: mutsummary_r5.py <mutlogs dir> <out.txt>"""
import os, re, sys
d, outp = sys.argv[1], sys.argv[2]
lines = []
for f in sorted(os.listdir(d)):
    if not f.endswith(".log"): continue
    log = open(os.path.join(d, f)).read()
    failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", log, re.M)))
    mine = [t for t in failed if t.startswith("r5_")]
    seat = [t for t in failed if not t.startswith("r5_")]
    ce = "error[E" in log or "could not compile" in log
    status = "COMPILE ERROR" if ce else ("KILLED" if failed else "SURVIVED")
    lines.append(f"{f[:-4]} {status}: branch tests failed {len(seat)} {seat}; gate_r5 failed {len(mine)} {mine}")
open(outp, "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
