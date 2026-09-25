#!/usr/bin/env python3
"""linear_reads_gate24T2d.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, never printed) for gate24T2d:
attachmentsForURL for #1250, #1253, #1262, #1263, #1264, #1265, #1266; and KS-1302, KS-1303, KS-1297, KS-1310, KS-1311, KS-1140, KS-1281, KS-1315, KS-1120 (state, description saved as linear_<KEY>.md, comment count +
newest comment ids/times), plus KS-1305 (MODE F residual) and KS-1293 (the :1 -> :2 criterion #1262 touches), state only. Writes only beside this
script. Usage: linear_reads_gate24T2d.py"""
import json, os, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate24T2d', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
for n in ('1250', '1253', '1262', '1263', '1264', '1265', '1266'):
    r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/' + n})
    nodes = ((r.get('data') or {}).get('attachmentsForURL') or {}).get('nodes', [])
    print('#%s attachmentsForURL: %d %s %s' % (n, len(nodes), [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes], r.get('errors', '')))
SAVE = ('KS-1302', 'KS-1303', 'KS-1297', 'KS-1310', 'KS-1311', 'KS-1140', 'KS-1281', 'KS-1315', 'KS-1120')
for k in SAVE + ('KS-1305', 'KS-1293'):
    r = q('query($id:String!){issue(id:$id){identifier title description state{name} archivedAt comments{nodes{id createdAt}}}}', {'id': k})
    i = (r.get('data') or {}).get('issue')
    if not i:
        print(k, r.get('errors')); continue
    cm = sorted(i['comments']['nodes'], key=lambda x: x['createdAt'])
    print('%s state=%s archivedAt=%s comments=%d newest=%s | %s' % (k, i['state']['name'], i['archivedAt'], len(cm), [(x['id'], x['createdAt']) for x in cm[-2:]], i['title'][:140]))
    if k in SAVE:
        open(os.path.join(G, 'linear_%s.md' % k), 'w', encoding='utf-8').write('%s %s\nstate %s\n\n%s\n' % (k, i['title'], i['state']['name'], i.get('description') or ''))
