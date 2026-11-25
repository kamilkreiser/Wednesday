"""My own byte search over a leak_r2 run ROOT for its markers and per-start value(s) (from its out dir); with
--plant, a control file holding the start value is written into the root first (must give exactly 1 hit).
usage: python3 -B -I leak_own.py <root> <out dir> [--plant]"""
import json, os, re, sys
root, od = sys.argv[1], sys.argv[2]
mk = json.load(open(os.path.join(od, "markers.json")))
log = open(os.path.join(od, "..", os.path.basename(od) + ".log")).read()
start = re.findall(r"start=\['([0-9a-f]+)'", log)
pats = [m.encode() for m in (mk if isinstance(mk, list) else list(mk))] + [s.encode() for s in start]
if "--plant" in sys.argv:
    open(os.path.join(root, "planted_control.txt"), "w").write("x" + start[0] + "y")
files = hits = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        p = os.path.join(dp, f)
        if os.path.islink(p) or not os.path.isfile(p): continue
        try: b = open(p, "rb").read()
        except OSError: continue
        files += 1
        for x in pats:
            if x in b: hits += 1; print("HIT", p, x[:20])
print(f"patterns {len(pats)} (markers {len(pats) - len(start)} + start {len(start)}), files {files}, hits {hits}")
