#!/usr/bin/env python3
r"""gh_gate73.py — READ-ONLY GitHub GETs for gate73 (X6). GH_TOKEN by NAME inside lib_gate73, never printed. No write verb exists here.

MODES
  api     --pr R --head H         open, unmerged, base develop, head.sha == H, 1 commit, files / +- == kit numstat; mergeable_state
                                  printed (carries NO testing claim); body sha256/16; title == the kit subject.        rc 0 / 11 / 3 API
  prtext  --pr R --head H         T1 exactly one `Refs <own key>` line; T2 0 closing-family words on any KS key in title + body (CONTROL
                                  planted `Fixes KS-1` = 1); T3 only the row's key hyphenated (CONTROL planted KS-9999 found); T4 title ==
                                  subject, LANDS <= 92; T5 the body names the four platform suites UNMEASURED (never a pass); T6 the
                                  live-sweep sentence: OWED for a runtime change (#1408), NOT owed for the others; T7 every sentence carrying
                                  a number, dumped for the gate to read against its own measurement.
  actions --pr R --at H --develop D [--history N] [--wait]
                                  every run by FULL 40-hex head_sha (CONTROL: a fabricated sha reads 0 runs, the head reads > 0); per
                                  workflow the LATEST run; failing jobs per run; each failing job's LOG read (the 302 followed WITHOUT auth;
                                  `##[group]` positive control; a fabricated needle 0). CLASSIFIED by Wednesday's three classes with the
                                  SUBSET predicate (never equality):
                                   (1) Security Scanning: failing jobs SUBSET of {Dependency Audit} AND its log carries the audit-contract
                                       needles; history: how many of the last N Security Scanning runs repo-wide failed (develop runs none on
                                       push, so history is the comparator);
                                   (2) PR Security Gates (KS-168): failing jobs SUBSET of develop D's failing jobs on the same workflow;
                                   (3) pr: failing jobs SUBSET of develop D's failing jobs on `pr`; every job develop fails that the head
                                       PASSES is named (Schemathesis at #1407).
                                  ANY failing run outside the three = OUTSIDE (a NO GO finding). A run not completed = PENDING (never a pass);
                                  --wait polls until two consecutive reads agree and nothing is pending (max 30 min).
  census  --pr R                  every OTHER open PR touching a row's code path (OVERLAP) or a platform doc (DOCS: forces a keep-both
                                  merge-in on whichever lands later), and any titled with a batch ticket. REPORT only.
  --selftest                      the classifier and the text checks on FIXTURES (no network), with planted arms that MUST fail.
rc 0 PASS / 1 FAIL or OUTSIDE or PENDING / 3 API failure / 11 PR state wrong."""
import hashlib, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate73 import K, ROWS, Tally, opt, row_arg, gh_get, gh_pages, gh_job_log, code_paths

CLASS_WF = {'Security Scanning': 1, 'PR Security Gates (KS-168)': 2, 'pr': 3}
NEEDLES_1 = K['actions']['classes']['1']['needles']
STEP_1 = K['actions']['classes']['1']['failed_step_prefix']
SUITES4 = ['Schemathesis', 'Akto', 'Playwright', 'erformance']


def api(r, head):
    R = ROWS[r]; t = Tally()
    try: p = gh_get('pulls/%s' % r)
    except Exception as x: print('API FAILURE: %s' % str(x)[:200]); return 3
    t.check('A1', p['state'] == 'open' and not p.get('merged') and p['base']['ref'] == 'develop', 'state %s merged %s base %s' % (p['state'], p.get('merged'), p['base']['ref']))
    t.check('A2', p['head']['sha'] == head, 'head.sha %s == %s' % (p['head']['sha'][:12], head[:12]))
    ns = R['numstat']; adds = sum(v[0] for v in ns.values()); dels = sum(v[1] for v in ns.values())
    t.check('A3', p['commits'] == 1 and p['changed_files'] == len(ns) and p['additions'] == adds and p['deletions'] == dels,
            'commits %s files %s +%s -%s (kit 1 / %d / +%d -%d)' % (p['commits'], p['changed_files'], p['additions'], p['deletions'], len(ns), adds, dels))
    t.check('A4', p['title'] == R['subject'], 'title == kit subject: %s (%r)' % (p['title'] == R['subject'], p['title'][:90]))
    body = (p.get('body') or '').encode()
    t.info('A5', 'mergeable %s mergeable_state %s (NO testing claim either way) | body %d B sha256/16 %s | base.sha %s' % (
        p.get('mergeable'), p.get('mergeable_state'), len(body), hashlib.sha256(body).hexdigest()[:16], p['base']['sha'][:12]))
    rc = t.end()
    return 11 if rc and any(x in t.fails for x in ('A1', 'A2')) else rc


def text_checks(r, title, body):
    R = ROWS[r]; t = Tally(); allt = title + '\n' + body; own = R['keys_hyphenated_allowed']
    refs = re.findall(r'(?im)^\s*Refs:?\s+(KS-\d+)\b', body)
    t.check('T1', refs == [R['ticket']], '`Refs <key>` lines %s (want exactly [%s])' % (refs, R['ticket']))
    cl = re.findall(K['closing_rx'], allt, re.I); clc = re.findall(K['closing_rx'], allt + '\nFixes KS-1\n', re.I)
    t.check('T2', not cl and len(clc) == 1, 'closing-family words on a key %d %s | CONTROL planted `Fixes KS-1` %d' % (len(cl), cl[:3], len(clc)))
    hy = sorted(set(re.findall(r'\bKS-\d+\b', allt)))
    t.check('T3', hy == sorted(own) and 'KS-9999' in re.findall(r'\bKS-\d+\b', allt + ' KS-9999'), 'hyphenated keys %s (want only %s) | de-hyphenated %s' % (
        hy, own, sorted(set(re.findall(r'\bKS \d+\b', allt)))[:12]))
    lands = len(title) + len(' (#%s)' % r)
    t.check('T4', title == R['subject'] and lands <= K['squash_max'], 'title == subject %s; LANDS %d <= %d' % (title == R['subject'], lands, K['squash_max']))
    um = re.search(r'(?is)unmeasured', body) is not None; named = [s for s in SUITES4 if s.lower() in body.lower()]
    t.check('T5', um and len(named) == 4, 'body says UNMEASURED %s and names the four platform suites %s' % (um, named))
    sweep_owed = re.search(r'(?is)live sweep[^.\n]{0,40}\b(is |)owed|sweep owed', body) is not None
    sweep_not = re.search(r'(?is)no live sweep|live sweep is not owed|not owe[sd]? a live sweep|NO live sweep owed', body) is not None
    t.check('T6', (sweep_owed and not sweep_not) if R['live_sweep_owed'] else (sweep_not or not sweep_owed),
            'runtime change %s: body says sweep OWED %s / NOT owed %s' % (R['runtime_change'], sweep_owed, sweep_not))
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n', body) if re.search(r'\d', s) and len(s.strip()) > 12]
    t.info('T7', '%d sentences carry a number; dumped for the gate to read against its OWN measurement (first 3: %s)' % (len(sents), [s[:80] for s in sents[:3]]))
    return t, sents


def prtext(r, head):
    try: p = gh_get('pulls/%s' % r)
    except Exception as x: print('API FAILURE: %s' % str(x)[:200]); return 3
    if p['head']['sha'] != head: print('REFUSED: the PR head %s != --head %s' % (p['head']['sha'][:12], head[:12])); return 11
    t, sents = text_checks(r, p['title'], p.get('body') or '')
    for s in sents: print('   T7| %s' % s[:220])
    return t.end()


# ---------------- actions ----------------
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
    """PURE: head_wf / dev_wf = {workflow: {'status','conclusion','failing': [jobs], 'needles1': bool}} -> (rows, verdict)."""
    rows = []; outside = []; pending = []
    for wf, h in sorted(head_wf.items()):
        if h['status'] != 'completed': pending.append(wf); rows.append((wf, 'PENDING', h)); continue
        if h['conclusion'] in ('success', 'skipped', 'neutral'): rows.append((wf, h['conclusion'], h)); continue
        c = CLASS_WF.get(wf)
        if c is None: outside.append(wf); rows.append((wf, 'OUTSIDE the three classes (a NO GO finding)', h)); continue
        hs = set(h['failing'])
        if c == 1:
            ok = hs <= {'Dependency Audit'} and bool(hs) and h.get('needles1', False)
            rows.append((wf, 'class (1) advisory-freeze %s: failing %s SUBSET of {Dependency Audit} %s; the ONLY failed step is the audit-contract step AND its log says `expected exit 0 (clean), got 1`: %s%s' % (
                'HOLDS' if ok else 'DOES NOT HOLD', sorted(hs), hs <= {'Dependency Audit'}, h.get('needles1'),
                ('; history %s' % hist1) if hist1 else ''), h))
            if not ok: outside.append(wf)
        else:
            d = dev_wf.get(wf)
            ds = set(d['failing']) if d else None
            ok = ds is not None and hs <= ds
            better = sorted(ds - hs) if ds is not None else []
            rows.append((wf, 'class (%d) %s: head failing %s SUBSET of develop\'s %s: %s%s' % (
                c, 'HOLDS' if ok else 'DOES NOT HOLD', sorted(hs), sorted(ds) if ds is not None else 'NO COMPARATOR', ok,
                ('; develop fails, head PASSES: %s (named, no cause claimed)' % better) if better else ''), h))
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
                    except Exception as x: lg = ''; e['logs'][j['name']] = {'error': str(x)[:120]}; continue
                    e['logs'][j['name']] = {'bytes': len(lg), 'groups': lg.count('##[group]'), 'fabricated_needle': lg.count('gate73-fabricated-needle-zz'),
                                            'needles1': {n: lg.count(n) for n in NEEDLES_1}}
                    if wf == 'Security Scanning' and j['name'] == 'Dependency Audit':
                        fsteps = [s_['name'] for s_ in j.get('steps', []) if s_.get('conclusion') == 'failure']
                        e['logs'][j['name']]['failed_steps'] = fsteps
                        # the class is proved by BOTH the jobs API's failed step (ONLY the audit-contract step) and its log line, with
                        # the `##[group]` control proving the log arrived
                        e['needles1'] = all(lg.count(n) > 0 for n in NEEDLES_1) and lg.count('##[group]') > 0 and \
                            len(fsteps) == 1 and fsteps[0].startswith(STEP_1)
        out[wf] = e
    return runs, out


def actions(r, head, dev, hist_n=12, wait=False):
    t = Tally()
    fab = 'f' * 40
    try:
        n_fab = len(runs_at(fab))
        prev = None; polls = 0
        while True:
            runs, head_wf = read_head(head)
            sig = json.dumps({k: (v['status'], v['conclusion'], v['failing']) for k, v in head_wf.items()}, sort_keys=True)
            polls += 1
            pend = [k for k, v in head_wf.items() if v['status'] != 'completed']
            if not wait or (sig == prev and not pend) or polls >= 30: break
            prev = sig; time.sleep(60)
        _, dev_wf = read_head(dev, log_needles=False)
        hist = gh_pages('actions/runs?per_page=100', 'workflow_runs')
        ss = [x for x in hist if x['name'] == 'Security Scanning' and x['status'] == 'completed'][:hist_n]
        hist1 = '%d of the last %d completed Security Scanning runs repo-wide FAILED across %d branches' % (
            sum(1 for x in ss if x['conclusion'] == 'failure'), len(ss), len(set(x['head_branch'] for x in ss)))
    except Exception as x:
        print('API FAILURE: %s' % str(x)[:200]); return 3
    t.check('X0', len(runs) > 0 and n_fab == 0, 'runs at the FULL head sha %d | CONTROL a fabricated sha reads %d | polls %d%s' % (len(runs), n_fab, polls, ' (two agreeing)' if wait else ''))
    for wf, e in sorted(head_wf.items()):
        for jn, lg in e['logs'].items():
            t.info('LOG', '%s / %s: %s' % (wf, jn, lg))
    rows, outside, pending = classify(head_wf, dev_wf, hist1)
    for wf, verdict, h in rows: print('   %-34s %s' % (wf, verdict))
    t.check('X1', not outside, 'reds OUTSIDE the three classes (or a class that does not hold): %s' % (outside or 'none'))
    t.check('X2', not pending, 'PENDING (never a pass): %s' % (pending or 'none'))
    t.info('X3', 'develop %s comparator: %s' % (dev[:12], {k: (v['conclusion'], v['failing']) for k, v in sorted(dev_wf.items())}))
    return t.end()


def census(r):
    t = Tally()
    try:
        prs = gh_pages('pulls?state=open', 'pulls')
    except Exception as x: print('API FAILURE: %s' % str(x)[:200]); return 3
    batch = set(ROWS); allcode = {p: k for k, R in ROWS.items() for p in code_paths(R)}; docs = {K['docs']['flow'], K['docs']['cheat']}
    keys = {R['ticket'] for R in ROWS.values()}; found = 0
    for p in prs:
        n = str(p['number'])
        if n in batch: continue
        fs = [f['filename'] for f in gh_pages('pulls/%s/files' % n, 'files')]
        ov = sorted(set(fs) & set(allcode)); dd = sorted(set(fs) & docs); kk = [k for k in keys if k in (p['title'] or '')]
        if ov or dd or kk:
            found += 1
            print('   #%s %-60s OVERLAP %s DOCS %s TITLE-KEYS %s' % (n, (p['title'] or '')[:60], ov, [os.path.basename(x) for x in dd], kk))
    t.check('C0', len(prs) >= len(batch), 'open PRs read %d (CONTROL: >= the %d batch PRs themselves)' % (len(prs), len(batch)))
    t.info('C1', '%d other open PR(s) collide (REPORT only; a DOCS collision forces a keep-both merge-in on whichever lands later)' % found)
    return t.end()


# ---------------- self-test (fixtures, no network) ----------------
def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    dev = {'PR Security Gates (KS-168)': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Code Security Gates']},
           'pr': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Akto suite (PR)', 'Performance suite (k6 smoke)', 'Playwright suite', 'Schemathesis suite']}}
    good = {'Security Scanning': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Dependency Audit'], 'needles1': True},
            'PR Security Gates (KS-168)': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Code Security Gates']},
            'pr': {'status': 'completed', 'conclusion': 'failure', 'failing': ['Akto suite (PR)', 'Performance suite (k6 smoke)', 'Playwright suite']},
            'pr-premerge-ack': {'status': 'completed', 'conclusion': 'success', 'failing': []}}
    rows, o, p = classify(good, dev); rep(not o and not p, '#1407-shaped head (pr a STRICT subset of develop): no OUTSIDE, no PENDING')
    rep(any('Schemathesis suite' in v for _, v, _ in rows), 'the job develop fails and the head passes (Schemathesis) is NAMED')
    eq = lambda hs, ds: hs == ds
    rep(not eq(set(good['pr']['failing']), set(dev['pr']['failing'])), 'PLANTED equality predicate would print a FALSE STOP on the same data (why SUBSET is the rule)')
    bad = json.loads(json.dumps(good)); bad['pr']['failing'].append('Unit tests')
    rows, o, p = classify(bad, dev); rep(o == ['pr'], 'PLANTED a red develop lacks (`Unit tests` in pr): OUTSIDE %s' % o)
    bad2 = json.loads(json.dumps(good)); bad2['CodeQL'] = {'status': 'completed', 'conclusion': 'failure', 'failing': ['analyze']}
    rows, o, p = classify(bad2, dev); rep('CodeQL' in o, 'PLANTED a failing workflow outside the three classes: OUTSIDE %s' % o)
    bad3 = json.loads(json.dumps(good)); bad3['Security Scanning']['failing'] = ['Dependency Audit', 'SAST Analysis']
    rows, o, p = classify(bad3, dev); rep('Security Scanning' in o, 'PLANTED class (1) with an extra failing job (SAST): DOES NOT HOLD')
    bad4 = json.loads(json.dumps(good)); bad4['Security Scanning']['needles1'] = False
    rows, o, p = classify(bad4, dev); rep('Security Scanning' in o, 'PLANTED class (1) whose log lacks the audit-contract needles (an unread / different failure): DOES NOT HOLD')
    pen = json.loads(json.dumps(good)); pen['pr'] = {'status': 'in_progress', 'conclusion': None, 'failing': []}
    rows, o, p = classify(pen, dev); rep(p == ['pr'], 'PLANTED pr in_progress: PENDING %s (never a pass)' % p)
    rows, o, p = classify(good, {}); rep(set(o) == {'pr', 'PR Security Gates (KS-168)'}, 'PLANTED no develop comparator: classes 2/3 DO NOT HOLD (%s)' % o)
    R = ROWS['1407']; body = 'Refs KS-998\nhttps://linear.app/secuura/issue/KS-998\nKS 1136 de-hyphenated. UNMEASURED: Schemathesis, Akto, Playwright, Performance. NO live sweep owed.\n'
    t, _ = text_checks('1407', R['subject'], body); rep(not t.fails, 'prtext GREEN on a well-formed #1407 body: fails %s' % t.fails)
    t, _ = text_checks('1407', R['subject'], body + 'Fixes KS-998\n'); rep('T2' in t.fails, 'PLANTED `Fixes KS-998`: T2 FAILS')
    t, _ = text_checks('1407', R['subject'], body + 'see KS-1136\n'); rep('T3' in t.fails, 'PLANTED a hyphenated foreign key KS-1136: T3 FAILS')
    t, _ = text_checks('1407', R['subject'] + ' (#1407)', body); rep('T4' in t.fails, 'PLANTED `(#1407)` in the title: T4 FAILS')
    t, _ = text_checks('1408', ROWS['1408']['subject'], body.replace('998', '1435').replace('NO live sweep owed.', 'Runtime change.')); rep('T6' in t.fails, 'PLANTED #1408 body without the live-sweep-OWED sentence: T6 FAILS')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    mode = A[0] if A else ''
    if mode == 'api': return api(row_arg(), opt(A, '--head'))
    if mode == 'prtext': return prtext(row_arg(), opt(A, '--head'))
    if mode == 'actions':
        h, d = opt(A, '--at'), opt(A, '--develop')
        if not (h and d and re.fullmatch(r'[0-9a-f]{40}', h) and re.fullmatch(r'[0-9a-f]{40}', d)): print('REFUSED: --at and --develop must be FULL 40-hex'); return 2
        return actions(row_arg(), h, d, int(opt(A, '--history', '12')), '--wait' in A)
    if mode == 'census': return census(row_arg(required=False) or '1407')
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
