#!/usr/bin/env python3
"""develop_move_read.py — READ-ONLY: what moved develop past 40fe4db69 during drafting (GitHub API GET only; GH_TOKEN by NAME, never printed)."""
import json, urllib.request, datetime, subprocess
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('develop_move_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('ls-remote develop:', subprocess.run(['git', '-C', '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files', 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1006/head', 'refs/pull/1005/head'], capture_output=True, text=True).stdout.strip().replace('\n', ' | '))
c = get('/compare/40fe4db6963cd11dba06bd46e0b00af39e68ef3a...develop')
print('compare 40fe4db69...develop: status', c['status'], 'ahead', c['ahead_by'], 'behind', c['behind_by'])
for cm in c['commits']: print('  commit', cm['sha'], 'parents', [p['sha'][:9] for p in cm['parents']], cm['commit']['message'].split('\n')[0][:140])
for f in c.get('files') or []: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
p = get('/pulls/1005'); print('PR #1005 state', p['state'], 'merged', p['merged'], 'merge_commit', p.get('merge_commit_sha'), 'merged_at', p.get('merged_at'))
c2 = get('/compare/develop...86fe59e6bf07108142fb3dbd06bef8747d2a4687')
print('compare develop...#1006 head: merge_base', c2['merge_base_commit']['sha'], 'status', c2['status'], 'ahead', c2['ahead_by'], 'behind', c2['behind_by'], 'files', len(c2.get('files') or []))
