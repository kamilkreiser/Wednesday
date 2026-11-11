# Drafter S56 2026-11-11: READ-ONLY Linear GraphQL read by key (query text only). Key read in-process from the project's .env; never printed.
import json, os, sys, urllib.request
envp = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
key = None
for line in open(envp):
    if line.startswith("LINEAR_API_KEY="): key = line.split("=",1)[1].strip().strip('"').strip("'")
H = {"Authorization": key, "Content-Type": "application/json"}
Q = "query($id:String!){issue(id:$id){identifier title state{name type} priority assignee{email} archivedAt createdAt updatedAt description parent{identifier} children{nodes{identifier}} relations{nodes{type relatedIssue{identifier}}} attachments{nodes{url title}} comments(first:50){nodes{id createdAt body user{email}}}}}"
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for k in sys.argv[2:]:
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://api.linear.app/graphql", data=json.dumps({"query":Q,"variables":{"id":k}}).encode(), headers=H), timeout=60))
    i = (d.get("data") or {}).get("issue")
    if not i: print(k,"NOT READ",str(d.get("errors"))[:100]); continue
    json.dump(i, open(f"{out}/{k}.json","w"), indent=1)
    c = sorted(i["comments"]["nodes"], key=lambda x:x["createdAt"], reverse=True)
    print(k, i["state"]["name"], "p", i["priority"], "archived", i["archivedAt"], "upd", i["updatedAt"][:16], "assignee", i["assignee"] and i["assignee"]["email"], "comments", len(c), "newest", c[0]["id"][:8] if c else "-", "children", len(i["children"]["nodes"]))
