# gate 191: READ PR 2003 via the GitHub API (GET only). The token is read from the Secuura env file and never printed.
import json, re, urllib.request
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate191-ks1958-pr2003"
tok = None
for line in open("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env", encoding="utf-8"):
    m = re.match(r"GH_TOKEN=(.*)$", line.rstrip("\n"))
    if m: tok = m.group(1).strip().strip('"')
assert tok
def get(path):
    r = urllib.request.Request("https://api.github.com/repos/Secuura/Distributed_Secuura" + path,
                               headers={"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json"}, method="GET")
    return json.load(urllib.request.urlopen(r, timeout=30))
p = get("/pulls/2003")
open(W + "/logs/pr2003_body.md", "w").write(p["body"] or "")
t = p["title"]
print("title", repr(t), "len", len(t), "starts Refs KS-1958:", t.startswith("Refs KS-1958:"))
print("state", p["state"], "draft", p["draft"], "head", p["head"]["sha"], "base", p["base"]["ref"], "merged", p["merged"], "mergeable", p.get("mergeable"), p.get("mergeable_state"))
print("body chars", len(p["body"] or ""))
c = get("/pulls/2003/commits")
print("commits", [x["sha"][:12] + " " + x["commit"]["message"].splitlines()[0] for x in c])
print("commit msg full:\n" + c[0]["commit"]["message"])
