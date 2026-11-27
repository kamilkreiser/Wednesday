#!/usr/bin/env python3
"""green_faults.py <work dir> <socket dir> - what rebuild, check, doctor and status SAY when an input is unreadable or cut."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
work, sock = sys.argv[1], sys.argv[2]; pgd = work + "/pg"; root = work + "/tree"
P = lambda s: print(s, flush=True)
rows = base_tree(root)
w(root, L + "_rules_index.tsv", "# h\n" + "\n".join(rows + [row("2027-01-06_q-locked.md")]) + "\n")
w(root, "0_Brain/daily/2027-01-20.md", "# d\n\n## Sessions\n- 06:19 the word is qzdailylocked here.\n")
w(root, L + "2027-01-06_q-locked.md", FM + "\n# L\n\nqzlessonlocked\n")
w(root, "0_Brain/skills/big.md", "# big\n\nqzbigstart " + "word " * 40000 + " qzbigend\n")
def show(label):
    for c in (["rebuild"], ["check"], ["doctor"], ["status"]):
        rc, out = tool(c, root, pgd, sock); ls = out.strip().split("\n")
        pick = [l.strip() for l in ls if l.startswith(("rebuild: ", "check: ", "OK ", "WARN ")) or "skipped for a fault" in l or "unreadable:" in l or "left out:" in l or "faults" in l]
        P("  [%s] %-7s rc %d : %s" % (label, c[0], rc, " || ".join(p[:210] for p in pick)))
P("== G0. control: everything readable"); show("clean")
rc, so = tool(["search", "qzbigend"], root, pgd, sock); P("  search for the word AFTER the 80,000-character cut (qzbigend): %s" % so.strip().split("\n")[-1][:120])
rc, so = tool(["search", "qzbigstart"], root, pgd, sock); P("  search for the word before the cut (control): %s" % so.strip().split("\n")[-1][:80])
P("== G1. the seat's own DAILY NOTE is unreadable (mode 000)")
os.chmod(root + "/0_Brain/daily/2027-01-20.md", 0); show("daily 000")
P("== G2. also a LESSON is unreadable (mode 000)")
os.chmod(root + "/" + L + "2027-01-06_q-locked.md", 0); show("daily+lesson 000")
P("== G3. the whole daily FOLDER is unreadable (mode 000)")
os.chmod(root + "/0_Brain/daily/2027-01-20.md", 0o644); os.chmod(root + "/" + L + "2027-01-06_q-locked.md", 0o644); os.chmod(root + "/0_Brain/daily", 0); show("daily folder 000")
os.chmod(root + "/0_Brain/daily", 0o755)
P("== G4. the seat's own LEDGER is a symlink (skipped, not 'unreadable')")
os.rename(root + "/" + L + "_ledger.md", root + "/" + L + "_ledger.real"); os.symlink("_ledger.real", root + "/" + L + "_ledger.md"); show("ledger symlink")
rc, so = tool(["stop"], root, pgd, sock); P("stop rc %d" % rc)
