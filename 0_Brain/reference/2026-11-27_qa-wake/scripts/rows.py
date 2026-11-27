import re,sys
G="/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md"
lines=open(G,encoding="utf-8").read().split("\n")
want=[int(x) for x in sys.argv[2].split(",")]
mode=sys.argv[1]
KW=re.compile(r"wednesday|\bwed\b|all seats|both seats|every seat|all three|fleet|each seat|any seat|coordinator|all agents|secuura|general|studio|this seat|both coordinators|either seat",re.I)
for n in want:
    l=lines[n-1]; cells=l.split("|")[1:-1]
    print("=== line %d | %d cells | %d bytes"%(n,len(cells),len(l.encode())))
    if mode=="other":
        print(" C1:",cells[0].strip()[:600])
        print(" EXP:",(cells[2].strip()[:300] if len(cells)>2 else "-"))
        rest="|".join(cells)
        hits=[]
        for m in KW.finditer(rest):
            s=max(0,m.start()-70); e=min(len(rest),m.end()+70)
            hits.append("..."+rest[s:e].replace("\n"," ")+"...")
        print(" KW hits: %d"%len(hits))
        for h in hits[:8]: print("   ",h)
    else:
        print(" C1:",cells[0].strip()[:900])
        print(" GIVEN:",(cells[1].strip()[:200] if len(cells)>1 else "-"))
        print(" EXP:",(cells[2].strip()[:700] if len(cells)>2 else "-"))
