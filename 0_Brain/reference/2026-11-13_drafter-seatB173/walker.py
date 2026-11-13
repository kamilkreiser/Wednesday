import subprocess,re
C="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB173/clone"
def g(*a): return subprocess.run(["git","-C",C]+list(a),capture_output=True,text=True,check=True).stdout
SKIP={'node_modules','dist','build','coverage','.git','__tests__','tests'}
def count(tree, planted=False):
    n=0
    for p in g("ls-tree","-r","--name-only","-z",tree).split("\0"):
        if not p.startswith("Blockchain/Dev/"): continue
        s=p[len("Blockchain/Dev/"):].split("/")
        if len(s)<4 or s[0] not in("services","packages") or s[2]!="src": continue
        segs=s[3:]
        if any(x in SKIP for x in segs[:-1]): continue
        name=segs[-1]
        if not name.endswith(".ts") or name.endswith(".d.ts"): continue
        if re.search(r"\.(test|spec)\.ts$",name): continue
        n+=1
    return n
dev=g("rev-parse","origin/develop").strip()
h=g("rev-parse","refs/remotes/pr/2079").strip()
t79=g("merge-tree","--write-tree",dev,h).strip()
print("410feda1a85e:",count("410feda1a85e"),"(gate 507)")
print("2079 head:",count(h),"(gate 500)")
print("dc57df60a959 + 2079 merge:",count(g("merge-tree","--write-tree","dc57df60a959",h).strip()),"(gate 501)")
print("develop a288aa45d6b2:",count(dev))
print("merge 2079 on a288aa45d6b2:",count(t79))
