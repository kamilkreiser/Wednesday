#!/usr/bin/env python3
"""repin_base_gateD2.py — the gateD2 answer to "develop moved since the builder's base" (#1374 KS-1402 squashes first): it REFUSES to guess.
It reads, read-only, the GitHub compare kit-base...<new develop> and the commits API (and nothing is fetched or written in any repo), then:
  R1 the new develop DESCENDS from kit base (compare status ahead, behind 0), each commit listed with its subject;
  R2 NO non-doc kit path moved: none of kit files (except the two platform-k docs), kit unchanged_must_equal, anything under
     services/timestamping/, kit pr0_files_all, or scripts/audit/** is in the compare's file list — any one of them is a RE-DRAFT (rc 1):
     the lock / baseline / source expectations were drafted against the old blobs;
  R3 prints the PROPOSED kit.json edits: base, base_tree, base_parent (= old base), the two docs' new base_blobs (blob shas from the compare),
     base_history += the old base; and states what the re-pin does NOT change (cells / suites / locks: their files are blob-equal).
--write (Wednesday's act, after reading the report): backs kit.json up to kit.json.pre-repin-<UTC> (never deleted) and writes the edits.
The launch action still re-reads develop and refuses (rc 10) until kit base == develop; the BUILDER must also rebase onto it (C1 P3).
Usage: repin_base_gateD2.py --new-develop <40-hex> [--write]   rc 0 clean re-pin (written or proposed) / 1 RE-DRAFT / 2 usage / 3 API"""
import json, os, re, sys, shutil, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gateD2 import K, G, gh_token, gh_get, now

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--new-develop' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
ND = A[A.index('--new-develop') + 1]
if not re.fullmatch(r'[0-9a-f]{40}', ND): print('REFUSING: --new-develop must be 40 lowercase hex'); raise SystemExit(2)
OB = K['base']
print('repin_base_gateD2 %s | kit base %s -> proposed %s | mode %s' % (now(), OB[:12], ND[:12], 'WRITE' if '--write' in A else 'report only'))
if ND == OB: print('NOTHING TO DO: the new develop IS the kit base'); raise SystemExit(0)
tok = gh_token()
if not tok: print('REFUSING: GH_TOKEN unset'); raise SystemExit(3)
c = gh_get('compare/%s...%s' % (OB, ND), tok); cm = gh_get('commits/%s' % ND, tok)
ok1 = c.get('status') == 'ahead' and c.get('behind_by') == 0
print('%s R1 descends: status %s ahead %s behind %s | commits %s' % ('PASS' if ok1 else 'FAIL', c.get('status'), c.get('ahead_by'), c.get('behind_by'),
      [(x['sha'][:12], x['commit']['message'].split('\n')[0][:80]) for x in c.get('commits', [])]))
files = {f['filename']: f for f in c.get('files', [])}
docs = set(K['docs'])
guard = (set(K['files']) - docs) | set(K['unchanged_must_equal']) | set(K['pr0_files_all'])
moved = sorted(p for p in files if p in guard or p.startswith(K['service'] + '/') or p.startswith('Blockchain/Dev/scripts/audit/'))
ok2 = not moved
print('%s R2 no non-doc kit path moved: %s | compare lists %d file(s): %s' % ('PASS' if ok2 else 'FAIL', moved or 'NONE', len(files), sorted(files)))
if not (ok1 and ok2):
    print('RE-DRAFT: the new develop is not a clean re-pin of this kit (%s) — the drafted expectations no longer hold; do NOT --write' % ('not a descendant' if not ok1 else 'non-doc kit paths moved'))
    raise SystemExit(1)
new = json.loads(json.dumps(K))
new['base'] = ND; new['base_tree'] = cm['commit']['tree']['sha']; new['base_parent'] = OB
for d in K['docs']:
    if d in files: new['base_blobs'][d] = files[d]['sha']
new['base_history'] = list(K.get('base_history') or []) + [{'base': OB, 'replaced_by': ND, 'at': now(), 'commits': [x['sha'] for x in c.get('commits', [])],
                                                           'docs_moved': sorted(set(files) & docs)}]
new['base_note'] = 'develop re-pinned %s -> %s by repin_base_gateD2.py (%s); only the platform-k docs moved' % (OB[:12], ND[:12], now())
ch = {k: (K.get(k), new[k]) for k in new if K.get(k) != new[k]}
for k, (a, b) in ch.items(): print('PROPOSED %s: %s -> %s' % (k, json.dumps(a)[:160], json.dumps(b)[:160]))
print('UNCHANGED by the re-pin (their files are blob-equal at the new develop): locks, baseline, cells / suite claims, unchanged_must_equal, pr0_* | NOTE: base_parent now names the OLD base; c1 P4b/P7 controls use pr0_parent/pr0_commit, which stay PR 0')
if '--write' in A:
    bk = os.path.join(G, 'kit.json.pre-repin-%s' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    shutil.copyfile(os.path.join(G, 'kit.json'), bk)
    json.dump(new, open(os.path.join(G, 'kit.json'), 'w'), indent=2, ensure_ascii=False); open(os.path.join(G, 'kit.json'), 'a').write('\n')
    print('WRITTEN kit.json (%d field(s)); backup %s' % (len(ch), bk))
else:
    print('REPORT ONLY: re-run with --write to apply (Wednesday\'s act)')
raise SystemExit(0)
