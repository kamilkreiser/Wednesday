#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #983 (KS-823) TIER-1 gate set. Token sourced by NAME (GH_TOKEN)
from the Secuura .env; never printed. Writes JSON + bodies under <G>/gh/ and the lane's files at four SHAs under <G>/model/."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
HEAD = 'f62c975c11ec97cdef04500fd98a43618e702763'   # #983 head (KS-823)
PARENT = 'e62eab87a6263e25c41c9bb814d5831842bb6c7e' # #982 head (KS-790) = #983's parent
M18 = '8861e62161466c40f08d2b10a30edeb203123993'    # origin develop at draft time
HEAD984 = 'd00a2015c89a4720eaeab64482bbd9b89d878024' # #984 head (KS-835), stacked on #983
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
base = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    r = urllib.request.urlopen(urllib.request.Request(base + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60)
    return json.load(r)
def save(name, obj):
    open(f'{G}/gh/{name}', 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
def atclass(b):
    cls = {'array': 0, 'prep': 0, 'email': 0, 'mention': 0, 'other': 0}
    for m in re.finditer(r'@', b):
        i = m.start(); pre = b[max(0, i - 1):i]; post = b[i + 1:i + 2]
        if pre == '[' and post == ']': cls['array'] += 1
        elif pre == ' ' and post == ' ': cls['prep'] += 1
        elif re.match(r'[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[a-z]{2,}', b[max(0, i - 40):i + 40]) and pre not in (' ', '\n', '(', '`'): cls['email'] += 1
        elif re.match(r'@[A-Za-z0-9][A-Za-z0-9-]*', b[i:i + 40]) and pre in (' ', '\n', '(', '', ':'): cls['mention'] += 1
        else: cls['other'] += 1
    return cls
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '/', datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%SZ'))
print('classifier positive control:', atclass('hi @kksecura and a[@] and PR #983 @ `sha` and x@y.com'))
for n in (983, 982, 984):
    pr = get(f'/pulls/{n}'); save(f'pr{n}.json', pr)
    print(f"PR #{n}: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:140]!r}")
    body = pr['body'] or ''
    open(f'{G}/gh/pr{n}_body.md', 'w', encoding='utf-8').write(body)
    print(f"  body chars={len(body)} at-signs={body.count('@')} classes={atclass(body)} KS={sorted(set(re.findall(r'KS-\d+', body)))} PRrefs={sorted(set(re.findall(r'#\d{3,4}', body)))}")
    print('  headings:', [l for l in body.splitlines() if l.startswith('#')])
    rv = get(f'/pulls/{n}/reviews'); save(f'pr{n}_reviews.json', rv); print('  reviews:', len(rv), [(r['user']['login'], r['state'], r['commit_id'][:9]) for r in rv])
    rc = get(f'/pulls/{n}/comments'); save(f'pr{n}_review_comments.json', rc); print('  review comments:', len(rc))
    ic = get(f'/issues/{n}/comments?per_page=100'); save(f'pr{n}_issue_comments.json', ic)
    for c in ic:
        b = c['body'] or ''
        open(f"{G}/gh/pr{n}_comment_{c['id']}.md", 'w', encoding='utf-8').write(b)
        print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))} head983={HEAD[:9] in b}")
body = open(f'{G}/gh/pr983_body.md', encoding='utf-8').read()
for tok_ in ['f62c975c1', 'e62eab87a', '#982', 'KS-790', 'stack', 'Stacked', 'STACKED', '7 failed | 4 passed', '11/11', '52 files', '702', '691', 'T1', 'T2', 'T3', 'T4', '4/4', 'fail-closed', 'FAIL-CLOSED', 'grandfather', 'ruling', 'NOT run', 'Not covered', 'NOT covered', 'Migrations', 'migration', 'raw socket', 'initJwtKeys', 'OAuthMintOptions', 'OAuthTokenClaims', 'client_id', 'readClientId', 'invalid_client', 'invalid_grant', 'invalid_request', 'Test Evidence', 'PII', 'KS-256', 'KS-823', 'KS-1003', 'KS-820', 'KS-821', 'KS-822', 'KS-835', 'RFC 6749']:
    print(f"  #983 body count {tok_!r}: {body.count(tok_)}")
files = get('/pulls/983/files?per_page=100'); save('pr983_files.json', files)
for f in files: print(f"  #983 file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
commits = get('/pulls/983/commits?per_page=100'); save('pr983_commits.json', commits)
for c in commits: print(f"  #983 commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['name']} <{c['commit']['author']['email']}> {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:160]!r}")
msg = commits[-1]['commit']['message']; open(f'{G}/gh/commit_983_msg.txt', 'w', encoding='utf-8').write(msg)
print('  head commit message KS ids:', sorted(set(re.findall(r'KS-\d+', msg))), 'PR refs:', sorted(set(re.findall(r'#\d{3,4}', msg))), 'at-signs:', msg.count('@'), atclass(msg), 'chars', len(msg), 'lines', msg.count('\n') + 1)
cm = get(f'/compare/develop...{HEAD}'); save('compare_develop_head.json', cm)
print(f"compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])}")
for f in cm['files']: print(f"  cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
cp = get(f'/compare/{PARENT}...{HEAD}'); save('compare_parent_head.json', cp)
print(f"compare parent...head: status={cp['status']} ahead={cp['ahead_by']} behind={cp['behind_by']} commits={len(cp['commits'])} files={len(cp['files'])}")
for f in cp['files']: print(f"  delta file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} changes={f['changes']} {f['filename']}")
cq = get(f'/compare/develop...{PARENT}'); save('compare_develop_parent.json', cq)
print(f"compare develop...parent(#982): status={cq['status']} merge_base={cq['merge_base_commit']['sha']} ahead={cq['ahead_by']} behind={cq['behind_by']} files={len(cq['files'])}: {[f['filename'].split('/')[-1] for f in cq['files']]}")
c4 = get(f'/compare/{HEAD}...{HEAD984}'); save('compare_head_984.json', c4)
print(f"compare head...#984: status={c4['status']} ahead={c4['ahead_by']} behind={c4['behind_by']} files={len(c4['files'])}: {[f['filename'].split('/')[-1] for f in c4['files']]}")
bd = get('/branches/develop'); DEV = bd['commit']['sha']; print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:120]))
print('develop == M18 pin:', DEV == M18)
r2 = get(f'/commits/{HEAD}'); save('commit_head.json', r2)
print(f"head commit: parents={[p['sha'] for p in r2['parents']]} files={len(r2['files'])} +{r2['stats']['additions']} -{r2['stats']['deletions']}")
P = 'Blockchain/Dev/services/auth/src/'
FILES = [P + 'routes/oauth.ts', P + 'services/jwt.ts', P + '__tests__/ks823-refresh-grant-client-auth-and-binding.test.ts',
         P + '__tests__/ks790-token-pre-auth-user-lookup.test.ts', P + '__tests__/ks820-821-token-client-auth-and-apptype.test.ts',
         P + 'types/index.ts', P + 'routes/auth.ts', P + 'services/oauth.ts', P + 'repositories/userRepo.ts']
for ref, tag in [(HEAD, 'head'), (PARENT, 'parent'), (M18, 'dev'), (HEAD984, 'h984')]:
    for p in FILES:
        short = p[len(P):].replace('/', '_')
        try:
            o = get(f'/contents/{p}?ref={ref}')
            raw = base64.b64decode(o['content'])
            open(f"{G}/model/api.{short}.{ref[:9]}", 'wb').write(raw)
            print(f"  contents {tag:6} {ref[:9]} {short}: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)}")
        except urllib.error.HTTPError as e:
            print(f"  contents {tag:6} {ref[:9]} {short}: ABSENT (HTTP {e.code})")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
