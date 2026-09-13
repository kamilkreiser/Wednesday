#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #903 (KS-991) TIER-2 ROUND-2 gate set. Token sourced by NAME (GH_TOKEN)
from the Secuura .env; never printed. Reads: /pulls/903 (+files, commits, reviews, review-comments, issue-comments), compare
develop...head, compare 48553f272...head (the fix commit), /branches/develop, /commits/{head, merge}, the contents API for the
test file / hook / preflight.sh at head, at the merge commit and at develop, the Actions runs at the head SHA with their jobs and
failed steps (attributed, never graded), and /pulls/{918,924,925} for the merge-order record."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G=sys.argv[1]
HEAD='a4f71cde660c1442d98317e26d93845340b20098'; MERGE='48553f272ac503d5b13be6bb1a9b6ba1c7f56586'; R1HEAD='a70f92d7cf24672a0d7de1c2e05e64c0bc38985c'
M18='8861e62161466c40f08d2b10a30edeb203123993'; OLDBASE='986c592d5d4e09f600af43e88cc2b69bc4ca7395'
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
print('classifier positive control:', atclass('hi @kksecura and a[@] and PR #903 @ `sha` and x@y.com'))
pr=get('/pulls/903'); save('pr903.json',pr)
print(f"PR #903: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:160]!r}")
body=pr['body'] or ''
open(f'{G}/gh/pr903_body.md','w',encoding='utf-8').write(body)
print(f"body chars={len(body)} lines={body.count(chr(10))+1} at-signs={body.count('@')} classes={atclass(body)}")
print('KS ids in body:', sorted(set(re.findall(r'KS-\d+', body))))
print('PR refs in body:', sorted(set(re.findall(r'#\d{3,4}', body))))
print('headings:', [l for l in body.splitlines() if l.startswith('#')])
for tok_ in ['Test Evidence','a4f71cde6','48553f272','a70f92d7c','8861e6216','986c592d5','f0748ed56','1b22d4e14','CASE 10','CASE 11','CASE 7','CASE 8','26 passed, 2 failed','23 passed, 5 failed','28 passed, 0 failed','29 passed, 0 failed','T1','T2','T3','CASE 5','Note on scope','does **not** address','DEPS MISSING','env_fail','strict ancestor','diverged','NOT run','Not covered','Migrations','bash 3.2.57','node v24','darwin','PREFLIGHT PASSED','Round 2','round 2','s214','KS-882','KS-854','KS-883','KS-989','KS-909','KS-731','KS-1138','KS-1075','Co-Authored']:
    print(f"  body count {tok_!r}: {body.count(tok_)}")
files=get('/pulls/903/files?per_page=100'); save('pr903_files.json',files)
for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} changes={f['changes']} sha={f['sha'][:9]} {f['filename']}")
commits=get('/pulls/903/commits?per_page=100'); save('pr903_commits.json',commits)
for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['name']} <{c['commit']['author']['email']}> {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:160]!r}")
print('  PR commits count via API:', len(commits))
cm_msg=[c for c in commits if c['sha']==HEAD][0]['commit']['message']; open(f'{G}/gh/commit_head_msg_api.txt','w',encoding='utf-8').write(cm_msg)
print('  head message KS ids:', sorted(set(re.findall(r'KS-\d+', cm_msg))), 'PR refs:', sorted(set(re.findall(r'#\d{3,4}', cm_msg))), 'at-signs:', cm_msg.count('@'), atclass(cm_msg), 'chars', len(cm_msg), 'lines', cm_msg.count('\n')+1)
mg_msg=[c for c in commits if c['sha']==MERGE][0]['commit']['message']
print('  merge message:', repr(mg_msg[:200]), 'KS ids:', sorted(set(re.findall(r'KS-\d+', mg_msg))), 'at-signs:', mg_msg.count('@'))
rv=get('/pulls/903/reviews'); save('pr903_reviews.json',rv); print('reviews:', len(rv), [(r['user']['login'], r['state'], r['submitted_at'], r['commit_id'][:9]) for r in rv])
rc=get('/pulls/903/comments'); save('pr903_review_comments.json',rc); print('review comments:', len(rc))
ic=get('/issues/903/comments?per_page=100'); save('pr903_issue_comments.json',ic)
for c in ic:
    b=c['body'] or ''
    open(f"{G}/gh/pr903_comment_{c['id']}.md",'w',encoding='utf-8').write(b)
    print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} classes={atclass(b)} KS={sorted(set(re.findall(r'KS-\d+', b)))} head-named={HEAD[:9] in b} CASE10={'CASE 10' in b} CASE11={'CASE 11' in b}")
cm=get(f'/compare/develop...{HEAD}'); save('compare_develop_head.json',cm)
print(f"compare develop...head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])} total_commits={cm['total_commits']}")
for f in cm['files']: print(f"  cmp file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
cf=get(f'/compare/{MERGE}...{HEAD}'); save('compare_merge_head.json',cf)
print(f"compare merge...head (the fix commit): status={cf['status']} ahead={cf['ahead_by']} behind={cf['behind_by']} files={len(cf['files'])}: {[(f['filename'], f['additions'], f['deletions'], f['changes']) for f in cf['files']]}")
if cf['files']: print('  patch hunk headers:', re.findall(r'^@@[^\n]*', cf['files'][0].get('patch',''), re.M))
cr=get(f'/compare/{R1HEAD}...{HEAD}'); save('compare_r1head_head.json',cr)
print(f"compare a70f92d7c...head: status={cr['status']} ahead={cr['ahead_by']} behind={cr['behind_by']} files={len(cr['files'])} total_commits={cr['total_commits']}")
bd=get('/branches/develop'); DEV=bd['commit']['sha']; print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:140]))
if DEV != M18:
    cd=get(f'/compare/{M18}...{DEV}'); save('compare_M18_develop.json',cd)
    print(f"compare M18...develop: status={cd['status']} ahead={cd['ahead_by']} files={len(cd['files'])}: {[f['filename'] for f in cd['files']]}")
else:
    print('develop == M18 (no delta to judge)')
for sha,tag in [(HEAD,'head'),(MERGE,'merge')]:
    hc=get(f'/commits/{sha}'); save(f'commit_{tag}.json',hc)
    print(f"{tag} commit {sha[:9]}: parents={[p['sha'] for p in hc['parents']]} files={len(hc['files'])} +{hc['stats']['additions']} -{hc['stats']['deletions']} tree={hc['commit']['tree']['sha'][:9]}")
    if tag=='head':
        for f in hc['files']: print(f"  head-commit file {f['status']:9} +{f['additions']} -{f['deletions']} {f['filename']}")
TF='Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh'
HK='.githooks/pre-push'
PF='Blockchain/Dev/scripts/preflight/preflight.sh'
AB='Blockchain/Dev/scripts/audit/audit-baseline.json'
for ref,tag in [(HEAD,'head'),(MERGE,'merge'),(M18,'m18'),(R1HEAD,'r1head'),(OLDBASE,'oldbase')]:
    for p in [TF, HK, PF, AB]:
        try:
            o=get(f'/contents/{p}?ref={ref}')
            raw=base64.b64decode(o['content'])
            short=p.split('/')[-1]
            open(f"{G}/model/{short}.api.{ref[:9]}",'wb').write(raw)
            print(f"  contents {ref[:9]} {short}: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x<0x20 and x not in (9,10,13)) or x==0x7f)} KS-991={raw.count(b'KS-991')} 'CASE 10'={raw.count(b'CASE 10')} 'CASE 11'={raw.count(b'CASE 11')} _refs==={raw.count(b'_refs=')} is-ancestor={raw.count(b'merge-base --is-ancestor develop origin/develop')}")
        except urllib.error.HTTPError as e:
            print(f"  contents {ref[:9]} {p.split('/')[-1]}: ABSENT (HTTP {e.code})")
# Actions at the head — attributed, never graded
runs=get(f'/actions/runs?head_sha={HEAD}&per_page=50'); save('actions_runs_head.json',runs)
print(f"actions runs at head: {runs['total_count']}")
out=[]
for r in runs['workflow_runs']:
    jobs=get(f"/actions/runs/{r['id']}/jobs?per_page=50"); save(f"actions_jobs_{r['id']}.json",jobs)
    js=[]
    for j in jobs['jobs']:
        fs=[(s['number'], s['name'], s['conclusion']) for s in j['steps'] if s['conclusion']=='failure']
        js.append({'name':j['name'],'status':j['status'],'conclusion':j['conclusion'],'failed_steps':fs})
    out.append({'run':r['name'],'id':r['id'],'event':r['event'],'status':r['status'],'conclusion':r['conclusion'],'url':r['html_url'],'jobs':js})
    print(f"  run {r['name']!r} id={r['id']} event={r['event']} status={r['status']} conclusion={r['conclusion']} created={r['created_at']}")
    for j in js: print(f"     job {j['name']!r} {j['status']}/{j['conclusion']} failed_steps={j['failed_steps']}")
save('ci_at_head_summary.json', out)
# develop's own latest run of the two red workflows — the control for "develop-own"
for wf in ['PR Security Gates (KS-168)','Security Scanning']:
    dr=get(f'/actions/runs?branch=develop&per_page=100')
    hits=[r for r in dr['workflow_runs'] if r['name']==wf][:3]
    print(f"  develop-branch runs of {wf!r} (newest 3): {[(r['head_sha'][:9], r['status'], r['conclusion'], r['created_at']) for r in hits]}")
    break
save('actions_runs_develop.json', dr)
allwf={}
for r in dr['workflow_runs']:
    allwf.setdefault(r['name'], []).append((r['head_sha'][:9], r['status'], r['conclusion'], r['created_at']))
for k,v in allwf.items(): print(f"  develop runs {k!r}: {v[:3]}")
for n in [918, 924, 925]:
    p=get(f'/pulls/{n}'); save(f'pr{n}.json', p)
    print(f"PR #{n}: state={p['state']} draft={p['draft']} merged={p['merged']} base={p['base']['ref']}@{p['base']['sha'][:9]} head={p['head']['sha'][:9]} branch={p['head']['ref'][:80]} commits={p['commits']} files={p['changed_files']} mergeable={p['mergeable']}/{p['mergeable_state']} updated={p['updated_at']} title={p['title'][:100]!r}")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
