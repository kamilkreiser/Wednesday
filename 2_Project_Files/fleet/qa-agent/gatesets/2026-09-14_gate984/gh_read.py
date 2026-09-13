#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #984 (KS-835) TIER-1 gate set. Token sourced by NAME (GH_TOKEN)
from the Secuura .env; never printed. Writes raw JSON under <G>/gh/ and the touched files' bytes under <G>/model/gh_*."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
HEAD = 'd00a2015c89a4720eaeab64482bbd9b89d878024'   # #984 head
P983 = 'f62c975c11ec97cdef04500fd98a43618e702763'   # #983 head = #984's parent
P982 = 'e62eab87a6263e25c41c9bb814d5831842bb6c7e'   # #982 head = #983's parent
M18 = '8861e62161466c40f08d2b10a30edeb203123993'    # origin develop at the builder's cut
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='):
        tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
print('GH_TOKEN: set' if tok else 'GH_TOKEN: unset')
base = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    r = urllib.request.urlopen(urllib.request.Request(base + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60)
    return json.load(r)
def save(name, obj):
    open(f'{G}/gh/{name}', 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
def atclass(b):
    cls = {'array': 0, 'prep': 0, 'email': 0, 'idiom': 0, 'mention': 0, 'other': 0}
    for m in re.finditer(r'@', b):
        i = m.start(); pre = b[max(0, i-1):i]; post = b[i+1:i+2]
        if pre == '[' and post == ']': cls['array'] += 1
        elif pre == ' ' and post == ' ': cls['prep'] += 1
        elif pre == ' ' and post == '`': cls['idiom'] += 1
        elif re.match(r'[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[a-z]{2,}', b[max(0, i-40):i+40]) and pre not in (' ', '\n', '(', '`'): cls['email'] += 1
        elif re.match(r'@[A-Za-z0-9][A-Za-z0-9-]*', b[i:i+40]) and pre in (' ', '\n', '(', '', ':'): cls['mention'] += 1
        else: cls['other'] += 1
    return cls
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '/', datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%SZ'))
print('classifier positive control:', atclass('hi @kksecura and a[@] and PR #984 @ `sha` and x@y.com'))
for n in (984, 983, 982):
    pr = get(f'/pulls/{n}'); save(f'pr{n}.json', pr)
    print(f"PR #{n}: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} BASE={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:140]!r}")
    body = pr['body'] or ''
    open(f'{G}/gh/pr{n}_body.md', 'w', encoding='utf-8').write(body)
    print(f"  body chars={len(body)} at-signs={body.count('@')} classes={atclass(body)} KS={sorted(set(re.findall(r'KS-\d+', body)))} PRrefs={sorted(set(re.findall(r'#\d{3,4}', body)))}")
    print('  headings:', [l for l in body.splitlines() if l.startswith('#')])
    if n == 984:
        for t in ['d00a2015c', 'f62c975c1', 'e62eab87a', '#983', '#982', 'H1', 'H2', 'H3', '53/707', '35/349', '52/702', '34/343', '4 failed | 1 passed', 'T1', 'T2', 'T3', 'T4', 'predicted 2', 'eight', 'seven', 'requireScope', 'authMethod', "'oauth'", 'Not covered', 'NOT run', 'Migrations', 'migrations', 'KS-823', 'KS-790', 'KS-835', 'KS-843', 'KS-164', 'blast', 'Blast', 'fail-closed', 'PREFLIGHT PASSED', 'PROTOCOL-CLEAN', 'stacked', 'STACKED', 'Stacked', 's212', '127.0.0.1', '/api/auth/refresh', 'Test Evidence']:
            print(f"  body count {t!r}: {body.count(t)}")
    files = get(f'/pulls/{n}/files?per_page=100'); save(f'pr{n}_files.json', files)
    for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
    commits = get(f'/pulls/{n}/commits?per_page=100'); save(f'pr{n}_commits.json', commits)
    for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['name']} <{c['commit']['author']['email']}> {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:140]!r}")
    rv = get(f'/pulls/{n}/reviews'); save(f'pr{n}_reviews.json', rv); print(f'  reviews: {len(rv)} {[ (r["user"]["login"], r["state"]) for r in rv]}')
    rc = get(f'/pulls/{n}/comments'); save(f'pr{n}_review_comments.json', rc); print('  review comments:', len(rc))
    ic = get(f'/issues/{n}/comments?per_page=100'); save(f'pr{n}_issue_comments.json', ic)
    for c in ic:
        b = c['body'] or ''
        open(f"{G}/gh/pr{n}_comment_{c['id']}.md", 'w', encoding='utf-8').write(b)
        print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))}")
    # the standing line: the PR's base must be develop and not already merged away from
    cb = get(f"/compare/develop...{pr['base']['ref']}") if pr['base']['ref'] != 'develop' else None
    print('  base-branch check:', 'base IS develop' if cb is None else f"base {pr['base']['ref']}: status={cb['status']} ahead={cb['ahead_by']} behind={cb['behind_by']}")
c984 = get(f'/pulls/984/commits?per_page=100')
msg = c984[-1]['commit']['message']; open(f'{G}/gh/commit_984_msg.txt', 'w', encoding='utf-8').write(msg)
print('#984 head commit message: chars', len(msg), 'lines', msg.count('\n') + 1, 'KS ids', sorted(set(re.findall(r'KS-\d+', msg))), 'PR refs', sorted(set(re.findall(r'#\d{3,4}', msg))), 'at-signs', msg.count('@'), atclass(msg))
cm = get(f'/compare/develop...{HEAD}'); save('compare_develop_head.json', cm)
print(f"compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} commits={len(cm['commits'])} files={len(cm['files'])}")
for f in cm['files']: print(f"  cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
cp = get(f'/compare/{P983}...{HEAD}'); save('compare_parent_head.json', cp)
print(f"compare parent(#983)...head: status={cp['status']} merge_base={cp['merge_base_commit']['sha']} ahead={cp['ahead_by']} behind={cp['behind_by']} commits={len(cp['commits'])} files={len(cp['files'])}")
for f in cp['files']:
    print(f"  delta file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} changes={f['changes']} {f['filename']}")
bd = get('/branches/develop'); DEV = bd['commit']['sha']; print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:120]))
print('develop == M18:', DEV == M18)
r = get(f'/commits/{HEAD}'); save('commit_head.json', r)
print(f"head commit: parents={[p['sha'] for p in r['parents']]} files={len(r['files'])} +{r['stats']['additions']} -{r['stats']['deletions']}")
TOUCHED = ['Blockchain/Dev/services/auth/src/services/jwt.ts', 'Blockchain/Dev/services/auth/src/routes/oauth.ts',
           'Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts',
           'Blockchain/Dev/services/auth/src/__tests__/ks823-refresh-grant-client-auth-and-binding.test.ts',
           'Blockchain/Dev/services/auth/src/__tests__/ks835-oauth-mint-carries-granted-scope.test.ts',
           'Blockchain/Dev/services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts',
           'Blockchain/Dev/services/auth/src/routes/auth.ts', 'Blockchain/Dev/services/api-gateway/src/middleware/auth.ts',
           'Blockchain/Dev/services/auth/src/types/index.ts']
for ref, tag in [(HEAD, 'head'), (P983, 'parent'), (DEV, 'dev')]:
    for p in TOUCHED:
        short = p.split('/')[-1]
        try:
            o = get(f'/contents/{p}?ref={ref}')
            raw = base64.b64decode(o['content'])
            open(f"{G}/model/gh_{short}.{tag}", 'wb').write(raw)
            print(f"  contents {tag:6} {short}: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)} listen(={raw.count(b'listen(')}")
        except urllib.error.HTTPError as e:
            print(f"  contents {tag:6} {short}: ABSENT (HTTP {e.code})")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
