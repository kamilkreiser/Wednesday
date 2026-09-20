#!/usr/bin/env python3
"""linear_reads.py — READ-ONLY Linear GraphQL queries (no mutation) for the #1105 gate: KS-1175 (state, assignee, attachments incl. #1105 and
its linkKind, comment list, the facts comment 21af3285-0a40-490c-bfff-bc3466b6066b BY ID — its byte length only, the builder claims 4999/4999,
its @-mention count, its createdAt), KS-1284 (state, priority, createdAt/updatedAt, attachments, comments — the builder says untouched since
filing), KS-721 with includeArchived (archivedAt; attachments), KS-1250 (F5, the builder says Wednesday closed it), attachmentsForURL for
pull/1105, and KS-1105's own attachments (namespace trap: the PR number is another ticket's number too). Key by NAME (LINEAR_API_KEY) from the
Secuura .env; never printed. Writes nothing (stdout). Derived from gatesets/2026-09-20_gate1100to1101/linear_reads.py."""
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
IQ = '''query($id:String!){ issue(id:$id){ identifier title state{name} priorityLabel archivedAt branchName createdAt updatedAt assignee{name}
  attachments(includeArchived:true){ nodes{ url title metadata createdAt } } comments(first:100){ nodes{ id createdAt body } }
  history(first:50){ nodes{ createdAt fromState{name} toState{name} botActor{name} } } } }'''
FACTS = '21af3285-0a40-490c-bfff-bc3466b6066b'
for k in ('KS-1175', 'KS-1284', 'KS-721', 'KS-1250'):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    atts = [(a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind'), a.get('createdAt')) for a in (d.get('attachments') or {}).get('nodes', [])]
    cs = sorted((d.get('comments') or {}).get('nodes', []), key=lambda c: c['createdAt'])
    hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
    print('%s | %s | state %s | priority %s | assignee %s | archivedAt %s | createdAt %s updatedAt %s | branchName %s | attachments %s | comments %d (newest %s)' % (k, d.get('title'), (d.get('state') or {}).get('name'),
          d.get('priorityLabel'), (d.get('assignee') or {}).get('name'), d.get('archivedAt'), d.get('createdAt'), d.get('updatedAt'), d.get('branchName'), atts, len(cs), (cs[-1]['id'][:8] + ' ' + cs[-1]['createdAt']) if cs else None))
    for h in sorted(hs, key=lambda h: h['createdAt'])[-4:]:
        print('   state change %s %s -> %s bot %s' % (h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name')))
    for c in cs:
        body = c['body'] or ''
        print('   comment %s %s | chars %d | utf-8 bytes %d | @-mentions %d | lines %d | names #1105 %s | names e02d3ecb5 %s | "NOT DONE" %s | "seven" %s | "not deployed anywhere" %s | "both GETs" %s'
              % (c['id'], c['createdAt'], len(body), len(body.encode('utf-8')), len(re.findall(r'(?<![\w/])@[A-Za-z]', body)), body.count('\n') + 1, '#1105' in body, 'e02d3ecb5' in body, 'NOT DONE' in body, 'seven' in body.lower(), 'not deployed anywhere' in body, 'both GETs' in body))
        if c['id'] == FACTS:
            print('   ^ THE FACTS COMMENT BY ID (builder claims 4999/4999 read back byte-equal, 0 @mentions)')
u = 'https://github.com/Secuura/Distributed_Secuura/pull/1105'
d = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': u})
print('attachmentsForURL pull/1105 -> %s' % [(x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in d['data']['attachmentsForURL']['nodes']])
d = q(IQ, {'id': 'KS-1105'}).get('data', {}).get('issue') or {}
print('namespace KS-1105: exists %s | title %s | state %s archivedAt %s attachments %s' % (bool(d), (d.get('title') or '')[:80], (d.get('state') or {}).get('name'), d.get('archivedAt'), [a['url'].split('/')[-1] for a in (d.get('attachments') or {}).get('nodes', [])]))
