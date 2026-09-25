#!/usr/bin/env python3
"""linear_reads_gate21T2d.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, never printed): for #1241 and
#1242, attachmentsForURL (which issues carry the PR, and the linkKind metadata); for KS-1226 and KS-980 (+ every foreign key a PR body names, passed
as argv): identifier, title, state, archivedAt, assignee, and the DESCRIPTION saved beside as linear_<key>.md (the ticket's own claim, for the
through-code review). Derived from gate21T2c's linear_reads_gate21T2c.py, re-keyed. Usage: linear_reads_gate21T2d.py [extra keys...]"""
import json, os, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate21T2d', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
for n in ('1241', '1242'):
    url = 'https://github.com/Secuura/Distributed_Secuura/pull/' + n
    r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': url})
    nodes = (r.get('data') or {}).get('attachmentsForURL', {}).get('nodes', []) if r.get('data') else []
    print('#%s attachmentsForURL: %d %s %s' % (n, len(nodes), [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes], r.get('errors', '')))
for k in ['KS-1226', 'KS-980'] + sys.argv[1:]:
    r = q('query($id:String!){issue(id:$id){identifier title description state{name} archivedAt assignee{email}}}', {'id': k})
    i = (r.get('data') or {}).get('issue')
    print('%s %s' % (k, ('state=%s archivedAt=%s assignee=%s | %s' % (i['state']['name'], i['archivedAt'], (i.get('assignee') or {}).get('email'), i['title'][:120])) if i else r.get('errors')))
    if i and k in ('KS-1226', 'KS-980'):
        open(os.path.join(G, 'linear_%s.md' % k), 'w', encoding='utf-8').write('%s %s\nstate %s\n\n%s\n' % (k, i['title'], i['state']['name'], i.get('description') or ''))
