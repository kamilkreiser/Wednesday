#!/usr/bin/env python3
"""linear_reads_gate25.py — READ-ONLY Linear GraphQL (queries only; LINEAR_API_KEY by NAME from the Secuura .env, sent without "Bearer", never
printed) for ONE gate25 kit (kit.json beside this script): attachmentsForURL for each PR — the LINK KIND per ticket (`closes` where the PR says it
does not close = the MAGIC-WORD-CLOSES class) — and each PR's own tickets (state, description saved as linear_<KEY>.md, comment count + newest
comment ids/times), plus the kit's extra keys (state only). Writes only beside this script. Usage: linear_reads_gate25.py"""
import json, os, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, var):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': var}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_reads_gate25 (%s)' % K['kit'], datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
SAVE = []
for n in sorted(K['prs']):
    r = q('query($u:String!){attachmentsForURL(url:$u){nodes{id title metadata issue{identifier state{name}}}}}', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/' + n})
    nodes = ((r.get('data') or {}).get('attachmentsForURL') or {}).get('nodes', [])
    kinds = [(x['issue']['identifier'], x['issue']['state']['name'], (x.get('metadata') or {}).get('linkKind')) for x in nodes]
    own = K['prs'][n]['keys']
    closes = [k for k, s, lk in kinds if lk == 'closes']
    missing = sorted(set(own) - {k for k, s, lk in kinds})
    print('#%s attachmentsForURL: %d %s %s | own keys %s | linked as `closes`: %s | own key with NO link: %s' % (n, len(nodes), kinds, r.get('errors', ''), own, closes or 'none', missing or 'none'))
    SAVE += own
for k in SAVE + K.get('extra_keys', []):
    r = q('query($id:String!){issue(id:$id){identifier title description state{name} archivedAt comments{nodes{id createdAt}}}}', {'id': k})
    i = (r.get('data') or {}).get('issue')
    if not i:
        print(k, r.get('errors')); continue
    cm = sorted(i['comments']['nodes'], key=lambda x: x['createdAt'])
    print('%s state=%s archivedAt=%s comments=%d newest=%s | %s' % (k, i['state']['name'], i['archivedAt'], len(cm), [(x['id'], x['createdAt']) for x in cm[-2:]], i['title'][:140]))
    if k in SAVE:
        open(os.path.join(G, 'linear_%s.md' % k), 'w', encoding='utf-8').write('%s %s\nstate %s\n\n%s\n' % (k, i['title'], i['state']['name'], i.get('description') or ''))
