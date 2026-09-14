#!/usr/bin/env python3
"""gh_read_siblings.py — the sibling PRs that may move develop under the #805 gate: #922 (KS-679, s231's next) and any
open PR whose head branch names ks-741; their heads, bases and per-file blobs (for DEV_CONTENT_ALLOWED). Read-only."""
import json, os, sys, urllib.request, datetime
G = sys.argv[1]; D = os.path.join(G, 'gh')
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('gh_read_siblings', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
opens = get('/pulls?state=open&per_page=100&base=develop')
print('open PRs on develop:', len(opens))
for p in opens:
    print('  #%d %s %s %s' % (p['number'], p['head']['sha'][:9], p['head']['ref'][:70], p['title'][:60]))
for n in (922,):
    pr = get('/pulls/%d' % n); files = get('/pulls/%d/files?per_page=100' % n)
    json.dump(pr, open(os.path.join(D, 'pr%d.json' % n), 'w'), indent=1); json.dump(files, open(os.path.join(D, 'pr%d_files.json' % n), 'w'), indent=1)
    print('#%d %s head %s %s base %s merge_base? commits %d files %d +%d -%d' % (n, pr['state'], pr['head']['sha'], pr['head']['ref'], pr['base']['sha'][:9], pr['commits'], pr['changed_files'], pr['additions'], pr['deletions']))
    for f in files: print('    %-95s %s +%d -%d' % (f['filename'], f['sha'], f['additions'], f['deletions']))
    c = get('/compare/develop...' + pr['head']['sha']); print('    compare develop...#%d: status %s merge_base %s ahead %d behind %d files %d' % (n, c['status'], c['merge_base_commit']['sha'][:9], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
