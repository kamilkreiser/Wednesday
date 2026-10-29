# READY — KS-1792-KS-1792 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1792_p1_github_no_access_token/out.md.checker/patch.diff`** (from `ls` at 09:51 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1792_p1_github_no_access_token/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1792_p1_github_no_access_token/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 09:51 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1792_p1_github_no_access_token/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `e3d8456ec81d0b02172dd5a3060404815e797bde`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/providers/social/github.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/providers/social/github.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	2	Blockchain/Dev/services/auth/src/providers/social/github.ts
74	0	Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: github.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/providers/social/github.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/providers/social/github.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts 74 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/providers/social/github.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1792: the GitHub adapter refuses a 200 token answer that has no access_token RED KS-1792 R1 a 200 error answer (bad_verification_code) is refused and /user is never called', 'KS-1792: the GitHub adapter refuses a 200 token answer that has no access_token RED KS-1792 R2 a 200 answer with an empty body object is refused and /user is never called', 'KS-1792: the GitHub adapter refuses a 200 token answer that has no access_token RED KS-1792 R3 a 200 answer whose access_token is not a string is refused and /user is never called']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1326 failed=0 | after: total=1331 failed=0` · `NEW reds: []` [baseline_suite.json total=1326 failed=0; after_suite.json total=1331 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/providers/social/github.ts` (+8/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts` (+74/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/providers/social/github.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `e3d8456ec81d0b02172dd5a3060404815e797bde` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1792_p1_github_no_access_token/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1792_p1_github_no_access_token/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/providers/social/github.ts b/Blockchain/Dev/services/auth/src/providers/social/github.ts
--- a/Blockchain/Dev/services/auth/src/providers/social/github.ts
+++ b/Blockchain/Dev/services/auth/src/providers/social/github.ts
@@ -86,5 +86,11 @@
-    const { access_token } = (await tokenRes.json()) as { access_token: string };
-
+    // KS-1792: GitHub answers a bad or expired code with HTTP 200 and an {error, error_description} body, so the !ok branch above never sees it. Refuse an answer that has no usable
+    // access_token (or that carries an error field) here, as a token-exchange failure, before any profile call: the guard must not be GitHub's 401 for `Bearer undefined`.
+    const tokenBody = (await tokenRes.json()) as { access_token?: unknown; error?: unknown };
+    if (typeof tokenBody.access_token !== 'string' || tokenBody.access_token === '' || tokenBody.error !== undefined) {
+      logger.warn('GitHub token endpoint answered 200 without an access token', { provider: 'github', error: typeof tokenBody.error === 'string' ? tokenBody.error.slice(0, 80) : undefined });
+      throw new Error('GitHub token exchange failed (no access token)');
+    }
+    const access_token = tokenBody.access_token;
     const profileRes = await fetch('https://api.github.com/user', {
       headers: { Authorization: `Bearer ${access_token}`, Accept: 'application/json' },
       signal: AbortSignal.timeout(PROVIDER_TIMEOUT_MS),
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1792-github-refuses-a-token-answer-without-an-access-token.test.ts
@@ -0,0 +1,74 @@
+// KS-1792: GitHub answers a bad or expired sign-in code with HTTP 200 and an {error, error_description} body. The adapter used to read access_token from it unchecked and call /user with
+// `Bearer undefined`, relying on GitHub answering that 401. GitHubProvider.exchangeCode now refuses such an answer before any profile call. fetch is replaced by a recording stub, so no
+// socket is opened; a good token answer is the control.
+import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
+
+const { silentLogger } = vi.hoisted(() => ({
+  silentLogger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() },
+}));
+vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
+
+import { GitHubProvider } from '../providers/social/github';
+
+const CONFIG = { clientId: 'cid-ks1792', clientSecret: 'secret-ks1792', callbackUrl: 'https://app.test/cb', enabled: true };
+
+let calls: string[];
+
+type Answer = { status: number; body: unknown };
+
+// A recording stub keyed by URL: the token endpoint answers `token`, api.github.com/user answers `user` (default: GitHub's own 401 for a bad bearer), anything else 404.
+function stubFetch(token: Answer, user: Answer = { status: 401, body: { message: 'Bad credentials' } }) {
+  calls = [];
+  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
+    calls.push(String(url));
+    const a = String(url).includes('/login/oauth/access_token') ? token : String(url).endsWith('/user') ? user : { status: 404, body: {} };
+    return new Response(JSON.stringify(a.body), { status: a.status, headers: { 'content-type': 'application/json' } });
+  }));
+}
+
+// The message exchangeCode rejects with, or 'RESOLVED' if it did not reject: a plain value, so a wrong answer fails by assertion.
+async function refusal(code: string): Promise<string> {
+  return new GitHubProvider(CONFIG).exchangeCode(code).then(() => 'RESOLVED', (e: Error) => e.message);
+}
+
+beforeEach(() => { vi.clearAllMocks(); });
+afterEach(() => { vi.unstubAllGlobals(); });
+
+describe('KS-1792: the GitHub adapter refuses a 200 token answer that has no access_token', () => {
+  it('RED KS-1792 R1 a 200 error answer (bad_verification_code) is refused and /user is never called', async () => {
+    stubFetch({ status: 200, body: { error: 'bad_verification_code', error_description: 'The code passed is incorrect or expired.' } });
+    expect(await refusal('bad')).toBe('GitHub token exchange failed (no access token)');
+    expect(calls).toEqual(['https://github.com/login/oauth/access_token']);
+  });
+
+  it('RED KS-1792 R2 a 200 answer with an empty body object is refused and /user is never called', async () => {
+    stubFetch({ status: 200, body: {} });
+    expect(await refusal('bad')).toBe('GitHub token exchange failed (no access token)');
+    expect(calls).toEqual(['https://github.com/login/oauth/access_token']);
+  });
+
+  it('RED KS-1792 R3 a 200 answer whose access_token is not a string is refused and /user is never called', async () => {
+    stubFetch({ status: 200, body: { access_token: 42 } });
+    expect(await refusal('bad')).toBe('GitHub token exchange failed (no access token)');
+    expect(calls).toEqual(['https://github.com/login/oauth/access_token']);
+  });
+
+  it('CONTROL KS-1792 C1 a good token answer still signs in: the profile call carries the Bearer token', async () => {
+    stubFetch(
+      { status: 200, body: { access_token: 'tok-ks1792' } },
+      { status: 200, body: { id: 7, email: 'a@secuura.test', name: 'Ada Lovelace', login: 'ada' } },
+    );
+    const profile = await new GitHubProvider(CONFIG).exchangeCode('good');
+    expect(profile.providerId).toBe('7');
+    expect(profile.email).toBe('a@secuura.test');
+    expect(calls).toEqual(['https://github.com/login/oauth/access_token', 'https://api.github.com/user']);
+    const profileInit = (vi.mocked(fetch).mock.calls[1] as unknown as [string, { headers: Record<string, string> }])[1];
+    expect(profileInit.headers.Authorization).toBe('Bearer tok-ks1792');
+  });
+
+  it('CONTROL KS-1792 C2 a non-2xx token answer is still the status-only failure', async () => {
+    stubFetch({ status: 400, body: { error: 'bad_verification_code' } });
+    expect(await refusal('bad')).toBe('GitHub token exchange failed (HTTP 400)');
+  });
+});
```
