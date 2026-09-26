#!/usr/bin/env python3
"""gh_read_gate28.py — READ-ONLY GitHub reads (REST GET only) for ONE gate28 kit (the kit is the directory this script lives in; its PR set is
kit.json beside it). GH_TOKEN by NAME from the Secuura .env, never printed. Per PR: head / state / mergeable / base / draft / title (length, ASCII,
the MG-11 squash-subject length `<title> (#NNNN)`) / body (KS keys, Refs lines, closing-word+key count, foreign keys, the Test Evidence and NOT
COVERED markers; saved as gh_body_<n>.md) / files / commits (each with its parents) / compare against the CURRENT develop / issue comments
(gh_comments_<n>.md). Then the census: every OPEN PR (newest first), those on branches of the lanes feeding this round (`-b29-`, `-l7r25-`, `-l6-r24-`), the PRs
split across the two kits, and Seat B 30th's in-flight PRs (kit.json `inflight`: open state and CURRENT head — they move).
Writes only beside this script. Usage: gh_read_gate28.py <develop>"""
import json, os, re, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
DEV = sys.argv[1]
ALLKEYS = {k for p in K['prs'].values() for k in p['keys']}
print('gh_read_gate28 (%s)' % K['kit'], datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'current develop', DEV)
for n in sorted(K['prs']):
    own = set(K['prs'][n]['keys'])
    p = get('pulls/' + n)
    print('=== #%s head %s state %s merged %s mergeable %s mergeable_state %s draft %s base %s head.ref %s' % (n, p['head']['sha'], p['state'], p['merged'], p.get('mergeable'), p.get('mergeable_state'), p['draft'], p['base']['ref'], p['head']['ref']))
    t = p['title']; b = p['body'] or ''
    subj = '%s (#%s)' % (t, n)
    print('title (%d chars, ascii %s; squash subject `<title> (#%s)` = %d chars, MG-11 <= 92: %s): %s' % (len(t), t.isascii(), n, len(subj), len(subj) <= 92, t))
    keys = sorted(set(re.findall(r'KS-\d+', b)))
    print('body %d chars; KS keys %s; Refs lines %s; closing-word+key %d %s; foreign hyphenated keys %s' % (len(b), keys, re.findall(r'(?im)^\s*Refs\b.*$', b),
          len(re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+', b)), re.findall(r'(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+KS-\d+', b), sorted(set(keys) - own)))
    print('body markers: Test Evidence %s | NOT covered %s | red proof %s | UNREACHABLE %d | develop 4db87c3e named %s | d7cdecf1 named %s | 6e2a00bf named %s' % (
        bool(re.search(r'(?i)test evidence', b)), bool(re.search(r'(?i)not\s+covered', b)), bool(re.search(r'(?i)red[- ]proof', b)), b.count('UNREACHABLE'),
        '4db87c3e' in b, 'd7cdecf1' in b, '6e2a00bf' in b))
    open(os.path.join(G, 'gh_body_%s.md' % n), 'w', encoding='utf-8').write('#%s %s\nhead %s\n\n%s\n' % (n, t, p['head']['sha'], b))
    f = get('pulls/%s/files?per_page=100' % n); print('files', len(f))
    for x in f: print('  %-8s +%d -%d %s %s' % (x['status'], x['additions'], x['deletions'], x['sha'], x['filename']))
    cs = get('pulls/%s/commits?per_page=100' % n); print('commits', len(cs))
    for c in cs: print('  %s parent %s | %s' % (c['sha'], ','.join(q['sha'][:12] for q in c['parents']), c['commit']['message'].splitlines()[0]))
    c = get('compare/%s...%s' % (DEV, p['head']['sha']))
    print('compare CURRENT develop...head: status %s merge_base %s ahead %d behind %d files %d %s' % (c['status'], c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c['files']), sorted(x['filename'] for x in c['files'])))
    com = get('issues/%s/comments?per_page=100' % n)
    with open(os.path.join(G, 'gh_comments_%s.md' % n), 'w', encoding='utf-8') as fh:
        for x in com: fh.write('--- comment %s by %s at %s\n%s\n' % (x['id'], x['user']['login'], x['created_at'], x['body']))
    print('issue comments', len(com), [(x['user']['login'], x['created_at']) for x in com])
op = get('pulls?state=open&per_page=100&sort=created&direction=desc')
print('=== census: %d OPEN PRs; newest twenty: %s' % (len(op), [(x['number'], x['head']['ref'][:70], x['created_at']) for x in op[:20]]))
r25 = [x for x in op if str(x['number']) not in K['this_batch']]
print('  EVERY OTHER OPEN PR (the in-flight census: number, head, branch, created): %s' % ([(x['number'], x['head']['sha'][:12], x['head']['ref'], x['created_at']) for x in r25] or 'NONE'))
both = sorted(set(K['this_batch']) | set(K['sibling_batch']))
print('  PRs in THIS kit %s and the SIBLING kit %s; open lane PRs in NEITHER: %s' % (K['this_batch'], K['sibling_batch'], [x['number'] for x in r25 if str(x['number']) not in both]))
for n in K['inflight']:
    p = get('pulls/' + n)
    print('  Seat B 30th in-flight #%s: state %s merged %s head %s updated_at %s (its head WILL move; not in this batch)' % (n, p['state'], p['merged'], p['head']['sha'], p.get('updated_at')))
