# gate 194: READ PR 2005 via the GitHub API (GET only). The token is read from the Secuura env file and never printed.
import json, re, hashlib, urllib.request
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959"
tok = None
for line in open("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env", encoding="utf-8"):
    m = re.match(r"GH_TOKEN=(.*)$", line.rstrip("\n"))
    if m: tok = m.group(1).strip().strip('"')
assert tok
def get(path):
    r = urllib.request.Request("https://api.github.com/repos/Secuura/Distributed_Secuura" + path,
                               headers={"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json"}, method="GET")
    return json.load(urllib.request.urlopen(r, timeout=30))
p = get("/pulls/2005")
body = p["body"] or ""
open(W + "/logs/pr2005_body.md", "w").write(body)
t = p["title"]
print("title", repr(t), "len", len(t), "starts 'Refs KS-1959:'", t.startswith("Refs KS-1959:"))
print("state", p["state"], "draft", p["draft"], "head", p["head"]["sha"], "base", p["base"]["ref"], "merged", p["merged"],
      "mergeable", p.get("mergeable"), p.get("mergeable_state"), "commits", p.get("commits"), "changed_files", p.get("changed_files"),
      "+", p.get("additions"), "-", p.get("deletions"))
print("body chars", len(body), "body sha1", hashlib.sha1(body.encode()).hexdigest())
seat = open("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-05_seatK-14th/pr/body.md").read()
print("seat read-back body.md equal to API body:", seat == body, "(rstrip-equal:", seat.rstrip() == body.rstrip(), ")")
c = get("/pulls/2005/commits")
msg = c[0]["commit"]["message"]
print("commits", [x["sha"][:12] + " " + x["commit"]["message"].splitlines()[0] for x in c])
open(W + "/logs/pr2005_commit_msg.txt", "w").write(msg)
CW = re.compile(r"(close[sd]?|fix(e[sd])?|resolve[sd]?)[: ]+(#|KS-|https://linear)", re.I)
print("close-word hits: body", len(CW.findall(body)), "title+commit", len(CW.findall(t + "\n" + msg)))
ctrl = "Closes KS-1959 and also fixes https://linear.app/secuura/issue/KS-1959"
print("close-word control string hits", len(CW.findall(ctrl)), "(expect 2)")
