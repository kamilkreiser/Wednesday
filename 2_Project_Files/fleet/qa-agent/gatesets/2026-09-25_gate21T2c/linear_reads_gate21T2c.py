#!/usr/bin/env python3
"""linear_reads_gate21T2c.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, never printed): for each of the
eight PR URLs (#1223 ROUND 2 widened in by Wednesday 06:3xZ), attachmentsForURL (which issues carry it, and the linkKind metadata); for the own keys + every foreign key a PR body names
(#1218: KS-1086; #1219: KS-480, KS-1228, KS-1264; #1233: KS-1213 (+ its own second key KS-1229); #1238: KS-979, KS-1155) + KS-1118 (#1223, not in the
batch): state, archivedAt, assignee. Derived from gate21T1b's linear_reads_gate21T1b.py, re-keyed."""
import json, urllib.request, datetime
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate21T2c', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
for n in ('1218', '1219', '1223', '1233', '1235', '1236', '1237', '1238'):
    url = 'https://github.com/Secuura/Distributed_Secuura/pull/' + n
    r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': url})
    nodes = (r.get('data') or {}).get('attachmentsForURL', {}).get('nodes', []) if r.get('data') else []
    print('#%s attachmentsForURL: %d %s %s' % (n, len(nodes), [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes], r.get('errors', '')))
for k in ('KS-897', 'KS-896', 'KS-1277', 'KS-1133', 'KS-1229', 'KS-1140', 'KS-1110', 'KS-1158', 'KS-1086', 'KS-480', 'KS-1228', 'KS-1264', 'KS-1213', 'KS-979', 'KS-1155', 'KS-1118', 'KS-1263'):
    r = q('query($id:String!){issue(id:$id){identifier title state{name} archivedAt assignee{email}}}', {'id': k})
    i = (r.get('data') or {}).get('issue')
    print('%s %s' % (k, ('state=%s archivedAt=%s assignee=%s | %s' % (i['state']['name'], i['archivedAt'], (i.get('assignee') or {}).get('email'), i['title'][:100])) if i else r.get('errors')))
