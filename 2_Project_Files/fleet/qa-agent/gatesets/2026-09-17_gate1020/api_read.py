#!/usr/bin/env python3
"""api_read.py — READ-ONLY GitHub + Linear reads for the #1020 (KS-769 fuse re-date) tier-2 gate set. GH_TOKEN / LINEAR_API_KEY by NAME
from the Secuura .env, never printed. GET / GraphQL queries only. Closing-phrase regex has a planted positive control."""
import json, os, re, urllib.request, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1020'
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
vals = {}
for line in open(ENV, encoding='utf-8'):
    for k in ('GH_TOKEN', 'LINEAR_API_KEY'):
        if line.startswith(k + '='): vals[k] = line.split('=', 1)[1].strip().strip('"').strip("'")
assert vals.get('GH_TOKEN') and vals.get('LINEAR_API_KEY'), 'keys not found by name'
print('GH_TOKEN: set | LINEAR_API_KEY: set')
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + vals['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(name, obj): open(os.path.join(G, 'gh', name), 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd]|ing)?|resolve[sd]?|resolving|complete[sd]?|completing|implement(?:s|ed|ing)?)\s*:?\s+(?:#\d+|[A-Z]{2,}-\d+|https?://\S*(?:linear\.app|github\.com)\S*)')
assert CLOSE.findall('Fixes KS-769') and CLOSE.findall('closes #12'), 'closing regex control failed'
assert not CLOSE.findall('Refs KS-769'), 'closing regex negative control failed'
print('closing-phrase regex: planted controls "Fixes KS-769", "closes #12" -> hit; "Refs KS-769" -> no hit')
H = '71bd80a35b406b9c99c7b96955a7521032d33c20'
N = 1020
print('api_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
pr = get('/pulls/%d' % N); save('pr1020.json', pr)
print('PR #1020', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], 'author', pr['user']['login'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'], '| title closing', CLOSE.findall(pr['title']))
print('  commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'], '| mergeable_state', pr.get('mergeable_state'))
body = pr.get('body') or ''
open(os.path.join(G, 'gh', 'pr1020_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), '| closing phrases', CLOSE.findall(body), '| KS ids', sorted(set(re.findall(r'KS-[0-9]+', body))), '| "Refs KS-769"', body.count('Refs KS-769'))
files = get('/pulls/%d/files?per_page=100' % N); save('pr1020_files.json', files)
mine = set()
for f in files: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'][:9], f['filename']); mine.add(f['filename'])
commits = get('/pulls/%d/commits?per_page=100' % N); save('pr1020_commits.json', commits)
for c in commits: print('  commit', c['sha'][:9], 'parents', [p['sha'][:9] for p in c['parents']], '| message closing phrases', CLOSE.findall(c['commit']['message']))
c = get('/compare/develop...' + H)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/%d/reviews' % N)), '| review comments', len(get('/pulls/%d/comments' % N)))
for x in get('/issues/%d/comments?per_page=100' % N): print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'closing', CLOSE.findall(x['body']))
print('  develop (branches API)', get('/branches/develop')['commit']['sha'])
AUDIT = 'Blockchain/Dev/scripts/audit/'
for p in get('/pulls?state=open&per_page=100'):
    if p['number'] == N: continue
    names = {f['filename'] for f in get('/pulls/%d/files?per_page=100' % p['number'])}
    print('  open #%d head %s files %d | SHARED with #1020: %s | scripts/audit files: %s | preflight files: %d | %s' % (p['number'], p['head']['sha'][:9], len(names), sorted(names & mine), sorted(n.replace(AUDIT, '') for n in names if n.startswith(AUDIT)), sum(1 for n in names if '/scripts/preflight/' in n or n == '.githooks/pre-push'), p['title'][:60]))
def gql(q, v):
    return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': vals['LINEAR_API_KEY'], 'Content-Type': 'application/json'}), timeout=60))
print('linear read', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
for u in ('https://github.com/Secuura/Distributed_Secuura/pull/1020', 'https://github.com/Secuura/Distributed_Secuura/pull/99999'):
    d = gql('query($u:String!){ attachmentsForURL(url:$u){ nodes{ url metadata createdAt issue{ identifier state{name} } } } }', {'u': u})
    ns = d.get('data', {}).get('attachmentsForURL', {}).get('nodes') if 'errors' not in d else None
    print('attachmentsForURL', u.rsplit('/', 1)[1], 'ERRORS' if ns is None else len(ns), d.get('errors', ''))
    for a in ns or []: print('   on %s [%s] linkKind=%r status=%r' % (a['issue']['identifier'], a['issue']['state']['name'], (a.get('metadata') or {}).get('linkKind'), (a.get('metadata') or {}).get('status')))
i = gql('query($id:String!){ issue(id:$id){ identifier title state{name type} completedAt attachments{nodes{url metadata}} comments(first:100){nodes{id createdAt}} } }', {'id': 'KS-769'})['data']['issue']
json.dump(i, open(G + '/linear/KS-769.json', 'w'), indent=1)
print('KS-769', repr(i['title'][:80]), 'state', i['state'], 'completedAt', i['completedAt'], 'attachments', [(a['url'].rsplit('/', 1)[1], (a['metadata'] or {}).get('linkKind'), (a['metadata'] or {}).get('status')) for a in i['attachments']['nodes']], '| comments', len(i['comments']['nodes']))
