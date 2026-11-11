# S58 drafter 2026-11-12: READ-ONLY Linear GraphQL census (team KS, includeArchived default false). key in-process, never printed.
import json, sys, urllib.request
envp = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
key = None
for line in open(envp):
    if line.startswith("LINEAR_API_KEY="): key = line.split("=",1)[1].strip().strip('"').strip("'")
H = {"Authorization": key, "Content-Type": "application/json"}
Q = 'query($after:String){issues(first:25, after:$after, filter:{team:{key:{eq:"KS"}}}){pageInfo{hasNextPage endCursor} nodes{identifier title priority updatedAt createdAt archivedAt state{name type} assignee{email} parent{identifier} project{name id} comments(first:50){nodes{id createdAt}}}}}'
out=[]; after=None; pages=0
while True:
    req = urllib.request.Request("https://api.linear.app/graphql", data=json.dumps({"query":Q,"variables":{"after":after}}).encode(), headers=H)
    d = json.load(urllib.request.urlopen(req, timeout=180))
    if d.get("errors"): print("ERR", str(d["errors"])[:300]); sys.exit(1)
    b=d["data"]["issues"]; out+=b["nodes"]; pages+=1
    if not b["pageInfo"]["hasNextPage"]: break
    after=b["pageInfo"]["endCursor"]
json.dump(out, open(sys.argv[1],"w"))
print("pages",pages,"issues",len(out))
