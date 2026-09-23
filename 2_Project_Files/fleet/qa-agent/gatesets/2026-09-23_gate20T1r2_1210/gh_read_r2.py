#!/usr/bin/env python3
"""gh_read_r2.py — read-only GitHub reads for #1210 (GH_TOKEN by NAME from the Secuura .env, never printed): the pull (head, state, base, title
length, body markers), its files, the compare develop...head, and the round-2 commit's message."""
import json, urllib.request, re
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
p = get('pulls/1210')
print('head', p['head']['sha'], 'state', p['state'], 'merged', p['merged'], 'base', p['base']['ref'], p['base']['sha'], 'draft', p['draft'])
t = p['title']; b = p['body'] or ''
print('title (%d chars, ascii %s): %s' % (len(t), t.isascii(), t))
print('body %d chars; KS keys %s; closing-word+key %d' % (len(b), sorted(set(re.findall(r'KS-\d+', b))), len(re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+', b))))
for k in ('FINDING', 'platform.ts:204', 'ks1215', 'ks1238', 'dangl', 'not fixed', 'LEG D', '827', 'round 2', 'Refs KS-1239'):
    print('  body marker %-16r %s' % (k, k.lower() in b.lower()))
f = get('pulls/1210/files'); print('files', len(f)); [print('  %s +%d -%d %s' % (x['status'], x['additions'], x['deletions'], x['filename'])) for x in f]
c = get('compare/dd8f99cc75b9b753172a40379eaab2b6c1026180...' + p['head']['sha'])
print('compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c['files'])))
m = get('commits/' + p['head']['sha'])['commit']['message']; print('r2 commit message (%d chars):' % len(m)); print(m)
