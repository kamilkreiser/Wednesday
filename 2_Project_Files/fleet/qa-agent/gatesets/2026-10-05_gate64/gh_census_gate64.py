#!/usr/bin/env python3
"""gh_census_gate64.py — COLLISION-CENSUS for #1389 (KS-1330): read-only GitHub GETs of every OTHER open PR and its files (GH_TOKEN by name).
  OVERLAP #n     touches the runner or its test (the 2 kit paths), or carries KS-1330 in its title: the launch action refuses (rc 15)
  EXPECTED #1250 #1250 (KS-1302 round 2, NO GO at cap, OPEN, ships nothing) touches both kit paths BY DESIGN — #1389 re-lands its
                 round-2 blobs. Expected ONLY at the kit's pinned head 2b8dcb824dd2; a MOVED #1250 is an OVERLAP (Q-1250)
  NEAR #n        touches `.githooks/pre-push` or `scripts/preflight/preflight.sh` (the hook that runs this runner as leg 14): REPORTED
  SUITES #n      adds or changes a `*.test.sh` directly under a runner ROOT: the runner globs it, so if it lands first the merge-in
                 tree's coupling census (c3_census_gate64.py) differs from the head's: REPORTED
  DOCS #n        touches either platform-k doc: EXPECTED (a later landing moves develop; #1389 then needs a merge-in by Seat G 2nd,
                 judged by c4_docs_gate64.py predict / qm on the real develop)
  CONTROLS       the classifier run on #1389 ITSELF must print OVERLAP, and #1250 must be seen and classed EXPECTED (or OVERLAP if
                 moved) — either missing means every zero below is blind
--selftest  the classifier on planted rows.   --json <file> saves the raw census.
rc 0 read OK and no OVERLAP / rc 15 an OVERLAP / rc 3 API failure or a BLIND control / rc 1 selftest broken."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate64 import K, gh_get, gh_pages

CODE = set(K['files']); DOCS = {K['flow'], K['cheat']}; HOOKS = set(K['hook_blobs'])
P1250 = K['pr1250']


def is_root_suite(p):
    for r in K['roots']:
        if p.startswith(r + '/') and '/' not in p[len(r) + 1:] and p.endswith('.test.sh'):
            return True
    return False


def classify(n, title, fs, head=None):
    c = sorted(set(fs) & CODE); tk = 'KS-1330' in title or 'KS 1330' in title
    if n == P1250['pr'] and not tk:
        if head == P1250['head']: return ['EXPECTED #%s | %s | kit paths %d (by design: #1389 re-lands its round-2 blobs) | head %s == kit' % (n, title[:60], len(c), head[:12])]
        return ['OVERLAP #%s | #1250 MOVED: head %s != kit %s (Q-1250: its branch must not move)' % (n, str(head)[:12], P1250['head'][:12])]
    if c or tk: return ['OVERLAP #%s | %s | kit paths %s | title KS-1330 %s' % (n, title[:70], c, tk)]
    out = []
    h = sorted(set(fs) & HOOKS); s = sorted(p for p in fs if is_root_suite(p)); d = sorted(set(fs) & DOCS)
    if h: out.append('NEAR #%s | %s | hook paths %s' % (n, title[:60], [os.path.basename(x) for x in h]))
    if s: out.append('SUITES #%s | %s | runner-globbed suites %s' % (n, title[:60], [os.path.basename(x) for x in s][:6]))
    if d: out.append('DOCS #%s | %s | %s' % (n, title[:60], [os.path.basename(x)[:24] for x in d]))
    return out


def selftest():
    T, R = K['test'], K['runner']
    arms = [('the runner', ('1', 'KS-9: x', [R]), 'OVERLAP'),
            ('the test', ('2', 'KS-9: x', [T, 'a.ts']), 'OVERLAP'),
            ('title KS-1330 only', ('3', 'KS-1330: follow-up', ['README.md']), 'OVERLAP'),
            ('#1250 at the kit head', (P1250['pr'], 'KS-1302: round 2', [R, T], P1250['head']), 'EXPECTED'),
            ('#1250 MOVED', (P1250['pr'], 'KS-1302: round 2', [R, T], 'e' * 40), 'OVERLAP'),
            ('pre-push only', ('4', 'KS-1127: leg 14 quoting', ['.githooks/pre-push']), 'NEAR'),
            ('preflight.sh only', ('5', 'KS-1127: x', [K['hook_blobs'] and list(K['hook_blobs'])[1]]), 'NEAR'),
            ('a new root suite', ('6', 'KS-1: y', ['systemTest/__tests__/zz_new.test.sh']), 'SUITES'),
            ('a NESTED suite is not globbed', ('7', 'KS-1: y', ['systemTest/__tests__/sub/zz.test.sh']), None),
            ('docs only', ('8', 'KS-1384: y', [K['flow'], K['cheat'], 'a.ts']), 'DOCS'),
            ('docs + the runner', ('9', 'KS-1: z', [K['cheat'], R]), 'OVERLAP'),
            ('disjoint', ('10', 'KS-2: z', ['README.md']), None)]
    ok = 0
    for name, args, want in arms:
        got = classify(*args); g = (bool(got) and got[0].startswith(want)) if want else not got; ok += g
        print('SELFTEST %s %s: want %s | got %s' % ('OK' if g else 'MISS', name, want or 'NOTHING', got or 'NOTHING'))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); print('CHECKED %d arm(s)' % len(arms))
    return 0 if ok == len(arms) else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    if '--selftest' in A: raise SystemExit(selftest())
    try:
        me = gh_get('pulls/' + K['pr']); own = [f['filename'] for f in gh_pages('pulls/%s/files' % K['pr'])]
        print('API #%s head %s branch %s base %s state %s merged %s changed_files %s' % (K['pr'], me['head']['sha'], me['head']['ref'], me['base']['ref'],
              me['state'], me.get('merged'), me.get('changed_files')))
        ctl = classify(K['pr'], me['title'], own)
        ctl_ok = bool(ctl) and ctl[0].startswith('OVERLAP')
        print('CONTROL the classifier on #%s ITSELF: %s' % (K['pr'], 'FIRES' if ctl_ok else 'BLIND'))
        rows = []; cnt = {'OVERLAP': 0, 'EXPECTED': 0, 'NEAR': 0, 'SUITES': 0, 'DOCS': 0}; others = 0; seen1250 = None
        for x in gh_pages('pulls?state=open'):
            n = str(x['number'])
            if n == K['pr']: continue
            others += 1
            fs = [f['filename'] for f in gh_pages('pulls/%s/files' % n)]
            for c in classify(n, x['title'], fs, x['head']['sha']):
                print(c + ' | head %s' % x['head']['sha'][:12]); cnt[c.split()[0]] += 1
                if n == P1250['pr']: seen1250 = c.split()[0]
            rows.append({'number': n, 'head': x['head']['sha'], 'title': x['title'], 'files': fs})
    except Exception as e:
        print('API FAILURE %s' % e); raise SystemExit(3)
    if '--json' in A: json.dump(rows, open(A[A.index('--json') + 1], 'w'), indent=1)
    print('CONTROL #%s (must-hit for both kit paths): %s' % (P1250['pr'], seen1250 or 'NOT SEEN (closed? the runner-path classifier is unproven)'))
    print('CENSUS %d other open PR(s): %d OVERLAP, %d EXPECTED, %d NEAR, %d SUITES, %d DOCS; control #%s %s' % (
        others, cnt['OVERLAP'], cnt['EXPECTED'], cnt['NEAR'], cnt['SUITES'], cnt['DOCS'], K['pr'], 'FIRES' if ctl_ok else 'BLIND'))
    if not ctl_ok or not seen1250: raise SystemExit(3)
    raise SystemExit(15 if cnt['OVERLAP'] else 0)
