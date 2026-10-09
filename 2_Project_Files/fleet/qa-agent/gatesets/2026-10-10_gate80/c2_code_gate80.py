#!/usr/bin/env python3
"""c2_code_gate80.py — the commits' CODE CLAIMS, measured against the diffs (read verbs only). Carried in shape from c2_code_gate79.py
`claims`; [g80] rebuilt for #1441 and #1442. Every census is taken CODE-ONLY (comments blanked, strings kept) BESIDE the raw count.

  c2_code_gate80.py claims --repo R --pr 1441|1442 --head H --base B
  c2_code_gate80.py --selftest

#1441 (webhooks.ts deliveries): W0 CODE-ONLY multiset of added / removed lines in webhooks.ts == the guard + the removed `.catch`;
  W1 `.catch(() => [])` code-only census base 2 -> head 1, the survivor INSIDE dispatchEvent (+ a planted control that fires);
  W2 ORDER inside the deliveries handler: id-format 400 < UUID guard < `const db` < $queryRaw < res.json(rows);
  W3 the query is a tagged template binding exactly the id (1 interpolation); 0 Unsafe calls in the handler; originate-wide
     `$queryRawUnsafe(` / `$executeRawUnsafe(` / tagged counts base vs head;
  W4 the route's outer catch + fail500 are byte-identical base vs head, fail500's response body is the constant (the .message only goes to the log);
  W5 UUID_PATTERN and WEBHOOK_ID_PATTERN declarations identical base vs head; the SIBLING helper rejectInvalidWebhookId identical;
  W6 PREDICTION table: each candidate id evaluated against the two regexes (python `re`, the JS source patterns) -> 400 / 200 [] / query;
  W7 the ks1341c test file's `it(` titles base -> head (C0 gone; D0 D4 D3 control D added) and the file is the ONLY test file touched.
#1442 (check-package-format.sh): S0 CODE-ONLY (full-line `#` comments blanked) added / removed lines == the one npm line; raw +4/-1;
  S1 `< /dev/null` sits INSIDE the `$( ... )`, after `cd "$dir" &&`, on the npm command, before `2>&1`; S2 `2>&1` still last on that line;
  S3 `done <<< "$selected"` once, `changed_paths="$(cat)"` once, the mode `case` block identical; S4 STDIN-CONSUMER CENSUS of every command
  line inside the `while IFS= read -r p` loop (printed for the gate to rule: which could read the loop's stdin); S5 suite file: 100644,
  header says `bash <file>`, 9 `check ` cells.
BOTH: D1 each doc change is a PURE INSERTION (one contiguous block; head minus the block == base byte for byte), position printed.
rc 0 all pass / 1 a FAIL / 2 refused."""
import difflib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate80 import K, PR, Tally, git, show, blob, req, code_only, span, resolvable

JS_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$')
JS_UUID = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
H_END = r'^\}\);[ \t]*$'


def norm(l): return re.sub(r'\s+', ' ', l).strip()


def added_removed(a, b):
    """multiset diff of normalised non-blank lines: (added, removed)."""
    la = [norm(x) for x in a.split('\n') if x.strip()]; lb = [norm(x) for x in b.split('\n') if x.strip()]
    add, rem = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes():
        if op in ('replace', 'delete'): rem += la[i1:i2]
        if op in ('replace', 'insert'): add += lb[j1:j2]
    return add, rem


def sh_code_only(txt):
    return '\n'.join('' if l.lstrip().startswith('#') else l for l in txt.split('\n'))


def catch_census(src):
    co = code_only(src)
    return co.count('.catch(() => [])'), src.count('.catch(() => [])')


def pure_insertion(base, head):
    """-> (ok, info). head == base with ONE contiguous block inserted; removing the block gives base byte for byte."""
    la = base.split('\n'); lb = head.split('\n')
    ops = [o for o in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if o[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert': return False, 'opcodes %s' % [(o[0], o[1], o[2], o[3], o[4]) for o in ops[:4]]
    _, i1, _, j1, j2 = ops[0]
    rebuilt = '\n'.join(lb[:j1] + lb[j2:])
    return rebuilt == base, 'one insertion of %d line(s) at head line %d of %d (base %d lines); head minus block == base: %s; first line %r; next line %r' % (
        j2 - j1, j1 + 1, len(lb), len(la), rebuilt == base, lb[j1][:60], (lb[j2] if j2 < len(lb) else '<EOF>')[:60])


def deliveries(src):
    s, e = span(src, K['prs']['1441']['route_anchor'], H_END)
    return s, e, src[s:e]


def order_ok(h):
    """positions of the handler's order anchors (code-only text): all present once, strictly increasing."""
    a = ['!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(req.params.id)', '!UUID_PATTERN.test(req.params.id)', 'const db = (req as any).db || prisma;',
         'db.$queryRaw`', 'deliveries: rows']
    pos = [h.find(x) for x in a]
    cnt = [h.count(x) for x in a]
    return all(c == 1 for c in cnt) and pos == sorted(pos), list(zip([x[:34] for x in a], pos, cnt))


def loop_body(sh):
    i = sh.find('while IFS= read -r p; do')
    j = sh.find('done <<< "$selected"')
    return (sh[i:j] if i >= 0 and j > i else ''), i, j


def stdin_census(body):
    """every line inside the loop with an external-command word; flags: which have a pipe feeding them / an explicit redirect."""
    rows = []
    for n, l in enumerate(body.split('\n'), 1):
        t = l.strip()
        if not t or t.startswith('#'): continue
        for cmd in ('npm', 'node', 'cat', 'grep', 'sed', 'printf', 'echo', 'read', 'cd', 'git', 'cut', 'awk', 'head', 'tail', 'tr', 'xargs'):
            if re.search(r'(^|[\s$(|&;"])%s(?=[\s)|;&"]|$)' % cmd, t) and not re.match(r'^(echo|printf)\s+"?\[format-gate\]', t):
                rows.append((n, cmd, '< /dev/null' in t, '|' in t, t[:110]))
    return rows


def run1441(repo, head, base):
    t = Tally(); P = PR(1441); wh = P['route_file']
    b, h = show(repo, base, wh), show(repo, head, wh)
    if not b or not h: print('REFUSED: webhooks.ts absent at base or head'); return 2
    cb, ch = code_only(b), code_only(h)
    add, rem = added_removed(cb, ch)
    want_add = ['if (!UUID_PATTERN.test(req.params.id)) {', 'return res.json({ success: true, deliveries: [] });', '}', '`;']
    want_rem = ['`.catch(() => []);']
    t.check('W0', sorted(add) == sorted(want_add) and sorted(rem) == sorted(want_rem),
            'CODE-ONLY multiset in %s base %s -> head %s: added %s removed %s (raw numstat +6/-1 beside; the 5 other added raw lines are comments)' % (wh.split('/')[-1], blob(repo, base, wh)[-12:], blob(repo, head, wh)[-12:], add, rem))
    (cob, rawb), (coh, rawh) = catch_census(b), catch_census(h)
    di = h.find('export async function dispatchEvent')
    surv = [m.start() for m in re.finditer(re.escape('.catch(() => [])'), ch)]
    plant = catch_census(h + '\nconst x = await q.catch(() => []);\n')[0]
    t.check('W1', cob == 2 and coh == 1 and len(surv) == 1 and di >= 0 and surv[0] > di and plant == coh + 1,
            '.catch(() => []) CODE-ONLY base %d (raw %d) -> head %d (raw %d); survivor offset %s is after `export async function dispatchEvent` %d: %s | CONTROL planted extra reads %d (must be head+1)' % (
                cob, rawb, coh, rawh, surv, di, bool(surv) and surv[0] > di, plant))
    hs, he, hh = deliveries(ch)
    ok, info = order_ok(hh)
    t.check('W2', ok, 'ORDER inside the deliveries handler (code-only; name, offset, count): %s' % info)
    bs, be, bh = deliveries(cb)
    q = re.findall(r'db\.\$queryRaw`.*?`', hh, re.S)
    interp = re.findall(r'\$\{([^}]*)\}', q[0]) if q else None
    unsafe_h = len(re.findall(r'\$(query|execute)RawUnsafe\(', hh))
    glob = lambda s: (len(re.findall(r'\$queryRawUnsafe\(', s)), len(re.findall(r'\$executeRawUnsafe\(', s)), len(re.findall(r'\$queryRaw`', s)))
    t.check('W3', len(q) == 1 and interp == ['req.params.id'] and unsafe_h == 0 and glob(cb)[:2] == glob(ch)[:2],
            'handler queries %d, interpolations %s, Unsafe calls in handler %d | file-wide (queryRawUnsafe, executeRawUnsafe, tagged $queryRaw) base %s -> head %s' % (len(q), interp, unsafe_h, glob(cb), glob(ch)))
    def catch_of(hnd): return hnd[hnd.rfind('} catch (err: any) {'):]
    fb = re.search(r'function fail500\(.*?\n\}', cb, re.S); fh = re.search(r'function fail500\(.*?\n\}', ch, re.S)
    body = fh.group(0) if fh else ''
    resp = re.search(r'res\.status\(500\)\.json\((.*)\);', body)
    t.check('W4', catch_of(bh) == catch_of(hh) and bool(fh) and fb and fb.group(0) == fh.group(0) and bool(resp) and '.message' not in resp.group(1) and not re.search(r'\berr\b', resp.group(1)),
            'outer catch identical base/head: %s | fail500 identical: %s | its response body %r carries no `err` / `.message` (the .message goes only to logger.error)' % (
                catch_of(bh) == catch_of(hh), bool(fb and fh and fb.group(0) == fh.group(0)), resp.group(1) if resp else None))
    decl = lambda s, n: re.findall(r'const %s = .*' % n, s)
    sb = re.search(r'export function rejectInvalidWebhookId.*?\n\}', cb, re.S); sh_ = re.search(r'export function rejectInvalidWebhookId.*?\n\}', ch, re.S)
    t.check('W5', decl(cb, 'UUID_PATTERN') == decl(ch, 'UUID_PATTERN') != [] and decl(cb, 'WEBHOOK_ID_PATTERN') == decl(ch, 'WEBHOOK_ID_PATTERN') != [] and bool(sb and sh_ and sb.group(0) == sh_.group(0)),
            'UUID_PATTERN %s | WEBHOOK_ID_PATTERN %s | sibling helper identical base/head: %s (it answers 404 for a non-UUID id on the OTHER routes)' % (
                decl(ch, 'UUID_PATTERN'), decl(ch, 'WEBHOOK_ID_PATTERN'), bool(sb and sh_ and sb.group(0) == sh_.group(0))))
    # the declared regexes must be the ones evaluated below
    srcs_ok = 'a-fA-F' not in ''.join(decl(ch, 'UUID_PATTERN')) and '/i;' in ''.join(decl(ch, 'UUID_PATTERN'))
    t.check('W6-PRE', srcs_ok, 'the python UUID regex mirrors the declared one (hex class 0-9a-f, /i flag): %s' % srcs_ok)
    u = '7a1f3d2b-2c3d-4e4f-9051-6b7c8d9e0f1a'
    cands = [('hyphenated lowercase UUID', u), ('same UUID UPPERCASED', u.upper()), ('same 32 hex WITHOUT hyphens', u.replace('-', '')),
             ('32 hex, hyphens in the wrong places', '7a1f-3d2b2c3d-4e4f9051-6b7c8d9e0f1a'), ('36-char non-hex (hyphenated)', 'zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz'),
             ('the string 0', '0'), ('garbage string', 'not-a-uuid'), ('fails the id-format regex', '-bad id')]
    pred = {}
    for name, v in cands:
        a = 'query' if (JS_ID.match(v) and JS_UUID.match(v)) else ('400' if not JS_ID.match(v) else '200 [] (no query)')
        pred[name] = a; t.info('W6', '%-38s %-40r HEAD route predicts: %s | the sibling helper would answer: %s' % (
            name, v, a, '400' if not JS_ID.match(v) else ('404' if not JS_UUID.match(v) else 'query')))
    t.check('W6', pred['same 32 hex WITHOUT hyphens'] == '200 [] (no query)' and pred['hyphenated lowercase UUID'] == 'query' and pred['fails the id-format regex'] == '400' and pred['garbage string'] == '200 [] (no query)',
            'PREDICTION (READ, never evidence): the unhyphenated 32-hex id passes the id-format regex and FAILS UUID_PATTERN -> head answers 200 [] with 0 db calls; the hyphenated UUID reaches the query. Whether POSTGRES accepts the unhyphenated form in ::uuid is UNMEASURED (no database); the gate PROBES the router, and cites Postgres docs or says UNMEASURED')
    tf = P['test_file']
    its = lambda s: re.findall(r"\bit(?:\.each\([^)]*\))?\(\s*'((?:[^'\\]|\\.)*)'", s)
    tb, th = its(show(repo, base, tf)), its(show(repo, head, tf))
    gone = [x for x in tb if x not in th]; new = [x for x in th if x not in tb]
    t.check('W7', len(tb) == 6 and len(th) == 9 and len(gone) == 1 and 'control KS-1341 C0' in gone[0] and len(new) == 4
            and sum(1 for x in new if x.startswith('RED KS-1345 D')) == 3 and sum(1 for x in new if x.startswith('control KS-1345 D')) == 1,
            'ks1341c `it(` / `it.each(` definitions base %d -> head %d (executed counts differ: the two it.each expand per route); gone %s; new %s' % (len(tb), len(th), [x[:50] for x in gone], [x[:44] for x in new]))
    other_tests = [p for p in git(repo, 'diff', '--name-only', base, head).split('\n') if '__tests__' in p and p != tf]
    t.check('W7b', not other_tests, 'test files touched other than ks1341c: %s' % (other_tests or 0))
    docs(repo, head, base, t, P)
    return t.end()


def docs(repo, head, base, t, P):
    for d in P['doc_paths']:
        b, h = show(repo, base, d), show(repo, head, d)
        ok, info = pure_insertion(b, h)
        t.check('D1', bool(b) and bool(h) and ok, '%s: %s' % (d.split('/')[-1], info))
    # planted: a doc with one base line altered must FAIL pure_insertion
    b = show(repo, base, P['doc_paths'][0]); h = show(repo, head, P['doc_paths'][0]).replace('<html', '<HTML', 1)
    t.check('D1-CONTROL', not pure_insertion(b, h)[0], 'CONTROL: the head doc with one base byte altered is NOT a pure insertion (the instrument can fail)')


def run1442(repo, head, base):
    t = Tally(); P = PR(1442); g = P['gate_script']
    b, h = show(repo, base, g), show(repo, head, g)
    if not b or not h: print('REFUSED: the gate script is absent at base or head'); return 2
    cb, ch = sh_code_only(b), sh_code_only(h)
    add, rem = added_removed(cb, ch)
    npm_b = 'out="$(cd "$dir" && npm run --silent format:check 2>&1)"'; npm_h = 'out="$(cd "$dir" && npm run --silent format:check < /dev/null 2>&1)"'
    raw_add, raw_rem = added_removed(b.replace('\r', ''), h.replace('\r', ''))
    t.check('S0', add == [npm_h] and rem == [npm_b] and len(raw_add) == 4 and len(raw_rem) == 1,
            'CODE-ONLY (full-line # comments blanked) added %s removed %s | RAW added %d removed %d (numstat +4/-1: the 3 comment lines + the npm line)' % (add, rem, len(raw_add), len(raw_rem)))
    ln = [l for l in h.split('\n') if 'npm run --silent format:check' in l and not l.lstrip().startswith('#')]
    L = ln[0] if len(ln) == 1 else ''
    m = re.match(r'^\s*out="\$\(cd "\$dir" && npm run --silent format:check < /dev/null 2>&1\)"$', L)
    t.check('S1', bool(m) and 0 <= L.find('cd "$dir" &&') < L.find('< /dev/null') < L.find('2>&1') and L.count('< /dev/null') == 1 and ch.count('< /dev/null') == 1,
            'npm lines at head %d; `< /dev/null` count CODE-ONLY in the file %d (raw %d: the comment names it); on the npm command inside $( ... ) after `cd "$dir" &&` and before `2>&1`: %s' % (len(ln), ch.count('< /dev/null'), h.count('< /dev/null'), bool(m)))
    t.check('S2', L.endswith('2>&1)"') and 0 <= L.find('< /dev/null') < L.find('2>&1'), '`2>&1` is still the last redirect, so stderr lands in $out: %s' % L.strip())
    body_h, i, j = loop_body(ch); body_b, _, _ = loop_body(cb)
    case_b = re.search(r'case "\$\{1:-\}" in.*?esac', cb, re.S); case_h = re.search(r'case "\$\{1:-\}" in.*?esac', ch, re.S)
    t.check('S3', ch.count('done <<< "$selected"') == 1 and ch.count('changed_paths="$(cat)"') == 1 and bool(case_b and case_h and case_b.group(0) == case_h.group(0)) and cb.count('done <<< "$selected"') == 1,
            '`done <<< "$selected"` x%d (base x%d), `changed_paths="$(cat)"` x%d, mode `case` block identical base/head: %s' % (
                ch.count('done <<< "$selected"'), cb.count('done <<< "$selected"'), ch.count('changed_paths="$(cat)"'), bool(case_b and case_h and case_b.group(0) == case_h.group(0))))
    rows = stdin_census(body_h)
    cat_in_loop = [r for r in rows if r[1] in ('cat', 'read') and r[1] == 'cat']
    t.check('S4', bool(body_h) and not cat_in_loop and any(r[1] == 'npm' and r[2] for r in rows),
            'STDIN-CONSUMER CENSUS: %d command line(s) inside the loop; a bare `cat` in the loop: %s; the npm line carries `< /dev/null`: %s (each row below is for the gate to RULE)' % (
                len(rows), bool(cat_in_loop), any(r[1] == 'npm' and r[2] for r in rows)))
    for n, cmd, redir, pipe, text in rows: t.info('S4', 'loop line %3d %-6s explicit-null-stdin=%-5s pipe-on-line=%-5s %s' % (n, cmd, redir, pipe, text))
    ctl = stdin_census('  x="$(cat)"')
    t.check('S4-CONTROL', any(r[1] == 'cat' for r in ctl), 'CONTROL: a planted bare `cat` inside a loop IS listed by the census')
    s = P['suite']; sb = show(repo, head, s)
    cells = len(re.findall(r'^\s*check "', sb, re.M))
    t.check('S5', bool(sb) and blob(repo, head, s).startswith('100644') and 'Usage: bash systemTest/__tests__/' in sb and cells >= 9 - 0,
            'new suite %s: mode %s, `check "` call sites %d (the READY says 9 cells; some cells call check twice), usage line says `bash <file>`' % (s.split('/')[-1], blob(repo, head, s)[:6], cells))
    docs(repo, head, base, t, P)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    a = 'x = 1;\n// c.catch(() => [])\nq`s`.catch(() => []);\n'
    rep(catch_census(a) == (1, 2), 'code_only census: a comment mention is blanked (code 1, raw 2)')
    rep(catch_census('const s = ".catch(() => [])";\n')[0] == 1, 'a string mention is KEPT (strings are code)')
    rep(catch_census('')[0] == 0, 'an empty file reads 0')
    ad, rm = added_removed('a\nb\nc', 'a\nB\nc\nd'); rep(ad == ['B', 'd'] and rm == ['b'], 'added_removed: replace + insert')
    ok, _ = pure_insertion('a\nb\n', 'a\nNEW\nb\n'); rep(ok, 'pure_insertion: one inserted line passes')
    ok, _ = pure_insertion('a\nb\n', 'a\nNEW\nB\n'); rep(not ok, 'PLANTED altered base line FAILS pure_insertion')
    ok, _ = pure_insertion('a\nb\n', 'a\nN1\nb\nN2\n'); rep(not ok, 'PLANTED two separate insertions FAIL (one contiguous block only)')
    ok, _ = pure_insertion('a\nb\n', 'a\nb\n'); rep(not ok, 'PLANTED no change FAILS (nothing inserted)')
    good = "x\nwebhooksRouter.get('/:id/deliveries', async (req, res) => {\n  try {\n    if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(req.params.id)) {\n      return 1;\n    }\n    if (!UUID_PATTERN.test(req.params.id)) {\n      return 2;\n    }\n    const db = (req as any).db || prisma;\n    const rows = await db.$queryRaw`SELECT ${req.params.id}::uuid`;\n    res.json({ success: true, deliveries: rows });\n  } catch (err: any) {\n    fail500(res, 'c', err);\n  }\n});\ny\n"
    s0, e0, hh = deliveries(good); rep(order_ok(hh)[0], 'order_ok: id regex < UUID guard < db < query < rows passes')
    swapped = good.replace("    if (!UUID_PATTERN.test(req.params.id)) {\n      return 2;\n    }\n", "").replace("    const db", "    if (!UUID_PATTERN.test(req.params.id)) {\n      return 2;\n    }\n    const db").replace("    if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(req.params.id)) {\n      return 1;\n    }\n", "")
    rep(not order_ok(deliveries(swapped)[2])[0], 'PLANTED handler without the id-format check (anchor absent) FAILS the order check')
    late = good.replace("    if (!UUID_PATTERN.test(req.params.id)) {\n      return 2;\n    }\n", "").replace("    res.json", "    if (!UUID_PATTERN.test(req.params.id)) {\n      return 2;\n    }\n    res.json")
    rep(not order_ok(deliveries(late)[2])[0], 'PLANTED guard AFTER the query FAILS the order check')
    try: span(good + good, "webhooksRouter.get('/:id/deliveries'", H_END); rep(False, 'a doubled anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: the route anchor twice -> refused')
    try: span('nothing', "webhooksRouter.get('/:id/deliveries'", H_END); rep(False, 'an absent anchor was ACCEPTED')
    except SystemExit: rep(True, 'ARM: the route anchor absent -> refused')
    u = '7a1f3d2b-2c3d-4e4f-9051-6b7c8d9e0f1a'
    rep(JS_ID.match(u.replace('-', '')) and not JS_UUID.match(u.replace('-', '')) and JS_UUID.match(u.upper()) and JS_ID.match(u) and JS_UUID.match(u), 'regex mirror: 32-hex passes id-format and fails UUID; UPPERCASE UUID passes; hyphenated passes both')
    rep(not JS_ID.match('-bad id') and JS_ID.match('0') and not JS_UUID.match('0'), 'regex mirror: `0` passes id-format, fails UUID; `-bad id` fails id-format')
    sh = 'x\n# note\nwhile IFS= read -r p; do\n    out="$(cd "$dir" && npm run --silent format:check < /dev/null 2>&1)"\n    printf \'%s\\n\' "$w" | grep -qxF "$f"\ndone <<< "$selected"\n'
    rows = stdin_census(loop_body(sh)[0]); rep(any(r[1] == 'npm' and r[2] for r in rows) and any(r[1] == 'grep' and r[3] for r in rows), 'stdin census lists the npm line (null stdin) and the piped grep')
    rep(not any(r[1] == 'npm' and r[2] for r in stdin_census(loop_body(sh.replace(' < /dev/null', ''))[0])), 'PLANTED npm line without `< /dev/null` is flagged (explicit-null-stdin False)')
    rep(any(r[1] == 'cat' for r in stdin_census('  x="$(cat)"')) and any(r[1] == 'cat' for r in stdin_census('cat | wc')), 'stdin census sees `$(cat)` and a piped `cat` (the closing paren and the pipe are word ends)')
    rep(sh_code_only('a\n  # x\nb').split('\n') == ['a', '', 'b'], 'sh_code_only blanks full-line comments only')
    try: req(['--repo', 'x', '--head', 'abc'], '--head', hex40=True); rep(False, 'short head ACCEPTED')
    except SystemExit: rep(True, 'REQUIRED-ARG ARM short --head -> refused')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A or A[0] != 'claims': print(__doc__); return 2
    try:
        repo = req(A, '--repo'); n = req(A, '--pr'); head = req(A, '--head', True); base = req(A, '--base', True); PR(n)
    except SystemExit as e:
        print(e); return 2
    for s, nm in ((head, 'head'), (base, 'base')):
        if not resolvable(repo, s): print('REFUSED: %s %s is not in %s' % (nm, s, repo)); return 2
    print('C2 claims #%s head %s base %s repo %s' % (n, head, base, repo))
    return run1441(repo, head, base) if n == '1441' else (run1442(repo, head, base) if n == '1442' else 2)


if __name__ == '__main__':
    sys.exit(main())
