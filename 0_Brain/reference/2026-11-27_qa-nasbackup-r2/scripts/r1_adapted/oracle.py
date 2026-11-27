#!/usr/bin/env python3
# oracle.py — "was any content on the destination lost?"  snap: record sha256 of every regular file under a root
# (excluding run markers, manifests, README). lost: every (sha256) recorded must still exist somewhere under the root.
import hashlib, json, os, sys
def scan(root):
    res = {}
    for d, dirs, files in os.walk(root):
        for f in files:
            p = os.path.join(d, f)
            if os.path.islink(p):
                continue
            rel = os.path.relpath(p, root)
            if "/manifests/" in rel or "/runs/" in rel or rel.endswith("README.txt"):
                continue
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            res.setdefault(h, []).append(rel)
    return res
cmd, root, snapf = sys.argv[1:4]
if cmd == "snap":
    s = scan(root); json.dump(s, open(snapf, "w"), indent=1); print("snap: %d distinct contents, %d files" % (len(s), sum(len(v) for v in s.values())))
else:
    before = json.load(open(snapf)); after = scan(root); n = 0
    for h, rels in sorted(before.items(), key=lambda kv: kv[1]):
        if h not in after:
            n += 1; print("LOST content %s formerly at %s" % (h[:12], rels))
    print("oracle: %d of %d contents lost" % (n, len(before)))
    sys.exit(1 if n else 0)
