import subprocess, json, re, os, sys
D="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB175"
C=D+"/clone_work/clone"
env=dict(os.environ); env["GH_CONFIG_DIR"]="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
def gh(*a):
    r=subprocess.run(["gh"]+list(a),capture_output=True,text=True,env=env)
    return r.returncode,r.stdout,r.stderr
def g(*a):
    return subprocess.run(["git","-C",C]+list(a),capture_output=True,text=True,check=True).stdout
dev=g("rev-parse","origin/develop").strip()
for n in [2227,2095,2090,2098,2089,2079,2220,2221,2222,2223,2224,2225,2099]:
    rc,o,e=gh("pr","view",str(n),"-R","Secuura/Distributed_Secuura","--json","state,isDraft,baseRefName,headRefOid,commits,files,mergeable,mergeStateStatus,body,title,additions,deletions")
    if rc!=0:
        print(n,"gh rc",rc,e[:200]); continue
    j=json.loads(o)
    gf=sorted(f["path"] for f in j["files"])
    h=j["headRefOid"]
    mb=g("merge-base",dev,h).strip()
    lf=sorted(l for l in g("diff","--name-only","-z",mb,h).split("\0") if l)
    body=j["body"] or ""
    dnm=len(re.findall(r"do not merge",body,flags=re.I))
    boxes=re.findall(r"- \[( |x)\] ",body)
    tierline=[l.strip()[:90] for l in body.splitlines() if re.search(r"tier\s*[12]",l,re.I)][:2]
    rc2,o2,e2=gh("api","repos/Secuura/Distributed_Secuura/commits/%s/check-runs?per_page=100"%h)
    cr="rc%d"%rc2
    if rc2==0:
        k=json.loads(o2)["check_runs"]
        from collections import Counter
        c=Counter((x["status"],x["conclusion"]) for x in k)
        cr="%d runs %s"%(len(k),dict(c))
    print(n,j["state"],"draft=%s"%j["isDraft"],j["baseRefName"],"head=%s"%h[:12],"commits=%d"%len(j["commits"]),"files=%d"%len(gf),"+%d -%d"%(j["additions"],j["deletions"]),"gh==git:%s"%(gf==lf),j["mergeable"],j["mergeStateStatus"],"dnm=%d"%dnm,"boxes=%s"%boxes,"checks:",cr)
    print("    tier lines:",tierline)
    print("    title:",j["title"][:110])
rc,o,e=gh("api","rate_limit","--jq",".resources.core")
print("rate_limit",o.strip())
rc,o,e=gh("pr","list","-R","Secuura/Distributed_Secuura","--search","KS-1699 in:title","--state","all","--json","number,title,state")
print("KS-1699 PR search:",o.strip())
rc,o,e=gh("pr","list","-R","Secuura/Distributed_Secuura","--search","created:>=2026-11-13","--state","all","--json","number,title,state")
print("PRs created >=2026-11-13:",o.strip()[:900])
