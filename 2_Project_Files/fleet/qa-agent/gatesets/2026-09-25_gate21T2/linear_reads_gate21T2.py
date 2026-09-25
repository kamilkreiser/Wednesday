#!/usr/bin/env python3
"""linear_reads_gate21T2.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, never printed): for each of the
six PR URLs, attachmentsForURL (which issues carry it, and the linkKind metadata); for the own keys + the foreign keys the six bodies name + the
carried-wording tickets (KS-562 anchoring red, KS-1155 load false-red): state, archivedAt, assignee, title. Derived from gate21T1's script."""
import json, urllib.request, datetime
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate21T2', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
for n in ('1215', '1218', '1220', '1221', '1222', '1223'):
    url = 'https://github.com/Secuura/Distributed_Secuura/pull/' + n
    r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': url})
    nodes = (r.get('data') or {}).get('attachmentsForURL', {}).get('nodes', []) if r.get('data') else []
    print('#%s attachmentsForURL: %d %s %s' % (n, len(nodes), [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes], r.get('errors', '')))
OWN = ('KS-1288', 'KS-897', 'KS-896', 'KS-1129', 'KS-1266', 'KS-1181', 'KS-1118')
FOREIGN = ('KS-1126', 'KS-1195', 'KS-1239', 'KS-818', 'KS-833', 'KS-858', 'KS-1086', 'KS-1135', 'KS-1175', 'KS-584', 'KS-1228', 'KS-1265', 'KS-485', 'KS-973', 'KS-727')
CARRIED = ('KS-562', 'KS-1155', 'KS-1143', 'KS-1291')
for grp, keys in (('OWN', OWN), ('FOREIGN (named in a body)', FOREIGN), ('CARRIED', CARRIED)):
    print('--', grp)
    for k in keys:
        r = q('query($id:String!){issue(id:$id){identifier title state{name} archivedAt assignee{email}}}', {'id': k})
        i = (r.get('data') or {}).get('issue')
        print('%s %s' % (k, ('state=%s archivedAt=%s assignee=%s | %s' % (i['state']['name'], i['archivedAt'], (i.get('assignee') or {}).get('email'), i['title'][:100])) if i else r.get('errors')))
