#!/usr/bin/env python3
"""gh_gate78.py — GitHub / Linear READ-ONLY instruments for gate78 (#1435, KS-1452). REST GETs + Linear GraphQL reads; tokens BY NAME,
never printed. Carried from gh_gate72.py; [g78] marks this kit's changes. EVERY PIN IS A REQUIRED ARGUMENT.

  api       --head H [--body-out F]   `API #1435 head <sha> branch <ref> base <ref> state <s> merged <b> mergeable <m> mergeable_state <ms>`,
            body sha256/16, chars AND utf-8 bytes; rc 1 unless head == H, open, unmerged, base develop.
  actions   --at H --develop D [--out DIR] [--wait MIN]     [g78] CLASSIFIED BY WORKFLOW PATH, never by a develop-only rule
            X0 runs exist at the FULL head sha; CONTROL a fabricated sha reads 0 runs
            A1 every workflow PATH at H: event / status / conclusion; PENDING named (never a pass); --wait polls every 60 s up to MIN minutes
               until nothing is pending (two agreeing reads)
            A2 for EVERY failing run at H: the failing jobs + steps, and each job LOG fetched by this tool (the 302 to the signed URL followed
               WITHOUT the Authorization header: an unfetched log reads as zero). Per log: bytes, POSITIVE control `##[group]` count (0 = the
               log was NOT READ -> NOT RUN), the failure SIGNATURE (error lines, timestamps and durations stripped), the CHANGE needles
               (handlebars, the three GHSA short ids, minimist) with the first lines carrying them, a FABRICATED needle (must be 0)
            A3 COMPARATORS, per path: (i) develop D's own run of the SAME path, if the workflow has one (pr-security-gates.yml and
               pr-platform-suites.yml trigger on push to develop); (ii) when D has NO run of that path (security-scan.yml triggers on
               pull_request + workflow_dispatch only — read at develop), the newest completed failing pull_request runs of the SAME path on
               OTHER heads (up to 2). The tool says which kind each comparator is and why.
            A4 history: the last 12 completed runs of each red path (any branch): conclusions counted
            CLASSIFY per red path: PRE-EXISTING only if (log read at H, ##[group] > 0) AND (a comparator, read here, shows the same failing
            job + step set with a failure signature COVERING the head's) AND (0 change needles in the head's failing logs). Else
            UNCLASSIFIED (the gate rules it BLOCKING). PLANTED-RULE CONTROL printed beside it: what a DEVELOP-ONLY classifier would say (for a
            path with no develop run it must say NEW — the gate76 lesson, made visible, never used to decide).
  census    every OTHER open PR touching any of the 5 paths or titled KS-1452 = OVERLAP; CONTROL: a fabricated row on a lock classifies OVERLAP.
  prtext    --head H --measured c2.json --reach c6.json --tar c3.json [--legs-head DIR] [--repo CLONE --base B] [--body-file F] [--sentences-out F]
            T1 exactly one `Refs KS-1452` line; T1b no closing-family word on it or the 3 lines above   T2 0 closing words before a key / #n
            T3 only KS-1452 hyphenated (title + body); T3b [g78] the sibling KS-1453 named UNHYPHENATED only (>= 1)   T4 title == the commit
            subject; squash <= 92   T5 0 trailer lines   T5b [g78] attribution lines (`Generated with`, `Co-Authored-By`) COUNTED and quoted —
            a finding for the gate to rule (gate77 Q-ATTR77 precedent), not a T-fail   T6 the body's numbers vs MEASURED (c2 / c3 / c6 /
            numstat / the head legs when --legs-head is given)   T7 every sentence carrying a digit, a version or an id -> --sentences-out
  linear    [g78] KS-1452: state In Progress, not archived, >= 1 comment linking PR #1435 (bodies to --comments-out, sha256/16 each), its
            attachments (the integration's PR link). KS-1453 (the sibling, filed NOT built): state Backlog, not archived, 0 attachments naming
            #1435 (the unhyphenated mention did not link it), its comments counted. Read-only.
  --selftest  the classifier (path comparators, develop-only planted rule), the redirect-without-auth opener, the key / closing /
              attribution scanners, the claims comparator.
rc 0 / 1 (finding, blind control, OVERLAP, UNCLASSIFIED, PENDING, NOT RUN) / 2 refused / 3 API failure."""
import hashlib, json, os, re, subprocess, sys, time, urllib.error, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate78 import K, gh_get, gh_pages, linear_issue, env_value, req, opt

P = K['pr']; KEY = P['ticket']; SIB = P['sibling_ticket']; AC = K['actions']
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
    print('NOTE: CI `Dependency Audit` (security-scan.yml) runs the audit gates\' own VALIDATOR suite in a CI checkout — a different instrument from the in-hook legs 6 / 7.')
    ok = x0 and not pend and all(v == 'PRE-EXISTING' for v in verdicts.values())
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


def attribution(body):
    return [l.strip() for l in body.split('\n') if re.search(r'Generated with|Co-Authored-By|Signed-off-by', l, re.I)]


def sibling(body):
    n = SIB.split('-', 1)[1]
    return len(re.findall(r'\bKS-%s\b' % n, body)), len(re.findall(r'\bKS %s\b' % n, body))


def claims(body, m, r, tar, ns, legs):
    out = []
    def one(cid, rx, want):
        hits = [tuple(int(x.replace(',', '')) for x in g.groups()) for g in re.finditer(rx, body)]
        if want is None: out.append((cid, hits or None, 'NOT MEASURED HERE', True)); return
        out.append((cid, hits or None, want, (not hits) or all(h == want for h in hits)))
    one('CL-SET', r'(\d+) locks, (\d+) entries, (\d+) field writes', (m['locks'], m['entries'], m['field_writes']))
    one('CL-PARENTS', r'all (\d+) declaring parents', (m['declaring_parents'],))
    one('CL-TRACKED', r'over all (\d+) tracked locks', (m['tracked_locks'],))
    one('CL-TARBALL', r'tarball \(([\d,]+) B\)', (tar['bytes'].get('handlebars@4.7.10'),) if tar else None)
    one('CL-LITERAL', r'control: `package-lock\.json` (\d+)', (r['lockfile_literal'],))
    one('CL-EXPRESS', r'express (\d+)', (r['express'],))
    one('CL-SHORTSTAT', r'(\d+) files changed, (\d+) insertions\(\+\), (\d+) deletions', (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values())))
    one('CL-LEG6', r'audit-gate: (\d+) distinct advisories reported, (\d+) baselined', legs.get('leg6') if legs else None)
    one('CL-LEG6-OTHER', r'names (\d+) other GHSA ids', legs.get('other6') if legs else None)
    one('CL-CLEANROOM', r'All (\d+) standalone lock', legs.get('cleanroom') if legs else None)
    return out


def legs_from(d):
    """the head legs' own outputs (c5 legs --out DIR, + cleanroom's dir beside it if present) -> the numbers T6 compares."""
    if not d: return None
    o6 = open(os.path.join(d, 'leg6.out')).read() + open(os.path.join(d, 'leg6.err')).read()
    s6 = re.search(r'audit-gate: (\d+) distinct advisories reported, (\d+) baselined', o6)
    oth = sorted(set(re.findall(r'GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}', o6)) - set(K['three_ids']))
    res = {'leg6': (int(s6.group(1)), int(s6.group(2))) if s6 else None, 'other6': (len(oth),)}
    cr = os.path.join(os.path.dirname(d.rstrip('/')), 'cleanroom', 'leg2_cleanroom.out')
    if os.path.isfile(cr):
        mm = re.search(r'All (\d+) standalone lock', open(cr).read()); res['cleanroom'] = (int(mm.group(1)),) if mm else None
    return res


def sentences(body):
    s = re.split(r'(?<=[.;:!?])\s+|\n+', body)
    return [x.strip() for x in s if x.strip() and re.search(r'\d|GHSA|KS-|KS \d|`', x)]


def prtext(head, measured, reach, tar, legs_dir, repo, base, body_file, sent_out):
    if body_file:
        body = open(body_file, encoding='utf-8').read(); title = P['subject']; print('OFFLINE body from %s (title assumed == kit subject)' % body_file)
    else:
        pr = gh_get('pulls/%s' % P['pr']); body = pr.get('body') or ''; title = pr['title']
        if pr['head']['sha'] != head: print('REFUSED: API head %s != --head %s' % (pr['head']['sha'], head)); return 1
    keys, closing = scan(body + '\n' + title); hits, bad = refs_window(body)
    co = len(re.findall(r'(?im)^\s*(co-authored-by|signed-off-by):', body)); lt = len(title) + len(' (#%s)' % P['pr'])
    sh, su = sibling(body + '\n' + title); attr = attribution(body)
    print('BODY sha256/16 %s, %d chars, %d utf8-bytes' % (hashlib.sha256(body.encode()).hexdigest()[:16], len(body), len(body.encode())))
    print('T1 `Refs %s` lines: %d at line(s) %s (want exactly 1) | T1b closing words on it or the 3 lines above: %s' % (KEY, len(hits), [i + 1 for i in hits], bad or 'none'))
    print('T2 closing references before a key / #n (title + body): %s (want none)' % (closing or 'none'))
    print('T3 hyphenated keys (title + body): %s -> only %s: %s' % (keys, KEY, keys == [KEY]))
    print('T3b sibling %s: hyphenated %d (want 0) | unhyphenated %d (want >= 1)' % (SIB, sh, su))
    print('T4 title %r (%d chars, squash %d <= %d %s) == kit subject %s' % (title, len(title), lt, P['squash_max'], lt <= P['squash_max'], title == P['subject']))
    print('T5 trailer-shaped lines in the body: %d' % co)
    print('T5b attribution lines (a finding for the gate to rule, not a T-fail): %d %s' % (len(attr), attr))
    ok = len(hits) == 1 and not bad and not closing and keys == [KEY] and sh == 0 and su >= 1 and lt <= P['squash_max'] and title == P['subject'] and co == 0
    m = json.load(open(measured)); r = json.load(open(reach)); t3 = json.load(open(tar)) if tar else None; ns = {}
    if repo and base:
        for l in subprocess.run(['git', '-C', repo, 'diff', '--numstat', base, head], capture_output=True, text=True).stdout.strip().split('\n'):
            a, dl, p = l.split('\t'); ns[p] = (int(a), int(dl))
    else: ns = dict((p, tuple(v)) for p, v in P['numstat'].items())
    for cid, stated, want, good in claims(body, m, r, t3, ns, legs_from(legs_dir)):
        st = 'OK      ' if (good and stated and want != 'NOT MEASURED HERE') else ('ABSENT  ' if not stated else ('UNMEASRD' if want == 'NOT MEASURED HERE' else 'MISMATCH'))
        print('T6 %-16s %s stated %s measured %s' % (cid, st, stated, want))
        ok &= good
    ss = sentences(body)
    if sent_out: open(sent_out, 'w').write('\n'.join('%3d  %s' % (i + 1, x) for i, x in enumerate(ss)) + '\n')
    print('T7 %d factual-looking sentences written to %s for the sentence-by-sentence ruling' % (len(ss), sent_out or '(not written: give --sentences-out)'))
    return 0 if ok else 1


def linear_read(comments_out):
    i, err = linear_issue(KEY)
    if not i: print('LINEAR %s not returned: %s' % (KEY, err)); return 1
    cs = i['comments']['nodes']; at = i['attachments']['nodes']
    print('LINEAR %s %r state %s (%s) updatedAt %s archivedAt %s comments %d attachments %d' % (
        i['identifier'], i['title'], i['state']['name'], i['state']['type'], i['updatedAt'], i['archivedAt'], len(cs), len(at)))
    link = [c for c in cs if re.search(r'pull/%s\b' % P['pr'], c['body'])]
    for c in cs: print('  COMMENT %s %s %d B sha256/16 %s links #%s: %s' % (c['id'][:8], c['createdAt'], len(c['body'].encode()), hashlib.sha256(c['body'].encode()).hexdigest()[:16], P['pr'], c in link))
    for a in at: print('  ATTACHMENT %s %r %s %s' % (a['id'][:8], a['title'], a['url'], a['createdAt']))
    if comments_out: open(comments_out, 'w').write('\n\n=====\n\n'.join('%s %s\n%s' % (c['id'], c['createdAt'], c['body']) for c in cs))
    j, err2 = linear_issue(SIB)
    if not j: print('LINEAR %s not returned: %s' % (SIB, err2)); return 1
    jat = j['attachments']['nodes']; jpr = [a for a in jat if re.search(r'pull/%s\b' % P['pr'], a['url'] or '')]
    print('LINEAR %s %r state %s updatedAt %s archivedAt %s comments %d attachments %d (naming #%s: %d)' % (
        j['identifier'], j['title'], j['state']['name'], j['updatedAt'], j['archivedAt'], len(j['comments']['nodes']), len(jat), P['pr'], len(jpr)))
    for a in jat: print('  ATTACHMENT %s %r %s' % (a['id'][:8], a['title'], a['url']))
    ok1 = i['state']['name'] in K['linear_ok_states'] and not i['archivedAt'] and len(link) >= 1
    ok2 = j['state']['name'] in K['linear_sibling_ok_states'] and not j['archivedAt'] and not jpr
    print('VERDICT %s %s (want state %s, not archived, >= 1 comment linking #%s) | %s %s (want state %s, not archived, 0 attachments naming #%s)' % (
        KEY, 'OK' if ok1 else 'FINDING', K['linear_ok_states'], P['pr'], SIB, 'OK' if ok2 else 'FINDING', K['linear_sibling_ok_states'], P['pr']))
    return 0 if ok1 and ok2 else 1


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    st = 'Audit-contract suites'
    nh = needles('##[group]x\n2026-10-09T00:30:00.1Z ##[error]expected exit 3 (refused), got 1\n')
    nd = needles('##[group]y\n2026-10-08T09:00:00.1Z ##[error]expected exit 3 (refused), got 1\n')
    v = classify_red([('Dependency Audit', [st], nh)], {'pr1434@d7ba337a8ef6': [('Dependency Audit', [st], nd)]})
    rep(v[0] == 'PRE-EXISTING' and v[2] == ['pr1434@d7ba337a8ef6'], 'classify: same job + step + signature on another PR head -> PRE-EXISTING, comparator named: %s' % (v,))
    rep(classify_red([('Dependency Audit', [st], nh)], {})[0] == 'UNCLASSIFIED', 'PLANTED-RULE: with NO comparator (a develop-only rule on a path develop never runs) -> UNCLASSIFIED, never pre-existing')
    rep(classify_red([('Dependency Audit', [st], needles('##[error]expected exit 3 (refused), got 1'))], {'d': [('Dependency Audit', [st], nd)]})[0] == 'UNCLASSIFIED', 'PLANTED unread head log (##[group] 0) -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', [st], needles('##[group]\n##[error]expected exit 3 (refused), got 1\nhandlebars 4.7.9'))], {'d': [('Dependency Audit', [st], nd)]})[0] == 'UNCLASSIFIED',
        'PLANTED change needle (handlebars) in the failing log -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', [st], nh)], {'d': [('Dependency Audit', ['other step'], nd)]})[0] == 'UNCLASSIFIED', 'PLANTED different failing step at the comparator -> UNCLASSIFIED')
    rep(classify_red([('Dependency Audit', [st], needles('##[group]\n##[error]expected exit 3 (refused), got 1\nshell suites: 70 passed, 1 failed'))], {'d': [('Dependency Audit', [st], nd)]})[0] == 'UNCLASSIFIED',
        'PLANTED an EXTRA failure line at the head (not in the comparator) -> UNCLASSIFIED')
    rep(signature('2026-10-06T20:00:00.1Z run_shell_suites: 57 passed, 4 failed\nok 0 failed\n') == ['run_shell_suites: 57 passed, 4 failed'], 'signature strips timestamps; `0 failed` is not a failure')
    rep(signature('✖ audit-locks: x (32.5ms)') == signature('✖ audit-locks: x (35.07ms)'), 'signature strips per-test durations')
    rep(needles('##[group]')['fabricated'] == 0 and needles(AC['fabricated_control'])['fabricated'] == 1, 'fabricated needle counts 0 unless planted')
    rep(isinstance(_NoRedirect().redirect_request(None, None, 302, '', {}, 'u'), type(None)), 'the log opener does NOT follow the 302 with the auth header')
    rep(latest_by_path([{'path': 'a.yml', 'created_at': '1', 'id': 1}, {'path': 'a.yml', 'created_at': '2', 'id': 2}])['a.yml']['id'] == 2, 'latest_by_path keys by PATH and keeps the newest run')
    rep(classify_pr({'title': 'KS-1452 x'}, []) == 'OVERLAP' and classify_pr({'title': 'x'}, [sorted(PATHS)[0]]) == 'OVERLAP' and classify_pr({'title': 'x'}, ['q/package-lock.json']) == 'LOCKS', 'census classifier')
    k, c = scan('Refs KS-1452. filed as KS 1453; KS 767.'); rep(k == ['KS-1452'] and not c, 'scan: de-hyphenated keys are not keys')
    k, c = scan('same shape as KS-1437 (#1406). Refs KS-1452'); rep(k == ['KS-1437', 'KS-1452'], 'PLANTED hyphenated foreign key KS-1437 FIRES T3')
    rep(sibling('filed separately as KS 1453') == (0, 1) and sibling('KS-1453 and KS 1453')[0] == 1, 'T3b sibling scanner: unhyphenated passes, hyphenated FIRES')
    rep(refs_window('a\nthis resolves it\nRefs KS-1452')[1] and not refs_window('Refs KS-1452 https://x')[1], 'closing word within 3 lines above Refs FIRES; clean passes')
    rep(attribution('x\n\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)\n') == ['\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)'] and attribution('clean') == [],
        'T5b attribution scanner: the Generated-with line is SEEN; a clean body reads 0')
    m = {'locks': 5, 'entries': 5, 'field_writes': 18, 'declaring_parents': 7, 'tracked_locks': 45}
    r = {'lockfile_literal': 8, 'express': 339}; tar = {'bytes': {'handlebars@4.7.10': 712317}}; ns = dict((p, tuple(v)) for p, v in P['numstat'].items())
    good = ('5 locks, 5 entries, 18 field writes. all 7 declaring parents say ^4.7.9. over all 45 tracked locks. tarball (712,317 B). '
            '(control: `package-lock.json` 8). express 339')
    rep(all(x[3] for x in claims(good, m, r, tar, ns, None)), 'claims: a true body passes')
    rep(not all(x[3] for x in claims('all 8 declaring parents', m, r, tar, ns, None)), 'PLANTED 8 declaring parents vs measured 7 FAILS')
    rep(not all(x[3] for x in claims('tarball (712,318 B)', m, r, tar, ns, None)), 'PLANTED a tarball size off by one byte FAILS')
    rep(not all(x[3] for x in claims('audit-gate: 9 distinct advisories reported, 24 baselined', m, r, tar, ns, {'leg6': (10, 24), 'other6': (15,)})), 'PLANTED leg 6 count vs the measured head FAILS')
    rep(any(x[2] == 'NOT MEASURED HERE' for x in claims('audit-gate: 9 distinct advisories reported, 24 baselined', m, r, tar, ns, None)), 'a claim whose instrument was not given reads NOT MEASURED HERE, never OK')
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
            return prtext(req(A, '--head', True), req(A, '--measured'), req(A, '--reach'), req(A, '--tar'), opt(A, '--legs-head'), opt(A, '--repo'), opt(A, '--base'),
                          opt(A, '--body-file'), opt(A, '--sentences-out'))
        if A[0] == 'linear': return linear_read(opt(A, '--comments-out'))
    except SystemExit as e:
        print(e); return 2
    except (OSError, ValueError, urllib.error.URLError, KeyError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
