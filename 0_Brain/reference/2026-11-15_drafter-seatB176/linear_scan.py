import json, urllib.request
ENVF="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
key=[l.split("=",1)[1].strip().strip('"').strip("'") for l in open(ENVF) if l.startswith("LINEAR_API_KEY=")][0]
def gq(q,v=None):
    req=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps({"query":q,"variables":v or {}}).encode(),headers={"Authorization":key,"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(req,timeout=60)); assert not d.get("errors"),d["errors"]; return d["data"]
i=gq("""query{issue(id:"KS-1695"){description comments(first:50){nodes{createdAt body}} history(first:10){nodes{createdAt}} }}""")["issue"]
txt=i["description"]+"\n"+"\n".join(c["body"] for c in i["comments"]["nodes"])
for t in ("2228","KS-1699","1667","KS-1695"): print("KS-1695 text occurrences",t,txt.count(t))
j=gq("""query{issue(id:"KS-1699"){relations(first:20){nodes{type relatedIssue{identifier}}} inverseRelations(first:20){nodes{type issue{identifier}}} children(first:10){nodes{identifier}} parent{identifier} comments(first:50){nodes{createdAt body}}}}""")["issue"]
print("KS-1699 relations",[(r["type"],r["relatedIssue"]["identifier"]) for r in j["relations"]["nodes"]],"inverse",[(r["type"],r["issue"]["identifier"]) for r in j["inverseRelations"]["nodes"]],"children",len(j["children"]["nodes"]),"parent",j["parent"])
tx="\n".join(c["body"] for c in j["comments"]["nodes"])
print("KS-1699 comments mention share:",tx.lower().count("/:id/share"),"recertify:",tx.lower().count("recertify"))
print("KS-1699 mentions of 'mention' nodes in comments (@kamil) count:",tx.count("@kamil"))
