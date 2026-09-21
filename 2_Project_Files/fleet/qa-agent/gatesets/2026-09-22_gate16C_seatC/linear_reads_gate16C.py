#!/usr/bin/env python3
"""linear_reads_gate16C.py — READ-ONLY Linear GraphQL queries (no mutation) for the Seat C 16th twelve-PR batch gate: the TWELVE own tickets (KS-864,
KS-1180, KS-1185, KS-1199, KS-1237, KS-855, KS-944, KS-1156, KS-1188, KS-1193, KS-1217, KS-910: state, assignee, archivedAt, branchName (with the
three LIVE foreign keys ks-1183 / ks-999 / ks-1018 the seat EXCISED from the pushed refs), attachments incl. linkKind, comment count, the last
state changes with the bot actor — the linear[bot] Backlog -> In Progress walks), the HELD KS-1123 (Backlog, #1002 only, untouched), attachmentsForURL
for each PR (want exactly the PR's own key, `contributes`), Seat B 16th's nine keys with their attachments (the four-condition attribution rule's
subjects — the seat attributed 8 by NAME), the NAMESPACE TRAP tickets KS-1147..KS-1167 (the PR numbers of this round's window as ticket numbers),
the 24 archived keys with includeArchived (the READYs' block), the 14 live foreign/content keys (the READYs' block), KS-256 / KS-1201 (mentioned in
every body), the rule-7 KS-485 / KS-772. Key by NAME (LINEAR_API_KEY) from the Secuura .env; never printed. Writes nothing (stdout). Re-runnable.
Derived from gatesets/2026-09-22_gate16B_seatB/linear_reads_gate16B.py."""
import glob, json, os, re, urllib.request, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round16C as R
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
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatC16_ready*_pr*_*.md'))):
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
for p in R.PUSH + ['2']:
    k = R.PRS[p]['key'] if p != '2' else R.HELD['key']
    d, atts = issue(k); cs = (d.get('comments') or {}).get('nodes', []); hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
    bn = d.get('branchName') or ''
    print('PR %-2s #%s %-7s | %s | state %s | priority %s | assignee %s | archivedAt %s | branchName %s (non-ascii %s; foreign ks- keys %s; hyphenless file-name forms %s) | attachments %s | comments %d (READY: %s)' % (
        p, READY.get(p, 'HELD' if p == '2' else '?'), k, (d.get('title') or '')[:80], (d.get('state') or {}).get('name'), d.get('priorityLabel'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), d.get('archivedAt'), bn, [c for c in bn if ord(c) > 127] or 'NONE',
        [x for x in re.findall(r'ks-\d{3,4}', bn) if x != k.lower()] or 'NONE', [x for x in re.findall(r'ks\d{3,4}', bn)] or 'NONE', atts, len(cs), R.PRS[p]['comments'] if p != '2' else '?'))
    for h in sorted(hs, key=lambda h: h['createdAt'])[-3:]:
        print('   state change %s %s -> %s bot %s actor %s' % (h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name'), (h.get('actor') or {}).get('name')))
    if p in READY:
        got = afu(READY[p]); print('   attachmentsForURL pull/%d -> %s | == want [%s] contributes: %s' % (READY[p], got, k, [x for x, _ in got] == [k] and all(lk == 'contributes' for _, lk in got)))
print('--- Seat B 16th keys (9) — attachments as they stand (the four-condition rule: same key, head ref in the other seat namespace, board login, addition only + the bot walk tolerated; the seat attributed 8 by NAME, KS-1171 held)')
for k in R.SEATB_KEYS:
    d, atts = issue(k); hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
    last = sorted(hs, key=lambda h: h['createdAt'])[-1:] if hs else []
    print('%s | state %s | archivedAt %s | assignee %s | attachments %s | last state change %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), atts, [(h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name')) for h in last]))
for bn, bk, bh, bf in R.SEATB:
    print('   attachmentsForURL pull/%s -> %s (want [(%s, contributes)])' % (bn, afu(bn), bk))
print('--- NAMESPACE TRAP: tickets numbered like the PRs of this window (KS-1147..KS-1167)')
for n in range(1147, 1168):
    d, atts = issue('KS-%d' % n)
    print('KS-%d: exists %s | title %s | state %s archivedAt %s attachments %s' % (n, bool(d), (d.get('title') or '')[:70], (d.get('state') or {}).get('name'), d.get('archivedAt'), [x[0] for x in atts]))
print('--- ARCHIVED (24) + live foreign/content (14) + KS-256 / KS-1201 (every body) + rule-7 KS-485 / KS-772 + KS-696 / KS-1287 / KS-1286')
for k in R.ARCHIVED + R.CONTENT_LIVE + ['KS-256', 'KS-1201', 'KS-485', 'KS-772', 'KS-696', 'KS-1287', 'KS-1286']:
    d, atts = issue(k)
    print('%s | state %s | archivedAt %s | assignee %s | attachments %d %s | comments %d | updatedAt %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), len(atts), [x[0] for x in atts][:8], len((d.get('comments') or {}).get('nodes', [])), d.get('updatedAt')))
for u, lbl in (('pull/1146', 'merged; KS-1156 (the 15th PR 10)'), ('pull/1029', 'merged; KS-1180 earlier raise'), ('pull/1009', 'merged; KS-864 earlier raise'), ('pull/1002', 'merged; KS-1123 earlier raise'), ('pull/1129', 'the foreign chore PR'), ('pull/1167', 'no such PR at the drafter read')):
    print('control attachmentsForURL %s (%s) -> %s' % (u, lbl, afu(u.split('/')[1])))
