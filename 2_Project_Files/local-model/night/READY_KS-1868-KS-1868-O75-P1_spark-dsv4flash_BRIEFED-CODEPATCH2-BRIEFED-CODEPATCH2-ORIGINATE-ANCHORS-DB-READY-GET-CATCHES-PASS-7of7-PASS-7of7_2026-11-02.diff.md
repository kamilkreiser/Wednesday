# READY — KS-1868-KS-1868-O75-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 13:31 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:31 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `04ff5262ad526a13c1a0df99480b76860a8d11d1`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/anchors.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/anchors.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/originate/src/routes/anchors.ts
145	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: anchors.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/anchors.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/anchors.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts 145 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/anchors.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 the originate anchor catches read the rejection value safely RED ks1868 R1 GET /:documentId: a revoked Proxy rejection logs both lines with a constant reason and the route answers 500', 'KS-1868 the originate anchor catches read the rejection value safely RED ks1868 R2 GET /:documentId: an Error whose message getter throws logs both lines with a constant reason and the route answers 500', 'KS-1868 the originate anchor catches read the rejection value safely RED ks1868 R3 verifyAnchorsDbReady: a revoked Proxy rejection logs a constant reason and the constant error is thrown', 'KS-1868 the originate anchor catches read the rejection value safely RED ks1868 R4 verifyAnchorsDbReady: an Error whose message getter throws logs a constant reason and the constant error is thrown']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1999 failed=0 | after: total=2005 failed=0` · `NEW reds: []` [baseline_suite.json total=1999 failed=0; after_suite.json total=2005 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/anchors.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts` (+145/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/anchors.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `04ff5262ad526a13c1a0df99480b76860a8d11d1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/anchors.ts b/Blockchain/Dev/services/originate/src/routes/anchors.ts
--- a/Blockchain/Dev/services/originate/src/routes/anchors.ts
+++ b/Blockchain/Dev/services/originate/src/routes/anchors.ts
@@ -48,8 +48,14 @@
     await prisma.$queryRaw`SELECT 1`;
     logger.info('anchors: database connection verified');
   } catch (err: any) {
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.error('anchors: database connection FAILED — anchor operations will not be available', {
-      error: err instanceof Error ? err.message : String(err),
+      error: reason,
     });
     throw new Error('Database is required for anchor operations');
   }
@@ -88,7 +94,13 @@
     if (rows.length > 0) return anchorFromDbRow(rows[0]);
     return null;
   } catch (err: any) {
-    logger.warn('Failed to fetch anchor from DB', { documentId, error: err instanceof Error ? err.message : String(err) });
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('Failed to fetch anchor from DB', { documentId, error: reason });
     // KS-1657: this catch returned null, and the only caller (GET /:documentId) reads null as "no anchor on record" and answers 404
     // with `anchored: false`. A failed read and a genuine absence were therefore one answer. Rethrow so the fault reaches the route's own
     // catch (a constant 500); null now means one thing only, zero rows. The warn log above is kept. Kam, 2026-10-28: "a — Fix it".
@@ -200,7 +212,13 @@
         verified: !simulated,
       });
     } catch (error) {
-      logger.error('Failed to get anchor', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to get anchor', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get anchor' } });
     }
   }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts
@@ -0,0 +1,145 @@
+// KS-1868: the originate anchor routes read a rejection value in three catch blocks. When the value cannot be read
+// (a revoked Proxy throws on property reads; an Error whose `message` getter throws, throws on `.message`) the catch
+// itself used to throw before its log line. Cells: GET /api/anchors/:documentId (the lookup `getAnchorByDocumentId`
+// logs a warn and RETHROWS; the route catch then logs an error and answers the constant 500) and
+// `verifyAnchorsDbReady` (logs an error and throws the constant `Database is required for anchor operations`).
+// An ordinary Error is the control. Harness: the ks1657 anchor-read-fault suite (same mocks; real router, real
+// loopback server). The database stand-in rejects with a plain function, not jest.fn(): a spy inspects what it
+// rejects with and could itself fail on a revoked Proxy before the code under test saw it. Nothing is written.
+const mockState: { toThrow: unknown; warned: unknown[][]; errored: unknown[][]; writes: number } = {
+  toThrow: undefined,
+  warned: [],
+  errored: [],
+  writes: 0,
+};
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: (..._args: unknown[]) => Promise.reject(mockState.toThrow),
+    $executeRaw: (..._args: unknown[]) => {
+      mockState.writes += 1;
+      return Promise.reject(mockState.toThrow);
+    },
+  },
+  getTenantManager: jest.fn(() => null),
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { userId: '11111111-2222-4333-8444-555555555555', role: 'ISSUER_ADMIN' };
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
+    warn: (...args: unknown[]) => {
+      mockState.warned.push(args);
+    },
+    error: (...args: unknown[]) => {
+      mockState.errored.push(args);
+    },
+  },
+}));
+
+import express from 'express';
+import { anchorsRouter, verifyAnchorsDbReady } from '../routes/anchors';
+
+const app = express();
+app.use('/api/anchors', express.json(), anchorsRouter);
+
+const DOC = 'doc-ks1868-lookup-target';
+const DB_READY_MESSAGE = 'Database is required for anchor operations';
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => server?.close());
+
+beforeEach(() => {
+  mockState.toThrow = undefined;
+  mockState.warned.length = 0;
+  mockState.errored.length = 0;
+  mockState.writes = 0;
+  delete process.env.SIMULATE_ANCHORING;
+});
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+async function getAnchor(): Promise<{ status: number; code: string | undefined }> {
+  const res = await fetch(`${baseUrl}/api/anchors/${DOC}`);
+  const body = (await res.json()) as { error?: { code?: string } };
+  return { status: res.status, code: body.error?.code };
+}
+
+describe('KS-1868 the originate anchor catches read the rejection value safely', () => {
+  it('control ks1868 C1 GET /:documentId: an ordinary Error is logged with its own message and the route answers 500', async () => {
+    mockState.toThrow = new Error('Connection terminated unexpectedly');
+    expect(await getAnchor()).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+    expect(mockState.warned).toEqual([['Failed to fetch anchor from DB', { documentId: DOC, error: 'Connection terminated unexpectedly' }]]);
+    expect(mockState.errored).toEqual([['Failed to get anchor', { error: 'Connection terminated unexpectedly' }]]);
+    expect(mockState.writes).toBe(0);
+  });
+
+  it('control ks1868 C2 verifyAnchorsDbReady: an ordinary Error is logged with its own message and the constant error is thrown', async () => {
+    mockState.toThrow = new Error('db down');
+    await expect(verifyAnchorsDbReady()).rejects.toThrow(DB_READY_MESSAGE);
+    expect(mockState.errored).toHaveLength(1);
+    expect(mockState.errored[0][1]).toEqual({ error: 'db down' });
+  });
+
+  it('RED ks1868 R1 GET /:documentId: a revoked Proxy rejection logs both lines with a constant reason and the route answers 500', async () => {
+    mockState.toThrow = revokedProxy();
+    expect(await getAnchor()).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+    expect(mockState.warned).toEqual([['Failed to fetch anchor from DB', { documentId: DOC, error: 'unreadable thrown value' }]]);
+    expect(mockState.errored).toEqual([['Failed to get anchor', { error: 'unreadable thrown value' }]]);
+    expect(mockState.writes).toBe(0);
+  });
+
+  it('RED ks1868 R2 GET /:documentId: an Error whose message getter throws logs both lines with a constant reason and the route answers 500', async () => {
+    mockState.toThrow = getterThrows();
+    expect(await getAnchor()).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+    expect(mockState.warned).toEqual([['Failed to fetch anchor from DB', { documentId: DOC, error: 'unreadable thrown value' }]]);
+    expect(mockState.errored).toEqual([['Failed to get anchor', { error: 'unreadable thrown value' }]]);
+    expect(mockState.writes).toBe(0);
+  });
+
+  it('RED ks1868 R3 verifyAnchorsDbReady: a revoked Proxy rejection logs a constant reason and the constant error is thrown', async () => {
+    mockState.toThrow = revokedProxy();
+    await expect(verifyAnchorsDbReady()).rejects.toThrow(DB_READY_MESSAGE);
+    expect(mockState.errored).toHaveLength(1);
+    expect(mockState.errored[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 verifyAnchorsDbReady: an Error whose message getter throws logs a constant reason and the constant error is thrown', async () => {
+    mockState.toThrow = getterThrows();
+    await expect(verifyAnchorsDbReady()).rejects.toThrow(DB_READY_MESSAGE);
+    expect(mockState.errored).toHaveLength(1);
+    expect(mockState.errored[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
