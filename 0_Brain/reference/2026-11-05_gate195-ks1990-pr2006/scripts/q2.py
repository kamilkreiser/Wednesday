import re,sys,hashlib
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate195-ks1990-pr2006/scratch/'
def cells(p):
    t=open(p).read().split('\n'); out={}; cur=None
    for i,l in enumerate(t):
        m=re.match(r"\s*it\('([^']*)'",l)
        if m:
            cur=m.group(1); out[cur]=[]
        if cur: out[cur].append(l)
    return out
b=cells(W+'ks1802_base.ts'); h=cells(W+'ks1802_head.ts')
print(len(b),len(h), list(b)==list(h))
for k in b:
    # cell body ends at first line '  });' ; truncate there
    def trim(ls):
        o=[]
        for l in ls:
            o.append(l)
            if l=='  });': break
        return o
    eq = trim(b[k])==trim(h[k])
    print(('EQUAL  ' if eq else 'CHANGED'), k[:60])
# control: edit one cell in a copy of base, expect unequal
c=open(W+'ks1802_base.ts').read().replace("'ks1802 ordinary'","'EDITED'",1)
open(W+'ks1802_ctl.ts','w').write(c)
cc=cells(W+'ks1802_ctl.ts')
k=[x for x in b if x.startswith('control KS-1802 C1')][0]
print('control(edited C1 vs base) equal?', cc[k]==b[k])
