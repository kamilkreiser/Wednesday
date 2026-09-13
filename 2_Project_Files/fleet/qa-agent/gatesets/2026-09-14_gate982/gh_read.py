#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #982 (KS-790) TIER-1 gate set. Token sourced by NAME (GH_TOKEN) from the Secuura .env; never printed.
Reads: /pulls/982 (+files, commits, reviews, review-comments, issue-comments), compare develop...head, /branches/develop, compare M18...develop,
/commits/head, the contents API for the three files at head and develop (+ userRepo.ts, jwt.ts at head), /pulls/983 and /pulls/984 (the stack), /pulls/881."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G=sys.argv[1]
HEAD='e62eab87a6263e25c41c9bb814d5831842bb6c7e'; M18='8861e62161466c40f08d2b10a30edeb203123993'
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
def atclass(b):
    cls={'array':0,'prep':0,'email':0,'mention':0,'other':0}
    for m in re.finditer(r'@', b):
        i=m.start(); pre=b[max(0,i-1):i]; post=b[i+1:i+2]
        if pre=='[' and post==']': cls['array']+=1
        elif pre==' ' and post==' ': cls['prep']+=1
        elif re.match(r'[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[a-z]{2,}', b[max(0,i-40):i+40]) and pre not in (' ','\n','(','`'): cls['email']+=1
        elif re.match(r'@[A-Za-z0-9][A-Za-z0-9-]*', b[i:i+40]) and pre in (' ','\n','(','',':') : cls['mention']+=1
        else: cls['other']+=1
    return cls
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '/', datetime.datetime.utcnow().strftime('%H:%M:%SZ'))
print('classifier positive control:', atclass('hi @kksecura and a[@] and PR #982 @ `sha` and x@y.com'))
pr=get('/pulls/982'); save('pr982.json',pr)
print(f"PR #982: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:160]!r}")
body=pr['body'] or ''
open(f'{G}/gh/pr982_body.md','w',encoding='utf-8').write(body)
print(f"body chars={len(body)} lines={body.count(chr(10))+1} at-signs={body.count('@')} classes={atclass(body)}")
print('KS ids in body:', sorted(set(re.findall(r'KS-\d+', body))))
print('PR refs in body:', sorted(set(re.findall(r'#\d{3,4}', body))))
print('headings:', [l for l in body.splitlines() if l.startswith('#')])
for tok_ in ['Test Evidence','e62eab87a','8861e6216','getUserByIdPreAuth','getUserById','verifyRefreshToken','require(','static import','4 failed | 2 passed','6/6','51 files','691','685','tsc','T1','T2','T3','ks820-821','mock entry','fallback','QUESTION','Not covered','NOT run','migration 039','NOT MEASURED','platform suites','Migrations','config','KS-823','KS-835','KS-781','KS-458','KS-963','#983','#984','127.0.0.1','raw socket','Co-Authored']:
    print(f"  body count {tok_!r}: {body.count(tok_)}")
files=get('/pulls/982/files?per_page=100'); save('pr982_files.json',files)
for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} changes={f['changes']} sha={f['sha'][:9]} {f['filename']}")
commits=get('/pulls/982/commits?per_page=100'); save('pr982_commits.json',commits)
for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['name']} <{c['commit']['author']['email']}> {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:160]!r}")
cm_msg=commits[-1]['commit']['message']; open(f'{G}/gh/commit_head_msg_api.txt','w',encoding='utf-8').write(cm_msg)
print('  head message KS ids:', sorted(set(re.findall(r'KS-\d+', cm_msg))), 'PR refs:', sorted(set(re.findall(r'#\d{3,4}', cm_msg))), 'at-signs:', cm_msg.count('@'), atclass(cm_msg), 'chars', len(cm_msg), 'lines', cm_msg.count('\n')+1)
rv=get('/pulls/982/reviews'); save('pr982_reviews.json',rv); print('reviews:', len(rv), [(r['user']['login'], r['state'], r['submitted_at']) for r in rv])
rc=get('/pulls/982/comments'); save('pr982_review_comments.json',rc); print('review comments:', len(rc))
ic=get('/issues/982/comments?per_page=100'); save('pr982_issue_comments.json',ic)
for c in ic:
    b=c['body'] or ''
    open(f"{G}/gh/pr982_comment_{c['id']}.md",'w',encoding='utf-8').write(b)
    print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))} head-mention={HEAD[:9] in b}")
cm=get(f'/compare/develop...{HEAD}'); save('compare_develop_head.json',cm)
print(f"compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])}")
for f in cm['files']: print(f"  cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
bd=get('/branches/develop'); DEV=bd['commit']['sha']; print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:140]))
if DEV != M18:
    cd=get(f'/compare/{M18}...{DEV}'); save('compare_M18_develop.json',cd)
    print(f"compare M18...develop: status={cd['status']} ahead={cd['ahead_by']} files={len(cd['files'])}: {[f['filename'] for f in cd['files']]}")
else:
    print('develop == M18 (no delta to judge)')
hc=get(f'/commits/{HEAD}'); save('commit_head.json',hc)
print(f"head commit: parents={[p['sha'] for p in hc['parents']]} files={len(hc['files'])} +{hc['stats']['additions']} -{hc['stats']['deletions']}")
for f in hc['files']: print(f"  head-commit file {f['status']:9} +{f['additions']} -{f['deletions']} {f['filename']}")
OAUTH='Blockchain/Dev/services/auth/src/routes/oauth.ts'
T790='Blockchain/Dev/services/auth/src/__tests__/ks790-token-pre-auth-user-lookup.test.ts'
T820='Blockchain/Dev/services/auth/src/__tests__/ks820-821-token-client-auth-and-apptype.test.ts'
UREPO='Blockchain/Dev/services/auth/src/repositories/userRepo.ts'
JWT='Blockchain/Dev/services/auth/src/services/jwt.ts'
INDEX='Blockchain/Dev/services/auth/src/index.ts'
for ref,tag in [(HEAD,'head'),(M18,'m18')]:
    for p in [OAUTH, T790, T820, UREPO, JWT, INDEX]:
        try:
            o=get(f'/contents/{p}?ref={ref}')
            raw=base64.b64decode(o['content'])
            short=p.split('/')[-1]
            open(f"{G}/model/{short}.api.{ref[:9]}",'wb').write(raw)
            print(f"  contents {ref[:9]} {short}: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x<0x20 and x not in (9,10,13)) or x==0x7f)} getUserById(={raw.count(b'userRepo.getUserById(')} getUserByIdPreAuth(={raw.count(b'getUserByIdPreAuth(')} require(={raw.count(b'require(')}")
        except urllib.error.HTTPError as e:
            print(f"  contents {ref[:9]} {p.split('/')[-1]}: ABSENT (HTTP {e.code})")
# the stack and the sibling, for the record
for n in [983, 984, 881]:
    p=get(f'/pulls/{n}'); save(f'pr{n}.json', p)
    print(f"PR #{n}: state={p['state']} draft={p['draft']} merged={p['merged']} base={p['base']['ref']}@{p['base']['sha'][:9]} head={p['head']['sha'][:9]} branch={p['head']['ref'][:80]} commits={p['commits']} files={p['changed_files']} mergeable={p['mergeable']}/{p['mergeable_state']} title={p['title'][:100]!r}")
c983=get(f"/compare/{HEAD}...{get('/pulls/983')['head']['sha']}"); save('compare_982_983.json', c983)
print(f"compare #982 head...#983 head: status={c983['status']} ahead={c983['ahead_by']} behind={c983['behind_by']} files={[f['filename'] for f in c983['files']]}")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
