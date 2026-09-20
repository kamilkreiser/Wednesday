#!/usr/bin/env python3
"""linear_reads.py — READ-ONLY Linear GraphQL queries (no mutation) for the #1106-#1111 batch gate: the six tickets (state, assignee, archivedAt,
branchName, attachments incl. linkKind, comment count, the last state changes with the bot actor), attachmentsForURL for pull/1106..1111, the
NAMESPACE TRAP tickets KS-1106..KS-1111 (the PR numbers are other tickets' numbers), the ten ARCHIVED keys with includeArchived (state,
archivedAt, attachment count) and the four live-but-foreign keys. Key by NAME (LINEAR_API_KEY) from the Secuura .env; never printed. Writes
nothing (stdout). Derived from gatesets/2026-09-20_gate1105/linear_reads.py."""
import json, re, urllib.request, subprocess
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
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
  attachments(includeArchived:true){ nodes{ url title metadata createdAt } } comments(first:100){ nodes{ id createdAt } }
  history(first:50){ nodes{ createdAt fromState{name} toState{name} botActor{name} actor{name} } } } }'''
PRS = [(1106, 'KS-1232'), (1107, 'KS-753'), (1108, 'KS-1234'), (1109, 'KS-1279'), (1110, 'KS-880'), (1111, 'KS-1223')]
for n, k in PRS:
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    atts = [(a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind'), a.get('createdAt')) for a in (d.get('attachments') or {}).get('nodes', [])]
    cs = (d.get('comments') or {}).get('nodes', [])
    hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
    print('#%d %s | %s | state %s | priority %s | assignee %s | archivedAt %s | branchName %s | attachments %s | comments %d' % (n, k, (d.get('title') or '')[:80], (d.get('state') or {}).get('name'),
          d.get('priorityLabel'), (d.get('assignee') or {}).get('name'), d.get('archivedAt'), d.get('branchName'), atts, len(cs)))
    for h in sorted(hs, key=lambda h: h['createdAt'])[-3:]:
        print('   state change %s %s -> %s bot %s actor %s' % (h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name'), (h.get('actor') or {}).get('name')))
    u = 'https://github.com/Secuura/Distributed_Secuura/pull/%d' % n
    a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': u})
    print('   attachmentsForURL pull/%d -> %s' % (n, [(x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes']]))
print('--- NAMESPACE TRAP: tickets numbered like the PRs')
for n in range(1106, 1112):
    d = q(IQ, {'id': 'KS-%d' % n}).get('data', {}).get('issue') or {}
    print('KS-%d: exists %s | title %s | state %s archivedAt %s attachments %s' % (n, bool(d), (d.get('title') or '')[:70], (d.get('state') or {}).get('name'), d.get('archivedAt'), [a['url'].split('/')[-1] for a in (d.get('attachments') or {}).get('nodes', [])]))
print('--- ARCHIVED (ten) + live-but-foreign (four) + mentioned-only')
for k in ('KS-1062', 'KS-1238', 'KS-1282', 'KS-501', 'KS-480', 'KS-740', 'KS-1041', 'KS-523', 'KS-1046', 'KS-781', 'KS-1260', 'KS-1209', 'KS-953', 'KS-741', 'KS-256', 'KS-1201'):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    print('%s | state %s | archivedAt %s | attachments %d %s | comments %d | updatedAt %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), len((d.get('attachments') or {}).get('nodes', [])), [a['url'].split('/')[-1] for a in (d.get('attachments') or {}).get('nodes', [])][:6], len((d.get('comments') or {}).get('nodes', [])), d.get('updatedAt')))
# control: attachmentsForURL on a live merged PR (#1104 KS-1272, live In Progress) must be non-empty
a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/1104'})
print('control attachmentsForURL pull/1104 (live KS-1272) -> %s' % [(x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes']])
