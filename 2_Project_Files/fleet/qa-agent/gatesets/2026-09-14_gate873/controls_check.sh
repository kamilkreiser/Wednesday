#!/bin/bash
# controls_check.sh — every :N anchor, blob, size, line count and token count the #873 brief cites, checked against the
# GitHub contents API (blobs at the head + develop M46 + the live develop) AND git at the checkout (read verbs only).
# Usage: bash controls_check.sh [--neg-head-as-dev] [--neg-token] [--neg-dev-as-ff52]
#   --neg-head-as-dev  : develop M46 passed where the head is expected (must FAIL on the two PR blobs + the new anchors)
#   --neg-token        : a token demanded PRESENT that is known ABSENT + one demanded ABSENT that is present (must FAIL 2)
#   --neg-dev-as-ff52  : develop pinned at the PR base ff5218867 (must FAIL: the originate ks914 test, the lockfile and
#                        audit-baseline.json differ there — the merge-in brought develop's)
# Prints ok/FAIL lines and a tally; rc 1 if FAILS>0. No secrets printed (GH_TOKEN / LINEAR_API_KEY by name from the Secuura .env).
set -u
ARGS="${1:-}"
python3 - "$ARGS" <<'PY'
import sys, json, urllib.request, urllib.error, base64, subprocess, datetime, hashlib
arg = sys.argv[1]
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
R = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
tok = ''; lkey = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
    if line.startswith('LINEAR_API_KEY='): lkey = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok and lkey
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def git(*a):
    return subprocess.run(['git', '-C', R] + list(a), capture_output=True, text=True).stdout
def rc(*a):
    return subprocess.run(['git', '-C', R] + list(a), capture_output=True, text=True).returncode
HEAD = 'c624c9a8dd24129dad46cf7a204ae75ecb875dc3'; M45 = '852e1fff773bd358170c11334d59496f05fdd8a7'; M46 = 'bc067e3e91821116f3344b2aa5a1d7a5cc968d18'
FF52 = 'ff5218867d3fabd1913fc43fdea442ef2afd81fc'; P7D8 = '7d8a3f0e48e1d0000dcbfc7ba3d36a443c6ed045'
if arg == '--neg-head-as-dev': HEAD = M46
DEV = FF52 if arg == '--neg-dev-as-ff52' else M46
D = 'Blockchain/Dev/'; SH = D + 'packages/shared/'; OR = D + 'services/originate/src/'
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
def gitblob(ref, path):
    return git('rev-parse', f'{ref}:{path}').strip()
# --- blobs at the head + develop (the brief's TARGET table) ---
GUARD = SH + 'src/security/ssrf-guard.ts'; TEST = SH + 'src/__tests__/ks914-shipped-path.test.ts'
EXPECT = {
  (HEAD, GUARD): ('5a838e0d6440b371ab7ffa27ea1ec4ea878db150', 25211), (HEAD, TEST): ('69706c1ef6b9fdeda03cece3051f94705fe17cf2', 10001),
  (DEV, GUARD): ('a1203248f913ceeb677c0ca39fb1a5ead081e852', 23348), (DEV, TEST): ('944a5530c6b3089bf6c1233b96ab9b666009f27d', 8130),
  (HEAD, SH + 'src/__tests__/ssrf-guard.test.ts'): ('afb0c0d0809ea62c3a963be3272342fec5a2d04a', None), (DEV, SH + 'src/__tests__/ssrf-guard.test.ts'): ('afb0c0d0809ea62c3a963be3272342fec5a2d04a', None),
  (HEAD, SH + 'src/__tests__/ks914-pinned-address.test.ts'): ('ffce480e4ddec290fe31c73578cb1ac9fa1adea3', None), (DEV, SH + 'src/__tests__/ks914-pinned-address.test.ts'): ('ffce480e4ddec290fe31c73578cb1ac9fa1adea3', None),
  (HEAD, SH + 'vitest.config.ts'): ('2a226c0068faa65538cda8d43d03bb9bee2944f1', None), (HEAD, SH + 'tsconfig.json'): ('1fd016cc28803cc8f36cc84db4628941a2af9c50', None), (HEAD, SH + 'package.json'): ('3957692311221fbe87c4ab19447de8cec44aa19a', None),
  (HEAD, OR + 'routes/webhooks.ts'): ('c88eb97db5a2466e9456506c2c1bf5094e3c5d4e', None), (DEV, OR + 'routes/webhooks.ts'): ('c88eb97db5a2466e9456506c2c1bf5094e3c5d4e', None),
  (HEAD, OR + '__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts'): ('eb655301e50549c8109c776b90cd44ccd10e650a', None), (DEV, OR + '__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts'): ('eb655301e50549c8109c776b90cd44ccd10e650a', None),
  (HEAD, D + 'services/m365-integration/src/index.ts'): ('1f3a91d4f4f1e98db4d54c9be0e86c768b79cde4', None), (DEV, D + 'services/m365-integration/src/index.ts'): ('1f3a91d4f4f1e98db4d54c9be0e86c768b79cde4', None),
  (HEAD, D + 'scripts/audit/audit-baseline.json'): ('03d1680e3c7a87f8df70e71082b67775536acde5', None), (DEV, D + 'scripts/audit/audit-baseline.json'): ('03d1680e3c7a87f8df70e71082b67775536acde5', None),
}
for (ref, path), (sha, size) in EXPECT.items():
    b = blob(ref, path)
    chk(b[0] == sha and (size is None or b[1] == size), f'{ref[:9]} {path.split("/")[-1]} blob {str(b[0])[:9]} size {b[1]} (expect {sha[:9]} {size})')
chk(gitblob(HEAD, D + 'package-lock.json') == gitblob(DEV, D + 'package-lock.json') == '17d2061b397595677ae789683b0ca1d4b8398bec', 'root lockfile 17d2061b3 at head == develop (git)')
chk(gitblob(FF52, D + 'package-lock.json') == 'b4a2d1e2e3c3906696062e5d78d0168d5b399264' and gitblob(FF52, D + 'scripts/audit/audit-baseline.json') == '33bc6f29a795f52e9d4da9bc6575b383e7475cb7' and gitblob(FF52, OR + '__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts') == '7ac27a1fd1d029bd6cc7247591b038af298199a2', 'ff5218867 had lockfile b4a2d1e2e / audit-baseline 33bc6f29a / originate ks914 test 7ac27a1fd (the merge-in brought develop\'s)')
chk(gitblob(M45, GUARD) == gitblob(M46, GUARD) == gitblob(FF52, GUARD) == 'a1203248f913ceeb677c0ca39fb1a5ead081e852' and gitblob(M45, TEST) == gitblob(M46, TEST) == gitblob(FF52, TEST) == '944a5530c6b3089bf6c1233b96ab9b666009f27d', 'the two base blobs equal at ff5218867, M45 and M46')
chk(gitblob(P7D8, GUARD) == gitblob(HEAD, GUARD) and gitblob(P7D8, TEST) == gitblob(HEAD, TEST), 'the two lane blobs at 7d8a3f0e4 == at the head (the merge moved neither)')
# --- line anchors + token counts on the API-fetched bytes (the brief's :N) ---
def text(ref, path): return blob(ref, path)[2] or ''
def lines(ref, path): return text(ref, path).split('\n')
def at(ref, path, n, needle):
    L = lines(ref, path); return n <= len(L) and needle in L[n-1]
def cnt(ref, path, needle): return text(ref, path).count(needle)
g = text(HEAD, GUARD); g0 = text(DEV, GUARD)
chk(len(lines(HEAD, GUARD)) == 582 and len(lines(DEV, GUARD)) == 544, 'ssrf-guard.ts 581 lines at head / 543 at develop (split +1)')
chk(hashlib.sha256(g.encode('utf-8')).hexdigest().startswith('f847a643838a715e') and hashlib.sha256(g0.encode('utf-8')).hexdigest().startswith('c57e3a0b90898311'), 'guard sha256 f847a643838a715e at head / c57e3a0b90898311 at develop')
chk(at(HEAD, GUARD, 56, "import { lookup } from 'dns/promises';"), 'guard :56 imports lookup from dns/promises (G-3 mock point)')
chk(at(HEAD, GUARD, 235, 'export function checkUrlLiteral(') and at(HEAD, GUARD, 253, "'url must use https:// — payloads are not delivered over plaintext HTTP',"), 'guard :235 checkUrlLiteral / :253 the https-only message')
chk(at(HEAD, GUARD, 262, 'if (family !== 0) {') and at(HEAD, GUARD, 264, 'if (reason) return { ok: false, error: `url host ${bare} is forbidden: ${reason}` };'), 'guard :262-264 the IP-literal classify')
chk(at(HEAD, GUARD, 310, 'export async function resolvePublicAddresses(') and at(HEAD, GUARD, 358, 'export async function assertSafeOutboundUrl(') and at(HEAD, GUARD, 388, 'export function pinnedLookup(address: string) {'), 'guard :310 resolvePublicAddresses / :358 assertSafeOutboundUrl / :388 pinnedLookup')
chk(at(HEAD, GUARD, 430, "export type SafeOutboundFailureReason = 'blocked' | 'request_failed';") and at(HEAD, GUARD, 432, 'export type SafeOutboundResult =') and at(HEAD, GUARD, 439, 'body?: string;'), 'guard :430 the reason type / :432 the result type / :439 body?: string')
chk(at(HEAD, GUARD, 451, "Returns the guard's error rather than throwing it") and at(HEAD, GUARD, 455, '"Rather than throwing it" is now literally true') and cnt(DEV, GUARD, '"Rather than throwing it" is now literally true') == 0, 'guard :451 the contract sentence / :455 the NEW sentence (0 at develop)')
chk(at(HEAD, GUARD, 465, 'export async function safeOutboundRequest(') and at(HEAD, GUARD, 471, "if (!literal.ok) return { ok: false, reason: 'blocked', error: literal.error };") and at(HEAD, GUARD, 475, "if (!resolved.ok) return { ok: false, reason: 'blocked', error: resolved.error };"), 'guard :465 safeOutboundRequest / :471 literal-layer blocked (T3) / :475 DNS-layer blocked (T4)')
chk(at(HEAD, GUARD, 477, 'const address = resolved.addresses[0];') and at(HEAD, GUARD, 484, 'const timeoutMs = init.timeoutMs ?? 10_000;') and at(HEAD, GUARD, 486, 'return new Promise((resolve) => {'), 'guard :477 the pinned address / :484 the 10 s default / :486 the executor')
chk(at(HEAD, GUARD, 489, 'const done = (r: SafeOutboundResult) => {') and at(HEAD, GUARD, 491, 'settled = true;') and at(HEAD, GUARD, 493, 'agent.destroy();') and at(HEAD, GUARD, 494, 'resolve(r);') and at(HEAD, GUARD, 495, '};'), 'guard :489-495 done (settled / clearTimeout / agent.destroy / resolve)')
chk(at(HEAD, GUARD, 497, '/*') and at(HEAD, GUARD, 498, '* KS-931 (KS-914 gate F2).') and at(HEAD, GUARD, 510, "* WHY `request_failed` AND NOT `blocked`") and at(HEAD, GUARD, 515, '*/'), 'guard :497-515 the KS-931 comment (:510 the WHY)')
chk(at(HEAD, GUARD, 516, 'let req: ReturnType<typeof mod.request>;') and at(HEAD, GUARD, 517, 'try {') and at(HEAD, GUARD, 518, 'req = mod.request('), 'guard :516-518 let req / try / req = mod.request(')
chk(at(HEAD, GUARD, 522, 'port: url.port || (isTls ? 443 : 80),') and at(HEAD, GUARD, 523, 'path: `${url.pathname}${url.search}`,'), 'guard :522-523 port / path')
chk(at(HEAD, GUARD, 534, '} catch (err) {') and at(HEAD, GUARD, 535, "done({ ok: false, reason: 'request_failed', error: (err as Error).message });") and at(HEAD, GUARD, 536, 'return;') and at(HEAD, GUARD, 537, '}'), 'guard :534-537 THE EXECUTOR CATCH (T1/T1b/T2)')
chk(at(HEAD, GUARD, 560, 'deadline = setTimeout(() => {') and at(HEAD, GUARD, 567, '}, timeoutMs);') and at(HEAD, GUARD, 569, "req.on('error', (err) => done({ ok: false, reason: 'request_failed', error: err.message }));"), 'guard :560-567 the deadline / :569 the error listener')
chk(at(HEAD, GUARD, 571, '// `write`/`end` can throw synchronously too (an unencodable body, a socket') and at(HEAD, GUARD, 572, '// already destroyed by the deadline above). Same contract, same handling.'), 'guard :571-572 the write/end comment (Peter\'s two reasons)')
chk(at(HEAD, GUARD, 573, 'try {') and at(HEAD, GUARD, 574, 'if (init.body) req.write(init.body);') and at(HEAD, GUARD, 575, 'req.end();') and at(HEAD, GUARD, 576, '} catch (err) {') and at(HEAD, GUARD, 577, 'req.destroy();') and at(HEAD, GUARD, 578, "done({ ok: false, reason: 'request_failed', error: (err as Error).message });") and at(HEAD, GUARD, 579, '}'), 'guard :573-579 the write/end wrap (T5 / G-4)')
chk(at(HEAD, GUARD, 488, 'let deadline: ReturnType<typeof setTimeout> | undefined;') and at(DEV, GUARD, 483, 'let deadline: ReturnType<typeof setTimeout> | undefined;'), 'the prefer-const `deadline` line :488 at head / :483 at develop')
A1 = "    } catch (err) {\n      done({ ok: false, reason: 'request_failed', error: (err as Error).message });\n      return;\n    }\n"
A2 = "    } catch (err) {\n      req.destroy();\n      done({ ok: false, reason: 'request_failed', error: (err as Error).message });\n    }\n"
chk(g.count(A1) == 1 and g0.count(A1) == 0 and g.count(A2) == 1 and g0.count(A2) == 0, 'T1 anchor (4-line first catch) 1/0 and T5 anchor (4-line second catch) 1/0 at head/develop')
chk(g.count("done({ ok: false, reason: 'request_failed', error: (err as Error).message });") == 2 and g0.count("done({ ok: false, reason: 'request_failed', error: (err as Error).message });") == 0, 'the done(...) line alone occurs TWICE at head (:535 + :578) / 0 at develop')
chk(g.count("reason: 'request_failed'") == 5 and g0.count("reason: 'request_failed'") == 3 and g.count("reason: 'blocked'") == 3 and g0.count("reason: 'blocked'") == 3, "reason: 'request_failed' 5/3, reason: 'blocked' 3/3 at head/develop")
chk(g.count('} catch (err) {') == 3 and g0.count('} catch (err) {') == 1 and g.count('req.destroy();') == 2 and g0.count('req.destroy();') == 1, '`} catch (err) {` 3/1 and `req.destroy();` 2/1 at head/develop')
chk(at(DEV, GUARD, 466, "if (!literal.ok) return { ok: false, reason: 'blocked', error: literal.error };") and at(DEV, GUARD, 470, "if (!resolved.ok) return { ok: false, reason: 'blocked', error: resolved.error };") and at(DEV, GUARD, 492, 'const req = mod.request(') and at(DEV, GUARD, 539, "req.on('error'") and at(DEV, GUARD, 540, 'if (init.body) req.write(init.body);') and at(DEV, GUARD, 541, 'req.end();'), 'base guard :466 / :470 / :492 const req = mod.request( / :539 / :540-541 bare write+end')
# the shipped test file
t = text(HEAD, TEST); t0 = text(DEV, TEST)
chk(len(lines(HEAD, TEST)) == 227 and len(lines(DEV, TEST)) == 183, 'ks914-shipped-path.test.ts 226 lines at head / 182 at develop')
chk(at(HEAD, TEST, 37, "vi.mock('https', async (importOriginal) => {") and at(HEAD, TEST, 39, 'request: vi.fn(actual.request)') and at(HEAD, TEST, 42, "const { safeOutboundRequest } = await import('../security/ssrf-guard');"), 'test :37-42 the https module-registry mock + the late import')
chk(at(HEAD, TEST, 20, '* NO TEST-ONLY HOLE IN THE GUARD.') and at(HEAD, TEST, 27, '* WHAT THEY DO NOT PROVE') and at(HEAD, TEST, 29, '* answer needs real DNS.'), 'test :20-29 the IP-literal / no-DNS header + the stated multi-address gap')
chk(at(HEAD, TEST, 84, "it('a refusal by the guard is `blocked`, and NO socket is opened'") and at(HEAD, TEST, 88, "expect(result.reason).toBe('blocked');") and at(HEAD, TEST, 95, "it('plaintext is refused as `blocked` by the literal check, before any resolution'") and at(HEAD, TEST, 99, "expect(result.reason).toBe('blocked');"), 'test :84/:88 the blocked cell / :95/:99 the plaintext cell (T3)')
chk(at(HEAD, TEST, 118, '/**') and at(HEAD, TEST, 119, '* KS-931 (KS-914 gate F2)') and at(HEAD, TEST, 131, '*/'), 'test :118-131 the KS-931 docblock')
chk(at(HEAD, TEST, 132, 'it.each([') and at(HEAD, TEST, 133, "['CRLF', 'a\\r\\nX-Injected: 1'],") and at(HEAD, TEST, 134, "['non-latin1', 'café中文'],") and at(HEAD, TEST, 135, "['NUL', 'a\\u0000b'],") and at(HEAD, TEST, 136, "an unencodable %s header returns a tagged failure instead of throwing"), 'test :132-136 the three it.each rows')
chk(at(HEAD, TEST, 137, "https://203.0.113.7/") and at(HEAD, TEST, 139, 'timeoutMs: 150,') and at(HEAD, TEST, 143, "expect(result.reason).toBe('request_failed');") and at(HEAD, TEST, 145, 'expect(result.error).toMatch(/Invalid character in header content/);'), 'test :137-145 TEST-NET-3 / 150 ms / the tag assertion (T2) / the message assertion')
chk(at(HEAD, TEST, 149, "it('CONTROL: an encodable header reaches the transport and fails on the DEADLINE, not on encoding'") and at(HEAD, TEST, 157, 'expect(result.error).toMatch(/deadline/);') and at(HEAD, TEST, 158, 'expect(result.error).not.toMatch(/Invalid character/);'), 'test :149-158 the CONTROL cell')
chk(at(HEAD, TEST, 184, "it('bounds a server that drips bytes forever (the drain case)'") and at(HEAD, TEST, 194, 'requestMock.mockImplementationOnce((opts: any, cb: any) =>') and at(HEAD, TEST, 196, ');') and at(HEAD, TEST, 211, 'expect(elapsed).toBeLessThan(3000);') and at(HEAD, TEST, 224, 'expect(elapsed).toBeLessThan(5000);'), 'test :184 the drip cell / :194-196 the loopback redirection / :211 + :224 the timing bounds')
TL = t.split('\n'); TL0 = t0.split('\n')
chk(TL[:117] == TL0[:117] and TL[161:] == TL0[117:] and len(TL) - len(TL0) == 44 and t.count("  it('") == 7 and t0.count("  it('") == 6 and t.count('it.each([') == 1 and t0.count('it.each([') == 0, 'the PR INSERTS 44 lines at :118-161 (prefix :1-117 and the suffix identical to develop); it( 7 / develop 6 (+ the control), it.each 1/0 (3 rows) — cells 6 -> 10')
chk(cnt(HEAD, TEST, 'X-Probe') == 2 and cnt(DEV, TEST, 'X-Probe') == 0 and cnt(HEAD, TEST, 'rebind.example') == 0, 'X-Probe 2/0 at head/develop; no rebind cell in the shipped file (G-3 is new)')
# sibling suites: no call of safeOutboundRequest( outside comments; the dns/promises mock point; the rebind block
sg = text(HEAD, SH + 'src/__tests__/ssrf-guard.test.ts'); pa = text(HEAD, SH + 'src/__tests__/ks914-pinned-address.test.ts')
chk(sg.count('safeOutboundRequest(') == 0 and sum(1 for l in pa.split('\n') if 'safeOutboundRequest(' in l and not l.strip().startswith('*')) == 0, 'ssrf-guard.test.ts and ks914-pinned-address.test.ts never CALL safeOutboundRequest( (T1-T5 whole-suite predictions)')
chk(at(HEAD, SH + 'src/__tests__/ssrf-guard.test.ts', 19, "vi.mock('dns/promises', () => ({ lookup: (...args: unknown[]) => lookupMock(...args) }));") and at(HEAD, SH + 'src/__tests__/ssrf-guard.test.ts', 212, "describe('assertSafeOutboundUrl — both layers'") and at(HEAD, SH + 'src/__tests__/ssrf-guard.test.ts', 224, "it('catches the rebind shape: literal-clean host, internal A record'") and at(HEAD, SH + 'src/__tests__/ssrf-guard.test.ts', 235, '});'), 'ssrf-guard.test.ts :19 the dns/promises mock / :212-235 the assertSafeOutboundUrl block (:224 the rebind)')
chk(sg.count("  it('") == 25 and sg.count('it.each([') == 4 and pa.count("  it('") == 6, 'ssrf-guard.test.ts 25 it( + 4 it.each blocks; ks914-pinned-address.test.ts 6 it(')
# config / scripts
chk('"exclude": ["node_modules", "dist", "src/__tests__"]' in text(HEAD, SH + 'tsconfig.json'), 'packages/shared tsconfig excludes src/__tests__ (KS-933 / KS-1000 class)')
chk("include: ['src/__tests__/**/*.test.ts']" in text(HEAD, SH + 'vitest.config.ts') and "'@secuura/shared': resolve(__dirname, 'src/index.ts')," in text(HEAD, SH + 'vitest.config.ts'), 'vitest.config.ts include pattern + the working-tree alias')
chk('"test": "vitest run"' in text(HEAD, SH + 'package.json') and '"build": "tsc"' in text(HEAD, SH + 'package.json'), 'packages/shared package.json test/build scripts')
# the call site
W = OR + 'routes/webhooks.ts'; w = text(HEAD, W)
chk(len(lines(HEAD, W)) == 550, 'webhooks.ts 549 lines')
chk(at(HEAD, W, 357, "webhooksRouter.post('/:id/test', async (req: Request, res: Response) => {") and at(HEAD, W, 358, 'try {') and at(HEAD, W, 373, "type: 'test.ping',") and at(HEAD, W, 390, '} catch (err: any) {') and at(HEAD, W, 391, "res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });"), 'webhooks.ts :357-391 the /:id/test route (hard-coded test.ping; the outer catch echoing err.message)')
chk(at(HEAD, W, 427, 'export async function deliverWebhook(') and at(HEAD, W, 450, 'const result = await safeOutboundRequest(') and at(HEAD, W, 454, 'headers: {') and at(HEAD, W, 457, "'x-secuura-event': (payload as any).type || 'unknown',") and at(HEAD, W, 458, "'x-secuura-delivery': (payload as any).id || uuidv4(),") and at(HEAD, W, 459, "'User-Agent': 'Secuura-Webhooks/1.0',"), 'webhooks.ts :427 deliverWebhook / :450 the call / :454-459 the headers (:457-458 the two caller-influenced values)')
chk(w[w.index('export async function deliverWebhook('):w.index('export async function dispatchEvent(')].count('try {') == 0, 'deliverWebhook has NO try/catch of its own (the reach premise)')
chk(at(HEAD, W, 474, "if (result.reason === 'blocked') {") and at(HEAD, W, 475, "logger.warn('webhook delivery blocked by SSRF guard', { url, reason: result.error });") and at(HEAD, W, 480, "error: `blocked by SSRF guard: ${result.error}`,") and at(HEAD, W, 483, "logger.warn('webhook delivery failed', { url, reason: result.error });") and at(HEAD, W, 489, '};'), 'webhooks.ts :474-489 the tag branch (G-5 ii)')
chk(at(HEAD, W, 503, 'export async function dispatchEvent(') and at(HEAD, W, 508, 'try {') and at(HEAD, W, 543, '} catch (err: any) {') and at(HEAD, W, 544, "logger.warn('Webhook dispatch failed', { eventType, error: err.message });") and at(HEAD, W, 545, 'return 0;'), 'webhooks.ts :503 dispatchEvent / :508 its try / :543-545 its catch (returns 0)')
chk(w.count("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });") == 7, 'the err.message-echoing 500 occurs at 7 sites in the router (8f)')
chk(git('grep', '-n', '-i', 'dispatchEvent(', HEAD, '--', D + 'services').count('\n') == 1 and 'webhooks.ts:503' in git('grep', '-n', '-i', 'dispatchEvent(', HEAD, '--', D + 'services'), 'dispatchEvent( has exactly 1 hit across services at head = its definition (0 product call sites; positive control = the definition)')
# the originate jest file + the m365 call site
OT = OR + '__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts'; ot = text(HEAD, OT)
chk(len(lines(HEAD, OT)) == 115 and at(HEAD, OT, 21, "jest.mock('../db'") and at(HEAD, OT, 29, 'const mockSafeOutboundRequest = jest.fn();') and at(HEAD, OT, 36, 'safeOutboundRequest: (...args: unknown[]) => mockSafeOutboundRequest(...args),') and at(HEAD, OT, 38, ');') and ot.count("  it('") == 4, 'originate ks914 test 114 lines / :21-38 the mock preamble / 4 cells — it MOCKS the guard')
M = D + 'services/m365-integration/src/index.ts'
chk(at(HEAD, M, 1236, 'const result = await safeOutboundRequest(wh.webhook_url, {') and at(HEAD, M, 1263, '} catch { failed.push(wh.id); }'), 'm365 index.ts :1236 the call / :1263 its own catch')
chk(git('grep', '-n', 'safeOutboundRequest(', HEAD, '--', D + 'services', D + 'packages').count('\n') == 11 and git('grep', '-n', '-i', 'safeoutboundrequest(', HEAD, '--', D + 'services', D + 'packages').count('\n') == 12, 'safeOutboundRequest( 11 case-sensitive hits across services+packages at head (the definition, the 2 call sites, 8 calls in the shipped test) — the -i control reads 12 (+ the originate mock name)')
# --- git-side: parents, merge-bases, counts, numstats, trees ---
chk(git('log', '-1', '--format=%P', HEAD).split() == [P7D8, M45], 'head parents = 7d8a3f0e4 + M45')
chk(git('rev-parse', HEAD + '^{tree}').strip() == '0550765442fd2e86120c94c002cdcec95ae8a916', 'head tree 055076544 (= the builder\'s merge-tree prediction)')
chk(git('merge-base', M45, HEAD).strip() == M45 and rc('merge-base', '--is-ancestor', M45, HEAD) == 0, 'M45 is an ancestor of the head (merge-base = M45)')
chk(git('merge-base', M46, HEAD).strip() == M45 and rc('merge-base', '--is-ancestor', M46, HEAD) == 1, 'M46 is NOT an ancestor of the head; merge-base head/M46 = M45')
chk(rc('merge-base', '--is-ancestor', P7D8, HEAD) == 0 and rc('merge-base', '--is-ancestor', FF52, P7D8) == 0, '7d8a3f0e4 is an ancestor of the head; ff5218867 of 7d8a3f0e4')
chk(git('rev-list', '--count', f'{M45}..{HEAD}').strip() == '2' and git('rev-list', '--count', f'{HEAD}..{M46}').strip() == '1', 'rev-list --count M45..head = 2, head..M46 = 1')
ns = sorted((l.split('\t') for l in git('diff', '--numstat', M45, HEAD).strip().split('\n') if l.count('\t') == 2), key=lambda x: x[2])   # an empty numstat reads as [] (a FAIL, not a crash)
chk([x[:2] for x in ns] == [['44', '0'], ['42', '4']] and len(ns) == 2, 'numstat M45..head = 44/0 (the test) + 42/4 (the guard), 2 files')
chk(git('diff', '--name-only', f'{M46}...{HEAD}').split() == git('diff', '--name-only', M45, HEAD).split() and len(git('diff', '--name-only', M45, HEAD).split()) == 2, 'three-dot M46...head == two-dot M45 head == the 2 files')
chk(git('diff', '--name-only', M45, M46).split() == [D + 'docs/KS-926-CHECKS-THAT-CANNOT-FAIL.md'], 'M45..M46 delta = the one docs file')
chk(git('log', '-1', '--format=%h', P7D8).strip() == '7d8a3f0e4' and git('log', '-1', '--format=%s', M46).strip().startswith('KS-926: state the family'), '7d8a3f0e4 abbreviates as stated; M46 is the #874 squash')
# --- the API: the PR + Peter's comments + the builder's answer + the sibling #922 ---
pr = get('/pulls/873'); body = pr.get('body') or ''
chk(pr['state'] == 'open' and not pr['draft'] and pr['head']['sha'] == 'c624c9a8dd24129dad46cf7a204ae75ecb875dc3' and pr['commits'] == 2 and pr['changed_files'] == 2 and pr['additions'] == 86 and pr['deletions'] == 4, 'PR #873 open, head c624c9a8d, 2 commits, 2 files, +86 -4')
chk(len(body) == 9916 and body.count('@') == 1 and body.count('<!--ack:schemathesis-->') == 1 and body.count('<!--ack:akto-->') == 1 and body.count('Closes KS-931') == 1 and body.count('pending author confirmation') == 0 and body.count('## Test Evidence') == 1 and body.index('@') < body.index('## Test Evidence'), 'PR body 9,916 chars / 1 at-sign above Test Evidence / ack markers 1+1 / Closes KS-931 1 / pending 0')
revs = get('/pulls/873/reviews?per_page=100'); rcs = get('/pulls/873/comments?per_page=100'); ics = get('/issues/873/comments?per_page=100')
chk(len(revs) == 0 and len(rcs) == 0, 'no review objects and no review comments on #873 (Peter reviewed by issue comment)')
byid = {c['id']: c for c in ics}
chk(5602055926 in byid and byid[5602055926]['user']['login'] == 'PeterObeden' and len(byid[5602055926]['body']) == 7145 and 'write' in byid[5602055926]['body'] and 'looks unreachable given the declared type' in byid[5602055926]['body'], "Peter's comment 5602055926 (7,145 chars) carries the write/end observation")
chk(5602110186 in byid and byid[5602110186]['user']['login'] == 'PeterObeden' and len(byid[5602110186]['body']) == 6696 and 'git archive ff5218867' in byid[5602110186]['body'] and '787 passed (787)' in byid[5602110186]['body'], "Peter's comment 5602110186 (6,696 chars) carries the git-archive method and 787")
chk(5662500697 in byid and byid[5662500697]['user']['login'] == 'kksecura' and len(byid[5662500697]['body']) == 4326 and byid[5662500697]['body'].count('@') == 0 and 'a one-line comment correction is a separate polish if wanted' in byid[5662500697]['body'], "the builder's answer 5662500697 (4,326 chars, 0 at-signs) records item 3")
c = get('/compare/develop...c624c9a8dd24129dad46cf7a204ae75ecb875dc3')
chk(c['merge_base_commit']['sha'] == M45 and c['ahead_by'] == 2 and len(c['files']) == 2 and sorted(f['sha'][:9] for f in c['files']) == ['5a838e0d6', '69706c1ef'], 'compare develop...head = merge_base M45, ahead 2, files 2 (the two lane blobs)')
f922 = get('/pulls/922/files?per_page=100'); by922 = {f['filename']: f['sha'] for f in f922}
chk(by922.get(SH + 'src/__tests__/ks256-spec-example-contract.test.ts') == '72533d3b01a4941578b1f777f0def3f9ec9ea6f0' and by922.get(SH + 'src/openapi/examples/fixtures.ts') == 'b54d26929c564d9cd4e2e2f27da12df6d6d85325' and len(f922) == 5 and get('/pulls/922')['state'] == 'open', '#922 (open) touches exactly the two packages/shared files in DEV_CONTENT_ALLOWED at the pinned blobs')
# --- Linear: KS-931 + attachments ---
def gql(q, v):
    return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': lkey, 'Content-Type': 'application/json'}), timeout=60))
i = gql('query($id:String!){ issue(id:$id){ identifier state{name} relations{nodes{relatedIssue{identifier}}} comments(first:50){nodes{id createdAt body}} attachments(first:50){nodes{url}} } }', {'id': 'KS-931'})['data']['issue']
cs = sorted(i['comments']['nodes'], key=lambda x: x['createdAt'])
chk(i['state']['name'] == 'In Review' and [r['relatedIssue']['identifier'] for r in i['relations']['nodes']] == ['KS-1000'] and len(cs) == 3 and cs[-1]['id'].startswith('e96239ac') and sum(x['body'].count('@') for x in cs) == 0, 'KS-931 In Review, relation KS-1000 only, 3 comments (last e96239ac), 0 at-signs')
atts = [a['url'] for a in i['attachments']['nodes'] if '/pull/' in a['url']]
chk(atts == ['https://github.com/Secuura/Distributed_Secuura/pull/873'] or (len(atts) == 1 and atts[0].endswith('/pull/873')), f'KS-931 PR attachments = #873 only ({atts})')
att_ctl = gql('query($u:String!){ attachmentsForURL(url:$u){ nodes{ issue{identifier} } } }', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/873'})['data']['attachmentsForURL']['nodes']
chk([a['issue']['identifier'] for a in att_ctl] == ['KS-931'], f'attachmentsForURL(/pull/873) -> KS-931 alone ({[a["issue"]["identifier"] for a in att_ctl]})')
# negative-token arm
if arg == '--neg-token':
    chk(cnt(HEAD, TEST, 'rebind.example') == 1, 'NEG: a rebind cell demanded PRESENT in the shipped file (known 0)')
    chk(g.count(A1) == 0, 'NEG: the T1 anchor demanded ABSENT at head (known 1)')
print(f'TALLY ok={ok} FAILS={fail} live_develop={live[:9]} {datetime.datetime.now().astimezone().strftime("%H:%M:%S")}')
sys.exit(1 if fail else 0)
PY
