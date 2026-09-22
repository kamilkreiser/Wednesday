#!/usr/bin/env python3
"""linear_reads_gate19C.py — READ-ONLY Linear GraphQL queries (the file asserts no `mutation`): the eleven own tickets (state, archivedAt, branchName
+ the scanner for excised archived keys ks-666 / ks-754 / ks-926, attachments, comment counts, the bot walk), attachmentsForURL per PR (#1187 TWO
keys; KS-1047: #1189 closed + #1190 open; KS-1097: #1140 merged + three open), the 37 archived keys' archivedAt, the 14 content keys' states, Seat B's
nine keys (attachments by NAME), controls (pull/1189 -> KS-1047; pull/1140 -> KS-1097; pull/1199 -> []). Key by NAME from the Secuura .env, never
printed. Writes nothing (stdout)."""
import glob, json, os, re, urllib.request, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round19C as R
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
IQ = '''query($id:String!){ issue(id:$id){ identifier title state{name} archivedAt branchName assignee{email}
  attachments(includeArchived:true){ nodes{ url metadata createdAt } } comments(first:100){ nodes{ id } }
  history(first:50){ nodes{ createdAt fromState{name} toState{name} botActor{name} actor{name} } } } }'''
def issue(k):
    d = q(IQ, {'id': k}).get('data', {}).get('issue') or {}
    atts = sorted((a['url'].split('/')[-1], (a.get('metadata') or {}).get('linkKind'), (a.get('createdAt') or '')[:19]) for a in (d.get('attachments') or {}).get('nodes', []))
    return d, atts
def afu(n):
    a = q('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{ identifier } metadata } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/%d' % int(n)})
    return sorted((x['issue']['identifier'], (x.get('metadata') or {}).get('linkKind')) for x in a['data']['attachmentsForURL']['nodes'])
SCAN = re.compile(r'ks-\d+')
print('--- own tickets')
for k in R.OWN:
    d, atts = issue(k); prs = [p for p in R.PUSH if k in R.PRS[p]['keys']]
    walks = [(h['createdAt'][:19], (h.get('fromState') or {}).get('name'), (h.get('toState') or {}).get('name'), (h.get('botActor') or {}).get('name') or (h.get('actor') or {}).get('name')) for h in (d.get('history') or {}).get('nodes', []) if h.get('toState') and h['createdAt'] >= '2026-09-22T04:00']
    print('  %-8s state %s archivedAt %s assignee %s | attachments %s | own PR(s) present %s | comments %d | branchName scanner %s (own %s; excised archived %s) | walks since 04:00Z %s' % (
        k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email'), atts, all(any(a[0] == R.PRS[p]['n'] for a in atts) for p in prs), len((d.get('comments') or {}).get('nodes', [])), SCAN.findall(d.get('branchName') or ''), k.lower(), [x for x in SCAN.findall(d.get('branchName') or '') if x.upper() in R.ARCHIVED] or 'NONE', walks))
print('--- attachmentsForURL per PR')
for p in R.PUSH:
    a = afu(R.PRS[p]['n']); want = sorted((k, 'contributes') for k in R.PRS[p]['keys']); print('  pull/%s -> %s == own keys contributes: %s' % (R.PRS[p]['n'], a, a == want))
for n, want in (('1189', 'KS-1047 (the CLOSED twin, expected)'), ('1140', 'KS-1097 (merged, expected)'), ('1199', '[] control'), ('1036', 'KS-763/KS-775 control')):
    print('  pull/%s -> %s (%s)' % (n, afu(n), want))
print('--- archived keys (37): archivedAt set on all:', end=' ')
arch = [(k, (issue(k)[0].get('archivedAt') or None) is not None) for k in R.ARCHIVED]; print(all(x[1] for x in arch), '| not archived:', [k for k, a in arch if not a] or 'NONE')
print('--- content / foreign keys (14):', [(k, (issue(k)[0].get('state') or {}).get('name')) for k in R.CONTENT_LIVE])
print('--- Seat B nine keys (read only):', [(k, (issue(k)[0].get('state') or {}).get('name'), [a[0] for a in issue(k)[1]]) for k in R.SEATB_KEYS])
print('done', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
