#!/usr/bin/env python3
"""c2_code_gate81.py — the commits' CODE CLAIMS, measured against the diffs (read verbs only; `node -e` evaluates a pure expression, nothing else).
Carried in shape from c2_code_gate80.py `claims`; [g81] rebuilt for #1443, #1444, #1445 and #1446. Every census is taken CODE-ONLY (comments blanked,
strings kept) BESIDE the raw count.

  c2_code_gate81.py claims --repo R --pr 1443|1444|1445|1446 --head H --base B
  c2_code_gate81.py --selftest

#1443 (api-gateway fail500 x3, KS-1346): A0 CODE-ONLY multiset of added / removed lines in EACH of notifications.ts, batch.ts, audit-export.ts == the one
  logger.error line (raw +4/-1 beside: 3 comment lines); A1 the new log EXPRESSION is byte-identical in the three files AND to originate adminConfig.ts:104
  at base (length printed; the PR #1443 body says 263 B and #1446's says 262 B: both are READ here); the pre-ruling `String(err)` text is the CONTROL;
  A2 fail500's response is the constant body in all three (no `err` / `.message`); A3 the expression EVALUATED (node) over 14 thrown values beside
  `String(err)`: FACTS for the gate (a thrown STRING and an Error's .message are logged verbatim); A4 residual `String(err)` / `.message` census over
  api-gateway/src/routes at head (class siblings, REPORTED); A5 the test file's definitions (5 it.each x 3 routes = 15) and the routes it drives.
#1446 (api-gateway audit-export 502, KS-1410): B0 CODE-ONLY multiset == the logger.error line + the constant message in, the template message out;
  B1 the new expression == adminConfig.ts:104 == #1443's (byte-identical); B2 `.message` census of audit-export.ts base -> head; B3 the non-ok branch is
  byte-identical (it still passes the upstream error through); B4 logger.error PRECEDES res.status(502) inside the catch; B5 the test file: 9 cells, X4 is
  the cell that carries `thrown Object with fields [password, host]`; B6 this file's own fail500 at :25 is still the PRE-ruling `String(err)` line at THIS head
  (the cross-PR fact: #1443 changes it).
#1445 (transfer process-expired, KS-1410): T0 CODE-ONLY multiset == the logger import + logger.error + the constant 500; T1 Q-4XX: every `.message` site of
  delegations.ts base -> head with its line numbers (the four 4xx sites are byte-identical, only their line numbers move by the import); T2 the catch's
  structure: `if (error instanceof Error) {... return ...}` then `next(error)` (a non-Error throw never reaches the log line: no cell exercises it);
  T3 `../utils/logger` exists at base; T4 the test file's definitions (T1 x3, T2, TC1, TC2 = 6).
#1444 (check-shared-relink.sh, KS-937): R0 CODE-ONLY (full-line # comments blanked) multiset == the two changed awk lines; raw +10/-2; R1 the regex line
  change is EXACTLY the prefix group `(\\/[^ \\t]*\\/)?` -> `([^ \\t]*\\/)?`; R2 the USER line carries the guard `if (u !~ /^:/)` exactly once (the ruled
  deviation) and the group drop; R3 effective_user_is_unprivileged() identical base/head (it reads "" as root: why the deviation exists); R4 the suite
  diff is a pure insertion of 80 lines holding 6 new cells (F-C x2, F-E x3, the F-E pin) and the base declared-cell census (expect / row_case / nonjs_case);
  R5 both files stay 100755.
ALL FOUR: D1 each doc change is a PURE INSERTION (one contiguous block; head minus the block == base byte for byte), position printed, and the flow block
  heading carries the kit's number (45. / 50. / 47. / 46.).
rc 0 all pass / 1 a FAIL / 2 refused."""
import difflib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate81 import K, PR, Tally, git, show, blob, req, code_only, resolvable

EXPR_RX = re.compile(r"\berror: (err instanceof Error \? err\.message : .*?: 'thrown ' \+ typeof err)\s*\}\s*\)\s*;?")
PRE_RULING = 'err instanceof Error ? err.message : String(err)'
PRECEDENT = (K['ruled_expression']['precedent_path'], K['ruled_expression']['precedent_line'])


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


def pure_insertion(base, head):
    """-> (ok, info). head == base with ONE contiguous block inserted; removing the block gives base byte for byte."""
    la = base.split('\n'); lb = head.split('\n')
    ops = [o for o in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if o[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'insert': return False, 'opcodes %s' % [(o[0], o[1], o[2], o[3], o[4]) for o in ops[:4]]
    _, i1, _, j1, j2 = ops[0]
    rebuilt = '\n'.join(lb[:j1] + lb[j2:])
    return rebuilt == base, 'one insertion of %d line(s) at head line %d of %d (base %d lines); head minus block == base: %s; first line %r; next line %r' % (
        j2 - j1, j1 + 1, len(lb), len(la), rebuilt == base, lb[j1][:60], (lb[j2] if j2 < len(lb) else '<EOF>')[:60])


def expr_of(src):
    """the ruled-expression text of the (one) logger.error line that carries it, from CODE-ONLY text; None when absent or ambiguous."""
    ms = EXPR_RX.findall(code_only(src))
    return ms[0] if len(ms) == 1 else None


def eval_table(expr):
    """the expression EVALUATED over fixed thrown values (node -e): -> {label: (ruled, string_err)}. FACTS only."""
    js = r"""
const f = new Function('err', 'return (' + process.argv[1] + ');');
const g = new Function('err', 'return (' + process.argv[2] + ');');
class DbFault { constructor(){ this.code='ECONNREFUSED'; this.dsn='postgres://svc:SECRET@10.0.4.17/app'; } }
const nullProto = Object.create(null); nullProto.password = 'SECRET';
const throwingKeys = new Proxy({}, { ownKeys() { throw new Error('ownKeys trap'); } });
const cases = [
 ['Error("boom SECRET-in-message")', new Error('boom SECRET-in-message')],
 ['Error("")', new Error('')],
 ['string "postgres://svc:SECRET@host/db"', 'postgres://svc:SECRET@host/db'],
 ['plain object {password, host}', {password: 'SECRET', host: 'h'}],
 ['class instance DbFault', new DbFault()],
 ['null-prototype object', nullProto],
 ['array [1,2]', [1, 2]],
 ['null', null], ['undefined', undefined], ['number 42', 42], ['boolean true', true],
 ['function', function foo() {}],
 ['symbol', Symbol('s')],
 ['object whose ownKeys trap throws', throwingKeys],
];
const out = {};
for (const [label, v] of cases) {
  const one = (fn) => { try { return String(fn(v)); } catch (e) { return 'THROWS ' + (e && e.message); } };
  out[label] = [one(f), one(g)];
}
console.log(JSON.stringify(out));
"""
    p = subprocess.run(['node', '-e', js, expr, PRE_RULING], capture_output=True, text=True, timeout=60)
    if p.returncode: raise SystemExit('eval_table: node rc %d %s' % (p.returncode, p.stderr[:200]))
    return json.loads(p.stdout)


def fail500_of(src):
    m = re.search(r'function fail500\(.*?\n\}', src, re.S)
    return m.group(0) if m else None


def docs(repo, head, base, t, P):
    for d in P['doc_paths']:
        b, h = show(repo, base, d), show(repo, head, d)
        ok, info = pure_insertion(b, h)
        t.check('D1', bool(b) and bool(h) and ok, '%s: %s' % (d.split('/')[-1], info))
    b = show(repo, base, P['doc_paths'][0]); h = show(repo, head, P['doc_paths'][0])
    la, lb = b.split('\n'), h.split('\n')
    ops = [o for o in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if o[0] != 'equal']
    frag = '\n'.join(lb[ops[0][3]:ops[0][4]]) if len(ops) == 1 else ''
    t.check('D1b', ('<h2>%s ' % P['flow_block']) in frag and frag.count('<h2>') == 1, 'flow doc fragment opens with <h2>%s (flow numbers in the fragment: %s)' % (P['flow_block'], re.findall(r'<h2>(\d+)\.', frag)))
    h2 = h.replace('<html', '<HTML', 1)
    t.check('D1-CONTROL', not pure_insertion(b, h2)[0], 'CONTROL: the head doc with one base byte altered is NOT a pure insertion (the instrument can fail)')


def run1443(repo, head, base):
    t = Tally(); P = PR(1443); exprs = {}; fb = {}
    new_line = "logger.error(context, { error: <RULED> });"
    for f in P['route_files']:
        b, h = show(repo, base, f), show(repo, head, f)
        if not b or not h: print('REFUSED: %s absent at base or head' % f); return 2
        cb, ch = code_only(b), code_only(h)
        add, rem = added_removed(cb, ch); nm = f.split('/')[-1]
        e = expr_of(h); exprs[nm] = e
        ok = (len(add) == 1 and len(rem) == 1 and e is not None and add[0] == norm('logger.error(context, { error: %s });' % e) and rem[0] == norm('logger.error(context, { error: %s });' % PRE_RULING))
        raw_a, raw_r = added_removed(b, h)
        t.check('A0', ok, '%s CODE-ONLY multiset: added %d removed %d (the ONE logger.error line, pre-ruling -> ruled) | RAW added %d removed %d (numstat %s: the 3 extra added raw lines are comments) | base blob %s -> head %s' % (
            nm, len(add), len(rem), len(raw_a), len(raw_r), P['numstat'][f], blob(repo, base, f)[-12:], blob(repo, head, f)[-12:]))
        fb[nm] = (fail500_of(ch), fail500_of(cb))
    pb = show(repo, base, PRECEDENT[0]); pe = expr_of(pb)
    vals = list(exprs.values())
    t.check('A1', all(vals) and len(set(vals)) == 1 and pe is not None and vals[0] == pe and PRE_RULING not in vals[0],
            'ruled expression byte-identical in %d files AND to %s:%d at base: %s | length %d bytes (the #1443 BODY says 263 B, the #1446 BODY says 262 B: the instrument reads %d for the expression text alone) | CONTROL the pre-ruling text %r differs: %s' % (
                len(vals), PRECEDENT[0].split('/')[-1], PRECEDENT[1], bool(vals and pe and vals[0] == pe), len((pe or '').encode()), len((pe or '').encode()), PRE_RULING, PRE_RULING != (pe or '')))
    cons = []
    for nm, (fh, fbase) in fb.items():
        resp = re.search(r"res\.status\(500\)\.json\((.*)\);", fh or '')
        cons.append(bool(resp) and '.message' not in resp.group(1) and not re.search(r'\berr\b', resp.group(1)) and "message: 'Internal server error'" in resp.group(1))
        # fail500 identical to base except the one logger line
        same = bool(fh and fbase) and [norm(x) for x in fh.split('\n') if x.strip() and 'logger.error' not in x] == [norm(x) for x in fbase.split('\n') if x.strip() and 'logger.error' not in x]
        cons.append(same)
    t.check('A2', all(cons), 'fail500 in the 3 files: response is the constant body (no `err` / `.message`) and the function is identical to base outside the logger line: %s' % cons)
    if pe:
        tab = eval_table(pe)
        for lab, (ruled, old) in tab.items(): t.info('A3', '%-38s ruled -> %-62s | String(err) -> %s' % (lab, ruled[:62], old[:50]))
        leak_string = tab['string "postgres://svc:SECRET@host/db"'][0] == 'postgres://svc:SECRET@host/db'
        leak_msg = 'SECRET-in-message' in tab['Error("boom SECRET-in-message")'][0]
        obj = tab['plain object {password, host}']
        t.check('A3', obj[0] == 'thrown Object with fields [password, host]' and obj[1] == '[object Object]' and leak_string and leak_msg,
                'EVALUATED over %d thrown values: a plain object logs its TYPE and FIELD NAMES (String(err) logged "[object Object]"); a thrown STRING is still logged VERBATIM (%s) and an Error\'s .message is still logged (%s): the gate measures what the cells prove, never "no longer leaks"' % (len(tab), leak_string, leak_msg))
    else:
        t.check('A3', False, 'no expression to evaluate')
    resid = {}
    out = git(repo, 'ls-tree', '-r', '--name-only', head, 'Blockchain/Dev/services/api-gateway/src/routes/').split('\n')
    for f in [x for x in out if x.endswith('.ts') and '__tests__' not in x]:
        c = code_only(show(repo, head, f)); n1, n2 = c.count('String(err)'), len(re.findall(r'\berr(or)?\.message\b', c))
        if n1 or n2: resid[f.split('/')[-1]] = (n1, n2)
    t.info('A4', 'residual CODE-ONLY `String(err)` / `err.message` counts in api-gateway/src/routes at the head (String(err), .message): %s (REPORTED for the gate: class siblings of the same fix)' % resid)
    tf = P['test_file']; ts = show(repo, head, tf)
    its = re.findall(r"\bit(?:\.each\([^)]*\))?\(\s*'((?:[^'\\]|\\.)*)'", ts)
    routes = re.findall(r"router: ([a-z]\w*Router),", ts)
    t.check('A5', len(its) == 5 and routes == ['notificationsRouter', 'batchRouter', 'auditExportRouter'] and len(its) * len(routes) == P['claims']['cells'],
            'test file %s: %d `it.each` definitions x %d routes (%s) = %d cells (the seat claims %d); only this test file is added (c1 P3)' % (tf.split('/')[-1], len(its), len(routes), routes, len(its) * len(routes), P['claims']['cells']))
    docs(repo, head, base, t, P)
    return t.end()


def run1446(repo, head, base):
    t = Tally(); P = PR(1446); f = P['route_files'][0]
    b, h = show(repo, base, f), show(repo, head, f)
    if not b or not h: print('REFUSED: audit-export.ts absent at base or head'); return 2
    cb, ch = code_only(b), code_only(h)
    add, rem = added_removed(cb, ch); e = expr_of(h)
    want_add = [norm("logger.error('Audit export could not reach the security service (GET /api/admin/audit/export)', { error: %s });" % (e or '<NONE>')), "message: 'Failed to reach security service',"]
    want_rem = ["message: `Failed to reach security service: ${err.message}`,"]
    raw_a, raw_r = added_removed(b, h)
    t.check('B0', sorted(add) == sorted(want_add) and sorted(rem) == sorted(want_rem),
            'CODE-ONLY multiset in audit-export.ts base %s -> head %s: added %d removed %d | RAW added %d removed %d (numstat %s: the rest are WHY comments) | added %s | removed %s' % (
                blob(repo, base, f)[-12:], blob(repo, head, f)[-12:], len(add), len(rem), len(raw_a), len(raw_r), P['numstat'][f], [x[:60] for x in add], rem))
    pe = expr_of(show(repo, base, PRECEDENT[0])); e43 = expr_of(show(repo, PR(1443)['head_expected'], f)) if resolvable(repo, PR(1443)['head_expected']) else None
    t.check('B1', e is not None and e == pe and (e43 is None or e == e43) and len((e or '').encode()) == 262,
            'the new expression == %s:%d at base: %s | == #1443\'s fail500 expression: %s | length %d bytes (this PR\'s body says 262 B; #1443\'s says 263 B)' % (
                PRECEDENT[0].split('/')[-1], PRECEDENT[1], e == pe, (e == e43) if e43 else 'NOT READ (#1443 head absent)', len((e or '').encode())))
    mb = len(re.findall(r'\berr\.message\b', cb)); mh = len(re.findall(r'\berr\.message\b', ch))
    t.check('B2', '${err.message}' in cb and '${err.message}' not in ch and mb == mh,
            'CODE-ONLY `err.message` occurrences in audit-export.ts base %d -> head %d (the 502 template `${err.message}` is GONE: base had it %s, head has it %s; the new log line\'s expression adds the one that replaces it); remaining sites by line: base %s -> head %s' % (
                mb, mh, '${err.message}' in cb, '${err.message}' in ch, [i + 1 for i, l in enumerate(cb.split('\n')) if re.search(r'\berr\.message\b', l)], [i + 1 for i, l in enumerate(ch.split('\n')) if re.search(r'\berr\.message\b', l)]))
    def region(src):
        i = src.find('if (response.ok) {'); j = src.find('} catch (err: any) {', i)
        return src[i:j] if i >= 0 and j > i else ''
    t.check('B3', bool(region(cb)) and region(cb) == region(ch), 'the fetch / non-ok region (it passes the upstream status and error through) is byte-identical base/head: %s (%d chars)' % (region(cb) == region(ch), len(region(ch))))
    i = ch.find('Audit export could not reach the security service'); j = ch.find('res.status(502)', i)
    t.check('B4', 0 <= i < j and ch.count('res.status(502)') == 1, 'logger.error (offset %d) PRECEDES res.status(502) (offset %d) inside the catch; res.status(502) occurs %d time(s)' % (i, j, ch.count('res.status(502)')))
    tf = P['test_file']; ts = show(repo, head, tf)
    its = re.findall(r"\bit(?:\.each\([^)]*\))?\(\s*'((?:[^'\\]|\\.)*)'", ts)
    each3 = len(re.findall(r"it\.each\(\['production', 'development', 'test'\]\)", ts))
    t.check('B5', len(its) == 7 and each3 == 1 and 'thrown Object with fields [password, host]' in ts and 'RED KS-1410 X4' in ts and len(its) - each3 + 3 * each3 == P['claims']['cells'],
            'test file %s: %d definitions (X1 is it.each x3) = %d cells (the seat claims %d); X4 names `thrown Object with fields [password, host]` (asserted IN THIS FILE): %s' % (
                tf.split('/')[-1], len(its), len(its) - each3 + 3 * each3, P['claims']['cells'], 'thrown Object with fields [password, host]' in ts))
    f500 = fail500_of(ch)
    t.check('B6', bool(f500) and PRE_RULING in f500, 'THIS head\'s own fail500 (audit-export.ts, :%d) is still the PRE-ruling `String(err)` line: %s | #1443\'s head changes exactly that line (the cross-PR fact the composition proof covers)' % (
        (ch[:ch.find('function fail500')].count('\n') + 1) if f500 else -1, bool(f500 and PRE_RULING in f500)))
    docs(repo, head, base, t, P)
    return t.end()


def sites_message(src):
    return [(i + 1, norm(l)) for i, l in enumerate(code_only(src).split('\n')) if re.search(r'\.message\b', l)]


def run1445(repo, head, base):
    t = Tally(); P = PR(1445); f = P['route_files'][0]
    b, h = show(repo, base, f), show(repo, head, f)
    if not b or not h: print('REFUSED: delegations.ts absent at base or head'); return 2
    cb, ch = code_only(b), code_only(h)
    add, rem = added_removed(cb, ch)
    want_add = ["import { logger } from '../utils/logger';", "logger.error('Process expired delegations failed (POST /api/delegations/admin/process-expired)', { error: error.message });",
                "return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });"]
    want_rem = ["return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: error.message } });"]
    raw_a, raw_r = added_removed(b, h)
    t.check('T0', sorted(add) == sorted(want_add) and sorted(rem) == sorted(want_rem),
            'CODE-ONLY multiset in delegations.ts base %s -> head %s: added %d removed %d | RAW added %d removed %d (numstat %s) | removed %s' % (
                blob(repo, base, f)[-12:], blob(repo, head, f)[-12:], len(add), len(rem), len(raw_a), len(raw_r), P['numstat'][f], rem))
    sb, sh_ = sites_message(b), sites_message(h)
    tb = [x[1] for x in sb]; th = [x[1] for x in sh_]
    gone = [x for x in tb if x not in th]; new = [x for x in th if x not in tb]
    t.info('T1', 'Q-4XX: `.message` sites BASE (line, text): %s' % sb)
    t.info('T1', 'Q-4XX: `.message` sites HEAD (line, text): %s' % sh_)
    t.check('T1', len(sb) == 7 and len(sh_) == 7 and len(gone) == 1 and len(new) == 1 and 'error.message' in gone[0] and 'logger.error' in new[0] and [x for x in tb if x not in gone] == [x for x in th if x not in new],
            'Q-4XX: %d `.message` sites at base, %d at head; exactly ONE site left (%s) and ONE logger site came in; the OTHER %d are byte-identical (the READY names the four 4xx response sites at base lines %s; measured base lines of the `message: error.message` response sites: %s; the other two are the `error.message ===` / `.startsWith` CONDITIONS at %s) — whether they belong in KS-1410 is a QUESTION for Wednesday/Kam, not a finding' % (
                len(sb), len(sh_), gone[0][:60] if gone else None, len(tb) - len(gone), P['claims']['sites_4xx_base'], [n for n, x in sb if 'message: error.message' in x and "status(5" not in x], [n for n, x in sb if 'message: error.message' not in x]))
    cat = ch[ch.find("router.post('/admin/process-expired'"):]
    cat = cat[:cat.find('\n});') + 4]
    struct = re.search(r"\} catch \(error\) \{\s*if \(error instanceof Error\) \{(.*?)\n    \}\s*next\(error\);\s*\}", cat, re.S)
    t.check('T2', bool(struct) and 'logger.error' in struct.group(1) and 'return res.status(500)' in struct.group(1) and cat.count('next(error)') == 1,
            'the catch is `if (error instanceof Error) { logger.error; return 500 }` then `next(error)` x%d: a thrown NON-Error skips the log line and the constant 500 and falls through to next(error) — NO new cell drives that path (the seat says so)' % cat.count('next(error)'))
    t.check('T3', bool(blob(repo, base, 'Blockchain/Dev/services/transfer/src/utils/logger.ts')) and "from '../utils/logger'" in h, 'the logger module exists at BASE (%s) and the head imports it from ../utils/logger' % blob(repo, base, 'Blockchain/Dev/services/transfer/src/utils/logger.ts')[-12:])
    tf = P['test_file']; ts = show(repo, head, tf)
    its = re.findall(r"\bit(?:\.each\([^)]*\))?\(\s*'((?:[^'\\]|\\.)*)'", ts)
    t.check('T4', len(its) == 4 and len(its) - 1 + 3 == P['claims']['cells'], 'test file %s: %d definitions (T1 is it.each x3) = %d cells (the seat claims %d); titles %s' % (tf.split('/')[-1], len(its), len(its) - 1 + 3, P['claims']['cells'], [x[:30] for x in its]))
    docs(repo, head, base, t, P)
    return t.end()


def cell_counts(sh):
    return dict(expect=len(re.findall(r'^expect "', sh, re.M)), row_case=len(re.findall(r'^row_case ', sh, re.M)), nonjs_case=len(re.findall(r'^nonjs_case ', sh, re.M)))


def run1444(repo, head, base):
    t = Tally(); P = PR(1444); g = P['gate_script']; s = P['suite']
    b, h = show(repo, base, g), show(repo, head, g)
    if not b or not h: print('REFUSED: the guard is absent at base or head'); return 2
    cb, ch = sh_code_only(b), sh_code_only(h)
    add, rem = added_removed(cb, ch); raw_a, raw_r = added_removed(b, h)
    t.check('R0', len(add) == 2 and len(rem) == 2 and len(raw_a) == 10 and len(raw_r) == 2,
            'CODE-ONLY (full-line # comments blanked) added %d removed %d | RAW added %d removed %d (numstat %s: the other 8 added lines are comments) | added %s' % (len(add), len(rem), len(raw_a), len(raw_r), P['numstat'][g], [x[:70] for x in add]))
    old_rx = r'(\/[^ \t]*\/)?node_modules'; new_rx = r'([^ \t]*\/)?node_modules'
    rl_b = [x for x in rem if 'relink[stage] = ord' in x]; rl_h = [x for x in add if 'relink[stage] = ord' in x]
    t.check('R1', len(rl_b) == 1 and len(rl_h) == 1 and old_rx in rl_b[0] and new_rx in rl_h[0] and rl_b[0].replace(old_rx, new_rx) == rl_h[0],
            'the relink regex line differs by EXACTLY the prefix group %s -> %s (the rest of the line is byte-identical): %s' % (old_rx, new_rx, bool(rl_b and rl_h and rl_b[0].replace(old_rx, new_rx) == rl_h[0])))
    guard = 'if (u !~ /^:/) sub(/:.*$/, "", u)'
    us_h = [x for x in add if 'sub(/^USER' in x]
    t.check('R2', len(us_h) == 1 and us_h[0].count(guard) == 1 and ch.count(guard) == 1 and cb.count(guard) == 0,
            'the USER line carries the ruled deviation guard `%s` exactly once (file-wide code-only count head %d, base %d): %s' % (guard, ch.count(guard), cb.count(guard), us_h))
    def fn(src):
        m = re.search(r'function effective_user_is_unprivileged\(.*?\n    \}', src, re.S); return m.group(0) if m else None
    fh_, fb_ = fn(ch), fn(cb)
    t.check('R3', bool(fh_) and fh_ == fb_, 'effective_user_is_unprivileged() is byte-identical base/head: %s; its first lines: %s' % (bool(fh_ and fh_ == fb_), [norm(x)[:90] for x in (fh_ or '').split('\n')[:6]]))
    sb, sh_ = show(repo, base, s), show(repo, head, s)
    ok, info = pure_insertion(sb, sh_)
    new_titles = re.findall(r'^expect "(F-[CE][^"]*)"', sh_, re.M); old_titles = set(re.findall(r'^expect "(F-[CE][^"]*)"', sb, re.M))
    added_t = [x for x in new_titles if x not in old_titles]
    cb_, ch_ = cell_counts(sb), cell_counts(sh_)
    t.check('R4', ok and len(added_t) == 6 and any('pin' in x for x in added_t),
            'suite diff: %s | NEW cells %d: %s | declared-cell census base %s (sum %d; the PR body says expect 28 + row_case 31 + nonjs_case 7 = 66) -> head %s (sum %d)' % (
                info, len(added_t), [x[:48] for x in added_t], cb_, sum(cb_.values()), ch_, sum(ch_.values())))
    t.check('R5', blob(repo, base, g).startswith('100755') and blob(repo, head, g).startswith('100755') and blob(repo, base, s).startswith('100755') and blob(repo, head, s).startswith('100755'), 'both files are 100755 at base AND head (script %s, suite %s)' % (blob(repo, head, g)[:6], blob(repo, head, s)[:6]))
    docs(repo, head, base, t, P)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    a = 'x = 1;\n// c.catch(() => [])\nq`s`;\n'
    rep(code_only(a).count('catch') == 0, 'code_only: a comment mention is blanked')
    t_re = 'x = `"${s.replace(/"/g, \'""\')}"`;\n// k `y` thrown text\nz = a / b; // tail\n'
    rep('thrown text' not in code_only(t_re) and 'tail' not in code_only(t_re) and '/"/g' in code_only(t_re), 'code_only [g81]: a REGEX LITERAL holding a quote inside a template expression (audit-export.ts line 60) no longer opens a phantom string; later comments are still blanked and the division is kept')
    ad, rm = added_removed('a\nb\nc', 'a\nB\nc\nd'); rep(ad == ['B', 'd'] and rm == ['b'], 'added_removed: replace + insert')
    ok, _ = pure_insertion('a\nb\n', 'a\nNEW\nb\n'); rep(ok, 'pure_insertion: one inserted line passes')
    ok, _ = pure_insertion('a\nb\n', 'a\nNEW\nB\n'); rep(not ok, 'PLANTED altered base line FAILS pure_insertion')
    ok, _ = pure_insertion('a\nb\n', 'a\nN1\nb\nN2\n'); rep(not ok, 'PLANTED two separate insertions FAIL (one contiguous block only)')
    ok, _ = pure_insertion('a\nb\n', 'a\nb\n'); rep(not ok, 'PLANTED no change FAILS (nothing inserted)')
    line = "logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });"
    e = expr_of(line); rep(e is not None and e.startswith('err instanceof Error') and e.endswith("typeof err"), 'expr_of extracts the ruled expression (%d bytes)' % len((e or '').encode()))
    rep(expr_of("logger.error(context, { error: %s });" % PRE_RULING) is None, 'CONTROL: the pre-ruling line yields NO ruled expression')
    rep(expr_of(line + '\n' + line) is None, 'ARM: two logger lines carrying the expression read as ambiguous (None), never a pass')
    rep(expr_of('// ' + line) is None, 'ARM: the expression in a COMMENT is blanked (code-only) and reads None')
    tab = eval_table(e)
    rep(tab['plain object {password, host}'][0] == 'thrown Object with fields [password, host]' and tab['plain object {password, host}'][1] == '[object Object]', 'eval_table: a plain object -> type + field names, String(err) -> [object Object]')
    rep(tab['string "postgres://svc:SECRET@host/db"'][0] == 'postgres://svc:SECRET@host/db', 'eval_table: a thrown string is returned VERBATIM (the stated gap)')
    rep(tab['Error("boom SECRET-in-message")'][0].startswith('boom') and tab['null'][0] == 'thrown object' or tab['null'][0] == 'thrown object', 'eval_table: Error -> message; null -> "thrown object" path read')
    rep(tab['class instance DbFault'][0] == 'thrown DbFault with fields [code, dsn]' and tab['null-prototype object'][0] == 'thrown object with fields [password]', 'eval_table: class name / null-prototype name read')
    rep(tab['object whose ownKeys trap throws'][0].startswith('THROWS'), 'eval_table: a throwing ownKeys trap is REPORTED as THROWS (a fact about the expression, not hidden)')
    f = "function fail500(res: Response, context: string, err: unknown): void {\n  logger.error(context, { error: x });\n  res.status(500).json({ a });\n}\nz"
    rep(fail500_of(f).endswith('}') and 'res.status(500)' in fail500_of(f), 'fail500_of extracts the function')
    rep(cell_counts('expect "a" 0 x\nrow_case a\nrow_case b\nnonjs_case c\n') == dict(expect=1, row_case=2, nonjs_case=1), 'cell_counts reads the three declared-cell helpers')
    rep(sites_message("a\n  return x(error.message);\n// error.message\n") == [(2, 'return x(error.message);')], 'sites_message blanks comments and numbers lines')
    rep(sh_code_only('a\n  # x\nb').split('\n') == ['a', '', 'b'], 'sh_code_only blanks full-line comments only')
    try: req(['--repo', 'x', '--head', 'abc'], '--head', hex40=True); rep(False, 'short head ACCEPTED')
    except SystemExit: rep(True, 'REQUIRED-ARG ARM short --head -> refused')
    try: PR(1441); rep(False, '--pr 1441 ACCEPTED')
    except SystemExit: rep(True, 'WRONG-PR ARM --pr 1441 (gate80\'s PR) -> refused')
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
    try:
        return {'1443': run1443, '1444': run1444, '1445': run1445, '1446': run1446}[n](repo, head, base)
    except SystemExit as e:   # a wrong head / foreign PR's tree makes a helper refuse: that is a FAIL of the claims, not a crash
        print('FAIL C2-REFUSED %s' % e); return 1


if __name__ == '__main__':
    sys.exit(main())
