#!/usr/bin/env python3
"""c6_scope_gate58.py — gate58 C6: what this PR is NOT, measured; the key scan; and the NOT COVERED statements the PR body must carry.
  S1 the changed path set (git diff --name-only base head) == exactly kit files (7 paths), equality BOTH ways.
  S2 0 test paths among them by kit test_path_rx, with a MUST-HIT CONTROL: the same regex over the base tree matches >= 1 path and
     none of the 7 kit paths (secuura-test-discipline §4 is triggered only by a test change).
  S3 0 runtime paths: every changed path is a package-lock.json or the baseline; 0 package.json; CONTROL: the same classifier calls
     scripts/audit/audit-gate.mjs a non-lock path.
  S4 the instruments did not move: the leg scripts and what they import / read (audit-gate, audit-locks, lock-discovery,
     baseline-contract, could-not-check, advisory-fetch-stub, the three leg-5 test files, expected-case-count, scripts/audit
     package.json + lock, lockfile-cleanroom.sh, preflight.sh, .githooks/pre-push) blob-equal base == head.
  S5 OUT OF SCOPE, measured: kit out_of_scope_lock's package-lock.json blob-equal base == head (== kit mobile_lock_blob) and still in
     OUT_OF_SCOPE_LOCKS at head with ticket KS-769 and expires 2027-01-01; it still pins browserslist 4.28.1 (printed).
  S6 MODES: the 7 paths 100644 at head; CONTROL Blockchain/Dev/scripts/run-migrations.sh reads 100755.
  K1-K4 KEYS on title / body / commit message / branch: the hyphenated KS keys == exactly [KS-749] (branch: `ks-749` and no other key);
     NO kit forbidden_hyphenated key (KS-751, archived) anywhere, case-insensitive, hyphen or underscore; no closing keyword
     (close/fix/resolve + a key or #n); the body carries `Refs KS-749` on its own line.
  K5 CONTROL: the same forbidden-key scanner FIRES on the base audit-baseline.json (its two browserslist rows carry `ticket: KS-751`) and
     on a planted string, so its zero on the PR surfaces is a measurement.
  N1 NOT COVERED in the PR body, each AFTER the body's first `not covered` / `not run` heading: `mobile/secuura-app` and the frontend
     `CSS build diff`.
--selftest: the same checks over plants (nothing written; the real title/body/commit are read once): T0 base-vs-base -> S1 FAIL;
  T1 the real surfaces -> PASS; T2 body + `KS-751` -> K2 FAIL; T3 title + `ks_751` -> K1 FAIL; T4 body without mobile/secuura-app -> N1;
  T5 body without the CSS line -> N1; T6 body + `Closes KS-749` -> K2; T7 body without the Refs line -> K2; T8 commit + `KS-751` -> K3.
Usage: c6_scope_gate58.py --repo <clone> --pr <n> --head <sha> [--base <sha>] [--selftest]   (rc 0 PASS / 1 FAIL / 2 usage / 3 API)"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate58 import K, git, commit, show, blob, now, Checks, gh_token, gh_get, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or not all(x in A for x in ('--repo', '--pr', '--head')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
REPO = opt('--repo'); PR = opt('--pr'); B = commit(REPO, opt('--base', K['base'])); H = commit(REPO, opt('--head'))
OWN = K['ticket']; FORB = K['forbidden_hyphenated']
RX = re.compile(K['test_path_rx'])
forb_rx = re.compile(r'(?i)\b(%s)\b' % '|'.join(re.escape(f).replace('\\-', '[-_]') for f in FORB))
CLOSE = re.compile(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[:\s]+(KS-\d+|#\d+)')


def scope(C, b, h):
    ch = sorted(x for x in git(REPO, 'diff', '--name-only', b, h).splitlines() if x)
    C.chk('S1 path set', ch == sorted(K['files']), '%d changed path(s) | MISSING %s | EXTRA %s' % (len(ch), sorted(set(K['files']) - set(ch)) or 'NONE', sorted(set(ch) - set(K['files'])) or 'NONE'))
    tree = git(REPO, 'ls-tree', '-r', '--name-only', b).splitlines(); hits = [p for p in tree if RX.search(p)]
    tp = [p for p in ch if RX.search(p)]; kp = [p for p in K['files'] if RX.search(p)]
    C.chk('S2 test paths (§4)', not tp and len(hits) > 0 and not kp, 'test paths among the changed %d %s | CONTROL the regex hits %d base-tree path(s), e.g. %s | 0 of the 7 kit paths: %s' % (len(tp), tp, len(hits), hits[:2], not kp))
    islock = lambda p: p.endswith('package-lock.json') or p == K['baseline']
    rt = [p for p in ch if not islock(p)]; pj = [p for p in ch if p.endswith('package.json')]
    C.chk('S3 runtime paths', not rt and not pj and not islock('Blockchain/Dev/scripts/audit/audit-gate.mjs'),
          'non-lock / non-baseline paths %d %s | package.json %d | CONTROL audit-gate.mjs classified non-lock: %s' % (len(rt), rt, len(pj), not islock('Blockchain/Dev/scripts/audit/audit-gate.mjs')))
    A_ = 'Blockchain/Dev/scripts/audit/'
    inst = sorted({A_ + f for f in ('audit-gate.mjs', 'audit-locks.mjs', 'lock-discovery.mjs', 'baseline-contract.mjs', 'could-not-check.mjs', 'advisory-fetch-stub.mjs',
                                     'baseline-contract.test.mjs', 'lock-discovery.test.mjs', 'gate-exit-codes.test.mjs', 'expected-case-count', 'package.json', 'package-lock.json')}
                  | {'Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh', 'Blockchain/Dev/scripts/preflight/preflight.sh', '.githooks/pre-push'})
    moved = [(p, blob(REPO, b, p), blob(REPO, h, p)) for p in inst if blob(REPO, b, p) != blob(REPO, h, p)]; absent = [p for p in inst if blob(REPO, b, p) is None]
    C.chk('S4 instruments unmoved', not moved and not absent, '%d of %d instrument files blob-equal base == head | moved %s | absent at base %s' % (len(inst) - len(moved), len(inst), moved or 'NONE', absent or 'NONE'))
    ol = K['out_of_scope_lock'] + '/package-lock.json'; ld = show(REPO, h, A_ + 'lock-discovery.mjs') or ''
    m = re.search(r"'%s',\s*\{.*?ticket:\s*'([A-Z]+-\d+)'.*?expires:\s*'(\d{4}-\d\d-\d\d)'" % re.escape(K['out_of_scope_lock']), ld, re.S)
    mv = (json.loads(show(REPO, h, ol) or '{}').get('packages', {}).get('node_modules/browserslist') or {})
    C.chk('S5 out-of-scope mobile lock', blob(REPO, b, ol) == blob(REPO, h, ol) == K['mobile_lock_blob'] and m is not None and m.group(1) == K['out_of_scope_ticket'] and m.group(2) == K['out_of_scope_expires'],
          '%s blob base %s == head %s == kit %s | in OUT_OF_SCOPE_LOCKS at head %s, ticket %s, expires %s | it still pins browserslist %s (dev %s)' % (
              ol, (blob(REPO, b, ol) or 'ABSENT')[:12], (blob(REPO, h, ol) or 'ABSENT')[:12], K['mobile_lock_blob'][:12], m is not None, m and m.group(1), m and m.group(2), mv.get('version'), mv.get('dev', 'ABSENT -> PROD')))
    md = {p: (git(REPO, 'ls-tree', h, '--', p).split() or ['ABSENT'])[0] for p in K['files']}; ctl = (git(REPO, 'ls-tree', h, '--', 'Blockchain/Dev/scripts/run-migrations.sh').split() or ['ABSENT'])[0]
    C.chk('S6 modes', all(v == '100644' for v in md.values()) and ctl == '100755', 'recorded modes at head %s | CONTROL run-migrations.sh %s (want 100755)' % (sorted(set(md.values())), ctl))
    return ch


def keys(C, title, body, msg, br):
    for tag, s, t in (('K1', 'title', title), ('K2', 'body', body), ('K3', 'commit', msg)):
        ks = sorted(set(re.findall(r'\bKS-\d+\b', t))); fb = sorted(set(m.group(0) for m in forb_rx.finditer(t))); cl = [m.group(0) for m in CLOSE.finditer(t)]
        refs = re.search(r'(?m)^Refs %s\s*$' % re.escape(OWN), t) is not None
        ok = ks == [OWN] and not fb and not cl and (refs if s == 'body' else True)
        C.chk('%s keys %s' % (tag, s), ok, 'hyphenated keys %s (want exactly [%s]) | forbidden %s %s | closing keyword %s%s' % (
            ks, OWN, FORB, fb or 'NONE', cl or 'NONE', (' | `Refs %s` on its own line: %s' % (OWN, refs)) if s == 'body' else ''))
    fb = sorted(set(m.group(0) for m in forb_rx.finditer(br))); other = sorted(set(re.findall(r'(?i)\bks-\d+\b', br)) - {OWN.lower()})
    C.chk('K4 keys branch', OWN.lower() in br.lower() and not fb and not other, 'branch %s carries %s: %s | forbidden %s | other keys %s' % (br, OWN.lower(), OWN.lower() in br.lower(), fb or 'NONE', other or 'NONE'))
    dehy = sorted(set(re.findall(r'\bKS \d+\b', body)))
    print('INFO de-hyphenated keys in the body (words, never attached): %s' % dehy)


def control(C):
    bl = show(REPO, B, K['baseline']) or ''; n1 = len(forb_rx.findall(bl)); n2 = len(forb_rx.findall('planted: see ks_751 and KS-751.'))
    C.chk('K5 CONTROL forbidden scanner fires', n1 >= 2 and n2 == 2, 'hits in the base audit-baseline.json %d (want >= 2: the two browserslist rows) | hits in a planted string %d (want 2)' % (n1, n2))


def notcov(C, body):
    hd = re.search(r'(?i)not (covered|run)', body); start = hd.start() if hd else None
    need = {'mobile/secuura-app': r'mobile/secuura-app', 'CSS build diff': r'(?i)CSS build diff'}
    pos = {k: [m.start() for m in re.finditer(v, body)] for k, v in need.items()}
    ok = start is not None and all(any(p > start for p in v) for v in pos.values())
    C.chk('N1 NOT COVERED names', ok, 'first not-covered/not-run heading at char %s | %s' % (start, ' | '.join('%s at %s' % (k, v or 'ABSENT') for k, v in pos.items())))


def run(b, h, title, body, msg, br, quiet=False):
    C = Checks(quiet=quiet); ch = scope(C, b, h); keys(C, title, body, msg, br); control(C); notcov(C, body); return C, ch


tok = gh_token()
if not tok: print('REFUSING: GH_TOKEN not found by name in the Secuura .env'); raise SystemExit(3)
p = gh_get('pulls/' + PR, tok); TITLE, BODY, BR = p.get('title') or '', p.get('body') or '', p['head']['ref']
MSG = git(REPO, 'log', '-1', '--format=%B', H)
print('c6_scope_gate58 %s | repo %s | PR #%s | base %s | head %s | API head %s' % (now(), REPO, PR, B[:12], H[:12], p['head']['sha'][:12]))
for nc in ('- (NC) no runtime change: 6 package-lock.json files + 1 suppression list; no source, manifest, image, migration or config. Nothing deployed or run against a live stack.',
           '- (NC) §4 exemption applies iff S2 reads 0 test paths; §5f NOT APPLICABLE (no runtime-behaviour change). NOT COVERED: any runtime / build-output effect of the bumped packages (the frontend CSS build diff for the caniuse-lite move is UNMEASURED unless the tester measures it).',
           '- (NC) %s: OUT OF GATE SCOPE (%s, excluded from leg 7 until %s); still pins browserslist 4.28.1 as PROD. NOT COVERED.' % (K['out_of_scope_lock'], K['out_of_scope_ticket'], K['out_of_scope_expires'])):
    print(nc)
if '--selftest' in A:
    arms = []

    def arm(name, b, h, t, bo, m, want_pass, expect):
        print('\n=== ARM %s (expected %s) ===' % (name, 'PASS' if want_pass else 'FAIL'))
        C, ch = run(b, h, t, bo, m, BR, quiet=True); got = C.nfail() == 0; ok = expect(C)
        print('ARM %s: verdict %s (expected %s) | failed %s | named as expected %s -> %s' % (name, 'PASS' if got else 'FAIL', 'PASS' if want_pass else 'FAIL', C.failed() or 'NONE', ok, 'OK' if (got == want_pass and ok) else 'MISMATCH'))
        arms.append(got == want_pass and ok)
    only = lambda pre: (lambda C: [t for t in C.failed()] == pre)
    arm('T0 base-vs-base', B, B, TITLE, BODY, MSG, False, lambda C: 'S1 path set' in C.failed())
    arm('T1 the real surfaces', B, H, TITLE, BODY, MSG, True, lambda C: True)
    arm('T2 body + KS-751', B, H, TITLE, BODY + '\nSee KS-751.\n', MSG, False, only(['K2 keys body']))
    arm('T3 title + ks_751', B, H, TITLE + ' (ks_751)', BODY, MSG, False, only(['K1 keys title']))
    arm('T4 body without mobile/secuura-app', B, H, TITLE, BODY.replace('mobile/secuura-app', 'the mobile app'), MSG, False, only(['N1 NOT COVERED names']))
    arm('T5 body without the CSS line', B, H, TITLE, re.sub(r'(?i)CSS build diff', 'build output', BODY), MSG, False, only(['N1 NOT COVERED names']))
    arm('T6 body + Closes KS-749', B, H, TITLE, BODY + '\nCloses KS-749\n', MSG, False, only(['K2 keys body']))
    arm('T7 body without the Refs line', B, H, TITLE, BODY.replace('Refs KS-749', 'Refs: see title', 1), MSG, False, only(['K2 keys body']))
    arm('T8 commit + KS-751', B, H, TITLE, BODY, MSG + '\nKS-751\n', False, only(['K3 keys commit']))
    n = arms.count(False)
    print('\nSELFTEST %s: %d of %d arms returned their expected verdict' % ('OK' if n == 0 else 'MISMATCH', len(arms) - n, len(arms)))
    raise SystemExit(1 if n else 0)
C, ch = run(B, H, TITLE, BODY, MSG, BR); n = C.nfail()
print('SCOPE %s: %d FAIL of %d checks | base %s head %s | changed %d' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), B[:12], H[:12], len(ch)))
raise SystemExit(1 if n else 0)
