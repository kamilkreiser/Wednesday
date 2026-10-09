#!/usr/bin/env python3
"""gh_gate81.py — GitHub / Linear READ-ONLY instruments for gate81 (#1443 KS-1346, #1444 KS-937, #1445 + #1446 KS-1410). REST GETs + Linear GraphQL
reads; tokens BY NAME, never printed. The Actions machinery (log fetch without the auth header on the 302, the failure SIGNATURE, comparators BY
WORKFLOW PATH, the planted develop-only rule) is CARRIED from gh_gate80.py; [g81] marks this kit's changes. EVERY PIN IS REQUIRED; every PR command
takes --pr 1443|1444|1445|1446 (a foreign number is refused).

  api       --pr N --head H [--body-out F]   head / branch / base / state / merged / mergeable / mergeable_state, body sha256/16, chars AND
            bytes; rc 1 unless head == H, open, unmerged, base develop. `dirty` is REPORTED (the docs keep-both is the merge seat's job).
  actions   --pr N --at H --develop D [--out DIR] [--wait MIN]   CLASSIFIED BY WORKFLOW PATH: X0 runs at the full head + fabricated-sha
            control; A1 every path's status, PENDING named; A2 every failing job's LOG read (##[group] positive control, SIGNATURE, CHANGE
            needles, fabricated needle 0; + the KS-1148 evidence: `semver` / `Cannot find package` counts in the log); A3 comparators
            (develop's run of the path, else pull_request runs of the SAME path on OTHER heads); A4 history. PRE-EXISTING only with a
            comparator covering the head's signature AND 0 change needles; else UNCLASSIFIED (BLOCKS). Known and VERIFIED here, never trusted:
            Security Scanning (KS-1148), PR Security Gates (KS-168) and `pr` fail on develop's OWN push run at 613070f29112.
  audit     --repo R --base B --head1443 H --head1444 H --head1445 H --head1446 H [--reference REV]   KS-1148 attribution, READ half: line 50 of
            Blockchain/Dev/scripts/audit/audit-locks.mjs at base, each of the four heads and the reference (if in the store), whether `from 'semver'`
            is on it, whether any PR touches the file / a manifest / a lock, plus a CONTROL (the same reader on a line that is not there).
  census    every OTHER open PR: OVERLAP-CODE (touches a non-doc path of ANY of the four, or is titled KS-1346 / KS-937 / KS-1410) / OVERLAP-DOCS
            (touches only the two shared docs) / other; names every PR touching audit-export.ts, batch.ts, notifications.ts, delegations.ts,
            check-shared-relink.sh, run-shell-suites.sh, or a ks1346 / ks1410 / check_shared_relink file. CONTROL: fabricated rows classify.
  prtext    --pr N --head H --repo CLONE --base B [--body-file F] [--sentences-out F]   T1 exactly one `Refs KS-n` line; T1b no closing word on
            it or the 3 lines above   T2 closing words before a key / #n (incl. fix(KS-n))   T3 only the PR's own key hyphenated (title + body)
            T4 title vs the commit subject: both recorded, <= 92 AS DECLARED, no `(#n)`   T5 0 trailer lines   T5b attribution lines COUNTED
            (gate77 Q-ATTR77: count, do not rule)   T6 the body's figures vs the measured / READY figures, per PR   T7 every factual sentence ->
            --sentences-out.
  linear    --pr N   state, archivedAt, updatedAt, comments (count, newest), attachments naming the PR. KS-1346 / KS-937 / KS-1410 must stay OPEN.
  --selftest
rc 0 / 1 (finding, blind control, OVERLAP-CODE, UNCLASSIFIED, PENDING, NOT RUN) / 2 refused / 3 API failure."""
import hashlib, json, os, re, subprocess, sys, time, urllib.error, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate81 import K, PR, gh_get, gh_pages, linear_issue, env_value, req, opt, git, show, resolvable

HERE = os.path.dirname(os.path.abspath(__file__))
AC = K['actions']
FAILING = ('failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required')
CLOSING = re.compile(K['closing_rx'], re.I)
CLOSING_WORD = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\b', re.I)
FIXPREFIX = re.compile(r'\b(fix|close|resolve|complete)[a-z]*\(\s*KS-\d+\s*\)', re.I)
ALL_PATHS = {}
for _p in K['prs'].values():
    for _x in _p['numstat']: ALL_PATHS.setdefault(_x, []).append(_p['pr'])
DOC_PATHS = set(K['known_develop_overlap'])
CODE_PATHS = set(ALL_PATHS) - DOC_PATHS
WATCH = ['audit-export.ts', 'batch.ts', 'notifications.ts', 'delegations.ts', 'check-shared-relink', 'check_shared_relink', 'run-shell-suites.sh', 'ks1346', 'ks1410']


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


SECS = re.compile(r'=\d+(?:\.\d+)?s\b')


def norm(l): return SECS.sub('=<N>s', DUR.sub('', TS.sub('', l).strip()))   # [g81] a measured-seconds figure (`kill_to_exit=11s` vs `12s`) is run-to-run timing, not a different failure


def signature(text):
    return sorted(set(norm(l) for l in text.split('\n') if SIG.search(norm(l))))


def needles(text):
    lines = text.split('\n')
    ch = dict((n, text.count(n)) for n in AC['needles_change'])
    return {'signature': signature(text), 'bytes': len(text.encode()), 'positive_group': text.count(AC['positive_control']),
            'change': ch, 'change_lines': [norm(l)[:200] for l in lines if any(n in l for n in AC['needles_change'])][:6],
            'fabricated': text.count(AC['fabricated_control']),
            'semver': text.count('semver'), 'cannot_find': len(re.findall(r'Cannot find (package|module)|ERR_MODULE_NOT_FOUND', text))}


def runs_at(sha): return gh_get('actions/runs?head_sha=%s&per_page=100' % sha)['workflow_runs']


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
        print('  JOB %-30s failing steps %s | log %d B, ##[group] %d, signature lines %d, change needles %s, fabricated %d | KS-1148 evidence: `semver` x%d, cannot-find x%d' % (
            j['name'], steps, n['bytes'], n['positive_group'], len(n['signature']), dict((k, v) for k, v in n['change'].items() if v) or 0, n['fabricated'], n['semver'], n['cannot_find']))
        for x in n['change_lines']: print('      CHANGE-NEEDLE LINE %s' % x)
        for x in n['signature'][:10]: print('      SIG %s' % x[:200])
    return res


def classify_red(head_jobs, comp_jobs):
    """-> (verdict, why, matched comparator labels). comp_jobs: {label: [(job, steps, needles)]} read by THIS tool.
    [g81] a CHANGE needle (a token of THESE changes, e.g. `format:check`) is a signal only where the head's count EXCEEDS the count in every
    comparator log that matched the job + step set + signature: the Playwright log names `format:check` 40 times on develop too."""
    why = []; matched = set()
    if not head_jobs: return 'UNCLASSIFIED', ['no failing job read at the head'], []
    for job, steps, n in head_jobs:
        if n['positive_group'] == 0: why.append('%s: log UNREAD (##[group] 0)' % job)
        sig = set(n['signature'])
        mc = [(lab, cn) for lab, js in comp_jobs.items() for (cj, cs, cn) in js
              if cj == job and set(cs) == set(steps) and cn['positive_group'] > 0 and sig and sig <= set(cn['signature'])]
        m = [lab for lab, _ in mc]
        excess = dict((k, v) for k, v in n['change'].items() if v and v > max([cn['change'].get(k, 0) for _, cn in mc] or [0]))
        if excess: why.append('%s: change needles present beyond the comparator %s' % (job, excess))
        if not m: why.append('%s: no comparator shows the same job + step set with a signature covering the head\'s %d lines' % (job, len(sig)))
        matched |= set(m)
    return ('PRE-EXISTING' if not why else 'UNCLASSIFIED'), why, sorted(matched)


def pr_comparators(path, head, n=2):
    wf = path.split('/')[-1]
    runs = gh_get('actions/workflows/%s/runs?event=pull_request&status=completed&per_page=30' % wf)['workflow_runs']
    return [r for r in runs if r['head_sha'] != head and r.get('conclusion') in FAILING][:n]


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
    print('NOTE: a CI red is classified by PATH against comparators read by this tool. KS-1148 (audit-locks.mjs :50, undeclared `semver`) is attributed ONLY where the failed step\'s log shows the import error identically on each PR and on the reference (the `audit` subcommand reads the line).')
    expected = set(AC.get('expected_pr_workflows', [])) | set(d)
    absent = sorted(p for p in expected if p not in h)
    real = sorted(p for p, r in h.items() if r.get('conclusion') not in ('skipped', None) or r['status'] != 'completed')
    print('NOT RUN AT HEAD %s | head runs that actually executed (not skipped): %s' % (absent or 'NONE', real or 'NONE'))
    ok = x0 and not pend and all(v == 'PRE-EXISTING' for v in verdicts.values()) and not absent
    return 0 if ok else 1


def line_n(text, n): 
    ls = text.split('\n'); return ls[n - 1] if 0 < n <= len(ls) else None


def audit(repo, base, heads, ref):
    A = K['audit_locks']; rc = 0
    revs = [('base', base)] + [('head' + n, h) for n, h in heads.items()] + ([('reference', ref)] if ref else [])
    for lab, rev in revs:
        if not resolvable(repo, rev): print('AUDIT %-9s %s NOT IN THE STORE (fetch BY SHA into your clone, X7): NOT READ' % (lab, rev[:12])); rc = 1; continue
        txt = show(repo, rev, A['path']); l = line_n(txt, A['line'])
        print('AUDIT %-9s %s %s:%d = %r | carries %s: %s' % (lab, rev[:12], A['path'].split('/')[-1], A['line'], l, A['needle'], bool(l and A['needle'] in l)))
        if not (l and A['needle'] in l): rc = 1
    ctl = line_n(show(repo, base, A['path']), 99999)
    print('AUDIT CONTROL: the same reader on line 99999 returns %r (must be None)' % ctl); rc |= 0 if ctl is None else 1
    for n in K['go_prs']:
        ns = set(PR(n)['numstat']); hit = sorted(p for p in ns if p == A['path'] or p.endswith('package.json') or p.endswith('package-lock.json'))
        print('AUDIT #%s touches audit-locks.mjs / a manifest / a lock: %s' % (n, hit or 'NONE')); rc |= 1 if hit else 0
    return rc


def classify_pr(pr_row, files):
    t = pr_row.get('title') or ''
    if re.search(r'KS[- ](1346|937|1410)\b', t) or set(files) & CODE_PATHS: return 'OVERLAP-CODE'
    if set(files) & DOC_PATHS: return 'OVERLAP-DOCS'
    return 'other'


def watched(files): return sorted(f for f in files if any(w in f for w in WATCH))


def census():
    prs = gh_pages('pulls?state=open'); rows, cnt = [], {}
    for pr in prs:
        if str(pr['number']) in K['prs']: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % pr['number'])]
        c = classify_pr(pr, files); cnt[c] = cnt.get(c, 0) + 1
        w = watched(files)
        if c != 'other' or w: rows.append('  %s #%d %s %s shared %s%s' % (c, pr['number'], pr['head']['sha'][:12], pr['title'][:60], sorted(set(files) & set(ALL_PATHS)), (' WATCHED %s' % w) if w else ''))
    ctl = classify_pr({'title': 'x'}, [K['prs']['1445']['route_files'][0]]) == 'OVERLAP-CODE' and classify_pr({'title': 'y'}, ['a.ts']) == 'other' \
        and classify_pr({'title': 'z'}, [sorted(DOC_PATHS)[0]]) == 'OVERLAP-DOCS' and classify_pr({'title': 'KS-1410: q'}, []) == 'OVERLAP-CODE' \
        and watched(['x/check-shared-relink.sh']) and not watched(['x/y.ts'])
    print('CENSUS %d other open PR(s) (the four gate PRs excluded): %s | CONTROL fires %s' % (sum(cnt.values()), cnt, bool(ctl)))
    for r in rows: print(r)
    return 3 if not ctl else (1 if cnt.get('OVERLAP-CODE') else 0)


def scan(text): return sorted(set(re.findall(r'\bKS-\d+\b', text))), CLOSING.findall(text), FIXPREFIX.findall(text)


def refs_window(body, key):
    lines = body.split('\n'); hits = [i for i, l in enumerate(lines) if re.match(r'^\s*`?Refs %s\b' % re.escape(key), l)]
    bad = [i for i in hits for j in range(max(0, i - 3), i + 1) if CLOSING_WORD.search(lines[j])]
    return hits, bad


def attribution(body):
    return [l.strip() for l in body.split('\n') if re.search(r'Generated with|Co-Authored-By|Signed-off-by', l, re.I)]


def claims(body, ns, pr):
    """the PR text's figures vs measured/READY. Each: (id, hits-or-None, want, ok). A claim is OK when the WANT value is among the hits of its
    regex (a body can carry several `N passed` figures for different suites), ABSENT when no hit, MISMATCH when hits exist and the want is not one."""
    out = []
    def one(cid, rx, want):
        hits = [tuple(int(x.replace(',', '')) for x in g.groups()) for g in re.finditer(rx, body)]
        out.append((cid, hits or None, want, (not hits) or want in hits))
    adds, dels = sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values())
    one('CL-FILES', r'\b(\d+) (?:files|paths)\b[^.\n]{0,20}\+(\d+)\s*/\s*-(\d+)', (len(ns), adds, dels))
    if pr == '1443':
        one('CL-RED', r'Tests (\d+) failed \\\| (\d+) passed \((\d+)\)', (9, 6, 15)); one('CL-GREEN', r'GREEN\)[^\n]*?Tests (\d+) passed \((\d+)\)', (15, 15)); one('CL-WHOLE', r'whole api-gateway suite[^\n]*?Tests (\d+) passed \((\d+)\)', (860, 860))
        one('CL-FILES95', r'whole api-gateway suite[^\n]*?Test Files (\d+) passed \((\d+)\)', (95, 95)); one('CL-LINT', r'(\d+) problems, \*\*(\d+) errors\*\*', (36, 0)); one('CL-LINELEN', r'\*\*(\d+) characters\*\*', (299,))
        one('CL-EXPR-BYTES', r'\((\d+) bytes, `cmp` rc 0', (262,)); one('CL-SHELL', r'shell suites: (\d+) passed, (\d+) failed, (\d+) skipped', (73, 0, 0)); one('CL-LEGS', r'(\d+)/15 legs ran, (\d+) SKIPPED', (12, 3))
    elif pr == '1444':
        one('CL-BASE-ARM', r'base guard:\*\*[^\n]*?(\d+) passed / (\d+) failed', (108, 4)); one('CL-PAYLOAD-ARM', r'without the deviation:\*\*[^\n]*?(\d+) passed / (\d+) failed', (111, 1)); one('CL-HEAD-ARM', r'(\d+) passed, (\d+) failed, rc 0', (112, 0))
        one('CL-PROBES', r'(\d+) probe Dockerfiles', (32,)); one('CL-WIDEN-CONTROL', r'\| accepted by both \| (\d+) \|', (5,)); one('CL-WIDEN-NEW', r'\| newly accepted \| (\d+) \|', (9,))
        one('CL-WIDEN-STILL', r'\| refused by both \| (\d+) \|', (18,)); one('CL-WIDEN-NEWREF', r'\| newly refused \| (\d+) \|', (0,)); one('CL-66', r'\b(\d+) of (\d+)\.', (66, 66))
        one('CL-HTML', r'html_docs_matrix\.test\.sh`? (\d+) passed / (\d+) failed', (12, 0)); one('CL-SIB-CASE', r'check_shared_relink_case\.test\.sh` (\d+)/(\d+)', (6, 0)); one('CL-SIB-TOK', r'check_shared_relink_tooling_tokens\.test\.sh` (\d+)/(\d+)', (6, 0))
        one('CL-SIB-PREFLIGHT', r'preflight_deps\.test\.sh` (\d+)/(\d+)', (56, 0)); one('CL-SHELL', r'shell suites: (\d+) passed, (\d+) failed, (\d+) skipped', (73, 0, 0)); one('CL-SCRIPT-DIFF', r'\(\+(\d+)/-(\d+), committed 100755\)', (10, 2))
    elif pr == '1445':
        one('CL-SUITE-BASE', r'\*\*(\d+) passed \((\d+)\)\*\* at the base', (79, 79)); one('CL-SUITE-HEAD', r'\u2192 \*\*(\d+) passed \((\d+)\)\*\* after', (85, 85)); one('CL-RED', r'\*\*(\d+) failed / (\d+) passed of (\d+)\*\*', (4, 81, 85))
        one('CL-CELLS', r'\((\d+) found, (\d+) passed\)', (6, 6)); one('CL-HTML', r'\*\*(\d+) passed, (\d+) failed\*\*', (12, 0)); one('CL-SHELL', r'shell suites: (\d+) passed, (\d+) failed, (\d+) skipped', (73, 0, 0))
        one('CL-WHY-CHARS', r'one added line of (\d+) characters', (150,)); one('CL-TSC-FILES', r'showing \*\*(\d+)\*\* files', (427,)); one('CL-LEGS', r'(\d+)/15 legs ran, (\d+) SKIPPED', (12, 3))
    elif pr == '1446':
        one('CL-BASE-RED', r'\*\*base\*\* product[^\n]*?\*\*(\d+) failed / (\d+) passed\*\*', (6, 3)); one('CL-PAYLOAD-RED', r'payload\'s product[^\n]*?\*\*(\d+) failed / (\d+) passed\*\*', (1, 8)); one('CL-SUITE-BASE', r'suite, \*\*base\*\*[^\n]*?Tests (\d+) passed \((\d+)\)', (845, 845))
        one('CL-SUITE-HEAD', r'suite, \*\*head\*\*[^\n]*?Tests (\d+) passed \((\d+)\)', (854, 854)); one('CL-FILES-BASE', r'suite, \*\*base\*\*[^\n]*?Test Files (\d+) passed \((\d+)\)', (94, 94)); one('CL-FILES-HEAD', r'suite, \*\*head\*\*[^\n]*?Test Files (\d+) passed \((\d+)\)', (95, 95))
        one('CL-EXPR-BYTES', r'\*\*(\d+) bytes\*\*', (262,)); one('CL-LINT', r'(\d+) problems, \*\*(\d+) errors\*\*', (36, 0)); one('CL-HTML', r'`(\d+) passed, (\d+) failed`', (12, 0))
        one('CL-HOOKSUITES', r'pre_push_hook_base\.test\.sh` (\d+)/(\d+)', (28, 0)); one('CL-SHELL', r'shell suites: (\d+) passed, (\d+) failed, (\d+) skipped', (73, 0, 0))
    return out


def sentences(body):
    s = re.split(r'(?<=[.;:!?])\s+|\n+', body)
    return [x.strip() for x in s if x.strip() and re.search(r'\d|KS-|KS \d|`|webhook|format', x)]


def prtext(pn, head, repo, base, body_file, sent_out):
    P = PR(pn); KEY = P['ticket']
    if body_file:
        body = open(body_file, encoding='utf-8').read(); title = P['title_observed']; print('OFFLINE body from %s (title = the kit\'s observed PR title)' % body_file)
    else:
        pr = gh_get('pulls/%s' % P['pr']); body = pr.get('body') or ''; title = pr['title']
        if pr['head']['sha'] != head: print('REFUSED: API head %s != --head %s' % (pr['head']['sha'], head)); return 1
    keys, closing, fixp = scan(body + '\n' + title); hits, bad = refs_window(body, KEY)
    co = len(re.findall(r'(?im)^\s*(co-authored-by|signed-off-by):', body)); attr = attribution(body)
    print('BODY #%s sha256/16 %s, %d chars, %d utf8-bytes' % (P['pr'], hashlib.sha256(body.encode()).hexdigest()[:16], len(body), len(body.encode())))
    print('T1 `Refs %s` lines: %d at line(s) %s (want exactly 1) | T1b closing words on it or the 3 lines above: %s' % (KEY, len(hits), [i + 1 for i in hits], bad or 'none'))
    print('T2 closing references (title + body): %s | conventional fix(KS-n) form: %s' % (closing or 'none', fixp or 'none'))
    print('T3 hyphenated keys (title + body): %s -> only %s: %s' % (keys, KEY, keys == [KEY] or keys == []))
    design = title == P['subject'].replace('KS-', 'KS ', 1)   # the de-hyphenated form (#1444's title) vs the hyphenated one (#1443/#1445/#1446)
    print('T4 title %r (%d chars) vs commit subject %r (%d): equal %s; title == subject with the key de-hyphenated (the by-design difference): %s; title <= %d AS DECLARED: %s; "(#" in title: %s' % (
        title, len(title), P['subject'], len(P['subject']), title == P['subject'], design, P['subject_max'], len(title) <= P['subject_max'], '(#' in title))
    print('T5 trailer-shaped lines in the body: %d' % co)
    print('T5b attribution lines (count and report; gate77 Q-ATTR77 precedent): %d %s' % (len(attr), attr))
    ok = len(hits) == 1 and not bad and (keys == [KEY] or keys == []) and len(title) <= P['subject_max'] and '(#' not in title and co == 0
    ns = {}
    for l in subprocess.run(['git', '-C', repo, 'diff', '--numstat', base, head], capture_output=True, text=True).stdout.strip().split('\n'):
        a, dl, p = l.split('\t'); ns[p] = (int(a), int(dl))
    msg = subprocess.run(['git', '-C', repo, 'log', '-1', '--format=%B', head], capture_output=True, text=True).stdout
    for src, txt in (('BODY', body), ('COMMIT-MSG', msg)):   # each source on its own: a true commit message must not mask a wrong body
        for cid, stated, want, good in claims(txt, ns, P['pr']):
            st = 'OK      ' if (good and stated) else ('ABSENT  ' if not stated else 'MISMATCH')
            print('T6 %-10s %-16s %s stated %s | measured/READY %s' % (src, cid, st, stated, want))
            ok &= good
    ss = sentences(body)
    if sent_out: open(sent_out, 'w').write('\n'.join('%3d  %s' % (i + 1, x) for i, x in enumerate(ss)) + '\n')
    print('T7 %d factual-looking sentences written to %s for the sentence-by-sentence ruling' % (len(ss), sent_out or '(not written: give --sentences-out)'))
    if P['pr'] in ('1443', '1446'):
        sents = [x for x in re.split(r'(?<=[.])\s+|\n', body) if re.search(r'no longer leak|never logs|never leaks|does not leak|no secret', x, re.I)]
        print('T8 sentences in the body that claim the log no longer leaks / never logs values (the ruled expression still logs a thrown STRING and an Error .message verbatim): %s' % (sents or 'NONE FOUND'))
        print('T8b the body states the string / Error .message gap: %s' % bool(re.search(r'thrown \*\*?text|thrown \*\*`?string|thrown string|\.message', body, re.I)))
    if P['pr'] == '1445':
        print('T8 the body names the Q-4XX question (the four 4xx error.message sites): %s' % bool(re.search(r':85.*:208.*:211.*:213', body, re.S)))
    if P['pr'] == '1444':
        print('T8 the body names the measured `../node_modules` gap: %s | names that Docker was NOT run on `USER :root`: %s' % (bool(re.search(r'\.\./node_modules', body)), bool(re.search(r'whether Docker accepts|Docker builds|No probe Dockerfile was built', body))))
    return 0 if ok else 1


def linear_read(pn, comments_out):
    P = PR(pn); KEY = P['ticket']
    i, err = linear_issue(KEY)
    if not i: print('LINEAR %s not returned: %s' % (KEY, err)); return 1
    cs = i['comments']['nodes']; at = i['attachments']['nodes']
    print('LINEAR %s %r state %s (%s) updatedAt %s archivedAt %s comments %d attachments %d' % (
        i['identifier'], i['title'], i['state']['name'], i['state']['type'], i['updatedAt'], i['archivedAt'], len(cs), len(at)))
    newest = sorted(cs, key=lambda c: c['createdAt'])[-1]['id'][:8] if cs else None
    link = [c for c in cs if re.search(r'pull/%s\b' % P['pr'], c['body']) or ('#' + P['pr']) in c['body']]
    for c in cs: print('  COMMENT %s %s %d B sha256/16 %s names #%s: %s' % (c['id'][:8], c['createdAt'], len(c['body'].encode()), hashlib.sha256(c['body'].encode()).hexdigest()[:16], P['pr'], c in link))
    for a in at: print('  ATTACHMENT %s %r %s %s' % (a['id'][:8], a['title'], a['url'], a['createdAt']))
    print('  newest comment %s | PR attached: %s' % (newest, any(P['pr'] in (a.get('url') or '') for a in at)))
    if comments_out: open(comments_out, 'w').write('\n\n=====\n\n'.join('%s %s\n%s' % (c['id'], c['createdAt'], c['body']) for c in cs))
    ok = i['state']['name'] in K['linear_ok_states'] and not i['archivedAt'] and i['state']['type'] not in ('completed', 'canceled')
    print('VERDICT %s %s (want state in %s, not archived, NOT Done/Canceled: the ticket stays open) | a comment naming #%s: %d (Wednesday\'s batch: reported, not required)' % (
        KEY, 'OK' if ok else 'FINDING', K['linear_ok_states'], P['pr'], len(link)))
    return 0 if ok else 1


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    st = 'Audit-contract suites'
    nh = needles('##[group]x\n2026-10-10T00:30:00.1Z ##[error]Cannot find package \'semver\' imported from audit-locks.mjs\n')
    nd = needles('##[group]y\n2026-10-08T09:00:00.1Z ##[error]Cannot find package \'semver\' imported from audit-locks.mjs\n')
    v = classify_red([('Dependency Audit', [st], nh)], {'pr1434@d7ba337a8ef6': [('Dependency Audit', [st], nd)]})
    rep(v[0] == 'PRE-EXISTING' and nh['semver'] == 1 and nh['cannot_find'] == 1, 'classify (carried): same job + step + signature on another PR head -> PRE-EXISTING; KS-1148 evidence counters read semver 1, cannot-find 1')
    rep(classify_red([('Dependency Audit', [st], nh)], {})[0] == 'UNCLASSIFIED', 'PLANTED-RULE: no comparator -> UNCLASSIFIED, never pre-existing')
    rep(classify_red([('All shell test suites', ['Run'], needles('##[group]\n##[error]x\nks1410_delegations_process_expired FAIL'))], {'d': [('All shell test suites', ['Run'], needles('##[group]\n##[error]x'))]})[0] == 'UNCLASSIFIED',
        '[g81] PLANTED change needle (ks1410 suite name) in the failing log -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', [st], needles('##[error]x'))], {'d': [('Dependency Audit', [st], nd)]})[0] == 'UNCLASSIFIED', 'PLANTED unread head log (##[group] 0) -> UNCLASSIFIED')
    both = '##[group]\n##[error]x\nks1410 x1\nks1410 x2\n'
    rep(classify_red([('J', ['S'], needles(both))], {'d': [('J', ['S'], needles(both))]})[0] == 'PRE-EXISTING', '[g81] a change needle present at the SAME count in the matched comparator is NOT a signal (the log names it on develop too)')
    rep(classify_red([('J', ['S'], needles(both + 'ks1410 x3\n'))], {'d': [('J', ['S'], needles(both))]})[0] == 'UNCLASSIFIED', '[g81] PLANTED one extra change-needle line beyond the comparator -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', ['Other step'], nh)], {'d': [('Dependency Audit', [st], nd)]})[0] == 'UNCLASSIFIED', 'PLANTED different failing STEP -> UNCLASSIFIED (same job name is not enough)')
    a_ = needles('##[group]\nFAIL KS-1330: x got kill_to_exit=11s\n'); b_ = needles('##[group]\nFAIL KS-1330: x got kill_to_exit=12s\n'); c_ = needles('##[group]\nFAIL KS-1331: x got kill_to_exit=12s\n')
    rep(a_['signature'] == b_['signature'] and a_['signature'] != c_['signature'], '[g81] a run-to-run seconds figure (kill_to_exit=11s vs 12s) does not split a signature; a different failure id still does')
    rep(isinstance(_NoRedirect().redirect_request(None, None, 302, '', {}, 'u'), type(None)), 'the log opener does NOT follow the 302 with the auth header')
    wh = K['prs']['1445']['route_files'][0]; gs = K['prs']['1444']['gate_script']; doc = sorted(DOC_PATHS)[0]; au = K['prs']['1443']['route_files'][2]
    rep(classify_pr({'title': 'KS-1410 x'}, []) == 'OVERLAP-CODE' and classify_pr({'title': 'KS 937: x'}, []) == 'OVERLAP-CODE' and classify_pr({'title': 'KS-1346: x'}, []) == 'OVERLAP-CODE' and classify_pr({'title': 'x'}, [wh]) == 'OVERLAP-CODE'
        and classify_pr({'title': 'x'}, [gs]) == 'OVERLAP-CODE' and classify_pr({'title': 'x'}, [au]) == 'OVERLAP-CODE' and classify_pr({'title': 'x'}, [doc]) == 'OVERLAP-DOCS' and classify_pr({'title': 'x'}, ['q.ts']) == 'other',
        'census classifier: code (any of the four) / docs / other')
    rep(watched(['a/audit-export.ts', 'b/run-shell-suites.sh', 'c/x.ts']) == ['a/audit-export.ts', 'b/run-shell-suites.sh'], 'census WATCH list finds audit-export.ts / run-shell-suites.sh and not x.ts')
    k, c, f = scan('KS-937: x\nRefs KS-937. the KS 739 file; KS 697.'); rep(k == ['KS-937'], 'scan: de-hyphenated keys are not keys')
    k, c, f = scan('same shape as KS-1406. Refs KS-937'); rep(k == ['KS-1406', 'KS-937'], 'PLANTED hyphenated foreign key KS-1406 FIRES T3')
    rep(refs_window('a\nthis resolves it\nRefs KS-937', 'KS-937')[1] and not refs_window('Refs KS-937 https://x', 'KS-937')[1], 'closing word within 3 lines above Refs FIRES; clean passes')
    rep(attribution('x\n\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)\n') and not attribution('clean'), 'T5b attribution scanner sees the Generated-with line; clean reads 0')
    for n in K['go_prs']:
        body = open(os.path.join(HERE, 'predictions', 'prbodies', 'pr%s_body.txt' % n), encoding='utf-8').read() if os.path.isfile(os.path.join(HERE, 'predictions', 'prbodies', 'pr%s_body.txt' % n)) else None
        ns = dict((p_, tuple(v)) for p_, v in K['prs'][n]['numstat'].items())
        if body:
            cl = claims(body, ns, n); bad = [x[0] for x in cl if not x[3]]
            rep(sum(1 for x in cl if x[1]) >= 5, 'claims #%s over the REAL body (kit builder\'s saved copy): %d of %d claims FOUND; MISMATCHES (to read, not assumed): %s' % (n, sum(1 for x in cl if x[1]), len(cl), bad or 'none'))
    ns = dict((p_, tuple(v)) for p_, v in K['prs']['1445']['numstat'].items())
    tb = '**79 passed (79)** at the base \u2192 **85 passed (85)** after. **4 failed / 81 passed of 85**. (6 found, 6 passed) **12 passed, 0 failed** one added line of 150 characters showing **427** files'
    cl = claims(tb, ns, '1445'); rep(all(x[3] and x[1] for x in cl if x[0] not in ('CL-FILES', 'CL-SHELL', 'CL-LEGS')), 'claims #1445: a true text passes, each claim FOUND')
    rep(not all(x[3] for x in claims(tb.replace('79 passed (79)', '78 passed (78)'), ns, '1445')), 'PLANTED "78 passed (78)" vs the 79 FAILS')
    rep(not all(x[3] for x in claims(tb.replace('4 failed / 81 passed of 85', '3 failed / 82 passed of 85'), ns, '1445')), 'PLANTED "3 failed / 82 passed of 85" FAILS')
    ns = dict((p_, tuple(v)) for p_, v in K['prs']['1446']['numstat'].items())
    tb6 = '| new test, **base** product | **6 failed / 3 passed**\n| the payload\'s product | **1 failed / 8 passed**\n| suite, **base** | Tests 845 passed (845)\n| suite, **head** | Tests 854 passed (854)\n **262 bytes** 36 problems, **0 errors** `12 passed, 0 failed`'
    rep(all(x[3] and x[1] for x in claims(tb6, ns, '1446') if x[0] in ('CL-BASE-RED', 'CL-PAYLOAD-RED', 'CL-SUITE-BASE', 'CL-SUITE-HEAD', 'CL-EXPR-BYTES', 'CL-LINT', 'CL-HTML')), 'claims #1446: a true text passes, each claim FOUND (two "N failed / M passed" figures in one text do not collide)')
    rep(not all(x[3] for x in claims(tb6.replace('**262 bytes**', '**263 bytes**'), ns, '1446')), 'PLANTED "263 bytes" vs the measured 262 FAILS (the #1443 body says 263)')
    ns = dict((p_, tuple(v)) for p_, v in K['prs']['1444']['numstat'].items())
    tb4 = '| accepted by both | 5 | | newly accepted | 9 | | refused by both | 18 | | newly refused | 0 |\n- **Against the base guard:** rc 1, **108 passed / 4 failed**\n- **Against the payload without the deviation:** **111 passed / 1 failed**\n**112 passed, 0 failed, rc 0** 32 probe Dockerfiles 66 of 66.'
    rep(all(x[3] and x[1] for x in claims(tb4, ns, '1444') if x[0] in ('CL-WIDEN-CONTROL', 'CL-WIDEN-NEW', 'CL-WIDEN-STILL', 'CL-WIDEN-NEWREF', 'CL-BASE-ARM', 'CL-PAYLOAD-ARM', 'CL-HEAD-ARM', 'CL-PROBES', 'CL-66')), 'claims #1444: a true text passes, each claim FOUND')
    rep(not all(x[3] for x in claims(tb4.replace('| newly accepted | 9 |', '| newly accepted | 10 |'), ns, '1444')), 'PLANTED widen "newly accepted 10" vs 9 FAILS')
    ns = dict((p_, tuple(v)) for p_, v in K['prs']['1443']['numstat'].items())
    rep(not all(x[3] for x in claims('GREEN) | `Tests 14 passed (14)`', ns, '1443')), 'PLANTED #1443 "Tests 14 passed (14)" (the claim is 15) FAILS')
    rep(any(x[1] is None for x in claims('nothing numeric', ns, '1443')), 'an absent claim reads ABSENT, never OK')
    rep(line_n('a\nb\nc', 2) == 'b' and line_n('a', 5) is None, 'line_n reads line 2 and returns None past the end (the audit CONTROL)')
    try: PR(1441); rep(False, '--pr 1441 (gate80\'s PR) ACCEPTED')
    except SystemExit: rep(True, 'WRONG-PR ARM --pr 1441 (gate80\'s PR) -> refused')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if not A: print(__doc__); return 2
    try:
        if A[0] == '--selftest': return selftest()
        if A[0] == 'audit':
            return audit(req(A, '--repo'), req(A, '--base', True), dict((n, req(A, '--head' + n, True)) for n in K['go_prs']), opt(A, '--reference'))
        if A[0] == 'census': return census()
        n = req(A, '--pr'); P = PR(n)
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
        if A[0] == 'prtext':
            return prtext(P['pr'], req(A, '--head', True), req(A, '--repo'), req(A, '--base', True), opt(A, '--body-file'), opt(A, '--sentences-out'))
        if A[0] == 'linear': return linear_read(P['pr'], opt(A, '--comments-out'))
    except SystemExit as e:
        print(e); return 2
    except (OSError, ValueError, urllib.error.URLError, KeyError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
