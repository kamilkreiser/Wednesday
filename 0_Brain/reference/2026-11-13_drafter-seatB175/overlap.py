import subprocess, itertools
D="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB175"
C=D+"/clone_work/clone"
def g(*a):
    return subprocess.run(["git","-C",C]+list(a),capture_output=True,text=True,check=True).stdout
dev=g("rev-parse","origin/develop").strip()
rows=[2095,2090,2098,2089,2079,2220,2221,2222,2223,2224]
extra=[2225,2160,2099,2227,"r118an"]
files={};stat={}
for n in rows+extra:
    h=g("rev-parse","refs/remotes/pr/%s"%n).strip()
    mb=g("merge-base",dev,h).strip()
    names=[l for l in g("diff","--name-only","-z",mb,h).split("\0") if l]
    ns=g("diff","--numstat",mb,h).splitlines()
    files[n]=set(names)
    a=sum(int(l.split("\t")[0]) for l in ns if l.split("\t")[0].isdigit())
    d=sum(int(l.split("\t")[1]) for l in ns if l.split("\t")[1].isdigit())
    print(n,len(names),"+%d -%d"%(a,d))
q=set().union(*[files[n] for n in rows])
print("distinct queued paths (12 rows):",len(q))
pairs=list(itertools.combinations(rows,2))
hits=[(a,b,sorted(files[a]&files[b])) for a,b in pairs if files[a]&files[b]]
print("pairs",len(pairs),"intersecting",len(hits),hits)
print("positive control 2224 vs itself:",len(files[2224]&files[2224]))
for n in extra:
    inter=files[n]&q
    print("%s vs queued: %d %s"%(n,len(inter),sorted(inter)))
print("r118 files:",sorted(files["r118an"]))
print("r118 self:",len(files['r118']&files['r118']))
print("2225 vs queued rows:",sorted(files[2225]&q))
print("2225 files:",sorted(files[2225]))

LOCKS={"Blockchain/Dev/package-lock.json","Blockchain/Dev/services/mcp-server/package-lock.json"}
for n in rows+["r118an",2225,2227]:
    print("locks vs",n,sorted(files[n]&LOCKS))
print("2099 vs locks",sorted(files[2099]&LOCKS))
print("positive control locks vs 2099 nonempty:",bool(files[2099]&LOCKS))
R={"x"}
print("r118 files",sorted(files["r118an"]))
