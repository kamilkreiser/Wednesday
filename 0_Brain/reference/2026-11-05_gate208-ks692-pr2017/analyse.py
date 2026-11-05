import json,sys
D=sys.argv[1]
L=lambda w:[json.loads(l) for l in open(f"{D}/evidence/authz_{w}.jsonl")]
h={ (r['op'],r['cred'],r['caller']):r for r in L('repo') if r['kind']=='cell'}
b={ (r['op'],r['cred'],r['caller']):r for r in L('base') if r['kind']=='cell'}
ok=lambda s:200<=s<300
rows=[];gains=[];narrow=[];admits=[];bad=[]
for k in sorted(h):
  H,B=h[k],b[k]
  rows.append(f"{k[0]:8} {k[1]:25} {k[2]:30} base={B['status']} head={H['status']} hw={H['writes']} hchg={H['stateChanged']} bw={B['writes']}")
  if ok(H['status']): admits.append(k)
  if ok(H['status']) and not ok(B['status']): gains.append(k)
  if ok(B['status']) and not ok(H['status']): narrow.append(k)
  if not ok(H['status']):
    if k[2]=='anonymous':
      if H['status']!=401: bad.append(('anon not 401',k,H['status']))
    else:
      same = H['status']==H['ctlStatus']==404 and H['body']==H['ctlBody'] and H['headers']==H['ctlHeaders']
      if not same: bad.append(('refusal != not-in-list 404',k,H['status'],H['body'],H['ctlBody']))
      if H['writes'] or H['stateChanged']: bad.append(('side effect',k))
  if ok(H['status']) and not (H['writes']==1 and H['stateChanged']): bad.append(('admit without write',k))
print("\n".join(rows))
print(f"\nCELLS {len(h)}; head admits {len(admits)}:"); [print('  ',a) for a in admits]
print(f"GAINS (head admits, base refused) {len(gains)}:"); [print('  ',g) for g in gains]
print(f"NARROWED (base admitted, head refuses) {len(narrow)}:"); [print('  ',n) for n in narrow]
print(f"ANOMALIES {len(bad)}:"); [print('  ',x) for x in bad]
# a sample refusal body/headers
k=('revoke','owned_by_creator','SYSTEM_ADMIN_other_tenant'); print("\nsample refusal body:",h[k]['body']); print("headers:",h[k]['headers']); print("ctl body:",h[k]['ctlBody'])
print("ms refusal vs ctl (max over cells):", max(abs(r['ms']-r['ctlMs']) for r in h.values() if not ok(r['status'])))
# base refusal statuses
from collections import Counter
print("base refusal statuses:",Counter(B['status'] for B in b.values() if not ok(B['status'])))
print("\nTRICKS head | base")
th=[r for r in L('repo') if r['kind']=='trick']; tb={ (r['name'],r['caller']):r for r in L('base') if r['kind']=='trick'}
for r in th:
  B=tb[(r['name'],r['caller'])]
  print(f"{r['name']:45} {r['caller']:20} head={r['status']} w={r['writes']} lc={r['listsChanged']} | base={B['status']} w={B['writes']} | {r['body'][:90]}")
