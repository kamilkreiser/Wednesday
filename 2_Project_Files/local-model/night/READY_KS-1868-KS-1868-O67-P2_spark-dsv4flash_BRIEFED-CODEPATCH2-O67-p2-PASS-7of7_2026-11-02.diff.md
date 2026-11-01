# READY — KS-1868-KS-1868-O67-P2 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 09:52 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:52 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `cde2dee4dffba6a61228c40d641ff567660c32b2`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/signatories.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/signatories.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/originate/src/routes/signatories.ts
139	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: signatories.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/signatories.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/signatories.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts 139 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/signatories.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=6 of total=12; red cell(s): ['KS-1868 PATCH /:id catch reads the thrown value safely RED ks1868 R1 PATCH /:id: a revoked Proxy thrown by the database is logged as a constant reason and answered with the constant 500', 'KS-1868 PATCH /:id catch reads the thrown value safely RED ks1868 R2 PATCH /:id: an Error whose message getter throws is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /:id/revoke catch reads the thrown value safely RED ks1868 R1 POST /:id/revoke: a revoked Proxy thrown by the database is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /:id/revoke catch reads the thrown value safely RED ks1868 R2 POST /:id/revoke: an Error whose message getter throws is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /:id/reinstate catch reads the thrown value safely RED ks1868 R1 POST /:id/reinstate: a revoked Proxy thrown by the database is logged as a constant reason and answered with the constant 500', 'KS-1868 POST /:id/reinstate catch reads the thrown value safely RED ks1868 R2 POST /:id/reinstate: an Error whose message getter throws is logged as a constant reason and answered with the constant 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1999 failed=0 | after: total=2011 failed=0` · `NEW reds: []` [baseline_suite.json total=1999 failed=0; after_suite.json total=2011 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/signatories.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts` (+139/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/signatories.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `cde2dee4dffba6a61228c40d641ff567660c32b2` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/signatories.ts b/Blockchain/Dev/services/originate/src/routes/signatories.ts
--- a/Blockchain/Dev/services/originate/src/routes/signatories.ts
+++ b/Blockchain/Dev/services/originate/src/routes/signatories.ts
@@ -355,6 +355,12 @@
       res.json({ success: true, message: 'Signatory updated' });
     } catch (error) {
-      logger.error('Failed to update signatory', { error: String(error) });
+      let reason: string;
+      try {
+        reason = String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to update signatory', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update signatory' } });
     }
   },
@@ -412,7 +418,13 @@
         revokedAt: now.toISOString(),
       });
     } catch (error) {
-      logger.error('Failed to revoke signatory', { error: String(error) });
+      let reason: string;
+      try {
+        reason = String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to revoke signatory', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to revoke signatory' } });
     }
   },
@@ -462,6 +474,12 @@
       res.json({ success: true, message: 'Signatory reinstated' });
     } catch (error) {
-      logger.error('Failed to reinstate signatory', { error: String(error) });
+      let reason: string;
+      try {
+        reason = String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to reinstate signatory', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to reinstate signatory' } });
     }
   },
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-signatories-write-routes-p2-unreadable-throw.test.ts
@@ -0,0 +1,139 @@
+process.env.NODE_ENV = 'development';
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+
+const mockQueryRaw = jest.fn();
+const mockExecuteRaw = jest.fn();
+const mockExecuteRawUnsafe = jest.fn();
+const mockLoggerError = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw, $executeRawUnsafe: mockExecuteRawUnsafe },
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { signatoriesRouter } from '../routes/signatories';
+// KS-1868 (originate routes/signatories.ts): the catch blocks of these routes logged `String(error)` themselves and then answered the constant 500. When the thrown value cannot be read
+// (a revoked Proxy; an Error whose `message` getter throws), String() threw INSIDE the catch: the handler's promise rejected and the request got NO answer. Each catch now reads the value
+// inside its own try and logs the constant reason `unreadable thrown value`. The database stand-in rejects with the thrown value on a real loopback listener; a request that gets no answer
+// within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
+const UNREADABLE = 'unreadable thrown value';
+const ACTOR = '11111111-1111-4111-8111-111111111111';
+
+const body500 = (message: string) => ({ success: false, error: { code: 'INTERNAL_ERROR', message } });
+
+const ROUTES = [
+  {
+    route: 'PATCH /:id',
+    method: 'PATCH',
+    path: '/11111111-1111-4111-8111-111111111111',
+    db: () => mockExecuteRawUnsafe,
+    context: 'Failed to update signatory',
+    message: 'Failed to update signatory', payload: { displayName: 'Ks Name' },
+  },
+  {
+    route: 'POST /:id/revoke',
+    method: 'POST',
+    path: '/11111111-1111-4111-8111-111111111111/revoke',
+    db: () => mockExecuteRaw,
+    context: 'Failed to revoke signatory',
+    message: 'Failed to revoke signatory', payload: { reason: 'ks1868' },
+  },
+  {
+    route: 'POST /:id/reinstate',
+    method: 'POST',
+    path: '/11111111-1111-4111-8111-111111111111/reinstate',
+    db: () => mockExecuteRaw,
+    context: 'Failed to reinstate signatory',
+    message: 'Failed to reinstate signatory', payload: undefined,
+  },
+];
+
+
+const app = express();
+app.use(express.json());
+app.use((req, _res, next) => {
+  (req as any).user = { userId: ACTOR, email: 'ks1868@example.test' };
+  next();
+});
+app.use('/api/signatories', signatoriesRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => server?.close());
+beforeEach(() => jest.resetAllMocks());
+
+async function callWithThrow(c: (typeof ROUTES)[number], thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  c.db().mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(baseUrl + '/api/signatories' + c.path, {
+      method: c.method,
+      headers: { 'content-type': 'application/json' },
+      body: c.method === 'GET' ? undefined : JSON.stringify(c.payload ?? {}),
+      signal: AbortSignal.timeout(1500),
+    });
+    return { status: res.status, body: await res.json() };
+  } catch {
+    return { status: 'NO ANSWER', body: null };
+  }
+}
+
+function revokedProxy(): object {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+function throwingMessageError(): Error {
+  const e = new Error('ks1868 hidden');
+  Object.defineProperty(e, 'message', {
+    get() {
+      throw new Error('ks1868 message getter');
+    },
+  });
+  return e;
+}
+
+describe.each(ROUTES)('KS-1868 $route catch reads the thrown value safely', (c) => {
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy thrown by the database is logged as a constant reason and answered with the constant 500`, async () => {
+    const reply = await callWithThrow(c, revokedProxy());
+    expect(reply).toEqual({ status: 500, body: body500(c.message) });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+    expect(c.db()).toHaveBeenCalledTimes(1);
+  });
+
+  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws is logged as a constant reason and answered with the constant 500`, async () => {
+    const reply = await callWithThrow(c, throwingMessageError());
+    expect(reply).toEqual({ status: 500, body: body500(c.message) });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+    expect(c.db()).toHaveBeenCalledTimes(1);
+  });
+
+  it(`control ks1868 C1 ${c.route}: an ordinary Error is logged as before (String of the Error) and the answer is the constant 500`, async () => {
+    const reply = await callWithThrow(c, new Error('ks1868 ordinary'));
+    expect(reply).toEqual({ status: 500, body: body500(c.message) });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'Error: ks1868 ordinary' }]]);
+    expect(c.db()).toHaveBeenCalledTimes(1);
+  });
+
+  it(`control ks1868 C2 ${c.route}: a thrown string is logged as itself, as before`, async () => {
+    const reply = await callWithThrow(c, 'ks1868 plain string');
+    expect(reply).toEqual({ status: 500, body: body500(c.message) });
+    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 plain string' }]]);
+    expect(c.db()).toHaveBeenCalledTimes(1);
+  });
+});
```
