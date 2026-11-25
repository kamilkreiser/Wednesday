#!/usr/bin/env python3
# QA-AUDIT-HOST-FIX byte scan. Usage: bytescan.py <file|-diff:...> ... -- <word> ...
# Words come ONLY from the command line. Each word is searched case-insensitively as bytes, in
# plain, backslash-escaped-space, URL-encoded and slug (space->-, space->_) spellings.
import sys, urllib.parse
args = sys.argv[1:]
i = args.index("--")
files, words = args[:i], args[i + 1:]
spell = set()
for w in words:
    for v in {w, w.replace(" ", "\\ "), urllib.parse.quote(w), w.replace(" ", "-"), w.replace(" ", "_"), w.replace(" ", "%20")}:
        spell.add(v.lower().encode())
hits = 0
for f in files:
    data = open(f, "rb").read().lower()
    for s in sorted(spell):
        k = data.count(s)
        if k:
            hits += k
            print(f"HIT {f}: {s!r} x{k}")
print(f"scanned {len(files)} files for {len(spell)} spellings of {len(words)} words: {hits} hits")
sys.exit(1 if hits else 0)
