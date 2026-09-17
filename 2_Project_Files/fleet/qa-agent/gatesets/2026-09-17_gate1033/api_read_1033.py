#!/usr/bin/env python3
"""api_read_1033.py — READ-ONLY GitHub + Linear reads for the #1033 (KS-763 PR-7, mysql2 override 3.23.1) tier-1 gate set. Copied from
api_read_1030.py. GH_TOKEN / LINEAR_API_KEY by NAME from the Secuura .env, never printed. GET / GraphQL queries only. Closing-phrase regex has
planted positive and negative controls."""
import json, os, re, urllib.request, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1033'
os.makedirs(G + '/out/gh', exist_ok=True); os.makedirs(G + '/out/linear', exist_ok=True)
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
def save(name, obj): open(os.path.join(G, 'out', 'gh', name), 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd]|ing)?|resolve[sd]?|resolving|complete[sd]?|completing|implement(?:s|ed|ing)?)\s*:?\s+(?:#\d+|[A-Z]{2,}-\d+|https?://\S*(?:linear\.app|github\.com)\S*)')
assert CLOSE.findall('Fixes KS-763') and CLOSE.findall('closes #12') and CLOSE.findall('Resolves KS-751'), 'closing regex control failed'
assert not CLOSE.findall('Refs KS-763') and not CLOSE.findall('Refs KS-751'), 'closing regex negative control failed'
print('closing-phrase regex: planted controls "Fixes KS-763", "closes #12", "Resolves KS-751" -> hit; "Refs KS-763", "Refs KS-751" -> no hit')
H = '2cab54988b4e7b71d403576719f5fd80e470fa92'
N = 1033
print('api_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
pr = get('/pulls/%d' % N); save('pr1033.json', pr)
print('PR #1033', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], 'author', pr['user']['login'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'], '| title closing', CLOSE.findall(pr['title']))
print('  commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'], '| mergeable_state', pr.get('mergeable_state'))
body = pr.get('body') or ''
open(os.path.join(G, 'out', 'gh', 'pr1033_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), '| closing phrases', CLOSE.findall(body), '| KS ids', sorted(set(re.findall(r'KS-[0-9]+', body))), '| "Refs KS-763"', body.count('Refs KS-763'), '| "not a claim about other runtimes"', body.count('not a claim about other runtimes'))
files = get('/pulls/%d/files?per_page=100' % N); save('pr1033_files.json', files)
mine = set()
for f in files: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'][:9], 'patch' if f.get('patch') else 'NO-PATCH', f['filename']); mine.add(f['filename'])
commits = get('/pulls/%d/commits?per_page=100' % N); save('pr1033_commits.json', commits)
for c in commits: print('  commit', c['sha'][:9], 'parents', [p['sha'][:9] for p in c['parents']], '| message closing phrases', CLOSE.findall(c['commit']['message']), '| first line', c['commit']['message'].splitlines()[0][:100])
c = get('/compare/develop...' + H)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/%d/reviews' % N)), '| review comments', len(get('/pulls/%d/comments' % N)))
for x in get('/issues/%d/comments?per_page=100' % N): print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'closing', CLOSE.findall(x['body']))
print('  develop (branches API)', get('/branches/develop')['commit']['sha'])
WATCH = {'Blockchain/Dev/package-lock.json', 'Blockchain/Dev/package.json', 'Blockchain/Dev/scripts/audit/audit-baseline.json', 'Blockchain/Dev/services/originate/package-lock.json', 'Blockchain/Dev/services/originate/package.json'}
assert mine == WATCH, 'PR files list is not the 5 expected (%d)' % len(mine)
opens = get('/pulls?state=open&per_page=100')
print('  open PRs', len(opens))
for p in opens:
    if p['number'] == N: continue
    names = {f['filename'] for f in get('/pulls/%d/files?per_page=100' % p['number'])}
    shared = sorted(n.replace('Blockchain/Dev/', '') for n in names & mine)
    if shared: print('  open #%d %s head %s | SHARED with #1033: %s | %s' % (p['number'], p['user']['login'], p['head']['sha'][:9], shared, p['title'][:70]))
def gql(q, v):
    return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': vals['LINEAR_API_KEY'], 'Content-Type': 'application/json'}), timeout=60))
print('linear read', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
for u in ('https://github.com/Secuura/Distributed_Secuura/pull/1033', 'https://github.com/Secuura/Distributed_Secuura/pull/1030', 'https://github.com/Secuura/Distributed_Secuura/pull/99999'):
    d = gql('query($u:String!){ attachmentsForURL(url:$u){ nodes{ url metadata createdAt issue{ identifier state{name} } } } }', {'u': u})
    ns = d.get('data', {}).get('attachmentsForURL', {}).get('nodes') if 'errors' not in d else None
    print('attachmentsForURL', u.rsplit('/', 1)[1], 'ERRORS' if ns is None else len(ns), d.get('errors', ''))
    for a in ns or []: print('   on %s [%s] linkKind=%r status=%r' % (a['issue']['identifier'], a['issue']['state']['name'], (a.get('metadata') or {}).get('linkKind'), (a.get('metadata') or {}).get('status')))
i = gql('query($id:String!){ issue(id:$id){ identifier title state{name type} completedAt archivedAt attachments{nodes{url metadata}} comments(first:100){nodes{id createdAt body}} } }', {'id': 'KS-763'})['data']['issue']
json.dump(i, open(G + '/out/linear/KS-763.json', 'w'), indent=1)
print('KS-763', repr(i['title'][:90]), 'state', i['state'], 'completedAt', i['completedAt'], 'archivedAt', i['archivedAt'], 'attachments', [(a['url'].rsplit('/', 1)[1], (a['metadata'] or {}).get('linkKind'), (a['metadata'] or {}).get('status')) for a in i['attachments']['nodes']], '| comments', len(i['comments']['nodes']))
for cm in sorted(i['comments']['nodes'], key=lambda x: x['createdAt'])[-3:]: print('  comment', cm['id'][:8], cm['createdAt'], 'chars', len(cm['body']), '| names #1033', '#1033' in cm['body'] or 'pull/1033' in cm['body'], '| @', '@' in cm['body'], '|', cm['body'][:140].replace('\n', ' '))
for tid in ('KS-751', 'KS-775', 'KS-749'):
    d = gql('query($id:String!){ issue(id:$id){ identifier title state{name} completedAt archivedAt attachments{nodes{url metadata}} } }', {'id': tid})
    x = (d.get('data') or {}).get('issue')
    if x: print('ISSUE', tid, repr(x['title'][:80]), x['state']['name'], 'completedAt', x['completedAt'], 'archivedAt', x['archivedAt'], 'attachments to pull/1033:', [a['url'] for a in x['attachments']['nodes'] if a['url'].endswith('/pull/1033')])
    else: print('ISSUE', tid, 'not returned', [e.get('message') for e in d.get('errors', [])])
h = gql('query($id:String!){ issue(id:$id){ history(first:50){ nodes{ createdAt botActor{name} fromState{name} toState{name} } } } }', {'id': 'KS-763'})
for x in (h.get('data') or {}).get('issue', {}).get('history', {}).get('nodes', []):
    if x.get('toState'): print('  KS-763 history', x['createdAt'], (x.get('botActor') or {}).get('name'), (x.get('fromState') or {}).get('name'), '->', x['toState']['name'])
print('done', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
