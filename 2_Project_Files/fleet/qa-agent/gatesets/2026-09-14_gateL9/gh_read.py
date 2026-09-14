#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the L9 (#940 #941 #942) TIER-2 gate set. Token sourced by NAME
(GH_TOKEN) from the Secuura .env; never printed. Writes raw JSON under <G>/gh/ and job logs under <G>/gh/joblog_<id>.txt.
Reads: the three PRs (state/base/head/files/commits/reviews/comments), compare develop...head ×3, branches/develop,
contents blobs of the lane's five files at the pinned SHAs, the Actions runs at each head (head_sha filter), the
named runs' jobs (steps + conclusions), and the named jobs' logs via the 302 redirect (Authorization header NOT sent
to the blob host — it 401s otherwise; s215's 1(c)). Never dispatches, never re-runs."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
H = {940: '1aa708be9fcf7a23575398546d84848c967e81c5', 941: 'd105e07a81c8549b7f47c0542e9594204ce6f599', 942: '53b9c3cc1a89f513620516c580a5de5bd60c64de'}
M18 = '8861e62161466c40f08d2b10a30edeb203123993'
BASE3 = 'a1e49d15152102acec7c97d96918211227c7fe1e'
C942 = 'c1676269d4b438b9b3f897d80bfeae1161dbec39'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='):
        tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
print('GH_TOKEN: set')
base = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p, raw=False):
    r = urllib.request.urlopen(urllib.request.Request(base + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60)
    return r.read() if raw else json.load(r)
def save(name, obj):
    open(f'{G}/gh/{name}', 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None
def joblog(jid):
    # step 1: ask the API for the log; it answers 302 with a signed blob URL. step 2: fetch that URL with NO auth header.
    opener = urllib.request.build_opener(NoRedirect)
    try:
        opener.open(urllib.request.Request(base + f'/actions/jobs/{jid}/logs', headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60)
        return None, 'no redirect'
    except urllib.error.HTTPError as e:
        if e.code not in (302, 301, 307): return None, f'HTTP {e.code}'
        loc = e.headers['Location']
    r = urllib.request.urlopen(urllib.request.Request(loc), timeout=120)
    b = r.read()
    open(f'{G}/gh/joblog_{jid}.txt', 'wb').write(b)
    return b.decode('utf-8', 'replace'), 'ok'
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
print('classifier positive control:', atclass('hi @kksecura and a[@] and PR #940 @ `sha` and x@y.com and `@hono/node-server`'))
for n in (940, 941, 942):
    pr = get(f'/pulls/{n}'); save(f'pr{n}.json', pr)
    print(f"PR #{n}: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} BASE={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:150]!r}")
    print('  head == pinned:', pr['head']['sha'] == H[n])
    body = pr['body'] or ''
    open(f'{G}/gh/pr{n}_body.md', 'w', encoding='utf-8').write(body)
    print(f"  body chars={len(body)} at-signs={body.count('@')} classes={atclass(body)} KS={sorted(set(re.findall(r'KS-\d+', body)))} PRrefs={sorted(set(re.findall(r'#\d{3,4}', body)))}")
    print('  headings:', [l for l in body.splitlines() if l.startswith('#')])
    for t in ['Observed in CI', 'NOT run', 'Test Evidence', 'audit-contract suites are red', 'shell: bash {0}', '34426409872', '102712486541', '34427102258', '102714559749', '34785721609', '103800717960', '34755906436', '103720115281', '34427586025', 'semver', 'audit-locks', '36 distinct advisories', '38 baselined', 'tsx@4.23.12', 'tsx@4.23.13', '14 passed, 0 failed', '27 passed, 2 failed', 'ks949_main_seed_idempotence', 'manifest_readers_agree', 'KS-1148', 'Migrations', 'Kam', 'CASE A', 'seven', '7 cases', 'stderr', 'probe.err']:
        c = body.count(t)
        if c: print(f"  body count {t!r}: {c}")
    files = get(f'/pulls/{n}/files?per_page=100'); save(f'pr{n}_files.json', files)
    for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} changes={f['changes']} {f['filename']}")
    commits = get(f'/pulls/{n}/commits?per_page=100'); save(f'pr{n}_commits.json', commits)
    for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['name']} <{c['commit']['author']['email']}> {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:140]!r}")
    rv = get(f'/pulls/{n}/reviews'); save(f'pr{n}_reviews.json', rv); print(f'  reviews: {len(rv)} {[(r["user"]["login"], r["state"]) for r in rv]}')
    rc = get(f'/pulls/{n}/comments'); save(f'pr{n}_review_comments.json', rc); print('  review comments:', len(rc))
    ic = get(f'/issues/{n}/comments?per_page=100'); save(f'pr{n}_issue_comments.json', ic)
    for c in ic:
        b = c['body'] or ''
        open(f"{G}/gh/pr{n}_comment_{c['id']}.md", 'w', encoding='utf-8').write(b)
        print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))}")
    print('  base-branch check:', 'base IS develop' if pr['base']['ref'] == 'develop' else f"base is {pr['base']['ref']} — NOT develop")
    cm = get(f"/compare/develop...{H[n]}"); save(f'compare_develop_{n}.json', cm)
    print(f"  compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} commits={len(cm['commits'])} files={len(cm['files'])}")
    for f in cm['files']: print(f"    cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} changes={f['changes']} {f['filename']}")
    # the live runs at the head
    runs = get(f"/actions/runs?head_sha={H[n]}&per_page=50"); save(f'runs_{n}.json', runs)
    print(f"  actions runs at head: total_count={runs['total_count']}")
    for r in runs['workflow_runs']:
        print(f"    run {r['id']} {r['name']!r} event={r['event']} status={r['status']} conclusion={r['conclusion']} created={r['created_at']} updated={r['updated_at']} attempt={r['run_attempt']} head={r['head_sha'][:9]} path={r['path']}")
bd = get('/branches/develop'); DEV = bd['commit']['sha']; print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:120]))
print('develop == M18:', DEV == M18)
# contents blobs at the pinned SHAs
FILES = ['.github/workflows/security-scan.yml', '.github/workflows/pr-security-gates.yml', 'Blockchain/Dev/.security/exceptions.yml', 'systemTest/__tests__/manifest_quarantine.test.sh', 'BACKLOG.md']
for ref, tag in [(H[940], 'h940'), (H[941], 'h941'), (H[942], 'h942'), (DEV, 'dev'), (BASE3, 'base3'), (C942, 'c942')]:
    for p in FILES:
        short = p.split('/')[-1]
        try:
            o = get(f'/contents/{p}?ref={ref}')
            raw = base64.b64decode(o['content'])
            open(f"{G}/model/gh_{short}.{tag}", 'wb').write(raw)
            print(f"  contents {tag:5} {short:32}: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)}")
        except urllib.error.HTTPError as e:
            print(f"  contents {tag:5} {short}: ABSENT (HTTP {e.code})")
# the named runs' jobs
RUNS = {'940_secscan': 34426409872, '941_secscan': 34427102258, '942_prsecgates': 34785721609, '942_secscan': 34785721561, '942_pr': 34785721735, 'dev_M18_prsecgates': 34755906436, '942orig_prsecgates': 34427586025}
for tag, rid in RUNS.items():
    try:
        run = get(f'/actions/runs/{rid}'); save(f'run_{rid}.json', run)
        print(f"run {tag} {rid}: {run['name']!r} head={run['head_sha']} event={run['event']} status={run['status']} conclusion={run['conclusion']} created={run['created_at']} attempt={run['run_attempt']} head_branch={run['head_branch']}")
        jobs = get(f'/actions/runs/{rid}/jobs?per_page=100'); save(f'jobs_{rid}.json', jobs)
        for j in jobs['jobs']:
            print(f"  job {j['id']} {j['name']!r} status={j['status']} conclusion={j['conclusion']} runner={j.get('runner_name')} labels={j.get('labels')}")
            for s in j['steps']:
                print(f"    step {s['number']:2} {s['conclusion']!s:9} {s['name']!r}")
    except urllib.error.HTTPError as e:
        print(f"run {tag} {rid}: HTTP {e.code}")
# the named jobs' logs
JOBS = {'940_depaudit': 102712486541, '941_depaudit': 102714559749, '942_codesecgates': 103800717960, 'dev_M18_codesecgates': 103720115281, '942orig_codesecgates': 102715992605}
for tag, jid in JOBS.items():
    txt, st = joblog(jid)
    if txt is None: print(f"joblog {tag} {jid}: {st}"); continue
    lines = txt.splitlines()
    print(f"joblog {tag} {jid}: ok, {len(txt)} bytes, {len(lines)} lines, sha256 {hashlib.sha256(txt.encode()).hexdigest()[:16]}")
    for pat in ['audit-contract suites are red', 'ℹ tests', 'ℹ pass', 'ℹ fail', "Cannot find package 'semver'", 'ERR_MODULE_NOT_FOUND', 'audit-gate:', 'OK — no advisories', 'not in allow-list', 'added ', 'npm warn exec', 'npm warn install-scripts', 'shell suites:', 'FAILED:', 'manifest_quarantine.test.sh', '14 passed, 0 failed', 'tsx@']:
        hits = [l for l in lines if pat in l]
        if hits:
            print(f"   {pat!r}: {len(hits)} line(s)")
            for l in hits[:8]: print('      ' + l.strip()[:220])
    n_x = sum(1 for l in lines if '✖' in l)
    print(f"   ✖ lines: {n_x}")
    for l in [l for l in lines if '✖' in l][:12]: print('      ' + l.strip()[:220])
    if tag == '942_codesecgates':
        seg = [l for l in lines if 'manifest_quarantine' in l]
        print('   manifest_quarantine lines:', len(seg))
        for l in seg[:6]: print('      ' + l.strip()[:200])
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
