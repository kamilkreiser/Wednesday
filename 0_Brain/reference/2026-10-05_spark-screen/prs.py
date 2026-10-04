import json,os,urllib.request
tok=os.environ["GH_TOKEN"]; R="https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(u):
    req=urllib.request.Request(u,headers={"Authorization":"Bearer "+tok,"Accept":"application/vnd.github+json"})
    return json.load(urllib.request.urlopen(req))
prs=[];p=1
while True:
    d=get(f"{R}/pulls?state=open&per_page=100&page={p}"); prs+=d
    if len(d)<100: break
    p+=1
out=[]
for pr in prs:
    files=[];q=1
    while True:
        f=get(f"{R}/pulls/{pr['number']}/files?per_page=100&page={q}"); files+=[x["filename"] for x in f]
        if len(f)<100: break
        q+=1
    out.append({"n":pr["number"],"title":pr["title"],"head":pr["head"]["ref"],"user":pr["user"]["login"],"draft":pr["draft"],"files":files})
json.dump(out,open(os.environ["S"]+"/prs.json","w"),indent=1)
print(len(out),"open PRs")
for o in out: print(o["n"],o["head"],len(o["files"]),o["title"][:80])
