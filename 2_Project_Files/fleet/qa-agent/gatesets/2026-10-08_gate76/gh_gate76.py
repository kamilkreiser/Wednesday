#!/usr/bin/env python3
r"""gh_gate76.py — READ-ONLY GitHub GETs for gate76 (X6). Carried from gh_gate75.py and re-keyed by the gate76 drafter: TWO rows (#1427,
#1428; `--pr` REQUIRED, no default); `prtext` T5 names each row's own NOT-RUN items (#1427: the live trivy scan; #1428: the live
PostgreSQL run) and a NEW T6 REPORTS attribution lines (`Generated with`) the squash body must not carry; the CI log extractor reads the
`container_trivy_*` and `shell suites:` lines instead of leg 14; census keys on BOTH rows' code paths, the trivy job's consumers and the
two docs. GH_TOKEN by NAME inside lib_gate76, never printed. No write verb exists here.

MODES
  api     --pr R --head H         open, unmerged, base develop, head.sha == H, 1 commit, files / +- == kit numstat; mergeable_state printed
                                  (NO testing claim); body sha256/16 vs the drafter's; title REPORTED.                  rc 0 / 11 / 3 API
  prtext  --pr R --head H         T1 the `Refs KS-n` set carries the own key (mergera1 requires own_keys == this set);
                                  T2 0 closing-family words on any KS key in title + body (BINDING; CONTROL planted `Fixes KS-1` = 1);
                                  T3 hyphenated keys REPORTED (foreign keys attach: STANDING_LINES :278); T4 title length / ASCII REPORTED;
                                  T5 the body has a NOT RUN section naming the row's live-run gap and the platform suites;
                                  T6 attribution lines (`Generated with`, `Co-Authored-By`) REPORTED: the squash body carries 0 (Q-ATTR76);
                                  T7 every sentence carrying a number, dumped for the gate to read against its own measurement.
  actions --pr R --at H --develop D --base B --comparator develop|base|union [--history N] [--wait]
                                  carried unchanged in logic from gh_gate75 (three classes, SUBSET, fabricated-sha control, failing-job logs
                                  with `##[group]` control, PENDING never a pass, a 0-runs comparator RE-READ). base == develop at draft.
  census  --pr R                  every OTHER open PR touching either row's code paths, the trivy job's consumers, or a platform doc; and any
                                  titled with KS 1274 / KS 593. REPORT only.
  --selftest                      the classifier and the text checks on FIXTURES (no network; the REAL #1427 and #1428 bodies at draft).
rc 0 PASS / 1 FAIL or OUTSIDE or PENDING / 3 API failure / 11 PR state wrong."""
import hashlib, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate76 import K, ROWS, Tally, opt, row_arg, gh_get, gh_pages, gh_job_log

CLASS_WF = {'Security Scanning': 1, 'PR Security Gates (KS-168)': 2, 'pr': 3}
NEEDLES_1 = K['actions']['classes']['1']['needles']
STEP_1 = K['actions']['classes']['1']['failed_step_prefix']
CENSUS_PATHS = {p for R_ in ROWS.values() for p in R_['numstat'] if not p.startswith('Projects Documents/')} | {
    'Blockchain/Testing/jobs/09-aggregate-report.sh', 'Blockchain/Testing/ci/orchestrate.sh', 'Blockchain/Dev/scripts/docker-build.sh',
    'Blockchain/Dev/services/originate/src/middleware/auth.ts'}
NOT_RUN_NAMED = {'1427': ('live', 'trivy', 'Schemathesis'), '1428': ('live run', 'PostgreSQL', 'Schemathesis')}


def api(r, head):
    R = ROWS[r]; t = Tally()
    try: p = gh_get('pulls/%s' % r)
    except Exception as x: print('API FAILURE: %s' % str(x)[:200]); return 3
    t.check('A1', p['state'] == 'open' and not p.get('merged') and p['base']['ref'] == 'develop', 'state %s merged %s base %s' % (p['state'], p.get('merged'), p['base']['ref']))
    t.check('A2', p['head']['sha'] == head, 'head.sha %s == %s' % (p['head']['sha'][:12], head[:12]))
    ns = R['numstat']; adds = sum(v[0] for v in ns.values()); dels = sum(v[1] for v in ns.values())
    t.check('A3', p['commits'] == 1 and p['changed_files'] == len(ns) and p['additions'] == adds and p['deletions'] == dels,
            'commits %s files %s +%s -%s (kit 1 / %d / +%d -%d)' % (p['commits'], p['changed_files'], p['additions'], p['deletions'], len(ns), adds, dels))
    body = (p.get('body') or '').encode()
    t.info('A4', 'title %d chars ASCII %s == kit pr_title %s (REPORTED: not the squash subject, Q-SUBJ76)' % (len(p['title']), p['title'].isascii(), p['title'] == R['pr_title']))
    t.info('A5', 'mergeable %s mergeable_state %s (NO testing claim either way) | body %d B sha256/16 %s (drafter %s) | base.sha %s' % (
        p.get('mergeable'), p.get('mergeable_state'), len(body), hashlib.sha256(body).hexdigest()[:16], R['body_sha256_16_at_draft'], p['base']['sha'][:12]))
    rc = t.end()
    return 11 if rc and any(x in t.fails for x in ('A1', 'A2')) else rc


def text_checks(r, title, body):
    R = ROWS[r]; t = Tally(); allt = title + '\n' + body
    refs = sorted(set(re.findall(r'Refs:?\s+(KS-\d+)\b', body)))
    t.check('T1', R['ticket'] in refs, '`Refs KS-n` set %s carries the own key %s | kit default own keys %s | EXTRA Refs %s (Q-KEYS76: mergera1 requires own_keys == this set)' % (
        refs, R['ticket'], R['own_keys_default'], sorted(set(refs) - set(R['own_keys_default'])) or 'none'))
    cl = re.findall(K['closing_rx'], allt, re.I); clc = re.findall(K['closing_rx'], allt + '\nFixes KS-1\n', re.I)
    t.check('T2', not cl and len(clc) == 1, 'closing-family words on a key %d %s | CONTROL planted `Fixes KS-1` %d' % (len(cl), cl[:3], len(clc)))
    hy = sorted(set(re.findall(r'\bKS-\d+\b', allt)))
    t.info('T3', 'hyphenated keys in title+body %s | foreign (attach, STANDING_LINES :278) %s | de-hyphenated %s' % (
        hy, sorted(set(hy) - set(R['own_keys_default'])), sorted(set(re.findall(r'\bKS \d+\b', allt)))[:12]))
    t.info('T4', 'title %d chars, ASCII %s, `(#` %s (the title is NOT the squash subject)' % (len(title), title.isascii(), '(#' in title))
    nr = re.search(r'(?is)\*\*NOT RUN', body) is not None
    named = [s for s in NOT_RUN_NAMED[r] if s in body]
    t.check('T5', nr and len(named) == len(NOT_RUN_NAMED[r]), 'body has a NOT RUN section %s naming %s of %s' % (nr, named, list(NOT_RUN_NAMED[r])))
    gen = len(re.findall(r'(?im)^.*generated with \[claude code\]', body)); cab = len(re.findall(r'(?im)^co-authored-by:', body))
    t.info('T6', 'attribution lines in the body: `Generated with` %d, `Co-Authored-By` %d (the SQUASH body carries 0 of each: Q-ATTR76; landed fleet squashes carry 0)' % (gen, cab))
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n', body) if re.search(r'\d', s) and len(s.strip()) > 12]
    t.info('T7', '%d sentences carry a number; dumped for the gate to read against its OWN measurement' % len(sents))
    return t, sents


def prtext(r, head):
    try: p = gh_get('pulls/%s' % r)
    except Exception as x: print('API FAILURE: %s' % str(x)[:200]); return 3
    if p['head']['sha'] != head: print('REFUSED: the PR head %s != --head %s' % (p['head']['sha'][:12], head[:12])); return 11
    t, sents = text_checks(r, p['title'], p.get('body') or '')
    for s in sents: print('   T7| %s' % s[:220])
    return t.end()


def suite_tallies(lg, needle):
    """{suite basename: 'N passed, M failed'} for every `=== <path> ===` header containing NEEDLE: the FIRST tally line after the header.
    WHY: the CI step prints the suite name and its tally on DIFFERENT lines (drafter 07:5xZ: a same-line regex read 0 tallies while the
    three headers were present: a false zero). A header with no tally before the next header reads 'NO TALLY' (never a pass)."""
    out, cur = {}, None
    for l in lg.split('\n'):
        m = re.search(r'=== (\S+) ===', l)
        if m: cur = os.path.basename(m.group(1)) if needle in m.group(1) else None
        if cur: out.setdefault(cur, 'NO TALLY')
        t = re.search(r'(\d+ passed, \d+ failed)', l)
        if cur and t and out[cur] == 'NO TALLY': out[cur] = t.group(1); cur = None
    return out


def runs_at(sha):
    return gh_pages('actions/runs?head_sha=%s' % sha, 'workflow_runs')


def latest_per_wf(runs):
    by = {}
    for r_ in runs:
        k = r_['name']
        if k not in by or (r_['run_number'], r_['run_attempt']) > (by[k]['run_number'], by[k]['run_attempt']): by[k] = r_
    return by


def failing_jobs(run):
    js = gh_pages('actions/runs/%s/jobs' % run['id'], 'jobs')
    return sorted(j['name'] for j in js if j.get('conclusion') == 'failure'), js


def classify(head_wf, dev_wf, hist1=None):
    """PURE: head_wf / dev_wf = {workflow: {'status','conclusion','failing': [jobs], 'needles1': bool}} -> (rows, outside, pending)."""
    rows = []; outside = []; pending = []
    for wf, h in sorted(head_wf.items()):
        if h['status'] != 'completed': pending.append(wf); rows.append((wf, 'PENDING', h)); continue
        if h['conclusion'] in ('success', 'skipped', 'neutral'): rows.append((wf, h['conclusion'], h)); continue
        c = CLASS_WF.get(wf)
        if c is None: outside.append(wf); rows.append((wf, 'OUTSIDE the three classes (a NO GO finding)', h)); continue
        hs = set(h['failing'])
        if c == 1:
            ok = hs <= {'Dependency Audit'} and bool(hs) and h.get('needles1', False)
            rows.append((wf, 'class (1) advisory-freeze %s: failing %s SUBSET of {Dependency Audit} %s; audit-contract step + log needle: %s%s' % (
                'HOLDS' if ok else 'DOES NOT HOLD', sorted(hs), hs <= {'Dependency Audit'}, h.get('needles1'), ('; history %s' % hist1) if hist1 else ''), h))
            if not ok: outside.append(wf)
        else:
            d = dev_wf.get(wf); ds = set(d['failing']) if d else None
            ok = ds is not None and hs <= ds
            better = sorted(ds - hs) if ds is not None else []
            rows.append((wf, 'class (%d) %s: head failing %s SUBSET of the comparator\'s %s: %s%s' % (
                c, 'HOLDS' if ok else 'DOES NOT HOLD', sorted(hs), sorted(ds) if ds is not None else 'NO COMPARATOR', ok,
                ('; the comparator fails, head PASSES: %s (named, no cause claimed)' % better) if better else ''), h))
            if not ok: outside.append(wf)
    return rows, outside, pending


def read_head(sha, log_needles=True):
    runs = runs_at(sha); by = latest_per_wf(runs); out = {}
    for wf, r_ in by.items():
        e = {'status': r_['status'], 'conclusion': r_['conclusion'], 'failing': [], 'run_id': r_['id'], 'logs': {}}
        if r_['status'] == 'completed' and r_['conclusion'] == 'failure':
            e['failing'], js = failing_jobs(r_)
            if log_needles:
                for j in js:
                    if j.get('conclusion') != 'failure': continue
                    try: lg = gh_job_log(j['id'])
                    except Exception as x: e['logs'][j['name']] = {'error': str(x)[:120]}; continue
                    fsteps = [s_['name'] for s_ in j.get('steps', []) if s_.get('conclusion') == 'failure']
                    e['logs'][j['name']] = {'bytes': len(lg), 'groups': lg.count('##[group]'), 'fabricated_needle': lg.count('gate76-fabricated-needle-zz'),
                                            'failed_steps': fsteps, 'needles1': {n: lg.count(n) for n in NEEDLES_1},
                                            'shell_suites': re.findall(r'shell suites: \d+ passed, \d+ failed, \d+ skipped \(of \d+\)', lg)[-1:],
                                            'FAILED': re.findall(r'FAILED: (\S+)', lg),
                                            'trivy_suites': suite_tallies(lg, 'container_trivy_')}
                    if wf == 'Security Scanning' and j['name'] == 'Dependency Audit':
                        e['needles1'] = all(lg.count(n) > 0 for n in NEEDLES_1) and lg.count('##[group]') > 0 and \
                            len(fsteps) == 1 and fsteps[0].startswith(STEP_1)
        out[wf] = e
    return runs, out


def actions(r, head, dev, base, comparator, hist_n=12, wait=False):
    t = Tally(); fab = 'f' * 40
    try:
        n_fab = len(runs_at(fab)); prev = None; polls = 0
        while True:
            runs, head_wf = read_head(head)
            sig = json.dumps({k: (v['status'], v['conclusion'], v['failing']) for k, v in head_wf.items()}, sort_keys=True)
            polls += 1
            pend = [k for k, v in head_wf.items() if v['status'] != 'completed']
            if not wait or (sig == prev and not pend) or polls >= 30: break
            prev = sig; time.sleep(60)
        _, dev_wf = read_head(dev, log_needles=True)
        if not dev_wf: time.sleep(5); _, dev_wf = read_head(dev, log_needles=True)
        if base == dev: base_wf = dev_wf
        else:
            _, base_wf = read_head(base, log_needles=False)
            if not base_wf: time.sleep(5); _, base_wf = read_head(base, log_needles=False)
        union = {}
        for wf in set(dev_wf) | set(base_wf):
            fs = set(dev_wf.get(wf, {}).get('failing', [])) | set(base_wf.get(wf, {}).get('failing', []))
            union[wf] = {'status': 'completed', 'conclusion': 'failure' if fs else 'success', 'failing': sorted(fs)}
        hist = gh_pages('actions/runs?per_page=100', 'workflow_runs')
        ss = [x for x in hist if x['name'] == 'Security Scanning' and x['status'] == 'completed'][:hist_n]
        hist1 = '%d of the last %d completed Security Scanning runs repo-wide FAILED across %d branches' % (
            sum(1 for x in ss if x['conclusion'] == 'failure'), len(ss), len(set(x['head_branch'] for x in ss)))
    except Exception as x:
        print('API FAILURE: %s' % str(x)[:200]); return 3
    t.check('X0', len(runs) > 0 and n_fab == 0, 'runs at the FULL head sha %d | CONTROL a fabricated sha reads %d | polls %d%s' % (len(runs), n_fab, polls, ' (two agreeing)' if wait else ''))
    for nm, wfs in (('head', head_wf), ('develop', dev_wf)):
        for wf, e in sorted(wfs.items()):
            for jn, lg in e['logs'].items(): t.info('LOG', '%s %s / %s: %s' % (nm, wf, jn, lg))
    comps = {'develop': dev_wf, 'base': base_wf, 'union': union}
    for name, cw in comps.items():
        rr, oo, _ = classify(head_wf, cw, hist1)
        print('  -- against %s%s: OUTSIDE %s' % (name, ' (THE RULED COMPARATOR)' if name == comparator else '', oo or 'none'))
        for wf, verdict, h in rr: print('     %-34s %s' % (wf, verdict))
    rows, outside, pending = classify(head_wf, comps[comparator], hist1)
    t.check('X1', not outside, 'reds OUTSIDE the three classes (or a class that does not hold): %s' % (outside or 'none'))
    t.check('X2', not pending, 'PENDING (never a pass): %s' % (pending or 'none'))
    t.info('X3', 'develop %s: %s | base %s %s' % (dev[:12], {k: (v['conclusion'], v['failing']) for k, v in sorted(dev_wf.items())}, base[:12], '(== develop)' if base == dev else ''))
    return t.end()


def census(r):
    t = Tally()
    try: prs = gh_pages('pulls?state=open', 'pulls')
    except Exception as x: print('API FAILURE: %s' % str(x)[:200]); return 3
    docs = {K['docs']['flow'], K['docs']['cheat']}; keys = {'KS-1274', 'KS 1274', 'KS-593', 'KS 593'}; found = 0
    for p in prs:
        n = str(p['number'])
        if n == r: continue
        fs = [f['filename'] for f in gh_pages('pulls/%s/files' % n, 'files')]
        ov = sorted(set(fs) & CENSUS_PATHS); dd = sorted(set(fs) & docs); kk = [k for k in keys if k in (p['title'] or '')]
        if ov or dd or kk:
            found += 1
            print('   #%s %-60s OVERLAP %s DOCS %s TITLE-KEYS %s' % (n, (p['title'] or '')[:60], ov, [os.path.basename(x) for x in dd], kk))
    t.check('C0', any(str(p['number']) == r for p in prs), 'open PRs read %d (CONTROL: #%s itself is among them)' % (len(prs), r))
    t.info('C1', '%d other open PR(s) collide (REPORT only; a DOCS collision landing first changes develop\'s doc blobs and re-runs c4 chain)' % found)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    dev = {'PR Security Gates (KS-168)': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Code Security Gates']},
           'pr': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Akto suite (PR)', 'Performance suite (k6 smoke)', 'Playwright suite', 'Schemathesis suite']}}
    good = {'Security Scanning': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Dependency Audit'], 'needles1': True},
            'PR Security Gates (KS-168)': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Code Security Gates']},
            'pr': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Akto suite (PR)', 'Performance suite (k6 smoke)', 'Playwright suite', 'Schemathesis suite']},
            'pr-premerge-ack': {'status': 'completed', 'conclusion': 'success', 'failing': []}}
    rows, o, p = classify(good, dev); rep(not o and not p, 'a head whose sets EQUAL the comparator\'s: subset holds, no OUTSIDE, no PENDING')
    bad = json.loads(json.dumps(good)); bad['pr']['failing'].append('Unit tests')
    rows, o, p = classify(bad, dev); rep(o == ['pr'], 'PLANTED a red the comparator lacks (`Unit tests` in pr): OUTSIDE %s' % o)
    bad2 = json.loads(json.dumps(good)); bad2['CodeQL'] = {'status': 'completed', 'conclusion': 'failure', 'failing': ['analyze']}
    rows, o, p = classify(bad2, dev); rep('CodeQL' in o, 'PLANTED a failing workflow outside the three classes: OUTSIDE %s' % o)
    bad3 = json.loads(json.dumps(good)); bad3['Security Scanning']['needles1'] = False
    rows, o, p = classify(bad3, dev); rep('Security Scanning' in o, 'PLANTED class (1) whose log lacks the audit-contract needle: DOES NOT HOLD')
    pen = json.loads(json.dumps(good)); pen['pr'] = {'status': 'in_progress', 'conclusion': None, 'failing': []}
    rows, o, p = classify(pen, dev); rep(p == ['pr'], 'PLANTED pr in_progress: PENDING %s (never a pass)' % p)
    rows, o, p = classify(good, {}); rep(set(o) == {'pr', 'PR Security Gates (KS-168)'}, 'PLANTED no comparator: classes 2/3 DO NOT HOLD (%s)' % o)
    cap = ('2026-10-08T07:00:00.0Z === Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh ===\n'
           '2026-10-08T07:00:00.1Z   ok   CONTROL - two clean scans\n2026-10-08T07:00:00.2Z \n2026-10-08T07:00:00.3Z   5 passed, 0 failed\n'
           '2026-10-08T07:00:00.4Z === Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh ===\n'
           '2026-10-08T07:00:00.5Z === Blockchain/Dev/scripts/__tests__/other.test.sh ===\n2026-10-08T07:00:00.6Z   9 passed, 0 failed\n')
    st = suite_tallies(cap, 'container_trivy_')
    rep(st == {'container_trivy_failed_scan_is_loud.test.sh': '5 passed, 0 failed', 'container_trivy_image_filter.test.sh': 'NO TALLY'},
        'suite_tallies on a CAPTURED-shape log (header and tally on separate lines; a header with no tally reads NO TALLY, a foreign suite\'s tally is not borrowed): %s' % st)
    import io, contextlib
    for r in ROWS:
        R = ROWS[r]
        body = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixture_body_%s_at_draft.md' % r), encoding='utf-8').read()
        rep(hashlib.sha256(body.encode()).hexdigest()[:16] == R['body_sha256_16_at_draft'], 'fixture = the REAL #%s body read by GET at draft (sha256/16 %s)' % (r, R['body_sha256_16_at_draft']))
        with contextlib.redirect_stdout(io.StringIO()): t, _ = text_checks(r, R['pr_title'], body)
        rep(not t.fails, 'prtext GREEN on the REAL #%s body: fails %s' % (r, t.fails))
        with contextlib.redirect_stdout(io.StringIO()): t, _ = text_checks(r, R['pr_title'], body + 'Fixes %s\n' % R['ticket'])
        rep('T2' in t.fails, 'PLANTED `Fixes %s` on #%s: T2 FAILS' % (R['ticket'], r))
        with contextlib.redirect_stdout(io.StringIO()): t, _ = text_checks(r, R['pr_title'], body.replace('Refs %s' % R['ticket'], 'Refs %s' % R['ticket'].replace('-', ' ')))
        rep('T1' in t.fails, 'PLANTED #%s\'s own Refs de-hyphenated: T1 FAILS' % r)
        with contextlib.redirect_stdout(io.StringIO()): t, _ = text_checks(r, R['pr_title'], body.replace('**NOT run', '**RAN').replace('**NOT RUN', '**RAN'))
        rep('T5' in t.fails, 'PLANTED #%s\'s NOT RUN section removed: T5 FAILS' % r)
    R = ROWS['1428']; body = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixture_body_1428_at_draft.md'), encoding='utf-8').read()
    with contextlib.redirect_stdout(io.StringIO()): t, _ = text_checks('1428', R['pr_title'], body + '\nThis does not close KS-593.\n')
    rep('T2' in t.fails, 'PLANTED the COMMIT-MESSAGE residue `does not close KS-593` into #1428\'s body: T2 FAILS (the negation does not hide the adjacency)')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    mode = A[0] if A else ''
    if mode == 'api': return api(row_arg(), opt(A, '--head'))
    if mode == 'prtext': return prtext(row_arg(), opt(A, '--head'))
    if mode == 'actions':
        h, d, b, c = opt(A, '--at'), opt(A, '--develop'), opt(A, '--base'), opt(A, '--comparator')
        if not (h and d and b and all(re.fullmatch(r'[0-9a-f]{40}', x) for x in (h, d, b))): print('REFUSED: --at, --develop and --base must be FULL 40-hex'); return 2
        if c not in ('develop', 'base', 'union'): print('REFUSED: --comparator develop|base|union is REQUIRED; no default'); return 2
        return actions(row_arg(), h, d, b, c, int(opt(A, '--history', '12')), '--wait' in A)
    if mode == 'census': return census(row_arg())
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
