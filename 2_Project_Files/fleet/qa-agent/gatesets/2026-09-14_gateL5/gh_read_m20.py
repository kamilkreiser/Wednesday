#!/usr/bin/env python3
"""gh_read_m20.py — READ-ONLY GitHub REST reads for the L5 gate set's M20 re-pin: /branches/develop, the three compares
against develop (now M20), the stack-parent compare, the M18...M20 and M19...M20 deltas, and the three PRs' state.
Token sourced by NAME (GH_TOKEN) from the Secuura .env; never printed. Raw JSON under <O>/gh/."""
import json, sys, os, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
O = sys.argv[1]; os.makedirs(f'{O}/gh', exist_ok=True)
M18 = '8861e62161466c40f08d2b10a30edeb203123993'; M19 = '6e78961e1d04277ecbdb0537e630afa0bf63b13c'; M20 = 'a5334350221c819f54d4a20a3308daeb9ca09617'
H = {'799': '6da848891924f859179d097d464a7b97c9783a6a', '880': 'a704137de38a3055e40ee62adc343c0239f34ea9', '985': 'fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0'}
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'; print('GH_TOKEN: set (by name)')
base = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(base + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(n, o): open(f'{O}/gh/{n}', 'w', encoding='utf-8').write(json.dumps(o, indent=1, ensure_ascii=False))
print('read at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
b = get('/branches/develop'); save('branches_develop.json', b)
print(f"/branches/develop: {b['commit']['sha']} {b['commit']['commit']['committer']['date']} {b['commit']['commit']['message'].splitlines()[0]!r}")
assert b['commit']['sha'] == M20, 'develop is not M20 — re-read'
for a, c, n in ((M18, M20, 'M18...M20'), (M19, M20, 'M19...M20')):
    x = get(f'/compare/{a}...{c}'); save(f'compare_{n}.json', x)
    print(f"{n}: status {x['status']} ahead {x['ahead_by']} behind {x['behind_by']} files {len(x['files'])}: " + ', '.join(f"{f['filename']} +{f['additions']} -{f['deletions']}" for f in x['files']))
for pr, h in H.items():
    x = get(f'/compare/develop...{h}'); save(f'compare_develop_{pr}.json', x)
    print(f"develop...#{pr} {h[:9]}: merge_base {x['merge_base_commit']['sha'][:9]} status {x['status']} ahead {x['ahead_by']} behind {x['behind_by']} files {len(x['files'])} commits {len(x['commits'])}")
x = get(f"/compare/{H['799']}...{H['985']}"); save('compare_799_985.json', x)
print(f"#799...#985: merge_base {x['merge_base_commit']['sha'][:9]} ahead {x['ahead_by']} behind {x['behind_by']} files {len(x['files'])}")
for pr in H:
    p = get(f'/pulls/{pr}'); save(f'pr{pr}.json', p)
    print(f"#{pr}: state {p['state']} draft {p['draft']} merged {p['merged']} base {p['base']['ref']}@{p['base']['sha'][:9]} head {p['head']['sha'][:9]} {p['head']['ref']} commits {p['commits']} files {p['changed_files']} +{p['additions']} -{p['deletions']} mergeable {p['mergeable']}/{p['mergeable_state']} updated {p['updated_at']} reviews? comments {p['comments']} review_comments {p['review_comments']}")
    assert p['head']['sha'] == H[pr] and p['state'] == 'open' and not p['merged'], f'#{pr} moved'
# Peter's #799 commission comment and the builder's answer — present, unchanged
cs = get('/issues/799/comments?per_page=100'); save('pr799_issue_comments.json', cs)
for c in cs:
    if c['id'] in (5600549339, 5656460918, 5529715057): print(f"#799 comment {c['id']} {c['user']['login']} {c['created_at']} {len(c['body'])} chars at-signs {c['body'].count('@')}")
rv = get('/pulls/799/reviews?per_page=100'); save('pr799_reviews.json', rv); print(f"#799 reviews: {len(rv)} — " + ', '.join(f"{r['id']}@{r['commit_id'][:9]} {r['state']}" for r in rv))
rv = get('/pulls/880/reviews?per_page=100'); save('pr880_reviews.json', rv); print(f"#880 reviews: {len(rv)} — " + ', '.join(f"{r['id']}@{r['commit_id'][:9]} {r['state']}" for r in rv))
rv = get('/pulls/985/reviews?per_page=100'); save('pr985_reviews.json', rv); print(f"#985 reviews: {len(rv)}")
