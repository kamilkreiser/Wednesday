import json, urllib.request, sys
env="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
key=None
for l in open(env):
    l=l.strip()
    if l.startswith("LINEAR_API_KEY") and "=" in l:
        key=l.split("=",1)[1].strip().strip('"').strip("'"); break
assert key, "no key"
q='''query($id:String!){issue(id:$id){identifier title state{name} description url
 comments(first:50){nodes{id createdAt user{name} body}}}}'''
out={}
for ident in sys.argv[1:]:
    r=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps({"query":q,"variables":{"id":ident}}).encode(),headers={"Authorization":key,"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(r,timeout=30))
    iss=d["data"]["issue"]; iss["comments"]["nodes"].sort(key=lambda c:c["createdAt"]); out[ident]=iss
json.dump(out,open(sys.argv[0].rsplit('/',1)[0]+"/tickets_ks911_ks912.json","w"),indent=1)
for k,v in out.items(): print(k,v["title"],v["state"]["name"],len(v["comments"]["nodes"]))
