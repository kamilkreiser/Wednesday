#!/bin/bash
# controls_check.sh — re-grep every positive-control token of the #984 (KS-835) TIER-1 brief at the PINNED head
# d00a2015c, its STACK PARENT f62c975c1 and develop M18 8861e6216 through the GitHub contents API (read-only; GH_TOKEN
# sourced by NAME from the Secuura .env, never printed). Tokens were derived from #984's OWN files at this head, the
# parent's copies, and the neighbours the brief reads (gateway middleware/auth.ts, routes/proxy.ts, services/enforcement.ts,
# middleware/rateLimitEnforce.ts, services/auth/src/routes/auth.ts, packages/shared/src/security/scopes.ts, the ks860 guard)
# — never carried from another gate's brief. PRESENT tokens must grep the stated count; ABSENT tokens must grep exactly 0;
# the line-exact anchors the brief cites must read as quoted; the blobs, sizes, sha256s and line counts must be the
# brief's; the scopes.ts delta must be docblock-only; the ks860 site/host regexes must read 0 offenders over the three
# test files (and 1 over a planted host-less control).
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD="${QA984_HEAD:-d00a2015c89a4720eaeab64482bbd9b89d878024}"
PARENT="${QA984_PARENT:-f62c975c11ec97cdef04500fd98a43618e702763}"
DEV="${QA984_DEVELOP:-8861e62161466c40f08d2b10a30edeb203123993}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
W="$(mktemp -d "${TMPDIR:-/tmp}/qa984ctl.XXXXXX")"
JWT='Blockchain/Dev/services/auth/src/services/jwt.ts'
OAUTH='Blockchain/Dev/services/auth/src/routes/oauth.ts'
SCOPES='Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts'
KS823='Blockchain/Dev/services/auth/src/__tests__/ks823-refresh-grant-client-auth-and-binding.test.ts'
KS835A='Blockchain/Dev/services/auth/src/__tests__/ks835-oauth-mint-carries-granted-scope.test.ts'
KS835G='Blockchain/Dev/services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts'
GWAUTH='Blockchain/Dev/services/api-gateway/src/middleware/auth.ts'
PROXY='Blockchain/Dev/services/api-gateway/src/routes/proxy.ts'
ENFORCE='Blockchain/Dev/services/api-gateway/src/services/enforcement.ts'
RATELIM='Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts'
AUTHR='Blockchain/Dev/services/auth/src/routes/auth.ts'
SHSCOPES='Blockchain/Dev/packages/shared/src/security/scopes.ts'
KS860='Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts'
TYPES='Blockchain/Dev/services/auth/src/types/index.ts'
KS820='Blockchain/Dev/services/auth/src/__tests__/ks820-821-token-client-auth-and-apptype.test.ts'

fetch() { # path ref outfile -> prints blob sha (or ABSENT / UNREADABLE)
  ( set -a; . "$SECUURA_ENV"; set +a
    P="$1" REF="$2" OUT="$3" python3 - <<'PY'
import base64, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/contents/" + os.environ["P"] + "?ref=" + os.environ["REF"]
try:
    o = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except urllib.error.HTTPError as e:
    print("ABSENT" if e.code == 404 else "UNREADABLE HTTP%d" % e.code); sys.exit(0)
except Exception as e:
    print("UNREADABLE " + type(e).__name__); sys.exit(0)
open(os.environ["OUT"], "wb").write(base64.b64decode(o["content"]))
print(o["sha"])
PY
  )
}
FAILS=0
echo "controls_check.sh — head ${HEAD:0:9}, parent ${PARENT:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
for spec in "jwt:$JWT:$HEAD" "jwt_p:$JWT:$PARENT" "jwt_d:$JWT:$DEV" "oauth:$OAUTH:$HEAD" "oauth_p:$OAUTH:$PARENT" "oauth_d:$OAUTH:$DEV" \
            "scopes:$SCOPES:$HEAD" "scopes_p:$SCOPES:$PARENT" "scopes_d:$SCOPES:$DEV" "ks823:$KS823:$HEAD" "ks823_p:$KS823:$PARENT" \
            "ks835a:$KS835A:$HEAD" "ks835g:$KS835G:$HEAD" "gwauth:$GWAUTH:$HEAD" "gwauth_d:$GWAUTH:$DEV" "proxy:$PROXY:$HEAD" "proxy_d:$PROXY:$DEV" \
            "enforce:$ENFORCE:$HEAD" "ratelim:$RATELIM:$HEAD" "authr:$AUTHR:$HEAD" "authr_d:$AUTHR:$DEV" "shscopes:$SHSCOPES:$HEAD" \
            "ks860:$KS860:$HEAD" "ks860_d:$KS860:$DEV" "types:$TYPES:$HEAD" "types_d:$TYPES:$DEV" "ks820:$KS820:$HEAD" "ks820_p:$KS820:$PARENT" "ks820_d:$KS820:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; esac
  if [ "$sha" = ABSENT ]; then echo "read $n = ${p##*/} @ ${ref:0:9}: ABSENT"; echo ABSENT > "$W/$n.blob"; continue; fi
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
done
# the two new test files must be ABSENT at the parent and at develop
for spec in "ks835a_p:$KS835A:$PARENT" "ks835g_p:$KS835G:$PARENT" "ks835a_d:$KS835A:$DEV" "ks835g_d:$KS835G:$DEV" "ks823_d:$KS823:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  [ "$sha" = ABSENT ] && echo "ok   $n = ${p##*/} @ ${ref:0:9}: ABSENT (as the brief says)" || { echo "FAIL $n = ${p##*/} @ ${ref:0:9}: expected ABSENT, got $sha"; FAILS=$((FAILS+1)); }
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis jwt 26562a224; blobis jwt_p 62b6db272; blobis jwt_d d0d55c11b
blobis oauth 0bab1b8bd; blobis oauth_p de00ffcea; blobis oauth_d 4b03f555e
blobis scopes 7aef335b9; blobis scopes_p b5403b189; blobis scopes_d b5403b189
blobis ks823 db9744c97; blobis ks823_p 2c0135b6f; blobis ks835a f61388142; blobis ks835g 548e1ec12
blobis gwauth 20311010d; blobis gwauth_d 20311010d; blobis proxy b99f45a4c; blobis proxy_d b99f45a4c
blobis enforce 533cd309c; blobis ratelim fc5c5a4d9; blobis authr 132d3b8d3; blobis authr_d 132d3b8d3; blobis shscopes c6040ca14
blobis ks860 e0dfadb9c; blobis ks860_d e0dfadb9c; blobis types 9b0b4f08a; blobis types_d 9b0b4f08a
blobis ks820 b998b5b7d; blobis ks820_p b998b5b7d; blobis ks820_d 106c762f1
for pair in "jwt:de0670cb20321114" "jwt_p:bad7e362c6ca68cb" "oauth:5e1ce25c995c3944" "oauth_p:70c634fdad581d01" "scopes:e0757e2185c1a832" "scopes_p:5ca7309168214d0c" \
            "ks823:4e743896fdc468e4" "ks823_p:b4fc5dde6a66d4ad" "ks835a:bc85078909065297" "ks835g:42841fc66a28487c" "gwauth:1ac19905b3198685" "authr:c1c3515cbb5b7a18"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(shasum -a 256 "$W/$f" | cut -c1-16)" = "$want" ] && echo "ok   $f sha256 $want" || { echo "FAIL $f sha256 is not $want"; FAILS=$((FAILS+1)); }
done
for pair in "jwt:406" "jwt_p:395" "jwt_d:374" "oauth:1338" "oauth_p:1332" "scopes:194" "scopes_p:183" "ks823:277" "ks823_p:276" "ks835a:219" "ks835g:125" "gwauth:401" "authr:1319"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -l < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want lines" || { echo "FAIL $f is not $want lines"; FAILS=$((FAILS+1)); }
done
for pair in "jwt:15955" "jwt_p:15066" "oauth:67687" "oauth_p:67227" "scopes:8138" "scopes_p:7348" "ks823:15731" "ks823_p:15463" "ks835a:11369" "ks835g:7109" "gwauth:16968" "authr:61456"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -c < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want bytes" || { echo "FAIL $f is not $want bytes"; FAILS=$((FAILS+1)); }
done
cmp -s "$W/scopes_p" "$W/scopes_d" && echo "ok   scopes.ts at the parent == at develop (untouched below #984)" || { echo "FAIL scopes.ts parent != develop"; FAILS=$((FAILS+1)); }
cmp -s "$W/gwauth" "$W/gwauth_d" && echo "ok   gateway auth.ts head == develop (untouched by the stack)" || { echo "FAIL gateway auth.ts head != develop"; FAILS=$((FAILS+1)); }
cmp -s "$W/proxy" "$W/proxy_d" && echo "ok   proxy.ts head == develop (untouched by the stack)" || { echo "FAIL proxy.ts head != develop"; FAILS=$((FAILS+1)); }
cmp -s "$W/authr" "$W/authr_d" && echo "ok   routes/auth.ts head == develop (untouched by the stack)" || { echo "FAIL routes/auth.ts head != develop"; FAILS=$((FAILS+1)); }
cmp -s "$W/ks860" "$W/ks860_d" && echo "ok   the ks860 guard head == develop" || { echo "FAIL ks860 head != develop"; FAILS=$((FAILS+1)); }
cmp -s "$W/ks820" "$W/ks820_p" && echo "ok   ks820-821 test head == parent (ruling 1's hunk is untouched above #982)" || { echo "FAIL ks820-821 head != parent"; FAILS=$((FAILS+1)); }
cmp -s "$W/jwt" "$W/jwt_p" && { echo "FAIL jwt.ts head == parent (#984 changed it)"; FAILS=$((FAILS+1)); } || echo "ok   jwt.ts head DIFFERS from the parent"
lineis() { # file line expected-text
  local got; got="$(sed -n "${2}p" "$W/$1")"
  [ "$got" = "$3" ] && echo "ok   $1:$2 = $3" || { echo "FAIL $1:$2 is: $got"; FAILS=$((FAILS+1)); }
}
# --- jwt.ts at head: the option type, the claims type, the two mint spreads
lineis jwt 35 "export interface OAuthMintOptions {"
lineis jwt 39 "  scopes: readonly string[];"
lineis jwt 41 "export type OAuthTokenClaims = JwtPayload & { client_id?: string; authMethod?: 'oauth' };"
lineis jwt 192 "  const scopes = getDefaultScopesForRole(user.role);"
lineis jwt 205 "    ...(oauth ? { scopes: [...oauth.scopes], authMethod: 'oauth' as const } : scopes.length > 0 ? { scopes } : {}),"
lineis jwt 206 "    ...(oauth ? { client_id: oauth.clientId } : {}), // KS-823"
lineis jwt 229 "    ...(oauth ? { scopes: [...oauth.scopes], authMethod: 'oauth' as const } : scopes.length > 0 ? { scopes } : {}), // KS-835"
lineis jwt 378 "export function verifyRefreshToken(token: string): OAuthTokenClaims {"
# --- jwt.ts at the PARENT: the pre-#984 shapes (the red-first's world)
lineis jwt_p 194 "    ...(scopes.length > 0 ? { scopes } : {}),"
lineis jwt_p 32 "export type OAuthTokenClaims = JwtPayload & { client_id?: string };"
# --- oauth.ts at head: the two grants
lineis oauth 848 "      const tokens = generateTokenPair(user, session.id, { clientId: client_id, scopes: parseScopeString(result.scope || '') });"
lineis oauth 857 "        scope: result.scope || '',"
lineis oauth 914 "        decoded = verifyRefreshToken(refresh_token);"
lineis oauth 935 "      if (decoded.client_id !== refreshClientId) {"
lineis oauth 954 "      const tokens = generateTokenPair(user, session.id, { clientId: refreshClientId, scopes: decoded.scopes ?? [] });"
lineis oauth 388 "  const requestedScopes = parseScopeString(scope);"
lineis oauth 656 "      scope: client.grantedScopes.join(' '),"
# --- scopes.ts at head: the gate's clauses (unchanged) and the new docblock
lineis scopes 35 "    const authMethod = user.authMethod || 'jwt';"
lineis scopes 36 "    if (authMethod === 'jwt' || authMethod === 'email') {"
lineis scopes 42 "    const userScopes: string[] = user.scopes || [];"
lineis scopes 45 "    if (userScopes.includes('*')) {"
lineis scopes 51 "    const hasScope = requiredScopes.some(s => userScopes.includes(s));"
lineis scopes 70 " * KS-835: what this reads, stated honestly. An OAuth-minted token carries the"
lineis scopes 84 "  if (user && !user.scopes) {"
lineis scopes 125 " *    any principal whose \`authMethod\` is \`jwt\` or \`email\`. KS-835 records that"
lineis scopes 126 " *    OAuth-minted tokens carry the \`email\` label too, so that branch is an"
# --- the gateway's authenticateToken: H3's two lines
lineis gwauth 147 "      authMethod: payload.authMethod || payload.auth_method || 'email',"
lineis gwauth 109 "export function parseTestToken(token: string): UserPayload | null {"
lineis gwauth 349 "      const decoded = await verifyRs256(token);"
lineis gwauth 370 "      req.user = decoded;"
lineis gwauth 277 "        authMethod: 'api_key',"
# --- the two other label consumers and the launder path
lineis enforce 161 "    const userAuthMethod = (user.authMethod || 'email').toLowerCase();"
lineis enforce 163 "    if (!allowed.includes(userAuthMethod) && !allowed.includes('email') && !allowed.includes('any')) {"
lineis ratelim 61 "const MACHINE_AUTH_METHODS = new Set(['api_key', 'oauth_app']);"
lineis ratelim 83 "    if (!user || !MACHINE_AUTH_METHODS.has(user.authMethod)) {"
lineis authr 658 "authRoutes.post('/refresh', async (req: AuthenticatedRequest, res: Response, next) => {"
lineis authr 665 "    const payload = verifyRefreshToken(refreshTokenValue);"
lineis authr 666 "    const session = await getSession(payload.sessionId);"
lineis authr 689 "    const tokens = generateTokenPair(user, session.id);"
# --- the scope-gated mounts
lineis proxy 375 "    requireScope('webhooks:manage'),"
lineis proxy 394 "    requireScope('users:read'),"
lineis proxy 568 "    requireScope('documents:read', 'documents:write'),"
lineis proxy 575 "    requireScope('certifications:read', 'certifications:write'),"
lineis proxy 731 "    requireScopeOrRole(ERASURE_SCOPE, ERASURE_GRACE_ROLES, ERASURE_ENFORCE_FLAG),"
lineis proxy 764 "    requireScope('anchors:write'),"
lineis proxy 770 "    requireScope('anchors:write'),"
lineis proxy 366 "  router.use('/api/auth', proxy('auth', { '^/api/auth': '/api/auth' }));"
# --- the role defaults
lineis shscopes 250 "    case 'OWNER':"
lineis shscopes 251 "      return ['documents:write'];"
# --- the tests: the listeners and the cells the brief cites
lineis ks835a 127 "  server = app.listen(0, '127.0.0.1');"
lineis ks835a 180 "    expect(access.scopes, \`access-token scopes: \${JSON.stringify(access.scopes)}\`).toEqual(['openid']);"
lineis ks835a 188 "    expect(decode(r.json?.access_token).authMethod).toBe('oauth');"
lineis ks835a 198 "    expect(access.scopes).toEqual(['openid']);"
lineis ks835a 208 "    expect(access.authMethod).toBe('oauth');"
lineis ks835a 209 "    expect(access.scopes ?? []).toEqual([]);"
lineis ks835a 216 "    expect(claims.scopes).toEqual(['documents:write']);"
lineis ks835g 60 "  app.get('/gated', authenticateToken(true), attachScopes, requireScope('webhooks:manage'), (req, res) => {"
lineis ks835g 64 "  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', resolve); });"
lineis ks835g 116 "    expect((withArray as unknown as { user: { scopes: string[] } }).user.scopes).toEqual(['openid']); // the array wins; the string never widens it"
lineis ks823 119 "let mint: (user: unknown, sessionId: string, opts?: { clientId: string; scopes: readonly string[] }) => { accessToken: string; refreshToken: string };"
lineis ks823 132 "  server = app.listen(0, '127.0.0.1');"
# --- the ks860 guard's clauses at develop (= head)
lineis ks860_d 433 "  const re = /\\.listen\\(\\s*0\\s*(,|\\))/g;"
lineis ks860_d 440 "      const host = /^\\s*(['\"])127\\.0\\.0\\.1\\1/.exec(rest);"
lineis ks860_d 463 "  it('🔴 no test file under services/ or packages/ calls app.listen(0) without binding 127.0.0.1', () => {"
lineis ks860_d 98 "const WALK_ROOTS = ['services', 'packages'] as const;"
chk() { # file token mode(present|absent|N)
  local f="$1" tok="$2" mode="$3" c
  c="$(/usr/bin/grep -c -F -- "$tok" "$W/$f")"
  if [ "$mode" = present ] && [ "$c" -ge 1 ]; then echo "ok   $f  present x$c  $tok"
  elif [ "$mode" = absent ] && [ "$c" -eq 0 ]; then echo "ok   $f  absent      $tok"
  elif [ "$mode" != present ] && [ "$mode" != absent ] && [ "$c" -eq "$mode" ]; then echo "ok   $f  exactly x$c $tok"
  else echo "FAIL $f  $mode expected, count $c: $tok"; FAILS=$((FAILS+1)); fi
}
# --- jwt.ts head: the tamper anchors
chk jwt "scopes: [...oauth.scopes], authMethod: 'oauth' as const" 2
chk jwt ", authMethod: 'oauth' as const" 2
chk jwt "scopes: readonly string[];" 1
chk jwt "authMethod?: 'oauth'" 1
chk jwt "// KS-835: an OAuth mint carries the GRANTED scopes (even when empty) and the" 1
chk jwt "getDefaultScopesForRole(user.role)" 2
chk jwt "'oauth_app'" 1
chk jwt "client_id: oauth.clientId" 2
# --- jwt.ts parent: the tamper shapes must NOT pre-exist; the head shapes absent
chk jwt_p "oauth.scopes" absent
chk jwt_p "authMethod" absent
chk jwt_p "scopes: readonly string[];" absent
chk jwt_p "client_id: oauth.clientId" 2
# --- oauth.ts head
chk oauth "scopes: parseScopeString(result.scope || '')" 1
chk oauth "scopes: decoded.scopes ?? []" 1
chk oauth "generateTokenPair(user, session.id, {" 2
chk oauth "scopes: ['documents:write']" absent
chk oauth "getDefaultScopesForRole" absent
chk oauth "validateScopes, parseScopeString, AVAILABLE_SCOPES," 1
chk oauth "decoded.client_id !== refreshClientId" 1
# --- oauth.ts parent: no grant passed
chk oauth_p "scopes: parseScopeString" absent
chk oauth_p "decoded.scopes" absent
chk oauth_p "generateTokenPair(user, session.id, { clientId: client_id });" 1
chk oauth_p "generateTokenPair(user, session.id, { clientId: refreshClientId });" 1
# --- scopes.ts head: the gate's clauses and the tamper anchors
chk scopes "const authMethod = user.authMethod || 'jwt';" 1
chk scopes "if (authMethod === 'jwt' || authMethod === 'email') {" 1
chk scopes "authMethod === 'oauth'" absent
chk scopes "if (user && !user.scopes) {" 1
chk scopes "user.scopes || []" 1
chk scopes "user.scopes || ['*']" absent
chk scopes "KS-835" 2
chk scopes "export function requireScopeOrRole(" 1
chk scopes_p "KS-835" 1
# --- the docblock-only delta: every changed line of scopes.ts head vs parent begins with ' *'
python3 - "$W/scopes_p" "$W/scopes" <<'PY' || FAILS=$((FAILS+1))
import sys, difflib
a = open(sys.argv[1], encoding='utf-8').read().splitlines(); b = open(sys.argv[2], encoding='utf-8').read().splitlines()
d = [l for l in difflib.unified_diff(a, b, n=0, lineterm='') if (l.startswith('+') or l.startswith('-')) and not l.startswith('+++') and not l.startswith('---')]
bad = [l for l in d if not l[1:].startswith(' *')]
print(f"{'ok  ' if d and not bad else 'FAIL'} scopes.ts parent->head: {len(d)} changed lines, {len(bad)} outside a docblock (expected 13 / 0): {bad[:3]}")
sys.exit(0 if d and not bad and len(d) == 13 else 1)
PY
# --- the gateway auth middleware
chk gwauth "req.user = decoded;" 1
chk gwauth "req.user = testPayload;" 1
chk gwauth "authMethod: payload.authMethod || payload.auth_method || 'email'," 1
chk gwauth "export function parseTestToken" 1
# --- proxy.ts: the mount counts (H-mounts)
chk proxy "requireScope(" 6
chk proxy "requireScopeOrRole(" 1
chk proxy "attachScopes," 8
chk proxy "import { requireScope, attachScopes, requireScopeOrRole } from '../middleware/scopes';" 1
chk proxy_d "requireScope(" 6
# --- the label's other consumers, the launder path, the role defaults
chk enforce "user.authMethod" 1
chk ratelim "'oauth_app'" 1
chk ratelim "'oauth'" absent
chk authr "authRoutes.post('/refresh'" 1
chk authr "const tokens = generateTokenPair(user, session.id);" 4
chk authr "client_id" absent
chk shscopes "export function getDefaultScopesForRole(" 1
# --- the tests
chk ks835a "  it(" 5
chk ks835a "listen(" 1
chk ks835a "await jwtMod.initJwtKeys();" 1
chk ks835a "scope: 'openid'" 1
chk ks835a "scope: ''" 1
chk ks835g "  it(" 6
chk ks835g "listen(" 1
chk ks835g "vi.stubGlobal('fetch', fetchMock);" 1
chk ks835g "const realFetch = globalThis.fetch;" 1
chk ks835g "enableTestTokens: false" 1
chk ks835g "The shape proxy.ts mounts eight times" 1
chk ks823 "  it(" 11
chk ks823 "expect(" 24
chk ks823_p "expect(" 24
chk ks823 "scopes: ['openid'] })" 8
chk ks823_p "scopes: ['openid'] })" absent
chk ks823 "listen(" 1
# --- the ks860 guard: the widened-guard rule re-derived over the three test files
cat > "$W/sim.py" <<'PY'
import re, sys
W = sys.argv[1]
SITE = re.compile(r"\.listen\(\s*0\s*(,|\))"); HOST = re.compile(r"^\s*(['\"])127\.0\.0\.1\1")
def offenders(src):
    out = []
    for m in SITE.finditer(src):
        rest = src[m.end():]
        if not (m.group(1) == ',' and HOST.match(rest)): out.append(src[:m.start()].count('\n') + 1)
    return out
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
for f in ["ks835a", "ks835g", "ks823"]:
    s = open(f"{W}/{f}", encoding="utf-8").read()
    ck(len(SITE.findall(s)) == 1 and offenders(s) == [], f"ks860 :433/:440 over {f}: 1 listen(0 site, offenders {offenders(s)} (expected [])")
g = open(f"{W}/ks835g", encoding="utf-8").read().replace("app.listen(0, '127.0.0.1', resolve)", "app.listen(0, resolve)")
ck(offenders(g) == [64], f"planted host-less control (the gateway test's :64 without the host) -> offenders {offenders(g)} (expected [64])")
sys.exit(1 if fails else 0)
PY
python3 "$W/sim.py" "$W" || FAILS=$((FAILS+1))
echo "work dir (kept): $W"
echo "controls_check: FAILS=$FAILS"
[ "$FAILS" -eq 0 ] && exit 0 || exit 1
