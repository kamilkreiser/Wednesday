#!/bin/zsh
# develop_move_read.sh — READ ONLY: what develop moved to (ls-remote; git fetch is NOT used — the object may be absent locally, then the GitHub API reads it).
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
echo "develop_move_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/develop refs/pull/1008/head refs/pull/1007/head refs/pull/1006/head refs/heads/feature/ks-1087-ornith-workflow-approve-keeps-pending
echo "cat-file 0308b7a04: $(git -C "$R" cat-file -t 0308b7a0447a2c01c12aad358c9b4d04a5178210 2>&1)"
python3 - <<'PY'
import json, urllib.request
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
get = lambda p: json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
c = get('/commits/0308b7a0447a2c01c12aad358c9b4d04a5178210')
print('commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'date', c['commit']['committer']['date'], '|', c['commit']['message'].split('\n')[0][:140])
for f in c['files']: print('  ', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
p7 = get('/pulls/1007'); print('PR #1007 state', p7['state'], 'merged', p7['merged'], 'merged_at', p7.get('merged_at'), 'merge_commit_sha', p7.get('merge_commit_sha'))
cmp = get('/compare/develop...dd7086d5aa574285beffc515f9371a438621f25d')
print('compare develop...#1008 head: merge_base %s status %s ahead %d behind %d files %d' % (cmp['merge_base_commit']['sha'], cmp['status'], cmp['ahead_by'], cmp['behind_by'], len(cmp.get('files') or [])))
PY
