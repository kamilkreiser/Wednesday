import subprocess, itertools
D="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB172"
C=D+"/clone"
def g(*a):
    return subprocess.run(["git","-C",C]+list(a),capture_output=True,text=True,check=True).stdout
dev=g("rev-parse","origin/develop").strip()
rows=[2098,2097,2096,2095,2090,2089,2079,2220,2221,2222,2223,2224]
extra=[2226,2225,2160,2099,"r118"]
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
print("2226 files:",sorted(files[2226]))
print("r118 files:",sorted(files["r118"]))
print("r118 vs 2226:",len(files["r118"]&files[2226]),"; r118 vs 2225:",len(files['r118']&files[2225]),"; r118 vs 2160:",sorted(files['r118']&files[2160]))
print("r118 self:",len(files['r118']&files['r118']))
print("2099 vs 2226:",sorted(files[2099]&files[2226]))
print("2225 vs queued rows:",sorted(files[2225]&q))
print("2225 files:",sorted(files[2225]))
