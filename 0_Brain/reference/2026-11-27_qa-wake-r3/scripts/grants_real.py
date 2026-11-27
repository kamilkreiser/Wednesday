# grants_real.py — build the pack on a SCRATCH COPY of the real inputs; list every dropped row for judging.
# Full row text goes to scratch only (it carries other seats' rows); the output folder gets class, line and counts.
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
root = mk_real("grants_real")
rc, o, e = wp(root, "--today", "2026-11-27")
print("build rc %d | %s | %s" % (rc, o.strip()[-300:], e.strip()[-200:]))
side = open(os.path.join(root, "0_Brain/wake/WAKE-wednesday.dropped.txt"), encoding="utf-8").read()
pack = open(os.path.join(root, "0_Brain/wake/WAKE-wednesday.md"), encoding="utf-8").read()
lines = open(os.path.join(root, "0_Brain/tasks/EXPIRING-GRANTS.md"), encoding="utf-8").read().split("\n")
drops = []
for l in side.split("\n"):
    m = re.match(r"(dead marker|other seat|past date|expired heading) \| line (\d+) \| (.*?) \| (.*)$", l)
    if m:
        drops.append((int(m.group(2)), m.group(1), m.group(3)))
print("dropped rows in the sidecar: %d" % len(drops))
by = {}
for n, c, w in drops:
    by.setdefault(c, []).append(n)
for c in by:
    print("  %s: %d: %s" % (c, len(by[c]), by[c]))
# compare with the lane's stored sidecar
lane_side = open(LANE + "/out/WAKE-wednesday.dropped.txt", encoding="utf-8").read()
lane_lines = sorted(int(x) for x in re.findall(r"\| line (\d+) \|", lane_side))
print("same line set as the lane's stored sidecar: %s (lane %d rows)" % (lane_lines == sorted(n for n, _, _ in drops), len(lane_lines)))
# every row of the register: is it in the pack verbatim, or in the sidecar? (conservation of rows)
rows = 0; inpack = 0; indrop = 0; neither = []
dl = set(n for n, _, _ in drops)
for i, l in enumerate(lines, 1):
    if not l.startswith("|"):
        continue
    cells = l.split("|")[1:-1]; c0 = cells[0].strip() if cells else ""
    if c0.lower() == "grant" or (c0 and set(c0) <= set("-: ")):
        continue
    rows += 1
    a = (l + "\n") in pack; b = i in dl
    inpack += a; indrop += b
    if a == b:
        neither.append((i, a, b))
print("register rows %d; verbatim in the pack %d; in the sidecar %d; in both or neither: %s" % (rows, inpack, indrop, neither))
full = os.path.join(BASE, "grants_real_dropped_fulltext.txt")
with open(full, "w", encoding="utf-8") as f:
    for n, c, w in drops:
        l = lines[n - 1]; cells = l.split("|")[1:-1]
        f.write("=== line %d | %s | %s | %d cells | %d bytes\n" % (n, c, w, len(cells), len(l.encode())))
        for k, cell in enumerate(cells):
            f.write("  C%d: %s\n" % (k + 1, cell.strip()))
        f.write("\n")
print("full text of the dropped rows (scratch only): " + full)
kept = os.path.join(BASE, "grants_real_kept_fulltext.txt")
with open(kept, "w", encoding="utf-8") as f:
    for i, l in enumerate(lines, 1):
        if l.startswith("|") and i not in dl:
            cells = l.split("|")[1:-1]
            f.write("=== line %d | %d cells\n  C1: %s\n  C3: %s\n\n" % (i, len(cells), cells[0].strip()[:400] if cells else "", cells[2].strip()[:300] if len(cells) > 2 else "-"))
print("kept rows (scratch only): " + kept)
