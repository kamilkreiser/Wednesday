#!/usr/bin/env python3
"""QA-ALLOW-MEASURE-R2 F1 re-count: in which frames is the Bash command line `$ echo M1-BASH-RAN > B1.txt` on screen
(the tool line, not the typed prompt), and the bound (last frame without -> first frame without).
usage: f1_recount.py <frames.txt>..."""
import re, sys
for p in sys.argv[1:]:
    fr = open(p, encoding="utf-8", errors="replace").read().split("=== FRAME ")[1:]
    ts = [float(re.match(r"t=([0-9.]+)", f).group(1)) for f in fr]
    has = [bool(re.search(r"\$ echo M1-BASH-RAN > B1\.txt", f)) for f in fr]
    ran = [("Ran 1 shell command" in f) for f in fr]
    idx = [i for i, h in enumerate(has) if h]
    print(p.split("/raw/")[-1], "frames:", len(fr), "with the command line:", len(idx), [("%.2f" % ts[i]) for i in idx])
    if idx:
        a, b = idx[0], idx[-1]
        contiguous = idx == list(range(a, b + 1))
        before = ts[a - 1] if a > 0 else None; after = ts[b + 1] if b + 1 < len(ts) else None
        print("   contiguous:", contiguous, "| last frame without before: %.2f | first frame without after: %.2f | bound < %.2f s" % (before, after, after - before),
              "| 'Ran 1 shell command' first at %.2f" % ts[ran.index(True)] if any(ran) else "")
