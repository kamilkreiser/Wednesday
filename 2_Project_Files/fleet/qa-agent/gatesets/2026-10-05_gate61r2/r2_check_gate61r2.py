#!/usr/bin/env python3
"""r2_check_gate61r2.py — gate61 ROUND 2 (#1383, KS-1401): the READ-ONLY instruments for the narrowed scope.

  scope [--repo R] [--head H] [--parent P]
      S1  ONE parent == the round-1 head (P, kit round1_head) and P is an ancestor of H (a fast-forward)
      S2  H^{tree} == kit claimed_tree (CONTROL: P^{tree} differs)
      S3  `git diff --numstat -z P H` == EXACTLY the kit r2_files with their +/- (so every OTHER path is byte-unchanged since round 1)
      S4  `git ls-tree H` modes == kit modes (the suite 100755; core.filemode is false in this repo, so the TREE is the only witness)
      S5  `%(trailers)` raw bytes == 1 (CONTROL commit bf277eead268 == 55)
      S6  subject <= 92, no `(#`; hyphenated keys in the WHOLE message == {KS-1401}; STRICT closing refs in the message == 0
      S7  049: P->H is ONE pure insertion; its live (comment-stripped) lines are EXACTLY the one bypass statement, third argument `true`;
          deleting the inserted lines from H's file gives P's file byte-for-byte; the bypass is the FIRST live statement after the DO
          block's BEGIN and lock_timeout is the next; no session-level SET / set_config(..., false) of the bypass anywhere live;
          sha256(049 at H) == kit
      S8  both docs: every changed line (old side AND new side) lies inside block 22.'s span; the close-tag line is unchanged and
          occurs once; the list of <h2>/<h3> lines is unchanged
      S9  the suite: pure insertion(s) only; `cell ` lines 11 -> 12; the new cell names N-1383-1; KS1401_F049_UNDER_TEST present
  body --body-file F [--baseline-file B]
      B1  body sha256: BASELINE (prefix kit body_baseline_sha256) or NEWER (accepted; the gate must cite Wednesday's N-1383-8 ruling)
      B2  STRICT closing references == 0 (closing keyword IMMEDIATELY followed by KS-<n> or #<n>), beside a planted positive control
          scored by the SAME predicate in the SAME run (must be 1)
      B3  exactly ONE `Refs KS-1401` line; hyphenated keys == {KS-1401}
      B4  "never reaches demo" + "kintsugi deploy" present
      INFO the F 3rd brief's WIDE predicate (a closing word within 120 chars of any key), the figures 62/12, any stale "53 passed"
  --selftest [--repo R]
      synthetic arms for every judge (one quiet + must-fire arms each) and, if R has the objects, the REAL quiet case (scope at the kit
      head) plus a REAL firing case (scope pretending the round-1 head is the round-2 commit).

READ-ONLY: git verbs are whitelisted (rev-parse, rev-list, log, show, diff, ls-tree, cat-file, merge-base); nothing is written anywhere
except stdout. rc 0 PASS / 1 FAIL / 2 usage or refusal. Prints `CHECKED <n>`; 0 checked is a FAIL."""
import difflib, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, 'kit.json'), encoding='utf-8'))
READ_VERBS = {'rev-parse', 'rev-list', 'log', 'show', 'diff', 'ls-tree', 'cat-file', 'merge-base'}
KEY = re.compile(r'\bKS-\d+\b')
CLOSE_WORDS = r'(?:close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?|completing)'
STRICT = re.compile(r'(?i)\b' + CLOSE_WORDS + r'\s*:?\s*(KS-\d+|#\d+)\b')
WIDE_WORD = re.compile(r'(?i)\b' + CLOSE_WORDS + r'\b')
BYPASS_RX = re.compile(r"^\s*PERFORM\s+set_config\(\s*'app\.tenant_scope_bypass'\s*,\s*'platform_admin'\s*,\s*true\s*\)\s*;\s*$", re.I)
LOCKT_RX = re.compile(r"^\s*PERFORM\s+set_config\(\s*'lock_timeout'", re.I)
SESSION_SET_RX = re.compile(r"(?i)(\bSET\s+(SESSION\s+)?app\.tenant_scope_bypass\b|set_config\(\s*'app\.tenant_scope_bypass'\s*,[^)]*,\s*false\s*\))")
H2 = re.compile(r'^\s*<h[23]\b')
CLOSE_TAG = re.compile(r'^\s*</body>\s*$')


class Checks:
    def __init__(self, quiet=False): self.res = []; self.quiet = quiet
    def chk(self, name, ok, detail):
        self.res.append((name, bool(ok)))
        if not self.quiet: print('%s %s | %s' % ('PASS' if ok else 'FAIL', name, detail))
    def info(self, msg):
        if not self.quiet: print('INFO ' + msg)
    def fails(self): return [n for n, ok in self.res if not ok]
    def done(self):
        print('CHECKED %d | PASS %d | FAIL %d' % (len(self.res), sum(1 for _, o in self.res if o), len(self.fails())))
        return 1 if (not self.res or self.fails()) else 0


def git(repo, *args, raw=False):
    if args[0] not in READ_VERBS: raise SystemExit('REFUSING: git verb %r is not a read verb' % args[0])
    p = subprocess.run(['git', '-C', repo] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0: raise SystemExit('git %s failed rc %d: %s' % (' '.join(args[:3]), p.returncode, p.stderr.decode()[:300]))
    return p.stdout if raw else p.stdout.decode('utf-8')


def strip_sql(text):
    """live SQL lines: `--` comments removed outside quotes, `/* */` removed (nested), blank lines dropped; returns [(lineno, text)]"""
    out, depth = [], 0
    for n, line in enumerate(text.split('\n'), 1):
        buf, i, q = [], 0, None
        while i < len(line):
            c, two = line[i], line[i:i + 2]
            if depth:
                if two == '/*': depth += 1; i += 2; continue
                if two == '*/': depth -= 1; i += 2; continue
                i += 1; continue
            if q:
                buf.append(c)
                if c == q: q = None
                i += 1; continue
            if c == "'": q = c; buf.append(c); i += 1; continue
            if two == '--': break
            if two == '/*': depth += 1; i += 2; continue
            buf.append(c); i += 1
        s = ''.join(buf).rstrip()
        if s.strip(): out.append((n, s))
    return out


def ops(a, b): return [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != 'equal']


def judge_049(C, old, new, want_sha=None):
    o, n = old.split('\n'), new.split('\n'); op = ops(o, n)
    C.chk('S7a 049 one pure insertion', len(op) == 1 and op[0][0] == 'insert', 'opcodes %s' % [(x[0], x[1], x[2], x[3], x[4]) for x in op])
    if not (len(op) == 1 and op[0][0] == 'insert'):
        return
    _, i1, _, j1, j2 = op[0]; ins = '\n'.join(n[j1:j2])
    live_ins = [s for _, s in strip_sql(ins)]
    C.chk('S7b the insert is EXACTLY one live statement: the bypass, is_local true', len(live_ins) == 1 and bool(BYPASS_RX.match(live_ins[0])),
          '%d live line(s) inserted at old :%d: %s' % (len(live_ins), i1 + 1, [x.strip()[:90] for x in live_ins]))
    C.chk('S7c H minus the insert == P byte-for-byte', '\n'.join(n[:j1] + n[j2:]) == old, 'inserted %d line(s) (%d comment/blank)' % (j2 - j1, (j2 - j1) - len(live_ins)))
    live = strip_sql(new); idx = next((k for k, (_, s) in enumerate(live) if re.match(r'^\s*BEGIN\s*$', s, re.I)), None)
    first = live[idx + 1][1].strip() if idx is not None and idx + 1 < len(live) else None
    second = live[idx + 2][1].strip() if idx is not None and idx + 2 < len(live) else None
    C.chk('S7d the bypass is the FIRST live statement after BEGIN; lock_timeout next', bool(first and BYPASS_RX.match(first) and second and LOCKT_RX.match(second)),
          'BEGIN at :%s | first %r | second %r' % (live[idx][0] if idx is not None else None, (first or '')[:80], (second or '')[:60]))
    ses = [(ln, s.strip()[:90]) for ln, s in live if SESSION_SET_RX.search(s)]
    C.chk('S7e no session-level bypass anywhere live', not ses, 'session-level hits %s' % (ses or 'NONE'))
    cnt_old = sum(s.count('tenant_scope_bypass') for _, s in strip_sql(old)); cnt_new = sum(s.count('tenant_scope_bypass') for _, s in strip_sql(new))
    C.chk('S7f live tenant_scope_bypass mentions: old + 1 == new', cnt_new == cnt_old + 1, 'old %d (the policy carve-outs) -> new %d' % (cnt_old, cnt_new))
    if want_sha:
        got = hashlib.sha256(new.encode('utf-8')).hexdigest()
        C.chk('S7g sha256(049 at H) == kit', got == want_sha, 'got %s want %s' % (got[:16], want_sha[:16]))


def block22_span(lines, num='22'):
    """[start, end): from the `<h2>22.` line (or its opening <div class="section"> / <section>) up to the close tag"""
    s = next((i for i, l in enumerate(lines) if re.match(r'^\s*<h2>' + num + r'\.', l)), None)
    c = [i for i, l in enumerate(lines) if CLOSE_TAG.match(l)]
    if s is None or len(c) != 1: return None, c
    while s > 0 and re.match(r'^\s*<(div class="section"|section)\b', lines[s - 1]): s -= 1
    return (s, c[0]), c


def judge_doc(C, name, old, new):
    o, n = old.split('\n'), new.split('\n')
    so, co = block22_span(o); sn, cn = block22_span(n)
    C.chk('S8a %s block 22. and ONE close tag on both sides' % name, so is not None and sn is not None, 'old span %s close %s | new span %s close %s' % (so, co, sn, cn))
    if so is None or sn is None: return
    op = ops(o, n); out = [x for x in op if not (so[0] <= x[1] and x[2] <= so[1] and sn[0] <= x[3] and x[4] <= sn[1])]
    C.chk('S8b %s every changed line inside block 22.' % name, op and not out, '%d hunk(s); outside block 22.: %s' % (len(op), [(x[0], x[1] + 1, x[2], x[3] + 1, x[4]) for x in out] or 'NONE'))
    C.chk('S8c %s close tag unchanged' % name, o[co[0]] == n[cn[0]], 'old %r -> new %r' % (o[co[0]], n[cn[0]]))
    ho, hn = [l.strip() for l in o if H2.match(l)], [l.strip() for l in n if H2.match(l)]
    C.chk('S8d %s <h2>/<h3> list unchanged' % name, ho == hn, '%d -> %d headings; first difference %s' % (len(ho), len(hn), next(((a[:60], b[:60]) for a, b in zip(ho, hn) if a != b), 'NONE' if len(ho) == len(hn) else 'a count change')))


def judge_suite(C, old, new):
    o, n = old.split('\n'), new.split('\n'); op = ops(o, n)
    C.chk('S9a suite: pure insertion(s) only', op and all(x[0] == 'insert' for x in op), 'opcodes %s' % [x[0] for x in op])
    co, cn = sum(1 for l in o if l.startswith('cell ')), sum(1 for l in n if l.startswith('cell '))
    C.chk('S9b suite cells 11 -> 12', (co, cn) == (11, 12), 'cell lines %d -> %d' % (co, cn))
    newcells = [l for l in n if l.startswith('cell ') and l not in o]
    C.chk('S9c the new cell names N-1383-1 and the override exists', len(newcells) == 1 and 'N-1383-1' in newcells[0] and 'KS1401_F049_UNDER_TEST' in new,
          'new cell(s) %s | KS1401_F049_UNDER_TEST present %s' % ([x[:90] for x in newcells], 'KS1401_F049_UNDER_TEST' in new))
    C.info('suite: `|| no "` assertion sites %d -> %d (a SOURCE count; the gate measures 62 at runtime)' % (old.count('|| no "'), new.count('|| no "')))


def strict_hits(text): return [m.group(0) for m in STRICT.finditer(text)]


def wide_hits(text, window=120):
    keys = [m.start() for m in re.finditer(r'\bKS[- ]\d+\b|#\d+', text)]
    return [text[max(0, m.start() - 20):m.end() + 30].replace('\n', ' ') for m in WIDE_WORD.finditer(text) if any(abs(k - m.start()) <= window for k in keys)]


def judge_message(C, msg):
    subj = msg.split('\n', 1)[0]
    C.chk('S6a subject <= 92, no (#', len(subj) <= 92 and '(#' not in subj, '%d chars: %r' % (len(subj), subj))
    keys = sorted(set(KEY.findall(msg)))
    C.chk('S6b hyphenated keys in the message == {KS-1401}', keys == ['KS-1401'], 'keys %s' % keys)
    h = strict_hits(msg); ctl = strict_hits('Closes KS-1401')
    C.chk('S6c STRICT closing refs in the message == 0 (control fires)', not h and len(ctl) == 1, 'hits %s | control %s' % (h or 'NONE', ctl))
    C.info('commit message WIDE predicate (closing word within 120 chars of a key): %s' % (wide_hits(msg) or 'NONE'))


def judge_body(C, body, baseline=None):
    sha = hashlib.sha256(body.encode('utf-8')).hexdigest(); base = K['body_baseline_sha256']
    cls = 'BASELINE' if sha == base else 'NEWER'
    C.chk('B1 body is the round-1 baseline or a newer body (either accepted)', True, '%s sha256 %s (%d bytes, %d chars) | baseline %s' % (cls, sha[:16], len(body.encode('utf-8')), len(body), base[:16]))
    if cls == 'NEWER':
        C.info('NEWER body: the gate diffs it against the baseline and cites Wednesday\'s N-1383-8 ruling (or names its absence)')
        if baseline is not None:
            d = [l for l in difflib.unified_diff(baseline.split('\n'), body.split('\n'), lineterm='', n=0) if l[:1] in '+-' and not l.startswith(('+++', '---'))]
            C.info('diff vs baseline: %d line(s) removed, %d added' % (sum(1 for l in d if l[0] == '-'), sum(1 for l in d if l[0] == '+')))
    h = strict_hits(body); ctl = strict_hits(body + '\n\nCloses KS-1401\n')
    C.chk('B2 STRICT closing refs == 0, planted control in the same run adds exactly 1', not h and len(ctl) == len(h) + 1, 'hits %s | body + planted `Closes KS-1401` scores %d (want hits + 1 = %d)' % (h or 'NONE', len(ctl), len(h) + 1))
    refs = re.findall(r'(?m)^Refs KS-1401\s*$', body); keys = sorted(set(KEY.findall(body)))
    C.chk('B3 ONE `Refs KS-1401`, hyphenated keys == {KS-1401}', len(refs) == 1 and keys == ['KS-1401'], 'Refs lines %d | keys %s' % (len(refs), keys))
    C.chk('B4 never-demo + kintsugi deploy', bool(re.search(r'(?i)never reaches demo|never demo', body)) and bool(re.search(r'(?i)kintsugi deploy', body)), 'never-demo %s | kintsugi deploy %s' % (bool(re.search(r'(?i)never reaches demo|never demo', body)), bool(re.search(r'(?i)kintsugi deploy', body))))
    C.info('WIDE predicate (F 3rd brief: closing word within 120 chars of a key): %s' % (wide_hits(body) or 'NONE'))
    C.info('figures: "62 passed, 0 failed" %s | "12 cells" %s | stale "53 passed" lines: %s' % ('62 passed, 0 failed' in body, '12 cells' in body,
           [l.strip()[:140] for l in body.split('\n') if '53 passed' in l] or 'NONE'))
    C.info('N-1383-8: demo-mechanism sentence %s | kintsugi nullability %s' % (bool(re.search(r'(?i)any\*{0,2} box that boots', body)), bool(re.search(r'(?i)nullab', body))))


def scope(C, repo, H, P):
    par = git(repo, 'rev-list', '--parents', '-n', '1', H).split()[1:]
    anc = subprocess.run(['git', '-C', repo, 'merge-base', '--is-ancestor', P, H]).returncode == 0
    C.chk('S1 ONE parent == round-1 head, fast-forward', par == [P] and anc, 'parents %s (want [%s]) | ancestor %s' % ([p[:12] for p in par], P[:12], anc))
    t, tp = git(repo, 'rev-parse', H + '^{tree}').strip(), git(repo, 'rev-parse', P + '^{tree}').strip()
    C.chk('S2 tree == claimed tree (control: parent tree differs)', t == K['claimed_tree'] and tp != t, 'H tree %s | claimed %s | parent tree %s' % (t[:12], K['claimed_tree'][:12], tp[:12]))
    raw = git(repo, 'diff', '--numstat', '-z', P, H).split('\0'); got = {}
    for rec in raw:
        if rec.strip():
            a, d, p = rec.split('\t', 2); got[p] = [int(a), int(d)]
    want = {p: v for p, v in K['r2_files'].items()}
    C.chk('S3 numstat P..H == EXACTLY the 4 declared paths and +/-', got == want, 'got %s' % {k.split('/')[-1]: v for k, v in got.items()})
    ls = {}
    for line in git(repo, 'ls-tree', H, '--', *K['modes'].keys()).strip().split('\n'):
        meta, path = line.split('\t', 1); ls[path] = meta.split()[0]
    C.chk('S4 ls-tree modes', ls == K['modes'], 'got %s' % {k.split('/')[-1]: v for k, v in ls.items()})
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', H, raw=True)); cb = len(git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control_commit'], raw=True))
    C.chk('S5 trailers raw 1 byte (control 55)', tb == 1 and cb == K['trailer_control_bytes_raw'], 'head %d | control %s %d' % (tb, K['trailer_control_commit'], cb))
    judge_message(C, git(repo, 'log', '-1', '--format=%B', H))
    mig = K['migration']
    judge_049(C, git(repo, 'show', '%s:%s' % (P, mig)), git(repo, 'show', '%s:%s' % (H, mig)), K['blobs_r2']['049_sha256'] if H == K['head'] else None)
    for d in K['docs']:
        judge_doc(C, d.split('/')[-1][:20], git(repo, 'show', '%s:%s' % (P, d)), git(repo, 'show', '%s:%s' % (H, d)))
    judge_suite(C, git(repo, 'show', '%s:%s' % (P, K['test'])), git(repo, 'show', '%s:%s' % (H, K['test'])))


# ---------------------------------------------------------------- self-test
MINI_OLD = """-- header comment
DO $x$
DECLARE
  t TEXT;
BEGIN
  -- lock comment
  PERFORM set_config('lock_timeout', '5s', true);

  FOREACH t IN ARRAY tables LOOP
    EXECUTE format('UPDATE public.%I SET tenant_id = $1 WHERE tenant_id IS NULL', t) USING d;
    EXECUTE $p$ CREATE POLICY p ON x USING (current_setting('app.tenant_scope_bypass', true) = 'platform_admin') $p$;
  END LOOP;
END
$x$;"""
FIX = "  -- N-1383-1: the backfill must not be filtered by the policy it manages\n  PERFORM set_config('app.tenant_scope_bypass', 'platform_admin', true);\n\n"
MINI_NEW = MINI_OLD.replace("BEGIN\n", "BEGIN\n" + FIX, 1)
DOC_OLD = """<html>
<h2>12. Older block (KS-1333)</h2>
<p>old twelve</p>
<h2>22. Migration 049 (KS-1401)</h2>
<p>11 cells, 53 assertions</p>
<p>tail</p>
</body>"""
DOC_NEW = DOC_OLD.replace('<p>11 cells, 53 assertions</p>', '<p>12 cells, 62 assertions</p>\n<p>Cell 12: N-1383-1</p>')
SUITE_OLD = 'cell "one"\nok\n' * 11 + '# end'
SUITE_NEW = SUITE_OLD.replace('# end', 'cell "N-1383-1: owner"\nF="${KS1401_F049_UNDER_TEST:-x}"\n# end')


def arm(label, fn, want_fail, tag):
    C = Checks(quiet=True); fn(C); f = C.fails(); fired = any(x.startswith(tag) for x in f)
    ok = (fired if want_fail else (not f and len(C.res) > 0))
    print('%s %s | %s | failed %s' % ('ARM-OK' if ok else 'ARM-BROKEN', label, ('must fire ' + tag) if want_fail else 'must be quiet', f or 'NONE'))
    return ok


def selftest(repo):
    res = []
    res.append(arm('Q049 the fix shape', lambda C: judge_049(C, MINI_OLD, MINI_NEW), False, ''))
    res.append(arm('T049a is_local false', lambda C: judge_049(C, MINI_OLD, MINI_NEW.replace("'platform_admin', true)", "'platform_admin', false)")), True, 'S7b'))
    res.append(arm('T049b a second live line (row_security off)', lambda C: judge_049(C, MINI_OLD, MINI_NEW.replace(FIX, FIX + "  SET LOCAL row_security = off;\n")), True, 'S7b'))
    res.append(arm('T049c bypass placed AFTER lock_timeout', lambda C: judge_049(C, MINI_OLD, MINI_OLD.replace("'5s', true);\n", "'5s', true);\n" + FIX, 1)), True, 'S7d'))
    res.append(arm('T049d an existing line edited too', lambda C: judge_049(C, MINI_OLD, MINI_NEW.replace("'5s'", "'9s'")), True, 'S7a'))
    res.append(arm('T049e session-level SET instead', lambda C: judge_049(C, MINI_OLD, MINI_OLD.replace("BEGIN\n", "BEGIN\n  SET app.tenant_scope_bypass = 'platform_admin';\n", 1)), True, 'S7b'))
    res.append(arm('T049f the fix line commented out', lambda C: judge_049(C, MINI_OLD, MINI_NEW.replace("  PERFORM set_config('app.tenant", "  -- PERFORM set_config('app.tenant")), True, 'S7b'))
    res.append(arm('QDOC an edit inside block 22.', lambda C: judge_doc(C, 'sim', DOC_OLD, DOC_NEW), False, ''))
    res.append(arm('TDOCa an edit in block 12.', lambda C: judge_doc(C, 'sim', DOC_OLD, DOC_NEW.replace('old twelve', 'new twelve')), True, 'S8b'))
    res.append(arm('TDOCb the close tag re-indented', lambda C: judge_doc(C, 'sim', DOC_OLD, DOC_NEW.replace('\n</body>', '\n  </body>')), True, 'S8'))
    res.append(arm('TDOCc a new <h2> inside block 22.', lambda C: judge_doc(C, 'sim', DOC_OLD, DOC_NEW.replace('<p>tail</p>', '<h2>23. x (KS-1)</h2>\n<p>tail</p>')), True, 'S8d'))
    res.append(arm('QSUITE one inserted cell', lambda C: judge_suite(C, SUITE_OLD, SUITE_NEW), False, ''))
    res.append(arm('TSUITEa an existing line edited', lambda C: judge_suite(C, SUITE_OLD, SUITE_NEW.replace('cell "one"\nok', 'cell "one"\nnot ok', 1)), True, 'S9a'))
    res.append(arm('TSUITEb no new cell', lambda C: judge_suite(C, SUITE_OLD, SUITE_OLD + '\n# comment'), True, 'S9b'))
    good_msg = "KS-1401: 049's backfill takes the platform bypass\n\nFixes gate61 finding N-1383-1 on #1383.\nThis also concerns KS 1376.\n"
    res.append(arm('QMSG a clean message (Fixes gate61 ... #1383 is NOT strict)', lambda C: judge_message(C, good_msg), False, ''))
    res.append(arm('TMSGa "fixes #1383"', lambda C: judge_message(C, good_msg + 'fixes #1383\n'), True, 'S6c'))
    res.append(arm('TMSGb "does not close KS-1401" (Linear ignores negation)', lambda C: judge_message(C, good_msg + 'This does not close KS-1401.\n'), True, 'S6c'))
    res.append(arm('TMSGc KS-1376 hyphenated', lambda C: judge_message(C, good_msg + 'KS-1376\n'), True, 'S6b'))
    res.append(arm('TMSGd "(#1383)" in the subject', lambda C: judge_message(C, good_msg.replace('bypass\n', 'bypass (#1383)\n', 1)), True, 'S6a'))
    gb = 'Refs KS-1401\n\nhttps://linear.app/secuura/issue/KS-1401\n049 NEVER reaches demo; it lands with the kintsugi deploy. KS 1376 de-hyphenated.\n'
    res.append(arm('QBODY a clean body', lambda C: judge_body(C, gb), False, ''))
    res.append(arm('TBODYa "Closes: KS-1401"', lambda C: judge_body(C, gb + 'Closes: KS-1401\n'), True, 'B2'))
    res.append(arm('TBODYb "resolves #1383"', lambda C: judge_body(C, gb + 'this resolves #1383\n'), True, 'B2'))
    res.append(arm('TBODYc a second Refs line', lambda C: judge_body(C, gb + 'Refs KS-1401\n'), True, 'B3'))
    res.append(arm('TBODYd never-demo removed', lambda C: judge_body(C, gb.replace('NEVER reaches demo', 'reaches nothing')), True, 'B4'))
    res.append(arm('TBODYe KS-1376 hyphenated', lambda C: judge_body(C, gb + 'KS-1376\n'), True, 'B3'))
    res.append(arm('TBODYf "This does not close KS-1401" (the round-1 D1 class)', lambda C: judge_body(C, gb + 'This does not close KS-1401 as Done.\n'), True, 'B2'))
    real = 0
    if repo:
        try:
            git(repo, 'cat-file', '-e', K['head'] + '^{commit}'); have = True
        except SystemExit:
            have = False
        if have:
            res.append(arm('QREAL scope at the kit head over the round-1 head', lambda C: scope(C, repo, K['head'], K['round1_head']), False, '')); real += 1
            res.append(arm('TREAL scope with the ROUND-1 head posing as the round-2 commit', lambda C: scope(C, repo, K['round1_head'], K['round1_head']), True, 'S1')); real += 1
        else:
            print('INFO real-object arms SKIPPED: %s lacks %s (a SKIP is not a pass for the gate)' % (repo, K['head'][:12]))
    n = len(res); bad = n - sum(res)
    print('SELFTEST %d/%d arms behave (%d on real objects) | CHECKED %d' % (n - bad, n, real, n))
    return 0 if n and not bad else 1


def main():
    a = sys.argv[1:]
    if not a or a[0] in ('-h', '--help'): print(__doc__); return 0 if a else 2
    def opt(k, d=None): return a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else d
    repo = opt('--repo', K['checkout'])
    if a[0] == '--selftest': return selftest(repo)
    C = Checks()
    if a[0] == 'scope':
        H, P = opt('--head', K['head']), opt('--parent', K['round1_head'])
        for s in (H, P):
            if not re.fullmatch(r'[0-9a-f]{40}', s): print('REFUSING: %r is not a full 40-hex sha' % s); return 2
        print('scope %s over %s in %s' % (H[:12], P[:12], repo)); scope(C, repo, H, P)
    elif a[0] == 'body':
        bf = opt('--body-file')
        if not bf or not os.path.isfile(bf): print('REFUSING: --body-file <file> is required'); return 2
        bl = opt('--baseline-file'); judge_body(C, open(bf, encoding='utf-8').read(), open(bl, encoding='utf-8').read() if bl else None)
    else:
        print(__doc__); return 2
    return C.done()


if __name__ == '__main__':
    sys.exit(main())
