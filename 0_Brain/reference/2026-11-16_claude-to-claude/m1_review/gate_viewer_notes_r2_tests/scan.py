#!/usr/bin/env python3
"""Byte scan of the files a branch adds or changes (blobs at <rev>), plus optional extra files (controls).
Words and roots come ONLY from the command line (never written into this file).
usage: python3 -B -I scan.py <repo> <base> <rev> <extra files ...> -- <word or root> ...
Each root is searched in its plain, shell-escaped (backslash), URL-encoded and slug spellings; words case-insensitively.
Fixed id classes: UUID, toolu_, msg_0, req_0, a session id of Claude Code shape."""
import re, subprocess, sys, urllib.parse
a = sys.argv[1:]; i = a.index("--"); head, terms = a[:i], a[i + 1:]
repo, base, rev, extra = head[0], head[1], head[2], head[3:]
pats = []
for t in terms:
    sp = {t, t.replace(" ", "\\ ").replace("!", "\\!"), urllib.parse.quote(t), urllib.parse.quote(t, safe=""),
          re.sub(r"[^A-Za-z0-9]", "-", t)}
    for s in sp:
        if s:
            pats.append(("term", re.compile(re.escape(s.encode()), re.I)))
pats += [("uuid", re.compile(rb"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")),
         ("toolu", re.compile(rb"toolu_[A-Za-z0-9]{6,}")), ("msg", re.compile(rb"msg_0[A-Za-z0-9]{6,}")),
         ("req", re.compile(rb"req_0[A-Za-z0-9]{6,}"))]
files = subprocess.run(["git", "-C", repo, "diff", "--name-only", "--diff-filter=AM", f"{base}...{rev}"], capture_output=True, text=True).stdout.split()
blobs = [(f, subprocess.run(["git", "-C", repo, "show", f"{rev}:{f}"], capture_output=True).stdout) for f in files]
blobs += [(f, open(f, "rb").read()) for f in extra]
hits = 0
for f, b in blobs:
    for cls, p in pats:
        for m in p.finditer(b):
            hits += 1
            print(f"HIT {f} class={cls} at byte {m.start()}: {b[max(0, m.start()-20):m.end()+10]!r}"[:200] if cls != "term" else f"HIT {f} class=term#{[q for c,q in pats].index(p)} at byte {m.start()}")
print(f"scanned {len(blobs)} files ({len(files)} from the branch, {len(extra)} controls), {len(pats)} patterns: {hits} hits")
sys.exit(1 if hits else 0)
