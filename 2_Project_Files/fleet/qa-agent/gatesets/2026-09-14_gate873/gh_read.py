#!/usr/bin/env python3
"""gh_read.py — PR #873 via the GitHub API (GH_TOKEN by NAME from the Secuura .env; never printed). Raw JSON under gh/."""
import json, os, sys, urllib.request, datetime
G = sys.argv[1]
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(name, obj):
    with open(os.path.join(G, 'gh', name), 'w', encoding='utf-8') as f: json.dump(obj, f, indent=1)
print('gh_read', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
pr = get('/pulls/873'); save('pr873.json', pr)
print('PR #873', pr['state'], 'draft', pr['draft'], 'head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'][:9])
print('  mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'])
body = pr.get('body') or ''
open(os.path.join(G, 'gh', 'pr873_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), 'at-signs', body.count('@'), 'ack:schemathesis', body.count('<!--ack:schemathesis-->'), 'ack:akto', body.count('<!--ack:akto-->'), 'ticked [x]', body.count('- [x]'), 'unticked [ ]', body.count('- [ ]'), 'Test Evidence', body.count('## Test Evidence'), 'pending author confirmation', body.count('pending author confirmation'), 'Closes KS-931', body.count('Closes KS-931'))
files = get('/pulls/873/files?per_page=100'); save('pr873_files.json', files)
print('  files:', [(f['filename'].split('/')[-1], f['additions'], f['deletions'], f['sha'][:9]) for f in files])
commits = get('/pulls/873/commits?per_page=100'); save('pr873_commits.json', commits)
print('  commits:', [(c['sha'][:9], [p['sha'][:9] for p in c['parents']], c['commit']['message'].split('\n')[0][:70]) for c in commits])
for base in ('develop', '852e1fff773bd358170c11334d59496f05fdd8a7', 'bc067e3e91821116f3344b2aa5a1d7a5cc968d18'):
    c = get('/compare/' + base + '...' + pr['head']['sha']); save('compare_%s.json' % base[:9], c)
    print('  compare %s...head: merge_base %s status %s ahead %d behind %d files %d' % (base[:9], c['merge_base_commit']['sha'][:9], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])), [(f['filename'].split('/')[-1], f['sha'][:9]) for f in (c.get('files') or [])])
revs = get('/pulls/873/reviews?per_page=100'); save('pr873_reviews.json', revs)
for r in revs:
    print('  review', r['id'], r['state'], r['user']['login'], r['submitted_at'], 'commit', (r.get('commit_id') or '')[:9], 'body chars', len(r.get('body') or ''))
rcs = get('/pulls/873/comments?per_page=100'); save('pr873_review_comments.json', rcs)
print('  review comments', len(rcs), [(c['id'], c['user']['login'], c['path'].split('/')[-1], c.get('line'), c.get('original_line'), (c.get('commit_id') or '')[:9]) for c in rcs])
ics = get('/issues/873/comments?per_page=100'); save('pr873_issue_comments.json', ics)
for c in ics:
    print('  issue comment', c['id'], c['user']['login'], c['created_at'], 'chars', len(c['body']), 'at-signs', c['body'].count('@'))
for ref in ('develop',):
    b = get('/branches/' + ref); print('  branch', ref, b['commit']['sha'])
