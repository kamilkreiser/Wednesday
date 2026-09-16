#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub reads for the #1007 (KS-864) tier-2 gate set. GH_TOKEN by NAME from the Secuura .env; never printed. GET only.
Reads PR #1007 (state, head, files, commits, body, comments, compare), and file-disjointness against every open PR (named: #1005, #1006)."""
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
H = 'b28ed490ada70df2056763f4512c98443285a694'
print('gh_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
pr = get('/pulls/1007'); save('pr1007.json', pr)
print('PR #1007', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], 'author', pr['user']['login'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'])
print('  mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'])
body = pr.get('body') or ''
open(os.path.join(G, 'gh', 'pr1007_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), 'ack:schemathesis', body.count('<!--ack:schemathesis-->'), 'ack:akto', body.count('<!--ack:akto-->'), 'ticked [x]', body.count('- [x]'), 'unticked [ ]', body.count('- [ ]'), 'Test Evidence', body.count('## Test Evidence'),
      'closes-like', re.findall(r'(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(?:#\d+|KS-[0-9]+)', body), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', body))), 'Part of KS-864', body.count('Part of KS-864'))
for i, l in enumerate(body.split('\n'), 1):
    if '@' in l: print('  body line %d has at-sign: %s' % (i, l[:160]))
files = get('/pulls/1007/files?per_page=100'); save('pr1007_files.json', files)
mine = set()
for f in files:
    print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename']); mine.add(f['filename'])
commits = get('/pulls/1007/commits?per_page=100'); save('pr1007_commits.json', commits)
for c in commits: print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], c['commit']['message'].split('\n')[0][:120])
c = get('/compare/develop...' + H); save('compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/1007/reviews')), '| review comments', len(get('/pulls/1007/comments')))
ics = get('/issues/1007/comments?per_page=100'); save('pr1007_issue_comments.json', ics)
for x in ics: print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', x['body']))), 'closes-like', re.findall(r'(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+KS-[0-9]+', x['body']))
for kind in ('check-runs', 'status'):
    try:
        r = get('/commits/%s/%s' % (H, kind)); print('  %s: read, keys %s' % (kind, sorted(r.keys())[:6]))
    except Exception as e: print('  %s: %s' % (kind, getattr(e, 'code', type(e).__name__)))
b = get('/branches/develop'); print('  develop (branches API)', b['commit']['sha'])
opn = get('/pulls?state=open&per_page=100')
print('  open PRs:', len(opn))
for p in opn:
    if p['number'] == 1007: continue
    pf = get('/pulls/%d/files?per_page=100' % p['number'])
    names = {f['filename'] for f in pf}
    shared = sorted(names & mine)
    ss = sorted(n.replace('Blockchain/Dev/', '') for n in names if 'system-status' in n or 'api-gateway/src/index.ts' in n)
    print('  open #%d head %s files %d | SHARED with #1007: %s | system-status/index.ts: %s | %s' % (p['number'], p['head']['sha'][:9], len(names), shared, ss, p['title'][:70]))
    if p['number'] in (1005, 1006):
        for n in sorted(names): print('      #%d file %s' % (p['number'], n))
