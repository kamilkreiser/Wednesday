#!/bin/bash
# controls_check.sh — re-grep every §4 positive-control token of the #983 (KS-823) TIER-1 ROUND-1 brief at the PINNED
# head f62c975c1, its stack PARENT e62eab87a (#982's head) and origin develop M18 8861e6216 through the GitHub contents
# API (read-only; GH_TOKEN sourced by NAME from the Secuura .env, never printed). Tokens were derived from #983's OWN
# files at this head and its parent — never carried from another gate's brief. PRESENT tokens must grep the stated
# count; ABSENT tokens must grep exactly 0; the untouched neighbours (types/index.ts, routes/auth.ts, services/oauth.ts,
# userRepo.ts, routes/wallet.ts) must be blob-identical at head and develop; jwt.ts must be blob-identical at parent and
# develop (the PR is the only thing that moves it); the ks790 test's delta must touch NO expect( line; the refresh
# branch's ORDER (identify -> resolve app -> secret -> verify token -> denylist -> binding -> user) must read from the
# source in that order; the minter census must read 5 two-argument callers + 2 three-argument callers.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD="${QA983_HEAD:-f62c975c11ec97cdef04500fd98a43618e702763}"
PARENT="${QA983_PARENT:-e62eab87a6263e25c41c9bb814d5831842bb6c7e}"
DEV="${QA983_DEVELOP:-8861e62161466c40f08d2b10a30edeb203123993}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
W="$(mktemp -d "${TMPDIR:-/tmp}/qa983ctl.XXXXXX")"
P='Blockchain/Dev/services/auth/src'
OAUTH="$P/routes/oauth.ts"; JWT="$P/services/jwt.ts"; T823="$P/__tests__/ks823-refresh-grant-client-auth-and-binding.test.ts"
T790="$P/__tests__/ks790-token-pre-auth-user-lookup.test.ts"; T820="$P/__tests__/ks820-821-token-client-auth-and-apptype.test.ts"
TYPES="$P/types/index.ts"; AUTHR="$P/routes/auth.ts"; SOAUTH="$P/services/oauth.ts"; UREPO="$P/repositories/userRepo.ts"; WALLET="$P/routes/wallet.ts"

fetch() { # path ref outfile -> prints blob sha (or UNREADABLE / ABSENT)
  ( set -a; . "$SECUURA_ENV"; set +a
    PTH="$1" REF="$2" OUT="$3" python3 - <<'PY'
import base64, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/contents/" + os.environ["PTH"] + "?ref=" + os.environ["REF"]
try:
    o = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except urllib.error.HTTPError as e:
    print("ABSENT HTTP%d" % e.code); sys.exit(0)
except Exception as e:
    print("UNREADABLE " + type(e).__name__); sys.exit(0)
open(os.environ["OUT"], "wb").write(base64.b64decode(o["content"]))
print(o["sha"])
PY
  )
}
FAILS=0
echo "controls_check.sh — head ${HEAD:0:9}, parent ${PARENT:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
for spec in "oauth:$OAUTH:$HEAD" "oauth_p:$OAUTH:$PARENT" "oauth_d:$OAUTH:$DEV" "jwt:$JWT:$HEAD" "jwt_p:$JWT:$PARENT" "jwt_d:$JWT:$DEV" \
            "t823:$T823:$HEAD" "t790:$T790:$HEAD" "t790_p:$T790:$PARENT" "t820:$T820:$HEAD" "t820_p:$T820:$PARENT" "t820_d:$T820:$DEV" \
            "types:$TYPES:$HEAD" "types_d:$TYPES:$DEV" "authr:$AUTHR:$HEAD" "authr_d:$AUTHR:$DEV" "soauth:$SOAUTH:$HEAD" "soauth_d:$SOAUTH:$DEV" \
            "urepo:$UREPO:$HEAD" "urepo_d:$UREPO:$DEV" "wallet:$WALLET:$HEAD" "wallet_d:$WALLET:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; ABSENT*) echo "FAIL $n: $p ABSENT at ${ref:0:9} ($sha)"; FAILS=$((FAILS+1)); : > "$W/$n"; echo "absent" > "$W/$n.blob"; continue ;; esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
done
# the two files that must NOT exist before the PR
for spec in "t823_p:$T823:$PARENT" "t823_d:$T823:$DEV" "t790_d:$T790:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in ABSENT*) echo "ok   $n: ${p##*/} ABSENT at ${ref:0:9} (as it must be)" ;; UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; *) echo "FAIL $n: ${p##*/} EXISTS at ${ref:0:9} (blob ${sha:0:9}) — it must not"; FAILS=$((FAILS+1)) ;; esac
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis oauth de00ffcea; blobis oauth_p 80e05458e; blobis oauth_d 4b03f555e
blobis jwt 62b6db272; blobis jwt_p d0d55c11b; blobis jwt_d d0d55c11b
blobis t823 2c0135b6f; blobis t790 f98e8c806; blobis t790_p cfed82d54
blobis t820 b998b5b7d; blobis t820_p b998b5b7d; blobis t820_d 106c762f1
blobis types 9b0b4f08a; blobis types_d 9b0b4f08a; blobis authr 132d3b8d3; blobis authr_d 132d3b8d3
blobis soauth e9953d376; blobis soauth_d e9953d376; blobis urepo 822b3fcd8; blobis urepo_d 822b3fcd8
same() { cmp -s "$W/$1" "$W/$2" && echo "ok   $1 == $2 byte-identical ($3)" || { echo "FAIL $1 != $2 ($3)"; FAILS=$((FAILS+1)); }; }
diff_() { cmp -s "$W/$1" "$W/$2" && { echo "FAIL $1 == $2 byte-identical ($3)"; FAILS=$((FAILS+1)); } || echo "ok   $1 != $2 DIFFERS ($3)"; }
same jwt_p jwt_d "jwt.ts: #982 does not touch it; #983 is the only mover"
diff_ jwt jwt_p "jwt.ts: #983 changes it"
diff_ oauth oauth_p "routes/oauth.ts: #983 changes it"; diff_ oauth_p oauth_d "routes/oauth.ts: #982 changed it first (the stack)"
same t820 t820_p "ks820-821: #983 does not touch the file #982 touched"; diff_ t820_p t820_d "ks820-821: #982's one mock hunk (ruled ACCEPTED)"
same types types_d "types/index.ts untouched (JwtPayload)"; same authr authr_d "routes/auth.ts untouched (the sibling /api/auth/refresh)"
same soauth soauth_d "services/oauth.ts untouched (getAppByClientId / verifyClientSecret / exchangeCode)"; same urepo urepo_d "userRepo.ts untouched"; same wallet wallet_d "routes/wallet.ts untouched"
diff_ t790 t790_p "ks790 test: #983 edits its refresh fixtures"
for pair in "oauth:70c634fdad581d01" "oauth_p:fc54cc5f1494ad48" "oauth_d:cc4f4ac0df1b3393" "jwt:bad7e362c6ca68cb" "jwt_p:33545ba5a9c6951a" "t823:b4fc5dde6a66d4ad" "t790:1a1e9b790a31da52" "t790_p:55c12270001fd653" "t820:d0883d41f8a38b96" "t820_d:4f66d57fd174c85b" "types:f76921a737b8e81f" "authr:c1c3515cbb5b7a18" "soauth:aaec1cfc72ee2c9d" "urepo:24670fe3656152d2"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(shasum -a 256 "$W/$f" | cut -c1-16)" = "$want" ] && echo "ok   $f sha256 $want" || { echo "FAIL $f sha256 is $(shasum -a 256 "$W/$f" | cut -c1-16), not $want"; FAILS=$((FAILS+1)); }
done
for pair in "oauth:1332" "oauth_p:1260" "oauth_d:1242" "jwt:395" "jwt_p:374" "t823:276" "t790:253" "t790_p:249" "t820:377" "t820_d:369" "authr:1319" "soauth:395"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -l < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want lines" || { echo "FAIL $f is $(wc -l < "$W/$f" | tr -d ' ') lines, not $want"; FAILS=$((FAILS+1)); }
done
for pair in "oauth:67227" "oauth_p:62763" "oauth_d:61492" "jwt:15066" "jwt_p:13692" "t823:15463" "t790:12822" "t790_p:12429" "t820:18387" "t820_d:17925"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -c < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want bytes" || { echo "FAIL $f is $(wc -c < "$W/$f" | tr -d ' ') bytes, not $want"; FAILS=$((FAILS+1)); }
done
lineis() { # file line expected-text
  local got; got="$(sed -n "${2}p" "$W/$1")"
  [ "$got" = "$3" ] && echo "ok   $1:$2 = $3" || { echo "FAIL $1:$2 is: $got"; FAILS=$((FAILS+1)); }
}
# --- routes/oauth.ts at HEAD: the lines the brief cites
lineis oauth 698 "function readClientId(req: Request): string | undefined {"
lineis oauth 714 "function readClientSecret(req: Request, clientId: string): string | undefined {"
lineis oauth 723 "        if (user === clientId && pass) return pass;"
lineis oauth 734 "oauthRouter.post('/token', async (req: Request, res: Response) => {"
lineis oauth 777 "      // SCOPE — this block is grant_type=authorization_code. The refresh_token"
lineis oauth 844 "      const tokens = generateTokenPair(user, session.id, { clientId: client_id });"
lineis oauth 856 "    } else if (grant_type === 'refresh_token') {"
lineis oauth 879 "      const refreshClientId = readClientId(req);"
lineis oauth 880 "      if (!refreshClientId) {"
lineis oauth 883 "      const refreshApp = await getAppByClientId(refreshClientId);"
lineis oauth 884 "      if (!refreshApp) {"
lineis oauth 887 "      if (refreshApp.appType === 'confidential') {"
lineis oauth 889 "        if (!presented || !(await verifyClientSecret(refreshClientId, presented))) {"
lineis oauth 910 "        decoded = verifyRefreshToken(refresh_token);"
lineis oauth 919 "      if (decoded.jti && (await isRefreshJtiDenylisted(decoded.jti))) {"
lineis oauth 931 "      if (decoded.client_id !== refreshClientId) {"
lineis oauth 938 "      const user = await userRepo.getUserByIdPreAuth(decoded.userId);"
lineis oauth 939 "      if (!user || user.status !== 'ACTIVE') {"
lineis oauth 948 "      const tokens = generateTokenPair(user, session.id, { clientId: refreshClientId });"
# --- routes/oauth.ts at the PARENT: the unfixed refresh branch (the red-first's product)
lineis oauth_p 754 "      // SCOPE — this whole block is grant_type=authorization_code. On"
lineis oauth_p 755 "      // grant_type=refresh_token NO client is authenticated at all today, for"
lineis oauth_p 818 "      const tokens = generateTokenPair(user, session.id);"
lineis oauth_p 876 "      const tokens = generateTokenPair(user, session.id);"
# --- jwt.ts at HEAD
lineis jwt 28 "export interface OAuthMintOptions {"
lineis jwt 32 "export type OAuthTokenClaims = JwtPayload & { client_id?: string };"
lineis jwt 166 "function signToken(payload: Omit<OAuthTokenClaims, 'iat' | 'exp'>, expiresInSeconds: number): string {"
lineis jwt 178 "export function generateAccessToken(user: User, sessionId: string, oauth?: OAuthMintOptions): string {"
lineis jwt 195 "    ...(oauth ? { client_id: oauth.clientId } : {}), // KS-823"
lineis jwt 206 "export function generateRefreshToken(user: User, sessionId: string, oauth?: OAuthMintOptions): string {"
lineis jwt 219 "    ...(oauth ? { client_id: oauth.clientId } : {}), // KS-823: the refresh grant checks this against the presenting client"
lineis jwt 229 "export function generateTokenPair(user: User, sessionId: string, oauth?: OAuthMintOptions): {"
lineis jwt 367 "export function verifyRefreshToken(token: string): OAuthTokenClaims {"
lineis jwt 368 "  const payload = verifyToken(token) as OAuthTokenClaims;"
# --- the new test at HEAD
lineis t823 131 "  server = app.listen(0, '127.0.0.1');"
lineis t823 125 "  await jwtMod.initJwtKeys();"
lineis t823 71 "      return { rows: row && row.is_active === true ? [row] : [] }; // the definer pins is_active = true"
lineis t823 228 "    const { refreshToken } = mint(USER, 'sess-login'); // no client: the /api/auth/login shape"
# --- the ks790 test at HEAD (the two stacked hunks) and at the PARENT
lineis t790 115 "    return { userId: ACTIVE_USER.id, sessionId: 'sess-old', jti: 'jti-790', type: 'refresh', client_id: 'client-1' };"
lineis t790 193 "const refresh = () => raw('POST', '/api/oauth/token', { grant_type: 'refresh_token', refresh_token: 'VALID_REFRESH_790', client_id: 'client-1', client_secret: 'the-secret' });"
lineis t790_p 113 "    return { userId: ACTIVE_USER.id, sessionId: 'sess-old', jti: 'jti-790', type: 'refresh' };"
lineis t790_p 189 "const refresh = () => raw('POST', '/api/oauth/token', { grant_type: 'refresh_token', refresh_token: 'VALID_REFRESH_790' });"
# --- the sibling /api/auth/refresh (unchanged; the class probe's lines)
lineis authr 658 "authRoutes.post('/refresh', async (req: AuthenticatedRequest, res: Response, next) => {"
lineis authr 665 "    const payload = verifyRefreshToken(refreshTokenValue);"
lineis authr 689 "    const tokens = generateTokenPair(user, session.id);"
lineis authr 698 "      await denylistRefreshJti(payload.jti, remaining);"
# --- services/oauth.ts (the mocked SQL shapes and the second refusal mechanism)
lineis soauth 133 "    'SELECT * FROM auth_find_oauth_app_by_client_id(\$1)',"
lineis soauth 158 "export async function verifyClientSecret(clientId: string, secret: string): Promise<boolean> {"
lineis soauth 161 "  if (result.rows.length === 0) return false;"
lineis soauth 266 "    'SELECT * FROM oauth_authorization_codes WHERE code = \$1 AND client_id = \$2 AND used = false',"
lineis soauth 340 "  await query('UPDATE oauth_authorization_codes SET used = true WHERE code = \$1', [params.code]);"
lineis soauth 374 "    appType: row.app_type || 'public',"
chk() { # file token mode(present|absent|N)
  local f="$1" tok="$2" mode="$3" c
  c="$(/usr/bin/grep -c -F -- "$tok" "$W/$f")"
  if [ "$mode" = present ] && [ "$c" -ge 1 ]; then echo "ok   $f  present x$c  $tok"
  elif [ "$mode" = absent ] && [ "$c" -eq 0 ]; then echo "ok   $f  absent      $tok"
  elif [ "$mode" != present ] && [ "$mode" != absent ] && [ "$c" -eq "$mode" ]; then echo "ok   $f  exactly x$c $tok"
  else echo "FAIL $f  $mode expected, count $c: $tok"; FAILS=$((FAILS+1)); fi
}
# --- routes/oauth.ts at head: the tamper anchors (count 1 each) and the parent's world absent
chk oauth "function readClientId(req: Request)" 1
chk oauth "const refreshClientId = readClientId(req);" 1
chk oauth "if (!refreshApp) {" 1
chk oauth "if (refreshApp.appType === 'confidential') {" 1
chk oauth "if (decoded.client_id !== refreshClientId) {" 1
chk oauth "generateTokenPair(user, session.id, { clientId: client_id });" 1
chk oauth "generateTokenPair(user, session.id, { clientId: refreshClientId });" 1
chk oauth "generateTokenPair(user, session.id);" absent
chk oauth "'Refresh token was not issued to this client'" 1
chk oauth "'client_id is required'" 2
chk oauth "'Unknown or inactive client'" 2
chk oauth "'Client authentication failed'" 2
chk oauth "userRepo.getUserByIdPreAuth(" 2
chk oauth "userRepo.getUserById(" absent
chk oauth "NO client is authenticated at all today" absent
chk oauth "KS-823, High, file-only by ruling" absent
chk oauth "OAuth refresh refused: token not bound to the presenting client" 1
chk oauth "OAuth refresh refused: confidential client did not authenticate" 1
chk oauth "denylistRefreshJti(" absent
chk oauth "import { generateTokenPair, verifyRefreshToken } from '../services/jwt';" 1
# --- routes/oauth.ts at the parent: the world the red-first runs against
chk oauth_p "readClientId" absent
chk oauth_p "refreshClientId" absent
chk oauth_p "decoded.client_id" absent
chk oauth_p "generateTokenPair(user, session.id);" 2
chk oauth_p "NO client is authenticated at all today" 1
chk oauth_p "userRepo.getUserByIdPreAuth(" 2
# --- routes/oauth.ts at develop: before #982 (the plain lookup) and before #983
chk oauth_d "userRepo.getUserById(" 2
chk oauth_d "userRepo.getUserByIdPreAuth(" absent
chk oauth_d "readClientId" absent
chk oauth_d "import { generateTokenPair, verifyRefreshToken } from '../services/jwt';" absent
# --- jwt.ts
chk jwt "export interface OAuthMintOptions {" 1
chk jwt "export type OAuthTokenClaims = JwtPayload & { client_id?: string };" 1
chk jwt "...(oauth ? { client_id: oauth.clientId } : {})" 2
chk jwt "oauth?: OAuthMintOptions" 3
chk jwt "client_id" 6
chk jwt "export function verifyRefreshToken(token: string): JwtPayload {" absent
chk jwt_p "OAuthMintOptions" absent
chk jwt_p "client_id" absent
chk jwt_p "export function verifyRefreshToken(token: string): JwtPayload {" 1
# --- the new test file: 11 cells, the raw socket, the real minter, the loopback bind
chk t823 "  it('" 11
chk t823 "app.listen(0, '127.0.0.1')" 1
chk t823 "await jwtMod.initJwtKeys();" 1
chk t823 "vi.mock('../services/jwt'" absent
chk t823 "auth_find_oauth_app_by_client_id" 1
chk t823 "net.connect(port, '127.0.0.1'" 1
chk t823 "REFUSES a confidential app\\'s refresh token presented with NO credential" 1
chk t823 "REFUSES a WRONG secret — 401 invalid_client" 1
chk t823 "REFUSES a DEACTIVATED app\\'s refresh token even with its correct secret" 1
chk t823 "BINDING — a token minted for client-1 presented by an authenticated client-2 is refused" 1
chk t823 "BINDING (fail-closed) — a refresh token carrying NO client claim" 1
chk t823 "REFUSES a refresh with NO client identification at all — 400 invalid_request" 1
chk t823 "MINT — the pair the authorization_code grant issues carries the redeeming client on BOTH halves" 1
chk t823 "CONTROL — the right secret in the body redeems" 1
chk t823 "CONTROL — the right secret over HTTP Basic redeems" 1
chk t823 "CONTROL — a PUBLIC app redeems its own bound token with its client_id and no secret" 1
chk t823 "CONTROL — an invalid refresh token is still 400 invalid_grant" 1
chk t823 "expect(claims.client_id).toBeUndefined();" 1
chk t823 "express.urlencoded" absent
chk t823 "getSession" absent
# --- the ks790 test: the stacked hunks; 6 cells and 17 expect( at head AND parent
chk t790 "  it('" 6
chk t790 "expect(" 17
chk t790_p "expect(" 17
chk t790 "client_id: 'client-1', client_secret: 'the-secret' });" 1
chk t790_p "client_id: 'client-1', client_secret: 'the-secret' });" absent
chk t790 "vi.mock('../services/jwt'" 1
chk t790 "app.listen(0, '127.0.0.1')" 1
# --- ks820-821: #982's one mock hunk (8 lines) present at head and parent, absent at develop
chk t820 "getUserByIdPreAuth: vi.fn(async () => ({" 1
chk t820_d "getUserByIdPreAuth" absent
# --- the sibling route and the service layer
chk authr "authRoutes.post('/refresh'" 1
chk authr "client_id" absent
chk authr "const tokens = generateTokenPair(user, session.id);" 4
chk wallet "generateTokenPair(user, session.id);" 1
chk soauth "'SELECT * FROM auth_find_oauth_app_by_client_id(\$1)'" 2
chk types "client_id" absent
# --- the Python re-derivations: the ks790 delta touches no assertion; the refresh branch's ORDER; the minter census;
#     readClientId/readClientSecret over the Basic-vs-body shapes; the raw-control-byte census
cat > "$W/sim.py" <<'PY'
import re, sys, base64
W = sys.argv[1]
def rd(n): return open(f"{W}/{n}", encoding="utf-8").read()
O, OP, J, T, K, KP, A, WL = rd("oauth"), rd("oauth_p"), rd("jwt"), rd("t823"), rd("t790"), rd("t790_p"), rd("authr"), rd("wallet")
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
# (1) the ks790 delta: the set of expect( lines is identical parent -> head (assertions unchanged, as the READY claims)
ek = [l.strip() for l in K.split("\n") if "expect(" in l]; ekp = [l.strip() for l in KP.split("\n") if "expect(" in l]
ck(ek == ekp and len(ek) == 17, f"ks790: expect( lines identical parent->head ({len(ekp)} -> {len(ek)}); assertions unchanged")
dl = [i + 1 for i, (a, b) in enumerate(zip(KP.split("\n"), K.split("\n"))) if a != b]
ck(len(K.split("\n")) - len(KP.split("\n")) == 4, f"ks790: +4 lines parent->head (first differing parent line {dl[:1]})")
# (2) ORDER inside the refresh branch at head: identify -> resolve app -> secret -> verify token -> denylist -> binding -> user -> mint
rs = O.index("} else if (grant_type === 'refresh_token') {"); rb = O[rs:O.index("} catch (error: any) {", rs)]
order = ["const refreshClientId = readClientId(req);", "if (!refreshClientId) {", "const refreshApp = await getAppByClientId(refreshClientId);", "if (!refreshApp) {",
         "if (refreshApp.appType === 'confidential') {", "verifyClientSecret(refreshClientId, presented)", "decoded = verifyRefreshToken(refresh_token);",
         "isRefreshJtiDenylisted(decoded.jti)", "if (decoded.client_id !== refreshClientId) {", "userRepo.getUserByIdPreAuth(decoded.userId)",
         "generateTokenPair(user, session.id, { clientId: refreshClientId });"]
idx = [rb.find(t) for t in order]
ck(all(i >= 0 for i in idx) and idx == sorted(idx), f"refresh-branch ORDER at head: identify < app < secret < verify < denylist < binding < user < mint (offsets {idx})")
rps = OP.index("} else if (grant_type === 'refresh_token') {"); rbp = OP[rps:OP.index("} catch (error: any) {", rps)]
ck(all(rbp.find(t) < 0 for t in order[:6] + [order[8]]), "refresh-branch at the PARENT: no client identification, no app lookup, no secret, no binding (the red-first's product)")
# (3) minter census across the auth service (routes only): 5 two-arg callers (auth.ts x4, wallet.ts x1) + 2 three-arg (oauth.ts)
two = A.count("generateTokenPair(user, session.id);") + WL.count("generateTokenPair(user, session.id);") + O.count("generateTokenPair(user, session.id);")
three = O.count("generateTokenPair(user, session.id, { clientId:")
ck(two == 5 and three == 2, f"minter census at head: {two} two-argument callers (auth.ts 4 + wallet.ts 1 + oauth.ts 0) + {three} three-argument (oauth.ts) = 7")
ck(A.count("const tokens = generateTokenPair(") == 5 and A.count("generateTokenPair(\n") == 1 and A.count("clientId") == 0, "routes/auth.ts: five `const tokens = generateTokenPair(` (four one-line + the multi-line :448) — none passes a client (the sibling /refresh re-mints UNBOUND)")
# (4) readClientId / readClientSecret re-derived from the head source's semantics over the gate's Basic-vs-body shapes
def read_client_id(body, headers):
    v = body.get("client_id")
    if isinstance(v, str) and len(v) > 0: return v
    h = headers.get("authorization")
    if h and re.match(r"^Basic ", h, re.I):
        try:
            d = base64.b64decode(h[6:].strip()).decode("utf8"); sep = d.find(":")
            if sep > 0: return d[:sep]
        except Exception: pass
    return None
def read_client_secret(body, headers, client_id):
    h = headers.get("authorization")
    if h and re.match(r"^Basic ", h, re.I):
        try:
            d = base64.b64decode(h[6:].strip()).decode("utf8"); sep = d.find(":")
            if sep > 0:
                u, p = d[:sep], d[sep + 1:]
                if u == client_id and p: return p
        except Exception: pass
    v = body.get("client_secret")
    return v if isinstance(v, str) and len(v) > 0 else None
def basic(u, p): return {"authorization": "Basic " + base64.b64encode(f"{u}:{p}".encode()).decode()}
ck(read_client_id({}, basic("client-1", "s1")) == "client-1" and read_client_secret({}, basic("client-1", "s1"), "client-1") == "s1", "shape: Basic only -> client from the userid, secret from the password (CONTROL Basic)")
ck(read_client_id({"client_id": "client-1", "client_secret": "s1"}, {}) == "client-1" and read_client_secret({"client_id": "client-1", "client_secret": "s1"}, {}, "client-1") == "s1", "shape: body only -> client + secret from the body (CONTROL body)")
ck(read_client_id({"client_id": "client-2"}, basic("client-1", "s1")) == "client-2" and read_client_secret({"client_id": "client-2"}, basic("client-1", "s1"), "client-2") is None, "shape Tg-MIX: body client-2 + Basic client-1:s1 -> identifies as client-2, NO secret attaches -> 401 (predicted)")
ck(read_client_id({"client_id": ""}, {}) is None and read_client_id({"client_id": 7}, {}) is None and read_client_id({"client_id": ["client-1"]}, {}) is None, "shape: empty / numeric / array client_id -> no identification -> 400 invalid_request (predicted)")
ck(read_client_id({}, basic("pub-1", "")) == "pub-1" and read_client_secret({}, basic("pub-1", ""), "pub-1") is None, "shape: Basic 'pub-1:' (empty password) -> identifies pub-1, no secret (a public app's Basic-only shape)")
ck(read_client_id({}, {"authorization": "Basic %%%not-base64"}) is None, "shape: malformed Basic -> no identification, no throw")
# (5) the fail-closed predicate as written: an ABSENT claim is refused, a matching claim passes, a foreign claim is refused
pred = lambda decoded_client, presenting: decoded_client != presenting
ck(pred(None, "client-1") and pred("client-1", "client-2") and not pred("client-1", "client-1"), "binding predicate `decoded.client_id !== refreshClientId`: absent -> refused (fail-closed), foreign -> refused, own -> passes")
# (6) the sibling /api/auth/refresh: verifies the same token type, mints with TWO arguments, never reads client_id
ck("verifyRefreshToken(refreshTokenValue)" in A and A.count("client_id") == 0 and "generateTokenPair(user, session.id);" in A[A.index("authRoutes.post('/refresh'"):A.index("authRoutes.post('/refresh'") + 3000], "routes/auth.ts /refresh: accepts any valid refresh token (cookie or body), reads no client, re-mints UNBOUND — the class probe's mechanism (READ ONLY)")
# (7) the new test's mocks name the product's SQL shapes exactly (a fixture naming the wrong object fails in the defect's shape)
S = rd("soauth")
ck("auth_find_oauth_app_by_client_id" in S and "FROM oauth_authorization_codes" in S and "used = false" in S and "UPDATE oauth_authorization_codes SET used = true" in S, "the ks823 mock's three SQL discriminators exist verbatim in services/oauth.ts at head")
ck("appType: row.app_type || 'public'" in S and "app_type" in T and "client_secret_hash" in T and "createHash('sha256')" in T, "the ks823 app rows use the product's column names (app_type, client_secret_hash = sha256 hex, is_active)")
# (8) raw-control-byte census over every fetched file + a synthetic positive control
bad = 0
for n in ["oauth", "jwt", "t823", "t790", "t820", "authr", "soauth"]:
    b = open(f"{W}/{n}", "rb").read(); bad += sum(1 for x in b if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)
ctrl = b"const bad = 'doc\x00bad';\n"; c = [i for i, x in enumerate(ctrl) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f]
ck(bad == 0 and c == [16], f"raw control bytes across the seven fetched files: {bad} (synthetic NUL control at offset {c})")
sys.exit(1 if fails else 0)
PY
python3 "$W/sim.py" "$W" || FAILS=$((FAILS+1))
echo "work dir (kept): $W"
echo "controls_check: FAILS=$FAILS"
[ "$FAILS" -eq 0 ] && exit 0 || exit 1
