# QA-POLICY-B: list the rows behind the docs-tier completeness misses (row id, tool, state count). usage: python3 -B -I docs_tier_rows.py <base> <head>
import json, sys, collections
B, H = sys.argv[1:3]
fb, fh = open(B), open(H); fb.readline(); fh.readline()
rows = collections.OrderedDict()
for lb, lh in zip(fb, fh):
    rb, rh = json.loads(lb), json.loads(lh)
    work = sum(16 + c + ch // 8 for c, ch in rh["b_stats"]); n = len(rh["b_stats"])
    if n > 1024 or work > 8000 or rh["oversize"] is not None: continue
    for sb, sh in zip(rb["states"], rh["states"]):
        t = sb.get("twin")
        if t and len(t) > 3 and t[3] == "X" and sh["cols"][0]["d"]["k"] in ("A", "Q", "W"):
            rows.setdefault(rb["id"], [rb["tool"], [w["k"] for w in rb["wins"]], 0, [n["name"] for n in rb.get("names", [])]])[2] += 1
print("rows", len(rows))
c = collections.Counter((":".join(k.split(":")[:1]), v[0], tuple(v[1])) for k, v in rows.items())
for k, v in c.most_common(): print("  ", k, v)
for k, v in list(rows.items())[:40]: print(k, v)
