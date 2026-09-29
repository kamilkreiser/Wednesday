#!/usr/bin/env python3
"""gh_read_gate42.py — READ-ONLY GitHub reads (REST GET only) for the gate42 kit (the directory this script lives in; kit.json beside it). GH_TOKEN by
NAME from the Secuura .env, never printed. Per PR: head / state / mergeable / base (ref AND sha — gate42 declares NO stack; #1339 branches from develop
8af6ab821600 itself; round 2 is a second commit on the same branch) / draft / title (length, ASCII, the MG-11 squash-subject length `<title> (#NNNN)`) / body (KS keys, Refs lines, closing-word+key count,
foreign keys, markers; saved as gh_body_<n>.md) / files / commits (each with its parents) / compare against its BASE (develop) / issue comments
(gh_comments_<n>.md). Then the census: every OPEN PR, the WIDEN census (kit.json widen_rx: the kit's keys in a title; widen_branch_rx: the
`-b43-<n>` segment Seat B 44th adopted AND its own `-b44-<n>`), every other open PR (kit.json `inflight`: state and CURRENT head — they move), and the
RELATED PRs by state: #1338 (MERGED rows: its squash 8af6ab821600 IS develop, #1339's base), and the DECLARED open-PR overlaps (kit.json
dead_open_declared: state, head, title). ROUND 2: every commit is listed with its parents; the round-1 head (kit.json round1_head) must be the round-2
commit's parent, and compare(round-1 head...head) lists the round-2 files. Shape copied from gate41's gh_read (the lineage runs back through the
predecessor kits), re-keyed for gate42 (the widen census by title AND branch, every spelling of the b43 AND b44 tokens with a planted control).
Writes only beside this script. Usage: gh_read_gate42.py <develop>"""
import json, os, re, sys, urllib.request, urllib.error, datetime, time
G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3: raise
            print('  (GitHub %d on %s — retry %d)' % (e.code, u, i + 1)); time.sleep(10)
DEV = sys.argv[1]
ST = K.get('stacks', {})
print('gh_read_gate42 (%s)' % K['kit'], datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'current develop', DEV)
HEADS = {}
for n in sorted(K['prs']):
    own = set(K['prs'][n]['keys'])
    p = get('pulls/' + n); HEADS[n] = p['head']['sha']
    print('=== #%s head %s state %s merged %s mergeable %s mergeable_state %s draft %s base %s base.sha %s head.ref %s' % (n, p['head']['sha'], p['state'], p['merged'], p.get('mergeable'), p.get('mergeable_state'), p['draft'], p['base']['ref'], p['base']['sha'], p['head']['ref']))
    t = p['title']; b = p['body'] or ''
    subj = '%s (#%s)' % (t, n)
    print('title (%d chars, ascii %s; squash subject `<title> (#%s)` = %d chars, MG-11 <= 92: %s): %s' % (len(t), t.isascii(), n, len(subj), len(subj) <= 92, t))
    keys = sorted(set(re.findall(r'KS-\d+', b)))
    print('body %d chars; KS keys %s; Refs lines %s; closing-word+key %d %s; foreign hyphenated keys %s' % (len(b), keys, re.findall(r'(?im)^\s*Refs\b.*$', b),
          len(re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+', b)), re.findall(r'(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+KS-\d+', b), sorted(set(keys) - own)))
    print('body markers: Test Evidence %s | NOT covered %s | red proof %s | stacked/retarget named %s | develop 8af6ab82 named %s | a card / ruling named %s | the prior gate (gate 41 / gate 42) named %s | round 2 named %s | N-1339-1 named %s | N-1339-2 named %s | KS 1379 / KS-1379 named %s | tsc named %s | jest named %s' % (
        bool(re.search(r'(?i)test evidence', b)), bool(re.search(r'(?i)not\s+covered', b)), bool(re.search(r'(?i)red[- ]proof', b)), bool(re.search(r'(?i)stack|retarget', b)), '8af6ab82' in b, bool(re.search(r'(?i)card|rul(ed|ing)', b)), bool(re.search(r'(?i)gate ?(41|42)', b)), bool(re.search(r'(?i)round 2', b)), 'N-1339-1' in b, 'N-1339-2' in b, bool(re.search(r'KS[- ]1379', b)), bool(re.search(r'\btsc\b', b)), bool(re.search(r'(?i)\bjest\b', b))))
    open(os.path.join(G, 'gh_body_%s.md' % n), 'w', encoding='utf-8').write('#%s %s\nhead %s\n\n%s\n' % (n, t, p['head']['sha'], b))
    f = get('pulls/%s/files?per_page=100' % n); print('files', len(f))
    for x in f: print('  %-8s +%d -%d %s %s' % (x['status'], x['additions'], x['deletions'], x['sha'], x['filename']))
    cs = get('pulls/%s/commits?per_page=100' % n); print('commits', len(cs))
    for c in cs: print('  %s parent %s | %s' % (c['sha'], ','.join(q['sha'][:12] for q in c['parents']), c['commit']['message'].splitlines()[0]))
    R1 = K.get('round1_head')
    if R1:
        c1 = get('compare/%s...%s' % (R1, p['head']['sha']))
        print('compare ROUND-1 head %s...head (round 2 only): status %s merge_base %s ahead %d behind %d files %d %s' % (R1[:12], c1['status'], c1['merge_base_commit']['sha'][:12], c1['ahead_by'], c1['behind_by'], len(c1['files']), [(x['filename'], x['additions'], x['deletions']) for x in c1['files']]))
    base = HEADS.get(ST[n]) if n in ST else DEV
    c = get('compare/%s...%s' % (base, p['head']['sha']))
    print('compare %s...head (%s): status %s merge_base %s ahead %d behind %d files %d %s' % (base, 'the STACKED parent #%s head' % ST[n] if n in ST else 'CURRENT develop', c['status'], c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c['files']), sorted(x['filename'] for x in c['files'])))
    if n in ST:
        c2 = get('compare/%s...%s' % (DEV, p['head']['sha']))
        print('compare CURRENT develop...head (stacked: carries the parent too): merge_base %s ahead %d behind %d files %s' % (c2['merge_base_commit']['sha'], c2['ahead_by'], c2['behind_by'], sorted(x['filename'] for x in c2['files'])))
    com = get('issues/%s/comments?per_page=100' % n)
    with open(os.path.join(G, 'gh_comments_%s.md' % n), 'w', encoding='utf-8') as fh:
        for x in com: fh.write('--- comment %s by %s at %s\n%s\n' % (x['id'], x['user']['login'], x['created_at'], x['body']))
    print('issue comments', len(com), [(x['user']['login'], x['created_at']) for x in com])
op = get('pulls?state=open&per_page=100&sort=created&direction=desc')
print('=== census: %d OPEN PRs; newest twenty: %s' % (len(op), [(x['number'], x['head']['ref'][:70], x['created_at']) for x in op[:20]]))
r = [x for x in op if str(x['number']) not in K['this_batch']]
print('  EVERY OTHER OPEN PR (the in-flight census: number, head, branch, base, created): %s' % ([(x['number'], x['head']['sha'][:12], x['head']['ref'], x['base']['ref'], x['created_at']) for x in r] or 'NONE'))
print('  open PRs in NEITHER this kit NOR kit.json inflight: %s' % ([x['number'] for x in r if str(x['number']) not in K['inflight']] or 'NONE'))
print('  open PRs whose BASE is not develop: %s' % ([(x['number'], x['base']['ref']) for x in op if x['base']['ref'] != 'develop'] or 'NONE'))
for n in K['inflight']:
    p = get('pulls/' + n)
    print('  in-flight #%s: state %s merged %s head %s updated_at %s (its head MAY move; not in this batch)' % (n, p['state'], p['merged'], p['head']['sha'], p.get('updated_at')))
WID = [(x['number'], x['head']['sha'], x['head']['ref'], x['user']['login'], x['title']) for x in op if re.match(K['widen_rx'], x['title']) or re.search(K['widen_branch_rx'], x['head']['ref'])]
print('  WIDEN census (open PRs titled with one of the kit keys, or on a branch matching %r, any author): %s' % (K['widen_branch_rx'], WID or 'NONE'))
# every spelling of the b43 token (adopted) AND Seat B 44th's b44 token (STANDING_LINES 2026-09-27): the branch segment, the seat-record prefix, a ref namespace; each with a planted control
SPELL = {r'-b43-': 'feature/ks-9999-x-b43-9', r's-b43-': 'worktrees/s-b43-ks9999', r'seatb43': 'refs/seatb43/pr9999', r'\bb43\b': 'refs/b43/pr9999',
         r'-b44-': 'feature/ks-9999-x-b44-9', r's-b44-': 'worktrees/s-b44-ks9999', r'seatb44': 'refs/seatb44/pr9999', r'\bb44\b': 'refs/b44/pr9999'}
for rx, plant in SPELL.items():
    hits = [(x['number'], x['head']['ref']) for x in op if re.search(rx, x['head']['ref'], re.I) and str(x['number']) not in K['this_batch']]
    print('  namespace spelling %r: open PRs OUTSIDE the kit whose branch carries it %s | CONTROL fires on the planted %r: %s' % (rx, hits or 'NONE', plant, bool(re.search(rx, plant, re.I))))
for n, want in [('1338', 'MERGED')] + [(d, 'OPEN') for d in sorted(K.get('dead_open_declared', {}))]:
    p = get('pulls/' + n)
    got = 'OPEN' if p['state'] == 'open' else ('MERGED' if p['merged'] else 'CLOSED-UNMERGED')
    print('  RELATED #%s: want %s got %s (%s) | state %s merged %s head %s merge_commit %s closed_at %s | %s' % (n, want, got, 'as expected' if got == want else 'DIFFERS', p['state'], p['merged'], p['head']['sha'], p.get('merge_commit_sha'), p.get('closed_at'), p['title'][:90]))
print('  WIDEN rows NOT in this kit: %s' % ([w for w in WID if str(w[0]) not in K['this_batch']] or 'NONE'))
