import subprocess, json, os
D="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-15_drafter-seatB176"
env=dict(os.environ); env["GH_CONFIG_DIR"]="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
Q="""query($after:String){repository(owner:"Secuura",name:"Distributed_Secuura"){pullRequests(states:OPEN,first:50,after:$after,orderBy:{field:CREATED_AT,direction:ASC}){pageInfo{hasNextPage endCursor} nodes{number title updatedAt headRefOid isDraft files(first:100){totalCount nodes{path}}}}}}"""
after=None; prs=[]
while True:
    a=["gh","api","graphql","-f","query="+Q]
    if after: a+=["-f","after="+after]
    r=subprocess.run(a,capture_output=True,text=True,env=env)
    if r.returncode: print("rc",r.returncode,r.stderr[:300]); break
    j=json.loads(r.stdout)["data"]["repository"]["pullRequests"]
    prs+=j["nodes"]
    if not j["pageInfo"]["hasNextPage"]: break
    after=j["pageInfo"]["endCursor"]
print("open PRs",len(prs))
json.dump(prs,open(D+"/census.json","w"))
rows=[2098,2089,2079,2220,2221,2222,2223,2224]
by={p["number"]:p for p in prs}
print("rows present+open:",[n for n in rows if n in by],"missing:",[n for n in rows if n not in by])
qpaths={n:set(f["path"] for f in by[n]["files"]["nodes"]) for n in rows if n in by}
allq=set().union(*qpaths.values())
trunc=[p["number"] for p in prs if p["files"]["totalCount"]>100]
print("PRs with >100 files (truncated read):",trunc)
for p in prs:
    if p["number"] in rows: continue
    ps=set(f["path"] for f in p["files"]["nodes"])
    hit=ps&allq
    if hit:
        who=[n for n in rows if qpaths[n]&ps]
        print("SHARES",p["number"],p["headRefOid"][:12],p["updatedAt"],"with rows",who,sorted(hit)[:4])
anch=[p["number"] for p in prs if any("services/anchoring" in f["path"] for f in p["files"]["nodes"])]
print("open PRs touching services/anchoring:",anch)
print("positive control (2224 vs own paths):",len(qpaths[2224]&qpaths[2224]))
print("PRs updated since 2026-11-13T03:30Z:",[(p["number"],p["updatedAt"]) for p in prs if p["updatedAt"]>"2026-11-13T03:30:00Z"][:30])
locks=[p["number"] for p in prs if any(f["path"].endswith("package-lock.json") for f in p["files"]["nodes"])]
print("open PRs touching a package-lock:",locks)
