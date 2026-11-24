#!/usr/bin/env python3
"""QA-DAEMON-NOTES item 10: byte scan for names, paths and ids. The words are given ONLY on the command
line (never written to a file). Usage:
  python3 -I -B qa_scan.py --words 'w1|w2|...' --whole 'short1|short2' FILE...
Each word is searched as bytes, case-insensitively, in these spellings: plain; every space and '/'
backslash-escaped; URL-encoded (%20, %2F); slug (spaces -> '-' and '_', lowercase). --whole words match
only as whole words (letters on neither side). Plus patterns for tool-use/message/request ids and UUIDs.
Prints one line per hit (file, offset, which word or pattern - the word itself is printed as '#<n>')."""
import re, sys, urllib.parse

args = sys.argv[1:]
words, whole, files = [], [], []
i = 0
while i < len(args):
    if args[i] == "--words":
        words = [w for w in args[i + 1].split("|") if w]
        i += 2
    elif args[i] == "--whole":
        whole = [w for w in args[i + 1].split("|") if w]
        i += 2
    else:
        files.append(args[i])
        i += 1


def spellings(w):
    s = {w, w.replace(" ", "\\ ").replace("/", "\\/"), urllib.parse.quote(w, safe=""),
         urllib.parse.quote(w), w.replace(" ", "-"), w.replace(" ", "_"), w.replace(" ", "")}
    return {x.lower().encode() for x in s if x}


pats = []
for n, w in enumerate(words):
    for sp in spellings(w):
        pats.append((f"#{n}", re.compile(re.escape(sp), re.I)))
for n, w in enumerate(whole):
    for sp in spellings(w):
        pats.append((f"whole#{n}", re.compile(rb"(?<![A-Za-z])" + re.escape(sp) + rb"(?![A-Za-z])", re.I)))
pats += [("toolu_id", re.compile(rb"toolu_[A-Za-z0-9]{8,}")), ("msg_id", re.compile(rb"msg_[A-Za-z0-9]{12,}")),
         ("req_id", re.compile(rb"req_[A-Za-z0-9]{12,}")),
         ("uuid", re.compile(rb"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I))]
hits = 0
for f in files:
    b = open(f, "rb").read()
    for name, p in pats:
        for m in p.finditer(b):
            hits += 1
            print(f"HIT {f} @{m.start()} {name}")
print(f"scanned {len(files)} file(s), {len(words)}+{len(whole)} word(s), {len(pats)} pattern(s): {hits} hit(s)")
