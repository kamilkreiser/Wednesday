#!/usr/bin/env python3
"""guards_sim.py — Wednesday's drafting re-derivation over the HEAD bytes of #982 (e62eab87a) and the develop bytes (M18 8861e6216),
read with `git show` into model/. Nothing here runs the suite; it asserts the SHAPE of the delta and the anchors the brief's tamper
table is built on, and it re-runs the ks860 loopback guard's :433/:440 regexes over the new test file (the widened-guard rule).
Exit 0 = every assertion holds · 1 = at least one failed. Usage: guards_sim.py <gate dir>"""
import re, sys, os, hashlib
G = sys.argv[1]
H = 'e62eab87a6263e25c41c9bb814d5831842bb6c7e'; D = '8861e62161466c40f08d2b10a30edeb203123993'
def rd(p): return open(p, encoding='utf-8').read()
oh = rd(f'{G}/model/oauth.ts.{H}'); od = rd(f'{G}/model/oauth.ts.{D}')
t790 = rd(f'{G}/model/ks790.test.ts.{H}')
k8h = rd(f'{G}/model/ks820.test.ts.{H}'); k8d = rd(f'{G}/model/ks820.test.ts.{D}')
ur = rd(f'{G}/model/userRepo.ts.{H}'); jw = rd(f'{G}/model/jwt.ts.{H}')
patch = rd(f'{G}/model/diff_oauth_ks820.patch')
fails = 0
def ck(cond, msg):
    global fails
    print(('ok   ' if cond else 'FAIL ') + msg); fails += 0 if cond else 1
def sha16(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]

print('== blobs / sizes')
ck(sha16(oh) == 'fc54cc5f1494ad48' and oh.count('\n') == 1260, f'oauth.ts@head sha256 {sha16(oh)} lines {oh.count(chr(10))} (expect fc54cc5f1494ad48 / 1260)')
ck(sha16(od) == 'cc4f4ac0df1b3393' and od.count('\n') == 1242, f'oauth.ts@develop sha256 {sha16(od)} lines {od.count(chr(10))} (expect cc4f4ac0df1b3393 / 1242)')
ck(sha16(t790) == '55c12270001fd653' and t790.count('\n') == 249, f'ks790 test sha256 {sha16(t790)} lines {t790.count(chr(10))} (expect 55c12270001fd653 / 249)')
ck(sha16(k8h) == 'd0883d41f8a38b96' and k8h.count('\n') == 377, f'ks820 test@head sha256 {sha16(k8h)} lines {k8h.count(chr(10))} (expect d0883d41f8a38b96 / 377)')
ck(sha16(k8d) == '4f66d57fd174c85b' and k8d.count('\n') == 369, f'ks820 test@develop sha256 {sha16(k8d)} lines {k8d.count(chr(10))} (expect 4f66d57fd174c85b / 369)')
for s, n in [(oh, 'oauth@head'), (od, 'oauth@develop'), (t790, 'ks790'), (k8h, 'ks820@head'), (k8d, 'ks820@develop')]:
    b = s.encode('utf-8'); ctrl = sum(1 for x in b if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)
    ck(ctrl == 0, f'{n}: 0 raw control bytes (got {ctrl})')

print('== the oauth.ts delta: 4 hunks; the CODE delta is -4/+3 (import, two swaps, the require removed with no code replacement)')
hunks = re.findall(r'^@@ [^@]* @@', patch, re.M)
ck(hunks == ['@@ -122,6 +122,14 @@', '@@ -26,7 +26,7 @@', '@@ -795,8 +795,17 @@', '@@ -829,7 +838,14 @@', '@@ -846,7 +862,9 @@'], f'hunk headers (ks820 first, then oauth.ts x4): {hunks}')
op = patch[patch.index('diff --git a/Blockchain/Dev/services/auth/src/routes/oauth.ts'):]
minus = [l[1:] for l in op.splitlines() if l.startswith('-') and not l.startswith('---')]
plus = [l[1:] for l in op.splitlines() if l.startswith('+') and not l.startswith('+++')]
ck(len(minus) == 5 and len(plus) == 23, f'oauth.ts -{len(minus)} +{len(plus)} (expect -5 +23)')
code_minus = [l for l in minus if not l.strip().startswith('//')]; code_plus = [l for l in plus if not l.strip().startswith('//')]
ck([l.strip() for l in code_minus] == ["import { generateTokenPair } from '../services/jwt';", 'const user = await userRepo.getUserById(result.userId);', "const { verifyRefreshToken } = require('../services/jwt');", 'const user = await userRepo.getUserById(decoded.userId);'], f'CODE lines removed ({len(code_minus)}): {[l.strip() for l in code_minus]}')
ck([l.strip() for l in code_plus] == ["import { generateTokenPair, verifyRefreshToken } from '../services/jwt';", 'const user = await userRepo.getUserByIdPreAuth(result.userId);', 'const user = await userRepo.getUserByIdPreAuth(decoded.userId);'], f'CODE lines added ({len(code_plus)}): {[l.strip() for l in code_plus]}')
ck(all(l.strip().startswith('//') for l in plus if l not in code_plus) and sum(1 for l in plus if l.strip().startswith('//')) == 20, f'the other {len(plus) - len(code_plus)} added lines are comments (20 expected)')
print('== the ks820 delta: ONE hunk, 8 lines INSERTED after develop:124, everything else byte-identical (ruling 1)')
kd = k8d.split('\n'); kh = k8h.split('\n')
ck(kh[:124] == kd[:124] and kh[132:] == kd[124:], 'ks820@head == develop[:124] + 8 lines + develop[124:]')
ins = kh[124:132]
ck(ins[0].strip().startswith('// KS-790') and ins[4].strip() == 'getUserByIdPreAuth: vi.fn(async () => ({' and ins[7].strip() == '})),', f'the 8 inserted lines are the one mock entry (+4 comment lines): {[l.strip()[:60] for l in ins]}')
ck(k8d.count('getUserByIdPreAuth') == 0 and k8h.count('getUserByIdPreAuth') == 1, f'getUserByIdPreAuth in ks820: develop {k8d.count("getUserByIdPreAuth")} head {k8h.count("getUserByIdPreAuth")}')
ck(re.findall(r"^\s*it\('", k8h, re.M).__len__() == 13 and re.findall(r"^\s*it\('", k8d, re.M).__len__() == 13, 'ks820 has 13 it( cells at both trees (no assertion added or removed)')

print('== anchors at head (the tamper table)')
A = [("userRepo.getUserByIdPreAuth(result.userId)", 1), ("userRepo.getUserByIdPreAuth(decoded.userId)", 1), ("userRepo.getUserById(", 0),
     ("import { generateTokenPair, verifyRefreshToken } from '../services/jwt';", 1), ("const { verifyRefreshToken } = require(", 0), ("require('../services/jwt')", 1),
     ("decoded = verifyRefreshToken(refresh_token);", 1), ("if (!user || user.status !== 'ACTIVE')", 1), ("description: 'User not found'", 1),
     ("description: 'User inactive or not found'", 1), ("description: 'Invalid refresh token'", 1), ("enforcePasswordLoginGates({", 1), ("oauthRouter.post('/token'", 1),
     ("      let decoded;\n      try {\n        decoded = verifyRefreshToken(refresh_token);", 1), ("KS-790", 3), ("getUserByIdPreAuth", 2)]
for tok, n in A: ck(oh.count(tok) == n, f'oauth@head  x{oh.count(tok)} (expect {n})  {tok[:80]!r}')
lines = oh.split('\n')
for ln, want in [(29, "import { generateTokenPair, verifyRefreshToken } from '../services/jwt';"), (808, '      const user = await userRepo.getUserByIdPreAuth(result.userId);'), (809, '      if (!user) {'),
                 (849, '      let decoded;'), (851, '        decoded = verifyRefreshToken(refresh_token);'), (867, '      const user = await userRepo.getUserByIdPreAuth(decoded.userId);'),
                 (868, "      if (!user || user.status !== 'ACTIVE') {"), (711, "oauthRouter.post('/token', async (req: Request, res: Response) => {"), (628, '    const gate = await enforcePasswordLoginGates({'),
                 (890, "    logger.error('OAuth token error', { error: error.message });"), (843, "      // used to be a `require('../services/jwt')` on this line — redundant with")]:
    ck(lines[ln - 1] == want, f'oauth@head:{ln} = {want.strip()[:70]!r}')
ck(lines[842].strip().startswith('//'), 'the only require( at head (:843) is INSIDE a comment')
B = [("userRepo.getUserById(result.userId)", 1), ("userRepo.getUserById(decoded.userId)", 1), ("const { verifyRefreshToken } = require('../services/jwt');", 1),
     ("import { generateTokenPair } from '../services/jwt';", 1), ("getUserByIdPreAuth", 0), ("KS-790", 0), ("enforcePasswordLoginGates({", 1)]
for tok, n in B: ck(od.count(tok) == n, f'oauth@develop x{od.count(tok)} (expect {n})  {tok[:80]!r}')
dl = od.split('\n')
for ln, want in [(799, '      const user = await userRepo.getUserById(result.userId);'), (832, "      const { verifyRefreshToken } = require('../services/jwt');"), (849, '      const user = await userRepo.getUserById(decoded.userId);'), (833, '      let decoded;')]:
    ck(dl[ln - 1] == want, f'oauth@develop:{ln} = {want.strip()[:70]!r}')
ck(dl[831].strip().startswith('const {') and dl[832].strip() == 'let decoded;' and dl[833].strip() == 'try {', 'at develop the require sits OUTSIDE the try (:832 require, :833 let decoded, :834 try) — its throw reaches the OUTER catch (500)')
T = [("app.listen(0, '127.0.0.1')", 1), ("listen(", 1), ("vi.mock('../services/jwt'", 1), ("vi.mock('../repositories/userRepo'", 1), ("getUserByIdPreAuth: vi.fn(", 1),
     ("world.plainLookup = null; world.preAuthLookup = { ...ACTIVE_USER };", 1), ("expect(world.calls.getUserById).toEqual([]);", 3), ("expect(world.calls.getUserByIdPreAuth).toEqual([ACTIVE_USER.id]);", 2),
     ("  it('", 6), ("  it('CONTROL", 4), ("status: 'SUSPENDED'", 1), ("'not-the-secret'", 1), ("toMatch(/User not found/)", 1), ("toMatch(/User inactive or not found/)", 2), ("net.connect(", 1),
     ("toContain('MINTED_790')", 2), ("verifyClientSecret: vi.fn(", 1), ("vi.mock('../middleware/tenantGuc'", 1), ("vi.mock('../db'", 1), ("expect(r.status).toBe(401);", 1)]
for tok, n in T: ck(t790.count(tok) == n, f'ks790 test x{t790.count(tok)} (expect {n})  {tok[:80]!r}')
tl = t790.split('\n')
ck(tl[137] == "  server = app.listen(0, '127.0.0.1');", f'ks790:138 = {tl[137].strip()!r}')
U = [("export async function getUserByIdPreAuth(id: string): Promise<User | null> {", 1), ("FROM auth_find_user_by_id($1)", 2), ("export async function getUserById(id: string, tenantId?: string): Promise<User | null> {", 1)]
for tok, n in U: ck(ur.count(tok) == n, f'userRepo@head x{ur.count(tok)} (expect {n})  {tok[:80]!r}')
ul = ur.split('\n')
ck(ul[504].startswith('export async function getUserByIdPreAuth(') and ul[402].startswith('export async function getUserById('), 'userRepo :505 getUserByIdPreAuth / :403 getUserById')
ck(jw.count("export function verifyRefreshToken(token: string): JwtPayload {") == 1 and jw.split('\n')[345].startswith('export function verifyRefreshToken('), 'jwt.ts:346 exports verifyRefreshToken (the static import resolves)')

print('== the ks860 loopback guard (:433 / :440 at M18 e0dfadb9c) over the NEW test file — the widened-guard rule')
SITE = re.compile(r"\.listen\(\s*0\s*(,|\))"); HOST = re.compile(r"^\s*(['\"])127\.0\.0\.1\1")
def offenders(src):
    out = []
    for m in SITE.finditer(src):
        rest = src[m.end():]
        if not (m.group(1) == ',' and HOST.match(rest)): out.append(src[:m.start()].count('\n') + 1)
    return out
ck(offenders(t790) == [], f'ks860 over ks790 test -> offenders {offenders(t790)} (expect [] — the one listen( at :138 binds 127.0.0.1)')
ck(offenders("server = app.listen(0);") == [1] and offenders("server = app.listen(0, '127.0.0.1');") == [], 'guard controls: bare listen(0) -> 1 offender; the shipped spelling -> 0')
ck(offenders(oh) == [] and offenders(od) == [], 'oauth.ts has no listen( site at either tree (not a test file anyway)')

print('== predictions the brief carries (drafter) — derived from the bytes above, NOT from a run')
print("  T1  :808 getUserByIdPreAuth -> getUserById   => ks790 cell 1 red (400 'User not found'); 5 green; 1 failed | 5 passed (6)")
print("  T2  :867 getUserByIdPreAuth -> getUserById   => ks790 cell 2 red (400 'User inactive or not found'); 1 failed | 5 passed (6)")
print("  T3d develop's require re-inserted at :849 BEFORE `let decoded;` (outside the try) => 3 refresh rows red, ALL 500 server_error; 3 failed | 3 passed (6)")
print("  T3b the require inserted INSIDE the try (before :851)                        => 3 refresh rows red, ALL 400 'Invalid refresh token' (the builder's T3 shape); 3 failed | 3 passed (6)")
print("  T4  :868 `!user || user.status !== 'ACTIVE'` -> `!user`                     => ks790 cell 5 red (200 with MINTED_790 for a SUSPENDED user); 1 failed | 5 passed (6)")
print("  T5  ks820 mock entry removed (the 8 inserted lines)                          => ks820 :246 / :320 / :328 red (500: getUserByIdPreAuth is not a function); 3 failed | 10 passed (13); ks790 6/6 untouched")
print("  T6  :809 `if (!user)` -> `if (false)`                                        => ks790 cell 3 red (500 server_error: the mocked createSession/generateTokenPair do not throw over null, but :820 reads `user.id` -> TypeError -> the outer catch); 1 failed | 5 passed (6)")
print("  T7  ks790 test :197 world inverted (plainLookup = the user, preAuthLookup = null) => cells 1,2 red (400 'User not found' / 'User inactive or not found' — the product asks the carve-out, which now answers null); cells 3,4,5,6 green (they set preAuthLookup themselves or never reach a lookup) -> 2 failed | 4 passed (6): the harness measures the carve-out, not the plain lookup — a harness self-check, optional")
print(f'guards_sim: FAILS={fails}')
sys.exit(1 if fails else 0)
