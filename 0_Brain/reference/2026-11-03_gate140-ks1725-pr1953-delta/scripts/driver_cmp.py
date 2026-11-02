import json,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta/logs/'
a=json.load(open(G+sys.argv[1])); b=json.load(open(G+sys.argv[2])); n=0
for k in a:
    eq=json.dumps(a[k])==json.dumps(b[k]); n+=not eq
    print(('EQUAL ' if eq else 'DIFF  ')+k + ('' if isinstance(a[k],list) or isinstance(a[k],str) else '  status %s/%s'%(a[k]['status'],b[k]['status'])))
    if not eq: print('   base',json.dumps(a[k])[:600]); print('   head',json.dumps(b[k])[:600])
print('rows',len(a),'diff',n)
