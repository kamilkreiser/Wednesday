#!/usr/bin/env python3
"""gh_gate68.py — GitHub READ-ONLY instruments for gate68 (#1393 ROUND 2, KS-1278). REST GETs only; GH_TOKEN by name, never printed.
--head is a PARAMETER (env G68_HEAD; default the stand-in 97ce2f).

  api       `API #1393 head <sha> branch <ref> base <ref> state <s> merged <b> mergeable <m> mergeable_state <ms>` (re-polled while null)
            + body sha256/16, chars, UTF-8 bytes (the READY's 97ce2f-era claim: c089b13d8cb5735b, 6,584 bytes = 6,551 characters);
            rc 1 unless the API head == --head, open, not merged.
  actions   [--at SHA] [--prev SHA]  runs at SHA vs the PR's OWN previous runs (default prev: the round-1 head 4a1620588819).
            NEW-FAILING / PENDING / NOT RUN (expected-but-absent, never a pass). PLANTED-NAME CONTROL (a fabricated failing run and a
            fabricated expected name must both be reported, else the NONE is blind -> rc 1).
  census    every OTHER open PR: OVERLAP (a kit code path, or KS-1278 in the title) / DOCS (a platform doc) / other.
            CONTROL: a fabricated row carrying documentRepo.ts must be OVERLAP.
  prtext    the live title + body: T1 one `Refs KS-1278` line, T2 0 closing references (title AND body), T3 only KS-1278 hyphenated
            (others de-hyphenated: KS 1419, KS 1424), T4 title == 97ce2f's subject OR the gate65-declared squash subject, <= 92, T5 0 Co-Authored-By in
            4a16..head; plus the NOT COVERED names it must carry (tamper matrix status, KS 1419, KS 1424) printed as FOUND / ABSENT.
  --selftest  the actions predicate, the census classifier and the key / closing scanners on synthetic input (no network).
rc 0 / 1 (finding, blind control, OVERLAP, NOT RUN) / 3 API failure."""
import hashlib, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate68 import K, gh_get, gh_pages, git

FAILING = ('failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required')
HEAD = os.environ.get('G68_HEAD', K['head_expected'])
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+(#\d+|KS-\d+)', re.I)


def runs_by_name(runs):
    out = {}
    for r in sorted(runs, key=lambda r: r.get('created_at', '')):
        out[r['name']] = (r.get('status'), r.get('conclusion'))
    return out


def compare(prev, head, expected):
    failing = lambda d, n: d.get(n, (None, None))[1] in FAILING
    new = sorted(n for n in head if failing(head, n) and not failing(prev, n))
    pending = sorted(n for n in head if head[n][0] != 'completed')
    notrun = sorted(n for n in (set(expected) | set(prev)) if n not in head)
    return new, pending, notrun


def classify(pr_row, files):
    if 'KS-1278' in (pr_row.get('title') or '') or set(files) & set(K['code_paths']): return 'OVERLAP'
    if set(files) & {K['flow'], K['cheat']}: return 'DOCS'
    return 'other'


def scan(text):
    return sorted(set(re.findall(r'\bKS-\d+\b', text))), CLOSING.findall(text)


def api(head):
    pr = None
    for i in range(3):
        pr = gh_get('pulls/%s' % K['pr'])
        if pr.get('mergeable') is not None: break
        time.sleep(5)
    b = pr.get('body') or ''
    print('API #%s head %s branch %s base %s state %s merged %s mergeable %s mergeable_state %s' % (
        K['pr'], pr['head']['sha'], pr['head']['ref'], pr['base']['ref'], pr['state'], pr['merged'], pr.get('mergeable'), pr.get('mergeable_state')))
    print('BODY sha256/16 %s chars %d utf8-bytes %d (READY claim at 97ce2f: %s) | title %r (%d chars) | commits %s +%s/-%s files %s | updated %s' % (
        hashlib.sha256(b.encode()).hexdigest()[:16], len(b), len(b.encode()), K['claims']['body'], pr['title'], len(pr['title']),
        pr.get('commits'), pr.get('additions'), pr.get('deletions'), pr.get('changed_files'), pr['updated_at']))
    if pr.get('mergeable_state') == 'dirty':
        print('INFO mergeable_state dirty = a merge conflict with develop (consistent with c4 mergetree: the CHEAT conflicts; the FLOW auto-merges MIS-ORDERED). It suppresses `pull_request` workflows (see actions).')
    return 0 if pr['head']['sha'] == head and pr['state'] == 'open' and not pr['merged'] else 1


def actions(at, prev):
    def get(sha):
        for i in range(3):
            r = gh_get('actions/runs?head_sha=%s&per_page=100' % sha)
            print('READ runs at %s: total_count %d (attempt %d)' % (sha[:12], r['total_count'], i + 1))
            if r['total_count']: return r['workflow_runs']
            time.sleep(5)
        return []
    h = runs_by_name(get(at)); p = runs_by_name(get(prev)) if prev else {}
    for n in sorted(set(h) | set(p)):
        print('RUN %-38s prev %-22s at %s' % (n, '/'.join(map(str, p.get(n, ('ABSENT', '-')))), '/'.join(map(str, h.get(n, ('ABSENT', '-'))))))
    new, pending, notrun = compare(p, h, [])
    hp = dict(h); hp['__planted_failing__'] = ('completed', 'failure')
    pn, _, pnr = compare(p, hp, ['__planted_expected__'])
    ctl = '__planted_failing__' in pn and '__planted_expected__' in pnr
    print('NEW-FAILING %s | PENDING %s | NOT RUN (on prev, absent at %s) %s | PLANTED-NAME CONTROL reported: %s' % (new or 'NONE', pending or 'NONE', at[:12], notrun or 'NONE', ctl))
    return 0 if ctl and not new and not pending and not notrun else 1


def census():
    prs = gh_pages('pulls?state=open')
    rows, cnt = [], {}
    for pr in prs:
        if str(pr['number']) == K['pr']: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % pr['number'])]
        c = classify(pr, files); cnt[c] = cnt.get(c, 0) + 1
        if c != 'other': rows.append('  %s #%d %s %s' % (c, pr['number'], pr['head']['sha'][:12], pr['title'][:70]))
    ctl = classify({'title': 'x'}, [K['repo_file']]) == 'OVERLAP' and classify({'title': 'y'}, [K['flow']]) == 'DOCS'
    print('CENSUS %d other open PR(s): %s | CONTROL fires %s' % (len(prs) - 1, cnt, ctl))
    for r in rows: print(r)
    return 3 if not ctl else (1 if cnt.get('OVERLAP') else 0)


def prtext(repo, head):
    pr = gh_get('pulls/%s' % K['pr']); body = pr.get('body') or ''; title = pr['title']
    keys, closing = scan(body + '\n' + title)
    refs = re.findall(r'(?m)^\s*`?Refs KS-1278\b', body)
    s97 = git(repo, 'log', '-1', '--format=%s', K['head_standin']).rstrip('\n')
    commits = git(repo, 'rev-list', '%s..%s' % (K['round1_head'], head)).split()
    co = sum(len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', c))) for c in commits)
    print('T1 `Refs KS-1278` lines in the body: %d (want 1)' % len(refs))
    print('T2 closing references (title + body): %s (want none)' % (closing or 'none'))
    print('T3 hyphenated keys (title + body): %s -> only KS-1278: %s' % (keys, keys == ['KS-1278']))
    which = 'the round-2 commit subject (97ce2f)' if title == s97 else ('the gate65-declared squash subject (round 1 title)' if title == K['squash_subject_gate65'] else 'NEITHER')
    print('T4 PR title == %s (%d chars, <= 92 %s) — the GO must name the squash subject it signs; both are candidates (RULINGS Q6)' % (which, len(title), len(title) <= 92))
    print('T5 Co-Authored-By in 4a16..head (%d commit(s)): %d' % (len(commits), co))
    for nm, rx in (('KS 1419', r'KS[ -]1419'), ('KS 1424', r'KS[ -]1424'), ('tamper matrix', r'tamper matrix'), ('NOT COVERED', r'NOT COVERED'), ('KS-TICKET placeholder', r'KS-TICKET')):
        print('NAME %-22s %s' % (nm, 'FOUND x%d' % len(re.findall(rx, body, re.I)) if re.search(rx, body, re.I) else 'ABSENT'))
    ok = len(refs) == 1 and not closing and keys == ['KS-1278'] and title in (s97, K['squash_subject_gate65']) and len(title) <= 92 and co == 0
    return 0 if ok else 1


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    new, pend, nr = compare({'pr': ('completed', 'failure'), 'S': ('completed', 'success')}, {'pr': ('completed', 'failure'), 'S': ('completed', 'failure')}, [])
    rep(new == ['S'], 'actions: success->failure is NEW-FAILING, failure->failure is not')
    new, pend, nr = compare({'pr': ('completed', 'success')}, {}, [])
    rep(nr == ['pr'], 'actions: a workflow on prev and absent at the head is NOT RUN, never a pass')
    rep(compare({}, {'pr': ('in_progress', None)}, [])[1] == ['pr'], 'actions: in_progress is PENDING')
    rep(classify({'title': 'KS-1278 x'}, []) == 'OVERLAP' and classify({'title': 'x'}, [K['route_file']]) == 'OVERLAP' and classify({'title': 'x'}, [K['cheat']]) == 'DOCS'
        and classify({'title': 'x'}, ['a.ts']) == 'other', 'census classifier OVERLAP / DOCS / other')
    k, c = scan('Refs KS-1278. Tracked as KS 1419 and KS 1424.'); rep(k == ['KS-1278'] and not c, 'scan: de-hyphenated keys are not keys; no closing word')
    k, c = scan('Fixes KS-1419. Refs KS-1278.'); rep(k == ['KS-1278', 'KS-1419'] and c, 'PLANTED: `Fixes KS-1419` is a closing reference AND a second hyphenated key')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if not A: print(__doc__); return 2
    head = opt('--head', HEAD)
    try:
        if A[0] == '--selftest': return selftest()
        if A[0] == 'api': return api(head)
        if A[0] == 'actions': return actions(opt('--at', head), opt('--prev', K['round1_head']))
        if A[0] == 'census': return census()
        if A[0] == 'prtext': return prtext(opt('--repo', K['checkout']), head)
    except (OSError, ValueError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
