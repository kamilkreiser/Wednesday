#!/usr/bin/env python3
"""c2_code_gate85.py — CHECK 1 (the code claims, READ against the diff) for gate85: ONE PR, #1453 (KS-1432). Read verbs on the repo; the only other things it runs are `node` on a
few lines of INLINE source (no npm, no npx, no node_modules) and `git apply` on files in a scratch dir OUTSIDE every repo (named exception X1).

  claims    --repo R --pr 1453 --head H --base B        F0..F10 (below). Every figure is the DRAFTER'S PREDICTION; the gate re-measures on its own tree.
  --selftest

  F0  raw added/removed lines per path (numstat) AND non-blank counts beside them (the builder's "+10/-1" and "11/1" differ by one blank/comment line)
  F1  line-level shape (difflib opcodes, whitespace-exact): the product diff = ONE pure insert (the exported function + its doc block) + ONE replace (1 line -> 2: a KS-1432 comment line and
      the call); the test diff = an import insert + a block replace; EVERY other line byte-identical
  F2  THE EQUIVALENCE CLAIM, on gate-owned instruments: the OLD inline condition read as TEXT from the base blob (exactly 1 match), the NEW predicate and call site read as TEXT from the head blob
      (exactly 1 match each); evaluated (a) in `node` over a gate-owned value list (the builder's 16 + more) and (b) by an independent pure-Python model of the three-term grammar over the same values,
      and (c) EXHAUSTIVELY over the 6 value classes `JSON.parse` can return (null / boolean / number / string / array / object): the predicate depends only on that class. MUTANT CONTROLS must disagree.
  F3  authentication-pattern census over the changed lines of the product file AND the route's registration line (`router.post('/api/documents', authenticateToken(true), ...)`) read at base and head
      (must be byte-identical); a planted `req.user.role` line must fire the pattern
  F4  reference census of `isAcceptableDocumentBody` / `isAcceptableBody` in api-gateway/src at base and head: CODE-ONLY (comments blanked, strings kept) BESIDE the raw count
  F5  the key `KS-1432` on added lines: product and test, per added line (the builder's "1 of 10 before the comment line"; "preceded by a KS-1432 line, 1 of 1")
  F6  the test file: cells (`it(`) 8 at base, 10 at head; the 8 pre-existing cells' text byte-identical; the two new cells' ids (`RED KS-1432 R1`, `control KS-1432 C1`)
  F7  PAYLOAD: the Spark sections applied (git apply, scratch dir outside every repo) onto the BASE blobs: product-only blob == d7e9c8c8696d, test blob == the head's 661e3e5c6fa4; removing the
      one KS-1432 comment line from the head product returns d7e9c8c8696d; control: a 1-byte-altered patch is refused / gives another blob
  F8  CI reach: workflow files at head that run an api-gateway unit suite (vitest / `npm run test`) and whether they trigger on pull_request (ci.yml is workflow_dispatch only)
  F9  CLASS SIBLINGS (report only, Q-CLASS): other test files at head that define their own copy of a route predicate ("Mirrors the ..." comments, local re-implementations)
  F10 test comment claims (the Spark comment "uses [the predicate] at the POST /api/documents call site"): quoted verbatim, with the call-site test's location, for the gate to rule UNVERIFIED / FALSE
rc 0 all pass / 1 a FAIL / 2 refused."""
import difflib, hashlib, json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate85 import K, PR, Tally, git, show, blob, req, resolvable, blob_of_bytes, must_be_outside, run as lrun

OLD_COND = "parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)"
RAWS = ['null', '[]', '[1]', '[[]]', '42', '0', '-0', '1e999', '"str"', '""', 'true', 'false', '{}', '{"a":1}', '{"title":"x","documentType":"CERTIFICATE"}', '{"__proto__":null}']   # the builder's 16
RAWS_GATE = RAWS + ['1', '-1', '1.5', '"null"', '"{}"', '"[]"', '[null]', '[{}]', '[[],[]]', '{"a":null}', '{"a":[]}', '{"a":{"b":{}}}', '{"constructor":1}', '{"length":0}', '{"0":1}', '"\\u0000"', '{"a":"\\u0000"}',
                    '123456789012345678901234567890', '[true,false,null,1,"a",{}]', '"  "']
AUTH_RX = re.compile(r'(req\.user|\.role\b|authenticateToken|requireRole|ADMIN_ROLES|isAdmin|verificationLevel|meetsVerificationLevel|\bjwt\b|\btoken\b|authorization|authorize|permission|tenantId|organizationId)', re.I)


def code_only(text):
    """comments blanked, strings kept (a small scanner for TS/JS: //, /* */, ', ", `)."""
    out, i, n, st = [], 0, len(text), None
    while i < n:
        c = text[i]; d = text[i + 1] if i + 1 < n else ''
        if st is None:
            if c == '/' and d == '/':
                while i < n and text[i] != '\n': i += 1
                continue
            if c == '/' and d == '*':
                i += 2
                while i < n - 1 and not (text[i] == '*' and text[i + 1] == '/'):
                    out.append('\n' if text[i] == '\n' else ' '); i += 1
                i += 2; continue
            if c in '\'"`': st = c
            out.append(c); i += 1
        else:
            out.append(c)
            if c == '\\' and i + 1 < n: out.append(text[i + 1]); i += 2; continue
            if c == st: st = None
            i += 1
    return ''.join(out)


def opcodes(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']


def node_eval(old_cond, new_ret, raws):
    """-> list of (raw, old_refuses, new_accepts, mutant_array_dropped_refuses) from `node` evaluating the three TEXTS (no npm). rc != 0 raises."""
    js = ("const raws=JSON.parse(process.argv[1]);const oldF=new Function('parsed','return ('+process.argv[2]+');');"
          "const newF=new Function('parsed','return '+process.argv[3]+';');const mut=new Function('parsed',\"return (parsed === null || typeof parsed !== 'object');\");"
          "console.log(JSON.stringify(raws.map(r=>{const v=JSON.parse(r);return [r,!!oldF(v),!!newF(v),!!mut(v)];})));")
    p = subprocess.run(['node', '-e', js, json.dumps(raws), old_cond, new_ret], capture_output=True, text=True)
    if p.returncode != 0: raise SystemExit('c2: node rc %d: %s' % (p.returncode, p.stderr[:300]))
    return json.loads(p.stdout)


def py_model(term_src, value):
    """independent model of the grammar `A || B || C` with A='parsed === null', B="typeof parsed !== 'object'", C='Array.isArray(parsed)', JS semantics over a Python-decoded JSON value."""
    def term(t):
        t = t.strip()
        if t == 'parsed === null': return value is None
        if t == "typeof parsed !== 'object'": return not (value is None or isinstance(value, (dict, list)))      # typeof null === 'object', arrays and objects are 'object'
        if t == 'Array.isArray(parsed)': return isinstance(value, list)
        raise SystemExit('c2: py_model cannot model the term %r (the grammar changed)' % t)
    return any([term(t) for t in term_src.split('||')])     # a LIST: every term is parsed even when an earlier one is already true (an unknown term is never skipped)


def value_class(v):
    return 'null' if v is None else 'boolean' if isinstance(v, bool) else 'number' if isinstance(v, (int, float)) else 'string' if isinstance(v, str) else 'array' if isinstance(v, list) else 'object'


def f1_shape(base_txt, head_txt):
    a, b = base_txt.split('\n'), head_txt.split('\n')
    return opcodes(a, b), a, b


def census_refs(txt, names):
    co = code_only(txt)
    return dict((n, (txt.count(n), co.count(n))) for n in names)


def apply_sections(base_blobs, sections):
    """git apply -p1 each section onto a scratch dir OUTSIDE every repo. -> {path: bytes} or raises."""
    d = tempfile.mkdtemp(prefix='c2_payload_', dir=os.environ.get('TMPDIR') or '/private/tmp/claude-501')
    must_be_outside(d, 'payload scratch')
    for pth, b in base_blobs.items():
        fp = os.path.join(d, pth); os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, 'wb').write(b)
    res = []
    for sec in sections:
        p = subprocess.run(['git', 'apply', '-p1', '--whitespace=nowarn', sec], cwd=d, capture_output=True, text=True); res.append((p.returncode, p.stderr.strip()[:200]))
    out = dict((pth, open(os.path.join(d, pth), 'rb').read()) for pth in base_blobs)
    return out, res, d


def claims(repo, P, head, base):
    t = Tally(); prod, test = P['product'], P['test_file']
    bp, hp, bt, ht = show(repo, base, prod), show(repo, head, prod), show(repo, base, test), show(repo, head, test)
    # F0
    ns = {}
    for l in git(repo, 'diff', '--numstat', base, head).strip().split('\n'):
        if not l: continue
        a, d, p = l.split('\t'); ns[p] = (int(a), int(d))
    raw = {}
    for p in (prod, test):
        diff = git(repo, 'diff', '-U0', base, head, '--', p).split('\n')
        add = [l[1:] for l in diff if l.startswith('+') and not l.startswith('+++')]; rem = [l[1:] for l in diff if l.startswith('-') and not l.startswith('---')]
        raw[p] = (add, rem)
    t.check('F0', all(ns[p] == (len(raw[p][0]), len(raw[p][1])) for p in raw) and ns[prod] == (11, 1) and ns[test] == (19, 3),
            'numstat product %s test %s | raw +/- product %d/%d (non-blank %d/%d) test %d/%d (non-blank %d/%d) | the builder says product +10/-1 and test +19/-3 "once the one blank line git cancels is removed", and the Spark patch +11/-2 and +20/-4' % (
                ns[prod], ns[test], len(raw[prod][0]), len(raw[prod][1]), sum(1 for x in raw[prod][0] if x.strip()), sum(1 for x in raw[prod][1] if x.strip()),
                len(raw[test][0]), len(raw[test][1]), sum(1 for x in raw[test][0] if x.strip()), sum(1 for x in raw[test][1] if x.strip())))
    # F1
    ops_p, a, b = f1_shape(bp, hp)
    desc_p = ['%s base[%d:%d] -> head[%d:%d] (%d -> %d lines)' % (tg, i1 + 1, i2, j1 + 1, j2, i2 - i1, j2 - j1) for tg, i1, i2, j1, j2 in ops_p]
    shape_ok = len(ops_p) == 2 and ops_p[0][0] == 'insert' and ops_p[1][0] == 'replace' and (ops_p[1][2] - ops_p[1][1], ops_p[1][4] - ops_p[1][3]) == (1, 2)
    t.check('F1a', shape_ok, 'product: %d change block(s): %s (want: ONE pure insert, then ONE replace of 1 line by 2); every other line of %d base lines byte-identical' % (len(ops_p), desc_p, len(a)))
    if shape_ok:
        ins = b[ops_p[0][3]:ops_p[0][4]]; rep_old = a[ops_p[1][1]:ops_p[1][2]]; rep_new = b[ops_p[1][3]:ops_p[1][4]]
        print('  INSERT (head lines %d-%d):' % (ops_p[0][3] + 1, ops_p[0][4])); [print('    | ' + x) for x in ins]
        print('  REPLACED line: %r' % rep_old[0]); print('  BY:'); [print('    | ' + x) for x in rep_new]
        t.check('F1b', rep_old[0].strip() == "if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {" and rep_new[0].strip().startswith('// KS-1432:') and rep_new[1].strip() == 'if (!isAcceptableDocumentBody(parsed)) {'
                and sum(1 for x in ins if x.startswith('export function isAcceptableDocumentBody(parsed: unknown): boolean {')) == 1 and ins[ins.index('export function isAcceptableDocumentBody(parsed: unknown): boolean {') + 1].strip() == "return !(parsed === null || typeof parsed !== 'object' || Array.isArray(parsed));",
                'the replaced line is the old inline condition; the new two lines are a KS-1432 comment and `if (!isAcceptableDocumentBody(parsed)) {`; the insert holds the function whose return is the negation of the old condition (TEXT)')
    ops_t, ta, tb = f1_shape(bt, ht)
    desc_t = ['%s base[%d:%d] -> head[%d:%d] (%d -> %d lines)' % (tg, i1 + 1, i2, j1 + 1, j2, i2 - i1, j2 - j1) for tg, i1, i2, j1, j2 in ops_t]
    removed_t = [x for tg, i1, i2, j1, j2 in ops_t for x in ta[i1:i2]]
    t.check('F1c', len(ops_t) == 2 and [o[0] for o in ops_t] == ['insert', 'replace'] and any('function isAcceptableBody(parsed: unknown): boolean {' in x for x in removed_t),
            'test: %d change block(s): %s | the removed lines are the private copy `function isAcceptableBody(parsed: unknown): boolean {...}` (%d removed lines)' % (len(ops_t), desc_t, len(removed_t)))
    # F2
    m_old = re.findall(r"if \((%s)\) \{" % re.escape(OLD_COND), bp); m_ret = re.findall(r"export function isAcceptableDocumentBody\(parsed: unknown\): boolean \{\n\s+return (.+);\n\}", hp)
    m_call = re.findall(r"if \((![A-Za-z]+\(parsed\))\) \{\n\s+res\.status\(400\)", hp); m_old_head = re.findall(r"if \((%s)\) \{" % re.escape(OLD_COND), hp)
    t.check('F2a', len(m_old) == 1 and len(m_ret) == 1 and len(m_call) == 1 and not m_old_head,
            'TEXT anchors: old inline condition x%d in the BASE product (want 1) and x%d in the HEAD product (want 0) | new predicate return x%d | new call site x%d (%s)' % (len(m_old), len(m_old_head), len(m_ret), len(m_call), m_call[:1]))
    if len(m_old) == 1 and len(m_ret) == 1:
        old_cond, new_ret = m_old[0], m_ret[0]
        print('  OLD (refuses when true): %s\n  NEW predicate return (accepts when true): %s' % (old_cond, new_ret))
        rows = node_eval(old_cond, new_ret, RAWS_GATE)
        dis = [r for r, o, n, m in rows if o == n]            # old refuses == new accepts means DISAGREE (new should accept exactly when old does not refuse)
        refused = sum(1 for r, o, n, m in rows if o); mut_dis = [r for r, o, n, m in rows if o != m]
        b16 = [x for x in rows if x[0] in RAWS]; dis16 = [x[0] for x in b16 if x[1] == x[2]]; ref16 = sum(1 for x in b16 if x[1])
        t.check('F2b', not dis and not dis16 and len(rows) == len(RAWS_GATE) and refused > 0 and (len(rows) - refused) > 0,
                'node evaluation of the TEXTS: the builder\'s %d values: %d refused / %d accepted, %d disagreements | the gate list of %d values: %d refused / %d accepted, %d disagreements %s' % (
                    len(b16), ref16, len(b16) - ref16, len(dis16), len(rows), refused, len(rows) - refused, len(dis), dis[:3] or ''))
        t.check('F2c-CONTROL', len(mut_dis) >= 3, 'MUTANT CONTROL (array check dropped) disagrees with the old condition on %d of the gate\'s %d values (%s) -> the comparison can fail' % (len(mut_dis), len(rows), mut_dis[:5]))
        # independent model: new accepts == not (the same three-term refusal), so compare old_cond's model with the negation of the predicate body's model
        inner = new_ret.strip(); inner = inner[2:-1] if inner.startswith('!(') and inner.endswith(')') else None
        if inner is None:
            t.check('F2d', False, 'the predicate return is no longer `!( ... )` over the same three terms: the python model cannot compare (%r)' % new_ret)
        else:
            pydis = [r for r in RAWS_GATE if py_model(old_cond, json.loads(r)) != py_model(inner, json.loads(r))]
            t.check('F2d', not pydis and inner == old_cond, 'independent pure-Python model of the three-term grammar over the same %d values: %d disagreements | the predicate body is the old condition character for character: %s' % (len(RAWS_GATE), len(pydis), inner == old_cond))
        # exhaustive over the classes JSON.parse can return
        classes = {}
        for r in RAWS_GATE:
            v = json.loads(r); classes.setdefault(value_class(v), []).append(py_model(old_cond, v))
        consistent = all(len(set(x)) == 1 for x in classes.values()) and set(classes) == {'null', 'boolean', 'number', 'string', 'array', 'object'}
        t.check('F2e', consistent, 'EXHAUSTIVE over the 6 classes JSON.parse can return: every value of a class gets ONE decision (%s) and all 6 classes are covered by the gate list -> the decision is a function of the class alone, so the list covers the input space of JSON.parse (text evaluation; NOT the TypeScript compiler)' % (dict((c, ('refuse' if x[0] else 'accept', len(x))) for c, x in sorted(classes.items())),))
        mutants = {'M-null': "parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)".replace('parsed === null || ', ''), 'M-typeof': OLD_COND.replace("!== 'object'", "=== 'object'"), 'M-array': OLD_COND.replace(' || Array.isArray(parsed)', '')}
        fired = dict((k, [r for r in RAWS_GATE if py_model_safe(v, json.loads(r)) != py_model(old_cond, json.loads(r))][:3]) for k, v in mutants.items())
        t.check('F2f-CONTROL', all(fired.values()), 'MUTANT CONTROLS on the python model (null check dropped / typeof flipped / array check dropped) each disagree somewhere: %s' % fired)
    # F3
    changed = raw[prod][0] + raw[prod][1]
    hits = [x for x in changed if AUTH_RX.search(x)]
    reg_b = [l for l in bp.split('\n') if re.search(r"router\.post\('/api/documents',", l)]; reg_h = [l for l in hp.split('\n') if re.search(r"router\.post\('/api/documents',", l)]
    ctl = AUTH_RX.search('const role = req.user.role;')
    t.check('F3', not hits and reg_b == reg_h and len(reg_h) == 1 and 'authenticateToken(true)' in reg_h[0] and bool(ctl),
            'authentication pattern over the %d changed lines of %s (%d added + %d removed): %d match %s | the builder says "0 of 11" (its count predates the comment line: the final diff has %d changed lines) | planted `req.user.role` control fires: %s | route registration line at base == head: %s (%r)' % (
                len(changed), prod.split('/')[-1], len(raw[prod][0]), len(raw[prod][1]), len(hits), hits[:3] or '', len(changed), bool(ctl), reg_b == reg_h, (reg_h or ['ABSENT'])[0].strip()[:110]))
    # F4
    names = ['isAcceptableDocumentBody', 'isAcceptableBody']
    cb = census_refs(bp, names); ch = census_refs(hp, names); ctb = census_refs(bt, names); cth = census_refs(ht, names)
    t.check('F4', ch['isAcceptableDocumentBody'][1] == 2 and cb['isAcceptableDocumentBody'] == (0, 0) and cth['isAcceptableDocumentBody'][0] >= 1 and cth['isAcceptableBody'][1] >= 1,
            'raw/code-only counts: product base %s head %s | test base %s head %s | (code-only product head: the definition + the one call = 2; the TEST reaches the export through `verification.isAcceptableDocumentBody` read as a property, a string it may or may not resolve; and `isAcceptableBody` stays a local wrapper name in the test)' % (cb, ch, ctb, cth))
    allhead = git(repo, 'grep', '-n', '-F', 'isAcceptableDocumentBody', head, '--', P['service_dir']).strip().split('\n')
    t.info('F4b', 'every line in api-gateway at head naming isAcceptableDocumentBody (git grep, raw): %d line(s): %s' % (len([x for x in allhead if x]), [x.split(':', 2)[1] + ':' + x.split(':', 2)[2][:70].strip() for x in allhead if x][:8]))
    # F5
    key = P['cheat_key']
    pk = [l for l in raw[prod][0] if key in l]; tk = [l for l in raw[test][0] if key in l]
    prod_lines = hp.split('\n'); call_idx = next((i for i, l in enumerate(prod_lines) if 'if (!isAcceptableDocumentBody(parsed)) {' in l), -1)
    t.check('F5', len(pk) >= 2 and call_idx > 0 and key in prod_lines[call_idx - 1],
            'KS-1432 on added product lines: %d of %d added (%d non-blank) | on added test lines: %d of %d | the changed existing code line (head line %d) is preceded by: %r (carries the key: %s) | the builder says "1 of 10 before the comment line was added" and made no every-line claim' % (
                len(pk), len(raw[prod][0]), sum(1 for x in raw[prod][0] if x.strip()), len(tk), len(raw[test][0]), call_idx + 1, prod_lines[call_idx - 1].strip()[:90] if call_idx > 0 else None, call_idx > 0 and key in prod_lines[call_idx - 1]))
    # F6
    def cells(txt):
        """vitest cells by TEXT: each `it('title'` is one; each `it.each([ rows ])(` is as many as its rows (rows = lines that open with `[` inside the array literal)."""
        n = [m.group(1) for m in re.finditer(r"^\s*it\((?:'([^']+)'|\"([^\"]+)\"|`([^`]+)`)", txt, re.M)]
        titles = [m.group(1) or m.group(2) or m.group(3) for m in re.finditer(r"^\s*it\((?:'([^']+)'|\"([^\"]+)\"|`([^`]+)`)", txt, re.M)]
        for m in re.finditer(r"^\s*it\.each\(\[\n(.*?)\n\s*\]\)\('([^']+)'", txt, re.M | re.S):
            rows = re.findall(r"^\s*\[", m.group(1), re.M); titles += ['%s [row %d]' % (m.group(2), i + 1) for i in range(len(rows))]
        return titles
    cb_, ch_ = cells(bt), cells(ht)
    t.check('F6', len(cb_) == 8 and len(ch_) == 10 and all(c in ch_ for c in cb_) and any('RED KS-1432 R1' in c for c in ch_) and any('control KS-1432 C1' in c for c in ch_),
            'it( cells: base %d, head %d (want 8 -> 10) | the 8 pre-existing cell titles all present at head: %s | new cells: %s' % (len(cb_), len(ch_), all(c in ch_ for c in cb_), [c for c in ch_ if c not in cb_]))
    same_lines = sum(1 for x in ta if x in set(tb)); t.info('F6b', 'base test lines %d, of which present verbatim in the head file: %d (the removed private copy accounts for the rest)' % (len(ta), same_lines))
    # F7
    sp = K['spark']
    if os.path.isfile(sp['section_product']) and os.path.isfile(sp['section_test']):
        c1 = hashlib.sha256(open(sp['patch'], 'rb').read()).hexdigest()[:16]
        out, res, d = apply_sections({prod: bp.encode('utf-8'), test: bt.encode('utf-8')}, [sp['section_product'], sp['section_test']])
        pb, tb_ = blob_of_bytes(out[prod]), blob_of_bytes(out[test])
        why_line = next((l for l in hp.split('\n') if l.strip().startswith('// KS-1432: this is the exported')), None)
        without = '\n'.join(l for l in hp.split('\n') if l != why_line) if why_line else None
        rb = blob_of_bytes(without) if without is not None else ''
        t.check('F7a', all(r[0] == 0 for r in res) and pb.startswith(P['spark_product_only_blob']) and tb_.startswith(P['spark_test_blob']) and tb_ == P['blobs_full']['test_head'],
                'git apply -p1 of the Spark sections onto the BASE blobs in a scratch dir outside every repo (%s): rc %s | product blob %s (builder: %s) | test blob %s == the head test blob %s: %s | patch.diff sha256/16 %s (kit %s)' % (
                    d, [r[0] for r in res], pb[:12], P['spark_product_only_blob'], tb_[:12], P['blobs_full']['test_head'][:12], tb_ == P['blobs_full']['test_head'], c1, sp['patch_sha256_16']))
        t.check('F7b', rb.startswith(P['spark_product_only_blob']) and blob_of_bytes(hp.encode()) == P['blobs_full']['product_head'],
                'removing the ONE KS-1432 comment line from the HEAD product returns blob %s (want %s) | the head product blob %s (kit %s)' % (rb[:12], P['spark_product_only_blob'], blob_of_bytes(hp.encode())[:12], P['blobs_full']['product_head'][:12]))
        bad = open(sp['section_product'], 'rb').read().replace(b'return !(parsed', b'return !!(parsed', 1)
        fd, fn = tempfile.mkstemp(prefix='c2_badpatch_', dir=os.path.dirname(d)); os.write(fd, bad); os.close(fd)
        out2, res2, d2 = apply_sections({prod: bp.encode('utf-8'), test: bt.encode('utf-8')}, [fn])
        t.check('F7c-CONTROL', blob_of_bytes(out2[prod]) != P['spark_product_only_blob'] or res2[0][0] != 0, 'CONTROL (the product section with one byte altered) gives rc %d and blob %s != %s -> the payload comparison can fail' % (res2[0][0], blob_of_bytes(out2[prod])[:12], P['spark_product_only_blob']))
    else:
        t.check('F7a', False, 'the Spark section files are not readable here (%s): NOT RUN, never a pass' % sp['section_product'])
    # F8
    wfs = [l.split('\t')[1] for l in git(repo, 'ls-tree', head, '.github/workflows/').strip().split('\n') if l]
    runners = []
    for w in wfs:
        txt = show(repo, head, w)
        lines = [(i + 1, l.strip()) for i, l in enumerate(txt.split('\n')) if re.search(r'(vitest|npm (run )?test( |$)|--workspaces)', l) and not l.strip().startswith('#')]
        if lines:
            on = re.search(r'(?m)^on:\s*\n((?:\s+.*\n)+)', txt); onb = on.group(1) if on else ''
            runners.append((w.split('/')[-1], 'pull_request' in onb, 'workflow_dispatch' in onb and 'pull_request' not in onb, lines[:2]))
    pr_runners = [r for r in runners if r[1]]
    t.info('F8', 'CI reach: %d of %d workflow files mention vitest / npm test; those that trigger on pull_request: %s; workflow_dispatch only: %s. THE GATE rules from the file text and the Actions runs (gh actions) whether ANY pull_request run executes the api-gateway suite; READ ONLY, a trigger block read by regex (the drafter read ci.yml `on:` = workflow_dispatch only; pr-platform-suites.yml mentions vitest only in COMMENTS, and its `test:unit` step failed in the job named `Playwright suite` in the Actions log, so it is not the api-gateway suite)' % (len(runners), len(wfs), [(r[0], r[3][0]) for r in pr_runners], [r[0] for r in runners if r[2]]))
    # F9
    sib = []
    for l in git(repo, 'grep', '-n', '-i', '-E', r'(mirrors the guard|mirrors the|copy of the (route|guard)|replica of)', head, '--', P['service_dir'] + '/src/__tests__').strip().split('\n'):
        if l: sib.append(l.split(':', 1)[1][:150])
    t.info('F9', 'class-sibling candidates (report only, Q-CLASS: a test that defines its own copy of production logic): %d line(s): %s' % (len(sib), sib[:8]))
    # F10
    cm = [l.strip() for l in ht.split('\n') if 'call site' in l]
    t.check('F10', len(cm) == 1, 'the Spark comment naming the call site, verbatim at head (%d line): %s | any test cell at head that drives POST /api/documents with a non-object body: %d (grep for `/api/documents` in the guard test; the ks815 file is where the route is driven) -> the gate rules the comment UNVERIFIED / FALSE with the M2 mutation (c3)' % (len(cm), cm[:1], len(re.findall(r"/api/documents'", ht))))
    return t.end()


def py_model_safe(src, value):
    try: return py_model(src, value)
    except SystemExit:
        # the mutants use terms outside the base grammar: model them directly
        if src.strip() == "typeof parsed !== 'object' || Array.isArray(parsed)": return (not (value is None or isinstance(value, (dict, list)))) or isinstance(value, list)
        if src.strip() == "parsed === null || typeof parsed === 'object' || Array.isArray(parsed)": return value is None or isinstance(value, (dict, list)) or isinstance(value, list)
        raise


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    co = code_only("a // KS-1432 x\n/* isAcceptableBody */ b 'isAcceptableBody' // tail\n`isAcceptableBody` c\n")
    rep('isAcceptableBody' not in co.split('\n')[0] and co.count('isAcceptableBody') == 2 and 'KS-1432' not in co, 'code_only blanks line and block comments and keeps strings (2 string mentions kept, 1 comment mention blanked)')
    rep(code_only("x /* a\n b */ y").count('\n') == 1, 'code_only keeps line structure across a block comment')
    ops = opcodes(['a', 'b', 'c'], ['a', 'X', 'Y', 'c']); rep(ops == [('replace', 1, 2, 1, 3)], 'opcodes: one replace of 1 line by 2')
    rep(py_model(OLD_COND, None) and py_model(OLD_COND, 5) and py_model(OLD_COND, 'a') and py_model(OLD_COND, True) and py_model(OLD_COND, []) and py_model(OLD_COND, [1]) and not py_model(OLD_COND, {}) and not py_model(OLD_COND, {'a': 1}), 'py_model: null / number / string / boolean / arrays refused; objects accepted')
    try: py_model('parsed === null || foo', None); rep(False, 'py_model ACCEPTED an unknown term')
    except SystemExit: rep(True, 'py_model REFUSES a term outside the grammar (a changed condition cannot be silently modelled)')
    rows = node_eval(OLD_COND, "!(%s)" % OLD_COND, RAWS)
    rep(len(rows) == 16 and sum(1 for r in rows if r[1]) == 12 and all(r[1] != r[2] for r in rows) and sum(1 for r in rows if r[1] != r[3]) == 3, 'node_eval on the builder\'s 16: 12 refused / 4 accepted, old vs `!(old)` never agree-on-refuse (0 disagreements), the array-dropped mutant disagrees on 3')
    rows2 = node_eval(OLD_COND, "!(parsed === null || typeof parsed !== 'object')", RAWS)
    rep(sum(1 for r in rows2 if r[1] == r[2]) == 3, 'PLANTED new predicate with the array check dropped: node_eval reads 3 disagreements (the comparison can fail)')
    cl = {}
    for r in RAWS_GATE: cl.setdefault(value_class(json.loads(r)), 0); cl[value_class(json.loads(r))] += 1
    rep(set(cl) == {'null', 'boolean', 'number', 'string', 'array', 'object'}, 'the gate value list covers all 6 JSON.parse classes: %s' % cl)
    rep(len(RAWS) == 16 and len(set(RAWS_GATE)) == len(RAWS_GATE), 'the builder\'s list is 16 values; the gate list has %d distinct values' % len(RAWS_GATE))
    rep(AUTH_RX.search('const role = req.user.role;') and AUTH_RX.search('router.post(x, authenticateToken(true))') and not AUTH_RX.search("if (!isAcceptableDocumentBody(parsed)) {"), 'auth pattern: fires on req.user.role and authenticateToken, silent on the call-site line')
    rep(blob_of_bytes(b'hello\n') == 'ce013625030ba8dba906f756967f9e9ca394464a', 'blob_of_bytes("hello\\n") == git\'s known blob id')
    for foreign in (1450, 1451, 1452):
        try: PR(foreign); rep(False, '--pr %s ACCEPTED' % foreign)
        except SystemExit: rep(True, 'WRONG-PR ARM --pr %s -> refused' % foreign)
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A or A[0] != 'claims': print(__doc__); return 2
    try:
        repo = req(A, '--repo'); P = PR(req(A, '--pr')); head = req(A, '--head', True); base = req(A, '--base', True)
        for s_ in (head, base):
            if not resolvable(repo, s_): raise SystemExit('REFUSED: %s is not in %s' % (s_[:12], repo))
        if head == base: raise SystemExit('REFUSED: --head == --base (an empty diff measures nothing)')
    except SystemExit as e:
        print(e); return 2
    print('C2 #%s head %s base %s repo %s' % (P['pr'], head, base, repo))
    return claims(repo, P, head, base)


if __name__ == '__main__':
    sys.exit(main())
