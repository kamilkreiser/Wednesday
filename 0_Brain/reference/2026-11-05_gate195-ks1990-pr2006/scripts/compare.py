import json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate195-ks1990-pr2006/runs/'
def load(s): return {r['cell']:r for r in map(json.loads,open(W+'matrix_%s.jsonl'%s))}
b=load('base'); h=load('head')
def perm(r): return (isinstance(r['status'],int) and 200<=r['status']<300) or r.get('success') is True
more=0; changed=0
for k in b:
    x,y=b[k],h[k]
    f=lambda r:(r['status'],r.get('success'),r.get('created'),r.get('alreadyPresent'),r.get('failed'),r.get('seededUsers'),r['keys'])
    ch=f(x)!=f(y); changed+=ch
    mp = perm(y) and not perm(x)
    # more permissive: head 2xx where base non-2xx, or success true where base false
    s2=lambda r:isinstance(r['status'],int) and 200<=r['status']<300
    mp = (s2(y) and not s2(x)) or (y.get('success') is True and x.get('success') is not True)
    more+=mp
    print('%-40s base %s/%s c%s a%s f%s | head %s/%s c%s a%s f%s %s%s'%(k,x['status'],x.get('success'),x.get('created'),x.get('alreadyPresent'),x.get('failed'),y['status'],y.get('success'),y.get('created'),y.get('alreadyPresent'),y.get('failed'),'CHANGED ' if ch else '','MORE-PERMISSIVE' if mp else ''))
print('cells',len(b),'changed',changed,'more_permissive',more)
for k in h:
    if k.startswith('leak'): print(k,'head leakHits=',repr(h[k]['leakHits']),'logHasToken=',h[k]['logHasToken'],'bytes',h[k]['bodyBytes'],'| base leakHits=',repr(b[k]['leakHits']))
print('keys head 500 cell:',h['all14fail']['keys'])
