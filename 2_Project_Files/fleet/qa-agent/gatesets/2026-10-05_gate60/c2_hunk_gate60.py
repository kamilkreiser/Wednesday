#!/usr/bin/env python3
"""c2_hunk_gate60.py — gate60 C2 HUNK for #1384 (KS-1210) vs the ticket and Q-1210, plus THE CLASS HUNT over routes/oauth.ts. Git objects only,
in YOUR scratch clone (read verbs); nothing is run.
  H1 SCOPE     services/oauth.ts, routes/users.ts and middleware/authenticate.ts BYTE-IDENTICAL develop -> head (blob ids, kit); in
               routes/oauth.ts the non-comment REMOVED lines are EXACTLY the kit's 4 (the pgSafeStringSchema import, both `scopes:
               z.array(pgSafeStringSchema)` lines, GET's `getAppById(req.params.id)`), the non-comment ADDED lines number exactly 43, and no
               added line names pgSafeStringSchema.
  H2 VOCAB     both schemas' `scopes:` line is `z.array(z.enum(AVAILABLE_SCOPES …)).optional()`; services/oauth.ts AVAILABLE_SCOPES parses to
               EXACTLY the kit nine (order kept); createApp's default scope list is a subset of the nine with NO privileged scope.
               INFO: the ks1210 test MOCKS AVAILABLE_SCOPES with its own NINE literal — compared here to the real nine (ks855 R1/CONTROL pin
               the real list's length and grouping; nothing pins the mock to the source).
  H3 LISTS     OAUTH_PRIVILEGED_SCOPES == kit privileged (and inside the nine); OAUTH_PLATFORM_ADMIN_ROLES == users.ts PLATFORM_ADMIN_ROLES ==
               kit 4; OAUTH_APP_ADMIN_ROLES == users.ts ADMIN_ROLES == kit 6 — an INDEPENDENT parser (the text after the `=`), not the test's.
  H4 BY-ID GATE (the class hunt) EVERY `oauthRouter.<verb>('…:id…'` handler: `appVisibleTo(req, req.params.id)` occurs BEFORE the first
               service call (getAppById( / updateApp( / rotateSecret( ) and its falsy branch returns 404 NOT_FOUND. CHECKED must be 4, the
               kit's by-id set == the handlers found. Every OTHER route registration is printed with what it reads (app by client_id,
               scope validation) as INFO for the gate to rule.
  H5 ORDER     PATCH: the ownership 404 precedes the privileged-scope 403 (non-disclosure); POST /apps: the privileged check precedes
               createApp( and uses isOauthPlatformAdmin (the FOUR list), never isOauthAppAdmin.
  H6 VISIBLE   appVisibleTo: owner test `app.createdBy && app.createdBy === req.user?.userId`, then isOauthAppAdmin, else null; the two
               role predicates read the right list (platform -> OAUTH_PLATFORM_ADMIN_ROLES, app admin -> OAUTH_APP_ADMIN_ROLES).
  H7 SIBLINGS  ks431 / ks451 develop -> head: `it(` count equal; the multiset of `expect(` lines, with every quoted string and string
               array normalised to <S>, is EQUAL (no assertion added, removed, inverted or weakened — only fixture literals changed).
  INFO         listApps(userId?) returns EVERY app for a falsy userId; createdBy NULL rows are admin-only; tenant predicate count in the four
               handlers (0 = the bound is RLS + seedTenantGuc alone).
--selftest  the REAL develop/head PASS (positive control); planted head copies FAIL their check: rotate-secret ungated (H4), PATCH order
            swapped (H5), the create gate on isOauthAppAdmin (H5), ORG_ADMIN added to the platform list (H3), the update schema reopened
            (H1+H2), services/oauth.ts edited (H1), an expect() removed from ks451 (H7), the owner test dropped (H6). And the REAL develop
            as the head is the must-fail arm on real code (H4 finds 0 of 4 gated).
Usage: c2_hunk_gate60.py --repo <clone> [--head sha] [--selftest]      rc 0 PASS / 1 FAIL / 2 usage"""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate60 import K, git, now, Checks, opt_factory, show, blob, has_commit, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); HEAD = opt('--head', K['head']); DEV = K['develop']
for s in (HEAD, DEV):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)
P, SV, US, AU = K['product'], K['service'], K['users_ts'], K['authenticate']
REMOVED = ["import { pgSafeStringSchema, runWithTenantId } from '@secuura/shared';", "  scopes: z.array(pgSafeStringSchema).optional(),",
           "  scopes: z.array(pgSafeStringSchema).optional(),", "    const app = await getAppById(req.params.id);"]
ADDED_N = 41   # difflib.SequenceMatcher non-comment added lines (git diff -U0 shows 43: two closing braces pair differently)
SCOPES_LINE = "  scopes: z.array(z.enum(AVAILABLE_SCOPES as unknown as [string, ...string[]])).optional(),"
SVC_CALL = re.compile(r'\b(getAppById|updateApp|rotateSecret)\(')
NOC = lambda l: l.strip() and not l.strip().startswith(('//', '/*', '*'))


def array_after(src, decl):
    i = src.find(decl)
    if i < 0: return None
    eq = src.find('=', i); o = src.find('[', eq); c = src.find(']', o)
    if eq < 0 or o < 0 or c < 0: return None
    return [s.strip().strip('\'"') for s in src[o + 1:c].split(',') if s.strip()]


def handlers(src):
    """[(registration line, body text)] for every top-level oauthRouter.<verb>( registration"""
    ls = src.split('\n'); idx = [i for i, l in enumerate(ls) if re.match(r'oauthRouter\.(get|post|patch|put|delete)\(', l)]
    out = []
    for n, i in enumerate(idx):
        end = idx[n + 1] if n + 1 < len(idx) else len(ls)
        close = next((j for j in range(i, end) if ls[j].startswith('});')), end - 1)   # the handler ends at its own top-level `});`
        out.append((ls[i], '\n'.join(ls[i:close + 1])))
    return out


def fn_body(src, sig):
    i = src.find(sig)
    if i < 0: return ''
    j = src.find('\n}\n', i)
    return src[i:j + 2] if j > 0 else src[i:]


def norm_expects(src):
    ex = [l.strip() for l in src.split('\n') if 'expect(' in l and NOC(l)]
    ex = [re.sub(r"'[^']*'|\"[^\"]*\"|`[^`]*`", '<S>', re.sub(r'//.*$', '', l)).strip() for l in ex]
    return collections.Counter(re.sub(r'\[\s*<S>(\s*,\s*<S>)*\s*\]', '[<S>]', l) for l in ex)


def judge(C, X):
    d, h = X['dev'], X['head']
    same = {p: X['blob_dev'][p] == X['blob_head'][p] and X['blob_dev'][p] is not None for p in (SV, US, AU)}
    dl, hl = d[P].split('\n'), h[P].split('\n')
    import difflib
    rem, add = [], []
    for op in difflib.SequenceMatcher(None, dl, hl, autojunk=False).get_opcodes():
        if op[0] in ('replace', 'delete'): rem += [l for l in dl[op[1]:op[2]] if NOC(l)]
        if op[0] in ('replace', 'insert'): add += [l for l in hl[op[3]:op[4]] if NOC(l)]
    C.chk('H1 scope of change', all(same.values()) and sorted(rem) == sorted(REMOVED) and len(add) == ADDED_N and not any('pgSafeStringSchema' in l for l in add),
          'byte-identical develop->head: %s | oauth.ts non-comment removed %d line(s) == the kit 4: %s | added %d (kit %d) | pgSafeStringSchema in an added line: %s' % (
              {p.split('/')[-1]: v for p, v in same.items()}, len(rem), sorted(rem) == sorted(REMOVED), len(add), ADDED_N, any('pgSafeStringSchema' in l for l in add)))
    for l in rem:
        if l not in REMOVED: print('INFO H1 unexpected removed line: %s' % l.strip()[:140])
    sv = X['head'][SV]; nine = array_after(sv, 'export const AVAILABLE_SCOPES'); nine = [re.sub(r'\s*//.*$', '', s) for s in (nine or [])]
    # AVAILABLE_SCOPES carries trailing comments per line: re-read item by item
    m = re.search(r'export const AVAILABLE_SCOPES = \[(.*?)\];', sv, re.S)
    nine = re.findall(r"'([^']+)'", m.group(1)) if m else []
    dflt = re.search(r"const scopes = params\.scopes \|\| \[([^\]]*)\]", sv); dflt = re.findall(r"'([^']+)'", dflt.group(1)) if dflt else None
    sl = [l for l in hl if re.match(r'\s*scopes:\s*z\.', l)]
    tn = array_after(h[K['test']], 'const NINE') or []
    C.chk('H2 vocabulary', sl == [SCOPES_LINE, SCOPES_LINE] and nine == K['available_scopes'] and dflt is not None and set(dflt) <= set(nine) and not set(dflt) & set(K['privileged_scopes']),
          'scopes lines in oauth.ts %d, both the closed enum: %s | services/oauth.ts AVAILABLE_SCOPES == kit nine: %s (%d) | createApp default %s within the nine, no privileged: %s' % (
              len(sl), sl == [SCOPES_LINE, SCOPES_LINE], nine == K['available_scopes'], len(nine), dflt, dflt is not None and set(dflt) <= set(nine) and not set(dflt) & set(K['privileged_scopes'])))
    print('INFO H2 the ks1210 test MOCKS AVAILABLE_SCOPES with NINE %s == the real nine: %s (nothing in the PR pins the mock to the source; ks855 pins the real list)' % (len(tn), tn == nine))
    o = {k: array_after(h[P], v) for k, v in K['oauth_ts_decls'].items()}; u = {k: array_after(h[US], v) for k, v in K['users_ts_decls'].items()}
    ok3 = o['privileged'] == K['privileged_scopes'] and set(o['privileged']) <= set(nine) and o['platform'] == u['platform'] == K['platform_roles'] and o['app_admin'] == u['app_admin'] == K['app_admin_roles']
    decls = [(i + 1, l.strip()) for i, l in enumerate(h[US].split('\n')) if re.search(r'\bconst ADMIN_ROLES\b', l)]
    print('INFO H3 users.ts carries %d `const ADMIN_ROLES` declarations %s; the drift cell (and this check) read the FIRST by indexOf — distinct lists: %d' % (
        len(decls), [d[0] for d in decls], len(set(d[1] for d in decls))))
    C.chk('H3 role lists', ok3, 'privileged %s | platform oauth %s users %s | app-admin oauth %s users %s | CHECKED 5 lists against the kit' % (o['privileged'], o['platform'], u['platform'], o['app_admin'], u['app_admin']))
    hs = handlers(h[P]); byid = [(r, b) for r, b in hs if re.search(r"'/apps/:id", r)]; gated = []
    for r, b in byid:
        v = b.find('appVisibleTo(req, req.params.id)'); s = SVC_CALL.search(b)
        tail = b[v:v + 400] if v >= 0 else ''
        g = v >= 0 and (s is None or v < s.start()) and ("status(404)" in tail or 'if (!app) return res.status(404)' in tail)
        gated.append((r.split(',')[0], g, b.count("tenant")))
    names = sorted(x[0] for x in gated); want = sorted(x.split(',')[0] for x in K['by_id_routes'])
    C.chk('H4 by-id gate (class hunt)', len(gated) == 4 and all(g for _, g, _ in gated) and names == want,
          'CHECKED %d by-id handler(s) (want 4) | gated before any service call, 404 on falsy: %s | the set == kit by_id_routes: %s' % (
              len(gated), [(n.replace('oauthRouter.', ''), g) for n, g, _ in gated], names == want))
    for n, g, t in gated: print('INFO H4 %s: tenant mentions in the handler body %d (0 = the cross-tenant bound is RLS + seedTenantGuc alone)' % (n.replace('oauthRouter.', ''), t))
    for r, b in hs:
        if (r, b) in byid: continue
        reads = [k for k in ('getAppByClientId', 'getAppById', 'updateApp', 'listApps', 'createApp', 'validateScopes', 'rotateSecret', 'appVisibleTo', 'authenticate(') if k + ('' if k.endswith('(') else '(') in b]
        print('INFO H4 other route %-60s reads %s' % (r.split(', async')[0][:60], reads or 'NONE'))
    pb = next((b for r, b in hs if r.startswith("oauthRouter.patch('/apps/:id'")), ''); cb = next((b for r, b in hs if r.startswith("oauthRouter.post('/apps',")), '')
    pv, pp = pb.find('appVisibleTo('), pb.find('privilegedScopesIn(')
    cp, cc = cb.find('privilegedScopesIn('), cb.find('createApp(')
    cgate = cb[cp:cc] if 0 <= cp < cc else ''
    C.chk('H5 order', 0 <= pv < pp and 0 <= cp < cc and 'isOauthPlatformAdmin(' in cgate and 'isOauthAppAdmin(' not in cgate and 'isOauthPlatformAdmin(' in pb[pp:pp + 300],
          'PATCH ownership-404 at +%d before privileged-403 at +%d: %s | POST privileged check at +%d before createApp at +%d: %s, on isOauthPlatformAdmin: %s (isOauthAppAdmin: %s)' % (
              pv, pp, 0 <= pv < pp, cp, cc, 0 <= cp < cc, 'isOauthPlatformAdmin(' in cgate, 'isOauthAppAdmin(' in cgate))
    av = fn_body(h[P], 'async function appVisibleTo('); ip = fn_body(h[P], 'function isOauthPlatformAdmin('); ia = fn_body(h[P], 'function isOauthAppAdmin(')
    ok6 = ('app.createdBy && app.createdBy === req.user?.userId' in av and 'isOauthAppAdmin(' in av and 'return null;' in av.split('isOauthAppAdmin(')[-1]
           and 'OAUTH_PLATFORM_ADMIN_ROLES' in ip and 'OAUTH_APP_ADMIN_ROLES' in ia)
    C.chk('H6 appVisibleTo', ok6,
          'owner test present: %s | admin bypass via isOauthAppAdmin: %s | else null: %s | isOauthPlatformAdmin reads the FOUR list: %s | isOauthAppAdmin reads the SIX list: %s' % (
              'app.createdBy && app.createdBy === req.user?.userId' in av, 'isOauthAppAdmin(' in av, 'return null;' in av.split('isOauthAppAdmin(')[-1], 'OAUTH_PLATFORM_ADMIN_ROLES' in ip, 'OAUTH_APP_ADMIN_ROLES' in ia))
    sib = {}
    for t in K['sibling_tests']:
        a, b = d[t], h[t]
        sib[t.split('/')[-1][:5]] = (len(re.findall(r'\bit\(', a)), len(re.findall(r'\bit\(', b)), norm_expects(a) == norm_expects(b), sum(norm_expects(a).values()), sum(norm_expects(b).values()))
    C.chk('H7 siblings fixture-only', all(v[0] == v[1] and v[2] for v in sib.values()), ' | '.join('%s it( %d->%d, normalised expect() multiset equal: %s (%d->%d)' % ((k,) + v) for k, v in sib.items()))
    lb = fn_body(X['head'][SV], 'export async function listApps(')
    print('INFO listApps: a falsy userId takes the unfiltered branch (%s) — every app, every tenant RLS admits' % ('SELECT * FROM oauth_apps ORDER BY' in lb))


def facts(head):
    paths = [P, SV, US, AU, K['test']] + K['sibling_tests']
    return {'dev': {p: show(REPO, DEV, p) or '' for p in paths}, 'head': {p: show(REPO, head, p) or '' for p in paths},
            'blob_dev': {p: blob(REPO, DEV, p) for p in (SV, US, AU)}, 'blob_head': {p: blob(REPO, head, p) for p in (SV, US, AU)}}


print('c2_hunk_gate60 %s | clone %s | develop %s | head %s' % (now(), REPO, DEV[:12], HEAD[:12]))
X = facts(HEAD)
if '--selftest' in A:
    import copy
    st = {'ok': 0, 'n': 0}

    def arm(path, old, new, count=1):
        X2 = copy.deepcopy(X); s = X2['head'][path]
        assert s.count(old) >= 1, 'plant anchor absent: %r' % old[:70]
        X2['head'][path] = s.replace(old, new, count)
        if path in (SV, US, AU): X2['blob_head'][path] = 'f' * 40
        landed = X2['head'][path] != X['head'][path]
        return lambda C: (C.chk('LANDED', landed, 'tamper landed'), judge(C, X2))
    rot = "    // KS-1210 gate 2: rotating another user's client secret is the sharpest of the\n    // four by-id routes — it would hand the caller working credentials.\n    if (!(await appVisibleTo(req, req.params.id))) {\n      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });\n    }\n    const newSecret"
    pat_a = "    if (!(await appVisibleTo(req, req.params.id))) {\n      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });\n    }\n    // KS-1210 gate 1: the same privileged-scope rule as the create path.\n    const privilegedUpdate = privilegedScopesIn(scopes);\n    if (privilegedUpdate.length > 0 && !isOauthPlatformAdmin(req.user?.role as string)) {\n      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: PRIVILEGE_REFUSED, details: { scopes: privilegedUpdate } } });\n    }\n"
    pat_b = "    // KS-1210 gate 1: the same privileged-scope rule as the create path.\n    const privilegedUpdate = privilegedScopesIn(scopes);\n    if (privilegedUpdate.length > 0 && !isOauthPlatformAdmin(req.user?.role as string)) {\n      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: PRIVILEGE_REFUSED, details: { scopes: privilegedUpdate } } });\n    }\n    if (!(await appVisibleTo(req, req.params.id))) {\n      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });\n    }\n"
    selftest_arm(st, 'T0 the REAL develop -> head (positive control)', lambda C: judge(C, X), None)
    selftest_arm(st, 'T1 rotate-secret ungated', arm(P, rot, '    const newSecret'), 'H4')
    selftest_arm(st, 'T2 PATCH order swapped (403 before the ownership 404)', arm(P, pat_a, pat_b), 'H5')
    selftest_arm(st, 'T3 the create gate on isOauthAppAdmin (the SIX list)', arm(P, "    if (privileged.length > 0 && !isOauthPlatformAdmin(", "    if (privileged.length > 0 && !isOauthAppAdmin("), 'H5')
    selftest_arm(st, 'T4 ORG_ADMIN added to the platform list', arm(P, "['SYSTEM_ADMIN', 'SUPER_ADMIN', 'admin', 'super_admin']", "['SYSTEM_ADMIN', 'SUPER_ADMIN', 'admin', 'super_admin', 'ORG_ADMIN']"), 'H3')
    selftest_arm(st, 'T5 the update schema reopened to any string', arm(P, SCOPES_LINE, '  scopes: z.array(z.string()).optional(),', -1), 'H2')
    selftest_arm(st, 'T6 services/oauth.ts edited (getAppById gains a predicate)', arm(SV, "'SELECT * FROM oauth_apps WHERE id = $1'", "'SELECT * FROM oauth_apps WHERE id = $1 AND is_active'"), 'H1')
    selftest_arm(st, 'T7 an expect() removed from ks451', arm(K['sibling_tests'][1], '    expect(r.success).toBe(true);\n  });\n});', '  });\n});'), 'H7')
    selftest_arm(st, 'T8 the owner test dropped from appVisibleTo', arm(P, '  if (app.createdBy && app.createdBy === req.user?.userId) return app;\n', ''), 'H6')
    Xd = copy.deepcopy(X); Xd['head'] = copy.deepcopy(X['dev']); Xd['blob_head'] = dict(X['blob_dev'])
    selftest_arm(st, 'T9 the REAL develop as the head (must-fail on real code: 0 of 4 gated)', lambda C: judge(C, Xd), 'H4')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)
C = Checks(); judge(C, X); n = C.nfail()
print('C2 HUNK %s: %d FAIL of %d checks | head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
