#!/usr/bin/env python3
"""linear_reads_gate15.py — READ-ONLY Linear GraphQL queries (no mutation) for the Seat B 15th ten-PR batch gate: the TWELVE own tickets (KS-1035,
KS-1036, KS-1037, KS-1049, KS-1045, KS-1097, KS-890, KS-1140, KS-1152, KS-979, KS-1120, KS-1156: state, assignee, archivedAt, branchName,
attachments incl. linkKind, comment count, the last state changes with the bot actor), attachmentsForURL for each PR whose READY is captured
(want exactly the PR's own key set, every link `contributes`), the NAMESPACE TRAP tickets KS-1136..KS-1147 (the PR numbers of this round as
ticket numbers), the NINETEEN archived keys with includeArchived (the standing 17 + KS-597 + KS-727), the CONTENT keys the touched files name
(KS-764 / KS-879 / KS-1020 / KS-835 — the seat's F3: archived; KS-869 / KS-601 live), the three DROPPED (KS-1118 / KS-1158 / KS-1181), the
14th's seven (still In Progress), KS-961 (open PR #887's) / KS-763 (open PR #1036's — the PR-number trap), the rule-7 KS-485 / KS-772, and
KS-696 (the seat's F7). Key by NAME (LINEAR_API_KEY) from the Secuura .env; never printed. Writes nothing (stdout). Re-runnable. Derived from
gatesets/2026-09-21_gate1130to1135/linear_reads_1130.py."""
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
KEYS = {'1': ['KS-1035', 'KS-1036'], '2': ['KS-1037', 'KS-1049'], '3': ['KS-1045'], '4': ['KS-1097'], '5': ['KS-890'], '6': ['KS-1140'], '7': ['KS-1152'], '8': ['KS-979'], '9': ['KS-1120'], '10': ['KS-1156']}
PUSH = [str(i) for i in range(1, 11)]
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB15_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(r'READY FOR QA \(Seat B 15th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = int(m.group(3))
def issue(k):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    atts = [(a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind'), (a.get('createdAt') or '')[:19]) for a in (d.get('attachments') or {}).get('nodes', [])]
    return d, atts
for p in PUSH:
    for k in KEYS[p]:
        d, atts = issue(k); cs = (d.get('comments') or {}).get('nodes', []); hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
        bn = d.get('branchName') or ''
        print('PR %s #%s %s | %s | state %s | priority %s | assignee %s | archivedAt %s | branchName %s (non-ascii %s; foreign ks- keys %s) | attachments %s | comments %d' % (p, READY.get(p, '?'), k, (d.get('title') or '')[:80], (d.get('state') or {}).get('name'), d.get('priorityLabel'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), d.get('archivedAt'), bn, [c for c in bn if ord(c) > 127] or 'NONE', [x for x in re.findall(r'ks-?\d{3,4}', bn) if x.replace('ks-', 'ks') != k.lower().replace('-', '')] or 'NONE', atts, len(cs)))
        for h in sorted(hs, key=lambda h: h['createdAt'])[-3:]:
            print('   state change %s %s -> %s bot %s actor %s' % (h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name'), (h.get('actor') or {}).get('name')))
    if p in READY:
        n = READY[p]; a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/%d' % n})
        got = sorted((x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes'])
        print('   attachmentsForURL pull/%d -> %s | == want %s: %s' % (n, got, sorted(KEYS[p]), sorted(k for k, _ in got) == sorted(KEYS[p]) and all(lk == 'contributes' for _, lk in got)))
print('--- NAMESPACE TRAP: tickets numbered like the PRs (KS-1136..KS-1147)')
for n in range(1136, 1148):
    d, atts = issue('KS-%d' % n)
    print('KS-%d: exists %s | title %s | state %s archivedAt %s attachments %s' % (n, bool(d), (d.get('title') or '')[:70], (d.get('state') or {}).get('name'), d.get('archivedAt'), [x[0] for x in atts]))
print('--- ARCHIVED (19) + CONTENT keys (7) + DROPPED (3) + the 14th seven + KS-961 / KS-763 (PR-number traps) + rule-7 (KS-485, KS-772) + KS-696 (F7) + KS-256 / KS-1201 (mentioned in every body)')
for k in ('KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490', 'KS-597', 'KS-727',
          'KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-869', 'KS-601', 'KS-1044',
          'KS-1118', 'KS-1158', 'KS-1181',
          'KS-1273', 'KS-1135', 'KS-958', 'KS-880', 'KS-887', 'KS-1236', 'KS-1006',
          'KS-961', 'KS-763', 'KS-485', 'KS-772', 'KS-696', 'KS-256', 'KS-1201', 'KS-973'):
    d, atts = issue(k)
    print('%s | state %s | archivedAt %s | assignee %s | attachments %d %s | comments %d | updatedAt %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), len(atts), [x[0] for x in atts][:8], len((d.get('comments') or {}).get('nodes', [])), d.get('updatedAt')))
for u, lbl in (('pull/1135', 'merged; KS-1236 + KS-1006'), ('pull/1130', 'merged; KS-1273'), ('pull/1129', 'the foreign chore PR'), ('pull/1036', 'OPEN — KS-763 (the PR-number trap)'), ('pull/1148', 'no such PR')):
    a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/' + u})
    print('control attachmentsForURL %s (%s) -> %s' % (u, lbl, [(x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes']]))
