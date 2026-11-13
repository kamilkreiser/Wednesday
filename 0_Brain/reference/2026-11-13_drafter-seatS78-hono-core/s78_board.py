import json, urllib.request, re
ENV="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
E={}
for l in open(ENV):
    l=l.strip()
    if "=" in l and not l.startswith("#"):
        k,v=l.split("=",1); E[k.strip()]=v.strip().strip('"').strip("'")
def gql(q,v=None):
    r=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps({"query":q,"variables":v or {}}).encode(),method="POST")
    r.add_header("Authorization",E["LINEAR_API_KEY"]); r.add_header("Content-Type","application/json"); r.add_header("User-Agent","wednesday-drafter/1.0")
    j=json.loads(urllib.request.urlopen(r,timeout=60).read().decode())
    if "errors" in j: raise SystemExit(json.dumps(j["errors"])[:300])
    return j["data"]
print("viewer:", gql("{viewer{name email}}")["viewer"]["email"])
terms=["GHSA-4m76-xfj5-7975","GHSA-h7mg-cq63-vhpq","GHSA-3gg2-335m-rxc6","GHSA-46wx-v44x-9hh2","GHSA-4h7h-rv7c-7m2v","4m76","h7mg","3gg2","46wx","4h7h","hono 4.13","hono","node-server","KS-2194"]
q='query($t:String!){searchIssues(term:$t,first:15,includeArchived:true){nodes{identifier title state{name} priority}}}'
for t in terms:
    n=gql(q,{"t":t})["searchIssues"]["nodes"]
    print(f"\n## search {t!r}: {len(n)} hits")
    for i in n: print("  ",i["identifier"],"|",i["state"]["name"],"|",i["title"][:110])
# full-text scan of recently updated issues
after=None; allv=[]
while True:
    d=gql('query($a:String){issues(first:100,after:$a,includeArchived:true,filter:{updatedAt:{gte:"2026-11-10T00:00:00Z"}}){nodes{identifier title description state{name}} pageInfo{hasNextPage endCursor}}}',{"a":after})["issues"]
    allv+=d["nodes"]
    if not d["pageInfo"]["hasNextPage"]: break
    after=d["pageInfo"]["endCursor"]
print("\n## scan: issues updated since 2026-11-10:",len(allv))
pat=re.compile(r"4m76|h7mg|3gg2|46wx|4h7h|hono|4\.13\.1[3-8]",re.I)
for i in allv:
    txt=(i["title"] or "")+" "+(i["description"] or "")
    m=sorted(set(x.lower() for x in pat.findall(txt)))
    if m: print("  ",i["identifier"],"|",i["state"]["name"],"|",i["title"][:100],"|",m)
print("control KS-2164 in scan:",any(i["identifier"]=="KS-2164" for i in allv),"| control KS-2194 in scan:",any(i["identifier"]=="KS-2194" for i in allv))
