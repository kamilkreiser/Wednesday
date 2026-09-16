#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub reads for the #1017 (KS-1195) tier-1 ROUND 1 set. GH_TOKEN by NAME from the Secuura .env; never printed. GET only.
PR, files, commits, compare develop...head, closing-phrase scan (planted controls), KS-1187 count (control), deploy-precondition presence, issue comments,
reviews, develop tip, JUDGED blobs at develop / head / pull 1014 head, open-PR exact and guarded-path overlap."""
import json, os, re, sys, urllib.request, urllib.error, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017'
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(name, obj): open(os.path.join(G, 'gh', name), 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
H = 'cbe29597d11e59f2e1a14519e9ba3dbf6de9a756'; P14 = '9ba0caf78b8ddb737541df38303b776c982521d2'
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?)\b[:\s]+(?:KS-[0-9]+|#[0-9]+)')
ctl = {'Fixes KS-1195': len(CLOSE.findall('Fixes KS-1195')), 'closes #12': len(CLOSE.findall('closes #12')), 'Refs KS-1195': len(CLOSE.findall('Refs KS-1195'))}
print('gh_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| closing regex controls', ctl)
assert ctl == {'Fixes KS-1195': 1, 'closes #12': 1, 'Refs KS-1195': 0}
K1187 = re.compile(r'KS-1187(?![0-9])'); assert len(K1187.findall('x KS-1187 y KS-11870')) == 1
DEPLOY = re.compile(r'(?i)deploy'); UNMEAS = re.compile(r'(?i)unmeasured')
pr = get('/pulls/1017'); save('pr1017.json', pr)
print('PR #1017', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'], '| title closing', CLOSE.findall(pr['title']))
print('  mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'], '| user', pr['user']['login'])
body = pr.get('body') or ''
open(os.path.join(G, 'gh', 'pr1017_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), 'at-signs', body.count('@'), 'closing', CLOSE.findall(body), 'KS ids', {k: body.count(k) for k in sorted(set(re.findall(r'KS-[0-9]+', body)))}, '| Refs KS-1195', body.count('Refs KS-1195'), '| KS-1187', len(K1187.findall(body + pr['title'])))
dl = [l.strip()[:220] for l in body.splitlines() if DEPLOY.search(l) and UNMEAS.search(l)]
print('  deploy-precondition lines (deploy AND unmeasured, case-insensitive):', len(dl)); [print('    >', x) for x in dl]
files = get('/pulls/1017/files?per_page=100'); save('pr1017_files.json', files)
for f in files: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
commits = get('/pulls/1017/commits?per_page=100'); save('pr1017_commits.json', commits)
for c in commits: print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'closing', CLOSE.findall(c['commit']['message']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', c['commit']['message']))), 'KS-1187', len(K1187.findall(c['commit']['message'])), '|', c['commit']['message'].split('\n')[0][:120])
c = get('/compare/develop...' + H); save('compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/1017/reviews')), '| review comments', len(get('/pulls/1017/comments')))
ics = get('/issues/1017/comments?per_page=100'); save('pr1017_issue_comments.json', ics)
for x in ics: print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'closing', CLOSE.findall(x['body']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', x['body']))), 'KS-1187', len(K1187.findall(x['body'])))
dev = get('/branches/develop')['commit']['sha']; print('  develop (branches API)', dev)
D = 'Blockchain/Dev/'
JUDGED = sys.argv[1].split(',')
blobs = {}
for f in JUDGED:
    row = {}
    for ref in (dev, H, P14):
        try: row[ref[:9]] = get('/contents/' + D + f + '?ref=' + ref)['sha']
        except urllib.error.HTTPError as e: row[ref[:9]] = 'ABSENT' if e.code == 404 else 'HTTP%d' % e.code
    blobs[f] = row
    print('  blob %-80s develop %s head %s pr1014 %s' % (f, row[dev[:9]], row[H[:9]], row[P14[:9]]))
save('judged_blobs.json', blobs)
opn = get('/pulls?state=open&per_page=100')
print('  open PRs:', len(opn))
mine = {f['filename'] for f in files}
GUARD = ('services/api-gateway/src/', 'services/api-gateway/package.json', 'services/api-gateway/tsconfig.json', 'services/api-gateway/vitest.', 'packages/shared/src/', 'services/security/src/index.ts', 'eslint.config.mjs', 'package-lock.json', 'docs/openapi/')
for p in opn:
    if p['number'] == 1017: continue
    pf = get('/pulls/%d/files?per_page=100' % p['number'])
    names = [f['filename'] for f in pf]
    exact = sorted(mine & set(names))
    touch = sorted({n.replace(D, '') for n in names if any(n.replace(D, '').startswith(g) for g in GUARD)})
    print('  open #%d head %s files %d | exact shared with #1017 %s | guarded-path overlap %s | %s' % (p['number'], p['head']['sha'][:9], len(names), exact, touch[:6], p['title'][:60]))
print('gh_read end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
