#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub reads for the #1008 (KS-1087) tier-1 gate set (derived from the sibling tier-1 set by asserted replacements). GH_TOKEN by NAME from the Secuura .env; never printed. GET only."""
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
H = 'dd7086d5aa574285beffc515f9371a438621f25d'
print('gh_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
pr = get('/pulls/1008'); save('pr1008.json', pr)
print('PR #1008', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], 'author', pr['user']['login'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'])
print('  mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'])
body = pr.get('body') or ''
open(os.path.join(G, 'gh', 'pr1008_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), 'at-signs', body.count('@'), 'ack:schemathesis', body.count('<!--ack:schemathesis-->'), 'ack:akto', body.count('<!--ack:akto-->'), 'ticked [x]', body.count('- [x]'), 'unticked [ ]', body.count('- [ ]'), 'Test Evidence', body.count('## Test Evidence'), 'Part of KS-1087', body.count('Part of KS-1087'), 'closes-like', re.findall(r'(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+KS-[0-9]+', body), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', body))))
for i, l in enumerate(body.split('\n'), 1):
    if '@' in l: print('  body line %d has at-sign: %s' % (i, l[:160]))
files = get('/pulls/1008/files?per_page=100'); save('pr1008_files.json', files)
for f in files: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
commits = get('/pulls/1008/commits?per_page=100'); save('pr1008_commits.json', commits)
for c in commits: print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], c['commit']['message'].split('\n')[0][:120])
c = get('/compare/develop...' + H); save('compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/1008/reviews')), '| review comments', len(get('/pulls/1008/comments')))
ics = get('/issues/1008/comments?per_page=100'); save('pr1008_issue_comments.json', ics)
for x in ics: print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'at-signs', x['body'].count('@'), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', x['body']))))
b = get('/branches/develop'); print('  develop (branches API)', b['commit']['sha'])
opn = get('/pulls?state=open&per_page=50')
print('  open PRs:', len(opn))
for p in opn:
    if p['number'] == 1008: continue
    pf = get('/pulls/%d/files?per_page=100' % p['number'])
    names = [f['filename'].replace('Blockchain/Dev/', '') for f in pf]
    touch = [n for n in names if n.startswith('services/api-gateway/') or n.startswith('services/originate/src/routes/documents') or n.startswith('frontend/issuer/src/components/DocumentList') or n.startswith('services/mcp-server/src/api-client') or n.endswith('package-lock.json') or n == 'eslint.config.mjs']
    print('  open #%d head %s base %s files %d | api-gateway/originate-documents/consumer/lockfile/eslint overlap %s | %s' % (p['number'], p['head']['sha'][:9], p['base']['ref'], len(names), touch, p['title'][:80]))
