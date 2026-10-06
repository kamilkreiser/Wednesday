#!/usr/bin/env python3
"""gh_gate69.py — GitHub READ-ONLY instruments for the gate69 BATCH. REST GETs only; GH_TOKEN by name, never printed.
--pr A|B (B needs --b-pr N; kit 1396); THE HEAD IS A PARAMETER (--head).

  api       `API #<n> head <sha> branch <ref> base <ref> state <s> merged <b> mergeable <m> mergeable_state <ms>` (re-polled while null)
            + body sha256/16, chars, UTF-8 bytes, title; rc 1 unless the API head == --head, open, not merged, base develop.
  actions   [--at SHA] [--prev SHA]  runs at SHA vs runs at prev (default prev: the develop the gate read — its PUSH runs are the
            baseline: at 3f9ff4e1e1b9 `PR Security Gates (KS-168)` and `pr` FAILED on push). NEW-FAILING / PENDING / NOT RUN; a
            PLANTED-NAME CONTROL must be reported, else the NONE is blind -> rc 1. Note: the token gets 403 on check-runs / statuses;
            only actions/runs is readable.
  census    [--b-pr N | --a-only]  every OTHER open PR: OVERLAP (a code path of EITHER batch PR, or KS-1305 / KS-1256 in the title;
            with --a-only PR A's paths / key only) / DOCS / other.
            CONTROL: a fabricated db.ts row and a fabricated verification.ts row must be OVERLAP.
  prtext    T1 one `Refs <key>` line, T2 0 closing references (title + body), T3 only the PR's key hyphenated, T4 title == the kit
            subject (A) / names the key (B), <= 92 with " (#n)", T5 0 Co-Authored-By in the body; NOT COVERED names printed FOUND/ABSENT.
  --selftest  the actions predicate, the census classifier and the key / closing scanners on synthetic input (no network).
rc 0 / 1 (finding, blind control, OVERLAP, NOT RUN) / 3 API failure."""
import hashlib, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate69 import K, gh_get, gh_pages, spec

FAILING = ('failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required')
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+(#\d+|KS-\d+)', re.I)
ALL_CODE = set(K['prs']['A']['code_paths']) | set(K['prs']['B']['code_paths'])
KEYS = (K['prs']['A']['ticket'], K['prs']['B']['ticket'])
NOTCOV = {'A': [('live sweep', r'live sweep'), ('PREFLIGHT INCOMPLETE', r'PREFLIGHT INCOMPLETE|12/15'), ('KS 1422', r'KS[ -]1422'), ('Prisma 7.10 / #949', r'7\.10|#949')],
          'B': [('live sweep', r'live sweep'), ('KS 1328 / db.retry', r'KS[ -]1328|db\.retry'), ('five other readers', r'five other readers|admin\.ts'), ('PREFLIGHT INCOMPLETE', r'PREFLIGHT INCOMPLETE|12/15'), ('Redis outage cost', r'outage')]}


def runs_by_name(runs):
    out = {}
    for r in sorted(runs, key=lambda r: r.get('created_at', '')):
        out[r['name']] = (r.get('status'), r.get('conclusion'))
    return out


def compare(prev, head, expected):
    failing = lambda d, n: d.get(n, (None, None))[1] in FAILING
    new = sorted(n for n in head if failing(head, n) and not failing(prev, n))
    pending = sorted(n for n in head if head[n][0] != 'completed')
    notrun = sorted(n for n in set(expected) if n not in head)
    return new, pending, notrun


SCOPE = {'code': ALL_CODE, 'keys': KEYS}   # --a-only narrows this to PR A's code paths and key (PR B is then just another open PR)


def classify(pr_row, files):
    t = pr_row.get('title') or ''
    if any(k in t for k in SCOPE['keys']) or set(files) & SCOPE['code']: return 'OVERLAP'
    if set(files) & {K['flow'], K['cheat']}: return 'DOCS'
    return 'other'


def scan(text): return sorted(set(re.findall(r'\bKS-\d+\b', text))), CLOSING.findall(text)


def api(sp):
    pr = None
    for i in range(3):
        pr = gh_get('pulls/%s' % sp['pr'])
        if pr.get('mergeable') is not None: break
        time.sleep(5)
    b = pr.get('body') or ''
    print('API #%s head %s branch %s base %s state %s merged %s mergeable %s mergeable_state %s' % (
        sp['pr'], pr['head']['sha'], pr['head']['ref'], pr['base']['ref'], pr['state'], pr['merged'], pr.get('mergeable'), pr.get('mergeable_state')))
    print('BODY sha256/16 %s chars %d utf8-bytes %d (READY claim: %s) | title %r (%d chars) | commits %s +%s/-%s files %s | updated %s' % (
        hashlib.sha256(b.encode()).hexdigest()[:16], len(b), len(b.encode()), sp['claims'].get('body'), pr['title'], len(pr['title']),
        pr.get('commits'), pr.get('additions'), pr.get('deletions'), pr.get('changed_files'), pr['updated_at']))
    return 0 if pr['head']['sha'] == sp['head'] and pr['state'] == 'open' and not pr['merged'] and pr['base']['ref'] == 'develop' else 1


def actions(at, prev):
    def get(sha):
        r = gh_get('actions/runs?head_sha=%s&per_page=100' % sha)
        print('READ runs at %s: total_count %d' % (sha[:12], r['total_count'])); return r['workflow_runs']
    h = runs_by_name(get(at)); p = runs_by_name(get(prev)) if prev else {}
    for n in sorted(set(h) | set(p)):
        print('RUN %-40s prev %-22s at %s' % (n, '/'.join(map(str, p.get(n, ('ABSENT', '-')))), '/'.join(map(str, h.get(n, ('ABSENT', '-'))))))
    new, pending, notrun = compare(p, h, [])
    hp = dict(h); hp['__planted_failing__'] = ('completed', 'failure')
    pn, _, pnr = compare(p, hp, ['__planted_expected__'])
    ctl = '__planted_failing__' in pn and '__planted_expected__' in pnr
    print('NEW-FAILING (vs prev %s) %s | PENDING %s | PLANTED-NAME CONTROL reported: %s' % (str(prev)[:12], new or 'NONE', pending or 'NONE', ctl))
    print('NOTE prev = develop PUSH runs; the PR runs are pull_request events — a workflow failing at BOTH is pre-existing on develop, never a pass; read its log (X6) before ruling.')
    return 0 if ctl and not new and not pending else 1


def census(exclude):
    prs = gh_pages('pulls?state=open'); rows, cnt = [], {}
    for pr in prs:
        if str(pr['number']) in exclude: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % pr['number'])]
        c = classify(pr, files); cnt[c] = cnt.get(c, 0) + 1
        if c != 'other': rows.append('  %s #%d %s %s' % (c, pr['number'], pr['head']['sha'][:12], pr['title'][:70]))
    ctl = classify({'title': 'x'}, [K['prs']['A']['product_file']]) == 'OVERLAP' and (classify({'title': 'x'}, [K['prs']['B']['product_file']]) == 'OVERLAP' or SCOPE['code'] != ALL_CODE) and classify({'title': 'y'}, [K['flow']]) == 'DOCS'
    print('CENSUS %d other open PR(s) (excluding %s): %s | CONTROL fires %s' % (sum(cnt.values()), sorted(exclude), cnt, ctl))
    for r in rows: print(r)
    return 3 if not ctl else (1 if cnt.get('OVERLAP') else 0)


def prtext(sp):
    pr = gh_get('pulls/%s' % sp['pr']); body = pr.get('body') or ''; title = pr['title']; key = sp['ticket']
    keys, closing = scan(body + '\n' + title)
    refs = re.findall(r'(?m)^\s*`?Refs %s\b' % re.escape(key), body)
    co = len(re.findall(r'(?im)^co-authored-by:', body))
    want_t = sp.get('subject') or sp.get('subjects', {}).get(sp['head'])
    lt = len(title) + len(' (#%s)' % sp['pr'])
    print('T1 `Refs %s` lines in the body: %d (want 1)' % (key, len(refs)))
    print('T2 closing references (title + body): %s (want none)' % (closing or 'none'))
    print('T3 hyphenated keys (title + body): %s -> only %s: %s' % (keys, key, keys == [key]))
    print('T4 title %r (%d chars, + " (#%s)" = %d, <= 92 %s) | == kit subject %s' % (title, len(title), sp['pr'], lt, lt <= 92, title == want_t if want_t else 'n/a (kit pins none)'))
    print('T5 Co-Authored-By in the body: %d' % co)
    for nm, rx in NOTCOV[sp['key']]:
        print('NAME %-22s %s' % (nm, 'FOUND x%d' % len(re.findall(rx, body, re.I)) if re.search(rx, body, re.I) else 'ABSENT'))
    return 0 if len(refs) == 1 and not closing and keys == [key] and lt <= 92 and key in title and co == 0 else 1


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    new, pend, nr = compare({'pr': ('completed', 'failure'), 'S': ('completed', 'success')}, {'pr': ('completed', 'failure'), 'S': ('completed', 'failure')}, [])
    rep(new == ['S'], 'actions: success->failure is NEW-FAILING, failure->failure (pre-existing) is not')
    rep(compare({}, {'pr': ('in_progress', None)}, [])[1] == ['pr'], 'actions: in_progress is PENDING')
    rep(compare({}, {}, ['x'])[2] == ['x'], 'actions: an expected workflow absent is NOT RUN')
    rep(classify({'title': 'KS-1305 x'}, []) == 'OVERLAP' and classify({'title': 'x'}, [K['prs']['B']['ks1195_file']]) == 'OVERLAP' and classify({'title': 'x'}, [K['cheat']]) == 'DOCS'
        and classify({'title': 'x'}, ['a.ts']) == 'other', 'census classifier OVERLAP / DOCS / other')
    k, c = scan('Refs KS-1256. See KS 1231 and KS 1233.'); rep(k == ['KS-1256'] and not c, 'scan: de-hyphenated keys are not keys; no closing word')
    k, c = scan('Fixes KS-1233. Refs KS-1256.'); rep(k == ['KS-1233', 'KS-1256'] and c, 'PLANTED: `Fixes KS-1233` is a closing reference AND a second hyphenated key')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if not A: print(__doc__); return 2
    try:
        if A[0] == '--selftest': return selftest()
        which = opt('--pr', 'A'); sp = spec(which, opt('--head'), opt('--b-pr') if which == 'B' else None)
        if A[0] in ('api', 'prtext') and not sp.get('pr'): print('NOT RUN: PR %s number not supplied' % which); return 1
        if A[0] == 'api': return api(sp)
        if A[0] == 'actions': return actions(opt('--at', sp['head']), opt('--prev', K['develop_at_draft']))
        if A[0] == 'census':
            if '--a-only' in A:
                SCOPE['code'] = set(K['prs']['A']['code_paths']); SCOPE['keys'] = (K['prs']['A']['ticket'],)
                return census({K['prs']['A']['pr']})
            return census({K['prs']['A']['pr'], str(opt('--b-pr') or K['prs']['B']['pr'] or '')})
        if A[0] == 'prtext': return prtext(sp)
    except (OSError, ValueError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
