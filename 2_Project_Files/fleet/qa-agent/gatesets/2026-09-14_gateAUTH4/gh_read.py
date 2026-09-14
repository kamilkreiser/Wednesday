#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the AUTH4 gate set (#983 r2, #984 r2, #986, #987 + develop M20).
Token sourced by NAME (GH_TOKEN) from the Secuura .env; never printed. Raw JSON under <G>/gh/."""
import json, sys, urllib.request, datetime, re
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
H = {983: '5b0f4dd583c745e5606c9dbd580fa31f90191c6c', 984: '9b020ff827be9c83fbf5e9d62d47bc020a44519d',
     986: 'ac1c119b56888bc064a820f9b191c409c520df64', 987: 'b6ed60f3b1bfe2f72ada658242b0995d0bef7424'}
M20 = 'a5334350221c819f54d4a20a3308daeb9ca09617'; M19 = '6e78961e1d04277ecbdb0537e630afa0bf63b13c'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='):
        tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
print('GH_TOKEN: set')
base = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    r = urllib.request.urlopen(urllib.request.Request(base + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60)
    return json.load(r)
def save(name, obj):
    open(f'{G}/gh/{name}', 'w', encoding='utf-8').write(json.dumps(obj, indent=1, ensure_ascii=False))
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
dev = get('/branches/develop'); print('origin develop (API) =', dev['commit']['sha'], 'M20' if dev['commit']['sha'] == M20 else 'NOT M20')
for n, sha in H.items():
    pr = get(f'/pulls/{n}'); save(f'pr{n}.json', pr)
    body = pr['body'] or ''
    open(f'{G}/gh/pr{n}_body.md', 'w', encoding='utf-8').write(body)
    ats = len(re.findall(r'(?<![\w\[])@[A-Za-z][\w-]*', body))
    print(f"PR #{n}: state={pr['state']} draft={pr['draft']} merged={pr['merged']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} {'==pin' if pr['head']['sha']==sha else 'MOVED'} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} reviews={len(get(f'/pulls/{n}/reviews'))} body_chars={len(body)} body_mentions={ats} updated={pr['updated_at']} title={pr['title'][:110]!r}")
    c = get(f'/pulls/{n}/commits'); save(f'pr{n}_commits.json', c)
    print(f"   commits: " + ' '.join(x['sha'][:9] + '(' + ','.join(p['sha'][:9] for p in x['parents']) + ')' for x in c))
    files = get(f'/pulls/{n}/files?per_page=100'); save(f'pr{n}_files.json', files)
    print('   files: ' + ' '.join(f"{f['filename'].split('/')[-1]}:{f['status'][0]}+{f['additions']}-{f['deletions']}" for f in files))
def cmp(a, b, tag):
    c = get(f'/compare/{a}...{b}'); save(f'compare_{tag}.json', c)
    print(f"compare {tag}: merge_base={c['merge_base_commit']['sha']} status={c['status']} ahead={c['ahead_by']} behind={c['behind_by']} commits={len(c['commits'])} files={len(c.get('files') or [])}: " + ' '.join(f['filename'].split('/')[-1] for f in (c.get('files') or [])))
cmp('develop', H[983], 'dev_983'); cmp('develop', H[984], 'dev_984'); cmp('develop', H[986], 'dev_986'); cmp('develop', H[987], 'dev_987')
cmp(H[983], H[984], '983_984'); cmp(H[984], H[986], '984_986'); cmp(H[984], H[987], '984_987'); cmp(H[986], H[987], '986_987'); cmp(M19, M20, 'M19_M20')
# develop blobs of the judged files at M20 (the launcher's content judgement)
for f in ('routes/auth.ts', 'routes/oauth.ts', 'services/jwt.ts'):
    j = get('/contents/Blockchain/Dev/services/auth/src/' + f + '?ref=' + M20)
    print(f'develop@M20 blob {f} = {j["sha"]} size={j["size"]}')
print('done', datetime.datetime.now().astimezone().strftime('%H:%M:%S'))
