#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub reads for the #1026 (KS-839) TIER 1 ROUND 1 drafter set. GH_TOKEN by NAME from the Secuura .env; never printed. GET only.
PR, files, commits (closing-phrase scan, planted controls), compare develop...head, body KS ids / closing / at-signs, reviews, develop tip, JUDGED blobs at develop and head, open PRs."""
import json, os, re, sys, urllib.request, urllib.error, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1026'
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(n, o): open(os.path.join(G, 'out', 'gh', n), 'w', encoding='utf-8').write(json.dumps(o, indent=1, ensure_ascii=False))
H = '8ab493354bbdb3fa52d2eb14654492db1a891e4a'
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?)\b[:\s]+(?:KS-[0-9]+|#[0-9]+)')
ctl = [len(CLOSE.findall(x)) for x in ('Fixes KS-839', 'closes #1026', 'Refs KS-839')]; assert ctl == [1, 1, 0]
print('gh_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| closing regex controls', ctl)
pr = get('/pulls/1026'); save('pr1026.json', pr); body = pr.get('body') or ''
print('PR #1026', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], '| head', pr['head']['sha'], '== pin', pr['head']['sha'] == H, pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  title:', pr['title'], '| title closing', CLOSE.findall(pr['title']), '| mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']))
print('  body chars', len(body), 'at-signs', body.count('@'), 'closing', CLOSE.findall(body), 'KS ids', {k: len(re.findall(re.escape(k) + r'(?![0-9])', body)) for k in sorted(set(re.findall(r'KS-[0-9]+', body)))})
open(os.path.join(G, 'out', 'gh', 'pr1026_body.md'), 'w', encoding='utf-8').write(body)
for f in get('/pulls/1026/files?per_page=100'): print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
for c in get('/pulls/1026/commits?per_page=100'): print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'closing', CLOSE.findall(c['commit']['message']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', c['commit']['message']))), '|', c['commit']['message'].split('\n')[0][:100])
c = get('/compare/develop...' + H); save('compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/1026/reviews')), '| review comments', len(get('/pulls/1026/comments')), '| issue comments', len(get('/issues/1026/comments')))
dev = get('/branches/develop')['commit']['sha']; print('  develop (branches API)', dev)
D = 'Blockchain/Dev/'
for f in sys.argv[1].split(','):
    row = {}
    for ref in (dev, H):
        try: row[ref[:9]] = get('/contents/' + D + f + '?ref=' + ref)['sha']
        except urllib.error.HTTPError as e: row[ref[:9]] = 'ABSENT' if e.code == 404 else 'HTTP%d' % e.code
    print('  blob %-100s develop %s head %s' % (f, row[dev[:9]], row[H[:9]]))
opn = get('/pulls?state=open&per_page=100'); print('  open PRs:', len(opn), sorted(p['number'] for p in opn))
for q in opn:
    if q['number'] == 1026: continue
    fs = [f['filename'] for f in get('/pulls/%d/files?per_page=100' % q['number'])]
    hit = [f for f in fs if f.startswith(D + 'services/auth/') or f.startswith(D + 'packages/shared/') or f in (D + 'package-lock.json', D + 'docs/openapi/secuura-api.yaml')]
    if hit: print('  open PR #%d overlaps guarded/auth paths:' % q['number'], hit[:8])
