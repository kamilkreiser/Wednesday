#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub reads for the #1018 (KS-1050) TIER 2 ROUND 1 drafter set. GH_TOKEN by NAME from the Secuura .env; never printed. GET only.
PR (mergeable, mergeable_state), files, commits (closing-phrase scan, planted controls), compare develop...head, body KS ids / closing / at-signs,
reviews, develop tip, blobs at develop and head for argv[1] (comma list, relative to Blockchain/Dev/), open PRs + file overlap with #1018."""
import json, os, re, sys, time, urllib.request, urllib.error, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018'
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(n, o): open(os.path.join(G, 'out', 'gh', n), 'w', encoding='utf-8').write(json.dumps(o, indent=1, ensure_ascii=False))
H = '267bd8624ce276ca62160216d042b8477bac52f1'
N = '1018'
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?)\b[:\s]+(?:KS-[0-9]+|#[0-9]+)')
ctl = [len(CLOSE.findall(x)) for x in ('Fixes KS-1050', 'closes #1018', 'Refs KS-1050')]; assert ctl == [1, 1, 0]
print('gh_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| closing regex controls', ctl)
pr = get('/pulls/' + N)
for _ in range(4):
    if pr.get('mergeable') is not None: break
    time.sleep(3); pr = get('/pulls/' + N)
save('pr1018.json', pr); body = pr.get('body') or ''
print('PR #1018', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], '| head', pr['head']['sha'], '== pin', pr['head']['sha'] == H, pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  title:', pr['title'], '| title closing', CLOSE.findall(pr['title']), '| mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']))
print('  body chars', len(body), 'at-signs', body.count('@'), 'closing', CLOSE.findall(body), 'KS ids', {k: len(re.findall(re.escape(k) + r'(?![0-9])', body)) for k in sorted(set(re.findall(r'KS-[0-9]+', body)))})
open(os.path.join(G, 'out', 'gh', 'pr1018_body.md'), 'w', encoding='utf-8').write(body)
files = get('/pulls/' + N + '/files?per_page=100'); save('pr1018_files.json', files)
mine = set()
for f in files: mine.add(f['filename']); print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
for c in get('/pulls/' + N + '/commits?per_page=100'): print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'closing', CLOSE.findall(c['commit']['message']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', c['commit']['message']))), '|', c['commit']['message'].split('\n')[0][:100])
c = get('/compare/develop...' + H); save('compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/' + N + '/reviews')), '| review comments', len(get('/pulls/' + N + '/comments')), '| issue comments', len(get('/issues/' + N + '/comments')))
dev = get('/branches/develop')['commit']['sha']; print('  develop (branches API)', dev)
D = 'Blockchain/Dev/'
if len(sys.argv) > 1 and sys.argv[1]:
    for f in sys.argv[1].split(','):
        row = {}
        for ref in (dev, H):
            try: row[ref[:9]] = get('/contents/' + D + f + '?ref=' + ref)['sha']
            except urllib.error.HTTPError as e: row[ref[:9]] = 'ABSENT' if e.code == 404 else 'HTTP%d' % e.code
        print('  blob %-90s develop %s head %s' % (f, row[dev[:9]], row[H[:9]]))
opn = get('/pulls?state=open&per_page=100'); print('  open PRs:', len(opn), sorted(p['number'] for p in opn))
for p in opn:
    if p['number'] == int(N): continue
    fs = {f['filename'] for f in get('/pulls/%d/files?per_page=100' % p['number'])}
    shared = sorted(fs & mine)
    auth = sorted(x for x in fs if x.startswith(D + 'services/auth/'))
    if shared or auth: print('  overlap #%d shared %s | auth files %d %s' % (p['number'], shared, len(auth), auth[:6]))
print('gh_read end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
