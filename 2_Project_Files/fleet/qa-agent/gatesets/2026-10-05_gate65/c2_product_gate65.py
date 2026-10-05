#!/usr/bin/env python3
r"""c2_product_gate65.py — C2 THROUGH-CODE: the product hunks of #1393 vs KS-1278 (READ verbs only; git objects).

  W1 documentRepo.ts base -> head: the ONLY non-comment lines added are the kit's five (the `ifStatusIsNot?: string;` option, the
     guardStatus declaration, `const affected = await (db || prisma).$executeRaw\``, the guard line, the guarded `return null`); the
     ONLY non-comment line removed is the unassigned `await (db || prisma).$executeRaw\``; every added comment block carries KS-1278 (§5d)
  W2 PARAMETERISATION: the guard line sits INSIDE a Prisma `$executeRaw` TAGGED TEMPLATE (opened by `$executeRaw\`` — never
     `$executeRawUnsafe`, never `Prisma.raw`/`sql.raw` — and not yet closed); `guardStatus` reaches SQL ONLY as `${guardStatus}`
     interpolations of that template (bound parameters), never quoted (`'${…}'`) and never concatenated (`+ guardStatus`)
  W3 OPT-IN: `guardStatus = opts?.ifStatusIsNot ?? null`, the null return is conditioned on `guardStatus !== null`, and across
     services/originate/src at the head EXACTLY ONE `updateDocument(` call passes `ifStatusIsNot` (the revoke route); the number of
     `updateDocument(` call sites is the same at base and head (CONTROL: that count is > 1, so the instrument sees callers)
  W4 routes/documents.ts base -> head: removed non-comment == [the unguarded call]; added non-comment == [the guarded call,
     `if (revoked === null) {`, the 400 line, `}`]; the new 400 line is BYTE-IDENTICAL to the read-time 400 line; comments carry KS-1278
  W5 ks1293 manifest: exactly ONE line added, `'ks1278-revoke-is-one-atomic-transition.test.ts',`, in sorted order (ks1264 < it < ks1293)
  W6 the new test: `it(` titles == the kit's four cells (R1, R2, C1, C2) and 0 `.skip` / `.only` / `xit` / `xdescribe`
  INFO the db client: the route reads with `(req as any).db` but the guarded write passes `undefined` (default prisma) — doubt D-MT
Usage: c2_product_gate65.py --repo <git dir> [--head <sha>]  |  --selftest --repo <git dir>
rc 0 all PASS / rc 1 any FAIL or 0 checked / rc 2 refused (an object unresolvable, named)."""
import os, re, sys, io, contextlib, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate65 import K, git, Tally

O = 'Blockchain/Dev/services/originate/src'
ADD_REPO = ['ifStatusIsNot?: string;', K['guard_decl'].strip(), 'const affected = await (db || prisma).$executeRaw`', K['guard_line'].strip(), K['guard_return'].strip()]
REM_REPO = ['await (db || prisma).$executeRaw`']
ADD_ROUTE = [K['route_call'].strip(), 'if (revoked === null) {', K['msg_400'], '}']
REM_ROUTE = [K['route_removed'].strip()]


def is_comment(l):
    s = l.strip()
    return s == '' or s.startswith('//') or s.startswith('/*') or s.startswith('*') or s.startswith('*/')


def delta(b, h):
    bl, hl = b.split('\n'), h.split('\n'); rem, add = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, bl, hl, autojunk=False).get_opcodes():
        if op != 'equal': rem += bl[i1:i2]; add += hl[j1:j2]
    return rem, add


def judge_repo(t, b, h):
    rem, add = delta(b, h)
    cr = [l.strip() for l in rem if not is_comment(l)]; ca = [l.strip() for l in add if not is_comment(l)]
    com = [l for l in add if is_comment(l) and l.strip()]
    t.check('W1', cr == REM_REPO and ca == ADD_REPO and any('KS-1278' in l for l in com),
            'documentRepo.ts non-comment removed %s | added %s | comment lines added %d, carry KS-1278 %s' % (cr, [x[:60] for x in ca], len(com), any('KS-1278' in l for l in com)))
    hl = h.split('\n'); gi = [i for i, l in enumerate(hl) if 'status IS DISTINCT FROM' in l]
    opened = None
    if len(gi) == 1:
        for i in range(gi[0], -1, -1):
            if '`' in hl[i] and i != gi[0]:
                opened = hl[i]; break
    inside = opened is not None and re.search(r'\$executeRaw`\s*$', opened) is not None and 'Unsafe' not in opened
    unclosed = len(gi) == 1 and all('`' not in hl[i] for i in range(hl.index(opened) + 1 if opened in hl else 0, gi[0] + 1)) if opened else False
    uses = re.findall(r'.{0,3}guardStatus.{0,3}', '\n'.join(hl[gi[0]:gi[0] + 1])) if gi else []
    quoted = bool(re.search(r"'\$\{guardStatus\}'", h)); concat = bool(re.search(r'\+\s*guardStatus|guardStatus\s*\+', h))
    raw = bool(re.search(r'(Prisma|sql)\.raw\(|\$executeRawUnsafe\([^)]*guardStatus', h))
    t.check('W2', len(gi) == 1 and inside and unclosed and not quoted and not concat and not raw and len(re.findall(r'\$\{guardStatus\}', hl[gi[0]] if gi else '')) == 2,
            'guard lines %d; template opener %r is a $executeRaw tagged template %s, unclosed up to the guard %s; ${guardStatus} interpolations on the guard line %d (want 2); quoted %s concatenated %s raw/unsafe %s' % (
                len(gi), (opened or '').strip()[:60], inside, unclosed, len(re.findall(r'\$\{guardStatus\}', hl[gi[0]] if gi else '')), quoted, concat, raw))
    t.info('W2-uses', 'guard line: %s' % (hl[gi[0]].strip() if gi else 'ABSENT'))
    return h


def judge_optin(t, h, calls_base, calls_head):
    decl = K['guard_decl'].strip() in h; ret = K['guard_return'].strip() in h
    guarded = [c for c in calls_head if 'ifStatusIsNot' in c]
    t.check('W3', decl and ret and len(guarded) == 1 and 'routes/documents.ts' in guarded[0] and len(calls_base) == len(calls_head) and len(calls_head) > 1,
            'guard declared `?? null` %s; null return conditioned on guardStatus !== null %s | updateDocument( call sites base %d head %d (CONTROL > 1); passing ifStatusIsNot %d: %s' % (
                decl, ret, len(calls_base), len(calls_head), len(guarded), [g[:90] for g in guarded]))


def judge_route(t, b, h):
    rem, add = delta(b, h)
    cr = [l.strip() for l in rem if not is_comment(l)]; ca = [l.strip() for l in add if not is_comment(l)]
    com = [l for l in add if is_comment(l) and l.strip()]
    reads = [l.strip() for l in h.split('\n') if l.strip() == K['msg_400']]
    t.check('W4', cr == REM_ROUTE and ca == ADD_ROUTE and len(reads) == 2 and any('KS-1278' in l for l in com),
            'documents.ts non-comment removed %s | added %s | the exact 400 line occurs %d time(s) (want 2: read-time + guard) | comments carry KS-1278 %s' % (
                [x[:60] for x in cr], [x[:60] for x in ca], len(reads), any('KS-1278' in l for l in com)))
    ln = h.split('\n'); s0 = next((i for i, l in enumerate(ln) if "'/:id/revoke'" in l), 0)
    e0 = next((i for i in range(s0 + 1, len(ln)) if ln[i].startswith('documentsRouter.')), len(ln))
    dbr = [i + 1 for i in range(s0, e0) if 'getDocument(id, tenantId, (req as any).db)' in ln[i]]
    t.info('W4-db', 'revoke route read uses (req as any).db (head lines %s); the guarded write passes db=undefined -> default prisma. Under MULTI_TENANCY_ENABLED=true the two clients differ (index.ts sets req.db = getRequestPrisma(req)): doubt D-MT' % dbr[:6])


def judge_manifest(t, b, h):
    rem, add = delta(b, h); new = "  'ks1278-revoke-is-one-atomic-transition.test.ts',"
    hl = h.split('\n'); ok_order = False
    if new in hl:
        i = hl.index(new); ok_order = hl[i - 1].strip().startswith("'ks1264") and hl[i + 1].strip().startswith("'ks1293")
    t.check('W5', rem == [] and add == [new] and ok_order, 'ks1293 removed %d added %s; sorted between ks1264 and ks1293 %s' % (len(rem), add, ok_order))


def judge_test(t, src):
    titles = re.findall(r"(?m)^\s*it\(\s*'([^']+)'", src); bad = re.findall(r'\b(it|describe|test)\.(skip|only)\b|\bx(it|describe)\(', src)
    want = list(K['cells'].values()); got = [next((w for w in want if ti.startswith(w)), None) for ti in titles]
    t.check('W6', got == want and not bad, '`it(` titles %d %s | skip/only %s' % (len(titles), [ti[:28] for ti in titles], bad))


def calls(repo, rev):
    out = git(repo, 'grep', '-n', '-F', 'updateDocument(', rev, '--', O, check=False)[1]
    return [l for l in out.splitlines() if 'export async function updateDocument' not in l and '__tests__' not in l]


def run_all(t, repo, head, override=None):
    ov = override or {}; b = K['base']
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    rh = ov.get('repo', g(head, K['repo_file'])); judge_repo(t, g(b, K['repo_file']), rh)
    judge_optin(t, rh, calls(repo, b), ov.get('calls', calls(repo, head)))
    judge_route(t, g(b, K['route_file']), ov.get('route', g(head, K['route_file'])))
    judge_manifest(t, g(b, K['manifest_test']), ov.get('manifest', g(head, K['manifest_test'])))
    judge_test(t, ov.get('test', g(head, K['test'])))


def selftest(repo):
    if not repo or git(repo, 'rev-parse', '--verify', '--quiet', K['head'] + '^{commit}', check=False)[0] != 0:
        print('SELFTEST REFUSED: --repo must hold the head %s (fetch it by sha into YOUR clone)' % K['head']); return 2
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p)); h = K['head']
    RH, RT, MF, TS = g(h, K['repo_file']), g(h, K['route_file']), g(h, K['manifest_test']), g(h, K['test'])
    CH = calls(repo, h)
    def sub(s, a, b_):
        assert s.count(a) == 1, 'tamper anchor must occur exactly once (%d): %r' % (s.count(a), a[:60]); return s.replace(a, b_)
    def go(ov):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): run_all(t, repo, h, ov)
        return t
    t0 = go({}); ok = int(not t0.fails and t0.n == 6); total = 1
    print('SELFTEST %s T0 positive control (the REAL head blobs): %d checked, fails %s' % ('OK' if ok else 'MISS', t0.n, t0.fails))
    arms = [
        ('$executeRawUnsafe instead of the tagged template', {'repo': sub(RH, 'const affected = await (db || prisma).$executeRaw`', 'const affected = await (db || prisma).$executeRawUnsafe(`')}, ['W1', 'W2']),
        ('guard value QUOTED into the SQL text', {'repo': sub(RH, 'status IS DISTINCT FROM ${guardStatus}::text)', "status IS DISTINCT FROM '${guardStatus}'::text)")}, ['W1', 'W2']),
        ('guard line moved AFTER the template closed', {'repo': sub(sub(RH, K['guard_line'] + '\n', ''), "    `;\n    if (guardStatus", "    `;\n" + K['guard_line'] + "\n    if (guardStatus")}, ['W2']),
        ('null return no longer conditioned on guardStatus', {'repo': sub(RH, K['guard_return'], '    if (affected === 0) return null;')}, ['W1', 'W3']),
        ('a second caller opts in (anchorStateSync)', {'calls': CH + ['%s:%s/services/anchorStateSync.ts:9: await updateDocument(id, t, u, undefined, { ifStatusIsNot: \'anchored\' });' % (h, O)]}, ['W3']),
        ('a caller removed (count drift)', {'calls': CH[1:]}, ['W3']),
        ('a different 400 message on the guard branch', {'route': sub(RT, "      if (revoked === null) {\n        " + K['msg_400'], "      if (revoked === null) {\n        " + K['msg_400'].replace('already revoked', 'not revocable'))}, ['W4']),
        ('the route records BEFORE the null check (an extra code line)', {'route': sub(RT, '      if (revoked === null) {\n', "      recordOnBehalfOf(req, id, 'revoke', revokeObo);\n      if (revoked === null) {\n")}, ['W4']),
        ('a second manifest line', {'manifest': sub(MF, "  'ks1293-originate-suite-is-hermetic.test.ts',", "  'ks1293-originate-suite-is-hermetic.test.ts',\n  'ks9999-x.test.ts',")}, ['W5']),
        ('manifest line out of order', {'manifest': sub(sub(MF, "  'ks1278-revoke-is-one-atomic-transition.test.ts',\n", ''), "  'ks444-certifications-issue-body-types.test.ts',", "  'ks444-certifications-issue-body-types.test.ts',\n  'ks1278-revoke-is-one-atomic-transition.test.ts',")}, ['W5']),
        ('R1 skipped', {'test': sub(TS, "  it('RED KS-1278 R1", "  it.skip('RED KS-1278 R1")}, ['W6']),
        ('C2 renamed', {'test': sub(TS, "it('control KS-1278 C2", "it('control C2")}, ['W6']),
    ]
    for name, ov, want in arms:
        t = go(ov); total += 1; new = set(t.fails) - set(t0.fails); gd = set(want) <= new; ok += gd
        print('SELFTEST %s %s: want NEW FAIL %s | got %s' % ('OK' if gd else 'MISS', name, want, sorted(new)))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    repo = opt('--repo')
    if '--selftest' in A: raise SystemExit(selftest(repo))
    head = opt('--head', K['head'])
    for s in (head, K['base']):
        if git(repo, 'rev-parse', '--verify', '--quiet', s + '^{commit}', check=False)[0] != 0:
            print('REFUSED: %s unresolvable in %s — fetch it by sha into YOUR clone (X7)' % (s, repo)); raise SystemExit(2)
    print('c2_product_gate65 repo %s head %s base %s' % (repo, head[:12], K['base'][:12]))
    t = Tally(); run_all(t, repo, head); raise SystemExit(t.end())
