import sys,collections
def load(p):
    d={}
    for l in open(p,encoding='utf-8'):
        f=l.rstrip('\n').split('\t'); d[tuple(f[:3])]=(int(f[3]),int(f[4]),int(f[5]),int(f[6]),f[7])
    return d
m=load(sys.argv[1]); b=load(sys.argv[2])
assert m.keys()==b.keys(), "row keys differ"
lower=[];raised=collections.Counter();same=0;changed_eq=[]
for k in m:
    (mr,mb,ms,md,mx),(br,bb,bs,bd,bx)=m[k],b[k]
    if br<mr or (br==mr and mr not in(0,10) and (bb>mb or bs>ms or bd<md)):
        lower.append((k,m[k],b[k]))
    elif (mr,mb,ms,md)!=(br,bb,bs,bd): raised[(k[0],mx,bx)]+=1
    else:
        same+=1
        if mx!=bx: changed_eq.append((k,mx,bx))
print('rows',len(m),'unchanged',same,'raised',sum(raised.values()),'LOWERED',len(lower))
for x in lower[:30]: print('LOWER',x)
tools=collections.Counter(k[0] for k in raised)
print('raised by tool:',dict(sorted(tools.items())))
print('same-rank, different summary:',len(changed_eq), changed_eq[:5])
# tools never raised (decisions identical everywhere)
alltools=sorted({k[0] for k in m}); print('tools with no change:',[t for t in alltools if t not in tools])
