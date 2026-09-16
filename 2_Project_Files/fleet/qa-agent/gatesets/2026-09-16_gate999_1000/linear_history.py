#!/usr/bin/env python3
"""READ-ONLY: Linear issue history (state transitions, attachment events) for KS-1129/KS-1130/KS-960, and the linear[bot] linkback summaries on #999/#1000. Keys by NAME; never printed; no mutations."""
import json, sys, urllib.request, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
vals={}
for line in open(ENV, encoding='utf-8'):
    for k in ('GH_TOKEN','LINEAR_API_KEY'):
        if line.startswith(k+'='): vals[k]=line.split('=',1)[1].strip().strip('"').strip("'")
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for n in (999,1000):
    r=urllib.request.urlopen(urllib.request.Request(f'https://api.github.com/repos/Secuura/Distributed_Secuura/issues/{n}/comments',headers={'Authorization':'Bearer '+vals['GH_TOKEN'],'Accept':'application/vnd.github+json'}),timeout=60)
    for c in json.load(r):
        sums=re.findall(r'<summary><a href="https://linear.app/secuura/issue/(KS-[0-9]+)/', c['body'] or '')
        print(f'PR #{n} linear[bot] linkback summaries (linked issues): {sums}')
def gql(q, v):
    r=urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query':q,'variables':v}).encode(), headers={'Authorization':vals['LINEAR_API_KEY'],'Content-Type':'application/json'}), timeout=60)
    j=json.load(r); assert 'errors' not in j, j.get('errors'); return j['data']
Q='''query($id:String!){ issue(id:$id){ identifier state{name} history(first:50){ nodes{ createdAt actor{name} fromState{name} toState{name} addedLabels{name} attachment{url} } } } }'''
for ident in ('KS-1129','KS-1130','KS-960'):
    i=gql(Q,{'id':ident})['issue']
    print(f"\n{i['identifier']} now [{i['state']['name']}]")
    for h in sorted(i['history']['nodes'], key=lambda h:h['createdAt']):
        if h['fromState'] or h['toState'] or h['attachment']:
            print(f"   {h['createdAt']} actor={h['actor']['name'] if h['actor'] else 'integration/none'} {h['fromState']['name'] if h['fromState'] else ''} -> {h['toState']['name'] if h['toState'] else ''} attachment={h['attachment']['url'] if h['attachment'] else ''}")
