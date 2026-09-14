#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #912 ROUND-2 (tier 1) gate set. Token sourced by NAME (GH_TOKEN)
from the Secuura .env in-process; never printed. Same method as the #881 round-2 set's gh_read.py."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G=sys.argv[1]
HEAD='609c44c55323b5c90320847b6837ca37f6586705'; MERGE='3231514154aaa8a469e6cdd5f553ee8ce6079b89'
R1='ae8751f380ed361505694ba71ad9bf1308ee0e87'; M18='8861e62161466c40f08d2b10a30edeb203123993'; MB1='e559f7bbace5281668637755410273ff58068c15'
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
print('classifier positive control:', atclass('hi @kksecura and a[@] and PR #912 @ `sha` and x@y.com'))
try:
    get('/pulls/99999'); print('NEGATIVE CONTROL FAILED: /pulls/99999 answered')
except urllib.error.HTTPError as e:
    print('negative control /pulls/99999 ->', e.code)
pr=get('/pulls/912'); save('pr912.json',pr)
print(f"PR #912: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:140]!r}")
body=pr['body'] or ''
open(f'{G}/gh/pr912_body.md','w',encoding='utf-8').write(body)
print(f"body chars={len(body)} at-signs={body.count('@')} classes={atclass(body)}")
print('KS ids in body:', sorted(set(re.findall(r'KS-\d+', body))))
print('PR refs in body:', sorted(set(re.findall(r'#\d{3,4}', body))))
print('headings:', [l for l in body.splitlines() if l.startswith('#') or l.startswith('> #')])
ack_lines=[l for l in body.splitlines() if '<!--ack:' in l]
print('ack lines:', ack_lines)
print('ack ticked (regex ^- \\[[xX]\\]):', [l for l in ack_lines if re.match(r'^- \[[xX]\]', l)])
for tok_ in ['Before merging','<!--ack:schemathesis-->','<!--ack:akto-->','- [ ] <!--ack:','- [x] <!--ack:','- [X] <!--ack:','PII','Not applicable','originate.openapi.ts:601','z.unknown().nullable()','609c44c55','323151415','ae8751f38','8861e6216','27509dc7a','1cc021a44','039da8d6e','163ca2c74','anchoredAt','threadToken','confidence','narrow','Test Evidence','NOT run','Not run','Schemathesis','Akto','Playwright','k6','node v24','bash 3.2.57','darwin','55 passed','598','56 passed','2 failed','4 passed','T1','T2','T3','T4','4/4','tsc','eslint','Migrations','migrations','KS-1004','KS-1017','KS-1019','KS-587','KS-1058','KS-1057','KS-1071','KS-1068','KS-535','KS-520','5602883901','5597511879','5656435630','<!-- name -->','<!-- @who -->']:
    print(f"  body count {tok_!r}: {body.count(tok_)}")
files=get('/pulls/912/files?per_page=100'); save('pr912_files.json',files)
for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
commits=get('/pulls/912/commits?per_page=100'); save('pr912_commits.json',commits)
for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['name']} <{c['commit']['author']['email']}> {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:160]!r}")
for c in commits:
    m=c['commit']['message']; open(f"{G}/gh/commit_{c['sha'][:9]}_msg.txt",'w',encoding='utf-8').write(m)
    print(f"  message {c['sha'][:9]}: KS ids {sorted(set(re.findall(r'KS-\d+', m)))} PR refs {sorted(set(re.findall(r'#\d{3,4}', m)))} at-signs {m.count('@')} {atclass(m)} chars {len(m)} lines {m.count(chr(10))+1}")
rv=get('/pulls/912/reviews'); save('pr912_reviews.json',rv); print('reviews:', len(rv))
for r in rv: print(f"  review {r['id']} {r['user']['login']} {r['state']} commit={r['commit_id']} at={r['submitted_at']} chars={len(r['body'] or '')} at-signs={(r['body'] or '').count('@')}")
rc=get('/pulls/912/comments'); save('pr912_review_comments.json',rc); print('review comments:', len(rc))
ic=get('/issues/912/comments?per_page=100'); save('pr912_issue_comments.json',ic)
for c in ic:
    b=c['body'] or ''
    open(f"{G}/gh/pr912_comment_{c['id']}_{c['user']['login']}.md",'w',encoding='utf-8').write(b)
    print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} sha256={hashlib.sha256(b.encode()).hexdigest()[:16]} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))} PRs={sorted(set(re.findall(r'#\d{3,4}', b)))} head={HEAD[:9] in b} merge={MERGE[:9] in b} r1={R1[:9] in b} NOGO={b.count('NO GO')} F1={b.count('F1')}")
cm=get(f'/compare/develop...{HEAD}'); save('compare_develop_head.json',cm)
print(f"compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])}")
for f in cm['files']: print(f"  cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
c12=get(f'/compare/{MERGE}...{HEAD}'); save('compare_merge_head.json',c12)
print(f"compare merge...head (the fix commit): status={c12['status']} ahead={c12['ahead_by']} behind={c12['behind_by']} commits={len(c12['commits'])} files={len(c12['files'])}")
for f in c12['files']: print(f"  fix file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']} changes={f['changes']}")
c1h=get(f'/compare/{R1}...{HEAD}'); save('compare_r1_head.json',c1h)
print(f"compare r1...head: status={c1h['status']} ahead={c1h['ahead_by']} behind={c1h['behind_by']} commits={len(c1h['commits'])} files={len(c1h['files'])} (develop's side included)")
c1m=get(f'/compare/develop...{R1}'); save('compare_develop_r1.json',c1m)
print(f"compare develop...r1: status={c1m['status']} merge_base={c1m['merge_base_commit']['sha'][:9]} ahead={c1m['ahead_by']} behind={c1m['behind_by']} files={len(c1m['files'])}")
bd=get('/branches/develop'); DEV=bd['commit']['sha']; print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:120]))
cmm=get(f'/compare/{M18}...{DEV}'); print(f"compare M18...develop-now: status={cmm['status']} ahead={cmm['ahead_by']} behind={cmm['behind_by']} files={len(cmm['files'])}")
hc=get(f'/commits/{HEAD}'); save('commit_head.json',hc)
print(f"head commit: parents={[p['sha'] for p in hc['parents']]} files={len(hc['files'])} +{hc['stats']['additions']} -{hc['stats']['deletions']}")
for f in hc['files']: print(f"  head-commit file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
mc=get(f'/commits/{MERGE}'); save('commit_merge.json',mc)
print(f"merge commit: parents={[p['sha'] for p in mc['parents']]} files={len(mc['files'])} +{mc['stats']['additions']} -{mc['stats']['deletions']} (the API diffs a merge against its FIRST parent = develop's side)")
# other PRs this gate must know
for n in (937, 939):
    p=get(f'/pulls/{n}'); save(f'pr{n}.json',p)
    fl=get(f'/pulls/{n}/files?per_page=100'); save(f'pr{n}_files.json',fl)
    print(f"PR #{n}: state={p['state']} head={p['head']['sha'][:9]} branch={p['head']['ref'][:60]} mergeable={p['mergeable']}/{p['mergeable_state']} updated={p['updated_at']} files={[ (f['filename'].split('/')[-1], f['additions'], f['deletions']) for f in fl]}")
P='Blockchain/Dev/services/originate/src/'
PATHS=[P+'services/anchorStateSync.ts', P+'__tests__/ks1004-anchor-failed-lockout.test.ts', P+'__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts',
       P+'__tests__/ks535-anchor-async-fail-propagates.test.ts', P+'repositories/documentRepo.ts', 'Blockchain/Dev/services/api-gateway/src/routes/verification.ts',
       'Blockchain/Dev/scripts/audit/audit-baseline.json']
for ref,tag in [(HEAD,'head'),(MERGE,'merge'),(R1,'r1'),(M18,'dev')]:
    for p in PATHS:
        try:
            o=get(f'/contents/{p}?ref={ref}')
            raw=base64.b64decode(o['content'])
            short=p.split('/')[-1]
            open(f"{G}/model/api.{short}.{ref[:9]}",'wb').write(raw)
            print(f"  contents {ref[:9]} {short}: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x<0x20 and x not in (9,10,13)) or x==0x7f)} listen(={raw.count(b'listen(')} anchoredAt={raw.count(b'anchoredAt')}")
        except urllib.error.HTTPError as e:
            print(f"  contents {ref[:9]} {p.split('/')[-1]}: ABSENT (HTTP {e.code})")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
