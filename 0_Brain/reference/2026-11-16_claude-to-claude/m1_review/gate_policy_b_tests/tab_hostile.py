# QA-POLICY-B item 4/6 tables from the differential outputs (rows I4/I6/I2 carry full Debug of `decide`).
# usage: python3 -B -I tab_hostile.py <base.jsonl> <head.jsonl> <prefix> [states,comma]
import json, sys
B, H, PFX = sys.argv[1:4]
STS = sys.argv[4].split(",") if len(sys.argv) > 4 else ["**/.env*", "**/.env", "<ws>/secret/**"]
COLS4 = [0, 8, 9, 3]   # decide/no view, owner StillAsk, owner Allowed, both-agree live_shell (column order of the harness)
def rows(p):
    f = open(p); f.readline()
    for l in f:
        r = json.loads(l)
        if r["id"].startswith(PFX): yield r
out = []
for rb, rh in zip(rows(B), rows(H)):
    assert rb["id"] == rh["id"]
    sb = {s["st"]: s for s in rb["states"]}; sh = {s["st"]: s for s in rh["states"]}
    name = (rb.get("names") or [{"name": "?"}])[0]["name"]
    nothing = sb["nothing"]["cols"][0]
    on_card = None
    if "full" in nothing:
        on_card = (name in nothing["full"]) if nothing["c"].startswith("a") else "n/a (" + nothing["c"] + ")"
    for st in STS:
        cb = " ".join(sb[st]["cols"][i]["c"] for i in COLS4)
        ch = " ".join(sh[st]["cols"][i]["c"] for i in COLS4)
        nm = rh.get("names") or [{}]
        out.append((rb["id"], st, cb, ch, on_card, nm[0].get("in_pieces"), nm[0].get("word_ends", [])[:2], rh["oversize"]))
for o in out:
    print("\t".join(str(x) for x in o))
