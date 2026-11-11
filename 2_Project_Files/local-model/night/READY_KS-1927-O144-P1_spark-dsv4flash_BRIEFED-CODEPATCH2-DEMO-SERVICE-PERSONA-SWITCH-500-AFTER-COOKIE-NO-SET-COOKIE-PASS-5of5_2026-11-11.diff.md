# READY — KS-1927-O144-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1927_o144_p1_demo_service_persona_switch_500_after_the_cookie_carries_no_set_cookie/out.md.checker/patch.diff`** (from `ls` at 22:16 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1927_o144_p1_demo_service_persona_switch_500_after_the_cookie_carries_no_set_cookie/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1927_o144_p1_demo_service_persona_switch_500_after_the_cookie_carries_no_set_cookie/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1927_o144_p1_demo_service_persona_switch_500_after_the_cookie_carries_no_set_cookie/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 22:16 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1927_o144_p1_demo_service_persona_switch_500_after_the_cookie_carries_no_set_cookie/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2e998b8d9aeaeaa6e87a35d933c6f0445bb981d4`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/demo-service/src/routes/persona.ts } + { Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/demo-service/src/routes/persona.ts` (product) and `Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	0	Blockchain/Dev/services/demo-service/src/routes/persona.ts
100	0	Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (5 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: persona.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/demo-service/src/routes/persona.ts`; test(s): `Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/demo-service/src/routes/persona.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts 100 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/demo-service/src/routes/persona.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1927 a failed persona switch does not hand out the refresh-token cookie RED ks1927 R1: a user that cannot be serialised (a BigInt) answers the generic 500 with no cookie', 'KS-1927 a failed persona switch does not hand out the refresh-token cookie RED ks1927 R2: a user whose toJSON throws answers the generic 500 with no cookie']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=103 failed=0 | after: total=108 failed=0` · `NEW reds: []` [baseline_suite.json total=103 failed=0; after_suite.json total=108 failed=0]
- A6 [verbatim]: `PASS A6 whole services/demo-service suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/demo-service: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/demo-service/src/routes/persona.ts` (+5/-0 per numstat.out) and the test file `Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts` (+100/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/demo-service/src/routes/persona.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2e998b8d9aeaeaa6e87a35d933c6f0445bb981d4` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1927_o144_p1_demo_service_persona_switch_500_after_the_cookie_carries_no_set_cookie/input.json`. Brief (given by --brief; its `# ` heading names KS-1927): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1927_o144_p1_demo_service_persona_switch_500_after_the_cookie_carries_no_set_cookie/KS-1927.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1927_o144_p1_demo_service_persona_switch_500_after_the_cookie_carries_no_set_cookie/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/demo-service/src/routes/persona.ts b/Blockchain/Dev/services/demo-service/src/routes/persona.ts
--- a/Blockchain/Dev/services/demo-service/src/routes/persona.ts
+++ b/Blockchain/Dev/services/demo-service/src/routes/persona.ts
@@ -39,2 +39,4 @@
 personaRouter.post('/persona/switch', async (req: Request, res: Response) => {
+  // KS-1927: set once the auth service's refresh-token cookie has been copied onto the response, so the catch can take it off again.
+  let cookieCopied = false;
   try {
@@ -63,3 +65,4 @@
     if (authResult.setCookieHeader) {
       res.setHeader('Set-Cookie', authResult.setCookieHeader);
+      cookieCopied = true;
     }
@@ -85,3 +88,5 @@
     logger.error('Persona switch error', { error: message });
+    // KS-1927: a failure after the cookie was copied (building the success answer) must not hand that cookie out on the generic 500.
+    if (cookieCopied && !res.headersSent) res.removeHeader('Set-Cookie');
     return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
   }
diff --git a/Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts b/Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/demo-service/src/__tests__/ks1927-persona-switch-500-after-the-cookie-carries-no-set-cookie.test.ts
@@ -0,0 +1,100 @@
+import { describe, it, expect, vi, beforeEach, afterAll } from 'vitest';
+import express from 'express';
+
+// KS-1927: POST /demo-api/persona/switch copies the auth service's httpOnly refresh-token cookie onto the response BEFORE it builds
+// the success answer. If building the answer throws, the catch answers the generic 500 and, until the fix, the 500 still carried that
+// Set-Cookie. The cells run the real router on a real Express server over real HTTP. The auth call is a stand-in that resolves; the
+// throw after the cookie is raised by a user object that cannot be serialised (a BigInt, a toJSON that throws), which makes the
+// real res.json throw. Only the answer's headers are read; the cookie value is a harmless stand-in.
+const h = vi.hoisted(() => ({
+  result: undefined as unknown,
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() },
+  createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }),
+}));
+
+vi.mock('../services/authClient', () => ({
+  authenticatePersona: () => Promise.resolve(h.result),
+}));
+
+import { personaRouter } from '../routes/persona';
+
+const COOKIE = 'refresh_token=ks1927-standin; Path=/api/auth; HttpOnly';
+const GENERIC = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+
+const app = express();
+app.use(express.json());
+app.use('/demo-api', personaRouter);
+const server = app.listen(0, '127.0.0.1');
+const ready = new Promise<void>((resolve) => server.on('listening', () => resolve()));
+
+async function post(): Promise<{ status: number; body: unknown; cookies: string[] }> {
+  await ready;
+  const addr = server.address();
+  const port = typeof addr === 'object' && addr ? addr.port : 0;
+  const r = await fetch(`http://127.0.0.1:${port}/demo-api/persona/switch`, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify({ persona: 'alice' }),
+  });
+  return { status: r.status, body: await r.json(), cookies: r.headers.getSetCookie() };
+}
+
+afterAll(() => {
+  server.close();
+});
+
+describe('KS-1927 a failed persona switch does not hand out the refresh-token cookie', () => {
+  beforeEach(() => {
+    h.result = undefined;
+  });
+
+  it('control ks1927 C1: a good switch answers 200 and carries the cookie', async () => {
+    h.result = { success: true, accessToken: 'jwt', user: { id: 'u1' }, setCookieHeader: COOKIE };
+    const out = await post();
+    expect(out.status).toBe(200);
+    expect(out.cookies).toEqual([COOKIE]);
+  });
+
+  it('control ks1927 C2: a failed auth answers 502 and carries no cookie', async () => {
+    h.result = { success: false, error: 'no', setCookieHeader: COOKIE };
+    const out = await post();
+    expect(out.status).toBe(502);
+    expect(out.cookies).toEqual([]);
+  });
+
+  it('control ks1927 C3: a throw before the cookie is copied answers the generic 500 and carries no cookie', async () => {
+    h.result = null;
+    const out = await post();
+    expect(out.status).toBe(500);
+    expect(out.body).toEqual(GENERIC);
+    expect(out.cookies).toEqual([]);
+  });
+
+  it('RED ks1927 R1: a user that cannot be serialised (a BigInt) answers the generic 500 with no cookie', async () => {
+    h.result = { success: true, accessToken: 'jwt', user: { id: 'u1', big: BigInt(1) }, setCookieHeader: COOKIE };
+    const out = await post();
+    expect(out.status).toBe(500);
+    expect(out.body).toEqual(GENERIC);
+    expect(out.cookies).toEqual([]);
+  });
+
+  it('RED ks1927 R2: a user whose toJSON throws answers the generic 500 with no cookie', async () => {
+    h.result = {
+      success: true,
+      accessToken: 'jwt',
+      user: {
+        toJSON() {
+          throw new Error('toJSON boom');
+        },
+      },
+      setCookieHeader: COOKIE,
+    };
+    const out = await post();
+    expect(out.status).toBe(500);
+    expect(out.body).toEqual(GENERIC);
+    expect(out.cookies).toEqual([]);
+  });
+});
```

> NOTE (operator o144, 2026-11-11): TIER 2 (response headers on a generic 500). Cookie-flag design: removal is conditional on a flag so the merged ks1868 persona test (a res stub with no removeHeader) stays green. Wednesday: read the + lines (golden = mine, byte-identical). UNMEASURED: whether a browser keeps a cookie from a 500; no real trigger for the throw (ticket says so). Load at the real round started 10.5 rising to 18 (other seats); A6 demo-service suite 103 -> 108, 0 red.
