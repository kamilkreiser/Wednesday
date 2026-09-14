#!/usr/bin/env python3
"""gh_read.py — READ-ONLY GitHub REST reads for the #813 gate set (KS-791; head 7b6fb960d; develop M38).
Token sourced by NAME (GH_TOKEN) from the Secuura .env; never printed. Raw JSON under <G>/gh/."""
import json, sys, urllib.request, datetime, re
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
N = 813; HEAD = '7b6fb960dafd6c27af1eb9bad2a031f6bfe3a3a4'; M38 = '0e78c7270188ac45c1c29f927bdf90728f10215d'
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
for tag in ('<!--ack:schemathesis-->', '<!--ack:akto-->', 'linear.app/secuura/issue/KS-', '## Test Evidence', 'minLength', 'Schemathesis', 'Akto', 'Playwright'):
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
cmp('develop', HEAD, 'dev_813')
for f in ('services/api-gateway/src/middleware/contentType.ts', 'services/api-gateway/src/__tests__/contentType.test.ts', 'services/originate/src/originate.openapi.ts', 'docs/openapi/secuura-api.yaml', 'services/api-gateway/src/middleware/csrf.ts', 'services/api-gateway/src/index.ts', 'scripts/generate-openapi.ts', 'package-lock.json'):
    for ref, lab in ((M38, 'M38'), (HEAD, 'head')):
        j = get('/contents/Blockchain/Dev/' + f + '?ref=' + ref)
        print(f'{lab} blob {f.split("/")[-1]} = {j["sha"]} size={j["size"]}')
print('done', datetime.datetime.now().astimezone().strftime('%H:%M:%S'))
