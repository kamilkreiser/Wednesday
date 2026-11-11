# READY — KS-1868-KS-1868-O137-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o137_p1_originate_anchors_write_route_catches_guard_the_thrown_value_read/out.md.checker/patch.diff`** (from `ls` at 15:37 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o137_p1_originate_anchors_write_route_catches_guard_the_thrown_value_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o137_p1_originate_anchors_write_route_catches_guard_the_thrown_value_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o137_p1_originate_anchors_write_route_catches_guard_the_thrown_value_read/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 15:37 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o137_p1_originate_anchors_write_route_catches_guard_the_thrown_value_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/anchors.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/anchors.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/originate/src/routes/anchors.ts
150	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: anchors.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/anchors.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/anchors.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts 150 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/anchors.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=4 of total=7; red cell(s): ['KS-1868 the originate anchor write catches log text for an unreadable thrown value RED ks1868 R1 POST /api/anchors: a revoked Proxy is logged as the constant reason and the route answers 500', 'KS-1868 the originate anchor write catches log text for an unreadable thrown value RED ks1868 R2 POST /api/anchors: an object whose toString throws is logged as the constant reason and the route answers 500', 'KS-1868 the originate anchor write catches log text for an unreadable thrown value RED ks1868 R3 POST /api/anchors/submit: a revoked Proxy is logged as the constant reason and the route answers 500', 'KS-1868 the originate anchor write catches log text for an unreadable thrown value RED ks1868 R4 POST /api/anchors/submit: an object whose toString throws is logged as the constant reason and the route answers 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2592 failed=11 | after: total=2599 failed=11` · `NEW reds: []` [baseline_suite.json total=2592 failed=11; after_suite.json total=2599 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/anchors.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts` (+150/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/anchors.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o137_p1_originate_anchors_write_route_catches_guard_the_thrown_value_read/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o137_p1_originate_anchors_write_route_catches_guard_the_thrown_value_read/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o137_p1_originate_anchors_write_route_catches_guard_the_thrown_value_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/anchors.ts b/Blockchain/Dev/services/originate/src/routes/anchors.ts
--- a/Blockchain/Dev/services/originate/src/routes/anchors.ts
+++ b/Blockchain/Dev/services/originate/src/routes/anchors.ts
@@ -340,4 +340,10 @@
     } catch (error) {
-      logger.error('Failed to create anchor', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = String(error instanceof Error ? error.message : error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to create anchor', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create anchor' } });
     }
@@ -435,4 +441,10 @@
     } catch (error) {
-      logger.error('Failed to submit anchor', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = String(error instanceof Error ? error.message : error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to submit anchor', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to submit anchor' } });
     }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-write-route-catches-unreadable-throw.test.ts
@@ -0,0 +1,150 @@
+// KS-1868 (originate anchors.ts, the two WRITE routes): the catches of POST /api/anchors and POST /api/anchors/submit log
+// `error: error instanceof Error ? error.message : String(error)` UNGUARDED, where the GET route and verifyAnchorsDbReady in the same file
+// already guard the read (a revoked Proxy throws on `instanceof`; an object whose toString throws throws on String()). A caught value like
+// that made the catch itself throw before its log line, and an Express 4 async handler that rejects answers nothing: the request hangs.
+// The cells raise the value from inside each route's try (the authenticated principal's `userId` getter throws it, so no network and no
+// database is involved) and assert the route still answers its constant 500, logs the constant reason and leaves no unhandled rejection.
+// Controls: an ordinary Error and a thrown plain string are logged as their own text. Harness: the ks1868 anchors test (same mocks; real
+// router, real loopback server; the abort signal turns a hang into a null answer).
+const mockState: { toThrow: unknown; errored: unknown[][] } = { toThrow: undefined, errored: [] };
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: (..._args: unknown[]) => Promise.resolve([]),
+    $executeRaw: (..._args: unknown[]) => Promise.resolve(0),
+  },
+  getTenantManager: jest.fn(() => null),
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user =
+      mockState.toThrow === undefined
+        ? { userId: '11111111-2222-4333-8444-555555555555', role: 'ISSUER_ADMIN' }
+        : {
+            get userId(): string {
+              throw mockState.toThrow;
+            },
+            role: 'ISSUER_ADMIN',
+          };
+    next();
+  },
+}));
+
+jest.mock('../middleware/rbac', () => ({ isAllowedByRoleOrScope: () => true }));
+
+jest.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    debug: () => undefined,
+    warn: () => undefined,
+    error: (...args: unknown[]) => {
+      mockState.errored.push(args);
+    },
+  },
+}));
+
+import express from 'express';
+import { anchorsRouter } from '../routes/anchors';
+
+const app = express();
+app.use('/api/anchors', express.json(), anchorsRouter);
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+let unhandled = 0;
+const onUnhandled = () => {
+  unhandled += 1;
+};
+
+beforeAll(async () => {
+  process.on('unhandledRejection', onUnhandled);
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => {
+  process.removeListener('unhandledRejection', onUnhandled);
+  server?.close();
+});
+
+beforeEach(() => {
+  mockState.toThrow = undefined;
+  mockState.errored.length = 0;
+  unhandled = 0;
+});
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+const toStringThrows = (): unknown => ({
+  toString() {
+    throw new Error('ts boom');
+  },
+});
+const reasonOf = (c: unknown[] | undefined): string => {
+  const v = (c?.[1] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+
+async function post(path: string, body: unknown): Promise<{ status: number; code: string | undefined } | null> {
+  try {
+    const res = await fetch(`${baseUrl}/api/anchors${path}`, {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json' },
+      body: JSON.stringify(body),
+      signal: AbortSignal.timeout(1500),
+    });
+    const data = (await res.json()) as { error?: { code?: string } };
+    return { status: res.status, code: data.error?.code };
+  } catch {
+    return null;
+  }
+}
+type Door = { path: string; body: unknown; line: string };
+const CREATE: Door = { path: '', body: { documentId: 'doc-ks1868-write', contentHash: 'a'.repeat(64) }, line: 'Failed to create anchor' };
+const SUBMIT: Door = { path: '/submit', body: { documentHash: 'a'.repeat(64) }, line: 'Failed to submit anchor' };
+
+async function run(door: Door, thrown: unknown, reason: string): Promise<void> {
+  mockState.toThrow = thrown;
+  expect(await post(door.path, door.body)).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+  expect(unhandled).toBe(0);
+  expect(mockState.errored).toHaveLength(1);
+  expect(mockState.errored[0][0]).toBe(door.line);
+  expect(reasonOf(mockState.errored[0])).toBe(reason);
+}
+
+describe('KS-1868 the originate anchor write catches log text for an unreadable thrown value', () => {
+  it('control ks1868 C1 POST /api/anchors: an ordinary Error is logged with its own message and the route answers 500', async () => {
+    await run(CREATE, new Error('boom create'), 'boom create');
+  });
+
+  it('control ks1868 C2 POST /api/anchors/submit: an ordinary Error is logged with its own message and the route answers 500', async () => {
+    await run(SUBMIT, new Error('boom submit'), 'boom submit');
+  });
+
+  it('control ks1868 C3 POST /api/anchors: a thrown plain string is logged as its own text and the route answers 500', async () => {
+    await run(CREATE, 'plain boom', 'plain boom');
+  });
+
+  it('RED ks1868 R1 POST /api/anchors: a revoked Proxy is logged as the constant reason and the route answers 500', async () => {
+    await run(CREATE, revokedProxy(), 'unreadable thrown value');
+  });
+
+  it('RED ks1868 R2 POST /api/anchors: an object whose toString throws is logged as the constant reason and the route answers 500', async () => {
+    await run(CREATE, toStringThrows(), 'unreadable thrown value');
+  });
+
+  it('RED ks1868 R3 POST /api/anchors/submit: a revoked Proxy is logged as the constant reason and the route answers 500', async () => {
+    await run(SUBMIT, revokedProxy(), 'unreadable thrown value');
+  });
+
+  it('RED ks1868 R4 POST /api/anchors/submit: an object whose toString throws is logged as the constant reason and the route answers 500', async () => {
+    await run(SUBMIT, toStringThrows(), 'unreadable thrown value');
+  });
+});
```
