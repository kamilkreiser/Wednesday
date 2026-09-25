#!/usr/bin/env python3
"""gh_read_gate21T1d.py — REST GET only: PR #1239 (head, base, state, mergeable, title, body), its commits and files, the compare develop...head.
Writes gh_body_1239.md beside this script. Never prints a credential."""
import json, os, re, sys, time, urllib.request
GS = os.path.dirname(os.path.abspath(__file__))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
API = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(API + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
p = get('pulls/1239'); tries = 1
while p.get('mergeable') is None and tries < 3:
    time.sleep(10); p = get('pulls/1239'); tries += 1
body = p.get('body') or ''
open(os.path.join(GS, 'gh_body_1239.md'), 'w', encoding='utf-8').write(body)
print('PR #1239 head %s base %s state %s mergeable %s (reads %d) draft %s' % (p['head']['sha'], p['base']['ref'], p['state'], p.get('mergeable'), tries, p.get('draft')))
print('title (%d chars, ascii %s): %s' % (len(p['title']), p['title'].isascii(), p['title']))
keys = re.findall(r'\bKS-\d+\b', body)
print('body: %d bytes; hyphenated KS keys: %s' % (len(body.encode()), sorted(set(keys), key=lambda k: int(k[3:]))), '| counts', {k: keys.count(k) for k in sorted(set(keys))})
print('closing words before a key:', re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#?KS-\d+', body))
cs = get('pulls/1239/commits')
for c in cs: print('commit %s parents %s | %s' % (c['sha'], [x['sha'][:9] for x in c['parents']], c['commit']['message'].splitlines()[0]))
fs = get('pulls/1239/files?per_page=100')
for f in fs: print('file %s %s +%d/-%d' % (f['status'], f['filename'], f['additions'], f['deletions']))
dev = sys.argv[1] if len(sys.argv) > 1 else 'develop'
c = get('compare/%s...%s' % (dev, p['head']['sha']))
print('compare %s...head: merge_base %s ahead %d behind %d files %d' % (dev, c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
