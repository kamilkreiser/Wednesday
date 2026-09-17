#!/usr/bin/env python3
"""api_read_1029.py — READ-ONLY GitHub GETs + Linear queries for the #1029 (KS-1180 part 1) TIER 2 drafter. Copied from gate1018/gh_read_r2.py +
linear_read_r2.py (asserted re-pointing only: H, N, the tickets, the controls, out/). Keys by NAME (GH_TOKEN, LINEAR_API_KEY) from the Secuura .env;
read transiently, never printed or written (only 'set: True/False'). GitHub: GET only. Linear: query only.
GitHub: PR 1029 (head, base, state, mergeable, title, body), files, commits (closing-phrase scan, planted controls), compare develop...head, reviews and
comments, develop tip, blobs at develop + head for argv[1] (comma list relative to Blockchain/Dev/), open PRs + overlap with #1029's file and api-gateway.
Linear: KS-1180 and KS-1073 (state, attachments linkKind, comments whole), attachmentsForURL pull/1029 + controls pull/1028 and pull/99999."""
import json, os, re, sys, time, urllib.request, urllib.error, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1029'
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
K = {}
for line in open(ENV, encoding='utf-8'):
    for n in ('GH_TOKEN', 'LINEAR_API_KEY'):
        if line.startswith(n + '='): K[n] = line.split('=', 1)[1].strip().strip('"').strip("'")
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
print('api_read_1029', now(), '| keys set:', {n: bool(K.get(n)) for n in ('GH_TOKEN', 'LINEAR_API_KEY')})
assert K.get('GH_TOKEN') and K.get('LINEAR_API_KEY')
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + K['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(sub, n, o): open(os.path.join(G, 'out', sub, n), 'w', encoding='utf-8').write(o if isinstance(o, str) else json.dumps(o, indent=1, ensure_ascii=False))
H = 'cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc'; N = '1029'
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?)\b[:\s]+(?:KS-[0-9]+|#[0-9]+)')
ctl = [len(CLOSE.findall(x)) for x in ('Fixes KS-1180', 'closes #1029', 'Resolves: KS-1180', 'Refs KS-1180', 'Refs KS-1180 (P-1016-1, P-1016-2)')]
print('closing-phrase regex controls', ctl); assert ctl == [1, 1, 1, 0, 0]
pr = get('/pulls/' + N)
for _ in range(4):
    if pr.get('mergeable') is not None: break
    time.sleep(3); pr = get('/pulls/' + N)
save('gh', 'pr1029.json', pr); body = pr.get('body') or ''; save('gh', 'pr1029_body.md', body)
print('PR #1029', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], '| head', pr['head']['sha'], '== pin', pr['head']['sha'] == H, pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  title:', pr['title'], '| title closing', CLOSE.findall(pr['title']), '| mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']))
print('  body chars', len(body), 'at-signs', body.count('@'), 'closing', CLOSE.findall(body), 'KS ids', {k: len(re.findall(re.escape(k) + r'(?![0-9])', body)) for k in sorted(set(re.findall(r'KS-[0-9]+', body)))},
      '| linear URLs', re.findall(r'https://linear\.app/\S+', body)[:4])
files = get('/pulls/' + N + '/files?per_page=100'); save('gh', 'pr1029_files.json', files); mine = set()
for f in files: mine.add(f['filename']); print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
commits = get('/pulls/' + N + '/commits?per_page=100'); save('gh', 'pr1029_commits.json', commits)
for c in commits: print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'closing', CLOSE.findall(c['commit']['message']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', c['commit']['message']))), '|', c['commit']['message'].split('\n')[0][:100])
c = get('/compare/develop...' + H); save('gh', 'compare_develop_head.json', {k: c[k] for k in ('status', 'ahead_by', 'behind_by', 'total_commits')} | {'merge_base': c['merge_base_commit']['sha'], 'files': [(x['filename'], x['sha']) for x in c.get('files') or []]})
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
ic = get('/issues/' + N + '/comments'); save('gh', 'pr1029_issue_comments.json', ic)
print('  reviews', len(get('/pulls/' + N + '/reviews')), '| review comments', len(get('/pulls/' + N + '/comments')), '| issue comments', len(ic), [(x['user']['login'], CLOSE.findall(x['body']), x['body'].count('@')) for x in ic])
dev = get('/branches/develop')['commit']['sha']; print('  develop (branches API)', dev)
D = 'Blockchain/Dev/'
if len(sys.argv) > 1 and sys.argv[1]:
    for f in sys.argv[1].split(','):
        row = {}
        for ref in (dev, H):
            try: row[ref[:9]] = get('/contents/' + D + f + '?ref=' + ref)['sha']
            except urllib.error.HTTPError as e: row[ref[:9]] = 'ABSENT' if e.code == 404 else 'HTTP%d' % e.code
        print('  blob %-90s develop %s head %s' % (f, row[dev[:9]], row[H[:9]]))
    for ref in (dev, H):
        src = [x for x in get('/contents/' + D + 'packages/shared?ref=' + ref) if x['name'] == 'src']
        print('  packages/shared/src tree @', ref[:9], src[0]['sha'] if src else 'ABSENT')
opn = get('/pulls?state=open&per_page=100'); print('  open PRs:', len(opn), sorted(p['number'] for p in opn))
for p in opn:
    if p['number'] == int(N): continue
    fs = {f['filename'] for f in get('/pulls/%d/files?per_page=100' % p['number'])}
    shared = sorted(fs & mine); gwf = sorted(x for x in fs if x.startswith(D + 'services/api-gateway/src/'))
    if shared or gwf: print('  overlap #%d shared %s | api-gateway/src files %d %s' % (p['number'], shared, len(gwf), gwf[:6]))
# ---- Linear (query only)
def gql(q, v): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': K['LINEAR_API_KEY'], 'Content-Type': 'application/json'}), timeout=60))
Q = '''query($id:String!){ issue(id:$id){ identifier title state{name type} priority archivedAt completedAt updatedAt startedAt branchName description relations{nodes{type relatedIssue{identifier}}} attachments{nodes{url title metadata createdAt updatedAt}} comments(first:100){nodes{id createdAt body user{name} botActor{name}}} history(first:30){nodes{createdAt fromState{name} toState{name} actor{name} botActor{name}}} } }'''
print('linear read at', now())
for n in ('KS-1180', 'KS-1073'):
    d = gql(Q, {'id': n})
    if 'errors' in d: print(n, 'ERRORS', d['errors']); continue
    i = d['data']['issue']; save('linear', n + '.json', i)
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    print(f"{n}: state={i['state']['name']}/{i['state']['type']} completedAt={i['completedAt']} comments={len(cs)} branch={i['branchName']!r} relations={[r['type']+':'+r['relatedIssue']['identifier'] for r in i['relations']['nodes']]} title={i['title'][:140]!r}")
    for h in i['history']['nodes']:
        if h.get('toState'): print(f"   history {h['createdAt']} {(h.get('fromState') or {}).get('name')} -> {h['toState']['name']} actor={(h.get('actor') or {}).get('name')} bot={(h.get('botActor') or {}).get('name')}")
    for a in i['attachments']['nodes']:
        md = a.get('metadata') or {}; print(f"   attachment {a['url']} linkKind={md.get('linkKind')!r} status={md.get('status')!r} created={a['createdAt']}")
    with open(f'{G}/out/linear/{n}.comments.md', 'w', encoding='utf-8') as fh:
        fh.write('# DESCRIPTION\n' + (i.get('description') or '') + '\n')
        for c in cs:
            who = (c.get('user') or {}).get('name') or (c.get('botActor') or {}).get('name')
            fh.write(f"\n\n# COMMENT {c['id']} {c['createdAt']} {who}\n{c['body']}\n")
            print(f"   comment {c['id'][:8]} {c['createdAt']} {who} chars={len(c['body'])} names#1029={'#1029' in c['body'] or 'pull/1029' in c['body']} first={c['body'][:90]!r}")
AQ = '''query($u:String!){ attachmentsForURL(url:$u){ nodes{ url metadata createdAt issue{ identifier state{name} } } } }'''
for u in ['https://github.com/Secuura/Distributed_Secuura/pull/1029', 'https://github.com/Secuura/Distributed_Secuura/pull/1028', 'https://github.com/Secuura/Distributed_Secuura/pull/99999']:
    d = gql(AQ, {'u': u}); ns = d['data']['attachmentsForURL']['nodes']; print(f"attachmentsForURL {u.rsplit('/',1)[1]}: {len(ns)}")
    for a in ns:
        md = a.get('metadata') or {}; print(f"   on {a['issue']['identifier']} [{a['issue']['state']['name']}] linkKind={md.get('linkKind')!r} created={a['createdAt']}")
print('api_read_1029 end', now())
