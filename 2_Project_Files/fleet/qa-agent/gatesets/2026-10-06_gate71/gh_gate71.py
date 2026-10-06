#!/usr/bin/env python3
r"""gh_gate71.py — GitHub READ-ONLY instruments for gate71, ONE ROW at a time (`--pr 1404` KS-1436 / `--pr 1398` KS-1136; WIDENED
2026-10-07). REST GETs only (X6); GH_TOKEN read BY NAME inside lib_gate71. THE HEAD IS A PARAMETER (--head). NOT RUN BY ANY DRAFTER against
the network (no drafter holds a GitHub identity): only --selftest was run.
  WIDENED: `api` / `prtext` / `actions` read the row's own figures (#1404: 1 / 4 / +177 / -1, body 56d358ebe4544bec, LANDS 74; #1398:
  1 / 4 / +349 / -0, aba1d9423478a0b6, LANDS 91). `api` PRINTS mergeable / mergeable_state (#1404 reads `dirty` by the author's
  correction: the predicted docs-only conflict) and never refuses on them. `census` excludes BOTH rows and classifies OVERLAP against
  both rows' code paths. NEW `job06 --at <sha> [--at <sha> ...]`: Q2's BY-LOG-LINE measurement — EVERY job of EVERY run at each sha
  (passing or failing), its log read (302 followed without auth, `##[group]` positive control, fabricated-needle control), and the
  count of each kit `job06_log_needles` line; a needle line that is not a shell-suite stub (`__tests__`) is a LIVE job-06 run inside a
  per-PR check and is printed as such. A sha with 0 runs is reported with the fabricated-sha control beside it.

  api       `API #1398 head <sha> branch <ref> base <ref> state <s> merged <b> mergeable <m> mergeable_state <ms>`; title; commits /
            changed_files / additions / deletions (want 1 / 4 / 349 / 0); body sha256/16 vs the author's `aba1d9423478a0b6`.
            rc 1 unless head == --head, open, not merged, base develop.
  prtext    T1 exactly one `Refs KS-1136` line, no closing-family word on it or the 3 lines above; T2 0 closing references before a key / #n
            (title + body); T3 only KS-1136 hyphenated (title + body); T4 title == the commit subject, LANDS len + 8 <= 92 (91 measured by
            c1; the READY says 90); T5 0 trailer-shaped lines; T6 every figure the body states vs --measured (c2 / c3 json), ABSENT = INFO;
            T7 does the body still carry the superseded "is unmeasured" runner sentence (the COMMIT MESSAGE does: a squash that takes the
            commit message lands a stale sentence)?
  actions   [--at SHA] [--wait]   every run at the head by FULL 40-hex head_sha (CONTROL: a fabricated 40-hex sha returns 0 runs). For every
            failing run: its failed jobs, each job LOG read (redirect followed WITHOUT the auth header), POSITIVE control `##[group]` > 0,
            fabricated-needle control 0, this PR's own path tokens counted (ks1136 / 09-aggregate-report / Projects Documents: want 0),
            the kit's known-class needle counted; then the SAME workflow's failing job read at every kit develop-side head that has it.
            KNOWN-CLASS = needle at the head AND at >= 1 develop-side head AND own tokens 0 -> named, does not block (gate69 Q5 / gate70 Q1).
            Anything else = UNCLASSIFIED -> BLOCKS. `PR Security Gates (KS-168)`'s log also goes through c3 classify (the failing SET == the
            known six; the new suite's own summary 6/0). PENDING runs -> rc 1; --wait re-polls to TWO consecutive agreeing all-terminal reads.
  census    every OTHER open PR touching the 2 code paths (OVERLAP) or a platform doc (DOCS: will need a merge-in, report its order) or titled
            KS-1136. CONTROL: fabricated rows classify OVERLAP / DOCS / other.
  --selftest  the classifier, the scanners, the claims comparator, the census classifier and the redirect request (no Authorization on the
            signed URL) on synthetic input. Planted arms must FAIL.
rc 0 / 1 (finding, blind control, PENDING, UNCLASSIFIED) / 3 API failure."""
import hashlib, json, os, re, sys, time, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate71 import K, P, gh_get, gh_pages, gh_job_log, opt
import c3_suites_gate71 as C3
import lib_gate71

KEY = P['ticket']; AC = K['actions']
SHAPE = {'1404': (1, 4, 177, 1), '1398': (1, 4, 349, 0)}[P['pr']]
FAILING = ('failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required')
CLOSING = re.compile(K['closing_rx'], re.I)
CLOSING_WORD = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\b', re.I)
CODE = [p for p in P['numstat'] if not p.startswith('Projects Documents/')]
DOCS = [K['docs']['flow'], K['docs']['cheat']]


def scan(text): return sorted(set(re.findall(r'\bKS-\d+\b', text))), CLOSING.findall(text)


def refs_window(body):
    lines = body.split('\n'); hits = [i for i, l in enumerate(lines) if re.match(r'^\s*`?Refs %s\b' % re.escape(KEY), l)]
    return hits, [i for i in hits for j in range(max(0, i - 3), i + 1) if CLOSING_WORD.search(lines[j])]


def classify_log(text, needle):
    """(class, detail) for one job log."""
    g = text.count(AC['positive_control']); fab = text.count(AC['fabricated_control'])
    own = {tok: text.count(tok) for tok in AC['own_path_tokens']}
    n = text.count(needle) if needle else 0
    if g == 0: return 'UNREAD', 'positive control %r = 0: the log was NOT read (a 302 followed with the auth header, or an error swallowed)' % AC['positive_control']
    if fab: return 'BROKEN', 'fabricated needle found %d times' % fab
    if any(own.values()): return 'OWN-PATH', 'this PR\'s own paths appear in the log %s: read it, it may be caused by this change' % own
    return ('NEEDLE', 'needle %r x%d | ##[group] %d | fabricated 0 | own tokens 0' % (needle, n, g)) if n else ('NO-NEEDLE', 'needle %r absent | ##[group] %d' % (needle, g))


def known_for(run_name, job_name):
    kc = AC['known_classes']
    if run_name in kc: return kc[run_name]['needle']
    for k, v in kc.items():
        if k.startswith('pr/') and run_name == 'pr' and k[3:].lower() in job_name.lower(): return v['needle']
    return None


def verdict(head_cls, dev_cls):
    if head_cls == 'NEEDLE' and 'NEEDLE' in dev_cls: return 'KNOWN-CLASS (named, does not block)'
    return 'UNCLASSIFIED (BLOCKS until read and ruled)'


def claims(body, m):
    if P['pr'] == '1404': return claims_1404(body, m)
    out = []
    def one(cid, rx, want):
        hits = [tuple(int(x) for x in mm.groups()) for mm in re.finditer(rx, body)]
        out.append((cid, hits or None, want, (not hits) or all(h == want for h in hits)))
    one('CL-SUITE', r'new suite alone: \*\*(\d+) passed, (\d+) failed', m.get('suite', (6, 0)))
    one('CL-REDFIRST', r'rc 1, (\d+) failed\*\*', (m.get('redfirst_failed', 3),))
    one('CL-ARM-A', r'\*\*(\d+) passed, (\d+) failed\*\*\. A \*missing\*', m.get('armA', (2, 4)))
    one('CL-ARM-B', r'\*\*(\d+) passed, (\d+) failed\*\*\. Every \*present\*', m.get('armB', (4, 2)))
    one('CL-LIST', r'goes \*\*(\d+) -> (\d+)\*\*', m.get('list', (67, 68)))
    one('CL-WHOLE', r'\*\*(\d+) passed, (\d+) failed, (\d+) skipped \(of (\d+)\)\*\*', m.get('whole', (68, 0, 0, 68)))
    one('CL-NUMSTAT', r'\+(\d+)/-(\d+)\)', (14, 0))
    return out


def claims_1404(body, m):
    out = []
    def one(cid, rx, want):
        hits = [tuple(int(x) for x in mm.groups()) for mm in re.finditer(rx, body)]
        out.append((cid, hits or None, want, (not hits) or all(h == want for h in hits)))
    one('CL-REDFIRST', r'(\d+) passed / (\d+) failed\D{0,40}->\s*\**(\d+) passed / (\d+) failed', m.get('redfirst', (1, 4, 5, 0)))
    one('CL-DEVNULL', r'2>/dev/null`? arm[^0-9]{0,40}(\d+) passed / (\d+) failed', m.get('devnull', (4, 1)))
    one('CL-LIST', r'(\d+) -> (\d+)', m.get('list', (67, 68)))
    one('CL-WHOLE', r'(\d+) passed, (\d+) failed, (\d+) skipped \(of (\d+)\)', m.get('whole', (68, 0, 0, 68)))
    return out


def job06_lines(text):
    """(needle lines, STUB lines — a shell suite under __tests__ driving a stubbed job, LIVE lines — anything else)."""
    hits = [l for l in text.split('\n') if any(nd in l for nd in AC['job06_log_needles'])]
    stub = [l for l in hits if '__tests__' in l or 'tenant_isolation_stderr_own_file' in l or 'orchestrate_jobs' in l]
    return hits, stub, [l for l in hits if l not in stub]


def job06(shas):
    """Q2 by LOG LINE: every job of every run at each sha; needle lines classified LIVE vs STUB (a shell suite under __tests__)."""
    n_fab, _ = runs_at('0' * 39 + '1'); print('CONTROL fabricated 40-hex head_sha -> %d runs (want 0)' % n_fab)
    rc = 0 if n_fab == 0 else 1; live_total = 0; read_total = 0
    for sha in shas:
        n, runs = runs_at(sha); print('SHA %s: %d run(s)' % (sha[:12], n))
        for r in sorted(runs, key=lambda r: r['name']):
            for j in gh_pages('actions/runs/%d/jobs?filter=latest' % r['id']):
                try: text = gh_job_log(j['id'])
                except (OSError, urllib.error.URLError) as e: print('  %s / %s: LOG UNREADABLE %s -> BLOCKS the measurement' % (r['name'], j['name'], e)); rc = 1; continue
                g = text.count(AC['positive_control']); fab = text.count(AC['fabricated_control'])
                if g == 0: print('  %s / %s: UNREAD (0 `##[group]`)' % (r['name'], j['name'])); rc = 1; continue
                read_total += 1
                hits, stub, live = job06_lines(text); live_total += len(live)
                print('  %-30s / %-40s ##[group] %d fab %d | job-06 needle lines %d (stub-suite %d, LIVE %d)%s' % (
                    r['name'][:30], j['name'][:40], g, fab, len(hits), len(stub), len(live), (' FIRST LIVE: %r' % live[0][:140]) if live else ''))
    print('JOB06 logs read %d | LIVE job-06 lines inside these runs: %d (%s)' % (read_total, live_total,
          'job 06 RUNS inside a per-PR check: #1398 alone would redden it' if live_total else 'no live job-06 run in any per-PR check read here'))
    return rc if read_total else 1


def api(head):
    pr = None
    for _ in range(3):
        pr = gh_get('pulls/%s' % P['pr'])
        if pr.get('mergeable') is not None: break
        time.sleep(5)
    b = pr.get('body') or ''
    print('API #%s head %s branch %s base %s state %s merged %s mergeable %s mergeable_state %s' % (
        P['pr'], pr['head']['sha'], pr['head']['ref'], pr['base']['ref'], pr['state'], pr['merged'], pr.get('mergeable'), pr.get('mergeable_state')))
    bs = hashlib.sha256(b.encode()).hexdigest()[:16]
    print('BODY sha256/16 %s (READY: %s, %s) chars %d utf8-bytes %d | title %r (%d chars) | commits %s files %s +%s/-%s | updated %s' % (
        bs, P['body_sha256_16_claimed'], 'EQUAL' if bs == P['body_sha256_16_claimed'] else 'DIFFERS', len(b), len(b.encode()), pr['title'], len(pr['title']),
        pr.get('commits'), pr.get('changed_files'), pr.get('additions'), pr.get('deletions'), pr['updated_at']))
    ok = pr['head']['sha'] == head and pr['state'] == 'open' and not pr['merged'] and pr['base']['ref'] == 'develop'
    shape = (pr.get('commits'), pr.get('changed_files'), pr.get('additions'), pr.get('deletions')) == SHAPE
    print('SHAPE commits/files/+/- == %s: %s | mergeable %s mergeable_state %s (PRINTED, never refused: a docs-only `dirty` is the predicted conflict — c4 targets / mergetree)' % (
        SHAPE, shape, pr.get('mergeable'), pr.get('mergeable_state')))
    return 0 if ok and shape else 1


def prtext(head, measured):
    pr = gh_get('pulls/%s' % P['pr']); body = pr.get('body') or ''; title = pr['title']
    keys, closing = scan(body + '\n' + title); hits, bad = refs_window(body)
    co = len(re.findall(r'(?im)^\s*(co-authored-by|signed-off-by):', body)); lands = len(title) + len(P['squash_suffix'])
    print('BODY sha256/16 %s, %d chars, %d utf8-bytes' % (hashlib.sha256(body.encode()).hexdigest()[:16], len(body), len(body.encode())))
    print('T1 `Refs %s` lines: %d at %s (want 1) | closing words on it or the 3 lines above: %s' % (KEY, len(hits), [i + 1 for i in hits], bad or 'none'))
    print('T2 closing references (title + body): %s' % (closing or 'none'))
    print('T3 hyphenated keys (title + body): %s -> only %s: %s | de-hyphenated %s' % (keys, KEY, keys == [KEY], sorted(set(re.findall(r'\bKS \d+\b', body)))))
    print('T4 title %r %d chars, LANDS %d (<= %d %s) == subject %s' % (title, len(title), lands, P['squash_max'], lands <= P['squash_max'], title == P['subject']))
    print('T5 trailer-shaped lines: %d' % co)
    stale = len(re.findall(r'(?i)green on the CI runner is unmeasured', body)) if P['pr'] == '1398' else len(re.findall(r'(?i)\bunmeasured\b', body))
    print('T7 the superseded "green on the CI runner is unmeasured" sentence in the BODY: %d (the head COMMIT MESSAGE carries it: a squash body taken from the commit message would land it)' % stale)
    ok = len(hits) == 1 and not bad and not closing and keys == [KEY] and lands <= P['squash_max'] and title == P['subject'] and co == 0
    m = json.load(open(measured)) if measured else {}
    if not measured: print('T6 measured values not given (--measured): the kit defaults are the DRAFTER\'s measurements (c2 suite_ex1)')
    for cid, stated, want, good in claims(body, m):
        print('T6 %-12s %s stated %s measured %s' % (cid, 'OK      ' if good and stated else ('ABSENT  ' if not stated else 'MISMATCH'), stated, want))
        ok &= good
    return 0 if ok else 1


def runs_at(sha):
    r = gh_get('actions/runs?head_sha=%s&per_page=100' % sha); return r['total_count'], r['workflow_runs']


def actions(head, wait):
    n_fab, _ = runs_at('0' * 39 + '1')
    print('CONTROL fabricated 40-hex head_sha -> %d runs (want 0)' % n_fab)
    prev = None; stable = 0
    while True:
        n, runs = runs_at(head)
        state = sorted((r['name'], r['status'], r.get('conclusion')) for r in runs)
        stable = stable + 1 if state == prev and all(s == 'completed' for _, s, _ in state) else 0
        prev = state
        if not wait or stable >= 1: break
        time.sleep(60)
    print('RUNS at %s: %d (author claimed %d) | stable-read %s' % (head[:12], n, AC['author_claim_runs_at_head'], 'two consecutive agreeing' if stable >= 1 else 'ONE read'))
    rc = 0 if n_fab == 0 else 1
    pend = [r for r in runs if r['status'] != 'completed']
    for r in sorted(runs, key=lambda r: r['name']):
        print('RUN %-34s %-11s %s' % (r['name'], r['status'], r.get('conclusion')))
    if pend: print('PENDING %s -> rc 1 (never read as clear)' % [r['name'] for r in pend]); rc = 1
    dev_runs = {}
    for dsha, what in AC['develop_side_heads'].items():
        try: dev_runs[dsha] = runs_at(dsha)[1]
        except (OSError, ValueError, urllib.error.URLError) as e: dev_runs[dsha] = []; print('DEV %s runs unreadable: %s' % (dsha[:12], e))
    for r in runs:
        if r.get('conclusion') not in FAILING: continue
        jobs = gh_pages('actions/runs/%d/jobs?filter=latest' % r['id'])
        for j in [j for j in jobs if j.get('conclusion') in FAILING]:
            needle = known_for(r['name'], j['name'])
            text = gh_job_log(j['id']); hc, hd = classify_log(text, needle)
            dcls = []
            for dsha, druns in dev_runs.items():
                for dr in [x for x in druns if x['name'] == r['name']]:
                    for dj in [x for x in gh_pages('actions/runs/%d/jobs?filter=latest' % dr['id']) if x['name'] == j['name']]:
                        dc, dd = classify_log(gh_job_log(dj['id']), needle); dcls.append(dc)
                        print('    DEV %s %s / %s: %s %s' % (dsha[:12], dr['name'], dj['name'], dc, dd))
            v = verdict(hc, dcls)
            print('  HEAD %s / %s: %s %s -> %s' % (r['name'], j['name'], hc, hd, v))
            if r['name'] == 'PR Security Gates (KS-168)':
                from lib_gate71 import Tally
                t = Tally(); C3.classify_text(text, t); print('    c3 classify on this log: %d FAIL %s' % (len(t.fails), t.fails))
                if t.fails: rc = 1
            if v.startswith('UNCLASSIFIED'): rc = 1
    return rc


def census():
    out_rows, cnt = [], {}
    rows = list(K['rows'])
    for pr in gh_pages('pulls?state=open'):
        if str(pr['number']) in rows: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % pr['number'])]
        c = classify_pr(pr, files); cnt[c] = cnt.get(c, 0) + 1
        if c != 'other': out_rows.append('  %s #%d %s %s' % (c, pr['number'], pr['head']['sha'][:12], pr['title'][:70]))
    ctl = classify_pr({'title': 'x'}, [CODE[0]]) == 'OVERLAP' and classify_pr({'title': 'x'}, [DOCS[0]]) == 'DOCS' and classify_pr({'title': 'y'}, ['a.ts']) == 'other'
    print('CENSUS %d other open PR(s): %s | CONTROL fires %s' % (sum(cnt.values()), cnt, ctl))
    for r in out_rows: print(r)
    return 3 if not ctl else (1 if cnt.get('OVERLAP') else 0)


ALL_CODE = sorted({p for R in K['rows'].values() for p in R['numstat'] if not p.startswith('Projects Documents/')})
ALL_KEYS = [R['ticket'] for R in K['rows'].values()]


def classify_pr(pr, files):
    if any(k in (pr.get('title') or '') for k in ALL_KEYS) or set(files) & set(ALL_CODE): return 'OVERLAP'
    if set(files) & set(DOCS): return 'DOCS'
    return 'other'


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    g = '##[group]Run x\n'
    rep(classify_log(g + "Error: Cannot find package 'semver' imported from …", "Cannot find package 'semver'")[0] == 'NEEDLE', 'a read log carrying the needle: NEEDLE')
    rep(classify_log("Cannot find package 'semver'", "Cannot find package 'semver'")[0] == 'UNREAD', 'PLANTED log with 0 `##[group]` (unread): UNREAD, never clean')
    rep(classify_log(g + 'bash Blockchain/Testing/jobs/09-aggregate-report.sh failed', 'x')[0] == 'OWN-PATH', 'PLANTED own path in the log: OWN-PATH')
    rep(classify_log(g + 'something else broke', 'No stack slot named')[0] == 'NO-NEEDLE', 'a different failure: NO-NEEDLE')
    rep(verdict('NEEDLE', ['NO-NEEDLE', 'NEEDLE']).startswith('KNOWN'), 'needle at head + one develop-side head: KNOWN-CLASS')
    rep(verdict('NEEDLE', ['NO-NEEDLE']).startswith('UNCLASSIFIED'), 'PLANTED needle at the head only (not on develop): UNCLASSIFIED')
    rep(verdict('NO-NEEDLE', ['NEEDLE']).startswith('UNCLASSIFIED'), 'PLANTED head without the needle: UNCLASSIFIED')
    rep(known_for('pr', 'Akto suite (PR)') == AC['known_classes']['pr/Akto']['needle'] and known_for('Security Scanning', 'Dependency Audit') == "Cannot find package 'semver'", 'needle lookup by run / job name')
    k, c = scan('Refs KS-1136\nKS 878 guarded 04.'); rep(k == ['KS-1136'] and not c, 'scan: de-hyphenated keys are not keys')
    k, c = scan('Closes KS-1136. Fixes KS-878.'); rep(k == ['KS-1136', 'KS-878'] and len(c) == 2, 'PLANTED Closes / Fixes: two closing refs and a second key')
    rep(refs_window('x\nthis resolves the bug\nRefs %s' % KEY)[1] and not refs_window('Refs %s\nhttps://x' % KEY)[1], 'closing word within 3 lines above `Refs %s` FIRES; a clean Refs passes' % KEY)
    if P['pr'] == '1404':
        g4 = 'Red-first 1 passed / 4 failed -> 5 passed / 0 failed. A `2>/dev/null` arm reads 4 passed / 1 failed. Discovery 67 -> 68. Whole shell-suite set 68 passed, 0 failed, 0 skipped (of 68), 339s.'
        rep(all(x[3] and x[1] for x in claims(g4, {})), 'claims (#1404): the commit-message figures pass, every claim FOUND')
        rep(not all(x[3] for x in claims(g4.replace('4 passed / 1 failed', '3 passed / 2 failed'), {})), 'PLANTED #1404 devnull figure 3/2 FAILS')
    h, s, l = job06_lines('##[group]x\nBlockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh: stub 06-tenant-isolation ok\nbash jobs/06-tenant-isolation.sh\n')
    rep(len(h) == 2 and len(s) == 1 and len(l) == 1, 'job06: a needle line carrying a __tests__ suite path is STUB; a bare `bash jobs/06-tenant-isolation.sh` line is LIVE (PLANTED live line found; line-local and CONSERVATIVE: an unattributed line reads LIVE and is read by a human)')
    rep(job06_lines('##[group]x\nnothing here\n') == ([], [], []), 'job06: a log without any job-06 needle reads 0 lines')
    good = '- the new suite alone: **6 passed, 0 failed, rc 0** x\n**rc 1, 3 failed** -- cells\n**2 passed, 4 failed**. A *missing* y\n**4 passed, 2 failed**. Every *present* z\ngoes **67 -> 68**\n**68 passed, 0 failed, 0 skipped (of 68)** in\n(100755 -> 100755, +14/-0)'
    if P['pr'] == '1398':
        rep(all(x[3] and x[1] for x in claims(good, {})), 'claims (#1398): a body with the author\'s true figures passes, every claim FOUND')
        rep(not all(x[3] for x in claims(good.replace('**2 passed, 4 failed**', '**3 passed, 3 failed**'), {})), 'PLANTED arm-A figure 3/3 FAILS')
    rep(classify_pr({'title': 'x'}, [CODE[0]]) == 'OVERLAP' and classify_pr({'title': 'x'}, [DOCS[1]]) == 'DOCS' and classify_pr({'title': 'KS-1136 y'}, []) == 'OVERLAP'
        and classify_pr({'title': 'KS-1436 z'}, []) == 'OVERLAP' and classify_pr({'title': 'x'}, ['Blockchain/Testing/jobs/06-tenant-isolation.sh']) == 'OVERLAP', 'census classifier (both rows: keys and code paths)')
    import urllib.request
    req = urllib.request.Request('https://signed.example/log?sig=1')
    rep('Authorization' not in req.headers and issubclass(lib_gate71._NoRedirect, urllib.request.HTTPRedirectHandler)
        and lib_gate71._NoRedirect().redirect_request(None, None, 302, '', {}, 'u') is None, 'the log fetch does NOT auto-follow the 302, and the signed-URL request carries no Authorization header')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if not A: print(__doc__); return 2
    try:
        if A[0] == '--selftest': return selftest()
        head = opt(A, '--head', P['head_expected'])
        if A[0] == 'api': return api(head)
        if A[0] == 'prtext': return prtext(head, opt(A, '--measured'))
        if A[0] == 'actions': return actions(opt(A, '--at', head), '--wait' in A)
        if A[0] == 'census': return census()
        if A[0] == 'job06':
            shas = [A[i + 1] for i, a in enumerate(A) if a == '--at' and i + 1 < len(A)]
            if not shas or not all(re.fullmatch(r'[0-9a-f]{40}', s) for s in shas): print('REFUSED: job06 needs one or more --at <40-hex>'); return 2
            return job06(shas)
    except (OSError, ValueError, urllib.error.URLError, KeyError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
