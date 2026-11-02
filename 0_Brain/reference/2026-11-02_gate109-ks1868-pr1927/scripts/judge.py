# Mechanical tier-1 judge. usage: judge.py [tamper]
import json, sys, copy
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate109-ks1868-pr1927/logs/'
tamper = sys.argv[1] if len(sys.argv) > 1 else ''
fails=[]; checks=0
def load(lab, env):
  return {json.loads(l)['scenario']: json.loads(l) for l in open(W+'probe_%s_%s.jsonl'%(lab,env))}
def proj(r):
  # every field of the /record outcome + verify outcome except the verify error TEXT
  vb=copy.deepcopy(r['verify']['body'])
  if isinstance(vb.get('data'),dict) and 'error' in vb['data']: vb['data']['error']='<text>'
  return {'direct': {k:v for k,v in r['direct'].get('resolved',{'rejected':1}).items() if k!='error'},
          'recStatus': r['record']['status'], 'recBody': r['record']['body'], 'rows': [{k:v for k,v in x.items()} for x in r['recordRows']],
          'ops': r['recordOps'], 'recChain': r['recordChain'], 'verStatus': r['verify']['status'], 'verBody': vb, 'verChain': r['verifyChain']}
for env in ['test','production']:
  B=load('base',env); H=load('head',env)
  if tamper=='verified' and env=='test': H['lookup:revoked']['recordRows'][0]['minted']=True; H['lookup:revoked']['recordRows'][0]['status']='minted'
  if tamper=='status' and env=='test': H['init:getterThrows']['record']['status']=500
  for site in ['init','lookup']:
    ref=proj(B[site+':ord'])
    for v in ['ord','revoked','getterThrows']:
      checks+=1
      if proj(H[site+':'+v])!=ref: fails.append('%s %s head-%s != base-ord'%(env,site,v))
    for v in ['revoked','getterThrows']:
      b=B[site+':'+v]; checks+=1
      if not (b['record']['status']==500 and b['recordRows']==[] and b['recordOps']==[] and b['verify']['status']==500): fails.append('%s base %s:%s not 500+nothing'%(env,site,v))
  # never verified unless the chain lookup resolved
  for lab,D in (('base',B),('head',H)):
    for s,r in D.items():
      checks+=1
      resolved = r['recordChain']['txsResolved']>0
      bad = any(x['status']=='minted' or x['minted'] for x in r['recordRows']) or (r['record']['body'].get('data') or {}).get('onChainVerified') is True \
            or (r['verify']['body'].get('data') or {}).get('verified') is True or r['direct'].get('resolved',{}).get('verified') is True
      if bad and not (resolved and s=='none'): fails.append('%s %s %s VERIFIED without chain'%(env,lab,s))
  checks+=1
  if not any(x['status']=='minted' for x in H['none']['recordRows']): fails.append('positive control: none scenario not minted')
print('checks',checks,'fails',len(fails)); [print(' ',f) for f in fails]
sys.exit(1 if fails else 0)
