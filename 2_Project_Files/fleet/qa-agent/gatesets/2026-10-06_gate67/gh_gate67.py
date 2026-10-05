#!/usr/bin/env python3
"""gh_gate67.py — GitHub READ-ONLY instruments + PR-text judge for gate67 (#1394, KS-723). REST GETs only; GH_TOKEN by name, never printed.

  api       `API #1394 head <sha> branch <ref> base <ref> state <s> merged <b> mergeable <m> mergeable_state <ms>` (re-polled while null)
            + body sha256/16, chars, bytes (claim d6adc2a75838b7e7 / 6,437 bytes).
  actions   [--at SHA] [--prev SHA]  runs at SHA (default the head) vs the PR's OWN previous runs at --prev (default: none exist — #1394
            has ONE head; attempt 1 of the push never created the ref). With no previous head the comparison is against the workflow
            set the kit EXPECTS on a PR (K actions_expected, read off #1385's runs) and every expected workflow absent at SHA is
            NOT RUN (named, never a pass). NEW-FAILING = failing at SHA and not failing at prev. PLANTED-NAME CONTROL: a fabricated
            failing workflow injected at SHA must be reported NEW-FAILING, and a fabricated expected name must be reported NOT RUN,
            else the NONE is blind (rc 1). Use `--at <merge-in M> --prev a94ec8f6…` after the merge-in.
  census    every OPEN PR's files: OVERLAP (a kit code path, or title KS-723) / SPEC (any *.openapi.ts or the yaml — regenerates the
            same yaml) / DOCS (a platform doc) / other. CONTROL: a fabricated row carrying anchoring.openapi.ts must be OVERLAP.
  prtext    the live body, SENTENCE BY SENTENCE: every sentence printed with TRUE / FALSE / NOT RE-DERIVED (+ why), judged against
            facts derived here from blobs (diff, spec, docs, index.ts, the doc grep counts). Plus T1 one `Refs KS-723` + URL, T2 0
            closing words, T3 only KS-723 hyphenated, T4 title == commit subject, T5 0 Co-Authored-By.
  --selftest  the actions predicate, census classifier and the sentence judge on synthetic input (no network).
rc 0 / 1 (finding, blind control, FALSE sentence, OVERLAP, NOT RUN) / 3 API failure."""
import hashlib, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate67 import K, gh_get, gh_pages, git
import yaml

FAILING = ('failure', 'timed_out', 'cancelled', 'startup_failure', 'action_required')
EXPECTED = K['actions_expected']


def runs_by_name(runs):
    out = {}
    for r in sorted(runs, key=lambda r: r.get('created_at', '')):
        out[r['name']] = (r.get('status'), r.get('conclusion'))
    return out


def compare(prev, head, expected):
    failing = lambda d, n: d.get(n, (None, None))[1] in FAILING
    new = sorted(n for n in head if failing(head, n) and not failing(prev, n))
    pending = sorted(n for n in head if head[n][0] != 'completed')
    notrun = sorted(n for n in (set(expected) | set(prev)) if n not in head)
    return new, pending, notrun


def classify(pr_row, files):
    if 'KS-723' in (pr_row.get('title') or '') or set(files) & set(K['code_paths']): return 'OVERLAP'
    if any(f.endswith('.openapi.ts') for f in files): return 'SPEC'
    if set(files) & {K['flow'], K['cheat']}: return 'DOCS'
    return 'other'


def api():
    pr = None
    for i in range(3):
        pr = gh_get('pulls/%s' % K['pr'])
        if pr.get('mergeable') is not None: break
        time.sleep(5)
    b = pr.get('body') or ''
    print('API #%s head %s branch %s base %s state %s merged %s mergeable %s mergeable_state %s' % (
        K['pr'], pr['head']['sha'], pr['head']['ref'], pr['base']['ref'], pr['state'], pr['merged'], pr.get('mergeable'), pr.get('mergeable_state')))
    print('BODY sha256/16 %s chars %d bytes %d (claim %s) | title == kit %s | commits %s +%s/-%s files %s | updated %s' % (
        hashlib.sha256(b.encode()).hexdigest()[:16], len(b), len(b.encode()), K['claims']['body'], pr['title'] == K['pr_title'],
        pr.get('commits'), pr.get('additions'), pr.get('deletions'), pr.get('changed_files'), pr['updated_at']))
    if pr.get('mergeable_state') == 'dirty':
        print('INFO mergeable_state dirty = a merge conflict with develop (consistent with c4 mergetree: BOTH platform docs conflict); NOT a stale cache. It also suppresses `pull_request` workflows (see actions).')
    return 0 if pr['head']['sha'] == K['head'] and pr['state'] == 'open' and not pr['merged'] else 1


def actions(at, prev):
    def get(sha):
        for i in range(3):
            r = gh_get('actions/runs?head_sha=%s&per_page=100' % sha)
            print('READ runs at %s: total_count %d (attempt %d)' % (sha[:12], r['total_count'], i + 1))
            if r['total_count']: return r['workflow_runs']
            time.sleep(5)
        return []
    h = runs_by_name(get(at)); p = runs_by_name(get(prev)) if prev else {}
    for n in sorted(set(h) | set(p) | set(EXPECTED)):
        print('RUN %-38s prev %-22s at %s' % (n, '/'.join(map(str, p.get(n, ('-', '-')))) if prev else '(no previous head)', '/'.join(map(str, h.get(n, ('ABSENT', '-'))))))
    new, pending, notrun = compare(p, h, EXPECTED)
    # planted-name control: one fabricated FAILING run at SHA and one fabricated EXPECTED name
    hp = dict(h); hp['__planted_failing__'] = ('completed', 'failure')
    pn, _, pnr = compare(p, hp, list(EXPECTED) + ['__planted_expected__'])
    ctl = '__planted_failing__' in pn and '__planted_expected__' in pnr
    print('NEW-FAILING %s | PENDING %s | NOT RUN (expected, absent at %s) %s | PLANTED-NAME CONTROL reported: %s' % (
        new or 'NONE', pending or 'NONE', at[:12], notrun or 'NONE', ctl))
    if notrun and not prev:
        print('INFO NOT RUN is NOT a pass: with mergeable_state dirty GitHub cannot build the test merge ref, so `pull_request` workflows do not trigger. Re-read at the merge-in M with `--at M --prev %s`.' % K['head'])
    return 0 if ctl and not new and not pending and not notrun else 1


def census():
    prs = gh_pages('pulls?state=open')
    rows, cnt = [], {}
    for pr in prs:
        if str(pr['number']) == K['pr']: continue
        files = [f['filename'] for f in gh_pages('pulls/%d/files' % pr['number'])]
        c = classify(pr, files); cnt[c] = cnt.get(c, 0) + 1
        if c != 'other': rows.append('  %s #%d %s %s' % (c, pr['number'], pr['head']['sha'][:12], pr['title'][:70]))
    ctl = classify({'title': 'x'}, [K['registry_file']]) == 'OVERLAP' and classify({'title': 'y'}, ['Blockchain/Dev/services/auth/src/auth.openapi.ts']) == 'SPEC'
    print('CENSUS %d other open PR(s): %s | CONTROL fires %s' % (len(prs) - 1, cnt, ctl))
    for r in rows: print(r)
    return 3 if not ctl else (1 if cnt.get('OVERLAP') else 0)


# ---------------- prtext ----------------
def facts(repo):
    H, B = K['head'], K['base']
    f = {}
    ns = git(repo, 'diff', '--numstat', B, H).splitlines()
    f['adds'] = sum(int(x.split('\t')[0]) for x in ns); f['dels'] = sum(int(x.split('\t')[1]) for x in ns); f['nfiles'] = len(ns)
    f['index_changed'] = K['route_file'] in git(repo, 'diff', '--name-only', B, H)
    idx = git(repo, 'show', '%s:%s' % (H, K['route_file'])).split('\n')
    f['line_tx'] = [i + 1 for i, l in enumerate(idx) if "app.get('/api/anchors/tx/:txHash'" in l]
    f['line_id'] = [i + 1 for i, l in enumerate(idx) if "app.get('/api/anchors/:id'" in l]
    f['hunks'] = re.findall(r'^@@ [^@]+ @@', git(repo, 'diff', '-U0', B, H, '--', K['registry_file']), re.M)
    f['hunks3'] = re.findall(r'^@@ [^@]+ @@', git(repo, 'diff', B, H, '--', K['registry_file']), re.M)
    yH, yB = git(repo, 'show', '%s:%s' % (H, K['spec'])), git(repo, 'show', '%s:%s' % (B, K['spec']))
    f['bytes'] = (len(yB.encode()), len(yH.encode())); f['paths'] = len(yaml.safe_load(yH)['paths']); f['txcount'] = (yB.count('/api/anchors/tx/'), yH.count('/api/anchors/tx/'))
    test = git(repo, 'show', '%s:%s' % (H, K['test'])); f['cells'] = len(re.findall(r"\bit\('", test))
    fl = git(repo, 'show', '%s:%s' % (H, K['flow'])); f['flow_h2'] = len(re.findall(r'<h2\b', fl, re.I))
    def gc(rev, pat):
        return tuple(sum(1 for l in git(repo, 'show', '%s:%s' % (rev, K[d])).split('\n') if re.search(pat, l, re.I)) for d in ('flow', 'cheat'))
    f['grep_auth'] = gc(B, 'auth'); f['grep_anch'] = gc(B, 'anchoring'); f['grep_unit'] = gc(B, 'anchoring.*unit suite')
    tc = json.loads(git(repo, 'show', '%s:%s' % (H, K['anchoring_tsconfig']))); f['excl'] = 'src/__tests__' in tc.get('exclude', [])
    return f


def rules(f):
    """(pattern over the sentence, judge(sentence) -> (verdict, why)). First matching rule wins; unmatched -> NOT RE-DERIVED."""
    T = lambda c, w: ('TRUE' if c else 'FALSE', w)
    return [
        (r'index\.ts:1089', lambda s: T(f['line_tx'] == [1089], 'route line at the head %s' % f['line_tx'])),
        (r'No route and no handler is changed', lambda s: T(not f['index_changed'], 'index.ts in the diff: %s' % f['index_changed'])),
        (r'index\.ts:827', lambda s: T(f['line_id'] == [827], 'GET /:id at %s; 405 on two live POSTs re-derived by c2 W6b' % f['line_id'])),
        (r'5 files, \+354', lambda s: T((f['nfiles'], f['adds'], f['dels']) == (5, 354, 0), 'numstat %d files +%d/-%d' % (f['nfiles'], f['adds'], f['dels']))),
        (r'one hunk at `:406`', lambda s: T(len(f['hunks']) == 1 and '406' in f['hunks'][0], 'actual hunk(s) -U0 %s / -U3 %s (one hunk: %s; `:406` matches neither — it is the held carve\'s header line)' % (f['hunks'], f.get('hunks3'), len(f['hunks']) == 1))),
        (r'NEW, 5 cells', lambda s: T(f['cells'] == 5 and K['base_blobs'][K['test']] is None, '%d it( cells, absent at base' % f['cells'])),
        (r'1,351,218', lambda s: T(f['bytes'] == (1351218, 1354452) and f['paths'] == 310 and f['txcount'] == (0, 1), 'bytes %s, paths %d, /api/anchors/tx/ %s' % (f['bytes'], f['paths'], f['txcount']))),
        (r'89/81', lambda s: T(f['grep_auth'] == (89, 81) and f['grep_anch'] == (18, 19), 'per-line grep at d784: auth %s, anchoring %s' % (f['grep_auth'], f['grep_anch']))),
        (r'anchoring\.\*unit suite', lambda s: T(f['grep_unit'] == (0, 0), 'per-line grep at d784: %s' % (f['grep_unit'],))),
        (r"exclude: \['node_modules','dist','src/__tests__'\]", lambda s: T(f['excl'], 'tsconfig exclude carries src/__tests__: %s' % f['excl'])),
        (r'17 total', lambda s: T(f['flow_h2'] == 17, 'flow <h2 at the head %d' % f['flow_h2'])),
        (r'`@@ -406,7 \+406,44 @@`|header-fixed copy|hunk body', lambda s: ('NOT RE-DERIVED', 'about the HELD CARVE artefact, not the commit (the commit\'s own hunk is %s)' % f['hunks'])),
    ]


def judge_sentences(body, rl):
    text = re.sub(r'\n(?=[-*] )', '\n\n', body)
    sents = [s.strip() for blk in text.split('\n\n') for s in re.split(r'(?:(?<=[.!?])|(?<=[.!?]\*\*))\s+(?=[A-Z*`(🔴])', blk.replace('\n', ' ')) if s.strip()]
    out = []
    for s in sents:
        for pat, j in rl:
            if re.search(pat, s):
                v, w = j(s); out.append((v, s, w)); break
        else:
            out.append(('NOT RE-DERIVED', s, 'no blob-derivable fact in this sentence, or it reports a builder RUN the gate re-measures (c3) / Linear / the hook'))
    return out


def prtext(repo):
    pr = gh_get('pulls/%s' % K['pr']); body = pr.get('body') or ''; title = pr['title']
    res = judge_sentences(body, rules(facts(repo)))
    for i, (v, s, w) in enumerate(res, 1):
        print('S%02d %-15s %s\n        -> %s' % (i, v, s[:230], w))
    keys = re.findall(r'\bKS-\d+\b', body + ' ' + title)
    refs = re.findall(r'^Refs KS-723\b.*https://linear\.app/secuura/issue/KS-723', body, re.M)
    closing = re.findall(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+(#\d+|KS-\d+)', body + ' ' + title, re.I)
    subj = git(repo, 'log', '-1', '--format=%s', K['head']).rstrip('\n'); co = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', K['head'])))
    nf = sum(1 for v, _, _ in res if v == 'FALSE')
    print('T1 Refs KS-723 + URL lines: %d (want 1)' % len(refs))
    print('T2 closing references: %s (want none)' % closing)
    print('T3 hyphenated keys (body + title): %s -> only KS-723: %s | KS-723 in the BODY %d (READY: 6), in the title %d' % (sorted(set(keys)), set(keys) == {'KS-723'}, len(re.findall(r'\bKS-723\b', body)), len(re.findall(r'\bKS-723\b', title))))
    print('T4 title == commit subject: %s (%d chars)' % (title == subj, len(title)))
    print('T5 Co-Authored-By in the commit: %d' % co)
    print('SENTENCES %d: TRUE %d | FALSE %d | NOT RE-DERIVED %d' % (len(res), sum(1 for v, _, _ in res if v == 'TRUE'), nf, sum(1 for v, _, _ in res if v == 'NOT RE-DERIVED')))
    ok = len(refs) == 1 and not closing and set(keys) == {'KS-723'} and title == subj and co == 0
    return 0 if ok and nf == 0 else 1


def selftest():
    res = []
    def rep(c, m): res.append(c); print('%s %s' % ('PASS' if c else 'FAIL', m))
    prev = {'pr': ('completed', 'failure'), 'Security Scanning': ('completed', 'success')}
    head = {'pr': ('completed', 'failure'), 'Security Scanning': ('completed', 'failure')}
    new, pend, nr = compare(prev, head, [])
    rep(new == ['Security Scanning'] and not pend, 'actions: success->failure is NEW-FAILING, failure->failure is not: %s' % new)
    new, pend, nr = compare({}, {'Dependabot standalone locks': ('completed', 'skipped')}, EXPECTED)
    rep(set(nr) == set(EXPECTED) - {'Dependabot standalone locks'}, 'actions: with no previous head, every expected workflow absent is NOT RUN: %s' % nr)
    new, pend, nr = compare({}, {'pr': ('in_progress', None)}, ['pr'])
    rep(pend == ['pr'], 'actions: in_progress is PENDING, never a pass')
    rep(classify({'title': 'KS-723 other'}, []) == 'OVERLAP' and classify({'title': 'x'}, [K['spec']]) == 'OVERLAP'
        and classify({'title': 'x'}, ['a/b.openapi.ts']) == 'SPEC' and classify({'title': 'x'}, [K['flow']]) == 'DOCS', 'census classifier OVERLAP/SPEC/DOCS')
    f = {'line_tx': [1089], 'index_changed': False, 'line_id': [827], 'nfiles': 5, 'adds': 354, 'dels': 0, 'hunks': ['@@ -409,0 +410,43 @@'],
         'cells': 5, 'bytes': (1351218, 1354452), 'paths': 310, 'txcount': (0, 1), 'grep_auth': (89, 81), 'grep_anch': (18, 19), 'grep_unit': (0, 0), 'excl': True, 'flow_h2': 17}
    r = judge_sentences('Routed since `index.ts:1089` ok. **No route and no handler is changed.** Planted: `index.ts:1089` again.', rules(f))
    rep([v for v, _, _ in r] == ['TRUE', 'TRUE', 'TRUE'], 'sentence judge splits and judges: %s' % [v for v, _, _ in r])
    f2 = dict(f, index_changed=True)
    r = judge_sentences('**No route and no handler is changed.**', rules(f2))
    rep(r[0][0] == 'FALSE', 'PLANTED: index.ts in the diff makes "No route and no handler is changed" FALSE')
    r = judge_sentences('The weather is fine.', rules(f)); rep(r[0][0] == 'NOT RE-DERIVED', 'an unmatched sentence is NOT RE-DERIVED, never TRUE')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if not A: print(__doc__); return 2
    try:
        if A[0] == '--selftest': return selftest()
        if A[0] == 'api': return api()
        if A[0] == 'actions': return actions(opt('--at', K['head']), opt('--prev'))
        if A[0] == 'census': return census()
        if A[0] == 'prtext': return prtext(opt('--repo', K['checkout']))
    except (OSError, ValueError) as e:
        print('API FAILURE: %s' % e); return 3
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
