import json, urllib.request
ENVF="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
key=[l.split("=",1)[1].strip().strip('"').strip("'") for l in open(ENVF) if l.startswith("LINEAR_API_KEY=")][0]
def gq(q,v=None):
    req=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps({"query":q,"variables":v or {}}).encode(),headers={"Authorization":key,"Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(req,timeout=60))["data"]
i=gq("""query{issue(id:"KS-1699"){title description comments(first:50){nodes{createdAt body}}}}""")["issue"]
print(i["title"]); print(i["description"][:3500]); 
cs=sorted(i["comments"]["nodes"],key=lambda c:c["createdAt"])
print("=== newest comment"); print(cs[-1]["body"][:3500])
