#!/usr/bin/env python3
"""gh_read_gate21T1.py — READ-ONLY GitHub reads (REST GET only) for the round-21 tier-1 batch gate over #1213 #1214 #1216 #1217.
GH_TOKEN by NAME from the Secuura .env, never printed. Per PR: head / state / base / draft / title (length, ASCII) / body (KS keys, closing-word+key
count, marker booleans, full text saved beside as gh_body_<n>.md) / files (status +a -d) / commits (sha, parent, message) / compare develop...head.
Plus each PR's issue comments (the seats' READY / Test Evidence may be posted there) saved as gh_comments_<n>.md.
Usage: gh_read_gate21T1.py [develop sha]   (writes gh_body_*.md / gh_comments_*.md beside itself; everything else to stdout)"""
import json, os, re, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
DEV = sys.argv[1] if len(sys.argv) > 1 else '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'
print('gh_read_gate21T1', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'develop', DEV)
MARK = {'1213': ['frvp', 'GHSA-frvp-7c67-39w9', '1.19.15', 'mcp-server', 'originate', '@prisma/dev', 'overrides', 'audit-baseline', 'NOT covered', 'legs 3, 4, 8', 'Refs KS-530'],
        '1214': ['jjmj', 'GHSA-jjmj-jmhj-qwj2', '6.30.6', 'react-router-dom', 'audit-baseline', 'row', 'audit:contract', 'NOT covered', 'legs 3, 4, 8', 'Refs KS-528'],
        '1216': ['explicitScope', 'principalScope', 'null', 'MALFORMED', 'byte-identical', 'rateLimitScope', 'legs 3/4/8', 'OWED', 'NOT covered', 'Refs KS-975'],
        '1217': ['reset', 'first failing path', '400', 'message', ':757', ':808', 'legs 3/4/8', 'OWED', 'NOT covered', 'Refs KS-976']}
for n in ('1213', '1214', '1216', '1217'):
    p = get('pulls/' + n)
    print('\n=== #%s head %s state %s merged %s draft %s base %s (base.sha %s) head.ref %s' % (n, p['head']['sha'], p['state'], p['merged'], p['draft'], p['base']['ref'], p['base']['sha'], p['head']['ref']))
    t = p['title']; b = p['body'] or ''
    print('title (%d chars, ascii %s): %s' % (len(t), t.isascii(), t))
    print('body %d chars; KS keys %s; closing-word+key %d' % (len(b), sorted(set(re.findall(r'KS-\d+', b))), len(re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+', b))))
    for k in MARK[n]: print('  body marker %-22r %s' % (k, k.lower() in b.lower()))
    open(os.path.join(G, 'gh_body_%s.md' % n), 'w', encoding='utf-8').write('#%s %s\nhead %s\n\n%s\n' % (n, t, p['head']['sha'], b))
    f = get('pulls/%s/files?per_page=100' % n); print('files', len(f))
    for x in f: print('  %-8s +%d -%d %s' % (x['status'], x['additions'], x['deletions'], x['filename']))
    cs = get('pulls/%s/commits?per_page=100' % n); print('commits', len(cs))
    for c in cs: print('  %s parent %s | %s' % (c['sha'], ','.join(q['sha'][:12] for q in c['parents']), c['commit']['message'].splitlines()[0]))
    c = get('compare/%s...%s' % (DEV, p['head']['sha']))
    print('compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c['files'])))
    com = get('issues/%s/comments?per_page=100' % n)
    with open(os.path.join(G, 'gh_comments_%s.md' % n), 'w', encoding='utf-8') as fh:
        for x in com: fh.write('--- comment %s by %s at %s\n%s\n' % (x['id'], x['user']['login'], x['created_at'], x['body']))
    print('issue comments', len(com), [(x['user']['login'], x['created_at']) for x in com])
