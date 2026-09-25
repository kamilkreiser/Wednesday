#!/usr/bin/env python3
"""gh_read_gate21T2e.py — READ-ONLY GitHub reads (REST GET only) for gate21T2e over #1241 KS-1226 round 2. GH_TOKEN by NAME from the Secuura .env,
never printed. Head / state / mergeable / base / draft / title (length, ASCII) / body (KS keys, closing-word+key count; saved as gh_body_1241.md) /
files / commits / compare against the CURRENT develop AND BASE aa600af94 / issue comments (gh_comments_1241.md). Usage: gh_read_gate21T2e.py <develop>"""
import json, os, re, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
DEV = sys.argv[1]; OLD = 'aa600af94d69ad59db279d32cbbd7596931a739b'; n = '1241'
print('gh_read_gate21T2e', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'current develop', DEV, '| BASE', OLD)
p = get('pulls/' + n)
print('=== #%s head %s state %s merged %s mergeable %s mergeable_state %s draft %s base %s head.ref %s' % (n, p['head']['sha'], p['state'], p['merged'], p.get('mergeable'), p.get('mergeable_state'), p['draft'], p['base']['ref'], p['head']['ref']))
t = p['title']; b = p['body'] or ''
print('title (%d chars, ascii %s): %s' % (len(t), t.isascii(), t))
print('body %d chars; KS keys %s; closing-word+key %d' % (len(b), sorted(set(re.findall(r'KS-\d+', b))), len(re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+', b))))
open(os.path.join(G, 'gh_body_1241.md'), 'w', encoding='utf-8').write('#%s %s\nhead %s\n\n%s\n' % (n, t, p['head']['sha'], b))
f = get('pulls/%s/files?per_page=100' % n); print('files', len(f))
for x in f: print('  %-8s +%d -%d %s' % (x['status'], x['additions'], x['deletions'], x['filename']))
cs = get('pulls/%s/commits?per_page=100' % n); print('commits', len(cs))
for c in cs: print('  %s parent %s | %s' % (c['sha'], ','.join(q['sha'][:12] for q in c['parents']), c['commit']['message'].splitlines()[0]))
for lab, base in (('CURRENT develop', DEV), ('BASE', OLD)):
    c = get('compare/%s...%s' % (base, p['head']['sha']))
    print('compare %s...head: status %s merge_base %s ahead %d behind %d files %d %s' % (lab, c['status'], c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c['files']), sorted(x['filename'] for x in c['files'])))
com = get('issues/%s/comments?per_page=100' % n)
with open(os.path.join(G, 'gh_comments_1241.md'), 'w', encoding='utf-8') as fh:
    for x in com: fh.write('--- comment %s by %s at %s\n%s\n' % (x['id'], x['user']['login'], x['created_at'], x['body']))
print('issue comments', len(com), [(x['user']['login'], x['created_at']) for x in com])
