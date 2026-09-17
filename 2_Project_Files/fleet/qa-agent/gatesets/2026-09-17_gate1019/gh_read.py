#!/usr/bin/env python3
"""gh_read.py JUDGED_CSV — READ-ONLY GitHub reads for the #1019 (KS-1187) tier-1 ROUND 1 set (derived from the #1017 set's gh_read.py). GH_TOKEN by NAME
from the Secuura .env; never printed. GET only. PR, files, commits, compare develop...head, closing-phrase scan (planted controls), KS ids, spelling census of
the PR description (Wednesday's rule: no spelling in the description; controls planted), at-signs, issue comments, reviews, develop tip, JUDGED blobs at
develop / head / #1017 head, open-PR exact and guarded-path overlap."""
import json, os, re, sys, urllib.request, urllib.error, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019'
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(name, obj): open(os.path.join(G, 'gh', name), 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
H = '8b8996f8b290ef55c35721c30f8671f982fa5a91'; P17 = 'cbe29597d11e59f2e1a14519e9ba3dbf6de9a756'
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?)\b[:\s]+(?:KS-[0-9]+|#[0-9]+)')
ctl = {'Fixes KS-1187': len(CLOSE.findall('Fixes KS-1187')), 'closes KS-843': len(CLOSE.findall('closes KS-843')), 'Refs KS-1187': len(CLOSE.findall('Refs KS-1187'))}
print('gh_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| closing regex controls', ctl)
assert ctl == {'Fixes KS-1187': 1, 'closes KS-843': 1, 'Refs KS-1187': 0}
SPELL = re.compile(r'(?i)%[0-9a-f]{2}|[a-z][a-z0-9+.-]*://|;[a-z0-9_]+=|/\./|/\.\./|//erasures|(?-i:ERASURES)')
sc = {x: len(SPELL.findall(x)) for x in ('POST /api/gdpr/%65rasures', 'http://h/erasures', '/erasures;x=1', '/api/gdpr/./erasures', 'Refs KS-1187 the door', '/api/gdpr/ERASURES')}
print('  spelling regex controls', sc); assert sc == {'POST /api/gdpr/%65rasures': 1, 'http://h/erasures': 1, '/erasures;x=1': 1, '/api/gdpr/./erasures': 1, 'Refs KS-1187 the door': 0, '/api/gdpr/ERASURES': 1}
pr = get('/pulls/1019'); save('pr1019.json', pr)
print('PR #1019', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'], '| title closing', CLOSE.findall(pr['title']), '| title spellings', SPELL.findall(pr['title']))
print('  mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'], '| user', pr['user']['login'], '| updated_at', pr['updated_at'])
body = pr.get('body') or ''
open(os.path.join(G, 'gh', 'pr1019_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), 'at-signs', body.count('@'), 'closing', CLOSE.findall(body), 'KS ids', {k: len(re.findall(re.escape(k) + r'(?![0-9])', body)) for k in sorted(set(re.findall(r'KS-[0-9]+', body)))}, '| Refs KS-1187', body.count('Refs KS-1187'), '| spellings in body', SPELL.findall(body))
print('  body lines naming KS-843:', [l.strip()[:160] for l in body.splitlines() if re.search(r'KS-843(?![0-9])', l)])
files = get('/pulls/1019/files?per_page=100'); save('pr1019_files.json', files)
for f in files: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
commits = get('/pulls/1019/commits?per_page=100'); save('pr1019_commits.json', commits)
for c in commits: print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'closing', CLOSE.findall(c['commit']['message']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', c['commit']['message']))), '|', c['commit']['message'].split('\n')[0][:120])
c = get('/compare/develop...' + H); save('compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/1019/reviews')), '| review comments', len(get('/pulls/1019/comments')))
ics = get('/issues/1019/comments?per_page=100'); save('pr1019_issue_comments.json', ics)
for x in ics: print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'closing', CLOSE.findall(x['body']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', x['body']))))
dev = get('/branches/develop')['commit']['sha']; print('  develop (branches API)', dev)
p17 = get('/pulls/1017'); print('  #1017 state', p17['state'], 'merged', p17['merged'], 'head', p17['head']['sha'])
D = 'Blockchain/Dev/'
JUDGED = sys.argv[1].split(',')
blobs = {}
for f in JUDGED:
    row = {}
    for ref in (dev, H, P17):
        try: row[ref[:9]] = get('/contents/' + D + f + '?ref=' + ref)['sha']
        except urllib.error.HTTPError as e: row[ref[:9]] = 'ABSENT' if e.code == 404 else 'HTTP%d' % e.code
    blobs[f] = row
    print('  blob %-84s develop %s head %s pr1017 %s' % (f, row[dev[:9]], row[H[:9]], row[P17[:9]]))
save('judged_blobs.json', blobs)
opn = get('/pulls?state=open&per_page=100')
print('  open PRs:', len(opn))
mine = {f['filename'] for f in files}
GUARD = ('services/api-gateway/src/routes/proxy.ts', 'services/api-gateway/src/middleware/', 'services/api-gateway/src/index.ts', 'services/api-gateway/src/routes/versioning.ts',
         'services/api-gateway/src/__tests__/ks843', 'services/api-gateway/package.json', 'services/api-gateway/tsconfig.json', 'services/api-gateway/vitest.',
         'services/originate/src/routes/gdpr.ts', 'services/originate/src/index.ts', 'eslint.config.mjs', 'package-lock.json')
for p in opn:
    if p['number'] == 1019: continue
    pf = get('/pulls/%d/files?per_page=100' % p['number'])
    names = [f['filename'] for f in pf]
    exact = sorted(mine & set(names))
    touch = sorted({n.replace(D, '') for n in names if any(n.replace(D, '').startswith(g) for g in GUARD)})
    print('  open #%d head %s files %d | exact shared with #1019 %s | guarded-path overlap %s | %s' % (p['number'], p['head']['sha'][:9], len(names), exact, touch[:6], p['title'][:60]))
print('gh_read end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
