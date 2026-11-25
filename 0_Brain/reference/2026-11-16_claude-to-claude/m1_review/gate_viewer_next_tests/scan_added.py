#!/usr/bin/env python3
"""QA-VIEWER-NEXT item 10: byte scan of the lane's ADDED lines (`git diff -U0 base...rev`, '+' lines) and, per file,
hit counts of the head's blob against the base's blob (equal counts: nothing added). Plus control files.
Words come ONLY from the command line. usage: python3 -B -I scan_added.py <repo> <base> <rev> <control files ...> -- <words ...>"""
import re, subprocess, sys, urllib.parse
a = sys.argv[1:]; i = a.index("--"); head, terms = a[:i], a[i + 1:]
repo, base, rev, extra = head[0], head[1], head[2], head[3:]
pats = []
for t in terms:
    for s in {t, t.replace(" ", "\\ ").replace("!", "\\!"), urllib.parse.quote(t), urllib.parse.quote(t, safe=""), re.sub(r"[^A-Za-z0-9]", "-", t)}:
        if s: pats.append(("term", re.compile(re.escape(s.encode()), re.I)))
pats += [("uuid", re.compile(rb"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")),
         ("toolu", re.compile(rb"toolu_[A-Za-z0-9]{6,}")), ("msg", re.compile(rb"msg_0[A-Za-z0-9]{6,}")), ("req", re.compile(rb"req_0[A-Za-z0-9]{6,}"))]
def g(*x): return subprocess.run(["git", "-C", repo, *x], capture_output=True).stdout
def count(b):
    out = {}
    for k, (cls, p) in enumerate(pats):
        n = len(p.findall(b))
        if n: out[k] = n
    return out
added = b"\n".join(l[1:] for l in g("diff", "-U0", f"{base}...{rev}").split(b"\n") if l.startswith(b"+") and not l.startswith(b"+++"))
print(f"patterns {len(pats)} ({len(terms)} words x spellings + 4 id classes)")
c = count(added); print(f"added lines ({added.count(b'\n') + 1}): hits {sum(c.values())} {c}")
for f in g("diff", "--name-only", f"{base}...{rev}").decode().split():
    hb, bb = count(g("show", f"{rev}:{f}")), count(g("show", f"{base}:{f}"))
    print(f"  {f}: head blob {sum(hb.values())}, base blob {sum(bb.values())}, by pattern equal: {hb == bb}")
for f in extra:
    c = count(open(f, "rb").read()); print(f"control {f.rsplit('/', 1)[-1]}: hits {sum(c.values())}")
