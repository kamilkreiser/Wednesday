#!/usr/bin/env python3
"""make_sim_gate56a.py — build the gate56a SIM fixtures (EXERCISE INPUT ONLY, never evidence of a PR).
It writes:
  (a) in a SCRATCH repo (--simrepo, a `git clone --shared -n` of a scratch clone that holds kit base): four commits made with plumbing
      (hash-object -w / read-tree / update-index / write-tree / commit-tree under a scratch GIT_INDEX_FILE) — no working tree, no checkout:
        good3  = kit base + PR 3's intended edit (the two expires -> 2026-10-31), subject = kit pr3 subject, no trailer
        good4  = kit base + PR 4's intended edit (expires -> 2027-01-01), subject = kit pr4 subject, no trailer
        bad4   = kit base + PR 4 with 2026-12-31 AND a Co-Authored-By trailer AND a ` (#9904)` subject suffix (C1 P5/P6 must FAIL)
        dev3   = good3 re-parented as "develop after PR 3 squashed" (same tree, same exact subject) for the SIBLING-ADVANCE arm
  (b) under this kit's sim/: pr_<n>.json + files_<n>.json (PULLS API replays: 9903 good3, 9904 good4, 9905 bad4), lsremote_*.txt replays,
      SIM_body_pr3.md / SIM_body_pr4.md (bodies written by the drafter from the briefs; NOT the seat's bodies), and sim_shas.json.
REFUSES (before writing anything) a --simrepo inside /Volumes/DevMASTER/!CODING/. The Secuura checkout is never touched.
Usage: make_sim_gate56a.py --source <scratch clone holding kit base> --simrepo <scratch dir> --syn <dir with baseline.good.json, lockdisc.good.mjs, lockdisc.wrong1231.mjs>"""
import json, os, subprocess, sys
G = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SIMD = os.path.join(G, 'sim')
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]
def opt(n): return A[A.index(n) + 1] if n in A else None
SRC, SR, SYN = opt('--source'), opt('--simrepo'), opt('--syn')
if not (SRC and SR and SYN):
    print(__doc__); raise SystemExit(2)
for p in (SRC, SR, SYN):
    if os.path.realpath(os.path.abspath(p)).startswith('/Volumes/DevMASTER/!CODING/') or os.path.abspath(p).startswith('/Volumes/DevMASTER/!CODING/'):
        print('REFUSING: %s is inside /Volumes/DevMASTER/!CODING/ (nothing was created)' % p); raise SystemExit(2)
if not os.path.isdir(SR):
    subprocess.run(['git', 'clone', '-q', '--shared', '-n', SRC, SR], check=True)
IDX = os.path.join(SR, '.sim_index')
ENV = dict(os.environ, GIT_INDEX_FILE=IDX, GIT_AUTHOR_NAME='SIM gate56a drafter', GIT_AUTHOR_EMAIL='sim@invalid', GIT_COMMITTER_NAME='SIM gate56a drafter',
           GIT_COMMITTER_EMAIL='sim@invalid', GIT_AUTHOR_DATE='2026-10-05T00:00:00Z', GIT_COMMITTER_DATE='2026-10-05T00:00:00Z')
def g(*a, inp=None):
    return subprocess.run(['git', '-C', SR] + list(a), capture_output=True, text=True, env=ENV, input=inp, check=True).stdout.strip()
def commit(path, src_file, parent, msg):
    g('read-tree', K['base'])
    blob = g('hash-object', '-w', src_file)
    g('update-index', '--cacheinfo', '100644,%s,%s' % (blob, path))
    tree = g('write-tree')
    return g('commit-tree', tree, '-p', parent, '-m', msg), tree
P3, P4 = K['prs']['pr3'], K['prs']['pr4']
good3, t3 = commit(P3['path'], os.path.join(SYN, 'baseline.good.json'), K['base'], P3['subject'])
good4, t4 = commit(P4['path'], os.path.join(SYN, 'lockdisc.good.mjs'), K['base'], P4['subject'])
bad4, tb = commit(P4['path'], os.path.join(SYN, 'lockdisc.wrong1231.mjs'), K['base'], P4['subject'] + ' (#9905)\n\nCo-Authored-By: Somebody <x@invalid>')
dev3 = good3
shas = {'base': K['base'], 'good3': good3, 'good4': good4, 'bad4': bad4, 'dev3_sibling_advance': dev3, 'trees': {'good3': t3, 'good4': t4, 'bad4': tb}}
json.dump(shas, open(os.path.join(SIMD, 'sim_shas.json'), 'w'), indent=1)
def numstat(a, b):
    out = []
    for l in g('diff', '--numstat', a, b).splitlines():
        x = l.split('\t'); out.append({'filename': x[2], 'additions': int(x[0]), 'deletions': int(x[1])})
    return out
B3 = open(os.path.join(SIMD, 'SIM_body_pr3.md'), encoding='utf-8').read(); B4 = open(os.path.join(SIMD, 'SIM_body_pr4.md'), encoding='utf-8').read()
def pr(n, head, br, title, body, base_sha):
    d = os.path.join(SIMD, 'pr%d' % n); os.makedirs(d, exist_ok=True)
    json.dump({'number': n, 'state': 'open', 'merged': False, 'mergeable': True, 'mergeable_state': 'clean', 'title': title, 'body': body,
               'user': {'login': 'SIM'}, 'created_at': '2026-10-05T00:00:00Z', 'base': {'ref': 'develop', 'sha': base_sha}, 'head': {'sha': head, 'ref': br}},
              open(os.path.join(d, 'pr_%d.json' % n), 'w'), indent=1)
    json.dump(numstat(head + '^', head), open(os.path.join(d, 'files_%d.json' % n), 'w'), indent=1)
    json.dump([], open(os.path.join(d, 'pulls.json'), 'w'))
pr(9903, good3, 'feature/ks-528-react-router-rows-redate-b59-3', P3['subject'], B3, K['base'])
pr(9904, good4, 'feature/ks-769-mobile-exclusion-redate-b59-4', P4['subject'], B4, K['base'])
pr(9905, bad4, 'feature/ks-769-mobile-exclusion-redate-b59-4', P4['subject'] + ' (#9905)', B4.replace('Refs KS-769', 'Refs KS-769\nalso KS-528'), K['base'])
pr(99041, good4, 'feature/ks-769-mobile-exclusion-redate-b59-4', P4['subject'], B4, dev3)
open(os.path.join(SIMD, 'lsremote_ok.txt'), 'w').write('%s\trefs/heads/develop\n%s\trefs/pull/9903/head\n%s\trefs/heads/feature/ks-528-react-router-rows-redate-b59-3\n%s\trefs/pull/9904/head\n%s\trefs/heads/feature/ks-769-mobile-exclusion-redate-b59-4\n' % (K['base'], good3, good3, good4, good4))
open(os.path.join(SIMD, 'lsremote_bad4.txt'), 'w').write('%s\trefs/heads/develop\n%s\trefs/pull/9905/head\n%s\trefs/heads/feature/ks-769-mobile-exclusion-redate-b59-4\n' % (K['base'], bad4, bad4))
open(os.path.join(SIMD, 'lsremote_sibling.txt'), 'w').write('%s\trefs/heads/develop\n%s\trefs/pull/99041/head\n%s\trefs/heads/feature/ks-769-mobile-exclusion-redate-b59-4\n' % (dev3, good4, good4))
print('SIM BUILT in %s (scratch) + %s: %s' % (SR, SIMD, json.dumps(shas)))
