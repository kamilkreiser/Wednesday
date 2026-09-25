#!/usr/bin/env python3
"""gh_read_gate21T2b.py — READ-ONLY GitHub reads (REST GET only) for the round-21 SECOND tier-2 batch gate over #1225 #1227 #1229 #1231 #1232
(FROZEN at five). GH_TOKEN by NAME from the Secuura .env, never printed. Per PR: head / state / base / draft / title (length, ASCII) / body (KS keys,
closing-word+key count, marker booleans, full text saved beside as gh_body_<n>.md) / files (status +a -d) / commits (sha, parent, message) /
compare develop...head (merge_base, ahead, behind, files). Plus each PR's issue comments saved as gh_comments_<n>.md. Derived from gate21T2's
gh_read_gate21T2.py, re-keyed. Usage: gh_read_gate21T2b.py [develop sha]"""
import json, os, re, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
DEV = sys.argv[1] if len(sys.argv) > 1 else 'ecb1aa75aefae35a8e2d8694f303adac7c17ab55'
print('gh_read_gate21T2b', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'develop', DEV)
MARK = {'1225': ['#1174', 'guard', 'dead', 'issuerName', 'red', 'legs 3', 'OWED', 'NOT covered', 'Refs KS-1291'],
        '1227': ['deny', 'prefix', 'candidate B', '14', 'collateral', 'len12', 'credit', '58/58', 'legs 3', 'NOT run', 'Refs KS-1252', 'Refs KS-1253'],
        '1229': ['latest', 'examined', 'stale', 'loosening', 'BACKLOG', 'option b', 'legs 3', 'NOT run', 'Refs KS-865', 'Refs KS-808'],
        '1231': ['CREATE TABLE', 'existence', 'SELECT', 'least-privilege', 'migration', 'memory', 'Ornith', 'legs 3', 'NOT run', 'Refs KS-1281'],
        '1232': ['WARN', 'platform', 'seed', 'fake', 'pg', '1142', 'Ornith', 'legs 3', 'NOT run', 'Refs KS-1128']}
for n in ('1225', '1227', '1229', '1231', '1232'):
    p = get('pulls/' + n)
    print('\n=== #%s head %s state %s merged %s draft %s base %s (base.sha %s) head.ref %s' % (n, p['head']['sha'], p['state'], p['merged'], p['draft'], p['base']['ref'], p['base']['sha'], p['head']['ref']))
    t = p['title']; b = p['body'] or ''
    print('title (%d chars, ascii %s): %s' % (len(t), t.isascii(), t))
    print('body %d chars; KS keys %s; closing-word+key %d' % (len(b), sorted(set(re.findall(r'KS-\d+', b))), len(re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+', b))))
    for k in MARK[n]: print('  body marker %-24r %s' % (k, k.lower() in b.lower()))
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
