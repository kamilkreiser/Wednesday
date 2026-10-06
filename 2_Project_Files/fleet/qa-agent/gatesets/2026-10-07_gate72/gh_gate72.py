#!/usr/bin/env python3
"""gh_gate72.py — GitHub / Linear READ-ONLY instruments for gate72 (#1406, KS-1437). REST GETs + Linear GraphQL reads; tokens BY NAME,
never printed. Carried from gh_gate70.py; [g72] marks changes. EVERY PIN IS A REQUIRED ARGUMENT.

  api       --head H [--body-out F]   `API #1406 head <sha> branch <ref> base <ref> state <s> merged <b> mergeable <m> mergeable_state <ms>`,
            body sha256/16, chars AND utf-8 bytes (the READY says "11,393 B"); rc 1 unless head == H, open, unmerged, base develop.
  actions   --at H --develop D --compare-head C [--out DIR]     [g72, Wednesday 2026-10-07: RE-VERIFY the builder's "pre-existing by log"]
            A1 runs at H by workflow name (status / conclusion); a PLANTED-NAME control must classify NEW-FAILING (else the NONE is blind)
            A2 for EVERY failing run at H: its jobs, the failing job + step names, and the job LOG fetched by this tool (the 302 to the
               signed URL is followed WITHOUT the Authorization header — STANDING_LINES, Seat E 8th: an unfetched log reads as zero).
               Per log: bytes, POSITIVE control `##[group]` count (> 0 or the log is UNREAD -> NOT RUN), the KS-788 / exit-code needles,
               the CHANGE needles (shell-quote, @modelcontextprotocol/sdk, pbkdf2, GHSA-pqg4/6qxp/477h), a FABRICATED needle (must be 0)
            A3 the SAME workflow at develop D (its push runs) and at C (#1397's head 3e7be2044fe8, the merged lock refresh): same failing
               job + step, same needles — read by this tool, never copied from the builder's mail
            A4 history: the last 12 runs of each red workflow (any branch): conclusions counted (builder: 12/12 and 10/10 FAILURE)
            CLASSIFY per red workflow: PRE-EXISTING only if (log read at H, positive control > 0) AND (the same failing step + a pre-existing
            needle at D or C, read here) AND (0 change needles in the failing step's log at H). Anything else: UNCLASSIFIED (the gate rules it
            BLOCKING, per gate70's Q1 rule). NOTE: CI's `Dependency Audit` job is NOT legs 6 / 7: it runs the audit gates' own VALIDATOR
            suite in a CI checkout; the in-hook legs 6/7 audit the advisories. A green leg 6/7 and a red CI step are different instruments.
  census    every OTHER open PR touching any of the 5 paths or titled KS-1437 = OVERLAP; CONTROL: a fabricated row on a lock classifies OVERLAP.
  prtext    --head H --measured c2.json --reach c6.json [--repo CLONE --base B] [--body-file F (offline: the drafter's saved body)]
            T1 exactly one `Refs KS-1437` line; T1b no closing-family word on it or the 3 lines above   T2 0 closing words before a key / #n
            T3 only KS-1437 hyphenated (title + body) — a hyphenated foreign key ATTACHES (STANDING_LINES :278)   T4 title == the commit
            subject; squash <= 92   T5 0 trailer lines   T6 the body's change-set numbers vs MEASURED (c2 / c6 / numstat)
            T7 every sentence carrying a digit, a version or an id is written to --sentences-out for the gate's sentence-by-sentence ruling
  linear    KS-1437: state In Progress / Backlog, not archived; its COMMENTS (bodies saved to --comments-out, sha256/16 each) for the
            gate's sentence-by-sentence read; KS-562 title + state (the pre-existing failure's ticket). Read-only.
  --selftest  the actions predicates, the classifier, the redirect-without-auth opener, the key / closing scanners, the claims comparator.
rc 0 / 1 (finding, blind control, OVERLAP, UNCLASSIFIED, NOT RUN) / 2 refused / 3 API failure."""
import hashlib, json, os, re, subprocess, sys, time, urllib.error, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate72 import K, gh_get, gh_pages, linear, env_value, req, opt

P = K['pr']; KEY = P['ticket']; AC = K['actions']
FAILING = ('failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required')
CLOSING = re.compile(K['closing_rx'], re.I)
CLOSING_WORD = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\b', re.I)
PATHS = set(P['numstat'])


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


def fetch_log(job_id):
    """job log text. The API answers 302 to a signed URL; that URL is fetched WITHOUT the Authorization header."""
    op = urllib.request.build_opener(_NoRedirect)
    r = urllib.request.Request('https://api.github.com/repos/%s/actions/jobs/%d/logs' % (K['gh_repo'], job_id),
                               headers={'Authorization': 'Bearer ' + env_value('GH_TOKEN'), 'Accept': 'application/vnd.github+json'})
    try:
        resp = op.open(r, timeout=60); return resp.read().decode('utf-8', 'replace')     # a direct 200 (rare)
    except urllib.error.HTTPError as e:
        if e.code not in (301, 302, 303, 307, 308): raise
        loc = e.headers.get('Location')
    return urllib.request.urlopen(urllib.request.Request(loc), timeout=120).read().decode('utf-8', 'replace')


SIG = re.compile(r'(##\[error\]|\b[1-9]\d* failed\b|\u2716|AssertionError|^not ok \d)')
TS = re.compile(r'^\d{4}-\d\d-\d\dT[\d:.]+Z\s?')
DUR = re.compile(r'\s*\(\d+(?:\.\d+)?m?s\)$')   # a test's duration, which differs run to run


def signature(text):
    """[g72] the FAILURE SIGNATURE of a log: every line (timestamp stripped) carrying an error marker, a non-zero `N failed`, a \u2716,
    an AssertionError or a TAP `not ok`. A red is PRE-EXISTING only if the head's signature is a SUBSET of a comparator's."""
    norm = lambda l: DUR.sub('', TS.sub('', l).strip())
    return sorted(set(norm(l) for l in text.split('\n') if SIG.search(norm(l))))


def needles(text):
    return {'signature': signature(text), 'bytes': len(text.encode()), 'positive_group': text.count(AC['positive_control']),
            'preexisting': dict((n, text.count(n)) for n in AC['needles_preexisting']),
            'change': dict((n, text.count(n)) for n in AC['needles_change']), 'fabricated': text.count(AC['fabricated_control'])}


def runs_at(sha):
    r = gh_get('actions/runs?head_sha=%s&per_page=100' % sha); return r['workflow_runs']


def latest_by_name(runs):
    out = {}
    for r in sorted(runs, key=lambda r: r.get('created_at', '')): out[r['name']] = r
    return out


def compare(prev, head, expected):
    failing = lambda d, n: (d.get(n) or {}).get('conclusion') in FAILING
    new = sorted(n for n in head if failing(head, n) and not failing(prev, n))
    pending = sorted(n for n in head if (head[n] or {}).get('status') != 'completed')
    notrun = sorted(n for n in set(expected) if n not in head)
    return new, pending, notrun


def failing_jobs(run, out_dir, tag):
    """[(job name, [failing step names], needles of its log)]"""
    res = []
    for j in gh_get('actions/runs/%d/jobs?per_page=100' % run['id'])['jobs']:
        if j.get('conclusion') not in FAILING: continue
        steps = [s['name'] for s in j.get('steps') or [] if s.get('conclusion') in FAILING]
        try: text = fetch_log(j['id'])
        except (urllib.error.URLError, OSError) as e: text = ''; print('  LOG FETCH FAILED job %s: %s' % (j['id'], e))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            fn = os.path.join(out_dir, '%s_%s_%d.log' % (tag, re.sub(r'\W+', '_', run['name'])[:30], j['id'])); open(fn, 'w').write(text)
        n = needles(text); res.append((j['name'], steps, n))
        print('  JOB %-28s failing steps %s | log %d B, ##[group] %d, failure-signature lines %d, kit needles %s, change needles %s, fabricated %d' % (
            j['name'], steps, n['bytes'], n['positive_group'], len(n['signature']), n['preexisting'], dict((k, v) for k, v in n['change'].items() if v) or 0, n['fabricated']))
        for x in n['signature'][:12]: print('      SIG %s' % x[:200])
    return res


def classify_red(head_jobs, comp_jobs):
    """PRE-EXISTING / UNCLASSIFIED + why. comp_jobs: {label: [(job, steps, needles)]} read at develop / #1397 by THIS tool."""
    why = []
    if not head_jobs: return 'UNCLASSIFIED', ['no failing job read at the head']
    for job, steps, n in head_jobs:
        if n['positive_group'] == 0: why.append('%s: log UNREAD (##[group] 0)' % job)
        if any(n['change'].values()): why.append('%s: change needles present %s' % (job, dict((k, v) for k, v in n['change'].items() if v)))
        sig = set(n['signature'])
        match = [lab for lab, js in comp_jobs.items() for (cj, cs, cn) in js
                 if cj == job and set(cs) == set(steps) and cn['positive_group'] > 0 and sig and sig <= set(cn['signature'])]
        if not match: why.append('%s: no comparator (develop / #1397) shows the same job + step with a failure signature covering the head\'s %d lines' % (job, len(sig)))
    return ('PRE-EXISTING' if not why else 'UNCLASSIFIED'), why


def actions(at, develop, comp_head, out_dir):
    h = latest_by_name(runs_at(at)); d = latest_by_name(runs_at(develop)); c = latest_by_name(runs_at(comp_head))
    print('READ runs: at %s %d workflows | develop %s %d | #1397 head %s %d' % (at[:12], len(h), develop[:12], len(d), comp_head[:12], len(c)))
    for n in sorted(set(h) | set(d) | set(c)):
        f = lambda x: '%s/%s' % ((x.get(n) or {}).get('status', 'ABSENT'), (x.get(n) or {}).get('conclusion', '-'))
        print('RUN %-40s head %-22s develop %-22s #1397 %s' % (n, f(h), f(d), f(c)))
    new, pending, _ = compare(d, h, [])
    hp = dict(h); hp['__planted_failing__'] = {'status': 'completed', 'conclusion': 'failure'}
    ctl = '__planted_failing__' in compare(d, hp, [])[0]
    print('NEW-FAILING vs develop %s | PENDING %s | PLANTED-NAME CONTROL reported: %s' % (new or 'NONE', pending or 'NONE', ctl))
    reds = sorted(n for n, r in h.items() if r.get('conclusion') in FAILING)
    verdicts = {}
    for n in reds:
        print('RED %s (run %d)' % (n, h[n]['id'])); hj = failing_jobs(h[n], out_dir, 'head')
        comp = {}
        for lab, src in (('develop', d), ('pr1397', c)):
            if n in src and src[n].get('conclusion') in FAILING:
                print(' COMPARATOR %s run %d' % (lab, src[n]['id'])); comp[lab] = failing_jobs(src[n], out_dir, lab)
            else: print(' COMPARATOR %s: %s' % (lab, (src.get(n) or {}).get('conclusion', 'ABSENT')))
        wf = h[n]['workflow_id']; hist = gh_get('actions/workflows/%d/runs?per_page=12' % wf)['workflow_runs']
        cnt = {}
        for r in hist: cnt[r.get('conclusion')] = cnt.get(r.get('conclusion'), 0) + 1
        print(' HISTORY last %d runs of %s: %s | on develop: %s' % (len(hist), n, cnt, sorted(set(r['head_sha'][:12] for r in hist if r.get('head_branch') == 'develop'))))
        v, why = classify_red(hj, comp); verdicts[n] = v
        print(' CLASSIFY %s: %s %s' % (n, v, why or ''))
    print('NOTE: CI `Dependency Audit` runs the audit gates\' own VALIDATOR suite in a CI checkout — a different instrument from the in-hook legs 6 / 7.')
    ok = ctl and not pending and all(v == 'PRE-EXISTING' for v in verdicts.values())
    return 0 if ok else 1


def classify_pr(pr_row, files):
    if KEY in (pr_row.get('title') or '') or set(files) & PATHS: return 'OVERLAP'
    if any(f.endswith('package-lock.json') for f in files): return 'LOCKS'
    return 'other'


def census():
    prs = gh_pages('pulls?state=open'); rows, cnt = [], {}
    for pr in prs:
        if str(pr['number']) == P['pr']: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % pr['number'])]
        c = classify_pr(pr, files); cnt[c] = cnt.get(c, 0) + 1
        if c != 'other': rows.append('  %s #%d %s %s %s' % (c, pr['number'], pr['head']['sha'][:12], pr['title'][:70], sorted(set(files) & PATHS)))
    ctl = classify_pr({'title': 'x'}, [sorted(PATHS)[0]]) == 'OVERLAP' and classify_pr({'title': 'y'}, ['a.ts']) == 'other'
    print('CENSUS %d other open PR(s): %s | CONTROL fires %s' % (sum(cnt.values()), cnt, ctl))
    for r in rows: print(r)
    return 3 if not ctl else (1 if cnt.get('OVERLAP') else 0)


def scan(text): return sorted(set(re.findall(r'\bKS-\d+\b', text))), CLOSING.findall(text)


def refs_window(body):
    lines = body.split('\n'); hits = [i for i, l in enumerate(lines) if re.match(r'^\s*`?Refs %s\b' % re.escape(KEY), l)]
    bad = [i for i in hits for j in range(max(0, i - 3), i + 1) if CLOSING_WORD.search(lines[j])]
    return hits, bad


def claims(body, m, r, ns):
    out = []
    def one(cid, rx, want):
        hits = [tuple(int(x.replace(',', '')) for x in g.groups()) for g in re.finditer(rx, body)]
        out.append((cid, hits or None, want, (not hits) or all(h == want for h in hits)))
    one('CL-SET', r'(\d+) locks, (\d+) entries, \*\*(\d+) field writes', (m['locks'], m['entries'], m['field_writes']))
    one('CL-SHORTSTAT', r'(\d+) files changed, (\d+) insertions\(\+\), (\d+) deletions', (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values())))
    one('CL-COPYLINES', r'Of (\d+) COPY lines naming `package\*\.json` across (\d+) Dockerfiles', (r['package_copy_lines'], r['dockerfiles_a']))
    one('CL-PBKDF2-IMAGES', r'pbkdf2 reaches (\d+) runtime images', (len(r['ships']['pbkdf2']),))
    one('CL-SHARED-BUILDER', r'(\d+) Dockerfiles copy `--from=shared-builder /shared`', (len(r['ships']['pbkdf2']),))
    return out


def sentences(body):
    s = re.split(r'(?<=[.;:!?])\s+|\n+', body)
    return [x.strip() for x in s if x.strip() and re.search(r'\d|GHSA|KS-|`', x)]


def prtext(head, measured, reach, repo, base, body_file, sent_out):
    if body_file:
        body = open(body_file, encoding='utf-8').read(); title = P['subject']; print('OFFLINE body from %s (title assumed == kit subject)' % body_file)
    else:
        pr = gh_get('pulls/%s' % P['pr']); body = pr.get('body') or ''; title = pr['title']
        if pr['head']['sha'] != head: print('REFUSED: API head %s != --head %s' % (pr['head']['sha'], head)); return 1
    keys, closing = scan(body + '\n' + title); hits, bad = refs_window(body)
    co = len(re.findall(r'(?im)^\s*(co-authored-by|signed-off-by):', body)); lt = len(title) + len(' (#%s)' % P['pr'])
    print('BODY sha256/16 %s, %d chars, %d utf8-bytes' % (hashlib.sha256(body.encode()).hexdigest()[:16], len(body), len(body.encode())))
    print('T1 `Refs %s` lines: %d at line(s) %s (want exactly 1) | T1b closing words on it or the 3 lines above: %s' % (KEY, len(hits), [i + 1 for i in hits], bad or 'none'))
    print('T2 closing references before a key / #n (title + body): %s (want none)' % (closing or 'none'))
    print('T3 hyphenated keys (title + body): %s -> only %s: %s' % (keys, KEY, keys == [KEY]))
    print('T4 title %r (%d chars, squash %d <= %d %s) == kit subject %s' % (title, len(title), lt, P['squash_max'], lt <= P['squash_max'], title == P['subject']))
    print('T5 trailer-shaped lines in the body: %d' % co)
    ok = len(hits) == 1 and not bad and not closing and keys == [KEY] and lt <= P['squash_max'] and title == P['subject'] and co == 0
    m = json.load(open(measured)); r = json.load(open(reach)); ns = {}
    if repo and base:
        for l in subprocess.run(['git', '-C', repo, 'diff', '--numstat', base, head], capture_output=True, text=True).stdout.strip().split('\n'):
            a, dl, p = l.split('\t'); ns[p] = (int(a), int(dl))
    else: ns = dict((p, tuple(v)) for p, v in P['numstat'].items())
    for cid, stated, want, good in claims(body, m, r, ns):
        print('T6 %-18s %s stated %s measured %s' % (cid, 'OK      ' if good and stated else ('ABSENT  ' if not stated else 'MISMATCH'), stated, want))
        ok &= good
    ss = sentences(body)
    if sent_out: open(sent_out, 'w').write('\n'.join('%3d  %s' % (i + 1, x) for i, x in enumerate(ss)) + '\n')
    print('T7 %d factual-looking sentences written to %s for the sentence-by-sentence ruling' % (len(ss), sent_out or '(not written: give --sentences-out)'))
    return 0 if ok else 1


def linear_read(comments_out):
    q = 'query($id:String!){issue(id:$id){identifier title state{name type} updatedAt archivedAt comments{nodes{id createdAt body}}}}'
    rr = linear(q, {'id': KEY}); i = (rr.get('data') or {}).get('issue')
    if not i: print('LINEAR %s not returned: %s' % (KEY, rr.get('errors'))); return 1
    cs = i['comments']['nodes']
    print('LINEAR %s state %s (%s) updatedAt %s archivedAt %s comments %d' % (i['identifier'], i['state']['name'], i['state']['type'], i['updatedAt'], i['archivedAt'], len(cs)))
    for c in cs: print('  COMMENT %s %s %d B sha256/16 %s' % (c['id'][:8], c['createdAt'], len(c['body'].encode()), hashlib.sha256(c['body'].encode()).hexdigest()[:16]))
    if comments_out: open(comments_out, 'w').write('\n\n=====\n\n'.join('%s %s\n%s' % (c['id'], c['createdAt'], c['body']) for c in cs))
    r2 = linear('query($id:String!){issue(id:$id){identifier title state{name}}}', {'id': K['known_failure']['ticket']})
    j = (r2.get('data') or {}).get('issue') or {}
    print('LINEAR %s %r state %s (the known failure\'s ticket)' % (j.get('identifier'), j.get('title'), (j.get('state') or {}).get('name')))
    return 0 if i['state']['name'] in K['linear_ok_states'] and not i['archivedAt'] else 1


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    S_ = lambda c: {'status': 'completed', 'conclusion': c}
    rep(compare({'pr': S_('failure'), 'S': S_('success')}, {'pr': S_('failure'), 'S': S_('failure')}, [])[0] == ['S'], 'actions: success->failure is NEW-FAILING, failure->failure is not')
    rep(compare({}, {'X': S_('failure')}, [])[0] == ['X'], 'actions: ABSENT at develop and failing at the head is NEW-FAILING (read its log)')
    rep(compare({}, {'pr': {'status': 'in_progress', 'conclusion': None}}, [])[1] == ['pr'], 'actions: in_progress is PENDING')
    pre = AC['needles_preexisting'][1]
    nh = needles('##[group]x\nAssertionError: %s\n' % pre); nd = needles('##[group]y\nAssertionError: %s\n' % pre)
    rep(classify_red([('Dependency Audit', ['s'], nh)], {'develop': [('Dependency Audit', ['s'], nd)]})[0] == 'PRE-EXISTING', 'classify: same job + step + needle at develop -> PRE-EXISTING')
    rep(classify_red([('Dependency Audit', ['s'], needles('AssertionError: ' + pre))], {'develop': [('Dependency Audit', ['s'], nd)]})[0] == 'UNCLASSIFIED', 'PLANTED unread head log (##[group] 0) -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', ['s'], needles('##[group]\nAssertionError: %s\npbkdf2' % pre))], {'develop': [('Dependency Audit', ['s'], nd)]})[0] == 'UNCLASSIFIED', 'PLANTED change needle (pbkdf2) in the failing log -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', ['s'], nh)], {'develop': [('Dependency Audit', ['other step'], nd)]})[0] == 'UNCLASSIFIED', 'PLANTED different failing step at develop -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', ['s'], nh)], {})[0] == 'UNCLASSIFIED', 'PLANTED no comparator read -> UNCLASSIFIED (never assumed pre-existing)')
    rep(classify_red([('Dependency Audit', ['s'], needles('##[group]\nAssertionError: %s\nrun_x: 3 passed, 2 failed' % pre))], {'develop': [('Dependency Audit', ['s'], nd)]})[0] == 'UNCLASSIFIED',
        'PLANTED an EXTRA failure line at the head (not in the comparator) -> UNCLASSIFIED')
    rep(signature('2026-10-06T20:00:00.1Z run_shell_suites: 57 passed, 4 failed\nok 0 failed\n') == ['run_shell_suites: 57 passed, 4 failed'], 'signature strips timestamps; `0 failed` is not a failure')
    rep(signature('\u2716 audit-locks: x (32.5ms)') == signature('\u2716 audit-locks: x (35.07ms)'), 'signature strips per-test durations (they differ run to run)')
    rep(needles('##[group]')['fabricated'] == 0 and needles(AC['fabricated_control'])['fabricated'] == 1, 'fabricated needle counts 0 unless planted')
    rep(isinstance(_NoRedirect().redirect_request(None, None, 302, '', {}, 'u'), type(None)), 'the log opener does NOT follow the 302 with the auth header (it re-requests the Location bare)')
    rep(classify_pr({'title': 'KS-1437 x'}, []) == 'OVERLAP' and classify_pr({'title': 'x'}, [sorted(PATHS)[0]]) == 'OVERLAP' and classify_pr({'title': 'x'}, ['q/package-lock.json']) == 'LOCKS', 'census classifier')
    k, c = scan('Refs KS-1437. Gate owners KS 470, KS 531.'); rep(k == ['KS-1437'] and not c, 'scan: de-hyphenated keys are not keys')
    k, c = scan('Preflight legs 6 (KS-470) ... Refs KS-1437'); rep(k == ['KS-1437', 'KS-470'], 'PLANTED hyphenated foreign key KS-470 FIRES T3')
    rep(refs_window('a\nthis resolves it\nRefs KS-1437')[1] and not refs_window('Refs KS-1437 https://x')[1], 'closing word within 3 lines above Refs FIRES; clean passes')
    m = {'locks': 5, 'entries': 7, 'field_writes': 18}; r = {'package_copy_lines': 82, 'dockerfiles_a': 37, 'ships': {'pbkdf2': ['x'] * 25}}; ns = dict((p, tuple(v)) for p, v in P['numstat'].items())
    good = '5 locks, 7 entries, **18 field writes**. 5 files changed, 18 insertions(+), 18 deletions(-) pbkdf2 reaches 25 runtime images'
    rep(all(x[3] for x in claims(good, m, r, ns)), 'claims: a true body passes')
    rep(not all(x[3] for x in claims('Of 82 COPY lines naming `package*.json` across 38 Dockerfiles', m, r, ns)), 'PLANTED 38 Dockerfiles vs measured 37 FAILS')
    rep(not all(x[3] for x in claims('5 locks, 7 entries, **21 field writes**', m, r, ns)), 'PLANTED 21 field writes FAILS')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if not A: print(__doc__); return 2
    try:
        if A[0] == '--selftest': return selftest()
        if A[0] == 'api':
            head = req(A, '--head', True); pr = gh_get('pulls/%s' % P['pr']); b = pr.get('body') or ''
            if opt(A, '--body-out'): open(opt(A, '--body-out'), 'w').write(b)
            print('API #%s head %s branch %s base %s state %s merged %s mergeable %s mergeable_state %s' % (
                P['pr'], pr['head']['sha'], pr['head']['ref'], pr['base']['ref'], pr['state'], pr['merged'], pr.get('mergeable'), pr.get('mergeable_state')))
            print('BODY sha256/16 %s chars %d utf8-bytes %d | title %r (%d) | commits %s +%s/-%s files %s | updated %s' % (
                hashlib.sha256(b.encode()).hexdigest()[:16], len(b), len(b.encode()), pr['title'], len(pr['title']), pr.get('commits'), pr.get('additions'),
                pr.get('deletions'), pr.get('changed_files'), pr['updated_at']))
            return 0 if pr['head']['sha'] == head and pr['state'] == 'open' and not pr['merged'] and pr['base']['ref'] == 'develop' else 1
        if A[0] == 'actions': return actions(req(A, '--at', True), req(A, '--develop', True), req(A, '--compare-head', True), opt(A, '--out'))
        if A[0] == 'census': return census()
        if A[0] == 'prtext': return prtext(req(A, '--head', True), req(A, '--measured'), req(A, '--reach'), opt(A, '--repo'), opt(A, '--base'), opt(A, '--body-file'), opt(A, '--sentences-out'))
        if A[0] == 'linear': return linear_read(opt(A, '--comments-out'))
    except SystemExit as e:
        print(e); return 2
    except (OSError, ValueError, urllib.error.URLError, KeyError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
