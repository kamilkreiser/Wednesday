#!/usr/bin/env python3
"""READ-ONLY GitHub REST reads for the #999 + #1000 tier-2 gate set. GH_TOKEN read by NAME from the Secuura .env; never printed. GET only."""
import json, sys, os, urllib.request, re, datetime, base64
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G=sys.argv[1]
os.makedirs(f'{G}/gh', exist_ok=True)
tok=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok=line.split('=',1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
base='https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    r=urllib.request.urlopen(urllib.request.Request(base+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}), timeout=60)
    return json.load(r)
def save(name, obj):
    open(f'{G}/gh/{name}','w',encoding='utf-8').write(json.dumps(obj,indent=1,ensure_ascii=False))
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
PINS={999:'91793e5d4f4d4b70eec93662c45555472e2bb8a6', 1000:'ab4a35d75d9b7611b4588ce88a792a489a124324'}
dev=get('/branches/develop'); print('develop tip (branches API):', dev['commit']['sha'], dev['commit']['commit']['committer']['date'])
for n,H in PINS.items():
    pr=get(f'/pulls/{n}'); save(f'pr{n}.json',pr)
    print(f"\nPR #{n}: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha']} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']}")
    print('  title:', pr['title'])
    print('  head == pin:', pr['head']['sha']==H)
    body=pr['body'] or ''
    open(f'{G}/gh/pr{n}_body.md','w',encoding='utf-8').write(body)
    print(f"  body chars={len(body)} KS ids={sorted(set(re.findall(r'KS-[0-9]+', body)))}")
    for m in re.finditer(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?|part of|ref(erences)?|related to|contributes to)\b[: ]+KS-[0-9]+', body):
        print('  closing/linking phrase:', repr(m.group(0)))
    files=get(f'/pulls/{n}/files?per_page=100'); save(f'pr{n}_files.json',files)
    for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} {f['filename']}")
    commits=get(f'/pulls/{n}/commits?per_page=100'); save(f'pr{n}_commits.json',commits)
    for c in commits: print(f"  commit {c['sha']} parents={[p['sha'] for p in c['parents']]} {c['commit']['author']['date']} subj={c['commit']['message'].splitlines()[0][:140]!r}")
    cm=get(f'/compare/develop...{H}'); save(f'compare_develop_{n}.json',cm)
    print(f"  compare develop...{H[:9]}: status={cm['status']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])} merge_base={cm['merge_base_commit']['sha']}")
    rv=get(f'/pulls/{n}/reviews'); print('  reviews:', len(rv))
    ic=get(f'/issues/{n}/comments?per_page=100'); print('  issue comments:', len(ic), [c['user']['login'] for c in ic])
    # full file contents at head for the brief drafter's read
    for f in files:
        o=get('/contents/'+f['filename']+'?ref='+H)
        p=f"{G}/gh/pr{n}_head_"+f['filename'].replace('/','__')
        open(p,'w',encoding='utf-8').write(base64.b64decode(o['content']).decode('utf-8','replace'))
        if f['status']!='added':
            try:
                o2=get('/contents/'+f['filename']+'?ref='+cm['merge_base_commit']['sha'])
                open(f"{G}/gh/pr{n}_base_"+f['filename'].replace('/','__'),'w',encoding='utf-8').write(base64.b64decode(o2['content']).decode('utf-8','replace'))
            except Exception as e: print('  base read failed', f['filename'], type(e).__name__)
        open(p+'.patch','w',encoding='utf-8').write(f.get('patch') or '')
# develop movement since the shared base
mb=json.load(open(f'{G}/gh/compare_develop_999.json'))['merge_base_commit']['sha']
dm=get(f'/compare/{mb}...develop'); save('compare_base_develop.json', dm)
print(f"\ncompare {mb[:9]}...develop: status={dm['status']} ahead={dm['ahead_by']} files={len(dm['files'])}")
for f in dm['files']:
    fn=f['filename']
    if 'api-gateway' in fn or 'services/auth/' in fn or 'packages/shared' in fn: print('   develop-moved touched:', f['status'], fn)
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
