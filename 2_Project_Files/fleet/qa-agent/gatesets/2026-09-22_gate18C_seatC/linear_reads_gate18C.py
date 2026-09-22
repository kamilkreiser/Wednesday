#!/usr/bin/env python3
"""linear_reads_gate18C.py — READ-ONLY Linear GraphQL queries (no mutation) for the Seat C 18th six-PR batch gate: the SIX own tickets (KS-947,
KS-1123, KS-1192, KS-1231, KS-1246, KS-1257: state, assignee (KS-1246 / KS-1257 ASSIGNED to the board login at the seat's item 0 — assignment only),
archivedAt, branchName (KS-947's carries the ARCHIVED `ks-733` the seat EXCISED from the pushed ref; KS-1192's the hyphenless `ks871` KEPT), the
hyphenated-key scanner on each branchName, attachments incl. linkKind (KS-1123 also carries #1002 merged — expected), comment count, the last state
changes with the bot actor — the linear[bot] Backlog -> In Progress walks on PR open), attachmentsForURL for each PR (want exactly the PR's own key,
`contributes`), Seat B 18th's seven keys with their attachments (the four-condition attribution rule's subjects — the seat attributed 3 by NAME before
its HOLD; Seat B's later four opened after), the NAMESPACE TRAP tickets KS-1167..KS-1181 (the PR numbers of this round's window as ticket numbers),
the 30 archived keys with includeArchived (the READYs' block), the 22 live foreign/content keys (the READYs' block), KS-256 / KS-1201 (mentioned in
every body), KS-763 / KS-775 (#1036's), the rule-7 KS-485 / KS-772. Key by NAME (LINEAR_API_KEY) from the Secuura .env; never printed. Writes nothing
(stdout). Re-runnable. Derived from gatesets/2026-09-22_gate16C_seatC/linear_reads_gate16C.py."""
import glob, json, os, re, urllib.request, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round18C as R
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
  history(first:50){ nodes{ createdAt fromState{name} toState{name} fromAssignee{email} toAssignee{email} botActor{name} actor{name} } } } }'''
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatC18_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = int(m.group(3))
def issue(k):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    atts = [(a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind'), (a.get('createdAt') or '')[:19]) for a in (d.get('attachments') or {}).get('nodes', [])]
    return d, atts
def afu(n):
    a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/%d' % int(n)})
    return sorted((x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes'])
SCAN = re.compile(r'ks-\d+')
for p in R.PUSH:
    k = R.PRS[p]['key']
    d, atts = issue(k); cs = (d.get('comments') or {}).get('nodes', []); hs = (d.get('history') or {}).get('nodes', [])
    bn = d.get('branchName') or ''
    print('PR %-2s #%s %-7s %-10s | %s | state %s | priority %s | assignee %s | archivedAt %s | branchName %s (non-ascii %s; scanner ks-N not own %s; hyphenless file-name forms %s) | attachments %s | comments %d (READY: %s)' % (
        p, READY.get(p, '?'), k, R.PRS[p]['kind'], (d.get('title') or '')[:80], (d.get('state') or {}).get('name'), d.get('priorityLabel'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), d.get('archivedAt'), bn, [c for c in bn if ord(c) > 127] or 'NONE',
        [x for x in SCAN.findall(bn) if x != k.lower()] or 'NONE', [x for x in re.findall(r'ks\d{3,4}', bn)] or 'NONE', atts, len(cs), R.PRS[p]['comments']))
    for h in sorted([h for h in hs if h.get('toState') or h.get('toAssignee')], key=lambda h: h['createdAt'])[-4:]:
        if h.get('toState'): print('   state change %s %s -> %s bot %s actor %s' % (h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name'), (h.get('actor') or {}).get('name')))
        if h.get('toAssignee'): print('   assignee change %s %s -> %s actor %s' % (h['createdAt'], (h.get('fromAssignee') or {}).get('email'), (h.get('toAssignee') or {}).get('email'), (h.get('actor') or {}).get('name')))
    if p in READY:
        got = afu(READY[p]); print('   attachmentsForURL pull/%d -> %s | == want [%s] contributes: %s' % (READY[p], got, k, [x for x, _ in got] == [k] and all(lk == 'contributes' for _, lk in got)))
print('--- Seat B 18th keys (7) — attachments as they stand (the four-condition rule; THIS seat attributed KS-1118 / KS-1158 / KS-1265 by NAME before its HOLD; #1176 #1177 #1178 #1179 opened after it)')
for k in R.SEATB_KEYS:
    d, atts = issue(k); hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
    last = sorted(hs, key=lambda h: h['createdAt'])[-1:] if hs else []
    print('%s | state %s | archivedAt %s | assignee %s | attachments %s | last state change %s | branchName scanner (not own) %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), atts, [(h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name')) for h in last], [x for x in SCAN.findall(d.get('branchName') or '') if x != k.lower()] or 'NONE'))
for bn, bk, bh, bf in R.SEATB:
    print('   attachmentsForURL pull/%s -> %s (want [(%s, contributes)])' % (bn, afu(bn), bk))
print('--- NAMESPACE TRAP: tickets numbered like the PRs of this window (KS-1167..KS-1181)')
for n in range(1167, 1182):
    d, atts = issue('KS-%d' % n)
    print('KS-%d: exists %s | title %s | state %s archivedAt %s attachments %s' % (n, bool(d), (d.get('title') or '')[:70], (d.get('state') or {}).get('name'), d.get('archivedAt'), [x[0] for x in atts]))
print('--- ARCHIVED (30) + live foreign/content (22) + KS-256 / KS-1201 (every body) + KS-763 / KS-775 (#1036) + rule-7 KS-485 / KS-772')
for k in R.ARCHIVED + R.CONTENT_LIVE + ['KS-256', 'KS-1201', 'KS-763', 'KS-775', 'KS-485', 'KS-772']:
    d, atts = issue(k)
    print('%s | state %s | archivedAt %s | assignee %s | attachments %d %s | comments %d | updatedAt %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), len(atts), [x[0] for x in atts][:8], len((d.get('comments') or {}).get('nodes', [])), d.get('updatedAt')))
for u, lbl in (('pull/1036', 'merged; KS-763 + KS-775 (the base move)'), ('pull/1002', 'merged; KS-1123 earlier raise'), ('pull/1035', 'merged; KS-1204 (the last to touch verification.ts)'), ('pull/1045', 'merged; KS-1230 (the last to touch admin.ts)'), ('pull/1129', 'the foreign chore PR'), ('pull/1180', 'no such PR at the drafter read')):
    print('control attachmentsForURL %s (%s) -> %s' % (u, lbl, afu(u.split('/')[1])))
print('done', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
