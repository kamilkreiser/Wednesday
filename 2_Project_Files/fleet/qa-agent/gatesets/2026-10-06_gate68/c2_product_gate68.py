#!/usr/bin/env python3
"""c2_product_gate68.py — C2 THROUGH-CODE for #1393 ROUND 2 (KS-1278), gate68. READ verbs only. --head is a parameter (env G68_HEAD).

  W1 shape: 4a16..head numstat; routes/documents.ts byte-identical to round 1 (the opt-in call unchanged)
  W2 the GUARDED statement (the ternary's second template in updateDocument), read as TEXT at the head:
       branch in TS on `guardStatus === null`; key `WHERE id = COALESCE(` of TWO scalar subqueries, the external_id arm FIRST
       (`d.external_id = ${id}`) then the pkey arm (`d2.id = ${idAsUuid}::uuid`), EACH tenant-scoped and `LIMIT 1`; the outer UPDATE
       keeps `AND tenant_id = ${tenantId}::uuid`; the status guard `status IS DISTINCT FROM ${guardStatus}::text` INSIDE the statement
  W3 the cast guard: `const idAsUuid = isValidUuid(id) ? id : null;` once; `${id}::uuid` exactly ONCE in the file and inside getDocument
       (none inside updateDocument); `${idAsUuid}::uuid` exactly ONCE, inside the guarded template. MUST-HIT control: `${tenantId}::uuid`
  W4 N3 BYTE-IDENTITY: the UNGUARDED template at the head == round 1's (4a16) single template, byte for byte (sha256 printed); INFO the
       diff vs the branch base 32e0 (round 1 added the guard line to every caller's statement, bound NULL for them)
  W5 caller census of `updateDocument(` over Blockchain/Dev at the head: definition / comment / test / PRODUCTION, opted-in = carries
       `ifStatusIsNot`; claim 13 production, 1 opted in, 12 others. Controls: must-hit (the definition is found) + a nonsense token (0)
  W6 §5d / PLACEHOLDERS: the lines ADDED in 4a16..head to the two product files carry no unfilled ticket placeholder
       (KS-TICKET, KS-XXX, KS-???, TBD-ticket); INFO whether any added line names KS 1424 / KS 1419
  W7 R2 BY POSITION (READ heuristic; the gate's G7 tamper is the measurement): R2's bound-value assertion is NOT a bare membership
       test (`.includes('revoked')` over all bindings), because the guarded template binds `${updated.status}` (= 'revoked' on the
       revoke path) in its SET clause BEFORE the guard — membership is satisfied whatever the guard binds (G7 blind)
  W8 INFO the guarded template's bindings in order, with the 0-based positions of `${guardStatus}` (for a positional R2 to be read against)
--selftest: planted texts (cast guard removed, outer tenant scope removed, pkey arm first, unguarded template 1 byte off, placeholder,
            membership-only R2) must each FAIL their check; the real stand-in head must pass W2 W3 W4 W5.
Usage: c2_product_gate68.py [--repo R] [--head H] | --selftest [--repo R]          rc 0 PASS / 1 FAIL / 2 refused"""
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate68 import K, git, Tally, resolvable, show

GUARD_OPEN = "    const affected = guardStatus === null\n      ? await (db || prisma).$executeRaw`"
GUARD_ELSE = "      : await (db || prisma).$executeRaw`"
R1_OPEN = "    const affected = await (db || prisma).$executeRaw`"
B0_OPEN = "    await (db || prisma).$executeRaw`\n      UPDATE documents SET"   # the branch base 32e0 (develop): no `affected`
PLACEHOLDER = re.compile(r'\bKS-(TICKET|X{2,}|\?{2,}|TBD|NNN+)\b|\bTBD-ticket\b', re.I)
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()[:16]


def templates(src):
    """(unguarded, guarded) template texts at a round-2 head, or (single, None) at round 1."""
    if GUARD_OPEN in src:
        a0 = src.index(GUARD_OPEN) + len(GUARD_OPEN); a1 = src.index('`', a0)
        b0 = src.index(GUARD_ELSE, a1) + len(GUARD_ELSE); b1 = src.index('`', b0)
        return src[a0:a1], src[b0:b1]
    if R1_OPEN in src:
        a0 = src.index(R1_OPEN) + len(R1_OPEN); return src[a0:src.index('`', a0)], None
    if B0_OPEN in src:
        a0 = src.index(B0_OPEN) + len(B0_OPEN) - len('\n      UPDATE documents SET'); return src[a0:src.index('`', a0)], None
    return None, None


def fn_span(src, name):
    i = src.index('export async function %s(' % name)
    j = src.find('\nexport ', i + 10)
    return i, (j if j > 0 else len(src))


def w2(t, guarded):
    if guarded is None: return t.check('W2', False, 'no guarded template (ternary on guardStatus === null) found')
    g = guarded
    co = g.find('WHERE id = COALESCE(')
    ext = g.find('d.external_id = ${id}'); pk = g.find('d2.id = ${idAsUuid}::uuid')
    arms = re.findall(r'\(SELECT (\w+)\.id FROM documents \1\s+WHERE (.*?)LIMIT 1\)', g, re.S)
    arm_ok = len(arms) == 2 and all('%s.tenant_id = ${tenantId}::uuid' % a in body for a, body in arms)
    close = g.rfind(')', 0, g.find('AND tenant_id = ${tenantId}::uuid', co) if co >= 0 else 0)
    outer = co >= 0 and re.search(r'\)\s*\n\s*AND tenant_id = \$\{tenantId\}::uuid\s*\n\s*AND \(\$\{guardStatus\}::text IS NULL OR status IS DISTINCT FROM \$\{guardStatus\}::text\)\s*$', g) is not None
    ok = co >= 0 and 0 <= ext < pk and arm_ok and outer
    return t.check('W2', ok, 'COALESCE key %s | external_id arm before pkey arm %s (offsets %d < %d) | 2 scalar subqueries each tenant-scoped + LIMIT 1 %s | outer tenant scope + status guard inside, last %s' % (
        co >= 0, 0 <= ext < pk, ext, pk, arm_ok, outer))


def w3(t, src, guarded):
    decl = src.count('    const idAsUuid = isValidUuid(id) ? id : null;\n')
    idc = [m.start() for m in re.finditer(r'\$\{id\}::uuid', src)]
    gd0, gd1 = fn_span(src, 'getDocument'); ud0, ud1 = fn_span(src, 'updateDocument')
    in_get = [x for x in idc if gd0 <= x < gd1]; in_upd = [x for x in idc if ud0 <= x < ud1]
    iau = len(re.findall(r'\$\{idAsUuid\}::uuid', src)); iau_g = len(re.findall(r'\$\{idAsUuid\}::uuid', guarded or ''))
    ctl = len(re.findall(r'\$\{tenantId\}::uuid', src))
    line = lambda off: src.count('\n', 0, off) + 1
    return t.check('W3', decl == 1 and len(idc) == 1 and len(in_get) == 1 and not in_upd and iau == 1 and iau_g == 1 and ctl > 0,
                   'idAsUuid = isValidUuid(id) ? id : null ×%d | ${id}::uuid ×%d at :%s (in getDocument %d, in updateDocument %d) | ${idAsUuid}::uuid ×%d (in the guarded template %d) | MUST-HIT ${tenantId}::uuid ×%d' % (
                       decl, len(idc), [line(x) for x in idc], len(in_get), len(in_upd), iau, iau_g, ctl))


def w4(t, unguarded, r1_single, base_single):
    ok = unguarded is not None and unguarded == r1_single
    t.check('W4', ok, 'N3 BYTE-IDENTITY: unguarded template at head sha256/16 %s == round-1 4a16 template %s: %s (%s / %s bytes)' % (
        sha(unguarded or ''), sha(r1_single or ''), ok, len((unguarded or '').encode()), len((r1_single or '').encode())))
    if base_single is not None and unguarded is not None:
        import difflib
        d = [l for l in difflib.unified_diff(base_single.split('\n'), unguarded.split('\n'), lineterm='', n=0) if l[:1] in '+-' and not l.startswith(('+++', '---'))]
        t.info('W4-base', 'vs the branch base 32e0 (develop\'s statement): %d changed line(s): %s — round 1\'s guard, bound NULL for the 12 unguarded callers (a no-op predicate, NOT byte-identical to develop)' % (len(d), d))


def census(lines):
    """lines: `path:lineno:text` from git grep. -> dict of classes."""
    out = {'definition': [], 'comment': [], 'test': [], 'production': [], 'opted': []}
    for l in lines:
        p, n, txt = l.split(':', 2)
        s = txt.strip()
        if 'export async function updateDocument(' in s: out['definition'].append('%s:%s' % (p, n)); continue
        if s.startswith(('//', '*', '/*')): out['comment'].append('%s:%s' % (p, n)); continue
        if '__tests__' in p or '.test.' in p: out['test'].append('%s:%s' % (p, n)); continue
        out['production'].append('%s:%s' % (p, n))
        if 'ifStatusIsNot' in s: out['opted'].append('%s:%s' % (p, n))
    return out


def w5(t, repo, head):
    rc, o, e = git(repo, 'grep', '-n', '-F', 'updateDocument(', head, '--', 'Blockchain/Dev', check=False)
    lines = [l.split(':', 1)[1] for l in o.splitlines()]
    c = census(lines)
    rc2, o2, e2 = git(repo, 'grep', '-n', '-F', 'updateDocumentZZQX_nonsense(', head, '--', 'Blockchain/Dev', check=False)
    ok = len(c['production']) == 13 and len(c['opted']) == 1 and c['opted'][0].endswith('routes/documents.ts:2398') and len(c['definition']) == 1 and rc2 == 1 and not o2
    t.check('W5', ok, 'grep lines %d = production %d (opted in %s) + definition %d + comment %d + test %d | MUST-HIT definition found %s | NONSENSE token rc %d lines %d' % (
        len(lines), len(c['production']), c['opted'], len(c['definition']), len(c['comment']), len(c['test']), bool(c['definition']), rc2, len(o2.splitlines())))
    t.info('W5-list', 'production callers: %s' % c['production'])
    t.info('W5-claim', "READY: '24 grep lines = 13 + 1 definition + 1 comment + 9 test lines' — measured %d = %d + %d + %d + %d" % (
        len(lines), len(c['production']), len(c['definition']), len(c['comment']), len(c['test'])))


def added_lines(repo, a, b, path):
    d = git(repo, 'diff', '-U0', a, b, '--', path)
    return [l[1:] for l in d.split('\n') if l.startswith('+') and not l.startswith('+++')]


def w6(t, added):
    bad = [l.strip()[:110] for l in added if PLACEHOLDER.search(l)]
    t.check('W6', not bad, 'added product lines %d; unfilled ticket placeholders %s' % (len(added), bad or 'none'))
    t.info('W6-names', 'added product lines naming KS 1424: %d, KS 1419: %d' % (
        sum(1 for l in added if re.search(r'KS[ -]1424', l)), sum(1 for l in added if re.search(r'KS[ -]1419', l))))


def r2_body(test):
    m = re.search(r"it\('RED KS-1278 R2.*?\n  \}\);", test, re.S)
    return m.group(0) if m else ''


def w7(t, test, guarded):
    body = r2_body(test)
    vm = re.search(r'const (\w+) = call \? call\.slice\(1\)([^;]*);', body)
    var = vm.group(1) if vm else None
    rhs_pos = bool(vm) and bool(re.search(r'\.slice\(\s*-\d|\[\s*-?\d+\s*\]', vm.group(2)))
    member = bool(var) and bool(re.search(r'\b%s\.includes\(' % var, body))
    positional = rhs_pos or bool(var) and bool(re.search(r'\b%s\s*\[|\b%s\.(indexOf|findIndex|lastIndexOf|at)\(|\b%s\.slice\(\s*-?\d' % (var, var, var), body))
    set_first = guarded is not None and 0 <= guarded.find('${updated.status}') < guarded.find('${guardStatus}')
    ok = bool(body) and bool(var) and positional
    t.check('W7', ok, "R2 found %s | bindings variable %r | bare membership %s.includes(...) %s | positional access %s | guarded template binds ${updated.status} BEFORE the guard %s -> %s" % (
        bool(body), var, var, member, positional, set_first,
        'MEMBERSHIP is satisfied by the SET binding: G7 PREDICTED BLIND (READ; the gate measures it)' if member and set_first else ('positional (the gate still measures G7)' if positional else 'no bound-value assertion found')))


def w8(t, guarded):
    if guarded is None: return
    b = re.findall(r'\$\{([^}]+)\}', guarded)
    t.info('W8', 'guarded bindings in order (%d): %s | ${guardStatus} at 0-based %s' % (len(b), b, [i for i, x in enumerate(b) if x == 'guardStatus']))


def run(repo, head, t):
    for n, s in (('head', head), ('round-1 head', K['round1_head']), ('branch base', K['branch_base'])):
        if not resolvable(repo, s): print('C2 REFUSED: %s unresolvable: %s' % (n, s)); return 'UNRESOLVABLE'
    src = show(repo, head, K['repo_file'])
    ung, gua = templates(src)
    r1s, _ = templates(show(repo, K['round1_head'], K['repo_file'])); b0, _ = templates(show(repo, K['branch_base'], K['repo_file']))
    ns = git(repo, 'diff', '--numstat', K['round1_head'], head).splitlines()
    route_same = git(repo, 'rev-parse', '%s:%s' % (head, K['route_file'])).strip() == git(repo, 'rev-parse', '%s:%s' % (K['round1_head'], K['route_file'])).strip()
    t.check('W1', route_same and ns, '4a16..head numstat %s | routes/documents.ts == round 1 %s' % ([x.replace('\t', ' ')[:70] for x in ns], route_same))
    w2(t, gua); w3(t, src, gua); w4(t, ung, r1s, b0)
    w5(t, repo, head)
    added = added_lines(repo, K['round1_head'], head, K['repo_file']) + added_lines(repo, K['round1_head'], head, K['route_file'])
    w6(t, added)
    w7(t, show(repo, head, K['test']), gua); w8(t, gua)
    return 'DONE'


def selftest(repo):
    import io, contextlib
    res = []
    def rep(c, m): res.append(c); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def q(f, *a):
        t = Tally(); b = io.StringIO()
        with contextlib.redirect_stdout(b): f(t, *a)
        return t
    st = K['head_standin']
    src = show(repo, st, K['repo_file']); ung, gua = templates(src); r1s, _ = templates(show(repo, K['round1_head'], K['repo_file']))
    rep(not q(w2, gua).fails, 'POSITIVE W2 on the real stand-in head')
    rep(not q(w3, src, gua).fails, 'POSITIVE W3 on the real stand-in head')
    rep(not q(w4, ung, r1s, None).fails, 'POSITIVE W4 (N3 byte-identity) on the real stand-in head')
    rep(not q(lambda t: w5(t, repo, st)).fails, 'POSITIVE W5 census 13 / 1 on the real stand-in head')
    s2 = src.replace('    const idAsUuid = isValidUuid(id) ? id : null;\n', '    const idAsUuid = id;\n')
    rep('W3' in q(w3, s2, gua).fails, 'PLANTED cast guard removed -> W3 FAIL')
    g2 = gua.replace('        AND tenant_id = ${tenantId}::uuid\n        AND (${guardStatus}', '        AND (${guardStatus}')
    rep(g2 != gua and 'W2' in q(w2, g2).fails, 'PLANTED outer tenant scope removed -> W2 FAIL')
    a = re.search(r'\(SELECT d\.id.*?LIMIT 1\)', gua, re.S).group(0); b = re.search(r'\(SELECT d2\.id.*?LIMIT 1\)', gua, re.S).group(0)
    g3 = gua.replace(a, '@@A@@').replace(b, a).replace('@@A@@', b)
    rep(g3 != gua and 'W2' in q(w2, g3).fails, 'PLANTED pkey arm FIRST -> W2 FAIL')
    g4 = gua.replace('LIMIT 1)', 'LIMIT 2)', 1)
    rep('W2' in q(w2, g4).fails, 'PLANTED a subquery without LIMIT 1 -> W2 FAIL')
    rep('W4' in q(w4, ung.replace('NOW()', 'now()'), r1s, None).fails, 'PLANTED unguarded template 1 token off -> W4 FAIL')
    rep('W6' in q(w6, ['    // tracked separately -- see KS-TICKET.']).fails and not q(w6, ['    // tracked as KS 1424']).fails, 'PLANTED KS-TICKET placeholder -> W6 FAIL; a filled `KS 1424` passes')
    mem = "  it('RED KS-1278 R2: x', async () => {\n    const bound = call ? call.slice(1) : [];\n    expect([bound.includes('revoked')]).toEqual([true]);\n  });"
    pos = "  it('RED KS-1278 R2: x', async () => {\n    const bound = call ? call.slice(1) : [];\n    expect([bound[gi], bound[gi + 1]]).toEqual(['revoked', 'revoked']);\n  });"
    sl2 = "  it('RED KS-1278 R2: x', async () => {\n    const guardBindings = call ? call.slice(1).slice(-2) : [];\n    expect([guardBindings]).toEqual([['revoked', 'revoked']]);\n  });"
    rep('W7' in q(w7, mem, gua).fails and not q(w7, pos, gua).fails and not q(w7, sl2, gua).fails, 'W7: a membership-only R2 FAILS; an indexed R2 and a slice(-2) R2 pass')
    b = io.StringIO()
    with contextlib.redirect_stdout(b): r = run(repo, 'f' * 40, Tally())
    rep(r == 'UNRESOLVABLE' and 'head unresolvable' in b.getvalue(), 'absent head refuses BY NAME')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    repo = opt('--repo', K['checkout'])
    if '--selftest' in A: return selftest(repo)
    t = Tally()
    r = run(repo, opt('--head', os.environ.get('G68_HEAD', K['head_expected'])), t)
    if r == 'UNRESOLVABLE': return 2
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
