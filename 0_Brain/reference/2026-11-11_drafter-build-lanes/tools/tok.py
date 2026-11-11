import json, re, sys, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
E = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_drafter-build-lanes/evidence/"
prs = json.load(open(E + "open_prs.json")); ready = json.load(open(E + "ready_paths.json"))
univ = {}
for x in prs:
    for f in x["files"]: univ.setdefault(f, set()).add("PR%d" % x["number"])
for k, v in ready.items(): univ.setdefault(k, set()).add("READY")
rx = re.compile(r'[A-Za-z0-9_.@-]+(?:/[A-Za-z0-9_.@{}*-]+)+\.(?:ts|tsx|js|cjs|mjs|sh|json|md|mdc|yaml|yml|sql|py|html|txt|conf)')
for k in sys.argv[1:]:
    i = json.load(open(E + f"tickets/{k}.json"))
    text = (i["description"] or "") + " ".join(c["body"] for c in i["comments"]["nodes"])
    toks = sorted(set(rx.findall(text)))
    hit = {}
    for t in toks:
        t2 = t.lstrip("./")
        for u, s in univ.items():
            if u == t2 or u.endswith("/" + t2): hit.setdefault(t2, set()).update(s)
    print(k, "tokens", len(toks), "excluded-token", len(hit))
    for t, s in hit.items(): print("    X", t, sorted(s)[:3])
