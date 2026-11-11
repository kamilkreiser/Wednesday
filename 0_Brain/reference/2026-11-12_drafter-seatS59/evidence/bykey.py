# S58 drafter: READ-ONLY Linear by-key (includeArchived) for keys absent from the default census. key in-process, never printed.
import json, sys, urllib.request
envp = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
key = None
for line in open(envp):
    if line.startswith("LINEAR_API_KEY="): key = line.split("=",1)[1].strip().strip('"').strip("'")
H = {"Authorization": key, "Content-Type": "application/json"}
Q = 'query($n:Float){issues(includeArchived:true, first:2, filter:{team:{key:{eq:"KS"}}, number:{eq:$n}}){nodes{identifier title priority updatedAt archivedAt state{name type} assignee{email} comments(first:50){nodes{id}}}}}'
out={}
for k in sys.argv[2:]:
    n=int(k.split('-')[1])
    req = urllib.request.Request("https://api.linear.app/graphql", data=json.dumps({"query":Q,"variables":{"n":n}}).encode(), headers=H)
    d = json.load(urllib.request.urlopen(req, timeout=60))
    if d.get("errors"): print("ERR",k,str(d["errors"])[:200]); continue
    nodes=d["data"]["issues"]["nodes"]; out[k]=nodes[0] if nodes else None
json.dump(out, open(sys.argv[1],"w")); print(len(out),"read")
