import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate111-ks1868-pr1929/logs/'
for ne in ['test','production']:
  print('== NODE_ENV',ne)
  for ver in ['base','head']:
    for l in open(W+f'probe_{ver}_{ne}.jsonl'):
      r=json.loads(l)
      if r['kind']=='boot':
        lg=[(x['lvl'],x['msg'][:40],x.get('error','')[:45],x['loggerThrew']) for x in r['logs']]
        print(ver,r['scen'].ljust(15),'BOOT init',r['initOut'],'writes',r['writes'],'unh',r['unhandled'],'dbLog',[d[:120] for d in r['dbLog'] if 'boot work' in d],'logs',[x for x in lg if x[0]=='error'])
      elif r['kind']=='direct':
        lg=[(x['lvl'],x['msg'][:40],x.get('error','')[:45],x['loggerThrew']) for x in r['logs']]
        print(ver,r['scen'].ljust(15),'DIRECT',r['direct'],'writes',r['writes'],'ops',len(r['ops']),'logs',lg)
      elif r['kind']=='net':
        print(ver,'NET',r)
