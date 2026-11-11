import json,sys,base64,urllib.request
envp="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
tok=None
for line in open(envp):
    if line.startswith("GH_TOKEN="): tok=line.split("=",1)[1].strip().strip('"').strip("'")
H={"Authorization":"Bearer "+tok,"Accept":"application/vnd.github+json","User-Agent":"wed-drafter-readonly"}
B="https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=60))
sha=sys.argv[1]; terms=sys.argv[2:]
for e in get(B+"/contents/.github/workflows?ref="+sha):
    d=get(e["url"]); t=base64.b64decode(d["content"]).decode(errors="replace")
    print(e["name"],len(t),"bytes","on:" in t,{x:t.lower().count(x.lower()) for x in terms})
