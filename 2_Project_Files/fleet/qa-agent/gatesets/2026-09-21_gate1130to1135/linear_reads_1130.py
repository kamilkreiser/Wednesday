#!/usr/bin/env python3
"""linear_reads_1130.py — READ-ONLY Linear GraphQL queries (no mutation) for the #1130-#113x batch gate: the SEVEN own tickets (KS-1273, KS-1135,
KS-958, KS-880, KS-887, KS-1236, KS-1006: state, assignee, archivedAt, branchName, attachments incl. linkKind, comment count, last state changes
with the bot actor), attachmentsForURL for each PR whose READY is captured (want {KS-1273} / {KS-1135} / {KS-958} / {KS-880} / {KS-887} /
{KS-1236, KS-1006}), the NAMESPACE TRAP tickets KS-1129..KS-1137, the SEVENTEEN archived keys with includeArchived, the live-but-foreign keys the
READYs list (26), the mentioned-only KS-256 / KS-1201, KS-961 (open PR #887's ticket — the PR-number trap), the rule-7 KS-485 / KS-772. Key by NAME
(LINEAR_API_KEY) from the Secuura .env; never printed. Writes nothing (stdout). Re-runnable. Derived from gatesets/2026-09-21_gate1119to1128/linear_reads.py."""
import glob, json, os, re, urllib.request, subprocess
G = os.path.dirname(os.path.abspath(__file__))
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
assert not re.search(r'\bmutation\s*[({]', open(__file__).read()), 'a GraphQL write in this file'
def q1(query, v=None):
    r = urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': v or {}}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60)
    return json.load(r)
def q(query, v=None):
    for _ in range(3):
        try: return q1(query, v)
        except Exception as e: print('   (retry after', type(e).__name__, ')')
    return q1(query, v)
IQ = '''query($id:String!){ issue(id:$id){ identifier title state{name} priorityLabel archivedAt branchName createdAt updatedAt assignee{name email}
  attachments(includeArchived:true){ nodes{ url title metadata createdAt } } comments(first:100){ nodes{ id createdAt } }
  history(first:50){ nodes{ createdAt fromState{name} toState{name} botActor{name} actor{name} } } } }'''
KEYS = {'1': ['KS-1273'], '2': ['KS-1135'], '6': ['KS-958'], '3': ['KS-880'], '5': ['KS-887'], '4': ['KS-1236', 'KS-1006']}
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB14_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(r'READY FOR QA \(Seat B 14th\): PR (\d) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = int(m.group(3))
def issue(k):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    atts = [(a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind'), (a.get('createdAt') or '')[:19]) for a in (d.get('attachments') or {}).get('nodes', [])]
    return d, atts
for p in ['1', '2', '6', '3', '5', '4']:
    for k in KEYS[p]:
        d, atts = issue(k); cs = (d.get('comments') or {}).get('nodes', []); hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
        print('PR %s #%s %s | %s | state %s | priority %s | assignee %s | archivedAt %s | branchName %s | attachments %s | comments %d' % (p, READY.get(p, '?'), k, (d.get('title') or '')[:80], (d.get('state') or {}).get('name'), d.get('priorityLabel'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), d.get('archivedAt'), d.get('branchName'), atts, len(cs)))
        for h in sorted(hs, key=lambda h: h['createdAt'])[-3:]:
            print('   state change %s %s -> %s bot %s actor %s' % (h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name'), (h.get('actor') or {}).get('name')))
    if p in READY:
        n = READY[p]; a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/%d' % n})
        got = sorted((x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes'])
        print('   attachmentsForURL pull/%d -> %s | == want %s: %s' % (n, got, sorted(KEYS[p]), sorted(k for k, _ in got) == sorted(KEYS[p]) and all(lk == 'contributes' for _, lk in got)))
print('--- NAMESPACE TRAP: tickets numbered like the PRs (KS-1129..KS-1137)')
for n in range(1129, 1138):
    d, atts = issue('KS-%d' % n)
    print('KS-%d: exists %s | title %s | state %s archivedAt %s attachments %s' % (n, bool(d), (d.get('title') or '')[:70], (d.get('state') or {}).get('name'), d.get('archivedAt'), [x[0] for x in atts]))
print('--- ARCHIVED (17) + live-but-foreign (26) + mentioned-only (KS-256, KS-1201) + KS-961 (open PR #887 is its) + rule-7 (KS-485, KS-772)')
for k in ('KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490',
          'KS-869', 'KS-1194', 'KS-1136', 'KS-1137', 'KS-957', 'KS-930', 'KS-969', 'KS-973', 'KS-1203', 'KS-1198', 'KS-1284', 'KS-1175', 'KS-1215', 'KS-753', 'KS-1232', 'KS-1223', 'KS-1234', 'KS-1283', 'KS-1244', 'KS-1275', 'KS-1279', 'KS-1272', 'KS-741', 'KS-1260', 'KS-1209', 'KS-953',
          'KS-256', 'KS-1201', 'KS-961', 'KS-485', 'KS-772'):
    d, atts = issue(k)
    print('%s | state %s | archivedAt %s | assignee %s | attachments %d %s | comments %d | updatedAt %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), len(atts), [x[0] for x in atts][:6], len((d.get('comments') or {}).get('nodes', [])), d.get('updatedAt')))
for u, lbl in (('pull/1118', 'merged; KS-1006 + KS-1236'), ('pull/1122', 'merged; KS-1273'), ('pull/1129', 'the foreign chore PR'), ('pull/1138', 'no such PR')):
    a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/' + u})
    print('control attachmentsForURL %s (%s) -> %s' % (u, lbl, [(x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes']]))
