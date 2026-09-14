#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #799 (KS-764) TIER-1 gate set. Token sourced by NAME (GH_TOKEN)
from the Secuura .env; never printed. Writes raw JSON under <G>/gh/ and the touched files' bytes under <G>/model/gh_*.
Adapted from gatesets/2026-09-14_gate984/gh_read.py (the same reads, re-pointed at #799 — a merge-shaped PR, not a stack)."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
HEAD = '6da848891924f859179d097d464a7b97c9783a6a'   # #799 head = the fix commit
MERGE = 'e6e25421e98ba8f11153f5fc394fe79fc96549a0'  # the develop-merge commit (the fix commit's parent)
PETER = '38f6377b9c6429be2627cb5454e98a36104a25b8'  # Peter's second develop merge = the head his 09-09 review stood on (7dfc7ebca + his merge)
M18 = '8861e62161466c40f08d2b10a30edeb203123993'    # origin develop at the builder's cut
os.makedirs(f'{G}/gh', exist_ok=True); os.makedirs(f'{G}/model', exist_ok=True)
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
    cls = {'array': 0, 'prep': 0, 'email': 0, 'idiom': 0, 'mention': 0, 'scope': 0, 'other': 0}
    for m in re.finditer(r'@', b):
        i = m.start(); pre = b[max(0, i-1):i]; post = b[i+1:i+2]
        if pre == '[' and post == ']': cls['array'] += 1
        elif pre == ' ' and post == ' ': cls['prep'] += 1
        elif pre == ' ' and post == '`': cls['idiom'] += 1
        elif b[i:i+9] == '@secuura/': cls['scope'] += 1
        elif re.match(r'[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[a-z]{2,}', b[max(0, i-40):i+40]) and pre not in (' ', '\n', '(', '`'): cls['email'] += 1
        elif re.match(r'@[A-Za-z0-9][A-Za-z0-9-]*', b[i:i+40]) and pre in (' ', '\n', '(', '', ':', '`'): cls['mention'] += 1
        else: cls['other'] += 1
    return cls
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '/', datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%SZ'))
print('classifier positive control:', atclass('hi @kksecura and a[@] and PR #799 @ `sha` and x@y.com and `@secuura/shared` and @kam'))
n = 799
pr = get(f'/pulls/{n}'); save(f'pr{n}.json', pr)
print(f"PR #{n}: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} BASE={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:160]!r}")
body = pr['body'] or ''
open(f'{G}/gh/pr{n}_body.md', 'w', encoding='utf-8').write(body)
print(f"  body chars={len(body)} at-signs={body.count('@')} classes={atclass(body)} KS={sorted(set(re.findall(r'KS-\d+', body)))} PRrefs={sorted(set(re.findall(r'#\d{3,4}', body)))}")
print('  headings:', [l for l in body.splitlines() if l.startswith('#')])
for t in ['6da848891', 'e6e25421e', '38f6377b9', '8861e6216', '7dfc7ebca', '@kam', '@secuura/shared', 'Test Evidence', '828/828', '205/205', '598/598', '343/343', '23/23', '1 failed | 22 passed', '1 failed | 9 passed', '1 failed | 6 passed', 'caller has no tenant', 'ADMIN_NO_TENANT', 'typeof', 'T1', 'T2', 'T3', 'loopback', 'F-2', 'F-3', 'F-1', '6(b)', '6(c)', 'nit', 'NOT done', 'Not covered', 'HOLD', '127.0.0.1', 'M18', 'Migrations', 'migration', 'F-764-03', 'startup-migrations', 'PREFLIGHT', 'PROTOCOL', 'ks742', 'KS-742', 'KS-860', 'ks860', 'round']:
    print(f"  body count {t!r}: {body.count(t)}")
files = get(f'/pulls/{n}/files?per_page=100'); save(f'pr{n}_files.json', files)
print(f'  files API: {len(files)} files, +{sum(f["additions"] for f in files)} -{sum(f["deletions"] for f in files)}')
for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} changes={f['changes']} {f['filename']}")
commits = get(f'/pulls/{n}/commits?per_page=100'); save(f'pr{n}_commits.json', commits)
print(f'  commits API: {len(commits)}')
for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['name']} <{c['commit']['author']['email']}> {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:150]!r}")
rv = get(f'/pulls/{n}/reviews?per_page=100'); save(f'pr{n}_reviews.json', rv); print(f'  reviews: {len(rv)}')
for r in rv:
    b = r['body'] or ''
    open(f"{G}/gh/pr{n}_review_{r['id']}.md", 'w', encoding='utf-8').write(b)
    print(f"  review {r['id']} {r['user']['login']} {r['state']} @{r['commit_id'][:9]} {r['submitted_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)}")
rc = get(f'/pulls/{n}/comments?per_page=100'); save(f'pr{n}_review_comments.json', rc); print('  review (inline) comments:', len(rc))
ic = get(f'/issues/{n}/comments?per_page=100'); save(f'pr{n}_issue_comments.json', ic); print('  issue comments:', len(ic))
for c in ic:
    b = c['body'] or ''
    open(f"{G}/gh/pr{n}_comment_{c['id']}.md", 'w', encoding='utf-8').write(b)
    print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))}")
cb = get(f"/compare/develop...{pr['base']['ref']}") if pr['base']['ref'] != 'develop' else None
print('  base-branch check:', 'base IS develop' if cb is None else f"base {pr['base']['ref']}: status={cb['status']} ahead={cb['ahead_by']} behind={cb['behind_by']}")
msg = commits[-1]['commit']['message']; open(f'{G}/gh/commit_799_head_msg.txt', 'w', encoding='utf-8').write(msg)
print('#799 head commit message: chars', len(msg), 'lines', msg.count('\n') + 1, 'KS ids', sorted(set(re.findall(r'KS-\d+', msg))), 'PR refs', sorted(set(re.findall(r'#\d{3,4}', msg))), 'at-signs', msg.count('@'), atclass(msg))
mm = commits[-2]['commit']['message']; print('#799 merge commit message:', repr(mm[:200]), 'KS ids', sorted(set(re.findall(r'KS-\d+', mm))), 'at-signs', mm.count('@'))
cm = get(f'/compare/develop...{HEAD}'); save('compare_develop_head.json', cm)
print(f"compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} commits={len(cm['commits'])} files={len(cm['files'])}")
for f in cm['files']: print(f"  cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} changes={f['changes']} {f['filename']}")
cp = get(f'/compare/{MERGE}...{HEAD}'); save('compare_merge_head.json', cp)
print(f"compare merge-commit...head (the FIX commit's delta): status={cp['status']} merge_base={cp['merge_base_commit']['sha']} ahead={cp['ahead_by']} behind={cp['behind_by']} commits={len(cp['commits'])} files={len(cp['files'])}")
for f in cp['files']: print(f"  delta file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} changes={f['changes']} {f['filename']}")
cq = get(f'/compare/{PETER}...{HEAD}'); save('compare_peter_head.json', cq)
print(f"compare 38f6377b9...head (what moved since Peter's last read): status={cq['status']} merge_base={cq['merge_base_commit']['sha']} ahead={cq['ahead_by']} behind={cq['behind_by']} commits={len(cq['commits'])} files={len(cq['files'])}")
bd = get('/branches/develop'); DEV = bd['commit']['sha']; print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:120]))
print('develop == M18:', DEV == M18)
r = get(f'/commits/{HEAD}'); save('commit_head.json', r)
print(f"head commit: parents={[p['sha'] for p in r['parents']]} files={len(r['files'])} +{r['stats']['additions']} -{r['stats']['deletions']}")
r2 = get(f'/commits/{MERGE}'); save('commit_merge.json', r2)
print(f"merge commit: parents={[p['sha'] for p in r2['parents']]} files(vs first parent)={len(r2['files'])} +{r2['stats']['additions']} -{r2['stats']['deletions']}")
p880 = get('/pulls/880'); print(f"PR #880 (the sibling on security index.ts): state={p880['state']} base={p880['base']['ref']} head={p880['head']['sha']} mergeable={p880['mergeable']}/{p880['mergeable_state']}")
TOUCHED = ['BACKLOG.md',
           'Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts',
           'Blockchain/Dev/packages/shared/src/index.ts',
           'Blockchain/Dev/packages/shared/src/middleware/index.ts',
           'Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts',
           'Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts',
           'Blockchain/Dev/services/originate/src/middleware/auth.ts',
           'Blockchain/Dev/services/originate/src/routes/adminConfig.ts',
           'Blockchain/Dev/services/security/src/__tests__/ks764-key-revoke-organisation-arm.test.ts',
           'Blockchain/Dev/services/security/src/__tests__/ks764-revoke-organisation-route-contract.test.ts',
           'Blockchain/Dev/services/security/src/index.ts',
           'Blockchain/Dev/services/security/src/keyRevokePolicy.ts',
           'Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts',
           'Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts',
           'Blockchain/Dev/scripts/audit/audit-baseline.json']
for ref, tag in [(HEAD, 'head'), (MERGE, 'merge'), (PETER, 'p38f'), (DEV, 'dev')]:
    for p in TOUCHED:
        short = p.replace('Blockchain/Dev/', '').replace('/', '__')
        try:
            o = get(f'/contents/{p}?ref={ref}')
            raw = base64.b64decode(o['content'])
            open(f"{G}/model/gh_{short}.{tag}", 'wb').write(raw)
            print(f"  contents {tag:6} {short}: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)} listen(={raw.count(b'listen(')}")
        except urllib.error.HTTPError as e:
            print(f"  contents {tag:6} {short}: ABSENT (HTTP {e.code})")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
