#!/usr/bin/env python3
"""linear_reads.py — READ-ONLY Linear GraphQL queries (no mutation): KS-1238 (state, attachments, description + comment 77f4ec90 in full),
KS-1282 (state, text, attachments), KS-1230, KS-1215, KS-1248 and KS-1062 (includeArchived; the issue's OWN attachments, since attachmentsForURL
is blind to archived issues), attachmentsForURL for pull/1097..1099, and KS-1097..KS-1099's attachments (namespace trap). Key by NAME
(LINEAR_API_KEY) from the Secuura .env; never printed. Writes nothing (stdout). Derived from gatesets/2026-09-20_gate1092to1096/linear_reads.py."""
import json, re, urllib.request
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
assert not re.search(r'\bmutation\s*[({]', open(__file__).read()), 'a GraphQL write in this file'
def q1(query, v=None):
    r = urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': v or {}}).encode(),
        headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60)
    return json.load(r)
def q(query, v=None):
    for _ in range(3):
        try: return q1(query, v)
        except Exception as e: print('   (retry after', type(e).__name__, ')')
    return q1(query, v)
IQ = '''query($id:String!){ issue(id:$id){ identifier title state{name} archivedAt branchName updatedAt description
  attachments(includeArchived:true){ nodes{ url title metadata } } comments(first:100){ nodes{ id createdAt body } }
  history(first:50){ nodes{ createdAt fromState{name} toState{name} botActor{name} } } } }'''
for k in ('KS-1238', 'KS-1282', 'KS-1230', 'KS-1215', 'KS-1248', 'KS-1062'):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    atts = [(a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind')) for a in (d.get('attachments') or {}).get('nodes', [])]
    cs = sorted((d.get('comments') or {}).get('nodes', []), key=lambda c: c['createdAt'])
    hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
    print('%s | %s | state %s | archivedAt %s | branchName %s | attachments %s | comments %d (newest %s)' % (k, d.get('title'), (d.get('state') or {}).get('name'),
          d.get('archivedAt'), d.get('branchName'), atts, len(cs), (cs[-1]['id'][:8] + ' ' + cs[-1]['createdAt']) if cs else None))
    for h in sorted(hs, key=lambda h: h['createdAt'])[-4:]:
        print('   state change %s %s -> %s bot %s' % (h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name')))
    if k in ('KS-1238', 'KS-1282'):
        print('   --- DESCRIPTION %s ---\n%s\n   --- END ---' % (k, d.get('description')))
        for c in cs:
            if c['id'].startswith('77f4ec90') or k == 'KS-1282': print('   --- COMMENT %s %s ---\n%s\n   --- END ---' % (c['id'], c['createdAt'], c['body']))
for n in (1097, 1098, 1099):
    u = 'https://github.com/Secuura/Distributed_Secuura/pull/%d' % n
    d = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': u})
    print('attachmentsForURL pull/%d -> %s' % (n, [(x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in d['data']['attachmentsForURL']['nodes']]))
for n in (1097, 1098, 1099):
    d = q(IQ, {'id': 'KS-%d' % n}).get('data', {}).get('issue') or {}
    print('namespace KS-%d: state %s archivedAt %s attachments %s' % (n, (d.get('state') or {}).get('name'), d.get('archivedAt'), [a['url'].split('/')[-1] for a in (d.get('attachments') or {}).get('nodes', [])]))
