import json,re,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate121-ks1940-pr1939'
def load(v): return {(r['cell'],r['value']):r for r in map(json.loads,open(f'{W}/logs/probe_{v}.jsonl'))}
B,Hd=load('base'),load('head')
U=re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'); D=re.compile(r'2026-11-\d\dT[0-9:.]+Z')
N1=re.compile(r'"proposalNumber": \d+'); N2=re.compile(r'Proposal #\d+')
# absolute proposal numbers accumulate across cells (base moves the counter in failure cells); the per-cell move is checked by counterDelta
def norm(x): return N2.sub('Proposal #N',N1.sub('"proposalNumber": N',D.sub('<now>',U.sub('<uuid>',json.dumps(x,sort_keys=True)))))
def code(r): b=r['body']; return (b or {}).get('error',{}).get('code') if isinstance(b,dict) and isinstance(b.get('error'),dict) else ('ok' if isinstance(b,dict) and b.get('success') else None)
SU={'success':False,'error':{'code':'SERVICE_UNAVAILABLE','message':'Governance participant store is temporarily unavailable'}}
rows=[];fails=[];checks=0
def chk(c,msg):
  global checks; checks+=1
  if not c: fails.append(msg)
for k in sorted(B, key=lambda k:(list(B).index(k))):
  b,h=B[k],Hd[k]; cell,val=k
  def s(r): return f"{r['status']} {code(r)} w={len(r['writes'])} {'UNCH' if r['unchanged'] else 'CHANGED'} cd={r['counterDelta']}"
  rows.append(f"{cell:36} {val:14} | base {s(b):40} | head {s(h)}")
  for r,v in((b,'base'),(h,'head')):
    chk(not r['unknown'],f'{k} {v} unknown sql {r["unknown"]}')
    chk(not r['plantedInLogs'],f'{k} {v} planted in logs')
  if val=='none' or cell=='get_absent':  # get_absent has no fault: every value is a control
    chk(norm({x:b[x] for x in('status','body','writes','reads','after','counterDelta')})==norm({x:h[x] for x in('status','body','writes','reads','after','counterDelta')}),f'{k} control base!=head')
  else:
    chk(h['status']==503 and h['body']==SU,f'{k} head not 503 SU: {h["status"]} {h["body"]}')
    chk(h['writes']==[] and h['unchanged'],f'{k} head wrote {h["writes"]}')
    chk(h['counterDelta']==1,f'{k} head counter moved {h["counterDelta"]}')
    # head logs: constant reason for unreadable
    if val not in('error','string'):
      chk(all('unreadable thrown value' in l[0] for l in h['logs']) and len(h['logs'])>=1,f'{k} head log {h["logs"]}')
print('\n'.join(rows)); print(f'\nCHECKS {checks} FAILED {len(fails)}'); print('\n'.join(fails))
