#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #931 (KS-1061) TIER-2 ROUND-1 gate set. Token sourced by NAME
(GH_TOKEN) from the Secuura .env; never printed. Reads: /pulls/931 (+files, commits, reviews, review-comments,
issue-comments), compare develop...head, /commits/{head}."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G=sys.argv[1]
# RE-PIN PATH: override via QA931_HEAD to re-read a NEW head (e.g. after the builder's ks695/develop
# re-merge) without editing this file — see BUILD_REPORT.md "THE RE-PIN PATH".
HEAD=os.environ.get('QA931_HEAD', '53b8a1f7a6056c1560af71252c753c005bee8f06')
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
print('classifier positive control:', atclass('hi @kksecura and a[@] and PR #931 @ `sha` and x@y.com'))
pr=get('/pulls/931'); save('pr931.json',pr)
print(f"PR #931: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:160]!r}")
assert pr['head']['sha']==HEAD, f"head mismatch: API says {pr['head']['sha']}, expected {HEAD}"
body=pr['body'] or ''
open(f'{G}/gh/pr931_body.md','w',encoding='utf-8').write(body)
print(f"body chars={len(body)} lines={body.count(chr(10))+1} at-signs={body.count('@')} classes={atclass(body)}")
print('KS ids in body:', sorted(set(re.findall(r'KS-\d+', body))))
print('PR refs in body:', sorted(set(re.findall(r'#\d{3,4}', body))))
print('headings:', [l for l in body.splitlines() if l.startswith('#')])
for tok_ in ['Test Evidence','makeSharedMock','ks1103','ks764','ks444','KS-927','assertSafeOutboundUrl','57 / 601','56 / 598','601','598','PREFLIGHT PASSED','red-first','Tamper','tamper','dirty','mergeable','Co-Authored','KS-1061']:
    print(f"  body count {tok_!r}: {body.count(tok_)}")
files=get('/pulls/931/files?per_page=100'); save('pr931_files.json',files)
for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} changes={f['changes']} sha={f['sha'][:9]} {f['filename']}")
print('  file count via API:', len(files))
commits=get('/pulls/931/commits?per_page=100'); save('pr931_commits.json',commits)
for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['name']} <{c['commit']['author']['email']}> {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:160]!r}")
print('  PR commits count via API:', len(commits))
rv=get('/pulls/931/reviews'); save('pr931_reviews.json',rv); print('reviews:', len(rv), [(r['user']['login'], r['state'], r['submitted_at'], r['commit_id'][:9]) for r in rv])
rc=get('/pulls/931/comments'); save('pr931_review_comments.json',rc); print('review comments:', len(rc))
ic=get('/issues/931/comments?per_page=100'); save('pr931_issue_comments.json',ic)
for c in ic:
    b=c['body'] or ''
    open(f"{G}/gh/pr931_comment_{c['id']}.md",'w',encoding='utf-8').write(b)
    print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))}")
cm=get(f'/compare/develop...{HEAD}'); save('compare_develop_head.json',cm)
print(f"compare develop...{HEAD[:9]}: status={cm['status']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])} merge_base_commit={cm['merge_base_commit']['sha']}")
for fchg in cm['files']: print(f"    cmp-file {fchg['filename']} status={fchg['status']}")
hc=get(f'/commits/{HEAD}'); save('commit_head.json', hc)
print('head commit verified:', hc['sha'], hc['commit']['message'].splitlines()[0][:160])
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
