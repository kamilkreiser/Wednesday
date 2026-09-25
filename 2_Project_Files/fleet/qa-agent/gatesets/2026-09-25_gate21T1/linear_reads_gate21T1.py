#!/usr/bin/env python3
"""linear_reads_gate21T1.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, never printed): for each of the
four PR URLs, attachmentsForURL (which issues carry it, and the linkKind metadata); for the four own keys + the two foreign keys #1217's body names
(KS-970, KS-974) + KS-562 / KS-1155 (carried wording tickets): state, archivedAt, assignee."""
import json, urllib.request, datetime
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate21T1', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
for n in ('1213', '1214', '1216', '1217'):
    url = 'https://github.com/Secuura/Distributed_Secuura/pull/' + n
    r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': url})
    nodes = (r.get('data') or {}).get('attachmentsForURL', {}).get('nodes', []) if r.get('data') else []
    print('#%s attachmentsForURL: %d %s %s' % (n, len(nodes), [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes], r.get('errors', '')))
for k in ('KS-530', 'KS-528', 'KS-975', 'KS-976', 'KS-970', 'KS-974', 'KS-562', 'KS-1155', 'KS-729'):
    r = q('query($id:String!){issue(id:$id){identifier title state{name} archivedAt assignee{email}}}', {'id': k})
    i = (r.get('data') or {}).get('issue')
    print('%s %s' % (k, ('state=%s archivedAt=%s assignee=%s | %s' % (i['state']['name'], i['archivedAt'], (i.get('assignee') or {}).get('email'), i['title'][:90])) if i else r.get('errors')))
