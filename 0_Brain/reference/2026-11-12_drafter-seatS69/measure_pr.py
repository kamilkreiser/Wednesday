import json,re,sys,urllib.request,collections
D="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS69"
ip=json.load(open(D+"/ip_live.json"))
TOK=None
for l in open("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env",encoding="utf-8",errors="replace"):
    m=re.match(r"\s*(?:export\s+)?GH_TOKEN=(.*)$",l.rstrip("\n"))
    if m: TOK=m.group(1).strip().strip("\"'")
prs=set(); other=[]
for i in ip:
    for a in i["attachments"]["nodes"]:
        m=re.fullmatch(r"https://github.com/Secuura/Distributed_Secuura/pull/(\d+)",a["url"])
        if m: prs.add(int(m.group(1)))
        elif a["sourceType"]=="github": other.append((i["identifier"],a["url"]))
prs=sorted(prs|{2175,2109,2195,2205})  # controls: 2175,2109 MERGED; 2195 OPEN at S68 wrap
print("distinct PRs",len(prs),"other github",other)
state={}
for k in range(0,len(prs),80):
    ch=prs[k:k+80]
    q="query { repository(owner:\"Secuura\", name:\"Distributed_Secuura\") { %s } rateLimit{cost remaining} }"%" ".join("p%d: pullRequest(number:%d){number state merged}"%(n,n) for n in ch)
    req=urllib.request.Request("https://api.github.com/graphql",data=json.dumps({"query":q}).encode(),headers={"Authorization":"Bearer "+TOK,"Content-Type":"application/json","User-Agent":"drafter/1.0"})
    js=json.load(urllib.request.urlopen(req,timeout=120))
    for e in js.get("errors") or []: print("ERR",json.dumps(e)[:200])
    for n in ch:
        d=js["data"]["repository"].get("p%d"%n)
        state[n]=None if d is None else ("MERGED" if d["merged"] else d["state"])
    print("rate",js["data"]["rateLimit"])
json.dump(state,open(D+"/pr_states.json","w"))
print(collections.Counter(state.values()))
print("controls",{n:state[n] for n in (2175,2109,2195,2205)})
