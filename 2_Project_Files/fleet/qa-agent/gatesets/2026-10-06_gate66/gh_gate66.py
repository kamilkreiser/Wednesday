#!/usr/bin/env python3
"""gh_gate66.py — GitHub READ-ONLY instruments for gate66 (#1385). REST GETs only; GH_TOKEN read BY NAME, never printed.

  api       one line `API #1385 head <sha> branch <ref> base <ref> state <s> merged <bool> mergeable <m> mergeable_state <ms>` + the body
            sha256/16 + chars (claim 64d208b5da2c4bfa / 7613). mergeable_state is RE-POLLED (up to 3 reads, 5 s apart, while null).
  actions   E 5th's method: the workflow runs at the head vs the runs at the PR's PREVIOUS head 79c87b8aaa48 (the comparable trigger —
            never develop's tip). Per workflow name: conclusion at prev and at head. NEW-FAILING = failing at head and NOT failing at
            prev. PENDING = not completed at head (named; never a pass). PLANTED-NAME CONTROL: the same predicate re-run with a fabricated
            failing workflow added at the head MUST report it, else the NONE is a blind spot (rc 1). `pr` is printed on its own line.
  census    every OPEN PR's files: OVERLAP (touches a kit code path or is titled KS-938) / DOCS (touches a platform-k doc) / other.
            CONTROL: a fabricated PR row carrying users.ts must classify OVERLAP.
  prtext    the live PR title + body: T1 one `Refs KS-938` + the ticket URL · T2 0 closing references (Linear + GitHub) · T3 only KS-938
            hyphenated · T4 title == the PR's commit subject · T5 0 Co-Authored-By.
  --selftest  the actions predicate + census classifier on synthetic rows (no network).
rc 0 / 1 (a finding: NEW-FAILING, PENDING, blind control, OVERLAP) / 3 API failure."""
import hashlib, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate66 import K, gh_get, gh_pages

FAILING = ('failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required')


def runs_by_name(runs):
    """latest run per workflow name -> (status, conclusion)."""
    out = {}
    for r in sorted(runs, key=lambda r: r.get('created_at', '')):
        out[r['name']] = (r.get('status'), r.get('conclusion'))
    return out


def compare(prev, head):
    failing = lambda d, n: d.get(n, (None, None))[1] in FAILING
    new = sorted(n for n in head if failing(head, n) and not failing(prev, n))
    pending = sorted(n for n in head if head[n][0] != 'completed')
    gone = sorted(n for n in prev if n not in head)
    return new, pending, gone


def classify(pr_row, files):
    code = set(K['code_paths']); docs = {K['flow'], K['cheat']}
    if 'KS-938' in (pr_row.get('title') or '') or set(files) & code: return 'OVERLAP'
    if set(files) & docs: return 'DOCS'
    return 'other'


def api():
    pr = None
    for i in range(3):
        pr = gh_get('pulls/%s' % K['pr'])
        if pr.get('mergeable') is not None: break
        time.sleep(5)
    b = (pr.get('body') or '')
    print('API #%s head %s branch %s base %s state %s merged %s mergeable %s mergeable_state %s' % (
        K['pr'], pr['head']['sha'], pr['head']['ref'], pr['base']['ref'], pr['state'], pr['merged'], pr.get('mergeable'), pr.get('mergeable_state')))
    print('BODY sha256/16 %s chars %d bytes %d (claim %s / %d) | title == kit %s | updated %s' % (
        hashlib.sha256(b.encode()).hexdigest()[:16], len(b), len(b.encode()), K['claims']['body_sha256_16'], K['claims']['body_chars'], pr['title'] == K['pr_title'], pr['updated_at']))
    return 0 if pr['head']['sha'] == K['head'] and pr['state'] == 'open' and not pr['merged'] else 1


def actions():
    def get(sha):
        # gh_actions_ex1 (drafter, 2026-10-06): the head's run list came back EMPTY once and 6 runs on the next read — an empty list
        # is an instrument read, never "nothing failing": re-poll up to 3 times, 10 s apart, and say so.
        for i in range(3):
            r = gh_get('actions/runs?head_sha=%s&per_page=100' % sha)
            print('READ runs at %s: total_count %s (attempt %d)' % (sha[:12], r.get('total_count'), i + 1))
            if r.get('workflow_runs'): return runs_by_name(r['workflow_runs'])
            time.sleep(10)
        return {}
    prev, head = get(K['prev_head']), get(K['head'])
    if not head or not prev:
        print('ACTIONS NOT READ: an empty run list after 3 reads (prev %d, head %d) — NOT RUN is never a pass' % (len(prev), len(head))); return 1
    for n in sorted(set(prev) | set(head)):
        print('RUN %-34s prev %-24s head %s' % (n, '/'.join(str(x) for x in prev.get(n, ('-', '-'))), '/'.join(str(x) for x in head.get(n, ('-', '-')))))
    new, pending, gone = compare(prev, head)
    planted = dict(head); planted['ZZ planted control workflow'] = ('completed', 'failure')
    cnew, _, _ = compare(prev, planted)
    blind = 'ZZ planted control workflow' not in cnew
    print('PR-WORKFLOW `pr` prev %s head %s' % (prev.get('pr'), head.get('pr')))
    print('FAILING at prev %s' % sorted(n for n in prev if prev[n][1] in FAILING))
    print('FAILING at head %s' % sorted(n for n in head if head[n][1] in FAILING))
    print('NEW-FAILING at head: %s | PENDING at head: %s | workflows at prev missing at head: %s | PLANTED-NAME CONTROL reported: %s' % (new or 'NONE', pending or 'NONE', gone or 'NONE', not blind))
    return 1 if (new or pending or blind or gone) else 0


def census():
    prs = gh_pages('pulls?state=open')
    rows = []
    for p in prs:
        if str(p['number']) == K['pr']: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % p['number'])]
        rows.append((p['number'], p['head']['sha'][:12], classify(p, files), (p['title'] or '')[:70]))
    ctl = classify({'title': 'SIM'}, [K['users_file']])
    for r in sorted(rows):
        if r[2] != 'other': print('CENSUS #%d %s %s %s' % r)
    ov = [r for r in rows if r[2] == 'OVERLAP']
    print('CENSUS %d other open PR(s): OVERLAP %d, DOCS %d | CONTROL (users.ts row) -> %s' % (len(rows), len(ov), sum(r[2] == 'DOCS' for r in rows), ctl))
    return 1 if ov or ctl != 'OVERLAP' else 0


KEY_RX = __import__('re').compile(r'\bKS-\d+\b')
CLOSE_RX = __import__('re').compile(r'\b(close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?|completing)\b[^.\n]{0,60}?\bKS-\d+', 2)
GHCLOSE_RX = __import__('re').compile(r'\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\d+', 2)


def judge_text(title, body):
    import re
    refs = re.findall(r'(?m)^Refs KS-938\s*$', body); keys = sorted(set(KEY_RX.findall(title + '\n' + body)))
    cl = CLOSE_RX.findall(title + '\n' + body) + GHCLOSE_RX.findall(title + '\n' + body)
    co = re.findall(r'(?im)^co-authored-by:', body)
    rows = [('T1', len(refs) == 1 and K['ticket_url'] in body, '`Refs KS-938` lines %d (want 1); ticket URL present %s' % (len(refs), K['ticket_url'] in body)),
            ('T2', not cl, 'closing references (Linear + GitHub) in title+body: %s' % (cl or 'none')),
            ('T3', keys == ['KS-938'], 'hyphenated keys %s (want only KS-938)' % keys),
            ('T4', title == K['pr_title'], 'title == the PR commit subject: %s' % (title == K['pr_title'])),
            ('T5', not co, 'Co-Authored-By lines %d' % len(co))]
    return rows


def prtext():
    pr = gh_get('pulls/%s' % K['pr']); rows = judge_text(pr['title'], pr.get('body') or '')
    bad = 0
    for cid, ok, msg in rows:
        print('%s %s %s' % ('PASS' if ok else 'FAIL', cid, msg)); bad += not ok
    print('CHECKED %d' % len(rows)); print('%d FAIL' % bad); return 1 if bad else 0


def selftest():
    ok = total = 0
    def rep(c, m):
        nonlocal ok, total
        total += 1; ok += bool(c); print('SELFTEST %s %s' % ('OK' if c else 'MISS', m))
    prev = {'pr': ('completed', 'failure'), 'Security Scanning': ('completed', 'failure'), 'ack': ('completed', 'success')}
    rep(compare(prev, dict(prev)) == ([], [], []), 'identical -> NONE')
    h = dict(prev); h['ack'] = ('completed', 'failure'); rep(compare(prev, h)[0] == ['ack'], 'success -> failure is NEW')
    h = dict(prev); h['pr'] = ('in_progress', None); rep(compare(prev, h)[1] == ['pr'], 'in_progress is PENDING, never a pass')
    h = dict(prev); h['new wf'] = ('completed', 'failure'); rep(compare(prev, h)[0] == ['new wf'], 'a workflow absent at prev and failing at head is NEW')
    h = dict(prev); del h['Security Scanning']; rep(compare(prev, h)[2] == ['Security Scanning'], 'a workflow that did not run at head is NAMED, not read as green')
    rep(classify({'title': 'x'}, [K['mfa_file']]) == 'OVERLAP', 'mfa.ts row -> OVERLAP')
    rep(classify({'title': 'x'}, [K['cheat']]) == 'DOCS', 'cheat row -> DOCS')
    rep(classify({'title': 'KS-938 follow-up'}, []) == 'OVERLAP', 'KS-938 title -> OVERLAP')
    rep(classify({'title': 'x'}, ['README.md']) == 'other', 'unrelated -> other')
    body = 'x\n\nRefs KS-938\n\n%s\n' % K['ticket_url']; T = K['pr_title']
    rep(all(r[1] for r in judge_text(T, body)), 'prtext positive (synthetic body) -> all PASS')
    rep(not judge_text(T, body + 'This fixes KS-938.\n')[1][1], 'a closing word before KS-938 -> T2 FAIL')
    rep(not judge_text(T, body + 'see KS-1419\n')[2][1], 'another hyphenated key -> T3 FAIL')
    rep(not judge_text(T, body + 'Refs KS-938\n')[0][1], 'two Refs lines -> T1 FAIL')
    rep(not judge_text(T, body + 'Co-Authored-By: X <x@y>\n')[4][1], 'a Co-Authored-By line -> T5 FAIL')
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A: print(__doc__); raise SystemExit(0)
    if '--selftest' in A: raise SystemExit(selftest())
    try:
        raise SystemExit({'api': api, 'actions': actions, 'census': census, 'prtext': prtext}[A[0]]())
    except SystemExit:
        raise
    except Exception as e:
        print('API FAILURE: %s' % str(e)[:200]); raise SystemExit(3)
