#!/usr/bin/env python3
"""linear_reads_gate20T2.py — READ-ONLY Linear GraphQL queries (the file asserts no `mutation`): the four own tickets (state, archivedAt, assignee,
branchName + the scanner, attachments, comment counts, the bot walk since 04:52Z), attachmentsForURL per PR (exactly its own key, contributes; KS-1081:
#1191 prior + #1205; KS-1139: #1192 prior + #1206), the seat's 41 ARCHIVED keys (boot/tickets_boot.json group, READ) archivedAt, the KS-547 content key,
controls (pull/1191 -> KS-1081; pull/1192 -> KS-1139; pull/9999 -> [] — a number no PR carries). Key by NAME from the Secuura .env, never printed.
Writes nothing (stdout). The gate19B script re-keyed (no Seat C lane this round)."""
import json, os, re, urllib.request, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round20T2 as R
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
print('date', now(), '| PR5_PENDING', R.PR5_PENDING)
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
IQ = '''query($id:String!){ issue(id:$id){ identifier title state{name} archivedAt branchName assignee{email}
  attachments(includeArchived:true){ nodes{ url metadata createdAt } } comments(first:100){ nodes{ id createdAt user{ name } botActor{ name } } }
  history(first:50){ nodes{ createdAt fromState{name} toState{name} botActor{name} actor{name} } } } }'''
def issue(k):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    atts = sorted((a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind'), (a.get('createdAt') or '')[:19]) for a in (d.get('attachments') or {}).get('nodes', []))
    return d, atts
def afu(n):
    a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/%d' % int(n)})
    return sorted((x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes'])
SCAN = re.compile(r'ks-\d+')
boot = json.load(open(R.SEAT_RECORD + 'boot/tickets_boot.json', encoding='utf-8'))
groups = {}
for k, v in boot.items(): groups.setdefault(v.get('group'), []).append(k)
print('the seat\'s boot/tickets_boot.json groups (READ):', {g: len(v) for g, v in groups.items()})
ARCH = sorted(next((v for g, v in groups.items() if g and 'arch' in str(g).lower()), []))
print('--- own tickets (tier 2)')
for k in R.OWN:
    d, atts = issue(k); prs = [p for p in R.PUSH if k in R.PRS[p]['keys']]
    walks = [(h['createdAt'][:19], (h.get('fromState') or {}).get('name'), (h.get('toState') or {}).get('name'), (h.get('botActor') or {}).get('name') or (h.get('actor') or {}).get('name')) for h in (d.get('history') or {}).get('nodes', []) if h.get('toState') and h['createdAt'] >= '2026-09-23T04:52']
    own_pr_present = all(any(a[0] == R.PRS[p]['n'] for a in atts) for p in prs if R.PRS[p]['n'])
    print('  %-8s state %s archivedAt %s assignee %s | attachments %s | own PR present %s | comments %d | title carries an archived key %s | branchName scanner %s (own %s) | walks since 04:52Z %s' % (
        k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email'), atts, own_pr_present, len((d.get('comments') or {}).get('nodes', [])), [a for a in ARCH + R.ARCHIVED_NAMED if a in (d.get('title') or '')] or 'NONE', SCAN.findall(d.get('branchName') or ''), k.lower(), walks))
    cm = [((c.get('createdAt') or '')[:19], (c.get('user') or {}).get('name') or (c.get('botActor') or {}).get('name')) for c in (d.get('comments') or {}).get('nodes', [])]
    print('           comments (createdAt, author — bodies never read): %s | since the round-20 brief 04:52Z: %d' % (sorted(cm), sum(1 for c in cm if c[0] >= '2026-09-23T04:52')))
print('--- attachmentsForURL per PR')
for p in R.PUSH:
    if not R.PRS[p]['n']: print('  PR %s PENDING' % p); continue
    a = afu(R.PRS[p]['n']); want = sorted((k, 'contributes') for k in R.PRS[p]['keys']); print('  pull/%s -> %s == own key contributes: %s' % (R.PRS[p]['n'], a, a == want))
for n, want in (('1191', 'KS-1081 (round 19\'s merged prior, expected)'), ('1192', 'KS-1139 (round 19\'s merged prior, expected)'), ('9999', '[] control (no such PR)')):
    print('  pull/%s -> %s (%s)' % (n, afu(n), want))
print('--- archived keys (the seat\'s boot group, %d): archivedAt set on all:' % len(ARCH), end=' ')
arch = [(k, (issue(k)[0].get('archivedAt') or None) is not None) for k in ARCH]; print(all(x[1] for x in arch), '| not archived:', [k for k, a in arch if not a] or 'NONE')
print('--- named archived content/excised keys:', [(k, (issue(k)[0].get('archivedAt') or None) is not None) for k in R.ARCHIVED_NAMED])
print('done', now())
