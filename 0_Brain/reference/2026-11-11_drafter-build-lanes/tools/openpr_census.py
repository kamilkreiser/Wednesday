# Drafter (Wednesday, 2026-11-11): READ-ONLY census of every OPEN PR on Secuura/Distributed_Secuura with its files, all pages.
# GH_TOKEN comes from the environment (set by envrun); never printed. No write verb.
import json, os, sys, urllib.request
H = {"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json", "User-Agent": "wed-drafter-readonly"}
BASE = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(BASE + p, headers=H), timeout=60))
prs, page = [], 1
while True:
    b = get(f"/pulls?state=open&per_page=100&page={page}"); prs += b
    if len(b) < 100: break
    page += 1
t = []
for p in prs:
    files, fp = [], 1
    while True:
        b = get(f"/pulls/{p['number']}/files?per_page=100&page={fp}"); files += [f["filename"] for f in b]
        if len(b) < 100: break
        fp += 1
    t.append({"number": p["number"], "head": p["head"]["sha"], "title": p["title"], "files": files, "changed_files": p.get("changed_files")})
json.dump(t, open(sys.argv[1], "w"), indent=1)
print("open PRs:", len(t), "files rows:", sum(len(x["files"]) for x in t))
