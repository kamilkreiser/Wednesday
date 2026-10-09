#!/usr/bin/env python3
"""gh_gate79.py — GitHub / Linear READ-ONLY instruments for gate79 (#1437, KS-1402). REST GETs + Linear GraphQL reads; tokens BY NAME,
never printed. The Actions machinery (log fetch without the auth header on the 302, the failure SIGNATURE, comparators BY WORKFLOW
PATH, the planted develop-only rule) is CARRIED VERBATIM from gh_gate78.py; [g79] marks this kit's changes. EVERY PIN IS REQUIRED.

  api       --head H [--body-out F]   head / branch / base / state / merged / mergeable / mergeable_state (the READY read `dirty`),
            body sha256/16, chars AND utf-8 bytes; rc 1 unless head == H, open, unmerged, base develop. `dirty` is REPORTED, not refused
            (the docs keep-both merge-in is the merge seat's job, Q-DOCSMERGE).
  actions   --at H --develop D [--out DIR] [--wait MIN]   CLASSIFIED BY WORKFLOW PATH (see gh_gate78.py's header, unchanged):
            X0 runs at the full head + fabricated-sha control; A1 every path's status, PENDING named; A2 every failing job's LOG read
            (##[group] positive control, SIGNATURE, CHANGE needles [g79: ks1402 / transfer-custody / lookupHash / RECIPIENT_NOT_FOUND /
            HOLDER_EMAIL_SCHEMA / email_lookup_hash / ks739 / ks697], fabricated needle 0); A3 comparators (develop's own run of the
            path, else pull_request runs of the SAME path on OTHER heads); A4 history. PRE-EXISTING only with a comparator covering the
            head's signature AND 0 change needles; else UNCLASSIFIED (BLOCKS).
  census    [g79] every OTHER open PR: OVERLAP-CODE (touches documents.ts, originate.openapi.ts or any of the 3 test files, or is
            titled KS-1402) / OVERLAP-DOCS (touches only the 2 Projects Documents html or the openapi yaml — the READY's 8 + #1429) /
            other. CONTROL: a fabricated row on documents.ts classifies OVERLAP-CODE.
  prtext    --head H --repo CLONE --base B [--body-file F] [--sentences-out F]
            T1 exactly one `Refs KS-1402` line; T1b no closing-family word on it or the 3 lines above   T2 closing words before a key
            / #n (title + body), the conventional `fix(KS-n)` form COUNTED (Q-FIXPREFIX)   T3 only KS-1402 hyphenated (title + body)
            T4 title == the commit subject; len(title) <= 92 AS DECLARED (no `(#n)` arithmetic)   T5 0 trailer lines   T5b attribution
            lines COUNTED (gate77 Q-ATTR77 precedent: a finding to rule)   T6 [g79] the body's figures vs measured: numstat
            (8 files, +852/-289), "14 rows" vs the matrix file's 13 (the READY's own correction), cell counts   T7 every factual
            sentence -> --sentences-out.
  linear    [g79] KS-1402: state, archivedAt, updatedAt, comments (count, newest id) vs the READY's (5, 7740c258,
            2026-10-09T02:07:01.353Z) — a CHANGE is printed, the ticket comment naming #1437 is Wednesday's batch (may or may not
            exist yet: reported either way); attachments naming #1437. Read-only.
  --selftest  the classifier (carried), the census classifier, the key / closing / fix-prefix / attribution scanners, the claims.
rc 0 / 1 (finding, blind control, OVERLAP-CODE, UNCLASSIFIED, PENDING, NOT RUN) / 2 refused / 3 API failure."""
import hashlib, json, os, re, subprocess, sys, time, urllib.error, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate79 import K, gh_get, gh_pages, linear_issue, env_value, req, opt

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
        resp = op.open(r, timeout=60); return resp.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        if e.code not in (301, 302, 303, 307, 308): raise
        loc = e.headers.get('Location')
    return urllib.request.urlopen(urllib.request.Request(loc), timeout=120).read().decode('utf-8', 'replace')


SIG = re.compile(r'(##\[error\]|\b[1-9]\d* failed\b|✖|AssertionError|^not ok \d|\bFAILED\b|\bFAIL\b)')
TS = re.compile(r'^\d{4}-\d\d-\d\dT[\d:.]+Z\s?')
DUR = re.compile(r'\s*\(\d+(?:\.\d+)?m?s\)$')


def norm(l): return DUR.sub('', TS.sub('', l).strip())


def signature(text):
    """the FAILURE SIGNATURE of a log: every line (timestamp + duration stripped) carrying an error marker, a non-zero `N failed`, a
    ✖, an AssertionError, a TAP `not ok`, or FAIL / FAILED as a word. PRE-EXISTING needs the head's signature to be a SUBSET."""
    return sorted(set(norm(l) for l in text.split('\n') if SIG.search(norm(l))))


def needles(text):
    lines = text.split('\n')
    ch = dict((n, text.count(n)) for n in AC['needles_change'])
    return {'signature': signature(text), 'bytes': len(text.encode()), 'positive_group': text.count(AC['positive_control']),
            'change': ch, 'change_lines': [norm(l)[:200] for l in lines if any(n in l for n in AC['needles_change'])][:6],
            'fabricated': text.count(AC['fabricated_control'])}


def runs_at(sha):
    return gh_get('actions/runs?head_sha=%s&per_page=100' % sha)['workflow_runs']


def latest_by_path(runs):
    out = {}
    for r in sorted(runs, key=lambda r: r.get('created_at', '')): out[r['path']] = r
    return out


def failing_jobs(run, out_dir, tag):
    res = []
    for j in gh_get('actions/runs/%d/jobs?per_page=100' % run['id'])['jobs']:
        if j.get('conclusion') not in FAILING: continue
        steps = [s['name'] for s in j.get('steps') or [] if s.get('conclusion') in FAILING]
        try: text = fetch_log(j['id'])
        except (urllib.error.URLError, OSError) as e: text = ''; print('  LOG FETCH FAILED job %s: %s' % (j['id'], e))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            fn = os.path.join(out_dir, '%s_%s_%d.log' % (tag, re.sub(r'\W+', '_', run['path'].split('/')[-1])[:30], j['id'])); open(fn, 'w').write(text)
        n = needles(text); res.append((j['name'], steps, n))
        print('  JOB %-30s failing steps %s | log %d B, ##[group] %d, signature lines %d, change needles %s, fabricated %d' % (
            j['name'], steps, n['bytes'], n['positive_group'], len(n['signature']), dict((k, v) for k, v in n['change'].items() if v) or 0, n['fabricated']))
        for x in n['change_lines']: print('      CHANGE-NEEDLE LINE %s' % x)
        for x in n['signature'][:10]: print('      SIG %s' % x[:200])
    return res


def classify_red(head_jobs, comp_jobs):
    """-> (verdict, why, matched comparator labels). comp_jobs: {label: [(job, steps, needles)]} read by THIS tool."""
    why = []; matched = set()
    if not head_jobs: return 'UNCLASSIFIED', ['no failing job read at the head'], []
    for job, steps, n in head_jobs:
        if n['positive_group'] == 0: why.append('%s: log UNREAD (##[group] 0)' % job)
        if any(n['change'].values()): why.append('%s: change needles present %s' % (job, dict((k, v) for k, v in n['change'].items() if v)))
        sig = set(n['signature'])
        m = [lab for lab, js in comp_jobs.items() for (cj, cs, cn) in js
             if cj == job and set(cs) == set(steps) and cn['positive_group'] > 0 and sig and sig <= set(cn['signature'])]
        if not m: why.append('%s: no comparator shows the same job + step set with a signature covering the head\'s %d lines' % (job, len(sig)))
        matched |= set(m)
    return ('PRE-EXISTING' if not why else 'UNCLASSIFIED'), why, sorted(matched)


def pr_comparators(path, head, n=2):
    wf = path.split('/')[-1]
    runs = gh_get('actions/workflows/%s/runs?event=pull_request&status=completed&per_page=30' % wf)['workflow_runs']
    out = [r for r in runs if r['head_sha'] != head and r.get('conclusion') in FAILING][:n]
    return out


def actions(at, develop, out_dir, wait_min):
    try:
        fab = runs_at('f' * 40); polls = 0; prev = None
        while True:
            h_runs = runs_at(at); h = latest_by_path(h_runs); polls += 1
            pend = sorted(p for p, r in h.items() if r['status'] != 'completed')
            sig = json.dumps(sorted((p, r['status'], r['conclusion']) for p, r in h.items()))
            if not wait_min or (not pend and sig == prev) or polls > wait_min: break
            prev = sig; time.sleep(60)
        d = latest_by_path(runs_at(develop))
    except (urllib.error.URLError, OSError, KeyError, ValueError) as e:
        print('API FAILURE: %s' % e); return 3
    x0 = len(h_runs) > 0 and len(fab) == 0
    print('X0 runs at the full head %s: %d | CONTROL fabricated sha: %d runs | polls %d -> %s' % (at, len(h_runs), len(fab), polls, 'PASS' if x0 else 'FAIL'))
    print('READ at %s: head %d paths | develop %s %d paths' % (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), len(h), develop[:12], len(d)))
    for p in sorted(set(h) | set(d)):
        f = lambda x: '%s/%s/%s' % ((x.get(p) or {}).get('event', '-'), (x.get(p) or {}).get('status', 'ABSENT'), (x.get(p) or {}).get('conclusion', '-'))
        print('RUN %-52s %-32s head %-34s develop %s' % (p, (h.get(p) or d.get(p))['name'], f(h), f(d)))
    pend = sorted(p for p, r in h.items() if r['status'] != 'completed')
    reds = sorted(p for p, r in h.items() if r.get('conclusion') in FAILING)
    verdicts = {}
    for p in reds:
        print('RED %s (%s, run %d)' % (p, h[p]['name'], h[p]['id'])); hj = failing_jobs(h[p], out_dir, 'head')
        comp = {}; devonly = {}
        if p in d and d[p].get('conclusion') in FAILING:
            print(' COMPARATOR develop %s push run %d (the path HAS a develop run)' % (develop[:12], d[p]['id'])); comp['develop'] = devonly['develop'] = failing_jobs(d[p], out_dir, 'develop')
        elif p in d:
            print(' COMPARATOR develop %s: its run of this path concluded %s (not failing: the head\'s red has no develop twin)' % (develop[:12], d[p].get('conclusion')))
        else:
            print(' COMPARATOR develop %s: 0 runs of %s (the workflow has no develop push trigger) -> pull_request comparators on OTHER heads' % (develop[:12], p))
        if 'develop' not in comp:
            for r in pr_comparators(p, at):
                lab = 'pr%s@%s' % (','.join(str(x['number']) for x in r.get('pull_requests') or []) or '?', r['head_sha'][:12])
                print(' COMPARATOR %s run %d (%s, %s, %s)' % (lab, r['id'], r['event'], r['head_branch'][:50], r['created_at'])); comp[lab] = failing_jobs(r, out_dir, lab)
        hist = gh_get('actions/workflows/%s/runs?status=completed&per_page=12' % p.split('/')[-1])['workflow_runs']
        cnt = {}
        for r in hist: cnt[r.get('conclusion')] = cnt.get(r.get('conclusion'), 0) + 1
        print(' HISTORY last %d completed runs of %s: %s | events %s' % (len(hist), p, cnt, sorted(set(r['event'] for r in hist))))
        v, why, m = classify_red(hj, comp); verdicts[p] = v
        dv = classify_red(hj, devonly)[0] if devonly else 'NEW (no develop run of this path: a develop-only rule calls every red NEW)'
        print(' CLASSIFY %s: %s by %s %s' % (p, v, m or 'no comparator', why or ''))
        print(' PLANTED-RULE CONTROL (develop-only classifier, NEVER the decision): %s' % dv)
    print('PENDING %s' % (pend or 'NONE'))
    print('NOTE: a CI red is classified by PATH against comparators read by this tool; a green in-hook preflight does not explain a red CI step.')
    # [g79] a workflow that ran at develop (or that the kit expects on a PR) but has NO run at the head is NOT RUN — never a pass. A
    # `dirty` PR (merge conflict) gets no pull_request merge ref, so its pull_request workflows do not start: 0 reds is then 0 MEASURED.
    expected = set(AC.get('expected_pr_workflows', [])) | set(d)
    absent = sorted(p for p in expected if p not in h)
    real = sorted(p for p, r in h.items() if r.get('conclusion') not in ('skipped', None) or r['status'] != 'completed')
    print('NOT RUN AT HEAD %s | head runs that actually executed (not skipped): %s' % (absent or 'NONE', real or 'NONE'))
    ok = x0 and not pend and all(v == 'PRE-EXISTING' for v in verdicts.values()) and not absent
    return 0 if ok else 1


CODE_PATHS = set(p for p in P['numstat'] if not p.startswith('Projects Documents/') and not p.endswith('secuura-api.yaml'))
DOC_PATHS = set(P['numstat']) - CODE_PATHS
FIXPREFIX = re.compile(r'\b(fix|close|resolve|complete)[a-z]*\(\s*KS-\d+\s*\)', re.I)


def classify_pr(pr_row, files):
    if KEY in (pr_row.get('title') or '') or set(files) & CODE_PATHS: return 'OVERLAP-CODE'
    if set(files) & DOC_PATHS: return 'OVERLAP-DOCS'
    return 'other'


def census():
    prs = gh_pages('pulls?state=open'); rows, cnt = [], {}
    for pr in prs:
        if str(pr['number']) == P['pr']: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % pr['number'])]
        c = classify_pr(pr, files); cnt[c] = cnt.get(c, 0) + 1
        if c != 'other': rows.append('  %s #%d %s %s %s' % (c, pr['number'], pr['head']['sha'][:12], pr['title'][:70], sorted(set(files) & set(P['numstat']))))
    ctl = classify_pr({'title': 'x'}, [K['route_file']]) == 'OVERLAP-CODE' and classify_pr({'title': 'y'}, ['a.ts']) == 'other' \
        and classify_pr({'title': 'z'}, [sorted(DOC_PATHS)[0]]) == 'OVERLAP-DOCS'
    print('CENSUS %d other open PR(s): %s | CONTROL fires %s' % (sum(cnt.values()), cnt, ctl))
    for r in rows: print(r)
    return 3 if not ctl else (1 if cnt.get('OVERLAP-CODE') else 0)


def scan(text): return sorted(set(re.findall(r'\bKS-\d+\b', text))), CLOSING.findall(text), FIXPREFIX.findall(text)


def refs_window(body):
    lines = body.split('\n'); hits = [i for i, l in enumerate(lines) if re.match(r'^\s*`?Refs %s\b' % re.escape(KEY), l)]
    bad = [i for i in hits for j in range(max(0, i - 3), i + 1) if CLOSING_WORD.search(lines[j])]
    return hits, bad


def attribution(body):
    return [l.strip() for l in body.split('\n') if re.search(r'Generated with|Co-Authored-By|Signed-off-by', l, re.I)]


def claims(body, ns):
    out = []
    def one(cid, rx, want):
        hits = [tuple(int(x.replace(',', '')) for x in g.groups()) for g in re.finditer(rx, body)]
        out.append((cid, hits or None, want, (not hits) or all(h == want for h in hits)))
    one('CL-FILES', r'\b(\d+) files\b[^.\n]{0,20}\+(\d+)\s*/\s*-(\d+)', (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values())))
    one('CL-ROWS', r'\b(\d+) rows\b', (K['ready_claims']['tamper_rows_file'],))
    one('CL-1402', r'ks1402\D{0,12}(\d+)/(\d+)', (11, 11))
    one('CL-739', r'ks739\D{0,12}(\d+)/(\d+)', (17, 17))
    one('CL-697', r'ks697\D{0,12}(\d+)/(\d+)', (17, 17))
    one('CL-SUITE', r'([\d,]+)/([\d,]+) across (\d+) files', (1096, 1096, 97))
    return out


def sentences(body):
    s = re.split(r'(?<=[.;:!?])\s+|\n+', body)
    return [x.strip() for x in s if x.strip() and re.search(r'\d|KS-|KS \d|`|tenant|auth', x)]


def prtext(head, repo, base, body_file, sent_out):
    if body_file:
        body = open(body_file, encoding='utf-8').read(); title = P['subject']; print('OFFLINE body from %s (title assumed == kit subject)' % body_file)
    else:
        pr = gh_get('pulls/%s' % P['pr']); body = pr.get('body') or ''; title = pr['title']
        if pr['head']['sha'] != head: print('REFUSED: API head %s != --head %s' % (pr['head']['sha'], head)); return 1
    keys, closing, fixp = scan(body + '\n' + title); hits, bad = refs_window(body)
    co = len(re.findall(r'(?im)^\s*(co-authored-by|signed-off-by):', body)); attr = attribution(body)
    print('BODY sha256/16 %s, %d chars, %d utf8-bytes' % (hashlib.sha256(body.encode()).hexdigest()[:16], len(body), len(body.encode())))
    print('T1 `Refs %s` lines: %d at line(s) %s (want exactly 1) | T1b closing words on it or the 3 lines above: %s' % (KEY, len(hits), [i + 1 for i in hits], bad or 'none'))
    print('T2 closing references (title + body): %s | conventional fix(KS-n) form: %s (Q-FIXPREFIX: the gate rules it)' % (closing or 'none', fixp or 'none'))
    print('T3 hyphenated keys (title + body): %s -> only %s: %s' % (keys, KEY, keys == [KEY]))
    print('T4 title %r (%d chars <= %d AS DECLARED: %s) == commit subject %s' % (title, len(title), P['subject_max'], len(title) <= P['subject_max'], title == P['subject']))
    print('T5 trailer-shaped lines in the body: %d' % co)
    print('T5b attribution lines (a finding for the gate to rule, not a T-fail): %d %s' % (len(attr), attr))
    ok = len(hits) == 1 and not bad and keys == [KEY] and len(title) <= P['subject_max'] and title == P['subject'] and co == 0
    ns = {}
    for l in subprocess.run(['git', '-C', repo, 'diff', '--numstat', base, head], capture_output=True, text=True).stdout.strip().split('\n'):
        a, dl, p = l.split('\t'); ns[p] = (int(a), int(dl))
    for cid, stated, want, good in claims(body, ns):
        st = 'OK      ' if (good and stated) else ('ABSENT  ' if not stated else 'MISMATCH')
        print('T6 %-10s %s stated %s measured %s' % (cid, st, stated, want))
        ok &= good
    ss = sentences(body)
    if sent_out: open(sent_out, 'w').write('\n'.join('%3d  %s' % (i + 1, x) for i, x in enumerate(ss)) + '\n')
    print('T7 %d factual-looking sentences written to %s for the sentence-by-sentence ruling' % (len(ss), sent_out or '(not written: give --sentences-out)'))
    return 0 if ok else 1


def linear_read(comments_out):
    i, err = linear_issue(KEY)
    if not i: print('LINEAR %s not returned: %s' % (KEY, err)); return 1
    cs = i['comments']['nodes']; at = i['attachments']['nodes']; rc_ = K['linear_ready_claims']
    print('LINEAR %s %r state %s (%s) updatedAt %s archivedAt %s comments %d attachments %d' % (
        i['identifier'], i['title'], i['state']['name'], i['state']['type'], i['updatedAt'], i['archivedAt'], len(cs), len(at)))
    newest = sorted(cs, key=lambda c: c['createdAt'])[-1]['id'][:8] if cs else None
    print('  vs the READY: comments %d (READY %d) | newest %s (READY %s) | updatedAt %s (READY %s) -> %s' % (
        len(cs), rc_['comments'], newest, rc_['newest_comment'], i['updatedAt'], rc_['updatedAt'],
        'UNCHANGED' if (len(cs), newest, i['updatedAt']) == (rc_['comments'], rc_['newest_comment'], rc_['updatedAt']) else 'CHANGED since the READY (read what changed)'))
    link = [c for c in cs if re.search(r'pull/%s\b' % P['pr'], c['body'])]
    for c in cs: print('  COMMENT %s %s %d B sha256/16 %s links #%s: %s' % (c['id'][:8], c['createdAt'], len(c['body'].encode()), hashlib.sha256(c['body'].encode()).hexdigest()[:16], P['pr'], c in link))
    for a in at: print('  ATTACHMENT %s %r %s %s' % (a['id'][:8], a['title'], a['url'], a['createdAt']))
    if comments_out: open(comments_out, 'w').write('\n\n=====\n\n'.join('%s %s\n%s' % (c['id'], c['createdAt'], c['body']) for c in cs))
    ok = i['state']['name'] in K['linear_ok_states'] and not i['archivedAt']
    print('VERDICT %s %s (want state in %s, not archived) | a comment linking #%s: %d (Wednesday\'s batch: reported, not required)' % (
        KEY, 'OK' if ok else 'FINDING', K['linear_ok_states'], P['pr'], len(link)))
    return 0 if ok else 1


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    st = 'Audit-contract suites'
    nh = needles('##[group]x\n2026-10-09T00:30:00.1Z ##[error]expected exit 3 (refused), got 1\n')
    nd = needles('##[group]y\n2026-10-08T09:00:00.1Z ##[error]expected exit 3 (refused), got 1\n')
    v = classify_red([('Dependency Audit', [st], nh)], {'pr1434@d7ba337a8ef6': [('Dependency Audit', [st], nd)]})
    rep(v[0] == 'PRE-EXISTING', 'classify (carried): same job + step + signature on another PR head -> PRE-EXISTING')
    rep(classify_red([('Dependency Audit', [st], nh)], {})[0] == 'UNCLASSIFIED', 'PLANTED-RULE: no comparator -> UNCLASSIFIED, never pre-existing')
    rep(classify_red([('Dependency Audit', [st], needles('##[group]\n##[error]expected exit 3 (refused), got 1\nks1402 cell C2 failed'))], {'d': [('Dependency Audit', [st], nd)]})[0] == 'UNCLASSIFIED',
        '[g79] PLANTED change needle (ks1402) in the failing log -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', [st], needles('##[error]expected exit 3 (refused), got 1'))], {'d': [('Dependency Audit', [st], nd)]})[0] == 'UNCLASSIFIED', 'PLANTED unread head log (##[group] 0) -> UNCLASSIFIED')
    rep(isinstance(_NoRedirect().redirect_request(None, None, 302, '', {}, 'u'), type(None)), 'the log opener does NOT follow the 302 with the auth header')
    rep(classify_pr({'title': 'KS-1402 x'}, []) == 'OVERLAP-CODE' and classify_pr({'title': 'x'}, [K['route_file']]) == 'OVERLAP-CODE'
        and classify_pr({'title': 'x'}, ['Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html']) == 'OVERLAP-DOCS' and classify_pr({'title': 'x'}, ['q.ts']) == 'other',
        '[g79] census classifier: code / docs / other')
    k, c, f = scan('fix(KS-1402): x\nRefs KS-1402. the KS 739 file; KS 697.'); rep(k == ['KS-1402'] and f, 'scan: de-hyphenated keys are not keys; fix(KS-1402) COUNTED')
    k, c, f = scan('same shape as KS-1406. Refs KS-1402'); rep(k == ['KS-1402', 'KS-1406'], 'PLANTED hyphenated foreign key KS-1406 FIRES T3')
    rep(refs_window('a\nthis resolves it\nRefs KS-1402')[1] and not refs_window('Refs KS-1402 https://x')[1], 'closing word within 3 lines above Refs FIRES; clean passes')
    rep(attribution('x\n\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)\n') and not attribution('clean'), 'T5b attribution scanner sees the Generated-with line; clean reads 0')
    ns = dict((p, tuple(v)) for p, v in P['numstat'].items())
    rep(all(x[3] for x in claims('8 files, +852/-289. the matrix holds 13 rows', ns)), 'claims: a true body passes')
    rep(not all(x[3] for x in claims('the matrix holds 14 rows', ns)), '[g79] PLANTED "14 rows" vs the file\'s 13 FAILS (the READY\'s own correction)')
    rep(not all(x[3] for x in claims('8 files, +853/-289', ns)), 'PLANTED +853 vs measured +852 FAILS')
    rep(any(x[1] is None for x in claims('nothing numeric', ns)), 'an absent claim reads ABSENT, never OK')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if not A: print(__doc__); return 2
    try:
        if A[0] == '--selftest': return selftest()
        if A[0] == 'api':
            head = req(A, '--head', True); pr = gh_get('pulls/%s' % P['pr']); b = pr.get('body') or ''
            if opt(A, '--body-out'): open(opt(A, '--body-out'), 'w').write(b)
            print('API #%s head %s branch %s base %s state %s merged %s mergeable %s mergeable_state %s draft %s' % (
                P['pr'], pr['head']['sha'], pr['head']['ref'], pr['base']['ref'], pr['state'], pr['merged'], pr.get('mergeable'), pr.get('mergeable_state'), pr.get('draft')))
            print('BODY sha256/16 %s chars %d utf8-bytes %d | title %r (%d) | commits %s +%s/-%s files %s | updated %s' % (
                hashlib.sha256(b.encode()).hexdigest()[:16], len(b), len(b.encode()), pr['title'], len(pr['title']), pr.get('commits'), pr.get('additions'),
                pr.get('deletions'), pr.get('changed_files'), pr['updated_at']))
            return 0 if pr['head']['sha'] == head and pr['state'] == 'open' and not pr['merged'] and pr['base']['ref'] == 'develop' else 1
        if A[0] == 'actions':
            w = opt(A, '--wait')
            return actions(req(A, '--at', True), req(A, '--develop', True), opt(A, '--out'), int(w) if w else 0)
        if A[0] == 'census': return census()
        if A[0] == 'prtext':
            return prtext(req(A, '--head', True), req(A, '--repo'), req(A, '--base', True), opt(A, '--body-file'), opt(A, '--sentences-out'))
        if A[0] == 'linear': return linear_read(opt(A, '--comments-out'))
    except SystemExit as e:
        print(e); return 2
    except (OSError, ValueError, urllib.error.URLError, KeyError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
