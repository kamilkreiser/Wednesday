#!/usr/bin/env python3
"""READ-ONLY GitHub REST reads for the #1002 (KS-1123) tier-2 gate set. GH_TOKEN read by NAME from the Secuura .env;
never printed, never written. GET only. Usage: gh_read.py <gateset dir>"""
import json, sys, os, urllib.request, urllib.error, re, datetime, base64
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
os.makedirs(f'{G}/gh', exist_ok=True)
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


def now():
    return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')


print('read at', now())
H = 'a376756aba1e1ae32c49ed47ba057fd80c7ed136'
BASE_PIN = '80686962'
dev = get('/branches/develop')
DEV = dev['commit']['sha']
print('develop tip (branches API):', DEV, dev['commit']['commit']['committer']['date'], repr(dev['commit']['commit']['message'].splitlines()[0][:120]))

pr = get('/pulls/1002'); save('pr1002.json', pr)
print(f"\nPR #1002: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha']} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']}")
print('  title:', pr['title'])
print('  head == pin:', pr['head']['sha'] == H)
body = pr['body'] or ''
open(f'{G}/gh/pr1002_body.md', 'w', encoding='utf-8').write(body)
print(f"  body chars={len(body)} KS ids={sorted(set(re.findall(r'KS-[0-9]+', body)))}")
for m in re.finditer(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?|part of|ref(erences)?|related to|contributes to)\b[: ]+KS-[0-9]+', body):
    print('  closing/linking phrase:', repr(m.group(0)))
files = get('/pulls/1002/files?per_page=100'); save('pr1002_files.json', files)
for f in files:
    print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} {f['filename']}")
commits = get('/pulls/1002/commits?per_page=100'); save('pr1002_commits.json', commits)
for c in commits:
    print(f"  commit {c['sha']} parents={[p['sha'] for p in c['parents']]} {c['commit']['author']['date']} subj={c['commit']['message'].splitlines()[0][:140]!r}")
cm = get(f'/compare/develop...{H}'); save('compare_develop_1002.json', cm)
MB = cm['merge_base_commit']['sha']
print(f"  compare develop...{H[:9]}: status={cm['status']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])} merge_base={MB}")
print('  merge_base startswith pin', BASE_PIN, ':', MB.startswith(BASE_PIN))
rv = get('/pulls/1002/reviews'); print('  reviews:', len(rv))
ic = get('/issues/1002/comments?per_page=100'); print('  issue comments:', len(ic), [c['user']['login'] for c in ic])
save('pr1002_issue_comments.json', ic)
parent = commits[0]['parents'][0]['sha'] if commits else MB
for f in files:
    o = get('/contents/' + f['filename'] + '?ref=' + H)
    p = f"{G}/gh/pr1002_head_" + f['filename'].replace('/', '__')
    open(p, 'w', encoding='utf-8').write(base64.b64decode(o['content']).decode('utf-8', 'replace'))
    open(p + '.patch', 'w', encoding='utf-8').write(f.get('patch') or '')
    if f['status'] != 'added':
        o2 = get('/contents/' + f['filename'] + '?ref=' + parent)
        open(f"{G}/gh/pr1002_base_" + f['filename'].replace('/', '__'), 'w', encoding='utf-8').write(base64.b64decode(o2['content']).decode('utf-8', 'replace'))

# develop movement since the PR's parent, and whether it touches this PR's files or api-gateway
dm = get(f'/compare/{parent}...develop'); save('compare_parent_develop.json', dm)
print(f"\ncompare {parent[:9]}...develop: status={dm['status']} ahead={dm['ahead_by']} behind={dm['behind_by']} files={len(dm['files'])}")
for c in dm.get('commits', []):
    print(f"   develop commit {c['sha'][:9]} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['committer']['date']} {c['commit']['message'].splitlines()[0][:110]!r}")
prfiles = {f['filename'] for f in files}
for f in dm['files']:
    fn = f['filename']
    tag = 'SAME FILE AS #1002' if fn in prfiles else ''
    print(f"   develop-moved: {f['status']:9} +{f['additions']} -{f['deletions']} {fn} {tag}")

# #1001's state (expected to merge next; file-disjointness)
p1 = get('/pulls/1001'); save('pr1001.json', p1)
print(f"\nPR #1001: state={p1['state']} merged={p1['merged']} merged_at={p1.get('merged_at')} merge_commit={p1.get('merge_commit_sha')} head={p1['head']['sha']}")
f1 = get('/pulls/1001/files?per_page=100'); save('pr1001_files.json', f1)
for f in f1:
    print(f"   #1001 file {f['status']:9} {f['filename']} {'SAME FILE AS #1002' if f['filename'] in prfiles else ''}")
for n in (999, 1000):
    pn = get(f'/pulls/{n}')
    print(f"PR #{n}: state={pn['state']} merged={pn['merged']} merged_at={pn.get('merged_at')} merge_commit={pn.get('merge_commit_sha')}")

# check-runs (403 expected per the #999 gate)
for ep in (f'/commits/{H}/check-runs', f'/commits/{H}/status'):
    try:
        j = get(ep)
        print('  ', ep, 'readable:', {k: j.get(k) for k in ('total_count', 'state')})
    except urllib.error.HTTPError as e:
        print('  ', ep, 'HTTP', e.code)
print('done at', now())
