#!/usr/bin/env python3
"""api_read_1028.py — READ-ONLY GitHub GETs + Linear queries for the #1028 (KS-744) TIER 1 drafter. Pattern: gate1023/api_read.py + gate1018/gh_read_r2.py
+ linear_read_r2.py. Keys by NAME (GH_TOKEN, LINEAR_API_KEY) from the Secuura .env; never printed (only 'set: True/False'). GitHub: GET only. Linear: query only.
GitHub: PR 1028 (head, base, state, mergeable, title, body), files, commits (closing-phrase scan with planted controls), compare develop...head, develop tip,
blobs at develop + head for argv[1] (comma list relative to Blockchain/Dev/), open PRs + overlap with services/api-gateway/ and packages/shared/.
Linear: KS-744 (state, branchName, attachments linkKind, comments, description), KS-1208, KS-1207, KS-1215; attachmentsForURL pull/1028 + controls
pull/1023 (KS-1207 contributes, merged) and pull/99999 (0). Raw JSON under out/gh and out/linear."""
import json, os, re, sys, time, urllib.request, urllib.error, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1028'
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
K = {}
for line in open(ENV, encoding='utf-8'):
    for n in ('GH_TOKEN', 'LINEAR_API_KEY'):
        if line.startswith(n + '='): K[n] = line.split('=', 1)[1].strip().strip('"').strip("'")
def now(): return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
print('api_read_1028', now(), '| keys set:', {n: bool(K.get(n)) for n in ('GH_TOKEN', 'LINEAR_API_KEY')})
assert K.get('GH_TOKEN') and K.get('LINEAR_API_KEY')
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def gh(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + K['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(sub, n, o): open(os.path.join(G, 'out', sub, n), 'w', encoding='utf-8').write(json.dumps(o, indent=1, ensure_ascii=False) if not isinstance(o, str) else o)
H = 'e39521cfb54cb5fd47c6bdae64ce707b3c9befce'; N = '1028'
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?)\b[:\s]+(?:KS-[0-9]+|#[0-9]+)')
ctl = [len(CLOSE.findall(x)) for x in ('Fixes KS-744', 'closes #1028', 'Resolves: KS-744', 'Refs KS-744', 'the fix for KS-744 is here')]
print('closing-phrase regex controls', ctl); assert ctl == [1, 1, 1, 0, 0]
pr = gh('/pulls/' + N)
for _ in range(4):
    if pr.get('mergeable') is not None: break
    time.sleep(3); pr = gh('/pulls/' + N)
save('gh', 'pr1028.json', pr); body = pr.get('body') or ''; save('gh', 'pr1028_body.md', body)
print('PR #1028', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], '| head', pr['head']['sha'], '== pin', pr['head']['sha'] == H, pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
print('  title:', repr(pr['title']), '| title closing', CLOSE.findall(pr['title']), '| mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']))
print('  body chars', len(body), 'at-signs', body.count('@'), 'closing', CLOSE.findall(body), 'KS ids', {k: len(re.findall(re.escape(k) + r'(?![0-9])', body)) for k in sorted(set(re.findall(r'KS-[0-9]+', body)))})
files = gh('/pulls/' + N + '/files?per_page=100'); save('gh', 'pr1028_files.json', files); mine = set()
for f in files: mine.add(f['filename']); print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
for c in gh('/pulls/' + N + '/commits?per_page=100'):
    print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'closing', CLOSE.findall(c['commit']['message']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', c['commit']['message']))), '|', c['commit']['message'].split('\n')[0][:110])
c = gh('/compare/develop...' + H); save('gh', 'compare_develop_head.json', c)
print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d %s' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or []), [(f['filename'].split('/')[-1], f['sha'][:9]) for f in c.get('files') or []]))
print('  reviews', len(gh('/pulls/' + N + '/reviews')), '| review comments', len(gh('/pulls/' + N + '/comments')), '| issue comments', len(gh('/issues/' + N + '/comments')))
dev = gh('/branches/develop')['commit']['sha']; print('  develop (branches API)', dev)
D = 'Blockchain/Dev/'
if len(sys.argv) > 1 and sys.argv[1]:
    for f in sys.argv[1].split(','):
        row = {}
        for ref in (dev, H):
            try: row[ref] = gh('/contents/' + D + f + '?ref=' + ref)['sha']
            except urllib.error.HTTPError as e: row[ref] = 'ABSENT' if e.code == 404 else 'HTTP%d' % e.code
        print('  blob %-100s develop %s head %s %s' % (f, row[dev], row[H], 'SAME' if row[dev] == row[H] else 'DIFF'))
opn = gh('/pulls?state=open&per_page=100'); print('  open PRs:', len(opn), sorted(p['number'] for p in opn))
for p in opn:
    if p['number'] == int(N): continue
    fs = {f['filename'] for f in gh('/pulls/%d/files?per_page=100' % p['number'])}
    gw = sorted(x for x in fs if x.startswith(D + 'services/api-gateway/') or x.startswith(D + 'packages/shared/'))
    print('  open #%d head %s files %d | shared-with-1028 %s | api-gateway/shared files %d %s' % (p['number'], p['head']['sha'][:9], len(fs), sorted(fs & mine), len(gw), gw[:6]))
L = K['LINEAR_API_KEY']
def gql(q, v): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': L, 'Content-Type': 'application/json'}), timeout=60))
Q = '''query($id:String!){ issue(id:$id){ identifier title state{name type} priority branchName description updatedAt relations{nodes{type relatedIssue{identifier}}} attachments{nodes{url metadata createdAt}} comments(first:100){nodes{id createdAt body user{name} botActor{name}}} history(first:30){nodes{createdAt fromState{name} toState{name} actor{name}}} } }'''
print('linear read at', now())
for n in ('KS-744', 'KS-1208', 'KS-1207', 'KS-1215'):
    d = gql(Q, {'id': n})
    if 'errors' in d: print(n, 'ERRORS', d['errors']); continue
    i = d['data']['issue']; save('linear', n + '.json', i)
    cs = sorted(i['comments']['nodes'], key=lambda z: z['createdAt'])
    print(f"{n}: state={i['state']['name']}/{i['state']['type']} prio={i['priority']} comments={len(cs)} branch={i['branchName']!r} relations={[r['type']+':'+r['relatedIssue']['identifier'] for r in i['relations']['nodes']]} title={i['title'][:130]!r}")
    for a in i['attachments']['nodes']: print(f"   attachment {a['url']} linkKind={(a.get('metadata') or {}).get('linkKind')!r} created={a['createdAt']}")
    for h in i['history']['nodes']:
        if h.get('toState'): print(f"   history {h['createdAt']} {(h.get('fromState') or {}).get('name')} -> {h['toState']['name']} actor={(h.get('actor') or {}).get('name')}")
    with open(f'{G}/out/linear/{n}.comments.md', 'w', encoding='utf-8') as fh:
        fh.write('# DESCRIPTION\n' + (i.get('description') or '') + '\n')
        for cm in cs:
            who = (cm.get('user') or {}).get('name') or (cm.get('botActor') or {}).get('name')
            fh.write(f"\n\n# COMMENT {cm['id']} {cm['createdAt']} {who}\n{cm['body']}\n")
            print(f"   comment {cm['id'][:8]} {cm['createdAt']} {who} chars={len(cm['body'])} closing={CLOSE.findall(cm['body'])} first={cm['body'][:90]!r}")
AQ = '''query($u:String!){ attachmentsForURL(url:$u){ nodes{ url metadata createdAt issue{ identifier state{name} } } } }'''
for u in ('1028', '1023', '99999'):
    d = gql(AQ, {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/' + u}); ns = d['data']['attachmentsForURL']['nodes']
    print(f"attachmentsForURL pull/{u}: {len(ns)} {[(a['issue']['identifier'], a['issue']['state']['name'], (a.get('metadata') or {}).get('linkKind')) for a in ns]}")
print('api_read_1028 end', now())
