import json,sys,copy
L='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate111-ks1868-pr1929/logs/'
files=sys.argv[1:] or None
def load(ver,ne,override=None):
  p=(override or {}).get((ver,ne)) or L+f'probe_{ver}_{ne}.jsonl'
  return [json.loads(l) for l in open(p) if l.strip()]
fails=[];checks=0
def chk(c,msg):
  global checks; checks+=1
  if not c: fails.append(msg)
UNREAD=['revoked','getterThrows','nullProto']
ov={}
for a in sys.argv[1:]:
  k,v=a.split('=',1); ver,ne=k.split('_'); ov[(ver,ne)]=v
for ne in ['test','production']:
  B=load('base',ne,ov); H=load('head',ne,ov)
  strip=lambda r:{k:v for k,v in r.items() if k!='ver'}
  rb=[strip(r) for r in B if r['kind']=='route']; rh=[strip(r) for r in H if r['kind']=='route']
  chk(len(rb)==len(rh)==99, f'{ne}: route record count {len(rb)} {len(rh)}')
  for x,y in zip(rb,rh): chk(x==y, f"{ne}: route record differs {x['scen']} {x['step']}")
  def get(R,s,k): return [r for r in R if r.get('scen')==s and r['kind']==k][0]
  for k in ['boot','direct']:
    for s in sorted({r['scen'] for r in B if r['kind']==k}):
      b,h=get(B,s,k),get(H,s,k)
      chk(b['writes']==0 and h['writes']==0, f'{ne} {k} {s}: write in verifyDbReady record')
      if s not in UNREAD:
        chk(strip(b)==strip(h), f'{ne} {k} {s}: readable/hostile-msg record differs base vs head')
    for s in UNREAD:
      h=copy.deepcopy(get(H,s,k)); o=copy.deepcopy(get(H,'ordinary',k)); b=get(B,s,k)
      for x in (h,o):
        x.pop('scen');
        for lg in x['logs']: lg.pop('error',None)
      chk(strip(h)==strip(o), f'{ne} {k} {s}: head unreadable != head ordinary (error text masked)')
      hl=[lg for lg in get(H,s,k)['logs'] if lg['lvl']=='error']
      chk(len(hl)==1 and hl[0]['error']=='str:unreadable thrown value' and hl[0]['keys']==['error'], f'{ne} {k} {s}: head log not the single constant')
      if k=='direct': chk('rejected' in b['direct'], f'{ne} direct {s}: base did not reject')
      if k=='boot': chk(any('boot work failed' in d for d in b['dbLog']), f'{ne} boot {s}: base has no boot-work-failed line')
  # counter seeding visible in R3 proposalNumber
  for R,v in ((B,'base'),(H,'head')):
    for r in R:
      if r['kind']=='route' and r['step'].startswith('R3'):
        n=r['res']['body']['data']['proposalNumber']
        chk(n==(8 if r['scen']=='none' else 1), f"{ne} {v} {r['scen']}: R3 proposalNumber {n}")
  for R in (B,H):
    n=[r for r in R if r['kind']=='net'][0]; chk(n['outbound']==[], f'{ne}: outbound connect {n}')
print('checks',checks,'fails',len(fails))
for f in fails: print('FAIL',f)
sys.exit(1 if fails else 0)
