#!/usr/bin/env python3
"""gh_read_gate24T2b.py — READ-ONLY GitHub reads (REST GET only) for gate24T2b over #1249, #1250, #1251, #1252, #1253, #1254, #1255 (and #1248's state only: it is
in the RUNNING gate24T2a batch and #1249 is STACKED on it — context, NOT graded here). GH_TOKEN by NAME from the Secuura .env, never printed. Per PR:
head / state / mergeable / base / draft / title (length, ASCII) / body (KS keys, Refs lines, closing-word+key count; saved as gh_body_<n>.md) /
files / commits / compare against the CURRENT develop / issue comments (gh_comments_<n>.md). Then the WIDEN census: every OPEN PR, and any whose
head branch names Seat L5's widen keys (ks-1201, ks-1296, ks-906, ks-1139). Usage: gh_read_gate24T2b.py <develop>"""
import json, os, re, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
DEV = sys.argv[1]
print('gh_read_gate24T2b', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'current develop', DEV)
for n in ('1249', '1250', '1251', '1252', '1253', '1254', '1255'):
    p = get('pulls/' + n)
    print('=== #%s head %s state %s merged %s mergeable %s mergeable_state %s draft %s base %s head.ref %s' % (n, p['head']['sha'], p['state'], p['merged'], p.get('mergeable'), p.get('mergeable_state'), p['draft'], p['base']['ref'], p['head']['ref']))
    t = p['title']; b = p['body'] or ''
    print('title (%d chars, ascii %s): %s' % (len(t), t.isascii(), t))
    print('body %d chars; KS keys %s; Refs lines %s; closing-word+key %d' % (len(b), sorted(set(re.findall(r'KS-\d+', b))), re.findall(r'(?im)^\s*Refs\b.*$', b), len(re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+', b))))
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
p = get('pulls/1248')
print('=== #1248 (gate24T2a, NOT GRADED here; #1249 is stacked on it) head %s state %s merged %s mergeable %s title %s' % (p['head']['sha'], p['state'], p['merged'], p.get('mergeable'), p['title']))
op = get('pulls?state=open&per_page=100&sort=created&direction=desc')
print('=== WIDEN census: %d OPEN PRs; newest ten: %s' % (len(op), [(x['number'], x['head']['ref'][:60]) for x in op[:10]]))
wid = [x for x in op if re.search(r'ks-(1201|1296|906|1139)\b', x['head']['ref'])]
print('  open PRs on Seat L5 widen branches (ks-1201 / ks-1296 / ks-906 / ks-1139): %s' % ([(x['number'], x['head']['sha'], x['head']['ref'], x['created_at']) for x in wid] or 'NONE'))
