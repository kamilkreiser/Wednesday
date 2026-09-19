#!/usr/bin/env python3
"""linear_reads.py — READ-ONLY Linear GraphQL queries (no mutation): KS-1238 (state, attachments, comment 60c1e1f7 in full + list of comment ids),
KS-1282 (state, text, attachments), KS-1230, KS-1215, KS-1062 / KS-739 (includeArchived), and attachmentsForURL for pull/1092..1096 and KS-1092..1096's
attachments (namespace trap). Key by NAME (LINEAR_API_KEY) from the Secuura .env; never printed. Writes nothing (stdout)."""
import json, urllib.request
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
def q(query, v=None):
    for _try in range(3):
        try: return q1(query, v)
        except Exception as e: print('   (retry after', type(e).__name__, ')')
    return q1(query, v)
def q1(query, v=None):
    r = urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': v or {}}).encode(),
        headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60)
    return json.load(r)
import re
assert not re.search(r'\bmutation\s*[({]', open(__file__).read()), 'a GraphQL write in this file'
IQ = '''query($id:String!){ issue(id:$id){ identifier title state{name} archivedAt branchName updatedAt description
  attachments(includeArchived:true){ nodes{ url title metadata } } comments(first:50){ nodes{ id createdAt body user{name} } } } }'''
for k in ('KS-1238', 'KS-1282', 'KS-1230', 'KS-1215', 'KS-1062', 'KS-739'):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    atts = [(a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind')) for a in (d.get('attachments') or {}).get('nodes', [])]
    cs = (d.get('comments') or {}).get('nodes', [])
    print('%s | %s | state %s | archivedAt %s | branchName %s | attachments %s | comments %d' % (k, d.get('title'), (d.get('state') or {}).get('name'), d.get('archivedAt'), d.get('branchName'), atts, len(cs)))
    for c in sorted(cs, key=lambda c: c['createdAt']): print('   comment %s %s %d chars' % (c['id'][:8], c['createdAt'], len(c['body'])))
    if k in ('KS-1238', 'KS-1282'):
        print('   --- DESCRIPTION %s ---\n%s\n   --- END ---' % (k, d.get('description')))
        for c in cs:
            if c['id'].startswith('60c1e1f7') or k == 'KS-1282': print('   --- COMMENT %s %s ---\n%s\n   --- END ---' % (c['id'], c['createdAt'], c['body']))
for n in range(1092, 1097):
    u = 'https://github.com/Secuura/Distributed_Secuura/pull/%d' % n
    d = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': u})
    print('attachmentsForURL pull/%d -> %s' % (n, [(x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in d['data']['attachmentsForURL']['nodes']]))
for n in range(1092, 1097):
    d = q(IQ, {'id': 'KS-%d' % n}).get('data', {}).get('issue') or {}
    print('namespace KS-%d: state %s attachments %s' % (n, (d.get('state') or {}).get('name'), [a['url'].split('/')[-1] for a in (d.get('attachments') or {}).get('nodes', [])]))
