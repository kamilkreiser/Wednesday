#!/usr/bin/env python3
"""corrections_verify.py — READ-ONLY check of seat A's 17:53:16Z STATUS (the 03:5x §5f ruling applied). Linear query only; key by NAME, never printed."""
import json, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
key = [l.split('=',1)[1].strip().strip('"').strip("'") for l in open(ENV) if l.startswith('LINEAR_API_KEY=')][0]
def gql(q, v): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60))
print('corrections_verify', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
Q = 'query($id:String!){ issue(id:$id){ identifier state{name type} comments(first:100){nodes{id}} } }'
exp = {'KS-1165': '49ee639b', 'KS-932': '00c142ab', 'KS-1073': '23461917', 'KS-844': 'c3b9f334', 'KS-1183': '4628db7c'}
ok = []
for n, cid in exp.items():
    i = gql(Q, {'id': n})['data']['issue']
    ids = [c['id'] for c in i['comments']['nodes']]
    print(f"  {n}: {i['state']['name']}/{i['state']['type']} comments={len(ids)}")
    if n != 'KS-1183': ok.append((f'{n} In Progress', i['state']['name'] == 'In Progress'))
    ok.append((f'{n} comment {cid}', any(x.startswith(cid) for x in ids)))
i = gql(Q, {'id': 'KS-1130'})['data']['issue']; print('  KS-1130:', i['state']['name']); ok.append(('KS-1130 still Done', i['state']['name'] == 'Done'))
A = 'query($u:String!){ attachmentsForURL(url:$u){ nodes{ metadata issue{ identifier } } } }'
nodes = gql(A, {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/1010'})['data']['attachmentsForURL']['nodes']
kinds = sorted((x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in nodes)
print('  #1010 attachments:', kinds)
ok.append(('#1010 links = KS-1087 contributes + KS-1183 contributes', kinds == [('KS-1087', 'contributes'), ('KS-1183', 'contributes')]))
ctrl = any(k == 'closes' for _, k in kinds); print('  CONTROL any closes (must be False):', ctrl)
for k, v in ok: print(('  PASS ' if v else '  FAIL ') + k)
print('RESULT', 'ALL PASS' if all(v for _, v in ok) else 'NOT ALL PASS', f'({sum(v for _, v in ok)}/{len(ok)})')
