#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub reads for the #1011 ROUND 2 (KS-871) tier-1 gate set. GH_TOKEN by NAME from the Secuura .env; never printed. GET only.
Adds over round 1: blobs at the CURRENT develop for the launcher's JUDGED files, compare develop...head with the merge commit, closing-phrase scan over
title/body/every commit message/issue comments with planted controls, open-PR overlap with the census source files."""
import json, os, re, sys, urllib.request, datetime
G = sys.argv[1]
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(name, obj):
    open(os.path.join(G, 'gh', name), 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
H = '6dc8256448b50de6a15519001a4f7032ace1ae19'
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[:\s]+(?:KS-[0-9]+|#[0-9]+)')
ctl = {'Fixes KS-871': len(CLOSE.findall('Fixes KS-871')), 'closes #12': len(CLOSE.findall('closes #12')), 'Part of KS-871': len(CLOSE.findall('Part of KS-871'))}
print('gh_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| closing regex controls', ctl)
assert ctl == {'Fixes KS-871': 1, 'closes #12': 1, 'Part of KS-871': 0}
pr = get('/pulls/1011'); save('pr1011.json', pr)
print('PR #1011', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'], '| title closing', CLOSE.findall(pr['title']))
print('  mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'])
body = pr.get('body') or ''
open(os.path.join(G, 'gh', 'pr1011_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), 'at-signs', body.count('@'), 'Part of KS-871', body.count('Part of KS-871'), 'Round 2 heads', body.count('Round 2'), 'superseded', body.lower().count('superseded'), 'closing', CLOSE.findall(body), 'KS ids', {k: body.count(k) for k in sorted(set(re.findall(r'KS-[0-9]+', body)))})
files = get('/pulls/1011/files?per_page=100'); save('pr1011_files.json', files)
for f in files: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
commits = get('/pulls/1011/commits?per_page=100'); save('pr1011_commits.json', commits)
for c in commits: print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'closing', CLOSE.findall(c['commit']['message']), '|', c['commit']['message'].split('\n')[0][:110])
c = get('/compare/develop...' + H); save('compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d %s' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or []), [(x['filename'].split('/')[-1], x['sha'][:9]) for x in c.get('files') or []]))
print('  reviews', len(get('/pulls/1011/reviews')), '| review comments', len(get('/pulls/1011/comments')))
ics = get('/issues/1011/comments?per_page=100'); save('pr1011_issue_comments.json', ics)
for x in ics: print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'closing', CLOSE.findall(x['body']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', x['body']))))
b = get('/branches/develop'); dev = b['commit']['sha']; print('  develop (branches API)', dev)
D = 'Blockchain/Dev/'
JUDGED = ['services/api-gateway/src/middleware/audit.ts', 'services/api-gateway/src/index.ts', 'services/api-gateway/src/routes/proxy.ts', 'services/api-gateway/src/middleware/normalisePath.ts',
          'services/api-gateway/src/routes/versioning.ts', 'services/api-gateway/src/db.ts', 'services/api-gateway/src/middleware/auth.ts', 'services/api-gateway/package.json',
          'services/api-gateway/vitest.config.ts', 'services/api-gateway/vitest.setup.ts', 'services/api-gateway/tsconfig.json', 'eslint.config.mjs',
          'services/api-gateway/src/routes/audit-export.ts', 'services/api-gateway/src/routes/verification.ts']
blobs = {}
for f in JUDGED:
    blobs[f] = {ref[:9]: get('/contents/' + D + f + '?ref=' + ref)['sha'] for ref in (dev, H)}
    print('  blob %-52s develop %s head %s' % (f, blobs[f][dev[:9]], blobs[f][H[:9]]))
save('judged_blobs.json', blobs)
opn = get('/pulls?state=open&per_page=50')
print('  open PRs:', len(opn))
CENSUS = ('services/api-gateway/src/middleware/audit.ts', 'services/api-gateway/src/index.ts', 'services/api-gateway/src/routes/', 'services/api-gateway/src/middleware/normalisePath.ts', 'services/api-gateway/src/services/health.ts', 'services/api-gateway/src/db', 'services/api-gateway/src/middleware/auth.ts')
for p in opn:
    if p['number'] == 1011: continue
    pf = get('/pulls/%d/files?per_page=100' % p['number'])
    names = [f['filename'].replace(D, '') for f in pf]
    touch = [n for n in names if n.startswith(CENSUS) or 'ks871' in n or n.endswith('package-lock.json') or n in ('services/api-gateway/package.json', 'services/api-gateway/tsconfig.json', 'eslint.config.mjs')]
    print('  open #%d head %s base %s files %d | census/guarded overlap %s | %s' % (p['number'], p['head']['sha'][:9], p['base']['ref'], len(names), touch, p['title'][:80]))
print('gh_read end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
