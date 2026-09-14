#!/usr/bin/env python3
"""gh_read_siblings.py — READ-ONLY: the file lists + per-file blob shas of the PRs that may squash onto develop before this
gate launches (#919, #939 = L2 ahead of #813 in the merge order; #805, #922 = L4, also the yaml; #916/#988/#927/#989 = systemTest)
— inputs to the launchers' DEV_CONTENT_ALLOWED tables. Token by NAME (GH_TOKEN); never printed."""
import json, sys, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; G = sys.argv[1]
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
base = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(base + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for n in [int(x) for x in sys.argv[2].split(',')]:
    pr = get(f'/pulls/{n}'); files = get(f'/pulls/{n}/files?per_page=100')
    json.dump({'pr': pr, 'files': files}, open(f'{G}/gh/sibling_pr{n}.json', 'w'), indent=1)
    c = get(f"/compare/develop...{pr['head']['sha']}")
    print(f"PR #{n}: state={pr['state']} merged={pr['merged']} head={pr['head']['sha']} base={pr['base']['sha'][:9]} merge_base={c['merge_base_commit']['sha'][:9]} ahead={c['ahead_by']} behind={c['behind_by']} files={len(files)} mergeable={pr['mergeable']}/{pr['mergeable_state']} title={pr['title'][:70]!r}")
    for f in files:
        print(f"    {f['filename']} {f['status']} +{f['additions']} -{f['deletions']} blob={f['sha']}")
print('done', datetime.datetime.now().astimezone().strftime('%H:%M:%S'))
