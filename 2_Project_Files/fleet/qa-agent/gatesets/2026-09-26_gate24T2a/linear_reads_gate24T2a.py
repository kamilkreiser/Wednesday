#!/usr/bin/env python3
"""linear_reads_gate24T2a.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, never printed) for the
round-24 tier-2 batch gate24T2a: attachmentsForURL for #1243, #1244, #1245, #1248 (issues carrying each PR + linkKind); KS-1117, KS-1300, KS-1111,
KS-1313, KS-1143 (state, description saved as linear_<KEY>.md, comment count + the newest comment ids/times); KS-1226 (the #1241 lineage, state only).
Writes only beside this script. Usage: linear_reads_gate24T2a.py"""
import json, os, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate24T2a', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
for n in ('1243', '1244', '1245', '1248', '1241'):
    r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/' + n})
    nodes = ((r.get('data') or {}).get('attachmentsForURL') or {}).get('nodes', [])
    print('#%s attachmentsForURL: %d %s %s' % (n, len(nodes), [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes], r.get('errors', '')))
for k in ('KS-1117', 'KS-1300', 'KS-1111', 'KS-1313', 'KS-1143', 'KS-1144', 'KS-1226'):
    r = q('query($id:String!){issue(id:$id){identifier title description state{name} archivedAt comments{nodes{id createdAt}}}}', {'id': k})
    i = (r.get('data') or {}).get('issue')
    if not i:
        print(k, r.get('errors')); continue
    cm = sorted(i['comments']['nodes'], key=lambda x: x['createdAt'])
    print('%s state=%s archivedAt=%s comments=%d newest=%s | %s' % (k, i['state']['name'], i['archivedAt'], len(cm), [(x['id'], x['createdAt']) for x in cm[-2:]], i['title'][:140]))
    if k not in ('KS-1226', 'KS-1144'):
        open(os.path.join(G, 'linear_%s.md' % k), 'w', encoding='utf-8').write('%s %s\nstate %s\n\n%s\n' % (k, i['title'], i['state']['name'], i.get('description') or ''))
