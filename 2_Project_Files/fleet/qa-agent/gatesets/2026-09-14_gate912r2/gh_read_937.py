#!/usr/bin/env python3
"""gh_read_937.py — READ-ONLY GitHub REST reads for the #937 (stacked on #912) half of the gate set. Token by NAME
(GH_TOKEN) from the Secuura .env in-process; never printed."""
import json, sys, os, urllib.request, urllib.error, base64, hashlib, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G=sys.argv[1]
H937='6fd3a8bec4e4cc858d38925e00703a37ffcf1b30'; H912='609c44c55323b5c90320847b6837ca37f6586705'
MDEV='bda4c74a6deab584df59d9b047f5a1615b2e12a0'; R1_937='cf8b23366f235f37207f7a228a724e9c9cf52fdb'; M18='8861e62161466c40f08d2b10a30edeb203123993'
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
pr=get('/pulls/937'); save('pr937.json',pr)
print(f"PR #937: state={pr['state']} draft={pr['draft']} merged={pr['merged']} author={pr['user']['login']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} created={pr['created_at']} updated={pr['updated_at']} title={pr['title'][:140]!r}")
body=pr['body'] or ''
open(f'{G}/gh/pr937_body.md','w',encoding='utf-8').write(body)
print(f"body chars={len(body)} at-signs={body.count('@')}")
print('KS ids in body:', sorted(set(re.findall(r'KS-\d+', body))))
print('PR refs in body:', sorted(set(re.findall(r'#\d{3,4}', body))))
print('headings:', [l for l in body.splitlines() if l.startswith('#') or l.startswith('> #')])
ack_lines=[l for l in body.splitlines() if '<!--ack:' in l]
print('ack lines:', ack_lines)
print('ack ticked:', [l for l in ack_lines if re.match(r'^- \[[xX]\]', l)])
for tok_ in ['Before merging','- [ ] <!--ack:','PII','Not applicable','6fd3a8bec','609c44c55','bda4c74a6','cf8b23366','8861e6216','a1e49d151','cd8509faf','#934','#912','stack','STACK','inFlight &&','1 failed','3 passed','4 passed','602','57 passed','15/15','package-lock','ancestry','Test Evidence','NOT run','Schemathesis','Akto','node v24','bash 3.2.57','darwin','KS-1059','KS-1004','KS-587','KS-1067','<!-- name -->']:
    print(f"  body count {tok_!r}: {body.count(tok_)}")
files=get('/pulls/937/files?per_page=100'); save('pr937_files.json',files)
for f in files: print(f"  file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
commits=get('/pulls/937/commits?per_page=100'); save('pr937_commits.json',commits)
for c in commits: print(f"  commit {c['sha']} parents={[p['sha'][:9] for p in c['parents']]} {c['commit']['author']['date']} tree={c['commit']['tree']['sha'][:9]} subj={c['commit']['message'].splitlines()[0][:150]!r}")
for c in commits:
    if c['sha'] in (MDEV, H937):
        m=c['commit']['message']; open(f"{G}/gh/commit_{c['sha'][:9]}_msg.txt",'w',encoding='utf-8').write(m)
        print(f"  message {c['sha'][:9]}: KS ids {sorted(set(re.findall(r'KS-\d+', m)))} PR refs {sorted(set(re.findall(r'#\d{3,4}', m)))} at-signs {m.count('@')} chars {len(m)}")
rv=get('/pulls/937/reviews'); print('reviews:', len(rv))
ic=get('/issues/937/comments?per_page=100'); save('pr937_issue_comments.json',ic)
for c in ic:
    b=c['body'] or ''
    open(f"{G}/gh/pr937_comment_{c['id']}_{c['user']['login']}.md",'w',encoding='utf-8').write(b)
    print(f"  issue comment {c['id']} {c['user']['login']} {c['created_at']} chars={len(b)} at-signs={b.count('@')} KS={sorted(set(re.findall(r'KS-\d+', b)))}")
cs=get(f'/compare/{H912}...{H937}'); save('compare_912_937.json',cs)
print(f"compare 912head...937head (THE STACK DELTA): status={cs['status']} merge_base={cs['merge_base_commit']['sha']} ahead={cs['ahead_by']} behind={cs['behind_by']} commits={len(cs['commits'])} files={len(cs['files'])}")
for f in cs['files']: print(f"  stack-delta file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
for c in cs['commits']: print(f"  stack-delta commit {c['sha'][:9]} {c['commit']['message'].splitlines()[0][:100]!r}")
cd=get(f'/compare/develop...{H937}'); save('compare_develop_937.json',cd)
print(f"compare develop...937head: status={cd['status']} merge_base={cd['merge_base_commit']['sha'][:9]} ahead={cd['ahead_by']} behind={cd['behind_by']} files={len(cd['files'])}")
for f in cd['files']: print(f"  dev-delta file {f['status']:9} +{f['additions']} -{f['deletions']} sha={f['sha'][:9]} {f['filename']}")
cm=get(f'/compare/{MDEV}...{H937}'); print(f"compare bda4c74a6...937head (the #912 merge alone): status={cm['status']} ahead={cm['ahead_by']} files={len(cm['files'])}")
cr=get(f'/compare/develop...{R1_937}'); print(f"compare develop...cf8b23366 (round-1 #937 shape): status={cr['status']} merge_base={cr['merge_base_commit']['sha'][:9]} ahead={cr['ahead_by']} behind={cr['behind_by']} files={len(cr['files'])} {[f['filename'].split('/')[-1] for f in cr['files']]}")
p934=get('/pulls/934'); print(f"PR #934: state={p934['state']} merged={p934['merged']} merged_at={p934['merged_at']} merge_commit={p934['merge_commit_sha'][:9] if p934['merge_commit_sha'] else None} head={p934['head']['sha'][:9]}")
p='Blockchain/Dev/services/originate/src/__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts'
for ref in (H937, R1_937, M18, H912):
    try:
        o=get(f'/contents/{p}?ref={ref}'); raw=base64.b64decode(o['content'])
        open(f"{G}/model/api.ks1059.test.ts.{ref[:9]}",'wb').write(raw)
        print(f"  contents {ref[:9]} ks1059: blob={o['sha'][:9]} size={o['size']} sha256={hashlib.sha256(raw).hexdigest()[:16]} lines={raw.count(b'\n')} ctrl={sum(1 for x in raw if (x<0x20 and x not in (9,10,13)) or x==0x7f)} listen(={raw.count(b'listen(')}")
    except urllib.error.HTTPError as e:
        print(f"  contents {ref[:9]} ks1059: ABSENT (HTTP {e.code})")
o=get(f'/contents/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts?ref={H937}')
print(f"  contents {H937[:9]} anchorStateSync.ts: blob={o['sha'][:9]} (expect d8e988f7a = #912's head)")
for lp in ('systemTest/api-explorer/package-lock.json','systemTest/performance/package-lock.json','systemTest/playwright/package-lock.json'):
    a=get(f'/contents/{lp}?ref={H937}')['sha']; b=get(f'/contents/{lp}?ref={M18}')['sha']
    print(f"  lock {lp.split('/')[1]}: 937head {a[:9]} develop {b[:9]} {'SAME' if a==b else 'DIFFER'}")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
