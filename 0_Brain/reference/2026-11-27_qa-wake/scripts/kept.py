import sys,datetime
sys.dont_write_bytecode=True
sys.path.insert(0,sys.argv[1])
import wake_pack as wp
G="/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md"
today=datetime.date.fromisoformat(sys.argv[2]); seat=sys.argv[3]
inexp=False; n=0
for i,l in enumerate(open(G,encoding="utf-8").read().split("\n"),1):
    if l.startswith("## "): inexp=l[3:].strip().lower().startswith("expired"); continue
    if not l.startswith("|"): continue
    cells=l.split("|")[1:-1]; c0=cells[0].strip() if cells else ""
    if c0.lower()=="grant" or (c0 and set(c0)<=set("-: ")): continue
    n+=1
    v,why=wp.classify_grant(l,seat,today)
    if len(sys.argv)>4:
        print(i,v); continue
    if v in("mine","unclassified"):
        print("=== line %d | %s%s | %d cells | %d B"%(i,v," (under Expired)" if inexp else "",len(cells),len(l.encode())))
        print("  C1:",c0[:260]); print("  EXP:",(cells[2].strip()[:260] if len(cells)>2 else "-"))
print("rows",n)
