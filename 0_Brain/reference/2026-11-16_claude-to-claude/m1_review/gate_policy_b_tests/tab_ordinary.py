# QA-POLICY-B item 3: the ordinary-corpus table from the differential outputs (rows `ord:`, `t29corp`, `fam:`, `ctl:`).
# usage: python3 -B -I tab_ordinary.py <base.jsonl> <head.jsonl>
# Columns: id, tool, field characters, B pieces, B work (the check's own arithmetic over the head's B pieces),
# ratio to the 8 000-unit guard, base four columns (state default), head four columns, refused/admitted.
import json, sys
B, H = sys.argv[1:3]
COLS4 = [0, 8, 9, 3]
def rows(p):
    f = open(p); f.readline()
    for l in f:
        r = json.loads(l)
        if r["id"].split(":")[0] in ("ord", "t29corp", "t29corp+name900", "fam", "ctl", "ord+"):
            yield r
res = []
for rb, rh in zip(rows(B), rows(H)):
    assert rb["id"] == rh["id"]
    st = {s["st"]: s for s in rh["states"]}; sb = {s["st"]: s for s in rb["states"]}
    work = sum(16 + c + ch // 8 for c, ch in rh["b_stats"]); n = len(rh["b_stats"])
    fl = rh["wins"][-1]["flen"] if rh["wins"] else 0
    hb = " ".join(st["default"]["cols"][i]["c"] for i in COLS4)
    bb = " ".join(sb["default"]["cols"][i]["c"] for i in COLS4)
    hx = " ".join(st["**/.env*"]["cols"][i]["c"] for i in COLS4)
    res.append((rh["id"], n, work, work / 8000, bb, hb, hx, "REFUSED" if rh["oversize"] else "admitted", rh["oversize"] or ""))
for r in res:
    print(f"{r[0]}\tB pieces {r[1]}\tB work {r[2]}\tratio {r[3]:.3f}\tbase(def) {r[4]}\thead(def) {r[5]}\thead(**/.env*) {r[6]}\t{r[7]}\t{r[8]}")
