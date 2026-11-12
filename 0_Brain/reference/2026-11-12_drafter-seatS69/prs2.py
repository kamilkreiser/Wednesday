import json,re,sys,urllib.request
TOK=None
for l in open("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env",encoding="utf-8",errors="replace"):
    m=re.match(r"\s*(?:export\s+)?GH_TOKEN=(.*)$",l.rstrip("\n"))
    if m: TOK=m.group(1).strip().strip("\"'")
ns=[int(x) for x in sys.argv[1:]]
q="query { repository(owner:\"Secuura\", name:\"Distributed_Secuura\") { %s } }"%" ".join("p%d: pullRequest(number:%d){number state merged mergedAt mergeCommit{oid} headRefOid title}"%(n,n) for n in ns)
req=urllib.request.Request("https://api.github.com/graphql",data=json.dumps({"query":q}).encode(),headers={"Authorization":"Bearer "+TOK,"Content-Type":"application/json","User-Agent":"drafter/1.0"})
js=json.load(urllib.request.urlopen(req,timeout=120))
for e in js.get("errors") or []: print("ERR",json.dumps(e)[:200])
for n in ns:
    d=js["data"]["repository"].get("p%d"%n)
    if not d: print(n,"ABSENT"); continue
    print(n,"MERGED" if d["merged"] else d["state"],d["mergedAt"] or "-",((d["mergeCommit"] or {}).get("oid") or "-")[:12],d["headRefOid"][:12],d["title"][:60])
