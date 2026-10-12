#!/bin/bash
# create_kintsugi_qa_login.sh — create the Kintsugi QA login (role ORG_ADMIN), bound to one organisation.
#
# Built by Seat V 6th (Secuura / Platform K), 2026-10-13, to Wednesday's spec. Kam runs it from his own terminal.
# By DEFAULT it logs in FOR him: it asks for his admin email and password (hidden), and for his authenticator
# code if the account has two-factor sign-in (hidden). An access token can only come from an account logging in;
# nobody can mint one for another identity, so this is the way to "generate the token".
#
# SECRETS: the admin email/password, the MFA code, every access token, and the QA login's password live ONLY in
# shell variables for the run. None is printed, logged, written to disk, or put on any command line: curl reads
# its whole request (headers and body) from stdin (`curl -K -`). They are unset on any exit.
#
# Requires: bash 3.2+, curl, python3.
#
# Usage:
#   ./create_kintsugi_qa_login.sh [--base-url URL] [--creds-file FILE] [--project-env FILE] [--org UUID]
#                                 [--token-from-env] [--dry-run] [--skip-owner-control]
#                                 [--platform-default-tenant-ok]
#     --token-from-env   use an admin token already in the environment variable KQA_ADMIN_TOKEN, instead of
#                        logging in (for an operator who prefers to fetch the token himself)
#
# Exit codes:
#   0 success                         10 bad arguments / missing tool      11 credentials file problem
#  12 admin sign-in / token problem   13 organisation pre-check failed     14 tenant mismatch (refused)
#  15 create refused                  16 attach-organisation refused       17 QA login cannot be used
#  18 key list check FAILED           19 OWNER negative control did not behave as expected
#  20 network / unexpected response
set -u

BASE_URL="https://kintsugi.secuura.net"
CREDS_FILE="/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env"
PROJECT_ENV="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
ORG_ID=""
DRY_RUN=0
SKIP_OWNER=0
PLATFORM_OK=0
TOKEN_FROM_ENV=0
DEFAULT_TENANT="a0000000-0000-4000-8000-000000000001"   # auth's DEFAULT_TENANT_ID (userRepo.ts:32)

# every secret-bearing variable, so the trap can clear them all
ADMIN_EMAIL=""; ADMIN_PW=""; MFA_CODE=""; ADMIN_TOKEN=""; NEW_TOKEN=""; OWN_TOKEN=""
QA_EMAIL=""; QA_PW=""; OWN_EMAIL=""; OWN_PW=""; HTTP_BODY=""; HTTP_CODE=""; BODY=""
wipe() { ADMIN_EMAIL=""; ADMIN_PW=""; MFA_CODE=""; ADMIN_TOKEN=""; NEW_TOKEN=""; OWN_TOKEN=""
         QA_PW=""; OWN_PW=""; HTTP_BODY=""; BODY=""
         unset ADMIN_EMAIL ADMIN_PW MFA_CODE ADMIN_TOKEN NEW_TOKEN OWN_TOKEN QA_PW OWN_PW HTTP_BODY BODY KQA_ADMIN_TOKEN; }
trap 'wipe' EXIT
trap 'wipe; printf "\n[ABORTED]\n" >&2; exit 130' INT TERM

say()  { printf '%s\n' "$*"; }
step() { printf '[%s] %s\n' "$1" "$2"; }
die()  { printf '[FAIL] %s\n' "$2" >&2; exit "$1"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --base-url) BASE_URL="${2:-}"; shift 2 ;;
    --creds-file) CREDS_FILE="${2:-}"; shift 2 ;;
    --project-env) PROJECT_ENV="${2:-}"; shift 2 ;;
    --org) ORG_ID="${2:-}"; shift 2 ;;
    --token-from-env) TOKEN_FROM_ENV=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --skip-owner-control) SKIP_OWNER=1; shift ;;
    --platform-default-tenant-ok) PLATFORM_OK=1; shift ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) die 10 "unknown argument: $1 (see --help)" ;;
  esac
done
BASE_URL="${BASE_URL%/}"
command -v curl >/dev/null 2>&1 || die 10 "curl is required"
command -v python3 >/dev/null 2>&1 || die 10 "python3 is required"

# ---- read KEY=VALUE from an env file WITHOUT sourcing it (sourcing can execute words in it) ----
env_get() {  # $1 file, $2 key -> value on stdout (callers capture it into a variable; never echoed)
  python3 - "$1" "$2" <<'PY'
import sys
path, key = sys.argv[1], sys.argv[2]
try:
    lines = open(path, encoding="utf-8").read().splitlines()
except OSError:
    sys.exit(3)
val = None
for ln in lines:
    s = ln.strip()
    if not s or s.startswith("#") or "=" not in s:
        continue
    if s.startswith("export "):
        s = s[7:].lstrip()
    k, v = s.split("=", 1)
    if k.strip() == key:
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        val = v
if val is None or val == "":
    sys.exit(4)
sys.stdout.write(val)
PY
}
mask_email() { printf '%s' "$1" | python3 -c 'import sys
e=sys.stdin.read(); u,_,d=e.partition("@"); print((u[:1]+"***@"+d) if d else "***")'; }

# ---- build a JSON body: key names on argv (not secret), values on stdin one per line (may be secret) ----
mkbody() {
  python3 -c 'import json, sys
keys = sys.argv[1:]
vals = [sys.stdin.readline().rstrip("\n") for _ in keys]
print(json.dumps(dict(zip(keys, vals)), separators=(",", ":")))' "$@"
}
# ---- read one dotted path out of the JSON in HTTP_BODY (body on stdin, path on argv) ----
jget() { printf '%s' "$HTTP_BODY" | python3 -c 'import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
for p in sys.argv[1].split("."):
    if isinstance(d, dict) and p in d: d = d[p]
    elif isinstance(d, list) and p.isdigit() and int(p) < len(d): d = d[int(p)]
    else: sys.exit(0)
if isinstance(d, (dict, list)): print(json.dumps(d))
elif d is not None: print(d)' "$1"; }
jlen() { printf '%s' "$HTTP_BODY" | python3 -c 'import json, sys
try:
    d = json.load(sys.stdin)
    for p in sys.argv[1].split("."): d = d[p]
    print(len(d) if isinstance(d, list) else -1)
except Exception:
    print(-1)' "$1"; }
errmsg() { printf '%s' "$HTTP_BODY" | python3 -c 'import json, sys
try:
    d = json.load(sys.stdin); e = d.get("error") if isinstance(d, dict) else None
    m = (e.get("message") if isinstance(e, dict) else e) or d.get("message") or ""
    print(str(m)[:200])
except Exception:
    print("(non-JSON response)")'; }
errcode() { printf '%s' "$HTTP_BODY" | python3 -c 'import json, sys
try:
    d = json.load(sys.stdin); e = d.get("error") if isinstance(d, dict) else None
    print(e.get("code", "") if isinstance(e, dict) else "")
except Exception:
    print("")'; }
# ---- decode one claim of a JWT WITHOUT verifying it (display + routing only; the server verifies). Token on stdin ----
jwt_claim() { printf '%s' "$1" | python3 -c 'import base64, json, sys
parts = sys.stdin.read().strip().split(".")
if len(parts) != 3: sys.exit(2)
p = parts[1] + "=" * (-len(parts[1]) % 4)
try:
    c = json.loads(base64.urlsafe_b64decode(p.encode()))
except Exception:
    sys.exit(2)
v = c.get(sys.argv[1])
if v is not None: print(v)' "$2"; }

# ---- the one HTTP primitive. curl reads its WHOLE request from stdin, so neither the token nor the body is ever
#      on a command line or on disk. Sets HTTP_CODE and HTTP_BODY. ----
cfgq() { local s="$1"; s="${s//\\/\\\\}"; s="${s//\"/\\\"}"; printf '%s' "$s"; }
http() {  # $1 METHOD  $2 path  $3 token-or-""  $4 json-body-or-""
  local method="$1" path="$2" tok="$3" body="$4"
  if [ "$DRY_RUN" = "1" ]; then
    local shown=""
    if [ -n "$body" ]; then
      shown="$(printf '%s' "$body" | python3 -c 'import json, sys
d = json.load(sys.stdin)
for k in ("password", "mfaCode"):
    if k in d: d[k] = "***"
if "email" in d:
    u, _, dom = d["email"].partition("@"); d["email"] = (u[:1] + "***@" + dom) if dom else "***"
print(json.dumps(d, separators=(",", ":")))')"
    fi
    say "    DRY-RUN would send: $method ${BASE_URL}${path}${tok:+   [Authorization: Bearer ***]}${shown:+   body: $shown}"
    HTTP_CODE="000"; HTTP_BODY="{}"; return 0
  fi
  local cfg out
  cfg="silent
max-time = 30
request = \"$method\"
url = \"$(cfgq "${BASE_URL}${path}")\"
header = \"Content-Type: application/json\"
header = \"Accept: application/json\""
  [ -n "$tok" ] && cfg="$cfg
header = \"Authorization: Bearer $(cfgq "$tok")\""
  [ -n "$body" ] && cfg="$cfg
data-binary = \"$(cfgq "$body")\""
  cfg="$cfg
write-out = \"\\n%{http_code}\""
  out="$(printf '%s\n' "$cfg" | curl -K - 2>/dev/null)" || out=$'\n000'
  cfg=""
  HTTP_CODE="${out##*$'\n'}"
  HTTP_BODY="${out%$'\n'*}"
  [ "$HTTP_BODY" = "$out" ] && HTTP_BODY=""
}

# ======================================================================================================
say "Kintsugi QA login — create an ORG_ADMIN bound to one organisation   (base: $BASE_URL)"
[ "$DRY_RUN" = "1" ] && say "DRY RUN: nothing will be sent; every call is printed with its secrets masked."

# ---- step 1: the QA login's own credentials, from the credentials file (never printed) ----
QA_EMAIL="$(env_get "$CREDS_FILE" KINTSUGI_QA_ORGADMIN_EMAIL)" || die 11 "KINTSUGI_QA_ORGADMIN_EMAIL is missing or empty in $CREDS_FILE"
QA_PW="$(env_get "$CREDS_FILE" KINTSUGI_QA_ORGADMIN_PASSWORD)" || die 11 "KINTSUGI_QA_ORGADMIN_PASSWORD is missing or empty in $CREDS_FILE"
step 1 "credentials read from the file for $(mask_email "$QA_EMAIL") (the password is not shown)"

# ---- step 2: the organisation ----
if [ -z "$ORG_ID" ]; then
  printf 'Organisation id (UUID) to bind the QA login to: '
  IFS= read -r ORG_ID || die 10 "no organisation id given"
fi
ORG_ID="$(printf '%s' "$ORG_ID" | tr -d '[:space:]' | tr 'A-F' 'a-f')"
printf '%s' "$ORG_ID" | grep -Eq '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' \
  || die 10 "that is not a UUID: the organisation id must look like 11111111-2222-4333-8444-555555555555"
step 2 "organisation $ORG_ID"

# ---- step 3: the ADMIN session — sign in for him (default), or a token from the environment ----
if [ "$TOKEN_FROM_ENV" = "1" ]; then
  ADMIN_TOKEN="${KQA_ADMIN_TOKEN:-}"; unset KQA_ADMIN_TOKEN
  ADMIN_TOKEN="$(printf '%s' "$ADMIN_TOKEN" | tr -d '[:space:]')"; ADMIN_TOKEN="${ADMIN_TOKEN#Bearer}"
  [ -n "$ADMIN_TOKEN" ] || die 12 "--token-from-env was given but KQA_ADMIN_TOKEN is empty"
  step 3 "admin token taken from the environment (not shown)"
else
  printf 'Your ADMIN email for %s (input hidden): ' "$BASE_URL"
  IFS= read -rs ADMIN_EMAIL || die 12 "no admin email given"; printf '\n'
  printf 'Your ADMIN password (input hidden): '
  IFS= read -rs ADMIN_PW || die 12 "no admin password given"; printf '\n'
  ADMIN_EMAIL="$(printf '%s' "$ADMIN_EMAIL" | tr -d '[:space:]')"
  [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PW" ] || die 12 "both the admin email and password are needed"
  BODY="$(printf '%s\n%s\n' "$ADMIN_EMAIL" "$ADMIN_PW" | mkbody email password)"
  http POST "/api/auth/login" "" "$BODY"
  if [ "$DRY_RUN" != "1" ] && [ "$HTTP_CODE" = "403" ] && [ "$(errcode)" = "MFA_REQUIRED" ]; then
    step 3 "your account uses two-factor sign-in"
    printf 'Code from your authenticator app (input hidden): '
    IFS= read -rs MFA_CODE || die 12 "no code given"; printf '\n'
    MFA_CODE="$(printf '%s' "$MFA_CODE" | tr -d '[:space:]-')"
    printf '%s' "$MFA_CODE" | grep -Eq '^[0-9A-Za-z]{6,8}$' || die 12 "that code is not 6-8 letters or digits; nothing more was sent"
    BODY="$(printf '%s\n%s\n%s\n' "$ADMIN_EMAIL" "$ADMIN_PW" "$MFA_CODE" | mkbody email password mfaCode)"
    MFA_CODE=""
    http POST "/api/auth/login" "" "$BODY"
    BODY=""
    [ "$HTTP_CODE" = "200" ] || die 12 "the two-factor code was refused (HTTP $HTTP_CODE: $(errmsg)). Not retried: repeated failures lock the account out."
  fi
  BODY=""; ADMIN_PW=""
  if [ "$DRY_RUN" = "1" ]; then
    say "    DRY-RUN: if the account uses two-factor sign-in, the same login is re-sent with \"mfaCode\":\"***\""
  else
    case "$HTTP_CODE" in
      200) ;;
      401) die 12 "your admin email or password was refused (401). Not retried: repeated failures lock the account out." ;;
      403) die 12 "sign-in refused (403): $(errmsg)" ;;
      000) die 20 "could not reach $BASE_URL" ;;
      *)   die 12 "sign-in failed: HTTP $HTTP_CODE $(errmsg)" ;;
    esac
    ADMIN_TOKEN="$(jget data.accessToken)"; HTTP_BODY=""
    [ -n "$ADMIN_TOKEN" ] || die 12 "signed in (200) but the answer carried no data.accessToken"
    step 3 "signed in as $(mask_email "$ADMIN_EMAIL")"
  fi
  ADMIN_EMAIL=""
fi

if [ "$DRY_RUN" = "1" ] && [ -z "$ADMIN_TOKEN" ]; then
  ROLE_UP="UNKNOWN"; TENANT=""; CALLER_KIND="unknown"
  say "    DRY-RUN: no token, so the role is unknown; both the tenant-admin and platform-admin calls are shown below"
else
  ROLE="$(jwt_claim "$ADMIN_TOKEN" role)" || die 12 "that does not look like an access token (it should be three dot-separated parts)"
  TENANT="$(jwt_claim "$ADMIN_TOKEN" tenantId)"
  EXP="$(jwt_claim "$ADMIN_TOKEN" exp)"
  ROLE_UP="$(printf '%s' "$ROLE" | tr 'a-z' 'A-Z')"
  step 3 "admin role ${ROLE_UP:-?}, tenant ${TENANT:-<none>}"
  if [ -n "$EXP" ] && [ "$(date +%s)" -ge "${EXP%%.*}" ] 2>/dev/null; then
    die 12 "the admin token has EXPIRED; sign in again"
  fi
  case "$ROLE_UP" in
    ORG_ADMIN) CALLER_KIND="tenant" ;;
    SYSTEM_ADMIN|SUPER_ADMIN) CALLER_KIND="platform" ;;
    *) die 12 "role ${ROLE_UP:-?} cannot create users here; you need ORG_ADMIN, SYSTEM_ADMIN or SUPER_ADMIN" ;;
  esac
  if [ "$CALLER_KIND" = "tenant" ] && [ -z "$TENANT" ]; then
    die 12 "your ORG_ADMIN token carries no tenant, so the server would refuse with 'Tenant context required'"
  fi
fi

# ---- step 4: pre-checks BEFORE anything is created ----
# 4a: the organisation must have at least one key visible to the caller. This makes a later '200 with zero keys'
#     for the NEW user unambiguous: it can then only mean a tenant mismatch.
http GET "/api/security/keys?organizationId=$ORG_ID" "$ADMIN_TOKEN" ""
if [ "$DRY_RUN" != "1" ]; then
  case "$HTTP_CODE" in
    200) n="$(jlen data)"
         if [ "$CALLER_KIND" = "tenant" ]; then
           [ "$n" -ge 1 ] 2>/dev/null || die 13 "REFUSED before creating anything: you see NO keys for organisation $ORG_ID ($n). As an ORG_ADMIN you only see your own tenant ($TENANT), so either the organisation is in ANOTHER tenant (the new user would be stranded there) or it has no API keys. Use an ORG_ADMIN of its own tenant, or pick an organisation that has keys."
         else
           [ "$n" -ge 1 ] 2>/dev/null || die 13 "REFUSED before creating anything: organisation $ORG_ID has NO keys ($n). Pick an organisation that has API keys (step 2 of STEPS.md)."
         fi
         step 4a "the organisation has $n key(s) visible to you" ;;
    401) die 12 "the server rejected the admin token (401): $(errmsg)" ;;
    403) die 12 "the admin role may not list keys (403): $(errmsg)" ;;
    *)   die 20 "unexpected answer listing the organisation's keys: HTTP $HTTP_CODE $(errmsg)" ;;
  esac
fi
# 4b: the TENANT. The new user is created in the caller's tenant (tenant admin) or the platform default tenant
#     (platform admin), and the API can never move it afterwards.
if [ "$CALLER_KIND" = "tenant" ] || [ "$CALLER_KIND" = "unknown" ]; then
  [ "$CALLER_KIND" = "unknown" ] && say "    (tenant admins only:)"
  http GET "/api/users/admin/organizations" "$ADMIN_TOKEN" ""
  if [ "$DRY_RUN" != "1" ]; then
    EXPECT_TENANT="$TENANT"
    [ "$HTTP_CODE" = "200" ] || die 13 "could not list your tenant's organisations: HTTP $HTTP_CODE $(errmsg)"
    found="$(printf '%s' "$HTTP_BODY" | python3 -c 'import json, sys
d = json.load(sys.stdin); orgs = (d.get("data") or {}).get("organizations") or []
print("yes" if any(str(o.get("id", "")).lower() == sys.argv[1] for o in orgs) else "no")' "$ORG_ID")"
    [ "$found" = "yes" ] || die 14 "REFUSED: organisation $ORG_ID is not in YOUR tenant ($TENANT). The new user would land in your tenant and could never be moved. Use an ORG_ADMIN of the organisation's own tenant."
    step 4b "the organisation is in your tenant ($TENANT), so the new user will match it"
  fi
fi
if [ "$CALLER_KIND" = "platform" ]; then
  EXPECT_TENANT="$DEFAULT_TENANT"
  if [ "$PLATFORM_OK" != "1" ]; then
    die 14 "REFUSED: you are a PLATFORM admin, so the new user would land in tenant $DEFAULT_TENANT, and NO API route reveals which tenant organisation $ORG_ID is in, so this script cannot check they match. Safe options: (a) run this as an ORG_ADMIN of the organisation's own tenant; or (b) if you KNOW the organisation is in tenant $DEFAULT_TENANT, re-run with --platform-default-tenant-ok (the key check at the end will still catch a mismatch)."
  fi
  step 4b "WARNING: platform admin; the new user lands in tenant $DEFAULT_TENANT. You asserted the organisation is in it (--platform-default-tenant-ok); step 8 verifies."
fi
[ "$CALLER_KIND" = "unknown" ] && say "    (platform admins: no extra call; refused unless --platform-default-tenant-ok)"

# ---- step 5: create the user (idempotent on 409) ----
BODY="$(printf '%s\n%s\nQA\nOrgAdmin\nORG_ADMIN\n' "$QA_EMAIL" "$QA_PW" | mkbody email password firstName lastName role)"
http POST "/api/users/admin/create" "$ADMIN_TOKEN" "$BODY"
BODY=""
NEW_ID=""; REUSED=0
if [ "$DRY_RUN" != "1" ]; then
  case "$HTTP_CODE" in
    201) NEW_ID="$(jget data.id)"
         [ -n "$NEW_ID" ] || die 20 "created (201) but the response carried no user id"
         step 5 "created the QA login, user id $NEW_ID" ;;
    409) qe="$(printf '%s' "$QA_EMAIL" | python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read(), safe=""))')"
         http GET "/api/users/lookup?email=$qe" "$ADMIN_TOKEN" ""
         [ "$HTTP_CODE" = "200" ] || die 15 "the QA login already exists (409) but it is NOT in your tenant, or cannot be looked up (HTTP $HTTP_CODE: $(errmsg)). It cannot be reused from here."
         NEW_ID="$(jget data.userId)"     # lookup answers data.userId (auth users.ts:333)
         ex_t="$(jget data.tenantId)"
         [ -n "$NEW_ID" ] || die 20 "lookup answered 200 but carried no user id"
         [ "$ex_t" = "$EXPECT_TENANT" ] || die 14 "REFUSED: the QA login already exists in tenant ${ex_t:-?}, not $EXPECT_TENANT. The API cannot move it; it needs a deploy-seat fix or a different email."
         REUSED=1
         step 5 "the QA login already exists (409): reusing user id $NEW_ID in tenant $ex_t (idempotent)" ;;
    403) die 15 "create refused (403): $(errmsg)" ;;
    400) die 15 "create refused (400): $(errmsg)" ;;
    401) die 12 "the server rejected the admin token (401): $(errmsg)" ;;
    *)   die 20 "unexpected answer to create: HTTP $HTTP_CODE $(errmsg)" ;;
  esac
else
  NEW_ID="<new-user-id>"
  say "    (on 409 only:) GET /api/users/lookup?email=*** then the QA login's password is checked by a login BEFORE anything is changed"
fi

# ---- step 5b: on a REUSED login, prove its password BEFORE changing anything about that user ----
if [ "$DRY_RUN" != "1" ] && [ "$REUSED" = "1" ]; then
  BODY="$(printf '%s\n%s\n' "$QA_EMAIL" "$QA_PW" | mkbody email password)"
  http POST "/api/auth/login" "" "$BODY"; BODY=""; HTTP_BODY=""
  case "$HTTP_CODE" in
    200) step 5b "the existing login's password matches the credentials file; safe to update it" ;;
    401) die 17 "REFUSED, NOTHING CHANGED: the QA login ALREADY EXISTED and its password does not match the credentials file. This script never resets passwords or touches an account it cannot log in as; reset it through an admin or use a new email." ;;
    *)   die 17 "REFUSED, NOTHING CHANGED: could not verify the existing login (HTTP $HTTP_CODE)" ;;
  esac
fi

# ---- step 6: attach the organisation (and re-assert the role, which makes a 409 rerun idempotent) ----
BODY="$(printf '%s\nORG_ADMIN\n' "$ORG_ID" | mkbody organizationId role)"
http PATCH "/api/users/admin/$NEW_ID" "$ADMIN_TOKEN" "$BODY"; BODY=""
if [ "$DRY_RUN" != "1" ]; then
  case "$HTTP_CODE" in
    200) step 6 "organisation attached (role ORG_ADMIN confirmed)" ;;
    400) die 16 "attach refused (400): $(errmsg)  — 'Invalid organizationId' means the organisation is not in your tenant" ;;
    403|404) die 16 "attach refused (HTTP $HTTP_CODE): $(errmsg)" ;;
    *)   die 20 "unexpected answer to attach: HTTP $HTTP_CODE $(errmsg)" ;;
  esac
fi
ADMIN_TOKEN=""   # the admin token is not needed again

# ---- step 7: log in AS the new user (its token carries the organisation only if minted after step 6) ----
BODY="$(printf '%s\n%s\n' "$QA_EMAIL" "$QA_PW" | mkbody email password)"
http POST "/api/auth/login" "" "$BODY"; BODY=""
if [ "$DRY_RUN" != "1" ]; then
  [ "$HTTP_CODE" = "200" ] || die 17 "login as the new user failed: HTTP $HTTP_CODE $(errmsg)"
  NEW_TOKEN="$(jget data.accessToken)"; HTTP_BODY=""
  [ -n "$NEW_TOKEN" ] || die 17 "login answered 200 but carried no data.accessToken"
  step 7 "logged in as the new user: role $(jwt_claim "$NEW_TOKEN" role), tenant $(jwt_claim "$NEW_TOKEN" tenantId), organisation $(jwt_claim "$NEW_TOKEN" organizationId)"
fi

# ---- step 8: the proof — the new user lists the organisation's keys, and the list is NOT empty ----
http GET "/api/security/keys?organizationId=$ORG_ID" "$NEW_TOKEN" ""
if [ "$DRY_RUN" != "1" ]; then
  case "$HTTP_CODE" in
    200) n="$(jlen data)"
         if [ "$n" -ge 1 ] 2>/dev/null; then
           step 8 "PASS: the new user lists $n key(s) for the organisation"
         else
           die 18 "FAILED: 200 with an EMPTY list. Step 4a proved the organisation HAS keys, so this means the new user (tenant $(jwt_claim "$NEW_TOKEN" tenantId)) is NOT in the organisation's tenant. The API cannot move it. Tell Wednesday; do not record these credentials."
         fi ;;
    403) die 18 "FAILED: the new user was refused the key list (403): $(errmsg)" ;;
    *)   die 20 "unexpected answer to the key list: HTTP $HTTP_CODE $(errmsg)" ;;
  esac
fi
NEW_TOKEN=""

# ---- step 9: optional negative control — the existing OWNER QA login must get 403 on the same call ----
if [ "$SKIP_OWNER" = "1" ]; then
  step 9 "OWNER negative control skipped (--skip-owner-control)"
elif ! OWN_EMAIL="$(env_get "$PROJECT_ENV" KINTSUGI_QA_GATE_OWNER_EMAIL 2>/dev/null)"; then
  step 9 "OWNER negative control skipped: KINTSUGI_QA_GATE_OWNER_EMAIL is not in $PROJECT_ENV"
elif ! OWN_PW="$(env_get "$PROJECT_ENV" KINTSUGI_QA_GATE_OWNER_PASSWORD 2>/dev/null)"; then
  step 9 "OWNER negative control skipped: its password is not in $PROJECT_ENV"
else
  BODY="$(printf '%s\n%s\n' "$OWN_EMAIL" "$OWN_PW" | mkbody email password)"; OWN_PW=""
  http POST "/api/auth/login" "" "$BODY"; BODY=""
  if [ "$DRY_RUN" != "1" ]; then
    [ "$HTTP_CODE" = "200" ] || die 19 "OWNER control: its login failed (HTTP $HTTP_CODE); the control could not run"
    OWN_TOKEN="$(jget data.accessToken)"; HTTP_BODY=""
  fi
  http GET "/api/security/keys?organizationId=$ORG_ID" "$OWN_TOKEN" ""
  if [ "$DRY_RUN" != "1" ]; then
    [ "$HTTP_CODE" = "403" ] || die 19 "OWNER control: expected 403 for the OWNER login, got HTTP $HTTP_CODE — the role check is not doing what we think"
    step 9 "OWNER negative control: the existing OWNER login is refused (403), so the PASS above is the role, not luck"
  fi
  OWN_TOKEN=""
fi

if [ "$DRY_RUN" = "1" ]; then
  say "DRY RUN complete: nothing was sent."
  exit 0
fi

# ---- step 10: ON SUCCESS ONLY, offer to record the login in the project credentials file ----
printf 'Append KINTSUGI_QA_ORGADMIN_EMAIL / KINTSUGI_QA_ORGADMIN_PASSWORD to %s ? [y/N] ' "$PROJECT_ENV"
IFS= read -r ans || ans=""
case "$ans" in
  y|Y|yes|YES)
    res="$(printf '%s\n%s\n' "$QA_EMAIL" "$QA_PW" | python3 -c 'import os, sys
path = sys.argv[1]
email = sys.stdin.readline().rstrip("\n"); pw = sys.stdin.readline().rstrip("\n")
existing = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
def _k(ln):
    k = ln.split("=", 1)[0].strip()
    return k[7:].strip() if k.startswith("export ") else k
keys = {_k(ln) for ln in existing.splitlines() if "=" in ln and not ln.lstrip().startswith("#")}
added = []
old = os.umask(0o077)
try:
    with open(path, "a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        for k, v in (("KINTSUGI_QA_ORGADMIN_EMAIL", email), ("KINTSUGI_QA_ORGADMIN_PASSWORD", pw)):
            if k not in keys:
                f.write(k + "=" + v + "\n"); added.append(k)
finally:
    os.umask(old)
print(",".join(added) if added else "none")' "$PROJECT_ENV")"
    if [ "$res" = "none" ]; then step 10 "both lines were already present; nothing written"
    else step 10 "appended: $res (values not shown)"; fi ;;
  *) step 10 "not written (you answered no)" ;;
esac
say "DONE: the Kintsugi QA login exists, is bound to organisation $ORG_ID, and passes the key-list check."
exit 0
# Note on cookies: the gateway skips CSRF for any request with an 'Authorization: Bearer' header
# (api-gateway/src/middleware/csrf.ts:365-366); this script never sends or stores a cookie.
