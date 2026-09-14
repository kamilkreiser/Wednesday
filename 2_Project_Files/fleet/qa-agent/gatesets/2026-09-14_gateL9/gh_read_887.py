#!/usr/bin/env python3
"""gh_read_887.py — READ-ONLY GitHub REST reads for the FOURTH section (#887 KS-961) of the L9 gate set. Same method as
gh_read.py (GH_TOKEN by NAME; the log 302 followed without the auth header)."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
H = '3aee3deed2e3ac557f0a52c0797c2a4a8df25f69'; REV = 'cb7a3e3be735c2536e8246877fac72ecd4bcd06d'; M18 = '8861e62161466c40f08d2b10a30edeb203123993'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
base = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(base + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(name, obj): open(f'{G}/gh/{name}', 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None
def joblog(jid):
    opener = urllib.request.build_opener(NoRedirect)
    try:
        opener.open(urllib.request.Request(base + f'/actions/jobs/{jid}/logs', headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60); return None, 'no redirect'
    except urllib.error.HTTPError as e:
        if e.code not in (302, 301, 307): return None, f'HTTP {e.code}'
        loc = e.headers['Location']
    b = urllib.request.urlopen(urllib.request.Request(loc), timeout=120).read()
    open(f'{G}/gh/joblog_{jid}.txt', 'wb').write(b); return b.decode('utf-8', 'replace'), 'ok'
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '/', datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%SZ'))
pr = get('/pulls/887'); save('pr887.json', pr)
print(f"PR #887: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} BASE={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:150]!r}")
print('  head == pinned:', pr['head']['sha'] == H)
body = pr['body'] or ''; open(f'{G}/gh/pr887_body.md', 'w', encoding='utf-8').write(body)
print(f"  body chars={len(body)} at-signs={body.count('@')} KS={sorted(set(re.findall(r'KS-\d+', body)))} PRrefs={sorted(set(re.findall(r'#\d{3,4}', body)))}")
print('  headings:', [l for l in body.splitlines() if l.startswith('#')])
for t in ['NOT run', 'Test Evidence', '34786655660', '103803259738', 'rollup-linux-x64-gnu', 'OpenSSL 3.6.3', 'de376a9f1', '3aee3deed', 'cb7a3e3be', 'LANDS ON 2', 'lands on 1', '1 of 208', '2 of 515', '0 of 588', 'PREFLIGHT PASSED', '11 of 14', '29 passed, 0 failed', 'Migrations', 'cannot run', 'could not run', 'first execution', 'advisory']:
    c = body.count(t)
    if c: print(f"  body count {t!r}: {c}")
files = get('/pulls/887/files?per_page=100'); save('pr887_files.json', files)
for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} changes={f['changes']} {f['filename']}")
commits = get('/pulls/887/commits?per_page=100'); save('pr887_commits.json', commits)
for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:120]!r}")
rv = get('/pulls/887/reviews'); save('pr887_reviews.json', rv)
for r in rv: print(f"  review {r['id']} {r['user']['login']} {r['state']} @{r['commit_id'][:9]} {r['submitted_at']} chars={len(r['body'] or '')} at-signs={(r['body'] or '').count('@')}")
rc = get('/pulls/887/comments'); print('  review comments:', len(rc))
ic = get('/issues/887/comments?per_page=100'); save('pr887_issue_comments.json', ic)
for c in ic:
    b = c['body'] or ''; open(f"{G}/gh/pr887_comment_{c['id']}.md", 'w', encoding='utf-8').write(b)
    print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} KS={sorted(set(re.findall(r'KS-\d+', b)))}")
    if c['user']['login'] != 'linear[bot]':
        for t in ['cb7a3e3be', 'de376a9f1', '3aee3deed', 'OpenSSL 3.6.3', '/opt/homebrew/bin/openssl', '26', '6', 'exit 1', '1 of 172', '2 of 515', '1 of 208', '0 of 588', '40 s', '58 s', '34786655660', '103803259738', 'rollup-linux-x64-gnu', 'rollup-darwin-arm64', 'npm/cli', '4828', 'threadTokenMint', 'ks444', 'auth-service', '635', '685']:
            print(f"     comment count {t!r}: {b.count(t)}")
print('  base-branch check:', 'base IS develop' if pr['base']['ref'] == 'develop' else 'NOT develop')
cm = get(f'/compare/develop...{H}'); save('compare_develop_887.json', cm)
print(f"  compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} commits={len(cm['commits'])} files={len(cm['files'])}")
for f in cm['files']: print(f"    cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} changes={f['changes']} {f['filename']}")
cr = get(f'/compare/{REV}...{H}'); save('compare_reviewed_887.json', cr)
print(f"  compare reviewed(cb7a3e3be)...head: status={cr['status']} merge_base={cr['merge_base_commit']['sha']} ahead={cr['ahead_by']} behind={cr['behind_by']} commits={len(cr['commits'])} files={len(cr['files'])}")
runs = get(f'/actions/runs?head_sha={H}&per_page=50'); save('runs_887.json', runs)
print(f"  actions runs at head: total_count={runs['total_count']}")
for r in runs['workflow_runs']: print(f"    run {r['id']} {r['name']!r} event={r['event']} status={r['status']} conclusion={r['conclusion']} created={r['created_at']} updated={r['updated_at']} head={r['head_sha'][:9]} path={r['path']}")
runs_rev = get(f'/actions/runs?head_sha={REV}&per_page=50'); print(f"  actions runs at the reviewed head cb7a3e3be: total_count={runs_rev['total_count']}", [(r['id'], r['name'], r['conclusion']) for r in runs_rev['workflow_runs']])
for p, tag in [('.github/workflows/pr-platform-suites.yml', 'wf'), ('Blockchain/Dev/docs/DEV-PROCESS.md', 'doc')]:
    for ref, rtag in [(H, 'h887'), (REV, 'rev'), (M18, 'dev'), ('de376a9f10d456a7030b169ba921f88305b70be5', 'mrg')]:
        o = get(f'/contents/{p}?ref={ref}'); raw = base64.b64decode(o['content'])
        print(f"  contents {rtag:4} {p.split('/')[-1]:24}: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)}")
rid = 34786655660
run = get(f'/actions/runs/{rid}'); save(f'run_{rid}.json', run)
print(f"run {rid}: {run['name']!r} head={run['head_sha']} event={run['event']} status={run['status']} conclusion={run['conclusion']} created={run['created_at']} updated={run['updated_at']} attempt={run['run_attempt']}")
jobs = get(f'/actions/runs/{rid}/jobs?per_page=100'); save(f'jobs_{rid}.json', jobs)
for j in jobs['jobs']:
    print(f"  job {j['id']} {j['name']!r} status={j['status']} conclusion={j['conclusion']} started={j.get('started_at')} completed={j.get('completed_at')}")
    if 'Workspace' in j['name']:
        for s in j['steps']: print(f"    step {s['number']:2} {s['conclusion']!s:9} {s['name']!r}")
jid = 103803259738
txt, st = joblog(jid)
if txt is None: print(f"joblog {jid}: {st}")
else:
    lines = txt.splitlines()
    print(f"joblog {jid}: ok, {len(txt)} bytes, {len(lines)} lines, sha256 {hashlib.sha256(txt.encode()).hexdigest()[:16]}")
    for pat in ['workspaces with a test script', 'skipped by --if-present', 'added ', 'rollup-linux-x64-gnu', 'Cannot find module', 'demo-overlay', 'outlook-addin', 'Node.js v', 'node-version', '##[error]', 'npm run build --workspaces', 'npm run test --workspaces', 'Process completed with exit code']:
        hits = [l for l in lines if pat in l]
        if hits:
            print(f"   {pat!r}: {len(hits)} line(s)")
            for l in hits[:5]: print('      ' + l.split('Z ', 1)[1].strip()[:200] if 'Z ' in l else '      ' + l[:200])
    built = [l for l in lines if re.search(r'^\S+ > \S+@\S+ build', l.split('Z ', 1)[1] if 'Z ' in l else l)]
    print('   workspace build headers:', len(built))
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
