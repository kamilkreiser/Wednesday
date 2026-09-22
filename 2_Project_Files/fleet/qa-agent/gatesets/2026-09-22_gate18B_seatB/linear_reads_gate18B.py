#!/usr/bin/env python3
"""linear_reads_gate18B.py — READ-ONLY Linear GraphQL queries (no mutation) for the Seat B 18th seven-PR batch gate: the SEVEN own tickets (KS-1118,
KS-1158, KS-1265, KS-1171, KS-811, KS-1188, KS-1181: state, assignee, archivedAt, branchName, attachments incl. linkKind, comment count, the last
state changes with the bot actor — the linear[bot] Backlog -> In Progress walks on KS-1265 / KS-1171 / KS-811), attachmentsForURL for each PR (want
exactly the PR's own key, `contributes`), the branchName scanner over the SEVEN Linear branchNames (the two excisions ks-999 / ks-727 the seat made;
the hyphenless file-name tokens), Seat C 18th's six keys with their attachments (the four-condition attribution rule's subjects), the NAMESPACE TRAP
tickets KS-1167..KS-1181 (the PR numbers of this round's window as ticket numbers), the 30 archived keys with includeArchived (the READYs' block),
the 19 live foreign/content keys (the READYs' block), the DEFERRED KS-1227, KS-795 (the ROUTECOLLAPSE cover cell's key), KS-999 (the live key excised
from KS-1188's branchName), KS-256 / KS-1201 (mentioned in every body), the rule-7 KS-485 / KS-772. Key by NAME (LINEAR_API_KEY) from the Secuura
.env; never printed. Writes nothing (stdout). Re-runnable. Derived from gatesets/2026-09-22_gate16B_seatB/linear_reads_gate16B.py."""
import glob, json, os, re, urllib.request, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round18B as R
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
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB18_ready*_pr*_*.md'))):
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
for p in R.PUSH:
    k = R.PRS[p]['key']
    d, atts = issue(k); cs = (d.get('comments') or {}).get('nodes', []); hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
    bn = d.get('branchName') or ''
    print('PR %s #%s %s | %s | state %s (boot %s; bot walk expected %s) | priority %s | assignee %s | archivedAt %s | branchName %s (non-ascii %s; hyphenated ks- keys %s; foreign hyphenless ks tokens %s) | attachments %s (want own #%s + prior %s) | comments %d (seat %d)' % (
        p, READY.get(p, '?'), k, (d.get('title') or '')[:80], (d.get('state') or {}).get('name'), R.PRS[p]['boot_state'], R.PRS[p]['bot_walk'], d.get('priorityLabel'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), d.get('archivedAt'), bn, [c for c in bn if ord(c) > 127] or 'NONE',
        re.findall(r'ks-\d+', bn), [x for x in re.findall(r'ks\d{3,4}', bn) if x != k.lower().replace('-', '')] or 'NONE', atts, READY.get(p), R.PRS[p]['prior_prs'], len(cs), R.PRS[p]['comments']))
    for h in sorted(hs, key=lambda h: h['createdAt'])[-3:]:
        print('   state change %s %s -> %s bot %s actor %s' % (h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name'), (h.get('actor') or {}).get('name')))
    if p in READY:
        got = afu(READY[p]); print('   attachmentsForURL pull/%d -> %s | == want [%s]: %s' % (READY[p], got, k, [x for x, _ in got] == [k] and all(lk == 'contributes' for _, lk in got)))
    if R.PRS[p]['prior_prs']:
        for pp in R.PRS[p]['prior_prs']: print('   the prior PR pull/%s -> attachmentsForURL %s' % (pp, afu(pp)))
print('--- Seat C 18th keys (6) — attachments as they stand (the four-condition rule: same key, head ref in the other seat namespace `-r16-…-1`, board login, addition only + the bot walk tolerated)')
for k in R.SEATC_KEYS:
    d, atts = issue(k); hs = [h for h in (d.get('history') or {}).get('nodes', []) if h.get('toState')]
    last = sorted(hs, key=lambda h: h['createdAt'])[-1:] if hs else []
    print('%s | state %s | archivedAt %s | assignee %s | attachments %s | last state change %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), atts, [(h['createdAt'], (h.get('fromState') or {}).get('name'), h['toState']['name'], (h.get('botActor') or {}).get('name')) for h in last]))
for cn, ck, ch, cf in R.SEATC:
    print('   attachmentsForURL pull/%s -> %s (want [(%s, contributes)])' % (cn, afu(cn), ck))
print('--- NAMESPACE TRAP: tickets numbered like the PRs of this window (KS-1167..KS-1181)')
for n in range(1167, 1182):
    d, atts = issue('KS-%d' % n)
    print('KS-%d: exists %s | title %s | state %s archivedAt %s attachments %s' % (n, bool(d), (d.get('title') or '')[:70], (d.get('state') or {}).get('name'), d.get('archivedAt'), [x[0] for x in atts]))
print('--- ARCHIVED (30) + live foreign/content (19) + the DEFERRED KS-1227 + KS-795 (the ks795 cover cell) + KS-999 (excised from KS-1188 branchName) + KS-256 / KS-1201 (every body) + rule-7 KS-485 / KS-772 + KS-1004 + KS-696 / KS-1287')
for k in R.ARCHIVED + R.CONTENT_LIVE + [R.DEFERRED, 'KS-795', 'KS-999', 'KS-256', 'KS-1201', 'KS-485', 'KS-772', 'KS-1004', 'KS-696', 'KS-1287']:
    d, atts = issue(k)
    print('%s | state %s | archivedAt %s | assignee %s | attachments %d %s | comments %d | updatedAt %s' % (k, (d.get('state') or {}).get('name'), d.get('archivedAt'), (d.get('assignee') or {}).get('email') or (d.get('assignee') or {}).get('name'), len(atts), [x[0] for x in atts][:8], len((d.get('comments') or {}).get('nodes', [])), d.get('updatedAt')))
for u, lbl in (('pull/1036', 'merged; KS-763 (the squash on develop)'), ('pull/1149', 'merged; KS-1118 (the 16th PR 2)'), ('pull/1153', 'merged; KS-1158 R3'), ('pull/1159', 'merged; KS-1181 F3'), ('pull/1163', 'merged; KS-1188 F1a/F1b/F2'), ('pull/1129', 'the foreign chore PR'), ('pull/1180', 'no such PR at the drafter read')):
    print('control attachmentsForURL %s (%s) -> %s' % (u, lbl, afu(u.split('/')[1])))
