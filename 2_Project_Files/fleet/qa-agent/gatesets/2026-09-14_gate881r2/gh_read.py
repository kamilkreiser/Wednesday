#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #881 ROUND-2 gate set. Token sourced by NAME (GH_TOKEN) from the
Secuura .env in-process; never printed. Same method as the #980 round-2 set's gh_read.py."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G=sys.argv[1]
HEAD='8ac9db66f6fd0d751f74ecc95bb314210a31ec52'; FIX='ffcea35cb7c478bdc9d9f32e8232251c15d3300e'
R1='787771b97e745a527639241dbad9d164a65325c7'; M18='8861e62161466c40f08d2b10a30edeb203123993'; MB1='306d0db923183f3b62b053f0242549e37bdf362c'
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
print('classifier positive control:', atclass('hi @kksecura and a[@] and PR #881 @ `sha` and x@y.com'))
pr=get('/pulls/881'); save('pr881.json',pr)
print(f"PR #881: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:140]!r}")
body=pr['body'] or ''
open(f'{G}/gh/pr881_body.md','w',encoding='utf-8').write(body)
print(f"body chars={len(body)} at-signs={body.count('@')} classes={atclass(body)}")
print('KS ids in body:', sorted(set(re.findall(r'KS-\d+', body))))
print('PR refs in body:', sorted(set(re.findall(r'#\d{3,4}', body))))
print('headings:', [l for l in body.splitlines() if l.startswith('#')])
for tok_ in ['Round 2','round 2','s212','8ac9db66f','ffcea35cb','787771b97','8861e6216','consent.js','CONSENT_SUBMIT_SCRIPT','<script src','inline','nonce','helmet','script-src','nginx','jsdom','4 failed','8 passed','12','24/24','703','613','54/703','47/613','T1','T2','T3','3/3/2','audit:gate','audit:locks','NOT run','Not covered','Migrations','CORS_ORIGINS','OpenAPI','allowedHeaders','Playwright','KS-799','KS-798','KS-841','KS-781','KS-245','KS-797','KS-804','KS-822','KS-1003','KS-1139','KS-1135','KS-1138']:
    print(f"  body count {tok_!r}: {body.count(tok_)}")
files=get('/pulls/881/files?per_page=100'); save('pr881_files.json',files)
for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
commits=get('/pulls/881/commits?per_page=100'); save('pr881_commits.json',commits)
for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['name']} <{c['commit']['author']['email']}> {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:160]!r}")
for c in commits:
    if c['sha'] in (FIX, HEAD):
        m=c['commit']['message']; open(f"{G}/gh/commit_{c['sha'][:9]}_msg.txt",'w',encoding='utf-8').write(m)
        print(f"  message {c['sha'][:9]}: KS ids {sorted(set(re.findall(r'KS-\d+', m)))} PR refs {sorted(set(re.findall(r'#\d{3,4}', m)))} at-signs {m.count('@')} {atclass(m)} chars {len(m)} lines {m.count(chr(10))+1}")
rv=get('/pulls/881/reviews'); save('pr881_reviews.json',rv); print('reviews:', len(rv))
for r in rv: print(f"  review {r['id']} {r['user']['login']} {r['state']} commit={r['commit_id']} at={r['submitted_at']} chars={len(r['body'] or '')} at-signs={(r['body'] or '').count('@')}")
rc=get('/pulls/881/comments'); save('pr881_review_comments.json',rc); print('review comments:', len(rc))
ic=get('/issues/881/comments?per_page=100'); save('pr881_issue_comments.json',ic)
for c in ic:
    b=c['body'] or ''
    open(f"{G}/gh/pr881_comment_{c['id']}.md",'w',encoding='utf-8').write(b)
    print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))} head-mention={HEAD[:9] in b} fix={FIX[:9] in b} r1={R1[:9] in b}")
cm=get(f'/compare/develop...{HEAD}'); save('compare_develop_head.json',cm)
print(f"compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])}")
for f in cm['files']: print(f"  cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
c12=get(f'/compare/{R1}...{FIX}'); save('compare_r1_fix.json',c12)
print(f"compare r1...fix: status={c12['status']} ahead={c12['ahead_by']} behind={c12['behind_by']} commits={len(c12['commits'])} files={len(c12['files'])}")
for f in c12['files']: print(f"  fix file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']} changes={f['changes']}")
c1h=get(f'/compare/{R1}...{HEAD}'); save('compare_r1_head.json',c1h)
print(f"compare r1...head: status={c1h['status']} ahead={c1h['ahead_by']} behind={c1h['behind_by']} commits={len(c1h['commits'])} files={len(c1h['files'])}")
bd=get('/branches/develop'); DEV=bd['commit']['sha']; print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:120]))
cmm=get(f'/compare/{M18}...{DEV}'); print(f"compare M18...develop-now: status={cmm['status']} ahead={cmm['ahead_by']} behind={cmm['behind_by']} files={len(cmm['files'])}")
hc=get(f'/commits/{HEAD}'); save('commit_head.json',hc)
print(f"head commit: parents={[p['sha'] for p in hc['parents']]} files={len(hc['files'])} +{hc['stats']['additions']} -{hc['stats']['deletions']}")
fc=get(f'/commits/{FIX}'); save('commit_fix.json',fc)
print(f"fix commit: parents={[p['sha'] for p in fc['parents']]} files={len(fc['files'])} +{fc['stats']['additions']} -{fc['stats']['deletions']}")
for f in fc['files']: print(f"  fix-commit file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
P='Blockchain/Dev/services/auth/src/'
PATHS=[P+'routes/oauth.ts', P+'__tests__/ks799-consent-form-csrf-submit.test.ts', P+'__tests__/ks799-consent-script-csp-and-execution.test.ts',
       P+'__tests__/ks798-consent-form-client-id.test.ts', P+'__tests__/ks841-consent-form-pkce-and-client-id.test.ts',
       P+'__tests__/ks781-n1-empty-mfacode-treated-as-absent.test.ts', P+'index.ts']
for ref,tag in [(HEAD,'head'),(FIX,'fix'),(R1,'r1'),(M18,'dev')]:
    for p in PATHS:
        try:
            o=get(f'/contents/{p}?ref={ref}')
            raw=base64.b64decode(o['content'])
            short=p.split('/')[-1]
            open(f"{G}/model/api.{short}.{ref[:9]}",'wb').write(raw)
            print(f"  contents {ref[:9]} {short}: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x<0x20 and x not in (9,10,13)) or x==0x7f)} listen(={raw.count(b'listen(')} consent.js={raw.count(b'consent.js')}")
        except urllib.error.HTTPError as e:
            print(f"  contents {ref[:9]} {p.split('/')[-1]}: ABSENT (HTTP {e.code})")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
