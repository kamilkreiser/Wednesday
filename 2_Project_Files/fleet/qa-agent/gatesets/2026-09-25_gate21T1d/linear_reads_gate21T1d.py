#!/usr/bin/env python3
"""linear_reads_gate21T1d.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, never printed): #1239's
attachmentsForURL (issues + linkKind), and KS-1263 / KS-1304 / KS-1305 (+ argv keys): identifier, title, state, archivedAt; KS-1263's description and
its comments' timestamps saved beside as linear_KS-1263.md. Re-keyed from gate21T2d's linear_reads_gate21T2d.py. Usage: linear_reads_gate21T1d.py [keys...]"""
import json, os, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate21T1d', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/1239'})
nodes = (r.get('data') or {}).get('attachmentsForURL', {}).get('nodes', []) if r.get('data') else []
print('#1239 attachmentsForURL: %d %s %s' % (len(nodes), [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes], r.get('errors', '')))
for k in ['KS-1263', 'KS-1304', 'KS-1305'] + sys.argv[1:]:
    r = q('query($id:String!){issue(id:$id){identifier title description state{name} archivedAt comments{nodes{createdAt}}}}', {'id': k})
    i = (r.get('data') or {}).get('issue')
    print('%s %s' % (k, ('state=%s archivedAt=%s comments=%d | %s' % (i['state']['name'], i['archivedAt'], len(i['comments']['nodes']), i['title'][:140])) if i else r.get('errors')))
    if i and k == 'KS-1263':
        open(os.path.join(G, 'linear_KS-1263.md'), 'w', encoding='utf-8').write('%s %s\nstate %s\ncomments at %s\n\n%s\n' % (k, i['title'], i['state']['name'], sorted(c['createdAt'] for c in i['comments']['nodes']), i.get('description') or ''))
