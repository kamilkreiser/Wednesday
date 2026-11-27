#!/usr/bin/env python3
"""realtree.py <work dir> <socket dir> - the real-tree figures, re-derived. The real brain is only READ (by the tool's
own scan, into MY scratch cluster). Two runs: A = my scratch copy of the allow-listed files; B = the real tree read in
place (BRAINDB_ROOT) so real link counts and symlinks are judged. No lesson file is opened by this script itself: the
(b) figure is re-derived from columns 1 and 3 of the rules index and the folder listing only."""
import os, sys, re, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *

work, sock = sys.argv[1], sys.argv[2]
P = lambda s: print(s, flush=True)
REAL = "/Volumes/DevMASTER/WEDNESDAY"; COPY = S + "/real/WEDNESDAY"; pgd = work + "/pgreal"
EV = REAL + "/2_Project_Files/brain-db/evidence/left_out_lessons_round4b.txt"
P("uptime: " + subprocess.run(["uptime"], stdout=subprocess.PIPE).stdout.decode().strip())
ev = left_out_from_report(open(EV, encoding="utf-8").read())
P("the seat's evidence file names %d left-out lessons: %s" % (len(ev), json.dumps(dict((c, sum(1 for v in ev.values() if v[0] == c)) for c in "abcdtf"))))
sets = {}
for label, root in (("A copy", COPY), ("B real tree in place", REAL)):
    t0 = time.time(); rc, out = tool(["rebuild"], root, pgd, sock); dt = time.time() - t0
    open("%s/rebuild-%s.out" % (work, label[0]), "w").write(out)
    rep = left_out_from_report(out); sets[label] = rep
    lines = out.strip().split("\n")
    P("== %s: rebuild rc %d in %.1f s (wall, includes server start on the first)" % (label, rc, dt))
    for l in lines:
        if re.match(r"\s+(rules|lesson|ledger|daily|skill|identity|people|architecture|rules_index|total)\s+\d", l) or "LESSONS:" in l or "time:" in l or "rules index:" in l or "NOT indexed" in l:
            P("   " + l.strip()[:230])
    P("   LAST LINE: " + lines[-1])
    by = dict((c, sorted(n for n, v in rep.items() if v[0] == c)) for c in "abcdtf")
    P("   names in the report: %d ; by clause %s" % (len(rep), dict((c, len(v)) for c, v in by.items() if v)))
    rc, co = tool(["check"], root, pgd, sock); open("%s/check-%s.out" % (work, label[0]), "w").write(co)
    P("   check rc %d: %s" % (rc, co.split("\n")[0]))
    P("   check: %s" % [l.strip() for l in co.split("\n") if "left out:" in l])
    shown = re.findall(r"^\s{11}(.+?)  \[", co, re.M); more = re.findall(r"\(\+(\d+) more", co)
    P("   check names %d lessons and says '+%s more': %d + %d = %d ; every shown name is in the rebuild's list: %s" % (
        len(shown), "+".join(more), len(shown), sum(map(int, more)), len(shown) + sum(map(int, more)), all(n in rep for n in shown)))
    rc, so = tool(["status"], root, pgd, sock); P("   status rc %d: %s" % (rc, [l.strip() for l in so.split("\n") if "left_out" in l or "counts" in l]))
    rc, do = tool(["doctor"], root, pgd, sock); P("   doctor rc %d: %s" % (rc, do.strip()[-150:]))
    rc, se = tool(["search", "qzzznotawordqzzz"], root, pgd, sock); P("   search (a word in no file) rc %d: %s" % (rc, [l[:110] for l in se.split("\n") if "NOTE" in l]))
    P("   the report's names equal the seat's evidence file's names: %s (only in mine: %s ; only in theirs: %s)" % (
        set(rep) == set(ev), sorted(set(rep) - set(ev)), sorted(set(ev) - set(rep))))
    P("   same clause for every name: %s" % all(rep[n][0] == ev[n][0] for n in rep if n in ev))
    if label.startswith("B"):
        for c in "abcdtf":
            for n in by[c]:
                P("      (%s) %s  [%s]" % (c, n, rep[n][1][:95]))
P("A and B name the same lessons: %s" % (set(sets["A copy"]) == set(sets["B real tree in place"])))
# independent re-derivation of (a) and (b): rules index columns 1 and 3 + the folder listing
idx = open(REAL + "/0_Brain/learnings/_rules_index.tsv", encoding="utf-8").read().split("\n")
rows = [l.split("\t") for l in idx[1:] if l.strip()]
P("rules index: %d non-blank lines below the header; field counts %s" % (len(rows), sorted(set(len(r) for r in rows))))
plain = dict((r[0], r[2]) for r in rows if "#" not in r[0]); hashed = [r[0] for r in rows if "#" in r[0]]
files = sorted(n for n in os.listdir(REAL + "/0_Brain/learnings") if re.fullmatch(r"\d{4}-\d{2}-\d{2}[_-].+\.md", n))
skip = [n for n in files if "(conflict_on_" in n or ".pre-" in n]
files = [n for n in files if n not in skip]
norow = [n for n in files if n not in plain]
other = [n for n in files if n in plain and plain[n] != "all" and "wednesday" not in plain[n].split(",")]
P("my own count: %d lesson files (plus %d sync or backup copies left out by path: %s); %d plain rows, %d '#n' rows; seats cells in use: %s" % (
    len(files), len(skip), skip, len(plain), len(hashed), json.dumps(dict((s, list(plain.values()).count(s)) for s in sorted(set(plain.values()))))))
P("my own count: lesson files with no plain row: %d %s ; plain rows naming no file: %d ; lesson files whose row does not name wednesday or all: %d" % (
    len(norow), norow, len([k for k in plain if k not in files]), len(other)))
B = sets["B real tree in place"]
P("my own (b) list equals the tool's (b) list: %s ; tool's (a) list: %s" % (sorted(other) == sorted(n for n, v in B.items() if v[0] == "b"), sorted(n for n, v in B.items() if v[0] == "a")))
# how often this seat's own ledgers cite the left-out c and d lessons (counts only)
led = ""
for n in ("_ledger.md", "_ledger_archive.md"):
    led += open(REAL + "/0_Brain/learnings/" + n, encoding="utf-8", errors="replace").read()
allc = sorted(((led.count(n[:-3]), n) for n in files), reverse=True)
rank = dict((n, i + 1) for i, (c, n) in enumerate(allc))
P("citations in the Wednesday seat's own two ledgers (file-stem count; rank among %d lessons):" % len(files))
for n, v in sorted(B.items()):
    if v[0] in ("c", "d"):
        P("   (%s) %-75s cited %3d times, rank %3d   [%s]" % (v[0], n, led.count(n[:-3]), rank[n], v[1][:60]))
rc, so = tool(["stop"], REAL, pgd, sock); P("stop rc %d: %s" % (rc, so.strip().split("\n")[-1][-60:]))
rc, so = tool(["status"], REAL, pgd, sock); P("status rc %d: %s" % (rc, [l for l in so.split("\n") if l.startswith("server")]))
