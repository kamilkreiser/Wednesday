#!/usr/bin/env python3
"""linear_reads_gate21T2b.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, never printed): for each of the
five PR URLs, attachmentsForURL (which issues carry it, and the linkKind metadata); for the own keys + the foreign keys the five bodies name + the
carried-wording ticket (KS-1155 load false-red): state, archivedAt, assignee, title. Derived from gate21T2's linear_reads_gate21T2.py, re-keyed."""
import json, urllib.request, datetime
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate21T2b', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
for n in ('1225', '1227', '1229', '1231', '1232'):
    url = 'https://github.com/Secuura/Distributed_Secuura/pull/' + n
    r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': url})
    nodes = (r.get('data') or {}).get('attachmentsForURL', {}).get('nodes', []) if r.get('data') else []
    print('#%s attachmentsForURL: %d %s %s' % (n, len(nodes), [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes], r.get('errors', '')))
OWN = ('KS-1291', 'KS-1252', 'KS-1253', 'KS-865', 'KS-808', 'KS-1281', 'KS-1128')
FOREIGN = ('KS-1265', 'KS-1277', 'KS-1031', 'KS-318', 'KS-897')
CARRIED = ('KS-1155',)
for grp, keys in (('OWN', OWN), ('FOREIGN (named in a body)', FOREIGN), ('CARRIED', CARRIED)):
    print('--', grp)
    for k in keys:
        r = q('query($id:String!){issue(id:$id){identifier title state{name} archivedAt assignee{email}}}', {'id': k})
        i = (r.get('data') or {}).get('issue')
        print('%s %s' % (k, ('state=%s archivedAt=%s assignee=%s | %s' % (i['state']['name'], i['archivedAt'], (i.get('assignee') or {}).get('email'), i['title'][:100])) if i else r.get('errors')))
