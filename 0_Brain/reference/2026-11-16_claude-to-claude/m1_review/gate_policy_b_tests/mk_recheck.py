# QA-POLICY-B: rows whose excluded-name cells the main comparison could not attribute, rebuilt from the outputs (a
# web fetch URL window that is the whole URL), for one re-run of the base twin under the corrected URL-escape rule.
import json, sys
out = open(sys.argv[1], "w"); n = 0; skipped = []
for seed in sys.argv[2:]:
    fb = open(f"/private/tmp/claude-501/qpb/out/main_{seed}_base.jsonl"); fh = open(f"/private/tmp/claude-501/qpb/out/main_{seed}_head.jsonl"); fb.readline(); fh.readline()
    for lb, lh in zip(fb, fh):
        if '"X"' not in lh: continue
        rb = json.loads(lb); rh = json.loads(lh); bad = False
        for sb, sh in zip(rb["states"], rh["states"]):
            for cb, ch in zip(sb["cols"], sh["cols"]):
                t = sb.get("twin")
                if ch["c"] == "X" and cb["c"] != "X" and t and t[1] != "X" and t[3] != "X": bad = True
        if not bad: continue
        w = rh["wins"]
        if rh["tool"] == "WebFetch" and w and w[0]["k"] == "url" and w[0]["wlen"] == w[0]["flen"] and rh["id"].endswith("WebFetchURL"):
            out.write(json.dumps({"id": f"recheck:{seed}:{rh['id']}", "grp": "RC", "tool": "WebFetchURL", "text": rh["windows"][0][1]}, ensure_ascii=False) + "\n"); n += 1
        else: skipped.append(rh["id"])
print("recheck rows", n, "not rebuildable", skipped)
