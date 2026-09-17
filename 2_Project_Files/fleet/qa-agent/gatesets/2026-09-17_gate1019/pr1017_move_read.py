#!/usr/bin/env python3
"""pr1017_move_read.py — READ-ONLY (GET): #1017's head moved during drafting (bounds_end 09:50:05: refs/pull/1017/head a067d4e3e, was cbe29597d at 09:37:10).
PR state, commits (sha, parents, message head), files with blob shas vs the cbe29597d blobs the #1019 launcher pins, compare cbe29597d...a067d4e3e,
compare develop...a067d4e3e, and whether the new head touches any #1019 file or proxy.ts. GH_TOKEN by NAME, never printed."""
import json, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('pr1017_move_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
p = get('/pulls/1017'); print('#1017 state', p['state'], 'merged', p['merged'], 'head', p['head']['sha'], 'updated_at', p['updated_at'], 'commits', p['commits'], 'files', p['changed_files'])
for c in get('/pulls/1017/commits?per_page=100'): print('  commit', c['sha'], 'parents', [x['sha'][:9] for x in c['parents']], c['commit']['committer']['date'], '|', c['commit']['message'].split('\n')[0][:140])
PIN = {'auth.ts': '8fbe102eb', 'rateLimitEnforce.ts': 'f4b66aa1a', 'index.ts': 'db127dbfa', 'ks1195-per-key-rate-limiter-runs-after-authentication.test.ts': 'ade08ac1e', 'ks781-p3-3-body-parser-order.test.ts': 'bc4815c4e'}
for f in get('/pulls/1017/files?per_page=100'):
    base = f['filename'].split('/')[-1]
    print('  file', f['status'], f['sha'][:9], 'pinned-in-#1019-launcher', PIN.get(base), 'SAME' if PIN.get(base) and f['sha'].startswith(PIN[base]) else 'DIFFERENT/NEW', f['filename'])
c = get('/compare/cbe29597d11e59f2e1a14519e9ba3dbf6de9a756...' + p['head']['sha']); print('  compare cbe29597d...head: status', c['status'], 'ahead', c['ahead_by'], 'behind', c['behind_by'], 'files', [(x['filename'].split('/')[-1], x['sha'][:9]) for x in c.get('files') or []])
d = get('/compare/develop...' + p['head']['sha']); print('  compare develop...#1017 head: merge_base', d['merge_base_commit']['sha'][:9], 'status', d['status'], 'ahead', d['ahead_by'], 'behind', d['behind_by'], 'files', len(d.get('files') or []))
print('  develop', get('/branches/develop')['commit']['sha'], '| #1019 head', get('/pulls/1019')['head']['sha'])
