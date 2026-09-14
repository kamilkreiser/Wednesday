#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the L7 TIER-2 gate set (#918 r2 / #924 re-gate / #925 re-gate, stacked).
Token sourced by NAME (GH_TOKEN) from the Secuura .env; never printed. Reads per PR: /pulls/N (+files, commits, reviews,
review-comments, issue-comments), the compares develop...head and parent...head, /branches/develop, the head commits' messages,
and the Actions runs at each head with their jobs and failed steps (attributed, never graded). Saves every JSON under gh/."""
import json, sys, os, urllib.request, urllib.error, re, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
M18 = '8861e62161466c40f08d2b10a30edeb203123993'
PRS = {
    918: dict(head='b54487216ebb49f1de7ed9349f089d92a3e5bfc1', parent='21368d250', reviewed='ed954f09e0771a746004cc932cf2e4abaf667d10',
              fix_commits=['b54487216ebb49f1de7ed9349f089d92a3e5bfc1'], merge_commits=['21368d250'], ticket='KS-926'),
    924: dict(head='b85f1db24596a5e0ce98fe2b1343d9f515a1a995', parent='a849f9ac9', reviewed='1497b39de',
              fix_commits=['a849f9ac9'], merge_commits=['b85f1db24596a5e0ce98fe2b1343d9f515a1a995'], ticket='KS-773'),
    925: dict(head='5341b1daed8afe4254e05ef66ef4350fd8220d4f', parent='4459a6068', reviewed='8a5aff863',
              fix_commits=['4459a6068', '5341b1daed8afe4254e05ef66ef4350fd8220d4f'], merge_commits=['ba23b2240', '4ece7b008', '6ab1944c9'], ticket='KS-1046'),
}
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='):
        tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
base = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    r = urllib.request.urlopen(urllib.request.Request(base + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60)
    return json.load(r)
def save(name, obj):
    open(f'{G}/gh/{name}', 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
def atclass(b):
    cls = {'array': 0, 'prep': 0, 'email': 0, 'mention': 0, 'codespan': 0, 'other': 0}
    spans = [(m.start(), m.end()) for m in re.finditer(r'`[^`\n]*`', b)]
    for m in re.finditer(r'@', b):
        i = m.start(); pre = b[max(0, i-1):i]; post = b[i+1:i+2]
        if any(s <= i < e for s, e in spans): cls['codespan'] += 1
        elif pre == '[' and post == ']': cls['array'] += 1
        elif pre == ' ' and post == ' ': cls['prep'] += 1
        elif re.match(r'[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[a-z]{2,}', b[max(0, i-40):i+40]) and pre not in (' ', '\n', '(', '`'): cls['email'] += 1
        elif re.match(r'@[A-Za-z0-9][A-Za-z0-9-]*', b[i:i+40]) and pre in (' ', '\n', '(', '', ':'): cls['mention'] += 1
        else: cls['other'] += 1
    return cls
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '/', datetime.datetime.utcnow().strftime('%H:%M:%SZ'))
print('classifier positive control:', atclass('hi @kksecura and a[@] and `DIRS[@]` and x@y.com'))
bd = get('/branches/develop'); DEV = bd['commit']['sha']
print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:120]), '| == M18:', DEV == M18)
for n, P in PRS.items():
    print(f"\n================ PR #{n} ({P['ticket']}) ================")
    pr = get(f'/pulls/{n}'); save(f'pr{n}.json', pr)
    print(f"PR #{n}: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:140]!r}")
    print('  head == pinned:', pr['head']['sha'] == P['head'])
    body = pr['body'] or ''
    open(f'{G}/gh/pr{n}_body.md', 'w', encoding='utf-8').write(body)
    print(f"  body chars={len(body)} lines={body.count(chr(10))+1} at-signs={body.count('@')} classes={atclass(body)}")
    print('  KS ids in body:', sorted(set(re.findall(r'KS-\d+', body))))
    print('  PR refs in body:', sorted(set(re.findall(r'#\d{3,4}', body))))
    print('  headings:', [l for l in body.splitlines() if l.startswith('#')])
    for t in ['Test Evidence', P['head'][:9], P['reviewed'][:9], 'bash 3.2.57', 'node v24', 'darwin', 'NOT run', 'NOT covered', 'Not covered', 'Migrations', 'round 2', 'Round 2', 'round 3', 'Round 3', 're-gate', 'Re-gate', 's161', '2026-09-09-s161', 'DEFERRED', 'HOMED_ELSEWHERE', 'check-environment.sh', 'check-akto-container-names.sh', '13 wired', '13/4/4', 'OK — all 21', 'OK — 13 code guards passed', '15 passed, 0 failed', '55 passed, 0 failed', '53 passed, 2 failed', '56 passed, 0 failed', '54 passed, 1 failed', '35 standalone', 'covered: ', 'CHECKED[*]', 'unbound variable', 'F-924-1', 'F-924-2', 'F-924-3', 'F-925-1', 'F-925-2', 'F-925-3', 'F-925-4', 'F-925-5', 'PREFLIGHT INCOMPLETE — 12/15', 'PREFLIGHT PASSED.', 'PREFLIGHT_STRICT_LEGS', 'HEADER-MISMATCH', 'TOTAL_LEGS=16', 'PREFLIGHT ABORTED', 'stacked', 'STACKED', '#903', '#918', '#924', '#925', 'Nothing failed', 'legs 3 4 8', '30 passed, 0 failed', 'docker info', 'env -i', '5151452193', 'Co-Authored', '13/13 legs ran', '10/13']:
        c = body.count(t)
        if c: print(f"    body count {t!r}: {c}")
    files = get(f'/pulls/{n}/files?per_page=100'); save(f'pr{n}_files.json', files)
    for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} changes={f['changes']} sha={f['sha'][:9]} {f['filename']}")
    commits = get(f'/pulls/{n}/commits?per_page=100'); save(f'pr{n}_commits.json', commits)
    print('  PR commits via API:', len(commits))
    for c in commits:
        msg = c['commit']['message']
        ids = sorted(set(re.findall(r'KS-\d+', msg))); prs = sorted(set(re.findall(r'#\d{3,4}', msg)))
        print(f"  commit {c['sha'][:9]} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} ids={ids} PRrefs={prs} at={msg.count('@')} chars={len(msg)} subj={msg.splitlines()[0][:110]!r}")
        if c['sha'][:9] in [x[:9] for x in P['fix_commits'] + P['merge_commits']]:
            open(f"{G}/gh/commit_{c['sha'][:9]}_msg.txt", 'w', encoding='utf-8').write(msg)
    rv = get(f'/pulls/{n}/reviews'); save(f'pr{n}_reviews.json', rv); print('  reviews:', len(rv), [(r['id'], r['user']['login'], r['state'], r['submitted_at'], r['commit_id'][:9], len(r['body'] or '')) for r in rv])
    rc = get(f'/pulls/{n}/comments'); save(f'pr{n}_review_comments.json', rc); print('  review comments:', len(rc))
    ic = get(f'/issues/{n}/comments?per_page=100'); save(f'pr{n}_issue_comments.json', ic)
    for c in ic:
        b = c['body'] or ''
        open(f"{G}/gh/pr{n}_comment_{c['id']}.md", 'w', encoding='utf-8').write(b)
        print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))} head-named={P['head'][:9] in b}")
    cm = get(f"/compare/develop...{P['head']}"); save(f'compare_develop_head_{n}.json', cm)
    print(f"  compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])} total_commits={cm['total_commits']}")
    for f in cm['files']: print(f"    cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
    cp = get(f"/compare/{P['parent']}...{P['head']}"); save(f'compare_parent_head_{n}.json', cp)
    print(f"  compare {P['parent']}...head: status={cp['status']} ahead={cp['ahead_by']} behind={cp['behind_by']} files={len(cp['files'])}: {[(f['filename'].split('/')[-1], f['additions'], f['deletions']) for f in cp['files']]}")
    for f in cp['files']:
        if f.get('patch'): print(f"    hunks in {f['filename'].split('/')[-1]}:", re.findall(r'^@@[^\n]*', f['patch'], re.M))
    cr = get(f"/compare/{P['reviewed']}...{P['head']}"); save(f'compare_reviewed_head_{n}.json', cr)
    print(f"  compare {P['reviewed'][:9]}...head: status={cr['status']} ahead={cr['ahead_by']} behind={cr['behind_by']} files={len(cr['files'])} total_commits={cr['total_commits']}")
    # Actions at the head — attributed, never graded
    runs = get(f"/actions/runs?head_sha={P['head']}&per_page=50"); save(f'actions_runs_head_{n}.json', runs)
    print(f"  actions runs at head: {runs['total_count']}")
    out = []
    for r in runs['workflow_runs']:
        jobs = get(f"/actions/runs/{r['id']}/jobs?per_page=50"); save(f"actions_jobs_{r['id']}.json", jobs)
        js = []
        for j in jobs['jobs']:
            fs = [(s['number'], s['name'], s['conclusion']) for s in j['steps'] if s['conclusion'] == 'failure']
            js.append({'name': j['name'], 'status': j['status'], 'conclusion': j['conclusion'], 'failed_steps': fs})
        out.append({'run': r['name'], 'id': r['id'], 'event': r['event'], 'status': r['status'], 'conclusion': r['conclusion'], 'url': r['html_url'], 'created': r['created_at'], 'jobs': js})
        print(f"    run {r['name']!r} id={r['id']} event={r['event']} status={r['status']} conclusion={r['conclusion']} created={r['created_at']}")
        for j in js: print(f"       job {j['name']!r} {j['status']}/{j['conclusion']} failed_steps={j['failed_steps']}")
    save(f'ci_at_head_summary_{n}.json', out)
# #903 for the stack record
p = get('/pulls/903'); save('pr903.json', p)
print(f"\nPR #903: state={p['state']} merged={p['merged']} head={p['head']['sha']} mergeable={p['mergeable']}/{p['mergeable_state']} updated={p['updated_at']}")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
