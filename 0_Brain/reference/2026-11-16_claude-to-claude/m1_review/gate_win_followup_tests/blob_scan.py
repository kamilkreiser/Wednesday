#!/usr/bin/env python3
"""Every blob of `git ls-tree -r <rev>`: count those holding a CR byte, and those with a NUL in the first
8,000 bytes. Usage: blob_scan.py <repo> <rev> [--control]  (--control adds two planted in-memory blobs)."""
import subprocess, sys
repo, rev = sys.argv[1], sys.argv[2]
ls = subprocess.run(["git", "-C", repo, "ls-tree", "-r", rev], capture_output=True, check=True).stdout.decode().splitlines()
modes = {}
cr, nul, empty, n = [], [], 0, 0
for line in ls:
    meta, path = line.split("\t", 1)
    mode, typ, oid = meta.split()
    modes[mode] = modes.get(mode, 0) + 1
    if typ != "blob":
        continue
    data = subprocess.run(["git", "-C", repo, "cat-file", "blob", oid], capture_output=True, check=True).stdout
    n += 1
    if not data:
        empty += 1
    if b"\r" in data:
        cr.append(path)
    if b"\0" in data[:8000]:
        nul.append(path)
if "--control" in sys.argv:
    for name, data in (("planted_crlf", b"a\r\nb\r\n"), ("planted_nul", b"x\0y")):
        n += 1
        if b"\r" in data: cr.append(name)
        if b"\0" in data[:8000]: nul.append(name)
print(f"{rev}: {n} blobs (modes {modes}); empty {empty}; with CR {len(cr)} {cr[:5]}; NUL in first 8000 {len(nul)} {nul[:5]}")
exts = {}
for line in ls:
    p = line.split("\t", 1)[1]
    e = p.rsplit(".", 1)[-1].lower() if "." in p.rsplit("/", 1)[-1] else "(none)"
    exts[e] = exts.get(e, 0) + 1
print("extensions:", sorted(exts.items(), key=lambda x: -x[1]))
