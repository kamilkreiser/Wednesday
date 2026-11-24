"""Cut the owner's screen out of a captured viewer.out: rows 1-4 and chosen entries, the run root masked IN PLACE
(same length, row geometry kept, also where the path is split across rows). usage: screen.py <viewer.out> <root> <seq,...>"""
import re, sys
out = open(sys.argv[1], encoding="utf-8").read().split("\n")[:-1]; root = sys.argv[2]; keep = {int(x) for x in sys.argv[3].split(",")}
mask = "<root>" + "_" * (len(root) - 6)
MARK = "    | "
ents, cur = [], None
for r in out[4:]:
    m = re.match(r"^#(\d+) ", r)
    if m: cur = [int(m.group(1)), [r]]; ents.append(cur)
    elif r.startswith(MARK) and cur: cur[1].append(r)
res = out[:4]
for seq, rows in ents:
    if seq not in keep: continue
    offs = [0 if i == 0 else len(MARK) for i in range(len(rows))]
    flat = [(i, j) for i, r in enumerate(rows) for j in range(offs[i], len(r))]
    text = "".join(rows[i][j] for i, j in flat)
    rr = [list(r) for r in rows]
    for m in re.finditer(re.escape(root), text):
        for k in range(len(root)):
            i, j = flat[m.start() + k]; rr[i][j] = mask[k]
    res += ["".join(x) for x in rr]
print("\n".join(res))
