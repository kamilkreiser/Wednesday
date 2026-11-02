import json, sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate109-ks1868-pr1927/logs/'
for env in ['test','production']:
  for lab in ['base','head']:
    print('==', lab, env)
    for l in open(W+'probe_%s_%s.jsonl'%(lab,env)):
      r=json.loads(l)
      d=r['direct']; d=('REJ '+d['rejected']) if 'rejected' in d else json.dumps(d['resolved'],sort_keys=True)
      rb=r['record']['body']; rbs=json.dumps(rb.get('data',rb.get('error')),sort_keys=True)
      print(f"{r['scenario']:22} direct={d}")
      print(f"{'':22} record={r['record']['status']} {rbs} rows={r['recordRows']} chain={r['recordChain']} logthrows={r['recordLogThrows']}")
      print(f"{'':22} verify={r['verify']['status']} {json.dumps(r['verify']['body'],sort_keys=True)} chain={r['verifyChain']} logthrows={r['verifyLogThrows']}")
      print(f"{'':22} recordLogs={r['recordLogs']}")
