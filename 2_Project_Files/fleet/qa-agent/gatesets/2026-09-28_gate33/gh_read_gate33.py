#!/usr/bin/env python3
"""gh_read_gate33.py — READ-ONLY GitHub reads (REST GET only) for the gate33 kit (the directory this script lives in; kit.json beside it). GH_TOKEN by
NAME from the Secuura .env, never printed. Per PR: head / state / mergeable / base (ref AND sha — gate33 declares NO stack; #1310 branches from a24db57e65c9,
the other five from the OLDER develop 94c9c7aa9be7) / draft / title (length, ASCII, the MG-11 squash-subject length `<title> (#NNNN)`) / body (KS keys,
Refs lines, closing-word+key count, foreign keys, markers; saved as gh_body_<n>.md) / files / commits (each with its parents) / compare against its BASE
(develop) / issue comments (gh_comments_<n>.md). Then the census: every OPEN PR, the WIDEN census (kit.json widen_rx: any of the five keys in a title;
widen_branch_rx: Seat B 35th's `-b35-<n>` branch segment), every other open PR (kit.json `inflight`: state and CURRENT head — they move), and the three
CLOSED predecessors #1302 / #1296 / #1297 (state, merged — each must read closed and NOT merged). Shape copied from gate32's gh_read (gate31 lineage),
re-keyed for gate33 (six rows, no stack, the widen census by title AND branch, every spelling of the b35 token with a planted control).
Writes only beside this script. Usage: gh_read_gate33.py <develop>"""
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
print('gh_read_gate33 (%s)' % K['kit'], datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'current develop', DEV)
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
    print('body markers: Test Evidence %s | NOT covered %s | red proof %s | stacked/retarget named %s | develop 94c9c7aa named %s | develop a24db57e named %s' % (
        bool(re.search(r'(?i)test evidence', b)), bool(re.search(r'(?i)not\s+covered', b)), bool(re.search(r'(?i)red[- ]proof', b)), bool(re.search(r'(?i)stack|retarget', b)), '94c9c7aa' in b, 'a24db57e' in b))
    open(os.path.join(G, 'gh_body_%s.md' % n), 'w', encoding='utf-8').write('#%s %s\nhead %s\n\n%s\n' % (n, t, p['head']['sha'], b))
    f = get('pulls/%s/files?per_page=100' % n); print('files', len(f))
    for x in f: print('  %-8s +%d -%d %s %s' % (x['status'], x['additions'], x['deletions'], x['sha'], x['filename']))
    cs = get('pulls/%s/commits?per_page=100' % n); print('commits', len(cs))
    for c in cs: print('  %s parent %s | %s' % (c['sha'], ','.join(q['sha'][:12] for q in c['parents']), c['commit']['message'].splitlines()[0]))
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
print('  WIDEN census (open PRs titled with one of the five keys, or on a branch matching %r, any author): %s' % (K['widen_branch_rx'], WID or 'NONE'))
# every spelling of Seat B 35th's token (STANDING_LINES 2026-09-27): the branch segment, the seat-record prefix, a ref namespace; each with a planted control
SPELL = {r'-b35-': 'feature/ks-9999-x-b35-9', r's-b35-': 'worktrees/s-b35-ks9999', r'seatb35': 'refs/seatb35/pr9999', r'\bb35\b': 'refs/b35/pr9999'}
for rx, plant in SPELL.items():
    hits = [(x['number'], x['head']['ref']) for x in op if re.search(rx, x['head']['ref'], re.I) and str(x['number']) not in K['this_batch']]
    print('  namespace spelling %r: open PRs OUTSIDE the kit whose branch carries it %s | CONTROL fires on the planted %r: %s' % (rx, hits or 'NONE', plant, bool(re.search(rx, plant, re.I))))
for n in ('1302', '1296', '1297'):
    p = get('pulls/' + n)
    print('  CLOSED predecessor #%s: state %s merged %s head %s closed_at %s | %s' % (n, p['state'], p['merged'], p['head']['sha'], p.get('closed_at'), p['title'][:90]))
print('  WIDEN rows NOT in this kit: %s' % ([w for w in WID if str(w[0]) not in K['this_batch']] or 'NONE'))
