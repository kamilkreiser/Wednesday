#!/usr/bin/env python3
"""linear_reads.py — READ-ONLY Linear GraphQL queries (no mutation) for the #1119-#1128 batch gate: the ELEVEN own tickets (state, assignee,
archivedAt, branchName, attachments incl. linkKind, comment count, the last state changes with the bot actor), attachmentsForURL for
pull/1119..1128 (want {KS-753} / {KS-1232} / {KS-957, KS-930} / {KS-1273} / {KS-1275} / {KS-880} / {KS-1223} / {KS-1283} / {KS-1244} / {KS-1234}),
the NAMESPACE TRAP tickets KS-1119..KS-1128, the THIRTEEN archived keys with includeArchived, the live-but-foreign keys the READYs list (27) plus the
two OUT candidates KS-887 / KS-958, the mentioned-only KS-256 / KS-1201, KS-1135 (the seat's nearest ticket for the leg-14 intermittent) and the
rule-7 KS-485 / KS-772. Key by NAME (LINEAR_API_KEY) from the Secuura .env; never printed. Writes nothing (stdout). Derived from
gatesets/2026-09-21_gate1112to1118/linear_reads.py."""
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
IQ = '''query($id:String!){ issue(id:$id){ identifier title state{name} priorityLabel archivedAt branchName createdAt updatedAt assignee{name email}
  attachments(includeArchived:true){ nodes{ url title metadata createdAt } } comments(first:100){ nodes{ id createdAt } }
  history(first:50){ nodes{ createdAt fromState{name} toState{name} botActor{name} actor{name} } } } }'''
PRS = [(1119, ['KS-753']), (1120, ['KS-1232']), (1121, ['KS-957', 'KS-930']), (1122, ['KS-1273']), (1123, ['KS-1275']), (1124, ['KS-880']), (1125, ['KS-1223']), (1126, ['KS-1283']), (1127, ['KS-1244']), (1128, ['KS-1234'])]
for n, keys in PRS:
    for k in keys:
        d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
        atts = [(a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind'), a.get('createdAt')) for a in (d.get('attachments') or {}).get('nodes', [])]
        cs = (d.get('comments') or {}).get('nodes', [])
        hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
        print('#%d %s | %s | state %s | priority %s | assignee %s | archivedAt %s | branchName %s | attachments %s | comments %d' % (n, k, (d.get('title') or '')[:80], (d.get('state') or {}).get('name'),
              d.get('priorityLabel'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), d.get('archivedAt'), d.get('branchName'), atts, len(cs)))
        for h in sorted(hs, key=lambda h: h['createdAt'])[-3:]:
            print('   state change %s %s -> %s bot %s actor %s' % (h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name'), (h.get('actor') or {}).get('name')))
    u = 'https://github.com/Secuura/Distributed_Secuura/pull/%d' % n
    a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': u})
    got = sorted((x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes'])
    print('   attachmentsForURL pull/%d -> %s | == want %s: %s' % (n, got, sorted(keys), sorted(k for k, _ in got) == sorted(keys) and all(lk == 'contributes' for _, lk in got)))
print('--- NAMESPACE TRAP: tickets numbered like the PRs')
for n in range(1119, 1129):
    d = q(IQ, {'id': 'KS-%d' % n}).get('data', {}).get('issue') or {}
    print('KS-%d: exists %s | title %s | state %s archivedAt %s attachments %s' % (n, bool(d), (d.get('title') or '')[:70], (d.get('state') or {}).get('name'), d.get('archivedAt'), [a['url'].split('/')[-1] for a in (d.get('attachments') or {}).get('nodes', [])]))
print('--- ARCHIVED (thirteen) + live-but-foreign (27) + OUT candidates (KS-887, KS-958) + mentioned-only (KS-256, KS-1201) + KS-1135 + rule-7 (KS-485, KS-772)')
for k in ('KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062',
          'KS-869', 'KS-740', 'KS-1136', 'KS-444', 'KS-921', 'KS-490', 'KS-1137', 'KS-1072', 'KS-815', 'KS-1215', 'KS-1203', 'KS-1198', 'KS-1284', 'KS-1175', 'KS-1006', 'KS-1236', 'KS-570', 'KS-719', 'KS-1194', 'KS-1279', 'KS-1272', 'KS-741', 'KS-1260', 'KS-1209', 'KS-953', 'KS-794', 'KS-1133',
          'KS-887', 'KS-958', 'KS-256', 'KS-1201', 'KS-1135', 'KS-485', 'KS-772'):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    print('%s | state %s | archivedAt %s | assignee %s | attachments %d %s | comments %d | updatedAt %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), len((d.get('attachments') or {}).get('nodes', [])), [a['url'].split('/')[-1] for a in (d.get('attachments') or {}).get('nodes', [])][:6], len((d.get('comments') or {}).get('nodes', [])), d.get('updatedAt')))
a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/1118'})
print('control attachmentsForURL pull/1118 (merged; KS-1006 + KS-1236) -> %s' % [(x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes']])
a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/1129'})
print('control attachmentsForURL pull/1129 (no such PR) -> %s' % [(x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes']])
