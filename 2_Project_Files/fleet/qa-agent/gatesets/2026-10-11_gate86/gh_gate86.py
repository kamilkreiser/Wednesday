#!/usr/bin/env python3
"""gh_gate86.py — GitHub / Linear READ-ONLY instruments for gate86 (a TIER-2 BATCH of FOUR PRs: #1451 #1452 #1454 #1455). REST GETs + Linear GraphQL reads; tokens BY NAME, never printed. The Actions
machinery (log fetch without the auth header on the 302, the failure SIGNATURE, comparators BY WORKFLOW PATH, the planted develop-only rule) is CARRIED from gh_gate85.py; [g86] marks this kit's
changes. EVERY PIN IS REQUIRED; every PR command takes --pr N with N in 1451 1452 1454 1455 (a foreign number is refused).

  api       --pr N --head H [--body-out F]   head / branch / base / state / merged / mergeable / mergeable_state, body sha256/16 vs the kit's pin (EQUAL / EDITED), chars AND bytes; rc 1 unless head == H,
            open, unmerged, base develop. [g86] the live bodies are the builders' bodies (Test Evidence written by Seats F 12th / 13th / 15th / 16th): the row says EQUAL or EDITED against the kit pin.
  actions   --pr N --at H --develop D [--out DIR] [--wait MIN]   CLASSIFIED BY WORKFLOW PATH (see gh_gate83): X0 / A1..A4. PRE-EXISTING only with a comparator covering the head's signature AND no change
            needle beyond the comparator's count; else UNCLASSIFIED (BLOCKS). Absent expected workflows are named NOT RUN. Runs still in progress are PENDING, never green.
  audit     --repo R --base1451 B .. --head1451 H ..   KS-1148 attribution, READ half, for all four PRs (bases differ per PR).
  census    every OTHER open PR: OVERLAP-CODE (touches a non-doc non-yaml path of the four, or is titled with one of the four keys) / OVERLAP-YAML (touches the shared yaml) / OVERLAP-DOCS (only the two docs) /
            other; names every PR touching a WATCHED path (stack_env.sh, dev-reload.sh, env.example, *.openapi.ts, generate-openapi, ...). CONTROL: fabricated rows classify.
  prtext    --pr N --head H [--body-file F] [--sentences-out F]   T1 exactly one `Refs KS-n` line, no closing word on it or the 3 lines above  T3 only the PR's own key hyphenated  T4 title vs the kit's declared
            subject  T5 attribution lines COUNTED (gate77 Q-ATTR77)  T7 every factual sentence -> --sentences-out  T8 per-PR REQUIRED scoping words (UNVERIFIED / PARTIAL / deviation) and FORBIDDEN phrases
            (closing words before a key, "unchanged"). [g86] NO per-figure claim table and NO push-log check: this batch has no per-PR figure pin file; the gate reads the Test Evidence sentence by sentence.
  linear    --pr N [--key KS-nnn]   state, archivedAt, updatedAt, comments (count, newest), attachments naming the PR. The ticket must stay OPEN.
  --selftest
rc 0 / 1 (finding, blind control, OVERLAP-CODE, UNCLASSIFIED, PENDING, NOT RUN) / 2 refused / 3 API failure."""
import sys, os
import hashlib, json, os, re, subprocess, sys, time, urllib.error, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate86 import K, PR, gh_get, gh_pages, linear_issue, env_value, req, opt, git, show, resolvable

HERE = os.path.dirname(os.path.abspath(__file__))
AC = K['actions']
FAILING = ('failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required')
CLOSING = re.compile(K['closing_rx'], re.I)
CLOSING_WORD = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\b', re.I)
FIXPREFIX = re.compile(r'\b(fix|close|resolve|complete)[a-z]*\(\s*KS-\d+\s*\)', re.I)
ALL_PATHS = {}
for _n, _p in K['prs'].items():
    for _x in _p['paths']: ALL_PATHS.setdefault(_x, []).append(_n)
DOC_PATHS = set(K['known_develop_overlap']); YAML = K['shared_yaml']
CODE_PATHS = set(ALL_PATHS) - DOC_PATHS - {YAML}
WATCH = ['stack_env.sh', 'dev-reload.sh', 'env.example', 'env.local.example', 'bootstrap-env', 'generate-openapi', '.openapi.ts', 'secuura-api.yaml', 'html_docs_matrix', 'run-shell-suites']



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
SHELLTOT = re.compile(r'shell suites: \d+ passed, (\d+) failed, \d+ skipped \(of \d+\)')
INFRA = re.compile(r'(Bad Gateway|\b50[234]\b|toomanyrequests|rate limit|TLS handshake|ECONNRESET|i/o timeout|no space left)', re.I)


def norm(l):
    # [g81] a measured-seconds figure (`kill_to_exit=11s` vs `12s`) is run-to-run timing, not a different failure.
    # [g86] the shell-suite TOTALS line keeps only its FAILED count: every gate84 PR ADDS one passing shell suite, so `69 passed (of 74)` becomes `70 passed (of 75)` with the same
    # 5 failed; a different failed count still splits the signature.
    return SHELLTOT.sub(lambda m: 'shell suites: <N> passed, %s failed, <N> skipped (of <N>)' % m.group(1), SECS.sub('=<N>s', DUR.sub('', TS.sub('', l).strip())))


def signature(text):
    # [g86] a line that PASSES (`PASS: ...`, `ok ...`) is never a failure signature even when its text says "failed" (a control cell describing a failed run)
    return sorted(set(n for n in (norm(l) for l in text.split('\n')) if SIG.search(n) and not n.startswith(('PASS', 'ok '))))


def needles(text):
    lines = text.split('\n'); sig = signature(text)
    # [g86] a CHANGE needle counts only on a FAILURE-SIGNATURE line: the runner prints every suite it runs, so a PR that ADDS a suite names itself in the log (passing).
    ch = dict((n, sum(1 for l in sig if n in l)) for n in AC['needles_change'])
    return {'signature': sig, 'bytes': len(text.encode()), 'positive_group': text.count(AC['positive_control']),
            'change': ch, 'change_lines': [norm(l)[:200] for l in lines if any(n in l for n in AC['needles_change'])][:6],
            'change_anywhere': dict((n, text.count(n)) for n in AC['needles_change'] if text.count(n)),
            'infra_hints': [norm(l)[:200] for l in lines if INFRA.search(l)][:3],
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
        print('  JOB %-30s failing steps %s | log %d B, ##[group] %d, signature lines %d, change needles ON SIGNATURE LINES %s (anywhere in the log %s), fabricated %d | KS-1148 evidence: `semver` x%d, cannot-find x%d' % (
            j['name'], steps, n['bytes'], n['positive_group'], len(n['signature']), dict((k, v) for k, v in n['change'].items() if v) or 0, n['change_anywhere'] or 0, n['fabricated'], n['semver'], n['cannot_find']))
        for x in n['change_lines']: print('      CHANGE-NEEDLE LINE (anywhere in the log) %s' % x)
        for x in n['signature'][:10]: print('      SIG %s' % x[:200])
        for x in n['infra_hints']: print('      INFRA-HINT (a hint to READ, never an auto-attribution) %s' % x)
    return res


def classify_red(head_jobs, comp_jobs):
    """-> (verdict, why, matched comparator labels). comp_jobs: {label: [(job, steps, needles)]} read by THIS tool.
    [g86] a CHANGE needle (a token of THESE changes, e.g. `format:check`) is a signal only where the head's count EXCEEDS the count in every
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


def audit(repo, bases, heads, ref):
    A = K['audit_locks']; rc = 0
    revs = [('base' + n, b) for n, b in sorted(bases.items())] + [('head' + n, h) for n, h in sorted(heads.items())] + ([('reference', ref)] if ref else [])
    seen = set()
    for lab, rev in revs:
        if not resolvable(repo, rev): print('AUDIT %-9s %s NOT IN THE STORE (fetch BY SHA into your clone, X7): NOT READ' % (lab, rev[:12])); rc = 1; continue
        txt = show(repo, rev, A['path']); l = line_n(txt, A['line'])
        print('AUDIT %-9s %s %s:%d = %r | carries %s: %s%s' % (lab, rev[:12], A['path'].split('/')[-1], A['line'], l, A['needle'], bool(l and A['needle'] in l), ' (same commit as an earlier row)' if rev in seen else ''))
        seen.add(rev)
        if not (l and A['needle'] in l): rc = 1
    ctl = line_n(show(repo, next(iter(bases.values())), A['path']), 99999)
    print('AUDIT CONTROL: the same reader on line 99999 returns %r (must be None)' % ctl); rc |= 0 if ctl is None else 1
    for n in K['go_prs']:
        ns = set(PR(n)['paths']); hit = sorted(p for p in ns if p == A['path'] or p.endswith('package.json') or p.endswith('package-lock.json'))
        print('AUDIT #%s touches audit-locks.mjs / a manifest / a lock: %s' % (n, hit or 'NONE')); rc |= 1 if hit else 0
    return rc


def scan(text): return sorted(set(re.findall(r'\bKS-\d+\b', text))), CLOSING.findall(text), FIXPREFIX.findall(text)


def refs_window(body, key):
    lines = body.split('\n'); hits = [i for i, l in enumerate(lines) if re.match(r'^\s*`?Refs %s\b' % re.escape(key), l)]
    bad = [i for i in hits for j in range(max(0, i - 3), i + 1) if CLOSING_WORD.search(lines[j])]
    return hits, bad


def attribution(body):
    return [l.strip() for l in body.split('\n') if re.search(r'Generated with|Co-Authored-By|Signed-off-by', l, re.I)]


REQUIRED = {  # per-PR scoping words the body must carry (the seats' own caveats; absence is a finding, presence is not proof)
    '1451': [('UNVERIFIED handler behaviour', r'UNVERIFIED|UNMEASURED'), ('declares, does not enforce', r'(?i)declare|spec only')],
    '1452': [('UNVERIFIED handler behaviour', r'UNVERIFIED|UNMEASURED'), ('declares, does not enforce', r'(?i)declare|spec only')],
    '1454': [('PARTIAL for the ticket', r'(?i)partial|one of the two scripts'), ('live run owed', r'(?i)live run|UNMEASURED')],
    '1455': [('piece 2', r'(?i)piece 2|second piece'), ('declared deviation', r'(?i)deviation|differs from the (spark )?payload'), ('fresh-clone bootstrap owed', r'(?i)fresh[- ]clone|UNMEASURED')]}
FORBIDDEN = [('"unchanged" as a claim of behaviour', r'(?i)\bbehaviou?r(?:s)? (?:is |are )?unchanged\b|\bunchanged behaviou?r\b'), ('closing word before a key', None)]


def sentences(body):
    out = []
    for blk in re.split(r'(?m)\n\s*\n|^\s*[-*|#]+\s*', body):
        for s in re.split(r'(?<=[.!?])\s+', re.sub(r'\s+', ' ', blk).strip()):
            if len(s) > 25 and re.search(r'\d', s): out.append(s)
    return out


def prtext(n, head, body_file, sent_out):
    P = PR(n); t_ok = True
    if body_file: body = open(body_file, encoding='utf-8').read()
    else:
        pr = gh_get('pulls/%s' % n); body = pr.get('body') or ''
        if pr['head']['sha'] != head: print('FAIL T0 the live head %s != --head %s' % (pr['head']['sha'][:12], head[:12])); return 1
    keys, closing, fixp = scan(body); hits, bad = refs_window(body, P['ticket']); rows = []
    def row(cid, ok, msg):
        nonlocal t_ok; t_ok = t_ok and ok; print('%s %s %s' % ('PASS' if ok else 'FAIL', cid, msg))
    row('T1', len(hits) == 1 and not bad, '`Refs %s` lines in the body: %d (want 1); a closing word within 3 lines above: %d' % (P['ticket'], len(hits), len(bad)))
    row('T3', set(keys) <= {P['ticket']}, 'hyphenated keys in the body: %s (want only %s; a foreign hyphenated key ATTACHES)' % (keys, P['ticket']))
    row('T3-CONTROL', scan('same shape as KS-9999 here')[0] == ['KS-9999'] and scan('the de-hyphenated KS 9999')[0] == [], 'CONTROL: the key scanner reads a planted hyphenated foreign key and ignores a de-hyphenated one')
    row('T3b', not closing and not fixp, 'closing-family words directly before a key / number: %s %s' % (closing[:3], fixp[:3]))
    row('T4', len(P['title']) <= 92 and P['title'] == P['subject'], 'title == the kit subject (%d chars): %r' % (len(P['title']), P['title'][:90]))
    at = attribution(body); print('INFO T5b attribution lines in the body: %d %s (counted, not ruled: gate77 Q-ATTR77)' % (len(at), [a[:60] for a in at]))
    for lab, rx in REQUIRED[n]: row('T8-REQ', bool(re.search(rx, body)), 'REQUIRED scoping: %s' % lab)
    for lab, rx in FORBIDDEN:
        if rx: row('T8-FORB', not re.search(rx, body), 'FORBIDDEN phrase absent: %s' % lab)
    row('T8-CONTROL', bool(re.search(FORBIDDEN[0][1], body + '\nthe behaviour is unchanged.')) and not re.search(REQUIRED[n][0][1], 'nothing here'), 'CONTROL: the forbidden detector fires on a planted sentence and the required detector fails on an empty text')
    ss = sentences(body); print('INFO T7 factual-looking sentences (with a digit): %d%s' % (len(ss), ' -> ' + sent_out if sent_out else ''))
    if sent_out: open(sent_out, 'w').write('\n'.join(ss) + '\n')
    sh = hashlib.sha256(body.encode()).hexdigest()[:16]; print('INFO T9 body sha256/16 %s vs the kit pin %s: %s' % (sh, P['body_sha256_16'], 'EQUAL' if sh == P['body_sha256_16'] else 'EDITED SINCE THE KIT'))
    return 0 if t_ok else 1


def linear_read(pn, comments_out, key=None):
    P = PR(pn); KEY = key or P['ticket']
    i, err = linear_issue(KEY)
    if not i: print('LINEAR %s not returned: %s' % (KEY, err)); return 1
    cs = i['comments']['nodes']; at = i['attachments']['nodes']
    print('LINEAR %s %r state %s (%s) updatedAt %s archivedAt %s comments %d attachments %d' % (i['identifier'], i['title'], i['state']['name'], i['state']['type'], i['updatedAt'], i['archivedAt'], len(cs), len(at)))
    newest = sorted(cs, key=lambda c: c['createdAt'])[-1]['id'][:8] if cs else None
    link = [c for c in cs if re.search(r'pull/%s\b' % P['pr'], c['body']) or ('#' + P['pr']) in c['body']]
    if key: print('  (a RELATED ticket read, not a gate ticket: its state is reported, not judged)')
    for c in cs: print('  COMMENT %s %s %d B sha256/16 %s names #%s: %s' % (c['id'][:8], c['createdAt'], len(c['body'].encode()), hashlib.sha256(c['body'].encode()).hexdigest()[:16], P['pr'], c in link))
    for a in at: print('  ATTACHMENT %s %r %s %s' % (a['id'][:8], a['title'], a['url'], a['createdAt']))
    print('  newest comment %s | PR attached: %s' % (newest, any(P['pr'] in (a.get('url') or '') for a in at)))
    if comments_out: open(comments_out, 'w').write('\n\n=====\n\n'.join('%s %s\n%s' % (c['id'], c['createdAt'], c['body']) for c in cs))
    ok = key is not None or (i['state']['name'] in K['linear_ok_states'] and not i['archivedAt'] and i['state']['type'] not in ('completed', 'canceled'))
    print('VERDICT %s %s (want state in %s, not archived, NOT Done/Canceled: the ticket stays open) | a comment naming #%s: %d (Wednesday\'s batch: reported, not required)' % (KEY, 'OK' if ok else 'FINDING', K['linear_ok_states'], P['pr'], len(link)))
    return 0 if ok else 1


def classify_pr(pr_row, files):
    t = pr_row.get('title') or ''; fs = set(files)
    if any(re.search(r'KS[- ]%s\b' % k.split('-')[1], t) for k in {p['ticket'] for p in K['prs'].values()}) or fs & CODE_PATHS: return 'OVERLAP-CODE'
    if YAML in fs: return 'OVERLAP-YAML'
    if fs & DOC_PATHS: return 'OVERLAP-DOCS'
    return 'other'


def watched(files): return sorted(f for f in files if any(w in f for w in WATCH))


def census():
    prs = gh_pages('pulls?state=open'); rows, cnt = [], {}
    for pr in prs:
        if str(pr['number']) in K['prs']: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % pr['number'])]
        c = classify_pr(pr, files); cnt[c] = cnt.get(c, 0) + 1; w = watched(files)
        if c != 'other' or w: rows.append('  %s #%d %s %s shared %s%s' % (c, pr['number'], pr['head']['sha'][:12], pr['title'][:60], sorted(x.split('/')[-1][:28] for x in set(files) & set(ALL_PATHS)), (' WATCHED %s' % [x.split('/')[-1][:30] for x in w][:4]) if w else ''))
    code1 = sorted(CODE_PATHS)[0]
    ctl = (classify_pr({'title': 'x'}, [code1]) == 'OVERLAP-CODE' and classify_pr({'title': 'y'}, ['a.ts']) == 'other' and classify_pr({'title': 'z'}, [sorted(DOC_PATHS)[0]]) == 'OVERLAP-DOCS'
           and classify_pr({'title': 'KS-1417: q'}, []) == 'OVERLAP-CODE' and classify_pr({'title': 'KS 591 q'}, []) == 'OVERLAP-CODE' and classify_pr({'title': 'x'}, [YAML]) == 'OVERLAP-YAML'
           and watched(['x/scripts/stack_env.sh']) and not watched(['x/y.ts']))
    print('CENSUS %d other open PR(s) (the four gated PRs excluded): %s | CONTROL fires %s' % (sum(cnt.values()), cnt, bool(ctl)))
    for r in rows: print(r)
    return 3 if not ctl else (1 if cnt.get('OVERLAP-CODE') else 0)


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    st = 'Audit-contract suites'
    nh = needles('##[group]x\n2026-10-10T00:30:00.1Z ##[error]Cannot find package \'semver\' imported from audit-locks.mjs\n')
    nd = needles('##[group]y\n2026-10-08T09:00:00.1Z ##[error]Cannot find package \'semver\' imported from audit-locks.mjs\n')
    rep(classify_red([('Dependency Audit', [st], nh)], {'pr1447@68a20b9bd374': [('Dependency Audit', [st], nd)]})[0] == 'PRE-EXISTING' and nh['semver'] == 1, 'classify (carried): same job + step + signature on another PR head -> PRE-EXISTING; KS-1148 counters read')
    rep(classify_red([('Dependency Audit', [st], nh)], {})[0] == 'UNCLASSIFIED', 'PLANTED-RULE: no comparator -> UNCLASSIFIED, never pre-existing')
    rep(classify_red([('All shell test suites', ['Run'], needles('##[group]\n##[error]x\nks1355 FAIL'))], {'d': [('All shell test suites', ['Run'], needles('##[group]\n##[error]x'))]})[0] == 'UNCLASSIFIED', '[g86] PLANTED change needle (ks1355) in the failing log -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', [st], needles('##[error]x'))], {'d': [('Dependency Audit', [st], nd)]})[0] == 'UNCLASSIFIED', 'PLANTED unread head log (##[group] 0) -> UNCLASSIFIED')
    both = '##[group]\n##[error]x\nFAIL ks1417 x1\nFAIL ks1417 x2\n'
    rep(classify_red([('J', ['S'], needles(both))], {'d': [('J', ['S'], needles(both))]})[0] == 'PRE-EXISTING', 'a change needle at the SAME count in the matched comparator is NOT a signal')
    rep(classify_red([('J', ['S'], needles(both + 'FAIL ks1417 x3\n'))], {'d': [('J', ['S'], needles(both))]})[0] == 'UNCLASSIFIED', 'PLANTED one extra FAILING line naming a change needle beyond the comparator -> UNCLASSIFIED')
    named = '##[group]\n##[error]x\nks1355_dev_reload: 7 passed, 0 failed\n'
    rep(needles(named)['change']['ks1355'] == 0 and needles(named)['change_anywhere'].get('ks1355') == 1, 'a PASSING line that names the PR\'s own test is NOT a change-needle signal')
    a_t = '##[group]\nshell suites: 69 passed, 5 failed, 0 skipped (of 74)\n##[error]x\n'; b_t = '##[group]\nshell suites: 70 passed, 5 failed, 0 skipped (of 75)\n##[error]x\n'; c_t = '##[group]\nshell suites: 69 passed, 6 failed, 0 skipped (of 75)\n##[error]x\n'
    rep(signature(a_t) == signature(b_t) and signature(a_t) != signature(c_t), 'the shell-suite TOTALS line keeps only its FAILED count')
    rep(isinstance(_NoRedirect().redirect_request(None, None, 302, '', {}, 'u'), type(None)), 'the log opener does NOT follow the 302 with the auth header')
    doc = sorted(DOC_PATHS)[0]; code1 = sorted(CODE_PATHS)[0]
    rep(classify_pr({'title': 'KS-1417 x'}, []) == 'OVERLAP-CODE' and classify_pr({'title': 'KS 1355: x'}, []) == 'OVERLAP-CODE' and classify_pr({'title': 'x'}, [code1]) == 'OVERLAP-CODE'
        and classify_pr({'title': 'x'}, [YAML]) == 'OVERLAP-YAML' and classify_pr({'title': 'x'}, [doc]) == 'OVERLAP-DOCS' and classify_pr({'title': 'x'}, ['q.ts']) == 'other', 'census classifier: code / yaml / docs / other')
    rep(watched(['a/scripts/stack_env.sh', 'b/x.openapi.ts', 'c/x.ts']) == ['a/scripts/stack_env.sh', 'b/x.openapi.ts'], 'census WATCH list finds stack_env.sh / *.openapi.ts and not x.ts')
    k, c, f = scan('KS-591: x\nRefs KS-591. the KS 808 file; KS 1031.'); rep(k == ['KS-591'], 'scan: de-hyphenated keys are not keys')
    k, c, f = scan('same shape as KS-1406. Refs KS-591'); rep(k == ['KS-1406', 'KS-591'], 'PLANTED hyphenated foreign key KS-1406 FIRES T3')
    rep(refs_window('a\nthis resolves it\nRefs KS-591', 'KS-591')[1] and not refs_window('Refs KS-591 https://x', 'KS-591')[1], 'closing word within 3 lines above Refs FIRES; clean passes')
    rep(attribution('x\n\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)\n') and not attribution('clean'), 'T5b attribution scanner sees the Generated-with line; clean reads 0')
    rep(len(sentences('Plain words only here without digits at all in this one sentence.')) == 0 and len(sentences('The suite goes from 77 to 78 shell suites after the change.')) == 1, 'sentences() keeps only factual-looking (digit) sentences')
    rep(line_n('a\nb\nc', 2) == 'b' and line_n('a', 5) is None, 'line_n reads line 2 and returns None past the end (the audit CONTROL)')
    for foreign in (1441, 1443, 1444, 1446, 1447, 1448, 1449, 1450, 1453):
        try: PR(foreign); rep(False, '--pr %s ACCEPTED' % foreign)
        except SystemExit: rep(True, 'WRONG-PR ARM --pr %s (not a gated PR) -> refused' % foreign)
    for good in (1451, 1452, 1454, 1455): rep(PR(good)['pr'] == str(good), '--pr %s accepted' % good)
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if not A: print(__doc__); return 2
    try:
        if A[0] == '--selftest': return selftest()
        if A[0] == 'audit':
            return audit(req(A, '--repo'), dict((n, req(A, '--base' + n, True)) for n in K['go_prs']), dict((n, req(A, '--head' + n, True)) for n in K['go_prs']), opt(A, '--reference'))
        if A[0] == 'census': return census()
        n = req(A, '--pr'); P = PR(n)
        if A[0] == 'api':
            head = req(A, '--head', True); pr = gh_get('pulls/%s' % P['pr']); b = pr.get('body') or ''
            if opt(A, '--body-out'): open(opt(A, '--body-out'), 'w').write(b)
            sh = hashlib.sha256(b.encode()).hexdigest()[:16]
            print('API #%s head %s branch %s base %s state %s merged %s mergeable %s mergeable_state %s draft %s' % (P['pr'], pr['head']['sha'], pr['head']['ref'], pr['base']['ref'], pr['state'], pr['merged'], pr.get('mergeable'), pr.get('mergeable_state'), pr.get('draft')))
            print('BODY sha256/16 %s chars %d utf8-bytes %d | kit pin %s: %s | title %r (%d) | commits %s +%s/-%s files %s | updated %s' % (
                sh, len(b), len(b.encode()), P['body_sha256_16'], 'EQUAL' if sh == P['body_sha256_16'] else 'EDITED SINCE THE KIT (read the new body: prtext)', pr['title'], len(pr['title']), pr.get('commits'), pr.get('additions'), pr.get('deletions'), pr.get('changed_files'), pr['updated_at']))
            return 0 if pr['head']['sha'] == head and pr['state'] == 'open' and not pr['merged'] and pr['base']['ref'] == 'develop' else 1
        if A[0] == 'actions':
            w = opt(A, '--wait')
            return actions(req(A, '--at', True), req(A, '--develop', True), opt(A, '--out'), int(w) if w else 0)
        if A[0] == 'prtext': return prtext(P['pr'], req(A, '--head', True), opt(A, '--body-file'), opt(A, '--sentences-out'))
        if A[0] == 'linear': return linear_read(P['pr'], opt(A, '--comments-out'), opt(A, '--key'))
    except SystemExit as e:
        print(e); return 2
    except (OSError, ValueError, urllib.error.URLError, KeyError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
