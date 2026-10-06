#!/usr/bin/env python3
"""c2_product_gate69.py — C2 THROUGH-CODE instruments for the gate69 BATCH. READ verbs only. Every check works on TEXT (develop blob vs
head blob), so --selftest feeds PLANTED texts through the SAME functions and each arm must FAIL.

PR A (#1395 KS-1305, originate src/db.ts = THE TENANT-ISOLATION MODULE; T1 because of where it lives):
  WA1 PURE INSERTION: db.ts merge-base..head numstat 19 / 0; ONE -U0 hunk; head minus the inserted lines == develop BYTE FOR BYTE; the
      hunk sits INSIDE getPrismaClient(), after `// Dynamic import …` and before `const { PrismaClient } = require('@prisma/client');`
  WA2 no ADDED line matches the tenant / GUC / RLS regex (kit tenant_rx) — with a MUST-HIT CONTROL: the same regex hits >= 10 lines of
      the unchanged develop db.ts (a regex that cannot hit proves nothing)
  WA3 every develop line matching tenant_rx is present at the head the SAME number of times (multiset equality) — the GUC / RLS / tenant
      lines are untouched, measured, not inferred from WA1
  WA4 THE GUARD: exactly ONE `if (` among the added lines; its condition splits on top-level `&&` into exactly 2 terms: the CODE term
      (`err?.code === 'MODULE_NOT_FOUND'`) and the MESSAGE term (`.includes('.prisma/client')`); the catch ends with `throw err;` (the
      SAME object); `throw err;` count head == develop + 1. Printed: the READY / commit call it a "three-term conjunction" — it is TWO
      conjuncts plus the same-object rethrow (Arm B tampers the rethrow, not a conjunct)
  WA5 the KS-458 tenant-GUC test file (6 cells) is byte-identical at the head and develop
  WA6 §5d: the inserted block carries a `KS-1305` why-comment; every non-comment added line is inside that commented block
PR B (#1396 KS-1256, api-gateway routes/verification.ts):
  WB1 every verification.ts hunk lies inside the `if (connectorMeta) {` branch, between it and `if (containerBad) {`
  WB2 the availability test `if (!redisService.isRedisAvailable()) {` occurs ONCE, BEFORE the allow-list read (the FIRST
      getNotificationSettings('platform-settings') line), and its body is a 503 + return
  WB3 the bare `} catch {}` after the read is gone (develop count - 1) and the replacing catch body answers 503 + return
  WB4 the SECOND platform-settings reader is untouched: its +/-8-line context is byte-identical develop vs head (line numbers printed —
      develop :1283, head :1304; the committed comments cite :1283)
  WB5 the 6 doubles files: 0 deletions, 33 additions in total, 0 added `expect(`, every file's additions name isRedisAvailable
  WB6 ks1195: exactly 2 changed assertion lines (-/+ pairs containing `expect(`), the title line, a header comment; the no-Redis
      precondition line and every DEGRADED / redis-not-ready line UNCHANGED
  WB7 isRedisAvailable consumers outside services/redis.ts and __tests__: exactly verification.ts (INFO: a module mock overriding the
      export reaches ONLY that consumer; redis.ts's own calls use the module-local binding)
  WB8 §5d: the verification.ts additions carry `KS-1256` why-comments (both new blocks)
Usage: c2_product_gate69.py --pr A|B --repo R [--head H] | --selftest --repo R          rc 0 PASS / 1 FAIL / 2 refused"""
import io, contextlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate69 import K, git, Tally, resolvable, spec

TRX = re.compile(K['prs']['A']['tenant_rx'])


def L(s): return s.split('\n')


def hunks(dtext, htext):
    """-U0 hunks computed in-process (difflib), as [(dev_start, dev_lines, head_start, head_lines)] 0-based."""
    import difflib
    sm = difflib.SequenceMatcher(None, L(dtext), L(htext), autojunk=False)
    return [(i1, L(dtext)[i1:i2], j1, L(htext)[j1:j2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']


def added(dtext, htext): return [l for _, _, _, a in hunks(dtext, htext) for l in a]
def removed(dtext, htext): return [l for _, r, _, _ in hunks(dtext, htext) for l in r]


def split_top_and(cond):
    depth = 0; parts = []; cur = ''
    i = 0
    while i < len(cond):
        ch = cond[i]
        if ch in '([{': depth += 1
        if ch in ')]}': depth -= 1
        if depth == 0 and cond[i:i + 2] == '&&':
            parts.append(cur.strip()); cur = ''; i += 2; continue
        cur += ch; i += 1
    parts.append(cur.strip()); return [p for p in parts if p]


def check_A(t, sp, dtext, htext, ks458_dev=None, ks458_head=None):
    hs = hunks(dtext, htext); add = added(dtext, htext); rem = removed(dtext, htext)
    H = L(htext)
    ok1 = len(hs) == 1 and not rem and len(add) == sp['numstat'][sp['product_file']][0]
    inside = False
    if len(hs) == 1:
        j = hs[0][2]; n = len(hs[0][3])
        before = [i for i, l in enumerate(H) if l == sp['insert_anchor_after']]; after = [i for i, l in enumerate(H) if l == sp['insert_anchor_before']]
        gp = [i for i, l in enumerate(H) if 'function getPrismaClient()' in l]
        inside = len(before) == 1 and len(after) == 1 and len(gp) == 1 and gp[0] < before[0] < j and j + n == after[0]
        ok1 = ok1 and H[:j] + H[j + n:] == L(dtext)
    t.check('WA1', ok1 and inside, 'hunks %d | added %d removed %d (kit %s) | head minus the insertion == develop %s | inside getPrismaClient between the two anchors %s' % (
        len(hs), len(add), len(rem), sp['numstat'][sp['product_file']], ok1, inside))
    hit_add = [l.strip()[:80] for l in add if TRX.search(l)]
    ctl = [l for l in L(dtext) if TRX.search(l)]
    t.check('WA2', not hit_add and len(ctl) >= 10, 'added lines matching tenant_rx: %d %s | MUST-HIT CONTROL: the same regex hits %d develop lines (want >= 10)' % (len(hit_add), hit_add[:3], len(ctl)))
    from collections import Counter
    dc = Counter(l for l in L(dtext) if TRX.search(l)); hc = Counter(l for l in L(htext) if TRX.search(l))
    lost = {l.strip()[:70]: dc[l] - hc[l] for l in dc if hc[l] != dc[l]}; new = {l.strip()[:70]: hc[l] - dc[l] for l in hc if hc[l] != dc[l] and l not in dc}
    t.check('WA3', not lost and not new, 'develop tenant / GUC / RLS lines %d distinct (%d total): changed-count %s | new %s' % (len(dc), sum(dc.values()), lost or 'none', new or 'none'))
    ifs = [l for l in add if re.match(r'^\s*if \(', l)]
    terms = split_top_and(re.sub(r'^\s*if \((.*)\)\s*\{\s*$', r'\1', ifs[0])) if len(ifs) == 1 else []
    code_t = [x for x in terms if "code === 'MODULE_NOT_FOUND'" in x]; msg_t = [x for x in terms if ".includes('.prisma/client')" in x]
    body = '\n'.join(add)
    rethrow = re.search(r"\}\s*\n\s*throw err;\s*\n\s*\}\s*$", body) is not None
    te = (htext.count('throw err;'), dtext.count('throw err;'))
    t.check('WA4', len(ifs) == 1 and len(terms) == 2 and len(code_t) == 1 and len(msg_t) == 1 and rethrow and te[0] == te[1] + 1,
            'if-statements added %d | top-level && terms %d %s | CODE term %d MESSAGE term %d | catch ends `throw err;` (same object) %s | `throw err;` head %d develop %d | NOTE the claim "three-term conjunction": %d conjunct(s) + the rethrow' % (
                len(ifs), len(terms), [x[:50] for x in terms], len(code_t), len(msg_t), rethrow, te[0], te[1], len(terms)))
    if ks458_dev is not None:
        t.check('WA5', ks458_dev == ks458_head and len(re.findall(r"^\s*it\(", ks458_head, re.M)) == list(sp['sibling_tests'].values())[0],
                'ks458 test byte-identical develop/head %s | it( cells %d (kit %d)' % (ks458_dev == ks458_head, len(re.findall(r"^\s*it\(", ks458_head or '', re.M)), list(sp['sibling_tests'].values())[0]))
    com = [l for l in add if l.strip().startswith('//')]
    t.check('WA6', any('KS-1305' in l for l in com) and add and add[0].strip().startswith('//'), '§5d: added comment lines %d, carrying KS-1305 %d; the insertion OPENS with the why-comment %s' % (
        len(com), sum('KS-1305' in l for l in com), bool(add) and add[0].strip().startswith('//')))


def check_B(t, sp, dtext, htext, files=None, consumers=None):
    H = L(htext); hs = hunks(dtext, htext)
    cb = [i for i, l in enumerate(H) if l == sp['connector_branch_open']]; bad = [i for i, l in enumerate(H) if l.strip() == 'if (containerBad) {']
    # `if (connectorMeta) {` occurs TWICE in the handler at the head (:1204 and :1301); the branch that matters is the LAST opening
    # before the first hunk, and the hunks must end before the first `if (containerBad) {` after it
    first = min((j for _, _, j, _ in hs), default=-1)
    cb = [max(i for i in cb if i < first)] if [i for i in cb if i < first] else []
    bad = [i for i in bad if cb and i > cb[0]]
    inside = len(cb) == 1 and len(bad) >= 1 and all(cb[0] < j and j + len(a) <= bad[0] for _, _, j, a in hs)
    t.check('WB1', bool(hs) and inside, '%d hunk(s) at head lines %s | all inside `if (connectorMeta) {` (:%s) .. `if (containerBad) {` (:%s): %s' % (
        len(hs), [j + 1 for _, _, j, _ in hs], cb[0] + 1 if cb else None, bad[0] + 1 if bad else None, inside))
    av = [i for i, l in enumerate(H) if l == sp['availability_check']]
    rd = [i for i, l in enumerate(H) if l == sp['read_line']]
    body_ok = len(av) == 1 and 'res.status(503)' in H[av[0] + 1] and H[av[0] + 2].strip() == 'return;'
    t.check('WB2', len(av) == 1 and rd and av[0] < rd[0] and body_ok, 'availability test x%d at :%s | first allow-list read at :%s | test BEFORE read %s | body 503 + return %s' % (
        len(av), av[0] + 1 if av else None, rd[0] + 1 if rd else None, bool(av and rd and av[0] < rd[0]), body_ok))
    bare = (sum(1 for l in L(dtext) if l.strip() == '} catch {}'), sum(1 for l in L(htext) if l.strip() == '} catch {}'))   # CODE lines only: the new comment QUOTES `} catch {}`
    ci = [i for i in range(len(H)) if H[i].strip() == '} catch {' and rd and i > rd[0]]
    cbody = '\n'.join(H[ci[0]:ci[0] + 12]) if ci else ''
    t.check('WB3', bare[1] == bare[0] - 1 and 'res.status(503)' in cbody and re.search(r'res\.status\(503\)[^\n]*\n\s*return;', cbody) is not None,
            'bare `} catch {}` develop %d head %d | the catch after the read answers 503 + return %s' % (bare[0], bare[1], 'res.status(503)' in cbody))
    D = L(dtext)
    rd_d = [i for i, l in enumerate(D) if l == sp['read_line']]
    if len(rd_d) >= 2 and len(rd) >= 2:
        cd, ch = D[rd_d[1] - 8:rd_d[1] + 9], H[rd[1] - 8:rd[1] + 9]
        t.check('WB4', cd == ch, 'second platform-settings reader: develop :%d head :%d | +/-8-line context identical %s (the committed comments cite :1283 = the DEVELOP line)' % (rd_d[1] + 1, rd[1] + 1, cd == ch))
    else:
        t.check('WB4', False, 'second reader not found (develop %d, head %d read lines)' % (len(rd_d), len(rd)))
    if files is not None:
        rows = []; tot_a = tot_d = 0; exp_add = 0; all_name = True
        for p, (dv, hv) in files['doubles'].items():
            a = added(dv, hv); r = removed(dv, hv); tot_a += len(a); tot_d += len(r)
            exp_add += sum('expect(' in l for l in a); nm = any('isRedisAvailable' in l for l in a); all_name &= nm
            rows.append('%s +%d/-%d' % (os.path.basename(p)[:12], len(a), len(r)))
        t.check('WB5', [tot_a, tot_d] == sp['doubles_numstat_total'] and exp_add == 0 and all_name and len(files['doubles']) == 6,
                'doubles %s | total +%d/-%d (kit %s) | added expect( %d | every file names isRedisAvailable %s' % (rows, tot_a, tot_d, sp['doubles_numstat_total'], exp_add, all_name))
        dv, hv = files['ks1195']
        hs95 = hunks(dv, hv)
        pairs = [(r, a) for _, r, _, a in hs95 if r and a]
        exp_pairs = sum(1 for r, a in pairs for x, y in zip(r, a) if 'expect(' in x and 'expect(' in y)
        title = sum(1 for r, a in pairs for x, y in zip(r, a) if x.strip().startswith('it(') and y.strip().startswith('it('))
        header = sum(1 for _, r, _, a in hs95 if not r and a and a[0].startswith('/**'))
        pre = [l for l in L(dv) if 'precondition: no Redis' in l]; deg = [l for l in L(dv) if re.search(r'DEGRADED|redis-not-ready', l)]
        same = pre and all(l in hv for l in pre) and all(L(hv).count(l) == L(dv).count(l) for l in deg)
        t.check('WB6', exp_pairs == sp['ks1195_changed_assertions'] and title == 1 and header == 1 and same and len(pairs) == 3,
                'ks1195: changed -/+ pairs %d | assertion pairs %d (kit %d) | title pairs %d | header comment blocks %d | precondition + %d DEGRADED/redis-not-ready line(s) unchanged %s' % (
                    len(pairs), exp_pairs, sp['ks1195_changed_assertions'], title, header, len(deg), bool(same)))
    if consumers is not None:
        t.check('WB7', consumers == ['Blockchain/Dev/services/api-gateway/src/routes/verification.ts'], 'isRedisAvailable consumers outside redis.ts / __tests__: %s' % consumers)
    add = added(dtext, htext)
    blocks = sum(1 for l in add if l.strip().startswith('// KS-1256'))
    t.check('WB8', blocks >= 2, '§5d: added `// KS-1256` why-comment openings %d (want >= 2: the availability test and the catch)' % blocks)


def load_A(repo, sp):
    b, h = sp['merge_base'], sp['head']; s = list(sp['sibling_tests'])[0]
    return git(repo, 'show', '%s:%s' % (b, sp['product_file'])), git(repo, 'show', '%s:%s' % (h, sp['product_file'])), git(repo, 'show', '%s:%s' % (b, s)), git(repo, 'show', '%s:%s' % (h, s))


def load_B(repo, sp):
    b, h = sp['merge_base'], sp['head']
    sh = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    files = {'doubles': {p: (sh(b, p), sh(h, p)) for p in sp['doubles_files']}, 'ks1195': (sh(b, sp['ks1195_file']), sh(h, sp['ks1195_file']))}
    g = git(repo, 'grep', '-l', '-i', 'isRedisAvailable', h, '--', 'Blockchain/Dev/services/api-gateway/src', check=False)[1]
    cons = sorted(x.split(':', 1)[1] for x in g.splitlines() if x and '__tests__' not in x and not x.endswith('services/redis.ts'))
    return sh(b, sp['product_file']), sh(h, sp['product_file']), files, cons


def selftest(repo):
    ok = n = 0
    def arm(name, fn, want):
        nonlocal ok, n
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): fn(t)
        good = (not t.fails) if want is None else (want in t.fails)
        n += 1; ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, t.fails or 'NONE'))
    spA = spec('A'); d, h, kd, kh = load_A(repo, spA)
    arm('A real head', lambda t: check_A(t, spA, d, h, kd, kh), None)
    gl = [l for l in L(h) if "set_config('app.current_tenant_id'" in l][0]
    arm('PLANTED A: a GUC line edited (set_config tenant -> bypass)', lambda t: check_A(t, spA, d, h.replace(gl, gl.replace('app.current_tenant_id', 'app.tenant_scope_bypass')), kd, kh), 'WA3')
    arm('PLANTED A: an added line touching the tenant scope', lambda t: check_A(t, spA, d, h.replace("      require('@prisma/client');\n", "      require('@prisma/client'); // currentTenantId()\n", 1), kd, kh), 'WA2')
    arm('PLANTED A: a THIRD conjunct', lambda t: check_A(t, spA, d, h.replace("String(err?.message).includes('.prisma/client')) {", "String(err?.message).includes('.prisma/client') && err?.requireStack) {"), kd, kh), 'WA4')
    arm('PLANTED A: the rethrow replaced by a new Error', lambda t: check_A(t, spA, d, h.replace("      throw err;\n    }\n    const { PrismaClient }", "      throw new Error(String(err));\n    }\n    const { PrismaClient }"), kd, kh), 'WA4')
    arm('PLANTED A: one develop line deleted inside the module', lambda t: check_A(t, spA, d, h.replace(gl + '\n', '', 1), kd, kh), 'WA1')
    arm('PLANTED A: ks458 edited', lambda t: check_A(t, spA, d, h, kd, kh + '\n// edit'), 'WA5')
    spB = spec('B', None, '1396'); bd, bh, files, cons = load_B(repo, spB)
    arm('B real head', lambda t: check_B(t, spB, bd, bh, files, cons), None)
    moved = bh.replace(spB['availability_check'] + '\n', '', 1).replace(spB['read_line'] + '\n', spB['read_line'] + '\n' + spB['availability_check'] + '\n', 1)
    arm('PLANTED B: the availability test moved AFTER the read', lambda t: check_B(t, spB, bd, moved, files, cons), 'WB2')
    arm('PLANTED B: the bare catch restored', lambda t: check_B(t, spB, bd, bh.replace("        } catch {\n          // KS-1256: a THROWN read", "        } catch {}\n        if (false) {\n          // KS-1256: a THROWN read", 1), files, cons), 'WB3')
    arm('PLANTED B: a hunk OUTSIDE the connector branch', lambda t: check_B(t, spB, bd, bh.replace(spB['connector_branch_open'] + '\n', '      // planted\n' + spB['connector_branch_open'] + '\n', 1), files, cons), 'WB1')
    f2 = {'doubles': dict(files['doubles']), 'ks1195': files['ks1195']}
    p0 = spB['doubles_files'][0]; f2['doubles'][p0] = (files['doubles'][p0][0], files['doubles'][p0][1] + '\nexpect(1).toBe(1);')
    arm('PLANTED B: an assertion added to a doubles file', lambda t: check_B(t, spB, bd, bh, f2, cons), 'WB5')
    f3 = {'doubles': files['doubles'], 'ks1195': (files['ks1195'][0], files['ks1195'][1].replace("toEqual(['2', '2', '2', '2', '2'])", "toEqual(['2', '2', '2', '2', '3'])"))}
    arm('PLANTED B: a THIRD ks1195 assertion changed', lambda t: check_B(t, spB, bd, bh, f3, cons), 'WB6')
    arm('PLANTED B: a second isRedisAvailable consumer', lambda t: check_B(t, spB, bd, bh, files, cons + ['Blockchain/Dev/services/api-gateway/src/routes/admin.ts']), 'WB7')
    print('SELFTEST %s %d of %d' % ('OK' if ok == n else 'BROKEN', ok, n)); print('CHECKED %d arm(s)' % n)
    return 0 if ok == n else 1


def main():
    A = sys.argv[1:]
    if not A or '--help' in A: print(__doc__); return 2
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    repo = opt('--repo', K['checkout'])
    if '--selftest' in A: return selftest(repo)
    which = opt('--pr', 'A'); sp = spec(which, opt('--head'), opt('--b-pr') if which == 'B' else None)
    for nm, s in (('head', sp['head']), ('merge-base', sp['merge_base'])):
        if not resolvable(repo, s): print('C2 REFUSED: %s unresolvable: %s' % (nm, s)); print('CHECKED 0'); return 2
    print('c2_product_gate69 PR %s %s | head %s | merge-base %s' % (which, sp['ticket'], sp['head'][:12], sp['merge_base'][:12]))
    t = Tally()
    if which == 'A': check_A(t, sp, *load_A(repo, sp))
    else:
        d, h, files, cons = load_B(repo, sp); check_B(t, sp, d, h, files, cons)
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
