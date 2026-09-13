#!/bin/bash
# controls_check.sh — re-grep every §4 positive-control token of the #982 (KS-790) TIER-1 brief at the PINNED head e62eab87a and
# develop M18 8861e6216 through the GitHub contents API (read-only; GH_TOKEN sourced by NAME from the Secuura .env, never printed).
# Tokens were derived from #982's OWN files at this head and at develop, and from userRepo.ts / jwt.ts / migration 039 (untouched
# by the PR) — never carried from another gate's brief. PRESENT tokens must grep the stated count; ABSENT tokens exactly 0; the
# blobs / sizes / lines / sha256 must match TARGET; the named lines must read as quoted; the ks820 file at head must equal
# develop[:124] + 8 lines + develop[124:]; the oauth.ts CODE delta must be -4/+3 in exactly FOUR changed regions; the ks860
# loopback regexes over the new test file must read NO offender; userRepo.ts / jwt.ts / index.ts must be blob-identical at head
# and develop; the new test file must be ABSENT at develop.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD="${QA982_HEAD:-e62eab87a6263e25c41c9bb814d5831842bb6c7e}"
DEV="${QA982_DEVELOP:-8861e62161466c40f08d2b10a30edeb203123993}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
W="$(mktemp -d "${TMPDIR:-/tmp}/qa982ctl.XXXXXX")"
OAUTH='Blockchain/Dev/services/auth/src/routes/oauth.ts'
T790='Blockchain/Dev/services/auth/src/__tests__/ks790-token-pre-auth-user-lookup.test.ts'
T820='Blockchain/Dev/services/auth/src/__tests__/ks820-821-token-client-auth-and-apptype.test.ts'
UREPO='Blockchain/Dev/services/auth/src/repositories/userRepo.ts'
JWT='Blockchain/Dev/services/auth/src/services/jwt.ts'
INDEX='Blockchain/Dev/services/auth/src/index.ts'
M039='Blockchain/Dev/migrations/039_rls_fail_closed.sql'

fetch() { # path ref outfile -> prints blob sha, or ABSENT, or UNREADABLE
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
echo "controls_check.sh — head ${HEAD:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
for spec in "oauth:$OAUTH:$HEAD" "oauth_dev:$OAUTH:$DEV" "t790:$T790:$HEAD" "t820:$T820:$HEAD" "t820_dev:$T820:$DEV" "urepo:$UREPO:$HEAD" "urepo_dev:$UREPO:$DEV" "jwt:$JWT:$HEAD" "jwt_dev:$JWT:$DEV" "index:$INDEX:$HEAD" "index_dev:$INDEX:$DEV" "m039:$M039:$HEAD"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; ABSENT) echo "FAIL $n ABSENT at ${ref:0:9}"; FAILS=$((FAILS+1)); continue ;; esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
done
# the new test file must be ABSENT at develop
absent="$(fetch "$T790" "$DEV" "$W/t790_dev")"
[ "$absent" = "ABSENT" ] && echo "ok   t790 ABSENT at develop (HTTP 404 — the file is NEW)" || { echo "FAIL t790 at develop read: $absent (expected ABSENT)"; FAILS=$((FAILS+1)); }
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis oauth 80e05458e; blobis oauth_dev 4b03f555e; blobis t790 cfed82d54; blobis t820 b998b5b7d; blobis t820_dev 106c762f1
blobis urepo 822b3fcd8; blobis urepo_dev 822b3fcd8; blobis jwt d0d55c11b; blobis jwt_dev d0d55c11b; blobis index edabbf871; blobis index_dev edabbf871
for pair in "urepo:urepo_dev" "jwt:jwt_dev" "index:index_dev"; do a="${pair%%:*}"; b="${pair#*:}"; cmp -s "$W/$a" "$W/$b" && echo "ok   $a byte-identical at head and develop" || { echo "FAIL $a DIFFERS between head and develop"; FAILS=$((FAILS+1)); }; done
cmp -s "$W/oauth" "$W/oauth_dev" && { echo "FAIL oauth.ts byte-identical at head and develop"; FAILS=$((FAILS+1)); } || echo "ok   oauth.ts DIFFERS between head and develop (as it must)"
cmp -s "$W/t820" "$W/t820_dev" && { echo "FAIL ks820 byte-identical at head and develop"; FAILS=$((FAILS+1)); } || echo "ok   ks820 DIFFERS between head and develop (the one hunk)"
for pair in "oauth:fc54cc5f1494ad48" "oauth_dev:cc4f4ac0df1b3393" "t790:55c12270001fd653" "t820:d0883d41f8a38b96" "t820_dev:4f66d57fd174c85b" "urepo:24670fe3656152d2" "jwt:33545ba5a9c6951a" "index:5b75376a2bd29b8c"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(shasum -a 256 "$W/$f" | cut -c1-16)" = "$want" ] && echo "ok   $f sha256 $want" || { echo "FAIL $f sha256 is not $want"; FAILS=$((FAILS+1)); }
done
for pair in "oauth:1260" "oauth_dev:1242" "t790:249" "t820:377" "t820_dev:369" "urepo:1874" "jwt:374" "index:312" "m039:271"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -l < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want lines" || { echo "FAIL $f is not $want lines"; FAILS=$((FAILS+1)); }
done
for pair in "oauth:62763" "oauth_dev:61492" "t790:12429" "t820:18387" "t820_dev:17925" "urepo:83504" "jwt:13692" "index:12509"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -c < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want bytes" || { echo "FAIL $f is not $want bytes"; FAILS=$((FAILS+1)); }
done
lineis() { # file line expected-text
  local got; got="$(sed -n "${2}p" "$W/$1")"
  [ "$got" = "$3" ] && echo "ok   $1:$2 = $3" || { echo "FAIL $1:$2 is: $got"; FAILS=$((FAILS+1)); }
}
# --- oauth.ts at head: the lines the brief cites
lineis oauth 29 "import { generateTokenPair, verifyRefreshToken } from '../services/jwt';"
lineis oauth 628 "    const gate = await enforcePasswordLoginGates({"
lineis oauth 711 "oauthRouter.post('/token', async (req: Request, res: Response) => {"
lineis oauth 808 "      const user = await userRepo.getUserByIdPreAuth(result.userId);"
lineis oauth 809 "      if (!user) {"
lineis oauth 820 "      logger.info('OAuth token issued', { clientId: client_id, userId: user.id, scope: result.scope });"
lineis oauth 836 "      // Verify and rotate refresh token. verifyRefreshToken THROWS"
lineis oauth 843 "      // used to be a \`require('../services/jwt')\` on this line — redundant with"
lineis oauth 849 "      let decoded;"
lineis oauth 851 "        decoded = verifyRefreshToken(refresh_token);"
lineis oauth 860 "      if (decoded.jti && (await isRefreshJtiDenylisted(decoded.jti))) {"
lineis oauth 867 "      const user = await userRepo.getUserByIdPreAuth(decoded.userId);"
lineis oauth 868 "      if (!user || user.status !== 'ACTIVE') {"
lineis oauth 890 "    logger.error('OAuth token error', { error: error.message });"
# --- oauth.ts at develop: the three sites
lineis oauth_dev 799 "      const user = await userRepo.getUserById(result.userId);"
lineis oauth_dev 832 "      const { verifyRefreshToken } = require('../services/jwt');"
lineis oauth_dev 833 "      let decoded;"
lineis oauth_dev 834 "      try {"
lineis oauth_dev 849 "      const user = await userRepo.getUserById(decoded.userId);"
lineis oauth_dev 800 "      if (!user) {"
# --- the new test file
lineis t790 138 "  server = app.listen(0, '127.0.0.1');"
lineis t790 197 "  world.plainLookup = null; world.preAuthLookup = { ...ACTIVE_USER };"
lineis t790 208 "    expect(world.calls.getUserById).toEqual([]); // the RLS-scoped lookup is not consulted on this pre-auth path"
# --- ks820 at head: the inserted mock entry
lineis t820 129 "  getUserByIdPreAuth: vi.fn(async () => ({"
# --- userRepo / jwt / 039
lineis urepo 403 "export async function getUserById(id: string, tenantId?: string): Promise<User | null> {"
lineis urepo 505 "export async function getUserByIdPreAuth(id: string): Promise<User | null> {"
lineis urepo 507 "    const result = await query(\`SELECT \${USER_COLS} FROM auth_find_user_by_id(\$1)\`, [id]);"
lineis jwt 346 "export function verifyRefreshToken(token: string): JwtPayload {"
lineis m039 199 "CREATE OR REPLACE FUNCTION auth_find_user_by_id(p_id UUID)"
lineis m039 200 "RETURNS SETOF users LANGUAGE sql SECURITY DEFINER SET search_path = public STABLE"
lineis index 102 "app.use(tenantGucContext());"
lineis index 115 "app.use('/api/oauth', oauthRouter);"
chk() { # file token mode(present|absent|N)
  local f="$1" tok="$2" mode="$3" c
  c="$(/usr/bin/grep -c -F -- "$tok" "$W/$f")"
  if [ "$mode" = present ] && [ "$c" -ge 1 ]; then echo "ok   $f  present x$c  $tok"
  elif [ "$mode" = absent ] && [ "$c" -eq 0 ]; then echo "ok   $f  absent      $tok"
  elif [ "$mode" != present ] && [ "$mode" != absent ] && [ "$c" -eq "$mode" ]; then echo "ok   $f  exactly x$c $tok"
  else echo "FAIL $f  $mode expected, count $c: $tok"; FAILS=$((FAILS+1)); fi
}
# --- oauth.ts at head: the tamper anchors and the develop world absent
chk oauth "userRepo.getUserByIdPreAuth(result.userId)" 1
chk oauth "userRepo.getUserByIdPreAuth(decoded.userId)" 1
chk oauth "userRepo.getUserById(" absent
chk oauth "const { verifyRefreshToken } = require(" absent
chk oauth "require('../services/jwt')" 1
chk oauth "decoded = verifyRefreshToken(refresh_token);" 1
chk oauth "if (!user || user.status !== 'ACTIVE')" 1
chk oauth "description: 'User not found'" 1
chk oauth "description: 'User inactive or not found'" 1
chk oauth "description: 'Invalid refresh token'" 1
chk oauth "description: 'Refresh token revoked'" 1
chk oauth "enforcePasswordLoginGates({" 1
chk oauth "oauthRouter.post('/token'" 1
chk oauth "seedTenantGuc" 7
chk oauth "message: 'server_error'" 3
chk oauth "KS-790" 3
chk oauth "generateTokenPair(user, session.id)" 2
# --- oauth.ts at develop
chk oauth_dev "userRepo.getUserById(result.userId)" 1
chk oauth_dev "userRepo.getUserById(decoded.userId)" 1
chk oauth_dev "const { verifyRefreshToken } = require('../services/jwt');" 1
chk oauth_dev "import { generateTokenPair } from '../services/jwt';" 1
chk oauth_dev "getUserByIdPreAuth" absent
chk oauth_dev "KS-790" absent
chk oauth_dev "enforcePasswordLoginGates({" 1
# --- the new test file
chk t790 "app.listen(0, '127.0.0.1')" 1
chk t790 "listen(" 1
chk t790 "vi.mock('../services/jwt'" 1
chk t790 "vi.mock('../repositories/userRepo'" 1
chk t790 "vi.mock('../db'" 1
chk t790 "getUserByIdPreAuth: vi.fn(" 1
chk t790 "expect(world.calls.getUserById).toEqual([]);" 3
chk t790 "expect(world.calls.getUserByIdPreAuth).toEqual([ACTIVE_USER.id]);" 2
chk t790 "  it('" 6
chk t790 "  it('CONTROL" 4
chk t790 "status: 'SUSPENDED'" 1
chk t790 "'not-the-secret'" 1
chk t790 "toMatch(/User not found/)" 1
chk t790 "toMatch(/User inactive or not found/)" 2
chk t790 "net.connect(" 1
chk t790 "toContain('MINTED_790')" 2
chk t790 "'VALID_REFRESH_790'" 2
chk t790 "expect(r.status).toBe(401);" 1
chk t790 "require(" absent
# --- ks820 at head and develop
chk t820 "getUserByIdPreAuth: vi.fn(async () => ({" 1
chk t820 "getUserById: vi.fn(async () => ({" 1
chk t820 "  it('" 13
chk t820 "KS-790" 1
chk t820_dev "getUserByIdPreAuth" absent
chk t820_dev "  it('" 13
# --- the untouched dependencies
chk urepo "FROM auth_find_user_by_id(\$1)" 2
chk urepo "throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');" 6
chk jwt "export function generateTokenPair(user: User, sessionId: string): {" 1
chk jwt "import" present
chk jwt "routes/" absent
chk m039 "SECURITY DEFINER" 10
chk m039 "'auth_find_user_by_id(UUID)'," 1
chk index "app.use(errorHandler);" 1
# --- the shapes re-derived in Python: the ks820 insertion, the oauth.ts CODE delta, the ks860 regexes over the new file
cat > "$W/sim.py" <<'PY'
import re, sys, difflib
W = sys.argv[1]
oh = open(f"{W}/oauth", encoding="utf-8").read(); od = open(f"{W}/oauth_dev", encoding="utf-8").read()
kh = open(f"{W}/t820", encoding="utf-8").read().split('\n'); kd = open(f"{W}/t820_dev", encoding="utf-8").read().split('\n')
t = open(f"{W}/t790", encoding="utf-8").read()
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
ck(kh[:124] == kd[:124] and kh[132:] == kd[124:] and len(kh) == len(kd) + 8, "ks820@head == develop[:124] + 8 lines + develop[124:] (ONE inserted hunk, nothing else)")
ck(kh[128].strip() == "getUserByIdPreAuth: vi.fn(async () => ({" and all(l.strip().startswith('//') for l in kh[124:128]), "the inserted 8 = 4 comment lines + the one mock entry")
sm = difflib.SequenceMatcher(None, od.split('\n'), oh.split('\n'), autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
ck(len(ops) == 4, f"oauth.ts develop -> head: {len(ops)} changed regions (expected 4): {[(o[0], o[1]+1, o[2], o[3]+1, o[4]) for o in ops]}")
minus = [l for o in ops for l in od.split('\n')[o[1]:o[2]]]; plus = [l for o in ops for l in oh.split('\n')[o[3]:o[4]]]
cm = [l.strip() for l in minus if not l.strip().startswith('//')]; cp = [l.strip() for l in plus if not l.strip().startswith('//')]
ck(cm == ["import { generateTokenPair } from '../services/jwt';", "const user = await userRepo.getUserById(result.userId);", "const { verifyRefreshToken } = require('../services/jwt');", "const user = await userRepo.getUserById(decoded.userId);"], f"CODE removed ({len(cm)}): {cm}")
ck(cp == ["import { generateTokenPair, verifyRefreshToken } from '../services/jwt';", "const user = await userRepo.getUserByIdPreAuth(result.userId);", "const user = await userRepo.getUserByIdPreAuth(decoded.userId);"], f"CODE added ({len(cp)}): {cp}")
ck(len(minus) == 5 and len(plus) == 23, f"raw lines -{len(minus)} +{len(plus)} (expected -5 +23)")
SITE = re.compile(r"\.listen\(\s*0\s*(,|\))"); HOST = re.compile(r"^\s*(['\"])127\.0\.0\.1\1")
def offenders(src):
    out = []
    for m in SITE.finditer(src):
        rest = src[m.end():]
        if not (m.group(1) == ',' and HOST.match(rest)): out.append(src[:m.start()].count('\n') + 1)
    return out
ck(offenders(t) == [], f"ks860 :433/:440 over the new test file -> offenders {offenders(t)} (expected [])")
ck(offenders("const s = app.listen(0);") == [1] and offenders("const s = app.listen(0, '127.0.0.1');") == [], "guard controls: bare listen(0) -> 1 offender; the shipped spelling -> 0")
for name, src in [("oauth@head", oh), ("oauth@develop", od), ("t790", t)]:
    b = src.encode('utf-8'); n = sum(1 for x in b if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)
    ck(n == 0, f"{name}: 0 raw control bytes (got {n})")
sys.exit(1 if fails else 0)
PY
python3 "$W/sim.py" "$W" || FAILS=$((FAILS+1))
echo "work dir (kept): $W"
echo "controls_check: FAILS=$FAILS"
[ "$FAILS" -eq 0 ] && exit 0 || exit 1
