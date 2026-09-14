#!/bin/bash
# controls_check.sh — every :N anchor, blob, size, line count and token count the AUTH4 brief cites, checked against
# the GitHub contents API (blobs at the four heads + develop M20 + the live develop) AND git at the checkout (read verbs).
# Usage: bash controls_check.sh [--neg-head-987-as-986] [--neg-token] [--neg-dev-as-M18]
#   --neg-head-987-as-986  : the #987 head passed where #986's is expected (must FAIL on blobs/anchors)
#   --neg-token            : a token demanded PRESENT that is known ABSENT + one demanded ABSENT that is present (must FAIL 2)
#   --neg-dev-as-M18       : develop pinned at M18 (must FAIL: oauth.ts blob / ks790 ABSENT)
# Prints ok/FAIL lines and a tally; rc 1 if FAILS>0. No secrets printed (GH_TOKEN by name from the Secuura .env).
set -u
O='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateAUTH4'
ARGS="${1:-}"
python3 - "$ARGS" <<'PY'
import sys, json, urllib.request, base64, hashlib, subprocess, datetime
arg = sys.argv[1]
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
R = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def git(*a):
    return subprocess.run(['git', '-C', R] + list(a), capture_output=True, text=True).stdout
H983 = '5b0f4dd583c745e5606c9dbd580fa31f90191c6c'; H984 = '9b020ff827be9c83fbf5e9d62d47bc020a44519d'
H986 = 'ac1c119b56888bc064a820f9b191c409c520df64'; H987 = 'b6ed60f3b1bfe2f72ada658242b0995d0bef7424'
M18 = '8861e62161466c40f08d2b10a30edeb203123993'; M19 = '6e78961e1d04277ecbdb0537e630afa0bf63b13c'; M20 = 'a5334350221c819f54d4a20a3308daeb9ca09617'
if arg == '--neg-head-987-as-986': H986 = H987
DEV = M18 if arg == '--neg-dev-as-M18' else M20
A = 'Blockchain/Dev/services/auth/src/'; G = 'Blockchain/Dev/services/api-gateway/src/'; S = 'Blockchain/Dev/packages/shared/src/'
ok = fail = 0
def chk(cond, msg):
    global ok, fail
    if cond: ok += 1; print('ok   ' + msg)
    else: fail += 1; print('FAIL ' + msg)
print('controls_check', arg or '(positive)', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
live = get('/branches/develop')['commit']['sha']; print('live develop =', live)
cache = {}
def blob(ref, path):
    k = (ref, path)
    if k not in cache:
        try:
            j = get('/contents/' + path + '?ref=' + ref)
            cache[k] = (j['sha'], j['size'], base64.b64decode(j['content']).decode('utf-8') if j.get('encoding') == 'base64' else None)
        except urllib.error.HTTPError as e:
            cache[k] = (None, None, None) if e.code == 404 else (('ERR', e.code, None))
    return cache[k]
# --- blobs at the four heads + develop (the brief's TARGET / scope tables) ---
EXPECT = {
  (H983, A+'routes/oauth.ts'): ('de00ffceaccd8155349e8de10aaeab3a94c33529', 67227), (H983, A+'services/jwt.ts'): ('62b6db272c911557d764ee2f0e77f1df26923426', 15066),
  (H983, A+'__tests__/ks790-token-pre-auth-user-lookup.test.ts'): ('f98e8c80695bfe454fc35dcb168106a24c240a35', 12822), (H983, A+'__tests__/ks823-refresh-grant-client-auth-and-binding.test.ts'): ('2c0135b6fdf3f18a80d7d3f8f9569b404cf105be', 15463),
  (H983, A+'routes/auth.ts'): ('132d3b8d39b4fc6bb7cd4140a6f9e814826e7cd6', 61456),
  (H984, A+'routes/oauth.ts'): ('0bab1b8bdd7c9cb2b085bf94d5487a308eb51dd0', 67687), (H984, A+'services/jwt.ts'): ('26562a22470af688ae733000792a2b0321650145', 15955),
  (H984, G+'middleware/scopes.ts'): ('7aef335b93acf7a94fbcadc61c353d7a5dde90c5', 8138), (H984, A+'__tests__/ks823-refresh-grant-client-auth-and-binding.test.ts'): ('db9744c97f74411cb46e45935be533639dadf945', 15731),
  (H984, A+'__tests__/ks835-oauth-mint-carries-granted-scope.test.ts'): ('f61388142ed4881dc41fcd015e1b809af53d538f', 11369), (H984, G+'__tests__/ks835-oauth-token-scope-gate.test.ts'): ('548e1ec1217ef627aeea06da43a9a8c284161b86', 7109),
  (H984, A+'routes/auth.ts'): ('132d3b8d39b4fc6bb7cd4140a6f9e814826e7cd6', 61456),
  (H986, A+'routes/auth.ts'): ('18946cd7c5c394d89ecbecf860ab66a96b1e22c7', 62586), (H986, A+'__tests__/ks1151-auth-refresh-refuses-oauth-token.test.ts'): ('5a7ed0bf45012daa0d20a85a716208829ef71936', 13359),
  (H986, A+'routes/oauth.ts'): ('0bab1b8bdd7c9cb2b085bf94d5487a308eb51dd0', 67687), (H986, A+'services/jwt.ts'): ('26562a22470af688ae733000792a2b0321650145', 15955),
  (H986, A+'services/session.ts'): ('16848a3190c3918c04cb3940517dcaa4b78cc61d', 13698), (H986, A+'services/refreshDenylist.ts'): ('9851b8cea30169d5d84a285c8c0423a06fee8f83', 2592),
  (H986, A+'__tests__/auth.integration.test.ts'): ('aa4b88f203d8f652d11c6f0ed9994191c8ffd5e7', 61424),
  (H987, A+'routes/oauth.ts'): ('7bfdcc2adbeed8056a32ddb80466e50fc33545cf', 68049), (H987, A+'__tests__/ks790-token-pre-auth-user-lookup.test.ts'): ('33e9d51ad2db63aadb83cdf711048254ca058365', 13001),
  (H987, A+'__tests__/ks1150-code-grant-status-pin.test.ts'): ('39175521b4415092d7a281c9bdf4597fc146783b', 11140), (H987, A+'routes/auth.ts'): ('132d3b8d39b4fc6bb7cd4140a6f9e814826e7cd6', 61456),
  (DEV, A+'routes/auth.ts'): ('132d3b8d39b4fc6bb7cd4140a6f9e814826e7cd6', 61456), (DEV, A+'routes/oauth.ts'): ('80e05458e9759fbc6c7f33bc8cd90060d30e6149', 62763),
  (DEV, A+'services/jwt.ts'): ('d0d55c11beab2bfd8f8140e12de4016cac742134', 13692), (DEV, S+'__tests__/ks860-test-listeners-bind-loopback.test.ts'): ('e0dfadb9cd78d5c648dd263d5df320df8f26b909', 35744),
  (DEV, S+'security/scopes.ts'): ('c6040ca14b831ca5814978077805493f470d1492', None), (DEV, 'Blockchain/Dev/scripts/audit/audit-baseline.json'): ('03d1680e3c7a87f8df70e71082b67775536acde5', 44616),
  (DEV, A+'__tests__/ks790-token-pre-auth-user-lookup.test.ts'): ('cfed82d544158ccd5393d8ad4d2f9bed5681039a', 12429),
}
for (ref, path), (sha, size) in EXPECT.items():
    b = blob(ref, path)
    chk(b[0] == sha and (size is None or b[1] == size), f'{ref[:9]} {path.split("/")[-1]} blob {str(b[0])[:9]} size {b[1]} (expect {sha[:9]} {size})')
ABSENT = [(DEV, A+'__tests__/ks823-refresh-grant-client-auth-and-binding.test.ts'), (DEV, A+'__tests__/ks1151-auth-refresh-refuses-oauth-token.test.ts'), (DEV, A+'__tests__/ks1150-code-grant-status-pin.test.ts'),
          (H986, A+'__tests__/ks1150-code-grant-status-pin.test.ts'), (H987, A+'__tests__/ks1151-auth-refresh-refuses-oauth-token.test.ts'), (H983, A+'__tests__/ks835-oauth-mint-carries-granted-scope.test.ts')]
for ref, path in ABSENT:
    chk(blob(ref, path)[0] is None, f'{ref[:9]} {path.split("/")[-1]} ABSENT')
# --- line anchors + token counts on the API-fetched bytes (the brief's :N) ---
def lines(ref, path): return (blob(ref, path)[2] or '').split('\n')   # an ABSENT blob reads as no lines (a FAIL, not a crash)
def at(ref, path, n, needle):
    L = lines(ref, path); return n <= len(L) and needle in L[n-1]
def cnt(ref, path, needle): return (blob(ref, path)[2] or '').count(needle)
a986 = lines(H986, A+'routes/auth.ts')
chk(at(H986, A+'routes/auth.ts', 658, "authRoutes.post('/refresh'"), 'auth.ts:658 the refresh route (H986)')
chk(at(H986, A+'routes/auth.ts', 665, 'const payload = verifyRefreshToken(refreshTokenValue);'), 'auth.ts:665 verifyRefreshToken')
chk(at(H986, A+'routes/auth.ts', 677, "if (payload.client_id !== undefined || payload.authMethod === 'oauth') {"), 'auth.ts:677 THE GUARD')
chk(at(H986, A+'routes/auth.ts', 678, "logger.warn('Refresh refused: OAuth-minted token"), 'auth.ts:678 logger.warn')
chk(at(H986, A+'routes/auth.ts', 686, 'const session = await getSession(payload.sessionId);'), 'auth.ts:686 getSession AFTER the guard')
chk(at(H986, A+'routes/auth.ts', 693, 'if (payload.jti && (await isRefreshJtiDenylisted(payload.jti))) {'), 'auth.ts:693 replay check')
chk(at(H986, A+'routes/auth.ts', 707, "if (!user || user.status !== 'ACTIVE') throw new InvalidCredentialsError();"), 'auth.ts:707 ACTIVE pin at the interactive refresh')
chk(at(H986, A+'routes/auth.ts', 709, 'const tokens = generateTokenPair(user, session.id);'), 'auth.ts:709 the two-argument mint')
chk(at(H986, A+'routes/auth.ts', 715, 'await rotateSessionRefreshToken(session.id, tokens.refreshToken);'), 'auth.ts:715 rotate')
chk(at(H986, A+'routes/auth.ts', 718, 'await denylistRefreshJti(payload.jti, remaining);'), 'auth.ts:718 denylist')
chk(cnt(H986, A+'routes/auth.ts', "if (payload.client_id !== undefined || payload.authMethod === 'oauth') {") == 1, 'guard anchor count 1 at H986')
chk(cnt(H984, A+'routes/auth.ts', "payload.client_id !== undefined") == 0, 'guard ABSENT at the parent H984 (count 0; control above = 1)')
chk(cnt(H986, A+'routes/auth.ts', 'generateTokenPair(') == 6 and cnt(H986, A+'routes/wallet.ts' if False else A+'routes/auth.ts', 'generateTokenPair(') == 6, 'auth.ts generateTokenPair( = 6 (5 calls + 1 comment)')
chk(cnt(H986, A+'routes/oauth.ts', 'generateTokenPair(') == 2, 'oauth.ts generateTokenPair( = 2 (both WITH options)')
chk(cnt(H986, A+'routes/oauth.ts', 'generateTokenPair(user, session.id, {') == 2, 'oauth.ts both mints pass a third argument')
chk(cnt(H986, A+'routes/auth.ts', 'generateTokenPair(user, session.id, {') == 0, 'auth.ts NO mint passes a third argument (count 0; control oauth.ts = 2)')
chk(cnt(H986, A+'routes/oauth.ts', 'denylistRefreshJti(') == 0 and cnt(H986, A+'routes/auth.ts', 'denylistRefreshJti(') == 2, 'R-2: denylistRefreshJti( oauth.ts 0 / auth.ts 2')
chk(cnt(H986, A+'routes/oauth.ts', 'isRefreshJtiDenylisted(') == 1, 'oauth.ts isRefreshJtiDenylisted( = 1')
j = lines(H986, A+'services/jwt.ts')
chk(at(H986, A+'services/jwt.ts', 205, "authMethod: 'oauth' as const"), 'jwt.ts:205 the access-half label spread')
chk(at(H986, A+'services/jwt.ts', 229, "authMethod: 'oauth' as const"), 'jwt.ts:229 the refresh-half label spread')
chk(at(H986, A+'services/jwt.ts', 206, 'client_id: oauth.clientId') and at(H986, A+'services/jwt.ts', 230, 'client_id: oauth.clientId'), 'jwt.ts:206/:230 client_id spreads')
chk(at(H986, A+'services/jwt.ts', 378, 'export function verifyRefreshToken(token: string): OAuthTokenClaims {'), 'jwt.ts:378 verifyRefreshToken')
chk(at(H986, A+'services/jwt.ts', 44, "JWT_REFRESH_EXPIRES_IN || '7d'"), "jwt.ts:44 refresh default '7d'")
chk(cnt(H986, A+'services/jwt.ts', 'user.authMethod') == 0, 'jwt.ts never copies user.authMethod (count 0; control: authMethod count = %d)' % cnt(H986, A+'services/jwt.ts', 'authMethod'))
chk(cnt(H986, A+'services/jwt.ts', 'authMethod') == 5, 'jwt.ts authMethod = 5')
chk(at(H986, A+'types/index.ts', 204, "authMethod?: 'email' | 'wallet' | 'federated' | 'social';"), 'types/index.ts:204 the USER field')
chk(at(H986, A+'types/index.ts', 109, "USER_STATUSES = ['PENDING', 'ACTIVE', 'SUSPENDED', 'DEACTIVATED', 'INVITED']"), 'types/index.ts:109 USER_STATUSES')
chk(at(H986, A+'middleware/errorHandler.ts', 84, 'export class InvalidCredentialsError extends UnauthorizedError') and at(H986, A+'middleware/errorHandler.ts', 38, "super(message, 401, 'UNAUTHORIZED')"), 'errorHandler.ts:84/:38 -> 401')
t = blob(H986, A+'__tests__/ks1151-auth-refresh-refuses-oauth-token.test.ts')[2] or ''
chk(t.count('expect(') == 30 and t.count('expect(world.sessionLookups') == 0 and 'sessionLookups: [] as string[]' in t.split('\n')[63], 'ks1151 test: 30 expect( / 0 on sessionLookups / :64 records it (T5 basis)')
chk(sum(1 for l in t.split('\n') if l.lstrip().startswith("it('")) == 5 and "app.listen(0, '127.0.0.1')" in t.split('\n')[121], 'ks1151 test: 5 cells, :122 loopback listener (it( count %d)' % t.count("it('"))
o987 = lines(H987, A+'routes/oauth.ts'); o984 = lines(H984, A+'routes/oauth.ts')
chk(at(H987, A+'routes/oauth.ts', 837, "if (!user || user.status !== 'ACTIVE') {") and at(H987, A+'routes/oauth.ts', 947, "if (!user || user.status !== 'ACTIVE') {"), 'oauth.ts:837 + :947 the pin and its twin (H987)')
chk(cnt(H987, A+'routes/oauth.ts', "if (!user || user.status !== 'ACTIVE') {") == 2 and cnt(H984, A+'routes/oauth.ts', "if (!user || user.status !== 'ACTIVE') {") == 1, 'bare guard count 2 at H987 / 1 at H984')
chk(at(H984, A+'routes/oauth.ts', 833, 'if (!user) {') and at(H984, A+'routes/oauth.ts', 943, "if (!user || user.status !== 'ACTIVE') {"), 'parent H984: :833 `if (!user) {` and :943 the twin (the CORRECTED read)')
chk(at(H987, A+'routes/oauth.ts', 833, 'KS-1150 (R-1)') and at(H987, A+'routes/oauth.ts', 838, "'User inactive or not found'"), 'oauth.ts:833 comment / :838 the unified description')
chk(cnt(H987, A+'routes/oauth.ts', "description: 'User not found'") == 0 and cnt(H984, A+'routes/oauth.ts', "description: 'User not found'") == 1, "'User not found' description gone at H987 (0), present at H984 (1)")
chk(at(H987, A+'routes/oauth.ts', 447, "oauthRouter.get('/authorize'") and at(H987, A+'routes/oauth.ts', 499, "oauthRouter.post('/authorize'") and at(H987, A+'routes/oauth.ts', 734, "oauthRouter.post('/token'"), 'oauth.ts:447/:499/:734 the routes (H-pending anchors)')
k = blob(H987, A+'__tests__/ks790-token-pre-auth-user-lookup.test.ts')[2]; k0 = blob(H984, A+'__tests__/ks790-token-pre-auth-user-lookup.test.ts')[2]
chk('/User inactive or not found/' in k.split('\n')[228] and '/User not found/' in k0.split('\n')[226], 'ks790 :229 re-stated at H987 / :227 original at H984')
chk(k.count('expect(') == k0.count('expect(') and k.count("it('") == k0.count("it('"), 'ks790 expect( / it( counts unchanged by #987 (%d / %d)' % (k.count('expect('), k.count("it('")))
t2 = blob(H987, A+'__tests__/ks1150-code-grant-status-pin.test.ts')[2]
chk(t2.count("it('") == 4 and "app.listen(0, '127.0.0.1')" in t2.split('\n')[129], 'ks1150 test: 4 cells, :130 loopback listener')
p = lines(H984, G+'routes/proxy.ts') if blob(H984, G+'routes/proxy.ts')[0] else []
chk(cnt(H984, G+'routes/proxy.ts', 'requireScope(') == 6 and cnt(H984, G+'routes/proxy.ts', 'requireScopeOrRole(') == 1, 'H-mounts: proxy.ts requireScope( 6 / requireScopeOrRole( 1 at H984')
# --- the barrels (the launcher's blob-judged OK sets) at M20 / #799 / #985 ---
for ref, path, sha in [(M20, S+'index.ts', '6731f0f2f230869b96afe486131b22a80e7cb0f0'), ('6da848891924f859179d097d464a7b97c9783a6a', S+'index.ts', '8794bca5fefe419bf95144cb24eac3a2697d332d'), ('fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0', S+'index.ts', 'aeaf90dadff7ad1d426111756c5ec54ee2b34fb8'),
                       (M20, S+'middleware/index.ts', 'b5932490cc2102caae0d82d1dc9bc1d5384cef9b'), ('6da848891924f859179d097d464a7b97c9783a6a', S+'middleware/index.ts', '3a67987a7be4a4c02f8326bf8a840a2c2b4efbf3')]:
    chk(blob(ref, path)[0] == sha, f'barrel {path.split("src/")[-1]} at {ref[:9]} = {sha[:9]}')
# --- git-side: trees, parents, merge-bases, counts, numstats ---
chk(git('rev-parse', H983 + '^{tree}', 'f62c975c1^{tree}').split() == ['db10aea98aa0b2a494dd516743acbac8a23c84b9'] * 2, '#983 r2 tree == round-1 head tree db10aea98')
chk(git('rev-parse', H984 + '^{tree}', 'd00a2015c^{tree}').split() == ['39ab0226aa7978499fbf84d9e1980547e889d82f'] * 2, '#984 r2 tree == round-1 head tree 39ab0226a')
chk(git('rev-parse', 'e62eab87a^{tree}', M19 + '^{tree}').split() == ['60327bfa0560fce54b74e95059916f4723ddad70'] * 2, 'e62eab87a tree == M19 tree (the squash is tree-identical)')
chk(git('log', '-1', '--format=%P', H986).split() == [H984] and git('log', '-1', '--format=%P', H987).split() == [H984], '#986 and #987 parents both = #984 (siblings)')
chk(git('log', '-1', '--format=%P', H983).split() == ['f62c975c11ec97cdef04500fd98a43618e702763', M19], '#983 r2 parents = f62c975c1 + M19')
chk(git('log', '-1', '--format=%P', H984).split() == ['d00a2015c89a4720eaeab64482bbd9b89d878024', H983], '#984 r2 parents = d00a2015c + #983 r2')
for h in (H983, H984, H986, H987):
    chk(git('merge-base', M20, h).strip() == M19, f'merge-base(M20, {h[:9]}) = M19')
chk(git('rev-list', '--count', f'{M19}..{H983}').strip() == '3' and git('rev-list', '--count', f'{H983}..{H984}').strip() == '2' and git('rev-list', '--count', f'{H984}..{H986}').strip() == '1' and git('rev-list', '--count', f'{H984}..{H987}').strip() == '1', 'rev-list counts 3 / 2 / 1 / 1')
chk(git('rev-list', '--count', f'{H986}..{H987}').strip() == '1' and git('rev-list', '--count', f'{H987}..{H986}').strip() == '1', '#986 and #987 neither contains the other')
chk(len(git('diff', '--name-only', H984, H986).split()) == 2 and len(git('diff', '--name-only', H984, H987).split()) == 3 and len(git('diff', '--name-only', M19, H983).split()) == 4 and len(git('diff', '--name-only', H983, H984).split()) == 6, 'own-delta file counts 2 / 3 / 4 / 6')
chk(git('diff', '--numstat', H984, H986, '--', A+'routes/auth.ts').split()[:2] == ['20', '0'] and git('diff', '--numstat', H984, H987, '--', A+'routes/oauth.ts').split()[:2] == ['6', '2'], 'numstat auth.ts +20 -0 / oauth.ts +6 -2')
chk(git('rev-parse', H986 + ':Blockchain/Dev/packages/shared', M20 + ':Blockchain/Dev/packages/shared').split() == ['d4acb0abe56f9f6f04371422b540ae150c21c4f2'] * 2, 'packages/shared subtree identical H986 == M20')
chk(git('rev-parse', H983 + ':Blockchain/Dev/package-lock.json', M20 + ':Blockchain/Dev/package-lock.json').split() == ['17d2061b397595677ae789683b0ca1d4b8398bec'] * 2, 'lockfile unchanged')
# negative-token arm
if arg == '--neg-token':
    chk(cnt(H986, A+'routes/oauth.ts', 'denylistRefreshJti(') == 1, 'NEG: oauth.ts denylistRefreshJti( demanded 1 (known 0)')
    chk(cnt(H986, A+'routes/auth.ts', "payload.client_id !== undefined") == 0, 'NEG: the guard demanded ABSENT at H986 (known present)')
print(f'TALLY ok={ok} FAILS={fail} live_develop={live[:9]} {datetime.datetime.now().astimezone().strftime("%H:%M:%S")}')
sys.exit(1 if fail else 0)
PY
