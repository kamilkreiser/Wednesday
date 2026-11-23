#!/usr/bin/env python3
"""QA-R3 item 5: undo ONLY the no-bytecode additions in the head's runner files and compare bytes with 379ceaa's.
usage: runner_undo_B.py <clone> <old rev> <new rev> <file>..."""
import subprocess, sys
c, old, new = sys.argv[1:4]
for f in sys.argv[4:]:
    o = subprocess.run(["git", "-C", c, "show", "%s:%s" % (old, f)], capture_output=True).stdout
    n = subprocess.run(["git", "-C", c, "show", "%s:%s" % (new, f)], capture_output=True).stdout
    u = n.replace(b"python3 -I -B ", b"python3 -I ").replace(b"python3 -B -c", b"python3 -c")
    u = u.replace(b"sys.dont_write_bytecode = True   # addendum 2, F-A: importing redact.py once wrote __pycache__/ here\n", b"")
    k = n.count(b" -B") + n.count(b"dont_write_bytecode")
    print("%-50s old=%d new=%d  -B/no-bytecode additions=%d  new-minus-additions == old: %s" % (f.split("/")[-1], len(o), len(n), k, u == o))
