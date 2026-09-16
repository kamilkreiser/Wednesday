#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub reads for the #1001 (KS-1165) tier-1 gate set. GH_TOKEN by NAME from the Secuura .env; never printed. GET only."""
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
H = '3925d4c072b940eb91de462b7b92eabfe8889c75'
print('gh_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
pr = get('/pulls/1001'); save('pr1001.json', pr)
print('PR #1001', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], 'author', pr['user']['login'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'])
print('  mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'])
body = pr.get('body') or ''
open(os.path.join(G, 'gh', 'pr1001_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), 'at-signs', body.count('@'), 'ack:schemathesis', body.count('<!--ack:schemathesis-->'), 'ack:akto', body.count('<!--ack:akto-->'), 'ticked [x]', body.count('- [x]'), 'unticked [ ]', body.count('- [ ]'), 'Test Evidence', body.count('## Test Evidence'), 'Closes KS-1165', body.count('Closes KS-1165'), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', body))))
files = get('/pulls/1001/files?per_page=100'); save('pr1001_files.json', files)
for f in files: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
commits = get('/pulls/1001/commits?per_page=100'); save('pr1001_commits.json', commits)
for c in commits: print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], c['commit']['message'].split('\n')[0][:120])
c = get('/compare/develop...' + H); save('compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/1001/reviews')), '| review comments', len(get('/pulls/1001/comments')))
ics = get('/issues/1001/comments?per_page=100'); save('pr1001_issue_comments.json', ics)
for x in ics: print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'at-signs', x['body'].count('@'))
b = get('/branches/develop'); print('  develop (branches API)', b['commit']['sha'])
for n in (999, 1000):
    p = get('/pulls/%d' % n); pf = get('/pulls/%d/files?per_page=100' % n)
    print('  sibling #%d state %s head %s files %s' % (n, p['state'], p['head']['sha'][:9], [f['filename'].replace('Blockchain/Dev/', '') for f in pf]))
