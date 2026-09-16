#!/usr/bin/env python3
"""READ-ONLY GitHub REST reads for #1003 (KS-1165) in the #1002+#1003 tier-2 gate set, plus a re-read of #1002's head
and develop. GH_TOKEN read by NAME from the Secuura .env; never printed or written. GET only. Usage: gh_read_1003.py <dir>"""
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
    return json.load(urllib.request.urlopen(urllib.request.Request(base + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))


def save(name, obj):
    open(f'{G}/gh/{name}', 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))


def now():
    return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')


print('read at', now())
PINS = {1002: 'a376756aba1e1ae32c49ed47ba057fd80c7ed136', 1003: 'c5488a6891e6ac6fe950c101196d8c33ab8e173f'}
dev = get('/branches/develop')
print('develop tip (branches API):', dev['commit']['sha'], dev['commit']['commit']['committer']['date'], repr(dev['commit']['commit']['message'].splitlines()[0][:100]))
filesets = {}
for n, H in PINS.items():
    pr = get(f'/pulls/{n}'); save(f'pr{n}.json', pr)
    print(f"\nPR #{n}: state={pr['state']} draft={pr['draft']} merged={pr['merged']} base={pr['base']['ref']}@{pr['base']['sha']} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']}")
    print('  title:', pr['title'])
    print('  head == pin:', pr['head']['sha'] == H)
    files = get(f'/pulls/{n}/files?per_page=100')
    filesets[n] = {f['filename'] for f in files}
    cm = get(f'/compare/develop...{H}')
    print(f"  compare develop...{H[:9]}: status={cm['status']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])} merge_base={cm['merge_base_commit']['sha']}")
    if n != 1003:
        continue
    body = pr['body'] or ''
    open(f'{G}/gh/pr1003_body.md', 'w', encoding='utf-8').write(body)
    print(f"  body chars={len(body)} KS ids={sorted(set(re.findall(r'KS-[0-9]+', body)))}")
    for m in re.finditer(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?|part of|ref(erences)?|related to|contributes to)\b[: ]+KS-[0-9]+', body):
        print('  closing/linking phrase:', repr(m.group(0)))
    save('pr1003_files.json', files)
    for f in files:
        print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} {f['filename']}")
    commits = get('/pulls/1003/commits?per_page=100'); save('pr1003_commits.json', commits)
    for c in commits:
        print(f"  commit {c['sha']} parents={[p['sha'] for p in c['parents']]} {c['commit']['author']['date']} subj={c['commit']['message'].splitlines()[0][:140]!r}")
    save('compare_develop_1003.json', cm)
    print('  reviews:', len(get('/pulls/1003/reviews')))
    ic = get('/issues/1003/comments?per_page=100'); save('pr1003_issue_comments.json', ic)
    print('  issue comments:', len(ic), [c['user']['login'] for c in ic])
    parent = commits[0]['parents'][0]['sha']
    for f in files:
        o = get('/contents/' + f['filename'] + '?ref=' + H)
        p = f"{G}/gh/pr1003_head_" + f['filename'].replace('/', '__')
        open(p, 'w', encoding='utf-8').write(base64.b64decode(o['content']).decode('utf-8', 'replace'))
        open(p + '.patch', 'w', encoding='utf-8').write(f.get('patch') or '')
        if f['status'] != 'added':
            o2 = get('/contents/' + f['filename'] + '?ref=' + parent)
            open(f"{G}/gh/pr1003_base_" + f['filename'].replace('/', '__'), 'w', encoding='utf-8').write(base64.b64decode(o2['content']).decode('utf-8', 'replace'))
    for ep in (f'/commits/{H}/check-runs', f'/commits/{H}/status'):
        try:
            j = get(ep); print('  ', ep, 'readable:', {k: j.get(k) for k in ('total_count', 'state')})
        except urllib.error.HTTPError as e:
            print('  ', ep, 'HTTP', e.code)
shared = filesets[1002] & filesets[1003]
print('\nfiles shared by #1002 and #1003:', len(shared), sorted(shared))
print('done at', now())
