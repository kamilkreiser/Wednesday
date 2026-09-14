#!/usr/bin/env python3
"""gh_read.py — PR #805 via the GitHub API (read-only): the PR, its files, commits, reviews, review comments, issue
comments (Peter's question 5584860862 + the builder's answer 5662521346), the compare develop...head and M44...develop.
Raw JSON to <gateset>/gh/; a summary to stdout. GH_TOKEN by NAME from the Secuura .env; never printed."""
import json, os, sys, urllib.request, datetime, re
G = sys.argv[1]; D = os.path.join(G, 'gh'); os.makedirs(D, exist_ok=True)
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(name, obj):
    with open(os.path.join(D, name), 'w', encoding='utf-8') as f: json.dump(obj, f, indent=1)
print('gh_read', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
pr = get('/pulls/805'); save('pr805.json', pr)
body = pr.get('body') or ''
open(os.path.join(D, 'pr805_body.md'), 'w', encoding='utf-8').write(body)
print('PR', pr['number'], pr['state'], 'draft', pr['draft'], 'head', pr['head']['sha'], pr['head']['ref'], 'base', pr['base']['ref'], pr['base']['sha'][:9], 'mergeable', pr.get('mergeable'), pr.get('mergeable_state'), 'commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), 'title:', pr['title'])
print('body chars', len(body), 'at-signs', body.count('@'), 'ack:schemathesis', body.count('<!--ack:schemathesis-->'), 'ack:akto', body.count('<!--ack:akto-->'), 'Closes KS-726', body.count('Closes KS-726'), '## Test Evidence', body.count('## Test Evidence'), 'ticked [x]', len(re.findall(r'- \[x\]', body)), 'unticked [ ]', len(re.findall(r'- \[ \]', body)))
files = get('/pulls/805/files?per_page=100'); save('pr805_files.json', files)
print('files', len(files))
for f in files: print('  %-90s %s +%d -%d %s' % (f['filename'], f['sha'][:9], f['additions'], f['deletions'], f['status']))
commits = get('/pulls/805/commits?per_page=100'); save('pr805_commits.json', commits)
print('commits', len(commits))
for c in commits: print('  ', c['sha'][:9], c['commit']['committer']['date'], '|', c['commit']['message'].split('\n')[0][:110], '| parents', [p['sha'][:9] for p in c['parents']])
reviews = get('/pulls/805/reviews?per_page=100'); save('pr805_reviews.json', reviews)
print('reviews', len(reviews))
for r in reviews: print('  ', r['id'], r['state'], r['user']['login'], r['submitted_at'], 'commit', (r.get('commit_id') or '')[:9], 'body chars', len(r.get('body') or ''))
rc = get('/pulls/805/comments?per_page=100'); save('pr805_review_comments.json', rc)
print('review comments', len(rc))
for r in rc: print('  ', r['id'], r['user']['login'], r['created_at'], r.get('path'), r.get('line') or r.get('original_line'), 'chars', len(r.get('body') or ''))
ic = get('/issues/805/comments?per_page=100'); save('pr805_issue_comments.json', ic)
print('issue comments', len(ic))
for c in ic:
    b = c.get('body') or ''
    print('  ', c['id'], c['user']['login'], c['created_at'], 'chars', len(b), 'at-signs', b.count('@'), '|', b.split('\n')[0][:120])
    open(os.path.join(D, 'comment_%d.md' % c['id']), 'w', encoding='utf-8').write(b)
for name, rng in (('compare_develop_head', 'develop...' + pr['head']['sha']), ('compare_M44_develop', '346b491f2...develop'), ('compare_M45_develop', '852e1fff7...develop')):
    c = get('/compare/' + rng); save(name + '.json', c)
    print(name, 'status', c['status'], 'merge_base', c['merge_base_commit']['sha'], 'ahead', c['ahead_by'], 'behind', c['behind_by'], 'files', len(c.get('files') or []), 'commits', len(c.get('commits') or []))
    for f in (c.get('files') or [])[:60]: print('    ', f['filename'], f['sha'][:9], '+%d -%d' % (f['additions'], f['deletions']))
dev = get('/branches/develop'); print('develop', dev['commit']['sha'], dev['commit']['commit']['committer']['date'], '|', dev['commit']['commit']['message'].split('\n')[0][:100])
