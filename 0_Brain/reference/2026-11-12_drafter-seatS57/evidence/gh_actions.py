# S57 drafter 2026-11-12: READ-ONLY GitHub REST GET (actions runs, workflows dir at a sha). Token read in-process; never printed.
import json, sys, urllib.request
envp = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
tok=None
for line in open(envp):
    if line.startswith("GH_TOKEN="): tok=line.split("=",1)[1].strip().strip('"').strip("'")
H={"Authorization":"Bearer "+tok,"Accept":"application/vnd.github+json","User-Agent":"wed-drafter-readonly"}
B="https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=60))
m=sys.argv[1]
if m=="runs":
    d=get(B+"/actions/runs?per_page=5")
    print("total_count",d["total_count"])
    for r in d["workflow_runs"]: print(r["id"],r["name"][:40],r["event"],r["status"],r["conclusion"],r["created_at"],r["head_sha"][:12])
elif m=="wf":
    d=get(B+"/contents/.github/workflows?ref="+sys.argv[2]); print(len(d),"entries"); print(" ".join(x["name"] for x in d))
elif m=="checks":
    d=get(B+"/commits/"+sys.argv[2]+"/check-runs?per_page=100"); print("total",d["total_count"]); 
    for r in d["check_runs"][:12]: print(r["name"][:50],r["status"],r["conclusion"])
