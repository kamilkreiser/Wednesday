import json,sys,re
d=json.load(open(sys.argv[1])); rows=[]
for f in d['testResults']:
    for t in f['assertionResults']:
        m=re.search(r'\b(R\d|C\d)\b',t['title']); tag=m.group(1) if m else '?'
        msg=' '.join(t.get('failureMessages') or [])
        by_assert = ('expect(' in msg) or ('toEqual' in msg)
        rows.append((f['name'].split('/')[-1][:60],tag,t['status'],by_assert,t['title'][:90]))
new={'R3','R4','R5','R6','C3','C4'}
from collections import Counter
c=Counter((('new' if r[1] in new else 'orig'), r[1], r[2], r[3] if r[2]=='failed' else '-') for r in rows)
for k,v in sorted(c.items()): print(v,k)
print('total',len(rows),'failed',sum(r[2]=='failed' for r in rows),'suites failed to run',sum(1 for f in d['testResults'] if f.get('status')=='failed' and not f['assertionResults']))
for r in rows:
    if r[2]=='failed': print('  FAIL',r[1],'assert' if r[3] else 'NOT-ASSERT',r[4])
