#!/usr/bin/env python3
"""linear_reads_gate21T2e.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, never printed): #1241
attachmentsForURL (issues carrying the PR + linkKind); KS-1226 (state, description saved as linear_KS-1226.md, comment count + the newest comment
ids/times); the four ids the round-2 READY says it filed for #1242's round-1 findings (KS-1306..KS-1309: identifier, title, state). Usage:
linear_reads_gate21T2e.py"""
import json, os, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate21T2e', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/1241'})
nodes = ((r.get('data') or {}).get('attachmentsForURL') or {}).get('nodes', [])
print('#1241 attachmentsForURL: %d %s %s' % (len(nodes), [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes], r.get('errors', '')))
r = q('query($id:String!){issue(id:$id){identifier title description state{name} archivedAt comments{nodes{id createdAt}}}}', {'id': 'KS-1226'})
i = (r.get('data') or {}).get('issue')
if i:
    cm = sorted(i['comments']['nodes'], key=lambda x: x['createdAt'])
    print('KS-1226 state=%s archivedAt=%s comments=%d newest=%s | %s' % (i['state']['name'], i['archivedAt'], len(cm), [(x['id'], x['createdAt']) for x in cm[-2:]], i['title'][:120]))
    open(os.path.join(G, 'linear_KS-1226.md'), 'w', encoding='utf-8').write('KS-1226 %s\nstate %s\n\n%s\n' % (i['title'], i['state']['name'], i.get('description') or ''))
else: print('KS-1226', r.get('errors'))
for k in ('KS-1306', 'KS-1307', 'KS-1308', 'KS-1309'):
    r = q('query($id:String!){issue(id:$id){identifier title state{name} archivedAt}}', {'id': k}); i = (r.get('data') or {}).get('issue')
    print('%s %s' % (k, ('state=%s archivedAt=%s | %s' % (i['state']['name'], i['archivedAt'], i['title'][:140])) if i else r.get('errors')))
