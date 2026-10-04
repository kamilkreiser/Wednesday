#!/usr/bin/env python3
"""c6_scope_gate54f.py — gate54f C6: what this PR is NOT, measured, plus the NOT COVERED statements the verdict must carry.
  S1 the changed path set (git diff --name-only base head) == exactly kit files (4 paths).
  S2 0 test paths among them by kit test_path_rx (secuura-test-discipline §4 is triggered only by a test change), with a MUST-HIT CONTROL:
     the same regex over the base tree matches >= 1 known test path (counted and two printed) and matches none of the 4 kit paths.
  S3 0 runtime paths: every changed path is a package-lock.json or the baseline; 0 package.json; CONTROL: the same classifier calls
     scripts/audit/audit-gate.mjs a non-lock path.
  S4 the instruments did not move: the leg scripts and the code they import (kit legs + lock-discovery / baseline-contract /
     could-not-check / advisory-fetch-stub, preflight.sh, .githooks/pre-push, scripts/audit package.json + lock) blob-equal base == head,
     so legs 2/6/7 at HEAD are the SAME instruments as at the base control.
  S5 out of gate scope, stated: kit out_of_scope_lock's package-lock.json blob-equal base == head, and the tree is still declared in
     OUT_OF_SCOPE_LOCKS (lock-discovery.mjs at head) with ticket KS-769 — its expires date printed (after that date it returns to leg 7's corpus).
  S6 MODES: the 4 paths are recorded 100644 at head; CONTROL Blockchain/Dev/scripts/run-migrations.sh reads 100755 (the instrument can see an exec bit).
  NC lines (printed, not checks): no runtime change; §5f NOT APPLICABLE; the mobile lock NOT COVERED (KS-769).
Usage: c6_scope_gate54f.py --repo <clone> --base <sha> --head <sha>   (rc 0 PASS / 1 FAIL / 2 usage)"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54f import K, git, commit, show, now, Checks

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--head' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); B = commit(REPO, opt('--base', K['base'])); H = commit(REPO, opt('--head'))
print('c6_scope_gate54f %s | repo %s | base %s | head %s' % (now(), REPO, B, H))
C = Checks(); RX = re.compile(K['test_path_rx'])
ch = sorted(x for x in git(REPO, 'diff', '--name-only', B, H).splitlines() if x)
C.chk('S1 path set', ch == sorted(K['files']), '%d changed path(s) %s | want exactly %s' % (len(ch), ch, sorted(K['files'])))
tree = git(REPO, 'ls-tree', '-r', '--name-only', B).splitlines(); hits = [p for p in tree if RX.search(p)]
tp = [p for p in ch if RX.search(p)]; kp = [p for p in K['files'] if RX.search(p)]
C.chk('S2 test paths (§4)', not tp and len(hits) > 0 and not kp,
      'test paths among the changed %d %s | CONTROL the regex hits %d path(s) in the base tree, e.g. %s | and 0 of the 4 kit paths: %s' % (
          len(tp), tp, len(hits), hits[:2], not kp))
islock = lambda p: p.endswith('package-lock.json') or p == K['baseline']
rt = [p for p in ch if not islock(p)]; pj = [p for p in ch if p.endswith('package.json')]
C.chk('S3 runtime paths', not rt and not pj and not islock('Blockchain/Dev/scripts/audit/audit-gate.mjs'),
      'non-lock / non-baseline paths %d %s | package.json %d | CONTROL audit-gate.mjs classified non-lock: %s' % (len(rt), rt, len(pj), not islock('Blockchain/Dev/scripts/audit/audit-gate.mjs')))
inst = sorted(set(K['legs'].values()) | {'Blockchain/Dev/scripts/audit/' + f for f in ('lock-discovery.mjs', 'baseline-contract.mjs', 'could-not-check.mjs', 'advisory-fetch-stub.mjs', 'package.json', 'package-lock.json')}
              | {'Blockchain/Dev/scripts/preflight/preflight.sh', '.githooks/pre-push'})
def blob(sha, p):
    l = git(REPO, 'ls-tree', sha, '--', p).strip(); return l.split()[2] if l else None
moved = [(p, blob(B, p), blob(H, p)) for p in inst if blob(B, p) != blob(H, p)]; absent = [p for p in inst if blob(B, p) is None]
C.chk('S4 instruments unmoved', not moved and not absent, '%d instrument file(s) blob-equal base == head | moved %s | absent at base %s' % (len(inst) - len(moved), moved or 'NONE', absent or 'NONE'))
ol = K['out_of_scope_lock'] + '/package-lock.json'; ld = show(REPO, H, 'Blockchain/Dev/scripts/audit/lock-discovery.mjs') or ''
m = re.search(r"'%s',\s*\{.*?ticket:\s*'([A-Z]+-\d+)'.*?expires:\s*'(\d{4}-\d\d-\d\d)'" % re.escape(K['out_of_scope_lock']), ld, re.S)
C.chk('S5 out-of-scope lock', blob(B, ol) == blob(H, ol) and blob(B, ol) is not None and m is not None and m.group(1) == K['out_of_scope_ticket'],
      '%s blob %s base == head %s | declared in OUT_OF_SCOPE_LOCKS at head: %s, ticket %s, expires %s' % (
          ol, (blob(B, ol) or 'ABSENT')[:12], blob(B, ol) == blob(H, ol), m is not None, m and m.group(1), m and m.group(2)))
md = {p: (git(REPO, 'ls-tree', H, '--', p).split() or ['ABSENT'])[0] for p in K['files']}; ctl = (git(REPO, 'ls-tree', H, '--', 'Blockchain/Dev/scripts/run-migrations.sh').split() or ['ABSENT'])[0]
C.chk('S6 modes', all(v == '100644' for v in md.values()) and ctl == '100755', 'recorded modes at head (git ls-tree; core.filemode is false) %s | CONTROL Blockchain/Dev/scripts/run-migrations.sh %s (want 100755)' % (
    sorted(set(md.values())), ctl))
print('NC no runtime change: the PR touches 3 package-lock.json files and 1 suppression list; no source, manifest, image, migration or config. Nothing is deployed or run against a live stack; no Akto / systemTest / service suite is in scope.')
print('NC secuura-test-discipline §4: exemption applies iff S2 reads 0 test paths; the PR body must SAY so with its reason (the skill: "say so explicitly and why").')
print('NC secuura-test-discipline §5f: NOT APPLICABLE — §5f governs a runtime-behaviour change (live sweep on a rebuilt stack); this PR has none (S3). NOT COVERED: any runtime effect of http-cache-semantics 4.3.0 inside anchoring / nft-certificate (no service suite, no container run).')
print('NC %s: OUT OF GATE SCOPE (%s). It still pins http-cache-semantics 4.2.0, braces and node-forge; it is excluded from leg 7 until the expires date in S5, after which it re-enters the corpus with its own advisories. NOT COVERED.' % (ol, K['out_of_scope_ticket']))
n = C.nfail()
print('SCOPE %s: %d FAIL of %d checks | base %s head %s | changed %d' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), B[:12], H[:12], len(ch)))
raise SystemExit(1 if n else 0)
