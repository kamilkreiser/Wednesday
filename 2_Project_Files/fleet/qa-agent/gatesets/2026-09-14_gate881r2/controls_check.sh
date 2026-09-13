#!/bin/bash
# controls_check.sh — re-grep every §4 positive-control token of the #881 ROUND 2 (tier 1) brief at the PINNED head
# 8ac9db66f through the GitHub contents API (read-only; GH_TOKEN sourced by NAME from the Secuura .env, never
# printed). Tokens were derived from the PR's OWN files at this head, at the fix commit ffcea35cb, at Peter's head
# 787771b97 and at develop M18 — never carried from another gate's brief. PRESENT tokens must grep the stated count;
# ABSENT tokens must grep exactly 0; the six PR files at head must be blob-identical to the fix commit; the three
# Peter-signed-off files blob-identical to 787771b97; the four gateway files + auth index.ts blob-identical at head and
# develop; the moved script bytes (r1's inline body vs head's CONSENT_SUBMIT_SCRIPT body) must diff EMPTY with leading
# whitespace normalised; the merge commit's tree must equal `git merge-tree --write-tree M18 fix` in the gate set's own
# --shared clone (a write verb run THERE, never in the checkout); the round-1 read (Peter's comment on disk) must be
# byte-identical to the API body.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
HEAD="${QA881R2_HEAD:-8ac9db66f6fd0d751f74ecc95bb314210a31ec52}"
FIX='ffcea35cb7c478bdc9d9f32e8232251c15d3300e'
R1='787771b97e745a527639241dbad9d164a65325c7'
DEV="${QA881R2_DEVELOP:-8861e62161466c40f08d2b10a30edeb203123993}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
CLONE='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate881r2/model/clone881'
R1_READ='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s212/item0/peter_comment_5583115315.md'
W="$(mktemp -d "${TMPDIR:-/tmp}/qa881r2ctl.XXXXXX")"
P='Blockchain/Dev/services/auth/src'
OAUTH="$P/routes/oauth.ts"
CSP="$P/__tests__/ks799-consent-script-csp-and-execution.test.ts"
CSRFT="$P/__tests__/ks799-consent-form-csrf-submit.test.ts"
KS798="$P/__tests__/ks798-consent-form-client-id.test.ts"
KS841="$P/__tests__/ks841-consent-form-pkce-and-client-id.test.ts"
KS781="$P/__tests__/ks781-n1-empty-mfacode-treated-as-absent.test.ts"
AIDX="$P/index.ts"
GCSRF='Blockchain/Dev/services/api-gateway/src/middleware/csrf.ts'
GSPEC='Blockchain/Dev/services/api-gateway/src/specRouteMap.ts'
GIDX='Blockchain/Dev/services/api-gateway/src/index.ts'
GPROXY='Blockchain/Dev/services/api-gateway/src/routes/proxy.ts'
NGINX='Blockchain/Dev/docker/nginx-gateway/nginx-production.conf'

fetch() { # path ref outfile -> prints blob sha (or UNREADABLE)
  ( set -a; . "$SECUURA_ENV"; set +a
    P="$1" REF="$2" OUT="$3" python3 - <<'PY'
import base64, json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/contents/" + os.environ["P"] + "?ref=" + os.environ["REF"]
try:
    o = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNREADABLE " + type(e).__name__); sys.exit(0)
open(os.environ["OUT"], "wb").write(base64.b64decode(o["content"]))
print(o["sha"])
PY
  )
}
FAILS=0
echo "controls_check.sh — head ${HEAD:0:9}, fix ${FIX:0:9}, r1 ${R1:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
for spec in "oauth:$OAUTH:$HEAD" "oauth_fix:$OAUTH:$FIX" "oauth_r1:$OAUTH:$R1" "oauth_dev:$OAUTH:$DEV" \
            "csp:$CSP:$HEAD" "csp_fix:$CSP:$FIX" "csrft:$CSRFT:$HEAD" "csrft_fix:$CSRFT:$FIX" "csrft_r1:$CSRFT:$R1" \
            "ks798:$KS798:$HEAD" "ks798_r1:$KS798:$R1" "ks841:$KS841:$HEAD" "ks841_r1:$KS841:$R1" "ks781:$KS781:$HEAD" "ks781_r1:$KS781:$R1" "ks781_dev:$KS781:$DEV" \
            "aidx:$AIDX:$HEAD" "aidx_dev:$AIDX:$DEV" "gcsrf:$GCSRF:$HEAD" "gcsrf_dev:$GCSRF:$DEV" "gspec:$GSPEC:$HEAD" "gspec_dev:$GSPEC:$DEV" \
            "gidx:$GIDX:$HEAD" "gidx_dev:$GIDX:$DEV" "gproxy:$GPROXY:$HEAD" "gproxy_dev:$GPROXY:$DEV" "nginx:$NGINX:$HEAD" "nginx_dev:$NGINX:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
done
# the two files that must be ABSENT at r1 / develop
for spec in "csp_r1:$CSP:$R1" "csp_dev:$CSP:$DEV" "csrft_dev:$CSRFT:$DEV" "ks798_dev:$KS798:$DEV"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*) echo "ok   $n ABSENT at ${ref:0:9} (${sha})" ;; *) echo "FAIL $n present at ${ref:0:9}: blob ${sha:0:9}"; FAILS=$((FAILS+1)) ;; esac
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis oauth ffb573842; blobis oauth_fix ffb573842; blobis oauth_r1 01c2d320f; blobis oauth_dev 4b03f555e
blobis csp 995ee34ce; blobis csp_fix 995ee34ce; blobis csrft a83594c38; blobis csrft_fix a83594c38; blobis csrft_r1 08803feb2
blobis ks798 d5143dc3f; blobis ks798_r1 d5143dc3f; blobis ks841 380ea51a4; blobis ks841_r1 380ea51a4; blobis ks781 5e390443f; blobis ks781_r1 5e390443f; blobis ks781_dev 5d5d490eb
blobis aidx edabbf871; blobis aidx_dev edabbf871; blobis gcsrf 1f16e2f89; blobis gcsrf_dev 1f16e2f89; blobis gspec "$(cat "$W/gspec_dev.blob")"
blobis gidx 6f38c819e; blobis gidx_dev 6f38c819e; blobis gproxy b99f45a4c; blobis gproxy_dev b99f45a4c; blobis nginx "$(cat "$W/nginx_dev.blob")"
for pair in "oauth:oauth_fix:the product file at head == at the fix commit (the merge carried it unchanged)" "ks798:ks798_r1:ks798 at head == Peter's head" "ks841:ks841_r1:ks841 at head == Peter's head" "ks781:ks781_r1:ks781-n1 at head == Peter's head" "aidx:aidx_dev:auth index.ts at head == develop (helmet mount untouched)" "gcsrf:gcsrf_dev:csrf.ts at head == develop" "gspec:gspec_dev:specRouteMap.ts at head == develop" "gidx:gidx_dev:gateway index.ts at head == develop" "gproxy:gproxy_dev:proxy.ts at head == develop" "nginx:nginx_dev:nginx-production.conf at head == develop"; do
  a="${pair%%:*}"; rest="${pair#*:}"; b="${rest%%:*}"; msg="${rest#*:}"
  cmp -s "$W/$a" "$W/$b" && echo "ok   $msg" || { echo "FAIL $msg — DIFFER"; FAILS=$((FAILS+1)); }
done
cmp -s "$W/oauth" "$W/oauth_r1" && { echo "FAIL oauth.ts at head is byte-identical to Peter's head (round 2 changed it)"; FAILS=$((FAILS+1)); } || echo "ok   oauth.ts at head DIFFERS from Peter's head (as round 2 must)"
cmp -s "$W/csrft" "$W/csrft_r1" && { echo "FAIL the csrf-submit test at head is byte-identical to Peter's head"; FAILS=$((FAILS+1)); } || echo "ok   the csrf-submit test at head DIFFERS from Peter's head (cell 1 re-pointed)"
cmp -s "$W/ks781" "$W/ks781_dev" && { echo "FAIL ks781-n1 at head == develop (the round-1 flip missing?)"; FAILS=$((FAILS+1)); } || echo "ok   ks781-n1 at head DIFFERS from develop (round 1's tripwire flip, Peter-reviewed)"
for pair in "oauth:11669c67e982213a" "oauth_r1:4416d681c5d5eefb" "oauth_dev:cc4f4ac0df1b3393" "csp:75fd750616f520f9" "csrft:da8490dbdc8f1666" "csrft_r1:ec1cdc3861c914b3" "ks798:d2df5fa2a12528f0" "ks841:180f74d3024acb3a" "ks781:7e817327eb3dbaa5" "aidx:5b75376a2bd29b8c"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(shasum -a 256 "$W/$f" | cut -c1-16)" = "$want" ] && echo "ok   $f sha256 $want" || { echo "FAIL $f sha256 is not $want"; FAILS=$((FAILS+1)); }
done
for pair in "oauth:1389" "oauth_r1:1341" "oauth_dev:1242" "csp:414" "csrft:164" "csrft_r1:153" "ks798:201" "ks841:152" "ks781:313" "ks781_dev:320" "aidx:312"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -l < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want lines" || { echo "FAIL $f is not $want lines"; FAILS=$((FAILS+1)); }
done
for pair in "oauth:69496" "oauth_r1:66571" "csp:22640" "csrft:9865" "csrft_r1:9018"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -c < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want bytes" || { echo "FAIL $f is not $want bytes"; FAILS=$((FAILS+1)); }
done
lineis() { # file line expected-text
  local got; got="$(sed -n "${2}p" "$W/$1")"
  [ "$got" = "$3" ] && echo "ok   $1:$2 = $3" || { echo "FAIL $1:$2 is: $got"; FAILS=$((FAILS+1)); }
}
# --- oauth.ts at head: the lines the brief cites
lineis oauth 10 " *   GET  /api/oauth/consent.js — The consent page's submit script (KS-799 round 2)"
lineis oauth 461 "function respondAuthorizeRedirect(req: Request, res: Response, url: string): void {"
lineis oauth 462 "  if ((req.get('x-requested-with') || '').toLowerCase() === 'xmlhttprequest') {"
lineis oauth 463 "    res.status(200).json({ success: true, redirect: url });"
lineis oauth 466 "  res.redirect(url);"
lineis oauth 473 "oauthRouter.get('/authorize', async (req: Request, res: Response) => {"
lineis oauth 496 "    const consentHtml = generateConsentPage({"
lineis oauth 510 "    res.setHeader('Content-Type', 'text/html');"
lineis oauth 560 'const CONSENT_SUBMIT_SCRIPT = `'
lineis oauth 570 "      function readCookie(name) {"
lineis oauth 580 "        ev.preventDefault();"
lineis oauth 581 "        var token = readCookie('XSRF-TOKEN');"
lineis oauth 589 "          redirect: 'manual',"
lineis oauth 593 "            'X-XSRF-TOKEN': token,"
lineis oauth 594 "            'X-Requested-With': 'XMLHttpRequest'"
lineis oauth 603 "          if (r.data && r.data.redirect) { window.location.assign(r.data.redirect); return; }"
lineis oauth 609 '`;'
lineis oauth 611 "oauthRouter.get('/consent.js', (_req: Request, res: Response) => {"
lineis oauth 614 "  res.setHeader('Content-Type', 'application/javascript; charset=utf-8');"
lineis oauth 615 "  res.setHeader('Cache-Control', 'no-store');"
lineis oauth 616 "  res.send(CONSENT_SUBMIT_SCRIPT);"
lineis oauth 619 "oauthRouter.post('/authorize', async (req: Request, res: Response) => {"
lineis oauth 675 "      return respondAuthorizeRedirect(req, res, denyUrl.toString()); // KS-799"
lineis oauth 785 "    respondAuthorizeRedirect(req, res, redirectUrl.toString()); // KS-799"
lineis oauth 1251 "function generateConsentPage(params: {"
lineis oauth 1276 "  <style>"
lineis oauth 1305 "  </style>"
lineis oauth 1323 '    <form method="POST" action="/api/oauth/authorize" id="form">'
lineis oauth 1359 "    </form>"
lineis oauth 1364 "  <!--"
lineis oauth 1381 "  -->"
lineis oauth 1382 '  <script src="/api/oauth/consent.js"></script>'
lineis oauth 1384 '</html>`;'
# --- oauth.ts at Peter's head: the inline element
lineis oauth_r1 1285 "  <script>"
lineis oauth_r1 1306 "        var token = readCookie('XSRF-TOKEN');"
lineis oauth_r1 1318 "            'X-XSRF-TOKEN': token,"
lineis oauth_r1 1319 "            'X-Requested-With': 'XMLHttpRequest'"
lineis oauth_r1 1328 "          if (r.data && r.data.redirect) { window.location.assign(r.data.redirect); return; }"
lineis oauth_r1 1334 "  </script>"
# --- the csp test at head
lineis csp 116 "const { JSDOM, VirtualConsole } = require('jsdom') as JsdomModule;"
lineis csp 176 "  app.use(helmet());"
lineis csp 181 "  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', resolve); });"
lineis csp 200 "  const live = html.replace(/<!--[\\s\\S]*?-->/g, '');"
lineis csp 224 "    if (sources.includes(\"'self'\") && target.origin === pageUrl.origin) return true;"
lineis csp 255 '      if (opts.seedCookie !== false) window.document.cookie = `XSRF-TOKEN=${XSRF_COOKIE_VALUE}`;'
lineis csp 301 "  it('C1: every <script> on the rendered consent page is admitted by the response\\'s own script-src (helmet mounted as index.ts does)', async () => {"
lineis csp 322 "  it('C2: GET /api/oauth/consent.js serves the submit logic as JavaScript (nosniff makes the media type load-bearing)', async () => {"
lineis csp 325 "    expect(res.headers.get('content-type') || '').toMatch(/javascript/);"
lineis csp 326 "    expect(res.headers.get('x-content-type-options')).toBe('nosniff');"
lineis csp 347 "    approve!.click(); // the browser's own activation → submit event → the page's listener"
lineis csp 353 "    expect(call.init.headers?.['X-XSRF-TOKEN']).toBe(XSRF_COOKIE_VALUE);"
lineis csp 363 "    expect(jsdomErrors.filter((e) => /HTMLFormElement/.test(e.message))).toEqual([]);"
lineis csp 393 "  it('C3 (control, no cookie): without an XSRF-TOKEN cookie the script shows the error and sends nothing', async () => {"
lineis csp 411 "    expect(received.filter((r) => r === 'GET /api/oauth/consent.js')).toHaveLength(1);"
# --- the csrf-submit test at head
lineis csrft 91 "  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', resolve); });"
lineis csrft 119 "    expect(html).toContain('<script src=\"/api/oauth/consent.js\">');"
lineis csrft 124 "    expect(js).toContain(\"'X-XSRF-TOKEN': token\");             // sends it as the required header"
lineis csrft 133 "    expect(res.status).toBe(200);"
lineis csrft 154 "    expect(res.status).toBe(302);"
# --- the CSP chain files
lineis aidx 68 "app.use(helmet());"
lineis aidx 115 "app.use('/api/oauth', oauthRouter);"
lineis gproxy 369 "  router.use('/api/oauth', proxy('auth', { '^/api/oauth': '/api/oauth' }));"
lineis gidx 258 "      scriptSrc: [\"'self'\", \"'unsafe-inline'\"],"
lineis gidx 387 "if (NODE_ENV !== 'test') {"
lineis gidx 1053 "  if (!matched) return next();"
lineis gcsrf 63 "  protectedMethods: ['POST', 'PUT', 'PATCH', 'DELETE'],"
lineis gcsrf 245 "    if (process.env.NODE_ENV !== 'production') {"
lineis gcsrf 289 "      httpOnly: false, // Client needs to read this"
lineis gcsrf 355 "          code: 'CSRF_ORIGIN_INVALID',"
lineis gcsrf 379 "          code: 'CSRF_TOKEN_MISSING',"
lineis nginx 281 "    add_header Content-Security-Policy \"default-src 'self'; script-src 'self'; style-src-elem 'self' fonts.googleapis.com; style-src-attr 'unsafe-inline'; font-src 'self' fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://*.blockfrost.io https://*.cardanoscan.io wss:; frame-ancestors 'self'; base-uri 'self'; form-action 'self';\" always;"
lineis nginx 347 "    location /api/ {"
chk() { # file token mode(present|absent|N)
  local f="$1" tok="$2" mode="$3" c
  c="$(/usr/bin/grep -c -F -- "$tok" "$W/$f")"
  if [ "$mode" = present ] && [ "$c" -ge 1 ]; then echo "ok   $f  present x$c  $tok"
  elif [ "$mode" = absent ] && [ "$c" -eq 0 ]; then echo "ok   $f  absent      $tok"
  elif [ "$mode" != present ] && [ "$mode" != absent ] && [ "$c" -eq "$mode" ]; then echo "ok   $f  exactly x$c $tok"
  else echo "FAIL $f  $mode expected, count $c: $tok"; FAILS=$((FAILS+1)); fi
}
# --- oauth.ts at head: the tamper anchors, counts as the brief states
chk oauth "oauthRouter.get('/consent.js'" 1
chk oauth "CONSENT_SUBMIT_SCRIPT" 3
chk oauth "'X-XSRF-TOKEN': token," 1
chk oauth "'X-Requested-With': 'XMLHttpRequest'" 1
chk oauth '<script src="/api/oauth/consent.js"></script>' 1
chk oauth "<script>" 2
chk oauth "</script>" 1
chk oauth "application/javascript; charset=utf-8" 1
chk oauth "res.setHeader('Cache-Control', 'no-store');" 1
chk oauth "res.send(CONSENT_SUBMIT_SCRIPT);" 1
chk oauth "window.location.assign(r.data.redirect)" 1
chk oauth "readCookie('XSRF-TOKEN')" 1
chk oauth "ev.preventDefault();" 1
chk oauth "res.setHeader('Content-Type', 'text/html')" 1
chk oauth "generateConsentPage(" 2
chk oauth "Content-Security-Policy" 1
chk oauth "helmet" 4
chk oauth "nonce" 2
chk oauth "if ((req.get('x-requested-with') || '').toLowerCase() === 'xmlhttprequest') {" 1
chk oauth "listen(" absent
chk oauth "respondAuthorizeRedirect(" 3
# --- oauth.ts at Peter's head: the inline world
chk oauth_r1 "consent.js" absent
chk oauth_r1 "CONSENT_SUBMIT_SCRIPT" absent
chk oauth_r1 "<script>" 2
chk oauth_r1 "</script>" 1
chk oauth_r1 "'X-XSRF-TOKEN': token," 1
# --- oauth.ts at develop: none of KS-799
chk oauth_dev "X-XSRF-TOKEN" absent
chk oauth_dev "consent.js" absent
chk oauth_dev "respondAuthorizeRedirect(" absent
# --- the csp test at head
chk csp "  it('" 7
chk csp "require('jsdom')" 1
chk csp "app.use(helmet());" 1
chk csp "app.listen(0, '127.0.0.1', resolve)" 1
chk csp "resources: 'usable'," 1
chk csp "runScripts: 'dangerously'," 1
chk csp "toMatch(/javascript/)" 1
chk csp "toBe('nosniff')" 1
chk csp "/HTMLFormElement/" 1
chk csp "navigation to another Document" 1
chk csp "GET /api/oauth/consent.js" 4
chk csp "fillCredentials(dom)" 4
# --- the csrf-submit test at head / r1
chk csrft "  it('" 5
chk csrft "toBe(302)" 2
chk csrft "toBe(200)" 3
chk csrft '<script src="/api/oauth/consent.js">' 1
chk csrft "let generateConsentPage" absent
chk csrft_r1 "let generateConsentPage" 1
chk csrft_r1 "consent.js" absent
chk csrft_r1 "  it('" 5
# --- the three signed-off files bind loopback
chk ks798 "app.listen(0, '127.0.0.1'" 1
chk ks841 "app.listen(0, '127.0.0.1'" 1
chk ks781 "app.listen(0, '127.0.0.1'" 1
# --- the CSP chain
chk aidx "app.use(helmet());" 1
chk gidx "'unsafe-inline'" 4
chk gidx "app.use(csrfMiddleware.generateToken);" 1
chk gidx "app.use(csrfMiddleware.protect);" 1
chk gidx "resolveSpecRoute(specMethodMap, req.path)" 1
chk gcsrf "cookieName: 'XSRF-TOKEN'," 1
chk gcsrf "headerName: 'X-XSRF-TOKEN'," 1
chk gcsrf "'/api/oauth" absent
chk gcsrf "export function createCsrfMiddleware" 1
chk gcsrf "CSRF_TOKEN_MISMATCH" 1
chk gspec "export function buildSpecMethodMap" 1
chk gspec "export function resolveSpecRoute" 1
chk gproxy "router.use('/api/oauth'" 1
chk nginx "script-src 'self';" 2
chk nginx "style-src-elem 'self'" 2
# --- the moved bytes: r1's inline body (between the tag lines) vs head's constant body, leading whitespace normalised
cat > "$W/moved.py" <<'PY'
import sys, hashlib, subprocess, json, os
W = sys.argv[1]; CLONE = sys.argv[2]; R1_READ = sys.argv[3]
r1 = open(f"{W}/oauth_r1", encoding="utf-8").read().split("\n"); hd = open(f"{W}/oauth", encoding="utf-8").read().split("\n")
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
body_r1 = [l.strip() for l in r1[1285:1333]]   # lines 1286..1333 (between <script> at 1285 and </script> at 1334)
body_hd = [l.strip() for l in hd[560:608]]     # lines 561..608 (between the backtick at 560 and `; at 609)
ck(len(body_r1) == 48 and len(body_hd) == 48, f"the moved script body is 48 lines at both heads ({len(body_r1)} / {len(body_hd)})")
ck(body_r1 == body_hd, "r1's inline body == head's CONSENT_SUBMIT_SCRIPT body, leading whitespace normalised (moved verbatim)")
ck("`" not in "\n".join(body_hd) and "${" not in "\n".join(body_hd), "the constant's body carries no backtick and no dollar-brace (it is interpolated into a template literal)")
# a positive control that the comparison can fail
ck([l.replace("token", "tok3n") for l in body_r1] != body_hd, "control: a one-token change makes the bodies differ")
# the head page carries exactly ONE live <script> element, with src, empty body
import re
def page(lines):
    # the consent page is the template literal returned by generateConsentPage: from `return \`<!DOCTYPE html>` to the closing `\`;`
    i = next(k for k, l in enumerate(lines) if l.startswith("  return `<!DOCTYPE html>")); j = next(k for k in range(i, len(lines)) if lines[k] == "</html>`;")
    return "\n".join(lines[i:j + 1])
html = page(hd)
live = re.sub(r"<!--[\s\S]*?-->", "", html)
tags = re.findall(r"<script\b([^>]*)>([\s\S]*?)</script>", live)
ck(hd[1269].startswith("  return `<!DOCTYPE html>") and hd[1383] == "</html>`;" and r1[1179].startswith("  return `<!DOCTYPE html>"), "the page template literal spans :1270-1384 at head and starts :1180 at r1")
ck(len(tags) == 1 and 'src="/api/oauth/consent.js"' in tags[0][0] and tags[0][1].strip() == "", f"head oauth.ts (comments stripped) carries exactly one <script> element, src=/api/oauth/consent.js, empty body: {[(a.strip(), len(b)) for a,b in tags]}")
html_r1 = page(r1); live_r1 = re.sub(r"<!--[\s\S]*?-->", "", html_r1)
tags_r1 = re.findall(r"<script\b([^>]*)>([\s\S]*?)</script>", live_r1)
ck(len(tags_r1) == 1 and "src=" not in tags_r1[0][0] and len(tags_r1[0][1]) > 1000, f"r1 oauth.ts carries exactly one INLINE <script> element (body {len(tags_r1[0][1]) if tags_r1 else 0} chars)")
# the merge-tree equality in the gate set's own --shared clone (a write verb run THERE)
def git(*a): return subprocess.run(["git", "-C", CLONE, *a], capture_output=True, text=True)
mt = git("merge-tree", "--write-tree", "8861e62161466c40f08d2b10a30edeb203123993", "ffcea35cb7c478bdc9d9f32e8232251c15d3300e")
ht = git("rev-parse", "8ac9db66f6fd0d751f74ecc95bb314210a31ec52^{tree}")
ck(mt.returncode == 0 and ht.returncode == 0 and mt.stdout.strip() == ht.stdout.strip() == "136e6c8ccce47c0787d71398dd41010298ac8e17", f"merge-tree(M18, fix) {mt.stdout.strip()[:9]} == head tree {ht.stdout.strip()[:9]} == 136e6c8cc (the merge commit is the mechanical union)")
mt2 = git("merge-tree", "--write-tree", "8861e62161466c40f08d2b10a30edeb203123993", "787771b97e745a527639241dbad9d164a65325c7")
ck(mt2.returncode == 0 and mt2.stdout.strip() != ht.stdout.strip(), f"control: merge-tree(M18, Peter's head) {mt2.stdout.strip()[:9]} DIFFERS from the head tree")
mb = git("merge-base", "8ac9db66f6fd0d751f74ecc95bb314210a31ec52", "8861e62161466c40f08d2b10a30edeb203123993")
ck(mb.stdout.strip() == "8861e62161466c40f08d2b10a30edeb203123993", f"merge-base(head, M18) = M18 itself ({mb.stdout.strip()[:9]}) — develop is an ancestor of the head")
ns = git("diff", "--name-status", "8861e62161466c40f08d2b10a30edeb203123993", "8ac9db66f6fd0d751f74ecc95bb314210a31ec52")
names = sorted(l.split("\t")[-1] for l in ns.stdout.strip().split("\n") if l)
want = sorted(["Blockchain/Dev/services/auth/src/routes/oauth.ts",
 "Blockchain/Dev/services/auth/src/__tests__/ks799-consent-script-csp-and-execution.test.ts",
 "Blockchain/Dev/services/auth/src/__tests__/ks799-consent-form-csrf-submit.test.ts",
 "Blockchain/Dev/services/auth/src/__tests__/ks798-consent-form-client-id.test.ts",
 "Blockchain/Dev/services/auth/src/__tests__/ks841-consent-form-pkce-and-client-id.test.ts",
 "Blockchain/Dev/services/auth/src/__tests__/ks781-n1-empty-mfacode-treated-as-absent.test.ts"])
ck(names == want, f"git diff --name-status M18 head = exactly the six PR files ({len(names)})")
fx = git("diff", "--numstat", "787771b97e745a527639241dbad9d164a65325c7", "ffcea35cb7c478bdc9d9f32e8232251c15d3300e")
ck(sorted(fx.stdout.strip().split("\n")) == sorted(["21\t10\tBlockchain/Dev/services/auth/src/__tests__/ks799-consent-form-csrf-submit.test.ts", "414\t0\tBlockchain/Dev/services/auth/src/__tests__/ks799-consent-script-csp-and-execution.test.ts", "105\t57\tBlockchain/Dev/services/auth/src/routes/oauth.ts"]), "git diff --numstat r1 fix = the three files 21/10, 414/0, 105/57")
# the round-1 read on disk == the API body
env = {}
for line in open("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env", encoding="utf-8"):
    if line.startswith("GH_TOKEN="): env["t"] = line.split("=", 1)[1].strip().strip('"').strip("'")
import urllib.request
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/Secuura/Distributed_Secuura/issues/comments/5583115315", headers={"Authorization": "Bearer " + env.get("t", ""), "Accept": "application/vnd.github+json"}), timeout=60))
    disk = open(R1_READ, encoding="utf-8").read()
    ck(c["body"] == disk and len(disk) == 11080, f"the round-1 read on disk == API comment 5583115315 ({len(disk)} chars, PeterObeden {c['created_at']})")
except Exception as e:
    ck(False, "the round-1 read could not be compared to the API: " + type(e).__name__)
# raw control bytes in the six head files
for f in ["oauth", "csp", "csrft", "ks798", "ks841", "ks781"]:
    b = open(f"{W}/{f}", "rb").read()
    ck(not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], f"{f} at head: 0 raw control bytes")
sys.exit(1 if fails else 0)
PY
python3 "$W/moved.py" "$W" "$CLONE" "$R1_READ" || FAILS=$((FAILS+1))
echo "work dir (kept): $W"
echo "controls_check: FAILS=$FAILS"
[ "$FAILS" -eq 0 ] && exit 0 || exit 1
