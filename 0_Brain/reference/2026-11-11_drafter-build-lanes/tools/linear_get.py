# Drafter 2026-11-11: READ-ONLY Linear GraphQL read of issues by key. LINEAR_API_KEY from the environment (envrun); never printed. Query only (no mutation text in this file).
import json, os, sys, urllib.request
URL = "https://api.linear.app/graphql"
H = {"Authorization": os.environ["LINEAR_API_KEY"], "Content-Type": "application/json"}
Q = "query($id:String!){issue(id:$id){identifier title state{name} priority assignee{name} updatedAt description attachments{nodes{url title}} comments(first:50){nodes{id createdAt body}}}}"
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for key in sys.argv[2:]:
    req = urllib.request.Request(URL, data=json.dumps({"query": Q, "variables": {"id": key}}).encode(), headers=H)
    try:
        d = json.load(urllib.request.urlopen(req, timeout=60))
    except Exception as e:
        print(key, "ERR", type(e).__name__); continue
    i = (d.get("data") or {}).get("issue")
    if not i:
        print(key, "NOT READ", str(d.get("errors"))[:120]); continue
    json.dump(i, open(f"{out}/{key}.json", "w"), indent=1)
    c = sorted(i["comments"]["nodes"], key=lambda x: x["createdAt"], reverse=True)
    print(key, i["state"]["name"], "p", i["priority"], "upd", i["updatedAt"][:16], "desc", len(i["description"] or ""), "comments", len(c), "newest", c[0]["id"][:8] if c else "-")
