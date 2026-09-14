#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #989 gate set (KS-973; head 9d0e2016a; develop M38).
Token sourced by NAME (GH_TOKEN) from the Secuura .env; never printed. Raw JSON under <G>/gh/."""
import json, sys, urllib.request, datetime, re
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
N = 989; HEAD = '9d0e2016ae60658ec908ee5e500583fd3a318c8a'; M38 = '0e78c7270188ac45c1c29f927bdf90728f10215d'
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
dev = get('/branches/develop'); print('origin develop (API) =', dev['commit']['sha'], 'M38' if dev['commit']['sha'] == M38 else 'NOT M38')
pr = get(f'/pulls/{N}'); save(f'pr{N}.json', pr)
body = pr['body'] or ''
open(f'{G}/gh/pr{N}_body.md', 'w', encoding='utf-8').write(body)
ats = len(re.findall(r'(?<![\w\[])@[A-Za-z][\w-]*', body))
print(f"PR #{N}: state={pr['state']} draft={pr['draft']} merged={pr['merged']} base={pr['base']['ref']}@{pr['base']['sha'][:9]} head={pr['head']['sha']} {'==pin' if pr['head']['sha']==HEAD else 'MOVED'} branch={pr['head']['ref']} commits={pr['commits']} files={pr['changed_files']} +{pr['additions']} -{pr['deletions']} mergeable={pr['mergeable']}/{pr['mergeable_state']} body_chars={len(body)} body_mentions={ats} updated={pr['updated_at']} title={pr['title'][:110]!r}")
for tag in ('<!--ack:schemathesis-->', '<!--ack:akto-->', 'linear.app/secuura/issue/KS-', '## Test Evidence', 'redactSecrets', '+332', 'items 3/4', 'OPEN', 'format', 'prettier'):
    print(f"   body count {tag!r} = {body.count(tag)}")
c = get(f'/pulls/{N}/commits'); save(f'pr{N}_commits.json', c)
print("   commits: " + ' '.join(x['sha'][:9] + '(' + ','.join(p['sha'][:9] for p in x['parents']) + ')' for x in c))
files = get(f'/pulls/{N}/files?per_page=100'); save(f'pr{N}_files.json', files)
print('   files: ' + ' '.join(f"{f['filename'].split('/')[-1]}:{f['status'][0]}+{f['additions']}-{f['deletions']} sha={f['sha'][:9]}" for f in files))
revs = get(f'/pulls/{N}/reviews'); save(f'pr{N}_reviews.json', revs)
for r in revs:
    print(f"   review {r['id']} {r['state']} by {r['user']['login']} commit_id={r['commit_id'][:9]} {'==head' if r['commit_id']==HEAD else '!=head'} at {r['submitted_at']} body_chars={len(r['body'] or '')}")
ics = get(f'/issues/{N}/comments?per_page=100'); save(f'pr{N}_issue_comments.json', ics)
for x in ics:
    print(f"   comment {x['id']} by {x['user']['login']} at {x['created_at']} chars={len(x['body'])} at_signs={x['body'].count('@')} first={x['body'][:90]!r}")
rcs = get(f'/pulls/{N}/comments?per_page=100'); save(f'pr{N}_review_comments.json', rcs)
print(f"   review comments: {len(rcs)}")
def cmp(a, b, tag):
    c = get(f'/compare/{a}...{b}'); save(f'compare_{tag}.json', c)
    print(f"compare {tag}: merge_base={c['merge_base_commit']['sha']} status={c['status']} ahead={c['ahead_by']} behind={c['behind_by']} commits={len(c['commits'])} files={len(c.get('files') or [])}: " + ' '.join(f"{f['filename'].split('/')[-1]}={f['sha'][:9]}" for f in (c.get('files') or [])))
cmp('develop', HEAD, 'dev_989')
for f in ('systemTest/fixtures/provision.ts', 'systemTest/fixtures/pre-suite.ts', 'systemTest/fixtures/provision-actors.ts', 'systemTest/fixtures/manifest.ts', 'systemTest/fixtures/actors.ts', 'systemTest/performance/vitest.unit.config.ts', 'systemTest/performance/package-lock.json', 'systemTest/performance/tests/unit/fixtures/provisionRedaction.test.ts', 'systemTest/performance/tests/unit/fixtures/preSuiteStreams.test.ts', 'systemTest/performance/tests/unit/fixtures/provisionDriftQuarantine.test.ts', 'systemTest/__tests__/pre_suite.test.sh'):
    for ref, lab in ((M38, 'M38'), (HEAD, 'head')):
        try:
            j = get('/contents/' + f + '?ref=' + ref)
            print(f'{lab} blob {f.split("/")[-1]} = {j["sha"]} size={j["size"]}')
        except Exception as e:
            print(f'{lab} blob {f.split("/")[-1]} = ABSENT ({type(e).__name__})')
# #927 (L13) — does it touch the two fixture files? (the READY says #989 is independent of #927)
p927 = get('/pulls/927'); save('pr927.json', p927)
print(f"PR #927: state={p927['state']} merged={p927['merged']} head={p927['head']['sha'][:9]} files={p927['changed_files']} base={p927['base']['ref']}")
f927 = get('/pulls/927/files?per_page=100'); save('pr927_files.json', f927)
print('   #927 files: ' + ' '.join(f['filename'] for f in f927))
for n in (916, 988):
    pp = get(f'/pulls/{n}'); ff = get(f'/pulls/{n}/files?per_page=100'); save(f'pr{n}_files.json', ff)
    print(f"PR #{n}: state={pp['state']} merged={pp['merged']} head={pp['head']['sha'][:9]} files: " + ' '.join(f['filename'] for f in ff))
print('done', datetime.datetime.now().astimezone().strftime('%H:%M:%S'))
