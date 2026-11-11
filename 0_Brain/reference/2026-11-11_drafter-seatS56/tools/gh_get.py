# Drafter S56 2026-11-11: READ-ONLY GitHub REST GET. Token read in-process from the project's .env; never printed.
# usage: gh_get.py pr N...   |   gh_get.py lines SHA PATH A B   |   gh_get.py cmp BASE HEAD
import base64, json, sys, urllib.parse, urllib.request
envp = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
tok = None
for line in open(envp):
    if line.startswith("GH_TOKEN="): tok = line.split("=",1)[1].strip().strip('"').strip("'")
H = {"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json", "User-Agent": "wed-drafter-readonly"}
B = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
m = sys.argv[1]
if m == "pr":
    for n in sys.argv[2:]:
        p = get(f"{B}/pulls/{n}")
        print(n, p["state"], "merged" if p["merged"] else "unmerged", "head", p["head"]["sha"][:12], "merge", (p.get("merge_commit_sha") or "-")[:12], "merged_at", p.get("merged_at"), "|", p["title"][:70])
elif m == "lines":
    sha, path, a, b = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    d = get(f"{B}/contents/{urllib.parse.quote(path)}?ref={sha}")
    t = base64.b64decode(d["content"]).decode(errors="replace").split("\n")
    print("lines in file", len(t))
    for i in range(a-1, min(b, len(t))): print(i+1, t[i][:200])
elif m == "cmp":
    c = get(f"{B}/compare/{sys.argv[2]}...{sys.argv[3]}")
    print(sys.argv[2][:12], "...", sys.argv[3][:12], "status", c["status"], "ahead", c["ahead_by"], "behind", c["behind_by"])
