#!/usr/bin/env python3
"""misc.py <work dir> <socket dir> - small direct probes of the real (scratch-copied) code."""
import os, sys, shutil, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
work, sock = sys.argv[1], sys.argv[2]; pgd = work + "/pg"
P = lambda s: print(s, flush=True)
lane = os.path.dirname(TOOL); pf = os.path.dirname(lane)
P("== M1. a folder ABOVE a table folder is a symlink (0_Brain -> another tree's 0_Brain)")
other = work + "/othertree"; rows = base_tree(other)
w(other, L + "2027-01-05_q-foreign.md", FM + "\n# F\n\nThe word is qzforeign here.\n"); rows.append(row("2027-01-05_q-foreign.md"))
w(other, L + "_rules_index.tsv", "# h\n" + "\n".join(rows) + "\n")
root = work + "/m1"; os.makedirs(root); w(root, "CLAUDE.md", "# Rules\n\n0. **First.** qzownrules\n"); os.symlink(other + "/0_Brain", root + "/0_Brain")
rc, out = tool(["rebuild"], root, pgd, sock)
P("  rebuild rc %d ; last line: %s" % (rc, out.strip().split("\n")[-1][:200]))
P("  says 'sits under a symlink': %d time(s)" % out.count("sits under a symlink"))
if rc == 0:
    d, e = dump(sock); P("  in the index: qzforeign %d qzcontrol %d (want 0 0); own rules file qzownrules %d (control, want > 0)" % (d.count("qzforeign"), d.count("qzcontrol"), d.count("qzownrules")))
P("== M1b. only learnings/ is a symlink into the other tree; and M1c. the tree ROOT itself reached through a symlink")
root = work + "/m1b"; rows = base_tree(root); shutil.rmtree(root + "/0_Brain/learnings"); os.symlink(other + "/0_Brain/learnings", root + "/0_Brain/learnings")
rc, out = tool(["rebuild"], root, pgd, sock); P("  M1b rebuild rc %d ; %s" % (rc, out.strip().split("\n")[-1][:220]))
os.symlink(other, work + "/rootlink")
rc, out = tool(["rebuild"], work + "/rootlink", pgd, sock); d, e = dump(sock)
P("  M1c (BRAINDB_ROOT is a symlink to a tree: the tree named IS that tree) rebuild rc %d ; qzforeign %d" % (rc, (d or "").count("qzforeign")))
P("== M2. init / start on a seat with NO scope file at all (a tree named TUESDAY)")
t = work + "/sim/TUESDAY/2_Project_Files"; os.makedirs(t + "/fleet/cockpit"); os.makedirs(t + "/tools")
shutil.copytree(lane, t + "/brain-db", ignore=shutil.ignore_patterns("evidence", "__pycache__"))
shutil.copy(pf + "/fleet/cockpit/seat_resolve.sh", t + "/fleet/cockpit/"); shutil.copy(pf + "/tools/seat_note.sh", t + "/tools/")
TT = t + "/brain-db/braindb.sh"
for c in (["status"], ["doctor"], ["up"], ["search", "x"], ["init"], ["start"], ["stop"]):
    rc, out = tool(c, other, work + "/pg-tue", sock, toolpath=TT)
    P("  %-7s rc %d ; cluster directory exists: %s ; lock file: %s ; %s" % (c[0], rc, os.path.exists(work + "/pg-tue"), os.path.exists(work + "/pg-tue.lock"), out.strip().split("\n")[-1][:120]))
P("== M3. odd scope files")
good = open(lane + "/scope/wednesday.scope").read()
cases = {"invalid UTF-8 bytes": good.encode() + b"\n# \xff\xfe\n", "a NUL byte": good.encode() + b"\n\x00\n", "CRLF line ends": good.replace("\n", "\r\n").encode(),
         "a BOM first": b"\xef\xbb\xbf" + good.encode(), "seat line twice (tuesday then wednesday)": ("seat tuesday\n" + good).encode(),
         "own_clients widened to datasec": good.replace("own_clients secuura general wednesday wed", "own_clients secuura general wednesday wed datasec").encode(),
         "empty file": b"", "allow line with a TAB separator": good.replace("allow skill        0_Brain", "allow\tskill\t0_Brain").encode()}
for what, data in cases.items():
    sc = work + "/odd.scope"; open(sc, "wb").write(data)
    rc, out = tool(["rebuild"], other, work + "/pg-odd", sock, scope=sc)
    P("  %-42s rc %d ; traceback %s ; cluster created %s ; %s" % (what, rc, "Traceback" in out, os.path.exists(work + "/pg-odd"), out.strip().split("\n")[-1][:110]))
    if os.path.exists(work + "/pg-odd"):
        tool(["stop"], other, work + "/pg-odd", sock, scope=sc); os.rename(work + "/pg-odd", work + "/pg-odd-%d" % len(os.listdir(work)))
os.makedirs(work + "/dir.scope")
rc, out = tool(["rebuild"], other, work + "/pg-odd", sock, scope=work + "/dir.scope"); P("  %-42s rc %d ; %s" % ("the scope path is a directory", rc, out.strip().split("\n")[-1][:110]))
for c in (["stop"],):
    tool(c, root, pgd, sock); tool(c, other, work + "/pg-tue", sock, toolpath=TT)
snap = subprocess.run(["ps", "-axww", "-o", "command="], stdout=subprocess.PIPE).stdout.decode()
P("postgres command lines with -D under my work dir at the end: %d" % sum(1 for l in snap.split("\n") if "postgres" in l.split(" ")[0] and (" -D " + work) in l))
