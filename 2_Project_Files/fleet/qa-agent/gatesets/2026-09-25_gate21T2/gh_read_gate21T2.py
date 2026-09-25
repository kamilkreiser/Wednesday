#!/usr/bin/env python3
"""gh_read_gate21T2.py — READ-ONLY GitHub reads (REST GET only) for the round-21 TIER-2 batch gate over #1215 #1218 #1220 #1221 #1222 #1223 (#1222 and #1223 added by Wednesday mid-draft; the batch is FROZEN at six).
GH_TOKEN by NAME from the Secuura .env, never printed. Per PR: head / state / base / draft / title (length, ASCII) / body (KS keys, closing-word+key
count, marker booleans, full text saved beside as gh_body_<n>.md) / files (status +a -d) / commits (sha, parent, message) / compare develop...head.
Plus each PR's issue comments saved as gh_comments_<n>.md. Derived from gate21T1's gh_read_gate21T1.py, re-keyed.
Usage: gh_read_gate21T2.py [develop sha]"""
import json, os, re, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
DEV = sys.argv[1] if len(sys.argv) > 1 else '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'
print('gh_read_gate21T2', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'develop', DEV)
MARK = {'1215': ['LEG D', 'by text', 'ordinal', 'ks781', 'red', 'tamper', 'legs 3, 4, 8', 'NOT run', 'NOT covered', 'Refs KS-1288'],
        '1218': ['build_fixture', '/dev/null', 'upstream=NONE', 'control', 'red', 'tamper', 'legs 3, 4, 8', 'NOT run', 'NOT covered', 'Refs KS-897', 'Refs KS-896'],
        '1220': ['anchorReadback', 'block_number', 'Number(', 'null', 'buildResponse', 'remaining', 'KS-562', 'threadTokenMint', 'legs 3/4/8', 'OWED', 'NOT covered', 'Refs KS-1129'],
        '1222': ['forwarded', 'entity.too.large', 'error-handler', 'canary', '0-hit', 'control', 'red', 'legs 3, 4, 8', 'NOT run', 'NOT covered', 'Refs KS-1181'],
        '1223': ['hash', 'documentHash', 'precedence', 'F-2', 'F-3', 'verification.ts', '#1136', 'T5', 'red', 'legs 3, 4, 8', 'NOT run', 'NOT covered', 'Refs KS-1118'],
        '1221': ['ANCHORING_SERVICE_URL', '127.0.0.1:2', '127.0.0.1:1', 'ECONNREFUSED', 'port 1', 'ks1228', 'ks520', 'probe', 'legs 3, 4, 8', 'NOT covered', 'Refs KS-1266']}
for n in ('1215', '1218', '1220', '1221', '1222', '1223'):
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
