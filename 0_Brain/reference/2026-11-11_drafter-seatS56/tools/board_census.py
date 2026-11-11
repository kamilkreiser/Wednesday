# Drafter S56, 2026-11-11: READ-ONLY Linear GraphQL census (query text only). Key read inside the process from the project's .env, never printed.
import json, os, sys, urllib.request
URL = "https://api.linear.app/graphql"
envp = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
key = None
for line in open(envp):
    line = line.strip()
    if line.startswith("LINEAR_API_KEY="):
        key = line.split("=", 1)[1].strip().strip('"').strip("'")
if not key:
    print("key missing"); sys.exit(1)
H = {"Authorization": key, "Content-Type": "application/json"}
Q = "query($after:String){issues(first:50, after:$after, filter:{team:{key:{eq:\"KS\"}}}){pageInfo{hasNextPage endCursor} nodes{identifier title priority state{name type} assignee{email} parent{identifier} children{nodes{identifier}} updatedAt createdAt}}}"
out = []; after = None; pages = 0
while True:
    req = urllib.request.Request(URL, data=json.dumps({"query": Q, "variables": {"after": after}}).encode(), headers=H)
    d = json.load(urllib.request.urlopen(req, timeout=120))
    if d.get("errors"): print("ERR", str(d["errors"])[:200]); sys.exit(1)
    b = d["data"]["issues"]; out += b["nodes"]; pages += 1
    if not b["pageInfo"]["hasNextPage"]: break
    after = b["pageInfo"]["endCursor"]
json.dump(out, open(sys.argv[1], "w"))
print("pages", pages, "issues", len(out))
