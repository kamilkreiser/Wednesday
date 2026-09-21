#!/usr/bin/env python3
"""api_read_gate1036.py — READ-ONLY GitHub + Linear reads for the #1036 (KS-763 PR-4, qs in range on express 4) tier-1 gate set. Copied from
gatesets/2026-09-17_gate1033/api_read_1033.py. GH_TOKEN / LINEAR_API_KEY by NAME from the Secuura .env, never printed. GET / GraphQL queries only.
Closing-phrase regex has planted positive and negative controls. Usage: api_read_gate1036.py <head> <develop>"""
import json, os, re, sys, urllib.request, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate1036_ks763'
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
assert CLOSE.findall('Fixes KS-763') and CLOSE.findall('closes #12') and CLOSE.findall('Resolves KS-775'), 'closing regex control failed'
assert not CLOSE.findall('Refs KS-763') and not CLOSE.findall('Refs KS-775'), 'closing regex negative control failed'
print('closing-phrase regex: planted controls "Fixes KS-763", "closes #12", "Resolves KS-775" -> hit; "Refs KS-763", "Refs KS-775" -> no hit')
H, DEV = sys.argv[1], sys.argv[2]
N = 1036
print('api_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
pr = get('/pulls/%d' % N); save('pr1036.json', pr)
print('PR #1036', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], 'author', pr['user']['login'], '| head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  head == pin:', pr['head']['sha'] == H, '| title:', pr['title'], '| title len', len(pr['title']), '| title closing', CLOSE.findall(pr['title']))
print('  commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']), '| review_comments', pr['review_comments'], 'comments', pr['comments'], '| mergeable', pr.get('mergeable'), 'mergeable_state', pr.get('mergeable_state'), '| updated_at', pr['updated_at'])
body = pr.get('body') or ''
open(os.path.join(G, 'out', 'gh', 'pr1036_body.md'), 'w', encoding='utf-8').write(body)
print('  body chars', len(body), '| closing phrases', CLOSE.findall(body), '| KS ids', sorted(set(re.findall(r'KS-[0-9]+', body))), '| "Refs KS-763"', body.count('Refs KS-763'), '| "Refs KS-775"', body.count('Refs KS-775'), '| "all 3 rows"', body.count('all 3 rows'), '| "express 5"', body.lower().count('express 5'), '| doubled comma ",,"', body.count(',,'))
files = get('/pulls/%d/files?per_page=100' % N); save('pr1036_files.json', files)
mine = set(); st = {}
for f in files: mine.add(f['filename']); st[f['status']] = st.get(f['status'], 0) + 1
print('  files API:', len(files), 'status', st, '| locks', sum(1 for f in mine if f.endswith('package-lock.json')), 'manifests', sum(1 for f in mine if f.endswith('package.json')), 'other', sorted(f for f in mine if not f.endswith('package-lock.json') and not f.endswith('package.json')))
print('  +/- from files API: +%d -%d' % (sum(f['additions'] for f in files), sum(f['deletions'] for f in files)))
commits = get('/pulls/%d/commits?per_page=100' % N); save('pr1036_commits.json', commits)
for c in commits:
    subj = c['commit']['message'].splitlines()[0]
    print('  commit', c['sha'][:9], 'parents', [p['sha'][:9] for p in c['parents']], '| message closing phrases', CLOSE.findall(c['commit']['message']), '| subject len', len(subj), 'ascii', subj.isascii(), '|', subj[:100])
c = get('/compare/develop...' + H)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d (compare API caps files at 300)' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('  reviews', len(get('/pulls/%d/reviews' % N)), '| review comments', len(get('/pulls/%d/comments' % N)))
for x in get('/issues/%d/comments?per_page=100' % N): print('  issue comment', x['id'], x['user']['login'], x['created_at'], 'chars', len(x['body']), 'closing', CLOSE.findall(x['body']))
bd = get('/branches/develop')['commit']['sha']
print('  develop (branches API)', bd, '| == the pin', DEV, '?', bd == DEV)
opens = get('/pulls?state=open&per_page=100'); save('open_prs.json', [{'number': p['number'], 'user': p['user']['login'], 'head': p['head']['sha'], 'title': p['title'], 'updated_at': p['updated_at']} for p in opens])
print('  open PRs', len(opens))
overlap = []
for p in opens:
    if p['number'] == N: continue
    names = {f['filename'] for f in get('/pulls/%d/files?per_page=100' % p['number'])}
    shared = sorted(n.replace('Blockchain/Dev/', '') for n in names & mine)
    if shared:
        overlap.append(p['number'])
        print('  open #%d %s head %s | SHARED with #1036 (%d): %s | %s' % (p['number'], p['user']['login'], p['head']['sha'][:9], len(shared), shared[:6], p['title'][:70]))
print('  OVERLAP set:', sorted(overlap), '| the READY named: #949 #948 #947 #946 #945 #649 #639 #635 #575 #572 | equal?', sorted(overlap) == sorted([949, 948, 947, 946, 945, 649, 639, 635, 575, 572]))
print('  other open PRs touching audit-baseline.json:', [p['number'] for p in opens if p['number'] != N and any(f['filename'].endswith('audit-baseline.json') for f in get('/pulls/%d/files?per_page=100' % p['number']))])
def gql(q, v):
    return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': vals['LINEAR_API_KEY'], 'Content-Type': 'application/json'}), timeout=60))
print('linear read', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
for u in ('https://github.com/Secuura/Distributed_Secuura/pull/1036', 'https://github.com/Secuura/Distributed_Secuura/pull/1033', 'https://github.com/Secuura/Distributed_Secuura/pull/99999'):
    d = gql('query($u:String!){ attachmentsForURL(url:$u){ nodes{ url metadata createdAt issue{ identifier state{name} } } } }', {'u': u})
    ns = d.get('data', {}).get('attachmentsForURL', {}).get('nodes') if 'errors' not in d else None
    print('attachmentsForURL', u.rsplit('/', 1)[1], 'ERRORS' if ns is None else len(ns), d.get('errors', ''))
    for a in ns or []: print('   on %s [%s] linkKind=%r status=%r' % (a['issue']['identifier'], a['issue']['state']['name'], (a.get('metadata') or {}).get('linkKind'), (a.get('metadata') or {}).get('status')))
WANT_COMMENTS = {'KS-775': '09d6f7c6-eb10-4e1f-8f98-16bf8254b689', 'KS-763': '1b1eb4d3-aa0f-4e38-8e70-9fbcb407a787'}
for tid in ('KS-763', 'KS-775'):
    i = gql('query($id:String!){ issue(id:$id){ identifier title state{name type} completedAt archivedAt assignee{name} attachments{nodes{url metadata}} comments(first:100){nodes{id createdAt body}} } }', {'id': tid})['data']['issue']
    json.dump(i, open(G + '/out/linear/%s.json' % tid, 'w'), indent=1)
    print(tid, repr(i['title'][:90]), 'state', i['state'], 'completedAt', i['completedAt'], 'archivedAt', i['archivedAt'], 'assignee', (i.get('assignee') or {}).get('name'), 'attachments', [(a['url'].rsplit('/', 1)[1], (a['metadata'] or {}).get('linkKind'), (a['metadata'] or {}).get('status')) for a in i['attachments']['nodes']], '| comments', len(i['comments']['nodes']))
    cm = [x for x in i['comments']['nodes'] if x['id'] == WANT_COMMENTS[tid]]
    print('  the READY-named comment', WANT_COMMENTS[tid][:8], 'present:', bool(cm), '| body:', repr(cm[0]['body'][:200]) if cm else '-', '| createdAt', cm[0]['createdAt'] if cm else '-')
    if tid == 'KS-775' and cm: print('  KS-775 body EXACTLY the READY string?', cm[0]['body'] == 'qs rows fixed in range on express 4; the express 5 migration ruled 2026-09-03 is unchanged')
for tid in ('KS-531',):
    d = gql('query($id:String!){ issue(id:$id){ identifier title state{name} completedAt archivedAt attachments{nodes{url metadata}} } }', {'id': tid})
    x = (d.get('data') or {}).get('issue')
    if x: print('ISSUE', tid, repr(x['title'][:80]), x['state']['name'], 'completedAt', x['completedAt'], 'archivedAt', x['archivedAt'], 'attachments to pull/1036:', [a['url'] for a in x['attachments']['nodes'] if a['url'].endswith('/pull/1036')])
    else: print('ISSUE', tid, 'not returned', [e.get('message') for e in d.get('errors', [])])
for tid in ('KS-763', 'KS-775'):
    h = gql('query($id:String!){ issue(id:$id){ history(first:50){ nodes{ createdAt botActor{name} fromState{name} toState{name} } } } }', {'id': tid})
    for x in (h.get('data') or {}).get('issue', {}).get('history', {}).get('nodes', []):
        if x.get('toState'): print('  %s history' % tid, x['createdAt'], (x.get('botActor') or {}).get('name'), (x.get('fromState') or {}).get('name'), '->', x['toState']['name'])
print('done', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
