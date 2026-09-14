#!/bin/bash
# controls_check.sh — every :N anchor, blob, size, line count and token count the #813 brief cites, checked against the
# GitHub contents API (blobs at the head + develop M38 + the live develop) AND git at the checkout (read verbs only).
# Usage: bash controls_check.sh [--neg-head-as-dev] [--neg-token] [--neg-dev-as-0911]
#   --neg-head-as-dev  : develop M38 passed where the head is expected (must FAIL on the four PR blobs + the new anchors)
#   --neg-token        : a token demanded PRESENT that is known ABSENT + one demanded ABSENT that is present (must FAIL 2)
#   --neg-dev-as-0911  : develop pinned at the 09-11 develop 2d864ae92 (must FAIL: originate.openapi.ts / the yaml / the
#                        test file differ there — the first arm, M38's parent 54e9b835d, did not discriminate: KS-487 touched
#                        none of the judged files; kept as .first-run-arm-did-not-discriminate.out)
# Prints ok/FAIL lines and a tally; rc 1 if FAILS>0. No secrets printed (GH_TOKEN by name from the Secuura .env).
set -u
ARGS="${1:-}"
python3 - "$ARGS" <<'PY'
import sys, json, urllib.request, urllib.error, base64, subprocess, datetime
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
HEAD = '7b6fb960dafd6c27af1eb9bad2a031f6bfe3a3a4'; M38 = '0e78c7270188ac45c1c29f927bdf90728f10215d'; D0911 = '2d864ae92'
P7BE = '7be1eccbe3e0a045e25583721c37053cbaea8f22'; P542 = '54225cbbd'
if arg == '--neg-head-as-dev': HEAD = M38
DEV = D0911 if arg == '--neg-dev-as-0911' else M38
D = 'Blockchain/Dev/'; G = D + 'services/api-gateway/src/'; OR = D + 'services/originate/src/'
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
            cache[k] = (j['sha'], j['size'], base64.b64decode(j['content']).decode('utf-8') if j.get('encoding') == 'base64' and j.get('content') else None)
        except urllib.error.HTTPError as e:
            cache[k] = (None, None, None) if e.code == 404 else (('ERR', e.code, None))
    return cache[k]
# The yaml (1.3 MB) exceeds the contents API's inline limit — read it by git at the pinned SHAs; blob sha via ls-tree.
def gitblob(ref, path):
    return git('rev-parse', f'{ref}:{path}').strip()
def gittext(ref, path):
    return git('show', f'{ref}:{path}')
# --- blobs at the head + develop (the brief's TARGET table) ---
EXPECT = {
  (HEAD, G+'middleware/contentType.ts'): ('5b5b3e7342d04451ea8a7dff0823fc5763122059', 7235), (HEAD, G+'__tests__/contentType.test.ts'): ('d77981707ab8b1d4c9a93a8c4e3f8f0fcee79f73', 27264),
  (HEAD, OR+'originate.openapi.ts'): ('5e2c499f1a987fa9bd6632d381b9c9ccd7d03637', 149792),
  (HEAD, G+'index.ts'): ('6f38c819e48162e3179aaf557085766f91beecc1', 65578), (HEAD, G+'middleware/csrf.ts'): ('1f16e2f899af46b8afc5e3872261e079c2cf88f5', 15607),
  (HEAD, D+'scripts/generate-openapi.ts'): ('e84acdc9e1be073751fcd6a8bb95504e23688019', 16364), (HEAD, D+'scripts/audit/audit-baseline.json'): ('03d1680e3c7a87f8df70e71082b67775536acde5', 44616),
  (DEV, G+'middleware/contentType.ts'): ('6dcdaa6e005f73e779008691f366cd71cf7ca30d', 5725), (DEV, G+'__tests__/contentType.test.ts'): ('1799ef843a09c707484143ce8c0cc9ecb7957ff0', 24711),
  (DEV, OR+'originate.openapi.ts'): ('12fb03ba61041abd0b1a38cf382258e926c39d06', 144669), (DEV, G+'index.ts'): ('6f38c819e48162e3179aaf557085766f91beecc1', 65578),
  (DEV, G+'middleware/csrf.ts'): ('1f16e2f899af46b8afc5e3872261e079c2cf88f5', 15607), (DEV, D+'scripts/generate-openapi.ts'): ('e84acdc9e1be073751fcd6a8bb95504e23688019', 16364),
}
for (ref, path), (sha, size) in EXPECT.items():
    b = blob(ref, path)
    chk(b[0] == sha and (size is None or b[1] == size), f'{ref[:9]} {path.split("/")[-1]} blob {str(b[0])[:9]} size {b[1]} (expect {sha[:9]} {size})')
chk(gitblob(HEAD, D+'docs/openapi/secuura-api.yaml') == 'd11a5a23721296e45767624d87c4fc1a8f9622f5' and gitblob(DEV, D+'docs/openapi/secuura-api.yaml') == '298d95e4a12b2384f360f83878c6ae84773cf00b', 'yaml blobs head d11a5a237 / develop 298d95e4a (git)')
chk(gitblob(HEAD, D+'package-lock.json') == gitblob(DEV, D+'package-lock.json') == '17d2061b397595677ae789683b0ca1d4b8398bec', 'lockfile 17d2061b3 unchanged')
chk(git('ls-tree', HEAD, '--', G+'routes/proxy.ts').split()[2] == git('ls-tree', DEV, '--', G+'routes/proxy.ts').split()[2], 'proxy.ts blob unchanged head == develop')
# --- line anchors + token counts on the API-fetched bytes (the brief's :N) ---
def lines(ref, path): return (blob(ref, path)[2] or '').split('\n')
def at(ref, path, n, needle):
    L = lines(ref, path); return n <= len(L) and needle in L[n-1]
def cnt(ref, path, needle): return (blob(ref, path)[2] or '').count(needle)
CT = G+'middleware/contentType.ts'
chk(len(lines(HEAD, CT)) == 146 and len(lines(DEV, CT)) == 118, 'contentType.ts 145 lines at head / 117 at develop (split +1)')
chk(at(HEAD, CT, 22, "const ENFORCED_PREFIX = '/api/';"), 'contentType.ts:22 ENFORCED_PREFIX')
chk(at(HEAD, CT, 54, "const FORM_ALLOWED_PATHS = new Set(['/api/oauth/token']);"), 'contentType.ts:54 FORM_ALLOWED_PATHS')
chk(at(HEAD, CT, 75, 'const OCTET_STREAM_ALLOWED_PATHS = new Set([') and at(HEAD, CT, 76, "'/api/verification/verify-file',") and at(HEAD, CT, 77, "'/api/v2/verification/verify-file',") and at(HEAD, CT, 78, ']);'), 'contentType.ts:75-78 the Set (two exact members)')
chk(at(HEAD, CT, 56, '/**') and at(HEAD, CT, 57, ' * KS-791:') and at(HEAD, CT, 74, ' */'), 'contentType.ts:56-74 the docblock')
chk(at(HEAD, CT, 72, "`contentType.test.ts` pins both halves") and at(HEAD, CT, 73, 'a sibling verification route still 415s'), 'contentType.ts:72-73 the "both halves" claim')
chk(at(HEAD, CT, 99, 'function hasBody(req: Request): boolean {') and at(HEAD, CT, 100, "req.headers['transfer-encoding'] !== undefined") and at(HEAD, CT, 103, '}'), 'contentType.ts:99-103 hasBody (:100 transfer-encoding)')
chk(at(HEAD, CT, 119, "if (!req.path.startsWith(ENFORCED_PREFIX)) return next();"), 'contentType.ts:119 the case-sensitive prefix guard')
chk(at(HEAD, CT, 122, 'if (!hasBody(req)) return next();'), 'contentType.ts:122 no body passes')
chk(at(HEAD, CT, 125, "const raw = req.headers['content-type'] ?? '';") and at(HEAD, CT, 126, "const mediaType = raw.split(';')[0].trim().toLowerCase();"), 'contentType.ts:125-126 media type stripped + lowercased')
chk(at(HEAD, CT, 128, 'if (isJsonMediaType(mediaType)) return next();'), 'contentType.ts:128 JSON pass')
chk(at(HEAD, CT, 131, "if (FORM_ALLOWED_PATHS.has(req.path) && mediaType === 'application/x-www-form-urlencoded') return next();"), 'contentType.ts:131 the RFC 6749 allowance')
chk(at(HEAD, CT, 135, "if (OCTET_STREAM_ALLOWED_PATHS.has(req.path) && mediaType === 'application/octet-stream') return next();"), 'contentType.ts:135 THE NEW BRANCH')
chk(at(HEAD, CT, 137, 'res.status(415).json({') and at(HEAD, CT, 144, '});'), 'contentType.ts:137-144 the 415 envelope')
chk(at(HEAD, CT, 140, "code: 'UNSUPPORTED_MEDIA_TYPE',") and at(HEAD, CT, 142, "details: { received: mediaType === '' ? '(none)' : mediaType.slice(0, 100) },"), "contentType.ts:140/:142 the envelope's code and details.received")
chk(at(HEAD, CT, 48, '// ⚠ KS-801:') and at(HEAD, CT, 53, '// the ticket.'), 'contentType.ts:48-53 the KS-801 note')
chk(at(HEAD, CT, 88, "return mediaType === 'application/json' || (mediaType.startsWith('application/') && mediaType.endsWith('+json'));"), 'contentType.ts:88 isJsonMediaType')
chk(cnt(HEAD, CT, 'OCTET_STREAM_ALLOWED_PATHS.has(req.path)') == 1 and cnt(DEV, CT, 'OCTET_STREAM_ALLOWED_PATHS') == 0, 'T1/T2 anchor count 1 at head / 0 at develop (control)')
chk(cnt(HEAD, CT, "mediaType === 'application/octet-stream'") == 1, "T4 anchor mediaType === 'application/octet-stream' count 1")
TT = G+'__tests__/contentType.test.ts'
chk(len(lines(HEAD, TT)) == 591, 'contentType.test.ts 590 lines at head')
chk(at(HEAD, TT, 29, 'function makeReq(') and at(HEAD, TT, 36, '}'), 'test :29-36 makeReq (the double)')
chk(at(HEAD, TT, 250, "describe('KS-802 — the media-type contract over a real Express app (real req.path)'") , 'test :250 the KS-802 real-Express block')
chk(at(HEAD, TT, 272, "server = app.listen(0, '127.0.0.1');"), 'test :272 loopback listener')
chk(at(HEAD, TT, 290, 'function rawPost(') and at(HEAD, TT, 320, '}') and at(HEAD, TT, 322, '/**'), 'test :290-320 rawPost (raw socket)')
chk(at(HEAD, TT, 334, 'async function post(path: string, contentType: string, body: string) {') and at(HEAD, TT, 341, '}'), 'test :334-341 fetch post')
chk(at(HEAD, TT, 497, 'it.each([') and at(HEAD, TT, 501, "KS-801 PERIMETER — %s + form is 200 today") and at(HEAD, TT, 511, '});'), 'test :497-511 the KS-801 PERIMETER cells (assert 200)')
chk(at(HEAD, TT, 544, "describe('enforceJsonContentType — KS-791 verify-file octet-stream exception'") and at(HEAD, TT, 590, '});'), 'test :544-590 the KS-791 block (6 cells)')
chk(at(HEAD, TT, 568, "it('SCOPE — a SIBLING verification route still 415s the identical binary body'"), 'test :568 the SIBLING cell')
chk(at(HEAD, TT, 576, "it('SCOPE — verify-file still 415s a NON-octet-stream binary type (application/pdf)'"), 'test :576 the pdf cell')
chk(at(HEAD, TT, 583, "it('SCOPE — the match is EXACT, not a prefix: a suffixed path is still refused'"), 'test :583 the EXACT cell')
t = blob(HEAD, TT)[2] or ''; t0 = blob(DEV, TT)[2] or ''
chk(t.count("  it('") - t0.count("  it('") == 6 and t[len(t0):].count('run(makeReq(') == 6 and t.count('makeReq({ path: V') == 4 and t.count('makeReq({ path: `${V1}') == 1, 'the PR adds exactly 6 it( cells, all 6 via the makeReq DOUBLE (4 on V1/V2 literal, 1 template, 1 sibling)')
chk(t[len(t0):].count('rawPost(') == 0 and t[len(t0):].count('fetch(') == 0 and t.startswith(t0), 'the 6 new cells send NO HTTP (0 rawPost/fetch in the appended block; the file is a pure append)')
OA = OR+'originate.openapi.ts'
chk(len(lines(HEAD, OA)) == 3857 and len(lines(DEV, OA)) == 3743, 'originate.openapi.ts 3856 lines at head / 3742 at develop')
chk(at(HEAD, OA, 2026, "path: '/api/verification/verify-file',") and at(HEAD, OA, 2077, "path: '/api/v2/verification/verify-file',"), 'openapi.ts:2026 / :2077 the two registerPath paths')
chk(at(HEAD, OA, 2044, "schema: z.string().min(1).openapi({ type: 'string', format: 'binary', minLength: 1, description: 'The document file, as raw bytes.' }),") and at(HEAD, OA, 2093, "minLength: 1, description: 'The document file, as raw bytes.'"), 'openapi.ts:2044 / :2093 the two minLength metadata sites')
chk(cnt(HEAD, OA, "minLength: 1, description: 'The document file, as raw bytes.'") == 2 and cnt(DEV, OA, "minLength: 1, description: 'The document file, as raw bytes.'") == 0, 'minLength metadata anchor count 2 at head / 0 at develop (control)')
chk(cnt(HEAD, OA, '.min(1).openapi') == 6 and cnt(DEV, OA, '.min(1).openapi') == 4, '.min(1).openapi 6 at head / 4 at develop (the +2)')
chk(at(HEAD, OA, 2053, 'NOTE: the handler additionally returns `fileSize`') and at(HEAD, OA, 2055, 'see KS-794') and at(HEAD, OA, 2102, 'NOTE: the handler additionally returns `fileSize`') and at(HEAD, OA, 2104, 'See KS-794'), 'openapi.ts:2053-2055 / :2102-2104 the KS-794 prose')
chk(cnt(HEAD, OA, "security: [],") - cnt(DEV, OA, "security: [],") == 2, 'both new operations are security: [] (+2)')
y = gittext(HEAD, D+'docs/openapi/secuura-api.yaml'); y0 = gittext(DEV, D+'docs/openapi/secuura-api.yaml'); Y = y.split('\n'); Y0 = y0.split('\n')
chk(len(Y) == 39728 and len(Y0) == 39553, 'yaml 39,727 lines at head / 39,552 at develop')
chk(Y[28911] == '  /api/verification/verify-file:' and Y[29004] == '  /api/v2/verification/verify-file:', 'yaml :28912 / :29005 the two paths')
chk(Y[28936].strip() == 'minLength: 1' and Y[29027].strip() == 'minLength: 1', 'yaml :28937 / :29028 minLength: 1 under the two octet-stream request schemas')
chk(sum(1 for l in Y if l.endswith('minLength: 1')) == 115 and sum(1 for l in Y0 if l.endswith('minLength: 1')) == 113, "yaml 'minLength: 1$' 115 at head / 113 at develop")
chk(y.count('application/octet-stream') == 3 and y0.count('application/octet-stream') == 0 and y0.count('verify-file') == 0, 'yaml octet-stream 3/0, verify-file 0 at develop')
added = [l for l in Y if l not in set(Y0)]
chk(sum(1 for l in added if '@' in l) == 0 and sum(1 for l in added if 'example:' in l.lower()) == 0 and y.count('@') >= 90, 'the yaml hunk: 0 at-signs, 0 example: lines (control: at-signs elsewhere >= 90)')
IX = G+'index.ts'
chk(at(HEAD, IX, 397, 'app.use(enforceJsonContentType);') and at(HEAD, IX, 387, "if (NODE_ENV !== 'test') {") and at(HEAD, IX, 389, 'app.use(csrfMiddleware.protect);') and at(HEAD, IX, 390, '}'), 'index.ts:397 the mount / :387-390 CSRF')
chk(at(HEAD, IX, 408, "'/api/gdpr', '/api/verification', '/api/v2/verification', '/api/nft', '/webhooks',") and at(HEAD, IX, 413, 'const shouldParseBody = (req: Request): boolean => !proxyPaths.some(p => req.path.startsWith(p));'), 'index.ts:408 proxyPaths carry both verification prefixes / :413 shouldParseBody')
CS = G+'middleware/csrf.ts'
chk(at(HEAD, CS, 82, 'excludedPaths: [') and at(HEAD, CS, 98, "'/api/verification/verify',") and cnt(HEAD, CS, 'v2/verification') == 0 and cnt(DEV, CS, 'v2/verification') == 0, 'csrf.ts:82 excludedPaths / :98 v1 verify / v2 ABSENT at head and develop (8a)')
chk(at(HEAD, CS, 337, "if (req.headers.authorization?.startsWith('Bearer ') || req.headers['x-api-key']) {"), 'csrf.ts:337 the bearer/api-key skip')
PX = G+'routes/proxy.ts'
chk(at(HEAD, PX, 589, "router.use('/api/verification',") and at(HEAD, PX, 590, "proxy('originate', { '^/api/verification': '/api/verification' }),") and at(HEAD, PX, 594, "router.use('/api/v2/verification',") and at(HEAD, PX, 595, "proxy('originate', { '^/api/v2/verification': '/api/v2/verification' }),"), 'proxy.ts:589-596 the two verification proxy mounts (no auth)')
chk(at(HEAD, PX, 699, '`//ERASURES`'), 'proxy.ts:699 the //ERASURES walk-around note (M9)')
VF = OR+'routes/verification.ts'
chk(at(HEAD, VF, 511, "verificationRouter.post('/verify-file', async (req: Request, res: Response) => {") and at(HEAD, VF, 522, 'if (fileBuffer.length === 0) {') and at(HEAD, VF, 523, 'return res.status(400).json({') and at(HEAD, VF, 539, 'let rows: any[] = await db.$queryRaw`'), 'verification.ts:511 the handler / :522-526 empty→400 / :539 $queryRaw')
chk(at(HEAD, OR+'routes/verificationV2.ts', 501, "verificationV2Router.post('/verify-file', async (req: Request, res: Response) => {"), 'verificationV2.ts:501 the v2 handler')
GEN = D+'scripts/generate-openapi.ts'
chk(at(HEAD, GEN, 257, 'if (checkMode) {') and at(HEAD, GEN, 264, "console.error('[gen-openapi] CHECK FAIL: generated YAML differs from on-disk version');") and at(HEAD, GEN, 268, "console.log('[gen-openapi] CHECK PASS: on-disk YAML matches generated');") and at(HEAD, GEN, 269, 'process.exit(0);'), 'generate-openapi.ts:257-269 the --check semantics')
pj = blob(HEAD, D+'package.json')[2] or ''
chk('"check:openapi": "npm run generate-openapi -- --check && npm run check:spec-examples"' in pj and '"generate-openapi": "npm run build --workspace=packages/shared && tsx scripts/generate-openapi.ts"' in pj, 'package.json check:openapi / generate-openapi scripts')
RP = D+'services/api-gateway/src/docs/developer-portal.html'
chk(cnt(HEAD, RP, 'verify-file') == 3, 'developer-portal.html mentions verify-file 3 times (8e)')
# Schemathesis runner anchors (item 7)
RUN = 'systemTest/schemathesis/scripts/run.py'
chk(len(lines(HEAD, RUN)) == 686 and at(HEAD, RUN, 353, 'def _run_pre_suite(command: str, base_url: str) -> int:') and at(HEAD, RUN, 430, 'assert_slot_named_for_local_target'), 'run.py 685 lines / :353 _run_pre_suite / :430 slot required for a local target')
# --- git-side: parents, merge-base, counts, numstats ---
chk(git('log', '-1', '--format=%P', HEAD).split() == [P7BE, M38], 'head parents = 7be1eccbe + M38')
chk(git('merge-base', M38, HEAD).strip() == M38 and subprocess.run(['git', '-C', R, 'merge-base', '--is-ancestor', M38, HEAD]).returncode == 0, 'M38 is an ancestor of the head (merge-base = M38)')
chk(subprocess.run(['git', '-C', R, 'merge-base', '--is-ancestor', P542, HEAD]).returncode == 0, "54225cbbd (Peter's reviewed head) is an ancestor of the head (fast-forward push)")
chk(git('rev-list', '--count', f'{M38}..{HEAD}').strip() == '4', 'rev-list --count M38..head = 4')
chk(git('rev-parse', HEAD + '^{tree}').strip() == '49ffe07036392d50ae09f04de429b9d769d12974', 'head tree 49ffe0703')
ns = sorted((l.split('\t') for l in git('diff', '--numstat', M38, HEAD).strip().split('\n') if l.count('\t') == 2), key=lambda x: x[2])   # an empty numstat reads as [] (a FAIL, not a crash)
chk([x[:2] for x in ns] == [['175', '0'], ['52', '0'], ['28', '0'], ['114', '0']] and len(ns) == 4, 'numstat M38..head = 175/52/28/114 additions, 0 deletions, 4 files')
chk(git('diff', '--name-only', f'{M38}...{HEAD}').split() == git('diff', '--name-only', M38, HEAD).split(), 'two-dot == three-dot (M38 is an ancestor)')
# negative-token arm
if arg == '--neg-token':
    chk(cnt(HEAD, CS, 'v2/verification') == 1, 'NEG: csrf.ts v2/verification demanded 1 (known 0)')
    chk(cnt(HEAD, CT, 'OCTET_STREAM_ALLOWED_PATHS.has(req.path)') == 0, 'NEG: the :135 anchor demanded ABSENT at head (known 1)')
print(f'TALLY ok={ok} FAILS={fail} live_develop={live[:9]} {datetime.datetime.now().astimezone().strftime("%H:%M:%S")}')
sys.exit(1 if fail else 0)
PY
