import json,sys,base64,urllib.request,urllib.parse
envp="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
tok=None
for line in open(envp):
    if line.startswith("GH_TOKEN="): tok=line.split("=",1)[1].strip().strip('"').strip("'")
H={"Authorization":"Bearer "+tok,"Accept":"application/vnd.github+json","User-Agent":"wed-drafter-readonly"}
B="https://api.github.com/repos/Secuura/Distributed_Secuura"
sha,path,a,b=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
d=json.load(urllib.request.urlopen(urllib.request.Request(B+"/contents/"+urllib.parse.quote(path)+"?ref="+sha,headers=H),timeout=60))
t=base64.b64decode(d["content"]).decode(errors="replace").split("\n")
print("lines",len(t))
for i in range(a-1,min(b,len(t))): print(i+1,t[i])
