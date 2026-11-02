import json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate109-ks1868-pr1927/logs/'
def cell(r):
  d=r['direct']; d=('REJ '+d['rejected'][:28]) if 'rejected' in d else '%s/%s/%s'%(d['resolved']['verified'],d['resolved']['status'],d['resolved'].get('error','-')[:24])
  rb=r['record']['body']; dd=rb.get('data') or {}
  rec='%d v=%s s=%s rows=%s'%(r['record']['status'],dd.get('onChainVerified','-'),dd.get('onChainStatus','-'),[(x['status'],x['minted']) for x in r['recordRows']])
  vb=r['verify']['body']; vd=vb.get('data') or {}
  ver='%d %s'%(r['verify']['status'], json.dumps(vd if vd else vb.get('error',{}).get('message'),sort_keys=True)[:70])
  ch='rc=%s vc=%s'%(r['recordChain']['txs'],r['verifyChain']['txs'])
  lt=r['recordLogThrows']+r['verifyLogThrows']+r.get('directLogThrows',[])
  return d,rec,ver,ch,lt
for env in ['test','production']:
  for lab in ['base','head']:
    print('==',lab,env)
    for l in open(W+'probe_%s_%s.jsonl'%(lab,env)):
      r=json.loads(l); d,rec,ver,ch,lt=cell(r)
      print('%-20s | %-38s | %-58s | %s | %s %s'%(r['scenario'],d,rec,ver,ch,lt if lt else ''))
