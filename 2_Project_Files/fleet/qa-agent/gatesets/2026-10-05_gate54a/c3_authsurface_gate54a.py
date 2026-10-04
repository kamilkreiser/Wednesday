#!/usr/bin/env python3
"""c3_authsurface_gate54a.py — gate54a C3 (STATIC half): the security review of the diff, read from git objects (READ ONLY, never executed).
The RUNTIME half is the probe `probe_ks1402_authsurface.test.ts.txt`, which the tester copies into ITS OWN head worktree (README section 3).
  S1 ADMISSION SURFACE: every route registration in every non-test .ts under Blockchain/Dev/services/*/src, at BASE and at HEAD, with the auth
     middleware it names. The routes that call authenticateAccessOrConnector(...) must be exactly kit connector_routes_base at base and
     kit connector_routes_head at head, all in routes/users.ts; 0 `.use(authenticateAccessOrConnector` (a wholesale mount). MUST-HIT CONTROLS:
     the same enumerator finds POST /stub admitting at BASE, and >= 10 users.ts routes guarded by plain authenticate().
  S2 THE OTHER DOOR IS UNCHANGED: the routes guarded by plain authenticate() are the same set base vs head except GET /lookup (moved, and
     only it); `export function authenticate(` body byte-equal base == head; jwt.ts blob-equal base == head (verifyAccessToken keeps its
     type:'access' invariant, verifyConnectorToken unchanged).
  S3 users.ts CODE DELTA: exactly ONE non-comment line removed and ONE added, both the /lookup registration, differing only in
     authenticate() -> authenticateAccessOrConnector(); every other changed line is a comment.
  S4 SHAPE + GATES KEPT: the /lookup handler body (after its registration line to its closing `});`) byte-equal base == head (so the HTTP
     response shape is unchanged), and it still carries the scope gate (hasUsersReadScope, ALLOWED_LOOKUP_ROLES, the 403), the cross-tenant 404
     (`user.tenantId !== callerTenantId`, USER_NOT_FOUND) and maskEmail(email); hasUsersReadScope / ALLOWED_LOOKUP_ROLES byte-equal.
  S5 LOG LABEL: authenticate.ts's code delta is exactly the logger.info label line + one added `route: req.baseUrl + req.path,`; the head
     file carries 0 `originalUrl` / `req.url` / `req.query`; MUST-HIT CONTROL: the same regex over services/*/src at HEAD finds >= 1.
  INFO (the gate rules, the drafter does not): the TENANTLESS doubt (ConnectorTokenClaims.tenantId is optional and the 404 guard is
     `callerTenantId && user.tenantId && ...`, so a connector token minted without a tenant skips it); stale comments; PR-body file:line claims.
--selftest: plants into copies of the real HEAD texts (never a repo write) — /me admits connectors, a router.use mount, the 404 made 200, the
     label from originalUrl, a scope gate removed, a second code line in users.ts — each must FAIL its named check; the real head must PASS.
--base-vs-base: analyse BASE as if it were the head (must FAIL S1: /lookup is not admitted).
Usage: c3_authsurface_gate54a.py --repo <clone> [--base sha] [--head sha] [--selftest | --base-vs-base]   (rc 0 PASS / 1 FAIL / 2 usage)"""
import os, re, subprocess, sys, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54a import K, git, now, Checks, has_commit

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head', K['expected_head'])
for s in (BASE, HEAD):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s): print('REFUSING: %s is not a 40-hex commit present in %s' % (s, REPO)); raise SystemExit(2)
TEST_RX = re.compile(r'(^|/)(__tests__|tests?|e2e|spec)/|\.(test|spec)\.[cm]?[jt]sx?$')
SR = K['services_root'] + '/'

def batch(sha, paths):
    """blob texts for sha:path via ONE `git cat-file --batch` (a read verb)"""
    if not paths: return {}
    r = subprocess.run(['git', '-C', REPO, 'cat-file', '--batch'], input=''.join('%s:%s\n' % (sha, p) for p in paths).encode(), capture_output=True)
    out = r.stdout; i = 0; res = {}
    for p in paths:
        j = out.index(b'\n', i); hdr = out[i:j].decode().split(); i = j + 1
        if len(hdr) < 3 or hdr[1] == 'missing': res[p] = None; continue
        n = int(hdr[2]); res[p] = out[i:i + n].decode('utf-8', 'replace'); i += n + 1
    return res

def src_files(sha):
    ls = git(REPO, 'ls-tree', '-r', '--name-only', sha, '--', K['services_root']).splitlines()
    return [p for p in ls if p.startswith(SR) and '/src/' in p and p.endswith('.ts') and not TEST_RX.search(p) and not p.endswith('.d.ts')]

REG = re.compile(r'''^\s*(\w+)\.(get|post|put|patch|delete|all|use)\(\s*(['"`])(.*?)\3\s*,(.*)$''')
USE_MW = re.compile(r'''^\s*(\w+)\.use\(\s*(authenticate\w*|optionalAuthenticate)\s*\(''')
MW = re.compile(r'\b(authenticateAccessOrConnector|authenticate|optionalAuthenticate|authenticateToken|requireRole|requireScope|attachScopes)\s*\(')

def routes(texts):
    """[(file, line, method, path, [middleware])] for every registration; + wholesale .use(mw) mounts"""
    out = []; mounts = []
    for f, t in texts.items():
        if t is None: continue
        L = t.split('\n')
        for i, l in enumerate(L):
            if l.strip().startswith('//') or l.strip().startswith('*'): continue
            m = REG.match(l)
            if m:
                rest = m.group(5)
                if rest.rstrip().endswith((',', '(')) and i + 1 < len(L): rest += ' ' + L[i + 1]
                out.append((f, i + 1, m.group(2).upper(), m.group(4), MW.findall(rest)))
            u = USE_MW.match(l)
            if u: mounts.append((f, i + 1, u.group(2)))
    return out, mounts

def func_body(text, sig):
    i = text.find(sig)
    if i < 0: return None
    j = text.index('{\n', i); d = 0   # the BODY brace (first `{` ending a line), never a `{ required: true }` default
    for k in range(j, len(text)):
        d += {'{': 1, '}': -1}.get(text[k], 0)
        if d == 0: return text[i:k + 1]
    return None

def handler(text, anchor):
    L = text.split('\n'); st = [i for i, l in enumerate(L) if anchor in l and not l.strip().startswith('//')]
    if len(st) != 1: return None, None
    for j in range(st[0] + 1, len(L)):
        if L[j].startswith('});'): return st[0] + 1, '\n'.join(L[st[0] + 1:j + 1])
    return st[0] + 1, None

def is_comment(l):
    s = l.strip(); return s == '' or s.startswith('//') or s.startswith('*') or s.startswith('/*') or s.startswith('*/')

def code_delta(a, b):
    sm = difflib.SequenceMatcher(None, a.split('\n'), b.split('\n'), autojunk=False); rm = []; ad = []; cm = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal': continue
        for l in a.split('\n')[i1:i2]:
            (cm := cm + 1) if is_comment(l) else rm.append(l)
        for l in b.split('\n')[j1:j2]:
            (cm := cm + 1) if is_comment(l) else ad.append(l)
    return rm, ad, cm

def analyse(BT, HT, label):
    """BT/HT: {path: text} at base / head (HT may carry plants). Returns Checks."""
    C = Checks(); U = K['users_routes']; MWF = K['authenticate_mw']; J = K['jwt_service']
    rb, mb = routes(BT); rh, mh = routes(HT)
    def conn(rs): return sorted('%s %s' % (m, p) for f, _, m, p, mw in rs if 'authenticateAccessOrConnector' in mw)
    def connf(rs): return sorted(set(f for f, _, m, p, mw in rs if 'authenticateAccessOrConnector' in mw))
    def plain(rs): return sorted('%s %s %s' % (f.split('/src/')[-1], m, p) for f, _, m, p, mw in rs if 'authenticate' in mw)
    cb, ch = conn(rb), conn(rh); wm = [x for x in mh if x[2] == 'authenticateAccessOrConnector']
    nusers_plain = len([1 for f, _, m, p, mw in rh if f == U and 'authenticate' in mw])
    C.chk('S1 admission surface', ch == sorted(K['connector_routes_head']) and connf(rh) in ([U], []) and connf(rh) == [U] and not wm and cb == sorted(K['connector_routes_base']) and nusers_plain >= 10,
          '[%s] connector-admitting routes: BASE %s | HEAD %s (want %s, all in users.ts: files %s) | wholesale .use(authenticateAccessOrConnector) %d | MUST-HIT: base admits %s (want %s), users.ts plain authenticate() routes at head %d (want >= 10) | %d registrations enumerated at head over %d files' % (
              label, cb, ch, K['connector_routes_head'], [f.split('/src/')[-1] for f in connf(rh)], len(wm), cb, K['connector_routes_base'], nusers_plain, len(rh), len(HT)))
    pb, ph = set(plain(rb)), set(plain(rh)); moved_out = sorted(pb - ph); moved_in = sorted(ph - pb)
    ab, ah = func_body(BT[MWF] or '', 'export function authenticate('), func_body(HT[MWF] or '', 'export function authenticate(')
    C.chk('S2 other door unchanged', moved_out == ['routes/users.ts GET /lookup'] and not moved_in and ab is not None and ab == ah and BT.get(J) == HT.get(J),
          'plain-authenticate() routes base %d / head %d; left the plain door %s (want only GET /lookup); joined %s | authenticate() body byte-equal %s (%s chars) | jwt.ts byte-equal %s' % (
              len(pb), len(ph), moved_out, moved_in or 'NONE', ab == ah and ab is not None, len(ah or ''), BT.get(J) == HT.get(J)))
    rm, ad, cm = code_delta(BT[U], HT[U])
    norm = lambda s: s.replace('authenticateAccessOrConnector()', 'authenticate()')
    ok3 = len(rm) == 1 and len(ad) == 1 and "'/lookup'" in rm[0] and "authenticate()" in rm[0] and 'authenticateAccessOrConnector()' in ad[0] and norm(ad[0]) == rm[0]
    C.chk('S3 users.ts code delta', ok3, 'non-comment lines removed %d %s | added %d %s | comment lines changed %d' % (len(rm), [x.strip()[:90] for x in rm], len(ad), [x.strip()[:90] for x in ad], cm))
    lb, hb = handler(BT[U], "userRoutes.get('/lookup'"), handler(HT[U], "userRoutes.get('/lookup'")
    body = hb[1] or ''
    need = ['hasUsersReadScope(callerScopes)', 'ALLOWED_LOOKUP_ROLES.includes(callerRole)', 'res.status(403)', 'res.status(404)', "'USER_NOT_FOUND'", 'user.tenantId !== callerTenantId', 'maskEmail(email)']
    miss = [n for n in need if n not in body]
    defs_eq = func_body(BT[U], 'function hasUsersReadScope(') == func_body(HT[U], 'function hasUsersReadScope(') and \
        [l for l in BT[U].split('\n') if l.startswith('const ALLOWED_LOOKUP_ROLES')] == [l for l in HT[U].split('\n') if l.startswith('const ALLOWED_LOOKUP_ROLES')]
    C.chk('S4 shape and gates kept', lb[1] is not None and lb[1] == hb[1] and not miss and defs_eq,
          '/lookup handler body (base :%s, head :%s, %d lines) byte-equal %s | gates present: %d of %d (missing %s) | hasUsersReadScope + ALLOWED_LOOKUP_ROLES byte-equal %s' % (
              lb[0], hb[0], body.count('\n') + 1, lb[1] == hb[1], len(need) - len(miss), len(need), miss or 'NONE', defs_eq))
    rm5, ad5, cm5 = code_delta(BT[MWF], HT[MWF])
    leak = re.compile(r'\b(originalUrl|req\.url\b|req\.query)')
    code = lambda t: '\n'.join(l for l in (t or '').split('\n') if not is_comment(l))   # comments may NAME originalUrl (the PR's own does)
    hl = len(leak.findall(code(HT[MWF]))); ctl = sum(len(leak.findall(code(t))) for f, t in HT.items() if f != MWF)
    lbl = [l.strip() for l in ad5]
    ok5 = len(rm5) == 1 and "logger.info('users/stub:" in rm5[0] and len(ad5) == 2 and any(l.startswith("logger.info('connector token accepted") for l in lbl) and 'route: req.baseUrl + req.path,' in lbl and hl == 0 and ctl >= 1
    C.chk('S5 log label', ok5, 'authenticate.ts non-comment removed %s | added %s | comment lines changed %d | originalUrl/req.url/req.query in authenticate.ts CODE lines at head: %d (want 0) | MUST-HIT the same regex over the other services/*/src CODE lines: %d (want >= 1)' % (
        [x.strip()[:80] for x in rm5], lbl, cm5, hl, ctl))
    return C

def load(sha):
    fs = src_files(sha); T = batch(sha, fs)
    for p in (K['users_routes'], K['authenticate_mw'], K['jwt_service']):
        if T.get(p) is None: raise SystemExit('REFUSING: %s absent at %s' % (p, sha[:12]))
    return T

print('c3_authsurface_gate54a %s | repo %s | base %s | head %s | mode %s' % (now(), REPO, BASE[:12], HEAD[:12], 'selftest' if '--selftest' in A else 'base-vs-base' if '--base-vs-base' in A else 'gate'))
BT = load(BASE)
if '--base-vs-base' in A:
    C = analyse(BT, dict(BT), 'BASE as head'); n = C.nfail()
    print('C3 STATIC %s (base-vs-base, a control: S1/S2/S3/S5 MUST fail): %d FAIL of %d' % ('PASS' if n == 0 else 'FAIL', n, len(C.res))); raise SystemExit(1 if n else 0)
HT = load(HEAD)
if '--selftest' in A:
    U = K['users_routes']; MWF = K['authenticate_mw']
    def plant(path, old, new, count=1):
        t = dict(HT); s = t[path]
        if s.count(old) < 1: raise SystemExit('SELFTEST REFUSING: plant anchor %r not in %s' % (old[:60], path))
        t[path] = s.replace(old, new, count); return t
    arms = [
        ('T0 real head', dict(HT), None),
        ('T1 /me admits connectors', plant(U, "userRoutes.get('/me', authenticate(), meHandler);", "userRoutes.get('/me', authenticateAccessOrConnector(), meHandler);"), 'S1'),
        ('T2 router.use mount', plant(U, 'export const userRoutes = Router();', 'export const userRoutes = Router();\nuserRoutes.use(authenticateAccessOrConnector());'), 'S1'),
        ('T3 cross-tenant 404 made 200', plant(U, "      return res.status(404).json({\n        success: false,\n        error: { code: 'USER_NOT_FOUND', message: 'No user with that email in this tenant' },", "      return res.status(200).json({\n        success: false,\n        error: { code: 'USER_NOT_FOUND', message: 'No user with that email in this tenant' },"), 'S4'),
        ('T4 label from originalUrl', plant(MWF, 'route: req.baseUrl + req.path,', 'route: req.originalUrl,'), 'S5'),
        ('T5 scope gate removed', plant(U, '    const allowedByScope = hasUsersReadScope(callerScopes);\n    if (!allowedByRole && !allowedByScope) {\n      logger.warn(\'users/lookup', '    const allowedByScope = true;\n    if (!allowedByRole && !allowedByScope) {\n      logger.warn(\'users/lookup'), 'S4'),
        ('T6 a second code line in users.ts', plant(U, 'const ALLOWED_LOOKUP_ROLES = [', "const ALLOWED_LOOKUP_ROLES = ['CONNECTOR', "), 'S3'),
        ('T7 authenticate() body touched', plant(MWF, "throw new UnauthorizedError('No token provided');", "throw new UnauthorizedError('No token');"), 'S2'),
    ]
    ok = 0
    for name, ht, want in arms:
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = analyse(BT, ht, name)
        f = C.failed(); good = (not f) if want is None else (any(x.startswith(want) for x in f))
        ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        for l in buf.getvalue().splitlines():
            if l.startswith('FAIL') or want is None: print('    ' + l[:330])
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); raise SystemExit(0 if ok == len(arms) else 1)
C = analyse(BT, HT, 'HEAD')
# ---- INFO: the doubts and the claims (never a FAIL here; the gate rules them) ----
J = HT[K['jwt_service']]; U = HT[K['users_routes']]; MWF = HT[K['authenticate_mw']]
m = re.search(r'export interface ConnectorTokenClaims \{(.*?)\n\}', J, re.S)
print('INFO D-TENANTLESS: ConnectorTokenClaims %s | generateConnectorToken spreads tenantId only when present: %s | the /lookup 404 guard reads %r — a connector token minted WITHOUT a tenant skips it. The probe arm P5 measures what /lookup answers then; the gate rules whether it blocks.' % (
    'tenantId OPTIONAL' if m and 'tenantId?:' in m.group(1) else 'tenantId ' + ('REQUIRED' if m else 'UNREAD'),
    '...(meta.tenantId ? { tenantId: meta.tenantId } : {})' in J,
    next((l.strip() for l in U.split('\n') if 'user.tenantId !== callerTenantId' in l and 'if (' in l), None)))
for i, l in enumerate(J.split('\n'), 1):
    if 'route (`POST /api/users/stub`)' in l or ('ONE' in l and 'route' in l and 'stub' in l): print('INFO STALE-COMMENT jwt.ts:%d (unchanged file) still reads %r' % (i, l.strip()[:120]))
TF = batch(HEAD, [K['test_file']])[K['test_file']] or ''
for i, l in enumerate(TF.split('\n'), 1):
    if 'authenticate.ts:105' in l: print('INFO STALE-CITE test:%d cites %r; runWithTenantId(connector.tenantId) is at authenticate.ts:%s at head' % (i, l.strip()[:100], [n for n, x in enumerate(MWF.split('\n'), 1) if 'runWithTenantId(connector.tenantId' in x]))
CL = [('users.ts:266', U, 266, "userRoutes.get('/lookup', authenticateAccessOrConnector()"), ('users.ts:180', U, 180, 'const ALLOWED_LOOKUP_ROLES'),
      ('users.ts:223', U, 223, 'function hasUsersReadScope'), ('users.ts:310', U, 310, 'queriedEmail: maskEmail(email)'),
      ('authenticate.ts:69', MWF, 69, 'for TWO routes'), ('authenticate.ts:107', MWF, 107, "logger.info('connector token accepted")]
BU = BT[K['users_routes']]; BM = BT[K['authenticate_mw']]
for name, t, ln, want in CL:
    got = t.split('\n')[ln - 1] if ln <= t.count('\n') + 1 else ''
    near = [n for n, x in enumerate(t.split('\n'), 1) if want in x]
    bt = BM if t is MWF else BU; bl = bt.split('\n')[ln - 1] if ln <= bt.count('\n') + 1 else ''
    print('INFO CLAIM %s: %s | the head line reads %r | the BASE line %d reads %r' % (name, 'AT THE LINE' if want in got else 'NOT AT THE HEAD LINE (found at head :%s)' % near, got.strip()[:90], ln, bl.strip()[:70]))
GW = 'Blockchain/Dev/services/api-gateway/src/routes/proxy.ts'; OD = 'Blockchain/Dev/services/originate/src/routes/documents.ts'
X = batch(HEAD, [GW, OD])
for name, path, a, b, wants in (('proxy.ts:461-466', GW, 461, 466, ['/api/users/lookup', "requireScope('users:read')"]), ('documents.ts:1667-1671', OD, 1667, 1671, ['/api/users/lookup', 'uthorization'])):
    t = X.get(path) or ''; seg = '\n'.join(t.split('\n')[a - 1:b])
    print('INFO CLAIM %s: %s of %s present in the cited lines %s' % (name, sum(w in seg for w in wants), len(wants), [w for w in wants if w not in seg] or 'all'))
n = C.nfail()
print('C3 STATIC %s: %d FAIL of %d checks | base %s | head %s (the runtime half is the probe; the doubts above are the gate\'s)' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), BASE[:12], HEAD[:12]))
raise SystemExit(1 if n else 0)
