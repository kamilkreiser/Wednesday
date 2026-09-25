#!/usr/bin/env python3
"""gh_read_gate21T2c.py — READ-ONLY GitHub reads (REST GET only) for the round-21 THIRD tier-2 batch gate over #1218 (round 2), #1219, #1233, #1235,
#1236, #1237, #1238 + #1223 ROUND 2 (widened by Wednesday 06:3xZ; eight, frozen). GH_TOKEN by NAME from the Secuura .env, never printed. Derived from gate21T1b's
gh_read_gate21T1b.py, re-keyed. Per PR: head / state / mergeable / base / draft / title (length, ASCII) / body (KS keys, closing-word+key count, full
text saved beside as gh_body_<n>.md) / files (status +a -d) / commits / compare against the CURRENT develop AND the old develop 6ab9d5021 (merge_base,
ahead, behind, files BY NAME) + issue comments saved as gh_comments_<n>.md.
Usage: gh_read_gate21T2c.py [current develop sha]"""
import json, os, re, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
DEV = sys.argv[1] if len(sys.argv) > 1 else '379c6eb1d45905f398fae67ee7dd2f46ad40432f'
OLD = '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'
print('gh_read_gate21T2c', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'current develop', DEV, '| old develop', OLD)
NS = ('1218', '1219', '1233', '1235', '1236', '1237', '1238', '1223')
for n in NS:
    p = get('pulls/' + n)
    print('\n=== #%s head %s state %s merged %s mergeable %s draft %s base %s (base.sha %s) head.ref %s' % (n, p['head']['sha'], p['state'], p['merged'], p.get('mergeable'), p['draft'], p['base']['ref'], p['base']['sha'], p['head']['ref']))
    t = p['title']; b = p['body'] or ''
    print('title (%d chars, ascii %s): %s' % (len(t), t.isascii(), t))
    print('body %d chars; KS keys %s; closing-word+key %d; legs 3/4/8 named %s' % (len(b), sorted(set(re.findall(r'KS-\d+', b))), len(re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+', b)), 'legs 3/4/8' in b.lower()))
    open(os.path.join(G, 'gh_body_%s.md' % n), 'w', encoding='utf-8').write('#%s %s\nhead %s\n\n%s\n' % (n, t, p['head']['sha'], b))
    f = get('pulls/%s/files?per_page=100' % n); print('files', len(f))
    for x in f: print('  %-8s +%d -%d %s' % (x['status'], x['additions'], x['deletions'], x['filename']))
    cs = get('pulls/%s/commits?per_page=100' % n); print('commits', len(cs))
    for c in cs: print('  %s parent %s | %s' % (c['sha'], ','.join(q['sha'][:12] for q in c['parents']), c['commit']['message'].splitlines()[0]))
    for lab, base in (('CURRENT develop', DEV), ('OLD develop', OLD)):
        c = get('compare/%s...%s' % (base, p['head']['sha']))
        print('compare %s...head: merge_base %s ahead %d behind %d files %d %s' % (lab, c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c['files']), sorted(x['filename'] for x in c['files'])))
    com = get('issues/%s/comments?per_page=100' % n)
    with open(os.path.join(G, 'gh_comments_%s.md' % n), 'w', encoding='utf-8') as fh:
        for x in com: fh.write('--- comment %s by %s at %s\n%s\n' % (x['id'], x['user']['login'], x['created_at'], x['body']))
    print('issue comments', len(com), [(x['user']['login'], x['created_at']) for x in com])
