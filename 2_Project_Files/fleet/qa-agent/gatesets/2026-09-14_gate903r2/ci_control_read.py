#!/usr/bin/env python3
"""ci_control_read.py — READ-ONLY: the jobs + failed steps of develop's OWN runs at M18 8861e6216 for the workflows red at the #903 head
(the control for 'develop-own'); token by NAME, never printed."""
import json, sys, urllib.request, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; G=sys.argv[1]
tok=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok=line.split('=',1)[1].strip().strip('"').strip("'")
assert tok
base='https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(base+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}), timeout=60))
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
runs=get('/actions/runs?head_sha=8861e62161466c40f08d2b10a30edeb203123993&per_page=50')
print('runs at develop M18:', runs['total_count'])
out=[]
for r in runs['workflow_runs']:
    jobs=get(f"/actions/runs/{r['id']}/jobs?per_page=50")
    js=[]
    for j in jobs['jobs']:
        fs=[(s['number'], s['name'], s['conclusion']) for s in j['steps'] if s['conclusion']=='failure']
        js.append({'name':j['name'],'status':j['status'],'conclusion':j['conclusion'],'failed_steps':fs})
    out.append({'run':r['name'],'id':r['id'],'event':r['event'],'status':r['status'],'conclusion':r['conclusion'],'created':r['created_at'],'jobs':js})
    print(f"  run {r['name']!r} id={r['id']} event={r['event']} status={r['status']} conclusion={r['conclusion']} created={r['created_at']}")
    for j in js:
        if j['conclusion'] in ('failure',) or j['failed_steps']: print(f"     job {j['name']!r} {j['status']}/{j['conclusion']} failed_steps={j['failed_steps']}")
json.dump(out, open(f'{G}/gh/ci_at_develop_M18_summary.json','w'), indent=1)
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
