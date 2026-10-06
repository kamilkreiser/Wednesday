#!/usr/bin/env python3
"""gh_gate70.py — GitHub / Linear READ-ONLY instruments for gate70 (#1397, KS-1425). REST GETs + one Linear GraphQL read; tokens BY NAME.
THE HEAD IS A PARAMETER (--head). Adapted from gh_gate69.py (the actions approach is gate69's, unchanged in substance).

  api       `API #1397 head <sha> branch <ref> base <ref> state <s> merged <b> mergeable <m> mergeable_state <ms>` (re-polled while null),
            body sha256/16, chars, UTF-8 bytes; rc 1 unless the API head == --head, open, not merged, base develop.
  actions   [--at SHA] [--prev SHA]  runs at SHA vs runs at prev (default: the develop the gate read — its PUSH runs are the baseline).
            NEW-FAILING / PENDING; a PLANTED-NAME CONTROL must be reported, else the NONE is blind -> rc 1. A workflow failing at BOTH
            is pre-existing, never a pass: read its job log (X6). The author MEASURED `Security Scanning` (fail 7, `Cannot find package
            'semver'` in the CI job) and `PR Security Gates (KS-168)` failing on develop's own head 4eaf and on #1394 / #1395 / #1396.
  census    every OTHER open PR touching any of the 37 paths or titled KS-1425 = OVERLAP; CONTROL: a fabricated row on the baseline and
            one on a lock must classify OVERLAP.
  prtext    [--measured c2.json] [--repo CLONE --head H]
            T1 exactly one `Refs KS-1425` line; T1b no closing-family word on it or on the 3 lines above it
            T2 0 closing-family words immediately before a key / #n (title + body)    T3 only KS-1425 hyphenated (title + body)
            T4 title == the commit subject; squash length <= 92        T5 0 Co-Authored-By / trailer lines in the body
            T6 CLAIMS vs MEASURED: every number the body states for the change set is compared with c2's measurement (field writes,
               entries, locks, per-package counts, rows 22 -> 24, +14/-0, 37 paths +172/-158, 78 entries / 45 locks, indent census,
               the root-lock resolved census, 59 cases); a claim the body does not make prints ABSENT (INFO).
  linear    KS-1425: state must be In Progress or Backlog (never Done / Canceled / archived on this PR's verdict).
  --selftest  the actions predicate, the classifier, the key / closing scanners and the claims comparator on synthetic input (no network).
rc 0 / 1 (finding, blind control, OVERLAP, NOT RUN) / 3 API failure."""
import hashlib, json, os, re, subprocess, sys, time, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate70 import K, gh_get, gh_pages, linear_issue

P = K['pr']; KEY = P['ticket']
FAILING = ('failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required')
CLOSING = re.compile(K['closing_rx'], re.I)
CLOSING_WORD = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\b', re.I)
PATHS = set(P['numstat'])


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


def classify(pr_row, files):
    if KEY in (pr_row.get('title') or '') or set(files) & PATHS: return 'OVERLAP'
    if any(f.endswith('package-lock.json') for f in files): return 'LOCKS'
    return 'other'


def scan(text): return sorted(set(re.findall(r'\bKS-\d+\b', text))), CLOSING.findall(text)


def refs_window(body):
    lines = body.split('\n'); hits = [i for i, l in enumerate(lines) if re.match(r'^\s*`?Refs %s\b' % re.escape(KEY), l)]
    bad = [i for i in hits for j in range(max(0, i - 3), i + 1) if CLOSING_WORD.search(lines[j])]
    return hits, bad


def claims(body, m):
    """[(id, stated, measured, ok)] — stated None = the body does not make that claim."""
    out = []
    def one(cid, rx, want, conv=lambda g: tuple(int(x.replace(',', '')) for x in g), alts=()):
        hits = [conv(x.groups()) for x in re.finditer(rx, body)]
        out.append((cid, hits or None, want if not alts else (want,) + tuple(alts), (not hits) or all(h == want or h in alts for h in hits)))
    one('CL-SET', r'\*\*(\d+) lockfiles, (\d+) entries, (\d+) field writes, \+(\d+)/-(\d+)', (m['locks'], m['entries'], m['field_writes'], m['field_writes'], m['field_writes']))
    one('CL-WRITES', r'\b(\d+) field writes\b', (m['field_writes'],))
    for n, rx in (('proxy-addr', r'proxy-addr (\d+) entries / (\d+) locks'), ('source-map-js', r'source-map-js (\d+) entries / (\d+) locks'), ('smol-toml', r'smol-toml (\d+) entries / (\d+) locks')):
        one('CL-%s' % n, rx, (m['per_package'].get(n), m['per_package'].get(n)))
    one('CL-ROWS', r'(\d+) rows to (\d+)', (K['baseline']['rows_before'], K['baseline']['rows_after']))
    one('CL-BASELINE-NUMSTAT', r'audit-baseline\.json` at \+(\d+)/-(\d+)', tuple(K['baseline']['numstat']))
    one('CL-PATHS', r'(\d+) paths, \+(\d+)/-(\d+)', (m.get('paths', P['file_count']), m.get('adds', P['adds_dels'][0]), m.get('dels', P['adds_dels'][1])))
    one('CL-CENSUS78', r'all (\d+) tracked lockfiles.*?found \*\*(\d+) entries\*\*', (m['tracked_locks'], m['five_any_version_entries']))
    dev2 = sum(1 for l, n in m['indent_by_lock'].items() if l.startswith('Blockchain/Dev/') and n == 2)
    st4 = sum(1 for l, n in m['indent_by_lock'].items() if l.startswith('systemTest/') and n == 4)
    one('CL-INDENT', r'The \*\*(\d+)\*\* locks under `Blockchain/Dev` are \*\*indent 2\*\*; the \*\*(\d+)\*\* under `systemTest` are \*\*indent 4\*\*', (dev2, st4))
    rr = m['root_resolved_census']
    one('CL-ROOTRES', r'\*\*([\d,]+)\*\* of its non-link entries have no `resolved` against \*\*([\d,]+)\*\*', (rr['without_resolved'], rr['with_resolved']),
        alts=((rr['without_resolved'] + 1, rr['with_resolved']),))   # +1 = the root "" entry counted as an entry (a definition, not an error)
    one('CL-CASES', r'(\d+) cases pass, 0 fail', (K['expected_case_count'],))
    return out


def api(head):
    pr = None
    for i in range(3):
        pr = gh_get('pulls/%s' % P['pr'])
        if pr.get('mergeable') is not None: break
        time.sleep(5)
    b = pr.get('body') or ''
    print('API #%s head %s branch %s base %s state %s merged %s mergeable %s mergeable_state %s' % (
        P['pr'], pr['head']['sha'], pr['head']['ref'], pr['base']['ref'], pr['state'], pr['merged'], pr.get('mergeable'), pr.get('mergeable_state')))
    print('BODY sha256/16 %s chars %d utf8-bytes %d (READY claim: "9,936 chars") | title %r (%d chars) | commits %s +%s/-%s files %s | updated %s' % (
        hashlib.sha256(b.encode()).hexdigest()[:16], len(b), len(b.encode()), pr['title'], len(pr['title']),
        pr.get('commits'), pr.get('additions'), pr.get('deletions'), pr.get('changed_files'), pr['updated_at']))
    return 0 if pr['head']['sha'] == head and pr['state'] == 'open' and not pr['merged'] and pr['base']['ref'] == 'develop' else 1


def actions(at, prev):
    def get(sha):
        r = gh_get('actions/runs?head_sha=%s&per_page=100' % sha)
        print('READ runs at %s: total_count %d' % (sha[:12], r['total_count'])); return r['workflow_runs']
    h = runs_by_name(get(at)); p = runs_by_name(get(prev)) if prev else {}
    for n in sorted(set(h) | set(p)):
        print('RUN %-40s prev %-22s at %s' % (n, '/'.join(map(str, p.get(n, ('ABSENT', '-')))), '/'.join(map(str, h.get(n, ('ABSENT', '-'))))))
    new, pending, _ = compare(p, h, [])
    hp = dict(h); hp['__planted_failing__'] = ('completed', 'failure')
    pn, _, pnr = compare(p, hp, ['__planted_expected__'])
    ctl = '__planted_failing__' in pn and '__planted_expected__' in pnr
    print('NEW-FAILING (vs prev %s) %s | PENDING %s | PLANTED-NAME CONTROL reported: %s' % (str(prev)[:12], new or 'NONE', pending or 'NONE', ctl))
    print('NOTE prev = develop PUSH runs; the PR runs are pull_request events — a workflow failing at BOTH is pre-existing on develop, never a pass; '
          'a workflow ABSENT at prev and failing at the head is NEW-FAILING here: read its log (X6) and classify it, with the log line as the instrument.')
    return 0 if ctl and not new and not pending else 1


def census():
    prs = gh_pages('pulls?state=open'); rows, cnt = [], {}
    for pr in prs:
        if str(pr['number']) == P['pr']: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % pr['number'])]
        c = classify(pr, files); cnt[c] = cnt.get(c, 0) + 1
        if c != 'other': rows.append('  %s #%d %s %s' % (c, pr['number'], pr['head']['sha'][:12], pr['title'][:70]))
    ctl = classify({'title': 'x'}, [K['baseline_path']]) == 'OVERLAP' and classify({'title': 'x'}, [sorted(p for p in PATHS if p.endswith('package-lock.json'))[0]]) == 'OVERLAP' and classify({'title': 'y'}, ['a.ts']) == 'other'
    print('CENSUS %d other open PR(s): %s | CONTROL fires %s' % (sum(cnt.values()), cnt, ctl))
    for r in rows: print(r)
    return 3 if not ctl else (1 if cnt.get('OVERLAP') else 0)


def prtext(measured, repo, head):
    pr = gh_get('pulls/%s' % P['pr']); body = pr.get('body') or ''; title = pr['title']
    keys, closing = scan(body + '\n' + title)
    hits, bad = refs_window(body)
    co = len(re.findall(r'(?im)^\s*(co-authored-by|signed-off-by):', body))
    lt = len(title) + len(' (#%s)' % P['pr'])
    print('BODY sha256/16 %s, %d chars, %d utf8-bytes' % (hashlib.sha256(body.encode()).hexdigest()[:16], len(body), len(body.encode())))
    print('T1 `Refs %s` lines: %d at line(s) %s (want exactly 1) | T1b closing words on it or the 3 lines above: %s' % (KEY, len(hits), [i + 1 for i in hits], bad or 'none'))
    print('T2 closing references before a key / #n (title + body): %s (want none)' % (closing or 'none'))
    print('T3 hyphenated keys (title + body): %s -> only %s: %s | de-hyphenated mentions %d' % (keys, KEY, keys == [KEY], len(re.findall(r'\bKS \d+\b', body + title))))
    print('T4 title %r (%d chars, squash %d <= %d %s) == kit subject %s' % (title, len(title), lt, P['squash_max'], lt <= P['squash_max'], title == P['subject']))
    print('T5 trailer-shaped lines in the body: %d' % co)
    ok = len(hits) == 1 and not bad and not closing and keys == [KEY] and lt <= P['squash_max'] and title == P['subject'] and co == 0
    if measured:
        m = json.load(open(measured))
        if repo:
            ns = [l.split('\t') for l in subprocess.run(['git', '-C', repo, 'diff', '--numstat', P['parents'][0], head], capture_output=True, text=True).stdout.strip().split('\n')]
            m['paths'], m['adds'], m['dels'] = len(ns), sum(int(x[0]) for x in ns), sum(int(x[1]) for x in ns)
        for cid, stated, want, good in claims(body, m):
            print('T6 %-22s %s stated %s measured %s' % (cid, 'OK      ' if good and stated else ('ABSENT  ' if not stated else 'MISMATCH'), stated, want))
            ok &= good
    else:
        print('T6 NOT RUN: --measured <c2 diff --json-out> not given (a claims check with no measurement is not a check)'); ok = False
    return 0 if ok else 1


def linear():
    r = linear_issue(KEY); i = (r.get('data') or {}).get('issue')
    if not i: print('LINEAR %s not returned: %s' % (KEY, r.get('errors'))); return 1
    print('LINEAR %s state %s (%s) updatedAt %s archivedAt %s' % (i['identifier'], i['state']['name'], i['state']['type'], i['updatedAt'], i['archivedAt']))
    return 0 if i['state']['name'] in K['linear_ok_states'] and not i['archivedAt'] else 1


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    new, _, _ = compare({'pr': ('completed', 'failure'), 'S': ('completed', 'success')}, {'pr': ('completed', 'failure'), 'S': ('completed', 'failure')}, [])
    rep(new == ['S'], 'actions: success->failure is NEW-FAILING, failure->failure (pre-existing) is not')
    rep(compare({}, {'X': ('completed', 'failure')}, [])[0] == ['X'], 'actions: a workflow ABSENT at prev and failing at the head is NEW-FAILING (read its log)')
    rep(compare({}, {'pr': ('in_progress', None)}, [])[1] == ['pr'], 'actions: in_progress is PENDING')
    rep(classify({'title': 'KS-1425 x'}, []) == 'OVERLAP' and classify({'title': 'x'}, [K['baseline_path']]) == 'OVERLAP' and classify({'title': 'x'}, ['q/package-lock.json']) == 'LOCKS'
        and classify({'title': 'x'}, ['a.ts']) == 'other', 'census classifier OVERLAP / LOCKS / other')
    k, c = scan('Refs KS-1425. Gate owners KS 470, KS 531.'); rep(k == ['KS-1425'] and not c, 'scan: de-hyphenated keys are not keys; no closing word')
    k, c = scan('Fixes KS-1403. Refs KS-1425.'); rep(k == ['KS-1403', 'KS-1425'] and c, 'PLANTED `Fixes KS-1403`: a closing reference AND a second key')
    rep(refs_window('a\nthis resolves it\nRefs KS-1425')[1] and not refs_window('Refs KS-1425 https://x')[1], 'PLANTED closing word within 3 lines above Refs FIRES; clean line 1 passes')
    m = {'locks': 36, 'entries': 54, 'field_writes': 158, 'per_package': {'proxy-addr': 16, 'source-map-js': 33, 'smol-toml': 4}, 'tracked_locks': 45, 'five_any_version_entries': 78,
         'indent_by_lock': dict([('Blockchain/Dev/a%d/package-lock.json' % i, 2) for i in range(40)] + [('systemTest/s%d/package-lock.json' % i, 4) for i in range(4)]),
         'root_resolved_census': {'without_resolved': 1609, 'with_resolved': 328}, 'paths': 37, 'adds': 172, 'dels': 158}
    good = '**36 lockfiles, 54 entries, 158 field writes, +158/-158, x\n158 field writes, not 162'
    rep(all(x[3] for x in claims(good, m)), 'claims: a true body passes (162 in "not 162" is not a stated write count)')
    rep(not all(x[3] for x in claims('**36 lockfiles, 54 entries, 162 field writes, +162/-162', m)), 'PLANTED 162 field writes FAILS')
    rep(not all(x[3] for x in claims('The **41** locks under `Blockchain/Dev` are **indent 2**; the **4** under `systemTest` are **indent 4**', m)), 'PLANTED indent census 41 vs measured 40 FAILS')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if not A: print(__doc__); return 2
    try:
        if A[0] == '--selftest': return selftest()
        head = opt('--head', P['head_expected'])
        if A[0] == 'api': return api(head)
        if A[0] == 'actions': return actions(opt('--at', head), opt('--prev', K['develop_at_draft']))
        if A[0] == 'census': return census()
        if A[0] == 'prtext': return prtext(opt('--measured'), opt('--repo'), head)
        if A[0] == 'linear': return linear()
    except (OSError, ValueError, urllib.error.URLError, KeyError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
