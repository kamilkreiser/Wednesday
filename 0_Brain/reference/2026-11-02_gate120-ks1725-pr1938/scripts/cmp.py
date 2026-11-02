import json,sys
from collections import Counter
def load(t):
    s=open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938/logs/driver_%s.json'%t).read()
    i=s.rindex('\n[\n {\n  "handler"')+1
    return json.loads(s[i:])
b,h=load('base'),load('head')
print('rows',len(b),len(h),'identical',b==h, 'bytes', json.dumps(b,sort_keys=False)==json.dumps(h,sort_keys=False))
print(Counter((r['handler'],r.get('status')) for r in h))
for r in h[:5]+[x for x in h if x['handler']=='auth'][:2]: print(r['handler'],r.get('status'),json.dumps(r.get('body',r.get('msg')))[:230])
print([r for r in h if r['handler'].endswith('plainError')][0])
